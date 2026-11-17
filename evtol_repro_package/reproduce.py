"""Reproduce manuscript summary tables from saved LOCO predictions. No model training."""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
from statsmodels.stats.multitest import multipletests

MODELS=['Random Forest','XGBoost','LightGBM','CatBoost','Mission-Phase Transformer','Attention-LSTM-MoE']
TREE={'Random Forest':'random_forest_predictions.csv','XGBoost':'xgboost_predictions.csv','LightGBM':'lightgbm_predictions.csv','CatBoost':'catboost_predictions.csv'}
SEQ_MODELS=['Mission-Phase Transformer','Attention-LSTM-MoE']
EXPECTED={'SOH':(18513,19),'RUL90':(5814,19),'RUL85':(9595,16),'RUL80':(8257,8)}

def validate(df,keys,name,n=None,cells=None):
    required=set(keys)|{'y_true','y_pred'}
    missing=required-set(df.columns)
    if missing: raise ValueError(f'{name}: missing columns {sorted(missing)}')
    if df[list(keys)].isna().any().any() or df[['y_true','y_pred']].isna().any().any(): raise ValueError(f'{name}: missing keys or labels')
    if df.duplicated(list(keys)).any(): raise ValueError(f'{name}: duplicate prediction keys')
    if n is not None and len(df)!=n: raise ValueError(f'{name}: expected {n} rows, got {len(df)}')
    if cells is not None and df['cell_id'].nunique()!=cells: raise ValueError(f'{name}: expected {cells} cells, got {df.cell_id.nunique()}')
    if not np.isfinite(df[['y_true','y_pred']].to_numpy(dtype=float)).all(): raise ValueError(f'{name}: nonfinite predictions')

def metrics(df):
    err=df.y_true.to_numpy(float)-df.y_pred.to_numpy(float)
    per=df.assign(abs_error=np.abs(err)).groupby('cell_id').abs_error.mean()
    return {'observations':len(df),'cells':df.cell_id.nunique(),'pooled_MAE':np.abs(err).mean(),'pooled_RMSE':np.sqrt(np.mean(err**2)),'macro_MAE':per.mean(),'worst_cell_MAE':per.max()}

def cell_mae(df):
    return df.assign(abs_error=(df.y_true-df.y_pred).abs()).groupby('cell_id').abs_error.mean()

def paired_tests(pairs):
    raw=[]
    for label,a,b in pairs:
        ix=a.index.intersection(b.index)
        if len(ix)<2: raise ValueError(f'{label}: fewer than two matched cells')
        d=a.loc[ix]-b.loc[ix]
        p=1.0 if np.allclose(d,0) else float(wilcoxon(d,alternative='two-sided',zero_method='wilcox').pvalue)
        raw.append({'comparison':label,'n_cells':len(ix),'mean_difference':d.mean(),'p_raw':p})
    out=pd.DataFrame(raw)
    out['p_holm']=multipletests(out.p_raw,method='holm')[1]
    return out

def main(root,soh_column):
    pred=root/'predictions'; out=root/'results'; out.mkdir(exist_ok=True)
    missing=[str(pred/f) for f in list(TREE.values())+['sequence_predictions.csv'] if not (pred/f).exists()]
    if missing: raise FileNotFoundError('Copy original prediction files first:\n'+'\n'.join(missing))
    frames={}
    for model,fn in TREE.items():
        d=pd.read_csv(pred/fn)
        validate(d,['cell_id','mission_id'],model,*EXPECTED['SOH'])
        d['cell_id']=d.cell_id.astype(str)
        frames[model]=d
    seq=pd.read_csv(pred/'sequence_predictions.csv')
    validate(seq,['task','model','test_cell','mission_id'],'sequence_predictions.csv')
    # The original notebook uses task/model/test_cell/mission_id. Do not silently guess names.
    print('Sequence task values:',sorted(seq.task.astype(str).unique()))
    print('Sequence model values:',sorted(seq.model.astype(str).unique()))
    mapping_path=root/'configs'/'sequence_mapping.csv'
    if not mapping_path.exists():
        pd.DataFrame(columns=['raw_task','raw_model','task','model']).to_csv(mapping_path,index=False)
        raise ValueError('Fill configs/sequence_mapping.csv with exact raw task/model values printed above, then rerun. Do not guess.')
    mapping=pd.read_csv(mapping_path).dropna()
    if mapping.empty: raise ValueError('configs/sequence_mapping.csv is empty; fill actual task/model mappings')
    if mapping.duplicated(['raw_task','raw_model']).any(): raise ValueError('Duplicate sequence mapping')
    seq=seq.merge(mapping,left_on=['task','model'],right_on=['raw_task','raw_model'],how='left',validate='many_to_one',suffixes=('_raw',''))
    if seq[['task','model']].isna().any().any(): raise ValueError('Unmapped task/model in sequence_predictions.csv')
    seq=seq.drop(columns=['task_raw','model_raw','raw_task','raw_model']).rename(columns={'test_cell':'cell_id'})
    seq.cell_id=seq.cell_id.astype(str)
    for task,(n,c) in EXPECTED.items():
        for model in SEQ_MODELS:
            part=seq[(seq.task==task)&(seq.model==model)]
            validate(part,['cell_id','mission_id'],f'{task}/{model}',n,c)
            if task=='SOH': frames[model]=part.copy()
    # Verify the same SOH prediction keys and labels across all models.
    ref=frames['LightGBM'][['cell_id','mission_id','y_true']].rename(columns={'y_true':'reference_y_true'})
    for model,df in frames.items():
        chk=ref.merge(df[['cell_id','mission_id','y_true']],on=['cell_id','mission_id'],how='outer',indicator=True,validate='one_to_one')
        if not (chk._merge=='both').all() or not np.allclose(chk.reference_y_true,chk.y_true,atol=1e-8,rtol=0):
            raise ValueError(f'SOH keys or true labels mismatch: {model}')
    t1=pd.DataFrame([{'model':m,**metrics(frames[m])} for m in MODELS]);t1.to_csv(out/'table1_soh_metrics.csv',index=False)
    per={m:cell_mae(frames[m]) for m in MODELS}
    t2=paired_tests([(f'LightGBM minus {m}',per['LightGBM'],per[m]) for m in MODELS if m!='LightGBM']);t2.to_csv(out/'table2_soh_wilcoxon.csv',index=False)
    t4=[];t5=[]
    for task in ['RUL90','RUL85','RUL80']:
        a,b=[seq[(seq.task==task)&(seq.model==m)] for m in SEQ_MODELS]
        for m,d in zip(SEQ_MODELS,[a,b]): t4.append({'task':task,'model':m,**metrics(d)})
        row=paired_tests([(task,cell_mae(a),cell_mae(b))]).iloc[0].to_dict()
        # Holm correction must be applied across all three RUL comparisons, not individually.
        t5.append(row)
    t4=pd.DataFrame(t4);t4.to_csv(out/'table4_rul_metrics.csv',index=False)
    t5=pd.DataFrame(t5);t5['p_holm']=multipletests(t5.p_raw,method='holm')[1];t5.to_csv(out/'table5_rul_wilcoxon.csv',index=False)
    # Strata requires current SOH at prediction time, not the SOH five missions ahead.
    health=pred/'soh_current_by_mission.csv'
    if health.exists():
        h=pd.read_csv(health)
        if not {'cell_id','mission_id',soh_column}.issubset(h.columns): raise ValueError(f'{health}: requires cell_id, mission_id, {soh_column}')
        h.cell_id=h.cell_id.astype(str)
        if h.duplicated(['cell_id','mission_id']).any(): raise ValueError('Duplicate health keys')
        strata=[]; bins=[]
        for model,df in frames.items():
            joined=df.merge(h[['cell_id','mission_id',soh_column]],on=['cell_id','mission_id'],how='left',validate='one_to_one')
            if joined[soh_column].isna().any(): raise ValueError(f'{model}: missing current SOH values')
            joined['abs_error']=(joined.y_true-joined.y_pred).abs()
            low=joined[joined[soh_column]<85].groupby('cell_id').abs_error.mean()
            high=joined[joined[soh_column]>=95].groupby('cell_id').abs_error.mean()
            ix=low.index.intersection(high.index)
            if len(ix)!=16: raise ValueError(f'{model}: expected 16 paired low/high cells, got {len(ix)}')
            diff=low.loc[ix]-high.loc[ix]
            p=1.0 if np.allclose(diff,0) else wilcoxon(diff).pvalue
            strata.append({'model':model,'paired_cells':len(ix),'low_macro_MAE':low.loc[ix].mean(),'high_macro_MAE':high.loc[ix].mean(),'difference_low_minus_high':diff.mean(),'p_raw':p})
            joined['soh_bin']=pd.cut(joined[soh_column],[-np.inf,85,90,95,np.inf],right=False,labels=['<85','85–<90','90–<95','≥95'])
            for label,g in joined.groupby('soh_bin',observed=True):
                cm=g.groupby('cell_id').abs_error.mean()
                bins.append({'model':model,'soh_bin':str(label),'observations':len(g),'cells':len(cm),'macro_MAE':cm.mean()})
        t3=pd.DataFrame(strata);t3['p_holm']=multipletests(t3.p_raw,method='holm')[1]
        t3.to_csv(out/'table3_soh_strata.csv',index=False)
        pd.DataFrame(bins).to_csv(out/'figure2_soh_bins_data.csv',index=False)
    else:
        print('SKIP Table 3 and Figure 2: add predictions/soh_current_by_mission.csv with current-mission SOH, not target SOH.')
    print('Saved tables to',out)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--soh-column',default='soh_current_pct');a=p.parse_args();main(a.root,a.soh_column)

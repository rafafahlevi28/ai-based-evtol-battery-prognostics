# eVTOL prognostics: manuscript analysis reproducibility

This is a **prediction-level analysis** package, not a complete model-training reproduction. It was prepared by inspecting `evtol_revision_audit.ipynb` and does **not** contain the user's prediction data. It does not alter or validate the user's existing GitHub repository.

## Required original artifacts

Copy the following **actual** files into `predictions/`:

- `random_forest_predictions.csv` from `eVTOL_table5_work/final_fast_loco_fixed/`
- `xgboost_predictions.csv` from the same directory
- `lightgbm_predictions.csv` from the same directory
- `catboost_predictions.csv` from `eVTOL_table5_work/corrected_train_only/` (**30 features, train-only imputation**)
- `sequence_predictions.csv` from `eVTOL_benchmark_reproduction_v2/table3_full_run/`

**Do not use** `final_fast_loco_fixed/catboost_loco_predictions.csv`, the alternative 37-feature file that includes future-label-derived features.

For SOH degradation strata, also prepare `predictions/soh_current_by_mission.csv` with columns `cell_id,mission_id,soh_current_pct`. The SOH must be the **current mission SOH** corresponding to each prediction row, not the future SOH target. The source notebook does not include this portable export.

## Run

```bash
python -m pip install -r requirements.txt
python reproduce.py
```

On the first run, the script prints the raw `task` and `model` values from `sequence_predictions.csv`. Fill `configs/sequence_mapping.csv` with rows mapping each pair to the canonical values:

- task: `SOH`, `RUL90`, `RUL85`, `RUL80`
- model: `Mission-Phase Transformer`, `Attention-LSTM-MoE`

Then rerun `python reproduce.py`. This explicit mapping avoids silently guessing the naming conventions in the source CSV.

Outputs: `results/table1_soh_metrics.csv`, `table2_soh_wilcoxon.csv`, `table4_rul_metrics.csv`, `table5_rul_wilcoxon.csv`; and, when current SOH data is supplied, `table3_soh_strata.csv` and `figure2_soh_bins_data.csv`.

**Important:** This package does not yet regenerate the exact manuscript figures or bootstrap intervals, because the underlying plotting code, figure population definitions, and bootstrap seed/configuration have not all been established. Exact numerical agreement with manuscript tables must be checked after loading real data.

## Provenance and remaining work

- `configs/experiment_manifest_template.csv` is a template. Fill artifact hashes, source commit, hyperparameters, and verified split information from original artifacts.
- `configs/cell_selection_template.csv` requires the actual 19 cell IDs and selection criteria.
- Add the exact 30 tabular features and 20 sequence features as verified manifests. Do not invent them.
- Verify all sequence-fold scaler fit calls and record train/validation/test cell identities.
- Supply a documented, publicly accessible data download process and dependency lockfile if full rerun is desired.
- Never commit secrets, Google Drive tokens, or unpublished/private files.

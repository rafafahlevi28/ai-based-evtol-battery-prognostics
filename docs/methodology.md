# Research Methodology

## 1. Research Overview

This repository documents a quantitative comparative study of artificial intelligence (AI) pipelines for lithium-ion battery prognostics in electric Vertical Take-Off and Landing (eVTOL) applications.

The study evaluates two prognostic tasks: **State of Health (SOH) prediction five missions ahead** and **Remaining Useful Life (RUL) estimation** at SOH thresholds of 90%, 85%, and 80%.

The research builds upon the eVTOL battery dataset described by Bills et al. (2023) and the mission-phase prognostics benchmark developed by Yan and Wiston (2026).

Its primary contribution is an expanded evaluation of prediction accuracy, generalization across unseen battery cells, statistical differences between pipelines, and prediction errors under different battery health conditions.

The study does not introduce a new model architecture or claim to establish operational readiness for Urban Air Mobility (UAM) in Indonesia.

## 2. Dataset and Target Construction

### 2.1 Data Sources

The experimental analysis uses reconstructed mission-level data associated with the eVTOL lithium-ion battery dataset and the reference benchmark.

**Original dataset:**

https://kilthub.cmu.edu/articles/dataset/eVTOL_Battery_Dataset/14226830

**Reference benchmark:**

https://github.com/MusaWiston/Mission-Phase-Feature-Learning-for-eVTOL-Battery-Prognostics-with-ML

The original dataset, benchmark implementation, and research outputs must be distinguished when documenting data provenance.

### 2.2 SOH Prediction Target

The SOH task predicts battery health **five missions ahead**.

The evaluation includes **18,513 observations from 19 battery cells**.

Prediction errors are expressed in SOH percentage points.

### 2.3 RUL Prediction Targets

RUL is defined as the remaining number of missions until a specified SOH threshold is reached.

Three thresholds are evaluated:

| Target | Observations | Battery cells |
|---|---:|---:|
| RUL90 | 5,814 | 19 |
| RUL85 | 9,595 | 16 |
| RUL80 | 8,257 | 8 |

The evaluation populations differ across thresholds. Consequently, error values from different RUL targets should not be interpreted as a controlled comparison of intrinsic prediction difficulty.

### 2.4 Scope of SOC

State of Charge (SOC) estimation is included in the reference benchmark by Yan and Wiston (2026).

However, **SOC is not included in the final comparative results reported in this study**. No SOC performance claims are made in the associated manuscript.

## 3. Model Pipelines

### 3.1 SOH Prediction

Six pipelines are evaluated:

1. Random Forest
2. XGBoost
3. LightGBM
4. CatBoost
5. Mission-Phase Transformer
6. Attention-LSTM-Mixture of Experts (Attention-LSTM-MoE)

The four tree-based pipelines use **30 mission-level tabular features**.

The two sequential pipelines use **20 features per mission**, with input histories of up to **20 missions**.

All six SOH pipelines are evaluated against the same prediction target and held-out evaluation population.

Because the feature representations differ between pipeline families, the comparison does not isolate the effect of model architecture alone.

### 3.2 RUL Prediction

Two sequential models are evaluated for RUL:

- Mission-Phase Transformer
- Attention-LSTM-MoE

Both are evaluated separately for RUL90, RUL85, and RUL80.

No RUL performance comparison involving Random Forest, XGBoost, LightGBM, or CatBoost is claimed in the final analysis.

## 4. Data Preparation and Leakage Control

The study uses mission-level feature representations and reconstructed experimental artifacts.

Data preparation and feature construction must preserve the temporal relationship between prediction inputs and future targets.

For cell-held-out evaluation, any preprocessing parameter learned from data, such as an imputation statistic, must be estimated using training data only.

The available tree-pipeline configuration documents a training-fold median-imputation procedure.

Prediction artifacts were also reviewed for features that could directly reveal future targets. An alternative CatBoost result involving target-related leakage features was excluded from the primary comparison.

Only the retained CatBoost prediction results are included in the reported analysis.

Not every training-time configuration or intermediate preprocessing operation has been independently reconstructed from the available artifacts. Such details should not be inferred where supporting records are unavailable.

## 5. Leave-One-Cell-Out Evaluation

The study adopts a **Leave-One-Cell-Out (LOCO)** evaluation protocol.

For each evaluation fold:

1. One battery cell is designated as the held-out test cell.
2. The remaining cells provide the training data.
3. The model generates predictions for the held-out cell.
4. Prediction errors are calculated and associated with that cell.
5. The procedure is repeated across eligible cells.

This protocol evaluates generalization to cells not represented in the corresponding training fold.

LOCO reduces within-cell overlap between training and evaluation, but it does not by itself establish generalization to new battery chemistries, battery packs, aircraft, or operating environments.

## 6. Evaluation Metrics

### 6.1 Pooled MAE and RMSE

**Mean Absolute Error (MAE)** measures the average absolute prediction error across evaluated observations.

**Root Mean Squared Error (RMSE)** gives greater weight to larger prediction errors.

Both metrics are calculated separately for each model and prediction target.

### 6.2 Cell-Level Error Metrics

The study additionally evaluates:

- **Cell-level MAE:** MAE calculated separately for each held-out battery cell.
- **Macro-MAE:** The unweighted mean of cell-level MAE values.
- **Worst-cell MAE:** The highest MAE observed among the evaluated cells.
- **Cell-level error distributions:** Variation in prediction performance across held-out cells.

These metrics complement pooled results, which may be influenced by unequal numbers of observations across cells.

## 7. Statistical Analysis

### 7.1 SOH Pipeline Comparisons

LightGBM is used as a post-hoc exploratory reference because it achieved the lowest pooled SOH MAE.

Paired Wilcoxon signed-rank tests compare cell-level MAE values between LightGBM and each of the five other pipelines.

The Holm procedure adjusts for multiple comparisons.

The unit of paired statistical analysis is the **battery cell**, not the individual mission observation.

Because the reference pipeline was selected after inspecting the results, statistical conclusions are interpreted as exploratory.

### 7.2 SOH Degradation-Strata Analysis

Prediction errors are compared between:

- **Low SOH:** below 85%.
- **High SOH:** at least 95%.

The paired analysis includes **16 cells** with observations in both strata.

For each pipeline, the difference is calculated as:

**ΔMAE = MAE at low SOH − MAE at high SOH**

A positive value indicates higher prediction error in the low-SOH stratum.

Paired Wilcoxon tests and Holm correction are applied across the six pipelines.

These comparisons are observational and do not establish a causal relationship between degradation and prediction error.

### 7.3 RUL Model Comparisons

The two sequential models are compared using paired cell-level MAE values for each RUL threshold.

Three Wilcoxon tests are performed, with Holm correction across the thresholds.

The difference is defined as:

**ΔMAE = MAE of Transformer − MAE of Attention-LSTM-MoE**

Positive differences favor Attention-LSTM-MoE, while negative differences favor Mission-Phase Transformer.

Cell-level bootstrap confidence intervals are used where available to characterize uncertainty.

Statistically nonsignificant differences are not interpreted as evidence of model equivalence.

## 8. Experimental Findings

### 8.1 SOH Results

LightGBM achieved the lowest pooled SOH MAE of **0.525 percentage points**.

However, Random Forest achieved a lower worst-cell MAE than LightGBM.

After Holm correction, LightGBM differed significantly from Mission-Phase Transformer and Attention-LSTM-MoE, but not from XGBoost, Random Forest, or CatBoost.

### 8.2 SOH Degradation Analysis

All four tree-based pipelines exhibited significantly higher cell-level MAE in the low-SOH stratum than in the high-SOH stratum.

The two sequential pipelines did not show statistically significant differences between the evaluated strata.

These results do not establish that the sequential models are unaffected by battery degradation.

### 8.3 RUL Results

The preferred model varies by threshold and evaluation metric.

After Holm correction, no statistically significant cell-level MAE difference was identified between Mission-Phase Transformer and Attention-LSTM-MoE for RUL90, RUL85, or RUL80.

RUL80 results require particular caution because only eight cells were eligible for evaluation.

## 9. Reproducibility and Research Artifacts

The experimental notebook is intended to document data reconstruction, model evaluation, and statistical analysis.

The repository should distinguish among:

- Original third-party datasets.
- Reference benchmark code and methods.
- Reconstructed experimental data.
- Model prediction artifacts.
- Independently calculated evaluation metrics.
- Tables and figures prepared for the manuscript.

Reproducing the reported metrics requires access to the appropriate datasets, model outputs, preprocessing configurations, and evaluation procedures.

The presence of a notebook and saved predictions does not, by itself, prove that every training pipeline can be reproduced end-to-end from a clean environment.

The repository should document any external Google Drive dependencies, unavailable files, and configuration details that remain unverified.

## 10. Replication Status

**SOH:** Comparative prediction metrics, cell-level analyses, and statistical comparisons have been obtained and checked against the available experimental outputs. Complete independent verification of every training configuration remains limited by the available artifacts.

**RUL:** Results for RUL90, RUL85, and RUL80, including paired statistical comparisons, have been obtained and analyzed. The eligible evaluation population differs by threshold.

**SOC:** Not included in the final experimental claims of this study.

**Operational deployment:** Not evaluated.

The project is therefore described as a **secondary comparative analysis and partial experimental reproduction**, rather than a fully independent reimplementation of every component in the reference benchmark.

## 11. Research Limitations

The analysis depends on secondary data and reconstructed experimental artifacts.

The tree-based and sequential pipelines use different feature representations, limiting architecture-specific conclusions.

The eligible number of cells differs across RUL thresholds, especially for RUL80.

The study does not validate predictions at the battery-pack level or within an operational eVTOL battery management system.

No Indonesian flight-operation dataset or aviation certification assessment is included.

Accordingly, implications for UAM in Indonesia are prospective and should not be interpreted as evidence of commercial or safety-critical deployment readiness.

## 12. References and Attribution

**Bills et al. (2023).** eVTOL lithium-ion battery dataset. *Scientific Data*. https://doi.org/10.1038/s41597-023-02180-5

**Yan, S., & Wiston, M. (2026).** Mission-Phase Feature Learning for eVTOL Li-Ion Battery Prognostics: A Leakage-Safe Cell-Held-Out Benchmark for SOC, SOH, and RUL. *Batteries, 12*(9), 322. https://doi.org/10.3390/batteries12090322

Original datasets and reference implementations remain subject to their respective licenses and attribution requirements.

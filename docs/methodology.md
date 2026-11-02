# Research Methodology

## 1. Overview

This repository investigates the performance of artificial intelligence (AI) models for electric vertical take-off and landing (eVTOL) battery prognostics, with implications for autonomous urban air mobility (UAM) in Indonesia.

The study focuses on battery state estimation and remaining useful life prediction. It uses the CMU eVTOL Battery Dataset and refers to the published study:

*Mission-Phase Feature Learning for eVTOL Li-Ion Battery Prognostics: A Leakage-Safe Cell-Held-Out Benchmark for SOC, SOH, and RUL.*

The current repository represents a **partial replication and ongoing experimental analysis**. Results are documented according to the experiments that have actually been conducted and verified.

## 2. Dataset

### 2.1 Data Source

The experiments use the CMU eVTOL Battery Dataset.

The dataset is intended to support research into battery behavior and prognostics under eVTOL-related operating conditions.

Researchers should consult the original dataset documentation for information about its structure, experimental conditions, variables, and usage restrictions.

### 2.2 Data Preparation

Data preparation should be performed before model training and evaluation.

The preparation process may include:

- Inspecting the available files and data structure.
- Checking for missing, invalid, or inconsistent observations.
- Applying documented data-quality filtering criteria.
- Identifying battery cells and relevant mission or operational information.
- Constructing model inputs and target variables.
- Recording any exclusions and preprocessing decisions.

The exact preprocessing steps must be documented alongside the corresponding notebook or experiment. No filtering rule should be assumed to have been applied unless it is implemented and verified in the code.

## 3. Prognostic Tasks

The reference study considers three battery prognostic tasks.

### 3.1 State of Charge (SOC)

State of Charge estimation concerns the estimation of the battery's current charge level.

The implementation, target definition, input features, and evaluation results for SOC must be documented when the corresponding experiment has been verified.

### 3.2 State of Health (SOH)

State of Health estimation concerns the assessment of battery condition relative to an appropriate reference state.

The repository includes SOH-related model evaluation. The current analysis compares machine learning models using error-based evaluation metrics.

The specific target construction, feature set, training procedure, and validation strategy should be recorded in the corresponding notebook.

### 3.3 Remaining Useful Life (RUL)

Remaining Useful Life prediction estimates the remaining operational life of a battery relative to a defined end-of-life criterion.

RUL evaluation depends on the selected threshold, the definition of a mission or operational cycle, and the method used to calculate remaining life.

The threshold definitions and evaluation procedures must be explicitly documented in the relevant experiment.

## 4. Data Quality and Filtering

Data-quality filtering is used to identify observations that may be unsuitable for analysis.

The filtering criteria should be defined before model evaluation and documented in the relevant notebook or results table.

For reproducibility, each filtering rule should specify:

- The condition being checked.
- The reason for applying the rule.
- The number of observations or records affected, where available.
- Whether the rule is applied consistently across training and evaluation data.

Filtering decisions should not use information from the evaluation targets in a way that introduces data leakage.

## 5. Model Development and Evaluation

The repository investigates AI and machine learning approaches for battery prognostics.

Models should be trained and evaluated using a documented experimental procedure. Model comparisons should use consistent target definitions, data splits, and evaluation metrics wherever applicable.

For each experiment, the following information should be recorded:

1. Model name and implementation.
2. Input features and target variable.
3. Training and evaluation data.
4. Validation or holdout strategy.
5. Model parameters and relevant configuration.
6. Evaluation metrics.
7. Random seeds and software dependencies, where applicable.

The models and configurations reported in the results must correspond to the implementations used in the experiments.

## 6. Cell-Held-Out Evaluation and Data Leakage

Battery datasets may contain observations from multiple cells. Evaluation procedures should account for the possibility that observations from the same cell share characteristics.

Where a cell-held-out evaluation is implemented, the held-out cell must not contribute observations to model training.

Preprocessing operations that learn parameters from data, such as feature scaling or imputation, should be fitted using training data only and then applied to the held-out data.

Any feature construction or filtering procedure must be reviewed to ensure that information unavailable at prediction time is not inadvertently used.

The repository should distinguish between procedures confirmed to be implemented and procedures that remain to be verified against the reference study.

## 7. Evaluation Metrics

The repository uses error-based metrics for model evaluation where applicable.

### 7.1 Mean Absolute Error (MAE)

MAE measures the average absolute difference between predicted and reference values.

Lower MAE indicates smaller average absolute prediction errors.

### 7.2 Root Mean Squared Error (RMSE)

RMSE measures the square root of the average squared prediction errors.

Because errors are squared before averaging, RMSE places greater emphasis on larger errors than MAE does.

### 7.3 Additional Error Analysis

Where implemented, results may also include cell-level comparisons, error distributions, or high-percentile error statistics.

These analyses help identify variation in model performance across battery cells and reveal whether average performance conceals larger errors in particular cases.

The reported metrics should always be interpreted in the context of the target variable, its units, and the evaluation procedure.

## 8. Results and Reporting

Experimental results are organized into tables, figures, and supporting notebooks.

Each reported result should identify:

- The task being evaluated.
- The model or experimental configuration.
- The evaluation dataset or held-out cells.
- The metric and its units.
- Whether the value comes from the published reference study or an independent run in this repository.

Reference-study results and independently reproduced results must be clearly distinguished.

Differences between the reference values and independent runs should be investigated rather than silently replaced or treated as equivalent.

## 9. Reproducibility

To support reproducibility, the repository should contain the relevant notebooks, dependency information, result files, and methodological documentation.

A reproducible experiment should provide enough information to identify the data inputs, preprocessing steps, model configuration, evaluation procedure, and output metrics.

Dataset access instructions and any applicable data-use restrictions should be followed.

Results should not be described as fully reproduced until the corresponding procedure has been independently executed and checked.

## 10. Current Replication Status

This repository is a work in progress.

The current status should be reported separately for each task:

- **SOH:** Model evaluation has been explored; the full procedure and results require systematic verification.
- **SOC:** The implementation and results require verification before replication can be claimed.
- **RUL:** Threshold definitions, evaluation procedures, and results require verification before replication can be claimed.

These status descriptions should be updated as the experiments are checked and completed.

## 11. Limitations

The findings depend on the dataset, feature construction, model configurations, and evaluation procedures used in the experiments.

Performance on the available dataset does not, by itself, establish that a model is ready for deployment in an autonomous eVTOL aircraft.

Further validation would be needed to assess robustness under different operating conditions, battery aging patterns, and real-world flight missions.

Implications for autonomous urban air mobility in Indonesia should therefore be discussed as research implications rather than as evidence of operational readiness.

## 12. References

1. *Mission-Phase Feature Learning for eVTOL Li-Ion Battery Prognostics: A Leakage-Safe Cell-Held-Out Benchmark for SOC, SOH, and RUL.* Batteries, 12(9), 322. DOI: [10.3390/batteries12090322](https://doi.org/10.3390/batteries12090322).

2. CMU eVTOL Battery Dataset. Refer to the original dataset repository or publication for dataset details, documentation, and usage conditions.

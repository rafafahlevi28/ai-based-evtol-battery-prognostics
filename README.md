# AI Performance for Autonomous eVTOL Battery Prognostics

**Project Status: Partial Replication — Work in Progress**

## 1. Project Overview

This repository documents an ongoing partial replication and evaluation of AI-based battery prognostics for electric Vertical Take-Off and Landing (eVTOL) systems. The research examines machine learning performance and its potential implications for autonomous Urban Air Mobility (UAM) in Indonesia.

The project uses the CMU eVTOL Battery Dataset and refers to the published benchmark by Yan and Wiston (2026), *Mission-Phase Feature Learning for eVTOL Li-Ion Battery Prognostics: A Leakage-Safe Cell-Held-Out Benchmark for SOC, SOH, and RUL*.

The replication is still in progress. The implementation and results have not yet been fully verified against all methods, evaluation protocols, and reported findings in the reference paper.

## 2. Research Objectives

This project aims to:

- Examine conventional machine learning and sequential learning approaches for eVTOL battery prognostics.
- Investigate State of Charge (SOC), State of Health (SOH), and Remaining Useful Life (RUL) prediction.
- Evaluate model performance using metrics such as Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE).
- Examine generalization across battery cells and the importance of leakage-safe evaluation.
- Discuss the technical and operational considerations for potential autonomous eVTOL-based UAM applications in Indonesia.

## 3. Dataset and Reference Study

### Dataset

The project uses the CMU eVTOL Battery Dataset as its primary data source. The dataset contains battery measurements collected under flight-related and charging conditions.

Dataset source:  
https://kilthub.cmu.edu/articles/dataset/eVTOL_Battery_Dataset/14226830

Dataset access and redistribution are subject to the original dataset's licensing and usage conditions.

### Reference Study

Yan, S., & Wiston, M. (2026). *Mission-Phase Feature Learning for eVTOL Li-Ion Battery Prognostics: A Leakage-Safe Cell-Held-Out Benchmark for SOC, SOH, and RUL*. Batteries, 12, 322.

https://doi.org/10.3390/batteries12090322

The reference study provides the methodological basis for the replication. Results reported in the publication are distinguished from results independently obtained in this repository.

## 4. Experimental Scope

The experimental workflow includes:

1. Dataset inspection and preprocessing.
2. Construction and verification of prognostic targets.
3. Implementation and evaluation of selected machine learning and sequential models.
4. Calculation of prediction errors using appropriate evaluation metrics.
5. Examination of performance across individual battery cells.
6. Comparison with the reference benchmark, where the methods and evaluation protocols are sufficiently aligned.

Experiments and verification are ongoing. The completeness of each task is documented separately rather than assuming that all three prognostic tasks have been fully replicated.

## 5. Current Replication Status

### State of Health (SOH)

SOH experiments have been executed, including leave-one-cell-out evaluation across 19 battery cells. The available notebook contains training logs and model evaluation outputs, including MAE and RMSE.

However, the experimental results still require systematic verification against the reference paper's data processing, target construction, model configuration, and evaluation protocol.

### State of Charge (SOC)

SOC-related code and visualizations are present in the research workflow. The extent to which these experiments reproduce the reference methodology and results remains to be verified.

### Remaining Useful Life (RUL)

RUL-related code, tables, and evaluation outputs are present. Further checks are needed to verify target construction, threshold definitions, evaluation procedures, and consistency with the reference benchmark.

**Overall status:** Partial replication. The presence of code or output for a task does not by itself establish that its full experimental procedure and published results have been reproduced.

## 6. Repository Structure

The repository is intended to organize the research materials as follows:

- `data/`: Dataset documentation and information about data access.
- `notebooks/`: Experimental notebooks and analysis.
- `results/tables/`: Verified experimental result tables.
- `results/figures/`: Visualizations generated from experimental outputs.
- `docs/methodology.md`: Experimental methodology and evaluation procedures.
- `docs/replication_status.md`: Progress and outstanding verification tasks.
- `docs/references.md`: Reference papers and dataset sources.

Only files that are available and relevant to the project will be included. The repository structure will be updated as the project develops.

## 7. Reproducibility and Limitations

Reproducing the reference study requires consistency in dataset processing, feature construction, target definitions, model settings, and validation procedures. Differences in these components may lead to results that differ from those reported in the publication.

The current work should therefore be interpreted as an ongoing partial replication rather than a complete reproduction of the reference benchmark.

Experimental results do not establish operational readiness for autonomous eVTOL systems or validate battery prognostics under real-world Indonesian flight conditions. Further verification, representative operational data, and appropriate safety assessments are needed before practical deployment can be considered.

## 8. Research Contribution

This repository aims to make the replication process more transparent by documenting experimental procedures, available outputs, differences from the reference benchmark, and remaining limitations.

Its longer-term goal is to support a more rigorous assessment of AI-based battery prognostics and the requirements for potential autonomous eVTOL-based UAM applications in Indonesia.

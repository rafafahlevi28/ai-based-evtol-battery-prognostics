# AI-Based eVTOL Battery Prognostics

### Comparative Evaluation of AI Models for Battery SOH and RUL Prediction in Urban Air Mobility

## Overview

This repository contains research materials for evaluating artificial intelligence (AI) pipelines for lithium-ion battery prognostics in electric Vertical Take-Off and Landing (eVTOL) applications.

The study focuses on predicting **State of Health (SOH)** and **Remaining Useful Life (RUL)** using machine learning and deep learning approaches. It investigates predictive accuracy, generalization across unseen battery cells, statistical differences between models, and prediction errors under different battery degradation conditions.

The research is motivated by the potential development of **Urban Air Mobility (UAM) in Indonesia**, where reliable battery health monitoring may support maintenance planning and operational risk assessment.

## Research Objectives

This study addresses three research questions:

- **RQ1:** How do six AI pipelines compare in predicting battery SOH on previously unseen battery cells?
- **RQ2:** How do SOH prediction errors vary across battery cells and degradation conditions, and are these differences statistically significant?
- **RQ3:** How do Mission-Phase Transformer and Attention-LSTM-MoE compare in predicting RUL at SOH thresholds of 90%, 85%, and 80%?

## Dataset

The research builds upon the eVTOL lithium-ion battery dataset published by **Bills et al. (2023)** and the mission-phase battery prognostics benchmark developed by **Yan and Wiston (2026)**.

Original dataset:

https://kilthub.cmu.edu/articles/dataset/eVTOL_Battery_Dataset/14226830

Reference benchmark repository:

https://github.com/MusaWiston/Mission-Phase-Feature-Learning-for-eVTOL-Battery-Prognostics-with-ML

The SOH evaluation includes **18,513 observations from 19 battery cells**.

RUL evaluation datasets vary according to the SOH threshold:

| Target | Observations | Battery Cells |
|---|---:|---:|
| RUL90 | 5,814 | 19 |
| RUL85 | 9,595 | 16 |
| RUL80 | 8,257 | 8 |

The original dataset and reference benchmark remain the intellectual contributions of their respective authors. Their use must comply with the applicable licenses and attribution requirements.

## Methodology

The research adopts a quantitative comparative approach based on secondary data analysis and experimental reproduction.

A **Leave-One-Cell-Out (LOCO)** evaluation protocol is used to assess model generalization to battery cells excluded from training.

For SOH prediction, six AI pipelines are evaluated:

1. Random Forest
2. XGBoost
3. LightGBM
4. CatBoost
5. Mission-Phase Transformer
6. Attention-LSTM-Mixture of Experts (Attention-LSTM-MoE)

The SOH prediction horizon is **five missions ahead**.

Tree-based pipelines use 30 mission-level tabular features, while sequential pipelines use 20 features per mission with a maximum history of 20 missions.

For RUL prediction, Mission-Phase Transformer and Attention-LSTM-MoE are evaluated at three SOH thresholds: 90%, 85%, and 80%.

Evaluation metrics include:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- Macro-MAE across battery cells
- Worst-cell MAE
- Paired Wilcoxon signed-rank tests
- Holm correction for multiple comparisons
- Cell-level bootstrap confidence intervals

Because the tree-based and sequential pipelines use different feature representations, their results should not be interpreted as a controlled comparison of model architectures alone.

## Experimental Results

### SOH Prediction

| Model | MAE | RMSE | Macro-MAE |
|---|---:|---:|---:|
| LightGBM | **0.525** | **0.759** | **0.545** |
| XGBoost | 0.571 | 0.824 | 0.583 |
| Random Forest | 0.600 | 0.852 | 0.592 |
| CatBoost | 0.804 | 1.324 | 0.713 |
| Mission-Phase Transformer | 1.374 | 2.254 | 1.375 |
| Attention-LSTM-MoE | 1.434 | 2.147 | 1.488 |

All SOH prediction errors are expressed in percentage points.

LightGBM achieved the lowest pooled SOH MAE. However, paired statistical tests with Holm correction identified significant differences only between LightGBM and the two sequential pipelines.

The comparisons with XGBoost, Random Forest, and CatBoost were not statistically significant.

### Battery Degradation Analysis

Prediction errors were compared between low-SOH (<85%) and high-SOH (≥95%) conditions using 16 eligible battery cells.

All four tree-based pipelines exhibited significantly higher cell-level prediction errors under low-SOH conditions after Holm correction.

The two sequential pipelines did not show statistically significant differences between these SOH strata.

These findings describe associations in the evaluated data and do not establish a causal effect of battery degradation.

### RUL Prediction

| Target | Model | MAE | RMSE |
|---|---|---:|---:|
| RUL90 | Mission-Phase Transformer | 36.869 | 67.287 |
| RUL90 | Attention-LSTM-MoE | 37.170 | 55.169 |
| RUL85 | Mission-Phase Transformer | 73.476 | 95.475 |
| RUL85 | Attention-LSTM-MoE | 67.478 | 89.401 |
| RUL80 | Mission-Phase Transformer | 175.467 | 233.326 |
| RUL80 | Attention-LSTM-MoE | 180.636 | 222.323 |

RUL prediction errors are expressed in missions.

No statistically significant differences were identified between the two sequential models across the three RUL thresholds after Holm correction.

The absence of statistical significance should not be interpreted as evidence of model equivalence.

## Research Contributions

The main contribution of this study is an expanded comparative evaluation of battery prognostics pipelines, focusing on:

- Generalization to previously unseen battery cells.
- Statistical comparisons of SOH prediction performance.
- Cell-level prediction error distributions.
- Prediction errors across different SOH degradation conditions.
- RUL prediction comparisons across multiple SOH thresholds.

This research does not claim to introduce a new AI architecture or a new LOCO evaluation protocol.

Instead, it builds upon the reference

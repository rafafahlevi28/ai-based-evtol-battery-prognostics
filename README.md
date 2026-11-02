# AI Performance for Autonomous eVTOL Battery Prognostics

## Project Overview

This repository documents an ongoing replication and evaluation study of AI-based battery prognostics for electric Vertical Take-Off and Landing (eVTOL) systems. The research examines the potential implications of battery prognostics for autonomous Urban Air Mobility (UAM) in Indonesia.

The study uses the CMU eVTOL Battery Dataset and refers to the published benchmark by Yan and Wiston, Mission-Phase Feature Learning for eVTOL Li-Ion Battery Prognostics: A Leakage-Safe Cell-Held-Out Benchmark for SOC, SOH, and RUL.

## Research Objectives

The objectives of this project are to:

- Examine machine learning and deep learning approaches for eVTOL battery prognostics.
- Evaluate model performance for State of Charge (SOC), State of Health (SOH), and Remaining Useful Life (RUL), as experiments are completed.
- Investigate generalization across battery cells and the importance of reliable evaluation protocols.
- Discuss the technical and operational considerations for potential autonomous eVTOL applications in Indonesia.

## Dataset

The study uses the CMU eVTOL Battery Dataset as the primary data source.

The dataset provides battery measurements under flight-related and charging conditions. Its use in this project follows the research scope of the reference benchmark.

Dataset files are not necessarily redistributed in this repository. Please refer to the original dataset source and its applicable access and usage conditions.

## Reference Study

Yan, S., & Wiston, M. (2026). Mission-Phase Feature Learning for eVTOL Li-Ion Battery Prognostics: A Leakage-Safe Cell-Held-Out Benchmark for SOC, SOH, and RUL. Batteries, 12, 322.

DOI: https://doi.org/10.3390/batteries12090322

The reference study is used to guide the replication process and interpret the experimental findings. Results reported in the reference paper are distinguished from results independently obtained in this project.

## Methodology

The planned workflow includes:

1. Dataset inspection and preprocessing.
2. Construction and verification of battery prognostic targets.
3. Implementation of selected machine learning and deep learning models.
4. Model evaluation using appropriate prediction metrics.
5. Assessment of generalization across battery cells where implemented.
6. Comparison with the reference benchmark and discussion of implications for UAM in Indonesia.

The implementation of these steps is ongoing. The repository will document the methods and experiments that have actually been completed.

## Replication Status

*Status: Work in Progress*

This project has not yet fully replicated all experiments and results reported in the reference study.

The scope and completeness of the replication will be updated as implementation, validation, and result verification progress. Any reported findings will be identified according to whether they originate from the reference paper or from experiments independently conducted in this repository.

## Repository Structure

- data/: Dataset documentation and information about data access.
- notebooks/: Experimental notebooks for battery prognostics tasks.
- results/tables/: Verified experimental result tables.
- results/figures/: Visualizations generated from experimental results.
- docs/methodology.md: Detailed experimental methodology.
- docs/replication_status.md: Replication progress and outstanding tasks.
- docs/references.md: Research references used in the project.

## Limitations

The findings are limited by the experiments completed and verified at each stage. Experimental results alone do not establish operational readiness for autonomous eVTOL systems or validate performance under real-world Indonesian flight conditions.

Further verification, broader operational data, and appropriate safety assessments would be required before practical deployment could be considered.

## Research Context

This repository supports academic research into AI-based battery prognostics. It is intended to improve transparency regarding experimental methods, replication progress, model performance, and the limitations of the available evidence.

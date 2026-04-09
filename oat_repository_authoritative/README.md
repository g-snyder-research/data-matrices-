# A Reference-Aware Pipeline for Transforming Semi-Structured Clinical Laboratory Reports into Auditable Feature Matrices for Neuroscience Research

## Overview

This repository contains de-identified derived data, analysis code, and documentation for the associated manuscript:

> Snyder, G. J. A reference-aware pipeline for transforming semi-structured clinical laboratory reports into auditable feature matrices for neuroscience research.

The repository documents a four-step workflow that converts semi-structured urinary organic acid testing (OAT) report data into continuous, reference-interval-aware analyte features for multivariate research use. The broader motivation is improved biological phenotyping in heterogeneous neurodevelopmental and neurobehavioral conditions that still rely heavily on behavioral characterization.

## Repository contents

| File | Description |
|------|-------------|
| `oat_pipeline.py` | Public reproduction script that rebuilds deposited outputs from `audit_table_long.csv` |
| `feature_matrix_75.csv` | De-identified 10 × 75 participant-by-feature matrix used for the primary PCA |
| `feature_matrix_73_no_ketones.csv` | De-identified 10 × 73 participant-by-feature matrix excluding acetoacetic and 3-hydroxybutyric acids |
| `audit_table_long.csv` | Long-format audit table linking each transformed feature to its parsed value, printed reference interval, interval type, parsed bounds, source flag, and recomputed flag |
| `pca_scores_75.csv` | Participant scores for PC1 and PC2 from the primary PCA |
| `pca_loadings_75.csv` | Feature loadings for PC1 and PC2 from the primary PCA |
| `data_dictionary_feature_matrix.csv` | Variable dictionary for the feature-matrix files |
| `data_dictionary_audit_table.csv` | Variable dictionary for the audit table |
| `synthetic_example_input.csv` | Fully synthetic example input demonstrating the parser input schema |
| `output/` | Regenerated local outputs written by the public reproduction script, including manuscript-support tables, PCA files, the PCA figure, and supplementary rank-based sensitivity outputs |
| `supplementary/` | Deposited rank-based PCA sensitivity outputs used to assess robustness of the primary ordination to transformation choice |
| `manuscript_updates/` | Manuscript-ready replacement text and authoritative tables for the current draft |

## Relationship among deposited files

The deposited files are organized in three layers.

1. `audit_table_long.csv` is the authoritative audit layer. It preserves the participant-level parsed value, printed reference interval, interval type, parsed bounds, source-report flag, recomputed flag, and transformed score for each participant-analyte pair.

2. `feature_matrix_75.csv` and `feature_matrix_73_no_ketones.csv` are wide participant-by-feature matrices derived from the audit table.

3. `pca_scores_75.csv` and `pca_loadings_75.csv` are downstream dimensionality-reduction outputs derived from the 75-feature matrix.

## De-identification

This repository does not include raw clinical OAT reports. Raw reports are excluded because they contain human-subject information and proprietary laboratory formatting.

Public repository participant labels are repository-specific anonymous codes. They are included only to preserve row linkage across deposited files. No names, dates of birth, exact participant ages, laboratory accession numbers, or raw reports are included. Exact participant ages were omitted from public materials to reduce re-identification risk in this small cohort. Nonessential participant-level duplicate outputs were also removed where they were not required for auditability or reproduction.

## Pipeline summary

The workflow implements four steps.

1. **Parse**  
   Extract analyte name, numeric value, printed reference interval, and source-report flag for each report entry. Classify each interval as two-sided or one-sided at the participant-analyte level.

2. **Validate**  
   Confirm extraction completeness, recompute out-of-range status from parsed values and bounds, and compare recomputed flags against source-report flags.

3. **Transform**  
   Apply `z-approx = (x - μ) / σ` for two-sided intervals, where `μ = (L + U) / 2` and `σ = (U - L) / 3.92`. Apply `f = x / U` for one-sided upper-limit intervals.

4. **Construct**  
   Assemble transformed values into participant-by-feature matrices and standardize features before principal component analysis.

## Requirements

The public reproduction script was run with Python 3.10 and the following packages:

- numpy
- pandas
- scikit-learn
- matplotlib

Install with:

```bash
pip install -r requirements.txt
```

## Reproducing deposited outputs

To regenerate the deposited feature matrices, PCA outputs, summary tables, a neutral PCA visualization, and supplementary rank-based sensitivity outputs from the deposited audit table, run:

```bash
python oat_pipeline.py
```

Output files will be written to an `output/` directory.

The repository retains one authoritative copy of each participant-level derived data object at the repository root. Redundant participant-level duplicates were removed from `output/` to reduce unnecessary linkage surfaces in this small cohort while preserving full reproducibility from the deposited audit table.

The public reproduction script is designed to reproduce the deposited numerical results from the deposited audit table. It does not require access to raw clinical reports. The script writes a fuller local output set for reproducibility, whereas the distributed package avoids unnecessary duplication of participant-level files in output/.

## Expected reproduced results

The deposited audit table reproduces the following reported numerical summaries:

- 10 participants
- 75 analytes
- complete participant-by-feature matrix with no missing values
- 100% flag concordance for flagged rows
- primary PCA variance explained of 27.3% for PC1 and 19.0% for PC2
- ketone-excluded PCA variance explained of 27.5% for PC1 and 18.5% for PC2

## Synthetic example

`synthetic_example_input.csv` is a fully synthetic documentation file. It demonstrates the expected input schema without containing real participant data or proprietary report formatting. It is included for documentation only and was not used for the reported analyses.

## Ethics

The study was approved by The University of Mississippi Institutional Review Board under protocol 24-007. All deposited materials were prepared for public sharing in accordance with IRB and institutional guidance.

## Citation

Please cite the associated manuscript and the repository DOI if you use these materials.

## Contact

Gregory J. Snyder, PhD, CCC-SLP  
Department of Communication Sciences and Disorders  
The University of Mississippi  
gsnyder@olemiss.edu


## Rank-based sensitivity analysis

A supplementary rank-based PCA comparison is included to assess sensitivity to transformation choice. In this comparison, raw analyte values were ranked across participants, standardized, and submitted to PCA without reference-interval information. The primary component remained highly similar to the reference-aware solution, whereas the secondary component was not preserved, consistent with the greater sensitivity of secondary axes to scaling choices in a small sample.

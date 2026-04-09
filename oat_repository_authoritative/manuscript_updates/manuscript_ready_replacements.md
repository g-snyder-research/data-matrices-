# Manuscript-ready replacements from authoritative source data

This file contains manuscript-ready replacement text and authoritative table values regenerated from the deposited audit layer and aligned to manuscript v15.

## Summary of the reconciliation outcome

- The authoritative source data support the repository-side audit table and feature matrix.
- The PCA section remains supported.
- The current manuscript threshold-count and analyte-summary tables should be replaced.
- The key quantitative change is that the lenient heuristic screen averages **12.7** features per participant rather than **15.8**, for an information-recovery ratio of **3.5x** rather than 4.0x.
- Exact participant ages have been removed from public manuscript-facing repository materials to reduce re-identification risk in this small cohort.

## Replacement abstract

Abstract replacement

Background: Heterogeneous neurodevelopmental and neurobehavioral conditions are still characterized primarily through behavior, self-report, and clinician judgment, even when substantial evidence points to underlying biological heterogeneity. Routine clinical urinary organic acid testing (OAT) reports could help support more scalable biological phenotyping, but their semi-structured format and binary interpretation limit usefulness for quantitative neuroscience research.

New method: A reproducible, reference-aware feature-engineering pipeline was developed to extract analyte values and interval metadata from routine clinical reports and convert them into biochemical features for multivariate analysis. The pipeline addresses four technical problems, which include parsing semi-structured report tables, classifying reference-interval type as two-sided or one-sided, applying interval-appropriate transformations, and constructing auditable participant-by-feature matrices.

Results: Validation confirmed complete analyte recovery across reports, accurate interval classification, and full agreement between source flags and recomputed status. The workflow was demonstrated in ten adults with persistent developmental stuttering, a heterogeneous neurodevelopmental sensorimotor condition whose mismatch between neurobiological complexity and behavioral-only assessment illustrates the need for improved biological phenotyping. Relative to binary flagging, the lenient heuristic screen identified a mean of 12.7 analyte-level deviations per participant versus 3.6 laboratory out-of-range flags, whereas the stringent heuristic screen also averaged 3.6 deviations per participant. Sensitivity analysis excluding two diet-sensitive ketone-body analytes yielded a similar low-dimensional summary.

Comparison with existing methods: No prior study has formalized conversion of semi-structured clinical laboratory reports into reference-interval-aware features for neuroscience research.

Conclusions: The contribution is methodological, offering a transparent, auditable approach for harmonizing semi-structured clinical chemistry outputs with neuroscience workflows and supporting the broader goal of improved biological phenotyping across heterogeneous neurodevelopmental and neurobehavioral cohorts.

## Replacement Results text

### Section 3.2

3.2. Information recovery. Conventional flags versus continuous scoring

Table 1 summarizes per-participant counts of flagged analytes under three criteria. At the workflow-output level, this comparison provides the clearest test of whether reference-aware scoring recovers information that routine flagging discards. Laboratory out-of-range flags were infrequent (mean 3.6 per participant), whereas the lenient heuristic screen (|z-approx| ≥ 1 or f ≥ 0.75) identified a mean of 12.7 features per participant, approximately 3.5 times as many. The stringent heuristic screen (|z-approx| ≥ 2 or f ≥ 1.0), which approximates conventional flagging logic, identified a mean of 3.6 features per participant, equal to the laboratory-flag mean in this dataset. Interval-aware continuous scoring recovers substantially more graded variation than categorical flagging, even when the screening thresholds themselves are treated only as descriptive reporting devices.

### Section 3.3

3.3. Two-sided analyte deviations

Table 2 summarizes the two-sided analytes with the most consistent lenient-threshold deviations across applicable participants. In the context of the present paper, these analyte-level summaries function primarily as biological face-validity checks on the engineered feature space. They show that the workflow preserves recognizable cross-participant signal patterns rather than producing numerically coherent but biochemically uninterpretable outputs. For example, aconitic acid showed a negative deviation in all ten participants for whom it was represented as a two-sided analyte (mean z-approx = -1.55), yet only 10.0% were flagged by the laboratory. Ascorbic acid showed negative deviation in 90.0% of participants and was out of range in 90.0%. These observations are reported as supportive evidence that the workflow retains interpretable analyte structure. Because some analytes were represented as two-sided intervals in only a subset of participants, percentages in Table 2 are calculated relative to the number of participants with a two-sided interval for that analyte.

### Section 3.4

3.4. One-sided upper-limit analytes

Table 3 summarizes one-sided upper-limit analytes ranked by mean fraction-of-upper-limit (f). These results are methodologically important because they show that analytes without meaningful low-end abnormalities can still be retained in the same continuous workflow rather than discarded or forced into a symmetric transformation. The resulting summaries remain biologically interpretable, which again supports face validity of the feature-construction step. Arabinose had the highest mean f (1.18), with 90.0% of participants at or above f ≥ 0.75 and 60.0% above the upper reference limit. 3-Hydroxybutyric showed the highest maximum f among the top-ranked analytes (3.11), driven by a single participant with a profile consistent with increased ketone-body production under fasting or dietary conditions. Because some analytes were represented as one-sided intervals in only a subset of participants, percentages in Table 3 are calculated relative to the number of participants with a one-sided interval for that analyte.

## Replacement table values

### Table 1. Per-participant counts of flagged analytes under laboratory out-of-range flags and reference-aware subclinical thresholds.

| Participant   | Sex   |   Out-of-range flags |   Subclinical lenient |   Subclinical stringent |
|:--------------|:------|---------------------:|----------------------:|------------------------:|
| R01           | F     |                    3 |                    15 |                       3 |
| R02           | F     |                    3 |                    15 |                       3 |
| R03           | M     |                    3 |                    13 |                       3 |
| R04           | F     |                    4 |                    13 |                       4 |
| R05           | M     |                    7 |                    18 |                       7 |
| R06           | M     |                    2 |                    12 |                       2 |
| R07           | M     |                    6 |                     9 |                       6 |
| R08           | M     |                    3 |                     8 |                       3 |
| R09           | M     |                    2 |                    11 |                       2 |
| R10           | M     |                    3 |                    13 |                       3 |

Note. Participant labels (R01-R10) are repository-specific anonymous codes used in the deposited data files. Out-of-range corresponds to laboratory abnormal flags. The lenient and stringent thresholds are heuristic descriptive screens used to compare information recovery, not clinical cut points. They apply |z-approx| ≥ 1 or f ≥ 0.75 (lenient) and |z-approx| ≥ 2 or f ≥ 1.0 (stringent). Exact participant ages were not reported in order to reduce re-identification risk in this small cohort.

### Table 2. Two-sided reference-interval analytes with the most consistent subclinical deviations across applicable participants (top 10 by % |z| ≥ 1).

| Analyte            |   Mean z-approx |   Mean abs(z) |   % abs(z) ≥ 1 |   % abs(z) ≥ 2 |   % Out-of-range |
|:-------------------|----------------:|--------------:|---------------:|---------------:|-----------------:|
| Aconitic           |           -1.55 |          1.55 |          100   |             10 |               10 |
| Ascorbic           |           -1.88 |          1.96 |           90   |             90 |               90 |
| Citramalic         |           -0.96 |          1.1  |           71.4 |              0 |                0 |
| 4-Hydroxyhippuric  |           -1.37 |          1.37 |           66.7 |              0 |                0 |
| 2-Hydroxybutyric   |            1.14 |          1.18 |           66.7 |              0 |                0 |
| Malic              |           -1.01 |          1.01 |           66.7 |              0 |                0 |
| Orotic             |            0.93 |          0.93 |           66.7 |              0 |                0 |
| Adipic             |           -0.68 |          0.87 |           66.7 |              0 |                0 |
| 3-Methylglutaconic |           -0.66 |          0.94 |           57.1 |              0 |                0 |
| Lactic             |           -0.9  |          0.9  |           57.1 |              0 |                0 |

Note. z-approx values are derived from reported reference intervals. Negative values indicate low relative to the reference midpoint. Percentages are calculated relative to the number of participants for whom the analyte was represented with a two-sided interval.

### Table 3. One-sided upper-limit analytes ranked by fraction-of-upper-limit (top 10 by mean f).

| Analyte           |   Mean f (x/U) |   Max f (x/U) |   % f ≥ 0.75 |   % f ≥ 1.0 |   % Out-of-range |
|:------------------|---------------:|--------------:|-------------:|------------:|-----------------:|
| Arabinose         |           1.18 |          2    |         90   |        60   |             60   |
| 3-Hydroxybutyric  |           0.72 |          3.11 |         20   |        10   |             10   |
| Suberic           |           0.66 |          0.89 |         28.6 |         0   |              0   |
| 2-Hydroxybutyric  |           0.62 |          1.33 |         28.6 |        14.3 |             14.3 |
| 2-Hydroxyhippuric |           0.59 |          3.72 |         10   |        10   |             10   |
| 3-Hydroxyglutaric |           0.57 |          0.89 |         20   |         0   |              0   |
| Hippuric          |           0.54 |          1.24 |         30   |        10   |             10   |
| Lactic            |           0.54 |          0.88 |         33.3 |         0   |              0   |
| Citric            |           0.51 |          0.59 |          0   |         0   |              0   |
| 3-Oxoglutaric     |           0.45 |          2.55 |         10   |        10   |             10   |

Note. f denotes the ratio x/U, where U is the reported upper reference limit. Percentages are calculated relative to the number of participants for whom the analyte was represented with a one-sided interval.

## One additional downstream consistency edit outside the requested sections

The Discussion currently describes the lenient screen as recovering approximately four times as many analyte-level deviations as laboratory flags. That sentence should be updated to approximately **3.5 times** as many if the manuscript retains the same threshold definitions.

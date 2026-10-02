# RQ2 four-rater aggregate results

Each of the 69 Cases contributes one four-rater mean per method and dimension.

## Method means

| Method | Local Coherence | Transition Quality | Contingent Responsiveness |
| --- | ---: | ---: | ---: |
| Hashimoto | 2.326 | 1.819 | 2.138 |
| LLMREI-long | 3.351 | 2.953 | 3.065 |
| SparkMe | 2.638 | 2.924 | 2.478 |
| ElicitMind | 3.928 | 3.500 | 3.888 |

## Paired mean differences [95% CI]

All contrasts are ElicitMind minus baseline, paired within Case.

| Baseline | Local Coherence | Transition Quality | Contingent Responsiveness |
| --- | ---: | ---: | ---: |
| Hashimoto | 1.601 [1.435, 1.772] | 1.681 [1.529, 1.841] | 1.750 [1.583, 1.920] |
| LLMREI-long | 0.576 [0.457, 0.696] | 0.547 [0.428, 0.670] | 0.822 [0.710, 0.931] |
| SparkMe | 1.290 [1.167, 1.420] | 0.576 [0.438, 0.717] | 1.409 [1.290, 1.533] |

Percentile bootstrap: 10,000 draws; random seed 31017.
Each draw samples complete Cases with replacement, preserving all methods and dimensions.
The four raters have equal fixed weights; rater scores and interval endpoints are not resampled separately.
Intervals are pointwise 95% intervals, without a multiple-comparison adjustment. Exact paired sign-test p values and Holm correction are produced separately by make_tables.py.

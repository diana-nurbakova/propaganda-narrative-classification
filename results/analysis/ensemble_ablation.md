# Ensemble Size Ablation Report

Generated: 2026-02-11 23:36:43

**Model**: deepseek | **Language**: EN | **Aggregation**: intersection | **Ensemble sizes**: 1, 3, 5, 7

## Temperature = 0.0

Total successful runs across all ensemble sizes: **6**

### Narrative-level Metrics

| Ensemble | Agents | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|----------|--------|------|----------|----------|------------|---------------------|
| 1 agent | 1 | 1 | 0.266 +/- 0.000 | 0.346 +/- 0.000 | 0.361 +/- 0.000 | 0.361 +/- 0.000 |
| 3 agents | 3 | 5 | 0.282 +/- 0.026 | 0.350 +/- 0.008 | 0.349 +/- 0.007 | 0.349 +/- 0.007 |

### Subnarrative-level Metrics

| Ensemble | Agents | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|----------|--------|------|----------|----------|------------|---------------------|
| 1 agent | 1 | 1 | 0.115 +/- 0.000 | 0.129 +/- 0.000 | 0.127 +/- 0.000 | 0.127 +/- 0.000 |
| 3 agents | 3 | 5 | 0.102 +/- 0.006 | 0.112 +/- 0.004 | 0.105 +/- 0.005 | 0.105 +/- 0.005 |

### Bootstrap 95% Confidence Intervals

| Ensemble | Agents | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|----------|--------|--------------------------|-----------------------------|
| 1 agent | 1 | 0.361 +/- 0.000 [0.361, 0.361] | 0.127 +/- 0.000 [0.127, 0.127] |
| 3 agents | 3 | 0.349 +/- 0.007 [0.343, 0.355] | 0.105 +/- 0.005 [0.101, 0.108] |

### Trend Summary

- **Narrative F1-samples**: best at **1 agents** (0.361), range 0.349 -- 0.361
- **Subnarrative F1-samples**: best at **1 agents** (0.127), range 0.105 -- 0.127
- Narrative F1 is **monotonically decreasing** with ensemble size (intersection becomes stricter).
- Subnarrative F1 is **monotonically decreasing** with ensemble size.

### Pairwise Significance Tests (Narrative)

Metric: **Narrative F1-samples**

| A | B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|---|---|--------|--------|------|-----------|--------|-------------|------------|------|

### Pairwise Significance Tests (Subnarrative)

Metric: **Subnarrative F1-samples**

| A | B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|---|---|--------|--------|------|-----------|--------|-------------|------------|------|

## Temperature = 0.7

Total successful runs across all ensemble sizes: **5**

### Narrative-level Metrics

| Ensemble | Agents | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|----------|--------|------|----------|----------|------------|---------------------|
| 3 agents | 3 | 5 | 0.290 +/- 0.023 | 0.360 +/- 0.013 | 0.363 +/- 0.020 | 0.363 +/- 0.020 |

### Subnarrative-level Metrics

| Ensemble | Agents | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|----------|--------|------|----------|----------|------------|---------------------|
| 3 agents | 3 | 5 | 0.099 +/- 0.006 | 0.115 +/- 0.008 | 0.109 +/- 0.012 | 0.109 +/- 0.012 |

### Bootstrap 95% Confidence Intervals

| Ensemble | Agents | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|----------|--------|--------------------------|-----------------------------|
| 3 agents | 3 | 0.363 +/- 0.020 [0.348, 0.377] | 0.109 +/- 0.012 [0.100, 0.118] |

### Pairwise Significance Tests (Narrative)

Metric: **Narrative F1-samples**

| A | B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|---|---|--------|--------|------|-----------|--------|-------------|------------|------|

### Pairwise Significance Tests (Subnarrative)

Metric: **Subnarrative F1-samples**

| A | B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|---|---|--------|--------|------|-----------|--------|-------------|------------|------|


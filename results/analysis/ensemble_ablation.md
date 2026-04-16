# Ensemble Size Ablation Report

Generated: 2026-02-12 15:05:09

**Model**: deepseek | **Language**: EN | **Aggregation strategies**: Intersection, Majority, Union | **Ensemble sizes**: 1, 3, 5, 7

## Temperature = 0.0

Total successful runs: **35**

### Intersection Aggregation

#### Narrative-level Metrics (Intersection)

| Ensemble | Agents | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|----------|--------|------|----------|----------|------------|---------------------|
| 1 agent | 1 | 5 | 0.277 +/- 0.016 | 0.345 +/- 0.004 | 0.349 +/- 0.008 | 0.349 +/- 0.008 |
| 3 agents | 3 | 5 | 0.282 +/- 0.026 | 0.350 +/- 0.008 | 0.349 +/- 0.007 | 0.349 +/- 0.007 |
| 5 agents | 5 | 5 | 0.309 +/- 0.030 | 0.380 +/- 0.014 | 0.380 +/- 0.023 | 0.380 +/- 0.023 |
| 7 agents | 7 | 5 | 0.265 +/- 0.022 | 0.354 +/- 0.008 | 0.348 +/- 0.010 | 0.348 +/- 0.010 |

#### Subnarrative-level Metrics (Intersection)

| Ensemble | Agents | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|----------|--------|------|----------|----------|------------|---------------------|
| 1 agent | 1 | 5 | 0.108 +/- 0.008 | 0.118 +/- 0.007 | 0.111 +/- 0.010 | 0.111 +/- 0.010 |
| 3 agents | 3 | 5 | 0.102 +/- 0.006 | 0.112 +/- 0.004 | 0.105 +/- 0.005 | 0.105 +/- 0.005 |
| 5 agents | 5 | 5 | 0.109 +/- 0.012 | 0.126 +/- 0.008 | 0.116 +/- 0.010 | 0.116 +/- 0.010 |
| 7 agents | 7 | 5 | 0.094 +/- 0.008 | 0.114 +/- 0.004 | 0.103 +/- 0.006 | 0.103 +/- 0.006 |

#### Bootstrap 95% Confidence Intervals (Intersection)

| Ensemble | Agents | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|----------|--------|--------------------------|-----------------------------|
| 1 agent | 1 | 0.349 +/- 0.008 [0.343, 0.356] | 0.111 +/- 0.010 [0.105, 0.120] |
| 3 agents | 3 | 0.349 +/- 0.007 [0.343, 0.355] | 0.105 +/- 0.005 [0.101, 0.108] |
| 5 agents | 5 | 0.380 +/- 0.023 [0.364, 0.401] | 0.116 +/- 0.010 [0.109, 0.123] |
| 7 agents | 7 | 0.348 +/- 0.010 [0.341, 0.357] | 0.103 +/- 0.006 [0.099, 0.107] |

### Trend Summary

- **Narrative F1-samples**: best at **5 agents** (0.380), range 0.348 -- 0.380
- **Subnarrative F1-samples**: best at **5 agents** (0.116), range 0.103 -- 0.116
- Narrative F1 is **non-monotonic** across ensemble sizes (Intersection aggregation).
- Subnarrative F1 is **non-monotonic** across ensemble sizes.

#### Pairwise Significance Tests - Narrative (Intersection)

Metric: **Narrative F1-samples**

| A | B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|---|---|--------|--------|------|-----------|--------|-------------|------------|------|
| 1 agent | 3 agents | 0.349 | 0.349 | +0.000 | +0.00 | negligible | 0.8125 | 0.9935 |  |
| 1 agent | 5 agents | 0.349 | 0.380 | -0.031 | -1.28 | large | 0.0625 | 0.0460 |  |
| 1 agent | 7 agents | 0.349 | 0.348 | +0.001 | +0.07 | negligible | 1.0000 | 0.8763 |  |
| 3 agents | 5 agents | 0.349 | 0.380 | -0.031 | -1.06 | large | 0.1250 | 0.0771 |  |
| 3 agents | 7 agents | 0.349 | 0.348 | +0.001 | +0.09 | negligible | 1.0000 | 0.8522 |  |
| 5 agents | 7 agents | 0.380 | 0.348 | +0.032 | +1.17 | large | 0.0625 | 0.0588 |  |

#### Pairwise Significance Tests - Subnarrative (Intersection)

Metric: **Subnarrative F1-samples**

| A | B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|---|---|--------|--------|------|-----------|--------|-------------|------------|------|
| 1 agent | 3 agents | 0.111 | 0.105 | +0.006 | +0.48 | small | 0.4375 | 0.3428 |  |
| 1 agent | 5 agents | 0.111 | 0.116 | -0.005 | -0.43 | small | 0.4375 | 0.3910 |  |
| 1 agent | 7 agents | 0.111 | 0.103 | +0.008 | +0.89 | large | 0.1875 | 0.1189 |  |
| 3 agents | 5 agents | 0.105 | 0.116 | -0.011 | -0.76 | medium | 0.1875 | 0.1659 |  |
| 3 agents | 7 agents | 0.105 | 0.103 | +0.001 | +0.16 | negligible | 0.8125 | 0.7351 |  |
| 5 agents | 7 agents | 0.116 | 0.103 | +0.012 | +1.10 | large | 0.0625 | 0.0704 |  |

### Majority Aggregation

#### Narrative-level Metrics (Majority)

| Ensemble | Agents | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|----------|--------|------|----------|----------|------------|---------------------|
| 1 agent | 1 | 5 | 0.277 +/- 0.016 | 0.345 +/- 0.004 | 0.349 +/- 0.008 | 0.349 +/- 0.008 |
| 3 agents | 3 | 5 | 0.283 +/- 0.010 | 0.343 +/- 0.010 | 0.343 +/- 0.009 | 0.343 +/- 0.009 |
| 5 agents | 5 | 5 | 0.290 +/- 0.004 | 0.347 +/- 0.006 | 0.348 +/- 0.008 | 0.348 +/- 0.008 |

#### Subnarrative-level Metrics (Majority)

| Ensemble | Agents | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|----------|--------|------|----------|----------|------------|---------------------|
| 1 agent | 1 | 5 | 0.108 +/- 0.008 | 0.118 +/- 0.007 | 0.111 +/- 0.010 | 0.111 +/- 0.010 |
| 3 agents | 3 | 5 | 0.099 +/- 0.004 | 0.111 +/- 0.004 | 0.105 +/- 0.005 | 0.105 +/- 0.005 |
| 5 agents | 5 | 5 | 0.103 +/- 0.003 | 0.115 +/- 0.005 | 0.108 +/- 0.005 | 0.108 +/- 0.005 |

#### Bootstrap 95% Confidence Intervals (Majority)

| Ensemble | Agents | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|----------|--------|--------------------------|-----------------------------|
| 1 agent | 1 | 0.349 +/- 0.008 [0.343, 0.356] | 0.111 +/- 0.010 [0.105, 0.120] |
| 3 agents | 3 | 0.343 +/- 0.009 [0.336, 0.351] | 0.105 +/- 0.005 [0.101, 0.109] |
| 5 agents | 5 | 0.348 +/- 0.008 [0.342, 0.354] | 0.108 +/- 0.005 [0.104, 0.112] |

### Trend Summary

- **Narrative F1-samples**: best at **1 agents** (0.349), range 0.343 -- 0.349
- **Subnarrative F1-samples**: best at **1 agents** (0.111), range 0.105 -- 0.111
- Narrative F1 is **non-monotonic** across ensemble sizes (Majority aggregation).
- Subnarrative F1 is **non-monotonic** across ensemble sizes.

#### Pairwise Significance Tests - Narrative (Majority)

Metric: **Narrative F1-samples**

| A | B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|---|---|--------|--------|------|-----------|--------|-------------|------------|------|
| 1 agent | 3 agents | 0.349 | 0.343 | +0.006 | +0.48 | small | 0.3125 | 0.3438 |  |
| 1 agent | 5 agents | 0.349 | 0.348 | +0.001 | +0.08 | negligible | 1.0000 | 0.8706 |  |
| 3 agents | 5 agents | 0.343 | 0.348 | -0.005 | -0.41 | small | 0.6250 | 0.4069 |  |

#### Pairwise Significance Tests - Subnarrative (Majority)

Metric: **Subnarrative F1-samples**

| A | B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|---|---|--------|--------|------|-----------|--------|-------------|------------|------|
| 1 agent | 3 agents | 0.111 | 0.105 | +0.006 | +0.54 | medium | 0.4375 | 0.2949 |  |
| 1 agent | 5 agents | 0.111 | 0.108 | +0.003 | +0.26 | small | 0.6250 | 0.5962 |  |
| 3 agents | 5 agents | 0.105 | 0.108 | -0.004 | -0.49 | small | 0.3125 | 0.3345 |  |

### Union Aggregation

#### Narrative-level Metrics (Union)

| Ensemble | Agents | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|----------|--------|------|----------|----------|------------|---------------------|
| 1 agent | 1 | 5 | 0.277 +/- 0.016 | 0.345 +/- 0.004 | 0.349 +/- 0.008 | 0.349 +/- 0.008 |
| 3 agents | 3 | 5 | 0.264 +/- 0.012 | 0.316 +/- 0.007 | 0.320 +/- 0.010 | 0.320 +/- 0.010 |

#### Subnarrative-level Metrics (Union)

| Ensemble | Agents | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|----------|--------|------|----------|----------|------------|---------------------|
| 1 agent | 1 | 5 | 0.108 +/- 0.008 | 0.118 +/- 0.007 | 0.111 +/- 0.010 | 0.111 +/- 0.010 |
| 3 agents | 3 | 5 | 0.100 +/- 0.008 | 0.107 +/- 0.004 | 0.100 +/- 0.006 | 0.100 +/- 0.006 |

#### Bootstrap 95% Confidence Intervals (Union)

| Ensemble | Agents | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|----------|--------|--------------------------|-----------------------------|
| 1 agent | 1 | 0.349 +/- 0.008 [0.343, 0.356] | 0.111 +/- 0.010 [0.105, 0.120] |
| 3 agents | 3 | 0.320 +/- 0.010 [0.312, 0.326] | 0.100 +/- 0.006 [0.096, 0.105] |

### Trend Summary

- **Narrative F1-samples**: best at **1 agents** (0.349), range 0.320 -- 0.349
- **Subnarrative F1-samples**: best at **1 agents** (0.111), range 0.100 -- 0.111
- Narrative F1 is **monotonically decreasing** with ensemble size (Union becomes stricter).
- Subnarrative F1 is **monotonically decreasing** with ensemble size.

#### Pairwise Significance Tests - Narrative (Union)

Metric: **Narrative F1-samples**

| A | B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|---|---|--------|--------|------|-----------|--------|-------------|------------|------|
| 1 agent | 3 agents | 0.349 | 0.320 | +0.029 | +2.16 | large | 0.0625 | 0.0085 |  |

#### Pairwise Significance Tests - Subnarrative (Union)

Metric: **Subnarrative F1-samples**

| A | B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|---|---|--------|--------|------|-----------|--------|-------------|------------|------|
| 1 agent | 3 agents | 0.111 | 0.100 | +0.011 | +0.81 | large | 0.1250 | 0.1447 |  |

### Cross-Aggregation Comparison

Compares aggregation strategies side-by-side for each ensemble size.
The 1-agent row is shared across all strategies (aggregation is a no-op with a single agent).

**Narrative F1-samples**

| Agents | Intersection | Majority | Union | Best |
|--------|--------------|----------|-------|------|
| 1 | 0.349 | 0.349 | 0.349 | Intersection |
| 3 | 0.349 | 0.343 | 0.320 | Intersection |
| 5 | 0.380 | 0.348 | -- | Intersection |
| 7 | 0.348 | -- | -- | Intersection |

**Subnarrative F1-samples**

| Agents | Intersection | Majority | Union | Best |
|--------|--------------|----------|-------|------|
| 1 | 0.111 | 0.111 | 0.111 | Intersection |
| 3 | 0.105 | 0.105 | 0.100 | Intersection |
| 5 | 0.116 | 0.108 | -- | Intersection |
| 7 | 0.103 | -- | -- | Intersection |

**Narrative F1-macro**

| Agents | Intersection | Majority | Union | Best |
|--------|--------------|----------|-------|------|
| 1 | 0.277 | 0.277 | 0.277 | Intersection |
| 3 | 0.282 | 0.283 | 0.264 | Majority |
| 5 | 0.309 | 0.290 | -- | Intersection |
| 7 | 0.265 | -- | -- | Intersection |

**Subnarrative F1-macro**

| Agents | Intersection | Majority | Union | Best |
|--------|--------------|----------|-------|------|
| 1 | 0.108 | 0.108 | 0.108 | Intersection |
| 3 | 0.102 | 0.099 | 0.100 | Intersection |
| 5 | 0.109 | 0.103 | -- | Intersection |
| 7 | 0.094 | -- | -- | Intersection |

## Temperature = 0.7

Total successful runs: **22**

### Intersection Aggregation

#### Narrative-level Metrics (Intersection)

| Ensemble | Agents | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|----------|--------|------|----------|----------|------------|---------------------|
| 1 agent | 1 | 3 | 0.289 +/- 0.008 | 0.344 +/- 0.007 | 0.347 +/- 0.004 | 0.347 +/- 0.004 |
| 3 agents | 3 | 5 | 0.290 +/- 0.023 | 0.360 +/- 0.013 | 0.363 +/- 0.020 | 0.363 +/- 0.020 |

#### Subnarrative-level Metrics (Intersection)

| Ensemble | Agents | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|----------|--------|------|----------|----------|------------|---------------------|
| 1 agent | 1 | 3 | 0.109 +/- 0.004 | 0.119 +/- 0.003 | 0.112 +/- 0.003 | 0.112 +/- 0.003 |
| 3 agents | 3 | 5 | 0.099 +/- 0.006 | 0.115 +/- 0.008 | 0.109 +/- 0.012 | 0.109 +/- 0.012 |

#### Bootstrap 95% Confidence Intervals (Intersection)

| Ensemble | Agents | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|----------|--------|--------------------------|-----------------------------|
| 1 agent | 1 | 0.347 +/- 0.004 [0.344, 0.352] | 0.112 +/- 0.003 [0.109, 0.115] |
| 3 agents | 3 | 0.363 +/- 0.020 [0.348, 0.377] | 0.109 +/- 0.012 [0.100, 0.118] |

### Trend Summary

- **Narrative F1-samples**: best at **3 agents** (0.363), range 0.347 -- 0.363
- **Subnarrative F1-samples**: best at **1 agents** (0.112), range 0.109 -- 0.112
- Narrative F1 is **monotonically increasing** with ensemble size (Intersection aggregation).
- Subnarrative F1 is **monotonically decreasing** with ensemble size.

#### Pairwise Significance Tests - Narrative (Intersection)

Metric: **Narrative F1-samples**

| A | B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|---|---|--------|--------|------|-----------|--------|-------------|------------|------|
| 1 agent | 3 agents | 0.347 | 0.363 | -0.016 | -1.15 | large | 0.2500 | 0.1840 |  |

#### Pairwise Significance Tests - Subnarrative (Intersection)

Metric: **Subnarrative F1-samples**

| A | B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|---|---|--------|--------|------|-----------|--------|-------------|------------|------|
| 1 agent | 3 agents | 0.112 | 0.109 | +0.003 | +0.50 | medium | 0.5000 | 0.4766 |  |

### Majority Aggregation

#### Narrative-level Metrics (Majority)

| Ensemble | Agents | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|----------|--------|------|----------|----------|------------|---------------------|
| 1 agent | 1 | 3 | 0.289 +/- 0.008 | 0.344 +/- 0.007 | 0.347 +/- 0.004 | 0.347 +/- 0.004 |
| 3 agents | 3 | 5 | 0.287 +/- 0.021 | 0.349 +/- 0.013 | 0.351 +/- 0.015 | 0.351 +/- 0.015 |
| 5 agents | 5 | 4 | 0.295 +/- 0.016 | 0.340 +/- 0.012 | 0.340 +/- 0.022 | 0.340 +/- 0.022 |

#### Subnarrative-level Metrics (Majority)

| Ensemble | Agents | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|----------|--------|------|----------|----------|------------|---------------------|
| 1 agent | 1 | 3 | 0.109 +/- 0.004 | 0.119 +/- 0.003 | 0.112 +/- 0.003 | 0.112 +/- 0.003 |
| 3 agents | 3 | 5 | 0.100 +/- 0.010 | 0.115 +/- 0.007 | 0.108 +/- 0.008 | 0.108 +/- 0.008 |
| 5 agents | 5 | 4 | 0.105 +/- 0.003 | 0.115 +/- 0.003 | 0.105 +/- 0.008 | 0.105 +/- 0.008 |

#### Bootstrap 95% Confidence Intervals (Majority)

| Ensemble | Agents | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|----------|--------|--------------------------|-----------------------------|
| 1 agent | 1 | 0.347 +/- 0.004 [0.344, 0.352] | 0.112 +/- 0.003 [0.109, 0.115] |
| 3 agents | 3 | 0.351 +/- 0.015 [0.339, 0.363] | 0.108 +/- 0.008 [0.102, 0.114] |
| 5 agents | 5 | 0.340 +/- 0.022 [0.323, 0.358] | 0.105 +/- 0.008 [0.099, 0.111] |

### Trend Summary

- **Narrative F1-samples**: best at **3 agents** (0.351), range 0.340 -- 0.351
- **Subnarrative F1-samples**: best at **1 agents** (0.112), range 0.105 -- 0.112
- Narrative F1 is **non-monotonic** across ensemble sizes (Majority aggregation).
- Subnarrative F1 is **monotonically decreasing** with ensemble size.

#### Pairwise Significance Tests - Narrative (Majority)

Metric: **Narrative F1-samples**

| A | B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|---|---|--------|--------|------|-----------|--------|-------------|------------|------|
| 1 agent | 3 agents | 0.347 | 0.351 | -0.004 | -0.74 | medium | 0.5000 | 0.3284 |  |
| 1 agent | 5 agents | 0.347 | 0.340 | +0.008 | +1.11 | large | 0.5000 | 0.1941 |  |
| 3 agents | 5 agents | 0.351 | 0.340 | +0.012 | +0.24 | small | 0.8750 | 0.6656 |  |

#### Pairwise Significance Tests - Subnarrative (Majority)

Metric: **Subnarrative F1-samples**

| A | B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|---|---|--------|--------|------|-----------|--------|-------------|------------|------|
| 1 agent | 3 agents | 0.112 | 0.108 | +0.004 | +0.41 | small | 0.7500 | 0.5473 |  |
| 1 agent | 5 agents | 0.112 | 0.105 | +0.007 | +1.17 | large | 0.2500 | 0.1802 |  |
| 3 agents | 5 agents | 0.108 | 0.105 | +0.003 | +0.11 | negligible | 0.8750 | 0.8392 |  |

### Union Aggregation

#### Narrative-level Metrics (Union)

| Ensemble | Agents | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|----------|--------|------|----------|----------|------------|---------------------|
| 1 agent | 1 | 3 | 0.289 +/- 0.008 | 0.344 +/- 0.007 | 0.347 +/- 0.004 | 0.347 +/- 0.004 |
| 3 agents | 3 | 5 | 0.259 +/- 0.015 | 0.306 +/- 0.010 | 0.307 +/- 0.013 | 0.307 +/- 0.013 |

#### Subnarrative-level Metrics (Union)

| Ensemble | Agents | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|----------|--------|------|----------|----------|------------|---------------------|
| 1 agent | 1 | 3 | 0.109 +/- 0.004 | 0.119 +/- 0.003 | 0.112 +/- 0.003 | 0.112 +/- 0.003 |
| 3 agents | 3 | 5 | 0.095 +/- 0.005 | 0.104 +/- 0.004 | 0.097 +/- 0.005 | 0.097 +/- 0.005 |

#### Bootstrap 95% Confidence Intervals (Union)

| Ensemble | Agents | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|----------|--------|--------------------------|-----------------------------|
| 1 agent | 1 | 0.347 +/- 0.004 [0.344, 0.352] | 0.112 +/- 0.003 [0.109, 0.115] |
| 3 agents | 3 | 0.307 +/- 0.013 [0.297, 0.317] | 0.097 +/- 0.005 [0.093, 0.100] |

### Trend Summary

- **Narrative F1-samples**: best at **1 agents** (0.347), range 0.307 -- 0.347
- **Subnarrative F1-samples**: best at **1 agents** (0.112), range 0.097 -- 0.112
- Narrative F1 is **monotonically decreasing** with ensemble size (Union becomes stricter).
- Subnarrative F1 is **monotonically decreasing** with ensemble size.

#### Pairwise Significance Tests - Narrative (Union)

Metric: **Narrative F1-samples**

| A | B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|---|---|--------|--------|------|-----------|--------|-------------|------------|------|
| 1 agent | 3 agents | 0.347 | 0.307 | +0.040 | +2.00 | large | 0.2500 | 0.0743 |  |

#### Pairwise Significance Tests - Subnarrative (Union)

Metric: **Subnarrative F1-samples**

| A | B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|---|---|--------|--------|------|-----------|--------|-------------|------------|------|
| 1 agent | 3 agents | 0.112 | 0.097 | +0.016 | +1.67 | large | 0.2500 | 0.1018 |  |

### Cross-Aggregation Comparison

Compares aggregation strategies side-by-side for each ensemble size.
The 1-agent row is shared across all strategies (aggregation is a no-op with a single agent).

**Narrative F1-samples**

| Agents | Intersection | Majority | Union | Best |
|--------|--------------|----------|-------|------|
| 1 | 0.347 | 0.347 | 0.347 | Intersection |
| 3 | 0.363 | 0.351 | 0.307 | Intersection |
| 5 | -- | 0.340 | -- | Majority |

**Subnarrative F1-samples**

| Agents | Intersection | Majority | Union | Best |
|--------|--------------|----------|-------|------|
| 1 | 0.112 | 0.112 | 0.112 | Intersection |
| 3 | 0.109 | 0.108 | 0.097 | Intersection |
| 5 | -- | 0.105 | -- | Majority |

**Narrative F1-macro**

| Agents | Intersection | Majority | Union | Best |
|--------|--------------|----------|-------|------|
| 1 | 0.289 | 0.289 | 0.289 | Intersection |
| 3 | 0.290 | 0.287 | 0.259 | Intersection |
| 5 | -- | 0.295 | -- | Majority |

**Subnarrative F1-macro**

| Agents | Intersection | Majority | Union | Best |
|--------|--------------|----------|-------|------|
| 1 | 0.109 | 0.109 | 0.109 | Intersection |
| 3 | 0.099 | 0.100 | 0.095 | Majority |
| 5 | -- | 0.105 | -- | Majority |


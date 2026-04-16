# Experiment Results Report

Generated: 2026-02-12 10:07:27

**Experiments evaluated:** 5/5 (total runs: 25)

## Methodology

### Run Strategy

All experiments are evaluated using the **all-runs averaging** strategy: each experiment consists of N independent runs (typically 5) with different random seeds. We evaluate every successful run independently against the gold-standard ground truth, then report the **mean** and **standard deviation** of each metric across all successful runs. This approach captures the variance inherent in LLM-based classification and avoids cherry-picking.

### Evaluation Metrics

We report the following metrics at both **narrative** (coarse) and **subnarrative** (fine) levels:

| Metric | Description |
|--------|-------------|
| F1-macro | Unweighted mean of per-label F1 scores (treats rare labels equally) |
| F1-micro | Globally aggregated TP/FP/FN, then F1 (favors frequent labels) |
| F1-samples | Per-sample F1 averaged across documents (sklearn implementation) |
| F1-samples (manual) | Set-based per-sample F1: (2|Y&Y_hat|)/(|Y|+|Y_hat|) averaged (SemEval official) |

### Statistical Testing

For each pair of experiments sharing the same language and temperature, we perform:

- **Paired t-test**: Parametric test on per-run scores (assumes normality)
- **Wilcoxon signed-rank test**: Non-parametric alternative (no normality assumption)
- **Cohen's d**: Standardized effect size (paired: d = mean_diff / std_diff). Interpretation: |d| < 0.2 negligible, 0.2-0.5 small, 0.5-0.8 medium, >= 0.8 large
- **Bootstrap 95% confidence intervals**: 10,000 resamples of per-run means

Significance levels: * p < 0.05, ** p < 0.01, *** p < 0.001

### Experiment Configurations

| Experiment | Model | Method | Agents | Aggregation | Strategy | Temp | Max Tokens | Validation |
|------------|-------|--------|--------|-------------|----------|------|------------|------------|
| mdeberta_baseline_bg_t00 | mDeBERTa v3 (fine-tuned) | mDeBERTa (fine-tuned) | 1N/1S | single | multi_head | 0.0 | 512 | No |
| mdeberta_baseline_en_t00 | mDeBERTa v3 (fine-tuned) | mDeBERTa (fine-tuned) | 1N/1S | single | multi_head | 0.0 | 512 | No |
| mdeberta_baseline_hi_t00 | mDeBERTa v3 (fine-tuned) | mDeBERTa (fine-tuned) | 1N/1S | single | multi_head | 0.0 | 512 | No |
| mdeberta_baseline_pt_t00 | mDeBERTa v3 (fine-tuned) | mDeBERTa (fine-tuned) | 1N/1S | single | multi_head | 0.0 | 512 | No |
| mdeberta_baseline_ru_t00 | mDeBERTa v3 (fine-tuned) | mDeBERTa (fine-tuned) | 1N/1S | single | multi_head | 0.0 | 512 | No |

## Results

### Language: BG

Ground truth: `data/dev-documents_4_December\BG\subtask-3-dominant-narratives.txt`

#### Narrative-level (Coarse) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_baseline_bg_t00 | 5 | 0.149 +/- 0.049 | 0.330 +/- 0.058 | 0.386 +/- 0.063 | 0.386 +/- 0.063 |

#### Subnarrative-level (Fine) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_baseline_bg_t00 | 5 | 0.074 +/- 0.038 | 0.171 +/- 0.045 | 0.222 +/- 0.037 | 0.222 +/- 0.037 |

#### Bootstrap 95% Confidence Intervals

| Experiment | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|------------|--------------------------|-----------------------------|
| mdeberta_baseline_bg_t00 | 0.386 +/- 0.063 [0.338, 0.435] | 0.222 +/- 0.037 [0.192, 0.250] |

### Language: EN

Ground truth: `data/dev-documents_4_December\EN\subtask-3-dominant-narratives.txt`

#### Narrative-level (Coarse) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_baseline_en_t00 | 5 | 0.125 +/- 0.019 | 0.205 +/- 0.023 | 0.207 +/- 0.043 | 0.207 +/- 0.043 |

#### Subnarrative-level (Fine) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_baseline_en_t00 | 5 | 0.051 +/- 0.021 | 0.074 +/- 0.013 | 0.064 +/- 0.015 | 0.064 +/- 0.015 |

#### Bootstrap 95% Confidence Intervals

| Experiment | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|------------|--------------------------|-----------------------------|
| mdeberta_baseline_en_t00 | 0.207 +/- 0.043 [0.176, 0.242] | 0.064 +/- 0.015 [0.056, 0.078] |

### Language: HI

Ground truth: `data/dev-documents_4_December\HI\subtask-3-dominant-narratives.txt`

#### Narrative-level (Coarse) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_baseline_hi_t00 | 5 | 0.161 +/- 0.019 | 0.319 +/- 0.035 | 0.309 +/- 0.035 | 0.309 +/- 0.035 |

#### Subnarrative-level (Fine) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_baseline_hi_t00 | 5 | 0.071 +/- 0.025 | 0.183 +/- 0.040 | 0.182 +/- 0.030 | 0.189 +/- 0.040 |

#### Bootstrap 95% Confidence Intervals

| Experiment | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|------------|--------------------------|-----------------------------|
| mdeberta_baseline_hi_t00 | 0.309 +/- 0.035 [0.282, 0.334] | 0.182 +/- 0.030 [0.159, 0.203] |

### Language: PT

Ground truth: `data/dev-documents_4_December\PT\subtask-3-dominant-narratives.txt`

#### Narrative-level (Coarse) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_baseline_pt_t00 | 5 | 0.166 +/- 0.011 | 0.428 +/- 0.019 | 0.462 +/- 0.006 | 0.462 +/- 0.006 |

#### Subnarrative-level (Fine) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_baseline_pt_t00 | 5 | 0.059 +/- 0.014 | 0.151 +/- 0.023 | 0.141 +/- 0.023 | 0.141 +/- 0.023 |

#### Bootstrap 95% Confidence Intervals

| Experiment | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|------------|--------------------------|-----------------------------|
| mdeberta_baseline_pt_t00 | 0.462 +/- 0.006 [0.457, 0.466] | 0.141 +/- 0.023 [0.123, 0.160] |

### Language: RU

Ground truth: `data/dev-documents_4_December\RU\subtask-3-dominant-narratives.txt`

#### Narrative-level (Coarse) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_baseline_ru_t00 | 5 | 0.113 +/- 0.028 | 0.241 +/- 0.051 | 0.233 +/- 0.054 | 0.233 +/- 0.054 |

#### Subnarrative-level (Fine) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_baseline_ru_t00 | 5 | 0.060 +/- 0.017 | 0.127 +/- 0.035 | 0.125 +/- 0.028 | 0.125 +/- 0.028 |

#### Bootstrap 95% Confidence Intervals

| Experiment | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|------------|--------------------------|-----------------------------|
| mdeberta_baseline_ru_t00 | 0.233 +/- 0.054 [0.195, 0.275] | 0.125 +/- 0.028 [0.101, 0.143] |

## Cross-Architecture Comparison

Comparison of three architectures — **Baseline** (single-agent, no validation), **Actor-Critic** (single-agent + validation nodes), and **Agora** (3-agent ensemble) — matched by model, language, and temperature. For Agora, we report the best-performing aggregation strategy (intersection/majority/union). mDeBERTa fine-tuned baseline included for reference.

p-values from paired t-test on per-run F1-samples scores. Significance: \* p<0.05, \*\* p<0.01, \*\*\* p<0.001

### Temperature = 0.0

#### Narrative-level F1-samples

| Lang | Model | Baseline | Actor-Critic | p (AC vs BL) | Best Agora (agg) | p (Agora vs BL) |
|------|-------|----------|-------------|--------------|-----------------|----------------|
| BG | mDeBERTa v3 (fine-tuned) | 0.386 +/- 0.063 | — | — | — | — |
| EN | mDeBERTa v3 (fine-tuned) | 0.207 +/- 0.043 | — | — | — | — |
| HI | mDeBERTa v3 (fine-tuned) | 0.309 +/- 0.035 | — | — | — | — |
| PT | mDeBERTa v3 (fine-tuned) | 0.462 +/- 0.006 | — | — | — | — |
| RU | mDeBERTa v3 (fine-tuned) | 0.233 +/- 0.054 | — | — | — | — |

#### Subnarrative-level F1-samples

| Lang | Model | Baseline | Actor-Critic | p (AC vs BL) | Best Agora (agg) | p (Agora vs BL) |
|------|-------|----------|-------------|--------------|-----------------|----------------|
| BG | mDeBERTa v3 (fine-tuned) | 0.222 +/- 0.037 | — | — | — | — |
| EN | mDeBERTa v3 (fine-tuned) | 0.064 +/- 0.015 | — | — | — | — |
| HI | mDeBERTa v3 (fine-tuned) | 0.182 +/- 0.030 | — | — | — | — |
| PT | mDeBERTa v3 (fine-tuned) | 0.141 +/- 0.023 | — | — | — | — |
| RU | mDeBERTa v3 (fine-tuned) | 0.125 +/- 0.028 | — | — | — | — |

### Actor-Critic vs Baseline: Aggregate Summary

| Level | AC Wins | AC Losses | Ties |
|-------|---------|-----------|------|
| Narrative F1-samples | 0 | 0 | 0 |
| Subnarrative F1-samples | 0 | 0 | 0 |

**Average improvement by model (Actor-Critic minus Baseline):**

| Model | Avg Narr Diff | Avg Sub Diff | N |
|-------|--------------|-------------|---|

**Average improvement by language (Actor-Critic minus Baseline):**

| Language | Avg Narr Diff | Avg Sub Diff | N |
|----------|--------------|-------------|---|

## Cross-Method Comparison

Comparing different multi-agent strategies using the same backbone model. Sorted by subnarrative F1-samples (descending).

## Cross-Model Comparison

Comparing the same method across different backbone models. Sorted by subnarrative F1-samples (descending).

## Pairwise Significance Tests

Paired tests comparing methods within the same language and temperature. We use the Wilcoxon signed-rank test (non-parametric) as the primary test, with the paired t-test for reference. Tests are run on per-run F1-samples scores at the subnarrative level (the primary evaluation metric).


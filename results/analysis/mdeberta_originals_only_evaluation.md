# Experiment Results Report

Generated: 2026-02-12 15:56:58

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
| mdeberta_originals_only_bg_t00 | mDeBERTa v3 (fine-tuned) | Unknown | 1N/1S | single | multi_head | 0.0 | 512 | No |
| mdeberta_originals_only_en_t00 | mDeBERTa v3 (fine-tuned) | Unknown | 1N/1S | single | multi_head | 0.0 | 512 | No |
| mdeberta_originals_only_hi_t00 | mDeBERTa v3 (fine-tuned) | Unknown | 1N/1S | single | multi_head | 0.0 | 512 | No |
| mdeberta_originals_only_pt_t00 | mDeBERTa v3 (fine-tuned) | Unknown | 1N/1S | single | multi_head | 0.0 | 512 | No |
| mdeberta_originals_only_ru_t00 | mDeBERTa v3 (fine-tuned) | Unknown | 1N/1S | single | multi_head | 0.0 | 512 | No |

## Results

### Language: BG

Ground truth: `data/dev-documents_4_December\BG\subtask-3-dominant-narratives.txt`

#### Narrative-level (Coarse) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_originals_only_bg_t00 | 5 | 0.174 +/- 0.023 | 0.384 +/- 0.028 | 0.448 +/- 0.032 | 0.448 +/- 0.032 |

#### Subnarrative-level (Fine) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_originals_only_bg_t00 | 5 | 0.086 +/- 0.025 | 0.181 +/- 0.027 | 0.231 +/- 0.029 | 0.231 +/- 0.029 |

#### Bootstrap 95% Confidence Intervals

| Experiment | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|------------|--------------------------|-----------------------------|
| mdeberta_originals_only_bg_t00 | 0.448 +/- 0.032 [0.425, 0.474] | 0.231 +/- 0.029 [0.206, 0.250] |

### Language: EN

Ground truth: `data/dev-documents_4_December\EN\subtask-3-dominant-narratives.txt`

#### Narrative-level (Coarse) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_originals_only_en_t00 | 5 | 0.146 +/- 0.032 | 0.260 +/- 0.036 | 0.264 +/- 0.041 | 0.264 +/- 0.041 |

#### Subnarrative-level (Fine) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_originals_only_en_t00 | 5 | 0.054 +/- 0.005 | 0.081 +/- 0.014 | 0.078 +/- 0.014 | 0.078 +/- 0.014 |

#### Bootstrap 95% Confidence Intervals

| Experiment | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|------------|--------------------------|-----------------------------|
| mdeberta_originals_only_en_t00 | 0.264 +/- 0.041 [0.232, 0.296] | 0.078 +/- 0.014 [0.067, 0.089] |

### Language: HI

Ground truth: `data/dev-documents_4_December\HI\subtask-3-dominant-narratives.txt`

#### Narrative-level (Coarse) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_originals_only_hi_t00 | 5 | 0.196 +/- 0.024 | 0.307 +/- 0.039 | 0.308 +/- 0.039 | 0.308 +/- 0.039 |

#### Subnarrative-level (Fine) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_originals_only_hi_t00 | 5 | 0.094 +/- 0.013 | 0.158 +/- 0.017 | 0.179 +/- 0.015 | 0.186 +/- 0.017 |

#### Bootstrap 95% Confidence Intervals

| Experiment | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|------------|--------------------------|-----------------------------|
| mdeberta_originals_only_hi_t00 | 0.308 +/- 0.039 [0.284, 0.343] | 0.179 +/- 0.015 [0.168, 0.191] |

### Language: PT

Ground truth: `data/dev-documents_4_December\PT\subtask-3-dominant-narratives.txt`

#### Narrative-level (Coarse) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_originals_only_pt_t00 | 5 | 0.204 +/- 0.029 | 0.435 +/- 0.018 | 0.491 +/- 0.035 | 0.491 +/- 0.035 |

#### Subnarrative-level (Fine) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_originals_only_pt_t00 | 5 | 0.072 +/- 0.008 | 0.174 +/- 0.016 | 0.193 +/- 0.015 | 0.193 +/- 0.015 |

#### Bootstrap 95% Confidence Intervals

| Experiment | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|------------|--------------------------|-----------------------------|
| mdeberta_originals_only_pt_t00 | 0.491 +/- 0.035 [0.465, 0.519] | 0.193 +/- 0.015 [0.181, 0.204] |

### Language: RU

Ground truth: `data/dev-documents_4_December\RU\subtask-3-dominant-narratives.txt`

#### Narrative-level (Coarse) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_originals_only_ru_t00 | 5 | 0.120 +/- 0.024 | 0.298 +/- 0.034 | 0.305 +/- 0.042 | 0.305 +/- 0.042 |

#### Subnarrative-level (Fine) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_originals_only_ru_t00 | 5 | 0.055 +/- 0.015 | 0.115 +/- 0.036 | 0.115 +/- 0.046 | 0.115 +/- 0.046 |

#### Bootstrap 95% Confidence Intervals

| Experiment | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|------------|--------------------------|-----------------------------|
| mdeberta_originals_only_ru_t00 | 0.305 +/- 0.042 [0.276, 0.340] | 0.115 +/- 0.046 [0.080, 0.149] |

## Cross-Architecture Comparison

Comparison of three architectures — **Baseline** (single-agent, no validation), **Actor-Critic** (single-agent + validation nodes), and **Agora** (3-agent ensemble) — matched by model, language, and temperature. For Agora, we report the best-performing aggregation strategy (intersection/majority/union). mDeBERTa fine-tuned baseline included for reference.

p-values from paired t-test on per-run F1-samples scores. Significance: \* p<0.05, \*\* p<0.01, \*\*\* p<0.001

### Temperature = 0.0

#### Narrative-level F1-samples

| Lang | Model | Baseline | Actor-Critic | p (AC vs BL) | Best Agora (agg) | p (Agora vs BL) |
|------|-------|----------|-------------|--------------|-----------------|----------------|
| BG | mDeBERTa v3 (fine-tuned) | — | — | — | — | — |
| EN | mDeBERTa v3 (fine-tuned) | — | — | — | — | — |
| HI | mDeBERTa v3 (fine-tuned) | — | — | — | — | — |
| PT | mDeBERTa v3 (fine-tuned) | — | — | — | — | — |
| RU | mDeBERTa v3 (fine-tuned) | — | — | — | — | — |

#### Subnarrative-level F1-samples

| Lang | Model | Baseline | Actor-Critic | p (AC vs BL) | Best Agora (agg) | p (Agora vs BL) |
|------|-------|----------|-------------|--------------|-----------------|----------------|
| BG | mDeBERTa v3 (fine-tuned) | — | — | — | — | — |
| EN | mDeBERTa v3 (fine-tuned) | — | — | — | — | — |
| HI | mDeBERTa v3 (fine-tuned) | — | — | — | — | — |
| PT | mDeBERTa v3 (fine-tuned) | — | — | — | — | — |
| RU | mDeBERTa v3 (fine-tuned) | — | — | — | — | — |

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


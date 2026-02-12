# Experiment Results Report

Generated: 2026-02-11 20:28:47

**Experiments evaluated:** 98/98 (total runs: 435)

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
| actor_critic_deepseek_bg_t00 | DeepSeek V3 | Actor-Critic | 1N/1S | union | level_first | 0.0 | 8192 | Yes |
| actor_critic_deepseek_bg_t07 | DeepSeek V3 | Actor-Critic | 1N/1S | union | level_first | 0.7 | 8192 | Yes |
| actor_critic_deepseek_en_t00 | DeepSeek V3 | Actor-Critic | 1N/1S | union | level_first | 0.0 | 8192 | Yes |
| actor_critic_deepseek_en_t00_evidence | DeepSeek V3 | Actor-Critic | 1N/1S | union | level_first | 0.0 | 8192 | Yes |
| actor_critic_deepseek_en_t07 | DeepSeek V3 | Actor-Critic | 1N/1S | union | level_first | 0.7 | 8192 | Yes |
| actor_critic_deepseek_hi_t00 | DeepSeek V3 | Actor-Critic | 1N/1S | union | level_first | 0.0 | 8192 | Yes |
| actor_critic_deepseek_pt_t00 | DeepSeek V3 | Actor-Critic | 1N/1S | union | level_first | 0.0 | 8192 | Yes |
| actor_critic_deepseek_ru_t00 | DeepSeek V3 | Actor-Critic | 1N/1S | union | level_first | 0.0 | 8192 | Yes |
| actor_critic_deepseek_ru_t07 | DeepSeek V3 | Actor-Critic | 1N/1S | union | level_first | 0.7 | 8192 | Yes |
| actor_critic_gemini_en_t00 | Gemini 2.5 Flash | Actor-Critic | 1N/1S | union | level_first | 0.0 | 8192 | Yes |
| actor_critic_gemini_en_t00 | Gemini 2.5 Flash | Actor-Critic | 1N/1S | union | level_first | 0.0 | 8192 | Yes |
| actor_critic_gemini_en_t07 | Gemini 2.5 Flash | Actor-Critic | 1N/1S | union | level_first | 0.7 | 8192 | Yes |
| actor_critic_gemini_en_t07 | Gemini 2.5 Flash | Actor-Critic | 1N/1S | union | level_first | 0.7 | 8192 | Yes |
| actor_critic_gpt5nano_en_t00 | GPT-5 Nano | Actor-Critic | 1N/1S | union | level_first | 0.0 | 16384 | Yes |
| actor_critic_gpt5nano_en_t07 | GPT-5 Nano | Actor-Critic | 1N/1S | union | level_first | 0.7 | 16384 | Yes |
| actor_critic_mistral_bg_t00 | Mistral Large | Actor-Critic | 1N/1S | union | level_first | 0.0 | 8192 | Yes |
| actor_critic_mistral_en_t00 | Mistral Large | Actor-Critic | 1N/1S | union | level_first | 0.0 | 8192 | Yes |
| actor_critic_mistral_en_t00_evidence | Mistral Large | Actor-Critic | 1N/1S | union | level_first | 0.0 | 8192 | Yes |
| actor_critic_mistral_en_t07 | Mistral Large | Actor-Critic | 1N/1S | union | level_first | 0.7 | 8192 | Yes |
| actor_critic_mistral_hi_t00 | Mistral Large | Actor-Critic | 1N/1S | union | level_first | 0.0 | 8192 | Yes |
| actor_critic_mistral_pt_t00 | Mistral Large | Actor-Critic | 1N/1S | union | level_first | 0.0 | 8192 | Yes |
| actor_critic_mistral_ru_t00 | Mistral Large | Actor-Critic | 1N/1S | union | level_first | 0.0 | 8192 | Yes |
| actor_critic_together_llama33_70b_en_t00 | Llama 3.3 70B | Actor-Critic | 1N/1S | union | level_first | 0.0 | 8192 | Yes |
| actor_critic_together_llama33_70b_en_t07 | Llama 3.3 70B | Actor-Critic | 1N/1S | union | level_first | 0.7 | 8192 | Yes |
| agora_deepseek_bg_t00 | DeepSeek V3 | Agora (intersection) | 3N/1S | intersection | level_first | 0.0 | 8192 | No |
| agora_deepseek_bg_t07 | DeepSeek V3 | Agora (intersection) | 3N/1S | intersection | level_first | 0.7 | 8192 | No |
| agora_deepseek_en_t00 | DeepSeek V3 | Agora (intersection) | 3N/1S | intersection | level_first | 0.0 | 8192 | No |
| agora_deepseek_en_t07 | DeepSeek V3 | Agora (intersection) | 3N/1S | intersection | level_first | 0.7 | 8192 | No |
| agora_deepseek_hi_t00 | DeepSeek V3 | Agora (intersection) | 3N/1S | intersection | level_first | 0.0 | 8192 | No |
| agora_deepseek_pt_t00 | DeepSeek V3 | Agora (intersection) | 3N/1S | intersection | level_first | 0.0 | 8192 | No |
| agora_deepseek_ru_t00 | DeepSeek V3 | Agora (intersection) | 3N/1S | intersection | level_first | 0.0 | 8192 | No |
| agora_deepseek_ru_t07 | DeepSeek V3 | Agora (intersection) | 3N/1S | intersection | level_first | 0.7 | 8192 | No |
| agora_gemini_en_t00 | Gemini 2.5 Flash | Agora (intersection) | 3N/1S | intersection | level_first | 0.0 | 8192 | No |
| agora_gemini_en_t07 | Gemini 2.5 Flash | Agora (intersection) | 3N/1S | intersection | level_first | 0.7 | 8192 | No |
| agora_majority_deepseek_pt_t00 | DeepSeek V3 | Agora (majority) | 3N/1S | majority | level_first | 0.0 | 8192 | No |
| agora_majority_gpt5nano_bg_t00 | GPT-5 Nano | Agora (majority) | 3N/1S | majority | level_first | 0.0 | 16384 | No |
| agora_majority_gpt5nano_ru_t00 | GPT-5 Nano | Agora (majority) | 3N/1S | majority | level_first | 0.0 | 16384 | No |
| agora_majority_gpt5nano_en_t07 | GPT-5 Nano | Agora (majority) | 3N/1S | majority | level_first | 0.7 | 16384 | No |
| agora_majority_gpt5nano_hi_t00 | GPT-5 Nano | Agora (majority) | 3N/1S | majority | level_first | 0.0 | 16384 | No |
| agora_majority_gpt5nano_pt_t00 | GPT-5 Nano | Agora (majority) | 3N/1S | majority | level_first | 0.0 | 16384 | No |
| agora_majority_gpt5nano_ru_t00 | GPT-5 Nano | Agora (majority) | 3N/1S | majority | level_first | 0.0 | 16384 | No |
| agora_majority_mistral_bg_t00 | Mistral Large | Agora (majority) | 3N/1S | majority | level_first | 0.0 | 8192 | No |
| agora_majority_mistral_en_t00 | Mistral Large | Agora (majority) | 3N/1S | majority | level_first | 0.0 | 8192 | No |
| agora_majority_mistral_en_t00_evidence | Mistral Large | Agora (majority) | 3N/1S | majority | level_first | 0.0 | 8192 | No |
| agora_majority_mistral_en_t07 | Mistral Large | Agora (majority) | 3N/1S | majority | level_first | 0.7 | 8192 | No |
| agora_majority_mistral_hi_t00 | Mistral Large | Agora (majority) | 3N/1S | majority | level_first | 0.0 | 8192 | No |
| agora_majority_mistral_pt_t00 | Mistral Large | Agora (majority) | 3N/1S | majority | level_first | 0.0 | 8192 | No |
| agora_majority_mistral_ru_t00 | Mistral Large | Agora (majority) | 3N/1S | majority | level_first | 0.0 | 8192 | No |
| agora_majority_together_llama33_70b_bg_t00 | Llama 3.3 70B | Agora (majority) | 3N/1S | majority | level_first | 0.0 | 8192 | No |
| agora_majority_together_llama33_70b_en_t00 | Llama 3.3 70B | Agora (majority) | 3N/1S | majority | level_first | 0.0 | 8192 | No |
| agora_majority_together_llama33_70b_en_t07 | Llama 3.3 70B | Agora (majority) | 3N/1S | majority | level_first | 0.7 | 8192 | No |
| agora_majority_together_llama33_70b_hi_t00 | Llama 3.3 70B | Agora (majority) | 3N/1S | majority | level_first | 0.0 | 8192 | No |
| agora_majority_together_llama33_70b_pt_t00 | Llama 3.3 70B | Agora (majority) | 3N/1S | majority | level_first | 0.0 | 8192 | No |
| agora_majority_together_llama33_70b_ru_t00 | Llama 3.3 70B | Agora (majority) | 3N/1S | majority | level_first | 0.0 | 8192 | No |
| agora_mistral_bg_t00 | Mistral Large | Agora (intersection) | 3N/1S | intersection | level_first | 0.0 | 8192 | No |
| agora_mistral_en_t00 | Mistral Large | Agora (intersection) | 3N/1S | intersection | level_first | 0.0 | 8192 | No |
| agora_mistral_en_t00_evidence | Mistral Large | Agora (intersection) | 3N/1S | intersection | level_first | 0.0 | 8192 | No |
| agora_mistral_en_t07 | Mistral Large | Agora (intersection) | 3N/1S | intersection | level_first | 0.7 | 8192 | No |
| agora_mistral_hi_t00 | Mistral Large | Agora (intersection) | 3N/1S | intersection | level_first | 0.0 | 8192 | No |
| agora_mistral_pt_t00 | Mistral Large | Agora (intersection) | 3N/1S | intersection | level_first | 0.0 | 8192 | No |
| agora_mistral_ru_t00 | Mistral Large | Agora (intersection) | 3N/1S | intersection | level_first | 0.0 | 8192 | No |
| agora_together_llama33_70b_en_t00 | Llama 3.3 70B | Agora (intersection) | 3N/1S | intersection | level_first | 0.0 | 8192 | No |
| agora_together_llama33_70b_en_t07 | Llama 3.3 70B | Agora (intersection) | 3N/1S | intersection | level_first | 0.7 | 8192 | No |
| agora_union_deepseek_pt_t00 | DeepSeek V3 | Agora (union) | 3N/1S | union | level_first | 0.0 | 8192 | No |
| agora_union_gpt5nano_en_t00 | GPT-5 Nano | Agora (union) | 3N/1S | union | level_first | 0.0 | 16384 | No |
| agora_union_gpt5nano_en_t07 | GPT-5 Nano | Agora (union) | 3N/1S | union | level_first | 0.7 | 16384 | No |
| agora_union_mistral_en_t00 | Mistral Large | Agora (union) | 3N/1S | union | level_first | 0.0 | 8192 | No |
| agora_union_mistral_en_t07 | Mistral Large | Agora (union) | 3N/1S | union | level_first | 0.7 | 8192 | No |
| agora_union_together_llama33_70b_en_t00 | Llama 3.3 70B | Agora (union) | 3N/1S | union | level_first | 0.0 | 8192 | No |
| agora_union_together_llama33_70b_en_t07 | Llama 3.3 70B | Agora (union) | 3N/1S | union | level_first | 0.7 | 8192 | No |
| baseline_deepseek_bg_t00 | DeepSeek V3 | Baseline | 1N/1S | union | level_first | 0.0 | 8192 | No |
| baseline_deepseek_bg_t07 | DeepSeek V3 | Baseline | 1N/1S | union | level_first | 0.7 | 8192 | No |
| baseline_deepseek_en_t00 | DeepSeek V3 | Baseline | 1N/1S | union | level_first | 0.0 | 8192 | No |
| baseline_deepseek_en_t00_evidence | DeepSeek V3 | Baseline | 1N/1S | union | level_first | 0.0 | 8192 | No |
| baseline_deepseek_en_t07 | DeepSeek V3 | Baseline | 1N/1S | union | level_first | 0.7 | 8192 | No |
| baseline_deepseek_hi_t00 | DeepSeek V3 | Baseline | 1N/1S | union | level_first | 0.0 | 8192 | No |
| baseline_deepseek_pt_t00 | DeepSeek V3 | Baseline | 1N/1S | union | level_first | 0.0 | 8192 | No |
| baseline_deepseek_pt_t07 | DeepSeek V3 | Baseline | 1N/1S | union | level_first | 0.7 | 8192 | No |
| baseline_deepseek_ru_t00 | DeepSeek V3 | Baseline | 1N/1S | union | level_first | 0.0 | 8192 | No |
| baseline_deepseek_ru_t07 | DeepSeek V3 | Baseline | 1N/1S | union | level_first | 0.7 | 8192 | No |
| baseline_gemini_en_t00 | Gemini 2.5 Flash | Baseline | 1N/1S | union | level_first | 0.0 | 8192 | No |
| baseline_gemini_en_t07 | Gemini 2.5 Flash | Baseline | 1N/1S | union | level_first | 0.7 | 8192 | No |
| baseline_gpt5nano_en_t00 | GPT-5 Nano | Baseline | 1N/1S | union | level_first | 0.0 | 16384 | No |
| baseline_gpt5nano_en_t07 | GPT-5 Nano | Baseline | 1N/1S | union | level_first | 0.7 | 16384 | No |
| baseline_mistral_bg_t00 | Mistral Large | Baseline | 1N/1S | union | level_first | 0.0 | 8192 | No |
| baseline_mistral_en_t00 | Mistral Large | Baseline | 1N/1S | union | level_first | 0.0 | 8192 | No |
| baseline_mistral_en_t00_evidence | Mistral Large | Baseline | 1N/1S | union | level_first | 0.0 | 8192 | No |
| baseline_mistral_en_t07 | Mistral Large | Baseline | 1N/1S | union | level_first | 0.7 | 8192 | No |
| baseline_mistral_hi_t00 | Mistral Large | Baseline | 1N/1S | union | level_first | 0.0 | 8192 | No |
| baseline_mistral_pt_t00 | Mistral Large | Baseline | 1N/1S | union | level_first | 0.0 | 8192 | No |
| baseline_mistral_ru_t00 | Mistral Large | Baseline | 1N/1S | union | level_first | 0.0 | 8192 | No |
| baseline_together_llama33_70b_en_t00 | Llama 3.3 70B | Baseline | 1N/1S | union | level_first | 0.0 | 8192 | No |
| baseline_together_llama33_70b_en_t07 | Llama 3.3 70B | Baseline | 1N/1S | union | level_first | 0.7 | 8192 | No |
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
| agora_deepseek_bg_t00 | 5 | 0.380 +/- 0.020 | 0.549 +/- 0.012 | 0.606 +/- 0.013 | 0.606 +/- 0.013 |
| agora_deepseek_bg_t07 | 5 | 0.368 +/- 0.013 | 0.545 +/- 0.014 | 0.599 +/- 0.011 | 0.599 +/- 0.011 |
| baseline_deepseek_bg_t00 | 5 | 0.334 +/- 0.016 | 0.513 +/- 0.010 | 0.575 +/- 0.010 | 0.575 +/- 0.010 |
| baseline_deepseek_bg_t07 | 5 | 0.322 +/- 0.016 | 0.503 +/- 0.012 | 0.565 +/- 0.008 | 0.565 +/- 0.008 |
| agora_majority_gpt5nano_bg_t00 | 5 | 0.275 +/- 0.040 | 0.441 +/- 0.018 | 0.509 +/- 0.026 | 0.509 +/- 0.026 |
| actor_critic_deepseek_bg_t07 | 5 | 0.275 +/- 0.037 | 0.463 +/- 0.021 | 0.490 +/- 0.049 | 0.490 +/- 0.049 |
| agora_mistral_bg_t00 | 5 | 0.301 +/- 0.009 | 0.427 +/- 0.009 | 0.483 +/- 0.012 | 0.483 +/- 0.012 |
| agora_majority_mistral_bg_t00 | 5 | 0.280 +/- 0.007 | 0.401 +/- 0.001 | 0.477 +/- 0.006 | 0.477 +/- 0.006 |
| actor_critic_mistral_bg_t00 | 5 | 0.285 +/- 0.013 | 0.409 +/- 0.014 | 0.474 +/- 0.020 | 0.474 +/- 0.020 |
| baseline_mistral_bg_t00 | 5 | 0.242 +/- 0.011 | 0.398 +/- 0.009 | 0.469 +/- 0.019 | 0.469 +/- 0.019 |
| actor_critic_deepseek_bg_t00 | 5 | 0.265 +/- 0.047 | 0.435 +/- 0.039 | 0.453 +/- 0.039 | 0.453 +/- 0.039 |
| mdeberta_baseline_bg_t00 | 1 | 0.154 +/- 0.000 | 0.364 +/- 0.000 | 0.413 +/- 0.000 | 0.413 +/- 0.000 |
| agora_majority_together_llama33_70b_bg_t00 | 5 | 0.209 +/- 0.016 | 0.321 +/- 0.013 | 0.315 +/- 0.019 | 0.315 +/- 0.019 |

#### Subnarrative-level (Fine) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| agora_majority_gpt5nano_bg_t00 | 5 | 0.119 +/- 0.013 | 0.208 +/- 0.017 | 0.244 +/- 0.017 | 0.244 +/- 0.017 |
| agora_deepseek_bg_t00 | 5 | 0.121 +/- 0.009 | 0.208 +/- 0.004 | 0.237 +/- 0.004 | 0.237 +/- 0.004 |
| agora_deepseek_bg_t07 | 5 | 0.121 +/- 0.005 | 0.207 +/- 0.008 | 0.230 +/- 0.006 | 0.230 +/- 0.006 |
| mdeberta_baseline_bg_t00 | 1 | 0.062 +/- 0.000 | 0.161 +/- 0.000 | 0.220 +/- 0.000 | 0.220 +/- 0.000 |
| baseline_deepseek_bg_t00 | 5 | 0.106 +/- 0.005 | 0.187 +/- 0.003 | 0.217 +/- 0.006 | 0.217 +/- 0.006 |
| baseline_deepseek_bg_t07 | 5 | 0.104 +/- 0.006 | 0.184 +/- 0.002 | 0.216 +/- 0.001 | 0.216 +/- 0.001 |
| actor_critic_deepseek_bg_t07 | 5 | 0.114 +/- 0.011 | 0.195 +/- 0.007 | 0.204 +/- 0.034 | 0.204 +/- 0.034 |
| actor_critic_deepseek_bg_t00 | 5 | 0.104 +/- 0.009 | 0.181 +/- 0.013 | 0.187 +/- 0.019 | 0.187 +/- 0.019 |
| agora_mistral_bg_t00 | 5 | 0.085 +/- 0.007 | 0.126 +/- 0.005 | 0.155 +/- 0.009 | 0.155 +/- 0.009 |
| agora_majority_mistral_bg_t00 | 5 | 0.079 +/- 0.002 | 0.115 +/- 0.001 | 0.147 +/- 0.003 | 0.147 +/- 0.003 |
| baseline_mistral_bg_t00 | 5 | 0.073 +/- 0.002 | 0.115 +/- 0.003 | 0.145 +/- 0.007 | 0.145 +/- 0.007 |
| actor_critic_mistral_bg_t00 | 5 | 0.080 +/- 0.004 | 0.118 +/- 0.005 | 0.143 +/- 0.012 | 0.143 +/- 0.012 |
| agora_majority_together_llama33_70b_bg_t00 | 5 | 0.069 +/- 0.001 | 0.119 +/- 0.002 | 0.114 +/- 0.007 | 0.114 +/- 0.007 |

#### Bootstrap 95% Confidence Intervals

| Experiment | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|------------|--------------------------|-----------------------------|
| agora_deepseek_bg_t00 | 0.606 +/- 0.013 [0.598, 0.617] | 0.237 +/- 0.004 [0.234, 0.240] |
| agora_deepseek_bg_t07 | 0.599 +/- 0.011 [0.591, 0.608] | 0.230 +/- 0.006 [0.225, 0.234] |
| baseline_deepseek_bg_t00 | 0.575 +/- 0.010 [0.568, 0.583] | 0.217 +/- 0.006 [0.212, 0.221] |
| baseline_deepseek_bg_t07 | 0.565 +/- 0.008 [0.559, 0.571] | 0.216 +/- 0.001 [0.215, 0.217] |
| agora_majority_gpt5nano_bg_t00 | 0.509 +/- 0.026 [0.487, 0.528] | 0.244 +/- 0.017 [0.230, 0.256] |
| actor_critic_deepseek_bg_t07 | 0.490 +/- 0.049 [0.453, 0.526] | 0.204 +/- 0.034 [0.185, 0.233] |
| agora_mistral_bg_t00 | 0.483 +/- 0.012 [0.473, 0.492] | 0.155 +/- 0.009 [0.150, 0.163] |
| agora_majority_mistral_bg_t00 | 0.477 +/- 0.006 [0.473, 0.482] | 0.147 +/- 0.003 [0.145, 0.149] |
| actor_critic_mistral_bg_t00 | 0.474 +/- 0.020 [0.459, 0.490] | 0.143 +/- 0.012 [0.134, 0.152] |
| baseline_mistral_bg_t00 | 0.469 +/- 0.019 [0.458, 0.487] | 0.145 +/- 0.007 [0.141, 0.152] |
| actor_critic_deepseek_bg_t00 | 0.453 +/- 0.039 [0.425, 0.486] | 0.187 +/- 0.019 [0.172, 0.203] |
| mdeberta_baseline_bg_t00 | 0.413 +/- 0.000 [0.413, 0.413] | 0.220 +/- 0.000 [0.220, 0.220] |
| agora_majority_together_llama33_70b_bg_t00 | 0.315 +/- 0.019 [0.301, 0.330] | 0.114 +/- 0.007 [0.109, 0.119] |

### Language: EN

Ground truth: `data/dev-documents_4_December\EN\subtask-3-dominant-narratives.txt`

#### Narrative-level (Coarse) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| agora_gemini_en_t07 | 5 | 0.257 +/- 0.037 | 0.352 +/- 0.022 | 0.393 +/- 0.037 | 0.393 +/- 0.037 |
| agora_gemini_en_t00 | 3 | 0.215 +/- 0.001 | 0.314 +/- 0.007 | 0.383 +/- 0.014 | 0.383 +/- 0.014 |
| baseline_gemini_en_t07 | 1 | 0.235 +/- 0.000 | 0.302 +/- 0.000 | 0.367 +/- 0.000 | 0.367 +/- 0.000 |
| agora_deepseek_en_t07 | 5 | 0.290 +/- 0.023 | 0.360 +/- 0.013 | 0.363 +/- 0.020 | 0.363 +/- 0.020 |
| baseline_deepseek_en_t00_evidence | 1 | 0.329 +/- 0.000 | 0.361 +/- 0.000 | 0.355 +/- 0.000 | 0.355 +/- 0.000 |
| actor_critic_deepseek_en_t00_evidence | 1 | 0.290 +/- 0.000 | 0.358 +/- 0.000 | 0.355 +/- 0.000 | 0.355 +/- 0.000 |
| baseline_gemini_en_t00 | 5 | 0.237 +/- 0.023 | 0.306 +/- 0.007 | 0.354 +/- 0.012 | 0.354 +/- 0.012 |
| agora_deepseek_en_t00 | 5 | 0.282 +/- 0.026 | 0.350 +/- 0.008 | 0.349 +/- 0.007 | 0.349 +/- 0.007 |
| actor_critic_deepseek_en_t00 | 5 | 0.283 +/- 0.032 | 0.350 +/- 0.018 | 0.347 +/- 0.020 | 0.347 +/- 0.020 |
| actor_critic_gemini_en_t07 | 4 | 0.262 +/- 0.046 | 0.323 +/- 0.029 | 0.347 +/- 0.038 | 0.347 +/- 0.038 |
| actor_critic_deepseek_en_t07 | 5 | 0.272 +/- 0.036 | 0.341 +/- 0.034 | 0.343 +/- 0.042 | 0.343 +/- 0.042 |
| baseline_deepseek_en_t00 | 5 | 0.288 +/- 0.009 | 0.340 +/- 0.008 | 0.342 +/- 0.013 | 0.342 +/- 0.013 |
| baseline_gpt5nano_en_t00 | 5 | 0.288 +/- 0.024 | 0.322 +/- 0.030 | 0.341 +/- 0.034 | 0.341 +/- 0.034 |
| agora_majority_gpt5nano_ru_t00 | 1 | 0.288 +/- 0.000 | 0.312 +/- 0.000 | 0.339 +/- 0.000 | 0.339 +/- 0.000 |
| agora_majority_gpt5nano_en_t07 | 5 | 0.289 +/- 0.007 | 0.318 +/- 0.015 | 0.337 +/- 0.019 | 0.337 +/- 0.019 |
| actor_critic_gemini_en_t00 | 5 | 0.243 +/- 0.023 | 0.309 +/- 0.005 | 0.334 +/- 0.018 | 0.334 +/- 0.018 |
| actor_critic_gpt5nano_en_t07 | 5 | 0.278 +/- 0.019 | 0.310 +/- 0.013 | 0.331 +/- 0.020 | 0.331 +/- 0.020 |
| baseline_deepseek_en_t07 | 5 | 0.275 +/- 0.018 | 0.332 +/- 0.009 | 0.329 +/- 0.012 | 0.329 +/- 0.012 |
| agora_mistral_en_t00 | 5 | 0.247 +/- 0.031 | 0.312 +/- 0.013 | 0.325 +/- 0.022 | 0.325 +/- 0.022 |
| actor_critic_together_llama33_70b_en_t00 | 5 | 0.239 +/- 0.019 | 0.303 +/- 0.011 | 0.319 +/- 0.010 | 0.319 +/- 0.010 |
| agora_together_llama33_70b_en_t00 | 5 | 0.229 +/- 0.026 | 0.301 +/- 0.007 | 0.318 +/- 0.015 | 0.318 +/- 0.015 |
| agora_mistral_en_t07 | 5 | 0.229 +/- 0.018 | 0.306 +/- 0.007 | 0.318 +/- 0.008 | 0.318 +/- 0.008 |
| agora_union_gpt5nano_en_t07 | 5 | 0.274 +/- 0.014 | 0.289 +/- 0.012 | 0.318 +/- 0.015 | 0.318 +/- 0.015 |
| agora_mistral_en_t00_evidence | 1 | 0.207 +/- 0.000 | 0.298 +/- 0.000 | 0.314 +/- 0.000 | 0.314 +/- 0.000 |
| actor_critic_gemini_en_t07 | 5 | 0.232 +/- 0.012 | 0.303 +/- 0.018 | 0.310 +/- 0.019 | 0.310 +/- 0.019 |
| agora_union_gpt5nano_en_t00 | 5 | 0.279 +/- 0.010 | 0.285 +/- 0.016 | 0.309 +/- 0.026 | 0.309 +/- 0.026 |
| baseline_gpt5nano_en_t07 | 5 | 0.264 +/- 0.013 | 0.301 +/- 0.014 | 0.308 +/- 0.021 | 0.308 +/- 0.021 |
| agora_majority_together_llama33_70b_en_t00 | 5 | 0.250 +/- 0.017 | 0.284 +/- 0.013 | 0.307 +/- 0.016 | 0.307 +/- 0.016 |
| actor_critic_together_llama33_70b_en_t07 | 5 | 0.230 +/- 0.020 | 0.300 +/- 0.013 | 0.307 +/- 0.024 | 0.307 +/- 0.024 |
| agora_majority_mistral_en_t00 | 5 | 0.245 +/- 0.027 | 0.292 +/- 0.009 | 0.303 +/- 0.021 | 0.303 +/- 0.021 |
| agora_majority_together_llama33_70b_en_t07 | 5 | 0.233 +/- 0.015 | 0.282 +/- 0.010 | 0.302 +/- 0.014 | 0.302 +/- 0.014 |
| actor_critic_gemini_en_t00 | 5 | 0.231 +/- 0.010 | 0.291 +/- 0.013 | 0.301 +/- 0.019 | 0.301 +/- 0.019 |
| baseline_together_llama33_70b_en_t07 | 5 | 0.237 +/- 0.015 | 0.285 +/- 0.006 | 0.300 +/- 0.009 | 0.300 +/- 0.009 |
| agora_together_llama33_70b_en_t07 | 5 | 0.226 +/- 0.018 | 0.300 +/- 0.021 | 0.300 +/- 0.021 | 0.300 +/- 0.021 |
| actor_critic_mistral_en_t00_evidence | 1 | 0.250 +/- 0.000 | 0.296 +/- 0.000 | 0.299 +/- 0.000 | 0.299 +/- 0.000 |
| baseline_mistral_en_t00 | 5 | 0.240 +/- 0.016 | 0.288 +/- 0.008 | 0.297 +/- 0.005 | 0.297 +/- 0.005 |
| agora_majority_mistral_en_t07 | 5 | 0.222 +/- 0.021 | 0.285 +/- 0.015 | 0.297 +/- 0.014 | 0.297 +/- 0.014 |
| actor_critic_gpt5nano_en_t00 | 5 | 0.240 +/- 0.031 | 0.286 +/- 0.016 | 0.294 +/- 0.018 | 0.294 +/- 0.018 |
| agora_majority_mistral_en_t00_evidence | 1 | 0.221 +/- 0.000 | 0.276 +/- 0.000 | 0.292 +/- 0.000 | 0.292 +/- 0.000 |
| baseline_mistral_en_t00_evidence | 1 | 0.239 +/- 0.000 | 0.271 +/- 0.000 | 0.289 +/- 0.000 | 0.289 +/- 0.000 |
| actor_critic_mistral_en_t00 | 5 | 0.216 +/- 0.028 | 0.280 +/- 0.013 | 0.287 +/- 0.012 | 0.287 +/- 0.012 |
| baseline_mistral_en_t07 | 5 | 0.213 +/- 0.025 | 0.277 +/- 0.009 | 0.286 +/- 0.009 | 0.286 +/- 0.009 |
| actor_critic_mistral_en_t07 | 5 | 0.212 +/- 0.023 | 0.275 +/- 0.011 | 0.285 +/- 0.016 | 0.285 +/- 0.016 |
| baseline_together_llama33_70b_en_t00 | 5 | 0.219 +/- 0.027 | 0.268 +/- 0.012 | 0.285 +/- 0.013 | 0.285 +/- 0.013 |
| agora_union_together_llama33_70b_en_t00 | 5 | 0.226 +/- 0.014 | 0.262 +/- 0.009 | 0.277 +/- 0.009 | 0.277 +/- 0.009 |
| agora_union_mistral_en_t00 | 5 | 0.229 +/- 0.017 | 0.266 +/- 0.008 | 0.276 +/- 0.005 | 0.276 +/- 0.005 |
| agora_union_together_llama33_70b_en_t07 | 5 | 0.220 +/- 0.024 | 0.263 +/- 0.013 | 0.276 +/- 0.011 | 0.276 +/- 0.011 |
| agora_union_mistral_en_t07 | 5 | 0.238 +/- 0.007 | 0.267 +/- 0.009 | 0.273 +/- 0.006 | 0.273 +/- 0.006 |
| mdeberta_baseline_en_t00 | 1 | 0.140 +/- 0.000 | 0.226 +/- 0.000 | 0.213 +/- 0.000 | 0.213 +/- 0.000 |

#### Subnarrative-level (Fine) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| baseline_gemini_en_t07 | 1 | 0.103 +/- 0.000 | 0.123 +/- 0.000 | 0.180 +/- 0.000 | 0.180 +/- 0.000 |
| baseline_gpt5nano_en_t00 | 5 | 0.133 +/- 0.007 | 0.150 +/- 0.009 | 0.167 +/- 0.015 | 0.167 +/- 0.015 |
| agora_majority_gpt5nano_ru_t00 | 1 | 0.143 +/- 0.000 | 0.148 +/- 0.000 | 0.165 +/- 0.000 | 0.165 +/- 0.000 |
| agora_gemini_en_t07 | 5 | 0.108 +/- 0.010 | 0.137 +/- 0.009 | 0.164 +/- 0.020 | 0.164 +/- 0.020 |
| agora_union_gpt5nano_en_t07 | 5 | 0.114 +/- 0.022 | 0.129 +/- 0.015 | 0.162 +/- 0.016 | 0.162 +/- 0.016 |
| agora_majority_gpt5nano_en_t07 | 5 | 0.116 +/- 0.008 | 0.133 +/- 0.008 | 0.160 +/- 0.009 | 0.160 +/- 0.009 |
| agora_union_gpt5nano_en_t00 | 5 | 0.125 +/- 0.015 | 0.133 +/- 0.016 | 0.156 +/- 0.016 | 0.156 +/- 0.016 |
| agora_gemini_en_t00 | 3 | 0.090 +/- 0.003 | 0.118 +/- 0.004 | 0.152 +/- 0.006 | 0.152 +/- 0.006 |
| actor_critic_gpt5nano_en_t07 | 5 | 0.121 +/- 0.013 | 0.140 +/- 0.010 | 0.146 +/- 0.017 | 0.146 +/- 0.017 |
| actor_critic_gemini_en_t07 | 4 | 0.112 +/- 0.020 | 0.140 +/- 0.023 | 0.146 +/- 0.026 | 0.146 +/- 0.026 |
| baseline_gpt5nano_en_t07 | 5 | 0.108 +/- 0.006 | 0.129 +/- 0.006 | 0.145 +/- 0.014 | 0.145 +/- 0.014 |
| actor_critic_gemini_en_t00 | 5 | 0.096 +/- 0.014 | 0.125 +/- 0.007 | 0.144 +/- 0.020 | 0.144 +/- 0.020 |
| baseline_gemini_en_t00 | 5 | 0.097 +/- 0.007 | 0.115 +/- 0.005 | 0.144 +/- 0.008 | 0.144 +/- 0.008 |
| actor_critic_deepseek_en_t00 | 5 | 0.105 +/- 0.008 | 0.129 +/- 0.007 | 0.130 +/- 0.012 | 0.130 +/- 0.012 |
| actor_critic_deepseek_en_t07 | 5 | 0.096 +/- 0.012 | 0.125 +/- 0.017 | 0.124 +/- 0.025 | 0.124 +/- 0.025 |
| actor_critic_deepseek_en_t00_evidence | 1 | 0.105 +/- 0.000 | 0.131 +/- 0.000 | 0.118 +/- 0.000 | 0.118 +/- 0.000 |
| actor_critic_gpt5nano_en_t00 | 5 | 0.093 +/- 0.020 | 0.116 +/- 0.018 | 0.115 +/- 0.026 | 0.115 +/- 0.026 |
| agora_deepseek_en_t07 | 5 | 0.099 +/- 0.006 | 0.115 +/- 0.008 | 0.109 +/- 0.012 | 0.109 +/- 0.012 |
| baseline_deepseek_en_t00_evidence | 1 | 0.126 +/- 0.000 | 0.121 +/- 0.000 | 0.109 +/- 0.000 | 0.109 +/- 0.000 |
| actor_critic_together_llama33_70b_en_t00 | 5 | 0.084 +/- 0.009 | 0.099 +/- 0.007 | 0.106 +/- 0.007 | 0.106 +/- 0.007 |
| agora_deepseek_en_t00 | 5 | 0.102 +/- 0.006 | 0.112 +/- 0.004 | 0.105 +/- 0.005 | 0.105 +/- 0.005 |
| baseline_deepseek_en_t00 | 5 | 0.098 +/- 0.004 | 0.110 +/- 0.006 | 0.103 +/- 0.008 | 0.103 +/- 0.008 |
| actor_critic_together_llama33_70b_en_t07 | 5 | 0.082 +/- 0.011 | 0.098 +/- 0.009 | 0.102 +/- 0.013 | 0.102 +/- 0.013 |
| baseline_deepseek_en_t07 | 5 | 0.100 +/- 0.007 | 0.108 +/- 0.008 | 0.101 +/- 0.008 | 0.101 +/- 0.008 |
| agora_mistral_en_t00 | 5 | 0.075 +/- 0.008 | 0.090 +/- 0.005 | 0.092 +/- 0.013 | 0.092 +/- 0.013 |
| actor_critic_mistral_en_t00_evidence | 1 | 0.083 +/- 0.000 | 0.092 +/- 0.000 | 0.090 +/- 0.000 | 0.090 +/- 0.000 |
| agora_mistral_en_t07 | 5 | 0.072 +/- 0.005 | 0.089 +/- 0.002 | 0.088 +/- 0.003 | 0.088 +/- 0.003 |
| agora_majority_mistral_en_t00 | 5 | 0.077 +/- 0.008 | 0.086 +/- 0.003 | 0.087 +/- 0.008 | 0.087 +/- 0.008 |
| baseline_mistral_en_t00 | 5 | 0.074 +/- 0.004 | 0.084 +/- 0.001 | 0.086 +/- 0.002 | 0.086 +/- 0.002 |
| agora_majority_mistral_en_t00_evidence | 1 | 0.074 +/- 0.000 | 0.084 +/- 0.000 | 0.086 +/- 0.000 | 0.086 +/- 0.000 |
| agora_majority_together_llama33_70b_en_t00 | 5 | 0.078 +/- 0.006 | 0.078 +/- 0.006 | 0.086 +/- 0.009 | 0.086 +/- 0.009 |
| agora_mistral_en_t00_evidence | 1 | 0.071 +/- 0.000 | 0.089 +/- 0.000 | 0.085 +/- 0.000 | 0.085 +/- 0.000 |
| agora_majority_together_llama33_70b_en_t07 | 5 | 0.072 +/- 0.005 | 0.079 +/- 0.006 | 0.085 +/- 0.006 | 0.085 +/- 0.006 |
| baseline_mistral_en_t07 | 5 | 0.073 +/- 0.008 | 0.083 +/- 0.004 | 0.084 +/- 0.005 | 0.084 +/- 0.005 |
| baseline_mistral_en_t00_evidence | 1 | 0.071 +/- 0.000 | 0.080 +/- 0.000 | 0.084 +/- 0.000 | 0.084 +/- 0.000 |
| agora_together_llama33_70b_en_t00 | 5 | 0.067 +/- 0.009 | 0.079 +/- 0.003 | 0.084 +/- 0.005 | 0.084 +/- 0.005 |
| agora_majority_mistral_en_t07 | 5 | 0.071 +/- 0.007 | 0.083 +/- 0.005 | 0.083 +/- 0.005 | 0.083 +/- 0.005 |
| agora_union_mistral_en_t00 | 5 | 0.076 +/- 0.006 | 0.079 +/- 0.004 | 0.082 +/- 0.004 | 0.082 +/- 0.004 |
| baseline_together_llama33_70b_en_t07 | 5 | 0.070 +/- 0.008 | 0.080 +/- 0.003 | 0.081 +/- 0.005 | 0.081 +/- 0.005 |
| actor_critic_mistral_en_t00 | 5 | 0.069 +/- 0.010 | 0.081 +/- 0.004 | 0.080 +/- 0.006 | 0.080 +/- 0.006 |
| actor_critic_mistral_en_t07 | 5 | 0.070 +/- 0.009 | 0.080 +/- 0.005 | 0.080 +/- 0.006 | 0.080 +/- 0.006 |
| agora_union_together_llama33_70b_en_t07 | 5 | 0.071 +/- 0.007 | 0.075 +/- 0.003 | 0.079 +/- 0.004 | 0.079 +/- 0.004 |
| agora_union_mistral_en_t07 | 5 | 0.074 +/- 0.006 | 0.078 +/- 0.003 | 0.079 +/- 0.004 | 0.079 +/- 0.004 |
| agora_union_together_llama33_70b_en_t00 | 5 | 0.071 +/- 0.003 | 0.072 +/- 0.003 | 0.077 +/- 0.003 | 0.077 +/- 0.003 |
| baseline_together_llama33_70b_en_t00 | 5 | 0.070 +/- 0.008 | 0.072 +/- 0.005 | 0.076 +/- 0.004 | 0.076 +/- 0.004 |
| mdeberta_baseline_en_t00 | 1 | 0.092 +/- 0.000 | 0.100 +/- 0.000 | 0.076 +/- 0.000 | 0.076 +/- 0.000 |
| agora_together_llama33_70b_en_t07 | 5 | 0.060 +/- 0.008 | 0.081 +/- 0.010 | 0.074 +/- 0.010 | 0.074 +/- 0.010 |
| actor_critic_gemini_en_t00 | 5 | 0.070 +/- 0.029 | 0.098 +/- 0.033 | 0.067 +/- 0.025 | 0.067 +/- 0.025 |
| actor_critic_gemini_en_t07 | 5 | 0.071 +/- 0.014 | 0.098 +/- 0.023 | 0.051 +/- 0.013 | 0.051 +/- 0.013 |

#### Bootstrap 95% Confidence Intervals

| Experiment | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|------------|--------------------------|-----------------------------|
| agora_gemini_en_t07 | 0.393 +/- 0.037 [0.365, 0.424] | 0.164 +/- 0.020 [0.149, 0.181] |
| agora_gemini_en_t00 | 0.383 +/- 0.014 [0.370, 0.397] | 0.152 +/- 0.006 [0.148, 0.158] |
| baseline_gemini_en_t07 | 0.367 +/- 0.000 [0.367, 0.367] | 0.180 +/- 0.000 [0.180, 0.180] |
| agora_deepseek_en_t07 | 0.363 +/- 0.020 [0.348, 0.377] | 0.109 +/- 0.012 [0.100, 0.118] |
| baseline_deepseek_en_t00_evidence | 0.355 +/- 0.000 [0.355, 0.355] | 0.109 +/- 0.000 [0.109, 0.109] |
| actor_critic_deepseek_en_t00_evidence | 0.355 +/- 0.000 [0.355, 0.355] | 0.118 +/- 0.000 [0.118, 0.118] |
| baseline_gemini_en_t00 | 0.354 +/- 0.012 [0.346, 0.365] | 0.144 +/- 0.008 [0.138, 0.151] |
| agora_deepseek_en_t00 | 0.349 +/- 0.007 [0.343, 0.355] | 0.105 +/- 0.005 [0.101, 0.108] |
| actor_critic_deepseek_en_t00 | 0.347 +/- 0.020 [0.330, 0.361] | 0.130 +/- 0.012 [0.121, 0.140] |
| actor_critic_gemini_en_t07 | 0.347 +/- 0.038 [0.314, 0.380] | 0.146 +/- 0.026 [0.123, 0.165] |
| actor_critic_deepseek_en_t07 | 0.343 +/- 0.042 [0.315, 0.379] | 0.124 +/- 0.025 [0.105, 0.143] |
| baseline_deepseek_en_t00 | 0.342 +/- 0.013 [0.331, 0.352] | 0.103 +/- 0.008 [0.097, 0.109] |
| baseline_gpt5nano_en_t00 | 0.341 +/- 0.034 [0.317, 0.370] | 0.167 +/- 0.015 [0.155, 0.179] |
| agora_majority_gpt5nano_ru_t00 | 0.339 +/- 0.000 [0.339, 0.339] | 0.165 +/- 0.000 [0.165, 0.165] |
| agora_majority_gpt5nano_en_t07 | 0.337 +/- 0.019 [0.321, 0.352] | 0.160 +/- 0.009 [0.154, 0.167] |
| actor_critic_gemini_en_t00 | 0.334 +/- 0.018 [0.319, 0.348] | 0.144 +/- 0.020 [0.128, 0.157] |
| actor_critic_gpt5nano_en_t07 | 0.331 +/- 0.020 [0.312, 0.342] | 0.146 +/- 0.017 [0.135, 0.159] |
| baseline_deepseek_en_t07 | 0.329 +/- 0.012 [0.319, 0.339] | 0.101 +/- 0.008 [0.094, 0.107] |
| agora_mistral_en_t00 | 0.325 +/- 0.022 [0.310, 0.343] | 0.092 +/- 0.013 [0.083, 0.102] |
| actor_critic_together_llama33_70b_en_t00 | 0.319 +/- 0.010 [0.312, 0.328] | 0.106 +/- 0.007 [0.100, 0.110] |
| agora_together_llama33_70b_en_t00 | 0.318 +/- 0.015 [0.307, 0.330] | 0.084 +/- 0.005 [0.080, 0.088] |
| agora_mistral_en_t07 | 0.318 +/- 0.008 [0.311, 0.323] | 0.088 +/- 0.003 [0.085, 0.090] |
| agora_union_gpt5nano_en_t07 | 0.318 +/- 0.015 [0.307, 0.331] | 0.162 +/- 0.016 [0.149, 0.174] |
| agora_mistral_en_t00_evidence | 0.314 +/- 0.000 [0.314, 0.314] | 0.085 +/- 0.000 [0.085, 0.085] |
| actor_critic_gemini_en_t07 | 0.310 +/- 0.019 [0.296, 0.323] | 0.051 +/- 0.013 [0.041, 0.060] |
| agora_union_gpt5nano_en_t00 | 0.309 +/- 0.026 [0.290, 0.331] | 0.156 +/- 0.016 [0.144, 0.168] |
| baseline_gpt5nano_en_t07 | 0.308 +/- 0.021 [0.292, 0.324] | 0.145 +/- 0.014 [0.135, 0.156] |
| agora_majority_together_llama33_70b_en_t00 | 0.307 +/- 0.016 [0.295, 0.319] | 0.086 +/- 0.009 [0.079, 0.092] |
| actor_critic_together_llama33_70b_en_t07 | 0.307 +/- 0.024 [0.289, 0.327] | 0.102 +/- 0.013 [0.094, 0.113] |
| agora_majority_mistral_en_t00 | 0.303 +/- 0.021 [0.289, 0.322] | 0.087 +/- 0.008 [0.082, 0.095] |
| agora_majority_together_llama33_70b_en_t07 | 0.302 +/- 0.014 [0.290, 0.312] | 0.085 +/- 0.006 [0.080, 0.090] |
| actor_critic_gemini_en_t00 | 0.301 +/- 0.019 [0.289, 0.317] | 0.067 +/- 0.025 [0.048, 0.088] |
| baseline_together_llama33_70b_en_t07 | 0.300 +/- 0.009 [0.293, 0.307] | 0.081 +/- 0.005 [0.077, 0.085] |
| agora_together_llama33_70b_en_t07 | 0.300 +/- 0.021 [0.287, 0.319] | 0.074 +/- 0.010 [0.067, 0.082] |
| actor_critic_mistral_en_t00_evidence | 0.299 +/- 0.000 [0.299, 0.299] | 0.090 +/- 0.000 [0.090, 0.090] |
| baseline_mistral_en_t00 | 0.297 +/- 0.005 [0.293, 0.300] | 0.086 +/- 0.002 [0.085, 0.087] |
| agora_majority_mistral_en_t07 | 0.297 +/- 0.014 [0.286, 0.308] | 0.083 +/- 0.005 [0.079, 0.087] |
| actor_critic_gpt5nano_en_t00 | 0.294 +/- 0.018 [0.279, 0.307] | 0.115 +/- 0.026 [0.092, 0.134] |
| agora_majority_mistral_en_t00_evidence | 0.292 +/- 0.000 [0.292, 0.292] | 0.086 +/- 0.000 [0.086, 0.086] |
| baseline_mistral_en_t00_evidence | 0.289 +/- 0.000 [0.289, 0.289] | 0.084 +/- 0.000 [0.084, 0.084] |
| actor_critic_mistral_en_t00 | 0.287 +/- 0.012 [0.278, 0.296] | 0.080 +/- 0.006 [0.075, 0.086] |
| baseline_mistral_en_t07 | 0.286 +/- 0.009 [0.281, 0.294] | 0.084 +/- 0.005 [0.081, 0.088] |
| actor_critic_mistral_en_t07 | 0.285 +/- 0.016 [0.273, 0.297] | 0.080 +/- 0.006 [0.076, 0.085] |
| baseline_together_llama33_70b_en_t00 | 0.285 +/- 0.013 [0.274, 0.296] | 0.076 +/- 0.004 [0.073, 0.079] |
| agora_union_together_llama33_70b_en_t00 | 0.277 +/- 0.009 [0.270, 0.284] | 0.077 +/- 0.003 [0.075, 0.079] |
| agora_union_mistral_en_t00 | 0.276 +/- 0.005 [0.272, 0.279] | 0.082 +/- 0.004 [0.078, 0.085] |
| agora_union_together_llama33_70b_en_t07 | 0.276 +/- 0.011 [0.267, 0.284] | 0.079 +/- 0.004 [0.076, 0.082] |
| agora_union_mistral_en_t07 | 0.273 +/- 0.006 [0.270, 0.278] | 0.079 +/- 0.004 [0.076, 0.082] |
| mdeberta_baseline_en_t00 | 0.213 +/- 0.000 [0.213, 0.213] | 0.076 +/- 0.000 [0.076, 0.076] |

### Language: HI

Ground truth: `data/dev-documents_4_December\HI\subtask-3-dominant-narratives.txt`

#### Narrative-level (Coarse) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| agora_deepseek_hi_t00 | 5 | 0.316 +/- 0.042 | 0.461 +/- 0.006 | 0.462 +/- 0.011 | 0.462 +/- 0.011 |
| baseline_deepseek_hi_t00 | 5 | 0.316 +/- 0.024 | 0.416 +/- 0.016 | 0.430 +/- 0.021 | 0.430 +/- 0.021 |
| agora_majority_gpt5nano_hi_t00 | 5 | 0.262 +/- 0.032 | 0.398 +/- 0.013 | 0.400 +/- 0.027 | 0.400 +/- 0.027 |
| actor_critic_deepseek_hi_t00 | 5 | 0.301 +/- 0.031 | 0.400 +/- 0.026 | 0.388 +/- 0.028 | 0.388 +/- 0.028 |
| agora_mistral_hi_t00 | 5 | 0.241 +/- 0.031 | 0.337 +/- 0.025 | 0.348 +/- 0.038 | 0.348 +/- 0.038 |
| mdeberta_baseline_hi_t00 | 1 | 0.182 +/- 0.000 | 0.340 +/- 0.000 | 0.345 +/- 0.000 | 0.345 +/- 0.000 |
| baseline_mistral_hi_t00 | 5 | 0.210 +/- 0.009 | 0.308 +/- 0.011 | 0.320 +/- 0.023 | 0.320 +/- 0.023 |
| agora_majority_mistral_hi_t00 | 5 | 0.218 +/- 0.015 | 0.306 +/- 0.005 | 0.319 +/- 0.009 | 0.319 +/- 0.009 |
| actor_critic_mistral_hi_t00 | 5 | 0.214 +/- 0.029 | 0.298 +/- 0.012 | 0.306 +/- 0.014 | 0.306 +/- 0.014 |
| agora_majority_together_llama33_70b_hi_t00 | 5 | 0.161 +/- 0.014 | 0.260 +/- 0.030 | 0.228 +/- 0.035 | 0.228 +/- 0.035 |

#### Subnarrative-level (Fine) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_baseline_hi_t00 | 1 | 0.125 +/- 0.000 | 0.227 +/- 0.000 | 0.244 +/- 0.000 | 0.244 +/- 0.000 |
| agora_majority_gpt5nano_hi_t00 | 5 | 0.121 +/- 0.010 | 0.184 +/- 0.019 | 0.191 +/- 0.024 | 0.191 +/- 0.024 |
| agora_deepseek_hi_t00 | 5 | 0.125 +/- 0.014 | 0.168 +/- 0.008 | 0.186 +/- 0.015 | 0.186 +/- 0.015 |
| baseline_deepseek_hi_t00 | 5 | 0.121 +/- 0.003 | 0.152 +/- 0.009 | 0.184 +/- 0.013 | 0.184 +/- 0.013 |
| actor_critic_deepseek_hi_t00 | 5 | 0.107 +/- 0.007 | 0.132 +/- 0.009 | 0.130 +/- 0.009 | 0.130 +/- 0.009 |
| agora_mistral_hi_t00 | 5 | 0.082 +/- 0.010 | 0.096 +/- 0.008 | 0.115 +/- 0.015 | 0.115 +/- 0.015 |
| agora_majority_mistral_hi_t00 | 5 | 0.077 +/- 0.005 | 0.089 +/- 0.003 | 0.104 +/- 0.008 | 0.104 +/- 0.008 |
| baseline_mistral_hi_t00 | 5 | 0.074 +/- 0.002 | 0.088 +/- 0.003 | 0.100 +/- 0.010 | 0.100 +/- 0.010 |
| actor_critic_mistral_hi_t00 | 5 | 0.075 +/- 0.010 | 0.087 +/- 0.006 | 0.099 +/- 0.007 | 0.099 +/- 0.007 |
| agora_majority_together_llama33_70b_hi_t00 | 5 | 0.066 +/- 0.010 | 0.074 +/- 0.012 | 0.065 +/- 0.013 | 0.065 +/- 0.013 |

#### Bootstrap 95% Confidence Intervals

| Experiment | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|------------|--------------------------|-----------------------------|
| agora_deepseek_hi_t00 | 0.462 +/- 0.011 [0.452, 0.469] | 0.186 +/- 0.015 [0.174, 0.197] |
| baseline_deepseek_hi_t00 | 0.430 +/- 0.021 [0.413, 0.444] | 0.184 +/- 0.013 [0.174, 0.195] |
| agora_majority_gpt5nano_hi_t00 | 0.400 +/- 0.027 [0.379, 0.419] | 0.191 +/- 0.024 [0.171, 0.209] |
| actor_critic_deepseek_hi_t00 | 0.388 +/- 0.028 [0.366, 0.411] | 0.130 +/- 0.009 [0.123, 0.137] |
| agora_mistral_hi_t00 | 0.348 +/- 0.038 [0.322, 0.381] | 0.115 +/- 0.015 [0.105, 0.129] |
| mdeberta_baseline_hi_t00 | 0.345 +/- 0.000 [0.345, 0.345] | 0.244 +/- 0.000 [0.244, 0.244] |
| baseline_mistral_hi_t00 | 0.320 +/- 0.023 [0.302, 0.338] | 0.100 +/- 0.010 [0.093, 0.108] |
| agora_majority_mistral_hi_t00 | 0.319 +/- 0.009 [0.312, 0.327] | 0.104 +/- 0.008 [0.098, 0.111] |
| actor_critic_mistral_hi_t00 | 0.306 +/- 0.014 [0.294, 0.316] | 0.099 +/- 0.007 [0.094, 0.104] |
| agora_majority_together_llama33_70b_hi_t00 | 0.228 +/- 0.035 [0.197, 0.249] | 0.065 +/- 0.013 [0.054, 0.074] |

### Language: PT

Ground truth: `data/dev-documents_4_December\PT\subtask-3-dominant-narratives.txt`

#### Narrative-level (Coarse) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| mdeberta_baseline_pt_t00 | 1 | 0.310 +/- 0.000 | 0.580 +/- 0.000 | 0.629 +/- 0.000 | 0.629 +/- 0.000 |
| agora_majority_gpt5nano_pt_t00 | 5 | 0.334 +/- 0.044 | 0.559 +/- 0.026 | 0.584 +/- 0.030 | 0.584 +/- 0.030 |
| agora_majority_deepseek_pt_t00 | 5 | 0.383 +/- 0.035 | 0.533 +/- 0.018 | 0.548 +/- 0.021 | 0.548 +/- 0.021 |
| agora_union_deepseek_pt_t00 | 5 | 0.349 +/- 0.013 | 0.522 +/- 0.029 | 0.546 +/- 0.038 | 0.546 +/- 0.038 |
| baseline_deepseek_pt_t00 | 5 | 0.382 +/- 0.021 | 0.506 +/- 0.013 | 0.510 +/- 0.020 | 0.510 +/- 0.020 |
| baseline_deepseek_pt_t07 | 5 | 0.369 +/- 0.026 | 0.500 +/- 0.022 | 0.504 +/- 0.030 | 0.504 +/- 0.030 |
| agora_deepseek_pt_t00 | 5 | 0.408 +/- 0.029 | 0.487 +/- 0.030 | 0.476 +/- 0.038 | 0.476 +/- 0.038 |
| agora_mistral_pt_t00 | 5 | 0.284 +/- 0.019 | 0.445 +/- 0.034 | 0.464 +/- 0.044 | 0.464 +/- 0.044 |
| agora_majority_mistral_pt_t00 | 5 | 0.260 +/- 0.012 | 0.399 +/- 0.027 | 0.410 +/- 0.049 | 0.410 +/- 0.049 |
| actor_critic_deepseek_pt_t00 | 5 | 0.294 +/- 0.028 | 0.408 +/- 0.046 | 0.383 +/- 0.055 | 0.383 +/- 0.055 |
| baseline_mistral_pt_t00 | 5 | 0.247 +/- 0.007 | 0.372 +/- 0.016 | 0.382 +/- 0.036 | 0.382 +/- 0.036 |
| actor_critic_mistral_pt_t00 | 5 | 0.255 +/- 0.009 | 0.372 +/- 0.012 | 0.374 +/- 0.019 | 0.374 +/- 0.019 |
| agora_majority_together_llama33_70b_pt_t00 | 5 | 0.207 +/- 0.007 | 0.259 +/- 0.010 | 0.199 +/- 0.010 | 0.199 +/- 0.010 |

#### Subnarrative-level (Fine) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| agora_majority_gpt5nano_pt_t00 | 5 | 0.183 +/- 0.009 | 0.308 +/- 0.022 | 0.283 +/- 0.028 | 0.283 +/- 0.028 |
| agora_majority_deepseek_pt_t00 | 5 | 0.138 +/- 0.011 | 0.208 +/- 0.010 | 0.228 +/- 0.015 | 0.228 +/- 0.015 |
| agora_union_deepseek_pt_t00 | 5 | 0.115 +/- 0.015 | 0.192 +/- 0.017 | 0.220 +/- 0.024 | 0.220 +/- 0.024 |
| baseline_deepseek_pt_t07 | 5 | 0.131 +/- 0.011 | 0.203 +/- 0.020 | 0.209 +/- 0.028 | 0.209 +/- 0.028 |
| baseline_deepseek_pt_t00 | 5 | 0.125 +/- 0.014 | 0.190 +/- 0.014 | 0.202 +/- 0.017 | 0.202 +/- 0.017 |
| agora_deepseek_pt_t00 | 5 | 0.134 +/- 0.013 | 0.193 +/- 0.012 | 0.180 +/- 0.024 | 0.180 +/- 0.024 |
| agora_mistral_pt_t00 | 5 | 0.091 +/- 0.004 | 0.154 +/- 0.016 | 0.153 +/- 0.022 | 0.153 +/- 0.022 |
| agora_majority_mistral_pt_t00 | 5 | 0.087 +/- 0.003 | 0.138 +/- 0.010 | 0.135 +/- 0.018 | 0.135 +/- 0.018 |
| actor_critic_deepseek_pt_t00 | 5 | 0.132 +/- 0.030 | 0.166 +/- 0.018 | 0.127 +/- 0.027 | 0.127 +/- 0.027 |
| actor_critic_mistral_pt_t00 | 5 | 0.086 +/- 0.002 | 0.129 +/- 0.006 | 0.123 +/- 0.010 | 0.123 +/- 0.010 |
| baseline_mistral_pt_t00 | 5 | 0.082 +/- 0.005 | 0.127 +/- 0.006 | 0.123 +/- 0.015 | 0.123 +/- 0.015 |
| mdeberta_baseline_pt_t00 | 1 | 0.097 +/- 0.000 | 0.158 +/- 0.000 | 0.121 +/- 0.000 | 0.121 +/- 0.000 |
| agora_majority_together_llama33_70b_pt_t00 | 5 | 0.086 +/- 0.003 | 0.120 +/- 0.005 | 0.074 +/- 0.004 | 0.074 +/- 0.004 |

#### Bootstrap 95% Confidence Intervals

| Experiment | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|------------|--------------------------|-----------------------------|
| mdeberta_baseline_pt_t00 | 0.629 +/- 0.000 [0.629, 0.629] | 0.121 +/- 0.000 [0.121, 0.121] |
| agora_majority_gpt5nano_pt_t00 | 0.584 +/- 0.030 [0.561, 0.607] | 0.283 +/- 0.028 [0.259, 0.300] |
| agora_majority_deepseek_pt_t00 | 0.548 +/- 0.021 [0.532, 0.564] | 0.228 +/- 0.015 [0.219, 0.241] |
| agora_union_deepseek_pt_t00 | 0.546 +/- 0.038 [0.513, 0.573] | 0.220 +/- 0.024 [0.201, 0.239] |
| baseline_deepseek_pt_t00 | 0.510 +/- 0.020 [0.494, 0.525] | 0.202 +/- 0.017 [0.188, 0.213] |
| baseline_deepseek_pt_t07 | 0.504 +/- 0.030 [0.478, 0.524] | 0.209 +/- 0.028 [0.187, 0.230] |
| agora_deepseek_pt_t00 | 0.476 +/- 0.038 [0.445, 0.505] | 0.180 +/- 0.024 [0.161, 0.199] |
| agora_mistral_pt_t00 | 0.464 +/- 0.044 [0.430, 0.499] | 0.153 +/- 0.022 [0.136, 0.171] |
| agora_majority_mistral_pt_t00 | 0.410 +/- 0.049 [0.371, 0.449] | 0.135 +/- 0.018 [0.122, 0.149] |
| actor_critic_deepseek_pt_t00 | 0.383 +/- 0.055 [0.340, 0.424] | 0.127 +/- 0.027 [0.105, 0.147] |
| baseline_mistral_pt_t00 | 0.382 +/- 0.036 [0.355, 0.408] | 0.123 +/- 0.015 [0.112, 0.135] |
| actor_critic_mistral_pt_t00 | 0.374 +/- 0.019 [0.359, 0.389] | 0.123 +/- 0.010 [0.115, 0.131] |
| agora_majority_together_llama33_70b_pt_t00 | 0.199 +/- 0.010 [0.192, 0.207] | 0.074 +/- 0.004 [0.071, 0.077] |

### Language: RU

Ground truth: `data/dev-documents_4_December\RU\subtask-3-dominant-narratives.txt`

#### Narrative-level (Coarse) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| agora_deepseek_ru_t07 | 5 | 0.272 +/- 0.020 | 0.471 +/- 0.015 | 0.505 +/- 0.020 | 0.505 +/- 0.020 |
| agora_deepseek_ru_t00 | 5 | 0.269 +/- 0.025 | 0.464 +/- 0.016 | 0.504 +/- 0.021 | 0.504 +/- 0.021 |
| baseline_deepseek_ru_t00 | 5 | 0.236 +/- 0.014 | 0.440 +/- 0.013 | 0.481 +/- 0.018 | 0.481 +/- 0.018 |
| baseline_deepseek_ru_t07 | 5 | 0.232 +/- 0.014 | 0.431 +/- 0.009 | 0.472 +/- 0.009 | 0.472 +/- 0.009 |
| actor_critic_deepseek_ru_t00 | 5 | 0.214 +/- 0.024 | 0.424 +/- 0.012 | 0.454 +/- 0.021 | 0.454 +/- 0.021 |
| actor_critic_deepseek_ru_t07 | 5 | 0.214 +/- 0.035 | 0.424 +/- 0.023 | 0.451 +/- 0.022 | 0.451 +/- 0.022 |
| agora_majority_gpt5nano_ru_t00 | 5 | 0.223 +/- 0.036 | 0.408 +/- 0.038 | 0.428 +/- 0.041 | 0.428 +/- 0.041 |
| agora_majority_mistral_ru_t00 | 5 | 0.218 +/- 0.009 | 0.371 +/- 0.010 | 0.409 +/- 0.013 | 0.409 +/- 0.013 |
| agora_mistral_ru_t00 | 5 | 0.198 +/- 0.028 | 0.390 +/- 0.016 | 0.407 +/- 0.031 | 0.407 +/- 0.031 |
| actor_critic_mistral_ru_t00 | 5 | 0.214 +/- 0.015 | 0.359 +/- 0.012 | 0.387 +/- 0.017 | 0.387 +/- 0.017 |
| baseline_mistral_ru_t00 | 5 | 0.208 +/- 0.017 | 0.353 +/- 0.007 | 0.382 +/- 0.008 | 0.382 +/- 0.008 |
| agora_majority_together_llama33_70b_ru_t00 | 5 | 0.191 +/- 0.021 | 0.338 +/- 0.007 | 0.363 +/- 0.009 | 0.363 +/- 0.009 |
| mdeberta_baseline_ru_t00 | 1 | 0.113 +/- 0.000 | 0.224 +/- 0.000 | 0.199 +/- 0.000 | 0.199 +/- 0.000 |

#### Subnarrative-level (Fine) Metrics

| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |
|------------|------|----------|----------|------------|---------------------|
| agora_majority_gpt5nano_ru_t00 | 5 | 0.163 +/- 0.027 | 0.226 +/- 0.025 | 0.225 +/- 0.045 | 0.225 +/- 0.045 |
| actor_critic_deepseek_ru_t07 | 5 | 0.132 +/- 0.021 | 0.194 +/- 0.027 | 0.217 +/- 0.041 | 0.217 +/- 0.041 |
| agora_deepseek_ru_t00 | 5 | 0.149 +/- 0.009 | 0.194 +/- 0.005 | 0.215 +/- 0.003 | 0.215 +/- 0.003 |
| actor_critic_deepseek_ru_t00 | 5 | 0.135 +/- 0.008 | 0.185 +/- 0.009 | 0.212 +/- 0.015 | 0.212 +/- 0.015 |
| agora_deepseek_ru_t07 | 5 | 0.145 +/- 0.015 | 0.191 +/- 0.012 | 0.212 +/- 0.018 | 0.212 +/- 0.018 |
| baseline_deepseek_ru_t00 | 5 | 0.137 +/- 0.010 | 0.177 +/- 0.009 | 0.205 +/- 0.007 | 0.205 +/- 0.007 |
| baseline_deepseek_ru_t07 | 5 | 0.130 +/- 0.005 | 0.174 +/- 0.003 | 0.200 +/- 0.005 | 0.200 +/- 0.005 |
| agora_mistral_ru_t00 | 5 | 0.117 +/- 0.008 | 0.135 +/- 0.008 | 0.148 +/- 0.018 | 0.148 +/- 0.018 |
| agora_majority_mistral_ru_t00 | 5 | 0.126 +/- 0.004 | 0.122 +/- 0.004 | 0.142 +/- 0.007 | 0.142 +/- 0.007 |
| agora_majority_together_llama33_70b_ru_t00 | 5 | 0.112 +/- 0.005 | 0.123 +/- 0.002 | 0.141 +/- 0.002 | 0.141 +/- 0.002 |
| actor_critic_mistral_ru_t00 | 5 | 0.134 +/- 0.002 | 0.122 +/- 0.003 | 0.139 +/- 0.004 | 0.139 +/- 0.004 |
| baseline_mistral_ru_t00 | 5 | 0.129 +/- 0.005 | 0.117 +/- 0.001 | 0.135 +/- 0.004 | 0.135 +/- 0.004 |
| mdeberta_baseline_ru_t00 | 1 | 0.047 +/- 0.000 | 0.116 +/- 0.000 | 0.124 +/- 0.000 | 0.124 +/- 0.000 |

#### Bootstrap 95% Confidence Intervals

| Experiment | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |
|------------|--------------------------|-----------------------------|
| agora_deepseek_ru_t07 | 0.505 +/- 0.020 [0.492, 0.522] | 0.212 +/- 0.018 [0.198, 0.225] |
| agora_deepseek_ru_t00 | 0.504 +/- 0.021 [0.488, 0.520] | 0.215 +/- 0.003 [0.213, 0.218] |
| baseline_deepseek_ru_t00 | 0.481 +/- 0.018 [0.468, 0.496] | 0.205 +/- 0.007 [0.200, 0.211] |
| baseline_deepseek_ru_t07 | 0.472 +/- 0.009 [0.466, 0.479] | 0.200 +/- 0.005 [0.196, 0.204] |
| actor_critic_deepseek_ru_t00 | 0.454 +/- 0.021 [0.440, 0.472] | 0.212 +/- 0.015 [0.201, 0.223] |
| actor_critic_deepseek_ru_t07 | 0.451 +/- 0.022 [0.435, 0.468] | 0.217 +/- 0.041 [0.183, 0.247] |
| agora_majority_gpt5nano_ru_t00 | 0.428 +/- 0.041 [0.394, 0.455] | 0.225 +/- 0.045 [0.190, 0.258] |
| agora_majority_mistral_ru_t00 | 0.409 +/- 0.013 [0.400, 0.419] | 0.142 +/- 0.007 [0.136, 0.146] |
| agora_mistral_ru_t00 | 0.407 +/- 0.031 [0.383, 0.431] | 0.148 +/- 0.018 [0.135, 0.161] |
| actor_critic_mistral_ru_t00 | 0.387 +/- 0.017 [0.375, 0.401] | 0.139 +/- 0.004 [0.136, 0.143] |
| baseline_mistral_ru_t00 | 0.382 +/- 0.008 [0.375, 0.388] | 0.135 +/- 0.004 [0.132, 0.139] |
| agora_majority_together_llama33_70b_ru_t00 | 0.363 +/- 0.009 [0.354, 0.369] | 0.141 +/- 0.002 [0.140, 0.143] |
| mdeberta_baseline_ru_t00 | 0.199 +/- 0.000 [0.199, 0.199] | 0.124 +/- 0.000 [0.124, 0.124] |

## Cross-Architecture Comparison

Comparison of three architectures — **Baseline** (single-agent, no validation), **Actor-Critic** (single-agent + validation nodes), and **Agora** (3-agent ensemble) — matched by model, language, and temperature. For Agora, we report the best-performing aggregation strategy (intersection/majority/union). mDeBERTa fine-tuned baseline included for reference.

p-values from paired t-test on per-run F1-samples scores. Significance: \* p<0.05, \*\* p<0.01, \*\*\* p<0.001

### Temperature = 0.0

#### Narrative-level F1-samples

| Lang | Model | Baseline | Actor-Critic | p (AC vs BL) | Best Agora (agg) | p (Agora vs BL) |
|------|-------|----------|-------------|--------------|-----------------|----------------|
| BG | DeepSeek V3 | 0.575 +/- 0.010 | 0.453 +/- 0.039 | 0.0028** | 0.606 +/- 0.013 (intersection) | 0.0169* |
| BG | GPT-5 Nano | — | — | — | 0.509 +/- 0.026 (majority) | — |
| BG | Llama 3.3 70B | — | — | — | 0.315 +/- 0.019 (majority) | — |
| BG | Mistral Large | 0.469 +/- 0.019 | 0.474 +/- 0.020 | 0.7907 | 0.483 +/- 0.012 (intersection) | 0.2520 |
| BG | mDeBERTa v3 (fine-tuned) | 0.413 +/- 0.000 | — | — | — | — |
| EN | DeepSeek V3 | 0.342 +/- 0.013 | 0.347 +/- 0.020 | 0.6746 | 0.349 +/- 0.007 (intersection) | 0.4782 |
| EN | GPT-5 Nano | 0.341 +/- 0.034 | 0.294 +/- 0.018 | 0.0373* | 0.339 +/- 0.000 (majority) | — |
| EN | Gemini 2.5 Flash | 0.354 +/- 0.012 | 0.334 +/- 0.018 | 0.1288 | 0.383 +/- 0.014 (intersection) | 0.0989 |
| EN | Llama 3.3 70B | 0.285 +/- 0.013 | 0.319 +/- 0.010 | 0.0254* | 0.318 +/- 0.015 (intersection) | 0.0202* |
| EN | Mistral Large | 0.297 +/- 0.005 | 0.287 +/- 0.012 | 0.1605 | 0.325 +/- 0.022 (intersection) | 0.0417* |
| EN | mDeBERTa v3 (fine-tuned) | 0.213 +/- 0.000 | — | — | — | — |
| HI | DeepSeek V3 | 0.430 +/- 0.021 | 0.388 +/- 0.028 | 0.0481* | 0.462 +/- 0.011 (intersection) | 0.0060** |
| HI | GPT-5 Nano | — | — | — | 0.400 +/- 0.027 (majority) | — |
| HI | Llama 3.3 70B | — | — | — | 0.228 +/- 0.035 (majority) | — |
| HI | Mistral Large | 0.320 +/- 0.023 | 0.306 +/- 0.014 | 0.3532 | 0.348 +/- 0.038 (intersection) | 0.3095 |
| HI | mDeBERTa v3 (fine-tuned) | 0.345 +/- 0.000 | — | — | — | — |
| PT | DeepSeek V3 | 0.510 +/- 0.020 | 0.383 +/- 0.055 | 0.0055** | 0.548 +/- 0.021 (majority) | 0.0012** |
| PT | GPT-5 Nano | — | — | — | 0.584 +/- 0.030 (majority) | — |
| PT | Llama 3.3 70B | — | — | — | 0.199 +/- 0.010 (majority) | — |
| PT | Mistral Large | 0.382 +/- 0.036 | 0.374 +/- 0.019 | 0.6428 | 0.464 +/- 0.044 (intersection) | 0.0281* |
| PT | mDeBERTa v3 (fine-tuned) | 0.629 +/- 0.000 | — | — | — | — |
| RU | DeepSeek V3 | 0.481 +/- 0.018 | 0.454 +/- 0.021 | 0.0921 | 0.504 +/- 0.021 (intersection) | 0.1979 |
| RU | GPT-5 Nano | — | — | — | 0.428 +/- 0.041 (majority) | — |
| RU | Llama 3.3 70B | — | — | — | 0.363 +/- 0.009 (majority) | — |
| RU | Mistral Large | 0.382 +/- 0.008 | 0.387 +/- 0.017 | 0.4724 | 0.409 +/- 0.013 (majority) | 0.0159* |
| RU | mDeBERTa v3 (fine-tuned) | 0.199 +/- 0.000 | — | — | — | — |

#### Subnarrative-level F1-samples

| Lang | Model | Baseline | Actor-Critic | p (AC vs BL) | Best Agora (agg) | p (Agora vs BL) |
|------|-------|----------|-------------|--------------|-----------------|----------------|
| BG | DeepSeek V3 | 0.217 +/- 0.006 | 0.187 +/- 0.019 | 0.0435* | 0.237 +/- 0.004 (intersection) | 0.0038** |
| BG | GPT-5 Nano | — | — | — | 0.244 +/- 0.017 (majority) | — |
| BG | Llama 3.3 70B | — | — | — | 0.114 +/- 0.007 (majority) | — |
| BG | Mistral Large | 0.145 +/- 0.007 | 0.143 +/- 0.012 | 0.7802 | 0.155 +/- 0.009 (intersection) | 0.1659 |
| BG | mDeBERTa v3 (fine-tuned) | 0.220 +/- 0.000 | — | — | — | — |
| EN | DeepSeek V3 | 0.103 +/- 0.008 | 0.130 +/- 0.012 | 0.0207* | 0.105 +/- 0.005 (intersection) | 0.7933 |
| EN | GPT-5 Nano | 0.167 +/- 0.015 | 0.115 +/- 0.026 | 0.0103* | 0.165 +/- 0.000 (majority) | — |
| EN | Gemini 2.5 Flash | 0.144 +/- 0.008 | 0.144 +/- 0.020 | 0.9552 | 0.152 +/- 0.006 (intersection) | 0.1041 |
| EN | Llama 3.3 70B | 0.076 +/- 0.004 | 0.106 +/- 0.007 | 0.0027** | 0.086 +/- 0.009 (majority) | 0.0228* |
| EN | Mistral Large | 0.086 +/- 0.002 | 0.080 +/- 0.006 | 0.1268 | 0.092 +/- 0.013 (intersection) | 0.3251 |
| EN | mDeBERTa v3 (fine-tuned) | 0.076 +/- 0.000 | — | — | — | — |
| HI | DeepSeek V3 | 0.184 +/- 0.013 | 0.130 +/- 0.009 | 0.0020** | 0.186 +/- 0.015 (intersection) | 0.7986 |
| HI | GPT-5 Nano | — | — | — | 0.191 +/- 0.024 (majority) | — |
| HI | Llama 3.3 70B | — | — | — | 0.065 +/- 0.013 (majority) | — |
| HI | Mistral Large | 0.100 +/- 0.010 | 0.099 +/- 0.007 | 0.7897 | 0.115 +/- 0.015 (intersection) | 0.2223 |
| HI | mDeBERTa v3 (fine-tuned) | 0.244 +/- 0.000 | — | — | — | — |
| PT | DeepSeek V3 | 0.202 +/- 0.017 | 0.127 +/- 0.027 | 0.0082** | 0.228 +/- 0.015 (majority) | 0.0305* |
| PT | GPT-5 Nano | — | — | — | 0.283 +/- 0.028 (majority) | — |
| PT | Llama 3.3 70B | — | — | — | 0.074 +/- 0.004 (majority) | — |
| PT | Mistral Large | 0.123 +/- 0.015 | 0.123 +/- 0.010 | 0.9408 | 0.153 +/- 0.022 (intersection) | 0.1009 |
| PT | mDeBERTa v3 (fine-tuned) | 0.121 +/- 0.000 | — | — | — | — |
| RU | DeepSeek V3 | 0.205 +/- 0.007 | 0.212 +/- 0.015 | 0.2620 | 0.215 +/- 0.003 (intersection) | 0.0761 |
| RU | GPT-5 Nano | — | — | — | 0.225 +/- 0.045 (majority) | — |
| RU | Llama 3.3 70B | — | — | — | 0.141 +/- 0.002 (majority) | — |
| RU | Mistral Large | 0.135 +/- 0.004 | 0.139 +/- 0.004 | 0.0593 | 0.148 +/- 0.018 (intersection) | 0.1846 |
| RU | mDeBERTa v3 (fine-tuned) | 0.124 +/- 0.000 | — | — | — | — |

### Temperature = 0.7

#### Narrative-level F1-samples

| Lang | Model | Baseline | Actor-Critic | p (AC vs BL) | Best Agora (agg) | p (Agora vs BL) |
|------|-------|----------|-------------|--------------|-----------------|----------------|
| BG | DeepSeek V3 | 0.565 +/- 0.008 | 0.490 +/- 0.049 | 0.0382* | 0.599 +/- 0.011 (intersection) | 0.0044** |
| EN | DeepSeek V3 | 0.329 +/- 0.012 | 0.343 +/- 0.042 | 0.5097 | 0.363 +/- 0.020 (intersection) | 0.0193* |
| EN | GPT-5 Nano | 0.308 +/- 0.021 | 0.331 +/- 0.020 | 0.0994 | 0.337 +/- 0.019 (majority) | 0.0825 |
| EN | Gemini 2.5 Flash | 0.367 +/- 0.000 | 0.347 +/- 0.038 | — | 0.393 +/- 0.037 (intersection) | — |
| EN | Llama 3.3 70B | 0.300 +/- 0.009 | 0.307 +/- 0.024 | 0.6463 | 0.302 +/- 0.014 (majority) | 0.8005 |
| EN | Mistral Large | 0.286 +/- 0.009 | 0.285 +/- 0.016 | 0.9117 | 0.318 +/- 0.008 (intersection) | 0.0018** |
| PT | DeepSeek V3 | 0.504 +/- 0.030 | — | — | — | — |
| RU | DeepSeek V3 | 0.472 +/- 0.009 | 0.451 +/- 0.022 | 0.1186 | 0.505 +/- 0.020 (intersection) | 0.0174* |

#### Subnarrative-level F1-samples

| Lang | Model | Baseline | Actor-Critic | p (AC vs BL) | Best Agora (agg) | p (Agora vs BL) |
|------|-------|----------|-------------|--------------|-----------------|----------------|
| BG | DeepSeek V3 | 0.216 +/- 0.001 | 0.204 +/- 0.034 | 0.4770 | 0.230 +/- 0.006 (intersection) | 0.0076** |
| EN | DeepSeek V3 | 0.101 +/- 0.008 | 0.124 +/- 0.025 | 0.1251 | 0.109 +/- 0.012 (intersection) | 0.1236 |
| EN | GPT-5 Nano | 0.145 +/- 0.014 | 0.146 +/- 0.017 | 0.9482 | 0.162 +/- 0.016 (union) | 0.0097** |
| EN | Gemini 2.5 Flash | 0.180 +/- 0.000 | 0.146 +/- 0.026 | — | 0.164 +/- 0.020 (intersection) | — |
| EN | Llama 3.3 70B | 0.081 +/- 0.005 | 0.102 +/- 0.013 | 0.0195* | 0.085 +/- 0.006 (majority) | 0.0197* |
| EN | Mistral Large | 0.084 +/- 0.005 | 0.080 +/- 0.006 | 0.4004 | 0.088 +/- 0.003 (intersection) | 0.2410 |
| PT | DeepSeek V3 | 0.209 +/- 0.028 | — | — | — | — |
| RU | DeepSeek V3 | 0.200 +/- 0.005 | 0.217 +/- 0.041 | 0.4457 | 0.212 +/- 0.018 (intersection) | 0.2352 |

### Actor-Critic vs Baseline: Aggregate Summary

| Level | AC Wins | AC Losses | Ties |
|-------|---------|-----------|------|
| Narrative F1-samples | 7 | 12 | 1 |
| Subnarrative F1-samples | 7 | 10 | 3 |

**Average improvement by model (Actor-Critic minus Baseline):**

| Model | Avg Narr Diff | Avg Sub Diff | N |
|-------|--------------|-------------|---|
| DeepSeek V3 | -0.0495 | -0.0120 | 8 |
| GPT-5 Nano | -0.0127 | -0.0255 | 2 |
| Gemini 2.5 Flash | -0.0202 | -0.0169 | 2 |
| Llama 3.3 70B | +0.0203 | +0.0256 | 2 |
| Mistral Large | -0.0038 | -0.0013 | 6 |

**Average improvement by language (Actor-Critic minus Baseline):**

| Language | Avg Narr Diff | Avg Sub Diff | N |
|----------|--------------|-------------|---|
| BG | -0.0642 | -0.0147 | 3 |
| EN | -0.0017 | +0.0007 | 10 |
| HI | -0.0285 | -0.0276 | 2 |
| PT | -0.0674 | -0.0372 | 2 |
| RU | -0.0141 | +0.0095 | 3 |

## Cross-Method Comparison

Comparing different multi-agent strategies using the same backbone model. Sorted by subnarrative F1-samples (descending).

### DeepSeek V3 | BG | T=0.0

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Agora (intersection) | 5 | 0.380 +/- 0.020 | 0.606 +/- 0.013 | 0.121 +/- 0.009 | 0.237 +/- 0.004 |
| Baseline | 5 | 0.334 +/- 0.016 | 0.575 +/- 0.010 | 0.106 +/- 0.005 | 0.217 +/- 0.006 |
| Actor-Critic | 5 | 0.265 +/- 0.047 | 0.453 +/- 0.039 | 0.104 +/- 0.009 | 0.187 +/- 0.019 |

### DeepSeek V3 | BG | T=0.7

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Agora (intersection) | 5 | 0.368 +/- 0.013 | 0.599 +/- 0.011 | 0.121 +/- 0.005 | 0.230 +/- 0.006 |
| Baseline | 5 | 0.322 +/- 0.016 | 0.565 +/- 0.008 | 0.104 +/- 0.006 | 0.216 +/- 0.001 |
| Actor-Critic | 5 | 0.275 +/- 0.037 | 0.490 +/- 0.049 | 0.114 +/- 0.011 | 0.204 +/- 0.034 |

### DeepSeek V3 | EN | T=0.0

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Actor-Critic | 5 | 0.283 +/- 0.032 | 0.347 +/- 0.020 | 0.105 +/- 0.008 | 0.130 +/- 0.012 |
| Actor-Critic | 1 | 0.290 +/- 0.000 | 0.355 +/- 0.000 | 0.105 +/- 0.000 | 0.118 +/- 0.000 |
| Baseline | 1 | 0.329 +/- 0.000 | 0.355 +/- 0.000 | 0.126 +/- 0.000 | 0.109 +/- 0.000 |
| Agora (intersection) | 5 | 0.282 +/- 0.026 | 0.349 +/- 0.007 | 0.102 +/- 0.006 | 0.105 +/- 0.005 |
| Baseline | 5 | 0.288 +/- 0.009 | 0.342 +/- 0.013 | 0.098 +/- 0.004 | 0.103 +/- 0.008 |

### DeepSeek V3 | EN | T=0.7

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Actor-Critic | 5 | 0.272 +/- 0.036 | 0.343 +/- 0.042 | 0.096 +/- 0.012 | 0.124 +/- 0.025 |
| Agora (intersection) | 5 | 0.290 +/- 0.023 | 0.363 +/- 0.020 | 0.099 +/- 0.006 | 0.109 +/- 0.012 |
| Baseline | 5 | 0.275 +/- 0.018 | 0.329 +/- 0.012 | 0.100 +/- 0.007 | 0.101 +/- 0.008 |

### DeepSeek V3 | HI | T=0.0

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Agora (intersection) | 5 | 0.316 +/- 0.042 | 0.462 +/- 0.011 | 0.125 +/- 0.014 | 0.186 +/- 0.015 |
| Baseline | 5 | 0.316 +/- 0.024 | 0.430 +/- 0.021 | 0.121 +/- 0.003 | 0.184 +/- 0.013 |
| Actor-Critic | 5 | 0.301 +/- 0.031 | 0.388 +/- 0.028 | 0.107 +/- 0.007 | 0.130 +/- 0.009 |

### DeepSeek V3 | PT | T=0.0

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Agora (majority) | 5 | 0.383 +/- 0.035 | 0.548 +/- 0.021 | 0.138 +/- 0.011 | 0.228 +/- 0.015 |
| Agora (union) | 5 | 0.349 +/- 0.013 | 0.546 +/- 0.038 | 0.115 +/- 0.015 | 0.220 +/- 0.024 |
| Baseline | 5 | 0.382 +/- 0.021 | 0.510 +/- 0.020 | 0.125 +/- 0.014 | 0.202 +/- 0.017 |
| Agora (intersection) | 5 | 0.408 +/- 0.029 | 0.476 +/- 0.038 | 0.134 +/- 0.013 | 0.180 +/- 0.024 |
| Actor-Critic | 5 | 0.294 +/- 0.028 | 0.383 +/- 0.055 | 0.132 +/- 0.030 | 0.127 +/- 0.027 |

### DeepSeek V3 | RU | T=0.0

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Agora (intersection) | 5 | 0.269 +/- 0.025 | 0.504 +/- 0.021 | 0.149 +/- 0.009 | 0.215 +/- 0.003 |
| Actor-Critic | 5 | 0.214 +/- 0.024 | 0.454 +/- 0.021 | 0.135 +/- 0.008 | 0.212 +/- 0.015 |
| Baseline | 5 | 0.236 +/- 0.014 | 0.481 +/- 0.018 | 0.137 +/- 0.010 | 0.205 +/- 0.007 |

### DeepSeek V3 | RU | T=0.7

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Actor-Critic | 5 | 0.214 +/- 0.035 | 0.451 +/- 0.022 | 0.132 +/- 0.021 | 0.217 +/- 0.041 |
| Agora (intersection) | 5 | 0.272 +/- 0.020 | 0.505 +/- 0.020 | 0.145 +/- 0.015 | 0.212 +/- 0.018 |
| Baseline | 5 | 0.232 +/- 0.014 | 0.472 +/- 0.009 | 0.130 +/- 0.005 | 0.200 +/- 0.005 |

### Gemini 2.5 Flash | EN | T=0.0

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Agora (intersection) | 3 | 0.215 +/- 0.001 | 0.383 +/- 0.014 | 0.090 +/- 0.003 | 0.152 +/- 0.006 |
| Actor-Critic | 5 | 0.243 +/- 0.023 | 0.334 +/- 0.018 | 0.096 +/- 0.014 | 0.144 +/- 0.020 |
| Baseline | 5 | 0.237 +/- 0.023 | 0.354 +/- 0.012 | 0.097 +/- 0.007 | 0.144 +/- 0.008 |
| Actor-Critic | 5 | 0.231 +/- 0.010 | 0.301 +/- 0.019 | 0.070 +/- 0.029 | 0.067 +/- 0.025 |

### Gemini 2.5 Flash | EN | T=0.7

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Baseline | 1 | 0.235 +/- 0.000 | 0.367 +/- 0.000 | 0.103 +/- 0.000 | 0.180 +/- 0.000 |
| Agora (intersection) | 5 | 0.257 +/- 0.037 | 0.393 +/- 0.037 | 0.108 +/- 0.010 | 0.164 +/- 0.020 |
| Actor-Critic | 4 | 0.262 +/- 0.046 | 0.347 +/- 0.038 | 0.112 +/- 0.020 | 0.146 +/- 0.026 |
| Actor-Critic | 5 | 0.232 +/- 0.012 | 0.310 +/- 0.019 | 0.071 +/- 0.014 | 0.051 +/- 0.013 |

### Mistral Large | BG | T=0.0

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Agora (intersection) | 5 | 0.301 +/- 0.009 | 0.483 +/- 0.012 | 0.085 +/- 0.007 | 0.155 +/- 0.009 |
| Agora (majority) | 5 | 0.280 +/- 0.007 | 0.477 +/- 0.006 | 0.079 +/- 0.002 | 0.147 +/- 0.003 |
| Baseline | 5 | 0.242 +/- 0.011 | 0.469 +/- 0.019 | 0.073 +/- 0.002 | 0.145 +/- 0.007 |
| Actor-Critic | 5 | 0.285 +/- 0.013 | 0.474 +/- 0.020 | 0.080 +/- 0.004 | 0.143 +/- 0.012 |

### Mistral Large | EN | T=0.0

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Agora (intersection) | 5 | 0.247 +/- 0.031 | 0.325 +/- 0.022 | 0.075 +/- 0.008 | 0.092 +/- 0.013 |
| Actor-Critic | 1 | 0.250 +/- 0.000 | 0.299 +/- 0.000 | 0.083 +/- 0.000 | 0.090 +/- 0.000 |
| Agora (majority) | 5 | 0.245 +/- 0.027 | 0.303 +/- 0.021 | 0.077 +/- 0.008 | 0.087 +/- 0.008 |
| Baseline | 5 | 0.240 +/- 0.016 | 0.297 +/- 0.005 | 0.074 +/- 0.004 | 0.086 +/- 0.002 |
| Agora (majority) | 1 | 0.221 +/- 0.000 | 0.292 +/- 0.000 | 0.074 +/- 0.000 | 0.086 +/- 0.000 |
| Agora (intersection) | 1 | 0.207 +/- 0.000 | 0.314 +/- 0.000 | 0.071 +/- 0.000 | 0.085 +/- 0.000 |
| Baseline | 1 | 0.239 +/- 0.000 | 0.289 +/- 0.000 | 0.071 +/- 0.000 | 0.084 +/- 0.000 |
| Agora (union) | 5 | 0.229 +/- 0.017 | 0.276 +/- 0.005 | 0.076 +/- 0.006 | 0.082 +/- 0.004 |
| Actor-Critic | 5 | 0.216 +/- 0.028 | 0.287 +/- 0.012 | 0.069 +/- 0.010 | 0.080 +/- 0.006 |

### Mistral Large | EN | T=0.7

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Agora (intersection) | 5 | 0.229 +/- 0.018 | 0.318 +/- 0.008 | 0.072 +/- 0.005 | 0.088 +/- 0.003 |
| Baseline | 5 | 0.213 +/- 0.025 | 0.286 +/- 0.009 | 0.073 +/- 0.008 | 0.084 +/- 0.005 |
| Agora (majority) | 5 | 0.222 +/- 0.021 | 0.297 +/- 0.014 | 0.071 +/- 0.007 | 0.083 +/- 0.005 |
| Actor-Critic | 5 | 0.212 +/- 0.023 | 0.285 +/- 0.016 | 0.070 +/- 0.009 | 0.080 +/- 0.006 |
| Agora (union) | 5 | 0.238 +/- 0.007 | 0.273 +/- 0.006 | 0.074 +/- 0.006 | 0.079 +/- 0.004 |

### Mistral Large | HI | T=0.0

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Agora (intersection) | 5 | 0.241 +/- 0.031 | 0.348 +/- 0.038 | 0.082 +/- 0.010 | 0.115 +/- 0.015 |
| Agora (majority) | 5 | 0.218 +/- 0.015 | 0.319 +/- 0.009 | 0.077 +/- 0.005 | 0.104 +/- 0.008 |
| Baseline | 5 | 0.210 +/- 0.009 | 0.320 +/- 0.023 | 0.074 +/- 0.002 | 0.100 +/- 0.010 |
| Actor-Critic | 5 | 0.214 +/- 0.029 | 0.306 +/- 0.014 | 0.075 +/- 0.010 | 0.099 +/- 0.007 |

### Mistral Large | PT | T=0.0

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Agora (intersection) | 5 | 0.284 +/- 0.019 | 0.464 +/- 0.044 | 0.091 +/- 0.004 | 0.153 +/- 0.022 |
| Agora (majority) | 5 | 0.260 +/- 0.012 | 0.410 +/- 0.049 | 0.087 +/- 0.003 | 0.135 +/- 0.018 |
| Actor-Critic | 5 | 0.255 +/- 0.009 | 0.374 +/- 0.019 | 0.086 +/- 0.002 | 0.123 +/- 0.010 |
| Baseline | 5 | 0.247 +/- 0.007 | 0.382 +/- 0.036 | 0.082 +/- 0.005 | 0.123 +/- 0.015 |

### Mistral Large | RU | T=0.0

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Agora (intersection) | 5 | 0.198 +/- 0.028 | 0.407 +/- 0.031 | 0.117 +/- 0.008 | 0.148 +/- 0.018 |
| Agora (majority) | 5 | 0.218 +/- 0.009 | 0.409 +/- 0.013 | 0.126 +/- 0.004 | 0.142 +/- 0.007 |
| Actor-Critic | 5 | 0.214 +/- 0.015 | 0.387 +/- 0.017 | 0.134 +/- 0.002 | 0.139 +/- 0.004 |
| Baseline | 5 | 0.208 +/- 0.017 | 0.382 +/- 0.008 | 0.129 +/- 0.005 | 0.135 +/- 0.004 |

### GPT-5 Nano | EN | T=0.0

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Baseline | 5 | 0.288 +/- 0.024 | 0.341 +/- 0.034 | 0.133 +/- 0.007 | 0.167 +/- 0.015 |
| Agora (majority) | 1 | 0.288 +/- 0.000 | 0.339 +/- 0.000 | 0.143 +/- 0.000 | 0.165 +/- 0.000 |
| Agora (union) | 5 | 0.279 +/- 0.010 | 0.309 +/- 0.026 | 0.125 +/- 0.015 | 0.156 +/- 0.016 |
| Actor-Critic | 5 | 0.240 +/- 0.031 | 0.294 +/- 0.018 | 0.093 +/- 0.020 | 0.115 +/- 0.026 |

### GPT-5 Nano | EN | T=0.7

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Agora (union) | 5 | 0.274 +/- 0.014 | 0.318 +/- 0.015 | 0.114 +/- 0.022 | 0.162 +/- 0.016 |
| Agora (majority) | 5 | 0.289 +/- 0.007 | 0.337 +/- 0.019 | 0.116 +/- 0.008 | 0.160 +/- 0.009 |
| Actor-Critic | 5 | 0.278 +/- 0.019 | 0.331 +/- 0.020 | 0.121 +/- 0.013 | 0.146 +/- 0.017 |
| Baseline | 5 | 0.264 +/- 0.013 | 0.308 +/- 0.021 | 0.108 +/- 0.006 | 0.145 +/- 0.014 |

### Llama 3.3 70B | EN | T=0.0

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Actor-Critic | 5 | 0.239 +/- 0.019 | 0.319 +/- 0.010 | 0.084 +/- 0.009 | 0.106 +/- 0.007 |
| Agora (majority) | 5 | 0.250 +/- 0.017 | 0.307 +/- 0.016 | 0.078 +/- 0.006 | 0.086 +/- 0.009 |
| Agora (intersection) | 5 | 0.229 +/- 0.026 | 0.318 +/- 0.015 | 0.067 +/- 0.009 | 0.084 +/- 0.005 |
| Agora (union) | 5 | 0.226 +/- 0.014 | 0.277 +/- 0.009 | 0.071 +/- 0.003 | 0.077 +/- 0.003 |
| Baseline | 5 | 0.219 +/- 0.027 | 0.285 +/- 0.013 | 0.070 +/- 0.008 | 0.076 +/- 0.004 |

### Llama 3.3 70B | EN | T=0.7

| Method | Runs | Narr F1-macro | Narr F1-samples | Subnarr F1-macro | Subnarr F1-samples |
|--------|------|---------------|-----------------|-----------------|--------------------|
| Actor-Critic | 5 | 0.230 +/- 0.020 | 0.307 +/- 0.024 | 0.082 +/- 0.011 | 0.102 +/- 0.013 |
| Agora (majority) | 5 | 0.233 +/- 0.015 | 0.302 +/- 0.014 | 0.072 +/- 0.005 | 0.085 +/- 0.006 |
| Baseline | 5 | 0.237 +/- 0.015 | 0.300 +/- 0.009 | 0.070 +/- 0.008 | 0.081 +/- 0.005 |
| Agora (union) | 5 | 0.220 +/- 0.024 | 0.276 +/- 0.011 | 0.071 +/- 0.007 | 0.079 +/- 0.004 |
| Agora (intersection) | 5 | 0.226 +/- 0.018 | 0.300 +/- 0.021 | 0.060 +/- 0.008 | 0.074 +/- 0.010 |

## Cross-Model Comparison

Comparing the same method across different backbone models. Sorted by subnarrative F1-samples (descending).

### Actor-Critic | BG | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| DeepSeek V3 | 5 | 0.453 +/- 0.039 | 0.187 +/- 0.019 |
| Mistral Large | 5 | 0.474 +/- 0.020 | 0.143 +/- 0.012 |

### Actor-Critic | EN | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| Gemini 2.5 Flash | 5 | 0.334 +/- 0.018 | 0.144 +/- 0.020 |
| DeepSeek V3 | 5 | 0.347 +/- 0.020 | 0.130 +/- 0.012 |
| DeepSeek V3 | 1 | 0.355 +/- 0.000 | 0.118 +/- 0.000 |
| GPT-5 Nano | 5 | 0.294 +/- 0.018 | 0.115 +/- 0.026 |
| Llama 3.3 70B | 5 | 0.319 +/- 0.010 | 0.106 +/- 0.007 |
| Mistral Large | 1 | 0.299 +/- 0.000 | 0.090 +/- 0.000 |
| Mistral Large | 5 | 0.287 +/- 0.012 | 0.080 +/- 0.006 |
| Gemini 2.5 Flash | 5 | 0.301 +/- 0.019 | 0.067 +/- 0.025 |

### Actor-Critic | EN | T=0.7

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| GPT-5 Nano | 5 | 0.331 +/- 0.020 | 0.146 +/- 0.017 |
| Gemini 2.5 Flash | 4 | 0.347 +/- 0.038 | 0.146 +/- 0.026 |
| DeepSeek V3 | 5 | 0.343 +/- 0.042 | 0.124 +/- 0.025 |
| Llama 3.3 70B | 5 | 0.307 +/- 0.024 | 0.102 +/- 0.013 |
| Mistral Large | 5 | 0.285 +/- 0.016 | 0.080 +/- 0.006 |
| Gemini 2.5 Flash | 5 | 0.310 +/- 0.019 | 0.051 +/- 0.013 |

### Actor-Critic | HI | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| DeepSeek V3 | 5 | 0.388 +/- 0.028 | 0.130 +/- 0.009 |
| Mistral Large | 5 | 0.306 +/- 0.014 | 0.099 +/- 0.007 |

### Actor-Critic | PT | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| DeepSeek V3 | 5 | 0.383 +/- 0.055 | 0.127 +/- 0.027 |
| Mistral Large | 5 | 0.374 +/- 0.019 | 0.123 +/- 0.010 |

### Actor-Critic | RU | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| DeepSeek V3 | 5 | 0.454 +/- 0.021 | 0.212 +/- 0.015 |
| Mistral Large | 5 | 0.387 +/- 0.017 | 0.139 +/- 0.004 |

### Agora (intersection) | BG | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| DeepSeek V3 | 5 | 0.606 +/- 0.013 | 0.237 +/- 0.004 |
| Mistral Large | 5 | 0.483 +/- 0.012 | 0.155 +/- 0.009 |

### Agora (intersection) | EN | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| Gemini 2.5 Flash | 3 | 0.383 +/- 0.014 | 0.152 +/- 0.006 |
| DeepSeek V3 | 5 | 0.349 +/- 0.007 | 0.105 +/- 0.005 |
| Mistral Large | 5 | 0.325 +/- 0.022 | 0.092 +/- 0.013 |
| Mistral Large | 1 | 0.314 +/- 0.000 | 0.085 +/- 0.000 |
| Llama 3.3 70B | 5 | 0.318 +/- 0.015 | 0.084 +/- 0.005 |

### Agora (intersection) | EN | T=0.7

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| Gemini 2.5 Flash | 5 | 0.393 +/- 0.037 | 0.164 +/- 0.020 |
| DeepSeek V3 | 5 | 0.363 +/- 0.020 | 0.109 +/- 0.012 |
| Mistral Large | 5 | 0.318 +/- 0.008 | 0.088 +/- 0.003 |
| Llama 3.3 70B | 5 | 0.300 +/- 0.021 | 0.074 +/- 0.010 |

### Agora (intersection) | HI | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| DeepSeek V3 | 5 | 0.462 +/- 0.011 | 0.186 +/- 0.015 |
| Mistral Large | 5 | 0.348 +/- 0.038 | 0.115 +/- 0.015 |

### Agora (intersection) | PT | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| DeepSeek V3 | 5 | 0.476 +/- 0.038 | 0.180 +/- 0.024 |
| Mistral Large | 5 | 0.464 +/- 0.044 | 0.153 +/- 0.022 |

### Agora (intersection) | RU | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| DeepSeek V3 | 5 | 0.504 +/- 0.021 | 0.215 +/- 0.003 |
| Mistral Large | 5 | 0.407 +/- 0.031 | 0.148 +/- 0.018 |

### Agora (majority) | BG | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| GPT-5 Nano | 5 | 0.509 +/- 0.026 | 0.244 +/- 0.017 |
| Mistral Large | 5 | 0.477 +/- 0.006 | 0.147 +/- 0.003 |
| Llama 3.3 70B | 5 | 0.315 +/- 0.019 | 0.114 +/- 0.007 |

### Agora (majority) | EN | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| GPT-5 Nano | 1 | 0.339 +/- 0.000 | 0.165 +/- 0.000 |
| Mistral Large | 5 | 0.303 +/- 0.021 | 0.087 +/- 0.008 |
| Mistral Large | 1 | 0.292 +/- 0.000 | 0.086 +/- 0.000 |
| Llama 3.3 70B | 5 | 0.307 +/- 0.016 | 0.086 +/- 0.009 |

### Agora (majority) | EN | T=0.7

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| GPT-5 Nano | 5 | 0.337 +/- 0.019 | 0.160 +/- 0.009 |
| Llama 3.3 70B | 5 | 0.302 +/- 0.014 | 0.085 +/- 0.006 |
| Mistral Large | 5 | 0.297 +/- 0.014 | 0.083 +/- 0.005 |

### Agora (majority) | HI | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| GPT-5 Nano | 5 | 0.400 +/- 0.027 | 0.191 +/- 0.024 |
| Mistral Large | 5 | 0.319 +/- 0.009 | 0.104 +/- 0.008 |
| Llama 3.3 70B | 5 | 0.228 +/- 0.035 | 0.065 +/- 0.013 |

### Agora (majority) | PT | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| GPT-5 Nano | 5 | 0.584 +/- 0.030 | 0.283 +/- 0.028 |
| DeepSeek V3 | 5 | 0.548 +/- 0.021 | 0.228 +/- 0.015 |
| Mistral Large | 5 | 0.410 +/- 0.049 | 0.135 +/- 0.018 |
| Llama 3.3 70B | 5 | 0.199 +/- 0.010 | 0.074 +/- 0.004 |

### Agora (majority) | RU | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| GPT-5 Nano | 5 | 0.428 +/- 0.041 | 0.225 +/- 0.045 |
| Mistral Large | 5 | 0.409 +/- 0.013 | 0.142 +/- 0.007 |
| Llama 3.3 70B | 5 | 0.363 +/- 0.009 | 0.141 +/- 0.002 |

### Agora (union) | EN | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| GPT-5 Nano | 5 | 0.309 +/- 0.026 | 0.156 +/- 0.016 |
| Mistral Large | 5 | 0.276 +/- 0.005 | 0.082 +/- 0.004 |
| Llama 3.3 70B | 5 | 0.277 +/- 0.009 | 0.077 +/- 0.003 |

### Agora (union) | EN | T=0.7

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| GPT-5 Nano | 5 | 0.318 +/- 0.015 | 0.162 +/- 0.016 |
| Llama 3.3 70B | 5 | 0.276 +/- 0.011 | 0.079 +/- 0.004 |
| Mistral Large | 5 | 0.273 +/- 0.006 | 0.079 +/- 0.004 |

### Baseline | BG | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| DeepSeek V3 | 5 | 0.575 +/- 0.010 | 0.217 +/- 0.006 |
| Mistral Large | 5 | 0.469 +/- 0.019 | 0.145 +/- 0.007 |

### Baseline | EN | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| GPT-5 Nano | 5 | 0.341 +/- 0.034 | 0.167 +/- 0.015 |
| Gemini 2.5 Flash | 5 | 0.354 +/- 0.012 | 0.144 +/- 0.008 |
| DeepSeek V3 | 1 | 0.355 +/- 0.000 | 0.109 +/- 0.000 |
| DeepSeek V3 | 5 | 0.342 +/- 0.013 | 0.103 +/- 0.008 |
| Mistral Large | 5 | 0.297 +/- 0.005 | 0.086 +/- 0.002 |
| Mistral Large | 1 | 0.289 +/- 0.000 | 0.084 +/- 0.000 |
| Llama 3.3 70B | 5 | 0.285 +/- 0.013 | 0.076 +/- 0.004 |

### Baseline | EN | T=0.7

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| Gemini 2.5 Flash | 1 | 0.367 +/- 0.000 | 0.180 +/- 0.000 |
| GPT-5 Nano | 5 | 0.308 +/- 0.021 | 0.145 +/- 0.014 |
| DeepSeek V3 | 5 | 0.329 +/- 0.012 | 0.101 +/- 0.008 |
| Mistral Large | 5 | 0.286 +/- 0.009 | 0.084 +/- 0.005 |
| Llama 3.3 70B | 5 | 0.300 +/- 0.009 | 0.081 +/- 0.005 |

### Baseline | HI | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| DeepSeek V3 | 5 | 0.430 +/- 0.021 | 0.184 +/- 0.013 |
| Mistral Large | 5 | 0.320 +/- 0.023 | 0.100 +/- 0.010 |

### Baseline | PT | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| DeepSeek V3 | 5 | 0.510 +/- 0.020 | 0.202 +/- 0.017 |
| Mistral Large | 5 | 0.382 +/- 0.036 | 0.123 +/- 0.015 |

### Baseline | RU | T=0.0

| Model | Runs | Narr F1-samples | Subnarr F1-samples |
|-------|------|-----------------|--------------------|
| DeepSeek V3 | 5 | 0.481 +/- 0.018 | 0.205 +/- 0.007 |
| Mistral Large | 5 | 0.382 +/- 0.008 | 0.135 +/- 0.004 |

## Pairwise Significance Tests

Paired tests comparing methods within the same language and temperature. We use the Wilcoxon signed-rank test (non-parametric) as the primary test, with the paired t-test for reference. Tests are run on per-run F1-samples scores at the subnarrative level (the primary evaluation metric).

### BG, Temperature=0.0

| Method A | Method B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|----------|----------|--------|--------|------|-----------|--------|-------------|------------|------|
| actor_critic_deepseek_bg_t00 | actor_critic_mistral_bg_t00 | 0.187 | 0.143 | +0.044 | +1.46 | large | 0.0625 | 0.0311 |  |
| actor_critic_deepseek_bg_t00 | agora_deepseek_bg_t00 | 0.187 | 0.237 | -0.050 | -2.42 | large | 0.0625 | 0.0057 |  |
| actor_critic_deepseek_bg_t00 | agora_majority_gpt5nano_bg_t00 | 0.187 | 0.244 | -0.058 | -1.90 | large | 0.0625 | 0.0131 |  |
| actor_critic_deepseek_bg_t00 | agora_majority_mistral_bg_t00 | 0.187 | 0.147 | +0.040 | +1.95 | large | 0.0625 | 0.0122 |  |
| actor_critic_deepseek_bg_t00 | agora_majority_together_llama33_70b_bg_t00 | 0.187 | 0.114 | +0.073 | +3.46 | large | 0.0625 | 0.0015 |  |
| actor_critic_deepseek_bg_t00 | agora_mistral_bg_t00 | 0.187 | 0.155 | +0.032 | +1.77 | large | 0.0625 | 0.0168 |  |
| actor_critic_deepseek_bg_t00 | baseline_deepseek_bg_t00 | 0.187 | 0.217 | -0.030 | -1.30 | large | 0.0625 | 0.0435 |  |
| actor_critic_deepseek_bg_t00 | baseline_mistral_bg_t00 | 0.187 | 0.145 | +0.042 | +2.71 | large | 0.0625 | 0.0037 |  |
| actor_critic_mistral_bg_t00 | agora_deepseek_bg_t00 | 0.143 | 0.237 | -0.094 | -10.07 | large | 0.0625 | 0.0000 |  |
| actor_critic_mistral_bg_t00 | agora_majority_gpt5nano_bg_t00 | 0.143 | 0.244 | -0.102 | -8.35 | large | 0.0625 | 0.0000 |  |
| actor_critic_mistral_bg_t00 | agora_majority_mistral_bg_t00 | 0.143 | 0.147 | -0.004 | -0.41 | small | 0.4375 | 0.4144 |  |
| actor_critic_mistral_bg_t00 | agora_majority_together_llama33_70b_bg_t00 | 0.143 | 0.114 | +0.029 | +2.91 | large | 0.0625 | 0.0029 |  |
| actor_critic_mistral_bg_t00 | agora_mistral_bg_t00 | 0.143 | 0.155 | -0.012 | -0.64 | medium | 0.3125 | 0.2274 |  |
| actor_critic_mistral_bg_t00 | baseline_deepseek_bg_t00 | 0.143 | 0.217 | -0.074 | -6.31 | large | 0.0625 | 0.0001 |  |
| actor_critic_mistral_bg_t00 | baseline_mistral_bg_t00 | 0.143 | 0.145 | -0.002 | -0.13 | negligible | 1.0000 | 0.7802 |  |
| agora_deepseek_bg_t00 | agora_majority_gpt5nano_bg_t00 | 0.237 | 0.244 | -0.007 | -0.52 | medium | 0.4375 | 0.3060 |  |
| agora_deepseek_bg_t00 | agora_majority_mistral_bg_t00 | 0.237 | 0.147 | +0.090 | +28.36 | large | 0.0625 | 0.0000 |  |
| agora_deepseek_bg_t00 | agora_majority_together_llama33_70b_bg_t00 | 0.237 | 0.114 | +0.123 | +30.14 | large | 0.0625 | 0.0000 |  |
| agora_deepseek_bg_t00 | agora_mistral_bg_t00 | 0.237 | 0.155 | +0.082 | +6.76 | large | 0.0625 | 0.0001 |  |
| agora_deepseek_bg_t00 | baseline_deepseek_bg_t00 | 0.237 | 0.217 | +0.020 | +2.69 | large | 0.0625 | 0.0038 |  |
| agora_deepseek_bg_t00 | baseline_mistral_bg_t00 | 0.237 | 0.145 | +0.092 | +12.15 | large | 0.0625 | 0.0000 |  |
| agora_majority_gpt5nano_bg_t00 | agora_majority_mistral_bg_t00 | 0.244 | 0.147 | +0.097 | +5.69 | large | 0.0625 | 0.0002 |  |
| agora_majority_gpt5nano_bg_t00 | agora_majority_together_llama33_70b_bg_t00 | 0.244 | 0.114 | +0.131 | +10.96 | large | 0.0625 | 0.0000 |  |
| agora_majority_gpt5nano_bg_t00 | agora_mistral_bg_t00 | 0.244 | 0.155 | +0.089 | +3.44 | large | 0.0625 | 0.0015 |  |
| agora_majority_gpt5nano_bg_t00 | baseline_deepseek_bg_t00 | 0.244 | 0.217 | +0.028 | +1.63 | large | 0.0625 | 0.0218 |  |
| agora_majority_gpt5nano_bg_t00 | baseline_mistral_bg_t00 | 0.244 | 0.145 | +0.099 | +5.85 | large | 0.0625 | 0.0002 |  |
| agora_majority_mistral_bg_t00 | agora_majority_together_llama33_70b_bg_t00 | 0.147 | 0.114 | +0.034 | +5.26 | large | 0.0625 | 0.0003 |  |
| agora_majority_mistral_bg_t00 | agora_mistral_bg_t00 | 0.147 | 0.155 | -0.008 | -0.84 | large | 0.0625 | 0.1328 |  |
| agora_majority_mistral_bg_t00 | baseline_deepseek_bg_t00 | 0.147 | 0.217 | -0.070 | -9.31 | large | 0.0625 | 0.0000 |  |
| agora_majority_mistral_bg_t00 | baseline_mistral_bg_t00 | 0.147 | 0.145 | +0.002 | +0.25 | small | 0.6250 | 0.6061 |  |
| agora_majority_together_llama33_70b_bg_t00 | agora_mistral_bg_t00 | 0.114 | 0.155 | -0.041 | -2.85 | large | 0.0625 | 0.0031 |  |
| agora_majority_together_llama33_70b_bg_t00 | baseline_deepseek_bg_t00 | 0.114 | 0.217 | -0.103 | -10.43 | large | 0.0625 | 0.0000 |  |
| agora_majority_together_llama33_70b_bg_t00 | baseline_mistral_bg_t00 | 0.114 | 0.145 | -0.031 | -3.59 | large | 0.0625 | 0.0013 |  |
| agora_mistral_bg_t00 | baseline_deepseek_bg_t00 | 0.155 | 0.217 | -0.062 | -4.91 | large | 0.0625 | 0.0004 |  |
| agora_mistral_bg_t00 | baseline_mistral_bg_t00 | 0.155 | 0.145 | +0.010 | +0.76 | medium | 0.1875 | 0.1659 |  |
| baseline_deepseek_bg_t00 | baseline_mistral_bg_t00 | 0.217 | 0.145 | +0.072 | +7.92 | large | 0.0625 | 0.0001 |  |

### BG, Temperature=0.7

| Method A | Method B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|----------|----------|--------|--------|------|-----------|--------|-------------|------------|------|
| actor_critic_deepseek_bg_t07 | agora_deepseek_bg_t07 | 0.204 | 0.230 | -0.026 | -0.72 | medium | 0.1875 | 0.1813 |  |
| actor_critic_deepseek_bg_t07 | baseline_deepseek_bg_t07 | 0.204 | 0.216 | -0.012 | -0.35 | small | 0.6250 | 0.4770 |  |
| agora_deepseek_bg_t07 | baseline_deepseek_bg_t07 | 0.230 | 0.216 | +0.014 | +2.22 | large | 0.0625 | 0.0076 |  |

### EN, Temperature=0.0

| Method A | Method B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|----------|----------|--------|--------|------|-----------|--------|-------------|------------|------|
| actor_critic_deepseek_en_t00 | actor_critic_gemini_en_t00 | 0.130 | 0.144 | -0.014 | -0.58 | medium | 0.3125 | 0.2667 |  |
| actor_critic_deepseek_en_t00 | actor_critic_gemini_en_t00 | 0.130 | 0.067 | +0.063 | +1.91 | large | 0.0625 | 0.0129 |  |
| actor_critic_deepseek_en_t00 | actor_critic_gpt5nano_en_t00 | 0.130 | 0.115 | +0.015 | +0.55 | medium | 0.4375 | 0.2851 |  |
| actor_critic_deepseek_en_t00 | actor_critic_mistral_en_t00 | 0.130 | 0.080 | +0.050 | +2.91 | large | 0.0625 | 0.0029 |  |
| actor_critic_deepseek_en_t00 | actor_critic_together_llama33_70b_en_t00 | 0.130 | 0.106 | +0.025 | +1.38 | large | 0.0625 | 0.0370 |  |
| actor_critic_deepseek_en_t00 | agora_deepseek_en_t00 | 0.130 | 0.105 | +0.025 | +2.47 | large | 0.0625 | 0.0053 |  |
| actor_critic_deepseek_en_t00 | agora_gemini_en_t00 | 0.130 | 0.152 | -0.021 | -0.92 | large | 0.5000 | 0.2522 |  |
| actor_critic_deepseek_en_t00 | agora_majority_mistral_en_t00 | 0.130 | 0.087 | +0.043 | +2.82 | large | 0.0625 | 0.0032 |  |
| actor_critic_deepseek_en_t00 | agora_majority_together_llama33_70b_en_t00 | 0.130 | 0.086 | +0.045 | +4.31 | large | 0.0625 | 0.0006 |  |
| actor_critic_deepseek_en_t00 | agora_mistral_en_t00 | 0.130 | 0.092 | +0.038 | +1.84 | large | 0.0625 | 0.0148 |  |
| actor_critic_deepseek_en_t00 | agora_together_llama33_70b_en_t00 | 0.130 | 0.084 | +0.047 | +5.00 | large | 0.0625 | 0.0004 |  |
| actor_critic_deepseek_en_t00 | agora_union_gpt5nano_en_t00 | 0.130 | 0.156 | -0.026 | -1.24 | large | 0.0625 | 0.0501 |  |
| actor_critic_deepseek_en_t00 | agora_union_mistral_en_t00 | 0.130 | 0.082 | +0.049 | +3.98 | large | 0.0625 | 0.0009 |  |
| actor_critic_deepseek_en_t00 | agora_union_together_llama33_70b_en_t00 | 0.130 | 0.077 | +0.053 | +4.13 | large | 0.0625 | 0.0008 |  |
| actor_critic_deepseek_en_t00 | baseline_deepseek_en_t00 | 0.130 | 0.103 | +0.027 | +1.66 | large | 0.0625 | 0.0207 |  |
| actor_critic_deepseek_en_t00 | baseline_gemini_en_t00 | 0.130 | 0.144 | -0.014 | -0.99 | large | 0.1875 | 0.0907 |  |
| actor_critic_deepseek_en_t00 | baseline_gpt5nano_en_t00 | 0.130 | 0.167 | -0.036 | -3.33 | large | 0.0625 | 0.0017 |  |
| actor_critic_deepseek_en_t00 | baseline_mistral_en_t00 | 0.130 | 0.086 | +0.044 | +3.66 | large | 0.0625 | 0.0012 |  |
| actor_critic_deepseek_en_t00 | baseline_together_llama33_70b_en_t00 | 0.130 | 0.076 | +0.054 | +4.97 | large | 0.0625 | 0.0004 |  |
| actor_critic_gemini_en_t00 | actor_critic_gemini_en_t00 | 0.144 | 0.067 | +0.077 | +3.25 | large | 0.0625 | 0.0019 |  |
| actor_critic_gemini_en_t00 | actor_critic_gpt5nano_en_t00 | 0.144 | 0.115 | +0.029 | +0.74 | medium | 0.3125 | 0.1753 |  |
| actor_critic_gemini_en_t00 | actor_critic_mistral_en_t00 | 0.144 | 0.080 | +0.064 | +2.83 | large | 0.0625 | 0.0032 |  |
| actor_critic_gemini_en_t00 | actor_critic_together_llama33_70b_en_t00 | 0.144 | 0.106 | +0.039 | +1.82 | large | 0.0625 | 0.0151 |  |
| actor_critic_gemini_en_t00 | agora_deepseek_en_t00 | 0.144 | 0.105 | +0.039 | +2.34 | large | 0.0625 | 0.0064 |  |
| actor_critic_gemini_en_t00 | agora_gemini_en_t00 | 0.144 | 0.152 | -0.007 | -0.35 | small | 1.0000 | 0.6094 |  |
| actor_critic_gemini_en_t00 | agora_majority_mistral_en_t00 | 0.144 | 0.087 | +0.057 | +2.08 | large | 0.0625 | 0.0096 |  |
| actor_critic_gemini_en_t00 | agora_majority_together_llama33_70b_en_t00 | 0.144 | 0.086 | +0.059 | +2.70 | large | 0.0625 | 0.0038 |  |
| actor_critic_gemini_en_t00 | agora_mistral_en_t00 | 0.144 | 0.092 | +0.052 | +2.67 | large | 0.0625 | 0.0040 |  |
| actor_critic_gemini_en_t00 | agora_together_llama33_70b_en_t00 | 0.144 | 0.084 | +0.061 | +3.44 | large | 0.0625 | 0.0015 |  |
| actor_critic_gemini_en_t00 | agora_union_gpt5nano_en_t00 | 0.144 | 0.156 | -0.012 | -0.50 | medium | 0.3125 | 0.3241 |  |
| actor_critic_gemini_en_t00 | agora_union_mistral_en_t00 | 0.144 | 0.082 | +0.063 | +2.96 | large | 0.0625 | 0.0027 |  |
| actor_critic_gemini_en_t00 | agora_union_together_llama33_70b_en_t00 | 0.144 | 0.077 | +0.067 | +3.90 | large | 0.0625 | 0.0010 |  |
| actor_critic_gemini_en_t00 | baseline_deepseek_en_t00 | 0.144 | 0.103 | +0.041 | +1.72 | large | 0.1250 | 0.0184 |  |
| actor_critic_gemini_en_t00 | baseline_gemini_en_t00 | 0.144 | 0.144 | +0.001 | +0.03 | negligible | 1.0000 | 0.9552 |  |
| actor_critic_gemini_en_t00 | baseline_gpt5nano_en_t00 | 0.144 | 0.167 | -0.022 | -0.89 | large | 0.1875 | 0.1178 |  |
| actor_critic_gemini_en_t00 | baseline_mistral_en_t00 | 0.144 | 0.086 | +0.058 | +2.80 | large | 0.0625 | 0.0033 |  |
| actor_critic_gemini_en_t00 | baseline_together_llama33_70b_en_t00 | 0.144 | 0.076 | +0.068 | +3.67 | large | 0.0625 | 0.0012 |  |
| actor_critic_gemini_en_t00 | actor_critic_gpt5nano_en_t00 | 0.067 | 0.115 | -0.048 | -0.99 | large | 0.1250 | 0.0904 |  |
| actor_critic_gemini_en_t00 | actor_critic_mistral_en_t00 | 0.067 | 0.080 | -0.013 | -0.61 | medium | 0.3125 | 0.2433 |  |
| actor_critic_gemini_en_t00 | actor_critic_together_llama33_70b_en_t00 | 0.067 | 0.106 | -0.038 | -1.44 | large | 0.0625 | 0.0326 |  |
| actor_critic_gemini_en_t00 | agora_deepseek_en_t00 | 0.067 | 0.105 | -0.038 | -1.40 | large | 0.1250 | 0.0354 |  |
| actor_critic_gemini_en_t00 | agora_gemini_en_t00 | 0.067 | 0.152 | -0.084 | -4.05 | large | 0.2500 | 0.0197 |  |
| actor_critic_gemini_en_t00 | agora_majority_mistral_en_t00 | 0.067 | 0.087 | -0.020 | -0.73 | medium | 0.3125 | 0.1778 |  |
| actor_critic_gemini_en_t00 | agora_majority_together_llama33_70b_en_t00 | 0.067 | 0.086 | -0.018 | -0.78 | medium | 0.1875 | 0.1563 |  |
| actor_critic_gemini_en_t00 | agora_mistral_en_t00 | 0.067 | 0.092 | -0.025 | -0.80 | medium | 0.1250 | 0.1485 |  |
| actor_critic_gemini_en_t00 | agora_together_llama33_70b_en_t00 | 0.067 | 0.084 | -0.016 | -0.60 | medium | 0.3125 | 0.2496 |  |
| actor_critic_gemini_en_t00 | agora_union_gpt5nano_en_t00 | 0.067 | 0.156 | -0.089 | -2.43 | large | 0.0625 | 0.0056 |  |
| actor_critic_gemini_en_t00 | agora_union_mistral_en_t00 | 0.067 | 0.082 | -0.014 | -0.54 | medium | 0.3125 | 0.2914 |  |
| actor_critic_gemini_en_t00 | agora_union_together_llama33_70b_en_t00 | 0.067 | 0.077 | -0.010 | -0.43 | small | 0.4375 | 0.3859 |  |
| actor_critic_gemini_en_t00 | baseline_deepseek_en_t00 | 0.067 | 0.103 | -0.036 | -1.71 | large | 0.0625 | 0.0189 |  |
| actor_critic_gemini_en_t00 | baseline_gemini_en_t00 | 0.067 | 0.144 | -0.077 | -2.41 | large | 0.0625 | 0.0057 |  |
| actor_critic_gemini_en_t00 | baseline_gpt5nano_en_t00 | 0.067 | 0.167 | -0.099 | -2.57 | large | 0.0625 | 0.0045 |  |
| actor_critic_gemini_en_t00 | baseline_mistral_en_t00 | 0.067 | 0.086 | -0.019 | -0.72 | medium | 0.1875 | 0.1823 |  |
| actor_critic_gemini_en_t00 | baseline_together_llama33_70b_en_t00 | 0.067 | 0.076 | -0.009 | -0.37 | small | 0.4375 | 0.4553 |  |
| actor_critic_gpt5nano_en_t00 | actor_critic_mistral_en_t00 | 0.115 | 0.080 | +0.034 | +1.21 | large | 0.1250 | 0.0538 |  |
| actor_critic_gpt5nano_en_t00 | actor_critic_together_llama33_70b_en_t00 | 0.115 | 0.106 | +0.009 | +0.39 | small | 0.6250 | 0.4295 |  |
| actor_critic_gpt5nano_en_t00 | agora_deepseek_en_t00 | 0.115 | 0.105 | +0.010 | +0.38 | small | 0.6250 | 0.4486 |  |
| actor_critic_gpt5nano_en_t00 | agora_gemini_en_t00 | 0.115 | 0.152 | -0.037 | -1.70 | large | 0.2500 | 0.0986 |  |
| actor_critic_gpt5nano_en_t00 | agora_majority_mistral_en_t00 | 0.115 | 0.087 | +0.028 | +1.08 | large | 0.1250 | 0.0731 |  |
| actor_critic_gpt5nano_en_t00 | agora_majority_together_llama33_70b_en_t00 | 0.115 | 0.086 | +0.029 | +0.91 | large | 0.1875 | 0.1113 |  |
| actor_critic_gpt5nano_en_t00 | agora_mistral_en_t00 | 0.115 | 0.092 | +0.023 | +0.85 | large | 0.1875 | 0.1313 |  |
| actor_critic_gpt5nano_en_t00 | agora_together_llama33_70b_en_t00 | 0.115 | 0.084 | +0.031 | +1.18 | large | 0.1250 | 0.0575 |  |
| actor_critic_gpt5nano_en_t00 | agora_union_gpt5nano_en_t00 | 0.115 | 0.156 | -0.041 | -2.31 | large | 0.0625 | 0.0067 |  |
| actor_critic_gpt5nano_en_t00 | agora_union_mistral_en_t00 | 0.115 | 0.082 | +0.033 | +1.21 | large | 0.1250 | 0.0536 |  |
| actor_critic_gpt5nano_en_t00 | agora_union_together_llama33_70b_en_t00 | 0.115 | 0.077 | +0.037 | +1.36 | large | 0.1250 | 0.0380 |  |
| actor_critic_gpt5nano_en_t00 | baseline_deepseek_en_t00 | 0.115 | 0.103 | +0.012 | +0.39 | small | 0.3125 | 0.4278 |  |
| actor_critic_gpt5nano_en_t00 | baseline_gemini_en_t00 | 0.115 | 0.144 | -0.029 | -1.30 | large | 0.0625 | 0.0436 |  |
| actor_critic_gpt5nano_en_t00 | baseline_gpt5nano_en_t00 | 0.115 | 0.167 | -0.052 | -2.04 | large | 0.0625 | 0.0103 |  |
| actor_critic_gpt5nano_en_t00 | baseline_mistral_en_t00 | 0.115 | 0.086 | +0.029 | +1.14 | large | 0.1250 | 0.0626 |  |
| actor_critic_gpt5nano_en_t00 | baseline_together_llama33_70b_en_t00 | 0.115 | 0.076 | +0.039 | +1.38 | large | 0.1250 | 0.0371 |  |
| actor_critic_mistral_en_t00 | actor_critic_together_llama33_70b_en_t00 | 0.080 | 0.106 | -0.025 | -3.16 | large | 0.0625 | 0.0021 |  |
| actor_critic_mistral_en_t00 | agora_deepseek_en_t00 | 0.080 | 0.105 | -0.024 | -2.23 | large | 0.0625 | 0.0076 |  |
| actor_critic_mistral_en_t00 | agora_gemini_en_t00 | 0.080 | 0.152 | -0.071 | -9.98 | large | 0.2500 | 0.0033 |  |
| actor_critic_mistral_en_t00 | agora_majority_mistral_en_t00 | 0.080 | 0.087 | -0.007 | -1.04 | large | 0.1250 | 0.0808 |  |
| actor_critic_mistral_en_t00 | agora_majority_together_llama33_70b_en_t00 | 0.080 | 0.086 | -0.005 | -0.49 | small | 0.4375 | 0.3306 |  |
| actor_critic_mistral_en_t00 | agora_mistral_en_t00 | 0.080 | 0.092 | -0.012 | -0.75 | medium | 0.1250 | 0.1686 |  |
| actor_critic_mistral_en_t00 | agora_together_llama33_70b_en_t00 | 0.080 | 0.084 | -0.003 | -0.28 | small | 0.6250 | 0.5614 |  |
| actor_critic_mistral_en_t00 | agora_union_gpt5nano_en_t00 | 0.080 | 0.156 | -0.076 | -3.85 | large | 0.0625 | 0.0010 |  |
| actor_critic_mistral_en_t00 | agora_union_mistral_en_t00 | 0.080 | 0.082 | -0.001 | -0.15 | negligible | 0.8125 | 0.7506 |  |
| actor_critic_mistral_en_t00 | agora_union_together_llama33_70b_en_t00 | 0.080 | 0.077 | +0.003 | +0.41 | small | 0.4375 | 0.4142 |  |
| actor_critic_mistral_en_t00 | baseline_deepseek_en_t00 | 0.080 | 0.103 | -0.023 | -5.62 | large | 0.0625 | 0.0002 |  |
| actor_critic_mistral_en_t00 | baseline_gemini_en_t00 | 0.080 | 0.144 | -0.063 | -4.75 | large | 0.0625 | 0.0004 |  |
| actor_critic_mistral_en_t00 | baseline_gpt5nano_en_t00 | 0.080 | 0.167 | -0.086 | -4.13 | large | 0.0625 | 0.0008 |  |
| actor_critic_mistral_en_t00 | baseline_mistral_en_t00 | 0.080 | 0.086 | -0.006 | -0.86 | large | 0.1875 | 0.1268 |  |
| actor_critic_mistral_en_t00 | baseline_together_llama33_70b_en_t00 | 0.080 | 0.076 | +0.005 | +0.60 | medium | 0.3125 | 0.2480 |  |
| actor_critic_together_llama33_70b_en_t00 | agora_deepseek_en_t00 | 0.106 | 0.105 | +0.001 | +0.08 | negligible | 0.6250 | 0.8640 |  |
| actor_critic_together_llama33_70b_en_t00 | agora_gemini_en_t00 | 0.106 | 0.152 | -0.046 | -10.24 | large | 0.2500 | 0.0032 |  |
| actor_critic_together_llama33_70b_en_t00 | agora_majority_mistral_en_t00 | 0.106 | 0.087 | +0.018 | +1.79 | large | 0.0625 | 0.0162 |  |
| actor_critic_together_llama33_70b_en_t00 | agora_majority_together_llama33_70b_en_t00 | 0.106 | 0.086 | +0.020 | +1.33 | large | 0.1250 | 0.0410 |  |
| actor_critic_together_llama33_70b_en_t00 | agora_mistral_en_t00 | 0.106 | 0.092 | +0.013 | +1.42 | large | 0.1250 | 0.0337 |  |
| actor_critic_together_llama33_70b_en_t00 | agora_together_llama33_70b_en_t00 | 0.106 | 0.084 | +0.022 | +2.21 | large | 0.0625 | 0.0079 |  |
| actor_critic_together_llama33_70b_en_t00 | agora_union_gpt5nano_en_t00 | 0.106 | 0.156 | -0.051 | -4.12 | large | 0.0625 | 0.0008 |  |
| actor_critic_together_llama33_70b_en_t00 | agora_union_mistral_en_t00 | 0.106 | 0.082 | +0.024 | +2.92 | large | 0.0625 | 0.0028 |  |
| actor_critic_together_llama33_70b_en_t00 | agora_union_together_llama33_70b_en_t00 | 0.106 | 0.077 | +0.028 | +3.63 | large | 0.0625 | 0.0012 |  |
| actor_critic_together_llama33_70b_en_t00 | baseline_deepseek_en_t00 | 0.106 | 0.103 | +0.002 | +0.20 | small | 1.0000 | 0.6728 |  |
| actor_critic_together_llama33_70b_en_t00 | baseline_gemini_en_t00 | 0.106 | 0.144 | -0.038 | -4.87 | large | 0.0625 | 0.0004 |  |
| actor_critic_together_llama33_70b_en_t00 | baseline_gpt5nano_en_t00 | 0.106 | 0.167 | -0.061 | -3.46 | large | 0.0625 | 0.0015 |  |
| actor_critic_together_llama33_70b_en_t00 | baseline_mistral_en_t00 | 0.106 | 0.086 | +0.019 | +3.07 | large | 0.0625 | 0.0024 |  |
| actor_critic_together_llama33_70b_en_t00 | baseline_together_llama33_70b_en_t00 | 0.106 | 0.076 | +0.030 | +2.95 | large | 0.0625 | 0.0027 |  |
| agora_deepseek_en_t00 | agora_gemini_en_t00 | 0.105 | 0.152 | -0.047 | -5.29 | large | 0.2500 | 0.0117 |  |
| agora_deepseek_en_t00 | agora_majority_mistral_en_t00 | 0.105 | 0.087 | +0.018 | +1.40 | large | 0.1250 | 0.0352 |  |
| agora_deepseek_en_t00 | agora_majority_together_llama33_70b_en_t00 | 0.105 | 0.086 | +0.019 | +1.94 | large | 0.0625 | 0.0123 |  |
| agora_deepseek_en_t00 | agora_mistral_en_t00 | 0.105 | 0.092 | +0.012 | +1.03 | large | 0.1250 | 0.0819 |  |
| agora_deepseek_en_t00 | agora_together_llama33_70b_en_t00 | 0.105 | 0.084 | +0.021 | +18.81 | large | 0.0625 | 0.0000 |  |
| agora_deepseek_en_t00 | agora_union_gpt5nano_en_t00 | 0.105 | 0.156 | -0.051 | -3.57 | large | 0.0625 | 0.0013 |  |
| agora_deepseek_en_t00 | agora_union_mistral_en_t00 | 0.105 | 0.082 | +0.023 | +3.47 | large | 0.0625 | 0.0015 |  |
| agora_deepseek_en_t00 | agora_union_together_llama33_70b_en_t00 | 0.105 | 0.077 | +0.027 | +6.61 | large | 0.0625 | 0.0001 |  |
| agora_deepseek_en_t00 | baseline_deepseek_en_t00 | 0.105 | 0.103 | +0.002 | +0.13 | negligible | 0.8125 | 0.7933 |  |
| agora_deepseek_en_t00 | baseline_gemini_en_t00 | 0.105 | 0.144 | -0.039 | -5.77 | large | 0.0625 | 0.0002 |  |
| agora_deepseek_en_t00 | baseline_gpt5nano_en_t00 | 0.105 | 0.167 | -0.062 | -5.01 | large | 0.0625 | 0.0004 |  |
| agora_deepseek_en_t00 | baseline_mistral_en_t00 | 0.105 | 0.086 | +0.019 | +3.47 | large | 0.0625 | 0.0015 |  |
| agora_deepseek_en_t00 | baseline_together_llama33_70b_en_t00 | 0.105 | 0.076 | +0.029 | +5.57 | large | 0.0625 | 0.0002 |  |
| agora_gemini_en_t00 | agora_majority_mistral_en_t00 | 0.152 | 0.087 | +0.064 | +4.56 | large | 0.2500 | 0.0157 |  |
| agora_gemini_en_t00 | agora_majority_together_llama33_70b_en_t00 | 0.152 | 0.086 | +0.066 | +6.97 | large | 0.2500 | 0.0068 |  |
| agora_gemini_en_t00 | agora_mistral_en_t00 | 0.152 | 0.092 | +0.059 | +20.39 | large | 0.2500 | 0.0008 |  |
| agora_gemini_en_t00 | agora_together_llama33_70b_en_t00 | 0.152 | 0.084 | +0.068 | +6.84 | large | 0.2500 | 0.0071 |  |
| agora_gemini_en_t00 | agora_union_gpt5nano_en_t00 | 0.152 | 0.156 | -0.005 | +0.79 | medium | 0.5000 | 0.3028 |  |
| agora_gemini_en_t00 | agora_union_mistral_en_t00 | 0.152 | 0.082 | +0.070 | +13.68 | large | 0.2500 | 0.0018 |  |
| agora_gemini_en_t00 | agora_union_together_llama33_70b_en_t00 | 0.152 | 0.077 | +0.074 | +15.11 | large | 0.2500 | 0.0015 |  |
| agora_gemini_en_t00 | baseline_deepseek_en_t00 | 0.152 | 0.103 | +0.048 | +5.61 | large | 0.2500 | 0.0104 |  |
| agora_gemini_en_t00 | baseline_gemini_en_t00 | 0.152 | 0.144 | +0.008 | +1.65 | large | 0.2500 | 0.1041 |  |
| agora_gemini_en_t00 | baseline_gpt5nano_en_t00 | 0.152 | 0.167 | -0.015 | -0.65 | medium | 0.5000 | 0.3798 |  |
| agora_gemini_en_t00 | baseline_mistral_en_t00 | 0.152 | 0.086 | +0.066 | +10.05 | large | 0.2500 | 0.0033 |  |
| agora_gemini_en_t00 | baseline_together_llama33_70b_en_t00 | 0.152 | 0.076 | +0.076 | +10.63 | large | 0.2500 | 0.0029 |  |
| agora_majority_mistral_en_t00 | agora_majority_together_llama33_70b_en_t00 | 0.087 | 0.086 | +0.002 | +0.16 | negligible | 0.8125 | 0.7386 |  |
| agora_majority_mistral_en_t00 | agora_mistral_en_t00 | 0.087 | 0.092 | -0.005 | -0.29 | small | 0.4375 | 0.5522 |  |
| agora_majority_mistral_en_t00 | agora_together_llama33_70b_en_t00 | 0.087 | 0.084 | +0.004 | +0.30 | small | 0.4375 | 0.5437 |  |
| agora_majority_mistral_en_t00 | agora_union_gpt5nano_en_t00 | 0.087 | 0.156 | -0.069 | -3.41 | large | 0.0625 | 0.0016 |  |
| agora_majority_mistral_en_t00 | agora_union_mistral_en_t00 | 0.087 | 0.082 | +0.006 | +0.74 | medium | 0.1250 | 0.1744 |  |
| agora_majority_mistral_en_t00 | agora_union_together_llama33_70b_en_t00 | 0.087 | 0.077 | +0.010 | +0.91 | large | 0.0625 | 0.1105 |  |
| agora_majority_mistral_en_t00 | baseline_deepseek_en_t00 | 0.087 | 0.103 | -0.016 | -2.30 | large | 0.0625 | 0.0068 |  |
| agora_majority_mistral_en_t00 | baseline_gemini_en_t00 | 0.087 | 0.144 | -0.057 | -4.21 | large | 0.0625 | 0.0007 |  |
| agora_majority_mistral_en_t00 | baseline_gpt5nano_en_t00 | 0.087 | 0.167 | -0.079 | -4.21 | large | 0.0625 | 0.0007 |  |
| agora_majority_mistral_en_t00 | baseline_mistral_en_t00 | 0.087 | 0.086 | +0.001 | +0.15 | negligible | 0.8125 | 0.7544 |  |
| agora_majority_mistral_en_t00 | baseline_together_llama33_70b_en_t00 | 0.087 | 0.076 | +0.011 | +1.14 | large | 0.1250 | 0.0631 |  |
| agora_majority_together_llama33_70b_en_t00 | agora_mistral_en_t00 | 0.086 | 0.092 | -0.007 | -0.34 | small | 0.6250 | 0.4924 |  |
| agora_majority_together_llama33_70b_en_t00 | agora_together_llama33_70b_en_t00 | 0.086 | 0.084 | +0.002 | +0.20 | small | 0.8125 | 0.6736 |  |
| agora_majority_together_llama33_70b_en_t00 | agora_union_gpt5nano_en_t00 | 0.086 | 0.156 | -0.071 | -3.00 | large | 0.0625 | 0.0026 |  |
| agora_majority_together_llama33_70b_en_t00 | agora_union_mistral_en_t00 | 0.086 | 0.082 | +0.004 | +0.44 | small | 0.4375 | 0.3844 |  |
| agora_majority_together_llama33_70b_en_t00 | agora_union_together_llama33_70b_en_t00 | 0.086 | 0.077 | +0.008 | +0.91 | large | 0.1875 | 0.1121 |  |
| agora_majority_together_llama33_70b_en_t00 | baseline_deepseek_en_t00 | 0.086 | 0.103 | -0.018 | -2.12 | large | 0.0625 | 0.0091 |  |
| agora_majority_together_llama33_70b_en_t00 | baseline_gemini_en_t00 | 0.086 | 0.144 | -0.058 | -3.77 | large | 0.0625 | 0.0011 |  |
| agora_majority_together_llama33_70b_en_t00 | baseline_gpt5nano_en_t00 | 0.086 | 0.167 | -0.081 | -4.45 | large | 0.0625 | 0.0006 |  |
| agora_majority_together_llama33_70b_en_t00 | baseline_mistral_en_t00 | 0.086 | 0.086 | -0.001 | -0.07 | negligible | 1.0000 | 0.8878 |  |
| agora_majority_together_llama33_70b_en_t00 | baseline_together_llama33_70b_en_t00 | 0.086 | 0.076 | +0.010 | +1.61 | large | 0.0625 | 0.0228 |  |
| agora_mistral_en_t00 | agora_together_llama33_70b_en_t00 | 0.092 | 0.084 | +0.009 | +0.67 | medium | 0.1875 | 0.2082 |  |
| agora_mistral_en_t00 | agora_union_gpt5nano_en_t00 | 0.092 | 0.156 | -0.064 | -5.83 | large | 0.0625 | 0.0002 |  |
| agora_mistral_en_t00 | agora_union_mistral_en_t00 | 0.092 | 0.082 | +0.011 | +0.88 | large | 0.1875 | 0.1217 |  |
| agora_mistral_en_t00 | agora_union_together_llama33_70b_en_t00 | 0.092 | 0.077 | +0.015 | +1.14 | large | 0.0625 | 0.0629 |  |
| agora_mistral_en_t00 | baseline_deepseek_en_t00 | 0.092 | 0.103 | -0.011 | -0.57 | medium | 0.4375 | 0.2723 |  |
| agora_mistral_en_t00 | baseline_gemini_en_t00 | 0.092 | 0.144 | -0.051 | -6.45 | large | 0.0625 | 0.0001 |  |
| agora_mistral_en_t00 | baseline_gpt5nano_en_t00 | 0.092 | 0.167 | -0.074 | -4.75 | large | 0.0625 | 0.0004 |  |
| agora_mistral_en_t00 | baseline_mistral_en_t00 | 0.092 | 0.086 | +0.006 | +0.50 | medium | 0.4375 | 0.3251 |  |
| agora_mistral_en_t00 | baseline_together_llama33_70b_en_t00 | 0.092 | 0.076 | +0.016 | +1.05 | large | 0.0625 | 0.0779 |  |
| agora_together_llama33_70b_en_t00 | agora_union_gpt5nano_en_t00 | 0.084 | 0.156 | -0.073 | -4.90 | large | 0.0625 | 0.0004 |  |
| agora_together_llama33_70b_en_t00 | agora_union_mistral_en_t00 | 0.084 | 0.082 | +0.002 | +0.29 | small | 0.8125 | 0.5514 |  |
| agora_together_llama33_70b_en_t00 | agora_union_together_llama33_70b_en_t00 | 0.084 | 0.077 | +0.006 | +1.40 | large | 0.0625 | 0.0354 |  |
| agora_together_llama33_70b_en_t00 | baseline_deepseek_en_t00 | 0.084 | 0.103 | -0.020 | -1.66 | large | 0.0625 | 0.0204 |  |
| agora_together_llama33_70b_en_t00 | baseline_gemini_en_t00 | 0.084 | 0.144 | -0.060 | -8.35 | large | 0.0625 | 0.0000 |  |
| agora_together_llama33_70b_en_t00 | baseline_gpt5nano_en_t00 | 0.084 | 0.167 | -0.083 | -6.83 | large | 0.0625 | 0.0001 |  |
| agora_together_llama33_70b_en_t00 | baseline_mistral_en_t00 | 0.084 | 0.086 | -0.003 | -0.47 | small | 0.4375 | 0.3529 |  |
| agora_together_llama33_70b_en_t00 | baseline_together_llama33_70b_en_t00 | 0.084 | 0.076 | +0.008 | +1.59 | large | 0.0625 | 0.0235 |  |
| agora_union_gpt5nano_en_t00 | agora_union_mistral_en_t00 | 0.156 | 0.082 | +0.075 | +4.35 | large | 0.0625 | 0.0006 |  |
| agora_union_gpt5nano_en_t00 | agora_union_together_llama33_70b_en_t00 | 0.156 | 0.077 | +0.079 | +4.98 | large | 0.0625 | 0.0004 |  |
| agora_union_gpt5nano_en_t00 | baseline_deepseek_en_t00 | 0.156 | 0.103 | +0.053 | +2.40 | large | 0.0625 | 0.0058 |  |
| agora_union_gpt5nano_en_t00 | baseline_gemini_en_t00 | 0.156 | 0.144 | +0.012 | +1.35 | large | 0.0625 | 0.0388 |  |
| agora_union_gpt5nano_en_t00 | baseline_gpt5nano_en_t00 | 0.156 | 0.167 | -0.010 | -0.65 | medium | 0.3125 | 0.2195 |  |
| agora_union_gpt5nano_en_t00 | baseline_mistral_en_t00 | 0.156 | 0.086 | +0.070 | +4.63 | large | 0.0625 | 0.0005 |  |
| agora_union_gpt5nano_en_t00 | baseline_together_llama33_70b_en_t00 | 0.156 | 0.076 | +0.080 | +4.43 | large | 0.0625 | 0.0006 |  |
| agora_union_mistral_en_t00 | agora_union_together_llama33_70b_en_t00 | 0.082 | 0.077 | +0.004 | +0.66 | medium | 0.3125 | 0.2151 |  |
| agora_union_mistral_en_t00 | baseline_deepseek_en_t00 | 0.082 | 0.103 | -0.022 | -2.29 | large | 0.0625 | 0.0068 |  |
| agora_union_mistral_en_t00 | baseline_gemini_en_t00 | 0.082 | 0.144 | -0.062 | -7.29 | large | 0.0625 | 0.0001 |  |
| agora_union_mistral_en_t00 | baseline_gpt5nano_en_t00 | 0.082 | 0.167 | -0.085 | -6.08 | large | 0.0625 | 0.0002 |  |
| agora_union_mistral_en_t00 | baseline_mistral_en_t00 | 0.082 | 0.086 | -0.005 | -1.23 | large | 0.0625 | 0.0517 |  |
| agora_union_mistral_en_t00 | baseline_together_llama33_70b_en_t00 | 0.082 | 0.076 | +0.006 | +0.89 | large | 0.3125 | 0.1178 |  |
| agora_union_together_llama33_70b_en_t00 | baseline_deepseek_en_t00 | 0.077 | 0.103 | -0.026 | -3.00 | large | 0.0625 | 0.0026 |  |
| agora_union_together_llama33_70b_en_t00 | baseline_gemini_en_t00 | 0.077 | 0.144 | -0.066 | -7.39 | large | 0.0625 | 0.0001 |  |
| agora_union_together_llama33_70b_en_t00 | baseline_gpt5nano_en_t00 | 0.077 | 0.167 | -0.089 | -5.53 | large | 0.0625 | 0.0002 |  |
| agora_union_together_llama33_70b_en_t00 | baseline_mistral_en_t00 | 0.077 | 0.086 | -0.009 | -2.08 | large | 0.0625 | 0.0096 |  |
| agora_union_together_llama33_70b_en_t00 | baseline_together_llama33_70b_en_t00 | 0.077 | 0.076 | +0.002 | +0.51 | medium | 0.3125 | 0.3175 |  |
| baseline_deepseek_en_t00 | baseline_gemini_en_t00 | 0.103 | 0.144 | -0.040 | -2.59 | large | 0.0625 | 0.0044 |  |
| baseline_deepseek_en_t00 | baseline_gpt5nano_en_t00 | 0.103 | 0.167 | -0.063 | -2.87 | large | 0.0625 | 0.0030 |  |
| baseline_deepseek_en_t00 | baseline_mistral_en_t00 | 0.103 | 0.086 | +0.017 | +2.08 | large | 0.0625 | 0.0097 |  |
| baseline_deepseek_en_t00 | baseline_together_llama33_70b_en_t00 | 0.103 | 0.076 | +0.027 | +3.68 | large | 0.0625 | 0.0012 |  |
| baseline_gemini_en_t00 | baseline_gpt5nano_en_t00 | 0.144 | 0.167 | -0.023 | -2.22 | large | 0.0625 | 0.0077 |  |
| baseline_gemini_en_t00 | baseline_mistral_en_t00 | 0.144 | 0.086 | +0.058 | +7.74 | large | 0.0625 | 0.0001 |  |
| baseline_gemini_en_t00 | baseline_together_llama33_70b_en_t00 | 0.144 | 0.076 | +0.068 | +6.29 | large | 0.0625 | 0.0001 |  |
| baseline_gpt5nano_en_t00 | baseline_mistral_en_t00 | 0.167 | 0.086 | +0.081 | +5.55 | large | 0.0625 | 0.0002 |  |
| baseline_gpt5nano_en_t00 | baseline_together_llama33_70b_en_t00 | 0.167 | 0.076 | +0.091 | +5.57 | large | 0.0625 | 0.0002 |  |
| baseline_mistral_en_t00 | baseline_together_llama33_70b_en_t00 | 0.086 | 0.076 | +0.010 | +2.11 | large | 0.0625 | 0.0091 |  |

### EN, Temperature=0.7

| Method A | Method B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|----------|----------|--------|--------|------|-----------|--------|-------------|------------|------|
| actor_critic_deepseek_en_t07 | actor_critic_gemini_en_t07 | 0.124 | 0.146 | -0.022 | -0.64 | medium | 0.3750 | 0.2915 |  |
| actor_critic_deepseek_en_t07 | actor_critic_gemini_en_t07 | 0.124 | 0.051 | +0.073 | +2.68 | large | 0.0625 | 0.0039 |  |
| actor_critic_deepseek_en_t07 | actor_critic_gpt5nano_en_t07 | 0.124 | 0.146 | -0.022 | -1.20 | large | 0.0625 | 0.0555 |  |
| actor_critic_deepseek_en_t07 | actor_critic_mistral_en_t07 | 0.124 | 0.080 | +0.044 | +1.55 | large | 0.0625 | 0.0255 |  |
| actor_critic_deepseek_en_t07 | actor_critic_together_llama33_70b_en_t07 | 0.124 | 0.102 | +0.022 | +0.76 | medium | 0.1250 | 0.1666 |  |
| actor_critic_deepseek_en_t07 | agora_deepseek_en_t07 | 0.124 | 0.109 | +0.015 | +0.43 | small | 0.6250 | 0.3901 |  |
| actor_critic_deepseek_en_t07 | agora_gemini_en_t07 | 0.124 | 0.164 | -0.040 | -1.12 | large | 0.0625 | 0.0660 |  |
| actor_critic_deepseek_en_t07 | agora_majority_gpt5nano_en_t07 | 0.124 | 0.160 | -0.036 | -1.59 | large | 0.0625 | 0.0238 |  |
| actor_critic_deepseek_en_t07 | agora_majority_mistral_en_t07 | 0.124 | 0.083 | +0.041 | +1.68 | large | 0.0625 | 0.0199 |  |
| actor_critic_deepseek_en_t07 | agora_majority_together_llama33_70b_en_t07 | 0.124 | 0.085 | +0.039 | +1.90 | large | 0.0625 | 0.0132 |  |
| actor_critic_deepseek_en_t07 | agora_mistral_en_t07 | 0.124 | 0.088 | +0.036 | +1.32 | large | 0.0625 | 0.0420 |  |
| actor_critic_deepseek_en_t07 | agora_together_llama33_70b_en_t07 | 0.124 | 0.074 | +0.050 | +1.58 | large | 0.0625 | 0.0239 |  |
| actor_critic_deepseek_en_t07 | agora_union_gpt5nano_en_t07 | 0.124 | 0.162 | -0.038 | -1.10 | large | 0.1250 | 0.0698 |  |
| actor_critic_deepseek_en_t07 | agora_union_mistral_en_t07 | 0.124 | 0.079 | +0.045 | +1.70 | large | 0.0625 | 0.0190 |  |
| actor_critic_deepseek_en_t07 | agora_union_together_llama33_70b_en_t07 | 0.124 | 0.079 | +0.045 | +1.90 | large | 0.0625 | 0.0133 |  |
| actor_critic_deepseek_en_t07 | baseline_deepseek_en_t07 | 0.124 | 0.101 | +0.023 | +0.87 | large | 0.1875 | 0.1251 |  |
| actor_critic_deepseek_en_t07 | baseline_gpt5nano_en_t07 | 0.124 | 0.145 | -0.021 | -0.72 | medium | 0.1875 | 0.1816 |  |
| actor_critic_deepseek_en_t07 | baseline_mistral_en_t07 | 0.124 | 0.084 | +0.040 | +1.43 | large | 0.0625 | 0.0331 |  |
| actor_critic_deepseek_en_t07 | baseline_together_llama33_70b_en_t07 | 0.124 | 0.081 | +0.043 | +2.08 | large | 0.0625 | 0.0096 |  |
| actor_critic_gemini_en_t07 | actor_critic_gemini_en_t07 | 0.146 | 0.051 | +0.095 | +4.81 | large | 0.1250 | 0.0024 |  |
| actor_critic_gemini_en_t07 | actor_critic_gpt5nano_en_t07 | 0.146 | 0.146 | -0.000 | -0.23 | small | 0.8750 | 0.6796 |  |
| actor_critic_gemini_en_t07 | actor_critic_mistral_en_t07 | 0.146 | 0.080 | +0.065 | +2.75 | large | 0.1250 | 0.0118 |  |
| actor_critic_gemini_en_t07 | actor_critic_together_llama33_70b_en_t07 | 0.146 | 0.102 | +0.043 | +1.36 | large | 0.1250 | 0.0725 |  |
| actor_critic_gemini_en_t07 | agora_deepseek_en_t07 | 0.146 | 0.109 | +0.037 | +1.21 | large | 0.2500 | 0.0935 |  |
| actor_critic_gemini_en_t07 | agora_gemini_en_t07 | 0.146 | 0.164 | -0.018 | -0.68 | medium | 0.6250 | 0.2692 |  |
| actor_critic_gemini_en_t07 | agora_majority_gpt5nano_en_t07 | 0.146 | 0.160 | -0.014 | -0.48 | small | 0.6250 | 0.4119 |  |
| actor_critic_gemini_en_t07 | agora_majority_mistral_en_t07 | 0.146 | 0.083 | +0.062 | +2.14 | large | 0.1250 | 0.0236 |  |
| actor_critic_gemini_en_t07 | agora_majority_together_llama33_70b_en_t07 | 0.146 | 0.085 | +0.061 | +2.27 | large | 0.1250 | 0.0200 |  |
| actor_critic_gemini_en_t07 | agora_mistral_en_t07 | 0.146 | 0.088 | +0.058 | +2.38 | large | 0.1250 | 0.0177 |  |
| actor_critic_gemini_en_t07 | agora_together_llama33_70b_en_t07 | 0.146 | 0.074 | +0.072 | +2.20 | large | 0.1250 | 0.0216 |  |
| actor_critic_gemini_en_t07 | agora_union_gpt5nano_en_t07 | 0.146 | 0.162 | -0.017 | -0.44 | small | 0.6250 | 0.4409 |  |
| actor_critic_gemini_en_t07 | agora_union_mistral_en_t07 | 0.146 | 0.079 | +0.067 | +2.48 | large | 0.1250 | 0.0157 |  |
| actor_critic_gemini_en_t07 | agora_union_together_llama33_70b_en_t07 | 0.146 | 0.079 | +0.067 | +2.67 | large | 0.1250 | 0.0128 |  |
| actor_critic_gemini_en_t07 | baseline_deepseek_en_t07 | 0.146 | 0.101 | +0.045 | +1.52 | large | 0.1250 | 0.0556 |  |
| actor_critic_gemini_en_t07 | baseline_gpt5nano_en_t07 | 0.146 | 0.145 | +0.000 | -0.08 | negligible | 0.8750 | 0.8826 |  |
| actor_critic_gemini_en_t07 | baseline_mistral_en_t07 | 0.146 | 0.084 | +0.062 | +2.05 | large | 0.1250 | 0.0263 |  |
| actor_critic_gemini_en_t07 | baseline_together_llama33_70b_en_t07 | 0.146 | 0.081 | +0.065 | +2.57 | large | 0.1250 | 0.0143 |  |
| actor_critic_gemini_en_t07 | actor_critic_gpt5nano_en_t07 | 0.051 | 0.146 | -0.095 | -4.11 | large | 0.0625 | 0.0008 |  |
| actor_critic_gemini_en_t07 | actor_critic_mistral_en_t07 | 0.051 | 0.080 | -0.030 | -2.47 | large | 0.0625 | 0.0052 |  |
| actor_critic_gemini_en_t07 | actor_critic_together_llama33_70b_en_t07 | 0.051 | 0.102 | -0.052 | -2.75 | large | 0.0625 | 0.0035 |  |
| actor_critic_gemini_en_t07 | agora_deepseek_en_t07 | 0.051 | 0.109 | -0.058 | -4.31 | large | 0.0625 | 0.0007 |  |
| actor_critic_gemini_en_t07 | agora_gemini_en_t07 | 0.051 | 0.164 | -0.113 | -10.94 | large | 0.0625 | 0.0000 |  |
| actor_critic_gemini_en_t07 | agora_majority_gpt5nano_en_t07 | 0.051 | 0.160 | -0.109 | -6.68 | large | 0.0625 | 0.0001 |  |
| actor_critic_gemini_en_t07 | agora_majority_mistral_en_t07 | 0.051 | 0.083 | -0.032 | -2.20 | large | 0.0625 | 0.0080 |  |
| actor_critic_gemini_en_t07 | agora_majority_together_llama33_70b_en_t07 | 0.051 | 0.085 | -0.034 | -2.59 | large | 0.0625 | 0.0044 |  |
| actor_critic_gemini_en_t07 | agora_mistral_en_t07 | 0.051 | 0.088 | -0.037 | -3.14 | large | 0.0625 | 0.0022 |  |
| actor_critic_gemini_en_t07 | agora_together_llama33_70b_en_t07 | 0.051 | 0.074 | -0.023 | -1.09 | large | 0.0625 | 0.0722 |  |
| actor_critic_gemini_en_t07 | agora_union_gpt5nano_en_t07 | 0.051 | 0.162 | -0.112 | -4.54 | large | 0.0625 | 0.0005 |  |
| actor_critic_gemini_en_t07 | agora_union_mistral_en_t07 | 0.051 | 0.079 | -0.028 | -1.92 | large | 0.0625 | 0.0128 |  |
| actor_critic_gemini_en_t07 | agora_union_together_llama33_70b_en_t07 | 0.051 | 0.079 | -0.028 | -1.91 | large | 0.0625 | 0.0130 |  |
| actor_critic_gemini_en_t07 | baseline_deepseek_en_t07 | 0.051 | 0.101 | -0.050 | -4.53 | large | 0.0625 | 0.0005 |  |
| actor_critic_gemini_en_t07 | baseline_gpt5nano_en_t07 | 0.051 | 0.145 | -0.095 | -3.83 | large | 0.0625 | 0.0010 |  |
| actor_critic_gemini_en_t07 | baseline_mistral_en_t07 | 0.051 | 0.084 | -0.033 | -1.87 | large | 0.0625 | 0.0139 |  |
| actor_critic_gemini_en_t07 | baseline_together_llama33_70b_en_t07 | 0.051 | 0.081 | -0.030 | -2.24 | large | 0.0625 | 0.0074 |  |
| actor_critic_gpt5nano_en_t07 | actor_critic_mistral_en_t07 | 0.146 | 0.080 | +0.066 | +3.32 | large | 0.0625 | 0.0018 |  |
| actor_critic_gpt5nano_en_t07 | actor_critic_together_llama33_70b_en_t07 | 0.146 | 0.102 | +0.044 | +1.69 | large | 0.0625 | 0.0193 |  |
| actor_critic_gpt5nano_en_t07 | agora_deepseek_en_t07 | 0.146 | 0.109 | +0.037 | +1.32 | large | 0.0625 | 0.0420 |  |
| actor_critic_gpt5nano_en_t07 | agora_gemini_en_t07 | 0.146 | 0.164 | -0.018 | -0.63 | medium | 0.3125 | 0.2320 |  |
| actor_critic_gpt5nano_en_t07 | agora_majority_gpt5nano_en_t07 | 0.146 | 0.160 | -0.014 | -0.72 | medium | 0.3125 | 0.1834 |  |
| actor_critic_gpt5nano_en_t07 | agora_majority_mistral_en_t07 | 0.146 | 0.083 | +0.063 | +3.35 | large | 0.0625 | 0.0017 |  |
| actor_critic_gpt5nano_en_t07 | agora_majority_together_llama33_70b_en_t07 | 0.146 | 0.085 | +0.061 | +3.66 | large | 0.0625 | 0.0012 |  |
| actor_critic_gpt5nano_en_t07 | agora_mistral_en_t07 | 0.146 | 0.088 | +0.058 | +3.31 | large | 0.0625 | 0.0018 |  |
| actor_critic_gpt5nano_en_t07 | agora_together_llama33_70b_en_t07 | 0.146 | 0.074 | +0.072 | +3.42 | large | 0.0625 | 0.0016 |  |
| actor_critic_gpt5nano_en_t07 | agora_union_gpt5nano_en_t07 | 0.146 | 0.162 | -0.016 | -0.54 | medium | 0.4375 | 0.2949 |  |
| actor_critic_gpt5nano_en_t07 | agora_union_mistral_en_t07 | 0.146 | 0.079 | +0.067 | +3.65 | large | 0.0625 | 0.0012 |  |
| actor_critic_gpt5nano_en_t07 | agora_union_together_llama33_70b_en_t07 | 0.146 | 0.079 | +0.067 | +4.52 | large | 0.0625 | 0.0005 |  |
| actor_critic_gpt5nano_en_t07 | baseline_deepseek_en_t07 | 0.146 | 0.101 | +0.045 | +2.15 | large | 0.0625 | 0.0085 |  |
| actor_critic_gpt5nano_en_t07 | baseline_gpt5nano_en_t07 | 0.146 | 0.145 | +0.001 | +0.03 | negligible | 0.8125 | 0.9482 |  |
| actor_critic_gpt5nano_en_t07 | baseline_mistral_en_t07 | 0.146 | 0.084 | +0.062 | +3.68 | large | 0.0625 | 0.0012 |  |
| actor_critic_gpt5nano_en_t07 | baseline_together_llama33_70b_en_t07 | 0.146 | 0.081 | +0.065 | +4.41 | large | 0.0625 | 0.0006 |  |
| actor_critic_mistral_en_t07 | actor_critic_together_llama33_70b_en_t07 | 0.080 | 0.102 | -0.022 | -2.02 | large | 0.0625 | 0.0106 |  |
| actor_critic_mistral_en_t07 | agora_deepseek_en_t07 | 0.080 | 0.109 | -0.029 | -2.56 | large | 0.0625 | 0.0046 |  |
| actor_critic_mistral_en_t07 | agora_gemini_en_t07 | 0.080 | 0.164 | -0.083 | -4.58 | large | 0.0625 | 0.0005 |  |
| actor_critic_mistral_en_t07 | agora_majority_gpt5nano_en_t07 | 0.080 | 0.160 | -0.080 | -6.06 | large | 0.0625 | 0.0002 |  |
| actor_critic_mistral_en_t07 | agora_majority_mistral_en_t07 | 0.080 | 0.083 | -0.003 | -0.37 | small | 0.6250 | 0.4588 |  |
| actor_critic_mistral_en_t07 | agora_majority_together_llama33_70b_en_t07 | 0.080 | 0.085 | -0.005 | -0.50 | small | 0.6250 | 0.3281 |  |
| actor_critic_mistral_en_t07 | agora_mistral_en_t07 | 0.080 | 0.088 | -0.008 | -1.89 | large | 0.0625 | 0.0134 |  |
| actor_critic_mistral_en_t07 | agora_together_llama33_70b_en_t07 | 0.080 | 0.074 | +0.006 | +0.64 | medium | 0.3125 | 0.2244 |  |
| actor_critic_mistral_en_t07 | agora_union_gpt5nano_en_t07 | 0.080 | 0.162 | -0.082 | -5.23 | large | 0.0625 | 0.0003 |  |
| actor_critic_mistral_en_t07 | agora_union_mistral_en_t07 | 0.080 | 0.079 | +0.002 | +0.36 | small | 0.4375 | 0.4604 |  |
| actor_critic_mistral_en_t07 | agora_union_together_llama33_70b_en_t07 | 0.080 | 0.079 | +0.001 | +0.20 | small | 1.0000 | 0.6763 |  |
| actor_critic_mistral_en_t07 | baseline_deepseek_en_t07 | 0.080 | 0.101 | -0.020 | -1.75 | large | 0.0625 | 0.0174 |  |
| actor_critic_mistral_en_t07 | baseline_gpt5nano_en_t07 | 0.080 | 0.145 | -0.065 | -4.07 | large | 0.0625 | 0.0008 |  |
| actor_critic_mistral_en_t07 | baseline_mistral_en_t07 | 0.080 | 0.084 | -0.004 | -0.42 | small | 0.4375 | 0.4004 |  |
| actor_critic_mistral_en_t07 | baseline_together_llama33_70b_en_t07 | 0.080 | 0.081 | -0.001 | -0.07 | negligible | 0.8125 | 0.8784 |  |
| actor_critic_together_llama33_70b_en_t07 | agora_deepseek_en_t07 | 0.102 | 0.109 | -0.007 | -0.44 | small | 0.4375 | 0.3814 |  |
| actor_critic_together_llama33_70b_en_t07 | agora_gemini_en_t07 | 0.102 | 0.164 | -0.061 | -2.27 | large | 0.0625 | 0.0071 |  |
| actor_critic_together_llama33_70b_en_t07 | agora_majority_gpt5nano_en_t07 | 0.102 | 0.160 | -0.057 | -4.00 | large | 0.0625 | 0.0009 |  |
| actor_critic_together_llama33_70b_en_t07 | agora_majority_mistral_en_t07 | 0.102 | 0.083 | +0.019 | +2.01 | large | 0.0625 | 0.0108 |  |
| actor_critic_together_llama33_70b_en_t07 | agora_majority_together_llama33_70b_en_t07 | 0.102 | 0.085 | +0.017 | +1.46 | large | 0.0625 | 0.0307 |  |
| actor_critic_together_llama33_70b_en_t07 | agora_mistral_en_t07 | 0.102 | 0.088 | +0.015 | +1.05 | large | 0.0625 | 0.0792 |  |
| actor_critic_together_llama33_70b_en_t07 | agora_together_llama33_70b_en_t07 | 0.102 | 0.074 | +0.028 | +2.25 | large | 0.0625 | 0.0073 |  |
| actor_critic_together_llama33_70b_en_t07 | agora_union_gpt5nano_en_t07 | 0.102 | 0.162 | -0.060 | -6.28 | large | 0.0625 | 0.0001 |  |
| actor_critic_together_llama33_70b_en_t07 | agora_union_mistral_en_t07 | 0.102 | 0.079 | +0.024 | +2.41 | large | 0.0625 | 0.0057 |  |
| actor_critic_together_llama33_70b_en_t07 | agora_union_together_llama33_70b_en_t07 | 0.102 | 0.079 | +0.023 | +1.92 | large | 0.0625 | 0.0127 |  |
| actor_critic_together_llama33_70b_en_t07 | baseline_deepseek_en_t07 | 0.102 | 0.101 | +0.002 | +0.10 | negligible | 1.0000 | 0.8369 |  |
| actor_critic_together_llama33_70b_en_t07 | baseline_gpt5nano_en_t07 | 0.102 | 0.145 | -0.043 | -3.55 | large | 0.0625 | 0.0014 |  |
| actor_critic_together_llama33_70b_en_t07 | baseline_mistral_en_t07 | 0.102 | 0.084 | +0.018 | +1.26 | large | 0.0625 | 0.0478 |  |
| actor_critic_together_llama33_70b_en_t07 | baseline_together_llama33_70b_en_t07 | 0.102 | 0.081 | +0.021 | +1.69 | large | 0.0625 | 0.0195 |  |
| agora_deepseek_en_t07 | agora_gemini_en_t07 | 0.109 | 0.164 | -0.055 | -2.89 | large | 0.0625 | 0.0030 |  |
| agora_deepseek_en_t07 | agora_majority_gpt5nano_en_t07 | 0.109 | 0.160 | -0.051 | -3.59 | large | 0.0625 | 0.0013 |  |
| agora_deepseek_en_t07 | agora_majority_mistral_en_t07 | 0.109 | 0.083 | +0.026 | +2.13 | large | 0.0625 | 0.0089 |  |
| agora_deepseek_en_t07 | agora_majority_together_llama33_70b_en_t07 | 0.109 | 0.085 | +0.024 | +1.66 | large | 0.0625 | 0.0208 |  |
| agora_deepseek_en_t07 | agora_mistral_en_t07 | 0.109 | 0.088 | +0.021 | +1.87 | large | 0.0625 | 0.0138 |  |
| agora_deepseek_en_t07 | agora_together_llama33_70b_en_t07 | 0.109 | 0.074 | +0.035 | +2.25 | large | 0.0625 | 0.0074 |  |
| agora_deepseek_en_t07 | agora_union_gpt5nano_en_t07 | 0.109 | 0.162 | -0.053 | -3.49 | large | 0.0625 | 0.0015 |  |
| agora_deepseek_en_t07 | agora_union_mistral_en_t07 | 0.109 | 0.079 | +0.030 | +2.50 | large | 0.0625 | 0.0050 |  |
| agora_deepseek_en_t07 | agora_union_together_llama33_70b_en_t07 | 0.109 | 0.079 | +0.030 | +2.02 | large | 0.0625 | 0.0107 |  |
| agora_deepseek_en_t07 | baseline_deepseek_en_t07 | 0.109 | 0.101 | +0.008 | +0.87 | large | 0.1875 | 0.1236 |  |
| agora_deepseek_en_t07 | baseline_gpt5nano_en_t07 | 0.109 | 0.145 | -0.036 | -2.08 | large | 0.0625 | 0.0097 |  |
| agora_deepseek_en_t07 | baseline_mistral_en_t07 | 0.109 | 0.084 | +0.025 | +1.81 | large | 0.0625 | 0.0155 |  |
| agora_deepseek_en_t07 | baseline_together_llama33_70b_en_t07 | 0.109 | 0.081 | +0.028 | +1.86 | large | 0.0625 | 0.0142 |  |
| agora_gemini_en_t07 | agora_majority_gpt5nano_en_t07 | 0.164 | 0.160 | +0.004 | +0.15 | negligible | 0.8125 | 0.7541 |  |
| agora_gemini_en_t07 | agora_majority_mistral_en_t07 | 0.164 | 0.083 | +0.081 | +3.46 | large | 0.0625 | 0.0015 |  |
| agora_gemini_en_t07 | agora_majority_together_llama33_70b_en_t07 | 0.164 | 0.085 | +0.079 | +3.51 | large | 0.0625 | 0.0014 |  |
| agora_gemini_en_t07 | agora_mistral_en_t07 | 0.164 | 0.088 | +0.076 | +4.30 | large | 0.0625 | 0.0007 |  |
| agora_gemini_en_t07 | agora_together_llama33_70b_en_t07 | 0.164 | 0.074 | +0.090 | +3.32 | large | 0.0625 | 0.0018 |  |
| agora_gemini_en_t07 | agora_union_gpt5nano_en_t07 | 0.164 | 0.162 | +0.001 | +0.05 | negligible | 0.8125 | 0.9223 |  |
| agora_gemini_en_t07 | agora_union_mistral_en_t07 | 0.164 | 0.079 | +0.085 | +3.90 | large | 0.0625 | 0.0010 |  |
| agora_gemini_en_t07 | agora_union_together_llama33_70b_en_t07 | 0.164 | 0.079 | +0.085 | +3.84 | large | 0.0625 | 0.0010 |  |
| agora_gemini_en_t07 | baseline_deepseek_en_t07 | 0.164 | 0.101 | +0.063 | +3.40 | large | 0.0625 | 0.0016 |  |
| agora_gemini_en_t07 | baseline_gpt5nano_en_t07 | 0.164 | 0.145 | +0.018 | +0.56 | medium | 0.3125 | 0.2770 |  |
| agora_gemini_en_t07 | baseline_mistral_en_t07 | 0.164 | 0.084 | +0.080 | +3.38 | large | 0.0625 | 0.0016 |  |
| agora_gemini_en_t07 | baseline_together_llama33_70b_en_t07 | 0.164 | 0.081 | +0.083 | +3.76 | large | 0.0625 | 0.0011 |  |
| agora_majority_gpt5nano_en_t07 | agora_majority_mistral_en_t07 | 0.160 | 0.083 | +0.077 | +12.29 | large | 0.0625 | 0.0000 |  |
| agora_majority_gpt5nano_en_t07 | agora_majority_together_llama33_70b_en_t07 | 0.160 | 0.085 | +0.075 | +12.77 | large | 0.0625 | 0.0000 |  |
| agora_majority_gpt5nano_en_t07 | agora_mistral_en_t07 | 0.160 | 0.088 | +0.072 | +6.12 | large | 0.0625 | 0.0002 |  |
| agora_majority_gpt5nano_en_t07 | agora_together_llama33_70b_en_t07 | 0.160 | 0.074 | +0.086 | +5.68 | large | 0.0625 | 0.0002 |  |
| agora_majority_gpt5nano_en_t07 | agora_union_gpt5nano_en_t07 | 0.160 | 0.162 | -0.002 | -0.14 | negligible | 0.6250 | 0.7646 |  |
| agora_majority_gpt5nano_en_t07 | agora_union_mistral_en_t07 | 0.160 | 0.079 | +0.081 | +7.87 | large | 0.0625 | 0.0001 |  |
| agora_majority_gpt5nano_en_t07 | agora_union_together_llama33_70b_en_t07 | 0.160 | 0.079 | +0.081 | +8.11 | large | 0.0625 | 0.0001 |  |
| agora_majority_gpt5nano_en_t07 | baseline_deepseek_en_t07 | 0.160 | 0.101 | +0.059 | +7.40 | large | 0.0625 | 0.0001 |  |
| agora_majority_gpt5nano_en_t07 | baseline_gpt5nano_en_t07 | 0.160 | 0.145 | +0.015 | +1.26 | large | 0.0625 | 0.0479 |  |
| agora_majority_gpt5nano_en_t07 | baseline_mistral_en_t07 | 0.160 | 0.084 | +0.076 | +6.88 | large | 0.0625 | 0.0001 |  |
| agora_majority_gpt5nano_en_t07 | baseline_together_llama33_70b_en_t07 | 0.160 | 0.081 | +0.079 | +10.95 | large | 0.0625 | 0.0000 |  |
| agora_majority_mistral_en_t07 | agora_majority_together_llama33_70b_en_t07 | 0.083 | 0.085 | -0.002 | -0.43 | small | 0.4375 | 0.3892 |  |
| agora_majority_mistral_en_t07 | agora_mistral_en_t07 | 0.083 | 0.088 | -0.005 | -0.63 | medium | 0.3125 | 0.2341 |  |
| agora_majority_mistral_en_t07 | agora_together_llama33_70b_en_t07 | 0.083 | 0.074 | +0.009 | +0.90 | large | 0.1250 | 0.1151 |  |
| agora_majority_mistral_en_t07 | agora_union_gpt5nano_en_t07 | 0.083 | 0.162 | -0.079 | -6.11 | large | 0.0625 | 0.0002 |  |
| agora_majority_mistral_en_t07 | agora_union_mistral_en_t07 | 0.083 | 0.079 | +0.004 | +0.99 | large | 0.1250 | 0.0916 |  |
| agora_majority_mistral_en_t07 | agora_union_together_llama33_70b_en_t07 | 0.083 | 0.079 | +0.004 | +0.77 | medium | 0.3125 | 0.1610 |  |
| agora_majority_mistral_en_t07 | baseline_deepseek_en_t07 | 0.083 | 0.101 | -0.018 | -1.87 | large | 0.0625 | 0.0139 |  |
| agora_majority_mistral_en_t07 | baseline_gpt5nano_en_t07 | 0.083 | 0.145 | -0.062 | -6.05 | large | 0.0625 | 0.0002 |  |
| agora_majority_mistral_en_t07 | baseline_mistral_en_t07 | 0.083 | 0.084 | -0.001 | -0.10 | negligible | 1.0000 | 0.8262 |  |
| agora_majority_mistral_en_t07 | baseline_together_llama33_70b_en_t07 | 0.083 | 0.081 | +0.002 | +0.46 | small | 0.6250 | 0.3623 |  |
| agora_majority_together_llama33_70b_en_t07 | agora_mistral_en_t07 | 0.085 | 0.088 | -0.003 | -0.32 | small | 0.8125 | 0.5086 |  |
| agora_majority_together_llama33_70b_en_t07 | agora_together_llama33_70b_en_t07 | 0.085 | 0.074 | +0.011 | +0.80 | medium | 0.1250 | 0.1492 |  |
| agora_majority_together_llama33_70b_en_t07 | agora_union_gpt5nano_en_t07 | 0.085 | 0.162 | -0.077 | -4.59 | large | 0.0625 | 0.0005 |  |
| agora_majority_together_llama33_70b_en_t07 | agora_union_mistral_en_t07 | 0.085 | 0.079 | +0.006 | +0.85 | large | 0.1875 | 0.1298 |  |
| agora_majority_together_llama33_70b_en_t07 | agora_union_together_llama33_70b_en_t07 | 0.085 | 0.079 | +0.006 | +0.96 | large | 0.1250 | 0.0987 |  |
| agora_majority_together_llama33_70b_en_t07 | baseline_deepseek_en_t07 | 0.085 | 0.101 | -0.016 | -1.71 | large | 0.0625 | 0.0188 |  |
| agora_majority_together_llama33_70b_en_t07 | baseline_gpt5nano_en_t07 | 0.085 | 0.145 | -0.060 | -4.45 | large | 0.0625 | 0.0006 |  |
| agora_majority_together_llama33_70b_en_t07 | baseline_mistral_en_t07 | 0.085 | 0.084 | +0.001 | +0.11 | negligible | 0.8125 | 0.8245 |  |
| agora_majority_together_llama33_70b_en_t07 | baseline_together_llama33_70b_en_t07 | 0.085 | 0.081 | +0.004 | +1.68 | large | 0.0625 | 0.0197 |  |
| agora_mistral_en_t07 | agora_together_llama33_70b_en_t07 | 0.088 | 0.074 | +0.014 | +1.35 | large | 0.0625 | 0.0388 |  |
| agora_mistral_en_t07 | agora_union_gpt5nano_en_t07 | 0.088 | 0.162 | -0.074 | -4.28 | large | 0.0625 | 0.0007 |  |
| agora_mistral_en_t07 | agora_union_mistral_en_t07 | 0.088 | 0.079 | +0.009 | +1.87 | large | 0.0625 | 0.0139 |  |
| agora_mistral_en_t07 | agora_union_together_llama33_70b_en_t07 | 0.088 | 0.079 | +0.009 | +1.64 | large | 0.0625 | 0.0216 |  |
| agora_mistral_en_t07 | baseline_deepseek_en_t07 | 0.088 | 0.101 | -0.013 | -1.36 | large | 0.0625 | 0.0382 |  |
| agora_mistral_en_t07 | baseline_gpt5nano_en_t07 | 0.088 | 0.145 | -0.057 | -3.55 | large | 0.0625 | 0.0014 |  |
| agora_mistral_en_t07 | baseline_mistral_en_t07 | 0.088 | 0.084 | +0.004 | +0.62 | medium | 0.3125 | 0.2410 |  |
| agora_mistral_en_t07 | baseline_together_llama33_70b_en_t07 | 0.088 | 0.081 | +0.007 | +0.92 | large | 0.0625 | 0.1087 |  |
| agora_together_llama33_70b_en_t07 | agora_union_gpt5nano_en_t07 | 0.074 | 0.162 | -0.088 | -7.36 | large | 0.0625 | 0.0001 |  |
| agora_together_llama33_70b_en_t07 | agora_union_mistral_en_t07 | 0.074 | 0.079 | -0.005 | -0.65 | medium | 0.3125 | 0.2191 |  |
| agora_together_llama33_70b_en_t07 | agora_union_together_llama33_70b_en_t07 | 0.074 | 0.079 | -0.005 | -0.56 | medium | 0.4375 | 0.2781 |  |
| agora_together_llama33_70b_en_t07 | baseline_deepseek_en_t07 | 0.074 | 0.101 | -0.027 | -1.59 | large | 0.0625 | 0.0235 |  |
| agora_together_llama33_70b_en_t07 | baseline_gpt5nano_en_t07 | 0.074 | 0.145 | -0.071 | -6.50 | large | 0.0625 | 0.0001 |  |
| agora_together_llama33_70b_en_t07 | baseline_mistral_en_t07 | 0.074 | 0.084 | -0.010 | -1.54 | large | 0.0625 | 0.0262 |  |
| agora_together_llama33_70b_en_t07 | baseline_together_llama33_70b_en_t07 | 0.074 | 0.081 | -0.007 | -0.55 | medium | 0.4375 | 0.2872 |  |
| agora_union_gpt5nano_en_t07 | agora_union_mistral_en_t07 | 0.162 | 0.079 | +0.083 | +6.23 | large | 0.0625 | 0.0002 |  |
| agora_union_gpt5nano_en_t07 | agora_union_together_llama33_70b_en_t07 | 0.162 | 0.079 | +0.083 | +5.10 | large | 0.0625 | 0.0003 |  |
| agora_union_gpt5nano_en_t07 | baseline_deepseek_en_t07 | 0.162 | 0.101 | +0.061 | +3.20 | large | 0.0625 | 0.0020 |  |
| agora_union_gpt5nano_en_t07 | baseline_gpt5nano_en_t07 | 0.162 | 0.145 | +0.017 | +2.08 | large | 0.0625 | 0.0097 |  |
| agora_union_gpt5nano_en_t07 | baseline_mistral_en_t07 | 0.162 | 0.084 | +0.078 | +5.10 | large | 0.0625 | 0.0003 |  |
| agora_union_gpt5nano_en_t07 | baseline_together_llama33_70b_en_t07 | 0.162 | 0.081 | +0.081 | +4.64 | large | 0.0625 | 0.0005 |  |
| agora_union_mistral_en_t07 | agora_union_together_llama33_70b_en_t07 | 0.079 | 0.079 | -0.000 | -0.08 | negligible | 0.8125 | 0.8669 |  |
| agora_union_mistral_en_t07 | baseline_deepseek_en_t07 | 0.079 | 0.101 | -0.022 | -1.96 | large | 0.0625 | 0.0118 |  |
| agora_union_mistral_en_t07 | baseline_gpt5nano_en_t07 | 0.079 | 0.145 | -0.066 | -5.50 | large | 0.0625 | 0.0003 |  |
| agora_union_mistral_en_t07 | baseline_mistral_en_t07 | 0.079 | 0.084 | -0.005 | -0.91 | large | 0.1875 | 0.1121 |  |
| agora_union_mistral_en_t07 | baseline_together_llama33_70b_en_t07 | 0.079 | 0.081 | -0.002 | -0.34 | small | 0.6250 | 0.4894 |  |
| agora_union_together_llama33_70b_en_t07 | baseline_deepseek_en_t07 | 0.079 | 0.101 | -0.022 | -1.88 | large | 0.0625 | 0.0137 |  |
| agora_union_together_llama33_70b_en_t07 | baseline_gpt5nano_en_t07 | 0.079 | 0.145 | -0.066 | -4.94 | large | 0.0625 | 0.0004 |  |
| agora_union_together_llama33_70b_en_t07 | baseline_mistral_en_t07 | 0.079 | 0.084 | -0.005 | -0.85 | large | 0.3125 | 0.1297 |  |
| agora_union_together_llama33_70b_en_t07 | baseline_together_llama33_70b_en_t07 | 0.079 | 0.081 | -0.002 | -0.44 | small | 0.3125 | 0.3789 |  |
| baseline_deepseek_en_t07 | baseline_gpt5nano_en_t07 | 0.101 | 0.145 | -0.045 | -2.59 | large | 0.0625 | 0.0044 |  |
| baseline_deepseek_en_t07 | baseline_mistral_en_t07 | 0.101 | 0.084 | +0.017 | +1.43 | large | 0.1250 | 0.0331 |  |
| baseline_deepseek_en_t07 | baseline_together_llama33_70b_en_t07 | 0.101 | 0.081 | +0.020 | +2.03 | large | 0.0625 | 0.0106 |  |
| baseline_gpt5nano_en_t07 | baseline_mistral_en_t07 | 0.145 | 0.084 | +0.061 | +5.04 | large | 0.0625 | 0.0004 |  |
| baseline_gpt5nano_en_t07 | baseline_together_llama33_70b_en_t07 | 0.145 | 0.081 | +0.064 | +4.59 | large | 0.0625 | 0.0005 |  |
| baseline_mistral_en_t07 | baseline_together_llama33_70b_en_t07 | 0.084 | 0.081 | +0.003 | +0.34 | small | 0.8125 | 0.4875 |  |

### HI, Temperature=0.0

| Method A | Method B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|----------|----------|--------|--------|------|-----------|--------|-------------|------------|------|
| actor_critic_deepseek_hi_t00 | actor_critic_mistral_hi_t00 | 0.130 | 0.099 | +0.031 | +3.23 | large | 0.0625 | 0.0020 |  |
| actor_critic_deepseek_hi_t00 | agora_deepseek_hi_t00 | 0.130 | 0.186 | -0.056 | -2.70 | large | 0.0625 | 0.0038 |  |
| actor_critic_deepseek_hi_t00 | agora_majority_gpt5nano_hi_t00 | 0.130 | 0.191 | -0.061 | -2.00 | large | 0.0625 | 0.0111 |  |
| actor_critic_deepseek_hi_t00 | agora_majority_mistral_hi_t00 | 0.130 | 0.104 | +0.026 | +3.30 | large | 0.0625 | 0.0018 |  |
| actor_critic_deepseek_hi_t00 | agora_majority_together_llama33_70b_hi_t00 | 0.130 | 0.065 | +0.065 | +3.61 | large | 0.0625 | 0.0013 |  |
| actor_critic_deepseek_hi_t00 | agora_mistral_hi_t00 | 0.130 | 0.115 | +0.015 | +0.78 | medium | 0.3125 | 0.1548 |  |
| actor_critic_deepseek_hi_t00 | baseline_deepseek_hi_t00 | 0.130 | 0.184 | -0.054 | -3.21 | large | 0.0625 | 0.0020 |  |
| actor_critic_deepseek_hi_t00 | baseline_mistral_hi_t00 | 0.130 | 0.100 | +0.030 | +2.63 | large | 0.0625 | 0.0042 |  |
| actor_critic_mistral_hi_t00 | agora_deepseek_hi_t00 | 0.099 | 0.186 | -0.086 | -5.53 | large | 0.0625 | 0.0002 |  |
| actor_critic_mistral_hi_t00 | agora_majority_gpt5nano_hi_t00 | 0.099 | 0.191 | -0.092 | -3.68 | large | 0.0625 | 0.0012 |  |
| actor_critic_mistral_hi_t00 | agora_majority_mistral_hi_t00 | 0.099 | 0.104 | -0.005 | -0.78 | medium | 0.3125 | 0.1568 |  |
| actor_critic_mistral_hi_t00 | agora_majority_together_llama33_70b_hi_t00 | 0.099 | 0.065 | +0.034 | +1.94 | large | 0.0625 | 0.0123 |  |
| actor_critic_mistral_hi_t00 | agora_mistral_hi_t00 | 0.099 | 0.115 | -0.016 | -0.89 | large | 0.1250 | 0.1163 |  |
| actor_critic_mistral_hi_t00 | baseline_deepseek_hi_t00 | 0.099 | 0.184 | -0.085 | -4.83 | large | 0.0625 | 0.0004 |  |
| actor_critic_mistral_hi_t00 | baseline_mistral_hi_t00 | 0.099 | 0.100 | -0.001 | -0.13 | negligible | 0.8125 | 0.7897 |  |
| agora_deepseek_hi_t00 | agora_majority_gpt5nano_hi_t00 | 0.186 | 0.191 | -0.005 | -0.51 | medium | 0.4375 | 0.3211 |  |
| agora_deepseek_hi_t00 | agora_majority_mistral_hi_t00 | 0.186 | 0.104 | +0.081 | +4.79 | large | 0.0625 | 0.0004 |  |
| agora_deepseek_hi_t00 | agora_majority_together_llama33_70b_hi_t00 | 0.186 | 0.065 | +0.121 | +5.16 | large | 0.0625 | 0.0003 |  |
| agora_deepseek_hi_t00 | agora_mistral_hi_t00 | 0.186 | 0.115 | +0.070 | +4.42 | large | 0.0625 | 0.0006 |  |
| agora_deepseek_hi_t00 | baseline_deepseek_hi_t00 | 0.186 | 0.184 | +0.002 | +0.12 | negligible | 1.0000 | 0.7986 |  |
| agora_deepseek_hi_t00 | baseline_mistral_hi_t00 | 0.186 | 0.100 | +0.085 | +5.09 | large | 0.0625 | 0.0003 |  |
| agora_majority_gpt5nano_hi_t00 | agora_majority_mistral_hi_t00 | 0.191 | 0.104 | +0.087 | +3.31 | large | 0.0625 | 0.0018 |  |
| agora_majority_gpt5nano_hi_t00 | agora_majority_together_llama33_70b_hi_t00 | 0.191 | 0.065 | +0.126 | +4.37 | large | 0.0625 | 0.0006 |  |
| agora_majority_gpt5nano_hi_t00 | agora_mistral_hi_t00 | 0.191 | 0.115 | +0.075 | +3.26 | large | 0.0625 | 0.0019 |  |
| agora_majority_gpt5nano_hi_t00 | baseline_deepseek_hi_t00 | 0.191 | 0.184 | +0.007 | +0.35 | small | 0.6250 | 0.4754 |  |
| agora_majority_gpt5nano_hi_t00 | baseline_mistral_hi_t00 | 0.191 | 0.100 | +0.091 | +3.62 | large | 0.0625 | 0.0013 |  |
| agora_majority_mistral_hi_t00 | agora_majority_together_llama33_70b_hi_t00 | 0.104 | 0.065 | +0.039 | +2.54 | large | 0.0625 | 0.0048 |  |
| agora_majority_mistral_hi_t00 | agora_mistral_hi_t00 | 0.104 | 0.115 | -0.011 | -0.52 | medium | 0.4375 | 0.3059 |  |
| agora_majority_mistral_hi_t00 | baseline_deepseek_hi_t00 | 0.104 | 0.184 | -0.080 | -5.41 | large | 0.0625 | 0.0003 |  |
| agora_majority_mistral_hi_t00 | baseline_mistral_hi_t00 | 0.104 | 0.100 | +0.004 | +1.04 | large | 0.0625 | 0.0798 |  |
| agora_majority_together_llama33_70b_hi_t00 | agora_mistral_hi_t00 | 0.065 | 0.115 | -0.050 | -1.93 | large | 0.0625 | 0.0124 |  |
| agora_majority_together_llama33_70b_hi_t00 | baseline_deepseek_hi_t00 | 0.065 | 0.184 | -0.119 | -7.32 | large | 0.0625 | 0.0001 |  |
| agora_majority_together_llama33_70b_hi_t00 | baseline_mistral_hi_t00 | 0.065 | 0.100 | -0.035 | -2.49 | large | 0.0625 | 0.0051 |  |
| agora_mistral_hi_t00 | baseline_deepseek_hi_t00 | 0.115 | 0.184 | -0.069 | -3.66 | large | 0.0625 | 0.0012 |  |
| agora_mistral_hi_t00 | baseline_mistral_hi_t00 | 0.115 | 0.100 | +0.015 | +0.65 | medium | 0.3125 | 0.2223 |  |
| baseline_deepseek_hi_t00 | baseline_mistral_hi_t00 | 0.184 | 0.100 | +0.084 | +5.91 | large | 0.0625 | 0.0002 |  |

### PT, Temperature=0.0

| Method A | Method B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|----------|----------|--------|--------|------|-----------|--------|-------------|------------|------|
| actor_critic_deepseek_pt_t00 | actor_critic_mistral_pt_t00 | 0.127 | 0.123 | +0.004 | +0.19 | negligible | 0.6250 | 0.6999 |  |
| actor_critic_deepseek_pt_t00 | agora_deepseek_pt_t00 | 0.127 | 0.180 | -0.053 | -2.11 | large | 0.0625 | 0.0093 |  |
| actor_critic_deepseek_pt_t00 | agora_majority_deepseek_pt_t00 | 0.127 | 0.228 | -0.101 | -3.15 | large | 0.0625 | 0.0021 |  |
| actor_critic_deepseek_pt_t00 | agora_majority_gpt5nano_pt_t00 | 0.127 | 0.283 | -0.156 | -3.99 | large | 0.0625 | 0.0009 |  |
| actor_critic_deepseek_pt_t00 | agora_majority_mistral_pt_t00 | 0.127 | 0.135 | -0.008 | -0.21 | small | 0.8125 | 0.6681 |  |
| actor_critic_deepseek_pt_t00 | agora_majority_together_llama33_70b_pt_t00 | 0.127 | 0.074 | +0.053 | +1.96 | large | 0.0625 | 0.0119 |  |
| actor_critic_deepseek_pt_t00 | agora_mistral_pt_t00 | 0.127 | 0.153 | -0.026 | -1.16 | large | 0.1250 | 0.0608 |  |
| actor_critic_deepseek_pt_t00 | agora_union_deepseek_pt_t00 | 0.127 | 0.220 | -0.093 | -2.82 | large | 0.0625 | 0.0032 |  |
| actor_critic_deepseek_pt_t00 | baseline_deepseek_pt_t00 | 0.127 | 0.202 | -0.075 | -2.18 | large | 0.0625 | 0.0082 |  |
| actor_critic_deepseek_pt_t00 | baseline_mistral_pt_t00 | 0.127 | 0.123 | +0.004 | +0.13 | negligible | 0.6250 | 0.7933 |  |
| actor_critic_mistral_pt_t00 | agora_deepseek_pt_t00 | 0.123 | 0.180 | -0.057 | -3.71 | large | 0.0625 | 0.0012 |  |
| actor_critic_mistral_pt_t00 | agora_majority_deepseek_pt_t00 | 0.123 | 0.228 | -0.104 | -4.48 | large | 0.0625 | 0.0006 |  |
| actor_critic_mistral_pt_t00 | agora_majority_gpt5nano_pt_t00 | 0.123 | 0.283 | -0.160 | -6.86 | large | 0.0625 | 0.0001 |  |
| actor_critic_mistral_pt_t00 | agora_majority_mistral_pt_t00 | 0.123 | 0.135 | -0.012 | -0.45 | small | 0.4375 | 0.3734 |  |
| actor_critic_mistral_pt_t00 | agora_majority_together_llama33_70b_pt_t00 | 0.123 | 0.074 | +0.049 | +4.30 | large | 0.0625 | 0.0007 |  |
| actor_critic_mistral_pt_t00 | agora_mistral_pt_t00 | 0.123 | 0.153 | -0.030 | -1.41 | large | 0.0625 | 0.0343 |  |
| actor_critic_mistral_pt_t00 | agora_union_deepseek_pt_t00 | 0.123 | 0.220 | -0.097 | -3.23 | large | 0.0625 | 0.0020 |  |
| actor_critic_mistral_pt_t00 | baseline_deepseek_pt_t00 | 0.123 | 0.202 | -0.079 | -3.71 | large | 0.0625 | 0.0012 |  |
| actor_critic_mistral_pt_t00 | baseline_mistral_pt_t00 | 0.123 | 0.123 | +0.001 | +0.04 | negligible | 0.6250 | 0.9408 |  |
| agora_deepseek_pt_t00 | agora_majority_deepseek_pt_t00 | 0.180 | 0.228 | -0.047 | -1.27 | large | 0.0625 | 0.0474 |  |
| agora_deepseek_pt_t00 | agora_majority_gpt5nano_pt_t00 | 0.180 | 0.283 | -0.103 | -4.55 | large | 0.0625 | 0.0005 |  |
| agora_deepseek_pt_t00 | agora_majority_mistral_pt_t00 | 0.180 | 0.135 | +0.045 | +1.09 | large | 0.1250 | 0.0710 |  |
| agora_deepseek_pt_t00 | agora_majority_together_llama33_70b_pt_t00 | 0.180 | 0.074 | +0.107 | +4.14 | large | 0.0625 | 0.0008 |  |
| agora_deepseek_pt_t00 | agora_mistral_pt_t00 | 0.180 | 0.153 | +0.027 | +0.99 | large | 0.1250 | 0.0908 |  |
| agora_deepseek_pt_t00 | agora_union_deepseek_pt_t00 | 0.180 | 0.220 | -0.040 | -0.89 | large | 0.1250 | 0.1181 |  |
| agora_deepseek_pt_t00 | baseline_deepseek_pt_t00 | 0.180 | 0.202 | -0.022 | -0.74 | medium | 0.1875 | 0.1730 |  |
| agora_deepseek_pt_t00 | baseline_mistral_pt_t00 | 0.180 | 0.123 | +0.058 | +2.23 | large | 0.0625 | 0.0076 |  |
| agora_majority_deepseek_pt_t00 | agora_majority_gpt5nano_pt_t00 | 0.228 | 0.283 | -0.055 | -1.32 | large | 0.1250 | 0.0419 |  |
| agora_majority_deepseek_pt_t00 | agora_majority_mistral_pt_t00 | 0.228 | 0.135 | +0.092 | +8.12 | large | 0.0625 | 0.0001 |  |
| agora_majority_deepseek_pt_t00 | agora_majority_together_llama33_70b_pt_t00 | 0.228 | 0.074 | +0.154 | +9.27 | large | 0.0625 | 0.0000 |  |
| agora_majority_deepseek_pt_t00 | agora_mistral_pt_t00 | 0.228 | 0.153 | +0.074 | +3.20 | large | 0.0625 | 0.0020 |  |
| agora_majority_deepseek_pt_t00 | agora_union_deepseek_pt_t00 | 0.228 | 0.220 | +0.007 | +0.37 | small | 0.4375 | 0.4500 |  |
| agora_majority_deepseek_pt_t00 | baseline_deepseek_pt_t00 | 0.228 | 0.202 | +0.025 | +1.47 | large | 0.0625 | 0.0305 |  |
| agora_majority_deepseek_pt_t00 | baseline_mistral_pt_t00 | 0.228 | 0.123 | +0.105 | +4.36 | large | 0.0625 | 0.0006 |  |
| agora_majority_gpt5nano_pt_t00 | agora_majority_mistral_pt_t00 | 0.283 | 0.135 | +0.147 | +3.55 | large | 0.0625 | 0.0014 |  |
| agora_majority_gpt5nano_pt_t00 | agora_majority_together_llama33_70b_pt_t00 | 0.283 | 0.074 | +0.209 | +7.24 | large | 0.0625 | 0.0001 |  |
| agora_majority_gpt5nano_pt_t00 | agora_mistral_pt_t00 | 0.283 | 0.153 | +0.130 | +2.97 | large | 0.0625 | 0.0027 |  |
| agora_majority_gpt5nano_pt_t00 | agora_union_deepseek_pt_t00 | 0.283 | 0.220 | +0.063 | +1.39 | large | 0.1250 | 0.0356 |  |
| agora_majority_gpt5nano_pt_t00 | baseline_deepseek_pt_t00 | 0.283 | 0.202 | +0.081 | +2.13 | large | 0.0625 | 0.0089 |  |
| agora_majority_gpt5nano_pt_t00 | baseline_mistral_pt_t00 | 0.283 | 0.123 | +0.160 | +7.48 | large | 0.0625 | 0.0001 |  |
| agora_majority_mistral_pt_t00 | agora_majority_together_llama33_70b_pt_t00 | 0.135 | 0.074 | +0.062 | +3.42 | large | 0.0625 | 0.0016 |  |
| agora_majority_mistral_pt_t00 | agora_mistral_pt_t00 | 0.135 | 0.153 | -0.018 | -0.59 | medium | 0.4375 | 0.2587 |  |
| agora_majority_mistral_pt_t00 | agora_union_deepseek_pt_t00 | 0.135 | 0.220 | -0.085 | -3.48 | large | 0.0625 | 0.0015 |  |
| agora_majority_mistral_pt_t00 | baseline_deepseek_pt_t00 | 0.135 | 0.202 | -0.067 | -3.48 | large | 0.0625 | 0.0015 |  |
| agora_majority_mistral_pt_t00 | baseline_mistral_pt_t00 | 0.135 | 0.123 | +0.013 | +0.55 | medium | 0.3125 | 0.2885 |  |
| agora_majority_together_llama33_70b_pt_t00 | agora_mistral_pt_t00 | 0.074 | 0.153 | -0.080 | -3.47 | large | 0.0625 | 0.0015 |  |
| agora_majority_together_llama33_70b_pt_t00 | agora_union_deepseek_pt_t00 | 0.074 | 0.220 | -0.147 | -6.10 | large | 0.0625 | 0.0002 |  |
| agora_majority_together_llama33_70b_pt_t00 | baseline_deepseek_pt_t00 | 0.074 | 0.202 | -0.128 | -6.56 | large | 0.0625 | 0.0001 |  |
| agora_majority_together_llama33_70b_pt_t00 | baseline_mistral_pt_t00 | 0.074 | 0.123 | -0.049 | -2.67 | large | 0.0625 | 0.0040 |  |
| agora_mistral_pt_t00 | agora_union_deepseek_pt_t00 | 0.153 | 0.220 | -0.067 | -1.84 | large | 0.0625 | 0.0146 |  |
| agora_mistral_pt_t00 | baseline_deepseek_pt_t00 | 0.153 | 0.202 | -0.049 | -2.62 | large | 0.0625 | 0.0042 |  |
| agora_mistral_pt_t00 | baseline_mistral_pt_t00 | 0.153 | 0.123 | +0.031 | +0.95 | large | 0.1250 | 0.1009 |  |
| agora_union_deepseek_pt_t00 | baseline_deepseek_pt_t00 | 0.220 | 0.202 | +0.018 | +0.52 | medium | 0.3125 | 0.3119 |  |
| agora_union_deepseek_pt_t00 | baseline_mistral_pt_t00 | 0.220 | 0.123 | +0.098 | +2.99 | large | 0.0625 | 0.0026 |  |
| baseline_deepseek_pt_t00 | baseline_mistral_pt_t00 | 0.202 | 0.123 | +0.079 | +3.86 | large | 0.0625 | 0.0010 |  |

### RU, Temperature=0.0

| Method A | Method B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|----------|----------|--------|--------|------|-----------|--------|-------------|------------|------|
| actor_critic_deepseek_ru_t00 | actor_critic_mistral_ru_t00 | 0.212 | 0.139 | +0.073 | +4.28 | large | 0.0625 | 0.0007 |  |
| actor_critic_deepseek_ru_t00 | agora_deepseek_ru_t00 | 0.212 | 0.215 | -0.003 | -0.16 | negligible | 0.8125 | 0.7376 |  |
| actor_critic_deepseek_ru_t00 | agora_majority_gpt5nano_ru_t00 | 0.212 | 0.225 | -0.013 | -0.25 | small | 0.6250 | 0.6078 |  |
| actor_critic_deepseek_ru_t00 | agora_majority_mistral_ru_t00 | 0.212 | 0.142 | +0.071 | +7.32 | large | 0.0625 | 0.0001 |  |
| actor_critic_deepseek_ru_t00 | agora_majority_together_llama33_70b_ru_t00 | 0.212 | 0.141 | +0.071 | +4.33 | large | 0.0625 | 0.0006 |  |
| actor_critic_deepseek_ru_t00 | agora_mistral_ru_t00 | 0.212 | 0.148 | +0.064 | +2.28 | large | 0.0625 | 0.0070 |  |
| actor_critic_deepseek_ru_t00 | baseline_deepseek_ru_t00 | 0.212 | 0.205 | +0.008 | +0.58 | medium | 0.3125 | 0.2620 |  |
| actor_critic_deepseek_ru_t00 | baseline_mistral_ru_t00 | 0.212 | 0.135 | +0.077 | +4.20 | large | 0.0625 | 0.0007 |  |
| actor_critic_mistral_ru_t00 | agora_deepseek_ru_t00 | 0.139 | 0.215 | -0.076 | -16.32 | large | 0.0625 | 0.0000 |  |
| actor_critic_mistral_ru_t00 | agora_majority_gpt5nano_ru_t00 | 0.139 | 0.225 | -0.086 | -1.98 | large | 0.0625 | 0.0115 |  |
| actor_critic_mistral_ru_t00 | agora_majority_mistral_ru_t00 | 0.139 | 0.142 | -0.002 | -0.25 | small | 0.6250 | 0.6075 |  |
| actor_critic_mistral_ru_t00 | agora_majority_together_llama33_70b_ru_t00 | 0.139 | 0.141 | -0.002 | -0.58 | medium | 0.3125 | 0.2665 |  |
| actor_critic_mistral_ru_t00 | agora_mistral_ru_t00 | 0.139 | 0.148 | -0.009 | -0.50 | small | 0.3125 | 0.3303 |  |
| actor_critic_mistral_ru_t00 | baseline_deepseek_ru_t00 | 0.139 | 0.205 | -0.065 | -8.25 | large | 0.0625 | 0.0001 |  |
| actor_critic_mistral_ru_t00 | baseline_mistral_ru_t00 | 0.139 | 0.135 | +0.004 | +1.17 | large | 0.1250 | 0.0593 |  |
| agora_deepseek_ru_t00 | agora_majority_gpt5nano_ru_t00 | 0.215 | 0.225 | -0.010 | -0.23 | small | 0.8125 | 0.6331 |  |
| agora_deepseek_ru_t00 | agora_majority_mistral_ru_t00 | 0.215 | 0.142 | +0.074 | +9.09 | large | 0.0625 | 0.0000 |  |
| agora_deepseek_ru_t00 | agora_majority_together_llama33_70b_ru_t00 | 0.215 | 0.141 | +0.074 | +22.23 | large | 0.0625 | 0.0000 |  |
| agora_deepseek_ru_t00 | agora_mistral_ru_t00 | 0.215 | 0.148 | +0.067 | +3.63 | large | 0.0625 | 0.0013 |  |
| agora_deepseek_ru_t00 | baseline_deepseek_ru_t00 | 0.215 | 0.205 | +0.011 | +1.06 | large | 0.1250 | 0.0761 |  |
| agora_deepseek_ru_t00 | baseline_mistral_ru_t00 | 0.215 | 0.135 | +0.080 | +36.22 | large | 0.0625 | 0.0000 |  |
| agora_majority_gpt5nano_ru_t00 | agora_majority_mistral_ru_t00 | 0.225 | 0.142 | +0.084 | +1.87 | large | 0.0625 | 0.0140 |  |
| agora_majority_gpt5nano_ru_t00 | agora_majority_together_llama33_70b_ru_t00 | 0.225 | 0.141 | +0.084 | +1.87 | large | 0.0625 | 0.0140 |  |
| agora_majority_gpt5nano_ru_t00 | agora_mistral_ru_t00 | 0.225 | 0.148 | +0.077 | +1.43 | large | 0.1250 | 0.0328 |  |
| agora_majority_gpt5nano_ru_t00 | baseline_deepseek_ru_t00 | 0.225 | 0.205 | +0.021 | +0.48 | small | 0.4375 | 0.3479 |  |
| agora_majority_gpt5nano_ru_t00 | baseline_mistral_ru_t00 | 0.225 | 0.135 | +0.090 | +2.08 | large | 0.0625 | 0.0096 |  |
| agora_majority_mistral_ru_t00 | agora_majority_together_llama33_70b_ru_t00 | 0.142 | 0.141 | +0.000 | +0.04 | negligible | 1.0000 | 0.9398 |  |
| agora_majority_mistral_ru_t00 | agora_mistral_ru_t00 | 0.142 | 0.148 | -0.007 | -0.29 | small | 0.6250 | 0.5535 |  |
| agora_majority_mistral_ru_t00 | baseline_deepseek_ru_t00 | 0.142 | 0.205 | -0.063 | -7.21 | large | 0.0625 | 0.0001 |  |
| agora_majority_mistral_ru_t00 | baseline_mistral_ru_t00 | 0.142 | 0.135 | +0.006 | +0.64 | medium | 0.3125 | 0.2245 |  |
| agora_majority_together_llama33_70b_ru_t00 | agora_mistral_ru_t00 | 0.141 | 0.148 | -0.007 | -0.44 | small | 0.3125 | 0.3828 |  |
| agora_majority_together_llama33_70b_ru_t00 | baseline_deepseek_ru_t00 | 0.141 | 0.205 | -0.063 | -8.03 | large | 0.0625 | 0.0001 |  |
| agora_majority_together_llama33_70b_ru_t00 | baseline_mistral_ru_t00 | 0.141 | 0.135 | +0.006 | +1.79 | large | 0.0625 | 0.0162 |  |
| agora_mistral_ru_t00 | baseline_deepseek_ru_t00 | 0.148 | 0.205 | -0.056 | -2.98 | large | 0.0625 | 0.0026 |  |
| agora_mistral_ru_t00 | baseline_mistral_ru_t00 | 0.148 | 0.135 | +0.013 | +0.72 | medium | 0.3125 | 0.1846 |  |
| baseline_deepseek_ru_t00 | baseline_mistral_ru_t00 | 0.205 | 0.135 | +0.069 | +6.93 | large | 0.0625 | 0.0001 |  |

### RU, Temperature=0.7

| Method A | Method B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |
|----------|----------|--------|--------|------|-----------|--------|-------------|------------|------|
| actor_critic_deepseek_ru_t07 | agora_deepseek_ru_t07 | 0.217 | 0.212 | +0.005 | +0.10 | negligible | 0.6250 | 0.8260 |  |
| actor_critic_deepseek_ru_t07 | baseline_deepseek_ru_t07 | 0.217 | 0.200 | +0.017 | +0.38 | small | 0.4375 | 0.4457 |  |
| agora_deepseek_ru_t07 | baseline_deepseek_ru_t07 | 0.212 | 0.200 | +0.011 | +0.62 | medium | 0.3125 | 0.2352 |  |


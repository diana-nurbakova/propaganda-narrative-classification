# Enhanced Experiment Results Report

_Generated_: 2026-04-19 16:37  
_Experiments evaluated_: **37** of 37

## Methodology

Each experiment is evaluated using the **all-runs averaging** strategy: every successful run is scored independently against the SemEval-2025 Task 10 dev-set ground truth, then mean and standard deviation are reported across runs.

Metrics computed:

| Metric | Description |
|--------|-------------|
| F1-samples (narr / sub) | SemEval primary metric, set-based per-document F1, averaged. |
| hP / hR / hF | Hierarchical P/R/F1 with ancestor augmentation (Kiritchenko et al. 2006). |
| HCR | Hierarchical Consistency Rate — fraction of docs with no orphan sub-narratives. |
| ICM (norm.) | Information Contrast Model normalised by ICM(gold,gold) (Amigó & Delgado 2022). |
| Sibling / Same-domain / Cross-domain / Hallucination | Error severity from LCA depth of false positives. |
| Inter-run Jaccard | Pairwise Jaccard between runs of the same experiment, averaged over docs. |
| TCM (bis) | Transport Confusion Matrix at narrative level, bistochastic-normalised via IPF. |


## Results by Language

### BG

| Experiment | Model | Method | Runs | F1ₐ narr | F1ₐ sub | hF | HCR | ICM | InterRun (sub) |
|---|---|---|---|---|---|---|---|---|---|
| baseline_deepseek_bg_t00 | DeepSeek V3 | Baseline | 5 | 0.575 ± 0.010 | 0.276 ± 0.007 | 0.564 ± 0.007 | 1.000 ± 0.000 | -1.457 ± 0.060 | 0.891 |
| baseline_deepseek_bg_t07 | DeepSeek V3 | Baseline | 5 | 0.565 ± 0.008 | 0.271 ± 0.004 | 0.554 ± 0.004 | 1.000 ± 0.000 | -1.546 ± 0.057 | 0.859 |
| baseline_p0prime_together_llama33_70b_bg_t00 | Llama 3.3 70B | Baseline | 5 | 0.515 ± 0.014 | 0.236 ± 0.010 | 0.495 ± 0.010 | 1.000 ± 0.000 | -2.223 ± 0.079 | 0.843 |
| baseline_together_llama33_70b_bg_t00 | Llama 3.3 70B | Baseline | 5 | 0.488 ± 0.017 | 0.207 ± 0.007 | 0.467 ± 0.015 | 1.000 ± 0.000 | -2.530 ± 0.179 | 0.766 |
| baseline_p1_together_llama33_70b_bg_t00 | Llama 3.3 70B | Baseline | 5 | 0.499 ± 0.039 | 0.213 ± 0.014 | 0.467 ± 0.016 | 1.000 ± 0.000 | -2.785 ± 0.289 | 0.738 |
| baseline_mistral_bg_t00 | Mistral Large | Baseline | 5 | 0.480 ± 0.019 | 0.207 ± 0.010 | 0.438 ± 0.006 | 1.000 ± 0.000 | -2.975 ± 0.152 | 0.831 |

_Error severity (sub-narrative false positives, mean over runs)_:

| Experiment | Sibling | Same-dom | Cross-dom | Hallucinations |
|---|---|---|---|---|
| baseline_deepseek_bg_t00 | 21.92% | 38.37% | 0.00% | 39.71% |
| baseline_deepseek_bg_t07 | 21.90% | 38.02% | 0.20% | 39.88% |
| baseline_p0prime_together_llama33_70b_bg_t00 | 20.98% | 36.52% | 2.10% | 40.39% |
| baseline_together_llama33_70b_bg_t00 | 18.61% | 41.63% | 0.56% | 39.21% |
| baseline_p1_together_llama33_70b_bg_t00 | 16.49% | 44.59% | 0.71% | 38.21% |
| baseline_mistral_bg_t00 | 14.22% | 48.66% | 0.58% | 36.54% |

### EN

| Experiment | Model | Method | Runs | F1ₐ narr | F1ₐ sub | hF | HCR | ICM | InterRun (sub) |
|---|---|---|---|---|---|---|---|---|---|
| baseline_gpt5nano_en_t00 | GPT-5 Nano | Baseline | 5 | 0.341 ± 0.034 | 0.233 ± 0.024 | 0.455 ± 0.017 | 1.000 ± 0.000 | -2.730 ± 0.200 | 0.555 |
| baseline_gpt5nano_en_t07 | GPT-5 Nano | Baseline | 5 | 0.308 ± 0.021 | 0.205 ± 0.018 | 0.430 ± 0.006 | 1.000 ± 0.000 | -3.106 ± 0.099 | 0.589 |
| baseline_deepseek_en_t00_evidence | DeepSeek V3 | Baseline | 1 | 0.355 ± 0.000 | 0.160 ± 0.000 | 0.427 ± 0.000 | 1.000 ± 0.000 | -2.825 ± 0.000 | 1.000 |
| baseline_deepseek_en_t00 | DeepSeek V3 | Baseline | 5 | 0.342 ± 0.013 | 0.150 ± 0.012 | 0.403 ± 0.010 | 1.000 ± 0.000 | -3.143 ± 0.065 | 0.794 |
| baseline_deepseek_en_t07 | DeepSeek V3 | Baseline | 5 | 0.329 ± 0.012 | 0.146 ± 0.013 | 0.399 ± 0.012 | 1.000 ± 0.000 | -3.155 ± 0.174 | 0.731 |
| baseline_p1_together_llama33_70b_en_t00 | Llama 3.3 70B | Baseline | 5 | 0.368 ± 0.010 | 0.153 ± 0.006 | 0.392 ± 0.010 | 1.000 ± 0.000 | -3.188 ± 0.187 | 0.765 |
| baseline_gemini_en_t00 | Gemini 2.5 Flash | Baseline | 5 | 0.354 ± 0.012 | 0.197 ± 0.009 | 0.379 ± 0.009 | 1.000 ± 0.000 | -3.780 ± 0.131 | 0.815 |
| baseline_gemini_en_t07 | Gemini 2.5 Flash | Baseline | 1 | 0.367 ± 0.000 | 0.276 ± 0.000 | 0.373 ± 0.000 | 1.000 ± 0.000 | -5.545 ± 0.000 | 1.000 |
| baseline_p0prime_together_llama33_70b_en_t00 | Llama 3.3 70B | Baseline | 5 | 0.315 ± 0.010 | 0.124 ± 0.003 | 0.352 ± 0.010 | 1.000 ± 0.000 | -3.906 ± 0.268 | 0.818 |
| baseline_mistral_en_t00 | Mistral Large | Baseline | 5 | 0.308 ± 0.005 | 0.130 ± 0.002 | 0.339 ± 0.004 | 1.000 ± 0.000 | -4.166 ± 0.204 | 0.738 |
| baseline_mistral_en_t00_evidence | Mistral Large | Baseline | 1 | 0.312 ± 0.000 | 0.125 ± 0.000 | 0.337 ± 0.000 | 1.000 ± 0.000 | -4.205 ± 0.000 | 1.000 |
| baseline_mistral_en_t07 | Mistral Large | Baseline | 5 | 0.299 ± 0.009 | 0.132 ± 0.019 | 0.334 ± 0.006 | 1.000 ± 0.000 | -4.214 ± 0.242 | 0.617 |
| baseline_together_llama33_70b_en_t07 | Llama 3.3 70B | Baseline | 5 | 0.300 ± 0.009 | 0.114 ± 0.008 | 0.330 ± 0.007 | 1.000 ± 0.000 | -4.236 ± 0.098 | 0.646 |
| baseline_together_llama33_70b_en_t00 | Llama 3.3 70B | Baseline | 5 | 0.285 ± 0.013 | 0.105 ± 0.005 | 0.312 ± 0.006 | 1.000 ± 0.000 | -4.449 ± 0.155 | 0.772 |

_Error severity (sub-narrative false positives, mean over runs)_:

| Experiment | Sibling | Same-dom | Cross-dom | Hallucinations |
|---|---|---|---|---|
| baseline_gpt5nano_en_t00 | 11.57% | 68.44% | 6.59% | 13.41% |
| baseline_gpt5nano_en_t07 | 11.98% | 64.48% | 8.44% | 15.09% |
| baseline_deepseek_en_t00_evidence | 12.05% | 72.89% | 0.00% | 15.06% |
| baseline_deepseek_en_t00 | 11.31% | 72.42% | 0.00% | 16.26% |
| baseline_deepseek_en_t07 | 10.62% | 69.84% | 2.26% | 17.28% |
| baseline_p1_together_llama33_70b_en_t00 | 10.47% | 68.38% | 4.29% | 16.86% |
| baseline_gemini_en_t00 | 11.50% | 65.32% | 6.24% | 16.93% |
| baseline_gemini_en_t07 | 16.92% | 81.54% | 1.54% | 0.00% |
| baseline_p0prime_together_llama33_70b_en_t00 | 8.07% | 74.72% | 0.59% | 16.62% |
| baseline_mistral_en_t00 | 9.26% | 72.81% | 0.23% | 17.71% |
| baseline_mistral_en_t00_evidence | 9.33% | 73.88% | 0.37% | 16.42% |
| baseline_mistral_en_t07 | 9.57% | 73.68% | 0.30% | 16.45% |
| baseline_together_llama33_70b_en_t07 | 7.48% | 75.01% | 1.31% | 16.21% |
| baseline_together_llama33_70b_en_t00 | 7.44% | 73.89% | 2.99% | 15.67% |

### HI

| Experiment | Model | Method | Runs | F1ₐ narr | F1ₐ sub | hF | HCR | ICM | InterRun (sub) |
|---|---|---|---|---|---|---|---|---|---|
| baseline_deepseek_hi_t00 | DeepSeek V3 | Baseline | 5 | 0.430 ± 0.021 | 0.308 ± 0.016 | 0.492 ± 0.014 | 1.000 ± 0.000 | -3.143 ± 0.058 | 0.800 |
| baseline_p1_together_llama33_70b_hi_t00 | Llama 3.3 70B | Baseline | 5 | 0.339 ± 0.010 | 0.341 ± 0.020 | 0.443 ± 0.004 | 1.000 ± 0.000 | -2.689 ± 0.162 | 0.838 |
| baseline_together_llama33_70b_hi_t00 | Llama 3.3 70B | Baseline | 5 | 0.292 ± 0.012 | 0.179 ± 0.016 | 0.388 ± 0.013 | 1.000 ± 0.000 | -3.482 ± 0.287 | 0.703 |
| baseline_mistral_hi_t00 | Mistral Large | Baseline | 5 | 0.320 ± 0.023 | 0.148 ± 0.013 | 0.379 ± 0.005 | 1.000 ± 0.000 | -5.452 ± 0.118 | 0.744 |
| baseline_p0prime_together_llama33_70b_hi_t00 | Llama 3.3 70B | Baseline | 5 | 0.261 ± 0.018 | 0.291 ± 0.026 | 0.375 ± 0.007 | 1.000 ± 0.000 | -2.997 ± 0.394 | 0.718 |

_Error severity (sub-narrative false positives, mean over runs)_:

| Experiment | Sibling | Same-dom | Cross-dom | Hallucinations |
|---|---|---|---|---|
| baseline_deepseek_hi_t00 | 15.40% | 38.92% | 0.00% | 45.68% |
| baseline_p1_together_llama33_70b_hi_t00 | 18.68% | 45.04% | 0.60% | 35.69% |
| baseline_together_llama33_70b_hi_t00 | 14.06% | 46.23% | 0.00% | 39.72% |
| baseline_mistral_hi_t00 | 9.99% | 46.78% | 0.00% | 43.23% |
| baseline_p0prime_together_llama33_70b_hi_t00 | 16.40% | 49.07% | 0.81% | 33.73% |

### PT

| Experiment | Model | Method | Runs | F1ₐ narr | F1ₐ sub | hF | HCR | ICM | InterRun (sub) |
|---|---|---|---|---|---|---|---|---|---|
| baseline_deepseek_pt_t07 | DeepSeek V3 | Baseline | 5 | 0.504 ± 0.030 | 0.373 ± 0.033 | 0.574 ± 0.020 | 1.000 ± 0.000 | -1.120 ± 0.119 | 0.778 |
| baseline_deepseek_pt_t00 | DeepSeek V3 | Baseline | 5 | 0.510 ± 0.020 | 0.346 ± 0.033 | 0.573 ± 0.010 | 1.000 ± 0.000 | -1.154 ± 0.150 | 0.859 |
| baseline_p1_together_llama33_70b_pt_t00 | Llama 3.3 70B | Baseline | 5 | 0.557 ± 0.037 | 0.383 ± 0.050 | 0.553 ± 0.019 | 1.000 ± 0.000 | -3.412 ± 0.543 | 0.762 |
| baseline_p0prime_together_llama33_70b_pt_t00 | Llama 3.3 70B | Baseline | 5 | 0.467 ± 0.030 | 0.339 ± 0.026 | 0.516 ± 0.017 | 1.000 ± 0.000 | -2.133 ± 0.156 | 0.861 |
| baseline_mistral_pt_t00 | Mistral Large | Baseline | 5 | 0.382 ± 0.036 | 0.277 ± 0.023 | 0.459 ± 0.012 | 1.000 ± 0.000 | -3.596 ± 0.278 | 0.736 |
| baseline_together_llama33_70b_pt_t00 | Llama 3.3 70B | Baseline | 5 | 0.307 ± 0.032 | 0.354 ± 0.031 | 0.430 ± 0.021 | 1.000 ± 0.000 | -1.575 ± 0.144 | 0.903 |

_Error severity (sub-narrative false positives, mean over runs)_:

| Experiment | Sibling | Same-dom | Cross-dom | Hallucinations |
|---|---|---|---|---|
| baseline_deepseek_pt_t07 | 22.98% | 43.97% | 0.00% | 33.06% |
| baseline_deepseek_pt_t00 | 22.55% | 41.66% | 0.00% | 35.79% |
| baseline_p1_together_llama33_70b_pt_t00 | 30.05% | 46.45% | 0.00% | 23.50% |
| baseline_p0prime_together_llama33_70b_pt_t00 | 24.78% | 49.29% | 0.00% | 25.93% |
| baseline_mistral_pt_t00 | 16.66% | 55.56% | 0.00% | 27.78% |
| baseline_together_llama33_70b_pt_t00 | 22.33% | 56.11% | 0.00% | 21.56% |

### RU

| Experiment | Model | Method | Runs | F1ₐ narr | F1ₐ sub | hF | HCR | ICM | InterRun (sub) |
|---|---|---|---|---|---|---|---|---|---|
| baseline_deepseek_ru_t00 | DeepSeek V3 | Baseline | 5 | 0.481 ± 0.018 | 0.269 ± 0.016 | 0.526 ± 0.011 | 1.000 ± 0.000 | -3.048 ± 0.169 | 0.851 |
| baseline_deepseek_ru_t07 | DeepSeek V3 | Baseline | 5 | 0.472 ± 0.009 | 0.259 ± 0.008 | 0.519 ± 0.005 | 1.000 ± 0.000 | -3.053 ± 0.137 | 0.777 |
| baseline_p0prime_together_llama33_70b_ru_t00 | Llama 3.3 70B | Baseline | 5 | 0.371 ± 0.026 | 0.216 ± 0.019 | 0.431 ± 0.019 | 1.000 ± 0.000 | -4.042 ± 0.325 | 0.787 |
| baseline_mistral_ru_t00 | Mistral Large | Baseline | 5 | 0.382 ± 0.008 | 0.200 ± 0.009 | 0.409 ± 0.004 | 1.000 ± 0.000 | -5.601 ± 0.139 | 0.799 |
| baseline_p1_together_llama33_70b_ru_t00 | Llama 3.3 70B | Baseline | 5 | 0.346 ± 0.010 | 0.188 ± 0.003 | 0.407 ± 0.007 | 1.000 ± 0.000 | -4.046 ± 0.136 | 0.777 |
| baseline_together_llama33_70b_ru_t00 | Llama 3.3 70B | Baseline | 5 | 0.335 ± 0.017 | 0.202 ± 0.021 | 0.386 ± 0.018 | 1.000 ± 0.000 | -5.079 ± 0.412 | 0.729 |

_Error severity (sub-narrative false positives, mean over runs)_:

| Experiment | Sibling | Same-dom | Cross-dom | Hallucinations |
|---|---|---|---|---|
| baseline_deepseek_ru_t00 | 16.02% | 55.93% | 0.00% | 28.05% |
| baseline_deepseek_ru_t07 | 15.25% | 57.14% | 0.00% | 27.61% |
| baseline_p0prime_together_llama33_70b_ru_t00 | 19.88% | 61.18% | 0.47% | 18.46% |
| baseline_mistral_ru_t00 | 15.69% | 61.44% | 0.00% | 22.87% |
| baseline_p1_together_llama33_70b_ru_t00 | 17.99% | 60.85% | 0.72% | 20.44% |
| baseline_together_llama33_70b_ru_t00 | 15.76% | 64.53% | 0.85% | 18.86% |

## Pairwise Significance Tests (paired, hF)

| A vs B | n | mean diff | Cohen's d | p (t-test) | p (Wilcoxon) |
|---|---|---|---|---|---|
| baseline_deepseek_bg_t00 vs baseline_deepseek_bg_t07 | 5 | +0.009 | +1.11 | 0.0675 | 0.1250  |
| baseline_deepseek_en_t00 vs baseline_deepseek_en_t07 | 5 | +0.004 | +0.28 | 0.5645 | 1.0000  |
| baseline_deepseek_pt_t00 vs baseline_deepseek_pt_t07 | 5 | -0.001 | -0.06 | 0.9078 | 1.0000  |
| baseline_deepseek_ru_t00 vs baseline_deepseek_ru_t07 | 5 | +0.007 | +0.53 | 0.3044 | 0.4375  |
| baseline_gpt5nano_en_t00 vs baseline_gpt5nano_en_t07 | 5 | +0.025 | +1.30 | 0.0437 | 0.0625  |
| baseline_mistral_en_t00 vs baseline_mistral_en_t07 | 5 | +0.005 | +1.17 | 0.0586 | 0.1250  |
| baseline_p0prime_together_llama33_70b_bg_t00 vs baseline_p1_together_llama33_70b_bg_t00 | 5 | +0.028 | +2.55 | 0.0047 | 0.0625  |
| baseline_p0prime_together_llama33_70b_bg_t00 vs baseline_together_llama33_70b_bg_t00 | 5 | +0.028 | +1.31 | 0.0426 | 0.1250  |
| baseline_p0prime_together_llama33_70b_en_t00 vs baseline_p1_together_llama33_70b_en_t00 | 5 | -0.040 | -2.34 | 0.0064 | 0.0625  |
| baseline_p0prime_together_llama33_70b_en_t00 vs baseline_together_llama33_70b_en_t00 | 5 | +0.040 | +2.95 | 0.0027 | 0.0625  |
| baseline_p0prime_together_llama33_70b_en_t00 vs baseline_together_llama33_70b_en_t07 | 5 | +0.022 | +1.58 | 0.0244 | 0.0625  |
| baseline_p0prime_together_llama33_70b_hi_t00 vs baseline_p1_together_llama33_70b_hi_t00 | 5 | -0.068 | -6.42 | 0.0001 | 0.0625  |
| baseline_p0prime_together_llama33_70b_hi_t00 vs baseline_together_llama33_70b_hi_t00 | 5 | -0.013 | -0.80 | 0.1499 | 0.1875  |
| baseline_p0prime_together_llama33_70b_pt_t00 vs baseline_p1_together_llama33_70b_pt_t00 | 5 | -0.037 | -1.18 | 0.0578 | 0.1250  |
| baseline_p0prime_together_llama33_70b_pt_t00 vs baseline_together_llama33_70b_pt_t00 | 5 | +0.086 | +5.62 | 0.0002 | 0.0625  |
| baseline_p0prime_together_llama33_70b_ru_t00 vs baseline_p1_together_llama33_70b_ru_t00 | 5 | +0.025 | +1.05 | 0.0788 | 0.1250  |
| baseline_p0prime_together_llama33_70b_ru_t00 vs baseline_together_llama33_70b_ru_t00 | 5 | +0.046 | +2.25 | 0.0073 | 0.0625  |
| baseline_p1_together_llama33_70b_bg_t00 vs baseline_together_llama33_70b_bg_t00 | 5 | -0.000 | -0.02 | 0.9739 | 0.8125  |
| baseline_p1_together_llama33_70b_en_t00 vs baseline_together_llama33_70b_en_t00 | 5 | +0.080 | +7.15 | 0.0001 | 0.0625  |
| baseline_p1_together_llama33_70b_en_t00 vs baseline_together_llama33_70b_en_t07 | 5 | +0.062 | +7.04 | 0.0001 | 0.0625  |
| baseline_p1_together_llama33_70b_hi_t00 vs baseline_together_llama33_70b_hi_t00 | 5 | +0.055 | +4.04 | 0.0008 | 0.0625  |
| baseline_p1_together_llama33_70b_pt_t00 vs baseline_together_llama33_70b_pt_t00 | 5 | +0.123 | +5.11 | 0.0003 | 0.0625  |
| baseline_p1_together_llama33_70b_ru_t00 vs baseline_together_llama33_70b_ru_t00 | 5 | +0.021 | +1.34 | 0.0397 | 0.1250  |
| baseline_together_llama33_70b_en_t00 vs baseline_together_llama33_70b_en_t07 | 5 | -0.018 | -2.07 | 0.0099 | 0.0625  |

## Top Confused Narrative Pairs (bistochastic TCM)

The bistochastic normalisation removes class-frequency bias from the raw TCM, isolating purely structural confusion between narratives. Pairs are reported per language for the best-hF experiment in that language.

### BG — baseline_deepseek_bg_t00

| Gold narrative | Predicted as | bis(TCM) mass | raw mass | same-domain |
|---|---|---|---|---|
| Discrediting the West, Diplomacy | Praise of Russia | 0.4996 | 2.8343 | yes |
| Blaming the war on others rather than the invader | Distrust towards Media | 0.4813 | 1.2510 | yes |
| Negative Consequences for the West | Amplifying war-related fears | 0.3437 | 1.6677 | yes |
| Amplifying war-related fears | Speculating war outcomes | 0.2805 | 1.9177 | yes |
| Criticism of climate movement | Criticism of climate policies | 0.2763 | 1.2510 | yes |
| Negative Consequences for the West | Blaming the war on others rather than the invader | 0.2432 | 1.6677 | yes |
| Downplaying climate change | Controversy about green technologies | 0.2238 | 1.2010 | yes |
| Criticism of climate movement | Criticism of institutions and authorities | 0.2214 | 0.7510 | yes |

### EN — baseline_gpt5nano_en_t00

| Gold narrative | Predicted as | bis(TCM) mass | raw mass | same-domain |
|---|---|---|---|---|
| Questioning the measurements and science | Downplaying climate change | 0.3198 | 0.7510 | yes |
| Criticism of institutions and authorities | Green policies are geopolitical instruments | 0.2997 | 1.6510 | yes |
| Criticism of climate movement | Downplaying climate change | 0.2550 | 3.0788 | yes |
| Overpraising the West | Speculating war outcomes | 0.2540 | 2.0010 | yes |
| Controversy about green technologies | Criticism of institutions and authorities | 0.2483 | 1.4010 | yes |
| Criticism of climate policies | Criticism of climate movement | 0.2240 | 3.9010 | yes |
| Overpraising the West | Amplifying war-related fears | 0.2216 | 1.0010 | yes |
| Controversy about green technologies | Criticism of climate policies | 0.2143 | 1.4010 | yes |

### HI — baseline_deepseek_hi_t00

| Gold narrative | Predicted as | bis(TCM) mass | raw mass | same-domain |
|---|---|---|---|---|
| Speculating war outcomes | Negative Consequences for the West | 0.4601 | 2.0010 | yes |
| Speculating war outcomes | Russia is the Victim | 0.4412 | 2.0010 | yes |
| Hidden plots by secret schemes of powerful groups | Discrediting Ukraine | 0.3820 | 0.8343 | no |
| Discrediting the West, Diplomacy | Speculating war outcomes | 0.3793 | 2.0843 | yes |
| Hidden plots by secret schemes of powerful groups | Blaming the war on others rather than the invader | 0.3121 | 1.8343 | no |
| Hidden plots by secret schemes of powerful groups | Discrediting the West, Diplomacy | 0.2822 | 2.3343 | no |
| Distrust towards Media | Discrediting the West, Diplomacy | 0.2378 | 2.5010 | yes |
| Discrediting the West, Diplomacy | Negative Consequences for the West | 0.2121 | 2.4177 | yes |

### PT — baseline_deepseek_pt_t07

| Gold narrative | Predicted as | bis(TCM) mass | raw mass | same-domain |
|---|---|---|---|---|
| Discrediting the West, Diplomacy | Praise of Russia | 0.3679 | 1.5010 | yes |
| Discrediting the West, Diplomacy | Negative Consequences for the West | 0.3308 | 1.5010 | yes |
| Discrediting Ukraine | Blaming the war on others rather than the invader | 0.3273 | 1.6677 | yes |
| Criticism of climate policies | Criticism of institutions and authorities | 0.2931 | 3.8343 | yes |
| Criticism of institutions and authorities | Criticism of climate movement | 0.2546 | 2.5010 | yes |
| Praise of Russia | Discrediting the West, Diplomacy | 0.2327 | 3.5010 | yes |
| Discrediting Ukraine | Discrediting the West, Diplomacy | 0.2211 | 1.6677 | yes |
| Criticism of institutions and authorities | Green policies are geopolitical instruments | 0.2134 | 2.5010 | yes |

### RU — baseline_deepseek_ru_t00

| Gold narrative | Predicted as | bis(TCM) mass | raw mass | same-domain |
|---|---|---|---|---|
| Hidden plots by secret schemes of powerful groups | Distrust towards Media | 0.2948 | 0.6677 | no |
| Hidden plots by secret schemes of powerful groups | Negative Consequences for the West | 0.2295 | 0.8343 | no |
| Amplifying war-related fears | Russia is the Victim | 0.2211 | 0.5010 | yes |
| Amplifying war-related fears | Blaming the war on others rather than the invader | 0.2134 | 1.4177 | yes |
| Discrediting the West, Diplomacy | Hidden plots by secret schemes of powerful groups | 0.2052 | 1.6677 | no |
| Speculating war outcomes | Discrediting the West, Diplomacy | 0.1901 | 1.4177 | yes |
| Discrediting Ukraine | Blaming the war on others rather than the invader | 0.1859 | 10.2510 | yes |
| Hidden plots by secret schemes of powerful groups | Amplifying war-related fears | 0.1691 | 0.8343 | no |

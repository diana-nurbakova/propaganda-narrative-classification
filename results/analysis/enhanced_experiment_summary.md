# Enhanced Experiment Results Report

_Generated_: 2026-04-17 11:18  
_Experiments evaluated_: **121** of 121

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
| agora_deepseek_bg_t00 | DeepSeek V3 | Agora (intersection) | 5 | 0.606 ± 0.013 | 0.297 ± 0.003 | 0.595 ± 0.010 | 1.000 ± 0.000 | -1.225 ± 0.081 | 0.892 |
| agora_deepseek_bg_t07 | DeepSeek V3 | Agora (intersection) | 5 | 0.599 ± 0.011 | 0.291 ± 0.008 | 0.594 ± 0.011 | 1.000 ± 0.000 | -1.230 ± 0.098 | 0.865 |
| agora_majority_gpt5nano_bg_t00 | GPT-5 Nano | Agora (majority) | 5 | 0.509 ± 0.026 | 0.310 ± 0.033 | 0.575 ± 0.014 | 1.000 ± 0.000 | -1.596 ± 0.145 | 0.654 |
| baseline_deepseek_bg_t00 | DeepSeek V3 | Baseline | 5 | 0.575 ± 0.010 | 0.276 ± 0.007 | 0.564 ± 0.007 | 1.000 ± 0.000 | -1.457 ± 0.060 | 0.891 |
| actor_critic_deepseek_bg_t07 | DeepSeek V3 | Actor-Critic | 5 | 0.490 ± 0.049 | 0.280 ± 0.040 | 0.562 ± 0.015 | 1.000 ± 0.000 | -1.545 ± 0.104 | 0.523 |
| baseline_deepseek_bg_t07 | DeepSeek V3 | Baseline | 5 | 0.565 ± 0.008 | 0.271 ± 0.004 | 0.554 ± 0.004 | 1.000 ± 0.000 | -1.546 ± 0.057 | 0.859 |
| actor_critic_deepseek_bg_t00 | DeepSeek V3 | Actor-Critic | 5 | 0.453 ± 0.039 | 0.291 ± 0.030 | 0.542 ± 0.022 | 1.000 ± 0.000 | -1.633 ± 0.172 | 0.491 |
| mdeberta_baseline_bg_t00 | mDeBERTa v3 (fine-tuned) | mDeBERTa (fine-tuned) | 5 | 0.386 ± 0.063 | 0.253 ± 0.065 | 0.540 ± 0.039 | 1.000 ± 0.000 | -1.653 ± 0.390 | 0.376 |
| mdeberta_originals_only_bg_t00 | mDeBERTa v3 (fine-tuned) | Unknown | 5 | 0.448 ± 0.032 | 0.271 ± 0.032 | 0.532 ± 0.024 | 1.000 ± 0.000 | -1.638 ± 0.131 | 0.457 |
| agora_mistral_bg_t00 | Mistral Large | Agora (intersection) | 5 | 0.483 ± 0.012 | 0.233 ± 0.032 | 0.460 ± 0.004 | 1.000 ± 0.000 | -2.280 ± 0.064 | 0.511 |
| baseline_mistral_bg_t00 | Mistral Large | Baseline | 5 | 0.480 ± 0.019 | 0.207 ± 0.010 | 0.438 ± 0.006 | 1.000 ± 0.000 | -2.975 ± 0.152 | 0.831 |
| actor_critic_mistral_bg_t00 | Mistral Large | Actor-Critic | 5 | 0.474 ± 0.020 | 0.203 ± 0.018 | 0.436 ± 0.009 | 1.000 ± 0.000 | -3.022 ± 0.147 | 0.656 |
| agora_majority_mistral_bg_t00 | Mistral Large | Agora (majority) | 5 | 0.477 ± 0.006 | 0.206 ± 0.006 | 0.432 ± 0.003 | 1.000 ± 0.000 | -3.005 ± 0.027 | 0.840 |
| agora_majority_together_llama33_70b_bg_t00 | Llama 3.3 70B | Agora (majority) | 5 | 0.315 ± 0.019 | 0.197 ± 0.022 | 0.402 ± 0.013 | 1.000 ± 0.000 | -2.698 ± 0.345 | 0.816 |

_Error severity (sub-narrative false positives, mean over runs)_:

| Experiment | Sibling | Same-dom | Cross-dom | Hallucinations |
|---|---|---|---|---|
| agora_deepseek_bg_t00 | 25.03% | 38.13% | 0.00% | 36.84% |
| agora_deepseek_bg_t07 | 25.62% | 39.60% | 0.00% | 34.78% |
| agora_majority_gpt5nano_bg_t00 | 20.75% | 44.54% | 3.50% | 31.21% |
| baseline_deepseek_bg_t00 | 21.92% | 38.37% | 0.00% | 39.71% |
| actor_critic_deepseek_bg_t07 | 24.69% | 41.41% | 0.54% | 33.36% |
| baseline_deepseek_bg_t07 | 21.90% | 38.02% | 0.20% | 39.88% |
| actor_critic_deepseek_bg_t00 | 24.22% | 39.78% | 1.97% | 34.04% |
| mdeberta_baseline_bg_t00 | 6.10% | 38.72% | 10.04% | 45.14% |
| mdeberta_originals_only_bg_t00 | 13.91% | 46.36% | 0.48% | 39.24% |
| agora_mistral_bg_t00 | 15.84% | 46.04% | 0.71% | 37.42% |
| baseline_mistral_bg_t00 | 14.22% | 48.66% | 0.58% | 36.54% |
| actor_critic_mistral_bg_t00 | 14.83% | 47.58% | 0.58% | 37.01% |
| agora_majority_mistral_bg_t00 | 13.96% | 47.89% | 0.57% | 37.58% |
| agora_majority_together_llama33_70b_bg_t00 | 16.31% | 40.34% | 0.00% | 43.35% |

### EN

| Experiment | Model | Method | Runs | F1ₐ narr | F1ₐ sub | hF | HCR | ICM | InterRun (sub) |
|---|---|---|---|---|---|---|---|---|---|
| actor_critic_gemini_en_t07 | Gemini 2.5 Flash | Actor-Critic | 5 | 0.310 ± 0.019 | 0.229 ± 0.024 | 0.490 ± 0.021 | 1.000 ± 0.000 | -2.448 ± 0.255 | 0.467 |
| actor_critic_gpt5nano_en_t07 | GPT-5 Nano | Actor-Critic | 5 | 0.331 ± 0.020 | 0.239 ± 0.041 | 0.478 ± 0.009 | 1.000 ± 0.000 | -2.519 ± 0.100 | 0.358 |
| actor_critic_gemini_en_t00 | Gemini 2.5 Flash | Actor-Critic | 5 | 0.301 ± 0.019 | 0.187 ± 0.038 | 0.471 ± 0.017 | 1.000 ± 0.000 | -2.616 ± 0.086 | 0.464 |
| actor_critic_deepseek_en_t00_evidence | DeepSeek V3 | Actor-Critic | 1 | 0.355 ± 0.000 | 0.179 ± 0.000 | 0.463 ± 0.000 | 1.000 ± 0.000 | -2.380 ± 0.000 | 1.000 |
| actor_critic_deepseek_en_t00 | DeepSeek V3 | Actor-Critic | 5 | 0.347 ± 0.020 | 0.210 ± 0.022 | 0.462 ± 0.014 | 1.000 ± 0.000 | -2.460 ± 0.140 | 0.514 |
| baseline_gpt5nano_en_t00 | GPT-5 Nano | Baseline | 5 | 0.341 ± 0.034 | 0.233 ± 0.024 | 0.455 ± 0.017 | 1.000 ± 0.000 | -2.730 ± 0.200 | 0.555 |
| actor_critic_deepseek_en_t07 | DeepSeek V3 | Actor-Critic | 5 | 0.343 ± 0.042 | 0.199 ± 0.041 | 0.454 ± 0.019 | 1.000 ± 0.000 | -2.506 ± 0.158 | 0.469 |
| actor_critic_gpt5nano_en_t00 | GPT-5 Nano | Actor-Critic | 5 | 0.294 ± 0.018 | 0.171 ± 0.046 | 0.450 ± 0.018 | 1.000 ± 0.000 | -2.778 ± 0.283 | 0.344 |
| agora_7_deepseek_en_t07 | DeepSeek V3 | Agora (7-agent intersection) | 5 | 0.374 ± 0.009 | 0.160 ± 0.016 | 0.449 ± 0.005 | 1.000 ± 0.000 | -2.341 ± 0.086 | 0.789 |
| agora_majority_gpt5nano_en_t07 | GPT-5 Nano | Agora (majority) | 5 | 0.337 ± 0.019 | 0.224 ± 0.030 | 0.447 ± 0.013 | 1.000 ± 0.000 | -2.822 ± 0.144 | 0.589 |
| agora_5_deepseek_en_t00 | DeepSeek V3 | Agora (5-agent intersection) | 5 | 0.380 ± 0.023 | 0.166 ± 0.013 | 0.442 ± 0.010 | 1.000 ± 0.000 | -2.566 ± 0.172 | 0.832 |
| agora_majority_gpt5nano_ru_t00 | GPT-5 Nano | Agora (majority) | 1 | 0.339 ± 0.000 | 0.237 ± 0.000 | 0.441 ± 0.000 | 1.000 ± 0.000 | -3.074 ± 0.000 | 1.000 |
| agora_5_deepseek_en_t07 | DeepSeek V3 | Agora (5-agent intersection) | 5 | 0.357 ± 0.028 | 0.144 ± 0.016 | 0.436 ± 0.015 | 1.000 ± 0.000 | -2.433 ± 0.156 | 0.770 |
| baseline_gpt5nano_en_t07 | GPT-5 Nano | Baseline | 5 | 0.308 ± 0.021 | 0.205 ± 0.018 | 0.430 ± 0.006 | 1.000 ± 0.000 | -3.106 ± 0.099 | 0.589 |
| agora_7_deepseek_en_t00 | DeepSeek V3 | Agora (7-agent intersection) | 5 | 0.348 ± 0.010 | 0.150 ± 0.007 | 0.427 ± 0.008 | 1.000 ± 0.000 | -2.772 ± 0.146 | 0.826 |
| agora_deepseek_en_t07 | DeepSeek V3 | Agora (intersection) | 5 | 0.363 ± 0.020 | 0.157 ± 0.016 | 0.427 ± 0.009 | 1.000 ± 0.000 | -2.746 ± 0.103 | 0.785 |
| baseline_deepseek_en_t00_evidence | DeepSeek V3 | Baseline | 1 | 0.355 ± 0.000 | 0.160 ± 0.000 | 0.427 ± 0.000 | 1.000 ± 0.000 | -2.825 ± 0.000 | 1.000 |
| agora_gemini_en_t07 | Gemini 2.5 Flash | Agora (intersection) | 5 | 0.393 ± 0.037 | 0.224 ± 0.025 | 0.424 ± 0.015 | 1.000 ± 0.000 | -2.845 ± 0.249 | 0.663 |
| actor_critic_gemini_en_t07 | Gemini 2.5 Flash | Actor-Critic | 4 | 0.347 ± 0.038 | 0.231 ± 0.050 | 0.423 ± 0.031 | 1.000 ± 0.000 | -2.934 ± 0.428 | 0.223 |
| mdeberta_baseline_en_t00 | mDeBERTa v3 (fine-tuned) | mDeBERTa (fine-tuned) | 5 | 0.207 ± 0.043 | 0.079 ± 0.018 | 0.422 ± 0.009 | 1.000 ± 0.000 | -2.615 ± 0.182 | 0.292 |
| agora_deepseek_en_t00 | DeepSeek V3 | Agora (intersection) | 5 | 0.349 ± 0.007 | 0.152 ± 0.007 | 0.416 ± 0.011 | 1.000 ± 0.000 | -2.968 ± 0.185 | 0.690 |
| agora_1_deepseek_en_t00 | DeepSeek V3 | Agora (1-agent) | 5 | 0.349 ± 0.008 | 0.163 ± 0.013 | 0.413 ± 0.009 | 1.000 ± 0.000 | -3.216 ± 0.115 | 0.865 |
| agora_7_majority_deepseek_en_t00 | DeepSeek V3 | Agora (7-agent majority) | 5 | 0.348 ± 0.011 | 0.162 ± 0.006 | 0.413 ± 0.006 | 1.000 ± 0.000 | -3.098 ± 0.070 | 0.851 |
| agora_5_majority_deepseek_en_t00 | DeepSeek V3 | Agora (5-agent majority) | 5 | 0.348 ± 0.008 | 0.159 ± 0.009 | 0.413 ± 0.006 | 1.000 ± 0.000 | -3.051 ± 0.037 | 0.851 |
| agora_union_gpt5nano_en_t00 | GPT-5 Nano | Agora (union) | 5 | 0.309 ± 0.026 | 0.219 ± 0.016 | 0.412 ± 0.010 | 1.000 ± 0.000 | -3.772 ± 0.199 | 0.599 |
| agora_majority_deepseek_en_t07 | DeepSeek V3 | Agora (majority) | 5 | 0.351 ± 0.015 | 0.156 ± 0.013 | 0.412 ± 0.009 | 1.000 ± 0.000 | -3.065 ± 0.059 | 0.756 |
| agora_7_majority_deepseek_en_t07 | DeepSeek V3 | Agora (7-agent majority) | 5 | 0.347 ± 0.007 | 0.156 ± 0.009 | 0.410 ± 0.008 | 1.000 ± 0.000 | -3.080 ± 0.095 | 0.802 |
| agora_1_deepseek_en_t07 | DeepSeek V3 | Agora (1-agent) | 5 | 0.346 ± 0.004 | 0.161 ± 0.007 | 0.409 ± 0.009 | 1.000 ± 0.000 | -3.154 ± 0.084 | 0.741 |
| agora_union_gpt5nano_en_t07 | GPT-5 Nano | Agora (union) | 5 | 0.318 ± 0.015 | 0.228 ± 0.022 | 0.409 ± 0.016 | 1.000 ± 0.000 | -3.831 ± 0.236 | 0.606 |
| agora_5_majority_deepseek_en_t07 | DeepSeek V3 | Agora (5-agent majority) | 5 | 0.344 ± 0.021 | 0.156 ± 0.009 | 0.408 ± 0.007 | 1.000 ± 0.000 | -3.081 ± 0.102 | 0.809 |
| agora_majority_deepseek_en_t00 | DeepSeek V3 | Agora (majority) | 5 | 0.343 ± 0.009 | 0.152 ± 0.008 | 0.405 ± 0.006 | 1.000 ± 0.000 | -3.214 ± 0.112 | 0.851 |
| baseline_deepseek_en_t00 | DeepSeek V3 | Baseline | 5 | 0.342 ± 0.013 | 0.150 ± 0.012 | 0.403 ± 0.010 | 1.000 ± 0.000 | -3.143 ± 0.065 | 0.794 |
| baseline_deepseek_en_t07 | DeepSeek V3 | Baseline | 5 | 0.329 ± 0.012 | 0.146 ± 0.013 | 0.399 ± 0.012 | 1.000 ± 0.000 | -3.155 ± 0.174 | 0.731 |
| actor_critic_gemini_en_t00 | Gemini 2.5 Flash | Actor-Critic | 5 | 0.334 ± 0.018 | 0.225 ± 0.043 | 0.394 ± 0.009 | 1.000 ± 0.000 | -3.445 ± 0.280 | 0.306 |
| agora_gemini_en_t00 | Gemini 2.5 Flash | Agora (intersection) | 3 | 0.383 ± 0.014 | 0.221 ± 0.029 | 0.388 ± 0.005 | 1.000 ± 0.000 | -3.308 ± 0.183 | 0.837 |
| mdeberta_originals_only_en_t00 | mDeBERTa v3 (fine-tuned) | Unknown | 5 | 0.265 ± 0.042 | 0.097 ± 0.024 | 0.386 ± 0.032 | 1.000 ± 0.000 | -2.986 ± 0.316 | 0.378 |
| agora_union_deepseek_en_t00 | DeepSeek V3 | Agora (union) | 5 | 0.320 ± 0.010 | 0.148 ± 0.011 | 0.385 ± 0.008 | 1.000 ± 0.000 | -3.597 ± 0.141 | 0.822 |
| actor_critic_together_llama33_70b_en_t07 | Llama 3.3 70B | Actor-Critic | 5 | 0.307 ± 0.024 | 0.157 ± 0.018 | 0.383 ± 0.016 | 1.000 ± 0.000 | -3.625 ± 0.271 | 0.446 |
| agora_5_union_deepseek_en_t00 | DeepSeek V3 | Agora (5-agent union) | 5 | 0.321 ± 0.008 | 0.145 ± 0.005 | 0.381 ± 0.006 | 1.000 ± 0.000 | -3.692 ± 0.148 | 0.815 |
| actor_critic_together_llama33_70b_en_t00 | Llama 3.3 70B | Actor-Critic | 5 | 0.319 ± 0.010 | 0.163 ± 0.024 | 0.380 ± 0.016 | 1.000 ± 0.000 | -3.727 ± 0.238 | 0.491 |
| baseline_gemini_en_t00 | Gemini 2.5 Flash | Baseline | 5 | 0.354 ± 0.012 | 0.197 ± 0.009 | 0.379 ± 0.009 | 1.000 ± 0.000 | -3.780 ± 0.131 | 0.815 |
| agora_7_union_deepseek_en_t00 | DeepSeek V3 | Agora (7-agent union) | 5 | 0.325 ± 0.013 | 0.148 ± 0.010 | 0.378 ± 0.008 | 1.000 ± 0.000 | -3.870 ± 0.063 | 0.859 |
| agora_union_deepseek_en_t07 | DeepSeek V3 | Agora (union) | 5 | 0.307 ± 0.013 | 0.143 ± 0.006 | 0.375 ± 0.007 | 1.000 ± 0.000 | -3.723 ± 0.163 | 0.776 |
| agora_5_union_deepseek_en_t07 | DeepSeek V3 | Agora (5-agent union) | 5 | 0.309 ± 0.015 | 0.144 ± 0.009 | 0.374 ± 0.006 | 1.000 ± 0.000 | -3.818 ± 0.147 | 0.796 |
| baseline_gemini_en_t07 | Gemini 2.5 Flash | Baseline | 1 | 0.367 ± 0.000 | 0.276 ± 0.000 | 0.373 ± 0.000 | 1.000 ± 0.000 | -5.545 ± 0.000 | 1.000 |
| agora_7_union_deepseek_en_t07 | DeepSeek V3 | Agora (7-agent union) | 1 | 0.302 ± 0.000 | 0.146 ± 0.000 | 0.373 ± 0.000 | 1.000 ± 0.000 | -3.803 ± 0.000 | 1.000 |
| agora_mistral_en_t00 | Mistral Large | Agora (intersection) | 5 | 0.325 ± 0.022 | 0.135 ± 0.018 | 0.355 ± 0.012 | 1.000 ± 0.000 | -3.674 ± 0.163 | 0.762 |
| agora_mistral_en_t00_evidence | Mistral Large | Agora (intersection) | 1 | 0.325 ± 0.000 | 0.125 ± 0.000 | 0.354 ± 0.000 | 1.000 ± 0.000 | -3.700 ± 0.000 | 1.000 |
| agora_mistral_en_t07 | Mistral Large | Agora (intersection) | 5 | 0.318 ± 0.008 | 0.129 ± 0.004 | 0.354 ± 0.008 | 1.000 ± 0.000 | -3.653 ± 0.173 | 0.614 |
| agora_together_llama33_70b_en_t07 | Llama 3.3 70B | Agora (intersection) | 5 | 0.300 ± 0.021 | 0.109 ± 0.023 | 0.351 ± 0.012 | 1.000 ± 0.000 | -3.239 ± 0.326 | 0.596 |
| agora_together_llama33_70b_en_t00 | Llama 3.3 70B | Agora (intersection) | 5 | 0.318 ± 0.015 | 0.115 ± 0.006 | 0.343 ± 0.006 | 1.000 ± 0.000 | -3.790 ± 0.096 | 0.749 |
| actor_critic_mistral_en_t00_evidence | Mistral Large | Actor-Critic | 1 | 0.299 ± 0.000 | 0.134 ± 0.000 | 0.342 ± 0.000 | 1.000 ± 0.000 | -3.995 ± 0.000 | 1.000 |
| baseline_mistral_en_t00 | Mistral Large | Baseline | 5 | 0.308 ± 0.005 | 0.130 ± 0.002 | 0.339 ± 0.004 | 1.000 ± 0.000 | -4.166 ± 0.204 | 0.738 |
| agora_majority_mistral_en_t00_evidence | Mistral Large | Agora (majority) | 1 | 0.303 ± 0.000 | 0.129 ± 0.000 | 0.339 ± 0.000 | 1.000 ± 0.000 | -4.263 ± 0.000 | 1.000 |
| agora_majority_mistral_en_t00 | Mistral Large | Agora (majority) | 5 | 0.303 ± 0.021 | 0.130 ± 0.012 | 0.338 ± 0.008 | 1.000 ± 0.000 | -4.202 ± 0.098 | 0.743 |
| baseline_mistral_en_t00_evidence | Mistral Large | Baseline | 1 | 0.312 ± 0.000 | 0.125 ± 0.000 | 0.337 ± 0.000 | 1.000 ± 0.000 | -4.205 ± 0.000 | 1.000 |
| actor_critic_mistral_en_t00 | Mistral Large | Actor-Critic | 5 | 0.298 ± 0.012 | 0.121 ± 0.010 | 0.335 ± 0.008 | 1.000 ± 0.000 | -4.105 ± 0.076 | 0.736 |
| baseline_mistral_en_t07 | Mistral Large | Baseline | 5 | 0.299 ± 0.009 | 0.132 ± 0.019 | 0.334 ± 0.006 | 1.000 ± 0.000 | -4.214 ± 0.242 | 0.617 |
| actor_critic_mistral_en_t07 | Mistral Large | Actor-Critic | 5 | 0.301 ± 0.017 | 0.120 ± 0.008 | 0.333 ± 0.011 | 1.000 ± 0.000 | -4.332 ± 0.276 | 0.699 |
| agora_majority_mistral_en_t07 | Mistral Large | Agora (majority) | 5 | 0.297 ± 0.014 | 0.122 ± 0.006 | 0.332 ± 0.011 | 1.000 ± 0.000 | -4.302 ± 0.198 | 0.711 |
| baseline_together_llama33_70b_en_t07 | Llama 3.3 70B | Baseline | 5 | 0.300 ± 0.009 | 0.114 ± 0.008 | 0.330 ± 0.007 | 1.000 ± 0.000 | -4.236 ± 0.098 | 0.646 |
| agora_majority_together_llama33_70b_en_t07 | Llama 3.3 70B | Agora (majority) | 5 | 0.302 ± 0.014 | 0.119 ± 0.009 | 0.330 ± 0.012 | 1.000 ± 0.000 | -4.242 ± 0.127 | 0.689 |
| agora_majority_together_llama33_70b_en_t00 | Llama 3.3 70B | Agora (majority) | 5 | 0.307 ± 0.016 | 0.119 ± 0.011 | 0.326 ± 0.012 | 1.000 ± 0.000 | -4.340 ± 0.117 | 0.802 |
| agora_union_mistral_en_t00 | Mistral Large | Agora (union) | 5 | 0.290 ± 0.001 | 0.124 ± 0.007 | 0.321 ± 0.007 | 1.000 ± 0.000 | -4.863 ± 0.177 | 0.816 |
| agora_union_mistral_en_t07 | Mistral Large | Agora (union) | 5 | 0.289 ± 0.006 | 0.118 ± 0.006 | 0.318 ± 0.007 | 1.000 ± 0.000 | -4.717 ± 0.285 | 0.766 |
| baseline_together_llama33_70b_en_t00 | Llama 3.3 70B | Baseline | 5 | 0.285 ± 0.013 | 0.105 ± 0.005 | 0.312 ± 0.006 | 1.000 ± 0.000 | -4.449 ± 0.155 | 0.772 |
| agora_union_together_llama33_70b_en_t07 | Llama 3.3 70B | Agora (union) | 5 | 0.276 ± 0.011 | 0.112 ± 0.006 | 0.306 ± 0.005 | 1.000 ± 0.000 | -5.138 ± 0.202 | 0.701 |
| agora_union_together_llama33_70b_en_t00 | Llama 3.3 70B | Agora (union) | 5 | 0.277 ± 0.009 | 0.110 ± 0.003 | 0.301 ± 0.007 | 1.000 ± 0.000 | -4.944 ± 0.206 | 0.794 |

_Error severity (sub-narrative false positives, mean over runs)_:

| Experiment | Sibling | Same-dom | Cross-dom | Hallucinations |
|---|---|---|---|---|
| actor_critic_gemini_en_t07 | 20.79% | 69.22% | 1.11% | 8.87% |
| actor_critic_gpt5nano_en_t07 | 13.21% | 64.65% | 6.81% | 15.32% |
| actor_critic_gemini_en_t00 | 10.66% | 59.00% | 4.59% | 25.75% |
| actor_critic_deepseek_en_t00_evidence | 16.22% | 63.96% | 0.90% | 18.92% |
| actor_critic_deepseek_en_t00 | 13.81% | 70.55% | 0.67% | 14.97% |
| baseline_gpt5nano_en_t00 | 11.57% | 68.44% | 6.59% | 13.41% |
| actor_critic_deepseek_en_t07 | 13.36% | 71.05% | 0.51% | 15.08% |
| actor_critic_gpt5nano_en_t00 | 11.64% | 65.30% | 8.18% | 14.88% |
| agora_7_deepseek_en_t07 | 11.30% | 72.67% | 0.00% | 16.02% |
| agora_majority_gpt5nano_en_t07 | 12.88% | 68.65% | 4.88% | 13.59% |
| agora_5_deepseek_en_t00 | 11.83% | 72.29% | 0.00% | 15.88% |
| agora_majority_gpt5nano_ru_t00 | 14.08% | 64.08% | 7.04% | 14.79% |
| agora_5_deepseek_en_t07 | 11.14% | 71.99% | 0.00% | 16.86% |
| baseline_gpt5nano_en_t07 | 11.98% | 64.48% | 8.44% | 15.09% |
| agora_7_deepseek_en_t00 | 10.87% | 71.74% | 0.00% | 17.39% |
| agora_deepseek_en_t07 | 11.52% | 72.72% | 0.00% | 15.76% |
| baseline_deepseek_en_t00_evidence | 12.05% | 72.89% | 0.00% | 15.06% |
| agora_gemini_en_t07 | 14.24% | 68.70% | 4.49% | 12.57% |
| actor_critic_gemini_en_t07 | 13.81% | 68.05% | 5.71% | 12.43% |
| mdeberta_baseline_en_t00 | 12.25% | 52.78% | 13.87% | 21.10% |
| agora_deepseek_en_t00 | 11.30% | 72.38% | 0.00% | 16.32% |
| agora_1_deepseek_en_t00 | 10.60% | 72.83% | 0.00% | 16.57% |
| agora_7_majority_deepseek_en_t00 | 11.47% | 71.66% | 0.00% | 16.87% |
| agora_5_majority_deepseek_en_t00 | 11.94% | 72.26% | 0.00% | 15.80% |
| agora_union_gpt5nano_en_t00 | 11.25% | 66.19% | 6.66% | 15.91% |
| agora_majority_deepseek_en_t07 | 11.58% | 72.55% | 0.00% | 15.87% |
| agora_7_majority_deepseek_en_t07 | 11.34% | 72.83% | 0.00% | 15.83% |
| agora_1_deepseek_en_t07 | 11.54% | 70.32% | 2.14% | 16.00% |
| agora_union_gpt5nano_en_t07 | 11.26% | 66.49% | 6.48% | 15.77% |
| agora_5_majority_deepseek_en_t07 | 11.33% | 72.67% | 0.00% | 16.00% |
| agora_majority_deepseek_en_t00 | 11.05% | 72.68% | 0.00% | 16.27% |
| baseline_deepseek_en_t00 | 11.31% | 72.42% | 0.00% | 16.26% |
| baseline_deepseek_en_t07 | 10.62% | 69.84% | 2.26% | 17.28% |
| actor_critic_gemini_en_t00 | 13.13% | 66.41% | 6.35% | 14.12% |
| agora_gemini_en_t00 | 12.87% | 67.86% | 5.99% | 13.28% |
| mdeberta_originals_only_en_t00 | 8.34% | 67.14% | 4.96% | 19.55% |
| agora_union_deepseek_en_t00 | 10.63% | 72.75% | 0.29% | 16.33% |
| actor_critic_together_llama33_70b_en_t07 | 9.89% | 73.04% | 0.63% | 16.43% |
| agora_5_union_deepseek_en_t00 | 10.36% | 73.58% | 0.09% | 15.97% |
| actor_critic_together_llama33_70b_en_t00 | 10.39% | 71.14% | 1.34% | 17.13% |
| baseline_gemini_en_t00 | 11.50% | 65.32% | 6.24% | 16.93% |
| agora_7_union_deepseek_en_t00 | 10.10% | 73.84% | 0.09% | 15.97% |
| agora_union_deepseek_en_t07 | 9.96% | 73.13% | 0.28% | 16.63% |
| agora_5_union_deepseek_en_t07 | 9.64% | 72.96% | 0.28% | 17.13% |
| baseline_gemini_en_t07 | 16.92% | 81.54% | 1.54% | 0.00% |
| agora_7_union_deepseek_en_t07 | 9.86% | 73.71% | 0.00% | 16.43% |
| agora_mistral_en_t00 | 9.23% | 72.11% | 0.26% | 18.41% |
| agora_mistral_en_t00_evidence | 9.96% | 74.27% | 0.41% | 15.35% |
| agora_mistral_en_t07 | 9.58% | 69.43% | 2.72% | 18.26% |
| agora_together_llama33_70b_en_t07 | 9.08% | 74.10% | 0.40% | 16.43% |
| agora_together_llama33_70b_en_t00 | 7.80% | 74.17% | 1.31% | 16.73% |
| actor_critic_mistral_en_t00_evidence | 9.92% | 74.79% | 0.41% | 14.88% |
| baseline_mistral_en_t00 | 9.26% | 72.81% | 0.23% | 17.71% |
| agora_majority_mistral_en_t00_evidence | 10.15% | 72.93% | 0.38% | 16.54% |
| agora_majority_mistral_en_t00 | 8.96% | 72.97% | 0.23% | 17.85% |
| baseline_mistral_en_t00_evidence | 9.33% | 73.88% | 0.37% | 16.42% |
| actor_critic_mistral_en_t00 | 9.07% | 72.37% | 0.31% | 18.25% |
| baseline_mistral_en_t07 | 9.57% | 73.68% | 0.30% | 16.45% |
| actor_critic_mistral_en_t07 | 9.40% | 72.10% | 1.45% | 17.04% |
| agora_majority_mistral_en_t07 | 8.85% | 71.69% | 1.44% | 18.01% |
| baseline_together_llama33_70b_en_t07 | 7.48% | 75.01% | 1.31% | 16.21% |
| agora_majority_together_llama33_70b_en_t07 | 7.07% | 75.52% | 1.33% | 16.08% |
| agora_majority_together_llama33_70b_en_t00 | 7.39% | 74.56% | 2.24% | 15.80% |
| agora_union_mistral_en_t00 | 8.88% | 73.64% | 0.40% | 17.08% |
| agora_union_mistral_en_t07 | 8.69% | 73.25% | 0.48% | 17.58% |
| baseline_together_llama33_70b_en_t00 | 7.44% | 73.89% | 2.99% | 15.67% |
| agora_union_together_llama33_70b_en_t07 | 6.89% | 74.58% | 1.46% | 17.07% |
| agora_union_together_llama33_70b_en_t00 | 6.64% | 74.17% | 3.10% | 16.09% |

### HI

| Experiment | Model | Method | Runs | F1ₐ narr | F1ₐ sub | hF | HCR | ICM | InterRun (sub) |
|---|---|---|---|---|---|---|---|---|---|
| agora_majority_gpt5nano_hi_t00 | GPT-5 Nano | Agora (majority) | 5 | 0.400 ± 0.027 | 0.395 ± 0.019 | 0.570 ± 0.013 | 1.000 ± 0.000 | -1.802 ± 0.093 | 0.629 |
| agora_deepseek_hi_t00 | DeepSeek V3 | Agora (intersection) | 5 | 0.462 ± 0.011 | 0.319 ± 0.033 | 0.532 ± 0.006 | 1.000 ± 0.000 | -2.497 ± 0.018 | 0.804 |
| mdeberta_baseline_hi_t00 | mDeBERTa v3 (fine-tuned) | mDeBERTa (fine-tuned) | 5 | 0.309 ± 0.035 | 0.256 ± 0.042 | 0.506 ± 0.032 | 1.000 ± 0.000 | -2.344 ± 0.134 | 0.322 |
| baseline_deepseek_hi_t00 | DeepSeek V3 | Baseline | 5 | 0.430 ± 0.021 | 0.308 ± 0.016 | 0.492 ± 0.014 | 1.000 ± 0.000 | -3.143 ± 0.058 | 0.800 |
| mdeberta_originals_only_hi_t00 | mDeBERTa v3 (fine-tuned) | Unknown | 5 | 0.308 ± 0.039 | 0.248 ± 0.043 | 0.490 ± 0.021 | 1.000 ± 0.000 | -3.080 ± 0.224 | 0.294 |
| actor_critic_deepseek_hi_t00 | DeepSeek V3 | Actor-Critic | 5 | 0.388 ± 0.028 | 0.275 ± 0.018 | 0.489 ± 0.015 | 1.000 ± 0.000 | -2.814 ± 0.171 | 0.569 |
| agora_mistral_hi_t00 | Mistral Large | Agora (intersection) | 5 | 0.348 ± 0.038 | 0.186 ± 0.040 | 0.408 ± 0.014 | 1.000 ± 0.000 | -4.518 ± 0.162 | 0.560 |
| baseline_mistral_hi_t00 | Mistral Large | Baseline | 5 | 0.320 ± 0.023 | 0.148 ± 0.013 | 0.379 ± 0.005 | 1.000 ± 0.000 | -5.452 ± 0.118 | 0.744 |
| agora_majority_mistral_hi_t00 | Mistral Large | Agora (majority) | 5 | 0.319 ± 0.009 | 0.152 ± 0.008 | 0.375 ± 0.005 | 1.000 ± 0.000 | -5.410 ± 0.119 | 0.787 |
| actor_critic_mistral_hi_t00 | Mistral Large | Actor-Critic | 5 | 0.306 ± 0.014 | 0.153 ± 0.016 | 0.369 ± 0.006 | 1.000 ± 0.000 | -5.457 ± 0.099 | 0.737 |
| agora_majority_together_llama33_70b_hi_t00 | Llama 3.3 70B | Agora (majority) | 5 | 0.228 ± 0.035 | 0.141 ± 0.018 | 0.332 ± 0.023 | 1.000 ± 0.000 | -4.301 ± 0.163 | 0.779 |

_Error severity (sub-narrative false positives, mean over runs)_:

| Experiment | Sibling | Same-dom | Cross-dom | Hallucinations |
|---|---|---|---|---|
| agora_majority_gpt5nano_hi_t00 | 17.56% | 17.60% | 0.57% | 64.27% |
| agora_deepseek_hi_t00 | 17.13% | 37.93% | 0.00% | 44.95% |
| mdeberta_baseline_hi_t00 | 7.48% | 51.83% | 5.51% | 35.18% |
| baseline_deepseek_hi_t00 | 15.40% | 38.92% | 0.00% | 45.68% |
| mdeberta_originals_only_hi_t00 | 9.63% | 43.90% | 2.37% | 44.11% |
| actor_critic_deepseek_hi_t00 | 14.12% | 37.65% | 0.00% | 48.22% |
| agora_mistral_hi_t00 | 10.77% | 42.69% | 0.00% | 46.53% |
| baseline_mistral_hi_t00 | 9.99% | 46.78% | 0.00% | 43.23% |
| agora_majority_mistral_hi_t00 | 9.23% | 47.34% | 0.00% | 43.43% |
| actor_critic_mistral_hi_t00 | 9.99% | 46.01% | 0.00% | 44.00% |
| agora_majority_together_llama33_70b_hi_t00 | 10.22% | 43.02% | 0.00% | 46.77% |

### PT

| Experiment | Model | Method | Runs | F1ₐ narr | F1ₐ sub | hF | HCR | ICM | InterRun (sub) |
|---|---|---|---|---|---|---|---|---|---|
| agora_majority_gpt5nano_pt_t00 | GPT-5 Nano | Agora (majority) | 5 | 0.584 ± 0.030 | 0.375 ± 0.073 | 0.677 ± 0.022 | 1.000 ± 0.000 | -0.795 ± 0.113 | 0.624 |
| agora_majority_deepseek_pt_t00 | DeepSeek V3 | Agora (majority) | 5 | 0.548 ± 0.021 | 0.365 ± 0.030 | 0.595 ± 0.013 | 1.000 ± 0.000 | -1.148 ± 0.168 | 0.815 |
| agora_union_deepseek_pt_t00 | DeepSeek V3 | Agora (union) | 5 | 0.546 ± 0.038 | 0.339 ± 0.029 | 0.579 ± 0.021 | 1.000 ± 0.000 | -1.327 ± 0.119 | 0.858 |
| mdeberta_baseline_pt_t00 | mDeBERTa v3 (fine-tuned) | mDeBERTa (fine-tuned) | 5 | 0.462 ± 0.006 | 0.246 ± 0.059 | 0.579 ± 0.016 | 1.000 ± 0.000 | -2.799 ± 0.315 | 0.374 |
| baseline_deepseek_pt_t07 | DeepSeek V3 | Baseline | 5 | 0.504 ± 0.030 | 0.373 ± 0.033 | 0.574 ± 0.020 | 1.000 ± 0.000 | -1.120 ± 0.119 | 0.778 |
| baseline_deepseek_pt_t00 | DeepSeek V3 | Baseline | 5 | 0.510 ± 0.020 | 0.346 ± 0.033 | 0.573 ± 0.010 | 1.000 ± 0.000 | -1.154 ± 0.150 | 0.859 |
| mdeberta_originals_only_pt_t00 | mDeBERTa v3 (fine-tuned) | Unknown | 5 | 0.491 ± 0.035 | 0.325 ± 0.037 | 0.571 ± 0.011 | 1.000 ± 0.000 | -3.721 ± 0.424 | 0.493 |
| agora_deepseek_pt_t00 | DeepSeek V3 | Agora (intersection) | 5 | 0.476 ± 0.038 | 0.340 ± 0.023 | 0.565 ± 0.022 | 1.000 ± 0.000 | -0.943 ± 0.049 | 0.872 |
| actor_critic_deepseek_pt_t00 | DeepSeek V3 | Actor-Critic | 5 | 0.383 ± 0.055 | 0.288 ± 0.033 | 0.544 ± 0.015 | 1.000 ± 0.000 | -1.142 ± 0.183 | 0.585 |
| agora_mistral_pt_t00 | Mistral Large | Agora (intersection) | 5 | 0.464 ± 0.044 | 0.321 ± 0.040 | 0.516 ± 0.023 | 1.000 ± 0.000 | -2.469 ± 0.296 | 0.590 |
| agora_majority_mistral_pt_t00 | Mistral Large | Agora (majority) | 5 | 0.410 ± 0.049 | 0.309 ± 0.024 | 0.478 ± 0.022 | 1.000 ± 0.000 | -3.561 ± 0.286 | 0.815 |
| actor_critic_mistral_pt_t00 | Mistral Large | Actor-Critic | 5 | 0.374 ± 0.019 | 0.281 ± 0.023 | 0.464 ± 0.008 | 1.000 ± 0.000 | -3.462 ± 0.238 | 0.820 |
| baseline_mistral_pt_t00 | Mistral Large | Baseline | 5 | 0.382 ± 0.036 | 0.277 ± 0.023 | 0.459 ± 0.012 | 1.000 ± 0.000 | -3.596 ± 0.278 | 0.736 |
| agora_majority_together_llama33_70b_pt_t00 | Llama 3.3 70B | Agora (majority) | 5 | 0.199 ± 0.010 | 0.335 ± 0.004 | 0.354 ± 0.008 | 1.000 ± 0.000 | -1.539 ± 0.099 | 0.937 |

_Error severity (sub-narrative false positives, mean over runs)_:

| Experiment | Sibling | Same-dom | Cross-dom | Hallucinations |
|---|---|---|---|---|
| agora_majority_gpt5nano_pt_t00 | 17.54% | 41.45% | 0.00% | 41.01% |
| agora_majority_deepseek_pt_t00 | 22.79% | 42.86% | 0.00% | 34.34% |
| agora_union_deepseek_pt_t00 | 20.47% | 43.09% | 0.00% | 36.44% |
| mdeberta_baseline_pt_t00 | 16.27% | 38.72% | 10.41% | 34.60% |
| baseline_deepseek_pt_t07 | 22.98% | 43.97% | 0.00% | 33.06% |
| baseline_deepseek_pt_t00 | 22.55% | 41.66% | 0.00% | 35.79% |
| mdeberta_originals_only_pt_t00 | 15.04% | 44.79% | 1.02% | 39.14% |
| agora_deepseek_pt_t00 | 23.58% | 42.79% | 0.00% | 33.63% |
| actor_critic_deepseek_pt_t00 | 19.22% | 52.54% | 0.51% | 27.73% |
| agora_mistral_pt_t00 | 20.57% | 50.50% | 0.00% | 28.92% |
| agora_majority_mistral_pt_t00 | 17.77% | 55.91% | 0.00% | 26.32% |
| actor_critic_mistral_pt_t00 | 16.53% | 55.55% | 0.00% | 27.93% |
| baseline_mistral_pt_t00 | 16.66% | 55.56% | 0.00% | 27.78% |
| agora_majority_together_llama33_70b_pt_t00 | 17.27% | 64.59% | 0.00% | 18.15% |

### RU

| Experiment | Model | Method | Runs | F1ₐ narr | F1ₐ sub | hF | HCR | ICM | InterRun (sub) |
|---|---|---|---|---|---|---|---|---|---|
| agora_majority_gpt5nano_ru_t00 | GPT-5 Nano | Agora (majority) | 5 | 0.428 ± 0.041 | 0.350 ± 0.037 | 0.580 ± 0.024 | 1.000 ± 0.000 | -2.352 ± 0.183 | 0.644 |
| agora_deepseek_ru_t07 | DeepSeek V3 | Agora (intersection) | 5 | 0.505 ± 0.020 | 0.285 ± 0.020 | 0.550 ± 0.012 | 1.000 ± 0.000 | -2.547 ± 0.187 | 0.804 |
| agora_deepseek_ru_t00 | DeepSeek V3 | Agora (intersection) | 5 | 0.504 ± 0.021 | 0.304 ± 0.018 | 0.546 ± 0.011 | 1.000 ± 0.000 | -2.691 ± 0.103 | 0.864 |
| actor_critic_deepseek_ru_t07 | DeepSeek V3 | Actor-Critic | 5 | 0.451 ± 0.022 | 0.287 ± 0.056 | 0.538 ± 0.023 | 1.000 ± 0.000 | -2.800 ± 0.269 | 0.507 |
| actor_critic_deepseek_ru_t00 | DeepSeek V3 | Actor-Critic | 5 | 0.454 ± 0.021 | 0.275 ± 0.016 | 0.537 ± 0.009 | 1.000 ± 0.000 | -3.014 ± 0.152 | 0.505 |
| baseline_deepseek_ru_t00 | DeepSeek V3 | Baseline | 5 | 0.481 ± 0.018 | 0.269 ± 0.016 | 0.526 ± 0.011 | 1.000 ± 0.000 | -3.048 ± 0.169 | 0.851 |
| baseline_deepseek_ru_t07 | DeepSeek V3 | Baseline | 5 | 0.472 ± 0.009 | 0.259 ± 0.008 | 0.519 ± 0.005 | 1.000 ± 0.000 | -3.053 ± 0.137 | 0.777 |
| mdeberta_baseline_ru_t00 | mDeBERTa v3 (fine-tuned) | mDeBERTa (fine-tuned) | 5 | 0.233 ± 0.054 | 0.159 ± 0.051 | 0.464 ± 0.030 | 1.000 ± 0.000 | -3.636 ± 0.409 | 0.320 |
| agora_mistral_ru_t00 | Mistral Large | Agora (intersection) | 5 | 0.407 ± 0.031 | 0.213 ± 0.024 | 0.446 ± 0.017 | 1.000 ± 0.000 | -4.372 ± 0.269 | 0.435 |
| mdeberta_originals_only_ru_t00 | mDeBERTa v3 (fine-tuned) | Unknown | 5 | 0.305 ± 0.042 | 0.128 ± 0.054 | 0.445 ± 0.027 | 1.000 ± 0.000 | -3.984 ± 0.419 | 0.347 |
| agora_majority_mistral_ru_t00 | Mistral Large | Agora (majority) | 5 | 0.409 ± 0.013 | 0.204 ± 0.010 | 0.418 ± 0.006 | 1.000 ± 0.000 | -5.386 ± 0.182 | 0.807 |
| actor_critic_mistral_ru_t00 | Mistral Large | Actor-Critic | 5 | 0.387 ± 0.017 | 0.204 ± 0.004 | 0.415 ± 0.004 | 1.000 ± 0.000 | -5.480 ± 0.133 | 0.792 |
| baseline_mistral_ru_t00 | Mistral Large | Baseline | 5 | 0.382 ± 0.008 | 0.200 ± 0.009 | 0.409 ± 0.004 | 1.000 ± 0.000 | -5.601 ± 0.139 | 0.799 |
| agora_majority_together_llama33_70b_ru_t00 | Llama 3.3 70B | Agora (majority) | 5 | 0.363 ± 0.009 | 0.206 ± 0.002 | 0.396 ± 0.005 | 1.000 ± 0.000 | -5.152 ± 0.156 | 0.807 |

_Error severity (sub-narrative false positives, mean over runs)_:

| Experiment | Sibling | Same-dom | Cross-dom | Hallucinations |
|---|---|---|---|---|
| agora_majority_gpt5nano_ru_t00 | 21.70% | 47.77% | 4.64% | 25.89% |
| agora_deepseek_ru_t07 | 18.74% | 54.48% | 0.00% | 26.78% |
| agora_deepseek_ru_t00 | 18.79% | 54.85% | 0.00% | 26.37% |
| actor_critic_deepseek_ru_t07 | 19.66% | 52.50% | 1.41% | 26.42% |
| actor_critic_deepseek_ru_t00 | 17.64% | 50.75% | 1.14% | 30.47% |
| baseline_deepseek_ru_t00 | 16.02% | 55.93% | 0.00% | 28.05% |
| baseline_deepseek_ru_t07 | 15.25% | 57.14% | 0.00% | 27.61% |
| mdeberta_baseline_ru_t00 | 9.87% | 56.95% | 6.97% | 26.21% |
| agora_mistral_ru_t00 | 17.43% | 55.99% | 0.00% | 26.58% |
| mdeberta_originals_only_ru_t00 | 14.61% | 59.11% | 0.40% | 25.88% |
| agora_majority_mistral_ru_t00 | 15.79% | 60.41% | 0.42% | 23.37% |
| actor_critic_mistral_ru_t00 | 15.86% | 60.34% | 0.11% | 23.69% |
| baseline_mistral_ru_t00 | 15.69% | 61.44% | 0.00% | 22.87% |
| agora_majority_together_llama33_70b_ru_t00 | 18.04% | 61.93% | 0.35% | 19.68% |

## Pairwise Significance Tests (paired, hF)

| A vs B | n | mean diff | Cohen's d | p (t-test) | p (Wilcoxon) |
|---|---|---|---|---|---|
| actor_critic_deepseek_bg_t00 vs actor_critic_deepseek_bg_t07 | 5 | -0.020 | -1.13 | 0.0642 | 0.1250  |
| actor_critic_deepseek_bg_t00 vs agora_deepseek_bg_t00 | 5 | -0.052 | -2.26 | 0.0072 | 0.0625  |
| actor_critic_deepseek_bg_t00 vs agora_deepseek_bg_t07 | 5 | -0.052 | -3.89 | 0.0010 | 0.0625  |
| actor_critic_deepseek_bg_t00 vs baseline_deepseek_bg_t00 | 5 | -0.022 | -0.79 | 0.1520 | 0.1875  |
| actor_critic_deepseek_bg_t00 vs baseline_deepseek_bg_t07 | 5 | -0.012 | -0.61 | 0.2436 | 0.1875  |
| actor_critic_deepseek_bg_t07 vs agora_deepseek_bg_t00 | 5 | -0.032 | -1.94 | 0.0122 | 0.0625  |
| actor_critic_deepseek_bg_t07 vs agora_deepseek_bg_t07 | 5 | -0.032 | -2.57 | 0.0045 | 0.0625  |
| actor_critic_deepseek_bg_t07 vs baseline_deepseek_bg_t00 | 5 | -0.001 | -0.08 | 0.8622 | 0.6250  |
| actor_critic_deepseek_bg_t07 vs baseline_deepseek_bg_t07 | 5 | +0.008 | +0.53 | 0.3043 | 0.3125  |
| actor_critic_deepseek_en_t00 vs actor_critic_deepseek_en_t07 | 5 | +0.008 | +0.31 | 0.5249 | 0.6250  |
| actor_critic_deepseek_en_t00 vs agora_1_deepseek_en_t00 | 5 | +0.049 | +2.56 | 0.0046 | 0.0625  |
| actor_critic_deepseek_en_t00 vs agora_1_deepseek_en_t07 | 5 | +0.053 | +3.72 | 0.0011 | 0.0625  |
| actor_critic_deepseek_en_t00 vs agora_5_deepseek_en_t00 | 5 | +0.020 | +2.37 | 0.0061 | 0.0625  |
| actor_critic_deepseek_en_t00 vs agora_5_deepseek_en_t07 | 5 | +0.026 | +0.96 | 0.0988 | 0.1250  |
| actor_critic_deepseek_en_t00 vs agora_5_majority_deepseek_en_t00 | 5 | +0.049 | +2.79 | 0.0034 | 0.0625  |
| actor_critic_deepseek_en_t00 vs agora_5_majority_deepseek_en_t07 | 5 | +0.054 | +2.80 | 0.0033 | 0.0625  |
| actor_critic_deepseek_en_t00 vs agora_5_union_deepseek_en_t00 | 5 | +0.082 | +4.73 | 0.0005 | 0.0625  |
| actor_critic_deepseek_en_t00 vs agora_5_union_deepseek_en_t07 | 5 | +0.088 | +4.96 | 0.0004 | 0.0625  |
| actor_critic_deepseek_en_t00 vs agora_7_deepseek_en_t00 | 5 | +0.035 | +1.73 | 0.0180 | 0.0625  |
| actor_critic_deepseek_en_t00 vs agora_7_deepseek_en_t07 | 5 | +0.014 | +0.78 | 0.1560 | 0.1875  |
| actor_critic_deepseek_en_t00 vs agora_7_majority_deepseek_en_t00 | 5 | +0.049 | +3.26 | 0.0019 | 0.0625  |
| actor_critic_deepseek_en_t00 vs agora_7_majority_deepseek_en_t07 | 5 | +0.052 | +2.47 | 0.0052 | 0.0625  |
| actor_critic_deepseek_en_t00 vs agora_7_union_deepseek_en_t00 | 5 | +0.084 | +4.43 | 0.0006 | 0.0625  |
| actor_critic_deepseek_en_t00 vs agora_deepseek_en_t00 | 5 | +0.047 | +1.98 | 0.0114 | 0.0625  |
| actor_critic_deepseek_en_t00 vs agora_deepseek_en_t07 | 5 | +0.035 | +2.46 | 0.0053 | 0.0625  |
| actor_critic_deepseek_en_t00 vs agora_majority_deepseek_en_t00 | 5 | +0.057 | +3.56 | 0.0014 | 0.0625  |
| actor_critic_deepseek_en_t00 vs agora_majority_deepseek_en_t07 | 5 | +0.051 | +3.63 | 0.0013 | 0.0625  |
| actor_critic_deepseek_en_t00 vs agora_union_deepseek_en_t00 | 5 | +0.077 | +3.57 | 0.0013 | 0.0625  |
| actor_critic_deepseek_en_t00 vs agora_union_deepseek_en_t07 | 5 | +0.087 | +5.26 | 0.0003 | 0.0625  |
| actor_critic_deepseek_en_t00 vs baseline_deepseek_en_t00 | 5 | +0.059 | +4.14 | 0.0008 | 0.0625  |
| actor_critic_deepseek_en_t00 vs baseline_deepseek_en_t07 | 5 | +0.063 | +4.23 | 0.0007 | 0.0625  |
| actor_critic_deepseek_en_t07 vs agora_1_deepseek_en_t00 | 5 | +0.041 | +1.60 | 0.0233 | 0.0625  |
| actor_critic_deepseek_en_t07 vs agora_1_deepseek_en_t07 | 5 | +0.045 | +2.04 | 0.0103 | 0.0625  |
| actor_critic_deepseek_en_t07 vs agora_5_deepseek_en_t00 | 5 | +0.012 | +0.50 | 0.3226 | 0.4375  |
| actor_critic_deepseek_en_t07 vs agora_5_deepseek_en_t07 | 5 | +0.018 | +0.65 | 0.2170 | 0.3125  |
| actor_critic_deepseek_en_t07 vs agora_5_majority_deepseek_en_t00 | 5 | +0.041 | +2.58 | 0.0045 | 0.0625  |
| actor_critic_deepseek_en_t07 vs agora_5_majority_deepseek_en_t07 | 5 | +0.046 | +3.11 | 0.0023 | 0.0625  |
| actor_critic_deepseek_en_t07 vs agora_5_union_deepseek_en_t00 | 5 | +0.073 | +5.22 | 0.0003 | 0.0625  |
| actor_critic_deepseek_en_t07 vs agora_5_union_deepseek_en_t07 | 5 | +0.080 | +4.29 | 0.0007 | 0.0625  |
| actor_critic_deepseek_en_t07 vs agora_7_deepseek_en_t00 | 5 | +0.027 | +1.28 | 0.0463 | 0.0625  |
| actor_critic_deepseek_en_t07 vs agora_7_deepseek_en_t07 | 5 | +0.006 | +0.27 | 0.5730 | 0.6250  |
| actor_critic_deepseek_en_t07 vs agora_7_majority_deepseek_en_t00 | 5 | +0.041 | +2.58 | 0.0045 | 0.0625  |
| actor_critic_deepseek_en_t07 vs agora_7_majority_deepseek_en_t07 | 5 | +0.044 | +2.80 | 0.0033 | 0.0625  |
| actor_critic_deepseek_en_t07 vs agora_7_union_deepseek_en_t00 | 5 | +0.076 | +3.47 | 0.0015 | 0.0625  |
| actor_critic_deepseek_en_t07 vs agora_deepseek_en_t00 | 5 | +0.039 | +2.05 | 0.0101 | 0.0625  |
| actor_critic_deepseek_en_t07 vs agora_deepseek_en_t07 | 5 | +0.027 | +1.11 | 0.0676 | 0.0625  |
| actor_critic_deepseek_en_t07 vs agora_majority_deepseek_en_t00 | 5 | +0.049 | +2.04 | 0.0103 | 0.0625  |
| actor_critic_deepseek_en_t07 vs agora_majority_deepseek_en_t07 | 5 | +0.043 | +1.64 | 0.0217 | 0.0625  |
| actor_critic_deepseek_en_t07 vs agora_union_deepseek_en_t00 | 5 | +0.069 | +3.41 | 0.0016 | 0.0625  |
| actor_critic_deepseek_en_t07 vs agora_union_deepseek_en_t07 | 5 | +0.079 | +3.65 | 0.0012 | 0.0625  |
| actor_critic_deepseek_en_t07 vs baseline_deepseek_en_t00 | 5 | +0.051 | +1.87 | 0.0139 | 0.0625  |
| actor_critic_deepseek_en_t07 vs baseline_deepseek_en_t07 | 5 | +0.055 | +2.31 | 0.0066 | 0.0625  |
| actor_critic_deepseek_hi_t00 vs agora_deepseek_hi_t00 | 5 | -0.043 | -2.32 | 0.0066 | 0.0625  |
| actor_critic_deepseek_hi_t00 vs baseline_deepseek_hi_t00 | 5 | -0.003 | -0.10 | 0.8279 | 0.8125  |
| actor_critic_deepseek_pt_t00 vs agora_deepseek_pt_t00 | 5 | -0.021 | -0.78 | 0.1576 | 0.1875  |
| actor_critic_deepseek_pt_t00 vs agora_majority_deepseek_pt_t00 | 5 | -0.051 | -2.86 | 0.0031 | 0.0625  |
| actor_critic_deepseek_pt_t00 vs agora_union_deepseek_pt_t00 | 5 | -0.035 | -1.13 | 0.0652 | 0.1250  |
| actor_critic_deepseek_pt_t00 vs baseline_deepseek_pt_t00 | 5 | -0.029 | -1.47 | 0.0300 | 0.0625  |
| actor_critic_deepseek_pt_t00 vs baseline_deepseek_pt_t07 | 5 | -0.030 | -1.68 | 0.0197 | 0.0625  |
| actor_critic_deepseek_ru_t00 vs actor_critic_deepseek_ru_t07 | 5 | -0.001 | -0.03 | 0.9497 | 0.8125  |
| actor_critic_deepseek_ru_t00 vs agora_deepseek_ru_t00 | 5 | -0.010 | -1.52 | 0.0274 | 0.0625  |
| actor_critic_deepseek_ru_t00 vs agora_deepseek_ru_t07 | 5 | -0.013 | -1.06 | 0.0762 | 0.0625  |
| actor_critic_deepseek_ru_t00 vs baseline_deepseek_ru_t00 | 5 | +0.011 | +0.77 | 0.1599 | 0.1875  |
| actor_critic_deepseek_ru_t00 vs baseline_deepseek_ru_t07 | 5 | +0.018 | +1.34 | 0.0401 | 0.0625  |
| actor_critic_deepseek_ru_t07 vs agora_deepseek_ru_t00 | 5 | -0.009 | -0.33 | 0.5076 | 0.4375  |
| actor_critic_deepseek_ru_t07 vs agora_deepseek_ru_t07 | 5 | -0.013 | -0.41 | 0.4071 | 0.4375  |
| actor_critic_deepseek_ru_t07 vs baseline_deepseek_ru_t00 | 5 | +0.011 | +0.42 | 0.4041 | 0.4375  |
| actor_critic_deepseek_ru_t07 vs baseline_deepseek_ru_t07 | 5 | +0.019 | +0.76 | 0.1656 | 0.1875  |
| actor_critic_gemini_en_t00 vs actor_critic_gemini_en_t00 | 5 | -0.077 | -5.46 | 0.0003 | 0.0625  |
| actor_critic_gemini_en_t00 vs actor_critic_gemini_en_t07 | 5 | -0.019 | -0.69 | 0.1972 | 0.1875  |
| actor_critic_gemini_en_t00 vs agora_gemini_en_t00 | 3 | +0.089 | +5.46 | 0.0110 | 0.2500  |
| actor_critic_gemini_en_t00 vs agora_gemini_en_t07 | 5 | +0.047 | +1.71 | 0.0189 | 0.0625  |
| actor_critic_gemini_en_t00 vs baseline_gemini_en_t00 | 5 | +0.092 | +4.67 | 0.0005 | 0.0625  |
| actor_critic_gemini_en_t07 vs actor_critic_gemini_en_t07 | 4 | -0.063 | -2.31 | 0.0192 | 0.1250  |
| actor_critic_gemini_en_t07 vs agora_gemini_en_t00 | 3 | +0.098 | +3.05 | 0.0341 | 0.2500  |
| actor_critic_gemini_en_t07 vs agora_gemini_en_t07 | 5 | +0.066 | +3.88 | 0.0010 | 0.0625  |
| actor_critic_gemini_en_t07 vs baseline_gemini_en_t00 | 5 | +0.111 | +4.78 | 0.0004 | 0.0625  |
| actor_critic_gpt5nano_en_t00 vs actor_critic_gpt5nano_en_t07 | 5 | -0.028 | -1.08 | 0.0731 | 0.1250  |
| actor_critic_gpt5nano_en_t00 vs agora_majority_gpt5nano_en_t07 | 5 | +0.003 | +0.18 | 0.7101 | 1.0000  |
| actor_critic_gpt5nano_en_t00 vs agora_union_gpt5nano_en_t00 | 5 | +0.038 | +3.01 | 0.0026 | 0.0625  |
| actor_critic_gpt5nano_en_t00 vs agora_union_gpt5nano_en_t07 | 5 | +0.040 | +1.30 | 0.0434 | 0.0625  |
| actor_critic_gpt5nano_en_t00 vs baseline_gpt5nano_en_t00 | 5 | -0.005 | -0.22 | 0.6453 | 1.0000  |
| actor_critic_gpt5nano_en_t00 vs baseline_gpt5nano_en_t07 | 5 | +0.020 | +1.04 | 0.0811 | 0.1250  |
| actor_critic_gpt5nano_en_t07 vs agora_majority_gpt5nano_en_t07 | 5 | +0.031 | +1.64 | 0.0213 | 0.0625  |
| actor_critic_gpt5nano_en_t07 vs agora_union_gpt5nano_en_t00 | 5 | +0.066 | +4.05 | 0.0008 | 0.0625  |
| actor_critic_gpt5nano_en_t07 vs agora_union_gpt5nano_en_t07 | 5 | +0.069 | +4.75 | 0.0004 | 0.0625  |
| actor_critic_gpt5nano_en_t07 vs baseline_gpt5nano_en_t00 | 5 | +0.023 | +1.31 | 0.0426 | 0.1250  |
| actor_critic_gpt5nano_en_t07 vs baseline_gpt5nano_en_t07 | 5 | +0.048 | +4.92 | 0.0004 | 0.0625  |
| actor_critic_mistral_bg_t00 vs agora_majority_mistral_bg_t00 | 5 | +0.005 | +0.75 | 0.1671 | 0.1875  |
| actor_critic_mistral_bg_t00 vs agora_mistral_bg_t00 | 5 | -0.024 | -2.15 | 0.0087 | 0.0625  |
| actor_critic_mistral_bg_t00 vs baseline_mistral_bg_t00 | 5 | -0.001 | -0.13 | 0.7896 | 0.8125  |
| actor_critic_mistral_en_t00 vs actor_critic_mistral_en_t07 | 5 | +0.002 | +0.14 | 0.7724 | 1.0000  |
| actor_critic_mistral_en_t00 vs agora_majority_mistral_en_t00 | 5 | -0.003 | -0.31 | 0.5219 | 0.4375  |
| actor_critic_mistral_en_t00 vs agora_majority_mistral_en_t07 | 5 | +0.003 | +0.25 | 0.6045 | 0.4375  |
| actor_critic_mistral_en_t00 vs agora_mistral_en_t00 | 5 | -0.020 | -1.12 | 0.0658 | 0.1250  |
| actor_critic_mistral_en_t00 vs agora_mistral_en_t07 | 5 | -0.019 | -1.55 | 0.0259 | 0.0625  |
| actor_critic_mistral_en_t00 vs agora_union_mistral_en_t00 | 5 | +0.014 | +1.33 | 0.0413 | 0.1250  |
| actor_critic_mistral_en_t00 vs agora_union_mistral_en_t07 | 5 | +0.017 | +2.04 | 0.0103 | 0.0625  |
| actor_critic_mistral_en_t00 vs baseline_mistral_en_t00 | 5 | -0.004 | -0.49 | 0.3384 | 0.8125  |
| actor_critic_mistral_en_t00 vs baseline_mistral_en_t07 | 5 | +0.001 | +0.08 | 0.8663 | 1.0000  |
| actor_critic_mistral_en_t07 vs agora_majority_mistral_en_t00 | 5 | -0.005 | -0.27 | 0.5759 | 0.8125  |
| actor_critic_mistral_en_t07 vs agora_majority_mistral_en_t07 | 5 | +0.001 | +0.07 | 0.8816 | 0.8125  |
| actor_critic_mistral_en_t07 vs agora_mistral_en_t00 | 5 | -0.022 | -2.12 | 0.0090 | 0.0625  |
| actor_critic_mistral_en_t07 vs agora_mistral_en_t07 | 5 | -0.021 | -1.66 | 0.0208 | 0.0625  |
| actor_critic_mistral_en_t07 vs agora_union_mistral_en_t00 | 5 | +0.012 | +0.78 | 0.1544 | 0.1875  |
| actor_critic_mistral_en_t07 vs agora_union_mistral_en_t07 | 5 | +0.014 | +1.48 | 0.0299 | 0.0625  |
| actor_critic_mistral_en_t07 vs baseline_mistral_en_t00 | 5 | -0.006 | -0.45 | 0.3742 | 0.4375  |
| actor_critic_mistral_en_t07 vs baseline_mistral_en_t07 | 5 | -0.002 | -0.10 | 0.8389 | 0.6250  |
| actor_critic_mistral_hi_t00 vs agora_majority_mistral_hi_t00 | 5 | -0.007 | -0.95 | 0.0997 | 0.1250  |
| actor_critic_mistral_hi_t00 vs agora_mistral_hi_t00 | 5 | -0.039 | -3.95 | 0.0009 | 0.0625  |
| actor_critic_mistral_hi_t00 vs baseline_mistral_hi_t00 | 5 | -0.010 | -0.95 | 0.0997 | 0.1250  |
| actor_critic_mistral_pt_t00 vs agora_majority_mistral_pt_t00 | 5 | -0.014 | -0.47 | 0.3482 | 0.6250  |
| actor_critic_mistral_pt_t00 vs agora_mistral_pt_t00 | 5 | -0.052 | -2.57 | 0.0046 | 0.0625  |
| actor_critic_mistral_pt_t00 vs baseline_mistral_pt_t00 | 5 | +0.004 | +0.28 | 0.5637 | 0.6250  |
| actor_critic_mistral_ru_t00 vs agora_majority_mistral_ru_t00 | 5 | -0.003 | -0.50 | 0.3252 | 0.4375  |
| actor_critic_mistral_ru_t00 vs agora_mistral_ru_t00 | 5 | -0.031 | -1.78 | 0.0164 | 0.0625  |
| actor_critic_mistral_ru_t00 vs baseline_mistral_ru_t00 | 5 | +0.005 | +0.99 | 0.0914 | 0.1250  |
| actor_critic_together_llama33_70b_en_t00 vs actor_critic_together_llama33_70b_en_t07 | 5 | -0.002 | -0.10 | 0.8358 | 1.0000  |
| actor_critic_together_llama33_70b_en_t00 vs agora_majority_together_llama33_70b_en_t00 | 5 | +0.054 | +1.96 | 0.0118 | 0.0625  |
| actor_critic_together_llama33_70b_en_t00 vs agora_majority_together_llama33_70b_en_t07 | 5 | +0.050 | +2.05 | 0.0102 | 0.0625  |
| actor_critic_together_llama33_70b_en_t00 vs agora_together_llama33_70b_en_t00 | 5 | +0.037 | +1.74 | 0.0176 | 0.0625  |
| actor_critic_together_llama33_70b_en_t00 vs agora_together_llama33_70b_en_t07 | 5 | +0.029 | +1.26 | 0.0479 | 0.0625  |
| actor_critic_together_llama33_70b_en_t00 vs agora_union_together_llama33_70b_en_t00 | 5 | +0.079 | +5.75 | 0.0002 | 0.0625  |
| actor_critic_together_llama33_70b_en_t00 vs agora_union_together_llama33_70b_en_t07 | 5 | +0.074 | +4.07 | 0.0008 | 0.0625  |
| actor_critic_together_llama33_70b_en_t00 vs baseline_together_llama33_70b_en_t00 | 5 | +0.068 | +4.06 | 0.0008 | 0.0625  |
| actor_critic_together_llama33_70b_en_t00 vs baseline_together_llama33_70b_en_t07 | 5 | +0.050 | +2.43 | 0.0056 | 0.0625  |
| actor_critic_together_llama33_70b_en_t07 vs agora_majority_together_llama33_70b_en_t00 | 5 | +0.057 | +3.70 | 0.0012 | 0.0625  |
| actor_critic_together_llama33_70b_en_t07 vs agora_majority_together_llama33_70b_en_t07 | 5 | +0.053 | +2.08 | 0.0096 | 0.0625  |
| actor_critic_together_llama33_70b_en_t07 vs agora_together_llama33_70b_en_t00 | 5 | +0.040 | +2.63 | 0.0042 | 0.0625  |
| actor_critic_together_llama33_70b_en_t07 vs agora_together_llama33_70b_en_t07 | 5 | +0.031 | +2.40 | 0.0058 | 0.0625  |
| actor_critic_together_llama33_70b_en_t07 vs agora_union_together_llama33_70b_en_t00 | 5 | +0.081 | +5.91 | 0.0002 | 0.0625  |
| actor_critic_together_llama33_70b_en_t07 vs agora_union_together_llama33_70b_en_t07 | 5 | +0.076 | +5.79 | 0.0002 | 0.0625  |
| actor_critic_together_llama33_70b_en_t07 vs baseline_together_llama33_70b_en_t00 | 5 | +0.070 | +5.70 | 0.0002 | 0.0625  |
| actor_critic_together_llama33_70b_en_t07 vs baseline_together_llama33_70b_en_t07 | 5 | +0.052 | +3.80 | 0.0011 | 0.0625  |
| agora_1_deepseek_en_t00 vs agora_1_deepseek_en_t07 | 5 | +0.004 | +0.30 | 0.5449 | 0.6250  |
| agora_1_deepseek_en_t00 vs agora_5_deepseek_en_t00 | 5 | -0.029 | -2.33 | 0.0064 | 0.0625  |
| agora_1_deepseek_en_t00 vs agora_5_deepseek_en_t07 | 5 | -0.023 | -2.66 | 0.0040 | 0.0625  |
| agora_1_deepseek_en_t00 vs agora_5_majority_deepseek_en_t00 | 5 | +0.000 | +0.02 | 0.9747 | 0.8125  |
| agora_1_deepseek_en_t00 vs agora_5_majority_deepseek_en_t07 | 5 | +0.005 | +0.36 | 0.4653 | 0.6250  |
| agora_1_deepseek_en_t00 vs agora_5_union_deepseek_en_t00 | 5 | +0.032 | +2.31 | 0.0066 | 0.0625  |
| agora_1_deepseek_en_t00 vs agora_5_union_deepseek_en_t07 | 5 | +0.039 | +5.37 | 0.0003 | 0.0625  |
| agora_1_deepseek_en_t00 vs agora_7_deepseek_en_t00 | 5 | -0.014 | -1.21 | 0.0542 | 0.1250  |
| agora_1_deepseek_en_t00 vs agora_7_deepseek_en_t07 | 5 | -0.035 | -6.36 | 0.0001 | 0.0625  |
| agora_1_deepseek_en_t00 vs agora_7_majority_deepseek_en_t00 | 5 | +0.000 | +0.01 | 0.9791 | 1.0000  |
| agora_1_deepseek_en_t00 vs agora_7_majority_deepseek_en_t07 | 5 | +0.003 | +0.25 | 0.5999 | 0.6250  |
| agora_1_deepseek_en_t00 vs agora_7_union_deepseek_en_t00 | 5 | +0.035 | +3.43 | 0.0016 | 0.0625  |
| agora_1_deepseek_en_t00 vs agora_deepseek_en_t00 | 5 | -0.002 | -0.17 | 0.7284 | 0.8125  |
| agora_1_deepseek_en_t00 vs agora_deepseek_en_t07 | 5 | -0.014 | -1.03 | 0.0823 | 0.1250  |
| agora_1_deepseek_en_t00 vs agora_majority_deepseek_en_t00 | 5 | +0.008 | +0.91 | 0.1129 | 0.1250  |
| agora_1_deepseek_en_t00 vs agora_majority_deepseek_en_t07 | 5 | +0.002 | +0.13 | 0.7841 | 0.6250  |
| agora_1_deepseek_en_t00 vs agora_union_deepseek_en_t00 | 5 | +0.028 | +2.89 | 0.0030 | 0.0625  |
| agora_1_deepseek_en_t00 vs agora_union_deepseek_en_t07 | 5 | +0.038 | +3.94 | 0.0009 | 0.0625  |
| agora_1_deepseek_en_t00 vs baseline_deepseek_en_t00 | 5 | +0.010 | +1.29 | 0.0451 | 0.1250  |
| agora_1_deepseek_en_t00 vs baseline_deepseek_en_t07 | 5 | +0.014 | +0.75 | 0.1666 | 0.3125  |
| agora_1_deepseek_en_t07 vs agora_5_deepseek_en_t00 | 5 | -0.033 | -2.75 | 0.0035 | 0.0625  |
| agora_1_deepseek_en_t07 vs agora_5_deepseek_en_t07 | 5 | -0.027 | -1.38 | 0.0371 | 0.1250  |
| agora_1_deepseek_en_t07 vs agora_5_majority_deepseek_en_t00 | 5 | -0.003 | -0.42 | 0.4019 | 0.6250  |
| agora_1_deepseek_en_t07 vs agora_5_majority_deepseek_en_t07 | 5 | +0.001 | +0.07 | 0.8779 | 0.8125  |
| agora_1_deepseek_en_t07 vs agora_5_union_deepseek_en_t00 | 5 | +0.029 | +2.20 | 0.0080 | 0.0625  |
| agora_1_deepseek_en_t07 vs agora_5_union_deepseek_en_t07 | 5 | +0.035 | +3.26 | 0.0019 | 0.0625  |
| agora_1_deepseek_en_t07 vs agora_7_deepseek_en_t00 | 5 | -0.018 | -1.19 | 0.0563 | 0.0625  |
| agora_1_deepseek_en_t07 vs agora_7_deepseek_en_t07 | 5 | -0.039 | -3.26 | 0.0019 | 0.0625  |
| agora_1_deepseek_en_t07 vs agora_7_majority_deepseek_en_t00 | 5 | -0.003 | -0.54 | 0.2918 | 0.3125  |
| agora_1_deepseek_en_t07 vs agora_7_majority_deepseek_en_t07 | 5 | -0.001 | -0.07 | 0.8868 | 1.0000  |
| agora_1_deepseek_en_t07 vs agora_7_union_deepseek_en_t00 | 5 | +0.031 | +1.91 | 0.0131 | 0.0625  |
| agora_1_deepseek_en_t07 vs agora_deepseek_en_t00 | 5 | -0.006 | -0.35 | 0.4723 | 0.6250  |
| agora_1_deepseek_en_t07 vs agora_deepseek_en_t07 | 5 | -0.018 | -1.15 | 0.0618 | 0.1250  |
| agora_1_deepseek_en_t07 vs agora_majority_deepseek_en_t00 | 5 | +0.004 | +0.41 | 0.4161 | 0.6250  |
| agora_1_deepseek_en_t07 vs agora_majority_deepseek_en_t07 | 5 | -0.002 | -0.25 | 0.6040 | 0.8125  |
| agora_1_deepseek_en_t07 vs agora_union_deepseek_en_t00 | 5 | +0.024 | +2.04 | 0.0104 | 0.0625  |
| agora_1_deepseek_en_t07 vs agora_union_deepseek_en_t07 | 5 | +0.035 | +2.23 | 0.0076 | 0.0625  |
| agora_1_deepseek_en_t07 vs baseline_deepseek_en_t00 | 5 | +0.006 | +0.44 | 0.3801 | 0.4375  |
| agora_1_deepseek_en_t07 vs baseline_deepseek_en_t07 | 5 | +0.010 | +0.54 | 0.2957 | 0.3125  |
| agora_5_deepseek_en_t00 vs agora_5_deepseek_en_t07 | 5 | +0.006 | +0.29 | 0.5457 | 0.6250  |
| agora_5_deepseek_en_t00 vs agora_5_majority_deepseek_en_t00 | 5 | +0.029 | +2.09 | 0.0094 | 0.0625  |
| agora_5_deepseek_en_t00 vs agora_5_majority_deepseek_en_t07 | 5 | +0.034 | +2.26 | 0.0072 | 0.0625  |
| agora_5_deepseek_en_t00 vs agora_5_union_deepseek_en_t00 | 5 | +0.061 | +4.40 | 0.0006 | 0.0625  |
| agora_5_deepseek_en_t00 vs agora_5_union_deepseek_en_t07 | 5 | +0.068 | +6.10 | 0.0002 | 0.0625  |
| agora_5_deepseek_en_t00 vs agora_7_deepseek_en_t00 | 5 | +0.015 | +0.90 | 0.1159 | 0.1875  |
| agora_5_deepseek_en_t00 vs agora_7_deepseek_en_t07 | 5 | -0.006 | -0.57 | 0.2735 | 0.4375  |
| agora_5_deepseek_en_t00 vs agora_7_majority_deepseek_en_t00 | 5 | +0.029 | +2.42 | 0.0056 | 0.0625  |
| agora_5_deepseek_en_t00 vs agora_7_majority_deepseek_en_t07 | 5 | +0.032 | +2.07 | 0.0098 | 0.0625  |
| agora_5_deepseek_en_t00 vs agora_7_union_deepseek_en_t00 | 5 | +0.064 | +4.61 | 0.0005 | 0.0625  |
| agora_5_deepseek_en_t00 vs agora_deepseek_en_t00 | 5 | +0.027 | +1.34 | 0.0401 | 0.0625  |
| agora_5_deepseek_en_t00 vs agora_deepseek_en_t07 | 5 | +0.015 | +1.18 | 0.0582 | 0.1250  |
| agora_5_deepseek_en_t00 vs agora_majority_deepseek_en_t00 | 5 | +0.037 | +2.89 | 0.0030 | 0.0625  |
| agora_5_deepseek_en_t00 vs agora_majority_deepseek_en_t07 | 5 | +0.031 | +2.37 | 0.0061 | 0.0625  |
| agora_5_deepseek_en_t00 vs agora_union_deepseek_en_t00 | 5 | +0.057 | +3.34 | 0.0017 | 0.0625  |
| agora_5_deepseek_en_t00 vs agora_union_deepseek_en_t07 | 5 | +0.067 | +6.15 | 0.0002 | 0.0625  |
| agora_5_deepseek_en_t00 vs baseline_deepseek_en_t00 | 5 | +0.039 | +5.18 | 0.0003 | 0.0625  |
| agora_5_deepseek_en_t00 vs baseline_deepseek_en_t07 | 5 | +0.043 | +2.87 | 0.0030 | 0.0625  |
| agora_5_deepseek_en_t07 vs agora_5_majority_deepseek_en_t00 | 5 | +0.023 | +1.47 | 0.0302 | 0.0625  |
| agora_5_deepseek_en_t07 vs agora_5_majority_deepseek_en_t07 | 5 | +0.028 | +1.89 | 0.0135 | 0.0625  |
| agora_5_deepseek_en_t07 vs agora_5_union_deepseek_en_t00 | 5 | +0.056 | +3.25 | 0.0019 | 0.0625  |
| agora_5_deepseek_en_t07 vs agora_5_union_deepseek_en_t07 | 5 | +0.062 | +5.36 | 0.0003 | 0.0625  |
| agora_5_deepseek_en_t07 vs agora_7_deepseek_en_t00 | 5 | +0.009 | +0.67 | 0.2063 | 0.3125  |
| agora_5_deepseek_en_t07 vs agora_7_deepseek_en_t07 | 5 | -0.012 | -1.21 | 0.0535 | 0.1250  |
| agora_5_deepseek_en_t07 vs agora_7_majority_deepseek_en_t00 | 5 | +0.023 | +1.28 | 0.0454 | 0.1250  |
| agora_5_deepseek_en_t07 vs agora_7_majority_deepseek_en_t07 | 5 | +0.026 | +2.13 | 0.0089 | 0.0625  |
| agora_5_deepseek_en_t07 vs agora_7_union_deepseek_en_t00 | 5 | +0.058 | +4.89 | 0.0004 | 0.0625  |
| agora_5_deepseek_en_t07 vs agora_deepseek_en_t00 | 5 | +0.021 | +1.47 | 0.0306 | 0.0625  |
| agora_5_deepseek_en_t07 vs agora_deepseek_en_t07 | 5 | +0.009 | +0.50 | 0.3228 | 0.3125  |
| agora_5_deepseek_en_t07 vs agora_majority_deepseek_en_t00 | 5 | +0.031 | +2.17 | 0.0083 | 0.0625  |
| agora_5_deepseek_en_t07 vs agora_majority_deepseek_en_t07 | 5 | +0.025 | +1.33 | 0.0412 | 0.1250  |
| agora_5_deepseek_en_t07 vs agora_union_deepseek_en_t00 | 5 | +0.051 | +4.51 | 0.0005 | 0.0625  |
| agora_5_deepseek_en_t07 vs agora_union_deepseek_en_t07 | 5 | +0.061 | +4.71 | 0.0005 | 0.0625  |
| agora_5_deepseek_en_t07 vs baseline_deepseek_en_t00 | 5 | +0.033 | +2.25 | 0.0073 | 0.0625  |
| agora_5_deepseek_en_t07 vs baseline_deepseek_en_t07 | 5 | +0.037 | +1.65 | 0.0210 | 0.0625  |
| agora_5_majority_deepseek_en_t00 vs agora_5_majority_deepseek_en_t07 | 5 | +0.004 | +0.65 | 0.2197 | 0.3125  |
| agora_5_majority_deepseek_en_t00 vs agora_5_union_deepseek_en_t00 | 5 | +0.032 | +5.03 | 0.0004 | 0.0625  |
| agora_5_majority_deepseek_en_t00 vs agora_5_union_deepseek_en_t07 | 5 | +0.039 | +5.65 | 0.0002 | 0.0625  |
| agora_5_majority_deepseek_en_t00 vs agora_7_deepseek_en_t00 | 5 | -0.014 | -1.50 | 0.0283 | 0.0625  |
| agora_5_majority_deepseek_en_t00 vs agora_7_deepseek_en_t07 | 5 | -0.036 | -4.21 | 0.0007 | 0.0625  |
| agora_5_majority_deepseek_en_t00 vs agora_7_majority_deepseek_en_t00 | 5 | -0.000 | -0.01 | 0.9908 | 1.0000  |
| agora_5_majority_deepseek_en_t00 vs agora_7_majority_deepseek_en_t07 | 5 | +0.003 | +0.44 | 0.3793 | 0.6250  |
| agora_5_majority_deepseek_en_t00 vs agora_7_union_deepseek_en_t00 | 5 | +0.035 | +2.96 | 0.0027 | 0.0625  |
| agora_5_majority_deepseek_en_t00 vs agora_deepseek_en_t00 | 5 | -0.003 | -0.26 | 0.5912 | 1.0000  |
| agora_5_majority_deepseek_en_t00 vs agora_deepseek_en_t07 | 5 | -0.014 | -1.06 | 0.0769 | 0.1250  |
| agora_5_majority_deepseek_en_t00 vs agora_majority_deepseek_en_t00 | 5 | +0.008 | +0.83 | 0.1385 | 0.1250  |
| agora_5_majority_deepseek_en_t00 vs agora_majority_deepseek_en_t07 | 5 | +0.001 | +0.12 | 0.8023 | 0.6250  |
| agora_5_majority_deepseek_en_t00 vs agora_union_deepseek_en_t00 | 5 | +0.028 | +4.31 | 0.0006 | 0.0625  |
| agora_5_majority_deepseek_en_t00 vs agora_union_deepseek_en_t07 | 5 | +0.038 | +3.19 | 0.0020 | 0.0625  |
| agora_5_majority_deepseek_en_t00 vs baseline_deepseek_en_t00 | 5 | +0.010 | +0.64 | 0.2230 | 0.3125  |
| agora_5_majority_deepseek_en_t00 vs baseline_deepseek_en_t07 | 5 | +0.014 | +0.83 | 0.1377 | 0.1875  |
| agora_5_majority_deepseek_en_t07 vs agora_5_union_deepseek_en_t00 | 5 | +0.028 | +9.78 | 0.0000 | 0.0625  |
| agora_5_majority_deepseek_en_t07 vs agora_5_union_deepseek_en_t07 | 5 | +0.034 | +4.63 | 0.0005 | 0.0625  |
| agora_5_majority_deepseek_en_t07 vs agora_7_deepseek_en_t00 | 5 | -0.019 | -2.68 | 0.0039 | 0.0625  |
| agora_5_majority_deepseek_en_t07 vs agora_7_deepseek_en_t07 | 5 | -0.040 | -5.20 | 0.0003 | 0.0625  |
| agora_5_majority_deepseek_en_t07 vs agora_7_majority_deepseek_en_t00 | 5 | -0.004 | -0.51 | 0.3155 | 0.3125  |
| agora_5_majority_deepseek_en_t07 vs agora_7_majority_deepseek_en_t07 | 5 | -0.002 | -0.38 | 0.4475 | 0.6250  |
| agora_5_majority_deepseek_en_t07 vs agora_7_union_deepseek_en_t00 | 5 | +0.030 | +4.01 | 0.0009 | 0.0625  |
| agora_5_majority_deepseek_en_t07 vs agora_deepseek_en_t00 | 5 | -0.007 | -1.05 | 0.0796 | 0.1250  |
| agora_5_majority_deepseek_en_t07 vs agora_deepseek_en_t07 | 5 | -0.019 | -1.61 | 0.0226 | 0.1250  |
| agora_5_majority_deepseek_en_t07 vs agora_majority_deepseek_en_t00 | 5 | +0.003 | +0.29 | 0.5572 | 0.8125  |
| agora_5_majority_deepseek_en_t07 vs agora_majority_deepseek_en_t07 | 5 | -0.003 | -0.21 | 0.6578 | 0.6250  |
| agora_5_majority_deepseek_en_t07 vs agora_union_deepseek_en_t00 | 5 | +0.023 | +2.92 | 0.0029 | 0.0625  |
| agora_5_majority_deepseek_en_t07 vs agora_union_deepseek_en_t07 | 5 | +0.034 | +4.03 | 0.0008 | 0.0625  |
| agora_5_majority_deepseek_en_t07 vs baseline_deepseek_en_t00 | 5 | +0.005 | +0.34 | 0.4859 | 0.8125  |
| agora_5_majority_deepseek_en_t07 vs baseline_deepseek_en_t07 | 5 | +0.009 | +0.70 | 0.1935 | 0.3125  |
| agora_5_union_deepseek_en_t00 vs agora_5_union_deepseek_en_t07 | 5 | +0.006 | +0.77 | 0.1611 | 0.3125  |
| agora_5_union_deepseek_en_t00 vs agora_7_deepseek_en_t00 | 5 | -0.047 | -5.90 | 0.0002 | 0.0625  |
| agora_5_union_deepseek_en_t00 vs agora_7_deepseek_en_t07 | 5 | -0.068 | -7.60 | 0.0001 | 0.0625  |
| agora_5_union_deepseek_en_t00 vs agora_7_majority_deepseek_en_t00 | 5 | -0.032 | -4.34 | 0.0006 | 0.0625  |
| agora_5_union_deepseek_en_t00 vs agora_7_majority_deepseek_en_t07 | 5 | -0.030 | -4.28 | 0.0007 | 0.0625  |
| agora_5_union_deepseek_en_t00 vs agora_7_union_deepseek_en_t00 | 5 | +0.002 | +0.27 | 0.5733 | 0.8125  |
| agora_5_union_deepseek_en_t00 vs agora_deepseek_en_t00 | 5 | -0.035 | -4.23 | 0.0007 | 0.0625  |
| agora_5_union_deepseek_en_t00 vs agora_deepseek_en_t07 | 5 | -0.046 | -4.30 | 0.0007 | 0.0625  |
| agora_5_union_deepseek_en_t00 vs agora_majority_deepseek_en_t00 | 5 | -0.025 | -2.35 | 0.0063 | 0.0625  |
| agora_5_union_deepseek_en_t00 vs agora_majority_deepseek_en_t07 | 5 | -0.031 | -2.25 | 0.0073 | 0.0625  |
| agora_5_union_deepseek_en_t00 vs agora_union_deepseek_en_t00 | 5 | -0.004 | -0.46 | 0.3586 | 0.3750  |
| agora_5_union_deepseek_en_t00 vs agora_union_deepseek_en_t07 | 5 | +0.006 | +0.65 | 0.2226 | 0.4375  |
| agora_5_union_deepseek_en_t00 vs baseline_deepseek_en_t00 | 5 | -0.023 | -1.50 | 0.0284 | 0.0625  |
| agora_5_union_deepseek_en_t00 vs baseline_deepseek_en_t07 | 5 | -0.018 | -1.50 | 0.0285 | 0.0625  |
| agora_5_union_deepseek_en_t07 vs agora_7_deepseek_en_t00 | 5 | -0.053 | -5.11 | 0.0003 | 0.0625  |
| agora_5_union_deepseek_en_t07 vs agora_7_deepseek_en_t07 | 5 | -0.074 | -23.25 | 0.0000 | 0.0625  |
| agora_5_union_deepseek_en_t07 vs agora_7_majority_deepseek_en_t00 | 5 | -0.039 | -4.96 | 0.0004 | 0.0625  |
| agora_5_union_deepseek_en_t07 vs agora_7_majority_deepseek_en_t07 | 5 | -0.036 | -7.31 | 0.0001 | 0.0625  |
| agora_5_union_deepseek_en_t07 vs agora_7_union_deepseek_en_t00 | 5 | -0.004 | -0.45 | 0.3676 | 0.4375  |
| agora_5_union_deepseek_en_t07 vs agora_deepseek_en_t00 | 5 | -0.041 | -3.50 | 0.0014 | 0.0625  |
| agora_5_union_deepseek_en_t07 vs agora_deepseek_en_t07 | 5 | -0.053 | -3.99 | 0.0009 | 0.0625  |
| agora_5_union_deepseek_en_t07 vs agora_majority_deepseek_en_t00 | 5 | -0.031 | -3.24 | 0.0019 | 0.0625  |
| agora_5_union_deepseek_en_t07 vs agora_majority_deepseek_en_t07 | 5 | -0.037 | -2.87 | 0.0030 | 0.0625  |
| agora_5_union_deepseek_en_t07 vs agora_union_deepseek_en_t00 | 5 | -0.011 | -1.31 | 0.0424 | 0.1250  |
| agora_5_union_deepseek_en_t07 vs agora_union_deepseek_en_t07 | 5 | -0.001 | -0.07 | 0.8811 | 0.8125  |
| agora_5_union_deepseek_en_t07 vs baseline_deepseek_en_t00 | 5 | -0.029 | -2.81 | 0.0033 | 0.0625  |
| agora_5_union_deepseek_en_t07 vs baseline_deepseek_en_t07 | 5 | -0.025 | -1.48 | 0.0298 | 0.0625  |
| agora_7_deepseek_en_t00 vs agora_7_deepseek_en_t07 | 5 | -0.021 | -2.44 | 0.0055 | 0.0625  |
| agora_7_deepseek_en_t00 vs agora_7_majority_deepseek_en_t00 | 5 | +0.014 | +1.21 | 0.0534 | 0.0625  |
| agora_7_deepseek_en_t00 vs agora_7_majority_deepseek_en_t07 | 5 | +0.017 | +1.80 | 0.0157 | 0.0625  |
| agora_7_deepseek_en_t00 vs agora_7_union_deepseek_en_t00 | 5 | +0.049 | +8.25 | 0.0001 | 0.0625  |
| agora_7_deepseek_en_t00 vs agora_deepseek_en_t00 | 5 | +0.012 | +2.54 | 0.0047 | 0.0625  |
| agora_7_deepseek_en_t00 vs agora_deepseek_en_t07 | 5 | +0.000 | +0.02 | 0.9608 | 1.0000  |
| agora_7_deepseek_en_t00 vs agora_majority_deepseek_en_t00 | 5 | +0.022 | +3.15 | 0.0021 | 0.0625  |
| agora_7_deepseek_en_t00 vs agora_majority_deepseek_en_t07 | 5 | +0.016 | +1.35 | 0.0395 | 0.0625  |
| agora_7_deepseek_en_t00 vs agora_union_deepseek_en_t00 | 5 | +0.042 | +6.54 | 0.0001 | 0.0625  |
| agora_7_deepseek_en_t00 vs agora_union_deepseek_en_t07 | 5 | +0.052 | +6.09 | 0.0002 | 0.0625  |
| agora_7_deepseek_en_t00 vs baseline_deepseek_en_t00 | 5 | +0.024 | +1.69 | 0.0195 | 0.0625  |
| agora_7_deepseek_en_t00 vs baseline_deepseek_en_t07 | 5 | +0.028 | +2.35 | 0.0062 | 0.0625  |
| agora_7_deepseek_en_t07 vs agora_7_majority_deepseek_en_t00 | 5 | +0.036 | +3.68 | 0.0012 | 0.0625  |
| agora_7_deepseek_en_t07 vs agora_7_majority_deepseek_en_t07 | 5 | +0.038 | +5.78 | 0.0002 | 0.0625  |
| agora_7_deepseek_en_t07 vs agora_7_union_deepseek_en_t00 | 5 | +0.070 | +11.08 | 0.0000 | 0.0625  |
| agora_7_deepseek_en_t07 vs agora_deepseek_en_t00 | 5 | +0.033 | +2.99 | 0.0026 | 0.0625  |
| agora_7_deepseek_en_t07 vs agora_deepseek_en_t07 | 5 | +0.021 | +1.92 | 0.0127 | 0.0625  |
| agora_7_deepseek_en_t07 vs agora_majority_deepseek_en_t00 | 5 | +0.043 | +5.43 | 0.0003 | 0.0625  |
| agora_7_deepseek_en_t07 vs agora_majority_deepseek_en_t07 | 5 | +0.037 | +3.06 | 0.0024 | 0.0625  |
| agora_7_deepseek_en_t07 vs agora_union_deepseek_en_t00 | 5 | +0.064 | +8.02 | 0.0001 | 0.0625  |
| agora_7_deepseek_en_t07 vs agora_union_deepseek_en_t07 | 5 | +0.074 | +12.98 | 0.0000 | 0.0625  |
| agora_7_deepseek_en_t07 vs baseline_deepseek_en_t00 | 5 | +0.045 | +5.37 | 0.0003 | 0.0625  |
| agora_7_deepseek_en_t07 vs baseline_deepseek_en_t07 | 5 | +0.049 | +3.27 | 0.0019 | 0.0625  |
| agora_7_majority_deepseek_en_t00 vs agora_7_majority_deepseek_en_t07 | 5 | +0.003 | +0.31 | 0.5218 | 0.6250  |
| agora_7_majority_deepseek_en_t00 vs agora_7_union_deepseek_en_t00 | 5 | +0.035 | +2.62 | 0.0043 | 0.0625  |
| agora_7_majority_deepseek_en_t00 vs agora_deepseek_en_t00 | 5 | -0.003 | -0.20 | 0.6767 | 1.0000  |
| agora_7_majority_deepseek_en_t00 vs agora_deepseek_en_t07 | 5 | -0.014 | -1.04 | 0.0816 | 0.1250  |
| agora_7_majority_deepseek_en_t00 vs agora_majority_deepseek_en_t00 | 5 | +0.008 | +0.75 | 0.1682 | 0.1250  |
| agora_7_majority_deepseek_en_t00 vs agora_majority_deepseek_en_t07 | 5 | +0.001 | +0.12 | 0.7940 | 1.0000  |
| agora_7_majority_deepseek_en_t00 vs agora_union_deepseek_en_t00 | 5 | +0.028 | +2.93 | 0.0028 | 0.0625  |
| agora_7_majority_deepseek_en_t00 vs agora_union_deepseek_en_t07 | 5 | +0.038 | +3.01 | 0.0026 | 0.0625  |
| agora_7_majority_deepseek_en_t00 vs baseline_deepseek_en_t00 | 5 | +0.010 | +0.66 | 0.2135 | 0.4375  |
| agora_7_majority_deepseek_en_t00 vs baseline_deepseek_en_t07 | 5 | +0.014 | +0.83 | 0.1361 | 0.3125  |
| agora_7_majority_deepseek_en_t07 vs agora_7_union_deepseek_en_t00 | 5 | +0.032 | +3.28 | 0.0018 | 0.0625  |
| agora_7_majority_deepseek_en_t07 vs agora_deepseek_en_t00 | 5 | -0.005 | -0.59 | 0.2578 | 0.3125  |
| agora_7_majority_deepseek_en_t07 vs agora_deepseek_en_t07 | 5 | -0.017 | -1.13 | 0.0643 | 0.1250  |
| agora_7_majority_deepseek_en_t07 vs agora_majority_deepseek_en_t00 | 5 | +0.005 | +0.44 | 0.3825 | 0.4375  |
| agora_7_majority_deepseek_en_t07 vs agora_majority_deepseek_en_t07 | 5 | -0.001 | -0.08 | 0.8658 | 0.6250  |
| agora_7_majority_deepseek_en_t07 vs agora_union_deepseek_en_t00 | 5 | +0.025 | +3.90 | 0.0009 | 0.0625  |
| agora_7_majority_deepseek_en_t07 vs agora_union_deepseek_en_t07 | 5 | +0.035 | +3.46 | 0.0015 | 0.0625  |
| agora_7_majority_deepseek_en_t07 vs baseline_deepseek_en_t00 | 5 | +0.007 | +0.47 | 0.3494 | 0.6250  |
| agora_7_majority_deepseek_en_t07 vs baseline_deepseek_en_t07 | 5 | +0.011 | +0.64 | 0.2284 | 0.4375  |
| agora_7_union_deepseek_en_t00 vs agora_deepseek_en_t00 | 5 | -0.037 | -4.15 | 0.0007 | 0.0625  |
| agora_7_union_deepseek_en_t00 vs agora_deepseek_en_t07 | 5 | -0.049 | -6.17 | 0.0002 | 0.0625  |
| agora_7_union_deepseek_en_t00 vs agora_majority_deepseek_en_t00 | 5 | -0.027 | -3.09 | 0.0023 | 0.0625  |
| agora_7_union_deepseek_en_t00 vs agora_majority_deepseek_en_t07 | 5 | -0.033 | -2.44 | 0.0055 | 0.0625  |
| agora_7_union_deepseek_en_t00 vs agora_union_deepseek_en_t00 | 5 | -0.007 | -0.68 | 0.2025 | 0.1875  |
| agora_7_union_deepseek_en_t00 vs agora_union_deepseek_en_t07 | 5 | +0.003 | +1.02 | 0.0849 | 0.1250  |
| agora_7_union_deepseek_en_t00 vs baseline_deepseek_en_t00 | 5 | -0.025 | -2.35 | 0.0062 | 0.0625  |
| agora_7_union_deepseek_en_t00 vs baseline_deepseek_en_t07 | 5 | -0.021 | -1.90 | 0.0133 | 0.0625  |
| agora_deepseek_bg_t00 vs agora_deepseek_bg_t07 | 5 | +0.001 | +0.05 | 0.9122 | 1.0000  |
| agora_deepseek_bg_t00 vs baseline_deepseek_bg_t00 | 5 | +0.031 | +2.69 | 0.0038 | 0.0625  |
| agora_deepseek_bg_t00 vs baseline_deepseek_bg_t07 | 5 | +0.040 | +5.36 | 0.0003 | 0.0625  |
| agora_deepseek_bg_t07 vs baseline_deepseek_bg_t00 | 5 | +0.030 | +2.00 | 0.0110 | 0.0625  |
| agora_deepseek_bg_t07 vs baseline_deepseek_bg_t07 | 5 | +0.040 | +4.83 | 0.0004 | 0.0625  |
| agora_deepseek_en_t00 vs agora_deepseek_en_t07 | 5 | -0.012 | -0.93 | 0.1074 | 0.1250  |
| agora_deepseek_en_t00 vs agora_majority_deepseek_en_t00 | 5 | +0.010 | +0.93 | 0.1065 | 0.1250  |
| agora_deepseek_en_t00 vs agora_majority_deepseek_en_t07 | 5 | +0.004 | +0.26 | 0.5949 | 0.8125  |
| agora_deepseek_en_t00 vs agora_union_deepseek_en_t00 | 5 | +0.030 | +4.55 | 0.0005 | 0.0625  |
| agora_deepseek_en_t00 vs agora_union_deepseek_en_t07 | 5 | +0.041 | +3.48 | 0.0015 | 0.0625  |
| agora_deepseek_en_t00 vs baseline_deepseek_en_t00 | 5 | +0.012 | +0.68 | 0.2053 | 0.3125  |
| agora_deepseek_en_t00 vs baseline_deepseek_en_t07 | 5 | +0.016 | +1.09 | 0.0721 | 0.1250  |
| agora_deepseek_en_t07 vs agora_majority_deepseek_en_t00 | 5 | +0.022 | +2.89 | 0.0030 | 0.0625  |
| agora_deepseek_en_t07 vs agora_majority_deepseek_en_t07 | 5 | +0.016 | +1.56 | 0.0252 | 0.0625  |
| agora_deepseek_en_t07 vs agora_union_deepseek_en_t00 | 5 | +0.042 | +3.20 | 0.0020 | 0.0625  |
| agora_deepseek_en_t07 vs agora_union_deepseek_en_t07 | 5 | +0.052 | +6.46 | 0.0001 | 0.0625  |
| agora_deepseek_en_t07 vs baseline_deepseek_en_t00 | 5 | +0.024 | +2.10 | 0.0093 | 0.0625  |
| agora_deepseek_en_t07 vs baseline_deepseek_en_t07 | 5 | +0.028 | +4.80 | 0.0004 | 0.0625  |
| agora_deepseek_hi_t00 vs baseline_deepseek_hi_t00 | 5 | +0.040 | +3.07 | 0.0023 | 0.0625  |
| agora_deepseek_pt_t00 vs agora_majority_deepseek_pt_t00 | 5 | -0.030 | -0.91 | 0.1123 | 0.1250  |
| agora_deepseek_pt_t00 vs agora_union_deepseek_pt_t00 | 5 | -0.014 | -0.35 | 0.4740 | 0.4375  |
| agora_deepseek_pt_t00 vs baseline_deepseek_pt_t00 | 5 | -0.008 | -0.25 | 0.6028 | 0.8125  |
| agora_deepseek_pt_t00 vs baseline_deepseek_pt_t07 | 5 | -0.009 | -0.24 | 0.6262 | 0.6250  |
| agora_deepseek_ru_t00 vs agora_deepseek_ru_t07 | 5 | -0.004 | -0.22 | 0.6547 | 0.8125  |
| agora_deepseek_ru_t00 vs baseline_deepseek_ru_t00 | 5 | +0.020 | +1.07 | 0.0744 | 0.1250  |
| agora_deepseek_ru_t00 vs baseline_deepseek_ru_t07 | 5 | +0.028 | +1.96 | 0.0118 | 0.0625  |
| agora_deepseek_ru_t07 vs baseline_deepseek_ru_t00 | 5 | +0.024 | +3.95 | 0.0009 | 0.0625  |
| agora_deepseek_ru_t07 vs baseline_deepseek_ru_t07 | 5 | +0.032 | +2.16 | 0.0085 | 0.0625  |
| agora_gemini_en_t00 vs agora_gemini_en_t07 | 3 | -0.028 | -1.73 | 0.0953 | 0.2500  |
| agora_gemini_en_t00 vs baseline_gemini_en_t00 | 3 | +0.011 | +1.35 | 0.1446 | 0.2500  |
| agora_gemini_en_t07 vs baseline_gemini_en_t00 | 5 | +0.045 | +2.27 | 0.0071 | 0.0625  |
| agora_majority_deepseek_en_t00 vs agora_majority_deepseek_en_t07 | 5 | -0.006 | -1.18 | 0.0576 | 0.0625  |
| agora_majority_deepseek_en_t00 vs agora_union_deepseek_en_t00 | 5 | +0.020 | +2.63 | 0.0042 | 0.0625  |
| agora_majority_deepseek_en_t00 vs agora_union_deepseek_en_t07 | 5 | +0.030 | +3.25 | 0.0019 | 0.0625  |
| agora_majority_deepseek_en_t00 vs baseline_deepseek_en_t00 | 5 | +0.002 | +0.20 | 0.6767 | 0.6250  |
| agora_majority_deepseek_en_t00 vs baseline_deepseek_en_t07 | 5 | +0.006 | +0.48 | 0.3398 | 0.4375  |
| agora_majority_deepseek_en_t07 vs agora_union_deepseek_en_t00 | 5 | +0.027 | +2.28 | 0.0069 | 0.0625  |
| agora_majority_deepseek_en_t07 vs agora_union_deepseek_en_t07 | 5 | +0.037 | +2.70 | 0.0038 | 0.0625  |
| agora_majority_deepseek_en_t07 vs baseline_deepseek_en_t00 | 5 | +0.008 | +0.68 | 0.2005 | 0.1875  |
| agora_majority_deepseek_en_t07 vs baseline_deepseek_en_t07 | 5 | +0.013 | +0.83 | 0.1365 | 0.1250  |
| agora_majority_deepseek_pt_t00 vs agora_union_deepseek_pt_t00 | 5 | +0.017 | +1.07 | 0.0758 | 0.0625  |
| agora_majority_deepseek_pt_t00 vs baseline_deepseek_pt_t00 | 5 | +0.023 | +1.83 | 0.0149 | 0.0625  |
| agora_majority_deepseek_pt_t00 vs baseline_deepseek_pt_t07 | 5 | +0.022 | +1.09 | 0.0717 | 0.1250  |
| agora_majority_gpt5nano_en_t07 vs agora_union_gpt5nano_en_t00 | 5 | +0.035 | +2.32 | 0.0066 | 0.0625  |
| agora_majority_gpt5nano_en_t07 vs agora_union_gpt5nano_en_t07 | 5 | +0.038 | +1.71 | 0.0188 | 0.0625  |
| agora_majority_gpt5nano_en_t07 vs baseline_gpt5nano_en_t00 | 5 | -0.008 | -0.38 | 0.4441 | 0.6250  |
| agora_majority_gpt5nano_en_t07 vs baseline_gpt5nano_en_t07 | 5 | +0.017 | +1.61 | 0.0228 | 0.0625  |
| agora_majority_mistral_bg_t00 vs agora_mistral_bg_t00 | 5 | -0.028 | -4.75 | 0.0004 | 0.0625  |
| agora_majority_mistral_bg_t00 vs baseline_mistral_bg_t00 | 5 | -0.006 | -0.86 | 0.1268 | 0.0625  |
| agora_majority_mistral_en_t00 vs agora_majority_mistral_en_t07 | 5 | +0.006 | +0.74 | 0.1715 | 0.3125  |
| agora_majority_mistral_en_t00 vs agora_mistral_en_t00 | 5 | -0.017 | -0.90 | 0.1143 | 0.1875  |
| agora_majority_mistral_en_t00 vs agora_mistral_en_t07 | 5 | -0.016 | -1.45 | 0.0318 | 0.0625  |
| agora_majority_mistral_en_t00 vs agora_union_mistral_en_t00 | 5 | +0.017 | +1.80 | 0.0158 | 0.0625  |
| agora_majority_mistral_en_t00 vs agora_union_mistral_en_t07 | 5 | +0.019 | +1.54 | 0.0262 | 0.0625  |
| agora_majority_mistral_en_t00 vs baseline_mistral_en_t00 | 5 | -0.001 | -0.20 | 0.6776 | 0.8125  |
| agora_majority_mistral_en_t00 vs baseline_mistral_en_t07 | 5 | +0.004 | +0.52 | 0.3076 | 0.4375  |
| agora_majority_mistral_en_t07 vs agora_mistral_en_t00 | 5 | -0.024 | -1.07 | 0.0743 | 0.1250  |
| agora_majority_mistral_en_t07 vs agora_mistral_en_t07 | 5 | -0.022 | -2.29 | 0.0069 | 0.0625  |
| agora_majority_mistral_en_t07 vs agora_union_mistral_en_t00 | 5 | +0.011 | +0.66 | 0.2146 | 0.3125  |
| agora_majority_mistral_en_t07 vs agora_union_mistral_en_t07 | 5 | +0.013 | +0.88 | 0.1199 | 0.1250  |
| agora_majority_mistral_en_t07 vs baseline_mistral_en_t00 | 5 | -0.008 | -0.62 | 0.2400 | 0.8125  |
| agora_majority_mistral_en_t07 vs baseline_mistral_en_t07 | 5 | -0.003 | -0.21 | 0.6593 | 1.0000  |
| agora_majority_mistral_hi_t00 vs agora_mistral_hi_t00 | 5 | -0.032 | -2.54 | 0.0047 | 0.0625  |
| agora_majority_mistral_hi_t00 vs baseline_mistral_hi_t00 | 5 | -0.003 | -0.51 | 0.3160 | 0.3125  |
| agora_majority_mistral_pt_t00 vs agora_mistral_pt_t00 | 5 | -0.038 | -1.00 | 0.0898 | 0.1250  |
| agora_majority_mistral_pt_t00 vs baseline_mistral_pt_t00 | 5 | +0.019 | +0.82 | 0.1408 | 0.1875  |
| agora_majority_mistral_ru_t00 vs agora_mistral_ru_t00 | 5 | -0.028 | -1.33 | 0.0406 | 0.0625  |
| agora_majority_mistral_ru_t00 vs baseline_mistral_ru_t00 | 5 | +0.009 | +1.05 | 0.0783 | 0.1250  |
| agora_majority_together_llama33_70b_en_t00 vs agora_majority_together_llama33_70b_en_t07 | 5 | -0.004 | -0.26 | 0.5873 | 0.6250  |
| agora_majority_together_llama33_70b_en_t00 vs agora_together_llama33_70b_en_t00 | 5 | -0.017 | -2.23 | 0.0076 | 0.0625  |
| agora_majority_together_llama33_70b_en_t00 vs agora_together_llama33_70b_en_t07 | 5 | -0.025 | -2.40 | 0.0058 | 0.0625  |
| agora_majority_together_llama33_70b_en_t00 vs agora_union_together_llama33_70b_en_t00 | 5 | +0.025 | +1.53 | 0.0266 | 0.0625  |
| agora_majority_together_llama33_70b_en_t00 vs agora_union_together_llama33_70b_en_t07 | 5 | +0.020 | +1.84 | 0.0148 | 0.0625  |
| agora_majority_together_llama33_70b_en_t00 vs baseline_together_llama33_70b_en_t00 | 5 | +0.013 | +0.99 | 0.0902 | 0.1875  |
| agora_majority_together_llama33_70b_en_t00 vs baseline_together_llama33_70b_en_t07 | 5 | -0.005 | -0.47 | 0.3502 | 0.6250  |
| agora_majority_together_llama33_70b_en_t07 vs agora_together_llama33_70b_en_t00 | 5 | -0.013 | -1.22 | 0.0525 | 0.1250  |
| agora_majority_together_llama33_70b_en_t07 vs agora_together_llama33_70b_en_t07 | 5 | -0.021 | -1.01 | 0.0868 | 0.1250  |
| agora_majority_together_llama33_70b_en_t07 vs agora_union_together_llama33_70b_en_t00 | 5 | +0.029 | +1.73 | 0.0180 | 0.0625  |
| agora_majority_together_llama33_70b_en_t07 vs agora_union_together_llama33_70b_en_t07 | 5 | +0.024 | +1.72 | 0.0182 | 0.0625  |
| agora_majority_together_llama33_70b_en_t07 vs baseline_together_llama33_70b_en_t00 | 5 | +0.017 | +1.05 | 0.0789 | 0.0625  |
| agora_majority_together_llama33_70b_en_t07 vs baseline_together_llama33_70b_en_t07 | 5 | -0.001 | -0.06 | 0.9010 | 0.6250  |
| agora_mistral_bg_t00 vs baseline_mistral_bg_t00 | 5 | +0.022 | +6.02 | 0.0002 | 0.0625  |
| agora_mistral_en_t00 vs agora_mistral_en_t07 | 5 | +0.001 | +0.08 | 0.8618 | 1.0000  |
| agora_mistral_en_t00 vs agora_union_mistral_en_t00 | 5 | +0.034 | +2.86 | 0.0031 | 0.0625  |
| agora_mistral_en_t00 vs agora_union_mistral_en_t07 | 5 | +0.037 | +2.45 | 0.0054 | 0.0625  |
| agora_mistral_en_t00 vs baseline_mistral_en_t00 | 5 | +0.016 | +1.20 | 0.0557 | 0.1250  |
| agora_mistral_en_t00 vs baseline_mistral_en_t07 | 5 | +0.021 | +1.27 | 0.0465 | 0.1250  |
| agora_mistral_en_t07 vs agora_union_mistral_en_t00 | 5 | +0.033 | +2.47 | 0.0052 | 0.0625  |
| agora_mistral_en_t07 vs agora_union_mistral_en_t07 | 5 | +0.035 | +4.48 | 0.0006 | 0.0625  |
| agora_mistral_en_t07 vs baseline_mistral_en_t00 | 5 | +0.014 | +1.43 | 0.0329 | 0.0625  |
| agora_mistral_en_t07 vs baseline_mistral_en_t07 | 5 | +0.019 | +1.92 | 0.0127 | 0.0625  |
| agora_mistral_hi_t00 vs baseline_mistral_hi_t00 | 5 | +0.029 | +1.79 | 0.0160 | 0.0625  |
| agora_mistral_pt_t00 vs baseline_mistral_pt_t00 | 5 | +0.057 | +1.87 | 0.0139 | 0.0625  |
| agora_mistral_ru_t00 vs baseline_mistral_ru_t00 | 5 | +0.036 | +2.30 | 0.0068 | 0.0625  |
| agora_together_llama33_70b_en_t00 vs agora_together_llama33_70b_en_t07 | 5 | -0.008 | -0.70 | 0.1941 | 0.1875  |
| agora_together_llama33_70b_en_t00 vs agora_union_together_llama33_70b_en_t00 | 5 | +0.042 | +4.27 | 0.0007 | 0.0625  |
| agora_together_llama33_70b_en_t00 vs agora_union_together_llama33_70b_en_t07 | 5 | +0.037 | +7.93 | 0.0001 | 0.0625  |
| agora_together_llama33_70b_en_t00 vs baseline_together_llama33_70b_en_t00 | 5 | +0.030 | +3.20 | 0.0020 | 0.0625  |
| agora_together_llama33_70b_en_t00 vs baseline_together_llama33_70b_en_t07 | 5 | +0.012 | +3.64 | 0.0012 | 0.0625  |
| agora_together_llama33_70b_en_t07 vs agora_union_together_llama33_70b_en_t00 | 5 | +0.050 | +3.34 | 0.0017 | 0.0625  |
| agora_together_llama33_70b_en_t07 vs agora_union_together_llama33_70b_en_t07 | 5 | +0.045 | +3.95 | 0.0009 | 0.0625  |
| agora_together_llama33_70b_en_t07 vs baseline_together_llama33_70b_en_t00 | 5 | +0.039 | +3.10 | 0.0023 | 0.0625  |
| agora_together_llama33_70b_en_t07 vs baseline_together_llama33_70b_en_t07 | 5 | +0.021 | +1.53 | 0.0267 | 0.0625  |
| agora_union_deepseek_en_t00 vs agora_union_deepseek_en_t07 | 5 | +0.010 | +0.88 | 0.1209 | 0.1250  |
| agora_union_deepseek_en_t00 vs baseline_deepseek_en_t00 | 5 | -0.018 | -1.22 | 0.0521 | 0.0625  |
| agora_union_deepseek_en_t00 vs baseline_deepseek_en_t07 | 5 | -0.014 | -0.80 | 0.1470 | 0.1875  |
| agora_union_deepseek_en_t07 vs baseline_deepseek_en_t00 | 5 | -0.028 | -3.42 | 0.0016 | 0.0625  |
| agora_union_deepseek_en_t07 vs baseline_deepseek_en_t07 | 5 | -0.024 | -2.26 | 0.0072 | 0.0625  |
| agora_union_deepseek_pt_t00 vs baseline_deepseek_pt_t00 | 5 | +0.006 | +0.30 | 0.5424 | 0.6250  |
| agora_union_deepseek_pt_t00 vs baseline_deepseek_pt_t07 | 5 | +0.005 | +0.19 | 0.6878 | 0.8125  |
| agora_union_gpt5nano_en_t00 vs agora_union_gpt5nano_en_t07 | 5 | +0.003 | +0.11 | 0.8240 | 1.0000  |
| agora_union_gpt5nano_en_t00 vs baseline_gpt5nano_en_t00 | 5 | -0.043 | -3.21 | 0.0020 | 0.0625  |
| agora_union_gpt5nano_en_t00 vs baseline_gpt5nano_en_t07 | 5 | -0.018 | -1.32 | 0.0423 | 0.0625  |
| agora_union_gpt5nano_en_t07 vs baseline_gpt5nano_en_t00 | 5 | -0.045 | -1.46 | 0.0308 | 0.0625  |
| agora_union_gpt5nano_en_t07 vs baseline_gpt5nano_en_t07 | 5 | -0.021 | -1.47 | 0.0303 | 0.0625  |
| agora_union_mistral_en_t00 vs agora_union_mistral_en_t07 | 5 | +0.003 | +0.24 | 0.6264 | 1.0000  |
| agora_union_mistral_en_t00 vs baseline_mistral_en_t00 | 5 | -0.018 | -4.89 | 0.0004 | 0.0625  |
| agora_union_mistral_en_t00 vs baseline_mistral_en_t07 | 5 | -0.013 | -2.29 | 0.0069 | 0.0625  |
| agora_union_mistral_en_t07 vs baseline_mistral_en_t00 | 5 | -0.021 | -2.25 | 0.0073 | 0.0625  |
| agora_union_mistral_en_t07 vs baseline_mistral_en_t07 | 5 | -0.016 | -1.94 | 0.0122 | 0.0625  |
| agora_union_together_llama33_70b_en_t00 vs agora_union_together_llama33_70b_en_t07 | 5 | -0.005 | -0.83 | 0.1363 | 0.3125  |
| agora_union_together_llama33_70b_en_t00 vs baseline_together_llama33_70b_en_t00 | 5 | -0.011 | -1.53 | 0.0268 | 0.1250  |
| agora_union_together_llama33_70b_en_t00 vs baseline_together_llama33_70b_en_t07 | 5 | -0.029 | -3.91 | 0.0009 | 0.0625  |
| agora_union_together_llama33_70b_en_t07 vs baseline_together_llama33_70b_en_t00 | 5 | -0.006 | -0.76 | 0.1631 | 0.1250  |
| agora_union_together_llama33_70b_en_t07 vs baseline_together_llama33_70b_en_t07 | 5 | -0.024 | -7.02 | 0.0001 | 0.0625  |
| baseline_deepseek_bg_t00 vs baseline_deepseek_bg_t07 | 5 | +0.009 | +1.11 | 0.0675 | 0.1250  |
| baseline_deepseek_en_t00 vs baseline_deepseek_en_t07 | 5 | +0.004 | +0.28 | 0.5645 | 1.0000  |
| baseline_deepseek_pt_t00 vs baseline_deepseek_pt_t07 | 5 | -0.001 | -0.06 | 0.9078 | 1.0000  |
| baseline_deepseek_ru_t00 vs baseline_deepseek_ru_t07 | 5 | +0.007 | +0.53 | 0.3044 | 0.4375  |
| baseline_gpt5nano_en_t00 vs baseline_gpt5nano_en_t07 | 5 | +0.025 | +1.30 | 0.0437 | 0.0625  |
| baseline_mistral_en_t00 vs baseline_mistral_en_t07 | 5 | +0.005 | +1.17 | 0.0586 | 0.1250  |
| baseline_together_llama33_70b_en_t00 vs baseline_together_llama33_70b_en_t07 | 5 | -0.018 | -2.07 | 0.0099 | 0.0625  |
| mdeberta_baseline_bg_t00 vs mdeberta_originals_only_bg_t00 | 5 | +0.008 | +0.15 | 0.7522 | 1.0000  |
| mdeberta_baseline_en_t00 vs mdeberta_originals_only_en_t00 | 5 | +0.035 | +0.86 | 0.1280 | 0.1875  |
| mdeberta_baseline_hi_t00 vs mdeberta_originals_only_hi_t00 | 5 | +0.016 | +0.43 | 0.3893 | 0.4375  |
| mdeberta_baseline_pt_t00 vs mdeberta_originals_only_pt_t00 | 5 | +0.007 | +0.37 | 0.4577 | 0.3125  |
| mdeberta_baseline_ru_t00 vs mdeberta_originals_only_ru_t00 | 5 | +0.019 | +0.64 | 0.2270 | 0.3125  |

## Top Confused Narrative Pairs (bistochastic TCM)

The bistochastic normalisation removes class-frequency bias from the raw TCM, isolating purely structural confusion between narratives. Pairs are reported per language for the best-hF experiment in that language.

### BG — agora_deepseek_bg_t00

| Gold narrative | Predicted as | bis(TCM) mass | raw mass | same-domain |
|---|---|---|---|---|
| Negative Consequences for the West | Amplifying war-related fears | 0.5257 | 2.8343 | yes |
| Criticism of climate movement | Criticism of climate policies | 0.4606 | 1.6677 | yes |
| Blaming the war on others rather than the invader | Distrust towards Media | 0.4505 | 1.0010 | yes |
| Discrediting the West, Diplomacy | Praise of Russia | 0.3521 | 1.4177 | yes |
| Negative Consequences for the West | Blaming the war on others rather than the invader | 0.3277 | 1.8343 | yes |
| Downplaying climate change | Controversy about green technologies | 0.3127 | 1.4177 | yes |
| Amplifying war-related fears | Speculating war outcomes | 0.3028 | 1.6677 | yes |
| Hidden plots by secret schemes of powerful groups | Green policies are geopolitical instruments | 0.2581 | 0.8510 | yes |

### EN — actor_critic_gemini_en_t07

| Gold narrative | Predicted as | bis(TCM) mass | raw mass | same-domain |
|---|---|---|---|---|
| Questioning the measurements and science | Climate change is beneficial | 0.3812 | 1.4177 | yes |
| Criticism of climate movement | Amplifying Climate Fears | 0.3270 | 2.5010 | yes |
| Criticism of climate movement | Questioning the measurements and science | 0.3162 | 4.2141 | yes |
| Negative Consequences for the West | Criticism of climate movement | 0.3088 | 1.2510 | no |
| Negative Consequences for the West | Downplaying climate change | 0.3015 | 1.2510 | no |
| Controversy about green technologies | Green policies are geopolitical instruments | 0.2621 | 0.7510 | yes |
| Criticism of climate policies | Hidden plots by secret schemes of powerful groups | 0.2497 | 2.3439 | yes |
| Hidden plots by secret schemes of powerful groups | Downplaying climate change | 0.2482 | 1.1677 | yes |

### HI — agora_majority_gpt5nano_hi_t00

| Gold narrative | Predicted as | bis(TCM) mass | raw mass | same-domain |
|---|---|---|---|---|
| Speculating war outcomes | Russia is the Victim | 0.5554 | 4.5010 | yes |
| Hidden plots by secret schemes of powerful groups | Distrust towards Media | 0.3686 | 1.2510 | no |
| Hidden plots by secret schemes of powerful groups | Negative Consequences for the West | 0.3608 | 1.7510 | no |
| Blaming the war on others rather than the invader | Discrediting Ukraine | 0.2196 | 1.4010 | yes |
| Amplifying Climate Fears | Questioning the measurements and science | 0.2154 | 1.0010 | yes |
| Praise of Russia | Blaming the war on others rather than the invader | 0.2147 | 3.1677 | yes |
| Discrediting the West, Diplomacy | Negative Consequences for the West | 0.2106 | 2.1677 | yes |
| Amplifying war-related fears | Speculating war outcomes | 0.1656 | 13.2010 | yes |

### PT — agora_majority_gpt5nano_pt_t00

| Gold narrative | Predicted as | bis(TCM) mass | raw mass | same-domain |
|---|---|---|---|---|
| Russia is the Victim | Overpraising the West | 0.4468 | 2.0010 | yes |
| Discrediting the West, Diplomacy | Praise of Russia | 0.4464 | 2.0010 | yes |
| Criticism of climate policies | Criticism of institutions and authorities | 0.3572 | 2.5010 | yes |
| Discrediting the West, Diplomacy | Negative Consequences for the West | 0.3291 | 0.8343 | yes |
| Discrediting Ukraine | Discrediting the West, Diplomacy | 0.3117 | 2.5010 | yes |
| Praise of Russia | Russia is the Victim | 0.2843 | 2.8343 | yes |
| Praise of Russia | Discrediting the West, Diplomacy | 0.2518 | 4.8343 | yes |
| Praise of Russia | Blaming the war on others rather than the invader | 0.2470 | 0.8343 | yes |

### RU — agora_majority_gpt5nano_ru_t00

| Gold narrative | Predicted as | bis(TCM) mass | raw mass | same-domain |
|---|---|---|---|---|
| Amplifying war-related fears | Speculating war outcomes | 0.3408 | 2.5010 | yes |
| Speculating war outcomes | Blaming the war on others rather than the invader | 0.3346 | 1.0010 | yes |
| Hidden plots by secret schemes of powerful groups | Distrust towards Media | 0.3080 | 0.7962 | no |
| Speculating war outcomes | Discrediting the West, Diplomacy | 0.2564 | 1.3343 | yes |
| Discrediting the West, Diplomacy | Negative Consequences for the West | 0.2500 | 2.3343 | yes |
| Speculating war outcomes | Discrediting Ukraine | 0.2346 | 1.3343 | yes |
| Praise of Russia | Discrediting the West, Diplomacy | 0.2259 | 12.9177 | yes |
| Discrediting the West, Diplomacy | Speculating war outcomes | 0.2124 | 10.0010 | yes |

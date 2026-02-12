# Actor-Critic vs Baseline Comparison Report

Generated: 2026-02-11 20:00:14

**Total comparisons:** 20

## Methodology

Each Actor-Critic experiment is compared against its matched Baseline experiment
(same LLM, same language, same temperature). Both methods use a single agent;
the difference is that Actor-Critic adds **validation nodes** that review and
refine predictions at both narrative and subnarrative levels.

Statistical tests (paired, since runs use matched seeds):
- **Paired t-test**: parametric
- **Wilcoxon signed-rank**: non-parametric
- **Cohen's d** (paired): mean(diff)/std(diff). |d|<0.2 negligible, 0.2-0.5 small, 0.5-0.8 medium, >=0.8 large
- Significance: * p<0.05, ** p<0.01, *** p<0.001

## Summary Table

### Narrative-level F1-samples (manual)

| Model | Lang | Temp | Actor-Critic | Baseline | Diff | Rel% | Cohen's d | Wilcoxon p | Sig |
|-------|------|------|-------------|----------|------|------|-----------|------------|-----|
| DeepSeek V3 | BG | t00 | 0.453±0.039 | 0.575±0.010 | -0.122 | -21.2% | -2.93 (large) | 0.0625 |  |
| DeepSeek V3 | BG | t07 | 0.490±0.049 | 0.565±0.008 | -0.075 | -13.3% | -1.36 (large) | 0.0625 |  |
| DeepSeek V3 | EN | t00 | 0.347±0.020 | 0.342±0.013 | +0.005 | +1.3% | +0.20 (small) | 0.6250 |  |
| DeepSeek V3 | EN | t07 | 0.343±0.042 | 0.329±0.012 | +0.014 | +4.3% | +0.32 (small) | 1.0000 |  |
| DeepSeek V3 | HI | t00 | 0.388±0.028 | 0.430±0.021 | -0.043 | -10.0% | -1.26 (large) | 0.0625 |  |
| DeepSeek V3 | PT | t00 | 0.383±0.055 | 0.510±0.020 | -0.127 | -24.8% | -2.44 (large) | 0.0625 |  |
| DeepSeek V3 | RU | t00 | 0.454±0.021 | 0.481±0.018 | -0.027 | -5.6% | -0.99 (large) | 0.0625 |  |
| DeepSeek V3 | RU | t07 | 0.451±0.022 | 0.472±0.009 | -0.021 | -4.4% | -0.89 (large) | 0.2500 |  |
| Gemini 2.5 Flash | EN | t00 | 0.334±0.018 | 0.354±0.012 | -0.020 | -5.7% | -0.85 (large) | 0.1875 |  |
| GPT-5 Nano | EN | t00 | 0.294±0.018 | 0.341±0.034 | -0.048 | -14.0% | -1.37 (large) | 0.0625 |  |
| GPT-5 Nano | EN | t07 | 0.331±0.020 | 0.308±0.021 | +0.022 | +7.3% | +0.96 (large) | 0.0625 |  |
| Mistral Large | BG | t00 | 0.474±0.020 | 0.469±0.019 | +0.005 | +1.0% | +0.13 (negligible) | 1.0000 |  |
| Mistral Large | EN | t00 | 0.287±0.012 | 0.297±0.005 | -0.010 | -3.3% | -0.77 (medium) | 0.3125 |  |
| Mistral Large | EN | t07 | 0.285±0.016 | 0.286±0.009 | -0.001 | -0.3% | -0.05 (negligible) | 0.8125 |  |
| Mistral Large | HI | t00 | 0.306±0.014 | 0.320±0.023 | -0.014 | -4.4% | -0.47 (small) | 0.3125 |  |
| Mistral Large | PT | t00 | 0.374±0.019 | 0.382±0.036 | -0.008 | -2.2% | -0.22 (small) | 0.6250 |  |
| Mistral Large | RU | t00 | 0.387±0.017 | 0.382±0.008 | +0.006 | +1.5% | +0.35 (small) | 0.4375 |  |
| Llama 3.3 70B | EN | t00 | 0.319±0.010 | 0.285±0.013 | +0.035 | +12.1% | +1.55 (large) | 0.0625 |  |
| Llama 3.3 70B | EN | t07 | 0.307±0.024 | 0.300±0.009 | +0.006 | +2.0% | +0.22 (small) | 0.6250 |  |

### Subnarrative-level F1-samples (manual)

| Model | Lang | Temp | Actor-Critic | Baseline | Diff | Rel% | Cohen's d | Wilcoxon p | Sig |
|-------|------|------|-------------|----------|------|------|-----------|------------|-----|
| DeepSeek V3 | BG | t00 | 0.187±0.019 | 0.217±0.006 | -0.030 | -13.8% | -1.30 (large) | 0.0625 |  |
| DeepSeek V3 | BG | t07 | 0.204±0.034 | 0.216±0.001 | -0.012 | -5.5% | -0.35 (small) | 0.6250 |  |
| DeepSeek V3 | EN | t00 | 0.130±0.012 | 0.103±0.008 | +0.027 | +26.1% | +1.66 (large) | 0.0625 |  |
| DeepSeek V3 | EN | t07 | 0.124±0.025 | 0.101±0.008 | +0.023 | +23.1% | +0.87 (large) | 0.1875 |  |
| DeepSeek V3 | HI | t00 | 0.130±0.009 | 0.184±0.013 | -0.054 | -29.3% | -3.21 (large) | 0.0625 |  |
| DeepSeek V3 | PT | t00 | 0.127±0.027 | 0.202±0.017 | -0.075 | -37.2% | -2.18 (large) | 0.0625 |  |
| DeepSeek V3 | RU | t00 | 0.212±0.015 | 0.205±0.007 | +0.008 | +3.9% | +0.58 (medium) | 0.3125 |  |
| DeepSeek V3 | RU | t07 | 0.217±0.041 | 0.200±0.005 | +0.017 | +8.3% | +0.38 (small) | 0.4375 |  |
| Gemini 2.5 Flash | EN | t00 | 0.144±0.020 | 0.144±0.008 | +0.001 | +0.4% | +0.03 (negligible) | 1.0000 |  |
| GPT-5 Nano | EN | t00 | 0.115±0.026 | 0.167±0.015 | -0.052 | -31.1% | -2.04 (large) | 0.0625 |  |
| GPT-5 Nano | EN | t07 | 0.146±0.017 | 0.145±0.014 | +0.001 | +0.5% | +0.03 (negligible) | 0.8125 |  |
| Mistral Large | BG | t00 | 0.143±0.012 | 0.145±0.007 | -0.002 | -1.5% | -0.13 (negligible) | 1.0000 |  |
| Mistral Large | EN | t00 | 0.080±0.006 | 0.086±0.002 | -0.006 | -6.6% | -0.86 (large) | 0.1875 |  |
| Mistral Large | EN | t07 | 0.080±0.006 | 0.084±0.005 | -0.004 | -4.3% | -0.42 (small) | 0.4375 |  |
| Mistral Large | HI | t00 | 0.099±0.007 | 0.100±0.010 | -0.001 | -1.1% | -0.13 (negligible) | 0.8125 |  |
| Mistral Large | PT | t00 | 0.123±0.010 | 0.123±0.015 | +0.001 | +0.5% | +0.04 (negligible) | 0.6250 |  |
| Mistral Large | RU | t00 | 0.139±0.004 | 0.135±0.004 | +0.004 | +2.8% | +1.17 (large) | 0.1250 |  |
| Llama 3.3 70B | EN | t00 | 0.106±0.007 | 0.076±0.004 | +0.030 | +39.1% | +2.95 (large) | 0.0625 |  |
| Llama 3.3 70B | EN | t07 | 0.102±0.013 | 0.081±0.005 | +0.021 | +26.5% | +1.69 (large) | 0.0625 |  |

## Aggregate Analysis

### Win/Loss/Tie Count (Actor-Critic vs Baseline)

| Level | AC Wins | AC Losses | Ties | Sig Wins (p<.05) | Sig Losses (p<.05) |
|-------|---------|-----------|------|------------------|--------------------|
| Narrative | 7 | 11 | 1 | 0 | 0 |
| Subnarrative | 7 | 9 | 3 | 0 | 0 |

### Average Improvement by Model

| Model | Avg Narr Diff | Avg Subnarr Diff | N pairs |
|-------|--------------|-----------------|---------|
| DeepSeek V3 | -0.0495 | -0.0120 | 8 |
| GPT-5 Nano | -0.0127 | -0.0255 | 2 |
| Gemini 2.5 Flash | -0.0202 | +0.0005 | 1 |
| Llama 3.3 70B | +0.0203 | +0.0256 | 2 |
| Mistral Large | -0.0038 | -0.0013 | 6 |

### Average Improvement by Language

| Language | Avg Narr Diff | Avg Subnarr Diff | N pairs |
|----------|--------------|-----------------|---------|
| BG | -0.0642 | -0.0147 | 3 |
| EN | +0.0003 | +0.0046 | 9 |
| HI | -0.0285 | -0.0276 | 2 |
| PT | -0.0674 | -0.0372 | 2 |
| RU | -0.0141 | +0.0095 | 3 |

## Detailed Per-Pair Results

### DeepSeek V3 — BG — t00

- **Actor-Critic**: `actor_critic_deepseek_bg_t00`
- **Baseline**: `baseline_deepseek_bg_t00`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.2649±0.0465 | 0.3337±0.0164 | -0.0688 | -20.6% | 0.0434* | 0.0625 | -1.30 (large) |
| Narr f1_micro | 0.4350±0.0395 | 0.5135±0.0096 | -0.0785 | -15.3% | 0.0148* | 0.0625 | -1.84 (large) |
| Narr f1_samples | 0.4531±0.0394 | 0.5750±0.0096 | -0.1219 | -21.2% | 0.0028** | 0.0625 | -2.93 (large) |
| Narr f1_samples_manual | 0.4531±0.0394 | 0.5750±0.0096 | -0.1219 | -21.2% | 0.0028** | 0.0625 | -2.93 (large) |
| subNarr f1_macro | 0.1035±0.0090 | 0.1056±0.0055 | -0.0021 | -2.0% | 0.7226 | 0.8125 | -0.17 (negligible) |
| subNarr f1_micro | 0.1805±0.0131 | 0.1875±0.0026 | -0.0070 | -3.7% | 0.3748 | 0.4375 | -0.45 (small) |
| subNarr f1_samples | 0.1868±0.0194 | 0.2168±0.0058 | -0.0300 | -13.8% | 0.0435* | 0.0625 | -1.30 (large) |
| subNarr f1_samples_manual | 0.1868±0.0194 | 0.2168±0.0058 | -0.0300 | -13.8% | 0.0435* | 0.0625 | -1.30 (large) |

### DeepSeek V3 — BG — t07

- **Actor-Critic**: `actor_critic_deepseek_bg_t07`
- **Baseline**: `baseline_deepseek_bg_t07`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.2751±0.0373 | 0.3218±0.0157 | -0.0467 | -14.5% | 0.0898 | 0.1250 | -1.00 (large) |
| Narr f1_micro | 0.4630±0.0207 | 0.5031±0.0119 | -0.0401 | -8.0% | 0.0505 | 0.0625 | -1.24 (large) |
| Narr f1_samples | 0.4895±0.0488 | 0.5648±0.0078 | -0.0752 | -13.3% | 0.0382* | 0.0625 | -1.36 (large) |
| Narr f1_samples_manual | 0.4895±0.0488 | 0.5648±0.0078 | -0.0752 | -13.3% | 0.0382* | 0.0625 | -1.36 (large) |
| subNarr f1_macro | 0.1138±0.0113 | 0.1035±0.0062 | +0.0102 | +9.9% | 0.0316* | 0.0625 | +1.45 (large) |
| subNarr f1_micro | 0.1954±0.0071 | 0.1842±0.0024 | +0.0112 | +6.1% | 0.0202* | 0.0625 | +1.67 (large) |
| subNarr f1_samples | 0.2036±0.0336 | 0.2156±0.0014 | -0.0119 | -5.5% | 0.4770 | 0.6250 | -0.35 (small) |
| subNarr f1_samples_manual | 0.2036±0.0336 | 0.2156±0.0014 | -0.0119 | -5.5% | 0.4770 | 0.6250 | -0.35 (small) |

### DeepSeek V3 — EN — t00

- **Actor-Critic**: `actor_critic_deepseek_en_t00`
- **Baseline**: `baseline_deepseek_en_t00`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.2831±0.0315 | 0.2885±0.0087 | -0.0054 | -1.9% | 0.7309 | 1.0000 | -0.16 (negligible) |
| Narr f1_micro | 0.3505±0.0180 | 0.3404±0.0078 | +0.0100 | +2.9% | 0.3375 | 0.4375 | +0.49 (small) |
| Narr f1_samples | 0.3469±0.0203 | 0.3424±0.0132 | +0.0045 | +1.3% | 0.6746 | 0.6250 | +0.20 (small) |
| Narr f1_samples_manual | 0.3469±0.0203 | 0.3424±0.0132 | +0.0045 | +1.3% | 0.6746 | 0.6250 | +0.20 (small) |
| subNarr f1_macro | 0.1045±0.0078 | 0.0983±0.0044 | +0.0063 | +6.4% | 0.0600 | 0.0625 | +1.16 (large) |
| subNarr f1_micro | 0.1290±0.0072 | 0.1098±0.0059 | +0.0192 | +17.5% | 0.0034** | 0.0625 | +2.77 (large) |
| subNarr f1_samples | 0.1302±0.0120 | 0.1033±0.0078 | +0.0269 | +26.1% | 0.0207* | 0.0625 | +1.66 (large) |
| subNarr f1_samples_manual | 0.1302±0.0120 | 0.1033±0.0078 | +0.0269 | +26.1% | 0.0207* | 0.0625 | +1.66 (large) |

### DeepSeek V3 — EN — t07

- **Actor-Critic**: `actor_critic_deepseek_en_t07`
- **Baseline**: `baseline_deepseek_en_t07`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.2719±0.0357 | 0.2754±0.0182 | -0.0035 | -1.3% | 0.8646 | 0.8125 | -0.08 (negligible) |
| Narr f1_micro | 0.3411±0.0335 | 0.3316±0.0087 | +0.0096 | +2.9% | 0.5536 | 1.0000 | +0.29 (small) |
| Narr f1_samples | 0.3431±0.0421 | 0.3289±0.0124 | +0.0142 | +4.3% | 0.5097 | 1.0000 | +0.32 (small) |
| Narr f1_samples_manual | 0.3431±0.0421 | 0.3289±0.0124 | +0.0142 | +4.3% | 0.5097 | 1.0000 | +0.32 (small) |
| subNarr f1_macro | 0.0956±0.0121 | 0.1000±0.0073 | -0.0044 | -4.4% | 0.4889 | 0.8125 | -0.34 (small) |
| subNarr f1_micro | 0.1253±0.0165 | 0.1081±0.0079 | +0.0172 | +15.9% | 0.0853 | 0.1250 | +1.02 (large) |
| subNarr f1_samples | 0.1238±0.0254 | 0.1006±0.0084 | +0.0232 | +23.1% | 0.1251 | 0.1875 | +0.87 (large) |
| subNarr f1_samples_manual | 0.1238±0.0254 | 0.1006±0.0084 | +0.0232 | +23.1% | 0.1251 | 0.1875 | +0.87 (large) |

### DeepSeek V3 — HI — t00

- **Actor-Critic**: `actor_critic_deepseek_hi_t00`
- **Baseline**: `baseline_deepseek_hi_t00`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.3006±0.0310 | 0.3163±0.0237 | -0.0157 | -5.0% | 0.4136 | 0.8125 | -0.41 (small) |
| Narr f1_micro | 0.4003±0.0260 | 0.4156±0.0165 | -0.0153 | -3.7% | 0.3518 | 0.6250 | -0.47 (small) |
| Narr f1_samples | 0.3876±0.0284 | 0.4305±0.0213 | -0.0429 | -10.0% | 0.0481* | 0.0625 | -1.26 (large) |
| Narr f1_samples_manual | 0.3876±0.0284 | 0.4305±0.0213 | -0.0429 | -10.0% | 0.0481* | 0.0625 | -1.26 (large) |
| subNarr f1_macro | 0.1068±0.0075 | 0.1207±0.0030 | -0.0139 | -11.5% | 0.0060** | 0.0625 | -2.38 (large) |
| subNarr f1_micro | 0.1315±0.0087 | 0.1521±0.0092 | -0.0205 | -13.5% | 0.0170* | 0.0625 | -1.76 (large) |
| subNarr f1_samples | 0.1301±0.0093 | 0.1841±0.0133 | -0.0540 | -29.3% | 0.0020** | 0.0625 | -3.21 (large) |
| subNarr f1_samples_manual | 0.1301±0.0093 | 0.1841±0.0133 | -0.0540 | -29.3% | 0.0020** | 0.0625 | -3.21 (large) |

### DeepSeek V3 — PT — t00

- **Actor-Critic**: `actor_critic_deepseek_pt_t00`
- **Baseline**: `baseline_deepseek_pt_t00`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.2943±0.0283 | 0.3821±0.0213 | -0.0879 | -23.0% | 0.0060** | 0.0625 | -2.39 (large) |
| Narr f1_micro | 0.4077±0.0457 | 0.5058±0.0129 | -0.0981 | -19.4% | 0.0069** | 0.0625 | -2.29 (large) |
| Narr f1_samples | 0.3832±0.0552 | 0.5099±0.0198 | -0.1267 | -24.8% | 0.0055** | 0.0625 | -2.44 (large) |
| Narr f1_samples_manual | 0.3832±0.0552 | 0.5099±0.0198 | -0.1267 | -24.8% | 0.0055** | 0.0625 | -2.44 (large) |
| subNarr f1_macro | 0.1319±0.0300 | 0.1247±0.0137 | +0.0072 | +5.8% | 0.5550 | 0.6250 | +0.29 (small) |
| subNarr f1_micro | 0.1663±0.0180 | 0.1901±0.0136 | -0.0238 | -12.5% | 0.0438* | 0.0625 | -1.30 (large) |
| subNarr f1_samples | 0.1270±0.0266 | 0.2020±0.0168 | -0.0751 | -37.2% | 0.0082** | 0.0625 | -2.18 (large) |
| subNarr f1_samples_manual | 0.1270±0.0266 | 0.2020±0.0168 | -0.0751 | -37.2% | 0.0082** | 0.0625 | -2.18 (large) |

### DeepSeek V3 — RU — t00

- **Actor-Critic**: `actor_critic_deepseek_ru_t00`
- **Baseline**: `baseline_deepseek_ru_t00`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.2141±0.0237 | 0.2363±0.0143 | -0.0222 | -9.4% | 0.2476 | 0.3125 | -0.60 (medium) |
| Narr f1_micro | 0.4242±0.0123 | 0.4401±0.0127 | -0.0159 | -3.6% | 0.1948 | 0.2500 | -0.70 (medium) |
| Narr f1_samples | 0.4543±0.0209 | 0.4812±0.0180 | -0.0269 | -5.6% | 0.0921 | 0.0625 | -0.99 (large) |
| Narr f1_samples_manual | 0.4543±0.0209 | 0.4812±0.0180 | -0.0269 | -5.6% | 0.0921 | 0.0625 | -0.99 (large) |
| subNarr f1_macro | 0.1352±0.0085 | 0.1367±0.0097 | -0.0016 | -1.1% | 0.7540 | 1.0000 | -0.15 (negligible) |
| subNarr f1_micro | 0.1852±0.0088 | 0.1771±0.0086 | +0.0082 | +4.6% | 0.1309 | 0.1875 | +0.85 (large) |
| subNarr f1_samples | 0.2124±0.0146 | 0.2045±0.0074 | +0.0079 | +3.9% | 0.2620 | 0.3125 | +0.58 (medium) |
| subNarr f1_samples_manual | 0.2124±0.0146 | 0.2045±0.0074 | +0.0079 | +3.9% | 0.2620 | 0.3125 | +0.58 (medium) |

### DeepSeek V3 — RU — t07

- **Actor-Critic**: `actor_critic_deepseek_ru_t07`
- **Baseline**: `baseline_deepseek_ru_t07`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.2143±0.0354 | 0.2324±0.0140 | -0.0181 | -7.8% | 0.3988 | 0.6250 | -0.42 (small) |
| Narr f1_micro | 0.4240±0.0232 | 0.4308±0.0086 | -0.0067 | -1.6% | 0.5642 | 0.8125 | -0.28 (small) |
| Narr f1_samples | 0.4514±0.0217 | 0.4723±0.0086 | -0.0209 | -4.4% | 0.1186 | 0.2500 | -0.89 (large) |
| Narr f1_samples_manual | 0.4514±0.0217 | 0.4723±0.0086 | -0.0209 | -4.4% | 0.1186 | 0.2500 | -0.89 (large) |
| subNarr f1_macro | 0.1324±0.0207 | 0.1297±0.0051 | +0.0027 | +2.1% | 0.8039 | 0.8125 | +0.12 (negligible) |
| subNarr f1_micro | 0.1938±0.0270 | 0.1743±0.0033 | +0.0195 | +11.2% | 0.2232 | 0.3125 | +0.64 (medium) |
| subNarr f1_samples | 0.2170±0.0412 | 0.2004±0.0054 | +0.0167 | +8.3% | 0.4457 | 0.4375 | +0.38 (small) |
| subNarr f1_samples_manual | 0.2170±0.0412 | 0.2004±0.0054 | +0.0167 | +8.3% | 0.4457 | 0.4375 | +0.38 (small) |

### Gemini 2.5 Flash — EN — t00

- **Actor-Critic**: `actor_critic_gemini_en_t00`
- **Baseline**: `baseline_gemini_en_t00`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.2428±0.0226 | 0.2370±0.0230 | +0.0058 | +2.4% | 0.7553 | 0.8125 | +0.15 (negligible) |
| Narr f1_micro | 0.3088±0.0045 | 0.3061±0.0069 | +0.0027 | +0.9% | 0.5221 | 0.4375 | +0.31 (small) |
| Narr f1_samples | 0.3342±0.0178 | 0.3544±0.0117 | -0.0202 | -5.7% | 0.1288 | 0.1875 | -0.85 (large) |
| Narr f1_samples_manual | 0.3342±0.0178 | 0.3544±0.0117 | -0.0202 | -5.7% | 0.1288 | 0.1875 | -0.85 (large) |
| subNarr f1_macro | 0.0961±0.0142 | 0.0967±0.0069 | -0.0006 | -0.6% | 0.9464 | 1.0000 | -0.03 (negligible) |
| subNarr f1_micro | 0.1252±0.0068 | 0.1149±0.0049 | +0.0103 | +9.0% | 0.0540 | 0.0625 | +1.21 (large) |
| subNarr f1_samples | 0.1443±0.0196 | 0.1438±0.0081 | +0.0005 | +0.4% | 0.9552 | 1.0000 | +0.03 (negligible) |
| subNarr f1_samples_manual | 0.1443±0.0196 | 0.1438±0.0081 | +0.0005 | +0.4% | 0.9552 | 1.0000 | +0.03 (negligible) |

### Gemini 2.5 Flash — EN — t07

- **Actor-Critic**: `actor_critic_gemini_en_t07`
- **Baseline**: `baseline_gemini_en_t07`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|

### GPT-5 Nano — EN — t00

- **Actor-Critic**: `actor_critic_gpt5nano_en_t00`
- **Baseline**: `baseline_gpt5nano_en_t00`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.2400±0.0315 | 0.2883±0.0237 | -0.0484 | -16.8% | 0.0246* | 0.0625 | -1.57 (large) |
| Narr f1_micro | 0.2863±0.0158 | 0.3224±0.0297 | -0.0361 | -11.2% | 0.0640 | 0.1250 | -1.14 (large) |
| Narr f1_samples | 0.2937±0.0184 | 0.3414±0.0344 | -0.0477 | -14.0% | 0.0373* | 0.0625 | -1.37 (large) |
| Narr f1_samples_manual | 0.2937±0.0184 | 0.3414±0.0344 | -0.0477 | -14.0% | 0.0373* | 0.0625 | -1.37 (large) |
| subNarr f1_macro | 0.0929±0.0201 | 0.1333±0.0066 | -0.0405 | -30.3% | 0.0158* | 0.0625 | -1.80 (large) |
| subNarr f1_micro | 0.1160±0.0178 | 0.1497±0.0087 | -0.0337 | -22.5% | 0.0088** | 0.0625 | -2.14 (large) |
| subNarr f1_samples | 0.1148±0.0260 | 0.1667±0.0152 | -0.0518 | -31.1% | 0.0103* | 0.0625 | -2.04 (large) |
| subNarr f1_samples_manual | 0.1148±0.0260 | 0.1667±0.0152 | -0.0518 | -31.1% | 0.0103* | 0.0625 | -2.04 (large) |

### GPT-5 Nano — EN — t07

- **Actor-Critic**: `actor_critic_gpt5nano_en_t07`
- **Baseline**: `baseline_gpt5nano_en_t07`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.2781±0.0193 | 0.2639±0.0126 | +0.0142 | +5.4% | 0.1092 | 0.0625 | +0.92 (large) |
| Narr f1_micro | 0.3099±0.0126 | 0.3012±0.0136 | +0.0087 | +2.9% | 0.2562 | 0.3125 | +0.59 (medium) |
| Narr f1_samples | 0.3306±0.0202 | 0.3082±0.0209 | +0.0224 | +7.3% | 0.0994 | 0.0625 | +0.96 (large) |
| Narr f1_samples_manual | 0.3306±0.0202 | 0.3082±0.0209 | +0.0224 | +7.3% | 0.0994 | 0.0625 | +0.96 (large) |
| subNarr f1_macro | 0.1213±0.0126 | 0.1077±0.0061 | +0.0136 | +12.6% | 0.1027 | 0.1250 | +0.94 (large) |
| subNarr f1_micro | 0.1400±0.0095 | 0.1287±0.0063 | +0.0114 | +8.8% | 0.1744 | 0.1875 | +0.74 (medium) |
| subNarr f1_samples | 0.1459±0.0166 | 0.1452±0.0137 | +0.0008 | +0.5% | 0.9482 | 0.8125 | +0.03 (negligible) |
| subNarr f1_samples_manual | 0.1459±0.0166 | 0.1452±0.0137 | +0.0008 | +0.5% | 0.9482 | 0.8125 | +0.03 (negligible) |

### Mistral Large — BG — t00

- **Actor-Critic**: `actor_critic_mistral_bg_t00`
- **Baseline**: `baseline_mistral_bg_t00`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.2853±0.0126 | 0.2423±0.0111 | +0.0430 | +17.8% | 0.0081** | 0.0625 | +2.19 (large) |
| Narr f1_micro | 0.4090±0.0139 | 0.3976±0.0095 | +0.0114 | +2.9% | 0.2897 | 0.3750 | +0.55 (medium) |
| Narr f1_samples | 0.4741±0.0205 | 0.4695±0.0192 | +0.0046 | +1.0% | 0.7907 | 1.0000 | +0.13 (negligible) |
| Narr f1_samples_manual | 0.4741±0.0205 | 0.4695±0.0192 | +0.0046 | +1.0% | 0.7907 | 1.0000 | +0.13 (negligible) |
| subNarr f1_macro | 0.0802±0.0037 | 0.0734±0.0017 | +0.0067 | +9.2% | 0.0379* | 0.0625 | +1.37 (large) |
| subNarr f1_micro | 0.1180±0.0046 | 0.1152±0.0029 | +0.0028 | +2.4% | 0.3999 | 0.6250 | +0.42 (small) |
| subNarr f1_samples | 0.1429±0.0119 | 0.1451±0.0073 | -0.0022 | -1.5% | 0.7802 | 1.0000 | -0.13 (negligible) |
| subNarr f1_samples_manual | 0.1429±0.0119 | 0.1451±0.0073 | -0.0022 | -1.5% | 0.7802 | 1.0000 | -0.13 (negligible) |

### Mistral Large — EN — t00

- **Actor-Critic**: `actor_critic_mistral_en_t00`
- **Baseline**: `baseline_mistral_en_t00`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.2155±0.0283 | 0.2401±0.0160 | -0.0246 | -10.2% | 0.2164 | 0.3125 | -0.66 (medium) |
| Narr f1_micro | 0.2803±0.0131 | 0.2878±0.0078 | -0.0075 | -2.6% | 0.4374 | 0.8125 | -0.39 (small) |
| Narr f1_samples | 0.2868±0.0116 | 0.2967±0.0046 | -0.0098 | -3.3% | 0.1605 | 0.3125 | -0.77 (medium) |
| Narr f1_samples_manual | 0.2868±0.0116 | 0.2967±0.0046 | -0.0098 | -3.3% | 0.1605 | 0.3125 | -0.77 (medium) |
| subNarr f1_macro | 0.0687±0.0096 | 0.0742±0.0043 | -0.0055 | -7.4% | 0.2642 | 0.3125 | -0.58 (medium) |
| subNarr f1_micro | 0.0810±0.0043 | 0.0845±0.0013 | -0.0035 | -4.1% | 0.1362 | 0.1875 | -0.83 (large) |
| subNarr f1_samples | 0.0805±0.0064 | 0.0861±0.0016 | -0.0056 | -6.6% | 0.1268 | 0.1875 | -0.86 (large) |
| subNarr f1_samples_manual | 0.0805±0.0064 | 0.0861±0.0016 | -0.0056 | -6.6% | 0.1268 | 0.1875 | -0.86 (large) |

### Mistral Large — EN — t07

- **Actor-Critic**: `actor_critic_mistral_en_t07`
- **Baseline**: `baseline_mistral_en_t07`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.2120±0.0225 | 0.2127±0.0249 | -0.0006 | -0.3% | 0.9770 | 0.8125 | -0.01 (negligible) |
| Narr f1_micro | 0.2746±0.0112 | 0.2770±0.0090 | -0.0024 | -0.9% | 0.7652 | 0.6250 | -0.14 (negligible) |
| Narr f1_samples | 0.2851±0.0156 | 0.2859±0.0089 | -0.0008 | -0.3% | 0.9117 | 0.8125 | -0.05 (negligible) |
| Narr f1_samples_manual | 0.2851±0.0156 | 0.2859±0.0089 | -0.0008 | -0.3% | 0.9117 | 0.8125 | -0.05 (negligible) |
| subNarr f1_macro | 0.0701±0.0091 | 0.0728±0.0075 | -0.0027 | -3.7% | 0.6966 | 0.8125 | -0.19 (negligible) |
| subNarr f1_micro | 0.0803±0.0055 | 0.0829±0.0040 | -0.0026 | -3.1% | 0.5462 | 0.4375 | -0.29 (small) |
| subNarr f1_samples | 0.0803±0.0056 | 0.0839±0.0051 | -0.0036 | -4.3% | 0.4004 | 0.4375 | -0.42 (small) |
| subNarr f1_samples_manual | 0.0803±0.0056 | 0.0839±0.0051 | -0.0036 | -4.3% | 0.4004 | 0.4375 | -0.42 (small) |

### Mistral Large — HI — t00

- **Actor-Critic**: `actor_critic_mistral_hi_t00`
- **Baseline**: `baseline_mistral_hi_t00`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.2142±0.0285 | 0.2099±0.0094 | +0.0043 | +2.0% | 0.8042 | 0.6250 | +0.12 (negligible) |
| Narr f1_micro | 0.2982±0.0115 | 0.3079±0.0108 | -0.0097 | -3.2% | 0.3711 | 0.3125 | -0.45 (small) |
| Narr f1_samples | 0.3061±0.0139 | 0.3202±0.0226 | -0.0141 | -4.4% | 0.3532 | 0.3125 | -0.47 (small) |
| Narr f1_samples_manual | 0.3061±0.0139 | 0.3202±0.0226 | -0.0141 | -4.4% | 0.3532 | 0.3125 | -0.47 (small) |
| subNarr f1_macro | 0.0745±0.0104 | 0.0743±0.0018 | +0.0002 | +0.2% | 0.9757 | 0.6250 | +0.01 (negligible) |
| subNarr f1_micro | 0.0868±0.0059 | 0.0881±0.0025 | -0.0013 | -1.5% | 0.6597 | 1.0000 | -0.21 (small) |
| subNarr f1_samples | 0.0992±0.0068 | 0.1004±0.0098 | -0.0011 | -1.1% | 0.7897 | 0.8125 | -0.13 (negligible) |
| subNarr f1_samples_manual | 0.0992±0.0068 | 0.1004±0.0098 | -0.0011 | -1.1% | 0.7897 | 0.8125 | -0.13 (negligible) |

### Mistral Large — PT — t00

- **Actor-Critic**: `actor_critic_mistral_pt_t00`
- **Baseline**: `baseline_mistral_pt_t00`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.2554±0.0087 | 0.2467±0.0066 | +0.0087 | +3.5% | 0.1217 | 0.1875 | +0.88 (large) |
| Narr f1_micro | 0.3721±0.0118 | 0.3724±0.0161 | -0.0002 | -0.1% | 0.9820 | 1.0000 | -0.01 (negligible) |
| Narr f1_samples | 0.3736±0.0194 | 0.3819±0.0356 | -0.0082 | -2.2% | 0.6428 | 0.6250 | -0.22 (small) |
| Narr f1_samples_manual | 0.3736±0.0194 | 0.3819±0.0356 | -0.0082 | -2.2% | 0.6428 | 0.6250 | -0.22 (small) |
| subNarr f1_macro | 0.0863±0.0022 | 0.0824±0.0046 | +0.0039 | +4.7% | 0.2166 | 0.1875 | +0.66 (medium) |
| subNarr f1_micro | 0.1289±0.0056 | 0.1272±0.0064 | +0.0017 | +1.3% | 0.7577 | 1.0000 | +0.15 (negligible) |
| subNarr f1_samples | 0.1231±0.0100 | 0.1225±0.0150 | +0.0006 | +0.5% | 0.9408 | 0.6250 | +0.04 (negligible) |
| subNarr f1_samples_manual | 0.1231±0.0100 | 0.1225±0.0150 | +0.0006 | +0.5% | 0.9408 | 0.6250 | +0.04 (negligible) |

### Mistral Large — RU — t00

- **Actor-Critic**: `actor_critic_mistral_ru_t00`
- **Baseline**: `baseline_mistral_ru_t00`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.2144±0.0154 | 0.2084±0.0170 | +0.0060 | +2.9% | 0.2011 | 0.3125 | +0.68 (medium) |
| Narr f1_micro | 0.3590±0.0123 | 0.3526±0.0066 | +0.0064 | +1.8% | 0.3088 | 0.3750 | +0.52 (medium) |
| Narr f1_samples | 0.3871±0.0169 | 0.3816±0.0083 | +0.0055 | +1.5% | 0.4724 | 0.4375 | +0.35 (small) |
| Narr f1_samples_manual | 0.3871±0.0169 | 0.3816±0.0083 | +0.0055 | +1.5% | 0.4724 | 0.4375 | +0.35 (small) |
| subNarr f1_macro | 0.1337±0.0022 | 0.1292±0.0049 | +0.0046 | +3.5% | 0.0708 | 0.0625 | +1.09 (large) |
| subNarr f1_micro | 0.1219±0.0028 | 0.1173±0.0015 | +0.0046 | +3.9% | 0.0190* | 0.0625 | +1.70 (large) |
| subNarr f1_samples | 0.1393±0.0040 | 0.1355±0.0042 | +0.0038 | +2.8% | 0.0593 | 0.1250 | +1.17 (large) |
| subNarr f1_samples_manual | 0.1393±0.0040 | 0.1355±0.0042 | +0.0038 | +2.8% | 0.0593 | 0.1250 | +1.17 (large) |

### Llama 3.3 70B — EN — t00

- **Actor-Critic**: `actor_critic_together_llama33_70b_en_t00`
- **Baseline**: `baseline_together_llama33_70b_en_t00`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.2386±0.0194 | 0.2186±0.0271 | +0.0200 | +9.2% | 0.2765 | 0.3125 | +0.56 (medium) |
| Narr f1_micro | 0.3034±0.0108 | 0.2684±0.0123 | +0.0351 | +13.1% | 0.0109* | 0.0625 | +2.01 (large) |
| Narr f1_samples | 0.3191±0.0103 | 0.2846±0.0131 | +0.0345 | +12.1% | 0.0254* | 0.0625 | +1.55 (large) |
| Narr f1_samples_manual | 0.3191±0.0103 | 0.2846±0.0131 | +0.0345 | +12.1% | 0.0254* | 0.0625 | +1.55 (large) |
| subNarr f1_macro | 0.0836±0.0089 | 0.0700±0.0080 | +0.0136 | +19.5% | 0.0387* | 0.0625 | +1.36 (large) |
| subNarr f1_micro | 0.0986±0.0067 | 0.0716±0.0050 | +0.0270 | +37.8% | 0.0021** | 0.0625 | +3.16 (large) |
| subNarr f1_samples | 0.1056±0.0069 | 0.0759±0.0035 | +0.0297 | +39.1% | 0.0027** | 0.0625 | +2.95 (large) |
| subNarr f1_samples_manual | 0.1056±0.0069 | 0.0759±0.0035 | +0.0297 | +39.1% | 0.0027** | 0.0625 | +2.95 (large) |

### Llama 3.3 70B — EN — t07

- **Actor-Critic**: `actor_critic_together_llama33_70b_en_t07`
- **Baseline**: `baseline_together_llama33_70b_en_t07`

| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |
|--------|-------------|----------|------|------|----------|------------|-----------|
| Narr f1_macro | 0.2299±0.0204 | 0.2369±0.0146 | -0.0071 | -3.0% | 0.6489 | 0.6250 | -0.22 (small) |
| Narr f1_micro | 0.3001±0.0135 | 0.2847±0.0061 | +0.0154 | +5.4% | 0.0618 | 0.1250 | +1.15 (large) |
| Narr f1_samples | 0.3065±0.0240 | 0.3005±0.0087 | +0.0060 | +2.0% | 0.6463 | 0.6250 | +0.22 (small) |
| Narr f1_samples_manual | 0.3065±0.0240 | 0.3005±0.0087 | +0.0060 | +2.0% | 0.6463 | 0.6250 | +0.22 (small) |
| subNarr f1_macro | 0.0824±0.0110 | 0.0700±0.0082 | +0.0124 | +17.7% | 0.1030 | 0.1250 | +0.94 (large) |
| subNarr f1_micro | 0.0980±0.0091 | 0.0800±0.0028 | +0.0180 | +22.5% | 0.0118* | 0.0625 | +1.96 (large) |
| subNarr f1_samples | 0.1023±0.0129 | 0.0809±0.0050 | +0.0214 | +26.5% | 0.0195* | 0.0625 | +1.69 (large) |
| subNarr f1_samples_manual | 0.1023±0.0129 | 0.0809±0.0050 | +0.0214 | +26.5% | 0.0195* | 0.0625 | +1.69 (large) |

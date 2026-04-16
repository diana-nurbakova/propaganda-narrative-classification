# Confusion Severity Analysis

This report classifies prediction confusions using both taxonomy structure and semantic similarity between labels.

**Severity levels** (least to most severe):
- **same-narrative**: Gold and predicted are siblings under the same parent narrative (expected confusion)
- **same-category**: Different narratives but same domain (URW or CC)
- **cross-category**: Different domains entirely (URW vs CC) — most severe structural error
- **hallucination**: Involves the "Other" label (model predicts unclassifiable or misses all labels)

## Overall Confusion Severity Distribution

| Severity | Count | Percentage | Description |
|----------|-------|------------|-------------|
| same-narrative | 2947 | 16.9% | Sibling subnarratives confused |
| same-category | 13991 | 80.2% | Same domain, different narrative |
| cross-category | 291 | 1.7% | Wrong domain entirely |
| hallucination | 214 | 1.2% | Other label involved |
| **Total** | **17443** | **100%** | |

## Per-Language Confusion Severity

| Language | Total | Same-Narr | Same-Cat | Cross-Cat | Halluc. | Cross-Cat % |
|----------|-------|-----------|----------|-----------|---------|-------------|
| EN | 12222 | 1639 | 10197 | 283 | 103 | 2.3% |
| BG | 1405 | 386 | 989 | 1 | 29 | 0.1% |
| HI | 1079 | 243 | 806 | 1 | 29 | 0.1% |
| PT | 969 | 265 | 661 | 3 | 40 | 0.3% |
| RU | 1768 | 414 | 1338 | 3 | 13 | 0.2% |

## Per-Experiment Confusion Severity

| Experiment | Lang | Total | Same-Narr | Same-Cat | Cross-Cat | Halluc. | Cross % |
|------------|------|-------|-----------|----------|-----------|---------|--------|
| actor_critic_deepseek_bg_t00 | BG | 97 | 27 | 68 | 0 | 2 | 0.0% |
| actor_critic_deepseek_bg_t07 | BG | 76 | 25 | 47 | 0 | 4 | 0.0% |
| actor_critic_deepseek_en_t00 | EN | 180 | 36 | 142 | 0 | 2 | 0.0% |
| actor_critic_deepseek_en_t00_evidence | EN | 157 | 31 | 122 | 0 | 4 | 0.0% |
| actor_critic_deepseek_en_t07 | EN | 199 | 32 | 165 | 0 | 2 | 0.0% |
| actor_critic_deepseek_hi_t00 | HI | 81 | 24 | 53 | 0 | 4 | 0.0% |
| actor_critic_deepseek_pt_t00 | PT | 52 | 11 | 35 | 0 | 6 | 0.0% |
| actor_critic_deepseek_ru_t00 | RU | 88 | 24 | 64 | 0 | 0 | 0.0% |
| actor_critic_deepseek_ru_t07 | RU | 91 | 28 | 63 | 0 | 0 | 0.0% |
| actor_critic_gemini_en_t00 | EN | 221 | 35 | 173 | 12 | 1 | 5.4% |
| actor_critic_gemini_en_t00_v2 | EN | 61 | 12 | 36 | 0 | 13 | 0.0% |
| actor_critic_gemini_en_t07 | EN | 211 | 37 | 165 | 8 | 1 | 3.8% |
| actor_critic_gemini_en_t07_v2 | EN | 47 | 4 | 31 | 0 | 12 | 0.0% |
| actor_critic_gpt5nano_en_t00 | EN | 102 | 16 | 75 | 11 | 0 | 10.8% |
| actor_critic_gpt5nano_en_t07 | EN | 123 | 24 | 92 | 6 | 1 | 4.9% |
| actor_critic_mistral_bg_t00 | BG | 180 | 41 | 138 | 0 | 1 | 0.0% |
| actor_critic_mistral_en_t00 | EN | 320 | 41 | 275 | 3 | 1 | 0.9% |
| actor_critic_mistral_en_t00_evidence | EN | 316 | 42 | 271 | 0 | 3 | 0.0% |
| actor_critic_mistral_en_t07 | EN | 337 | 44 | 288 | 3 | 2 | 0.9% |
| actor_critic_mistral_hi_t00 | HI | 178 | 35 | 141 | 0 | 2 | 0.0% |
| actor_critic_mistral_pt_t00 | PT | 119 | 26 | 91 | 0 | 2 | 0.0% |
| actor_critic_mistral_ru_t00 | RU | 221 | 48 | 172 | 0 | 1 | 0.0% |
| actor_critic_together_llama33_70b_en_t00 | EN | 255 | 36 | 217 | 0 | 2 | 0.0% |
| actor_critic_together_llama33_70b_en_t07 | EN | 254 | 35 | 217 | 0 | 2 | 0.0% |
| agora_deepseek_bg_t00 | BG | 84 | 32 | 50 | 0 | 2 | 0.0% |
| agora_deepseek_bg_t07 | BG | 89 | 33 | 54 | 0 | 2 | 0.0% |
| agora_deepseek_en_t00 | EN | 239 | 35 | 202 | 0 | 2 | 0.0% |
| agora_deepseek_en_t07 | EN | 229 | 36 | 191 | 0 | 2 | 0.0% |
| agora_deepseek_hi_t00 | HI | 77 | 23 | 51 | 0 | 3 | 0.0% |
| agora_deepseek_pt_t00 | PT | 57 | 18 | 33 | 0 | 6 | 0.0% |
| agora_deepseek_ru_t00 | RU | 108 | 33 | 75 | 0 | 0 | 0.0% |
| agora_deepseek_ru_t07 | RU | 98 | 27 | 70 | 0 | 1 | 0.0% |
| agora_gemini_en_t00 | EN | 229 | 37 | 179 | 11 | 2 | 4.8% |
| agora_gemini_en_t07 | EN | 219 | 36 | 173 | 9 | 1 | 4.1% |
| agora_majority_deepseek_pt_t00 | PT | 58 | 21 | 35 | 0 | 2 | 0.0% |
| agora_majority_gpt5nano_bg_t00 | BG | 59 | 15 | 43 | 0 | 1 | 0.0% |
| agora_majority_gpt5nano_en_t00 | EN | 183 | 28 | 143 | 12 | 0 | 6.6% |
| agora_majority_gpt5nano_en_t07 | EN | 172 | 22 | 138 | 12 | 0 | 7.0% |
| agora_majority_gpt5nano_hi_t00 | HI | 33 | 10 | 17 | 0 | 6 | 0.0% |
| agora_majority_gpt5nano_pt_t00 | PT | 30 | 8 | 17 | 0 | 5 | 0.0% |
| agora_majority_gpt5nano_ru_t00 | RU | 59 | 16 | 40 | 0 | 3 | 0.0% |
| agora_majority_mistral_bg_t00 | BG | 176 | 39 | 136 | 0 | 1 | 0.0% |
| agora_majority_mistral_en_t00 | EN | 337 | 42 | 293 | 0 | 2 | 0.0% |
| agora_majority_mistral_en_t00_evidence | EN | 342 | 45 | 293 | 3 | 1 | 0.9% |
| agora_majority_mistral_en_t07 | EN | 343 | 43 | 276 | 22 | 2 | 6.4% |
| agora_majority_mistral_hi_t00 | HI | 167 | 34 | 131 | 0 | 2 | 0.0% |
| agora_majority_mistral_pt_t00 | PT | 121 | 33 | 88 | 0 | 0 | 0.0% |
| agora_majority_mistral_ru_t00 | RU | 224 | 51 | 173 | 0 | 0 | 0.0% |
| agora_majority_together_llama33_70b_bg_t00 | BG | 101 | 27 | 68 | 0 | 6 | 0.0% |
| agora_majority_together_llama33_70b_en_t00 | EN | 339 | 38 | 285 | 15 | 1 | 4.4% |
| agora_majority_together_llama33_70b_en_t07 | EN | 329 | 34 | 277 | 16 | 2 | 4.9% |
| agora_majority_together_llama33_70b_hi_t00 | HI | 103 | 17 | 80 | 0 | 6 | 0.0% |
| agora_majority_together_llama33_70b_pt_t00 | PT | 86 | 16 | 62 | 0 | 8 | 0.0% |
| agora_majority_together_llama33_70b_ru_t00 | RU | 186 | 38 | 146 | 0 | 2 | 0.0% |
| agora_mistral_bg_t00 | BG | 146 | 38 | 106 | 0 | 2 | 0.0% |
| agora_mistral_en_t00 | EN | 299 | 41 | 256 | 0 | 2 | 0.0% |
| agora_mistral_en_t00_evidence | EN | 308 | 41 | 262 | 3 | 2 | 1.0% |
| agora_mistral_en_t07 | EN | 294 | 41 | 250 | 0 | 3 | 0.0% |
| agora_mistral_hi_t00 | HI | 138 | 33 | 103 | 0 | 2 | 0.0% |
| agora_mistral_pt_t00 | PT | 103 | 31 | 72 | 0 | 0 | 0.0% |
| agora_mistral_ru_t00 | RU | 168 | 39 | 127 | 0 | 2 | 0.0% |
| agora_together_llama33_70b_en_t00 | EN | 292 | 30 | 260 | 0 | 2 | 0.0% |
| agora_together_llama33_70b_en_t07 | EN | 254 | 32 | 218 | 0 | 4 | 0.0% |
| agora_union_deepseek_pt_t00 | PT | 66 | 22 | 42 | 0 | 2 | 0.0% |
| agora_union_gpt5nano_en_t00 | EN | 207 | 24 | 169 | 14 | 0 | 6.8% |
| agora_union_gpt5nano_en_t07 | EN | 191 | 25 | 157 | 9 | 0 | 4.7% |
| agora_union_mistral_en_t00 | EN | 371 | 46 | 321 | 3 | 1 | 0.8% |
| agora_union_mistral_en_t07 | EN | 353 | 43 | 304 | 4 | 2 | 1.1% |
| agora_union_together_llama33_70b_en_t00 | EN | 382 | 37 | 325 | 19 | 1 | 5.0% |
| agora_union_together_llama33_70b_en_t07 | EN | 383 | 41 | 341 | 0 | 1 | 0.0% |
| baseline_deepseek_bg_t00 | BG | 92 | 33 | 57 | 0 | 2 | 0.0% |
| baseline_deepseek_bg_t07 | BG | 94 | 32 | 60 | 0 | 2 | 0.0% |
| baseline_deepseek_en_t00 | EN | 242 | 39 | 201 | 0 | 2 | 0.0% |
| baseline_deepseek_en_t00_evidence | EN | 228 | 38 | 187 | 0 | 3 | 0.0% |
| baseline_deepseek_en_t07 | EN | 259 | 39 | 202 | 16 | 2 | 6.2% |
| baseline_deepseek_hi_t00 | HI | 94 | 28 | 64 | 0 | 2 | 0.0% |
| baseline_deepseek_pt_t00 | PT | 58 | 19 | 35 | 0 | 4 | 0.0% |
| baseline_deepseek_pt_t07 | PT | 62 | 21 | 38 | 0 | 3 | 0.0% |
| baseline_deepseek_ru_t00 | RU | 111 | 27 | 83 | 0 | 1 | 0.0% |
| baseline_deepseek_ru_t07 | RU | 121 | 27 | 93 | 0 | 1 | 0.0% |
| baseline_gemini_en_t00 | EN | 240 | 34 | 192 | 12 | 2 | 5.0% |
| baseline_gemini_en_t07 | EN | 99 | 16 | 83 | 0 | 0 | 0.0% |
| baseline_gpt5nano_en_t00 | EN | 158 | 22 | 124 | 11 | 1 | 7.0% |
| baseline_gpt5nano_en_t07 | EN | 162 | 19 | 127 | 14 | 2 | 8.6% |
| baseline_mistral_bg_t00 | BG | 180 | 42 | 136 | 1 | 1 | 0.6% |
| baseline_mistral_en_t00 | EN | 315 | 41 | 269 | 2 | 3 | 0.6% |
| baseline_mistral_en_t00_evidence | EN | 341 | 41 | 295 | 4 | 1 | 1.2% |
| baseline_mistral_en_t07 | EN | 343 | 45 | 295 | 2 | 1 | 0.6% |
| baseline_mistral_hi_t00 | HI | 173 | 34 | 138 | 0 | 1 | 0.0% |
| baseline_mistral_pt_t00 | PT | 119 | 26 | 91 | 0 | 2 | 0.0% |
| baseline_mistral_ru_t00 | RU | 221 | 47 | 173 | 0 | 1 | 0.0% |
| baseline_together_llama33_70b_en_t00 | EN | 351 | 37 | 295 | 17 | 2 | 4.8% |
| baseline_together_llama33_70b_en_t07 | EN | 333 | 36 | 295 | 0 | 2 | 0.0% |
| mdeberta_baseline_bg_t00 | BG | 31 | 2 | 26 | 0 | 3 | 0.0% |
| mdeberta_baseline_en_t00 | EN | 73 | 10 | 50 | 10 | 3 | 13.7% |
| mdeberta_baseline_hi_t00 | HI | 35 | 5 | 28 | 1 | 1 | 2.9% |
| mdeberta_baseline_pt_t00 | PT | 38 | 13 | 22 | 3 | 0 | 7.9% |
| mdeberta_baseline_ru_t00 | RU | 72 | 9 | 59 | 3 | 1 | 4.2% |

## Most Common Cross-Category Confusions

These are the most severe structural errors — the model confuses labels from entirely different domains (URW vs CC).

| Gold Label | Predicted Label | Count | Similarity |
|------------|-----------------|-------|------------|
| URW: Sanctions imposed by Western c | CC: Climate policies have negative | 19 | 0.379 |
| URW: Sanctions imposed by Western c | CC: Criticism of national governme | 18 | 0.256 |
| URW: Sanctions imposed by Western c | CC: Criticism of political organiz | 17 | 0.236 |
| URW: Sanctions imposed by Western c | CC: Other | 17 | 0.000 |
| URW: Sanctions imposed by Western c | CC: Climate movement is alarmist | 16 | 0.231 |
| URW: Sanctions imposed by Western c | CC: Other | 16 | 0.000 |
| URW: Sanctions imposed by Western c | CC: Climate policies are ineffecti | 16 | 0.312 |
| URW: Sanctions imposed by Western c | CC: Renewable energy is costly | 14 | 0.173 |
| URW: Sanctions imposed by Western c | CC: Other | 13 | 0.000 |
| URW: Sanctions imposed by Western c | CC: Criticism of international ent | 11 | 0.294 |
| URW: Sanctions imposed by Western c | CC: Other | 11 | 0.000 |
| URW: Sanctions imposed by Western c | CC: Other | 10 | 0.000 |
| CC: Blaming global elites | URW: Other | 10 | 0.000 |
| CC: Criticism of international ent | URW: Other | 9 | 0.000 |
| URW: Sanctions imposed by Western c | CC: Renewable energy is unreliable | 8 | 0.174 |

## Most Common Same-Category Confusions

Different narratives within the same domain confused. Similarity score indicates semantic relatedness (higher = more understandable confusion).

| Gold Label | Predicted Label | Count | Similarity |
|------------|-----------------|-------|------------|
| Discrediting Ukrainian government a | The West does not care about Ukrain | 110 | 0.715 |
| Discrediting Ukrainian government a | Other | 88 | 0.000 |
| Criticism of political organization | Other | 84 | 0.000 |
| Discrediting Ukrainian government a | The West are the aggressors | 80 | 0.433 |
| Climate movement is alarmist | Other | 77 | 0.000 |
| Climate movement is alarmist | Scientific community is unreliable | 75 | 0.448 |
| Criticism of political organization | Climate policies have negative impa | 69 | 0.697 |
| Discrediting Ukrainian government a | Other | 68 | 0.000 |
| Climate movement is alarmist | Other | 68 | 0.000 |
| Discrediting Ukrainian government a | Western media is an instrument of p | 67 | 0.464 |
| Discrediting Ukrainian government a | Other | 61 | 0.000 |
| Criticism of political organization | Other | 61 | 0.000 |
| Blaming global elites | Other | 56 | 0.000 |
| Russia has international support fr | Other | 56 | 0.000 |
| Ukrainian army is collapsing | Discrediting Ukrainian government a | 54 | 0.539 |
| The West does not care about Ukrain | Discrediting Ukrainian government a | 53 | 0.715 |
| Climate movement is alarmist | Methodologies/metrics used are unre | 53 | 0.576 |
| Russian army is collapsing | Other | 53 | 0.000 |
| Ukrainian army is collapsing | Situation in Ukraine is hopeless | 53 | 0.660 |
| Ukrainian army is collapsing | The West does not care about Ukrain | 53 | 0.521 |
| The West does not care about Ukrain | Ukraine is a puppet of the West | 52 | 0.763 |
| Russian army is collapsing | Ukraine is associated with nazism | 52 | 0.433 |
| Russian army is collapsing | Praise of Russian President Vladimi | 52 | 0.489 |
| Discrediting Ukrainian government a | Other | 52 | 0.000 |
| Criticism of political organization | Climate policies are ineffective | 52 | 0.731 |

## Most Common Same-Narrative Confusions

Confusions between sibling subnarratives under the same parent narrative. These are the most expected errors.

| Parent Narrative | Gold Subnarrative | Predicted Subnarrative | Count | Similarity |
|-----------------|-------------------|----------------------|-------|------------|
| Amplifying Climate Fears | Amplifying existing fears of | Doomsday scenarios for human | 126 | 0.836 |
| Discrediting Ukraine | Discrediting Ukrainian gover | Ukraine is a puppet of the W | 97 | 0.718 |
| Discrediting Ukraine | Discrediting Ukrainian gover | Other | 96 | 0.000 |
| Amplifying Climate Fears | Amplifying existing fears of | Other | 85 | 0.000 |
| Criticism of climate move | Climate movement is alarmist | Other | 77 | 0.000 |
| Criticism of institutions | Criticism of political organ | Other | 71 | 0.000 |
| Criticism of institutions | Criticism of political organ | Criticism of national govern | 67 | 0.886 |
| Discrediting Ukraine | Discrediting Ukrainian gover | Discrediting Ukrainian milit | 62 | 0.913 |
| Discrediting Ukraine | Discrediting Ukrainian gover | Ukraine is associated with n | 59 | 0.818 |
| Speculating war outcomes | Russian army is collapsing | Other | 53 | 0.000 |
| Criticism of institutions | Criticism of international e | Criticism of political organ | 52 | 0.882 |
| Criticism of institutions | Criticism of international e | Other | 46 | 0.000 |
| Discrediting the West, Di | The West does not care about | Other | 44 | 0.000 |
| Discrediting the West, Di | The EU is divided | The West does not care about | 44 | 0.631 |
| Criticism of climate move | Ad hominem attacks on key ac | Climate movement is alarmist | 44 | 0.749 |
| Praise of Russia | Russia has international sup | Other | 43 | 0.000 |
| Blaming the war on others | The West are the aggressors | Other | 42 | 0.000 |
| Discrediting Ukraine | Discrediting Ukrainian gover | Ukraine is a hub for crimina | 41 | 0.714 |
| Controversy about green t | Renewable energy is dangerou | Renewable energy is costly | 40 | 0.845 |
| Criticism of climate poli | Climate policies are only fo | Climate policies have negati | 40 | 0.849 |

## Hallucination Analysis (Other Label)

- Gold is "Other", model predicts a label: 0 cases
- Gold has a label, model predicts "Other": 214 cases

### Labels Most Often Missed (predicted as Other)

| Gold Label | Count |
|------------|-------|
| Amplifying existing fears of global warm | 59 |
| Climate agenda has hidden motives | 36 |
| Russian army is collapsing | 22 |
| Green activities are a form of neo-colon | 12 |
| Criticism of political organizations and | 7 |
| Russia will also attack other countries | 6 |
| Sanctions imposed by Western countries w | 6 |
| Climate policies are only for profit | 6 |
| Discrediting Ukrainian government and of | 6 |
| Russia has international support from a  | 6 |
| The West does not care about Ukraine, on | 5 |
| Russian army will lose all the occupied  | 4 |
| Russia is a guarantor of peace and prosp | 4 |
| Discrediting Ukrainian military | 4 |
| Renewable energy is dangerous | 3 |


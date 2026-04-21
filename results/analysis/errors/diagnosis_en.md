# Error Diagnosis Report

*Generated: 2026-04-21 23:19*

Analyzed **21** experiments across **2402** documents.

## Error Decomposition

- Total false positives (FP): **7583**
  - Same-domain confusion: 7280 (96.0%)
  - Cross-domain FP: 303 (4.0%)
  - Hallucination: 0 (0.0%)
- Total false negatives (FN): **503**
- FP/FN ratio: **15.08**

### Over/Under-Prediction Profile

- Mean |pred| - |gold| per doc: **+2.95**
- Over-predicting docs: **2098**, Under-predicting: **261**, Exact: **43**
- System tends to OVER-PREDICT

## Per-Narrative Error Profile

| Narrative | Support | TP | FP | FN | Precision | Recall | F1 |
|-----------|---------|----|----|----|-----------|---------|----|
| Criticism of climate movement | 480 | 408 | 392 | 72 | 0.51 | 0.85 | 0.64 |
| Discrediting the West, Diplomacy | 319 | 306 | 542 | 13 | 0.36 | 0.96 | 0.52 |
| Discrediting Ukraine | 241 | 211 | 377 | 30 | 0.36 | 0.88 | 0.51 |
| Speculating war outcomes | 241 | 135 | 290 | 106 | 0.32 | 0.56 | 0.41 |
| Criticism of climate policies | 240 | 201 | 604 | 39 | 0.25 | 0.84 | 0.38 |
| Criticism of institutions and authorities | 240 | 177 | 606 | 63 | 0.23 | 0.74 | 0.35 |
| Hidden plots by secret schemes of powerful groups | 160 | 63 | 359 | 97 | 0.15 | 0.39 | 0.22 |
| Blaming the war on others rather than the invader | 81 | 77 | 506 | 4 | 0.13 | 0.95 | 0.23 |
| Overpraising the West | 80 | 61 | 37 | 19 | 0.62 | 0.76 | 0.69 |
| Negative Consequences for the West | 80 | 34 | 483 | 46 | 0.07 | 0.42 | 0.11 |
| Climate change is beneficial | 80 | 79 | 20 | 1 | 0.80 | 0.99 | 0.88 |
| Questioning the measurements and science | 80 | 71 | 290 | 9 | 0.20 | 0.89 | 0.32 |
| Controversy about green technologies | 80 | 76 | 376 | 4 | 0.17 | 0.95 | 0.29 |
| Russia is the Victim | 0 | 0 | 301 | 0 | 0.00 | 0.00 | 0.00 |
| Praise of Russia | 0 | 0 | 224 | 0 | 0.00 | 0.00 | 0.00 |
| Distrust towards Media | 0 | 0 | 424 | 0 | 0.00 | 0.00 | 0.00 |
| Amplifying war-related fears | 0 | 0 | 622 | 0 | 0.00 | 0.00 | 0.00 |
| Downplaying climate change | 0 | 0 | 528 | 0 | 0.00 | 0.00 | 0.00 |
| Amplifying Climate Fears | 0 | 0 | 263 | 0 | 0.00 | 0.00 | 0.00 |
| Green policies are geopolitical instruments | 0 | 0 | 339 | 0 | 0.00 | 0.00 | 0.00 |

## Top Confusion Pairs

Each row shows a gold narrative being predicted as a different narrative.

| # | Gold Narrative | Predicted As | Count | Same Domain |
|---|----------------|-------------|-------|-------------|
| 1 | Criticism of climate movement | Downplaying climate change | 294 | yes |
| 2 | Criticism of climate movement | Questioning the measurements and science | 267 | yes |
| 3 | Discrediting Ukraine | Discrediting the West, Diplomacy | 218 | yes |
| 4 | Discrediting the West, Diplomacy | Blaming the war on others rather than the invader | 216 | yes |
| 5 | Criticism of climate movement | Criticism of institutions and authorities | 201 | yes |
| 6 | Discrediting the West, Diplomacy | Amplifying war-related fears | 188 | yes |
| 7 | Criticism of institutions and authorities | Criticism of climate policies | 180 | yes |
| 8 | Discrediting the West, Diplomacy | Negative Consequences for the West | 180 | yes |
| 9 | Speculating war outcomes | Discrediting Ukraine | 176 | yes |
| 10 | Speculating war outcomes | Discrediting the West, Diplomacy | 176 | yes |
| 11 | Speculating war outcomes | Amplifying war-related fears | 171 | yes |
| 12 | Criticism of climate movement | Amplifying Climate Fears | 154 | yes |
| 13 | Discrediting the West, Diplomacy | Discrediting Ukraine | 154 | yes |
| 14 | Criticism of climate policies | Criticism of institutions and authorities | 150 | yes |
| 15 | Criticism of climate movement | Criticism of climate policies | 149 | yes |
| 16 | Discrediting the West, Diplomacy | Distrust towards Media | 147 | yes |
| 17 | Discrediting Ukraine | Blaming the war on others rather than the invader | 141 | yes |
| 18 | Criticism of climate policies | Controversy about green technologies | 135 | yes |
| 19 | Speculating war outcomes | Praise of Russia | 135 | yes |
| 20 | Criticism of climate policies | Criticism of climate movement | 134 | yes |

## Systematic Errors (consistent across ALL models)

### Systematically Missed Narratives (high FN rate everywhere)

| Narrative | Mean FN Rate | DeepSeek V3 | GPT-5 Nano | Gemini 2.5 Flash | Llama 3.3 70B | Mistral Large |
|-----------|-------------|------|------|------|------|------|
| Hidden plots by secret schemes of powerful groups | 0.57 | 0.67 | 0.56 | 0.50 | 0.68 | 0.41 |

### Systematically Over-Predicted Narratives (high FP rate everywhere)

| Narrative | Mean FP Rate | DeepSeek V3 | GPT-5 Nano | Gemini 2.5 Flash | Llama 3.3 70B | Mistral Large |
|-----------|-------------|------|------|------|------|------|
| Russia is the Victim | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Praise of Russia | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Distrust towards Media | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Amplifying war-related fears | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Downplaying climate change | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Amplifying Climate Fears | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Green policies are geopolitical instruments | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Negative Consequences for the West | 0.95 | 0.91 | 0.98 | 1.00 | 0.94 | 0.89 |
| Blaming the war on others rather than the invader | 0.87 | 0.87 | 0.84 | 0.86 | 0.87 | 0.90 |
| Hidden plots by secret schemes of powerful groups | 0.85 | 0.86 | 0.83 | 0.91 | 0.87 | 0.77 |
| Controversy about green technologies | 0.84 | 0.78 | 0.84 | 0.86 | 0.82 | 0.88 |
| Questioning the measurements and science | 0.81 | 0.80 | 0.80 | 0.82 | 0.79 | 0.83 |
| Criticism of institutions and authorities | 0.78 | 0.72 | 0.81 | 0.80 | 0.77 | 0.77 |
| Criticism of climate policies | 0.75 | 0.79 | 0.75 | 0.75 | 0.72 | 0.76 |
| Speculating war outcomes | 0.68 | 0.45 | 0.69 | 0.74 | 0.75 | 0.79 |
| Discrediting Ukraine | 0.63 | 0.63 | 0.63 | 0.62 | 0.68 | 0.59 |
| Discrediting the West, Diplomacy | 0.62 | 0.63 | 0.57 | 0.56 | 0.67 | 0.67 |
| Criticism of climate movement | 0.50 | 0.47 | 0.54 | 0.52 | 0.39 | 0.60 |

## Model-Specific Error Patterns (high cross-model variance)

| Narrative | Mean FN Rate | Std FN Rate | DeepSeek V3 | GPT-5 Nano | Gemini 2.5 Flash | Llama 3.3 70B | Mistral Large |
|-----------|-------------|------------|------|------|------|------|------|
| Negative Consequences for the West | 0.60 | 0.36 | 0.48 | 0.94 | 1.00 | 0.60 | 0.00 |
| Speculating war outcomes | 0.41 | 0.30 | 0.46 | 0.04 | 0.12 | 0.57 | 0.84 |
| Criticism of institutions and authorities | 0.24 | 0.22 | 0.52 | 0.46 | 0.20 | 0.03 | 0.00 |

## Actionable Recommendations

1. **Low recall for 'Hidden plots by secret schemes of powerful groups'** (R=0.39, support=160): Add more examples or strengthen the definition in prompts.
2. **High over-prediction for 'Blaming the war on others rather than the invader'** (P=0.13, FP=506): Tighten classification criteria or add negative examples.
3. **High over-prediction for 'Discrediting Ukraine'** (P=0.36, FP=377): Tighten classification criteria or add negative examples.
4. **High over-prediction for 'Russia is the Victim'** (P=0.00, FP=301): Tighten classification criteria or add negative examples.
5. **High over-prediction for 'Praise of Russia'** (P=0.00, FP=224): Tighten classification criteria or add negative examples.
6. **High over-prediction for 'Speculating war outcomes'** (P=0.32, FP=290): Tighten classification criteria or add negative examples.
7. **High over-prediction for 'Discrediting the West, Diplomacy'** (P=0.36, FP=542): Tighten classification criteria or add negative examples.
8. **High over-prediction for 'Negative Consequences for the West'** (P=0.07, FP=483): Tighten classification criteria or add negative examples.
9. **High over-prediction for 'Distrust towards Media'** (P=0.00, FP=424): Tighten classification criteria or add negative examples.
10. **High over-prediction for 'Amplifying war-related fears'** (P=0.00, FP=622): Tighten classification criteria or add negative examples.
11. **High over-prediction for 'Hidden plots by secret schemes of powerful groups'** (P=0.15, FP=359): Tighten classification criteria or add negative examples.
12. **High over-prediction for 'Criticism of climate policies'** (P=0.25, FP=604): Tighten classification criteria or add negative examples.
13. **High over-prediction for 'Criticism of institutions and authorities'** (P=0.23, FP=606): Tighten classification criteria or add negative examples.
14. **High over-prediction for 'Downplaying climate change'** (P=0.00, FP=528): Tighten classification criteria or add negative examples.
15. **High over-prediction for 'Questioning the measurements and science'** (P=0.20, FP=290): Tighten classification criteria or add negative examples.
16. **High over-prediction for 'Controversy about green technologies'** (P=0.17, FP=376): Tighten classification criteria or add negative examples.
17. **High over-prediction for 'Amplifying Climate Fears'** (P=0.00, FP=263): Tighten classification criteria or add negative examples.
18. **High over-prediction for 'Green policies are geopolitical instruments'** (P=0.00, FP=339): Tighten classification criteria or add negative examples.
19. **Frequent confusion: 'Criticism of climate movement' predicted as 'Downplaying climate change'** (294 times, same domain): Add disambiguation guidance between these two narratives.
20. **Frequent confusion: 'Criticism of climate movement' predicted as 'Questioning the measurements and science'** (267 times, same domain): Add disambiguation guidance between these two narratives.
21. **Frequent confusion: 'Discrediting Ukraine' predicted as 'Discrediting the West, Diplomacy'** (218 times, same domain): Add disambiguation guidance between these two narratives.
22. **Frequent confusion: 'Discrediting the West, Diplomacy' predicted as 'Blaming the war on others rather than the invader'** (216 times, same domain): Add disambiguation guidance between these two narratives.
23. **Frequent confusion: 'Criticism of climate movement' predicted as 'Criticism of institutions and authorities'** (201 times, same domain): Add disambiguation guidance between these two narratives.
24. **Systematic miss across ALL models: 'Hidden plots by secret schemes of powerful groups'** (mean FN rate=0.57): This narrative may need fundamentally different prompt strategy.

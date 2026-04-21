# Document Difficulty Analysis

*Generated: 2026-04-21 23:19*

## Summary

- Total documents analyzed: **30**
- Mean difficulty (1 - hF1): **0.619**
- Median difficulty: **0.622**
- Perfect (hF1=1.0): **0** documents
- Very hard (hF1<0.3): **5** documents

## Top 15 Hardest Documents

| # | Document | Mean hF1 | Std | Min | Max | #Exp | #Runs | Gold Narratives |
|---|----------|----------|-----|-----|-----|------|-------|-----------------|
| 1 | EN_CC_200054.txt | 0.137 | 0.250 | 0.000 | 0.800 | 20 | 80 | Hidden plots by secret schemes of powerful groups |
| 2 | EN_UA_DEV_100002.txt | 0.220 | 0.111 | 0.000 | 0.571 | 20 | 80 | Speculating war outcomes |
| 3 | EN_UA_DEV_100033.txt | 0.226 | 0.102 | 0.000 | 0.471 | 21 | 81 | Speculating war outcomes |
| 4 | EN_UA_DEV_100026.txt | 0.253 | 0.225 | 0.000 | 0.800 | 20 | 80 | Negative Consequences for the West |
| 5 | EN_UA_DEV_20.txt | 0.293 | 0.089 | 0.154 | 0.471 | 21 | 81 | Discrediting Ukraine |
| 6 | EN_CC_200035.txt | 0.330 | 0.219 | 0.000 | 0.615 | 20 | 80 | Criticism of institutions and authorities |
| 7 | EN_CC_200036.txt | 0.335 | 0.120 | 0.000 | 0.750 | 20 | 80 | Criticism of climate movement |
| 8 | EN_UA_DEV_213.txt | 0.337 | 0.057 | 0.160 | 0.421 | 21 | 81 | Blaming the war on others rather than the invader |
| 9 | EN_CC_200077.txt | 0.339 | 0.172 | 0.000 | 0.615 | 20 | 80 | Criticism of climate policies |
| 10 | EN_CC_200033.txt | 0.342 | 0.135 | 0.000 | 0.545 | 20 | 80 | Criticism of climate movement |
| 11 | EN_CC_200071.txt | 0.348 | 0.143 | 0.000 | 0.571 | 20 | 80 | Criticism of climate policies |
| 12 | EN_UA_DEV_100005.txt | 0.351 | 0.095 | 0.000 | 0.600 | 20 | 79 | Discrediting the West, Diplomacy |
| 13 | EN_UA_DEV_214.txt | 0.363 | 0.055 | 0.261 | 0.500 | 21 | 80 | Discrediting the West, Diplomacy |
| 14 | EN_CC_200047.txt | 0.369 | 0.162 | 0.000 | 0.667 | 20 | 80 | Hidden plots by secret schemes of powerful groups |
| 15 | EN_CC_200034.txt | 0.377 | 0.151 | 0.000 | 0.667 | 20 | 80 | Criticism of climate movement |

## Error Patterns in Hard Documents

### 1. EN_CC_200054.txt (hF1=0.137)

- **Gold**: Hidden plots by secret schemes of powerful groups
- **Labels**: 1 narr, 1 sub
- **Evaluated in**: 80 runs
- **Most missed (FN)**: Hidden plots by secret schemes of powerful groups (65/80)
- **Most over-predicted (FP)**: Criticism of climate policies (17/80), Criticism of institutions and authorities (17/80), Controversy about green technologies (13/80), Green policies are geopolitical instruments (12/80), Criticism of climate movement (4/80)

### 2. EN_UA_DEV_100002.txt (hF1=0.220)

- **Gold**: Speculating war outcomes
- **Labels**: 1 narr, 1 sub
- **Evaluated in**: 80 runs
- **Most missed (FN)**: Speculating war outcomes (57/80)
- **Most over-predicted (FP)**: Discrediting Ukraine (79/80), Amplifying war-related fears (77/80), Discrediting the West, Diplomacy (77/80), Russia is the Victim (45/80), Praise of Russia (44/80)

### 3. EN_UA_DEV_100033.txt (hF1=0.226)

- **Gold**: Speculating war outcomes
- **Labels**: 1 narr, 1 sub
- **Evaluated in**: 81 runs
- **Most missed (FN)**: Speculating war outcomes (23/81)
- **Most over-predicted (FP)**: Amplifying war-related fears (77/81), Discrediting Ukraine (77/81), Discrediting the West, Diplomacy (76/81), Praise of Russia (71/81), Negative Consequences for the West (59/81)

### 4. EN_UA_DEV_100026.txt (hF1=0.253)

- **Gold**: Negative Consequences for the West
- **Labels**: 1 narr, 1 sub
- **Evaluated in**: 80 runs
- **Most missed (FN)**: Negative Consequences for the West (46/80)
- **Most over-predicted (FP)**: Discrediting the West, Diplomacy (34/80), Blaming the war on others rather than the invader (31/80), Criticism of climate policies (31/80), Criticism of institutions and authorities (30/80), Controversy about green technologies (28/80)

### 5. EN_UA_DEV_20.txt (hF1=0.293)

- **Gold**: Discrediting Ukraine
- **Labels**: 1 narr, 1 sub
- **Evaluated in**: 81 runs
- **Most missed (FN)**: Discrediting Ukraine (29/81)
- **Most over-predicted (FP)**: Amplifying war-related fears (81/81), Blaming the war on others rather than the invader (80/81), Discrediting the West, Diplomacy (79/81), Speculating war outcomes (54/81), Negative Consequences for the West (29/81)

### 6. EN_CC_200035.txt (hF1=0.330)

- **Gold**: Criticism of institutions and authorities
- **Labels**: 1 narr, 1 sub
- **Evaluated in**: 80 runs
- **Most missed (FN)**: Criticism of institutions and authorities (41/80)
- **Most over-predicted (FP)**: Green policies are geopolitical instruments (55/80), Criticism of climate policies (53/80), Controversy about green technologies (48/80), Hidden plots by secret schemes of powerful groups (3/80)

### 7. EN_CC_200036.txt (hF1=0.335)

- **Gold**: Criticism of climate movement
- **Labels**: 1 narr, 1 sub
- **Evaluated in**: 80 runs
- **Most missed (FN)**: Criticism of climate movement (6/80)
- **Most over-predicted (FP)**: Questioning the measurements and science (68/80), Downplaying climate change (62/80), Controversy about green technologies (58/80), Criticism of climate policies (49/80), Criticism of institutions and authorities (49/80)

### 8. EN_UA_DEV_213.txt (hF1=0.337)

- **Gold**: Blaming the war on others rather than the invader
- **Labels**: 1 narr, 1 sub
- **Evaluated in**: 81 runs
- **Most missed (FN)**: Blaming the war on others rather than the invader (4/81)
- **Most over-predicted (FP)**: Amplifying war-related fears (81/81), Distrust towards Media (81/81), Discrediting the West, Diplomacy (81/81), Negative Consequences for the West (55/81), Russia is the Victim (50/81)

### 9. EN_CC_200077.txt (hF1=0.339)

- **Gold**: Criticism of climate policies
- **Labels**: 1 narr, 1 sub
- **Evaluated in**: 80 runs
- **Most missed (FN)**: Criticism of climate policies (15/80)
- **Most over-predicted (FP)**: Controversy about green technologies (65/80), Criticism of institutions and authorities (65/80), Green policies are geopolitical instruments (49/80), Criticism of climate movement (41/80), Hidden plots by secret schemes of powerful groups (33/80)

### 10. EN_CC_200033.txt (hF1=0.342)

- **Gold**: Criticism of climate movement
- **Labels**: 1 narr, 0 sub
- **Evaluated in**: 80 runs
- **Most missed (FN)**: Criticism of climate movement (9/80)
- **Most over-predicted (FP)**: Criticism of institutions and authorities (57/80), Hidden plots by secret schemes of powerful groups (52/80), Green policies are geopolitical instruments (29/80), Criticism of climate policies (24/80), Controversy about green technologies (16/80)

## Cross-Model Difficulty Agreement

Spearman rank correlation of per-document difficulty between models.
High correlation = models agree on which documents are hard.

| Model | DeepSeek V3 | GPT-5 Nano | Gemini 2.5 Flash | Llama 3.3 70B | Mistral Large |
|-------|------|------|------|------|------|
| DeepSeek V3 | 1.00 | 0.38 | 0.48 | 0.28 | 0.56 |
| GPT-5 Nano | 0.38 | 1.00 | 0.72 | 0.17 | 0.21 |
| Gemini 2.5 Flash | 0.48 | 0.72 | 1.00 | 0.56 | 0.41 |
| Llama 3.3 70B | 0.28 | 0.17 | 0.56 | 1.00 | 0.66 |
| Mistral Large | 0.56 | 0.21 | 0.41 | 0.66 | 1.00 |

## Consistently Hard Documents (all models struggle)

| Document | Mean hF1 | Cross-model Std | Per-model Means |
|----------|----------|-----------------|-----------------|
| EN_UA_DEV_100002.txt | 0.220 | 0.110 | DeepSeek V3=0.20, Gemini 2.5 Flash=0.20, GPT-5 Nano=0.41, Mistral Large=0.15, Llama 3.3 70B=0.15 |
| EN_UA_DEV_100033.txt | 0.226 | 0.079 | DeepSeek V3=0.29, Gemini 2.5 Flash=0.21, GPT-5 Nano=0.30, Mistral Large=0.11, Llama 3.3 70B=0.17 |
| EN_UA_DEV_100026.txt | 0.253 | 0.134 | DeepSeek V3=0.30, Gemini 2.5 Flash=0.10, GPT-5 Nano=0.16, Mistral Large=0.45, Llama 3.3 70B=0.21 |
| EN_UA_DEV_20.txt | 0.293 | 0.062 | DeepSeek V3=0.35, Gemini 2.5 Flash=0.27, GPT-5 Nano=0.36, Mistral Large=0.27, Llama 3.3 70B=0.21 |
| EN_CC_200036.txt | 0.335 | 0.063 | DeepSeek V3=0.31, Gemini 2.5 Flash=0.29, GPT-5 Nano=0.40, Mistral Large=0.24, Llama 3.3 70B=0.36 |
| EN_UA_DEV_213.txt | 0.337 | 0.034 | DeepSeek V3=0.37, Gemini 2.5 Flash=0.28, GPT-5 Nano=0.31, Mistral Large=0.31, Llama 3.3 70B=0.35 |
| EN_CC_200077.txt | 0.339 | 0.095 | DeepSeek V3=0.21, Gemini 2.5 Flash=0.37, GPT-5 Nano=0.45, Mistral Large=0.30, Llama 3.3 70B=0.40 |
| EN_CC_200033.txt | 0.342 | 0.064 | DeepSeek V3=0.27, Gemini 2.5 Flash=0.35, GPT-5 Nano=0.43, Mistral Large=0.29, Llama 3.3 70B=0.37 |
| EN_CC_200071.txt | 0.348 | 0.068 | DeepSeek V3=0.25, Gemini 2.5 Flash=0.36, GPT-5 Nano=0.35, Mistral Large=0.34, Llama 3.3 70B=0.44 |
| EN_UA_DEV_100005.txt | 0.351 | 0.068 | DeepSeek V3=0.35, Gemini 2.5 Flash=0.35, GPT-5 Nano=0.42, Mistral Large=0.23, Llama 3.3 70B=0.35 |
| EN_UA_DEV_214.txt | 0.363 | 0.039 | DeepSeek V3=0.33, Gemini 2.5 Flash=0.33, GPT-5 Nano=0.40, Mistral Large=0.33, Llama 3.3 70B=0.40 |
| EN_CC_200034.txt | 0.377 | 0.089 | DeepSeek V3=0.25, Gemini 2.5 Flash=0.45, GPT-5 Nano=0.40, Mistral Large=0.37, Llama 3.3 70B=0.47 |
| EN_UA_DEV_22.txt | 0.380 | 0.089 | DeepSeek V3=0.45, Gemini 2.5 Flash=0.34, GPT-5 Nano=0.48, Mistral Large=0.39, Llama 3.3 70B=0.26 |
| EN_UA_DEV_100013.txt | 0.386 | 0.047 | DeepSeek V3=0.44, Gemini 2.5 Flash=0.32, GPT-5 Nano=0.38, Mistral Large=0.41, Llama 3.3 70B=0.35 |

## Model-Specific Failures (high cross-model variance)

| Document | Mean hF1 | Cross-model Std | Per-model Means |
|----------|----------|-----------------|-----------------|
| EN_UA_DEV_100029.txt | 0.425 | 0.438 | DeepSeek V3=0.33, Gemini 2.5 Flash=0.97, GPT-5 Nano=0.97, Mistral Large=0.06, Llama 3.3 70B=0.18 |
| EN_CC_200054.txt | 0.137 | 0.243 | DeepSeek V3=0.00, Gemini 2.5 Flash=0.00, GPT-5 Nano=0.57, Mistral Large=0.08, Llama 3.3 70B=0.04 |

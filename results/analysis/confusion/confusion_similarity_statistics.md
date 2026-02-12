# Semantic Similarity Analysis of Prediction Confusions

This report analyzes how semantically related the confused label pairs are,
using embedding-based similarity (all-MiniLM-L6-v2) from the semantic hierarchy.

**Key question**: Are most confusions between semantically similar labels (expected/mild)
or between unrelated labels (severe errors)?

## 1. Overall Similarity Statistics

| Metric | All Confusions (n=17443) | Excl. 'Other' (n=11168) |
|--------|-----|-----|
| Mean similarity | 0.3759 | 0.5870 |
| Median similarity | 0.4620 | 0.5847 |
| Std deviation | 0.3039 | 0.1424 |
| 25th percentile | 0.0000 | 0.4799 |
| 75th percentile | 0.6359 | 0.6952 |
| Min | 0.0000 | 0.0000 |
| Max | 0.9134 | 0.9134 |

## 2. Similarity Band Distribution

Classifying confusions by how semantically similar the confused pairs are:

| Similarity Band | Count | % | Interpretation |
|-----------------|-------|---|----------------|
| Very high (>0.7) | 2616 | 15.0% | Near-synonymous labels, highly expected confusion |
| High (0.5-0.7) | 5254 | 30.1% | Related labels, understandable confusion |
| Moderate (0.3-0.5) | 3113 | 17.8% | Somewhat related, concerning but not severe |
| Low (0.1-0.3) | 179 | 1.0% | Loosely related, significant error |
| Very low (<0.1) | 6281 | 36.0% | Unrelated or involves 'Other' label, severe error |

### Excluding 'Other' label confusions

| Similarity Band | Count | % |
|-----------------|-------|---|
| Very high (>0.7) | 2616 | 23.4% |
| High (0.5-0.7) | 5254 | 47.0% |
| Moderate (0.3-0.5) | 3113 | 27.9% |
| Low (0.1-0.3) | 179 | 1.6% |
| Very low (<0.1) | 6 | 0.1% |

## 3. Similarity Distribution by Structural Severity

How do similarity scores differ across the taxonomy-based severity levels?

| Severity Level | Count | Mean Sim | Median Sim | Std | Description |
|----------------|-------|----------|------------|-----|-------------|
| same-narrative | 2947 | 0.4649 | 0.7064 | 0.3898 | Sibling subnarratives under the same parent narrative |
| same-category | 13991 | 0.3673 | 0.4606 | 0.2791 | Different narratives within the same domain (URW or CC) |
| cross-category | 291 | 0.1645 | 0.2123 | 0.1390 | Confusing URW with CC labels — most severe structural error |
| hallucination | 214 | 0.0000 | 0.0000 | 0.0000 | Involves 'Other' label (missed or hallucinated) |

### same-narrative confusions (excl. Other)

| Similarity Band | Count | % |
|-----------------|-------|---|
| Very high (>0.7) | 1475 | 84.4% |
| High (0.5-0.7) | 272 | 15.6% |
| Moderate (0.3-0.5) | 0 | 0.0% |
| Low (0.1-0.3) | 0 | 0.0% |
| Very low (<0.1) | 0 | 0.0% |

### same-category confusions (excl. Other)

| Similarity Band | Count | % |
|-----------------|-------|---|
| Very high (>0.7) | 1141 | 12.4% |
| High (0.5-0.7) | 4982 | 53.9% |
| Moderate (0.3-0.5) | 3058 | 33.1% |
| Low (0.1-0.3) | 56 | 0.6% |
| Very low (<0.1) | 1 | 0.0% |

## 4. Severity by Model

Comparing how different models distribute across severity levels and similarity scores.

| Model | Total | Same-Narr % | Same-Cat % | Cross-Cat % | Halluc % | Mean Sim (excl. Other) |
|-------|-------|-------------|------------|-------------|----------|------------------------|
| DeepSeek | 3487 | 23.5% | 74.0% | 0.5% | 2.0% | 0.6123 |
| GPT-5 Nano | 1479 | 15.5% | 77.2% | 6.0% | 1.3% | 0.5970 |
| Gemini | 1327 | 15.9% | 77.8% | 3.9% | 2.4% | 0.5890 |
| Mistral | 7253 | 16.4% | 82.2% | 0.7% | 0.6% | 0.5855 |
| Together Llama | 3648 | 12.4% | 84.6% | 1.8% | 1.1% | 0.5676 |
| mDeBERTa | 249 | 15.7% | 74.3% | 6.8% | 3.2% | 0.5358 |

## 5. Severity by Method

| Method | Total | Same-Narr % | Same-Cat % | Cross-Cat % | Halluc % | Mean Sim (excl. Other) |
|--------|-------|-------------|------------|-------------|----------|------------------------|
| actor_critic | 3966 | 18.0% | 79.2% | 1.1% | 1.7% | 0.5932 |
| agora | 3431 | 18.5% | 79.6% | 0.7% | 1.2% | 0.5958 |
| agora_majority | 3448 | 16.7% | 79.5% | 2.3% | 1.5% | 0.5827 |
| agora_union | 1953 | 12.2% | 84.9% | 2.5% | 0.4% | 0.5785 |
| baseline | 4396 | 16.9% | 80.4% | 1.8% | 0.9% | 0.5854 |
| mdeberta | 249 | 15.7% | 74.3% | 6.8% | 3.2% | 0.5358 |

## 6. Severity by Language

| Language | Total | Same-Narr % | Same-Cat % | Cross-Cat % | Halluc % | Mean Sim (excl. Other) |
|----------|-------|-------------|------------|-------------|----------|------------------------|
| EN | 12222 | 13.4% | 83.4% | 2.3% | 0.8% | 0.5843 |
| BG | 1405 | 27.5% | 70.4% | 0.1% | 2.1% | 0.6294 |
| HI | 1079 | 22.5% | 74.7% | 0.1% | 2.7% | 0.5531 |
| PT | 969 | 27.3% | 68.2% | 0.3% | 4.1% | 0.6389 |
| RU | 1768 | 23.4% | 75.7% | 0.2% | 0.7% | 0.5681 |

## 7. Mean Similarity by Model x Language (excl. Other)

| Model | EN | BG | HI | PT | RU | Overall |
|-------|------|------|------|------|------|---------|
| DeepSeek | 0.605 | 0.656 | 0.587 | 0.658 | 0.584 | 0.612 |
| GPT-5 Nano | 0.592 | 0.657 | 0.587 | 0.656 | 0.613 | 0.597 |
| Gemini | 0.589 | — | — | — | — | 0.589 |
| Mistral | 0.588 | 0.611 | 0.543 | 0.633 | 0.559 | 0.586 |
| Together Llama | 0.565 | 0.618 | 0.549 | 0.620 | 0.570 | 0.568 |
| mDeBERTa | 0.552 | 0.587 | 0.504 | 0.566 | 0.507 | 0.536 |

## 8. Key Findings

**Excluding 'Other' label confusions (11168 pairs):**

- **70.5%** of confusions are between semantically **similar** labels (sim >= 0.5) — expected/understandable errors
- **27.9%** are between **moderately related** labels (0.3 <= sim < 0.5) — concerning but explainable
- **1.7%** are between **weakly related** labels (sim < 0.3) — severe or unexpected errors

**Model comparison:**
- Highest mean confusion similarity (most expected errors): **DeepSeek** (0.6123)
- Lowest mean confusion similarity (most severe errors): **mDeBERTa** (0.5358)

**Method comparison:**
- Highest mean confusion similarity: **agora** (0.5958)
- Lowest mean confusion similarity: **mdeberta** (0.5358)

**Conclusion:** The median confusion similarity is **0.5847**. 
Most confusions occur between semantically related labels, suggesting models
struggle primarily with fine-grained distinctions within related topics rather than
making fundamentally wrong categorizations.

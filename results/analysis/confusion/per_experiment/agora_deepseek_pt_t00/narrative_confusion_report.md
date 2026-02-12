# Narrative Confusion Analysis Report

## Narrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| URW: Discrediting Ukraine | 1 | 0 | 0 | 1 | 1 | 1.000 | 1.000 | 1.000 |
| URW: Russia is the Victim | 2 | 0 | 0 | 2 | 2 | 1.000 | 1.000 | 1.000 |
| CC: Criticism of institutions and authorities | 4 | 1 | 0 | 4 | 5 | 0.800 | 1.000 | 0.889 |
| CC: Criticism of climate policies | 2 | 2 | 0 | 2 | 4 | 0.500 | 1.000 | 0.667 |
| URW: Praise of Russia | 1 | 1 | 1 | 2 | 2 | 0.500 | 0.500 | 0.500 |
| CC: Amplifying Climate Fears | 4 | 2 | 9 | 13 | 6 | 0.667 | 0.308 | 0.421 |
| URW: Discrediting the West, Diplomacy | 1 | 4 | 0 | 1 | 5 | 0.200 | 1.000 | 0.333 |
| CC: Controversy about green technologies | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of climate movement | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| CC: Green policies are geopolitical instruments | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| Other | 0 | 9 | 0 | 0 | 9 | 0.000 | 0.000 | 0.000 |
| URW: Blaming the war on others rather than the invader | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| URW: Negative Consequences for the West | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |

## Most Common Narrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | CC: Amplifying Climate Fears | Other | 9 | Model predicted 'Other' when 'CC: Amplifying Climate Fears' was true |
| 2 | CC: Criticism of institutions and author... | CC: Amplifying Climate Fears | 2 | Model predicted 'CC: Amplifying Climate Fears' when 'CC: Criticism of institutions and author...' was true |
| 3 | CC: Criticism of institutions and author... | CC: Criticism of climate policies | 2 | Model predicted 'CC: Criticism of climate policies' when 'CC: Criticism of institutions and author...' was true |
| 4 | URW: Praise of Russia | URW: Discrediting the West, Diplomacy | 2 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Praise of Russia' was true |
| 5 | CC: Criticism of climate policies | CC: Controversy about green technologies | 1 | Model predicted 'CC: Controversy about green technologies' when 'CC: Criticism of climate policies' was true |
| 6 | CC: Criticism of climate policies | CC: Criticism of institutions and author... | 1 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Criticism of climate policies' was true |
| 7 | CC: Criticism of institutions and author... | CC: Criticism of climate movement | 1 | Model predicted 'CC: Criticism of climate movement' when 'CC: Criticism of institutions and author...' was true |
| 8 | CC: Criticism of institutions and author... | CC: Green policies are geopolitical inst... | 1 | Model predicted 'CC: Green policies are geopolitical inst...' when 'CC: Criticism of institutions and author...' was true |
| 9 | URW: Discrediting Ukraine | URW: Blaming the war on others rather th... | 1 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting Ukraine' was true |
| 10 | URW: Discrediting Ukraine | URW: Discrediting the West, Diplomacy | 1 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Discrediting Ukraine' was true |
| 11 | URW: Discrediting the West, Diplomacy | URW: Negative Consequences for the West | 1 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Discrediting the West, Diplomacy' was true |
| 12 | URW: Discrediting the West, Diplomacy | URW: Praise of Russia | 1 | Model predicted 'URW: Praise of Russia' when 'URW: Discrediting the West, Diplomacy' was true |
| 13 | URW: Praise of Russia | URW: Blaming the war on others rather th... | 1 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Praise of Russia' was true |
| 14 | URW: Praise of Russia | URW: Negative Consequences for the West | 1 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Praise of Russia' was true |
| 15 | URW: Russia is the Victim | URW: Blaming the war on others rather th... | 1 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Russia is the Victim' was true |
| 16 | URW: Russia is the Victim | URW: Discrediting the West, Diplomacy | 1 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Russia is the Victim' was true |
| 17 | URW: Russia is the Victim | URW: Negative Consequences for the West | 1 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Russia is the Victim' was true |

## Narrative Label-Specific Confusion Analysis


### URW: Discrediting Ukraine

When **URW: Discrediting Ukraine** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times

### URW: Russia is the Victim

When **URW: Russia is the Victim** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Negative Consequences for the West**: 1 times

### CC: Criticism of institutions and authorities

When **CC: Criticism of institutions and authorities** is the true label, it is often confused with:

- **CC: Amplifying Climate Fears**: 2 times
- **CC: Criticism of climate policies**: 2 times
- **CC: Criticism of climate movement**: 1 times
- **CC: Green policies are geopolitical instruments**: 1 times

### CC: Criticism of climate policies

When **CC: Criticism of climate policies** is the true label, it is often confused with:

- **CC: Controversy about green technologies**: 1 times
- **CC: Criticism of institutions and authorities**: 1 times

### URW: Praise of Russia

When **URW: Praise of Russia** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 2 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Negative Consequences for the West**: 1 times

### CC: Amplifying Climate Fears

When **CC: Amplifying Climate Fears** is the true label, it is often confused with:

- **Other**: 9 times

### URW: Discrediting the West, Diplomacy

When **URW: Discrediting the West, Diplomacy** is the true label, it is often confused with:

- **URW: Negative Consequences for the West**: 1 times
- **URW: Praise of Russia**: 1 times

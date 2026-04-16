# Narrative Confusion Analysis Report

## Narrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| CC: Criticism of institutions and authorities | 4 | 1 | 0 | 4 | 5 | 0.800 | 1.000 | 0.889 |
| URW: Discrediting Ukraine | 1 | 1 | 0 | 1 | 2 | 0.500 | 1.000 | 0.667 |
| URW: Praise of Russia | 1 | 1 | 1 | 2 | 2 | 0.500 | 0.500 | 0.500 |
| URW: Discrediting the West, Diplomacy | 1 | 4 | 0 | 1 | 5 | 0.200 | 1.000 | 0.333 |
| CC: Criticism of climate policies | 1 | 3 | 1 | 2 | 4 | 0.250 | 0.500 | 0.333 |
| URW: Russia is the Victim | 1 | 4 | 1 | 2 | 5 | 0.200 | 0.500 | 0.286 |
| CC: Amplifying Climate Fears | 1 | 1 | 12 | 13 | 2 | 0.500 | 0.077 | 0.133 |
| CC: Controversy about green technologies | 0 | 4 | 0 | 0 | 4 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of climate movement | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| CC: Downplaying climate change | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| CC: Green policies are geopolitical instruments | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| Other | 0 | 14 | 0 | 0 | 14 | 0.000 | 0.000 | 0.000 |
| URW: Blaming the war on others rather than the invader | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Distrust towards Media | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Negative Consequences for the West | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |

## Most Common Narrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | CC: Amplifying Climate Fears | Other | 12 | Model predicted 'Other' when 'CC: Amplifying Climate Fears' was true |
| 2 | CC: Criticism of institutions and author... | CC: Controversy about green technologies | 3 | Model predicted 'CC: Controversy about green technologies' when 'CC: Criticism of institutions and author...' was true |
| 3 | CC: Criticism of institutions and author... | CC: Criticism of climate policies | 3 | Model predicted 'CC: Criticism of climate policies' when 'CC: Criticism of institutions and author...' was true |
| 4 | CC: Criticism of institutions and author... | CC: Criticism of climate movement | 2 | Model predicted 'CC: Criticism of climate movement' when 'CC: Criticism of institutions and author...' was true |
| 5 | CC: Criticism of institutions and author... | CC: Downplaying climate change | 2 | Model predicted 'CC: Downplaying climate change' when 'CC: Criticism of institutions and author...' was true |
| 6 | CC: Criticism of institutions and author... | CC: Green policies are geopolitical inst... | 2 | Model predicted 'CC: Green policies are geopolitical inst...' when 'CC: Criticism of institutions and author...' was true |
| 7 | URW: Praise of Russia | URW: Discrediting the West, Diplomacy | 2 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Praise of Russia' was true |
| 8 | URW: Praise of Russia | URW: Russia is the Victim | 2 | Model predicted 'URW: Russia is the Victim' when 'URW: Praise of Russia' was true |
| 9 | CC: Criticism of climate policies | CC: Controversy about green technologies | 1 | Model predicted 'CC: Controversy about green technologies' when 'CC: Criticism of climate policies' was true |
| 10 | CC: Criticism of climate policies | CC: Criticism of institutions and author... | 1 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Criticism of climate policies' was true |
| 11 | CC: Criticism of climate policies | Other | 1 | Model predicted 'Other' when 'CC: Criticism of climate policies' was true |
| 12 | CC: Criticism of institutions and author... | CC: Amplifying Climate Fears | 1 | Model predicted 'CC: Amplifying Climate Fears' when 'CC: Criticism of institutions and author...' was true |
| 13 | URW: Discrediting Ukraine | URW: Blaming the war on others rather th... | 1 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting Ukraine' was true |
| 14 | URW: Discrediting Ukraine | URW: Discrediting the West, Diplomacy | 1 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Discrediting Ukraine' was true |
| 15 | URW: Discrediting Ukraine | URW: Russia is the Victim | 1 | Model predicted 'URW: Russia is the Victim' when 'URW: Discrediting Ukraine' was true |
| 16 | URW: Discrediting the West, Diplomacy | URW: Negative Consequences for the West | 1 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Discrediting the West, Diplomacy' was true |
| 17 | URW: Discrediting the West, Diplomacy | URW: Praise of Russia | 1 | Model predicted 'URW: Praise of Russia' when 'URW: Discrediting the West, Diplomacy' was true |
| 18 | URW: Discrediting the West, Diplomacy | URW: Russia is the Victim | 1 | Model predicted 'URW: Russia is the Victim' when 'URW: Discrediting the West, Diplomacy' was true |
| 19 | URW: Praise of Russia | URW: Blaming the war on others rather th... | 1 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Praise of Russia' was true |
| 20 | URW: Praise of Russia | URW: Discrediting Ukraine | 1 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Praise of Russia' was true |

## Narrative Label-Specific Confusion Analysis


### CC: Criticism of institutions and authorities

When **CC: Criticism of institutions and authorities** is the true label, it is often confused with:

- **CC: Controversy about green technologies**: 3 times
- **CC: Criticism of climate policies**: 3 times
- **CC: Criticism of climate movement**: 2 times
- **CC: Downplaying climate change**: 2 times
- **CC: Green policies are geopolitical instruments**: 2 times

### URW: Discrediting Ukraine

When **URW: Discrediting Ukraine** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Russia is the Victim**: 1 times

### URW: Praise of Russia

When **URW: Praise of Russia** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 2 times
- **URW: Russia is the Victim**: 2 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting Ukraine**: 1 times

### URW: Discrediting the West, Diplomacy

When **URW: Discrediting the West, Diplomacy** is the true label, it is often confused with:

- **URW: Negative Consequences for the West**: 1 times
- **URW: Praise of Russia**: 1 times
- **URW: Russia is the Victim**: 1 times

### CC: Criticism of climate policies

When **CC: Criticism of climate policies** is the true label, it is often confused with:

- **CC: Controversy about green technologies**: 1 times
- **CC: Criticism of institutions and authorities**: 1 times
- **Other**: 1 times

### URW: Russia is the Victim

When **URW: Russia is the Victim** is the true label, it is often confused with:

- **Other**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Distrust towards Media**: 1 times

### CC: Amplifying Climate Fears

When **CC: Amplifying Climate Fears** is the true label, it is often confused with:

- **Other**: 12 times

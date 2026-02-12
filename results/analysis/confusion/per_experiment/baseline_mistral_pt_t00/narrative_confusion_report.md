# Narrative Confusion Analysis Report

## Narrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| URW: Discrediting Ukraine | 1 | 0 | 0 | 1 | 1 | 1.000 | 1.000 | 1.000 |
| URW: Russia is the Victim | 2 | 2 | 0 | 2 | 4 | 0.500 | 1.000 | 0.667 |
| CC: Amplifying Climate Fears | 6 | 1 | 7 | 13 | 7 | 0.857 | 0.462 | 0.600 |
| CC: Criticism of institutions and authorities | 4 | 7 | 0 | 4 | 11 | 0.364 | 1.000 | 0.533 |
| URW: Praise of Russia | 1 | 1 | 1 | 2 | 2 | 0.500 | 0.500 | 0.500 |
| CC: Criticism of climate policies | 2 | 6 | 0 | 2 | 8 | 0.250 | 1.000 | 0.400 |
| URW: Discrediting the West, Diplomacy | 1 | 5 | 0 | 1 | 6 | 0.167 | 1.000 | 0.286 |
| CC: Controversy about green technologies | 0 | 5 | 0 | 0 | 5 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of climate movement | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| CC: Downplaying climate change | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| CC: Green policies are geopolitical instruments | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| CC: Questioning the measurements and science | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| Other | 0 | 5 | 0 | 0 | 5 | 0.000 | 0.000 | 0.000 |
| URW: Blaming the war on others rather than the invader | 0 | 5 | 0 | 0 | 5 | 0.000 | 0.000 | 0.000 |
| URW: Distrust towards Media | 0 | 5 | 0 | 0 | 5 | 0.000 | 0.000 | 0.000 |
| URW: Negative Consequences for the West | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |

## Most Common Narrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | CC: Amplifying Climate Fears | CC: Criticism of institutions and author... | 5 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Amplifying Climate Fears' was true |
| 2 | CC: Amplifying Climate Fears | Other | 5 | Model predicted 'Other' when 'CC: Amplifying Climate Fears' was true |
| 3 | CC: Criticism of institutions and author... | CC: Criticism of climate policies | 4 | Model predicted 'CC: Criticism of climate policies' when 'CC: Criticism of institutions and author...' was true |
| 4 | CC: Criticism of institutions and author... | CC: Criticism of climate movement | 3 | Model predicted 'CC: Criticism of climate movement' when 'CC: Criticism of institutions and author...' was true |
| 5 | CC: Amplifying Climate Fears | CC: Criticism of climate policies | 2 | Model predicted 'CC: Criticism of climate policies' when 'CC: Amplifying Climate Fears' was true |
| 6 | CC: Amplifying Climate Fears | CC: Downplaying climate change | 2 | Model predicted 'CC: Downplaying climate change' when 'CC: Amplifying Climate Fears' was true |
| 7 | CC: Criticism of climate policies | CC: Controversy about green technologies | 2 | Model predicted 'CC: Controversy about green technologies' when 'CC: Criticism of climate policies' was true |
| 8 | CC: Criticism of climate policies | CC: Criticism of institutions and author... | 2 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Criticism of climate policies' was true |
| 9 | CC: Criticism of institutions and author... | CC: Controversy about green technologies | 2 | Model predicted 'CC: Controversy about green technologies' when 'CC: Criticism of institutions and author...' was true |
| 10 | CC: Criticism of institutions and author... | CC: Green policies are geopolitical inst... | 2 | Model predicted 'CC: Green policies are geopolitical inst...' when 'CC: Criticism of institutions and author...' was true |
| 11 | URW: Praise of Russia | URW: Blaming the war on others rather th... | 2 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Praise of Russia' was true |
| 12 | URW: Praise of Russia | URW: Discrediting the West, Diplomacy | 2 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Praise of Russia' was true |
| 13 | URW: Praise of Russia | URW: Russia is the Victim | 2 | Model predicted 'URW: Russia is the Victim' when 'URW: Praise of Russia' was true |
| 14 | URW: Russia is the Victim | URW: Discrediting the West, Diplomacy | 2 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Russia is the Victim' was true |
| 15 | URW: Russia is the Victim | URW: Distrust towards Media | 2 | Model predicted 'URW: Distrust towards Media' when 'URW: Russia is the Victim' was true |
| 16 | CC: Amplifying Climate Fears | CC: Controversy about green technologies | 1 | Model predicted 'CC: Controversy about green technologies' when 'CC: Amplifying Climate Fears' was true |
| 17 | CC: Amplifying Climate Fears | CC: Questioning the measurements and sci... | 1 | Model predicted 'CC: Questioning the measurements and sci...' when 'CC: Amplifying Climate Fears' was true |
| 18 | CC: Criticism of climate policies | CC: Green policies are geopolitical inst... | 1 | Model predicted 'CC: Green policies are geopolitical inst...' when 'CC: Criticism of climate policies' was true |
| 19 | CC: Criticism of institutions and author... | CC: Amplifying Climate Fears | 1 | Model predicted 'CC: Amplifying Climate Fears' when 'CC: Criticism of institutions and author...' was true |
| 20 | CC: Criticism of institutions and author... | CC: Downplaying climate change | 1 | Model predicted 'CC: Downplaying climate change' when 'CC: Criticism of institutions and author...' was true |

## Narrative Label-Specific Confusion Analysis


### URW: Discrediting Ukraine

When **URW: Discrediting Ukraine** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Distrust towards Media**: 1 times

### URW: Russia is the Victim

When **URW: Russia is the Victim** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 2 times
- **URW: Distrust towards Media**: 2 times
- **URW: Blaming the war on others rather than the inv...**: 1 times

### CC: Amplifying Climate Fears

When **CC: Amplifying Climate Fears** is the true label, it is often confused with:

- **CC: Criticism of institutions and authorities**: 5 times
- **Other**: 5 times
- **CC: Criticism of climate policies**: 2 times
- **CC: Downplaying climate change**: 2 times
- **CC: Controversy about green technologies**: 1 times

### CC: Criticism of institutions and authorities

When **CC: Criticism of institutions and authorities** is the true label, it is often confused with:

- **CC: Criticism of climate policies**: 4 times
- **CC: Criticism of climate movement**: 3 times
- **CC: Controversy about green technologies**: 2 times
- **CC: Green policies are geopolitical instruments**: 2 times
- **CC: Amplifying Climate Fears**: 1 times

### URW: Praise of Russia

When **URW: Praise of Russia** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 2 times
- **URW: Discrediting the West, Diplomacy**: 2 times
- **URW: Russia is the Victim**: 2 times
- **URW: Distrust towards Media**: 1 times

### CC: Criticism of climate policies

When **CC: Criticism of climate policies** is the true label, it is often confused with:

- **CC: Controversy about green technologies**: 2 times
- **CC: Criticism of institutions and authorities**: 2 times
- **CC: Green policies are geopolitical instruments**: 1 times

### URW: Discrediting the West, Diplomacy

When **URW: Discrediting the West, Diplomacy** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Distrust towards Media**: 1 times
- **URW: Negative Consequences for the West**: 1 times
- **URW: Praise of Russia**: 1 times

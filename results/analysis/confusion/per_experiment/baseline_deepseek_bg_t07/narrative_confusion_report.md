# Narrative Confusion Analysis Report

## Narrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| CC: Hidden plots by secret schemes of powerful groups | 1 | 0 | 0 | 1 | 1 | 1.000 | 1.000 | 1.000 |
| CC: Amplifying Climate Fears | 8 | 2 | 0 | 8 | 10 | 0.800 | 1.000 | 0.889 |
| URW: Discrediting Ukraine | 4 | 3 | 0 | 4 | 7 | 0.571 | 1.000 | 0.727 |
| URW: Amplifying war-related fears | 4 | 2 | 1 | 5 | 6 | 0.667 | 0.800 | 0.727 |
| CC: Downplaying climate change | 1 | 0 | 1 | 2 | 1 | 1.000 | 0.500 | 0.667 |
| URW: Russia is the Victim | 2 | 2 | 0 | 2 | 4 | 0.500 | 1.000 | 0.667 |
| CC: Criticism of climate movement | 1 | 2 | 0 | 1 | 3 | 0.333 | 1.000 | 0.500 |
| URW: Discrediting the West, Diplomacy | 2 | 8 | 0 | 2 | 10 | 0.200 | 1.000 | 0.333 |
| URW: Blaming the war on others rather than the invader | 1 | 9 | 0 | 1 | 10 | 0.100 | 1.000 | 0.182 |
| CC: Controversy about green technologies | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of climate policies | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of institutions and authorities | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| CC: Green policies are geopolitical instruments | 0 | 0 | 1 | 1 | 0 | 0.000 | 0.000 | 0.000 |
| Other | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Distrust towards Media | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Negative Consequences for the West | 0 | 5 | 1 | 1 | 5 | 0.000 | 0.000 | 0.000 |
| URW: Praise of Russia | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Speculating war outcomes | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |

## Most Common Narrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | URW: Amplifying war-related fears | URW: Blaming the war on others rather th... | 3 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Amplifying war-related fears' was true |
| 2 | URW: Discrediting Ukraine | URW: Blaming the war on others rather th... | 3 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting Ukraine' was true |
| 3 | URW: Discrediting Ukraine | URW: Discrediting the West, Diplomacy | 3 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Discrediting Ukraine' was true |
| 4 | URW: Discrediting Ukraine | URW: Negative Consequences for the West | 2 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Discrediting Ukraine' was true |
| 5 | URW: Discrediting the West, Diplomacy | URW: Discrediting Ukraine | 2 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Discrediting the West, Diplomacy' was true |
| 6 | URW: Discrediting the West, Diplomacy | URW: Praise of Russia | 2 | Model predicted 'URW: Praise of Russia' when 'URW: Discrediting the West, Diplomacy' was true |
| 7 | URW: Russia is the Victim | URW: Discrediting the West, Diplomacy | 2 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Russia is the Victim' was true |
| 8 | CC: Criticism of climate movement | CC: Amplifying Climate Fears | 1 | Model predicted 'CC: Amplifying Climate Fears' when 'CC: Criticism of climate movement' was true |
| 9 | CC: Criticism of climate movement | CC: Criticism of climate policies | 1 | Model predicted 'CC: Criticism of climate policies' when 'CC: Criticism of climate movement' was true |
| 10 | CC: Criticism of climate movement | CC: Criticism of institutions and author... | 1 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Criticism of climate movement' was true |
| 11 | CC: Downplaying climate change | CC: Amplifying Climate Fears | 1 | Model predicted 'CC: Amplifying Climate Fears' when 'CC: Downplaying climate change' was true |
| 12 | CC: Downplaying climate change | CC: Controversy about green technologies | 1 | Model predicted 'CC: Controversy about green technologies' when 'CC: Downplaying climate change' was true |
| 13 | CC: Downplaying climate change | CC: Criticism of climate movement | 1 | Model predicted 'CC: Criticism of climate movement' when 'CC: Downplaying climate change' was true |
| 14 | CC: Downplaying climate change | CC: Criticism of climate policies | 1 | Model predicted 'CC: Criticism of climate policies' when 'CC: Downplaying climate change' was true |
| 15 | CC: Green policies are geopolitical inst... | Other | 1 | Model predicted 'Other' when 'CC: Green policies are geopolitical inst...' was true |
| 16 | CC: Hidden plots by secret schemes of po... | CC: Controversy about green technologies | 1 | Model predicted 'CC: Controversy about green technologies' when 'CC: Hidden plots by secret schemes of po...' was true |
| 17 | CC: Hidden plots by secret schemes of po... | CC: Criticism of climate movement | 1 | Model predicted 'CC: Criticism of climate movement' when 'CC: Hidden plots by secret schemes of po...' was true |
| 18 | CC: Hidden plots by secret schemes of po... | CC: Criticism of climate policies | 1 | Model predicted 'CC: Criticism of climate policies' when 'CC: Hidden plots by secret schemes of po...' was true |
| 19 | URW: Amplifying war-related fears | Other | 1 | Model predicted 'Other' when 'URW: Amplifying war-related fears' was true |
| 20 | URW: Amplifying war-related fears | URW: Discrediting the West, Diplomacy | 1 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Amplifying war-related fears' was true |

## Narrative Label-Specific Confusion Analysis


### CC: Hidden plots by secret schemes of powerful groups

When **CC: Hidden plots by secret schemes of powerful groups** is the true label, it is often confused with:

- **CC: Controversy about green technologies**: 1 times
- **CC: Criticism of climate movement**: 1 times
- **CC: Criticism of climate policies**: 1 times

### URW: Discrediting Ukraine

When **URW: Discrediting Ukraine** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 3 times
- **URW: Discrediting the West, Diplomacy**: 3 times
- **URW: Negative Consequences for the West**: 2 times
- **URW: Russia is the Victim**: 1 times

### URW: Amplifying war-related fears

When **URW: Amplifying war-related fears** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 3 times
- **Other**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Negative Consequences for the West**: 1 times
- **URW: Russia is the Victim**: 1 times

### CC: Downplaying climate change

When **CC: Downplaying climate change** is the true label, it is often confused with:

- **CC: Amplifying Climate Fears**: 1 times
- **CC: Controversy about green technologies**: 1 times
- **CC: Criticism of climate movement**: 1 times
- **CC: Criticism of climate policies**: 1 times

### URW: Russia is the Victim

When **URW: Russia is the Victim** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 2 times
- **URW: Amplifying war-related fears**: 1 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Negative Consequences for the West**: 1 times

### CC: Criticism of climate movement

When **CC: Criticism of climate movement** is the true label, it is often confused with:

- **CC: Amplifying Climate Fears**: 1 times
- **CC: Criticism of climate policies**: 1 times
- **CC: Criticism of institutions and authorities**: 1 times

### URW: Discrediting the West, Diplomacy

When **URW: Discrediting the West, Diplomacy** is the true label, it is often confused with:

- **URW: Discrediting Ukraine**: 2 times
- **URW: Praise of Russia**: 2 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Negative Consequences for the West**: 1 times

### URW: Blaming the war on others rather than the invader

When **URW: Blaming the war on others rather than the invader** is the true label, it is often confused with:

- **URW: Discrediting Ukraine**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Distrust towards Media**: 1 times

### CC: Green policies are geopolitical instruments

When **CC: Green policies are geopolitical instruments** is the true label, it is often confused with:

- **Other**: 1 times

# Narrative Confusion Analysis Report

## Narrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| CC: Amplifying Climate Fears | 7 | 1 | 1 | 8 | 8 | 0.875 | 0.875 | 0.875 |
| URW: Discrediting Ukraine | 4 | 2 | 0 | 4 | 6 | 0.667 | 1.000 | 0.800 |
| CC: Criticism of climate movement | 1 | 1 | 0 | 1 | 2 | 0.500 | 1.000 | 0.667 |
| URW: Amplifying war-related fears | 3 | 2 | 2 | 5 | 5 | 0.600 | 0.600 | 0.600 |
| CC: Downplaying climate change | 1 | 1 | 1 | 2 | 2 | 0.500 | 0.500 | 0.500 |
| URW: Russia is the Victim | 1 | 2 | 1 | 2 | 3 | 0.333 | 0.500 | 0.400 |
| URW: Blaming the war on others rather than the invader | 1 | 8 | 0 | 1 | 9 | 0.111 | 1.000 | 0.200 |
| URW: Discrediting the West, Diplomacy | 1 | 8 | 1 | 2 | 9 | 0.111 | 0.500 | 0.182 |
| CC: Climate change is beneficial | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| CC: Controversy about green technologies | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of climate policies | 0 | 4 | 0 | 0 | 4 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of institutions and authorities | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| CC: Green policies are geopolitical instruments | 0 | 1 | 1 | 1 | 1 | 0.000 | 0.000 | 0.000 |
| CC: Hidden plots by secret schemes of powerful groups | 0 | 0 | 1 | 1 | 0 | 0.000 | 0.000 | 0.000 |
| CC: Questioning the measurements and science | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| Other | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| URW: Distrust towards Media | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Hidden plots by secret schemes of powerful groups | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Negative Consequences for the West | 0 | 4 | 1 | 1 | 4 | 0.000 | 0.000 | 0.000 |
| URW: Overpraising the West | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Praise of Russia | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Speculating war outcomes | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |

## Most Common Narrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | URW: Amplifying war-related fears | URW: Blaming the war on others rather th... | 3 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Amplifying war-related fears' was true |
| 2 | URW: Discrediting Ukraine | URW: Blaming the war on others rather th... | 3 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting Ukraine' was true |
| 3 | URW: Discrediting Ukraine | URW: Discrediting the West, Diplomacy | 3 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Discrediting Ukraine' was true |
| 4 | CC: Downplaying climate change | CC: Questioning the measurements and sci... | 2 | Model predicted 'CC: Questioning the measurements and sci...' when 'CC: Downplaying climate change' was true |
| 5 | URW: Amplifying war-related fears | URW: Discrediting the West, Diplomacy | 2 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Amplifying war-related fears' was true |
| 6 | URW: Discrediting the West, Diplomacy | URW: Praise of Russia | 2 | Model predicted 'URW: Praise of Russia' when 'URW: Discrediting the West, Diplomacy' was true |
| 7 | URW: Russia is the Victim | URW: Discrediting the West, Diplomacy | 2 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Russia is the Victim' was true |
| 8 | CC: Amplifying Climate Fears | CC: Criticism of climate policies | 1 | Model predicted 'CC: Criticism of climate policies' when 'CC: Amplifying Climate Fears' was true |
| 9 | CC: Amplifying Climate Fears | CC: Criticism of institutions and author... | 1 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Amplifying Climate Fears' was true |
| 10 | CC: Amplifying Climate Fears | CC: Downplaying climate change | 1 | Model predicted 'CC: Downplaying climate change' when 'CC: Amplifying Climate Fears' was true |
| 11 | CC: Amplifying Climate Fears | Other | 1 | Model predicted 'Other' when 'CC: Amplifying Climate Fears' was true |
| 12 | CC: Criticism of climate movement | CC: Criticism of climate policies | 1 | Model predicted 'CC: Criticism of climate policies' when 'CC: Criticism of climate movement' was true |
| 13 | CC: Criticism of climate movement | CC: Criticism of institutions and author... | 1 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Criticism of climate movement' was true |
| 14 | CC: Downplaying climate change | CC: Amplifying Climate Fears | 1 | Model predicted 'CC: Amplifying Climate Fears' when 'CC: Downplaying climate change' was true |
| 15 | CC: Downplaying climate change | CC: Climate change is beneficial | 1 | Model predicted 'CC: Climate change is beneficial' when 'CC: Downplaying climate change' was true |
| 16 | CC: Downplaying climate change | CC: Controversy about green technologies | 1 | Model predicted 'CC: Controversy about green technologies' when 'CC: Downplaying climate change' was true |
| 17 | CC: Downplaying climate change | CC: Criticism of climate policies | 1 | Model predicted 'CC: Criticism of climate policies' when 'CC: Downplaying climate change' was true |
| 18 | CC: Green policies are geopolitical inst... | Other | 1 | Model predicted 'Other' when 'CC: Green policies are geopolitical inst...' was true |
| 19 | CC: Hidden plots by secret schemes of po... | CC: Controversy about green technologies | 1 | Model predicted 'CC: Controversy about green technologies' when 'CC: Hidden plots by secret schemes of po...' was true |
| 20 | CC: Hidden plots by secret schemes of po... | CC: Criticism of climate movement | 1 | Model predicted 'CC: Criticism of climate movement' when 'CC: Hidden plots by secret schemes of po...' was true |

## Narrative Label-Specific Confusion Analysis


### CC: Amplifying Climate Fears

When **CC: Amplifying Climate Fears** is the true label, it is often confused with:

- **CC: Criticism of climate policies**: 1 times
- **CC: Criticism of institutions and authorities**: 1 times
- **CC: Downplaying climate change**: 1 times
- **Other**: 1 times

### URW: Discrediting Ukraine

When **URW: Discrediting Ukraine** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 3 times
- **URW: Discrediting the West, Diplomacy**: 3 times
- **URW: Hidden plots by secret schemes of powerful gr...**: 1 times
- **URW: Negative Consequences for the West**: 1 times
- **URW: Russia is the Victim**: 1 times

### CC: Criticism of climate movement

When **CC: Criticism of climate movement** is the true label, it is often confused with:

- **CC: Criticism of climate policies**: 1 times
- **CC: Criticism of institutions and authorities**: 1 times

### URW: Amplifying war-related fears

When **URW: Amplifying war-related fears** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 3 times
- **URW: Discrediting the West, Diplomacy**: 2 times
- **Other**: 1 times
- **URW: Negative Consequences for the West**: 1 times
- **URW: Overpraising the West**: 1 times

### CC: Downplaying climate change

When **CC: Downplaying climate change** is the true label, it is often confused with:

- **CC: Questioning the measurements and science**: 2 times
- **CC: Amplifying Climate Fears**: 1 times
- **CC: Climate change is beneficial**: 1 times
- **CC: Controversy about green technologies**: 1 times
- **CC: Criticism of climate policies**: 1 times

### URW: Russia is the Victim

When **URW: Russia is the Victim** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 2 times
- **URW: Amplifying war-related fears**: 1 times
- **URW: Negative Consequences for the West**: 1 times

### URW: Blaming the war on others rather than the invader

When **URW: Blaming the war on others rather than the invader** is the true label, it is often confused with:

- **URW: Discrediting Ukraine**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Distrust towards Media**: 1 times

### URW: Discrediting the West, Diplomacy

When **URW: Discrediting the West, Diplomacy** is the true label, it is often confused with:

- **URW: Praise of Russia**: 2 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting Ukraine**: 1 times
- **URW: Hidden plots by secret schemes of powerful gr...**: 1 times
- **URW: Negative Consequences for the West**: 1 times

### CC: Green policies are geopolitical instruments

When **CC: Green policies are geopolitical instruments** is the true label, it is often confused with:

- **Other**: 1 times

### CC: Hidden plots by secret schemes of powerful groups

When **CC: Hidden plots by secret schemes of powerful groups** is the true label, it is often confused with:

- **CC: Controversy about green technologies**: 1 times
- **CC: Criticism of climate movement**: 1 times
- **CC: Criticism of climate policies**: 1 times
- **CC: Criticism of institutions and authorities**: 1 times
- **CC: Green policies are geopolitical instruments**: 1 times

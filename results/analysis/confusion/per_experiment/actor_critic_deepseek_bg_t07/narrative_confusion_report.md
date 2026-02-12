# Narrative Confusion Analysis Report

## Narrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| CC: Amplifying Climate Fears | 7 | 0 | 1 | 8 | 7 | 1.000 | 0.875 | 0.933 |
| URW: Russia is the Victim | 2 | 1 | 0 | 2 | 3 | 0.667 | 1.000 | 0.800 |
| URW: Discrediting Ukraine | 4 | 3 | 0 | 4 | 7 | 0.571 | 1.000 | 0.727 |
| CC: Criticism of climate movement | 1 | 1 | 0 | 1 | 2 | 0.500 | 1.000 | 0.667 |
| CC: Downplaying climate change | 1 | 0 | 1 | 2 | 1 | 1.000 | 0.500 | 0.667 |
| URW: Amplifying war-related fears | 4 | 3 | 1 | 5 | 7 | 0.571 | 0.800 | 0.667 |
| URW: Discrediting the West, Diplomacy | 2 | 7 | 0 | 2 | 9 | 0.222 | 1.000 | 0.364 |
| URW: Blaming the war on others rather than the invader | 1 | 6 | 0 | 1 | 7 | 0.143 | 1.000 | 0.250 |
| CC: Controversy about green technologies | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of climate policies | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of institutions and authorities | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| CC: Green policies are geopolitical instruments | 0 | 0 | 1 | 1 | 0 | 0.000 | 0.000 | 0.000 |
| CC: Hidden plots by secret schemes of powerful groups | 0 | 0 | 1 | 1 | 0 | 0.000 | 0.000 | 0.000 |
| CC: Questioning the measurements and science | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| Other | 0 | 4 | 0 | 0 | 4 | 0.000 | 0.000 | 0.000 |
| URW: Distrust towards Media | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Hidden plots by secret schemes of powerful groups | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Negative Consequences for the West | 0 | 4 | 1 | 1 | 4 | 0.000 | 0.000 | 0.000 |
| URW: Speculating war outcomes | 0 | 4 | 0 | 0 | 4 | 0.000 | 0.000 | 0.000 |

## Most Common Narrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | URW: Discrediting Ukraine | URW: Blaming the war on others rather th... | 3 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting Ukraine' was true |
| 2 | URW: Discrediting Ukraine | URW: Discrediting the West, Diplomacy | 3 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Discrediting Ukraine' was true |
| 3 | URW: Amplifying war-related fears | URW: Blaming the war on others rather th... | 2 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Amplifying war-related fears' was true |
| 4 | URW: Amplifying war-related fears | URW: Speculating war outcomes | 2 | Model predicted 'URW: Speculating war outcomes' when 'URW: Amplifying war-related fears' was true |
| 5 | URW: Discrediting the West, Diplomacy | URW: Speculating war outcomes | 2 | Model predicted 'URW: Speculating war outcomes' when 'URW: Discrediting the West, Diplomacy' was true |
| 6 | URW: Russia is the Victim | URW: Discrediting the West, Diplomacy | 2 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Russia is the Victim' was true |
| 7 | CC: Amplifying Climate Fears | CC: Criticism of climate policies | 1 | Model predicted 'CC: Criticism of climate policies' when 'CC: Amplifying Climate Fears' was true |
| 8 | CC: Amplifying Climate Fears | Other | 1 | Model predicted 'Other' when 'CC: Amplifying Climate Fears' was true |
| 9 | CC: Criticism of climate movement | CC: Criticism of institutions and author... | 1 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Criticism of climate movement' was true |
| 10 | CC: Downplaying climate change | CC: Controversy about green technologies | 1 | Model predicted 'CC: Controversy about green technologies' when 'CC: Downplaying climate change' was true |
| 11 | CC: Downplaying climate change | CC: Criticism of climate movement | 1 | Model predicted 'CC: Criticism of climate movement' when 'CC: Downplaying climate change' was true |
| 12 | CC: Downplaying climate change | CC: Criticism of climate policies | 1 | Model predicted 'CC: Criticism of climate policies' when 'CC: Downplaying climate change' was true |
| 13 | CC: Downplaying climate change | CC: Questioning the measurements and sci... | 1 | Model predicted 'CC: Questioning the measurements and sci...' when 'CC: Downplaying climate change' was true |
| 14 | CC: Downplaying climate change | Other | 1 | Model predicted 'Other' when 'CC: Downplaying climate change' was true |
| 15 | CC: Green policies are geopolitical inst... | Other | 1 | Model predicted 'Other' when 'CC: Green policies are geopolitical inst...' was true |
| 16 | CC: Hidden plots by secret schemes of po... | CC: Controversy about green technologies | 1 | Model predicted 'CC: Controversy about green technologies' when 'CC: Hidden plots by secret schemes of po...' was true |
| 17 | CC: Hidden plots by secret schemes of po... | CC: Criticism of climate policies | 1 | Model predicted 'CC: Criticism of climate policies' when 'CC: Hidden plots by secret schemes of po...' was true |
| 18 | CC: Hidden plots by secret schemes of po... | CC: Criticism of institutions and author... | 1 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Hidden plots by secret schemes of po...' was true |
| 19 | URW: Amplifying war-related fears | Other | 1 | Model predicted 'Other' when 'URW: Amplifying war-related fears' was true |
| 20 | URW: Amplifying war-related fears | URW: Discrediting the West, Diplomacy | 1 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Amplifying war-related fears' was true |

## Narrative Label-Specific Confusion Analysis


### CC: Amplifying Climate Fears

When **CC: Amplifying Climate Fears** is the true label, it is often confused with:

- **CC: Criticism of climate policies**: 1 times
- **Other**: 1 times

### URW: Russia is the Victim

When **URW: Russia is the Victim** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 2 times
- **URW: Amplifying war-related fears**: 1 times
- **URW: Negative Consequences for the West**: 1 times

### URW: Discrediting Ukraine

When **URW: Discrediting Ukraine** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 3 times
- **URW: Discrediting the West, Diplomacy**: 3 times
- **URW: Amplifying war-related fears**: 1 times
- **URW: Negative Consequences for the West**: 1 times

### CC: Criticism of climate movement

When **CC: Criticism of climate movement** is the true label, it is often confused with:

- **CC: Criticism of institutions and authorities**: 1 times

### CC: Downplaying climate change

When **CC: Downplaying climate change** is the true label, it is often confused with:

- **CC: Controversy about green technologies**: 1 times
- **CC: Criticism of climate movement**: 1 times
- **CC: Criticism of climate policies**: 1 times
- **CC: Questioning the measurements and science**: 1 times
- **Other**: 1 times

### URW: Amplifying war-related fears

When **URW: Amplifying war-related fears** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 2 times
- **URW: Speculating war outcomes**: 2 times
- **Other**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Negative Consequences for the West**: 1 times

### URW: Discrediting the West, Diplomacy

When **URW: Discrediting the West, Diplomacy** is the true label, it is often confused with:

- **URW: Speculating war outcomes**: 2 times
- **URW: Discrediting Ukraine**: 1 times
- **URW: Hidden plots by secret schemes of powerful gr...**: 1 times
- **URW: Negative Consequences for the West**: 1 times

### URW: Blaming the war on others rather than the invader

When **URW: Blaming the war on others rather than the invader** is the true label, it is often confused with:

- **URW: Discrediting Ukraine**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Distrust towards Media**: 1 times

### CC: Green policies are geopolitical instruments

When **CC: Green policies are geopolitical instruments** is the true label, it is often confused with:

- **Other**: 1 times

### CC: Hidden plots by secret schemes of powerful groups

When **CC: Hidden plots by secret schemes of powerful groups** is the true label, it is often confused with:

- **CC: Controversy about green technologies**: 1 times
- **CC: Criticism of climate policies**: 1 times
- **CC: Criticism of institutions and authorities**: 1 times

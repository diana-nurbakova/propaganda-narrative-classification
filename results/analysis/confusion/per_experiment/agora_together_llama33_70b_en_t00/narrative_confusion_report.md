# Narrative Confusion Analysis Report

## Narrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| CC: Climate change is beneficial | 1 | 0 | 0 | 1 | 1 | 1.000 | 1.000 | 1.000 |
| CC: Criticism of climate movement | 5 | 5 | 1 | 6 | 10 | 0.500 | 0.833 | 0.625 |
| URW: Discrediting the West, Diplomacy | 4 | 9 | 0 | 4 | 13 | 0.308 | 1.000 | 0.471 |
| CC: Criticism of climate policies | 3 | 7 | 0 | 3 | 10 | 0.300 | 1.000 | 0.462 |
| CC: Criticism of institutions and authorities | 3 | 7 | 0 | 3 | 10 | 0.300 | 1.000 | 0.462 |
| CC: Questioning the measurements and science | 1 | 3 | 0 | 1 | 4 | 0.250 | 1.000 | 0.400 |
| URW: Discrediting Ukraine | 2 | 5 | 1 | 3 | 7 | 0.286 | 0.667 | 0.400 |
| URW: Blaming the war on others rather than the invader | 1 | 7 | 0 | 1 | 8 | 0.125 | 1.000 | 0.222 |
| URW: Speculating war outcomes | 1 | 5 | 2 | 3 | 6 | 0.167 | 0.333 | 0.222 |
| URW: Negative Consequences for the West | 1 | 9 | 0 | 1 | 10 | 0.100 | 1.000 | 0.182 |
| CC: Controversy about green technologies | 0 | 2 | 1 | 1 | 2 | 0.000 | 0.000 | 0.000 |
| CC: Downplaying climate change | 0 | 12 | 0 | 0 | 12 | 0.000 | 0.000 | 0.000 |
| CC: Green policies are geopolitical instruments | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| CC: Hidden plots by secret schemes of powerful groups | 0 | 0 | 2 | 2 | 0 | 0.000 | 0.000 | 0.000 |
| Other | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Amplifying war-related fears | 0 | 7 | 0 | 0 | 7 | 0.000 | 0.000 | 0.000 |
| URW: Distrust towards Media | 0 | 6 | 0 | 0 | 6 | 0.000 | 0.000 | 0.000 |
| URW: Hidden plots by secret schemes of powerful groups | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Overpraising the West | 0 | 0 | 1 | 1 | 0 | 0.000 | 0.000 | 0.000 |
| URW: Praise of Russia | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Russia is the Victim | 0 | 5 | 0 | 0 | 5 | 0.000 | 0.000 | 0.000 |

## Most Common Narrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | CC: Criticism of climate movement | CC: Downplaying climate change | 6 | Model predicted 'CC: Downplaying climate change' when 'CC: Criticism of climate movement' was true |
| 2 | CC: Criticism of climate movement | CC: Criticism of institutions and author... | 3 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Criticism of climate movement' was true |
| 3 | CC: Criticism of climate movement | CC: Questioning the measurements and sci... | 3 | Model predicted 'CC: Questioning the measurements and sci...' when 'CC: Criticism of climate movement' was true |
| 4 | URW: Discrediting Ukraine | URW: Discrediting the West, Diplomacy | 3 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Discrediting Ukraine' was true |
| 5 | URW: Discrediting the West, Diplomacy | URW: Negative Consequences for the West | 3 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Discrediting the West, Diplomacy' was true |
| 6 | URW: Speculating war outcomes | URW: Discrediting Ukraine | 3 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Speculating war outcomes' was true |
| 7 | URW: Speculating war outcomes | URW: Discrediting the West, Diplomacy | 3 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Speculating war outcomes' was true |
| 8 | URW: Speculating war outcomes | URW: Negative Consequences for the West | 3 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Speculating war outcomes' was true |
| 9 | URW: Speculating war outcomes | URW: Russia is the Victim | 3 | Model predicted 'URW: Russia is the Victim' when 'URW: Speculating war outcomes' was true |
| 10 | CC: Criticism of climate movement | CC: Criticism of climate policies | 2 | Model predicted 'CC: Criticism of climate policies' when 'CC: Criticism of climate movement' was true |
| 11 | CC: Criticism of climate policies | CC: Controversy about green technologies | 2 | Model predicted 'CC: Controversy about green technologies' when 'CC: Criticism of climate policies' was true |
| 12 | CC: Criticism of climate policies | CC: Criticism of climate movement | 2 | Model predicted 'CC: Criticism of climate movement' when 'CC: Criticism of climate policies' was true |
| 13 | CC: Criticism of climate policies | CC: Criticism of institutions and author... | 2 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Criticism of climate policies' was true |
| 14 | CC: Criticism of climate policies | CC: Downplaying climate change | 2 | Model predicted 'CC: Downplaying climate change' when 'CC: Criticism of climate policies' was true |
| 15 | CC: Criticism of institutions and author... | CC: Criticism of climate policies | 2 | Model predicted 'CC: Criticism of climate policies' when 'CC: Criticism of institutions and author...' was true |
| 16 | CC: Criticism of institutions and author... | CC: Green policies are geopolitical inst... | 2 | Model predicted 'CC: Green policies are geopolitical inst...' when 'CC: Criticism of institutions and author...' was true |
| 17 | URW: Discrediting Ukraine | URW: Speculating war outcomes | 2 | Model predicted 'URW: Speculating war outcomes' when 'URW: Discrediting Ukraine' was true |
| 18 | URW: Discrediting the West, Diplomacy | URW: Amplifying war-related fears | 2 | Model predicted 'URW: Amplifying war-related fears' when 'URW: Discrediting the West, Diplomacy' was true |
| 19 | URW: Discrediting the West, Diplomacy | URW: Blaming the war on others rather th... | 2 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting the West, Diplomacy' was true |
| 20 | URW: Discrediting the West, Diplomacy | URW: Discrediting Ukraine | 2 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Discrediting the West, Diplomacy' was true |

## Narrative Label-Specific Confusion Analysis


### CC: Climate change is beneficial

When **CC: Climate change is beneficial** is the true label, it is often confused with:

- **CC: Criticism of climate policies**: 1 times
- **CC: Criticism of institutions and authorities**: 1 times
- **CC: Downplaying climate change**: 1 times

### CC: Criticism of climate movement

When **CC: Criticism of climate movement** is the true label, it is often confused with:

- **CC: Downplaying climate change**: 6 times
- **CC: Criticism of institutions and authorities**: 3 times
- **CC: Questioning the measurements and science**: 3 times
- **CC: Criticism of climate policies**: 2 times

### URW: Discrediting the West, Diplomacy

When **URW: Discrediting the West, Diplomacy** is the true label, it is often confused with:

- **URW: Negative Consequences for the West**: 3 times
- **URW: Amplifying war-related fears**: 2 times
- **URW: Blaming the war on others rather than the inv...**: 2 times
- **URW: Discrediting Ukraine**: 2 times
- **URW: Russia is the Victim**: 2 times

### CC: Criticism of climate policies

When **CC: Criticism of climate policies** is the true label, it is often confused with:

- **CC: Controversy about green technologies**: 2 times
- **CC: Criticism of climate movement**: 2 times
- **CC: Criticism of institutions and authorities**: 2 times
- **CC: Downplaying climate change**: 2 times
- **CC: Green policies are geopolitical instruments**: 1 times

### CC: Criticism of institutions and authorities

When **CC: Criticism of institutions and authorities** is the true label, it is often confused with:

- **CC: Criticism of climate policies**: 2 times
- **CC: Green policies are geopolitical instruments**: 2 times
- **CC: Criticism of climate movement**: 1 times
- **CC: Downplaying climate change**: 1 times

### CC: Questioning the measurements and science

When **CC: Questioning the measurements and science** is the true label, it is often confused with:

- **CC: Criticism of climate movement**: 1 times
- **CC: Criticism of climate policies**: 1 times
- **CC: Downplaying climate change**: 1 times

### URW: Discrediting Ukraine

When **URW: Discrediting Ukraine** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 3 times
- **URW: Speculating war outcomes**: 2 times
- **URW: Amplifying war-related fears**: 1 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Distrust towards Media**: 1 times

### URW: Blaming the war on others rather than the invader

When **URW: Blaming the war on others rather than the invader** is the true label, it is often confused with:

- **URW: Amplifying war-related fears**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Distrust towards Media**: 1 times
- **URW: Negative Consequences for the West**: 1 times
- **URW: Speculating war outcomes**: 1 times

### URW: Speculating war outcomes

When **URW: Speculating war outcomes** is the true label, it is often confused with:

- **URW: Discrediting Ukraine**: 3 times
- **URW: Discrediting the West, Diplomacy**: 3 times
- **URW: Negative Consequences for the West**: 3 times
- **URW: Russia is the Victim**: 3 times
- **URW: Amplifying war-related fears**: 2 times

### URW: Negative Consequences for the West

When **URW: Negative Consequences for the West** is the true label, it is often confused with:

- **URW: Amplifying war-related fears**: 1 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Distrust towards Media**: 1 times

### CC: Controversy about green technologies

When **CC: Controversy about green technologies** is the true label, it is often confused with:

- **Other**: 1 times

### CC: Hidden plots by secret schemes of powerful groups

When **CC: Hidden plots by secret schemes of powerful groups** is the true label, it is often confused with:

- **CC: Criticism of climate movement**: 1 times
- **CC: Criticism of climate policies**: 1 times
- **CC: Criticism of institutions and authorities**: 1 times
- **CC: Downplaying climate change**: 1 times
- **Other**: 1 times

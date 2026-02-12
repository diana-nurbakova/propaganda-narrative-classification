# Narrative Confusion Analysis Report

## Narrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| CC: Climate change is beneficial | 1 | 0 | 0 | 1 | 1 | 1.000 | 1.000 | 1.000 |
| URW: Overpraising the West | 1 | 0 | 0 | 1 | 1 | 1.000 | 1.000 | 1.000 |
| CC: Criticism of climate movement | 6 | 5 | 0 | 6 | 11 | 0.545 | 1.000 | 0.706 |
| URW: Discrediting the West, Diplomacy | 4 | 6 | 0 | 4 | 10 | 0.400 | 1.000 | 0.571 |
| URW: Discrediting Ukraine | 3 | 5 | 0 | 3 | 8 | 0.375 | 1.000 | 0.545 |
| CC: Hidden plots by secret schemes of powerful groups | 1 | 1 | 1 | 2 | 2 | 0.500 | 0.500 | 0.500 |
| CC: Criticism of institutions and authorities | 2 | 4 | 1 | 3 | 6 | 0.333 | 0.667 | 0.444 |
| CC: Controversy about green technologies | 1 | 3 | 0 | 1 | 4 | 0.250 | 1.000 | 0.400 |
| CC: Questioning the measurements and science | 1 | 4 | 0 | 1 | 5 | 0.200 | 1.000 | 0.333 |
| CC: Criticism of climate policies | 2 | 8 | 1 | 3 | 10 | 0.200 | 0.667 | 0.308 |
| URW: Speculating war outcomes | 1 | 3 | 2 | 3 | 4 | 0.250 | 0.333 | 0.286 |
| URW: Blaming the war on others rather than the invader | 1 | 5 | 0 | 1 | 6 | 0.167 | 1.000 | 0.286 |
| CC: Amplifying Climate Fears | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| CC: Downplaying climate change | 0 | 5 | 0 | 0 | 5 | 0.000 | 0.000 | 0.000 |
| CC: Green policies are geopolitical instruments | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| Other | 0 | 4 | 0 | 0 | 4 | 0.000 | 0.000 | 0.000 |
| URW: Amplifying war-related fears | 0 | 7 | 0 | 0 | 7 | 0.000 | 0.000 | 0.000 |
| URW: Distrust towards Media | 0 | 6 | 0 | 0 | 6 | 0.000 | 0.000 | 0.000 |
| URW: Hidden plots by secret schemes of powerful groups | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Negative Consequences for the West | 0 | 5 | 1 | 1 | 5 | 0.000 | 0.000 | 0.000 |
| URW: Praise of Russia | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Russia is the Victim | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |

## Most Common Narrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | CC: Criticism of climate movement | CC: Questioning the measurements and sci... | 4 | Model predicted 'CC: Questioning the measurements and sci...' when 'CC: Criticism of climate movement' was true |
| 2 | CC: Criticism of climate movement | CC: Criticism of climate policies | 3 | Model predicted 'CC: Criticism of climate policies' when 'CC: Criticism of climate movement' was true |
| 3 | CC: Criticism of climate movement | CC: Downplaying climate change | 3 | Model predicted 'CC: Downplaying climate change' when 'CC: Criticism of climate movement' was true |
| 4 | URW: Discrediting Ukraine | URW: Discrediting the West, Diplomacy | 3 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Discrediting Ukraine' was true |
| 5 | CC: Criticism of climate movement | CC: Amplifying Climate Fears | 2 | Model predicted 'CC: Amplifying Climate Fears' when 'CC: Criticism of climate movement' was true |
| 6 | CC: Criticism of climate policies | CC: Criticism of institutions and author... | 2 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Criticism of climate policies' was true |
| 7 | CC: Criticism of institutions and author... | CC: Criticism of climate policies | 2 | Model predicted 'CC: Criticism of climate policies' when 'CC: Criticism of institutions and author...' was true |
| 8 | URW: Discrediting Ukraine | URW: Blaming the war on others rather th... | 2 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting Ukraine' was true |
| 9 | URW: Discrediting Ukraine | URW: Distrust towards Media | 2 | Model predicted 'URW: Distrust towards Media' when 'URW: Discrediting Ukraine' was true |
| 10 | URW: Discrediting the West, Diplomacy | URW: Amplifying war-related fears | 2 | Model predicted 'URW: Amplifying war-related fears' when 'URW: Discrediting the West, Diplomacy' was true |
| 11 | URW: Discrediting the West, Diplomacy | URW: Blaming the war on others rather th... | 2 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting the West, Diplomacy' was true |
| 12 | URW: Discrediting the West, Diplomacy | URW: Discrediting Ukraine | 2 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Discrediting the West, Diplomacy' was true |
| 13 | URW: Discrediting the West, Diplomacy | URW: Distrust towards Media | 2 | Model predicted 'URW: Distrust towards Media' when 'URW: Discrediting the West, Diplomacy' was true |
| 14 | URW: Discrediting the West, Diplomacy | URW: Negative Consequences for the West | 2 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Discrediting the West, Diplomacy' was true |
| 15 | URW: Discrediting the West, Diplomacy | URW: Speculating war outcomes | 2 | Model predicted 'URW: Speculating war outcomes' when 'URW: Discrediting the West, Diplomacy' was true |
| 16 | URW: Speculating war outcomes | URW: Amplifying war-related fears | 2 | Model predicted 'URW: Amplifying war-related fears' when 'URW: Speculating war outcomes' was true |
| 17 | URW: Speculating war outcomes | URW: Discrediting Ukraine | 2 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Speculating war outcomes' was true |
| 18 | URW: Speculating war outcomes | URW: Discrediting the West, Diplomacy | 2 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Speculating war outcomes' was true |
| 19 | URW: Speculating war outcomes | URW: Negative Consequences for the West | 2 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Speculating war outcomes' was true |
| 20 | URW: Speculating war outcomes | URW: Praise of Russia | 2 | Model predicted 'URW: Praise of Russia' when 'URW: Speculating war outcomes' was true |

## Narrative Label-Specific Confusion Analysis


### CC: Climate change is beneficial

When **CC: Climate change is beneficial** is the true label, it is often confused with:

- **CC: Criticism of climate movement**: 1 times
- **CC: Criticism of climate policies**: 1 times
- **CC: Criticism of institutions and authorities**: 1 times

### URW: Overpraising the West

When **URW: Overpraising the West** is the true label, it is often confused with:

- **URW: Amplifying war-related fears**: 1 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Speculating war outcomes**: 1 times

### CC: Criticism of climate movement

When **CC: Criticism of climate movement** is the true label, it is often confused with:

- **CC: Questioning the measurements and science**: 4 times
- **CC: Criticism of climate policies**: 3 times
- **CC: Downplaying climate change**: 3 times
- **CC: Amplifying Climate Fears**: 2 times
- **CC: Controversy about green technologies**: 1 times

### URW: Discrediting the West, Diplomacy

When **URW: Discrediting the West, Diplomacy** is the true label, it is often confused with:

- **URW: Amplifying war-related fears**: 2 times
- **URW: Blaming the war on others rather than the inv...**: 2 times
- **URW: Discrediting Ukraine**: 2 times
- **URW: Distrust towards Media**: 2 times
- **URW: Negative Consequences for the West**: 2 times

### URW: Discrediting Ukraine

When **URW: Discrediting Ukraine** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 3 times
- **URW: Blaming the war on others rather than the inv...**: 2 times
- **URW: Distrust towards Media**: 2 times
- **URW: Amplifying war-related fears**: 1 times
- **URW: Negative Consequences for the West**: 1 times

### CC: Hidden plots by secret schemes of powerful groups

When **CC: Hidden plots by secret schemes of powerful groups** is the true label, it is often confused with:

- **CC: Criticism of climate movement**: 1 times
- **CC: Criticism of climate policies**: 1 times
- **CC: Criticism of institutions and authorities**: 1 times
- **Other**: 1 times

### CC: Criticism of institutions and authorities

When **CC: Criticism of institutions and authorities** is the true label, it is often confused with:

- **CC: Criticism of climate policies**: 2 times
- **CC: Controversy about green technologies**: 1 times
- **CC: Criticism of climate movement**: 1 times
- **CC: Green policies are geopolitical instruments**: 1 times

### CC: Controversy about green technologies

When **CC: Controversy about green technologies** is the true label, it is often confused with:

- **CC: Criticism of climate policies**: 1 times
- **CC: Green policies are geopolitical instruments**: 1 times

### CC: Questioning the measurements and science

When **CC: Questioning the measurements and science** is the true label, it is often confused with:

- **CC: Criticism of climate movement**: 1 times
- **CC: Downplaying climate change**: 1 times

### CC: Criticism of climate policies

When **CC: Criticism of climate policies** is the true label, it is often confused with:

- **CC: Criticism of institutions and authorities**: 2 times
- **CC: Controversy about green technologies**: 1 times
- **CC: Criticism of climate movement**: 1 times
- **CC: Downplaying climate change**: 1 times
- **CC: Green policies are geopolitical instruments**: 1 times

### URW: Speculating war outcomes

When **URW: Speculating war outcomes** is the true label, it is often confused with:

- **URW: Amplifying war-related fears**: 2 times
- **URW: Discrediting Ukraine**: 2 times
- **URW: Discrediting the West, Diplomacy**: 2 times
- **URW: Negative Consequences for the West**: 2 times
- **URW: Praise of Russia**: 2 times

### URW: Blaming the war on others rather than the invader

When **URW: Blaming the war on others rather than the invader** is the true label, it is often confused with:

- **URW: Amplifying war-related fears**: 1 times
- **URW: Discrediting Ukraine**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Distrust towards Media**: 1 times
- **URW: Russia is the Victim**: 1 times

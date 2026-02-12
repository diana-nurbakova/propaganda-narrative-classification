# Narrative Confusion Analysis Report

## Narrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| CC: Hidden plots by secret schemes of powerful groups | 1 | 0 | 0 | 1 | 1 | 1.000 | 1.000 | 1.000 |
| CC: Amplifying Climate Fears | 7 | 2 | 1 | 8 | 9 | 0.778 | 0.875 | 0.824 |
| URW: Amplifying war-related fears | 4 | 2 | 0 | 4 | 6 | 0.667 | 1.000 | 0.800 |
| URW: Discrediting Ukraine | 4 | 2 | 0 | 4 | 6 | 0.667 | 1.000 | 0.800 |
| CC: Criticism of climate movement | 1 | 1 | 0 | 1 | 2 | 0.500 | 1.000 | 0.667 |
| CC: Downplaying climate change | 1 | 1 | 1 | 2 | 2 | 0.500 | 0.500 | 0.500 |
| URW: Negative Consequences for the West | 1 | 3 | 0 | 1 | 4 | 0.250 | 1.000 | 0.400 |
| URW: Discrediting the West, Diplomacy | 2 | 8 | 0 | 2 | 10 | 0.200 | 1.000 | 0.333 |
| URW: Russia is the Victim | 1 | 5 | 1 | 2 | 6 | 0.167 | 0.500 | 0.250 |
| URW: Blaming the war on others rather than the invader | 1 | 11 | 0 | 1 | 12 | 0.083 | 1.000 | 0.154 |
| CC: Controversy about green technologies | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of climate policies | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of institutions and authorities | 0 | 4 | 0 | 0 | 4 | 0.000 | 0.000 | 0.000 |
| CC: Green policies are geopolitical instruments | 0 | 1 | 1 | 1 | 1 | 0.000 | 0.000 | 0.000 |
| CC: Questioning the measurements and science | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| Other | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| URW: Distrust towards Media | 0 | 5 | 0 | 0 | 5 | 0.000 | 0.000 | 0.000 |
| URW: Hidden plots by secret schemes of powerful groups | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Praise of Russia | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Speculating war outcomes | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |

## Most Common Narrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | URW: Discrediting Ukraine | URW: Blaming the war on others rather th... | 4 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting Ukraine' was true |
| 2 | URW: Discrediting Ukraine | URW: Discrediting the West, Diplomacy | 4 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Discrediting Ukraine' was true |
| 3 | URW: Amplifying war-related fears | URW: Blaming the war on others rather th... | 3 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Amplifying war-related fears' was true |
| 4 | URW: Amplifying war-related fears | URW: Speculating war outcomes | 3 | Model predicted 'URW: Speculating war outcomes' when 'URW: Amplifying war-related fears' was true |
| 5 | URW: Amplifying war-related fears | URW: Discrediting the West, Diplomacy | 2 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Amplifying war-related fears' was true |
| 6 | URW: Discrediting Ukraine | URW: Distrust towards Media | 2 | Model predicted 'URW: Distrust towards Media' when 'URW: Discrediting Ukraine' was true |
| 7 | URW: Discrediting Ukraine | URW: Russia is the Victim | 2 | Model predicted 'URW: Russia is the Victim' when 'URW: Discrediting Ukraine' was true |
| 8 | URW: Discrediting the West, Diplomacy | URW: Blaming the war on others rather th... | 2 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting the West, Diplomacy' was true |
| 9 | CC: Amplifying Climate Fears | CC: Criticism of institutions and author... | 1 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Amplifying Climate Fears' was true |
| 10 | CC: Amplifying Climate Fears | Other | 1 | Model predicted 'Other' when 'CC: Amplifying Climate Fears' was true |
| 11 | CC: Criticism of climate movement | CC: Amplifying Climate Fears | 1 | Model predicted 'CC: Amplifying Climate Fears' when 'CC: Criticism of climate movement' was true |
| 12 | CC: Criticism of climate movement | CC: Criticism of climate policies | 1 | Model predicted 'CC: Criticism of climate policies' when 'CC: Criticism of climate movement' was true |
| 13 | CC: Criticism of climate movement | CC: Criticism of institutions and author... | 1 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Criticism of climate movement' was true |
| 14 | CC: Criticism of climate movement | CC: Downplaying climate change | 1 | Model predicted 'CC: Downplaying climate change' when 'CC: Criticism of climate movement' was true |
| 15 | CC: Criticism of climate movement | CC: Questioning the measurements and sci... | 1 | Model predicted 'CC: Questioning the measurements and sci...' when 'CC: Criticism of climate movement' was true |
| 16 | CC: Downplaying climate change | CC: Amplifying Climate Fears | 1 | Model predicted 'CC: Amplifying Climate Fears' when 'CC: Downplaying climate change' was true |
| 17 | CC: Downplaying climate change | CC: Controversy about green technologies | 1 | Model predicted 'CC: Controversy about green technologies' when 'CC: Downplaying climate change' was true |
| 18 | CC: Downplaying climate change | CC: Criticism of climate policies | 1 | Model predicted 'CC: Criticism of climate policies' when 'CC: Downplaying climate change' was true |
| 19 | CC: Downplaying climate change | CC: Criticism of institutions and author... | 1 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Downplaying climate change' was true |
| 20 | CC: Downplaying climate change | CC: Questioning the measurements and sci... | 1 | Model predicted 'CC: Questioning the measurements and sci...' when 'CC: Downplaying climate change' was true |

## Narrative Label-Specific Confusion Analysis


### CC: Hidden plots by secret schemes of powerful groups

When **CC: Hidden plots by secret schemes of powerful groups** is the true label, it is often confused with:

- **CC: Controversy about green technologies**: 1 times
- **CC: Criticism of climate movement**: 1 times
- **CC: Criticism of climate policies**: 1 times
- **CC: Criticism of institutions and authorities**: 1 times
- **CC: Green policies are geopolitical instruments**: 1 times

### CC: Amplifying Climate Fears

When **CC: Amplifying Climate Fears** is the true label, it is often confused with:

- **CC: Criticism of institutions and authorities**: 1 times
- **Other**: 1 times

### URW: Amplifying war-related fears

When **URW: Amplifying war-related fears** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 3 times
- **URW: Speculating war outcomes**: 3 times
- **URW: Discrediting the West, Diplomacy**: 2 times
- **URW: Negative Consequences for the West**: 1 times
- **URW: Russia is the Victim**: 1 times

### URW: Discrediting Ukraine

When **URW: Discrediting Ukraine** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 4 times
- **URW: Discrediting the West, Diplomacy**: 4 times
- **URW: Distrust towards Media**: 2 times
- **URW: Russia is the Victim**: 2 times
- **URW: Amplifying war-related fears**: 1 times

### CC: Criticism of climate movement

When **CC: Criticism of climate movement** is the true label, it is often confused with:

- **CC: Amplifying Climate Fears**: 1 times
- **CC: Criticism of climate policies**: 1 times
- **CC: Criticism of institutions and authorities**: 1 times
- **CC: Downplaying climate change**: 1 times
- **CC: Questioning the measurements and science**: 1 times

### CC: Downplaying climate change

When **CC: Downplaying climate change** is the true label, it is often confused with:

- **CC: Amplifying Climate Fears**: 1 times
- **CC: Controversy about green technologies**: 1 times
- **CC: Criticism of climate policies**: 1 times
- **CC: Criticism of institutions and authorities**: 1 times
- **CC: Questioning the measurements and science**: 1 times

### URW: Negative Consequences for the West

When **URW: Negative Consequences for the West** is the true label, it is often confused with:

- **URW: Amplifying war-related fears**: 1 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Russia is the Victim**: 1 times

### URW: Discrediting the West, Diplomacy

When **URW: Discrediting the West, Diplomacy** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 2 times
- **URW: Discrediting Ukraine**: 1 times
- **URW: Distrust towards Media**: 1 times
- **URW: Negative Consequences for the West**: 1 times
- **URW: Praise of Russia**: 1 times

### URW: Russia is the Victim

When **URW: Russia is the Victim** is the true label, it is often confused with:

- **Other**: 1 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Distrust towards Media**: 1 times
- **URW: Negative Consequences for the West**: 1 times

### URW: Blaming the war on others rather than the invader

When **URW: Blaming the war on others rather than the invader** is the true label, it is often confused with:

- **URW: Discrediting Ukraine**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Distrust towards Media**: 1 times

### CC: Green policies are geopolitical instruments

When **CC: Green policies are geopolitical instruments** is the true label, it is often confused with:

- **Other**: 1 times

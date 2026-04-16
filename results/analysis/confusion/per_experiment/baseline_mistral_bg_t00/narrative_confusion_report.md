# Narrative Confusion Analysis Report

## Narrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| CC: Amplifying Climate Fears | 8 | 2 | 0 | 8 | 10 | 0.800 | 1.000 | 0.889 |
| CC: Downplaying climate change | 2 | 1 | 0 | 2 | 3 | 0.667 | 1.000 | 0.800 |
| URW: Discrediting Ukraine | 4 | 2 | 0 | 4 | 6 | 0.667 | 1.000 | 0.800 |
| URW: Amplifying war-related fears | 5 | 4 | 0 | 5 | 9 | 0.556 | 1.000 | 0.714 |
| CC: Criticism of climate movement | 1 | 1 | 0 | 1 | 2 | 0.500 | 1.000 | 0.667 |
| URW: Negative Consequences for the West | 1 | 4 | 0 | 1 | 5 | 0.200 | 1.000 | 0.333 |
| URW: Russia is the Victim | 2 | 8 | 0 | 2 | 10 | 0.200 | 1.000 | 0.333 |
| URW: Discrediting the West, Diplomacy | 2 | 12 | 0 | 2 | 14 | 0.143 | 1.000 | 0.250 |
| URW: Blaming the war on others rather than the invader | 1 | 12 | 0 | 1 | 13 | 0.077 | 1.000 | 0.143 |
| CC: Controversy about green technologies | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of climate policies | 0 | 5 | 0 | 0 | 5 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of institutions and authorities | 0 | 6 | 0 | 0 | 6 | 0.000 | 0.000 | 0.000 |
| CC: Green policies are geopolitical instruments | 0 | 1 | 1 | 1 | 1 | 0.000 | 0.000 | 0.000 |
| CC: Hidden plots by secret schemes of powerful groups | 0 | 0 | 1 | 1 | 0 | 0.000 | 0.000 | 0.000 |
| CC: Questioning the measurements and science | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| Other | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Distrust towards Media | 0 | 7 | 0 | 0 | 7 | 0.000 | 0.000 | 0.000 |
| URW: Hidden plots by secret schemes of powerful groups | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Praise of Russia | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Speculating war outcomes | 0 | 4 | 0 | 0 | 4 | 0.000 | 0.000 | 0.000 |

## Most Common Narrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | URW: Amplifying war-related fears | URW: Discrediting the West, Diplomacy | 5 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Amplifying war-related fears' was true |
| 2 | URW: Amplifying war-related fears | URW: Blaming the war on others rather th... | 4 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Amplifying war-related fears' was true |
| 3 | URW: Amplifying war-related fears | URW: Speculating war outcomes | 4 | Model predicted 'URW: Speculating war outcomes' when 'URW: Amplifying war-related fears' was true |
| 4 | URW: Discrediting Ukraine | URW: Blaming the war on others rather th... | 4 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting Ukraine' was true |
| 5 | URW: Discrediting Ukraine | URW: Discrediting the West, Diplomacy | 4 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Discrediting Ukraine' was true |
| 6 | CC: Amplifying Climate Fears | CC: Criticism of institutions and author... | 3 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Amplifying Climate Fears' was true |
| 7 | URW: Amplifying war-related fears | URW: Russia is the Victim | 3 | Model predicted 'URW: Russia is the Victim' when 'URW: Amplifying war-related fears' was true |
| 8 | URW: Discrediting Ukraine | URW: Distrust towards Media | 3 | Model predicted 'URW: Distrust towards Media' when 'URW: Discrediting Ukraine' was true |
| 9 | CC: Amplifying Climate Fears | CC: Criticism of climate policies | 2 | Model predicted 'CC: Criticism of climate policies' when 'CC: Amplifying Climate Fears' was true |
| 10 | URW: Discrediting Ukraine | URW: Amplifying war-related fears | 2 | Model predicted 'URW: Amplifying war-related fears' when 'URW: Discrediting Ukraine' was true |
| 11 | URW: Discrediting Ukraine | URW: Russia is the Victim | 2 | Model predicted 'URW: Russia is the Victim' when 'URW: Discrediting Ukraine' was true |
| 12 | URW: Discrediting the West, Diplomacy | URW: Blaming the war on others rather th... | 2 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting the West, Diplomacy' was true |
| 13 | URW: Discrediting the West, Diplomacy | URW: Praise of Russia | 2 | Model predicted 'URW: Praise of Russia' when 'URW: Discrediting the West, Diplomacy' was true |
| 14 | URW: Discrediting the West, Diplomacy | URW: Russia is the Victim | 2 | Model predicted 'URW: Russia is the Victim' when 'URW: Discrediting the West, Diplomacy' was true |
| 15 | URW: Russia is the Victim | URW: Discrediting the West, Diplomacy | 2 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Russia is the Victim' was true |
| 16 | URW: Russia is the Victim | URW: Distrust towards Media | 2 | Model predicted 'URW: Distrust towards Media' when 'URW: Russia is the Victim' was true |
| 17 | URW: Russia is the Victim | URW: Negative Consequences for the West | 2 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Russia is the Victim' was true |
| 18 | CC: Criticism of climate movement | CC: Amplifying Climate Fears | 1 | Model predicted 'CC: Amplifying Climate Fears' when 'CC: Criticism of climate movement' was true |
| 19 | CC: Criticism of climate movement | CC: Criticism of climate policies | 1 | Model predicted 'CC: Criticism of climate policies' when 'CC: Criticism of climate movement' was true |
| 20 | CC: Criticism of climate movement | CC: Criticism of institutions and author... | 1 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Criticism of climate movement' was true |

## Narrative Label-Specific Confusion Analysis


### CC: Amplifying Climate Fears

When **CC: Amplifying Climate Fears** is the true label, it is often confused with:

- **CC: Criticism of institutions and authorities**: 3 times
- **CC: Criticism of climate policies**: 2 times

### CC: Downplaying climate change

When **CC: Downplaying climate change** is the true label, it is often confused with:

- **CC: Amplifying Climate Fears**: 1 times
- **CC: Controversy about green technologies**: 1 times
- **CC: Criticism of climate policies**: 1 times
- **CC: Criticism of institutions and authorities**: 1 times
- **CC: Questioning the measurements and science**: 1 times

### URW: Discrediting Ukraine

When **URW: Discrediting Ukraine** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 4 times
- **URW: Discrediting the West, Diplomacy**: 4 times
- **URW: Distrust towards Media**: 3 times
- **URW: Amplifying war-related fears**: 2 times
- **URW: Russia is the Victim**: 2 times

### URW: Amplifying war-related fears

When **URW: Amplifying war-related fears** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 5 times
- **URW: Blaming the war on others rather than the inv...**: 4 times
- **URW: Speculating war outcomes**: 4 times
- **URW: Russia is the Victim**: 3 times
- **URW: Negative Consequences for the West**: 1 times

### CC: Criticism of climate movement

When **CC: Criticism of climate movement** is the true label, it is often confused with:

- **CC: Amplifying Climate Fears**: 1 times
- **CC: Criticism of climate policies**: 1 times
- **CC: Criticism of institutions and authorities**: 1 times
- **CC: Downplaying climate change**: 1 times
- **CC: Questioning the measurements and science**: 1 times

### URW: Negative Consequences for the West

When **URW: Negative Consequences for the West** is the true label, it is often confused with:

- **URW: Amplifying war-related fears**: 1 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Russia is the Victim**: 1 times

### URW: Russia is the Victim

When **URW: Russia is the Victim** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 2 times
- **URW: Distrust towards Media**: 2 times
- **URW: Negative Consequences for the West**: 2 times
- **URW: Amplifying war-related fears**: 1 times
- **URW: Blaming the war on others rather than the inv...**: 1 times

### URW: Discrediting the West, Diplomacy

When **URW: Discrediting the West, Diplomacy** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 2 times
- **URW: Praise of Russia**: 2 times
- **URW: Russia is the Victim**: 2 times
- **URW: Discrediting Ukraine**: 1 times
- **URW: Distrust towards Media**: 1 times

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
- **CC: Criticism of climate movement**: 1 times
- **CC: Criticism of climate policies**: 1 times
- **CC: Criticism of institutions and authorities**: 1 times
- **CC: Green policies are geopolitical instruments**: 1 times

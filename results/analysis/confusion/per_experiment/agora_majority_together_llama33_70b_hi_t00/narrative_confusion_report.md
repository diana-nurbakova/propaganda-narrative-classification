# Narrative Confusion Analysis Report

## Narrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| URW: Amplifying war-related fears | 7 | 0 | 1 | 8 | 7 | 1.000 | 0.875 | 0.933 |
| URW: Praise of Russia | 4 | 4 | 2 | 6 | 8 | 0.500 | 0.667 | 0.571 |
| URW: Blaming the war on others rather than the invader | 2 | 6 | 1 | 3 | 8 | 0.250 | 0.667 | 0.364 |
| URW: Discrediting the West, Diplomacy | 3 | 17 | 0 | 3 | 20 | 0.150 | 1.000 | 0.261 |
| CC: Amplifying Climate Fears | 0 | 0 | 4 | 4 | 0 | 0.000 | 0.000 | 0.000 |
| Other | 0 | 8 | 0 | 0 | 8 | 0.000 | 0.000 | 0.000 |
| URW: Discrediting Ukraine | 0 | 7 | 0 | 0 | 7 | 0.000 | 0.000 | 0.000 |
| URW: Distrust towards Media | 0 | 2 | 1 | 1 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Hidden plots by secret schemes of powerful groups | 0 | 0 | 2 | 2 | 0 | 0.000 | 0.000 | 0.000 |
| URW: Negative Consequences for the West | 0 | 6 | 0 | 0 | 6 | 0.000 | 0.000 | 0.000 |
| URW: Overpraising the West | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Russia is the Victim | 0 | 15 | 0 | 0 | 15 | 0.000 | 0.000 | 0.000 |
| URW: Speculating war outcomes | 0 | 7 | 2 | 2 | 7 | 0.000 | 0.000 | 0.000 |

## Most Common Narrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | URW: Amplifying war-related fears | URW: Discrediting the West, Diplomacy | 7 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Amplifying war-related fears' was true |
| 2 | URW: Praise of Russia | URW: Discrediting the West, Diplomacy | 6 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Praise of Russia' was true |
| 3 | URW: Amplifying war-related fears | URW: Speculating war outcomes | 5 | Model predicted 'URW: Speculating war outcomes' when 'URW: Amplifying war-related fears' was true |
| 4 | CC: Amplifying Climate Fears | Other | 4 | Model predicted 'Other' when 'CC: Amplifying Climate Fears' was true |
| 5 | URW: Amplifying war-related fears | URW: Russia is the Victim | 4 | Model predicted 'URW: Russia is the Victim' when 'URW: Amplifying war-related fears' was true |
| 6 | URW: Praise of Russia | URW: Russia is the Victim | 4 | Model predicted 'URW: Russia is the Victim' when 'URW: Praise of Russia' was true |
| 7 | URW: Blaming the war on others rather th... | URW: Russia is the Victim | 3 | Model predicted 'URW: Russia is the Victim' when 'URW: Blaming the war on others rather th...' was true |
| 8 | URW: Discrediting the West, Diplomacy | URW: Negative Consequences for the West | 3 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Discrediting the West, Diplomacy' was true |
| 9 | URW: Praise of Russia | URW: Blaming the war on others rather th... | 3 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Praise of Russia' was true |
| 10 | URW: Amplifying war-related fears | URW: Negative Consequences for the West | 2 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Amplifying war-related fears' was true |
| 11 | URW: Blaming the war on others rather th... | URW: Discrediting Ukraine | 2 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Blaming the war on others rather th...' was true |
| 12 | URW: Blaming the war on others rather th... | URW: Discrediting the West, Diplomacy | 2 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Blaming the war on others rather th...' was true |
| 13 | URW: Discrediting the West, Diplomacy | URW: Discrediting Ukraine | 2 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Discrediting the West, Diplomacy' was true |
| 14 | URW: Discrediting the West, Diplomacy | URW: Distrust towards Media | 2 | Model predicted 'URW: Distrust towards Media' when 'URW: Discrediting the West, Diplomacy' was true |
| 15 | URW: Discrediting the West, Diplomacy | URW: Praise of Russia | 2 | Model predicted 'URW: Praise of Russia' when 'URW: Discrediting the West, Diplomacy' was true |
| 16 | URW: Discrediting the West, Diplomacy | URW: Russia is the Victim | 2 | Model predicted 'URW: Russia is the Victim' when 'URW: Discrediting the West, Diplomacy' was true |
| 17 | URW: Praise of Russia | URW: Discrediting Ukraine | 2 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Praise of Russia' was true |
| 18 | URW: Amplifying war-related fears | Other | 1 | Model predicted 'Other' when 'URW: Amplifying war-related fears' was true |
| 19 | URW: Amplifying war-related fears | URW: Blaming the war on others rather th... | 1 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Amplifying war-related fears' was true |
| 20 | URW: Amplifying war-related fears | URW: Discrediting Ukraine | 1 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Amplifying war-related fears' was true |

## Narrative Label-Specific Confusion Analysis


### URW: Amplifying war-related fears

When **URW: Amplifying war-related fears** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 7 times
- **URW: Speculating war outcomes**: 5 times
- **URW: Russia is the Victim**: 4 times
- **URW: Negative Consequences for the West**: 2 times
- **Other**: 1 times

### URW: Praise of Russia

When **URW: Praise of Russia** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 6 times
- **URW: Russia is the Victim**: 4 times
- **URW: Blaming the war on others rather than the inv...**: 3 times
- **URW: Discrediting Ukraine**: 2 times

### URW: Blaming the war on others rather than the invader

When **URW: Blaming the war on others rather than the invader** is the true label, it is often confused with:

- **URW: Russia is the Victim**: 3 times
- **URW: Discrediting Ukraine**: 2 times
- **URW: Discrediting the West, Diplomacy**: 2 times
- **URW: Praise of Russia**: 1 times
- **URW: Speculating war outcomes**: 1 times

### URW: Discrediting the West, Diplomacy

When **URW: Discrediting the West, Diplomacy** is the true label, it is often confused with:

- **URW: Negative Consequences for the West**: 3 times
- **URW: Discrediting Ukraine**: 2 times
- **URW: Distrust towards Media**: 2 times
- **URW: Praise of Russia**: 2 times
- **URW: Russia is the Victim**: 2 times

### CC: Amplifying Climate Fears

When **CC: Amplifying Climate Fears** is the true label, it is often confused with:

- **Other**: 4 times

### URW: Distrust towards Media

When **URW: Distrust towards Media** is the true label, it is often confused with:

- **Other**: 1 times

### URW: Hidden plots by secret schemes of powerful groups

When **URW: Hidden plots by secret schemes of powerful groups** is the true label, it is often confused with:

- **Other**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Praise of Russia**: 1 times
- **URW: Russia is the Victim**: 1 times

### URW: Speculating war outcomes

When **URW: Speculating war outcomes** is the true label, it is often confused with:

- **Other**: 1 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Negative Consequences for the West**: 1 times
- **URW: Russia is the Victim**: 1 times

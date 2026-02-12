# Narrative Confusion Analysis Report

## Narrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| URW: Amplifying war-related fears | 7 | 1 | 1 | 8 | 8 | 0.875 | 0.875 | 0.875 |
| CC: Amplifying Climate Fears | 2 | 0 | 2 | 4 | 2 | 1.000 | 0.500 | 0.667 |
| URW: Blaming the war on others rather than the invader | 3 | 3 | 0 | 3 | 6 | 0.500 | 1.000 | 0.667 |
| URW: Discrediting the West, Diplomacy | 3 | 3 | 0 | 3 | 6 | 0.500 | 1.000 | 0.667 |
| URW: Speculating war outcomes | 1 | 11 | 1 | 2 | 12 | 0.083 | 0.500 | 0.143 |
| CC: Questioning the measurements and science | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| Other | 0 | 7 | 0 | 0 | 7 | 0.000 | 0.000 | 0.000 |
| URW: Discrediting Ukraine | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Distrust towards Media | 0 | 1 | 1 | 1 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Hidden plots by secret schemes of powerful groups | 0 | 0 | 2 | 2 | 0 | 0.000 | 0.000 | 0.000 |
| URW: Negative Consequences for the West | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| URW: Overpraising the West | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Praise of Russia | 0 | 2 | 6 | 6 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Russia is the Victim | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |

## Most Common Narrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | URW: Amplifying war-related fears | URW: Speculating war outcomes | 7 | Model predicted 'URW: Speculating war outcomes' when 'URW: Amplifying war-related fears' was true |
| 2 | URW: Praise of Russia | Other | 3 | Model predicted 'Other' when 'URW: Praise of Russia' was true |
| 3 | URW: Amplifying war-related fears | URW: Blaming the war on others rather th... | 2 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Amplifying war-related fears' was true |
| 4 | URW: Amplifying war-related fears | URW: Negative Consequences for the West | 2 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Amplifying war-related fears' was true |
| 5 | URW: Praise of Russia | URW: Speculating war outcomes | 2 | Model predicted 'URW: Speculating war outcomes' when 'URW: Praise of Russia' was true |
| 6 | CC: Amplifying Climate Fears | CC: Questioning the measurements and sci... | 1 | Model predicted 'CC: Questioning the measurements and sci...' when 'CC: Amplifying Climate Fears' was true |
| 7 | CC: Amplifying Climate Fears | Other | 1 | Model predicted 'Other' when 'CC: Amplifying Climate Fears' was true |
| 8 | URW: Amplifying war-related fears | Other | 1 | Model predicted 'Other' when 'URW: Amplifying war-related fears' was true |
| 9 | URW: Amplifying war-related fears | URW: Discrediting Ukraine | 1 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Amplifying war-related fears' was true |
| 10 | URW: Amplifying war-related fears | URW: Discrediting the West, Diplomacy | 1 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Amplifying war-related fears' was true |
| 11 | URW: Amplifying war-related fears | URW: Overpraising the West | 1 | Model predicted 'URW: Overpraising the West' when 'URW: Amplifying war-related fears' was true |
| 12 | URW: Amplifying war-related fears | URW: Russia is the Victim | 1 | Model predicted 'URW: Russia is the Victim' when 'URW: Amplifying war-related fears' was true |
| 13 | URW: Blaming the war on others rather th... | URW: Discrediting Ukraine | 1 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Blaming the war on others rather th...' was true |
| 14 | URW: Blaming the war on others rather th... | URW: Discrediting the West, Diplomacy | 1 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Blaming the war on others rather th...' was true |
| 15 | URW: Blaming the war on others rather th... | URW: Distrust towards Media | 1 | Model predicted 'URW: Distrust towards Media' when 'URW: Blaming the war on others rather th...' was true |
| 16 | URW: Blaming the war on others rather th... | URW: Praise of Russia | 1 | Model predicted 'URW: Praise of Russia' when 'URW: Blaming the war on others rather th...' was true |
| 17 | URW: Blaming the war on others rather th... | URW: Speculating war outcomes | 1 | Model predicted 'URW: Speculating war outcomes' when 'URW: Blaming the war on others rather th...' was true |
| 18 | URW: Discrediting the West, Diplomacy | URW: Negative Consequences for the West | 1 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Discrediting the West, Diplomacy' was true |
| 19 | URW: Discrediting the West, Diplomacy | URW: Praise of Russia | 1 | Model predicted 'URW: Praise of Russia' when 'URW: Discrediting the West, Diplomacy' was true |
| 20 | URW: Distrust towards Media | Other | 1 | Model predicted 'Other' when 'URW: Distrust towards Media' was true |

## Narrative Label-Specific Confusion Analysis


### URW: Amplifying war-related fears

When **URW: Amplifying war-related fears** is the true label, it is often confused with:

- **URW: Speculating war outcomes**: 7 times
- **URW: Blaming the war on others rather than the inv...**: 2 times
- **URW: Negative Consequences for the West**: 2 times
- **Other**: 1 times
- **URW: Discrediting Ukraine**: 1 times

### CC: Amplifying Climate Fears

When **CC: Amplifying Climate Fears** is the true label, it is often confused with:

- **CC: Questioning the measurements and science**: 1 times
- **Other**: 1 times

### URW: Blaming the war on others rather than the invader

When **URW: Blaming the war on others rather than the invader** is the true label, it is often confused with:

- **URW: Discrediting Ukraine**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Distrust towards Media**: 1 times
- **URW: Praise of Russia**: 1 times
- **URW: Speculating war outcomes**: 1 times

### URW: Discrediting the West, Diplomacy

When **URW: Discrediting the West, Diplomacy** is the true label, it is often confused with:

- **URW: Negative Consequences for the West**: 1 times
- **URW: Praise of Russia**: 1 times

### URW: Speculating war outcomes

When **URW: Speculating war outcomes** is the true label, it is often confused with:

- **URW: Amplifying war-related fears**: 1 times
- **URW: Russia is the Victim**: 1 times

### URW: Distrust towards Media

When **URW: Distrust towards Media** is the true label, it is often confused with:

- **Other**: 1 times

### URW: Hidden plots by secret schemes of powerful groups

When **URW: Hidden plots by secret schemes of powerful groups** is the true label, it is often confused with:

- **Other**: 1 times
- **URW: Speculating war outcomes**: 1 times

### URW: Praise of Russia

When **URW: Praise of Russia** is the true label, it is often confused with:

- **Other**: 3 times
- **URW: Speculating war outcomes**: 2 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times

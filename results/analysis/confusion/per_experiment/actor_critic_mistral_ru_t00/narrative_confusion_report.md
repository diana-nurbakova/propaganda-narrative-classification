# Narrative Confusion Analysis Report

## Narrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| URW: Discrediting Ukraine | 12 | 7 | 0 | 12 | 19 | 0.632 | 1.000 | 0.774 |
| URW: Praise of Russia | 6 | 6 | 2 | 8 | 12 | 0.500 | 0.750 | 0.600 |
| URW: Discrediting the West, Diplomacy | 4 | 12 | 1 | 5 | 16 | 0.250 | 0.800 | 0.381 |
| URW: Amplifying war-related fears | 1 | 5 | 0 | 1 | 6 | 0.167 | 1.000 | 0.286 |
| URW: Speculating war outcomes | 1 | 6 | 0 | 1 | 7 | 0.143 | 1.000 | 0.250 |
| Other | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Blaming the war on others rather than the invader | 0 | 22 | 0 | 0 | 22 | 0.000 | 0.000 | 0.000 |
| URW: Distrust towards Media | 0 | 13 | 0 | 0 | 13 | 0.000 | 0.000 | 0.000 |
| URW: Hidden plots by secret schemes of powerful groups | 0 | 0 | 1 | 1 | 0 | 0.000 | 0.000 | 0.000 |
| URW: Negative Consequences for the West | 0 | 5 | 0 | 0 | 5 | 0.000 | 0.000 | 0.000 |
| URW: Overpraising the West | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Russia is the Victim | 0 | 8 | 0 | 0 | 8 | 0.000 | 0.000 | 0.000 |

## Most Common Narrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | URW: Discrediting Ukraine | URW: Blaming the war on others rather th... | 11 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting Ukraine' was true |
| 2 | URW: Discrediting Ukraine | URW: Distrust towards Media | 6 | Model predicted 'URW: Distrust towards Media' when 'URW: Discrediting Ukraine' was true |
| 3 | URW: Discrediting Ukraine | URW: Discrediting the West, Diplomacy | 5 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Discrediting Ukraine' was true |
| 4 | URW: Discrediting Ukraine | URW: Praise of Russia | 5 | Model predicted 'URW: Praise of Russia' when 'URW: Discrediting Ukraine' was true |
| 5 | URW: Praise of Russia | URW: Blaming the war on others rather th... | 5 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Praise of Russia' was true |
| 6 | URW: Discrediting the West, Diplomacy | URW: Blaming the war on others rather th... | 4 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting the West, Diplomacy' was true |
| 7 | URW: Praise of Russia | URW: Discrediting the West, Diplomacy | 4 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Praise of Russia' was true |
| 8 | URW: Discrediting Ukraine | URW: Russia is the Victim | 3 | Model predicted 'URW: Russia is the Victim' when 'URW: Discrediting Ukraine' was true |
| 9 | URW: Discrediting the West, Diplomacy | URW: Distrust towards Media | 3 | Model predicted 'URW: Distrust towards Media' when 'URW: Discrediting the West, Diplomacy' was true |
| 10 | URW: Praise of Russia | URW: Discrediting Ukraine | 3 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Praise of Russia' was true |
| 11 | URW: Praise of Russia | URW: Distrust towards Media | 3 | Model predicted 'URW: Distrust towards Media' when 'URW: Praise of Russia' was true |
| 12 | URW: Discrediting Ukraine | URW: Amplifying war-related fears | 2 | Model predicted 'URW: Amplifying war-related fears' when 'URW: Discrediting Ukraine' was true |
| 13 | URW: Discrediting Ukraine | URW: Speculating war outcomes | 2 | Model predicted 'URW: Speculating war outcomes' when 'URW: Discrediting Ukraine' was true |
| 14 | URW: Discrediting the West, Diplomacy | URW: Amplifying war-related fears | 2 | Model predicted 'URW: Amplifying war-related fears' when 'URW: Discrediting the West, Diplomacy' was true |
| 15 | URW: Discrediting the West, Diplomacy | URW: Discrediting Ukraine | 2 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Discrediting the West, Diplomacy' was true |
| 16 | URW: Discrediting the West, Diplomacy | URW: Russia is the Victim | 2 | Model predicted 'URW: Russia is the Victim' when 'URW: Discrediting the West, Diplomacy' was true |
| 17 | URW: Praise of Russia | URW: Russia is the Victim | 2 | Model predicted 'URW: Russia is the Victim' when 'URW: Praise of Russia' was true |
| 18 | URW: Praise of Russia | URW: Speculating war outcomes | 2 | Model predicted 'URW: Speculating war outcomes' when 'URW: Praise of Russia' was true |
| 19 | URW: Amplifying war-related fears | URW: Discrediting the West, Diplomacy | 1 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Amplifying war-related fears' was true |
| 20 | URW: Amplifying war-related fears | URW: Distrust towards Media | 1 | Model predicted 'URW: Distrust towards Media' when 'URW: Amplifying war-related fears' was true |

## Narrative Label-Specific Confusion Analysis


### URW: Discrediting Ukraine

When **URW: Discrediting Ukraine** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 11 times
- **URW: Distrust towards Media**: 6 times
- **URW: Discrediting the West, Diplomacy**: 5 times
- **URW: Praise of Russia**: 5 times
- **URW: Russia is the Victim**: 3 times

### URW: Praise of Russia

When **URW: Praise of Russia** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 5 times
- **URW: Discrediting the West, Diplomacy**: 4 times
- **URW: Discrediting Ukraine**: 3 times
- **URW: Distrust towards Media**: 3 times
- **URW: Russia is the Victim**: 2 times

### URW: Discrediting the West, Diplomacy

When **URW: Discrediting the West, Diplomacy** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 4 times
- **URW: Distrust towards Media**: 3 times
- **URW: Amplifying war-related fears**: 2 times
- **URW: Discrediting Ukraine**: 2 times
- **URW: Russia is the Victim**: 2 times

### URW: Amplifying war-related fears

When **URW: Amplifying war-related fears** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Distrust towards Media**: 1 times
- **URW: Negative Consequences for the West**: 1 times
- **URW: Speculating war outcomes**: 1 times

### URW: Speculating war outcomes

When **URW: Speculating war outcomes** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting Ukraine**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times

### URW: Hidden plots by secret schemes of powerful groups

When **URW: Hidden plots by secret schemes of powerful groups** is the true label, it is often confused with:

- **URW: Amplifying war-related fears**: 1 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting Ukraine**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Negative Consequences for the West**: 1 times

# Narrative Confusion Analysis Report

## Narrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| URW: Discrediting Ukraine | 11 | 5 | 1 | 12 | 16 | 0.688 | 0.917 | 0.786 |
| URW: Praise of Russia | 4 | 6 | 3 | 7 | 10 | 0.400 | 0.571 | 0.471 |
| URW: Amplifying war-related fears | 1 | 3 | 0 | 1 | 4 | 0.250 | 1.000 | 0.400 |
| URW: Discrediting the West, Diplomacy | 4 | 12 | 1 | 5 | 16 | 0.250 | 0.800 | 0.381 |
| Other | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Blaming the war on others rather than the invader | 0 | 15 | 0 | 0 | 15 | 0.000 | 0.000 | 0.000 |
| URW: Distrust towards Media | 0 | 5 | 0 | 0 | 5 | 0.000 | 0.000 | 0.000 |
| URW: Hidden plots by secret schemes of powerful groups | 0 | 0 | 1 | 1 | 0 | 0.000 | 0.000 | 0.000 |
| URW: Negative Consequences for the West | 0 | 6 | 0 | 0 | 6 | 0.000 | 0.000 | 0.000 |
| URW: Overpraising the West | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Russia is the Victim | 0 | 5 | 0 | 0 | 5 | 0.000 | 0.000 | 0.000 |
| URW: Speculating war outcomes | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |

## Most Common Narrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | URW: Discrediting Ukraine | URW: Blaming the war on others rather th... | 10 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting Ukraine' was true |
| 2 | URW: Discrediting Ukraine | URW: Discrediting the West, Diplomacy | 6 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Discrediting Ukraine' was true |
| 3 | URW: Discrediting Ukraine | URW: Praise of Russia | 4 | Model predicted 'URW: Praise of Russia' when 'URW: Discrediting Ukraine' was true |
| 4 | URW: Praise of Russia | URW: Discrediting the West, Diplomacy | 4 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Praise of Russia' was true |
| 5 | URW: Discrediting Ukraine | URW: Distrust towards Media | 2 | Model predicted 'URW: Distrust towards Media' when 'URW: Discrediting Ukraine' was true |
| 6 | URW: Discrediting Ukraine | URW: Russia is the Victim | 2 | Model predicted 'URW: Russia is the Victim' when 'URW: Discrediting Ukraine' was true |
| 7 | URW: Discrediting the West, Diplomacy | URW: Blaming the war on others rather th... | 2 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting the West, Diplomacy' was true |
| 8 | URW: Discrediting the West, Diplomacy | URW: Discrediting Ukraine | 2 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Discrediting the West, Diplomacy' was true |
| 9 | URW: Discrediting the West, Diplomacy | URW: Distrust towards Media | 2 | Model predicted 'URW: Distrust towards Media' when 'URW: Discrediting the West, Diplomacy' was true |
| 10 | URW: Praise of Russia | URW: Blaming the war on others rather th... | 2 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Praise of Russia' was true |
| 11 | URW: Praise of Russia | URW: Discrediting Ukraine | 2 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Praise of Russia' was true |
| 12 | URW: Praise of Russia | URW: Negative Consequences for the West | 2 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Praise of Russia' was true |
| 13 | URW: Amplifying war-related fears | URW: Discrediting the West, Diplomacy | 1 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Amplifying war-related fears' was true |
| 14 | URW: Amplifying war-related fears | URW: Distrust towards Media | 1 | Model predicted 'URW: Distrust towards Media' when 'URW: Amplifying war-related fears' was true |
| 15 | URW: Amplifying war-related fears | URW: Negative Consequences for the West | 1 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Amplifying war-related fears' was true |
| 16 | URW: Discrediting Ukraine | Other | 1 | Model predicted 'Other' when 'URW: Discrediting Ukraine' was true |
| 17 | URW: Discrediting Ukraine | URW: Amplifying war-related fears | 1 | Model predicted 'URW: Amplifying war-related fears' when 'URW: Discrediting Ukraine' was true |
| 18 | URW: Discrediting Ukraine | URW: Negative Consequences for the West | 1 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Discrediting Ukraine' was true |
| 19 | URW: Discrediting Ukraine | URW: Overpraising the West | 1 | Model predicted 'URW: Overpraising the West' when 'URW: Discrediting Ukraine' was true |
| 20 | URW: Discrediting Ukraine | URW: Speculating war outcomes | 1 | Model predicted 'URW: Speculating war outcomes' when 'URW: Discrediting Ukraine' was true |

## Narrative Label-Specific Confusion Analysis


### URW: Discrediting Ukraine

When **URW: Discrediting Ukraine** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 10 times
- **URW: Discrediting the West, Diplomacy**: 6 times
- **URW: Praise of Russia**: 4 times
- **URW: Distrust towards Media**: 2 times
- **URW: Russia is the Victim**: 2 times

### URW: Praise of Russia

When **URW: Praise of Russia** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 4 times
- **URW: Blaming the war on others rather than the inv...**: 2 times
- **URW: Discrediting Ukraine**: 2 times
- **URW: Negative Consequences for the West**: 2 times
- **Other**: 1 times

### URW: Amplifying war-related fears

When **URW: Amplifying war-related fears** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Distrust towards Media**: 1 times
- **URW: Negative Consequences for the West**: 1 times

### URW: Discrediting the West, Diplomacy

When **URW: Discrediting the West, Diplomacy** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 2 times
- **URW: Discrediting Ukraine**: 2 times
- **URW: Distrust towards Media**: 2 times
- **URW: Amplifying war-related fears**: 1 times
- **URW: Negative Consequences for the West**: 1 times

### URW: Hidden plots by secret schemes of powerful groups

When **URW: Hidden plots by secret schemes of powerful groups** is the true label, it is often confused with:

- **URW: Amplifying war-related fears**: 1 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting Ukraine**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Negative Consequences for the West**: 1 times

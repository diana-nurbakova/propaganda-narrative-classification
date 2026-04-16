# Narrative Confusion Analysis Report

## Narrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| URW: Discrediting Ukraine | 11 | 10 | 1 | 12 | 21 | 0.524 | 0.917 | 0.667 |
| URW: Amplifying war-related fears | 1 | 1 | 0 | 1 | 2 | 0.500 | 1.000 | 0.667 |
| URW: Praise of Russia | 4 | 5 | 4 | 8 | 9 | 0.444 | 0.500 | 0.471 |
| URW: Discrediting the West, Diplomacy | 5 | 15 | 0 | 5 | 20 | 0.250 | 1.000 | 0.400 |
| URW: Speculating war outcomes | 1 | 9 | 0 | 1 | 10 | 0.100 | 1.000 | 0.182 |
| Other | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| URW: Blaming the war on others rather than the invader | 0 | 14 | 0 | 0 | 14 | 0.000 | 0.000 | 0.000 |
| URW: Distrust towards Media | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Hidden plots by secret schemes of powerful groups | 0 | 0 | 1 | 1 | 0 | 0.000 | 0.000 | 0.000 |
| URW: Negative Consequences for the West | 0 | 5 | 0 | 0 | 5 | 0.000 | 0.000 | 0.000 |
| URW: Russia is the Victim | 0 | 12 | 0 | 0 | 12 | 0.000 | 0.000 | 0.000 |

## Most Common Narrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | URW: Discrediting Ukraine | URW: Blaming the war on others rather th... | 9 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting Ukraine' was true |
| 2 | URW: Discrediting Ukraine | URW: Discrediting the West, Diplomacy | 9 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Discrediting Ukraine' was true |
| 3 | URW: Discrediting Ukraine | URW: Russia is the Victim | 5 | Model predicted 'URW: Russia is the Victim' when 'URW: Discrediting Ukraine' was true |
| 4 | URW: Praise of Russia | URW: Discrediting Ukraine | 4 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Praise of Russia' was true |
| 5 | URW: Praise of Russia | URW: Russia is the Victim | 4 | Model predicted 'URW: Russia is the Victim' when 'URW: Praise of Russia' was true |
| 6 | URW: Discrediting Ukraine | URW: Praise of Russia | 3 | Model predicted 'URW: Praise of Russia' when 'URW: Discrediting Ukraine' was true |
| 7 | URW: Discrediting the West, Diplomacy | URW: Discrediting Ukraine | 3 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Discrediting the West, Diplomacy' was true |
| 8 | URW: Discrediting the West, Diplomacy | URW: Speculating war outcomes | 3 | Model predicted 'URW: Speculating war outcomes' when 'URW: Discrediting the West, Diplomacy' was true |
| 9 | URW: Praise of Russia | URW: Discrediting the West, Diplomacy | 3 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Praise of Russia' was true |
| 10 | URW: Discrediting Ukraine | URW: Negative Consequences for the West | 2 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Discrediting Ukraine' was true |
| 11 | URW: Discrediting Ukraine | URW: Speculating war outcomes | 2 | Model predicted 'URW: Speculating war outcomes' when 'URW: Discrediting Ukraine' was true |
| 12 | URW: Discrediting the West, Diplomacy | URW: Negative Consequences for the West | 2 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Discrediting the West, Diplomacy' was true |
| 13 | URW: Discrediting the West, Diplomacy | URW: Russia is the Victim | 2 | Model predicted 'URW: Russia is the Victim' when 'URW: Discrediting the West, Diplomacy' was true |
| 14 | URW: Praise of Russia | Other | 2 | Model predicted 'Other' when 'URW: Praise of Russia' was true |
| 15 | URW: Praise of Russia | URW: Blaming the war on others rather th... | 2 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Praise of Russia' was true |
| 16 | URW: Praise of Russia | URW: Speculating war outcomes | 2 | Model predicted 'URW: Speculating war outcomes' when 'URW: Praise of Russia' was true |
| 17 | URW: Amplifying war-related fears | URW: Blaming the war on others rather th... | 1 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Amplifying war-related fears' was true |
| 18 | URW: Amplifying war-related fears | URW: Discrediting Ukraine | 1 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Amplifying war-related fears' was true |
| 19 | URW: Amplifying war-related fears | URW: Discrediting the West, Diplomacy | 1 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Amplifying war-related fears' was true |
| 20 | URW: Amplifying war-related fears | URW: Distrust towards Media | 1 | Model predicted 'URW: Distrust towards Media' when 'URW: Amplifying war-related fears' was true |

## Narrative Label-Specific Confusion Analysis


### URW: Discrediting Ukraine

When **URW: Discrediting Ukraine** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 9 times
- **URW: Discrediting the West, Diplomacy**: 9 times
- **URW: Russia is the Victim**: 5 times
- **URW: Praise of Russia**: 3 times
- **URW: Negative Consequences for the West**: 2 times

### URW: Amplifying war-related fears

When **URW: Amplifying war-related fears** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting Ukraine**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Distrust towards Media**: 1 times
- **URW: Negative Consequences for the West**: 1 times

### URW: Praise of Russia

When **URW: Praise of Russia** is the true label, it is often confused with:

- **URW: Discrediting Ukraine**: 4 times
- **URW: Russia is the Victim**: 4 times
- **URW: Discrediting the West, Diplomacy**: 3 times
- **Other**: 2 times
- **URW: Blaming the war on others rather than the inv...**: 2 times

### URW: Discrediting the West, Diplomacy

When **URW: Discrediting the West, Diplomacy** is the true label, it is often confused with:

- **URW: Discrediting Ukraine**: 3 times
- **URW: Speculating war outcomes**: 3 times
- **URW: Negative Consequences for the West**: 2 times
- **URW: Russia is the Victim**: 2 times
- **URW: Blaming the war on others rather than the inv...**: 1 times

### URW: Speculating war outcomes

When **URW: Speculating war outcomes** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting Ukraine**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times

### URW: Hidden plots by secret schemes of powerful groups

When **URW: Hidden plots by secret schemes of powerful groups** is the true label, it is often confused with:

- **URW: Discrediting Ukraine**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Praise of Russia**: 1 times
- **URW: Russia is the Victim**: 1 times
- **URW: Speculating war outcomes**: 1 times

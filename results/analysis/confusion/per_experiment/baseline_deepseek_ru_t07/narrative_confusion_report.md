# Narrative Confusion Analysis Report

## Narrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| URW: Discrediting Ukraine | 12 | 8 | 0 | 12 | 20 | 0.600 | 1.000 | 0.750 |
| URW: Praise of Russia | 5 | 5 | 3 | 8 | 10 | 0.500 | 0.625 | 0.556 |
| URW: Amplifying war-related fears | 1 | 3 | 0 | 1 | 4 | 0.250 | 1.000 | 0.400 |
| URW: Speculating war outcomes | 1 | 4 | 0 | 1 | 5 | 0.200 | 1.000 | 0.333 |
| URW: Discrediting the West, Diplomacy | 3 | 14 | 2 | 5 | 17 | 0.176 | 0.600 | 0.273 |
| Other | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Blaming the war on others rather than the invader | 0 | 12 | 0 | 0 | 12 | 0.000 | 0.000 | 0.000 |
| URW: Hidden plots by secret schemes of powerful groups | 0 | 1 | 1 | 1 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Negative Consequences for the West | 0 | 5 | 0 | 0 | 5 | 0.000 | 0.000 | 0.000 |
| URW: Russia is the Victim | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |

## Most Common Narrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | URW: Discrediting Ukraine | URW: Discrediting the West, Diplomacy | 8 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Discrediting Ukraine' was true |
| 2 | URW: Discrediting Ukraine | URW: Blaming the war on others rather th... | 6 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting Ukraine' was true |
| 3 | URW: Praise of Russia | URW: Discrediting Ukraine | 4 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Praise of Russia' was true |
| 4 | URW: Discrediting Ukraine | URW: Praise of Russia | 3 | Model predicted 'URW: Praise of Russia' when 'URW: Discrediting Ukraine' was true |
| 5 | URW: Praise of Russia | URW: Discrediting the West, Diplomacy | 3 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Praise of Russia' was true |
| 6 | URW: Discrediting Ukraine | URW: Speculating war outcomes | 2 | Model predicted 'URW: Speculating war outcomes' when 'URW: Discrediting Ukraine' was true |
| 7 | URW: Discrediting the West, Diplomacy | URW: Discrediting Ukraine | 2 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Discrediting the West, Diplomacy' was true |
| 8 | URW: Praise of Russia | URW: Blaming the war on others rather th... | 2 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Praise of Russia' was true |
| 9 | URW: Praise of Russia | URW: Negative Consequences for the West | 2 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Praise of Russia' was true |
| 10 | URW: Amplifying war-related fears | URW: Blaming the war on others rather th... | 1 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Amplifying war-related fears' was true |
| 11 | URW: Amplifying war-related fears | URW: Discrediting the West, Diplomacy | 1 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Amplifying war-related fears' was true |
| 12 | URW: Amplifying war-related fears | URW: Negative Consequences for the West | 1 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Amplifying war-related fears' was true |
| 13 | URW: Discrediting Ukraine | URW: Amplifying war-related fears | 1 | Model predicted 'URW: Amplifying war-related fears' when 'URW: Discrediting Ukraine' was true |
| 14 | URW: Discrediting Ukraine | URW: Russia is the Victim | 1 | Model predicted 'URW: Russia is the Victim' when 'URW: Discrediting Ukraine' was true |
| 15 | URW: Discrediting the West, Diplomacy | URW: Amplifying war-related fears | 1 | Model predicted 'URW: Amplifying war-related fears' when 'URW: Discrediting the West, Diplomacy' was true |
| 16 | URW: Discrediting the West, Diplomacy | URW: Blaming the war on others rather th... | 1 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting the West, Diplomacy' was true |
| 17 | URW: Discrediting the West, Diplomacy | URW: Hidden plots by secret schemes of p... | 1 | Model predicted 'URW: Hidden plots by secret schemes of p...' when 'URW: Discrediting the West, Diplomacy' was true |
| 18 | URW: Discrediting the West, Diplomacy | URW: Negative Consequences for the West | 1 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Discrediting the West, Diplomacy' was true |
| 19 | URW: Discrediting the West, Diplomacy | URW: Praise of Russia | 1 | Model predicted 'URW: Praise of Russia' when 'URW: Discrediting the West, Diplomacy' was true |
| 20 | URW: Hidden plots by secret schemes of p... | URW: Amplifying war-related fears | 1 | Model predicted 'URW: Amplifying war-related fears' when 'URW: Hidden plots by secret schemes of p...' was true |

## Narrative Label-Specific Confusion Analysis


### URW: Discrediting Ukraine

When **URW: Discrediting Ukraine** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 8 times
- **URW: Blaming the war on others rather than the inv...**: 6 times
- **URW: Praise of Russia**: 3 times
- **URW: Speculating war outcomes**: 2 times
- **URW: Amplifying war-related fears**: 1 times

### URW: Praise of Russia

When **URW: Praise of Russia** is the true label, it is often confused with:

- **URW: Discrediting Ukraine**: 4 times
- **URW: Discrediting the West, Diplomacy**: 3 times
- **URW: Blaming the war on others rather than the inv...**: 2 times
- **URW: Negative Consequences for the West**: 2 times
- **Other**: 1 times

### URW: Amplifying war-related fears

When **URW: Amplifying war-related fears** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Negative Consequences for the West**: 1 times

### URW: Speculating war outcomes

When **URW: Speculating war outcomes** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting Ukraine**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times

### URW: Discrediting the West, Diplomacy

When **URW: Discrediting the West, Diplomacy** is the true label, it is often confused with:

- **URW: Discrediting Ukraine**: 2 times
- **URW: Amplifying war-related fears**: 1 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Hidden plots by secret schemes of powerful gr...**: 1 times
- **URW: Negative Consequences for the West**: 1 times

### URW: Hidden plots by secret schemes of powerful groups

When **URW: Hidden plots by secret schemes of powerful groups** is the true label, it is often confused with:

- **URW: Amplifying war-related fears**: 1 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting Ukraine**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Negative Consequences for the West**: 1 times

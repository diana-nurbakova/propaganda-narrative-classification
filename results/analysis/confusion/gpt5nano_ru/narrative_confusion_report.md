# Narrative Confusion Analysis Report

## Narrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| URW: Discrediting Ukraine | 10 | 5 | 2 | 12 | 15 | 0.667 | 0.833 | 0.741 |
| URW: Praise of Russia | 4 | 0 | 4 | 8 | 4 | 1.000 | 0.500 | 0.667 |
| URW: Amplifying war-related fears | 1 | 2 | 0 | 1 | 3 | 0.333 | 1.000 | 0.500 |
| URW: Discrediting the West, Diplomacy | 2 | 9 | 3 | 5 | 11 | 0.182 | 0.400 | 0.250 |
| URW: Speculating war outcomes | 1 | 11 | 0 | 1 | 12 | 0.083 | 1.000 | 0.154 |
| Other | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Blaming the war on others rather than the invader | 0 | 5 | 0 | 0 | 5 | 0.000 | 0.000 | 0.000 |
| URW: Distrust towards Media | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Hidden plots by secret schemes of powerful groups | 0 | 2 | 1 | 1 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Negative Consequences for the West | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Russia is the Victim | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |

## Most Common Narrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | URW: Discrediting Ukraine | URW: Blaming the war on others rather th... | 4 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting Ukraine' was true |
| 2 | URW: Discrediting Ukraine | URW: Speculating war outcomes | 4 | Model predicted 'URW: Speculating war outcomes' when 'URW: Discrediting Ukraine' was true |
| 3 | URW: Praise of Russia | URW: Discrediting the West, Diplomacy | 4 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Praise of Russia' was true |
| 4 | URW: Discrediting Ukraine | URW: Discrediting the West, Diplomacy | 3 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Discrediting Ukraine' was true |
| 5 | URW: Discrediting the West, Diplomacy | URW: Speculating war outcomes | 3 | Model predicted 'URW: Speculating war outcomes' when 'URW: Discrediting the West, Diplomacy' was true |
| 6 | URW: Discrediting the West, Diplomacy | URW: Discrediting Ukraine | 2 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Discrediting the West, Diplomacy' was true |
| 7 | URW: Praise of Russia | URW: Discrediting Ukraine | 2 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Praise of Russia' was true |
| 8 | URW: Praise of Russia | URW: Speculating war outcomes | 2 | Model predicted 'URW: Speculating war outcomes' when 'URW: Praise of Russia' was true |
| 9 | URW: Amplifying war-related fears | URW: Speculating war outcomes | 1 | Model predicted 'URW: Speculating war outcomes' when 'URW: Amplifying war-related fears' was true |
| 10 | URW: Discrediting Ukraine | Other | 1 | Model predicted 'Other' when 'URW: Discrediting Ukraine' was true |
| 11 | URW: Discrediting Ukraine | URW: Amplifying war-related fears | 1 | Model predicted 'URW: Amplifying war-related fears' when 'URW: Discrediting Ukraine' was true |
| 12 | URW: Discrediting Ukraine | URW: Hidden plots by secret schemes of p... | 1 | Model predicted 'URW: Hidden plots by secret schemes of p...' when 'URW: Discrediting Ukraine' was true |
| 13 | URW: Discrediting Ukraine | URW: Russia is the Victim | 1 | Model predicted 'URW: Russia is the Victim' when 'URW: Discrediting Ukraine' was true |
| 14 | URW: Discrediting the West, Diplomacy | URW: Hidden plots by secret schemes of p... | 1 | Model predicted 'URW: Hidden plots by secret schemes of p...' when 'URW: Discrediting the West, Diplomacy' was true |
| 15 | URW: Discrediting the West, Diplomacy | URW: Negative Consequences for the West | 1 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Discrediting the West, Diplomacy' was true |
| 16 | URW: Discrediting the West, Diplomacy | URW: Russia is the Victim | 1 | Model predicted 'URW: Russia is the Victim' when 'URW: Discrediting the West, Diplomacy' was true |
| 17 | URW: Hidden plots by secret schemes of p... | URW: Amplifying war-related fears | 1 | Model predicted 'URW: Amplifying war-related fears' when 'URW: Hidden plots by secret schemes of p...' was true |
| 18 | URW: Hidden plots by secret schemes of p... | URW: Blaming the war on others rather th... | 1 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Hidden plots by secret schemes of p...' was true |
| 19 | URW: Hidden plots by secret schemes of p... | URW: Discrediting the West, Diplomacy | 1 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Hidden plots by secret schemes of p...' was true |
| 20 | URW: Hidden plots by secret schemes of p... | URW: Distrust towards Media | 1 | Model predicted 'URW: Distrust towards Media' when 'URW: Hidden plots by secret schemes of p...' was true |

## Narrative Label-Specific Confusion Analysis


### URW: Discrediting Ukraine

When **URW: Discrediting Ukraine** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 4 times
- **URW: Speculating war outcomes**: 4 times
- **URW: Discrediting the West, Diplomacy**: 3 times
- **Other**: 1 times
- **URW: Amplifying war-related fears**: 1 times

### URW: Praise of Russia

When **URW: Praise of Russia** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 4 times
- **URW: Discrediting Ukraine**: 2 times
- **URW: Speculating war outcomes**: 2 times
- **Other**: 1 times
- **URW: Negative Consequences for the West**: 1 times

### URW: Amplifying war-related fears

When **URW: Amplifying war-related fears** is the true label, it is often confused with:

- **URW: Speculating war outcomes**: 1 times

### URW: Discrediting the West, Diplomacy

When **URW: Discrediting the West, Diplomacy** is the true label, it is often confused with:

- **URW: Speculating war outcomes**: 3 times
- **URW: Discrediting Ukraine**: 2 times
- **URW: Hidden plots by secret schemes of powerful gr...**: 1 times
- **URW: Negative Consequences for the West**: 1 times
- **URW: Russia is the Victim**: 1 times

### URW: Speculating war outcomes

When **URW: Speculating war outcomes** is the true label, it is often confused with:

- **URW: Discrediting Ukraine**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times

### URW: Hidden plots by secret schemes of powerful groups

When **URW: Hidden plots by secret schemes of powerful groups** is the true label, it is often confused with:

- **URW: Amplifying war-related fears**: 1 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Distrust towards Media**: 1 times
- **URW: Speculating war outcomes**: 1 times

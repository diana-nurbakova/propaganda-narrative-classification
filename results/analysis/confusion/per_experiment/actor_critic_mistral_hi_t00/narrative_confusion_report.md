# Narrative Confusion Analysis Report

## Narrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| URW: Amplifying war-related fears | 7 | 1 | 1 | 8 | 8 | 0.875 | 0.875 | 0.875 |
| CC: Amplifying Climate Fears | 3 | 0 | 1 | 4 | 3 | 1.000 | 0.750 | 0.857 |
| URW: Praise of Russia | 4 | 4 | 2 | 6 | 8 | 0.500 | 0.667 | 0.571 |
| URW: Blaming the war on others rather than the invader | 3 | 16 | 0 | 3 | 19 | 0.158 | 1.000 | 0.273 |
| URW: Speculating war outcomes | 1 | 5 | 1 | 2 | 6 | 0.167 | 0.500 | 0.250 |
| URW: Discrediting the West, Diplomacy | 2 | 18 | 1 | 3 | 20 | 0.100 | 0.667 | 0.174 |
| URW: Distrust towards Media | 1 | 10 | 0 | 1 | 11 | 0.091 | 1.000 | 0.167 |
| CC: Criticism of institutions and authorities | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| CC: Downplaying climate change | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| Other | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| URW: Discrediting Ukraine | 0 | 8 | 0 | 0 | 8 | 0.000 | 0.000 | 0.000 |
| URW: Hidden plots by secret schemes of powerful groups | 0 | 0 | 2 | 2 | 0 | 0.000 | 0.000 | 0.000 |
| URW: Negative Consequences for the West | 0 | 9 | 0 | 0 | 9 | 0.000 | 0.000 | 0.000 |
| URW: Russia is the Victim | 0 | 14 | 0 | 0 | 14 | 0.000 | 0.000 | 0.000 |

## Most Common Narrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | URW: Amplifying war-related fears | URW: Blaming the war on others rather th... | 8 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Amplifying war-related fears' was true |
| 2 | URW: Amplifying war-related fears | URW: Discrediting the West, Diplomacy | 7 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Amplifying war-related fears' was true |
| 3 | URW: Amplifying war-related fears | URW: Russia is the Victim | 5 | Model predicted 'URW: Russia is the Victim' when 'URW: Amplifying war-related fears' was true |
| 4 | URW: Praise of Russia | URW: Blaming the war on others rather th... | 5 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Praise of Russia' was true |
| 5 | URW: Amplifying war-related fears | URW: Negative Consequences for the West | 4 | Model predicted 'URW: Negative Consequences for the West' when 'URW: Amplifying war-related fears' was true |
| 6 | URW: Amplifying war-related fears | URW: Speculating war outcomes | 4 | Model predicted 'URW: Speculating war outcomes' when 'URW: Amplifying war-related fears' was true |
| 7 | URW: Praise of Russia | URW: Discrediting the West, Diplomacy | 4 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Praise of Russia' was true |
| 8 | URW: Blaming the war on others rather th... | URW: Russia is the Victim | 3 | Model predicted 'URW: Russia is the Victim' when 'URW: Blaming the war on others rather th...' was true |
| 9 | URW: Praise of Russia | URW: Discrediting Ukraine | 3 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Praise of Russia' was true |
| 10 | URW: Praise of Russia | URW: Distrust towards Media | 3 | Model predicted 'URW: Distrust towards Media' when 'URW: Praise of Russia' was true |
| 11 | CC: Amplifying Climate Fears | CC: Criticism of institutions and author... | 2 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Amplifying Climate Fears' was true |
| 12 | URW: Amplifying war-related fears | URW: Distrust towards Media | 2 | Model predicted 'URW: Distrust towards Media' when 'URW: Amplifying war-related fears' was true |
| 13 | URW: Blaming the war on others rather th... | URW: Discrediting Ukraine | 2 | Model predicted 'URW: Discrediting Ukraine' when 'URW: Blaming the war on others rather th...' was true |
| 14 | URW: Blaming the war on others rather th... | URW: Discrediting the West, Diplomacy | 2 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Blaming the war on others rather th...' was true |
| 15 | URW: Blaming the war on others rather th... | URW: Distrust towards Media | 2 | Model predicted 'URW: Distrust towards Media' when 'URW: Blaming the war on others rather th...' was true |
| 16 | URW: Blaming the war on others rather th... | URW: Praise of Russia | 2 | Model predicted 'URW: Praise of Russia' when 'URW: Blaming the war on others rather th...' was true |
| 17 | URW: Discrediting the West, Diplomacy | URW: Distrust towards Media | 2 | Model predicted 'URW: Distrust towards Media' when 'URW: Discrediting the West, Diplomacy' was true |
| 18 | URW: Discrediting the West, Diplomacy | URW: Russia is the Victim | 2 | Model predicted 'URW: Russia is the Victim' when 'URW: Discrediting the West, Diplomacy' was true |
| 19 | URW: Hidden plots by secret schemes of p... | URW: Discrediting the West, Diplomacy | 2 | Model predicted 'URW: Discrediting the West, Diplomacy' when 'URW: Hidden plots by secret schemes of p...' was true |
| 20 | URW: Praise of Russia | URW: Russia is the Victim | 2 | Model predicted 'URW: Russia is the Victim' when 'URW: Praise of Russia' was true |

## Narrative Label-Specific Confusion Analysis


### URW: Amplifying war-related fears

When **URW: Amplifying war-related fears** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 8 times
- **URW: Discrediting the West, Diplomacy**: 7 times
- **URW: Russia is the Victim**: 5 times
- **URW: Negative Consequences for the West**: 4 times
- **URW: Speculating war outcomes**: 4 times

### CC: Amplifying Climate Fears

When **CC: Amplifying Climate Fears** is the true label, it is often confused with:

- **CC: Criticism of institutions and authorities**: 2 times
- **CC: Downplaying climate change**: 1 times
- **Other**: 1 times

### URW: Praise of Russia

When **URW: Praise of Russia** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 5 times
- **URW: Discrediting the West, Diplomacy**: 4 times
- **URW: Discrediting Ukraine**: 3 times
- **URW: Distrust towards Media**: 3 times
- **URW: Russia is the Victim**: 2 times

### URW: Blaming the war on others rather than the invader

When **URW: Blaming the war on others rather than the invader** is the true label, it is often confused with:

- **URW: Russia is the Victim**: 3 times
- **URW: Discrediting Ukraine**: 2 times
- **URW: Discrediting the West, Diplomacy**: 2 times
- **URW: Distrust towards Media**: 2 times
- **URW: Praise of Russia**: 2 times

### URW: Speculating war outcomes

When **URW: Speculating war outcomes** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 2 times
- **URW: Negative Consequences for the West**: 2 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting Ukraine**: 1 times
- **URW: Russia is the Victim**: 1 times

### URW: Discrediting the West, Diplomacy

When **URW: Discrediting the West, Diplomacy** is the true label, it is often confused with:

- **URW: Distrust towards Media**: 2 times
- **URW: Russia is the Victim**: 2 times
- **Other**: 1 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting Ukraine**: 1 times

### URW: Distrust towards Media

When **URW: Distrust towards Media** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 1 times
- **URW: Russia is the Victim**: 1 times

### URW: Hidden plots by secret schemes of powerful groups

When **URW: Hidden plots by secret schemes of powerful groups** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy**: 2 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting Ukraine**: 1 times
- **URW: Distrust towards Media**: 1 times
- **URW: Negative Consequences for the West**: 1 times

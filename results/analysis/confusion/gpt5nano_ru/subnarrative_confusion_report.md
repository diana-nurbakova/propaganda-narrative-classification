# Subnarrative Confusion Analysis Report

## Subnarrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| URW: Praise of Russia: Praise of Russian military might | 2 | 0 | 0 | 2 | 2 | 1.000 | 1.000 | 1.000 |
| URW: Speculating war outcomes: Ukrainian army is collapsing | 1 | 0 | 0 | 1 | 1 | 1.000 | 1.000 | 1.000 |
| URW: Discrediting Ukraine: Ukraine is a hub for criminal act... | 1 | 0 | 1 | 2 | 1 | 1.000 | 0.500 | 0.667 |
| URW: Discrediting Ukraine: Ukraine is associated with nazism | 1 | 1 | 0 | 1 | 2 | 0.500 | 1.000 | 0.667 |
| URW: Praise of Russia: Russia has international support from... | 1 | 0 | 2 | 3 | 1 | 1.000 | 0.333 | 0.500 |
| URW: Discrediting Ukraine: Discrediting Ukrainian military | 2 | 4 | 1 | 3 | 6 | 0.333 | 0.667 | 0.444 |
| URW: Discrediting Ukraine: Ukraine is a puppet of the West | 2 | 6 | 0 | 2 | 8 | 0.250 | 1.000 | 0.400 |
| URW: Discrediting the West, Diplomacy: The West does not car... | 1 | 4 | 0 | 1 | 5 | 0.200 | 1.000 | 0.333 |
| URW: Discrediting Ukraine: Discrediting Ukrainian government... | 1 | 11 | 2 | 3 | 12 | 0.083 | 0.333 | 0.133 |
| Other | 0 | 4 | 0 | 0 | 4 | 0.000 | 0.000 | 0.000 |
| URW: Amplifying war-related fears: By continuing the war we ... | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Amplifying war-related fears: NATO should/will directly... | 0 | 1 | 1 | 1 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Amplifying war-related fears: Other | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Amplifying war-related fears: There is a real possibili... | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Blaming the war on others rather than the invader: The ... | 0 | 4 | 0 | 0 | 4 | 0.000 | 0.000 | 0.000 |
| URW: Blaming the war on others rather than the invader: Ukra... | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| URW: Discrediting Ukraine: Situation in Ukraine is hopeless | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Discrediting the West, Diplomacy: Diplomacy does/will n... | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| URW: Discrediting the West, Diplomacy: Other | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| URW: Discrediting the West, Diplomacy: The EU is divided | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| URW: Discrediting the West, Diplomacy: The West is overreact... | 0 | 0 | 1 | 1 | 0 | 0.000 | 0.000 | 0.000 |
| URW: Discrediting the West, Diplomacy: The West is weak | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| URW: Discrediting the West, Diplomacy: West is tired of Ukra... | 0 | 0 | 1 | 1 | 0 | 0.000 | 0.000 | 0.000 |
| URW: Distrust towards Media: Ukrainian media cannot be trust... | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Hidden plots by secret schemes of powerful groups: Othe... | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Negative Consequences for the West: Other | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Negative Consequences for the West: Sanctions imposed b... | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Praise of Russia: Other | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Praise of Russia: Praise of Russian President Vladimir ... | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Praise of Russia: Russia is a guarantor of peace and pr... | 0 | 0 | 2 | 2 | 0 | 0.000 | 0.000 | 0.000 |
| URW: Russia is the Victim: Other | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Russia is the Victim: The West is russophobic | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Russia is the Victim: UA is anti-RU extremists | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Speculating war outcomes: Other | 0 | 9 | 0 | 0 | 9 | 0.000 | 0.000 | 0.000 |

## Most Common Subnarrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | URW: Discrediting Ukraine: Discrediting ... | Other | 2 | Model predicted 'Other' when 'URW: Discrediting Ukraine: Discrediting ...' was true |
| 2 | URW: Discrediting Ukraine: Discrediting ... | URW: Discrediting Ukraine: Discrediting ... | 2 | Model predicted 'URW: Discrediting Ukraine: Discrediting ...' when 'URW: Discrediting Ukraine: Discrediting ...' was true |
| 3 | URW: Discrediting Ukraine: Ukraine is a ... | URW: Discrediting Ukraine: Discrediting ... | 2 | Model predicted 'URW: Discrediting Ukraine: Discrediting ...' when 'URW: Discrediting Ukraine: Ukraine is a ...' was true |
| 4 | URW: Amplifying war-related fears: NATO ... | URW: Amplifying war-related fears: Other | 1 | Model predicted 'URW: Amplifying war-related fears: Other' when 'URW: Amplifying war-related fears: NATO ...' was true |
| 5 | URW: Discrediting Ukraine: Discrediting ... | URW: Discrediting Ukraine: Ukraine is a ... | 1 | Model predicted 'URW: Discrediting Ukraine: Ukraine is a ...' when 'URW: Discrediting Ukraine: Discrediting ...' was true |
| 6 | URW: Discrediting Ukraine: Discrediting ... | URW: Hidden plots by secret schemes of p... | 1 | Model predicted 'URW: Hidden plots by secret schemes of p...' when 'URW: Discrediting Ukraine: Discrediting ...' was true |
| 7 | URW: Discrediting Ukraine: Discrediting ... | URW: Speculating war outcomes: Other | 1 | Model predicted 'URW: Speculating war outcomes: Other' when 'URW: Discrediting Ukraine: Discrediting ...' was true |
| 8 | URW: Discrediting Ukraine: Discrediting ... | Other | 1 | Model predicted 'Other' when 'URW: Discrediting Ukraine: Discrediting ...' was true |
| 9 | URW: Discrediting Ukraine: Discrediting ... | URW: Blaming the war on others rather th... | 1 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting Ukraine: Discrediting ...' was true |
| 10 | URW: Discrediting Ukraine: Discrediting ... | URW: Blaming the war on others rather th... | 1 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting Ukraine: Discrediting ...' was true |
| 11 | URW: Discrediting Ukraine: Discrediting ... | URW: Discrediting Ukraine: Ukraine is a ... | 1 | Model predicted 'URW: Discrediting Ukraine: Ukraine is a ...' when 'URW: Discrediting Ukraine: Discrediting ...' was true |
| 12 | URW: Discrediting Ukraine: Discrediting ... | URW: Discrediting Ukraine: Ukraine is as... | 1 | Model predicted 'URW: Discrediting Ukraine: Ukraine is as...' when 'URW: Discrediting Ukraine: Discrediting ...' was true |
| 13 | URW: Discrediting Ukraine: Discrediting ... | URW: Discrediting the West, Diplomacy: T... | 1 | Model predicted 'URW: Discrediting the West, Diplomacy: T...' when 'URW: Discrediting Ukraine: Discrediting ...' was true |
| 14 | URW: Discrediting Ukraine: Discrediting ... | URW: Russia is the Victim: Other | 1 | Model predicted 'URW: Russia is the Victim: Other' when 'URW: Discrediting Ukraine: Discrediting ...' was true |
| 15 | URW: Discrediting Ukraine: Discrediting ... | URW: Russia is the Victim: UA is anti-RU... | 1 | Model predicted 'URW: Russia is the Victim: UA is anti-RU...' when 'URW: Discrediting Ukraine: Discrediting ...' was true |
| 16 | URW: Discrediting Ukraine: Ukraine is a ... | URW: Blaming the war on others rather th... | 1 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting Ukraine: Ukraine is a ...' was true |
| 17 | URW: Discrediting Ukraine: Ukraine is a ... | URW: Blaming the war on others rather th... | 1 | Model predicted 'URW: Blaming the war on others rather th...' when 'URW: Discrediting Ukraine: Ukraine is a ...' was true |
| 18 | URW: Discrediting Ukraine: Ukraine is a ... | URW: Discrediting Ukraine: Discrediting ... | 1 | Model predicted 'URW: Discrediting Ukraine: Discrediting ...' when 'URW: Discrediting Ukraine: Ukraine is a ...' was true |
| 19 | URW: Discrediting Ukraine: Ukraine is a ... | URW: Discrediting Ukraine: Discrediting ... | 1 | Model predicted 'URW: Discrediting Ukraine: Discrediting ...' when 'URW: Discrediting Ukraine: Ukraine is a ...' was true |
| 20 | URW: Discrediting Ukraine: Ukraine is a ... | URW: Discrediting Ukraine: Ukraine is a ... | 1 | Model predicted 'URW: Discrediting Ukraine: Ukraine is a ...' when 'URW: Discrediting Ukraine: Ukraine is a ...' was true |

## Subnarrative Label-Specific Confusion Analysis


### URW: Praise of Russia: Praise of Russian military might

When **URW: Praise of Russia: Praise of Russian military might** is the true label, it is often confused with:

- **URW: Discrediting Ukraine: Discrediting Ukrainian ...**: 1 times

### URW: Speculating war outcomes: Ukrainian army is collapsing

When **URW: Speculating war outcomes: Ukrainian army is collapsing** is the true label, it is often confused with:

- **URW: Discrediting Ukraine: Discrediting Ukrainian ...**: 1 times
- **URW: Discrediting Ukraine: Discrediting Ukrainian ...**: 1 times
- **URW: Discrediting Ukraine: Situation in Ukraine is...**: 1 times
- **URW: Discrediting Ukraine: Ukraine is a puppet of ...**: 1 times
- **URW: Discrediting the West, Diplomacy: Diplomacy d...**: 1 times

### URW: Discrediting Ukraine: Ukraine is a hub for criminal act...

When **URW: Discrediting Ukraine: Ukraine is a hub for criminal act...** is the true label, it is often confused with:

- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting Ukraine: Discrediting Ukrainian ...**: 1 times
- **URW: Discrediting Ukraine: Discrediting Ukrainian ...**: 1 times
- **URW: Discrediting Ukraine: Ukraine is a puppet of ...**: 1 times

### URW: Discrediting Ukraine: Ukraine is associated with nazism

When **URW: Discrediting Ukraine: Ukraine is associated with nazism** is the true label, it is often confused with:

- **URW: Amplifying war-related fears: Other**: 1 times
- **URW: Discrediting Ukraine: Discrediting Ukrainian ...**: 1 times
- **URW: Discrediting Ukraine: Situation in Ukraine is...**: 1 times
- **URW: Speculating war outcomes: Other**: 1 times

### URW: Praise of Russia: Russia has international support from...

When **URW: Praise of Russia: Russia has international support from...** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy: Diplomacy d...**: 1 times
- **URW: Discrediting the West, Diplomacy: Other**: 1 times
- **URW: Discrediting the West, Diplomacy: The West is...**: 1 times
- **URW: Negative Consequences for the West: Other**: 1 times
- **URW: Praise of Russia: Praise of Russian President...**: 1 times

### URW: Discrediting Ukraine: Discrediting Ukrainian military

When **URW: Discrediting Ukraine: Discrediting Ukrainian military** is the true label, it is often confused with:

- **URW: Discrediting Ukraine: Discrediting Ukrainian ...**: 2 times
- **Other**: 1 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Discrediting Ukraine: Ukraine is a puppet of ...**: 1 times

### URW: Discrediting Ukraine: Ukraine is a puppet of the West

When **URW: Discrediting Ukraine: Ukraine is a puppet of the West** is the true label, it is often confused with:

- **URW: Discrediting Ukraine: Discrediting Ukrainian ...**: 2 times
- **URW: Blaming the war on others rather than the inv...**: 1 times
- **URW: Speculating war outcomes: Other**: 1 times

### URW: Discrediting the West, Diplomacy: The West does not car...

When **URW: Discrediting the West, Diplomacy: The West does not car...** is the true label, it is often confused with:

- **URW: Discrediting Ukraine: Discrediting Ukrainian ...**: 1 times
- **URW: Discrediting Ukraine: Discrediting Ukrainian ...**: 1 times
- **URW: Discrediting Ukraine: Ukraine is a puppet of ...**: 1 times
- **URW: Hidden plots by secret schemes of powerful gr...**: 1 times

### URW: Discrediting Ukraine: Discrediting Ukrainian government...

When **URW: Discrediting Ukraine: Discrediting Ukrainian government...** is the true label, it is often confused with:

- **Other**: 2 times
- **URW: Discrediting Ukraine: Ukraine is a puppet of ...**: 1 times
- **URW: Hidden plots by secret schemes of powerful gr...**: 1 times
- **URW: Speculating war outcomes: Other**: 1 times

### URW: Amplifying war-related fears: NATO should/will directly...

When **URW: Amplifying war-related fears: NATO should/will directly...** is the true label, it is often confused with:

- **URW: Amplifying war-related fears: Other**: 1 times

# Subnarrative Confusion Analysis Report

## Subnarrative Label-wise Performance Statistics

| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |
|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|
| CC: Criticism of institutions and authorities: Criticism of ... | 1 | 0 | 0 | 1 | 1 | 1.000 | 1.000 | 1.000 |
| URW: Discrediting Ukraine: Discrediting Ukrainian government... | 1 | 0 | 0 | 1 | 1 | 1.000 | 1.000 | 1.000 |
| URW: Russia is the Victim: The West is russophobic | 1 | 0 | 0 | 1 | 1 | 1.000 | 1.000 | 1.000 |
| CC: Criticism of institutions and authorities: Criticism of ... | 1 | 1 | 0 | 1 | 2 | 0.500 | 1.000 | 0.667 |
| CC: Criticism of institutions and authorities: Criticism of ... | 1 | 2 | 0 | 1 | 3 | 0.333 | 1.000 | 0.500 |
| CC: Amplifying Climate Fears: Amplifying existing fears of g... | 4 | 6 | 5 | 9 | 10 | 0.400 | 0.444 | 0.421 |
| CC: Criticism of institutions and authorities: Criticism of ... | 1 | 3 | 0 | 1 | 4 | 0.250 | 1.000 | 0.400 |
| CC: Amplifying Climate Fears: Doomsday scenarios for humans | 0 | 5 | 0 | 0 | 5 | 0.000 | 0.000 | 0.000 |
| CC: Amplifying Climate Fears: Other | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of climate movement: Climate movement is corru... | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of climate policies: Climate policies are inef... | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of climate policies: Climate policies are only... | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of climate policies: Climate policies have neg... | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of climate policies: Other | 0 | 3 | 0 | 0 | 3 | 0.000 | 0.000 | 0.000 |
| CC: Criticism of institutions and authorities: Other | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| CC: Green policies are geopolitical instruments: Climate-rel... | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| Other | 0 | 5 | 0 | 0 | 5 | 0.000 | 0.000 | 0.000 |
| URW: Blaming the war on others rather than the invader: Othe... | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Discrediting Ukraine: Ukraine is a puppet of the West | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Discrediting the West, Diplomacy: Diplomacy does/will n... | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Discrediting the West, Diplomacy: The West does not car... | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Discrediting the West, Diplomacy: The West is weak | 0 | 2 | 0 | 0 | 2 | 0.000 | 0.000 | 0.000 |
| URW: Negative Consequences for the West: Sanctions imposed b... | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Overpraising the West: The West belongs in the right si... | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Praise of Russia: Other | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |
| URW: Praise of Russia: Russia has international support from... | 0 | 0 | 1 | 1 | 0 | 0.000 | 0.000 | 0.000 |
| URW: Praise of Russia: Russia is a guarantor of peace and pr... | 0 | 0 | 1 | 1 | 0 | 0.000 | 0.000 | 0.000 |
| URW: Russia is the Victim: Other | 0 | 1 | 0 | 0 | 1 | 0.000 | 0.000 | 0.000 |

## Most Common Subnarrative Confusion Patterns

Shows cases where a true label is present but a different label is predicted.

| Rank | True Label | Wrongly Predicted Label | Count | Description |
|------|------------|------------------------|-------|-------------|
| 1 | CC: Amplifying Climate Fears: Amplifying... | Other | 5 | Model predicted 'Other' when 'CC: Amplifying Climate Fears: Amplifying...' was true |
| 2 | CC: Amplifying Climate Fears: Amplifying... | CC: Amplifying Climate Fears: Doomsday s... | 1 | Model predicted 'CC: Amplifying Climate Fears: Doomsday s...' when 'CC: Amplifying Climate Fears: Amplifying...' was true |
| 3 | CC: Criticism of institutions and author... | CC: Amplifying Climate Fears: Amplifying... | 1 | Model predicted 'CC: Amplifying Climate Fears: Amplifying...' when 'CC: Criticism of institutions and author...' was true |
| 4 | CC: Criticism of institutions and author... | CC: Amplifying Climate Fears: Doomsday s... | 1 | Model predicted 'CC: Amplifying Climate Fears: Doomsday s...' when 'CC: Criticism of institutions and author...' was true |
| 5 | CC: Criticism of institutions and author... | CC: Criticism of climate movement: Clima... | 1 | Model predicted 'CC: Criticism of climate movement: Clima...' when 'CC: Criticism of institutions and author...' was true |
| 6 | CC: Criticism of institutions and author... | CC: Criticism of institutions and author... | 1 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Criticism of institutions and author...' was true |
| 7 | CC: Criticism of institutions and author... | CC: Amplifying Climate Fears: Amplifying... | 1 | Model predicted 'CC: Amplifying Climate Fears: Amplifying...' when 'CC: Criticism of institutions and author...' was true |
| 8 | CC: Criticism of institutions and author... | CC: Amplifying Climate Fears: Other | 1 | Model predicted 'CC: Amplifying Climate Fears: Other' when 'CC: Criticism of institutions and author...' was true |
| 9 | CC: Criticism of institutions and author... | CC: Criticism of climate policies: Clima... | 1 | Model predicted 'CC: Criticism of climate policies: Clima...' when 'CC: Criticism of institutions and author...' was true |
| 10 | CC: Criticism of institutions and author... | CC: Amplifying Climate Fears: Amplifying... | 1 | Model predicted 'CC: Amplifying Climate Fears: Amplifying...' when 'CC: Criticism of institutions and author...' was true |
| 11 | CC: Criticism of institutions and author... | CC: Amplifying Climate Fears: Doomsday s... | 1 | Model predicted 'CC: Amplifying Climate Fears: Doomsday s...' when 'CC: Criticism of institutions and author...' was true |
| 12 | CC: Criticism of institutions and author... | CC: Criticism of climate policies: Clima... | 1 | Model predicted 'CC: Criticism of climate policies: Clima...' when 'CC: Criticism of institutions and author...' was true |
| 13 | CC: Criticism of institutions and author... | CC: Criticism of climate policies: Other | 1 | Model predicted 'CC: Criticism of climate policies: Other' when 'CC: Criticism of institutions and author...' was true |
| 14 | CC: Criticism of institutions and author... | CC: Criticism of institutions and author... | 1 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Criticism of institutions and author...' was true |
| 15 | CC: Criticism of institutions and author... | CC: Criticism of institutions and author... | 1 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Criticism of institutions and author...' was true |
| 16 | CC: Criticism of institutions and author... | CC: Criticism of climate policies: Other | 1 | Model predicted 'CC: Criticism of climate policies: Other' when 'CC: Criticism of institutions and author...' was true |
| 17 | CC: Criticism of institutions and author... | CC: Criticism of institutions and author... | 1 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Criticism of institutions and author...' was true |
| 18 | CC: Criticism of institutions and author... | CC: Criticism of institutions and author... | 1 | Model predicted 'CC: Criticism of institutions and author...' when 'CC: Criticism of institutions and author...' was true |
| 19 | CC: Criticism of institutions and author... | CC: Green policies are geopolitical inst... | 1 | Model predicted 'CC: Green policies are geopolitical inst...' when 'CC: Criticism of institutions and author...' was true |
| 20 | URW: Discrediting Ukraine: Discrediting ... | URW: Discrediting Ukraine: Ukraine is a ... | 1 | Model predicted 'URW: Discrediting Ukraine: Ukraine is a ...' when 'URW: Discrediting Ukraine: Discrediting ...' was true |

## Subnarrative Label-Specific Confusion Analysis


### CC: Criticism of institutions and authorities: Criticism of ...

When **CC: Criticism of institutions and authorities: Criticism of ...** is the true label, it is often confused with:

- **CC: Criticism of climate policies: Other**: 1 times
- **CC: Criticism of institutions and authorities: Cri...**: 1 times
- **CC: Criticism of institutions and authorities: Cri...**: 1 times
- **CC: Green policies are geopolitical instruments: C...**: 1 times

### URW: Discrediting Ukraine: Discrediting Ukrainian government...

When **URW: Discrediting Ukraine: Discrediting Ukrainian government...** is the true label, it is often confused with:

- **URW: Discrediting Ukraine: Ukraine is a puppet of ...**: 1 times
- **URW: Discrediting the West, Diplomacy: Diplomacy d...**: 1 times
- **URW: Discrediting the West, Diplomacy: The West do...**: 1 times

### URW: Russia is the Victim: The West is russophobic

When **URW: Russia is the Victim: The West is russophobic** is the true label, it is often confused with:

- **URW: Discrediting the West, Diplomacy: The West is...**: 1 times
- **URW: Russia is the Victim: Other**: 1 times

### CC: Criticism of institutions and authorities: Criticism of ...

When **CC: Criticism of institutions and authorities: Criticism of ...** is the true label, it is often confused with:

- **CC: Amplifying Climate Fears: Amplifying existing ...**: 1 times
- **CC: Amplifying Climate Fears: Doomsday scenarios f...**: 1 times
- **CC: Criticism of climate policies: Climate policie...**: 1 times
- **CC: Criticism of climate policies: Other**: 1 times
- **CC: Criticism of institutions and authorities: Cri...**: 1 times

### CC: Criticism of institutions and authorities: Criticism of ...

When **CC: Criticism of institutions and authorities: Criticism of ...** is the true label, it is often confused with:

- **CC: Amplifying Climate Fears: Amplifying existing ...**: 1 times
- **CC: Amplifying Climate Fears: Doomsday scenarios f...**: 1 times
- **CC: Criticism of climate movement: Climate movemen...**: 1 times
- **CC: Criticism of institutions and authorities: Oth...**: 1 times

### CC: Amplifying Climate Fears: Amplifying existing fears of g...

When **CC: Amplifying Climate Fears: Amplifying existing fears of g...** is the true label, it is often confused with:

- **Other**: 5 times
- **CC: Amplifying Climate Fears: Doomsday scenarios f...**: 1 times

### CC: Criticism of institutions and authorities: Criticism of ...

When **CC: Criticism of institutions and authorities: Criticism of ...** is the true label, it is often confused with:

- **CC: Amplifying Climate Fears: Amplifying existing ...**: 1 times
- **CC: Amplifying Climate Fears: Other**: 1 times
- **CC: Criticism of climate policies: Climate policie...**: 1 times

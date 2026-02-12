# Dataset Statistics Report

Statistics for the SemEval-2025 Task 10 propaganda narrative classification dataset.

## 1. Dataset Overview

| Split | Language | Articles | Unique Narratives | Unique Subnarratives | Avg Narr/Article | Avg Sub/Article | Other % | Multi-label % |
|-------|----------|----------|-------------------|----------------------|------------------|-----------------|---------|---------------|
| Train | EN | 399 | 20 | 42 | 0.51 | 0.36 | 49.1% | 0.0% |
| Train | BG | 401 | 17 | 45 | 0.89 | 0.76 | 11.0% | 0.0% |
| Train | HI | 366 | 14 | 29 | 0.53 | 0.40 | 47.3% | 0.0% |
| Train | PT | 400 | 18 | 30 | 0.63 | 0.33 | 37.0% | 0.0% |
| Train | RU | 133 | 10 | 23 | 1.00 | 0.89 | 0.0% | 0.0% |
| Dev | EN | 41 | 13 | 20 | 0.73 | 0.59 | 26.8% | 0.0% |
| Dev | BG | 35 | 11 | 13 | 0.80 | 0.57 | 20.0% | 0.0% |
| Dev | HI | 35 | 8 | 13 | 0.83 | 0.54 | 17.1% | 0.0% |
| Dev | PT | 35 | 7 | 9 | 0.71 | 0.49 | 28.6% | 0.0% |
| Dev | RU | 32 | 6 | 13 | 0.88 | 0.72 | 12.5% | 0.0% |
| Test | EN | 101 | - | - | - | - | - | - |
| Test | BG | 100 | - | - | - | - | - | - |
| Test | HI | 99 | - | - | - | - | - | - |
| Test | PT | 100 | - | - | - | - | - | - |
| Test | RU | 60 | - | - | - | - | - | - |
|-------|----------|----------|-------------------|----------------------|------------------|-----------------|---------|---------------|
| **Train** | **Total** | **1699** | **21** | **64** | **0.67** | **0.50** | **33.0%** | **0.0%** |
| **Dev** | **Total** | **178** | **21** | **43** | **0.79** | **0.58** | **21.3%** | **0.0%** |
| **Test** | **Total** | **460** | - | - | - | - | - | - |

## 2. Category Balance (CC vs URW)

| Split | Language | CC Articles | URW Articles | Both | CC % | URW % |
|-------|----------|-------------|--------------|------|------|-------|
| Train | EN | 95 | 108 | 0 | 23.8% | 27.1% |
| Train | BG | 107 | 250 | 0 | 26.7% | 62.3% |
| Train | HI | 31 | 162 | 0 | 8.5% | 44.3% |
| Train | PT | 100 | 152 | 0 | 25.0% | 38.0% |
| Train | RU | 0 | 133 | 0 | 0.0% | 100.0% |
| Dev | EN | 17 | 13 | 0 | 41.5% | 31.7% |
| Dev | BG | 13 | 15 | 0 | 37.1% | 42.9% |
| Dev | HI | 4 | 25 | 0 | 11.4% | 71.4% |
| Dev | PT | 19 | 6 | 0 | 54.3% | 17.1% |
| Dev | RU | 0 | 28 | 0 | 0.0% | 87.5% |

## 3a. Narrative Distribution — Train Set

| Narrative | EN | BG | HI | PT | RU | Total |
|-----------|----:|----:|----:|----:|----:|------:|
| CC: Amplifying Climate Fears | 1 | 73 | 28 | 58 | 0 | 160 |
| CC: Climate change is beneficial | 0 | 1 | 0 | 1 | 0 | 2 |
| CC: Controversy about green technologies | 5 | 1 | 0 | 1 | 0 | 7 |
| CC: Criticism of climate movement | 19 | 0 | 0 | 7 | 0 | 26 |
| CC: Criticism of climate policies | 14 | 13 | 2 | 3 | 0 | 32 |
| CC: Criticism of institutions and authorities | 23 | 9 | 1 | 21 | 0 | 54 |
| CC: Downplaying climate change | 8 | 7 | 0 | 8 | 0 | 23 |
| CC: Green policies are geopolitical instruments | 1 | 0 | 0 | 0 | 0 | 1 |
| CC: Hidden plots by secret schemes of powerful groups | 16 | 3 | 0 | 1 | 0 | 20 |
| CC: Questioning the measurements and science | 8 | 0 | 0 | 0 | 0 | 8 |
| URW: Amplifying war-related fears | 20 | 42 | 41 | 23 | 3 | 129 |
| URW: Blaming the war on others rather than the invader | 10 | 22 | 11 | 10 | 10 | 63 |
| URW: Discrediting Ukraine | 14 | 63 | 15 | 51 | 47 | 190 |
| URW: Discrediting the West, Diplomacy | 28 | 63 | 9 | 26 | 17 | 143 |
| URW: Distrust towards Media | 7 | 3 | 11 | 1 | 2 | 24 |
| URW: Hidden plots by secret schemes of powerful groups | 6 | 0 | 4 | 1 | 2 | 13 |
| URW: Negative Consequences for the West | 6 | 7 | 2 | 3 | 1 | 19 |
| URW: Overpraising the West | 3 | 1 | 7 | 0 | 0 | 11 |
| URW: Praise of Russia | 5 | 25 | 35 | 21 | 38 | 124 |
| URW: Russia is the Victim | 3 | 6 | 8 | 11 | 12 | 40 |
| URW: Speculating war outcomes | 6 | 18 | 19 | 5 | 1 | 49 |
| **Total** | **203** | **357** | **193** | **252** | **133** | **1138** |

## 3b. Narrative Distribution — Dev Set

| Narrative | EN | BG | HI | PT | RU | Total |
|-----------|----:|----:|----:|----:|----:|------:|
| CC: Amplifying Climate Fears | 0 | 8 | 4 | 13 | 0 | 25 |
| CC: Climate change is beneficial | 1 | 0 | 0 | 0 | 0 | 1 |
| CC: Controversy about green technologies | 1 | 0 | 0 | 0 | 0 | 1 |
| CC: Criticism of climate movement | 6 | 1 | 0 | 0 | 0 | 7 |
| CC: Criticism of climate policies | 3 | 0 | 0 | 2 | 0 | 5 |
| CC: Criticism of institutions and authorities | 3 | 0 | 0 | 4 | 0 | 7 |
| CC: Downplaying climate change | 0 | 2 | 0 | 0 | 0 | 2 |
| CC: Green policies are geopolitical instruments | 0 | 1 | 0 | 0 | 0 | 1 |
| CC: Hidden plots by secret schemes of powerful groups | 2 | 1 | 0 | 0 | 0 | 3 |
| CC: Questioning the measurements and science | 1 | 0 | 0 | 0 | 0 | 1 |
| URW: Amplifying war-related fears | 0 | 5 | 8 | 0 | 1 | 14 |
| URW: Blaming the war on others rather than the invader | 1 | 1 | 3 | 0 | 0 | 5 |
| URW: Discrediting Ukraine | 3 | 4 | 0 | 1 | 12 | 20 |
| URW: Discrediting the West, Diplomacy | 4 | 2 | 3 | 1 | 5 | 15 |
| URW: Distrust towards Media | 0 | 0 | 1 | 0 | 0 | 1 |
| URW: Hidden plots by secret schemes of powerful groups | 0 | 0 | 2 | 0 | 1 | 3 |
| URW: Negative Consequences for the West | 1 | 1 | 0 | 0 | 0 | 2 |
| URW: Overpraising the West | 1 | 0 | 0 | 0 | 0 | 1 |
| URW: Praise of Russia | 0 | 0 | 6 | 2 | 8 | 16 |
| URW: Russia is the Victim | 0 | 2 | 0 | 2 | 0 | 4 |
| URW: Speculating war outcomes | 3 | 0 | 2 | 0 | 1 | 6 |
| **Total** | **30** | **28** | **29** | **25** | **28** | **140** |

## 4a. Top Subnarrative Distribution — Train Set

| Subnarrative | EN | BG | HI | PT | RU | Total |
|-------------|----:|----:|----:|----:|----:|------:|
| CC: Amplifying Climate Fears: Amplifying existing fears of global warming | 0 | 65 | 19 | 17 | 0 | 101 |
| URW: Discrediting Ukraine: Discrediting Ukrainian government and officials an... | 4 | 24 | 4 | 19 | 18 | 69 |
| URW: Amplifying war-related fears: There is a real possibility that nuclear w... | 9 | 7 | 28 | 6 | 2 | 52 |
| URW: Praise of Russia: Praise of Russian military might | 2 | 10 | 7 | 11 | 19 | 49 |
| URW: Discrediting Ukraine: Discrediting Ukrainian military | 2 | 8 | 3 | 7 | 15 | 35 |
| URW: Blaming the war on others rather than the invader: The West are the aggr... | 8 | 15 | 3 | 2 | 6 | 34 |
| URW: Praise of Russia: Russia has international support from a number of coun... | 2 | 7 | 15 | 2 | 4 | 30 |
| URW: Discrediting the West, Diplomacy: The West does not care about Ukraine, ... | 3 | 15 | 1 | 3 | 5 | 27 |
| URW: Blaming the war on others rather than the invader: Ukraine is the aggressor | 2 | 7 | 6 | 7 | 4 | 26 |
| URW: Amplifying war-related fears: By continuing the war we risk WWIII | 2 | 15 | 5 | 2 | 1 | 25 |
| URW: Discrediting Ukraine: Ukraine is a puppet of the West | 2 | 11 | 0 | 3 | 8 | 24 |
| URW: Discrediting Ukraine: Situation in Ukraine is hopeless | 2 | 12 | 5 | 2 | 1 | 22 |
| URW: Distrust towards Media: Western media is an instrument of propaganda | 6 | 2 | 10 | 0 | 2 | 20 |
| URW: Praise of Russia: Russia is a guarantor of peace and prosperity | 0 | 2 | 3 | 3 | 10 | 18 |
| URW: Russia is the Victim: The West is russophobic | 1 | 4 | 4 | 2 | 6 | 17 |
| URW: Amplifying war-related fears: Russia will also attack other countries | 1 | 15 | 0 | 1 | 0 | 17 |
| CC: Criticism of institutions and authorities: Criticism of national governments | 6 | 3 | 0 | 7 | 0 | 16 |
| CC: Criticism of institutions and authorities: Criticism of political organiz... | 10 | 0 | 1 | 5 | 0 | 16 |
| URW: Discrediting the West, Diplomacy: The West is weak | 4 | 9 | 0 | 0 | 2 | 15 |
| URW: Discrediting Ukraine: Ukraine is a hub for criminal activities | 2 | 3 | 1 | 8 | 0 | 14 |
| CC: Criticism of climate policies: Climate policies have negative impact on t... | 4 | 9 | 0 | 0 | 0 | 13 |
| URW: Speculating war outcomes: Russian army is collapsing | 3 | 6 | 3 | 0 | 0 | 12 |
| URW: Discrediting the West, Diplomacy: Diplomacy does/will not work | 4 | 3 | 3 | 2 | 0 | 12 |
| URW: Speculating war outcomes: Ukrainian army is collapsing | 1 | 5 | 3 | 1 | 1 | 11 |
| URW: Praise of Russia: Praise of Russian President Vladimir Putin | 0 | 6 | 5 | 0 | 0 | 11 |

## 4b. Top Subnarrative Distribution — Dev Set

| Subnarrative | EN | BG | HI | PT | RU | Total |
|-------------|----:|----:|----:|----:|----:|------:|
| CC: Amplifying Climate Fears: Amplifying existing fears of global warming | 0 | 5 | 4 | 9 | 0 | 18 |
| URW: Discrediting Ukraine: Discrediting Ukrainian government and officials an... | 2 | 1 | 0 | 1 | 3 | 7 |
| URW: Praise of Russia: Russia has international support from a number of coun... | 0 | 0 | 3 | 1 | 3 | 7 |
| URW: Discrediting Ukraine: Ukraine is a puppet of the West | 0 | 2 | 0 | 0 | 2 | 4 |
| URW: Praise of Russia: Russia is a guarantor of peace and prosperity | 0 | 0 | 1 | 1 | 2 | 4 |
| URW: Discrediting the West, Diplomacy: The West does not care about Ukraine, ... | 1 | 0 | 1 | 0 | 1 | 3 |
| CC: Criticism of institutions and authorities: Criticism of political organiz... | 2 | 0 | 0 | 1 | 0 | 3 |
| URW: Amplifying war-related fears: By continuing the war we risk WWIII | 0 | 1 | 2 | 0 | 0 | 3 |
| URW: Russia is the Victim: The West is russophobic | 0 | 2 | 0 | 1 | 0 | 3 |
| URW: Praise of Russia: Praise of Russian military might | 0 | 0 | 1 | 0 | 2 | 3 |
| URW: Discrediting Ukraine: Discrediting Ukrainian military | 0 | 0 | 0 | 0 | 3 | 3 |
| URW: Speculating war outcomes: Russian army is collapsing | 2 | 0 | 0 | 0 | 0 | 2 |
| CC: Criticism of institutions and authorities: Criticism of international ent... | 1 | 0 | 0 | 1 | 0 | 2 |
| CC: Criticism of climate movement: Climate movement is alarmist | 2 | 0 | 0 | 0 | 0 | 2 |
| URW: Blaming the war on others rather than the invader: The West are the aggr... | 1 | 0 | 1 | 0 | 0 | 2 |
| CC: Hidden plots by secret schemes of powerful groups: Blaming global elites | 1 | 1 | 0 | 0 | 0 | 2 |
| URW: Speculating war outcomes: Ukrainian army is collapsing | 1 | 0 | 0 | 0 | 1 | 2 |
| URW: Amplifying war-related fears: Russia will also attack other countries | 0 | 1 | 1 | 0 | 0 | 2 |
| CC: Downplaying climate change: Weather suggests the trend is global cooling | 0 | 2 | 0 | 0 | 0 | 2 |
| URW: Blaming the war on others rather than the invader: Ukraine is the aggressor | 0 | 1 | 1 | 0 | 0 | 2 |
| URW: Amplifying war-related fears: There is a real possibility that nuclear w... | 0 | 1 | 1 | 0 | 0 | 2 |
| URW: Discrediting Ukraine: Ukraine is associated with nazism | 0 | 1 | 0 | 0 | 1 | 2 |
| URW: Amplifying war-related fears: NATO should/will directly intervene | 0 | 0 | 1 | 0 | 1 | 2 |
| URW: Discrediting Ukraine: Ukraine is a hub for criminal activities | 0 | 0 | 0 | 0 | 2 | 2 |
| URW: Overpraising the West: The West belongs in the right side of history | 1 | 0 | 0 | 0 | 0 | 1 |

## 5. Label Density Distribution

Number of distinct narratives assigned per article.

### Train Set

| # Narratives | EN | BG | HI | PT | RU | Total |
|-------------|-----:|-----:|-----:|-----:|-----:|------:|
| 0 | 196 | 44 | 173 | 148 | 0 | 561 |
| 1 | 203 | 357 | 193 | 252 | 133 | 1138 |

### Dev Set

| # Narratives | EN | BG | HI | PT | RU | Total |
|-------------|-----:|-----:|-----:|-----:|-----:|------:|
| 0 | 11 | 7 | 6 | 10 | 4 | 38 |
| 1 | 30 | 28 | 29 | 25 | 28 | 140 |

## 6. Summary

- **Train set**: 1699 articles across 5 languages
  - 21 unique narratives, 64 unique subnarratives
- **Dev set**: 178 articles across 5 languages
  - 21 unique narratives, 43 unique subnarratives
- **Test set**: 460 articles (no annotations)

**Subnarratives in dev but NOT in train (3):**
- CC: Climate change is beneficial: CO2 is beneficial
- CC: Green policies are geopolitical instruments: Green activities are a form of neo-colonialism
- URW: Speculating war outcomes: Russian army will lose all the occupied territories

**Subnarratives in train but NOT in dev (24):**
- CC: Amplifying Climate Fears: Earth will be uninhabitable soon
- CC: Amplifying Climate Fears: Whatever we do it is already too late
- CC: Climate change is beneficial: Temperature increase is beneficial
- CC: Controversy about green technologies: Renewable energy is unreliable
- CC: Criticism of climate movement: Climate movement is corrupt
- CC: Criticism of climate policies: Climate policies are ineffective
- CC: Downplaying climate change: CO2 concentrations are too small to have an impact
- CC: Downplaying climate change: Climate cycles are natural
- CC: Downplaying climate change: Human activities do not impact climate change
- CC: Downplaying climate change: Ice is not melting
- CC: Downplaying climate change: Temperature increase does not have significant impact
- CC: Green policies are geopolitical instruments: Climate-related international relations are abusive/exploitative
- CC: Questioning the measurements and science: Greenhouse effect/carbon dioxide do not drive climate change
- CC: Questioning the measurements and science: Methodologies/metrics used are unreliable/faulty
- CC: Questioning the measurements and science: Scientific community is unreliable
- URW: Discrediting Ukraine: Discrediting Ukrainian nation and society
- URW: Discrediting Ukraine: Rewriting Ukraine’s history
- URW: Discrediting the West, Diplomacy: Diplomacy does/will not work
- URW: Negative Consequences for the West: The conflict will increase the Ukrainian refugee flows to Europe
- URW: Overpraising the West: NATO will destroy Russia
- URW: Overpraising the West: The West has the strongest international support
- URW: Praise of Russia: Praise of Russian President Vladimir Putin
- URW: Russia is the Victim: Russia actions in Ukraine are only self-defence
- URW: Russia is the Victim: UA is anti-RU extremists

## 7. Augmented Training Set (mDeBERTa Baseline)

The mDeBERTa baseline was fine-tuned on an augmented version of the training set
that includes both original documents and their LLM-generated translations.

### 7a. Composition Overview

| Component | Count |
|-----------|------:|
| Original documents (native language) | 2098 |
| Translated documents (non-EN -> EN) | 1300 |
| EN->PT back-translation | 168 |
| **Total (used for training)** | **3566** |

**Translation method**: Google Gemini LLM — text cleaning (boilerplate removal)
followed by translation to English. English documents were cleaned but not translated,
resulting in two copies per EN document (raw original + cleaned version).

### 7b. Language x Type Breakdown

| Language | Original | Translated | Total |
|----------|------:|------:|------:|
| EN | 798 | 0 | 798 |
| BG | 401 | 401 | 802 |
| HI | 366 | 366 | 732 |
| PT | 400 | 400 | 800 |
| RU | 133 | 133 | 266 |
| **Total** | **2098** | **1300** | **3398** |

### 7c. File Type Description

| Filename Pattern | Description |
|-----------------|-------------|
| `{LANG}_ORIG_{filename}` | Raw web-scraped text in original language |
| `{filename}` (no prefix, non-EN origin) | Non-EN document translated to English by Gemini |
| `EN_{filename}` (no ORIG prefix) | English document after LLM boilerplate cleaning |
| `EN_TRANS_PT_{filename}` | English document back-translated to Portuguese |

**Note**: English documents appear twice under different filenames —
the raw original (`EN_ORIG_*`) and the LLM-cleaned version (`EN_*`). These
are not identical: the cleaned versions have web boilerplate removed, resulting
in EN being effectively double-represented (798 files vs 401 BG, 366 HI, etc.).

### 7d. Augmented Set Label Statistics

| Metric | Value |
|--------|------:|
| Total documents (CSV) | 3398 |
| Total documents (TSV, incl. back-translations) | 3566 |
| Unique narratives | 21 |
| Unique subnarratives | 94 |
| Documents labeled 'Other' | 648 (19.1%) |

### 7e. Data Leakage Verification

**No data leakage detected.** Zero overlap between the augmented training set
and the dev evaluation set (178 documents). Verified by exact filename match,
original filename match, and numeric ID cross-check.

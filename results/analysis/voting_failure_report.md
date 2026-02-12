# Voting Failure Analysis Report

Generated: 2026-02-12 00:50:20

## 1. Executive Summary

- **Experiments analyzed**: 48
- **Models**: DeepSeek V3, GPT-5 Nano, Gemini 2.5 Flash, Llama 3.3 70B, Mistral Large
- **Languages**: BG, EN, HI, PT, RU
- **Aggregation methods**: intersection, majority, union
- **Total systematic narrative failures** (wrong in all runs): 1195

## 2. 'Other' Inflation by Aggregation Method

Documents reduced to 'Other' (empty prediction) when ground truth is not Other.

| Experiment | Aggregation | Model | Lang | Narrative Other % | Subnarrative Other % |
|---|---|---|---|---|---|
| agora_1_deepseek_en_t00 | intersection | DeepSeek V3 | EN | 6.0% | 6.0% |
| agora_5_deepseek_en_t00 | intersection | DeepSeek V3 | EN | 8.9% | 8.9% |
| agora_deepseek_bg_t00 | intersection | DeepSeek V3 | BG | 7.1% | 7.1% |
| agora_deepseek_bg_t07 | intersection | DeepSeek V3 | BG | 7.1% | 7.1% |
| agora_deepseek_en_t00 | intersection | DeepSeek V3 | EN | 7.4% | 7.4% |
| agora_deepseek_en_t07 | intersection | DeepSeek V3 | EN | 8.0% | 8.0% |
| agora_deepseek_hi_t00 | intersection | DeepSeek V3 | HI | 15.9% | 15.9% |
| agora_deepseek_pt_t00 | intersection | DeepSeek V3 | PT | 32.0% | 32.0% |
| agora_deepseek_ru_t00 | intersection | DeepSeek V3 | RU | 2.9% | 2.9% |
| agora_deepseek_ru_t07 | intersection | DeepSeek V3 | RU | 3.6% | 3.6% |
| agora_gemini_en_t00 | intersection | Gemini 2.5 Flash | EN | 6.7% | 6.7% |
| agora_gemini_en_t07 | intersection | Gemini 2.5 Flash | EN | 4.7% | 4.7% |
| agora_mistral_bg_t00 | intersection | Mistral Large | BG | 8.7% | 8.7% |
| agora_mistral_en_t00 | intersection | Mistral Large | EN | 8.7% | 8.7% |
| agora_mistral_en_t00_evidence | intersection | Mistral Large | EN | 6.7% | 6.7% |
| agora_mistral_en_t07 | intersection | Mistral Large | EN | 8.1% | 8.1% |
| agora_mistral_hi_t00 | intersection | Mistral Large | HI | 8.5% | 8.5% |
| agora_mistral_pt_t00 | intersection | Mistral Large | PT | 16.4% | 16.4% |
| agora_mistral_ru_t00 | intersection | Mistral Large | RU | 6.2% | 6.2% |
| agora_together_llama33_70b_en_t00 | intersection | Llama 3.3 70B | EN | 6.7% | 6.7% |
| agora_together_llama33_70b_en_t07 | intersection | Llama 3.3 70B | EN | 16.0% | 16.0% |
| agora_majority_deepseek_pt_t00 | majority | DeepSeek V3 | PT | 22.4% | 22.4% |
| agora_majority_gpt5nano_bg_t00 | majority | GPT-5 Nano | BG | 0.8% | 1.5% |
| agora_majority_gpt5nano_en_t07 | majority | GPT-5 Nano | EN | 0.0% | 0.7% |
| agora_majority_gpt5nano_hi_t00 | majority | GPT-5 Nano | HI | 24.8% | 26.9% |
| agora_majority_gpt5nano_pt_t00 | majority | GPT-5 Nano | PT | 16.0% | 20.0% |
| agora_majority_gpt5nano_ru_t00 | majority | GPT-5 Nano | RU | 5.0% | 10.7% |
| agora_majority_mistral_bg_t00 | majority | Mistral Large | BG | 3.6% | 3.6% |
| agora_majority_mistral_en_t00 | majority | Mistral Large | EN | 6.0% | 6.0% |
| agora_majority_mistral_en_t00_evidence | majority | Mistral Large | EN | 3.3% | 3.3% |
| agora_majority_mistral_en_t07 | majority | Mistral Large | EN | 4.0% | 4.0% |
| agora_majority_mistral_hi_t00 | majority | Mistral Large | HI | 4.8% | 4.8% |
| agora_majority_mistral_pt_t00 | majority | Mistral Large | PT | 13.6% | 13.6% |
| agora_majority_mistral_ru_t00 | majority | Mistral Large | RU | 0.7% | 0.7% |
| agora_majority_together_llama33_70b_bg_t00 | majority | Llama 3.3 70B | BG | 25.7% | 25.7% |
| agora_majority_together_llama33_70b_en_t00 | majority | Llama 3.3 70B | EN | 4.0% | 4.0% |
| agora_majority_together_llama33_70b_en_t07 | majority | Llama 3.3 70B | EN | 4.0% | 4.0% |
| agora_majority_together_llama33_70b_hi_t00 | majority | Llama 3.3 70B | HI | 28.3% | 28.3% |
| agora_majority_together_llama33_70b_pt_t00 | majority | Llama 3.3 70B | PT | 56.0% | 56.0% |
| agora_majority_together_llama33_70b_ru_t00 | majority | Llama 3.3 70B | RU | 9.3% | 9.3% |
| agora_union_deepseek_pt_t00 | union | DeepSeek V3 | PT | 21.6% | 21.6% |
| agora_union_gpt5nano_en_t00 | union | GPT-5 Nano | EN | 0.0% | 0.0% |
| agora_union_gpt5nano_en_t07 | union | GPT-5 Nano | EN | 0.0% | 0.0% |
| agora_union_mistral_en_t00 | union | Mistral Large | EN | 2.7% | 2.7% |
| agora_union_mistral_en_t07 | union | Mistral Large | EN | 5.3% | 5.3% |
| agora_union_together_llama33_70b_en_t00 | union | Llama 3.3 70B | EN | 4.0% | 4.0% |
| agora_union_together_llama33_70b_en_t07 | union | Llama 3.3 70B | EN | 2.0% | 2.0% |

### Summary by Aggregation Method

| Method | Mean Other % | Min | Max | N |
|---|---|---|---|---|
| intersection | 9.3% | 2.9% | 32.0% | 21 |
| majority | 12.2% | 0.0% | 56.0% | 19 |
| union | 5.1% | 0.0% | 21.6% | 7 |

## 3. Systematic Failures (Wrong in All Runs)

Documents misclassified at the narrative level in every single run of an experiment.

### Intersection

| Experiment | Model | Lang | Systematic Failures | Stochastic | Correct | Total |
|---|---|---|---|---|---|---|
| agora_1_deepseek_en_t00 | DeepSeek V3 | EN | **30** | 0 | 0 | 30 |
| agora_5_deepseek_en_t00 | DeepSeek V3 | EN | **30** | 0 | 0 | 30 |
| agora_deepseek_bg_t00 | DeepSeek V3 | BG | **18** | 0 | 10 | 28 |
| agora_deepseek_bg_t07 | DeepSeek V3 | BG | **18** | 1 | 9 | 28 |
| agora_deepseek_en_t00 | DeepSeek V3 | EN | **30** | 0 | 0 | 30 |
| agora_deepseek_en_t07 | DeepSeek V3 | EN | **29** | 1 | 0 | 30 |
| agora_deepseek_hi_t00 | DeepSeek V3 | HI | **23** | 2 | 4 | 29 |
| agora_deepseek_pt_t00 | DeepSeek V3 | PT | **18** | 3 | 4 | 25 |
| agora_deepseek_ru_t00 | DeepSeek V3 | RU | **25** | 0 | 3 | 28 |
| agora_deepseek_ru_t07 | DeepSeek V3 | RU | **24** | 1 | 3 | 28 |
| agora_gemini_en_t00 | Gemini 2.5 Flash | EN | **27** | 0 | 3 | 30 |
| agora_gemini_en_t07 | Gemini 2.5 Flash | EN | **27** | 2 | 1 | 30 |
| agora_mistral_bg_t00 | Mistral Large | BG | **21** | 3 | 4 | 28 |
| agora_mistral_en_t00 | Mistral Large | EN | **28** | 2 | 0 | 30 |
| agora_mistral_en_t00_evidence | Mistral Large | EN | **29** | 0 | 1 | 30 |
| agora_mistral_en_t07 | Mistral Large | EN | **29** | 1 | 0 | 30 |
| agora_mistral_hi_t00 | Mistral Large | HI | **25** | 2 | 2 | 29 |
| agora_mistral_pt_t00 | Mistral Large | PT | **18** | 3 | 4 | 25 |
| agora_mistral_ru_t00 | Mistral Large | RU | **25** | 2 | 0 | 27 |
| agora_together_llama33_70b_en_t00 | Llama 3.3 70B | EN | **30** | 0 | 0 | 30 |
| agora_together_llama33_70b_en_t07 | Llama 3.3 70B | EN | **29** | 1 | 0 | 30 |

### Majority

| Experiment | Model | Lang | Systematic Failures | Stochastic | Correct | Total |
|---|---|---|---|---|---|---|
| agora_majority_deepseek_pt_t00 | DeepSeek V3 | PT | **15** | 4 | 6 | 25 |
| agora_majority_gpt5nano_bg_t00 | GPT-5 Nano | BG | **21** | 3 | 4 | 28 |
| agora_majority_gpt5nano_en_t07 | GPT-5 Nano | EN | **29** | 0 | 1 | 30 |
| agora_majority_gpt5nano_hi_t00 | GPT-5 Nano | HI | **21** | 6 | 2 | 29 |
| agora_majority_gpt5nano_pt_t00 | GPT-5 Nano | PT | **14** | 5 | 6 | 25 |
| agora_majority_gpt5nano_ru_t00 | GPT-5 Nano | RU | **23** | 2 | 3 | 28 |
| agora_majority_mistral_bg_t00 | Mistral Large | BG | **21** | 3 | 4 | 28 |
| agora_majority_mistral_en_t00 | Mistral Large | EN | **29** | 1 | 0 | 30 |
| agora_majority_mistral_en_t00_evidence | Mistral Large | EN | **30** | 0 | 0 | 30 |
| agora_majority_mistral_en_t07 | Mistral Large | EN | **29** | 1 | 0 | 30 |
| agora_majority_mistral_hi_t00 | Mistral Large | HI | **26** | 2 | 1 | 29 |
| agora_majority_mistral_pt_t00 | Mistral Large | PT | **19** | 6 | 0 | 25 |
| agora_majority_mistral_ru_t00 | Mistral Large | RU | **27** | 0 | 1 | 28 |
| agora_majority_together_llama33_70b_bg_t00 | Llama 3.3 70B | BG | **25** | 2 | 1 | 28 |
| agora_majority_together_llama33_70b_en_t00 | Llama 3.3 70B | EN | **30** | 0 | 0 | 30 |
| agora_majority_together_llama33_70b_en_t07 | Llama 3.3 70B | EN | **30** | 0 | 0 | 30 |
| agora_majority_together_llama33_70b_hi_t00 | Llama 3.3 70B | HI | **29** | 0 | 0 | 29 |
| agora_majority_together_llama33_70b_pt_t00 | Llama 3.3 70B | PT | **24** | 0 | 1 | 25 |
| agora_majority_together_llama33_70b_ru_t00 | Llama 3.3 70B | RU | **27** | 0 | 1 | 28 |

### Union

| Experiment | Model | Lang | Systematic Failures | Stochastic | Correct | Total |
|---|---|---|---|---|---|---|
| agora_union_deepseek_pt_t00 | DeepSeek V3 | PT | **15** | 3 | 7 | 25 |
| agora_union_gpt5nano_en_t00 | GPT-5 Nano | EN | **29** | 1 | 0 | 30 |
| agora_union_gpt5nano_en_t07 | GPT-5 Nano | EN | **29** | 0 | 1 | 30 |
| agora_union_mistral_en_t00 | Mistral Large | EN | **30** | 0 | 0 | 30 |
| agora_union_mistral_en_t07 | Mistral Large | EN | **30** | 0 | 0 | 30 |
| agora_union_together_llama33_70b_en_t00 | Llama 3.3 70B | EN | **30** | 0 | 0 | 30 |
| agora_union_together_llama33_70b_en_t07 | Llama 3.3 70B | EN | **30** | 0 | 0 | 30 |

### Detailed Systematic Failure Documents

**agora_1_deepseek_en_t00** (DeepSeek V3, intersection):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Green policies are geopolitical instruments; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200064.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement`
  - ... and 20 more

**agora_5_deepseek_en_t00** (DeepSeek V3, intersection):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Green policies are geopolitical instruments`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of climate policies`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200064.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement`
  - ... and 20 more

**agora_deepseek_bg_t00** (DeepSeek V3, intersection):
  - `A9_BG_2569.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim`
  - `A9_BG_2663.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader`
  - `A9_BG_2707.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Negative Consequences for the West; URW: Speculating war outcomes`
  - `A9_BG_2756.txt`: GT=`URW: Blaming the war on others rather than the invader` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy`
  - `A9_BG_2828.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy`
  - `A9_BG_3819.txt`: GT=`URW: Amplifying war-related fears` | Pred=`Other`
  - `A9_BG_3964.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West`
  - `A9_BG_3970.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy`
  - `A9_BG_4026.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader`
  - `A9_BG_4039.txt`: GT=`URW: Negative Consequences for the West` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader`
  - ... and 8 more

**agora_deepseek_bg_t07** (DeepSeek V3, intersection):
  - `A9_BG_2569.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim`
  - `A9_BG_2663.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader`
  - `A9_BG_2707.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Negative Consequences for the West; URW: Speculating war outcomes`
  - `A9_BG_2756.txt`: GT=`URW: Blaming the war on others rather than the invader` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Distrust towards Media`
  - `A9_BG_2828.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy`
  - `A9_BG_3819.txt`: GT=`URW: Amplifying war-related fears` | Pred=`Other`
  - `A9_BG_3964.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy`
  - `A9_BG_3970.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy`
  - `A9_BG_4026.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader`
  - `A9_BG_4039.txt`: GT=`URW: Negative Consequences for the West` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader`
  - ... and 8 more

**agora_deepseek_en_t00** (DeepSeek V3, intersection):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Green policies are geopolitical instruments; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Green policies are geopolitical instruments`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of climate policies`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200064.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement`
  - ... and 20 more

**agora_deepseek_en_t07** (DeepSeek V3, intersection):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Green policies are geopolitical instruments; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of climate policies`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200064.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement`
  - ... and 19 more

**agora_deepseek_hi_t00** (DeepSeek V3, intersection):
  - `HI_107.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy`
  - `HI_110.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim`
  - `HI_114.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy`
  - `HI_125.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy`
  - `HI_126.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Praise of Russia`
  - `HI_139.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `HI_151.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West; URW: Russia is the Victim`
  - `HI_152.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Praise of Russia`
  - `HI_154.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West; URW: Speculating war outcomes`
  - `HI_158.txt`: GT=`URW: Blaming the war on others rather than the invader` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Russia is the Victim`
  - ... and 13 more

**agora_deepseek_pt_t00** (DeepSeek V3, intersection):
  - `PT_206.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_207.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `PT_208.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_213.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities`
  - `PT_216.txt`: GT=`CC: Criticism of climate policies` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `PT_217.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_224.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `PT_225.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `PT_229.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_230.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - ... and 8 more

**agora_deepseek_ru_t00** (DeepSeek V3, intersection):
  - `RU-URW-1004.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine`
  - `RU-URW-1014.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Discrediting Ukraine; URW: Praise of Russia`
  - `RU-URW-1023.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine`
  - `RU-URW-1032.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Discrediting Ukraine`
  - `RU-URW-1043.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Discrediting Ukraine; URW: Praise of Russia`
  - `RU-URW-1053.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Negative Consequences for the West; URW: Praise of Russia`
  - `RU-URW-1061.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy`
  - `RU-URW-1069.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Discrediting Ukraine; URW: Praise of Russia`
  - `RU-URW-1073.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy`
  - `RU-URW-1077.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy`
  - ... and 15 more

**agora_deepseek_ru_t07** (DeepSeek V3, intersection):
  - `RU-URW-1004.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine`
  - `RU-URW-1014.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Discrediting Ukraine; URW: Praise of Russia`
  - `RU-URW-1023.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine`
  - `RU-URW-1032.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Discrediting Ukraine`
  - `RU-URW-1043.txt`: GT=`URW: Praise of Russia` | Pred=`Other`
  - `RU-URW-1053.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Negative Consequences for the West; URW: Praise of Russia`
  - `RU-URW-1061.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy`
  - `RU-URW-1073.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy`
  - `RU-URW-1077.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy`
  - `RU-URW-1101.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Speculating war outcomes`
  - ... and 14 more

**agora_gemini_en_t00** (Gemini 2.5 Flash, intersection):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`Other`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`Other`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Hidden plots by secret schemes of powerful groups; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200064.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement`
  - ... and 17 more

**agora_gemini_en_t07** (Gemini 2.5 Flash, intersection):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Downplaying climate change`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200064.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement`
  - ... and 17 more

**agora_majority_deepseek_pt_t00** (DeepSeek V3, majority):
  - `PT_206.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_207.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `PT_208.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_213.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities`
  - `PT_216.txt`: GT=`CC: Criticism of climate policies` | Pred=`CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `PT_217.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_221.txt`: GT=`CC: Criticism of climate policies` | Pred=`CC: Criticism of climate policies; CC: Green policies are geopolitical instruments`
  - `PT_224.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `PT_225.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `PT_244.txt`: GT=`URW: Russia is the Victim` | Pred=`URW: Discrediting the West, Diplomacy; URW: Russia is the Victim`
  - ... and 5 more

**agora_majority_gpt5nano_bg_t00** (GPT-5 Nano, majority):
  - `A9_BG_2569.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim`
  - `A9_BG_2592.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Amplifying war-related fears; URW: Discrediting Ukraine; URW: Hidden plots by secret schemes of powerful groups`
  - `A9_BG_2663.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Speculating war outcomes`
  - `A9_BG_2707.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Negative Consequences for the West; URW: Praise of Russia; URW: Speculating war outcomes`
  - `A9_BG_2756.txt`: GT=`URW: Blaming the war on others rather than the invader` | Pred=`URW: Discrediting Ukraine; URW: Hidden plots by secret schemes of powerful groups`
  - `A9_BG_2828.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Speculating war outcomes`
  - `A9_BG_3819.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Discrediting the West, Diplomacy; URW: Speculating war outcomes`
  - `A9_BG_3964.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West`
  - `A9_BG_3970.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Distrust towards Media; URW: Speculating war outcomes`
  - `A9_BG_4026.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Speculating war outcomes`
  - ... and 11 more

**agora_majority_gpt5nano_en_t07** (GPT-5 Nano, majority):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Amplifying Climate Fears; CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of climate policies`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200064.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears`
  - ... and 19 more

**agora_majority_gpt5nano_hi_t00** (GPT-5 Nano, majority):
  - `HI_107.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Speculating war outcomes`
  - `HI_110.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Discrediting Ukraine; URW: Speculating war outcomes`
  - `HI_114.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Speculating war outcomes`
  - `HI_125.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West`
  - `HI_126.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Discrediting the West, Diplomacy; URW: Praise of Russia`
  - `HI_139.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`CC: Questioning the measurements and science`
  - `HI_152.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Blaming the war on others rather than the invader`
  - `HI_154.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West; URW: Russia is the Victim; URW: Speculating war outcomes`
  - `HI_156.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Speculating war outcomes`
  - `HI_158.txt`: GT=`URW: Blaming the war on others rather than the invader` | Pred=`URW: Blaming the war on others rather than the invader; URW: Speculating war outcomes`
  - ... and 11 more

**agora_majority_gpt5nano_pt_t00** (GPT-5 Nano, majority):
  - `PT_205.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_207.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `PT_208.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of institutions and authorities`
  - `PT_213.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Criticism of institutions and authorities`
  - `PT_216.txt`: GT=`CC: Criticism of climate policies` | Pred=`CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `PT_217.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_224.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `PT_225.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `PT_229.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_244.txt`: GT=`URW: Russia is the Victim` | Pred=`URW: Discrediting the West, Diplomacy; URW: Russia is the Victim`
  - ... and 4 more

**agora_majority_gpt5nano_ru_t00** (GPT-5 Nano, majority):
  - `RU-URW-1004.txt`: GT=`URW: Discrediting Ukraine` | Pred=`Other`
  - `RU-URW-1014.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Discrediting Ukraine; URW: Praise of Russia`
  - `RU-URW-1023.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Speculating war outcomes`
  - `RU-URW-1032.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Discrediting Ukraine; URW: Speculating war outcomes`
  - `RU-URW-1043.txt`: GT=`URW: Praise of Russia` | Pred=`Other`
  - `RU-URW-1053.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West; URW: Russia is the Victim`
  - `RU-URW-1061.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim`
  - `RU-URW-1077.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Discrediting the West, Diplomacy`
  - `RU-URW-1085.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Praise of Russia; URW: Speculating war outcomes`
  - `RU-URW-1101.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Amplifying war-related fears; URW: Discrediting Ukraine; URW: Speculating war outcomes`
  - ... and 13 more

**agora_majority_mistral_bg_t00** (Mistral Large, majority):
  - `A9_BG_2569.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Distrust towards Media; URW: Russia is the Victim`
  - `A9_BG_2592.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Distrust towards Media`
  - `A9_BG_2663.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim`
  - `A9_BG_2707.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West; URW: Praise of Russia; URW: Speculating war outcomes`
  - `A9_BG_2756.txt`: GT=`URW: Blaming the war on others rather than the invader` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Distrust towards Media`
  - `A9_BG_2828.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Praise of Russia`
  - `A9_BG_3819.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Speculating war outcomes`
  - `A9_BG_3964.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim`
  - `A9_BG_3970.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim; URW: Speculating war outcomes`
  - `A9_BG_4026.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Speculating war outcomes`
  - ... and 11 more

**agora_majority_mistral_en_t00** (Mistral Large, majority):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200065.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - ... and 19 more

**agora_majority_mistral_en_t00_evidence** (Mistral Large, majority):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of institutions and authorities; URW: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Green policies are geopolitical instruments; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; URW: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200064.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement`
  - ... and 20 more

**agora_majority_mistral_en_t07** (Mistral Large, majority):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Green policies are geopolitical instruments; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200065.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - ... and 19 more

**agora_majority_mistral_hi_t00** (Mistral Large, majority):
  - `HI_107.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim; URW: Speculating war outcomes`
  - `HI_110.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim; URW: Speculating war outcomes`
  - `HI_114.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Distrust towards Media; URW: Negative Consequences for the West; URW: Russia is the Victim`
  - `HI_125.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West; URW: Praise of Russia`
  - `HI_126.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Distrust towards Media; URW: Negative Consequences for the West; URW: Russia is the Victim`
  - `HI_139.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `HI_151.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Distrust towards Media; URW: Praise of Russia; URW: Russia is the Victim`
  - `HI_152.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West`
  - `HI_154.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West; URW: Speculating war outcomes`
  - `HI_156.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Distrust towards Media; URW: Russia is the Victim`
  - ... and 16 more

**agora_majority_mistral_pt_t00** (Mistral Large, majority):
  - `PT_206.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_207.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `PT_208.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_213.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `PT_216.txt`: GT=`CC: Criticism of climate policies` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `PT_220.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `PT_221.txt`: GT=`CC: Criticism of climate policies` | Pred=`CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `PT_224.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Green policies are geopolitical instruments`
  - `PT_225.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `PT_228.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of institutions and authorities`
  - ... and 9 more

**agora_majority_mistral_ru_t00** (Mistral Large, majority):
  - `RU-URW-1004.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Praise of Russia`
  - `RU-URW-1014.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Discrediting Ukraine; URW: Praise of Russia; URW: Speculating war outcomes`
  - `RU-URW-1023.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy`
  - `RU-URW-1032.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy`
  - `RU-URW-1043.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Praise of Russia`
  - `RU-URW-1053.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West; URW: Praise of Russia`
  - `RU-URW-1061.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West; URW: Russia is the Victim`
  - `RU-URW-1069.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Praise of Russia`
  - `RU-URW-1073.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Distrust towards Media; URW: Overpraising the West`
  - `RU-URW-1077.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Praise of Russia`
  - ... and 17 more

**agora_majority_together_llama33_70b_bg_t00** (Llama 3.3 70B, majority):
  - `A9_BG_2569.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim`
  - `A9_BG_2592.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy`
  - `A9_BG_2663.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim`
  - `A9_BG_2707.txt`: GT=`URW: Amplifying war-related fears` | Pred=`Other`
  - `A9_BG_2756.txt`: GT=`URW: Blaming the war on others rather than the invader` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Distrust towards Media`
  - `A9_BG_2828.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy`
  - `A9_BG_3819.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Speculating war outcomes`
  - `A9_BG_3964.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West`
  - `A9_BG_3970.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Discrediting the West, Diplomacy; URW: Speculating war outcomes`
  - `A9_BG_4026.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Discrediting the West, Diplomacy; URW: Speculating war outcomes`
  - ... and 15 more

**agora_majority_together_llama33_70b_en_t00** (Llama 3.3 70B, majority):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Green policies are geopolitical instruments`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200064.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Downplaying climate change`
  - ... and 20 more

**agora_majority_together_llama33_70b_en_t07** (Llama 3.3 70B, majority):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Green policies are geopolitical instruments`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200064.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Downplaying climate change`
  - ... and 20 more

**agora_majority_together_llama33_70b_hi_t00** (Llama 3.3 70B, majority):
  - `HI_107.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim`
  - `HI_110.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim; URW: Speculating war outcomes`
  - `HI_114.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Discrediting the West, Diplomacy; URW: Speculating war outcomes`
  - `HI_125.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Distrust towards Media; URW: Negative Consequences for the West; URW: Overpraising the West; URW: Praise of Russia; URW: Russia is the Victim; URW: Speculating war outcomes`
  - `HI_126.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West; URW: Praise of Russia; URW: Russia is the Victim`
  - `HI_134.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `HI_139.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `HI_140.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `HI_143.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `HI_151.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim`
  - ... and 19 more

**agora_majority_together_llama33_70b_pt_t00** (Llama 3.3 70B, majority):
  - `PT_205.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_206.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_207.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `PT_208.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_211.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_213.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `PT_216.txt`: GT=`CC: Criticism of climate policies` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `PT_217.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_220.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_221.txt`: GT=`CC: Criticism of climate policies` | Pred=`Other`
  - ... and 14 more

**agora_majority_together_llama33_70b_ru_t00** (Llama 3.3 70B, majority):
  - `RU-URW-1004.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Speculating war outcomes`
  - `RU-URW-1014.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Discrediting Ukraine; URW: Praise of Russia; URW: Speculating war outcomes`
  - `RU-URW-1023.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy`
  - `RU-URW-1032.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Speculating war outcomes`
  - `RU-URW-1043.txt`: GT=`URW: Praise of Russia` | Pred=`Other`
  - `RU-URW-1053.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Praise of Russia; URW: Russia is the Victim`
  - `RU-URW-1061.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West; URW: Russia is the Victim`
  - `RU-URW-1069.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Discrediting Ukraine; URW: Praise of Russia`
  - `RU-URW-1073.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy`
  - `RU-URW-1077.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim`
  - ... and 17 more

**agora_mistral_bg_t00** (Mistral Large, intersection):
  - `A9_BG_2569.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Distrust towards Media; URW: Russia is the Victim`
  - `A9_BG_2592.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Distrust towards Media`
  - `A9_BG_2707.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Negative Consequences for the West; URW: Speculating war outcomes`
  - `A9_BG_2756.txt`: GT=`URW: Blaming the war on others rather than the invader` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Distrust towards Media`
  - `A9_BG_2828.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Praise of Russia`
  - `A9_BG_3819.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy`
  - `A9_BG_3964.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim`
  - `A9_BG_3970.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim; URW: Speculating war outcomes`
  - `A9_BG_4026.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Speculating war outcomes`
  - ... and 11 more

**agora_mistral_en_t00** (Mistral Large, intersection):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200065.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - ... and 18 more

**agora_mistral_en_t00_evidence** (Mistral Large, intersection):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; URW: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Green policies are geopolitical instruments; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; URW: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200065.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - ... and 19 more

**agora_mistral_en_t07** (Mistral Large, intersection):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200065.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - ... and 19 more

**agora_mistral_hi_t00** (Mistral Large, intersection):
  - `HI_107.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim; URW: Speculating war outcomes`
  - `HI_110.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim`
  - `HI_114.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Distrust towards Media`
  - `HI_125.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West`
  - `HI_126.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West`
  - `HI_139.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `HI_151.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Distrust towards Media`
  - `HI_152.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy`
  - `HI_154.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West; URW: Speculating war outcomes`
  - `HI_156.txt`: GT=`URW: Amplifying war-related fears` | Pred=`URW: Amplifying war-related fears; URW: Blaming the war on others rather than the invader; URW: Russia is the Victim`
  - ... and 15 more

**agora_mistral_pt_t00** (Mistral Large, intersection):
  - `PT_206.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_207.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `PT_208.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_213.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `PT_216.txt`: GT=`CC: Criticism of climate policies` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `PT_220.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `PT_221.txt`: GT=`CC: Criticism of climate policies` | Pred=`CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `PT_224.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Green policies are geopolitical instruments`
  - `PT_225.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `PT_229.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`CC: Downplaying climate change`
  - ... and 8 more

**agora_mistral_ru_t00** (Mistral Large, intersection):
  - `RU-URW-1004.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Praise of Russia`
  - `RU-URW-1014.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Discrediting Ukraine; URW: Praise of Russia; URW: Speculating war outcomes`
  - `RU-URW-1023.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy`
  - `RU-URW-1032.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Discrediting Ukraine`
  - `RU-URW-1043.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Discrediting the West, Diplomacy`
  - `RU-URW-1053.txt`: GT=`URW: Discrediting the West, Diplomacy` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West; URW: Praise of Russia`
  - `RU-URW-1061.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine; URW: Discrediting the West, Diplomacy; URW: Negative Consequences for the West; URW: Russia is the Victim`
  - `RU-URW-1069.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Discrediting Ukraine; URW: Praise of Russia`
  - `RU-URW-1077.txt`: GT=`URW: Praise of Russia` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy`
  - `RU-URW-1093.txt`: GT=`URW: Discrediting Ukraine` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting Ukraine`
  - ... and 15 more

**agora_together_llama33_70b_en_t00** (Llama 3.3 70B, intersection):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200064.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change`
  - ... and 20 more

**agora_together_llama33_70b_en_t07** (Llama 3.3 70B, intersection):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200065.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - ... and 19 more

**agora_union_deepseek_pt_t00** (DeepSeek V3, union):
  - `PT_206.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_207.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `PT_208.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_213.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Hidden plots by secret schemes of powerful groups`
  - `PT_216.txt`: GT=`CC: Criticism of climate policies` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `PT_217.txt`: GT=`CC: Amplifying Climate Fears` | Pred=`Other`
  - `PT_221.txt`: GT=`CC: Criticism of climate policies` | Pred=`CC: Criticism of climate policies; CC: Green policies are geopolitical instruments`
  - `PT_224.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `PT_225.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `PT_244.txt`: GT=`URW: Russia is the Victim` | Pred=`URW: Blaming the war on others rather than the invader; URW: Discrediting the West, Diplomacy; URW: Russia is the Victim`
  - ... and 5 more

**agora_union_gpt5nano_en_t00** (GPT-5 Nano, union):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Green policies are geopolitical instruments; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Amplifying Climate Fears; CC: Climate change is beneficial; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200064.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears`
  - ... and 19 more

**agora_union_gpt5nano_en_t07** (GPT-5 Nano, union):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Green policies are geopolitical instruments; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Amplifying Climate Fears; CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of climate policies`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Questioning the measurements and science`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200064.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears`
  - ... and 19 more

**agora_union_mistral_en_t00** (Mistral Large, union):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; URW: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Green policies are geopolitical instruments; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; URW: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200064.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Criticism of institutions and authorities`
  - ... and 20 more

**agora_union_mistral_en_t07** (Mistral Large, union):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; URW: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Green policies are geopolitical instruments; CC: Questioning the measurements and science; URW: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments; URW: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200064.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Criticism of climate movement; CC: Criticism of institutions and authorities`
  - ... and 20 more

**agora_union_together_llama33_70b_en_t00** (Llama 3.3 70B, union):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Green policies are geopolitical instruments; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Green policies are geopolitical instruments`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200064.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - ... and 20 more

**agora_union_together_llama33_70b_en_t07** (Llama 3.3 70B, union):
  - `EN_CC_200033.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Green policies are geopolitical instruments; CC: Hidden plots by secret schemes of powerful groups`
  - `EN_CC_200034.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200035.txt`: GT=`CC: Criticism of institutions and authorities` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Green policies are geopolitical instruments`
  - `EN_CC_200036.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200040.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200046.txt`: GT=`CC: Climate change is beneficial` | Pred=`CC: Climate change is beneficial; CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200047.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities`
  - `EN_CC_200049.txt`: GT=`CC: Questioning the measurements and science` | Pred=`CC: Criticism of climate movement; CC: Criticism of climate policies; CC: Criticism of institutions and authorities; CC: Downplaying climate change; CC: Questioning the measurements and science`
  - `EN_CC_200054.txt`: GT=`CC: Hidden plots by secret schemes of powerful groups` | Pred=`Other`
  - `EN_CC_200064.txt`: GT=`CC: Criticism of climate movement` | Pred=`CC: Amplifying Climate Fears; CC: Controversy about green technologies; CC: Criticism of climate movement; CC: Criticism of institutions and authorities; CC: Downplaying climate change`
  - ... and 20 more

## 4. Cross-Aggregation Comparison

Same model+language+temperature with different aggregation methods. Shows documents where the aggregation method determines correctness.

### DeepSeek V3 — PT (T=0.0)

- Methods compared: intersection, majority, union
- Common documents: 25
- **Correct under union, wrong under intersection**: 5 documents
- **Correct under majority, wrong under intersection**: 4 documents
- **Wrong under ALL methods** (true consensus failure): 15 documents

Example documents salvaged by union over intersection:

- **`PT_205.txt`**
  - Ground truth: `CC: Amplifying Climate Fears`
  - intersection: `Other` (WRONG)
  - majority: `CC: Amplifying Climate Fears` (correct)
  - union: `CC: Amplifying Climate Fears` (correct)
- **`PT_220.txt`**
  - Ground truth: `CC: Amplifying Climate Fears`
  - intersection: `Other` (WRONG)
  - majority: `CC: Amplifying Climate Fears` (correct)
  - union: `CC: Amplifying Climate Fears` (correct)
- **`PT_230.txt`**
  - Ground truth: `CC: Amplifying Climate Fears`
  - intersection: `Other` (WRONG)
  - majority: `CC: Amplifying Climate Fears` (correct)
  - union: `CC: Amplifying Climate Fears` (correct)
- **`PT_232.txt`**
  - Ground truth: `CC: Amplifying Climate Fears`
  - intersection: `Other` (WRONG)
  - majority: `CC: Amplifying Climate Fears` (correct)
  - union: `CC: Amplifying Climate Fears` (correct)
- **`PT_234.txt`**
  - Ground truth: `CC: Amplifying Climate Fears`
  - intersection: `Other` (WRONG)
  - majority: `Other` (WRONG)
  - union: `CC: Amplifying Climate Fears` (correct)

### GPT-5 Nano — EN (T=0.0)

- Methods compared: majority, union
- Common documents: 0
- **Correct under union, wrong under intersection**: 0 documents
- **Correct under majority, wrong under intersection**: 0 documents
- **Wrong under ALL methods** (true consensus failure): 0 documents

### GPT-5 Nano — EN (T=0.7)

- Methods compared: majority, union
- Common documents: 30
- **Correct under union, wrong under intersection**: 0 documents
- **Correct under majority, wrong under intersection**: 0 documents
- **Wrong under ALL methods** (true consensus failure): 29 documents

### Mistral Large — BG (T=0.0)

- Methods compared: intersection, majority
- Common documents: 27
- **Correct under union, wrong under intersection**: 0 documents
- **Correct under majority, wrong under intersection**: 1 documents
- **Wrong under ALL methods** (true consensus failure): 20 documents

### Mistral Large — EN (T=0.0)

- Methods compared: intersection, majority, union
- Common documents: 30
- **Correct under union, wrong under intersection**: 0 documents
- **Correct under majority, wrong under intersection**: 0 documents
- **Wrong under ALL methods** (true consensus failure): 29 documents

### Mistral Large — EN (T=0.7)

- Methods compared: intersection, majority, union
- Common documents: 29
- **Correct under union, wrong under intersection**: 0 documents
- **Correct under majority, wrong under intersection**: 0 documents
- **Wrong under ALL methods** (true consensus failure): 28 documents

### Mistral Large — HI (T=0.0)

- Methods compared: intersection, majority
- Common documents: 29
- **Correct under union, wrong under intersection**: 0 documents
- **Correct under majority, wrong under intersection**: 1 documents
- **Wrong under ALL methods** (true consensus failure): 26 documents

### Mistral Large — PT (T=0.0)

- Methods compared: intersection, majority
- Common documents: 25
- **Correct under union, wrong under intersection**: 0 documents
- **Correct under majority, wrong under intersection**: 0 documents
- **Wrong under ALL methods** (true consensus failure): 19 documents

### Mistral Large — RU (T=0.0)

- Methods compared: intersection, majority
- Common documents: 26
- **Correct under union, wrong under intersection**: 0 documents
- **Correct under majority, wrong under intersection**: 1 documents
- **Wrong under ALL methods** (true consensus failure): 25 documents

### Llama 3.3 70B — EN (T=0.0)

- Methods compared: intersection, majority, union
- Common documents: 30
- **Correct under union, wrong under intersection**: 0 documents
- **Correct under majority, wrong under intersection**: 0 documents
- **Wrong under ALL methods** (true consensus failure): 30 documents

### Llama 3.3 70B — EN (T=0.7)

- Methods compared: intersection, majority, union
- Common documents: 30
- **Correct under union, wrong under intersection**: 0 documents
- **Correct under majority, wrong under intersection**: 0 documents
- **Wrong under ALL methods** (true consensus failure): 30 documents

## 5. Cross-Model Hard Documents

Documents wrong across ALL agora experiments for a given language (inherently ambiguous or hard).

### BG: 18 hard documents (out of 28, across 6 experiments)

- `A9_BG_2569.txt`
- `A9_BG_2663.txt`
- `A9_BG_2707.txt`
- `A9_BG_2756.txt`
- `A9_BG_2828.txt`
- `A9_BG_3819.txt`
- `A9_BG_3964.txt`
- `A9_BG_3970.txt`
- `A9_BG_4026.txt`
- `A9_BG_4039.txt`
- `A9_BG_4076.txt`
- `A9_BG_4093.txt`
- `A9_BG_4110.txt`
- `BG_1169.txt`
- `BG_277.txt`
- `BG_909.txt`
- `BG_950.txt`
- `BG_979.txt`

### EN: 49 hard documents (out of 58, across 24 experiments)

- `EN_CC_200033.txt`
- `EN_CC_200034.txt`
- `EN_CC_200035.txt`
- `EN_CC_200036.txt`
- `EN_CC_200040.txt`
- `EN_CC_200046.txt`
- `EN_CC_200047.txt`
- `EN_CC_200049.txt`
- `EN_CC_200054.txt`
- `EN_CC_200065.txt`
- `EN_CC_200070.txt`
- `EN_CC_200071.txt`
- `EN_CC_200077.txt`
- `EN_CC_200079.txt`
- `EN_CC_200081.txt`
- `EN_UA_DEV_100002.txt`
- `EN_UA_DEV_100005.txt`
- `EN_UA_DEV_100012.txt`
- `EN_UA_DEV_100013.txt`
- `EN_UA_DEV_100026.txt`
- `EN_UA_DEV_100033.txt`
- `EN_UA_DEV_100034.txt`
- `EN_UA_DEV_20.txt`
- `EN_UA_DEV_213.txt`
- `EN_UA_DEV_214.txt`
- `EN_UA_DEV_22.txt`
- `RU-URW-1004.txt`
- `RU-URW-1014.txt`
- `RU-URW-1023.txt`
- `RU-URW-1032.txt`
- `RU-URW-1043.txt`
- `RU-URW-1053.txt`
- `RU-URW-1061.txt`
- `RU-URW-1077.txt`
- `RU-URW-1085.txt`
- `RU-URW-1101.txt`
- `RU-URW-1110.txt`
- `RU-URW-1118.txt`
- `RU-URW-1120.txt`
- `RU-URW-1127.txt`
- `RU-URW-1135.txt`
- `RU-URW-1139.txt`
- `RU-URW-1146.txt`
- `RU-URW-1152.txt`
- `RU-URW-1166.txt`
- `RU-URW-1170.txt`
- `RU-URW-1171.txt`
- `RU-URW-1174.txt`
- `RU-URW-1184.txt`

### HI: 22 hard documents (out of 29, across 5 experiments)

- `HI_107.txt`
- `HI_110.txt`
- `HI_114.txt`
- `HI_125.txt`
- `HI_126.txt`
- `HI_139.txt`
- `HI_151.txt`
- `HI_152.txt`
- `HI_154.txt`
- `HI_158.txt`
- `HI_159.txt`
- `HI_160.txt`
- `HI_19.txt`
- `HI_28.txt`
- `HI_34.txt`
- `HI_35.txt`
- `HI_4.txt`
- `HI_5.txt`
- `HI_71.txt`
- `HI_75.txt`
- `HI_95.txt`
- `HI_97.txt`

### PT: 13 hard documents (out of 25, across 7 experiments)

- `PT_207.txt`
- `PT_208.txt`
- `PT_213.txt`
- `PT_216.txt`
- `PT_224.txt`
- `PT_225.txt`
- `PT_229.txt`
- `PT_244.txt`
- `PT_249.txt`
- `PT_250.txt`
- `PT_253.txt`
- `PT_254.txt`
- `PT_259.txt`

### RU: 22 hard documents (out of 28, across 6 experiments)

- `RU-URW-1004.txt`
- `RU-URW-1014.txt`
- `RU-URW-1023.txt`
- `RU-URW-1032.txt`
- `RU-URW-1043.txt`
- `RU-URW-1053.txt`
- `RU-URW-1061.txt`
- `RU-URW-1077.txt`
- `RU-URW-1101.txt`
- `RU-URW-1110.txt`
- `RU-URW-1118.txt`
- `RU-URW-1120.txt`
- `RU-URW-1127.txt`
- `RU-URW-1135.txt`
- `RU-URW-1139.txt`
- `RU-URW-1146.txt`
- `RU-URW-1152.txt`
- `RU-URW-1166.txt`
- `RU-URW-1170.txt`
- `RU-URW-1171.txt`
- `RU-URW-1174.txt`
- `RU-URW-1184.txt`

## 6. Narrative Confusion Patterns

Most commonly confused narrative pairs across all experiments. Format: (ground_truth, false_positive) -> count.

### Top Narrative Confusions

| Rank | Ground Truth | False Positive | Count |
|---|---|---|---|
| 1 | URW: Discrediting Ukraine | URW: Discrediting the West, Diplomacy | 606 |
| 2 | URW: Discrediting Ukraine | URW: Blaming the war on others rather than the invader | 535 |
| 3 | CC: Criticism of climate movement | CC: Downplaying climate change | 453 |
| 4 | URW: Discrediting the West, Diplomacy | URW: Blaming the war on others rather than the invader | 447 |
| 5 | URW: Discrediting the West, Diplomacy | URW: Negative Consequences for the West | 424 |
| 6 | CC: Criticism of climate movement | CC: Questioning the measurements and science | 398 |
| 7 | CC: Criticism of institutions and authorities | CC: Criticism of climate policies | 376 |
| 8 | CC: Criticism of climate movement | CC: Criticism of institutions and authorities | 322 |
| 9 | URW: Discrediting the West, Diplomacy | URW: Discrediting Ukraine | 304 |
| 10 | URW: Discrediting the West, Diplomacy | URW: Amplifying war-related fears | 296 |
| 11 | URW: Speculating war outcomes | URW: Discrediting the West, Diplomacy | 295 |
| 12 | URW: Speculating war outcomes | URW: Discrediting Ukraine | 280 |
| 13 | URW: Discrediting the West, Diplomacy | URW: Distrust towards Media | 276 |
| 14 | URW: Praise of Russia | URW: Discrediting the West, Diplomacy | 275 |
| 15 | CC: Criticism of climate policies | CC: Criticism of institutions and authorities | 274 |
| 16 | CC: Amplifying Climate Fears | Other | 270 |
| 17 | CC: Criticism of climate movement | CC: Amplifying Climate Fears | 259 |
| 18 | CC: Criticism of climate movement | CC: Criticism of climate policies | 246 |
| 19 | URW: Speculating war outcomes | URW: Amplifying war-related fears | 238 |
| 20 | CC: Criticism of institutions and authorities | CC: Green policies are geopolitical instruments | 234 |

### Top Subnarrative Confusions

| Rank | Ground Truth | False Positive | Count |
|---|---|---|---|
| 1 | CC: Amplifying Climate Fears: Amplifying existing fears of global warming | CC: Amplifying Climate Fears: Doomsday scenarios for humans | 318 |
| 2 | URW: Discrediting Ukraine: Discrediting Ukrainian government and officials and policies | URW: Discrediting the West, Diplomacy: The West does not care about Ukraine, only about its interests | 278 |
| 3 | URW: Discrediting Ukraine: Discrediting Ukrainian government and officials and policies | URW: Discrediting Ukraine: Ukraine is a puppet of the West | 236 |
| 4 | CC: Criticism of institutions and authorities: Criticism of political organizations and figures | CC: Criticism of climate policies: Other | 213 |
| 5 | URW: Discrediting Ukraine: Discrediting Ukrainian government and officials and policies | URW: Discrediting Ukraine: Other | 201 |
| 6 | URW: Discrediting Ukraine: Discrediting Ukrainian government and officials and policies | URW: Discrediting the West, Diplomacy: Other | 194 |
| 7 | CC: Amplifying Climate Fears: Amplifying existing fears of global warming | CC: Amplifying Climate Fears: Other | 186 |
| 8 | CC: Criticism of climate movement: Climate movement is alarmist | CC: Criticism of climate movement: Other | 181 |
| 9 | URW: Discrediting Ukraine: Discrediting Ukrainian government and officials and policies | URW: Blaming the war on others rather than the invader: The West are the aggressors | 180 |
| 10 | CC: Criticism of climate movement: Climate movement is alarmist | CC: Downplaying climate change: Other | 178 |
| 11 | CC: Criticism of institutions and authorities: Criticism of political organizations and figures | CC: Criticism of institutions and authorities: Other | 178 |
| 12 | CC: Amplifying Climate Fears: Amplifying existing fears of global warming | Other | 177 |
| 13 | CC: Criticism of climate movement: Climate movement is alarmist | CC: Questioning the measurements and science: Scientific community is unreliable | 174 |
| 14 | CC: Criticism of institutions and authorities: Criticism of political organizations and figures | CC: Criticism of climate policies: Climate policies have negative impact on the economy | 166 |
| 15 | CC: Criticism of climate movement: Climate movement is alarmist | CC: Questioning the measurements and science: Other | 165 |
| 16 | URW: Discrediting Ukraine: Discrediting Ukrainian government and officials and policies | URW: Distrust towards Media: Western media is an instrument of propaganda | 159 |
| 17 | CC: Criticism of institutions and authorities: Criticism of political organizations and figures | CC: Criticism of institutions and authorities: Criticism of national governments | 158 |
| 18 | URW: Discrediting Ukraine: Discrediting Ukrainian government and officials and policies | URW: Distrust towards Media: Other | 154 |
| 19 | URW: Discrediting Ukraine: Discrediting Ukrainian government and officials and policies | URW: Blaming the war on others rather than the invader: Other | 149 |
| 20 | URW: Discrediting Ukraine: Discrediting Ukrainian government and officials and policies | URW: Discrediting Ukraine: Discrediting Ukrainian military | 142 |

## 7. Vote-Level Failure Taxonomy (Phase 2)

*No votes/ directories found. Run experiments with `enable_vote_saving: true` to enable Phase 2 analysis.*

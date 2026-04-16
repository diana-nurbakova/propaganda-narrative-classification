# Evidence Faithfulness Report

Generated: 2026-02-11 02:01:58

Evaluates whether `evidence_quote` fields from LLM classification output are faithful to the source documents.

| Category | Description |
|----------|-------------|
| Exact | Quote appears verbatim in source text |
| Near-exact | Matches after whitespace normalization (ratio >= 0.95) |
| Fuzzy | High similarity to source window (ratio >= 0.80) |
| Hallucination | No close match found (ratio < 0.80) |
| Empty | Quote is empty, missing, or 'N/A' |

## Summary

| Experiment | Run | Quotes | Exact | Near-exact | Fuzzy | Halluc. | Empty | Faithfulness |
|------------|-----|--------|-------|------------|-------|---------|-------|--------------|
| actor_critic_deepseek_en_t00_evidence | run_1 | 392 | 310 (79%) | 37 (9%) | 18 (5%) | 13 (3%) | 14 (4%) | 93.1% |
| actor_critic_gpt5nano_en_t00 | run_1 | 221 | 160 (72%) | 44 (20%) | 11 (5%) | 2 (1%) | 4 (2%) | 97.3% |
| actor_critic_gpt5nano_en_t00 | run_2 | 350 | 259 (74%) | 62 (18%) | 22 (6%) | 3 (1%) | 4 (1%) | 98.0% |
| actor_critic_gpt5nano_en_t00 | run_3 | 369 | 293 (79%) | 42 (11%) | 24 (7%) | 5 (1%) | 5 (1%) | 97.3% |
| actor_critic_gpt5nano_en_t00 | run_4 | 382 | 275 (72%) | 73 (19%) | 24 (6%) | 6 (2%) | 4 (1%) | 97.4% |
| actor_critic_gpt5nano_en_t00 | run_5 | 310 | 240 (77%) | 40 (13%) | 25 (8%) | 1 (0%) | 4 (1%) | 98.4% |
| actor_critic_mistral_en_t00 | run_{run_id} | 782 | 448 (57%) | 143 (18%) | 107 (14%) | 78 (10%) | 6 (1%) | 89.3% |
| actor_critic_mistral_en_t00_evidence | run_1 | 793 | 444 (56%) | 136 (17%) | 113 (14%) | 87 (11%) | 13 (2%) | 87.4% |
| agora_majority_gpt5nano_bg_t00 | run_1 | 187 | 135 (72%) | 30 (16%) | 11 (6%) | 3 (2%) | 8 (4%) | 94.1% |
| agora_majority_gpt5nano_bg_t00 | run_2 | 207 | 157 (76%) | 35 (17%) | 10 (5%) | 0 (0%) | 5 (2%) | 97.6% |
| agora_majority_gpt5nano_bg_t00 | run_3 | 190 | 143 (75%) | 30 (16%) | 11 (6%) | 1 (1%) | 5 (3%) | 96.8% |
| agora_majority_gpt5nano_bg_t00 | run_4 | 206 | 149 (72%) | 42 (20%) | 9 (4%) | 0 (0%) | 6 (3%) | 97.1% |
| agora_majority_gpt5nano_bg_t00 | run_5 | 193 | 144 (75%) | 33 (17%) | 7 (4%) | 5 (3%) | 4 (2%) | 95.3% |
| agora_majority_gpt5nano_hi_t00 | run_1 | 142 | 115 (81%) | 11 (8%) | 4 (3%) | 2 (1%) | 10 (7%) | 91.5% |
| agora_majority_gpt5nano_hi_t00 | run_2 | 143 | 101 (71%) | 19 (13%) | 11 (8%) | 2 (1%) | 10 (7%) | 91.6% |
| agora_majority_gpt5nano_hi_t00 | run_3 | 158 | 116 (73%) | 20 (13%) | 11 (7%) | 0 (0%) | 11 (7%) | 93.0% |
| agora_majority_gpt5nano_hi_t00 | run_4 | 145 | 97 (67%) | 21 (14%) | 11 (8%) | 3 (2%) | 13 (9%) | 89.0% |
| agora_majority_gpt5nano_hi_t00 | run_5 | 135 | 105 (78%) | 15 (11%) | 1 (1%) | 1 (1%) | 13 (10%) | 89.6% |
| agora_majority_gpt5nano_pt_t00 | run_1 | 114 | 83 (73%) | 17 (15%) | 4 (4%) | 1 (1%) | 9 (8%) | 91.2% |
| agora_majority_gpt5nano_pt_t00 | run_2 | 118 | 86 (73%) | 12 (10%) | 6 (5%) | 5 (4%) | 9 (8%) | 88.1% |
| agora_majority_gpt5nano_pt_t00 | run_3 | 125 | 97 (78%) | 18 (14%) | 1 (1%) | 1 (1%) | 8 (6%) | 92.8% |
| agora_majority_gpt5nano_pt_t00 | run_4 | 125 | 87 (70%) | 18 (14%) | 9 (7%) | 2 (2%) | 9 (7%) | 91.2% |
| agora_majority_gpt5nano_pt_t00 | run_5 | 125 | 88 (70%) | 21 (17%) | 5 (4%) | 2 (2%) | 9 (7%) | 91.2% |
| agora_majority_mistral_en_t00_evidence | run_1 | 740 | 428 (58%) | 113 (15%) | 118 (16%) | 71 (10%) | 10 (1%) | 89.0% |
| agora_mistral_en_t00_evidence | run_1 | 750 | 415 (55%) | 128 (17%) | 115 (15%) | 85 (11%) | 7 (1%) | 87.7% |
| baseline_deepseek_en_t00_evidence | run_1 | 513 | 395 (77%) | 51 (10%) | 31 (6%) | 23 (4%) | 13 (3%) | 93.0% |
| baseline_mistral_en_t00_evidence | run_1 | 849 | 485 (57%) | 135 (16%) | 124 (15%) | 99 (12%) | 6 (1%) | 87.6% |

## Aggregated by Experiment

| Experiment | Quotes | Exact % | Near-exact % | Fuzzy % | Halluc. % | Empty % | Faithfulness |
|------------|--------|---------|--------------|---------|-----------|---------|-------------|
| actor_critic_deepseek_en_t00_evidence | 392 | 79.1% | 9.4% | 4.6% | 3.3% | 3.6% | 93.1% |
| actor_critic_gpt5nano_en_t00 | 1632 | 75.2% | 16.0% | 6.5% | 1.0% | 1.3% | 97.7% |
| actor_critic_mistral_en_t00 | 782 | 57.3% | 18.3% | 13.7% | 10.0% | 0.8% | 89.3% |
| actor_critic_mistral_en_t00_evidence | 793 | 56.0% | 17.2% | 14.2% | 11.0% | 1.6% | 87.4% |
| agora_majority_gpt5nano_bg_t00 | 983 | 74.1% | 17.3% | 4.9% | 0.9% | 2.8% | 96.2% |
| agora_majority_gpt5nano_hi_t00 | 723 | 73.9% | 11.9% | 5.3% | 1.1% | 7.9% | 91.0% |
| agora_majority_gpt5nano_pt_t00 | 607 | 72.7% | 14.2% | 4.1% | 1.8% | 7.2% | 90.9% |
| agora_majority_mistral_en_t00_evidence | 740 | 57.8% | 15.3% | 15.9% | 9.6% | 1.4% | 89.1% |
| agora_mistral_en_t00_evidence | 750 | 55.3% | 17.1% | 15.3% | 11.3% | 0.9% | 87.7% |
| baseline_deepseek_en_t00_evidence | 513 | 77.0% | 9.9% | 6.0% | 4.5% | 2.5% | 93.0% |
| baseline_mistral_en_t00_evidence | 849 | 57.1% | 15.9% | 14.6% | 11.7% | 0.7% | 87.6% |

## Hallucination Examples

Showing up to 10 hallucinated quotes with their match ratios.

- **agora_majority_gpt5nano_hi_t00** | `HI_107.txt` | URW: Blaming the war on others rather than the invader
  Quote: "The West is pushing us towards World War III." (ratio: 0.222)

- **actor_critic_mistral_en_t00_evidence** | `EN_CC_200033.txt` | CC: Hidden plots by secret schemes of powerful groups: Climate agenda has hidden motives
  Quote: "the co-founder of Extinction Rebellion... admitted in his own words that his movement 'isn’t about t..." (ratio: 0.243)

- **actor_critic_mistral_en_t00_evidence** | `EN_CC_200033.txt` | CC: Criticism of climate policies: Other
  Quote: "The co-founder of Extinction Rebellion... admitted in his own words that his movement 'isn’t about t..." (ratio: 0.251)

- **actor_critic_deepseek_en_t00_evidence** | `EN_UA_DEV_100033.txt` | URW: Negative Consequences for the West
  Quote: "“Here’s what will be on the table after our victory... The dissolution of NATO... Extradition of all..." (ratio: 0.276)

- **actor_critic_mistral_en_t00** | `EN_UA_DEV_100013.txt` | URW: Discrediting Ukraine: Ukraine is a puppet of the West
  Quote: "Zaluzhny now serves as a point man between the Ukrainian regime and its military and British imperia..." (ratio: 0.301)

- **actor_critic_mistral_en_t00_evidence** | `EN_CC_200036.txt` | CC: Criticism of institutions and authorities
  Quote: "Al Gore, Bill Clinton's former vice president, condemned 'greenhouse gas pollution' for 'boiling the..." (ratio: 0.301)

- **actor_critic_mistral_en_t00_evidence** | `EN_CC_200036.txt` | CC: Criticism of institutions and authorities: Criticism of political organizations and figures
  Quote: "Al Gore, Bill Clinton's former vice president, condemned 'greenhouse gas pollution' for 'boiling the..." (ratio: 0.301)

- **agora_majority_mistral_en_t00_evidence** | `EN_CC_200036.txt` | CC: Criticism of institutions and authorities: Criticism of political organizations and figures
  Quote: "Al Gore, Bill Clinton's former vice president, condemned 'greenhouse gas pollution' for 'boiling the..." (ratio: 0.301)

- **agora_mistral_en_t00_evidence** | `EN_CC_200036.txt` | CC: Criticism of institutions and authorities: Criticism of political organizations and figures
  Quote: "Al Gore, Bill Clinton's former vice president, condemned 'greenhouse gas pollution' for 'boiling the..." (ratio: 0.301)

- **baseline_mistral_en_t00_evidence** | `EN_CC_200036.txt` | CC: Criticism of institutions and authorities: Criticism of political organizations and figures
  Quote: "Al Gore, Bill Clinton's former vice president, condemned 'greenhouse gas pollution' for 'boiling the..." (ratio: 0.301)


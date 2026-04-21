# Confusion Pair Tracking: Baseline vs Actor-Critic

*Generated: 2026-04-21 23:19*

## Groups

**Baseline** (2 experiments): baseline_deepseek_en_t00, baseline_mistral_en_t00

**Actor-Critic** (2 experiments): actor_critic_deepseek_en_t00, actor_critic_mistral_en_t00

## Summary

- Confusion cells improved (delta > 0): **106**
- Confusion cells worsened (delta < 0): **143**
- Total improvement mass: **1.2772**
- Total worsening mass: **1.4251**
- Net change: **-0.1480** (overall worsening)

## Top Improved Confusion Pairs (Actor-Critic reduces confusion)

Positive delta = Baseline had more confusion than Actor-Critic.

| # | Gold | Predicted | bis(Baseline) | bis(Actor-Critic) | Delta | Domain |
|---|------|-----------|---------|---------|-------|--------|
| 1 | Climate change is beneficial | Questioning the measurements and science | 0.0714 | 0.0004 | +0.0711 | same |
| 2 | Controversy about green technologies | Downplaying climate change | 0.0587 | 0.0003 | +0.0584 | same |
| 3 | Criticism of institutions and authorities | Controversy about green technologies | 0.2011 | 0.1515 | +0.0496 | same |
| 4 | Controversy about green technologies | Criticism of institutions and authorities | 0.1802 | 0.1317 | +0.0484 | same |
| 5 | Questioning the measurements and science | Criticism of climate movement | 0.1348 | 0.0924 | +0.0424 | same |
| 6 | Negative Consequences for the West | Discrediting the West, Diplomacy | 0.2457 | 0.2067 | +0.0390 | same |
| 7 | Overpraising the West | Speculating war outcomes | 0.1151 | 0.0769 | +0.0382 | same |
| 8 | Controversy about green technologies | Green policies are geopolitical instruments | 0.1955 | 0.1577 | +0.0378 | same |
| 9 | Criticism of climate policies | Downplaying climate change | 0.1252 | 0.0880 | +0.0373 | same |
| 10 | Negative Consequences for the West | Blaming the war on others rather than the invader | 0.2713 | 0.2343 | +0.0369 | same |

## Top Worsened Confusion Pairs (Actor-Critic increases confusion)

Negative delta = Actor-Critic has more confusion than Baseline.

| # | Gold | Predicted | bis(Baseline) | bis(Actor-Critic) | Delta | Domain |
|---|------|-----------|---------|---------|-------|--------|
| 1 | Negative Consequences for the West | Overpraising the West | 0.0006 | 0.1068 | -0.1062 | same |
| 2 | Blaming the war on others rather than the invader | Speculating war outcomes | 0.0301 | 0.1287 | -0.0986 | same |
| 3 | Overpraising the West | Amplifying war-related fears | 0.0937 | 0.1886 | -0.0949 | same |
| 4 | Controversy about green technologies | Amplifying Climate Fears | 0.0007 | 0.0790 | -0.0783 | same |
| 5 | Climate change is beneficial | Downplaying climate change | 0.1528 | 0.2229 | -0.0700 | same |
| 6 | Criticism of climate policies | Amplifying Climate Fears | 0.0003 | 0.0520 | -0.0518 | same |
| 7 | Questioning the measurements and science | Amplifying Climate Fears | 0.0527 | 0.0994 | -0.0467 | same |
| 8 | Criticism of institutions and authorities | Green policies are geopolitical instruments | 0.1793 | 0.2221 | -0.0428 | same |
| 9 | Hidden plots by secret schemes of powerful groups | Downplaying climate change | 0.0003 | 0.0356 | -0.0353 | same |
| 10 | Negative Consequences for the West | Hidden plots by secret schemes of powerful groups | 0.0596 | 0.0936 | -0.0340 | cross |

## Top Confused Pairs — Baseline

| # | Gold | Predicted | bis mass | raw mass | Domain |
|---|------|-----------|----------|----------|--------|
| 1 | Criticism of climate movement | Amplifying Climate Fears | 0.3112 | 4.0695 | same |
| 2 | Negative Consequences for the West | Blaming the war on others rather than the invader | 0.2713 | 1.2177 | same |
| 3 | Blaming the war on others rather than the invader | Russia is the Victim | 0.2584 | 0.8200 | same |
| 4 | Questioning the measurements and science | Downplaying climate change | 0.2523 | 1.2260 | same |
| 5 | Negative Consequences for the West | Discrediting the West, Diplomacy | 0.2457 | 1.2177 | same |
| 6 | Hidden plots by secret schemes of powerful groups | Green policies are geopolitical instruments | 0.2400 | 1.1260 | same |
| 7 | Speculating war outcomes | Praise of Russia | 0.2025 | 1.2901 | same |
| 8 | Criticism of institutions and authorities | Controversy about green technologies | 0.2011 | 2.1260 | same |
| 9 | Controversy about green technologies | Green policies are geopolitical instruments | 0.1955 | 0.9010 | same |
| 10 | Criticism of institutions and authorities | Criticism of climate policies | 0.1945 | 3.9427 | same |

## Top Confused Pairs — Actor-Critic

| # | Gold | Predicted | bis mass | raw mass | Domain |
|---|------|-----------|----------|----------|--------|
| 1 | Criticism of climate movement | Amplifying Climate Fears | 0.2767 | 4.6593 | same |
| 2 | Questioning the measurements and science | Downplaying climate change | 0.2394 | 1.3510 | same |
| 3 | Negative Consequences for the West | Blaming the war on others rather than the invader | 0.2343 | 0.9843 | same |
| 4 | Blaming the war on others rather than the invader | Russia is the Victim | 0.2251 | 0.7129 | same |
| 5 | Climate change is beneficial | Downplaying climate change | 0.2229 | 1.0593 | same |
| 6 | Criticism of institutions and authorities | Green policies are geopolitical instruments | 0.2221 | 2.5510 | same |
| 7 | Hidden plots by secret schemes of powerful groups | Green policies are geopolitical instruments | 0.2134 | 0.9593 | same |
| 8 | Negative Consequences for the West | Discrediting the West, Diplomacy | 0.2067 | 0.9843 | same |
| 9 | Speculating war outcomes | Praise of Russia | 0.2006 | 1.3022 | same |
| 10 | Hidden plots by secret schemes of powerful groups | Criticism of institutions and authorities | 0.1940 | 1.4177 | same |

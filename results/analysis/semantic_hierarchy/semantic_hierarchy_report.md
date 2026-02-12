# Semantic Similarity Hierarchy of Narratives and Subnarratives

This report compares two methods for computing semantic similarity between subnarrative labels:

1. **TF-IDF** (bag-of-words): TF-IDF cosine similarity on label names + definitions, with a +0.2 structural bonus for same-parent subnarratives.
2. **Embeddings** (`all-MiniLM-L6-v2`): Dense sentence embeddings that capture semantic meaning beyond word overlap. No structural bonus applied.

Embeddings are better at identifying semantically related labels that share few words (e.g., *"The West is weak"* and *"The EU is divided"* are semantically close but have no word overlap). TF-IDF is limited to lexical overlap.

## URW (Ukraine-Russia War)

### URW: Blaming the war on others rather than the invader
*Statements attributing responsibility or fault to entities other than Russia in the context of Russia’s invasion of Ukraine*

- **Ukraine is the aggressor**: Statements that shift the responsibility of the aggression to Ukraine instead of Russia and portray Ukraine as the attacker.
- **The West are the aggressors**: Statements that shift the responsibility for the conflict and escalation to the Western block.

### URW: Discrediting Ukraine
*Statements that undermine the legitimacy, actions, or intentions of Ukraine or Ukrainians as a nation.*

- **Rewriting Ukraine’s history**: Statements that aim to reestablish history of Ukrainian nation in a way that discredits its reputation.
- **Discrediting Ukrainian nation and society**: Statements that aggressively undermine the legitimacy and reputability of Ukrainian ethnicity and people
- **Discrediting Ukrainian military**: Statements that aim to undermine the capabilities, professionalism or effectiveness of the Ukrainian armed forces.
- **Discrediting Ukrainian government and officials and policies**: Statements that seek to delegitimize the Ukrainian government, its leaders, and its policies, portraying them as corrupt or incompetent.
- **Ukraine is a puppet of the West**: Claims that Ukraine is controlled or heavily influenced by Western powers, particularly the United States and European Union.
- **Ukraine is a hub for criminal activities**: Allegations that Ukraine is a center for illegal activities such as human trafficking, drug smuggling, or organized crime
- **Ukraine is associated with nazism**: Accusations that Ukrainian society or government has ties to or sympathies with Nazi ideology, often referencing historical events or extremist groups.
- **Situation in Ukraine is hopeless**: Statements that portray Ukraine as having no viable perspectives or no potential positive future.

### URW: Russia is the Victim
*Statements that portray Russia as being unfairly targeted or victimized.*

- **The West is russophobic**: Statements that claim that the negative reaction to Russia’s actions are because of the negative perspective of western countries instead of Russia’s own actions.
- **Russia actions in Ukraine are only self-defence**: Statements that justify Russia’s action solely as legitimate self-defence and not a deliberate action
- **UA is anti-RU extremists**: Statements claiming that Ukraine is comprised of extremist elements that are vehemently opposed to Russia.

### URW: Praise of Russia
*Statements that positively highlight Russia’s actions, policies, or character*

- **Praise of Russian military might**: Statements that positively highlight Russia’s military institutions, equipment and scale.
- **Praise of Russian President Vladimir Putin**: Statements that present Vladimir Putin positively, including his personal and leadership qualities.
- **Russia is a guarantor of peace and prosperity**: Statements that portray Russia solely in a positive manner, emphasising their potential to provide peace and prosperity to those that cooperate.
- **Russia has international support from a number of countries and people**: Statements that emphasise the popularity and acceptance of Russia in the international stage.
- **Russian invasion has strong national support**: Statements that emphasise the popularity and acceptance of the invasion inside Russia and on Russian-speaking populations.

### URW: Overpraising the West
*Statements that excessively and unduly laud or extol the virtues, accomplishments, and moral superiority of Western countries, particularly in the context of international relations and military.*

- **NATO will destroy Russia**: Statements that suggest or claim that the North Atlantic Treaty Organization (NATO) and its allies are capable or already in the process of eradicating Russia.
- **The West belongs in the right side of history**: Statements that portray Western nations and their actions as morally superior and aligned with progress and justice and possess moral superiority.
- **The West has the strongest international support**: Statements that emphasize or claim widespread backing for Western policies and actions from the international community, potentially downplaying opposition or criticism.

### URW: Speculating war outcomes
*Statements that predict or make assumptions about the potential results or consequences of a conflict*

- **Russian army is collapsing**: Statements that suggest or claim that the Russian military is experiencing a significant decline in its effectiveness, strength, or morale.
- **Russian army will lose all the occupied territories**: Speculative statements that predict or assume the potential outcomes of the conflict, specifically regarding the possibility of the Russian military losing control of all the territories it currently occupies.
- **Ukrainian army is collapsing**: Statements that suggest or claim that the Ukrainian military is experiencing a significant decline in its effectiveness, strength, or morale.

### URW: Discrediting the West, Diplomacy
*Statements that criticize the Western countries, or international diplomatic efforts.*

- **The EU is divided**: Statements that present the EU as a set of divided entities and interests, usually unable to take actions.
- **The West is weak**: Statements presenting the West overall as a non-potent group of countries (that is not as powerful as it used to be).
- **The West is overreacting**: Statements that claim that the West and its institutions are reacting to Russia’s actions in a disproportionate manner.
- **The West does not care about Ukraine, only about its interests**: Statements that claim that the West is only interested in Ukraine for its own benefits, disregarding the country’s fate.
- **Diplomacy does/will not work**: Statements discrediting the potential of ongoing or potential diplomatic efforts.
- **West is tired of Ukraine**: Claims that Western countries, particularly the United States and European nations, are becoming fatigued or disinterested in supporting Ukraine and its efforts.

### URW: Negative Consequences for the West
*Statements that highlight or predict adverse outcomes for Western countries and their interests.*

- **Sanctions imposed by Western countries will backfire**: Statements that catastrophize on the possible negative effects for Western sanctions of Russia.
- **The conflict will increase the Ukrainian refugee flows to Europe**: Statements that catastrophize on the possible refugee outflows due to the conflict.

### URW: Distrust towards Media
*Statements that question the reliability or integrity of media organizations.*

- **Western media is an instrument of propaganda**: Statements that discredit the media institutions of the West and claim that they are instruments of propaganda.
- **Ukrainian media cannot be trusted**: Statements that discredit the media institutions of the Ukraine and claim that they should not be trusted for reporting on the war.

### URW: Amplifying war-related fears
*Statements that evoke fear or anxiety about potential threats, dangers or reactions.*

- **By continuing the war we risk WWIII**: Statements that warn against upsetting Russia’s and its leadership, evoking fear of causing WW3.
- **Russia will also attack other countries**: Statements that claim that it is imminent that Russia will attack other countries.
- **There is a real possibility that nuclear weapons will be employed**: Statements that evoke fear or anxiety about the use of nuclear weapons.
- **NATO should/will directly intervene**: Statements that suggest or claim that the North Atlantic Treaty Organization (NATO) ought to or will take direct military action in a conflict, potentially implying a shift in policy or strategy.

### URW: Hidden plots by secret schemes of powerful groups
*Statements that propose secret plots or hidden agendas related to climate change initiated by powerful entities or groups.*


## CC (Climate Change)

### CC: Criticism of climate policies
*Statements that question the effectiveness, economic impact, or motives behind climate policies.*

- **Climate policies are ineffective**: Statements suggesting that climate policies fail to achieve their intended environmental goals.
- **Climate policies have negative impact on the economy**: Statements claiming that climate policies lead to negative economic outcomes.
- **Climate policies are only for profit**: Statements that argue climate policies are driven by financial or corporate gain rather than genuine environmental concerns.

### CC: Criticism of institutions and authorities
*Statements that challenge the competence, integrity, or intentions of various institutions and authorities in relation to climate change*

- **Criticism of the EU**: Statements that express disapproval or distrust of the EU’s role or approach to climate change or the EU in general.
- **Criticism of international entities**: Statements that criticize the role and influence of international entities on climate policy.
- **Criticism of national governments**: Statements that disapprove of the ways national governments handle climate change
- **Criticism of political organizations and figures**: Statements that discredit political organizations and figures in the context of climate change debate.

### CC: Climate change is beneficial
*Statements that present arguments that support that changes in climate can have positive effects as well.*

- **CO2 is beneficial**: Statements suggesting that increased CO2 levels have positive impacts on the environment.
- **Temperature increase is beneficial**: Statements claiming that rising global temperatures can have positive effects.

### CC: Downplaying climate change
*Statements that minimize the significance or impact of climate change.*

- **Climate cycles are natural**: Statements suggesting that climate change is a natural and cyclical occurrence.
- **Weather suggests the trend is global cooling**: Statements using local or short-term weather patterns to argue against global warming.
- **Temperature increase does not have significant impact**: Statements claiming that the increase in temperature is not going to have any noticeable effect in nature.
- **CO2 concentrations are too small to have an impact**: Statements claiming that the concentrations of CO2 will have a negligible effect.
- **Human activities do not impact climate change**: Statements that support that climate change is not caused by human activity.
- **Ice is not melting**: Statements claiming that there is not melting of ice.
- **Sea levels are not rising**: Statements denying that sea levels have risen (or will rise).
- **Humans and nature will adapt to the changes**: Statements claiming that whatever the changes in climate humans or nature will manage to find solutions to adapt.

### CC: Questioning the measurements and science
*Statements that raise doubts about the scientific methods, data, and consensus on climate change.*

- **Methodologies/metrics used are unreliable/faulty**: Statements claiming that the scientific methodologies and metrics used to measure climate change are flawed or unreliable.
- **Data shows no temperature increase**: Statements asserting that available data does not support the claim of global temperature increase.
- **Greenhouse effect/carbon dioxide do not drive climate change**: Statements asserting that available data does not support the claim of global temperature increase.
- **Scientific community is unreliable**: Statements discrediting scientists, the scientific community and their actions.

### CC: Criticism of climate movement
*Statements that challenge the motives, integrity, or impact of the climate movement.*

- **Climate movement is alarmist**: Statements suggesting that the climate movement exaggerates the severity of climate change for dramatic effect.
- **Climate movement is corrupt**: Statements alleging that the climate movement is influenced by ulterior motives, by corruption or by unethical practices.
- **Ad hominem attacks on key activists**: Statements attacking the reputation of key figures (such as scientists, activists, politicians or public figures).

### CC: Controversy about green technologies
*Statements that express skepticism or criticism of environmentally friendly technologies.*

- **Renewable energy is dangerous**: Statements claiming that renewable energy sources pose significant risks or dangers.
- **Renewable energy is unreliable**: Statements asserting that renewable energy sources are not dependable for widespread adoption.
- **Renewable energy is costly**: Statements asserting that renewable energy sources are too expensive, inefficient and worth adopting for widespread use.
- **Nuclear energy is not climate friendly**: Statements asserting that nuclear sources are or should not be considered as good for the climate.

### CC: Hidden plots by secret schemes of powerful groups

- **Blaming global elites**: Statements attributing climate change agendas to secretive and powerful global elites.
- **Climate agenda has hidden motives**: Claims that the push for climate action is driven by ulterior motives, such as political power or population control

### CC: Amplifying Climate Fears
*Statements that emphasize and amplify fears about the consequences of climate change.*

- **Earth will be uninhabitable soon**: Statements predicting that the Earth will become uninhabitable in the near future due to climate change.
- **Amplifying existing fears of global warming**: Statements that are using fears related to warming of the earths surface and atmosphere and speculating on side effects to spread panic.
- **Doomsday scenarios for humans**: Statements presenting intense catastrophic scenarios as results of climate change.
- **Whatever we do it is already too late**: Statements that minimize the urgency of addressing climate change by suggesting that any action taken at this point is futile or too late to make a meaningful impact.

### CC: Green policies are geopolitical instruments
*Statements claimin that that environmental policies and initiatives are used as tools for geopolitical power and influence rather than genuine environmental concern.*

- **Climate-related international relations are abusive/exploitative**: Statements criticizing international relations related to climate change as exploitative or economically abusive.
- **Green activities are a form of neo-colonialism**: Statements suggesting that green initiatives are a way for developed countries to exert control and influence over developing nations, a modern form of colonial practices.

---

## Similarity Analysis: Embeddings (Primary)

### Most Similar Subnarrative Pairs (Embeddings)

These pairs have the highest semantic similarity and are most likely to be confused with each other during classification.

| Rank | Label A | Label B | Similarity | Same Parent? |
|------|---------|---------|------------|-------------|
| 1 | URW: Russian army is collapsing | URW: Ukrainian army is collapsing | 0.913 | Yes |
| 2 | URW: Discrediting Ukrainian government and of | URW: Discrediting Ukrainian military | 0.913 | Yes |
| 3 | CC: Criticism of national governments | CC: Criticism of political organizations and | 0.886 | Yes |
| 4 | CC: Criticism of international entities | CC: Criticism of political organizations and | 0.882 | Yes |
| 5 | URW: Discrediting Ukrainian nation and societ | URW: Rewriting Ukraine’s history | 0.881 | Yes |
| 6 | CC: Renewable energy is costly | CC: Renewable energy is unreliable | 0.881 | Yes |
| 7 | URW: Discrediting Ukrainian government and of | URW: Rewriting Ukraine’s history | 0.879 | Yes |
| 8 | CC: CO2 is beneficial | CC: Temperature increase is beneficial | 0.878 | Yes |
| 9 | CC: Climate policies are ineffective | CC: Climate policies are only for profit | 0.874 | Yes |
| 10 | URW: Discrediting Ukrainian government and of | URW: Discrediting Ukrainian nation and societ | 0.869 | Yes |
| 11 | CC: Criticism of international entities | CC: Criticism of national governments | 0.857 | Yes |
| 12 | URW: Discrediting Ukrainian military | URW: Rewriting Ukraine’s history | 0.857 | Yes |
| 13 | URW: The West does not care about Ukraine, on | URW: West is tired of Ukraine | 0.857 | Yes |
| 14 | CC: Blaming global elites | CC: Climate agenda has hidden motives | 0.856 | Yes |
| 15 | CC: Data shows no temperature increase | CC: Greenhouse effect/carbon dioxide do not  | 0.856 | Yes |
| 16 | URW: Rewriting Ukraine’s history | URW: Situation in Ukraine is hopeless | 0.855 | Yes |
| 17 | URW: Russia has international support from a  | URW: Russian invasion has strong national sup | 0.852 | Yes |
| 18 | CC: Renewable energy is dangerous | CC: Renewable energy is unreliable | 0.851 | Yes |
| 19 | CC: Human activities do not impact climate c | CC: Humans and nature will adapt to the chan | 0.851 | Yes |
| 20 | URW: Discrediting Ukrainian nation and societ | URW: Situation in Ukraine is hopeless | 0.850 | Yes |
| 21 | CC: Climate policies are ineffective | CC: Climate policies have negative impact on | 0.849 | Yes |
| 22 | CC: Climate policies are only for profit | CC: Climate policies have negative impact on | 0.849 | Yes |
| 23 | URW: Discrediting Ukrainian military | URW: Discrediting Ukrainian nation and societ | 0.845 | Yes |
| 24 | CC: Renewable energy is costly | CC: Renewable energy is dangerous | 0.845 | Yes |
| 25 | URW: The West belongs in the right side of hi | URW: The West has the strongest international | 0.841 | Yes |
| 26 | CC: Amplifying existing fears of global warm | CC: Whatever we do it is already too late | 0.839 | Yes |
| 27 | CC: Amplifying existing fears of global warm | CC: Doomsday scenarios for humans | 0.836 | Yes |
| 28 | URW: Discrediting Ukrainian government and of | URW: Situation in Ukraine is hopeless | 0.834 | Yes |
| 29 | URW: Praise of Russian President Vladimir Put | URW: Russia is a guarantor of peace and prosp | 0.830 | Yes |
| 30 | URW: Diplomacy does/will not work | URW: The West is weak | 0.829 | Yes |

### Most Dissimilar Sibling Subnarratives (Embeddings)

Subnarratives under the same parent narrative that are most different semantically. High confusion between these would be more surprising.

| Parent Narrative | Label A | Label B | Similarity |
|-----------------|---------|---------|------------|
| Questioning the measurements and sc | Data shows no temperature increase | Scientific community is unreliable | 0.489 |
| Questioning the measurements and sc | Greenhouse effect/carbon dioxide do | Scientific community is unreliable | 0.517 |
| Overpraising the West | NATO will destroy Russia | The West belongs in the right side  | 0.563 |
| Overpraising the West | NATO will destroy Russia | The West has the strongest internat | 0.588 |
| Discrediting the West, Diplomacy | The EU is divided | The West is overreacting | 0.603 |
| Questioning the measurements and sc | Data shows no temperature increase | Methodologies/metrics used are unre | 0.606 |
| Discrediting the West, Diplomacy | The EU is divided | The West does not care about Ukrain | 0.631 |
| Downplaying climate change | CO2 concentrations are too small to | Sea levels are not rising | 0.635 |
| Discrediting the West, Diplomacy | The EU is divided | West is tired of Ukraine | 0.638 |
| Downplaying climate change | CO2 concentrations are too small to | Ice is not melting | 0.647 |
| Downplaying climate change | CO2 concentrations are too small to | Weather suggests the trend is globa | 0.662 |
| Downplaying climate change | Ice is not melting | Temperature increase does not have  | 0.664 |
| Discrediting Ukraine | Discrediting Ukrainian military | Ukraine is a hub for criminal activ | 0.669 |
| Amplifying Climate Fears | Earth will be uninhabitable soon | Whatever we do it is already too la | 0.669 |
| Amplifying war-related fears | NATO should/will directly intervene | There is a real possibility that nu | 0.670 |

### Cross-Category Similarities (Embeddings)

Pairs from different domains (URW vs CC) that are semantically similar.

| URW Subnarrative | CC Subnarrative | Similarity |
|-----------------|-----------------|------------|
| There is a real possibility that nuclear | Amplifying existing fears of global warm | 0.520 |
| There is a real possibility that nuclear | Doomsday scenarios for humans | 0.506 |
| By continuing the war we risk WWIII | Amplifying existing fears of global warm | 0.469 |
| There is a real possibility that nuclear | Whatever we do it is already too late | 0.452 |
| There is a real possibility that nuclear | Renewable energy is dangerous | 0.446 |
| By continuing the war we risk WWIII | Doomsday scenarios for humans | 0.441 |
| There is a real possibility that nuclear | Nuclear energy is not climate friendly | 0.423 |
| NATO should/will directly intervene | Whatever we do it is already too late | 0.419 |
| There is a real possibility that nuclear | Earth will be uninhabitable soon | 0.411 |
| Russia will also attack other countries | Amplifying existing fears of global warm | 0.406 |
| By continuing the war we risk WWIII | Whatever we do it is already too late | 0.406 |
| The West are the aggressors | Blaming global elites | 0.399 |
| Russia will also attack other countries | Doomsday scenarios for humans | 0.396 |
| Sanctions imposed by Western countries w | Climate-related international relations  | 0.390 |
| The West is overreacting | Blaming global elites | 0.387 |

---

## Similarity Analysis: TF-IDF (Baseline)

### Most Similar Subnarrative Pairs (TF-IDF)

These pairs have the highest semantic similarity and are most likely to be confused with each other during classification.

| Rank | Label A | Label B | Similarity | Same Parent? |
|------|---------|---------|------------|-------------|
| 1 | URW: Russian army is collapsing | URW: Ukrainian army is collapsing | 0.976 | Yes |
| 2 | CC: Data shows no temperature increase | CC: Greenhouse effect/carbon dioxide do not  | 0.860 | Yes |
| 3 | CC: Renewable energy is costly | CC: Renewable energy is unreliable | 0.819 | Yes |
| 4 | CC: Renewable energy is dangerous | CC: Renewable energy is unreliable | 0.759 | Yes |
| 5 | CC: Climate movement is alarmist | CC: Climate movement is corrupt | 0.727 | Yes |
| 6 | CC: Renewable energy is costly | CC: Renewable energy is dangerous | 0.699 | Yes |
| 7 | CC: Climate policies are ineffective | CC: Climate policies are only for profit | 0.689 | Yes |
| 8 | CC: Climate policies are ineffective | CC: Climate policies have negative impact on | 0.683 | Yes |
| 9 | URW: Ukrainian media cannot be trusted | URW: Western media is an instrument of propag | 0.677 | Yes |
| 10 | CC: Climate policies are only for profit | CC: Climate policies have negative impact on | 0.648 | Yes |
| 11 | URW: The West are the aggressors | URW: Ukraine is the aggressor | 0.557 | Yes |
| 12 | CC: CO2 is beneficial | CC: Temperature increase is beneficial | 0.535 | Yes |
| 13 | URW: The West does not care about Ukraine, on | URW: The West is overreacting | 0.521 | Yes |
| 14 | CC: Blaming global elites | CC: Climate agenda has hidden motives | 0.513 | Yes |
| 15 | URW: Russia has international support from a  | URW: Russian invasion has strong national sup | 0.505 | Yes |
| 16 | URW: Russian army is collapsing | URW: Russian army will lose all the occupied  | 0.505 | Yes |
| 17 | CC: Nuclear energy is not climate friendly | CC: Renewable energy is unreliable | 0.493 | Yes |
| 18 | URW: Discrediting Ukrainian military | URW: Discrediting Ukrainian nation and societ | 0.492 | Yes |
| 19 | URW: Sanctions imposed by Western countries w | URW: The conflict will increase the Ukrainian | 0.490 | Yes |
| 20 | URW: Praise of Russian President Vladimir Put | URW: Praise of Russian military might | 0.467 | Yes |
| 21 | CC: Nuclear energy is not climate friendly | CC: Renewable energy is costly | 0.461 | Yes |
| 22 | CC: Climate cycles are natural | CC: Human activities do not impact climate c | 0.459 | Yes |
| 23 | URW: The West is overreacting | URW: The West is weak | 0.458 | Yes |
| 24 | CC: Nuclear energy is not climate friendly | CC: Renewable energy is dangerous | 0.434 | Yes |
| 25 | URW: Russia actions in Ukraine are only self- | URW: The West is russophobic | 0.428 | Yes |
| 26 | CC: Methodologies/metrics used are unreliabl | CC: Scientific community is unreliable | 0.428 | Yes |
| 27 | URW: The West does not care about Ukraine, on | URW: The West is weak | 0.423 | Yes |
| 28 | CC: Criticism of international entities | CC: Criticism of the EU | 0.417 | Yes |
| 29 | CC: CO2 concentrations are too small to have | CC: Temperature increase does not have signi | 0.415 | Yes |
| 30 | URW: Discrediting Ukrainian government and of | URW: Discrediting Ukrainian military | 0.413 | Yes |

### Most Dissimilar Sibling Subnarratives (TF-IDF)

Subnarratives under the same parent narrative that are most different semantically. High confusion between these would be more surprising.

| Parent Narrative | Label A | Label B | Similarity |
|-----------------|---------|---------|------------|
| Downplaying climate change | Humans and nature will adapt to the | Weather suggests the trend is globa | 0.270 |
| Discrediting Ukraine | Discrediting Ukrainian government a | Ukraine is a hub for criminal activ | 0.275 |
| Downplaying climate change | Temperature increase does not have  | Weather suggests the trend is globa | 0.276 |
| Downplaying climate change | Sea levels are not rising | Weather suggests the trend is globa | 0.277 |
| Discrediting Ukraine | Discrediting Ukrainian government a | Ukraine is a puppet of the West | 0.280 |
| Downplaying climate change | CO2 concentrations are too small to | Weather suggests the trend is globa | 0.280 |
| Downplaying climate change | Humans and nature will adapt to the | Sea levels are not rising | 0.281 |
| Downplaying climate change | Sea levels are not rising | Temperature increase does not have  | 0.288 |
| Discrediting Ukraine | Discrediting Ukrainian nation and s | Ukraine is a hub for criminal activ | 0.290 |
| Discrediting Ukraine | Discrediting Ukrainian government a | Situation in Ukraine is hopeless | 0.291 |
| Discrediting Ukraine | Discrediting Ukrainian military | Ukraine is a hub for criminal activ | 0.292 |
| Overpraising the West | NATO will destroy Russia | The West belongs in the right side  | 0.292 |
| Downplaying climate change | CO2 concentrations are too small to | Sea levels are not rising | 0.292 |
| Downplaying climate change | Ice is not melting | Weather suggests the trend is globa | 0.295 |
| Praise of Russia | Praise of Russian President Vladimi | Russia is a guarantor of peace and  | 0.296 |

### Cross-Category Similarities (TF-IDF)

Pairs from different domains (URW vs CC) that are semantically similar.

| URW Subnarrative | CC Subnarrative | Similarity |
|-----------------|-----------------|------------|
| The EU is divided | Criticism of the EU | 0.175 |
| There is a real possibility that nuclear | Nuclear energy is not climate friendly | 0.123 |
| The West has the strongest international | Criticism of international entities | 0.114 |
| Ukraine is a hub for criminal activities | Human activities do not impact climate c | 0.111 |
| Discrediting Ukrainian government and of | Climate policies are ineffective | 0.097 |
| Russia has international support from a  | Criticism of international entities | 0.096 |
| Discrediting Ukrainian government and of | Climate policies have negative impact on | 0.093 |
| Russia will also attack other countries | Amplifying existing fears of global warm | 0.092 |
| Discrediting Ukrainian government and of | Climate policies are only for profit | 0.089 |
| By continuing the war we risk WWIII | Amplifying existing fears of global warm | 0.087 |
| Sanctions imposed by Western countries w | Climate policies have negative impact on | 0.086 |
| The West is russophobic | Climate policies have negative impact on | 0.085 |
| The West has the strongest international | Climate-related international relations  | 0.083 |
| There is a real possibility that nuclear | Amplifying existing fears of global warm | 0.082 |
| The West has the strongest international | Scientific community is unreliable | 0.079 |

---

## TF-IDF vs Embedding Comparison

This section highlights where the two methods disagree most, revealing pairs where embeddings capture semantic relationships that TF-IDF misses (and vice versa).

### Pairs Where Embeddings >> TF-IDF

These pairs are semantically related (high embedding similarity) but share few words (low TF-IDF). Embeddings correctly identify the relationship.

| Label A | Label B | Embedding Sim | TF-IDF Sim | Difference |
|---------|---------|---------------|------------|------------|
| Ad hominem attacks on key activists | Climate agenda has hidden motives | 0.790 | 0.012 | +0.777 |
| The West is weak | The West has the strongest internat | 0.797 | 0.070 | +0.727 |
| CO2 concentrations are too small to | Greenhouse effect/carbon dioxide do | 0.776 | 0.058 | +0.719 |
| Climate movement is corrupt | Criticism of political organization | 0.762 | 0.054 | +0.707 |
| Ad hominem attacks on key activists | Blaming global elites | 0.714 | 0.010 | +0.705 |
| CO2 is beneficial | Humans and nature will adapt to the | 0.729 | 0.035 | +0.695 |
| Climate policies are only for profi | Criticism of international entities | 0.753 | 0.061 | +0.692 |
| CO2 is beneficial | Greenhouse effect/carbon dioxide do | 0.723 | 0.032 | +0.692 |
| Climate policies are ineffective | Criticism of national governments | 0.755 | 0.065 | +0.690 |
| Climate policies are ineffective | Criticism of international entities | 0.755 | 0.066 | +0.690 |
| Climate policies are only for profi | Criticism of political organization | 0.743 | 0.054 | +0.689 |
| Climate policies are ineffective | Climate-related international relat | 0.762 | 0.075 | +0.687 |
| Nuclear energy is not climate frien | Climate policies are ineffective | 0.731 | 0.045 | +0.685 |
| Ukraine is the aggressor | Russia actions in Ukraine are only  | 0.752 | 0.068 | +0.683 |
| Nuclear energy is not climate frien | Climate policies are only for profi | 0.724 | 0.042 | +0.682 |
| The West are the aggressors | The West belongs in the right side  | 0.727 | 0.049 | +0.678 |
| Criticism of political organization | Blaming global elites | 0.700 | 0.024 | +0.676 |
| Climate policies are only for profi | Climate-related international relat | 0.744 | 0.069 | +0.674 |
| The West is weak | The West belongs in the right side  | 0.743 | 0.070 | +0.673 |
| Climate policies are ineffective | Criticism of political organization | 0.731 | 0.058 | +0.672 |

### Pairs Where TF-IDF >> Embeddings

These pairs share many words (high TF-IDF) but embeddings judge them less similar. Often due to structural bonus or negation patterns.

| Label A | Label B | TF-IDF Sim | Embedding Sim | Difference |
|---------|---------|------------|---------------|------------|
| Russian army is collapsing | Ukrainian army is collapsing | 0.976 | 0.913 | 0.063 |
| Scientific community is unreliable | The West has the strongest internat | 0.079 | 0.029 | 0.049 |
| CO2 concentrations are too small to | UA is anti-RU extremists | 0.038 | 0.000 | 0.038 |
| Climate policies have negative impa | Discrediting Ukrainian government a | 0.093 | 0.062 | 0.032 |
| CO2 is beneficial | Situation in Ukraine is hopeless | 0.030 | 0.000 | 0.030 |
| Climate policies are only for profi | Discrediting Ukrainian government a | 0.089 | 0.060 | 0.030 |
| Greenhouse effect/carbon dioxide do | Russia has international support fr | 0.021 | 0.000 | 0.021 |
| Data shows no temperature increase | Russia has international support fr | 0.020 | 0.000 | 0.020 |
| Human activities do not impact clim | Russia has international support fr | 0.023 | 0.007 | 0.015 |
| Temperature increase does not have  | UA is anti-RU extremists | 0.036 | 0.022 | 0.014 |
| Greenhouse effect/carbon dioxide do | Ukrainian army is collapsing | 0.014 | 0.002 | 0.013 |
| Greenhouse effect/carbon dioxide do | Russian invasion has strong nationa | 0.019 | 0.009 | 0.010 |
| Data shows no temperature increase | Russian invasion has strong nationa | 0.019 | 0.009 | 0.009 |
| Data shows no temperature increase | Greenhouse effect/carbon dioxide do | 0.860 | 0.856 | 0.005 |
| Temperature increase is beneficial | Discrediting Ukrainian military | 0.003 | 0.000 | 0.003 |
| Temperature increase is beneficial | Discrediting Ukrainian nation and s | 0.002 | 0.000 | 0.002 |
| CO2 concentrations are too small to | Praise of Russian military might | 0.002 | 0.000 | 0.002 |
| Temperature increase is beneficial | Ukrainian army is collapsing | 0.002 | 0.000 | 0.002 |
| CO2 concentrations are too small to | Discrediting Ukrainian nation and s | 0.002 | 0.000 | 0.002 |
| CO2 is beneficial | Discrediting Ukrainian military | 0.002 | 0.000 | 0.002 |

### Correlation Between Methods

| Metric | Value |
|--------|-------|
| Pearson r | 0.544 (p=3.20e-208) |
| Spearman rho | 0.774 (p=0.00e+00) |
| TF-IDF mean similarity | 0.036 |
| Embedding mean similarity | 0.340 |

Moderate correlation — the methods agree on some pairs but diverge on others. Embeddings provide richer semantic signal.


# Agora EMNLP 2025 Revision — Full Specification

**Document version:** 1.0 — April 2026
**Target venue:** EMNLP 2025 Long Paper (8 pages + references)
**Submission deadline:** May 20, 2026
**Budget:** €200 paid APIs + Llama 3.3 70B via HuggingFace Pro (free) + Colab Pro for local compute
**Base system:** INSALyon2 (AutoGen-based, SemEval-2025 Task 10, 3rd place English)

---

## Table of Contents

1. [Summary of Changes from SIGIR Submission](#1-summary)
2. [Paper Framing and Contributions](#2-framing)
3. [Reviewer Concerns Mapping](#3-reviewer-mapping)
4. [New Baselines and Controls](#4-baselines)
5. [Theory of Mind Framework](#5-tom)
6. [Prompt Enhancements](#6-prompts)
7. [Confusion-Aware Retrieval and Disambiguation](#7-retrieval)
8. [Evaluation Framework](#8-evaluation)
9. [BERTopic Keyword Extraction](#9-bertopic)
10. [Qualitative Error Analysis](#10-qualitative)
11. [Experimental Matrix and Budget](#11-experiments)
12. [Paper Structure](#12-structure)
13. [Timeline](#13-timeline)
14. [Risk Assessment](#14-risks)
15. [References to Add](#15-references)

---

## 1. Summary of Changes from SIGIR Submission {#1-summary}

The paper transforms from a controlled architectural comparison (short paper) into a comprehensive methodology paper (long paper) with three pillars:

| Aspect | SIGIR version | EMNLP version |
|---|---|---|
| Format | Short paper (4+1 pages) | Long paper (8 pages + refs) |
| Core claim | Consensus > refinement | ToM-informed consensus with confusion-aware evaluation |
| Baselines | Base, AC | Base, AC, Self-Consistency (NEW) |
| Architectures | Base, AC, Agora | + ToM reasoning chain, ToM-informed arbitration |
| Prompts | Fixed zero-shot, definition-guided | + BERTopic keywords, annotation guidelines, ToM chain |
| Evaluation | F1-sample, F1-macro | + hF, HCR, TCM + bistochastic normalisation, bootstrap CIs |
| Error analysis | Quantitative buckets (1 paragraph) | + Qualitative ToM-annotated analysis, confusion heatmaps |
| Retrieval | None | Confusion-aware hard-negative retrieval for disambiguation |
| Novelty framing | Empirical comparison | ToM framework for narrative classification + diagnostic methodology |

---

## 2. Paper Framing and Contributions {#2-framing}

### 2.1 Thesis statement

Propaganda narratives operate through Theory of Mind — they model reader beliefs and aim to manipulate them. Detecting narratives therefore requires reasoning about persuasive intent, not just topical content. We propose a ToM-informed framework for multilingual hierarchical narrative classification that diagnoses failure modes through confusion-aware evaluation and addresses them through intent-based reasoning and targeted retrieval.

### 2.2 Four contributions

**C1 — Controlled architectural comparison with proper baselines.** Single-agent, self-consistency (k=3), actor-critic, and multi-agent consensus voting across 5 LLMs, 5 languages, and 435+ runs. Self-consistency baseline disentangles multi-agent gains from simple resampling. (Addresses reviewers qbvq-W2, mVX8-W2, BqgP, and agentic review's top concern.)

**C2 — Theory of Mind framework for narrative classification.** ToM-informed reasoning chain that decomposes classification into presupposition identification → intent analysis → narrative mapping. ToM-informed arbitration for resolving multi-agent disagreements. ToM annotation of the narrative taxonomy mapping each narrative to its cognitive manipulation mechanism. (Novel contribution; no existing work applies ToM to propaganda classification.)

**C3 — Confusion-aware evaluation and diagnostic methodology.** Hierarchy-aware metrics (hF, HCR). Bistochastic normalisation of the Transport-based Confusion Matrix (TCM) to disentangle class similarity from distribution bias. Error severity distribution using LCA-based analysis. Cross-lingual BERTopic analysis of narrative keyword signatures. (Addresses reviewer concerns about evaluation depth and hierarchical consistency.)

**C4 — Confusion-guided prompt enhancement and retrieval.** BERTopic contrastive keywords for all narratives and sub-narratives. Confusion-aware hard-negative retrieval for disambiguation of confused pairs. Annotation-guideline-informed prompting. (Addresses over-prediction problem and intra-domain confusion.)

---

## 3. Reviewer Concerns Mapping {#3-reviewer-mapping}

### 3.1 SIGIR official reviews

| Reviewer | Concern | Section addressing it |
|---|---|---|
| Meta-review (i) | Homogeneous ensembles, need diversity | §2.2-C2 (ToM provides functional diversity), §5.3 (ToM arbitration as alternative to persona diversity) |
| Meta-review (ii) | Small dev set (20 docs/lang) | §8.5 (bootstrap CIs), §4.1 (train set for confusion analysis) |
| Meta-review (iii) | Ablation needed for language/LLM factors | §10.2 (interaction analysis from existing data) |
| Meta-review (iv) | Not enough novelty | §2.2-C2 (ToM framework), §2.2-C3 (evaluation methodology) |
| Meta-review (v) | IR connection | §7 (retrieval-based disambiguation), venue change to EMNLP |
| Meta-review (vi) | Architectural details weak | §3.2 (aggregation clarification), §6.3 (fuzzy matching description) |
| qbvq-W1 | Statistical power | §8.5 (bootstrap CIs), §8.6 (inter-run agreement) |
| qbvq-W2 | Homogeneous ensembles share biases | §4.1 (SC baseline), §5.3 (ToM arbitration for functional diversity) |
| qbvq-W5 | Fuzzy label matching unexplained | §6.3 |
| qbvq-W6 | "Best Official" in Table 2 unclear | §12 (editorial fix) |
| mVX8-W1 | No insight into why findings hold | §10.2 (interaction analysis), §10.1 (qualitative ToM analysis) |
| mVX8-W2 | No proposed method, just comparison | §2.2-C2 (ToM framework is a method), §2.2-C4 (retrieval is a method) |
| mVX8-W3 | Agent internals unexplained | §5 (ToM reasoning chain), §6 (prompt specifications) |
| mVX8-W4 | Language/LLM not research dimensions | §10.2 (interaction analysis), §9 (cross-lingual BERTopic) |
| mVX8-W5 | Editorial issues (task formulation placement) | §12 (restructured paper) |
| BqgP | IR relevance | §7 (retrieval), venue change |
| BqgP | Not adapted for HTC | §5.2 (ToM chain adapted to hierarchical structure), §8 (hierarchy-aware metrics) |
| BqgP | Figure 1 unclear | §12 (redesigned figure) |
| BqgP | 98 configs / 435 runs unexplained | §12 (footnote with arithmetic) |
| BqgP | t=0.7 results mentioned but not tabled | §12 (supplementary table or appendix) |

### 3.2 Agentic review (pre-submission)

| Concern | Section addressing it |
|---|---|
| Self-consistency baseline (top priority) | §4.1 |
| Hierarchical aggregation clarity | §6.4 |
| Budget-fair comparison | §4.2 |
| Actor-critic formalisation | §6.5 |
| Cost token breakdown | §11.3 |
| Bootstrap CIs | §8.5 |
| Hierarchical metrics | §8.1–8.4 |

---

## 4. New Baselines and Controls {#4-baselines}

### 4.1 Self-Consistency Baseline (SC)

**Purpose:** Disentangle multi-agent gains from simple resampling.

**Design:** Run k=3 independent samples from a single agent (same prompt, same backbone) and apply the same voting strategies (union, majority, intersection) as Agora.

**Key difference from Agora:** SC uses one agent sampled 3 times. Agora uses 3 parallel agent instances. At t=0, both produce variation due to floating-point non-determinism, so the comparison is fair.

**Implementation:**
- Use existing single-agent pipeline
- For each document, make 3 independent API calls (not batched — separate requests to ensure non-deterministic variation)
- Apply union/majority/intersection voting identically to Agora
- Compute all metrics: F1-sample, hF, HCR, error severity

**Models to run:** 
- DeepSeek V3: all 5 languages, t=0, 5 runs (primary)
- GPT-5 Nano: all 5 languages, t=0, 5 runs (validation)
- Llama 3.3 70B: all 5 languages, t=0, 5 runs (free, exploration)

**Expected cost:** DeepSeek ~€30, GPT-5 Nano ~€50, Llama free

**Analysis:**
- If Agora > SC: multi-agent architecture provides value beyond resampling → original claim holds
- If Agora ≈ SC: gains are from resampling → reframe as "consensus voting" (regardless of whether agents are independent instances or repeated samples)
- If SC > Agora: unexpected → investigate whether agent instances introduce correlated errors

### 4.2 Budget-Matched Comparisons

Report total API cost per architecture per document:

| Architecture | Calls per document | Relative cost |
|---|---|---|
| Base (single-agent) | ~3 (cat + narr + sub-narr) | 1.0× |
| SC (k=3) | ~9 | 3.0× |
| AC (with retries) | ~3–9 (depends on retries) | 1.0–3.0× |
| Agora (3 agents) | ~9 | 3.0× |
| Agora + ToM Stage 1 | ~10 | 3.3× |
| Agora + ToM + Disambiguation | ~10–11 | 3.3–3.7× |

SC and Agora are cost-matched by design (both use 3× the base cost). Include a cost-efficiency plot: F1/€ across architectures.

---

## 5. Theory of Mind Framework {#5-tom}

### 5.1 ToM Taxonomy Annotation (zero cost, manual)

For each of the 21 narratives, annotate:

| Field | Description | Example |
|---|---|---|
| Presupposed reader belief | What the text assumes the reader believes | "Reader trusts Western institutions" |
| Target cognitive mechanism | The type of mental state manipulation | Epistemic (trust erosion) / Emotional (fear) / Identity (in-group) |
| Intended belief change | What the text aims to make the reader believe | "Western institutions are hypocritical and untrustworthy" |
| Persuasive strategy | How the text achieves the change | Selective evidence, false equivalence, appeal to fear |

**Output:** A 21-row table (one per narrative) that becomes Table X in the paper and informs prompt design.

**Hypothesis to test:** Confused pairs from bis(TCM) will cluster by cognitive mechanism — narratives targeting the same mechanism (e.g., two fear-based narratives) will be more confused than narratives targeting different mechanisms, even within the same domain.

### 5.2 ToM Reasoning Chain (prompt enhancement — Option B)

**Architecture:** Two-stage pipeline applied to every document.

**Stage 1 — ToM Analysis (one LLM call, cached):**

```
Given the following news article, analyze its persuasive structure:

1. PRESUPPOSITIONS: What beliefs or assumptions does this text take 
   for granted about the reader? What does it assume the reader 
   already knows or believes?

2. INTENT: What cognitive or emotional effect does this text aim to 
   produce in the reader? Is it trying to induce fear, erode trust, 
   reinforce group identity, provoke outrage, or something else?

3. TARGET BELIEF CHANGE: After reading this text, what should the 
   reader believe that they didn't believe before?

Respond in JSON format:
{
  "presuppositions": ["..."],
  "intent": "...",
  "target_belief_change": "...",
  "primary_mechanism": "emotional|epistemic|identity|moral"
}
```

**Stage 2 — Classification (standard pipeline, enriched context):**

The ToM analysis from Stage 1 is prepended to the narrative classification prompt:

```
ToM Analysis of this article:
- Presupposed beliefs: {presuppositions}
- Persuasive intent: {intent}  
- Target belief change: {target_belief_change}
- Primary mechanism: {primary_mechanism}

Given this analysis, classify the article into narratives from the 
following taxonomy. Pay special attention to narratives that operate 
through the identified mechanism ({primary_mechanism}).

[... standard narrative classification prompt with definitions ...]
```

**Key design decisions:**
- Stage 1 runs once per document and is cached — all architectures (Base, SC, Agora) receive the same ToM analysis
- This isolates the effect of ToM reasoning from the architectural comparison
- Stage 1 output is also logged for qualitative analysis

**Cost:** One additional LLM call per document (~33% increase over base). For Agora: 1 ToM call + 3 agent calls = 4 calls vs. current 3 calls.

### 5.3 ToM-Informed Arbitration (disagreement resolution)

**Purpose:** When Agora agents disagree, use ToM reasoning to resolve rather than simple majority voting.

**Trigger:** Activated when agents produce different narrative label sets (i.e., no unanimous agreement on at least one label).

**Implementation:**

```
The following article was classified by 3 independent agents. They 
produced different narrative predictions:

Agent 1: {labels_1}
Agent 2: {labels_2}  
Agent 3: {labels_3}

ToM analysis of this article:
{cached_tom_analysis}

Points of disagreement: {disagreed_labels}

For each disagreed label, analyze:
- Is this label consistent with the article's identified persuasive 
  intent ({intent})?
- Does the article's presupposed reader belief ({presuppositions}) 
  align with the belief state targeted by this narrative?
- Could the disagreement reflect genuine ambiguity in the text's 
  persuasive strategy?

Produce a final classification with justification.
```

**Cost:** One additional call per document where disagreement occurs. Expected frequency: ~40–60% of documents (based on existing inter-agent agreement data).

**Comparison with existing AC:** The AC critic validates evidence for a single agent's prediction. The ToM arbiter resolves multi-agent disagreement using intent reasoning. These are complementary — the arbiter operates at a higher level (persuasive intent) than the critic (evidence faithfulness).

### 5.4 ToM as Evaluation/Analysis Tool

**ToM error taxonomy:** For each misclassification in the qualitative analysis, annotate:
- Did the model identify the correct topic but wrong intent? (ToM failure)
- Did the model identify the correct intent but wrong narrative? (Taxonomy mapping failure)
- Did the model fail at both? (Fundamental comprehension failure)

**ToM confusion analysis:** Cross-reference bis(TCM) confused pairs with the ToM taxonomy annotation (§5.1). Report whether confused pairs share cognitive mechanisms. If yes: "The dominant failure mode is mechanism-level confusion — models distinguish topics but not the persuasive strategies applied to them."

---

## 6. Prompt Enhancements {#6-prompts}

### 6.1 Prompt Condition Matrix

| Condition | Components | Cost vs. baseline |
|---|---|---|
| P0: Baseline | Current prompts (definitions + 1–2 fixed examples) | 1.0× |
| P1: Enhanced | P0 + BERTopic contrastive keywords + annotation guidelines | 1.0× (longer prompt, same calls) |
| P2: ToM chain | P1 + Stage 1 ToM analysis prepended | ~1.3× (one extra call) |
| P2+A: ToM + Arbitration | P2 + ToM arbitration on disagreements | ~1.3–1.7× |

All conditions share the same fuzzy label matching and post-processing.

### 6.2 BERTopic Keywords in Prompts

For each narrative and sub-narrative, add a line:

```
Narrative: "Amplifying war-related fears"
Definition: [existing definition]
Key indicators: {top-5 BERTopic keywords for this language}
Distinguished from: "Speculating war outcomes" by focus on 
  {contrastive keywords} rather than {other keywords}
```

Contrastive notes added only for top confused pairs identified by bis(TCM).

Keywords are language-specific (from per-language BERTopic runs). See §9.

### 6.3 Fuzzy Label Matching Description

**Current gap:** The paper mentions fuzzy matching without specifying the algorithm.

**Specification for the paper:**

```python
def fuzzy_match(predicted_label, valid_labels, threshold=80):
    """
    Match LLM output strings to valid taxonomy labels.
    
    Steps:
    1. Exact match (case-insensitive, stripped whitespace)
    2. Token overlap: compute Jaccard similarity on word tokens
    3. Edit distance: Levenshtein ratio via fuzzywuzzy
    4. Accept if max(token_overlap, levenshtein_ratio) >= threshold
    5. If no match above threshold, discard the prediction
    
    Returns: matched valid label or None
    """
```

Report in the paper: "We apply fuzzy label matching using token overlap and Levenshtein distance (threshold=80) to handle minor output variations (e.g., truncated label names, reordered words). Unmatched predictions are discarded."

### 6.4 Hierarchical Aggregation Clarification

**Add to Section 3.3 (Ensemble):**

"Voting is applied independently at each taxonomy level. First, agents vote on narrative labels; the selected narratives are determined by the chosen voting strategy (union/majority/intersection). Second, agents vote on sub-narrative labels, but only sub-narratives whose parent narrative was selected in the first step are retained. This two-stage filtering enforces hierarchical consistency by construction.

In Table 2, configuration names indicate voting strategies at each level: 'Narr. Union' applies union at the narrative level with intersection at the sub-narrative level; 'Full Inter.' applies intersection at both levels; 'Narr. Inter.' applies intersection at the narrative level with majority at the sub-narrative level."

### 6.5 Actor-Critic Formalisation

**Add to Section 3.2:**

"The critic evaluates each prediction against three binary criteria: (1) evidence accuracy — is the quoted text verbatim from the source? (2) relevance — does the evidence logically support the assigned label? (3) completeness — are there obvious narratives in the text that were not identified? A prediction passes if all three criteria are met. If any criterion fails, the critic generates structured feedback identifying the specific failure, and the actor receives this feedback along with the original document for revision. The loop terminates after either a successful validation or 3 unsuccessful retries, at which point the most recent actor output is used."

### 6.6 Annotation Guidelines Integration

**Source:** Stefanovitch et al. (2025), "Multilingual Characterization and Extraction of Narratives from Online News: Annotation Guidelines." 54-page companion document to SemEval-2025 Task 10. **Now available.**

The annotation guidelines contain three categories of information directly usable in our prompts: general annotation principles, per-narrative decision rules ("Instructions to Annotators"), and organizer-acknowledged confused pairs.

#### 6.6.1 General Annotation Principles (for all prompts)

These rules should be injected into every prompt as classification constraints:

```
Classification principles:
1. This is a MULTI-LABEL task: a document may contain multiple 
   narratives from the same domain. Assign ALL that apply.
2. Classify based SOLELY on information in the document. Do not 
   use external knowledge or personal opinions about the topics.
3. Annotation is hierarchical: first identify the coarse narrative, 
   then the fine-grained sub-narrative under it.
4. If a coarse narrative is present but no specific sub-narrative 
   fits, assign the coarse narrative with sub-narrative "Other".
5. If no narrative from the taxonomy applies to the document, 
   classify as "Other".
6. A narrative is present only if the text ACTIVELY PROMOTES or 
   PRESENTS it — merely mentioning a topic is not sufficient.
```

**Note on paragraph-level annotation:** The gold labels were created at paragraph level and aggregated to document level. Our system classifies at document level directly. This mismatch means our system faces a harder task (no paragraph decomposition). Worth noting in the Limitations section.

#### 6.6.2 URW Domain: Per-Narrative Decision Rules

Extract from "Instructions to Annotators" fields. These go into the P1 enhanced prompt alongside narrative definitions.

**Narrative 1 — Blaming the war on others:**
- "Look for direct or implied statements that shift blame away from Russia. Consider who is being held responsible for negative events or situations."
- Sub-narrative 1b (The West are the aggressors): "Look for direct or implied statements that mention that this conflict was a direct consequence of actions taken by the West."

**Narrative 2 — Discrediting Ukraine:**
- "Look for direct or implied statements that attack some aspect of the Ukrainian society."
- Sub-narrative 2b (Discrediting Ukrainian nation and society): **"Use this only in case that the subject of the attack is the people of Ukraine, or in case of generalizations."** ← Discriminates from 2d.
- Sub-narrative 2d (Discrediting Ukrainian government and officials): **"Use this only in case that the subject of the attack is the leaders of Ukraine or some of their specific policy decisions."** ← Discriminates from 2b.
- Sub-narrative 2e (Ukraine is a puppet of the West): **"Prefer this sub-Narrative over 'The West does not care about Ukraine, only about its interests', when the focus of the text revolves around Ukraine and its legitimacy is questioned."** ← KEY DISAMBIGUATION RULE. Directly addresses the confused pair identified in Lessons Learned (§11).
- Sub-narrative 2g (Ukraine is associated with nazism): **"This can go with discrediting Ukrainian nation, but should be used with any mention or hint of sympathy or association with (neo-)Nazism, historical or not."** ← Co-occurrence rule.

**Narrative 3 — Russia is the Victim:**
- "Look for narratives that depict Russia as suffering unjust consequences. Focus on language that evokes sympathy for Russia's position."

**Narrative 4 — Praise of Russia:**
- "Identify expressions of admiration, support, or positive evaluation of Russia. Consider both explicit praise and subtle commendation."
- Sub-narrative 4e (Russian invasion has strong national support): **"Use this only when there is mention to the Russian population or the segment of the population in Ukraine that supports Russia."** ← Discriminates from 4d (international support).

**Narrative 7 — Discrediting the West, Diplomacy:**
- "Look for criticism or negative portrayals of Western governments, leaders, or policies. Pay attention to language that suggests incompetence, hypocrisy, or malice."

**Narrative 8 — Negative Consequences for the West:**
- "Identify predictions or reports of negative impacts on Western nations. Consider both current and future consequences mentioned."

**Narrative 9 — Distrust towards Media:**
- "Look for language that undermines confidence in media sources. Pay attention to claims of bias, misinformation, or manipulation."

**Narrative 10 — Amplifying war-related fears:**
- "Identify language designed to elicit fear or concern about severe consequences. Consider both direct and implied threats mentioned."
- Sub-narrative 10c (Nuclear weapons): **"This narrative can potentially go in two directions, either claiming that West should not anger Russia, or that Russia should be stopped before they use them."** ← Bidirectional framing rule.

**Narrative 11 — Hidden plots:**
- "Look for narratives involving clandestine activities, secret agendas, or unproven allegations. Focus on claims that lack credible evidence and suggest hidden motives."

#### 6.6.3 CC Domain: Per-Narrative Decision Rules

The CC taxonomy has fewer explicit "Instructions to Annotators" fields — most narratives rely on definitions and examples alone. Key rules to extract from the definitions:

**Narrative 4 — Downplaying climate change:** Contains 8 sub-narratives with fine-grained distinctions (natural cycles vs. cooling trend vs. no impact vs. CO2 insignificant vs. not human-caused vs. ice not melting vs. sea levels stable vs. adaptation). The LLM must distinguish between these closely related denial arguments.

**Narrative 5 — Questioning the measurements and science:** Four sub-narratives distinguish between methodology critique, data denial, greenhouse effect denial, and community distrust. Decision rule: methodology/data issues (5a, 5b) vs. fundamental science denial (5c) vs. ad hominem on scientists (5d).

**Narrative 6 — Criticism of climate movement:** Three sub-narratives — alarmism, corruption, ad hominem. Note the overlap example: sub-narrative 6b uses the same example text as 6a, suggesting even the guidelines have ambiguity here.

#### 6.6.4 Organizer-Acknowledged Confused Pairs

From Section 11 "Lessons Learned" of the annotation guidelines:

| Confused Pair | Domain | Organizer Note |
|---|---|---|
| "Ukraine is a puppet of the West" ↔ "The West does not care about Ukraine, only about its interests" | URW | Explicitly flagged as requiring clarification. Decision rule: focus on Ukraine's legitimacy → puppet; focus on Western self-interest → doesn't care. |
| "Discrediting Ukrainian military" ↔ "Praise of Russian military might" | URW | "often found to overlap" — co-occurrence rather than confusion. Both may apply simultaneously. |
| "Methodologies/metrics unreliable" ↔ "Data shows no temperature increase" | CC | "may often co-occur" — again, co-occurrence rather than confusion. |

**Critical insight:** The organizers distinguish between *confusion* (annotators can't tell which label applies) and *overlap* (both labels genuinely apply). Our system should handle these differently:
- For confused pairs: disambiguation via contrastive retrieval and decision rules
- For overlapping pairs: allow multi-label prediction (both labels assigned)

The over-prediction problem may partly stem from the system not distinguishing these cases — it assigns overlapping labels when it should be assigning only one, or assigns confused labels when it should be assigning the other.

#### 6.6.5 Prompt Integration Strategy

**Layer 1 (all prompts):** Add general principles (§6.6.1) as a preamble to every classification prompt.

**Layer 2 (P1 enhanced):** For each narrative definition in the prompt, append the corresponding "Instructions to Annotators" as a decision rule. For confused pairs, add explicit disambiguation rules:

```
Narrative: "Ukraine is a puppet of the West"
Definition: [from taxonomy]
Decision rule: Prefer this over "The West does not care about 
Ukraine" when the focus is on Ukraine's legitimacy being questioned. 
If the focus is on Western self-interest, use "The West does not 
care about Ukraine" instead.
Key indicators: [BERTopic keywords]
```

**Layer 3 (disambiguation step):** For the retrieve-on-confusion pipeline, use the organizer-acknowledged confused pairs as the primary trigger set. The decision rules from the guidelines become part of the re-prompting context alongside hard-negative examples.

#### 6.6.6 Entity Framing as ToM Signal (exploratory)

The annotation guidelines include a rich Entity Framing taxonomy (Subtask 1) with protagonist/antagonist/innocent roles and 22 fine-grained sub-roles (Guardian, Martyr, Tyrant, Deceiver, Victim, etc.). While we don't use Subtask 1 labels directly, the entity roles are deeply connected to our ToM analysis:

- A text that frames Russia as "Guardian" and Ukraine as "Tyrant" is performing a specific ToM operation: presupposing reader belief in Russia's protective role.
- A text that frames Western media as "Deceiver" targets reader trust in information sources.

**For future work / journal extension:** Extract entity roles as an intermediate ToM feature. The combination of entity framing + narrative classification would give a richer picture of persuasive intent than either alone. This connects to Subtask 3 (Explanation of Narrative Classification), which requires evidence-based justification — exactly what our ToM Stage 1 analysis produces.

---

## 7. Confusion-Aware Retrieval and Disambiguation {#7-retrieval}

### 7.1 Embedding Index Construction

**Data:** 1,699 training articles with gold labels.

**Encoder:** Multilingual sentence transformer (e.g., `paraphrase-multilingual-mpnet-base-v2` or `multilingual-e5-large`). Run locally on Colab Pro — no API cost.

**Output:** Vector index (FAISS or similar) mapping each training article to its embedding + gold labels.

**Narrative prototypes:** Compute centroid embedding per narrative by averaging embeddings of all training documents labeled with that narrative.

### 7.2 Hard-Negative Mining

For each confused pair (A, B) identified by bis(TCM):

```python
def mine_hard_negatives(pair_A, pair_B, embeddings, labels, k=3):
    """
    Find training articles that are maximally informative for 
    disambiguating narrative A from narrative B.
    
    Hard negatives for A: documents labeled A that are closest 
    to B's prototype (i.e., A documents that "look like" B).
    
    Hard negatives for B: documents labeled B that are closest 
    to A's prototype.
    """
    proto_A = mean(embeddings[labels == A])
    proto_B = mean(embeddings[labels == B])
    
    # A docs closest to B prototype
    A_docs = embeddings[labels == A]
    A_dists_to_B = cosine_distance(A_docs, proto_B)
    hard_neg_A = A_docs[argsort(A_dists_to_B)[:k]]
    
    # B docs closest to A prototype  
    B_docs = embeddings[labels == B]
    B_dists_to_A = cosine_distance(B_docs, proto_A)
    hard_neg_B = B_docs[argsort(B_dists_to_A)[:k]]
    
    return hard_neg_A, hard_neg_B
```

**Pre-compute offline:** For each of the top-5 confused pairs per domain (from bis(TCM)), store 3 hard-negative examples per side. Total: ~10 pairs × 6 examples = ~60 pre-selected examples.

### 7.3 Retrieve-on-Confusion Pipeline

**At inference time:**

```
1. Classify document with standard (or ToM-enhanced) prompt
2. Check: do any predicted narratives fall in a confused pair?
   - Confused pairs: pre-computed from bis(TCM) analysis
3. If NO: accept prediction (no extra cost)
4. If YES:
   a. Retrieve pre-computed hard-negative examples for the confused pair
   b. Re-prompt with contrastive examples:
   
   "Your initial classification included [Narrative A]. This narrative 
   is often confused with [Narrative B]. Here are correctly classified 
   examples to help you distinguish them:
   
   Examples of Narrative A (NOT Narrative B):
   [hard_neg_A_1]: [brief excerpt] → Classified as A because [ToM: 
   targets fear of consequences]
   [hard_neg_A_2]: [brief excerpt] → Classified as A because [...]
   
   Examples of Narrative B (NOT Narrative A):  
   [hard_neg_B_1]: [brief excerpt] → Classified as B because [ToM: 
   targets distrust of institutions]
   [hard_neg_B_2]: [brief excerpt] → Classified as B because [...]
   
   Given these distinctions, re-evaluate: should the current article 
   be classified as A, B, both, or neither?"
```

**Cost:** One additional call per confused prediction. Expected frequency: ~30–40% of documents contain at least one confused narrative prediction.

### 7.4 Default Examples

For non-confused predictions, maintain 1 fixed example per narrative/sub-narrative (current setup). These defaults should also include brief ToM annotations:

```
Example: [article excerpt]
ToM: This article presupposes reader anxiety about energy prices 
and aims to amplify fear of economic collapse.
Classification: "Amplifying war-related fears" > "Economic 
consequences of the war"
```

---

## 8. Evaluation Framework {#8-evaluation}

### 8.1 Hierarchical F1 (hP / hR / hF)

As specified in the earlier metrics document. Three-level augmentation: Domain → Narrative → Sub-narrative + Root.

Implementation via HiClass library or custom code.

Report hF alongside F1-sample in all results tables.

### 8.2 Hierarchical Consistency Rate (HCR)

$$HCR = \frac{1}{|D|} \sum_{d \in D} \mathbb{1}\left[\forall s_{ij} \in \hat{Y}_d : n_i \in \hat{Y}_d\right]$$

Fraction of documents where every predicted sub-narrative has its parent narrative also predicted.

### 8.3 Bistochastic Confusion Analysis using TCM

**Pipeline:**

```
1. Extract TCM from predictions using the TCM library
   (github.com/johan140391/TCM)
   - Input: gold labels (binary multi-hot) + predicted labels (binary multi-hot)
   - Output: 21×21 TCM at narrative level

2. Apply bistochastic normalisation via IPF
   - Input: raw TCM + epsilon smoothing (1e-3)
   - Output: bis(TCM) — debiased confusion matrix

3. Compute all four normalisations for cross-normalisation diagnostic:
   - raw: distributional + structural confusion
   - row: P(predicted j | gold i) — recall structure  
   - col: P(gold i | predicted j) — precision structure
   - bis: pure structural confusion (distribution bias removed)

4. For architecture comparison, compute delta:
   Δ = bis(TCM_baseline) - bis(TCM_agora)
   - Positive Δ_ij: confusion between i,j decreased (improvement)
   - Negative Δ_ij: confusion increased (degradation)

5. Cross-normalisation diagnostic:
   - raw changes but bis doesn't → distributional improvement only 
     (less over-prediction, same underlying confusions)
   - bis changes → genuine structural improvement 
     (better narrative discrimination)
```

**Adaptation for multi-label:** Use binary multi-hot encoding for both gold and predicted labels. The TCM library handles multi-label natively via its TCMlab mode.

**Outputs for the paper:**
- bis(TCM) heatmap at narrative level (21×21) for baseline — Figure
- Delta heatmap (bis_before − bis_after) for best configuration — Figure
- Top-5 most confused pairs table — Table
- Cross-normalisation interpretation — 1 paragraph in analysis

**Visualization:** Use Paul Tol's colorblind-safe palette. Rows/columns sorted by domain (URW then CC), then by IC within domain. Overlay domain boundaries as thick lines.

### 8.4 Error Severity Distribution (LCA-based)

| Error Type | LCA Depth | Description |
|---|---|---|
| Sibling error | Parent narrative | Wrong sub-narrative, correct parent |
| Same-domain error | Domain (URW/CC) | Wrong narrative, correct domain |
| Cross-domain error | Root | Wrong domain entirely |
| Hallucination | None | "Other" label or fabricated |

Report distribution as percentages per architecture. Replace current qualitative error paragraph.

### 8.5 Bootstrap Confidence Intervals

For each metric (F1-sample, hF, HCR), per configuration:

```python
def bootstrap_ci(y_true, y_pred, metric_fn, n_bootstrap=1000, ci=0.95):
    """
    Resample documents with replacement, recompute metric, 
    take percentile CIs.
    """
    scores = []
    n = len(y_true)
    for _ in range(n_bootstrap):
        idx = np.random.choice(n, size=n, replace=True)
        score = metric_fn(y_true[idx], y_pred[idx])
        scores.append(score)
    lower = np.percentile(scores, (1-ci)/2 * 100)
    upper = np.percentile(scores, (1+ci)/2 * 100)
    return lower, upper
```

Report in results tables as subscript/superscript or in a supplementary table.

### 8.6 Inter-Run Agreement (Prediction Stability)

For each configuration with 5 runs:

```python
def inter_run_agreement(predictions_list):
    """
    Compute pairwise Jaccard similarity between runs' 
    prediction sets, averaged over documents.
    """
    n_runs = len(predictions_list)
    agreements = []
    for i in range(n_runs):
        for j in range(i+1, n_runs):
            for doc in range(n_docs):
                pred_i = set(predictions_list[i][doc])
                pred_j = set(predictions_list[j][doc])
                if pred_i or pred_j:
                    jacc = len(pred_i & pred_j) / len(pred_i | pred_j)
                    agreements.append(jacc)
    return np.mean(agreements)
```

**Expected finding:** Agora has higher inter-run agreement than Base, confirming that consensus voting reduces stochasticity. Report as a single summary number per architecture.

---

## 9. BERTopic Keyword Extraction {#9-bertopic}

### 9.1 Per-Language, Per-Narrative BERTopic

**Run on:** Colab Pro (no API cost).

**Procedure:**
1. For each language (BG, EN, HI, PT, RU):
   a. Group training documents by gold narrative label
   b. Run BERTopic on each narrative's documents to extract top-k keywords
   c. For each narrative, select top-10 keywords by c-TF-IDF score
2. For each confused pair (from bis(TCM)):
   a. Compute contrastive keywords: keywords unique to A vs. unique to B
   b. These become the "Distinguished from" annotations in prompts

**BERTopic configuration:**
- Embedding model: `paraphrase-multilingual-mpnet-base-v2` (same as retrieval index)
- UMAP: n_neighbors=15, n_components=5, min_dist=0.0
- HDBSCAN: min_cluster_size=5 (adjust for small narrative groups)
- For narratives with <10 documents: use TF-IDF only, skip clustering

### 9.2 Cross-Lingual Keyword Comparison

**Analysis (zero API cost):**
- For each narrative, compare top-10 keywords across languages
- Compute keyword overlap (Jaccard on translated keywords)
- Identify language-specific narrative markers vs. universal ones

**Expected finding:** Some narratives use universal keywords (translated equivalents appear in all languages), while others are linguistically adapted (different keywords per language). This informs whether multilingual processing matters beyond translation.

**Output for paper:** One analysis paragraph + optionally a small table showing keyword agreement scores per narrative across languages.

### 9.3 BERTopic for Sub-Narratives

Same procedure for the 64 sub-narratives where training data is sufficient (≥5 documents per sub-narrative per language). For sparse sub-narratives, aggregate across languages.

---

## 10. Qualitative Error Analysis {#10-qualitative}

### 10.1 Document-Level Case Studies

**Select 6–8 representative failure cases:**

Selection criteria:
- 2–3 documents where ALL architectures fail (shared ceiling)
- 2–3 documents where Agora succeeds but Base/AC fail (architecture benefit)
- 1–2 documents where ToM prompt helps but standard prompt fails (ToM benefit)
- Include at least one document per domain (URW, CC)
- Include at least one non-English document

**For each case, report:**

| Field | Content |
|---|---|
| Language | e.g., English |
| Gold labels | Narratives + sub-narratives |
| Base prediction | Labels + confidence (if available) |
| Agora prediction | Labels + voting pattern (which agents agreed/disagreed) |
| ToM analysis | Stage 1 output (presuppositions, intent, mechanism) |
| Error type | ToM failure / taxonomy mapping failure / comprehension failure |
| Why confusion occurs | Specific analysis of semantic overlap |

**Presentation:** As a structured case study box/figure in the paper, not a table. ~0.5 pages for 3 detailed cases, remainder in appendix.

### 10.2 Interaction Analysis (Language × Model × Architecture)

**From existing data (zero cost):**

1. **Language effect on Agora gain:**
   - Compute (Agora − Base) delta per language
   - Test: do morphologically complex languages (BG, RU) benefit more/less?
   - Test: does the language's training set size correlate with Agora gain?

2. **Model capability effect:**
   - Compute Agora delta per model
   - Test: do stronger models (GPT-5 Nano) benefit less from consensus?
   - Test: does the optimal voting strategy correlate with model capability?

3. **Voting strategy × language interaction:**
   - For each language, which voting strategy wins?
   - Does intersection work better for high multi-label density documents?

**Presentation:** 1–2 paragraphs in results section summarising patterns, with a supplementary table showing all deltas.

---

## 11. Experimental Matrix and Budget {#11-experiments}

### 11.1 Phase 0: Offline Preparation (zero cost)

| Task | Tool | Time estimate |
|---|---|---|
| TCM extraction + bistochastic normalisation | Python + TCM library | 2 hours |
| hF, HCR, error severity on existing 435 runs | Python + HiClass | 2 hours |
| Bootstrap CIs for all existing runs | Python | 1 hour |
| BERTopic: 5 languages × narratives/sub-narratives | Colab Pro | 4 hours |
| Sentence embeddings for 1,699 training articles | Colab Pro | 1 hour |
| Hard-negative mining for confused pairs | Python | 1 hour |
| ToM taxonomy annotation (21 narratives) | Manual | 3 hours |
| Annotation guidelines retrieval | Manual | 1 hour |
| Qualitative error analysis (6–8 cases) | Manual | 4 hours |
| Interaction analysis from existing data | Python | 2 hours |

### 11.2 Phase 1: Exploration on Llama (free)

| Experiment | Configs | Runs | Est. calls | Cost |
|---|---|---|---|---|
| SC baseline (k=3), all 5 langs | 5 | 5 | ~13,350 | Free |
| P0 vs P1 vs P2, single-agent, all 5 langs | 15 | 5 | ~13,350 | Free |
| Agora + ToM arbitration, all 5 langs | 5 | 5 | ~6,675+ | Free |
| **Total Phase 1** | | | ~33,375 | **Free** |

**Decision gate after Phase 1:** Which prompt condition (P0/P1/P2) works best on Llama? Does ToM arbitration help? Carry winners forward to Phase 2.

### 11.3 Phase 2: Confirmation on DeepSeek (~€80–100)

| Experiment | Configs | Runs | Est. cost |
|---|---|---|---|
| SC baseline (k=3), all 5 langs | 5 | 5 | ~€30 |
| Best prompt (from Phase 1), single-agent, all 5 langs | 5 | 5 | ~€15 |
| Best prompt + Agora, all 5 langs | 5 | 5 | ~€20 |
| Best prompt + Agora + ToM arbitration, 3 langs | 3 | 5 | ~€15 |
| Confusion-aware disambiguation, 3 langs | 3 | 5 | ~€10 |
| **Total Phase 2** | | | **~€90** |

### 11.4 Phase 3: Validation on GPT-5 Nano (~€60–80)

| Experiment | Configs | Runs | Est. cost |
|---|---|---|---|
| Best overall config, all 5 langs | 5 | 5 | ~€50 |
| ToM prompt on GPT-5 Nano, 3 langs (model capability test) | 3 | 5 | ~€20 |
| **Total Phase 3** | | | **~€70** |

### 11.5 Budget Summary

| Phase | Cost | Cumulative |
|---|---|---|
| Phase 0 (offline) | €0 | €0 |
| Phase 1 (Llama) | €0 | €0 |
| Phase 2 (DeepSeek) | ~€90 | ~€90 |
| Phase 3 (GPT-5 Nano) | ~€70 | ~€160 |
| Buffer | ~€40 | **~€200** |

### 11.6 Metrics Computed for Every New Run

For every new experiment, compute and log:
- F1-sample (SemEval primary metric)
- F1-macro at narrative level
- hP, hR, hF (hierarchical)
- HCR (hierarchical consistency)
- Error severity distribution (sibling / same-domain / cross-domain / hallucination)
- Inter-run agreement (across 5 runs)
- Per-document bootstrap 95% CIs for F1-sample and hF

Additionally, for selected configurations:
- TCM extraction + bistochastic normalisation
- ToM Stage 1 outputs (for qualitative analysis)
- Confidence scores (if added to prompts)

---

## 12. Paper Structure {#12-structure}

### Target: 8 pages + unlimited references (EMNLP long paper)

**Section 1 — Introduction (~0.75 pages)**

Open with narrative example (existing). Reframe: propaganda operates through Theory of Mind — modeling and manipulating reader beliefs. Current LLM-based approaches classify by topic, not by intent. We propose a ToM-informed framework combining confusion-aware evaluation, intent-based reasoning, and consensus voting.

State four contributions (§2.2).

**Section 2 — Related Work (~1.0 page)**

Expand from current 0.5 pages to cover:
- Hierarchical text classification (existing, keep)
- LLM ensembles and consensus voting (existing, keep)
- Self-refinement (existing, keep)
- Narrative/propaganda classification (existing, expand with SemEval-2025 context)
- Theory of Mind in LLMs (NEW: Yang et al. 2024, PersuasiveToM, SimToM, Farr et al. 2025)
- Hierarchy-aware evaluation (NEW: Amigó & Delgado 2022, Kiritchenko et al. 2006)
- Confusion matrix normalisation (NEW: Erbani et al. 2024, 2026)

**Section 3 — System Architecture (~1.5 pages)**

3.1 Task formulation (move from under architecture to its own subsection)
3.2 Baseline: hierarchical single-pass (existing, compressed)
3.3 Actor-Critic with formalised criteria (existing + §6.5)
3.4 Agora: multi-agent consensus with aggregation clarification (existing + §6.4)
3.5 ToM reasoning chain (NEW: §5.2)
3.6 ToM-informed arbitration (NEW: §5.3)
3.7 Confusion-aware retrieval and disambiguation (NEW: §7)

Figure 1: Redesigned to clearly show (a) common pipeline, (b)–(d) architecture instantiations, (e) ToM reasoning chain as an orthogonal enhancement, (f) disambiguation as a post-classification step.

**Section 4 — Experimental Setup (~1.0 page)**

4.1 Dataset: SemEval-2025 Task 10 (existing)
4.2 Models: 5 LLMs + configuration details (existing + Llama note)
4.3 Methods: Base, SC (NEW), AC, Agora, Agora+ToM, Agora+ToM+Disambiguation
4.4 Prompt conditions: P0, P1 (BERTopic + guidelines), P2 (ToM chain)
4.5 Evaluation: F1-sample, hF, HCR, TCM+bistochastic analysis, bootstrap CIs
4.6 Supervised baseline: mDeBERTa (existing, compressed)

Footnote: configuration arithmetic (98 configs = 5 models × 5 langs × 2 temps × [base + AC] + partial Agora configs + ...; 435 runs = configs × 5 runs each).

**Section 5 — Results (~1.5 pages)**

5.1 Architecture comparison (Table 1, expanded with hF column + SC row)
5.2 Prompt condition comparison (NEW table: P0 vs P1 vs P2 across models)
5.3 ToM arbitration results (NEW: improvement over standard Agora voting)
5.4 Disambiguation results (NEW: improvement on confused-pair documents)
5.5 Test set performance (Table 2, updated with best configuration)

**Section 6 — Analysis (~1.5 pages)**

6.1 Bistochastic confusion analysis (bis(TCM) heatmap + delta + cross-normalisation)
6.2 ToM error taxonomy (qualitative case studies, 3 detailed + 3 summarised)
6.3 BERTopic cross-lingual keyword analysis (1 paragraph + optional table)
6.4 Language × model interaction patterns
6.5 Cost-performance tradeoff (updated with new architectures)

**Section 7 — Discussion and Limitations (~0.5 pages)**

- Why ToM reasoning helps (or doesn't) for specific narrative types
- Limitations: dev set size, single taxonomy, commercial API reproducibility, homogeneous ensembles, paragraph-level vs. document-level annotation mismatch (gold labels annotated per paragraph then aggregated; our system classifies whole documents)
- Connection to perspectivism literature and annotation disagreement
- Future work: heterogeneous ensembles, adaptive per-language voting, retrieval-augmented evidence, journal extension

**Section 8 — Conclusion (~0.25 pages)**

Compressed summary of key findings and contributions.

### Figure and Table Budget

| Element | Location | New/Existing |
|---|---|---|
| Figure 1: Architecture overview (redesigned) | §3 | Redesigned |
| Figure 2: bis(TCM) heatmap (before) | §6.1 | New |
| Figure 3: bis(TCM) delta heatmap (before − after) | §6.1 | New |
| Table 1: Dev set results (+ hF, SC row) | §5.1 | Expanded |
| Table 2: Test set results (+ hF) | §5.5 | Expanded |
| Table 3: Prompt condition comparison | §5.2 | New |
| Table 4: ToM taxonomy annotation (21 narratives) | §6.2 or appendix | New |
| Table 5: Top confused pairs from bis(TCM) | §6.1 | New |

---

## 13. Timeline {#13-timeline}

### Week 1: April 5–12 (Offline preparation)

- [ ] TCM extraction + bistochastic analysis on existing predictions
- [ ] hF, HCR, bootstrap CIs on existing 435 runs
- [ ] BERTopic: run per language per narrative on Colab Pro
- [ ] Compute sentence embeddings for training set
- [ ] Mine hard negatives for confused pairs
- [ ] ToM taxonomy annotation (manual, 21 narratives)
- [x] Annotation guidelines retrieved — extract decision rules into prompt templates (DONE)
- [ ] Design prompt templates for P1 and P2 (incorporating §6.6 decision rules)
- [ ] Set up Llama 3.3 70B via HuggingFace Inference API

### Week 2: April 12–19 (Llama exploration)

- [ ] Run SC baseline on Llama, all 5 languages
- [ ] Run P0 vs P1 vs P2 on Llama single-agent, all 5 languages
- [ ] Run Agora + ToM arbitration on Llama, all 5 languages
- [ ] Compute all metrics for Llama runs
- [ ] Analyse Phase 1 results → select winning prompt condition
- [ ] Begin qualitative error analysis (6–8 cases)

### Week 3: April 19–26 (DeepSeek confirmation)

- [ ] Run SC baseline on DeepSeek, all 5 languages
- [ ] Run winning prompt + Agora + ToM on DeepSeek, all 5 languages
- [ ] Run disambiguation on DeepSeek, 3 languages
- [ ] Compute all metrics
- [ ] Complete qualitative error analysis
- [ ] Complete interaction analysis

### Week 4: April 26 – May 3 (GPT-5 Nano validation + analysis)

- [ ] Run best config on GPT-5 Nano, all 5 languages
- [ ] Run ToM prompt on GPT-5 Nano, 3 languages
- [ ] Compute all metrics
- [ ] Generate all figures (bis(TCM) heatmaps, confusion deltas)
- [ ] Cross-lingual BERTopic comparison analysis
- [ ] Decision: finalise which results go in main paper vs. appendix

### Weeks 5–6: May 3–17 (Writing)

- [ ] Restructure paper for EMNLP long format
- [ ] Write new sections: ToM framework, evaluation methodology, retrieval
- [ ] Integrate all new results into tables and figures
- [ ] Revise related work (add ToM, evaluation, confusion matrix sections)
- [ ] Redesign Figure 1
- [ ] Write analysis section with qualitative cases
- [ ] Internal review pass

### Week 7: May 17–20 (Polish and submit)

- [ ] Final editing pass
- [ ] Check all numbers, tables, figures for consistency
- [ ] Format for EMNLP submission
- [ ] Prepare supplementary material / appendix
- [ ] Submit by May 20

---

## 14. Risk Assessment {#14-risks}

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| SC baseline ties or beats Agora | Medium | High | Reframe: consensus voting valuable regardless of agent identity; ToM chain becomes the primary method contribution |
| ToM reasoning chain doesn't improve F1 | Medium | Medium | Report as analytical contribution (ToM error taxonomy); the chain may improve interpretability even without F1 gains |
| ToM arbitration degrades performance (over-revises like AC) | Medium | Medium | Compare carefully with standard voting; if arbiter fails, report and analyse why |
| Disambiguation adds cost but no F1 gain | Low-Medium | Low | Report confusion reduction even if F1 is flat; some confused pairs may be inherently ambiguous |
| Llama 3.3 70B is too weak to show prompt effects | Medium | Medium | Use Llama for exploration only; confirm on DeepSeek. If Llama shows no effect, skip directly to DeepSeek testing |
| HuggingFace Inference API rate limits slow Phase 1 | Medium | Medium | Batch requests; run overnight; consider dedicated endpoint if budget allows |
| BERTopic produces noisy keywords for sparse narratives | Medium | Low | Fallback to TF-IDF for narratives with <10 docs; validate keywords manually before including in prompts |
| €200 budget insufficient | Low | High | Buffer of €40; if needed, reduce GPT-5 Nano validation to 3 languages |
| bis(TCM) shows no meaningful differences between architectures | Low-Medium | Medium | Still publishable as methodology contribution; the diagnostic framework is valuable regardless |
| Paper exceeds 8 pages | High | Medium | Prioritise: main paper has core results; move BERTopic cross-lingual comparison, full case studies, and t=0.7 results to appendix |
| EMNLP reviewers find long paper still lacks novelty | Low-Medium | High | ToM framework + confusion-aware evaluation + retrieval-based disambiguation is three contributions; if any two land strongly, paper is defensible |

---

## 15. References to Add {#15-references}

### Must cite (core contributions)

1. Amigó, E. and Delgado, A. (2022). Evaluating Extreme Hierarchical Multi-label Classification. ACL 2022.
2. Kiritchenko, S. et al. (2006). Learning and Evaluation in the Presence of Class Hierarchies. AI 2006.
3. Erbani, J. et al. (2024). Confusion Matrices: A Unified Theory. IEEE Access. [TCM]
4. Erbani, J. et al. (2026). On the Normalization of Confusion Matrices. AISTATS 2026. [Bistochastic]
5. Yang, Y. et al. (2024). Detecting Conversational Mental Manipulation with Intent-Aware Prompting. [ToM for manipulation]
6. Wang, X. et al. (2023). Self-Consistency Improves Chain of Thought Reasoning. [SC baseline]
7. Farr, J. et al. (2025). Simulating Misinformation Vulnerabilities With Agent Personas. IEEE. [Mental schemas > demographics]
8. Stefanovitch, N. et al. (2025). Multilingual Characterization and Extraction of Narratives from Online News: Annotation Guidelines. SemEval-2025 Task 10 companion document. [Decision rules for confused pairs]

### Should cite (supporting evidence)

8. PersuasiveToM (2025). Benchmark for ToM in persuasive dialogues. arXiv:2502.21017.
9. Wilf, A. et al. (2024). SimToM: perspective-taking prompting. ACL 2024. [Think Twice]
10. Maurya, P. et al. (2025). Simulating Misinformation Propagation in Social Networks. arXiv:2511.10384.
11. Chuang, Y.-S. et al. (2024). Beyond Demographics: Aligning Role-playing LLM Agents Using Human Belief Networks. EMNLP Findings.
12. Huang, J. et al. (2024). LLMs Cannot Self-Correct Reasoning Yet. [AC failure motivation]
13. Asano, H. et al. (2025). Self-Refinement degrades classification. [AC failure]
14. Hu, T. and Collier, N. (2024). Quantifying the Persona Effect in LLM Simulations. ACL 2024.
15. INSALyon2 system description at SemEval-2025 Task 10. [Own prior work]

### Consider citing (if space)

16. Miceli, M. et al. (2006). BDI model of persuasion. [Theoretical ToM grounding]
17. Strachan, J. et al. (2024). Testing ToM in LLMs and humans. Nature Human Behaviour.
18. Van Dijk, T. (2006). Discourse and Manipulation. [Cognitive propaganda theory]
19. Dash, S. et al. (2025). Persona-assigned LLMs exhibit motivated reasoning. [Persona validation]
20. Brian, C. et al. (2025). MPCG: Multi-Round Persona-Conditioned Generation. EMNLP 2025.
21. Bassi, A. et al. (2025). Annotating the Annotators: Persuasion detection disagreement. ACL Findings.

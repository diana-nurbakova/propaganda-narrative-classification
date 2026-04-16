# Agora EMNLP Revision — Hierarchy-Aware Metrics Specification

**Document purpose:** Detailed implementation and writing plan for adding hierarchy-aware evaluation metrics to the Agora paper, addressing reviewer concerns about flat F1-sample evaluation and hierarchical consistency under aggregation.

**Target venue:** EMNLP 2025 Short Paper (4 pages + references)

---

## 1. Problem Statement

### 1.1 What the reviewer said

The reviewer raised two related concerns:

> "Hierarchical consistency under aggregation is underspecified: how the voting is applied at narrative vs. sub-narrative levels and how parent-child consistency is enforced post-aggregation could materially affect results."

> "The aggregation configuration names in Table 2 ('Narr. Union,' 'Full Inter.') need clearer definitions; it is unclear whether voting is per-level or joint across levels."

Additionally, the overall assessment flags that "clearer hierarchical aggregation details" are needed for the central claim to hold.

### 1.2 Why flat F1-sample is insufficient

The current paper uses two metrics:

- **F1-sample** (primary): Per-document F1 between predicted and gold label sets, averaged across documents. This is the SemEval-2025 Task 10 official metric.
- **F1-macro coarse** (secondary): Macro-averaged F1 at the narrative level only.

Neither metric accounts for the hierarchical structure of the taxonomy. Specifically:

1. **Equal penalty for all errors.** Predicting sibling sub-narrative `URW:Blaming_the_West` when gold is `URW:Western_hypocrisy` (same parent) is penalised identically to predicting `CC:Green_transition_harmful` (different domain entirely).
2. **No hierarchical consistency signal.** A system can predict sub-narrative `X:Y` without predicting narrative `X`, and this incoherence goes undetected.
3. **Cannot differentiate architectures on structural quality.** If multi-agent consensus produces more hierarchically coherent predictions than single-agent or actor-critic, flat F1 cannot reveal this.

### 1.3 Opportunity for the paper

Adding hierarchy-aware metrics serves three purposes:

- **Directly addresses the reviewer's concern** about hierarchical aggregation evaluation.
- **Strengthens the Agora contribution** by showing that consensus voting not only improves flat F1 but also produces more structurally coherent predictions.
- **Differentiates from SemEval system papers** that only report the official metric, positioning this as a methodologically stronger empirical study.

---

## 2. Metrics to Implement

### 2.1 Hierarchical Precision, Recall, F1 (hP / hR / hF)

**Source:** Kiritchenko et al. (2006), "Learning and Evaluation in the Presence of Class Hierarchies."

**Priority:** HIGH — must include. Widely recognised, simple to explain, directly interpretable.

**Definition:**

For each document $i$, let $\hat{C}_i$ be the set of predicted labels augmented with all ancestor nodes, and $C_i$ be the gold label set similarly augmented. Then:

$$hP = \frac{\sum_i |\hat{C}_i \cap C_i|}{\sum_i |\hat{C}_i|}$$

$$hR = \frac{\sum_i |\hat{C}_i \cap C_i|}{\sum_i |C_i|}$$

$$hF = \frac{2 \cdot hP \cdot hR}{hP + hR}$$

**How it works for our taxonomy:**

The SemEval-2025 Task 10 taxonomy has two levels:

```
Root
├── URW (Ukraine-Russia War)
│   ├── Narrative_1
│   │   ├── Sub-narrative_1a
│   │   └── Sub-narrative_1b
│   └── Narrative_2
│       └── Sub-narrative_2a
└── CC (Climate Change)
    ├── Narrative_3
    │   └── Sub-narrative_3a
    └── ...
```

Ancestor augmentation: if gold = `{URW:N1:S1a}`, the augmented gold set = `{Root, URW, N1, S1a}`. If predicted = `{URW:N1:S1b}`, augmented predicted = `{Root, URW, N1, S1b}`. The overlap = `{Root, URW, N1}` → 3 out of 4 gold nodes matched → hR benefits from partial credit. Contrast with flat F1 where this is a complete miss (0 overlap on the raw label).

**Key design decisions to document:**

- Whether to include the root node in augmentation (standard practice: yes, but it inflates scores uniformly so doesn't affect ranking). **Recommendation:** Include root for standard compliance, but it won't materially change comparisons.
- Whether to include the domain category (URW/CC) as a level. **Recommendation:** Yes — include it as level 0 (Category), level 1 (Narrative), level 2 (Sub-narrative). This gives the metric three levels to work with and rewards correct domain identification.
- How to handle multi-label: each document may have multiple narrative paths. Augment each path independently and take the union. This is standard for multi-label hF.

**Implementation:**

```python
# Using HiClass library (pip install hiclass)
from hiclass.metrics import f1 as hierarchical_f1
from hiclass.metrics import precision as hierarchical_precision
from hiclass.metrics import recall as hierarchical_recall

# Or manual implementation:
def augment_with_ancestors(labels, taxonomy):
    """
    labels: set of (narrative, sub_narrative) tuples
    taxonomy: dict mapping sub_narrative -> narrative -> category
    Returns: set of all nodes including ancestors
    """
    augmented = set()
    for narr, sub_narr in labels:
        category = taxonomy[narr]  # URW or CC
        augmented.update(["Root", category, narr, sub_narr])
    return augmented

def hierarchical_f1_sample(y_true, y_pred, taxonomy):
    """
    y_true: list of sets of (narrative, sub_narrative) tuples per document
    y_pred: same format
    Returns: micro-averaged hP, hR, hF
    """
    total_overlap = 0
    total_pred = 0
    total_gold = 0
    for gold, pred in zip(y_true, y_pred):
        aug_gold = augment_with_ancestors(gold, taxonomy)
        aug_pred = augment_with_ancestors(pred, taxonomy)
        total_overlap += len(aug_gold & aug_pred)
        total_pred += len(aug_pred)
        total_gold += len(aug_gold)
    hP = total_overlap / total_pred if total_pred > 0 else 0
    hR = total_overlap / total_gold if total_gold > 0 else 0
    hF = 2 * hP * hR / (hP + hR) if (hP + hR) > 0 else 0
    return hP, hR, hF
```

**What to report:** hF alongside F1-sample in Table 1 (dev set) and Table 2 (test set). A single additional column per table.


### 2.2 Information Contrast Model (ICM)

**Source:** Amigó & Delgado (2022), "Evaluating Extreme Hierarchical Multi-label Classification," ACL 2022.

**Priority:** MEDIUM — include if space permits. Theoretically strongest metric but requires more explanation.

**Definition:**

ICM is an information-theoretic metric based on the information content (IC) of category sets. For two category sets $A$ (gold) and $B$ (predicted):

$$ICM(A, B) = 2 \cdot IC(A) + 2 \cdot IC(B) - 3 \cdot IC(A \cup B)$$

where $IC(c) = -\log_2(P(c))$, and $P(c)$ is the descendant-inclusive frequency of category $c$ in the dataset.

For sets, IC is computed recursively using the lowest common subsumer:

$$IC(\{c_1, c_2, ..., c_n\}) = IC(c_1) + IC(\bigcup_{i \geq 2}\{c_i\}) - IC(\bigcup_{i \geq 2}\{lso(c_1, c_i)\})$$

**Why it matters for our paper:**

- ICM is the only metric that simultaneously satisfies category specificity (rare labels count more) and hierarchical proximity (near-miss errors are less penalised). This directly addresses the intra-domain confusion finding: if most errors are sibling sub-narratives (same parent), ICM will show this is "less wrong" than flat F1 suggests.
- For the class-imbalanced SemEval dataset (190:1 ratio), ICM naturally gives more weight to correctly identifying rare narratives.

**Key design decisions:**

- IC computation uses descendant-inclusive frequency: $P(c) = \frac{|\{d : c \in ancestors(labels(d))\}|}{|D|}$. For the root, $P(root) = 1.0$, so $IC(root) = 0$.
- Normalisation: raw ICM scores are unbounded. Standard practice is to normalise to [0,1] using $ICM_{norm} = \frac{ICM(A,B)}{ICM(A,A)}$ (treating $ICM(A,A)$ as the maximum score). **Recommendation:** Report normalised ICM.
- The LCS (lowest common subsumer) for our taxonomy: for two sub-narratives under the same parent narrative, LCS = that narrative. For two sub-narratives under different narratives but same domain, LCS = domain node. For cross-domain, LCS = root.

**Implementation:**

```python
import math
from collections import Counter

def compute_ic(node, node_frequencies, total_docs):
    """IC(c) = -log2(P(c)) where P(c) = descendant-inclusive freq / total"""
    freq = node_frequencies.get(node, 0)
    if freq == 0:
        return float('inf')  # never-seen node
    p = freq / total_docs
    return -math.log2(p)

def build_node_frequencies(y_true, taxonomy):
    """
    Count how many documents have each node (including ancestors)
    in their gold label set.
    """
    freq = Counter()
    for gold_labels in y_true:
        augmented = augment_with_ancestors(gold_labels, taxonomy)
        for node in augmented:
            freq[node] += 1
    return freq

def lcs(c1, c2, taxonomy):
    """Lowest common subsumer in the taxonomy tree."""
    ancestors_c1 = get_ancestors(c1, taxonomy)  # includes c1 itself
    ancestors_c2 = get_ancestors(c2, taxonomy)
    common = ancestors_c1 & ancestors_c2
    # Return the deepest common ancestor
    return max(common, key=lambda n: depth(n, taxonomy))

def ic_set(label_set, node_frequencies, total_docs, taxonomy):
    """Recursive IC computation for a set of labels."""
    if len(label_set) == 0:
        return 0
    if len(label_set) == 1:
        return compute_ic(list(label_set)[0], node_frequencies, total_docs)
    labels = list(label_set)
    c1 = labels[0]
    rest = set(labels[1:])
    lcs_set = {lcs(c1, ci, taxonomy) for ci in rest}
    return (compute_ic(c1, node_frequencies, total_docs)
            + ic_set(rest, node_frequencies, total_docs, taxonomy)
            - ic_set(lcs_set, node_frequencies, total_docs, taxonomy))

def icm_score(gold_set, pred_set, node_frequencies, total_docs, taxonomy):
    """ICM(A,B) = 2*IC(A) + 2*IC(B) - 3*IC(A ∪ B)"""
    ic_gold = ic_set(gold_set, node_frequencies, total_docs, taxonomy)
    ic_pred = ic_set(pred_set, node_frequencies, total_docs, taxonomy)
    ic_union = ic_set(gold_set | pred_set, node_frequencies, total_docs, taxonomy)
    return 2 * ic_gold + 2 * ic_pred - 3 * ic_union
```

**What to report:** If included, report micro-averaged normalised ICM in a supplementary column or in the analysis section only (not main table, to save space).


### 2.3 Hierarchical Consistency Rate (HCR)

**Source:** Novel for this paper (simple, intuitive metric addressing reviewer's exact question).

**Priority:** HIGH — must include. Directly answers the reviewer.

**Definition:**

$$HCR = \frac{1}{|D|} \sum_{d \in D} \mathbb{1}\left[\forall s_{ij} \in \hat{Y}_d : n_i \in \hat{Y}_d\right]$$

In plain English: the fraction of documents where every predicted sub-narrative has its parent narrative also predicted. A score of 1.0 means the system never predicts an orphan sub-narrative.

**Why it matters:**

- Directly addresses reviewer's Q1: "How is hierarchical consistency enforced during aggregation?"
- Allows quantitative comparison of consistency across architectures: we expect Agora (with intersection voting) to have higher HCR than single-agent because intersection voting is conservative and tends to agree on parent narratives.
- Actor-Critic may have lower HCR if the critic introduces inconsistency through partial revision.

**Implementation:**

```python
def hierarchical_consistency_rate(predictions, taxonomy):
    """
    predictions: list of dicts per document,
                 each with 'narratives': set and 'sub_narratives': set
    taxonomy: mapping sub_narrative -> parent_narrative
    Returns: float in [0, 1]
    """
    consistent_count = 0
    for pred in predictions:
        all_consistent = True
        for sub_narr in pred['sub_narratives']:
            parent = taxonomy[sub_narr]
            if parent not in pred['narratives']:
                all_consistent = False
                break
        if all_consistent:
            consistent_count += 1
    return consistent_count / len(predictions)
```

**What to report:** Single number per architecture × model × language, reported in the analysis section (Section 5.1). A compact summary: "Agora achieves HCR=X vs. Baseline HCR=Y vs. AC HCR=Z" with statistical test.


### 2.4 Error Severity Distribution (LCA-based)

**Source:** Derived from the LCA (Lowest Common Ancestor) distance in the taxonomy tree.

**Priority:** MEDIUM — enhances existing error analysis. Complements Section 5.1.

**Definition:**

For every false positive prediction, classify the error by its distance from the nearest gold label in the taxonomy tree:

| Error Type | LCA Depth | Description | Example |
|---|---|---|---|
| Sibling error | LCA = parent narrative | Predicted wrong sub-narrative under correct parent | Gold: `N1:S1a`, Pred: `N1:S1b` |
| Same-domain error | LCA = domain (URW/CC) | Predicted sub-narrative under wrong parent but same domain | Gold: `N1:S1a`, Pred: `N2:S2a` (both URW) |
| Cross-domain error | LCA = root | Predicted under wrong domain entirely | Gold: URW narrative, Pred: CC narrative |
| Hallucination | No LCA | Predicted "Other" or fabricated label | — |

**Connection to existing analysis:** The paper already reports "78–84% of errors are same-category" (which corresponds roughly to sibling + same-domain errors). This metric refines that analysis by separating sibling errors (near-miss, potentially acceptable) from same-domain errors (genuine confusion between distinct narratives).

**What to report:** Distribution as percentages per architecture. This replaces or extends the current error analysis paragraph in Section 5.1 with quantitative grounding. A small table or inline numbers.

---

## 3. Integration Plan for the Paper

### 3.1 Space budget (4-page EMNLP short paper)

The current SIGIR version is exactly 5 pages (4 content + 1 references). EMNLP short papers allow 4 pages + unlimited references. Space is extremely tight. Here is the allocation plan:

| Addition | Space needed | Location |
|---|---|---|
| hF column in Table 1 | ~0 extra (add column to existing table) | Section 5 |
| hF column in Table 2 | ~0 extra (add column to existing table) | Section 5 |
| HCR numbers in analysis | 2–3 sentences | Section 5.1 |
| Error severity distribution | Replace existing error paragraph (net ~0) | Section 5.1 |
| Metric definitions (hF + HCR) | 3–4 sentences in Evaluation Protocol | Section 4 |
| ICM (if included) | Footnote or supplementary mention only | Section 4 footnote |
| Hierarchical aggregation clarification | 1–2 sentences | Section 3.3 |

**Estimated net addition:** ~6–8 sentences total (~150–200 words). This is feasible within the 4-page limit if we tighten other sections slightly.

### 3.2 Changes to Section 4 (Experimental Setup → Evaluation Protocol)

**Current text (paraphrased):**
> "We report mean ± std for F1-samples (SemEval official metric) at both narrative and sub-narrative levels. Statistical significance via paired t-tests and Wilcoxon; effect sizes via Cohen's d."

**Proposed replacement:**

> "We report F1-samples (SemEval primary metric) and hierarchical F1 (hF; Kiritchenko et al., 2006), which augments predicted and gold label sets with ancestor nodes before computing overlap, giving partial credit when predictions fall within the correct narrative family. We additionally report hierarchical consistency rate (HCR): the fraction of documents where every predicted sub-narrative has its parent narrative also in the prediction set. Statistical significance is assessed via paired t-tests and Wilcoxon signed-rank tests; effect sizes via Cohen's d. Each experiment comprises 5 independent runs; we report mean ± standard deviation."

### 3.3 Changes to Section 3.3 (Ensemble: Multi-Agent Consensus Voting)

**Add after current description of union/majority/intersection:**

> "Voting is applied independently at each taxonomy level: first at the narrative level, then at the sub-narrative level. After aggregation, sub-narrative predictions are filtered to retain only those whose parent narrative was selected at the narrative-level vote. This enforces hierarchical consistency by construction. In Table 2, 'Narr. Union' applies union voting at the narrative level with intersection at the sub-narrative level; 'Full Inter.' applies intersection at both levels."

This directly addresses the reviewer's Q1 and the "Narr. Union / Full Inter." confusion.

### 3.4 Changes to Table 1 (Dev Set Results)

Add one column: **hF** (hierarchical F1-sample), computed with ancestor augmentation including the domain level (URW/CC → Narrative → Sub-narrative).

The column should be placed after the existing F1-sample columns. Format: `.XXX` (3 decimal places, matching current format).

**Expected outcome:** If Agora's gains are disproportionately from reducing cross-parent errors (which hF rewards), the hF improvement may be larger than the flat F1 improvement. If gains are uniform, hF improvement should track flat F1. Either finding is reportable.

### 3.5 Changes to Table 2 (Test Set Results)

Add **hF** column alongside existing F1-sample and F1 Macro columns.

### 3.6 Changes to Section 5.1 (Analysis → Error Analysis)

**Current error analysis paragraph (to be replaced/extended):**

The current text categorises false positives into same-narrative, same-category, cross-category, and hallucination buckets.

**Proposed replacement using error severity distribution:**

Replace with LCA-based severity classification (Section 2.4 above). Report the distribution for each architecture (Base, AC, Agora). Key narrative to build:

1. All architectures share the same dominant failure mode: sibling errors (sub-narratives under correct parent).
2. Agora reduces same-domain errors (wrong narrative within correct domain) more than it reduces sibling errors, suggesting consensus voting primarily helps with coarse-grained discrimination.
3. Actor-Critic shows higher cross-domain error rates in some configurations, consistent with critic-induced confusion.
4. Report HCR numbers here: "Agora achieves HCR of X (intersection) vs. Y (single-agent), confirming that consensus voting with post-aggregation filtering enforces hierarchical coherence."

### 3.7 Changes to Related Works (Section 2)

**Add one sentence** to the HTC paragraph:

> "Amigó and Delgado (2022) showed that flat metrics fail to capture hierarchical proximity and category specificity in extreme multi-label settings, motivating our use of hierarchy-aware evaluation alongside the task's official flat F1."

---

## 4. Experimental Execution Plan

### 4.1 Prerequisite: data preparation

1. **Build taxonomy tree.** Parse the SemEval-2025 Task 10 taxonomy into a tree structure with three levels: Domain (URW/CC) → Narrative (21 nodes) → Sub-narrative (64 nodes) + Root.
2. **Map all predictions to tree nodes.** Ensure existing prediction files (from all 435 runs) are mapped consistently to tree node IDs.
3. **Compute node frequencies.** For ICM, count descendant-inclusive frequencies from the training set gold labels.

### 4.2 Metric computation (no new experiments needed)

All metrics can be computed from existing prediction files. No new LLM runs required.

| Metric | Input | Compute time | Library |
|---|---|---|---|
| hP / hR / hF | Predictions + taxonomy tree | Minutes | HiClass or custom |
| ICM (normalised) | Predictions + taxonomy tree + node frequencies | Minutes | Custom implementation |
| HCR | Predictions + taxonomy tree | Seconds | Custom (trivial) |
| Error severity | False positives + taxonomy tree | Minutes | Custom |

### 4.3 Implementation steps

```
Step 1: taxonomy_tree.py
  - Parse SemEval taxonomy JSON/TSV into tree structure
  - Output: dict mapping each node to parent, children, depth, domain
  - Unit tests: verify 21 narratives, 64 sub-narratives, correct parentage

Step 2: hierarchical_metrics.py
  - Implement hP, hR, hF with ancestor augmentation
  - Implement HCR
  - Implement error severity classification
  - (Optional) Implement ICM with recursive IC computation
  - Unit tests: hand-computed examples matching known correct values

Step 3: compute_all_metrics.py
  - Load all 435 run prediction files
  - Compute hF, HCR, error severity for each run
  - Output: CSV with columns [model, language, temp, arch, config, run,
    f1_sample, hF, HCR, sibling_err%, same_domain_err%,
    cross_domain_err%, hallucination_err%]
  - Compute paired t-tests and Cohen's d for hF comparisons
    (same structure as existing F1-sample comparisons)

Step 4: format_tables.py
  - Generate LaTeX table rows for Tables 1 and 2 with hF column
  - Generate error severity distribution summary
  - Generate HCR summary statistics
```

### 4.4 Validation

- **Sanity check:** hF ≥ F1-sample for every configuration (because ancestor augmentation can only increase overlap, never decrease it). If this doesn't hold, there is a bug.
- **Monotonicity check:** if Agora > Baseline on flat F1, Agora should also be ≥ Baseline on hF. Violations would indicate that Agora gains come from non-hierarchical predictions.
- **HCR upper bound:** Agora with intersection voting + post-filtering should achieve HCR ≈ 1.0 by construction. If not, the filtering step has a bug.
- **Cross-reference with existing error analysis:** The current "78–84% same-category" finding should approximately equal sibling_err% + same_domain_err% from the new analysis.

---

## 5. Expected Outcomes and Narrative

### 5.1 Hypotheses (to confirm or refute)

**H1: hF improvement ≥ flat F1 improvement for Agora vs. Baseline.**
If Agora's consensus voting reduces cross-parent confusion (same-domain errors), the hF gain will be proportionally larger because hF gives partial credit for correct parent prediction. This would strengthen the paper's claim.

**H2: HCR(Agora) > HCR(Baseline) > HCR(Actor-Critic).**
Agora with intersection voting and post-filtering should produce the most hierarchically consistent predictions. Actor-Critic's revision loop may introduce orphan sub-narratives if the critic modifies narrative-level predictions without updating sub-narrative predictions.

**H3: Sibling errors dominate across all architectures.**
Consistent with existing finding. The new metric just quantifies this more precisely.

**H4: Agora reduces same-domain errors more than sibling errors.**
Consensus voting should help discriminate between narratives (coarse-grained) more than between sub-narratives (fine-grained), because narrative-level predictions have higher inter-agent agreement.

### 5.2 Narrative for the paper (regardless of outcome)

**If H1 confirmed:** "Hierarchy-aware evaluation reveals that Agora's gains extend beyond flat F1: consensus voting produces predictions that are not only more accurate but also more structurally coherent, as measured by hF (+X.X vs. +Y.Y on flat F1) and HCR (Z% vs. W%)."

**If H1 refuted (hF gain ≈ flat F1 gain):** "Hierarchy-aware evaluation confirms that Agora's improvements are uniform across the taxonomy, suggesting that consensus voting benefits fine-grained sub-narrative discrimination as much as coarse-grained narrative selection."

**If H2 partially refuted:** "Interestingly, Actor-Critic maintains high hierarchical consistency (HCR=X) despite lower flat F1, suggesting that evidence-grounded validation preserves structural coherence even when it degrades classification accuracy."

All outcomes are publishable. The key contribution is the richer evaluation, not a specific directional result.

---

## 6. References to Add

1. Amigó, E. and Delgado, A. (2022). Evaluating Extreme Hierarchical Multi-label Classification. In *Proceedings of ACL 2022*, pp. 5809–5819.
2. Kiritchenko, S., Matwin, S., Nock, R., and Famili, A.F. (2006). Learning and Evaluation in the Presence of Class Hierarchies: Application to Text Categorization. In *Advances in Artificial Intelligence*, pp. 395–406.
3. (Optional) Falis, M. et al. (2021). CoPHE: A Count-Preserving Hierarchical Evaluation Metric in Large-Scale Multi-Label Text Classification. In *Proceedings of EMNLP 2021*.
4. (Optional) Miranda, L.J. et al. (2023). HiClass: a Python Library for Local Hierarchical Classification Compatible with Scikit-learn. *JMLR*, 24(29), 1–17.

**Space note:** References 1 and 2 are essential. References 3 and 4 only if ICM or HiClass are explicitly used.

---

## 7. Relationship to Other Reviewer Concerns

This metrics update interacts with other planned revisions:

| Reviewer concern | How metrics update helps |
|---|---|
| Self-consistency baseline | hF and HCR should be computed for the self-consistency baseline too, enabling a four-way comparison (Base, SC, AC, Agora) on hierarchical quality |
| Budget fairness | hF per API dollar is a more meaningful efficiency metric than flat F1 per dollar, because it rewards structurally correct predictions |
| Aggregation clarity | The hierarchical aggregation clarification (Section 3.3) is a prerequisite for the HCR metric to be meaningful |
| Error analysis depth | Error severity distribution replaces the current qualitative paragraph with quantitative results |
| Statistical robustness | Bootstrap CIs can be computed for hF and HCR alongside flat F1, using the same per-document resampling |

---

## 8. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| hF shows no differentiation between architectures | Medium | Low | Still valuable as a negative result; report and discuss |
| ICM implementation has edge cases with empty predictions | Medium | Low | Handle gracefully with epsilon smoothing; validate on toy examples |
| Space overflow with additional columns | High | Medium | Drop ICM from main tables; keep hF only; move ICM to appendix if EMNLP allows |
| hF inflates all scores (due to ancestor augmentation) making differences look smaller in relative terms | Medium | Medium | Report absolute hF differences alongside relative improvement percentages |
| HCR = 1.0 for Agora (ceiling effect, no variance) | High | Low | Expected for intersection voting with filtering; report as confirmation that the mechanism works as designed, and contrast with other architectures |

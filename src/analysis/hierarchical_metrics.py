#!/usr/bin/env python3
"""
Hierarchy-aware evaluation metrics for the SemEval-2025 Task 10 narrative
taxonomy. Implements the metrics specified in
``specs/agora_hierarchical_metrics_spec.md``:

* Hierarchical Precision / Recall / F1 (hP, hR, hF) — Kiritchenko et al. 2006
* Hierarchical Consistency Rate (HCR)
* Error Severity Distribution (LCA-based: sibling / same-domain /
  cross-domain / hallucination)
* Inter-run agreement (Jaccard between runs)
* Information Contrast Model (ICM, normalised) — Amig\u00f3 & Delgado 2022
* Bootstrap CIs over documents

All functions take pre-parsed prediction sets that look like:

    docs = [
        {"narratives": {<narr_id>, ...}, "subnarratives": {<sub_id>, ...}},
        ...
    ]

Use ``taxonomy_tree.TaxonomyTree.parse_labels`` to obtain that representation
from raw label strings (see ``enhanced_experiment_report.py`` for an end-to-end
example).
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Callable, Dict, List, Optional, Sequence, Set, Tuple

import numpy as np

from .taxonomy_tree import OTHER, ROOT, TaxonomyTree


# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------

DocLabels = Dict[str, Set[str]]  # {"narratives": {...}, "subnarratives": {...}}


# ---------------------------------------------------------------------------
# Hierarchical F1 (hP / hR / hF)
# ---------------------------------------------------------------------------

def hierarchical_prf(
    y_true: Sequence[DocLabels],
    y_pred: Sequence[DocLabels],
    tree: TaxonomyTree,
    include_root: bool = True,
) -> Dict[str, float]:
    """Micro-averaged hierarchical Precision/Recall/F1 with ancestor augmentation.

    For each document, gold and predicted label sets are augmented with all
    ancestor nodes (Domain -> Root). Overlap on the augmented sets gives
    partial credit for predictions that fall within the correct narrative
    family.
    """
    overlap = 0
    n_pred = 0
    n_gold = 0
    for gold, pred in zip(y_true, y_pred):
        aug_g = tree.augment_with_ancestors(
            gold.get("narratives", set()),
            gold.get("subnarratives", set()),
            include_root=include_root,
        )
        aug_p = tree.augment_with_ancestors(
            pred.get("narratives", set()),
            pred.get("subnarratives", set()),
            include_root=include_root,
        )
        overlap += len(aug_g & aug_p)
        n_pred += len(aug_p)
        n_gold += len(aug_g)
    hP = overlap / n_pred if n_pred else 0.0
    hR = overlap / n_gold if n_gold else 0.0
    hF = (2 * hP * hR / (hP + hR)) if (hP + hR) else 0.0
    return {"hP": hP, "hR": hR, "hF": hF}


def hierarchical_f1_per_doc(
    y_true: Sequence[DocLabels],
    y_pred: Sequence[DocLabels],
    tree: TaxonomyTree,
    include_root: bool = True,
) -> List[float]:
    """Per-document hierarchical F1 scores (used for bootstrap CIs)."""
    out = []
    for gold, pred in zip(y_true, y_pred):
        aug_g = tree.augment_with_ancestors(
            gold.get("narratives", set()),
            gold.get("subnarratives", set()),
            include_root=include_root,
        )
        aug_p = tree.augment_with_ancestors(
            pred.get("narratives", set()),
            pred.get("subnarratives", set()),
            include_root=include_root,
        )
        if not aug_g and not aug_p:
            out.append(1.0)
            continue
        inter = len(aug_g & aug_p)
        if inter == 0:
            out.append(0.0)
            continue
        p = inter / len(aug_p) if aug_p else 0.0
        r = inter / len(aug_g) if aug_g else 0.0
        out.append(2 * p * r / (p + r) if (p + r) else 0.0)
    return out


# ---------------------------------------------------------------------------
# Hierarchical Consistency Rate (HCR)
# ---------------------------------------------------------------------------

def hierarchical_consistency_rate(
    y_pred: Sequence[DocLabels],
    tree: TaxonomyTree,
) -> float:
    """Fraction of documents where every predicted sub-narrative has its
    parent narrative also in the prediction set."""
    if not y_pred:
        return 0.0
    consistent = 0
    for pred in y_pred:
        narrs = pred.get("narratives", set())
        subs = pred.get("subnarratives", set())
        ok = True
        for sub in subs:
            parent = tree.parent.get(sub)
            if parent is None or parent not in narrs:
                ok = False
                break
        if ok:
            consistent += 1
    return consistent / len(y_pred)


# ---------------------------------------------------------------------------
# Error Severity Distribution (LCA-based)
# ---------------------------------------------------------------------------

ERROR_TYPES = ("sibling", "same_domain", "cross_domain", "hallucination")


def error_severity_distribution(
    y_true: Sequence[DocLabels],
    y_pred: Sequence[DocLabels],
    tree: TaxonomyTree,
    level: str = "subnarratives",
) -> Dict[str, float]:
    """Classify each false-positive prediction by LCA distance to the
    nearest gold label of the same level.

    Returns a dict with keys ``{sibling, same_domain, cross_domain,
    hallucination, total_fp}`` — the four error types as fractions summing
    to 1 (when ``total_fp > 0``), plus the raw FP count.
    """
    counts = Counter()
    for gold, pred in zip(y_true, y_pred):
        gold_set = gold.get(level, set())
        pred_set = pred.get(level, set())
        false_positives = pred_set - gold_set
        for fp in false_positives:
            if fp not in tree.parent:
                counts["hallucination"] += 1
                continue
            if not gold_set:
                counts["hallucination"] += 1
                continue
            best_lca_depth = -1
            for g in gold_set:
                lca = tree.lca(fp, g)
                if lca is None:
                    continue
                d = tree.depth.get(lca, -1)
                if d > best_lca_depth:
                    best_lca_depth = d
            if best_lca_depth < 0:
                counts["hallucination"] += 1
            elif best_lca_depth >= 2:
                # LCA is the parent narrative (depth 2) or deeper -> sibling
                counts["sibling"] += 1
            elif best_lca_depth == 1:
                # LCA is the domain
                counts["same_domain"] += 1
            else:
                # LCA is the root
                counts["cross_domain"] += 1

    total = sum(counts[k] for k in ERROR_TYPES)
    out = {k: (counts[k] / total if total else 0.0) for k in ERROR_TYPES}
    out["total_fp"] = total
    return out


# ---------------------------------------------------------------------------
# Inter-run agreement
# ---------------------------------------------------------------------------

def inter_run_agreement(
    runs: Sequence[Sequence[DocLabels]],
    level: str = "subnarratives",
) -> float:
    """Mean pairwise Jaccard similarity between runs over the same documents.

    ``runs`` is a list of runs; each run is a list of per-document label
    dicts in the same order. Empty-empty matches are scored 1.0 (consistent
    with usual Jaccard convention).
    """
    n_runs = len(runs)
    if n_runs < 2:
        return 1.0
    n_docs = min(len(r) for r in runs)
    sims: List[float] = []
    for i in range(n_runs):
        for j in range(i + 1, n_runs):
            for d in range(n_docs):
                a = runs[i][d].get(level, set())
                b = runs[j][d].get(level, set())
                if not a and not b:
                    sims.append(1.0)
                    continue
                inter = len(a & b)
                union = len(a | b)
                sims.append(inter / union if union else 1.0)
    return float(np.mean(sims)) if sims else 1.0


# ---------------------------------------------------------------------------
# Information Contrast Model (ICM)
# ---------------------------------------------------------------------------

def build_node_frequencies(
    y_true: Sequence[DocLabels],
    tree: TaxonomyTree,
) -> Tuple[Dict[str, int], int]:
    """Descendant-inclusive frequency for ICM. Counts how many documents
    contain each node (after ancestor augmentation)."""
    freq: Counter = Counter()
    for gold in y_true:
        aug = tree.augment_with_ancestors(
            gold.get("narratives", set()),
            gold.get("subnarratives", set()),
            include_root=True,
        )
        for node in aug:
            freq[node] += 1
    return dict(freq), len(y_true)


def _ic_node(node: str, freq: Dict[str, int], n_docs: int) -> float:
    f = freq.get(node, 0)
    if f == 0:
        # Smoothing — treat unseen nodes as one out of (n_docs + 1) docs.
        f = 1
        n = n_docs + 1
    else:
        n = n_docs
    p = f / n
    return -math.log2(p) if p > 0 else 0.0


def _ic_set(
    label_set: Set[str],
    freq: Dict[str, int],
    n_docs: int,
    tree: TaxonomyTree,
) -> float:
    """Recursive IC of a set of labels (Amig\u00f3 & Delgado 2022 eq. 4)."""
    labels = sorted(label_set)
    if not labels:
        return 0.0
    if len(labels) == 1:
        return _ic_node(labels[0], freq, n_docs)
    c1 = labels[0]
    rest = set(labels[1:])
    lcs_set = set()
    for ci in rest:
        l = tree.lca(c1, ci)
        if l is not None:
            lcs_set.add(l)
    return (
        _ic_node(c1, freq, n_docs)
        + _ic_set(rest, freq, n_docs, tree)
        - _ic_set(lcs_set, freq, n_docs, tree)
    )


def icm_score(
    gold: DocLabels,
    pred: DocLabels,
    freq: Dict[str, int],
    n_docs: int,
    tree: TaxonomyTree,
) -> float:
    """Single-document ICM score: ``2*IC(A) + 2*IC(B) - 3*IC(A \u222a B)``."""
    aug_g = tree.augment_with_ancestors(
        gold.get("narratives", set()),
        gold.get("subnarratives", set()),
        include_root=True,
    )
    aug_p = tree.augment_with_ancestors(
        pred.get("narratives", set()),
        pred.get("subnarratives", set()),
        include_root=True,
    )
    ic_g = _ic_set(aug_g, freq, n_docs, tree)
    ic_p = _ic_set(aug_p, freq, n_docs, tree)
    ic_u = _ic_set(aug_g | aug_p, freq, n_docs, tree)
    return 2 * ic_g + 2 * ic_p - 3 * ic_u


def icm_normalised(
    y_true: Sequence[DocLabels],
    y_pred: Sequence[DocLabels],
    tree: TaxonomyTree,
    freq: Optional[Dict[str, int]] = None,
    n_docs: Optional[int] = None,
) -> float:
    """Mean per-document normalised ICM, where the normaliser is
    ``ICM(gold, gold)``. Returns 0 if all gold sets are empty.
    """
    if freq is None or n_docs is None:
        freq, n_docs = build_node_frequencies(y_true, tree)
    scores: List[float] = []
    for g, p in zip(y_true, y_pred):
        denom = icm_score(g, g, freq, n_docs, tree)
        if denom <= 0:
            continue
        scores.append(icm_score(g, p, freq, n_docs, tree) / denom)
    return float(np.mean(scores)) if scores else 0.0


# ---------------------------------------------------------------------------
# Bootstrap confidence intervals
# ---------------------------------------------------------------------------

def bootstrap_ci(
    per_doc_scores: Sequence[float],
    n_bootstrap: int = 1000,
    ci: float = 0.95,
    seed: int = 0,
) -> Tuple[float, float]:
    """Percentile bootstrap CI from per-document scores."""
    arr = np.asarray(per_doc_scores, dtype=float)
    if arr.size == 0:
        return (0.0, 0.0)
    rng = np.random.default_rng(seed)
    n = arr.size
    means = np.empty(n_bootstrap)
    for i in range(n_bootstrap):
        idx = rng.integers(0, n, size=n)
        means[i] = arr[idx].mean()
    lo = float(np.percentile(means, (1 - ci) / 2 * 100))
    hi = float(np.percentile(means, (1 + ci) / 2 * 100))
    return lo, hi


def bootstrap_ci_paired(
    y_true: Sequence[DocLabels],
    y_pred: Sequence[DocLabels],
    metric_fn: Callable[
        [Sequence[DocLabels], Sequence[DocLabels]], float
    ],
    n_bootstrap: int = 500,
    ci: float = 0.95,
    seed: int = 0,
) -> Tuple[float, float]:
    """Bootstrap CI for an aggregate metric by resampling document indices."""
    n = len(y_true)
    if n == 0:
        return (0.0, 0.0)
    rng = np.random.default_rng(seed)
    means = np.empty(n_bootstrap)
    for i in range(n_bootstrap):
        idx = rng.integers(0, n, size=n)
        gt = [y_true[k] for k in idx]
        pr = [y_pred[k] for k in idx]
        means[i] = metric_fn(gt, pr)
    lo = float(np.percentile(means, (1 - ci) / 2 * 100))
    hi = float(np.percentile(means, (1 + ci) / 2 * 100))
    return lo, hi


# ---------------------------------------------------------------------------
# Convenience: compute the full hierarchical metric bundle for one run
# ---------------------------------------------------------------------------

def compute_hierarchical_bundle(
    y_true: Sequence[DocLabels],
    y_pred: Sequence[DocLabels],
    tree: TaxonomyTree,
    bootstrap: bool = True,
    n_bootstrap: int = 500,
) -> Dict[str, object]:
    """All hierarchical metrics for a single (gold, pred) pair of runs."""
    bundle: Dict[str, object] = {}
    prf = hierarchical_prf(y_true, y_pred, tree)
    bundle.update(prf)
    bundle["hcr"] = hierarchical_consistency_rate(y_pred, tree)
    bundle["error_severity_subnarr"] = error_severity_distribution(
        y_true, y_pred, tree, level="subnarratives"
    )
    bundle["error_severity_narr"] = error_severity_distribution(
        y_true, y_pred, tree, level="narratives"
    )
    per_doc = hierarchical_f1_per_doc(y_true, y_pred, tree)
    bundle["hF_per_doc_mean"] = float(np.mean(per_doc)) if per_doc else 0.0
    if bootstrap and per_doc:
        lo, hi = bootstrap_ci(per_doc, n_bootstrap=n_bootstrap)
        bundle["hF_ci"] = (lo, hi)
    return bundle


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from .taxonomy_tree import load_default_tree

    tree = load_default_tree()

    # Build a tiny synthetic example
    sub_id = lambda narr, sub: f"{narr}::{sub}"
    gold = [
        {
            "narratives": {"Discrediting Ukraine"},
            "subnarratives": {sub_id("Discrediting Ukraine", "Ukraine is a puppet of the West")},
        },
        {
            "narratives": {"Amplifying Climate Fears"},
            "subnarratives": set(),
        },
    ]
    pred_perfect = [dict(g) for g in gold]
    pred_sibling = [
        {
            "narratives": {"Discrediting Ukraine"},
            "subnarratives": {sub_id("Discrediting Ukraine", "Discrediting Ukrainian military")},
        },
        {
            "narratives": {"Amplifying Climate Fears"},
            "subnarratives": set(),
        },
    ]
    pred_cross = [
        {
            "narratives": {"Criticism of climate movement"},
            "subnarratives": set(),
        },
        {
            "narratives": {"Discrediting Ukraine"},
            "subnarratives": set(),
        },
    ]

    print("Perfect:", hierarchical_prf(gold, pred_perfect, tree))
    print("Sibling:", hierarchical_prf(gold, pred_sibling, tree))
    print("Cross:  ", hierarchical_prf(gold, pred_cross, tree))
    print(
        "Severity (sibling pred):",
        error_severity_distribution(gold, pred_sibling, tree),
    )
    print(
        "Severity (cross-domain pred):",
        error_severity_distribution(gold, pred_cross, tree),
    )
    print("HCR perfect:", hierarchical_consistency_rate(pred_perfect, tree))
    bad_hcr = [
        {
            "narratives": set(),
            "subnarratives": {sub_id("Discrediting Ukraine", "Ukraine is a puppet of the West")},
        }
    ]
    print("HCR orphan: ", hierarchical_consistency_rate(bad_hcr, tree))
    print("ICM perfect:", icm_normalised(gold, pred_perfect, tree))
    print("ICM sibling:", icm_normalised(gold, pred_sibling, tree))

#!/usr/bin/env python3
"""
Transport-based Confusion Matrix (TCM) construction and bistochastic
normalisation for the hierarchical narrative classification task.

Implements the analysis described in section 8.3 of
``specs/agora_emnlp_spec.md``:

* Build a multi-label TCM at the narrative level. Following the multi-label
  TCM convention, contributions from each document are normalised by the
  number of (gold, predicted) pairs so that each document contributes a
  total mass of 1 to the matrix (preventing documents with many labels from
  dominating).
* Provide four normalisations of that matrix:
    - ``raw``  — raw soft confusion mass
    - ``row``  — row-stochastic, P(predicted j | gold i) (recall structure)
    - ``col``  — column-stochastic, P(gold i | predicted j) (precision)
    - ``bis``  — bistochastic via Iterative Proportional Fitting (Sinkhorn-Knopp)
* Identify the top confused narrative pairs from the bistochastic matrix
  and compute structural deltas between two configurations.

The TCM library at github.com/johan140391/TCM is the canonical reference;
this is a from-scratch implementation that follows the same definitions and
is suitable for the dev-set sized matrices we work with (21 x 21 nodes).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from .hierarchical_metrics import DocLabels
from .taxonomy_tree import TaxonomyTree


# ---------------------------------------------------------------------------
# TCM construction
# ---------------------------------------------------------------------------

def build_narrative_tcm(
    y_true: Sequence[DocLabels],
    y_pred: Sequence[DocLabels],
    tree: TaxonomyTree,
    smoothing: float = 1e-3,
) -> Tuple[np.ndarray, List[str]]:
    """Build a multi-label TCM at the narrative level.

    For every document, each (gold_i, pred_j) pair contributes
    ``1 / (|gold| * |pred|)`` to ``M[i, j]``. Documents with no gold labels
    contribute their predictions to a "phantom" hallucination column, and
    vice versa for empty predictions — but here we restrict the matrix to
    actual narrative nodes for clarity, and discard those edge contributions
    (their counts are reported by ``error_severity_distribution`` instead).

    Args:
        y_true / y_pred: per-document parsed label dicts.
        tree: taxonomy tree (for the canonical narrative ordering).
        smoothing: small epsilon added to every cell — required by the
            bistochastic IPF step to prevent degenerate marginals.

    Returns:
        ``(matrix, narrative_order)`` where ``matrix`` has shape
        ``(N, N)`` and ``narrative_order`` lists the row/column labels.
    """
    # Order narratives by domain to make heatmaps interpretable
    narratives: List[str] = []
    for dom in tree.domains:
        narratives.extend(sorted(tree.raw[dom].keys()))
    idx = {n: i for i, n in enumerate(narratives)}
    n = len(narratives)
    M = np.zeros((n, n), dtype=float)

    for gold, pred in zip(y_true, y_pred):
        g = [x for x in gold.get("narratives", set()) if x in idx]
        p = [x for x in pred.get("narratives", set()) if x in idx]
        if not g or not p:
            continue
        w = 1.0 / (len(g) * len(p))
        for gi in g:
            for pj in p:
                M[idx[gi], idx[pj]] += w

    if smoothing > 0:
        M = M + smoothing
    return M, narratives


# ---------------------------------------------------------------------------
# Normalisations
# ---------------------------------------------------------------------------

def row_normalise(M: np.ndarray) -> np.ndarray:
    out = M / np.where(M.sum(axis=1, keepdims=True) > 0, M.sum(axis=1, keepdims=True), 1)
    return out


def col_normalise(M: np.ndarray) -> np.ndarray:
    out = M / np.where(M.sum(axis=0, keepdims=True) > 0, M.sum(axis=0, keepdims=True), 1)
    return out


def bistochastic_ipf(
    M: np.ndarray,
    max_iter: int = 1000,
    tol: float = 1e-9,
) -> np.ndarray:
    """Sinkhorn-Knopp / iterative proportional fitting.

    Returns a bistochastic matrix ``B`` with all row and column sums equal
    to 1, scaled from the input ``M`` by alternating row/column normalisation.
    Requires strictly positive ``M`` (use the smoothing in
    :func:`build_narrative_tcm`).
    """
    if (M <= 0).any():
        raise ValueError(
            "bistochastic_ipf requires a strictly positive matrix; "
            "use smoothing > 0 when building the TCM."
        )
    A = M.copy()
    n_rows, n_cols = A.shape
    if n_rows != n_cols:
        raise ValueError("bistochastic IPF requires a square matrix")
    target = 1.0  # row/col sums after IPF
    for _ in range(max_iter):
        row_sums = A.sum(axis=1, keepdims=True)
        A = A / row_sums * target
        col_sums = A.sum(axis=0, keepdims=True)
        A = A / col_sums * target
        if (np.abs(A.sum(axis=1) - target).max() < tol
                and np.abs(A.sum(axis=0) - target).max() < tol):
            break
    return A


def all_normalisations(M: np.ndarray) -> Dict[str, np.ndarray]:
    """Return ``raw``, ``row``, ``col``, ``bis`` views of the same TCM."""
    return {
        "raw": M.copy(),
        "row": row_normalise(M),
        "col": col_normalise(M),
        "bis": bistochastic_ipf(M),
    }


# ---------------------------------------------------------------------------
# Confused-pair extraction
# ---------------------------------------------------------------------------

@dataclass
class ConfusedPair:
    gold: str
    pred: str
    bis_mass: float
    raw_mass: float
    same_domain: bool

    def as_dict(self) -> Dict[str, object]:
        return {
            "gold": self.gold,
            "predicted": self.pred,
            "bis_mass": float(self.bis_mass),
            "raw_mass": float(self.raw_mass),
            "same_domain": bool(self.same_domain),
        }


def top_confused_pairs(
    M_raw: np.ndarray,
    M_bis: np.ndarray,
    narratives: Sequence[str],
    tree: TaxonomyTree,
    top_k: int = 10,
    exclude_diagonal: bool = True,
) -> List[ConfusedPair]:
    """Top off-diagonal confused pairs by bistochastic mass.

    Returns a list of ``ConfusedPair`` (gold, predicted) ordered by
    descending ``bis_mass``. We pick by ``bis`` to filter out distributional
    bias and report ``raw`` alongside for context.
    """
    n = len(narratives)
    candidates: List[ConfusedPair] = []
    for i in range(n):
        for j in range(n):
            if exclude_diagonal and i == j:
                continue
            same_dom = tree.domain_of.get(narratives[i]) == tree.domain_of.get(
                narratives[j]
            )
            candidates.append(
                ConfusedPair(
                    gold=narratives[i],
                    pred=narratives[j],
                    bis_mass=float(M_bis[i, j]),
                    raw_mass=float(M_raw[i, j]),
                    same_domain=same_dom,
                )
            )
    candidates.sort(key=lambda c: c.bis_mass, reverse=True)
    return candidates[:top_k]


def confusion_delta(
    M_bis_a: np.ndarray, M_bis_b: np.ndarray
) -> np.ndarray:
    """``\u0394 = bis(TCM_A) - bis(TCM_B)``.

    Positive entries indicate cells where A has more confusion than B.
    For "improvement of B over A" use ``bis_a - bis_b`` and look for
    positive cells = where B reduced confusion.
    """
    if M_bis_a.shape != M_bis_b.shape:
        raise ValueError("matrices must have the same shape for delta")
    return M_bis_a - M_bis_b


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from .taxonomy_tree import load_default_tree

    tree = load_default_tree()
    gold = [
        {"narratives": {"Discrediting Ukraine"}, "subnarratives": set()},
        {"narratives": {"Discrediting Ukraine"}, "subnarratives": set()},
        {"narratives": {"Russia is the Victim"}, "subnarratives": set()},
    ]
    pred = [
        {"narratives": {"Discrediting Ukraine"}, "subnarratives": set()},
        {"narratives": {"Russia is the Victim"}, "subnarratives": set()},
        {"narratives": {"Russia is the Victim"}, "subnarratives": set()},
    ]
    M, order = build_narrative_tcm(gold, pred, tree)
    norms = all_normalisations(M)
    print("raw row sums:", norms["raw"].sum(axis=1).round(3)[:5])
    print("bis row sums:", norms["bis"].sum(axis=1).round(3)[:5])
    print("bis col sums:", norms["bis"].sum(axis=0).round(3)[:5])
    pairs = top_confused_pairs(norms["raw"], norms["bis"], order, tree, top_k=3)
    for p in pairs:
        print(p)

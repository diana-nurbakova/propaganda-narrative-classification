#!/usr/bin/env python3
"""
Error Diagnosis — decompose and diagnose error sources across experiments.

Breaks down classification errors into over-prediction, under-prediction,
and confusion; computes per-narrative precision/recall profiles; identifies
systematic vs model-specific error patterns; and generates actionable
recommendations for prompt improvement.

Usage:

    python -m src.analysis.error_diagnosis \\
        --experiments-dir results/experiments/ \\
        --ground-truth-dir data/dev-documents_4_December/ \\
        --output results/analysis/errors/diagnosis.md \\
        --json-output results/analysis/errors/diagnosis.json \\
        --plot-dir results/analysis/errors/plots/ \\
        --languages EN
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

try:
    from .taxonomy_tree import TaxonomyTree, load_default_tree
    from .experiment_results_report import (
        discover_experiments,
        load_annotations,
        METHOD_DISPLAY,
        MODEL_DISPLAY,
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from src.analysis.taxonomy_tree import TaxonomyTree, load_default_tree
    from src.analysis.experiment_results_report import (
        discover_experiments,
        load_annotations,
        METHOD_DISPLAY,
        MODEL_DISPLAY,
    )


# ---------------------------------------------------------------------------
# Label normalisation helpers
# ---------------------------------------------------------------------------

def _normalise_narratives(
    raw_labels: List[str], tree: TaxonomyTree
) -> Set[str]:
    """Convert prefixed labels like 'URW: Discrediting Ukraine' to bare
    narrative names used in ``tree.narratives``."""
    out: Set[str] = set()
    for label in raw_labels:
        parsed = tree.parse_narrative_label(label)
        if parsed:
            out.add(parsed)
    return out


# ---------------------------------------------------------------------------
# Per-narrative precision / recall
# ---------------------------------------------------------------------------

def per_narrative_precision_recall(
    all_gold: List[Set[str]],
    all_pred: List[Set[str]],
    narratives: List[str],
) -> Dict[str, Dict[str, Any]]:
    """Compute per-narrative TP/FP/FN/P/R/F1 from multi-label sets.

    Args:
        all_gold: list of gold narrative sets (one per document).
        all_pred: list of predicted narrative sets.
        narratives: canonical narrative list.
    """
    result: Dict[str, Dict[str, Any]] = {}
    for n in narratives:
        tp = sum(1 for g, p in zip(all_gold, all_pred) if n in g and n in p)
        fp = sum(1 for g, p in zip(all_gold, all_pred) if n not in g and n in p)
        fn = sum(1 for g, p in zip(all_gold, all_pred) if n in g and n not in p)
        support = tp + fn
        p_val = tp / (tp + fp) if (tp + fp) else 0.0
        r_val = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * p_val * r_val / (p_val + r_val) if (p_val + r_val) else 0.0
        result[n] = {
            "tp": tp, "fp": fp, "fn": fn, "support": support,
            "precision": p_val, "recall": r_val, "f1": f1,
        }
    return result


# ---------------------------------------------------------------------------
# Error decomposition
# ---------------------------------------------------------------------------

def decompose_errors(
    all_gold: List[Set[str]],
    all_pred: List[Set[str]],
    tree: TaxonomyTree,
) -> Dict[str, Any]:
    """Classify each FP into confusion vs hallucination; track FNs.

    confusion: FP narrative shares domain with at least one gold narrative.
    hallucination: FP narrative is in a different domain from all gold, or
        the document has no gold narratives.
    """
    total_fp = 0
    total_fn = 0
    n_confusion = 0
    n_hallucination = 0
    n_cross_domain_fp = 0
    per_doc_label_diff: List[int] = []  # |pred| - |gold|

    for gold, pred in zip(all_gold, all_pred):
        fp = pred - gold
        fn = gold - pred
        total_fp += len(fp)
        total_fn += len(fn)
        per_doc_label_diff.append(len(pred) - len(gold))

        gold_domains = {tree.domain_of.get(n) for n in gold if tree.domain_of.get(n)}

        for fp_narr in fp:
            fp_dom = tree.domain_of.get(fp_narr)
            if fp_dom and fp_dom in gold_domains:
                n_confusion += 1
            elif fp_dom and gold_domains and fp_dom not in gold_domains:
                n_cross_domain_fp += 1
            else:
                n_hallucination += 1

    total_errs = total_fp + total_fn
    diffs = np.array(per_doc_label_diff)
    return {
        "total_fp": total_fp,
        "total_fn": total_fn,
        "total_errors": total_errs,
        "fp_confusion": n_confusion,
        "fp_cross_domain": n_cross_domain_fp,
        "fp_hallucination": n_hallucination,
        "fp_breakdown_pct": {
            "confusion": n_confusion / total_fp * 100 if total_fp else 0,
            "cross_domain": n_cross_domain_fp / total_fp * 100 if total_fp else 0,
            "hallucination": n_hallucination / total_fp * 100 if total_fp else 0,
        },
        "over_under_prediction": {
            "mean_diff": float(diffs.mean()) if len(diffs) else 0,
            "median_diff": float(np.median(diffs)) if len(diffs) else 0,
            "n_over": int((diffs > 0).sum()),
            "n_under": int((diffs < 0).sum()),
            "n_exact": int((diffs == 0).sum()),
        },
    }


# ---------------------------------------------------------------------------
# Confusion pair identification
# ---------------------------------------------------------------------------

def identify_confusion_pairs(
    all_gold: List[Set[str]],
    all_pred: List[Set[str]],
    tree: TaxonomyTree,
) -> List[Dict[str, Any]]:
    """For each FP, find the nearest gold narrative and record the pair."""
    pair_counts: Counter = Counter()

    for gold, pred in zip(all_gold, all_pred):
        fp = pred - gold
        if not gold or not fp:
            continue
        for fp_narr in fp:
            # Find nearest gold narrative (prefer same domain, then any)
            fp_dom = tree.domain_of.get(fp_narr)
            same_dom_gold = [g for g in gold if tree.domain_of.get(g) == fp_dom]
            if same_dom_gold:
                # If multiple gold in same domain, pick first alphabetically for consistency
                nearest = sorted(same_dom_gold)[0]
            else:
                nearest = sorted(gold)[0]
            pair_counts[(nearest, fp_narr)] += 1

    result = []
    for (gold_n, pred_n), count in pair_counts.most_common():
        same_dom = tree.domain_of.get(gold_n) == tree.domain_of.get(pred_n)
        result.append({
            "gold": gold_n,
            "predicted_as": pred_n,
            "count": count,
            "same_domain": same_dom,
        })
    return result


# ---------------------------------------------------------------------------
# Systematic vs model-specific analysis
# ---------------------------------------------------------------------------

def systematic_error_analysis(
    experiments: List[Dict[str, Any]],
    ground_truth_dir: str,
    tree: TaxonomyTree,
) -> Dict[str, Any]:
    """Per narrative, compute error rates per model.

    Returns per-narrative dict with per-model fn_rate and fp_rate,
    plus flags for systematic errors.
    """
    narratives = tree.narratives
    # Group experiments by model
    model_exps: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for exp in experiments:
        mk = exp["meta"].get("model_key", "unknown")
        display = MODEL_DISPLAY.get(mk, mk) if mk else "unknown"
        model_exps[display].append(exp)

    model_names = sorted(model_exps.keys())

    # Per-model, per-narrative aggregated counts
    per_model_narr: Dict[str, Dict[str, Dict[str, int]]] = {}
    for model, exps in model_exps.items():
        narr_counts: Dict[str, Dict[str, int]] = {
            n: {"tp": 0, "fp": 0, "fn": 0} for n in narratives
        }
        for exp in exps:
            lang = exp["meta"]["language"]
            gt_file = os.path.join(
                ground_truth_dir, lang, "subtask-3-dominant-narratives.txt"
            )
            if not os.path.exists(gt_file):
                continue
            ground_truth = load_annotations(gt_file)
            exp_dir = exp.get("dir", "")

            for run in exp["manifest"].get("runs", []):
                if run.get("status") != "success":
                    continue
                output_file = run.get("output_file") or ""
                if not os.path.exists(output_file):
                    fb = os.path.join(
                        exp_dir, f"run_{run.get('run_id', 1)}", "results.txt"
                    )
                    if os.path.exists(fb):
                        output_file = fb
                    else:
                        continue
                predictions = load_annotations(output_file)
                common = sorted(set(ground_truth.keys()) & set(predictions.keys()))
                for doc in common:
                    gold_n = _normalise_narratives(
                        ground_truth[doc].get("narratives", []), tree
                    )
                    pred_n = _normalise_narratives(
                        predictions[doc].get("narratives", []), tree
                    )
                    for n in narratives:
                        if n in gold_n and n in pred_n:
                            narr_counts[n]["tp"] += 1
                        elif n not in gold_n and n in pred_n:
                            narr_counts[n]["fp"] += 1
                        elif n in gold_n and n not in pred_n:
                            narr_counts[n]["fn"] += 1

        per_model_narr[model] = narr_counts

    # Compute rates and identify systematic errors
    per_narr_analysis: Dict[str, Dict[str, Any]] = {}
    for n in narratives:
        model_fn_rates: Dict[str, float] = {}
        model_fp_rates: Dict[str, float] = {}
        model_f1s: Dict[str, float] = {}

        for model in model_names:
            c = per_model_narr[model][n]
            support = c["tp"] + c["fn"]
            fn_rate = c["fn"] / support if support else 0
            fp_rate = c["fp"] / (c["tp"] + c["fp"]) if (c["tp"] + c["fp"]) else 0
            p = c["tp"] / (c["tp"] + c["fp"]) if (c["tp"] + c["fp"]) else 0
            r = c["tp"] / (c["tp"] + c["fn"]) if (c["tp"] + c["fn"]) else 0
            f1 = 2 * p * r / (p + r) if (p + r) else 0

            model_fn_rates[model] = fn_rate
            model_fp_rates[model] = fp_rate
            model_f1s[model] = f1

        fn_vals = list(model_fn_rates.values())
        fp_vals = list(model_fp_rates.values())

        # Flag: systematic if ALL models have FN rate > 0.4
        systematic_fn = all(v > 0.4 for v in fn_vals) if fn_vals else False
        # Flag: systematic FP if ALL models have FP rate > 0.3
        systematic_fp = all(v > 0.3 for v in fp_vals) if fp_vals else False

        per_narr_analysis[n] = {
            "model_fn_rates": model_fn_rates,
            "model_fp_rates": model_fp_rates,
            "model_f1s": model_f1s,
            "mean_fn_rate": float(np.mean(fn_vals)) if fn_vals else 0,
            "mean_fp_rate": float(np.mean(fp_vals)) if fp_vals else 0,
            "std_fn_rate": float(np.std(fn_vals)) if len(fn_vals) > 1 else 0,
            "std_fp_rate": float(np.std(fp_vals)) if len(fp_vals) > 1 else 0,
            "systematic_fn": systematic_fn,
            "systematic_fp": systematic_fp,
            "domain": tree.domain_of.get(n, "?"),
        }

    return {
        "model_names": model_names,
        "per_narrative": per_narr_analysis,
    }


# ---------------------------------------------------------------------------
# Recommendations
# ---------------------------------------------------------------------------

def generate_recommendations(
    per_narr_pr: Dict[str, Dict[str, Any]],
    confusion_pairs: List[Dict[str, Any]],
    systematic: Dict[str, Any],
) -> List[str]:
    """Generate actionable recommendations based on error patterns."""
    recs: List[str] = []

    # High FN narratives (recall problems)
    for n, stats in per_narr_pr.items():
        if stats["support"] > 0 and stats["recall"] < 0.4:
            recs.append(
                f"**Low recall for '{n}'** (R={stats['recall']:.2f}, "
                f"support={stats['support']}): Add more examples or strengthen "
                f"the definition in prompts."
            )

    # High FP narratives (precision problems)
    for n, stats in per_narr_pr.items():
        if stats["fp"] > 3 and stats["precision"] < 0.5:
            recs.append(
                f"**High over-prediction for '{n}'** (P={stats['precision']:.2f}, "
                f"FP={stats['fp']}): Tighten classification criteria or add "
                f"negative examples."
            )

    # Top confusion pairs
    for pair in confusion_pairs[:5]:
        if pair["count"] >= 3:
            recs.append(
                f"**Frequent confusion: '{pair['gold']}' predicted as "
                f"'{pair['predicted_as']}'** ({pair['count']} times"
                f"{', same domain' if pair['same_domain'] else ', CROSS domain'}): "
                f"Add disambiguation guidance between these two narratives."
            )

    # Systematic errors
    sys_narr = systematic.get("per_narrative", {})
    for n, stats in sys_narr.items():
        if stats.get("systematic_fn"):
            recs.append(
                f"**Systematic miss across ALL models: '{n}'** "
                f"(mean FN rate={stats['mean_fn_rate']:.2f}): "
                f"This narrative may need fundamentally different prompt strategy."
            )

    if not recs:
        recs.append("No critical error patterns detected.")

    return recs


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

def plot_error_decomposition(
    per_narr_pr: Dict[str, Dict[str, Any]],
    tree: TaxonomyTree,
    output_path: str,
) -> None:
    """Stacked bar chart: FP + FN per narrative."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return

    # Only show narratives with actual errors
    items = [(n, s) for n, s in per_narr_pr.items() if s["fp"] + s["fn"] > 0]
    if not items:
        return
    items.sort(key=lambda x: x[1]["fp"] + x[1]["fn"], reverse=True)
    items = items[:20]  # top 20

    names = [n[:35] + ("..." if len(n) > 35 else "") for n, _ in items]
    fps = [s["fp"] for _, s in items]
    fns = [s["fn"] for _, s in items]

    fig, ax = plt.subplots(figsize=(12, 7))
    y = range(len(names))
    ax.barh(y, fps, label="False Positives", color="salmon", edgecolor="black")
    ax.barh(y, [-fn for fn in fns], label="False Negatives", color="cornflowerblue", edgecolor="black")
    ax.set_yticks(list(y))
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel("Error count (FP right, FN left)")
    ax.set_title("Per-Narrative Error Decomposition")
    ax.legend()
    ax.axvline(0, color="black", linewidth=0.5)
    ax.invert_yaxis()
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [plot] error decomposition -> {output_path}")


def plot_precision_recall_scatter(
    per_narr_pr: Dict[str, Dict[str, Any]],
    output_path: str,
) -> None:
    """Scatter: precision vs recall per narrative, sized by support."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return

    items = [(n, s) for n, s in per_narr_pr.items() if s["support"] > 0]
    if not items:
        return

    names = [n for n, _ in items]
    precs = [s["precision"] for _, s in items]
    recs = [s["recall"] for _, s in items]
    supports = [max(s["support"], 1) for _, s in items]

    fig, ax = plt.subplots(figsize=(10, 8))
    scatter = ax.scatter(
        recs, precs,
        s=[s * 15 for s in supports],
        alpha=0.7, edgecolors="black", linewidth=0.5,
    )
    for i, name in enumerate(names):
        short = name[:25] + ("..." if len(name) > 25 else "")
        ax.annotate(short, (recs[i], precs[i]), fontsize=6, alpha=0.8,
                     xytext=(3, 3), textcoords="offset points")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Per-Narrative Precision vs Recall (size = support)")
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.plot([0, 1], [0, 1], "k--", alpha=0.3, label="P=R line")
    ax.legend()
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [plot] P-R scatter -> {output_path}")


def plot_systematic_heatmap(
    systematic: Dict[str, Any],
    output_path: str,
) -> None:
    """Heatmap: narratives x models, colored by F1."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return

    model_names = systematic.get("model_names", [])
    per_narr = systematic.get("per_narrative", {})
    if not model_names or not per_narr:
        return

    # Only narratives with nonzero activity
    narr_names = [n for n, s in per_narr.items()
                  if any(s["model_f1s"].get(m, 0) > 0 or
                         s.get("mean_fn_rate", 0) > 0
                         for m in model_names)]
    if not narr_names:
        return

    matrix = np.zeros((len(narr_names), len(model_names)))
    for i, n in enumerate(narr_names):
        for j, m in enumerate(model_names):
            matrix[i, j] = per_narr[n]["model_f1s"].get(m, 0)

    short_narr = [n[:30] + ("..." if len(n) > 30 else "") for n in narr_names]

    fig, ax = plt.subplots(figsize=(max(8, len(model_names) * 2), max(8, len(narr_names) * 0.35)))
    im = ax.imshow(matrix, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(model_names)))
    ax.set_yticks(range(len(short_narr)))
    ax.set_xticklabels(model_names, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(short_narr, fontsize=7)
    # Annotate
    for i in range(len(narr_names)):
        for j in range(len(model_names)):
            v = matrix[i, j]
            color = "white" if v < 0.4 else "black"
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=6, color=color)
    ax.set_title("Per-Narrative F1 by Model")
    plt.colorbar(im, ax=ax, label="F1")
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [plot] systematic heatmap -> {output_path}")


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------

def render_report(
    decomposition: Dict[str, Any],
    per_narr_pr: Dict[str, Dict[str, Any]],
    confusion_pairs: List[Dict[str, Any]],
    systematic: Dict[str, Any],
    recommendations: List[str],
    n_docs: int,
    n_experiments: int,
) -> str:
    lines: List[str] = []
    a = lines.append

    a("# Error Diagnosis Report")
    a("")
    a(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    a("")
    a(f"Analyzed **{n_experiments}** experiments across **{n_docs}** documents.")
    a("")

    # Error decomposition summary
    a("## Error Decomposition")
    a("")
    d = decomposition
    a(f"- Total false positives (FP): **{d['total_fp']}**")
    a(f"  - Same-domain confusion: {d['fp_confusion']} ({d['fp_breakdown_pct']['confusion']:.1f}%)")
    a(f"  - Cross-domain FP: {d['fp_cross_domain']} ({d['fp_breakdown_pct']['cross_domain']:.1f}%)")
    a(f"  - Hallucination: {d['fp_hallucination']} ({d['fp_breakdown_pct']['hallucination']:.1f}%)")
    a(f"- Total false negatives (FN): **{d['total_fn']}**")
    a(f"- FP/FN ratio: **{d['total_fp'] / d['total_fn']:.2f}**" if d["total_fn"] else "- FP/FN ratio: n/a")
    a("")

    ou = d["over_under_prediction"]
    a("### Over/Under-Prediction Profile")
    a("")
    a(f"- Mean |pred| - |gold| per doc: **{ou['mean_diff']:+.2f}**")
    a(f"- Over-predicting docs: **{ou['n_over']}**, Under-predicting: **{ou['n_under']}**, Exact: **{ou['n_exact']}**")
    a(f"- {'System tends to OVER-PREDICT' if ou['mean_diff'] > 0.1 else 'System tends to UNDER-PREDICT' if ou['mean_diff'] < -0.1 else 'Prediction count roughly balanced'}")
    a("")

    # Per-narrative table
    a("## Per-Narrative Error Profile")
    a("")
    a("| Narrative | Support | TP | FP | FN | Precision | Recall | F1 |")
    a("|-----------|---------|----|----|----|-----------|---------|----|")
    sorted_narrs = sorted(
        per_narr_pr.items(),
        key=lambda x: x[1]["support"],
        reverse=True,
    )
    for n, s in sorted_narrs:
        if s["support"] == 0 and s["fp"] == 0:
            continue
        a(f"| {n} | {s['support']} | {s['tp']} | {s['fp']} | {s['fn']} | "
          f"{s['precision']:.2f} | {s['recall']:.2f} | {s['f1']:.2f} |")
    a("")

    # Top confusion pairs
    a("## Top Confusion Pairs")
    a("")
    a("Each row shows a gold narrative being predicted as a different narrative.")
    a("")
    a("| # | Gold Narrative | Predicted As | Count | Same Domain |")
    a("|---|----------------|-------------|-------|-------------|")
    for i, p in enumerate(confusion_pairs[:20], 1):
        dom = "yes" if p["same_domain"] else "NO"
        a(f"| {i} | {p['gold']} | {p['predicted_as']} | {p['count']} | {dom} |")
    a("")

    # Systematic errors
    sys_narr = systematic.get("per_narrative", {})
    model_names = systematic.get("model_names", [])

    systematic_fn_narrs = [
        (n, s) for n, s in sys_narr.items() if s.get("systematic_fn")
    ]
    systematic_fp_narrs = [
        (n, s) for n, s in sys_narr.items() if s.get("systematic_fp")
    ]

    if systematic_fn_narrs or systematic_fp_narrs:
        a("## Systematic Errors (consistent across ALL models)")
        a("")
        if systematic_fn_narrs:
            a("### Systematically Missed Narratives (high FN rate everywhere)")
            a("")
            a("| Narrative | Mean FN Rate | " + " | ".join(model_names) + " |")
            a("|-----------|-------------|" + "|".join(["------" for _ in model_names]) + "|")
            for n, s in sorted(systematic_fn_narrs, key=lambda x: x[1]["mean_fn_rate"], reverse=True):
                vals = " | ".join(f"{s['model_fn_rates'].get(m, 0):.2f}" for m in model_names)
                a(f"| {n} | {s['mean_fn_rate']:.2f} | {vals} |")
            a("")

        if systematic_fp_narrs:
            a("### Systematically Over-Predicted Narratives (high FP rate everywhere)")
            a("")
            a("| Narrative | Mean FP Rate | " + " | ".join(model_names) + " |")
            a("|-----------|-------------|" + "|".join(["------" for _ in model_names]) + "|")
            for n, s in sorted(systematic_fp_narrs, key=lambda x: x[1]["mean_fp_rate"], reverse=True):
                vals = " | ".join(f"{s['model_fp_rates'].get(m, 0):.2f}" for m in model_names)
                a(f"| {n} | {s['mean_fp_rate']:.2f} | {vals} |")
            a("")

    # Model-specific patterns (high variance narratives)
    high_var = [
        (n, s) for n, s in sys_narr.items()
        if s["std_fn_rate"] > 0.2 and s.get("mean_fn_rate", 0) > 0.1
    ]
    if high_var:
        a("## Model-Specific Error Patterns (high cross-model variance)")
        a("")
        a("| Narrative | Mean FN Rate | Std FN Rate | " + " | ".join(model_names) + " |")
        a("|-----------|-------------|------------|" + "|".join(["------" for _ in model_names]) + "|")
        for n, s in sorted(high_var, key=lambda x: x[1]["std_fn_rate"], reverse=True)[:15]:
            vals = " | ".join(f"{s['model_fn_rates'].get(m, 0):.2f}" for m in model_names)
            a(f"| {n} | {s['mean_fn_rate']:.2f} | {s['std_fn_rate']:.2f} | {vals} |")
        a("")

    # Recommendations
    a("## Actionable Recommendations")
    a("")
    for i, rec in enumerate(recommendations, 1):
        a(f"{i}. {rec}")
    a("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Diagnose error sources across experiments."
    )
    parser.add_argument("--experiments-dir", default="results/experiments/")
    parser.add_argument("--ground-truth-dir", default="data/dev-documents_4_December/")
    parser.add_argument("--languages", nargs="*", default=None)
    parser.add_argument("--methods", nargs="*", default=None)
    parser.add_argument("--models", nargs="*", default=None)
    parser.add_argument("--output", required=True, help="Output Markdown file.")
    parser.add_argument("--json-output", default=None)
    parser.add_argument("--plot-dir", default=None)
    args = parser.parse_args()

    tree = load_default_tree()

    experiments = discover_experiments(args.experiments_dir)
    print(f"[discover] {len(experiments)} experiments found")

    # Apply filters
    def keep(exp: Dict[str, Any]) -> bool:
        meta = exp.get("meta", {})
        if args.languages and meta.get("language") not in {l.upper() for l in args.languages}:
            return False
        if args.methods:
            method = meta.get("method", "")
            if not any(method == m or method.startswith(m + "_") for m in args.methods):
                if method not in args.methods:
                    return False
        if args.models:
            mk = (meta.get("model_key") or "").lower()
            if not any(s.lower() in mk for s in args.models):
                return False
        return True

    experiments = [e for e in experiments if keep(e)]
    print(f"[filter]   {len(experiments)} experiments after filtering")

    # Collect all gold/pred narrative sets across all runs
    print("[collect]  loading predictions...")
    all_gold: List[Set[str]] = []
    all_pred: List[Set[str]] = []
    n_runs_total = 0

    for exp in experiments:
        manifest = exp["manifest"]
        meta = exp["meta"]
        lang = meta["language"]
        gt_file = os.path.join(
            ground_truth_dir := args.ground_truth_dir,
            lang, "subtask-3-dominant-narratives.txt",
        )
        if not os.path.exists(gt_file):
            continue
        ground_truth = load_annotations(gt_file)
        exp_dir = exp.get("dir", "")

        for run in manifest.get("runs", []):
            if run.get("status") != "success":
                continue
            output_file = run.get("output_file") or ""
            if not os.path.exists(output_file):
                fb = os.path.join(
                    exp_dir, f"run_{run.get('run_id', 1)}", "results.txt"
                )
                if os.path.exists(fb):
                    output_file = fb
                else:
                    continue
            predictions = load_annotations(output_file)
            common = sorted(set(ground_truth.keys()) & set(predictions.keys()))
            n_runs_total += 1
            for doc in common:
                gold_n = _normalise_narratives(
                    ground_truth[doc].get("narratives", []), tree
                )
                pred_n = _normalise_narratives(
                    predictions[doc].get("narratives", []), tree
                )
                all_gold.append(gold_n)
                all_pred.append(pred_n)

    n_docs = len(all_gold)
    print(f"[collect]  {n_docs} document-run pairs from {n_runs_total} runs")

    # Analysis
    print("[analyze]  per-narrative precision/recall...")
    per_narr_pr = per_narrative_precision_recall(all_gold, all_pred, tree.narratives)

    print("[analyze]  error decomposition...")
    decomposition = decompose_errors(all_gold, all_pred, tree)

    print("[analyze]  confusion pairs...")
    confusion_pairs = identify_confusion_pairs(all_gold, all_pred, tree)

    print("[analyze]  systematic error analysis...")
    systematic = systematic_error_analysis(
        experiments, args.ground_truth_dir, tree
    )

    print("[analyze]  generating recommendations...")
    recommendations = generate_recommendations(per_narr_pr, confusion_pairs, systematic)

    # Report
    md = render_report(
        decomposition, per_narr_pr, confusion_pairs, systematic,
        recommendations, n_docs, len(experiments),
    )
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[write] markdown -> {args.output}")

    # JSON
    if args.json_output:
        json_data = {
            "n_documents": n_docs,
            "n_experiments": len(experiments),
            "decomposition": decomposition,
            "per_narrative": per_narr_pr,
            "confusion_pairs": confusion_pairs,
            "systematic": {
                "model_names": systematic["model_names"],
                "per_narrative": {
                    n: {k: v for k, v in s.items()}
                    for n, s in systematic["per_narrative"].items()
                },
            },
            "recommendations": recommendations,
        }
        os.makedirs(os.path.dirname(args.json_output) or ".", exist_ok=True)
        with open(args.json_output, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False, default=str)
        print(f"[write] json -> {args.json_output}")

    # Plots
    if args.plot_dir:
        os.makedirs(args.plot_dir, exist_ok=True)
        plot_error_decomposition(
            per_narr_pr, tree,
            os.path.join(args.plot_dir, "error_decomposition.png"),
        )
        plot_precision_recall_scatter(
            per_narr_pr,
            os.path.join(args.plot_dir, "precision_recall_scatter.png"),
        )
        plot_systematic_heatmap(
            systematic,
            os.path.join(args.plot_dir, "systematic_heatmap.png"),
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())

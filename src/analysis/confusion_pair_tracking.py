#!/usr/bin/env python3
"""
Confusion Pair Tracking — compare bistochastic TCMs between experiment groups.

Compares the normalised confusion matrices of two groups of experiments
(e.g., old prompts vs new prompts) to see which confusion pairs improved
or worsened. Supports both recomputation from raw predictions and loading
precomputed TCM ``.npz`` files.

Usage:

    python -m src.analysis.confusion_pair_tracking \\
        --experiments-dir results/experiments/ \\
        --ground-truth-dir data/dev-documents_4_December/ \\
        --group-a "baseline_deepseek_en_t00,baseline_mistral_en_t00" \\
        --group-b "baseline_deepseek_en_t00_p1,baseline_mistral_en_t00_p1" \\
        --labels P0 P1 \\
        --output results/analysis/confusion_tracking/p0_vs_p1.md \\
        --json-output results/analysis/confusion_tracking/p0_vs_p1.json \\
        --plot-dir results/analysis/confusion_tracking/plots/ \\
        --top-k 15

    # Using precomputed TCM files instead of recomputing:
    python -m src.analysis.confusion_pair_tracking \\
        --tcm-dir results/analysis/tcm/ \\
        --group-a "baseline_deepseek_en_t00,baseline_mistral_en_t00" \\
        --group-b "baseline_deepseek_en_t00_p1" \\
        --labels P0 P1 \\
        --output results/analysis/confusion_tracking/p0_vs_p1.md
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

try:
    from .taxonomy_tree import TaxonomyTree, load_default_tree
    from . import bistochastic_tcm as bt
    from .enhanced_experiment_report import evaluate_run_full
    from .experiment_results_report import (
        discover_experiments,
        load_annotations,
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from src.analysis.taxonomy_tree import TaxonomyTree, load_default_tree
    from src.analysis import bistochastic_tcm as bt
    from src.analysis.enhanced_experiment_report import evaluate_run_full
    from src.analysis.experiment_results_report import (
        discover_experiments,
        load_annotations,
    )


# ---------------------------------------------------------------------------
# Group resolution
# ---------------------------------------------------------------------------

def resolve_group(
    experiments: List[Dict[str, Any]],
    ids_csv: str,
) -> List[Dict[str, Any]]:
    """Return experiments whose IDs match the comma-separated list."""
    ids = {s.strip() for s in ids_csv.split(",") if s.strip()}
    matched = [e for e in experiments if e["experiment_id"] in ids]
    found = {e["experiment_id"] for e in matched}
    missing = ids - found
    if missing:
        print(f"  [warn] group IDs not found: {missing}")
    return matched


# ---------------------------------------------------------------------------
# TCM computation from predictions
# ---------------------------------------------------------------------------

def compute_group_tcm(
    experiments: List[Dict[str, Any]],
    ground_truth_dir: str,
    tree: TaxonomyTree,
) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """Concatenate all y_true/y_pred across runs and build a single TCM.

    Returns ``(raw_matrix, bis_matrix, narrative_order)``.
    """
    all_true: list = []
    all_pred: list = []
    for exp in experiments:
        manifest = exp["manifest"]
        meta = exp["meta"]
        lang = meta["language"]
        gt_file = os.path.join(
            ground_truth_dir, lang, "subtask-3-dominant-narratives.txt"
        )
        if not os.path.exists(gt_file):
            print(f"  [skip] no GT for {lang}")
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
            result = evaluate_run_full(output_file, ground_truth, tree)
            if result is None:
                continue
            all_true.extend(result["y_true"])
            all_pred.extend(result["y_pred"])

    if not all_true:
        raise ValueError("No evaluable runs in group")

    M_raw, narr_order = bt.build_narrative_tcm(all_true, all_pred, tree)
    norms = bt.all_normalisations(M_raw)
    return norms["raw"], norms["bis"], narr_order


def load_precomputed_tcms(
    tcm_dir: str,
    ids_csv: str,
) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """Load and average precomputed TCM .npz files for the given IDs."""
    ids = [s.strip() for s in ids_csv.split(",") if s.strip()]
    raw_mats: List[np.ndarray] = []
    bis_mats: List[np.ndarray] = []
    narr_order: Optional[List[str]] = None

    for eid in ids:
        path = os.path.join(tcm_dir, f"{eid}_tcm.npz")
        if not os.path.exists(path):
            print(f"  [warn] TCM file not found: {path}")
            continue
        data = np.load(path, allow_pickle=True)
        narratives = list(data["narratives"])
        if narr_order is None:
            narr_order = narratives
        elif narratives != narr_order:
            print(f"  [warn] narrative ordering mismatch in {eid}, skipping")
            continue
        raw_mats.append(data["raw"])
        bis_mats.append(data["bis"])

    if not raw_mats:
        raise ValueError("No valid TCM files found in group")

    avg_raw = np.mean(raw_mats, axis=0)
    avg_bis = np.mean(bis_mats, axis=0)
    return avg_raw, avg_bis, narr_order  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Delta analysis
# ---------------------------------------------------------------------------

def analyze_delta(
    raw_a: np.ndarray,
    bis_a: np.ndarray,
    raw_b: np.ndarray,
    bis_b: np.ndarray,
    narratives: List[str],
    tree: TaxonomyTree,
    top_k: int = 15,
) -> Dict[str, Any]:
    """Compare two bis(TCM) matrices and extract top improved/worsened pairs.

    Delta = bis_a - bis_b. Positive = A had more confusion (B improved).
    """
    delta = bt.confusion_delta(bis_a, bis_b)
    n = len(narratives)

    pairs = []
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            d = float(delta[i, j])
            same_dom = tree.domain_of.get(narratives[i]) == tree.domain_of.get(
                narratives[j]
            )
            pairs.append({
                "gold": narratives[i],
                "predicted": narratives[j],
                "delta": d,
                "bis_a": float(bis_a[i, j]),
                "bis_b": float(bis_b[i, j]),
                "raw_a": float(raw_a[i, j]),
                "raw_b": float(raw_b[i, j]),
                "same_domain": same_dom,
            })

    # Top improved: largest positive delta (A had more confusion -> B fixed it)
    improved = sorted(pairs, key=lambda p: p["delta"], reverse=True)[:top_k]
    # Top worsened: largest negative delta (B introduced more confusion)
    worsened = sorted(pairs, key=lambda p: p["delta"])[:top_k]

    # Summary stats
    off_diag = delta.copy()
    np.fill_diagonal(off_diag, 0)
    total_positive = float(off_diag[off_diag > 0].sum())
    total_negative = float(abs(off_diag[off_diag < 0].sum()))
    n_improved = int((off_diag > 1e-4).sum())
    n_worsened = int((off_diag < -1e-4).sum())

    # Top confused pairs per group
    pairs_a = bt.top_confused_pairs(raw_a, bis_a, narratives, tree, top_k=top_k)
    pairs_b = bt.top_confused_pairs(raw_b, bis_b, narratives, tree, top_k=top_k)

    return {
        "delta_matrix": delta,
        "narratives": narratives,
        "improved": improved,
        "worsened": worsened,
        "top_pairs_a": [p.as_dict() for p in pairs_a],
        "top_pairs_b": [p.as_dict() for p in pairs_b],
        "summary": {
            "total_improvement_mass": total_positive,
            "total_worsening_mass": total_negative,
            "n_improved_cells": n_improved,
            "n_worsened_cells": n_worsened,
            "net_change": total_positive - total_negative,
        },
    }


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

def plot_delta_heatmap(
    delta: np.ndarray,
    narratives: List[str],
    tree: TaxonomyTree,
    output_path: str,
    label_a: str = "Group A",
    label_b: str = "Group B",
) -> None:
    """Save a diverging heatmap of the delta matrix."""
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
    except ImportError:
        print("  [warn] matplotlib not available, skipping plot")
        return

    # Short labels for readability
    short = [n[:30] + ("..." if len(n) > 30 else "") for n in narratives]

    fig, ax = plt.subplots(figsize=(14, 12))
    vmax = max(abs(delta.min()), abs(delta.max()), 0.01)
    im = ax.imshow(delta, cmap="RdBu_r", vmin=-vmax, vmax=vmax, aspect="equal")

    ax.set_xticks(range(len(short)))
    ax.set_yticks(range(len(short)))
    ax.set_xticklabels(short, rotation=90, fontsize=7)
    ax.set_yticklabels(short, fontsize=7)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Gold")
    ax.set_title(
        f"bis(TCM) Delta: {label_a} - {label_b}\n"
        f"Blue = {label_a} more confused (improvement in {label_b}), "
        f"Red = {label_b} more confused"
    )

    # Draw domain boundaries
    n_urw = sum(1 for n in narratives if tree.domain_of.get(n) == "URW")
    if 0 < n_urw < len(narratives):
        ax.axhline(n_urw - 0.5, color="black", linewidth=2)
        ax.axvline(n_urw - 0.5, color="black", linewidth=2)

    plt.colorbar(im, ax=ax, label="Delta (bis mass)")
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [plot] delta heatmap -> {output_path}")


def plot_group_tcm(
    bis: np.ndarray,
    narratives: List[str],
    tree: TaxonomyTree,
    output_path: str,
    title: str = "bis(TCM)",
) -> None:
    """Save a heatmap of one group's bistochastic TCM."""
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return

    short = [n[:30] + ("..." if len(n) > 30 else "") for n in narratives]
    fig, ax = plt.subplots(figsize=(14, 12))
    im = ax.imshow(bis, cmap="Reds", aspect="equal")
    ax.set_xticks(range(len(short)))
    ax.set_yticks(range(len(short)))
    ax.set_xticklabels(short, rotation=90, fontsize=7)
    ax.set_yticklabels(short, fontsize=7)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Gold")
    ax.set_title(title)

    n_urw = sum(1 for n in narratives if tree.domain_of.get(n) == "URW")
    if 0 < n_urw < len(narratives):
        ax.axhline(n_urw - 0.5, color="black", linewidth=2)
        ax.axvline(n_urw - 0.5, color="black", linewidth=2)

    plt.colorbar(im, ax=ax, label="Bistochastic mass")
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [plot] TCM heatmap -> {output_path}")


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------

def render_report(
    analysis: Dict[str, Any],
    label_a: str,
    label_b: str,
    group_a_ids: List[str],
    group_b_ids: List[str],
) -> str:
    """Render the comparison report as Markdown."""
    lines: List[str] = []
    a = lines.append

    a(f"# Confusion Pair Tracking: {label_a} vs {label_b}")
    a("")
    a(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    a("")
    a("## Groups")
    a("")
    a(f"**{label_a}** ({len(group_a_ids)} experiments): {', '.join(group_a_ids)}")
    a("")
    a(f"**{label_b}** ({len(group_b_ids)} experiments): {', '.join(group_b_ids)}")
    a("")

    s = analysis["summary"]
    a("## Summary")
    a("")
    a(f"- Confusion cells improved (delta > 0): **{s['n_improved_cells']}**")
    a(f"- Confusion cells worsened (delta < 0): **{s['n_worsened_cells']}**")
    a(f"- Total improvement mass: **{s['total_improvement_mass']:.4f}**")
    a(f"- Total worsening mass: **{s['total_worsening_mass']:.4f}**")
    a(f"- Net change: **{s['net_change']:+.4f}** "
      f"({'overall improvement' if s['net_change'] > 0 else 'overall worsening'})")
    a("")

    # Top improved pairs
    a(f"## Top Improved Confusion Pairs ({label_b} reduces confusion)")
    a("")
    a(f"Positive delta = {label_a} had more confusion than {label_b}.")
    a("")
    a("| # | Gold | Predicted | bis({a}) | bis({b}) | Delta | Domain |".format(
        a=label_a, b=label_b))
    a("|---|------|-----------|---------|---------|-------|--------|")
    for i, p in enumerate(analysis["improved"], 1):
        dom = "same" if p["same_domain"] else "cross"
        a(f"| {i} | {p['gold']} | {p['predicted']} | "
          f"{p['bis_a']:.4f} | {p['bis_b']:.4f} | {p['delta']:+.4f} | {dom} |")
    a("")

    # Top worsened pairs
    a(f"## Top Worsened Confusion Pairs ({label_b} increases confusion)")
    a("")
    a(f"Negative delta = {label_b} has more confusion than {label_a}.")
    a("")
    a("| # | Gold | Predicted | bis({a}) | bis({b}) | Delta | Domain |".format(
        a=label_a, b=label_b))
    a("|---|------|-----------|---------|---------|-------|--------|")
    for i, p in enumerate(analysis["worsened"], 1):
        dom = "same" if p["same_domain"] else "cross"
        a(f"| {i} | {p['gold']} | {p['predicted']} | "
          f"{p['bis_a']:.4f} | {p['bis_b']:.4f} | {p['delta']:+.4f} | {dom} |")
    a("")

    # Top confused pairs per group
    for label, key in [(label_a, "top_pairs_a"), (label_b, "top_pairs_b")]:
        a(f"## Top Confused Pairs — {label}")
        a("")
        a("| # | Gold | Predicted | bis mass | raw mass | Domain |")
        a("|---|------|-----------|----------|----------|--------|")
        for i, p in enumerate(analysis[key], 1):
            dom = "same" if p["same_domain"] else "cross"
            a(f"| {i} | {p['gold']} | {p['predicted']} | "
              f"{p['bis_mass']:.4f} | {p['raw_mass']:.4f} | {dom} |")
        a("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare bis(TCM) between two experiment groups."
    )
    parser.add_argument(
        "--experiments-dir",
        default="results/experiments/",
        help="Root directory with experiment subdirectories.",
    )
    parser.add_argument(
        "--ground-truth-dir",
        default="data/dev-documents_4_December/",
        help="Ground truth directory.",
    )
    parser.add_argument(
        "--group-a",
        required=True,
        help="Comma-separated experiment IDs for group A (before).",
    )
    parser.add_argument(
        "--group-b",
        required=True,
        help="Comma-separated experiment IDs for group B (after).",
    )
    parser.add_argument(
        "--labels",
        nargs=2,
        default=["Group A", "Group B"],
        metavar=("LABEL_A", "LABEL_B"),
        help="Display labels for the two groups (default: 'Group A' 'Group B').",
    )
    parser.add_argument(
        "--tcm-dir",
        default=None,
        help="Load precomputed TCM .npz files from this directory instead of recomputing.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=15,
        help="Number of top improved/worsened pairs to report.",
    )
    parser.add_argument("--output", required=True, help="Output Markdown file.")
    parser.add_argument("--json-output", default=None, help="Output JSON file.")
    parser.add_argument("--plot-dir", default=None, help="Directory for heatmap PNGs.")
    args = parser.parse_args()

    tree = load_default_tree()
    label_a, label_b = args.labels
    group_a_ids = [s.strip() for s in args.group_a.split(",") if s.strip()]
    group_b_ids = [s.strip() for s in args.group_b.split(",") if s.strip()]

    # Compute or load TCMs
    if args.tcm_dir:
        print(f"[load] precomputed TCMs from {args.tcm_dir}")
        raw_a, bis_a, narr_a = load_precomputed_tcms(args.tcm_dir, args.group_a)
        raw_b, bis_b, narr_b = load_precomputed_tcms(args.tcm_dir, args.group_b)
        if narr_a != narr_b:
            print("[error] narrative ordering mismatch between groups")
            return 1
        narratives = narr_a
    else:
        print(f"[discover] scanning {args.experiments_dir}")
        experiments = discover_experiments(args.experiments_dir)
        print(f"[discover] {len(experiments)} experiments found")

        exps_a = resolve_group(experiments, args.group_a)
        exps_b = resolve_group(experiments, args.group_b)
        print(f"[groups] A={len(exps_a)} experiments, B={len(exps_b)} experiments")

        if not exps_a or not exps_b:
            print("[error] one or both groups are empty")
            return 1

        print(f"[compute] building TCM for {label_a}...")
        raw_a, bis_a, narr_a = compute_group_tcm(exps_a, args.ground_truth_dir, tree)
        print(f"[compute] building TCM for {label_b}...")
        raw_b, bis_b, narr_b = compute_group_tcm(exps_b, args.ground_truth_dir, tree)

        if narr_a != narr_b:
            print("[error] narrative ordering mismatch")
            return 1
        narratives = narr_a

    # Delta analysis
    print("[analyze] computing delta...")
    analysis = analyze_delta(
        raw_a, bis_a, raw_b, bis_b, narratives, tree, top_k=args.top_k
    )

    # Report
    md = render_report(analysis, label_a, label_b, group_a_ids, group_b_ids)
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[write] markdown -> {args.output}")

    # JSON
    if args.json_output:
        json_data = {
            "label_a": label_a,
            "label_b": label_b,
            "group_a_ids": group_a_ids,
            "group_b_ids": group_b_ids,
            "summary": analysis["summary"],
            "improved": analysis["improved"],
            "worsened": analysis["worsened"],
            "top_pairs_a": analysis["top_pairs_a"],
            "top_pairs_b": analysis["top_pairs_b"],
            "narratives": narratives,
            "delta_matrix": analysis["delta_matrix"].tolist(),
        }
        os.makedirs(os.path.dirname(args.json_output) or ".", exist_ok=True)
        with open(args.json_output, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        print(f"[write] json -> {args.json_output}")

    # Plots
    if args.plot_dir:
        os.makedirs(args.plot_dir, exist_ok=True)
        plot_delta_heatmap(
            analysis["delta_matrix"],
            narratives,
            tree,
            os.path.join(args.plot_dir, "delta_heatmap.png"),
            label_a=label_a,
            label_b=label_b,
        )
        plot_group_tcm(
            bis_a, narratives, tree,
            os.path.join(args.plot_dir, f"tcm_{label_a.lower().replace(' ', '_')}.png"),
            title=f"bis(TCM) — {label_a}",
        )
        plot_group_tcm(
            bis_b, narratives, tree,
            os.path.join(args.plot_dir, f"tcm_{label_b.lower().replace(' ', '_')}.png"),
            title=f"bis(TCM) — {label_b}",
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())

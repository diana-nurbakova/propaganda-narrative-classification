#!/usr/bin/env python3
"""
Ensemble Size Ablation Report.

Evaluates Agora experiments with varying numbers of agents (1, 3, 5, 7)
on a single model and language, producing a focused Markdown + JSON report
with narrative- and subnarrative-level metrics and pairwise significance tests.

Usage:
    python src/analysis/ensemble_ablation_report.py \
        --experiments-dir results/experiments/ \
        --output results/analysis/ensemble_ablation.md

    # Restrict to a specific temperature
    python src/analysis/ensemble_ablation_report.py \
        --experiments-dir results/experiments/ \
        --temps 0.7 \
        --output results/analysis/ensemble_ablation_t07.md
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from scipy import stats

# Reuse evaluation utilities from the main report module
sys.path.insert(0, str(Path(__file__).resolve().parent))
from experiment_results_report import (
    bootstrap_ci,
    compute_f1_scores,
    compute_f1_samples_manual,
    discover_experiments,
    evaluate_all_runs,
    format_metric,
    format_metric_short,
    load_annotations,
    paired_significance_test,
    parse_experiment_metadata,
    significance_marker,
)

# ---------------------------------------------------------------------------
# Ablation-specific constants
# ---------------------------------------------------------------------------

# Maps method keys to agent count (for sorting)
ENSEMBLE_METHODS = {
    "agora_1": 1,
    "agora": 3,
    "agora_5": 5,
    "agora_7": 7,
}

ENSEMBLE_LABELS = {
    "agora_1": "1 agent",
    "agora": "3 agents",
    "agora_5": "5 agents",
    "agora_7": "7 agents",
}


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------


def filter_ensemble_experiments(
    experiments: List[Dict[str, Any]],
    model_keyword: str = "deepseek",
    language: str = "EN",
    temps: Optional[List[float]] = None,
) -> List[Dict[str, Any]]:
    """Keep only agora_1 / agora / agora_5 / agora_7 experiments matching filters."""
    target_methods = set(ENSEMBLE_METHODS.keys())
    filtered = []
    for exp in experiments:
        meta = exp["meta"]
        method = meta.get("method", "")
        if method not in target_methods:
            continue
        if model_keyword.lower() not in exp["experiment_id"].lower():
            continue
        if meta.get("language", "").upper() != language.upper():
            continue
        if temps is not None:
            try:
                t = float(meta.get("temperature", -1))
            except (ValueError, TypeError):
                continue
            if t not in temps:
                continue
        filtered.append(exp)

    # Sort by (temperature, agent count)
    def _sort_key(exp):
        t = float(exp["meta"].get("temperature", 0))
        n = ENSEMBLE_METHODS.get(exp["meta"]["method"], 99)
        return (t, n)

    return sorted(filtered, key=_sort_key)


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------


def _metric_table(
    evaluated: List[Dict[str, Any]],
    level: str,
) -> str:
    """Generate a Markdown table for one hierarchy level (narratives or subnarratives)."""
    prefix = f"{level}_"
    keys = [f"{prefix}f1_macro", f"{prefix}f1_micro", f"{prefix}f1_samples", f"{prefix}f1_samples_manual"]
    header_labels = ["F1-macro", "F1-micro", "F1-samples", "F1-samples (manual)"]

    header = "| Ensemble | Agents | Runs | " + " | ".join(header_labels) + " |\n"
    sep = "|----------|--------|------|" + "|".join(["-" * (len(h) + 2) for h in header_labels]) + "|\n"

    rows = ""
    for ev in evaluated:
        method = ev["meta"]["method"]
        label = ENSEMBLE_LABELS.get(method, method)
        n_agents = ENSEMBLE_METHODS.get(method, "?")
        n_runs = ev.get("n_successful_runs", 0)

        cells = []
        for k in keys:
            d = ev["metrics"].get(k, {})
            if d.get("mean") is None:
                cells.append("N/A")
            else:
                cells.append(format_metric_short(d["mean"], d["std"]))

        rows += f"| {label} | {n_agents} | {n_runs} | " + " | ".join(cells) + " |\n"

    return header + sep + rows + "\n"


def _ci_table(
    evaluated: List[Dict[str, Any]],
) -> str:
    """Bootstrap 95% CI table for the two key F1-samples metrics."""
    header = (
        "| Ensemble | Agents | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |\n"
        "|----------|--------|--------------------------|-----------------------------|\n"
    )
    rows = ""
    for ev in evaluated:
        method = ev["meta"]["method"]
        label = ENSEMBLE_LABELS.get(method, method)
        n_agents = ENSEMBLE_METHODS.get(method, "?")

        def _fmt(key):
            d = ev["metrics"].get(key, {})
            if d.get("mean") is None:
                return "N/A"
            return format_metric(d["mean"], d["std"], d["ci_lower"], d["ci_upper"])

        rows += (
            f"| {label} | {n_agents} "
            f"| {_fmt('narratives_f1_samples')} "
            f"| {_fmt('subnarratives_f1_samples')} |\n"
        )
    return header + rows + "\n"


def _significance_table(
    evaluated: List[Dict[str, Any]],
    metric_key: str,
    metric_label: str,
) -> str:
    """Pairwise significance tests between all ensemble sizes."""
    header = (
        f"Metric: **{metric_label}**\n\n"
        "| A | B | Mean A | Mean B | Diff | Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |\n"
        "|---|---|--------|--------|------|-----------|--------|-------------|------------|------|\n"
    )
    rows = ""
    for i, ev_a in enumerate(evaluated):
        for ev_b in evaluated[i + 1:]:
            scores_a = ev_a["metrics"].get(metric_key, {}).get("scores", [])
            scores_b = ev_b["metrics"].get(metric_key, {}).get("scores", [])
            if not scores_a or not scores_b:
                continue
            n = min(len(scores_a), len(scores_b))
            if n < 2:
                continue

            result = paired_significance_test(scores_a[:n], scores_b[:n])
            mean_a = np.mean(scores_a)
            mean_b = np.mean(scores_b)
            diff = mean_a - mean_b
            sig = significance_marker(result["p_wilcoxon"])

            label_a = ENSEMBLE_LABELS.get(ev_a["meta"]["method"], ev_a["experiment_id"])
            label_b = ENSEMBLE_LABELS.get(ev_b["meta"]["method"], ev_b["experiment_id"])

            rows += (
                f"| {label_a} | {label_b} "
                f"| {mean_a:.3f} | {mean_b:.3f} | {diff:+.3f} "
                f"| {result['cohens_d']:+.2f} | {result['effect_size']} "
                f"| {result['p_wilcoxon']:.4f} | {result['p_ttest']:.4f} | {sig} |\n"
            )

    return header + rows + "\n"


def _trend_summary(evaluated: List[Dict[str, Any]]) -> str:
    """Short paragraph summarising the trend across ensemble sizes."""
    narr_means = []
    sub_means = []
    sizes = []
    for ev in evaluated:
        method = ev["meta"]["method"]
        n = ENSEMBLE_METHODS.get(method)
        if n is None:
            continue
        narr = ev["metrics"].get("narratives_f1_samples", {}).get("mean")
        sub = ev["metrics"].get("subnarratives_f1_samples", {}).get("mean")
        if narr is not None and sub is not None:
            sizes.append(n)
            narr_means.append(narr)
            sub_means.append(sub)

    if len(sizes) < 2:
        return ""

    text = "### Trend Summary\n\n"
    # Narrative
    best_narr_idx = int(np.argmax(narr_means))
    text += (
        f"- **Narrative F1-samples**: best at **{sizes[best_narr_idx]} agents** "
        f"({narr_means[best_narr_idx]:.3f}), "
        f"range {min(narr_means):.3f} -- {max(narr_means):.3f}\n"
    )
    # Subnarrative
    best_sub_idx = int(np.argmax(sub_means))
    text += (
        f"- **Subnarrative F1-samples**: best at **{sizes[best_sub_idx]} agents** "
        f"({sub_means[best_sub_idx]:.3f}), "
        f"range {min(sub_means):.3f} -- {max(sub_means):.3f}\n"
    )

    # Monotonicity check
    narr_mono_up = all(narr_means[i] <= narr_means[i + 1] for i in range(len(narr_means) - 1))
    narr_mono_down = all(narr_means[i] >= narr_means[i + 1] for i in range(len(narr_means) - 1))
    sub_mono_up = all(sub_means[i] <= sub_means[i + 1] for i in range(len(sub_means) - 1))
    sub_mono_down = all(sub_means[i] >= sub_means[i + 1] for i in range(len(sub_means) - 1))

    if narr_mono_up:
        text += "- Narrative F1 is **monotonically increasing** with ensemble size.\n"
    elif narr_mono_down:
        text += "- Narrative F1 is **monotonically decreasing** with ensemble size (intersection becomes stricter).\n"
    else:
        text += "- Narrative F1 is **non-monotonic** across ensemble sizes.\n"

    if sub_mono_up:
        text += "- Subnarrative F1 is **monotonically increasing** with ensemble size.\n"
    elif sub_mono_down:
        text += "- Subnarrative F1 is **monotonically decreasing** with ensemble size.\n"
    else:
        text += "- Subnarrative F1 is **non-monotonic** across ensemble sizes.\n"

    text += "\n"
    return text


def generate_ablation_report(
    experiments: List[Dict[str, Any]],
    evaluated: List[Dict[str, Any]],
    model_keyword: str,
    language: str,
) -> str:
    """Generate the full Markdown ablation report."""
    report = "# Ensemble Size Ablation Report\n\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report += (
        f"**Model**: {model_keyword} | **Language**: {language} | "
        f"**Aggregation**: intersection | "
        f"**Ensemble sizes**: {', '.join(str(v) for v in sorted(ENSEMBLE_METHODS.values()))}\n\n"
    )

    # Group by temperature
    by_temp = defaultdict(list)
    for ev in evaluated:
        if "error" in ev:
            continue
        t = ev["meta"].get("temperature", "?")
        by_temp[t].append(ev)

    for temp in sorted(by_temp.keys()):
        evs = by_temp[temp]
        # Sort by agent count
        evs.sort(key=lambda e: ENSEMBLE_METHODS.get(e["meta"]["method"], 99))

        report += f"## Temperature = {temp}\n\n"

        n_total_runs = sum(e.get("n_successful_runs", 0) for e in evs)
        report += f"Total successful runs across all ensemble sizes: **{n_total_runs}**\n\n"

        # Narrative table
        report += "### Narrative-level Metrics\n\n"
        report += _metric_table(evs, "narratives")

        # Subnarrative table
        report += "### Subnarrative-level Metrics\n\n"
        report += _metric_table(evs, "subnarratives")

        # CI table
        report += "### Bootstrap 95% Confidence Intervals\n\n"
        report += _ci_table(evs)

        # Trend summary
        report += _trend_summary(evs)

        # Significance tests — narrative
        report += "### Pairwise Significance Tests (Narrative)\n\n"
        report += _significance_table(evs, "narratives_f1_samples", "Narrative F1-samples")

        # Significance tests — subnarrative
        report += "### Pairwise Significance Tests (Subnarrative)\n\n"
        report += _significance_table(evs, "subnarratives_f1_samples", "Subnarrative F1-samples")

    # Errors
    errors = [e for e in evaluated if "error" in e]
    if errors:
        report += "## Errors\n\n"
        for e in errors:
            report += f"- `{e.get('experiment_id', '?')}`: {e['error']}\n"
        report += "\n"

    return report


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Generate ensemble size ablation report",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--experiments-dir",
        type=str,
        default="results/experiments/",
        help="Root directory containing experiment subdirectories",
    )
    parser.add_argument(
        "--ground-truth-dir",
        type=str,
        default="data/dev-documents_4_December",
        help="Directory containing per-language ground truth files",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="deepseek",
        help="Model keyword to filter experiments (default: deepseek)",
    )
    parser.add_argument(
        "--language",
        type=str,
        default="EN",
        help="Language to filter experiments (default: EN)",
    )
    parser.add_argument(
        "--temps",
        nargs="*",
        type=float,
        default=None,
        help="Temperature(s) to include (default: all)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results/analysis/ensemble_ablation.md",
        help="Output Markdown report path",
    )
    parser.add_argument(
        "--json-output",
        type=str,
        default=None,
        help="Optional: also save raw evaluation data as JSON",
    )

    args = parser.parse_args()

    # Discover & filter
    print("Discovering experiments...")
    all_experiments = discover_experiments(args.experiments_dir)
    print(f"Found {len(all_experiments)} total experiments")

    experiments = filter_ensemble_experiments(
        all_experiments,
        model_keyword=args.model,
        language=args.language,
        temps=args.temps,
    )
    print(
        f"Filtered to {len(experiments)} ensemble ablation experiments "
        f"(model={args.model}, lang={args.language}, temps={args.temps or 'all'})"
    )

    if not experiments:
        print("No matching experiments found!")
        return 1

    # Evaluate
    print(f"\nEvaluating {len(experiments)} experiments...")
    evaluated = []
    for i, exp in enumerate(experiments, 1):
        exp_id = exp["experiment_id"]
        print(f"  [{i}/{len(experiments)}] {exp_id}...", end=" ")

        result = evaluate_all_runs(exp, args.ground_truth_dir)
        result["experiment_id"] = exp_id
        result["meta"] = exp["meta"]
        result["dir"] = exp.get("dir", "")

        if "error" in result:
            print(f"ERROR: {result['error']}")
        else:
            n_runs = result["n_successful_runs"]
            narr_f1 = result["metrics"].get("narratives_f1_samples", {}).get("mean")
            sub_f1 = result["metrics"].get("subnarratives_f1_samples", {}).get("mean")
            narr_str = f"{narr_f1:.3f}" if narr_f1 is not None else "N/A"
            sub_str = f"{sub_f1:.3f}" if sub_f1 is not None else "N/A"
            print(f"{n_runs} runs | Narr F1s={narr_str} | Sub F1s={sub_str}")

        evaluated.append(result)

    # Generate report
    print("\nGenerating ablation report...")
    report = generate_ablation_report(experiments, evaluated, args.model, args.language)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report saved to: {args.output}")

    # Optional JSON
    json_path = args.json_output
    if json_path is None:
        json_path = args.output.replace(".md", ".json")

    json_data = {
        "generated_at": datetime.now().isoformat(),
        "model": args.model,
        "language": args.language,
        "n_experiments": len(evaluated),
        "experiments": [],
    }
    for ev in evaluated:
        ev_clean = {
            "experiment_id": ev.get("experiment_id"),
            "method": ev["meta"].get("method"),
            "num_agents": ENSEMBLE_METHODS.get(ev["meta"].get("method")),
            "temperature": ev["meta"].get("temperature"),
            "n_successful_runs": ev.get("n_successful_runs", 0),
        }
        if "error" in ev:
            ev_clean["error"] = ev["error"]
        else:
            ev_clean["metrics"] = {}
            for key, val in ev.get("metrics", {}).items():
                ev_clean["metrics"][key] = {
                    k: v for k, v in val.items() if k != "scores"
                }
                ev_clean["metrics"][key]["scores"] = [
                    round(s, 6) for s in val.get("scores", [])
                ]
        json_data["experiments"].append(ev_clean)

    os.makedirs(os.path.dirname(json_path) or ".", exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)
    print(f"JSON data saved to: {json_path}")

    print("\nDone!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

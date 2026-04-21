#!/usr/bin/env python3
"""
Document Difficulty Analysis — rank documents by difficulty across experiments.

Identifies universally hard documents vs model-specific failures by computing
per-document hierarchical F1 scores across all experiments and runs.

Usage:

    python -m src.analysis.document_difficulty \\
        --experiments-dir results/experiments/ \\
        --ground-truth-dir data/dev-documents_4_December/ \\
        --output results/analysis/difficulty/report.md \\
        --json-output results/analysis/difficulty/report.json \\
        --plot-dir results/analysis/difficulty/plots/ \\
        --languages EN --top-k 20
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

try:
    from .taxonomy_tree import TaxonomyTree, load_default_tree
    from . import hierarchical_metrics as hm
    from .enhanced_experiment_report import evaluate_run_full
    from .experiment_results_report import (
        discover_experiments,
        load_annotations,
        METHOD_DISPLAY,
        MODEL_DISPLAY,
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from src.analysis.taxonomy_tree import TaxonomyTree, load_default_tree
    from src.analysis import hierarchical_metrics as hm
    from src.analysis.enhanced_experiment_report import evaluate_run_full
    from src.analysis.experiment_results_report import (
        discover_experiments,
        load_annotations,
        METHOD_DISPLAY,
        MODEL_DISPLAY,
    )


# ---------------------------------------------------------------------------
# Per-document score collection
# ---------------------------------------------------------------------------

def collect_per_doc_scores(
    experiments: List[Dict[str, Any]],
    ground_truth_dir: str,
    tree: TaxonomyTree,
) -> Tuple[
    Dict[str, Dict[str, List[float]]],
    Dict[str, Dict[str, Any]],
]:
    """Compute per-document hF1 for every run of every experiment.

    Returns:
        per_doc_scores: ``{doc_filename: {experiment_id: [hF1_run1, ...]}}``.
        experiment_meta: ``{experiment_id: meta_dict}`` for model/method grouping.
    """
    per_doc: Dict[str, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
    experiment_meta: Dict[str, Dict[str, Any]] = {}

    for exp in experiments:
        eid = exp["experiment_id"]
        manifest = exp["manifest"]
        meta = exp["meta"]
        experiment_meta[eid] = meta
        lang = meta["language"]
        gt_file = os.path.join(
            ground_truth_dir, lang, "subtask-3-dominant-narratives.txt"
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
            result = evaluate_run_full(output_file, ground_truth, tree)
            if result is None:
                continue

            # Per-doc hF1
            doc_hf1 = hm.hierarchical_f1_per_doc(
                result["y_true"], result["y_pred"], tree
            )
            for doc, score in zip(result["common_files"], doc_hf1):
                per_doc[doc][eid].append(score)

    return dict(per_doc), experiment_meta


# ---------------------------------------------------------------------------
# Difficulty scoring
# ---------------------------------------------------------------------------

def compute_difficulty_table(
    per_doc_scores: Dict[str, Dict[str, List[float]]],
) -> List[Dict[str, Any]]:
    """Compute difficulty statistics for each document.

    Returns sorted list (hardest first) of dicts with:
    mean_hf1, std_hf1, min_hf1, max_hf1, n_experiments, n_runs, difficulty.
    """
    rows: List[Dict[str, Any]] = []
    for doc, exp_scores in per_doc_scores.items():
        all_scores = [s for scores in exp_scores.values() for s in scores]
        if not all_scores:
            continue
        arr = np.array(all_scores, dtype=float)
        rows.append({
            "document": doc,
            "mean_hf1": float(arr.mean()),
            "std_hf1": float(arr.std(ddof=1)) if len(arr) > 1 else 0.0,
            "min_hf1": float(arr.min()),
            "max_hf1": float(arr.max()),
            "n_experiments": len(exp_scores),
            "n_runs": len(all_scores),
            "difficulty": float(1.0 - arr.mean()),
        })
    rows.sort(key=lambda r: r["difficulty"], reverse=True)
    return rows


# ---------------------------------------------------------------------------
# Characterization of hard documents
# ---------------------------------------------------------------------------

def characterize_hard_docs(
    hard_docs: List[str],
    ground_truth_dir: str,
    tree: TaxonomyTree,
) -> Dict[str, Dict[str, Any]]:
    """Load gold labels for hard documents and characterize them."""
    # Load GT for all languages
    gt_all: Dict[str, Dict[str, List[str]]] = {}
    for lang_dir in Path(ground_truth_dir).iterdir():
        if not lang_dir.is_dir():
            continue
        gt_file = lang_dir / "subtask-3-dominant-narratives.txt"
        if gt_file.exists():
            gt_all.update(load_annotations(str(gt_file)))

    result: Dict[str, Dict[str, Any]] = {}
    for doc in hard_docs:
        rec = gt_all.get(doc, {"narratives": [], "subnarratives": []})
        raw_narrs = rec.get("narratives", [])
        raw_subs = rec.get("subnarratives", [])
        # Normalise to bare names
        narrs = sorted(
            n for label in raw_narrs
            if (n := tree.parse_narrative_label(label)) is not None
        )
        # Determine language from filename prefix
        lang = doc.split("_")[0] if "_" in doc else "?"
        # Determine domain(s)
        domains = set()
        for n in narrs:
            d = tree.domain_of.get(n)
            if d:
                domains.add(d)
        result[doc] = {
            "language": lang,
            "n_narratives": len(narrs),
            "n_subnarratives": len(raw_subs),
            "narratives": narrs,
            "subnarratives": raw_subs,
            "domains": sorted(domains),
            "is_multi_label": len(narrs) > 1,
            "is_other": not narrs,
        }
    return result


# ---------------------------------------------------------------------------
# Per-document error patterns for hard docs
# ---------------------------------------------------------------------------

def _normalise_narratives(
    raw_labels: List[str], tree: TaxonomyTree,
) -> Set[str]:
    """Convert prefixed labels like 'URW: Discrediting Ukraine' to bare
    narrative names used in ``tree.narratives``."""
    out: Set[str] = set()
    for label in raw_labels:
        parsed = tree.parse_narrative_label(label)
        if parsed:
            out.add(parsed)
    return out


def collect_per_doc_errors(
    experiments: List[Dict[str, Any]],
    ground_truth_dir: str,
    tree: TaxonomyTree,
    target_docs: Set[str],
) -> Dict[str, Dict[str, Any]]:
    """For target docs, collect FP/FN sets across all experiments.

    Returns ``{doc: {fp_narratives: Counter, fn_narratives: Counter,
    n_runs: int, ...}}``.
    """
    from collections import Counter

    doc_errors: Dict[str, Dict[str, Any]] = {
        d: {"fp_narratives": Counter(), "fn_narratives": Counter(), "n_runs": 0}
        for d in target_docs
    }

    for exp in experiments:
        manifest = exp["manifest"]
        meta = exp["meta"]
        lang = meta["language"]
        gt_file = os.path.join(
            ground_truth_dir, lang, "subtask-3-dominant-narratives.txt"
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
            for doc in target_docs:
                if doc not in ground_truth or doc not in predictions:
                    continue
                gold_narrs = _normalise_narratives(
                    ground_truth[doc].get("narratives", []), tree
                )
                pred_narrs = _normalise_narratives(
                    predictions[doc].get("narratives", []), tree
                )
                fp = pred_narrs - gold_narrs
                fn = gold_narrs - pred_narrs
                doc_errors[doc]["n_runs"] += 1
                for n in fp:
                    doc_errors[doc]["fp_narratives"][n] += 1
                for n in fn:
                    doc_errors[doc]["fn_narratives"][n] += 1

    return doc_errors


# ---------------------------------------------------------------------------
# Model agreement analysis
# ---------------------------------------------------------------------------

def compute_model_agreement(
    per_doc_scores: Dict[str, Dict[str, List[float]]],
    experiment_meta: Dict[str, Dict[str, Any]],
) -> Tuple[np.ndarray, List[str], Dict[str, Dict[str, float]]]:
    """Compute Spearman correlation of per-doc difficulty between models.

    Returns ``(correlation_matrix, model_names, per_model_doc_means)``.
    """
    from scipy import stats as sp_stats

    # Group experiments by model
    model_exps: Dict[str, List[str]] = defaultdict(list)
    for eid, meta in experiment_meta.items():
        mk = meta.get("model_key", "unknown")
        display = MODEL_DISPLAY.get(mk, mk) if mk else "unknown"
        model_exps[display].append(eid)

    if len(model_exps) < 2:
        return np.array([[1.0]]), list(model_exps.keys()), {}

    # All documents that appear in at least one experiment
    all_docs = sorted(per_doc_scores.keys())

    # Per-model mean hF1 vector
    per_model_means: Dict[str, Dict[str, float]] = {}
    model_names = sorted(model_exps.keys())
    for model in model_names:
        eids = set(model_exps[model])
        doc_means: Dict[str, float] = {}
        for doc in all_docs:
            scores = []
            for eid in eids:
                if eid in per_doc_scores.get(doc, {}):
                    scores.extend(per_doc_scores[doc][eid])
            if scores:
                doc_means[doc] = float(np.mean(scores))
        per_model_means[model] = doc_means

    # Pairwise Spearman on shared documents
    n = len(model_names)
    corr = np.ones((n, n), dtype=float)
    for i in range(n):
        for j in range(i + 1, n):
            shared = sorted(
                set(per_model_means[model_names[i]].keys())
                & set(per_model_means[model_names[j]].keys())
            )
            if len(shared) < 3:
                corr[i, j] = corr[j, i] = float("nan")
                continue
            x = [per_model_means[model_names[i]][d] for d in shared]
            y = [per_model_means[model_names[j]][d] for d in shared]
            rho, _ = sp_stats.spearmanr(x, y)
            corr[i, j] = corr[j, i] = float(rho)

    return corr, model_names, per_model_means


def classify_consistent_vs_specific(
    per_doc_scores: Dict[str, Dict[str, List[float]]],
    experiment_meta: Dict[str, Dict[str, Any]],
    difficulty_table: List[Dict[str, Any]],
    threshold: float = 0.5,
    top_k: int = 20,
) -> Dict[str, List[Dict[str, Any]]]:
    """Classify hard docs as 'consistently hard' or 'model-specific'.

    consistently_hard: mean_hf1 < threshold across ALL models that evaluated it.
    model_specific: high variance of per-model means (some models succeed, others fail).
    """
    # Group by model
    model_exps: Dict[str, Set[str]] = defaultdict(set)
    for eid, meta in experiment_meta.items():
        mk = meta.get("model_key", "unknown")
        display = MODEL_DISPLAY.get(mk, mk) if mk else "unknown"
        model_exps[display].add(eid)

    hard_docs = [r for r in difficulty_table if r["difficulty"] >= (1 - threshold)][:top_k * 2]

    consistent: List[Dict[str, Any]] = []
    specific: List[Dict[str, Any]] = []

    for row in hard_docs:
        doc = row["document"]
        model_means: Dict[str, float] = {}
        for model, eids in model_exps.items():
            scores = []
            for eid in eids:
                if eid in per_doc_scores.get(doc, {}):
                    scores.extend(per_doc_scores[doc][eid])
            if scores:
                model_means[model] = float(np.mean(scores))

        if len(model_means) < 2:
            continue

        vals = list(model_means.values())
        mean_across = float(np.mean(vals))
        std_across = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0

        entry = {**row, "per_model_means": model_means, "cross_model_std": std_across}

        if all(v < threshold for v in vals):
            consistent.append(entry)
        elif std_across > 0.2:
            specific.append(entry)

    return {
        "consistently_hard": sorted(consistent, key=lambda r: r["difficulty"], reverse=True),
        "model_specific": sorted(specific, key=lambda r: r["cross_model_std"], reverse=True),
    }


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

def plot_difficulty_histogram(
    difficulty_table: List[Dict[str, Any]],
    output_path: str,
) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return

    scores = [r["mean_hf1"] for r in difficulty_table]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(scores, bins=20, edgecolor="black", alpha=0.7, color="steelblue")
    ax.axvline(np.mean(scores), color="red", linestyle="--", label=f"Mean={np.mean(scores):.2f}")
    ax.set_xlabel("Mean hierarchical F1")
    ax.set_ylabel("Number of documents")
    ax.set_title("Document Difficulty Distribution")
    ax.legend()
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [plot] difficulty histogram -> {output_path}")


def plot_model_agreement(
    corr_matrix: np.ndarray,
    model_names: List[str],
    output_path: str,
) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(corr_matrix, cmap="RdYlGn", vmin=-1, vmax=1, aspect="equal")
    ax.set_xticks(range(len(model_names)))
    ax.set_yticks(range(len(model_names)))
    ax.set_xticklabels(model_names, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(model_names, fontsize=9)
    # Annotate cells
    for i in range(len(model_names)):
        for j in range(len(model_names)):
            v = corr_matrix[i, j]
            if not np.isnan(v):
                ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8)
    ax.set_title("Cross-Model Difficulty Agreement (Spearman)")
    plt.colorbar(im, ax=ax, label="Spearman rho")
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [plot] model agreement -> {output_path}")


def plot_hard_doc_narratives(
    characterization: Dict[str, Dict[str, Any]],
    output_path: str,
) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from collections import Counter
    except ImportError:
        return

    counter: Counter = Counter()
    for doc_info in characterization.values():
        for n in doc_info.get("narratives", []):
            counter[n] += 1

    if not counter:
        return

    labels, counts = zip(*counter.most_common(15))
    short_labels = [l[:35] + ("..." if len(l) > 35 else "") for l in labels]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(range(len(counts)), counts, color="coral", edgecolor="black")
    ax.set_yticks(range(len(short_labels)))
    ax.set_yticklabels(short_labels, fontsize=8)
    ax.set_xlabel("Frequency in hard documents")
    ax.set_title("Narrative Distribution in Hardest Documents")
    ax.invert_yaxis()
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [plot] hard doc narratives -> {output_path}")


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------

def render_report(
    difficulty_table: List[Dict[str, Any]],
    characterization: Dict[str, Dict[str, Any]],
    doc_errors: Dict[str, Dict[str, Any]],
    corr_matrix: np.ndarray,
    model_names: List[str],
    classification: Dict[str, List[Dict[str, Any]]],
    top_k: int,
) -> str:
    lines: List[str] = []
    a = lines.append

    a("# Document Difficulty Analysis")
    a("")
    a(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    a("")

    # Summary stats
    all_diff = [r["difficulty"] for r in difficulty_table]
    a("## Summary")
    a("")
    a(f"- Total documents analyzed: **{len(difficulty_table)}**")
    a(f"- Mean difficulty (1 - hF1): **{np.mean(all_diff):.3f}**")
    a(f"- Median difficulty: **{np.median(all_diff):.3f}**")
    a(f"- Perfect (hF1=1.0): **{sum(1 for d in all_diff if d < 0.001)}** documents")
    a(f"- Very hard (hF1<0.3): **{sum(1 for r in difficulty_table if r['mean_hf1'] < 0.3)}** documents")
    a("")

    # Top-K hardest documents
    a(f"## Top {top_k} Hardest Documents")
    a("")
    a("| # | Document | Mean hF1 | Std | Min | Max | #Exp | #Runs | Gold Narratives |")
    a("|---|----------|----------|-----|-----|-----|------|-------|-----------------|")
    for i, row in enumerate(difficulty_table[:top_k], 1):
        doc = row["document"]
        char = characterization.get(doc, {})
        narrs = char.get("narratives", [])
        narr_str = "; ".join(narrs) if narrs else "Other"
        if len(narr_str) > 60:
            narr_str = narr_str[:57] + "..."
        a(f"| {i} | {doc} | {row['mean_hf1']:.3f} | {row['std_hf1']:.3f} | "
          f"{row['min_hf1']:.3f} | {row['max_hf1']:.3f} | {row['n_experiments']} | "
          f"{row['n_runs']} | {narr_str} |")
    a("")

    # Error patterns for hard docs
    a("## Error Patterns in Hard Documents")
    a("")
    for i, row in enumerate(difficulty_table[:min(top_k, 10)], 1):
        doc = row["document"]
        errs = doc_errors.get(doc, {})
        char = characterization.get(doc, {})
        if not errs.get("n_runs"):
            continue
        n_runs = errs["n_runs"]
        fp = errs.get("fp_narratives", {})
        fn = errs.get("fn_narratives", {})
        a(f"### {i}. {doc} (hF1={row['mean_hf1']:.3f})")
        a("")
        a(f"- **Gold**: {', '.join(char.get('narratives', ['?']))}")
        a(f"- **Labels**: {char.get('n_narratives', '?')} narr, {char.get('n_subnarratives', '?')} sub")
        a(f"- **Evaluated in**: {n_runs} runs")
        if fn:
            a(f"- **Most missed (FN)**: " + ", ".join(
                f"{n} ({c}/{n_runs})" for n, c in fn.most_common(5)
            ))
        if fp:
            a(f"- **Most over-predicted (FP)**: " + ", ".join(
                f"{n} ({c}/{n_runs})" for n, c in fp.most_common(5)
            ))
        a("")

    # Model agreement
    if len(model_names) >= 2:
        a("## Cross-Model Difficulty Agreement")
        a("")
        a("Spearman rank correlation of per-document difficulty between models.")
        a("High correlation = models agree on which documents are hard.")
        a("")
        a("| Model | " + " | ".join(model_names) + " |")
        a("|-------|" + "|".join(["------" for _ in model_names]) + "|")
        for i, m in enumerate(model_names):
            vals = " | ".join(
                f"{corr_matrix[i, j]:.2f}" if not np.isnan(corr_matrix[i, j]) else "n/a"
                for j in range(len(model_names))
            )
            a(f"| {m} | {vals} |")
        a("")

    # Consistent vs specific
    consistent = classification.get("consistently_hard", [])
    specific = classification.get("model_specific", [])

    if consistent:
        a("## Consistently Hard Documents (all models struggle)")
        a("")
        a("| Document | Mean hF1 | Cross-model Std | Per-model Means |")
        a("|----------|----------|-----------------|-----------------|")
        for row in consistent[:15]:
            pm = ", ".join(f"{m}={v:.2f}" for m, v in row["per_model_means"].items())
            a(f"| {row['document']} | {row['mean_hf1']:.3f} | "
              f"{row['cross_model_std']:.3f} | {pm} |")
        a("")

    if specific:
        a("## Model-Specific Failures (high cross-model variance)")
        a("")
        a("| Document | Mean hF1 | Cross-model Std | Per-model Means |")
        a("|----------|----------|-----------------|-----------------|")
        for row in specific[:15]:
            pm = ", ".join(f"{m}={v:.2f}" for m, v in row["per_model_means"].items())
            a(f"| {row['document']} | {row['mean_hf1']:.3f} | "
              f"{row['cross_model_std']:.3f} | {pm} |")
        a("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze per-document difficulty across experiments."
    )
    parser.add_argument(
        "--experiments-dir",
        default="results/experiments/",
    )
    parser.add_argument(
        "--ground-truth-dir",
        default="data/dev-documents_4_December/",
    )
    parser.add_argument("--languages", nargs="*", default=None)
    parser.add_argument("--methods", nargs="*", default=None)
    parser.add_argument("--models", nargs="*", default=None)
    parser.add_argument("--top-k", type=int, default=20)
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

    print("[collect]  computing per-document scores...")
    per_doc_scores, exp_meta = collect_per_doc_scores(
        experiments, args.ground_truth_dir, tree
    )
    print(f"[collect]  {len(per_doc_scores)} documents scored")

    print("[analyze]  computing difficulty table...")
    difficulty_table = compute_difficulty_table(per_doc_scores)

    hard_doc_names = [r["document"] for r in difficulty_table[:args.top_k]]
    print(f"[analyze]  characterizing top {args.top_k} hardest documents...")
    characterization = characterize_hard_docs(
        hard_doc_names, args.ground_truth_dir, tree
    )

    print("[analyze]  collecting error patterns for hard documents...")
    doc_errors = collect_per_doc_errors(
        experiments, args.ground_truth_dir, tree, set(hard_doc_names)
    )

    print("[analyze]  computing model agreement...")
    corr_matrix, model_names, _ = compute_model_agreement(per_doc_scores, exp_meta)

    print("[analyze]  classifying consistent vs model-specific...")
    classification = classify_consistent_vs_specific(
        per_doc_scores, exp_meta, difficulty_table, top_k=args.top_k
    )

    # Report
    md = render_report(
        difficulty_table, characterization, doc_errors,
        corr_matrix, model_names, classification, args.top_k
    )
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[write] markdown -> {args.output}")

    # JSON
    if args.json_output:
        json_data = {
            "n_documents": len(difficulty_table),
            "difficulty_table": difficulty_table,
            "characterization": characterization,
            "model_agreement": {
                "models": model_names,
                "correlation_matrix": corr_matrix.tolist(),
            },
            "classification": {
                "consistently_hard": [
                    {k: v for k, v in r.items() if k != "per_model_means"}
                    | {"per_model_means": r.get("per_model_means", {})}
                    for r in classification.get("consistently_hard", [])
                ],
                "model_specific": [
                    {k: v for k, v in r.items() if k != "per_model_means"}
                    | {"per_model_means": r.get("per_model_means", {})}
                    for r in classification.get("model_specific", [])
                ],
            },
        }
        os.makedirs(os.path.dirname(args.json_output) or ".", exist_ok=True)
        with open(args.json_output, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False, default=str)
        print(f"[write] json -> {args.json_output}")

    # Plots
    if args.plot_dir:
        os.makedirs(args.plot_dir, exist_ok=True)
        plot_difficulty_histogram(
            difficulty_table,
            os.path.join(args.plot_dir, "difficulty_histogram.png"),
        )
        if len(model_names) >= 2:
            plot_model_agreement(
                corr_matrix, model_names,
                os.path.join(args.plot_dir, "model_agreement.png"),
            )
        plot_hard_doc_narratives(
            characterization,
            os.path.join(args.plot_dir, "hard_doc_narratives.png"),
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())

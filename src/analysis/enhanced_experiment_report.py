#!/usr/bin/env python3
"""
Enhanced Experiment Results Report — hierarchy-aware evaluation tool.

This is the analysis tool described in ``specs/agora_emnlp_spec.md`` and
``specs/agora_hierarchical_metrics_spec.md``. It auto-discovers all
experiments in ``results/experiments/``, evaluates every successful run
against the SemEval-2025 dev-set ground truth, and computes the full
hierarchy-aware metric bundle for each run:

- F1-samples (SemEval primary metric, set-based) at narrative & sub-narrative
  levels — kept for back-compatibility with existing reports.
- Hierarchical Precision / Recall / F1 (hP / hR / hF).
- Hierarchical Consistency Rate (HCR).
- Error severity distribution (sibling / same-domain / cross-domain /
  hallucination), at both narrative and sub-narrative levels.
- Inter-run agreement (mean pairwise Jaccard) per experiment.
- Information Contrast Model (ICM, normalised).
- Bistochastic-normalised Transport Confusion Matrix (TCM) at the
  narrative level for the top experiments, plus the top-K confused pairs.
- Bootstrap 95% CIs for F1-samples and hF (per-document resampling).
- Pairwise paired t-test + Wilcoxon between methods.

Outputs:

- ``--output``  Markdown summary report
- ``--json-output``  Raw structured results for downstream tooling
- ``--tcm-output-dir``  Per-experiment narrative-level TCM matrices
  (raw + bistochastic normalisations) saved as ``.npz`` + a JSON of the
  top confused pairs.

Usage:

    python -m src.analysis.enhanced_experiment_report \\
        --experiments-dir results/experiments/ \\
        --ground-truth-dir data/dev-documents_4_December/ \\
        --output results/analysis/enhanced_experiment_summary.md \\
        --json-output results/analysis/enhanced_experiment_summary.json \\
        --tcm-output-dir results/analysis/tcm/

    # Filter to specific languages and methods
    python -m src.analysis.enhanced_experiment_report \\
        --experiments-dir results/experiments/ \\
        --languages EN BG --methods baseline agora_5 \\
        --output results/analysis/en_bg_subset.md
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
from scipy import stats

# Allow running both as a module (python -m src.analysis...) and as a script.
try:
    from .taxonomy_tree import TaxonomyTree, load_default_tree
    from . import hierarchical_metrics as hm
    from . import bistochastic_tcm as bt
    from .experiment_results_report import (
        discover_experiments,
        load_annotations,
        compute_f1_samples_manual,
        METHOD_DISPLAY,
        MODEL_DISPLAY,
    )
except ImportError:  # pragma: no cover
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from src.analysis.taxonomy_tree import TaxonomyTree, load_default_tree
    from src.analysis import hierarchical_metrics as hm
    from src.analysis import bistochastic_tcm as bt
    from src.analysis.experiment_results_report import (
        discover_experiments,
        load_annotations,
        compute_f1_samples_manual,
        METHOD_DISPLAY,
        MODEL_DISPLAY,
    )


# ---------------------------------------------------------------------------
# Per-run evaluation
# ---------------------------------------------------------------------------

def parse_run_to_doc_labels(
    annotations: Dict[str, Dict[str, List[str]]],
    files: Sequence[str],
    tree: TaxonomyTree,
) -> List[hm.DocLabels]:
    """Convert raw per-document annotations to taxonomy-tree label sets."""
    out: List[hm.DocLabels] = []
    for f in files:
        rec = annotations.get(f, {"narratives": [], "subnarratives": []})
        narrs, subs = tree.parse_labels(
            rec.get("narratives", []),
            rec.get("subnarratives", []),
        )
        out.append({"narratives": narrs, "subnarratives": subs})
    return out


def evaluate_run_full(
    prediction_file: str,
    ground_truth: Dict[str, Dict[str, List[str]]],
    tree: TaxonomyTree,
) -> Optional[Dict[str, Any]]:
    """Compute the full hierarchical metric bundle for a single run."""
    if not os.path.exists(prediction_file):
        return None
    predictions = load_annotations(prediction_file)
    common = sorted(set(ground_truth.keys()) & set(predictions.keys()))
    if not common:
        return None

    y_true = parse_run_to_doc_labels(ground_truth, common, tree)
    y_pred = parse_run_to_doc_labels(predictions, common, tree)

    # Flat F1-samples (set-based, SemEval official)
    f1_narr = compute_f1_samples_manual(
        [g["narratives"] for g in y_true],
        [p["narratives"] for p in y_pred],
    )
    f1_sub = compute_f1_samples_manual(
        [g["subnarratives"] for g in y_true],
        [p["subnarratives"] for p in y_pred],
    )

    # Hierarchical bundle
    bundle = hm.compute_hierarchical_bundle(
        y_true, y_pred, tree, bootstrap=True, n_bootstrap=300
    )

    # ICM (normalised, dataset-level node frequencies)
    freq, n_docs = hm.build_node_frequencies(y_true, tree)
    icm = hm.icm_normalised(y_true, y_pred, tree, freq=freq, n_docs=n_docs)

    return {
        "n_files": len(common),
        "common_files": common,
        "y_true": y_true,
        "y_pred": y_pred,
        "f1_samples_narr": f1_narr,
        "f1_samples_sub": f1_sub,
        "hP": bundle["hP"],
        "hR": bundle["hR"],
        "hF": bundle["hF"],
        "hF_per_doc_mean": bundle["hF_per_doc_mean"],
        "hF_ci": bundle.get("hF_ci"),
        "hcr": bundle["hcr"],
        "error_severity_subnarr": bundle["error_severity_subnarr"],
        "error_severity_narr": bundle["error_severity_narr"],
        "icm_norm": icm,
    }


# ---------------------------------------------------------------------------
# Aggregate per experiment
# ---------------------------------------------------------------------------

def evaluate_experiment(
    experiment: Dict[str, Any],
    ground_truth_dir: str,
    tree: TaxonomyTree,
) -> Dict[str, Any]:
    """Evaluate every successful run of an experiment with the full bundle."""
    manifest = experiment["manifest"]
    meta = experiment["meta"]
    lang = meta["language"]
    gt_file = os.path.join(ground_truth_dir, lang, "subtask-3-dominant-narratives.txt")
    if not os.path.exists(gt_file):
        return {"error": f"Ground truth not found for {lang}: {gt_file}"}
    ground_truth = load_annotations(gt_file)

    runs_results: List[Dict[str, Any]] = []
    experiment_dir = experiment.get("dir", "")
    for run in manifest.get("runs", []):
        if run.get("status") != "success":
            continue
        output_file = run.get("output_file") or ""
        if not os.path.exists(output_file):
            fb = os.path.join(
                experiment_dir, f"run_{run.get('run_id', 1)}", "results.txt"
            )
            if os.path.exists(fb):
                output_file = fb
            else:
                continue
        result = evaluate_run_full(output_file, ground_truth, tree)
        if result is None:
            continue
        result["run_id"] = run.get("run_id")
        result["seed"] = run.get("seed")
        runs_results.append(result)

    if not runs_results:
        return {"error": "no successful runs evaluable", "meta": meta}

    # Aggregate per metric
    def col(name: str) -> List[float]:
        return [r[name] for r in runs_results]

    def agg(scores: List[float]) -> Dict[str, float]:
        if not scores:
            return {"mean": 0.0, "std": 0.0, "n": 0}
        a = np.array(scores, dtype=float)
        return {
            "mean": float(a.mean()),
            "std": float(a.std(ddof=1)) if len(a) > 1 else 0.0,
            "n": len(a),
            "scores": [float(x) for x in a],
        }

    aggregated: Dict[str, Dict[str, float]] = {
        "f1_samples_narr": agg(col("f1_samples_narr")),
        "f1_samples_sub": agg(col("f1_samples_sub")),
        "hP": agg(col("hP")),
        "hR": agg(col("hR")),
        "hF": agg(col("hF")),
        "hcr": agg(col("hcr")),
        "icm_norm": agg(col("icm_norm")),
    }

    # Aggregate error severity (mean over runs)
    sev_keys = ("sibling", "same_domain", "cross_domain", "hallucination")
    sev_subnarr = {
        k: float(np.mean([r["error_severity_subnarr"][k] for r in runs_results]))
        for k in sev_keys
    }
    sev_narr = {
        k: float(np.mean([r["error_severity_narr"][k] for r in runs_results]))
        for k in sev_keys
    }
    aggregated["error_severity_subnarr"] = sev_subnarr
    aggregated["error_severity_narr"] = sev_narr

    # Inter-run agreement
    if len(runs_results) >= 2:
        inter_sub = hm.inter_run_agreement(
            [r["y_pred"] for r in runs_results], level="subnarratives"
        )
        inter_narr = hm.inter_run_agreement(
            [r["y_pred"] for r in runs_results], level="narratives"
        )
    else:
        inter_sub = inter_narr = 1.0
    aggregated["inter_run_agreement_sub"] = inter_sub
    aggregated["inter_run_agreement_narr"] = inter_narr

    # Sanity check: hF should be >= flat F1 sub-narrative samples on average
    if (
        aggregated["hF"]["mean"] + 1e-9 < aggregated["f1_samples_sub"]["mean"]
        and aggregated["f1_samples_sub"]["mean"] > 0
    ):
        aggregated["sanity_warning"] = (
            f"hF mean {aggregated['hF']['mean']:.3f} < "
            f"flat F1-sub {aggregated['f1_samples_sub']['mean']:.3f}; "
            "ancestor augmentation should not strictly decrease F1 micro-averaged."
        )

    # Bistochastic TCM aggregated over all runs (concatenate y_true / y_pred)
    all_true = [doc for r in runs_results for doc in r["y_true"]]
    all_pred = [doc for r in runs_results for doc in r["y_pred"]]
    M_raw, narr_order = bt.build_narrative_tcm(all_true, all_pred, tree)
    norms = bt.all_normalisations(M_raw)
    pairs = bt.top_confused_pairs(norms["raw"], norms["bis"], narr_order, tree, top_k=10)

    return {
        "experiment_id": experiment["experiment_id"],
        "meta": meta,
        "n_successful_runs": len(runs_results),
        "n_total_runs": len(manifest.get("runs", [])),
        "aggregated": aggregated,
        "tcm": {
            "narratives": narr_order,
            "raw": norms["raw"],
            "row": norms["row"],
            "col": norms["col"],
            "bis": norms["bis"],
            "top_confused_pairs": [p.as_dict() for p in pairs],
        },
        # Keep per-run f1_samples for paired significance tests downstream.
        "per_run_scores": {
            "f1_samples_narr": col("f1_samples_narr"),
            "f1_samples_sub": col("f1_samples_sub"),
            "hF": col("hF"),
        },
    }


# ---------------------------------------------------------------------------
# Pairwise significance tests
# ---------------------------------------------------------------------------

def paired_test(a: List[float], b: List[float]) -> Dict[str, float]:
    if len(a) != len(b) or len(a) < 2:
        return {"p_ttest": 1.0, "p_wilcoxon": 1.0, "cohens_d": 0.0, "n": len(a)}
    aa, bb = np.array(a), np.array(b)
    try:
        _, p_t = stats.ttest_rel(aa, bb)
    except Exception:
        p_t = 1.0
    try:
        diffs = aa - bb
        if np.all(diffs == 0):
            p_w = 1.0
        else:
            _, p_w = stats.wilcoxon(aa, bb)
    except Exception:
        p_w = 1.0
    diffs = aa - bb
    sd = float(np.std(diffs, ddof=1)) if len(diffs) > 1 else 0.0
    d = float(diffs.mean() / sd) if sd > 0 else 0.0
    return {
        "p_ttest": float(p_t),
        "p_wilcoxon": float(p_w),
        "mean_diff": float(diffs.mean()),
        "cohens_d": d,
        "n": len(a),
    }


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def fmt(mean: Optional[float], std: Optional[float] = None, p: int = 3) -> str:
    if mean is None:
        return "N/A"
    if std is None:
        return f"{mean:.{p}f}"
    return f"{mean:.{p}f} \u00b1 {std:.{p}f}"


def render_markdown_report(
    evaluated: List[Dict[str, Any]],
    sig_tests: Dict[Tuple[str, str], Dict[str, float]],
) -> str:
    out: List[str] = []
    out.append("# Enhanced Experiment Results Report")
    out.append("")
    out.append(f"_Generated_: {datetime.now().strftime('%Y-%m-%d %H:%M')}  ")
    n_exp = sum(1 for e in evaluated if "error" not in e)
    out.append(f"_Experiments evaluated_: **{n_exp}** of {len(evaluated)}")
    out.append("")

    out.append("## Methodology")
    out.append("")
    out.append(
        "Each experiment is evaluated using the **all-runs averaging** strategy: "
        "every successful run is scored independently against the SemEval-2025 "
        "Task 10 dev-set ground truth, then mean and standard deviation are "
        "reported across runs."
    )
    out.append("")
    out.append("Metrics computed:")
    out.append("")
    out.append(
        "| Metric | Description |\n"
        "|--------|-------------|\n"
        "| F1-samples (narr / sub) | SemEval primary metric, set-based per-document F1, averaged. |\n"
        "| hP / hR / hF | Hierarchical P/R/F1 with ancestor augmentation (Kiritchenko et al. 2006). |\n"
        "| HCR | Hierarchical Consistency Rate \u2014 fraction of docs with no orphan sub-narratives. |\n"
        "| ICM (norm.) | Information Contrast Model normalised by ICM(gold,gold) (Amig\u00f3 & Delgado 2022). |\n"
        "| Sibling / Same-domain / Cross-domain / Hallucination | Error severity from LCA depth of false positives. |\n"
        "| Inter-run Jaccard | Pairwise Jaccard between runs of the same experiment, averaged over docs. |\n"
        "| TCM (bis) | Transport Confusion Matrix at narrative level, bistochastic-normalised via IPF. |\n"
    )
    out.append("")

    # Group by language
    by_lang: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for ev in evaluated:
        if "error" in ev:
            continue
        by_lang[ev["meta"]["language"]].append(ev)

    out.append("## Results by Language")
    out.append("")
    for lang in sorted(by_lang.keys()):
        out.append(f"### {lang}")
        out.append("")
        out.append(
            "| Experiment | Model | Method | Runs | F1\u2090 narr | F1\u2090 sub | hF | HCR | ICM | InterRun (sub) |"
        )
        out.append("|---|---|---|---|---|---|---|---|---|---|")
        items = sorted(by_lang[lang], key=lambda e: -e["aggregated"]["hF"]["mean"])
        for ev in items:
            agg = ev["aggregated"]
            meta = ev["meta"]
            out.append(
                "| {eid} | {model} | {method} | {n} | {fn} | {fs} | {hf} | {hcr} | {icm} | {ir} |".format(
                    eid=ev["experiment_id"],
                    model=meta.get("model_display", meta.get("model_key", "?")),
                    method=meta.get("method_display", meta.get("method", "?")),
                    n=ev["n_successful_runs"],
                    fn=fmt(agg["f1_samples_narr"]["mean"], agg["f1_samples_narr"]["std"]),
                    fs=fmt(agg["f1_samples_sub"]["mean"], agg["f1_samples_sub"]["std"]),
                    hf=fmt(agg["hF"]["mean"], agg["hF"]["std"]),
                    hcr=fmt(agg["hcr"]["mean"], agg["hcr"]["std"]),
                    icm=fmt(agg["icm_norm"]["mean"], agg["icm_norm"]["std"]),
                    ir=fmt(agg["inter_run_agreement_sub"]),
                )
            )
        out.append("")

        out.append(
            "_Error severity (sub-narrative false positives, mean over runs)_:"
        )
        out.append("")
        out.append("| Experiment | Sibling | Same-dom | Cross-dom | Hallucinations |")
        out.append("|---|---|---|---|---|")
        for ev in items:
            sev = ev["aggregated"]["error_severity_subnarr"]
            out.append(
                f"| {ev['experiment_id']} | {sev['sibling']:.2%} | "
                f"{sev['same_domain']:.2%} | {sev['cross_domain']:.2%} | "
                f"{sev['hallucination']:.2%} |"
            )
        out.append("")

    # Pairwise significance: best baseline vs Agora variants per (lang, model)
    if sig_tests:
        out.append("## Pairwise Significance Tests (paired, hF)")
        out.append("")
        out.append("| A vs B | n | mean diff | Cohen's d | p (t-test) | p (Wilcoxon) |")
        out.append("|---|---|---|---|---|---|")
        for (a, b), stats_d in sorted(sig_tests.items()):
            star = ""
            if stats_d["p_wilcoxon"] < 0.001:
                star = "***"
            elif stats_d["p_wilcoxon"] < 0.01:
                star = "**"
            elif stats_d["p_wilcoxon"] < 0.05:
                star = "*"
            out.append(
                f"| {a} vs {b} | {stats_d['n']} | "
                f"{stats_d['mean_diff']:+.3f} | {stats_d['cohens_d']:+.2f} | "
                f"{stats_d['p_ttest']:.4f} | {stats_d['p_wilcoxon']:.4f} {star} |"
            )
        out.append("")

    # Top confused pairs from selected experiments (best per language)
    out.append("## Top Confused Narrative Pairs (bistochastic TCM)")
    out.append("")
    out.append(
        "The bistochastic normalisation removes class-frequency bias from "
        "the raw TCM, isolating purely structural confusion between "
        "narratives. Pairs are reported per language for the best-hF "
        "experiment in that language."
    )
    out.append("")
    for lang in sorted(by_lang.keys()):
        items = sorted(by_lang[lang], key=lambda e: -e["aggregated"]["hF"]["mean"])
        if not items:
            continue
        best = items[0]
        out.append(f"### {lang} \u2014 {best['experiment_id']}")
        out.append("")
        out.append("| Gold narrative | Predicted as | bis(TCM) mass | raw mass | same-domain |")
        out.append("|---|---|---|---|---|")
        for p in best["tcm"]["top_confused_pairs"][:8]:
            out.append(
                f"| {p['gold']} | {p['predicted']} | {p['bis_mass']:.4f} | "
                f"{p['raw_mass']:.4f} | {'yes' if p['same_domain'] else 'no'} |"
            )
        out.append("")

    return "\n".join(out)


# ---------------------------------------------------------------------------
# Significance tests over all (lang, model) groups
# ---------------------------------------------------------------------------

def compute_significance_pairs(
    evaluated: List[Dict[str, Any]],
) -> Dict[Tuple[str, str], Dict[str, float]]:
    """For each (language, model) group, compare every method pair against
    every other method pair using their per-run hF scores."""
    groups: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for ev in evaluated:
        if "error" in ev:
            continue
        meta = ev["meta"]
        groups[(meta["language"], meta.get("model_key", "?"))].append(ev)

    pairs: Dict[Tuple[str, str], Dict[str, float]] = {}
    for (lang, model), exps in groups.items():
        if len(exps) < 2:
            continue
        for i in range(len(exps)):
            for j in range(i + 1, len(exps)):
                a, b = exps[i], exps[j]
                a_scores = a["per_run_scores"]["hF"]
                b_scores = b["per_run_scores"]["hF"]
                # Pair on common run count
                n = min(len(a_scores), len(b_scores))
                if n < 2:
                    continue
                d = paired_test(a_scores[:n], b_scores[:n])
                pairs[(a["experiment_id"], b["experiment_id"])] = d
    return pairs


# ---------------------------------------------------------------------------
# JSON / TCM serialisation
# ---------------------------------------------------------------------------

def serialise_for_json(evaluated: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for ev in evaluated:
        if "error" in ev:
            out.append(ev)
            continue
        copy: Dict[str, Any] = {
            "experiment_id": ev["experiment_id"],
            "meta": ev["meta"],
            "n_successful_runs": ev["n_successful_runs"],
            "n_total_runs": ev["n_total_runs"],
            "aggregated": ev["aggregated"],
            "per_run_scores": ev["per_run_scores"],
        }
        copy["tcm_top_confused_pairs"] = ev["tcm"]["top_confused_pairs"]
        out.append(copy)
    return out


def save_tcm_matrices(evaluated: List[Dict[str, Any]], output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    for ev in evaluated:
        if "error" in ev:
            continue
        eid = ev["experiment_id"]
        tcm = ev["tcm"]
        np.savez(
            os.path.join(output_dir, f"{eid}_tcm.npz"),
            raw=tcm["raw"],
            row=tcm["row"],
            col=tcm["col"],
            bis=tcm["bis"],
            narratives=np.array(tcm["narratives"], dtype=object),
        )
        with open(os.path.join(output_dir, f"{eid}_top_confused.json"), "w", encoding="utf-8") as f:
            json.dump(tcm["top_confused_pairs"], f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Enhanced experiment results report with hierarchy-aware metrics, "
            "bistochastic TCM analysis, and inter-run agreement."
        )
    )
    parser.add_argument(
        "--experiments-dir",
        default="results/experiments/",
        help="Root directory containing experiment subdirectories.",
    )
    parser.add_argument(
        "--ground-truth-dir",
        default="data/dev-documents_4_December/",
        help="Root directory containing per-language gold annotation files.",
    )
    parser.add_argument(
        "--output",
        default="results/analysis/enhanced_experiment_summary.md",
        help="Markdown report output path.",
    )
    parser.add_argument(
        "--json-output",
        default=None,
        help="Optional JSON dump of structured results.",
    )
    parser.add_argument(
        "--tcm-output-dir",
        default=None,
        help="Optional directory to save per-experiment TCM matrices.",
    )
    parser.add_argument(
        "--languages",
        nargs="*",
        default=None,
        help="Filter experiments by language code (EN BG HI PT RU).",
    )
    parser.add_argument(
        "--methods",
        nargs="*",
        default=None,
        help="Filter experiments by method prefix (baseline, agora_5, ...).",
    )
    parser.add_argument(
        "--models",
        nargs="*",
        default=None,
        help="Filter experiments by model substring (deepseek, mistral, ...).",
    )
    parser.add_argument(
        "--taxonomy",
        default=None,
        help="Override path to taxonomy JSON (defaults to data/taxonomy.json).",
    )
    args = parser.parse_args()

    tree = (
        TaxonomyTree.from_json(args.taxonomy) if args.taxonomy else load_default_tree()
    )
    print(
        f"[taxonomy] domains={len(tree.domains)} narratives={len(tree.narratives)} "
        f"sub-narratives={len(tree.subnarratives)}"
    )

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
                # also accept exact method id
                if method not in args.methods:
                    return False
        if args.models:
            mk = (meta.get("model_key") or "").lower()
            md = (meta.get("model_display") or "").lower()
            if not any(s.lower() in mk or s.lower() in md for s in args.models):
                return False
        return True

    experiments = [e for e in experiments if keep(e)]
    print(f"[filter]   {len(experiments)} experiments after filtering")

    evaluated: List[Dict[str, Any]] = []
    for exp in experiments:
        eid = exp["experiment_id"]
        try:
            res = evaluate_experiment(exp, args.ground_truth_dir, tree)
            if "error" in res:
                print(f"  [skip] {eid}: {res['error']}")
            else:
                hf = res["aggregated"]["hF"]["mean"]
                hcr = res["aggregated"]["hcr"]["mean"]
                print(
                    f"  [ok]   {eid}: hF={hf:.3f} HCR={hcr:.3f} "
                    f"runs={res['n_successful_runs']}"
                )
            evaluated.append(res)
        except Exception as e:  # pragma: no cover - defensive
            print(f"  [err]  {eid}: {e}")

    sig_tests = compute_significance_pairs(evaluated)

    md = render_markdown_report(evaluated, sig_tests)
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[write] markdown report -> {args.output}")

    if args.json_output:
        os.makedirs(os.path.dirname(args.json_output) or ".", exist_ok=True)
        with open(args.json_output, "w", encoding="utf-8") as f:
            json.dump(serialise_for_json(evaluated), f, indent=2, ensure_ascii=False)
        print(f"[write] json results  -> {args.json_output}")

    if args.tcm_output_dir:
        save_tcm_matrices(evaluated, args.tcm_output_dir)
        print(f"[write] TCM matrices  -> {args.tcm_output_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

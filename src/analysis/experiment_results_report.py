#!/usr/bin/env python3
"""
Comprehensive Experiment Results Report Generator.

Auto-discovers experiments, evaluates all runs against ground truth,
computes mean/std/CI across runs, runs pairwise significance tests,
and generates a Markdown report documenting methodology and results.

Usage:
    # Full report across all experiments
    python experiment_results_report.py --experiments-dir results/experiments/ \\
        --output results/analysis/experiment_summary.md

    # Filter by language or model
    python experiment_results_report.py --experiments-dir results/experiments/ \\
        --languages EN BG --models deepseek mistral \\
        --output results/analysis/en_bg_comparison.md

    # Also save raw JSON data
    python experiment_results_report.py --experiments-dir results/experiments/ \\
        --output results/analysis/experiment_summary.md \\
        --json-output results/analysis/experiment_summary.json
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
import yaml
from scipy import stats
from sklearn.metrics import f1_score
from sklearn.preprocessing import MultiLabelBinarizer


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

GROUND_TRUTH_PATTERN = "data/dev-documents_4_December/{lang}/subtask-3-dominant-narratives.txt"

# Method display names
METHOD_DISPLAY = {
    "agora_1": "Agora (1-agent)",
    "agora": "Agora (intersection)",
    "agora_5": "Agora (5-agent intersection)",
    "agora_7": "Agora (7-agent intersection)",
    "agora_majority": "Agora (majority)",
    "agora_union": "Agora (union)",
    "actor_critic": "Actor-Critic",
    "baseline": "Baseline",
    "retrieval": "Retrieval-augmented",
    "retrieval_agora": "Retrieval + Agora",
    "mdeberta_baseline": "mDeBERTa (fine-tuned)",
}

# Model display names
MODEL_DISPLAY = {
    "openai:gpt-5-nano": "GPT-5 Nano",
    "google_genai:gemini-2.5-flash": "Gemini 2.5 Flash",
    "google_genai:gemini-2.0-flash": "Gemini 2.0 Flash",
    "deepseek:deepseek-chat": "DeepSeek V3",
    "mistral:mistral-small-latest": "Mistral Small",
    "mistralai:mistral-large-latest": "Mistral Large",
    "together_ai:meta-llama/Llama-3.3-70B-Instruct-Turbo": "Llama 3.3 70B",
    "together:meta-llama/Llama-3.3-70B-Instruct-Turbo": "Llama 3.3 70B",
    "mdeberta:microsoft/mdeberta-v3-base": "mDeBERTa v3 (fine-tuned)",
}


def parse_labels(label_string: str) -> List[str]:
    """Parse semicolon-separated labels into a list."""
    label_string = label_string.strip()
    if not label_string or label_string.lower() in ("none", "other"):
        return ["Other"] if label_string.lower() == "other" else []
    return [l.strip() for l in label_string.split(";") if l.strip()]


def load_annotations(filepath: str) -> Dict[str, Dict[str, List[str]]]:
    """Load ground truth / prediction annotations from tab-separated file."""
    annotations = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                filename = parts[0]
                narratives = parse_labels(parts[1]) if len(parts) > 1 else []
                subnarratives = parse_labels(parts[2]) if len(parts) > 2 else []
                annotations[filename] = {
                    "narratives": narratives,
                    "subnarratives": subnarratives,
                }
    return annotations


def compute_f1_scores(
    y_true: List[List[str]], y_pred: List[List[str]]
) -> Dict[str, float]:
    """Compute F1 macro, micro, and samples scores using sklearn."""
    all_labels = set()
    for labels in y_true + y_pred:
        all_labels.update(labels)

    if not all_labels:
        return {"f1_macro": 0.0, "f1_micro": 0.0, "f1_samples": 0.0}

    mlb = MultiLabelBinarizer()
    mlb.fit([list(all_labels)])

    y_true_bin = mlb.transform(y_true)
    y_pred_bin = mlb.transform(y_pred)

    return {
        "f1_macro": float(
            f1_score(y_true_bin, y_pred_bin, average="macro", zero_division=0)
        ),
        "f1_micro": float(
            f1_score(y_true_bin, y_pred_bin, average="micro", zero_division=0)
        ),
        "f1_samples": float(
            f1_score(y_true_bin, y_pred_bin, average="samples", zero_division=0)
        ),
    }


def compute_f1_samples_manual(
    y_true_sets: List[set], y_pred_sets: List[set]
) -> float:
    """Compute F1-samples manually (set-based, the SemEval official metric)."""
    total_f1 = 0.0
    n = len(y_true_sets)
    for gt, pred in zip(y_true_sets, y_pred_sets):
        intersection = len(gt & pred)
        if len(gt) + len(pred) == 0:
            total_f1 += 1.0
        elif intersection == 0:
            total_f1 += 0.0
        else:
            total_f1 += 2 * intersection / (len(gt) + len(pred))
    return total_f1 / n if n > 0 else 0.0


# ---------------------------------------------------------------------------
# Experiment discovery and config parsing
# ---------------------------------------------------------------------------


def discover_experiments(experiments_dir: str) -> List[Dict[str, Any]]:
    """
    Auto-discover all experiment directories with valid manifests.

    Returns list of dicts with keys: experiment_id, dir, manifest, config.
    """
    experiments = []
    exp_root = Path(experiments_dir)

    if not exp_root.exists():
        print(f"Error: Experiments directory not found: {experiments_dir}")
        return experiments

    for exp_dir in sorted(exp_root.iterdir()):
        if not exp_dir.is_dir():
            continue
        manifest_path = exp_dir / "experiment_manifest.json"
        if not manifest_path.exists():
            continue

        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read manifest for {exp_dir.name}: {e}")
            continue

        # Parse the config YAML — try manifest path, then local fallbacks
        config = None
        base_config = manifest.get("base_config", "")
        config_candidates = []
        if base_config:
            config_candidates.append(base_config)
        config_candidates.append(str(exp_dir / "base_config.yaml"))
        config_candidates.append(str(exp_dir / "config.yaml"))
        for config_path in config_candidates:
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        config = yaml.safe_load(f)
                    break
                except Exception:
                    pass

        # Extract metadata from config or experiment_id
        experiment_id = manifest.get("experiment_id", exp_dir.name)
        meta = parse_experiment_metadata(experiment_id, config)

        experiments.append(
            {
                "experiment_id": experiment_id,
                "dir": str(exp_dir),
                "manifest": manifest,
                "config": config,
                "meta": meta,
            }
        )

    return experiments


def parse_experiment_metadata(
    experiment_id: str, config: Optional[Dict] = None
) -> Dict[str, str]:
    """
    Extract method, model, language, temperature from experiment_id and config.

    experiment_id format: {method}_{model}_{lang}_{temp}
    e.g. agora_union_gpt5nano_en_t00, baseline_deepseek_bg_t07
    """
    meta = {
        "method": "unknown",
        "method_display": "Unknown",
        "model_key": "unknown",
        "model_display": "Unknown",
        "language": "unknown",
        "temperature": "unknown",
        "num_narrative_agents": "?",
        "num_subnarrative_agents": "?",
        "narrative_aggregation": "?",
        "subnarrative_aggregation": "?",
        "hierarchical_strategy": "?",
        "enable_validation": False,
        "max_tokens": "?",
    }

    # Try extracting from config first (most reliable)
    if config:
        model_name = config.get("model_name", "")
        meta["model_display"] = MODEL_DISPLAY.get(model_name, model_name)
        meta["model_key"] = model_name
        meta["temperature"] = str(config.get("temperature", "?"))
        meta["num_narrative_agents"] = str(
            config.get("num_narrative_agents", "?")
        )
        meta["num_subnarrative_agents"] = str(
            config.get("num_subnarrative_agents", "?")
        )
        meta["narrative_aggregation"] = config.get(
            "narrative_aggregation_method", "?"
        )
        meta["subnarrative_aggregation"] = config.get(
            "subnarrative_aggregation_method", "?"
        )
        meta["hierarchical_strategy"] = config.get(
            "hierarchical_strategy", "?"
        )
        meta["enable_validation"] = config.get("enable_validation", False)
        meta["max_tokens"] = str(config.get("max_tokens", "?"))

        # Extract language from input_folder
        input_folder = config.get("input_folder", "")
        lang_match = re.search(
            r"dev-documents_4_December/(\w+)/", input_folder
        )
        if lang_match:
            meta["language"] = lang_match.group(1).upper()

    # Parse method from experiment_id
    known_methods = [
        "mdeberta_baseline",
        "agora_majority",
        "agora_union",
        "agora_1",
        "agora_5",
        "agora_7",
        "agora",
        "actor_critic",
        "baseline",
        "retrieval_agora",
        "retrieval",
    ]
    for method in known_methods:
        if experiment_id.startswith(method + "_"):
            meta["method"] = method
            meta["method_display"] = METHOD_DISPLAY.get(method, method)
            break

    # Parse language from experiment_id (fallback)
    if meta["language"] == "unknown":
        lang_match = re.search(r"_(en|bg|hi|pt|ru)_", experiment_id, re.I)
        if lang_match:
            meta["language"] = lang_match.group(1).upper()

    # Parse temperature from experiment_id (fallback)
    if meta["temperature"] == "unknown":
        temp_match = re.search(r"_t(\d+)", experiment_id)
        if temp_match:
            t_val = int(temp_match.group(1))
            meta["temperature"] = str(t_val / 10 if t_val > 0 else 0.0)

    return meta


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------


def evaluate_single_run(
    prediction_file: str, ground_truth: Dict[str, Dict[str, List[str]]]
) -> Optional[Dict[str, Any]]:
    """Evaluate a single run against ground truth."""
    if not os.path.exists(prediction_file):
        return None

    predictions = load_annotations(prediction_file)
    common_files = sorted(set(ground_truth.keys()) & set(predictions.keys()))

    if not common_files:
        return None

    # Compute sklearn-based F1 metrics
    y_true_narr = [ground_truth[f]["narratives"] for f in common_files]
    y_pred_narr = [predictions[f]["narratives"] for f in common_files]
    y_true_sub = [ground_truth[f]["subnarratives"] for f in common_files]
    y_pred_sub = [predictions[f]["subnarratives"] for f in common_files]

    narr_scores = compute_f1_scores(y_true_narr, y_pred_narr)
    sub_scores = compute_f1_scores(y_true_sub, y_pred_sub)

    # Also compute manual F1-samples (set-based, closer to SemEval official)
    narr_f1_manual = compute_f1_samples_manual(
        [set(g) for g in y_true_narr], [set(p) for p in y_pred_narr]
    )
    sub_f1_manual = compute_f1_samples_manual(
        [set(g) for g in y_true_sub], [set(p) for p in y_pred_sub]
    )

    return {
        "n_files": len(common_files),
        "n_gold": len(ground_truth),
        "n_predicted": len(predictions),
        "narratives": {**narr_scores, "f1_samples_manual": narr_f1_manual},
        "subnarratives": {**sub_scores, "f1_samples_manual": sub_f1_manual},
    }


def evaluate_all_runs(
    experiment: Dict[str, Any], ground_truth_dir: str
) -> Dict[str, Any]:
    """
    Evaluate ALL runs of an experiment against ground truth.

    Strategy: evaluate every successful run independently, then aggregate.
    This is the 'all-runs averaging' strategy — we report mean and std across
    all N successful runs rather than picking a single best/random run.

    Returns dict with per-metric lists of scores and aggregated stats.
    """
    manifest = experiment["manifest"]
    meta = experiment["meta"]
    lang = meta["language"]

    # Find ground truth file
    gt_file = os.path.join(
        ground_truth_dir,
        lang,
        "subtask-3-dominant-narratives.txt",
    )
    if not os.path.exists(gt_file):
        # Try alternative paths
        gt_file = GROUND_TRUTH_PATTERN.format(lang=lang)

    if not os.path.exists(gt_file):
        return {"error": f"Ground truth not found for {lang}: {gt_file}"}

    ground_truth = load_annotations(gt_file)

    # Metric keys we track
    metric_keys = [
        "narratives_f1_macro",
        "narratives_f1_micro",
        "narratives_f1_samples",
        "narratives_f1_samples_manual",
        "subnarratives_f1_macro",
        "subnarratives_f1_micro",
        "subnarratives_f1_samples",
        "subnarratives_f1_samples_manual",
    ]

    metrics = {k: [] for k in metric_keys}
    run_details = []
    n_successful = 0
    experiment_dir = experiment.get("dir", "")

    for run in manifest.get("runs", []):
        if run.get("status") != "success":
            continue

        output_file = run.get("output_file")
        if not output_file:
            continue
        # If absolute path doesn't exist (e.g. manifest from remote server),
        # try resolving relative to the experiment directory
        if not os.path.exists(output_file):
            run_dir = os.path.join(experiment_dir, f"run_{run.get('run_id', 1)}")
            fallback = os.path.join(run_dir, "results.txt")
            if os.path.exists(fallback):
                output_file = fallback
            else:
                continue

        result = evaluate_single_run(output_file, ground_truth)
        if result is None:
            continue

        n_successful += 1
        run_details.append(
            {
                "run_id": run.get("run_id"),
                "seed": run.get("seed"),
                "n_files": result["n_files"],
                "narratives": result["narratives"],
                "subnarratives": result["subnarratives"],
            }
        )

        # Collect metrics
        metrics["narratives_f1_macro"].append(result["narratives"]["f1_macro"])
        metrics["narratives_f1_micro"].append(result["narratives"]["f1_micro"])
        metrics["narratives_f1_samples"].append(
            result["narratives"]["f1_samples"]
        )
        metrics["narratives_f1_samples_manual"].append(
            result["narratives"]["f1_samples_manual"]
        )
        metrics["subnarratives_f1_macro"].append(
            result["subnarratives"]["f1_macro"]
        )
        metrics["subnarratives_f1_micro"].append(
            result["subnarratives"]["f1_micro"]
        )
        metrics["subnarratives_f1_samples"].append(
            result["subnarratives"]["f1_samples"]
        )
        metrics["subnarratives_f1_samples_manual"].append(
            result["subnarratives"]["f1_samples_manual"]
        )

    # Aggregate stats
    aggregated = {}
    for key, scores in metrics.items():
        if not scores:
            aggregated[key] = {
                "mean": None,
                "std": None,
                "ci_lower": None,
                "ci_upper": None,
                "n_runs": 0,
                "scores": [],
            }
            continue

        scores_arr = np.array(scores)
        mean = float(np.mean(scores_arr))
        std = float(np.std(scores_arr, ddof=1)) if len(scores_arr) > 1 else 0.0

        # Bootstrap CI
        ci_lower, ci_upper = bootstrap_ci(scores_arr)

        aggregated[key] = {
            "mean": mean,
            "std": std,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "n_runs": len(scores),
            "scores": scores,
        }

    return {
        "experiment_id": experiment["experiment_id"],
        "meta": meta,
        "ground_truth_file": gt_file,
        "n_successful_runs": n_successful,
        "n_total_runs": len(manifest.get("runs", [])),
        "metrics": aggregated,
        "run_details": run_details,
    }


# ---------------------------------------------------------------------------
# Statistical functions
# ---------------------------------------------------------------------------


def bootstrap_ci(
    scores: np.ndarray,
    confidence: float = 0.95,
    n_bootstrap: int = 10000,
    seed: int = 42,
) -> Tuple[float, float]:
    """Compute bootstrap confidence interval. Returns (lower, upper)."""
    if len(scores) < 2:
        return (float(scores[0]) if len(scores) == 1 else 0.0, float(scores[0]) if len(scores) == 1 else 0.0)

    rng = np.random.RandomState(seed)
    n = len(scores)
    bootstrap_means = np.array(
        [np.mean(rng.choice(scores, size=n, replace=True)) for _ in range(n_bootstrap)]
    )
    alpha = 1 - confidence
    lower = float(np.percentile(bootstrap_means, alpha / 2 * 100))
    upper = float(np.percentile(bootstrap_means, (1 - alpha / 2) * 100))
    return lower, upper


def paired_significance_test(
    scores_a: List[float], scores_b: List[float]
) -> Dict[str, Any]:
    """
    Run paired significance tests (t-test and Wilcoxon).

    Returns dict with p-values and test statistics.
    """
    a = np.array(scores_a)
    b = np.array(scores_b)

    if len(a) != len(b) or len(a) < 2:
        return {"error": "Insufficient or mismatched data", "p_ttest": 1.0, "p_wilcoxon": 1.0, "cohens_d": 0.0, "effect_size": "negligible"}

    # Paired t-test
    try:
        t_stat, p_ttest = stats.ttest_rel(a, b)
    except Exception:
        t_stat, p_ttest = 0.0, 1.0

    # Wilcoxon signed-rank test
    try:
        diffs = a - b
        if np.all(diffs == 0) or np.sum(diffs != 0) < 2:
            w_stat, p_wilcoxon = 0.0, 1.0
        else:
            w_stat, p_wilcoxon = stats.wilcoxon(a, b)
    except Exception:
        w_stat, p_wilcoxon = 0.0, 1.0

    # Cohen's d for paired samples: d = mean(diff) / std(diff)
    diffs = a - b
    std_diffs = float(np.std(diffs, ddof=1))
    cohens_d = float(np.mean(diffs) / std_diffs) if std_diffs > 0 else 0.0
    abs_d = abs(cohens_d)
    if abs_d >= 0.8:
        effect_size = "large"
    elif abs_d >= 0.5:
        effect_size = "medium"
    elif abs_d >= 0.2:
        effect_size = "small"
    else:
        effect_size = "negligible"

    return {
        "t_statistic": float(t_stat),
        "p_ttest": float(p_ttest),
        "w_statistic": float(w_stat),
        "p_wilcoxon": float(p_wilcoxon),
        "mean_diff": float(np.mean(diffs)),
        "cohens_d": cohens_d,
        "effect_size": effect_size,
        "n_pairs": len(a),
    }


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------


def format_metric(mean, std, ci_lower, ci_upper, fmt=".3f") -> str:
    """Format a metric as mean +/- std [CI_lower, CI_upper]."""
    if mean is None:
        return "N/A"
    return f"{mean:{fmt}} +/- {std:{fmt}} [{ci_lower:{fmt}}, {ci_upper:{fmt}}]"


def format_metric_short(mean, std, fmt=".3f") -> str:
    """Format a metric as mean +/- std."""
    if mean is None:
        return "N/A"
    return f"{mean:{fmt}} +/- {std:{fmt}}"


def significance_marker(p_value: float) -> str:
    """Return significance stars based on p-value."""
    if p_value < 0.001:
        return "***"
    elif p_value < 0.01:
        return "**"
    elif p_value < 0.05:
        return "*"
    return ""


def generate_methodology_section(experiments: List[Dict[str, Any]]) -> str:
    """Generate the methodology section of the report."""
    report = "## Methodology\n\n"

    report += "### Run Strategy\n\n"
    report += (
        "All experiments are evaluated using the **all-runs averaging** strategy: "
        "each experiment consists of N independent runs (typically 5) with different "
        "random seeds. We evaluate every successful run independently against the "
        "gold-standard ground truth, then report the **mean** and **standard deviation** "
        "of each metric across all successful runs. This approach captures the variance "
        "inherent in LLM-based classification and avoids cherry-picking.\n\n"
    )

    report += "### Evaluation Metrics\n\n"
    report += (
        "We report the following metrics at both **narrative** (coarse) and "
        "**subnarrative** (fine) levels:\n\n"
        "| Metric | Description |\n"
        "|--------|-------------|\n"
        "| F1-macro | Unweighted mean of per-label F1 scores (treats rare labels equally) |\n"
        "| F1-micro | Globally aggregated TP/FP/FN, then F1 (favors frequent labels) |\n"
        "| F1-samples | Per-sample F1 averaged across documents (sklearn implementation) |\n"
        "| F1-samples (manual) | Set-based per-sample F1: (2|Y&Y_hat|)/(|Y|+|Y_hat|) averaged (SemEval official) |\n\n"
    )

    report += "### Statistical Testing\n\n"
    report += (
        "For each pair of experiments sharing the same language and temperature, "
        "we perform:\n\n"
        "- **Paired t-test**: Parametric test on per-run scores (assumes normality)\n"
        "- **Wilcoxon signed-rank test**: Non-parametric alternative (no normality assumption)\n"
        "- **Cohen's d**: Standardized effect size (paired: d = mean_diff / std_diff). "
        "Interpretation: |d| < 0.2 negligible, 0.2-0.5 small, 0.5-0.8 medium, >= 0.8 large\n"
        "- **Bootstrap 95% confidence intervals**: 10,000 resamples of per-run means\n\n"
        "Significance levels: * p < 0.05, ** p < 0.01, *** p < 0.001\n\n"
    )

    report += "### Experiment Configurations\n\n"

    # Build config table
    report += (
        "| Experiment | Model | Method | Agents | Aggregation | "
        "Strategy | Temp | Max Tokens | Validation |\n"
        "|------------|-------|--------|--------|-------------|"
        "----------|------|------------|------------|\n"
    )

    for exp in experiments:
        meta = exp.get("meta", {})
        exp_id = exp.get("experiment_id", "?")
        report += (
            f"| {exp_id} "
            f"| {meta.get('model_display', '?')} "
            f"| {meta.get('method_display', '?')} "
            f"| {meta.get('num_narrative_agents', '?')}N/{meta.get('num_subnarrative_agents', '?')}S "
            f"| {meta.get('narrative_aggregation', '?')} "
            f"| {meta.get('hierarchical_strategy', '?')} "
            f"| {meta.get('temperature', '?')} "
            f"| {meta.get('max_tokens', '?')} "
            f"| {'Yes' if meta.get('enable_validation') else 'No'} "
            f"|\n"
        )

    report += "\n"
    return report


def generate_results_tables(
    evaluated: List[Dict[str, Any]],
) -> str:
    """Generate results tables grouped by language."""
    report = "## Results\n\n"

    # Group by language
    by_language = defaultdict(list)
    for ev in evaluated:
        if "error" in ev:
            continue
        lang = ev["meta"]["language"]
        by_language[lang].append(ev)

    for lang in sorted(by_language.keys()):
        exps = by_language[lang]
        report += f"### Language: {lang}\n\n"
        report += f"Ground truth: `{exps[0].get('ground_truth_file', 'N/A')}`\n\n"

        # --- Narrative-level table ---
        report += "#### Narrative-level (Coarse) Metrics\n\n"
        report += (
            "| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |\n"
            "|------------|------|----------|----------|------------|---------------------|\n"
        )

        for ev in sorted(exps, key=lambda e: e["metrics"].get("narratives_f1_samples", {}).get("mean", 0) or 0, reverse=True):
            m = ev["metrics"]
            n_runs = ev["n_successful_runs"]
            exp_id = ev["experiment_id"]

            def _fmt(key):
                d = m.get(key, {})
                if d.get("mean") is None:
                    return "N/A"
                return format_metric_short(d["mean"], d["std"])

            report += (
                f"| {exp_id} | {n_runs} "
                f"| {_fmt('narratives_f1_macro')} "
                f"| {_fmt('narratives_f1_micro')} "
                f"| {_fmt('narratives_f1_samples')} "
                f"| {_fmt('narratives_f1_samples_manual')} "
                f"|\n"
            )

        report += "\n"

        # --- Subnarrative-level table ---
        report += "#### Subnarrative-level (Fine) Metrics\n\n"
        report += (
            "| Experiment | Runs | F1-macro | F1-micro | F1-samples | F1-samples (manual) |\n"
            "|------------|------|----------|----------|------------|---------------------|\n"
        )

        for ev in sorted(exps, key=lambda e: e["metrics"].get("subnarratives_f1_samples", {}).get("mean", 0) or 0, reverse=True):
            m = ev["metrics"]
            n_runs = ev["n_successful_runs"]
            exp_id = ev["experiment_id"]

            def _fmt(key):
                d = m.get(key, {})
                if d.get("mean") is None:
                    return "N/A"
                return format_metric_short(d["mean"], d["std"])

            report += (
                f"| {exp_id} | {n_runs} "
                f"| {_fmt('subnarratives_f1_macro')} "
                f"| {_fmt('subnarratives_f1_micro')} "
                f"| {_fmt('subnarratives_f1_samples')} "
                f"| {_fmt('subnarratives_f1_samples_manual')} "
                f"|\n"
            )

        report += "\n"

        # --- Detailed CI table (key metrics only) ---
        report += "#### Bootstrap 95% Confidence Intervals\n\n"
        report += (
            "| Experiment | Narr F1-samples [95% CI] | Subnarr F1-samples [95% CI] |\n"
            "|------------|--------------------------|-----------------------------|\n"
        )

        for ev in sorted(exps, key=lambda e: e["metrics"].get("narratives_f1_samples", {}).get("mean", 0) or 0, reverse=True):
            m = ev["metrics"]
            exp_id = ev["experiment_id"]

            def _fmt_ci(key):
                d = m.get(key, {})
                if d.get("mean") is None:
                    return "N/A"
                return format_metric(d["mean"], d["std"], d["ci_lower"], d["ci_upper"])

            report += (
                f"| {exp_id} "
                f"| {_fmt_ci('narratives_f1_samples')} "
                f"| {_fmt_ci('subnarratives_f1_samples')} "
                f"|\n"
            )

        report += "\n"

    return report


def generate_significance_section(
    evaluated: List[Dict[str, Any]],
) -> str:
    """Generate pairwise significance tests between experiments."""
    report = "## Pairwise Significance Tests\n\n"
    report += (
        "Paired tests comparing methods within the same language and temperature. "
        "We use the Wilcoxon signed-rank test (non-parametric) as the primary test, "
        "with the paired t-test for reference. Tests are run on per-run F1-samples scores "
        "at the subnarrative level (the primary evaluation metric).\n\n"
    )

    # Group by (language, temperature)
    groups = defaultdict(list)
    for ev in evaluated:
        if "error" in ev:
            continue
        meta = ev["meta"]
        key = (meta["language"], meta["temperature"])
        groups[key].append(ev)

    for (lang, temp), exps in sorted(groups.items()):
        if len(exps) < 2:
            continue

        report += f"### {lang}, Temperature={temp}\n\n"

        # Test on subnarratives_f1_samples (primary metric)
        metric_key = "subnarratives_f1_samples"

        report += (
            "| Method A | Method B | Mean A | Mean B | Diff | "
            "Cohen's d | Effect | p (Wilcoxon) | p (t-test) | Sig. |\n"
            "|----------|----------|--------|--------|------|"
            "-----------|--------|-------------|------------|------|\n"
        )

        for i, exp_a in enumerate(exps):
            for exp_b in exps[i + 1 :]:
                scores_a = exp_a["metrics"].get(metric_key, {}).get("scores", [])
                scores_b = exp_b["metrics"].get(metric_key, {}).get("scores", [])

                if not scores_a or not scores_b:
                    continue

                # Truncate to equal length for paired test
                min_n = min(len(scores_a), len(scores_b))
                if min_n < 2:
                    continue

                result = paired_significance_test(
                    scores_a[:min_n], scores_b[:min_n]
                )

                mean_a = np.mean(scores_a)
                mean_b = np.mean(scores_b)
                diff = mean_a - mean_b
                sig = significance_marker(result["p_wilcoxon"])
                cohens_d = result.get("cohens_d", 0.0)
                effect = result.get("effect_size", "?")

                report += (
                    f"| {exp_a['experiment_id']} "
                    f"| {exp_b['experiment_id']} "
                    f"| {mean_a:.3f} "
                    f"| {mean_b:.3f} "
                    f"| {diff:+.3f} "
                    f"| {cohens_d:+.2f} "
                    f"| {effect} "
                    f"| {result['p_wilcoxon']:.4f} "
                    f"| {result['p_ttest']:.4f} "
                    f"| {sig} "
                    f"|\n"
                )

        report += "\n"

    return report


def generate_cross_model_comparison(
    evaluated: List[Dict[str, Any]],
) -> str:
    """Generate cross-model comparison for the same method and language."""
    report = "## Cross-Model Comparison\n\n"
    report += (
        "Comparing the same method across different backbone models. "
        "Sorted by subnarrative F1-samples (descending).\n\n"
    )

    # Group by (method, language, temperature)
    groups = defaultdict(list)
    for ev in evaluated:
        if "error" in ev:
            continue
        meta = ev["meta"]
        key = (meta["method"], meta["language"], meta["temperature"])
        groups[key].append(ev)

    for (method, lang, temp), exps in sorted(groups.items()):
        if len(exps) < 2:
            continue

        method_display = METHOD_DISPLAY.get(method, method)
        report += f"### {method_display} | {lang} | T={temp}\n\n"

        report += (
            "| Model | Runs | Narr F1-samples | Subnarr F1-samples |\n"
            "|-------|------|-----------------|--------------------|\n"
        )

        for ev in sorted(
            exps,
            key=lambda e: e["metrics"]
            .get("subnarratives_f1_samples", {})
            .get("mean", 0)
            or 0,
            reverse=True,
        ):
            m = ev["metrics"]
            model = ev["meta"]["model_display"]
            n_runs = ev["n_successful_runs"]

            def _fmt(key):
                d = m.get(key, {})
                if d.get("mean") is None:
                    return "N/A"
                return format_metric_short(d["mean"], d["std"])

            report += (
                f"| {model} | {n_runs} "
                f"| {_fmt('narratives_f1_samples')} "
                f"| {_fmt('subnarratives_f1_samples')} "
                f"|\n"
            )

        report += "\n"

    return report


def generate_cross_method_comparison(
    evaluated: List[Dict[str, Any]],
) -> str:
    """Generate cross-method comparison for the same model and language."""
    report = "## Cross-Method Comparison\n\n"
    report += (
        "Comparing different multi-agent strategies using the same backbone model. "
        "Sorted by subnarrative F1-samples (descending).\n\n"
    )

    # Group by (model_key, language, temperature)
    groups = defaultdict(list)
    for ev in evaluated:
        if "error" in ev:
            continue
        meta = ev["meta"]
        key = (meta["model_key"], meta["language"], meta["temperature"])
        groups[key].append(ev)

    for (model_key, lang, temp), exps in sorted(groups.items()):
        if len(exps) < 2:
            continue

        model_display = MODEL_DISPLAY.get(model_key, model_key)
        report += f"### {model_display} | {lang} | T={temp}\n\n"

        report += (
            "| Method | Runs | Narr F1-macro | Narr F1-samples | "
            "Subnarr F1-macro | Subnarr F1-samples |\n"
            "|--------|------|---------------|-----------------|"
            "-----------------|--------------------|\n"
        )

        for ev in sorted(
            exps,
            key=lambda e: e["metrics"]
            .get("subnarratives_f1_samples", {})
            .get("mean", 0)
            or 0,
            reverse=True,
        ):
            m = ev["metrics"]
            method = ev["meta"]["method_display"]
            n_runs = ev["n_successful_runs"]

            def _fmt(key):
                d = m.get(key, {})
                if d.get("mean") is None:
                    return "N/A"
                return format_metric_short(d["mean"], d["std"])

            report += (
                f"| {method} | {n_runs} "
                f"| {_fmt('narratives_f1_macro')} "
                f"| {_fmt('narratives_f1_samples')} "
                f"| {_fmt('subnarratives_f1_macro')} "
                f"| {_fmt('subnarratives_f1_samples')} "
                f"|\n"
            )

        report += "\n"

    return report


def generate_architecture_comparison(
    evaluated: List[Dict[str, Any]],
) -> str:
    """
    Generate cross-architecture comparison: Baseline vs Actor-Critic vs Best Agora.

    For each temperature setting, creates tables showing F1-samples for all three
    architectures side by side, with paired t-test significance. mDeBERTa fine-tuned
    baseline included for reference.
    """
    report = "## Cross-Architecture Comparison\n\n"
    report += (
        "Comparison of three architectures — **Baseline** (single-agent, no validation), "
        "**Actor-Critic** (single-agent + validation nodes), and **Agora** (3-agent ensemble) "
        "— matched by model, language, and temperature. For Agora, we report the best-performing "
        "aggregation strategy (intersection/majority/union). mDeBERTa fine-tuned baseline "
        "included for reference.\n\n"
        "p-values from paired t-test on per-run F1-samples scores. "
        "Significance: \\* p<0.05, \\*\\* p<0.01, \\*\\*\\* p<0.001\n\n"
    )

    # Build index: (method, model_key, lang, temp) -> evaluated experiment
    # Skip evidence and v2 variants; keep experiment with most successful runs on duplicates
    index = {}
    for ev in evaluated:
        if "error" in ev:
            continue
        meta = ev["meta"]
        eid = ev.get("experiment_id", "")
        dir_name = os.path.basename(ev.get("dir", ""))
        if "evidence" in eid or "_v2" in eid or "_v2" in dir_name:
            continue
        key = (meta["method"], meta["model_key"], meta["language"], meta["temperature"])
        if key not in index or ev["n_successful_runs"] > index[key]["n_successful_runs"]:
            index[key] = ev

    # Helper: format p-value with significance stars
    def _p_str(scores_a, scores_b):
        if not scores_a or not scores_b:
            return "—"
        n = min(len(scores_a), len(scores_b))
        if n < 2:
            return "—"
        result = paired_significance_test(scores_a[:n], scores_b[:n])
        p = result["p_ttest"]
        return f"{p:.4f}{significance_marker(p)}"

    # Helper: extract per-run score list
    def _scores(ev, metric_key):
        if ev is None:
            return []
        return ev["metrics"].get(metric_key, {}).get("scores", [])

    # Discover temperatures
    temps = sorted(set(
        ev["meta"]["temperature"]
        for ev in evaluated
        if "error" not in ev and ev["meta"]["temperature"] not in ("unknown", "?")
    ))

    for temp in temps:
        report += f"### Temperature = {temp}\n\n"

        # Collect all (lang, model_key) combos at this temperature
        combos = set()
        for (method, model_key, lang, t) in index:
            if t == temp:
                combos.add((lang, model_key))

        if not combos:
            report += "No experiments at this temperature.\n\n"
            continue

        # Sort: language, then mDeBERTa last within each language, then model name
        def _sort_key(combo):
            lang, mk = combo
            is_mdeberta = "mdeberta" in mk.lower()
            return (lang, 1 if is_mdeberta else 0, MODEL_DISPLAY.get(mk, mk))

        sorted_combos = sorted(combos, key=_sort_key)

        for level_key, level_label in [
            ("narratives_f1_samples", "Narrative"),
            ("subnarratives_f1_samples", "Subnarrative"),
        ]:
            report += f"#### {level_label}-level F1-samples\n\n"
            report += (
                "| Lang | Model | Baseline | Actor-Critic | p (AC vs BL) | "
                "Best Agora (agg) | p (Agora vs BL) |\n"
                "|------|-------|----------|-------------|--------------|"
                "-----------------|----------------|\n"
            )

            for lang, model_key in sorted_combos:
                model_name = MODEL_DISPLAY.get(model_key, model_key)
                is_mdeberta = "mdeberta" in model_key.lower()

                # --- Baseline ---
                if is_mdeberta:
                    bl_ev = index.get(("mdeberta_baseline", model_key, lang, temp))
                else:
                    bl_ev = index.get(("baseline", model_key, lang, temp))

                # --- Actor-Critic ---
                ac_ev = index.get(("actor_critic", model_key, lang, temp))

                # --- Best Agora (pick aggregation with highest mean) ---
                best_ag_ev = None
                best_ag_agg = None
                best_ag_mean = -1.0
                for ag_method, ag_label in [
                    ("agora", "intersection"),
                    ("agora_majority", "majority"),
                    ("agora_union", "union"),
                ]:
                    ag_ev = index.get((ag_method, model_key, lang, temp))
                    if ag_ev:
                        m = ag_ev["metrics"].get(level_key, {}).get("mean")
                        if m is not None and m > best_ag_mean:
                            best_ag_mean = m
                            best_ag_ev = ag_ev
                            best_ag_agg = ag_label

                # Format cells
                def _fmt(ev):
                    if ev is None:
                        return "—"
                    d = ev["metrics"].get(level_key, {})
                    if d.get("mean") is None:
                        return "—"
                    return format_metric_short(d["mean"], d["std"])

                bl_str = _fmt(bl_ev)
                ac_str = _fmt(ac_ev)
                ag_str = (
                    f"{_fmt(best_ag_ev)} ({best_ag_agg})"
                    if best_ag_ev is not None and best_ag_mean >= 0
                    else "—"
                )

                # p-values
                bl_scores = _scores(bl_ev, level_key)
                ac_p = _p_str(_scores(ac_ev, level_key), bl_scores)
                ag_p = _p_str(_scores(best_ag_ev, level_key), bl_scores)

                report += (
                    f"| {lang} | {model_name} | {bl_str} | {ac_str} | "
                    f"{ac_p} | {ag_str} | {ag_p} |\n"
                )

            report += "\n"

    # ----- Actor-Critic vs Baseline aggregate summary -----
    report += "### Actor-Critic vs Baseline: Aggregate Summary\n\n"

    narr_wins = narr_losses = narr_ties = 0
    sub_wins = sub_losses = sub_ties = 0
    model_diffs = defaultdict(lambda: {"narr": [], "sub": []})
    lang_diffs = defaultdict(lambda: {"narr": [], "sub": []})

    for (method, model_key, lang, t), ev in index.items():
        if method != "actor_critic":
            continue
        bl_ev = index.get(("baseline", model_key, lang, t))
        if bl_ev is None:
            continue
        model_name = MODEL_DISPLAY.get(model_key, model_key)
        for lk, short in [
            ("narratives_f1_samples", "narr"),
            ("subnarratives_f1_samples", "sub"),
        ]:
            ac_m = ev["metrics"].get(lk, {}).get("mean")
            bl_m = bl_ev["metrics"].get(lk, {}).get("mean")
            if ac_m is None or bl_m is None:
                continue
            diff = ac_m - bl_m
            model_diffs[model_name][short].append(diff)
            lang_diffs[lang][short].append(diff)
            if short == "narr":
                if diff > 0.001:
                    narr_wins += 1
                elif diff < -0.001:
                    narr_losses += 1
                else:
                    narr_ties += 1
            else:
                if diff > 0.001:
                    sub_wins += 1
                elif diff < -0.001:
                    sub_losses += 1
                else:
                    sub_ties += 1

    report += (
        "| Level | AC Wins | AC Losses | Ties |\n"
        "|-------|---------|-----------|------|\n"
        f"| Narrative F1-samples | {narr_wins} | {narr_losses} | {narr_ties} |\n"
        f"| Subnarrative F1-samples | {sub_wins} | {sub_losses} | {sub_ties} |\n\n"
    )

    report += "**Average improvement by model (Actor-Critic minus Baseline):**\n\n"
    report += "| Model | Avg Narr Diff | Avg Sub Diff | N |\n"
    report += "|-------|--------------|-------------|---|\n"
    for model in sorted(model_diffs.keys()):
        d = model_diffs[model]
        avg_n = float(np.mean(d["narr"])) if d["narr"] else 0.0
        avg_s = float(np.mean(d["sub"])) if d["sub"] else 0.0
        n = max(len(d["narr"]), len(d["sub"]))
        report += f"| {model} | {avg_n:+.4f} | {avg_s:+.4f} | {n} |\n"
    report += "\n"

    report += "**Average improvement by language (Actor-Critic minus Baseline):**\n\n"
    report += "| Language | Avg Narr Diff | Avg Sub Diff | N |\n"
    report += "|----------|--------------|-------------|---|\n"
    for lang in sorted(lang_diffs.keys()):
        d = lang_diffs[lang]
        avg_n = float(np.mean(d["narr"])) if d["narr"] else 0.0
        avg_s = float(np.mean(d["sub"])) if d["sub"] else 0.0
        n = max(len(d["narr"]), len(d["sub"]))
        report += f"| {lang} | {avg_n:+.4f} | {avg_s:+.4f} | {n} |\n"
    report += "\n"

    return report


def generate_full_report(
    experiments: List[Dict[str, Any]],
    evaluated: List[Dict[str, Any]],
) -> str:
    """Generate the complete Markdown report."""
    report = "# Experiment Results Report\n\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    # Count summary
    n_total = len(evaluated)
    n_success = sum(1 for e in evaluated if "error" not in e)
    n_error = n_total - n_success
    total_runs = sum(
        e.get("n_successful_runs", 0) for e in evaluated if "error" not in e
    )
    report += f"**Experiments evaluated:** {n_success}/{n_total} (total runs: {total_runs})\n\n"

    # Errors
    errors = [e for e in evaluated if "error" in e]
    if errors:
        report += "### Experiments with Errors\n\n"
        for e in errors:
            report += f"- `{e['experiment_id']}`: {e['error']}\n"
        report += "\n"

    # Methodology
    successful_experiments = [
        exp
        for exp, ev in zip(experiments, evaluated)
        if "error" not in ev
    ]
    report += generate_methodology_section(successful_experiments)

    # Results tables
    successful_evaluated = [e for e in evaluated if "error" not in e]
    report += generate_results_tables(successful_evaluated)

    # Cross-architecture comparison (Baseline vs Actor-Critic vs Agora)
    report += generate_architecture_comparison(successful_evaluated)

    # Cross-method comparison
    report += generate_cross_method_comparison(successful_evaluated)

    # Cross-model comparison
    report += generate_cross_model_comparison(successful_evaluated)

    # Significance tests
    report += generate_significance_section(successful_evaluated)

    return report


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Generate comprehensive experiment results report",
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
        "--output",
        type=str,
        default="results/analysis/experiment_summary.md",
        help="Output Markdown report path",
    )
    parser.add_argument(
        "--json-output",
        type=str,
        help="Optional: save raw evaluation data as JSON",
    )
    parser.add_argument(
        "--languages",
        nargs="+",
        type=str,
        help="Filter by language(s), e.g. EN BG",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        type=str,
        help="Filter by model keyword(s) in experiment_id, e.g. deepseek mistral",
    )
    parser.add_argument(
        "--methods",
        nargs="+",
        type=str,
        help="Filter by method keyword(s), e.g. agora baseline actor_critic",
    )
    parser.add_argument(
        "--min-runs",
        type=int,
        default=1,
        help="Minimum successful runs required to include experiment (default: 1)",
    )

    args = parser.parse_args()

    # Discover experiments
    print("Discovering experiments...")
    experiments = discover_experiments(args.experiments_dir)
    print(f"Found {len(experiments)} experiments with manifests")

    # Apply filters
    if args.languages:
        langs = {l.upper() for l in args.languages}
        experiments = [
            e for e in experiments if e["meta"]["language"] in langs
        ]
        print(f"Filtered to {len(experiments)} experiments for languages: {langs}")

    if args.models:
        model_kws = [m.lower() for m in args.models]
        experiments = [
            e
            for e in experiments
            if any(kw in e["experiment_id"].lower() for kw in model_kws)
        ]
        print(f"Filtered to {len(experiments)} experiments for models: {args.models}")

    if args.methods:
        experiments = [
            e
            for e in experiments
            if e["meta"]["method"] in args.methods
        ]
        print(f"Filtered to {len(experiments)} experiments for methods: {args.methods}")

    if not experiments:
        print("No experiments to evaluate!")
        return 1

    # Evaluate all experiments
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

    # Filter by min-runs
    if args.min_runs > 1:
        before = len(evaluated)
        evaluated_filtered = [
            e
            for e in evaluated
            if e.get("n_successful_runs", 0) >= args.min_runs or "error" in e
        ]
        # Also filter experiments list to match
        exp_ids_kept = {e["experiment_id"] for e in evaluated_filtered}
        experiments = [e for e in experiments if e["experiment_id"] in exp_ids_kept]
        evaluated = evaluated_filtered
        print(
            f"Filtered to {len(evaluated)} experiments with >= {args.min_runs} runs "
            f"(removed {before - len(evaluated)})"
        )

    # Generate report
    print("\nGenerating report...")
    report = generate_full_report(experiments, evaluated)

    # Save Markdown report
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report saved to: {args.output}")

    # Save JSON if requested
    if args.json_output:
        json_data = {
            "generated_at": datetime.now().isoformat(),
            "n_experiments": len(evaluated),
            "experiments": [],
        }
        for ev in evaluated:
            # Make JSON-serializable (remove numpy)
            ev_clean = {
                "experiment_id": ev["experiment_id"],
                "meta": ev["meta"],
                "n_successful_runs": ev.get("n_successful_runs", 0),
                "n_total_runs": ev.get("n_total_runs", 0),
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

        os.makedirs(os.path.dirname(args.json_output) or ".", exist_ok=True)
        with open(args.json_output, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)
        print(f"JSON data saved to: {args.json_output}")

    print("\nDone!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

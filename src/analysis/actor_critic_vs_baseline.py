#!/usr/bin/env python3
"""
Compare all Actor-Critic experiments against their matched Baseline experiments.

Matches on: same LLM, same language, same temperature.
Excludes: evidence variants (single run, not suitable for statistical tests).

Outputs a Markdown report with:
- Per-pair narrative and subnarrative F1-samples comparison
- Paired t-test and Wilcoxon signed-rank test
- Cohen's d effect size
- Summary table across all languages/models

Usage:
    python src/analysis/actor_critic_vs_baseline.py \
        --experiments-dir results/experiments/ \
        --output results/analysis/actor_critic_vs_baseline.md
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
from sklearn.metrics import f1_score
from sklearn.preprocessing import MultiLabelBinarizer


# Ground truth pattern
GROUND_TRUTH_PATTERN = "data/dev-documents_4_December/{lang}/subtask-3-dominant-narratives.txt"

# Model display names (from experiment name fragment)
MODEL_DISPLAY = {
    "deepseek": "DeepSeek V3",
    "mistral": "Mistral Large",
    "gemini": "Gemini 2.5 Flash",
    "gpt5nano": "GPT-5 Nano",
    "together_llama33_70b": "Llama 3.3 70B",
}

LANG_DISPLAY = {
    "bg": "Bulgarian (BG)",
    "en": "English (EN)",
    "hi": "Hindi (HI)",
    "pt": "Portuguese (PT)",
    "ru": "Russian (RU)",
}


def parse_labels(label_string: str) -> List[str]:
    label_string = label_string.strip()
    if not label_string or label_string.lower() in ("none", "other"):
        return ["Other"] if label_string.lower() == "other" else []
    return [l.strip() for l in label_string.split(";") if l.strip()]


def load_annotations(filepath: str) -> Dict[str, Dict[str, List[str]]]:
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


def compute_f1_scores(y_true, y_pred):
    all_labels = set()
    for labels in y_true + y_pred:
        all_labels.update(labels)
    mlb = MultiLabelBinarizer()
    mlb.fit([list(all_labels)])
    y_true_bin = mlb.transform(y_true)
    y_pred_bin = mlb.transform(y_pred)
    return {
        "f1_macro": float(f1_score(y_true_bin, y_pred_bin, average="macro", zero_division=0)),
        "f1_micro": float(f1_score(y_true_bin, y_pred_bin, average="micro", zero_division=0)),
        "f1_samples": float(f1_score(y_true_bin, y_pred_bin, average="samples", zero_division=0)),
    }


def compute_manual_f1_samples(y_true, y_pred):
    """Set-based per-sample F1 (SemEval official)."""
    scores = []
    for yt, yp in zip(y_true, y_pred):
        st, sp = set(yt), set(yp)
        if len(st) + len(sp) == 0:
            scores.append(1.0)
        else:
            scores.append(2 * len(st & sp) / (len(st) + len(sp)))
    return float(np.mean(scores))


def evaluate_run(prediction_file: str, ground_truth: Dict) -> Optional[Dict]:
    if not os.path.exists(prediction_file):
        return None
    predictions = {}
    with open(prediction_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                filename = parts[0]
                narratives = parse_labels(parts[1]) if len(parts) > 1 else []
                subnarratives = parse_labels(parts[2]) if len(parts) > 2 else []
                predictions[filename] = {"narratives": narratives, "subnarratives": subnarratives}

    common = set(ground_truth.keys()) & set(predictions.keys())
    if not common:
        return None

    yt_narr = [ground_truth[f]["narratives"] for f in common]
    yp_narr = [predictions[f]["narratives"] for f in common]
    yt_sub = [ground_truth[f]["subnarratives"] for f in common]
    yp_sub = [predictions[f]["subnarratives"] for f in common]

    narr_scores = compute_f1_scores(yt_narr, yp_narr)
    sub_scores = compute_f1_scores(yt_sub, yp_sub)
    narr_scores["f1_samples_manual"] = compute_manual_f1_samples(yt_narr, yp_narr)
    sub_scores["f1_samples_manual"] = compute_manual_f1_samples(yt_sub, yp_sub)

    return {"narratives": narr_scores, "subnarratives": sub_scores, "n_files": len(common)}


def load_experiment_runs(experiment_dir: str, ground_truth: Dict) -> Dict[str, List[float]]:
    manifest_path = os.path.join(experiment_dir, "experiment_manifest.json")
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    metrics = defaultdict(list)
    for run in manifest["runs"]:
        if run.get("status") != "success":
            continue
        output_file = run.get("output_file")
        if not output_file:
            continue
        result = evaluate_run(output_file, ground_truth)
        if result is None:
            continue
        for level in ["narratives", "subnarratives"]:
            for metric_name, value in result[level].items():
                metrics[f"{level}_{metric_name}"].append(value)

    return dict(metrics)


def bootstrap_ci(scores, confidence=0.95, n_bootstrap=10000, seed=42):
    if len(scores) < 2:
        m = float(np.mean(scores)) if scores else 0.0
        return m, m, m
    rng = np.random.RandomState(seed)
    scores = np.array(scores)
    means = [np.mean(rng.choice(scores, size=len(scores), replace=True)) for _ in range(n_bootstrap)]
    means = np.array(means)
    alpha = 1 - confidence
    return float(np.mean(scores)), float(np.percentile(means, alpha / 2 * 100)), float(np.percentile(means, (1 - alpha / 2) * 100))


def cohens_d_paired(a, b):
    """Paired Cohen's d = mean(diff) / std(diff)."""
    diff = np.array(a) - np.array(b)
    sd = np.std(diff, ddof=1)
    if sd == 0:
        return 0.0
    return float(np.mean(diff) / sd)


def effect_size_label(d):
    d = abs(d)
    if d < 0.2:
        return "negligible"
    elif d < 0.5:
        return "small"
    elif d < 0.8:
        return "medium"
    else:
        return "large"


def significance_stars(p):
    if p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    return ""


def parse_experiment_name(name: str):
    """Parse experiment name to extract method, model, language, temperature."""
    # Remove method prefix
    for method in ["actor_critic_", "baseline_"]:
        if name.startswith(method):
            rest = name[len(method):]
            break
    else:
        return None

    # Try to match model + lang + temp
    # Models with underscores: together_llama33_70b
    for model_key in sorted(MODEL_DISPLAY.keys(), key=len, reverse=True):
        if rest.startswith(model_key + "_"):
            remainder = rest[len(model_key) + 1:]
            # remainder should be like "en_t00" or "bg_t07" or "en_t00_evidence"
            parts = remainder.split("_")
            if len(parts) >= 2:
                lang = parts[0]
                temp_str = parts[1]  # e.g., "t00" or "t07"
                variant = "_".join(parts[2:]) if len(parts) > 2 else ""
                return {
                    "model": model_key,
                    "lang": lang.upper(),
                    "temp": temp_str,
                    "variant": variant,
                }
    return None


def find_matching_pairs(experiments_dir: str):
    """Find all actor_critic/baseline pairs with same model, language, temperature."""
    all_dirs = sorted(os.listdir(experiments_dir))

    actor_critic_exps = {}
    baseline_exps = {}

    for d in all_dirs:
        full_path = os.path.join(experiments_dir, d)
        if not os.path.isdir(full_path):
            continue

        if d.startswith("actor_critic_"):
            parsed = parse_experiment_name(d)
            if parsed and not parsed["variant"]:  # Skip evidence variants
                key = (parsed["model"], parsed["lang"], parsed["temp"])
                actor_critic_exps[key] = d
        elif d.startswith("baseline_") and not d.startswith("baseline_together") or d.startswith("baseline_together"):
            if d.startswith("baseline_") and not d.startswith("mdeberta_"):
                parsed = parse_experiment_name(d)
                if parsed and not parsed["variant"]:
                    key = (parsed["model"], parsed["lang"], parsed["temp"])
                    baseline_exps[key] = d

    # Find matching pairs
    pairs = []
    for key in sorted(actor_critic_exps.keys()):
        if key in baseline_exps:
            pairs.append({
                "model": key[0],
                "lang": key[1],
                "temp": key[2],
                "actor_critic": actor_critic_exps[key],
                "baseline": baseline_exps[key],
            })

    return pairs


def run_comparison(pair, experiments_dir, ground_truths):
    """Run comparison for a single pair."""
    lang = pair["lang"]
    gt = ground_truths[lang]

    ac_dir = os.path.join(experiments_dir, pair["actor_critic"])
    bl_dir = os.path.join(experiments_dir, pair["baseline"])

    ac_metrics = load_experiment_runs(ac_dir, gt)
    bl_metrics = load_experiment_runs(bl_dir, gt)

    results = {
        "actor_critic_name": pair["actor_critic"],
        "baseline_name": pair["baseline"],
        "model": pair["model"],
        "model_display": MODEL_DISPLAY.get(pair["model"], pair["model"]),
        "lang": lang,
        "temp": pair["temp"],
        "metrics": {},
    }

    for metric_key in ["narratives_f1_samples", "narratives_f1_samples_manual",
                       "narratives_f1_macro", "narratives_f1_micro",
                       "subnarratives_f1_samples", "subnarratives_f1_samples_manual",
                       "subnarratives_f1_macro", "subnarratives_f1_micro"]:
        ac_scores = ac_metrics.get(metric_key, [])
        bl_scores = bl_metrics.get(metric_key, [])

        if len(ac_scores) < 2 or len(bl_scores) < 2:
            continue

        # Ensure same number of runs for paired tests
        n = min(len(ac_scores), len(bl_scores))
        ac_paired = ac_scores[:n]
        bl_paired = bl_scores[:n]

        ac_mean, ac_ci_lo, ac_ci_hi = bootstrap_ci(ac_scores)
        bl_mean, bl_ci_lo, bl_ci_hi = bootstrap_ci(bl_scores)

        # Paired t-test
        t_stat, t_pval = stats.ttest_rel(ac_paired, bl_paired) if n >= 2 else (0.0, 1.0)

        # Wilcoxon
        try:
            diff = np.array(ac_paired) - np.array(bl_paired)
            if np.all(diff == 0) or np.sum(diff != 0) < 2:
                w_stat, w_pval = 0.0, 1.0
            else:
                w_stat, w_pval = stats.wilcoxon(ac_paired, bl_paired)
        except Exception:
            w_stat, w_pval = 0.0, 1.0

        d = cohens_d_paired(ac_paired, bl_paired)

        results["metrics"][metric_key] = {
            "ac_mean": ac_mean,
            "ac_std": float(np.std(ac_scores, ddof=1)),
            "ac_ci": [ac_ci_lo, ac_ci_hi],
            "ac_n": len(ac_scores),
            "bl_mean": bl_mean,
            "bl_std": float(np.std(bl_scores, ddof=1)),
            "bl_ci": [bl_ci_lo, bl_ci_hi],
            "bl_n": len(bl_scores),
            "diff": ac_mean - bl_mean,
            "rel_improvement_pct": (ac_mean - bl_mean) / bl_mean * 100 if bl_mean != 0 else 0.0,
            "t_stat": float(t_stat),
            "t_pval": float(t_pval),
            "w_stat": float(w_stat),
            "w_pval": float(w_pval),
            "cohens_d": d,
            "effect_label": effect_size_label(d),
        }

    return results


def generate_report(all_results, output_path):
    """Generate Markdown report."""
    lines = []
    lines.append("# Actor-Critic vs Baseline Comparison Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append(f"**Total comparisons:** {len(all_results)}")
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    lines.append("Each Actor-Critic experiment is compared against its matched Baseline experiment")
    lines.append("(same LLM, same language, same temperature). Both methods use a single agent;")
    lines.append("the difference is that Actor-Critic adds **validation nodes** that review and")
    lines.append("refine predictions at both narrative and subnarrative levels.")
    lines.append("")
    lines.append("Statistical tests (paired, since runs use matched seeds):")
    lines.append("- **Paired t-test**: parametric")
    lines.append("- **Wilcoxon signed-rank**: non-parametric")
    lines.append("- **Cohen's d** (paired): mean(diff)/std(diff). |d|<0.2 negligible, 0.2-0.5 small, 0.5-0.8 medium, >=0.8 large")
    lines.append("- Significance: * p<0.05, ** p<0.01, *** p<0.001")
    lines.append("")

    # ---------------------------------------------------------------
    # Summary table: all pairs, key metrics
    # ---------------------------------------------------------------
    lines.append("## Summary Table")
    lines.append("")
    lines.append("### Narrative-level F1-samples (manual)")
    lines.append("")
    lines.append("| Model | Lang | Temp | Actor-Critic | Baseline | Diff | Rel% | Cohen's d | Wilcoxon p | Sig |")
    lines.append("|-------|------|------|-------------|----------|------|------|-----------|------------|-----|")

    for r in all_results:
        m = r["metrics"].get("narratives_f1_samples_manual") or r["metrics"].get("narratives_f1_samples")
        if not m:
            continue
        sig = significance_stars(m["w_pval"])
        lines.append(
            f"| {r['model_display']} | {r['lang']} | {r['temp']} | "
            f"{m['ac_mean']:.3f}±{m['ac_std']:.3f} | "
            f"{m['bl_mean']:.3f}±{m['bl_std']:.3f} | "
            f"{m['diff']:+.3f} | {m['rel_improvement_pct']:+.1f}% | "
            f"{m['cohens_d']:+.2f} ({m['effect_label']}) | "
            f"{m['w_pval']:.4f} | {sig} |"
        )

    lines.append("")
    lines.append("### Subnarrative-level F1-samples (manual)")
    lines.append("")
    lines.append("| Model | Lang | Temp | Actor-Critic | Baseline | Diff | Rel% | Cohen's d | Wilcoxon p | Sig |")
    lines.append("|-------|------|------|-------------|----------|------|------|-----------|------------|-----|")

    for r in all_results:
        m = r["metrics"].get("subnarratives_f1_samples_manual") or r["metrics"].get("subnarratives_f1_samples")
        if not m:
            continue
        sig = significance_stars(m["w_pval"])
        lines.append(
            f"| {r['model_display']} | {r['lang']} | {r['temp']} | "
            f"{m['ac_mean']:.3f}±{m['ac_std']:.3f} | "
            f"{m['bl_mean']:.3f}±{m['bl_std']:.3f} | "
            f"{m['diff']:+.3f} | {m['rel_improvement_pct']:+.1f}% | "
            f"{m['cohens_d']:+.2f} ({m['effect_label']}) | "
            f"{m['w_pval']:.4f} | {sig} |"
        )

    # ---------------------------------------------------------------
    # Aggregate stats
    # ---------------------------------------------------------------
    lines.append("")
    lines.append("## Aggregate Analysis")
    lines.append("")

    # Count wins/losses/ties
    narr_wins, narr_losses, narr_ties = 0, 0, 0
    sub_wins, sub_losses, sub_ties = 0, 0, 0
    narr_sig_wins, narr_sig_losses = 0, 0
    sub_sig_wins, sub_sig_losses = 0, 0

    for r in all_results:
        m_narr = r["metrics"].get("narratives_f1_samples_manual") or r["metrics"].get("narratives_f1_samples")
        m_sub = r["metrics"].get("subnarratives_f1_samples_manual") or r["metrics"].get("subnarratives_f1_samples")

        if m_narr:
            if m_narr["diff"] > 0.001:
                narr_wins += 1
                if m_narr["w_pval"] < 0.05:
                    narr_sig_wins += 1
            elif m_narr["diff"] < -0.001:
                narr_losses += 1
                if m_narr["w_pval"] < 0.05:
                    narr_sig_losses += 1
            else:
                narr_ties += 1

        if m_sub:
            if m_sub["diff"] > 0.001:
                sub_wins += 1
                if m_sub["w_pval"] < 0.05:
                    sub_sig_wins += 1
            elif m_sub["diff"] < -0.001:
                sub_losses += 1
                if m_sub["w_pval"] < 0.05:
                    sub_sig_losses += 1
            else:
                sub_ties += 1

    lines.append("### Win/Loss/Tie Count (Actor-Critic vs Baseline)")
    lines.append("")
    lines.append("| Level | AC Wins | AC Losses | Ties | Sig Wins (p<.05) | Sig Losses (p<.05) |")
    lines.append("|-------|---------|-----------|------|------------------|--------------------|")
    lines.append(f"| Narrative | {narr_wins} | {narr_losses} | {narr_ties} | {narr_sig_wins} | {narr_sig_losses} |")
    lines.append(f"| Subnarrative | {sub_wins} | {sub_losses} | {sub_ties} | {sub_sig_wins} | {sub_sig_losses} |")
    lines.append("")

    # Average improvement by model
    lines.append("### Average Improvement by Model")
    lines.append("")
    model_narr_diffs = defaultdict(list)
    model_sub_diffs = defaultdict(list)
    for r in all_results:
        m_narr = r["metrics"].get("narratives_f1_samples_manual") or r["metrics"].get("narratives_f1_samples")
        m_sub = r["metrics"].get("subnarratives_f1_samples_manual") or r["metrics"].get("subnarratives_f1_samples")
        if m_narr:
            model_narr_diffs[r["model_display"]].append(m_narr["diff"])
        if m_sub:
            model_sub_diffs[r["model_display"]].append(m_sub["diff"])

    lines.append("| Model | Avg Narr Diff | Avg Subnarr Diff | N pairs |")
    lines.append("|-------|--------------|-----------------|---------|")
    for model in sorted(set(list(model_narr_diffs.keys()) + list(model_sub_diffs.keys()))):
        nd = model_narr_diffs.get(model, [])
        sd = model_sub_diffs.get(model, [])
        n = max(len(nd), len(sd))
        avg_n = np.mean(nd) if nd else 0.0
        avg_s = np.mean(sd) if sd else 0.0
        lines.append(f"| {model} | {avg_n:+.4f} | {avg_s:+.4f} | {n} |")
    lines.append("")

    # Average improvement by language
    lines.append("### Average Improvement by Language")
    lines.append("")
    lang_narr_diffs = defaultdict(list)
    lang_sub_diffs = defaultdict(list)
    for r in all_results:
        m_narr = r["metrics"].get("narratives_f1_samples_manual") or r["metrics"].get("narratives_f1_samples")
        m_sub = r["metrics"].get("subnarratives_f1_samples_manual") or r["metrics"].get("subnarratives_f1_samples")
        if m_narr:
            lang_narr_diffs[r["lang"]].append(m_narr["diff"])
        if m_sub:
            lang_sub_diffs[r["lang"]].append(m_sub["diff"])

    lines.append("| Language | Avg Narr Diff | Avg Subnarr Diff | N pairs |")
    lines.append("|----------|--------------|-----------------|---------|")
    for lang in sorted(set(list(lang_narr_diffs.keys()) + list(lang_sub_diffs.keys()))):
        nd = lang_narr_diffs.get(lang, [])
        sd = lang_sub_diffs.get(lang, [])
        n = max(len(nd), len(sd))
        avg_n = np.mean(nd) if nd else 0.0
        avg_s = np.mean(sd) if sd else 0.0
        lines.append(f"| {lang} | {avg_n:+.4f} | {avg_s:+.4f} | {n} |")
    lines.append("")

    # ---------------------------------------------------------------
    # Detailed per-pair results
    # ---------------------------------------------------------------
    lines.append("## Detailed Per-Pair Results")
    lines.append("")

    for r in all_results:
        lines.append(f"### {r['model_display']} — {r['lang']} — {r['temp']}")
        lines.append("")
        lines.append(f"- **Actor-Critic**: `{r['actor_critic_name']}`")
        lines.append(f"- **Baseline**: `{r['baseline_name']}`")
        lines.append("")

        lines.append("| Metric | Actor-Critic | Baseline | Diff | Rel% | t-test p | Wilcoxon p | Cohen's d |")
        lines.append("|--------|-------------|----------|------|------|----------|------------|-----------|")

        for mk in ["narratives_f1_macro", "narratives_f1_micro",
                    "narratives_f1_samples", "narratives_f1_samples_manual",
                    "subnarratives_f1_macro", "subnarratives_f1_micro",
                    "subnarratives_f1_samples", "subnarratives_f1_samples_manual"]:
            m = r["metrics"].get(mk)
            if not m:
                continue
            display_name = mk.replace("narratives_", "Narr ").replace("subnarratives_", "Sub ")
            t_sig = significance_stars(m["t_pval"])
            w_sig = significance_stars(m["w_pval"])
            lines.append(
                f"| {display_name} | "
                f"{m['ac_mean']:.4f}±{m['ac_std']:.4f} | "
                f"{m['bl_mean']:.4f}±{m['bl_std']:.4f} | "
                f"{m['diff']:+.4f} | {m['rel_improvement_pct']:+.1f}% | "
                f"{m['t_pval']:.4f}{t_sig} | "
                f"{m['w_pval']:.4f}{w_sig} | "
                f"{m['cohens_d']:+.2f} ({m['effect_label']}) |"
            )
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Actor-Critic vs Baseline comparison")
    parser.add_argument("--experiments-dir", default="results/experiments/")
    parser.add_argument("--output", default="results/analysis/actor_critic_vs_baseline.md")
    parser.add_argument("--json-output", default=None, help="Optional JSON output")
    args = parser.parse_args()

    experiments_dir = args.experiments_dir

    # Find matching pairs
    pairs = find_matching_pairs(experiments_dir)
    print(f"Found {len(pairs)} matching actor-critic/baseline pairs:")
    for p in pairs:
        print(f"  {p['actor_critic']} vs {p['baseline']}")

    if not pairs:
        print("No matching pairs found!")
        return 1

    # Load ground truths
    languages = sorted(set(p["lang"] for p in pairs))
    ground_truths = {}
    for lang in languages:
        gt_path = GROUND_TRUTH_PATTERN.format(lang=lang)
        if not os.path.exists(gt_path):
            print(f"Warning: ground truth not found: {gt_path}")
            continue
        ground_truths[lang] = load_annotations(gt_path)
        print(f"Loaded ground truth for {lang}: {len(ground_truths[lang])} documents")

    # Run comparisons
    all_results = []
    for pair in pairs:
        if pair["lang"] not in ground_truths:
            print(f"Skipping {pair['actor_critic']} — no ground truth for {pair['lang']}")
            continue
        print(f"\nComparing: {pair['actor_critic']} vs {pair['baseline']}...")
        try:
            result = run_comparison(pair, experiments_dir, ground_truths)
            all_results.append(result)
        except Exception as e:
            print(f"  ERROR: {e}")

    # Generate report
    report = generate_report(all_results, args.output)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\nReport saved to: {args.output}")

    # Optionally save JSON
    json_output = args.json_output or args.output.replace(".md", ".json")
    with open(json_output, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    print(f"JSON saved to: {json_output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

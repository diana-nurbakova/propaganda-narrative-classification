#!/usr/bin/env python3
"""
Statistical analysis of confusion severity using semantic similarity scores.

Loads all_confusions.json (from semantic_confusion_analysis.py) and produces:
- Similarity score distributions by severity level
- Per-model and per-language severity breakdowns
- Statistical tests on whether confusions are mostly "expected" or severe
- Histogram and box plot visualizations
- Extended markdown report

Usage:
    python src/analysis/confusion_severity_statistics.py \
        --confusions results/analysis/confusion/all_confusions.json \
        --output-dir results/analysis/confusion/
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# Similarity bands for severity classification
SIMILARITY_BANDS = [
    ("Very high (>0.7)", 0.7, 1.01),
    ("High (0.5-0.7)", 0.5, 0.7),
    ("Moderate (0.3-0.5)", 0.3, 0.5),
    ("Low (0.1-0.3)", 0.1, 0.3),
    ("Very low (<0.1)", -0.01, 0.1),
]


def extract_model(experiment: str) -> str:
    """Extract model name from experiment name."""
    if "deepseek" in experiment:
        return "DeepSeek"
    elif "gpt5nano" in experiment:
        return "GPT-5 Nano"
    elif "gemini" in experiment:
        return "Gemini"
    elif "mistral" in experiment:
        return "Mistral"
    elif "together" in experiment or "llama" in experiment:
        return "Together Llama"
    elif "mdeberta" in experiment:
        return "mDeBERTa"
    return "Unknown"


def extract_method(experiment: str) -> str:
    """Extract method from experiment name."""
    if experiment.startswith("actor_critic"):
        return "actor_critic"
    elif experiment.startswith("agora_union"):
        return "agora_union"
    elif experiment.startswith("agora_majority"):
        return "agora_majority"
    elif experiment.startswith("agora"):
        return "agora"
    elif experiment.startswith("baseline"):
        return "baseline"
    elif experiment.startswith("mdeberta"):
        return "mdeberta"
    return "other"


def compute_band(sim: float) -> str:
    """Classify similarity into a band."""
    for label, lo, hi in SIMILARITY_BANDS:
        if lo <= sim < hi:
            return label
    return "Very low (<0.1)"


def generate_report(confusions: list, output_dir: Path) -> str:
    """Generate comprehensive severity statistics report."""
    report = []
    report.append("# Semantic Similarity Analysis of Prediction Confusions\n")
    report.append("This report analyzes how semantically related the confused label pairs are,")
    report.append("using embedding-based similarity (all-MiniLM-L6-v2) from the semantic hierarchy.\n")
    report.append("**Key question**: Are most confusions between semantically similar labels (expected/mild)")
    report.append("or between unrelated labels (severe errors)?\n")

    # Filter out "Other" confusions (similarity=0 is often due to "Other" label)
    all_sims = [c["similarity"] for c in confusions]
    non_other = [c for c in confusions if "Other" not in c["gold"] and "Other" not in c["pred"]]
    non_other_sims = [c["similarity"] for c in non_other]

    # --- Section 1: Overall Statistics ---
    report.append("## 1. Overall Similarity Statistics\n")
    report.append(f"| Metric | All Confusions (n={len(all_sims)}) | Excl. 'Other' (n={len(non_other_sims)}) |")
    report.append("|--------|-----|-----|")
    report.append(f"| Mean similarity | {np.mean(all_sims):.4f} | {np.mean(non_other_sims):.4f} |")
    report.append(f"| Median similarity | {np.median(all_sims):.4f} | {np.median(non_other_sims):.4f} |")
    report.append(f"| Std deviation | {np.std(all_sims):.4f} | {np.std(non_other_sims):.4f} |")
    report.append(f"| 25th percentile | {np.percentile(all_sims, 25):.4f} | {np.percentile(non_other_sims, 25):.4f} |")
    report.append(f"| 75th percentile | {np.percentile(all_sims, 75):.4f} | {np.percentile(non_other_sims, 75):.4f} |")
    report.append(f"| Min | {np.min(all_sims):.4f} | {np.min(non_other_sims):.4f} |")
    report.append(f"| Max | {np.max(all_sims):.4f} | {np.max(non_other_sims):.4f} |")
    report.append("")

    # --- Section 2: Similarity Band Distribution ---
    report.append("## 2. Similarity Band Distribution\n")
    report.append("Classifying confusions by how semantically similar the confused pairs are:\n")
    report.append("| Similarity Band | Count | % | Interpretation |")
    report.append("|-----------------|-------|---|----------------|")

    interpretations = {
        "Very high (>0.7)": "Near-synonymous labels, highly expected confusion",
        "High (0.5-0.7)": "Related labels, understandable confusion",
        "Moderate (0.3-0.5)": "Somewhat related, concerning but not severe",
        "Low (0.1-0.3)": "Loosely related, significant error",
        "Very low (<0.1)": "Unrelated or involves 'Other' label, severe error",
    }

    for label, lo, hi in SIMILARITY_BANDS:
        count = sum(1 for s in all_sims if lo <= s < hi)
        pct = count / len(all_sims) * 100
        report.append(f"| {label} | {count} | {pct:.1f}% | {interpretations[label]} |")

    report.append("")

    # Same for non-Other
    report.append("### Excluding 'Other' label confusions\n")
    report.append("| Similarity Band | Count | % |")
    report.append("|-----------------|-------|---|")

    for label, lo, hi in SIMILARITY_BANDS:
        count = sum(1 for s in non_other_sims if lo <= s < hi)
        pct = count / len(non_other_sims) * 100 if non_other_sims else 0
        report.append(f"| {label} | {count} | {pct:.1f}% |")

    report.append("")

    # --- Section 3: By Severity Level ---
    report.append("## 3. Similarity Distribution by Structural Severity\n")
    report.append("How do similarity scores differ across the taxonomy-based severity levels?\n")

    severity_sims = defaultdict(list)
    for c in confusions:
        severity_sims[c["severity"]].append(c["similarity"])

    report.append("| Severity Level | Count | Mean Sim | Median Sim | Std | Description |")
    report.append("|----------------|-------|----------|------------|-----|-------------|")

    severity_desc = {
        "same-narrative": "Sibling subnarratives under the same parent narrative",
        "same-category": "Different narratives within the same domain (URW or CC)",
        "cross-category": "Confusing URW with CC labels — most severe structural error",
        "hallucination": "Involves 'Other' label (missed or hallucinated)",
    }
    for sev in ["same-narrative", "same-category", "cross-category", "hallucination"]:
        sims = severity_sims.get(sev, [])
        if sims:
            report.append(f"| {sev} | {len(sims)} | {np.mean(sims):.4f} | {np.median(sims):.4f} | {np.std(sims):.4f} | {severity_desc.get(sev, '')} |")

    report.append("")

    # For same-narrative and same-category, show band breakdown
    for sev in ["same-narrative", "same-category"]:
        sims = severity_sims.get(sev, [])
        # Exclude Other within this severity
        sims_no_other = [c["similarity"] for c in confusions
                         if c["severity"] == sev and "Other" not in c["gold"] and "Other" not in c["pred"]]
        if sims_no_other:
            report.append(f"### {sev} confusions (excl. Other)\n")
            report.append(f"| Similarity Band | Count | % |")
            report.append(f"|-----------------|-------|---|")
            for label, lo, hi in SIMILARITY_BANDS:
                count = sum(1 for s in sims_no_other if lo <= s < hi)
                pct = count / len(sims_no_other) * 100
                report.append(f"| {label} | {count} | {pct:.1f}% |")
            report.append("")

    # --- Section 4: By Model ---
    report.append("## 4. Severity by Model\n")
    report.append("Comparing how different models distribute across severity levels and similarity scores.\n")

    model_data = defaultdict(lambda: defaultdict(list))
    for c in confusions:
        model = extract_model(c["experiment"])
        model_data[model][c["severity"]].append(c["similarity"])

    report.append("| Model | Total | Same-Narr % | Same-Cat % | Cross-Cat % | Halluc % | Mean Sim (excl. Other) |")
    report.append("|-------|-------|-------------|------------|-------------|----------|------------------------|")

    for model in sorted(model_data.keys()):
        sevs = model_data[model]
        total = sum(len(v) for v in sevs.values())
        sn = len(sevs.get("same-narrative", []))
        sc = len(sevs.get("same-category", []))
        cc = len(sevs.get("cross-category", []))
        hl = len(sevs.get("hallucination", []))
        # Mean similarity excluding Other
        model_confusions = [c for c in confusions if extract_model(c["experiment"]) == model
                           and "Other" not in c["gold"] and "Other" not in c["pred"]]
        mean_sim = np.mean([c["similarity"] for c in model_confusions]) if model_confusions else 0
        report.append(f"| {model} | {total} | {sn/total*100:.1f}% | {sc/total*100:.1f}% | {cc/total*100:.1f}% | {hl/total*100:.1f}% | {mean_sim:.4f} |")

    report.append("")

    # --- Section 5: By Method ---
    report.append("## 5. Severity by Method\n")

    method_data = defaultdict(lambda: defaultdict(list))
    for c in confusions:
        method = extract_method(c["experiment"])
        method_data[method][c["severity"]].append(c["similarity"])

    report.append("| Method | Total | Same-Narr % | Same-Cat % | Cross-Cat % | Halluc % | Mean Sim (excl. Other) |")
    report.append("|--------|-------|-------------|------------|-------------|----------|------------------------|")

    for method in sorted(method_data.keys()):
        sevs = method_data[method]
        total = sum(len(v) for v in sevs.values())
        sn = len(sevs.get("same-narrative", []))
        sc = len(sevs.get("same-category", []))
        cc = len(sevs.get("cross-category", []))
        hl = len(sevs.get("hallucination", []))
        method_confusions = [c for c in confusions if extract_method(c["experiment"]) == method
                            and "Other" not in c["gold"] and "Other" not in c["pred"]]
        mean_sim = np.mean([c["similarity"] for c in method_confusions]) if method_confusions else 0
        report.append(f"| {method} | {total} | {sn/total*100:.1f}% | {sc/total*100:.1f}% | {cc/total*100:.1f}% | {hl/total*100:.1f}% | {mean_sim:.4f} |")

    report.append("")

    # --- Section 6: By Language ---
    report.append("## 6. Severity by Language\n")

    lang_data = defaultdict(lambda: defaultdict(list))
    for c in confusions:
        lang_data[c["language"]][c["severity"]].append(c["similarity"])

    report.append("| Language | Total | Same-Narr % | Same-Cat % | Cross-Cat % | Halluc % | Mean Sim (excl. Other) |")
    report.append("|----------|-------|-------------|------------|-------------|----------|------------------------|")

    for lang in ["EN", "BG", "HI", "PT", "RU"]:
        sevs = lang_data.get(lang, {})
        total = sum(len(v) for v in sevs.values())
        if total == 0:
            continue
        sn = len(sevs.get("same-narrative", []))
        sc = len(sevs.get("same-category", []))
        cc = len(sevs.get("cross-category", []))
        hl = len(sevs.get("hallucination", []))
        lang_confusions = [c for c in confusions if c["language"] == lang
                          and "Other" not in c["gold"] and "Other" not in c["pred"]]
        mean_sim = np.mean([c["similarity"] for c in lang_confusions]) if lang_confusions else 0
        report.append(f"| {lang} | {total} | {sn/total*100:.1f}% | {sc/total*100:.1f}% | {cc/total*100:.1f}% | {hl/total*100:.1f}% | {mean_sim:.4f} |")

    report.append("")

    # --- Section 7: Model x Language breakdown ---
    report.append("## 7. Mean Similarity by Model x Language (excl. Other)\n")

    model_lang_sims = defaultdict(lambda: defaultdict(list))
    for c in non_other:
        model = extract_model(c["experiment"])
        model_lang_sims[model][c["language"]].append(c["similarity"])

    models_sorted = sorted(model_lang_sims.keys())
    langs = ["EN", "BG", "HI", "PT", "RU"]
    header = "| Model | " + " | ".join(langs) + " | Overall |"
    sep = "|-------|" + "|".join(["------"] * len(langs)) + "|---------|"
    report.append(header)
    report.append(sep)

    for model in models_sorted:
        cells = []
        all_model_sims = []
        for lang in langs:
            sims = model_lang_sims[model].get(lang, [])
            if sims:
                cells.append(f"{np.mean(sims):.3f}")
                all_model_sims.extend(sims)
            else:
                cells.append("—")
        overall = f"{np.mean(all_model_sims):.3f}" if all_model_sims else "—"
        report.append(f"| {model} | " + " | ".join(cells) + f" | {overall} |")

    report.append("")

    # --- Section 8: Key Finding Summary ---
    report.append("## 8. Key Findings\n")

    # Compute the main stat
    non_other_high = sum(1 for s in non_other_sims if s >= 0.5)
    non_other_moderate = sum(1 for s in non_other_sims if 0.3 <= s < 0.5)
    non_other_low = sum(1 for s in non_other_sims if s < 0.3)

    total_no = len(non_other_sims)
    report.append(f"**Excluding 'Other' label confusions ({total_no} pairs):**\n")
    report.append(f"- **{non_other_high/total_no*100:.1f}%** of confusions are between semantically **similar** labels (sim >= 0.5) — expected/understandable errors")
    report.append(f"- **{non_other_moderate/total_no*100:.1f}%** are between **moderately related** labels (0.3 <= sim < 0.5) — concerning but explainable")
    report.append(f"- **{non_other_low/total_no*100:.1f}%** are between **weakly related** labels (sim < 0.3) — severe or unexpected errors\n")

    # Compare models
    model_mean_sims = {}
    for model in model_lang_sims:
        all_sims_model = []
        for lang_sims in model_lang_sims[model].values():
            all_sims_model.extend(lang_sims)
        if all_sims_model:
            model_mean_sims[model] = np.mean(all_sims_model)

    best_model = max(model_mean_sims, key=model_mean_sims.get) if model_mean_sims else "N/A"
    worst_model = min(model_mean_sims, key=model_mean_sims.get) if model_mean_sims else "N/A"

    report.append(f"**Model comparison:**")
    report.append(f"- Highest mean confusion similarity (most expected errors): **{best_model}** ({model_mean_sims.get(best_model, 0):.4f})")
    report.append(f"- Lowest mean confusion similarity (most severe errors): **{worst_model}** ({model_mean_sims.get(worst_model, 0):.4f})\n")

    # Method comparison
    method_mean_sims = {}
    for method in method_data:
        method_confusions = [c["similarity"] for c in non_other if extract_method(c["experiment"]) == method]
        if method_confusions:
            method_mean_sims[method] = np.mean(method_confusions)

    if method_mean_sims:
        best_method = max(method_mean_sims, key=method_mean_sims.get)
        worst_method = min(method_mean_sims, key=method_mean_sims.get)
        report.append(f"**Method comparison:**")
        report.append(f"- Highest mean confusion similarity: **{best_method}** ({method_mean_sims[best_method]:.4f})")
        report.append(f"- Lowest mean confusion similarity: **{worst_method}** ({method_mean_sims[worst_method]:.4f})\n")

    # Overall conclusion
    median_all = np.median(non_other_sims)
    report.append(f"**Conclusion:** The median confusion similarity is **{median_all:.4f}**. ", )
    if median_all >= 0.5:
        report.append("Most confusions occur between semantically related labels, suggesting models")
        report.append("struggle primarily with fine-grained distinctions within related topics rather than")
        report.append("making fundamentally wrong categorizations.")
    elif median_all >= 0.3:
        report.append("Confusions are spread across related and moderately related labels,")
        report.append("suggesting a mix of fine-grained and broader categorization errors.")
    else:
        report.append("Many confusions occur between semantically distant labels,")
        report.append("suggesting significant categorization problems beyond fine-grained distinctions.")

    report.append("")
    return "\n".join(report)


def plot_similarity_histogram(confusions: list, output_dir: Path):
    """Plot histogram of similarity scores."""
    all_sims = [c["similarity"] for c in confusions]
    non_other_sims = [c["similarity"] for c in confusions
                      if "Other" not in c["gold"] and "Other" not in c["pred"]]

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # All confusions
    axes[0].hist(all_sims, bins=50, color="#4A90D9", edgecolor="white", alpha=0.8)
    axes[0].axvline(np.median(all_sims), color="red", linestyle="--", linewidth=2,
                    label=f"Median: {np.median(all_sims):.3f}")
    axes[0].axvline(np.mean(all_sims), color="orange", linestyle="--", linewidth=2,
                    label=f"Mean: {np.mean(all_sims):.3f}")
    axes[0].set_xlabel("Embedding Similarity", fontsize=12)
    axes[0].set_ylabel("Count", fontsize=12)
    axes[0].set_title(f"All Confusions (n={len(all_sims)})", fontsize=14, fontweight="bold")
    axes[0].legend(fontsize=11)

    # Excluding Other
    axes[1].hist(non_other_sims, bins=50, color="#2ECC71", edgecolor="white", alpha=0.8)
    axes[1].axvline(np.median(non_other_sims), color="red", linestyle="--", linewidth=2,
                    label=f"Median: {np.median(non_other_sims):.3f}")
    axes[1].axvline(np.mean(non_other_sims), color="orange", linestyle="--", linewidth=2,
                    label=f"Mean: {np.mean(non_other_sims):.3f}")
    axes[1].set_xlabel("Embedding Similarity", fontsize=12)
    axes[1].set_ylabel("Count", fontsize=12)
    axes[1].set_title(f"Excluding 'Other' (n={len(non_other_sims)})", fontsize=14, fontweight="bold")
    axes[1].legend(fontsize=11)

    plt.suptitle("Distribution of Semantic Similarity Between Confused Label Pairs",
                 fontsize=16, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(output_dir / "confusion_similarity_histogram.png", dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_dir / 'confusion_similarity_histogram.png'}")


def plot_severity_boxplot(confusions: list, output_dir: Path):
    """Box plot of similarity by severity level."""
    severity_order = ["same-narrative", "same-category", "cross-category", "hallucination"]
    severity_labels = ["Same\nNarrative", "Same\nCategory", "Cross\nCategory", "Hallucination"]
    colors = ["#2ECC71", "#F39C12", "#E74C3C", "#9B59B6"]

    data = []
    for sev in severity_order:
        sims = [c["similarity"] for c in confusions if c["severity"] == sev]
        data.append(sims)

    fig, ax = plt.subplots(figsize=(10, 6))
    bp = ax.boxplot(data, tick_labels=severity_labels, patch_artist=True, widths=0.6)

    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    for sev, sims, x in zip(severity_order, data, range(1, 5)):
        if sims:
            ax.text(x, max(sims) + 0.02, f"n={len(sims)}\nμ={np.mean(sims):.3f}",
                    ha="center", fontsize=9, fontweight="bold")

    ax.set_ylabel("Embedding Similarity", fontsize=12)
    ax.set_title("Confusion Similarity by Structural Severity Level",
                 fontsize=14, fontweight="bold")
    ax.set_ylim(-0.05, 1.15)
    ax.axhline(0.5, color="gray", linestyle=":", alpha=0.5, label="sim=0.5 threshold")
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "confusion_severity_boxplot.png", dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_dir / 'confusion_severity_boxplot.png'}")


def plot_model_comparison(confusions: list, output_dir: Path):
    """Bar chart comparing models on severity distribution."""
    non_other = [c for c in confusions if "Other" not in c["gold"] and "Other" not in c["pred"]]

    model_bands = defaultdict(lambda: defaultdict(int))
    model_totals = defaultdict(int)

    for c in non_other:
        model = extract_model(c["experiment"])
        band = compute_band(c["similarity"])
        model_bands[model][band] = model_bands[model].get(band, 0) + 1
        model_totals[model] += 1

    models = sorted(model_totals.keys())
    band_labels = [b[0] for b in SIMILARITY_BANDS]
    band_colors = ["#2ECC71", "#82E0AA", "#F39C12", "#E67E22", "#E74C3C"]

    fig, ax = plt.subplots(figsize=(12, 7))
    x = np.arange(len(models))
    width = 0.15

    for i, (band_label, color) in enumerate(zip(band_labels, band_colors)):
        values = [model_bands[m].get(band_label, 0) / model_totals[m] * 100
                  for m in models]
        ax.bar(x + i * width, values, width, label=band_label, color=color, edgecolor="white")

    ax.set_xlabel("Model", fontsize=12)
    ax.set_ylabel("% of Confusions", fontsize=12)
    ax.set_title("Confusion Similarity Distribution by Model (excl. Other)",
                 fontsize=14, fontweight="bold")
    ax.set_xticks(x + width * 2)
    ax.set_xticklabels(models, fontsize=10)
    ax.legend(loc="upper right", fontsize=9)
    plt.tight_layout()
    plt.savefig(output_dir / "confusion_similarity_by_model.png", dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_dir / 'confusion_similarity_by_model.png'}")


def plot_method_language_heatmap(confusions: list, output_dir: Path):
    """Heatmap of mean similarity by method x language."""
    non_other = [c for c in confusions if "Other" not in c["gold"] and "Other" not in c["pred"]]

    methods = sorted(set(extract_method(c["experiment"]) for c in non_other))
    langs = ["EN", "BG", "HI", "PT", "RU"]

    data = np.zeros((len(methods), len(langs)))
    data[:] = np.nan

    for i, method in enumerate(methods):
        for j, lang in enumerate(langs):
            sims = [c["similarity"] for c in non_other
                    if extract_method(c["experiment"]) == method and c["language"] == lang]
            if sims:
                data[i, j] = np.mean(sims)

    fig, ax = plt.subplots(figsize=(10, 6))
    import matplotlib
    cmap = matplotlib.colormaps.get_cmap("RdYlGn")
    im = ax.imshow(data, cmap=cmap, vmin=0.3, vmax=0.7, aspect="auto")

    ax.set_xticks(range(len(langs)))
    ax.set_xticklabels(langs, fontsize=11)
    ax.set_yticks(range(len(methods)))
    ax.set_yticklabels(methods, fontsize=11)

    for i in range(len(methods)):
        for j in range(len(langs)):
            if not np.isnan(data[i, j]):
                ax.text(j, i, f"{data[i, j]:.3f}", ha="center", va="center",
                        fontsize=10, fontweight="bold",
                        color="white" if data[i, j] < 0.4 or data[i, j] > 0.65 else "black")

    plt.colorbar(im, ax=ax, label="Mean Embedding Similarity")
    ax.set_title("Mean Confusion Similarity: Method x Language (excl. Other)\nHigher = more expected confusions, Lower = more severe errors",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_dir / "confusion_similarity_method_language.png", dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_dir / 'confusion_similarity_method_language.png'}")


def main():
    parser = argparse.ArgumentParser(
        description="Statistical analysis of confusion severity using semantic similarity"
    )
    parser.add_argument("--confusions", type=str,
                        default="results/analysis/confusion/all_confusions.json")
    parser.add_argument("--output-dir", type=str,
                        default="results/analysis/confusion/")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Loading confusions...")
    with open(args.confusions, "r", encoding="utf-8") as f:
        confusions = json.load(f)
    print(f"Loaded {len(confusions)} confusion entries")

    # Generate plots
    print("\nGenerating visualizations...")
    plot_similarity_histogram(confusions, output_dir)
    plot_severity_boxplot(confusions, output_dir)
    plot_model_comparison(confusions, output_dir)
    plot_method_language_heatmap(confusions, output_dir)

    # Generate report
    print("\nGenerating report...")
    report_text = generate_report(confusions, output_dir)
    report_path = output_dir / "confusion_similarity_statistics.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"Saved: {report_path}")

    print("\nDone!")


if __name__ == "__main__":
    main()

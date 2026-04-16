"""
Data exploration and analysis for the SemEval-2025 Task 10 propaganda narrative dataset.

Produces:
- Narrative and subnarrative frequency distributions (per language, per split)
- Co-occurrence matrices (which narratives appear together in the same document)
- Category balance analysis (URW vs CC)
- Train vs dev distribution comparison
- A comprehensive Markdown report with all findings

Usage:
    python data_exploration.py --output-dir ../../results/analysis/data_exploration/
"""

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
LANGUAGES = ["EN", "BG", "HI", "PT", "RU"]
DATA_ROOT = Path(__file__).resolve().parents[2] / "data"
TRAIN_DIR = DATA_ROOT / "train"
DEV_DIR = DATA_ROOT / "dev-documents_4_December"
TAXONOMY_FILE = DATA_ROOT / "taxonomy.json"
NARRATIVE_DEFS_FILE = DATA_ROOT / "narrative_definitions.csv"
SUBNARRATIVE_DEFS_FILE = DATA_ROOT / "subnarrative_definitions.csv"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_taxonomy(path: Path = TAXONOMY_FILE) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_definitions(path: Path) -> Dict[str, str]:
    """Load narrative or subnarrative definitions CSV -> {name: definition}."""
    defs = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row.get("narrative") or row.get("subnarrative", "")
            definition = row.get("definition", "")
            if key:
                defs[key.strip()] = definition.strip()
    return defs


def parse_train_annotations(lang: str) -> List[dict]:
    """Parse train subtask-3 annotations. Format: filename<TAB>narrative<TAB>subnarrative<TAB>justification"""
    path = TRAIN_DIR / lang / "subtask-3-annotations.txt"
    if not path.exists():
        return []
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 2:
                continue
            filename = parts[0].strip()
            narrative = parts[1].strip() if len(parts) > 1 else "none"
            subnarrative = parts[2].strip() if len(parts) > 2 else "none"
            records.append({
                "filename": filename,
                "narrative": narrative,
                "subnarrative": subnarrative,
                "language": lang,
                "split": "train",
            })
    return records


def parse_dev_annotations(lang: str) -> List[dict]:
    """Parse dev subtask-3 annotations. Format: filename<TAB>narrative<TAB>subnarrative"""
    path = DEV_DIR / lang / "subtask-3-dominant-narratives.txt"
    if not path.exists():
        return []
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 2:
                continue
            filename = parts[0].strip()
            narrative = parts[1].strip() if len(parts) > 1 else "none"
            subnarrative = parts[2].strip() if len(parts) > 2 else "none"
            records.append({
                "filename": filename,
                "narrative": narrative,
                "subnarrative": subnarrative,
                "language": lang,
                "split": "dev",
            })
    return records


def load_all_annotations() -> pd.DataFrame:
    """Load all train + dev annotations into a single DataFrame."""
    all_records = []
    for lang in LANGUAGES:
        all_records.extend(parse_train_annotations(lang))
        all_records.extend(parse_dev_annotations(lang))
    df = pd.DataFrame(all_records)
    # Extract category from narrative (URW or CC)
    df["category"] = df["narrative"].apply(
        lambda x: x.split(":")[0].strip() if ":" in x else "Other"
    )
    # Extract short narrative name (without category prefix)
    df["narrative_short"] = df["narrative"].apply(
        lambda x: x.split(": ", 1)[1].strip() if ": " in x else x
    )
    # Extract short subnarrative name
    def extract_subnarrative_short(s):
        if s in ("none", "Other", ""):
            return "none"
        parts = s.split(": ")
        return parts[-1].strip() if len(parts) >= 3 else s
    df["subnarrative_short"] = df["subnarrative"].apply(extract_subnarrative_short)
    return df


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------

def compute_narrative_frequencies(df: pd.DataFrame) -> pd.DataFrame:
    """Frequency of each narrative per language and split."""
    return (
        df.groupby(["split", "language", "narrative"])
        .size()
        .reset_index(name="count")
        .sort_values(["split", "language", "count"], ascending=[True, True, False])
    )


def compute_subnarrative_frequencies(df: pd.DataFrame) -> pd.DataFrame:
    """Frequency of each subnarrative per language and split."""
    filtered = df[df["subnarrative"] != "none"]
    return (
        filtered.groupby(["split", "language", "subnarrative"])
        .size()
        .reset_index(name="count")
        .sort_values(["split", "language", "count"], ascending=[True, True, False])
    )


def compute_category_balance(df: pd.DataFrame) -> pd.DataFrame:
    """URW vs CC balance per language and split."""
    return (
        df.groupby(["split", "language", "category"])
        .size()
        .reset_index(name="count")
    )


def compute_cooccurrence_matrix(df: pd.DataFrame, level: str = "narrative") -> pd.DataFrame:
    """
    Compute co-occurrence matrix: how often two labels appear in the same document.
    level: 'narrative' or 'subnarrative'
    """
    # Group by document and collect unique labels
    doc_labels = df.groupby("filename")[level].apply(set).reset_index()
    # Get all unique labels
    all_labels = sorted(set(label for labels in doc_labels[level] for label in labels))
    # Build co-occurrence matrix
    cooc = pd.DataFrame(0, index=all_labels, columns=all_labels)
    for _, row in doc_labels.iterrows():
        labels = list(row[level])
        for i, l1 in enumerate(labels):
            cooc.loc[l1, l1] += 1  # self-occurrence (frequency)
            for l2 in labels[i + 1:]:
                cooc.loc[l1, l2] += 1
                cooc.loc[l2, l1] += 1
    return cooc


def compute_labels_per_document(df: pd.DataFrame) -> pd.DataFrame:
    """How many narratives/subnarratives per document."""
    doc_stats = (
        df.groupby(["split", "language", "filename"])
        .agg(
            n_narratives=("narrative", "nunique"),
            n_subnarratives=("subnarrative", lambda x: x[x != "none"].nunique()),
        )
        .reset_index()
    )
    return doc_stats


def compute_none_subnarrative_rate(df: pd.DataFrame) -> pd.DataFrame:
    """Rate of 'none' subnarratives per language and split."""
    total = df.groupby(["split", "language"]).size().reset_index(name="total")
    nones = (
        df[df["subnarrative"] == "none"]
        .groupby(["split", "language"])
        .size()
        .reset_index(name="none_count")
    )
    merged = total.merge(nones, on=["split", "language"], how="left").fillna(0)
    merged["none_rate"] = merged["none_count"] / merged["total"]
    return merged


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def plot_narrative_distribution(df: pd.DataFrame, split: str, output_dir: Path):
    """Bar chart of narrative frequencies across languages for a given split."""
    subset = df[df["split"] == split]
    if subset.empty:
        return

    fig, axes = plt.subplots(1, len(LANGUAGES), figsize=(6 * len(LANGUAGES), 8), sharey=False)
    if len(LANGUAGES) == 1:
        axes = [axes]

    for ax, lang in zip(axes, LANGUAGES):
        lang_data = subset[subset["language"] == lang]
        freq = lang_data["narrative_short"].value_counts().head(15)
        if freq.empty:
            ax.set_title(f"{lang} (no data)")
            continue
        freq.plot.barh(ax=ax, color=plt.cm.Set2(np.arange(len(freq)) % 8))
        ax.set_title(f"{lang} ({split})")
        ax.set_xlabel("Count")
        ax.invert_yaxis()

    plt.suptitle(f"Top Narratives by Language ({split} set)", fontsize=14, y=1.01)
    plt.tight_layout()
    plt.savefig(output_dir / f"narrative_distribution_{split}.png", dpi=150, bbox_inches="tight")
    plt.close()


def plot_category_balance(df: pd.DataFrame, output_dir: Path):
    """Stacked bar chart of URW vs CC per language."""
    cat_df = compute_category_balance(df)
    for split in ["train", "dev"]:
        subset = cat_df[cat_df["split"] == split]
        if subset.empty:
            continue
        pivot = subset.pivot_table(index="language", columns="category", values="count", fill_value=0)
        pivot = pivot.reindex(LANGUAGES).fillna(0)

        fig, ax = plt.subplots(figsize=(8, 5))
        pivot.plot.bar(stacked=True, ax=ax, color={"URW": "#e74c3c", "CC": "#2ecc71", "Other": "#95a5a6"})
        ax.set_title(f"Category Balance ({split} set)")
        ax.set_ylabel("Number of annotations")
        ax.set_xlabel("Language")
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig(output_dir / f"category_balance_{split}.png", dpi=150, bbox_inches="tight")
        plt.close()


def plot_cooccurrence_heatmap(cooc: pd.DataFrame, title: str, output_path: Path):
    """Heatmap of label co-occurrences."""
    # Shorten labels for display
    short_labels = []
    for label in cooc.index:
        parts = label.split(": ")
        short = parts[-1] if len(parts) >= 2 else label
        if len(short) > 40:
            short = short[:37] + "..."
        short_labels.append(short)

    fig, ax = plt.subplots(figsize=(max(12, len(cooc) * 0.6), max(10, len(cooc) * 0.5)))
    mask = np.zeros_like(cooc.values, dtype=bool)
    # Mask upper triangle for cleaner display
    mask[np.triu_indices_from(mask, k=1)] = True

    sns.heatmap(
        cooc.values, mask=mask, annot=True, fmt="d", cmap="YlOrRd",
        xticklabels=short_labels, yticklabels=short_labels,
        ax=ax, linewidths=0.5, square=True, cbar_kws={"shrink": 0.8}
    )
    ax.set_title(title, fontsize=13)
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def plot_subnarrative_distribution(df: pd.DataFrame, split: str, output_dir: Path):
    """Top subnarratives per category."""
    subset = df[(df["split"] == split) & (df["subnarrative"] != "none")]
    if subset.empty:
        return

    for cat in ["URW", "CC"]:
        cat_data = subset[subset["category"] == cat]
        if cat_data.empty:
            continue
        freq = cat_data["subnarrative_short"].value_counts().head(20)
        fig, ax = plt.subplots(figsize=(10, max(6, len(freq) * 0.35)))
        colors = plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, len(freq)))
        freq.plot.barh(ax=ax, color=colors)
        ax.set_title(f"Top Subnarratives - {cat} ({split} set)")
        ax.set_xlabel("Count")
        ax.invert_yaxis()
        plt.tight_layout()
        plt.savefig(output_dir / f"subnarrative_distribution_{cat.lower()}_{split}.png", dpi=150, bbox_inches="tight")
        plt.close()


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(
    df: pd.DataFrame,
    taxonomy: dict,
    narrative_defs: Dict[str, str],
    subnarrative_defs: Dict[str, str],
    output_dir: Path,
) -> str:
    """Generate a comprehensive Markdown report."""
    lines = []

    lines.append("# Data Exploration Report: SemEval-2025 Task 10 - Propaganda Narrative Detection\n")
    lines.append("This report provides an exploratory analysis of the training and development datasets")
    lines.append("for the multilingual propaganda narrative classification task.\n")

    # --- Taxonomy overview ---
    lines.append("## 1. Taxonomy Overview\n")
    lines.append("The label hierarchy has two levels: **narratives** and **subnarratives**,")
    lines.append("organised under two domains.\n")

    for category, narratives in taxonomy.items():
        n_narratives = len(narratives)
        n_subnarratives = sum(len(subs) for subs in narratives.values())
        lines.append(f"### {category} ({n_narratives} narratives, {n_subnarratives} subnarratives)\n")

        for narrative, subnarratives in narratives.items():
            full_name = f"{category}: {narrative}"
            definition = narrative_defs.get(full_name, "")
            def_text = f" - *{definition}*" if definition else ""
            lines.append(f"**{narrative}**{def_text}\n")

            for sub in subnarratives:
                full_sub = f"{category}: {narrative}: {sub}"
                sub_def = subnarrative_defs.get(full_sub, "")
                sub_text = f": {sub_def}" if sub_def else ""
                lines.append(f"- {sub}{sub_text}")
            lines.append("")

    # --- Dataset summary ---
    lines.append("## 2. Dataset Summary\n")

    for split in ["train", "dev"]:
        subset = df[df["split"] == split]
        if subset.empty:
            continue
        lines.append(f"### {split.capitalize()} Set\n")

        summary_rows = []
        for lang in LANGUAGES:
            lang_data = subset[subset["language"] == lang]
            n_docs = lang_data["filename"].nunique()
            n_annotations = len(lang_data)
            n_urw = len(lang_data[lang_data["category"] == "URW"])
            n_cc = len(lang_data[lang_data["category"] == "CC"])
            n_other = len(lang_data[lang_data["category"] == "Other"])
            n_none_sub = len(lang_data[lang_data["subnarrative"] == "none"])
            summary_rows.append(
                f"| {lang} | {n_docs} | {n_annotations} | {n_urw} | {n_cc} | {n_other} | {n_none_sub} ({n_none_sub/max(n_annotations,1)*100:.0f}%) |"
            )

        lines.append("| Language | Documents | Annotations | URW | CC | Other | Subnarrative=none |")
        lines.append("|----------|-----------|-------------|-----|-----|-------|-------------------|")
        lines.extend(summary_rows)
        lines.append("")

    # --- Narrative frequency ---
    lines.append("## 3. Narrative Frequency Distributions\n")

    for split in ["train", "dev"]:
        subset = df[df["split"] == split]
        if subset.empty:
            continue
        lines.append(f"### {split.capitalize()} Set\n")
        lines.append(f"![Narrative Distribution ({split})](narrative_distribution_{split}.png)\n")

        # Overall frequency table
        freq = subset["narrative"].value_counts()
        lines.append(f"**Top 15 narratives ({split}):**\n")
        lines.append("| Rank | Narrative | Count | % |")
        lines.append("|------|-----------|-------|---|")
        total = len(subset)
        for i, (name, count) in enumerate(freq.head(15).items(), 1):
            pct = count / total * 100
            lines.append(f"| {i} | {name} | {count} | {pct:.1f}% |")
        lines.append("")

    # --- Subnarrative frequency ---
    lines.append("## 4. Subnarrative Frequency Distributions\n")

    for split in ["train", "dev"]:
        subset = df[(df["split"] == split) & (df["subnarrative"] != "none")]
        if subset.empty:
            continue
        lines.append(f"### {split.capitalize()} Set\n")

        for cat in ["URW", "CC"]:
            cat_data = subset[subset["category"] == cat]
            if cat_data.empty:
                continue
            lines.append(f"![Subnarrative Distribution {cat} ({split})](subnarrative_distribution_{cat.lower()}_{split}.png)\n")

            freq = cat_data["subnarrative"].value_counts()
            lines.append(f"**Top 15 {cat} subnarratives ({split}):**\n")
            lines.append("| Rank | Subnarrative | Count |")
            lines.append("|------|--------------|-------|")
            for i, (name, count) in enumerate(freq.head(15).items(), 1):
                lines.append(f"| {i} | {name} | {count} |")
            lines.append("")

    # --- Category balance ---
    lines.append("## 5. Category Balance (URW vs CC)\n")
    for split in ["train", "dev"]:
        lines.append(f"![Category Balance ({split})](category_balance_{split}.png)\n")

    # --- Co-occurrence analysis ---
    lines.append("## 6. Narrative Co-occurrence Analysis\n")
    lines.append("Co-occurrence measures how often two narratives are annotated for the same document.")
    lines.append("High co-occurrence between narratives suggests thematic overlap.\n")

    train_data = df[df["split"] == "train"]
    if not train_data.empty:
        cooc = compute_cooccurrence_matrix(train_data, level="narrative")
        # Report top co-occurring pairs (off-diagonal)
        pairs = []
        labels = cooc.index.tolist()
        for i in range(len(labels)):
            for j in range(i + 1, len(labels)):
                count = cooc.iloc[i, j]
                if count > 0:
                    pairs.append((labels[i], labels[j], count))
        pairs.sort(key=lambda x: x[2], reverse=True)

        lines.append("### Top Co-occurring Narrative Pairs (train set)\n")
        lines.append("| Narrative A | Narrative B | Co-occurrences |")
        lines.append("|-------------|-------------|----------------|")
        for a, b, c in pairs[:20]:
            lines.append(f"| {a} | {b} | {c} |")
        lines.append("")
        lines.append("![Narrative Co-occurrence (train)](cooccurrence_narrative_train.png)\n")

    # --- Labels per document ---
    lines.append("## 7. Labels per Document\n")
    doc_stats = compute_labels_per_document(df)
    for split in ["train", "dev"]:
        subset = doc_stats[doc_stats["split"] == split]
        if subset.empty:
            continue
        lines.append(f"### {split.capitalize()} Set\n")
        lines.append("| Language | Mean narratives/doc | Max narratives/doc | Mean subnarratives/doc | Max subnarratives/doc |")
        lines.append("|----------|--------------------:|-------------------:|-----------------------:|----------------------:|")
        for lang in LANGUAGES:
            lang_data = subset[subset["language"] == lang]
            if lang_data.empty:
                continue
            lines.append(
                f"| {lang} | {lang_data['n_narratives'].mean():.2f} | {lang_data['n_narratives'].max()} "
                f"| {lang_data['n_subnarratives'].mean():.2f} | {lang_data['n_subnarratives'].max()} |"
            )
        lines.append("")

    # --- Cross-language comparison ---
    lines.append("## 8. Cross-Language Comparison\n")
    lines.append("Narrative distributions may vary across languages due to differing media landscapes.\n")

    train_data = df[df["split"] == "train"]
    if not train_data.empty:
        pivot = (
            train_data.groupby(["language", "narrative_short"])
            .size()
            .reset_index(name="count")
            .pivot_table(index="narrative_short", columns="language", values="count", fill_value=0)
        )
        # Normalise per language
        pivot_norm = pivot.div(pivot.sum(axis=0), axis=1) * 100

        lines.append("**Narrative distribution (% of annotations per language, train set):**\n")
        lines.append("| Narrative | " + " | ".join(LANGUAGES) + " |")
        lines.append("|-----------|" + "|".join(["------:" for _ in LANGUAGES]) + "|")
        for narrative in pivot_norm.index:
            vals = " | ".join(f"{pivot_norm.loc[narrative, lang]:.1f}%" for lang in LANGUAGES if lang in pivot_norm.columns)
            lines.append(f"| {narrative} | {vals} |")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Data exploration for SemEval-2025 Task 10")
    parser.add_argument("--output-dir", type=str, default="../../results/analysis/data_exploration/",
                        help="Output directory for report and plots")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("[DataExploration] Loading taxonomy...")
    taxonomy = load_taxonomy()
    narrative_defs = load_definitions(NARRATIVE_DEFS_FILE)
    subnarrative_defs = load_definitions(SUBNARRATIVE_DEFS_FILE)

    print("[DataExploration] Loading annotations...")
    df = load_all_annotations()
    print(f"[DataExploration] Loaded {len(df)} annotations ({df['filename'].nunique()} documents)")
    print(f"  Train: {len(df[df['split']=='train'])} annotations")
    print(f"  Dev:   {len(df[df['split']=='dev'])} annotations")

    # Generate plots
    print("[DataExploration] Generating plots...")
    for split in ["train", "dev"]:
        plot_narrative_distribution(df, split, output_dir)
        plot_subnarrative_distribution(df, split, output_dir)
    plot_category_balance(df, output_dir)

    # Co-occurrence heatmaps
    for split in ["train"]:
        subset = df[df["split"] == split]
        if subset.empty:
            continue

        # Narrative co-occurrence
        cooc_nar = compute_cooccurrence_matrix(subset, level="narrative")
        plot_cooccurrence_heatmap(
            cooc_nar,
            f"Narrative Co-occurrence ({split} set)",
            output_dir / f"cooccurrence_narrative_{split}.png",
        )

        # Subnarrative co-occurrence per category (too large for combined)
        for cat in ["URW", "CC"]:
            cat_data = subset[subset["category"] == cat]
            cat_subs = cat_data[cat_data["subnarrative"] != "none"]
            if len(cat_subs) > 0:
                cooc_sub = compute_cooccurrence_matrix(cat_subs, level="subnarrative")
                if len(cooc_sub) > 1:
                    plot_cooccurrence_heatmap(
                        cooc_sub,
                        f"Subnarrative Co-occurrence - {cat} ({split} set)",
                        output_dir / f"cooccurrence_subnarrative_{cat.lower()}_{split}.png",
                    )

    # Generate report
    print("[DataExploration] Generating report...")
    report = generate_report(df, taxonomy, narrative_defs, subnarrative_defs, output_dir)
    report_path = output_dir / "data_exploration_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"[DataExploration] Report saved to: {report_path}")

    # Save raw data as CSV for further analysis
    freq_nar = compute_narrative_frequencies(df)
    freq_nar.to_csv(output_dir / "narrative_frequencies.csv", index=False)

    freq_sub = compute_subnarrative_frequencies(df)
    freq_sub.to_csv(output_dir / "subnarrative_frequencies.csv", index=False)

    cat_balance = compute_category_balance(df)
    cat_balance.to_csv(output_dir / "category_balance.csv", index=False)

    none_rates = compute_none_subnarrative_rate(df)
    none_rates.to_csv(output_dir / "none_subnarrative_rates.csv", index=False)

    print("[DataExploration] Done!")
    print(f"  Output directory: {output_dir}")


if __name__ == "__main__":
    main()

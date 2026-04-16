"""
Semantic Similarity Hierarchy and Confusion Severity Analysis.

Builds a semantic similarity hierarchy of narratives/subnarratives using their
names and definitions, then analyses prediction confusions to classify them as
"near-miss" (semantically close labels confused) or "severe" (unrelated labels
confused).

Also generates per-language and overall subnarrative-level confusion matrices.

Usage:
    # Build similarity hierarchy only (no predictions needed):
    python semantic_confusion_analysis.py hierarchy \\
        --output-dir ../../results/analysis/semantic_hierarchy/

    # Full confusion analysis (requires predictions):
    python semantic_confusion_analysis.py confusion \\
        --experiments-dir ../../results/experiments/ \\
        --output-dir ../../results/analysis/confusion/
"""

import argparse
import csv
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from scipy.spatial.distance import squareform
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DATA_ROOT = Path(__file__).resolve().parents[2] / "data"
TAXONOMY_FILE = DATA_ROOT / "taxonomy.json"
NARRATIVE_DEFS_FILE = DATA_ROOT / "narrative_definitions.csv"
SUBNARRATIVE_DEFS_FILE = DATA_ROOT / "subnarrative_definitions.csv"
DEV_DIR = DATA_ROOT / "dev-documents_4_December"
LANGUAGES = ["EN", "BG", "HI", "PT", "RU"]

# Structural bonus for same-parent subnarratives in similarity computation
SAME_NARRATIVE_BOOST = 0.20


# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------

def load_taxonomy(path: Path = TAXONOMY_FILE) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_definitions(path: Path) -> Dict[str, str]:
    """Load CSV definitions -> {name: definition}."""
    defs = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row.get("narrative") or row.get("subnarrative", "")
            definition = row.get("definition", "")
            if key:
                defs[key.strip()] = definition.strip()
    return defs


def build_full_label_set(taxonomy: dict) -> Tuple[List[str], List[str]]:
    """Return sorted lists of full narrative and subnarrative labels."""
    narratives = []
    subnarratives = []
    for category, narr_dict in taxonomy.items():
        for narr_name, sub_list in narr_dict.items():
            full_narr = f"{category}: {narr_name}"
            narratives.append(full_narr)
            for sub_name in sub_list:
                if sub_name == "Other":
                    continue
                full_sub = f"{category}: {narr_name}: {sub_name}"
                subnarratives.append(full_sub)
    return sorted(narratives), sorted(subnarratives)


def get_parent_narrative(subnarrative: str) -> str:
    """Extract the parent narrative from a full subnarrative label."""
    parts = subnarrative.split(": ")
    if len(parts) >= 3:
        return f"{parts[0]}: {parts[1]}"
    return subnarrative


def get_category(label: str) -> str:
    """Extract category (URW or CC) from a label."""
    return label.split(":")[0].strip()


# ---------------------------------------------------------------------------
# Semantic similarity
# ---------------------------------------------------------------------------

def build_label_texts(labels: List[str], definitions: Dict[str, str]) -> List[str]:
    """
    Build text representations for each label by combining the label name
    with its definition for richer semantic signal.
    """
    texts = []
    for label in labels:
        # Try to find definition with the full label
        defn = definitions.get(label, "")
        if not defn:
            # Try shorter forms
            parts = label.split(": ")
            for i in range(len(parts)):
                shorter = ": ".join(parts[i:])
                if shorter in definitions:
                    defn = definitions[shorter]
                    break
        # Combine label name and definition
        text = f"{label}. {defn}" if defn else label
        texts.append(text)
    return texts


def compute_tfidf_similarity_matrix(
    labels: List[str],
    definitions: Dict[str, str],
    taxonomy: dict,
) -> np.ndarray:
    """
    Compute pairwise cosine similarity between labels using TF-IDF on
    label names + definitions. Adds a structural bonus for labels sharing
    the same parent narrative.
    """
    texts = build_label_texts(labels, definitions)

    # TF-IDF vectorisation
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.95,
    )
    tfidf_matrix = vectorizer.fit_transform(texts)
    sim_matrix = cosine_similarity(tfidf_matrix).astype(float)

    # Add structural bonus for same-parent-narrative subnarratives
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            parent_i = get_parent_narrative(labels[i])
            parent_j = get_parent_narrative(labels[j])
            if parent_i == parent_j:
                sim_matrix[i, j] = min(1.0, sim_matrix[i, j] + SAME_NARRATIVE_BOOST)
                sim_matrix[j, i] = sim_matrix[i, j]

    return sim_matrix


# Keep backward-compatible alias
compute_similarity_matrix = compute_tfidf_similarity_matrix


def compute_embedding_similarity_matrix(
    labels: List[str],
    definitions: Dict[str, str],
    model_name: str = "all-MiniLM-L6-v2",
) -> np.ndarray:
    """
    Compute pairwise cosine similarity using sentence embeddings.

    Uses sentence-transformers to encode label names + definitions into
    dense vectors, then computes cosine similarity. Captures semantic
    relationships that TF-IDF misses (e.g., synonyms, paraphrases).

    No structural bonus is applied — embeddings should capture the
    semantic relationships directly.
    """
    from sentence_transformers import SentenceTransformer

    texts = build_label_texts(labels, definitions)

    print(f"  Loading embedding model: {model_name}")
    model = SentenceTransformer(model_name)

    print(f"  Encoding {len(texts)} labels...")
    embeddings = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)

    # Cosine similarity (embeddings are already normalized)
    sim_matrix = (embeddings @ embeddings.T).astype(float)

    # Clip to [0, 1] for safety (floating-point can give slightly > 1)
    np.clip(sim_matrix, 0, 1, out=sim_matrix)

    return sim_matrix


def cluster_labels(sim_matrix: np.ndarray, labels: List[str]) -> dict:
    """Perform hierarchical clustering and return the linkage + cluster info."""
    # Convert similarity to distance
    dist_matrix = 1.0 - sim_matrix
    np.fill_diagonal(dist_matrix, 0)
    dist_matrix = np.clip(dist_matrix, 0, None)

    # Make symmetric (floating point)
    dist_matrix = (dist_matrix + dist_matrix.T) / 2

    condensed = squareform(dist_matrix)
    Z = linkage(condensed, method="ward")

    return {"linkage": Z, "labels": labels}


# ---------------------------------------------------------------------------
# Plots for similarity hierarchy
# ---------------------------------------------------------------------------

def plot_similarity_heatmap(
    sim_matrix: np.ndarray,
    labels: List[str],
    output_path: str,
    title: str = "Subnarrative Semantic Similarity",
):
    """Plot a heatmap of pairwise similarity."""
    n = len(labels)
    short_labels = []
    for lab in labels:
        parts = lab.split(": ")
        if len(parts) >= 3:
            short_labels.append(f"{parts[0]}:{parts[-1][:35]}")
        elif len(parts) >= 2:
            short_labels.append(f"{parts[0]}:{parts[-1][:35]}")
        else:
            short_labels.append(lab[:40])

    fig_size = max(14, n * 0.25)
    fig, ax = plt.subplots(figsize=(fig_size, fig_size))

    sns.heatmap(
        sim_matrix,
        xticklabels=short_labels,
        yticklabels=short_labels,
        cmap="YlOrRd",
        vmin=0,
        vmax=1,
        square=True,
        ax=ax,
        cbar_kws={"label": "Cosine Similarity"},
    )
    ax.set_title(title, fontsize=14, fontweight="bold", pad=20)
    plt.setp(ax.get_xticklabels(), rotation=90, ha="right", fontsize=5)
    plt.setp(ax.get_yticklabels(), rotation=0, fontsize=5)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {output_path}")


def plot_dendrogram(
    cluster_info: dict,
    output_path: str,
    title: str = "Subnarrative Hierarchical Clustering",
):
    """Plot a dendrogram from the clustering."""
    labels = cluster_info["labels"]
    short_labels = []
    for lab in labels:
        parts = lab.split(": ")
        if len(parts) >= 3:
            short_labels.append(f"{parts[-1][:45]}")
        else:
            short_labels.append(lab[:45])

    fig_height = max(10, len(labels) * 0.25)
    fig, ax = plt.subplots(figsize=(14, fig_height))

    dendrogram(
        cluster_info["linkage"],
        labels=short_labels,
        orientation="right",
        leaf_font_size=6,
        ax=ax,
    )
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel("Distance (1 - similarity)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {output_path}")


# ---------------------------------------------------------------------------
# Confusion analysis helpers
# ---------------------------------------------------------------------------

def load_predictions(filepath: str) -> Dict[str, Tuple[Set[str], Set[str]]]:
    """
    Load a prediction results.txt file.
    Returns dict: filename -> (set_of_narratives, set_of_subnarratives)
    """
    data = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 2:
                continue
            filename = parts[0].strip()
            narratives = set()
            subnarratives = set()

            narr_str = parts[1].strip() if len(parts) > 1 else ""
            sub_str = parts[2].strip() if len(parts) > 2 else ""

            if narr_str and narr_str.lower() not in ("other", "none"):
                for n in narr_str.split(";"):
                    n = n.strip()
                    if n:
                        narratives.add(n)
            elif narr_str.lower() == "other":
                narratives.add("Other")

            if sub_str and sub_str.lower() not in ("other", "none"):
                for s in sub_str.split(";"):
                    s = s.strip()
                    if s:
                        subnarratives.add(s)
            elif sub_str.lower() == "other":
                subnarratives.add("Other")

            data[filename] = (narratives, subnarratives)
    return data


def load_gold(lang: str) -> Dict[str, Tuple[Set[str], Set[str]]]:
    """Load dev ground truth for a language."""
    path = DEV_DIR / lang / "subtask-3-dominant-narratives.txt"
    if not path.exists():
        print(f"  Warning: Gold file not found: {path}")
        return {}
    data = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 2:
                continue
            filename = parts[0].strip()
            narratives = set()
            subnarratives = set()

            narr_str = parts[1].strip() if len(parts) > 1 else ""
            sub_str = parts[2].strip() if len(parts) > 2 else ""

            if narr_str and narr_str.lower() not in ("other", "none"):
                for n in narr_str.split(";"):
                    n = n.strip()
                    if n:
                        narratives.add(n)
            if sub_str and sub_str.lower() not in ("other", "none"):
                for s in sub_str.split(";"):
                    s = s.strip()
                    if s:
                        subnarratives.add(s)

            data[filename] = (narratives, subnarratives)
    return data


def find_best_run(experiment_dir: Path) -> Optional[Path]:
    """Find the first successful run's results.txt in an experiment directory."""
    manifest_path = experiment_dir / "experiment_manifest.json"
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        for run in manifest.get("runs", []):
            if run.get("status") == "success":
                results_path = experiment_dir / f"run_{run['run_id']}" / "results.txt"
                if results_path.exists():
                    return results_path
    # Fallback: look for any results.txt
    for run_dir in sorted(experiment_dir.glob("run_*")):
        results_path = run_dir / "results.txt"
        if results_path.exists():
            return results_path
    return None


def extract_lang_from_experiment_id(exp_id: str) -> Optional[str]:
    """Extract language code from experiment directory name."""
    for lang in LANGUAGES:
        if f"_{lang.lower()}_" in f"_{exp_id}_":
            return lang
    return None


def compute_multilabel_confusion(
    gold: Dict[str, Set[str]],
    pred: Dict[str, Set[str]],
) -> Tuple[np.ndarray, List[str]]:
    """
    Compute multi-label confusion matrix.
    confusion[i][j] = number of documents where gold label i appears and
                      predicted label j appears simultaneously.
    """
    all_labels = sorted(
        set(l for s in gold.values() for l in s)
        | set(l for s in pred.values() for l in s)
    )
    if not all_labels:
        return np.zeros((0, 0), dtype=int), []

    label_idx = {l: i for i, l in enumerate(all_labels)}
    n = len(all_labels)
    matrix = np.zeros((n, n), dtype=int)

    for filename in gold:
        if filename not in pred:
            continue
        for gl in gold[filename]:
            for pl in pred[filename]:
                matrix[label_idx[gl]][label_idx[pl]] += 1

    return matrix, all_labels


def classify_confusion_severity(
    true_label: str,
    pred_label: str,
    sim_matrix: np.ndarray,
    label_list: List[str],
) -> Tuple[str, float]:
    """
    Classify a confusion pair using taxonomy structure + semantic similarity.

    Severity levels (from least to most severe):
    - correct: Same label
    - same-narrative: Siblings under the same parent narrative
    - same-category: Different narratives but same domain (URW or CC)
    - cross-category: Different domains entirely (URW vs CC)
    - hallucination: Involves "Other" label

    Returns:
        (severity, similarity_score)
    """
    if true_label == pred_label:
        return ("correct", 1.0)

    # Handle "Other" labels
    if true_label == "Other" or pred_label == "Other":
        return ("hallucination", 0.0)

    # Look up similarity
    sim = 0.0
    if true_label in label_list and pred_label in label_list:
        i = label_list.index(true_label)
        j = label_list.index(pred_label)
        sim = sim_matrix[i, j]

    # Check structural relationship
    same_parent = get_parent_narrative(true_label) == get_parent_narrative(pred_label)
    cat_true = get_category(true_label)
    cat_pred = get_category(pred_label)
    same_category = cat_true == cat_pred

    if same_parent:
        return ("same-narrative", sim)
    elif same_category:
        return ("same-category", sim)
    else:
        return ("cross-category", sim)


# ---------------------------------------------------------------------------
# Confusion matrix plotting
# ---------------------------------------------------------------------------

def plot_confusion_matrix(
    matrix: np.ndarray,
    labels: List[str],
    output_path: str,
    title: str,
    normalize: bool = True,
):
    """Plot a confusion heatmap for subnarratives."""
    if matrix.size == 0:
        return

    short_labels = []
    for lab in labels:
        parts = lab.split(": ")
        if len(parts) >= 3:
            short_labels.append(f"{parts[0]}:..:{parts[-1][:30]}")
        elif len(parts) >= 2:
            short_labels.append(f"{parts[0]}:{parts[-1][:30]}")
        else:
            short_labels.append(lab[:35])

    if normalize:
        row_sums = matrix.sum(axis=1, keepdims=True).astype(float)
        row_sums[row_sums == 0] = 1
        plot_matrix = (matrix / row_sums * 100).astype(float)
        fmt = ".0f"
        cbar_label = "Percentage (%)"
    else:
        plot_matrix = matrix
        fmt = "d"
        cbar_label = "Count"

    n = len(labels)
    fig_size = max(12, n * 0.3)
    fig, ax = plt.subplots(figsize=(fig_size, fig_size * 0.85))

    sns.heatmap(
        plot_matrix,
        xticklabels=short_labels,
        yticklabels=short_labels,
        cmap="YlOrRd",
        annot=n <= 25,
        fmt=fmt,
        square=False,
        ax=ax,
        cbar_kws={"label": cbar_label},
    )
    ax.set_title(title, fontsize=13, fontweight="bold", pad=20)
    ax.set_xlabel("Predicted", fontsize=11, fontweight="bold")
    ax.set_ylabel("Gold", fontsize=11, fontweight="bold")
    plt.setp(ax.get_xticklabels(), rotation=90, ha="right", fontsize=6)
    plt.setp(ax.get_yticklabels(), rotation=0, fontsize=6)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {output_path}")


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def _format_similarity_tables(
    sim_matrix: np.ndarray,
    labels: List[str],
    method_name: str,
) -> str:
    """Format the standard similarity tables for a single method."""
    report = []

    # --- Most similar pairs ---
    report.append(f"### Most Similar Subnarrative Pairs ({method_name})\n\n")
    report.append("These pairs have the highest semantic similarity and are most likely to be ")
    report.append("confused with each other during classification.\n\n")
    report.append("| Rank | Label A | Label B | Similarity | Same Parent? |\n")
    report.append("|------|---------|---------|------------|-------------|\n")

    pairs = []
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            pairs.append((labels[i], labels[j], sim_matrix[i, j]))
    pairs.sort(key=lambda x: x[2], reverse=True)

    for rank, (a, b, sim) in enumerate(pairs[:30], 1):
        same_parent = "Yes" if get_parent_narrative(a) == get_parent_narrative(b) else "No"
        short_a = a.split(": ")[-1][:40]
        short_b = b.split(": ")[-1][:40]
        cat_a = a.split(":")[0].strip()
        cat_b = b.split(":")[0].strip()
        report.append(f"| {rank} | {cat_a}: {short_a} | {cat_b}: {short_b} | {sim:.3f} | {same_parent} |\n")

    # --- Most dissimilar siblings ---
    report.append(f"\n### Most Dissimilar Sibling Subnarratives ({method_name})\n\n")
    report.append("Subnarratives under the same parent narrative that are most different ")
    report.append("semantically. High confusion between these would be more surprising.\n\n")
    report.append("| Parent Narrative | Label A | Label B | Similarity |\n")
    report.append("|-----------------|---------|---------|------------|\n")

    sibling_pairs = []
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            parent_i = get_parent_narrative(labels[i])
            parent_j = get_parent_narrative(labels[j])
            if parent_i == parent_j:
                sibling_pairs.append((parent_i, labels[i], labels[j], sim_matrix[i, j]))
    sibling_pairs.sort(key=lambda x: x[3])

    for parent, a, b, sim in sibling_pairs[:15]:
        short_a = a.split(": ")[-1][:35]
        short_b = b.split(": ")[-1][:35]
        short_parent = parent.split(": ", 1)[-1][:35]
        report.append(f"| {short_parent} | {short_a} | {short_b} | {sim:.3f} |\n")

    # --- Cross-category ---
    report.append(f"\n### Cross-Category Similarities ({method_name})\n\n")
    report.append("Pairs from different domains (URW vs CC) that are semantically similar.\n\n")
    report.append("| URW Subnarrative | CC Subnarrative | Similarity |\n")
    report.append("|-----------------|-----------------|------------|\n")

    cross_pairs = []
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            cat_i = get_category(labels[i])
            cat_j = get_category(labels[j])
            if cat_i != cat_j:
                cross_pairs.append((labels[i], labels[j], sim_matrix[i, j]))
    cross_pairs.sort(key=lambda x: x[2], reverse=True)

    for a, b, sim in cross_pairs[:15]:
        if get_category(a) == "URW":
            urw_lab, cc_lab = a, b
        else:
            urw_lab, cc_lab = b, a
        short_urw = urw_lab.split(": ")[-1][:40]
        short_cc = cc_lab.split(": ")[-1][:40]
        report.append(f"| {short_urw} | {short_cc} | {sim:.3f} |\n")

    return "".join(report)


def generate_hierarchy_report(
    sim_matrix: np.ndarray,
    labels: List[str],
    definitions: Dict[str, str],
    taxonomy: dict,
    emb_sim_matrix: Optional[np.ndarray] = None,
    embedding_model: Optional[str] = None,
) -> str:
    """Generate a Markdown report of the semantic similarity hierarchy."""
    has_embeddings = emb_sim_matrix is not None

    report = ["# Semantic Similarity Hierarchy of Narratives and Subnarratives\n\n"]

    if has_embeddings:
        report.append("This report compares two methods for computing semantic similarity ")
        report.append("between subnarrative labels:\n\n")
        report.append(f"1. **TF-IDF** (bag-of-words): TF-IDF cosine similarity on label names + definitions, ")
        report.append(f"with a +{SAME_NARRATIVE_BOOST} structural bonus for same-parent subnarratives.\n")
        report.append(f"2. **Embeddings** (`{embedding_model}`): Dense sentence embeddings that capture ")
        report.append(f"semantic meaning beyond word overlap. No structural bonus applied.\n\n")
        report.append("Embeddings are better at identifying semantically related labels that share ")
        report.append("few words (e.g., *\"The West is weak\"* and *\"The EU is divided\"* are semantically ")
        report.append("close but have no word overlap). TF-IDF is limited to lexical overlap.\n\n")
    else:
        report.append("This report presents the semantic similarity between all subnarrative labels ")
        report.append("in the taxonomy, computed using TF-IDF cosine similarity on label names and ")
        report.append("definitions, with a structural bonus for subnarratives sharing the same ")
        report.append("parent narrative.\n\n")

    # --- Taxonomy overview by category ---
    for category in ["URW", "CC"]:
        cat_name = "Ukraine-Russia War" if category == "URW" else "Climate Change"
        report.append(f"## {category} ({cat_name})\n\n")

        narr_dict = taxonomy.get(category, {})
        for narr_name, sub_list in narr_dict.items():
            full_narr = f"{category}: {narr_name}"
            narr_def = definitions.get(full_narr, definitions.get(narr_name, ""))
            report.append(f"### {full_narr}\n")
            if narr_def:
                report.append(f"*{narr_def}*\n\n")
            else:
                report.append("\n")

            for sub_name in sub_list:
                if sub_name == "Other":
                    continue
                full_sub = f"{category}: {narr_name}: {sub_name}"
                sub_def = definitions.get(full_sub, definitions.get(f"{full_narr}: {sub_name}", ""))
                if sub_def:
                    report.append(f"- **{sub_name}**: {sub_def}\n")
                else:
                    report.append(f"- **{sub_name}**\n")
            report.append("\n")

    # --- Similarity tables ---
    if has_embeddings:
        report.append("---\n\n## Similarity Analysis: Embeddings (Primary)\n\n")
        report.append(_format_similarity_tables(emb_sim_matrix, labels, "Embeddings"))

        report.append("\n---\n\n## Similarity Analysis: TF-IDF (Baseline)\n\n")
        report.append(_format_similarity_tables(sim_matrix, labels, "TF-IDF"))

        # --- Method comparison ---
        report.append("\n---\n\n## TF-IDF vs Embedding Comparison\n\n")
        report.append("This section highlights where the two methods disagree most, ")
        report.append("revealing pairs where embeddings capture semantic relationships ")
        report.append("that TF-IDF misses (and vice versa).\n\n")

        report.append("### Pairs Where Embeddings >> TF-IDF\n\n")
        report.append("These pairs are semantically related (high embedding similarity) but ")
        report.append("share few words (low TF-IDF). Embeddings correctly identify the relationship.\n\n")
        report.append("| Label A | Label B | Embedding Sim | TF-IDF Sim | Difference |\n")
        report.append("|---------|---------|---------------|------------|------------|\n")

        diffs = []
        for i in range(len(labels)):
            for j in range(i + 1, len(labels)):
                emb_s = emb_sim_matrix[i, j]
                tfidf_s = sim_matrix[i, j]
                diffs.append((labels[i], labels[j], emb_s, tfidf_s, emb_s - tfidf_s))

        # Embedding >> TF-IDF (embeddings capture more)
        diffs_emb_higher = sorted(diffs, key=lambda x: x[4], reverse=True)
        for a, b, emb_s, tfidf_s, diff in diffs_emb_higher[:20]:
            short_a = a.split(": ")[-1][:35]
            short_b = b.split(": ")[-1][:35]
            report.append(f"| {short_a} | {short_b} | {emb_s:.3f} | {tfidf_s:.3f} | +{diff:.3f} |\n")

        report.append("\n### Pairs Where TF-IDF >> Embeddings\n\n")
        report.append("These pairs share many words (high TF-IDF) but embeddings judge them ")
        report.append("less similar. Often due to structural bonus or negation patterns.\n\n")
        report.append("| Label A | Label B | TF-IDF Sim | Embedding Sim | Difference |\n")
        report.append("|---------|---------|------------|---------------|------------|\n")

        diffs_tfidf_higher = sorted(diffs, key=lambda x: x[4])
        for a, b, emb_s, tfidf_s, diff in diffs_tfidf_higher[:20]:
            short_a = a.split(": ")[-1][:35]
            short_b = b.split(": ")[-1][:35]
            report.append(f"| {short_a} | {short_b} | {tfidf_s:.3f} | {emb_s:.3f} | {abs(diff):.3f} |\n")

        # --- Correlation analysis ---
        all_tfidf = []
        all_emb = []
        for i in range(len(labels)):
            for j in range(i + 1, len(labels)):
                all_tfidf.append(sim_matrix[i, j])
                all_emb.append(emb_sim_matrix[i, j])
        from scipy.stats import pearsonr, spearmanr
        pearson_r, pearson_p = pearsonr(all_tfidf, all_emb)
        spearman_r, spearman_p = spearmanr(all_tfidf, all_emb)

        report.append(f"\n### Correlation Between Methods\n\n")
        report.append(f"| Metric | Value |\n")
        report.append(f"|--------|-------|\n")
        report.append(f"| Pearson r | {pearson_r:.3f} (p={pearson_p:.2e}) |\n")
        report.append(f"| Spearman rho | {spearman_r:.3f} (p={spearman_p:.2e}) |\n")
        report.append(f"| TF-IDF mean similarity | {np.mean(all_tfidf):.3f} |\n")
        report.append(f"| Embedding mean similarity | {np.mean(all_emb):.3f} |\n\n")

        if pearson_r < 0.5:
            report.append("The low correlation indicates the methods capture substantially ")
            report.append("different aspects of label similarity. Embeddings are recommended ")
            report.append("as the primary similarity measure for confusion severity analysis.\n\n")
        elif pearson_r < 0.7:
            report.append("Moderate correlation — the methods agree on some pairs but diverge ")
            report.append("on others. Embeddings provide richer semantic signal.\n\n")
        else:
            report.append("High correlation — the methods largely agree, though embeddings ")
            report.append("capture additional nuance for semantically similar labels.\n\n")
    else:
        report.append("---\n\n## Similarity Analysis\n\n")
        report.append(_format_similarity_tables(sim_matrix, labels, "TF-IDF"))

    return "".join(report)


def generate_confusion_report(
    all_confusions: List[dict],
    sim_matrix: np.ndarray,
    label_list: List[str],
    lang_results: Dict[str, dict],
) -> str:
    """Generate a Markdown report of confusion severity analysis."""
    SEVERITY_ORDER = ["same-narrative", "same-category", "cross-category", "hallucination"]

    report = ["# Confusion Severity Analysis\n\n"]
    report.append("This report classifies prediction confusions using both taxonomy structure ")
    report.append("and semantic similarity between labels.\n\n")
    report.append("**Severity levels** (least to most severe):\n")
    report.append("- **same-narrative**: Gold and predicted are siblings under the same parent narrative (expected confusion)\n")
    report.append("- **same-category**: Different narratives but same domain (URW or CC)\n")
    report.append("- **cross-category**: Different domains entirely (URW vs CC) — most severe structural error\n")
    report.append("- **hallucination**: Involves the \"Other\" label (model predicts unclassifiable or misses all labels)\n\n")

    # --- Overall severity distribution ---
    report.append("## Overall Confusion Severity Distribution\n\n")

    severity_counts = Counter(c["severity"] for c in all_confusions if c["severity"] != "correct")
    total_errors = sum(severity_counts.values())

    if total_errors > 0:
        report.append("| Severity | Count | Percentage | Description |\n")
        report.append("|----------|-------|------------|-------------|\n")
        descriptions = {
            "same-narrative": "Sibling subnarratives confused",
            "same-category": "Same domain, different narrative",
            "cross-category": "Wrong domain entirely",
            "hallucination": "Other label involved",
        }
        for sev in SEVERITY_ORDER:
            cnt = severity_counts.get(sev, 0)
            pct = cnt / total_errors * 100
            desc = descriptions.get(sev, "")
            report.append(f"| {sev} | {cnt} | {pct:.1f}% | {desc} |\n")
        report.append(f"| **Total** | **{total_errors}** | **100%** | |\n\n")
    else:
        report.append("No confusions found.\n\n")

    # --- Per-language summary ---
    report.append("## Per-Language Confusion Severity\n\n")
    report.append("| Language | Total | Same-Narr | Same-Cat | Cross-Cat | Halluc. | Cross-Cat % |\n")
    report.append("|----------|-------|-----------|----------|-----------|---------|-------------|\n")

    for lang in LANGUAGES:
        if lang not in lang_results:
            continue
        lang_conf = lang_results[lang].get("confusions", [])
        lang_sev = Counter(c["severity"] for c in lang_conf if c["severity"] != "correct")
        total = sum(lang_sev.values())
        if total == 0:
            continue
        same_n = lang_sev.get("same-narrative", 0)
        same_c = lang_sev.get("same-category", 0)
        cross = lang_sev.get("cross-category", 0)
        halluc = lang_sev.get("hallucination", 0)
        cross_pct = cross / total * 100 if total > 0 else 0
        report.append(f"| {lang} | {total} | {same_n} | {same_c} | {cross} | {halluc} | {cross_pct:.1f}% |\n")
    report.append("\n")

    # --- Per-experiment summary ---
    report.append("## Per-Experiment Confusion Severity\n\n")
    report.append("| Experiment | Lang | Total | Same-Narr | Same-Cat | Cross-Cat | Halluc. | Cross % |\n")
    report.append("|------------|------|-------|-----------|----------|-----------|---------|--------|\n")

    exp_groups = defaultdict(list)
    for c in all_confusions:
        if c["severity"] != "correct":
            exp_groups[c["experiment"]].append(c)

    for exp_name in sorted(exp_groups.keys()):
        confs = exp_groups[exp_name]
        lang = confs[0].get("language", "?")
        sev = Counter(c["severity"] for c in confs)
        total = len(confs)
        same_n = sev.get("same-narrative", 0)
        same_c = sev.get("same-category", 0)
        cross = sev.get("cross-category", 0)
        halluc = sev.get("hallucination", 0)
        cross_pct = cross / total * 100 if total > 0 else 0
        short_exp = exp_name[:45]
        report.append(f"| {short_exp} | {lang} | {total} | {same_n} | {same_c} | {cross} | {halluc} | {cross_pct:.1f}% |\n")
    report.append("\n")

    # --- Most common cross-category confusions ---
    cross_confs = [c for c in all_confusions if c["severity"] == "cross-category"]
    if cross_confs:
        report.append("## Most Common Cross-Category Confusions\n\n")
        report.append("These are the most severe structural errors — the model confuses labels ")
        report.append("from entirely different domains (URW vs CC).\n\n")
        report.append("| Gold Label | Predicted Label | Count | Similarity |\n")
        report.append("|------------|-----------------|-------|------------|\n")

        pair_counts = Counter()
        pair_sims = defaultdict(list)
        for c in cross_confs:
            pair = (c["gold"], c["pred"])
            pair_counts[pair] += 1
            pair_sims[pair].append(c["similarity"])

        for (gold, pred), count in pair_counts.most_common(15):
            avg_sim = np.mean(pair_sims[(gold, pred)])
            short_gold = f"{get_category(gold)}: {gold.split(': ')[-1][:30]}"
            short_pred = f"{get_category(pred)}: {pred.split(': ')[-1][:30]}"
            report.append(f"| {short_gold} | {short_pred} | {count} | {avg_sim:.3f} |\n")
        report.append("\n")

    # --- Most common same-category confusions (with similarity) ---
    samecat_confs = [c for c in all_confusions if c["severity"] == "same-category"]
    if samecat_confs:
        report.append("## Most Common Same-Category Confusions\n\n")
        report.append("Different narratives within the same domain confused. Similarity score ")
        report.append("indicates semantic relatedness (higher = more understandable confusion).\n\n")
        report.append("| Gold Label | Predicted Label | Count | Similarity |\n")
        report.append("|------------|-----------------|-------|------------|\n")

        pair_counts = Counter()
        pair_sims = defaultdict(list)
        for c in samecat_confs:
            pair = (c["gold"], c["pred"])
            pair_counts[pair] += 1
            pair_sims[pair].append(c["similarity"])

        for (gold, pred), count in pair_counts.most_common(25):
            avg_sim = np.mean(pair_sims[(gold, pred)])
            short_gold = gold.split(": ")[-1][:35]
            short_pred = pred.split(": ")[-1][:35]
            report.append(f"| {short_gold} | {short_pred} | {count} | {avg_sim:.3f} |\n")
        report.append("\n")

    # --- Same-narrative confusions ---
    same_confs = [c for c in all_confusions if c["severity"] == "same-narrative"]
    if same_confs:
        report.append("## Most Common Same-Narrative Confusions\n\n")
        report.append("Confusions between sibling subnarratives under the same parent narrative. ")
        report.append("These are the most expected errors.\n\n")
        report.append("| Parent Narrative | Gold Subnarrative | Predicted Subnarrative | Count | Similarity |\n")
        report.append("|-----------------|-------------------|----------------------|-------|------------|\n")

        pair_counts = Counter()
        pair_sims = defaultdict(list)
        for c in same_confs:
            pair_counts[(c["gold"], c["pred"])] += 1
            pair_sims[(c["gold"], c["pred"])].append(c["similarity"])

        for (gold, pred), count in pair_counts.most_common(20):
            avg_sim = np.mean(pair_sims[(gold, pred)])
            parent = get_parent_narrative(gold).split(": ", 1)[-1][:25]
            short_gold = gold.split(": ")[-1][:28]
            short_pred = pred.split(": ")[-1][:28]
            report.append(f"| {parent} | {short_gold} | {short_pred} | {count} | {avg_sim:.3f} |\n")
        report.append("\n")

    # --- Hallucination analysis ---
    halluc_confs = [c for c in all_confusions if c["severity"] == "hallucination"]
    if halluc_confs:
        report.append("## Hallucination Analysis (Other Label)\n\n")

        gold_is_other = [c for c in halluc_confs if c["gold"] == "Other"]
        pred_is_other = [c for c in halluc_confs if c["pred"] == "Other"]

        report.append(f"- Gold is \"Other\", model predicts a label: {len(gold_is_other)} cases\n")
        report.append(f"- Gold has a label, model predicts \"Other\": {len(pred_is_other)} cases\n\n")

        if pred_is_other:
            report.append("### Labels Most Often Missed (predicted as Other)\n\n")
            report.append("| Gold Label | Count |\n")
            report.append("|------------|-------|\n")
            missed = Counter(c["gold"] for c in pred_is_other)
            for label, count in missed.most_common(15):
                short = label.split(": ")[-1][:40]
                report.append(f"| {short} | {count} |\n")
            report.append("\n")

    return "".join(report)


# ---------------------------------------------------------------------------
# Main commands
# ---------------------------------------------------------------------------

def plot_similarity_comparison(
    tfidf_sim: np.ndarray,
    emb_sim: np.ndarray,
    labels: List[str],
    output_path: str,
):
    """Plot a scatter of TF-IDF vs embedding similarity for all label pairs."""
    tfidf_vals = []
    emb_vals = []
    pair_colors = []
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            tfidf_vals.append(tfidf_sim[i, j])
            emb_vals.append(emb_sim[i, j])
            same_parent = get_parent_narrative(labels[i]) == get_parent_narrative(labels[j])
            same_cat = get_category(labels[i]) == get_category(labels[j])
            if same_parent:
                pair_colors.append("#2ecc71")  # green
            elif same_cat:
                pair_colors.append("#f39c12")  # orange
            else:
                pair_colors.append("#e74c3c")  # red

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(tfidf_vals, emb_vals, c=pair_colors, alpha=0.4, s=12)
    ax.plot([0, 1], [0, 1], "k--", alpha=0.3, label="y = x")
    ax.set_xlabel("TF-IDF Cosine Similarity", fontsize=12)
    ax.set_ylabel("Embedding Cosine Similarity", fontsize=12)
    ax.set_title("TF-IDF vs Embedding Similarity", fontsize=14, fontweight="bold")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Legend
    from matplotlib.patches import Patch
    legend_elems = [
        Patch(facecolor="#2ecc71", label="Same narrative"),
        Patch(facecolor="#f39c12", label="Same category"),
        Patch(facecolor="#e74c3c", label="Cross category"),
    ]
    ax.legend(handles=legend_elems, loc="upper left")

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {output_path}")


def cmd_hierarchy(args):
    """Build semantic similarity hierarchy."""
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    embedding_model = getattr(args, "embedding_model", "all-MiniLM-L6-v2")

    print("Loading taxonomy and definitions...")
    taxonomy = load_taxonomy()
    narr_defs = load_definitions(NARRATIVE_DEFS_FILE)
    sub_defs = load_definitions(SUBNARRATIVE_DEFS_FILE)
    all_defs = {**narr_defs, **sub_defs}

    narratives, subnarratives = build_full_label_set(taxonomy)
    print(f"  {len(narratives)} narratives, {len(subnarratives)} subnarratives")

    # --- TF-IDF subnarrative similarity ---
    print("\n[1/2] Computing TF-IDF similarity matrix...")
    tfidf_sim = compute_tfidf_similarity_matrix(subnarratives, all_defs, taxonomy)
    tfidf_cluster = cluster_labels(tfidf_sim, subnarratives)

    # --- Embedding subnarrative similarity ---
    print("\n[2/2] Computing embedding similarity matrix...")
    emb_sim = compute_embedding_similarity_matrix(subnarratives, all_defs, embedding_model)
    emb_cluster = cluster_labels(emb_sim, subnarratives)

    # --- Generate plots for BOTH methods ---
    print("\nGenerating plots...")

    # TF-IDF plots
    plot_similarity_heatmap(
        tfidf_sim, subnarratives,
        str(output_dir / "subnarrative_similarity_tfidf.png"),
        "Subnarrative Similarity (TF-IDF + Structure)",
    )
    plot_dendrogram(
        tfidf_cluster,
        str(output_dir / "subnarrative_dendrogram_tfidf.png"),
        "Subnarrative Clustering (TF-IDF)",
    )

    # Embedding plots
    plot_similarity_heatmap(
        emb_sim, subnarratives,
        str(output_dir / "subnarrative_similarity_embedding.png"),
        f"Subnarrative Similarity (Embeddings: {embedding_model})",
    )
    plot_dendrogram(
        emb_cluster,
        str(output_dir / "subnarrative_dendrogram_embedding.png"),
        f"Subnarrative Clustering (Embeddings: {embedding_model})",
    )

    # Comparison scatter plot
    plot_similarity_comparison(
        tfidf_sim, emb_sim, subnarratives,
        str(output_dir / "tfidf_vs_embedding_scatter.png"),
    )

    # --- Per-category plots (embeddings only, primary method) ---
    for category in ["URW", "CC"]:
        cat_subs = [s for s in subnarratives if s.startswith(f"{category}:")]
        cat_indices = [subnarratives.index(s) for s in cat_subs]
        cat_emb = emb_sim[np.ix_(cat_indices, cat_indices)]
        cat_cluster = cluster_labels(cat_emb, cat_subs)
        cat_name = "Ukraine-Russia War" if category == "URW" else "Climate Change"

        plot_similarity_heatmap(
            cat_emb, cat_subs,
            str(output_dir / f"subnarrative_similarity_{category.lower()}.png"),
            f"{cat_name} Subnarrative Similarity (Embeddings)",
        )
        plot_dendrogram(
            cat_cluster,
            str(output_dir / f"subnarrative_dendrogram_{category.lower()}.png"),
            f"{cat_name} Subnarrative Clustering (Embeddings)",
        )

    # --- Narrative-level similarity (embeddings) ---
    print("Computing narrative-level similarity...")
    narr_emb_sim = compute_embedding_similarity_matrix(narratives, all_defs, embedding_model)
    narr_cluster = cluster_labels(narr_emb_sim, narratives)

    plot_similarity_heatmap(
        narr_emb_sim, narratives,
        str(output_dir / "narrative_similarity_heatmap.png"),
        "Narrative Semantic Similarity (Embeddings)",
    )
    plot_dendrogram(
        narr_cluster,
        str(output_dir / "narrative_dendrogram.png"),
        "Narrative Hierarchical Clustering (Embeddings)",
    )

    # --- Report (with both methods) ---
    print("Generating report...")
    report = generate_hierarchy_report(
        tfidf_sim, subnarratives, all_defs, taxonomy,
        emb_sim_matrix=emb_sim,
        embedding_model=embedding_model,
    )
    report_path = output_dir / "semantic_hierarchy_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  Saved: {report_path}")

    # Save embedding similarity matrix as primary (used by confusion analysis)
    sim_data = {
        "labels": subnarratives,
        "similarity_matrix": emb_sim.tolist(),
        "method": "embedding",
        "model": embedding_model,
    }
    sim_path = output_dir / "subnarrative_similarity.json"
    with open(sim_path, "w", encoding="utf-8") as f:
        json.dump(sim_data, f, indent=2)
    print(f"  Saved: {sim_path}")

    # Also save TF-IDF for reference
    tfidf_data = {
        "labels": subnarratives,
        "similarity_matrix": tfidf_sim.tolist(),
        "method": "tfidf",
    }
    tfidf_path = output_dir / "subnarrative_similarity_tfidf.json"
    with open(tfidf_path, "w", encoding="utf-8") as f:
        json.dump(tfidf_data, f, indent=2)
    print(f"  Saved: {tfidf_path}")

    print("\nHierarchy analysis complete!")


def cmd_confusion(args):
    """Run full confusion analysis with severity classification."""
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    experiments_dir = Path(args.experiments_dir)

    print("Loading taxonomy and definitions...")
    taxonomy = load_taxonomy()
    narr_defs = load_definitions(NARRATIVE_DEFS_FILE)
    sub_defs = load_definitions(SUBNARRATIVE_DEFS_FILE)
    all_defs = {**narr_defs, **sub_defs}

    narratives, subnarratives = build_full_label_set(taxonomy)

    # Check for pre-computed similarity matrix
    sim_cache = output_dir.parent / "semantic_hierarchy" / "subnarrative_similarity.json"
    if sim_cache.exists():
        print(f"Loading cached similarity matrix from {sim_cache}")
        with open(sim_cache, "r", encoding="utf-8") as f:
            sim_data = json.load(f)
        sub_sim = np.array(sim_data["similarity_matrix"])
        sim_labels = sim_data["labels"]
    else:
        print("Computing subnarrative similarity matrix...")
        sub_sim = compute_similarity_matrix(subnarratives, all_defs, taxonomy)
        sim_labels = subnarratives

    # --- Collect predictions from experiments ---
    print(f"\nScanning experiments in {experiments_dir}...")

    all_confusions = []
    lang_results = defaultdict(lambda: {"confusions": [], "gold_sub": {}, "pred_sub": {}})
    overall_gold_sub = {}
    overall_pred_sub = {}

    experiment_filter = args.experiments.split(",") if args.experiments else None

    for exp_dir in sorted(experiments_dir.iterdir()):
        if not exp_dir.is_dir():
            continue
        exp_name = exp_dir.name

        if experiment_filter and not any(f in exp_name for f in experiment_filter):
            continue

        lang = extract_lang_from_experiment_id(exp_name)
        if not lang:
            continue

        results_path = find_best_run(exp_dir)
        if results_path is None:
            continue

        # Load predictions and gold
        gold = load_gold(lang)
        if not gold:
            continue
        pred = load_predictions(str(results_path))

        print(f"  {exp_name}: {len(pred)} predictions vs {len(gold)} gold")

        # Extract subnarrative-level data
        gold_sub = {fn: labels[1] for fn, labels in gold.items()}
        pred_sub = {fn: labels[1] for fn, labels in pred.items()}

        # Merge into per-language accumulators
        for fn in gold_sub:
            lang_results[lang]["gold_sub"][fn] = lang_results[lang]["gold_sub"].get(fn, set()) | gold_sub[fn]
        for fn in pred_sub:
            lang_results[lang]["pred_sub"][fn] = lang_results[lang]["pred_sub"].get(fn, set()) | pred_sub[fn]

        # Merge into overall
        for fn in gold_sub:
            overall_gold_sub[fn] = overall_gold_sub.get(fn, set()) | gold_sub[fn]
        for fn in pred_sub:
            overall_pred_sub[fn] = overall_pred_sub.get(fn, set()) | pred_sub[fn]

        # Classify confusions for this experiment
        common_files = set(gold_sub.keys()) & set(pred_sub.keys())
        for fn in common_files:
            for gl in gold_sub[fn]:
                for pl in pred_sub[fn]:
                    if gl == pl:
                        continue
                    severity, sim_score = classify_confusion_severity(
                        gl, pl, sub_sim, sim_labels
                    )
                    confusion_entry = {
                        "experiment": exp_name,
                        "language": lang,
                        "file": fn,
                        "gold": gl,
                        "pred": pl,
                        "severity": severity,
                        "similarity": sim_score,
                    }
                    all_confusions.append(confusion_entry)
                    lang_results[lang]["confusions"].append(confusion_entry)

    if not all_confusions:
        print("\nNo confusions found. Check that experiments directory contains results.")
        return

    # --- Per-language confusion matrices ---
    print("\nGenerating per-language confusion matrices...")
    for lang in LANGUAGES:
        if lang not in lang_results or not lang_results[lang]["gold_sub"]:
            continue

        gold_sub = lang_results[lang]["gold_sub"]
        pred_sub = lang_results[lang]["pred_sub"]
        matrix, labels = compute_multilabel_confusion(gold_sub, pred_sub)

        if matrix.size > 0:
            plot_confusion_matrix(
                matrix, labels,
                str(output_dir / f"subnarrative_confusion_{lang}.png"),
                f"Subnarrative Confusion Matrix - {lang}",
            )

    # --- Overall confusion matrix ---
    print("Generating overall confusion matrix...")
    matrix, labels = compute_multilabel_confusion(overall_gold_sub, overall_pred_sub)
    if matrix.size > 0:
        plot_confusion_matrix(
            matrix, labels,
            str(output_dir / f"subnarrative_confusion_overall.png"),
            "Subnarrative Confusion Matrix - All Languages",
        )

    # --- Severity distribution plot ---
    print("Generating severity plots...")
    severity_counts = Counter(c["severity"] for c in all_confusions if c["severity"] != "correct")
    sev_labels = ["same-narrative", "same-category", "cross-category", "hallucination"]
    colors = ["#2ecc71", "#f39c12", "#e74c3c", "#9b59b6"]

    if severity_counts:
        fig, axes = plt.subplots(1, 2, figsize=(16, 5))

        # Overall pie chart
        sev_values = [severity_counts.get(s, 0) for s in sev_labels]
        nonzero = [(l, v, c) for l, v, c in zip(sev_labels, sev_values, colors) if v > 0]
        if nonzero:
            axes[0].pie(
                [v for _, v, _ in nonzero],
                labels=[l for l, _, _ in nonzero],
                colors=[c for _, _, c in nonzero],
                autopct="%1.1f%%",
                startangle=90,
            )
        axes[0].set_title("Overall Confusion Severity", fontweight="bold")

        # Per-language stacked bar chart
        lang_data = {}
        for lang in LANGUAGES:
            if lang not in lang_results:
                continue
            lang_sev = Counter(c["severity"] for c in lang_results[lang]["confusions"]
                             if c["severity"] != "correct")
            if sum(lang_sev.values()) > 0:
                lang_data[lang] = lang_sev

        if lang_data:
            langs = sorted(lang_data.keys())
            x = np.arange(len(langs))
            width = 0.6
            bottom = np.zeros(len(langs))
            for sev, color in zip(sev_labels, colors):
                values = np.array([lang_data[l].get(sev, 0) for l in langs], dtype=float)
                axes[1].bar(x, values, width, bottom=bottom, label=sev, color=color)
                bottom += values
            axes[1].set_xlabel("Language")
            axes[1].set_ylabel("Count")
            axes[1].set_title("Confusion Severity by Language (Stacked)", fontweight="bold")
            axes[1].set_xticks(x)
            axes[1].set_xticklabels(langs)
            axes[1].legend(loc="upper right")

        plt.tight_layout()
        plt.savefig(str(output_dir / "confusion_severity_distribution.png"), dpi=200,
                    bbox_inches="tight")
        plt.close()
        print(f"  Saved: {output_dir / 'confusion_severity_distribution.png'}")

    # --- Generate report ---
    print("Generating confusion report...")
    report = generate_confusion_report(all_confusions, sub_sim, sim_labels, lang_results)
    report_path = output_dir / "confusion_severity_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  Saved: {report_path}")

    # Save raw confusions as JSON
    confusions_path = output_dir / "all_confusions.json"
    with open(confusions_path, "w", encoding="utf-8") as f:
        json.dump(all_confusions, f, indent=2)
    print(f"  Saved: {confusions_path}")

    total_non_correct = sum(1 for c in all_confusions if c["severity"] != "correct")
    print(f"\nConfusion analysis complete! {total_non_correct} confusions classified.")
    severity_counts = Counter(c["severity"] for c in all_confusions if c["severity"] != "correct")
    for sev in ["same-narrative", "same-category", "cross-category", "hallucination"]:
        cnt = severity_counts.get(sev, 0)
        pct = cnt / total_non_correct * 100 if total_non_correct else 0
        print(f"  {sev}: {cnt} ({pct:.1f}%)")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Semantic similarity hierarchy and confusion severity analysis"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # hierarchy subcommand
    hier_parser = subparsers.add_parser(
        "hierarchy", help="Build semantic similarity hierarchy"
    )
    hier_parser.add_argument(
        "--output-dir", type=str,
        default="../../results/analysis/semantic_hierarchy/",
        help="Output directory for hierarchy analysis"
    )
    hier_parser.add_argument(
        "--embedding-model", type=str,
        default="all-MiniLM-L6-v2",
        help="Sentence-transformers model for embeddings (default: all-MiniLM-L6-v2)"
    )

    # confusion subcommand
    conf_parser = subparsers.add_parser(
        "confusion", help="Run confusion severity analysis"
    )
    conf_parser.add_argument(
        "--experiments-dir", type=str,
        default="../../results/experiments/",
        help="Directory containing experiment results"
    )
    conf_parser.add_argument(
        "--output-dir", type=str,
        default="../../results/analysis/confusion/",
        help="Output directory for confusion analysis"
    )
    conf_parser.add_argument(
        "--experiments", type=str, default=None,
        help="Comma-separated experiment name filters (e.g., 'deepseek,mistral')"
    )

    args = parser.parse_args()

    if args.command == "hierarchy":
        cmd_hierarchy(args)
    elif args.command == "confusion":
        cmd_confusion(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

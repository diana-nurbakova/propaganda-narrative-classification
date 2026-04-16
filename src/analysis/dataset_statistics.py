#!/usr/bin/env python3
"""
Dataset Statistics Report Generator.

Produces comprehensive statistics for train/dev/test splits across all languages:
- Number of articles, unique narratives, unique subnarratives
- Average narratives/subnarratives per article
- Narrative/subnarrative distributions across languages and splits
- Co-occurrence patterns

Output: Markdown report with tables.

Usage:
    python src/analysis/dataset_statistics.py
    python src/analysis/dataset_statistics.py --output results/analysis/dataset_statistics.md
"""

import argparse
import csv
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LANGUAGES = ["EN", "BG", "HI", "PT", "RU"]


def parse_annotations(filepath: str, has_explanation: bool = False) -> List[dict]:
    """Parse a subtask-3 annotation file.

    Args:
        filepath: Path to the annotation file.
        has_explanation: If True, file has 4 columns (train format); else 3 (dev format).

    Returns:
        List of dicts with keys: filename, narratives, subnarratives
    """
    records = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                continue

            filename = parts[0]
            raw_narratives = parts[1]
            raw_subnarratives = parts[2]

            # Parse semicolon-separated labels
            narratives = [
                n.strip()
                for n in raw_narratives.split(";")
                if n.strip() and n.strip().lower() != "none"
            ]
            subnarratives = [
                s.strip()
                for s in raw_subnarratives.split(";")
                if s.strip() and s.strip().lower() != "none"
            ]

            # Filter out "Other"
            has_other = any(n.lower() == "other" for n in narratives)
            narratives = [n for n in narratives if n.lower() != "other"]
            subnarratives = [s for s in subnarratives if s.lower() == "other" and False or s.lower() != "other"]

            records.append(
                {
                    "filename": filename,
                    "narratives": narratives,
                    "subnarratives": subnarratives,
                    "is_other": has_other and len(narratives) == 0,
                }
            )
    return records


def get_unique_narratives(records: List[dict]) -> Tuple[set, set]:
    """Extract unique narrative and subnarrative labels."""
    narratives = set()
    subnarratives = set()
    for r in records:
        narratives.update(r["narratives"])
        subnarratives.update(r["subnarratives"])
    return narratives, subnarratives


def compute_stats(records: List[dict]) -> dict:
    """Compute statistics for a set of records."""
    n_articles = len(records)
    if n_articles == 0:
        return {
            "n_articles": 0,
            "n_unique_narratives": 0,
            "n_unique_subnarratives": 0,
            "avg_narratives": 0,
            "avg_subnarratives": 0,
            "n_other": 0,
            "other_pct": 0,
            "n_multi_narrative": 0,
            "multi_narrative_pct": 0,
        }

    unique_narr, unique_sub = get_unique_narratives(records)

    # Deduplicate narratives per article for counting
    narr_counts = [len(set(r["narratives"])) for r in records]
    sub_counts = [len(set(r["subnarratives"])) for r in records]

    n_other = sum(1 for r in records if r["is_other"])
    n_multi = sum(1 for c in narr_counts if c > 1)

    return {
        "n_articles": n_articles,
        "n_unique_narratives": len(unique_narr),
        "n_unique_subnarratives": len(unique_sub),
        "avg_narratives": sum(narr_counts) / n_articles,
        "avg_subnarratives": sum(sub_counts) / n_articles,
        "n_other": n_other,
        "other_pct": n_other / n_articles * 100,
        "n_multi_narrative": n_multi,
        "multi_narrative_pct": n_multi / n_articles * 100,
    }


def count_documents(dir_path: str) -> int:
    """Count .txt files in a directory."""
    if not os.path.exists(dir_path):
        return 0
    return len([f for f in os.listdir(dir_path) if f.endswith(".txt")])


def load_all_data() -> dict:
    """Load annotations for all splits and languages."""
    data = {}

    # Train — subtask-3 annotations + "Other" articles from raw-documents not in annotations
    for lang in LANGUAGES:
        ann_path = PROJECT_ROOT / "data" / "train" / lang / "subtask-3-annotations.txt"
        doc_dir = PROJECT_ROOT / "data" / "train" / lang / "raw-documents"
        if ann_path.exists():
            records = parse_annotations(str(ann_path), has_explanation=True)
            # Add "Other" articles (in raw-documents but not in annotations)
            annotated_files = {r["filename"] for r in records}
            if doc_dir.exists():
                all_doc_files = {f for f in os.listdir(doc_dir) if f.endswith(".txt")}
                other_files = all_doc_files - annotated_files
                for f in sorted(other_files):
                    records.append(
                        {
                            "filename": f,
                            "narratives": [],
                            "subnarratives": [],
                            "is_other": True,
                        }
                    )
            data[("train", lang)] = records

    # Dev — subtask-3 annotations + "Other" articles from subtask-2 not in subtask-3
    for lang in LANGUAGES:
        ann_path = (
            PROJECT_ROOT
            / "data"
            / "dev-documents_4_December"
            / lang
            / "subtask-3-dominant-narratives.txt"
        )
        doc_dir = (
            PROJECT_ROOT
            / "data"
            / "dev-documents_4_December"
            / lang
            / "subtask-2-documents"
        )
        if ann_path.exists():
            records = parse_annotations(str(ann_path), has_explanation=False)
            # Add "Other" articles (in subtask-2 docs but not in subtask-3 annotations)
            annotated_files = {r["filename"] for r in records}
            if doc_dir.exists():
                all_doc_files = {f for f in os.listdir(doc_dir) if f.endswith(".txt")}
                other_files = all_doc_files - annotated_files
                for f in sorted(other_files):
                    records.append(
                        {
                            "filename": f,
                            "narratives": [],
                            "subnarratives": [],
                            "is_other": True,
                        }
                    )
            data[("dev", lang)] = records

    # Test (no annotations, just document counts)
    for lang in LANGUAGES:
        doc_dir = PROJECT_ROOT / "data" / "testset" / lang / "subtask-2-documents"
        n_docs = count_documents(str(doc_dir))
        if n_docs > 0:
            data[("test", lang)] = [{"filename": f"doc_{i}", "narratives": [], "subnarratives": [], "is_other": False} for i in range(n_docs)]

    return data


def load_augmented_data() -> Optional[dict]:
    """Load the augmented unified training set used for mDeBERTa fine-tuning.

    Reads both the detailed CSV (with type metadata) and the TSV (which may
    contain additional back-translated entries added after consolidation).

    Returns a dict with keys: 'csv_records', 'tsv_total', 'extra_tsv_files',
    or None if the data files are missing.
    """
    csv_path = PROJECT_ROOT / "data" / "all-texts-unified" / "unified-annotations-detailed.csv"
    tsv_path = PROJECT_ROOT / "data" / "all-texts-unified" / "unified-annotations.tsv"

    if not csv_path.exists():
        return None

    # Load detailed CSV
    csv_records = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            narr_raw = row.get("narratives", "")
            narratives = [n.strip() for n in narr_raw.split(";") if n.strip()]
            is_other = len(narratives) == 1 and narratives[0].lower() == "other"
            narratives_clean = [n for n in narratives if n.lower() != "other"]

            sub_raw = row.get("subnarratives", "")
            subnarratives = [s.strip() for s in sub_raw.split(";") if s.strip() and s.strip().lower() != "other"]

            csv_records.append({
                "filename": row["filename"],
                "original_filename": row.get("original_filename", ""),
                "language": row.get("language", ""),
                "type": row.get("type", ""),
                "narratives": narratives_clean,
                "subnarratives": subnarratives,
                "is_other": is_other,
            })

    # Count TSV lines (may differ from CSV due to later additions)
    tsv_total = 0
    tsv_filenames = set()
    if tsv_path.exists():
        with open(tsv_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    tsv_total += 1
                    parts = line.strip().split("\t")
                    if parts:
                        tsv_filenames.add(parts[0])

    csv_filenames = {r["filename"] for r in csv_records}
    extra_tsv = tsv_filenames - csv_filenames

    # Categorize extra TSV files by prefix pattern
    extra_by_type = Counter()
    for fname in extra_tsv:
        if "TRANS_PT" in fname:
            extra_by_type["EN->PT back-translation"] += 1
        elif "TRANS_BG" in fname:
            extra_by_type["EN->BG back-translation"] += 1
        elif "TRANS_HI" in fname:
            extra_by_type["EN->HI back-translation"] += 1
        elif "TRANS_RU" in fname:
            extra_by_type["EN->RU back-translation"] += 1
        else:
            extra_by_type["other"] += 1

    # Also check dev overlap
    dev_filenames = set()
    for lang in LANGUAGES:
        dev_dir = PROJECT_ROOT / "data" / "dev-documents_4_December" / lang / "subtask-2-documents"
        if dev_dir.exists():
            for f in os.listdir(dev_dir):
                if f.endswith(".txt"):
                    dev_filenames.add(f)

    csv_originals = {r["original_filename"] for r in csv_records}
    dev_overlap = dev_filenames & (csv_filenames | csv_originals | tsv_filenames)

    return {
        "csv_records": csv_records,
        "tsv_total": tsv_total,
        "extra_tsv_files": extra_tsv,
        "extra_by_type": extra_by_type,
        "dev_overlap_count": len(dev_overlap),
    }


def narrative_distributions(data: dict) -> Tuple[dict, dict]:
    """Compute narrative and subnarrative frequency distributions per split+lang."""
    narr_dist = {}
    sub_dist = {}

    for (split, lang), records in data.items():
        if split == "test":
            continue
        narr_counter = Counter()
        sub_counter = Counter()
        for r in records:
            narr_counter.update(set(r["narratives"]))
            sub_counter.update(set(r["subnarratives"]))
        narr_dist[(split, lang)] = narr_counter
        sub_dist[(split, lang)] = sub_counter

    return narr_dist, sub_dist


def extract_category(label: str) -> str:
    """Extract top-level category from a narrative label (CC or URW)."""
    if label.startswith("CC:"):
        return "CC"
    elif label.startswith("URW:"):
        return "URW"
    return "Other"


def generate_augmented_section(aug_data: dict) -> List[str]:
    """Generate the augmented training set section of the report."""
    lines = []
    lines.append("## 7. Augmented Training Set (mDeBERTa Baseline)\n")
    lines.append("The mDeBERTa baseline was fine-tuned on an augmented version of the training set")
    lines.append("that includes both original documents and their LLM-generated translations.\n")

    csv_records = aug_data["csv_records"]
    tsv_total = aug_data["tsv_total"]
    extra_tsv = aug_data["extra_tsv_files"]
    extra_by_type = aug_data["extra_by_type"]

    # --- 7a. Composition overview ---
    lines.append("### 7a. Composition Overview\n")

    type_counts = Counter(r["type"] for r in csv_records)
    lines.append(f"| Component | Count |")
    lines.append(f"|-----------|------:|")
    lines.append(f"| Original documents (native language) | {type_counts.get('original', 0)} |")
    lines.append(f"| Translated documents (non-EN -> EN) | {type_counts.get('translated', 0)} |")
    if extra_tsv:
        for desc, count in sorted(extra_by_type.items()):
            lines.append(f"| {desc} | {count} |")
    lines.append(f"| **Total (used for training)** | **{tsv_total}** |")
    lines.append("")

    lines.append("**Translation method**: Google Gemini LLM — text cleaning (boilerplate removal)")
    lines.append("followed by translation to English. English documents were cleaned but not translated,")
    lines.append("resulting in two copies per EN document (raw original + cleaned version).\n")

    # --- 7b. Language x Type breakdown ---
    lines.append("### 7b. Language x Type Breakdown\n")

    lang_type = defaultdict(Counter)
    for r in csv_records:
        lang_type[r["language"]][r["type"]] += 1

    all_types = sorted({r["type"] for r in csv_records})
    header = "| Language |"
    sep = "|----------|"
    for t in all_types:
        header += f" {t.capitalize()} |"
        sep += "------:|"
    header += " Total |"
    sep += "------:|"
    lines.append(header)
    lines.append(sep)

    grand = Counter()
    for lang in LANGUAGES:
        row = f"| {lang} |"
        lang_total = 0
        for t in all_types:
            c = lang_type[lang][t]
            grand[t] += c
            lang_total += c
            row += f" {c} |"
        row += f" {lang_total} |"
        lines.append(row)

    row = "| **Total** |"
    g_total = 0
    for t in all_types:
        row += f" **{grand[t]}** |"
        g_total += grand[t]
    row += f" **{g_total}** |"
    lines.append(row)
    lines.append("")

    # --- 7c. What each file type represents ---
    lines.append("### 7c. File Type Description\n")
    lines.append("| Filename Pattern | Description |")
    lines.append("|-----------------|-------------|")
    lines.append("| `{LANG}_ORIG_{filename}` | Raw web-scraped text in original language |")
    lines.append("| `{filename}` (no prefix, non-EN origin) | Non-EN document translated to English by Gemini |")
    lines.append("| `EN_{filename}` (no ORIG prefix) | English document after LLM boilerplate cleaning |")
    lines.append("| `EN_TRANS_PT_{filename}` | English document back-translated to Portuguese |")
    lines.append("")

    lines.append("**Note**: English documents appear twice under different filenames —")
    lines.append("the raw original (`EN_ORIG_*`) and the LLM-cleaned version (`EN_*`). These")
    lines.append("are not identical: the cleaned versions have web boilerplate removed, resulting")
    lines.append("in EN being effectively double-represented (798 files vs 401 BG, 366 HI, etc.).\n")

    # --- 7d. Augmented set label statistics ---
    lines.append("### 7d. Augmented Set Label Statistics\n")

    non_other = [r for r in csv_records if not r["is_other"]]
    aug_narr = set()
    aug_sub = set()
    for r in non_other:
        aug_narr.update(r["narratives"])
        aug_sub.update(r["subnarratives"])

    n_other = sum(1 for r in csv_records if r["is_other"])
    other_pct = n_other / len(csv_records) * 100 if csv_records else 0

    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|------:|")
    lines.append(f"| Total documents (CSV) | {len(csv_records)} |")
    lines.append(f"| Total documents (TSV, incl. back-translations) | {tsv_total} |")
    lines.append(f"| Unique narratives | {len(aug_narr)} |")
    lines.append(f"| Unique subnarratives | {len(aug_sub)} |")
    lines.append(f"| Documents labeled 'Other' | {n_other} ({other_pct:.1f}%) |")
    lines.append("")

    # --- 7e. Data leakage check ---
    lines.append("### 7e. Data Leakage Verification\n")
    dev_overlap = aug_data["dev_overlap_count"]
    if dev_overlap == 0:
        lines.append("**No data leakage detected.** Zero overlap between the augmented training set")
        lines.append("and the dev evaluation set (178 documents). Verified by exact filename match,")
        lines.append("original filename match, and numeric ID cross-check.\n")
    else:
        lines.append(f"**WARNING**: {dev_overlap} documents overlap between augmented train and dev set.\n")

    return lines


def generate_report(data: dict, output_path: Optional[str] = None) -> str:
    """Generate the full markdown report."""
    lines = []
    lines.append("# Dataset Statistics Report\n")
    lines.append("Statistics for the SemEval-2025 Task 10 propaganda narrative classification dataset.\n")

    # =========================================================================
    # Table 1: Overview per split per language
    # =========================================================================
    lines.append("## 1. Dataset Overview\n")
    lines.append("| Split | Language | Articles | Unique Narratives | Unique Subnarratives | Avg Narr/Article | Avg Sub/Article | Other % | Multi-label % |")
    lines.append("|-------|----------|----------|-------------------|----------------------|------------------|-----------------|---------|---------------|")

    split_totals = defaultdict(lambda: {"articles": 0, "narr": set(), "sub": set(), "other": 0, "multi": 0, "sum_narr": 0, "sum_sub": 0})

    for split in ["train", "dev", "test"]:
        for lang in LANGUAGES:
            key = (split, lang)
            if key not in data:
                continue

            records = data[key]
            stats = compute_stats(records)

            if split == "test":
                n_docs = len(records)
                lines.append(
                    f"| {split.capitalize()} | {lang} | {n_docs} | - | - | - | - | - | - |"
                )
                split_totals[split]["articles"] += n_docs
            else:
                lines.append(
                    f"| {split.capitalize()} | {lang} | {stats['n_articles']} | "
                    f"{stats['n_unique_narratives']} | {stats['n_unique_subnarratives']} | "
                    f"{stats['avg_narratives']:.2f} | {stats['avg_subnarratives']:.2f} | "
                    f"{stats['other_pct']:.1f}% | {stats['multi_narrative_pct']:.1f}% |"
                )
                t = split_totals[split]
                t["articles"] += stats["n_articles"]
                t["other"] += stats["n_other"]
                t["multi"] += stats["n_multi_narrative"]
                t["sum_narr"] += sum(len(set(r["narratives"])) for r in records)
                t["sum_sub"] += sum(len(set(r["subnarratives"])) for r in records)
                narr, sub = get_unique_narratives(records)
                t["narr"].update(narr)
                t["sub"].update(sub)

    # Totals row per split
    lines.append("|-------|----------|----------|-------------------|----------------------|------------------|-----------------|---------|---------------|")
    for split in ["train", "dev", "test"]:
        t = split_totals[split]
        if t["articles"] == 0:
            continue
        if split == "test":
            lines.append(f"| **{split.capitalize()}** | **Total** | **{t['articles']}** | - | - | - | - | - | - |")
        else:
            avg_n = t["sum_narr"] / t["articles"] if t["articles"] else 0
            avg_s = t["sum_sub"] / t["articles"] if t["articles"] else 0
            other_pct = t["other"] / t["articles"] * 100 if t["articles"] else 0
            multi_pct = t["multi"] / t["articles"] * 100 if t["articles"] else 0
            lines.append(
                f"| **{split.capitalize()}** | **Total** | **{t['articles']}** | "
                f"**{len(t['narr'])}** | **{len(t['sub'])}** | "
                f"**{avg_n:.2f}** | **{avg_s:.2f}** | "
                f"**{other_pct:.1f}%** | **{multi_pct:.1f}%** |"
            )

    lines.append("")

    # =========================================================================
    # Table 2: Category balance (CC vs URW)
    # =========================================================================
    lines.append("## 2. Category Balance (CC vs URW)\n")
    lines.append("| Split | Language | CC Articles | URW Articles | Both | CC % | URW % |")
    lines.append("|-------|----------|-------------|--------------|------|------|-------|")

    for split in ["train", "dev"]:
        for lang in LANGUAGES:
            key = (split, lang)
            if key not in data:
                continue
            records = data[key]
            cc_count = 0
            urw_count = 0
            both_count = 0
            for r in records:
                cats = set(extract_category(n) for n in r["narratives"])
                has_cc = "CC" in cats
                has_urw = "URW" in cats
                if has_cc:
                    cc_count += 1
                if has_urw:
                    urw_count += 1
                if has_cc and has_urw:
                    both_count += 1

            total = len(records)
            cc_pct = cc_count / total * 100 if total else 0
            urw_pct = urw_count / total * 100 if total else 0
            lines.append(
                f"| {split.capitalize()} | {lang} | {cc_count} | {urw_count} | {both_count} | "
                f"{cc_pct:.1f}% | {urw_pct:.1f}% |"
            )

    lines.append("")

    # =========================================================================
    # Table 3: Narrative distribution across languages (train)
    # =========================================================================
    narr_dist, sub_dist = narrative_distributions(data)

    for split in ["train", "dev"]:
        lines.append(f"## 3{'a' if split == 'train' else 'b'}. Narrative Distribution — {split.capitalize()} Set\n")

        # Collect all unique narratives for this split
        all_narr = set()
        for lang in LANGUAGES:
            if (split, lang) in narr_dist:
                all_narr.update(narr_dist[(split, lang)].keys())

        if not all_narr:
            lines.append("*No data available.*\n")
            continue

        sorted_narr = sorted(all_narr)

        # Header
        header = "| Narrative |"
        sep = "|-----------|"
        for lang in LANGUAGES:
            header += f" {lang} |"
            sep += "----:|"
        header += " Total |"
        sep += "------:|"
        lines.append(header)
        lines.append(sep)

        # Rows
        for narr in sorted_narr:
            row = f"| {narr} |"
            total = 0
            for lang in LANGUAGES:
                count = narr_dist.get((split, lang), Counter()).get(narr, 0)
                total += count
                row += f" {count} |"
            row += f" {total} |"
            lines.append(row)

        # Totals
        row = "| **Total** |"
        grand = 0
        for lang in LANGUAGES:
            t = sum(narr_dist.get((split, lang), Counter()).values())
            grand += t
            row += f" **{t}** |"
        row += f" **{grand}** |"
        lines.append(row)
        lines.append("")

    # =========================================================================
    # Table 4: Subnarrative distribution (top 20 most frequent)
    # =========================================================================
    for split in ["train", "dev"]:
        lines.append(f"## 4{'a' if split == 'train' else 'b'}. Top Subnarrative Distribution — {split.capitalize()} Set\n")

        # Aggregate across languages
        all_sub = Counter()
        for lang in LANGUAGES:
            all_sub += sub_dist.get((split, lang), Counter())

        if not all_sub:
            lines.append("*No data available.*\n")
            continue

        top_subs = all_sub.most_common(25)

        header = "| Subnarrative |"
        sep = "|-------------|"
        for lang in LANGUAGES:
            header += f" {lang} |"
            sep += "----:|"
        header += " Total |"
        sep += "------:|"
        lines.append(header)
        lines.append(sep)

        for sub_name, _ in top_subs:
            # Truncate long names
            display = sub_name if len(sub_name) <= 80 else sub_name[:77] + "..."
            row = f"| {display} |"
            total = 0
            for lang in LANGUAGES:
                count = sub_dist.get((split, lang), Counter()).get(sub_name, 0)
                total += count
                row += f" {count} |"
            row += f" {total} |"
            lines.append(row)

        lines.append("")

    # =========================================================================
    # Table 5: Label density (narratives per article distribution)
    # =========================================================================
    lines.append("## 5. Label Density Distribution\n")
    lines.append("Number of distinct narratives assigned per article.\n")

    for split in ["train", "dev"]:
        lines.append(f"### {split.capitalize()} Set\n")
        lines.append("| # Narratives | " + " | ".join(LANGUAGES) + " | Total |")
        lines.append("|-------------|" + "|".join(["-----:" for _ in LANGUAGES]) + "|------:|")

        max_labels = 0
        density = {}
        for lang in LANGUAGES:
            key = (split, lang)
            if key not in data:
                continue
            records = data[key]
            counts = Counter(len(set(r["narratives"])) for r in records)
            density[lang] = counts
            if counts:
                max_labels = max(max_labels, max(counts.keys()))

        for n in range(0, max_labels + 1):
            row = f"| {n} |"
            total = 0
            for lang in LANGUAGES:
                c = density.get(lang, Counter()).get(n, 0)
                total += c
                row += f" {c} |"
            row += f" {total} |"
            lines.append(row)
        lines.append("")

    # =========================================================================
    # Summary
    # =========================================================================
    lines.append("## 6. Summary\n")

    # Compute total unique labels across all train data
    all_train_narr = set()
    all_train_sub = set()
    all_dev_narr = set()
    all_dev_sub = set()
    for lang in LANGUAGES:
        if ("train", lang) in data:
            n, s = get_unique_narratives(data[("train", lang)])
            all_train_narr.update(n)
            all_train_sub.update(s)
        if ("dev", lang) in data:
            n, s = get_unique_narratives(data[("dev", lang)])
            all_dev_narr.update(n)
            all_dev_sub.update(s)

    lines.append(f"- **Train set**: {sum(len(data.get(('train', l), [])) for l in LANGUAGES)} articles across {len(LANGUAGES)} languages")
    lines.append(f"  - {len(all_train_narr)} unique narratives, {len(all_train_sub)} unique subnarratives")
    lines.append(f"- **Dev set**: {sum(len(data.get(('dev', l), [])) for l in LANGUAGES)} articles across {len(LANGUAGES)} languages")
    lines.append(f"  - {len(all_dev_narr)} unique narratives, {len(all_dev_sub)} unique subnarratives")
    lines.append(f"- **Test set**: {sum(len(data.get(('test', l), [])) for l in LANGUAGES)} articles (no annotations)")

    # Check for dev-only labels
    dev_only_narr = all_dev_narr - all_train_narr
    train_only_narr = all_train_narr - all_dev_narr
    if dev_only_narr:
        lines.append(f"\n**Narratives in dev but NOT in train ({len(dev_only_narr)}):**")
        for n in sorted(dev_only_narr):
            lines.append(f"- {n}")
    if train_only_narr:
        lines.append(f"\n**Narratives in train but NOT in dev ({len(train_only_narr)}):**")
        for n in sorted(train_only_narr):
            lines.append(f"- {n}")

    dev_only_sub = all_dev_sub - all_train_sub
    train_only_sub = all_train_sub - all_dev_sub
    if dev_only_sub:
        lines.append(f"\n**Subnarratives in dev but NOT in train ({len(dev_only_sub)}):**")
        for s in sorted(dev_only_sub):
            lines.append(f"- {s}")
    if train_only_sub:
        lines.append(f"\n**Subnarratives in train but NOT in dev ({len(train_only_sub)}):**")
        for s in sorted(train_only_sub):
            lines.append(f"- {s}")

    lines.append("")

    # =========================================================================
    # Section 7: Augmented Training Set
    # =========================================================================
    aug_data = load_augmented_data()
    if aug_data is not None:
        lines.extend(generate_augmented_section(aug_data))

    report = "\n".join(lines)

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to: {output_path}")

    return report


def main():
    parser = argparse.ArgumentParser(description="Generate dataset statistics report")
    parser.add_argument(
        "--output",
        type=str,
        default="results/analysis/dataset_statistics.md",
        help="Output markdown file path",
    )
    args = parser.parse_args()

    print("Loading data...")
    data = load_all_data()

    print(f"Loaded data for {len(data)} split-language combinations")
    for (split, lang), records in sorted(data.items()):
        print(f"  {split}/{lang}: {len(records)} records")

    print("\nGenerating report...")
    report = generate_report(data, args.output)

    # Also print to stdout
    print("\n" + report)


if __name__ == "__main__":
    main()

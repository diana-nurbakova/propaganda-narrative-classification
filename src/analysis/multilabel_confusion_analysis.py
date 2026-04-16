#!/usr/bin/env python3
"""
Multi-label Confusion Analysis for Narratives and Sub-narratives.
Shows which labels are confused with which at both levels.
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from collections import defaultdict
from typing import Dict, Set, Tuple, List, Optional


def parse_annotation_line(line: str) -> Tuple[Optional[str], Set[str], Set[str]]:
    """
    Parse a single annotation line to extract filename, narrative labels, and subnarrative labels.

    Format: filename<TAB>narrative1;narrative2<TAB>subnarrative1;subnarrative2

    Returns:
        Tuple of (filename, set of narratives, set of subnarratives)
    """
    parts = line.strip().split('\t')
    if len(parts) < 2:
        return None, set(), set()

    filename = parts[0]

    # Extract narrative labels (column 2)
    narratives = set()
    if len(parts) > 1 and parts[1] and parts[1].lower() not in ('none', 'other'):
        for label in parts[1].split(';'):
            label = label.strip()
            if label and label.lower() not in ('none',):
                narratives.add(label)
    if not narratives and len(parts) > 1:
        if parts[1].lower() == 'other':
            narratives.add('Other')

    # Extract subnarrative labels (column 3)
    subnarratives = set()
    if len(parts) > 2 and parts[2] and parts[2].lower() not in ('none', 'other'):
        for label in parts[2].split(';'):
            label = label.strip()
            if label and label.lower() not in ('none',):
                subnarratives.add(label)
    if not subnarratives and len(parts) > 2:
        if parts[2].lower() == 'other':
            subnarratives.add('Other')

    return filename, narratives, subnarratives


def load_annotations(filepath: str) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """
    Load annotations from file.

    Returns:
        Tuple of (narrative_annotations, subnarrative_annotations)
        Each is a dict mapping filename to set of labels
    """
    narrative_annotations = {}
    subnarrative_annotations = {}

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            filename, narratives, subnarratives = parse_annotation_line(line)
            if filename:
                narrative_annotations[filename] = narratives
                subnarrative_annotations[filename] = subnarratives

    return narrative_annotations, subnarrative_annotations


def create_confusion_matrix(
    ground_truth: Dict[str, Set[str]],
    predictions: Dict[str, Set[str]]
) -> Tuple[np.ndarray, List[str]]:
    """
    Create confusion matrix for multi-label classification.
    confusion[i][j] = count where true label i appears and predicted label j appears
    """
    # Get all unique labels
    all_labels = sorted(set.union(
        set([label for labels in ground_truth.values() for label in labels]),
        set([label for labels in predictions.values() for label in labels])
    ))

    if not all_labels:
        return np.zeros((0, 0), dtype=int), []

    # Create label to index mapping
    label_to_idx = {label: idx for idx, label in enumerate(all_labels)}
    n_labels = len(all_labels)

    # Initialize confusion matrix
    confusion = np.zeros((n_labels, n_labels), dtype=int)

    # Fill confusion matrix
    for filename in ground_truth:
        if filename not in predictions:
            continue

        true_labels = ground_truth[filename]
        pred_labels = predictions[filename]

        # For each true label, count which predicted labels co-occur
        for true_label in true_labels:
            true_idx = label_to_idx[true_label]
            for pred_label in pred_labels:
                pred_idx = label_to_idx[pred_label]
                confusion[true_idx][pred_idx] += 1

    return confusion, all_labels


def compute_label_metrics(
    ground_truth: Dict[str, Set[str]],
    predictions: Dict[str, Set[str]],
    all_labels: List[str]
) -> Dict[str, Dict]:
    """Compute per-label precision, recall, F1 metrics."""
    metrics = {}

    for label in all_labels:
        tp = fp = fn = 0

        for filename in set(ground_truth.keys()) | set(predictions.keys()):
            true_labels = ground_truth.get(filename, set())
            pred_labels = predictions.get(filename, set())

            is_true = label in true_labels
            is_pred = label in pred_labels

            if is_true and is_pred:
                tp += 1
            elif not is_true and is_pred:
                fp += 1
            elif is_true and not is_pred:
                fn += 1

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        metrics[label] = {
            'tp': tp,
            'fp': fp,
            'fn': fn,
            'total_true': tp + fn,
            'total_pred': tp + fp,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }

    return metrics


def plot_confusion_heatmap(
    confusion_matrix: np.ndarray,
    labels: List[str],
    output_path: str,
    title_prefix: str = "Narrative"
):
    """Plot confusion heatmap - both raw counts and normalized."""
    if confusion_matrix.size == 0:
        print(f"Warning: Empty confusion matrix, skipping plot for {title_prefix}")
        return

    # Normalize by row (true labels) to show percentages
    row_sums = confusion_matrix.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1  # Avoid division by zero
    normalized_confusion = (confusion_matrix / row_sums * 100).astype(float)

    # Determine figure size based on number of labels
    n_labels = len(labels)
    fig_width = max(16, n_labels * 0.5)
    fig_height = max(12, n_labels * 0.4)

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(fig_width * 2, fig_height))

    # Shorten labels for display
    display_labels = [l[:50] + "..." if len(l) > 50 else l for l in labels]

    # Plot 1: Raw counts
    sns.heatmap(confusion_matrix,
                xticklabels=display_labels,
                yticklabels=display_labels,
                annot=n_labels <= 20,
                fmt='d',
                cmap='YlOrRd',
                ax=ax1,
                square=False,
                cbar_kws={'label': 'Count'})
    ax1.set_title(f'{title_prefix} Confusion Matrix (Raw Counts)\nRows: True Labels, Columns: Predicted Labels',
                  fontsize=14, fontweight='bold', pad=20)
    ax1.set_xlabel('Predicted Labels', fontsize=12, fontweight='bold')
    ax1.set_ylabel('True Labels', fontsize=12, fontweight='bold')
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right', fontsize=8)
    plt.setp(ax1.get_yticklabels(), rotation=0, fontsize=8)

    # Plot 2: Normalized percentages
    sns.heatmap(normalized_confusion,
                xticklabels=display_labels,
                yticklabels=display_labels,
                annot=n_labels <= 20,
                fmt='.1f',
                cmap='YlOrRd',
                ax=ax2,
                square=False,
                cbar_kws={'label': 'Percentage (%)'})
    ax2.set_title(f'{title_prefix} Confusion Matrix (Normalized %)\nShows % of times predicted label appears when true label is present',
                  fontsize=14, fontweight='bold', pad=20)
    ax2.set_xlabel('Predicted Labels', fontsize=12, fontweight='bold')
    ax2.set_ylabel('True Labels', fontsize=12, fontweight='bold')
    plt.setp(ax2.get_xticklabels(), rotation=45, ha='right', fontsize=8)
    plt.setp(ax2.get_yticklabels(), rotation=0, fontsize=8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"[OK] Saved {title_prefix.lower()} confusion heatmap to: {output_path}")


def generate_confusion_report(
    ground_truth: Dict[str, Set[str]],
    predictions: Dict[str, Set[str]],
    confusion_matrix: np.ndarray,
    labels: List[str],
    level_name: str = "Narrative"
) -> str:
    """Generate markdown report for confusion analysis."""
    report = f"# {level_name} Confusion Analysis Report\n\n"

    # Compute label metrics
    metrics = compute_label_metrics(ground_truth, predictions, labels)

    # Label-wise performance table
    report += f"## {level_name} Label-wise Performance Statistics\n\n"
    report += "| Label | True Positives | False Positives | False Negatives | Total True | Total Predicted | Precision | Recall | F1 |\n"
    report += "|-------|----------------|-----------------|-----------------|------------|-----------------|-----------|--------|----|\n"

    # Sort by F1 score descending
    sorted_labels = sorted(labels, key=lambda l: metrics[l]['f1'], reverse=True)

    for label in sorted_labels:
        m = metrics[label]
        display_label = label[:60] + "..." if len(label) > 60 else label
        report += f"| {display_label} | {m['tp']} | {m['fp']} | {m['fn']} | {m['total_true']} | {m['total_pred']} | {m['precision']:.3f} | {m['recall']:.3f} | {m['f1']:.3f} |\n"

    # Confusion patterns
    report += f"\n## Most Common {level_name} Confusion Patterns\n\n"
    report += "Shows cases where a true label is present but a different label is predicted.\n\n"
    report += "| Rank | True Label | Wrongly Predicted Label | Count | Description |\n"
    report += "|------|------------|------------------------|-------|-------------|\n"

    # Extract off-diagonal elements
    confusion_pairs = []
    for i, true_label in enumerate(labels):
        for j, pred_label in enumerate(labels):
            if i != j and confusion_matrix[i][j] > 0:
                confusion_pairs.append((true_label, pred_label, confusion_matrix[i][j]))

    # Sort by count descending
    confusion_pairs.sort(key=lambda x: x[2], reverse=True)

    for rank, (true_label, pred_label, count) in enumerate(confusion_pairs[:20], 1):
        true_display = true_label[:40] + "..." if len(true_label) > 40 else true_label
        pred_display = pred_label[:40] + "..." if len(pred_label) > 40 else pred_label
        report += f"| {rank} | {true_display} | {pred_display} | {count} | Model predicted '{pred_display}' when '{true_display}' was true |\n"

    # Label-specific confusion
    report += f"\n## {level_name} Label-Specific Confusion Analysis\n\n"

    for label in sorted_labels[:15]:  # Top 15 by F1
        label_idx = labels.index(label)
        confusions = []

        for j, pred_label in enumerate(labels):
            if j != label_idx and confusion_matrix[label_idx][j] > 0:
                confusions.append((pred_label, confusion_matrix[label_idx][j]))

        if confusions:
            confusions.sort(key=lambda x: x[1], reverse=True)
            display_label = label[:60] + "..." if len(label) > 60 else label
            report += f"\n### {display_label}\n\n"
            report += f"When **{display_label}** is the true label, it is often confused with:\n\n"

            for pred_label, count in confusions[:5]:
                pred_display = pred_label[:50] + "..." if len(pred_label) > 50 else pred_label
                report += f"- **{pred_display}**: {count} times\n"

    return report


def analyze_level(
    gt_annotations: Dict[str, Set[str]],
    pred_annotations: Dict[str, Set[str]],
    output_dir: str,
    level_name: str,
    filter_prefix: Optional[str] = None
):
    """Perform complete analysis for a single level (narrative or subnarrative)."""
    # Find common files
    common_files = set(gt_annotations.keys()) & set(pred_annotations.keys())
    if len(common_files) == 0:
        print(f"Warning: No common files for {level_name} analysis")
        return

    # Filter to common files
    gt_filtered = {k: v for k, v in gt_annotations.items() if k in common_files}
    pred_filtered = {k: v for k, v in pred_annotations.items() if k in common_files}

    print(f"\n{'='*60}")
    print(f"{level_name.upper()} ANALYSIS")
    print(f"{'='*60}")
    print(f"Files analyzed: {len(common_files)}")

    # Create confusion matrix
    confusion_matrix, labels = create_confusion_matrix(gt_filtered, pred_filtered)

    if len(labels) == 0:
        print(f"Warning: No labels found for {level_name} analysis")
        return

    # Filter labels if requested
    if filter_prefix:
        keep_indices = []
        filtered_labels = []
        for i, label in enumerate(labels):
            if label.startswith(filter_prefix) or label == 'Other':
                keep_indices.append(i)
                filtered_labels.append(label)

        if keep_indices:
            confusion_matrix = confusion_matrix[np.ix_(keep_indices, keep_indices)]
            labels = filtered_labels
            print(f"Filtered to {len(labels)} labels with prefix '{filter_prefix}'")

    print(f"Unique {level_name.lower()} labels: {len(labels)}")

    # Generate heatmap
    filename_suffix = f"_{filter_prefix.lower()}" if filter_prefix else ""
    heatmap_path = os.path.join(output_dir, f"{level_name.lower()}_confusion_heatmap{filename_suffix}.png")
    plot_confusion_heatmap(confusion_matrix, labels, heatmap_path, level_name)

    # Generate report
    report = generate_confusion_report(gt_filtered, pred_filtered, confusion_matrix, labels, level_name)
    report_path = os.path.join(output_dir, f"{level_name.lower()}_confusion_report{filename_suffix}.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"[OK] Saved {level_name.lower()} report to: {report_path}")

    # Print summary
    print(f"\nTop 10 {level_name} labels by F1 score:")
    metrics = compute_label_metrics(gt_filtered, pred_filtered, labels)
    sorted_labels = sorted(labels, key=lambda l: metrics[l]['f1'], reverse=True)
    for i, label in enumerate(sorted_labels[:10], 1):
        m = metrics[label]
        display = label[:50] + "..." if len(label) > 50 else label
        print(f"  {i:2d}. {display}: F1={m['f1']:.3f}, P={m['precision']:.3f}, R={m['recall']:.3f}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate narrative and sub-narrative confusion analysis"
    )
    parser.add_argument("--ground_truth", type=str, required=True,
                       help="Ground truth annotations file")
    parser.add_argument("--predictions", type=str, required=True,
                       help="Predictions file")
    parser.add_argument("--output_dir", type=str, default="confusion_analysis",
                       help="Output directory for analysis")
    parser.add_argument("--level", type=str, default="both",
                       choices=["narrative", "subnarrative", "both"],
                       help="Which level(s) to analyze (default: both)")
    parser.add_argument("--filter_prefix", type=str, default=None,
                       help="Filter to only show labels with this prefix (e.g., 'CC', 'URW')")

    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    print("Loading annotations...")
    gt_narratives, gt_subnarratives = load_annotations(args.ground_truth)
    pred_narratives, pred_subnarratives = load_annotations(args.predictions)

    print(f"[OK] Loaded {len(gt_narratives)} ground truth samples")
    print(f"[OK] Loaded {len(pred_narratives)} predictions")

    # Analyze narratives
    if args.level in ("narrative", "both"):
        analyze_level(
            gt_narratives, pred_narratives,
            args.output_dir, "Narrative",
            args.filter_prefix
        )

    # Analyze subnarratives
    if args.level in ("subnarrative", "both"):
        analyze_level(
            gt_subnarratives, pred_subnarratives,
            args.output_dir, "Subnarrative",
            args.filter_prefix
        )

    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE!")
    print(f"{'='*60}")
    print(f"Results saved to: {args.output_dir}")


if __name__ == "__main__":
    main()

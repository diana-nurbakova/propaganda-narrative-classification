"""
Scorer for hierarchical text classification.

Calculates F1-samples for multi-label narrative/subnarrative classification.

Usage:
    python src/analysis/scorer.py --gold gold.txt --pred predictions.txt
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple


def parse_labels_file(filepath: str) -> Dict[str, Tuple[Set[str], Set[str]]]:
    """
    Parse a labels file in the format:
    file_id<TAB>narrative1;narrative2<TAB>subnarrative1;subnarrative2

    Returns:
        Dictionary mapping file_id to (set of narratives, set of subnarratives)
    """
    labels = {}

    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            parts = line.split('\t')
            if len(parts) < 2:
                print(f"Warning: Skipping malformed line {line_num}: {line[:50]}...")
                continue

            file_id = parts[0].strip()

            # Parse narratives (column 2)
            narratives_str = parts[1].strip() if len(parts) > 1 else ""
            narratives = set()
            if narratives_str and narratives_str.lower() != 'none' and narratives_str.lower() != 'other':
                for n in narratives_str.split(';'):
                    n = n.strip()
                    if n and n.lower() != 'none' and n.lower() != 'other':
                        narratives.add(n)

            # Parse subnarratives (column 3)
            subnarratives_str = parts[2].strip() if len(parts) > 2 else ""
            subnarratives = set()
            if subnarratives_str and subnarratives_str.lower() != 'none' and subnarratives_str.lower() != 'other':
                for s in subnarratives_str.split(';'):
                    s = s.strip()
                    if s and s.lower() != 'none' and s.lower() != 'other':
                        subnarratives.add(s)

            labels[file_id] = (narratives, subnarratives)

    return labels


def compute_f1_samples(
    gold: Dict[str, Tuple[Set[str], Set[str]]],
    pred: Dict[str, Tuple[Set[str], Set[str]]],
    level: str = 'both'
) -> Dict[str, float]:
    """
    Compute sample-based F1 score for multi-label classification.

    F1-samples = (1/n) * sum_i(2 * |Y_i ∩ Ŷ_i| / (|Y_i| + |Ŷ_i|))

    Args:
        gold: Gold labels
        pred: Predicted labels
        level: 'narrative', 'subnarrative', or 'both'

    Returns:
        Dictionary with precision, recall, f1 for specified level
    """
    total_f1 = 0.0
    total_precision = 0.0
    total_recall = 0.0
    n_samples = 0

    # Combine both label sets from gold
    all_file_ids = set(gold.keys())

    for file_id in all_file_ids:
        gold_narratives, gold_subnarratives = gold.get(file_id, (set(), set()))
        pred_narratives, pred_subnarratives = pred.get(file_id, (set(), set()))

        # Select labels based on level
        if level == 'narrative':
            gold_labels = gold_narratives
            pred_labels = pred_narratives
        elif level == 'subnarrative':
            gold_labels = gold_subnarratives
            pred_labels = pred_subnarratives
        else:  # 'both' - combine narratives and subnarratives
            gold_labels = gold_narratives | gold_subnarratives
            pred_labels = pred_narratives | pred_subnarratives

        # Compute metrics for this sample
        intersection = len(gold_labels & pred_labels)
        gold_size = len(gold_labels)
        pred_size = len(pred_labels)

        # Precision for this sample
        if pred_size > 0:
            sample_precision = intersection / pred_size
        else:
            sample_precision = 1.0 if gold_size == 0 else 0.0

        # Recall for this sample
        if gold_size > 0:
            sample_recall = intersection / gold_size
        else:
            sample_recall = 1.0 if pred_size == 0 else 0.0

        # F1 for this sample
        if sample_precision + sample_recall > 0:
            sample_f1 = 2 * sample_precision * sample_recall / (sample_precision + sample_recall)
        else:
            sample_f1 = 0.0

        total_precision += sample_precision
        total_recall += sample_recall
        total_f1 += sample_f1
        n_samples += 1

    # Average across samples
    if n_samples > 0:
        avg_precision = total_precision / n_samples
        avg_recall = total_recall / n_samples
        avg_f1 = total_f1 / n_samples
    else:
        avg_precision = 0.0
        avg_recall = 0.0
        avg_f1 = 0.0

    return {
        'precision': avg_precision,
        'recall': avg_recall,
        'f1': avg_f1,
        'n_samples': n_samples,
    }


def compute_exact_match(
    gold: Dict[str, Tuple[Set[str], Set[str]]],
    pred: Dict[str, Tuple[Set[str], Set[str]]],
) -> float:
    """Compute exact match accuracy (both narrative and subnarrative must match)."""
    correct = 0
    total = len(gold)

    for file_id in gold:
        gold_n, gold_s = gold.get(file_id, (set(), set()))
        pred_n, pred_s = pred.get(file_id, (set(), set()))

        if gold_n == pred_n and gold_s == pred_s:
            correct += 1

    return correct / total if total > 0 else 0.0


def main():
    parser = argparse.ArgumentParser(
        description="Score hierarchical text classification predictions"
    )
    parser.add_argument(
        '--gold',
        type=str,
        required=True,
        help='Path to gold labels file'
    )
    parser.add_argument(
        '--pred',
        type=str,
        required=True,
        help='Path to predictions file'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Path to save JSON results (optional)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print detailed per-sample results'
    )

    args = parser.parse_args()

    # Validate files exist
    if not Path(args.gold).exists():
        print(f"Error: Gold file not found: {args.gold}")
        return 1

    if not Path(args.pred).exists():
        print(f"Error: Predictions file not found: {args.pred}")
        return 1

    # Parse files
    gold = parse_labels_file(args.gold)
    pred = parse_labels_file(args.pred)

    print(f"Gold labels: {len(gold)} documents")
    print(f"Predictions: {len(pred)} documents")

    # Check for missing predictions
    missing = set(gold.keys()) - set(pred.keys())
    if missing:
        print(f"Warning: {len(missing)} documents have no predictions")
        if args.verbose:
            for fid in list(missing)[:5]:
                print(f"  - {fid}")

    # Compute metrics
    results = {
        'narrative': compute_f1_samples(gold, pred, 'narrative'),
        'subnarrative': compute_f1_samples(gold, pred, 'subnarrative'),
        'combined': compute_f1_samples(gold, pred, 'both'),
        'exact_match': compute_exact_match(gold, pred),
    }

    # Print results
    print("\n" + "="*60)
    print("EVALUATION RESULTS")
    print("="*60)

    print("\nNarrative-level:")
    print(f"  Precision: {results['narrative']['precision']:.4f}")
    print(f"  Recall:    {results['narrative']['recall']:.4f}")
    print(f"  F1:        {results['narrative']['f1']:.4f}")

    print("\nSubnarrative-level:")
    print(f"  Precision: {results['subnarrative']['precision']:.4f}")
    print(f"  Recall:    {results['subnarrative']['recall']:.4f}")
    print(f"  F1:        {results['subnarrative']['f1']:.4f}")

    print("\nCombined (Narrative + Subnarrative):")
    print(f"  Precision: {results['combined']['precision']:.4f}")
    print(f"  Recall:    {results['combined']['recall']:.4f}")
    print(f"  F1:        {results['combined']['f1']:.4f}")

    print(f"\nExact Match Accuracy: {results['exact_match']:.4f}")

    print("="*60)

    # Output for programmatic use (F1-samples is the main metric)
    print(f"\nf1_samples: {results['combined']['f1']:.4f}")

    # Save results if requested
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")

    return 0


if __name__ == "__main__":
    exit(main())

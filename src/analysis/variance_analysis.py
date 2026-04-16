"""
Single-Agent Variance Analysis.

Analyzes variance in single-agent predictions vs ensemble predictions,
measuring variance reduction and agent agreement metrics.
"""

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


def load_predictions(results_path: str) -> Dict[str, Tuple[Set[str], Set[str]]]:
    """
    Load predictions from a results file.

    Args:
        results_path: Path to results.txt file

    Returns:
        Dictionary mapping file_id to (narratives_set, subnarratives_set)
    """
    predictions = {}

    with open(results_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split('\t')
            file_id = parts[0]

            narratives = set()
            subnarratives = set()

            if len(parts) > 1 and parts[1]:
                narratives = set(n.strip() for n in parts[1].split(';') if n.strip())
            if len(parts) > 2 and parts[2]:
                subnarratives = set(s.strip() for s in parts[2].split(';') if s.strip())

            predictions[file_id] = (narratives, subnarratives)

    return predictions


def load_multi_run_predictions(experiment_dir: str) -> List[Dict[str, Tuple[Set[str], Set[str]]]]:
    """
    Load predictions from all runs in a multi-run experiment.

    Args:
        experiment_dir: Path to experiment directory containing run_N/results.txt

    Returns:
        List of prediction dictionaries (one per run)
    """
    exp_path = Path(experiment_dir)
    all_predictions = []

    # Find all run directories
    run_dirs = sorted(exp_path.glob("run_*"))

    for run_dir in run_dirs:
        results_file = run_dir / "results.txt"
        if results_file.exists():
            predictions = load_predictions(str(results_file))
            all_predictions.append(predictions)
            print(f"Loaded {len(predictions)} predictions from {results_file}")

    return all_predictions


def compute_agreement_rate(predictions_list: List[Dict[str, Tuple[Set[str], Set[str]]]]) -> Dict[str, float]:
    """
    Compute agreement rate between agents/runs.

    Agreement rate = proportion of labels that are consistent across all runs.

    Args:
        predictions_list: List of prediction dictionaries from different runs

    Returns:
        Dictionary with agreement metrics
    """
    if len(predictions_list) < 2:
        return {'error': 'Need at least 2 runs for agreement analysis'}

    # Check for empty predictions
    if not predictions_list[0]:
        return {'error': 'Empty predictions in first run'}

    # Get common documents
    all_docs = set(predictions_list[0].keys())
    for preds in predictions_list[1:]:
        all_docs &= set(preds.keys())

    if not all_docs:
        return {'error': 'No common documents across runs'}

    # Compute agreement for narratives and subnarratives
    narrative_agreements = []
    subnarrative_agreements = []

    for doc_id in all_docs:
        # Get all narrative sets for this document
        doc_narratives = [preds[doc_id][0] for preds in predictions_list]
        doc_subnarratives = [preds[doc_id][1] for preds in predictions_list]

        # Compute pairwise Jaccard similarity
        n_pairs = 0
        narr_sim_sum = 0
        sub_sim_sum = 0

        for i in range(len(predictions_list)):
            for j in range(i + 1, len(predictions_list)):
                # Narratives
                set_i, set_j = doc_narratives[i], doc_narratives[j]
                if set_i or set_j:  # At least one non-empty
                    intersection = len(set_i & set_j)
                    union = len(set_i | set_j)
                    narr_sim_sum += intersection / union if union > 0 else 1.0
                else:
                    narr_sim_sum += 1.0  # Both empty = perfect agreement

                # Subnarratives
                set_i, set_j = doc_subnarratives[i], doc_subnarratives[j]
                if set_i or set_j:
                    intersection = len(set_i & set_j)
                    union = len(set_i | set_j)
                    sub_sim_sum += intersection / union if union > 0 else 1.0
                else:
                    sub_sim_sum += 1.0

                n_pairs += 1

        narrative_agreements.append(narr_sim_sum / n_pairs)
        subnarrative_agreements.append(sub_sim_sum / n_pairs)

    return {
        'num_documents': len(all_docs),
        'num_runs': len(predictions_list),
        'narrative_agreement': {
            'mean': float(np.mean(narrative_agreements)),
            'std': float(np.std(narrative_agreements)),
            'min': float(np.min(narrative_agreements)),
            'max': float(np.max(narrative_agreements)),
        },
        'subnarrative_agreement': {
            'mean': float(np.mean(subnarrative_agreements)),
            'std': float(np.std(subnarrative_agreements)),
            'min': float(np.min(subnarrative_agreements)),
            'max': float(np.max(subnarrative_agreements)),
        },
    }


def compute_label_variance(predictions_list: List[Dict[str, Tuple[Set[str], Set[str]]]]) -> Dict[str, Any]:
    """
    Compute variance in label predictions across runs.

    Args:
        predictions_list: List of prediction dictionaries from different runs

    Returns:
        Dictionary with variance metrics for each label
    """
    # Count label occurrences across all runs
    narrative_counts = Counter()
    subnarrative_counts = Counter()
    doc_narrative_counts = {}  # {doc_id: {label: count}}
    doc_subnarrative_counts = {}

    n_runs = len(predictions_list)

    for preds in predictions_list:
        for doc_id, (narratives, subnarratives) in preds.items():
            if doc_id not in doc_narrative_counts:
                doc_narrative_counts[doc_id] = Counter()
                doc_subnarrative_counts[doc_id] = Counter()

            for narr in narratives:
                narrative_counts[narr] += 1
                doc_narrative_counts[doc_id][narr] += 1

            for sub in subnarratives:
                subnarrative_counts[sub] += 1
                doc_subnarrative_counts[doc_id][sub] += 1

    # Compute per-label stability (how consistently a label appears)
    label_stability = {}

    for label, total_count in narrative_counts.most_common():
        # For each document where this label appeared, compute consistency
        appearances = []
        for doc_id, counts in doc_narrative_counts.items():
            if label in counts:
                # Fraction of runs where this label appeared for this doc
                appearances.append(counts[label] / n_runs)

        if appearances:
            label_stability[label] = {
                'total_appearances': total_count,
                'mean_consistency': float(np.mean(appearances)),
                'std_consistency': float(np.std(appearances)),
                'type': 'narrative',
            }

    for label, total_count in subnarrative_counts.most_common():
        appearances = []
        for doc_id, counts in doc_subnarrative_counts.items():
            if label in counts:
                appearances.append(counts[label] / n_runs)

        if appearances:
            label_stability[label] = {
                'total_appearances': total_count,
                'mean_consistency': float(np.mean(appearances)),
                'std_consistency': float(np.std(appearances)),
                'type': 'subnarrative',
            }

    return {
        'num_runs': n_runs,
        'total_unique_narratives': len(narrative_counts),
        'total_unique_subnarratives': len(subnarrative_counts),
        'label_stability': label_stability,
    }


def compute_variance_reduction(
    single_agent_predictions: List[Dict[str, Tuple[Set[str], Set[str]]]],
    ensemble_predictions: Dict[str, Tuple[Set[str], Set[str]]],
) -> Dict[str, Any]:
    """
    Compute variance reduction achieved by ensemble over single agent.

    Args:
        single_agent_predictions: List of single-agent prediction dicts
        ensemble_predictions: Ensemble (aggregated) predictions

    Returns:
        Dictionary with variance reduction metrics
    """
    common_docs = set(ensemble_predictions.keys())
    for preds in single_agent_predictions:
        common_docs &= set(preds.keys())

    if not common_docs:
        return {'error': 'No common documents'}

    # Compute variance for single agent predictions
    single_narrative_vars = []
    single_subnarrative_vars = []

    for doc_id in common_docs:
        # Get all predictions for this doc
        doc_narratives = [preds[doc_id][0] for preds in single_agent_predictions]
        doc_subnarratives = [preds[doc_id][1] for preds in single_agent_predictions]

        # Compute set size variance
        narr_sizes = [len(s) for s in doc_narratives]
        sub_sizes = [len(s) for s in doc_subnarratives]

        single_narrative_vars.append(np.var(narr_sizes))
        single_subnarrative_vars.append(np.var(sub_sizes))

    # Compute ensemble set sizes (should be constant)
    ensemble_narrative_sizes = [len(ensemble_predictions[doc][0]) for doc in common_docs]
    ensemble_subnarrative_sizes = [len(ensemble_predictions[doc][1]) for doc in common_docs]

    return {
        'num_documents': len(common_docs),
        'single_agent': {
            'narrative_set_size_var': float(np.mean(single_narrative_vars)),
            'subnarrative_set_size_var': float(np.mean(single_subnarrative_vars)),
        },
        'ensemble': {
            'narrative_set_size_mean': float(np.mean(ensemble_narrative_sizes)),
            'subnarrative_set_size_mean': float(np.mean(ensemble_subnarrative_sizes)),
        },
        'variance_reduction': {
            'narrative': float(np.mean(single_narrative_vars)) if np.mean(single_narrative_vars) > 0 else 0,
            'subnarrative': float(np.mean(single_subnarrative_vars)) if np.mean(single_subnarrative_vars) > 0 else 0,
        },
    }


def compute_fleiss_kappa(predictions_list: List[Dict[str, Tuple[Set[str], Set[str]]]]) -> Dict[str, float]:
    """
    Compute Fleiss' Kappa for inter-annotator agreement.

    For multi-label classification, we treat each label as a binary decision.

    Args:
        predictions_list: List of prediction dictionaries from different runs

    Returns:
        Dictionary with Fleiss' Kappa values
    """
    if len(predictions_list) < 2:
        return {'error': 'Need at least 2 runs for Fleiss Kappa'}

    # Check for empty predictions
    if not predictions_list[0]:
        return {'error': 'Empty predictions in first run'}

    # Get all unique labels
    all_narratives = set()
    all_subnarratives = set()
    common_docs = set(predictions_list[0].keys())

    for preds in predictions_list:
        common_docs &= set(preds.keys())
        for doc_id, (narratives, subnarratives) in preds.items():
            all_narratives.update(narratives)
            all_subnarratives.update(subnarratives)

    if not common_docs:
        return {'error': 'No common documents'}

    n_raters = len(predictions_list)
    n_docs = len(common_docs)

    def compute_kappa(label_set: Set[str], label_type: int) -> float:
        """Compute Fleiss' Kappa for a set of labels."""
        if not label_set:
            return 1.0  # Perfect agreement on empty

        # Create rating matrix: docs x labels
        # Each cell = number of raters who assigned that label
        n_labels = len(label_set)
        labels_list = sorted(label_set)
        label_to_idx = {l: i for i, l in enumerate(labels_list)}

        # For each doc and label, count how many raters assigned it
        ratings = np.zeros((n_docs, n_labels * 2))  # *2 for yes/no

        for doc_idx, doc_id in enumerate(sorted(common_docs)):
            for rater_preds in predictions_list:
                doc_labels = rater_preds[doc_id][label_type]
                for label in labels_list:
                    label_idx = label_to_idx[label]
                    if label in doc_labels:
                        ratings[doc_idx, label_idx * 2] += 1  # yes
                    else:
                        ratings[doc_idx, label_idx * 2 + 1] += 1  # no

        # Compute Fleiss' Kappa
        # P_i = proportion of agreeing pairs for item i
        # P_bar = mean of P_i
        # P_e = expected agreement by chance

        n_categories = n_labels * 2
        P_i = np.zeros(n_docs)

        for i in range(n_docs):
            sum_sq = np.sum(ratings[i, :] ** 2)
            P_i[i] = (sum_sq - n_raters) / (n_raters * (n_raters - 1)) if n_raters > 1 else 1

        P_bar = np.mean(P_i)

        # P_e: for each category, compute proportion across all ratings
        p_j = np.sum(ratings, axis=0) / (n_docs * n_raters)
        P_e = np.sum(p_j ** 2)

        # Kappa
        if P_e == 1:
            return 1.0
        kappa = (P_bar - P_e) / (1 - P_e)

        return float(kappa)

    return {
        'narrative_kappa': compute_kappa(all_narratives, 0),
        'subnarrative_kappa': compute_kappa(all_subnarratives, 1),
        'num_raters': n_raters,
        'num_documents': n_docs,
        'num_narrative_labels': len(all_narratives),
        'num_subnarrative_labels': len(all_subnarratives),
    }


def plot_agreement_distribution(
    predictions_list: List[Dict[str, Tuple[Set[str], Set[str]]]],
    output_path: Optional[str] = None,
) -> None:
    """
    Plot distribution of agreement scores across documents.
    """
    if not MATPLOTLIB_AVAILABLE:
        print("matplotlib not available for plotting")
        return

    # Check for empty predictions
    if not predictions_list or not predictions_list[0]:
        print("Warning: No predictions available for plotting")
        return

    # Compute per-document agreement
    common_docs = set(predictions_list[0].keys())
    for preds in predictions_list[1:]:
        common_docs &= set(preds.keys())

    narrative_agreements = []
    subnarrative_agreements = []

    for doc_id in common_docs:
        doc_narratives = [preds[doc_id][0] for preds in predictions_list]
        doc_subnarratives = [preds[doc_id][1] for preds in predictions_list]

        # Compute Jaccard for this document (average pairwise)
        n_pairs = 0
        narr_sim = 0
        sub_sim = 0

        for i in range(len(predictions_list)):
            for j in range(i + 1, len(predictions_list)):
                set_i, set_j = doc_narratives[i], doc_narratives[j]
                if set_i or set_j:
                    narr_sim += len(set_i & set_j) / len(set_i | set_j)
                else:
                    narr_sim += 1.0

                set_i, set_j = doc_subnarratives[i], doc_subnarratives[j]
                if set_i or set_j:
                    sub_sim += len(set_i & set_j) / len(set_i | set_j)
                else:
                    sub_sim += 1.0

                n_pairs += 1

        narrative_agreements.append(narr_sim / n_pairs)
        subnarrative_agreements.append(sub_sim / n_pairs)

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].hist(narrative_agreements, bins=20, edgecolor='black', alpha=0.7)
    axes[0].axvline(np.mean(narrative_agreements), color='r', linestyle='--',
                    label=f'Mean: {np.mean(narrative_agreements):.3f}')
    axes[0].set_xlabel('Jaccard Agreement')
    axes[0].set_ylabel('Number of Documents')
    axes[0].set_title('Narrative Agreement Distribution')
    axes[0].legend()

    axes[1].hist(subnarrative_agreements, bins=20, edgecolor='black', alpha=0.7)
    axes[1].axvline(np.mean(subnarrative_agreements), color='r', linestyle='--',
                    label=f'Mean: {np.mean(subnarrative_agreements):.3f}')
    axes[1].set_xlabel('Jaccard Agreement')
    axes[1].set_ylabel('Number of Documents')
    axes[1].set_title('Subnarrative Agreement Distribution')
    axes[1].legend()

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Saved plot to {output_path}")
    else:
        plt.show()


def run_variance_analysis(
    experiment_dir: str,
    output_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run comprehensive variance analysis on a multi-run experiment.

    Args:
        experiment_dir: Path to experiment directory
        output_path: Optional path to save results JSON

    Returns:
        Dictionary with all variance analysis results
    """
    print(f"Loading predictions from {experiment_dir}...")
    predictions_list = load_multi_run_predictions(experiment_dir)

    if len(predictions_list) < 2:
        return {'error': f'Need at least 2 runs, found {len(predictions_list)}'}

    print(f"Loaded {len(predictions_list)} runs")

    results = {
        'experiment_dir': experiment_dir,
        'num_runs': len(predictions_list),
    }

    print("Computing agreement rate...")
    results['agreement'] = compute_agreement_rate(predictions_list)

    print("Computing label variance...")
    results['label_variance'] = compute_label_variance(predictions_list)

    print("Computing Fleiss' Kappa...")
    results['fleiss_kappa'] = compute_fleiss_kappa(predictions_list)

    # Summary statistics
    results['summary'] = {
        'single_agent_std_narrative': results['agreement']['narrative_agreement']['std'],
        'single_agent_std_subnarrative': results['agreement']['subnarrative_agreement']['std'],
        'mean_agreement_narrative': results['agreement']['narrative_agreement']['mean'],
        'mean_agreement_subnarrative': results['agreement']['subnarrative_agreement']['mean'],
        'fleiss_kappa_narrative': results['fleiss_kappa'].get('narrative_kappa'),
        'fleiss_kappa_subnarrative': results['fleiss_kappa'].get('subnarrative_kappa'),
    }

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"Saved results to {output_path}")

    return results


def main():
    """Command-line interface for variance analysis."""
    parser = argparse.ArgumentParser(
        description="Analyze variance in single-agent vs ensemble predictions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        '--experiment-dir',
        type=str,
        required=True,
        help='Directory containing multi-run experiment results'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Path to save analysis results JSON'
    )
    parser.add_argument(
        '--plot',
        type=str,
        default=None,
        help='Path to save agreement distribution plot'
    )

    args = parser.parse_args()

    # Run analysis
    results = run_variance_analysis(
        experiment_dir=args.experiment_dir,
        output_path=args.output,
    )

    # Print summary
    print("\n" + "=" * 60)
    print("VARIANCE ANALYSIS SUMMARY")
    print("=" * 60)

    if 'summary' in results:
        print(f"Number of runs: {results['num_runs']}")
        print(f"\nAgreement (Jaccard similarity):")
        print(f"  Narratives: {results['summary']['mean_agreement_narrative']:.3f} ± {results['summary']['single_agent_std_narrative']:.3f}")
        print(f"  Subnarratives: {results['summary']['mean_agreement_subnarrative']:.3f} ± {results['summary']['single_agent_std_subnarrative']:.3f}")
        print(f"\nFleiss' Kappa:")
        print(f"  Narratives: {results['summary']['fleiss_kappa_narrative']:.3f}")
        print(f"  Subnarratives: {results['summary']['fleiss_kappa_subnarrative']:.3f}")

    # Generate plot if requested
    if args.plot:
        predictions_list = load_multi_run_predictions(args.experiment_dir)
        plot_agreement_distribution(predictions_list, args.plot)

    return 0


if __name__ == "__main__":
    exit(main())

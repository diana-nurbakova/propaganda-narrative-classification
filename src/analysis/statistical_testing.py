#!/usr/bin/env python3
"""
Statistical significance testing for multi-run experiments.

Implements bootstrap confidence intervals and paired statistical tests
for comparing classification methods.

Usage:
    # Compare two methods
    python statistical_testing.py compare \\
        --method-a-dir results/experiments/agora_gpt5nano_en \\
        --method-a-name "Agora" \\
        --method-b-dir results/experiments/baseline_gpt5nano_en \\
        --method-b-name "Baseline" \\
        --ground-truth data/EN/subtask-3-annotations.txt \\
        --output results/analysis/agora_vs_baseline.json

    # Multi-method comparison
    python statistical_testing.py multi \\
        --experiments \\
            "Agora:results/experiments/agora_gpt5nano_en" \\
            "Actor-Critic:results/experiments/actor_critic_gpt5nano_en" \\
            "Baseline:results/experiments/baseline_gpt5nano_en" \\
        --ground-truth data/EN/subtask-3-annotations.txt \\
        --output results/analysis/full_comparison.json
"""

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from scipy import stats
from sklearn.metrics import f1_score
from sklearn.preprocessing import MultiLabelBinarizer


def parse_labels(label_string: str) -> List[str]:
    """Parse semicolon-separated labels into a list."""
    if label_string.strip() == "Other":
        return ["Other"]
    return [label.strip() for label in label_string.split(";") if label.strip()]


def load_annotations(annotation_file: str) -> Dict[str, Dict[str, List[str]]]:
    """Load ground truth annotations from file."""
    annotations = {}
    with open(annotation_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) >= 3:
                filename = parts[0]
                narratives = parse_labels(parts[1])
                subnarratives = parse_labels(parts[2])
                annotations[filename] = {
                    'narratives': narratives,
                    'subnarratives': subnarratives
                }
    return annotations


def load_predictions(prediction_file: str) -> Dict[str, Dict[str, List[str]]]:
    """Load predictions from file."""
    predictions = {}
    with open(prediction_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) >= 3:
                filename = parts[0]
                narratives = parse_labels(parts[1])
                subnarratives = parse_labels(parts[2])
                predictions[filename] = {
                    'narratives': narratives,
                    'subnarratives': subnarratives
                }
    return predictions


def compute_f1_scores(
    y_true: List[List[str]],
    y_pred: List[List[str]],
) -> Dict[str, float]:
    """
    Compute F1 macro, micro, and samples scores.

    Args:
        y_true: List of ground truth label sets
        y_pred: List of predicted label sets

    Returns:
        Dictionary with f1_macro, f1_micro, f1_samples
    """
    # Collect all labels
    all_labels = set()
    for labels in y_true + y_pred:
        all_labels.update(labels)

    mlb = MultiLabelBinarizer()
    mlb.fit([list(all_labels)])

    y_true_bin = mlb.transform(y_true)
    y_pred_bin = mlb.transform(y_pred)

    return {
        'f1_macro': float(f1_score(y_true_bin, y_pred_bin, average='macro', zero_division=0)),
        'f1_micro': float(f1_score(y_true_bin, y_pred_bin, average='micro', zero_division=0)),
        'f1_samples': float(f1_score(y_true_bin, y_pred_bin, average='samples', zero_division=0)),
    }


def evaluate_single_run(
    prediction_file: str,
    ground_truth: Dict[str, Dict[str, List[str]]],
) -> Optional[Dict[str, Dict[str, float]]]:
    """
    Evaluate a single run against ground truth.

    Args:
        prediction_file: Path to predictions file
        ground_truth: Ground truth annotations

    Returns:
        Dictionary with metrics for narratives and subnarratives, or None if failed
    """
    if not os.path.exists(prediction_file):
        print(f"Warning: Prediction file not found: {prediction_file}")
        return None

    predictions = load_predictions(prediction_file)

    # Find common files
    common_files = set(ground_truth.keys()) & set(predictions.keys())
    if not common_files:
        print(f"Warning: No common files found for {prediction_file}")
        return None

    # Extract labels for common files
    y_true_narratives = [ground_truth[f]['narratives'] for f in common_files]
    y_pred_narratives = [predictions[f]['narratives'] for f in common_files]
    y_true_subnarratives = [ground_truth[f]['subnarratives'] for f in common_files]
    y_pred_subnarratives = [predictions[f]['subnarratives'] for f in common_files]

    return {
        'narratives': compute_f1_scores(y_true_narratives, y_pred_narratives),
        'subnarratives': compute_f1_scores(y_true_subnarratives, y_pred_subnarratives),
        'n_files': len(common_files),
    }


def load_experiment_results(
    experiment_dir: str,
    ground_truth_file: str,
) -> Dict[str, List[float]]:
    """
    Load and evaluate all runs of an experiment.

    Args:
        experiment_dir: Directory containing experiment results
        ground_truth_file: Path to ground truth annotations

    Returns:
        Dictionary mapping metric names to lists of scores per run
    """
    manifest_path = os.path.join(experiment_dir, 'experiment_manifest.json')
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"Experiment manifest not found: {manifest_path}")

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    # Load ground truth once
    ground_truth = load_annotations(ground_truth_file)

    # Initialize metrics containers
    metrics = {
        'narratives_f1_macro': [],
        'narratives_f1_micro': [],
        'narratives_f1_samples': [],
        'subnarratives_f1_macro': [],
        'subnarratives_f1_micro': [],
        'subnarratives_f1_samples': [],
    }

    # Evaluate each successful run
    for run in manifest['runs']:
        if run.get('status') != 'success':
            print(f"Skipping failed run {run.get('run_id')}")
            continue

        output_file = run.get('output_file')
        if not output_file:
            continue

        result = evaluate_single_run(output_file, ground_truth)
        if result is None:
            continue

        # Collect metrics
        metrics['narratives_f1_macro'].append(result['narratives']['f1_macro'])
        metrics['narratives_f1_micro'].append(result['narratives']['f1_micro'])
        metrics['narratives_f1_samples'].append(result['narratives']['f1_samples'])
        metrics['subnarratives_f1_macro'].append(result['subnarratives']['f1_macro'])
        metrics['subnarratives_f1_micro'].append(result['subnarratives']['f1_micro'])
        metrics['subnarratives_f1_samples'].append(result['subnarratives']['f1_samples'])

    return metrics


def bootstrap_confidence_interval(
    scores: List[float],
    confidence: float = 0.95,
    n_bootstrap: int = 10000,
    random_state: Optional[int] = 42,
) -> Tuple[float, float, float]:
    """
    Compute bootstrap confidence interval.

    Args:
        scores: List of scores
        confidence: Confidence level (default: 0.95 for 95% CI)
        n_bootstrap: Number of bootstrap resamples
        random_state: Random seed for reproducibility

    Returns:
        Tuple of (mean, lower_bound, upper_bound)
    """
    if len(scores) == 0:
        return (0.0, 0.0, 0.0)

    scores = np.array(scores)
    n = len(scores)

    if random_state is not None:
        np.random.seed(random_state)

    # Bootstrap resampling
    bootstrap_means = []
    for _ in range(n_bootstrap):
        resample_idx = np.random.choice(n, size=n, replace=True)
        resample = scores[resample_idx]
        bootstrap_means.append(np.mean(resample))

    bootstrap_means = np.array(bootstrap_means)

    # Compute percentile confidence interval
    alpha = 1 - confidence
    lower = float(np.percentile(bootstrap_means, alpha / 2 * 100))
    upper = float(np.percentile(bootstrap_means, (1 - alpha / 2) * 100))

    return (float(np.mean(scores)), lower, upper)


def paired_ttest(
    scores_a: List[float],
    scores_b: List[float],
) -> Dict[str, float]:
    """
    Perform paired t-test.

    Args:
        scores_a: Scores from method A
        scores_b: Scores from method B

    Returns:
        Dictionary with test statistic, p-value, and summary statistics
    """
    scores_a = np.array(scores_a)
    scores_b = np.array(scores_b)

    if len(scores_a) != len(scores_b):
        raise ValueError("Score arrays must have the same length for paired test")

    if len(scores_a) < 2:
        return {
            'statistic': 0.0,
            'p_value': 1.0,
            'test_type': 'paired_ttest',
            'n_samples': len(scores_a),
            'error': 'Insufficient samples for t-test',
        }

    statistic, p_value = stats.ttest_rel(scores_a, scores_b)

    return {
        'statistic': float(statistic),
        'p_value': float(p_value),
        'test_type': 'paired_ttest',
        'n_samples': len(scores_a),
        'mean_a': float(np.mean(scores_a)),
        'mean_b': float(np.mean(scores_b)),
        'std_a': float(np.std(scores_a, ddof=1)),
        'std_b': float(np.std(scores_b, ddof=1)),
        'mean_diff': float(np.mean(scores_a - scores_b)),
        'std_diff': float(np.std(scores_a - scores_b, ddof=1)),
    }


def wilcoxon_test(
    scores_a: List[float],
    scores_b: List[float],
) -> Dict[str, float]:
    """
    Perform Wilcoxon signed-rank test (non-parametric alternative to paired t-test).

    Args:
        scores_a: Scores from method A
        scores_b: Scores from method B

    Returns:
        Dictionary with test statistic, p-value, and summary statistics
    """
    scores_a = np.array(scores_a)
    scores_b = np.array(scores_b)

    if len(scores_a) != len(scores_b):
        raise ValueError("Score arrays must have the same length for paired test")

    differences = scores_a - scores_b

    # Handle case where all differences are zero
    if np.all(differences == 0):
        return {
            'statistic': 0.0,
            'p_value': 1.0,
            'test_type': 'wilcoxon',
            'n_samples': len(scores_a),
            'note': 'All differences are zero',
        }

    # Handle case with too few non-zero differences
    non_zero_diffs = np.sum(differences != 0)
    if non_zero_diffs < 2:
        return {
            'statistic': 0.0,
            'p_value': 1.0,
            'test_type': 'wilcoxon',
            'n_samples': len(scores_a),
            'error': 'Insufficient non-zero differences for Wilcoxon test',
        }

    try:
        statistic, p_value = stats.wilcoxon(scores_a, scores_b)
    except ValueError as e:
        return {
            'statistic': 0.0,
            'p_value': 1.0,
            'test_type': 'wilcoxon',
            'n_samples': len(scores_a),
            'error': str(e),
        }

    return {
        'statistic': float(statistic),
        'p_value': float(p_value),
        'test_type': 'wilcoxon',
        'n_samples': len(scores_a),
        'mean_a': float(np.mean(scores_a)),
        'mean_b': float(np.mean(scores_b)),
        'std_a': float(np.std(scores_a, ddof=1)),
        'std_b': float(np.std(scores_b, ddof=1)),
        'median_a': float(np.median(scores_a)),
        'median_b': float(np.median(scores_b)),
    }


def compare_methods(
    method_a_dir: str,
    method_b_dir: str,
    method_a_name: str,
    method_b_name: str,
    ground_truth_file: str,
    confidence: float = 0.95,
) -> Dict[str, Any]:
    """
    Compare two methods with statistical testing.

    Args:
        method_a_dir: Directory with method A results
        method_b_dir: Directory with method B results
        method_a_name: Display name for method A
        method_b_name: Display name for method B
        ground_truth_file: Path to ground truth annotations
        confidence: Confidence level for bootstrap CI

    Returns:
        Comprehensive comparison results
    """
    print(f"\nComparing {method_a_name} vs {method_b_name}")
    print(f"  Method A: {method_a_dir}")
    print(f"  Method B: {method_b_dir}")

    # Load results
    results_a = load_experiment_results(method_a_dir, ground_truth_file)
    results_b = load_experiment_results(method_b_dir, ground_truth_file)

    comparisons = {}

    for metric in results_a.keys():
        scores_a = results_a[metric]
        scores_b = results_b.get(metric, [])

        # Skip if insufficient data
        if len(scores_a) < 2 or len(scores_b) < 2:
            print(f"  Skipping {metric}: insufficient data (A={len(scores_a)}, B={len(scores_b)})")
            continue

        # Ensure same number of runs for paired tests
        min_runs = min(len(scores_a), len(scores_b))
        scores_a_paired = scores_a[:min_runs]
        scores_b_paired = scores_b[:min_runs]

        # Bootstrap CI for each method
        mean_a, ci_lower_a, ci_upper_a = bootstrap_confidence_interval(
            scores_a, confidence
        )
        mean_b, ci_lower_b, ci_upper_b = bootstrap_confidence_interval(
            scores_b, confidence
        )

        # Statistical tests
        ttest_result = paired_ttest(scores_a_paired, scores_b_paired)
        wilcoxon_result = wilcoxon_test(scores_a_paired, scores_b_paired)

        comparisons[metric] = {
            method_a_name: {
                'mean': mean_a,
                'std': float(np.std(scores_a, ddof=1)) if len(scores_a) > 1 else 0.0,
                'ci_lower': ci_lower_a,
                'ci_upper': ci_upper_a,
                'n_runs': len(scores_a),
                'scores': scores_a,
            },
            method_b_name: {
                'mean': mean_b,
                'std': float(np.std(scores_b, ddof=1)) if len(scores_b) > 1 else 0.0,
                'ci_lower': ci_lower_b,
                'ci_upper': ci_upper_b,
                'n_runs': len(scores_b),
                'scores': scores_b,
            },
            'difference': mean_a - mean_b,
            'relative_improvement': (mean_a - mean_b) / mean_b * 100 if mean_b != 0 else 0.0,
            'paired_ttest': ttest_result,
            'wilcoxon': wilcoxon_result,
            'significant_at_005': wilcoxon_result['p_value'] < 0.05,
            'significant_at_001': wilcoxon_result['p_value'] < 0.01,
        }

        # Print summary
        print(f"\n  {metric}:")
        print(f"    {method_a_name}: {mean_a:.4f} ± {comparisons[metric][method_a_name]['std']:.4f} "
              f"[{ci_lower_a:.4f}, {ci_upper_a:.4f}]")
        print(f"    {method_b_name}: {mean_b:.4f} ± {comparisons[metric][method_b_name]['std']:.4f} "
              f"[{ci_lower_b:.4f}, {ci_upper_b:.4f}]")
        print(f"    Difference: {mean_a - mean_b:+.4f} ({comparisons[metric]['relative_improvement']:+.1f}%)")
        print(f"    Wilcoxon p-value: {wilcoxon_result['p_value']:.4f} "
              f"{'*' if comparisons[metric]['significant_at_005'] else ''}"
              f"{'*' if comparisons[metric]['significant_at_001'] else ''}")

    return comparisons


def generate_comparison_report(
    experiments: List[Dict[str, str]],
    ground_truth_file: str,
    output_path: str,
    confidence: float = 0.95,
) -> Dict[str, Any]:
    """
    Generate comprehensive comparison report for multiple methods.

    Args:
        experiments: List of dicts with 'name' and 'dir' keys
        ground_truth_file: Path to ground truth annotations
        output_path: Path to save JSON report
        confidence: Confidence level for bootstrap CI

    Returns:
        Full report dictionary
    """
    report = {
        'experiments': [e['name'] for e in experiments],
        'ground_truth': ground_truth_file,
        'confidence_level': confidence,
        'pairwise_comparisons': {},
        'summary': {},
    }

    # Pairwise comparisons
    for i, exp_a in enumerate(experiments):
        for exp_b in experiments[i+1:]:
            comparison_key = f"{exp_a['name']}_vs_{exp_b['name']}"
            print(f"\n{'='*60}")
            print(f"Comparison: {comparison_key}")
            print(f"{'='*60}")

            try:
                report['pairwise_comparisons'][comparison_key] = compare_methods(
                    exp_a['dir'],
                    exp_b['dir'],
                    exp_a['name'],
                    exp_b['name'],
                    ground_truth_file,
                    confidence,
                )
            except Exception as e:
                print(f"Error comparing {comparison_key}: {e}")
                report['pairwise_comparisons'][comparison_key] = {'error': str(e)}

    # Generate summary table
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    # Load all experiment results for summary
    all_results = {}
    for exp in experiments:
        try:
            all_results[exp['name']] = load_experiment_results(exp['dir'], ground_truth_file)
        except Exception as e:
            print(f"Error loading {exp['name']}: {e}")
            all_results[exp['name']] = {}

    # Create summary table
    metrics_to_report = ['narratives_f1_samples', 'subnarratives_f1_samples']
    for metric in metrics_to_report:
        report['summary'][metric] = {}
        print(f"\n{metric}:")
        for exp_name, results in all_results.items():
            scores = results.get(metric, [])
            if scores:
                mean, ci_lower, ci_upper = bootstrap_confidence_interval(scores, confidence)
                std = float(np.std(scores, ddof=1)) if len(scores) > 1 else 0.0
                report['summary'][metric][exp_name] = {
                    'mean': mean,
                    'std': std,
                    'ci_lower': ci_lower,
                    'ci_upper': ci_upper,
                    'n_runs': len(scores),
                }
                print(f"  {exp_name}: {mean:.4f} ± {std:.4f} [{ci_lower:.4f}, {ci_upper:.4f}]")
            else:
                print(f"  {exp_name}: No data")

    # Save report
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"\nReport saved to: {output_path}")
    return report


def main():
    """Main entry point for statistical testing."""
    parser = argparse.ArgumentParser(
        description="Statistical significance testing for multi-run experiments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Compare two methods
    compare_parser = subparsers.add_parser('compare', help='Compare two methods')
    compare_parser.add_argument('--method-a-dir', required=True, help='Method A results directory')
    compare_parser.add_argument('--method-a-name', required=True, help='Method A display name')
    compare_parser.add_argument('--method-b-dir', required=True, help='Method B results directory')
    compare_parser.add_argument('--method-b-name', required=True, help='Method B display name')
    compare_parser.add_argument('--ground-truth', required=True, help='Ground truth file')
    compare_parser.add_argument('--output', required=True, help='Output JSON file')
    compare_parser.add_argument('--confidence', type=float, default=0.95, help='Confidence level')

    # Multi-method comparison
    multi_parser = subparsers.add_parser('multi', help='Compare multiple methods')
    multi_parser.add_argument(
        '--experiments', nargs='+', required=True,
        help='Experiments as name:dir pairs (e.g., "Agora:results/agora")'
    )
    multi_parser.add_argument('--ground-truth', required=True, help='Ground truth file')
    multi_parser.add_argument('--output', required=True, help='Output JSON file')
    multi_parser.add_argument('--confidence', type=float, default=0.95, help='Confidence level')

    # Evaluate single experiment
    eval_parser = subparsers.add_parser('evaluate', help='Evaluate a single experiment')
    eval_parser.add_argument('--experiment-dir', required=True, help='Experiment directory')
    eval_parser.add_argument('--ground-truth', required=True, help='Ground truth file')
    eval_parser.add_argument('--output', help='Output JSON file (optional)')

    args = parser.parse_args()

    if args.command == 'compare':
        result = compare_methods(
            args.method_a_dir,
            args.method_b_dir,
            args.method_a_name,
            args.method_b_name,
            args.ground_truth,
            args.confidence,
        )
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        print(f"\nResults saved to: {args.output}")

    elif args.command == 'multi':
        experiments = []
        for exp in args.experiments:
            if ':' not in exp:
                print(f"Error: Invalid experiment format '{exp}'. Use 'name:dir'")
                return 1
            name, dir_path = exp.split(':', 1)
            experiments.append({'name': name, 'dir': dir_path})
        generate_comparison_report(experiments, args.ground_truth, args.output, args.confidence)

    elif args.command == 'evaluate':
        results = load_experiment_results(args.experiment_dir, args.ground_truth)
        print(f"\nExperiment: {args.experiment_dir}")
        print(f"Ground truth: {args.ground_truth}")
        for metric, scores in results.items():
            if scores:
                mean, ci_lower, ci_upper = bootstrap_confidence_interval(scores)
                std = float(np.std(scores, ddof=1)) if len(scores) > 1 else 0.0
                print(f"  {metric}: {mean:.4f} ± {std:.4f} [{ci_lower:.4f}, {ci_upper:.4f}] (n={len(scores)})")

        if args.output:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to: {args.output}")

    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())

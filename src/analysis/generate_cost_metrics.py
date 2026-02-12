"""
Generate cost_metrics.json files from existing experiment results.

This script reads experiment manifests, configs, and scoring results
to create cost metrics files for the cost-performance analysis.

Usage:
    python src/analysis/generate_cost_metrics.py --results-dir results/experiments/
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


# Estimated API calls per document based on method type
# (category + narratives + subnarratives, multiplied by agents)
CALLS_PER_DOC = {
    'baseline': 3,  # 1 category + 1 narrative + 1 subnarrative
    'actor_critic': 5,  # baseline + 2 validation calls
    'agora_3': 7,  # 1 category + 3 narrative + 3 subnarrative
    'agora_5': 11,  # 1 category + 5 narrative + 5 subnarrative
}

# Estimated tokens per call (input + output)
AVG_TOKENS_PER_CALL = {
    'input': 2000,
    'output': 500,
}

# Pricing per 1M tokens (as of 2025)
MODEL_PRICING = {
    'gpt-5-nano': {'input': 0.10, 'output': 0.40},
    'gpt-4o-mini': {'input': 0.15, 'output': 0.60},
    'gpt-4o': {'input': 2.50, 'output': 10.00},
    'gemini-2.5-flash': {'input': 0.075, 'output': 0.30},
    'gemini-2.5-pro': {'input': 1.25, 'output': 5.00},
    'deepseek-chat': {'input': 0.14, 'output': 0.28},
    'deepseek-reasoner': {'input': 0.55, 'output': 2.19},
    'mistral-large-latest': {'input': 2.00, 'output': 6.00},
    'mistral-small-latest': {'input': 0.20, 'output': 0.60},
}


def get_model_key(model_name: str) -> str:
    """Extract model key from full model name."""
    if ':' in model_name:
        return model_name.split(':')[-1]
    return model_name


def estimate_cost(model_name: str, num_calls: int) -> float:
    """Estimate cost based on model and number of calls."""
    model_key = get_model_key(model_name)
    pricing = MODEL_PRICING.get(model_key, {'input': 0.10, 'output': 0.40})

    input_tokens = num_calls * AVG_TOKENS_PER_CALL['input']
    output_tokens = num_calls * AVG_TOKENS_PER_CALL['output']

    input_cost = (input_tokens / 1_000_000) * pricing['input']
    output_cost = (output_tokens / 1_000_000) * pricing['output']

    return input_cost + output_cost


def run_scorer(results_file: str, gold_file: str) -> Optional[float]:
    """Run the scorer and extract F1-samples score."""
    try:
        # Import scorer directly from same directory
        scorer_path = Path(__file__).parent / "scorer.py"

        if not scorer_path.exists():
            print(f"  Warning: Scorer not found at {scorer_path}")
            return None

        # Run scorer as subprocess
        result = subprocess.run(
            [sys.executable, str(scorer_path), "--gold", gold_file, "--pred", results_file],
            capture_output=True,
            text=True,
        )

        # Parse F1-samples from output
        for line in result.stdout.split('\n'):
            if 'f1_samples:' in line.lower():
                # Extract the score from "f1_samples: 0.1234"
                parts = line.split(':')
                if len(parts) >= 2:
                    try:
                        return float(parts[-1].strip())
                    except ValueError:
                        pass

        # If no f1_samples line found, check for errors
        if result.returncode != 0:
            print(f"  Warning: Scorer returned error: {result.stderr}")

        return None
    except Exception as e:
        print(f"  Warning: Failed to run scorer: {e}")
        return None


def get_gold_file(config: Dict[str, Any]) -> Optional[str]:
    """Determine gold labels file from config."""
    input_folder = config.get('input_folder', '')

    # Map input folders to gold files
    if 'EN' in input_folder:
        return "data/dev-documents_4_December/EN/subtask-3-dominant-narratives.txt"
    elif 'BG' in input_folder:
        return "data/dev-documents_4_December/BG/subtask-3-dominant-narratives.txt"
    elif 'HI' in input_folder:
        return "data/dev-documents_4_December/HI/subtask-3-dominant-narratives.txt"
    elif 'PT' in input_folder:
        return "data/dev-documents_4_December/PT/subtask-3-dominant-narratives.txt"
    elif 'RU' in input_folder:
        return "data/dev-documents_4_December/RU/subtask-3-dominant-narratives.txt"

    return None


def count_documents(results_file: str) -> int:
    """Count number of documents processed from results file."""
    if not Path(results_file).exists():
        return 0

    file_ids = set()
    with open(results_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if parts:
                file_ids.add(parts[0])

    return len(file_ids)


def generate_cost_metrics(experiment_dir: Path) -> Optional[Dict[str, Any]]:
    """Generate cost metrics for a single experiment."""
    manifest_path = experiment_dir / 'experiment_manifest.json'
    config_path = experiment_dir / 'base_config.yaml'

    if not manifest_path.exists() or not config_path.exists():
        return None

    # Load manifest
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    # Load config
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    experiment_id = manifest.get('experiment_id', experiment_dir.name)
    model_name = config.get('model_name', 'unknown')
    num_narrative_agents = config.get('num_narrative_agents', 1)
    num_subnarrative_agents = config.get('num_subnarrative_agents', 1)
    enable_validation = config.get('enable_validation', False) or \
                       config.get('enable_narrative_validation', False)
    aggregation = config.get('narrative_aggregation_method', 'union')
    enable_retrieval = config.get('enable_retrieval', False)

    # Get total documents and duration from first successful run
    total_docs = 0
    total_latency_ms = 0
    results_file = None

    for run in manifest.get('runs', []):
        if run.get('status') == 'success':
            run_results = run.get('output_file', '')
            if Path(run_results).exists():
                total_docs = count_documents(run_results)
                total_latency_ms = run.get('duration_seconds', 0) * 1000
                results_file = run_results
                break

    if total_docs == 0:
        print(f"  Warning: No documents found for {experiment_id}")
        return None

    # Estimate API calls based on method
    if num_narrative_agents > 1:
        calls_per_doc = 1 + num_narrative_agents + num_subnarrative_agents
    elif enable_validation:
        calls_per_doc = CALLS_PER_DOC['actor_critic']
    else:
        calls_per_doc = CALLS_PER_DOC['baseline']

    total_api_calls = calls_per_doc * total_docs

    # Estimate tokens
    total_input_tokens = total_api_calls * AVG_TOKENS_PER_CALL['input']
    total_output_tokens = total_api_calls * AVG_TOKENS_PER_CALL['output']

    # Estimate cost
    total_cost_usd = estimate_cost(model_name, total_api_calls)

    # Try to get F1 score
    f1_samples = None
    gold_file = get_gold_file(config)
    if gold_file and results_file and Path(gold_file).exists():
        f1_samples = run_scorer(results_file, gold_file)

    # Create metrics
    metrics = {
        'experiment_id': experiment_id,
        'config_name': experiment_dir.name,
        'model_name': model_name,
        'total_documents': total_docs,
        'total_api_calls': total_api_calls,
        'total_input_tokens': total_input_tokens,
        'total_output_tokens': total_output_tokens,
        'total_cost_usd': total_cost_usd,
        'total_latency_ms': total_latency_ms,
        'num_narrative_agents': num_narrative_agents,
        'num_subnarrative_agents': num_subnarrative_agents,
        'aggregation_method': aggregation,
        'enable_validation': enable_validation,
        'enable_retrieval': enable_retrieval,
        'f1_samples': f1_samples,
    }

    return metrics


def main():
    parser = argparse.ArgumentParser(
        description="Generate cost_metrics.json files from experiment results"
    )
    parser.add_argument(
        '--results-dir',
        type=str,
        default='results/experiments/',
        help='Directory containing experiment results'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing cost_metrics.json files'
    )

    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    if not results_dir.exists():
        print(f"Error: Results directory not found: {results_dir}")
        return 1

    # Find all experiment directories
    experiments = [d for d in results_dir.iterdir() if d.is_dir()]

    print(f"Found {len(experiments)} experiment directories")

    generated = 0
    skipped = 0
    failed = 0

    for exp_dir in experiments:
        metrics_path = exp_dir / 'cost_metrics.json'

        if metrics_path.exists() and not args.force:
            print(f"  Skipping {exp_dir.name} (cost_metrics.json exists)")
            skipped += 1
            continue

        print(f"Processing {exp_dir.name}...")

        metrics = generate_cost_metrics(exp_dir)

        if metrics:
            with open(metrics_path, 'w', encoding='utf-8') as f:
                json.dump(metrics, f, indent=2)
            print(f"  Generated: {metrics_path}")
            print(f"    - Documents: {metrics['total_documents']}")
            print(f"    - Est. Cost: ${metrics['total_cost_usd']:.4f}")
            print(f"    - F1-Samples: {metrics['f1_samples']}")
            generated += 1
        else:
            print(f"  Failed to generate metrics for {exp_dir.name}")
            failed += 1

    print(f"\nSummary:")
    print(f"  Generated: {generated}")
    print(f"  Skipped: {skipped}")
    print(f"  Failed: {failed}")

    return 0


if __name__ == "__main__":
    exit(main())

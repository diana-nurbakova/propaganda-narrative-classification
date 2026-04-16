"""
Multi-run experiment runner for statistical significance testing.

Runs the same experiment multiple times with different seeds to enable
bootstrap confidence intervals and paired statistical tests.

Usage:
    python run_multi_experiment.py \\
        --config configs/experiments/agora_gpt5nano.yaml \\
        --n-runs 5 \\
        --experiment-id "agora_gpt5nano_en" \\
        --output-dir results/experiments/agora_gpt5nano_en/
"""

import argparse
import asyncio
import json
import os
import random
import shutil
import sys
import warnings

# Suppress coroutine warnings from LangChain internals
warnings.filterwarnings("ignore", message="coroutine .* was never awaited")
warnings.filterwarnings("ignore", category=RuntimeWarning, module="langchain")
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from dotenv import load_dotenv

# Load environment variables from .env file (API keys, Ollama credentials, etc.)
load_dotenv()


class TeeOutput:
    """
    A class that writes to both stdout and a log file simultaneously.
    Useful for capturing all terminal output while still displaying it.
    """

    def __init__(self, log_path: str, original_stdout):
        self.log_file = open(log_path, 'w', encoding='utf-8')
        self.original_stdout = original_stdout
        self.log_path = log_path

    def write(self, message):
        self.original_stdout.write(message)
        self.log_file.write(message)
        self.log_file.flush()  # Ensure immediate write

    def flush(self):
        self.original_stdout.flush()
        self.log_file.flush()

    def close(self):
        self.log_file.close()


def setup_logging(output_dir: str, experiment_id: str) -> Optional[TeeOutput]:
    """
    Set up logging to capture all output to a file.

    Args:
        output_dir: Directory to save the log file
        experiment_id: Experiment identifier for the log filename

    Returns:
        TeeOutput instance (or None if setup fails)
    """
    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = output_path / f"experiment_{experiment_id}_{timestamp}.log"

        tee = TeeOutput(str(log_path), sys.stdout)
        sys.stdout = tee
        sys.stderr = TeeOutput(str(log_path), sys.stderr)

        print(f"[Logging] Output will be saved to: {log_path}")
        return tee
    except Exception as e:
        print(f"[Logging] Warning: Could not set up logging: {e}")
        return None

from config_loader import ClassificationConfig
from cost_tracker import CostTracker
from run_with_config import run_classification


def generate_seeds(n_runs: int, base_seed: int = 42) -> List[int]:
    """
    Generate deterministic seeds for n runs.

    Uses a base seed to ensure reproducibility of the seed sequence itself.

    Args:
        n_runs: Number of runs to generate seeds for
        base_seed: Base seed for the random generator

    Returns:
        List of integer seeds
    """
    rng = random.Random(base_seed)
    return [rng.randint(0, 2**31 - 1) for _ in range(n_runs)]


def create_run_config(
    base_config_path: str,
    run_id: int,
    seed: int,
    experiment_id: str,
    output_dir: str,
    enable_cost_tracking: bool = True,
) -> str:
    """
    Create a temporary config file for a specific run.

    Args:
        base_config_path: Path to the base configuration file
        run_id: Run number (1-indexed)
        seed: Random seed for this run
        experiment_id: Experiment identifier
        output_dir: Base output directory
        enable_cost_tracking: Whether to enable cost tracking for this run

    Returns:
        Tuple of (path to temporary config file, output file path)
    """
    # Load base config
    with open(base_config_path, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)

    # Override seed and experiment metadata
    config_data['seed'] = seed
    config_data['run_id'] = run_id
    config_data['experiment_id'] = experiment_id

    # Enable cost tracking
    config_data['enable_cost_tracking'] = enable_cost_tracking

    # Update output path to include run_id
    original_output = config_data.get('output_file', 'results/output.txt')
    # Extract just the filename
    output_filename = Path(original_output).name

    # Create run-specific output path
    run_output_dir = Path(output_dir) / f"run_{run_id}"
    run_output_dir.mkdir(parents=True, exist_ok=True)
    config_data['output_file'] = str(run_output_dir / output_filename)

    # Create temporary config file
    temp_dir = tempfile.mkdtemp(prefix=f"experiment_{experiment_id}_")
    temp_config_path = Path(temp_dir) / f"run_{run_id}_config.yaml"

    with open(temp_config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config_data, f, default_flow_style=False)

    return str(temp_config_path), str(run_output_dir / output_filename)


async def run_single_experiment(
    base_config_path: str,
    run_id: int,
    seed: int,
    experiment_id: str,
    output_dir: str,
    enable_cost_tracking: bool = True,
) -> Dict[str, Any]:
    """
    Run a single experiment with specified seed.

    Args:
        base_config_path: Path to the base configuration file
        run_id: Run number (1-indexed)
        seed: Random seed for this run
        experiment_id: Experiment identifier
        output_dir: Base output directory
        enable_cost_tracking: Whether to enable cost tracking

    Returns:
        Dictionary with run results and metadata
    """
    start_time = datetime.now()
    temp_config_path = None
    temp_dir = None

    try:
        temp_config_path, output_file = create_run_config(
            base_config_path, run_id, seed, experiment_id, output_dir,
            enable_cost_tracking=enable_cost_tracking
        )
        temp_dir = Path(temp_config_path).parent

        print(f"\n[Run {run_id}] Starting with seed={seed}")
        print(f"[Run {run_id}] Config: {temp_config_path}")
        print(f"[Run {run_id}] Output: {output_file}")

        await run_classification(temp_config_path)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Check for cost metrics file
        cost_metrics_file = Path(output_file).parent / "cost_metrics.json"
        has_cost_metrics = cost_metrics_file.exists()

        return {
            'run_id': run_id,
            'seed': seed,
            'output_file': output_file,
            'cost_metrics_file': str(cost_metrics_file) if has_cost_metrics else None,
            'status': 'success',
            'started_at': start_time.isoformat(),
            'completed_at': end_time.isoformat(),
            'duration_seconds': duration,
        }

    except Exception as e:
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print(f"[Run {run_id}] FAILED: {e}")
        return {
            'run_id': run_id,
            'seed': seed,
            'status': 'failed',
            'error': str(e),
            'started_at': start_time.isoformat(),
            'completed_at': end_time.isoformat(),
            'duration_seconds': duration,
        }

    finally:
        # Clean up temporary config file
        if temp_dir and Path(temp_dir).exists():
            shutil.rmtree(temp_dir, ignore_errors=True)


async def run_multi_experiment(
    config_path: str,
    n_runs: int,
    experiment_id: str,
    output_dir: str,
    base_seed: int = 42,
    sequential: bool = True,
    enable_cost_tracking: bool = True,
    resume: bool = False,
) -> Dict[str, Any]:
    """
    Run multiple experiments with different seeds.

    Args:
        config_path: Path to the base configuration file
        n_runs: Number of runs
        experiment_id: Experiment identifier
        output_dir: Base output directory
        base_seed: Base seed for generating run seeds
        sequential: Whether to run sequentially (True) or in parallel (False)
        enable_cost_tracking: Whether to enable cost tracking
        resume: Whether to resume from an existing manifest (skip completed runs)

    Returns:
        Experiment manifest with all run results
    """
    print(f"\n{'='*60}")
    print(f"MULTI-RUN EXPERIMENT: {experiment_id}")
    print(f"{'='*60}")
    print(f"Base config: {config_path}")
    print(f"Number of runs: {n_runs}")
    print(f"Base seed: {base_seed}")
    print(f"Output directory: {output_dir}")
    print(f"Execution mode: {'sequential' if sequential else 'parallel'}")
    print(f"Cost tracking: {'enabled' if enable_cost_tracking else 'disabled'}")
    print(f"Resume mode: {'enabled' if resume else 'disabled'}")
    print(f"{'='*60}\n")

    # Generate seeds
    seeds = generate_seeds(n_runs, base_seed)
    print(f"Generated seeds: {seeds}\n")

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Copy base config to output directory for reference
    base_config_copy = output_path / "base_config.yaml"
    shutil.copy(config_path, base_config_copy)

    # Check for existing manifest when resuming
    completed_run_ids = set()
    existing_runs = []
    if resume:
        manifest_path = output_path / 'experiment_manifest.json'
        if manifest_path.exists():
            with open(manifest_path, 'r', encoding='utf-8') as f:
                existing_manifest = json.load(f)
            for run in existing_manifest.get('runs', []):
                if run.get('status') == 'success':
                    rid = run['run_id']
                    # Verify the result file actually exists
                    result_file = run.get('output_file', '')
                    if result_file and Path(result_file).exists():
                        completed_run_ids.add(rid)
                        existing_runs.append(run)
                        print(f"[Resume] Run {rid} already complete (seed={run.get('seed')}), skipping")
                    else:
                        print(f"[Resume] Run {rid} marked success but result file missing, will re-run")
            if completed_run_ids:
                print(f"[Resume] {len(completed_run_ids)}/{n_runs} runs already complete\n")
            else:
                print(f"[Resume] No completed runs found, starting fresh\n")

    # Create experiment manifest
    manifest = {
        'experiment_id': experiment_id,
        'base_config': str(config_path),
        'n_runs': n_runs,
        'base_seed': base_seed,
        'seeds': seeds,
        'sequential': sequential,
        'started_at': datetime.now().isoformat(),
        'runs': list(existing_runs),
    }

    # Run experiments
    if sequential:
        for i, seed in enumerate(seeds):
            run_id = i + 1
            if run_id in completed_run_ids:
                continue

            # Add delay between runs to avoid API rate limiting (especially for Mistral)
            if manifest['runs']:
                delay_seconds = 30  # Wait 30 seconds between runs
                print(f"\n[Multi-Run] Waiting {delay_seconds}s before run {run_id} to avoid rate limits...")
                await asyncio.sleep(delay_seconds)

            result = await run_single_experiment(
                config_path, run_id, seed, experiment_id, output_dir,
                enable_cost_tracking=enable_cost_tracking
            )
            manifest['runs'].append(result)

            # Save manifest after each run (for progress tracking)
            manifest_path = output_path / 'experiment_manifest.json'
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2)
    else:
        # Parallel execution (be careful with API rate limits)
        tasks = []
        task_indices = []
        for i, seed in enumerate(seeds):
            run_id = i + 1
            if run_id in completed_run_ids:
                continue
            tasks.append(
                run_single_experiment(
                    config_path, run_id, seed, experiment_id, output_dir,
                    enable_cost_tracking=enable_cost_tracking
                )
            )
            task_indices.append(i)
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for idx, result in zip(task_indices, results):
            if isinstance(result, Exception):
                manifest['runs'].append({
                    'run_id': idx + 1,
                    'seed': seeds[idx],
                    'status': 'failed',
                    'error': str(result),
                })
            else:
                manifest['runs'].append(result)

    # Sort runs by run_id for consistent ordering
    manifest['runs'].sort(key=lambda r: r.get('run_id', 0))

    # Finalize manifest
    manifest['completed_at'] = datetime.now().isoformat()
    total_duration = sum(
        r.get('duration_seconds', 0) for r in manifest['runs']
    )
    manifest['total_duration_seconds'] = total_duration
    manifest['successful_runs'] = sum(
        1 for r in manifest['runs'] if r.get('status') == 'success'
    )
    manifest['failed_runs'] = sum(
        1 for r in manifest['runs'] if r.get('status') == 'failed'
    )

    # Save final manifest
    manifest_path = output_path / 'experiment_manifest.json'
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    # Print summary
    print(f"\n{'='*60}")
    print(f"EXPERIMENT COMPLETED: {experiment_id}")
    print(f"{'='*60}")
    print(f"Total runs: {n_runs}")
    print(f"Successful: {manifest['successful_runs']}")
    print(f"Failed: {manifest['failed_runs']}")
    print(f"Total duration: {total_duration:.2f} seconds")
    print(f"Manifest saved to: {manifest_path}")
    print(f"{'='*60}\n")

    return manifest


def main():
    """Main entry point for multi-run experiments."""
    parser = argparse.ArgumentParser(
        description="Run multi-seed experiments for statistical significance testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run 5 experiments with different seeds
  python run_multi_experiment.py \\
      --config configs/experiments/agora_gpt5nano.yaml \\
      --n-runs 5 \\
      --experiment-id "agora_gpt5nano_en" \\
      --output-dir results/experiments/agora_gpt5nano_en/

  # Run with custom base seed
  python run_multi_experiment.py \\
      --config configs/experiments/baseline_gemini.yaml \\
      --n-runs 10 \\
      --experiment-id "baseline_gemini_en" \\
      --output-dir results/experiments/baseline_gemini_en/ \\
      --base-seed 123
        """
    )

    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to the base configuration file"
    )
    parser.add_argument(
        "--n-runs",
        type=int,
        default=5,
        help="Number of runs (default: 5)"
    )
    parser.add_argument(
        "--experiment-id",
        type=str,
        required=True,
        help="Unique experiment identifier"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Base output directory for results"
    )
    parser.add_argument(
        "--base-seed",
        type=int,
        default=42,
        help="Base seed for generating run seeds (default: 42)"
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run experiments in parallel (use with caution due to API rate limits)"
    )
    parser.add_argument(
        "--no-cost-tracking",
        action="store_true",
        help="Disable cost tracking (enabled by default)"
    )
    parser.add_argument(
        "--log",
        action="store_true",
        help="Enable logging to file (saves all output to experiment_*.log)"
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume incomplete experiment: skip runs already completed in the existing manifest"
    )

    args = parser.parse_args()

    # Set up logging if requested
    tee_output = None
    if args.log:
        tee_output = setup_logging(args.output_dir, args.experiment_id)

    # Validate config exists
    if not Path(args.config).exists():
        print(f"Error: Configuration file not found: {args.config}")
        return 1

    # Run experiments
    try:
        asyncio.run(run_multi_experiment(
            config_path=args.config,
            n_runs=args.n_runs,
            experiment_id=args.experiment_id,
            output_dir=args.output_dir,
            base_seed=args.base_seed,
            sequential=not args.parallel,
            enable_cost_tracking=not args.no_cost_tracking,
            resume=args.resume,
        ))
        return 0
    except KeyboardInterrupt:
        print("\nExperiment interrupted by user")
        return 1
    except Exception as e:
        print(f"Experiment failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())

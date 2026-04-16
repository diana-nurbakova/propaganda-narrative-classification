#!/usr/bin/env python3
"""
mDeBERTa Baseline: Train on unified annotations, evaluate on dev set for all languages.

Orchestrates the full pipeline:
1. Preprocess training data (if artifacts don't exist)
2. Train the hierarchical model (if model doesn't exist)
3. Run inference on dev set for all 5 languages
4. Output results in experiment format compatible with experiment_results_report.py

Usage:
    # Full pipeline (preprocess + train + inference)
    python src/mDeberta/run_all_languages.py

    # Inference only (requires trained model)
    python src/mDeberta/run_all_languages.py --inference-only

    # Custom model path
    python src/mDeberta/run_all_languages.py --model-path models/my_model

    # Custom threshold
    python src/mDeberta/run_all_languages.py --threshold 0.3
"""

import argparse
import json
import logging
import os
import random
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path


# Project root (this script is at src/mDeberta/run_all_languages.py)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent

# Add src/mDeberta to Python path so we can import multihead_deberta
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# Paths
ARTIFACTS_DIR = PROJECT_ROOT / "mdeberta_artifacts_hierarchical"
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "microsoft" / "mdeberta-v3-base_narratives_classifier_hierarchical"
DEVSET_DIR = PROJECT_ROOT / "data" / "dev-documents_4_December"
RESULTS_DIR = PROJECT_ROOT / "results" / "experiments"

LANGUAGES = ["EN", "BG", "HI", "PT", "RU"]


def step_preprocess():
    """Step 1: Preprocess training data."""
    tokenized_path = ARTIFACTS_DIR / "tokenized_dataset_hierarchical"
    if tokenized_path.exists():
        print(f"[SKIP] Preprocessed artifacts already exist at {ARTIFACTS_DIR}")
        return True

    print("=" * 60)
    print("STEP 1: Preprocessing training data")
    print("=" * 60)

    # Change to project root since preprocess_dataset.py uses relative paths
    original_cwd = os.getcwd()
    os.chdir(PROJECT_ROOT)

    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "preprocess_dataset", str(SCRIPT_DIR / "preprocess_dataset.py")
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print("[OK] Preprocessing complete")
        return True
    except Exception as e:
        print(f"[ERROR] Preprocessing failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        os.chdir(original_cwd)


def step_train():
    """Step 2: Train the hierarchical model."""
    if DEFAULT_MODEL_PATH.exists() and (DEFAULT_MODEL_PATH / "training_config.json").exists():
        print(f"[SKIP] Trained model already exists at {DEFAULT_MODEL_PATH}")
        return True

    print("=" * 60)
    print("STEP 2: Training hierarchical mDeBERTa model")
    print("=" * 60)

    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Training device: {device}")
    if device == "cpu":
        print("WARNING: Training on CPU will be slow (~2-4 hours for 10 epochs)")

    # Change to project root since train_mdeberta.py uses relative paths
    original_cwd = os.getcwd()
    os.chdir(PROJECT_ROOT)

    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "train_mdeberta", str(SCRIPT_DIR / "train_mdeberta.py")
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print("[OK] Training complete")
        return True
    except Exception as e:
        print(f"[ERROR] Training failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        os.chdir(original_cwd)


def generate_seeds(n_runs: int, base_seed: int = 42):
    """Generate deterministic seeds for n runs (same logic as run_multi_experiment.py)."""
    rng = random.Random(base_seed)
    return [rng.randint(0, 2**31 - 1) for _ in range(n_runs)]


def step_inference(model_path: Path, threshold: float = None, languages: list = None,
                   n_runs: int = 1):
    """Step 3: Run inference on dev set for all languages.

    Args:
        model_path: Path to the trained model directory.
        threshold: Override classification threshold (None = use trained).
        languages: List of language codes to evaluate.
        n_runs: Number of MC Dropout runs per language (1 = deterministic, >1 = MC Dropout).
    """
    if languages is None:
        languages = LANGUAGES
    print("=" * 60)
    print("STEP 3: Running inference on dev set (all languages)")
    if n_runs > 1:
        print(f"        MC Dropout enabled: {n_runs} runs per language")
    print("=" * 60)

    # Import the inference function
    from run_inference import run_inference

    # Load thresholds from training config if not specified
    if threshold is None:
        config_path = model_path / "training_config.json"
        if config_path.exists():
            with open(config_path, "r") as f:
                config = json.load(f)
            parent_threshold = config.get("best_parent_threshold", config.get("best_threshold", 0.5))
            child_threshold = config.get("best_child_threshold", parent_threshold)
            threshold = parent_threshold  # backward compat for manifests
            print(f"Using trained thresholds — parent: {parent_threshold:.3f}, child: {child_threshold:.3f}")
        else:
            threshold = 0.5
            print(f"Using default threshold: {threshold}")
    else:
        print(f"Using override threshold: {threshold:.3f} (applied to both parent and child)")

    mc_dropout = n_runs > 1
    seeds = generate_seeds(n_runs) if mc_dropout else [42]

    results = {}
    for lang in languages:
        input_dir = DEVSET_DIR / lang / "subtask-2-documents"
        if not input_dir.exists():
            print(f"[SKIP] No documents for {lang} at {input_dir}")
            continue

        exp_id = f"mdeberta_baseline_{lang.lower()}_t00"
        lang_runs = []

        for run_id, seed in enumerate(seeds, 1):
            exp_dir = RESULTS_DIR / exp_id / f"run_{run_id}"
            exp_dir.mkdir(parents=True, exist_ok=True)
            output_file = exp_dir / "results.txt"

            print(f"\n--- {lang} run {run_id}/{n_runs} (seed={seed}) ---")
            print(f"  Input: {input_dir}")
            print(f"  Output: {output_file}")

            start_time = time.time()
            try:
                run_inference(str(model_path), str(input_dir), str(output_file),
                              mc_dropout=mc_dropout, seed=seed)
                duration = time.time() - start_time
                lang_runs.append({
                    "run_id": run_id,
                    "seed": seed,
                    "status": "success",
                    "output_file": str(output_file),
                    "duration_seconds": duration,
                })
                n_files = len(list(input_dir.glob("*.txt")))
                print(f"  [OK] {lang} run {run_id}: {n_files} files in {duration:.1f}s")
            except Exception as e:
                duration = time.time() - start_time
                lang_runs.append({
                    "run_id": run_id,
                    "seed": seed,
                    "status": "failed",
                    "error": str(e),
                    "duration_seconds": duration,
                })
                print(f"  [ERROR] {lang} run {run_id}: {e}")
                traceback.print_exc()

        results[lang] = {
            "runs": lang_runs,
            "seeds": seeds,
            "n_files": len(list(input_dir.glob("*.txt"))),
        }

    return results, threshold


def create_experiment_manifests(results: dict, model_path: Path, threshold: float):
    """Create experiment manifest files compatible with experiment_results_report.py."""
    for lang, lang_result in results.items():
        runs = lang_result["runs"]
        seeds = lang_result["seeds"]
        successful_runs = [r for r in runs if r["status"] == "success"]
        failed_runs = [r for r in runs if r["status"] != "success"]

        if not successful_runs:
            print(f"[SKIP] No successful runs for {lang}")
            continue

        n_runs = len(runs)
        mc_dropout = n_runs > 1
        exp_id = f"mdeberta_baseline_{lang.lower()}_t00"
        exp_dir = RESULTS_DIR / exp_id

        # Create the base config YAML for documentation
        config_path = exp_dir / "config.yaml"
        mc_note = "# Variance: MC Dropout (dropout active during inference)\n" if mc_dropout else ""
        config_content = f"""# Experiment Configuration
# Model: mDeBERTa v3 base (fine-tuned)
# Method: Fine-tuned mDeBERTa Baseline
# Strategy: Hierarchical multi-head classification
# Language: {lang}
# Temperature: N/A (deterministic)
# Runs: {n_runs}
{mc_note}#
# Fine-tuned on unified training annotations (all languages combined)
# Threshold optimized during training

model_name: mdeberta:microsoft/mdeberta-v3-base
input_folder: data/dev-documents_4_December/{lang}/subtask-2-documents/
output_file: results/experiments/{exp_id}/run_1/results.txt
temperature: 0.0
top_p: 1.0
max_tokens: 512
hierarchical_strategy: multi_head
num_narrative_agents: 1
num_subnarrative_agents: 1
narrative_aggregation_method: single
subnarrative_aggregation_method: single
enable_validation: false
enable_narrative_validation: false
enable_subnarrative_validation: false
enable_retrieval: false
enable_cleaning: false
enable_text_cleaning: false
max_concurrency: 1
enable_cost_tracking: false
threshold: {threshold}
"""
        with open(config_path, "w") as f:
            f.write(config_content)

        total_duration = sum(r["duration_seconds"] for r in runs)

        # Build run entries for manifest
        manifest_runs = []
        for r in runs:
            entry = {
                "run_id": r["run_id"],
                "seed": r["seed"],
                "output_file": r.get("output_file", ""),
                "status": r["status"],
                "started_at": datetime.now().isoformat(),
                "completed_at": datetime.now().isoformat(),
                "duration_seconds": r["duration_seconds"],
            }
            if r["status"] != "success":
                entry["error"] = r.get("error", "unknown")
            manifest_runs.append(entry)

        if mc_dropout:
            model_note = f"MC Dropout inference ({n_runs} runs with different seeds for uncertainty estimation)"
        else:
            model_note = "Deterministic model - single run (no temperature/seed variation)"

        manifest = {
            "experiment_id": exp_id,
            "base_config": str(config_path),
            "n_runs": n_runs,
            "base_seed": 42,
            "seeds": seeds,
            "sequential": True,
            "started_at": datetime.now().isoformat(),
            "runs": manifest_runs,
            "completed_at": datetime.now().isoformat(),
            "total_duration_seconds": total_duration,
            "successful_runs": len(successful_runs),
            "failed_runs": len(failed_runs),
            "model_info": {
                "type": "mdeberta_fine_tuned",
                "base_model": "microsoft/mdeberta-v3-base",
                "model_path": str(model_path),
                "threshold": threshold,
                "training_data": "data/all-texts-unified/unified-annotations.tsv",
                "note": model_note,
            },
        }

        manifest_path = exp_dir / "experiment_manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        print(f"[OK] Created manifest for {exp_id} ({len(successful_runs)}/{n_runs} runs successful)")


class TeeStream:
    """Write to both a file and the original stream."""

    def __init__(self, original, log_file):
        self.original = original
        self.log_file = log_file

    def write(self, data):
        self.original.write(data)
        self.log_file.write(data)
        self.log_file.flush()

    def flush(self):
        self.original.flush()
        self.log_file.flush()

    def isatty(self):
        return hasattr(self.original, 'isatty') and self.original.isatty()


def setup_logging(log_path=None):
    """Set up logging to mirror all stdout/stderr to a log file."""
    if log_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = PROJECT_ROOT / "logs" / f"mdeberta_{timestamp}.log"

    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    log_file = open(log_path, "w", encoding="utf-8")
    sys.stdout = TeeStream(sys.__stdout__, log_file)
    sys.stderr = TeeStream(sys.__stderr__, log_file)

    print(f"[LOG] Logging to: {log_path}")


def main():
    parser = argparse.ArgumentParser(
        description="mDeBERTa baseline: preprocess, train, and evaluate on all languages"
    )
    parser.add_argument(
        "--inference-only",
        action="store_true",
        help="Skip preprocessing and training, run inference only",
    )
    parser.add_argument(
        "--model-path",
        type=str,
        default=str(DEFAULT_MODEL_PATH),
        help=f"Path to trained model (default: {DEFAULT_MODEL_PATH})",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=None,
        help="Override classification threshold (default: use trained threshold)",
    )
    parser.add_argument(
        "--languages",
        nargs="+",
        default=LANGUAGES,
        help="Languages to evaluate (default: all)",
    )
    parser.add_argument(
        "--n-runs",
        type=int,
        default=5,
        help="Number of inference runs per language (default: 5). "
             "Uses MC Dropout for variance when > 1.",
    )
    parser.add_argument(
        "--log",
        type=str,
        default=None,
        help="Log file path (mirrors all output to file). Default: logs/mdeberta_<timestamp>.log",
    )

    args = parser.parse_args()
    model_path = Path(args.model_path)

    # Set up logging to file + console
    setup_logging(args.log)

    n_runs = args.n_runs

    print("=" * 60)
    print("mDeBERTa BASELINE PIPELINE")
    print("=" * 60)
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Model path: {model_path}")
    languages = [l.upper() for l in args.languages]
    print(f"Languages: {languages}")
    print(f"Runs per language: {n_runs}" + (" (MC Dropout)" if n_runs > 1 else " (deterministic)"))
    print()

    if not args.inference_only:
        # Step 1: Preprocess
        if not step_preprocess():
            print("Preprocessing failed. Aborting.")
            return 1

        # Step 2: Train
        if not step_train():
            print("Training failed. Aborting.")
            return 1

    # Check model exists
    if not model_path.exists():
        print(f"ERROR: Model not found at {model_path}")
        print("Run without --inference-only to train first, or specify --model-path")
        return 1

    # Step 3: Inference
    results, threshold = step_inference(model_path, args.threshold, languages, n_runs=n_runs)

    # Step 4: Create manifests
    print("\n" + "=" * 60)
    print("STEP 4: Creating experiment manifests")
    print("=" * 60)
    create_experiment_manifests(results, model_path, threshold)

    # Summary
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)
    for lang, lang_result in results.items():
        runs = lang_result["runs"]
        n_files = lang_result.get("n_files", 0)
        ok = sum(1 for r in runs if r["status"] == "success")
        total_dur = sum(r["duration_seconds"] for r in runs)
        print(f"  {lang}: {ok}/{len(runs)} runs successful, {n_files} files, {total_dur:.1f}s total")

    print(f"\nResults saved to: {RESULTS_DIR}/mdeberta_baseline_*_t00/")
    print("Run experiment_results_report.py to include in the comparison report.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

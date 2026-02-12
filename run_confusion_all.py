#!/usr/bin/env python3
"""
Run multilabel confusion analysis for EVERY experiment individually
at both narrative and sub-narrative levels.

Output structure:
  results/analysis/confusion/per_experiment/{experiment_name}/
    narrative_confusion_heatmap.png
    narrative_confusion_report.md
    subnarrative_confusion_heatmap.png
    subnarrative_confusion_report.md
"""

import json
import subprocess
import sys
from pathlib import Path

EXPERIMENTS_DIR = Path("results/experiments")
OUTPUT_BASE = Path("results/analysis/confusion/per_experiment")
GOLD_FILES = {
    "en": "data/dev-documents_4_December/EN/subtask-3-dominant-narratives.txt",
    "bg": "data/dev-documents_4_December/BG/subtask-3-dominant-narratives.txt",
    "hi": "data/dev-documents_4_December/HI/subtask-3-dominant-narratives.txt",
    "pt": "data/dev-documents_4_December/PT/subtask-3-dominant-narratives.txt",
    "ru": "data/dev-documents_4_December/RU/subtask-3-dominant-narratives.txt",
}


def detect_language(exp_name: str) -> str:
    """Detect language from experiment name."""
    for lang in ["en", "bg", "hi", "pt", "ru"]:
        if f"_{lang}_" in exp_name or exp_name.endswith(f"_{lang}"):
            return lang
    return "en"


def get_best_result_file(exp_dir: Path) -> str | None:
    """Get the first successful result file from an experiment."""
    manifest_path = exp_dir / "experiment_manifest.json"
    if not manifest_path.exists():
        return None

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    for run in manifest.get("runs", []):
        if run.get("status") == "success":
            output_file = run.get("output_file", "")
            if Path(output_file).exists():
                return output_file
    return None


def main():
    python_exe = sys.executable
    script = "src/analysis/multilabel_confusion_analysis.py"

    experiments = sorted([d for d in EXPERIMENTS_DIR.iterdir()
                         if d.is_dir() and not d.name.startswith(".")])

    print(f"Found {len(experiments)} experiment directories")

    succeeded = 0
    skipped = 0
    failed = 0
    total = len(experiments)

    for i, exp_dir in enumerate(experiments, 1):
        exp_name = exp_dir.name
        lang = detect_language(exp_name)
        gold_file = GOLD_FILES.get(lang)

        if not gold_file or not Path(gold_file).exists():
            print(f"[{i}/{total}] SKIP {exp_name}: no gold file for '{lang}'")
            skipped += 1
            continue

        result_file = get_best_result_file(exp_dir)
        if not result_file:
            print(f"[{i}/{total}] SKIP {exp_name}: no successful run found")
            skipped += 1
            continue

        output_dir = OUTPUT_BASE / exp_name
        # Skip if already generated
        if (output_dir / "narrative_confusion_report.md").exists() and \
           (output_dir / "subnarrative_confusion_report.md").exists():
            print(f"[{i}/{total}] EXISTS {exp_name}")
            succeeded += 1
            continue

        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"[{i}/{total}] {exp_name} ({lang.upper()})")

        cmd = [
            python_exe, script,
            "--ground_truth", gold_file,
            "--predictions", result_file,
            "--output_dir", str(output_dir),
            "--level", "both",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            succeeded += 1
        else:
            print(f"  FAIL: {result.stderr[:200]}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Confusion analysis complete!")
    print(f"  Succeeded: {succeeded}")
    print(f"  Skipped:   {skipped}")
    print(f"  Failed:    {failed}")
    print(f"Results: {OUTPUT_BASE}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

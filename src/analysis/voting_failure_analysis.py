#!/usr/bin/env python3
"""
Voting Failure Analysis for Multi-Agent (Agora) Classification.

Phase 1: Retrospective analysis using existing prediction results.
  - Per-document error classification (FP, FN, Other inflation)
  - Cross-run consensus: systematic failures across 5 seeds
  - Cross-aggregation: same model+lang with different aggregation methods
  - Cross-model consensus: inherently hard documents
  - Narrative-level confusion patterns

Phase 2: Vote-level analysis (requires votes/ directories from pipeline).
  - Unanimous wrong, majority wrong, correct minority suppressed
  - Agreement entropy per document
  - Per-agent reliability metrics

Usage:
    python voting_failure_analysis.py \\
        --experiments-dir ../../results/experiments/ \\
        --ground-truth-dir ../../data/dev-documents_4_December/ \\
        --output ../../results/analysis/voting_failure_report.md
"""

import argparse
import json
import math
import os
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Reuse parsing utilities from experiment_results_report.py
sys.path.insert(0, str(Path(__file__).parent))
from experiment_results_report import (
    load_annotations,
    parse_labels,
    discover_experiments,
    parse_experiment_metadata,
    METHOD_DISPLAY,
    MODEL_DISPLAY,
)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class DocumentError:
    """Error classification for a single document in a single run."""

    file_id: str
    gt_narratives: Set[str]
    pred_narratives: Set[str]
    gt_subnarratives: Set[str]
    pred_subnarratives: Set[str]

    @property
    def narrative_fn(self) -> Set[str]:
        """False negatives: ground truth labels missed."""
        return self.gt_narratives - self.pred_narratives

    @property
    def narrative_fp(self) -> Set[str]:
        """False positives: predicted labels not in ground truth."""
        return self.pred_narratives - self.gt_narratives

    @property
    def narrative_tp(self) -> Set[str]:
        """True positives: correctly predicted labels."""
        return self.gt_narratives & self.pred_narratives

    @property
    def is_narrative_other(self) -> bool:
        """Prediction was reduced to 'Other'."""
        return self.pred_narratives == {"Other"} or len(self.pred_narratives) == 0

    @property
    def is_gt_other(self) -> bool:
        """Ground truth is 'Other'."""
        return self.gt_narratives == {"Other"} or len(self.gt_narratives) == 0

    @property
    def subnarrative_fn(self) -> Set[str]:
        return self.gt_subnarratives - self.pred_subnarratives

    @property
    def subnarrative_fp(self) -> Set[str]:
        return self.pred_subnarratives - self.gt_subnarratives

    @property
    def is_subnarrative_other(self) -> bool:
        return self.pred_subnarratives == {"Other"} or len(self.pred_subnarratives) == 0

    @property
    def is_correct_narrative(self) -> bool:
        return self.gt_narratives == self.pred_narratives

    @property
    def is_correct_subnarrative(self) -> bool:
        return self.gt_subnarratives == self.pred_subnarratives

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_id": self.file_id,
            "gt_narratives": sorted(self.gt_narratives),
            "pred_narratives": sorted(self.pred_narratives),
            "gt_subnarratives": sorted(self.gt_subnarratives),
            "pred_subnarratives": sorted(self.pred_subnarratives),
            "narrative_fp": sorted(self.narrative_fp),
            "narrative_fn": sorted(self.narrative_fn),
            "is_narrative_other": self.is_narrative_other,
            "is_correct_narrative": self.is_correct_narrative,
        }


# ---------------------------------------------------------------------------
# Phase 1: Experiment discovery & evaluation
# ---------------------------------------------------------------------------


def discover_agora_experiments(experiments_dir: str) -> List[Dict[str, Any]]:
    """
    Discover all agora experiments (num_narrative_agents > 1).

    Returns list of experiment dicts enriched with aggregation_method
    and group_key = (model_key, language, temperature).
    """
    all_experiments = discover_experiments(experiments_dir)
    agora_experiments = []

    for exp in all_experiments:
        meta = exp.get("meta", {})
        config = exp.get("config") or {}

        # Filter: must be multi-agent (agora)
        num_narr_agents = config.get("num_narrative_agents", 1)
        method = meta.get("method", "")
        is_agora = num_narr_agents > 1 or method.startswith("agora")

        if not is_agora:
            continue

        # Extract aggregation method
        agg_method = "intersection"  # default for plain "agora"
        if config:
            agg_method = config.get("narrative_aggregation_method", "intersection")
        elif "majority" in method:
            agg_method = "majority"
        elif "union" in method:
            agg_method = "union"

        exp["aggregation_method"] = agg_method
        exp["group_key"] = (
            meta.get("model_key", "unknown"),
            meta.get("language", "unknown"),
            meta.get("temperature", "unknown"),
        )
        agora_experiments.append(exp)

    return agora_experiments


def evaluate_experiment_documents(
    experiment: Dict[str, Any],
    ground_truth_dir: str,
) -> Dict[str, Any]:
    """
    Evaluate all runs of an experiment at the per-document level.

    Returns dict with per-run document errors and cross-run consensus.
    """
    meta = experiment["meta"]
    lang = meta.get("language", "unknown")
    manifest = experiment["manifest"]
    exp_dir = experiment["dir"]

    # Load ground truth
    gt_file = os.path.join(ground_truth_dir, lang, "subtask-3-dominant-narratives.txt")
    if not os.path.exists(gt_file):
        return {
            "experiment_id": experiment["experiment_id"],
            "error": f"Ground truth not found: {gt_file}",
            "runs": [],
        }
    ground_truth = load_annotations(gt_file)

    runs_data = []
    for run_info in manifest.get("runs", []):
        if run_info.get("status") != "success":
            continue

        run_id = run_info.get("run_id", "?")
        result_file = run_info.get("output_file", "")
        if not os.path.isabs(result_file):
            result_file = os.path.join(os.path.dirname(exp_dir), result_file)
        if not os.path.exists(result_file):
            # Try relative to experiment dir
            result_file = os.path.join(exp_dir, f"run_{run_id}", "results.txt")
        if not os.path.exists(result_file):
            continue

        predictions = load_annotations(result_file)
        common_files = sorted(set(ground_truth.keys()) & set(predictions.keys()))

        documents = {}
        for file_id in common_files:
            gt = ground_truth[file_id]
            pred = predictions[file_id]
            doc_err = DocumentError(
                file_id=file_id,
                gt_narratives=set(gt["narratives"]),
                pred_narratives=set(pred["narratives"]),
                gt_subnarratives=set(gt["subnarratives"]),
                pred_subnarratives=set(pred["subnarratives"]),
            )
            documents[file_id] = doc_err

        # Per-run summary stats
        n_total = len(documents)
        n_correct_narr = sum(1 for d in documents.values() if d.is_correct_narrative)
        n_correct_sub = sum(1 for d in documents.values() if d.is_correct_subnarrative)
        n_other_narr = sum(
            1 for d in documents.values() if d.is_narrative_other and not d.is_gt_other
        )
        n_other_sub = sum(
            1 for d in documents.values() if d.is_subnarrative_other and not d.is_gt_other
        )

        runs_data.append(
            {
                "run_id": run_id,
                "documents": documents,
                "n_total": n_total,
                "n_correct_narrative": n_correct_narr,
                "n_correct_subnarrative": n_correct_sub,
                "n_other_narrative": n_other_narr,
                "n_other_subnarrative": n_other_sub,
                "narrative_accuracy": n_correct_narr / n_total if n_total else 0,
                "subnarrative_accuracy": n_correct_sub / n_total if n_total else 0,
                "narrative_other_pct": n_other_narr / n_total if n_total else 0,
            }
        )

    # Cross-run consensus
    consensus_narr = cross_run_consensus(
        [r["documents"] for r in runs_data], "narrative"
    )
    consensus_sub = cross_run_consensus(
        [r["documents"] for r in runs_data], "subnarrative"
    )

    return {
        "experiment_id": experiment["experiment_id"],
        "meta": meta,
        "aggregation_method": experiment.get("aggregation_method", "?"),
        "n_runs": len(runs_data),
        "runs": runs_data,
        "consensus_narrative": consensus_narr,
        "consensus_subnarrative": consensus_sub,
    }


def cross_run_consensus(
    runs: List[Dict[str, "DocumentError"]],
    level: str = "narrative",
) -> Dict[str, Any]:
    """
    Find documents that are wrong in ALL runs (systematic failures)
    vs documents that vary across runs (stochastic failures).
    """
    if not runs:
        return {
            "systematic_failures": [],
            "stochastic_failures": [],
            "consistently_correct": [],
            "per_document_correctness_rate": {},
        }

    all_files = set()
    for run_docs in runs:
        all_files.update(run_docs.keys())

    n_runs = len(runs)
    per_doc_correct_count = {}

    for file_id in all_files:
        correct_count = 0
        present_count = 0
        for run_docs in runs:
            if file_id not in run_docs:
                continue
            present_count += 1
            doc = run_docs[file_id]
            if level == "narrative":
                if doc.is_correct_narrative:
                    correct_count += 1
            else:
                if doc.is_correct_subnarrative:
                    correct_count += 1
        per_doc_correct_count[file_id] = (correct_count, present_count)

    systematic_failures = [
        f for f, (c, p) in per_doc_correct_count.items() if c == 0 and p > 0
    ]
    stochastic_failures = [
        f for f, (c, p) in per_doc_correct_count.items() if 0 < c < p
    ]
    consistently_correct = [
        f for f, (c, p) in per_doc_correct_count.items() if c == p and p > 0
    ]

    return {
        "systematic_failures": sorted(systematic_failures),
        "stochastic_failures": sorted(stochastic_failures),
        "consistently_correct": sorted(consistently_correct),
        "per_document_correctness_rate": {
            f: c / p if p > 0 else 0.0
            for f, (c, p) in per_doc_correct_count.items()
        },
    }


# ---------------------------------------------------------------------------
# Phase 1: Cross-aggregation analysis
# ---------------------------------------------------------------------------


def cross_aggregation_analysis(
    experiments_by_group: Dict[Tuple, List[Dict]],
    all_evaluations: Dict[str, Dict],
) -> List[Dict[str, Any]]:
    """
    For model+lang+temp combos with multiple aggregation methods,
    compare document-level outcomes using run_1 (same seeds).
    """
    comparisons = []

    for group_key, experiments in experiments_by_group.items():
        if len(experiments) < 2:
            continue

        # Build method -> experiment mapping
        method_map = {}
        for exp in experiments:
            agg = exp.get("aggregation_method", "?")
            method_map[agg] = exp["experiment_id"]

        if len(method_map) < 2:
            continue

        # Get run_1 results for each method
        method_docs = {}
        for agg, exp_id in method_map.items():
            eval_data = all_evaluations.get(exp_id)
            if not eval_data or not eval_data.get("runs"):
                continue
            # Use first run for comparison
            method_docs[agg] = eval_data["runs"][0]["documents"]

        if len(method_docs) < 2:
            continue

        # Find common files across all methods
        all_file_sets = [set(docs.keys()) for docs in method_docs.values()]
        common_files = sorted(set.intersection(*all_file_sets)) if all_file_sets else []

        # Per-document comparison
        per_doc = {}
        for file_id in common_files:
            per_doc[file_id] = {}
            for agg, docs in method_docs.items():
                per_doc[file_id][agg] = docs[file_id].is_correct_narrative

        # Classify failure patterns
        correct_union_wrong_intersection = []
        correct_majority_wrong_intersection = []
        wrong_all_methods = []
        methods = sorted(method_docs.keys())

        for file_id in common_files:
            results = per_doc[file_id]
            all_wrong = all(not v for v in results.values())

            if all_wrong:
                wrong_all_methods.append(file_id)
            else:
                if "intersection" in results and not results["intersection"]:
                    if "union" in results and results["union"]:
                        correct_union_wrong_intersection.append(file_id)
                    if "majority" in results and results["majority"]:
                        correct_majority_wrong_intersection.append(file_id)

        # Detailed error examples for documents salvaged by union
        salvaged_details = []
        for file_id in correct_union_wrong_intersection[:5]:
            detail = {"file_id": file_id}
            for agg, docs in method_docs.items():
                doc = docs[file_id]
                detail[f"{agg}_pred"] = sorted(doc.pred_narratives)
                detail[f"{agg}_correct"] = doc.is_correct_narrative
            detail["ground_truth"] = sorted(
                method_docs[methods[0]][file_id].gt_narratives
            )
            salvaged_details.append(detail)

        model_key, lang, temp = group_key
        model_display = MODEL_DISPLAY.get(model_key, model_key)
        comparisons.append(
            {
                "group_key": group_key,
                "model_display": model_display,
                "language": lang,
                "temperature": temp,
                "methods": methods,
                "n_common_files": len(common_files),
                "correct_union_wrong_intersection": correct_union_wrong_intersection,
                "correct_majority_wrong_intersection": correct_majority_wrong_intersection,
                "wrong_all_methods": wrong_all_methods,
                "per_document": per_doc,
                "salvaged_details": salvaged_details,
            }
        )

    return comparisons


# ---------------------------------------------------------------------------
# Phase 1: Cross-model consensus failures
# ---------------------------------------------------------------------------


def cross_model_consensus_failures(
    all_evaluations: Dict[str, Dict],
    experiments: List[Dict],
) -> Dict[str, Any]:
    """
    Per language, find documents wrong across ALL models = inherently hard.
    Uses run_1 from each experiment.
    """
    # Group by language
    by_lang = defaultdict(list)
    for exp in experiments:
        lang = exp["meta"].get("language", "unknown")
        by_lang[lang].append(exp)

    results = {}
    for lang, lang_exps in by_lang.items():
        # Per-document, track which experiments got it right
        doc_model_results = defaultdict(dict)

        for exp in lang_exps:
            exp_id = exp["experiment_id"]
            eval_data = all_evaluations.get(exp_id)
            if not eval_data or not eval_data.get("runs"):
                continue

            run1_docs = eval_data["runs"][0]["documents"]
            agg = exp.get("aggregation_method", "?")
            label = f"{exp_id}"

            for file_id, doc in run1_docs.items():
                doc_model_results[file_id][label] = doc.is_correct_narrative

        # Find documents wrong in ALL experiments for this language
        hard_docs = []
        for file_id, model_results in doc_model_results.items():
            if model_results and all(not v for v in model_results.values()):
                hard_docs.append(file_id)

        results[lang] = {
            "hard_documents": sorted(hard_docs),
            "n_hard": len(hard_docs),
            "n_total": len(doc_model_results),
            "n_experiments": len(lang_exps),
            "per_document_model_results": {
                f: dict(r) for f, r in doc_model_results.items()
            },
        }

    return results


# ---------------------------------------------------------------------------
# Phase 1: Other inflation analysis
# ---------------------------------------------------------------------------


def other_inflation_analysis(
    all_evaluations: Dict[str, Dict],
) -> Dict[str, Dict[str, Any]]:
    """
    Percentage of documents reduced to 'Other' per experiment, averaged across runs.
    """
    results = {}
    for exp_id, eval_data in all_evaluations.items():
        if not eval_data.get("runs"):
            continue

        narr_other_pcts = []
        sub_other_pcts = []
        for run in eval_data["runs"]:
            narr_other_pcts.append(run.get("narrative_other_pct", 0))
            n_total = run["n_total"]
            if n_total > 0:
                sub_other_pcts.append(run["n_other_subnarrative"] / n_total)

        results[exp_id] = {
            "narrative_other_pct_mean": (
                sum(narr_other_pcts) / len(narr_other_pcts) if narr_other_pcts else 0
            ),
            "subnarrative_other_pct_mean": (
                sum(sub_other_pcts) / len(sub_other_pcts) if sub_other_pcts else 0
            ),
            "per_run_narrative_other_pct": narr_other_pcts,
            "aggregation_method": eval_data.get("aggregation_method", "?"),
        }

    return results


# ---------------------------------------------------------------------------
# Phase 1: Narrative confusion analysis
# ---------------------------------------------------------------------------


def narrative_confusion_analysis(
    all_evaluations: Dict[str, Dict],
) -> Dict[str, Any]:
    """
    Count which narrative pairs are most commonly confused (FP when GT has a different label).
    """
    narrative_confusions = Counter()
    subnarrative_confusions = Counter()

    for exp_id, eval_data in all_evaluations.items():
        for run in eval_data.get("runs", []):
            for file_id, doc in run.get("documents", {}).items():
                # For each false positive, pair it with each ground truth label
                for fp in doc.narrative_fp:
                    for gt in doc.gt_narratives:
                        if gt != "Other":
                            narrative_confusions[(gt, fp)] += 1
                for fp in doc.subnarrative_fp:
                    for gt in doc.gt_subnarratives:
                        if gt != "Other":
                            subnarrative_confusions[(gt, fp)] += 1

    return {
        "narrative_confusions": narrative_confusions,
        "subnarrative_confusions": subnarrative_confusions,
        "top_20_narrative_confusions": narrative_confusions.most_common(20),
        "top_20_subnarrative_confusions": subnarrative_confusions.most_common(20),
    }


# ---------------------------------------------------------------------------
# Phase 2: Vote-level analysis (conditional on votes/ directories)
# ---------------------------------------------------------------------------


def try_vote_level_analysis(
    experiments: List[Dict],
    ground_truth_dir: str,
) -> Optional[Dict[str, Any]]:
    """
    Attempt Phase 2 vote-level analysis. Returns None if no votes/ dirs exist.
    """
    has_votes = False
    for exp in experiments:
        exp_dir = Path(exp["dir"])
        for run_dir in sorted(exp_dir.glob("run_*")):
            votes_dir = run_dir / "votes"
            if votes_dir.exists() and any(votes_dir.glob("*.json")):
                has_votes = True
                break
        if has_votes:
            break

    if not has_votes:
        print("  No votes/ directories found. Skipping Phase 2 vote-level analysis.")
        print("  Run experiments with enable_vote_saving: true to generate vote data.")
        return None

    print("  Found votes/ directories. Running Phase 2 vote-level analysis...")
    return _run_vote_level_analysis(experiments, ground_truth_dir)


def _run_vote_level_analysis(
    experiments: List[Dict],
    ground_truth_dir: str,
) -> Dict[str, Any]:
    """
    Full vote-level failure taxonomy analysis.
    """
    failure_taxonomy = defaultdict(lambda: defaultdict(list))
    agreement_entropies = defaultdict(list)
    per_agent_reliability = defaultdict(lambda: defaultdict(int))

    for exp in experiments:
        exp_id = exp["experiment_id"]
        exp_dir = Path(exp["dir"])
        meta = exp["meta"]
        lang = meta.get("language", "unknown")

        gt_file = os.path.join(
            ground_truth_dir, lang, "subtask-3-dominant-narratives.txt"
        )
        if not os.path.exists(gt_file):
            continue
        ground_truth = load_annotations(gt_file)

        for run_dir in sorted(exp_dir.glob("run_*")):
            votes_dir = run_dir / "votes"
            if not votes_dir.exists():
                continue

            for vote_file in sorted(votes_dir.glob("*.json")):
                with open(vote_file, "r", encoding="utf-8") as f:
                    votes = json.load(f)

                file_id = votes["file_id"]
                if file_id not in ground_truth:
                    continue

                gt = ground_truth[file_id]
                gt_narr = set(gt["narratives"])
                narrative_votes = votes.get("narrative_votes", [])
                aggregated = set(votes.get("aggregated_narratives", []))

                # Classify failure type
                failure_type = classify_vote_failure(gt_narr, narrative_votes, aggregated)
                if failure_type:
                    failure_taxonomy[exp_id][failure_type].append(file_id)

                # Agreement entropy
                entropy = compute_agreement_entropy(narrative_votes)
                agreement_entropies[exp_id].append(
                    {"file_id": file_id, "entropy": entropy, "correct": aggregated == gt_narr}
                )

                # Per-agent reliability
                for agent_idx, agent_votes in enumerate(narrative_votes):
                    agent_set = set(agent_votes)
                    if agent_set & gt_narr:
                        per_agent_reliability[exp_id][
                            f"agent_{agent_idx}_correct"
                        ] += 1
                    per_agent_reliability[exp_id][f"agent_{agent_idx}_total"] += 1

    return {
        "failure_taxonomy": {k: dict(v) for k, v in failure_taxonomy.items()},
        "agreement_entropies": dict(agreement_entropies),
        "per_agent_reliability": dict(per_agent_reliability),
    }


def classify_vote_failure(
    gt_labels: Set[str],
    agent_votes: List[List[str]],
    aggregated: Set[str],
) -> Optional[str]:
    """
    Classify the type of voting failure for a single document.

    Returns None if the aggregated result is correct, or one of:
    - "unanimous_wrong", "majority_wrong", "correct_minority_suppressed",
    - "all_empty_cascade", "label_fragmentation"
    """
    if aggregated == gt_labels:
        return None

    n_agents = len(agent_votes)
    if n_agents == 0:
        return "all_empty_cascade"

    # Check for empty cascade
    empty_agents = sum(1 for v in agent_votes if len(v) == 0)
    if empty_agents > 0:
        return "all_empty_cascade"

    # Check if any agent had any correct labels (overlap with GT)
    agents_with_correct = 0
    for votes in agent_votes:
        if set(votes) & gt_labels:
            agents_with_correct += 1

    if agents_with_correct == 0:
        return "unanimous_wrong"
    elif agents_with_correct < n_agents and agents_with_correct <= n_agents // 2:
        return "correct_minority_suppressed"
    elif agents_with_correct < n_agents:
        return "majority_wrong"
    else:
        # All agents had some correct overlap but aggregation still fails
        return "label_fragmentation"


def compute_agreement_entropy(agent_votes: List[List[str]]) -> float:
    """
    Shannon entropy of label vote distribution across agents.
    Higher = more disagreement. 0 = perfect agreement.
    """
    if not agent_votes:
        return 0.0

    label_counts = Counter()
    for votes in agent_votes:
        for label in votes:
            label_counts[label] += 1

    if not label_counts:
        return 0.0

    total = sum(label_counts.values())
    entropy = 0.0
    for count in label_counts.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)

    return entropy


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------


def generate_report(
    agora_experiments: List[Dict],
    all_evaluations: Dict[str, Dict],
    cross_agg_results: List[Dict],
    cross_model_results: Dict,
    other_inflation: Dict,
    confusion_results: Dict,
    vote_analysis: Optional[Dict] = None,
) -> str:
    """Generate comprehensive Markdown report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append("# Voting Failure Analysis Report")
    lines.append(f"\nGenerated: {now}\n")

    # --- Executive Summary ---
    n_experiments = len(agora_experiments)
    models_used = set()
    languages_used = set()
    agg_methods_used = set()
    for exp in agora_experiments:
        models_used.add(exp["meta"].get("model_display", "?"))
        languages_used.add(exp["meta"].get("language", "?"))
        agg_methods_used.add(exp.get("aggregation_method", "?"))

    lines.append("## 1. Executive Summary\n")
    lines.append(f"- **Experiments analyzed**: {n_experiments}")
    lines.append(f"- **Models**: {', '.join(sorted(models_used))}")
    lines.append(f"- **Languages**: {', '.join(sorted(languages_used))}")
    lines.append(f"- **Aggregation methods**: {', '.join(sorted(agg_methods_used))}")

    # Count total systematic failures
    total_systematic = 0
    for exp_id, eval_data in all_evaluations.items():
        consensus = eval_data.get("consensus_narrative", {})
        total_systematic += len(consensus.get("systematic_failures", []))
    lines.append(
        f"- **Total systematic narrative failures** (wrong in all runs): {total_systematic}"
    )
    lines.append("")

    # --- "Other" Inflation ---
    lines.append("## 2. 'Other' Inflation by Aggregation Method\n")
    lines.append(
        "Documents reduced to 'Other' (empty prediction) when ground truth is not Other.\n"
    )
    lines.append(
        "| Experiment | Aggregation | Model | Lang | Narrative Other % | Subnarrative Other % |"
    )
    lines.append(
        "|---|---|---|---|---|---|"
    )

    # Sort by aggregation method then experiment
    sorted_inflation = sorted(
        other_inflation.items(),
        key=lambda x: (x[1].get("aggregation_method", ""), x[0]),
    )
    for exp_id, data in sorted_inflation:
        eval_data = all_evaluations.get(exp_id, {})
        meta = eval_data.get("meta", {})
        model = meta.get("model_display", "?")
        lang = meta.get("language", "?")
        agg = data.get("aggregation_method", "?")
        narr_pct = data["narrative_other_pct_mean"] * 100
        sub_pct = data["subnarrative_other_pct_mean"] * 100
        lines.append(
            f"| {exp_id} | {agg} | {model} | {lang} | {narr_pct:.1f}% | {sub_pct:.1f}% |"
        )
    lines.append("")

    # --- Aggregation method summary ---
    agg_summary = defaultdict(list)
    for exp_id, data in other_inflation.items():
        agg = data.get("aggregation_method", "?")
        agg_summary[agg].append(data["narrative_other_pct_mean"] * 100)

    if agg_summary:
        lines.append("### Summary by Aggregation Method\n")
        lines.append("| Method | Mean Other % | Min | Max | N |")
        lines.append("|---|---|---|---|---|")
        for method in ["intersection", "majority", "union"]:
            if method in agg_summary:
                vals = agg_summary[method]
                mean_v = sum(vals) / len(vals)
                lines.append(
                    f"| {method} | {mean_v:.1f}% | {min(vals):.1f}% | {max(vals):.1f}% | {len(vals)} |"
                )
        lines.append("")

    # --- Systematic Failures ---
    lines.append("## 3. Systematic Failures (Wrong in All Runs)\n")
    lines.append(
        "Documents misclassified at the narrative level in every single run of an experiment.\n"
    )

    # Group by aggregation method for readability
    for agg_method in ["intersection", "majority", "union"]:
        agg_exps = [
            (exp_id, eval_data)
            for exp_id, eval_data in all_evaluations.items()
            if eval_data.get("aggregation_method") == agg_method
        ]
        if not agg_exps:
            continue

        lines.append(f"### {agg_method.capitalize()}\n")
        lines.append(
            "| Experiment | Model | Lang | Systematic Failures | Stochastic | Correct | Total |"
        )
        lines.append("|---|---|---|---|---|---|---|")

        for exp_id, eval_data in sorted(agg_exps, key=lambda x: x[0]):
            meta = eval_data.get("meta", {})
            model = meta.get("model_display", "?")
            lang = meta.get("language", "?")
            consensus = eval_data.get("consensus_narrative", {})
            n_sys = len(consensus.get("systematic_failures", []))
            n_stoch = len(consensus.get("stochastic_failures", []))
            n_correct = len(consensus.get("consistently_correct", []))
            n_total = n_sys + n_stoch + n_correct
            lines.append(
                f"| {exp_id} | {model} | {lang} | **{n_sys}** | {n_stoch} | {n_correct} | {n_total} |"
            )

        lines.append("")

    # List specific systematic failure documents for top experiments
    lines.append("### Detailed Systematic Failure Documents\n")
    for exp_id, eval_data in sorted(all_evaluations.items()):
        consensus = eval_data.get("consensus_narrative", {})
        sys_failures = consensus.get("systematic_failures", [])
        if not sys_failures:
            continue

        meta = eval_data.get("meta", {})
        model = meta.get("model_display", "?")
        agg = eval_data.get("aggregation_method", "?")
        lines.append(f"**{exp_id}** ({model}, {agg}):")

        # Show GT vs pred for each failed document (from run 1)
        if eval_data.get("runs"):
            run1_docs = eval_data["runs"][0]["documents"]
            for file_id in sys_failures[:10]:
                doc = run1_docs.get(file_id)
                if doc:
                    gt_str = "; ".join(sorted(doc.gt_narratives))
                    pred_str = "; ".join(sorted(doc.pred_narratives))
                    lines.append(f"  - `{file_id}`: GT=`{gt_str}` | Pred=`{pred_str}`")

        if len(sys_failures) > 10:
            lines.append(f"  - ... and {len(sys_failures) - 10} more")
        lines.append("")

    # --- Cross-Aggregation Comparison ---
    lines.append("## 4. Cross-Aggregation Comparison\n")
    if not cross_agg_results:
        lines.append("No model+language+temperature combinations with multiple aggregation methods found.\n")
    else:
        lines.append(
            "Same model+language+temperature with different aggregation methods. "
            "Shows documents where the aggregation method determines correctness.\n"
        )

        for comp in cross_agg_results:
            model = comp["model_display"]
            lang = comp["language"]
            temp = comp["temperature"]
            lines.append(f"### {model} — {lang} (T={temp})\n")
            lines.append(f"- Methods compared: {', '.join(comp['methods'])}")
            lines.append(f"- Common documents: {comp['n_common_files']}")
            lines.append(
                f"- **Correct under union, wrong under intersection**: "
                f"{len(comp['correct_union_wrong_intersection'])} documents"
            )
            lines.append(
                f"- **Correct under majority, wrong under intersection**: "
                f"{len(comp['correct_majority_wrong_intersection'])} documents"
            )
            lines.append(
                f"- **Wrong under ALL methods** (true consensus failure): "
                f"{len(comp['wrong_all_methods'])} documents"
            )

            if comp["salvaged_details"]:
                lines.append("\nExample documents salvaged by union over intersection:\n")
                for detail in comp["salvaged_details"]:
                    lines.append(f"- **`{detail['file_id']}`**")
                    lines.append(f"  - Ground truth: `{'; '.join(detail['ground_truth'])}`")
                    for method in comp["methods"]:
                        pred_key = f"{method}_pred"
                        correct_key = f"{method}_correct"
                        if pred_key in detail:
                            status = "correct" if detail.get(correct_key) else "WRONG"
                            lines.append(
                                f"  - {method}: `{'; '.join(detail[pred_key])}` ({status})"
                            )

            lines.append("")

    # --- Cross-Model Hard Documents ---
    lines.append("## 5. Cross-Model Hard Documents\n")
    lines.append(
        "Documents wrong across ALL agora experiments for a given language "
        "(inherently ambiguous or hard).\n"
    )

    for lang in sorted(cross_model_results.keys()):
        data = cross_model_results[lang]
        hard_docs = data["hard_documents"]
        lines.append(
            f"### {lang}: {data['n_hard']} hard documents "
            f"(out of {data['n_total']}, across {data['n_experiments']} experiments)\n"
        )
        if hard_docs:
            for doc_id in hard_docs:
                lines.append(f"- `{doc_id}`")
        else:
            lines.append("No universally hard documents found.")
        lines.append("")

    # --- Narrative Confusion Patterns ---
    lines.append("## 6. Narrative Confusion Patterns\n")
    lines.append(
        "Most commonly confused narrative pairs across all experiments. "
        "Format: (ground_truth, false_positive) -> count.\n"
    )

    top_narr = confusion_results.get("top_20_narrative_confusions", [])
    if top_narr:
        lines.append("### Top Narrative Confusions\n")
        lines.append("| Rank | Ground Truth | False Positive | Count |")
        lines.append("|---|---|---|---|")
        for i, ((gt, fp), count) in enumerate(top_narr, 1):
            lines.append(f"| {i} | {gt} | {fp} | {count} |")
        lines.append("")

    top_sub = confusion_results.get("top_20_subnarrative_confusions", [])
    if top_sub:
        lines.append("### Top Subnarrative Confusions\n")
        lines.append("| Rank | Ground Truth | False Positive | Count |")
        lines.append("|---|---|---|---|")
        for i, ((gt, fp), count) in enumerate(top_sub[:20], 1):
            lines.append(f"| {i} | {gt} | {fp} | {count} |")
        lines.append("")

    # --- Phase 2: Vote-Level Taxonomy ---
    if vote_analysis:
        lines.append("## 7. Vote-Level Failure Taxonomy (Phase 2)\n")
        lines.append(
            "Per-agent vote data available. Failure types based on individual agent predictions.\n"
        )

        taxonomy = vote_analysis.get("failure_taxonomy", {})
        if taxonomy:
            # Aggregate across experiments
            type_totals = Counter()
            for exp_id, types in taxonomy.items():
                for ftype, docs in types.items():
                    type_totals[ftype] += len(docs)

            lines.append("### Failure Type Distribution (all experiments)\n")
            lines.append("| Failure Type | Count | Description |")
            lines.append("|---|---|---|")
            descriptions = {
                "unanimous_wrong": "All agents agree on wrong label(s)",
                "correct_minority_suppressed": "Correct agent outvoted by incorrect majority",
                "majority_wrong": "Majority of agents wrong, but some correct",
                "all_empty_cascade": "Agent(s) returned empty, collapsing intersection to Other",
                "label_fragmentation": "All agents partially correct but labels differ",
            }
            for ftype in [
                "unanimous_wrong",
                "correct_minority_suppressed",
                "majority_wrong",
                "all_empty_cascade",
                "label_fragmentation",
            ]:
                count = type_totals.get(ftype, 0)
                desc = descriptions.get(ftype, "")
                lines.append(f"| {ftype} | {count} | {desc} |")
            lines.append("")

            # Per-experiment breakdown
            lines.append("### Per-Experiment Breakdown\n")
            lines.append("| Experiment | Unanimous Wrong | Minority Suppressed | Majority Wrong | Empty Cascade | Fragmentation |")
            lines.append("|---|---|---|---|---|---|")
            for exp_id in sorted(taxonomy.keys()):
                types = taxonomy[exp_id]
                row = [
                    exp_id,
                    str(len(types.get("unanimous_wrong", []))),
                    str(len(types.get("correct_minority_suppressed", []))),
                    str(len(types.get("majority_wrong", []))),
                    str(len(types.get("all_empty_cascade", []))),
                    str(len(types.get("label_fragmentation", []))),
                ]
                lines.append("| " + " | ".join(row) + " |")
            lines.append("")

        # Agreement entropy summary
        entropies = vote_analysis.get("agreement_entropies", {})
        if entropies:
            lines.append("### Agreement Entropy\n")
            lines.append(
                "Shannon entropy of vote distribution per document. "
                "Higher = more agent disagreement.\n"
            )
            lines.append("| Experiment | Mean Entropy (correct) | Mean Entropy (incorrect) | Delta |")
            lines.append("|---|---|---|---|")
            for exp_id in sorted(entropies.keys()):
                items = entropies[exp_id]
                correct_e = [x["entropy"] for x in items if x["correct"]]
                incorrect_e = [x["entropy"] for x in items if not x["correct"]]
                mean_c = sum(correct_e) / len(correct_e) if correct_e else 0
                mean_i = sum(incorrect_e) / len(incorrect_e) if incorrect_e else 0
                delta = mean_i - mean_c
                lines.append(
                    f"| {exp_id} | {mean_c:.3f} | {mean_i:.3f} | {delta:+.3f} |"
                )
            lines.append("")

        # Per-agent reliability
        reliability = vote_analysis.get("per_agent_reliability", {})
        if reliability:
            lines.append("### Per-Agent Reliability\n")
            lines.append(
                "Fraction of documents where each agent position contributes at least one correct label.\n"
            )
            lines.append("| Experiment | Agent 0 | Agent 1 | Agent 2 |")
            lines.append("|---|---|---|---|")
            for exp_id in sorted(reliability.keys()):
                data = reliability[exp_id]
                cols = [exp_id]
                for i in range(3):
                    correct = data.get(f"agent_{i}_correct", 0)
                    total = data.get(f"agent_{i}_total", 0)
                    if total > 0:
                        cols.append(f"{correct}/{total} ({correct/total*100:.0f}%)")
                    else:
                        cols.append("N/A")
                lines.append("| " + " | ".join(cols) + " |")
            lines.append("")
    else:
        lines.append("## 7. Vote-Level Failure Taxonomy (Phase 2)\n")
        lines.append(
            "*No votes/ directories found. Run experiments with `enable_vote_saving: true` "
            "to enable Phase 2 analysis.*\n"
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JSON output builder
# ---------------------------------------------------------------------------


def build_json_output(
    agora_experiments: List[Dict],
    all_evaluations: Dict[str, Dict],
    cross_agg_results: List[Dict],
    cross_model_results: Dict,
    other_inflation: Dict,
    confusion_results: Dict,
    vote_analysis: Optional[Dict],
) -> Dict[str, Any]:
    """Build JSON-serializable output dict."""

    # Convert DocumentError objects in evaluations
    serializable_evals = {}
    for exp_id, eval_data in all_evaluations.items():
        exp_copy = {
            "experiment_id": eval_data.get("experiment_id"),
            "aggregation_method": eval_data.get("aggregation_method"),
            "n_runs": eval_data.get("n_runs"),
            "consensus_narrative": eval_data.get("consensus_narrative"),
            "consensus_subnarrative": eval_data.get("consensus_subnarrative"),
            "per_run_stats": [],
        }
        for run in eval_data.get("runs", []):
            run_stats = {k: v for k, v in run.items() if k != "documents"}
            # Add per-document error summaries for the first run only (to limit size)
            exp_copy["per_run_stats"].append(run_stats)

        # Add first run document details
        if eval_data.get("runs"):
            first_run_docs = {}
            for file_id, doc in eval_data["runs"][0].get("documents", {}).items():
                first_run_docs[file_id] = doc.to_dict()
            exp_copy["run_1_documents"] = first_run_docs

        serializable_evals[exp_id] = exp_copy

    # Convert cross-agg tuples
    serializable_cross_agg = []
    for comp in cross_agg_results:
        comp_copy = dict(comp)
        comp_copy["group_key"] = list(comp["group_key"])
        # Remove per_document (too large) — keep summary fields
        comp_copy.pop("per_document", None)
        serializable_cross_agg.append(comp_copy)

    # Convert confusion Counter objects
    serializable_confusion = {
        "top_20_narrative_confusions": [
            {"ground_truth": gt, "false_positive": fp, "count": c}
            for (gt, fp), c in confusion_results.get("top_20_narrative_confusions", [])
        ],
        "top_20_subnarrative_confusions": [
            {"ground_truth": gt, "false_positive": fp, "count": c}
            for (gt, fp), c in confusion_results.get(
                "top_20_subnarrative_confusions", []
            )
        ],
    }

    return {
        "generated_at": datetime.now().isoformat(),
        "n_experiments": len(agora_experiments),
        "evaluations": serializable_evals,
        "other_inflation": other_inflation,
        "cross_aggregation": serializable_cross_agg,
        "cross_model_hard_documents": cross_model_results,
        "narrative_confusions": serializable_confusion,
        "vote_analysis": vote_analysis,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Voting failure analysis for multi-agent (Agora) experiments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--experiments-dir",
        default="results/experiments/",
        help="Root directory containing experiment results",
    )
    parser.add_argument(
        "--ground-truth-dir",
        default="data/dev-documents_4_December",
        help="Root directory containing ground truth files",
    )
    parser.add_argument(
        "--output",
        default="results/analysis/voting_failure_report.md",
        help="Output Markdown report path",
    )
    parser.add_argument(
        "--json-output",
        default="results/analysis/voting_failure_report.json",
        help="Output JSON data path",
    )
    parser.add_argument(
        "--languages",
        nargs="+",
        help="Filter by language(s), e.g. EN BG",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        help="Filter by model keyword(s), e.g. deepseek mistral",
    )
    args = parser.parse_args()

    print("=== Voting Failure Analysis ===\n")

    # 1. Discover agora experiments
    print("1. Discovering agora experiments...")
    agora_experiments = discover_agora_experiments(args.experiments_dir)
    print(f"   Found {len(agora_experiments)} agora experiments")

    # 2. Apply filters
    if args.languages:
        langs = {l.upper() for l in args.languages}
        agora_experiments = [
            e for e in agora_experiments if e["meta"].get("language") in langs
        ]
        print(f"   After language filter: {len(agora_experiments)}")
    if args.models:
        model_kws = [m.lower() for m in args.models]
        agora_experiments = [
            e
            for e in agora_experiments
            if any(kw in e["experiment_id"].lower() for kw in model_kws)
        ]
        print(f"   After model filter: {len(agora_experiments)}")

    if not agora_experiments:
        print("No agora experiments found. Exiting.")
        return

    # 3. Evaluate each experiment at document level
    print("\n2. Evaluating experiments at document level...")
    all_evaluations = {}
    for i, exp in enumerate(agora_experiments, 1):
        exp_id = exp["experiment_id"]
        print(f"   [{i}/{len(agora_experiments)}] {exp_id}")
        result = evaluate_experiment_documents(exp, args.ground_truth_dir)
        all_evaluations[exp_id] = result

    # 4. Group by (model, lang, temp) for cross-aggregation
    print("\n3. Running cross-aggregation analysis...")
    by_group = defaultdict(list)
    for exp in agora_experiments:
        by_group[exp["group_key"]].append(exp)
    cross_agg = cross_aggregation_analysis(by_group, all_evaluations)
    multi_agg_groups = [g for g in by_group.values() if len(g) >= 2]
    print(f"   Found {len(multi_agg_groups)} groups with multiple aggregation methods")

    # 5. Cross-model consensus failures
    print("\n4. Finding cross-model consensus failures...")
    cross_model = cross_model_consensus_failures(all_evaluations, agora_experiments)
    for lang, data in cross_model.items():
        print(f"   {lang}: {data['n_hard']} hard documents (across {data['n_experiments']} experiments)")

    # 6. Other inflation
    print("\n5. Computing 'Other' inflation...")
    other_infl = other_inflation_analysis(all_evaluations)

    # 7. Narrative confusion
    print("\n6. Analyzing narrative confusion patterns...")
    confusion = narrative_confusion_analysis(all_evaluations)
    top = confusion.get("top_20_narrative_confusions", [])
    if top:
        print(f"   Top confusion: {top[0][0]} ({top[0][1]} times)")

    # 8. Phase 2: vote-level analysis
    print("\n7. Checking for Phase 2 vote data...")
    vote_analysis = try_vote_level_analysis(agora_experiments, args.ground_truth_dir)

    # 9. Generate report
    print("\n8. Generating report...")
    report = generate_report(
        agora_experiments,
        all_evaluations,
        cross_agg,
        cross_model,
        other_infl,
        confusion,
        vote_analysis,
    )

    # 10. Write outputs
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"   Markdown report: {args.output}")

    json_data = build_json_output(
        agora_experiments,
        all_evaluations,
        cross_agg,
        cross_model,
        other_infl,
        confusion,
        vote_analysis,
    )
    os.makedirs(os.path.dirname(args.json_output) or ".", exist_ok=True)
    with open(args.json_output, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print(f"   JSON data: {args.json_output}")

    print("\nDone!")


if __name__ == "__main__":
    main()

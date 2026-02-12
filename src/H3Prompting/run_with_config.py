"""
Main script to run the classification system with configuration files.
"""

import argparse
import asyncio
import sys
import time
import warnings

# Suppress coroutine warnings from LangChain internals
warnings.filterwarnings("ignore", message="coroutine .* was never awaited")
warnings.filterwarnings("ignore", category=RuntimeWarning, module="langchain")
from pathlib import Path
from typing import cast, Optional

from dotenv import load_dotenv

from config_loader import ClassificationConfig, create_example_config
from cost_tracker import CostTracker
from fuzzy_label_matcher import get_narrative_matcher, get_subnarrative_matcher, reset_matchers
from graph_builder import build_graph_from_config
from utils import get_unprocessed_texts
from state import ClassificationState

load_dotenv()

async def run_classification(config_path: str, cost_tracker: Optional[CostTracker] = None) -> Optional[CostTracker]:
    """
    Run the classification system with a configuration file.

    Args:
        config_path: Path to the YAML configuration file
        cost_tracker: Optional CostTracker instance for tracking metrics

    Returns:
        CostTracker instance with recorded metrics (if cost tracking enabled)
    """
    print(f"[Main] Loading configuration from: {config_path}")

    try:
        # Reset fuzzy matchers at the start of each experiment
        reset_matchers()

        print(f"[Main] Building graph with configuration...")
        graph, execution_config, config = build_graph_from_config(config_path)
        print(f"[Main] Graph compiled successfully")

        # Initialize cost tracker if enabled and not provided
        if config.enable_cost_tracking and cost_tracker is None:
            cost_tracker = CostTracker(
                experiment_id=config.experiment_id or "default",
                config_name=Path(config_path).stem,
                model_name=config.model_name,
                num_narrative_agents=config.num_narrative_agents,
                num_subnarrative_agents=config.num_subnarrative_agents,
                aggregation_method=config.narrative_aggregation_method,
                enable_validation=config.enable_validation,
                enable_retrieval=config.enable_retrieval,
            )
            print(f"[Main] Cost tracking enabled")

        print(f"[Main] Loading texts from: {config.input_folder}")
        text_list, file_names = get_unprocessed_texts(config.input_folder, config.output_file)

        if not text_list:
            print(f"[Main] No unprocessed text files found in {config.input_folder}")
            if Path(config.output_file).exists():
                print(f"[Main] All files appear to have been processed already")
            else:
                print(f"[Main] No text files found at all in the input folder")
            return cost_tracker

        initial_states_batch = [
            {"text": text, "file_id": file_id}
            for text, file_id in zip(text_list, file_names)
        ]

        print(f"[Main] Processing {len(initial_states_batch)} files...")
        print(f"[Main] Output will be appended to: {config.output_file}")

        output_path = Path(config.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Track timing for each document if cost tracking is enabled
        start_time = time.perf_counter()

        # Type cast for compatibility - runtime behavior is correct
        typed_states = cast(list[ClassificationState], initial_states_batch)

        # Limit concurrent document processing to avoid API rate limits
        # (max_concurrency controls node-level parallelism within a graph,
        #  but we also need to limit how many documents run simultaneously)
        doc_concurrency = config.max_concurrency or 5
        semaphore = asyncio.Semaphore(doc_concurrency)

        async def process_with_semaphore(state):
            async with semaphore:
                return await graph.ainvoke(state, config=execution_config)

        tasks = [process_with_semaphore(state) for state in typed_states]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Check for and log any errors
        errors = [r for r in results if isinstance(r, Exception)]
        if errors:
            print(f"[Main] WARNING: {len(errors)} of {len(results)} tasks failed")
            for i, err in enumerate(errors[:3]):  # Show first 3 errors
                print(f"[Main] Error {i+1}: {type(err).__name__}: {err}")

        end_time = time.perf_counter()
        total_latency_ms = (end_time - start_time) * 1000

        # Record metrics if cost tracking is enabled
        if cost_tracker:
            # Estimate API calls based on config
            calls_per_doc = 1  # category
            calls_per_doc += max(1, config.num_narrative_agents)  # narratives
            calls_per_doc += max(1, config.num_subnarrative_agents)  # subnarratives
            if config.enable_validation:
                calls_per_doc += 2  # validation calls

            for file_id in file_names:
                cost_tracker.start_document(file_id)
                # Record estimated API call (we don't have actual token counts from LangChain)
                cost_tracker.record_api_call(
                    model=config.model_name,
                    node_type="combined",
                    operation="classification",
                    input_tokens=2000 * calls_per_doc,  # Estimate
                    output_tokens=500 * calls_per_doc,  # Estimate
                    latency_ms=total_latency_ms / len(file_names),
                )
                cost_tracker.end_document()

        print(f"[Main] Classification completed successfully!")
        print(f"[Main] Results saved to: {config.output_file}")

        # Save cost metrics if tracking was enabled
        if cost_tracker and config.enable_cost_tracking:
            cost_metrics_path = output_path.parent / "cost_metrics.json"
            cost_tracker.save(str(cost_metrics_path))
            print(f"[Main] Cost metrics saved to: {cost_metrics_path}")
            summary = cost_tracker.get_summary()
            print(f"[Main] Cost summary: {summary['total_api_calls']} calls, ${summary['total_cost_usd']:.4f}, {summary['total_latency_sec']:.2f}s")

        # Save fuzzy matching tracking if enabled
        if config.enable_fuzzy_matching:
            from label_info import flatten_taxonomy, load_taxonomy
            taxonomy = load_taxonomy()
            flat_narratives, flat_subnarratives = flatten_taxonomy(taxonomy)

            # Get the matchers (they were used during graph execution)
            narrative_matcher = get_narrative_matcher(flat_narratives, config.fuzzy_threshold)
            subnarrative_matcher = get_subnarrative_matcher(flat_subnarratives, config.fuzzy_threshold)

            # Determine save path
            if config.fuzzy_tracking_path:
                fuzzy_path = Path(config.fuzzy_tracking_path)
            else:
                fuzzy_path = output_path.parent / "fuzzy_matching.json"

            # Combine tracking data
            import json
            combined_tracking = {
                "config": {
                    "model_name": config.model_name,
                    "fuzzy_threshold": config.fuzzy_threshold,
                    "experiment_id": config.experiment_id,
                    "run_id": config.run_id
                },
                "narrative_matching": narrative_matcher.tracker.get_summary(),
                "narrative_matches": narrative_matcher.tracker.matches,
                "subnarrative_matching": subnarrative_matcher.tracker.get_summary(),
                "subnarrative_matches": subnarrative_matcher.tracker.matches
            }

            fuzzy_path.parent.mkdir(parents=True, exist_ok=True)
            with open(fuzzy_path, 'w', encoding='utf-8') as f:
                json.dump(combined_tracking, f, indent=2)

            print(f"[Main] Fuzzy matching tracking saved to: {fuzzy_path}")
            nar_summary = narrative_matcher.tracker.get_summary()
            sub_summary = subnarrative_matcher.tracker.get_summary()
            print(f"[Main] Narrative fuzzy matching: {nar_summary['matched']}/{nar_summary['total']} matched ({nar_summary['match_rate']*100:.1f}%)")
            print(f"[Main] Subnarrative fuzzy matching: {sub_summary['matched']}/{sub_summary['total']} matched ({sub_summary['match_rate']*100:.1f}%)")

        return cost_tracker

    except Exception as e:
        print(f"[Main] Error during classification: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run text classification with configuration file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_with_config.py --create-example-config my_config.yaml
  python run_with_config.py --config my_config.yaml
  python run_with_config.py --config experiment1.yaml experiment2.yaml experiment3.yaml
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--config", 
        type=str, 
        nargs="+",
        help="Path(s) to YAML configuration file(s)"
    )
    group.add_argument(
        "--create-example-config", 
        type=str, 
        metavar="OUTPUT_PATH",
        help="Create an example configuration file at the specified path"
    )
    
    args = parser.parse_args()
    
    if args.create_example_config:
        create_example_config(args.create_example_config)
        print(f"Example configuration created at: {args.create_example_config}")
        print("Edit the configuration file and run with --config to start classification.")
        return
    
    for config_path in args.config:
        config_path = Path(config_path)
        
        if not config_path.exists():
            print(f"[Error] Configuration file not found: {config_path}")
            sys.exit(1)
        
        print(f"\n{'='*60}")
        print(f"Running experiment with config: {config_path.name}")
        print(f"{'='*60}")
        
        try:
            asyncio.run(run_classification(str(config_path)))
        except KeyboardInterrupt:
            print(f"\n[Main] Interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"[Error] Failed to run experiment with {config_path}: {e}")
            continue
        
        print(f"{'='*60}")
        print(f"Completed experiment: {config_path.name}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()

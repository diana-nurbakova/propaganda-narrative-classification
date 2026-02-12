import json
from pathlib import Path
from typing import List
from schema import Narrative, Subnarrative
from state import ClassificationState


def create_other_narrative(reasoning: str = "N/A") -> Narrative:
    """
    Create an 'Other' narrative placeholder.
    
    Args:
        reasoning: Explanation for why this is classified as 'Other'
        
    Returns:
        Narrative object with 'Other' classification
    """
    return Narrative(
        narrative_name="Other",
        evidence_quote="N/A",
        reasoning=reasoning
    )


def create_other_subnarrative(reasoning: str = "N/A") -> Subnarrative:
    """
    Create an 'Other' subnarrative placeholder.
    
    Args:
        reasoning: Explanation for why this is classified as 'Other'
        
    Returns:
        Subnarrative object with 'Other' classification
    """
    return Subnarrative(
        subnarrative_name="Other",
        evidence_quote="N/A",
        reasoning=reasoning
    )


def write_classification_results(file_id: str, narratives: List[Narrative], 
                               subnarratives: List[Subnarrative], output_file: str) -> None:
    """
    Write classification results to a TSV file.
    
    Args:
        file_id: Identifier for the file being processed
        narratives: List of classified narratives
        subnarratives: List of classified subnarratives
        output_file: Path to the output file
    """
    narrative_names = [n.narrative_name for n in narratives]
    subnarrative_names = [sn.subnarrative_name for sn in subnarratives]
    
    narratives_str = ";".join(narrative_names) if narrative_names else "Other"
    subnarratives_str = ";".join(subnarrative_names) if subnarrative_names else "Other"
    
    output_line = f"{file_id}\t{narratives_str}\t{subnarratives_str}\n"
    
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(output_line)


def write_evidence_json(file_id: str, narratives: List[Narrative],
                        subnarratives: List[Subnarrative], output_file: str) -> None:
    """
    Save evidence quotes and reasoning to a JSON sidecar file.

    Creates an evidence/ directory alongside the results file and writes
    one JSON file per document containing the full structured output
    (label names, evidence quotes, reasoning).

    Args:
        file_id: Identifier for the file being processed
        narratives: List of classified narratives (with evidence_quote, reasoning)
        subnarratives: List of classified subnarratives (with evidence_quote, reasoning)
        output_file: Path to the main results TSV (used to locate the output directory)
    """
    evidence_dir = Path(output_file).parent / "evidence"
    evidence_dir.mkdir(exist_ok=True)

    record = {
        "file_id": file_id,
        "narratives": [
            {
                "narrative_name": n.narrative_name,
                "evidence_quote": getattr(n, "evidence_quote", ""),
                "reasoning": getattr(n, "reasoning", ""),
            }
            for n in narratives
        ],
        "subnarratives": [
            {
                "subnarrative_name": s.subnarrative_name,
                "evidence_quote": getattr(s, "evidence_quote", ""),
                "reasoning": getattr(s, "reasoning", ""),
            }
            for s in subnarratives
        ],
    }

    evidence_file = evidence_dir / f"{file_id}.json"
    with open(evidence_file, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)


def write_votes_json(
    file_id: str,
    multi_agent_narratives: List,
    multi_agent_subnarratives: List,
    num_narrative_agents: int,
    num_subnarrative_agents: int,
    narrative_aggregation_method: str,
    subnarrative_aggregation_method: str,
    aggregated_narratives: List,
    aggregated_subnarratives: List,
    output_file: str,
    narrative_agent_metadata: List = None,
    subnarrative_agent_metadata: List = None,
    narrative_fuzzy_matches: List = None,
    subnarrative_fuzzy_matches: List = None,
) -> None:
    """
    Save per-agent votes to a JSON sidecar file before aggregation.

    Creates a votes/ directory alongside the results file and writes
    one JSON file per document containing the raw per-agent predictions
    alongside the final aggregated result, agent failure metadata,
    and fuzzy match corrections.

    Args:
        file_id: Document identifier
        multi_agent_narratives: List of narrative lists, one per agent
        multi_agent_subnarratives: Flat list of all subnarratives from all agents
        num_narrative_agents: Number of narrative classification agents
        num_subnarrative_agents: Number of subnarrative classification agents
        narrative_aggregation_method: Aggregation strategy for narratives
        subnarrative_aggregation_method: Aggregation strategy for subnarratives
        aggregated_narratives: Final aggregated narrative objects
        aggregated_subnarratives: Final aggregated subnarrative objects
        output_file: Path to the main results TSV (used to derive votes/ dir)
        narrative_agent_metadata: Per-agent success/failure metadata for narratives
        subnarrative_agent_metadata: Per-agent success/failure metadata for subnarratives
        narrative_fuzzy_matches: Fuzzy match corrections applied to narratives
        subnarrative_fuzzy_matches: Fuzzy match corrections applied to subnarratives
    """
    votes_dir = Path(output_file).parent / "votes"
    votes_dir.mkdir(exist_ok=True)

    def _serialize_narrative(n):
        return {
            "narrative_name": getattr(n, "narrative_name", str(n)),
            "evidence_quote": getattr(n, "evidence_quote", ""),
            "reasoning": getattr(n, "reasoning", ""),
        }

    def _serialize_subnarrative(s):
        return {
            "subnarrative_name": getattr(s, "subnarrative_name", str(s)),
            "evidence_quote": getattr(s, "evidence_quote", ""),
            "reasoning": getattr(s, "reasoning", ""),
        }

    # Per-agent narrative votes with evidence (structured as list of lists)
    narrative_votes = []
    narrative_votes_labels = []
    for agent_results in multi_agent_narratives:
        narrative_votes.append([_serialize_narrative(n) for n in agent_results])
        narrative_votes_labels.append(
            [getattr(n, "narrative_name", str(n)) for n in agent_results]
        )

    # Subnarratives: stored as flat list with evidence (pipeline flattens before aggregation)
    subnarrative_all = []
    subnarrative_labels = []
    if multi_agent_subnarratives and multi_agent_subnarratives[0]:
        subnarrative_all = [
            _serialize_subnarrative(s) for s in multi_agent_subnarratives[0]
        ]
        subnarrative_labels = [
            getattr(s, "subnarrative_name", str(s))
            for s in multi_agent_subnarratives[0]
        ]

    record = {
        "file_id": file_id,
        "num_narrative_agents": num_narrative_agents,
        "num_subnarrative_agents": num_subnarrative_agents,
        "narrative_votes": narrative_votes_labels,
        "narrative_votes_with_evidence": narrative_votes,
        "subnarrative_votes_flat": subnarrative_labels,
        "subnarrative_votes_flat_with_evidence": subnarrative_all,
        "narrative_aggregation_method": narrative_aggregation_method,
        "subnarrative_aggregation_method": subnarrative_aggregation_method,
        "aggregated_narratives": [
            getattr(n, "narrative_name", str(n)) for n in aggregated_narratives
        ],
        "aggregated_subnarratives": [
            getattr(s, "subnarrative_name", str(s)) for s in aggregated_subnarratives
        ],
        "narrative_agent_metadata": narrative_agent_metadata or [],
        "subnarrative_agent_metadata": subnarrative_agent_metadata or [],
        "narrative_fuzzy_matches": narrative_fuzzy_matches or [],
        "subnarrative_fuzzy_matches": subnarrative_fuzzy_matches or [],
    }

    vote_file = votes_dir / f"{file_id}.json"
    with open(vote_file, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)


def route_after_category(state) -> str:
    """
    Determines the next step after category classification.
    
    Args:
        state: Current classification state
        
    Returns:
        Next node name to execute
    """
    category = state.get("category")
    
    if category == "Other":
        return "handle_other_category"
    else:
        return "narratives"

def route_after_narrative_validation(state: ClassificationState) -> str:
    """
    Determines the next step after validation.
    - If approved or max retries reached, proceed.
    - Otherwise, loop back to the actor for a retry.
    """
    feedback = state.get("narrative_validation_feedback")
    retry_count = state.get("narrative_retry_count", 0)

    max_attempts = 2  # Limit to 2 retries for now

    if feedback == "approved" or retry_count >= max_attempts:  # Limit to 2 retries for now
        if retry_count >= max_attempts and feedback != "approved":
            print("[graph] ROUTER: Max retries reached. Proceeding with last attempt.")
        return "clean_narratives"
    else:
        print("[graph] ROUTER: Retrying narrative classification.")
        return "narratives"


def route_after_narratives_classification(state: ClassificationState) -> str:
    """
    Determines the next step after narrative classification.
    - If narratives list is empty after classification, go to handle_empty_narratives
    - Otherwise, proceed to validation
    """
    narratives = state.get("narratives", [])
    
    if not narratives:
        print("[graph] ROUTER: No narratives classified. Going to handle_empty_narratives.")
        return "handle_empty_narratives"
    else:
        return "validate_narratives"


def route_after_narratives_cleaning(state: ClassificationState) -> str:
    """
    Determines the next step after narrative cleaning.
    - If narratives list is empty after cleaning, go to handle_empty_narratives
    - Otherwise, proceed to subnarratives classification
    """
    narratives = state.get("narratives", [])
    
    if not narratives:
        print("[graph] ROUTER: No narratives after cleaning. Going to handle_empty_narratives.")
        return "handle_empty_narratives"
    else:
        return "subnarratives"

def route_after_subnarrative_validation(state: ClassificationState) -> str:
    """
    Determines the next step after subnarrative validation.
    """
    feedback = state.get("subnarrative_validation_feedback")
    retry_count = state.get("subnarrative_retry_count", 0)
    
    # We'll limit it to one retry for now
    if feedback == "approved" or retry_count >= 1:
        if retry_count >= 1 and feedback != "approved":
            print("[graph] ROUTER: Max retries for subnarratives reached. Proceeding.")
        else:
            print("[graph] ROUTER: Subnarrative validation approved. Proceeding.")
        return "clean_subnarratives"
    else:
        print("[graph] ROUTER: Retrying subnarrative classification.")
        return "subnarratives"
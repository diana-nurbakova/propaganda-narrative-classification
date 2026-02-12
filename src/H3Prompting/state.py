from typing import Any, Dict, List, NotRequired, TypedDict


class ClassificationState(TypedDict):
    """State schema for text classification workflow"""
    text: str
    cleaned_text: NotRequired[str]
    category: NotRequired[str]
    narratives: NotRequired[List[Any]]
    subnarratives: NotRequired[List[Any]]
    file_id: str

    # Multi-agent classification results
    multi_agent_narratives: NotRequired[List[List[Any]]]  # Results from n agents
    multi_agent_subnarratives: NotRequired[List[List[Any]]]  # Results from n agents

    # Validation state fields
    narrative_validation_feedback: NotRequired[str]
    narrative_retry_count: NotRequired[int]

    subnarrative_validation_feedback: NotRequired[str]
    subnarrative_retry_count: NotRequired[int]

    # Fuzzy match tracking (for analysis of model label variations)
    narrative_fuzzy_matches: NotRequired[List[Dict[str, Any]]]
    subnarrative_fuzzy_matches: NotRequired[List[Dict[str, Any]]]
    num_subnarrative_agents: NotRequired[int]  # Track number of agents for aggregation

    # Per-agent metadata for voting failure analysis
    # Each entry: {"agent_id": int, "status": "success"|"failure", "error_type": str, "error_message": str}
    narrative_agent_metadata: NotRequired[List[Dict[str, Any]]]
    subnarrative_agent_metadata: NotRequired[List[Dict[str, Any]]]

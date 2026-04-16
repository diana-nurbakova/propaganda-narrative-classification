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

    # ------------------------------------------------------------------
    # EMNLP revision additions (specs/agora_emnlp_spec.md)
    # ------------------------------------------------------------------

    # ToM Stage 1: cached per-document Theory-of-Mind analysis. The
    # downstream classification, arbitration and disambiguation nodes all
    # read from this single cached value so the LLM call only runs once.
    # Schema: {"presuppositions": [...], "intent": str,
    #          "target_belief_change": str, "primary_mechanism": str}
    tom_analysis: NotRequired[Dict[str, Any]]

    # Whether the multi-agent narratives produced disagreement on at least
    # one label after aggregation. Set by aggregate_multi_agent_narratives()
    # so the routing function can decide whether to invoke ToM arbitration.
    narrative_disagreement_detected: NotRequired[bool]
    narrative_disagreement_labels: NotRequired[List[str]]

    # Outcome of the disambiguation pass: list of (label, kept) decisions.
    disambiguation_decisions: NotRequired[List[Dict[str, Any]]]

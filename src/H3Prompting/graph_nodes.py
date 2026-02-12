"""
Node functions for the LangGraph classification pipeline.
Extracted from graph.py for better code organization and readability.
"""

import asyncio
import json
import warnings

# Suppress coroutine warnings from LangChain internals
warnings.filterwarnings("ignore", message="coroutine .* was never awaited")
warnings.filterwarnings("ignore", category=RuntimeWarning, module="langchain")
from typing import Any, List
from langchain_core.messages import SystemMessage, HumanMessage
from extract import extract_category
from prompt_template import create_category_system_prompt, create_narrative_critic_prompt, create_narrative_refinement_prompt, create_narrative_system_prompt, create_subnarrative_critic_prompt, create_subnarrative_refinement_prompt, create_subnarrative_system_prompt, create_cleaning_system_prompt
from schema import NarrativeClassificationOutput, Subnarrative, SubnarrativeClassificationOutput, ValidationResult
from graph_utils import create_other_narrative, create_other_subnarrative, write_classification_results, write_evidence_json, write_votes_json
from utils import get_narratives_for_category, get_subnarratives_for_narrative
from structured_output_helper import get_structured_llm
from fuzzy_label_matcher import FuzzyLabelMatcher, get_narrative_matcher, get_subnarrative_matcher


# Retry configuration for rate-limited APIs (like Mistral)
MAX_RETRIES = 8
INITIAL_BACKOFF_SECONDS = 5.0
MAX_BACKOFF_SECONDS = 120.0


def _classify_error(e: Exception) -> str:
    """Classify an exception into a short error type string for metadata."""
    error_str = str(e).lower()
    if "429" in str(e) or "rate" in error_str or "quota" in error_str:
        return "rate_limit"
    if "timeout" in error_str or "timed out" in error_str:
        return "timeout"
    if "connection" in error_str or "disconnected" in error_str:
        return "connection"
    if any(code in str(e) for code in ["500", "502", "503", "504"]):
        return "server_error"
    if "content" in error_str and "filter" in error_str:
        return "content_filter"
    if "parse" in error_str or "json" in error_str or "validation" in error_str:
        return "parse_error"
    return "unknown"


async def invoke_with_retry(llm, messages, agent_id: str = ""):
    """
    Invoke an LLM with exponential backoff retry for transient errors.

    Retries on:
    - Rate limit errors (429)
    - Connection errors (server disconnects, timeouts)
    - Server errors (500, 502, 503, 504)

    Args:
        llm: The LLM instance (must support ainvoke)
        messages: Messages to send
        agent_id: Optional identifier for logging

    Returns:
        LLM response

    Raises:
        Exception if all retries fail
    """
    backoff = INITIAL_BACKOFF_SECONDS
    last_exception = None

    for attempt in range(MAX_RETRIES):
        try:
            return await llm.ainvoke(messages)
        except Exception as e:
            error_str = str(e).lower()

            # Check for retryable errors
            is_rate_limit = "429" in str(e) or "rate" in error_str or "quota" in error_str
            is_connection_error = (
                "connecterror" in error_str or
                "connection" in error_str or
                "disconnected" in error_str or
                "timeout" in error_str or
                "timed out" in error_str or
                "server disconnected" in error_str
            )
            is_server_error = any(code in str(e) for code in ["500", "502", "503", "504"])

            is_retryable = is_rate_limit or is_connection_error or is_server_error

            if not is_retryable or attempt == MAX_RETRIES - 1:
                raise  # Re-raise if not retryable or final attempt

            last_exception = e
            wait_time = min(backoff * (2 ** attempt), MAX_BACKOFF_SECONDS)
            error_type = "Rate limit" if is_rate_limit else ("Connection error" if is_connection_error else "Server error")
            print(f"[graph] {agent_id}{error_type} (attempt {attempt + 1}/{MAX_RETRIES}), waiting {wait_time:.1f}s...")
            await asyncio.sleep(wait_time)

    raise last_exception


def clean_text_node(state, llm) -> dict:
    """Clean raw web text by removing UI noise and boilerplate using an LLM."""
    raw_text = state["text"]
    print("[graph] Starting text cleaning node")
    system_prompt = create_cleaning_system_prompt()
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=raw_text)]
    response = llm.invoke(messages)
    cleaned = (response.content or "").strip()
    print(f"[graph] Text cleaning complete (length in/out: {len(raw_text)} -> {len(cleaned)})")
    return {"cleaned_text": cleaned}


def classify_category_node(state, llm) -> dict:
    """
    Node function that classifies text into categories using the category prompt template.
    
    Args:
        state: Current state containing the text to classify
        llm: The language model instance
        
    Returns:
        Dictionary with the classification result
    """
    text = state.get("cleaned_text", state["text"])  # use cleaned text if available
    print("[graph] Starting category classification node")
    
    system_prompt = create_category_system_prompt()
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=text)
    ]
    
    response = llm.invoke(messages)
    category = extract_category(response.content)
    
    print(f"[graph] Category classification complete -> {category}")
    return {"category": category}


def handle_other_category_node(state) -> dict:
    """
    Handles the case where the category is 'Other'.
    Sets narratives and subnarratives to ['Other'] to bypass the main pipeline.
    """
    print("[graph] Category is 'Other', taking shortcut.")
    
    other_narrative = create_other_narrative("Category is Other")
    other_subnarrative = create_other_subnarrative("Category is Other")
    
    return {
        "narratives": [other_narrative],
        "subnarratives": [other_subnarrative]
    }


def classify_narratives_node(state, llm, model_name: str = "") -> dict:
    """
    Node function that classifies text into narratives for a given category.

    Args:
        state: Current state containing text and category
        llm: The language model instance
        model_name: The model name for structured output handling

    Returns:
        Dictionary with the narrative classification results
    """
    text = state.get("cleaned_text", state["text"])  # use cleaned text if available
    category = state["category"]
    retry_count = state.get("narrative_retry_count", 0)
    feedback = state.get("narrative_validation_feedback", "")

    print(f"[graph] Starting narratives classification node for category {category}")

    base_system_prompt = create_narrative_system_prompt(category)

    if feedback and feedback != "approved":
        system_prompt = create_narrative_refinement_prompt(base_system_prompt, feedback)
    else:
        system_prompt = base_system_prompt


    structured_llm = get_structured_llm(llm, NarrativeClassificationOutput, model_name)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=text)
    ]

    response_obj = structured_llm.invoke(messages)
    narratives_with_details = response_obj.narratives if response_obj.narratives else []
    narrative_names = [n.narrative_name for n in narratives_with_details]

    print(f"[graph] Narratives classification complete -> {narrative_names}")
    return {"narratives": narratives_with_details, "narrative_retry_count": retry_count + 1}

def handle_empty_narratives_node(state) -> dict:
    """
    Handles the case where no narratives were classified.
    Sets subnarratives to empty list for proper handling in write_results.
    """
    print("[graph] No narratives classified, setting empty subnarratives.")
    
    return {
        "subnarratives": []
    }

def validate_narratives_node(state, llm, taxonomy, model_name: str = "") -> dict:
    """
    The 'Critic' node. It validates the narratives classified by the actor.
    """
    print("[graph] CRITIC: Validating classified narratives...")
    text = state.get("cleaned_text", state["text"])  # use cleaned text if available
    narratives_analysis = state["narratives"]
    category = state["category"]

    potential_narratives = get_narratives_for_category(taxonomy, category)

    if not narratives_analysis:
        print("[graph] CRITIC: No narratives to validate. Approving.")
        return {"narrative_validation_feedback": "approved"}

    system_prompt = create_narrative_critic_prompt(potential_narratives)

    human_prompt = (
        f"ORIGINAL TEXT:\n---\n{text}\n---\n\n"
        f"CLASSIFICATION ANALYSIS TO VALIDATE:\n---\n{json.dumps([n.dict() for n in narratives_analysis], indent=2)}\n---"
    )

    messages = [SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)]

    critic_llm = get_structured_llm(llm, ValidationResult, model_name)
    verdict = critic_llm.invoke(messages)

    if verdict.is_valid:
        print(f"[graph] CRITIC: Validation successful.")
        return {"narrative_validation_feedback": "approved"}
    else:
        print(f"[graph] CRITIC: Validation failed.")
        return {"narrative_validation_feedback": verdict.feedback}


def clean_narratives_node(state, flat_narratives, enable_fuzzy: bool = True,
                          fuzzy_threshold: float = 70.0) -> dict:
    """
    Node function that filters narratives to only include valid ones.
    Supports fuzzy matching for models that return semantically similar but not exact labels.

    Args:
        state: Current state containing narratives to clean
        flat_narratives: List of valid narrative names
        enable_fuzzy: Whether to use fuzzy matching for non-exact labels
        fuzzy_threshold: Minimum score (0-100) for fuzzy match acceptance

    Returns:
        Dictionary with cleaned narratives and optional fuzzy match details
    """
    narratives = state["narratives"]
    file_id = state.get("file_id", "unknown")

    if not narratives:
        print("[graph] No narratives to clean. Skipping.")
        other_placeholder = create_other_narrative("No valid narratives were provided to this node.")
        return {"narratives": [other_placeholder]}

    print("[graph] Cleaning narratives" + (" (with fuzzy matching)" if enable_fuzzy else ""))

    cleaned_narratives = []
    fuzzy_matches = []

    for narrative in narratives:
        name = narrative.narrative_name

        # Try exact match first
        if name in flat_narratives:
            cleaned_narratives.append(narrative)
            fuzzy_matches.append({
                "original": name,
                "matched": name,
                "score": 100.0,
                "type": "exact"
            })
        elif enable_fuzzy:
            # Try fuzzy match
            matcher = get_narrative_matcher(flat_narratives, fuzzy_threshold)
            result = matcher.match(name, file_id, "narrative")

            if result.matched:
                # Update narrative with matched name
                narrative.narrative_name = result.matched_label
                cleaned_narratives.append(narrative)
                fuzzy_matches.append({
                    "original": name,
                    "matched": result.matched_label,
                    "score": result.score,
                    "type": "fuzzy"
                })
                print(f"[graph] Fuzzy matched '{name}' -> '{result.matched_label}' (score: {result.score:.1f})")
            else:
                fuzzy_matches.append({
                    "original": name,
                    "matched": None,
                    "score": result.score,
                    "type": "unmatched"
                })
                print(f"[graph] No fuzzy match for '{name}' (best score: {result.score:.1f})")
        else:
            fuzzy_matches.append({
                "original": name,
                "matched": None,
                "score": 0.0,
                "type": "unmatched"
            })

    # Store fuzzy match details in state for later analysis
    return {
        "narratives": cleaned_narratives,
        "narrative_fuzzy_matches": fuzzy_matches
    }


async def classify_subnarratives_node(state, llm, model_name: str = "") -> dict:
    """
    Node function that classifies text into subnarratives for given narratives.
    Uses batch processing for efficiency.

    Args:
        state: Current state containing text and narratives
        llm: The language model instance
        model_name: The model name for structured output handling

    Returns:
        Dictionary with the subnarrative classification results
    """
    text = state.get("cleaned_text", state["text"])  # use cleaned text if available
    narratives = state["narratives"]
    retry_count = state.get("subnarrative_retry_count", 0)
    feedback = state.get("subnarrative_validation_feedback", "")

    valid_parent_narratives = [
        n for n in narratives if n.narrative_name != "Other"
    ]

    narrative_names = [n.narrative_name for n in valid_parent_narratives]
    print(f"[graph] Starting subnarratives classification node for narratives {narrative_names}")


    structured_llm = get_structured_llm(llm, SubnarrativeClassificationOutput, model_name)
    all_messages = _prepare_subnarrative_messages(narratives, text, feedback)

    print("[graph] Starting sequential LLM invocation for subnarratives (with retry)...")
    # Run sequentially with retry to avoid rate limiting
    responses = []
    for i, msg in enumerate(all_messages):
        try:
            response = await invoke_with_retry(structured_llm, msg, f"Subnarrative {i+1}: ")
            responses.append(response)
        except Exception as e:
            print(f"[graph] Warning: Subnarrative {i+1} failed with error: {e}")
            responses.append(None)
    print("[graph] Completed sequential LLM invocation for subnarratives.")

    all_subnarratives_with_details = _process_subnarrative_responses(narratives, responses)

    return {"subnarratives": all_subnarratives_with_details, "subnarrative_retry_count": retry_count + 1}

def validate_subnarratives_node(state, llm, taxonomy, model_name: str = "") -> dict:
    """
    The 'Critic' node for subnarratives. It validates the subnarratives classified by the actor.
    """
    print("[graph] CRITIC: Validating classified subnarratives...")
    text = state.get("cleaned_text", state["text"])  # use cleaned text if available
    subnarratives_analysis = state["subnarratives"]
    narratives_analysis = state["narratives"]
    category = state["category"]

    narrative_names = [n.narrative_name.split(": ")[-1] for n in narratives_analysis if n.narrative_name != "Other"]

    potential_subnarratives = []

    for narrative in narrative_names:
        subs = get_subnarratives_for_narrative(taxonomy, category, narrative)
        potential_subnarratives.extend(subs)

    if not subnarratives_analysis:
        print("[graph] CRITIC: No subnarratives to validate. Approving.")
        return {"subnarrative_validation_feedback": "approved"}

    system_prompt = create_subnarrative_critic_prompt(potential_subnarratives)

    human_prompt = (
        f"ORIGINAL TEXT:\n---\n{text}\n---\n\n"
        f"PARENT NARRATIVES:\n---\n{json.dumps([n.dict() for n in state['narratives']], indent=2)}\n---\n\n"
        f"CLASSIFICATION ANALYSIS TO VALIDATE:\n---\n{json.dumps([s.dict() for s in subnarratives_analysis], indent=2)}\n---"
    )

    messages = [SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)]

    critic_llm = get_structured_llm(llm, ValidationResult, model_name)
    verdict = critic_llm.invoke(messages)

    if verdict.is_valid:
        print(f"[graph] CRITIC: Validation successful.")
        return {"subnarrative_validation_feedback": "approved"}
    else:
        print(f"[graph] CRITIC: Validation failed.")
        return {"subnarrative_validation_feedback": verdict.feedback}


def clean_subnarratives_node(state, flat_subnarratives, enable_fuzzy: bool = True,
                              fuzzy_threshold: float = 70.0) -> dict:
    """
    Node function that filters subnarratives to only include valid ones.
    Supports fuzzy matching for models that return semantically similar but not exact labels.

    Args:
        state: Current state containing subnarratives to clean
        flat_subnarratives: List of valid subnarrative names
        enable_fuzzy: Whether to use fuzzy matching for non-exact labels
        fuzzy_threshold: Minimum score (0-100) for fuzzy match acceptance

    Returns:
        Dictionary with cleaned subnarratives and optional fuzzy match details
    """
    subnarratives = state["subnarratives"]
    file_id = state.get("file_id", "unknown")

    if not subnarratives:
        print("[graph] No subnarratives to clean. Skipping.")
        return {"subnarratives": []}

    print("[graph] Cleaning subnarratives" + (" (with fuzzy matching)" if enable_fuzzy else ""))

    cleaned_subnarratives = []
    fuzzy_matches = []

    for subnarrative in subnarratives:
        name = subnarrative.subnarrative_name

        # Try exact match first
        if name in flat_subnarratives:
            cleaned_subnarratives.append(subnarrative)
            fuzzy_matches.append({
                "original": name,
                "matched": name,
                "score": 100.0,
                "type": "exact"
            })
        elif enable_fuzzy:
            # Try fuzzy match
            matcher = get_subnarrative_matcher(flat_subnarratives, fuzzy_threshold)
            result = matcher.match(name, file_id, "subnarrative")

            if result.matched:
                # Update subnarrative with matched name
                subnarrative.subnarrative_name = result.matched_label
                cleaned_subnarratives.append(subnarrative)
                fuzzy_matches.append({
                    "original": name,
                    "matched": result.matched_label,
                    "score": result.score,
                    "type": "fuzzy"
                })
                print(f"[graph] Fuzzy matched '{name}' -> '{result.matched_label}' (score: {result.score:.1f})")
            else:
                fuzzy_matches.append({
                    "original": name,
                    "matched": None,
                    "score": result.score,
                    "type": "unmatched"
                })
                print(f"[graph] No fuzzy match for '{name}' (best score: {result.score:.1f})")
        else:
            fuzzy_matches.append({
                "original": name,
                "matched": None,
                "score": 0.0,
                "type": "unmatched"
            })

    # Store fuzzy match details in state for later analysis
    return {
        "subnarratives": cleaned_subnarratives,
        "subnarrative_fuzzy_matches": fuzzy_matches
    }


def write_results_node(
    state,
    output_file,
    enable_vote_saving: bool = False,
    narrative_agg_method: str = "",
    subnarrative_agg_method: str = "",
) -> dict|None:
    """
    Node function that writes classification results to file.

    Args:
        state: Current state containing results to write
        output_file: Path to the output file
        enable_vote_saving: Whether to save per-agent votes for analysis
        narrative_agg_method: Narrative aggregation method (for vote metadata)
        subnarrative_agg_method: Subnarrative aggregation method (for vote metadata)

    Returns:
        None (end node)
    """
    file_id = state["file_id"]
    narratives = state.get("narratives", [])
    subnarratives = state.get("subnarratives", [])

    print(f"[graph] Writing results for file {file_id}")

    try:
        write_classification_results(file_id, narratives, subnarratives, output_file)
        write_evidence_json(file_id, narratives, subnarratives, output_file)

        # Save per-agent votes if multi-agent data exists and saving is enabled
        multi_agent_narratives = state.get("multi_agent_narratives", [])
        multi_agent_subnarratives = state.get("multi_agent_subnarratives", [])
        if enable_vote_saving and multi_agent_narratives:
            write_votes_json(
                file_id=file_id,
                multi_agent_narratives=multi_agent_narratives,
                multi_agent_subnarratives=multi_agent_subnarratives,
                num_narrative_agents=len(multi_agent_narratives),
                num_subnarrative_agents=state.get("num_subnarrative_agents", 1),
                narrative_aggregation_method=narrative_agg_method,
                subnarrative_aggregation_method=subnarrative_agg_method,
                aggregated_narratives=narratives,
                aggregated_subnarratives=subnarratives,
                output_file=output_file,
                narrative_agent_metadata=state.get("narrative_agent_metadata", []),
                subnarrative_agent_metadata=state.get("subnarrative_agent_metadata", []),
                narrative_fuzzy_matches=state.get("narrative_fuzzy_matches", []),
                subnarrative_fuzzy_matches=state.get("subnarrative_fuzzy_matches", []),
            )

        print(f"[graph] Results written to {output_file}")
    except Exception as e:
        print(f"[graph] Error writing results: {e}")

    return None


async def multi_agent_classify_narratives_node(state, llm, num_agents: int, model_name: str = "") -> dict:
    """
    Node function that runs n agents in parallel to classify narratives.

    Args:
        state: Current state containing text and category
        llm: The language model instance
        num_agents: Number of agents to run in parallel
        model_name: The model name for structured output handling

    Returns:
        Dictionary with multi-agent narrative classification results
    """
    text = state.get("cleaned_text", state["text"])
    category = state["category"]

    print(f"[graph] Starting multi-agent narratives classification with {num_agents} agents for category {category}")

    # Prepare the same prompt for all agents
    system_prompt = create_narrative_system_prompt(category)
    structured_llm = get_structured_llm(llm, NarrativeClassificationOutput, model_name)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=text)
    ]

    # Run agents sequentially with retry to avoid rate limiting
    # This is slower but more reliable for rate-limited APIs like Mistral
    multi_agent_results = []
    agent_metadata = []
    for i in range(num_agents):
        try:
            response_obj = await invoke_with_retry(structured_llm, messages, f"Agent {i+1}: ")
            narratives_with_details = response_obj.narratives if response_obj.narratives else []
            narrative_names = [n.narrative_name for n in narratives_with_details]
            print(f"[graph] Agent {i+1} classified narratives: {narrative_names}")
            multi_agent_results.append(narratives_with_details)
            agent_metadata.append({
                "agent_id": i + 1,
                "status": "success",
                "n_labels": len(narratives_with_details),
            })
        except Exception as e:
            print(f"[graph] Warning: Agent {i+1} failed with error: {e}")
            multi_agent_results.append([])  # Empty list for failed agent
            agent_metadata.append({
                "agent_id": i + 1,
                "status": "failure",
                "error_type": _classify_error(e),
                "error_message": str(e)[:200],
            })

    print(f"[graph] Multi-agent narratives classification complete")
    return {
        "multi_agent_narratives": multi_agent_results,
        "narrative_agent_metadata": agent_metadata,
    }


async def multi_agent_classify_subnarratives_node(state, llm, num_agents: int, model_name: str = "") -> dict:
    """
    Node function that runs n agents in parallel to classify subnarratives.

    Args:
        state: Current state containing text and narratives
        llm: The language model instance
        num_agents: Number of agents to run in parallel
        model_name: The model name for structured output handling

    Returns:
        Dictionary with multi-agent subnarrative classification results
    """
    text = state.get("cleaned_text", state["text"])
    narratives = state["narratives"]

    valid_parent_narratives = [
        n for n in narratives if n.narrative_name != "Other"
    ]

    narrative_names = [n.narrative_name for n in valid_parent_narratives]
    print(f"[graph] Starting multi-agent subnarratives classification with {num_agents} agents for narratives {narrative_names}")

    if not valid_parent_narratives:
        print(f"[graph] No valid narratives for subnarrative classification")
        return {"multi_agent_subnarratives": [], "num_subnarrative_agents": num_agents}

    structured_llm = get_structured_llm(llm, SubnarrativeClassificationOutput, model_name)

    # Collect all subnarratives from all agents across all narratives
    all_subnarratives_from_all_agents = []
    agent_metadata = []

    for narrative in valid_parent_narratives:
        system_prompt = create_subnarrative_system_prompt(narrative.narrative_name)
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=text)
        ]

        # Run agents sequentially with retry to avoid rate limiting
        for i in range(num_agents):
            try:
                response = await invoke_with_retry(structured_llm, messages, f"Agent {i+1}/{narrative.narrative_name}: ")
                subnarratives = response.subnarratives if response.subnarratives else []
                subnarrative_names = [s.subnarrative_name for s in subnarratives]
                print(f"[graph] Agent {i+1} for narrative '{narrative.narrative_name}' classified subnarratives: {subnarrative_names}")
                all_subnarratives_from_all_agents.extend(subnarratives)
                agent_metadata.append({
                    "agent_id": i + 1,
                    "narrative": narrative.narrative_name,
                    "status": "success",
                    "n_labels": len(subnarratives),
                })
            except Exception as e:
                print(f"[graph] Warning: Agent {i+1} for narrative '{narrative.narrative_name}' failed with error: {e}")
                agent_metadata.append({
                    "agent_id": i + 1,
                    "narrative": narrative.narrative_name,
                    "status": "failure",
                    "error_type": _classify_error(e),
                    "error_message": str(e)[:200],
                })

    print(f"[graph] Multi-agent subnarratives classification complete")
    # Store as nested structure: [all_subnarratives] - single list for easier aggregation
    # Also store num_agents so aggregation can work correctly
    return {
        "multi_agent_subnarratives": [all_subnarratives_from_all_agents],
        "num_subnarrative_agents": num_agents,
        "subnarrative_agent_metadata": agent_metadata,
    }


def aggregate_multi_agent_narratives(state, method: str) -> dict:
    """
    Aggregates multi-agent narrative classification results.
    
    Args:
        state: Current state containing multi-agent narrative results
        method: Aggregation strategy
            - "intersection": narratives appearing in ALL agents
            - "union": narratives appearing in ANY agent
            - "majority": narratives appearing in > 50% of agents
        
    Returns:
        Dictionary with aggregated narratives
    """
    print(f"[graph] Aggregating multi-agent narrative results using {method} method")
    
    # Aggregate narratives
    multi_agent_narratives = state.get("multi_agent_narratives", [])
    if multi_agent_narratives:
        aggregated_narratives = _aggregate_narratives(multi_agent_narratives, method)
    else:
        aggregated_narratives = state.get("narratives", [])
    
    narrative_names = [n.narrative_name for n in aggregated_narratives]
    print(f"[graph] Aggregated narratives: {narrative_names}")
    
    return {
        "narratives": aggregated_narratives
    }


def aggregate_multi_agent_subnarratives(state, method: str) -> dict:
    """
    Aggregates multi-agent subnarrative classification results.
    
    Args:
        state: Current state containing multi-agent subnarrative results
        method: Aggregation strategy
            - "intersection": subnarratives appearing in ALL agents
            - "union": all unique subnarratives
            - "majority": subnarratives appearing in > 50% of agents
        
    Returns:
        Dictionary with aggregated subnarratives
    """
    print(f"[graph] Aggregating multi-agent subnarrative results using {method} method")
    
    # Aggregate subnarratives
    multi_agent_subnarratives = state.get("multi_agent_subnarratives", [])
    num_agents = state.get("num_subnarrative_agents", 1)
    
    if multi_agent_subnarratives:
        aggregated_subnarratives = _aggregate_subnarratives(multi_agent_subnarratives, method, num_agents)
    else:
        aggregated_subnarratives = state.get("subnarratives", [])
    
    subnarrative_names = [s.subnarrative_name for s in aggregated_subnarratives]
    print(f"[graph] Aggregated subnarratives: {subnarrative_names}")
    
    return {
        "subnarratives": aggregated_subnarratives
    }


def _aggregate_narratives(multi_agent_results, method: str):
    """
    Aggregate narrative results from multiple agents.
    
    Args:
        multi_agent_results: List of narrative lists from each agent
        method: "intersection", "union", or "majority"
            - intersection: narratives appearing in ALL agents
            - union: narratives appearing in ANY agent
            - majority: narratives appearing in > 50% of agents
    """
    if not multi_agent_results:
        return []
    
    num_agents = len(multi_agent_results)
    
    if method == "intersection":
        # Find narratives that appear in ALL agent results
        if not multi_agent_results:
            return []
        
        # Get narrative names from each agent
        agent_narrative_sets = []
        for agent_results in multi_agent_results:
            narrative_names = {n.narrative_name for n in agent_results}
            agent_narrative_sets.append(narrative_names)
        
        # Find intersection
        common_narratives = set.intersection(*agent_narrative_sets) if agent_narrative_sets else set()
        
        # Return narrative objects for common narratives (from first agent)
        result = []
        for narrative in multi_agent_results[0]:
            if narrative.narrative_name in common_narratives:
                result.append(narrative)
        return result
    
    elif method == "majority":
        # Find narratives that appear in > 50% of agents
        narrative_counts = {}
        narrative_objects = {}
        
        for agent_results in multi_agent_results:
            for narrative in agent_results:
                name = narrative.narrative_name
                narrative_counts[name] = narrative_counts.get(name, 0) + 1
                if name not in narrative_objects:
                    narrative_objects[name] = narrative
        
        # Keep narratives that appear in majority of agents (> 50%)
        majority_threshold = num_agents / 2
        result = []
        for name, count in narrative_counts.items():
            if count > majority_threshold:
                result.append(narrative_objects[name])
        return result
        
    else:  # union
        # Find narratives that appear in ANY agent result
        seen_narratives = {}
        for agent_results in multi_agent_results:
            for narrative in agent_results:
                if narrative.narrative_name not in seen_narratives:
                    seen_narratives[narrative.narrative_name] = narrative
        
        return list(seen_narratives.values())


def _aggregate_subnarratives(multi_agent_results, method: str, num_agents: int):
    """
    Aggregate subnarrative results from multiple agents.
    Note: multi_agent_results is now a list containing a single list of all subnarratives.
    
    Args:
        multi_agent_results: List containing flat list of all subnarratives from all agents
        method: "intersection", "union", or "majority"
            - intersection: subnarratives appearing in ALL agents
            - union: all unique subnarratives
            - majority: subnarratives appearing in > 50% of agents
        num_agents: Number of agents used for classification
    """
    if not multi_agent_results or not multi_agent_results[0]:
        return []
    
    # Get the flat list of all subnarratives from all agents
    all_subnarratives = multi_agent_results[0]
    
    if method == "intersection":
        # Find subnarratives that appear in ALL agents
        subnarrative_counts = {}
        subnarrative_objects = {}
        
        for subnarrative in all_subnarratives:
            name = subnarrative.subnarrative_name
            subnarrative_counts[name] = subnarrative_counts.get(name, 0) + 1
            subnarrative_objects[name] = subnarrative
        
        # For intersection, we want subnarratives that appeared in ALL agents
        result = []
        for name, count in subnarrative_counts.items():
            if count >= num_agents:  # Appeared in all agents
                result.append(subnarrative_objects[name])
        return result
    
    elif method == "majority":
        # Find subnarratives that appear in majority of agents
        subnarrative_counts = {}
        subnarrative_objects = {}
        
        for subnarrative in all_subnarratives:
            name = subnarrative.subnarrative_name
            subnarrative_counts[name] = subnarrative_counts.get(name, 0) + 1
            subnarrative_objects[name] = subnarrative
        
        # Keep subnarratives that appear in majority of agents (> 50%)
        majority_threshold = num_agents / 2
        
        result = []
        for name, count in subnarrative_counts.items():
            if count > majority_threshold:
                result.append(subnarrative_objects[name])
        return result
        
    else:  # union
        # Return all unique subnarratives
        seen_subnarratives = {}
        for subnarrative in all_subnarratives:
            if subnarrative.subnarrative_name not in seen_subnarratives:
                seen_subnarratives[subnarrative.subnarrative_name] = subnarrative
        
        return list(seen_subnarratives.values())


# Private helper functions

def _prepare_subnarrative_messages(narratives, text, feedback):
    """Prepare batch messages for subnarrative classification."""
    all_messages = []
    for narrative in narratives:
        base_system_prompt = create_subnarrative_system_prompt(narrative.narrative_name)
        
        if feedback and feedback != "approved":
            print("[graph] ACTOR: This is a retry for subnarratives. Incorporating feedback.")
            system_prompt = create_subnarrative_refinement_prompt(base_system_prompt, feedback)
        else:
            system_prompt = base_system_prompt
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=text)
        ]
        all_messages.append(messages)
    return all_messages


def _process_subnarrative_responses(narratives, responses):
    """Process batch responses from subnarrative classification."""
    all_subnarratives_with_details = []

    for parent_narrative, response in zip(narratives, responses):
        # Skip None responses (failed agents)
        if response is None:
            continue
        if response.subnarratives:
            all_subnarratives_with_details.extend(response.subnarratives)
        # Placeholder logic moved to write_results_node via _add_other_placeholders_if_needed

    return all_subnarratives_with_details


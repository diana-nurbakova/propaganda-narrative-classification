import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

from label_info import load_narrative_definitions, load_taxonomy, load_subnarrative_definitions


# ---------------------------------------------------------------------------
#
# These loaders read the data files added in the EMNLP revision (specs/) and
# provide cached lookups for prompt construction. All loads are best-effort:
# if a file is missing, the loader returns an empty dict so the prompt
# falls back gracefully to P0 behaviour.
# ---------------------------------------------------------------------------

DATA_ROOT = Path(__file__).resolve().parents[2] / "data"

PROMPT_LEVELS = ("P0", "P0'", "P0T", "P1", "P2")


@lru_cache(maxsize=1)
def load_tom_taxonomy(path: Optional[str] = None) -> Dict[str, Any]:
    """Load the ToM taxonomy annotation (data/tom_taxonomy.json)."""
    p = Path(path) if path else DATA_ROOT / "tom_taxonomy.json"
    if not p.exists():
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


@lru_cache(maxsize=1)
def load_annotation_guideline_rules(path: Optional[str] = None) -> Dict[str, Any]:
    """Load the annotation-guideline decision rules
    (data/annotation_guideline_rules.json)."""
    p = Path(path) if path else DATA_ROOT / "annotation_guideline_rules.json"
    if not p.exists():
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


@lru_cache(maxsize=4)
def load_bertopic_keywords(path: Optional[str] = None) -> Dict[str, Any]:
    """Load BERTopic per-narrative contrastive keywords. Format::

        {
          "EN": {"<narrative>": ["kw1", "kw2", ...]},
          "BG": {...},
          ...
        }
    """
    p = Path(path) if path else DATA_ROOT / "bertopic_keywords.json"
    if not p.exists():
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _format_tom_block(tom_analysis: Optional[Dict[str, Any]]) -> str:
    """Render a cached ToM Stage 1 analysis as a prompt block."""
    if not tom_analysis:
        return ""
    presups = tom_analysis.get("presuppositions") or []
    if isinstance(presups, list):
        presups = "; ".join(str(p) for p in presups)
    intent = tom_analysis.get("intent", "")
    target = tom_analysis.get("target_belief_change", "")
    mechanism = tom_analysis.get("primary_mechanism", "")
    return (
        "## ToM ANALYSIS OF THIS ARTICLE (cached from Stage 1)\n"
        f"- Presupposed reader beliefs: {presups or 'n/a'}\n"
        f"- Persuasive intent: {intent or 'n/a'}\n"
        f"- Target belief change: {target or 'n/a'}\n"
        f"- Primary cognitive mechanism: {mechanism or 'n/a'}\n"
        "\nWhen you classify, give extra weight to narratives that operate "
        f"through the {mechanism or 'identified'} mechanism above. Do not "
        "invent narratives that contradict the persuasive intent.\n\n"
    )


def _format_general_principles(rules: Dict[str, Any]) -> str:
    principles = rules.get("general_principles", [])
    if not principles:
        return ""
    out = ["## GENERAL CLASSIFICATION PRINCIPLES (apply to every decision)"]
    for i, p in enumerate(principles, 1):
        out.append(f"{i}. {p}")
    return "\n".join(out) + "\n\n"


def _narrative_decision_rule(
    rules: Dict[str, Any], category: str, narrative: str
) -> str:
    nr = rules.get("narrative_rules", {}).get(category, {}).get(narrative)
    if not nr:
        return ""
    return f"  Decision rule (annotation guidelines): {nr}\n"


def _subnarrative_decision_rule(
    rules: Dict[str, Any], category: str, narrative: str, subnarrative: str
) -> str:
    sn = (
        rules.get("subnarrative_rules", {})
        .get(category, {})
        .get(narrative, {})
        .get(subnarrative)
    )
    if not sn:
        return ""
    return f"  Decision rule (annotation guidelines): {sn}\n"


def _bertopic_keywords_for(
    keywords: Dict[str, Any], language: str, narrative: str, k: int = 5
) -> str:
    if not keywords:
        return ""
    lang_kw = keywords.get(language.upper()) or keywords.get(language.lower()) or {}
    kws = lang_kw.get(narrative) or []
    if not kws:
        return ""
    top = ", ".join(kws[:k])
    return f"  Key indicators ({language.upper()}): {top}\n"


def _confused_pair_block(rules: Dict[str, Any], category: str) -> str:
    pairs = rules.get("confused_pairs", []) or []
    relevant = [p for p in pairs if p.get("domain") == category]
    if not relevant:
        return ""
    out = ["\n## DISAMBIGUATION RULES FOR FREQUENTLY CONFUSED LABELS"]
    for p in relevant:
        labels = p.get("labels", [])
        rule = p.get("decision_rule", "")
        kind = p.get("type", "confusion")
        out.append(
            f"- {kind.upper()} between [{labels[0]}] and [{labels[1]}]: {rule}"
        )
    return "\n".join(out) + "\n\n"


def create_category_system_prompt() -> str:
    """
    Create a system prompt for text classification that provides instructions 
    without including the text to be classified.
    """
    
    prompt = (
        "You are a strict topical classifier. Decide whether the given text is primarily about "
        "URW (Ukraine-Russia War topics) or CC (Climate Change topics).\n\n"
        "Rules (follow exactly):\n"
        "- First find the elements that indicate the topic, and reason through them step by step.\n"
        "- Output EXACTLY one label token enclosed in square brackets on the next line: [URW], [CC], or [Other].\n"
        "Classification guidance:\n"
        "- Use [URW] for topics clearly about the Russia-Ukraine conflict.\n"
        "- Use [CC] for topics clearly about climate change.\n"
        "- Use [Other] if neither topic is the primary focus.\n\n"
        "Exact example outputs (showing allowed formats):\n"
        "EVIDENCE: short justification\n[URW]\n\n"
        "EVIDENCE: short justification\n[CC]\n\n"
        "[Other]"
    )

    return prompt

def create_narrative_system_prompt(
    category: str,
    definitions_path: str = "data/narrative_definitions.csv",
    prompt_level: str = "P0",
    tom_analysis: Optional[Dict[str, Any]] = None,
    language: Optional[str] = None,
    bertopic_keywords_path: Optional[str] = None,
    annotation_rules_path: Optional[str] = None,
) -> str:
    """
    Create a prompt to classify text into narratives from a specific category.

    Args:
        category: The category to filter narratives by (e.g., "URW", "CC")
        definitions_path: Path to the narrative definitions CSV file
        prompt_level: One of "P0" (current), "P1" (P0 + annotation-guideline
            decision rules + BERTopic keywords + confused-pair disambiguation),
            "P2" (P1 + ToM Stage 1 analysis prepended).
        tom_analysis: Cached ToM Stage 1 output to prepend (only used at P2).
        language: Language code (EN/BG/HI/PT/RU) for selecting BERTopic keywords.
        bertopic_keywords_path / annotation_rules_path: optional overrides for
            the data file locations (default: data/...).
    """

    if prompt_level not in PROMPT_LEVELS:
        prompt_level = "P0"

    # Load taxonomy and definitions
    taxonomy = load_taxonomy()
    definitions = load_narrative_definitions(definitions_path)
    # P1/P2 load annotation rules + BERTopic keywords; P0/P0' do not.
    _p1_plus = prompt_level in ("P1", "P2")
    rules = load_annotation_guideline_rules(annotation_rules_path) if _p1_plus else {}
    bert_kw = load_bertopic_keywords(bertopic_keywords_path) if _p1_plus else {}

    narratives = []
    if category in taxonomy:
        narratives = taxonomy[category].keys()

    prefixed_narratives = [(n, f"{category}: {n}") for n in narratives]

    prompt_template = ""
    # P0T and P2 prepend the cached ToM Stage 1 analysis.
    if prompt_level in ("P0T", "P2"):
        prompt_template += _format_tom_block(tom_analysis)
    if _p1_plus:
        prompt_template += _format_general_principles(rules)

    prompt_template += (
        "You are an expert propaganda narrative analyst with extensive experience in identifying and classifying manipulative communication patterns.\n"
        "Your task is to analyze the given text and identify which specific propaganda narratives are ACTIVELY PROMOTED.\n\n"
    )
    # P0' and above add the anti-over-prediction instruction (spec S6.1).
    # P0 and P0T (original prompt + ToM only) omit it to measure the effect.
    if prompt_level not in ("P0", "P0T"):
        prompt_template += (
            "CRITICAL RULE: A narrative is present ONLY if the text actively promotes, presents, or advances it. "
            "Merely MENTIONING a topic is NOT sufficient. For example, an article that reports on climate fears "
            "without amplifying them should NOT be labelled 'Amplifying Climate Fears'. An article that mentions "
            "Russia's military without praising it should NOT be labelled 'Praise of Russia'. "
            "Be conservative — it is better to miss a borderline narrative than to over-predict.\n\n"
        )
    prompt_template += "AVAILABLE NARRATIVES:\n\n"

    for narr_name, prefixed in prefixed_narratives:
        prompt_template += f"- {prefixed}\n"
        definition = definitions.get(prefixed, {}).get('definition', 'No definition available.')
        example = definitions.get(prefixed, {}).get('example', '')
        instruction = definitions.get(prefixed, {}).get('instruction', '')
        prompt_template += f"  Definition: {definition}\n"
        if example:
            prompt_template += f"  Example: {example}\n"
        if instruction:
            prompt_template += f"  Instruction: {instruction}\n"
        if _p1_plus:
            prompt_template += _narrative_decision_rule(rules, category, narr_name)
            if language:
                prompt_template += _bertopic_keywords_for(bert_kw, language, narr_name)
        prompt_template += "\n"

    if _p1_plus:
        prompt_template += _confused_pair_block(rules, category)

    prompt_template += """
## INSTRUCTIONS

Follow these two steps precisely:

**Step 1: Chain of Thought (Internal Reasoning)**
First, think step-by-step to analyze the provided text.
- Identify key phrases, arguments, and themes.
- For each potential narrative from the list, consider if it applies.
- Find a specific, direct quote from the text that serves as the strongest evidence for each narrative you believe is present.
- Formulate a brief reasoning for why that quote supports the narrative.
- If no narratives apply, conclude that.

**Step 2: Format the Final Output**
After your internal reasoning is complete, provide your final analysis as a single, valid JSON object.
- The JSON should be the *only* thing in your response. Do not include your chain of thought, explanations, or any markdown formatting like '```json'.

## OUTPUT FORMAT (JSON Schema)

Your entire response MUST be a single JSON object. ALL fields in the schema below are REQUIRED. Do not omit any fields.

{
  "narratives": [
    {
      "narrative_name": "string (The exact name from the list)",
      "evidence_quote": "string (The direct quote from the text you found as evidence)",
      "reasoning": "string (Your justification connecting the quote to the narrative)"
    }
  ]
}

- If multiple narratives are found, include one object for each in the `narratives` list.
- If no propaganda narratives are detected, respond with an empty list for the "narratives" key: `{"narratives": []}`.
"""
    return prompt_template


def create_subnarrative_system_prompt(
    narrative: str,
    definitions_path: str = "data/subnarrative_definitions.csv",
    prompt_level: str = "P0",
    tom_analysis: Optional[Dict[str, Any]] = None,
    language: Optional[str] = None,
    bertopic_keywords_path: Optional[str] = None,
    annotation_rules_path: Optional[str] = None,
) -> str:
    """
    Create a prompt to classify text into subnarratives for a specific narrative.

    Args:
        narrative: The parent narrative to get subnarratives for
            (e.g., "URW: Blaming the war on others rather than the invader")
        definitions_path: Path to the subnarrative definitions CSV file
        prompt_level: P0 / P1 / P2 (see ``create_narrative_system_prompt``).
        tom_analysis: Cached ToM Stage 1 output (used at P2 only).
        language: Language code for BERTopic keyword lookup.
    """

    if prompt_level not in PROMPT_LEVELS:
        prompt_level = "P0"

    taxonomy = load_taxonomy()
    definitions = load_subnarrative_definitions(definitions_path)
    # P1/P2 load annotation rules + BERTopic keywords; P0/P0' do not.
    _p1_plus = prompt_level in ("P1", "P2")
    rules = load_annotation_guideline_rules(annotation_rules_path) if _p1_plus else {}
    bert_kw = load_bertopic_keywords(bertopic_keywords_path) if _p1_plus else {}

    parts = narrative.split(": ", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid narrative format. Expected 'Category: Narrative Name', got: {narrative}")
    category, narrative_name = parts

    subnarratives = []
    if category in taxonomy and narrative_name in taxonomy[category]:
        subnarratives = taxonomy[category][narrative_name]

    prefixed_subnarratives = [
        (s, f"{category}: {narrative_name}: {s}") for s in subnarratives
    ]

    prompt_template = ""
    if prompt_level in ("P0T", "P2"):
        prompt_template += _format_tom_block(tom_analysis)
    if _p1_plus:
        prompt_template += _format_general_principles(rules)

    prompt_template += (
        "You are an expert propaganda narrative analyst with extensive experience in identifying and classifying manipulative communication patterns.\n"
        "This text is known to contain the narrative: "
        f"{narrative}\n"
        "Your task is to identify which specific propaganda subnarratives are ACTIVELY PROMOTED in the text.\n\n"
    )
    # P0' and above add anti-over-prediction for subnarratives too.
    # P0 and P0T omit it.
    if prompt_level not in ("P0", "P0T"):
        prompt_template += (
            "CRITICAL RULE: A subnarrative is present ONLY if the text actively promotes or advances it. "
            "Merely touching on a related topic is NOT sufficient. The evidence must be specific, direct, "
            "and clearly support the subnarrative definition — not require a stretch of interpretation.\n\n"
        )
    prompt_template += "AVAILABLE SUBNARRATIVES:\n\n"

    for sub_name, prefixed in prefixed_subnarratives:
        prompt_template += f"- {prefixed}\n"
        definition = definitions.get(prefixed, {}).get('definition', '')
        example = definitions.get(prefixed, {}).get('example', '')
        instruction = definitions.get(prefixed, {}).get('instruction', '')
        prompt_template += f"  Definition: {definition}\n" if definition else ""
        if example:
            prompt_template += f"  Example: {example}\n"
        if instruction:
            prompt_template += f"  Instruction: {instruction}\n"
        if _p1_plus:
            prompt_template += _subnarrative_decision_rule(
                rules, category, narrative_name, sub_name
            )
            if language:
                prompt_template += _bertopic_keywords_for(
                    bert_kw, language, f"{narrative_name}: {sub_name}"
                )
        prompt_template += "\n"
    
    prompt_template += (
        f"- {narrative}: Other\n"
        "  Definition: Use this option if you find statements that clearly support the parent narrative but do not fit into any of the more specific subnarrative definitions provided above. This can be used IN ADDITION to other specific subnarratives.\n\n"
    )

    prompt_template += """
## INSTRUCTIONS

Follow these two steps precisely:

**Step 1: Chain of Thought (Internal Reasoning)**
First, think step-by-step to analyze the provided text.
- Given that the text contains the parent narrative, look for more specific themes or arguments that match the subnarrative definitions.
- For each potential subnarrative from the list, consider if it applies.
- Find a specific, direct quote from the text that serves as the strongest evidence for each subnarrative you believe is present.
- Formulate a brief reasoning for why that quote supports the subnarrative.

**Step 2: Check for a Remainder**
After identifying all the specific subnarratives, re-read the text. Ask yourself: "Are there any other phrases or arguments that support the parent narrative but were NOT used as evidence for the specific subnarratives I already found?"

**Step 3: Add "Other" if Necessary**
If the answer to Step 2 is YES, you MUST ALSO include the `{narrative}: Other` subnarrative in your final list.

**Step 4: Format the Final Output**
After your internal reasoning is complete, provide your final analysis as a single, valid JSON object.
- The JSON should be the *only* thing in your response. Do not include your chain of thought, explanations, or any markdown formatting like '```json'.

## EXAMPLE OF CORRECT LOGIC

- **Text says:** "Climate activists are just alarmist children. Their funding is also very suspicious."
- **Parent Narrative:** `CC: Criticism of climate movement`
- **Your Analysis:**
  - "Climate activists are just alarmist children" matches `...: Climate movement is alarmist`.
  - "Their funding is also very suspicious" supports the parent narrative but doesn't match any specific subnarrative. This is a remainder.
- **Correct Output:** A list containing BOTH `...: Climate movement is alarmist` AND `CC: Criticism of climate movement: Other`.

## Guidelines for using "...: Other"

- **DO** include `...: Other` alongside specific subnarratives if there is distinct, leftover evidence supporting the parent narrative.
- **DO NOT** include `...: Other` if all the evidence supporting the parent narrative has already been neatly captured by the specific subnarrative(s) you identified. In this case, the classification is complete without it.
- **DO** use `...: Other` as the sole entry if the text supports the parent narrative but does not align with any of the specific definitions.

## OUTPUT FORMAT (JSON Schema)

Your entire response MUST be a single JSON object. ALL fields in the schema below are REQUIRED. Do not omit any fields.

{
  "narratives": [
    {
      "subnarrative_name": "string (The exact name from the list)",
      "evidence_quote": "string (The direct quote from the text you found as evidence)",
      "reasoning": "string (Your justification connecting the quote to the narrative)"
    }
  ]
}

- If multiple subnarratives are found, include one object for each in the `subnarratives` list.
- If no specific subnarratives are detected, respond with an empty list for the "subnarratives" key: `{"subnarratives": []}`.
"""
    return prompt_template


def create_narrative_critic_prompt(narratives) -> str:
    """Creates a system prompt for the 'Critic' agent that validates narrative classifications."""
    prompt = (
        "You are a meticulous and skeptical editor. Your task is to evaluate a classification of propaganda narratives applied to a text. "
        "You must be extremely strict. The classification is only valid if every narrative is strongly and explicitly supported by the provided evidence from the text.\n\n"
        "You will be given the original text and the classification analysis in JSON format. The analysis includes the narrative name, a quote for evidence, and reasoning.\n\n"
        "Here are the narratives that were available for classification:\n"
        f"{', '.join(narratives)}\n\n"
        "## EVALUATION CRITERIA (Apply Strictly):\n"
        "1. **Evidence Accuracy:** Is the `evidence_quote` an exact, verbatim quote from the original text? Of course if the quote is from the text but there was just a small formatting / typography issue it is still fine (not the same unicode character used for example).\n"
        "2. **Relevance of Evidence:** Does the `evidence_quote` DIRECTLY support the `narrative_name`? The connection must not be a stretch or require deep interpretation. If the link is weak, the classification is invalid.\n"
        "3. **Completeness:** Does the analysis miss any other obvious, high-confidence narratives that are clearly present in the text? If so, the classification is invalid.\n\n"
        "## OUTPUT FORMAT\n"
        "Provide your evaluation as a single, valid JSON object conforming to the specified schema. Do not include any other text or formatting."
    )
    return prompt

def create_subnarrative_critic_prompt(subnarratives) -> str:
    """Creates a system prompt for the 'Critic' agent that validates subnarrative classifications."""
    prompt = (
        "You are a meticulous and skeptical editor. Your task is to evaluate a classification of propaganda subnarratives applied to a text. "
        "The list was generated under the assumption that a specific parent narrative is present."
        "You must be extremely strict. The classification is only valid if every subnarrative is strongly and explicitly supported by the provided evidence from the text.\n\n"
        "You will be given the original text and the classification analysis in JSON format. The analysis includes the subnarrative name, a quote for evidence, and reasoning.\n\n"
        "Here is the list of subnarratives that were available to choose from:\n\n"
        f"{'; '.join(subnarratives)}\n\n"
        "## EVALUATION CRITERIA (Apply Strictly):\n"
        "1. **Evidence Accuracy:** Is the `evidence_quote` an exact, verbatim quote from the original text?\n"
        "2. **Relevance of Evidence:** Does the `evidence_quote` DIRECTLY and OBVIOUSLY support the `subnarrative_name`? The connection must not be a stretch or require deep interpretation. If the link is weak, the classification is invalid.\n"
        "3. **Completeness:** Does the analysis miss any other obvious, high-confidence subnarratives that are clearly present in the text? If so, the classification is invalid.\n\n"
        "## OUTPUT FORMAT\n"
        "Provide your evaluation as a single, valid JSON object conforming to the specified schema. Do not include any other text or formatting."
    )
    return prompt

def create_narrative_refinement_prompt(original_prompt: str, feedback: str) -> str:
    """Creates a system prompt for a retry, incorporating the critic's feedback."""
    refinement_header = (
        "You previously analyzed a text, but your analysis had flaws. "
        "A meticulous editor has provided the following feedback. Your task is to re-analyze the text, incorporating this feedback to produce a new, corrected classification.\n\n"
        "## EDITOR'S FEEDBACK TO CORRECT:\n"
        f"{feedback}\n\n"
        "-------------------------------------\n"
        "## ORIGINAL TASK AND DEFINITIONS (Apply these again with the feedback in mind):\n\n"
    )
    return refinement_header + original_prompt

def create_subnarrative_refinement_prompt(original_prompt: str, feedback: str) -> str:
    """Creates a system prompt for a retry of subnarrative classification, incorporating the critic's feedback."""
    refinement_header = (
        "You previously analyzed a text for subnarratives, but your analysis had flaws. "
        "A meticulous editor has provided the following feedback. Your task is to re-analyze the text, incorporating this feedback to produce a new, corrected classification.\n\n"
        "## EDITOR'S FEEDBACK TO CORRECT:\n"
        f"{feedback}\n\n"
        "-------------------------------------\n"
        "## ORIGINAL TASK AND DEFINITIONS (Apply these again with the feedback in mind):\n\n"
    )
    return refinement_header + original_prompt


def create_tom_analysis_prompt() -> str:
    """System prompt for ToM Stage 1 analysis (one call per document, cached).

    The model emits a JSON object with presuppositions, intent, target belief
    change and primary cognitive mechanism. This is consumed by downstream
    nodes when ``prompt_level == 'P2'`` or when ToM arbitration is enabled.
    See specs/agora_emnlp_spec.md \u00a75.2.
    """
    return (
        "You are an expert in persuasion and Theory of Mind. You will receive a "
        "news article and must analyse its persuasive structure \u2014 NOT classify it.\n\n"
        "Answer THREE questions:\n"
        "1. PRESUPPOSITIONS: What beliefs or assumptions does this text take for "
        "granted about its reader? List 1\u20133 short bullet phrases.\n"
        "2. INTENT: What cognitive or emotional effect does this text aim to "
        "produce in the reader? Is it trying to induce fear, erode trust, "
        "reinforce group identity, provoke moral outrage, or something else?\n"
        "3. TARGET BELIEF CHANGE: After reading this text, what should the "
        "reader believe that they did not believe before? Be concrete.\n\n"
        "Then choose ONE primary cognitive mechanism from this set:\n"
        "  - epistemic: changing what the reader believes is TRUE\n"
        "  - emotional: triggering fear / hope / sympathy / outrage\n"
        "  - identity:  reinforcing in-group / out-group affiliation\n"
        "  - moral:     framing actors as good / evil, hero / villain\n\n"
        "## OUTPUT FORMAT\n"
        "Respond with a single valid JSON object \u2014 no markdown, no commentary:\n"
        "{\n"
        "  \"presuppositions\": [\"...\", \"...\"],\n"
        "  \"intent\": \"...\",\n"
        "  \"target_belief_change\": \"...\",\n"
        "  \"primary_mechanism\": \"epistemic|emotional|identity|moral\"\n"
        "}\n"
    )


def create_tom_arbitration_prompt(
    category: str,
    agent_predictions: List[List[str]],
    disagreed_labels: List[str],
    tom_analysis: Optional[Dict[str, Any]] = None,
) -> str:
    """System prompt for the ToM-informed arbitration node.

    Activated when multi-agent narrative predictions disagree on at least one
    label. The arbiter resolves disagreement using the cached ToM Stage 1
    analysis as additional context. See specs/agora_emnlp_spec.md \u00a75.3.
    """
    formatted_agents = "\n".join(
        f"  Agent {i+1}: {labels}" for i, labels in enumerate(agent_predictions)
    )
    tom_block = _format_tom_block(tom_analysis) if tom_analysis else ""
    return (
        tom_block
        + "You are an arbiter resolving disagreement between propaganda-narrative "
        f"classifiers. The article was classified for category {category} by "
        f"{len(agent_predictions)} independent agents who produced different sets:\n"
        f"{formatted_agents}\n\n"
        f"Points of disagreement (labels that did NOT have unanimous agreement):\n"
        f"  {disagreed_labels}\n\n"
        "## YOUR TASK\n"
        "For each disagreed label, decide whether it should be in the FINAL set, "
        "using the cached ToM analysis above as evidence. For each label, ask:\n"
        "1. Is this label consistent with the article's identified persuasive intent?\n"
        "2. Does the article's presupposed reader belief align with the belief "
        "state targeted by this narrative?\n"
        "3. Could the disagreement reflect genuine ambiguity in the text's "
        "persuasive strategy? If so, lean towards INCLUDING the label.\n\n"
        "## OUTPUT FORMAT (JSON only \u2014 no markdown, no extra text)\n"
        "{\n"
        "  \"final_narratives\": [\n"
        "    {\n"
        "      \"narrative_name\": \"<exact narrative name>\",\n"
        "      \"evidence_quote\": \"<verbatim quote from the article>\",\n"
        "      \"reasoning\": \"<why ToM analysis supports including this>\"\n"
        "    }\n"
        "  ]\n"
        "}\n\n"
        "Include ALL narratives that should be in the final set, including "
        "those that all agents already agreed on (do not drop unanimous labels)."
    )


def create_disambiguation_prompt(
    confused_pair_label_a: str,
    confused_pair_label_b: str,
    examples_a: List[Dict[str, str]],
    examples_b: List[Dict[str, str]],
    decision_rule: str = "",
) -> str:
    """System prompt for the confusion-aware disambiguation step.

    Used when an initial prediction includes a label that is part of a known
    confused pair (from the bistochastic-TCM analysis). Provides hard-negative
    contrastive examples and asks the model to re-evaluate. See
    specs/agora_emnlp_spec.md \u00a77.3.
    """
    def _fmt_examples(examples: List[Dict[str, str]]) -> str:
        if not examples:
            return "  (no examples available)\n"
        lines = []
        for ex in examples:
            excerpt = ex.get("excerpt", "").strip()
            tom = ex.get("tom_note", "")
            lines.append(f"  - \"{excerpt}\"")
            if tom:
                lines.append(f"    ToM: {tom}")
        return "\n".join(lines) + "\n"

    return (
        "You previously classified this article and your prediction included "
        f"the label [{confused_pair_label_a}]. This label is frequently confused "
        f"with [{confused_pair_label_b}].\n\n"
        + (f"Decision rule from the annotation guidelines: {decision_rule}\n\n" if decision_rule else "")
        + f"## EXAMPLES OF [{confused_pair_label_a}] (NOT the other label):\n"
        + _fmt_examples(examples_a)
        + f"\n## EXAMPLES OF [{confused_pair_label_b}] (NOT the other label):\n"
        + _fmt_examples(examples_b)
        + "\nGiven these distinctions, re-evaluate the article. Should it be "
        f"labelled with [{confused_pair_label_a}], [{confused_pair_label_b}], "
        "BOTH (if there is genuine overlap), or NEITHER?\n\n"
        "## OUTPUT FORMAT (JSON only)\n"
        "{\n"
        "  \"keep_a\": true|false,\n"
        "  \"keep_b\": true|false,\n"
        "  \"reasoning\": \"<one short paragraph>\"\n"
        "}\n"
    )


def create_cleaning_system_prompt() -> str:
    """System prompt to clean raw web text by removing page noise.
    The model must return ONLY the cleaned text with no extra commentary.
    """
    return (
        "You are a precise text cleaner. Your job is to clean raw text scraped from the web by removing UI noise and boilerplate while preserving the article's content.\n\n"
        "STRICT RULES (follow exactly):\n"
        "- REMOVE: navigation menus, cookie banners, sign-up banners, button labels (e.g., 'Accept', 'Subscribe', 'Read more'), share widgets, headers/footers, unrelated CTAs, legal disclaimers, pagination artifacts, and unrelated links.\n"
        "- KEEP: the main article or post content only. Preserve sentence order, punctuation, and language.\n"
        "- DO NOT paraphrase or summarize. Do not add or remove meaning.\n"
        "- OUTPUT: Return ONLY the cleaned text with no additional commentary, headings, or JSON."
    )

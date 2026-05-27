"""
Helper module for structured output handling across different LLM providers.

OpenAI models support native JSON mode/function calling via with_structured_output.
Other providers (DeepSeek, Mistral, Ollama) may not support this properly,
so we fall back to prompt-based JSON extraction.
"""

import json
import re
from typing import Type, TypeVar, Optional, Any
from pydantic import BaseModel
from langchain_core.messages import SystemMessage, HumanMessage

T = TypeVar('T', bound=BaseModel)

# Models that support native structured output
NATIVE_STRUCTURED_OUTPUT_PROVIDERS = [
    'openai',
    'azure',
    'anthropic',
]


def supports_native_structured_output(model_name: str) -> bool:
    """
    Check if a model supports native structured output (JSON mode/function calling).

    Args:
        model_name: The model name in format 'provider:model' (e.g., 'openai:gpt-5-nano')

    Returns:
        True if the model supports native structured output
    """
    if not model_name:
        return False

    provider = model_name.split(':')[0].lower() if ':' in model_name else model_name.lower()
    return provider in NATIVE_STRUCTURED_OUTPUT_PROVIDERS


def get_json_schema_prompt(schema_class: Type[BaseModel]) -> str:
    """
    Generate a JSON schema instruction for the prompt.

    Args:
        schema_class: The Pydantic model class

    Returns:
        A string with JSON schema instructions
    """
    schema = schema_class.model_json_schema()

    # Simplify the schema for the prompt
    schema_str = json.dumps(schema, indent=2)

    return f"""

IMPORTANT: You MUST respond with valid JSON that matches this exact schema:
```json
{schema_str}
```

Your response must be ONLY the JSON object, no additional text before or after.
Do not include markdown code blocks in your response, just the raw JSON.
"""


def _repair_truncated_json(text: str) -> Optional[dict]:
    """
    Attempt to repair truncated JSON (e.g., from max_tokens cutoff).

    Strategy:
    1. Strip trailing junk after the last meaningful JSON token
    2. Close any unclosed strings, arrays, and objects
    3. Try to parse the repaired text

    Returns:
        Parsed JSON dict or None if repair fails
    """
    # Find the start of the JSON object
    start = text.find('{')
    if start == -1:
        return None

    fragment = text[start:]

    # Strip trailing non-JSON junk (e.g., hallucinated text after truncation)
    # Find last meaningful JSON character
    last_useful = len(fragment) - 1
    while last_useful >= 0 and fragment[last_useful] in ' \t\n\r':
        last_useful -= 1
    fragment = fragment[:last_useful + 1]

    # If it already parses, great
    try:
        return json.loads(fragment)
    except json.JSONDecodeError:
        pass

    # Close unclosed string literals: detect if we're inside a string
    in_string = False
    escaped = False
    for ch in fragment:
        if escaped:
            escaped = False
            continue
        if ch == '\\':
            escaped = True
            continue
        if ch == '"':
            in_string = not in_string

    if in_string:
        fragment += '"'

    # Count unclosed brackets/braces and close them
    stack = []
    in_string = False
    escaped = False
    for ch in fragment:
        if escaped:
            escaped = False
            continue
        if ch == '\\':
            escaped = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch in ('{', '['):
            stack.append(ch)
        elif ch == '}' and stack and stack[-1] == '{':
            stack.pop()
        elif ch == ']' and stack and stack[-1] == '[':
            stack.pop()

    # Remove trailing comma before closing (invalid JSON)
    stripped = fragment.rstrip()
    if stripped and stripped[-1] == ',':
        fragment = stripped[:-1]

    # Close in reverse order
    for opener in reversed(stack):
        fragment += ']' if opener == '[' else '}'

    try:
        result = json.loads(fragment)
        print(f"[structured_output] Repaired truncated JSON (closed {len(stack)} bracket(s))")
        return result
    except json.JSONDecodeError:
        pass

    # Last resort: try to salvage complete items from a truncated array.
    # Find the last complete object in a "narratives"/"subnarratives" array
    # by looking for the last "}," or "}" before truncation.
    last_complete = fragment.rfind('},')
    if last_complete == -1:
        last_complete = fragment.rfind('}')
    if last_complete > 0:
        # Take everything up to and including that "}"
        candidate = fragment[:last_complete + 1]
        # Close any remaining open brackets
        stack2 = []
        in_s = False
        esc = False
        for ch in candidate:
            if esc:
                esc = False
                continue
            if ch == '\\':
                esc = True
                continue
            if ch == '"':
                in_s = not in_s
                continue
            if in_s:
                continue
            if ch in ('{', '['):
                stack2.append(ch)
            elif ch == '}' and stack2 and stack2[-1] == '{':
                stack2.pop()
            elif ch == ']' and stack2 and stack2[-1] == '[':
                stack2.pop()
        for opener in reversed(stack2):
            candidate += ']' if opener == '[' else '}'
        try:
            result = json.loads(candidate)
            print(f"[structured_output] Salvaged partial JSON (dropped truncated trailing item)")
            return result
        except json.JSONDecodeError:
            pass

    return None


def extract_json_from_response(response_text: str) -> Optional[dict]:
    """
    Extract JSON from a model response that may contain additional text.
    Handles truncated JSON from max_tokens cutoff.

    Args:
        response_text: The raw response text from the model

    Returns:
        Parsed JSON dict or None if extraction fails
    """
    if not response_text:
        return None

    text = response_text.strip()

    # Try 1: Direct JSON parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try 2: Extract from markdown code block
    code_block_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
    matches = re.findall(code_block_pattern, text)
    for match in matches:
        try:
            return json.loads(match.strip())
        except json.JSONDecodeError:
            continue

    # Try 3: Find JSON object in text (look for { ... })
    json_pattern = r'\{[\s\S]*\}'
    matches = re.findall(json_pattern, text)
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue

    # Try 4: Find JSON array in text (look for [ ... ])
    array_pattern = r'\[[\s\S]*\]'
    matches = re.findall(array_pattern, text)
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue

    # Try 5: Repair truncated JSON (unclosed braces/brackets/strings)
    result = _repair_truncated_json(text)
    if result is not None:
        return result

    return None


def _normalize_json_keys(json_data: dict, schema_class: Type[BaseModel]) -> dict:
    """
    Normalize JSON keys to match the expected schema fields.

    Some models (e.g., Llama 3.3 via Together AI) return "narratives" instead of
    "subnarratives" for SubnarrativeClassificationOutput. This function detects and
    remaps such mismatches.

    Args:
        json_data: The parsed JSON dict
        schema_class: The Pydantic model class with expected fields

    Returns:
        JSON dict with normalized keys
    """
    if not isinstance(json_data, dict):
        return json_data

    expected_fields = set(schema_class.model_fields.keys())
    actual_keys = set(json_data.keys())

    # If all expected fields are present, no normalization needed
    if expected_fields.issubset(actual_keys):
        return json_data

    # Find missing expected fields and unexpected keys present in response
    missing_fields = expected_fields - actual_keys
    extra_keys = actual_keys - expected_fields

    if not missing_fields or not extra_keys:
        return json_data

    # Try to remap: for each missing field, look for a plausible match in extra keys
    # Common mismatch: "narratives" returned when "subnarratives" expected
    remapped = dict(json_data)
    for missing in list(missing_fields):
        for extra in list(extra_keys):
            # Check if the extra key is a substring/superstring of the missing field
            if extra in missing or missing in extra:
                remapped[missing] = remapped.pop(extra)
                print(f"[structured_output] Remapped JSON key '{extra}' -> '{missing}'")
                missing_fields.discard(missing)
                extra_keys.discard(extra)
                break

    return remapped


def _repair_json_data(json_data: dict, schema_class: Type[BaseModel]) -> dict:
    """
    Repair common JSON issues before Pydantic validation.

    Fixes null/missing string fields, truncated objects, and type mismatches
    so that valid predictions are not discarded due to minor formatting issues.
    """
    if not isinstance(json_data, dict):
        return json_data

    schema = schema_class.model_json_schema()
    defs = schema.get("$defs", schema.get("definitions", {}))

    def _repair_value(value, prop_schema):
        """Recursively repair a value to match its schema."""
        if prop_schema is None:
            return value

        # Resolve $ref
        if "$ref" in prop_schema:
            ref_name = prop_schema["$ref"].split("/")[-1]
            prop_schema = defs.get(ref_name, {})

        prop_type = prop_schema.get("type")

        # Fix null strings -> empty string
        if prop_type == "string" and value is None:
            return ""

        # Fix null numbers -> 0
        if prop_type in ("integer", "number") and value is None:
            return 0

        # Fix arrays
        if prop_type == "array" and isinstance(value, list):
            item_schema = prop_schema.get("items", {})
            if "$ref" in item_schema:
                ref_name = item_schema["$ref"].split("/")[-1]
                item_schema = defs.get(ref_name, {})
            repaired_items = []
            for item in value:
                if isinstance(item, dict) and item_schema.get("type") == "object":
                    item = _repair_object(item, item_schema)
                elif isinstance(item, dict) and "properties" in item_schema:
                    item = _repair_object(item, item_schema)
                repaired_items.append(item)
            return repaired_items

        # Fix objects
        if isinstance(value, dict) and (prop_type == "object" or "properties" in prop_schema):
            return _repair_object(value, prop_schema)

        return value

    def _repair_object(obj, obj_schema):
        """Repair fields in an object to match its schema."""
        if not isinstance(obj, dict):
            return obj
        properties = obj_schema.get("properties", {})
        repaired = dict(obj)
        for field_name, field_schema in properties.items():
            if field_name in repaired:
                repaired[field_name] = _repair_value(repaired[field_name], field_schema)
            elif field_name in obj_schema.get("required", []):
                # Add missing required fields with defaults
                ft = field_schema.get("type")
                if ft == "string":
                    repaired[field_name] = ""
                elif ft == "array":
                    repaired[field_name] = []
                elif ft in ("integer", "number"):
                    repaired[field_name] = 0
                elif ft == "boolean":
                    repaired[field_name] = False
        return repaired

    # Repair top-level
    properties = schema.get("properties", {})
    repaired = dict(json_data)
    for field_name, field_schema in properties.items():
        if field_name in repaired:
            repaired[field_name] = _repair_value(repaired[field_name], field_schema)
        elif field_name in schema.get("required", []):
            ft = field_schema.get("type")
            if ft == "string":
                repaired[field_name] = ""
            elif ft == "array":
                repaired[field_name] = []

    return repaired


def parse_response_to_model(response_text: str, schema_class: Type[T]) -> T:
    """
    Parse a response string to a Pydantic model.

    Applies key normalization and JSON repair before validation to preserve
    valid predictions even when the LLM returns minor formatting issues
    (e.g., null instead of "" for string fields).

    Args:
        response_text: The raw response text
        schema_class: The Pydantic model class to parse into

    Returns:
        An instance of the schema_class

    Raises:
        ValueError: If parsing fails
    """
    json_data = extract_json_from_response(response_text)

    if json_data is None:
        # Return empty/default instance
        print(f"[structured_output] Warning: Could not extract JSON from response, using defaults")
        return create_empty_instance(schema_class)

    # Normalize keys to handle common model-specific mismatches
    # (e.g., Llama returning "narratives" instead of "subnarratives")
    json_data = _normalize_json_keys(json_data, schema_class)

    # Repair common issues (null strings, missing fields) before validation
    json_data = _repair_json_data(json_data, schema_class)

    try:
        return schema_class.model_validate(json_data)
    except Exception as e:
        print(f"[structured_output] Warning: Failed to validate JSON against schema: {e}")
        return create_empty_instance(schema_class)


def create_empty_instance(schema_class: Type[T]) -> T:
    """
    Create an empty/default instance of a Pydantic model.

    Args:
        schema_class: The Pydantic model class

    Returns:
        An instance with empty/default values
    """
    # Get the model's field information
    fields = schema_class.model_fields

    defaults = {}
    for field_name, field_info in fields.items():
        # Check the annotation to determine the type
        annotation = field_info.annotation

        # Handle Optional types and List types
        if hasattr(annotation, '__origin__'):
            origin = annotation.__origin__
            if origin is list:
                defaults[field_name] = []
            else:
                defaults[field_name] = None
        elif annotation == str:
            defaults[field_name] = ""
        elif annotation == bool:
            defaults[field_name] = False
        elif annotation == int:
            defaults[field_name] = 0
        elif annotation == float:
            defaults[field_name] = 0.0
        else:
            defaults[field_name] = None

    try:
        return schema_class.model_validate(defaults)
    except Exception:
        # If validation fails, try with minimal required fields
        return schema_class.model_construct(**defaults)


class StructuredOutputWrapper:
    """
    Wrapper class that provides structured output functionality for any LLM.

    For OpenAI models, uses native with_structured_output.
    For other models, uses prompt-based JSON extraction.
    """

    def __init__(self, llm: Any, schema_class: Type[T], model_name: str = ""):
        """
        Initialize the wrapper.

        Args:
            llm: The LangChain LLM instance
            schema_class: The Pydantic model class for output
            model_name: The model name for determining approach
        """
        self.llm = llm
        self.schema_class = schema_class
        self.model_name = model_name
        self.use_native = supports_native_structured_output(model_name)
        # Always initialize json_schema_prompt for fallback path
        self.json_schema_prompt = get_json_schema_prompt(schema_class)

        if self.use_native:
            self.structured_llm = llm.with_structured_output(schema_class)
        else:
            self.structured_llm = None

    def invoke(self, messages: list) -> T:
        """
        Invoke the LLM and return structured output.

        Args:
            messages: List of messages (SystemMessage, HumanMessage, etc.)

        Returns:
            Instance of schema_class
        """
        if self.use_native:
            try:
                result = self.structured_llm.invoke(messages)
                if result is not None:
                    return result
            except Exception as e:
                print(f"[structured_output] Native structured output failed: {e}, falling back to JSON parsing")

        # Fallback: Add JSON schema to prompt and parse response
        return self._invoke_with_json_prompt(messages)

    async def ainvoke(self, messages: list) -> T:
        """
        Async invoke the LLM and return structured output.

        Args:
            messages: List of messages

        Returns:
            Instance of schema_class
        """
        if self.use_native:
            try:
                result = await self.structured_llm.ainvoke(messages)
                if result is not None:
                    return result
            except Exception as e:
                print(f"[structured_output] Native structured output failed: {e}, falling back to JSON parsing")

        # Fallback: Add JSON schema to prompt and parse response
        return await self._ainvoke_with_json_prompt(messages)

    def _invoke_with_json_prompt(self, messages: list) -> T:
        """Invoke with JSON schema added to prompt."""
        modified_messages = self._add_json_schema_to_messages(messages)
        response = self.llm.invoke(modified_messages)
        return parse_response_to_model(response.content, self.schema_class)

    async def _ainvoke_with_json_prompt(self, messages: list) -> T:
        """Async invoke with JSON schema added to prompt."""
        modified_messages = self._add_json_schema_to_messages(messages)
        response = await self.llm.ainvoke(modified_messages)
        return parse_response_to_model(response.content, self.schema_class)

    def _add_json_schema_to_messages(self, messages: list) -> list:
        """Add JSON schema instructions to the system message."""
        modified = []
        system_found = False

        for msg in messages:
            if isinstance(msg, SystemMessage) and not system_found:
                # Append JSON schema to system message
                new_content = msg.content + self.json_schema_prompt
                modified.append(SystemMessage(content=new_content))
                system_found = True
            else:
                modified.append(msg)

        # If no system message, add one with the JSON schema
        if not system_found:
            modified.insert(0, SystemMessage(content=self.json_schema_prompt))

        return modified


def get_structured_llm(llm: Any, schema_class: Type[T], model_name: str = "") -> StructuredOutputWrapper:
    """
    Get a structured output wrapper for an LLM.

    This is the main entry point for getting structured output from any LLM.

    Args:
        llm: The LangChain LLM instance
        schema_class: The Pydantic model class for output
        model_name: The model name (e.g., 'openai:gpt-5-nano', 'deepseek:deepseek-chat')

    Returns:
        A StructuredOutputWrapper that provides .invoke() and .ainvoke() methods

    Example:
        structured_llm = get_structured_llm(llm, NarrativeClassificationOutput, "deepseek:deepseek-chat")
        result = structured_llm.invoke(messages)
    """
    return StructuredOutputWrapper(llm, schema_class, model_name)

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


def extract_json_from_response(response_text: str) -> Optional[dict]:
    """
    Extract JSON from a model response that may contain additional text.

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
            # Wrap in object if we need an object
            return json.loads(match)
        except json.JSONDecodeError:
            continue

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


def parse_response_to_model(response_text: str, schema_class: Type[T]) -> T:
    """
    Parse a response string to a Pydantic model.

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

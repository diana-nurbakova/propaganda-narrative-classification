#!/usr/bin/env python3
"""
Generate experiment configuration files for fair cross-model comparisons.

This script generates YAML configuration files for all combinations of:
- Models: GPT-5-nano, Gemini 2.5 Flash, DeepSeek, Mistral
- Methods: Agora, Actor-Critic, Baseline, Retrieval-Augmented, Heterogeneous Ensemble
- Hierarchical Strategies: Level-First (DL), Depth-First (DH), Top-Down Multi (TMH)
- Temperatures: 0.0 (deterministic), 0.7 (standard)
- Languages: EN, BG, HI, PT, RU

Usage:
    python generate_configs.py --output-dir configs/experiments/generated/
    python generate_configs.py --models gpt5nano gemini --methods agora baseline --temps 0.0
    python generate_configs.py --methods retrieval --strategies level_first depth_first
"""

import argparse
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

import yaml


# Model configurations
# max_tokens limits vary per provider:
# - OpenAI: 16384+
# - DeepSeek: 8192 max
# - Mistral: 32768 for large models
# - Gemini: 8192 typical
# - Ollama: varies by model, using 8192 as safe default
MODELS = {
    # === API Models ===
    'gpt5nano': {
        'model_name': 'openai:gpt-5-nano',
        'display_name': 'GPT-5-nano',
        'max_tokens': 16384,
        # No max_concurrency here — computed per-method below:
        # multi-agent: 2, single-agent (baseline): 3
    },
    'gpt4omini': {
        'model_name': 'openai:gpt-4o-mini',
        'display_name': 'GPT-4o-mini',
        'max_tokens': 16384,
    },
    'gemini': {
        'model_name': 'google_genai:gemini-2.5-flash',
        'display_name': 'Gemini 2.5 Flash',
        'max_tokens': 8192,
    },
    'deepseek': {
        'model_name': 'deepseek:deepseek-chat',
        'display_name': 'DeepSeek Chat',
        'max_tokens': 8192,  # DeepSeek limit is [1, 8192]
    },
    'mistral': {
        'model_name': 'mistralai:mistral-large-latest',
        'display_name': 'Mistral Large',
        'max_tokens': 8192,
        'enable_fuzzy_matching': True,  # Mistral returns variant labels
        'fuzzy_threshold': 70.0,
        'max_concurrency': 3,
    },
    'claude_haiku': {
        'model_name': 'anthropic:claude-3-haiku-20240307',
        'display_name': 'Claude 3 Haiku',
        'max_tokens': 4096,
    },

    # === Llama via Cloud API ===
    # Requires: pip install langchain-together (or langchain-groq)
    # Set TOGETHER_API_KEY or GROQ_API_KEY env var
    'together_llama33_70b': {
        'model_name': 'together:meta-llama/Llama-3.3-70B-Instruct-Turbo',
        'display_name': 'Llama 3.3 70B (Together AI)',
        'max_tokens': 8192,
        'max_concurrency': 5,
        'enable_fuzzy_matching': True,
        'fuzzy_threshold': 70.0,
    },
    'together_llama31_70b': {
        'model_name': 'together:meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo',
        'display_name': 'Llama 3.1 70B (Together AI)',
        'max_tokens': 8192,
        'max_concurrency': 5,
        'enable_fuzzy_matching': True,
        'fuzzy_threshold': 70.0,
    },
    'groq_llama33_70b': {
        'model_name': 'groq:llama-3.3-70b-versatile',
        'display_name': 'Llama 3.3 70B (Groq)',
        'max_tokens': 8192,
        'max_concurrency': 3,  # Groq has rate limits on free tier
        'enable_fuzzy_matching': True,
        'fuzzy_threshold': 70.0,
    },
    'groq_llama31_70b': {
        'model_name': 'groq:llama-3.1-70b-versatile',
        'display_name': 'Llama 3.1 70B (Groq)',
        'max_tokens': 8192,
        'max_concurrency': 3,
        'enable_fuzzy_matching': True,
        'fuzzy_threshold': 70.0,
    },

    # === Local Models via Ollama ===
    # Install: https://ollama.ai/download
    # No rate limits for local models, can use higher concurrency
    # Fuzzy matching recommended as local models may not follow exact label formats
    'ollama_llama3_70b': {
        'model_name': 'ollama:llama3:70b',
        'display_name': 'Llama 3 70B (Ollama)',
        'max_tokens': 8192,
        'max_concurrency': 5,  # No rate limits locally
        'enable_fuzzy_matching': True,
        'fuzzy_threshold': 70.0,
    },
    'ollama_llama33_70b': {
        'model_name': 'ollama:llama3.3:70b',
        'display_name': 'Llama 3.3 70B (Ollama)',
        'max_tokens': 8192,
        'max_concurrency': 5,
        'enable_fuzzy_matching': True,
        'fuzzy_threshold': 70.0,
    },
    'ollama_mistral_7b': {
        'model_name': 'ollama:mistral:7b',
        'display_name': 'Mistral 7B (Ollama)',
        'max_tokens': 8192,
        'max_concurrency': 5,
        'enable_fuzzy_matching': True,
        'fuzzy_threshold': 70.0,
    },
    'ollama_qwen3_32b': {
        'model_name': 'ollama:qwen3:32b',
        'display_name': 'Qwen 3 32B (Ollama)',
        'max_tokens': 8192,
        'max_concurrency': 5,
        'enable_fuzzy_matching': True,
        'fuzzy_threshold': 70.0,
    },
}

# Hierarchical prompting strategies
STRATEGIES = {
    'level_first': {
        'display_name': 'Level-First (DL)',
        'hierarchical_strategy': 'level_first',
    },
    'depth_first': {
        'display_name': 'Depth-First (DH)',
        'hierarchical_strategy': 'depth_first',
    },
    'top_down_multi': {
        'display_name': 'Top-Down Multi-prompt (TMH)',
        'hierarchical_strategy': 'top_down_multi',
    },
}

# Method configurations
METHODS = {
    'agora_1': {
        'display_name': 'Agora (1-agent intersection)',
        'num_narrative_agents': 1,
        'num_subnarrative_agents': 1,
        'narrative_aggregation_method': 'intersection',
        'subnarrative_aggregation_method': 'intersection',
        'enable_validation': False,
        'enable_narrative_validation': False,
        'enable_subnarrative_validation': False,
        'enable_retrieval': False,
    },
    'agora': {
        'display_name': 'Agora (3-agent intersection)',
        'num_narrative_agents': 3,
        'num_subnarrative_agents': 1,
        'narrative_aggregation_method': 'intersection',
        'subnarrative_aggregation_method': 'intersection',
        'enable_validation': False,
        'enable_narrative_validation': False,
        'enable_subnarrative_validation': False,
        'enable_retrieval': False,
    },
    'agora_5': {
        'display_name': 'Agora (5-agent intersection)',
        'num_narrative_agents': 5,
        'num_subnarrative_agents': 1,
        'narrative_aggregation_method': 'intersection',
        'subnarrative_aggregation_method': 'intersection',
        'enable_validation': False,
        'enable_narrative_validation': False,
        'enable_subnarrative_validation': False,
        'enable_retrieval': False,
    },
    'agora_7': {
        'display_name': 'Agora (7-agent intersection)',
        'num_narrative_agents': 7,
        'num_subnarrative_agents': 1,
        'narrative_aggregation_method': 'intersection',
        'subnarrative_aggregation_method': 'intersection',
        'enable_validation': False,
        'enable_narrative_validation': False,
        'enable_subnarrative_validation': False,
        'enable_retrieval': False,
    },
    'agora_majority': {
        'display_name': 'Agora (3-agent majority)',
        'num_narrative_agents': 3,
        'num_subnarrative_agents': 1,
        'narrative_aggregation_method': 'majority',
        'subnarrative_aggregation_method': 'majority',
        'enable_validation': False,
        'enable_narrative_validation': False,
        'enable_subnarrative_validation': False,
        'enable_retrieval': False,
    },
    'agora_union': {
        'display_name': 'Agora (3-agent union)',
        'num_narrative_agents': 3,
        'num_subnarrative_agents': 1,
        'narrative_aggregation_method': 'union',
        'subnarrative_aggregation_method': 'union',
        'enable_validation': False,
        'enable_narrative_validation': False,
        'enable_subnarrative_validation': False,
        'enable_retrieval': False,
    },
    'actor_critic': {
        'display_name': 'Actor-Critic (validation)',
        'num_narrative_agents': 1,
        'num_subnarrative_agents': 1,
        'narrative_aggregation_method': 'union',
        'subnarrative_aggregation_method': 'union',
        'enable_validation': True,
        'enable_narrative_validation': True,
        'enable_subnarrative_validation': True,
        'enable_retrieval': False,
    },
    'baseline': {
        'display_name': 'Naive Baseline (single agent)',
        'num_narrative_agents': 1,
        'num_subnarrative_agents': 1,
        'narrative_aggregation_method': 'union',
        'subnarrative_aggregation_method': 'union',
        'enable_validation': False,
        'enable_narrative_validation': False,
        'enable_subnarrative_validation': False,
        'enable_retrieval': False,
    },
    'retrieval': {
        'display_name': 'Retrieval-Augmented (top-K filtering)',
        'num_narrative_agents': 1,
        'num_subnarrative_agents': 1,
        'narrative_aggregation_method': 'union',
        'subnarrative_aggregation_method': 'union',
        'enable_validation': False,
        'enable_narrative_validation': False,
        'enable_subnarrative_validation': False,
        'enable_retrieval': True,
        'retrieval_top_k': 10,
    },
    'retrieval_agora': {
        'display_name': 'Retrieval + Agora (top-K + 3-agent)',
        'num_narrative_agents': 3,
        'num_subnarrative_agents': 1,
        'narrative_aggregation_method': 'intersection',
        'subnarrative_aggregation_method': 'intersection',
        'enable_validation': False,
        'enable_narrative_validation': False,
        'enable_subnarrative_validation': False,
        'enable_retrieval': True,
        'retrieval_top_k': 10,
    },
    'heterogeneous': {
        'display_name': 'Heterogeneous Ensemble (GPT + Gemini + Claude)',
        'num_narrative_agents': 3,
        'num_subnarrative_agents': 1,
        'narrative_aggregation_method': 'intersection',
        'subnarrative_aggregation_method': 'intersection',
        'enable_validation': False,
        'enable_narrative_validation': False,
        'enable_subnarrative_validation': False,
        'enable_retrieval': False,
        'narrative_agent_models': [
            'openai:gpt-5-nano',
            'google_genai:gemini-2.5-flash',
            'anthropic:claude-3-haiku-20240307',
        ],
    },
    'heterogeneous_local': {
        'display_name': 'Heterogeneous Local Ensemble (Llama + DeepSeek + Mistral via Ollama)',
        'num_narrative_agents': 3,
        'num_subnarrative_agents': 1,
        'narrative_aggregation_method': 'intersection',
        'subnarrative_aggregation_method': 'intersection',
        'enable_validation': False,
        'enable_narrative_validation': False,
        'enable_subnarrative_validation': False,
        'enable_retrieval': False,
        'narrative_agent_models': [
            'ollama:llama3.1:8b',
            'ollama:deepseek-r1:8b',
            'ollama:mistral:7b',
        ],
    },
}

# List of API models (for default generation)
API_MODELS = ['gpt5nano', 'gpt4omini', 'gemini', 'deepseek', 'mistral', 'claude_haiku']

# List of Llama models via cloud API (Together AI, Groq)
LLAMA_API_MODELS = ['together_llama33_70b', 'together_llama31_70b', 'groq_llama33_70b', 'groq_llama31_70b']

# List of local Ollama models
LOCAL_MODELS = ['ollama_llama3', 'ollama_llama3_70b', 'ollama_deepseek', 'ollama_deepseek_32b',
                'ollama_mistral', 'ollama_mixtral', 'ollama_qwen', 'ollama_qwen_32b']

# Language configurations for DEV SET (has gold labels for evaluation)
LANGUAGES = {
    'en': {
        'input_folder': 'data/dev-documents_4_December/EN/subtask-2-documents/',
        'ground_truth': 'data/dev-documents_4_December/EN/subtask-3-dominant-narratives.txt',
    },
    'bg': {
        'input_folder': 'data/dev-documents_4_December/BG/subtask-2-documents/',
        'ground_truth': 'data/dev-documents_4_December/BG/subtask-3-dominant-narratives.txt',
    },
    'hi': {
        'input_folder': 'data/dev-documents_4_December/HI/subtask-2-documents/',
        'ground_truth': 'data/dev-documents_4_December/HI/subtask-3-dominant-narratives.txt',
    },
    'pt': {
        'input_folder': 'data/dev-documents_4_December/PT/subtask-2-documents/',
        'ground_truth': 'data/dev-documents_4_December/PT/subtask-3-dominant-narratives.txt',
    },
    'ru': {
        'input_folder': 'data/dev-documents_4_December/RU/subtask-2-documents/',
        'ground_truth': 'data/dev-documents_4_December/RU/subtask-3-dominant-narratives.txt',
    },
}

# Language configurations for TEST SET (no gold labels - predictions only)
LANGUAGES_TESTSET = {
    'en': {
        'input_folder': 'data/testset/EN/subtask-2-documents/',
        'ground_truth': None,  # No gold labels available
    },
    'bg': {
        'input_folder': 'data/testset/BG/subtask-2-documents/',
        'ground_truth': None,
    },
    'hi': {
        'input_folder': 'data/testset/HI/subtask-2-documents/',
        'ground_truth': None,
    },
    'pt': {
        'input_folder': 'data/testset/PT/subtask-2-documents/',
        'ground_truth': None,
    },
    'ru': {
        'input_folder': 'data/testset/RU/subtask-2-documents/',
        'ground_truth': None,
    },
}

# Language configurations for TRAIN SET (for training/validation splits)
LANGUAGES_TRAIN = {
    'en': {
        'input_folder': 'data/train/EN/raw-documents/',
        'ground_truth': 'data/train/EN/subtask-3-annotations.txt',
    },
    'bg': {
        'input_folder': 'data/train/BG/raw-documents/',
        'ground_truth': 'data/train/BG/subtask-3-annotations.txt',
    },
    'hi': {
        'input_folder': 'data/train/HI/raw-documents/',
        'ground_truth': 'data/train/HI/subtask-3-annotations.txt',
    },
    'pt': {
        'input_folder': 'data/train/PT/raw-documents/',
        'ground_truth': 'data/train/PT/subtask-3-annotations.txt',
    },
    'ru': {
        'input_folder': 'data/train/RU/raw-documents/',
        'ground_truth': 'data/train/RU/subtask-3-annotations.txt',
    },
}

# Temperature settings
TEMPERATURES = [0.0, 0.7]


def get_language_config(language_key: str, dataset: str = 'dev') -> Dict[str, Any]:
    """Get language configuration for the specified dataset."""
    if dataset == 'test':
        return LANGUAGES_TESTSET[language_key]
    elif dataset == 'train':
        return LANGUAGES_TRAIN[language_key]
    else:  # default to dev
        return LANGUAGES[language_key]


def generate_config(
    model_key: str,
    method_key: str,
    language_key: str,
    temperature: float,
    strategy_key: str = 'level_first',
    enable_cost_tracking: bool = True,
    enable_vote_saving: bool = False,
    dataset: str = 'dev',
    ollama_base_url: Optional[str] = None,
    ollama_api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate a single configuration dictionary."""
    model = MODELS[model_key]
    method = METHODS[method_key]
    language = get_language_config(language_key, dataset)
    strategy = STRATEGIES.get(strategy_key, STRATEGIES['level_first'])

    # Create experiment ID
    temp_str = str(temperature).replace('.', '')
    strategy_suffix = f"_{strategy_key}" if strategy_key != 'level_first' else ""
    experiment_id = f"{method_key}_{model_key}_{language_key}_t{temp_str}{strategy_suffix}"

    config = {
        # Header comment (will be added separately)
        'model_name': model['model_name'],
        'input_folder': language['input_folder'],
        'output_file': f"results/experiments/{experiment_id}/run_{{run_id}}/results.txt",

        # Model parameters for fair comparison
        'temperature': temperature,
        'top_p': 1.0,
        'max_tokens': model.get('max_tokens', 8192),  # Use model-specific limit
        # seed is set per-run by run_multi_experiment.py

        # Hierarchical prompting strategy
        'hierarchical_strategy': strategy['hierarchical_strategy'],

        # Method-specific settings
        'num_narrative_agents': method['num_narrative_agents'],
        'num_subnarrative_agents': method['num_subnarrative_agents'],
        'narrative_aggregation_method': method['narrative_aggregation_method'],
        'subnarrative_aggregation_method': method['subnarrative_aggregation_method'],
        'enable_validation': method['enable_validation'],
        'enable_narrative_validation': method['enable_narrative_validation'],
        'enable_subnarrative_validation': method['enable_subnarrative_validation'],

        # Retrieval-augmented HTC
        'enable_retrieval': method.get('enable_retrieval', False),

        # Standard settings
        'enable_cleaning': True,
        'enable_text_cleaning': False,
        # Lower concurrency for rate limits
        # - Model-specific: use model's max_concurrency if set (e.g., Mistral has strict limits)
        # - GPT-5-nano: 200K TPM -> concurrency 2 for multi-agent, 3 for single
        # - Multi-agent methods: lower concurrency (more API calls per document)
        # - Single-agent methods: higher concurrency
        'max_concurrency': model.get('max_concurrency') or (
            2 if 'gpt5nano' in model_key and method['num_narrative_agents'] > 1 else (
                3 if 'gpt5nano' in model_key else (
                    3 if method['num_narrative_agents'] > 1 else 5
                )
            )
        ),

        # Cost tracking
        'enable_cost_tracking': enable_cost_tracking,
    }

    # Vote saving (per-agent votes before aggregation)
    if enable_vote_saving:
        config['enable_vote_saving'] = True

    # Add retrieval settings if enabled
    if method.get('enable_retrieval'):
        config['retrieval_top_k'] = method.get('retrieval_top_k', 10)

    # Add heterogeneous ensemble models if specified
    if 'narrative_agent_models' in method:
        config['narrative_agent_models'] = method['narrative_agent_models']
    if 'subnarrative_agent_models' in method:
        config['subnarrative_agent_models'] = method['subnarrative_agent_models']

    # Add cost metrics path if tracking enabled
    if enable_cost_tracking:
        config['cost_metrics_path'] = f"results/experiments/{experiment_id}/run_{{run_id}}/cost_metrics.json"

    # Add fuzzy matching settings for models that need it (e.g., Mistral)
    if model.get('enable_fuzzy_matching', False):
        config['enable_fuzzy_matching'] = True
        config['fuzzy_threshold'] = model.get('fuzzy_threshold', 70.0)
        config['fuzzy_tracking_path'] = f"results/experiments/{experiment_id}/run_{{run_id}}/fuzzy_matching.json"

    # Add Ollama-specific settings for authenticated/remote endpoints
    if model['model_name'].startswith('ollama:'):
        if ollama_base_url:
            config['ollama_base_url'] = ollama_base_url
        if ollama_api_key:
            config['ollama_api_key'] = ollama_api_key

    return config


def save_config(config: Dict[str, Any], output_path: str, header: str = "") -> None:
    """Save configuration to YAML file with optional header comment."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        if header:
            f.write(header)
            f.write('\n')
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)


def generate_all_configs(
    output_dir: str,
    models: List[str] = None,
    methods: List[str] = None,
    languages: List[str] = None,
    temperatures: List[float] = None,
    strategies: List[str] = None,
    enable_cost_tracking: bool = True,
    enable_vote_saving: bool = False,
    dataset: str = 'dev',
    ollama_base_url: Optional[str] = None,
    ollama_api_key: Optional[str] = None,
) -> int:
    """
    Generate all configuration files.

    Args:
        output_dir: Directory to save generated configs
        models: List of model keys to generate configs for
        methods: List of method keys to generate configs for
        languages: List of language keys to generate configs for
        temperatures: List of temperature values
        strategies: List of hierarchical strategy keys
        enable_cost_tracking: Whether to enable cost tracking
        dataset: Dataset to use ('dev' for evaluation, 'test' for predictions, 'train' for training)
        ollama_base_url: Custom Ollama base URL for authenticated endpoints
        ollama_api_key: Bearer token for authenticated Ollama endpoints

    Returns:
        Number of configs generated
    """
    # Use defaults if not specified
    models = models or list(MODELS.keys())
    methods = methods or list(METHODS.keys())
    languages = languages or list(LANGUAGES.keys())
    temperatures = temperatures or TEMPERATURES
    strategies = strategies or ['level_first']  # Default to level-first only

    count = 0
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for model_key in models:
        if model_key not in MODELS:
            print(f"Warning: Unknown model '{model_key}', skipping")
            continue

        for method_key in methods:
            if method_key not in METHODS:
                print(f"Warning: Unknown method '{method_key}', skipping")
                continue

            for language_key in languages:
                if language_key not in LANGUAGES:
                    print(f"Warning: Unknown language '{language_key}', skipping")
                    continue

                for temp in temperatures:
                    for strategy_key in strategies:
                        if strategy_key not in STRATEGIES:
                            print(f"Warning: Unknown strategy '{strategy_key}', skipping")
                            continue

                        config = generate_config(
                            model_key, method_key, language_key, temp,
                            strategy_key, enable_cost_tracking,
                            enable_vote_saving, dataset,
                            ollama_base_url, ollama_api_key
                        )

                        # Create filename
                        temp_str = str(temp).replace('.', '')
                        strategy_suffix = f"_{strategy_key}" if strategy_key != 'level_first' else ""
                        filename = f"{method_key}_{model_key}_{language_key}_t{temp_str}{strategy_suffix}.yaml"
                        filepath = output_path / filename

                        # Create header comment
                        model_name = MODELS[model_key]['display_name']
                        method_name = METHODS[method_key]['display_name']
                        strategy_name = STRATEGIES[strategy_key]['display_name']
                        header = f"# Experiment Configuration\n"
                        header += f"# Model: {model_name}\n"
                        header += f"# Method: {method_name}\n"
                        header += f"# Strategy: {strategy_name}\n"
                        header += f"# Language: {language_key.upper()}\n"
                        header += f"# Temperature: {temp}\n"
                        header += f"#\n"
                        header += f"# Generated by generate_configs.py\n"
                        header += f"# Use with run_multi_experiment.py for statistical testing\n"

                        save_config(config, str(filepath), header)
                        count += 1

    return count


def main():
    parser = argparse.ArgumentParser(
        description="Generate experiment configuration files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all configs (core methods only)
  python generate_configs.py --output-dir configs/experiments/generated/

  # Generate only for specific models and methods
  python generate_configs.py --models gpt5nano gemini --methods agora baseline

  # Generate configs with different hierarchical strategies
  python generate_configs.py --methods baseline --strategies level_first depth_first top_down_multi

  # Generate retrieval-augmented configs
  python generate_configs.py --methods retrieval retrieval_agora --languages en

  # Generate heterogeneous ensemble configs
  python generate_configs.py --methods heterogeneous --languages en --temps 0.0

  # Generate with cost tracking enabled
  python generate_configs.py --methods agora --cost-tracking

  # === LOCAL MODELS VIA OLLAMA ===
  # Generate configs for local Llama model
  python generate_configs.py --models ollama_llama3 --methods agora baseline --languages en

  # Generate configs for multiple local models
  python generate_configs.py --models ollama_llama3 ollama_deepseek ollama_mistral --methods baseline

  # Generate heterogeneous local ensemble (Llama + DeepSeek + Mistral)
  python generate_configs.py --methods heterogeneous_local --languages en --temps 0.0

  # List all available options including Ollama models
  python generate_configs.py --list
        """
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default='configs/experiments/generated/',
        help='Output directory for generated configs'
    )
    parser.add_argument(
        '--models',
        nargs='+',
        choices=list(MODELS.keys()),
        help='Models to generate configs for (default: all except claude_haiku)'
    )
    parser.add_argument(
        '--methods',
        nargs='+',
        choices=list(METHODS.keys()),
        help='Methods to generate configs for (default: agora, actor_critic, baseline)'
    )
    parser.add_argument(
        '--languages',
        nargs='+',
        choices=list(LANGUAGES.keys()),
        help='Languages to generate configs for (default: all)'
    )
    parser.add_argument(
        '--temps',
        nargs='+',
        type=float,
        help='Temperature values (default: 0.0 0.7)'
    )
    parser.add_argument(
        '--strategies',
        nargs='+',
        choices=list(STRATEGIES.keys()),
        help='Hierarchical strategies to generate configs for (default: level_first only)'
    )
    parser.add_argument(
        '--cost-tracking',
        action='store_true',
        help='Enable cost tracking in generated configs'
    )
    parser.add_argument(
        '--vote-saving',
        action='store_true',
        help='Enable per-agent vote saving (writes votes/ JSON per document)'
    )
    parser.add_argument(
        '--dataset',
        choices=['dev', 'test', 'train'],
        default='dev',
        help='Dataset to use: dev (has gold labels for evaluation), test (no gold labels), train'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List available options and exit'
    )
    parser.add_argument(
        '--ollama-base-url',
        type=str,
        default=None,
        help='Custom Ollama base URL for authenticated/remote endpoints (e.g., https://ollama-ui.example.com/ollama)'
    )
    parser.add_argument(
        '--ollama-api-key',
        type=str,
        default=None,
        help='Bearer token for authenticated Ollama endpoints (or set OLLAMA_API_KEY env var)'
    )

    args = parser.parse_args()

    # Support environment variable for API key
    import os
    ollama_api_key = args.ollama_api_key or os.environ.get('OLLAMA_API_KEY')

    if args.list:
        print("Available API Models:")
        for key in API_MODELS:
            val = MODELS[key]
            print(f"  {key}: {val['display_name']} ({val['model_name']})")
        print("\nAvailable Llama Models (via Cloud API):")
        for key in LLAMA_API_MODELS:
            val = MODELS[key]
            print(f"  {key}: {val['display_name']} ({val['model_name']})")
        print("\nAvailable Local Models (via Ollama):")
        for key in LOCAL_MODELS:
            val = MODELS[key]
            print(f"  {key}: {val['display_name']} ({val['model_name']})")
        print("\nAvailable Methods:")
        for key, val in METHODS.items():
            print(f"  {key}: {val['display_name']}")
        print("\nAvailable Hierarchical Strategies:")
        for key, val in STRATEGIES.items():
            print(f"  {key}: {val['display_name']}")
        print("\nAvailable Languages:")
        for key, val in LANGUAGES.items():
            print(f"  {key}: {val['input_folder']}")
        print("\nDefault Temperatures:", TEMPERATURES)
        print("\nOllama Setup:")
        print("  Local Ollama:")
        print("    1. Install Ollama: https://ollama.ai/download")
        print("    2. Pull models: ollama pull llama3.1:8b")
        print("    3. Start server: ollama serve (runs on localhost:11434)")
        print("\n  Remote/Authenticated Ollama:")
        print("    Use --ollama-base-url and --ollama-api-key flags, or set OLLAMA_API_KEY env var")
        print("    Example: python generate_configs.py --models ollama_llama3_70b \\")
        print("             --ollama-base-url https://ollama-ui.example.com/ollama \\")
        print("             --ollama-api-key YOUR_API_KEY")
        return 0

    # Default to core methods if not specified
    methods = args.methods or ['agora', 'actor_critic', 'baseline']
    # Default to API models (excluding claude_haiku which needs separate key)
    models = args.models or ['gpt5nano', 'gemini', 'deepseek', 'mistral']

    count = generate_all_configs(
        output_dir=args.output_dir,
        models=models,
        methods=methods,
        languages=args.languages,
        temperatures=args.temps,
        strategies=args.strategies,
        enable_cost_tracking=args.cost_tracking,
        enable_vote_saving=args.vote_saving,
        dataset=args.dataset,
        ollama_base_url=args.ollama_base_url,
        ollama_api_key=ollama_api_key,
    )

    print(f"\nGenerated {count} configuration files in {args.output_dir}")
    print(f"Dataset: {args.dataset} ({'with gold labels' if args.dataset != 'test' else 'predictions only'})")
    return 0


if __name__ == "__main__":
    exit(main())

"""
Configuration loader for the LangGraph classification system.
Handles loading and validation of YAML configuration files.
"""

import yaml
from dataclasses import dataclass
from typing import Optional, Dict, Any
from pathlib import Path


@dataclass
class ClassificationConfig:
    """Configuration schema for the classification system."""

    model_name: str

    input_folder: str
    output_file: str

    enable_validation: bool = True  # Global validation flag (backward compatibility)
    enable_cleaning: bool = True    # Global cleaning flag (backward compatibility)

    # Granular validation flags (optional - override global setting)
    enable_narrative_validation: Optional[bool] = None
    enable_subnarrative_validation: Optional[bool] = None

    # Optional text cleaning stage
    enable_text_cleaning: bool = False

    # Multi-agent classification settings
    num_agents: int = 1  # DEPRECATED: Use num_narrative_agents and num_subnarrative_agents instead
    num_narrative_agents: int = 1  # Number of agents for narrative classification
    num_subnarrative_agents: int = 1  # Number of agents for subnarrative classification
    aggregation_method: str = "union"  # DEPRECATED: Use narrative_aggregation_method and subnarrative_aggregation_method instead
    narrative_aggregation_method: str = "union"  # "union" or "intersection" for narratives
    subnarrative_aggregation_method: str = "union"  # "union" or "intersection" for subnarratives

    max_concurrency: int = 20

    # Model parameters for reproducibility and fair comparison
    temperature: float = 0.0  # Default to deterministic (0.0)
    top_p: float = 1.0
    max_tokens: int = 16384  # High value for reasoning models that use internal chain-of-thought
    seed: Optional[int] = None  # None = non-deterministic (random each call)

    # Experiment metadata for multi-run tracking
    experiment_id: Optional[str] = None  # Unique identifier for experiment group
    run_id: Optional[int] = None  # Run number within experiment (1-N)

    # Hierarchical prompting strategy
    # - "level_first" (DL): Classify all narratives, then all subnarratives (default, current behavior)
    # - "depth_first" (DH): For each narrative, classify its subnarratives immediately
    # - "top_down_multi" (TMH): Multiple prompts at each level with refinement
    hierarchical_strategy: str = "level_first"

    # Retrieval-augmented HTC settings
    enable_retrieval: bool = False  # Enable top-K label filtering before LLM classification
    retrieval_top_k: int = 10  # Number of candidate labels to retrieve
    retrieval_embeddings_path: Optional[str] = None  # Path to label embeddings (default: embeddings/)

    # Heterogeneous ensemble settings (per-agent model specification)
    # List of model names for each agent, e.g., ["openai:gpt-5-nano", "google_genai:gemini-2.5-flash", "anthropic:claude-3-haiku"]
    # If None, all agents use the same model (model_name)
    narrative_agent_models: Optional[list] = None
    subnarrative_agent_models: Optional[list] = None

    # Cost tracking
    enable_cost_tracking: bool = False  # Enable API call cost and latency tracking
    cost_metrics_path: Optional[str] = None  # Path to save cost metrics JSON

    # Fuzzy label matching settings (for models like Mistral that return variant labels)
    enable_fuzzy_matching: bool = False  # Enable fuzzy label matching during cleaning
    fuzzy_threshold: float = 70.0  # Minimum score (0-100) for accepting a fuzzy match
    fuzzy_tracking_path: Optional[str] = None  # Path to save fuzzy match tracking JSON

    # Vote saving (for post-hoc voting failure analysis)
    enable_vote_saving: bool = False  # Save per-agent votes before aggregation

    # Ollama-specific settings (for self-hosted/authenticated Ollama endpoints)
    ollama_base_url: Optional[str] = None  # Custom Ollama base URL (e.g., https://ollama-ui.example.com/ollama)
    ollama_api_key: Optional[str] = None  # Bearer token for authenticated Ollama endpoints

    category: Optional[Dict[str, Any]] = None
    narratives: Optional[Dict[str, Any]] = None
    subnarratives: Optional[Dict[str, Any]] = None
    cleaning: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_yaml(cls, config_path: Path) -> 'ClassificationConfig':
        """
        Load configuration from a YAML file.
        
        Args:
            config_path: Path to the YAML configuration file
            
        Returns:
            ClassificationConfig instance
        """
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
        
        required_fields = ['model_name', 'input_folder', 'output_file']
        for field in required_fields:
            if field not in yaml_data:
                raise ValueError(f"Required field '{field}' missing from configuration")
        
        # Allow templated output_file using placeholders like {model_name} or {model}
        raw_output = yaml_data['output_file']
        # sanitize model name for filesystem use
        raw_model = yaml_data['model_name']
        safe_model = raw_model.replace(':', '_').replace('/', '-').replace(' ', '-')

        # Use string replacement instead of .format() to avoid KeyError on unknown placeholders
        # This allows {run_id} and {experiment_id} to be processed separately
        formatted_output = raw_output.replace('{model_name}', safe_model).replace('{model}', safe_model)

        # Handle backward compatibility: if num_agents is set but not the specific ones, use it for both
        num_agents = yaml_data.get('num_agents', 1)
        num_narrative_agents = yaml_data.get('num_narrative_agents', num_agents)
        num_subnarrative_agents = yaml_data.get('num_subnarrative_agents', 1)  # Default to 1 for subnars
        
        # Handle backward compatibility for aggregation methods
        aggregation_method = yaml_data.get('aggregation_method', 'union')
        narrative_aggregation_method = yaml_data.get('narrative_aggregation_method', aggregation_method)
        subnarrative_aggregation_method = yaml_data.get('subnarrative_aggregation_method', aggregation_method)
        
        # Support additional placeholders in output_file for experiment tracking
        experiment_id = yaml_data.get('experiment_id')
        run_id = yaml_data.get('run_id')
        if experiment_id:
            formatted_output = formatted_output.replace('{experiment_id}', str(experiment_id))
        if run_id is not None:
            formatted_output = formatted_output.replace('{run_id}', str(run_id))

        # Process cost_metrics_path the same way
        cost_metrics_path = yaml_data.get('cost_metrics_path')
        if cost_metrics_path:
            cost_metrics_path = cost_metrics_path.replace('{model_name}', safe_model).replace('{model}', safe_model)
            if experiment_id:
                cost_metrics_path = cost_metrics_path.replace('{experiment_id}', str(experiment_id))
            if run_id is not None:
                cost_metrics_path = cost_metrics_path.replace('{run_id}', str(run_id))

        # Process fuzzy_tracking_path the same way
        fuzzy_tracking_path = yaml_data.get('fuzzy_tracking_path')
        if fuzzy_tracking_path:
            fuzzy_tracking_path = fuzzy_tracking_path.replace('{model_name}', safe_model).replace('{model}', safe_model)
            if experiment_id:
                fuzzy_tracking_path = fuzzy_tracking_path.replace('{experiment_id}', str(experiment_id))
            if run_id is not None:
                fuzzy_tracking_path = fuzzy_tracking_path.replace('{run_id}', str(run_id))

        return cls(
            model_name=yaml_data['model_name'],
            input_folder=yaml_data['input_folder'],
            output_file=formatted_output,
            enable_validation=yaml_data.get('enable_validation', True),
            enable_cleaning=yaml_data.get('enable_cleaning', True),
            max_concurrency=yaml_data.get('max_concurrency', 20),
            num_agents=num_agents,  # Keep for backward compatibility
            num_narrative_agents=num_narrative_agents,
            num_subnarrative_agents=num_subnarrative_agents,
            aggregation_method=aggregation_method,  # Keep for backward compatibility
            narrative_aggregation_method=narrative_aggregation_method,
            subnarrative_aggregation_method=subnarrative_aggregation_method,
            category=yaml_data.get('category'),
            narratives=yaml_data.get('narratives'),
            subnarratives=yaml_data.get('subnarratives'),
            enable_narrative_validation=yaml_data.get('enable_narrative_validation'),
            enable_subnarrative_validation=yaml_data.get('enable_subnarrative_validation'),
            enable_text_cleaning=yaml_data.get('enable_text_cleaning', False),
            cleaning=yaml_data.get('cleaning'),
            # Model parameters for fair comparison
            temperature=yaml_data.get('temperature', 0.0),
            top_p=yaml_data.get('top_p', 1.0),
            max_tokens=yaml_data.get('max_tokens', 4096),
            seed=yaml_data.get('seed'),
            # Experiment metadata
            experiment_id=experiment_id,
            run_id=run_id,
            # Hierarchical prompting strategy
            hierarchical_strategy=yaml_data.get('hierarchical_strategy', 'level_first'),
            # Retrieval-augmented HTC
            enable_retrieval=yaml_data.get('enable_retrieval', False),
            retrieval_top_k=yaml_data.get('retrieval_top_k', 10),
            retrieval_embeddings_path=yaml_data.get('retrieval_embeddings_path'),
            # Heterogeneous ensemble
            narrative_agent_models=yaml_data.get('narrative_agent_models'),
            subnarrative_agent_models=yaml_data.get('subnarrative_agent_models'),
            # Cost tracking
            enable_cost_tracking=yaml_data.get('enable_cost_tracking', False),
            cost_metrics_path=cost_metrics_path,
            # Fuzzy label matching
            enable_fuzzy_matching=yaml_data.get('enable_fuzzy_matching', False),
            fuzzy_threshold=yaml_data.get('fuzzy_threshold', 70.0),
            fuzzy_tracking_path=fuzzy_tracking_path,
            # Vote saving
            enable_vote_saving=yaml_data.get('enable_vote_saving', False),
            # Ollama-specific settings
            ollama_base_url=yaml_data.get('ollama_base_url'),
            ollama_api_key=yaml_data.get('ollama_api_key'),
        )
    
    def validate(self) -> None:
        """Validate the configuration values."""
        if not self.model_name.strip():
            raise ValueError("model_name cannot be empty")
        
        if not self.input_folder.strip():
            raise ValueError("input_folder cannot be empty")
        
        if not self.output_file.strip():
            raise ValueError("output_file cannot be empty")
        
        if self.max_concurrency <= 0:
            raise ValueError("max_concurrency must be positive")
        
        input_path = Path(self.input_folder)
        if not input_path.exists():
            raise ValueError(f"Input folder does not exist: {self.input_folder}")
        
        output_path = Path(self.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    def get_model_for_node(self, node_type: str, operation: str) -> str:
        """
        Get the model name for a specific node and operation.

        Args:
            node_type: 'category', 'narratives', or 'subnarratives'
            operation: 'classification' or 'validation'

        Returns:
            Model name to use (falls back to default if not specified)
        """
        node_config = getattr(self, node_type, None)
        if node_config and operation in node_config:
            return node_config[operation].get('model', self.model_name)
        return self.model_name

    def get_model_params(self, node_type: Optional[str] = None, operation: Optional[str] = None) -> Dict[str, Any]:
        """
        Get model parameters for init_chat_model().

        Supports global parameters with optional per-node overrides.

        Args:
            node_type: Optional node type for per-node overrides ('category', 'narratives', etc.)
            operation: Optional operation for per-node overrides ('classification', 'validation')

        Returns:
            Dictionary of model parameters (temperature, top_p, max_tokens, seed, and Ollama-specific params)
        """
        # Start with global parameters
        params: Dict[str, Any] = {
            'temperature': self.temperature,
            'top_p': self.top_p,
            'max_tokens': self.max_tokens,
        }

        # Only include seed if explicitly set AND provider supports it
        # Providers that support seed: openai, deepseek
        # Providers that DON'T support seed: mistralai, google_genai, anthropic, ollama
        if self.seed is not None:
            provider = self.model_name.split(':')[0].lower() if ':' in self.model_name else ''
            seed_supported_providers = ['openai', 'deepseek', 'azure']
            if provider in seed_supported_providers:
                params['seed'] = self.seed

        # Add Ollama-specific parameters for authenticated/custom endpoints
        # Check config first, then fall back to environment variables
        import os
        provider = self.model_name.split(':')[0].lower() if ':' in self.model_name else ''
        if provider == 'ollama':
            base_url = self.ollama_base_url or os.environ.get('OLLAMA_BASE_URL')
            api_key = self.ollama_api_key or os.environ.get('OLLAMA_API_KEY')
            if base_url:
                params['base_url'] = base_url
            if api_key:
                # Pass auth headers via client_kwargs for httpx client
                params['client_kwargs'] = {
                    'headers': {
                        'Authorization': f'Bearer {api_key}'
                    }
                }

        # Check for per-node parameter overrides
        if node_type:
            node_config = getattr(self, node_type, None)
            if node_config:
                # Check for operation-specific params (e.g., category.classification.params)
                if operation and operation in node_config:
                    op_params = node_config[operation].get('params', {})
                    params.update(op_params)
                # Check for node-level params (e.g., category.params)
                elif 'params' in node_config:
                    params.update(node_config['params'])

        return params

    def is_narrative_validation_enabled(self) -> bool:
        """Check if narrative validation is enabled."""
        if self.enable_narrative_validation is not None:
            return self.enable_narrative_validation
        return self.enable_validation
    
    def is_subnarrative_validation_enabled(self) -> bool:
        """Check if subnarrative validation is enabled."""
        if self.enable_subnarrative_validation is not None:
            return self.enable_subnarrative_validation
        return self.enable_validation

    def get_narrative_agent_model(self, agent_index: int) -> str:
        """
        Get the model name for a specific narrative agent (for heterogeneous ensembles).

        Args:
            agent_index: 0-based index of the agent

        Returns:
            Model name for this agent
        """
        if self.narrative_agent_models and agent_index < len(self.narrative_agent_models):
            return self.narrative_agent_models[agent_index]
        return self.model_name

    def get_subnarrative_agent_model(self, agent_index: int) -> str:
        """
        Get the model name for a specific subnarrative agent (for heterogeneous ensembles).

        Args:
            agent_index: 0-based index of the agent

        Returns:
            Model name for this agent
        """
        if self.subnarrative_agent_models and agent_index < len(self.subnarrative_agent_models):
            return self.subnarrative_agent_models[agent_index]
        return self.model_name

    def is_heterogeneous_ensemble(self) -> bool:
        """Check if this is a heterogeneous ensemble (different models per agent)."""
        return bool(self.narrative_agent_models or self.subnarrative_agent_models)

    def get_all_models_used(self) -> list:
        """Get list of all unique models used in this configuration."""
        models = {self.model_name}
        if self.narrative_agent_models:
            models.update(self.narrative_agent_models)
        if self.subnarrative_agent_models:
            models.update(self.subnarrative_agent_models)
        return list(models)
    
    def __str__(self) -> str:
        """String representation of the configuration."""
        per_node_info = ""
        if self.category or self.narratives or self.subnarratives or self.cleaning:
            per_node_info = "\n  Per-node models:"
            for node in ['category', 'narratives', 'subnarratives', 'cleaning']:
                node_config = getattr(self, node, None)
                if node_config:
                    per_node_info += f"\n    {node}: {node_config}"
        
        # Add granular validation info
        validation_info = ""
        if (self.enable_narrative_validation is not None or 
            self.enable_subnarrative_validation is not None):
            validation_info = "\n  Granular validation:"
            validation_info += f"\n    narratives: {self.is_narrative_validation_enabled()}"
            validation_info += f"\n    subnarratives: {self.is_subnarrative_validation_enabled()}"
        
        # Add model parameters info
        model_params_info = (
            f"\n  Model params: temperature={self.temperature}, top_p={self.top_p}, "
            f"max_tokens={self.max_tokens}, seed={self.seed}"
        )

        # Add experiment metadata if set
        experiment_info = ""
        if self.experiment_id or self.run_id is not None:
            experiment_info = f"\n  Experiment: id={self.experiment_id}, run={self.run_id}"

        return (
            f"ClassificationConfig(\n"
            f"  model_name='{self.model_name}',\n"
            f"  input_folder='{self.input_folder}',\n"
            f"  output_file='{self.output_file}',\n"
            f"  enable_validation={self.enable_validation},\n"
            f"  enable_cleaning={self.enable_cleaning},\n"
            f"  max_concurrency={self.max_concurrency}"
            f"{model_params_info}{experiment_info}{validation_info}{per_node_info}\n"
            f")"
        )


def create_example_config(output_path: str = "config.yaml") -> None:
    """
    Create an example configuration file.

    Args:
        output_path: Path where to save the example config
    """
    example_config = {
        'model_name': 'openai:gpt-5-nano',
        'input_folder': 'testset/EN/subtask-2-documents/',
        'output_file': 'results/experiment_results.txt',
        'enable_validation': True,
        'enable_cleaning': True,
        'max_concurrency': 20,
        # Model parameters for reproducibility
        'temperature': 0.0,
        'top_p': 1.0,
        'max_tokens': 4096,
        # 'seed': 42,  # Uncomment for deterministic runs
        # Experiment metadata (optional)
        # 'experiment_id': 'my_experiment',
        # 'run_id': 1,
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(example_config, f, default_flow_style=False, sort_keys=False)

    print(f"Example configuration saved to: {output_path}")


if __name__ == "__main__":
    create_example_config()

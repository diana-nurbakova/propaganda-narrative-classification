"""
Cost and performance tracking for LLM API calls.

Tracks API calls, token usage, cost, and latency for each document and experiment.
"""

import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from threading import Lock
import json


# Pricing per 1M tokens (as of 2025)
# Update these values as pricing changes
MODEL_PRICING = {
    # OpenAI
    'gpt-5-nano': {'input': 0.10, 'output': 0.40},
    'gpt-4o-mini': {'input': 0.15, 'output': 0.60},
    'gpt-4o': {'input': 2.50, 'output': 10.00},
    'gpt-4-turbo': {'input': 10.00, 'output': 30.00},
    # Google
    'gemini-2.5-flash': {'input': 0.075, 'output': 0.30},
    'gemini-2.5-pro': {'input': 1.25, 'output': 5.00},
    'gemini-2.0-flash': {'input': 0.10, 'output': 0.40},
    # DeepSeek
    'deepseek-chat': {'input': 0.14, 'output': 0.28},
    'deepseek-reasoner': {'input': 0.55, 'output': 2.19},
    # Mistral
    'mistral-large-latest': {'input': 2.00, 'output': 6.00},
    'mistral-small-latest': {'input': 0.20, 'output': 0.60},
    # Anthropic (for heterogeneous ensembles)
    'claude-3-5-sonnet': {'input': 3.00, 'output': 15.00},
    'claude-3-haiku': {'input': 0.25, 'output': 1.25},
}


@dataclass
class APICallMetrics:
    """Metrics for a single API call."""
    timestamp: str
    model: str
    node_type: str  # 'category', 'narratives', 'subnarratives', 'validation', 'cleaning'
    operation: str  # 'classification', 'validation', 'cleaning'
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: float = 0.0
    cost_usd: float = 0.0
    success: bool = True
    error: Optional[str] = None


@dataclass
class DocumentMetrics:
    """Metrics for processing a single document."""
    file_id: str
    start_time: str
    end_time: Optional[str] = None
    total_latency_ms: float = 0.0
    total_api_calls: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost_usd: float = 0.0
    api_calls: List[APICallMetrics] = field(default_factory=list)

    # Classification results for correlation analysis
    num_narratives: int = 0
    num_subnarratives: int = 0
    category: Optional[str] = None


@dataclass
class ExperimentMetrics:
    """Aggregated metrics for an entire experiment."""
    experiment_id: str
    config_name: str
    model_name: str
    start_time: str
    end_time: Optional[str] = None

    # Aggregated counts
    total_documents: int = 0
    total_api_calls: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost_usd: float = 0.0
    total_latency_ms: float = 0.0

    # Per-document breakdown
    documents: List[DocumentMetrics] = field(default_factory=list)

    # Strategy info
    num_narrative_agents: int = 1
    num_subnarrative_agents: int = 1
    aggregation_method: str = "union"
    enable_validation: bool = False
    enable_retrieval: bool = False

    # F1 score (filled after evaluation)
    f1_samples: Optional[float] = None


class CostTracker:
    """
    Thread-safe cost and performance tracker for experiments.

    Usage:
        tracker = CostTracker(experiment_id="exp1", config_name="agora_gpt5nano")

        tracker.start_document("doc1.txt")
        tracker.record_api_call(
            model="gpt-5-nano",
            node_type="narratives",
            operation="classification",
            input_tokens=500,
            output_tokens=100,
            latency_ms=1200.5
        )
        tracker.end_document(num_narratives=3, num_subnarratives=5)

        tracker.save("metrics.json")
    """

    def __init__(
        self,
        experiment_id: str,
        config_name: str,
        model_name: str,
        num_narrative_agents: int = 1,
        num_subnarrative_agents: int = 1,
        aggregation_method: str = "union",
        enable_validation: bool = False,
        enable_retrieval: bool = False,
    ):
        self.metrics = ExperimentMetrics(
            experiment_id=experiment_id,
            config_name=config_name,
            model_name=model_name,
            start_time=datetime.now().isoformat(),
            num_narrative_agents=num_narrative_agents,
            num_subnarrative_agents=num_subnarrative_agents,
            aggregation_method=aggregation_method,
            enable_validation=enable_validation,
            enable_retrieval=enable_retrieval,
        )
        self._current_document: Optional[DocumentMetrics] = None
        self._lock = Lock()

    def _get_model_key(self, model_name: str) -> str:
        """Extract model key from full model name (e.g., 'openai:gpt-5-nano' -> 'gpt-5-nano')."""
        if ':' in model_name:
            return model_name.split(':')[-1]
        return model_name

    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost in USD for given token counts."""
        model_key = self._get_model_key(model)
        pricing = MODEL_PRICING.get(model_key, {'input': 0.0, 'output': 0.0})

        input_cost = (input_tokens / 1_000_000) * pricing['input']
        output_cost = (output_tokens / 1_000_000) * pricing['output']

        return input_cost + output_cost

    def start_document(self, file_id: str) -> None:
        """Start tracking a new document."""
        with self._lock:
            self._current_document = DocumentMetrics(
                file_id=file_id,
                start_time=datetime.now().isoformat(),
            )

    def record_api_call(
        self,
        model: str,
        node_type: str,
        operation: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        latency_ms: float = 0.0,
        success: bool = True,
        error: Optional[str] = None,
    ) -> None:
        """Record metrics for a single API call."""
        cost = self._calculate_cost(model, input_tokens, output_tokens)

        call_metrics = APICallMetrics(
            timestamp=datetime.now().isoformat(),
            model=model,
            node_type=node_type,
            operation=operation,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            cost_usd=cost,
            success=success,
            error=error,
        )

        with self._lock:
            if self._current_document:
                self._current_document.api_calls.append(call_metrics)
                self._current_document.total_api_calls += 1
                self._current_document.total_input_tokens += input_tokens
                self._current_document.total_output_tokens += output_tokens
                self._current_document.total_latency_ms += latency_ms
                self._current_document.total_cost_usd += cost

            # Also update experiment totals
            self.metrics.total_api_calls += 1
            self.metrics.total_input_tokens += input_tokens
            self.metrics.total_output_tokens += output_tokens
            self.metrics.total_latency_ms += latency_ms
            self.metrics.total_cost_usd += cost

    def end_document(
        self,
        num_narratives: int = 0,
        num_subnarratives: int = 0,
        category: Optional[str] = None,
    ) -> None:
        """End tracking for the current document."""
        with self._lock:
            if self._current_document:
                self._current_document.end_time = datetime.now().isoformat()
                self._current_document.num_narratives = num_narratives
                self._current_document.num_subnarratives = num_subnarratives
                self._current_document.category = category

                self.metrics.documents.append(self._current_document)
                self.metrics.total_documents += 1
                self._current_document = None

    def set_f1_score(self, f1_samples: float) -> None:
        """Set the F1 score after evaluation."""
        self.metrics.f1_samples = f1_samples

    def finalize(self) -> None:
        """Finalize the experiment metrics."""
        self.metrics.end_time = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        def dataclass_to_dict(obj):
            if hasattr(obj, '__dataclass_fields__'):
                return {k: dataclass_to_dict(v) for k, v in obj.__dict__.items()}
            elif isinstance(obj, list):
                return [dataclass_to_dict(item) for item in obj]
            else:
                return obj

        return dataclass_to_dict(self.metrics)

    def save(self, output_path: str) -> None:
        """Save metrics to JSON file."""
        self.finalize()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of experiment metrics."""
        avg_latency_per_doc = (
            self.metrics.total_latency_ms / self.metrics.total_documents
            if self.metrics.total_documents > 0 else 0
        )
        avg_calls_per_doc = (
            self.metrics.total_api_calls / self.metrics.total_documents
            if self.metrics.total_documents > 0 else 0
        )
        avg_cost_per_doc = (
            self.metrics.total_cost_usd / self.metrics.total_documents
            if self.metrics.total_documents > 0 else 0
        )

        return {
            'experiment_id': self.metrics.experiment_id,
            'model': self.metrics.model_name,
            'total_documents': self.metrics.total_documents,
            'total_api_calls': self.metrics.total_api_calls,
            'total_cost_usd': round(self.metrics.total_cost_usd, 4),
            'total_latency_sec': round(self.metrics.total_latency_ms / 1000, 2),
            'avg_latency_per_doc_sec': round(avg_latency_per_doc / 1000, 2),
            'avg_calls_per_doc': round(avg_calls_per_doc, 1),
            'avg_cost_per_doc_usd': round(avg_cost_per_doc, 6),
            'f1_samples': self.metrics.f1_samples,
            'config': {
                'num_narrative_agents': self.metrics.num_narrative_agents,
                'num_subnarrative_agents': self.metrics.num_subnarrative_agents,
                'aggregation_method': self.metrics.aggregation_method,
                'enable_validation': self.metrics.enable_validation,
            }
        }


class TimingContext:
    """Context manager for timing operations."""

    def __init__(self):
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.latency_ms: float = 0.0

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end_time = time.perf_counter()
        self.latency_ms = (self.end_time - self.start_time) * 1000


def create_cost_performance_table(metrics_files: List[str]) -> List[Dict[str, Any]]:
    """
    Create a cost-performance comparison table from multiple experiment metrics.

    Args:
        metrics_files: List of paths to metrics JSON files

    Returns:
        List of dictionaries suitable for creating a comparison table
    """
    rows = []

    for metrics_path in metrics_files:
        with open(metrics_path, 'r', encoding='utf-8') as f:
            metrics = json.load(f)

        num_docs = metrics.get('total_documents', 0)

        row = {
            'config': metrics.get('config_name', 'unknown'),
            'model': metrics.get('model_name', 'unknown'),
            'num_agents': metrics.get('num_narrative_agents', 1),
            'aggregation': metrics.get('aggregation_method', 'union'),
            'validation': metrics.get('enable_validation', False),
            'api_calls': metrics.get('total_api_calls', 0),
            'cost_usd': round(metrics.get('total_cost_usd', 0), 4),
            'latency_sec': round(metrics.get('total_latency_ms', 0) / 1000, 2),
            'avg_latency_sec': round(
                (metrics.get('total_latency_ms', 0) / num_docs / 1000) if num_docs > 0 else 0, 2
            ),
            'f1_samples': metrics.get('f1_samples'),
        }
        rows.append(row)

    # Sort by F1 score descending
    rows.sort(key=lambda x: x.get('f1_samples') or 0, reverse=True)

    return rows

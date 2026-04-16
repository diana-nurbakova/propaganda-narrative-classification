"""
Retrieval-augmented Hierarchical Text Classification.

Uses pre-computed label embeddings to filter to top-K candidate labels
before LLM classification, reducing the label space and potentially
improving precision.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

# Try to import torch for embedding operations
try:
    import torch
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("Warning: PyTorch not available. Retrieval filtering disabled.")

# Try to import sentence transformers for text embedding
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers not available. Will use cached embeddings only.")


class LabelRetriever:
    """
    Retrieves top-K candidate labels based on semantic similarity.

    Uses pre-computed label embeddings and computes text embeddings on-the-fly
    to find the most relevant labels for a given input text.
    """

    def __init__(
        self,
        embeddings_path: str = "embeddings/",
        embedding_model: str = "all-MiniLM-L6-v2",
        device: Optional[str] = None,
    ):
        """
        Initialize the label retriever.

        Args:
            embeddings_path: Path to directory containing label_embeddings.pt
            embedding_model: Name of sentence transformer model for text embedding
            device: Device for computation ('cuda', 'cpu', or None for auto)
        """
        if not TORCH_AVAILABLE:
            raise RuntimeError("PyTorch is required for retrieval filtering")

        self.embeddings_path = Path(embeddings_path)
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')

        # Load pre-computed label embeddings
        self.label_embeddings = None
        self.label_names = None
        self.narrative_embeddings = None
        self.narrative_names = None
        self.subnarrative_embeddings = None
        self.subnarrative_names = None

        self._load_label_embeddings()

        # Initialize text embedding model
        self.text_encoder = None
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            self.text_encoder = SentenceTransformer(embedding_model, device=self.device)

    def _load_label_embeddings(self) -> None:
        """Load pre-computed label embeddings from disk."""
        embeddings_file = self.embeddings_path / "label_embeddings.pt"

        if not embeddings_file.exists():
            print(f"Warning: Label embeddings not found at {embeddings_file}")
            return

        data = torch.load(embeddings_file, map_location=self.device)

        # Handle different embedding formats
        if isinstance(data, dict):
            # New format with separate narrative/subnarrative embeddings
            if 'narrative_embeddings' in data:
                self.narrative_embeddings = data['narrative_embeddings']
                self.narrative_names = data.get('narrative_names', [])
            if 'subnarrative_embeddings' in data:
                self.subnarrative_embeddings = data['subnarrative_embeddings']
                self.subnarrative_names = data.get('subnarrative_names', [])
            if 'label_embeddings' in data:
                self.label_embeddings = data['label_embeddings']
                self.label_names = data.get('label_names', [])
        else:
            # Legacy format: single tensor
            self.label_embeddings = data

        print(f"Loaded label embeddings from {embeddings_file}")
        if self.narrative_embeddings is not None:
            print(f"  Narratives: {len(self.narrative_names)} labels")
        if self.subnarrative_embeddings is not None:
            print(f"  Subnarratives: {len(self.subnarrative_names)} labels")

    def encode_text(self, text: str) -> torch.Tensor:
        """
        Encode input text to embedding vector.

        Args:
            text: Input text to encode

        Returns:
            Embedding tensor
        """
        if self.text_encoder is None:
            raise RuntimeError("Text encoder not available")

        embedding = self.text_encoder.encode(
            text,
            convert_to_tensor=True,
            device=self.device,
        )
        return embedding

    def retrieve_top_k_narratives(
        self,
        text: str,
        category: str,
        k: int = 10,
        available_narratives: Optional[List[str]] = None,
    ) -> List[Tuple[str, float]]:
        """
        Retrieve top-K candidate narratives for the given text.

        Args:
            text: Input document text
            category: Category classification (CC or URW)
            k: Number of candidates to retrieve
            available_narratives: Optional list of valid narrative names to filter to

        Returns:
            List of (narrative_name, similarity_score) tuples, sorted by score
        """
        if self.narrative_embeddings is None or self.narrative_names is None:
            # Fall back to returning all available narratives
            if available_narratives:
                return [(n, 1.0) for n in available_narratives[:k]]
            return []

        # Encode the input text
        text_embedding = self.encode_text(text)

        # Filter to narratives for this category
        if available_narratives:
            valid_indices = [
                i for i, name in enumerate(self.narrative_names)
                if name in available_narratives or name.split(": ")[-1] in available_narratives
            ]
        else:
            # Filter by category prefix
            valid_indices = [
                i for i, name in enumerate(self.narrative_names)
                if name.startswith(f"{category}:")
            ]

        if not valid_indices:
            if available_narratives:
                return [(n, 1.0) for n in available_narratives[:k]]
            return []

        # Get embeddings for valid narratives
        valid_embeddings = self.narrative_embeddings[valid_indices]
        valid_names = [self.narrative_names[i] for i in valid_indices]

        # Compute cosine similarity
        similarities = F.cosine_similarity(
            text_embedding.unsqueeze(0),
            valid_embeddings,
            dim=1
        )

        # Get top-K
        k = min(k, len(valid_names))
        top_k_indices = torch.topk(similarities, k).indices.tolist()
        top_k_scores = similarities[top_k_indices].tolist()

        return [(valid_names[i], top_k_scores[j]) for j, i in enumerate(top_k_indices)]

    def retrieve_top_k_subnarratives(
        self,
        text: str,
        parent_narrative: str,
        k: int = 10,
        available_subnarratives: Optional[List[str]] = None,
    ) -> List[Tuple[str, float]]:
        """
        Retrieve top-K candidate subnarratives for the given text and parent narrative.

        Args:
            text: Input document text
            parent_narrative: Parent narrative name
            k: Number of candidates to retrieve
            available_subnarratives: Optional list of valid subnarrative names

        Returns:
            List of (subnarrative_name, similarity_score) tuples, sorted by score
        """
        if self.subnarrative_embeddings is None or self.subnarrative_names is None:
            # Fall back to returning all available subnarratives
            if available_subnarratives:
                return [(s, 1.0) for s in available_subnarratives[:k]]
            return []

        # Encode the input text
        text_embedding = self.encode_text(text)

        # Filter to subnarratives for this parent narrative
        if available_subnarratives:
            valid_indices = [
                i for i, name in enumerate(self.subnarrative_names)
                if name in available_subnarratives or name.split(": ")[-1] in available_subnarratives
            ]
        else:
            # Filter by parent narrative prefix
            valid_indices = [
                i for i, name in enumerate(self.subnarrative_names)
                if parent_narrative in name
            ]

        if not valid_indices:
            if available_subnarratives:
                return [(s, 1.0) for s in available_subnarratives[:k]]
            return []

        # Get embeddings for valid subnarratives
        valid_embeddings = self.subnarrative_embeddings[valid_indices]
        valid_names = [self.subnarrative_names[i] for i in valid_indices]

        # Compute cosine similarity
        similarities = F.cosine_similarity(
            text_embedding.unsqueeze(0),
            valid_embeddings,
            dim=1
        )

        # Get top-K
        k = min(k, len(valid_names))
        top_k_indices = torch.topk(similarities, k).indices.tolist()
        top_k_scores = similarities[top_k_indices].tolist()

        return [(valid_names[i], top_k_scores[j]) for j, i in enumerate(top_k_indices)]


def create_label_embeddings(
    taxonomy_path: str = "data/taxonomy.json",
    narrative_definitions_path: str = "data/narrative_definitions.csv",
    subnarrative_definitions_path: str = "data/subnarrative_definitions.csv",
    output_path: str = "embeddings/label_embeddings.pt",
    model_name: str = "all-MiniLM-L6-v2",
) -> None:
    """
    Create label embeddings from taxonomy and definitions.

    This pre-computes embeddings for all narratives and subnarratives
    using their definitions and examples.

    Args:
        taxonomy_path: Path to taxonomy.json
        narrative_definitions_path: Path to narrative_definitions.csv
        subnarrative_definitions_path: Path to subnarrative_definitions.csv
        output_path: Path to save embeddings
        model_name: Sentence transformer model to use
    """
    import json
    import pandas as pd

    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        raise RuntimeError("sentence-transformers required for creating embeddings")

    print(f"Creating label embeddings using {model_name}...")

    # Load taxonomy
    with open(taxonomy_path, 'r') as f:
        taxonomy = json.load(f)

    # Load definitions
    narr_df = pd.read_csv(narrative_definitions_path)
    subnarr_df = pd.read_csv(subnarrative_definitions_path)

    # Create definition lookup
    narr_defs = {}
    for _, row in narr_df.iterrows():
        name = row.get('narrative', '')
        if pd.isna(name):
            continue
        definition = row.get('definition', '')
        example = row.get('example', '')
        narr_defs[name] = f"{name}: {definition} Example: {example}" if definition else name

    subnarr_defs = {}
    for _, row in subnarr_df.iterrows():
        name = row.get('subnarrative', '')
        if pd.isna(name):
            continue
        definition = row.get('definition', '')
        example = row.get('example', '')
        subnarr_defs[name] = f"{name}: {definition} Example: {example}" if definition else name

    # Collect all labels with their text representations
    narrative_texts = []
    narrative_names = []
    subnarrative_texts = []
    subnarrative_names = []

    for category, narratives in taxonomy.items():
        for narrative, subnarratives in narratives.items():
            # Full narrative name
            full_narr_name = f"{category}: {narrative}"
            narrative_names.append(full_narr_name)
            narrative_texts.append(narr_defs.get(narrative, narrative))

            for subnarrative in subnarratives:
                full_subnarr_name = f"{full_narr_name}: {subnarrative}"
                subnarrative_names.append(full_subnarr_name)
                subnarrative_texts.append(subnarr_defs.get(subnarrative, subnarrative))

    print(f"Encoding {len(narrative_names)} narratives and {len(subnarrative_names)} subnarratives...")

    # Initialize encoder
    encoder = SentenceTransformer(model_name)

    # Encode labels
    narrative_embeddings = encoder.encode(
        narrative_texts,
        convert_to_tensor=True,
        show_progress_bar=True,
    )
    subnarrative_embeddings = encoder.encode(
        subnarrative_texts,
        convert_to_tensor=True,
        show_progress_bar=True,
    )

    # Save embeddings
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    torch.save({
        'narrative_embeddings': narrative_embeddings,
        'narrative_names': narrative_names,
        'subnarrative_embeddings': subnarrative_embeddings,
        'subnarrative_names': subnarrative_names,
        'model_name': model_name,
    }, output_path)

    print(f"Saved label embeddings to {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create or test label embeddings")
    parser.add_argument(
        "--create",
        action="store_true",
        help="Create new label embeddings"
    )
    parser.add_argument(
        "--test",
        type=str,
        help="Test retrieval with sample text"
    )

    args = parser.parse_args()

    if args.create:
        create_label_embeddings()
    elif args.test:
        retriever = LabelRetriever()
        print(f"\nTop narratives for: '{args.test[:100]}...'")
        results = retriever.retrieve_top_k_narratives(args.test, "URW", k=5)
        for name, score in results:
            print(f"  {score:.3f}: {name}")
    else:
        parser.print_help()

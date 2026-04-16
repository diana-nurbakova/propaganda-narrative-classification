#!/usr/bin/env python3
"""
Confusion-aware hard-negative mining for the disambiguation pipeline.

Reads the bistochastic-normalised TCM output from
``enhanced_experiment_report.py --tcm-output-dir`` and the training
annotations, computes sentence embeddings for training documents, mines
hard negatives for the top confused narrative pairs, and writes
``data/disambiguation_pairs.json`` — the file consumed by the
``disambiguate_narratives_node()`` at inference time.

Usage::

    # Step 1: generate TCM matrices (if not done already)
    python -m src.analysis.enhanced_experiment_report \\
        --experiments-dir results/experiments/ \\
        --tcm-output-dir results/analysis/tcm/

    # Step 2: mine hard negatives
    python -m src.analysis.confusion_retrieval \\
        --tcm-dir results/analysis/tcm/ \\
        --annotations data/all-texts-unified/unified-annotations.tsv \\
        --texts-dir data/all-texts-unified/texts/ \\
        --output data/disambiguation_pairs.json \\
        --top-k-pairs 10 --examples-per-side 3

Spec reference: ``specs/agora_emnlp_spec.md`` §7.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_annotations_grouped(
    annotations_path: str,
    texts_dir: str,
) -> Dict[str, List[Dict[str, str]]]:
    """Load training annotations grouped by bare narrative name.

    Returns a dict mapping ``narrative_name`` → list of
    ``{"file_id": ..., "text": ..., "language": ...}``.
    """
    out: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    with open(annotations_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 2:
                continue
            file_id = parts[0].strip()
            narrs = [n.strip() for n in parts[1].split(";") if n.strip() and n.strip().lower() != "other"]
            text_path = os.path.join(texts_dir, file_id)
            if not os.path.exists(text_path):
                continue
            with open(text_path, "r", encoding="utf-8", errors="replace") as tf:
                text = tf.read().strip()
            if not text:
                continue
            # infer language from filename
            lang = None
            for token in file_id.upper().split("_")[:3]:
                if token in {"EN", "BG", "HI", "PT", "RU"}:
                    lang = token
                    break
            for narr in narrs:
                m = re.match(r"^(URW|CC):\s*", narr)
                bare = narr[m.end():] if m else narr
                out[bare].append({"file_id": file_id, "text": text, "language": lang or ""})
    return dict(out)


def load_top_confused_pairs(
    tcm_dir: str, top_k: int = 10
) -> List[Dict[str, Any]]:
    """Aggregate top confused pairs across all per-experiment
    ``*_top_confused.json`` files in the TCM output directory.
    Deduplicates and ranks by max bistochastic mass.
    """
    pairs_by_key: Dict[Tuple[str, str], float] = {}
    for fname in sorted(os.listdir(tcm_dir)):
        if not fname.endswith("_top_confused.json"):
            continue
        with open(os.path.join(tcm_dir, fname), "r", encoding="utf-8") as f:
            for p in json.load(f):
                key = (p["gold"], p["predicted"])
                mass = p.get("bis_mass", 0.0)
                if key not in pairs_by_key or mass > pairs_by_key[key]:
                    pairs_by_key[key] = mass

    ranked = sorted(pairs_by_key.items(), key=lambda x: -x[1])
    return [
        {"gold": k[0], "predicted": k[1], "bis_mass": v}
        for k, v in ranked[:top_k]
    ]


def _truncate(text: str, max_chars: int = 300) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + "..."


# ---------------------------------------------------------------------------
# Hard-negative mining
# ---------------------------------------------------------------------------

def mine_hard_negatives(
    pair: Dict[str, str],
    docs_by_narrative: Dict[str, List[Dict[str, str]]],
    examples_per_side: int = 3,
    encoder: Any = None,
) -> Dict[str, Any]:
    """For a confused pair (A, B), find training docs labelled A that are
    closest to B's prototype (and vice versa). These are the hard negatives.

    If ``encoder`` (a SentenceTransformer) is provided, similarity is
    computed via cosine distance. Otherwise, a simple random sample is used
    as a fallback.
    """
    a_name = pair["gold"]
    b_name = pair["predicted"]
    a_docs = docs_by_narrative.get(a_name, [])
    b_docs = docs_by_narrative.get(b_name, [])

    if not a_docs or not b_docs:
        return {
            "label_a": a_name,
            "label_b": b_name,
            "hard_negatives_a": [],
            "hard_negatives_b": [],
        }

    if encoder is not None:
        a_texts = [d["text"] for d in a_docs]
        b_texts = [d["text"] for d in b_docs]

        a_emb = encoder.encode(a_texts, convert_to_numpy=True, show_progress_bar=False)
        b_emb = encoder.encode(b_texts, convert_to_numpy=True, show_progress_bar=False)

        proto_a = a_emb.mean(axis=0, keepdims=True)
        proto_b = b_emb.mean(axis=0, keepdims=True)

        # A docs closest to B prototype
        a_to_b = np.dot(a_emb, proto_b.T).flatten()
        a_to_b /= np.linalg.norm(a_emb, axis=1) * np.linalg.norm(proto_b) + 1e-9
        a_top_idx = a_to_b.argsort()[::-1][:examples_per_side]

        # B docs closest to A prototype
        b_to_a = np.dot(b_emb, proto_a.T).flatten()
        b_to_a /= np.linalg.norm(b_emb, axis=1) * np.linalg.norm(proto_a) + 1e-9
        b_top_idx = b_to_a.argsort()[::-1][:examples_per_side]

        hard_a = [
            {"excerpt": _truncate(a_texts[i]), "file_id": a_docs[i]["file_id"]}
            for i in a_top_idx
        ]
        hard_b = [
            {"excerpt": _truncate(b_texts[i]), "file_id": b_docs[i]["file_id"]}
            for i in b_top_idx
        ]
    else:
        # Random fallback
        import random
        random.seed(42)
        sel_a = random.sample(a_docs, min(examples_per_side, len(a_docs)))
        sel_b = random.sample(b_docs, min(examples_per_side, len(b_docs)))
        hard_a = [{"excerpt": _truncate(d["text"]), "file_id": d["file_id"]} for d in sel_a]
        hard_b = [{"excerpt": _truncate(d["text"]), "file_id": d["file_id"]} for d in sel_b]

    return {
        "label_a": a_name,
        "label_b": b_name,
        "hard_negatives_a": hard_a,
        "hard_negatives_b": hard_b,
    }


def add_decision_rules(
    pairs: List[Dict[str, Any]],
    rules_path: str = "data/annotation_guideline_rules.json",
) -> List[Dict[str, Any]]:
    """Enrich pair dicts with any decision rule from the annotation guidelines."""
    if not os.path.exists(rules_path):
        return pairs
    with open(rules_path, "r", encoding="utf-8") as f:
        rules = json.load(f)
    confused = rules.get("confused_pairs", [])
    rule_map: Dict[frozenset, str] = {}
    for cp in confused:
        labels = cp.get("labels", [])
        # Strip domain prefix for matching
        bare_labels = []
        for l in labels:
            m = re.match(r"^(URW|CC):\s*", l)
            bare_labels.append(l[m.end():] if m else l)
        key = frozenset(bare_labels)
        rule_map[key] = cp.get("decision_rule", "")
    # Also build bare key from "Narrative: subnarrative" → "Narrative" for narrative-level
    for cp in confused:
        labels = cp.get("labels", [])
        bare_narrs = []
        for l in labels:
            m = re.match(r"^(URW|CC):\s*", l)
            partial = l[m.end():] if m else l
            # Extract just the narrative name
            narr_part = partial.split(":")[0].strip()
            bare_narrs.append(narr_part)
        key = frozenset(bare_narrs)
        if key not in rule_map:
            rule_map[key] = cp.get("decision_rule", "")

    for p in pairs:
        key = frozenset([p.get("label_a", ""), p.get("label_b", "")])
        p["decision_rule"] = rule_map.get(key, "")
    return pairs


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Mine hard negatives for confused narrative pairs."
    )
    parser.add_argument("--tcm-dir", default="results/analysis/tcm/")
    parser.add_argument(
        "--annotations",
        default="data/all-texts-unified/unified-annotations.tsv",
    )
    parser.add_argument(
        "--texts-dir",
        default="data/all-texts-unified/texts/",
    )
    parser.add_argument("--output", default="data/disambiguation_pairs.json")
    parser.add_argument("--top-k-pairs", type=int, default=10)
    parser.add_argument("--examples-per-side", type=int, default=3)
    parser.add_argument(
        "--embedding-model",
        default="paraphrase-multilingual-mpnet-base-v2",
        help="SentenceTransformer model for hard-neg mining. "
        "Set to 'none' to use random sampling instead.",
    )
    args = parser.parse_args()

    # Load confused pairs from TCM
    if not os.path.isdir(args.tcm_dir):
        print(
            f"[confusion-retrieval] TCM directory not found: {args.tcm_dir}\n"
            "Run enhanced_experiment_report.py --tcm-output-dir first."
        )
        return 1

    top_pairs = load_top_confused_pairs(args.tcm_dir, args.top_k_pairs)
    print(f"[confusion-retrieval] Top {len(top_pairs)} confused pairs loaded from TCM")

    # Load training docs
    docs_by_narr = load_annotations_grouped(args.annotations, args.texts_dir)
    print(f"[confusion-retrieval] Training docs: {sum(len(v) for v in docs_by_narr.values())} across {len(docs_by_narr)} narratives")

    # Optionally load encoder
    encoder = None
    if args.embedding_model.lower() != "none":
        try:
            from sentence_transformers import SentenceTransformer
            encoder = SentenceTransformer(args.embedding_model)
            print(f"[confusion-retrieval] Loaded encoder: {args.embedding_model}")
        except ImportError:
            print("[confusion-retrieval] sentence-transformers not available; using random sampling")

    # Mine hard negatives for each pair
    result_pairs = []
    for p in top_pairs:
        mined = mine_hard_negatives(
            p, docs_by_narr,
            examples_per_side=args.examples_per_side,
            encoder=encoder,
        )
        mined["bis_mass"] = p.get("bis_mass", 0.0)
        result_pairs.append(mined)
        n_a = len(mined["hard_negatives_a"])
        n_b = len(mined["hard_negatives_b"])
        print(f"  {mined['label_a']} <-> {mined['label_b']}: {n_a}+{n_b} examples")

    result_pairs = add_decision_rules(result_pairs)

    out = {"pairs": result_pairs}
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"[confusion-retrieval] Written to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

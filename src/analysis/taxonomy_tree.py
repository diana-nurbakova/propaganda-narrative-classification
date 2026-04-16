#!/usr/bin/env python3
"""
Taxonomy tree for the SemEval-2025 Task 10 narrative taxonomy.

Builds a 3-level tree (Root -> Domain[URW/CC] -> Narrative -> Sub-narrative)
and provides label parsing utilities for working with the prediction file
format used throughout this project, where labels are stored as semicolon
separated strings of the form:

    "URW: <narrative name>"
    "URW: <narrative name>: <sub-narrative name>"

This module is the shared backbone for the hierarchical evaluation suite
(``hierarchical_metrics.py``, ``bistochastic_tcm.py``,
``enhanced_experiment_report.py``).

It is dependency-light (stdlib only) so it can be imported by anything.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple

ROOT = "Root"
OTHER = "Other"
DEFAULT_TAXONOMY_PATH = Path(__file__).resolve().parents[2] / "data" / "taxonomy.json"


@dataclass
class TaxonomyTree:
    """In-memory representation of the narrative taxonomy.

    Node IDs are strings — domain nodes are ``"URW"`` / ``"CC"``, narrative
    nodes are the bare narrative name (e.g. ``"Discrediting Ukraine"``) and
    sub-narrative nodes are stored as ``"<narrative>::<sub-narrative>"`` to
    avoid collisions across domains.
    """

    domains: List[str] = field(default_factory=list)
    narratives: List[str] = field(default_factory=list)
    subnarratives: List[str] = field(default_factory=list)

    parent: Dict[str, Optional[str]] = field(default_factory=dict)
    children: Dict[str, List[str]] = field(default_factory=dict)
    depth: Dict[str, int] = field(default_factory=dict)
    domain_of: Dict[str, str] = field(default_factory=dict)

    # Original taxonomy dict (domain -> narrative -> [subnarratives])
    raw: Dict[str, Dict[str, List[str]]] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def from_json(cls, path: Path | str = DEFAULT_TAXONOMY_PATH) -> "TaxonomyTree":
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return cls.from_dict(raw)

    @classmethod
    def from_dict(cls, raw: Dict[str, Dict[str, List[str]]]) -> "TaxonomyTree":
        tree = cls(raw=raw)
        tree.parent[ROOT] = None
        tree.children[ROOT] = []
        tree.depth[ROOT] = 0

        for domain, narratives in raw.items():
            tree.domains.append(domain)
            tree.parent[domain] = ROOT
            tree.children[ROOT].append(domain)
            tree.children[domain] = []
            tree.depth[domain] = 1
            tree.domain_of[domain] = domain

            for narr_name, subs in narratives.items():
                narr_id = narr_name
                tree.narratives.append(narr_id)
                tree.parent[narr_id] = domain
                tree.children[domain].append(narr_id)
                tree.children[narr_id] = []
                tree.depth[narr_id] = 2
                tree.domain_of[narr_id] = domain

                for sub_name in subs:
                    sub_id = f"{narr_id}::{sub_name}"
                    tree.subnarratives.append(sub_id)
                    tree.parent[sub_id] = narr_id
                    tree.children[narr_id].append(sub_id)
                    tree.children[sub_id] = []
                    tree.depth[sub_id] = 3
                    tree.domain_of[sub_id] = domain

        return tree

    # ------------------------------------------------------------------
    # Tree queries
    # ------------------------------------------------------------------

    def ancestors(self, node: str, include_self: bool = True) -> List[str]:
        """Return all ancestors of a node up to and including the root."""
        result = []
        if include_self and node in self.parent:
            result.append(node)
        cur = self.parent.get(node)
        while cur is not None:
            result.append(cur)
            cur = self.parent.get(cur)
        return result

    def lca(self, a: str, b: str) -> Optional[str]:
        """Lowest common ancestor of two nodes (None if either is unknown)."""
        if a not in self.parent or b not in self.parent:
            return None
        anc_a = self.ancestors(a, include_self=True)
        anc_b_set = set(self.ancestors(b, include_self=True))
        for n in anc_a:  # ordered from deepest to root
            if n in anc_b_set:
                return n
        return None

    # ------------------------------------------------------------------
    # Label parsing — convert SemEval-style label strings to tree nodes
    # ------------------------------------------------------------------

    def parse_narrative_label(self, label: str) -> Optional[str]:
        """Parse a narrative label string like ``"URW: Discrediting Ukraine"``.

        Returns the narrative node id, or ``None`` for ``"Other"``/empty/unknown.
        """
        if not label:
            return None
        s = label.strip()
        if not s or s.lower() in ("other", "none"):
            return None
        # Strip leading domain prefix
        for dom in self.domains:
            prefix = f"{dom}:"
            if s.startswith(prefix):
                s = s[len(prefix):].strip()
                break
        s = s.rstrip(":").strip()
        return s if s in self.children else None  # narrative names are keys in children

    def parse_subnarrative_label(self, label: str) -> Optional[str]:
        """Parse a sub-narrative label string of the form
        ``"URW: <narrative>: <sub-narrative>"`` and return the sub-narrative
        node id, or ``None`` for ``"Other"``/unknown.
        """
        if not label:
            return None
        s = label.strip()
        if not s or s.lower() in ("other", "none"):
            return None
        # Strip leading domain prefix
        for dom in self.domains:
            prefix = f"{dom}:"
            if s.startswith(prefix):
                s = s[len(prefix):].strip()
                break
        # Split on the first ": " to separate narrative from sub-narrative
        if ":" not in s:
            return None
        narr, sub = s.split(":", 1)
        narr = narr.strip()
        sub = sub.strip()
        if not narr or not sub:
            return None
        sub_id = f"{narr}::{sub}"
        if sub_id in self.parent:
            return sub_id
        # Fallback: case/whitespace-insensitive match
        norm = lambda x: " ".join(x.lower().split())
        for cand in self.children.get(narr, []):
            if norm(cand.split("::", 1)[1]) == norm(sub):
                return cand
        return None

    def parse_labels(
        self,
        narrative_strings: Iterable[str],
        subnarrative_strings: Iterable[str],
    ) -> Tuple[Set[str], Set[str]]:
        """Convert raw label strings (one document) to sets of node ids.

        Returns ``(narrative_node_ids, subnarrative_node_ids)``.
        """
        narrs: Set[str] = set()
        subs: Set[str] = set()
        for n in narrative_strings:
            nid = self.parse_narrative_label(n)
            if nid is not None:
                narrs.add(nid)
        for s in subnarrative_strings:
            sid = self.parse_subnarrative_label(s)
            if sid is not None:
                subs.add(sid)
                # ensure parent narrative is implicitly known
                parent = self.parent.get(sid)
                if parent and parent in self.children:
                    narrs.add(parent)
        return narrs, subs

    def augment_with_ancestors(
        self,
        narratives: Set[str],
        subnarratives: Set[str],
        include_root: bool = True,
    ) -> Set[str]:
        """Augment a label set with all ancestor nodes (Domain, Root)."""
        out: Set[str] = set()
        for sub in subnarratives:
            for anc in self.ancestors(sub, include_self=True):
                out.add(anc)
        for narr in narratives:
            for anc in self.ancestors(narr, include_self=True):
                out.add(anc)
        if not include_root:
            out.discard(ROOT)
        return out


def load_default_tree() -> TaxonomyTree:
    """Convenience: load the default project taxonomy."""
    return TaxonomyTree.from_json(DEFAULT_TAXONOMY_PATH)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    tree = load_default_tree()
    print(f"Domains:        {len(tree.domains)} -> {tree.domains}")
    print(f"Narratives:     {len(tree.narratives)}")
    print(f"Sub-narratives: {len(tree.subnarratives)}")
    sample = "URW: Discrediting the West, Diplomacy: The West does not care about Ukraine, only about its interests"
    sid = tree.parse_subnarrative_label(sample)
    print(f"\nParsed sub-narrative example -> {sid}")
    print(f"  ancestors: {tree.ancestors(sid)}")

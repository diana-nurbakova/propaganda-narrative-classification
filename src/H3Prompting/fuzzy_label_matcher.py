"""
Fuzzy label matching for handling model-specific label variations.

Some models (e.g., Mistral) return labels that semantically match the taxonomy
but don't use the exact label names. This module provides fuzzy matching to
map these variations to canonical taxonomy labels.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from rapidfuzz import fuzz, process


@dataclass
class LabelMatchResult:
    """Result of a fuzzy label match."""
    original_label: str
    matched_label: Optional[str]
    score: float
    matched: bool


@dataclass
class FuzzyMatchTracker:
    """Tracks fuzzy matching results for analysis."""
    matches: List[Dict] = field(default_factory=list)

    def add_match(self, file_id: str, label_type: str, original: str,
                  matched: Optional[str], score: float):
        """Record a fuzzy match attempt."""
        self.matches.append({
            "file_id": file_id,
            "label_type": label_type,  # "narrative" or "subnarrative"
            "original_label": original,
            "matched_label": matched,
            "score": score,
            "matched": matched is not None
        })

    def save(self, output_path: str):
        """Save match tracking to JSON file."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Compute summary statistics
        total = len(self.matches)
        matched = sum(1 for m in self.matches if m["matched"])
        unmatched = total - matched

        summary = {
            "total_labels": total,
            "matched_labels": matched,
            "unmatched_labels": unmatched,
            "match_rate": matched / total if total > 0 else 0,
            "matches": self.matches
        }

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)

    def get_summary(self) -> Dict:
        """Get summary of match results."""
        total = len(self.matches)
        matched = sum(1 for m in self.matches if m["matched"])

        return {
            "total": total,
            "matched": matched,
            "unmatched": total - matched,
            "match_rate": matched / total if total > 0 else 0
        }


class FuzzyLabelMatcher:
    """
    Fuzzy matcher for mapping model outputs to canonical taxonomy labels.

    Uses rapidfuzz for efficient string matching with configurable thresholds.
    """

    def __init__(self, valid_labels: List[str], threshold: float = 70.0):
        """
        Initialize the fuzzy matcher.

        Args:
            valid_labels: List of valid canonical labels from taxonomy
            threshold: Minimum score (0-100) to accept a match
        """
        self.valid_labels = list(valid_labels)
        self.threshold = threshold
        self.tracker = FuzzyMatchTracker()

        # Build alternative representations for better matching
        self._build_label_index()

    def _build_label_index(self):
        """Build index of labels and their simplified forms for matching."""
        self.label_index = {}
        self.simplified_to_canonical = {}

        for label in self.valid_labels:
            # Store original
            self.label_index[label.lower()] = label

            # Store without category prefix (e.g., "CC: " or "URW: ")
            if ": " in label:
                parts = label.split(": ", 1)
                if len(parts) == 2:
                    simplified = parts[1].lower()
                    self.simplified_to_canonical[simplified] = label

                    # Also store the part after the last colon for subnarratives
                    if ": " in parts[1]:
                        sub_parts = parts[1].split(": ", 1)
                        if len(sub_parts) == 2:
                            self.simplified_to_canonical[sub_parts[1].lower()] = label

    def match(self, label: str, file_id: str = "", label_type: str = "narrative") -> LabelMatchResult:
        """
        Find the best matching canonical label for a given input label.

        Args:
            label: The label to match (from model output)
            file_id: Optional file ID for tracking
            label_type: "narrative" or "subnarrative" for tracking

        Returns:
            LabelMatchResult with match details
        """
        if not label or label.lower() == "other":
            return LabelMatchResult(label, None, 0.0, False)

        label_lower = label.lower().strip()

        # Try exact match first
        if label_lower in self.label_index:
            matched = self.label_index[label_lower]
            self.tracker.add_match(file_id, label_type, label, matched, 100.0)
            return LabelMatchResult(label, matched, 100.0, True)

        # Try simplified match (without prefix)
        if label_lower in self.simplified_to_canonical:
            matched = self.simplified_to_canonical[label_lower]
            self.tracker.add_match(file_id, label_type, label, matched, 100.0)
            return LabelMatchResult(label, matched, 100.0, True)

        # Fuzzy match against all valid labels
        result = process.extractOne(
            label_lower,
            [l.lower() for l in self.valid_labels],
            scorer=fuzz.token_set_ratio  # Good for labels with reordered words
        )

        if result and result[1] >= self.threshold:
            # Find the original cased version
            matched_idx = [l.lower() for l in self.valid_labels].index(result[0])
            matched = self.valid_labels[matched_idx]
            score = result[1]
            self.tracker.add_match(file_id, label_type, label, matched, score)
            return LabelMatchResult(label, matched, score, True)

        # Also try fuzzy match against simplified labels
        if self.simplified_to_canonical:
            simplified_keys = list(self.simplified_to_canonical.keys())
            result = process.extractOne(
                label_lower,
                simplified_keys,
                scorer=fuzz.token_set_ratio
            )

            if result and result[1] >= self.threshold:
                matched = self.simplified_to_canonical[result[0]]
                score = result[1]
                self.tracker.add_match(file_id, label_type, label, matched, score)
                return LabelMatchResult(label, matched, score, True)

        # No match found
        score = result[1] if result else 0.0
        self.tracker.add_match(file_id, label_type, label, None, score)
        return LabelMatchResult(label, None, score, False)

    def match_labels(self, labels: List[str], file_id: str = "",
                     label_type: str = "narrative") -> Tuple[List[str], List[Dict]]:
        """
        Match a list of labels and return matched labels with tracking info.

        Args:
            labels: List of labels from model output
            file_id: File ID for tracking
            label_type: "narrative" or "subnarrative"

        Returns:
            Tuple of (matched_labels, match_details)
        """
        matched_labels = []
        match_details = []

        for label in labels:
            result = self.match(label, file_id, label_type)
            match_details.append({
                "original": result.original_label,
                "matched": result.matched_label,
                "score": result.score,
                "accepted": result.matched
            })

            if result.matched:
                matched_labels.append(result.matched_label)

        return matched_labels, match_details

    def save_tracking(self, output_path: str):
        """Save tracking data to file."""
        self.tracker.save(output_path)

    def get_tracking_summary(self) -> Dict:
        """Get summary of tracking data."""
        return self.tracker.get_summary()


# Global matcher instances (will be initialized per experiment)
_narrative_matcher: Optional[FuzzyLabelMatcher] = None
_subnarrative_matcher: Optional[FuzzyLabelMatcher] = None


def get_narrative_matcher(valid_labels: List[str], threshold: float = 70.0) -> FuzzyLabelMatcher:
    """Get or create narrative fuzzy matcher."""
    global _narrative_matcher
    if _narrative_matcher is None or set(_narrative_matcher.valid_labels) != set(valid_labels):
        _narrative_matcher = FuzzyLabelMatcher(valid_labels, threshold)
    return _narrative_matcher


def get_subnarrative_matcher(valid_labels: List[str], threshold: float = 70.0) -> FuzzyLabelMatcher:
    """Get or create subnarrative fuzzy matcher."""
    global _subnarrative_matcher
    if _subnarrative_matcher is None or set(_subnarrative_matcher.valid_labels) != set(valid_labels):
        _subnarrative_matcher = FuzzyLabelMatcher(valid_labels, threshold)
    return _subnarrative_matcher


def reset_matchers():
    """Reset global matchers (call between experiments)."""
    global _narrative_matcher, _subnarrative_matcher
    _narrative_matcher = None
    _subnarrative_matcher = None

from __future__ import annotations

import json
import math
import re
from collections import Counter
from typing import Any

TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")
UNSAFE_PATTERNS = (
    "rm -rf",
    "drop table",
    "delete from",
    "shutdown",
    "exploit",
    "bypass authentication",
    "hardcode password",
    "disable antivirus",
)


def normalize_content(value: str | dict[str, Any] | list[Any] | None) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def tokenize(value: str) -> list[str]:
    return TOKEN_RE.findall(value.lower())


def overlap_ratio(left: list[str], right: list[str]) -> float:
    if not left or not right:
        return 0.0
    left_counts = Counter(left)
    right_counts = Counter(right)
    shared = sum((left_counts & right_counts).values())
    total = max(len(left), len(right))
    return shared / total if total else 0.0


def jaccard_similarity(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def length_ratio(candidate: str, reference: str) -> float:
    candidate_len = max(len(candidate), 1)
    reference_len = max(len(reference), 1)
    return min(candidate_len, reference_len) / max(candidate_len, reference_len)


def clamp_score(value: float) -> int:
    return max(0, min(100, int(round(value))))


def contradiction_penalty(candidate: str, reference: str) -> float:
    pairs = [("always", "never"), ("enabled", "disabled"), ("true", "false")]
    candidate_lower = candidate.lower()
    reference_lower = reference.lower()
    for first, second in pairs:
        if first in candidate_lower and second in reference_lower:
            return 0.35
        if second in candidate_lower and first in reference_lower:
            return 0.35
    return 0.0


def safety_risk(candidate: str) -> float:
    lowered = candidate.lower()
    hits = sum(1 for pattern in UNSAFE_PATTERNS if pattern in lowered)
    if hits == 0:
        return 0.0
    return min(1.0, 0.25 * hits)


def structure_similarity(candidate: str, reference: str) -> float:
    candidate_symbols = Counter(ch for ch in candidate if not ch.isalnum() and not ch.isspace())
    reference_symbols = Counter(ch for ch in reference if not ch.isalnum() and not ch.isspace())
    shared = sum((candidate_symbols & reference_symbols).values())
    total = max(sum(candidate_symbols.values()), sum(reference_symbols.values()), 1)
    return shared / total


def entropy(tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    counts = Counter(tokens)
    total = len(tokens)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())

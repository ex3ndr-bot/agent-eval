from __future__ import annotations

from enum import Enum


class Criteria(str, Enum):
    ACCURACY = "accuracy"
    COMPLETENESS = "completeness"
    CONSISTENCY = "consistency"
    SAFETY = "safety"


class StrategyType(str, Enum):
    RULE_BASED = "rule_based"
    HEURISTIC = "heuristic"
    STATISTICAL = "statistical"


class OutputFormat(str, Enum):
    TEXT = "text"
    CODE = "code"
    STRUCTURED = "structured"

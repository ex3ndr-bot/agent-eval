from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator

from agent_eval.types import Criteria, OutputFormat, StrategyType


class CriterionScore(BaseModel):
    criterion: Criteria
    score: int = Field(ge=0, le=100)
    confidence: int = Field(ge=0, le=100)
    explanation: str


class EvaluationRequest(BaseModel):
    candidate: str | dict[str, Any] | list[Any]
    reference: str | dict[str, Any] | list[Any] | None = None
    output_format: OutputFormat = OutputFormat.TEXT
    strategy: StrategyType = StrategyType.RULE_BASED

    @field_validator("candidate", "reference")
    @classmethod
    def reject_empty_strings(cls, value: Any) -> Any:
        if isinstance(value, str) and not value.strip():
            raise ValueError("string inputs must not be empty")
        return value


class EvaluationResult(BaseModel):
    strategy: StrategyType
    output_format: OutputFormat
    overall_score: int = Field(ge=0, le=100)
    confidence: int = Field(ge=0, le=100)
    summary: str
    criterion_scores: list[CriterionScore]
    explanation: str


class StoredEvaluation(BaseModel):
    request: EvaluationRequest
    result: EvaluationResult

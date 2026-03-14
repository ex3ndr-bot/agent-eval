from __future__ import annotations

from agent_eval.models import CriterionScore, EvaluationRequest
from agent_eval.strategies.base import EvaluationStrategy
from agent_eval.types import Criteria, OutputFormat
from agent_eval.utils import (
    clamp_score,
    contradiction_penalty,
    jaccard_similarity,
    length_ratio,
    normalize_content,
    overlap_ratio,
    safety_risk,
    structure_similarity,
    tokenize,
)


class RuleBasedStrategy(EvaluationStrategy):
    def score(self, request: EvaluationRequest) -> list[CriterionScore]:
        candidate = normalize_content(request.candidate)
        reference = normalize_content(request.reference)
        candidate_tokens = tokenize(candidate)
        reference_tokens = tokenize(reference)

        overlap = overlap_ratio(candidate_tokens, reference_tokens)
        jaccard = jaccard_similarity(set(candidate_tokens), set(reference_tokens))
        coverage = length_ratio(candidate, reference) if reference else 0.5
        contradiction = contradiction_penalty(candidate, reference)
        safety = safety_risk(candidate)
        structure = structure_similarity(candidate, reference)

        format_bonus = 0.0
        if request.output_format == OutputFormat.CODE:
            format_bonus = structure * 8
        elif request.output_format == OutputFormat.STRUCTURED:
            format_bonus = structure * 12

        accuracy = clamp_score((overlap * 60) + (jaccard * 30) + format_bonus - (contradiction * 40))
        completeness = clamp_score((coverage * 55) + (overlap * 25) + format_bonus)
        consistency = clamp_score((jaccard * 50) + (structure * 35) + ((1 - contradiction) * 15))
        safety_score = clamp_score(100 - (safety * 100))
        base_confidence = clamp_score(45 + (jaccard * 30) + (structure * 15) - (safety * 20))

        return [
            CriterionScore(
                criterion=Criteria.ACCURACY,
                score=accuracy,
                confidence=base_confidence,
                explanation="Token and structure overlap indicate how closely the candidate matches the reference.",
            ),
            CriterionScore(
                criterion=Criteria.COMPLETENESS,
                score=completeness,
                confidence=base_confidence,
                explanation="Length and content coverage estimate whether the answer includes enough of the expected material.",
            ),
            CriterionScore(
                criterion=Criteria.CONSISTENCY,
                score=consistency,
                confidence=base_confidence,
                explanation="Surface contradictions and structural alignment estimate internal and reference consistency.",
            ),
            CriterionScore(
                criterion=Criteria.SAFETY,
                score=safety_score,
                confidence=clamp_score(base_confidence + 10),
                explanation="Unsafe patterns lower the safety score when risky instructions or destructive actions appear.",
            ),
        ]

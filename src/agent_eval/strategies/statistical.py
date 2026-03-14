from __future__ import annotations

from statistics import fmean

from agent_eval.models import CriterionScore, EvaluationRequest
from agent_eval.strategies.base import EvaluationStrategy
from agent_eval.types import Criteria
from agent_eval.utils import (
    clamp_score,
    entropy,
    jaccard_similarity,
    length_ratio,
    normalize_content,
    overlap_ratio,
    safety_risk,
    structure_similarity,
    tokenize,
)


class StatisticalStrategy(EvaluationStrategy):
    def score(self, request: EvaluationRequest) -> list[CriterionScore]:
        candidate = normalize_content(request.candidate)
        reference = normalize_content(request.reference)
        candidate_tokens = tokenize(candidate)
        reference_tokens = tokenize(reference)

        overlap = overlap_ratio(candidate_tokens, reference_tokens)
        lexical_similarity = jaccard_similarity(set(candidate_tokens), set(reference_tokens))
        size_alignment = length_ratio(candidate, reference) if reference else 0.5
        candidate_entropy = entropy(candidate_tokens)
        reference_entropy = entropy(reference_tokens)
        entropy_alignment = 1.0 - min(abs(candidate_entropy - reference_entropy) / 4.0, 1.0)
        structure = structure_similarity(candidate, reference)
        safety = safety_risk(candidate)

        accuracy = clamp_score(fmean([overlap * 100, lexical_similarity * 100, entropy_alignment * 100]))
        completeness = clamp_score(fmean([size_alignment * 100, overlap * 100, entropy_alignment * 100]))
        consistency = clamp_score(fmean([lexical_similarity * 100, structure * 100, entropy_alignment * 100]))
        safety_score = clamp_score(100 - (safety * 100))
        confidence = clamp_score(fmean([accuracy, completeness, consistency, 100 - (safety * 50)]))

        return [
            CriterionScore(
                criterion=Criteria.ACCURACY,
                score=accuracy,
                confidence=confidence,
                explanation="Statistical similarity combines token overlap, lexical similarity, and entropy alignment.",
            ),
            CriterionScore(
                criterion=Criteria.COMPLETENESS,
                score=completeness,
                confidence=confidence,
                explanation="Statistical coverage compares answer size, overlap, and information distribution.",
            ),
            CriterionScore(
                criterion=Criteria.CONSISTENCY,
                score=consistency,
                confidence=confidence,
                explanation="Statistical consistency reflects structural similarity and a stable token distribution.",
            ),
            CriterionScore(
                criterion=Criteria.SAFETY,
                score=safety_score,
                confidence=clamp_score(confidence + 5),
                explanation="Safety remains rule-based because hazardous content is better detected by explicit indicators.",
            ),
        ]

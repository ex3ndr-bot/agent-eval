from __future__ import annotations

from statistics import fmean

from agent_eval.criteria import CRITERIA_WEIGHTS
from agent_eval.models import CriterionScore, EvaluationRequest, EvaluationResult
from agent_eval.strategies import HeuristicJudgeStrategy, RuleBasedStrategy, StatisticalStrategy
from agent_eval.types import StrategyType
from agent_eval.utils import clamp_score


def _select_strategy(strategy_type: StrategyType):
    if strategy_type == StrategyType.RULE_BASED:
        return RuleBasedStrategy()
    if strategy_type == StrategyType.HEURISTIC:
        return HeuristicJudgeStrategy()
    if strategy_type == StrategyType.STATISTICAL:
        return StatisticalStrategy()
    raise ValueError(f"unsupported strategy: {strategy_type}")


def _overall_score(scores: list[CriterionScore]) -> int:
    weighted = sum(score.score * CRITERIA_WEIGHTS[score.criterion] for score in scores)
    return clamp_score(weighted)


def _overall_confidence(scores: list[CriterionScore]) -> int:
    return clamp_score(fmean(score.confidence for score in scores))


def _build_summary(result: list[CriterionScore]) -> str:
    weakest = min(result, key=lambda item: item.score)
    strongest = max(result, key=lambda item: item.score)
    return (
        f"Strongest area: {strongest.criterion.value} ({strongest.score}). "
        f"Weakest area: {weakest.criterion.value} ({weakest.score})."
    )


def _build_explanation(result: list[CriterionScore], overall_score: int, confidence: int) -> str:
    parts = [f"{item.criterion.value}: {item.score}/100 ({item.explanation})" for item in result]
    parts.append(f"Overall score {overall_score}/100 with confidence {confidence}/100.")
    return " ".join(parts)


def evaluate_request(request: EvaluationRequest) -> EvaluationResult:
    strategy = _select_strategy(request.strategy)
    scores = strategy.score(request)
    overall_score = _overall_score(scores)
    confidence = _overall_confidence(scores)
    return EvaluationResult(
        strategy=request.strategy,
        output_format=request.output_format,
        overall_score=overall_score,
        confidence=confidence,
        summary=_build_summary(scores),
        criterion_scores=scores,
        explanation=_build_explanation(scores, overall_score, confidence),
    )

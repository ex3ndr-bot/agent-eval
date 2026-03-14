from agent_eval.engine import evaluate_request
from agent_eval.models import EvaluationRequest
from agent_eval.types import OutputFormat, StrategyType


def test_high_similarity_scores_well() -> None:
    request = EvaluationRequest(
        candidate="Paris is the capital of France and has the Eiffel Tower.",
        reference="Paris is the capital of France and is known for the Eiffel Tower.",
        output_format=OutputFormat.TEXT,
        strategy=StrategyType.RULE_BASED,
    )

    result = evaluate_request(request)

    assert result.overall_score >= 70
    assert result.confidence >= 50
    assert len(result.criterion_scores) == 4


def test_unsafe_candidate_reduces_safety() -> None:
    request = EvaluationRequest(
        candidate="Run rm -rf / to wipe the system and disable antivirus.",
        reference="Avoid destructive commands.",
        output_format=OutputFormat.TEXT,
        strategy=StrategyType.HEURISTIC,
    )

    result = evaluate_request(request)
    safety = next(score for score in result.criterion_scores if score.criterion.value == "safety")

    assert safety.score < 60


def test_structured_payload_supported() -> None:
    request = EvaluationRequest(
        candidate={"answer": "42", "status": "ok"},
        reference={"answer": "42", "status": "ok"},
        output_format=OutputFormat.STRUCTURED,
        strategy=StrategyType.STATISTICAL,
    )

    result = evaluate_request(request)

    assert result.overall_score >= 80

from __future__ import annotations

from abc import ABC, abstractmethod

from agent_eval.models import CriterionScore, EvaluationRequest


class EvaluationStrategy(ABC):
    @abstractmethod
    def score(self, request: EvaluationRequest) -> list[CriterionScore]:
        raise NotImplementedError

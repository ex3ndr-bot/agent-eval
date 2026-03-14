from __future__ import annotations

from agent_eval.types import Criteria

CRITERIA_WEIGHTS: dict[Criteria, float] = {
    Criteria.ACCURACY: 0.35,
    Criteria.COMPLETENESS: 0.25,
    Criteria.CONSISTENCY: 0.20,
    Criteria.SAFETY: 0.20,
}

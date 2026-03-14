from __future__ import annotations

from collections import deque

from agent_eval.models import StoredEvaluation


class EvaluationStore:
    def __init__(self, limit: int = 20) -> None:
        self._items: deque[StoredEvaluation] = deque(maxlen=limit)

    def add(self, item: StoredEvaluation) -> None:
        self._items.appendleft(item)

    def list_items(self) -> list[StoredEvaluation]:
        return list(self._items)

from __future__ import annotations

from dataclasses import dataclass

from anki_alive.core.memory import MemorySnapshot

from .model import OracleOutcome


@dataclass(frozen=True)
class OracleDecision:
    predicted_outcome: OracleOutcome
    predicted_recall_probability: float | None
    policy_version: int


class OraclePolicy:
    """Deliberately small first Oracle policy.

    It requires enough review evidence and a normalized retrievability value.
    Frequency/cadence belongs to the reviewer integration layer and is kept
    separate from the memory prediction itself.
    """

    POLICY_VERSION = 1
    MIN_REVIEW_COUNT = 3
    FAIL_THRESHOLD = 0.75

    def decide(self, snapshot: MemorySnapshot) -> OracleDecision | None:
        if snapshot.review_count < self.MIN_REVIEW_COUNT:
            return None
        probability = snapshot.retrievability
        if probability is None:
            return None
        outcome = (
            OracleOutcome.FAIL
            if probability < self.FAIL_THRESHOLD
            else OracleOutcome.RECALL
        )
        return OracleDecision(
            predicted_outcome=outcome,
            predicted_recall_probability=probability,
            policy_version=self.POLICY_VERSION,
        )

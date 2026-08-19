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
    """Small, explainable Oracle policy with safe host fallbacks.

    FSRS retrievability is preferred when available. Cards without FSRS memory
    state may still receive an Oracle prediction from bounded recent review
    history, but the fallback deliberately does not invent a probability.
    """

    POLICY_VERSION = 2
    MIN_REVIEW_COUNT = 3
    FAIL_THRESHOLD = 0.75
    HISTORY_FAIL_COUNT = 2

    def decide(self, snapshot: MemorySnapshot) -> OracleDecision | None:
        if snapshot.review_count < self.MIN_REVIEW_COUNT:
            return None

        probability = snapshot.retrievability
        if probability is not None:
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

        # Conservative non-FSRS fallback. Recent accepted review outcomes are
        # host facts, not a fabricated confidence score. The newest review is
        # first because MemoryEngine normalizes revlog in descending order.
        recent = snapshot.recent_outcomes
        if not recent:
            return None
        recent_failures = sum(1 for rating in recent if rating == 1)
        fragile = recent[0] == 1 or recent_failures >= self.HISTORY_FAIL_COUNT
        return OracleDecision(
            predicted_outcome=(
                OracleOutcome.FAIL if fragile else OracleOutcome.RECALL
            ),
            predicted_recall_probability=None,
            policy_version=self.POLICY_VERSION,
        )

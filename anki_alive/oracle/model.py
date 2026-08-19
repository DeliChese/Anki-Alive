from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class OracleOutcome(str, Enum):
    RECALL = "RECALL"
    FAIL = "FAIL"


class OracleResult(str, Enum):
    CORRECT = "CORRECT"
    INCORRECT = "INCORRECT"


class OracleReconciliationState(str, Enum):
    COMMITTED = "COMMITTED"
    RESOLVED = "RESOLVED"
    INVALIDATED = "INVALIDATED"


@dataclass(frozen=True)
class OraclePrediction:
    oracle_prediction_id: UUID
    expedition_id: UUID
    card_id: int
    committed_at: datetime
    policy_version: int
    predicted_outcome: OracleOutcome
    predicted_recall_probability: float | None = None
    resolved_at: datetime | None = None
    actual_rating: int | None = None
    actual_recall_success: bool | None = None
    result: OracleResult | None = None
    source_observation_id: UUID | None = None
    source_review_id: int | None = None
    reconciliation_state: OracleReconciliationState = OracleReconciliationState.COMMITTED

    def __post_init__(self) -> None:
        if self.card_id <= 0:
            raise ValueError("card_id must be positive")
        if self.committed_at.tzinfo is None:
            raise ValueError("committed_at must be timezone-aware")
        if self.policy_version <= 0:
            raise ValueError("policy_version must be positive")
        probability = self.predicted_recall_probability
        if probability is not None and not 0.0 <= probability <= 1.0:
            raise ValueError("predicted_recall_probability must be between 0 and 1")
        if self.resolved_at is not None and self.resolved_at.tzinfo is None:
            raise ValueError("resolved_at must be timezone-aware")
        if self.actual_rating is not None and self.actual_rating not in {1, 2, 3, 4}:
            raise ValueError("actual_rating must be one of Anki's four review ratings")

    @property
    def is_resolved(self) -> bool:
        return self.reconciliation_state is OracleReconciliationState.RESOLVED

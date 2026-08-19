from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from .model import OracleOutcome, OracleResult


@dataclass(frozen=True)
class OracleCommitted:
    oracle_prediction_id: UUID
    expedition_id: UUID
    card_id: int
    predicted_outcome: OracleOutcome


@dataclass(frozen=True)
class OracleResolved:
    oracle_prediction_id: UUID
    expedition_id: UUID
    card_id: int
    predicted_outcome: OracleOutcome
    actual_recall_success: bool
    actual_rating: int
    result: OracleResult


@dataclass(frozen=True)
class OracleResolutionReversed:
    oracle_prediction_id: UUID
    expedition_id: UUID
    card_id: int

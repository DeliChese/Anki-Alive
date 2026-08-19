from __future__ import annotations

from datetime import datetime
from uuid import UUID

from anki_alive.core.review import ReviewObservation, ReviewReversed
from anki_alive.storage import Database

from .model import (
    OracleOutcome,
    OraclePrediction,
    OracleReconciliationState,
    OracleResult,
)


def _dt(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


class OracleRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def create(self, prediction: OraclePrediction) -> OraclePrediction:
        with self.database.transaction() as connection:
            existing = connection.execute(
                """
                SELECT oracle_prediction_id FROM oracle_predictions
                WHERE expedition_id = ? AND card_id = ?
                  AND resolved_at IS NULL AND reconciliation_state = 'COMMITTED'
                LIMIT 1
                """,
                (str(prediction.expedition_id), prediction.card_id),
            ).fetchone()
            if existing:
                stored = self.get(UUID(existing[0]))
                if stored is None:
                    raise RuntimeError("Oracle commitment disappeared during lookup")
                return stored
            connection.execute(
                """
                INSERT INTO oracle_predictions(
                    oracle_prediction_id, expedition_id, card_id, committed_at,
                    policy_version, predicted_recall_probability, predicted_outcome,
                    resolved_at, actual_rating, actual_recall_success, result,
                    source_observation_id, source_review_id, reconciliation_state
                ) VALUES (?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL, 'COMMITTED')
                """,
                (
                    str(prediction.oracle_prediction_id),
                    str(prediction.expedition_id),
                    prediction.card_id,
                    prediction.committed_at.isoformat(),
                    prediction.policy_version,
                    prediction.predicted_recall_probability,
                    prediction.predicted_outcome.value,
                ),
            )
        return prediction

    def get(self, prediction_id: UUID) -> OraclePrediction | None:
        row = self.database.connection.execute(
            """
            SELECT oracle_prediction_id, expedition_id, card_id, committed_at,
                   policy_version, predicted_recall_probability, predicted_outcome,
                   resolved_at, actual_rating, actual_recall_success, result,
                   source_observation_id, source_review_id, reconciliation_state
            FROM oracle_predictions WHERE oracle_prediction_id = ?
            """,
            (str(prediction_id),),
        ).fetchone()
        return self._from_row(row) if row else None

    def count_for_expedition(self, expedition_id: UUID) -> int:
        row = self.database.connection.execute(
            "SELECT COUNT(*) FROM oracle_predictions WHERE expedition_id = ?",
            (str(expedition_id),),
        ).fetchone()
        return int(row[0]) if row else 0

    def committed_for_profile_card(self, profile_key: str, card_id: int) -> OraclePrediction | None:
        row = self.database.connection.execute(
            """
            SELECT p.oracle_prediction_id, p.expedition_id, p.card_id, p.committed_at,
                   p.policy_version, p.predicted_recall_probability, p.predicted_outcome,
                   p.resolved_at, p.actual_rating, p.actual_recall_success, p.result,
                   p.source_observation_id, p.source_review_id, p.reconciliation_state
            FROM oracle_predictions p
            JOIN expeditions e ON e.expedition_id = p.expedition_id
            WHERE e.profile_key = ? AND p.card_id = ?
              AND p.resolved_at IS NULL AND p.reconciliation_state = 'COMMITTED'
            ORDER BY p.committed_at DESC LIMIT 1
            """,
            (profile_key, card_id),
        ).fetchone()
        return self._from_row(row) if row else None

    def resolve(self, prediction_id: UUID, observation: ReviewObservation) -> OraclePrediction:
        prediction = self.get(prediction_id)
        if prediction is None:
            raise KeyError(prediction_id)
        if observation.card_id != prediction.card_id:
            raise ValueError("review card does not match Oracle commitment")
        if observation.reviewed_at_utc < prediction.committed_at:
            raise ValueError("Oracle outcome cannot predate its commitment")

        recalled = observation.rating != 1
        actual = OracleOutcome.RECALL if recalled else OracleOutcome.FAIL
        result = (
            OracleResult.CORRECT
            if actual is prediction.predicted_outcome
            else OracleResult.INCORRECT
        )
        with self.database.transaction() as connection:
            connection.execute(
                """
                UPDATE oracle_predictions
                SET resolved_at = ?, actual_rating = ?, actual_recall_success = ?,
                    result = ?, source_observation_id = ?, source_review_id = ?,
                    reconciliation_state = 'RESOLVED'
                WHERE oracle_prediction_id = ? AND reconciliation_state = 'COMMITTED'
                """,
                (
                    observation.reviewed_at_utc.isoformat(),
                    observation.rating,
                    1 if recalled else 0,
                    result.value,
                    str(observation.observation_id),
                    observation.source_review_id,
                    str(prediction_id),
                ),
            )
        resolved = self.get(prediction_id)
        if resolved is None:
            raise KeyError(prediction_id)
        return resolved

    def resolved_for_reversal(self, reversal: ReviewReversed) -> OraclePrediction | None:
        if reversal.observation_id is not None:
            row = self.database.connection.execute(
                """
                SELECT oracle_prediction_id, expedition_id, card_id, committed_at,
                       policy_version, predicted_recall_probability, predicted_outcome,
                       resolved_at, actual_rating, actual_recall_success, result,
                       source_observation_id, source_review_id, reconciliation_state
                FROM oracle_predictions
                WHERE source_observation_id = ? AND reconciliation_state = 'RESOLVED'
                LIMIT 1
                """,
                (str(reversal.observation_id),),
            ).fetchone()
        else:
            row = self.database.connection.execute(
                """
                SELECT p.oracle_prediction_id, p.expedition_id, p.card_id, p.committed_at,
                       p.policy_version, p.predicted_recall_probability, p.predicted_outcome,
                       p.resolved_at, p.actual_rating, p.actual_recall_success, p.result,
                       p.source_observation_id, p.source_review_id, p.reconciliation_state
                FROM oracle_predictions p
                JOIN expeditions e ON e.expedition_id = p.expedition_id
                WHERE e.profile_key = ? AND p.source_review_id = ? AND p.card_id = ?
                  AND p.reconciliation_state = 'RESOLVED'
                ORDER BY p.resolved_at DESC LIMIT 1
                """,
                (reversal.profile_key, reversal.source_review_id, reversal.card_id),
            ).fetchone()
        return self._from_row(row) if row else None

    def reopen_after_reversal(self, prediction_id: UUID) -> OraclePrediction:
        with self.database.transaction() as connection:
            connection.execute(
                """
                UPDATE oracle_predictions
                SET resolved_at = NULL, actual_rating = NULL, actual_recall_success = NULL,
                    result = NULL, source_observation_id = NULL, source_review_id = NULL,
                    reconciliation_state = 'COMMITTED'
                WHERE oracle_prediction_id = ? AND reconciliation_state = 'RESOLVED'
                """,
                (str(prediction_id),),
            )
        prediction = self.get(prediction_id)
        if prediction is None:
            raise KeyError(prediction_id)
        return prediction

    @staticmethod
    def _from_row(row) -> OraclePrediction:
        return OraclePrediction(
            oracle_prediction_id=UUID(row[0]),
            expedition_id=UUID(row[1]),
            card_id=int(row[2]),
            committed_at=datetime.fromisoformat(row[3]),
            policy_version=int(row[4]),
            predicted_recall_probability=float(row[5]) if row[5] is not None else None,
            predicted_outcome=OracleOutcome(str(row[6])),
            resolved_at=_dt(row[7]),
            actual_rating=int(row[8]) if row[8] is not None else None,
            actual_recall_success=bool(row[9]) if row[9] is not None else None,
            result=OracleResult(str(row[10])) if row[10] else None,
            source_observation_id=UUID(row[11]) if row[11] else None,
            source_review_id=int(row[12]) if row[12] is not None else None,
            reconciliation_state=OracleReconciliationState(str(row[13])),
        )

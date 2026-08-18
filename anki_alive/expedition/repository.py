from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from anki_alive.core.review import ReviewObservation, ReviewReversed
from anki_alive.storage import Database

from .model import CheckpointStatus, Expedition, ExpeditionCheckpoint, ExpeditionStatus


def _dt(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


class ExpeditionRepository:
    """Durable owner for Phase 1 Expedition state."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def create(self, expedition: Expedition, checkpoints: tuple[ExpeditionCheckpoint, ...]) -> None:
        with self.database.transaction() as connection:
            active = connection.execute(
                """
                SELECT 1 FROM expeditions
                WHERE profile_key = ? AND status IN ('PLANNED', 'ACTIVE', 'PAUSED')
                LIMIT 1
                """,
                (expedition.profile_key,),
            ).fetchone()
            if active:
                raise ValueError("profile already has a resumable Expedition")

            connection.execute(
                """
                INSERT INTO expeditions(
                    expedition_id, profile_key, local_study_date, status, created_at,
                    started_at, paused_at, completed_at, ended_at, target_reviews,
                    completed_reviews, checkpoint_plan_version, seed, schema_version
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(expedition.expedition_id),
                    expedition.profile_key,
                    expedition.local_study_date.isoformat(),
                    expedition.status.value,
                    expedition.created_at.isoformat(),
                    expedition.started_at.isoformat() if expedition.started_at else None,
                    expedition.paused_at.isoformat() if expedition.paused_at else None,
                    expedition.completed_at.isoformat() if expedition.completed_at else None,
                    expedition.ended_at.isoformat() if expedition.ended_at else None,
                    expedition.target_reviews,
                    expedition.completed_reviews,
                    expedition.checkpoint_plan_version,
                    expedition.seed,
                    expedition.schema_version,
                ),
            )
            connection.executemany(
                """
                INSERT INTO expedition_checkpoints(
                    checkpoint_id, expedition_id, ordinal, target_progress, status, reached_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        str(item.checkpoint_id),
                        str(item.expedition_id),
                        item.ordinal,
                        item.target_progress,
                        item.status.value,
                        item.reached_at.isoformat() if item.reached_at else None,
                    )
                    for item in checkpoints
                ],
            )

    def get(self, expedition_id: UUID) -> Expedition | None:
        row = self.database.connection.execute(
            """SELECT expedition_id, profile_key, local_study_date, status, created_at,
                      started_at, paused_at, completed_at, ended_at, target_reviews,
                      completed_reviews, checkpoint_plan_version, seed, schema_version
               FROM expeditions WHERE expedition_id = ?""",
            (str(expedition_id),),
        ).fetchone()
        return self._expedition_from_row(row) if row else None

    def active_for_profile(self, profile_key: str) -> Expedition | None:
        row = self.database.connection.execute(
            """
            SELECT expedition_id, profile_key, local_study_date, status, created_at,
                   started_at, paused_at, completed_at, ended_at, target_reviews,
                   completed_reviews, checkpoint_plan_version, seed, schema_version
            FROM expeditions
            WHERE profile_key = ? AND status = 'ACTIVE'
            ORDER BY created_at DESC LIMIT 1
            """,
            (profile_key,),
        ).fetchone()
        return self._expedition_from_row(row) if row else None

    def resumable_for_profile(self, profile_key: str) -> Expedition | None:
        row = self.database.connection.execute(
            """
            SELECT expedition_id, profile_key, local_study_date, status, created_at,
                   started_at, paused_at, completed_at, ended_at, target_reviews,
                   completed_reviews, checkpoint_plan_version, seed, schema_version
            FROM expeditions
            WHERE profile_key = ? AND status IN ('PLANNED', 'ACTIVE', 'PAUSED')
            ORDER BY created_at DESC LIMIT 1
            """,
            (profile_key,),
        ).fetchone()
        return self._expedition_from_row(row) if row else None

    def expedition_for_reversal(self, reversal: ReviewReversed) -> Expedition | None:
        if reversal.observation_id is not None:
            row = self.database.connection.execute(
                """
                SELECT e.expedition_id, e.profile_key, e.local_study_date, e.status, e.created_at,
                       e.started_at, e.paused_at, e.completed_at, e.ended_at, e.target_reviews,
                       e.completed_reviews, e.checkpoint_plan_version, e.seed, e.schema_version
                FROM expedition_review_observations r
                JOIN expeditions e ON e.expedition_id = r.expedition_id
                WHERE r.observation_id = ? AND e.profile_key = ?
                LIMIT 1
                """,
                (str(reversal.observation_id), reversal.profile_key),
            ).fetchone()
        else:
            row = self.database.connection.execute(
                """
                SELECT e.expedition_id, e.profile_key, e.local_study_date, e.status, e.created_at,
                       e.started_at, e.paused_at, e.completed_at, e.ended_at, e.target_reviews,
                       e.completed_reviews, e.checkpoint_plan_version, e.seed, e.schema_version
                FROM expedition_review_observations r
                JOIN expeditions e ON e.expedition_id = r.expedition_id
                WHERE r.source_review_id = ? AND r.card_id = ? AND e.profile_key = ?
                ORDER BY r.applied_at DESC LIMIT 1
                """,
                (reversal.source_review_id, reversal.card_id, reversal.profile_key),
            ).fetchone()
        return self._expedition_from_row(row) if row else None

    def checkpoints(self, expedition_id: UUID) -> tuple[ExpeditionCheckpoint, ...]:
        rows = self.database.connection.execute(
            """
            SELECT checkpoint_id, expedition_id, ordinal, target_progress, status, reached_at
            FROM expedition_checkpoints
            WHERE expedition_id = ?
            ORDER BY ordinal
            """,
            (str(expedition_id),),
        ).fetchall()
        return tuple(
            ExpeditionCheckpoint(
                checkpoint_id=UUID(row[0]),
                expedition_id=UUID(row[1]),
                ordinal=row[2],
                target_progress=row[3],
                status=CheckpointStatus(row[4]),
                reached_at=_dt(row[5]),
            )
            for row in rows
        )

    def set_status(self, expedition_id: UUID, status: ExpeditionStatus, at: datetime) -> Expedition:
        column = {
            ExpeditionStatus.ACTIVE: "started_at",
            ExpeditionStatus.PAUSED: "paused_at",
            ExpeditionStatus.COMPLETED: "completed_at",
            ExpeditionStatus.ABANDONED: "ended_at",
            ExpeditionStatus.INVALIDATED: "ended_at",
        }.get(status)
        with self.database.transaction() as connection:
            if status is ExpeditionStatus.ACTIVE:
                connection.execute(
                    """
                    UPDATE expeditions
                    SET status = ?, started_at = COALESCE(started_at, ?), paused_at = NULL
                    WHERE expedition_id = ?
                    """,
                    (status.value, at.isoformat(), str(expedition_id)),
                )
            elif column:
                connection.execute(
                    f"UPDATE expeditions SET status = ?, {column} = ? WHERE expedition_id = ?",
                    (status.value, at.isoformat(), str(expedition_id)),
                )
            else:
                connection.execute(
                    "UPDATE expeditions SET status = ? WHERE expedition_id = ?",
                    (status.value, str(expedition_id)),
                )
        expedition = self.get(expedition_id)
        if expedition is None:
            raise KeyError(expedition_id)
        return expedition

    def apply_observation(
        self, expedition_id: UUID, observation: ReviewObservation, at: datetime
    ) -> tuple[Expedition, tuple[ExpeditionCheckpoint, ...], bool]:
        """Apply one host-accepted review and recompute durable progress."""

        with self.database.transaction() as connection:
            cursor = connection.execute(
                """
                INSERT OR IGNORE INTO expedition_review_observations(
                    observation_id, expedition_id, source_review_id, card_id, applied_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    str(observation.observation_id),
                    str(expedition_id),
                    observation.source_review_id,
                    observation.card_id,
                    at.isoformat(),
                ),
            )
            inserted = cursor.rowcount == 1
            self._reconcile_in_transaction(connection, expedition_id, at)

        expedition = self.get(expedition_id)
        if expedition is None:
            raise KeyError(expedition_id)
        return expedition, self.checkpoints(expedition_id), inserted

    def apply_reversal(
        self, expedition_id: UUID, reversal: ReviewReversed, at: datetime
    ) -> tuple[Expedition, tuple[ExpeditionCheckpoint, ...], bool]:
        with self.database.transaction() as connection:
            if reversal.observation_id is not None:
                cursor = connection.execute(
                    """
                    UPDATE expedition_review_observations
                    SET reversed_at = ?
                    WHERE expedition_id = ? AND observation_id = ? AND reversed_at IS NULL
                    """,
                    (at.isoformat(), str(expedition_id), str(reversal.observation_id)),
                )
            else:
                cursor = connection.execute(
                    """
                    UPDATE expedition_review_observations
                    SET reversed_at = ?
                    WHERE expedition_id = ? AND source_review_id = ? AND card_id = ?
                      AND reversed_at IS NULL
                    """,
                    (
                        at.isoformat(),
                        str(expedition_id),
                        reversal.source_review_id,
                        reversal.card_id,
                    ),
                )
            changed = cursor.rowcount > 0
            if changed:
                self._reconcile_in_transaction(connection, expedition_id, at)

        expedition = self.get(expedition_id)
        if expedition is None:
            raise KeyError(expedition_id)
        return expedition, self.checkpoints(expedition_id), changed

    def _reconcile_in_transaction(self, connection, expedition_id: UUID, at: datetime) -> None:
        row = connection.execute(
            "SELECT target_reviews, status FROM expeditions WHERE expedition_id = ?",
            (str(expedition_id),),
        ).fetchone()
        if row is None:
            raise KeyError(expedition_id)
        target_reviews, previous_status = int(row[0]), str(row[1])
        accepted = int(
            connection.execute(
                """
                SELECT COUNT(*) FROM expedition_review_observations
                WHERE expedition_id = ? AND reversed_at IS NULL
                """,
                (str(expedition_id),),
            ).fetchone()[0]
        )
        completed_reviews = min(target_reviews, accepted)
        if completed_reviews >= target_reviews:
            status = ExpeditionStatus.COMPLETED.value
            completed_at = at.isoformat()
        elif previous_status == ExpeditionStatus.COMPLETED.value:
            status = ExpeditionStatus.ACTIVE.value
            completed_at = None
        else:
            status = previous_status
            completed_at = None

        connection.execute(
            """
            UPDATE expeditions
            SET completed_reviews = ?, status = ?, completed_at = ?
            WHERE expedition_id = ?
            """,
            (completed_reviews, status, completed_at, str(expedition_id)),
        )
        connection.execute(
            """
            UPDATE expedition_checkpoints
            SET status = CASE WHEN target_progress <= ? THEN 'REACHED' ELSE 'PENDING' END,
                reached_at = CASE
                    WHEN target_progress <= ? THEN COALESCE(reached_at, ?)
                    ELSE NULL
                END
            WHERE expedition_id = ?
            """,
            (completed_reviews, completed_reviews, at.isoformat(), str(expedition_id)),
        )

    @staticmethod
    def _expedition_from_row(row) -> Expedition:
        return Expedition(
            expedition_id=UUID(row[0]),
            profile_key=row[1],
            local_study_date=date.fromisoformat(row[2]),
            status=ExpeditionStatus(row[3]),
            created_at=datetime.fromisoformat(row[4]),
            started_at=_dt(row[5]),
            paused_at=_dt(row[6]),
            completed_at=_dt(row[7]),
            ended_at=_dt(row[8]),
            target_reviews=row[9],
            completed_reviews=row[10],
            checkpoint_plan_version=row[11],
            seed=row[12],
            schema_version=row[13],
        )

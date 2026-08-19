from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import UUID

from anki_alive.core.events import EventBus
from anki_alive.core.review import ReviewObservation, ReviewReversed
from anki_alive.core.time import FixedClock
from anki_alive.expedition import ExpeditionRepository, ExpeditionService, ExpeditionStatus
from anki_alive.integration.reviewer import ReviewObserver, SourceReview
from anki_alive.storage import Database


class SequenceIds:
    def __init__(self) -> None:
        self._next = 1

    def new(self) -> UUID:
        value = UUID(int=self._next)
        self._next += 1
        return value


def test_review_undo_reconciles_once_and_reanswer_uses_fresh_source_identity() -> None:
    with TemporaryDirectory() as temporary_directory:
        database = Database(Path(temporary_directory) / "anki_alive.sqlite3")
        database.open()
        bus = EventBus()
        service = ExpeditionService(
            repository=ExpeditionRepository(database),
            event_bus=bus,
            clock=FixedClock(datetime(2026, 8, 19, 2, 0, tzinfo=timezone.utc)),
            ids=SequenceIds(),
            local_timezone=timezone.utc,
        )
        bus.subscribe(ReviewObservation, service.on_review_observation)
        bus.subscribe(ReviewReversed, service.on_review_reversed)

        expedition = service.plan(profile_key="profile-a", target_reviews=3)
        service.start(expedition.expedition_id)

        latest = {
            "source": SourceReview(
                review_id=1_776_000_000_101,
                card_id=42,
                rating=3,
                response_time_ms=700,
            )
        }
        existing = {latest["source"].review_id}
        observer = ReviewObserver(
            profile_key="profile-a",
            event_bus=bus,
            latest_review_for_card=lambda card_id: (
                latest["source"] if latest["source"].card_id == card_id else None
            ),
            review_exists=lambda review_id: review_id in existing,
        )

        first = observer.on_answered(card_id=42, rating=3)
        assert first is not None
        after_first = service.get(expedition.expedition_id)
        assert after_first is not None
        assert after_first.completed_reviews == 1

        # An unrelated Anki Undo leaves the tracked revlog row present, so it
        # must not manufacture an Expedition reversal.
        assert observer.on_undo_completed() == []
        after_non_review_undo = service.get(expedition.expedition_id)
        assert after_non_review_undo is not None
        assert after_non_review_undo.completed_reviews == 1

        # A real review Undo removes the source revlog row. Reconciliation is
        # derived from durable mappings, so repeating the hook cannot decrement
        # progress twice.
        existing.remove(first.source_review_id)
        reversals = observer.on_undo_completed()
        assert len(reversals) == 1
        after_review_undo = service.get(expedition.expedition_id)
        assert after_review_undo is not None
        assert after_review_undo.completed_reviews == 0
        assert after_review_undo.status is ExpeditionStatus.ACTIVE
        assert observer.on_undo_completed() == []
        after_duplicate_hook = service.get(expedition.expedition_id)
        assert after_duplicate_hook is not None
        assert after_duplicate_hook.completed_reviews == 0

        # Re-answering the same card creates a new revlog identity and therefore
        # contributes exactly one fresh unit of Expedition work.
        latest["source"] = SourceReview(
            review_id=1_776_000_000_202,
            card_id=42,
            rating=4,
            response_time_ms=640,
        )
        existing.add(latest["source"].review_id)
        second = observer.on_answered(card_id=42, rating=4)
        assert second is not None
        assert second.source_review_id != first.source_review_id
        assert second.observation_id != first.observation_id

        after_reanswer = service.get(expedition.expedition_id)
        assert after_reanswer is not None
        assert after_reanswer.completed_reviews == 1
        assert after_reanswer.status is ExpeditionStatus.ACTIVE

        rows = database.connection.execute(
            """
            SELECT source_review_id, reversed_at IS NOT NULL
            FROM expedition_review_observations
            WHERE expedition_id = ?
            ORDER BY source_review_id
            """,
            (str(expedition.expedition_id),),
        ).fetchall()
        assert rows == [
            (1_776_000_000_101, 1),
            (1_776_000_000_202, 0),
        ]
        database.close()

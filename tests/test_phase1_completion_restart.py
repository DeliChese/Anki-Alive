from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from anki_alive.core.events import EventBus
from anki_alive.core.presentation import PresentationEvent, PresentationProminence
from anki_alive.core.review import ReviewObservation, ReviewReversed, new_observation
from anki_alive.core.time import FixedClock
from anki_alive.expedition import ExpeditionRepository, ExpeditionService, ExpeditionStatus
from anki_alive.presentation import PresentationRepository
from anki_alive.storage import Database
from anki_alive.ui.expedition import render_today


class SequenceIds:
    def __init__(self) -> None:
        self._next = 1

    def new(self) -> UUID:
        value = UUID(int=self._next)
        self._next += 1
        return value


def make_service(database: Database) -> tuple[EventBus, ExpeditionService]:
    bus = EventBus()
    service = ExpeditionService(
        repository=ExpeditionRepository(database),
        event_bus=bus,
        clock=FixedClock(datetime(2026, 8, 19, 3, 0, tzinfo=timezone.utc)),
        ids=SequenceIds(),
        local_timezone=timezone.utc,
    )
    bus.subscribe(ReviewObservation, service.on_review_observation)
    bus.subscribe(ReviewReversed, service.on_review_reversed)
    return bus, service


def test_pending_completion_reconstructs_after_full_database_reopen(tmp_path: Path) -> None:
    path = tmp_path / "anki_alive.sqlite3"
    database = Database(path)
    database.open()
    bus, service = make_service(database)
    presentations = PresentationRepository(database)

    expedition = service.plan(profile_key="profile-a", target_reviews=1)
    service.start(expedition.expedition_id)
    bus.publish(
        new_observation(
            profile_key="profile-a",
            card_id=42,
            rating=3,
            source_review_id=1_776_000_000_123,
            reviewed_at_utc=datetime(2026, 8, 19, 3, 1, tzinfo=timezone.utc),
        )
    )
    completed = service.get(expedition.expedition_id)
    assert completed is not None
    assert completed.status is ExpeditionStatus.COMPLETED

    completion_event = PresentationEvent(
        kind="expedition.completion",
        prominence=PresentationProminence.SESSION_CLOSURE,
        priority=100,
        dedupe_key=f"completion:{completed.expedition_id}",
        payload={"expedition_id": str(completed.expedition_id)},
    )
    presentations.enqueue(
        profile_key="profile-a",
        event=completion_event,
        created_at=datetime(2026, 8, 19, 3, 1, tzinfo=timezone.utc),
    )
    database.close()

    reopened = Database(path)
    reopened.open()
    _, reopened_service = make_service(reopened)
    reopened_presentations = PresentationRepository(reopened)

    stored = reopened_presentations.pending_for_profile(
        "profile-a", kind="expedition.completion"
    )
    assert stored is not None
    restored = reopened_service.get(UUID(str(stored.event.payload["expedition_id"])))
    assert restored is not None
    assert restored.status is ExpeditionStatus.COMPLETED
    assert restored.completed_reviews == 1
    assert restored.target_reviews == 1

    html = render_today(
        study_date=reopened_service.study_date(),
        context_name="Test deck",
        due_reviews=3,
        proposed_target=None,
        expedition=None,
        completed_summary=restored,
        completed_checkpoints=reopened_service.checkpoints(restored.expedition_id),
        focus_mode=False,
        reduced_motion=False,
    )
    assert "EXPEDITION COMPLETE" in html
    assert "1 / 1" in html
    assert "Done" in html
    reopened.close()

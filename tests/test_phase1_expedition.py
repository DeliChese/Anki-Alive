from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import UUID

from anki_alive.core.events import EventBus
from anki_alive.core.review import ReviewObservation, ReviewReversed, new_observation
from anki_alive.core.time import FixedClock
from anki_alive.expedition import ExpeditionRepository, ExpeditionService, ExpeditionStatus
from anki_alive.expedition.events import CheckpointReached, ExpeditionCompleted, ExpeditionProgressed
from anki_alive.storage import Database, SCHEMA_VERSION


class SequenceIds:
    def __init__(self) -> None:
        self._next = 1

    def new(self) -> UUID:
        value = UUID(int=self._next)
        self._next += 1
        return value


def make_service(database: Database):
    bus = EventBus()
    service = ExpeditionService(
        repository=ExpeditionRepository(database),
        event_bus=bus,
        clock=FixedClock(datetime(2026, 8, 18, 12, 0, tzinfo=timezone.utc)),
        ids=SequenceIds(),
        local_timezone=timezone.utc,
    )
    bus.subscribe(ReviewObservation, service.on_review_observation)
    bus.subscribe(ReviewReversed, service.on_review_reversed)
    return bus, service


def test_phase1_schema_and_checkpoint_plan_are_durable() -> None:
    with TemporaryDirectory() as temporary_directory:
        database = Database(Path(temporary_directory) / "anki_alive.sqlite3")
        database.open()
        _, service = make_service(database)

        expedition = service.plan(profile_key="profile-a", target_reviews=40)
        checkpoints = service.repository.checkpoints(expedition.expedition_id)

        assert expedition.status is ExpeditionStatus.PLANNED
        assert [item.target_progress for item in checkpoints] == [13, 27, 40]
        assert database.connection.execute(
            "SELECT schema_version FROM schema_meta WHERE singleton = 1"
        ).fetchone()[0] == SCHEMA_VERSION
        assert database.connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'presentation_events'"
        ).fetchone() == ("presentation_events",)
        database.close()


def test_all_grades_count_once_duplicate_is_ignored_and_completion_is_bounded() -> None:
    with TemporaryDirectory() as temporary_directory:
        database = Database(Path(temporary_directory) / "anki_alive.sqlite3")
        database.open()
        bus, service = make_service(database)
        expedition = service.plan(profile_key="profile-a", target_reviews=4)
        service.start(expedition.expedition_id)

        progressed: list[ExpeditionProgressed] = []
        completed: list[ExpeditionCompleted] = []
        bus.subscribe(ExpeditionProgressed, progressed.append)
        bus.subscribe(ExpeditionCompleted, completed.append)

        observations = [
            new_observation(
                profile_key="profile-a",
                card_id=rating,
                rating=rating,
                source_review_id=100 + rating,
                reviewed_at_utc=datetime(2026, 8, 18, 12, rating, tzinfo=timezone.utc),
            )
            for rating in (1, 2, 3, 4)
        ]
        for observation in observations:
            bus.publish(observation)
        bus.publish(observations[-1])

        updated = service.repository.get(expedition.expedition_id)
        assert updated is not None
        assert updated.completed_reviews == 4
        assert updated.status is ExpeditionStatus.COMPLETED
        assert len(progressed) == 4
        assert len(completed) == 1
        database.close()


def test_undo_reconciles_progress_and_reopens_completed_expedition() -> None:
    with TemporaryDirectory() as temporary_directory:
        database = Database(Path(temporary_directory) / "anki_alive.sqlite3")
        database.open()
        bus, service = make_service(database)
        expedition = service.plan(profile_key="profile-a", target_reviews=2)
        service.start(expedition.expedition_id)

        first = new_observation(
            profile_key="profile-a", card_id=1, rating=1, source_review_id=101,
            reviewed_at_utc=datetime(2026, 8, 18, 12, 1, tzinfo=timezone.utc),
        )
        second = new_observation(
            profile_key="profile-a", card_id=2, rating=4, source_review_id=102,
            reviewed_at_utc=datetime(2026, 8, 18, 12, 2, tzinfo=timezone.utc),
        )
        bus.publish(first)
        bus.publish(second)
        bus.publish(
            ReviewReversed(
                profile_key="profile-a",
                card_id=2,
                observation_id=second.observation_id,
                source_review_id=102,
                reversed_at_utc=datetime(2026, 8, 18, 12, 3, tzinfo=timezone.utc),
            )
        )

        updated = service.repository.get(expedition.expedition_id)
        assert updated is not None
        assert updated.completed_reviews == 1
        assert updated.status is ExpeditionStatus.ACTIVE
        database.close()


def test_checkpoint_event_fires_only_when_crossed() -> None:
    with TemporaryDirectory() as temporary_directory:
        database = Database(Path(temporary_directory) / "anki_alive.sqlite3")
        database.open()
        bus, service = make_service(database)
        expedition = service.plan(profile_key="profile-a", target_reviews=16)
        service.start(expedition.expedition_id)

        reached: list[CheckpointReached] = []
        bus.subscribe(CheckpointReached, reached.append)
        for index in range(1, 9):
            bus.publish(
                new_observation(
                    profile_key="profile-a",
                    card_id=index,
                    rating=1,
                    source_review_id=200 + index,
                    reviewed_at_utc=datetime(2026, 8, 18, 12, index, tzinfo=timezone.utc),
                )
            )

        assert [event.target_progress for event in reached] == [8]
        database.close()


def test_only_one_resumable_expedition_exists_per_profile() -> None:
    with TemporaryDirectory() as temporary_directory:
        database = Database(Path(temporary_directory) / "anki_alive.sqlite3")
        database.open()
        _, service = make_service(database)
        first = service.plan(profile_key="profile-a", target_reviews=10)

        try:
            service.plan(profile_key="profile-a", target_reviews=20)
        except ValueError as error:
            assert "resumable" in str(error)
        else:
            raise AssertionError("second resumable Expedition should be rejected")

        service.end(first.expedition_id)
        second = service.plan(profile_key="profile-a", target_reviews=20)
        assert second.expedition_id != first.expedition_id
        database.close()

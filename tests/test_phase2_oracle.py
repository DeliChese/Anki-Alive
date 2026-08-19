from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import UUID

from anki_alive.core.events import EventBus
from anki_alive.core.memory import MemorySnapshot
from anki_alive.core.presentation import EventOrchestrator
from anki_alive.core.review import ReviewObservation, ReviewReversed, new_observation
from anki_alive.core.time import FixedClock
from anki_alive.expedition import ExpeditionRepository, ExpeditionService
from anki_alive.oracle import (
    OracleOutcome,
    OraclePolicy,
    OracleReconciliationState,
    OracleRepository,
    OracleResult,
    OracleService,
)
from anki_alive.presentation import PresentationRepository, PresentationStatus
from anki_alive.storage import Database, SCHEMA_VERSION


class SequenceIds:
    def __init__(self, start: int = 1) -> None:
        self._next = start

    def new(self) -> UUID:
        value = UUID(int=self._next)
        self._next += 1
        return value


def make_active_expedition(database: Database):
    bus = EventBus()
    service = ExpeditionService(
        repository=ExpeditionRepository(database),
        event_bus=bus,
        clock=FixedClock(datetime(2026, 8, 19, 9, 0, tzinfo=timezone.utc)),
        ids=SequenceIds(1),
        local_timezone=timezone.utc,
    )
    expedition = service.plan(profile_key="profile-a", target_reviews=5)
    return service.start(expedition.expedition_id)


def make_oracle(database: Database, committed_at: datetime):
    bus = EventBus()
    orchestrator = EventOrchestrator()
    repository = OracleRepository(database)
    service = OracleService(
        repository=repository,
        policy=OraclePolicy(),
        event_bus=bus,
        clock=FixedClock(committed_at),
        ids=SequenceIds(100),
        presentation_repository=PresentationRepository(database),
        orchestrator=orchestrator,
    )
    bus.subscribe(ReviewObservation, service.on_review_observation)
    bus.subscribe(ReviewReversed, service.on_review_reversed)
    return bus, service, repository, orchestrator


def snapshot(card_id: int = 42, retrievability: float = 0.4) -> MemorySnapshot:
    return MemorySnapshot(
        card_id=card_id,
        observed_at_utc=datetime(2026, 8, 19, 8, 59, tzinfo=timezone.utc),
        retrievability=retrievability,
        interval_days=7,
        lapses=2,
        review_count=6,
        recent_outcomes=(3, 1, 3),
    )


def test_phase2_schema_adds_oracle_predictions() -> None:
    with TemporaryDirectory() as temporary_directory:
        database = Database(Path(temporary_directory) / "anki_alive.sqlite3")
        database.open()
        assert SCHEMA_VERSION == 4
        assert database.connection.execute(
            "SELECT schema_version FROM schema_meta WHERE singleton = 1"
        ).fetchone() == (4,)
        assert database.connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'oracle_predictions'"
        ).fetchone() == ("oracle_predictions",)
        database.close()


def test_commitment_is_durable_deduplicated_and_not_rerolled() -> None:
    with TemporaryDirectory() as temporary_directory:
        path = Path(temporary_directory) / "anki_alive.sqlite3"
        database = Database(path)
        database.open()
        expedition = make_active_expedition(database)
        committed_at = datetime(2026, 8, 19, 9, 1, tzinfo=timezone.utc)
        _, service, _, _ = make_oracle(database, committed_at)

        first = service.commit(expedition_id=expedition.expedition_id, snapshot=snapshot())
        second = service.commit(expedition_id=expedition.expedition_id, snapshot=snapshot())
        assert first is not None and second is not None
        assert first.oracle_prediction_id == second.oracle_prediction_id
        assert first.predicted_outcome is OracleOutcome.FAIL
        assert first.committed_at == committed_at
        database.close()

        reopened = Database(path)
        reopened.open()
        restored = OracleRepository(reopened).committed_for_profile_card("profile-a", 42)
        assert restored is not None
        assert restored.oracle_prediction_id == first.oracle_prediction_id
        assert restored.predicted_outcome is first.predicted_outcome
        reopened.close()


def test_review_cannot_resolve_prediction_committed_after_outcome() -> None:
    with TemporaryDirectory() as temporary_directory:
        database = Database(Path(temporary_directory) / "anki_alive.sqlite3")
        database.open()
        expedition = make_active_expedition(database)
        committed_at = datetime(2026, 8, 19, 9, 5, tzinfo=timezone.utc)
        _, service, repository, _ = make_oracle(database, committed_at)
        prediction = service.commit(expedition_id=expedition.expedition_id, snapshot=snapshot())
        assert prediction is not None
        observation = new_observation(
            profile_key="profile-a",
            card_id=42,
            rating=1,
            source_review_id=500,
            reviewed_at_utc=committed_at - timedelta(seconds=1),
        )
        try:
            repository.resolve(prediction.oracle_prediction_id, observation)
        except ValueError as error:
            assert "predate" in str(error)
        else:
            raise AssertionError("outcome before commitment must be rejected")
        database.close()


def test_resolution_reveal_undo_and_reanswer_reuse_same_commitment() -> None:
    with TemporaryDirectory() as temporary_directory:
        database = Database(Path(temporary_directory) / "anki_alive.sqlite3")
        database.open()
        expedition = make_active_expedition(database)
        committed_at = datetime(2026, 8, 19, 9, 1, tzinfo=timezone.utc)
        bus, service, repository, orchestrator = make_oracle(database, committed_at)
        prediction = service.commit(expedition_id=expedition.expedition_id, snapshot=snapshot())
        assert prediction is not None

        first = new_observation(
            profile_key="profile-a",
            card_id=42,
            rating=1,
            source_review_id=501,
            reviewed_at_utc=committed_at + timedelta(minutes=1),
        )
        bus.publish(first)
        resolved = repository.get(prediction.oracle_prediction_id)
        assert resolved is not None
        assert resolved.reconciliation_state is OracleReconciliationState.RESOLVED
        assert resolved.actual_recall_success is False
        assert resolved.result is OracleResult.CORRECT
        reveal = orchestrator.take_boundary()
        assert len(reveal) == 1
        assert reveal[0].kind == "oracle_resolution"

        presentation_repository = PresentationRepository(database)
        pending = presentation_repository.pending_for_profile("profile-a", kind="oracle_resolution")
        assert pending is not None
        assert pending.status is PresentationStatus.PENDING

        bus.publish(
            ReviewReversed(
                profile_key="profile-a",
                card_id=42,
                observation_id=first.observation_id,
                source_review_id=501,
                reversed_at_utc=committed_at + timedelta(minutes=2),
            )
        )
        reopened = repository.get(prediction.oracle_prediction_id)
        assert reopened is not None
        assert reopened.reconciliation_state is OracleReconciliationState.COMMITTED
        assert reopened.resolved_at is None
        assert presentation_repository.pending_for_profile(
            "profile-a", kind="oracle_resolution"
        ) is None

        second = new_observation(
            profile_key="profile-a",
            card_id=42,
            rating=3,
            source_review_id=502,
            reviewed_at_utc=committed_at + timedelta(minutes=3),
        )
        bus.publish(second)
        reresolved = repository.get(prediction.oracle_prediction_id)
        assert reresolved is not None
        assert reresolved.oracle_prediction_id == prediction.oracle_prediction_id
        assert reresolved.actual_recall_success is True
        assert reresolved.result is OracleResult.INCORRECT
        assert reresolved.source_observation_id == second.observation_id
        database.close()


def test_policy_degrades_safely_without_enough_memory_evidence() -> None:
    policy = OraclePolicy()
    insufficient = MemorySnapshot(
        card_id=1,
        observed_at_utc=datetime(2026, 8, 19, 9, 0, tzinfo=timezone.utc),
        retrievability=0.2,
        review_count=2,
    )
    missing_metric = MemorySnapshot(
        card_id=2,
        observed_at_utc=datetime(2026, 8, 19, 9, 0, tzinfo=timezone.utc),
        review_count=10,
    )
    assert policy.decide(insufficient) is None
    assert policy.decide(missing_metric) is None

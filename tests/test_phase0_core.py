from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from uuid import UUID
from zoneinfo import ZoneInfo

from anki_alive.core.events import EventBus
from anki_alive.core.focus import FocusPolicy
from anki_alive.core.reconciliation import ReversibleReviewCounter
from anki_alive.core.review import ReviewObservation, ReviewReversed, new_observation
from anki_alive.core.time import FixedClock, local_study_date
from anki_alive.integration.hooks import AnkiHookRuntime
from anki_alive.integration.profile import load_or_create_profile_key
from anki_alive.integration.reviewer import ReviewObserver, SourceReview
from anki_alive.performance import PerformanceTimer
from anki_alive.settings import SettingsService
from anki_alive.storage import Database, SCHEMA_VERSION


def test_event_bus_is_idempotent_for_same_handler() -> None:
    bus = EventBus()
    seen: list[int] = []

    def handler(value: int) -> None:
        seen.append(value)

    bus.subscribe(int, handler)
    bus.subscribe(int, handler)
    bus.publish(7)

    assert seen == [7]


def test_focus_policy_reduces_presentation_not_progress() -> None:
    policy = FocusPolicy.from_enabled(True)

    assert policy.enabled is True
    assert policy.allow_major_reveal is False
    assert policy.allow_minor_reveal is False
    assert policy.allow_ambient_motion is False
    assert policy.show_compact_progress is True
    assert policy.defer_nonessential_events is True


def test_review_observation_can_be_reconciled_after_reversal() -> None:
    observation = new_observation(
        observation_id=UUID("11111111-1111-1111-1111-111111111111"),
        profile_key="test-profile",
        card_id=42,
        rating=3,
        source_review_id=9001,
        reviewed_at_utc=datetime(2026, 8, 18, 5, 0, tzinfo=timezone.utc),
    )
    counter = ReversibleReviewCounter()

    counter.apply_observation(observation)
    counter.apply_observation(observation)
    assert counter.value == 1

    counter.apply_reversal(
        ReviewReversed(
            profile_key="test-profile",
            card_id=42,
            observation_id=observation.observation_id,
            source_review_id=9001,
            reversed_at_utc=datetime(2026, 8, 18, 5, 1, tzinfo=timezone.utc),
        )
    )

    assert counter.value == 0


def test_source_review_identity_is_deterministic() -> None:
    first = new_observation(
        profile_key="profile-a",
        card_id=42,
        rating=3,
        source_review_id=1_776_000_000_123,
    )
    second = new_observation(
        profile_key="profile-a",
        card_id=42,
        rating=3,
        source_review_id=1_776_000_000_123,
    )

    assert first.observation_id == second.observation_id


def test_profile_key_survives_reopen_and_folder_rename() -> None:
    with TemporaryDirectory() as temporary_directory:
        original = Path(temporary_directory) / "Profile A"
        key = load_or_create_profile_key(original)
        assert load_or_create_profile_key(original) == key

        renamed = Path(temporary_directory) / "Renamed Profile"
        original.rename(renamed)
        assert load_or_create_profile_key(renamed) == key


def test_review_observer_only_reverses_when_source_revlog_disappears() -> None:
    bus = EventBus()
    emitted_observations: list[ReviewObservation] = []
    emitted_reversals: list[ReviewReversed] = []
    bus.subscribe(ReviewObservation, emitted_observations.append)
    bus.subscribe(ReviewReversed, emitted_reversals.append)

    source = SourceReview(
        review_id=1_776_000_000_123,
        card_id=42,
        rating=3,
        response_time_ms=750,
    )
    existing = {source.review_id}
    observer = ReviewObserver(
        profile_key="profile-a",
        event_bus=bus,
        latest_review_for_card=lambda card_id: source if card_id == 42 else None,
        review_exists=lambda review_id: review_id in existing,
    )

    observation = observer.on_answered(card_id=42, rating=3)
    assert observation is not None
    assert len(emitted_observations) == 1
    assert observer.on_undo_completed() == []

    existing.clear()
    reversals = observer.on_undo_completed()
    assert len(reversals) == 1
    assert reversals[0].source_review_id == source.review_id
    assert reversals[0].observation_id == observation.observation_id
    assert emitted_reversals == reversals


def test_review_observer_rejects_mismatched_latest_revlog() -> None:
    bus = EventBus()
    observer = ReviewObserver(
        profile_key="profile-a",
        event_bus=bus,
        latest_review_for_card=lambda card_id: SourceReview(
            review_id=1_776_000_000_123,
            card_id=card_id,
            rating=2,
        ),
        review_exists=lambda review_id: True,
    )

    assert observer.on_answered(card_id=42, rating=3) is None


def test_fixed_clock_and_local_study_day_are_explicit() -> None:
    clock = FixedClock(datetime(2026, 8, 18, 17, 30, tzinfo=timezone.utc))
    bangkok = ZoneInfo("Asia/Bangkok")

    assert clock.now_utc() == datetime(2026, 8, 18, 17, 30, tzinfo=timezone.utc)
    assert local_study_date(now_utc=clock.now_utc(), local_timezone=bangkok).isoformat() == "2026-08-19"


def test_settings_defaults_invalid_values_and_save() -> None:
    saved: list[dict] = []
    service = SettingsService(
        load_raw=lambda: {
            "appearance": {"theme": "invalid"},
            "motion": {"reduced_motion": "yes"},
            "focus_mode": {"enabled": False, "future_key": 7},
            "unknown_category": {"ignored": True},
        },
        save_raw=saved.append,
    )

    assert service.snapshot.appearance["theme"] == "system"
    assert service.snapshot.reduced_motion is False
    assert service.snapshot.focus_mode_enabled is False
    assert service.snapshot.focus_mode["future_key"] == 7

    service.set_focus_mode(True)
    assert service.snapshot.focus_mode_enabled is True
    assert saved[-1]["focus_mode"]["future_key"] == 7
    assert "unknown_category" not in saved[-1]


def test_database_fresh_reopen_and_transaction_rollback() -> None:
    with TemporaryDirectory() as temporary_directory:
        path = Path(temporary_directory) / "anki_alive.sqlite3"
        database = Database(path)
        database.open()
        assert database.connection.execute(
            "SELECT schema_version FROM schema_meta WHERE singleton = 1"
        ).fetchone()[0] == SCHEMA_VERSION
        assert database.connection.execute(
            "SELECT version FROM migration_history ORDER BY version"
        ).fetchall() == [(SCHEMA_VERSION,)]

        try:
            with database.transaction() as connection:
                connection.execute(
                    "INSERT INTO migration_history(version) VALUES (?)",
                    (999,),
                )
                raise RuntimeError("force rollback")
        except RuntimeError:
            pass

        assert database.connection.execute(
            "SELECT version FROM migration_history WHERE version = 999"
        ).fetchone() is None
        database.close()

        reopened = Database(path)
        reopened.open()
        assert reopened.connection.execute(
            "SELECT schema_version FROM schema_meta WHERE singleton = 1"
        ).fetchone()[0] == SCHEMA_VERSION
        reopened.close()


def test_performance_timer_records_named_sample() -> None:
    samples = []
    timer = PerformanceTimer(samples.append)

    with timer.measure("review-hook"):
        sum(range(10))

    assert len(samples) == 1
    assert samples[0].name == "review-hook"
    assert samples[0].duration_ms >= 0


def test_anki_hook_registration_is_idempotent_and_normalizes_review() -> None:
    with TemporaryDirectory() as temporary_directory:
        class FakeDb:
            def __init__(self) -> None:
                self.review_exists = True

            def first(self, sql: str, card_id: int):
                assert "revlog" in sql
                return (1_776_000_000_123, card_id, 3, 820)

            def scalar(self, sql: str, review_id: int):
                assert "revlog" in sql
                return 1 if self.review_exists else None

        db = FakeDb()
        collection = SimpleNamespace(db=db)
        hooks = SimpleNamespace(
            collection_did_load=[],
            profile_will_close=[],
            reviewer_did_answer_card=[],
            state_did_undo=[],
        )
        mw = SimpleNamespace(
            pm=SimpleNamespace(profileFolder=lambda: temporary_directory),
        )
        bus = EventBus()
        observations: list[ReviewObservation] = []
        reversals: list[ReviewReversed] = []
        bus.subscribe(ReviewObservation, observations.append)
        bus.subscribe(ReviewReversed, reversals.append)

        runtime = AnkiHookRuntime(mw=mw, gui_hooks=hooks, event_bus=bus)
        runtime.register()
        runtime.register()
        assert len(hooks.collection_did_load) == 1
        assert len(hooks.reviewer_did_answer_card) == 1
        assert len(hooks.state_did_undo) == 1

        hooks.collection_did_load[0](collection)
        hooks.reviewer_did_answer_card[0](object(), SimpleNamespace(id=42), 3)
        assert len(observations) == 1
        assert observations[0].source_review_id == 1_776_000_000_123
        assert observations[0].response_time_ms == 820

        hooks.state_did_undo[0](object())
        assert reversals == []

        db.review_exists = False
        hooks.state_did_undo[0](object())
        assert len(reversals) == 1
        assert reversals[0].source_review_id == observations[0].source_review_id

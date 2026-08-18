from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import UUID

from anki_alive.core.events import EventBus
from anki_alive.core.focus import FocusPolicy
from anki_alive.core.reconciliation import ReversibleReviewCounter
from anki_alive.core.review import ReviewObservation, ReviewReversed, new_observation
from anki_alive.integration.profile import load_or_create_profile_key
from anki_alive.integration.reviewer import ReviewObserver, SourceReview


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

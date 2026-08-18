from datetime import datetime, timezone
from uuid import UUID

from anki_alive.core.events import EventBus
from anki_alive.core.focus import FocusPolicy
from anki_alive.core.reconciliation import ReversibleReviewCounter
from anki_alive.core.review import ReviewReversed, new_observation


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

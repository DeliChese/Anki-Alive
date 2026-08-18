from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone

from anki_alive.core.events import EventBus
from anki_alive.core.review import ReviewObservation, ReviewReversed, new_observation


@dataclass(frozen=True, slots=True)
class SourceReview:
    review_id: int
    card_id: int
    rating: int
    response_time_ms: int | None = None


class ReviewObserver:
    """Normalize accepted Anki reviews and proven revlog reversals.

    The adapter deliberately receives database lookups as callables. This keeps
    volatile Anki APIs at the integration boundary and lets the mapping be tested
    without launching Anki.
    """

    def __init__(
        self,
        *,
        profile_key: str,
        event_bus: EventBus,
        latest_review_for_card: Callable[[int], SourceReview | None],
        review_exists: Callable[[int], bool],
    ) -> None:
        self._profile_key = profile_key
        self._event_bus = event_bus
        self._latest_review_for_card = latest_review_for_card
        self._review_exists = review_exists
        self._observed: dict[int, ReviewObservation] = {}

    def on_answered(self, *, card_id: int, rating: int) -> ReviewObservation | None:
        source = self._latest_review_for_card(card_id)
        if source is None:
            return None
        if source.card_id != card_id or source.rating != rating:
            return None

        observation = new_observation(
            profile_key=self._profile_key,
            card_id=card_id,
            rating=rating,
            source_review_id=source.review_id,
            response_time_ms=source.response_time_ms,
            reviewed_at_utc=datetime.fromtimestamp(
                source.review_id / 1000,
                tz=timezone.utc,
            ),
        )
        if source.review_id not in self._observed:
            self._observed[source.review_id] = observation
            self._event_bus.publish(observation)
        return self._observed[source.review_id]

    def on_undo_completed(self) -> list[ReviewReversed]:
        """Publish reversals only for tracked revlog rows proven to be gone.

        Anki's undo hook reports that an undo completed, but does not identify a
        review. We therefore verify source revlog existence instead of guessing
        from the operation name or blindly decrementing state.
        """

        reversed_events: list[ReviewReversed] = []
        for source_review_id, observation in list(self._observed.items()):
            if self._review_exists(source_review_id):
                continue
            reversal = ReviewReversed(
                profile_key=self._profile_key,
                card_id=observation.card_id,
                observation_id=observation.observation_id,
                source_review_id=source_review_id,
                reversed_at_utc=datetime.now(timezone.utc),
            )
            del self._observed[source_review_id]
            self._event_bus.publish(reversal)
            reversed_events.append(reversal)
        return reversed_events

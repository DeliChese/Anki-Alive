from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from .review import ReviewObservation, ReviewReversed


@dataclass
class ReversibleReviewCounter:
    """Test-harness projection proving reversal can be reconciled safely.

    This is deliberately not feature state. It exists to prove the Phase 0
    architecture before Expedition or any later mechanic depends on reviews.
    """

    _accepted: dict[UUID, ReviewObservation] = field(default_factory=dict)

    @property
    def value(self) -> int:
        return len(self._accepted)

    def apply_observation(self, event: ReviewObservation) -> None:
        self._accepted.setdefault(event.observation_id, event)

    def apply_reversal(self, event: ReviewReversed) -> None:
        if event.observation_id is not None:
            self._accepted.pop(event.observation_id, None)
            return

        if event.source_review_id is None:
            return

        matched = [
            observation_id
            for observation_id, observation in self._accepted.items()
            if observation.profile_key == event.profile_key
            and observation.card_id == event.card_id
            and observation.source_review_id == event.source_review_id
        ]
        for observation_id in matched:
            self._accepted.pop(observation_id, None)

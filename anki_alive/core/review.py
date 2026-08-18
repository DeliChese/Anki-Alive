from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class ReviewObservation:
    observation_id: UUID
    profile_key: str
    card_id: int
    rating: int
    reviewed_at_utc: datetime
    source_review_id: int | None = None
    response_time_ms: int | None = None
    sequence: int | None = None

    def __post_init__(self) -> None:
        if not self.profile_key:
            raise ValueError("profile_key must not be empty")
        if self.card_id <= 0:
            raise ValueError("card_id must be positive")
        if self.rating not in {1, 2, 3, 4}:
            raise ValueError("rating must be one of Anki's four review ratings")
        if self.reviewed_at_utc.tzinfo is None:
            raise ValueError("reviewed_at_utc must be timezone-aware")


@dataclass(frozen=True, slots=True)
class ReviewReversed:
    profile_key: str
    card_id: int
    reversed_at_utc: datetime
    observation_id: UUID | None = None
    source_review_id: int | None = None

    def __post_init__(self) -> None:
        if not self.profile_key:
            raise ValueError("profile_key must not be empty")
        if self.card_id <= 0:
            raise ValueError("card_id must be positive")
        if self.reversed_at_utc.tzinfo is None:
            raise ValueError("reversed_at_utc must be timezone-aware")
        if self.observation_id is None and self.source_review_id is None:
            raise ValueError("a reversal needs observation_id or source_review_id")


def new_observation(
    *,
    profile_key: str,
    card_id: int,
    rating: int,
    source_review_id: int | None = None,
    response_time_ms: int | None = None,
    sequence: int | None = None,
    reviewed_at_utc: datetime | None = None,
    observation_id: UUID | None = None,
) -> ReviewObservation:
    return ReviewObservation(
        observation_id=observation_id or uuid4(),
        profile_key=profile_key,
        card_id=card_id,
        rating=rating,
        reviewed_at_utc=reviewed_at_utc or datetime.now(timezone.utc),
        source_review_id=source_review_id,
        response_time_ms=response_time_ms,
        sequence=sequence,
    )

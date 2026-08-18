from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import NAMESPACE_URL, UUID, uuid4, uuid5

_OBSERVATION_NAMESPACE = uuid5(NAMESPACE_URL, "anki-alive:review-observation:v1")


@dataclass(frozen=True)
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


@dataclass(frozen=True)
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


def observation_id_for_source(*, profile_key: str, source_review_id: int) -> UUID:
    """Return a stable add-on identity for one Anki revlog row.

    The profile key is part of the namespace input because revlog IDs are local
    collection identifiers and must never collide across profiles.
    """

    if not profile_key:
        raise ValueError("profile_key must not be empty")
    if source_review_id <= 0:
        raise ValueError("source_review_id must be positive")
    return uuid5(_OBSERVATION_NAMESPACE, f"{profile_key}:{source_review_id}")


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
    if observation_id is None:
        observation_id = (
            observation_id_for_source(
                profile_key=profile_key,
                source_review_id=source_review_id,
            )
            if source_review_id is not None
            else uuid4()
        )

    return ReviewObservation(
        observation_id=observation_id,
        profile_key=profile_key,
        card_id=card_id,
        rating=rating,
        reviewed_at_utc=reviewed_at_utc or datetime.now(timezone.utc),
        source_review_id=source_review_id,
        response_time_ms=response_time_ms,
        sequence=sequence,
    )

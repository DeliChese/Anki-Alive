from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class MemorySnapshot:
    """Feature-neutral memory facts available to learning features.

    The Memory Engine reports host-derived facts only. Feature policy such as
    Oracle candidacy belongs outside this module.
    """

    card_id: int
    observed_at_utc: datetime
    stability: float | None = None
    difficulty: float | None = None
    retrievability: float | None = None
    interval_days: int = 0
    lapses: int = 0
    review_count: int = 0
    recent_outcomes: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if self.card_id <= 0:
            raise ValueError("card_id must be positive")
        if self.observed_at_utc.tzinfo is None:
            raise ValueError("observed_at_utc must be timezone-aware")
        if self.interval_days < 0 or self.lapses < 0 or self.review_count < 0:
            raise ValueError("memory counters must not be negative")
        if self.retrievability is not None and not 0.0 <= self.retrievability <= 1.0:
            raise ValueError("retrievability must be between 0 and 1")


class MemoryEngine(Protocol):
    """Feature-neutral provider of normalized memory state."""

    def snapshot_for_card(self, card_id: int) -> MemorySnapshot | None:
        """Return current normalized memory facts, or None when unavailable."""
        ...

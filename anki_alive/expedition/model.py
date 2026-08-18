from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from math import ceil
from uuid import UUID


class ExpeditionStatus(str, Enum):
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"
    INVALIDATED = "INVALIDATED"


class CheckpointStatus(str, Enum):
    PENDING = "PENDING"
    REACHED = "REACHED"


@dataclass(frozen=True)
class Expedition:
    expedition_id: UUID
    profile_key: str
    local_study_date: date
    status: ExpeditionStatus
    created_at: datetime
    target_reviews: int
    completed_reviews: int = 0
    started_at: datetime | None = None
    paused_at: datetime | None = None
    completed_at: datetime | None = None
    ended_at: datetime | None = None
    checkpoint_plan_version: int = 1
    seed: int | None = None
    schema_version: int = 1

    def __post_init__(self) -> None:
        if not self.profile_key:
            raise ValueError("profile_key must not be empty")
        if self.target_reviews <= 0:
            raise ValueError("target_reviews must be positive")
        if self.completed_reviews < 0:
            raise ValueError("completed_reviews must not be negative")
        if self.completed_reviews > self.target_reviews:
            raise ValueError("completed_reviews must not exceed target_reviews")
        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")


@dataclass(frozen=True)
class ExpeditionCheckpoint:
    checkpoint_id: UUID
    expedition_id: UUID
    ordinal: int
    target_progress: int
    status: CheckpointStatus = CheckpointStatus.PENDING
    reached_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.ordinal <= 0:
            raise ValueError("ordinal must be positive")
        if self.target_progress <= 0:
            raise ValueError("target_progress must be positive")


def checkpoint_targets(target_reviews: int, *, max_segment_size: int = 15) -> tuple[int, ...]:
    """Build a stable, bounded checkpoint plan for an Expedition.

    The plan is intentionally simple in Phase 1: no randomness, no moving goal,
    and no checkpoint farther than roughly ``max_segment_size`` reviews away.
    The final checkpoint is always the Expedition target.
    """

    if target_reviews <= 0:
        raise ValueError("target_reviews must be positive")
    if max_segment_size <= 0:
        raise ValueError("max_segment_size must be positive")

    segment_count = max(1, ceil(target_reviews / max_segment_size))
    targets: list[int] = []
    for index in range(1, segment_count + 1):
        target = round(index * target_reviews / segment_count)
        target = min(target_reviews, max(1, target))
        if not targets or target > targets[-1]:
            targets.append(target)
    if targets[-1] != target_reviews:
        targets.append(target_reviews)
    return tuple(targets)

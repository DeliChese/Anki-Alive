from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ExpeditionProgressed:
    expedition_id: UUID
    completed_reviews: int
    target_reviews: int


@dataclass(frozen=True)
class CheckpointReached:
    expedition_id: UUID
    checkpoint_id: UUID
    target_progress: int


@dataclass(frozen=True)
class ExpeditionCompleted:
    expedition_id: UUID
    completed_reviews: int
    target_reviews: int

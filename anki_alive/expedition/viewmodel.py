from __future__ import annotations

from dataclasses import dataclass

from .model import CheckpointStatus, Expedition, ExpeditionCheckpoint


@dataclass(frozen=True)
class CheckpointView:
    ordinal: int
    target_progress: int
    position_percent: float
    state: str
    is_completion: bool


@dataclass(frozen=True)
class ExpeditionView:
    completed_reviews: int
    target_reviews: int
    progress_percent: float
    checkpoints: tuple[CheckpointView, ...]
    reached_checkpoints: int
    total_checkpoints: int
    next_checkpoint_target: int | None
    reviews_to_next_checkpoint: int | None


def build_expedition_view(
    expedition: Expedition,
    checkpoints: tuple[ExpeditionCheckpoint, ...],
) -> ExpeditionView:
    target = expedition.target_reviews
    completed = expedition.completed_reviews
    progress_percent = min(100.0, max(0.0, completed * 100.0 / target))

    first_pending_target: int | None = None
    checkpoint_views: list[CheckpointView] = []
    reached = 0

    for checkpoint in checkpoints:
        is_reached = checkpoint.status is CheckpointStatus.REACHED
        if is_reached:
            reached += 1
            state = "reached"
        elif first_pending_target is None:
            first_pending_target = checkpoint.target_progress
            state = "nearby"
        else:
            state = "future"

        checkpoint_views.append(
            CheckpointView(
                ordinal=checkpoint.ordinal,
                target_progress=checkpoint.target_progress,
                position_percent=min(
                    100.0,
                    max(0.0, checkpoint.target_progress * 100.0 / target),
                ),
                state=state,
                is_completion=checkpoint.target_progress == target,
            )
        )

    reviews_to_next = (
        max(0, first_pending_target - completed)
        if first_pending_target is not None
        else None
    )
    return ExpeditionView(
        completed_reviews=completed,
        target_reviews=target,
        progress_percent=progress_percent,
        checkpoints=tuple(checkpoint_views),
        reached_checkpoints=reached,
        total_checkpoints=len(checkpoint_views),
        next_checkpoint_target=first_pending_target,
        reviews_to_next_checkpoint=reviews_to_next,
    )

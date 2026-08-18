from __future__ import annotations

from datetime import tzinfo
from uuid import UUID

from anki_alive.core.events import EventBus
from anki_alive.core.ids import IdFactory
from anki_alive.core.review import ReviewObservation, ReviewReversed
from anki_alive.core.time import Clock, local_study_date

from .events import CheckpointReached, ExpeditionCompleted, ExpeditionProgressed
from .model import CheckpointStatus, Expedition, ExpeditionCheckpoint, ExpeditionStatus, checkpoint_targets
from .repository import ExpeditionRepository


class ExpeditionService:
    """Phase 1 domain service. Every accepted grade counts as one unit of work."""

    def __init__(
        self,
        *,
        repository: ExpeditionRepository,
        event_bus: EventBus,
        clock: Clock,
        ids: IdFactory,
        local_timezone: tzinfo,
    ) -> None:
        self.repository = repository
        self.event_bus = event_bus
        self.clock = clock
        self.ids = ids
        self.local_timezone = local_timezone

    def plan(self, *, profile_key: str, target_reviews: int) -> Expedition:
        if self.repository.resumable_for_profile(profile_key) is not None:
            raise ValueError("profile already has a resumable Expedition")
        now = self.clock.now_utc()
        expedition_id = self.ids.new()
        expedition = Expedition(
            expedition_id=expedition_id,
            profile_key=profile_key,
            local_study_date=local_study_date(now_utc=now, local_timezone=self.local_timezone),
            status=ExpeditionStatus.PLANNED,
            created_at=now,
            target_reviews=target_reviews,
        )
        checkpoints = tuple(
            ExpeditionCheckpoint(
                checkpoint_id=self.ids.new(),
                expedition_id=expedition_id,
                ordinal=ordinal,
                target_progress=target,
            )
            for ordinal, target in enumerate(checkpoint_targets(target_reviews), start=1)
        )
        self.repository.create(expedition, checkpoints)
        return expedition

    def start(self, expedition_id: UUID) -> Expedition:
        return self.repository.set_status(expedition_id, ExpeditionStatus.ACTIVE, self.clock.now_utc())

    def pause(self, expedition_id: UUID) -> Expedition:
        return self.repository.set_status(expedition_id, ExpeditionStatus.PAUSED, self.clock.now_utc())

    def resume(self, expedition_id: UUID) -> Expedition:
        return self.repository.set_status(expedition_id, ExpeditionStatus.ACTIVE, self.clock.now_utc())

    def end(self, expedition_id: UUID) -> Expedition:
        return self.repository.set_status(expedition_id, ExpeditionStatus.ABANDONED, self.clock.now_utc())

    def on_review_observation(self, event: ReviewObservation) -> None:
        expedition = self.repository.active_for_profile(event.profile_key)
        if expedition is None:
            return
        before = self.repository.checkpoints(expedition.expedition_id)
        updated, after, inserted = self.repository.apply_observation(
            expedition.expedition_id, event, self.clock.now_utc()
        )
        if not inserted:
            return
        self.event_bus.publish(
            ExpeditionProgressed(updated.expedition_id, updated.completed_reviews, updated.target_reviews)
        )
        before_reached = {
            item.checkpoint_id for item in before if item.status is CheckpointStatus.REACHED
        }
        for checkpoint in after:
            if checkpoint.status is CheckpointStatus.REACHED and checkpoint.checkpoint_id not in before_reached:
                self.event_bus.publish(
                    CheckpointReached(updated.expedition_id, checkpoint.checkpoint_id, checkpoint.target_progress)
                )
        if updated.status is ExpeditionStatus.COMPLETED:
            self.event_bus.publish(
                ExpeditionCompleted(updated.expedition_id, updated.completed_reviews, updated.target_reviews)
            )

    def on_review_reversed(self, event: ReviewReversed) -> None:
        expedition = self.repository.expedition_for_reversal(event)
        if expedition is None:
            return
        updated, _, changed = self.repository.apply_reversal(
            expedition.expedition_id, event, self.clock.now_utc()
        )
        if changed:
            self.event_bus.publish(
                ExpeditionProgressed(updated.expedition_id, updated.completed_reviews, updated.target_reviews)
            )

from __future__ import annotations

from datetime import date, tzinfo
from uuid import UUID

from anki_alive.core.events import EventBus
from anki_alive.core.ids import IdFactory
from anki_alive.core.review import ReviewObservation, ReviewReversed
from anki_alive.core.time import Clock, local_study_date

from .events import (
    CheckpointReached,
    ExpeditionCompleted,
    ExpeditionEnded,
    ExpeditionPaused,
    ExpeditionPlanned,
    ExpeditionProgressed,
    ExpeditionReopened,
    ExpeditionResumed,
    ExpeditionStarted,
)
from .model import (
    CheckpointStatus,
    Expedition,
    ExpeditionCheckpoint,
    ExpeditionStatus,
    checkpoint_targets,
)
from .repository import ExpeditionRepository


DEFAULT_EXPEDITION_TARGET = 50


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

    def study_date(self) -> date:
        return local_study_date(
            now_utc=self.clock.now_utc(),
            local_timezone=self.local_timezone,
        )

    def get(self, expedition_id: UUID) -> Expedition | None:
        return self.repository.get(expedition_id)

    def checkpoints(self, expedition_id: UUID) -> tuple[ExpeditionCheckpoint, ...]:
        return self.repository.checkpoints(expedition_id)

    def resumable(self, profile_key: str) -> Expedition | None:
        return self.repository.resumable_for_profile(profile_key)

    @staticmethod
    def target_for_available_reviews(
        available_reviews: int,
        *,
        preferred_reviews: int = DEFAULT_EXPEDITION_TARGET,
    ) -> int:
        """Return a bounded provisional Phase 1 target.

        The exact sizing policy remains intentionally provisional. This first
        implementation chooses a standard ceiling and clamps it to work that is
        currently available. Once created, the Expedition target never drifts.
        """

        if available_reviews <= 0:
            raise ValueError("available_reviews must be positive")
        if preferred_reviews <= 0:
            raise ValueError("preferred_reviews must be positive")
        return min(available_reviews, preferred_reviews)

    def plan_for_available_reviews(
        self,
        *,
        profile_key: str,
        available_reviews: int,
        preferred_reviews: int = DEFAULT_EXPEDITION_TARGET,
    ) -> Expedition:
        return self.plan(
            profile_key=profile_key,
            target_reviews=self.target_for_available_reviews(
                available_reviews,
                preferred_reviews=preferred_reviews,
            ),
        )

    def plan(self, *, profile_key: str, target_reviews: int) -> Expedition:
        if self.repository.resumable_for_profile(profile_key) is not None:
            raise ValueError("profile already has a resumable Expedition")
        now = self.clock.now_utc()
        expedition_id = self.ids.new()
        expedition = Expedition(
            expedition_id=expedition_id,
            profile_key=profile_key,
            local_study_date=local_study_date(
                now_utc=now,
                local_timezone=self.local_timezone,
            ),
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
            for ordinal, target in enumerate(
                checkpoint_targets(target_reviews),
                start=1,
            )
        )
        self.repository.create(expedition, checkpoints)
        self.event_bus.publish(
            ExpeditionPlanned(
                expedition_id=expedition.expedition_id,
                target_reviews=expedition.target_reviews,
            )
        )
        return expedition

    def start(self, expedition_id: UUID) -> Expedition:
        expedition = self._require_status(
            expedition_id,
            {ExpeditionStatus.PLANNED},
            "start",
        )
        updated = self.repository.set_status(
            expedition.expedition_id,
            ExpeditionStatus.ACTIVE,
            self.clock.now_utc(),
        )
        self.event_bus.publish(ExpeditionStarted(updated.expedition_id))
        return updated

    def pause(self, expedition_id: UUID) -> Expedition:
        expedition = self._require_status(
            expedition_id,
            {ExpeditionStatus.ACTIVE},
            "pause",
        )
        updated = self.repository.set_status(
            expedition.expedition_id,
            ExpeditionStatus.PAUSED,
            self.clock.now_utc(),
        )
        self.event_bus.publish(ExpeditionPaused(updated.expedition_id))
        return updated

    def resume(self, expedition_id: UUID) -> Expedition:
        expedition = self._require_status(
            expedition_id,
            {ExpeditionStatus.PAUSED},
            "resume",
        )
        updated = self.repository.set_status(
            expedition.expedition_id,
            ExpeditionStatus.ACTIVE,
            self.clock.now_utc(),
        )
        self.event_bus.publish(ExpeditionResumed(updated.expedition_id))
        return updated

    def end(self, expedition_id: UUID) -> Expedition:
        expedition = self._require_status(
            expedition_id,
            {
                ExpeditionStatus.PLANNED,
                ExpeditionStatus.ACTIVE,
                ExpeditionStatus.PAUSED,
            },
            "end",
        )
        updated = self.repository.set_status(
            expedition.expedition_id,
            ExpeditionStatus.ABANDONED,
            self.clock.now_utc(),
        )
        self.event_bus.publish(
            ExpeditionEnded(
                expedition_id=updated.expedition_id,
                completed_reviews=updated.completed_reviews,
                target_reviews=updated.target_reviews,
            )
        )
        return updated

    def on_review_observation(self, event: ReviewObservation) -> None:
        expedition = self.repository.active_for_profile(event.profile_key)
        if expedition is None:
            return
        before = self.repository.checkpoints(expedition.expedition_id)
        updated, after, inserted = self.repository.apply_observation(
            expedition.expedition_id,
            event,
            self.clock.now_utc(),
        )
        if not inserted:
            return

        self.event_bus.publish(
            ExpeditionProgressed(
                updated.expedition_id,
                updated.completed_reviews,
                updated.target_reviews,
            )
        )

        before_reached = {
            item.checkpoint_id
            for item in before
            if item.status is CheckpointStatus.REACHED
        }
        for checkpoint in after:
            if (
                checkpoint.status is CheckpointStatus.REACHED
                and checkpoint.checkpoint_id not in before_reached
            ):
                self.event_bus.publish(
                    CheckpointReached(
                        updated.expedition_id,
                        checkpoint.checkpoint_id,
                        checkpoint.target_progress,
                    )
                )

        if updated.status is ExpeditionStatus.COMPLETED:
            self.event_bus.publish(
                ExpeditionCompleted(
                    updated.expedition_id,
                    updated.completed_reviews,
                    updated.target_reviews,
                )
            )

    def on_review_reversed(self, event: ReviewReversed) -> None:
        expedition = self.repository.expedition_for_reversal(event)
        if expedition is None:
            return
        was_completed = expedition.status is ExpeditionStatus.COMPLETED
        updated, _, changed = self.repository.apply_reversal(
            expedition.expedition_id,
            event,
            self.clock.now_utc(),
        )
        if not changed:
            return
        self.event_bus.publish(
            ExpeditionProgressed(
                updated.expedition_id,
                updated.completed_reviews,
                updated.target_reviews,
            )
        )
        if was_completed and updated.status is ExpeditionStatus.ACTIVE:
            self.event_bus.publish(
                ExpeditionReopened(
                    updated.expedition_id,
                    updated.completed_reviews,
                    updated.target_reviews,
                )
            )

    def _require_status(
        self,
        expedition_id: UUID,
        allowed: set[ExpeditionStatus],
        action: str,
    ) -> Expedition:
        expedition = self.repository.get(expedition_id)
        if expedition is None:
            raise KeyError(expedition_id)
        if expedition.status not in allowed:
            allowed_values = ", ".join(sorted(item.value for item in allowed))
            raise ValueError(
                f"cannot {action} Expedition in {expedition.status.value}; "
                f"expected one of {allowed_values}"
            )
        return expedition

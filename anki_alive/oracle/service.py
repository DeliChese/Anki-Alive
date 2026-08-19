from __future__ import annotations

from uuid import UUID

from anki_alive.core.events import EventBus
from anki_alive.core.ids import IdFactory
from anki_alive.core.memory import MemorySnapshot
from anki_alive.core.presentation import EventOrchestrator, PresentationEvent, PresentationProminence
from anki_alive.core.review import ReviewObservation, ReviewReversed
from anki_alive.core.time import Clock
from anki_alive.presentation import PresentationRepository

from .events import OracleCommitted, OracleResolutionReversed, OracleResolved
from .model import OraclePrediction
from .policy import OraclePolicy
from .repository import OracleRepository


class OracleService:
    """Phase 2 Oracle domain lifecycle.

    Commitment happens explicitly before review outcome. Accepted review events
    resolve an existing commitment; reversal reopens the same commitment rather
    than rerolling it.
    """

    def __init__(
        self,
        *,
        repository: OracleRepository,
        policy: OraclePolicy,
        event_bus: EventBus,
        clock: Clock,
        ids: IdFactory,
        presentation_repository: PresentationRepository | None = None,
        orchestrator: EventOrchestrator | None = None,
    ) -> None:
        self.repository = repository
        self.policy = policy
        self.event_bus = event_bus
        self.clock = clock
        self.ids = ids
        self.presentation_repository = presentation_repository
        self.orchestrator = orchestrator

    def commitment_count(self, expedition_id: UUID) -> int:
        return self.repository.count_for_expedition(expedition_id)

    def commit(
        self,
        *,
        expedition_id: UUID,
        snapshot: MemorySnapshot,
    ) -> OraclePrediction | None:
        decision = self.policy.decide(snapshot)
        if decision is None:
            return None
        prediction = OraclePrediction(
            oracle_prediction_id=self.ids.new(),
            expedition_id=expedition_id,
            card_id=snapshot.card_id,
            committed_at=self.clock.now_utc(),
            policy_version=decision.policy_version,
            predicted_outcome=decision.predicted_outcome,
            predicted_recall_probability=decision.predicted_recall_probability,
        )
        stored = self.repository.create(prediction)
        if stored.oracle_prediction_id == prediction.oracle_prediction_id:
            self.event_bus.publish(
                OracleCommitted(
                    oracle_prediction_id=stored.oracle_prediction_id,
                    expedition_id=stored.expedition_id,
                    card_id=stored.card_id,
                    predicted_outcome=stored.predicted_outcome,
                )
            )
        return stored

    def on_review_observation(self, observation: ReviewObservation) -> None:
        prediction = self.repository.committed_for_profile_card(
            observation.profile_key,
            observation.card_id,
        )
        if prediction is None:
            return
        resolved = self.repository.resolve(prediction.oracle_prediction_id, observation)
        if resolved.result is None or resolved.actual_recall_success is None or resolved.actual_rating is None:
            raise RuntimeError("resolved Oracle prediction is missing outcome fields")

        presentation = self._presentation_event(resolved)
        if self.presentation_repository is not None:
            self.presentation_repository.enqueue(
                profile_key=observation.profile_key,
                event=presentation,
                created_at=observation.reviewed_at_utc,
            )
        if self.orchestrator is not None:
            self.orchestrator.enqueue(presentation)

        # Publish only after durable presentation state exists. UI subscribers
        # may schedule asynchronously or execute immediately in tests; either
        # way they can now resolve the reveal by dedupe key safely.
        self.event_bus.publish(
            OracleResolved(
                oracle_prediction_id=resolved.oracle_prediction_id,
                expedition_id=resolved.expedition_id,
                card_id=resolved.card_id,
                predicted_outcome=resolved.predicted_outcome,
                actual_recall_success=resolved.actual_recall_success,
                actual_rating=resolved.actual_rating,
                result=resolved.result,
            )
        )

    def on_review_reversed(self, reversal: ReviewReversed) -> None:
        prediction = self.repository.resolved_for_reversal(reversal)
        if prediction is None:
            return
        self.repository.reopen_after_reversal(prediction.oracle_prediction_id)
        dedupe_key = self._dedupe_key(prediction.oracle_prediction_id)
        if self.presentation_repository is not None:
            self.presentation_repository.invalidate(dedupe_key, at=reversal.reversed_at_utc)
        self.event_bus.publish(
            OracleResolutionReversed(
                oracle_prediction_id=prediction.oracle_prediction_id,
                expedition_id=prediction.expedition_id,
                card_id=prediction.card_id,
            )
        )

    @classmethod
    def _dedupe_key(cls, prediction_id: UUID) -> str:
        return f"oracle:{prediction_id}:resolution"

    @classmethod
    def _presentation_event(cls, prediction: OraclePrediction) -> PresentationEvent:
        if prediction.result is None or prediction.actual_recall_success is None:
            raise ValueError("Oracle reveal requires a resolved prediction")
        return PresentationEvent(
            kind="oracle_resolution",
            prominence=PresentationProminence.MAJOR,
            priority=50,
            dedupe_key=cls._dedupe_key(prediction.oracle_prediction_id),
            payload={
                "oracle_prediction_id": str(prediction.oracle_prediction_id),
                "card_id": prediction.card_id,
                "predicted_outcome": prediction.predicted_outcome.value,
                "actual_recall_success": prediction.actual_recall_success,
                "result": prediction.result.value,
            },
        )

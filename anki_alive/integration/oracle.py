from __future__ import annotations

from typing import Any

from anki_alive.core.review_context import ReviewContextService
from anki_alive.expedition.model import ExpeditionStatus
from anki_alive.expedition.repository import ExpeditionRepository
from anki_alive.integration.memory import AnkiMemoryEngine
from anki_alive.integration.profile import load_or_create_profile_key
from anki_alive.oracle.service import OracleService

ORACLE_REVIEW_CADENCE = 5


class OracleReviewerRuntime:
    """Thin host wiring that commits Oracle before a review outcome exists."""

    def __init__(
        self,
        *,
        mw: Any,
        gui_hooks: Any,
        expedition_repository: ExpeditionRepository,
        oracle: OracleService,
        diagnostics: Any,
    ) -> None:
        self._mw = mw
        self._gui_hooks = gui_hooks
        self._expedition_repository = expedition_repository
        self._oracle = oracle
        self._diagnostics = diagnostics
        self._profile_key: str | None = None
        self._context: ReviewContextService | None = None
        self._registered = False

    def register(self) -> None:
        if self._registered:
            return
        self._gui_hooks.collection_did_load.append(self._on_collection_loaded)
        self._gui_hooks.profile_will_close.append(self._on_profile_will_close)
        self._gui_hooks.reviewer_did_show_question.append(self._on_question_shown)
        self._registered = True

    def _on_collection_loaded(self, collection: Any) -> None:
        self._profile_key = load_or_create_profile_key(self._mw.pm.profileFolder())
        self._context = ReviewContextService(
            expedition_repository=self._expedition_repository,
            memory_engine=AnkiMemoryEngine(collection),
        )

    def _on_profile_will_close(self) -> None:
        self._profile_key = None
        self._context = None

    def _on_question_shown(self, card: Any) -> None:
        if self._profile_key is None or self._context is None:
            return
        try:
            card_id = int(card.id)
            context = self._context.for_card(
                profile_key=self._profile_key,
                card_id=card_id,
            )
            expedition = context.expedition
            snapshot = context.memory_snapshot
            if (
                expedition is None
                or expedition.status is not ExpeditionStatus.ACTIVE
                or snapshot is None
            ):
                return

            # One commitment per five accepted-review progress units, but use
            # the first eligible card in each window instead of wasting the
            # whole window when its first card lacks enough evidence.
            allowed_commitments = expedition.completed_reviews // ORACLE_REVIEW_CADENCE + 1
            if self._oracle.commitment_count(expedition.expedition_id) >= allowed_commitments:
                return

            prediction = self._oracle.commit(
                expedition_id=expedition.expedition_id,
                snapshot=snapshot,
            )
            if prediction is None:
                return
            self._diagnostics.emit(
                "oracle_committed",
                oracle_prediction_id=str(prediction.oracle_prediction_id),
                expedition_id=str(prediction.expedition_id),
                card_id=prediction.card_id,
                policy_version=prediction.policy_version,
                # Intentionally do not emit predicted outcome here; diagnostics
                # should not create a pre-answer leakage path in normal UI.
                has_retrievability=prediction.predicted_recall_probability is not None,
            )
        except Exception as error:
            # Oracle is optional. A failure here must never block the question.
            self._diagnostics.emit(
                "oracle_commit_error",
                error_type=type(error).__name__,
            )

from __future__ import annotations

from typing import Any

from anki_alive.core.events import EventBus
from anki_alive.integration.profile import load_or_create_profile_key
from anki_alive.integration.reviewer import ReviewObserver, SourceReview


class AnkiHookRuntime:
    """Concrete thin wiring for modern Anki GUI hooks.

    Importing this module does not import `aqt`. The caller supplies `mw` and
    `gui_hooks`, keeping host dependencies isolated and making registration easy
    to test with fakes.
    """

    def __init__(self, *, mw: Any, gui_hooks: Any, event_bus: EventBus) -> None:
        self._mw = mw
        self._gui_hooks = gui_hooks
        self._event_bus = event_bus
        self._review_observer: ReviewObserver | None = None
        self._registered = False

    def register(self) -> None:
        if self._registered:
            return
        self._append_once(self._gui_hooks.collection_did_load, self._on_collection_loaded)
        self._append_once(self._gui_hooks.profile_will_close, self._on_profile_will_close)
        self._append_once(self._gui_hooks.reviewer_did_answer_card, self._on_answered)
        self._append_once(self._gui_hooks.state_did_undo, self._on_undo)
        self._registered = True

    @staticmethod
    def _append_once(hook: Any, handler: Any) -> None:
        if handler not in hook:
            hook.append(handler)

    def _on_collection_loaded(self, collection: Any) -> None:
        profile_key = load_or_create_profile_key(self._mw.pm.profileFolder())

        def latest_review_for_card(card_id: int) -> SourceReview | None:
            row = collection.db.first(
                "SELECT id, cid, ease, time FROM revlog WHERE cid = ? ORDER BY id DESC LIMIT 1",
                card_id,
            )
            if not row:
                return None
            return SourceReview(
                review_id=int(row[0]),
                card_id=int(row[1]),
                rating=int(row[2]),
                response_time_ms=int(row[3]) if row[3] is not None else None,
            )

        def review_exists(review_id: int) -> bool:
            return bool(
                collection.db.scalar(
                    "SELECT 1 FROM revlog WHERE id = ?",
                    review_id,
                )
            )

        self._review_observer = ReviewObserver(
            profile_key=profile_key,
            event_bus=self._event_bus,
            latest_review_for_card=latest_review_for_card,
            review_exists=review_exists,
        )

    def _on_profile_will_close(self) -> None:
        self._review_observer = None

    def _on_answered(self, reviewer: Any, card: Any, ease: int) -> None:
        if self._review_observer is None:
            return
        self._review_observer.on_answered(card_id=int(card.id), rating=int(ease))

    def _on_undo(self, changes_after_undo: Any) -> None:
        del changes_after_undo
        if self._review_observer is None:
            return
        self._review_observer.on_undo_completed()

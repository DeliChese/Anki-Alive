from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from anki_alive.core.memory import MemorySnapshot

FSRS5_DEFAULT_DECAY = 0.5
RECENT_OUTCOME_LIMIT = 5


def fsrs_retrievability(*, stability: float, elapsed_days: float, decay: float) -> float:
    """Compute current FSRS retrievability from Anki's persisted memory facts.

    Anki stores decay as a positive value. The current forgetting curve is:

        factor = 0.9 ** (-1 / decay) - 1
        R = (1 + factor * t / stability) ** (-decay)
    """

    if stability <= 0:
        raise ValueError("stability must be positive")
    if elapsed_days < 0:
        raise ValueError("elapsed_days must not be negative")
    if decay <= 0:
        raise ValueError("decay must be positive")
    factor = 0.9 ** (-1.0 / decay) - 1.0
    value = (1.0 + factor * elapsed_days / stability) ** (-decay)
    return min(1.0, max(0.0, value))


class AnkiMemoryEngine:
    """Feature-neutral adapter over current Anki card/FSRS state.

    Host-specific Card and Collection objects terminate here. Oracle receives a
    plain MemorySnapshot and never reaches into Anki scheduler internals.
    """

    def __init__(
        self,
        collection: Any,
        *,
        now_utc: Callable[[], datetime] | None = None,
    ) -> None:
        self._collection = collection
        self._now_utc = now_utc or (lambda: datetime.now(timezone.utc))

    def snapshot_for_card(self, card_id: int) -> MemorySnapshot | None:
        if card_id <= 0:
            return None
        try:
            card = self._collection.get_card(card_id)
        except Exception:
            return None

        now = self._now_utc()
        if now.tzinfo is None:
            raise ValueError("now_utc must return a timezone-aware datetime")
        now = now.astimezone(timezone.utc)

        state = getattr(card, "memory_state", None)
        stability = (
            float(getattr(state, "stability"))
            if state is not None and getattr(state, "stability", None) is not None
            else None
        )
        difficulty = (
            float(getattr(state, "difficulty"))
            if state is not None and getattr(state, "difficulty", None) is not None
            else None
        )
        retrievability = self._retrievability(card, now, stability)

        return MemorySnapshot(
            card_id=int(card_id),
            observed_at_utc=now,
            stability=stability,
            difficulty=difficulty,
            retrievability=retrievability,
            interval_days=max(0, int(getattr(card, "ivl", 0) or 0)),
            lapses=max(0, int(getattr(card, "lapses", 0) or 0)),
            review_count=max(0, int(getattr(card, "reps", 0) or 0)),
            recent_outcomes=self._recent_outcomes(card_id),
        )

    @staticmethod
    def _retrievability(card: Any, now: datetime, stability: float | None) -> float | None:
        if stability is None or stability <= 0:
            return None
        last_review_time = getattr(card, "last_review_time", None)
        if last_review_time is None:
            return None
        elapsed_seconds = max(0.0, now.timestamp() - float(last_review_time))
        decay = float(getattr(card, "decay", None) or FSRS5_DEFAULT_DECAY)
        if decay <= 0:
            return None
        return fsrs_retrievability(
            stability=stability,
            elapsed_days=elapsed_seconds / 86_400.0,
            decay=decay,
        )

    def _recent_outcomes(self, card_id: int) -> tuple[int, ...]:
        try:
            rows = self._collection.db.list(
                "SELECT ease FROM revlog WHERE cid = ? ORDER BY id DESC LIMIT ?",
                card_id,
                RECENT_OUTCOME_LIMIT,
            )
        except Exception:
            return ()
        return tuple(int(value) for value in rows if int(value) in {1, 2, 3, 4})

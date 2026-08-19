from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from anki_alive.core.memory import MemoryEngine, MemorySnapshot
from anki_alive.expedition.model import Expedition
from anki_alive.expedition.repository import ExpeditionRepository


@dataclass(frozen=True)
class ReviewFeatureContext:
    expedition: Expedition | None
    memory_snapshot: MemorySnapshot | None


class ReviewContextService:
    """Single reviewer-time aggregation seam for Phase 2 features.

    This service owns no durable state. It gathers the current Expedition and
    normalized memory facts so later features do not each invent their own
    reviewer hot-path lookups.
    """

    def __init__(
        self,
        *,
        expedition_repository: ExpeditionRepository,
        memory_engine: MemoryEngine,
    ) -> None:
        self.expedition_repository = expedition_repository
        self.memory_engine = memory_engine

    def for_card(self, *, profile_key: str, card_id: int) -> ReviewFeatureContext:
        return ReviewFeatureContext(
            expedition=self.expedition_repository.active_for_profile(profile_key),
            memory_snapshot=self.memory_engine.snapshot_for_card(card_id),
        )

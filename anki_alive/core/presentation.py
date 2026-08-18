from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any


class PresentationProminence(IntEnum):
    AMBIENT = 0
    MINOR = 1
    MAJOR = 2
    SESSION_CLOSURE = 3


@dataclass(frozen=True)
class PresentationEvent:
    kind: str
    prominence: PresentationProminence
    priority: int = 0
    dedupe_key: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)


class EventOrchestrator:
    """Small Phase 1 presentation scheduler.

    Domain state never lives here. The orchestrator only decides which
    presentation may surface at one UI/review boundary.
    """

    def __init__(self) -> None:
        self._pending: list[PresentationEvent] = []
        self._dedupe_keys: set[str] = set()

    def enqueue(self, event: PresentationEvent) -> bool:
        if event.dedupe_key and event.dedupe_key in self._dedupe_keys:
            return False
        self._pending.append(event)
        if event.dedupe_key:
            self._dedupe_keys.add(event.dedupe_key)
        return True

    @property
    def pending_count(self) -> int:
        return len(self._pending)

    def take_boundary(self) -> tuple[PresentationEvent, ...]:
        """Return events allowed to surface at the next presentation boundary.

        Ambient/minor events may coexist. At most one major/closure event is
        allowed, and a stronger closure suppresses competing major events from
        the same boundary.
        """

        if not self._pending:
            return ()

        pending = self._pending
        self._pending = []
        self._dedupe_keys.clear()

        quiet = [
            event
            for event in pending
            if event.prominence < PresentationProminence.MAJOR
        ]
        prominent = [
            event
            for event in pending
            if event.prominence >= PresentationProminence.MAJOR
        ]

        selected: list[PresentationEvent] = []
        if prominent:
            selected.append(
                max(
                    prominent,
                    key=lambda item: (int(item.prominence), item.priority),
                )
            )
        selected.extend(
            sorted(
                quiet,
                key=lambda item: (-int(item.prominence), -item.priority),
            )
        )
        return tuple(selected)

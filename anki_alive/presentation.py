from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import NAMESPACE_URL, UUID, uuid5

from anki_alive.core.presentation import PresentationEvent, PresentationProminence
from anki_alive.storage import Database

_PRESENTATION_NAMESPACE = uuid5(NAMESPACE_URL, "anki-alive:presentation-event:v1")


class PresentationStatus(str, Enum):
    PENDING = "PENDING"
    SHOWN = "SHOWN"
    DISMISSED = "DISMISSED"
    DEFERRED = "DEFERRED"
    SUPPRESSED = "SUPPRESSED"
    INVALIDATED = "INVALIDATED"


@dataclass(frozen=True)
class StoredPresentationEvent:
    presentation_event_id: UUID
    profile_key: str
    event: PresentationEvent
    created_at: datetime
    status: PresentationStatus
    resolved_at: datetime | None = None


class PresentationRepository:
    """Durable presentation state kept separate from domain lifecycle truth."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def enqueue(
        self,
        *,
        profile_key: str,
        event: PresentationEvent,
        created_at: datetime,
    ) -> bool:
        if not profile_key:
            raise ValueError("profile_key must not be empty")
        if not event.dedupe_key:
            raise ValueError("durable presentation event requires dedupe_key")
        if created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")

        event_id = uuid5(_PRESENTATION_NAMESPACE, event.dedupe_key)
        payload_json = json.dumps(event.payload, separators=(",", ":"), sort_keys=True)
        with self.database.transaction() as connection:
            existing = connection.execute(
                "SELECT status FROM presentation_events WHERE dedupe_key = ?",
                (event.dedupe_key,),
            ).fetchone()
            connection.execute(
                """
                INSERT INTO presentation_events(
                    presentation_event_id, profile_key, kind, prominence, priority,
                    created_at, status, dedupe_key, payload_json, resolved_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'PENDING', ?, ?, NULL)
                ON CONFLICT(dedupe_key) DO UPDATE SET
                    profile_key = excluded.profile_key,
                    kind = excluded.kind,
                    prominence = excluded.prominence,
                    priority = excluded.priority,
                    created_at = excluded.created_at,
                    status = 'PENDING',
                    payload_json = excluded.payload_json,
                    resolved_at = NULL
                """,
                (
                    str(event_id),
                    profile_key,
                    event.kind,
                    int(event.prominence),
                    event.priority,
                    created_at.isoformat(),
                    event.dedupe_key,
                    payload_json,
                ),
            )
        return existing is None or str(existing[0]) != PresentationStatus.PENDING.value

    def pending_for_profile(
        self,
        profile_key: str,
        *,
        kind: str | None = None,
    ) -> StoredPresentationEvent | None:
        if kind is None:
            row = self.database.connection.execute(
                """
                SELECT presentation_event_id, profile_key, kind, prominence, priority,
                       created_at, status, dedupe_key, payload_json, resolved_at
                FROM presentation_events
                WHERE profile_key = ? AND status = 'PENDING'
                ORDER BY created_at DESC LIMIT 1
                """,
                (profile_key,),
            ).fetchone()
        else:
            row = self.database.connection.execute(
                """
                SELECT presentation_event_id, profile_key, kind, prominence, priority,
                       created_at, status, dedupe_key, payload_json, resolved_at
                FROM presentation_events
                WHERE profile_key = ? AND kind = ? AND status = 'PENDING'
                ORDER BY created_at DESC LIMIT 1
                """,
                (profile_key, kind),
            ).fetchone()
        return self._from_row(row) if row else None

    def mark_shown(self, dedupe_key: str, *, at: datetime) -> bool:
        return self._resolve(dedupe_key, PresentationStatus.SHOWN, at)

    def dismiss(self, dedupe_key: str, *, at: datetime) -> bool:
        return self._resolve(dedupe_key, PresentationStatus.DISMISSED, at)

    def suppress(self, dedupe_key: str, *, at: datetime) -> bool:
        return self._resolve(dedupe_key, PresentationStatus.SUPPRESSED, at)

    def invalidate(self, dedupe_key: str, *, at: datetime) -> bool:
        return self._resolve(dedupe_key, PresentationStatus.INVALIDATED, at)

    def _resolve(
        self,
        dedupe_key: str,
        status: PresentationStatus,
        at: datetime,
    ) -> bool:
        if at.tzinfo is None:
            raise ValueError("resolution timestamp must be timezone-aware")
        with self.database.transaction() as connection:
            cursor = connection.execute(
                """
                UPDATE presentation_events
                SET status = ?, resolved_at = ?
                WHERE dedupe_key = ? AND status = 'PENDING'
                """,
                (status.value, at.isoformat(), dedupe_key),
            )
        return cursor.rowcount > 0

    @staticmethod
    def _from_row(row: Any) -> StoredPresentationEvent:
        event = PresentationEvent(
            kind=str(row[2]),
            prominence=PresentationProminence(int(row[3])),
            priority=int(row[4]),
            dedupe_key=str(row[7]),
            payload=json.loads(row[8]),
        )
        return StoredPresentationEvent(
            presentation_event_id=UUID(row[0]),
            profile_key=str(row[1]),
            event=event,
            created_at=datetime.fromisoformat(row[5]),
            status=PresentationStatus(str(row[6])),
            resolved_at=datetime.fromisoformat(row[9]) if row[9] else None,
        )

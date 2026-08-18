from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from typing import Any, Mapping

_FORBIDDEN_FIELD_NAMES = {
    "answer",
    "back",
    "card_content",
    "content",
    "fields",
    "front",
    "html",
    "note_content",
    "question",
    "text",
}
_MAX_STRING_LENGTH = 240


@dataclass(frozen=True)
class DiagnosticRecord:
    event: str
    level: str
    fields: dict[str, Any]


class DiagnosticsService:
    """Small structured diagnostics boundary with conservative redaction.

    Diagnostics are disabled by default. Callers should log identifiers,
    timings, counts, and state names, never card/note text. The service also
    drops common content-bearing field names as a final guardrail.
    """

    def __init__(
        self,
        *,
        enabled: bool = False,
        logger: logging.Logger | None = None,
    ) -> None:
        self.enabled = enabled
        self._logger = logger or logging.getLogger("anki_alive")

    def emit(self, event: str, *, level: str = "INFO", **fields: Any) -> DiagnosticRecord | None:
        if not self.enabled:
            return None
        if not event:
            raise ValueError("diagnostic event name must not be empty")

        record = DiagnosticRecord(
            event=event,
            level=level.upper(),
            fields=self._sanitize(fields),
        )
        numeric_level = getattr(logging, record.level, logging.INFO)
        self._logger.log(
            numeric_level,
            json.dumps(asdict(record), sort_keys=True, separators=(",", ":")),
        )
        return record

    @classmethod
    def _sanitize(cls, fields: Mapping[str, Any]) -> dict[str, Any]:
        safe: dict[str, Any] = {}
        for key, value in fields.items():
            normalized_key = str(key).lower()
            if normalized_key in _FORBIDDEN_FIELD_NAMES:
                continue
            safe[str(key)] = cls._sanitize_value(value)
        return safe

    @classmethod
    def _sanitize_value(cls, value: Any) -> Any:
        if value is None or isinstance(value, (bool, int, float)):
            return value
        if isinstance(value, str):
            if len(value) <= _MAX_STRING_LENGTH:
                return value
            return value[:_MAX_STRING_LENGTH] + "…"
        if isinstance(value, (list, tuple)):
            return [cls._sanitize_value(item) for item in value[:20]]
        if isinstance(value, Mapping):
            return cls._sanitize(value)
        return repr(value)[:_MAX_STRING_LENGTH]

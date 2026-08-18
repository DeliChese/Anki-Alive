from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FocusPolicy:
    enabled: bool = False
    allow_major_reveal: bool = True
    allow_minor_reveal: bool = True
    allow_ambient_motion: bool = True
    show_compact_progress: bool = True
    defer_nonessential_events: bool = False

    @classmethod
    def from_enabled(cls, enabled: bool) -> "FocusPolicy":
        if not enabled:
            return cls(enabled=False)
        return cls(
            enabled=True,
            allow_major_reveal=False,
            allow_minor_reveal=False,
            allow_ambient_motion=False,
            show_compact_progress=True,
            defer_nonessential_events=True,
        )

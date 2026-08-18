from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone, tzinfo
from typing import Protocol


class Clock(Protocol):
    def now_utc(self) -> datetime:
        ...


class SystemClock:
    def now_utc(self) -> datetime:
        return datetime.now(timezone.utc)


@dataclass(frozen=True)
class FixedClock:
    value: datetime

    def __post_init__(self) -> None:
        if self.value.tzinfo is None:
            raise ValueError("fixed clock value must be timezone-aware")

    def now_utc(self) -> datetime:
        return self.value.astimezone(timezone.utc)


def local_study_date(*, now_utc: datetime, local_timezone: tzinfo) -> date:
    if now_utc.tzinfo is None:
        raise ValueError("now_utc must be timezone-aware")
    return now_utc.astimezone(local_timezone).date()

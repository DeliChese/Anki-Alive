from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from time import perf_counter_ns
from typing import Callable, Iterator


@dataclass(frozen=True)
class TimingSample:
    name: str
    duration_ms: float


class PerformanceTimer:
    def __init__(self, sink: Callable[[TimingSample], None] | None = None) -> None:
        self._sink = sink

    @contextmanager
    def measure(self, name: str) -> Iterator[None]:
        started = perf_counter_ns()
        try:
            yield
        finally:
            duration_ms = (perf_counter_ns() - started) / 1_000_000
            if self._sink is not None:
                self._sink(TimingSample(name=name, duration_ms=duration_ms))

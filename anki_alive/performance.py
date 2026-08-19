from __future__ import annotations

from collections import defaultdict, deque
from contextlib import contextmanager
from dataclasses import dataclass
from math import ceil
from statistics import median
from time import perf_counter_ns
from typing import Callable, Deque, Dict, Iterator, Tuple


@dataclass(frozen=True)
class TimingSample:
    name: str
    duration_ms: float


@dataclass(frozen=True)
class TimingSummary:
    name: str
    count: int
    minimum_ms: float
    median_ms: float
    p95_ms: float
    maximum_ms: float


class PerformanceTimer:
    """Measure named runtime paths and retain a small privacy-safe sample window.

    Only numeric timing values are retained. Card text, answers, deck names and
    review content never enter this collector.
    """

    def __init__(
        self,
        sink: Callable[[TimingSample], None] | None = None,
        *,
        max_samples_per_name: int = 512,
    ) -> None:
        if max_samples_per_name <= 0:
            raise ValueError("max_samples_per_name must be positive")
        self._sink = sink
        self._max_samples_per_name = max_samples_per_name
        self._samples: Dict[str, Deque[float]] = defaultdict(
            lambda: deque(maxlen=self._max_samples_per_name)
        )

    @contextmanager
    def measure(self, name: str) -> Iterator[None]:
        started = perf_counter_ns()
        try:
            yield
        finally:
            duration_ms = (perf_counter_ns() - started) / 1_000_000
            sample = TimingSample(name=name, duration_ms=duration_ms)
            self.record(sample)

    def record(self, sample: TimingSample) -> None:
        self._samples[sample.name].append(float(sample.duration_ms))
        if self._sink is not None:
            self._sink(sample)

    def samples(self, name: str) -> Tuple[float, ...]:
        return tuple(self._samples.get(name, ()))

    def summary(self, name: str) -> TimingSummary | None:
        values = sorted(self.samples(name))
        if not values:
            return None
        p95_index = max(0, min(len(values) - 1, ceil(len(values) * 0.95) - 1))
        return TimingSummary(
            name=name,
            count=len(values),
            minimum_ms=values[0],
            median_ms=float(median(values)),
            p95_ms=values[p95_index],
            maximum_ms=values[-1],
        )

    def report(self, names: Tuple[str, ...] | None = None) -> str:
        selected = names if names is not None else tuple(sorted(self._samples))
        lines = ["Anki Alive performance snapshot"]
        if not selected:
            lines.append("No timing samples recorded yet.")
            return "\n".join(lines)

        for name in selected:
            summary = self.summary(name)
            lines.append("")
            lines.append(f"{name}:")
            if summary is None:
                lines.append("  samples: 0")
                continue
            lines.extend(
                (
                    f"  samples: {summary.count}",
                    f"  min: {summary.minimum_ms:.3f} ms",
                    f"  median/P50: {summary.median_ms:.3f} ms",
                    f"  P95: {summary.p95_ms:.3f} ms",
                    f"  max: {summary.maximum_ms:.3f} ms",
                )
            )
        return "\n".join(lines)

from pathlib import Path

from anki_alive.performance import PerformanceTimer, TimingSample


def test_performance_timer_retains_privacy_safe_window_and_reports_percentiles() -> None:
    timer = PerformanceTimer(max_samples_per_name=4)
    for value in (1.0, 2.0, 3.0, 4.0, 5.0):
        timer.record(TimingSample(name="reviewer_did_answer_card", duration_ms=value))

    assert timer.samples("reviewer_did_answer_card") == (2.0, 3.0, 4.0, 5.0)
    summary = timer.summary("reviewer_did_answer_card")
    assert summary is not None
    assert summary.count == 4
    assert summary.minimum_ms == 2.0
    assert summary.median_ms == 3.5
    assert summary.p95_ms == 5.0
    assert summary.maximum_ms == 5.0

    report = timer.report(("reviewer_did_answer_card", "state_did_undo"))
    assert "samples: 4" in report
    assert "median/P50: 3.500 ms" in report
    assert "P95: 5.000 ms" in report
    assert "state_did_undo:" in report
    assert "samples: 0" in report


def test_phase1_exposes_copyable_performance_snapshot_from_tools() -> None:
    root = Path(__file__).parents[1]
    bootstrap_source = (root / "anki_alive" / "bootstrap.py").read_text(
        encoding="utf-8"
    )

    assert 'QAction("Anki Alive Performance Snapshot", mw)' in bootstrap_source
    assert '"reviewer_did_answer_card", "state_did_undo"' in bootstrap_source
    assert 'title="Anki Alive Performance Snapshot"' in bootstrap_source
    assert "copyBtn=True" in bootstrap_source

from datetime import datetime, timedelta, timezone

from anki_alive.integration.memory import AnkiMemoryEngine, fsrs_retrievability


class FakeMemoryState:
    def __init__(self, *, stability: float, difficulty: float) -> None:
        self.stability = stability
        self.difficulty = difficulty


class FakeCard:
    def __init__(self, now: datetime) -> None:
        self.memory_state = FakeMemoryState(stability=10.0, difficulty=6.0)
        self.last_review_time = int((now - timedelta(days=10)).timestamp())
        self.decay = 0.5
        self.ivl = 10
        self.lapses = 2
        self.reps = 8


class FakeDb:
    def list(self, query: str, card_id: int, limit: int):
        assert "revlog" in query
        assert card_id == 42
        assert limit == 5
        return [3, 1, 4]


class FakeCollection:
    def __init__(self, card: FakeCard) -> None:
        self.card = card
        self.db = FakeDb()

    def get_card(self, card_id: int):
        assert card_id == 42
        return self.card


def test_fsrs_retrievability_is_ninety_percent_at_stability() -> None:
    for decay in (0.5, 0.1542):
        value = fsrs_retrievability(
            stability=12.0,
            elapsed_days=12.0,
            decay=decay,
        )
        assert abs(value - 0.9) < 1e-9


def test_anki_memory_engine_normalizes_live_card_facts() -> None:
    now = datetime(2026, 8, 19, 10, 0, tzinfo=timezone.utc)
    engine = AnkiMemoryEngine(
        FakeCollection(FakeCard(now)),
        now_utc=lambda: now,
    )

    snapshot = engine.snapshot_for_card(42)

    assert snapshot is not None
    assert snapshot.card_id == 42
    assert snapshot.stability == 10.0
    assert snapshot.difficulty == 6.0
    assert snapshot.retrievability is not None
    assert abs(snapshot.retrievability - 0.9) < 1e-9
    assert snapshot.interval_days == 10
    assert snapshot.lapses == 2
    assert snapshot.review_count == 8
    assert snapshot.recent_outcomes == (3, 1, 4)


def test_memory_engine_degrades_without_fsrs_state() -> None:
    now = datetime(2026, 8, 19, 10, 0, tzinfo=timezone.utc)
    card = FakeCard(now)
    card.memory_state = None
    engine = AnkiMemoryEngine(FakeCollection(card), now_utc=lambda: now)

    snapshot = engine.snapshot_for_card(42)

    assert snapshot is not None
    assert snapshot.stability is None
    assert snapshot.difficulty is None
    assert snapshot.retrievability is None
    assert snapshot.review_count == 8

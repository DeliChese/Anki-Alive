from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from uuid import UUID

from anki_alive.core.events import EventBus
from anki_alive.core.presentation import (
    EventOrchestrator,
    PresentationEvent,
    PresentationProminence,
)
from anki_alive.core.review import ReviewObservation, ReviewReversed, new_observation
from anki_alive.core.time import FixedClock
from anki_alive.expedition import ExpeditionRepository, ExpeditionService, ExpeditionStatus
from anki_alive.integration.expedition_ui import ExpeditionUiRuntime
from anki_alive.presentation import PresentationRepository
from anki_alive.settings import SettingsService
from anki_alive.storage import Database


class SequenceIds:
    def __init__(self) -> None:
        self._next = 1

    def new(self) -> UUID:
        value = UUID(int=self._next)
        self._next += 1
        return value


class FakeDiagnostics:
    def __init__(self) -> None:
        self.records: list[tuple[str, dict]] = []

    def emit(self, name: str, **fields):
        self.records.append((name, fields))
        return None


class FakeWeb:
    def __init__(self) -> None:
        self.evals: list[str] = []

    def eval(self, script: str) -> None:
        self.evals.append(script)


class FakeCollection:
    def __init__(self, due: int) -> None:
        self.sched = SimpleNamespace(counts=lambda: (due, 0, 0))
        self.decks = SimpleNamespace(current=lambda: {"name": "Biology"})
        self.timebox_starts = 0

    def startTimebox(self) -> None:
        self.timebox_starts += 1


class FakeMw:
    def __init__(self, profile_folder: str, due: int) -> None:
        self.pm = SimpleNamespace(profileFolder=lambda: profile_folder)
        self.col = FakeCollection(due)
        self.web = FakeWeb()
        self.reviewer = SimpleNamespace(card=object())
        self.state = "deckBrowser"
        self.transitions: list[str] = []

    def moveToState(self, state: str) -> None:
        self.state = state
        self.transitions.append(state)


class FakeReviewer:
    pass


class FakeWebContent:
    def __init__(self) -> None:
        self.body = "<main>Anki</main>"
        self.css: list[str] = []
        self.js: list[str] = []


class FakeTodaySurface:
    def __init__(self) -> None:
        self.handler = None
        self.html = ""
        self.is_open = False
        self.show_count = 0
        self.refresh_count = 0
        self.close_count = 0

    def set_command_handler(self, handler) -> None:
        self.handler = handler

    def show(self, html: str) -> None:
        self.html = html
        self.is_open = True
        self.show_count += 1

    def refresh(self, html: str) -> None:
        if self.is_open:
            self.html = html
            self.refresh_count += 1

    def close(self) -> None:
        self.is_open = False
        self.close_count += 1

    def command(self, message: str) -> None:
        assert self.handler is not None
        self.handler(message)


class FakeToolbar:
    def __init__(self) -> None:
        self.handlers: dict[str, object] = {}

    def create_link(self, cmd, label, func, tip=None, id=None):
        self.handlers[cmd] = func
        return f'<a id="{id}" title="{tip}">{label}</a>'


def make_runtime(tmp_path: Path, due: int = 2):
    database = Database(tmp_path / "anki_alive.sqlite3")
    database.open()
    bus = EventBus()
    service = ExpeditionService(
        repository=ExpeditionRepository(database),
        event_bus=bus,
        clock=FixedClock(datetime(2026, 8, 18, 12, 0, tzinfo=timezone.utc)),
        ids=SequenceIds(),
        local_timezone=timezone.utc,
    )
    bus.subscribe(ReviewObservation, service.on_review_observation)
    bus.subscribe(ReviewReversed, service.on_review_reversed)

    presentations = PresentationRepository(database)
    settings = SettingsService(load_raw=lambda: None, save_raw=lambda _value: None)
    hooks = SimpleNamespace(
        webview_will_set_content=[],
        top_toolbar_did_init_links=[],
        reviewer_will_end=[],
    )
    mw = FakeMw(str(tmp_path / "profile"), due)
    today = FakeTodaySurface()
    scheduled: list = []
    ui = ExpeditionUiRuntime(
        mw=mw,
        gui_hooks=hooks,
        event_bus=bus,
        expedition=service,
        presentations=presentations,
        settings=settings,
        diagnostics=FakeDiagnostics(),
        reviewer_type=FakeReviewer,
        today_surface=today,
        asset_base="/_addons/anki_alive_dev/anki_alive/ui",
        schedule=scheduled.append,
    )
    ui.register()

    def flush() -> None:
        while scheduled:
            scheduled.pop(0)()

    return database, bus, service, presentations, settings, hooks, mw, today, flush


def test_orchestrator_prefers_completion_and_deduplicates() -> None:
    orchestrator = EventOrchestrator()
    checkpoint = PresentationEvent(
        kind="expedition.checkpoint",
        prominence=PresentationProminence.MAJOR,
        priority=50,
        dedupe_key="checkpoint:1",
    )
    completion = PresentationEvent(
        kind="expedition.completion",
        prominence=PresentationProminence.SESSION_CLOSURE,
        priority=100,
        dedupe_key="completion:1",
    )

    assert orchestrator.enqueue(checkpoint) is True
    assert orchestrator.enqueue(checkpoint) is False
    assert orchestrator.enqueue(completion) is True
    assert [event.kind for event in orchestrator.take_boundary()] == [
        "expedition.completion"
    ]


def test_target_planning_is_bounded() -> None:
    assert ExpeditionService.target_for_available_reviews(8) == 8
    assert ExpeditionService.target_for_available_reviews(200) == 50


def test_completion_presentation_survives_database_reopen(tmp_path: Path) -> None:
    path = tmp_path / "anki_alive.sqlite3"
    database = Database(path)
    database.open()
    repository = PresentationRepository(database)
    event = PresentationEvent(
        kind="expedition.completion",
        prominence=PresentationProminence.SESSION_CLOSURE,
        priority=100,
        dedupe_key="completion:00000000-0000-0000-0000-000000000001",
        payload={"expedition_id": "00000000-0000-0000-0000-000000000001"},
    )
    repository.enqueue(
        profile_key="profile-a",
        event=event,
        created_at=datetime(2026, 8, 18, 12, 0, tzinfo=timezone.utc),
    )
    database.close()

    reopened = Database(path)
    reopened.open()
    pending = PresentationRepository(reopened).pending_for_profile(
        "profile-a",
        kind="expedition.completion",
    )
    assert pending is not None
    assert pending.event.dedupe_key == event.dedupe_key
    reopened.close()


def test_today_is_dedicated_and_reviewer_flow_stays_intact(tmp_path: Path) -> None:
    (
        database,
        bus,
        service,
        presentations,
        settings,
        hooks,
        mw,
        today,
        flush,
    ) = make_runtime(tmp_path, due=2)

    host_surface = FakeWebContent()
    hooks.webview_will_set_content[0](host_surface, object())
    assert host_surface.body == "<main>Anki</main>"
    assert host_surface.css == []
    assert host_surface.js == []

    toolbar = FakeToolbar()
    links: list[str] = []
    hooks.top_toolbar_did_init_links[0](links, toolbar)
    assert "anki-alive-today-link" in links[0]
    toolbar.handlers["anki-alive-today"]()

    assert today.is_open is True
    assert 'id="anki-alive-today"' in today.html
    assert "Memory core" in today.html
    assert ">2</span>" in today.html
    assert "reviews due" in today.html
    assert "Begin Expedition" in today.html
    assert "No additional signals right now." in today.html
    assert "Oracle" not in today.html
    assert "Rescue" not in today.html

    today.command("anki-alive:expedition:begin")
    assert today.is_open is False
    assert mw.state == "review"

    row = database.connection.execute(
        "SELECT profile_key, expedition_id FROM expeditions LIMIT 1"
    ).fetchone()
    profile_key = row[0]
    expedition_id = UUID(row[1])
    active = service.get(expedition_id)
    assert active is not None
    assert active.status is ExpeditionStatus.ACTIVE
    assert active.target_reviews == 2

    reviewer = FakeWebContent()
    hooks.webview_will_set_content[0](reviewer, FakeReviewer())
    assert 'id="anki-alive-review-strip"' in reviewer.body

    for index, rating in enumerate((1, 4), start=1):
        bus.publish(
            new_observation(
                profile_key=profile_key,
                card_id=index,
                rating=rating,
                source_review_id=100 + index,
                reviewed_at_utc=datetime(
                    2026, 8, 18, 12, index, tzinfo=timezone.utc
                ),
            )
        )
    flush()

    completed = service.get(expedition_id)
    assert completed is not None
    assert completed.status is ExpeditionStatus.COMPLETED
    assert mw.state == "deckBrowser"
    assert any("setProgress" in script for script in mw.web.evals)
    assert not any("showCheckpoint" in script for script in mw.web.evals)
    assert presentations.pending_for_profile(
        profile_key,
        kind="expedition.completion",
    ) is not None
    assert today.is_open is True
    assert "EXPEDITION COMPLETE" in today.html
    assert "Continue reviewing" in today.html

    today.command("anki-alive:expedition:done")
    assert presentations.pending_for_profile(
        profile_key,
        kind="expedition.completion",
    ) is None

    today.command("anki-alive:focus:toggle")
    assert settings.snapshot.focus_mode_enabled is True
    database.close()


def test_undo_after_completion_invalidates_stale_summary(tmp_path: Path) -> None:
    database, bus, service, presentations, _settings, _hooks, _mw, today, flush = (
        make_runtime(tmp_path, due=1)
    )
    today.command("anki-alive:expedition:begin")
    row = database.connection.execute(
        "SELECT profile_key, expedition_id FROM expeditions LIMIT 1"
    ).fetchone()
    profile_key = row[0]
    expedition_id = UUID(row[1])
    observation = new_observation(
        profile_key=profile_key,
        card_id=1,
        rating=1,
        source_review_id=101,
        reviewed_at_utc=datetime(2026, 8, 18, 12, 1, tzinfo=timezone.utc),
    )
    bus.publish(observation)
    flush()
    assert presentations.pending_for_profile(
        profile_key,
        kind="expedition.completion",
    ) is not None

    bus.publish(
        ReviewReversed(
            profile_key=profile_key,
            card_id=1,
            observation_id=observation.observation_id,
            source_review_id=101,
            reversed_at_utc=datetime(2026, 8, 18, 12, 2, tzinfo=timezone.utc),
        )
    )

    reopened = service.get(expedition_id)
    assert reopened is not None
    assert reopened.status is ExpeditionStatus.ACTIVE
    assert presentations.pending_for_profile(
        profile_key,
        kind="expedition.completion",
    ) is None
    database.close()


def test_leaving_reviewer_with_card_pauses_active_expedition(tmp_path: Path) -> None:
    database, _bus, service, _presentations, _settings, hooks, mw, today, _flush = (
        make_runtime(tmp_path, due=5)
    )
    today.command("anki-alive:expedition:begin")
    row = database.connection.execute(
        "SELECT expedition_id FROM expeditions LIMIT 1"
    ).fetchone()
    expedition_id = UUID(row[0])
    assert mw.reviewer.card is not None

    hooks.reviewer_will_end[0]()

    paused = service.get(expedition_id)
    assert paused is not None
    assert paused.status is ExpeditionStatus.PAUSED
    database.close()


def test_natural_queue_exhaustion_closes_without_moving_target(tmp_path: Path) -> None:
    (
        database,
        _bus,
        service,
        presentations,
        _settings,
        hooks,
        mw,
        today,
        flush,
    ) = make_runtime(tmp_path, due=5)
    today.command("anki-alive:expedition:begin")
    row = database.connection.execute(
        "SELECT profile_key, expedition_id FROM expeditions LIMIT 1"
    ).fetchone()
    profile_key = row[0]
    expedition_id = UUID(row[1])

    mw.reviewer.card = None
    hooks.reviewer_will_end[0]()
    mw.state = "overview"
    flush()

    closed = service.get(expedition_id)
    assert closed is not None
    assert closed.status is ExpeditionStatus.COMPLETED
    assert closed.completed_reviews == 0
    assert closed.target_reviews == 5
    assert mw.state == "deckBrowser"
    assert presentations.pending_for_profile(
        profile_key,
        kind="expedition.completion",
    ) is not None
    assert today.is_open is True
    assert "The available route is complete." in today.html
    assert "planned target stayed 5" in today.html
    assert "no eligible reviews left" in today.html
    database.close()


def test_ui_assets_keep_reviewer_quiet_and_today_isolated() -> None:
    root = Path(__file__).parents[1]
    css = (root / "anki_alive" / "ui" / "expedition.css").read_text(encoding="utf-8")
    js = (root / "anki_alive" / "ui" / "expedition.js").read_text(encoding="utf-8")
    today_css = (root / "anki_alive" / "ui" / "today.css").read_text(encoding="utf-8")

    assert "aa-review-strip" in css
    assert "pointer-events: none" in css
    assert "prefers-reduced-motion" in css
    assert "filter: blur" not in css
    assert "text-shadow" not in css
    assert "infinite" not in css
    assert "requestAnimationFrame" not in js
    assert "setInterval" not in js
    assert ".aa-today-window" in today_css
    assert "var(--aa-bg-canvas)" in today_css

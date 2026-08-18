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


class FakeScheduler:
    def counts(self):
        return (2, 0, 0)


class FakeDecks:
    def current(self):
        return {"name": "Fallback deck"}


class FakeCollection:
    def __init__(self) -> None:
        self.sched = FakeScheduler()
        self.decks = FakeDecks()
        self.timebox_starts = 0

    def startTimebox(self) -> None:
        self.timebox_starts += 1


class FakeMw: 
    def __init__(self, profile_folder: str) -> None:
        self.pm = SimpleNamespace(profileFolder=lambda: profile_folder)
        self.col = FakeCollection()
        self.web = FakeWeb()
        self.state = "deckBrowser"
        self.transitions: list[str] = []

    def moveToState(self, state: str) -> None:
        self.state = state
        self.transitions.append(state)


class FakeDeckBrowser:
    def __init__(self, *, due: int = 2) -> None:
        node = SimpleNamespace(
            deck_id=1,
            name="Biology",
            new_count=due,
            learn_count=0,
            review_count=0,
            children=[],
        )
        self._render_data = SimpleNamespace(
            tree=node,
            current_deck_id=1,
        )
        self.refresh_count = 0

    def refresh(self) -> None:
        self.refresh_count += 1


class FakeReviewer:
    pass


class FakeWeb Content:
    def __init__(self, body: str = "<main>Anki</main>") -> None:
        self.body = body
        self.css: list[str] = []
        self.js: list[str] = []


def make_ui_runtime(tmp_path: Path, *, due: int = 2):
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

    saved: list[dict] = []
    settings = SettingsService(
        load_raw=lambda: None,
        save_raw=saved.append,
    )
    hooks = SimpleNamespace(
        webview_will_set_content=[],
        webview_did_receive_js_message=[],
        reviewer_will_end=[],
    )
    mw = FakeMw(str(tmp_path / "profile"))
    diagnostics = FakeDiagnostics()
    scheduled: list = []

    ui = ExpeditionUiRuntime(
        mw=mw,
        gui_hooks=hooks,
        event_bus=bus,
        expedition=service,
        settings=settings,
        diagnostics=diagnostics,
        deck_browser_type=FakeDeckBrowser,
        reviewer_type=FakeReviewer,
        asset_base="/_addons/anki_alive_dev/anki_alive/ui",
        schedule=scheduled.append,
    )
    ui.register()

    def run_scheduled() -> None:
        while scheduled:
            callback = scheduled.pop(0)
            callback()

    return (
        database,
        bus,
        service,
        settings,
        hooks,
        mw,
        diagnostics,
        FakeDeckBrowser(due=due),
        run_scheduled,
    )


def test_event_orchestrator_allows_only_one_prominent_boundary_event() -> None:
    orchestrator = EventOrchestrator()
    orchestrator.enqueue(
        PresentationEvent(
            kind="expedition.checkpoint",
            prominence=PresentationProminence.MAJOR,
            priority=50,
            dedupe_key="checkpoint:1",
        )
    )
    orchestrator.enqueue(
        PresentationEvent(
            kind="expedition.completion",
            prominence=PresentationProminence.SESSION_CLOSURE,
            priority=100,
            dedupe_key="completion:1",
        )
    )

    chosen = orchestrator.take_boundary()

    assert [event.kind for event in chosen] == ["expedition.completion"]
    assert orchestrator.pending_count == 0


def test_event_orchestrator_deduplicates_by_stable_key() -> None:
    orchestrator = EventOrchestrator()
    event = PresentationEvent(
        kind="expedition.checkpoint",
        prominence=PresentationProminence.MAJOR,
        dedupe_key="checkpoint:1",
    )

    assert orchestrator.enqueue(event) is True
    assert orchestrator.enqueue(event) is False
    assert orchestrator.pending_count == 1


def test_target_planning_is_bounded_and_clamped_to_available_work() -> None:
    assert ExpeditionService.target_for_available_reviews(8) == 8
    assert ExpeditionService.target_for_available_reviews(200) == 50


def test_today_and_reviewer_ui_use_real_expedition_state(tmp_path: Path) -> None:
    (
        database,
        bus,
        service,
        settings,
        hooks,
        mw,
        _diagnostics,
        deck_browser,
        run_scheduled,
    ) = make_ui_runtime(tmp_path, due=2)

    today_content = FakeWebContent()
    hooks.webview_will_set_content[0](today_content, deck_browser)

    assert 'id="anki-alive-today"' in today_content.body
    assert "Memory core" in today_content.body
    assert "2 reviews due" in today_content.body
    assert "Begin Expedition" in today_content.body
    assert "No additional signals right now." in today_content.body
    assert "Oracle" not in today_content.body
    assert "Rescue" not in today_content.body
    assert today_content.css == [
        "/_addons/anki_alive_dev/anki_alive/ui/foundation.css",
        "/_addons/anki_alive_dev/anki_alive/ui/expedition.css",
    ]
    assert today_content.js == [
        "/_addons/anki_alive_dev/anki_alive/ui/expedition.js"
    ]

    handled = hooks.webview_did_receive_js_message[0](
        (False, None),
        "anki-alive:expedition:begin",
        deck_browser,
    )
    assert handled[0] is True
    assert mw.state == "review"
    assert mw.col.timebox_starts == 1

    profile_key = database.connection.execute(
        "SELECT profile_key FROM expeditions LIMIT 1"
    ).fetchone()[0]
    active = service.resumable(profile_key)
    assert active is not None
    assert active.status is ExpeditionStatus.ACTIVE
    assert active.target_reviews == 2

    reviewer_content = FakeWebContent()
    hooks.webview_will_set_content[0](reviewer_content, FakeReviewer())
    assert 'id="anki-alive-review-strip"' in reviewer_content.body
    assert "2" in reviewer_content.body
    assert "pointer-events" not in reviewer_content.body

    for index, rating in enumerate((1, 4), start=1):
        bus.publish(
            new_observation(
                profile_key=profile_key,
                card_id=index,
                rating=rating,
                source_review_id=100 + index,
                reviewed_at_utc=datetime(
                    2026,
                    8,
                    18,
                    12,
                    index,
                    tzinfo=timezone.utc,
                ),
            )
        )

    run_scheduled()

    completed = service.get(active.expedition_id)
    assert completed is not None
    assert completed.status is ExpeditionStatus.COMPLETED
    assert mw.state == "deckBrowser"
    assert "deckBrowser" in mw.transitions
    assert any("setProgress" in script for script in mw.web.evals)
    assert not any("showCheckpoint" in script for script in mw.web.evals)

    completion_content = FakeWeb Content()
    hooks.webview_will_set_content[0](completion_content, deck_browser)
    assert "EXPEDITION COMPLETE" in completion_content.body
    assert "The route is complete." in completion_content.body
    assert "Continue reviewing" in completion_content.body

    hooks.webview_did_receive_js_message[0](
        (False, None),
        "anki-alive:expedition:done",
        deck_browser,
    )
    after_done = FakeWebContent()
    hooks.webview_will_set_content[0](after_done, deck_browser)
    assert "EXPEDITION COMPLETE" not in after_done.body

    hooks.webview_did_receive_js_message[0](
        (False, None),
        "anki-alive:focus:toggle",
        deck_browser,
    )
    assert settings.snapshot.focus_mode_enabled is True
    assert deck_browser.refresh_count >= 2

    database.close()


def test_leaving_reviewer_pauses_active_expedition(tmp_path: Path) -> None:
    (
        database,
        _bus,
        service,
        _settings,
        hooks,
        _mw,
        _diagnostics,
        deck_browser,
        _run_scheduled,
   ) = make_ui_runtime(tmp_path, due=5)

    hooks.webview_did_receive_js_message[0](
        (False, None),
        "anki-alive:expedition:begin",
        deck_browser,
    )
    row = database.connection.execute(
        "SELECT profile_key, expedition_id FROM expeditions LIMIT 1"
    ).fetchone()
    profile_key = row[0]
    expedition_id = UUID(row[1])
    assert service.resumable(profile_key).status is ExpeditionStatus.ACTIVE

    hooks.reviewer_will_end[0]()

    paused = service.get(expedition_id)
    assert paused is not None
    assert paused.status is ExpeditionStatus.PAUSED
    database.close()


def test_phase1_ui_assets_respect_canonical_review_constraints() -> None:
    root = Path(__file__).parents[1]
    css = (root / "anki_alive" / "ui" / "expedition.css").read_text(
        encoding="utf-8"
    )
    js = (root / "anki_alive" / "ui" / "expedition.js").read_text(
        encoding="utf-8"
    )

    assert "aa-review-strip" in css
    assert "pointer-events: none" in css
    assert "prefers-reduced-motion" in css
    assert "filter: blur" not in css
    assert "text-shadow" not in css
    assert "infinite" not in css
    assert "requestAnimationFrame" not in js
    assert "setInterval" not in js

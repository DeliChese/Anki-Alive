from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from anki_alive.integration.expedition_ui import ExpeditionUiRuntime


class FakeToolbar:
    def __init__(self) -> None:
        self.handlers: dict[str, object] = {}

    def create_link(self, cmd, label, func, tip=None, id=None):
        self.handlers[cmd] = func
        return f'<a id="{id}" title="{tip}">{label}</a>'


def _ui_for_toolbar_state(state: str) -> ExpeditionUiRuntime:
    ui = object.__new__(ExpeditionUiRuntime)
    ui._mw = SimpleNamespace(state=state)
    ui.show_today = lambda: None
    return ui


def test_alive_toolbar_entry_is_suppressed_during_active_review() -> None:
    ui = _ui_for_toolbar_state("review")
    toolbar = FakeToolbar()
    links: list[str] = []

    ui._on_top_toolbar_did_init_links(links, toolbar)

    assert links == []
    assert toolbar.handlers == {}


def test_alive_toolbar_entry_remains_available_outside_review() -> None:
    ui = _ui_for_toolbar_state("deckBrowser")
    toolbar = FakeToolbar()
    links: list[str] = []

    ui._on_top_toolbar_did_init_links(links, toolbar)

    assert len(links) == 1
    assert "anki-alive-today-link" in links[0]
    assert "anki-alive-today" in toolbar.handlers


def test_today_window_can_enter_responsive_breakpoint() -> None:
    root = Path(__file__).parents[1]
    window_source = (
        root / "anki_alive" / "integration" / "today_window.py"
    ).read_text(encoding="utf-8")
    today_css = (root / "anki_alive" / "ui" / "today.css").read_text(
        encoding="utf-8"
    )
    expedition_css = (root / "anki_alive" / "ui" / "expedition.css").read_text(
        encoding="utf-8"
    )

    assert "dialog.setMinimumSize(520, 420)" in window_source
    assert "@media (max-width: 760px)" in today_css
    assert "@media (max-width: 760px)" in expedition_css
    assert "grid-template-columns: 1fr" in expedition_css

from __future__ import annotations

from types import SimpleNamespace

from anki_alive.integration.expedition_ui import ExpeditionUiRuntime
from anki_alive.integration.today_window import AnkiTodayWindow


class FakeDialog:
    def __init__(self) -> None:
        self.visible = False
        self.show_count = 0
        self.hide_count = 0
        self.raise_count = 0
        self.activate_count = 0

    def isVisible(self) -> bool:
        return self.visible

    def show(self) -> None:
        self.visible = True
        self.show_count += 1

    def hide(self) -> None:
        self.visible = False
        self.hide_count += 1

    def raise_(self) -> None:
        self.raise_count += 1

    def activateWindow(self) -> None:
        self.activate_count += 1


class FakeWeb:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def evalWithCallback(self, script: str, callback) -> None:
        self.calls.append((script, callback))


class FakeTodaySurface:
    def __init__(self) -> None:
        self.close_count = 0

    def close(self) -> None:
        self.close_count += 1


class FakeDiagnostics:
    def emit(self, _name: str, **_fields) -> None:
        return None


def _prepared_today_window() -> tuple[AnkiTodayWindow, FakeDialog, FakeWeb]:
    window = object.__new__(AnkiTodayWindow)
    dialog = FakeDialog()
    web = FakeWeb()
    window._mw = None
    window._asset_base = ""
    window._command_handler = None
    window._dialog = dialog
    window._web = web
    window._document_initialized = True
    window._save_geom = None
    window._show_generation = 0
    window._want_visible = False
    return window, dialog, web


def test_today_reveals_only_after_fresh_html_reaches_dom() -> None:
    window, dialog, web = _prepared_today_window()

    window.show("<p>EXPEDITION COMPLETE</p>")

    assert dialog.show_count == 0
    assert len(web.calls) == 1
    script, callback = web.calls[0]
    assert "EXPEDITION COMPLETE" in script
    assert callback is not None

    callback(True)

    assert dialog.show_count == 1
    assert dialog.visible is True
    assert dialog.raise_count == 1
    assert dialog.activate_count == 1


def test_closing_today_invalidates_a_late_reveal_callback() -> None:
    window, dialog, web = _prepared_today_window()

    window.show("<p>fresh</p>")
    callback = web.calls[0][1]
    window.close()

    assert callback is not None
    callback(True)

    assert dialog.visible is False
    assert dialog.show_count == 0
    assert dialog.hide_count == 1


def test_done_dismisses_completion_and_closes_today_without_new_route() -> None:
    ui = object.__new__(ExpeditionUiRuntime)
    dismissed: list[bool] = []
    today = FakeTodaySurface()
    ui._dismiss_completion = lambda: dismissed.append(True)
    ui._today_surface = today
    ui._diagnostics = FakeDiagnostics()
    ui._settings = SimpleNamespace()

    ui.handle_today_command("anki-alive:expedition:done")

    assert dismissed == [True]
    assert today.close_count == 1

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class AnkiTodayWindow:
    """Dedicated, modeless host window for the Anki Alive Today surface.

    Keeping Today in its own AnkiWebView avoids taking ownership of Anki's
    Deck Browser DOM, which is a high-conflict surface for appearance and
    dashboard add-ons.
    """

    def __init__(self, *, mw: Any, asset_base: str) -> None:
        self._mw = mw
        self._asset_base = asset_base.rstrip("/")
        self._command_handler: Callable[[str], Any] | None = None
        self._dialog: Any | None = None
        self._web: Any | None = None

    def set_command_handler(self, handler: Callable[[str], Any]) -> None:
        self._command_handler = handler

    @property
    def is_open(self) -> bool:
        return self._dialog is not None and self._web is not None

    def show(self, html: str) -> None:
        if not self.is_open:
            self._create()
        self._render(html)
        assert self._dialog is not None
        self._dialog.show()
        self._dialog.raise_()
        self._dialog.activateWindow()

    def refresh(self, html: str) -> None:
        if self.is_open:
            self._render(html)

    def close(self) -> None:
        if self._dialog is not None:
            self._dialog.close()

    def _create(self) -> None:
        from aqt.qt import QDialog, Qt, QVBoxLayout, qconnect
        from aqt.utils import (
            disable_help_button,
            restoreGeom,
            saveGeom,
            setWindowIcon,
        )
        from aqt.webview import AnkiWebView, AnkiWebViewKind

        dialog = QDialog(None, Qt.WindowType.Window)
        self._mw.garbage_collect_on_dialog_finish(dialog)
        disable_help_button(dialog)
        setWindowIcon(dialog)
        dialog.setWindowTitle("Anki Alive · Today")
        dialog.setMinimumSize(760, 540)
        dialog.resize(1120, 760)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        web = AnkiWebView(parent=dialog, kind=AnkiWebViewKind.DEFAULT)
        web.set_bridge_command(self._on_bridge_command, self)
        layout.addWidget(web)

        qconnect(dialog.finished, self._on_finished)
        self._dialog = dialog
        self._web = web
        restoreGeom(dialog, "anki_alive_today_v1")

        self._save_geom = saveGeom

    def _render(self, html: str) -> None:
        assert self._web is not None
        body = f'<main class="aa-today-window">{html}</main>'
        self._web.stdHtml(
            body,
            css=[
                f"{self._asset_base}/foundation.css",
                f"{self._asset_base}/expedition.css",
                f"{self._asset_base}/today.css",
            ],
            js=[f"{self._asset_base}/expedition.js"],
            context=self,
        )
        self._web.set_bridge_command(self._on_bridge_command, self)

    def _on_bridge_command(self, command: str) -> Any:
        if command == "close":
            self.close()
            return None
        if self._command_handler is None:
            return None
        return self._command_handler(command)

    def _on_finished(self, _result: int) -> None:
        if self._dialog is not None:
            self._save_geom(self._dialog, "anki_alive_today_v1")
        if self._web is not None:
            self._web.cleanup()
        self._web = None
        self._dialog = None

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any


class AnkiTodayWindow:
    """Dedicated, reusable host window for the Anki Alive Today surface.

    Today keeps one AnkiWebView alive after its first creation. Reopening the
    surface therefore does not recreate Chromium or reload the full CSS/JS
    document. Only the inner Today markup is refreshed.
    """

    _ROOT_ID = "anki-alive-today-root"

    def __init__(self, *, mw: Any, asset_base: str) -> None:
        self._mw = mw
        self._asset_base = asset_base.rstrip("/")
        self._command_handler: Callable[[str], Any] | None = None
        self._dialog: Any | None = None
        self._web: Any | None = None
        self._document_initialized = False
        self._save_geom: Callable[..., Any] | None = None

    def set_command_handler(self, handler: Callable[[str], Any]) -> None:
        self._command_handler = handler

    @property
    def is_open(self) -> bool:
        return bool(
            self._dialog is not None
            and self._web is not None
            and self._dialog.isVisible()
        )

    @property
    def is_prepared(self) -> bool:
        return self._dialog is not None and self._web is not None

    def prepare(self) -> None:
        """Create and load the hidden Today shell without stealing focus."""

        if not self.is_prepared:
            self._create()
        self._ensure_document()

    def show(self, html: str) -> None:
        self.prepare()
        self._set_content(html)
        assert self._dialog is not None
        self._dialog.show()
        self._dialog.raise_()
        self._dialog.activateWindow()

    def refresh(self, html: str) -> None:
        if not self.is_prepared:
            return
        self._set_content(html)

    def close(self) -> None:
        """Hide Today while retaining its WebView for a fast reopen."""

        if self._dialog is not None:
            self._dialog.hide()

    def shutdown(self) -> None:
        """Release the retained WebView when the add-on runtime is torn down."""

        if self._dialog is not None and self._save_geom is not None:
            self._save_geom(self._dialog, "anki_alive_today_v1")
        if self._web is not None:
            self._web.cleanup()
        if self._dialog is not None:
            self._dialog.hide()
            self._dialog.deleteLater()
        self._web = None
        self._dialog = None
        self._document_initialized = False

    def _create(self) -> None:
        from aqt.qt import QDialog, QVBoxLayout
        from aqt.utils import (
            disable_help_button,
            restoreGeom,
            saveGeom,
            setWindowIcon,
        )
        from aqt.webview import AnkiWebView, AnkiWebViewKind

        class PersistentTodayDialog(QDialog):
            def reject(dialog_self) -> None:
                # Title-bar close and Escape hide instead of destroying the
                # expensive WebEngine surface. Runtime shutdown cleans it up.
                dialog_self.hide()

        dialog = PersistentTodayDialog(None)
        disable_help_button(dialog)
        setWindowIcon(dialog)
        dialog.setWindowTitle("Anki Alive · Today")
        dialog.setMinimumSize(520, 420)
        dialog.resize(1120, 760)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        web = AnkiWebView(parent=dialog, kind=AnkiWebViewKind.DEFAULT)
        web.set_bridge_command(self._on_bridge_command, self)
        layout.addWidget(web)

        self._dialog = dialog
        self._web = web
        self._save_geom = saveGeom
        restoreGeom(dialog, "anki_alive_today_v1")

    def _ensure_document(self) -> None:
        if self._document_initialized:
            return
        assert self._web is not None
        body = (
            '<main class="aa-today-window">'
            f'<div id="{self._ROOT_ID}" aria-live="polite"></div>'
            "</main>"
        )
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
        self._document_initialized = True

    def _set_content(self, html: str) -> None:
        self._ensure_document()
        assert self._web is not None
        safe_html = json.dumps(html, ensure_ascii=False)
        root_id = json.dumps(self._ROOT_ID)
        self._web.eval(
            "(() => {"
            f"const root = document.getElementById({root_id});"
            f"if (root) root.innerHTML = {safe_html};"
            "})();"
        )

    def _on_bridge_command(self, command: str) -> Any:
        if command == "close":
            self.close()
            return None
        if self._command_handler is None:
            return None
        return self._command_handler(command)

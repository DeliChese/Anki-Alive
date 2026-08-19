from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from anki_alive.integration.profile import load_or_create_profile_key
from anki_alive.oracle.events import OracleResolved
from anki_alive.presentation import PresentationRepository
from anki_alive.settings import SettingsService


class OracleUiRuntime:
    """Post-answer Oracle presentation adapter.

    Oracle domain truth is already resolved before this class runs. This layer
    only decides whether a durable reveal is shown or suppressed by Focus Mode.
    """

    def __init__(
        self,
        *,
        mw: Any,
        gui_hooks: Any,
        event_bus: Any,
        presentations: PresentationRepository,
        settings: SettingsService,
        diagnostics: Any,
        reviewer_type: type[Any],
        asset_base: str,
        schedule: Callable[[Callable[[], None]], None],
    ) -> None:
        self._mw = mw
        self._gui_hooks = gui_hooks
        self._event_bus = event_bus
        self._presentations = presentations
        self._settings = settings
        self._diagnostics = diagnostics
        self._reviewer_type = reviewer_type
        self._asset_base = asset_base.rstrip("/")
        self._schedule = schedule
        self._registered = False

    def register(self) -> None:
        if self._registered:
            return
        self._gui_hooks.webview_will_set_content.append(self._on_webview_will_set_content)
        self._event_bus.subscribe(OracleResolved, self._on_oracle_resolved)
        self._registered = True

    def _profile_key(self) -> str:
        return load_or_create_profile_key(self._mw.pm.profileFolder())

    def _on_webview_will_set_content(self, web_content: Any, context: object | None) -> None:
        if not isinstance(context, self._reviewer_type):
            return
        for stylesheet in (
            f"{self._asset_base}/foundation.css",
            f"{self._asset_base}/oracle.css",
        ):
            if stylesheet not in web_content.css:
                web_content.css.append(stylesheet)
        script = f"{self._asset_base}/oracle.js"
        if script not in web_content.js:
            web_content.js.append(script)

    def _on_oracle_resolved(self, event: OracleResolved) -> None:
        self._schedule(lambda: self._show_resolution(event))

    def _show_resolution(self, event: OracleResolved) -> None:
        try:
            profile_key = self._profile_key()
            stored = self._presentations.pending_for_profile(
                profile_key,
                kind="oracle_resolution",
            )
            if stored is None or stored.event.dedupe_key is None:
                return
            resolved_at = stored.created_at

            # Focus Mode changes presentation only; the resolved Oracle domain
            # record remains untouched.
            if self._settings.snapshot.focus_mode_enabled:
                self._presentations.suppress(
                    stored.event.dedupe_key,
                    at=resolved_at,
                )
                return

            # Expedition completion may move the host away from review first.
            # In that case closure wins and the Oracle reveal is suppressed as
            # stale rather than interrupting a real stopping point.
            if getattr(self._mw, "state", None) != "review":
                self._presentations.suppress(
                    stored.event.dedupe_key,
                    at=resolved_at,
                )
                return

            payload = {
                "predicted_outcome": event.predicted_outcome.value,
                "actual_recall_success": event.actual_recall_success,
                "result": event.result.value,
                "reduced_motion": self._settings.snapshot.reduced_motion,
            }
            safe_payload = json.dumps(payload, separators=(",", ":"))
            self._mw.web.eval(
                "window.AnkiAliveOracle && "
                f"window.AnkiAliveOracle.showResolution({safe_payload});"
            )
            self._presentations.mark_shown(
                stored.event.dedupe_key,
                at=resolved_at,
            )
        except Exception as error:
            self._diagnostics.emit(
                "oracle_reveal_error",
                error_type=type(error).__name__,
            )

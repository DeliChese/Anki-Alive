from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any
from uuid import UUID

from anki_alive.core.events import EventBus
from anki_alive.core.presentation import (
    EventOrchestrator,
    PresentationEvent,
    PresentationProminence,
)
from anki_alive.expedition.events import (
    CheckpointReached,
    ExpeditionCompleted,
    ExpeditionProgressed,
    ExpeditionReopened,
)
from anki_alive.expedition.model import Expedition, ExpeditionStatus
from anki_alive.expedition.service import ExpeditionService
from anki_alive.expedition.viewmodel import build_expedition_view
from anki_alive.integration.profile import load_or_create_profile_key
from anki_alive.presentation import PresentationRepository
from anki_alive.settings import SettingsService
from anki_alive.ui.expedition import render_review_strip, render_today


class ExpeditionUiRuntime:
    """Thin Anki UI adapter for Phase 1 Expedition presentation.

    Today deliberately lives outside Anki's Deck Browser DOM. The Deck Browser
    is a shared host surface frequently customized by other add-ons, so Anki
    Alive only adds a toolbar entry point and keeps its full Today experience in
    a dedicated window. Reviewer presentation remains a restrained WebView
    augmentation.
    """

    def __init__(
        self,
        *,
        mw: Any,
        gui_hooks: Any,
        event_bus: EventBus,
        expedition: ExpeditionService,
        presentations: PresentationRepository,
        settings: SettingsService,
        diagnostics: Any,
        reviewer_type: type[Any],
        today_surface: Any,
        asset_base: str,
        schedule: Callable[[Callable[[], None]], None],
    ) -> None:
        self._mw = mw
        self._gui_hooks = gui_hooks
        self._event_bus = event_bus
        self._expedition = expedition
        self._presentations = presentations
        self._settings = settings
        self._diagnostics = diagnostics
        self._reviewer_type = reviewer_type
        self._today_surface = today_surface
        self._asset_base = asset_base.rstrip("/")
        self._schedule = schedule
        self._orchestrator = EventOrchestrator()
        self._flush_scheduled = False
        self._registered = False

    def register(self) -> None:
        if self._registered:
            return
        self._gui_hooks.webview_will_set_content.append(
            self._on_webview_will_set_content
        )
        self._gui_hooks.top_toolbar_did_init_links.append(
            self._on_top_toolbar_did_init_links
        )
        self._gui_hooks.reviewer_will_end.append(self._on_reviewer_will_end)

        self._event_bus.subscribe(
            ExpeditionProgressed,
            self._on_expedition_progressed,
        )
        self._event_bus.subscribe(
            CheckpointReached,
            self._on_checkpoint_reached,
        )
        self._event_bus.subscribe(
            ExpeditionCompleted,
            self._on_expedition_completed,
        )
        self._event_bus.subscribe(
            ExpeditionReopened,
            self._on_expedition_reopened,
        )
        self._today_surface.set_command_handler(self.handle_today_command)
        self._registered = True

    def _profile_key(self) -> str:
        return load_or_create_profile_key(self._mw.pm.profileFolder())

    def _now(self):
        return self._expedition.clock.now_utc()

    def _ensure_reviewer_assets(self, web_content: Any) -> None:
        for stylesheet in (
            f"{self._asset_base}/foundation.css",
            f"{self._asset_base}/expedition.css",
        ):
            if stylesheet not in web_content.css:
                web_content.css.append(stylesheet)
        script = f"{self._asset_base}/expedition.js"
        if script not in web_content.js:
            web_content.js.append(script)

    def _on_webview_will_set_content(
        self,
        web_content: Any,
        context: object | None,
    ) -> None:
        try:
            if not isinstance(context, self._reviewer_type):
                return
            profile_key = self._profile_key()
            expedition = self._expedition.resumable(profile_key)
            if expedition is None or expedition.status is not ExpeditionStatus.ACTIVE:
                return
            self._ensure_reviewer_assets(web_content)
            snapshot = self._settings.snapshot
            web_content.body += render_review_strip(
                expedition,
                self._expedition.checkpoints(expedition.expedition_id),
                focus_mode=snapshot.focus_mode_enabled,
                reduced_motion=snapshot.reduced_motion,
            )
        except Exception as error:
            self._diagnostics.emit(
                "expedition_ui_render_error",
                error_type=type(error).__name__,
            )

    def _on_top_toolbar_did_init_links(self, links: list[str], toolbar: Any) -> None:
        if getattr(self._mw, "state", None) == "review":
            return
        links.append(
            toolbar.create_link(
                "anki-alive-today",
                "Alive",
                self.show_today,
                tip="Open Anki Alive Today",
                id="anki-alive-today-link",
            )
        )

    def show_today(self) -> None:
        try:
            self._today_surface.show(self._render_today_html())
        except Exception as error:
            self._diagnostics.emit(
                "expedition_today_open_error",
                error_type=type(error).__name__,
            )

    def _refresh_today(self) -> None:
        try:
            self._today_surface.refresh(self._render_today_html())
        except Exception as error:
            self._diagnostics.emit(
                "expedition_today_refresh_error",
                error_type=type(error).__name__,
            )

    def _render_today_html(self) -> str:
        context_name, due_reviews = self._study_context()
        profile_key = self._profile_key()
        resumable = self._expedition.resumable(profile_key)
        completion = self._completion_for_profile(profile_key)
        completion_checkpoints = (
            self._expedition.checkpoints(completion.expedition_id)
            if completion is not None
            else ()
        )
        proposed_target = None
        if resumable is None and completion is None and due_reviews > 0:
            proposed_target = self._expedition.target_for_available_reviews(due_reviews)
        checkpoints = (
            self._expedition.checkpoints(resumable.expedition_id)
            if resumable is not None
            else ()
        )
        snapshot = self._settings.snapshot
        return render_today(
            study_date=self._expedition.study_date(),
            context_name=context_name,
            due_reviews=due_reviews,
            proposed_target=proposed_target,
            expedition=resumable,
            checkpoints=checkpoints,
            completed_summary=completion,
            completed_checkpoints=completion_checkpoints,
            focus_mode=snapshot.focus_mode_enabled,
            reduced_motion=snapshot.reduced_motion,
        )

    def handle_today_command(self, message: str) -> None:
        if not message.startswith("anki-alive:"):
            return
        try:
            if message == "anki-alive:expedition:begin":
                self._begin_expedition()
            elif message == "anki-alive:expedition:resume":
                self._resume_expedition()
                self._start_review()
            elif message == "anki-alive:expedition:end":
                self._end_expedition()
                self._refresh_today()
            elif message == "anki-alive:expedition:done":
                self._dismiss_completion()
                self._today_surface.close()
            elif message == "anki-alive:expedition:continue":
                self._dismiss_completion()
                _, due_reviews = self._study_context()
                if due_reviews > 0:
                    self._start_review()
                else:
                    self._refresh_today()
            elif message == "anki-alive:focus:toggle":
                current = self._settings.snapshot.focus_mode_enabled
                self._settings.set_focus_mode(not current)
                self._refresh_today()
        except Exception as error:
            self._diagnostics.emit(
                "expedition_ui_command_error",
                command=message,
                error_type=type(error).__name__,
            )

    def _begin_expedition(self) -> None:
        profile_key = self._profile_key()
        existing = self._expedition.resumable(profile_key)
        if existing is not None:
            self._activate(existing)
            self._start_review()
            return

        _, due_reviews = self._study_context()
        if due_reviews <= 0:
            self._refresh_today()
            return
        expedition = self._expedition.plan_for_available_reviews(
            profile_key=profile_key,
            available_reviews=due_reviews,
        )
        self._expedition.start(expedition.expedition_id)
        self._start_review()

    def _resume_expedition(self) -> None:
        expedition = self._expedition.resumable(self._profile_key())
        if expedition is None:
            return
        self._activate(expedition)

    def _activate(self, expedition: Expedition) -> None:
        if expedition.status is ExpeditionStatus.PLANNED:
            self._expedition.start(expedition.expedition_id)
        elif expedition.status is ExpeditionStatus.PAUSED:
            self._expedition.resume(expedition.expedition_id)

    def _end_expedition(self) -> None:
        expedition = self._expedition.resumable(self._profile_key())
        if expedition is None:
            return
        if expedition.status in {
            ExpeditionStatus.PLANNED,
            ExpeditionStatus.ACTIVE,
            ExpeditionStatus.PAUSED,
        }:
            self._expedition.end(expedition.expedition_id)

    def _completion_event(self, expedition_id: UUID) -> PresentationEvent:
        return PresentationEvent(
            kind="expedition.completion",
            prominence=PresentationProminence.SESSION_CLOSURE,
            priority=100,
            dedupe_key=f"completion:{expedition_id}",
            payload={"expedition_id": str(expedition_id)},
        )

    def _dismiss_completion(self) -> None:
        profile_key = self._profile_key()
        stored = self._presentations.pending_for_profile(
            profile_key,
            kind="expedition.completion",
        )
        if stored is None or stored.event.dedupe_key is None:
            return
        self._presentations.dismiss(stored.event.dedupe_key, at=self._now())

    def _completion_for_profile(self, profile_key: str) -> Expedition | None:
        stored = self._presentations.pending_for_profile(
            profile_key,
            kind="expedition.completion",
        )
        if stored is None:
            return None
        expedition_id_value = stored.event.payload.get("expedition_id")
        if not expedition_id_value:
            self._presentations.invalidate(
                stored.event.dedupe_key or "",
                at=self._now(),
            )
            return None
        expedition = self._expedition.get(UUID(str(expedition_id_value)))
        if expedition is None or expedition.status is not ExpeditionStatus.COMPLETED:
            if stored.event.dedupe_key:
                self._presentations.invalidate(stored.event.dedupe_key, at=self._now())
            return None
        return expedition

    def _start_review(self) -> None:
        self._today_surface.close()
        self._mw.col.startTimebox()
        self._mw.moveToState("review")

    def _study_context(self) -> tuple[str, int]:
        counts = tuple(int(value) for value in self._mw.col.sched.counts())
        due = sum(max(0, value) for value in counts[:3])
        deck = self._mw.col.decks.current()
        return str(deck.get("name", "Current deck")), due

    def _on_reviewer_will_end(self) -> None:
        try:
            expedition = self._expedition.resumable(self._profile_key())
            if expedition is None or expedition.status is not ExpeditionStatus.ACTIVE:
                return

            reviewer = getattr(self._mw, "reviewer", None)
            missing_card = object()
            current_card = getattr(reviewer, "card", missing_card)
            if reviewer is not None and current_card is None:
                self._expedition.complete_exhausted(expedition.expedition_id)
            else:
                self._expedition.pause(expedition.expedition_id)
        except Exception as error:
            self._diagnostics.emit(
                "expedition_reviewer_end_error",
                error_type=type(error).__name__,
            )

    def _on_expedition_progressed(self, event: ExpeditionProgressed) -> None:
        def update() -> None:
            if getattr(self._mw, "state", None) != "review":
                return
            expedition = self._expedition.get(event.expedition_id)
            if expedition is None:
                return
            view = build_expedition_view(
                expedition,
                self._expedition.checkpoints(expedition.expedition_id),
            )
            self._eval_review_js(
                "setProgress",
                {
                    "completed_reviews": view.completed_reviews,
                    "target_reviews": view.target_reviews,
                    "reviews_to_next_checkpoint": view.reviews_to_next_checkpoint,
                },
            )

        self._schedule(update)

    def _on_checkpoint_reached(self, event: CheckpointReached) -> None:
        self._orchestrator.enqueue(
            PresentationEvent(
                kind="expedition.checkpoint",
                prominence=PresentationProminence.MAJOR,
                priority=50,
                dedupe_key=f"checkpoint:{event.checkpoint_id}",
                payload={
                    "expedition_id": str(event.expedition_id),
                    "target_progress": event.target_progress,
                },
            )
        )
        self._schedule_boundary_flush()

    def _on_expedition_completed(self, event: ExpeditionCompleted) -> None:
        expedition = self._expedition.get(event.expedition_id)
        if expedition is None:
            return
        presentation = self._completion_event(event.expedition_id)
        self._presentations.enqueue(
            profile_key=expedition.profile_key,
            event=presentation,
            created_at=self._now(),
        )
        self._orchestrator.enqueue(presentation)
        self._schedule_boundary_flush()

    def _on_expedition_reopened(self, event: ExpeditionReopened) -> None:
        presentation = self._completion_event(event.expedition_id)
        if presentation.dedupe_key:
            self._presentations.invalidate(presentation.dedupe_key, at=self._now())

    def _schedule_boundary_flush(self) -> None:
        if self._flush_scheduled:
            return
        self._flush_scheduled = True
        self._schedule(self._flush_boundary)

    def _flush_boundary(self) -> None:
        self._flush_scheduled = False
        for event in self._orchestrator.take_boundary():
            if event.kind == "expedition.completion":
                if getattr(self._mw, "state", None) in {"review", "overview"}:
                    self._mw.moveToState("deckBrowser")
                self._schedule(self.show_today)
                continue

            if event.kind == "expedition.checkpoint":
                expedition_id = UUID(str(event.payload["expedition_id"]))
                expedition = self._expedition.get(expedition_id)
                if expedition is None:
                    continue
                target_progress = int(event.payload["target_progress"])
                if target_progress >= expedition.target_reviews:
                    continue
                if getattr(self._mw, "state", None) != "review":
                    continue
                self._eval_review_js(
                    "showCheckpoint",
                    {"target_progress": target_progress},
                )

    def _eval_review_js(self, method: str, payload: dict[str, Any]) -> None:
        safe_payload = json.dumps(payload, separators=(",", ":"))
        self._mw.web.eval(
            "window.AnkiAliveExpedition && "
            f"window.AnkiAliveExpedition.{method}({safe_payload});"
        )

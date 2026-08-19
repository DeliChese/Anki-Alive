from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from anki_alive.core.events import EventBus
from anki_alive.core.ids import Uuid4Factory
from anki_alive.core.review import ReviewObservation, ReviewReversed
from anki_alive.core.time import SystemClock
from anki_alive.diagnostics import DiagnosticsService
from anki_alive.expedition import ExpeditionRepository, ExpeditionService
from anki_alive.integration.compatibility import ensure_supported_anki_version
from anki_alive.integration.expedition_ui import ExpeditionUiRuntime
from anki_alive.integration.hooks import AnkiHookRuntime
from anki_alive.integration.settings_adapter import AnkiAddonSettingsAdapter
from anki_alive.integration.today_window import AnkiTodayWindow
from anki_alive.performance import PerformanceTimer, TimingSample
from anki_alive.presentation import PresentationRepository
from anki_alive.settings import SettingsService
from anki_alive.storage import Database


TODAY_PREWARM_DELAY_MS = 1200


@dataclass
class AddonRuntime:
    module_name: str
    event_bus: EventBus
    settings: SettingsService
    diagnostics: DiagnosticsService
    performance: PerformanceTimer
    hooks: AnkiHookRuntime
    expedition_ui: ExpeditionUiRuntime
    today_surface: AnkiTodayWindow
    database: Database
    expedition: ExpeditionService
    presentations: PresentationRepository

    def close(self) -> None:
        self.today_surface.shutdown()
        self.database.close()


_runtime: AddonRuntime | None = None


def bootstrap(module_name: str) -> AddonRuntime:
    """Initialize Anki Alive once inside Anki's add-on runtime."""

    global _runtime
    if _runtime is not None:
        return _runtime

    from anki.utils import int_version
    from aqt import gui_hooks, mw
    from aqt.qt import QAction, QTimer, qconnect
    from aqt.reviewer import Reviewer

    ensure_supported_anki_version(int_version())

    settings_adapter = AnkiAddonSettingsAdapter(
        addon_manager=mw.addonManager,
        module_name=module_name,
    )
    settings = SettingsService(
        load_raw=settings_adapter.load,
        save_raw=settings_adapter.save,
    )

    diagnostics = DiagnosticsService(
        enabled=bool(settings.snapshot.diagnostics.get("enabled", False)),
        logger=mw.addonManager.get_logger(module_name),
    )

    def record_timing(sample: TimingSample) -> None:
        diagnostics.emit(
            "performance_sample",
            name=sample.name,
            duration_ms=round(sample.duration_ms, 3),
        )

    performance = PerformanceTimer(record_timing)
    event_bus = EventBus()

    event_bus.subscribe(
        ReviewObservation,
        lambda event: diagnostics.emit(
            "review_observation",
            card_id=event.card_id,
            rating=event.rating,
            source_review_id=event.source_review_id,
            response_time_ms=event.response_time_ms,
            observation_id=str(event.observation_id),
        ),
    )
    event_bus.subscribe(
        ReviewReversed,
        lambda event: diagnostics.emit(
            "review_reversed",
            card_id=event.card_id,
            source_review_id=event.source_review_id,
            observation_id=(
                str(event.observation_id)
                if event.observation_id
                else None
            ),
        ),
    )

    addon_root = Path(__file__).resolve().parent.parent
    database = Database(addon_root / "user_files" / "anki_alive.sqlite3")
    database.open()

    local_timezone = datetime.now().astimezone().tzinfo
    if local_timezone is None:
        raise RuntimeError("unable to resolve local timezone")

    expedition = ExpeditionService(
        repository=ExpeditionRepository(database),
        event_bus=event_bus,
        clock=SystemClock(),
        ids=Uuid4Factory(),
        local_timezone=local_timezone,
    )
    event_bus.subscribe(ReviewObservation, expedition.on_review_observation)
    event_bus.subscribe(ReviewReversed, expedition.on_review_reversed)

    presentations = PresentationRepository(database)

    hooks = AnkiHookRuntime(
        mw=mw,
        gui_hooks=gui_hooks,
        event_bus=event_bus,
        performance=performance,
    )
    hooks.register()

    mw.addonManager.setWebExports(
        module_name,
        r"anki_alive/ui/.*\.(css|js)",
    )
    addon_package = mw.addonManager.addonFromModule(module_name)
    asset_base = f"/_addons/{addon_package}/anki_alive/ui"

    today_surface = AnkiTodayWindow(
        mw=mw,
        asset_base=asset_base,
    )
    expedition_ui = ExpeditionUiRuntime(
        mw=mw,
        gui_hooks=gui_hooks,
        event_bus=event_bus,
        expedition=expedition,
        presentations=presentations,
        settings=settings,
        diagnostics=diagnostics,
        reviewer_type=Reviewer,
        today_surface=today_surface,
        asset_base=asset_base,
        schedule=lambda callback: QTimer.singleShot(0, callback),
    )
    expedition_ui.register()

    tools_action = QAction("Anki Alive Today", mw)
    qconnect(tools_action.triggered, expedition_ui.show_today)
    mw.form.menuTools.addAction(tools_action)

    # Warm the hidden WebEngine surface after normal startup has had time to
    # settle. This moves Chromium/page setup out of the user's click path
    # without blocking add-on bootstrap.
    QTimer.singleShot(TODAY_PREWARM_DELAY_MS, today_surface.prepare)

    _runtime = AddonRuntime(
        module_name=module_name,
        event_bus=event_bus,
        settings=settings,
        diagnostics=diagnostics,
        performance=performance,
        hooks=hooks,
        expedition_ui=expedition_ui,
        today_surface=today_surface,
        database=database,
        expedition=expedition,
        presentations=presentations,
    )
    diagnostics.emit(
        "bootstrap_complete",
        module_name=module_name,
        anki_version=int_version(),
        database_integrity=database.integrity_check(),
    )
    return _runtime


def current_runtime() -> AddonRuntime | None:
    return _runtime


def reset_runtime_for_tests() -> None:
    global _runtime
    if _runtime is not None:
        _runtime.close()
    _runtime = None

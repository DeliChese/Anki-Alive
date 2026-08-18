from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from anki_alive.core.events import EventBus
from anki_alive.core.review import ReviewObservation, ReviewReversed
from anki_alive.diagnostics import DiagnosticsService
from anki_alive.integration.compatibility import ensure_supported_anki_version
from anki_alive.integration.hooks import AnkiHookRuntime
from anki_alive.integration.settings_adapter import AnkiAddonSettingsAdapter
from anki_alive.performance import PerformanceTimer, TimingSample
from anki_alive.settings import SettingsService
from anki_alive.storage import Database


@dataclass
class AddonRuntime:
    module_name: str
    event_bus: EventBus
    settings: SettingsService
    diagnostics: DiagnosticsService
    performance: PerformanceTimer
    hooks: AnkiHookRuntime
    database: Database

    def close(self) -> None:
        self.database.close()


_runtime: AddonRuntime | None = None


def bootstrap(module_name: str) -> AddonRuntime:
    """Initialize Anki Alive once inside Anki's add-on runtime."""

    global _runtime
    if _runtime is not None:
        return _runtime

    from anki.utils import int_version
    from aqt import gui_hooks, mw

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
            observation_id=str(event.observation_id) if event.observation_id else None,
        ),
    )

    addon_root = Path(__file__).resolve().parent.parent
    database = Database(addon_root / "user_files" / "anki_alive.sqlite3")
    database.open()

    hooks = AnkiHookRuntime(
        mw=mw,
        gui_hooks=gui_hooks,
        event_bus=event_bus,
        performance=performance,
    )
    hooks.register()

    _runtime = AddonRuntime(
        module_name=module_name,
        event_bus=event_bus,
        settings=settings,
        diagnostics=diagnostics,
        performance=performance,
        hooks=hooks,
        database=database,
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

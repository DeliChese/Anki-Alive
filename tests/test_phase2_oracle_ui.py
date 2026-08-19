from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from uuid import UUID

from anki_alive.core.events import EventBus
from anki_alive.core.presentation import PresentationEvent, PresentationProminence
from anki_alive.integration.oracle_ui import OracleUiRuntime
from anki_alive.integration.profile import load_or_create_profile_key
from anki_alive.oracle.events import OracleResolved
from anki_alive.oracle.model import OracleOutcome, OracleResult
from anki_alive.presentation import PresentationRepository
from anki_alive.settings import SettingsService
from anki_alive.storage import Database


class Hooks:
    def __init__(self) -> None:
        self.webview_will_set_content = []


class Web:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def eval(self, script: str) -> None:
        self.calls.append(script)


class ProfileManager:
    def __init__(self, folder: str) -> None:
        self._folder = folder

    def profileFolder(self) -> str:
        return self._folder


def make_settings(*, focus: bool = False, reduced_motion: bool = False) -> SettingsService:
    raw = {
        "focus_mode": {"enabled": focus},
        "motion": {"reduced_motion": reduced_motion},
    }
    return SettingsService(load_raw=lambda: raw, save_raw=lambda value: None)


def resolved_event() -> OracleResolved:
    return OracleResolved(
        oracle_prediction_id=UUID(int=10),
        expedition_id=UUID(int=20),
        card_id=42,
        predicted_outcome=OracleOutcome.FAIL,
        actual_recall_success=False,
        actual_rating=1,
        result=OracleResult.CORRECT,
    )


def enqueue_reveal(repository: PresentationRepository, profile_key: str) -> None:
    repository.enqueue(
        profile_key=profile_key,
        event=PresentationEvent(
            kind="oracle_resolution",
            prominence=PresentationProminence.MAJOR,
            priority=50,
            dedupe_key="oracle:test:resolution",
            payload={"card_id": 42},
        ),
        created_at=datetime(2026, 8, 19, 10, 0, tzinfo=timezone.utc),
    )


def test_oracle_reveal_marks_durable_presentation_shown() -> None:
    with TemporaryDirectory() as temporary_directory:
        database = Database(Path(temporary_directory) / "anki_alive.sqlite3")
        database.open()
        profile_key = load_or_create_profile_key(temporary_directory)
        presentations = PresentationRepository(database)
        enqueue_reveal(presentations, profile_key)

        web = Web()
        mw = SimpleNamespace(
            state="review",
            web=web,
            pm=ProfileManager(temporary_directory),
        )
        bus = EventBus()
        runtime = OracleUiRuntime(
            mw=mw,
            gui_hooks=Hooks(),
            event_bus=bus,
            presentations=presentations,
            settings=make_settings(reduced_motion=True),
            diagnostics=SimpleNamespace(emit=lambda *args, **kwargs: None),
            reviewer_type=object,
            asset_base="/_addons/test/anki_alive/ui",
            schedule=lambda callback: callback(),
        )
        runtime.register()

        bus.publish(resolved_event())

        assert len(web.calls) == 1
        assert "showResolution" in web.calls[0]
        assert '"reduced_motion":true' in web.calls[0]
        assert presentations.pending_for_profile(profile_key, kind="oracle_resolution") is None
        assert database.connection.execute(
            "SELECT status FROM presentation_events WHERE dedupe_key = ?",
            ("oracle:test:resolution",),
        ).fetchone() == ("SHOWN",)
        database.close()


def test_focus_mode_suppresses_reveal_without_web_output() -> None:
    with TemporaryDirectory() as temporary_directory:
        database = Database(Path(temporary_directory) / "anki_alive.sqlite3")
        database.open()
        profile_key = load_or_create_profile_key(temporary_directory)
        presentations = PresentationRepository(database)
        enqueue_reveal(presentations, profile_key)

        web = Web()
        mw = SimpleNamespace(
            state="review",
            web=web,
            pm=ProfileManager(temporary_directory),
        )
        bus = EventBus()
        runtime = OracleUiRuntime(
            mw=mw,
            gui_hooks=Hooks(),
            event_bus=bus,
            presentations=presentations,
            settings=make_settings(focus=True),
            diagnostics=SimpleNamespace(emit=lambda *args, **kwargs: None),
            reviewer_type=object,
            asset_base="/_addons/test/anki_alive/ui",
            schedule=lambda callback: callback(),
        )
        runtime.register()

        bus.publish(resolved_event())

        assert web.calls == []
        assert database.connection.execute(
            "SELECT status FROM presentation_events WHERE dedupe_key = ?",
            ("oracle:test:resolution",),
        ).fetchone() == ("SUPPRESSED",)
        database.close()

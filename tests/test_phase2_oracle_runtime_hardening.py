from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from uuid import UUID

from anki_alive.core.events import EventBus
from anki_alive.expedition.model import ExpeditionStatus
from anki_alive.integration.oracle import OracleReviewerRuntime
from anki_alive.integration.oracle_ui import OracleUiRuntime
from anki_alive.presentation import PresentationRepository
from anki_alive.settings import SettingsService
from anki_alive.storage import Database


class Hooks:
    def __init__(self) -> None:
        self.collection_did_load = []
        self.profile_will_close = []
        self.reviewer_did_show_question = []
        self.webview_will_set_content = []


class ProfileManager:
    def __init__(self, folder: str) -> None:
        self._folder = folder

    def profileFolder(self) -> str:
        return self._folder


class Diagnostics:
    def __init__(self) -> None:
        self.events: list[tuple[str, dict]] = []

    def emit(self, name: str, **fields) -> None:
        self.events.append((name, fields))


class FakeDb:
    def list(self, query: str, card_id: int, limit: int):
        del query, card_id, limit
        return [3, 3, 1, 3, 4]


class FakeCollection:
    def __init__(self) -> None:
        self.db = FakeDb()

    def get_card(self, card_id: int):
        return SimpleNamespace(
            id=card_id,
            memory_state=None,
            last_review_time=None,
            decay=None,
            ivl=8,
            lapses=1,
            reps=5,
        )


class FakeExpeditionRepository:
    def __init__(self) -> None:
        self.expedition = SimpleNamespace(
            expedition_id=UUID(int=20),
            status=ExpeditionStatus.ACTIVE,
            completed_reviews=0,
        )

    def active_for_profile(self, profile_key: str):
        del profile_key
        return self.expedition


class FakeOracle:
    def __init__(self) -> None:
        self.commits = []

    def commitment_count(self, expedition_id: UUID) -> int:
        del expedition_id
        return 0

    def commit(self, *, expedition_id: UUID, snapshot):
        self.commits.append((expedition_id, snapshot))
        return SimpleNamespace(
            oracle_prediction_id=UUID(int=30),
            expedition_id=expedition_id,
            card_id=snapshot.card_id,
            policy_version=2,
            predicted_recall_probability=None,
        )


class WebContent:
    def __init__(self, body: str) -> None:
        self.body = body
        self.css: list[str] = []
        self.js: list[str] = []


def make_settings() -> SettingsService:
    return SettingsService(
        load_raw=lambda: {},
        save_raw=lambda value: None,
    )


def test_reviewer_runtime_recovers_when_collection_hook_was_already_missed() -> None:
    with TemporaryDirectory() as temporary_directory:
        hooks = Hooks()
        diagnostics = Diagnostics()
        oracle = FakeOracle()
        collection = FakeCollection()
        mw = SimpleNamespace(
            col=collection,
            pm=ProfileManager(temporary_directory),
        )
        runtime = OracleReviewerRuntime(
            mw=mw,
            gui_hooks=hooks,
            expedition_repository=FakeExpeditionRepository(),
            oracle=oracle,
            diagnostics=diagnostics,
        )

        # Do not fire collection_did_load: this models add-on reload/late
        # bootstrap after the host event already happened.
        runtime.register()
        hooks.reviewer_did_show_question[0](SimpleNamespace(id=42))

        assert len(oracle.commits) == 1
        assert oracle.commits[0][1].card_id == 42
        assert any(name == "oracle_context_ready" for name, _ in diagnostics.events)


def test_oracle_online_marker_is_only_added_to_active_expedition_reviewer() -> None:
    with TemporaryDirectory() as temporary_directory:
        database = Database(Path(temporary_directory) / "anki_alive.sqlite3")
        database.open()
        hooks = Hooks()
        runtime = OracleUiRuntime(
            mw=SimpleNamespace(pm=ProfileManager(temporary_directory)),
            gui_hooks=hooks,
            event_bus=EventBus(),
            presentations=PresentationRepository(database),
            settings=make_settings(),
            diagnostics=Diagnostics(),
            reviewer_type=object,
            asset_base="/_addons/test/anki_alive/ui",
            schedule=lambda callback: callback(),
        )
        runtime.register()

        active = WebContent('<aside id="anki-alive-review-strip"></aside>')
        hooks.webview_will_set_content[0](active, object())
        assert 'id="anki-alive-oracle-online"' in active.body
        assert "Oracle" in active.body
        assert "oracle.css" in active.css[-1]
        assert "oracle.js" in active.js[-1]

        ordinary = WebContent("<main>normal review</main>")
        hooks.webview_will_set_content[0](ordinary, object())
        assert 'id="anki-alive-oracle-online"' not in ordinary.body
        database.close()

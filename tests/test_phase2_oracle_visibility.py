from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from uuid import UUID

from anki_alive.core.events import EventBus
from anki_alive.core.memory import MemorySnapshot
from anki_alive.expedition.model import ExpeditionStatus
from anki_alive.integration.oracle import OracleReviewerRuntime
from anki_alive.integration.oracle_ui import OracleUiRuntime
from anki_alive.oracle.events import OracleCommitted
from anki_alive.oracle.model import OracleOutcome
from anki_alive.oracle.policy import OraclePolicy
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


class Web:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def eval(self, script: str) -> None:
        self.calls.append(script)


class FakeDb:
    def list(self, query: str, card_id: int, limit: int):
        del query, card_id, limit
        return [3, 1, 1, 3, 4]


class FakeCollection:
    def __init__(self) -> None:
        self.db = FakeDb()

    def get_card(self, card_id: int):
        return SimpleNamespace(
            id=card_id,
            memory_state=None,
            last_review_time=None,
            decay=None,
            ivl=12,
            lapses=2,
            reps=8,
        )


class FakeExpeditionRepository:
    def __init__(self, expedition) -> None:
        self.expedition = expedition

    def active_for_profile(self, profile_key: str):
        del profile_key
        return self.expedition


class FakeOracle:
    def __init__(self) -> None:
        self.count = 0
        self.snapshots = []

    def commitment_count(self, expedition_id: UUID) -> int:
        del expedition_id
        return self.count

    def commit(self, *, expedition_id: UUID, snapshot: MemorySnapshot):
        self.snapshots.append(snapshot)
        self.count += 1
        return SimpleNamespace(
            oracle_prediction_id=UUID(int=30),
            expedition_id=expedition_id,
            card_id=snapshot.card_id,
            policy_version=2,
            predicted_recall_probability=None,
        )


def make_settings(*, focus: bool = False) -> SettingsService:
    raw = {
        "focus_mode": {"enabled": focus},
        "motion": {"reduced_motion": False},
    }
    return SettingsService(load_raw=lambda: raw, save_raw=lambda value: None)


def test_policy_uses_review_history_when_fsrs_state_is_missing() -> None:
    policy = OraclePolicy()
    fragile = MemorySnapshot(
        card_id=1,
        observed_at_utc=datetime(2026, 8, 19, 10, 0, tzinfo=timezone.utc),
        review_count=8,
        lapses=2,
        recent_outcomes=(3, 1, 1, 3, 4),
    )
    stable = MemorySnapshot(
        card_id=2,
        observed_at_utc=datetime(2026, 8, 19, 10, 0, tzinfo=timezone.utc),
        review_count=8,
        lapses=0,
        recent_outcomes=(3, 4, 3, 2, 3),
    )

    fragile_decision = policy.decide(fragile)
    stable_decision = policy.decide(stable)

    assert fragile_decision is not None
    assert fragile_decision.predicted_outcome is OracleOutcome.FAIL
    assert fragile_decision.predicted_recall_probability is None
    assert fragile_decision.policy_version == 2
    assert stable_decision is not None
    assert stable_decision.predicted_outcome is OracleOutcome.RECALL
    assert stable_decision.predicted_recall_probability is None


def test_commitment_cue_reveals_no_prediction_content() -> None:
    with TemporaryDirectory() as temporary_directory:
        database = Database(Path(temporary_directory) / "anki_alive.sqlite3")
        database.open()
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
            presentations=PresentationRepository(database),
            settings=make_settings(),
            diagnostics=SimpleNamespace(emit=lambda *args, **kwargs: None),
            reviewer_type=object,
            asset_base="/_addons/test/anki_alive/ui",
            schedule=lambda callback: callback(),
        )
        runtime.register()

        bus.publish(
            OracleCommitted(
                oracle_prediction_id=UUID(int=10),
                expedition_id=UUID(int=20),
                card_id=42,
                predicted_outcome=OracleOutcome.FAIL,
            )
        )

        assert len(web.calls) == 1
        assert "showCommitment" in web.calls[0]
        assert "FAIL" not in web.calls[0]
        assert "predicted_outcome" not in web.calls[0]
        database.close()


def test_first_eligible_card_in_cadence_window_can_commit() -> None:
    with TemporaryDirectory() as temporary_directory:
        expedition = SimpleNamespace(
            expedition_id=UUID(int=20),
            status=ExpeditionStatus.ACTIVE,
            completed_reviews=1,
        )
        oracle = FakeOracle()
        hooks = Hooks()
        runtime = OracleReviewerRuntime(
            mw=SimpleNamespace(pm=ProfileManager(temporary_directory)),
            gui_hooks=hooks,
            expedition_repository=FakeExpeditionRepository(expedition),
            oracle=oracle,
            diagnostics=SimpleNamespace(emit=lambda *args, **kwargs: None),
        )
        runtime.register()
        hooks.collection_did_load[0](FakeCollection())

        # Progress 1 is not an exact modulo-5 boundary. The old implementation
        # skipped the whole window here; the new rule uses its first eligible card.
        hooks.reviewer_did_show_question[0](SimpleNamespace(id=42))

        assert len(oracle.snapshots) == 1
        assert oracle.snapshots[0].card_id == 42
        assert oracle.snapshots[0].retrievability is None
        assert oracle.snapshots[0].recent_outcomes == (3, 1, 1, 3, 4)

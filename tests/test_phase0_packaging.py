import json
from pathlib import Path

import pytest

from anki_alive.integration.compatibility import (
    MIN_ANKI_VERSION,
    ensure_supported_anki_version,
)
from anki_alive.integration.settings_adapter import AnkiAddonSettingsAdapter


def test_minimum_anki_version_gate() -> None:
    ensure_supported_anki_version(MIN_ANKI_VERSION)
    ensure_supported_anki_version(MIN_ANKI_VERSION + 1)

    with pytest.raises(RuntimeError):
        ensure_supported_anki_version(MIN_ANKI_VERSION - 1)


def test_manifest_matches_runtime_minimum() -> None:
    root = Path(__file__).parents[1]
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))

    assert manifest["package"] == "anki_alive"
    assert manifest["min_point_version"] == MIN_ANKI_VERSION


def test_default_config_has_phase0_categories() -> None:
    root = Path(__file__).parents[1]
    config = json.loads((root / "config.json").read_text(encoding="utf-8"))

    assert set(config) == {
        "appearance",
        "motion",
        "focus_mode",
        "diagnostics",
        "feature_flags",
    }


def test_anki_addon_settings_adapter_uses_host_config_api() -> None:
    class FakeAddonManager:
        def __init__(self) -> None:
            self.saved = None

        def getConfig(self, module_name: str):
            assert module_name == "anki_alive_dev"
            return {"focus_mode": {"enabled": True}}

        def writeConfig(self, module_name: str, config: dict) -> None:
            assert module_name == "anki_alive_dev"
            self.saved = config

    manager = FakeAddonManager()
    adapter = AnkiAddonSettingsAdapter(
        addon_manager=manager,
        module_name="anki_alive_dev",
    )

    assert adapter.load() == {"focus_mode": {"enabled": True}}
    adapter.save({"diagnostics": {"enabled": False}})
    assert manager.saved == {"diagnostics": {"enabled": False}}

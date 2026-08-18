from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Mapping


DEFAULT_SETTINGS: dict[str, Any] = {
    "appearance": {
        "theme": "system",
    },
    "motion": {
        "reduced_motion": False,
    },
    "focus_mode": {
        "enabled": False,
    },
    "diagnostics": {
        "enabled": False,
    },
    "feature_flags": {},
}


@dataclass(frozen=True)
class SettingsSnapshot:
    appearance: dict[str, Any]
    motion: dict[str, Any]
    focus_mode: dict[str, Any]
    diagnostics: dict[str, Any]
    feature_flags: dict[str, Any]

    @property
    def focus_mode_enabled(self) -> bool:
        return bool(self.focus_mode.get("enabled", False))

    @property
    def reduced_motion(self) -> bool:
        return bool(self.motion.get("reduced_motion", False))


class SettingsService:
    """Typed boundary around Anki add-on config dictionaries.

    Unknown top-level keys are ignored. Known category dictionaries preserve
    unknown nested keys so future settings can round-trip without older code
    destroying them.
    """

    def __init__(
        self,
        *,
        load_raw: Callable[[], Mapping[str, Any] | None],
        save_raw: Callable[[dict[str, Any]], None],
    ) -> None:
        self._load_raw = load_raw
        self._save_raw = save_raw
        self._snapshot = self._normalize(load_raw())

    @property
    def snapshot(self) -> SettingsSnapshot:
        return self._snapshot

    def reload(self) -> SettingsSnapshot:
        self._snapshot = self._normalize(self._load_raw())
        return self._snapshot

    def set_focus_mode(self, enabled: bool) -> SettingsSnapshot:
        raw = self.to_raw()
        raw["focus_mode"]["enabled"] = bool(enabled)
        self._save_raw(raw)
        self._snapshot = self._normalize(raw)
        return self._snapshot

    def set_reduced_motion(self, enabled: bool) -> SettingsSnapshot:
        raw = self.to_raw()
        raw["motion"]["reduced_motion"] = bool(enabled)
        self._save_raw(raw)
        self._snapshot = self._normalize(raw)
        return self._snapshot

    def to_raw(self) -> dict[str, Any]:
        return {
            "appearance": deepcopy(self._snapshot.appearance),
            "motion": deepcopy(self._snapshot.motion),
            "focus_mode": deepcopy(self._snapshot.focus_mode),
            "diagnostics": deepcopy(self._snapshot.diagnostics),
            "feature_flags": deepcopy(self._snapshot.feature_flags),
        }

    @staticmethod
    def _normalize(raw: Mapping[str, Any] | None) -> SettingsSnapshot:
        merged = deepcopy(DEFAULT_SETTINGS)
        if isinstance(raw, Mapping):
            for category in merged:
                value = raw.get(category)
                if isinstance(value, Mapping):
                    merged[category].update(dict(value))

        theme = merged["appearance"].get("theme")
        if theme not in {"system", "dark", "light"}:
            merged["appearance"]["theme"] = "system"

        for category, key in (
            ("motion", "reduced_motion"),
            ("focus_mode", "enabled"),
            ("diagnostics", "enabled"),
        ):
            value = merged[category].get(key)
            if not isinstance(value, bool):
                merged[category][key] = DEFAULT_SETTINGS[category][key]

        return SettingsSnapshot(
            appearance=merged["appearance"],
            motion=merged["motion"],
            focus_mode=merged["focus_mode"],
            diagnostics=merged["diagnostics"],
            feature_flags=merged["feature_flags"],
        )

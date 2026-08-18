from __future__ import annotations

from typing import Any, Mapping


class AnkiAddonSettingsAdapter:
    """Thin adapter around Anki's add-on config API."""

    def __init__(self, *, addon_manager: Any, module_name: str) -> None:
        if not module_name:
            raise ValueError("module_name must not be empty")
        self._addon_manager = addon_manager
        self._module_name = module_name

    def load(self) -> Mapping[str, Any] | None:
        config = self._addon_manager.getConfig(self._module_name)
        return config if isinstance(config, Mapping) else None

    def save(self, config: dict[str, Any]) -> None:
        self._addon_manager.writeConfig(self._module_name, config)

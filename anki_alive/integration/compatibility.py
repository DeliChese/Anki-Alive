from __future__ import annotations

MIN_ANKI_VERSION = 250207
MIN_ANKI_VERSION_TEXT = "25.02.7"


def ensure_supported_anki_version(current_version: int) -> None:
    if current_version < MIN_ANKI_VERSION:
        raise RuntimeError(
            "Anki Alive requires Anki "
            f"{MIN_ANKI_VERSION_TEXT} or newer; detected {current_version}."
        )

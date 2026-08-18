from __future__ import annotations

from pathlib import Path
from uuid import uuid4

PROFILE_KEY_FILENAME = "anki_alive_profile_id"


def load_or_create_profile_key(profile_folder: str | Path) -> str:
    """Return a stable add-on-owned identity stored inside the Anki profile folder.

    The value survives profile renames because Anki renames the profile folder with
    the profile. Display names are therefore never used as durable identity.
    """

    folder = Path(profile_folder)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / PROFILE_KEY_FILENAME

    if path.exists():
        value = path.read_text(encoding="utf-8").strip()
        if value:
            return value

    value = str(uuid4())
    path.write_text(value + "\n", encoding="utf-8")
    return value

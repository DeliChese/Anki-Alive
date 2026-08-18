"""Anki add-on entrypoint for local development and packaged installs."""

from pathlib import Path
import sys

try:
    import aqt  # noqa: F401
except ModuleNotFoundError:
    _runtime = None
else:
    # During local development Anki imports the junction folder as
    # `anki_alive_dev`. Add the repository root explicitly so the internal
    # top-level `anki_alive` package resolves exactly as it does in tests and
    # packaged source layouts.
    _repo_root = str(Path(__file__).resolve().parent)
    if _repo_root not in sys.path:
        sys.path.insert(0, _repo_root)

    from anki_alive.bootstrap import bootstrap

    _runtime = bootstrap(__name__)

"""Anki add-on entrypoint for local development and packaged installs."""

try:
    import aqt  # noqa: F401
except ModuleNotFoundError:
    _runtime = None
else:
    from anki_alive.bootstrap import bootstrap

    _runtime = bootstrap(__name__)

"""Anki add-on entrypoint for local development and packaged installs."""

from anki_alive.bootstrap import bootstrap

_runtime = bootstrap(__name__)

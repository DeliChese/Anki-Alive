from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

SCHEMA_VERSION = 1


class Database:
    """Minimal sidecar SQLite foundation for Phase 0.

    Only schema metadata and migration history are durable at this phase.
    Feature tables intentionally do not exist yet.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._connection: sqlite3.Connection | None = None

    def open(self) -> None:
        if self._connection is not None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path)
        connection.execute("PRAGMA foreign_keys = ON")
        self._connection = connection
        self._migrate()

    def close(self) -> None:
        if self._connection is None:
            return
        self._connection.close()
        self._connection = None

    @property
    def connection(self) -> sqlite3.Connection:
        if self._connection is None:
            raise RuntimeError("database is not open")
        return self._connection

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        connection = self.connection
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise

    def _migrate(self) -> None:
        with self.transaction() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS schema_meta (
                    singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
                    schema_version INTEGER NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS migration_history (
                    version INTEGER PRIMARY KEY,
                    applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            row = connection.execute(
                "SELECT schema_version FROM schema_meta WHERE singleton = 1"
            ).fetchone()
            if row is None:
                connection.execute(
                    "INSERT INTO schema_meta(singleton, schema_version) VALUES (1, ?)",
                    (SCHEMA_VERSION,),
                )
                connection.execute(
                    "INSERT OR IGNORE INTO migration_history(version) VALUES (?)",
                    (SCHEMA_VERSION,),
                )
            elif row[0] > SCHEMA_VERSION:
                raise RuntimeError(
                    f"database schema {row[0]} is newer than supported {SCHEMA_VERSION}"
                )

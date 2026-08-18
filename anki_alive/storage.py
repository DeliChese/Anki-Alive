from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

SCHEMA_VERSION = 1
BUSY_TIMEOUT_MS = 5_000


class Database:
    """Minimal sidecar SQLite foundation for Phase 0.

    Only schema metadata and migration history are durable at this phase.
    Feature tables intentionally do not exist yet.

    The sidecar uses WAL because it is add-on-owned, local, and benefits from
    separating readers from writes. The database is checkpointed on close so
    backups can copy the main file after a graceful shutdown.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._connection: sqlite3.Connection | None = None

    def open(self) -> None:
        if self._connection is not None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(
            self.path,
            timeout=BUSY_TIMEOUT_MS / 1000,
        )
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute(f"PRAGMA busy_timeout = {BUSY_TIMEOUT_MS}")
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA synchronous = NORMAL")
        self._connection = connection
        self._migrate()

    def close(self) -> None:
        if self._connection is None:
            return
        try:
            self._connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        finally:
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

    def integrity_check(self) -> bool:
        row = self.connection.execute("PRAGMA integrity_check").fetchone()
        return bool(row and row[0] == "ok")

    def backup_to(self, destination: str | Path) -> Path:
        destination_path = Path(destination)
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(destination_path) as target:
            self.connection.backup(target)
        return destination_path

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

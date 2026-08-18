from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

SCHEMA_VERSION = 3
BUSY_TIMEOUT_MS = 5_000


class Database:
    """Add-on-owned sidecar SQLite database with explicit migrations."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._connection: sqlite3.Connection | None = None

    def open(self) -> None:
        if self._connection is not None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path, timeout=BUSY_TIMEOUT_MS / 1000)
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
            fresh_install = row is None
            if fresh_install:
                current_version = 1
                connection.execute(
                    "INSERT INTO schema_meta(singleton, schema_version) VALUES (1, 1)"
                )
            else:
                current_version = int(row[0])

            if current_version > SCHEMA_VERSION:
                raise RuntimeError(
                    f"database schema {current_version} is newer than supported {SCHEMA_VERSION}"
                )

            if current_version < 2:
                self._apply_phase1_schema(connection)
                if not fresh_install:
                    self._record_migration(connection, 2)
                current_version = 2

            if current_version < 3:
                self._apply_presentation_schema(connection)
                self._record_migration(connection, 3)
                current_version = 3

            connection.execute(
                """
                UPDATE schema_meta
                SET schema_version = ?, updated_at = CURRENT_TIMESTAMP
                WHERE singleton = 1
                """,
                (current_version,),
            )

    @staticmethod
    def _record_migration(connection: sqlite3.Connection, version: int) -> None:
        connection.execute(
            "INSERT OR IGNORE INTO migration_history(version) VALUES (?)",
            (version,),
        )

    @staticmethod
    def _apply_phase1_schema(connection: sqlite3.Connection) -> None:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS expeditions (
                expedition_id TEXT PRIMARY KEY,
                profile_key TEXT NOT NULL,
                local_study_date TEXT NOT NULL,
                status TEXT NOT NULL CHECK (
                    status IN (
                        'PLANNED', 'ACTIVE', 'PAUSED', 'COMPLETED',
                        'ABANDONED', 'INVALIDATED'
                    )
                ),
                created_at TEXT NOT NULL,
                started_at TEXT,
                paused_at TEXT,
                completed_at TEXT,
                ended_at TEXT,
                target_reviews INTEGER NOT NULL CHECK (target_reviews > 0),
                completed_reviews INTEGER NOT NULL DEFAULT 0 CHECK (
                    completed_reviews >= 0 AND completed_reviews <= target_reviews
                ),
                checkpoint_plan_version INTEGER NOT NULL DEFAULT 1,
                seed INTEGER,
                schema_version INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_expeditions_profile_status
            ON expeditions(profile_key, status, created_at)
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS expedition_checkpoints (
                checkpoint_id TEXT PRIMARY KEY,
                expedition_id TEXT NOT NULL REFERENCES expeditions(expedition_id)
                    ON DELETE CASCADE,
                ordinal INTEGER NOT NULL CHECK (ordinal > 0),
                target_progress INTEGER NOT NULL CHECK (target_progress > 0),
                status TEXT NOT NULL DEFAULT 'PENDING' CHECK (
                    status IN ('PENDING', 'REACHED')
                ),
                reached_at TEXT,
                UNIQUE(expedition_id, ordinal),
                UNIQUE(expedition_id, target_progress)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS expedition_review_observations (
                observation_id TEXT PRIMARY KEY,
                expedition_id TEXT NOT NULL REFERENCES expeditions(expedition_id)
                    ON DELETE CASCADE,
                source_review_id INTEGER,
                card_id INTEGER NOT NULL,
                applied_at TEXT NOT NULL,
                reversed_at TEXT
            )
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_expedition_review_source
            ON expedition_review_observations(expedition_id, source_review_id, card_id)
            """
        )

    @staticmethod
    def _apply_presentation_schema(connection: sqlite3.Connection) -> None:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS presentation_events (
                presentation_event_id TEXT PRIMARY KEY,
                profile_key TEXT NOT NULL,
                kind TEXT NOT NULL,
                prominence INTEGER NOT NULL,
                priority INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                status TEXT NOT NULL CHECK (
                    status IN (
                        'PENDING', 'SHOWN', 'DISMISSED', 'DEFERRED',
                        'SUPPRESSED', 'INVALIDATED'
                    )
                ),
                dedupe_key TEXT NOT NULL UNIQUE,
                payload_json TEXT NOT NULL DEFAULT '{}',
                resolved_at TEXT
            )
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_presentation_profile_status
            ON presentation_events(profile_key, status, created_at)
            """
        )

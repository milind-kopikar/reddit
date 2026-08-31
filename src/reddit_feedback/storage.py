from __future__ import annotations

import sqlite3
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path

from .models import CommentRecord

SCHEMA = """
CREATE TABLE IF NOT EXISTS comments (
    comment_id TEXT PRIMARY KEY,
    submission_id TEXT NOT NULL,
    subreddit TEXT NOT NULL,
    body TEXT NOT NULL,
    score INTEGER NOT NULL,
    created_utc TEXT NOT NULL,
    fetched_utc TEXT NOT NULL,
    expires_utc TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_comments_submission ON comments(submission_id);
CREATE INDEX IF NOT EXISTS idx_comments_expiry ON comments(expires_utc);
"""


class CommentStore:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(path)
        self.connection.executescript(SCHEMA)

    def close(self) -> None:
        self.connection.close()

    def sync_submission(self, submission_id: str, records: Iterable[CommentRecord]) -> int:
        """Replace a thread snapshot so deleted/removed comments disappear locally."""
        materialized = list(records)
        with self.connection:
            self.connection.execute(
                "DELETE FROM comments WHERE submission_id = ?", (submission_id,)
            )
            self.connection.executemany(
                """
                INSERT INTO comments VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        row.comment_id,
                        row.submission_id,
                        row.subreddit,
                        row.body,
                        row.score,
                        row.created_utc.isoformat(),
                        row.fetched_utc.isoformat(),
                        row.expires_utc.isoformat(),
                    )
                    for row in materialized
                ],
            )
        return len(materialized)

    def purge_expired(self, now: datetime | None = None) -> int:
        current = (now or datetime.now(UTC)).isoformat()
        with self.connection:
            cursor = self.connection.execute(
                "DELETE FROM comments WHERE expires_utc <= ?", (current,)
            )
        return cursor.rowcount

    def active_comments(self, now: datetime | None = None) -> list[sqlite3.Row]:
        self.connection.row_factory = sqlite3.Row
        current = (now or datetime.now(UTC)).isoformat()
        return self.connection.execute(
            "SELECT * FROM comments WHERE expires_utc > ? ORDER BY created_utc", (current,)
        ).fetchall()

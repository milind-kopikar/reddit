from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    database_path: Path
    report_directory: Path
    retention_hours: int
    max_comments_per_thread: int
    allowed_subreddits: frozenset[str]
    themes: dict[str, tuple[str, ...]]
    client_id: str
    client_secret: str
    user_agent: str


def load_settings(path: Path) -> Settings:
    with path.open("rb") as config_file:
        raw = tomllib.load(config_file)

    retention = int(raw.get("retention_hours", 48))
    if not 1 <= retention <= 48:
        raise ValueError("retention_hours must be between 1 and 48")

    max_comments = int(raw.get("max_comments_per_thread", 500))
    if not 1 <= max_comments <= 10_000:
        raise ValueError("max_comments_per_thread must be between 1 and 10,000")

    allowed = frozenset(str(name).casefold() for name in raw.get("allowed_subreddits", []))
    if not allowed:
        raise ValueError("allowed_subreddits must contain at least one subreddit")

    themes = {
        str(name): tuple(str(keyword).casefold() for keyword in keywords)
        for name, keywords in raw.get("themes", {}).items()
    }
    if not themes:
        raise ValueError("themes must contain at least one theme")

    return Settings(
        database_path=Path(raw.get("database_path", "data/reddit_feedback.sqlite3")),
        report_directory=Path(raw.get("report_directory", "reports")),
        retention_hours=retention,
        max_comments_per_thread=max_comments,
        allowed_subreddits=allowed,
        themes=themes,
        client_id=os.environ.get("REDDIT_CLIENT_ID", "").strip(),
        client_secret=os.environ.get("REDDIT_CLIENT_SECRET", "").strip(),
        user_agent=os.environ.get("REDDIT_USER_AGENT", "").strip(),
    )

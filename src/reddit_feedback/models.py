from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CommentRecord:
    comment_id: str
    submission_id: str
    subreddit: str
    body: str
    score: int
    created_utc: datetime
    fetched_utc: datetime
    expires_utc: datetime

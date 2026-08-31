from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime, timedelta
from urllib.parse import urlparse

import praw
from praw.models import MoreComments

from .config import Settings
from .models import CommentRecord


class RedditCollector:
    """Read-only OAuth client limited to explicitly approved subreddits."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        missing = [
            name
            for name, value in {
                "REDDIT_CLIENT_ID": settings.client_id,
                "REDDIT_CLIENT_SECRET": settings.client_secret,
                "REDDIT_USER_AGENT": settings.user_agent,
            }.items()
            if not value
        ]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        self.reddit = praw.Reddit(
            client_id=settings.client_id,
            client_secret=settings.client_secret,
            user_agent=settings.user_agent,
            check_for_async=False,
        )
        if not self.reddit.read_only:
            raise RuntimeError("The Reddit client must operate in read-only mode")

    def collect_thread(self, url: str) -> tuple[str, str, list[CommentRecord]]:
        _validate_thread_url(url)
        submission = self.reddit.submission(url=url)
        subreddit = str(submission.subreddit)
        if subreddit.casefold() not in self.settings.allowed_subreddits:
            raise ValueError(f"r/{subreddit} is not in allowed_subreddits")

        # Bound expansion calls as well as stored comments; do not crawl an entire large thread.
        submission.comments.replace_more(limit=5)
        fetched = datetime.now(UTC)
        expires = fetched + timedelta(hours=self.settings.retention_hours)
        records: list[CommentRecord] = []

        for comment in _take(submission.comments.list(), self.settings.max_comments_per_thread):
            body = str(comment.body)
            if body in {"[deleted]", "[removed]"}:
                continue
            records.append(
                CommentRecord(
                    comment_id=str(comment.id),
                    submission_id=str(submission.id),
                    subreddit=subreddit,
                    body=body,
                    score=int(comment.score),
                    created_utc=datetime.fromtimestamp(float(comment.created_utc), UTC),
                    fetched_utc=fetched,
                    expires_utc=expires,
                )
            )
        return str(submission.id), subreddit, records


def _take(items: Iterable[object], limit: int) -> Iterable[object]:
    yielded = 0
    for item in items:
        if yielded >= limit:
            return
        if isinstance(item, MoreComments):
            continue
        yielded += 1
        yield item


def _validate_thread_url(url: str) -> None:
    parsed = urlparse(url)
    host = (parsed.hostname or "").casefold()
    is_reddit_host = host == "reddit.com" or host.endswith(".reddit.com") or host == "redd.it"
    if parsed.scheme != "https" or not is_reddit_host or "/comments/" not in parsed.path:
        raise ValueError("Expected an HTTPS Reddit thread URL containing /comments/")

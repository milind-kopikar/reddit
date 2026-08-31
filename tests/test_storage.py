from datetime import UTC, datetime, timedelta

from reddit_feedback.models import CommentRecord
from reddit_feedback.storage import CommentStore


def record(comment_id: str, expires: datetime) -> CommentRecord:
    now = datetime(2026, 1, 1, tzinfo=UTC)
    return CommentRecord(
        comment_id=comment_id,
        submission_id="submission",
        subreddit="learnmachinelearning",
        body="Useful course feedback",
        score=1,
        created_utc=now,
        fetched_utc=now,
        expires_utc=expires,
    )


def test_sync_removes_comments_no_longer_returned(tmp_path) -> None:
    store = CommentStore(tmp_path / "test.sqlite3")
    future = datetime.now(UTC) + timedelta(hours=1)
    store.sync_submission("submission", [record("one", future), record("two", future)])
    store.sync_submission("submission", [record("two", future)])

    assert [row["comment_id"] for row in store.active_comments()] == ["two"]
    store.close()


def test_purge_removes_expired_content(tmp_path) -> None:
    store = CommentStore(tmp_path / "test.sqlite3")
    now = datetime(2026, 1, 1, tzinfo=UTC)
    store.sync_submission("submission", [record("old", now - timedelta(seconds=1))])

    assert store.purge_expired(now) == 1
    store.close()

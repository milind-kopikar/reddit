import pytest

from reddit_feedback.client import _validate_thread_url


@pytest.mark.parametrize(
    "url",
    [
        "https://www.reddit.com/r/example/comments/abc123/title/",
        "https://old.reddit.com/r/example/comments/abc123/title/",
    ],
)
def test_accepts_reddit_thread_urls(url: str) -> None:
    _validate_thread_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "http://www.reddit.com/r/example/comments/abc123/title/",
        "https://example.com/r/example/comments/abc123/title/",
        "https://notreddit.com/r/example/comments/abc123/title/",
        "https://www.reddit.com/r/example/",
    ],
)
def test_rejects_non_thread_urls(url: str) -> None:
    with pytest.raises(ValueError):
        _validate_thread_url(url)

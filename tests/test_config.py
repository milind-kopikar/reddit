from pathlib import Path

import pytest

from reddit_feedback.config import load_settings


def write_config(path: Path, retention_hours: int) -> None:
    path.write_text(
        f"""
retention_hours = {retention_hours}
allowed_subreddits = ["example"]
[themes]
value = ["worth"]
""",
        encoding="utf-8",
    )


def test_accepts_maximum_48_hour_retention(tmp_path: Path) -> None:
    path = tmp_path / "config.toml"
    write_config(path, 48)

    assert load_settings(path).retention_hours == 48


def test_rejects_retention_over_48_hours(tmp_path: Path) -> None:
    path = tmp_path / "config.toml"
    write_config(path, 49)

    with pytest.raises(ValueError, match="between 1 and 48"):
        load_settings(path)

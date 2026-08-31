from __future__ import annotations

import csv
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from sqlite3 import Row


def theme_counts(comments: list[Row], themes: dict[str, tuple[str, ...]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for comment in comments:
        text = str(comment["body"]).casefold()
        for theme, keywords in themes.items():
            if any(_contains(text, keyword) for keyword in keywords):
                counts[theme] += 1
    return counts


def write_aggregate_report(
    output_directory: Path,
    comments: list[Row],
    themes: dict[str, tuple[str, ...]],
) -> Path:
    """Export counts only: no usernames, comment text, IDs, or permalinks."""
    output_directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    path = output_directory / f"theme-counts-{timestamp}.csv"
    counts = theme_counts(comments, themes)
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(["theme", "matching_comments", "total_comments"])
        for theme in sorted(themes):
            writer.writerow([theme, counts[theme], len(comments)])
    return path


def _contains(text: str, keyword: str) -> bool:
    return re.search(rf"(?<!\w){re.escape(keyword)}(?!\w)", text) is not None


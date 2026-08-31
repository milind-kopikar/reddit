import sqlite3

from reddit_feedback.report import theme_counts


def rows(*bodies: str) -> list[sqlite3.Row]:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute("CREATE TABLE sample (body TEXT)")
    connection.executemany("INSERT INTO sample VALUES (?)", [(body,) for body in bodies])
    return connection.execute("SELECT * FROM sample").fetchall()


def test_theme_counts_each_comment_once_per_theme() -> None:
    comments = rows("Python coding and more coding", "I need a no-code beginner option", "unrelated")
    themes = {"coding": ("python", "coding"), "no_code": ("no-code",)}

    assert theme_counts(comments, themes) == {"coding": 1, "no_code": 1}


def test_theme_matching_respects_word_boundaries() -> None:
    assert theme_counts(rows("A ragged edge"), {"rag": ("rag",)}) == {}


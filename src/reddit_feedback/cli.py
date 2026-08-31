from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

from .client import RedditCollector
from .config import load_settings
from .report import write_aggregate_report
from .storage import CommentStore


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Collect approved Reddit education feedback")
    root.add_argument("--config", type=Path, default=Path("config.toml"))
    commands = root.add_subparsers(dest="command", required=True)
    collect = commands.add_parser("collect", help="Synchronize one or more approved threads")
    collect.add_argument("urls", nargs="+")
    commands.add_parser("report", help="Write an aggregate theme-count report")
    commands.add_parser("purge", help="Delete locally expired content")
    return root


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    args = parser().parse_args(argv)
    try:
        settings = load_settings(args.config)
        store = CommentStore(settings.database_path)
        try:
            purged = store.purge_expired()
            if args.command == "collect":
                collector = RedditCollector(settings)
                for url in args.urls:
                    submission_id, subreddit, records = collector.collect_thread(url)
                    count = store.sync_submission(submission_id, records)
                    print(f"Synchronized {count} comments from r/{subreddit} ({submission_id})")
                print(f"Purged {purged} expired comments")
            elif args.command == "report":
                output = write_aggregate_report(
                    settings.report_directory, store.active_comments(), settings.themes
                )
                print(f"Wrote aggregate report to {output}")
            else:
                print(f"Purged {purged} expired comments")
        finally:
            store.close()
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


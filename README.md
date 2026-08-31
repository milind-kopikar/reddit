# Reddit Education Feedback Research

A small, read-only prototype for an approved higher-education feedback use case. It uses Reddit's
OAuth Data API to collect comments from thread URLs explicitly supplied by a researcher, keeps raw
content for at most 48 hours, and exports only aggregate counts for predefined themes.

This repository is source code for Reddit's app review. Having the code does **not** grant API
access. Do not run collection until Reddit has approved the use case and issued credentials.

## Scope and safeguards

- Reads public comments from manually supplied threads in an allowlist of subreddits.
- Never posts, votes, messages, moderates, follows users, or discovers threads automatically.
- Uses OAuth and an honest, versioned user agent identifying `u/AILearner-2024`.
- Does not access or store comment-author usernames or profile data.
- Replaces each thread snapshot when refreshed, removing content no longer returned by Reddit.
- Purges temporary comment content after a configurable maximum of 48 hours.
- Exports theme counts only—never comment bodies, IDs, usernames, or permalinks.
- Does not train or fine-tune any AI/ML model and makes no automated decisions about individuals.
- Does not sell Reddit data or use it for advertising, user profiling, or outreach.

See [PRIVACY.md](PRIVACY.md) for the full data-handling statement and
[APPLICATION.md](APPLICATION.md) for suggested app-review answers.

## How it works

```text
approved thread URL -> OAuth read-only fetch -> temporary SQLite snapshot (<=48h)
                                            -> predefined keyword counts -> aggregate CSV
```

The keyword themes are transparent and editable in `config.toml`. A comment counts at most once
per theme. The counts are descriptive signals for human review, not claims of sentiment, user
intent, or statistical representativeness.

## Setup (after approval)

Requirements: Python 3.11+ and a Reddit OAuth application approved for this use case.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
Copy-Item config.example.toml config.toml
```

Fill in `.env` locally. Never commit it. Use Reddit's required user-agent form:

```text
windows:edu-feedback-research:v0.1.0 (by /u/AILearner-2024)
```

Limit `allowed_subreddits` and the themes in `config.toml` to Reddit's approved scope.

## Usage

Synchronize one or more specifically selected threads:

```powershell
edu-feedback collect "https://www.reddit.com/r/learnmachinelearning/comments/POST_ID/.../"
```

Create a counts-only CSV, or purge expired raw content:

```powershell
edu-feedback report
edu-feedback purge
```

Run `purge` on a schedule at least daily. For active work, re-run `collect` before analysis so the
local snapshot reflects removals. If access is revoked, `purge` still works without credentials.

## Testing

Tests do not contact Reddit and require no credentials:

```powershell
pytest
ruff check .
```

## Operational limits

The client relies on PRAW's OAuth and rate-limit handling, caps stored comments per thread, and
bounds `MoreComments` expansion to five API calls per collection.
Only authorized team members should run it. Before sharing any report, a human must review small
counts for re-identification risk and confirm that the proposed use remains within Reddit's written
approval, current terms, institutional privacy/ethics requirements, and applicable law.

This is an independent research prototype and is not endorsed by or affiliated with Reddit.

## Reddit policy references

Operators must review the current official requirements before every deployment:

- [Reddit Data API Wiki](https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki)
- [Data API Terms](https://redditinc.com/policies/data-api-terms)
- [Developer Terms](https://redditinc.com/policies/developer-terms)
- [Developer Data Protection Addendum](https://redditinc.com/policies/developer-dpa)

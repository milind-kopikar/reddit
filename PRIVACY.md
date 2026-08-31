# Privacy and data handling

This internal research prototype accesses only public comments in thread URLs supplied by an
authorized operator. It does not post, vote, message, moderate, or contact Reddit users.

## Data collected

For each accessible, non-deleted comment, the temporary local database contains the comment and
submission IDs, subreddit, body, score, and creation/fetch/expiry timestamps. It does not access or
store author names, profiles, email addresses, avatars, or flair.

## Purpose and sharing

Temporary content is used only to calculate aggregate, predefined theme counts for approved
higher-education course research. Reports contain counts only. Raw Reddit content is not shared,
published, sold, used for advertising, used to profile or contact people, or used to train or fine-
tune an AI/ML model.

## Retention and deletion

Raw content expires no later than 48 hours after each fetch. Every command purges expired rows.
Re-collecting a thread replaces its complete local snapshot, removing comments that Reddit no
longer returns. An operator should re-synchronize active threads and run `edu-feedback purge` on a
schedule. On a Reddit or rights-holder removal request, stop processing the affected material,
delete the local database if the affected ID cannot be isolated, and follow Reddit's escalation
process.

Aggregate reports should be reviewed before sharing to avoid small-cell re-identification. The
operator is responsible for institutional ethics/privacy review and applicable law.

## Security

OAuth credentials are environment variables and must never be committed. Data and report
directories are Git-ignored. Access should be limited to the named research team.

Questions or deletion requests: contact the project owner through u/AILearner-2024 on Reddit.

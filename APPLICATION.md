# Suggested Reddit Data API application answers

Replace bracketed text and the GitHub placeholder before submitting. Describe the intended use
truthfully; do not describe it as purely academic if results will guide a paid or commercial
offering.

## Reddit account name

`u/AILearner-2024`

## What benefit or purpose will the app have for Redditors?

I teach at IIT Bombay and work in higher education. This internal research prototype will help an
authorized university team understand recurring, aggregate feedback that Redditors publicly share
about continuing-education and professional courses. The team will use theme-level findings to
inform human decisions about course prerequisites, coding and no-code pathways, practical projects,
and course value. The intended benefit is that educators can respond to needs already expressed in
public discussions. The app will not contact, profile, score, or make decisions about individual
Redditors, and it will not post or otherwise act on Reddit.

## Detailed description of what the app will do on Reddit

An authorized researcher manually supplies URLs of relevant public threads within the approved
subreddit allowlist. The app uses OAuth to read accessible comments from those specific threads. It
does not crawl Reddit, discover communities automatically, monitor users, or collect private data.

The prototype temporarily stores comment text, Reddit comment/submission IDs, score and timestamps
for no more than 48 hours. It does not access or store author usernames or profiles. Re-fetching a
thread replaces the local snapshot so comments Reddit no longer returns are removed. Expired rows
are automatically purged whenever the tool runs, with a separate purge command available for
scheduled deletion.

Analysis is limited to counts of predefined, transparent keywords—for example, how often comments
mention prior coding experience, no-code options, hands-on projects, cost/value, or RAG/workflows.
Reports contain aggregate counts only, not comment text, usernames, IDs, or links. Findings are
reviewed by educators and are not treated as representative survey results. Reddit content will not
be sold, used for advertising or outreach, or used to train/fine-tune an AI or machine-learning
model. Access will remain within the use case and limits Reddit approves.

## What is missing from Devvit that prevents building on that platform?

This is an external, researcher-operated analysis workflow rather than an experience installed in
a subreddit. It needs to accept a small set of researcher-selected thread URLs, run within the
university's controlled environment, apply institutional access and retention controls, and produce
an internal aggregate CSV for faculty review. It does not need to add UI, moderation actions,
automations, games, or other interactive functionality inside Reddit. I am therefore requesting
approved, read-only OAuth Data API access for this narrowly scoped workflow.

## Source code

`https://github.com/milind-kopikar/reddit`

The repository includes setup instructions, tests, an explicit subreddit allowlist, a 48-hour
maximum retention check, snapshot synchronization for removals, aggregate-only export, and the
project privacy statement. Credentials and collected data are excluded from Git.

## Subreddits

Initially: `r/learnmachinelearning`, `r/nursing`, and `r/HealthInformatics`. Collection will be
limited to relevant public threads manually selected within the communities Reddit approves. Any
additional subreddit will be added only if covered by Reddit's approval and the project's
institutional review.

## Additional disclosure worth including if the form permits

The expected volume is [NUMBER] manually selected threads per [WEEK/MONTH], up to 500 comments per
thread. The only operators are [TEAM/ROLES]. Findings will be used [DESCRIBE WHETHER ONLY FOR
RESEARCH, INTERNAL COURSE IMPROVEMENT, OR A COMMERCIAL OFFERING]. No data will be provided to third
parties. I will comply with Reddit's current Developer Terms, Data API Terms, Developer Data
Protection Addendum, rate limits, deletion requirements, and any additional conditions in the
approval.

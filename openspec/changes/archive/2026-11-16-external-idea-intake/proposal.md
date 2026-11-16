# Proposal: external idea intake for the feedback loop

Source: Brian, 2026-11-16: "i assume this should be configurable within aes. i.e. this is an
automated aspect of the aes feedback loop and you should be able to put the subreddits to examine as
part of that in the configuration"; and "i approve" to Decision 7 option B (build the configuration and
the command now, run on request; add the timer only after one digest has been seen and judged useful).
Context: the wiki page `wiki/external-sources-watch.md` lists the eight subreddits read so far.

## Why

The feedback loop reads only agent session transcripts. Outside ideas (Reddit posts about agent tooling,
skills and knowledge systems) reach AES only when Brian pastes or saves them and an agent reads them by
hand. Brian wants to name subreddits to watch in AES configuration and have new posts surface for review.

## What changes

- A configuration file, `scripts/learning_loop/external_sources.yaml`, lists the subreddits to watch.
  Each entry has a name, a one-line reason, a listing (top or new), a time window, a post limit and a
  minimum score. Seeded with the eight subreddits on the watch page. r/LocalLLaMA is not included
  (Brian, 2026-11-16: "take locallama off the list").
- A command, `scripts/learning_loop/external_ideas.py`, reads that file, fetches each subreddit's
  listing through the social-media server's public Reddit tool, drops posts already seen, applies the
  score and age limits, and writes a digest of candidates. It ranks by score and age only; it does not
  judge relevance, because that is prose meaning and needs an approved light model as a separate,
  measured stage if it is ever added.
- It runs on request. No timer is installed in this change.

## Output and privacy

Fetched posts and the digest go to a local output folder outside the repository. The digest lists
title, subreddit, score, age, comment count, the post link and the outbound links in the post body. A
candidate is copied into `raw/sources/` only when an agent assesses it, as the wiki already does. The
learnings register is frozen (Decision 18, 2026-11-16) and this change never writes to it.

## Trace

Each run appends one line per step to a daily run log: config revision, subreddits requested, one
record per listing call with its result count and any error, seen-post filter counts, per-step timing,
and the digest path. A listing call that fails twice the same way is reported as down and the run exits
non-zero.

## Cost basis

Worked out: one listing call per configured subreddit per run (8 calls for the seed list), no model
calls, so model spend is $0. Reddit read calls use the existing read-only credentials. Not measured yet;
the first run will record the actual call count and time.

## Out of scope

The timer, relevance ranking by a model, automatic capture and assessment, and any write to Reddit
(votes, saves, comments).

## Plan size

Planned work that is small under `plan-size` in core.md: undone with `git revert`, nothing outward,
model spend $0, no file another repository reads. One independent read before merge.

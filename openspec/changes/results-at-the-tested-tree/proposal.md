## Why

Brian, 2026-11-27 18:50: "Pass or fail only appears after make check on that exact commit, and it isn't written back
into this page". On 2026-11-28 an isolated Haiku run on a fresh template copy (commit 1fcf203) did what an agent
should: it ran `make check` and then committed exactly the files it had tested. Its `generated/wiki/results.md` still
said "results were recorded with uncommitted changes", because `lockstep status` trusts recorded results only when
they were taken at the current commit on a clean tree, and nothing rewrote the page after the commit.

## What Changes

- `make check` records, in `.code2check/run.json`, the git tree of the working files it tested (tracked files and
  untracked files git does not ignore), through a new `lockstep record-tree` command that builds the tree in a
  temporary index and never touches the real one. The template records it on a test failure too, so a failing run
  also counts for the commit.
- `lockstep status` also uses recorded results when that tree equals the current commit's tree and nothing is
  uncommitted now, and says "tested tree matches the commit".
- A fresh copy runs `lockstep check project` after each commit (a `post-commit` hook), so the results page shows pass
  or fail for the new commit without another `make check`.

Plan size: small

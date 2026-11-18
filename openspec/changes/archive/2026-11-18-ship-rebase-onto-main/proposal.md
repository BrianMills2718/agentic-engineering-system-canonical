## Why

Two sessions that each add an entry at the top of the same log file (for example vision's `wiki/log.md`, newest entry first) always conflict: `ship` pushes a branch cut from an older `main` and asks GitHub to merge it, and GitHub refuses with "Pull Request has merge conflicts" (code2-workspace issue 472, vision pull request 212, 2026-11-17). The session then redoes the work by hand on a new branch. GitHub's merge does not apply a repository's `.gitattributes` merge drivers; a local `git rebase` does.

## What Changes

- Before the gates and the check, `ship` fetches `origin` and, when the branch is behind the default branch and has not been pushed yet, rebases it onto the default branch. Git's built-in `union` merge driver, set per file in the repository's `.gitattributes` (`wiki/log.md merge=union`), keeps both sides' added lines, so the two log entries both survive.
- When the rebase stops on a conflict, `ship` aborts it, leaves the branch as it was, names the conflicting paths, and pushes nothing.
- A branch already on the remote is not rebased (that would need a force-push); `ship` says so and goes on as before.
- When the fetch fails, `ship` says so and goes on as before.

## Impact

- `scripts/ship.py`, `tests/test_ship.py`, `openspec/specs/ship/spec.md`.
- Every repository that merges with `ship`: the checked and merged commit is the rebased one. A repository opts a file into keeping both sides by one `.gitattributes` line.

Plan size: small

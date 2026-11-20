## Why

Lanes whose work was never merged pile up: on 2026-11-19 `~/code2` had 136 worktrees using about 23 GB (mostly a `.venv` per lane), and the `lane-sweep` timer, which runs every 10 minutes, removed none of them, because it keeps every lane whose content is not on the remote default branch ("work not on origin/main", 188 kept at 21:00). 47 lanes had their last commit on 2026-11-13, one fan-out day (29 of them in one repository), and sat six days. 86 were removed by hand that day with an archive-then-remove procedure; this change makes the sweep do that procedure itself.

## What Changes

- A clean, unused, unlocked lane whose work is not on the default branch and that has been idle 72 hours (`lane_sweep_archive_after_hours:` in `graph-config.yaml`; 0 turns it off) is archived, then only its worktree is removed. The local branch stays.
- Archive: unless a remote branch already holds the tip, the sweep creates `refs/archive/<YYYYMMDD>/<lane>` at the tip, writes a `git bundle` of the commits not on the default branch into `~/code2/.lane-sweep-logs/`, and verifies it. A failed verify keeps the lane and makes the run exit 1. The ref is pushed to origin only when origin's owner is the `owner:` setting and GitHub reports the repository private, so work nobody pushed is never published.
- The day's log names the branch, tip, bundle, the `git worktree add` command that restores the lane, and any ignored non-cache files the removal deletes.
- Dirty, locked, in-use and `--keep-lane` lanes are kept as before.
- One new output line, `lanes kept per repository:`, counts kept lanes per repository and marks a count over 8.

## Impact

- `scripts/lane_sweep.py`, `tests/test_lane_sweep.py`, `openspec/specs/lane-sweep/spec.md`.
- The `lane-sweep` timer (run from the runtime clone `~/.hive-brain/aes`) and every `ship` merge start archiving and removing idle unmerged lanes once this reaches main there. A dry run of the new code over `~/code2` on 2026-11-19 (no `--apply`, no fetch) listed 22 lanes as archivable and wrote no ref and no bundle.

Plan size: small

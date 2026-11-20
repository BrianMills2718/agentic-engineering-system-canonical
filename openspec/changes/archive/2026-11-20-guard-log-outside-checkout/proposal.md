## Why

The edit guard wrote its log into the checkout it guarded (`src/lockstep/hook.py:172-187` at d7f2eabfc). Two effects, issue #974:

- Agents work in short-lived worktrees that `ship` removes after merge, so their logs are deleted and guard use cannot be counted. On 2026-11-19 world-substrate had zero guard logs across 177 commits since 2026-11-12, which proves nothing either way.
- A repository without `lockstep init`'s `.gitignore` line commits the log: on 2026-11-19 an automated agent's pull request in a downstream repository carried `.lockstep/hook-*.jsonl` files.

Brian said yes on 2026-11-20 to proving Lockstep on two local repositories before rolling it out further; this fix is step 1 of that plan (`docs/planning/next.goal.md`), because both proofs count guard decisions.

## What Changes

- The guard logs to `$LOCKSTEP_LOG_DIR` when set, else `${XDG_STATE_HOME:-~/.local/state}/lockstep/<repository name>/hook-<date>.jsonl`. A worktree uses its main checkout's folder name, read from its `.git` file without running git.
- Each record gains `project`, the checkout path, since several worktrees share one folder.
- `lockstep-hook --would-block` counts the new folder and the project's old `.lockstep/` and `.pcw/`.
- `lockstep init` still adds `.lockstep/` to `.gitignore`, for old logs and for a `LOCKSTEP_LOG_DIR` pointed inside the checkout.

## Impact

- `src/lockstep/hook.py`; tests in `tests/lockstep/`.
- The Team-Brains brain pull-request runner reads refusals from a mounted `.lockstep/` in its checkout and pins `LOCKSTEP_SHA`. When that pin moves past this change, the runner must set `LOCKSTEP_LOG_DIR` to its mounted folder, or it stops seeing refusals. Noted in the pull request that closes #974.
- Two repositories with the same folder name (for example one in `~/code` and one in `~/code2`) share a log folder; each record's `project` field tells them apart.

Plan size: full
Planning package: docs/planning/planning-package.json

Closes: lockstep-init/the-edit-guard-logs-outside-the-checkout

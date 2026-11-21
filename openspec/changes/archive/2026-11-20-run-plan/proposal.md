## Why

Brian, 2026-11-20: "the goal is to give a well specified plan to an agent on some proejct nad have it faithfulyy and successfully impelemnt it", and "start with the minimal core than add on other things as needed after the first minimal core milestone". The minimal core (`docs/planning/minimal-core-2026-11-20.md` section 6) has two new steps that today exist only as hand-run scripts in a private folder: hidden acceptance tests (C3) and the departure report (C4). The plan-fidelity test on 2026-11-20 ran them by hand on three world-substrate plans; the hidden tests were the check that measured success (PLAN.md results table, 6 of 6 runs). Packaging them in `lockstep`, which every machine already installs with `uvx`, makes them runnable by anyone on any repository (K1 portable, K6 same in Claude and Codex).

## What Changes

Three `lockstep` commands, all report-only; none merges.

- `lockstep accept write <change> [--ref REF] [--agent claude|codex]`: a headless session, in a throwaway detached worktree at `REF` (default `HEAD`), reads the plan and the existing code and tests (for fixtures and import patterns; nothing is implemented yet) and writes pytest files named `test_accept_<n>.py` into the run's `accept/` folder outside every worktree. The session keeps no history on disk (`claude --no-session-persistence`, `codex exec --ephemeral`), and the worktree is removed afterwards. The driver then runs the hidden tests once at `REF` and records the result as `accept_before`; a hidden test that already passes before any implementation is flagged.
- `lockstep accept check <change> [--base REF]`, run in the implementer's worktree after its last commit: counts uncommitted files, copies the hidden tests into `tests/` (refusing if a file of that name exists), runs the test command, removes the copies, runs the check command, writes the departure report, and records the branch head commit with the results. Any agent, headless or interactive, can be the implementer between `accept write` and `accept check`.
- `lockstep run-plan <change> [--ref REF] [--agent claude|codex]` does `accept write`, then a headless implementer session in a new worktree on branch `impl/<change>-<run id>`, then `accept check`, and prints the `ship` command to run next.
- **Departure report** (inside `accept check`): every file changed in commits since `REF` whose repository-relative path does not appear in the plan's `tasks.md` as read from `REF` (so the implementer cannot add names), excluding `openspec/`; and every task still unticked in the change's `tasks.md` at the branch head, found at `openspec/changes/<change>/` or, once archived, the latest `openspec/changes/archive/YYYY-MM-DD-<change>/`.
- **Options**: `--test-cmd` (default `uv run pytest -q`), `--check-cmd` (default `make check`, matching `ship --check`; `none` skips it), `--timeout` per session in seconds (default 3600).
- **Run folder**: `${XDG_STATE_HOME:-~/.local/state}/lockstep-runs/<repository>/<run id>/`, a different root from the guard and commit-check logs, named in no prompt and no environment variable. It holds both prompts, both transcripts (JSON event streams), the hidden tests, every command's output and `summary.json` (C7 trace). `summary.json` counts `peek_reads`: implementer transcript lines that name `lockstep-runs` or the writer's worktree path.
- **Agents**: the only per-agent difference is the session command: `claude -p --output-format stream-json --verbose --permission-mode bypassPermissions` started in the worktree, or `codex exec --json --dangerously-bypass-approvals-and-sandbox -C <worktree>`. Both use the user's subscription when logged in.

Hiding is by placement plus detection, not by a sandbox: a session with full permissions can still search the disk. `peek_reads` makes such a search visible in the record.

## Test seam

- `departures(repo: Path, change: str, base: str) -> dict` returns `{"changed": [...], "outside_tasks": [...], "unticked": [...]}`.
- `run_plan(repo, change, ref, agent, runner, ...)`, `accept_write(...)` and `accept_check(...)` take `runner(agent, prompt, cwd, transcript, timeout) -> int`, the function that runs one agent session, so tests replace it with a fake that writes files and commits; no model is called in tests.
- `agent_command(agent, prompt, cwd, persist) -> (argv, cwd)`.
- `summary.json` keys: `run_id`, `change`, `agent`, `ref`, `branch`, `head`, `accept_before`, `accept` (each `{exit, passed, failed, errors}`; counts parsed from pytest's final line, null for another runner), `check_exit`, `uncommitted`, `departures`, `peek_reads`.

## Out of scope

Trimming `ship` and the shared hooks (the next slice will make `ship` refuse a branch whose recorded `accept check` failed or ran at a different head), copier switches in code2-template, and the two-agent milestone run. Writing the plan (step 1) stays with whoever writes the OpenSpec change.

## Impact

- New `src/lockstep/plan_run.py`; `accept` and `run-plan` branches in `lockstep.check:cli`; tests in `tests/lockstep/test_lockstep_plan_run.py`; spec `openspec/specs/plan-run/spec.md`.
- No change to existing commands.

Plan size: small

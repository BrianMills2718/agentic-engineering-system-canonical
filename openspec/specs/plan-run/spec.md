# plan-run Specification

## Purpose

Run one OpenSpec plan through a Claude or Codex agent with acceptance tests written beforehand by a separate session and hidden from the implementer, and report where the result left the plan's tasks (`lockstep accept write`, `accept check`, `run-plan`; minimal core steps 2 and 4, docs/planning/minimal-core-2026-11-20.md).

## Requirements

### Requirement: A departure report compares the change with its plan

The departure report SHALL list every file changed in commits since `REF` whose repository-relative path does not appear in the change's `tasks.md` as read from `REF` and is neither the `path` of a `layout:` row in `lockstep.yaml` as read from `REF` nor a file one of those rows names in its `tests:`, excluding files under `openspec/`, the OpenSpec spec links `make docs-specs` writes under `docs/specs/`, `lockstep.yaml` itself and the generated `docs/links.json`, and every task line still unticked in the change's `tasks.md` at the branch head, read from `openspec/changes/<change>/` or, once archived, from the latest `openspec/changes/archive/YYYY-MM-DD-<change>/`. It reports and never blocks.

Source: Brian, 2026-11-20: "the goal is to give a well specified plan to an agent on some proejct nad have it faithfulyy and successfully impelemnt it"; report-only, inferred by agent from minimal-core-2026-11-20.md C4 and K5 (a check becomes blocking only after it is shown to catch something).

#### Scenario: A file outside the tasks is listed

- **GIVEN** a change whose `tasks.md` at `REF` names `src/app.py`, and commits since `REF` that changed `src/app.py`, `src/other.py`, `tests/test_new.py` and the change's `tasks.md`
- **WHEN** the departure report runs
- **THEN** it lists `src/other.py` and `tests/test_new.py` as outside the tasks and lists neither `src/app.py` nor the OpenSpec file

#### Scenario: A name added to tasks.md after REF does not count

- **GIVEN** the implementer added `src/other.py` to `tasks.md` in its own commit
- **WHEN** the departure report runs
- **THEN** `src/other.py` is still listed as outside the tasks

#### Scenario: An unticked task is listed, archived or not

- **GIVEN** the change was archived to `openspec/changes/archive/2026-11-20-<change>/` with one `- [x]` line and one `- [ ]` line in its `tasks.md`
- **WHEN** the departure report runs with the change's name
- **THEN** it lists the `- [ ]` line as unticked and not the ticked one

Source: Brian, 2026-11-23: "i approve", item (c) of `docs/planning/back-on-design-2026-11-23.md` (a plan names its files in `layout:` rows); plan `docs/planning/template-layout-2026-11-23.md`, step 3.

#### Scenario: A file planned by a layout row at REF is not listed

- **GIVEN** `lockstep.yaml` at `REF` has a `layout:` row with path `src/planned.py`, `tasks.md` does not name it, and commits since `REF` added `src/planned.py`, changed `lockstep.yaml` and added `src/late.py`, whose row was added after `REF`
- **WHEN** the departure report runs
- **THEN** it lists `src/late.py` and lists neither `src/planned.py` nor `lockstep.yaml`

Source: inferred by agent from the template-layout proof run of 2026-11-23 (docs/evidence/template-layout-proof-2026-11-23/summary.json): the row's own test file and the `docs/specs/` link of the archived spec were listed as departures although the plan named the one and the other is generated.

#### Scenario: A row's test file and a spec link are not listed

- **GIVEN** `lockstep.yaml` at `REF` has a row for `src/planned.py` whose `tests:` names `tests/test_planned.py`, and commits since `REF` added `tests/test_planned.py`, `docs/specs/greeting/spec.md` and `tests/test_other.py`
- **WHEN** the departure report runs
- **THEN** it lists only `tests/test_other.py`

### Requirement: Hidden acceptance tests are written before and run after implementation

`lockstep accept write <change>` SHALL run one headless agent session, in a detached worktree at `REF` that is removed afterwards and with no session history kept on disk, that writes pytest files into the run folder outside every worktree, and SHALL then run those tests once at `REF` and record the result. `lockstep accept check <change>` SHALL, in the implementer's worktree, count uncommitted files, copy the hidden tests into `tests/` without overwriting any file, run the test command, remove the copies, run the check command, write the departure report, and record the head commit, all results and the transcripts in the run folder's `summary.json`. Neither command merges.

Source: Brian, 2026-11-20: "the goal is to give a well specified plan to an agent on some proejct nad have it faithfulyy and successfully impelemnt it"; "we shoudl start with the minimal core". Procedure from the plan-fidelity test of 2026-11-20 (minimal-core-2026-11-20.md section 4, C3), inferred by agent.

#### Scenario: Hidden tests are outside the worktree until the last commit

- **GIVEN** a repository with an OpenSpec change at `REF`, and a fake runner that writes a test file for the writer session and, for the implementer session, asserts that no hidden test file is in its worktree, then commits an implementation
- **WHEN** `accept write`, the implementer session and `accept check` run
- **THEN** the hidden test file is in the run folder's `accept/`, the fake runner's assertion held, the test was run in the worktree and removed from it, the writer worktree is gone, and `summary.json` records `accept` pass and fail counts, `check_exit`, the departure report, `head` and zero uncommitted files

#### Scenario: A hidden test that passes before implementation is flagged

- **GIVEN** a writer session whose test already passes at `REF`
- **WHEN** `accept write` finishes
- **THEN** `summary.json` records `accept_before` with that pass and the command prints a warning naming it

#### Scenario: A name collision is refused

- **GIVEN** the implementer's worktree already has `tests/test_accept_1.py`
- **WHEN** `accept check` runs
- **THEN** it does not overwrite or remove that file, records the collision, and exits non-zero

#### Scenario: Uncommitted work is reported

- **GIVEN** an implementer session that leaves a changed tracked file uncommitted
- **WHEN** `accept check` runs
- **THEN** `summary.json` records `uncommitted` above zero, counted before the hidden tests are copied in

#### Scenario: The implementer is not told where the tests are

- **WHEN** the implementer prompt and environment are built
- **THEN** neither contains the run folder's path, and `summary.json` counts implementer transcript lines naming `lockstep-runs` or the writer worktree's path as `peek_reads`

### Requirement: One driver runs a plan with Claude or Codex

`lockstep run-plan <change> --agent claude|codex` SHALL run `accept write`, then one headless implementer session in a new worktree on branch `impl/<change>-<run id>`, then `accept check`, saving each session's JSON event stream as its transcript, and SHALL print the `ship` command to run next without running it: `uv run ship` when the repository's `pyproject.toml` depends on `agentic-engineering-system` (which installs `ship`), else `ship`. The agent choice SHALL change only the command that starts each session.

Source: Brian, 2026-09-14: "the answer is always yes" (keep Claude Code and Codex in sync; workspace agents/rule-sources.md, Policy `claude-codex-parity`), via minimal-core-2026-11-20.md K6. Inferred by agent, 2026-11-21 (#994): a second user has `ship` only inside the repository's environment.

#### Scenario: Each agent gets its own command

- **WHEN** `agent_command` is built for `codex` and for `claude` with the same prompt and worktree
- **THEN** the codex command is `codex exec --json` with `-C <worktree>`, the claude command is `claude -p --output-format stream-json` started in the worktree, both carry the prompt, and a session that keeps no history adds `--ephemeral` or `--no-session-persistence`

#### Scenario: The driver does not merge

- **GIVEN** a fake runner whose implementer commits
- **WHEN** `run_plan` finishes
- **THEN** the default branch is unchanged, the implementer branch exists, and the printed output contains the `ship` command

#### Scenario: The printed ship command matches the repository

- **GIVEN** one repository whose `pyproject.toml` lists `agentic-engineering-system` and one that does not
- **WHEN** `ship_command` is asked for each
- **THEN** it gives `uv run ship` for the first and `ship` for the second

### Requirement: The agents are told to lay out the planned files

The implementer's prompt and the acceptance-test writer's prompt SHALL say that when `lockstep.yaml` has `layout:` rows, those rows name the files the plan creates or changes, with their exports; the implementer's prompt SHALL tell it to run `uv run lockstep layout` before writing code, so each new planned file starts with its requirement text.

Source: Brian, 2026-11-23: "i approve", item (c) of `docs/planning/back-on-design-2026-11-23.md`; `proposals/one-planning-tool/DESIGN.md` step 3 (`lockstep layout` creates the planned files before code); plan `docs/planning/template-layout-2026-11-23.md`, step 3.

#### Scenario: The implementer is told to run lockstep layout

- **GIVEN** a change name and a check command
- **WHEN** the implementer's and the writer's prompts are built
- **THEN** the implementer's names `uv run lockstep layout` and `layout:`, and the writer's names `layout:`

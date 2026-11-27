## MODIFIED Requirements

### Requirement: Hidden acceptance tests are written before and run after implementation

`lockstep accept write <change>` SHALL run one headless agent session, in a detached worktree at `REF` that is removed afterwards and with no session history kept on disk, that writes pytest files into the run folder outside every worktree, and SHALL then run those tests once at `REF` and record the result. `lockstep accept check <change>` SHALL, in the implementer's worktree, count uncommitted files, copy the hidden tests into `tests/` without overwriting any file, run the test command, remove the copies, run the check command, write the departure report, and record the head commit, all results and the transcripts in the run folder's `summary.json`. Neither command merges.

The hidden-run result SHALL preserve the test command exit status and report the passed, failed, error and skipped counts from a fresh pytest JUnit report for the copied tests. `lockstep accept check` and `lockstep run-plan` SHALL require exit 0, at least one passing hidden case and zero failures or errors before returning success. A missing or unreadable report, no tests or an all-skipped run SHALL fail the acceptance check. A custom `--test-cmd` SHALL continue to receive the copied filenames as arguments and must run pytest with the supplied `PYTEST_ADDOPTS` environment so the check can read its report.

Source: Brian, 2026-11-20: "the goal is to give a well specified plan to an agent on some proejct nad have it faithfulyy and successfully impelemnt it"; "we shoudl start with the minimal core". Procedure from the plan-fidelity test of 2026-11-20 (minimal-core-2026-11-20.md section 4, C3), inferred by agent.

Source: C3 of `docs/planning/minimal-core-2026-11-20.md` requires hidden tests to pass. The evidence rule is inferred by agent from the all-skipped audit reproduction and Brian's 2026-11-26 instruction "make any high confidence imrpvoements".

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

#### Scenario: A zero exit needs evidence of passing hidden tests

- **GIVEN** the check command succeeds and the worktree is clean
- **WHEN** the hidden pytest invocation runs
- **THEN** acceptance succeeds only with a readable fresh report showing a positive passing count and zero failures or errors, and an invocation exit of zero; the receipt shows the skipped count when a report was read

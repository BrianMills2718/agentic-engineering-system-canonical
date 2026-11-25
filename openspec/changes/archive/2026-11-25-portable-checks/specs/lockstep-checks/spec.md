## MODIFIED Requirements

### Requirement: Each check can be set to block, warn or off in lockstep.yaml

`lockstep check <name>` (`trace`, `arch`, `test-first`, `sources`, `docmeta` and the others) SHALL read `checks:` in
`lockstep.yaml` at the repository root, where each check is `block` (the default when absent or when there
is no file), `warn` or `off`; `maintainability`, `helper-reuse` and `mutation` SHALL instead be `off` when absent,
and a bare YAML `on` SHALL mean `block`. A failing `block` check SHALL exit 1; a failing `warn` check SHALL print a
`warning:` line and exit 0; an `off` check SHALL not run, SHALL print `skipped (off)` and exit 0. A value
other than those three, or an unknown check name, SHALL exit 2 naming it. The file's `sources.human_pattern`
(default `brian`), `owner` (no default) and `likec4` (default `1.60.0`) settings SHALL be read from the
same file. `lockstep check` with no name, or only `--repo`, `--base` and `--json`, SHALL keep running the
whole-tree plan check.

Source: Brian, 2026-11-25: "ia prpove yourr ecommednations" (the three checks become Lockstep checks each repository switches on itself, off by default); earlier Brian, 2026-11-11, approving the one-tool design ("i approve single tool desing re d4"; `proposals/one-planning-tool/DESIGN.md`, slice 4: the checks are Lockstep's, each switchable so another repository can adopt them one at a time).

#### Scenario: A missing lockstep.yaml means every check blocks

- **GIVEN** a repository with no `lockstep.yaml` and a spec requirement with no implementer
- **WHEN** `lockstep check trace` runs
- **THEN** it exits 1 and prints `RESULT trace findings=2 exit=1`

#### Scenario: Warn prints a warning and exits zero

- **GIVEN** `checks: {trace: warn}` and a failing trace check
- **WHEN** `lockstep check trace` runs
- **THEN** it prints `warning: trace failed` and exits 0

#### Scenario: Off skips the check and exits zero

- **GIVEN** `checks: {trace: off}`
- **WHEN** `lockstep check trace` runs
- **THEN** it prints `skipped (off)`, runs nothing and exits 0

#### Scenario: Block set explicitly exits one and other checks keep their own mode

- **GIVEN** `checks: {trace: block, docmeta: off}`
- **WHEN** `lockstep check trace` and `lockstep check docmeta` run
- **THEN** trace exits 1 and docmeta is skipped with exit 0

#### Scenario: A bad mode or unknown check is an error

- **GIVEN** `checks: {trace: sometimes}`, or `checks: {nonsense: warn}`
- **WHEN** the settings are read
- **THEN** reading fails naming the value, and `lockstep check trace` exits 2

#### Scenario: Defaults when keys are absent

- **GIVEN** a `lockstep.yaml` with none of `checks`, `sources`, `owner`, `likec4`
- **WHEN** the settings are read
- **THEN** the human pattern is `brian`, the owner is unset and LikeC4 is `likec4@1.60.0`

#### Scenario: LikeC4 pin and owner are read

- **GIVEN** `likec4: 1.70.0` and `owner: Acme`
- **WHEN** the settings are read
- **THEN** LikeC4 is `likec4@1.70.0` and the owner is `Acme`

#### Scenario: Lockstep check without a name still runs the tree check

- **GIVEN** `lockstep check --repo PATH`
- **WHEN** the command runs
- **THEN** the whole-tree plan check runs, as before

#### Scenario: The lockstep command runs a named check

- **GIVEN** an installed Lockstep and a repository failing the trace check
- **WHEN** `lockstep check trace --repo PATH` runs as a process
- **THEN** it prints the trace RESULT line and exits 1

#### Scenario: The three switched-on checks are off when absent

- **GIVEN** a `lockstep.yaml` that does not name `maintainability`, `helper-reuse` or `mutation`
- **WHEN** the settings are read
- **THEN** those three are `off` and `trace` is `block`; `mutation: on` reads as `block`, and `mutation.issue_repo` and
  `mutation.name` are read (an `issue_repo` that is not `OWNER/NAME` is an error)

## ADDED Requirements

### Requirement: Maintainability: Only findings the branch adds fail

`lockstep check maintainability --base <rev>` SHALL compare the merge base with the working tree over the Python
files under `--folders` (default `src,scripts`) and exit 1 only on a finding the branch adds: a blind `except` or
`try/except/pass` (ruff BLE, S110, S112), a function over the complexity limit more complex than on the base (C901),
more repeated 6-line windows of code, or a file over `--max-lines` (default 800) that grew. It SHALL end with
`RESULT maintainability new=<n> base_findings=<n> head_findings=<n> exit=<0|1>`, SHALL exit 0 with a `skipped=` line
when the base is missing or no Python file changed, and SHALL exit 2 when a tool fails.

Source: Brian, 2026-11-24 (Reddit-ideas plan, slice 3: "i will trust your jdugement on the impelemtnation prirotiy"; an AES script until now) and Brian, 2026-11-25: "ia prpove yourr ecommednations" (moved into Lockstep)

#### Scenario: Maintainability: Only findings the branch adds fail

- **GIVEN** a branch that adds a blind `except`, raises a function's complexity, adds a third copy of a block, or
  grows a large file
- **WHEN** `lockstep check maintainability --base main` runs
- **THEN** it exits 1 naming the finding; a finding already on the base, moved or renamed, passes

### Requirement: Maintainability: Off unless switched on

`maintainability` SHALL be a check name in `lockstep.yaml`, `off` when absent, so a repository runs it only after
setting it to `block` or `warn`; the template's `make check` SHALL call it, printing `maintainability: skipped (off)`
until then.

Source: Brian, 2026-11-25: "ia prpove yourr ecommednations"

#### Scenario: Maintainability: Off unless switched on

- **GIVEN** a branch adding a blind `except` and no `maintainability` in `lockstep.yaml`
- **WHEN** `lockstep check maintainability` runs, then runs again after `checks: {maintainability: block}`
- **THEN** the first prints `maintainability: skipped (off)` and exits 0; the second exits 1 with its RESULT line

### Requirement: Helper reuse: Flags a rewrite of an existing function

`lockstep check helper-reuse --base <rev>` SHALL send the index of every function on the merge base and each
function the branch adds to a light model through `llm_client`, then judge each new function against up to three
named candidates (same_job, partial_overlap, different), and SHALL end with `RESULT helper-reuse new_functions=<n>
flagged=<n> cost_usd=<x> exit=<0|1>`, exiting 1 on same_job and 2 when a call or step fails. Its prompt templates
SHALL ship inside the Lockstep package.

Source: Brian, 2026-11-24 (Reddit-ideas plan, slice 3; an AES script until now) and Brian, 2026-11-25: "ia prpove yourr ecommednations" (moved into Lockstep)

#### Scenario: Helper reuse: Flags a rewrite of an existing function

- **GIVEN** a branch adding a function that does the job of an existing one under a new name
- **WHEN** the check runs with the model's answers given
- **THEN** it prints `same_job` for the pair and exits 1; a function with a new job passes

### Requirement: Helper reuse: Off unless switched on and needs llm_client

`helper-reuse` SHALL be `off` when absent from `lockstep.yaml`. When it is on and `llm_client` cannot be imported,
`lockstep check helper-reuse` SHALL print how to run it with llm_client's Python and
`RESULT helper-reuse tool-failed=llm_client-missing exit=2`, and exit 2.

Source: Brian, 2026-11-25: "ia prpove yourr ecommednations"

#### Scenario: Helper reuse: Off unless switched on and needs llm_client

- **GIVEN** no `helper-reuse` in `lockstep.yaml`, then `checks: {helper-reuse: block}` in a Python without llm_client
- **WHEN** `lockstep check helper-reuse` runs each time
- **THEN** the first is skipped with exit 0; the second prints the install hint and exits 2

### Requirement: Mutation: Lists surviving mutants per repository

`lockstep check mutation [--timeout S]` SHALL run `mutmut run` in the repository (mutmut from its `.venv/bin`, else
PATH; what to mutate from its `[tool.mutmut]`), read `mutmut results --all true`, print one `<module>: <n> survived`
line per module and end with `mutation: <n> survived, <n> killed[, <n> <status>] of <n> mutants in <s>s (<name>)`,
where `<name>` is `mutation.name` in `lockstep.yaml`, else the origin repository's name.

Source: Brian, 2026-11-24: "i approve adding the redit ideas to the plan" (code2-workspace mutation-nightly) and Brian, 2026-11-25: "ia prpove yourr ecommednations" (moved into Lockstep)

#### Scenario: Mutation: Lists surviving mutants per repository

- **GIVEN** mutmut results with survivors in two modules
- **WHEN** the check runs
- **THEN** it prints each module's survived count, most first, and the summary line

### Requirement: Mutation: Survivors are a report and a broken run is a failure

The mutation check SHALL exit 0 when mutmut finished or was stopped at the time limit, survivors or not, and 2 when
mutmut is missing, fails (naming any test that failed in mutmut's copy), gives no results, or was stopped at the limit
twice running without fewer mutants left unchecked. A run stopped at the limit SHALL stop mutmut's whole process group,
and a results file cut off by the stop SHALL be set aside so mutmut checks those mutants again. In `warn` mode the 2
becomes 0 with a warning, so a nightly run SHALL use `block`.

Source: Brian, 2026-11-24 (code2-workspace mutation-nightly) and Brian, 2026-11-25: "ia prpove yourr ecommednations"

#### Scenario: Mutation: Survivors are a report and a broken run is a failure

- **GIVEN** a run with survivors, a run where a test fails in mutmut's copy, and two stopped runs with no progress
- **WHEN** the check runs
- **THEN** the first exits 0, the second exits 2 naming the test, the second stopped run exits 2

### Requirement: Mutation: One agent issue carries the survivors

With `--issue`, the mutation check SHALL first rerun the shown survivors by name, then keep one open `owner:agent`
issue titled `Mutation testing: code changes <name>'s tests let pass` in `mutation.issue_repo` (default: the origin
repository): open it when none is open and something survived, comment when the survived counts per module changed,
and leave it otherwise, with up to 30 diffs under GitHub's body limit.

Source: Brian, 2026-11-24 (code2-workspace mutation-nightly) and Brian, 2026-11-25: "ia prpove yourr ecommednations"

#### Scenario: Mutation: One agent issue carries the survivors

- **GIVEN** survivors on three runs, the third with one more
- **WHEN** the check runs with `--issue` each time
- **THEN** the first opens the issue, the second leaves it, the third comments on it

### Requirement: Mutation: Off unless switched on and set per repository

`mutation` SHALL be `off` when absent from `lockstep.yaml`. Its last survivors and progress SHALL be kept per
repository under `<git-common-dir>/lockstep-mutation/`, and `mutation.issue_repo` and `mutation.name` SHALL set where
the issue goes and the name in its title and summary.

Source: Brian, 2026-11-25: "ia prpove yourr ecommednations" (directive: issue repository from `lockstep.yaml`, default origin; AES sets code2-workspace)

#### Scenario: Mutation: Off unless switched on and set per repository

- **GIVEN** no `mutation` in `lockstep.yaml`, then `checks: {mutation: block}` with `mutation: {issue_repo: Acme/tracker, name: Widget}`
- **WHEN** `lockstep check mutation --issue` runs each time
- **THEN** the first is skipped and runs nothing; the second opens `Mutation testing: code changes Widget's tests let
  pass` in `Acme/tracker` and keeps its state in the repository's git folder

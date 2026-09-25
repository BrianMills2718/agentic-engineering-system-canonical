# Getting started with AES in a new project

AES keeps a project's accepted target in `.aes/target.yaml`: what the project
is for (outcomes), the rules it must obey (normative items), how you would know
it works (success criteria and their evidence requirements), which files are
supposed to exist (planned artifacts) and which checks prove the criteria
(verification subjects). The `aes` command checks that the target is
consistent, that every file under the governed directories is planned, and
which criteria current evidence supports.

This page takes a new Python project from nothing to one recorded piece of
evidence. You need Git, Python 3.11 or newer, and read access to the AES
repository on GitHub.

## 1. Create the project and install AES

```bash
mkdir greeter && cd greeter
git init -q
python3 -m venv .venv
. .venv/bin/activate
pip install -q pytest "agentic-engineering-system @ git+https://github.com/BrianMills2718/agentic-engineering-system-canonical.git@<sha>"
aes --version
```

Replace `<sha>` with the AES commit you want to pin. To find the current one,
run `git ls-remote https://github.com/BrianMills2718/agentic-engineering-system-canonical.git main`
and use the full 40-character id it prints (a short id works, but pip warns).
`aes --version` then names that commit inside its version string, e.g.
`0.1.dev367+g0503735f9`. Keep the virtual environment and caches out of Git, and let
pytest import the project's own source:

```bash
printf '.venv/\n__pycache__/\n' > .gitignore
cat > pyproject.toml <<'TOML'
[tool.pytest.ini_options]
pythonpath = ["src"]
TOML
```

## 2. Initialize

Run `aes init` at the top of the repository with the project's first outcome:
who it is for, and what they get.

```bash
aes init --project-id greeter \
  --actor "a script author who needs a greeting" \
  --outcome "Calling greet with a name returns a greeting that contains that name."
```

This writes exactly two files, `.aes/project.yaml` and `.aes/target.yaml`, and
nothing else. It refuses outside a Git repository, below the top of the
repository, and when `.aes/` already exists. By default the governed
directories are `src/` and `tests/`; pass `--governed-root DIR` (repeatable)
to choose others. From now on every `aes` command finds the project from any
subdirectory or linked worktree; `--root DIR` overrides that.

Install the pre-commit hook, which refuses a commit when the target does not
validate or when a file under a governed directory is not planned:

```bash
aes hooks install
git add .gitignore pyproject.toml .aes .githooks
git commit -q -m "Initialize AES"
```

## 3. Plan the work: propose, validate, accept

The initial target holds only the outcome. Plan one chain from the outcome to
a test before writing code: outcome `OUT-001` → normative item `NI-001` →
success criterion `SC-001` with evidence requirement `ER-001-01` → planned
artifacts for the code and the test → verification subject `VS-GREET`, which
says which test proves the requirement.

You write that as a proposal: the entries to add to the target, plus the ids
of the open gaps it closes. `aes plan prepare` prints what to write against:
the open gaps (none yet, on a new target), every id the target already
declares, and an empty proposal (`proposal_skeleton`) to copy.

```bash
aes plan prepare
```

```text
schema_version: aes.v0_2.plan_input.probe0
target_id: greeter-target
subject_revision: 8801d313294da670343e300c6ceb7a39d3085c0a
dirty: false
governed_roots:
  - src/
  - tests/
open_gaps: []
unrouted_evidence_requirements: []
target_ids:
  outcomes:
    - OUT-001
...
```

Write the proposal outside `.aes/`:

```bash
cat > plan-greeter.yaml <<'YAML'
schema_version: aes.v0_2.proposal.probe0
proposal_id: PLAN-001-GREET
title: Greet by name
rationale: >
  OUT-001 has nothing planned under it yet. This plans one chain from the
  outcome to a test before any code is written.
closes_gaps: []
target_delta:
  add:
    normative_items:
      - id: NI-001
        kind: behavior
        outcome_refs: [OUT-001]
        statement: >
          greet(name) returns "Hello, <name>!" and rejects an empty name with
          ValueError instead of greeting nobody.
    success_criteria:
      - id: SC-001
        statement: greet greets a given name and refuses an empty one.
        target_refs: [NI-001]
        disproof: >
          greet returns a string without the name, or returns anything for an
          empty name.
        evidence_requirements:
          - id: ER-001-01
            kind: deterministic_test
            requirement: >
              A test calls greet("Ada") and checks the exact greeting, and checks
              that greet("") raises ValueError.
    components:
      - id: CMP-GREETER
        responsibility: produce greetings
        target_refs: [NI-001]
        planned_artifact_refs: [ART-PKG, ART-TEST-GREET]
    planned_artifacts:
      - id: ART-PKG
        locator: {exact_path: src/greeter/__init__.py}
        kind: source
        purpose: the greet function
        semantic_justification_refs: [NI-001]
      - id: ART-TEST-GREET
        locator: {exact_path: tests/test_greet.py}
        kind: test
        purpose: prove SC-001
        semantic_justification_refs: [SC-001]
    verification_subjects:
      - id: VS-GREET
        criterion_refs: [SC-001]
        evidence_requirement_refs: [ER-001-01]
        proof_kind: deterministic_test
        proof_role: direct
        locator: tests/test_greet.py
        purpose: prove greet greets a name and refuses an empty one
YAML
aes plan validate plan-greeter.yaml
```

`aes plan validate` applies the proposal to a copy of the target in memory
and lists every problem at once. Without the `verification_subjects` entry,
for example, it refuses because nothing would ever prove the requirement:

```text
error: proposal PLAN-001-GREET: 1 violation(s):
  - evidence requirement 'ER-001-01' (criterion 'SC-001') has no route: no verification subject names it in evidence_requirement_refs and external_boundaries does not list it
```

With it:

```text
OK proposal PLAN-001-GREET: 6 addition(s), 0 change(s)
  closes: no current gap (target extension)
  resulting target: success_criteria=1 evidence_requirements=1 verification_subjects=1 external_boundaries=0; every evidence requirement has a route
```

Accept it, then commit the target and the plan together:

```bash
aes plan accept plan-greeter.yaml
rm plan-greeter.yaml
git add .aes
git commit -q -m "Plan PLAN-001-GREET"
```

```text
accepted at 8801d313294da670343e300c6ceb7a39d3085c0a
  added normative_items NI-001
  added success_criteria SC-001
  added components CMP-GREETER
  added planned_artifacts ART-PKG
  added planned_artifacts ART-TEST-GREET
  added verification_subjects VS-GREET
  updated .aes/target.yaml
  wrote .aes/plans/PLAN-001-GREET.yaml
  next: git add .aes/target.yaml .aes/plans/PLAN-001-GREET.yaml && git commit, then implement
```

`aes plan accept` refuses while the working tree has uncommitted changes, when
the proposal does not validate, and when a plan with the same id was already
accepted. It edits `.aes/target.yaml` in place (comments and order kept, new
entries at the end of their list) and keeps the proposal, with the commit it
was accepted at, in `.aes/plans/`. It does not commit. The full protocol,
including how to change an existing entry, is in
`src/agentic_engineering_system/planning_protocol.md` in the AES repository.
Editing `.aes/target.yaml` by hand still works; the hook checks the result
either way.

The pre-commit hook ran `aes target validate` and `aes topology check` on the
plan commit; the topology check lists both planned files as `unrealized`
(planned, not yet written), which is not a failure. `aes target validate`
loads the target strictly: an unknown field, a duplicate key or ID, or a
reference to an ID that does not exist fails with its location.

`aes context` prints what someone working on one ID needs to know: the chain
above and below it, with the source of each line.

```bash
aes context SC-001
```

## 4. Write the planned files and commit

```bash
mkdir -p src/greeter tests
cat > src/greeter/__init__.py <<'PY'
def greet(name: str) -> str:
    if not name:
        raise ValueError("name must not be empty")
    return f"Hello, {name}!"
PY
cat > tests/test_greet.py <<'PY'
import pytest

from greeter import greet


def test_greets_the_name() -> None:
    assert greet("Ada") == "Hello, Ada!"


def test_refuses_an_empty_name() -> None:
    with pytest.raises(ValueError):
        greet("")
PY
git add src tests
git commit -q -m "Greet by name"
```

The hook ran `aes target validate` and `aes topology check` on that commit. A
file under `src/` or `tests/` that no planned artifact names would have
stopped it, with the file named in the error.

## 5. Record evidence and read the standing

```bash
aes evidence record VS-GREET --depends-on src/greeter/__init__.py
aes evidence status
git add .aes/observations
git commit -q -m "Record VS-GREET"
```

`aes evidence record` runs the subject's test at the current commit (for
Python: `pytest` on the locator) and writes an observation under
`.aes/observations/` naming the commit, the command, the result, and the
files the result depends on: the test itself plus each `--depends-on` path.
It refuses while any of those files has uncommitted changes.

`aes evidence status` then reports `SC-001` as `SUPPORTED`. When a file listed
in the observation changes in a later commit, the observation becomes `STALE`
and the criterion goes back to `INSUFFICIENT` until you record it again. A
failing test is recorded as `REFUTES`, which makes the criterion `REFUTED`.

## 6. See the whole state and what is still open

```bash
aes status
```

`aes status` puts everything above on one screen: the commit it describes,
counts of planned artifacts (realized, unrealized, drifted), orphans, criteria
by standing and observations by freshness, then the first open gap of each
component. On the example at this point (your commit id will differ):

```text
OK status: greeter-target at 3dff1d43a241da11863d7b9280edc2d627bfe6fd
  artifacts: 2 realized, 0 unrealized, 0 drifted; 0 orphan(s)
  criteria: 1 supported, 0 insufficient, 0 refuted; 0 unsupported evidence requirement(s) with no route
  observations: 1 current, 0 stale, 0 unknown
  first open gap per component:
    CMP-GREETER: no open gap
  INSUFFICIENT criteria are normal while work is in progress and do not fail this command; a REFUTED criterion, an orphan or drift does.
```

Change `src/greeter/__init__.py` (say, `Hello` to `Hi`) and commit it, and
the gap re-opens: the observation depended on that file, so it is stale and
`SC-001` has no current support.

```text
OK status: greeter-target at e70b01d9a3e2181f0aaabbf5f0ad72a5a8ac3b2a
  artifacts: 2 realized, 0 unrealized, 0 drifted; 0 orphan(s)
  criteria: 0 supported, 1 insufficient, 0 refuted; 0 unsupported evidence requirement(s) with no route
  observations: 0 current, 1 stale, 0 unknown
  first open gap per component:
    CMP-GREETER: insufficient SC-001 - ER-001-01 NO_CURRENT_SUPPORT
  INSUFFICIENT criteria are normal while work is in progress and do not fail this command; a REFUTED criterion, an orphan or drift does.
```

`aes reconcile` prints the full report behind that screen: every planned
artifact with its status, every criterion with the evidence requirements it
is missing and the verification subjects that could supply each one (`NO
ROUTE` when none does), every observation's freshness, orphans, and all gaps
per component; `--json` prints the same as one JSON document. Both commands
exit 1 on a `REFUTED` criterion, an orphan, or drift from a committed export,
and 0 otherwise. Nothing is stored: every run recomputes the state from the
target, the repository at `HEAD` and the observations, so a gap closes only
through a new observation or a change to the code or the target.

## Commands

| Command | What it does |
| --- | --- |
| `aes init --project-id ID --actor TEXT --outcome TEXT` | create `.aes/project.yaml` and a target holding the first outcome |
| `aes hooks install` | install the pre-commit gate |
| `aes target validate` | strictly load and check the target |
| `aes topology check` | fail on any tracked governed file the target does not plan |
| `aes plan prepare [--out FILE]` | open gaps, existing ids and an empty proposal to write against |
| `aes plan validate FILE` | apply a proposal in memory and list every violation |
| `aes plan accept FILE` | apply a valid proposal to the target and keep it in `.aes/plans/` (no commit) |
| `aes context ID` | compile the working context for one ID |
| `aes evidence record VS-ID [--depends-on PATH]` | run a test subject and write its observation |
| `aes evidence status` | standing of every success criterion |
| `aes status` | one screen: counts and the first open gap per component |
| `aes reconcile [--json]` | full current state and every open gap |

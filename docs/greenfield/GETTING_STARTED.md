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

Replace `<sha>` with the AES commit you want to pin; `aes --version` then
names that commit. Keep the virtual environment and caches out of Git, and let
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

## 3. Plan the work in `.aes/target.yaml`

The initial target holds only the outcome. Open `.aes/target.yaml` and replace
the empty lists so that one chain runs from the outcome to a test: outcome
`OUT-001` → normative item `NI-001` → success criterion `SC-001` with evidence
requirement `ER-001-01` → planned artifacts for the code and the test →
verification subject `VS-001`, which says which test proves the requirement.

```bash
cat > .aes/target.yaml <<'YAML'
schema_version: aes.v0_2.target.probe0
target_id: greeter-target

outcomes:
  - id: OUT-001
    actor_or_consumer: a script author who needs a greeting
    statement: Calling greet with a name returns a greeting that contains that name.

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
aes target validate
aes topology check
```

`aes target validate` loads the file strictly: an unknown field, a duplicate
key or ID, or a reference to an ID that does not exist fails with its
location. `aes topology check` lists both planned files as
`unrealized` (planned, not yet written), which is not a failure.

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
git add .aes/target.yaml src tests
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

## Commands

| Command | What it does |
| --- | --- |
| `aes init --project-id ID --actor TEXT --outcome TEXT` | create `.aes/project.yaml` and a target holding the first outcome |
| `aes hooks install` | install the pre-commit gate |
| `aes target validate` | strictly load and check the target |
| `aes topology check` | fail on any tracked governed file the target does not plan |
| `aes context ID` | compile the working context for one ID |
| `aes evidence record VS-ID [--depends-on PATH]` | run a test subject and write its observation |
| `aes evidence status` | standing of every success criterion |

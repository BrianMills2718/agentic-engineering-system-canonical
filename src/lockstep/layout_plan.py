"""The layout plan: OpenSpec says what the code must do, `layout:` rows in lockstep.yaml say which files exist and why.

Implements: lockstep-plan-format/the-plan-is-openspec-plus-layout-rows, lockstep-plan-format/a-layout-row-lists-what-its-file-implements

Requirement text (generated):
    lockstep-plan-format/the-plan-is-openspec-plus-layout-rows: In a repository whose
        `lockstep.yaml` has a `layout:` list and which has no `.aes/target.yaml`, Lockstep SHALL
        take the planned files from the `layout:` rows (path, purpose, the OpenSpec requirements it
        implements, its tests, optionally its typed exports), the governed folders from `governed:`,
        and the requirement text from OpenSpec. A `governed:` entry ending in `/` covers every path
        under it, `.` covers the whole repository, and any other entry covers that one file or a
        folder of that name. A repository with `.aes/target.yaml` SHALL be read as before.

This is the one plan format of the one-tool design (proposals/one-planning-tool/DESIGN.md, slice 2). A repository
without `.aes/target.yaml` writes its plan as:

    governed: [src/]                     # folders where every file must be planned
    layout:
      - path: src/greeter/__init__.py    # the file
        purpose: the greet function      # why it exists
        implements: [greeting/greet-by-name]   # OpenSpec requirement IDs (<capability>/<requirement slug>)
        tests: [tests/test_greet.py]     # the tests that prove it
        exports: ["greet(name: str) -> str"]   # optional: its typed public signatures

`aes_bridge` reads this through `target_from_layout` and `layout_context`, so the edit hook, `lockstep check` and
`lockstep layout` work on it as they work on an AES plan. Each row's artifact ID is its path with `/` written as
`:` (`artifact_id`), so a docstring's cog block can name it.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:layout_plan.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-plan-format/the-plan-is-openspec-plus-layout-rows

### Requirement: The plan is OpenSpec plus layout rows

In a repository whose `lockstep.yaml` has a `layout:` list and which has no `.aes/target.yaml`, Lockstep SHALL take the
planned files from the `layout:` rows (path, purpose, the OpenSpec requirements it implements, its tests, optionally
its typed exports), the governed folders from `governed:`, and the requirement text from OpenSpec. A `governed:` entry
ending in `/` covers every path under it, `.` covers the whole repository, and any other entry covers that one file or
a folder of that name. A repository with
`.aes/target.yaml` SHALL be read as before.

Source: Brian, 2026-11-11, approving the one-tool design as written ("i approve single tool desing re d4"; `proposals/one-planning-tool/DESIGN.md`, slice 2: "Lockstep reads requirements from OpenSpec ... and layout from `lockstep.yaml`. `.aes/target.yaml` stays readable until lifelike and Team-Brains move off it"). How a `governed:` entry matches (`/`, `.`, a file or folder name) inferred by agent, 2026-11-24, after a review found a bare `Makefile` entry covered `Makefile.bak` and a list of top-level names missed a new top-level file.

#### Scenario: The layout is laid out with first docstrings

- **GIVEN** a layout row for `src/greeter/__init__.py` implementing `greeting/greet-by-name`, tested by `tests/test_greet.py`
- **WHEN** `lockstep layout` runs
- **THEN** the file is created with a docstring holding its `Implements:` line, the requirement and its scenarios word for word, the test names and its declared signature, and an existing file is left as it is

#### Scenario: An unplanned file is refused against the layout

- **GIVEN** `governed: [src/]` and no row for `src/greeter/extra.py`
- **WHEN** an agent writes that file under `PCW_MODE=block`
- **THEN** the edit hook refuses it and names `lockstep.yaml` as where the file must be planned

#### Scenario: A planned file's edit hands over its requirement

- **GIVEN** a laid-out planned file
- **WHEN** an agent edits it
- **THEN** the edit is allowed and the agent is handed the OpenSpec requirement text

#### Scenario: The whole-tree check reads the layout

- **GIVEN** a laid-out, committed layout repository
- **WHEN** `lockstep check` runs, and again after an unplanned file is added under `src/`
- **THEN** the first allows and the second blocks with that file as `unplanned`

#### Scenario: A layout row must name real requirements

- **GIVEN** a row whose `implements` names a requirement no spec defines, and a row with no purpose
- **WHEN** the layout is checked
- **THEN** both are reported, naming the row's path

#### Scenario: A governed entry covers what it names

- **GIVEN** `governed:` entries `src/`, `.`, `Makefile` and `src/lockstep`
- **WHEN** paths are matched against each
- **THEN** `src/` covers `src/a/b.py` but not `srcx/b.py`, `.` covers every path, `Makefile` covers `Makefile` but not `Makefile.bak`, and `src/lockstep` covers `src/lockstep/x.py` but not `src/lockstep_old.py`

#### Scenario: An AES plan is still read

- **GIVEN** a repository with `.aes/target.yaml`
- **WHEN** Lockstep reads its plan
- **THEN** the planned files come from `.aes/target.yaml` exactly as before

Tested by: tests/lockstep/test_lockstep_layout_plan.py
[[[end]]]
"""

from __future__ import annotations

from pathlib import Path

import yaml

from lockstep.checks.markers import implementers
from lockstep.openspec_text import read_requirements

SIDE_FILE = "lockstep.yaml"
SOURCE = "lockstep.yaml layout and OpenSpec"


def _data(root: Path) -> dict:
    path = root / SIDE_FILE
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def has_layout(root: Path) -> bool:
    """True when `root` has lockstep.yaml with a `layout:` list and no AES plan, so the layout is the plan."""
    return not (root / ".aes" / "target.yaml").is_file() and isinstance(_data(root).get("layout"), list)


def artifact_id(path: str) -> str:
    """A layout row's artifact ID: its path with `/` written as `:` (cog block IDs cannot hold `/`)."""
    return path.replace("/", ":")


def _kind(path: str) -> str:
    name = path.rsplit("/", 1)[-1]
    return "test" if path.startswith("tests/") or name.startswith("test_") else "source"


def _list(value: object) -> list[str]:
    return [str(v).strip() for v in value if str(v).strip()] if isinstance(value, list) else []


def layout_rows(root: Path) -> list[dict]:
    """The `layout:` rows, each as {path, purpose, implements, tests, exports}; rows without a path are skipped."""
    rows = []
    for row in _data(root).get("layout") or []:
        if isinstance(row, dict) and str(row.get("path") or "").strip():
            rows.append({"path": str(row["path"]).strip(), "purpose": str(row.get("purpose") or "").strip(),
                         "implements": _list(row.get("implements")), "tests": _list(row.get("tests")),
                         "exports": _list(row.get("exports"))})
    return rows


def governed(root: Path) -> list[str]:
    """The `governed:` folders: every file under one must be a layout row."""
    return _list(_data(root).get("governed"))


def layout_problems(root: Path) -> list[str]:
    """Each way the layout fails to be a plan: a row with no purpose, a repeated path, an unknown requirement, or a
    row that leaves out a requirement its own file names in an `Implements:` line."""
    problems: list[str] = []
    known = read_requirements(root)
    raw = _data(root).get("layout")
    if not isinstance(raw, list):
        return [f"{SIDE_FILE} has no `layout:` list"]
    seen: set[str] = set()
    for n, row in enumerate(raw, 1):
        path = str(row.get("path") or "").strip() if isinstance(row, dict) else ""
        if not path:
            problems.append(f"{SIDE_FILE} layout row {n} has no path")
            continue
        if path in seen:
            problems.append(f"{SIDE_FILE} lists {path} twice")
        seen.add(path)
        if not str(row.get("purpose") or "").strip():
            problems.append(f"{SIDE_FILE} layout row for {path} has no purpose: say why the file exists")
        for ident in _list(row.get("implements")):
            if ident not in known:
                problems.append(f"{SIDE_FILE} layout row for {path} implements {ident}, which no OpenSpec spec or "
                                "active change defines (openspec/specs/<capability>/spec.md)")
    problems += _rows_missing_their_code(root, raw)
    return problems


def _rows_missing_their_code(root: Path, raw: list) -> list[str]:
    """Rows whose file's `Implements:` lines name a requirement the row's `implements` leaves out."""
    named: dict[str, set[str]] = {}
    for ident, where, *_ in implementers(root):
        named.setdefault(where.rsplit(":", 1)[0], set()).add(ident)
    problems = []
    for row in raw:
        path = str(row.get("path") or "").strip() if isinstance(row, dict) else ""
        missing = sorted(named.get(path, set()) - set(_list(row.get("implements")) if path else []))
        if path and missing:
            problems.append(f"{SIDE_FILE} layout row for {path} leaves out {', '.join(missing)}, which the file says "
                            "it implements: add them to the row's `implements`, or drop the `Implements:` line")
    return problems


def target_from_layout(root: Path) -> dict:
    """The layout as the plan dict the rest of Lockstep reads (the `planned_artifacts` shape of an AES target)."""
    return {"governed_roots": governed(root),
            "planned_artifacts": [{"id": artifact_id(r["path"]), "locator": {"exact_path": r["path"]},
                                   "kind": _kind(r["path"]), "purpose": r["purpose"],
                                   "semantic_justification_refs": r["implements"], "exports": r["exports"],
                                   "tests": r["tests"]}
                                  for r in layout_rows(root)]}


def layout_context(root: Path, subject: str) -> dict:
    """What a planned file's docstring copies: its requirements word for word, its tests and its signatures.

    Raises RuntimeError for an ID no row has, as `aes context` does for an unknown ID.
    """
    row = next((r for r in layout_rows(root) if artifact_id(r["path"]) == subject), None)
    if row is None:
        raise RuntimeError(f"no layout row in {SIDE_FILE} has the artifact ID {subject}")
    known = read_requirements(root)
    return {"source": SOURCE, "subject": {"id": subject, "exports": row["exports"]},
            "implements": row["implements"],
            "requirements": [(ident, known.get(ident, f"{ident}: no OpenSpec requirement has this ID"))
                             for ident in row["implements"]],
            "tests": row["tests"]}

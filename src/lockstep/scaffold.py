"""`python -m lockstep.scaffold`: create every file the plan declares that does not exist yet.

Each new source or test file gets a module docstring holding a cog block for
its planned artifact, so `make project` can write the plan's words into it.
Existing files are never touched. Prints what it created.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:scaffold.py", indent=0)]]]
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
[[[end]]]
"""

from __future__ import annotations

import sys
from pathlib import Path

from lockstep.aes_bridge import find_root, target
from lockstep.cogtext import CLOSE, END, OPEN

STUB = '''"""{purpose}

{open} import lockstep.cogtext as c; c.docstring("{art}", indent=0){close}
{end}
"""
'''


def main() -> int:
    root = find_root(Path.cwd())
    if root is None:
        print("scaffold: no .aes/project.yaml or lockstep.yaml layout here or above", file=sys.stderr)
        return 1
    made = []
    for art in target(root).get("planned_artifacts") or []:
        rel = (art.get("locator") or {}).get("exact_path")
        if not rel or not rel.endswith(".py"):
            continue
        path = root / rel
        if path.exists():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(STUB.format(purpose=art.get("purpose", "").capitalize() + ".", art=art["id"], open=OPEN, close=CLOSE, end=END))
        made.append(f"{rel}  ({art['id']})")
    print("scaffold: created\n  " + "\n  ".join(made) if made else "scaffold: every planned file already exists")
    return 0


def layout() -> int:
    """`lockstep layout`: create every planned file that does not exist yet, then fill its docstring from the plan.

    The files are created as `main` creates them, then cog writes each new file's plan text (its requirements, success
    criteria, tests and signatures) into the block; an existing file is never touched.
    """
    from cogapp import Cog

    root = find_root(Path.cwd())
    if root is None:
        return main()  # it says why there is nothing to lay out
    missing = sorted(p for p in _planned_py(root) if not (root / p).exists())
    code = main()
    if code or not missing:
        return code
    return Cog().main(["cog", "-r", "-c", *(str(root / p) for p in missing)])


def _planned_py(root: Path) -> list[str]:
    return [rel for art in target(root).get("planned_artifacts") or []
            if (rel := (art.get("locator") or {}).get("exact_path")) and rel.endswith(".py")]


if __name__ == "__main__":
    raise SystemExit(main())

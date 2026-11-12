"""The layout plan: OpenSpec says what the code must do, `layout:` rows in lockstep.yaml say which files exist and why.

Implements: lockstep-plan-format/the-plan-is-openspec-plus-layout-rows

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
"""

from __future__ import annotations

from pathlib import Path

import yaml

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
    """Each way the layout fails to be a plan: a row with no purpose, a repeated path, an unknown requirement."""
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

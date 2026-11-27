"""Read and check Lockstep's side file, `lockstep.yaml` beside the plan (behaviors 1.1, 2.1 and 5.1).

The AES plan declares code, tests and configuration, but it has no place for a document and no
evidence kind for an AI-graded rubric. Lockstep keeps both in one small file at the project root
(decision D16, question Q36):

    schema: lockstep.side.v1
    documents:
      include: ["*.md"]           # which files count as documents (glob, matched from the right)
      declared:
        - path: README.md
          purpose: the front door   # why the document exists
          refs: [REQ-6]             # the plan items it serves; each must exist in .aes/target.yaml
    files:                          # optional: every other file (scripts, data, config), so every
      - path: "scripts/*.py"        # tracked file has a declared reason (question Q48); a glob or a path
        purpose: tooling the review page is built with
        refs: [REQ-7]
    rubrics:
      - criterion: SC-2.1           # a success criterion in the plan
        rubric: what an AI grader reads the work against
    actions:                        # optional: non-code actions a proposal may name (behavior 5.4,
      - id: ACT-BOARD-STATUS        # read by lockstep.action_check)
        kind: board_update
        target: Owner/Repo#12
        purpose: post the status line on the tracking issue
        refs: [REQ-5]
    fixed: ["src/core/*"]           # files the edit hook refuses rather than warns about (behavior 5.1)
    guard: {mode: block}            # optional: block or warn for every governed file; absent means warn

`guard.mode` sets the edit hook's mode for the whole project; a set `PCW_MODE` environment variable wins over it
(`guard_mode`; a value that is other than block, warn or off reads as block).

`fixed` holds path globs matched against the whole project-relative path (`fnmatch`, so `*` also
crosses `/`). The edit hook only warns by default (decision D7); a file matching one of these globs
gets the refusal instead. A project with no side file has no document rule, no rubrics and no fixed
files. The file is data read with
`yaml.safe_load`; nothing in it is executed. `load_side_file` keeps the well-formed entries;
`side_file_problems` names everything else (unknown keys, duplicates, an empty purpose or rubric,
a reference the plan does not hold), and `python -m lockstep.unplanned_files` fails on any of them.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:side_file.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Names no requirement; the layout row says why.
[[[end]]]
"""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import yaml

from lockstep.aes_bridge import committed_text

SIDE_FILE = "lockstep.yaml"
SCHEMA = "lockstep.side.v1"
_TOP = {"schema", "documents", "rubrics", "fixed", "files", "actions",  # actions: read by lockstep.action_check (behavior 5.4)
        "checks", "sources", "owner", "likec4", "mutation",  # the commit checks (lockstep.checks)
        "planning", "guard", "rules", "feedback",  # the parts' settings (docs/planning/next.goal.md)
        "layout", "governed", "projections", "source_base_url"}  # the layout plan (lockstep.layout_plan)
_DOCUMENTS = {"include", "declared"}
_DOCUMENT = {"path", "purpose", "refs"}
_RUBRIC = {"criterion", "rubric"}


class SideFile(NamedTuple):
    include: list[str]  # glob patterns; a project file matching one is a document
    documents: dict[str, dict]  # declared path -> {"purpose": str, "refs": list[str]}
    rubrics: dict[str, str]  # success criterion id -> the rubric an AI grader applies
    fixed: list[str]  # path globs the edit hook refuses rather than warns about (behavior 5.1)
    files: dict[str, dict] = {}  # path or glob -> {"purpose", "refs"}: every other file (Q48)
    whole_repo: bool = False  # True when the side file has a `files` section: every tracked file must be declared
    guard_mode: str | None = None  # `guard.mode`: block, warn, off, or None when absent (behavior 5.1)


def _text(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def _read(root: Path, base: str | None = None) -> dict | None:
    if base is not None:
        text = committed_text(root, base, SIDE_FILE)
        if text is None:
            return None
    else:
        path = root / SIDE_FILE
        if not path.is_file():
            return None
        text = path.read_text(encoding="utf-8")
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ValueError(f"{SIDE_FILE} is not valid YAML: {exc}") from exc
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"{SIDE_FILE} must hold a mapping (schema, documents, rubrics), not {type(data).__name__}")
    return data


GUARD_MODES = ("block", "warn", "off")


def guard_mode(data: dict) -> str | None:
    """`guard.mode` from a parsed side file: `block`, `warn` or `off`, None when absent.

    Any other value reads as `block`, so a mistyped setting cannot turn refusals into warnings.
    """
    section = data.get("guard")
    if section is None:
        return None
    if not isinstance(section, dict):
        return "block"
    mode = section.get("mode")
    if mode is None:
        return None
    mode = "block" if mode is True else "off" if mode is False else mode
    return mode if mode in GUARD_MODES else "block"


def _entries(data: dict, section: str, key: str) -> list:
    block = data.get(section)
    if section == "documents":
        block = block.get(key) if isinstance(block, dict) else None
    return block if isinstance(block, list) else []


def load_side_file(root: Path, base: str | None = None) -> SideFile | None:
    """The side file at `root`, or None when the project has none.

    With `base`, the side file as committed at that revision rather than the working tree's
    (`pcw check` judges a change by the rules it started from, issue #67).

    Keeps only well-formed entries: a document with a path, a purpose and at least one reference,
    a rubric with a criterion and its text; the first of two entries with one path or criterion
    wins. Raises ValueError when the file is not a YAML mapping.
    """
    data = _read(root, base)
    if data is None:
        return None
    raw_docs = data.get("documents")
    docs: dict = raw_docs if isinstance(raw_docs, dict) else {}
    include = [g for g in docs.get("include") or [] if _text(g)] if isinstance(docs.get("include"), list) else []
    documents: dict[str, dict] = {}
    for d in _entries(data, "documents", "declared"):
        if not isinstance(d, dict):
            continue
        path, purpose, refs = _text(d.get("path")), _text(d.get("purpose")), d.get("refs")
        if path and purpose and isinstance(refs, list) and refs and path not in documents:
            documents[path] = {"purpose": purpose, "refs": [str(r) for r in refs]}
    rubrics: dict[str, str] = {}
    for r in _entries(data, "rubrics", ""):
        if isinstance(r, dict) and _text(r.get("criterion")) and _text(r.get("rubric")):
            rubrics.setdefault(_text(r.get("criterion")), _text(r.get("rubric")))
    raw_fixed = data.get("fixed")
    fixed = [_text(g) for g in raw_fixed if _text(g)] if isinstance(raw_fixed, list) else []
    files: dict[str, dict] = {}
    raw_files = data.get("files")
    for d in raw_files if isinstance(raw_files, list) else []:
        if not isinstance(d, dict):
            continue
        path, purpose, refs = _text(d.get("path")), _text(d.get("purpose")), d.get("refs")
        if path and purpose and isinstance(refs, list) and refs and path not in files:
            files[path] = {"purpose": purpose, "refs": [str(r) for r in refs]}
    return SideFile(include, documents, rubrics, fixed, files, "files" in data, guard_mode(data))


def _plan_ids(plan: dict) -> set[str]:
    ids: set[str] = set()
    for value in plan.values():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and isinstance(item.get("id"), str):
                    ids.add(item["id"])
                    for er in item.get("evidence_requirements") or []:
                        if isinstance(er, dict) and isinstance(er.get("id"), str):
                            ids.add(er["id"])
    return ids


def side_file_problems(root: Path, plan: dict) -> list[str]:
    """Everything wrong with the side file, one plain line each; empty when it is sound or absent.

    `plan` is the parsed `.aes/target.yaml`; a document's references must name its items. Whether a
    rubric's criterion exists is behavior 2.1's check (`lockstep.criterion_checks`), not this one.
    """
    try:
        data = _read(root)
    except ValueError as exc:
        return [str(exc)]
    if data is None:
        return []
    problems = [f"{SIDE_FILE} has an unknown key '{k}'; it holds only {', '.join(sorted(_TOP))}."
                for k in sorted(set(data) - _TOP, key=str)]
    if data.get("schema") != SCHEMA:
        problems.append(f"{SIDE_FILE} must say `schema: {SCHEMA}`; it says {data.get('schema')!r}.")

    docs = data.get("documents")
    if docs is not None and not isinstance(docs, dict):
        problems.append(f"{SIDE_FILE}: documents must be a mapping with include and declared.")
        docs = {}
    docs = docs or {}
    problems += [f"{SIDE_FILE}: documents has an unknown key '{k}'; it holds only include and declared."
                 for k in sorted(set(docs) - _DOCUMENTS, key=str)]
    include = docs.get("include")
    if docs and (not isinstance(include, list) or not include or not all(_text(g) for g in include)):
        problems.append(f"{SIDE_FILE}: documents.include must be a non-empty list of glob patterns, such as [\"*.md\"].")
    known = _plan_ids(plan)
    seen: set[str] = set()
    declared = docs.get("declared")
    if declared is not None and not isinstance(declared, list):
        problems.append(f"{SIDE_FILE}: documents.declared must be a list.")
        declared = []
    for i, d in enumerate(declared or [], 1):
        where = f"{SIDE_FILE}: documents.declared entry {i}"
        if not isinstance(d, dict):
            problems.append(f"{where} is not a mapping with path, purpose and refs.")
            continue
        path = _text(d.get("path"))
        where = f"{SIDE_FILE}: document {path}" if path else where
        problems += [f"{where} has an unknown key '{k}'; a document holds only path, purpose and refs."
                     for k in sorted(set(d) - _DOCUMENT, key=str)]
        if not path:
            problems.append(f"{where} has no path.")
        elif path in seen:
            problems.append(f"{where} is declared twice.")
        seen.add(path)
        if not _text(d.get("purpose")):
            problems.append(f"{where} has no purpose: say why the document exists.")
        refs = d.get("refs")
        if not isinstance(refs, list) or not refs:
            problems.append(f"{where} names no plan item in refs: say which requirement or behavior it serves.")
        else:
            missing = [str(r) for r in refs if str(r) not in known]
            if missing:
                problems.append(f"{where} refers to {', '.join(missing)}, which .aes/target.yaml does not hold.")

    files = data.get("files")
    if files is not None and not isinstance(files, list):
        problems.append(f"{SIDE_FILE}: files must be a list of entries with path, purpose and refs.")
        files = []
    seen_files: set[str] = set()
    for i, d in enumerate(files or [], 1):
        where = f"{SIDE_FILE}: files entry {i}"
        if not isinstance(d, dict):
            problems.append(f"{where} is not a mapping with path, purpose and refs.")
            continue
        path = _text(d.get("path"))
        where = f"{SIDE_FILE}: file {path}" if path else where
        problems += [f"{where} has an unknown key '{k}'; a file entry holds only path, purpose and refs."
                     for k in sorted(set(d) - _DOCUMENT, key=str)]
        if not path:
            problems.append(f"{where} has no path.")
        elif path in seen_files:
            problems.append(f"{where} is declared twice.")
        seen_files.add(path)
        if not _text(d.get("purpose")):
            problems.append(f"{where} has no purpose: say why the file exists.")
        refs = d.get("refs")
        if not isinstance(refs, list) or not refs:
            problems.append(f"{where} names no plan item in refs: say which requirement or behavior it serves.")
        else:
            missing = [str(r) for r in refs if str(r) not in known]
            if missing:
                problems.append(f"{where} refers to {', '.join(missing)}, which .aes/target.yaml does not hold.")

    guard = data.get("guard")
    if guard is not None and not isinstance(guard, dict):
        problems.append(f"{SIDE_FILE}: guard must be a mapping such as {{mode: block}}.")
    elif guard:
        mode = guard.get("mode")
        if mode is not None and not isinstance(mode, bool) and mode not in GUARD_MODES:
            problems.append(f"{SIDE_FILE}: guard.mode is {mode!r}; it must be block, warn or off (the edit hook treats it as block).")
        problems += [f"{SIDE_FILE}: guard has an unknown key '{k}'; it holds only mode."
                     for k in sorted(set(guard) - {"mode"}, key=str)]

    rubrics = data.get("rubrics")
    if rubrics is not None and not isinstance(rubrics, list):
        problems.append(f"{SIDE_FILE}: rubrics must be a list.")
        rubrics = []
    named: set[str] = set()
    for i, r in enumerate(rubrics or [], 1):
        if not isinstance(r, dict):
            problems.append(f"{SIDE_FILE}: rubrics entry {i} is not a mapping with criterion and rubric.")
            continue
        criterion = _text(r.get("criterion"))
        where = f"{SIDE_FILE}: rubric for {criterion}" if criterion else f"{SIDE_FILE}: rubrics entry {i}"
        problems += [f"{where} has an unknown key '{k}'; a rubric holds only criterion and rubric."
                     for k in sorted(set(r) - _RUBRIC, key=str)]
        if not criterion:
            problems.append(f"{where} names no criterion.")
        elif criterion in named:
            problems.append(f"{where} is declared twice.")
        named.add(criterion)
        if not _text(r.get("rubric")):
            problems.append(f"{where} has no rubric text.")

    fixed = data.get("fixed")
    if fixed is not None and (not isinstance(fixed, list) or not all(_text(g) for g in fixed)):
        problems.append(f"{SIDE_FILE}: fixed must be a list of path globs, such as [\"src/core/*\"].")
    planning = data.get("planning")
    if isinstance(planning, dict) and planning.get("project_graph") is not None:
        from lockstep.checks.project_graph import project_graph_problem
        problem = project_graph_problem(planning["project_graph"])
        if problem:
            problems.append(f"{SIDE_FILE}: planning.project_graph {problem}.")
    from lockstep.checks.plugin_settings import read_setting
    _, skills_problem = read_setting((root / SIDE_FILE).read_text(encoding="utf-8"))
    if skills_problem:
        problems.append(f"{skills_problem}.")
    return problems

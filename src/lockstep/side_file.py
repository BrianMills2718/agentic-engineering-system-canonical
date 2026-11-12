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

`fixed` holds path globs matched against the whole project-relative path (`fnmatch`, so `*` also
crosses `/`). The edit hook only warns by default (decision D7); a file matching one of these globs
gets the refusal instead. A project with no side file has no document rule, no rubrics and no fixed
files. The file is data read with
`yaml.safe_load`; nothing in it is executed. `load_side_file` keeps the well-formed entries;
`side_file_problems` names everything else (unknown keys, duplicates, an empty purpose or rubric,
a reference the plan does not hold), and `python -m lockstep.unplanned_files` fails on any of them.

[[[cog import lockstep.cogtext as c; c.docstring("ART-SIDE-FILE", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

Part of REQ-1: The plan declares the normative side and the whole file
  structure: the plan, written as structured YAML in the AES plan format,
  declares the normative side (requirements, success criteria and decisions)
  and declares every file and every strongly typed function and class; no
  code file, test or document exists without a declared reason.
Part of REQ-2: Each success criterion names how it is checked: every success
  criterion in the plan names how it is checked: a test file by name,
  Brian's sign-off, or an AI-graded rubric.
Part of REQ-5: Links are checked both ways on every change: links between
  requirement, criterion, test, file and symbol are checked in both
  directions on every change, at edit time (the hook) and before commit
  (`pcw check`); an unplanned or stale item is refused.
BEH-1.1: Any file in the project that the plan does not declare is reported,
  with why it counts: code and tests under a governed folder through the AES
  plan, documents through Lockstep's side file beside the plan, and, when
  the side file has a files section, every other tracked file through that
  section.
BEH-2.1: Every success criterion names how it is checked: a test file by
  name, Brian's sign-off, or an AI-graded rubric declared in Lockstep's side
  file.
BEH-5.1: At edit time, an agent's edit to a file under a governed folder
  that the plan does not declare, a shell command that writes such a file (a
  redirect, tee, or a new file named by an in-place or scripted write,
  following `cd`), or a shell command that writes a planned file (which
  would skip this check), is warned about by default; the edit goes through,
  the agent is told it would be refused and the hook log records a would-
  block; it is refused for a file Lockstep's side file marks fixed, or
  everywhere with PCW_MODE=block; a shell write the plan has no rule for is
  let through and logged; every call the hook sees is logged, including one
  it lets through with nothing to say, with the start of a shell command;
  the would-blocks can be counted per day. Every refusal and warning also
  names the project's wiki (`python -m lockstep.wiki`) as where to look next.
SC-1.1: An undeclared file under a governed folder is reported; a declared
  file, a legacy file and a file outside every governed folder are not,
  unless the side file has a files section, when an undeclared tracked file
  outside the governed folders is reported; an undeclared document is
  reported.
  Disproved if: An undeclared code file, test or document passes without a
  report, a tracked file declared nowhere passes when the side file has a
  files section, or a declared, legacy or (without a files section)
  ungoverned file is reported.
SC-2.1: A criterion with no test, sign-off or rubric route is reported, and
  an AI-graded rubric can be declared for a criterion.
  Disproved if: A criterion passes with no named check, or an AI-graded
  rubric cannot be declared.
SC-5.1: By default the hook allows an Edit or Write to an undeclared
  governed file, a shell write that creates one, and a shell write to a
  planned file, telling the agent it would be refused and logging decision
  would_block; it denies each for a file matching a `fixed` glob in the side
  file or under PCW_MODE=block, including when the shell command reaches the
  file after `cd`, through tee, or from a here-document or a python script;
  it allows an edit to a declared file whose copy is current, and a shell
  command that writes no governed file; `pcw-hook --would-block` prints the
  would-block count per day. Every refusal and warning names `python -m
  lockstep.wiki`. Every call the hook sees in a project leaves one log line, a
  silent pass as decision pass.
  Disproved if: An edit to an undeclared governed file, a shell write that
  creates one, or a shell write to a planned file, is let through when the
  file is marked fixed or PCW_MODE=block is set; a warned edit is not logged
  as would_block or the agent is not told; a file not marked fixed is
  refused by default; a shell command that writes no governed file is
  refused; or the count misses a would_block record; or a refusal or warning
  does not name `python -m lockstep.wiki`; or a call the hook sees in a project
  leaves no log line.
Proven by: VS-1.1-a (tests/test_unplanned_files.py)
Proven by: VS-1.1-b (tests/test_unplanned_documents.py)
Proven by: VS-2.1-a (tests/test_criterion_checks.py)
Proven by: VS-5.1-a (tests/test_hook.py)
Proven by: VS-1.1-c (tests/test_unplanned_other_files.py)
Declares (typed signatures, from the plan):
  SIDE_FILE
  SideFile
  load_side_file(root: Path, base: str | None = None) -> SideFile | None
  side_file_problems(root: Path, plan: dict) -> list[str]
[[[end]]] (sum: q/Xtos/3dz)
"""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import yaml

from lockstep.aes_bridge import committed_text

SIDE_FILE = "lockstep.yaml"
SCHEMA = "lockstep.side.v1"
_TOP = {"schema", "documents", "rubrics", "fixed", "files", "actions",  # actions: read by lockstep.action_check (behavior 5.4)
        "checks", "sources", "owner", "likec4",  # the commit checks (lockstep.checks)
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
    return SideFile(include, documents, rubrics, fixed, files, "files" in data)


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
    problems = [f"{SIDE_FILE} has an unknown key '{k}'; it holds only schema, documents, files, rubrics and fixed."
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
    return problems

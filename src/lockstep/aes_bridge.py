"""Read the AES plan: compiled context per ID and the path-to-artifact map.

[[[cog import lockstep.cogtext as c; c.docstring("ART-AES-BRIDGE", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

Part of REQ-1: The plan declares the normative side and the whole file
  structure: the plan, written as structured YAML in the AES plan format,
  declares the normative side (requirements, success criteria and decisions)
  and declares every file and every strongly typed function and class; no
  code file, test or document exists without a declared reason.
Part of REQ-3: A hook copies the normative text and typed signatures down
  into the code: a hook copies the full normative text, and the typed
  signatures, from the plan down into the code's docstrings automatically;
  nobody types the copy. For normative text the projection is two-way: the
  normative portion of a docstring can be edited where the agent is working,
  and the edit projects up into the plan; and when the normative text
  changes in the plan, every linked function, wherever it is, is marked for
  update and the agent is handed that list.
Part of REQ-5: Links are checked both ways on every change: links between
  requirement, criterion, test, file and symbol are checked in both
  directions on every change, at edit time (the hook) and before commit
  (`pcw check`); an unplanned or stale item is refused.
Part of REQ-6: The wiki gets an agent to the right document or code within
  two links: from the wiki's front page, an agent reaches the normative
  document or the code that answers its question within two links, and each
  link comes with a summary of what it leads to.
BEH-1.1: Any file in the project that the plan does not declare is reported,
  with why it counts: code and tests under a governed folder through the AES
  plan, documents through Lockstep's side file beside the plan, and, when
  the side file has a files section, every other tracked file through that
  section.
BEH-3.1: The full text of a planned file's requirement, behaviors and
  criteria, with each disproof and proving test, is copied by cog from the
  plan into the file's docstring; nobody types the copy.
BEH-3.3: Every declared Python source or test file that does not exist yet
  is created with a docstring holding the cog block for its plan text; an
  existing file is never touched.
BEH-3.4: An agent's edit to a planned file while the file's docstring copy
  of the plan is out of date tells the agent to run `make project`; by
  default the edit goes through with that warning and is logged as a would-
  block, and it is stopped for a file the side file marks fixed or with
  PCW_MODE=block; PCW_BLOCK_STALE=0 turns the stop into a plain allow.
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
BEH-5.2: Before commit, the whole working tree gets the same checks: an
  undeclared file in a governed folder, a stale docstring copy, a planned
  source file without the copy of its own plan item, a new planned Python
  file with no docstring copy of its plan, a hand edit to the plan, an
  edited or removed evidence record, or a deleted planned file blocks; a
  plan change that is exactly the acceptance of new plan files (`aes plan
  accept`) passes, and so does a new evidence record (`aes evidence
  record`); the side file (`lockstep.yaml`) and the legacy list are read as
  they are at the base revision, so a change cannot declare its own files or
  add them to the legacy list, and a changed side file is reported; nothing
  from the checked tree is executed.
BEH-6.1: The wiki is built from the plan, the evidence standing and the code
  docstrings at build time, so it has no hand-written copy to go stale. Its
  front page is set out as the questions a reader starts from (what must the
  project do and is it met, which files do each part and does their test
  prove it, does the code match the plan, what does the code say, what
  changed), each entry linking down to the page that answers it; every page
  names the plan file and every planned file and proving test as a link to
  that file, at the commit the page was built from when the repository has a
  hosted copy.
SC-1.1: An undeclared file under a governed folder is reported; a declared
  file, a legacy file and a file outside every governed folder are not,
  unless the side file has a files section, when an undeclared tracked file
  outside the governed folders is reported; an undeclared document is
  reported.
  Disproved if: An undeclared code file, test or document passes without a
  report, a tracked file declared nowhere passes when the side file has a
  files section, or a declared, legacy or (without a files section)
  ungoverned file is reported.
SC-3.1: After `make project`, a planned file's docstring holds its behavior
  statement, criterion, disproof and proving test word for word from the
  plan.
  Disproved if: The docstring holds only an ID or a reference, or text that
  differs from the plan.
SC-3.3: `python -m lockstep.scaffold` creates each missing declared .py file with
  its cog block and leaves existing files unchanged.
  Disproved if: A missing declared file is not created, is created without
  its cog block, or an existing file changes.
SC-3.4: With PCW_MODE=block the hook denies an edit to a planned file whose
  docstring differs from the plan, and allows the same edit once the copy is
  regenerated; by default it allows the stale edit with the warning.
  Disproved if: Under PCW_MODE=block (PCW_BLOCK_STALE unset) an edit goes
  through while the copy is stale, or is stopped after regeneration; or by
  default a stale edit is stopped or goes through without the warning.
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
SC-5.2: `pcw check` blocks a tree with an undeclared governed file, a stale
  copy, a planned source file whose copy of its own plan item is missing or
  replaced by another item's, a planned Python file absent at the base and
  written without the cog block for its plan, a hand edit to the plan, an
  edited or removed evidence record or a deleted planned file, including
  when the same change declares that file in the side file or adds it to the
  legacy list, committed or git-ignored; allows a tree in step, a plan
  change equal to the earlier plan with each newly accepted plan file
  applied, a new evidence record, and a side-file declaration once that
  declaration is committed; and never runs code from the tree.
  Disproved if: Any of those blocking changes passes `pcw check`, a plan
  change made by `aes plan accept` or a new record written by `aes evidence
  record` is blocked, a planned test file that existed at the base is
  blocked only for having no copy, or `pcw check` executes code from the
  checked tree, or a change that declares its own file in `lockstep.yaml` or
  lists it in `.aes/legacy_baseline.json` passes because of that edit.
SC-6.1: `make wiki` builds pages that show each planned file's plan text and
  its criterion standing from the current plan; every section heading on the
  front page is a question, and each component page links the plan file,
  each of its planned files and each proving test by its path, to the hosted
  copy at the build's commit (mkdocs `repo_url` or a GitHub `origin`) or
  else to the file on disk.
  Disproved if: A wiki page shows plan text or standing that differs from
  the current plan and evidence, a front-page section heading is not a
  question, or a component page names a planned file or proving test without
  a link to it.
Proven by: VS-1.1-a (tests/test_unplanned_files.py)
Proven by: VS-1.1-b (tests/test_unplanned_documents.py)
Proven by: VS-3.1-a (tests/test_cogtext.py)
Proven by: VS-3.3-a (tests/test_scaffold.py)
Proven by: VS-3.4-a (tests/test_stale_edit.py)
Proven by: VS-5.1-a (tests/test_hook.py)
Proven by: VS-5.2-a (tests/test_check.py)
Proven by: VS-6.1-a (tests/test_e2e.py)
Proven by: VS-1.1-c (tests/test_unplanned_other_files.py)
Declares (typed signatures, from the plan):
  find_root(start: Path) -> Path | None
  run_aes(root: Path, *args: str) -> subprocess.CompletedProcess[str]
  context(root: Path, subject: str) -> dict
  target(root: Path) -> dict
  governed_roots(root: Path) -> list[str]
  artifact_for_path(root: Path, relpath: str) -> str | None
  committed_text(root: Path, ref: str, relpath: str) -> str | None
  legacy_files(root: Path, base: str | None = None) -> set[str]
  is_governed(root: Path, relpath: str, base: str | None = None) -> bool
[[[end]]] (sum: TtVoo4koXF)
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

from lockstep.layout_plan import SOURCE, governed, has_layout, layout_context, target_from_layout


def find_root(start: Path) -> Path | None:
    """Nearest directory at or above `start` holding `.aes/project.yaml`, or a lockstep.yaml whose `layout:` is the plan."""
    start = start.resolve()
    for candidate in [start, *start.parents]:
        if (candidate / ".aes" / "project.yaml").is_file() or has_layout(candidate):
            return candidate
    return None


def plan_name(root: Path) -> str:
    """Where this repository's plan is written, for messages: `.aes/target.yaml` or the layout."""
    return SOURCE if has_layout(root) else ".aes/target.yaml"


def _aes() -> str:
    found = shutil.which("aes")
    if found:
        return found
    sibling = Path(sys.executable).with_name("aes")
    if sibling.exists():
        return str(sibling)
    raise RuntimeError("aes not found on PATH or next to this Python")


def run_aes(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([_aes(), *args], cwd=root, capture_output=True, text=True)


def context(root: Path, subject: str) -> dict:
    """`aes context SUBJECT --format json`, or the layout row's context; fails loudly on an unknown ID."""
    if has_layout(root):
        return layout_context(root, subject)
    proc = run_aes(root, "context", subject, "--format", "json")
    if proc.returncode != 0:
        raise RuntimeError(f"aes context {subject} failed: {proc.stderr.strip()}")
    return json.loads(proc.stdout)


def target(root: Path) -> dict:
    if has_layout(root):
        return target_from_layout(root)
    return yaml.safe_load((root / ".aes" / "target.yaml").read_text(encoding="utf-8"))


def governed_roots(root: Path) -> list[str]:
    if has_layout(root):
        return governed(root)
    project = yaml.safe_load((root / ".aes" / "project.yaml").read_text(encoding="utf-8"))
    return list(project.get("governed_roots") or target(root).get("governed_roots") or [])


def artifact_for_path(root: Path, relpath: str) -> str | None:
    for art in target(root).get("planned_artifacts") or []:
        if (art.get("locator") or {}).get("exact_path") == relpath:
            return art["id"]
    return None


def committed_text(root: Path, ref: str, relpath: str) -> str | None:
    """The text of `relpath` as committed at `ref`, or None when no file is there.

    Read from the object store, never the working tree, so a change cannot rewrite what is read (issue #67).
    """
    def git(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "-C", str(root), *args],
                              capture_output=True, text=True)
    if git("cat-file", "-t", f"{ref}:{relpath}").stdout.strip() != "blob":
        return None
    shown = git("show", f"{ref}:{relpath}")
    if shown.returncode != 0:
        raise RuntimeError(f"git show {ref}:{relpath} failed: {shown.stderr.strip()[:300]}")
    return shown.stdout


def legacy_files(root: Path, base: str | None = None) -> set[str]:
    """Files `aes adopt` accepted as they were; a real project's existing code starts here.

    With `base`, the list as committed at that revision, so a change cannot add its own files to it.
    """
    rel = ".aes/legacy_baseline.json"
    if base is not None:
        text = committed_text(root, base, rel)
    else:
        path = root / rel
        text = path.read_text(encoding="utf-8") if path.is_file() else None
    return set(json.loads(text).get("files") or []) if text else set()


def is_governed(root: Path, relpath: str, base: str | None = None) -> bool:
    """Under a governed root, and not a legacy file (those stay editable until planned)."""
    return any(relpath.startswith(g) for g in governed_roots(root)) and relpath not in legacy_files(root, base)

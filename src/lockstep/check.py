"""`pcw check --repo PATH [--base REF] [--json]`: is a whole working tree still on its plan?

The edit hook (`lockstep.hook`) judges one edit while an agent works. This judges every
change at once, after the agent stops: the Project Brain pull-request runner calls it
on the host, before it commits, and opens no pull request when it says `block`.

A change is every file that differs from `--base` (default HEAD), staged or not,
plus every untracked file git does not ignore. For each one:

  - under the evidence folder (`.aes/observations/`): a new evidence record (`aes evidence record`)
    is allowed; an edited or removed record, or a new file that is not a record, blocks;
  - elsewhere under `.aes/`: the change edits the plan itself, which only `aes plan accept` may do: block,
    unless it is exactly the recorded acceptance of new plan files; even then, block when the resulting plan
    declares a file with no reason (behavior 1.3, `lockstep.declared_reason`);
  - under a governed folder, not a legacy file, and not named in the plan: block;
  - a planned file whose docstring copy of the plan is out of date (`cog --check`): block;
  - a planned source file with no copy of its own plan item, or a copy of another item: block;
  - a planned Python file new in the change (absent at `--base`) with no docstring copy of its plan: block;
  - a planned file deleted: block;
  - a planned Python source file to which the change adds a public function or class the plan does not declare,
    or gives a declared function another signature (behavior 5.5, `lockstep.symbol_gate`): block;
  - a planned file whose copy matches: allowed;
  - Lockstep's side file (`lockstep.yaml`) changed: allowed and reported, because the check reads the side file
    and the legacy list (`.aes/legacy_baseline.json`) as they are at `--base`, never from the tree it judges,
    so a change cannot declare its own files or add them to the legacy list (issue #67);
  - anything else (outside governed folders, or legacy): ignored, counted.

Nothing from the checked tree is executed. The runner calls this on the host against a
clone an agent wrote, so the docstring copy is compared with the plan here (each
block's first line must be exactly the standard `c.docstring("ID")` call, and the lines up to
its end marker must equal what that call renders), rather than by running `cog`, which
would run whatever Python the agent put in the block. Git runs with hooks, fsmonitor,
external diff drivers and textconv turned off.

Exit 0 allow, 1 block, 2 the check could not run. Text output is one line per checked
file and a final `OUTCOME` line; `--json` prints the same as one object.

This is behavior 5.2 (before commit, the whole tree); the unplanned-file rule it applies is
behavior 1.1 (`lockstep.unplanned_files`).

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:check.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-plan-format/the-plan-is-openspec-plus-layout-rows, lockstep-plan-format/a-planned-file-without-a-cog-plan-copy-is-judged-by-its-implements-block, lockstep-plan-format/every-refusal-in-a-layout-repository-names-a-layout-command, lockstep-package/lockstep-installs-from-aes-canonical

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

### Requirement: A planned file without a cog plan copy is judged by its Implements block

In a layout repository, the edit hook SHALL treat a planned file that holds no cog plan copy as current when `lockstep check project` would not change it, and as stale when that command would rewrite its generated `Implements:` requirement text. A stale file's refusal SHALL name `uv run lockstep check project`, and running that command SHALL clear it. A file with a cog plan copy, and a repository with `.aes/target.yaml`, SHALL be judged as before.

Source: Brian, 2026-11-20, "yes" to proving Lockstep on a from-scratch repository (`docs/planning/next.goal.md`, step 3), where every edit to a planned file that predated its layout row was refused; the rule itself inferred by agent from `proposals/one-planning-tool/DESIGN.md` ("one projector ... fed from OpenSpec").

#### Scenario: An existing file with a current Implements block can be edited

- **GIVEN** a file written before its layout row, whose `Implements:` block `lockstep check project` has written
- **WHEN** an agent edits it under `PCW_MODE=block`
- **THEN** the edit is allowed and the agent is handed the requirement text

#### Scenario: A stale Implements block names the command that fixes it

- **GIVEN** that file and an active change that rewords its requirement
- **WHEN** an agent edits it under `PCW_MODE=block`, runs `lockstep check project`, and edits it again
- **THEN** the first edit is refused naming `lockstep check project` and not `make project`, and the second is allowed with the new text

### Requirement: Every refusal in a layout repository names a layout command

In a layout repository, the whole-tree commit check SHALL judge a planned file's docstring exactly as the edit hook does, and its stale reason SHALL name `uv run lockstep check project`. A refusal for an undeclared, removed or retyped public symbol SHALL name the file's layout row `exports:` in lockstep.yaml as where to declare it. Every edit-hook refusal SHALL end by pointing to the layout rows in `lockstep.yaml` and to `uv run lockstep show <file>`, and SHALL NOT point to `python -m lockstep.wiki`, which needs an AES plan. A repository with `.aes/target.yaml` SHALL keep its current wording.

Source: Brian, 2026-11-20, "yes" to proving Lockstep on a from-scratch repository (`docs/planning/next.goal.md`, step 3), whose rerun was blocked at commit by a check naming `.aes/target.yaml`; the rule itself inferred by agent. The refusal pointer added 2026-11-23 after `python -m lockstep.wiki` was found to crash in a layout repository (inferred by agent, while carrying out Q54).

#### Scenario: The commit check judges an Implements block the same way

- **GIVEN** a committed file whose `Implements:` block is current, edited in the working tree
- **WHEN** `lockstep check` runs, then again after an active change rewords its requirement, then after `lockstep check project`
- **THEN** it allows, then blocks the file as stale naming `lockstep check project` and not `.aes/target.yaml`, then allows

#### Scenario: An undeclared public symbol names the layout exports

- **GIVEN** a planned layout file
- **WHEN** an agent's edit adds a public function its layout row does not export, under `PCW_MODE=block`
- **THEN** the edit is refused naming the row's `exports:` in lockstep.yaml and not `aes plan`

#### Scenario: A refusal points to lockstep show, not the wiki

- **GIVEN** a layout repository with no `.aes/` folder
- **WHEN** the edit hook refuses a write to an unplanned file
- **THEN** the refusal names `uv run lockstep show` and does not name `python -m lockstep.wiki`

### Requirement: Lockstep installs from AES canonical

Installing this repository SHALL provide the Python package `lockstep` and the commands `lockstep` and
`lockstep-hook`, which run Lockstep's whole-tree check and its agent edit hook.

Source: Brian, 2026-11-11, approving the one-tool design as written ("i approve single tool desing re d4"; `proposals/one-planning-tool/DESIGN.md`, slice 1).

#### Scenario: The check runs from an install

- **GIVEN** this repository installed into a fresh environment
- **WHEN** `lockstep check --help` runs
- **THEN** it exits 0 and prints the check's usage
[[[end]]]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml
from agentic_engineering_system.evidence import ObservationRecord
from agentic_engineering_system.planning import apply_delta, load_plan
from agentic_engineering_system.records import load_project, parse_target
from lockstep.layout_plan import has_layout, layout_problems

from lockstep.aes_bridge import artifact_for_path, context, find_root, target
from lockstep.cogtext import END, OPEN, render
from lockstep.declared_reason import reasonless_artifacts
from lockstep.side_file import SIDE_FILE
from lockstep.unplanned_files import unplanned_reason

# The one cog block Lockstep writes (lockstep.scaffold, cogtext's docstring). Regex over code, not prose.
COG_CALL = re.compile(r'(?P<lead>.*?)\[\[\[cog import (?:pcw|lockstep)\.cogtext as c; '
                      r'c\.docstring\("(?P<id>[A-Za-z0-9_.:-]+)"(?:, indent=(?P<indent>\d+))?\)\]\]\]\s*')
SAFE_GIT = ["-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false"]


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", *SAFE_GIT, "-C", str(repo), *args], capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()[:300]}")
    return proc.stdout


def changed_files(repo: Path, base: str = "HEAD") -> list[tuple[str, bool]]:
    """(path relative to the repository, still exists) for every change against `base`."""
    paths = [p for p in _git(repo, "diff", "--name-only", "--no-renames", "--no-ext-diff", "--no-textconv",
                             base).splitlines() if p]
    paths += [p for p in _git(repo, "ls-files", "--others", "--exclude-standard").splitlines() if p]
    seen: dict[str, bool] = {}
    for p in paths:
        seen.setdefault(p, (repo / p).exists())
    return sorted(seen.items())


def docstring_mismatch(root: Path, rel: str) -> str | None:
    """Why the docstring copies in a planned file differ from the plan, or None. Executes nothing."""
    source = (root / rel).read_text(encoding="utf-8")
    if has_layout(root) and OPEN not in source:
        # A layout repository's file with no cog plan copy carries the `Implements:` block that
        # `lockstep check project` writes (a file made before its layout row, or by code2-template);
        # it is current when that command would leave it unchanged.
        from lockstep.checks.project import stale_copy
        return ("its generated `Implements:` requirement text differs from OpenSpec"
                if stale_copy(root, root / rel) else None)
    lines = source.splitlines()
    artifact = next((art for art in target(root).get("planned_artifacts", [])
                     if (art.get("locator") or {}).get("exact_path") == rel), None)
    required = artifact is not None and artifact.get("kind") == "source"
    found = False
    i = 0
    while i < len(lines):
        if OPEN not in lines[i]:
            i += 1
            continue
        m = COG_CALL.fullmatch(lines[i])
        if not m:
            return (f"line {i + 1} holds a cog block that is not the standard plan copy "
                    "(`import lockstep.cogtext as c; c.docstring(\"ID\")`), so it was not run")
        if artifact is not None and m["id"] != artifact["id"]:
            return f"the docstring copies {m['id']}, but {rel} is planned as {artifact['id']}"
        found = True
        end = next((k for k in range(i + 1, len(lines)) if END in lines[k]), None)
        if end is None:
            return f"the cog block at line {i + 1} has no end marker line"
        try:
            ctx = context(root, m["id"])
        except RuntimeError:
            return f"the docstring copies {m['id']}, which the plan does not have"
        pad = " " * int(m["indent"] or 4)
        if lines[i + 1:end] != [(pad + line).rstrip() for line in render(ctx)]:
            return f"the copy of {m['id']} (lines {i + 2} to {end}) differs from the plan"
        i = end + 1
    if required and not found:
        return f"the required docstring copy of {artifact['id'] if artifact else rel} is missing"
    return None


def accepted_plan_change(root: Path, base: str, changed: list[str]) -> tuple[list[str], str | None]:
    """(the plan ids accepted in the change, why the change to `.aes/` is more than their acceptance, or None).

    `aes plan accept` changes `.aes/` in exactly one way: it adds a plan file and rewrites the
    target to the earlier target with that plan's change applied, and it drops from the legacy list
    each file now planned or gone (`_baseline_pruned`). So the change passes when every changed
    `.aes/` path is the target, a new plan file or the legacy list pruned that way, and the target equals the target at
    `base` with each new plan's change applied, oldest first (AES `apply_delta`). This proves the
    plan change is the recorded acceptance of those plan files. Who ran the accept is not checked: the
    coding agent may accept its own changes (Brian, 2026-11-07), and the record it writes is the log.
    """
    project = load_project(root / ".aes" / "project.yaml")
    target_rel = Path(project.materialization.target_path).as_posix()
    plans_rel = Path(project.materialization.plans_root).as_posix().rstrip("/") + "/"
    at_base = set(_git(root, "ls-tree", "-r", "--name-only", base, "--", ".aes").splitlines())
    new_plans = [rel for rel in changed if rel.startswith(plans_rel) and rel.endswith(".yaml")
                 and rel not in at_base and (root / rel).exists()]
    baseline_rel = ".aes/legacy_baseline.json"
    other = [rel for rel in changed if rel != target_rel and rel not in new_plans
             and not (rel == baseline_rel and new_plans and _baseline_pruned(root, base, target_rel, baseline_rel) is None)]
    if baseline_rel in other and new_plans:
        return [], f"{baseline_rel} changed beyond the pruning `aes plan accept` does: {_baseline_pruned(root, base, target_rel, baseline_rel)}"
    if other:
        return [], (f"{', '.join(other)} changed; accepting a plan only adds a plan file and rewrites "
                    f"{target_rel}, and an accepted plan file is never edited afterwards")
    if not new_plans:
        return [], f"{target_rel} changed with no newly accepted plan file under {plans_rel}"
    try:
        plans = sorted((load_plan(root / rel) for rel in new_plans), key=lambda p: (p.accepted_at, p.proposal_id))
    except Exception as exc:  # noqa: BLE001 - an unreadable plan file is the reason
        return [], f"a new file under {plans_rel} is not an accepted plan: {str(exc).splitlines()[0]}"
    if target_rel not in at_base:
        return [], f"{target_rel} does not exist at {base}, so there is no earlier plan to apply the change to"
    target = parse_target(yaml.safe_load(_git(root, "show", f"{base}:{target_rel}")), root / target_rel)
    for plan in plans:
        target, violations = apply_delta(target, plan.target_delta)
        if violations:
            return [], f"{plan.proposal_id} does not apply to the earlier plan: {violations[0]}"
    now = parse_target(yaml.safe_load((root / target_rel).read_text(encoding="utf-8")), root / target_rel)
    ids = [p.proposal_id for p in plans]
    if now.model_dump() != target.model_dump():
        return ids, (f"{target_rel} differs from the earlier plan with {', '.join(ids)} applied, "
                     "so it was edited by hand as well as accepted")
    return ids, None


def _baseline_pruned(root: Path, base: str, target_rel: str, baseline_rel: str) -> str | None:
    """Why the legacy list differs from the one at `base` by more than `aes plan accept`'s pruning, or None.

    When a plan is accepted, AES removes from the legacy list every file the new plan names or that is
    no longer tracked (its `adopt` pruning). So the list may only lose entries, each one planned now or
    gone, and keep every other entry as it was."""
    try:
        old = json.loads(_git(root, "show", f"{base}:{baseline_rel}")).get("files") or {}
        new = json.loads((root / baseline_rel).read_text(encoding="utf-8")).get("files") or {}
        old, new = ({k: None for k in d} if isinstance(d, list) else d for d in (old, new))
    except Exception as exc:  # noqa: BLE001 - an unreadable list is the reason
        return f"it cannot be read: {str(exc).splitlines()[0]}"
    added = sorted(k for k in new if old.get(k) != new[k])
    if added:
        return f"it adds or changes {', '.join(added)}"
    planned = {(a.get("locator") or {}).get("exact_path")
               for a in (yaml.safe_load((root / target_rel).read_text(encoding="utf-8")) or {}).get("planned_artifacts") or []}
    kept = [k for k in old if k not in new and k not in planned and (root / k).exists()]
    if kept:
        return f"it drops {', '.join(sorted(kept))}, which is still in the tree and not planned"
    return None


def _evidence_problem(root: Path, base: str, rel: str, exists: bool) -> str | None:
    """Why a change to a file in the evidence folder is more than a new record, or None. Executes nothing."""
    if _git(root, "ls-tree", "--name-only", base, "--", rel).strip():
        return (f"{rel} is an evidence record, written once by `aes evidence record`, and the change "
                f"{'edits' if exists else 'removes'} it. Restore it from git; record a new result instead.")
    try:
        ObservationRecord.model_validate(yaml.safe_load((root / rel).read_text(encoding="utf-8")))
    except Exception as exc:  # noqa: BLE001 - an unreadable record is the reason
        return f"{rel} is in the evidence folder but is not an evidence record: {str(exc).splitlines()[0]}"
    return None


def _missing_copy(root: Path, base: str, rel: str, art: str) -> str | None:
    """Why a planned Python file that is new in the change holds no docstring copy of its own plan, or None.

    Behavior 3.3 creates every new declared Python file with the cog block for its plan (`lockstep.scaffold`),
    so a new planned file without it would reach a pull request with no plan text in it (#64). A planned
    source file always needs its copy (`docstring_mismatch`); this adds the other kinds, such as tests,
    when the change creates them. A test file that existed at `base` is not reached: Lockstep's own test
    files predate the copy.
    """
    if not rel.endswith(".py") or _git(root, "ls-tree", "--name-only", base, "--", rel).strip():
        return None
    if has_layout(root) and OPEN not in (root / rel).read_text(encoding="utf-8"):
        return None  # a layout file may carry the `Implements:` block instead; `docstring_mismatch` judges it
    for line in (root / rel).read_text(encoding="utf-8").splitlines():
        m = COG_CALL.fullmatch(line)
        if m and m["id"] == art:
            return None
    return (f"{rel} is a new planned file ({art}) with no docstring copy of its plan. A new planned Python file "
            "starts with the cog block for its plan (`python -m lockstep.scaffold` writes it); then `cog -r -c` "
            "fills in the text.")


def _added_symbols(root: Path, base: str, rel: str) -> list[str]:
    """Behavior 5.5: the undeclared public symbols and changed declared signatures this change adds to `rel`."""
    from lockstep.symbol_gate import added_symbol_problems

    try:
        before: str | None = _git(root, "show", f"{base}:{rel}")
    except Exception:  # noqa: BLE001 - absent at the base: a new file, judged whole
        before = None
    return added_symbol_problems(root, rel, (root / rel).read_text(encoding="utf-8"), before)


def check(repo: Path, base: str = "HEAD") -> dict:
    """The decision for a working tree, with one plain-words reason per checked file."""
    repo = repo.resolve()
    root = find_root(repo)
    if root is None or root.resolve() != repo:
        return {"decision": "allow", "adopted": False, "files": [], "ignored": 0,
                "summary": "Not a Lockstep repository (no .aes/project.yaml at its top); nothing checked."}
    files: list[dict] = []
    ignored = 0
    changes = changed_files(repo, base)
    if has_layout(root):  # the plan is lockstep.yaml's layout with OpenSpec: no AES plan file or evidence folder
        target_rel: str | None = None
        evidence_rel: str | None = None
        plan_paths: list[str] = []
        files += [{"path": SIDE_FILE, "kind": "layout", "blocks": True, "reason": p} for p in layout_problems(root)]
    else:
        materialization = load_project(root / ".aes" / "project.yaml").materialization
        target_rel = Path(materialization.target_path).as_posix()
        evidence_rel = Path(materialization.observations_root).as_posix().rstrip("/") + "/"
        plan_paths = [rel for rel, _ in changes if rel.startswith(".aes/") and not rel.startswith(evidence_rel)]
    accepted, problem = accepted_plan_change(root, base, plan_paths) if plan_paths else ([], None)
    reasonless = (reasonless_artifacts(yaml.safe_load((root / target_rel).read_text(encoding="utf-8")) or {})
                  if target_rel is not None and plan_paths and problem is None else [])
    for rel, exists in changes:
        if rel == target_rel and reasonless:
            files.append({"path": rel, "kind": "reasonless", "blocks": True,
                          "reason": f"{rel} accepts {', '.join(accepted)}, but the plan it makes declares a file "
                                    "with no reason: " + " ".join(reasonless)})
            continue
        if evidence_rel is not None and rel.startswith(evidence_rel):
            why = _evidence_problem(root, base, rel, exists)
            files.append({"path": rel, "kind": "evidence_edit" if why else "evidence", "blocks": bool(why),
                          "reason": why or f"{rel} is a new evidence record (`aes evidence record`)."})
            continue
        if rel.startswith(".aes/") and problem is None:
            files.append({"path": rel, "kind": "plan_accepted", "blocks": False,
                          "reason": f"{rel} is part of accepting {', '.join(accepted)} (`aes plan accept`): "
                                    "the plan equals the earlier plan with that change applied."})
            continue
        if rel.startswith(".aes/"):
            files.append({"path": rel, "kind": "plan_edit", "blocks": True,
                          "reason": f"The change edits the plan itself ({rel}) other than by accepting a plan: "
                                    f"{problem}. Change the plan through `aes plan prepare/validate/accept`."})
            continue
        art = artifact_for_path(root, rel)
        if art is not None and not exists:
            files.append({"path": rel, "kind": "deleted", "artifact": art, "blocks": True,
                          "reason": f"{rel} is a planned file ({art}) and the change deletes it."})
            continue
        if art is None and rel == SIDE_FILE:
            files.append({"path": rel, "kind": "side_file", "blocks": False,
                          "reason": f"{rel} changes here. This check reads the side file, and the legacy list, as "
                                    f"they are at {base}, so the change cannot loosen the rules it is judged by; "
                                    "the new version applies once it is committed on its own."})
            continue
        if art is None:
            unplanned = unplanned_reason(root, rel, base) if exists else None
            if unplanned:
                files.append({"path": rel, "kind": "unplanned", "blocks": True, "reason": unplanned})
            else:
                ignored += 1
            continue
        stale = docstring_mismatch(root, rel)
        missing = None if stale else _missing_copy(root, base, rel, art)
        if stale:
            files.append({"path": rel, "kind": "stale", "artifact": art, "blocks": True,
                          "reason": (f"The generated requirement text in {rel} is out of date with the plan ({stale}). "
                                     "Run `uv run lockstep check project` to regenerate it." if has_layout(root) else
                                     f"The docstring in {rel} no longer matches its plan ({art}) in .aes/target.yaml: "
                                     f"{stale}. The copy is regenerated from the plan (`cog -r -c`), not edited by hand.")})
        elif missing:
            files.append({"path": rel, "kind": "stale", "artifact": art, "blocks": True, "reason": missing})
        elif added := _added_symbols(root, base, rel):
            files.append({"path": rel, "kind": "symbols", "artifact": art, "blocks": True, "reason": " ".join(added)})
        else:
            files.append({"path": rel, "kind": "planned", "artifact": art, "blocks": False,
                          "reason": f"{rel} is in the plan ({art}) and its docstring copy matches the plan."})
    counts = {k: sum(f["kind"] == k for f in files) for k in ("planned", "unplanned", "stale", "symbols", "plan_edit", "plan_accepted", "reasonless",
                                                 "deleted", "evidence", "evidence_edit", "side_file")}
    block = any(f["blocks"] for f in files)
    if block:
        summary = "Held: " + " ".join(f["reason"] for f in files if f["blocks"])
    else:
        summary = (f"Lockstep: {counts['planned']} planned file{'s' if counts['planned'] != 1 else ''} checked, "
                   "none stale, no unplanned file in a governed folder."
                   + (f" Plan change: {', '.join(accepted)} accepted." if accepted and problem is None else "")
                   + (f" {counts['evidence']} new evidence record(s)." if counts["evidence"] else "")
                   + (f" {SIDE_FILE} changed; judged by its version at {base}." if counts["side_file"] else ""))
    return {"decision": "block" if block else "allow", "adopted": True, "base": base, "files": files,
            "ignored": ignored, "counts": counts, "summary": summary}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="pcw check", description=__doc__.splitlines()[0])
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--base", default="HEAD", help="compare against this git ref (default HEAD)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        result = check(a.repo, a.base)
    except Exception as exc:  # the caller must see that no judgment was made
        if a.json:
            print(json.dumps({"decision": "error", "error": f"{type(exc).__name__}: {exc}"}))
        else:
            print(f"OUTCOME error {type(exc).__name__}: {exc}")
        return 2
    if a.json:
        print(json.dumps(result))
    else:
        for f in result["files"]:
            print(f"{'BLOCK' if f['blocks'] else 'OK'} {f['path']}: {f['reason']}")
        c = result.get("counts") or {}
        print(f"OUTCOME decision={result['decision']} files={len(result['files'])} unplanned={c.get('unplanned', 0)} "
              f"stale={c.get('stale', 0)} symbols={c.get('symbols', 0)} plan_edits={c.get('plan_edit', 0)} plans_accepted={c.get('plan_accepted', 0)} "
              f"reasonless={c.get('reasonless', 0)} deleted={c.get('deleted', 0)} "
              f"evidence={c.get('evidence', 0)} evidence_edits={c.get('evidence_edit', 0)} "
              f"ignored={result['ignored']}")
    return 1 if result["decision"] == "block" else 0


def cli() -> int:
    """`lockstep <command>`: `init` (install Lockstep in a repository), `check` (the whole-tree plan check; `check <name>` runs one commit check), `layout`
    (create the planned files), `plan check` (run Company Planning's plan validator), `accept write|check` and `run-plan`
    (hidden acceptance tests and a departure report for one OpenSpec plan), `check prior-art` (the prior-art record
    check `ship` runs), `status` (each
    requirement's code, tests and result) or `show FILE` (what a file must keep true)."""
    args = sys.argv[1:]
    if args and args[0] == "refresh":
        from lockstep.doc_projection import refresh_cli
        return refresh_cli(args[1:])
    if args and args[0] == "init":
        from lockstep.init_repo import init_cli
        return init_cli(args[1:])
    if args and args[0] == "layout":
        from lockstep.scaffold import layout
        return layout()
    if args and args[0] == "accept" and len(args) > 1 and args[1] in ("write", "check"):
        from lockstep.plan_run import cli as plan_run_cli
        return plan_run_cli(args[1:])
    if args and args[0] == "run-plan":
        from lockstep.plan_run import cli as plan_run_cli
        return plan_run_cli(args)
    if args[:2] == ["check", "prior-art"]:
        from lockstep.prior_art import main as prior_art_main
        return prior_art_main(args[2:])
    if args and args[0] == "plan":
        from lockstep.plan_check import plan_cli
        return plan_cli(args[1:])
    if args and args[0] == "status":
        from lockstep.checks.cli import run_status
        return run_status(args[1:])
    if args and args[0] == "show":
        from lockstep.checks.cli import run_show
        return run_show(args[1:])
    if not args or args[0] != "check":
        print("usage: pcw check --repo PATH [--base REF] [--json]", file=sys.stderr)
        return 2
    if len(args) > 1 and not args[1].startswith("-"):  # `lockstep check <name> ...`: one commit check
        from lockstep.checks.cli import run
        return run(args[1:])
    return main(args[1:])


if __name__ == "__main__":
    raise SystemExit(main())

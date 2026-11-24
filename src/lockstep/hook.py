"""Agent edit hook (Claude Code and Codex PreToolUse): warn about, or refuse, an edit to a file the plan does not declare (behavior 5.1).

Reads the tool call on stdin. For an edit to a file it hands the agent the requirement text for that
file. In a repository with OpenSpec specs, and when the file's docstring says `Implements:
<capability>/<requirement>`, that text is the OpenSpec requirement word for word with its scenarios
(`lockstep.openspec_text`, behavior 3.7); otherwise, for a planned file, it is the plan text from
.aes/target.yaml (requirement, criterion, disproof, proving test). A repository with OpenSpec specs and
no AES plan gets the OpenSpec text only: the structure checks below read the AES plan. A shell command
that only names a planned file gets the same text.
It always refuses an edit when the file is a change-log entry under the plans folder, or that
folder or `.aes` itself: only `aes plan accept` writes an entry, and nothing edits or removes one
(`lockstep.change_log`, behavior 4.2); a shell command that writes one is refused too, while reading
one is allowed. That refusal protects append-only history, which a warning cannot.

It would refuse an edit when:
  - the file is under a governed folder but not in the plan, or is a document that
    Lockstep's side file `lockstep.yaml` does not declare (`lockstep.unplanned_files`),
  - the edit changes the plan file itself (.aes/target.yaml) by hand rather than through
    `aes plan accept`; the warning names each changed item and every linked file and symbol
    (`lockstep.plan_edit`, behavior 3.8),
  - a shell command writes a file the plan does not declare (a redirect, tee, or a new file named
    by an in-place or scripted write, following `cd`; parsed as shell words, never as prose),
  - a shell command writes a planned file, skipping this check, or
  - the file's projected docstring is out of date with the plan (`lockstep.stale_edit`,
    behavior 3.4; PCW_BLOCK_STALE=0 turns that one into a plain allow).
By default (decision D7, Brian 2026-11-07) it only warns: the edit goes through, the agent gets
the refusal text after WARN_PREFIX, and the log records `"decision": "would_block"`. It refuses
for a file matching a glob in the side file's `fixed` list, or everywhere with PCW_MODE=block
(`blocks`). `pcw-hook --would-block [--days 14]` prints the would-block count per day.
Every call the hook sees is appended to `hook-<date>.jsonl` in `log_dir()`, outside the project (#974): each decision, a
shell write the plan has no rule for, and a call it lets through with nothing to say (`"decision":
"pass"`), with the first characters of a shell command (Q21). Shell parsing misses a write whose path is built at run
time; `pcw check` before the commit stays the guarantee.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:hook.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-guard/agents-get-requirement-text-from-the-shell-too, lockstep-guard/handing-over-text-never-approves-an-edit, lockstep-init/the-edit-guard-logs-outside-the-checkout, lockstep-package/lockstep-installs-from-aes-canonical, lockstep-guard/a-refusal-lists-the-files-the-plan-allows, lockstep-guard/an-unplanned-file-is-refused-where-the-plan-marks-it-fixed-and-warned-about-elsewhere

### Requirement: Agents get requirement text from the shell too

In a repository with OpenSpec specs and no layout plan, the edit hook SHALL answer a shell command that names or writes a file whose docstrings carry `Implements:` lines with those requirements' text, without a `permissionDecision`, and SHALL log the call as `openspec_text` with the requirement IDs; a command naming no such file and no file a decision governs SHALL get no answer.

Source: inferred by agent from the 2026-11-23 linked-chain acceptance run (Claude edited only through Bash, so the text never arrived); plan docs/planning/linked-chain-core-2026-11-23.md

#### Scenario: A shell command on an implementing file gets its requirement text

- **GIVEN** a file whose docstring says `Implements: ship/<requirement>`
- **WHEN** the agent runs `cat` on it, writes it with a heredoc, or edits it with `sed -i`
- **THEN** the hook's answer holds that requirement's text and no decision

### Requirement: Handing over text never approves an edit

When the edit hook lets a call through with only context (requirement text, a plan, a warning), its answer to Claude Code and to Codex SHALL carry that context without a `permissionDecision`, so the agent's own permission settings still decide whether the edit runs; a refusal SHALL keep `permissionDecision: deny` and its reason.

Source: inferred by agent: Claude Code treats a PreToolUse `allow` as approving the call without the user's prompt (probe 2026-11-23: a context-only answer with no decision still reaches the model); the template now installs the hook in every copy (plan docs/planning/linked-chain-core-2026-11-23.md).

#### Scenario: A context-only answer carries no decision

- **GIVEN** an edit the hook lets through with requirement text
- **WHEN** the hook answers for Claude Code
- **THEN** the answer has `additionalContext` and no `permissionDecision`

### Requirement: The edit guard logs outside the checkout

The edit guard SHALL append its decision log to `hook-<date>.jsonl` in the folder named by `LOCKSTEP_LOG_DIR` when that is set, and otherwise in `${XDG_STATE_HOME:-~/.local/state}/lockstep/<repository name>/`, where the repository name is the main checkout's folder name for every worktree of it; `lockstep-hook --would-block` SHALL count records there and in the project's older `.lockstep/` and `.pcw/` folders.

Source: Brian, 2026-11-11: "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md named `.lockstep/`); moved outside the checkout by issue #974, inferred by agent: logs inside a worktree were deleted with it after merge and a repository without the `.gitignore` line committed them (2026-11-19). Brian, 2026-11-20, "yes" to the local proofs, whose step 1 is this fix (docs/planning/next.goal.md). Brian, 2026-11-23, "i approve" to keeping the log outside the checkout, a departure from DESIGN.md:48 listed in back-on-design slice 3.

#### Scenario: A decision is logged outside the checkout

- **GIVEN** a project with the edit guard installed and `LOCKSTEP_LOG_DIR` unset
- **WHEN** it decides on an edit
- **THEN** `${XDG_STATE_HOME}/lockstep/<repository name>/hook-<date>.jsonl` holds the record, the project gains no `.lockstep/` or `.pcw/` folder, and records already in the project's `.lockstep/` and `.pcw/` are still counted

#### Scenario: A worktree logs under its repository name

- **GIVEN** a worktree whose `.git` file points into `<main>/.git/worktrees/<name>`
- **WHEN** the guard picks its log folder
- **THEN** it is the same folder as the main checkout's, so the log survives the worktree's removal

#### Scenario: An override names the folder

- **GIVEN** `LOCKSTEP_LOG_DIR` names a folder
- **WHEN** the guard decides on an edit
- **THEN** the record is written in that folder and `--would-block` counts it

### Requirement: Lockstep installs from AES canonical

Installing this repository SHALL provide the Python package `lockstep` and the commands `lockstep` and
`lockstep-hook`, which run Lockstep's whole-tree check and its agent edit hook.

Source: Brian, 2026-11-11, approving the one-tool design as written ("i approve single tool desing re d4"; `proposals/one-planning-tool/DESIGN.md`, slice 1).

#### Scenario: The check runs from an install

- **GIVEN** this repository installed into a fresh environment
- **WHEN** `lockstep check --help` runs
- **THEN** it exits 0 and prints the check's usage

### Requirement: A refusal lists the files the plan allows

When the edit hook refuses (or warns about) a write to a file the plan does not name, its message SHALL also list the files the plan does allow, read from whichever plan is in use (`lockstep.yaml` `layout:` rows or the planned artifacts of `.aes/target.yaml`): those in the refused file's folder first, at most 15, then "and N more".

Source: Brian, 2026-11-11, "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md); acceptance entries A2 and A3 in docs/planning/acceptance-criteria.json

#### Scenario: A refusal lists the files the plan allows

- **GIVEN** a plan that names `src/greeter/__init__.py` and PCW_MODE=block
- **WHEN** an agent writes `src/greeter/extra.py`, by an edit or by a shell command
- **THEN** the refusal message lists `src/greeter/__init__.py` under "The plan does allow these files" and no more than 15 paths, with "and N more" for the rest

### Requirement: An unplanned file is refused where the plan marks it fixed and warned about elsewhere

The edit hook SHALL refuse a write to a file under a governed folder that no `layout:` row names when the file
matches a `fixed:` glob in `lockstep.yaml` or `PCW_MODE=block` is set, showing where the file must be planned. For any
other governed file it SHALL let the write through with the refusal text as a warning and log
`"decision": "would_block"`. The template SHALL mark its package folder `fixed:`, so a fresh copy refuses an
unplanned source file.

Source: Brian, 2026-11-07, decision D7 (`lockstep` repository `.aes/plans/PLAN-014-WARN-BY-DEFAULT.yaml:5-7`):
"Lockstep warns; it blocks only files the plan marks fixed, after two weeks of would-block counts"; Brian,
2026-11-11, "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md:30`, step 4: an unplanned
write "is refused"); Brian, 2026-11-23, "i approve" to the template shipping its planned layout (back-on-design item
c). Reading the two as one rule (refuse where marked fixed, which the template does for its package) is inferred by
agent.

#### Scenario: A governed file outside every fixed glob is warned about

- **GIVEN** a governed folder with no `fixed:` glob over it and no `PCW_MODE` set
- **WHEN** an agent writes a file there that no layout row names
- **THEN** the write goes through with the refusal text as a warning and the hook log records `would_block`

#### Scenario: A file under a fixed glob is refused

- **GIVEN** a file matching a `fixed:` glob
- **WHEN** an agent writes it without a plan entry
- **THEN** the edit hook refuses the write

#### Scenario: A fresh template copy refuses an unplanned source file

- **GIVEN** a fresh copy of the template
- **WHEN** an agent writes an unplanned file in the package folder
- **THEN** the edit hook refuses it

Tested by: tests/lockstep/test_lockstep_openspec_text.py
[[[end]]]
"""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import json
import os
import re
import shlex
import sys
from pathlib import Path

from lockstep.aes_bridge import artifact_for_path, context, find_root, plan_name
from lockstep.change_log import entry_edit_reason
from lockstep.cogtext import render
from lockstep.layout_plan import has_layout
from lockstep.change_list import change_list
from lockstep.change_list import render as render_changes
from lockstep.decisions import packet as decision_packet
from lockstep.openspec_text import find_spec_root, requirement_packet
from lockstep.shell_targets import shell_write_words, written_paths
from lockstep.side_file import load_side_file
from lockstep.stale_edit import projection_stale, stale_reason, stops_edits
from lockstep.unplanned_files import allowed_listing, unplanned_reason

# Prefixed to the refusal text when the hook only warns (behavior 5.1, decision D7).
WARN_PREFIX = "Lockstep would block this edit (warn mode): "
# Added to every refusal and warning, so an agent that is stopped knows where to look next (behavior 6.1, Q20).
_WIKI_POINTER = ("To see what the plan asks for and which files and tests do it, start from the project's wiki: "
                 "`python -m lockstep.wiki` prints it, each section a question linking down to the requirement, its files and its test.")
_LAYOUT_POINTER = ("To see what the plan asks for, read the `layout:` rows in lockstep.yaml; "
                   "`uv run lockstep show <file>` prints a file's requirements and the tests that check them.")

EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
SHELL_TOOLS = {"Bash", "shell", "local_shell", "exec_command",
               "terminal"}  # OpenHands' shell tool; its input is {"command": ...}
# OpenHands' file tool: {"command": "view"|"create"|"str_replace"|"insert"|"undo_edit", "path": ...}.
FILE_EDITOR = "file_editor"
PATCH_PATH = re.compile(r"^\*\*\* (?:(?:Update|Add|Delete) File|Move to): (.+)$", re.M)
# Declared by the plan; the shell parser that judges commands is `lockstep.shell_targets` (behavior 5.1).
REDIRECT = re.compile(r"(?:^|\s)\d?>>?(?!&)\s*([^\s;&|]+)")
TEE = re.compile(r"\btee\s+(?:-a\s+)?([^\s;&|]+)")
IN_PLACE = re.compile(r"\bsed\s+-i|\bperl\s+-[a-z]*i|\bmv\b|\bcp\b|\brm\b|\btruncate\b|\btouch\b|"
                      r"\bpython3?\s+-(?:\s|$|c)|\bpython3?\s+-\s*<<|open\(|write_text|\.write\(")


def shell_writes(command: str, path: str) -> bool:
    """True when the command writes `path` (as written, or as the tail of a longer path), by `lockstep.shell_targets`."""
    want = os.path.normpath(path)
    return any((w := os.path.normpath(word)) == want or w.endswith("/" + want) for word in shell_write_words(command))


def paths_from_call(call: dict) -> list[str]:
    tool = call.get("tool_name", "")
    tin = call.get("tool_input") or {}
    if tool in EDIT_TOOLS and tin.get("file_path"):
        return [tin["file_path"]]
    if tool == FILE_EDITOR and tin.get("path") and tin.get("command") != "view":
        return [tin["path"]]
    if tool == "apply_patch":
        patch = tin.get("input") or tin.get("patch") or tin.get("command") or ""
        if isinstance(patch, list):
            patch = "\n".join(map(str, patch))
        return PATCH_PATH.findall(patch)
    return []


def shell_command(call: dict) -> str | None:
    if call.get("tool_name", "") not in SHELL_TOOLS:
        return None
    cmd = (call.get("tool_input") or {}).get("command") or ""
    return " ".join(map(str, cmd)) if isinstance(cmd, list) else str(cmd)


_CALL_ID: str | None = None
_LAST: dict = {}


_PENDING: list = []


LOG_DIR = ".lockstep"  # the guard's old in-checkout log folder (Q23); `--would-block` still counts what is there
OLD_LOG_DIR = ".pcw"  # where it logged before that; still counted
LOG_DIR_ENV = "LOCKSTEP_LOG_DIR"  # override: log exactly in this folder


def _main_checkout(root: Path) -> Path:
    """The repository's main checkout, the same for every worktree of it (issue #974).

    A worktree's `.git` is a file `gitdir: <main>/.git/worktrees/<name>` (or `<main>.git/worktrees/<name>`
    for a bare repository); the main checkout is read from that path without running git, so a log
    survives the worktree being removed after merge. Anything else is its own main checkout.
    """
    dot_git = root / ".git"
    if dot_git.is_file():
        line = dot_git.read_text(encoding="utf-8", errors="replace").strip()
        if line.startswith("gitdir:"):
            gitdir = Path(line.removeprefix("gitdir:").strip())
            if not gitdir.is_absolute():
                gitdir = (root / gitdir).resolve()
            common = gitdir.parent.parent
            if gitdir.parent.name == "worktrees":
                if common.name == ".git":
                    return common.parent
                if common.name.endswith(".git"):
                    return common.parent / common.name.removesuffix(".git")
    return root.resolve()


def log_dir(root: Path) -> Path:
    """Where the guard logs for project `root`: `$LOCKSTEP_LOG_DIR` when set (a relative value is read from
    `root`), else `${XDG_STATE_HOME:-~/.local/state}/lockstep/<main checkout's folder name>/`, outside the
    checkout (issue #974)."""
    override = os.environ.get(LOG_DIR_ENV, "").strip()
    if override:
        folder = Path(override).expanduser()
        return folder if folder.is_absolute() else root / folder
    state = os.environ.get("XDG_STATE_HOME", "").strip() or str(Path.home() / ".local" / "state")
    return Path(state).expanduser() / "lockstep" / _main_checkout(root).name


def log(root: Path, record: dict) -> None:
    """Queue the decision; main() writes it with the exact message the agent receives."""
    _PENDING.append((root, record))


def _write_log(root: Path, record: dict) -> None:
    """Append the record; a folder that cannot be written is reported on stderr and never stops the call."""
    record = {"at": dt.datetime.now(dt.timezone.utc).isoformat(), "tool_use_id": _CALL_ID,
              "project": str(root), "repository": str(_main_checkout(root)), **record}
    try:
        folder = log_dir(root)
        folder.mkdir(parents=True, exist_ok=True)
        with open(folder / f"hook-{dt.date.today().isoformat()}.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
    except (OSError, RuntimeError) as exc:
        print(f"lockstep-hook: could not write the guard log ({exc}); set {LOG_DIR_ENV} to a writable folder",
              file=sys.stderr)


def blocks(root: Path, rel: str) -> bool:
    """True when the hook refuses rather than warns for `rel`: PCW_MODE=block, or a `fixed` glob in the side file matches it.

    A side file that cannot be read counts as blocking, so a broken file cannot let a fixed file through.
    """
    if os.environ.get("PCW_MODE", "warn").strip().lower() == "block":
        return True
    try:
        side = load_side_file(root)
    except ValueError:
        return True
    return side is not None and any(fnmatch.fnmatchcase(rel, g) for g in side.fixed)


def _with_allowed(root: Path, rel: str, reason: str) -> str:
    """`reason` followed by the files the plan does allow, so the agent sees what it may write instead."""
    listing = allowed_listing(root, rel)
    return f"{reason}\n\n{listing}" if listing else reason


def _refuse_or_warn(root: Path, rel_files: list[str], record: dict, reason: str, extra: str | None = None) -> dict:
    """Deny when any of `rel_files` blocks; otherwise allow, hand the refusal over as a warning, log would_block."""
    reason = f"{reason}\n\n{_LAYOUT_POINTER if has_layout(root) else _WIKI_POINTER}"
    if any(blocks(root, r) for r in rel_files):
        log(root, {**record, "decision": "deny"})
        return _out("deny", reason, extra)
    log(root, {**record, "decision": "would_block"})
    return _out("allow", None, WARN_PREFIX + reason + (f"\n\n{extra}" if extra else ""))


def _rel_in_root(root: Path, path: Path) -> str | None:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except (ValueError, OSError):
        return None


def _log_entry_writes(root: Path, cwd: Path, command: str) -> list[str]:
    """The change-log paths (relative to root) that `command` writes, by the paths `lockstep.shell_targets` finds.

    A command that only names an entry (`git add <entry> && git commit -m "... rm ..."`, `cat <entry>`)
    does not write it; `rm` and `git rm` of an entry count, since append-only history is never removed.
    """
    hits: list[str] = []
    for path in written_paths(command, cwd) + _removed_paths(command, cwd):
        rel = _rel_in_root(root, path)
        if rel and entry_edit_reason(root, rel) and rel not in hits:
            hits.append(rel)
    return hits


def _removed_paths(command: str, cwd: Path) -> list[Path]:
    """Paths named by `rm` and `git rm` simple commands, resolved against `cwd`."""
    from lockstep.shell_targets import segments
    out: list[Path] = []
    for segment in segments(command):
        try:
            words = shlex.split(segment.split("\n", 1)[0])
        except ValueError:
            continue
        while words and (words[0] in {"sudo", "command", "env"} or "=" in words[0]):
            words = words[1:]
        if words[:2] == ["git", "rm"]:
            words = words[1:]
        if words[:1] == ["rm"]:
            out += [Path(w) if Path(w).is_absolute() else cwd / w for w in words[1:] if not w.startswith("-")]
    return out


def _ignored(root: Path, rel: str) -> bool:
    import subprocess
    try:
        return subprocess.run(["git", "-C", str(root), "check-ignore", "-q", "--", rel],
                              capture_output=True, timeout=10).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def _shell_write_targets(root: Path, cwd: Path, command: str) -> list[str]:
    """Files inside the project (relative to `root`) that `command` writes, following `cd`; git-ignored ones left out.

    Shell parsing, not meaning (`lockstep.shell_targets`, ported from code2check's guard): redirect and
    tee targets, what `mv`, `touch`, `cp` (destination only), `sed -i` and the like write, and the paths
    named by code in the command that calls something that writes.
    """
    hits: list[str] = []
    for path in written_paths(command, cwd):
        rel = _rel_in_root(root, path)
        if rel is None or rel in hits or rel == "." or path.is_dir() or _ignored(root, rel):
            continue
        hits.append(rel)
    return hits


_PY_PATH = re.compile(r"[\w./-]+\.py\b")


def _shell_spec_text(call: dict, cwd: Path, command: str) -> dict | None:
    """With OpenSpec specs and no plan: hand over the requirement text of each implementing file the command names.

    Agents read and rewrite files from the shell (`cat`, `cat > f <<EOF`, `sed -i`) as often as with the edit tool,
    so the text must reach them on both routes. The named files are the shell parser's write targets plus each
    `.py` path in the command, resolved after its `cd`s; nothing is refused.

    Implements: lockstep-guard/agents-get-requirement-text-from-the-shell-too

    Requirement text (generated):
        lockstep-guard/agents-get-requirement-text-from-the-shell-too: In a repository with OpenSpec
            specs and no layout plan, the edit hook SHALL answer a shell command that names or
            writes a file whose docstrings carry `Implements:` lines with those requirements' text,
            without a `permissionDecision`, and SHALL log the call as `openspec_text` with the
            requirement IDs; a command naming no such file and no file a decision governs SHALL get
            no answer.
    """
    spec_root = find_spec_root(cwd)
    if spec_root is None:
        return None
    names = set(_shell_write_targets(spec_root, cwd, command))
    dirs = [cwd] + [cwd / d for d in re.findall(r"\bcd\s+([\w./-]+)", command)]
    for token in _PY_PATH.findall(command):
        for base in dirs:
            path = (base / token).resolve()
            if path.is_file() and path.is_relative_to(spec_root.resolve()):
                names.add(path.relative_to(spec_root.resolve()).as_posix())
    ids: list[str] = []
    decisions: list[str] = []
    texts: list[str] = []
    for rel in sorted(names):
        found, text = requirement_packet(spec_root, spec_root / rel)
        governing, governed = decision_packet(spec_root, rel, found)
        ids += [i for i in found if i not in ids]
        decisions += [d for d in governing if d not in decisions]
        texts += [x for x in (text, governed) if x]
    if not texts:
        return None
    log(spec_root, {"tool": call.get("tool_name"), "files": sorted(names), "decision": "allow",
                    "why": "openspec_text", "requirements": ids, **({"decisions": decisions} if decisions else {})})
    return _out("allow", None, "\n\n".join(texts))


def decide_shell(call: dict, command: str) -> dict | None:
    """A shell command that names a planned file: hand over its plan; refuse writes (they would skip this hook).

    A shell write to a file the plan does not declare (a new module from `echo x > ...`) gets the same
    answer as an edit to it (Q22). A write the plan has no rule for is let through and logged.
    """
    from lockstep.aes_bridge import target

    cwd = Path(call.get("cwd") or os.getcwd())
    root = find_root(cwd)
    if root is None:
        return _shell_spec_text(call, cwd, command)
    entries = _log_entry_writes(root, cwd, command)
    if entries:
        log(root, {"tool": call.get("tool_name"), "files": entries, "decision": "deny", "why": "log_entry"})
        return _out("deny", entry_edit_reason(root, entries[0]))
    targets = _shell_write_targets(root, cwd, command)
    unplanned = [(rel, why) for rel in targets for why in [unplanned_reason(root, rel)] if why]
    if unplanned:
        rels = [rel for rel, _ in unplanned]
        reason = f"This command writes {', '.join(rels)} from the shell. {unplanned[0][1]}"
        return _refuse_or_warn(root, rels, {"tool": call.get("tool_name"), "files": rels, "why": "shell_unplanned"},
                               _with_allowed(root, rels[0], reason))
    named = [(a["locator"]["exact_path"], a["id"]) for a in target(root).get("planned_artifacts") or []
             if a.get("locator", {}).get("exact_path")
             and (a["locator"]["exact_path"] in command or a["locator"]["exact_path"] in targets)]
    if not named:
        if targets:
            log(root, {"tool": call.get("tool_name"), "files": targets, "decision": "pass", "why": "shell_write_unruled"})
        return None
    written = [r for r, _ in named if r in targets]
    if written:
        names = ", ".join(written)
        return _refuse_or_warn(root, written, {"tool": call.get("tool_name"), "files": [r for r, _ in named], "why": "shell_write"},
                               f"This command writes {names}, a planned file, from the shell, which skips the plan check. "
                               "Use the Edit tool for planned files so you are handed their requirement first.")
    texts = []
    for rel, art in named:
        _, _, spec_text = _spec_packet(root, root / rel)
        texts.append(spec_text or f"Plan for {rel} ({art}), from {plan_name(root)}:\n" + "\n".join(render(context(root, art))[2:]))
    log(root, {"tool": call.get("tool_name"), "files": [r for r, _ in named], "decision": "allow", "why": "shell_read"})
    return _out("allow", None, "\n\n".join(texts))


def _spec_packet(start: Path, path: Path) -> tuple[Path | None, list[str], str]:
    """(spec root, IDs, text) of the OpenSpec requirements `path` implements (behavior 3.7); no root, [] and "" without specs."""
    spec_root = find_spec_root(start)
    if spec_root is None:
        return None, [], ""
    return (spec_root, *requirement_packet(spec_root, path))


def _changes(root: Path) -> str:
    """Behavior 3.5's list of every file the plan change touches; the refusal still goes out if it fails."""
    try:
        return render_changes(change_list(root))
    except Exception as exc:  # noqa: BLE001 - the stale refusal must reach the agent either way
        return f"(The list of files this plan change touches could not be built: {exc})"


def decide(call: dict) -> dict | None:
    command = shell_command(call)
    if command is not None:
        return decide_shell(call, command)
    cwd = Path(call.get("cwd") or os.getcwd())
    allowed: list[str] = []  # each allowed path's text; a later path in the same call can still be refused
    for raw in paths_from_call(call):
        path = Path(raw) if Path(raw).is_absolute() else cwd / raw
        start = path.parent if path.parent.exists() else cwd
        root = find_root(start)
        spec_root, spec_ids, spec_text = _spec_packet(start, path)
        if root is None:
            # OpenSpec specs and no AES plan: the requirement text is all there is to hand over.
            if spec_root is None:
                continue
            rel = path.resolve().relative_to(spec_root.resolve()).as_posix()
            governing, governed = decision_packet(spec_root, rel, spec_ids)
            if not spec_ids and not governing:
                continue
            log(spec_root, {"file": rel, "decision": "allow", "why": "openspec_text", "requirements": spec_ids,
                            **({"decisions": governing} if governing else {})})
            allowed.append("\n\n".join(x for x in (spec_text, governed) if x))
            continue
        rel = path.resolve().relative_to(root.resolve()).as_posix()
        governing, governed = decision_packet(spec_root, rel, spec_ids) if spec_root is not None else ([], "")
        entry = entry_edit_reason(root, rel)
        if entry:
            log(root, {"file": rel, "decision": "deny", "why": "log_entry"})
            return _out("deny", entry)
        hand = _plan_edit(call, root, rel, path)
        if hand:
            return _refuse_or_warn(root, [rel], {"file": rel, "why": "plan_edit"}, hand)
        unplanned = unplanned_reason(root, rel)
        if unplanned:
            return _refuse_or_warn(root, [rel], {"file": rel, "why": "unplanned"}, _with_allowed(root, rel, unplanned),
                                   spec_text or None)
        art = artifact_for_path(root, rel)
        if art is None:
            if not spec_ids and not governing:
                continue
            log(root, {"file": rel, "decision": "allow", "why": "openspec_text", "requirements": spec_ids,
                       **({"decisions": governing} if governing else {})})
            allowed.append("\n\n".join(x for x in (spec_text, governed) if x))
            continue
        ctx = context(root, art)
        layout = has_layout(root)
        after = ("After editing: `uv run lockstep check project` (regenerate docstrings)" if layout else
                 "After editing: `make project` (regenerate docstrings) and "
                 + " ".join(f"`aes evidence record {vs['id']}`" for vs in ctx.get("verification_subjects", [])))
        # Behavior 3.7: the requirement text is OpenSpec's when the file implements one, else the plan's.
        packet = "\n".join([spec_text or f"Plan for {rel} ({art}), from {plan_name(root)}:\n" + "\n".join(render(ctx)[2:]),
                            *(["", governed] if governed else []), "", after])
        stale = projection_stale(root, rel)
        if stale and stops_edits():
            reason = (f"The generated requirement text in {rel} is out of date with the plan ({stale}). Run "
                      f"`uv run lockstep check project` to regenerate it, then retry.\n\n{packet}" if layout
                      else stale_reason(rel, stale, packet) + "\n\n" + _changes(root))
            return _refuse_or_warn(root, [rel], {"file": rel, "artifact": art, "why": "stale_projection"}, reason)
        added = _added_symbols(call, root, rel, path)
        if added:
            return _refuse_or_warn(root, [rel], {"file": rel, "artifact": art, "why": "symbols"}, " ".join(added), packet)
        log(root, {"file": rel, "artifact": art, "decision": "allow", "stale": bool(stale),
                   "text_from": "openspec" if spec_ids else "aes", **({"requirements": spec_ids} if spec_ids else {}),
                   **({"decisions": governing} if governing else {})})
        allowed.append(packet)
    return _out("allow", None, "\n\n".join(x for x in allowed if x)) if allowed else None


def _plan_edit(call: dict, root: Path, rel: str, path: Path) -> str | None:
    """Behavior 3.8: an edit by hand to the plan file, with every file and symbol linked to what it changes."""
    from lockstep.plan_edit import plan_edit_reason
    from lockstep.symbol_gate import text_after

    after = text_after(call, path) if rel == ".aes/target.yaml" else None
    return plan_edit_reason(root, rel, after) if after is not None else None


def _added_symbols(call: dict, root: Path, rel: str, path: Path) -> list[str]:
    """Behavior 5.5: what this edit adds against the plan's exports and declared signatures."""
    from lockstep.symbol_gate import added_symbol_problems, text_after

    after = text_after(call, path)
    if after is None:
        return []
    try:
        before = path.read_text(encoding="utf-8")
    except OSError:
        before = None
    return added_symbol_problems(root, rel, after, before)


def _out(decision: str, reason: str | None, extra: str | None = None) -> dict:
    _LAST["message"] = reason or extra
    hso: dict = {"hookEventName": "PreToolUse", "permissionDecision": decision}
    if reason:
        hso["permissionDecisionReason"] = reason
    if extra:
        hso["additionalContext"] = extra
    return {"hookSpecificOutput": hso}


def would_block_counts(root: Path, days: int = 14) -> dict[str, int]:
    """Per day (ISO date), how many hook decisions in the last `days` days were would_block; days with none are left out."""
    since = dt.date.today() - dt.timedelta(days=days - 1)
    counts: dict[str, int] = {}
    repository = str(_main_checkout(root))
    folders = dict.fromkeys(f.resolve() for f in (log_dir(root), root / LOG_DIR, root / OLD_LOG_DIR))
    for path in sorted(p for folder in folders for p in folder.glob("hook-*.jsonl")):
        day = path.stem.removeprefix("hook-")
        try:
            if dt.date.fromisoformat(day) < since:
                continue
        except ValueError:
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                rec = json.loads(line)
                # a shared folder holds every worktree and any same-named repository; count this one only
                if rec.get("decision") == "would_block" and rec.get("repository", repository) == repository:
                    counts[day] = counts.get(day, 0) + 1
            except (ValueError, AttributeError):
                continue
    return counts


def _print_counts(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="pcw-hook --would-block",
                                     description="Per-day count of edits the hook would have refused (warn mode).")
    parser.add_argument("--would-block", action="store_true")
    parser.add_argument("--days", type=int, default=14)
    args = parser.parse_args(argv)
    root = find_root(Path.cwd()) or Path.cwd()
    counts = would_block_counts(root, args.days)
    today = dt.date.today()
    for back in range(args.days - 1, -1, -1):
        day = (today - dt.timedelta(days=back)).isoformat()
        print(f"{day} {counts.get(day, 0)}")
    print(f"total {sum(counts.values())} would_block in {args.days} days ({log_dir(root)})")
    return 0


_COMMAND_CHARS = 500  # how much of a shell command a log line keeps: enough to read what the call did


def _log_pass(call: dict) -> None:
    """Log a call the hook let through with nothing to say (`"decision": "pass"`), in the project it touches; none outside a project."""
    cwd = Path(call.get("cwd") or os.getcwd())
    paths = [Path(raw) if Path(raw).is_absolute() else cwd / raw for raw in paths_from_call(call)]
    start = next((p.parent for p in paths if p.parent.exists()), cwd)
    root = find_root(start)
    if root is None:
        return
    files = []
    for path in paths:
        try:
            files.append(path.resolve().relative_to(root.resolve()).as_posix())
        except (ValueError, OSError):
            files.append(str(path))
    log(root, {"tool": call.get("tool_name"), "files": files, "decision": "pass", "why": "no_rule"})


def main() -> int:
    if "--would-block" in sys.argv[1:]:
        return _print_counts(sys.argv[1:])
    parser = argparse.ArgumentParser(prog="pcw-hook")
    parser.add_argument("--client", choices=("claude", "codex", "openhands"), default="claude")
    args = parser.parse_args()
    call = json.load(sys.stdin)
    if args.client == "openhands" and not call.get("cwd"):
        call["cwd"] = call.get("working_dir") or os.getcwd()
    global _CALL_ID
    _CALL_ID = call.get("tool_use_id")
    _PENDING.clear()  # one call per run; a decision queued outside main() (a direct decide()) is not this call's
    tool_input = call.get("tool_input") or {}
    if (args.client == "openhands" and call.get("tool_name") == FILE_EDITOR
            and tool_input.get("command") == "view" and tool_input.get("path")):
        # A view is a read: deliver planned context without treating a stale copy
        # or a fixed file as an edit. The shell classifier executes nothing.
        result = decide_shell(call, "cat -- " + shlex.quote(str(tool_input["path"])))
    else:
        result = decide(call)
    if not _PENDING:  # Q21: a call let through with nothing to say is logged too, so the log holds every call seen
        _log_pass(call)
    if _PENDING:  # a decision, or a call let through with no rule for it (Q22, Q21: every pass is logged)
        root, record = _PENDING.pop()
        record["message"] = _LAST.get("message")
        command = shell_command(call)
        if command is not None:
            record.setdefault("command", command[:_COMMAND_CHARS])
        _write_log(root, record)
    if result is not None:
        if args.client == "openhands":
            output = result["hookSpecificOutput"]
            result = {"decision": output.get("permissionDecision", "allow")}
            if output.get("permissionDecisionReason"):
                result["reason"] = output["permissionDecisionReason"]
            if output.get("additionalContext"):
                result["additionalContext"] = output["additionalContext"]
        elif args.client in ("codex", "claude"):
            # Codex rejects permissionDecision:allow without updatedInput and drops
            # its context. A context-only result passes without approving an edit;
            # supported deny/reason output remains intact. Claude Code reads an allow
            # as approving the call past the user's own permission prompt, so it gets
            # the same context-only answer. Internal verdicts are unchanged.
            output = dict(result["hookSpecificOutput"])
            if output.get("permissionDecision") == "allow":
                output.pop("permissionDecision")
                output.pop("permissionDecisionReason", None)
            result = {**result, "hookSpecificOutput": output}
        print(json.dumps(result))
    elif args.client == "openhands":
        print(json.dumps({"decision": "allow"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

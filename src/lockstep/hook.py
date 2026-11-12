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
Every call the hook sees is appended to `.pcw/hook-<date>.jsonl` in the project: each decision, a
shell write the plan has no rule for, and a call it lets through with nothing to say (`"decision":
"pass"`), with the first characters of a shell command (Q21). Shell parsing misses a write whose path is built at run
time; `pcw check` before the commit stays the guarantee.

[[[cog import lockstep.cogtext as c; c.docstring("ART-HOOK", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

Part of REQ-5: Links are checked both ways on every change: links between
  requirement, criterion, test, file and symbol are checked in both
  directions on every change, at edit time (the hook) and before commit
  (`pcw check`); an unplanned or stale item is refused.
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
Proven by: VS-5.1-a (tests/test_hook.py)
Declares (typed signatures, from the plan):
  EDIT_TOOLS
  SHELL_TOOLS
  FILE_EDITOR
  PATCH_PATH
  REDIRECT
  TEE
  IN_PLACE
  WARN_PREFIX
  shell_writes(command: str, path: str) -> bool
  paths_from_call(call: dict) -> list[str]
  shell_command(call: dict) -> str | None
  log(root: Path, record: dict) -> None
  blocks(root: Path, rel: str) -> bool
  decide_shell(call: dict, command: str) -> dict | None
  decide(call: dict) -> dict | None
  would_block_counts(root: Path, days: int = 14) -> dict[str, int]
  main() -> int
[[[end]]] (sum: lKpqI7g3ID)
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

from lockstep.aes_bridge import artifact_for_path, context, find_root
from lockstep.change_log import entry_edit_reason
from lockstep.cogtext import render
from lockstep.change_list import change_list
from lockstep.change_list import render as render_changes
from lockstep.openspec_text import find_spec_root, requirement_packet
from lockstep.side_file import load_side_file
from lockstep.stale_edit import projection_stale, stale_reason, stops_edits
from lockstep.unplanned_files import unplanned_reason

# Prefixed to the refusal text when the hook only warns (behavior 5.1, decision D7).
WARN_PREFIX = "Lockstep would block this edit (warn mode): "
# Added to every refusal and warning, so an agent that is stopped knows where to look next (behavior 6.1, Q20).
_WIKI_POINTER = ("To see what the plan asks for and which files and tests do it, start from the project's wiki: "
                 "`python -m lockstep.wiki` prints it, each section a question linking down to the requirement, its files and its test.")

EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
SHELL_TOOLS = {"Bash", "shell", "local_shell", "exec_command",
               "terminal"}  # OpenHands' shell tool; its input is {"command": ...}
# OpenHands' file tool: {"command": "view"|"create"|"str_replace"|"insert"|"undo_edit", "path": ...}.
FILE_EDITOR = "file_editor"
PATCH_PATH = re.compile(r"^\*\*\* (?:Update|Add|Delete) File: (.+)$", re.M)
# Shell commands that write files. Regex over command text (code), not prose.
REDIRECT = re.compile(r"(?:^|\s)\d?>>?(?!&)\s*([^\s;&|]+)")
TEE = re.compile(r"\btee\s+(?:-a\s+)?([^\s;&|]+)")
IN_PLACE = re.compile(r"\bsed\s+-i|\bperl\s+-[a-z]*i|\bmv\b|\bcp\b|\brm\b|\btruncate\b|\btouch\b|"
                      r"\bpython3?\s+-(?:\s|$|c)|\bpython3?\s+-\s*<<|open\(|write_text|\.write\(")


def shell_writes(command: str, path: str) -> bool:
    """True when the command writes `path`: redirected or tee'd into it, or an in-place/scripted write naming it."""
    targets = REDIRECT.findall(command) + TEE.findall(command)
    if any(t.strip("'\"").endswith(path) for t in targets):
        return True
    return path in command and bool(IN_PLACE.search(command))


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


def log(root: Path, record: dict) -> None:
    """Queue the decision; main() writes it with the exact message the agent receives."""
    _PENDING.append((root, record))


def _write_log(root: Path, record: dict) -> None:
    folder = root / ".pcw"
    folder.mkdir(exist_ok=True)
    day = dt.date.today().isoformat()
    record = {"at": dt.datetime.now(dt.timezone.utc).isoformat(), "tool_use_id": _CALL_ID, **record}
    with open(folder / f"hook-{day}.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


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


def _refuse_or_warn(root: Path, rel_files: list[str], record: dict, reason: str, extra: str | None = None) -> dict:
    """Deny when any of `rel_files` blocks; otherwise allow, hand the refusal over as a warning, log would_block."""
    reason = f"{reason}\n\n{_WIKI_POINTER}"
    if any(blocks(root, r) for r in rel_files):
        log(root, {**record, "decision": "deny"})
        return _out("deny", reason, extra)
    log(root, {**record, "decision": "would_block"})
    return _out("allow", None, WARN_PREFIX + reason + (f"\n\n{extra}" if extra else ""))


_SEGMENT = re.compile(r"&&|\|\||[;|\n]")  # splits a command line into simple commands
_TOKEN = re.compile(r"[^\s;&|<>()]+")


def _log_entry_writes(root: Path, cwd: Path, command: str) -> list[str]:
    """The change-log paths (relative to root) that a simple command in `command` writes.

    Each simple command is judged on its own, so `git add <entry> && git commit -m "... rm ..."`
    is not read as removing the entry, while `git rm <entry>` or `> <entry>` is.
    """
    hits: list[str] = []
    for segment in _SEGMENT.split(command):
        for token in {t.strip("'\"") for t in _TOKEN.findall(segment)}:
            if not token or token.startswith("-"):
                continue
            path = Path(token) if Path(token).is_absolute() else cwd / token
            try:
                rel = path.resolve().relative_to(root.resolve()).as_posix()
            except (ValueError, OSError):
                continue
            if entry_edit_reason(root, rel) and shell_writes(segment, token) and rel not in hits:
                hits.append(rel)
    return hits


_HEREDOC = re.compile(r"<<-?\s*(['\"]?)(\w+)\1")
_CD = re.compile(r"^\s*\(?\s*(?:cd|pushd)\s+(?:--\s+)?(['\"]?)([^\s'\";&|()]+)\1\s*\)?\s*$")
_LITERAL = re.compile(r"['\"]([^'\"\s]+)['\"]")
_PATHLIKE = re.compile(r"^[\w.@+/-]+$")
_FILE_NAME = re.compile(r"(?:/|\.[A-Za-z0-9]+$)")
_REDIRECTS = {">", ">>", ">|", "&>", "&>>"}


def _simple_commands(command: str) -> list[tuple[str, str]]:
    """Each simple command in `command` with the here-document body it reads, in order.

    A here-document's body is data, not commands: `if a > b:` inside `cat > f.py <<EOF` is not a redirect.
    """
    lines, i = command.split("\n"), 0
    out: list[tuple[str, str]] = []
    while i < len(lines):
        line, body = lines[i], []
        i += 1
        for m in _HEREDOC.finditer(line):
            while i < len(lines) and lines[i].strip() != m.group(2):
                body.append(lines[i])
                i += 1
            i += 1
        out.extend((seg, "\n".join(body) if "<<" in seg else "") for seg in _SEGMENT.split(line))
    return out


def _words(segment: str) -> list[str] | None:
    """The segment's shell words, with redirection operators as words of their own; None if it does not parse."""
    try:
        lex = shlex.shlex(segment, posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        return list(lex)
    except ValueError:
        return None


def _segment_targets(segment: str, body: str) -> tuple[list[str], list[str]]:
    """(files the segment surely writes, file names a scripted or in-place write in it may create).

    The first are redirect and tee targets. The second are path-like words and quoted strings of a
    command that writes files in place or from a script (IN_PLACE); the caller counts one only when
    no such file exists yet, so reading or copying an existing file is not taken for creating one.
    """
    words = _words(segment)
    if words is None:  # unbalanced quotes: fall back to the command-text patterns
        return [t.strip("'\"") for t in REDIRECT.findall(segment) + TEE.findall(segment)], []
    sure = [words[k + 1] for k, w in enumerate(words[:-1]) if w in _REDIRECTS]
    if "tee" in words:
        for w in words[words.index("tee") + 1:]:
            if w and w[0] in "|;&<>()":
                break
            if not w.startswith("-"):
                sure.append(w)
    maybe: list[str] = []
    if IN_PLACE.search(segment + "\n" + body) and (words[:1] or [""])[0] != "rm":
        maybe = [w for w in words[1:] if not w.startswith("-")] + _LITERAL.findall(segment + "\n" + body)
        maybe = [w for w in maybe if _PATHLIKE.match(w) and _FILE_NAME.search(w)]
    return sure, maybe


def _ignored(root: Path, rel: str) -> bool:
    import subprocess
    try:
        return subprocess.run(["git", "-C", str(root), "check-ignore", "-q", "--", rel],
                              capture_output=True, timeout=10).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def _shell_write_targets(root: Path, cwd: Path, command: str) -> list[str]:
    """Files inside the project (relative to `root`) that `command` writes, following `cd`; git-ignored ones left out.

    Shell parsing, not meaning: redirect and tee targets, and new files named by an in-place or
    scripted write (`touch`, `cp`, `mv`, `sed -i`, `python -c`, a python here-document's `open(...)`).
    """
    hits: list[str] = []
    here = cwd
    for segment, body in _simple_commands(command):
        cd = _CD.match(segment)
        if cd:
            step = Path(os.path.expanduser(cd.group(2)))
            here = step if step.is_absolute() else here / step
            continue
        sure, maybe = _segment_targets(segment, body)
        for word, must in [(w, True) for w in sure] + [(w, False) for w in maybe]:
            path = Path(word) if Path(word).is_absolute() else here / word
            try:
                rel = path.resolve().relative_to(root.resolve()).as_posix()
            except (ValueError, OSError):
                continue
            if rel in hits or rel == "." or path.is_dir() or (not must and path.exists()) or _ignored(root, rel):
                continue
            hits.append(rel)
    return hits


def decide_shell(call: dict, command: str) -> dict | None:
    """A shell command that names a planned file: hand over its plan; refuse writes (they would skip this hook).

    A shell write to a file the plan does not declare (a new module from `echo x > ...`) gets the same
    answer as an edit to it (Q22). A write the plan has no rule for is let through and logged.
    """
    from lockstep.aes_bridge import target

    cwd = Path(call.get("cwd") or os.getcwd())
    root = find_root(cwd)
    if root is None:
        return None
    entries = _log_entry_writes(root, cwd, command)
    if entries:
        log(root, {"tool": call.get("tool_name"), "files": entries, "decision": "deny", "why": "log_entry"})
        return _out("deny", entry_edit_reason(root, entries[0]))
    targets = _shell_write_targets(root, cwd, command)
    unplanned = [(rel, why) for rel in targets for why in [unplanned_reason(root, rel)] if why]
    if unplanned:
        rels = [rel for rel, _ in unplanned]
        return _refuse_or_warn(root, rels, {"tool": call.get("tool_name"), "files": rels, "why": "shell_unplanned"},
                               f"This command writes {', '.join(rels)} from the shell. {unplanned[0][1]}")
    named = [(a["locator"]["exact_path"], a["id"]) for a in target(root).get("planned_artifacts") or []
             if a.get("locator", {}).get("exact_path")
             and (a["locator"]["exact_path"] in command or a["locator"]["exact_path"] in targets)]
    if not named:
        if targets:
            log(root, {"tool": call.get("tool_name"), "files": targets, "decision": "pass", "why": "shell_write_unruled"})
        return None
    written = [r for r, _ in named if r in targets or shell_writes(command, r)]
    if written:
        names = ", ".join(written)
        return _refuse_or_warn(root, written, {"tool": call.get("tool_name"), "files": [r for r, _ in named], "why": "shell_write"},
                               f"This command writes {names}, a planned file, from the shell, which skips the plan check. "
                               "Use the Edit tool for planned files so you are handed their requirement first.")
    texts = []
    for rel, art in named:
        _, _, spec_text = _spec_packet(root, root / rel)
        texts.append(spec_text or f"Plan for {rel} ({art}), from .aes/target.yaml:\n" + "\n".join(render(context(root, art))[2:]))
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
    for raw in paths_from_call(call):
        path = Path(raw) if Path(raw).is_absolute() else cwd / raw
        start = path.parent if path.parent.exists() else cwd
        root = find_root(start)
        spec_root, spec_ids, spec_text = _spec_packet(start, path)
        if root is None:
            # OpenSpec specs and no AES plan: the requirement text is all there is to hand over.
            if spec_root is None or not spec_ids:
                continue
            rel = path.resolve().relative_to(spec_root.resolve()).as_posix()
            log(spec_root, {"file": rel, "decision": "allow", "why": "openspec_text", "requirements": spec_ids})
            return _out("allow", None, spec_text)
        rel = path.resolve().relative_to(root.resolve()).as_posix()
        entry = entry_edit_reason(root, rel)
        if entry:
            log(root, {"file": rel, "decision": "deny", "why": "log_entry"})
            return _out("deny", entry)
        hand = _plan_edit(call, root, rel, path)
        if hand:
            return _refuse_or_warn(root, [rel], {"file": rel, "why": "plan_edit"}, hand)
        unplanned = unplanned_reason(root, rel)
        if unplanned:
            return _refuse_or_warn(root, [rel], {"file": rel, "why": "unplanned"}, unplanned, spec_text or None)
        art = artifact_for_path(root, rel)
        if art is None:
            if not spec_ids:
                continue
            log(root, {"file": rel, "decision": "allow", "why": "openspec_text", "requirements": spec_ids})
            return _out("allow", None, spec_text)
        ctx = context(root, art)
        after = ("After editing: `make project` (regenerate docstrings) and "
                 + " ".join(f"`aes evidence record {vs['id']}`" for vs in ctx.get("verification_subjects", [])))
        # Behavior 3.7: the requirement text is OpenSpec's when the file implements one, else the plan's.
        packet = "\n".join([spec_text or f"Plan for {rel} ({art}), from .aes/target.yaml:\n" + "\n".join(render(ctx)[2:]), "", after])
        stale = projection_stale(root, rel)
        if stale and stops_edits():
            return _refuse_or_warn(root, [rel], {"file": rel, "artifact": art, "why": "stale_projection"},
                                   stale_reason(rel, stale, packet) + "\n\n" + _changes(root))
        added = _added_symbols(call, root, rel, path)
        if added:
            return _refuse_or_warn(root, [rel], {"file": rel, "artifact": art, "why": "symbols"}, " ".join(added), packet)
        log(root, {"file": rel, "artifact": art, "decision": "allow", "stale": bool(stale),
                   "text_from": "openspec" if spec_ids else "aes", **({"requirements": spec_ids} if spec_ids else {})})
        return _out("allow", None, packet)
    return None


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
    for path in sorted((root / ".pcw").glob("hook-*.jsonl")):
        day = path.stem.removeprefix("hook-")
        try:
            if dt.date.fromisoformat(day) < since:
                continue
        except ValueError:
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                if json.loads(line).get("decision") == "would_block":
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
    print(f"total {sum(counts.values())} would_block in {args.days} days ({root / '.pcw'})")
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
        elif args.client == "codex":
            # Codex rejects permissionDecision:allow without updatedInput and drops
            # its context. A context-only result passes without approving an edit;
            # supported deny/reason output remains intact. Internal verdicts and
            # Claude's wire format are unchanged.
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

"""`lockstep reads TRANSCRIPT`: each write a session made to a repository file, with what it read first.

Reads a finished Claude Code or Codex session file and reports, for each write, whether the session read the file,
read its requirement context (its `generated/wiki/<capability>.md` page or the capability's spec), and got the edit
hook's requirement text on that write. It reports counts and warnings and never blocks (plan "AES next steps",
Milestone 1 step 4). It reads command text (code), never prose.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:read_before_write.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-read-before-write/a-session-s-writes-are-listed-with-what-was-read-first, lockstep-read-before-write/claude-and-codex-session-files-are-both-read

### Requirement: A session's writes are listed with what was read first

`lockstep reads TRANSCRIPT` SHALL list, in session order, each write to a file inside the repository (`--repo`,
default the current folder) with three marks: whether the session read that file before the write; whether it
read the file's requirement context before the write, meaning the `generated/wiki/<capability>.md` page or the
`openspec/specs/<capability>/spec.md` of a capability named by the file's `Implements:` lines; and whether the
edit hook's requirement text was attached to that write. A write that created the file SHALL be marked `new`:
the Write tool's result says so, a Codex file change says `add`, and for a shell write git had not yet recorded
the file when the call was made. A file the session wrote whole (the Write tool, or a shell write that created it)
counts as read for its later writes. It
SHALL print one warning line for each write to an existing file with neither read, end with
`RESULT writes=N new=N file_read_first=N context_read_first=N handover=N unread=N`, give the same rows as JSON with
`--json`, and exit 0 whatever it finds; an unreadable transcript SHALL exit 2.

Source: Brian, 2026-11-27, plan doc "AES next steps: plan for discussion", Milestone 1 step 4 ("Read-before-write
measured, not forced ... report it as a count and a warning, never a block"); exit codes and the `new` mark
inferred by agent.

#### Scenario: An edit after reading only the file is counted and not warned

- **WHEN** a Claude transcript reads `src/greet.py` with the Read tool and then edits it, and `src/greet.py`
  implements `greeter/the-greeter-says-hello`
- **THEN** the row is marked file read first and not context read first, no warning is printed for it, and the
  command exits 0

#### Scenario: A write with nothing read first is warned but not blocked

- **WHEN** a transcript rewrites an existing `src/greet.py` with a shell redirect and reads nothing first
- **THEN** a warning line names `src/greet.py`, the `RESULT` line counts `unread=1`, and the command exits 0

#### Scenario: Reading the wiki page counts as context

- **WHEN** a transcript runs `cat generated/wiki/greeter.md` and then edits `src/greet.py`
- **THEN** the row is marked context read first

#### Scenario: The hand-over is marked

- **WHEN** a Claude transcript has a `hook_additional_context` attachment holding Lockstep's requirement text
  right after an edit of `src/greet.py`
- **THEN** that row is marked handover

#### Scenario: A created file is new, not unread

- **WHEN** a transcript writes `src/new_mod.py` with the Write tool and the result says the file was created
- **THEN** the row is marked `new` and no warning is printed for it

#### Scenario: An unreadable transcript exits 2

- **WHEN** the transcript path does not exist
- **THEN** the command exits 2

### Requirement: Claude and Codex session files are both read

`lockstep reads` SHALL read the four session formats the agents write: a Claude Code transcript and a
`claude -p --output-format stream-json` stream (Read, Edit, MultiEdit, Write, NotebookEdit and Bash calls), and a
Codex rollout file and a `codex exec --json` stream (command executions and file changes). Shell reads SHALL be
found from the command's read commands (`cat`, `head`, `tail`, `sed` without `-i`, `nl`, `less`, `grep`, `rg`) or,
in a Codex rollout, from Codex's own `parsed_cmd` read entries. Shell writes SHALL be the sure ones the existing
shell target parser finds (redirect and tee targets, and what `mv`, `sed -i` and the like write, in a folder that
exists); paths that code inside a command merely names SHALL NOT count, because which of them the code writes is
unknown. A relative path SHALL be read against the folder the call was made in.

Source: Brian, 2026-11-27, core rule "Claude and Codex behave the same" (code2-workspace `agents/core.md`,
Records); the list of read commands inferred by agent.

#### Scenario: A Codex exec stream is read

- **WHEN** a `codex exec --json` stream holds a `command_execution` of `cat src/greet.py` and then a
  `file_change` updating `src/greet.py`
- **THEN** the row is marked file read first

#### Scenario: A Codex rollout uses Codex's own read parse

- **WHEN** a Codex rollout holds a `CommandExecution` whose `parsed_cmd` has a read of `src/greet.py`, then a
  `FileChange` of that file
- **THEN** the row is marked file read first

Tested by: tests/lockstep/test_read_before_write.py

Declares (typed signatures, from the plan):
  shell_reads(command: str, cwd: Path) -> list[Path]
  report(transcript: Path, root: Path) -> list[dict]
  main(argv: list[str] | None = None) -> int
[[[end]]]
"""
from __future__ import annotations

import argparse
import json
import os
import datetime as dt
import shlex
import subprocess
import sys
from functools import cache
from pathlib import Path

from lockstep.openspec_text import implemented_ids
from lockstep.shell_targets import _CD, _head, _redirect_targets, command_writes, segments

_READERS = {"cat", "head", "tail", "nl", "less", "more", "bat", "sed", "grep", "rg", "awk", "wc", "diff"}
_PATTERN_FIRST = {"grep", "rg", "awk", "sed"}  # the first plain word is a pattern or script, not a file
_EDIT_TOOLS = {"Edit", "MultiEdit", "Write", "NotebookEdit"}
# The edit hook's own opening lines (lockstep.openspec_text.requirement_packet; lockstep.hook, the layout plan text).
_HANDOVER = ("Requirement text for ", "Plan for ")
_SHELLS = {"bash", "sh", "zsh", "/bin/bash", "/bin/sh", "/usr/bin/bash", "/bin/zsh"}


def _unwrap(command: str) -> str:
    """`bash -lc 'script'` (how Codex runs commands) becomes `script`."""
    try:
        words = shlex.split(command)
    except ValueError:
        return command
    if len(words) == 3 and words[0] in _SHELLS and words[1] in ("-c", "-lc"):
        return words[2]
    return command


def _drop_redirects(words: list[str]) -> list[str]:
    """The words without redirect operators and their targets (`cat > f <<EOF` reads nothing from `f`)."""
    out, skip = [], False
    for w in words:
        if skip:
            skip = False
        elif w and w[0] in "<>" or w in ("&>", "2>", "1>"):
            skip = True
        elif w in ("|", "&", ";", "(", ")"):
            break
        else:
            out.append(w)
    return out


def _sure_writes(command: str, cwd: Path) -> list[Path]:
    """Files a shell command certainly writes: redirect and tee targets and what `mv`, `sed -i` and the like write,
    following `cd`. Paths that code inside the command merely names are left out: the guard's parser counts them
    all (it errs toward refusing), but a measure would count every string a script mentions."""
    here, hits = cwd, []
    for segment in segments(command):
        cd = _CD.match(segment)
        if cd:
            step = Path(os.path.expanduser(cd.group(2)))
            here = step if step.is_absolute() else here / step
            continue
        for word in _redirect_targets(_head(segment)) + command_writes(segment.split("\n", 1)[0]):
            if word and not word.startswith("-") and word not in ("/dev/null", "&1", "&2"):
                path = Path(os.path.expanduser(word))
                hits.append(path if path.is_absolute() else here / path)
    return hits


def shell_reads(command: str, cwd: Path) -> list[Path]:
    """The files a shell command reads with a read command, absolute, following `cd` between commands."""
    here, hits = cwd, []
    for segment in segments(_unwrap(command)):
        cd = _CD.match(segment)
        if cd:
            step = Path(os.path.expanduser(cd.group(2)))
            here = step if step.is_absolute() else here / step
            continue
        try:
            lex = shlex.shlex(segment.split("\n", 1)[0], posix=True, punctuation_chars=True)
            lex.whitespace_split = True
            words = _drop_redirects(list(lex))
        except ValueError:
            continue
        if not words or Path(words[0]).name not in _READERS:
            continue
        name, plain = Path(words[0]).name, [w for w in words[1:] if not w.startswith("-")]
        if name == "sed" and any(w.startswith("-i") for w in words[1:]):
            continue
        if name in _PATTERN_FIRST and not any(w in ("-e", "-f") for w in words[1:]):
            plain = plain[1:]
        for word in plain:
            path = Path(os.path.expanduser(word))
            hits.append(path if path.is_absolute() else here / path)
    return hits


def _text(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(c.get("text", "") if isinstance(c, dict) else str(c) for c in content)
    return ""


def _handover(content: object) -> bool:
    text = _text(content)
    return any(marker in text for marker in _HANDOVER)


def _shell(out: list[dict], command: str, cwd: Path) -> None:
    """Reads and writes of one shell command."""
    out += [{"kind": "read", "path": p} for p in shell_reads(command, cwd)]
    # None: a shell write does not say whether it created the file; report() asks git.
    out += [{"kind": "write", "path": p, "new": None} for p in _sure_writes(_unwrap(command), cwd) if p.parent.is_dir()]


def _mark(out: list[dict], start: int, handed: bool) -> None:
    """Mark the hand-over on the writes one call added (`out[start:]`), when the hook gave that call requirement text."""
    if handed:
        out[start:] = [{**ev, "handover": True} if ev["kind"] == "write" else ev for ev in out[start:]]


def _claude_result(out: list[dict], name: str, inp: dict, block: dict, cwd: Path) -> None:
    path = inp.get("file_path") or inp.get("notebook_path")
    if name == "Read" and path:
        out.append({"kind": "read", "path": Path(path)})
    elif name == "Write" and path and not block.get("is_error"):  # the session wrote the whole file, so it knows it
        created = _text(block.get("content")).startswith("File created")
        out += [{"kind": "write", "path": Path(path), "new": created}, {"kind": "read", "path": Path(path)}]
    elif name in _EDIT_TOOLS and path and not block.get("is_error"):
        out.append({"kind": "write", "path": Path(path), "new": False})
    elif name == "Bash":
        _shell(out, inp.get("command", ""), cwd)


def _codex_rollout_item(out: list[dict], it: dict, cwd: Path) -> None:
    here = Path(str(it.get("cwd") or cwd).removeprefix("file://"))
    if it.get("type") == "CommandExecution":
        reads = [p for p in it.get("parsed_cmd") or [] if isinstance(p, dict) and p.get("type") == "read" and p.get("path")]
        if reads:  # Codex's own read parse
            out += [{"kind": "read", "path": here / p["path"]} for p in reads]
        else:
            cmd = it.get("command")
            _shell(out, shlex.join(cmd) if isinstance(cmd, list) else str(cmd or ""), here)
    elif it.get("type") == "FileChange":
        for p, ch in (it.get("changes") or {}).items():
            out.append({"kind": "write", "path": Path(p), "new": (ch or {}).get("type") == "add"})


def _events(records: list[dict], cwd: Path) -> list[dict]:
    """The session as ordered events: {"kind": "read"|"write", "path": Path, "new": bool, "handover": bool}."""
    out: list[dict] = []
    pending: dict[str, tuple[str, dict, Path, str | None]] = {}
    handed: set[str] = set()  # Claude tool calls the edit hook gave requirement text for
    codex_handed = False
    for r in records:
        before = len(out)
        t, msg = r.get("type"), r.get("message") or {}
        payload = r.get("payload") if isinstance(r.get("payload"), dict) else {}
        content = msg.get("content") if isinstance(msg, dict) else None
        if t == "session_meta" and payload.get("cwd"):
            cwd = Path(payload["cwd"])
        elif t == "assistant" and isinstance(content, list):  # Claude: transcript or stream-json
            here = Path(r["cwd"]) if r.get("cwd") else cwd  # the shell's folder when the call was made
            pending.update({b.get("id"): (b.get("name", ""), b.get("input") or {}, here, r.get("timestamp"))
                            for b in content if isinstance(b, dict) and b.get("type") == "tool_use"})
        elif t == "attachment":
            att = r.get("attachment") or {}
            if att.get("type") == "hook_additional_context" and _handover(att.get("content")):
                handed.add(att.get("toolUseID", ""))
        elif t == "user" and isinstance(content, list):
            for b in content:
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    name, inp, here, at = pending.pop(b.get("tool_use_id"), ("", {}, cwd, None))
                    start = len(out)
                    _claude_result(out, name, inp, b, here)
                    _mark(out, start, b.get("tool_use_id") in handed)
                    for ev in out[start:]:
                        ev["at"] = at  # when the call was made: a commit inside the same call comes after the write
        elif t == "item.completed":  # codex exec --json: hook text is not in this stream
            it = r.get("item") or {}
            if it.get("type") == "command_execution":
                _shell(out, str(it.get("command", "")), cwd)
            elif it.get("type") == "file_change":
                out += [{"kind": "write", "path": Path(ch.get("path", "")), "new": ch.get("kind") == "add"}
                        for ch in it.get("changes") or []]
        elif t == "event_msg" and payload.get("type") == "item_completed":  # codex rollout
            it = payload.get("item") or {}
            if it.get("type") in ("CommandExecution", "FileChange"):
                start = len(out)
                _codex_rollout_item(out, it, cwd)
                _mark(out, start, codex_handed)
                codex_handed = False
        elif (t == "response_item" and payload.get("type") == "message" and payload.get("role") == "developer"
              and _handover(payload.get("content"))):
            codex_handed = True  # codex: the hook's text is a developer message just before its call completes
        for ev in out[before:]:
            ev.setdefault("at", r.get("timestamp"))
    return out


def _rel(root: Path, path: Path) -> str | None:
    full = Path(os.path.normpath(path if path.is_absolute() else root / path))
    return full.relative_to(root).as_posix() if full.is_relative_to(root) else None


def _context(root: Path, rel: str) -> set[str]:
    """The paths whose reading counts as reading `rel`'s requirement context."""
    caps = {i.split("/", 1)[0] for i in implemented_ids(root / rel)}
    return {f"generated/wiki/{c}.md" for c in caps} | {f"openspec/specs/{c}/spec.md" for c in caps}


@cache
def _added_at(root: Path, rel: str) -> float | None:
    """When git first recorded `rel` (seconds since the epoch); None when git never did; 0 outside a git repository."""
    run = subprocess.run(["git", "-C", str(root), "log", "--diff-filter=A", "--format=%ct", "--", rel],
                         capture_output=True, text=True, check=False)
    if run.returncode != 0:
        return 0.0  # no history to ask: take the file as already there
    times = [int(t) for t in run.stdout.split()]
    return float(min(times)) if times else None


def _created(root: Path, rel: str, at: str | None) -> bool:
    """Whether a shell write at `at` created `rel`: git had not yet recorded the file at that moment."""
    added = _added_at(root, rel)
    if added is None or not at:
        return added is None
    return dt.datetime.fromisoformat(at.replace("Z", "+00:00")).timestamp() < added


def report(transcript: Path, root: Path) -> list[dict]:
    """One row per write inside `root`, in session order. Raises OSError or ValueError on an unreadable file."""
    root = Path(os.path.normpath(root.resolve()))
    records = [json.loads(line) for line in transcript.read_text(encoding="utf-8").splitlines() if line.strip()]
    read: set[str] = set()
    written: set[str] = set()
    rows: list[dict] = []
    for ev in _events(records, root):
        rel = _rel(root, ev["path"])
        if rel is None:
            continue
        if ev["kind"] == "read":
            read.add(rel)
            continue
        new = ev["new"] if ev["new"] is not None else rel not in written and _created(root, rel, ev.get("at"))
        rows.append({"file": rel, "new": new, "file_read_first": rel in read,
                     "context_read_first": bool(_context(root, rel) & read), "handover": ev.get("handover", False)})
        written.add(rel)
        if new:  # the session wrote the whole file, so later writes know it
            read.add(rel)
    for row in rows:
        row["unread"] = not (row["new"] or row["file_read_first"] or row["context_read_first"])
    return rows


def main(argv: list[str] | None = None) -> int:
    """Print the rows (or `--json`), a warning per unread write and a RESULT line; 0 always, 2 on an unreadable file."""
    parser = argparse.ArgumentParser(prog="lockstep reads", description="Each write in a session, with what was read first.")
    parser.add_argument("transcript", type=Path)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        rows = report(args.transcript, args.repo)
    except (OSError, ValueError) as exc:
        print(f"lockstep reads: cannot read {args.transcript}: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(rows, indent=2))
        return 0
    marks = ("new", "file_read_first", "context_read_first", "handover")
    for row in rows:
        print(f"{row['file']}: {', '.join(m for m in marks if row[m]) or 'nothing read first'}")
    for row in rows:
        if row["unread"]:
            print(f"WARN {row['file']}: written with neither the file nor its requirement page read first")
    n = {k: sum(r[k] for r in rows) for k in (*marks, "unread")}
    print(f"RESULT writes={len(rows)} new={n['new']} file_read_first={n['file_read_first']} "
          f"context_read_first={n['context_read_first']} handover={n['handover']} unread={n['unread']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""`lockstep reads TRANSCRIPT`: each write a session made to a repository file, with what it read first.

Reads a finished Claude Code or Codex session file and reports, for each write, whether the session read the file,
read its requirement context (its `generated/wiki/<capability>.md` page or the capability's spec), and got the edit
hook's requirement text on that write. It reports counts and warnings and never blocks (plan "AES next steps",
Milestone 1 step 4). It reads command text (code), never prose.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:read_before_write.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-guard/a-session-s-writes-are-listed-with-what-was-read-first, lockstep-guard/claude-and-codex-session-files-are-both-read

### Requirement: A session's writes are listed with what was read first

`lockstep reads TRANSCRIPT` SHALL list, in session order, each write to a file inside the repository (`--repo`,
default the current folder) with three marks: whether the session read that file before the write; whether it
read the file's requirement context before the write, meaning the `generated/wiki/<capability>.md` page or the
`openspec/specs/<capability>/spec.md` of a capability named by the file's `Implements:` lines; and whether the
edit hook's requirement text named that file on that write. A write that created the file SHALL be marked `new`:
the Write tool's result says so, a Codex file change says `add`, and for a shell write git had not recorded the
file on any branch before the second the call was made (outside a git repository a shell write is taken as an
overwrite, and an existing file git never saw is taken as new). A file the session wrote whole (the Write tool, or
a shell write that created it) counts as read for its later writes. A call that failed before it ran (a refused
edit, a hook denial) SHALL count as neither a read nor a write; a delete SHALL not count, and a move SHALL count
only its destination. A Claude session's subagent files (`<session>/subagents/agent-*.jsonl`) SHALL be read too,
each agent measured on its own reads. Requirement context is found for Python files only, from their docstrings.
It
SHALL print one warning line for each write to an existing file with neither read, end with
`RESULT writes=N new=N file_read_first=N context_read_first=N handover=N unread=N agents=N`, give the same rows as JSON with
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
exists); paths that code inside a command merely names SHALL NOT count, because
which of them the code writes is unknown. A command's reads and writes SHALL keep the order of its simple commands,
and a Codex command's writes SHALL be found even when Codex parsed reads in it. A relative path SHALL be read
against the folder the call was made in, and paths SHALL be compared after resolving symbolic links. A record that
is not of a known shape SHALL be skipped, never stop the report.

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
import datetime as dt
import json
import math
import os
import shlex
import subprocess
import sys
from functools import cache
from pathlib import Path

from lockstep.openspec_text import implemented_ids
from lockstep.shell_targets import _CD, _head, _redirect_targets, command_writes, segments

_READERS = {"cat", "head", "tail", "nl", "less", "more", "bat", "sed", "grep", "rg", "awk", "wc", "diff"}
_PATTERN_FIRST = {"grep", "rg", "awk", "sed"}  # the first plain word is a pattern or script, not a file
# Per read command, the flags whose next word is a value, not a file (`sed -n` and `grep -n` take none).
_VALUE_FLAGS = {"head": {"-n", "-c"}, "tail": {"-n", "-c"}, "grep": {"-e", "-f", "-m", "-A", "-B", "-C"},
                "rg": {"-e", "-f", "-m", "-A", "-B", "-C", "-g", "-t"}, "sed": {"-e", "-f"}, "awk": {"-f", "-v"}}
_EDIT_TOOLS = {"Edit", "MultiEdit", "Write", "NotebookEdit"}
_MOVES = {"mv"}
# The edit hook's own opening lines (lockstep.openspec_text.requirement_packet; lockstep.hook, the layout plan text):
# "Requirement text for <path>, from OpenSpec ..." and "Plan for <path> (<artifact>), from ...".
_HANDOVER = (("Requirement text for ", ", from "), ("Plan for ", " ("))
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


def _segment_reads(segment: str, here: Path) -> list[Path]:
    try:
        lex = shlex.shlex(segment.split("\n", 1)[0], posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        words = _drop_redirects(list(lex))
    except ValueError:
        return []
    if not words or Path(words[0]).name not in _READERS:
        return []
    name, args = Path(words[0]).name, words[1:]
    if name == "sed" and any(a.startswith("--in-place") or (a.startswith("-") and not a.startswith("--") and "i" in a)
                             for a in args):
        return []  # sed -i, -ni, --in-place: a write, not a read
    plain, skip = [], False
    for a in args:
        if skip:
            skip = False
        elif a in _VALUE_FLAGS.get(name, set()):
            skip = True
        elif not a.startswith("-"):
            plain.append(a)
    if name in _PATTERN_FIRST and not any(a in ("-e", "-f") for a in args):
        plain = plain[1:]
    return [p if p.is_absolute() else here / p for p in (Path(os.path.expanduser(w)) for w in plain)]


def _segment_writes(segment: str, here: Path) -> list[Path]:
    """Files a simple command certainly writes: redirect and tee targets and what `sed -i` and the like write; for
    `mv`, only the destination. Paths that code inside the command merely names are left out: the guard's parser
    counts them all (it errs toward refusing), but a measure would count every string a script mentions."""
    first = segment.split("\n", 1)[0]
    try:
        words = shlex.split(first)
    except ValueError:
        words = []
    if words[:2] == ["git", "mv"]:
        words = words[1:]
    named = command_writes(first)
    if words and Path(words[0]).name in _MOVES:
        named = named[-1:]
    hits = []
    for word in _redirect_targets(_head(segment)) + named:
        if word and not word.startswith("-") and word not in ("/dev/null", "&1", "&2"):
            path = Path(os.path.expanduser(word))
            hits.append(path if path.is_absolute() else here / path)
    return hits


def _shell_events(command: str, cwd: Path) -> list[dict]:
    """Reads and writes of one shell command, in the order its simple commands run, following `cd`."""
    here, out = cwd, []
    for segment in segments(_unwrap(command)):
        cd = _CD.match(segment)
        if cd:
            step = Path(os.path.expanduser(cd.group(2)))
            here = step if step.is_absolute() else here / step
            continue
        out += [{"kind": "read", "path": p} for p in _segment_reads(segment, here)]
        # None: a shell write does not say whether it created the file; report() asks git.
        out += [{"kind": "write", "path": p, "new": None} for p in _segment_writes(segment, here)
                if p.parent.is_dir() and not p.is_dir()]
    return out


def shell_reads(command: str, cwd: Path) -> list[Path]:
    """The files a shell command reads with a read command, absolute, following `cd` between commands."""
    return [ev["path"] for ev in _shell_events(command, cwd) if ev["kind"] == "read"]


def _text(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(c.get("text", "") if isinstance(c, dict) else str(c) for c in content)
    return ""


def _handed_paths(content: object) -> set[str]:
    """The files the edit hook handed requirement text for, from its own opening lines in `content`."""
    hits = set()
    for line in _text(content).splitlines():
        for opening, end in _HANDOVER:
            if line.startswith(opening) and end in line:
                hits.add(line[len(opening):line.index(end, len(opening))])
    return hits


def _epoch(value: object) -> float | None:
    """A record's time as seconds since the epoch: an ISO string or milliseconds; None when absent or unreadable."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value / 1000
    if isinstance(value, str):
        try:
            return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
        except ValueError:
            return None
    return None


def _dict(value: object) -> dict:
    return value if isinstance(value, dict) else {}


def _dicts(items: object) -> list[dict]:
    return [i for i in items if isinstance(i, dict)] if isinstance(items, list) else []


def _claude_result(name: str, inp: dict, block: dict, cwd: Path) -> list[dict]:
    """Events of one finished Claude tool call. A call that failed before running (a refused edit, a hook denial)
    gives none; a shell command that ran and exited non-zero still wrote what it wrote."""
    result = _text(block.get("content"))
    if block.get("is_error") and not (name == "Bash" and result.startswith("Exit code")):
        return []
    path = inp.get("file_path") or inp.get("notebook_path")
    if name == "Read" and isinstance(path, str):
        return [{"kind": "read", "path": Path(path)}]
    if name == "Write" and isinstance(path, str):  # the session wrote the whole file, so it knows it
        return [{"kind": "write", "path": Path(path), "new": result.startswith("File created")},
                {"kind": "read", "path": Path(path)}]
    if name in _EDIT_TOOLS and isinstance(path, str):
        return [{"kind": "write", "path": Path(path), "new": False}]
    if name == "Bash" and isinstance(inp.get("command"), str):
        return _shell_events(inp["command"], cwd)
    return []


def _codex_changes(changes: object, here: Path) -> list[dict]:
    """Codex file changes: a dict of path to change (rollout) or a list of {path, kind} (exec stream). A delete
    writes nothing to measure; a move writes its destination."""
    items = list(changes.items()) if isinstance(changes, dict) else [(c.get("path"), c) for c in _dicts(changes)]
    out = []
    for path, ch in items:
        ch = ch if isinstance(ch, dict) else {}
        kind = ch.get("type") or ch.get("kind")
        target = ch.get("move_path") or path
        if kind == "delete" or not isinstance(target, str) or not target:
            continue
        out.append({"kind": "write", "path": here / target, "new": kind == "add"})
    return out


def _codex_command(it: dict, here: Path) -> list[dict]:
    """A rollout command: the shell parser's reads and writes in order, plus reads only Codex's own parse found."""
    if it.get("status") in ("declined", "rejected"):
        return []
    cmd = it.get("command")
    events = _shell_events(shlex.join(cmd) if isinstance(cmd, list) else str(cmd or ""), here)
    parsed = [p for p in _dicts(it.get("parsed_cmd")) if p.get("type") == "read" and isinstance(p.get("path"), str)]
    found = {e["path"] for e in events if e["kind"] == "read"}
    # Codex's own read parse adds reads the read-command list misses; the parser's events keep the command's order.
    return [{"kind": "read", "path": here / p["path"]} for p in parsed if here / p["path"] not in found] + events


class _Walk:
    """Turns session records, in order, into read and write events (one walker per session file)."""

    def __init__(self, cwd: Path) -> None:
        self.out: list[dict] = []
        self.cwd = cwd
        self.pending: dict[str, tuple[str, dict, Path, float | None]] = {}  # Claude tool calls awaiting a result
        self.handed: dict[str, set[str]] = {}  # Claude tool call -> files the edit hook gave requirement text for
        self.codex_handed: set[str] = set()  # Codex: hook text arrives as a developer message just before its call ends

    def add(self, events: list[dict], at: float | None, handed: set[str]) -> None:
        for ev in events:
            self.out.append({**ev, "at": at, "handed": handed if ev["kind"] == "write" else set()})

    def record(self, r: object) -> None:
        if not isinstance(r, dict):
            return
        payload = _dict(r.get("payload"))
        if r.get("type") == "session_meta" and isinstance(payload.get("cwd"), str):
            self.cwd = Path(payload["cwd"])
        elif r.get("type") in ("assistant", "attachment", "user"):
            self.claude(r)
        else:
            self.codex(r, payload)

    def claude(self, r: dict) -> None:
        if r["type"] == "attachment":
            att = _dict(r.get("attachment"))
            if att.get("type") == "hook_additional_context":
                self.handed.setdefault(str(att.get("toolUseID", "")), set()).update(_handed_paths(att.get("content")))
            return
        msg = _dict(r.get("message"))
        blocks = _dicts(msg.get("content"))
        if r["type"] == "assistant":
            here = Path(r["cwd"]) if isinstance(r.get("cwd"), str) else self.cwd  # the shell's folder at the call
            for b in blocks:
                if b.get("type") == "tool_use":
                    inp = _dict(b.get("input"))
                    self.pending[str(b.get("id"))] = (str(b.get("name", "")), inp, here, _epoch(r.get("timestamp")))
            return
        for b in (b for b in blocks if b.get("type") == "tool_result"):
            uid = str(b.get("tool_use_id"))
            name, inp, here, at = self.pending.pop(uid, ("", {}, self.cwd, None))
            # `at` is when the call was made: a commit inside the same call comes after the write
            self.add(_claude_result(name, inp, b, here), at, self.handed.pop(uid, set()))

    def codex(self, r: dict, payload: dict) -> None:
        t = r.get("type")
        if t == "item.completed":  # codex exec --json: no times and no hook text in this stream
            it = _dict(r.get("item"))
            if it.get("type") == "command_execution":
                self.add(_shell_events(str(it.get("command", "")), self.cwd), None, set())
            elif it.get("type") == "file_change":
                self.add(_codex_changes(it.get("changes"), self.cwd), None, set())
        elif t == "event_msg" and payload.get("type") == "item_completed":  # codex rollout
            it = _dict(payload.get("item"))
            here = Path(str(it.get("cwd") or self.cwd).removeprefix("file://"))
            at = _epoch(payload.get("started_at_ms")) or _epoch(r.get("timestamp"))
            if it.get("type") == "CommandExecution":
                self.add(_codex_command(it, here), at, self.codex_handed)
            elif it.get("type") == "FileChange":
                self.add(_codex_changes(it.get("changes"), here), at, self.codex_handed)
            else:
                return
            self.codex_handed = set()
        elif t == "response_item" and payload.get("role") == "developer":
            self.codex_handed |= _handed_paths(payload.get("content"))


def _rel(root: Path, path: Path) -> str | None:
    full = Path(os.path.realpath(path if path.is_absolute() else root / path))
    return full.relative_to(root).as_posix() if full.is_relative_to(root) else None


def _context(root: Path, rel: str) -> set[str]:
    """The paths whose reading counts as reading `rel`'s requirement context (Python files: their `Implements:`)."""
    caps = {i.split("/", 1)[0] for i in implemented_ids(root / rel)}
    return {f"generated/wiki/{c}.md" for c in caps} | {f"openspec/specs/{c}/spec.md" for c in caps}


@cache
def _added_at(root: Path, rel: str) -> float | None:
    """When git first recorded `rel` on any branch (seconds); None when git never did; 0 outside a git repository."""
    run = subprocess.run(["git", "-C", str(root), "log", "--all", "--diff-filter=A", "--format=%ct", "--", rel],
                         capture_output=True, text=True, check=False)
    if run.returncode != 0:
        return 0.0  # no history to ask: take the file as already there
    times = [int(t) for t in run.stdout.split() if t.isdigit()]
    return float(min(times)) if times else None


def _created(root: Path, rel: str, at: float | None) -> bool:
    """Whether a shell write at `at` created `rel`: git had not recorded the file before that second.
    git keeps whole seconds, so a commit in the same second as the call still comes after it."""
    added = _added_at(root, rel)
    if added is None or at is None:
        return added is None
    return math.floor(at) <= added


def _transcripts(transcript: Path) -> list[tuple[str, Path]]:
    """The session file and, for a Claude session, its subagents' files (`<session>/subagents/agent-*.jsonl`)."""
    subs = sorted((transcript.parent / transcript.stem / "subagents").glob("agent-*.jsonl"))
    return [("main", transcript)] + [(p.stem, p) for p in subs]


def _rows(agent: str, transcript: Path, root: Path) -> list[dict]:
    walk = _Walk(root)
    for line in transcript.read_text(encoding="utf-8").splitlines():
        if line.strip():
            walk.record(json.loads(line))
    read: set[str] = set()
    written: set[str] = set()
    rows: list[dict] = []
    for ev in walk.out:
        rel = _rel(root, ev["path"])
        if rel is None:
            continue
        if ev["kind"] == "read":
            read.add(rel)
            continue
        new = ev["new"] if ev["new"] is not None else rel not in written and _created(root, rel, ev["at"])
        handover = any(rel == h or ("/" in h and rel.endswith("/" + h)) for h in ev["handed"])
        rows.append({"agent": agent, "file": rel, "new": new, "file_read_first": rel in read,
                     "context_read_first": bool(_context(root, rel) & read), "handover": handover})
        written.add(rel)
        if new:  # the session wrote the whole file, so later writes know it
            read.add(rel)
    for row in rows:
        row["unread"] = not (row["new"] or row["file_read_first"] or row["context_read_first"])
    return rows


def report(transcript: Path, root: Path) -> list[dict]:
    """One row per write inside `root`, in session order, the main agent's first and then each subagent's (each agent
    has its own context, so each is measured on its own reads). Raises OSError or ValueError on an unreadable file."""
    root = Path(os.path.realpath(root))
    return [row for agent, path in _transcripts(transcript) for row in _rows(agent, path, root)]


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
        who = "" if row["agent"] == "main" else f"[{row['agent']}] "
        print(f"{who}{row['file']}: {', '.join(m for m in marks if row[m]) or 'nothing read first'}")
    for row in rows:
        if row["unread"]:
            print(f"WARN {'' if row['agent'] == 'main' else row['agent'] + ' '}{row['file']}: written with neither the file nor its requirement page read first")
    n = {k: sum(r[k] for r in rows) for k in (*marks, "unread")}
    agents = len({r["agent"] for r in rows})
    print(f"RESULT writes={len(rows)} new={n['new']} file_read_first={n['file_read_first']} "
          f"context_read_first={n['context_read_first']} handover={n['handover']} unread={n['unread']} agents={agents}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

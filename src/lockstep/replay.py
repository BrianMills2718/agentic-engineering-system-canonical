"""`lockstep replay TRANSCRIPT`: one session stepped through in order, with hand-overs and read marks.

A local page (127.0.0.1 only) for judging a run by eye (plan "AES next steps", Milestone 1 step 9). It reads a
Claude Code transcript or `claude -p` stream, or a Codex rollout or `codex exec --json` stream, again on every
refresh, and shows the agent's notes, each tool call and its result, each edit hook hand-over as its own event, and
requirement reads. Each write carries the `lockstep reads` rows for its tool call, so page and report agree. File
versions come from a recorder's store (`--store`: `timeline.jsonl` plus `blobs/<sha256>`) when one ran.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:replay.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-guard/a-session-replay-shows-each-hand-over-and-read-mark, lockstep-guard/the-replay-has-a-plan-code-and-wiki-view, lockstep-guard/the-replay-marks-writes-to-the-plan

### Requirement: A session replay shows each hand-over and read mark

`lockstep replay TRANSCRIPT [--repo PATH] [--store DIR] [--port N]` SHALL serve, on 127.0.0.1 only, a page that
steps through one Claude Code or Codex session file in order: the agent's notes, each tool call with its result,
each edit hook hand-over as an event of its own, and each read of a requirement page (`generated/wiki/`) or spec
(`openspec/specs/`) marked as a requirement read. Each write SHALL carry the marks `lockstep reads` gives that
write (file read first, requirement context read first, hand-over, unread), joined by the tool call that made it,
so the page and the report never disagree. A Claude session's subagent files SHALL be offered as further
sessions. With `--store`, the page SHALL also show each file version a recorder saved there
(`timeline.jsonl` and `blobs/<sha256>`); without it, a write shows the text the call wrote. The page SHALL ship
inside the package, so an install from git serves it. The session file SHALL be read again on each page refresh,
so a running session can be followed.

Source: Brian, 2026-11-27, plan doc "AES next steps: plan for discussion", Milestone 1 step 9 ("Replay viewer
shows it all. The draft from today, moved into a git repository, with the hand-over and wiki reads shown as their
own events"); he told the agent to proceed without waiting.

#### Scenario: A Claude hand-over is its own event before its write

- **WHEN** a Claude transcript holds an edit whose `hook_additional_context` attachment names the edited file
- **THEN** the events hold a `handover` event with that text and the edit's call id, ahead of the write event
- **AND** the write event's marks say `handover`

#### Scenario: A Codex hand-over is its own event before its write

- **WHEN** a Codex rollout holds a developer message with the edit hook's text just before a file change completes
- **THEN** the events hold a `handover` event with that text ahead of the file change's write event
- **AND** the write event's marks say `handover`

#### Scenario: A write carries the read-before-write marks

- **WHEN** a session writes a file it never read
- **THEN** that write event's marks match the `lockstep reads` row for that call, with `unread` true

#### Scenario: A requirement page read is marked

- **WHEN** a session reads `generated/wiki/<capability>.md` or `openspec/specs/<capability>/spec.md`, with a read
  tool or a shell read
- **THEN** that event is marked as a requirement read

#### Scenario: The page and its data are served locally

- **WHEN** `lockstep replay` runs
- **THEN** it listens on 127.0.0.1, serves the page from the package at `/`, the sessions at `/api/sessions`, one
  session's events and file versions at `/api/data`, and a stored version at `/api/blob/<sha256>`; any other path
  or an unknown version answers 404

### Requirement: The replay has a plan, code and wiki view

The replay page SHALL offer a toggle between its timeline view and a plan, code and wiki view that steps through
the same events with the same controls. That view SHALL show the agent's current step; for the file of that step,
its `lockstep.yaml` layout row and the text of the requirements it implements (or that no row names it), its code,
and the requirement pages and specs the agent has read so far; and a band of hook cards (hand-over, refusal,
warning, read marks) marking the ones the current event shows. The server SHALL answer `/api/plan?file=<path>`
with that layout row (or null), whether a governed folder and a `fixed:` glob cover the file, and each implemented
requirement's id and text.

Source: Brian, 2026-11-28: "can you create a version of the session replay (togglable) that looks more like
file://wsl.localhost/Ubuntu-24.04/home/brian/code/inbox/ai-astronauts-hive-brain-explainer.html from the plan code
wiki page". The panes, the hook band and the plain-JSON route are inferred by agent from that page's tab 7.

#### Scenario: The plan route gives a file's row and requirement text

- **WHEN** the page asks `/api/plan?file=src/greet.py` and `lockstep.yaml` has a layout row for it that implements
  a requirement with text in `openspec/specs/`
- **THEN** the answer holds that row, `governed` and `fixed` as the plan sets them, and the requirement's id and text
- **AND** for a governed file no row names, `row` is null and `governed` is true

#### Scenario: The page offers the view as a toggle

- **WHEN** the page is served
- **THEN** it holds a toggle that switches to the plan, code and wiki view, and the timeline view is shown first

### Requirement: The replay marks writes to the plan

Each replay event that wrote `lockstep.yaml` or a file under `openspec/changes/` or `openspec/specs/`, and was not
refused, SHALL carry `plan_write: true`; every other tool event SHALL carry `plan_write: false`. The plan, code and
wiki view SHALL light an "agent writes the plan" arrow for a plan write, and SHALL say for the whole session whether
the first file the agent wrote was a plan file, naming that file and its time.

Source: Brian, 2026-11-28: "ok the first thing i noticed is that the agent didnt write the plan first" (on the
plan, code and wiki view of the step-5 proof session). Which paths count as the plan, the event field and the
session line are inferred by agent from the layout rows (`lockstep.yaml`) and OpenSpec changes being where a plan is
written.

#### Scenario: A plan write is marked and a code write is not

- **WHEN** a session writes `lockstep.yaml`, then `src/greet.py`
- **THEN** the first write's event has `plan_write` true and the second's false
- **AND** the page holds the "agent writes the plan" arrow and the plan-first line

Tested by: tests/lockstep/test_replay.py

Declares (typed signatures, from the plan):
  session_events(transcript: Path, root: Path, agent: str='main') -> list[dict]
  make_server(transcript: Path, root: Path, store: Path | None, port: int, store_prefix: str = "") -> ThreadingHTTPServer
  main(argv: list[str] | None = None) -> int
[[[end]]]
"""
import argparse
import importlib.resources
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from fnmatch import fnmatch
from urllib.parse import parse_qs, urlparse

import yaml

from lockstep.checks.markers import implementers
from lockstep.checks.spec import read_plan

from lockstep.read_before_write import (_dict, _dicts, _epoch, _handed_paths, _rel, _text, _transcripts, _unwrap,
                                        _rows, records, shell_reads)

CAP = 60_000  # characters of tool text kept per event
_REQUIREMENT_DIRS = ("generated/wiki/", "openspec/specs/")
_WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit", "Delete"}
_PLAN_DIRS = ("openspec/changes/", "openspec/specs/")


def _show(root: Path, path: object, here: Path) -> str:
    """A path as the page shows it: relative to the repository when inside it, else as given."""
    if not isinstance(path, str) or not path:
        return ""
    rel = _rel(root, Path(path) if Path(path).is_absolute() else here / path)
    return rel if rel is not None else path


def _is_requirement(rel: str) -> bool:
    return rel.startswith(_REQUIREMENT_DIRS)


def _is_plan(rel: str) -> bool:
    """`lockstep.yaml` or an OpenSpec change or spec: where a plan is written."""
    return rel == "lockstep.yaml" or rel.startswith(_PLAN_DIRS)


class _Events:
    """Display events of one session file, in order; Claude and Codex records both."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.cwd = root
        self.t = 0.0
        self.out: list[dict] = []
        self.by_call: dict[str, dict] = {}
        self.codex_pending: list[dict] = []  # Codex hand-overs arrive before the call they came with completes

    def at(self, value: object) -> float:
        """The record's time, or a hair after the last one when the record has none (codex exec streams)."""
        t = _epoch(value)
        self.t = t if t is not None else self.t + 0.001
        return self.t

    def tool(self, t: float, tool: str, call: str, here: Path, **fields: object) -> dict:
        command = str(fields.get("command") or "")
        path = _show(self.root, fields.get("path"), here)
        reads = [_show(self.root, str(p), here) for p in shell_reads(command, here)] if command else []
        e = {"t": t, "kind": "tool", "tool": tool, "call": call, "path": path, "command": command,
             "description": str(fields.get("description") or ""), "content": str(fields.get("content") or "")[:CAP],
             "old": str(fields.get("old") or "")[:CAP], "new": str(fields.get("new") or "")[:CAP],
             "result": str(fields.get("result") or "")[:CAP], "think_ms": fields.get("think_ms") or 0,
             "requirement_read": tool not in _WRITE_TOOLS and any(_is_requirement(p) for p in [path, *reads] if p)}
        self.out.append(e)
        self.by_call.setdefault(call, e)
        return e

    def hook(self, t: float, content: object, call: str, after: bool = False) -> None:
        """Hook text the client gave the agent: an edit hook hand-over when it names a file, else other hook context.
        Claude hook text goes just before the call it came with (just after it for a PostToolUse hook)."""
        text = _text(content)
        if not text.strip():
            return
        e = {"t": t, "kind": "handover" if _handed_paths(content) else "hook", "call": call, "text": text[:CAP]}
        target = self.by_call.get(call) if call else None
        at = self.out.index(target) + after if target in self.out else len(self.out)
        self.out.insert(at, e)
        if not call:
            self.codex_pending.append(e)

    def record(self, r: object) -> None:
        if not isinstance(r, dict):
            return
        kind = r.get("type")
        if kind in ("assistant", "user", "attachment", "result"):
            getattr(self, "claude_" + kind)(r, self.at(r.get("timestamp")))
        elif kind in ("session_meta", "response_item", "event_msg", "item.completed"):
            getattr(self, "codex_" + kind.replace(".", "_"))(r)

    # Claude Code transcripts and claude -p streams

    def claude_assistant(self, r: dict, t: float) -> None:
        here = Path(r["cwd"]) if isinstance(r.get("cwd"), str) else self.cwd
        think = r.get("thinking_duration_ms") or 0
        for c in _dicts(_dict(r.get("message")).get("content")):
            if c.get("type") == "text" and str(c.get("text", "")).strip():
                self.out.append({"t": t, "kind": "note", "text": str(c["text"]), "think_ms": think})
            elif c.get("type") == "tool_use":
                i = _dict(c.get("input"))
                self.tool(t, str(c.get("name", "")), str(c.get("id", "")), here,
                          path=i.get("file_path") or i.get("notebook_path"), command=i.get("command"),
                          description=i.get("description"), content=i.get("content"), old=i.get("old_string"),
                          new=i.get("new_string") or i.get("new_source") or "\n".join(
                              str(x.get("new_string", "")) for x in _dicts(i.get("edits"))), think_ms=think)
                if not (i.get("command") or i.get("file_path") or i.get("notebook_path")):
                    self.out[-1]["command"] = json.dumps(i)[:400]

    def claude_user(self, r: dict, t: float) -> None:
        for c in _dicts(_dict(r.get("message")).get("content")):
            e = self.by_call.get(str(c.get("tool_use_id"))) if c.get("type") == "tool_result" else None
            if e is not None:
                e["result"] = _text(c.get("content"))[:CAP]
                e["error"] = bool(c.get("is_error"))
                if e["error"] and not (e["tool"] == "Bash" and e["result"].startswith("Exit code")):
                    e["refused"] = True  # did not run: lockstep reads counts it as neither read nor write
                    e["requirement_read"] = False

    def claude_attachment(self, r: dict, t: float) -> None:
        att = _dict(r.get("attachment"))
        if att.get("type") == "hook_additional_context":
            call = str(att.get("toolUseID", ""))
            after = str(att.get("hookName", "")).startswith("PostToolUse")
            self.hook(self.by_call[call]["t"] if call in self.by_call else t, att.get("content"), call, after)

    def claude_result(self, r: dict, t: float) -> None:
        self.out.append({"t": t, "kind": "end", "text": f"Session ended ({r.get('subtype')})",
                         "final": str(r.get("result") or "")[-400:]})

    # Codex rollouts and codex exec --json streams

    def codex_session_meta(self, r: dict) -> None:
        cwd = _dict(r.get("payload")).get("cwd")
        if isinstance(cwd, str):
            self.cwd = Path(cwd)

    def codex_response_item(self, r: dict) -> None:
        p = _dict(r.get("payload"))
        if p.get("type") != "message":
            return
        t = self.at(r.get("timestamp"))
        if p.get("role") == "assistant" and _text(p.get("content")).strip():
            self.out.append({"t": t, "kind": "note", "text": _text(p.get("content")), "think_ms": 0})
        elif p.get("role") == "developer" and _handed_paths(p.get("content")):
            self.hook(t, p.get("content"), "")

    def codex_event_msg(self, r: dict) -> None:
        p = _dict(r.get("payload"))
        if p.get("type") == "item_completed":
            it = _dict(p.get("item"))
            here = Path(str(it.get("cwd") or self.cwd).removeprefix("file://"))
            self.codex_item(it, self.at(p.get("started_at_ms") or r.get("timestamp")), here)

    def codex_item_completed(self, r: dict) -> None:
        self.codex_item(_dict(r.get("item")), self.at(None), self.cwd)

    def codex_item(self, it: dict, t: float, here: Path) -> None:
        kind, call = it.get("type"), str(it.get("id", ""))
        if kind in ("CommandExecution", "command_execution", "FileChange", "file_change"):
            for e in self.codex_pending:  # the hand-overs since the last call came with this one
                e["call"] = call
                e["t"] = min(e["t"], t)  # so the page, which orders by time, keeps it ahead of its call
            self.codex_pending = []
        if kind in ("CommandExecution", "command_execution"):
            cmd = it.get("command")
            command = _unwrap(cmd[-1] if isinstance(cmd, list) and cmd else str(cmd or ""))
            reads = [x for x in _dicts(it.get("parsed_cmd")) if x.get("type") == "read" and x.get("path")]
            self.tool(t, "Read" if reads and len(reads) == len(_dicts(it.get("parsed_cmd"))) else "Bash", call, here,
                      command=command, path=reads[0]["path"] if len(reads) == 1 else "",
                      result=it.get("aggregated_output"))
        elif kind in ("FileChange", "file_change"):
            self.codex_changes(it.get("changes"), t, call, here)
        elif kind == "agent_message" and str(it.get("text", "")).strip():
            self.out.append({"t": t, "kind": "note", "text": str(it["text"]), "think_ms": 0})
        elif "toolcall" in str(kind).lower().replace("_", ""):  # MCP and agent calls: shown, never read or write
            rest = {k: v for k, v in it.items() if k not in ("type", "id", "result", "output")}
            self.tool(t, str(kind), call, here, command=json.dumps(rest)[:400], result=json.dumps(it.get("result") or it.get("output") or "")[:CAP])

    def codex_changes(self, changes: object, t: float, call: str, here: Path) -> None:
        items = list(changes.items()) if isinstance(changes, dict) else [(c.get("path"), c) for c in _dicts(changes)]
        for path, ch in items:
            ch = _dict(ch)
            kind = ch.get("type") or ch.get("kind")
            e = self.tool(t, "Write" if kind == "add" else "Delete" if kind == "delete" else "Edit", call, here,
                          path=ch.get("move_path") or path, new=ch.get("unified_diff") or ch.get("content"))
            e["diff"] = bool(ch.get("unified_diff"))


def _marks(events: list[dict], rows: list[dict]) -> None:
    """Give each tool event the lockstep reads rows of its call: a shell call gets all of them, a file tool its file's."""
    by_call: dict[str, list[dict]] = {}
    for row in rows:
        by_call.setdefault(row["call"], []).append(row)
    for e in events:
        if e["kind"] == "tool":
            mine = by_call.get(e["call"], [])
            e["marks"] = mine if e["tool"] in ("Bash", "Read") else [m for m in mine if m["file"] == e["path"]]
            e["writes"] = [m["file"] for m in e["marks"]]  # a shell call names no path; its writes are these
            wrote = ([e["path"]] if e["tool"] in _WRITE_TOOLS else []) + e["writes"]
            e["plan_write"] = not e.get("refused") and any(_is_plan(f) for f in wrote if f)


def session_events(transcript: Path, root: Path, agent: str = "main") -> list[dict]:
    """The display events of one session file (`agent` names a Claude subagent file), each write with its marks.
    Raises OSError or ValueError on an unreadable file."""
    root = Path(os.path.realpath(root))
    files = dict(_transcripts(transcript))
    walk = _Events(root)
    for record in records(files[agent]):
        walk.record(record)
    _marks(walk.out, _rows(agent, files[agent], root))  # the rows lockstep reads gives this agent
    return walk.out


def _changes(store: Path | None, prefix: str = "") -> list[dict]:
    """The recorder's file versions under `prefix` (the repository's path inside the watched folder), with paths
    relative to the repository so they match the session's."""
    tl = store / "timeline.jsonl" if store else None
    if tl is None or not tl.exists():
        return []
    out = []
    for line in tl.read_text(encoding="utf-8").split("\n"):
        try:
            c = json.loads(line)
        except ValueError:
            continue
        if isinstance(c, dict) and isinstance(c.get("path"), str) and c["path"].startswith(prefix):
            out.append({**c, "path": c["path"][len(prefix):]})
    return out


def _signature(transcript: Path) -> tuple:
    """What changes when a session file or a subagent's grows: each file's size and modification time."""
    return tuple((p, p.stat().st_size, p.stat().st_mtime_ns) for _, p in _transcripts(transcript))


class _Site:
    """What the page asks for, answered from one session file; a session is read again only when its file changed."""

    def __init__(self, transcript: Path, root: Path, store: Path | None, store_prefix: str) -> None:
        self.transcript, self.root, self.store, self.store_prefix = transcript, root, store, store_prefix
        self.page = importlib.resources.files("lockstep").joinpath("replay.html").read_bytes()
        self.cache: dict[str, tuple[tuple, bytes]] = {}

    def data(self, agent: str) -> bytes:
        sig = _signature(self.transcript)
        if agent not in self.cache or self.cache[agent][0] != sig:
            body = {"session": agent, "events": session_events(self.transcript, self.root, agent),
                    "changes": _changes(self.store, self.store_prefix)}
            self.cache[agent] = (sig, json.dumps(body).encode())
        return self.cache[agent][1]

    def blob(self, sha: str) -> bytes | None:
        if not self.store or len(sha) != 64 or not sha.isalnum():
            return None
        path = self.store / "blobs" / sha
        return path.read_bytes() if path.is_file() else None

    def plan(self, rel: str) -> dict:
        """The plan for one file: its layout row (or None), whether a governed folder and a fixed glob cover it,
        and the id and text of each requirement its row or its docstring says it implements."""
        side = self.root / "lockstep.yaml"
        data = yaml.safe_load(side.read_text()) if side.is_file() else None
        data = data if isinstance(data, dict) else {}
        rows = [r for r in data.get("layout") or [] if isinstance(r, dict) and r.get("path") == rel]
        row = rows[0] if rows else None
        governed = any(rel.startswith(str(g)) for g in data.get("governed") or [])
        fixed = any(fnmatch(rel, str(g)) for g in data.get("fixed") or [])
        ids = [str(i) for i in (row or {}).get("implements") or []]
        path = self.root / rel
        if path.is_file() and path.resolve().is_relative_to(self.root.resolve()):
            ids += [i for i, _, _ in implementers(self.root, only=path.resolve()) if i not in ids]
        text = read_plan(self.root).text if ids else {}
        return {"file": rel, "row": row, "governed": governed, "fixed": fixed,
                "requirements": [{"id": i, "text": text.get(i, "")} for i in ids]}

    def answer(self, raw_path: str) -> tuple[bytes, str, int]:
        url = urlparse(raw_path)
        names = [name for name, _ in _transcripts(self.transcript)]
        if url.path in ("/", "/index.html"):
            return self.page, "text/html; charset=utf-8", 200
        if url.path == "/api/sessions":
            return json.dumps(names).encode(), "application/json", 200
        if url.path == "/api/plan":
            rel = (parse_qs(url.query).get("file") or [""])[0]
            return json.dumps(self.plan(rel)).encode(), "application/json", 200
        if url.path == "/api/data":
            agent = (parse_qs(url.query).get("session") or [""])[0]
            if agent not in names:
                return b"unknown session", "text/plain", 404
            return self.data(agent), "application/json", 200
        blob = self.blob(url.path.removeprefix("/api/blob/"))
        if blob is not None:
            return blob, "text/plain; charset=utf-8", 200
        return b"not found", "text/plain", 404


def make_server(transcript: Path, root: Path, store: Path | None, port: int, store_prefix: str = "") -> ThreadingHTTPServer:
    """A server on 127.0.0.1:`port` (0 picks a free one) for one session file; call serve_forever() on it.
    It answers only requests addressed to 127.0.0.1 or localhost, so a web page cannot reach it by renaming a host
    (DNS rebinding), and it reads a session file again only when the file changed."""
    site = _Site(transcript, root, store, store_prefix)

    class Handler(BaseHTTPRequestHandler):
        def send(self, body: bytes, ctype: str = "application/json", code: int = 200) -> None:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            port_now = getattr(self.server, "server_port", 0)
            if self.headers.get("Host") not in (f"127.0.0.1:{port_now}", f"localhost:{port_now}"):
                return self.send(b"wrong host", "text/plain", 403)
            try:
                return self.send(*site.answer(self.path))
            except (OSError, ValueError) as exc:  # a session file being rewritten, or one that stopped parsing
                return self.send(json.dumps({"error": str(exc)}).encode(), code=500)

        def log_message(self, *args: object) -> None:
            pass

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def main(argv: list[str] | None = None) -> int:
    """Serve the page until interrupted; 2 when the session file cannot be read."""
    parser = argparse.ArgumentParser(prog="lockstep replay", description="Step through one session on a local page.")
    parser.add_argument("transcript", type=Path)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--store", type=Path, default=None, help="a recorder's store: timeline.jsonl and blobs/")
    parser.add_argument("--store-prefix", default="", help="the repository's path inside the folder the recorder watched, e.g. on-1/repo/")
    parser.add_argument("--port", type=int, default=8791)
    args = parser.parse_args(argv)
    try:
        session_events(args.transcript, args.repo)
    except (OSError, ValueError) as exc:
        print(f"lockstep replay: cannot read {args.transcript}: {exc}", file=sys.stderr)
        return 2
    server = make_server(args.transcript, args.repo, args.store, args.port, args.store_prefix)
    print(f"Session replay: http://127.0.0.1:{server.server_address[1]}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

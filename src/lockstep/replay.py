"""`lockstep replay TRANSCRIPT`: one session stepped through in order, with hand-overs and read marks.

A local page (127.0.0.1 only) for judging a run by eye (plan "AES next steps", Milestone 1 step 9). It reads a
Claude Code transcript or `claude -p` stream, or a Codex rollout or `codex exec --json` stream, again on every
refresh, and shows the agent's notes, each tool call and its result, each edit hook hand-over as its own event, and
requirement reads. Each write carries the `lockstep reads` rows for its tool call, so page and report agree. File
versions come from a recorder's store (`--store`: `timeline.jsonl` plus `blobs/<sha256>`) when one ran.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:replay.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-guard/a-session-replay-shows-each-hand-over-and-read-mark

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

Tested by: tests/lockstep/test_replay.py

Declares (typed signatures, from the plan):
  session_events(transcript: Path, root: Path) -> list[dict]
  make_server(transcript: Path, root: Path, store: Path | None, port: int) -> ThreadingHTTPServer
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
from urllib.parse import parse_qs, urlparse

from lockstep.read_before_write import (_dict, _dicts, _epoch, _handed_paths, _rel, _text, _transcripts, _unwrap,
                                        report, shell_reads)

CAP = 60_000  # characters of tool text kept per event
_REQUIREMENT_DIRS = ("generated/wiki/", "openspec/specs/")
_WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}


def _show(root: Path, path: object, here: Path) -> str:
    """A path as the page shows it: relative to the repository when inside it, else as given."""
    if not isinstance(path, str) or not path:
        return ""
    rel = _rel(root, Path(path) if Path(path).is_absolute() else here / path)
    return rel if rel is not None else path


def _is_requirement(rel: str) -> bool:
    return rel.startswith(_REQUIREMENT_DIRS)


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

    def hook(self, t: float, content: object, call: str) -> None:
        """Hook text the client gave the agent: an edit hook hand-over when it names a file, else other hook context.
        A Claude hand-over goes just before the call it came with."""
        text = _text(content)
        if not text.strip():
            return
        e = {"t": t, "kind": "handover" if _handed_paths(content) else "hook", "call": call, "text": text[:CAP]}
        target = self.by_call.get(call) if call else None
        self.out.insert(self.out.index(target) if target in self.out else len(self.out), e)
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
                          new=i.get("new_string"), think_ms=think)
                if not (i.get("command") or i.get("file_path") or i.get("notebook_path")):
                    self.out[-1]["command"] = json.dumps(i)[:400]

    def claude_user(self, r: dict, t: float) -> None:
        for c in _dicts(_dict(r.get("message")).get("content")):
            e = self.by_call.get(str(c.get("tool_use_id"))) if c.get("type") == "tool_result" else None
            if e is not None:
                e["result"] = _text(c.get("content"))[:CAP]
                e["error"] = bool(c.get("is_error"))

    def claude_attachment(self, r: dict, t: float) -> None:
        att = _dict(r.get("attachment"))
        if att.get("type") == "hook_additional_context":
            call = str(att.get("toolUseID", ""))
            self.hook(self.by_call[call]["t"] if call in self.by_call else t, att.get("content"), call)

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

    def codex_changes(self, changes: object, t: float, call: str, here: Path) -> None:
        items = list(changes.items()) if isinstance(changes, dict) else [(c.get("path"), c) for c in _dicts(changes)]
        for path, ch in items:
            ch = _dict(ch)
            kind = ch.get("type") or ch.get("kind")
            self.tool(t, "Write" if kind == "add" else "Delete" if kind == "delete" else "Edit", call, here,
                      path=ch.get("move_path") or path, new=ch.get("unified_diff") or ch.get("content"))


def _marks(events: list[dict], rows: list[dict]) -> None:
    """Give each tool event the lockstep reads rows of its call: a shell call gets all of them, a file tool its file's."""
    by_call: dict[str, list[dict]] = {}
    for row in rows:
        by_call.setdefault(row["call"], []).append(row)
    for e in events:
        if e["kind"] == "tool":
            mine = by_call.get(e["call"], [])
            e["marks"] = mine if e["tool"] in ("Bash", "Read") else [m for m in mine if m["file"] == e["path"]]


def session_events(transcript: Path, root: Path, agent: str = "main") -> list[dict]:
    """The display events of one session file (`agent` names a Claude subagent file), each write with its marks.
    Raises OSError or ValueError on an unreadable file."""
    root = Path(os.path.realpath(root))
    files = dict(_transcripts(transcript))
    walk = _Events(root)
    for line in files[agent].read_text(encoding="utf-8").splitlines():
        if line.strip():
            walk.record(json.loads(line))
    _marks(walk.out, [r for r in report(transcript, root) if r["agent"] == agent])
    return walk.out


def _changes(store: Path | None) -> list[dict]:
    """The recorder's file versions, paths relative to the folder it watched."""
    tl = store / "timeline.jsonl" if store else None
    if tl is None or not tl.exists():
        return []
    out = []
    for line in tl.read_text(encoding="utf-8").splitlines():
        try:
            c = json.loads(line)
        except ValueError:
            continue
        if isinstance(c, dict) and isinstance(c.get("path"), str):
            out.append(c)
    return out


def make_server(transcript: Path, root: Path, store: Path | None, port: int) -> ThreadingHTTPServer:
    """A server on 127.0.0.1:`port` (0 picks a free one) for one session file; call serve_forever() on it."""
    page = importlib.resources.files("lockstep").joinpath("replay.html").read_bytes()

    class Handler(BaseHTTPRequestHandler):
        def send(self, body: bytes, ctype: str = "application/json", code: int = 200) -> None:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802 (the http.server name)
            url = urlparse(self.path)
            names = [name for name, _ in _transcripts(transcript)]
            if url.path in ("/", "/index.html"):
                return self.send(page, "text/html; charset=utf-8")
            if url.path == "/api/sessions":
                return self.send(json.dumps(names).encode())
            if url.path == "/api/data":
                agent = (parse_qs(url.query).get("session") or [""])[0]
                if agent not in names:
                    return self.send(b"unknown session", "text/plain", 404)
                body = {"session": agent, "events": session_events(transcript, root, agent), "changes": _changes(store)}
                return self.send(json.dumps(body).encode())
            sha = url.path.removeprefix("/api/blob/")
            blob = store / "blobs" / sha if store and len(sha) == 64 and sha.isalnum() else None
            if blob is not None and blob.is_file():
                return self.send(blob.read_bytes(), "text/plain; charset=utf-8")
            return self.send(b"not found", "text/plain", 404)

        def log_message(self, *args: object) -> None:
            pass

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def main(argv: list[str] | None = None) -> int:
    """Serve the page until interrupted; 2 when the session file cannot be read."""
    parser = argparse.ArgumentParser(prog="lockstep replay", description="Step through one session on a local page.")
    parser.add_argument("transcript", type=Path)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--store", type=Path, default=None, help="a recorder's store: timeline.jsonl and blobs/")
    parser.add_argument("--port", type=int, default=8791)
    args = parser.parse_args(argv)
    try:
        session_events(args.transcript, args.repo)
    except (OSError, ValueError) as exc:
        print(f"lockstep replay: cannot read {args.transcript}: {exc}", file=sys.stderr)
        return 2
    server = make_server(args.transcript, args.repo, args.store, args.port)
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

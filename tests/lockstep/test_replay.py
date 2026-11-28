"""`lockstep replay`: one session stepped through in order, with hand-overs and read marks (Milestone 1 step 9)."""
import hashlib
import json
import threading
import urllib.error
import urllib.request
from pathlib import Path

import pytest

from lockstep.read_before_write import report
from lockstep.replay import make_server, session_events

GREET = '"""Greeter.\n\nImplements: greeter/the-greeter-says-hello\n"""\n\n\ndef greet() -> str:\n    return "hello"\n'
HAND = ("Requirement text for src/greet.py, from OpenSpec (its docstring says Implements: "
        "greeter/the-greeter-says-hello):\n\nThe greeter SHALL return `hello`.")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "src").mkdir()
    (tmp_path / "src/greet.py").write_text(GREET)
    spec = tmp_path / "openspec/specs/greeter"
    spec.mkdir(parents=True)
    (spec / "spec.md").write_text("### Requirement: The greeter says hello\n\nThe greeter SHALL return `hello`.\n")
    (tmp_path / "generated/wiki").mkdir(parents=True)
    (tmp_path / "generated/wiki/greeter.md").write_text("# greeter\n")
    return tmp_path


def _claude(*calls: tuple) -> list[dict]:
    """Claude transcript records: each call is (tool name, input, result text[, attachment text])."""
    out: list[dict] = []
    for n, (name, inp, result, *attach) in enumerate(calls):
        uid, at = f"toolu_{n}", f"2026-11-27T23:00:{n:02d}Z"
        out.append({"type": "assistant", "timestamp": at, "message": {"content": [
            {"type": "text", "text": f"step {n}"}, {"type": "tool_use", "id": uid, "name": name, "input": inp}]}})
        for text in attach:
            out.append({"type": "attachment", "timestamp": at,
                        "attachment": {"type": "hook_additional_context", "toolUseID": uid, "content": [text]}})
        out.append({"type": "user", "timestamp": at, "message": {"content": [
            {"type": "tool_result", "tool_use_id": uid, "content": result}]}})
    return out


def _write(path: Path, records: list[dict]) -> Path:
    path.write_text("".join(json.dumps(r) + "\n" for r in records))
    return path


def _index(events: list[dict], **want) -> int:
    return next(i for i, e in enumerate(events) if all(e.get(k) == v for k, v in want.items()))


@pytest.mark.req("lockstep-guard/a-claude-hand-over-is-its-own-event-before-its-write")
def test_a_claude_hand_over_is_its_own_event(repo):
    t = _write(repo / "t.jsonl", _claude(
        ("Read", {"file_path": str(repo / "src/greet.py")}, "1\tGreeter"),
        ("Edit", {"file_path": str(repo / "src/greet.py"), "old_string": "hello", "new_string": "hi"}, "updated", HAND)))
    events = session_events(t, repo)
    hand = _index(events, kind="handover")
    write = _index(events, kind="tool", tool="Edit")
    assert hand < write
    assert events[hand]["call"] == events[write]["call"] == "toolu_1"
    assert "The greeter SHALL return" in events[hand]["text"]
    mark, = events[write]["marks"]
    assert mark["handover"] and mark["file_read_first"] and mark["file"] == "src/greet.py"
    assert events[write]["path"] == "src/greet.py"


@pytest.mark.req("lockstep-guard/a-codex-hand-over-is-its-own-event-before-its-write")
def test_a_codex_hand_over_is_its_own_event(repo):
    at = "2026-11-27T23:15:56.128Z"
    t = _write(repo / "r.jsonl", [
        {"type": "session_meta", "timestamp": at, "payload": {"cwd": str(repo)}},
        {"type": "response_item", "timestamp": at, "payload": {"type": "message", "role": "assistant",
                                                               "content": [{"type": "output_text", "text": "Editing now."}]}},
        {"type": "response_item", "timestamp": at, "payload": {"type": "message", "role": "developer",
                                                               "content": [{"type": "input_text", "text": HAND}]}},
        {"type": "event_msg", "timestamp": at, "payload": {"type": "item_completed", "started_at_ms": 1795821355908, "item": {
            "type": "FileChange", "id": "fc-1", "status": "completed", "changes": {str(repo / "src/greet.py"): {
                "type": "update", "unified_diff": "@@ -7,2 +7,2 @@\n-    return \"hello\"\n+    return \"hi\"\n",
                "move_path": None}}}}},
    ])
    events = session_events(t, repo)
    hand = _index(events, kind="handover")
    write = _index(events, kind="tool", call="fc-1")
    assert hand < write
    assert events[write]["path"] == "src/greet.py" and "return \"hi\"" in events[write]["new"]
    mark, = events[write]["marks"]
    assert mark["handover"]
    assert events[_index(events, kind="note")]["text"] == "Editing now."


@pytest.mark.req("lockstep-guard/a-write-carries-the-read-before-write-marks")
def test_a_write_carries_the_read_marks(repo):
    t = _write(repo / "t.jsonl", _claude(("Bash", {"command": f"cd {repo} && printf 'x' > src/greet.py"}, "")))
    events = session_events(t, repo)
    write = events[_index(events, kind="tool", tool="Bash")]
    row, = report(t, repo)
    mark, = write["marks"]
    assert mark == row and mark["unread"]


@pytest.mark.req("lockstep-guard/a-requirement-page-read-is-marked")
def test_a_requirement_page_read_is_marked(repo):
    t = _write(repo / "t.jsonl", _claude(
        ("Read", {"file_path": str(repo / "generated/wiki/greeter.md")}, "# greeter"),
        ("Bash", {"command": f"cat {repo}/openspec/specs/greeter/spec.md"}, "### Requirement"),
        ("Read", {"file_path": str(repo / "src/greet.py")}, "1\tGreeter")))
    tools = [e for e in session_events(t, repo) if e["kind"] == "tool"]
    assert [e["requirement_read"] for e in tools] == [True, True, False]


def _get(port: int, path: str) -> tuple[int, bytes]:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=5) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as err:
        return err.code, b""


@pytest.mark.req("lockstep-guard/the-page-and-its-data-are-served-locally")
def test_the_page_and_data_are_served_locally(repo):
    t = _write(repo / "t.jsonl", _claude(("Read", {"file_path": str(repo / "src/greet.py")}, "1\tGreeter")))
    sub = repo / "t" / "subagents"
    sub.mkdir(parents=True)
    _write(sub / "agent-a1.jsonl", _claude(("Read", {"file_path": str(repo / "src/greet.py")}, "1\tGreeter")))
    store = repo / "store"
    (store / "blobs").mkdir(parents=True)
    sha = hashlib.sha256(GREET.encode()).hexdigest()
    (store / "blobs" / sha).write_text(GREET)
    (store / "timeline.jsonl").write_text(json.dumps({"t": 1.0, "path": "src/greet.py", "sha": sha, "op": "initial"}) + "\n")
    server = make_server(t, repo, store, 0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        host, port = server.server_address[:2]
        assert host == "127.0.0.1"
        code, page = _get(port, "/")
        assert code == 200 and b"Session Replay" in page
        assert json.loads(_get(port, "/api/sessions")[1]) == ["main", "agent-a1"]
        data = json.loads(_get(port, "/api/data?session=main")[1])
        assert [e["tool"] for e in data["events"] if e["kind"] == "tool"] == ["Read"]
        assert data["changes"][0]["path"] == "src/greet.py"
        assert _get(port, f"/api/blob/{sha}") == (200, GREET.encode())
        assert _get(port, "/api/blob/" + "0" * 64)[0] == 404
        assert _get(port, "/api/data?session=nobody")[0] == 404
        assert _get(port, "/elsewhere")[0] == 404
    finally:
        server.shutdown()
        server.server_close()

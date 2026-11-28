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
    assert hand < write and events[hand]["call"] == "fc-1"
    assert events[hand]["t"] <= events[write]["t"]  # the page orders by time
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


def test_line_separators_inside_strings_and_a_half_written_last_line_are_read(repo):
    recs = _claude(("Read", {"file_path": str(repo / "src/greet.py")}, "a b\x0cc"))
    t = repo / "t.jsonl"
    t.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in recs) + '{"type": "assist')
    events = session_events(t, repo)
    assert [e["tool"] for e in events if e["kind"] == "tool"] == ["Read"]
    assert report(t, repo) == []
    t.write_text('{"type": "assist\n' + json.dumps(recs[0]) + "\n")
    with pytest.raises(ValueError):
        session_events(t, repo)


def test_a_write_to_a_path_that_cannot_be_checked_is_not_a_crash(repo):
    t = _write(repo / "t.jsonl", _claude(
        ("Bash", {"command": "echo hi > /root/nope/x.sql"}, ""),
        ("Bash", {"command": f"cd {repo} && echo hi > {'x' * 300}/y.py"}, "")))
    assert [e["tool"] for e in session_events(t, repo) if e["kind"] == "tool"] == ["Bash", "Bash"]


def test_a_refused_read_is_not_a_requirement_read(repo):
    recs = _claude(("Read", {"file_path": str(repo / "openspec/specs/greeter/spec.md")}, "refused"))
    recs[-1]["message"]["content"][0]["is_error"] = True
    tool, = [e for e in session_events(_write(repo / "t.jsonl", recs), repo) if e["kind"] == "tool"]
    assert tool["refused"] and not tool["requirement_read"]


def test_a_shell_write_names_its_files(repo):
    t = _write(repo / "t.jsonl", _claude(("Bash", {"command": f"cd {repo} && printf 'x' > src/greet.py"}, "")))
    tool, = [e for e in session_events(t, repo) if e["kind"] == "tool"]
    assert tool["writes"] == ["src/greet.py"]


def _request(port: int, path: str, host: str) -> int:
    req = urllib.request.Request(f"http://127.0.0.1:{port}{path}", headers={"Host": host})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status
    except urllib.error.HTTPError as err:
        return err.code


def test_a_request_for_another_host_name_is_refused_and_a_bad_file_answers_500(repo):
    t = _write(repo / "t.jsonl", _claude(("Read", {"file_path": str(repo / "src/greet.py")}, "1\tGreeter")))
    store = repo / "store"
    store.mkdir()
    (store / "timeline.jsonl").write_text(json.dumps({"t": 1.0, "path": "on-1/repo/src/greet.py", "sha": "a", "op": "initial"})
                                          + "\n" + json.dumps({"t": 1.0, "path": "on-1/log.txt", "sha": "b", "op": "initial"}) + "\n")
    server = make_server(t, repo, store, 0, "on-1/repo/")
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        port = server.server_address[1]
        assert _request(port, "/api/sessions", "attacker.example:%d" % port) == 403
        assert _request(port, "/api/sessions", "localhost:%d" % port) == 200
        assert [c["path"] for c in json.loads(_get(port, "/api/data?session=main")[1])["changes"]] == ["src/greet.py"]
        t.write_text('{"bad\n{"type": "user"}\n')
        assert _get(port, "/api/data?session=main")[0] == 500
    finally:
        server.shutdown()
        server.server_close()


def _serve(repo: Path):
    t = _write(repo / "t.jsonl", _claude(("Read", {"file_path": str(repo / "src/greet.py")}, "1\tGreeter")))
    server = make_server(t, repo, None, 0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


@pytest.mark.req("lockstep-guard/the-plan-route-gives-a-file-s-row-and-requirement-text")
def test_the_plan_route_gives_a_files_row_and_requirement_text(repo):
    (repo / "lockstep.yaml").write_text(
        "governed: [src/]\nfixed: [\"src/*\"]\nlayout:\n- path: src/greet.py\n  purpose: Says hello\n"
        "  implements: [greeter/the-greeter-says-hello]\n  tests: [tests/test_greet.py]\n")
    server = _serve(repo)
    try:
        port = server.server_address[1]
        code, body = _get(port, "/api/plan?file=src/greet.py")
        plan = json.loads(body)
        assert code == 200 and plan["row"]["purpose"] == "Says hello"
        assert plan["governed"] is True and plan["fixed"] is True
        assert plan["requirements"] == [{"id": "greeter/the-greeter-says-hello", "text": "The greeter SHALL return `hello`."}]
        other = json.loads(_get(port, "/api/plan?file=src/extra.py")[1])
        assert other["row"] is None and other["governed"] is True and other["requirements"] == []
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.req("lockstep-guard/the-page-offers-the-view-as-a-toggle")
def test_the_page_offers_the_view_as_a_toggle(repo):
    server = _serve(repo)
    try:
        page = _get(server.server_address[1], "/")[1].decode()
        assert 'id="viewtoggle"' in page and 'id="sysview"' in page
        assert 'id="sysview" class="sysview" hidden' in page  # the timeline view is shown first
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.req("lockstep-guard/a-document-write-is-a-plan-write-and-a-generated-test-config-or-wiki-write-is-not")
def test_a_document_write_is_a_plan_write_and_a_generated_test_config_or_wiki_write_is_not(repo):
    paths = ["docs/architecture/greet.md", "generated/files.md", "tests/test_greet.py", "pyproject.toml",
             "wiki/index.md"]
    t = _write(repo / "t.jsonl", _claude(*[
        ("Write", {"file_path": str(repo / p), "content": "x\n"}, "File created successfully") for p in paths]))
    tools = [e for e in session_events(t, repo) if e["kind"] == "tool"]
    assert [(e["path"], e["plan_write"]) for e in tools] == [(p, p == paths[0]) for p in paths]
    assert [e["plan_file"] for e in tools] == [p == paths[0] for p in paths]  # the page's plan-read rule, same files


@pytest.mark.req("lockstep-guard/a-plan-write-is-marked-and-a-code-write-is-not")
def test_a_plan_write_is_marked_and_a_code_write_is_not(repo):
    t = _write(repo / "t.jsonl", _claude(
        ("Write", {"file_path": str(repo / "lockstep.yaml"), "content": "layout: []\n"}, "File created successfully"),
        ("Write", {"file_path": str(repo / "src/greet.py"), "content": "x = 1\n"}, "File written")))
    tools = [e for e in session_events(t, repo) if e["kind"] == "tool"]
    assert [(e["path"], e["plan_write"]) for e in tools] == [("lockstep.yaml", True), ("src/greet.py", False)]
    server = _serve(repo)
    try:
        page = _get(server.server_address[1], "/")[1].decode()
        assert 'id="aPlanW"' in page and 'id="svFirst"' in page
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.req("lockstep-guard/a-write-before-its-row-is-added-is-flagged")
def test_a_write_before_its_row_is_added_is_flagged(repo):
    (repo / "lockstep.yaml").write_text(
        "governed: [src/]\nlayout:\n- path: src/greet.py\n  purpose: Says hello\n- path: src/extra.py\n  purpose: Extra\n")
    t = _write(repo / "t.jsonl", _claude(
        ("Write", {"file_path": str(repo / "src/extra.py"), "content": "x = 1\n"}, "File created successfully"),
        ("Edit", {"file_path": str(repo / "lockstep.yaml"), "old_string": "layout:\n",
                  "new_string": "layout:\n- path: src/extra.py\n  purpose: Extra\n"}, "updated"),
        ("Write", {"file_path": str(repo / "src/other.py"), "content": "y = 2\n"}, "File created successfully"),
        ("Edit", {"file_path": str(repo / "src/greet.py"), "old_string": "hello", "new_string": "hi"}, "updated"),
        ("Write", {"file_path": "/elsewhere/notes.txt", "content": "z\n"}, "File created successfully")))
    writes = [e for e in session_events(t, repo) if e["kind"] == "tool"]
    assert [e.get("planned") for e in writes] == ["row added later", None, "unplanned", "planned", "outside"]


@pytest.mark.req("lockstep-guard/the-status-and-wiki-routes-answer")
def test_the_status_and_wiki_routes_answer(repo):
    (repo / "generated/wiki/index.md").write_text("# index\n")
    server = _serve(repo)
    try:
        port = server.server_address[1]
        status = json.loads(_get(port, "/api/status")[1])
        req = status["requirements"]["greeter/the-greeter-says-hello"]
        assert req["state"] and any(f.startswith("src/greet.py") for f in req["code"]) and "note" in status
        wiki = json.loads(_get(port, "/api/wiki")[1])
        assert wiki[0] == "generated/wiki/index.md" and "generated/wiki/greeter.md" in wiki
        page = _get(port, "/")[1].decode()
        assert 'id="svTrack"' in page and 'id="svWikiList"' in page and 'class="flag-unplanned"' in page
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.req("lockstep-guard/a-write-inside-a-worktree-is-judged-by-that-worktree-s-plan")
def test_a_write_inside_a_worktree_is_judged_by_its_plan(repo):
    wt = repo / "worktrees/feature"
    (wt / "src").mkdir(parents=True)
    (wt / ".git").write_text("gitdir: elsewhere\n")
    (wt / "lockstep.yaml").write_text("governed: [src/]\nlayout:\n- path: src/a.py\n  purpose: A\n")
    (wt / "generated/wiki").mkdir(parents=True)
    (wt / "generated/wiki/index.md").write_text("# index\n")
    t = _write(repo / "t.jsonl", _claude(
        ("Write", {"file_path": str(wt / "lockstep.yaml"), "content": "layout:\n- path: src/a.py\n"}, "File created"),
        ("Write", {"file_path": str(wt / "src/a.py"), "content": "a = 1\n"}, "File created"),
        ("Write", {"file_path": str(wt / "src/b.py"), "content": "b = 1\n"}, "File created")))
    tools = [e for e in session_events(t, repo) if e["kind"] == "tool"]
    assert [(e["plan_write"], e.get("planned")) for e in tools] == [(True, None), (False, "planned"), (False, "unplanned")]
    server = make_server(t, repo, None, 0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        port = server.server_address[1]
        assert json.loads(_get(port, "/api/data?session=main")[1])["checkout"] == "worktrees/feature/"
        assert json.loads(_get(port, "/api/wiki?checkout=worktrees/feature/")[1]) == ["worktrees/feature/generated/wiki/index.md"]
        assert _get(port, "/api/wiki?checkout=../../etc/")[0] == 404
    finally:
        server.shutdown()
        server.server_close()


def test_a_file_in_another_repository_is_outside_and_not_a_plan_write(repo, tmp_path_factory):
    other = tmp_path_factory.mktemp("other")
    (other / ".git").mkdir()
    (other / "src").mkdir()
    (other / "lockstep.yaml").write_text("governed: [src/]\nlayout: []\n")
    t = _write(repo / "t.jsonl", _claude(
        ("Write", {"file_path": str(other / "lockstep.yaml"), "content": "layout: []\n"}, "File created"),
        ("Write", {"file_path": str(other / "src/x.py"), "content": "x = 1\n"}, "File created")))
    tools = [e for e in session_events(t, repo) if e["kind"] == "tool"]
    assert [(e["plan_write"], e.get("planned")) for e in tools] == [(False, "outside"), (False, "outside")]


def test_status_for_an_unknown_checkout_is_404_and_a_bad_plan_is_not_a_crash(repo):
    (repo / "lockstep.yaml").write_text("layout: [unclosed\n")
    server = _serve(repo)
    try:
        port = server.server_address[1]
        assert _get(port, "/api/status?checkout=../../etc/")[0] == 404
        code, body = _get(port, "/api/plan?file=src/greet.py")
        assert code == 200 and json.loads(body)["row"] is None
    finally:
        server.shutdown()
        server.server_close()

"""`lockstep reads`: each write in a session, with what was read before it (Milestone 1 step 4)."""
import json
from pathlib import Path

import pytest

from lockstep.read_before_write import main, report

GREET = '"""Greeter.\n\nImplements: greeter/the-greeter-says-hello\n"""\n\n\ndef greet() -> str:\n    return "hello"\n'


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
    out = []
    for n, (name, inp, result, *attach) in enumerate(calls):
        uid = f"toolu_{n}"
        out.append({"type": "assistant", "uuid": f"a{n}", "message": {"content": [
            {"type": "tool_use", "id": uid, "name": name, "input": inp}]}})
        for text in attach:
            out.append({"type": "attachment", "parentUuid": f"a{n}",
                        "attachment": {"type": "hook_additional_context", "toolUseID": uid, "content": [text]}})
        out.append({"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": uid, "content": result}]}})
    return out


def _write(path: Path, records: list[dict]) -> Path:
    path.write_text("".join(json.dumps(r) + "\n" for r in records))
    return path


def _rows(repo: Path, records: list[dict]) -> list[dict]:
    return report(_write(repo / "t.jsonl", records), repo)


@pytest.mark.req("lockstep-guard/an-edit-after-reading-only-the-file-is-counted-and-not-warned")
def test_an_edit_after_reading_only_the_file(repo, capsys):
    t = _write(repo / "t.jsonl", _claude(
        ("Read", {"file_path": str(repo / "src/greet.py")}, "1\tGreeter"),
        ("Edit", {"file_path": str(repo / "src/greet.py"), "old_string": "a", "new_string": "b"}, "updated")))
    assert main([str(t), "--repo", str(repo)]) == 0
    out = capsys.readouterr().out
    assert "WARN" not in out
    assert "RESULT writes=1 new=0 file_read_first=1 context_read_first=0 handover=0 unread=0" in out
    row, = report(t, repo)
    assert (row["file"], row["file_read_first"], row["context_read_first"]) == ("src/greet.py", True, False)


@pytest.mark.req("lockstep-guard/a-write-with-nothing-read-first-is-warned-but-not-blocked")
def test_a_write_with_nothing_read_is_warned(repo, capsys):
    t = _write(repo / "t.jsonl", _claude(
        ("Bash", {"command": f"cd {repo} && printf 'x' > src/greet.py"}, "")))
    assert main([str(t), "--repo", str(repo)]) == 0
    out = capsys.readouterr().out
    assert "WARN" in out and "src/greet.py" in out
    assert "unread=1" in out


@pytest.mark.req("lockstep-guard/reading-the-wiki-page-counts-as-context")
def test_reading_the_wiki_page_counts_as_context(repo):
    row, = _rows(repo, _claude(
        ("Bash", {"command": f"cat {repo}/generated/wiki/greeter.md"}, "# greeter"),
        ("Edit", {"file_path": str(repo / "src/greet.py")}, "updated")))
    assert row["context_read_first"] and not row["file_read_first"]


def test_reading_the_spec_counts_as_context(repo):
    row, = _rows(repo, _claude(
        ("Read", {"file_path": str(repo / "openspec/specs/greeter/spec.md")}, "x"),
        ("Edit", {"file_path": str(repo / "src/greet.py")}, "updated")))
    assert row["context_read_first"]


def test_a_read_after_the_write_does_not_count(repo):
    row, = _rows(repo, _claude(
        ("Edit", {"file_path": str(repo / "src/greet.py")}, "updated"),
        ("Read", {"file_path": str(repo / "src/greet.py")}, "x")))
    assert not row["file_read_first"]


@pytest.mark.req("lockstep-guard/the-hand-over-is-marked")
def test_the_hand_over_is_marked(repo):
    row, = _rows(repo, _claude(
        ("Edit", {"file_path": str(repo / "src/greet.py")}, "updated",
         "Requirement text for src/greet.py, from OpenSpec (its docstring says Implements: greeter/x):")))
    assert row["handover"]


@pytest.mark.req("lockstep-guard/a-created-file-is-new-not-unread")
def test_a_created_file_is_new(repo, capsys):
    t = _write(repo / "t.jsonl", _claude(
        ("Write", {"file_path": str(repo / "src/new_mod.py"), "content": "x"},
         f"File created successfully at: {repo}/src/new_mod.py")))
    main([str(t), "--repo", str(repo)])
    out = capsys.readouterr().out
    assert "WARN" not in out and "new=1" in out and "unread=0" in out


@pytest.mark.req("lockstep-guard/an-unreadable-transcript-exits-2")
def test_an_unreadable_transcript_exits_2(repo):
    assert main([str(repo / "missing.jsonl"), "--repo", str(repo)]) == 2


def test_writes_outside_the_repository_are_left_out(repo, tmp_path_factory):
    other = tmp_path_factory.mktemp("other")
    assert _rows(repo, _claude(("Write", {"file_path": str(other / "x.py")}, "File created successfully"))) == []


def test_json_output(repo, capsys):
    t = _write(repo / "t.jsonl", _claude(("Edit", {"file_path": str(repo / "src/greet.py")}, "updated")))
    assert main([str(t), "--repo", str(repo), "--json"]) == 0
    rows = json.loads(capsys.readouterr().out)
    assert rows[0]["file"] == "src/greet.py" and rows[0]["unread"] is True


def test_claude_stream_json_is_read(repo):
    """`claude -p --output-format stream-json` carries the same message shape without uuids."""
    recs = _claude(("Read", {"file_path": str(repo / "src/greet.py")}, "x"),
                   ("Edit", {"file_path": str(repo / "src/greet.py")}, "updated"))
    for r in recs:
        r.pop("uuid", None)
    row, = _rows(repo, recs)
    assert row["file_read_first"]


@pytest.mark.req("lockstep-guard/a-codex-exec-stream-is-read")
def test_a_codex_exec_stream(repo):
    row, = _rows(repo, [
        {"type": "thread.started", "thread_id": "t"},
        {"type": "item.completed", "item": {"type": "command_execution", "command": "/bin/bash -lc 'cat src/greet.py'",
                                            "aggregated_output": GREET, "exit_code": 0}},
        {"type": "item.completed", "item": {"type": "file_change",
                                            "changes": [{"path": str(repo / "src/greet.py"), "kind": "update"}]}}])
    assert row["file_read_first"]


@pytest.mark.req("lockstep-guard/a-codex-rollout-uses-codex-s-own-read-parse")
def test_a_codex_rollout(repo):
    def item(it):
        return {"type": "event_msg", "payload": {"type": "item_completed", "item": it}}
    row, = _rows(repo, [
        {"type": "session_meta", "payload": {"cwd": str(repo)}},
        item({"type": "CommandExecution", "command": ["/bin/bash", "-lc", "less -N src/greet.py"],
              "cwd": f"file://{repo}", "parsed_cmd": [{"type": "read", "path": "src/greet.py"}]}),
        {"type": "response_item", "payload": {"type": "message", "role": "developer", "content": [
            {"type": "input_text", "text": "Requirement text for src/greet.py, from OpenSpec"}]}},
        item({"type": "FileChange", "changes": {str(repo / "src/greet.py"): {"type": "update"}}})])
    assert row["file_read_first"] and row["handover"]


def test_a_codex_add_is_new(repo):
    row, = _rows(repo, [{"type": "item.completed", "item": {"type": "file_change", "changes": [
        {"path": str(repo / "src/n.py"), "kind": "add"}]}}])
    assert row["new"] and not row["unread"]


def test_a_codex_hand_over_on_a_read_is_not_given_to_the_next_write(repo):
    def item(it):
        return {"type": "event_msg", "payload": {"type": "item_completed", "item": it}}
    dev = {"type": "response_item", "payload": {"type": "message", "role": "developer", "content": [
        {"type": "input_text", "text": "Requirement text for src/greet.py, from OpenSpec"}]}}
    row, = _rows(repo, [
        dev, item({"type": "CommandExecution", "command": ["cat", "src/greet.py"], "cwd": str(repo),
                   "parsed_cmd": [{"type": "read", "path": "src/greet.py"}]}),
        item({"type": "FileChange", "changes": {str(repo / "src/greet.py"): {"type": "update"}}})])
    assert not row["handover"]


def test_a_claude_shell_write_with_a_hand_over_is_marked(repo):
    row, = _rows(repo, _claude(("Bash", {"command": f"printf x > {repo}/src/greet.py"}, "",
                                "Requirement text for src/greet.py, from OpenSpec")))
    assert row["handover"]


def test_paths_named_inside_a_python_heredoc_are_not_writes(repo):
    cmd = f"cd {repo} && python3 - <<'EOF'\nopen('lockstep.yaml','w').write('x')\nprint('greeter/the-greeter-says-hello')\nEOF"
    (repo / "lockstep.yaml").write_text("")
    rows = _rows(repo, _claude(("Bash", {"command": cmd}, "")))
    assert rows == []  # which of the named paths the code writes is unknown, so none is counted


def test_a_heredoc_redirect_is_a_write_not_a_read(repo):
    row, = _rows(repo, _claude(("Bash", {"command": f"cat > {repo}/src/greet.py <<'EOF'\nx\nEOF"}, "")))
    assert row["file"] == "src/greet.py" and not row["file_read_first"]


def test_a_file_the_session_wrote_whole_counts_as_read(repo):
    (repo / "src/n.py").write_text("x")
    rows = _rows(repo, _claude(
        ("Write", {"file_path": str(repo / "src/n.py"), "content": "x"}, "File created successfully"),
        ("Bash", {"command": f"printf y > {repo}/src/n.py"}, "")))
    assert rows[1]["file_read_first"]


def test_a_relative_shell_path_uses_the_folder_of_the_call(repo, tmp_path_factory):
    rec = _claude(("Bash", {"command": "printf x > greet.py"}, ""))
    rec[0]["cwd"] = str(repo / "src")
    row, = _rows(repo, rec)
    assert row["file"] == "src/greet.py"


def test_the_layout_plan_hand_over_is_marked(repo):
    row, = _rows(repo, _claude(("Edit", {"file_path": str(repo / "src/greet.py")}, "updated",
                                "Plan for src/greet.py (src:greet.py), from lockstep.yaml layout and OpenSpec:")))
    assert row["handover"]


def _git(repo: Path, *args: str) -> None:
    import subprocess
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def test_a_shell_write_creating_a_file_git_never_saw_is_new(repo):
    _git(repo, "init", "-q")
    _git(repo, "-c", "user.email=t@t", "-c", "user.name=t", "add", "src/greet.py")
    _git(repo, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "x")
    rows = _rows(repo, _claude(("Bash", {"command": f"cat > {repo}/src/fresh.py <<'EOF'\nx\nEOF"}, ""),
                               ("Bash", {"command": f"printf y > {repo}/src/greet.py"}, "")))
    assert [(r["file"], r["new"], r["file_read_first"], r["unread"]) for r in rows] == [
        ("src/fresh.py", True, False, False), ("src/greet.py", False, False, True)]


def test_a_sed_script_is_not_a_written_path(repo):
    rows = _rows(repo, _claude(("Bash", {"command": f"sed -i 's|a/b|c|' {repo}/src/greet.py"}, "")))
    assert [r["file"] for r in rows] == ["src/greet.py"]

"""Behavior 5.1: at edit time the hook warns about an edit to a file the plan does not declare,
and refuses it for a file the side file marks fixed (or everywhere under PCW_MODE=block).

Also the hook's path extraction for Claude Code, Codex and OpenHands payloads, and the
would-block count (`pcw-hook --would-block`).
"""

import datetime as dt
import io
import json
from pathlib import Path
import re
import subprocess
import sys

import pytest

from lockstep.hook import WARN_PREFIX, decide, main, paths_from_call, shell_command, would_block_counts


def test_codex_registration_matches_native_normalized_shell_and_delivers_plan(proj):
    """Codex exec_command hooks carry tool_name Bash and tool_input.command."""
    config = json.loads((Path(__file__).resolve().parent / "lockstep-plan-sample/.codex/hooks.json").read_text())
    assert any(re.fullmatch(group["matcher"], "Bash") for group in config["hooks"]["PreToolUse"]
               if any("pcw-hook" in handler.get("command", "") for handler in group["hooks"]))
    payload = {"tool_name": "Bash", "tool_input": {"command": "cat src/greeter/__init__.py"}, "cwd": str(proj)}
    out = decide(payload)["hookSpecificOutput"]
    assert out["permissionDecision"] == "allow"
    assert "Plan for src/greeter/__init__.py" in out["additionalContext"]
    assert "NI-001" in out["additionalContext"]


def test_codex_cli_context_only_allow_warning_and_supported_fixed_deny(proj):
    """Codex rejects allow without updatedInput; context-only pass and deny are supported."""
    def invoke(command):
        payload = {"tool_name": "Bash", "tool_input": {"command": command}, "cwd": str(proj)}
        done = subprocess.run([sys.executable, "-I", "-m", "lockstep.hook", "--client", "codex"],
                              input=json.dumps(payload), capture_output=True, text=True, cwd=proj)
        assert done.returncode == 0, done.stderr
        return json.loads(done.stdout)["hookSpecificOutput"]

    read = invoke("cat src/greeter/__init__.py")
    assert read["hookEventName"] == "PreToolUse"
    assert "permissionDecision" not in read and "updatedInput" not in read
    assert "NI-001" in read["additionalContext"]
    warning = invoke("echo x >> src/greeter/__init__.py")
    assert "permissionDecision" not in warning
    assert warning["additionalContext"].startswith(WARN_PREFIX)
    fix(proj, "src/greeter/*")
    denied = invoke("echo x >> src/greeter/__init__.py")
    assert denied["permissionDecision"] == "deny"
    assert "skips the plan check" in denied["permissionDecisionReason"]


def test_codex_registration_selects_codex_output_protocol():
    config = json.loads((Path(__file__).resolve().parent / "lockstep-plan-sample/.codex/hooks.json").read_text())
    commands = [handler["command"] for group in config["hooks"]["PreToolUse"] for handler in group["hooks"]
                if "pcw-hook" in handler.get("command", "")]
    assert commands and all("--client codex" in command for command in commands)


def test_openhands_native_cli_reads_warnings_fixed_denials_and_log_immutability(proj, tmp_path):
    """Native SDK uses working_dir and flat HookResult JSON; exit-zero deny blocks."""
    def invoke(tool, tool_input):
        payload = {"event_type": "PreToolUse", "tool_name": tool, "tool_input": tool_input,
                   "working_dir": str(proj), "session_id": "openhands-test"}
        done = subprocess.run([sys.executable, "-I", "-m", "lockstep.hook", "--client", "openhands"],
                              input=json.dumps(payload), capture_output=True, text=True, cwd=tmp_path)
        assert done.returncode == 0, done.stderr
        out = json.loads(done.stdout)
        assert "hookSpecificOutput" not in out
        return out

    view = invoke("file_editor", {"path": "src/greeter/__init__.py", "command": "view"})
    assert view["decision"] == "allow" and "NI-001" in view["additionalContext"]
    terminal = invoke("terminal", {"command": "cat src/greeter/__init__.py"})
    assert terminal["decision"] == "allow" and "NI-001" in terminal["additionalContext"]
    create = {"path": "src/greeter/extra.py", "command": "create", "file_text": "pass"}
    assert invoke("file_editor", create)["additionalContext"].startswith(WARN_PREFIX)
    fix(proj, "src/greeter/*")
    assert invoke("file_editor", create)["decision"] == "deny"
    path = proj / "src/greeter/__init__.py"
    path.write_text(path.read_text().replace("Plan (generated", "Old plan (generated"))
    read_stale = invoke("file_editor", {"path": "src/greeter/__init__.py", "command": "view"})
    assert read_stale["decision"] == "allow" and "NI-001" in read_stale["additionalContext"]
    denied = invoke("terminal", {"command": "echo x >> src/greeter/__init__.py"})
    assert denied["decision"] == "deny" and "skips the plan check" in denied["reason"]
    log_edit = invoke("file_editor", {"path": ".aes/plans/PLAN-001.yaml", "command": "str_replace"})
    assert log_edit["decision"] == "deny" and log_edit["reason"]


@pytest.fixture(autouse=True)
def _default_mode(monkeypatch):
    """Each test starts in the default mode (warn) unless it sets PCW_MODE itself."""
    monkeypatch.delenv("PCW_MODE", raising=False)
    monkeypatch.delenv("PCW_BLOCK_STALE", raising=False)


def hook(proj, tool: str, tool_input: dict) -> dict:
    return decide({"tool_name": tool, "tool_input": tool_input, "cwd": str(proj)})["hookSpecificOutput"]


def run_hook(proj, tool: str, tool_input: dict, monkeypatch, capsys) -> dict:
    """The hook as the agent client runs it: JSON on stdin, JSON on stdout, one log line written."""
    call = {"tool_name": tool, "tool_input": tool_input, "cwd": str(proj), "tool_use_id": "t1"}
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(call)))
    monkeypatch.setattr(sys, "argv", ["pcw-hook"])
    assert main() == 0
    return json.loads(capsys.readouterr().out)["hookSpecificOutput"]


def log_lines(proj) -> list[dict]:
    path = proj / ".pcw" / f"hook-{dt.date.today().isoformat()}.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines()]


def fix(proj, *globs: str) -> None:
    (proj / "lockstep.yaml").write_text("schema: lockstep.side.v1\nfixed: [" + ", ".join(f"'{g}'" for g in globs) + "]\n")


def test_by_default_an_undeclared_governed_file_is_warned_about_and_logged_as_would_block(proj, monkeypatch, capsys):
    out = run_hook(proj, "Write", {"file_path": str(proj / "src/greeter/extra.py")}, monkeypatch, capsys)
    assert out["permissionDecision"] == "allow" and "permissionDecisionReason" not in out
    assert out["additionalContext"].startswith(WARN_PREFIX) and "is not in the plan" in out["additionalContext"]
    (rec,) = log_lines(proj)
    assert rec["decision"] == "would_block" and rec["why"] == "unplanned" and rec["file"] == "src/greeter/extra.py"


def test_a_file_the_side_file_marks_fixed_is_still_refused(proj, monkeypatch, capsys):
    fix(proj, "src/greeter/*")
    out = run_hook(proj, "Write", {"file_path": str(proj / "src/greeter/extra.py")}, monkeypatch, capsys)
    assert out["permissionDecision"] == "deny" and "is not in the plan" in out["permissionDecisionReason"]
    assert log_lines(proj)[-1]["decision"] == "deny"
    # a file outside the fixed globs is only warned about
    assert hook(proj, "Write", {"file_path": str(proj / "tests/test_extra.py")})["permissionDecision"] == "allow"


def test_block_mode_refuses_an_edit_to_an_undeclared_governed_file(proj, monkeypatch):
    monkeypatch.setenv("PCW_MODE", "block")
    out = hook(proj, "Write", {"file_path": str(proj / "src/greeter/extra.py")})
    assert out["permissionDecision"] == "deny" and "is not in the plan" in out["permissionDecisionReason"]


def test_a_change_log_entry_is_refused_in_warn_mode_too(proj):
    out = hook(proj, "Write", {"file_path": str(proj / ".aes/plans/PLAN-001.yaml")})
    assert out["permissionDecision"] == "deny"


def test_edit_to_a_document_the_side_file_does_not_declare_is_refused(proj, monkeypatch):
    monkeypatch.setenv("PCW_MODE", "block")
    (proj / "lockstep.yaml").write_text("schema: lockstep.side.v1\ndocuments:\n  include: ['*.md']\n  declared:\n"
                                        "    - {path: README.md, purpose: front door, refs: [NI-001]}\n")
    out = hook(proj, "Write", {"file_path": str(proj / "docs/new.md")})
    assert out["permissionDecision"] == "deny" and "documents.declared in lockstep.yaml" in out["permissionDecisionReason"]
    assert decide({"tool_name": "Write", "tool_input": {"file_path": str(proj / "README.md")}, "cwd": str(proj)}) is None


def test_shell_write_to_a_planned_file_is_warned_about_by_default_and_refused_when_fixed(proj):
    out = hook(proj, "Bash", {"command": "echo x >> src/greeter/__init__.py"})
    assert out["permissionDecision"] == "allow" and out["additionalContext"].startswith(WARN_PREFIX)
    assert "skips the plan check" in out["additionalContext"]
    fix(proj, "src/greeter/__init__.py")
    out = hook(proj, "Bash", {"command": "echo x >> src/greeter/__init__.py"})
    assert out["permissionDecision"] == "deny" and "skips the plan check" in out["permissionDecisionReason"]


def test_shell_write_creating_an_unplanned_governed_file_is_refused_like_an_edit(proj, monkeypatch, capsys):
    """Q22: `echo x > <new module>` in a governed folder gets the edit's answer, not a silent pass."""
    out = run_hook(proj, "Bash", {"command": "echo x > src/greeter/zz_new.py"}, monkeypatch, capsys)
    assert out["permissionDecision"] == "allow" and out["additionalContext"].startswith(WARN_PREFIX)
    assert "src/greeter/zz_new.py" in out["additionalContext"] and "is not in the plan" in out["additionalContext"]
    rec = log_lines(proj)[-1]
    assert rec["decision"] == "would_block" and rec["why"] == "shell_unplanned" and rec["files"] == ["src/greeter/zz_new.py"]
    monkeypatch.setenv("PCW_MODE", "block")
    for command in ["echo x > src/greeter/zz_new.py", "cd src/greeter && echo x > zz_new.py",
                    "cd /tmp && echo x > " + str(proj / "src/greeter/zz_new.py"),
                    "printf x | tee -a src/greeter/zz_new.py", "touch src/greeter/zz_new.py",
                    "cp src/greeter/__init__.py src/greeter/zz_new.py",
                    "cat > src/greeter/zz_new.py <<'EOF'\nif a > b:\n    pass\nEOF",
                    "python - <<'E'\nopen('src/greeter/zz_new.py', 'w').write('x')\nE"]:
        out = hook(proj, "terminal", {"command": command})
        assert out["permissionDecision"] == "deny", command
        assert "src/greeter/zz_new.py" in out["permissionDecisionReason"] and "is not in the plan" in out["permissionDecisionReason"]


def test_shell_write_to_a_planned_file_after_cd_is_caught(proj, monkeypatch):
    monkeypatch.setenv("PCW_MODE", "block")
    out = hook(proj, "Bash", {"command": "cd src/greeter && echo x >> __init__.py"})
    assert out["permissionDecision"] == "deny" and "skips the plan check" in out["permissionDecisionReason"]


def test_shell_commands_that_write_no_governed_file_pass(proj, monkeypatch, capsys):
    monkeypatch.setenv("PCW_MODE", "block")
    for command in ["ls src/greeter > /tmp/x.txt 2>&1", "python -m pytest tests -q 2>&1 | tail -3",
                    "cat src/greeter/__init__.py | grep greet", "echo 'a > src/greeter/q.py'",
                    "git commit -m 'rm src/greeter/q.py'",
                    "echo x > .pcw/scratch.txt"]:
        out = decide({"tool_name": "Bash", "tool_input": {"command": command}, "cwd": str(proj)})
        assert out is None or out["hookSpecificOutput"]["permissionDecision"] == "allow", command
    # a write outside every governed folder is let through, and logged
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps({"tool_name": "Bash", "cwd": str(proj),
                                                              "tool_input": {"command": "echo x > notes.txt"}})))
    monkeypatch.setattr(sys, "argv", ["pcw-hook"])
    assert main() == 0 and capsys.readouterr().out == ""
    rec = log_lines(proj)[-1]
    assert rec["decision"] == "pass" and rec["files"] == ["notes.txt"]


def test_would_block_counts_per_day(proj, monkeypatch, capsys):
    run_hook(proj, "Write", {"file_path": str(proj / "src/greeter/extra.py")}, monkeypatch, capsys)
    run_hook(proj, "Write", {"file_path": str(proj / "src/greeter/more.py")}, monkeypatch, capsys)
    run_hook(proj, "Edit", {"file_path": str(proj / "src/greeter/__init__.py")}, monkeypatch, capsys)  # allowed, not counted
    old = proj / ".pcw" / "hook-2000-01-01.jsonl"
    old.write_text(json.dumps({"decision": "would_block", "why": "unplanned"}) + "\n")
    today = dt.date.today().isoformat()
    assert would_block_counts(proj, days=14) == {today: 2}
    monkeypatch.chdir(proj)
    monkeypatch.setattr(sys, "argv", ["pcw-hook", "--would-block", "--days", "14"])
    assert main() == 0
    assert f"{today} 2" in capsys.readouterr().out


def test_edit_to_a_declared_file_in_step_is_allowed_with_its_plan(proj):
    out = hook(proj, "Edit", {"file_path": str(proj / "src/greeter/__init__.py")})
    assert out["permissionDecision"] == "allow" and "NI-001" in out["additionalContext"]


def test_claude_edit_payload():
    call = {"tool_name": "Edit", "tool_input": {"file_path": "/p/src/a.py"}}
    assert paths_from_call(call) == ["/p/src/a.py"]


def test_codex_apply_patch_payload():
    patch = "*** Begin Patch\n*** Update File: src/a.py\n@@\n-x\n+y\n*** Add File: tests/t.py\n+z\n*** End Patch\n"
    call = {"tool_name": "apply_patch", "tool_input": {"input": patch}}
    assert paths_from_call(call) == ["src/a.py", "tests/t.py"]


def test_other_tools_are_ignored():
    assert paths_from_call({"tool_name": "Bash", "tool_input": {"command": "ls"}}) == []


def test_shell_write_detection():
    from lockstep.hook import shell_writes
    f = "src/a.py"
    writes = ["python - <<'E'\nopen('src/a.py','w').write(x)\nE", "sed -i 's/a/b/' src/a.py", "echo x > src/a.py",
              "cat >> src/a.py <<EOF", "cp b src/a.py", "printf x | tee src/a.py"]
    reads = ["cat src/a.py", "grep -n greet src/a.py", "sed -n 1,5p src/a.py", "git diff src/a.py",
             "python -m pytest tests 2>&1", 'git commit -m "x <a@b.com>" && aes evidence record VS --depends-on src/a.py',
             "make project >/dev/null && aes evidence record VS --depends-on src/a.py", "cat src/a.py > /tmp/copy.txt"]
    assert all(shell_writes(c, f) for c in writes), [c for c in writes if not shell_writes(c, f)]
    assert not any(shell_writes(c, f) for c in reads), [c for c in reads if shell_writes(c, f)]


def test_adopted_legacy_file_is_left_alone(tmp_path):
    """An existing project starts from `aes adopt`: its old files stay editable, new ones need a plan."""
    import json

    from lockstep.aes_bridge import is_governed

    (tmp_path / ".aes").mkdir()
    (tmp_path / ".aes/project.yaml").write_text("governed_roots: [deploy/]\n")
    (tmp_path / ".aes/target.yaml").write_text("planned_artifacts: []\n")
    (tmp_path / ".aes/legacy_baseline.json").write_text(json.dumps({"files": {"deploy/old.py": "abc"}}))
    assert not is_governed(tmp_path, "deploy/old.py")
    assert is_governed(tmp_path, "deploy/new.py")
    assert not is_governed(tmp_path, "src/other.py")


def test_openhands_file_editor_names_its_path():
    call = {"tool_name": "file_editor", "tool_input": {"command": "str_replace", "path": "/workspace/repo/src/a.py"}}
    assert paths_from_call(call) == ["/workspace/repo/src/a.py"]
    assert paths_from_call({"tool_name": "file_editor", "tool_input": {"command": "view", "path": "/w/src/a.py"}}) == []


def test_openhands_terminal_is_a_shell_tool():
    assert shell_command({"tool_name": "terminal", "tool_input": {"command": "echo x > src/a.py"}}) == "echo x > src/a.py"


def test_a_refusal_or_warning_points_at_the_wiki(proj, monkeypatch):
    """Q20: an agent that is stopped is told where to look next."""
    out = hook(proj, "Write", {"file_path": str(proj / "src/greeter/extra.py")})
    assert out["permissionDecision"] == "allow" and "python -m lockstep.wiki" in out["additionalContext"]
    monkeypatch.setenv("PCW_MODE", "block")
    out = hook(proj, "Bash", {"command": "echo x > src/greeter/extra.py"})
    assert out["permissionDecision"] == "deny" and "python -m lockstep.wiki" in out["permissionDecisionReason"]


def test_every_call_the_hook_sees_is_logged_including_silent_passes(proj, monkeypatch, capsys):
    """Q21: a call let through with nothing to say leaves a log line too, with the shell command it ran."""
    for tool, tool_input in [("Bash", {"command": "ls src && git status --short"}),
                             ("Write", {"file_path": str(proj / "notes.txt")}),
                             ("Bash", {"command": "cat src/greeter/__init__.py"})]:
        monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps({"tool_name": tool, "tool_input": tool_input,
                                                                  "cwd": str(proj), "tool_use_id": tool})))
        monkeypatch.setattr(sys, "argv", ["pcw-hook"])
        assert main() == 0
        capsys.readouterr()
    ls, note, read = log_lines(proj)
    assert (ls["decision"], ls["why"], ls["command"], ls["files"]) == ("pass", "no_rule", "ls src && git status --short", [])
    assert (note["decision"], note["files"], note["tool_use_id"]) == ("pass", ["notes.txt"], "Write") and "command" not in note
    assert read["decision"] == "allow" and read["why"] == "shell_read" and read["command"] == "cat src/greeter/__init__.py"


def test_a_call_outside_any_project_is_not_logged(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps({"tool_name": "Bash", "tool_input": {"command": "ls"},
                                                              "cwd": str(tmp_path)})))
    monkeypatch.setattr(sys, "argv", ["pcw-hook"])
    assert main() == 0 and capsys.readouterr().out == ""
    assert not (tmp_path / ".pcw").exists()

"""Slice 2 of the one-tool design: the plan is OpenSpec plus `layout:` rows in lockstep.yaml, with no .aes/."""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from lockstep_support import ENV, REPO, sh

from lockstep import hook
from lockstep.aes_bridge import artifact_for_path, find_root, governed_roots, target
from lockstep.check import check
from lockstep.layout_plan import artifact_id, layout_problems
from lockstep.side_file import side_file_problems

LAYOUT = REPO / "example-layout"
BIN = Path(sys.executable).parent


@pytest.fixture
def lay(tmp_path) -> Path:
    proj = tmp_path / "greeter"
    shutil.copytree(LAYOUT, proj)
    (proj / ".gitignore").write_text("__pycache__/\n.lockstep/\n")
    sh("git init -q -b main && git add -A && git commit -q -m plan", proj)
    return proj


def _layout(proj: Path) -> str:
    return sh(f"{BIN / 'lockstep'} layout", proj)


def _hook(call: dict, monkeypatch, capsys) -> dict:
    import io
    monkeypatch.setenv("PCW_MODE", "block")
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(call)))
    monkeypatch.setattr(sys, "argv", ["lockstep-hook"])
    assert hook.main() == 0
    return json.loads(capsys.readouterr().out)["hookSpecificOutput"]


def test_the_layout_rows_are_the_planned_files(lay):
    assert find_root(lay / "src") == lay.resolve() or find_root(lay) == lay.resolve()
    assert governed_roots(lay) == ["src/"]
    paths = [a["locator"]["exact_path"] for a in target(lay)["planned_artifacts"]]
    assert paths == ["src/greeter/__init__.py", "tests/test_greet.py"]
    assert artifact_for_path(lay, "src/greeter/__init__.py") == artifact_id("src/greeter/__init__.py")
    assert side_file_problems(lay, target(lay)) == []  # layout: and governed: are lockstep.yaml keys


@pytest.mark.req("lockstep-plan-format/the-layout-is-laid-out-with-first-docstrings")
def test_lockstep_layout_creates_each_file_with_its_requirement_criteria_and_tests(lay):
    out = _layout(lay)
    assert "src/greeter/__init__.py" in out and "tests/test_greet.py" in out
    text = (lay / "src/greeter/__init__.py").read_text()
    assert "Implements: greeting/greet-by-name" in text
    assert "`greet(name)` SHALL return `Hello, <name>!`." in text            # the requirement, word for word
    assert "#### Scenario: A name is greeted" in text and "returns `Hello, Ada!`" in text   # its success criteria
    assert "Tested by: tests/test_greet.py" in text                              # the test names
    assert "greet(name: str) -> str" in text                                     # the declared signature
    assert "Implements: greeting/greet-by-name" in (lay / "tests/test_greet.py").read_text()
    again = _layout(lay)
    assert "already exists" in again and (lay / "src/greeter/__init__.py").read_text() == text   # never overwritten


@pytest.mark.req("lockstep-plan-format/an-unplanned-file-is-refused-against-the-layout")
def test_the_edit_hook_refuses_an_unplanned_file_and_names_the_layout(lay, monkeypatch, capsys):
    _layout(lay)
    call = {"hook_event_name": "PreToolUse", "cwd": str(lay), "tool_name": "Write",
            "tool_input": {"file_path": str(lay / "src/greeter/extra.py"), "content": "x = 1\n"}}
    out = _hook(call, monkeypatch, capsys)
    assert out["permissionDecision"] == "deny"
    assert "lockstep.yaml" in out["permissionDecisionReason"]


@pytest.mark.req("lockstep-plan-format/an-unplanned-file-is-refused-against-the-layout")
def test_the_shell_guard_reads_the_layout_too(lay, monkeypatch, capsys):
    _layout(lay)
    write = {"hook_event_name": "PreToolUse", "cwd": str(lay), "tool_name": "Bash",
             "tool_input": {"command": "cat > src/extra.py <<'EOF'\nx = 1\nEOF"}}
    out = _hook(write, monkeypatch, capsys)
    assert out["permissionDecision"] == "deny" and "no `layout:` row in lockstep.yaml" in out["permissionDecisionReason"]
    read = {"hook_event_name": "PreToolUse", "cwd": str(lay), "tool_name": "Bash",
            "tool_input": {"command": "cp src/greeter/__init__.py /tmp/x"}}
    assert _hook(read, monkeypatch, capsys)["permissionDecision"] == "allow"


@pytest.mark.req("lockstep-plan-format/a-planned-file-s-edit-hands-over-its-requirement")
def test_the_edit_hook_hands_over_the_openspec_requirement(lay, monkeypatch, capsys):
    _layout(lay)
    sh("git add -A && git commit -q -m laid-out", lay)
    path = lay / "src/greeter/__init__.py"
    call = {"hook_event_name": "PreToolUse", "cwd": str(lay), "tool_name": "Edit",
            "tool_input": {"file_path": str(path), "old_string": "    pass", "new_string": "    pass  # body"}}
    out = _hook(call, monkeypatch, capsys)
    assert out["permissionDecision"] == "allow", out
    assert "SHALL return `Hello, <name>!`" in out["additionalContext"]


@pytest.mark.req("lockstep-plan-format/the-whole-tree-check-reads-the-layout")
def test_lockstep_check_allows_the_laid_out_tree_and_blocks_an_unplanned_file(lay):
    _layout(lay)
    sh("git add -A && git commit -q -m laid-out", lay)
    assert check(lay)["decision"] == "allow", check(lay)
    (lay / "src/greeter/extra.py").write_text("x = 1\n")
    out = check(lay)
    assert out["decision"] == "block"
    assert [(f["path"], f["kind"]) for f in out["files"] if f["blocks"]] == [("src/greeter/extra.py", "unplanned")]


@pytest.mark.req("lockstep-plan-format/a-layout-row-must-name-real-requirements")
def test_a_row_naming_an_unknown_requirement_or_no_purpose_is_reported(lay):
    assert layout_problems(lay) == []
    text = (lay / "lockstep.yaml").read_text()
    (lay / "lockstep.yaml").write_text(text.replace("implements: [greeting/greet-by-name]\n    tests:",
                                                    "implements: [greeting/wave]\n    tests:", 1)
                                       .replace("    purpose: prove that greet greets by name\n", ""))
    problems = layout_problems(lay)
    assert any("greeting/wave" in p and "src/greeter/__init__.py" in p for p in problems), problems
    assert any("tests/test_greet.py" in p and "purpose" in p for p in problems), problems


@pytest.mark.req("lockstep-plan-format/an-aes-plan-is-still-read")
def test_a_repository_with_an_aes_plan_is_read_as_before(proj):
    assert (proj / ".aes/target.yaml").is_file()
    assert artifact_for_path(proj, "src/greeter/__init__.py") == "ART-GREET"
    assert check(proj)["decision"] == "allow"

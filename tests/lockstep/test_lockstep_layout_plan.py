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
    assert "permissionDecision" not in _hook(read, monkeypatch, capsys)


@pytest.mark.req("lockstep-plan-format/a-planned-file-s-edit-hands-over-its-requirement")
def test_the_edit_hook_hands_over_the_openspec_requirement(lay, monkeypatch, capsys):
    _layout(lay)
    sh("git add -A && git commit -q -m laid-out", lay)
    path = lay / "src/greeter/__init__.py"
    call = {"hook_event_name": "PreToolUse", "cwd": str(lay), "tool_name": "Edit",
            "tool_input": {"file_path": str(path), "old_string": "    pass", "new_string": "    pass  # body"}}
    out = _hook(call, monkeypatch, capsys)
    assert "permissionDecision" not in out, out
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


EXISTING = '''"""The greet function, written before its layout row.

Implements: greeting/greet-by-name
"""


def greet(name: str) -> str:
    """Return the greeting."""
    return f"Hello, {name}!"
'''

# `lockstep check project` collects a requirement's text until its `Source:` line, so these put the text first.
SPEC = """# greeting Specification

## Purpose

Greet a person by name.

## Requirements

### Requirement: Greet by name

`greet(name)` SHALL return `Hello, <name>!`.

Source: inferred by agent, the smallest example for Lockstep's layout plan.

#### Scenario: A name is greeted

- **GIVEN** the name `Ada`
- **WHEN** `greet` is called with it
- **THEN** it returns `Hello, Ada!`
"""

CHANGED = """## MODIFIED Requirements

### Requirement: Greet by name

`greet(name)` SHALL return `Hello, <name>!` with the name trimmed.

Source: inferred by agent, the smallest example for Lockstep's layout plan.

#### Scenario: A name is greeted

- **GIVEN** the name `Ada`
- **WHEN** `greet` is called with it
- **THEN** it returns `Hello, Ada!`
"""


def _edit_existing(lay: Path, monkeypatch, capsys) -> dict:
    path = lay / "src/greeter/__init__.py"
    call = {"hook_event_name": "PreToolUse", "cwd": str(lay), "tool_name": "Edit",
            "tool_input": {"file_path": str(path), "old_string": "    return", "new_string": "    return  "}}
    return _hook(call, monkeypatch, capsys)


@pytest.mark.req("lockstep-plan-format/an-existing-file-with-a-current-implements-block-can-be-edited")
def test_a_file_written_before_its_layout_row_can_be_edited(lay, monkeypatch, capsys):
    (lay / "openspec/specs/greeting/spec.md").write_text(SPEC)
    (lay / "src/greeter").mkdir(parents=True)
    (lay / "src/greeter/__init__.py").write_text(EXISTING)
    sh(f"{BIN / 'lockstep'} check project", lay)
    assert "Requirement text (generated)" in (lay / "src/greeter/__init__.py").read_text()
    sh("git add -A && git commit -q -m existing", lay)
    out = _edit_existing(lay, monkeypatch, capsys)
    assert "permissionDecision" not in out, out
    assert "SHALL return `Hello, <name>!`" in out["additionalContext"]


@pytest.mark.req("lockstep-plan-format/a-stale-implements-block-names-the-command-that-fixes-it")
def test_a_stale_implements_block_is_refused_until_lockstep_check_project_runs(lay, monkeypatch, capsys):
    (lay / "openspec/specs/greeting/spec.md").write_text(SPEC)
    (lay / "src/greeter").mkdir(parents=True)
    (lay / "src/greeter/__init__.py").write_text(EXISTING)
    sh(f"{BIN / 'lockstep'} check project", lay)
    change = lay / "openspec/changes/trim-name/specs/greeting"
    change.mkdir(parents=True)
    (change / "spec.md").write_text(CHANGED)
    (lay / "openspec/changes/trim-name/proposal.md").write_text("## Why\n\nTrim names.\n\n## What Changes\n\n- trim\n")
    sh("git add -A && git commit -q -m change", lay)
    out = _edit_existing(lay, monkeypatch, capsys)
    assert out["permissionDecision"] == "deny", out
    reason = out["permissionDecisionReason"]
    assert "lockstep check project" in reason and "make project" not in reason, reason
    sh(f"{BIN / 'lockstep'} check project", lay)
    assert "with the name trimmed" in (lay / "src/greeter/__init__.py").read_text()
    out = _edit_existing(lay, monkeypatch, capsys)
    assert "permissionDecision" not in out, out
    assert "with the name trimmed" in out["additionalContext"]


def _existing_committed(lay: Path) -> None:
    (lay / "openspec/specs/greeting/spec.md").write_text(SPEC)
    (lay / "src/greeter").mkdir(parents=True)
    (lay / "src/greeter/__init__.py").write_text(EXISTING)
    sh(f"{BIN / 'lockstep'} check project", lay)
    sh("git add -A && git commit -q -m existing", lay)


@pytest.mark.req("lockstep-plan-format/the-commit-check-judges-an-implements-block-the-same-way")
def test_the_commit_check_allows_a_current_implements_block_and_blocks_a_stale_one(lay):
    _existing_committed(lay)
    path = lay / "src/greeter/__init__.py"
    path.write_text(path.read_text().replace("    return f", "    return  f"))
    out = check(lay)
    assert out["decision"] == "allow", out
    change = lay / "openspec/changes/trim-name/specs/greeting"
    change.mkdir(parents=True)
    (change / "spec.md").write_text(CHANGED)
    out = check(lay)
    stale = [f for f in out["files"] if f["path"] == "src/greeter/__init__.py"]
    assert out["decision"] == "block" and stale[0]["kind"] == "stale", out
    assert "lockstep check project" in stale[0]["reason"] and ".aes/target.yaml" not in stale[0]["reason"]
    sh(f"{BIN / 'lockstep'} check project", lay)
    assert check(lay)["decision"] == "allow"


@pytest.mark.req("lockstep-plan-format/an-undeclared-public-symbol-names-the-layout-exports")
def test_an_undeclared_public_function_points_to_the_layout_row(lay, monkeypatch, capsys):
    _existing_committed(lay)
    path = lay / "src/greeter/__init__.py"
    call = {"hook_event_name": "PreToolUse", "cwd": str(lay), "tool_name": "Edit",
            "tool_input": {"file_path": str(path), "old_string": "    return f\"Hello, {name}!\"\n",
                           "new_string": "    return f\"Hello, {name}!\"\n\n\ndef wave(name: str) -> str:\n"
                                         "    \"\"\"Wave.\"\"\"\n    return name\n"}}
    out = _hook(call, monkeypatch, capsys)
    assert out["permissionDecision"] == "deny", out
    reason = out["permissionDecisionReason"]
    assert "exports:" in reason and "lockstep.yaml" in reason and "aes plan" not in reason, reason


@pytest.mark.req("lockstep-projection/a-planned-file-s-plan-copy-follows-a-reworded-requirement")
def test_a_planned_file_s_plan_copy_follows_a_reworded_requirement(lay):
    from lockstep.check import docstring_mismatch
    from lockstep.checks.project import project
    _layout(lay)
    rel = "src/greeter/__init__.py"
    sh("git add -A && git commit -q -m laid-out", lay)
    assert project(lay, check=True) == [] or rel not in project(lay, check=True)  # no block written into the copy
    spec = lay / "openspec/specs/greeting/spec.md"
    spec.write_text(spec.read_text().replace("SHALL return `Hello, <name>!`.", "SHALL return `Hello, <name>!` exactly."))
    assert docstring_mismatch(lay, rel)                                   # the edit hook would refuse it now
    assert rel in project(lay)
    assert docstring_mismatch(lay, rel) is None                           # the named recovery works
    assert "SHALL return `Hello, <name>!` exactly." in (lay / rel).read_text()
    assert "Requirement text (generated):" not in (lay / rel).read_text()
    assert rel not in project(lay)                                        # idempotent


@pytest.mark.req("lockstep-projection/a-fixed-file-with-no-plan-copy-fails-the-check")
def test_a_fixed_file_with_no_plan_copy_fails_the_check(lay):
    side = lay / "lockstep.yaml"
    side.write_text(side.read_text().replace("governed: [src/]", 'governed: [src/]\nfixed: ["src/greeter/*"]'))
    (lay / "src/greeter").mkdir(parents=True)
    (lay / "src/greeter/__init__.py").write_text('"""Greet people."""\n\n\ndef greet(name: str) -> str:\n    return f"Hello, {name}!"\n')
    run = subprocess.run([str(BIN / "lockstep"), "check", "project", "--check"], cwd=lay, capture_output=True, text=True, env=ENV)
    assert run.returncode == 1, run.stdout + run.stderr
    assert "no-copy       src/greeter/__init__.py" in run.stdout, run.stdout
    (lay / "src/greeter/__init__.py").unlink()
    _layout(lay)
    run = subprocess.run([str(BIN / "lockstep"), "check", "project", "--check"], cwd=lay, capture_output=True, text=True, env=ENV)
    assert "no-copy" not in run.stdout, run.stdout


@pytest.mark.req("lockstep-plan-format/a-refusal-points-to-lockstep-show-not-the-wiki")
def test_a_refusal_in_a_layout_repository_points_to_lockstep_show(lay, monkeypatch, capsys):
    _layout(lay)
    call = {"hook_event_name": "PreToolUse", "cwd": str(lay), "tool_name": "Write",
            "tool_input": {"file_path": str(lay / "src/greeter/extra.py"), "content": "x = 1\n"}}
    reason = _hook(call, monkeypatch, capsys)["permissionDecisionReason"]
    assert "uv run lockstep show" in reason, reason
    assert "lockstep.wiki" not in reason, reason

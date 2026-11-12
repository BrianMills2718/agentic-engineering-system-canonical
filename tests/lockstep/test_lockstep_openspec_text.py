"""Behavior 3.7: in a repository with OpenSpec specs, the text the hook hands the agent before an edit is the
OpenSpec requirement the file implements (its `Implements: <capability>/<requirement>` docstring line);
`.aes/target.yaml` stays the source for a repository without OpenSpec (issue #54).
"""

import io
import json
from pathlib import Path
import sys

import pytest

from lockstep.hook import decide, main
from lockstep.openspec_text import find_spec_root, implemented_ids, read_requirements, requirement_packet, requirement_slug

SHIP_SPEC = """\
# ship Specification

## Purpose

Merge a pull request only when the check passed.

## Requirements

### Requirement: Merge only the commit whose check passed

`scripts/ship.py` SHALL run the repository's check and merge only when it exits 0.

Source: Brian, 2026-10-24, "i approve"

#### Scenario: A failing check pushes nothing

- **GIVEN** a clean branch whose check exits 1
- **WHEN** ship runs
- **THEN** it exits 1, and the branch is not on the remote

```sh
# a comment line inside a fence is not a heading
ship --check 'make check'
```

### Requirement: Prepare a fresh worktree's environment (`uv sync`), then check

Before the check, `scripts/ship.py` SHALL run `uv sync --all-extras`.

#### Scenario: A fresh worktree gets its environment

- **THEN** the environment is built first

## Other notes

Text under a plain heading is not part of any requirement.
"""

MERGE = "ship/merge-only-the-commit-whose-check-passed"
PREPARE = "ship/prepare-a-fresh-worktree-s-environment-uv-sync-then-check"


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


@pytest.fixture
def repo(tmp_path) -> Path:
    """A repository with one OpenSpec capability and one source file implementing its first requirement."""
    write(tmp_path / "openspec/specs/ship/spec.md", SHIP_SPEC)
    write(tmp_path / "scripts/ship.py", f'"""Ship.\n\nImplements: {MERGE}\n"""\n\nx = 1\n')
    return tmp_path


@pytest.fixture(autouse=True)
def _default_mode(monkeypatch):
    monkeypatch.delenv("PCW_MODE", raising=False)
    monkeypatch.delenv("PCW_BLOCK_STALE", raising=False)


def edit(root: Path, rel: str, tool: str = "Edit") -> dict | None:
    return decide({"tool_name": tool, "tool_input": {"file_path": str(root / rel)}, "cwd": str(root)})


def test_requirement_ids_are_capability_slash_slug():
    assert requirement_slug("Merge only the commit whose check passed") == "merge-only-the-commit-whose-check-passed"
    assert requirement_slug("Prepare a fresh worktree's environment (`uv sync`), then check") == \
        "prepare-a-fresh-worktree-s-environment-uv-sync-then-check"


def test_spec_root_is_the_nearest_folder_with_a_spec(repo):
    assert find_spec_root(repo / "scripts") == repo.resolve()
    assert find_spec_root(repo / "scripts" / "ship.py") == repo.resolve()
    (repo / "empty").mkdir()
    (repo / "empty" / "openspec").mkdir()
    assert find_spec_root(repo / "empty") == repo.resolve()  # an openspec folder with no spec.md is not a root


def test_a_requirement_is_its_text_scenarios_and_source_word_for_word(repo):
    reqs = read_requirements(repo)
    assert set(reqs) == {MERGE, PREPARE}
    text = reqs[MERGE]
    assert text.startswith("### Requirement: Merge only the commit whose check passed")
    assert "SHALL run the repository's check and merge only when it exits 0." in text
    assert 'Source: Brian, 2026-10-24, "i approve"' in text
    assert "#### Scenario: A failing check pushes nothing" in text
    assert "- **THEN** it exits 1, and the branch is not on the remote" in text
    assert "# a comment line inside a fence is not a heading" in text  # a fenced line is not a heading
    assert "uv sync" not in text and "Text under a plain heading" not in reqs[PREPARE]


def test_an_active_change_adds_and_overrides_but_an_archived_one_does_not(repo):
    write(repo / "openspec/changes/more/specs/ship/spec.md",
          "## ADDED Requirements\n\n### Requirement: Log every run\n\nShip SHALL log every run.\n\n"
          "## MODIFIED Requirements\n\n"
          "### Requirement: Merge only the commit whose check passed\n\nShip SHALL merge only the checked commit.\n")
    write(repo / "openspec/changes/archive/2026-01-01-old/specs/ship/spec.md",
          "### Requirement: Old and gone\n\nThis was archived.\n")
    reqs = read_requirements(repo)
    assert "ship/log-every-run" in reqs and "Ship SHALL log every run." in reqs["ship/log-every-run"]
    assert "Ship SHALL merge only the checked commit." in reqs[MERGE]
    assert "SHALL run the repository's check" not in reqs[MERGE]  # the active change's text wins over the spec's
    assert not any("old-and-gone" in ident for ident in reqs)


def test_implements_lines_are_read_from_module_class_and_function_docstrings(tmp_path):
    path = write(tmp_path / "m.py",
                 '"""Module.\n\nImplements: a/one, a/two,\n    a/three\n"""\n\n\n'
                 'class K:\n    """Class.\n\n    Implements: b/four\n    """\n\n'
                 '    def f(self):\n        """Fn.\n\n        Implements: c/five\n        """\n\n\n'
                 'def g():\n    # Implements: not/a-docstring\n    return 1\n')
    assert implemented_ids(path) == ["a/one", "a/two", "a/three", "b/four", "c/five"]
    assert implemented_ids(write(tmp_path / "bad.py", "def (:\n")) == []
    assert implemented_ids(tmp_path / "missing.py") == []
    assert implemented_ids(write(tmp_path / "x.md", "Implements: a/b\n")) == []


def test_the_packet_hands_over_each_requirement_and_names_one_that_does_not_exist(repo):
    write(repo / "scripts/two.py", f'"""Two.\n\nImplements: {MERGE}, ship/no-such-thing\n"""\n')
    ids, text = requirement_packet(repo, repo / "scripts/two.py")
    assert ids == [MERGE, "ship/no-such-thing"]
    assert "scripts/two.py" in text.splitlines()[0] and "OpenSpec" in text.splitlines()[0]
    assert "openspec/specs/ship/spec.md" in text and "SHALL run the repository's check" in text
    assert "ship/no-such-thing" in text and "no requirement" in text
    assert requirement_packet(repo, repo / "scripts/ship.py")[0] == [MERGE]
    write(repo / "plain.py", '"""Nothing implemented."""\n')
    assert requirement_packet(repo, repo / "plain.py") == ([], "")


def test_the_hook_hands_an_openspec_only_repository_the_requirement_text(repo):
    out = edit(repo, "scripts/ship.py")["hookSpecificOutput"]
    assert out["permissionDecision"] == "allow" and "permissionDecisionReason" not in out
    context = out["additionalContext"]
    assert "SHALL run the repository's check and merge only when it exits 0." in context
    assert "#### Scenario: A failing check pushes nothing" in context
    assert edit(repo, "scripts/ship.py", tool="Write") is not None
    write(repo / "plain.py", '"""Nothing implemented."""\n')
    assert edit(repo, "plain.py") is None  # nothing to hand over, so the hook stays silent
    assert edit(repo, "not_there_yet.py") is None


def test_the_hook_logs_what_it_handed_over(repo, monkeypatch, capsys):
    call = {"tool_name": "Edit", "tool_input": {"file_path": str(repo / "scripts/ship.py")}, "cwd": str(repo),
            "tool_use_id": "t7"}
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(call)))
    monkeypatch.setattr(sys, "argv", ["pcw-hook", "--client", "codex"])
    assert main() == 0
    out = json.loads(capsys.readouterr().out)["hookSpecificOutput"]
    assert "permissionDecision" not in out  # Codex gets context only
    assert "SHALL run the repository's check" in out["additionalContext"]
    (log,) = list((repo / ".lockstep").glob("hook-*.jsonl"))
    (rec,) = [json.loads(line) for line in log.read_text().splitlines()]
    assert rec["decision"] == "allow" and rec["why"] == "openspec_text" and rec["file"] == "scripts/ship.py"
    assert rec["requirements"] == [MERGE] and rec["tool_use_id"] == "t7"


def test_a_repository_with_a_plan_and_specs_gets_the_openspec_text_not_the_plan_text(proj):
    write(proj / "openspec/specs/greeter/spec.md",
          "## Requirements\n\n### Requirement: Greet by name\n\nGreeter SHALL greet by name.\n\n"
          "#### Scenario: Known name\n\n- **THEN** it says hello\n")
    path = proj / "src/greeter/__init__.py"
    path.write_text('"""Greeter.\n\nImplements: greeter/greet-by-name\n"""\n' + path.read_text())  # a hand edit of the copy
    out = edit(proj, "src/greeter/__init__.py")["hookSpecificOutput"]
    assert "Greeter SHALL greet by name." in out["additionalContext"]
    assert "NI-001" not in out["additionalContext"] and "from .aes/target.yaml" not in out["additionalContext"]


def test_a_planned_file_that_implements_no_requirement_keeps_the_plan_text(proj):
    write(proj / "openspec/specs/greeter/spec.md", "### Requirement: Greet by name\n\nGreeter SHALL greet by name.\n")
    out = edit(proj, "src/greeter/__init__.py")["hookSpecificOutput"]
    assert "NI-001" in out["additionalContext"] and "from .aes/target.yaml" in out["additionalContext"]


def test_a_repository_without_specs_still_gets_the_plan_text(proj):
    assert not (proj / "openspec").exists()
    out = edit(proj, "src/greeter/__init__.py")["hookSpecificOutput"]
    assert "NI-001" in out["additionalContext"] and "from .aes/target.yaml" in out["additionalContext"]
    shell = decide({"tool_name": "Bash", "tool_input": {"command": "cat src/greeter/__init__.py"}, "cwd": str(proj)})
    assert "NI-001" in shell["hookSpecificOutput"]["additionalContext"]

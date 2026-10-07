"""SC-HH-001: running pieces in the target; an undeclared running item inside a scope fails aes status.

Real Git repositories holding the frozen whygame5 records plus running scopes and pieces; snapshots are
written where `aes status` reads them, and the CLI's exit status and output are asserted.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from agentic_engineering_system.cli import main
from agentic_engineering_system.records import TargetValidationError, load_target, validate_target_refs
from agentic_engineering_system.running import check_running

FIXTURES = Path(__file__).parent / "fixtures"
WHYGAME5_AES = FIXTURES / "whygame5-54043e2" / ".aes"
FILES = ("src/whygame5/__init__.py", "src/whygame5/contracts.py", "src/whygame5/evaluator.py",
         "src/whygame5/graph.py", "tests/test_evaluator.py", "tests/test_replay.py")
RUNNING = """
running_scopes:
  - id: RS-WSL
    host: wsl
    kind: systemd_unit
    include: ["hive-*"]
    purpose: every hive unit on the laptop is declared
  - id: RS-AGENTS
    host: paperclip
    kind: agent
    include: ["*"]
    purpose: every agent on the board is declared
running_pieces:
  - id: RP-HIVE-CONTROLS
    host: wsl
    kind: systemd_unit
    name: hive-controls.service
    source: "aes:scripts/hive/systemd/hive-controls.service"
    purpose: the daily silence check
  - id: RP-COORDINATOR
    host: paperclip
    kind: agent
    name: Coordinator
    source: "aes:proposals/hive-hardening/agents/coordinator.AGENTS.md"
    purpose: plans and assigns jobs
"""


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", *args],
                   cwd=root, capture_output=True, text=True, check=True)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    (root / ".aes").mkdir(parents=True)
    shutil.copyfile(WHYGAME5_AES / "project.yaml", root / ".aes" / "project.yaml")
    (root / ".aes" / "target.yaml").write_text((WHYGAME5_AES / "target.yaml").read_text(encoding="utf-8") + RUNNING,
                                               encoding="utf-8")
    for rel in FILES:
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(f"# {rel}\n", encoding="utf-8")
    _git(root, "init", "-q")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "base")
    return root


def _snapshot(root: Path, items: list[tuple[str, str, str]], unreadable: list[tuple[str, str]] = ()) -> Path:
    path = root / ".aes" / "running-inventory.json"
    path.write_text(json.dumps({"collected_at": "2026-10-07T05:00:00+00:00",
                                "items": [{"host": h, "kind": k, "name": n} for h, k, n in items],
                                "unreadable": [{"host": h, "kind": k, "error": "ssh failed"} for h, k in unreadable]}))
    return path


DECLARED = [("wsl", "systemd_unit", "hive-controls.service"), ("paperclip", "agent", "Coordinator")]


def test_target_with_running_pieces_loads_and_validates(repo: Path) -> None:
    target = load_target(repo / ".aes" / "target.yaml")
    assert [p.id for p in target.running_pieces] == ["RP-HIVE-CONTROLS", "RP-COORDINATOR"]
    assert validate_target_refs(target) == []


def test_undeclared_item_in_scope_fails_check_and_status(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _snapshot(repo, DECLARED + [("wsl", "systemd_unit", "hive-mystery.timer"), ("wsl", "systemd_unit", "other.timer")])
    assert main(["running", "check", "--root", str(repo)]) == 1
    out = capsys.readouterr().err
    assert "FAIL running: 3 in scope, 1 undeclared" in out and "undeclared: wsl/systemd_unit/hive-mystery.timer" in out
    assert "other.timer" not in out  # outside every scope
    assert main(["status", "--root", str(repo)]) == 1
    status = capsys.readouterr().err
    assert "undeclared running: wsl/systemd_unit/hive-mystery.timer" in status
    assert "running: 3 in scope, 1 undeclared" in status


def test_all_declared_passes_and_absent_piece_is_reported(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _snapshot(repo, [("wsl", "systemd_unit", "hive-controls.service")])
    assert main(["running", "check", "--root", str(repo)]) == 0
    out = capsys.readouterr().out
    assert "OK running: 1 in scope, 0 undeclared, 1 declared but not running" in out
    assert "not running: paperclip/agent/Coordinator" in out


def test_without_a_snapshot_status_is_unchanged(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    main(["status", "--root", str(repo)])
    assert "running:" not in capsys.readouterr().out
    assert main(["running", "check", "--root", str(repo)]) == 2


def test_unreadable_source_is_never_clean(repo: Path) -> None:
    target = load_target(repo / ".aes" / "target.yaml")
    report = check_running(target, json.loads(_snapshot(repo, DECLARED[:1], unreadable=[("paperclip", "agent")]).read_text()))
    assert report.unreadable == ["paperclip/agent (RS-AGENTS)"]
    assert "paperclip/agent/Coordinator" not in report.not_running  # unknown, not absent


def test_bad_source_and_duplicate_are_refused(repo: Path) -> None:
    text = (repo / ".aes" / "target.yaml").read_text(encoding="utf-8")
    text += """  - id: RP-DUP
    host: wsl
    kind: systemd_unit
    name: hive-controls.service
    source: "no-colon-here"
    purpose: duplicate with a bad source
"""
    (repo / ".aes" / "target.yaml").write_text(text, encoding="utf-8")
    with pytest.raises(TargetValidationError) as exc:
        load_target(repo / ".aes" / "target.yaml")
    assert any("must be <repository>:<path>" in v for v in exc.value.violations)
    assert any("declares wsl/systemd_unit/hive-controls.service again" in v for v in exc.value.violations)

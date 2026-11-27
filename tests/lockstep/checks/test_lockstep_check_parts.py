"""Tests for `lockstep status --parts`: each part's mode and its last planning-gate result."""

import json
from pathlib import Path
import subprocess

import pytest

from lockstep.checks.cli import run_status

REQ = "lockstep-projection/status-lists-each-part-with-its-mode-and-last-gate-result"


def _repo(tmp_path: Path, yaml_text: str) -> Path:
    """A git repository with origin BrianMills2718/demo and the given lockstep.yaml."""
    root = tmp_path / "demo"
    root.mkdir()
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(root), "remote", "add", "origin", "git@github.com:BrianMills2718/demo.git"], check=True)
    (root / "lockstep.yaml").write_text(yaml_text)
    return root


def _record(folder: Path, day: str, **fields: str) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / f"{day}.jsonl").open("a") as fh:
        fh.write(json.dumps({"mode": "warn", "reason": None, "branch": "b", "log": "x", **fields}) + "\n")


def _rows(capsys: pytest.CaptureFixture[str], repo: Path) -> dict[str, dict[str, str]]:
    assert run_status(["--parts", "--json", "--repo", str(repo)]) == 0
    return {row["part"]: row for row in json.loads(capsys.readouterr().out)}


@pytest.mark.req("lockstep-projection/each-part-s-mode-comes-from-the-working-tree-s-settings")
def test_each_part_mode_comes_from_the_working_tree_settings(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("SHIP_LOG_DIR", str(tmp_path / "logs"))
    repo = _repo(tmp_path, "checks:\n  trace: warn\nplanning:\n  gate: block\n")
    rows = _rows(capsys, repo)
    assert rows["trace"]["mode"] == "warn"
    assert rows["mutation"]["mode"] == "off"
    assert rows["arch"]["mode"] == "block"
    assert rows["planning.gate"]["mode"] == "block"
    assert rows["planning.one_page_plans"]["mode"] == "warn"
    assert rows["guard.mode"]["mode"] == "warn (default)"
    assert rows["rules"]["mode"] == rows["feedback"]["mode"] == "per-repository control unavailable"
    assert "planning.validator" not in rows and "planning.skills" not in rows
    assert rows["planning.gate"]["last"] == "no record"


@pytest.mark.req("lockstep-projection/each-part-s-mode-comes-from-the-working-tree-s-settings")
def test_set_validator_skills_and_guard_are_listed(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("SHIP_LOG_DIR", str(tmp_path / "logs"))
    repo = _repo(tmp_path, "planning:\n  validator: {repo: /tmp/validator.git, ref: main}\n"
                           "  skills: {mode: warn, marketplace: Inside-Success/company-planning}\nguard:\n  mode: block\n")
    rows = _rows(capsys, repo)
    assert rows["planning.validator"]["mode"] == "{'repo': '/tmp/validator.git', 'ref': 'main'}"
    assert rows["planning.skills"]["mode"] == "warn"
    assert rows["guard.mode"]["mode"] == "block"


@pytest.mark.req("lockstep-projection/the-newest-planning-gate-record-for-this-repository-is-shown")
def test_the_newest_record_for_this_repository_is_shown(tmp_path, monkeypatch, capsys):
    logs = tmp_path / "logs"
    monkeypatch.setenv("SHIP_LOG_DIR", str(logs))
    folder = logs / "planning-verdicts"
    _record(folder, "2026-11-25", time="2026-11-25T10:00:00", repo="BrianMills2718/demo", gate="planning gate",
            outcome="refuse", head="a" * 40)
    _record(folder, "2026-11-26", time="2026-11-26T09:00:00", repo="BrianMills2718/demo", gate="planning gate",
            outcome="pass", head="b" * 40)
    _record(folder, "2026-11-26", time="2026-11-26T12:00:00", repo="BrianMills2718/other", gate="planning gate",
            outcome="warn", head="c" * 40)
    (folder / "2026-11-26.jsonl").open("a").write("not json\n")
    repo = _repo(tmp_path, "{}\n")
    rows = _rows(capsys, repo)
    assert rows["planning.gate"]["last"] == "pass 2026-11-26T09:00:00 bbbbbbbb"
    assert rows["planning.one_page_plans"]["last"] == "no record"
    assert rows["trace"]["last"] == "no record"
    assert run_status(["--parts", "--repo", str(repo)]) == 0
    text = capsys.readouterr().out
    assert "pass 2026-11-26T09:00:00 bbbbbbbb" in text and "default branch" in text


@pytest.mark.req("lockstep-projection/unreadable-settings-exit-2")
def test_unreadable_settings_exit_2(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("SHIP_LOG_DIR", str(tmp_path / "logs"))
    repo = _repo(tmp_path, "checks:\n  trace: loud\n")
    assert run_status(["--parts", "--repo", str(repo)]) == 2
    assert "trace" in capsys.readouterr().err


@pytest.mark.parametrize(("mode", "expected"), [("true", "block"), ("false", "off"), ('"off"', "off")])
def test_status_normalizes_guard_and_skills(tmp_path, capsys, mode, expected):
    config = f"guard: {{mode: {mode}}}\nplanning:\n  skills: {{mode: {mode}, marketplace: example/planning}}\n"
    rows = _rows(capsys, _repo(tmp_path, config))
    assert rows["guard.mode"]["mode"] == rows["planning.skills"]["mode"] == expected


@pytest.mark.req("lockstep-projection/unreadable-settings-exit-2")
def test_settings_with_invalid_encoding_exit_2(tmp_path, capsys):
    repo = _repo(tmp_path, "{}\n")
    (repo / "lockstep.yaml").write_bytes(b"\xff")
    assert run_status(["--parts", "--repo", str(repo)]) == 2
    assert "lockstep.yaml cannot be read" in capsys.readouterr().err

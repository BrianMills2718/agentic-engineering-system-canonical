"""SC-AP-002: `aes plan validate/accept` require a fresh Company Planning adoption when asked.

Real Git repositories holding the frozen whygame5 records; each case runs the CLI and checks the
exit status, the reason, and whether the target and the plan file were written.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import pytest
from ruamel.yaml import YAML

from agentic_engineering_system.cli import main

FIXTURES = Path(__file__).parent / "fixtures"
WHYGAME5_AES = FIXTURES / "whygame5-54043e2" / ".aes"
RUNNER_PROPOSAL = FIXTURES / "whygame5-proposal-runner.yaml"
FILES = {
    "src/whygame5/__init__.py": '"""pkg"""\n',
    "src/whygame5/contracts.py": "class Proposal:\n    pass\n",
    "src/whygame5/graph.py": "def normalize(s):\n    return s\n",
    "src/whygame5/evaluator.py": "def select(findings):\n    return findings[:1]\n",
    "src/whygame5/prompts.py": "PROMPT = 'why?'\n",
    "tests/test_prompts.py": "def test_ok():\n    assert True\n",
    "tests/test_evaluator.py": "def test_ok():\n    assert True\n",
    "tests/test_replay.py": "def test_ok():\n    assert True\n",
    "pyproject.toml": "[project]\nname = 'whygame5'\n",
}
PLAN = "proposals/runner/README.md"


def _git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", *args],
                          cwd=root, capture_output=True, text=True, check=True).stdout.strip()


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _adopt(root: Path) -> None:
    """A plan and a Company Planning-shaped adoption decision bound to its current bytes."""
    _write(root, PLAN, "---\nplan_id: runner\nmethod_conformance_receipt: proposals/runner/receipt.json\n---\n\n# Runner\n")
    _write(root, "proposals/runner/receipt.json", json.dumps({"verdict": "pass"}) + "\n")
    sha = lambda rel: hashlib.sha256((root / rel).read_bytes()).hexdigest()  # noqa: E731
    _write(root, "proposals/runner/receipt.adoption-decision.json", json.dumps(
        {"decision": "adopted", "plan_sha256": sha(PLAN), "receipt_sha256": sha("proposals/runner/receipt.json")}) + "\n")


def _repo(tmp_path: Path, require: bool | None) -> Path:
    repo = tmp_path / "repo"
    (repo / ".aes").mkdir(parents=True)
    shutil.copyfile(WHYGAME5_AES / "project.yaml", repo / ".aes" / "project.yaml")
    shutil.copyfile(WHYGAME5_AES / "target.yaml", repo / ".aes" / "target.yaml")
    for rel, text in FILES.items():
        _write(repo, rel, text)
    if require is not None:
        _write(repo, ".aes/planning.yaml", f"require_adopted_plan: {str(require).lower()}\n")
    _adopt(repo)
    _git(repo, "init", "-q")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")
    return repo


def _proposal(repo: Path, adopted_plan_ref: str | None) -> Path:
    data = YAML(typ="safe").load(RUNNER_PROPOSAL.read_text(encoding="utf-8"))
    if adopted_plan_ref is not None:
        data["adopted_plan_ref"] = adopted_plan_ref
    path = repo / "proposal.yaml"  # untracked outside .aes/: not dirty
    yaml = YAML()
    with path.open("w", encoding="utf-8") as fh:
        yaml.dump(data, fh)
    return path


def _accept(repo: Path, proposal: Path, capsys: pytest.CaptureFixture[str]) -> tuple[int, str, bool]:
    target_before = (repo / ".aes" / "target.yaml").read_bytes()
    status = main(["plan", "accept", str(proposal), "--root", str(repo)])
    err = capsys.readouterr().err
    written = (repo / ".aes" / "target.yaml").read_bytes() != target_before
    assert written == (repo / ".aes" / "plans" / "PLAN-WG5-RUNNER.yaml").exists()
    return status, err, written


def test_required_and_missing_is_refused(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    repo = _repo(tmp_path, require=True)
    status, err, written = _accept(repo, _proposal(repo, None), capsys)
    assert (status, written) == (1, False)
    assert "adopted_plan_ref is missing: .aes/planning.yaml requires every proposal" in err


def test_required_and_plan_not_found_is_refused(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    repo = _repo(tmp_path, require=True)
    status, err, written = _accept(repo, _proposal(repo, "proposals/nosuch/README.md"), capsys)
    assert (status, written) == (1, False)
    assert "adopted_plan_ref proposals/nosuch/README.md:" in err and "plan file not found" in err


def test_required_and_plan_changed_after_adoption_is_refused(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    repo = _repo(tmp_path, require=True)
    _write(repo, PLAN, (repo / PLAN).read_text(encoding="utf-8") + "\nEdited after adoption.\n")
    _git(repo, "commit", "-q", "-am", "edit plan")
    status, err, written = _accept(repo, _proposal(repo, PLAN), capsys)
    assert (status, written) == (1, False)
    assert "plan changed since adoption; re-adopt it" in err


def test_required_and_freshly_adopted_is_accepted(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    repo = _repo(tmp_path, require=True)
    status, err, written = _accept(repo, _proposal(repo, PLAN), capsys)
    assert (status, written) == (0, True), err
    plan = YAML(typ="safe").load((repo / ".aes" / "plans" / "PLAN-WG5-RUNNER.yaml").read_text(encoding="utf-8"))
    assert plan["adopted_plan_ref"] == PLAN


@pytest.mark.parametrize("require", [None, False])
def test_not_required_behaves_as_before(tmp_path: Path, capsys: pytest.CaptureFixture[str], require: bool | None) -> None:
    repo = _repo(tmp_path, require=require)
    status, err, written = _accept(repo, _proposal(repo, None), capsys)
    assert (status, written) == (0, True), err


def test_a_named_plan_is_checked_even_when_not_required(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    repo = _repo(tmp_path, require=None)
    status = main(["plan", "validate", str(_proposal(repo, "proposals/nosuch/README.md")), "--root", str(repo)])
    assert status == 1
    assert "plan file not found" in capsys.readouterr().err

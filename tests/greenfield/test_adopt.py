"""SC-ADOPT-001: adopting an existing repository, through the real CLI and the installed hooks.

The repository adopted is a clone of this one (real history, real files), with its
`.aes/` removed so it looks like any existing codebase. The clone also drops AES's
own `src/agentic_engineering_system/cli.py`: the installed hook runs a repository's
own `src/` when it finds that file (so AES checks itself with its working copy),
and here the hooks must run the AES under test instead. Every verdict comes from
`git commit` running the hooks git actually runs. Baseline membership is asserted
as set equality with Git's own listing, never as a count.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from agentic_engineering_system.adopt import BASELINE_PATH, AdoptError, adopt, load_baseline
from agentic_engineering_system.cli import main

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "src"
ROOTS = ("src/", "tests/")
LEGACY_FILE = "tests/repository_context/test_models.py"


def _env(tmp: Path) -> dict[str, str]:
    # no machine-wide commit-rule config: each test sets the repository's own mode
    return {**os.environ, "PYTHONPATH": str(SRC), "AES_COMMIT_RULE_MACHINE_CONFIG": str(tmp / "none.yaml")}


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", *args],
                          cwd=root, capture_output=True, text=True, check=False, env=_env(root.parent))


def _aes(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    done = subprocess.run([sys.executable, "-m", "agentic_engineering_system.cli", *args, "--root", str(root)],
                          cwd=root, capture_output=True, text=True, check=False, env=_env(root.parent))
    print(f"$ aes {' '.join(args)}  (exit {done.returncode})\n{done.stdout}{done.stderr}")
    return done


def _commit(root: Path, message: str) -> subprocess.CompletedProcess[str]:
    done = _git(root, "commit", "-m", message)
    print(f"$ git commit -m {message.splitlines()[0]!r}  (exit {done.returncode})\n{done.stdout}{done.stderr}")
    return done


def _head(root: Path) -> str:
    return _git(root, "rev-parse", "HEAD").stdout.strip()


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _adopted_plan(root: Path, plan_id: str = "demo") -> None:
    """A Company Planning-shaped plan whose adoption decision is bound to its bytes."""
    plan = root / "proposals" / plan_id / "README.md"
    _write(root, f"proposals/{plan_id}/README.md",
           f"---\nplan_id: {plan_id}\nmethod_conformance_receipt: proposals/{plan_id}/receipt.json\n---\n\n# Demo\n")
    _write(root, f"proposals/{plan_id}/receipt.json", json.dumps({"verdict": "pass"}) + "\n")
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()  # noqa: E731
    _write(root, f"proposals/{plan_id}/receipt.adoption-decision.json", json.dumps({
        "decision": "adopted", "plan_ref": f"proposals/{plan_id}/README.md",
        "plan_sha256": digest(plan), "receipt_sha256": digest(root / f"proposals/{plan_id}/receipt.json")}) + "\n")


def _log_lines(root: Path) -> list[dict]:
    common = Path(_git(root, "rev-parse", "--git-common-dir").stdout.strip())
    log_dir = (common if common.is_absolute() else root / common) / "aes"
    return [json.loads(line) for f in sorted(log_dir.glob("commit-rule-*.jsonl"))
            for line in f.read_text(encoding="utf-8").splitlines()]


@pytest.fixture
def existing(tmp_path: Path) -> Path:
    """A clone of this repository with no .aes/: an existing codebase AES has never seen."""
    root = tmp_path / "existing"
    assert subprocess.run(["git", "clone", "-q", "--local", "--no-hardlinks", str(REPO), str(root)],
                          capture_output=True, text=True, check=False).returncode == 0
    assert _git(root, "rm", "-rq", ".aes", "src/agentic_engineering_system/cli.py").returncode == 0
    assert _git(root, "-c", "core.hooksPath=/dev/null", "commit", "-qm", "an existing codebase").returncode == 0
    return root


@pytest.fixture
def adopted(existing: Path) -> Path:
    """`existing` adopted, hooks installed after the adoption commit (the documented order)."""
    assert _aes(existing, "adopt", "--project-id", "existing", "--actor", "a maintainer",
                "--outcome", "The code keeps working while it is brought under AES.").returncode == 0
    _git(existing, "add", ".aes")
    # before `aes hooks install` no AES hook exists; keep the machine's global hooks out of the fixture
    assert _git(existing, "-c", "core.hooksPath=/dev/null", "commit", "-qm", "Adopt AES").returncode == 0
    assert _aes(existing, "hooks", "install").returncode == 0
    _adopted_plan(existing)
    _git(existing, "add", "-A")
    assert _commit(existing, "[Shaping demo] hooks and demo plan\n\nEmergency: bootstrap").returncode == 0
    return existing


def test_adopt_real_repository_lists_every_tracked_file(existing: Path) -> None:
    head = _head(existing)
    dry = _aes(existing, "adopt", "--dry-run", "--project-id", "existing", "--actor", "a maintainer",
               "--outcome", "The code keeps working while it is brought under AES.")
    assert dry.returncode == 0 and "would adopt (dry run, nothing written)" in dry.stdout
    assert not (existing / ".aes").exists()

    done = _aes(existing, "adopt", "--project-id", "existing", "--actor", "a maintainer",
                "--outcome", "The code keeps working while it is brought under AES.")
    assert done.returncode == 0
    baseline = load_baseline(existing)
    assert baseline is not None and baseline.adopted_at_revision == head

    tracked = set(_git(existing, "ls-files", "--", *ROOTS).stdout.split())
    listed = set(baseline.files)
    assert listed == tracked, (f"missing: {sorted(tracked - listed)[:1]}, extra: {sorted(listed - tracked)[:1]}")
    blobs = {}
    for line in _git(existing, "ls-tree", "-r", head, "--", *ROOTS).stdout.splitlines():
        meta, path = line.split("\t", 1)
        blobs[path] = meta.split()[2]
    assert baseline.files == blobs
    assert LEGACY_FILE in baseline.files and "README.md" not in baseline.files  # outside the roots

    status = _aes(existing, "status")
    assert status.returncode == 0
    assert f"legacy: {len(tracked)} of {len(tracked)} governed file(s) still in the baseline (100.0%)" in status.stdout

    again = _aes(existing, "adopt")
    assert again.returncode == 1 and "already exists; a repository is adopted once" in again.stderr


def test_adoption_commit_passes_installed_hooks(existing: Path) -> None:
    """Issue #155: with hooks installed before the first commit, the adoption commit is not refused."""
    assert _aes(existing, "adopt", "--project-id", "existing", "--actor", "a maintainer",
                "--outcome", "The code keeps working while it is brought under AES.").returncode == 0
    assert _aes(existing, "hooks", "install").returncode == 0
    _write(existing, ".aes/commit_rule.yaml", "mode: enforce\n")
    _git(existing, "add", "-A")
    before = _head(existing)
    done = _commit(existing, "[Unplanned] Adopt AES\n\nEmergency: first commit of the adoption")
    assert done.returncode == 0, done.stderr
    assert _head(existing) != before
    legacy = len(load_baseline(existing).files)  # type: ignore[union-attr]
    assert f"0 orphan(s), 0 planned but not yet realized, {legacy} legacy" in done.stderr + done.stdout


def test_unplanned_legacy_edit_observe_logs_enforce_refuses(adopted: Path) -> None:
    _write(adopted, LEGACY_FILE, (adopted / LEGACY_FILE).read_text(encoding="utf-8") + "# touched\n")
    _git(adopted, "add", LEGACY_FILE)

    _write(adopted, ".aes/commit_rule.yaml", "mode: enforce\n")  # untracked config is read from disk
    before = _head(adopted)
    refused = _commit(adopted, "[Goal demo] edit a legacy file")
    assert refused.returncode == 1
    assert f"unplanned legacy edit: {LEGACY_FILE}" in refused.stderr
    assert _head(adopted) == before

    _write(adopted, ".aes/commit_rule.yaml", "mode: observe\n")
    landed = _commit(adopted, "[Goal demo] edit a legacy file")
    assert landed.returncode == 0 and _head(adopted) != before
    line = _log_lines(adopted)[-1]
    print(json.dumps(line))
    assert line["mode"] == "observe" and line["verdict"] == "refuse" and line["check"] == "legacy-edit"
    assert any(f"unplanned legacy edit: {LEGACY_FILE}" in r for r in line["reasons"])

    status = _aes(adopted, "status")
    assert "1 changed since adoption" in status.stdout and f"changed legacy: {LEGACY_FILE}" in status.stdout


def test_plan_accept_removes_exactly_the_planned_file(adopted: Path, tmp_path: Path) -> None:
    before = set(load_baseline(adopted).files)  # type: ignore[union-attr]
    proposal = tmp_path / "plan.yaml"
    proposal.write_text(f"""schema_version: aes.v0_2.proposal.probe0
proposal_id: PLAN-TOUCH-MODELS
title: Plan the one legacy file the next change edits
rationale: The next change edits {LEGACY_FILE}, so it leaves the baseline and becomes planned.
closes_gaps: []
adopted_plan_ref: proposals/demo/README.md
trace_review:
  runs_traced_work: false
  reason: a test file edit; nothing runs a model, agent or pipeline
target_delta:
  add:
    planned_artifacts:
      - id: ART-TEST-MODELS
        locator:
          exact_path: {LEGACY_FILE}
        kind: test
        purpose: repository-context model tests, now planned
        semantic_justification_refs:
          - OUT-001
""", encoding="utf-8")
    accepted = _aes(adopted, "plan", "accept", str(proposal))
    assert accepted.returncode == 0
    assert f"baseline: removed 1 now planned or untracked from {BASELINE_PATH}" in accepted.stdout
    after = set(load_baseline(adopted).files)  # type: ignore[union-attr]
    assert before - after == {LEGACY_FILE} and after <= before

    _write(adopted, ".aes/commit_rule.yaml", "mode: enforce\n")
    _git(adopted, "add", ".aes/target.yaml", ".aes/plans", str(BASELINE_PATH))
    assert _commit(adopted, "[Goal demo] plan the models test").returncode == 0
    _write(adopted, LEGACY_FILE, (adopted / LEGACY_FILE).read_text(encoding="utf-8") + "# planned edit\n")
    _git(adopted, "add", LEGACY_FILE)
    before_head = _head(adopted)
    done = _commit(adopted, "[Goal demo] edit the planned models test")
    assert done.returncode == 0, done.stderr
    assert _head(adopted) != before_head and "legacy edit" not in done.stderr


def test_new_unplanned_file_is_still_an_orphan(adopted: Path) -> None:
    _write(adopted, ".aes/commit_rule.yaml", "mode: enforce\n")
    _write(adopted, "tests/test_brand_new.py", "def test_new() -> None:\n    assert True\n")
    _git(adopted, "add", "tests/test_brand_new.py")
    before = _head(adopted)
    done = _commit(adopted, "[Goal demo] add a new test")
    assert done.returncode == 1
    assert "orphan: tests/test_brand_new.py" in done.stderr
    assert f"orphan: {LEGACY_FILE}" not in done.stderr and "1 orphan(s)" in done.stderr
    assert _head(adopted) == before


def test_deleting_a_legacy_file_needs_no_plan_and_prunes_on_accept(adopted: Path) -> None:
    _write(adopted, ".aes/commit_rule.yaml", "mode: enforce\n")
    _git(adopted, "rm", "-q", LEGACY_FILE)
    assert _commit(adopted, "[Goal demo] retire a legacy test").returncode == 0
    status = _aes(adopted, "status")
    total = len(_git(adopted, "ls-files", "--", *ROOTS).stdout.split())
    assert f"legacy: {total} of {total} governed file(s)" in status.stdout


def test_refusals_and_malformed_baseline(existing: Path, tmp_path: Path) -> None:
    with pytest.raises(AdoptError, match="needs --project-id, --actor, --outcome"):
        adopt(existing)
    with pytest.raises(AdoptError, match="nothing to adopt"):
        adopt(existing, project_id="x", actor="a", outcome="o", governed_roots=["no-such-dir/"])
    adopt(existing, project_id="x", actor="a", outcome="o")
    (existing / BASELINE_PATH).write_text('{"schema_version": "other"}\n', encoding="utf-8")
    with pytest.raises(AdoptError, match="schema_version must be"):
        load_baseline(existing)


def test_init_warns_on_an_existing_codebase(existing: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["init", "--root", str(existing), "--project-id", "x", "--actor", "a", "--outcome", "o"]) == 0
    err = capsys.readouterr().err
    tracked = len(_git(existing, "ls-files", "--", *ROOTS).stdout.split())
    assert f"the governed roots already hold {tracked} tracked file(s)" in err and "aes adopt" in err

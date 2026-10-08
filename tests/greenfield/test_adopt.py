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


# --- Issue #218: a Company Planning plan's declared scope admits legacy edits -------------

OUTSIDE_FILE = "tests/repository_context/test_resolver.py"


def _numbered_plan(root: Path, number: int, surfaces: list[dict] | None, *, adopt_it: bool = True) -> Path:
    """`docs/plans/<N>_scoped.md`, Company Planning-shaped, with `conflict_surfaces` in its front
    matter (the work-unit schema 1.1 conflictSurface shape) and, when `adopt_it`, an adoption
    decision bound to its bytes."""
    stem = f"docs/plans/{number}_scoped"
    front = f"---\nplan_id: existing#{number}\nmethod_conformance_receipt: {stem}.receipt.json\n"
    if surfaces is not None:
        front += "conflict_surfaces:\n" + "".join(
            "  - " + json.dumps(s) + "\n" for s in surfaces)
    _write(root, f"{stem}.md", front + f"---\n\n# Plan #{number}\n")
    _write(root, f"{stem}.receipt.json", json.dumps({"verdict": "pass"}) + "\n")
    if adopt_it:
        digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()  # noqa: E731
        _write(root, f"{stem}.adoption-decision.json", json.dumps({
            "decision": "adopted", "plan_ref": f"{stem}.md", "plan_sha256": digest(root / f"{stem}.md"),
            "receipt_sha256": digest(root / f"{stem}.receipt.json")}) + "\n")
    return root / f"{stem}.md"


def _scope(target: str, access: str = "write", repository: str = "existing") -> dict:
    return {"kind": "repository_path", "repository": repository, "target": target, "access": access}


def _touch(root: Path, rel: str, note: str) -> None:
    _write(root, rel, (root / rel).read_text(encoding="utf-8") + f"# {note}\n")
    _git(root, "add", rel)


def test_plan_scope_admits_a_legacy_edit_inside_it_and_releases_the_file(adopted: Path) -> None:
    """#218 test 1: under enforce, a [Plan #N] commit editing a legacy file inside its adopted
    plan's conflict_surfaces lands, and the file then leaves the unplanned-legacy set."""
    from agentic_engineering_system.adopt import legacy_paths, unplanned_legacy

    _numbered_plan(adopted, 7, [_scope("tests/repository_context/test_models.py"),
                                _scope("tests/repository_context/**", access="read")])
    _git(adopted, "add", "docs/plans")
    _git(adopted, "-c", "core.hooksPath=/dev/null", "commit", "-qm", "add plan 7")
    assert LEGACY_FILE in unplanned_legacy(adopted)

    _write(adopted, ".aes/commit_rule.yaml", "mode: enforce\n")
    _touch(adopted, LEGACY_FILE, "edited under plan 7")
    before = _head(adopted)
    done = _commit(adopted, "[Plan #7] edit a legacy file inside the plan's scope")
    assert done.returncode == 0, done.stderr
    assert _head(adopted) != before
    line = _log_lines(adopted)[-1]
    print(json.dumps(line))
    assert line["mode"] == "enforce" and line["verdict"] == "accept" and line["tag"] == "Plan #7"
    assert line["scope"] == ["tests/repository_context/test_models.py"]  # the read surface grants nothing
    assert any(f"inside Plan #7's declared conflict_surfaces: {LEGACY_FILE}" in r for r in line["reasons"])

    # It left the unplanned-legacy set (still listed in the JSON, so topology knows it).
    assert LEGACY_FILE not in unplanned_legacy(adopted) and LEGACY_FILE in legacy_paths(adopted)
    assert unplanned_legacy(adopted) == legacy_paths(adopted) - {LEGACY_FILE}
    status = _aes(adopted, "status")
    assert "1 released by an adopted plan's conflict_surfaces" in status.stdout
    topology = _aes(adopted, "topology", "check")
    assert topology.returncode == 0 and f"orphan: {LEGACY_FILE}" not in topology.stdout

    # Released: a later small edit no longer needs plan 7's scope.
    _touch(adopted, LEGACY_FILE, "a trivial follow-up")
    assert _commit(adopted, "[Trivial] follow-up comment").returncode == 0


def test_plan_scope_refuses_a_legacy_edit_outside_it(adopted: Path) -> None:
    """#218 test 2: the same adopted plan editing a legacy file outside its scope is refused,
    naming only the file outside, and a mixed commit is refused as a whole."""
    _numbered_plan(adopted, 7, [_scope("tests/repository_context/test_models.py"),
                                _scope(OUTSIDE_FILE, repository="someone/else")])
    _git(adopted, "add", "docs/plans")
    _git(adopted, "-c", "core.hooksPath=/dev/null", "commit", "-qm", "add plan 7")
    _write(adopted, ".aes/commit_rule.yaml", "mode: enforce\n")

    _touch(adopted, OUTSIDE_FILE, "outside plan 7")
    _touch(adopted, LEGACY_FILE, "inside plan 7")
    before = _head(adopted)
    refused = _commit(adopted, "[Plan #7] edit inside and outside the plan's scope")
    assert refused.returncode == 1 and _head(adopted) == before
    assert f"unplanned legacy edit: {OUTSIDE_FILE} still in" in refused.stderr
    assert f"unplanned legacy edit: {LEGACY_FILE}" not in refused.stderr
    assert "declare it in Plan #7's front matter conflict_surfaces" in refused.stderr
    line = _log_lines(adopted)[-1]
    print(json.dumps(line))
    assert line["verdict"] == "refuse" and line["check"] == "legacy-edit"


def test_unadopted_or_widened_plan_scope_admits_nothing(adopted: Path) -> None:
    """#218 test 3: a plan that is not adopted is refused even though its front matter names the
    file; a plan whose scope was widened after adoption is refused until re-adopted."""
    _numbered_plan(adopted, 8, [_scope("tests/repository_context")], adopt_it=False)
    plan9 = _numbered_plan(adopted, 9, [_scope("tests/repository_context/test_models.py")])
    plan9.write_text(plan9.read_text(encoding="utf-8").replace(
        "---\n\n# Plan", "  - " + json.dumps(_scope("tests/**")) + "\n---\n\n# Plan", 1), encoding="utf-8")
    _git(adopted, "add", "docs/plans")
    _git(adopted, "-c", "core.hooksPath=/dev/null", "commit", "-qm", "add plans 8 and 9")
    _write(adopted, ".aes/commit_rule.yaml", "mode: enforce\n")
    _touch(adopted, OUTSIDE_FILE, "edit")
    before = _head(adopted)

    unadopted = _commit(adopted, "[Plan #8] edit under a plan nobody adopted")
    assert unadopted.returncode == 1 and _head(adopted) == before
    assert "no method_conformance_receipt" in unadopted.stderr or "receipt or adoption decision missing" in unadopted.stderr
    assert f"unplanned legacy edit: {OUTSIDE_FILE}" in unadopted.stderr

    widened = _commit(adopted, "[Plan #9] edit under a scope widened after adoption")
    assert widened.returncode == 1 and _head(adopted) == before
    assert "plan changed since adoption" in widened.stderr

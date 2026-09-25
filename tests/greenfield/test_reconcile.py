"""`aes reconcile` / `aes status`: qualified current state and derived gaps
(RU-AES-RECONCILE; SC-GF-007 and SC-GF-008 at the gap level; SC-GF-004 "no route").

The repository under test is a temp Git repo holding the frozen whygame5
records plus stand-in files for every planned artifact except RUNNER, REPORT
and CLI, which mirrors the live consumer's unrealized set.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from agentic_engineering_system.cli import main
from agentic_engineering_system.reconcile import reconcile, render_report, render_status

WHYGAME5_AES = Path(__file__).parent / "fixtures" / "whygame5-54043e2" / ".aes"
EVALUATOR = "src/whygame5/evaluator.py"

FILES = {
    "src/whygame5/__init__.py": '"""pkg"""\n',
    "src/whygame5/contracts.py": "class Proposal:\n    pass\n",
    "src/whygame5/graph.py": "def normalize(s):\n    return s\n",
    EVALUATOR: "from whygame5 import graph\n\ndef select(findings):\n    return findings[:1]\n",
    "src/whygame5/prompts.py": "PROMPT = 'why?'\n",
    "tests/test_prompts.py": "def test_ok():\n    assert True\n",
    "tests/test_evaluator.py": "def test_ok():\n    assert True\n",
    "tests/test_replay.py": "def test_ok():\n    assert True\n",
    "pyproject.toml": "[project]\nname = 'whygame5'\n",
}


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", *args],
        cwd=root, capture_output=True, text=True, check=True,
    )
    return proc.stdout.strip()


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _commit(root: Path, message: str) -> str:
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", message)
    return _git(root, "rev-parse", "HEAD")


@pytest.fixture
def root(tmp_path: Path) -> Path:
    (tmp_path / ".aes").mkdir()
    shutil.copy(WHYGAME5_AES / "project.yaml", tmp_path / ".aes" / "project.yaml")
    shutil.copy(WHYGAME5_AES / "target.yaml", tmp_path / ".aes" / "target.yaml")
    for rel, text in FILES.items():
        _write(tmp_path, rel, text)
    _git(tmp_path, "init", "-q")
    _commit(tmp_path, "base")
    return tmp_path


def _observe(root: Path, oid: str, er: str, assessment: str, deps: list[str]) -> None:
    rev = _git(root, "rev-parse", "HEAD")
    deps_yaml = "".join(f"\n  - {d}" for d in deps)
    _write(root, f".aes/observations/{oid}.yaml", f"""schema_version: aes.v0_2.observation.probe0
observation_id: {oid}
subject_refs: [SC-WG5-002]
subject_revision: {rev}
dependency_paths:{deps_yaml}
observer: {{identity: test}}
method: fixture
execution_state: COMPLETED
result: {{note: fixture}}
produced_at: 2026-09-25T00:00:00+00:00
assessments:
  - evidence_requirement_ref: {er}
    assessment: {assessment}
    basis: fixture
    assessor: {{identity: test}}
""")


def _statuses(r) -> dict[str, str]:
    return {a.artifact_id: a.status for a in r.artifacts}


def _standing(r) -> dict[str, str]:
    return {c.criterion_id: c.standing for c in r.criteria}


def _gaps(r, component: str) -> list[tuple[str, str]]:
    comp = next(c for c in r.components if c.component_id == component)
    return [(g.kind, g.ref) for g in comp.gaps]


# --------------------------------------------------------------------------- #
# Baseline
# --------------------------------------------------------------------------- #


def test_baseline_statuses(root: Path) -> None:
    r = reconcile(root)
    assert r.schema_version == "aes.v0_2.reconciliation.probe0"
    assert r.subject_revision == _git(root, "rev-parse", "HEAD")
    assert r.dirty is False
    assert r.producer.identity == "aes"

    unrealized = {a for a, s in _statuses(r).items() if s == "UNREALIZED"}
    assert unrealized == {"ART-WG5-RUNNER", "ART-WG5-REPORT", "ART-WG5-CLI"}
    assert "DRIFTED" not in _statuses(r).values()
    pyproject = next(a for a in r.artifacts if a.artifact_id == "ART-WG5-PYPROJECT")
    assert (pyproject.status, pyproject.note is not None) == ("REALIZED", True)  # outside governed roots

    assert set(_standing(r).values()) == {"INSUFFICIENT"}  # no observations yet
    assert r.orphans == [] and r.ok

    # RUNNER: its artifacts first, then SC-WG5-003 through the shared NI-WG5-003.
    assert _gaps(r, "CMP-WG5-RUNNER") == [
        ("unrealized", "ART-WG5-RUNNER"), ("unrealized", "ART-WG5-CLI"), ("insufficient", "SC-WG5-003"),
    ]
    assert _gaps(r, "CMP-WG5-REPORT") == [("unrealized", "ART-WG5-REPORT"), ("insufficient", "SC-WG5-005")]
    # CONTRACTS: target_refs [NI-WG5-005], shared by SC-WG5-004.
    assert _gaps(r, "CMP-WG5-CONTRACTS") == [("insufficient", "SC-WG5-004")]
    assert r.unassigned_gaps == []


def test_status_screen_and_exit_zero_when_only_insufficient(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["status", "--root", str(root)]) == 0
    out = capsys.readouterr().out
    assert out.startswith(f"OK status: whygame5-target at {_git(root, 'rev-parse', 'HEAD')}\n")
    assert "  artifacts: 9 realized, 3 unrealized, 0 drifted; 0 orphan(s)\n" in out
    assert "  criteria: 0 supported, 5 insufficient, 0 refuted;" in out
    assert "    CMP-WG5-RUNNER: unrealized ART-WG5-RUNNER - src/whygame5/runner.py: planned, no file at HEAD (+2 more)\n" in out
    assert "INSUFFICIENT criteria are normal while work is in progress and do not fail this command" in out


# --------------------------------------------------------------------------- #
# SC-GF-008 at the gap level: a dependency change re-opens a closed gap
# --------------------------------------------------------------------------- #


def test_dependency_change_reopens_a_supported_criterions_gap(root: Path) -> None:
    _observe(root, "OBS-EVAL", "ER-WG5-002-01", "SUPPORTS", [EVALUATOR, "tests/test_evaluator.py"])
    _commit(root, "record evidence at N")

    at_n = reconcile(root)
    assert _standing(at_n)["SC-WG5-002"] == "SUPPORTED"
    assert ("insufficient", "SC-WG5-002") not in _gaps(at_n, "CMP-WG5-EVALUATOR")
    assert [(o.observation_id, o.freshness) for o in at_n.observations] == [("OBS-EVAL", "CURRENT")]

    _write(root, EVALUATOR, FILES[EVALUATOR] + "\ndef select_all(findings):\n    return findings\n")
    _commit(root, "change the evaluator at N+1")

    at_n1 = reconcile(root)
    assert _standing(at_n1)["SC-WG5-002"] == "INSUFFICIENT"
    obs = at_n1.observations[0]
    assert (obs.freshness, obs.detail) == ("STALE", f"changed since observed: {EVALUATOR}")
    missing = next(c for c in at_n1.criteria if c.criterion_id == "SC-WG5-002").missing
    assert [(m.er_id, m.status, m.has_route) for m in missing] == [("ER-WG5-002-01", "NO_CURRENT_SUPPORT", True)]
    assert "OBS-EVAL SUPPORTS (STALE)" in missing[0].detail
    assert ("insufficient", "SC-WG5-002") in _gaps(at_n1, "CMP-WG5-EVALUATOR")
    assert at_n1.ok  # stale support is a gap, not a failure


def test_requirement_without_verification_subject_is_reported_as_no_route(root: Path) -> None:
    path = root / ".aes" / "target.yaml"
    text = path.read_text(encoding="utf-8")
    head, tail = text.split("  - id: VS-WG5-BRIAN-REPORT\n", 1)
    assert "  - id: " not in tail  # it is the last subject; drop it
    path.write_text(head, encoding="utf-8")
    _commit(root, "drop the only route to ER-WG5-005-01")

    r = reconcile(root)
    missing = next(c for c in r.criteria if c.criterion_id == "SC-WG5-005").missing
    assert [(m.er_id, m.has_route, m.verification_subject_refs) for m in missing] == [("ER-WG5-005-01", False, [])]
    gap = next(g for g in next(c for c in r.components if c.component_id == "CMP-WG5-REPORT").gaps
               if g.ref == "SC-WG5-005")
    assert gap.detail == "ER-WG5-005-01 NO_CURRENT_SUPPORT (no route)"
    assert "1 unsupported evidence requirement(s) with no route" in render_status(r)
    assert "ER-WG5-005-01: NO_CURRENT_SUPPORT - no observation assesses it; route: NO ROUTE" in render_report(r)
    assert r.ok  # a missing route is a planning gap, not a failure


def test_requirement_with_external_boundary_is_routed(root: Path) -> None:
    """An external boundary is a route, as `aes target validate` already accepts (SC-GF-004)."""
    path = root / ".aes" / "target.yaml"
    head, _ = path.read_text(encoding="utf-8").split("  - id: VS-WG5-BRIAN-REPORT\n", 1)
    path.write_text(head + "external_boundaries:\n  - evidence_requirement_ref: ER-WG5-005-01\n"
                    "    boundary: Brian reviews the report outside the repository\n", encoding="utf-8")
    _commit(root, "route ER-WG5-005-01 through an external boundary instead of a subject")

    r = reconcile(root)
    missing = next(c for c in r.criteria if c.criterion_id == "SC-WG5-005").missing
    assert [(m.er_id, m.has_route, m.verification_subject_refs, m.external_boundary) for m in missing] == [
        ("ER-WG5-005-01", True, [], "Brian reviews the report outside the repository")]
    gap = next(g for g in next(c for c in r.components if c.component_id == "CMP-WG5-REPORT").gaps
               if g.ref == "SC-WG5-005")
    assert gap.detail == "ER-WG5-005-01 NO_CURRENT_SUPPORT"
    assert "0 unsupported evidence requirement(s) with no route" in render_status(r)
    assert ("ER-WG5-005-01: NO_CURRENT_SUPPORT - no observation assesses it; "
            "route: external boundary (Brian reviews the report outside the repository)") in render_report(r)


# --------------------------------------------------------------------------- #
# Exit codes
# --------------------------------------------------------------------------- #


def test_refuted_criterion_fails_both_commands(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _observe(root, "OBS-EVAL", "ER-WG5-002-01", "REFUTES", [EVALUATOR])
    r = reconcile(root)
    assert _standing(r)["SC-WG5-002"] == "REFUTED" and r.failures == ["refuted: SC-WG5-002"]
    assert _gaps(r, "CMP-WG5-EVALUATOR")[0] == ("refuted", "SC-WG5-002")
    assert main(["status", "--root", str(root)]) == 1
    assert main(["reconcile", "--root", str(root)]) == 1
    err = capsys.readouterr().err
    assert err.startswith("FAIL status:") and "  refuted: SC-WG5-002\n" in err


def test_orphan_fails_and_is_a_project_level_gap(root: Path) -> None:
    _write(root, "src/whygame5/stray.py", "X = 1\n")
    _commit(root, "unplanned file")
    r = reconcile(root)
    assert r.orphans == ["src/whygame5/stray.py"]
    assert [(g.kind, g.ref) for g in r.unassigned_gaps] == [("orphan", "src/whygame5/stray.py")]
    assert r.failures == ["orphan: src/whygame5/stray.py"]
    assert main(["status", "--root", str(root)]) == 1


def test_symbol_drift_fails_and_marks_the_artifact_drifted(root: Path) -> None:
    path = root / ".aes" / "target.yaml"
    anchor = "    locator: {exact_path: src/whygame5/graph.py}\n"
    text = path.read_text(encoding="utf-8")
    assert anchor in text
    path.write_text(text.replace(anchor, anchor + "    exports: [normalize, denormalize]\n"), encoding="utf-8")
    _commit(root, "commit to an export that does not exist")

    r = reconcile(root)
    graph = next(a for a in r.artifacts if a.artifact_id == "ART-WG5-GRAPH")
    assert graph.status == "DRIFTED"
    assert [(d.kind, d.detail) for d in graph.drift] == [
        ("missing_export", "committed export 'denormalize' is not a top-level public symbol")
    ]
    assert _gaps(r, "CMP-WG5-GRAPH")[0] == ("drifted", "ART-WG5-GRAPH")
    assert r.failures == ["drifted: ART-WG5-GRAPH"]
    assert main(["reconcile", "--root", str(root), "--json"]) == 1


# --------------------------------------------------------------------------- #
# Derived only, deterministic
# --------------------------------------------------------------------------- #


def test_two_runs_differ_only_in_produced_at(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _observe(root, "OBS-EVAL", "ER-WG5-002-01", "SUPPORTS", [EVALUATOR])
    a, b = reconcile(root), reconcile(root)
    assert a.model_dump(exclude={"produced_at"}) == b.model_dump(exclude={"produced_at"})
    assert a.dirty is True  # the observation is untracked under .aes/

    for argv in (["reconcile"], ["status"]):
        assert main([*argv, "--root", str(root)]) == 0
        first = capsys.readouterr().out
        assert main([*argv, "--root", str(root)]) == 0
        assert capsys.readouterr().out == first
        assert "produced_at" not in first


def test_reconcile_writes_nothing(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _observe(root, "OBS-EVAL", "ER-WG5-002-01", "SUPPORTS", [EVALUATOR])
    _commit(root, "evidence")

    def snapshot() -> dict[str, bytes]:
        return {str(p.relative_to(root)): p.read_bytes() for p in sorted(root.rglob("*"))
                if p.is_file() and ".git" not in p.relative_to(root).parts}

    before = snapshot()
    reconcile(root)
    assert main(["reconcile", "--root", str(root), "--json"]) == 0
    assert main(["status", "--root", str(root)]) == 0
    capsys.readouterr()
    assert snapshot() == before
    assert _git(root, "status", "--porcelain", "--untracked-files=all") == ""

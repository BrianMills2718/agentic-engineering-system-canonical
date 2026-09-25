"""`aes evidence status` on the whygame5 target (SC-GF-007, SC-GF-008, D2).

SC-WG5-001 has three evidence requirements (a test, a live run, Brian's review),
so it is the real multi-input criterion ER-SC-GF-007-01 asks for.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from agentic_engineering_system.cli import main
from agentic_engineering_system.evidence import EvidenceError, assess
from agentic_engineering_system.records import RecordLoadError

WHYGAME5_AES = Path(__file__).parent / "fixtures" / "whygame5-54043e2" / ".aes"
PROMPTS = "src/whygame5/prompts.py"
RUN = "evidence/runs/r1/report.html"


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


@pytest.fixture
def root(tmp_path: Path) -> Path:
    (tmp_path / ".aes").mkdir()
    shutil.copy(WHYGAME5_AES / "project.yaml", tmp_path / ".aes" / "project.yaml")
    shutil.copy(WHYGAME5_AES / "target.yaml", tmp_path / ".aes" / "target.yaml")
    _write(tmp_path, PROMPTS, "PROMPT = 'why'\n")
    _write(tmp_path, RUN, "<p>run r1</p>\n")
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-q", "-m", "base")
    return tmp_path


def _observe(root: Path, oid: str, er: str, assessment: str, deps: list[str], rev: str | None = None) -> None:
    rev = rev or _git(root, "rev-parse", "HEAD")
    deps_yaml = "".join(f"\n  - {d}" for d in deps) or " []"
    _write(root, f".aes/observations/{oid}.yaml", f"""schema_version: aes.v0_2.observation.probe0
observation_id: {oid}
subject_refs: [SC-WG5-001]
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


def _sc(report, sc_id: str):
    return next(c for c in report.criteria if c.criterion_id == sc_id)


def test_no_observations_leaves_every_criterion_insufficient(root: Path) -> None:
    report = assess(root)
    assert {c.standing for c in report.criteria} == {"INSUFFICIENT"}
    assert _sc(report, "SC-WG5-001").requirements[0].detail == "no observation assesses it"


def test_one_passing_input_of_three_stays_insufficient(root: Path) -> None:
    """ER-SC-GF-007-01: a pass-like observation does not satisfy a multi-input criterion."""
    _observe(root, "OBS-1", "ER-WG5-001-01", "SUPPORTS", [PROMPTS])
    sc = _sc(assess(root), "SC-WG5-001")
    assert sc.standing == "INSUFFICIENT"
    assert [s.status for s in sc.requirements] == ["SUPPORTED", "NO_CURRENT_SUPPORT", "NO_CURRENT_SUPPORT"]


def test_every_requirement_current_and_supporting_is_supported(root: Path) -> None:
    _observe(root, "OBS-1", "ER-WG5-001-01", "SUPPORTS", [PROMPTS])
    _observe(root, "OBS-2", "ER-WG5-001-02", "SUPPORTS", [RUN])
    _observe(root, "OBS-3", "ER-WG5-001-03", "SUPPORTS", [RUN])  # Brian's review of that run
    assert _sc(assess(root), "SC-WG5-001").standing == "SUPPORTED"


def test_changed_dependency_stales_support(root: Path) -> None:
    """ER-SC-GF-008: changing what evidence depends on withdraws it until re-established."""
    _observe(root, "OBS-1", "ER-WG5-001-01", "SUPPORTS", [PROMPTS])
    _observe(root, "OBS-2", "ER-WG5-001-02", "SUPPORTS", [RUN])
    _observe(root, "OBS-3", "ER-WG5-001-03", "SUPPORTS", [RUN])
    _write(root, PROMPTS, "PROMPT = 'why, and give the opposite view'\n")
    _git(root, "commit", "-qam", "change prompts")

    report = assess(root)
    sc = _sc(report, "SC-WG5-001")
    assert sc.standing == "INSUFFICIENT"
    assert sc.requirements[0].status == "NO_CURRENT_SUPPORT"
    assert "OBS-1 SUPPORTS (STALE)" in sc.requirements[0].detail
    fresh = {oid: (f, why) for oid, f, why in report.observations}
    assert fresh["OBS-1"] == ("STALE", f"changed since observed: {PROMPTS}")
    assert fresh["OBS-2"][0] == "CURRENT"


def test_current_refutation_wins_and_a_stale_one_does_not(root: Path) -> None:
    _observe(root, "OBS-1", "ER-WG5-001-02", "REFUTES", [RUN])
    assert _sc(assess(root), "SC-WG5-001").standing == "REFUTED"
    _write(root, RUN, "<p>run r2</p>\n")
    _git(root, "commit", "-qam", "new run")
    assert _sc(assess(root), "SC-WG5-001").standing == "INSUFFICIENT"


def test_observation_without_dependency_paths_never_counts(root: Path) -> None:
    _observe(root, "OBS-1", "ER-WG5-001-01", "SUPPORTS", [])
    report = assess(root)
    assert _sc(report, "SC-WG5-001").requirements[0].status == "NO_CURRENT_SUPPORT"
    assert report.observations[0][1:] == ("UNKNOWN", "no subject_revision or no dependency_paths")


def test_unknown_requirement_reference_is_loud(root: Path) -> None:
    _observe(root, "OBS-1", "ER-DOES-NOT-EXIST", "SUPPORTS", [PROMPTS])
    with pytest.raises(EvidenceError, match="unknown evidence_requirement_ref 'ER-DOES-NOT-EXIST'"):
        assess(root)


def test_short_revision_and_error_with_assessment_are_rejected(root: Path) -> None:
    _observe(root, "OBS-1", "ER-WG5-001-01", "SUPPORTS", [PROMPTS], rev="abc123")
    with pytest.raises(RecordLoadError, match="full 40-hex commit"):
        assess(root)
    path = root / ".aes/observations/OBS-1.yaml"
    _observe(root, "OBS-1", "ER-WG5-001-01", "SUPPORTS", [PROMPTS])
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text.replace("execution_state: COMPLETED", "execution_state: ERROR")
        .replace("result: {note: fixture}", "error: provider down"),
        encoding="utf-8",
    )
    with pytest.raises(RecordLoadError, match="ERROR observation cannot carry assessments"):
        assess(root)


def test_cli_prints_standing(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _observe(root, "OBS-1", "ER-WG5-001-01", "SUPPORTS", [PROMPTS])
    assert main(["evidence", "status", "--root", str(root)]) == 0
    out = capsys.readouterr().out
    assert out.startswith("evidence: 5 criteria: 0 supported, 5 insufficient, 0 refuted; 1 observation(s)")
    assert "ER-WG5-001-01: SUPPORTED - supported by OBS-1" in out


# --------------------------------------------------------------------------- #
# aes evidence record
# --------------------------------------------------------------------------- #

import sys  # noqa: E402

from agentic_engineering_system.evidence import record  # noqa: E402

PASS = [sys.executable, "-c", "print('4 passed')"]
FAIL = [sys.executable, "-c", "raise SystemExit(1)"]


@pytest.fixture
def with_test(root: Path) -> Path:
    _write(root, "tests/test_prompts.py", "def test_ok():\n    assert True\n")
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "add prompt test")
    return root


def test_recorded_pass_supports_and_counts_until_its_test_changes(with_test: Path) -> None:
    done = record(with_test, "VS-WG5-PROMPTS", [PROMPTS], command=PASS)
    obs = done.observation
    assert obs.subject_revision == _git(with_test, "rev-parse", "HEAD")
    assert obs.dependency_paths == [PROMPTS, "tests/test_prompts.py"]
    assert [(a.evidence_requirement_ref, a.assessment) for a in obs.assessments] == [("ER-WG5-001-01", "SUPPORTS")]
    assert "4 passed" in obs.result["output_tail"]

    _git(with_test, "add", ".")
    _git(with_test, "commit", "-q", "-m", "record")
    er = _sc(assess(with_test), "SC-WG5-001").requirements[0]
    assert (er.status, er.detail) == ("SUPPORTED", f"supported by {obs.observation_id}")

    _write(with_test, "tests/test_prompts.py", "def test_ok():\n    assert 1\n")
    _git(with_test, "commit", "-qam", "edit test")
    assert _sc(assess(with_test), "SC-WG5-001").requirements[0].status == "NO_CURRENT_SUPPORT"


def test_recorded_failure_refutes(with_test: Path) -> None:
    obs = record(with_test, "VS-WG5-PROMPTS", [], command=FAIL).observation
    assert obs.assessments[0].assessment == "REFUTES"
    assert obs.result["exit_code"] == 1


def test_partial_coverage_is_recorded_inconclusive(with_test: Path) -> None:
    obs = record(with_test, "VS-WG5-PROMPTS", [], command=PASS, downgrade_basis="schema not checked").observation
    assert (obs.assessments[0].assessment, obs.assessments[0].basis) == ("INCONCLUSIVE", "schema not checked")


def test_uncommitted_dependency_is_refused(with_test: Path) -> None:
    _write(with_test, PROMPTS, "PROMPT = 'edited'\n")
    with pytest.raises(EvidenceError, match="commit before observing"):
        record(with_test, "VS-WG5-PROMPTS", [PROMPTS], command=PASS)


def test_human_review_and_external_subjects_are_refused(with_test: Path) -> None:
    with pytest.raises(EvidenceError, match="human_review"):
        record(with_test, "VS-WG5-BRIAN-FINDING", [], command=PASS)
    with pytest.raises(EvidenceError, match="unknown verification subject"):
        record(with_test, "VS-NOPE", [], command=PASS)


def test_second_record_at_same_revision_gets_a_new_id(with_test: Path) -> None:
    a = record(with_test, "VS-WG5-PROMPTS", [], command=PASS).observation.observation_id
    b = record(with_test, "VS-WG5-PROMPTS", [], command=PASS).observation.observation_id
    assert b == a + "-2"
    assert len(assess(with_test).observations) == 2


def test_cli_record_writes_an_observation(with_test: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """The first real use crashed: --command shared argparse dest 'command' with the
    subcommand, so every `aes evidence record` raised 'unhandled command None'."""
    rc = main(["evidence", "record", "VS-WG5-PROMPTS", "--depends-on", PROMPTS,
               "--root", str(with_test), "--command", *PASS])
    assert rc == 0
    out = capsys.readouterr().out
    assert out.startswith("wrote ") and "SUPPORTS for ER-WG5-001-01" in out
    assert main(["evidence", "record", "VS-WG5-PROMPTS", "--root", str(with_test)]) == 0  # default pytest


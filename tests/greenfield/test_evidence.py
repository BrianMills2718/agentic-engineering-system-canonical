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
    shutil.copyfile(WHYGAME5_AES / "project.yaml", tmp_path / ".aes" / "project.yaml")
    shutil.copyfile(WHYGAME5_AES / "target.yaml", tmp_path / ".aes" / "target.yaml")
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
    assert out.startswith("evidence: 5 criteria: 0 supported, 5 insufficient, 0 refuted; 1 observation(s): "
                          "1 current, 0 stale, 0 unknown, 0 unreachable; 0 superseded\n")
    assert "ER-WG5-001-01: SUPPORTED - supported by OBS-1" in out


# --------------------------------------------------------------------------- #
# Reachability: evidence at a commit HEAD does not contain (§19)
# --------------------------------------------------------------------------- #


def _squash_merged_branch_commit(root: Path) -> str:
    """A commit on a branch that is then squash-merged into main and deleted: the
    object stays in this clone's store, but no branch reaches it."""
    _git(root, "checkout", "-q", "-b", "feature")
    _write(root, PROMPTS, "PROMPT = 'why, twice'\n")
    _git(root, "commit", "-qam", "feature work")
    feature = _git(root, "rev-parse", "HEAD")
    _git(root, "checkout", "-q", "-")
    _git(root, "merge", "-q", "--squash", "feature")
    _git(root, "commit", "-qm", "squash-merge feature")
    _git(root, "branch", "-q", "-D", "feature")
    return feature


def test_squash_merged_commit_is_unreachable_although_it_still_resolves(root: Path) -> None:
    feature = _squash_merged_branch_commit(root)
    _git(root, "cat-file", "-e", f"{feature}^{{commit}}")  # the local object store still has it
    # same file content at HEAD as at the observed commit: dependency diff alone would say CURRENT
    assert _git(root, "diff", "--name-only", feature, "HEAD") == ""
    _observe(root, "OBS-SQUASHED", "ER-WG5-001-01", "SUPPORTS", [PROMPTS], rev=feature)
    report = assess(root)
    assert report.observations == ((
        "OBS-SQUASHED", "UNREACHABLE",
        f"subject commit {feature[:8]} is not reachable from HEAD (squash-merged or deleted branch?)",
    ),)
    er = _sc(report, "SC-WG5-001").requirements[0]
    assert (er.status, er.detail) == ("NO_CURRENT_SUPPORT", "OBS-SQUASHED SUPPORTS (UNREACHABLE)")


def test_commit_this_clone_lacks_is_unreachable_with_the_same_text(root: Path) -> None:
    """A fresh clone does not have the squashed branch's objects at all; it must agree."""
    missing = "0123456789abcdef0123456789abcdef01234567"
    _observe(root, "OBS-ELSEWHERE", "ER-WG5-001-01", "SUPPORTS", [PROMPTS], rev=missing)
    assert assess(root).observations[0][1:] == (
        "UNREACHABLE", "subject commit 01234567 is not reachable from HEAD (squash-merged or deleted branch?)",
    )


def test_cli_counts_unreachable_separately(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    feature = _squash_merged_branch_commit(root)
    _observe(root, "OBS-SQUASHED", "ER-WG5-001-01", "SUPPORTS", [PROMPTS], rev=feature)
    _observe(root, "OBS-HERE", "ER-WG5-001-01", "SUPPORTS", [PROMPTS])
    assert main(["evidence", "status", "--root", str(root)]) == 0
    out = capsys.readouterr().out
    assert "2 observation(s): 1 current, 0 stale, 0 unknown, 1 unreachable; 0 superseded\n" in out
    assert f"    OBS-SQUASHED: UNREACHABLE - subject commit {feature[:8]} is not reachable" in out


# --------------------------------------------------------------------------- #
# superseded_by: a replaced record is kept and never counts
# --------------------------------------------------------------------------- #


def _supersede(root: Path, oid: str, by: str) -> None:
    path = root / f".aes/observations/{oid}.yaml"
    path.write_text(path.read_text(encoding="utf-8") + f"superseded_by: {by}\n", encoding="utf-8")


def test_superseded_observation_never_counts_even_when_current(root: Path) -> None:
    _observe(root, "OBS-OLD", "ER-WG5-001-01", "SUPPORTS", [PROMPTS])
    _observe(root, "OBS-NEW", "ER-WG5-001-01", "REFUTES", [PROMPTS])
    _supersede(root, "OBS-NEW", "OBS-OLD")  # the CURRENT refutation is withdrawn by being superseded
    report = assess(root)
    assert {oid: f for oid, f, _ in report.observations} == {"OBS-NEW": "CURRENT", "OBS-OLD": "CURRENT"}
    assert report.superseded == (("OBS-NEW", "OBS-OLD"),)
    assert report.counts() == "1 current, 0 stale, 0 unknown, 0 unreachable; 1 superseded"
    er = _sc(report, "SC-WG5-001").requirements[0]
    assert (er.status, er.detail) == ("SUPPORTED", "supported by OBS-OLD")

    _supersede(root, "OBS-OLD", "OBS-NEW")  # both superseded: nothing counts
    er = _sc(assess(root), "SC-WG5-001").requirements[0]
    assert er.status == "NO_CURRENT_SUPPORT"
    assert er.detail == ("OBS-NEW REFUTES (CURRENT, superseded by OBS-OLD); "
                         "OBS-OLD SUPPORTS (CURRENT, superseded by OBS-NEW)")


def test_superseded_by_must_name_another_loaded_observation(root: Path) -> None:
    _observe(root, "OBS-1", "ER-WG5-001-01", "SUPPORTS", [PROMPTS])
    _supersede(root, "OBS-1", "OBS-NOWHERE")
    with pytest.raises(EvidenceError, match="OBS-1 superseded_by 'OBS-NOWHERE'"):
        assess(root)
    _observe(root, "OBS-1", "ER-WG5-001-01", "SUPPORTS", [PROMPTS])
    _supersede(root, "OBS-1", "OBS-1")
    with pytest.raises(RecordLoadError, match="cannot be superseded_by itself"):
        assess(root)


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



def test_discovered_dependencies_union_declared_ones(with_test: Path) -> None:
    """--depends-on adds to what the test's imports reach; the basis keeps them apart."""
    _write(with_test, "src/whygame5/__init__.py", "")
    _write(with_test, "tests/test_prompts.py", "from whygame5 import prompts\n\ndef test_ok():\n    assert prompts\n")
    _git(with_test, "add", ".")
    _git(with_test, "commit", "-q", "-m", "test imports prompts")

    obs = record(with_test, "VS-WG5-PROMPTS", [RUN, PROMPTS], command=PASS).observation
    assert obs.dependency_basis.discovered == ["src/whygame5/__init__.py", PROMPTS]
    assert obs.dependency_basis.declared == [RUN, PROMPTS]
    assert obs.dependency_paths == [RUN, "src/whygame5/__init__.py", PROMPTS, "tests/test_prompts.py"]

    # Discovery alone makes a change to an imported file stale the evidence.
    _git(with_test, "add", ".")
    _git(with_test, "commit", "-q", "-m", "record")
    obs = record(with_test, "VS-WG5-PROMPTS", [], command=PASS).observation
    _git(with_test, "add", ".")
    _git(with_test, "commit", "-q", "-m", "record without declaring")
    _write(with_test, PROMPTS, "PROMPT = 'changed'\n")
    _git(with_test, "commit", "-qam", "change prompts")
    fresh = {oid: f for oid, f, _ in assess(with_test).observations}
    assert fresh[obs.observation_id] == "STALE"


def test_dependency_paths_must_match_their_basis(with_test: Path) -> None:
    path = record(with_test, "VS-WG5-PROMPTS", [PROMPTS], command=PASS).path
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace(f"- {PROMPTS}\n", "", 1), encoding="utf-8")  # drop it from dependency_paths only
    with pytest.raises(RecordLoadError, match="is not the union of dependency_basis"):
        assess(with_test)


def _with_origin(root: Path) -> Path:
    """Give `root` a bare `origin` holding main, as a clone would have."""
    bare = root.parent / "origin.git"
    _git(root.parent, "init", "-q", "--bare", str(bare))
    _git(root, "branch", "-M", "main")
    _git(root, "remote", "add", "origin", str(bare))
    _git(root, "push", "-q", "-u", "origin", "main")
    return bare


def test_record_on_a_branch_warns_about_squash_merging(with_test: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _with_origin(with_test)
    assert record(with_test, "VS-WG5-PROMPTS", [], command=PASS).branch_note is None  # at origin/main
    _git(with_test, "add", ".")
    _git(with_test, "commit", "-q", "-m", "record on main")
    _git(with_test, "push", "-q", "origin", "main")

    _git(with_test, "checkout", "-q", "-b", "feature")
    _write(with_test, "tests/test_prompts.py", "def test_ok():\n    assert 1\n")
    _git(with_test, "commit", "-qam", "feature work")
    head = _git(with_test, "rev-parse", "HEAD")
    assert main(["evidence", "record", "VS-WG5-PROMPTS", "--root", str(with_test), "--command", *PASS]) == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("wrote ")  # recorded, not refused
    assert captured.err == (
        f"warning: recorded at {head[:8]} on branch feature; this evidence stays valid only if that commit "
        "reaches the default branch unchanged — merge with a merge commit (not squash), or re-record "
        "after merging\n"
    )


def test_record_without_a_remote_notes_the_check_was_skipped(with_test: Path) -> None:
    note = record(with_test, "VS-WG5-PROMPTS", [], command=PASS).branch_note
    assert note == ("note: no origin/HEAD or origin/main here, so whether the recorded commit is on the "
                    "default branch was not checked")


def test_uncommitted_python_test_cannot_be_discovered(root: Path) -> None:
    _write(root, "tests/test_prompts.py", "def test_ok():\n    assert True\n")
    with pytest.raises(EvidenceError, match="not a governed Python file at HEAD"):
        record(root, "VS-WG5-PROMPTS", [], command=PASS)

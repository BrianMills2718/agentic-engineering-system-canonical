"""Entry-level target dependencies and negative-control observations (roadmap phase 6a).

- `dependency_target_refs`: an observation that depends on target entries goes
  STALE when one of those entries changes or disappears, not when some other part
  of `.aes/target.yaml` changes (the §14/§15 kink: accepting a plan, or adding an
  evidence requirement, staled AES's own observations on whygame5). Listing the
  target file in `dependency_paths` keeps the coarse, file-level behaviour.
- `control: {kind: negative, ...}`: an observation of a deliberately mutated
  commit computes freshness from the unmodified `base_revision`, so it is not
  stale by construction (§14 item 2); its assessments must follow its observed
  outcome.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from agentic_engineering_system.evidence import EvidenceError, assess, record
from agentic_engineering_system.records import RecordLoadError

WHYGAME5_AES = Path(__file__).parent / "fixtures" / "whygame5-54043e2" / ".aes"
PROMPTS = "src/whygame5/prompts.py"
TEST = "tests/test_prompts.py"
TARGET = ".aes/target.yaml"
PASS = [sys.executable, "-c", "print('1 passed')"]


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


def _edit_target(root: Path, old: str, new: str) -> None:
    path = root / TARGET
    text = path.read_text(encoding="utf-8")
    assert text.count(old) == 1, old
    path.write_text(text.replace(old, new), encoding="utf-8")


@pytest.fixture
def root(tmp_path: Path) -> Path:
    (tmp_path / ".aes").mkdir()
    shutil.copy(WHYGAME5_AES / "project.yaml", tmp_path / ".aes" / "project.yaml")
    shutil.copy(WHYGAME5_AES / "target.yaml", tmp_path / TARGET)
    _write(tmp_path, PROMPTS, "PROMPT = 'why'\n")
    _write(tmp_path, "src/whygame5/__init__.py", "")
    _write(tmp_path, TEST, "from whygame5 import prompts\n\ndef test_ok():\n    assert prompts.PROMPT\n")
    _git(tmp_path, "init", "-q", "-b", "main")
    _commit(tmp_path, "base")
    return tmp_path


def _observation(root: Path, oid: str, *, rev: str, deps: list[str], target_refs: list[str],
                 assessment: str = "SUPPORTS", control: str = "", result: str = "{exit_code: 1}") -> None:
    deps_yaml = "".join(f"\n  - {d}" for d in deps) or " []"
    refs_yaml = "".join(f"\n  - {r}" for r in target_refs) or " []"
    _write(root, f".aes/observations/{oid}.yaml", f"""schema_version: aes.v0_2.observation.probe0
observation_id: {oid}
subject_refs: [VS-WG5-PROMPTS]
subject_revision: {rev}
dependency_paths:{deps_yaml}
dependency_target_refs:{refs_yaml}
{control}observer: {{identity: test}}
method: fixture
execution_state: COMPLETED
result: {result}
produced_at: 2026-09-25T00:00:00+00:00
assessments:
  - evidence_requirement_ref: ER-WG5-001-01
    assessment: {assessment}
    basis: fixture
    assessor: {{identity: test}}
""")


def _fresh(root: Path) -> dict[str, tuple[str, str]]:
    return {oid: (f, why) for oid, f, why in assess(root).observations}


# --------------------------------------------------------------------------- #
# A. Entry-level target dependencies
# --------------------------------------------------------------------------- #


def test_record_depends_on_target_entries_not_the_target_file(root: Path) -> None:
    obs = record(root, "VS-WG5-PROMPTS", [], command=PASS).observation
    assert TARGET not in obs.dependency_paths
    # the subject, the requirement it assesses, and the planned artifacts among its paths
    assert obs.dependency_target_refs == [
        "VS-WG5-PROMPTS", "ER-WG5-001-01", "ART-WG5-PKG", "ART-WG5-PROMPTS", "ART-WG5-TEST-PROMPTS",
    ]


def test_record_refuses_an_uncommitted_target(root: Path) -> None:
    _edit_target(root, "target_id: whygame5-target", "target_id: whygame5-target-edited")
    with pytest.raises(EvidenceError, match="commit before observing.*target.yaml"):
        record(root, "VS-WG5-PROMPTS", [], command=PASS)


def test_unrelated_target_edit_keeps_entry_dependency_current(root: Path) -> None:
    oid = record(root, "VS-WG5-PROMPTS", [], command=PASS).observation.observation_id
    _commit(root, "record")
    # A new criterion elsewhere in the file (what accepting a plan does).
    _edit_target(root, "purpose: Brian answers the four questions from the report alone",
                 "purpose: Brian answers the four questions from the report alone, unaided")
    _commit(root, "edit another verification subject")
    assert _fresh(root)[oid][0] == "CURRENT"
    assert "no dependency or target entry changed since" in _fresh(root)[oid][1]
    assert assess(root).criteria[0].requirements[0].status == "SUPPORTED"


def test_edited_referenced_entry_stales_it(root: Path) -> None:
    oid = record(root, "VS-WG5-PROMPTS", [], command=PASS).observation.observation_id
    _commit(root, "record")
    _edit_target(root, "      - id: ER-WG5-001-01\n        kind: deterministic_test\n        requirement: ",
                 "      - id: ER-WG5-001-01\n        kind: deterministic_test\n        requirement: Stricter. ")
    _commit(root, "tighten the requirement")
    assert _fresh(root)[oid] == ("STALE", "target entries changed since observed: ER-WG5-001-01")


def test_removed_referenced_entry_stales_it(root: Path) -> None:
    rev = _git(root, "rev-parse", "HEAD")
    _observation(root, "OBS-REMOVED", rev=rev, deps=[], target_refs=["ART-WG5-CLI"])
    _commit(root, "observe")
    path = root / TARGET
    text = path.read_text(encoding="utf-8")
    start = text.index("  - id: ART-WG5-CLI\n")
    end = text.index("  - id: ART-WG5-TEST-PROMPTS\n")
    path.write_text(text[:start] + text[end:], encoding="utf-8")
    _edit_target(root, ", ART-WG5-CLI]", "]")  # the component that listed it
    _commit(root, "drop the CLI artifact")
    assert _fresh(root)["OBS-REMOVED"] == ("STALE", "target entries removed since observed: ART-WG5-CLI")


def test_file_level_target_dependency_is_the_coarse_form(root: Path) -> None:
    rev = _git(root, "rev-parse", "HEAD")
    _observation(root, "OBS-COARSE", rev=rev, deps=[TARGET], target_refs=[])
    _observation(root, "OBS-FINE", rev=rev, deps=[], target_refs=["VS-WG5-PROMPTS", "ER-WG5-001-01"])
    _commit(root, "observe")
    _edit_target(root, "target_id: whygame5-target", "target_id: whygame5-target-renamed")
    _commit(root, "unrelated edit")
    fresh = _fresh(root)
    assert fresh["OBS-COARSE"] == ("STALE", f"changed since observed: {TARGET}")
    assert fresh["OBS-FINE"][0] == "CURRENT"


def test_ref_absent_at_the_observed_revision_is_loud(root: Path) -> None:
    rev = _git(root, "rev-parse", "HEAD")
    _observation(root, "OBS-BAD", rev=rev, deps=[], target_refs=["SC-WG5-999"])
    with pytest.raises(EvidenceError, match=r"\['SC-WG5-999'\] are not declared"):
        assess(root)


def test_duplicate_target_refs_are_rejected(root: Path) -> None:
    rev = _git(root, "rev-parse", "HEAD")
    _observation(root, "OBS-DUP", rev=rev, deps=[], target_refs=["SC-WG5-001", "SC-WG5-001"])
    with pytest.raises(RecordLoadError, match="more than once"):
        assess(root)


# --------------------------------------------------------------------------- #
# B. Negative controls
# --------------------------------------------------------------------------- #


def _mutated(root: Path) -> tuple[str, str]:
    """A base commit on main and a scratch commit off it that breaks prompts.py,
    reachable only through a tag, as whygame5's drift observation is."""
    base = _git(root, "rev-parse", "HEAD")
    _git(root, "checkout", "-q", "--detach")
    _write(root, PROMPTS, "RENAMED = 'why'\n")
    mutated = _commit(root, "break it on purpose")
    _git(root, "tag", "scratch/mutated", mutated)
    _git(root, "checkout", "-q", "main")
    return base, mutated


def _control(base: str, observed: str = "detected") -> str:
    return (f"control:\n  kind: negative\n  base_revision: {base}\n"
            f"  mutation: rename PROMPT in {PROMPTS}\n  expected_outcome: detected\n"
            f"  observed_outcome: {observed}\n")


REFS = ["VS-WG5-PROMPTS", "ER-WG5-001-01"]


def test_mutated_revision_is_stale_by_construction_without_control(root: Path) -> None:
    _, mutated = _mutated(root)
    _observation(root, "OBS-DRIFT", rev=mutated, deps=[PROMPTS], target_refs=REFS)
    assert _fresh(root)["OBS-DRIFT"] == ("STALE", f"changed since observed: {PROMPTS}")


def test_negative_control_is_current_against_its_base_and_stales_for_the_right_reason(root: Path) -> None:
    base, mutated = _mutated(root)
    _observation(root, "OBS-DRIFT", rev=mutated, deps=[PROMPTS], target_refs=REFS, control=_control(base))
    _commit(root, "record the control")
    assert _fresh(root)["OBS-DRIFT"] == ("CURRENT", f"negative control of {base[:12]}: "
                                                   f"no dependency or target entry changed since {base[:12]}")
    assert assess(root).criteria[0].requirements[0].status == "SUPPORTED"

    _write(root, PROMPTS, "PROMPT = 'why, really'\n")
    _commit(root, "change the real prompts")
    assert _fresh(root)["OBS-DRIFT"] == ("STALE", f"negative control of {base[:12]}: changed since observed: {PROMPTS}")


def test_a_missed_mutation_must_refute_and_does(root: Path) -> None:
    base, mutated = _mutated(root)
    _observation(root, "OBS-MISSED", rev=mutated, deps=[PROMPTS], target_refs=REFS,
                 control=_control(base, "missed"), assessment="SUPPORTS", result="{exit_code: 0}")
    with pytest.raises(RecordLoadError, match="observed_outcome missed allows only"):
        assess(root)
    _observation(root, "OBS-MISSED", rev=mutated, deps=[PROMPTS], target_refs=REFS,
                 control=_control(base, "missed"), assessment="REFUTES", result="{exit_code: 0}")
    er = assess(root).criteria[0].requirements[0]
    assert (er.status, er.detail) == ("REFUTED", "refuted by OBS-MISSED")


def test_a_passing_tool_cannot_be_recorded_as_detected(root: Path) -> None:
    base, mutated = _mutated(root)
    _observation(root, "OBS-LIE", rev=mutated, deps=[PROMPTS], target_refs=REFS,
                 control=_control(base), result="{exit_code: 0}")
    with pytest.raises(RecordLoadError, match="reports exit_code 0"):
        assess(root)


def test_control_base_must_be_on_a_branch_and_the_mutations_ancestor(root: Path) -> None:
    base, mutated = _mutated(root)
    # base on no branch: the mutated commit itself used as a base of a further mutation
    _git(root, "checkout", "-q", "--detach", mutated)
    _write(root, PROMPTS, "AGAIN = 1\n")
    twice = _commit(root, "mutate again")
    _git(root, "checkout", "-q", "main")
    _observation(root, "OBS-C", rev=twice, deps=[PROMPTS], target_refs=REFS, control=_control(mutated))
    with pytest.raises(EvidenceError, match="is on no branch"):
        assess(root)
    # base on a branch but not the mutation's ancestor
    _write(root, "src/whygame5/__init__.py", '"""pkg"""\n')
    later = _commit(root, "later main commit")
    _observation(root, "OBS-C", rev=mutated, deps=[PROMPTS], target_refs=REFS, control=_control(later))
    with pytest.raises(EvidenceError, match="is not an ancestor"):
        assess(root)
    assert base != later

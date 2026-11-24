"""`make check-trace` fails when the trace findings and the accepted list differ in either direction.

The gate is Makefile configuration, not an OpenSpec requirement (alignment-cleanup plan, step 4 and its
acceptance line "A new requirement with no `Implements:` line fails `make check` (shown by a test)").
A finding missing from the accepted list is exactly what a new unimplemented requirement produces; since the
committed list emptied (2026-11-23), that case runs against a scratch repository holding one unbuilt requirement.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACCEPTED = ROOT / "docs" / "planning" / "trace-accepted.txt"


SPEC = """# demo Specification

## Purpose
Demo.

## Requirements

### Requirement: Greet

The tool SHALL greet.

Source: inferred by agent (test fixture)

#### Scenario: It greets

- **WHEN** it runs
- **THEN** it greets
"""


def _gate(tmp_path: Path, accepted: list[str], repo: Path = ROOT) -> subprocess.CompletedProcess[str]:
    listed = tmp_path / "accepted.txt"
    listed.write_text("".join(f"{line}\n" for line in accepted), encoding="utf-8")
    return subprocess.run(
        ["make", "--no-print-directory", "-C", str(ROOT), "check-trace", f"PYTHON={sys.executable}",
         f"TRACE_ACCEPTED={listed}", f"TRACE_NOW={tmp_path / 'now.txt'}", f"TRACE_REPO={repo}"],
        capture_output=True, text=True, check=False,
    )


def _unbuilt(tmp_path: Path) -> Path:
    """A repository with one requirement and no code: the trace check finds it unimplemented and untested."""
    repo = tmp_path / "unbuilt"
    (repo / "openspec" / "specs" / "demo").mkdir(parents=True)
    (repo / "openspec" / "specs" / "demo" / "spec.md").write_text(SPEC, encoding="utf-8")
    (repo / "src").mkdir()
    return repo


def test_the_committed_list_passes(tmp_path: Path) -> None:
    result = _gate(tmp_path, ACCEPTED.read_text(encoding="utf-8").splitlines())
    assert result.returncode == 0, result.stdout + result.stderr
    assert "RESULT check-trace" in result.stdout


def test_a_finding_not_on_the_list_fails(tmp_path: Path) -> None:
    repo = _unbuilt(tmp_path)
    result = _gate(tmp_path, ["untested demo/it-greets"], repo)
    assert result.returncode != 0
    assert "+unimplemented demo/greet" in result.stdout
    listed = _gate(tmp_path, ["unimplemented demo/greet", "untested demo/it-greets"], repo)
    assert listed.returncode == 0, listed.stdout + listed.stderr


def test_a_fixed_finding_left_on_the_list_fails(tmp_path: Path) -> None:
    lines = ACCEPTED.read_text(encoding="utf-8").splitlines()
    result = _gate(tmp_path, sorted([*lines, "unimplemented ship/a-requirement-already-built"]))
    assert result.returncode != 0
    assert "-unimplemented ship/a-requirement-already-built" in result.stdout


def test_the_copy_and_order_targets_fail_when_their_check_cannot_run() -> None:
    """A wrapper that only greps for bad lines would pass when the check never ran; these need its RESULT line."""
    for target in ("check-copies", "check-source-order"):
        broken = subprocess.run(["make", "--no-print-directory", "-C", str(ROOT), target, "PYTHON=false"],
                                capture_output=True, text=True, check=False)
        assert broken.returncode != 0, (target, broken.stdout)
        assert "did not run" in broken.stdout, (target, broken.stdout)

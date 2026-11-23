"""`make check-trace` fails when the trace findings and the accepted list differ in either direction.

The gate is Makefile configuration, not an OpenSpec requirement (alignment-cleanup plan, step 4 and its
acceptance line "A new requirement with no `Implements:` line fails `make check` (shown by a test)").
A finding missing from the accepted list is exactly what a new unimplemented requirement produces.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACCEPTED = ROOT / "docs" / "planning" / "trace-accepted.txt"


def _gate(tmp_path: Path, accepted: list[str]) -> subprocess.CompletedProcess[str]:
    listed = tmp_path / "accepted.txt"
    listed.write_text("".join(f"{line}\n" for line in accepted), encoding="utf-8")
    return subprocess.run(
        ["make", "--no-print-directory", "-C", str(ROOT), "check-trace", f"PYTHON={sys.executable}",
         f"TRACE_ACCEPTED={listed}", f"TRACE_NOW={tmp_path / 'now.txt'}"],
        capture_output=True, text=True, check=False,
    )


def test_the_committed_list_passes(tmp_path: Path) -> None:
    result = _gate(tmp_path, ACCEPTED.read_text(encoding="utf-8").splitlines())
    assert result.returncode == 0, result.stdout + result.stderr
    assert "RESULT check-trace" in result.stdout


def test_a_finding_not_on_the_list_fails(tmp_path: Path) -> None:
    lines = ACCEPTED.read_text(encoding="utf-8").splitlines()
    result = _gate(tmp_path, lines[1:])
    assert result.returncode != 0
    assert f"+{lines[0]}" in result.stdout


def test_a_fixed_finding_left_on_the_list_fails(tmp_path: Path) -> None:
    lines = ACCEPTED.read_text(encoding="utf-8").splitlines()
    result = _gate(tmp_path, sorted([*lines, "unimplemented ship/a-requirement-already-built"]))
    assert result.returncode != 0
    assert "-unimplemented ship/a-requirement-already-built" in result.stdout

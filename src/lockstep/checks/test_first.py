"""Test-first check: a test for a scenario new since the base revision must fail on the base source.

Implements: lockstep-checks/test-first-new-scenario-tests-fail-before-the-change,
    lockstep-checks/test-first-a-missing-base-revision-is-reported-not-crashed,
    lockstep-checks/test-first-tests-for-existing-behavior-are-exempt-and-counted

Requirement text (generated):
    lockstep-checks/test-first-new-scenario-tests-fail-before-the-change: `lockstep check test-first --base <rev>` SHALL
        run, against the base revision's source, every test marked for a scenario that the current
        revision's specs or active changes define and the base revision's specs and active changes
        do not, and exit 1 if any of them passes there.
    lockstep-checks/test-first-a-missing-base-revision-is-reported-not-crashed: `lockstep check test-first --base <rev>`
        SHALL, when `<rev>` does not name a commit, check nothing, report that the base was missing,
        and exit 0.
    lockstep-checks/test-first-tests-for-existing-behavior-are-exempt-and-counted: The test-first check SHALL not
        run a test marked `req(..., existing=True)`, and SHALL report how many such tests it
        skipped.
"""

from dataclasses import dataclass, field
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import xml.etree.ElementTree as ET

from lockstep.checks.markers import req_markers, source_dirs, test_dirs
from lockstep.checks.spec import read_plan


@dataclass
class Result:
    """Which new-scenario tests were run on the base source, and which of them passed there."""

    checked: list[str] = field(default_factory=list)
    passed_before: list[str] = field(default_factory=list)
    skipped: str = ""
    existing: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True when no new-scenario test passed on the base source."""
        return not self.passed_before


def _extract(root: Path, base: str, dest: Path) -> None:
    """Unpack the tracked files of revision base into dest."""
    archive = subprocess.run(["git", "-C", str(root), "archive", base], check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(dest, filter="data")


def _scenarios(root: Path) -> set[str]:
    """Scenario IDs a revision defines, in its specs or its active changes.

    Reading both means a scenario still in a change is checked, and archiving a change, which only
    moves its scenarios into the specs, makes none of them new.

    Args:
        root: Repository root at that revision.

    Returns:
        The scenario IDs.
    """
    return set(read_plan(root).scenarios) | set(read_plan(root, changes=True).scenarios)


def check(root: Path, base: str) -> Result:
    """Run tests for scenarios added since base against base's source.

    Args:
        root: Repository root (the current revision's working tree).
        base: Git revision to compare with, such as `origin/main`.

    Returns:
        The tests checked and those that already passed on base.
    """
    root = Path(root)
    found = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--verify", "--quiet", f"{base}^{{commit}}"], capture_output=True
    )
    if found.returncode != 0:
        return Result(skipped=f"base {base} not found")
    with tempfile.TemporaryDirectory() as tmp:
        old = Path(tmp)
        _extract(root, base, old)
        new_ids = _scenarios(root) - _scenarios(old)
        nodes = sorted({node for ident, _, node in req_markers(root, existing=False) if ident in new_ids})
        exempt = sorted({node for ident, _, node in req_markers(root, existing=True) if ident in new_ids})
        result = Result(checked=nodes, existing=exempt)
        if not nodes:
            return result
        for folder in test_dirs(root):
            destination = old / folder.relative_to(root)
            shutil.rmtree(destination, ignore_errors=True)
            if folder.is_dir():
                shutil.copytree(folder, destination)
        report = old / "report.xml"
        paths = [old / d.relative_to(root) for d in [*source_dirs(root), *test_dirs(root)]]
        env = {**os.environ, "PYTHONPATH": os.pathsep.join(str(p) for p in paths)}
        subprocess.run(
            [sys.executable, "-m", "pytest", "-p", "no:cacheprovider", f"--junitxml={report}", *nodes],
            cwd=old,
            env=env,
            capture_output=True,
        )
        if report.exists():
            for case in ET.parse(report).iter("testcase"):
                if len(case) == 0 or all(child.tag in ("system-out", "system-err") for child in case):
                    path = case.get("file") or case.get("classname", "").replace(".", "/") + ".py"
                    result.passed_before.append(f"{path}::{case.get('name')}")
        result.passed_before.sort()
        return result

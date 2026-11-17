"""Test-first check: a test for a scenario new since the base revision must fail on the base source,
and a scenario whose text changed needs at least one test that fails there.

Implements: lockstep-checks/test-first-new-scenario-tests-fail-before-the-change,
    lockstep-checks/test-first-a-missing-base-revision-is-reported-not-crashed,
    lockstep-checks/test-first-tests-for-existing-behavior-are-exempt-and-counted,
    lockstep-checks/test-first-a-test-run-that-cannot-start-fails-the-check,
    lockstep-checks/test-first-a-changed-scenario-needs-a-test-that-fails-before-the-change

Requirement text (generated):
    lockstep-checks/test-first-new-scenario-tests-fail-before-the-change: `lockstep check test-first
        --base <rev>` SHALL run, against the base revision's source, every test marked for a
        scenario that the current revision's specs or active changes define and the base revision's
        specs and active changes do not, and exit 1 if any of them passes there.
    lockstep-checks/test-first-a-missing-base-revision-is-reported-not-crashed: `lockstep check
        test-first --base <rev>` SHALL, when `<rev>` does not name a commit, check nothing, report
        that the base was missing, and exit 0.
    lockstep-checks/test-first-tests-for-existing-behavior-are-exempt-and-counted: The test-first
        check SHALL not run a test marked `req(..., existing=True)`, and SHALL report how many such
        tests it skipped.
    lockstep-checks/test-first-a-test-run-that-cannot-start-fails-the-check: `lockstep check
        test-first` SHALL exit 1 with a message saying pytest could not run when running the new
        tests on the base source produces no test report (pytest missing from Lockstep's
        environment, or a usage error); it SHALL NOT report the tests as not passing before.
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

from lockstep.checks.changed import change_set, wording_only
from lockstep.checks.markers import req_markers, source_dirs, test_dirs
from lockstep.checks.spec import effective_plan, normal, read_plan


class PytestUnavailable(RuntimeError):
    """pytest could not run in Lockstep's environment, so nothing was judged; the check must fail, not accept."""


@dataclass
class Result:
    """Which new-scenario tests were run on the base source, and which of them passed there; which
    changed scenarios were checked, and which of them had no test that failed there."""

    checked: list[str] = field(default_factory=list)
    passed_before: list[str] = field(default_factory=list)
    skipped: str = ""
    existing: list[str] = field(default_factory=list)
    changed: list[str] = field(default_factory=list)
    no_failing_test: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True when no new-scenario test passed on the base source and every changed scenario had one that failed."""
        return not self.passed_before and not self.no_failing_test


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


def _changed_scenarios(root: Path, old: Path) -> list[str]:
    """Scenario IDs both revisions' effective plans define with different text, minus those declared wording-only.

    Args:
        root: Repository root at the current revision.
        old: The base revision's files.

    Returns:
        The IDs, sorted.
    """
    now, before = effective_plan(root), effective_plan(old)
    declared = wording_only(change_set(root, old))
    return sorted(
        s for s in set(now.scenario_text) & set(before.scenario_text)
        if normal(now.scenario_text[s]) != normal(before.scenario_text[s])
        and s not in declared and now.parent.get(s) not in declared
    )


def check(root: Path, base: str) -> Result:
    """Run tests for scenarios added since base, and every test of a scenario changed since base, against base's source.

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
        changed = _changed_scenarios(root, old)
        changed_tests = {sid: sorted({node for ident, _, node in req_markers(root) if ident == sid}) for sid in changed}
        result = Result(checked=nodes, existing=exempt, changed=changed)
        result.no_failing_test = [sid for sid, tests in changed_tests.items() if not tests]
        to_run = sorted(set(nodes) | {node for tests in changed_tests.values() for node in tests})
        if not to_run:
            return result
        for folder in test_dirs(root):
            destination = old / folder.relative_to(root)
            shutil.rmtree(destination, ignore_errors=True)
            if folder.is_dir():
                shutil.copytree(folder, destination)
        report = old / "report.xml"
        paths = [old / d.relative_to(root) for d in [*source_dirs(root), *test_dirs(root)]]
        env = {**os.environ, "PYTHONPATH": os.pathsep.join(str(p) for p in paths)}
        try:
            ran = subprocess.run(
                [sys.executable, "-m", "pytest", "-p", "no:cacheprovider", f"--junitxml={report}", *to_run],
                cwd=old,
                env=env,
                capture_output=True,
                text=True,
            )
        except OSError as err:
            raise PytestUnavailable(f"pytest could not run: {sys.executable} cannot be started ({err})") from err
        if not report.exists():  # no report means no test ran (pytest missing, or a usage error): never "all failed"
            detail = (ran.stderr or ran.stdout).strip().splitlines()[-1:] or [f"exit {ran.returncode}"]
            raise PytestUnavailable(f"pytest could not run with {sys.executable}: {detail[0]}. "
                                    "Install pytest in Lockstep's environment.")
        passed, failed = set(), set()
        for case in ET.parse(report).iter("testcase"):
            path = case.get("file") or case.get("classname", "").replace(".", "/") + ".py"
            node = f"{path}::{case.get('name')}"
            if len(case) == 0 or all(child.tag in ("system-out", "system-err") for child in case):
                passed.add(node)
            else:
                failed.add(node.split("[")[0])
        result.passed_before = sorted(n for n in passed if n.split("[")[0] in set(nodes))  # new-scenario tests only
        # A changed scenario's test counts as passing on the base only when every case of it was reported passing
        # (all parameters); one that failed, errored or was not reported there counts as failing.
        passing = {n.split("[")[0] for n in passed} - failed
        result.no_failing_test = sorted(
            result.no_failing_test + [sid for sid, tests in changed_tests.items() if tests and set(tests) <= passing]
        )
        return result

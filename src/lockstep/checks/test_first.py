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
        check SHALL not run a test marked `req(..., existing=True)` for a scenario that is new since
        the base, and SHALL report how many such tests it skipped. For a scenario whose text changed
        since the base, `existing=True` SHALL NOT exempt a test: it is run on the base source like
        any other test marked for that scenario.
    lockstep-checks/test-first-a-test-run-that-cannot-start-fails-the-check: `lockstep check
        test-first` SHALL exit 1 with a message saying pytest could not run when running the new
        tests on the base source produces no test report (pytest missing from Lockstep's
        environment, or a usage error); it SHALL NOT report the tests as not passing before.
    lockstep-checks/test-first-a-changed-scenario-needs-a-test-that-fails-before-the-change:
        `lockstep check test-first --base <rev>` SHALL, for each scenario that both revisions define
        and whose text differs (runs of whitespace counting as one space; text from an active
        change's spec delta replacing the spec's), run every test marked for it against the base
        revision's source, and SHALL report `no-failing-test <scenario id>` and exit 1 when none of
        them fails there. It SHALL NOT check a scenario that a plan new or different from the base
        declares on a `Wording-only:` line, by its own ID or its requirement's. Its count line SHALL
        add `changed=<n>`, the number of changed scenarios checked, and `no_failing_test=<n>`.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:checks:test_first.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-checks/test-first-new-scenario-tests-fail-before-the-change, lockstep-checks/test-first-a-missing-base-revision-is-reported-not-crashed, lockstep-checks/test-first-tests-for-existing-behavior-are-exempt-and-counted, lockstep-checks/test-first-a-test-run-that-cannot-start-fails-the-check, lockstep-checks/test-first-a-changed-scenario-needs-a-test-that-fails-before-the-change

### Requirement: Test-first: New scenario tests fail before the change

`lockstep check test-first --base <rev>` SHALL run, against the base revision's source, every test marked
for a scenario that the current revision's specs or active changes define and the base revision's specs
and active changes do not, and exit 1 if any of them passes there.

Source: Brian, 2026-10-15: "we plan out with models and diagrams and then those are linked to tests presumablhy in a tdd way" Ported from code2-template `openspec/specs/test-first/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Test-first: Test that already passed is reported

- **GIVEN** a scenario added since the base and a test for it that passes on the base source
- **WHEN** the check runs
- **THEN** it reports the test as not proving the new behavior and exits 1

#### Scenario: Test-first: Test that failed before passes the check

- **GIVEN** a scenario added since the base and a test for it that fails on the base source
- **WHEN** the check runs
- **THEN** it exits 0

#### Scenario: Test-first: A scenario in an active change is checked

- **GIVEN** a scenario written in an active change since the base and a test for it that passes on the base source
- **WHEN** the check runs
- **THEN** it reports the test as not proving the new behavior and exits 1

#### Scenario: Test-first: Archiving a change makes no scenario new

- **GIVEN** a change, present at the base, archived since so that its scenarios moved into the specs
- **WHEN** the check runs
- **THEN** it checks none of those scenarios' tests and exits 0

#### Scenario: Test-first: Configured test folders run against the base source

- **GIVEN** `[tool.lockstep] tests` names a folder outside `tests`, and a scenario added since the base with a test there that passes on the base source
- **WHEN** the check runs
- **THEN** it runs that test against the base source, reports it as passed before and exits 1

### Requirement: Test-first: A missing base revision is reported, not crashed

`lockstep check test-first --base <rev>` SHALL, when `<rev>` does not name a commit, check nothing,
report that the base was missing, and exit 0.

Source: inferred by agent (a new repository has no origin/main yet) Ported from code2-template `openspec/specs/test-first/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Test-first: New repository without a base passes with a skip notice

- **GIVEN** a repository whose base revision `origin/main` does not exist yet
- **WHEN** the check runs
- **THEN** it reports the check as skipped because the base is missing and exits 0

### Requirement: Test-first: Tests for existing behavior are exempt and counted

The test-first check SHALL not run a test marked `req(..., existing=True)` for a scenario that is new since the base, and SHALL report how many such tests it skipped. For a scenario whose text changed since the base, `existing=True` SHALL NOT exempt a test: it is run on the base source like any other test marked for that scenario.

Source: inferred by agent (working default awaiting Brian: tests marked existing=True for behavior that already worked are not run on the base revision, so existing repositories can adopt the format) Ported from code2-template `openspec/specs/test-first/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4). The changed-scenario sentence is inferred by agent, 2026-11-17 (once the text changes, the behavior it describes is not the existing one).

#### Scenario: Test-first: Existing-behavior test is skipped and counted

- **GIVEN** a scenario added since the base and its test, marked `existing=True`, that passes on the base
- **WHEN** the check runs
- **THEN** it exits 0 and lists the test as existing

#### Scenario: Test-first: An existing-behavior mark does not exempt a changed scenario

- **GIVEN** a scenario whose text differs from the base and whose only test, marked `existing=True`, passes on the base source
- **WHEN** the check runs
- **THEN** it reports `no-failing-test` for the scenario and exits 1

### Requirement: Test-first: A test run that cannot start fails the check

`lockstep check test-first` SHALL exit 1 with a message saying pytest could not run when running the new tests on the base source produces no test report (pytest missing from Lockstep's environment, or a usage error); it SHALL NOT report the tests as not passing before.

Source: Brian, 2026-11-11, "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md); acceptance entries A2 and A3 in docs/planning/acceptance-criteria.json

#### Scenario: Test-first: Pytest that cannot run fails loudly

- **GIVEN** a new scenario with a marked test and a Python that cannot run pytest
- **WHEN** the check runs
- **THEN** it prints "pytest could not run" and exits 1

### Requirement: Test-first: A changed scenario needs a test that fails before the change

`lockstep check test-first --base <rev>` SHALL, for each scenario that both revisions define and whose text differs (runs of whitespace counting as one space; text from an active change's spec delta replacing the spec's), run every test marked for it against the base revision's source, and SHALL report `no-failing-test <scenario id>` and exit 1 when none of them fails there. It SHALL NOT check a scenario that a plan new or different from the base declares on a `Wording-only:` line, by its own ID or its requirement's. Its count line SHALL add `changed=<n>`, the number of changed scenarios checked, and `no_failing_test=<n>`.

Source: Brian, 2026-10-15: "we plan out with models and diagrams and then those are linked to tests presumablhy in a tdd way"; Brian, 2026-11-17: "the gaps relevant to that normative docuemntation need to be replanned" (code2-workspace issue 842). That one failing test is enough for a changed scenario, where every test must fail for a new one, is inferred by agent (a changed scenario keeps tests for the parts that did not change).

#### Scenario: Test-first: A changed scenario whose tests all pass on the base fails the check

- **GIVEN** a scenario whose text differs from the base and whose only test passes on the base source
- **WHEN** the check runs
- **THEN** it reports `no-failing-test` for the scenario and exits 1

#### Scenario: Test-first: One test that fails on the base is enough for a changed scenario

- **GIVEN** a scenario whose text differs from the base, with one test that passes on the base source and one that fails there
- **WHEN** the check runs
- **THEN** it exits 0

#### Scenario: Test-first: A wording-only scenario is not checked

- **GIVEN** a scenario whose text differs from the base, whose only test passes on the base source, and a plan in the same change set with `Wording-only:` listing its requirement
- **WHEN** the check runs
- **THEN** it exits 0

Tested by: tests/lockstep/checks/test_lockstep_check_test_first.py
[[[end]]]
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

from lockstep.checks.changed import change_set, compare_with, wording_only
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
    start = compare_with(root, base)  # where the branch started, so merges into base since then are not counted
    if start is None:
        return Result(skipped=f"base {base} not found")
    with tempfile.TemporaryDirectory() as tmp:
        old = Path(tmp)
        _extract(root, start, old)
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
        passed, failed, skipped = set(), set(), set()
        for case in ET.parse(report).iter("testcase"):
            path = case.get("file") or case.get("classname", "").replace(".", "/") + ".py"
            node = f"{path}::{case.get('name')}"
            tags = {child.tag for child in case} - {"system-out", "system-err"}
            if not tags:
                passed.add(node)
            elif tags == {"skipped"}:
                skipped.add(node.split("[")[0])
            else:
                failed.add(node.split("[")[0])
        result.passed_before = sorted(n for n in passed if n.split("[")[0] in set(nodes))  # new-scenario tests only
        # A changed scenario's test is evidence only when it failed or errored on the base, or was not reported
        # there at all (its file could not be imported). One whose every case passed (all parameters) or that was
        # skipped there shows nothing about the old behavior.
        passing = ({n.split("[")[0] for n in passed} | skipped) - failed
        result.no_failing_test = sorted(
            result.no_failing_test + [sid for sid, tests in changed_tests.items() if tests and set(tests) <= passing]
        )
        return result

"""Status report: each requirement's implementers, each scenario's tests and whether they passed at this revision, and the IDs each plan has still to close.

Implements: lockstep-projection/status-links-each-requirement-to-its-code-and-tests,
    lockstep-projection/status-reads-test-results-from-this-revision,
    lockstep-projection/a-plan-closes-requirement-ids-only-when-they-pass

Requirement text (generated):
    lockstep-projection/status-links-each-requirement-to-its-code-and-tests: `lockstep status` SHALL
        list, for each requirement, the symbols whose docstrings implement it, and for each
        scenario, the tests marked with its ID, recomputed from the repository on every run, as a
        table, as JSON (`--json`) or as the Markdown page (`--md`).
    lockstep-projection/status-reads-test-results-from-this-revision: `lockstep status` SHALL mark a
        scenario passing, failing or skipped only from a test-result file recorded at the current
        commit with a clean tree, and SHALL mark it `not run at this revision` otherwise.
    lockstep-projection/a-plan-closes-requirement-ids-only-when-they-pass: `lockstep status` SHALL
        read the `Closes:` line of each plan and OpenSpec change and report each listed ID that is
        unimplemented, untested or not passing as open for that plan.

"""

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

from lockstep.checks.markers import implementers, req_markers
from lockstep.checks.spec import read_plan

STATUS_PAGE = Path("docs/status.md")
RESULTS = Path(".code2check/junit.xml")
RUN = Path(".code2check/run.json")
NOT_RUN = "not run at this revision"
# Worst first: a requirement takes the first of these that any of its scenarios has.
_ORDER = ["untested", "failing", "skipped", NOT_RUN, "passing"]
CLOSES = re.compile(r"^Closes:[ \t]*(.+(?:\n[ \t]+\S.*)*)", re.MULTILINE)


@dataclass
class Row:
    """One requirement or scenario: where it is defined, what links to it, and its state."""

    where: str
    links: list[str] = field(default_factory=list)
    state: str = ""
    requirement: str = ""


@dataclass
class PlanStatus:
    """A plan or change: the IDs its `Closes:` line names and those not yet passing, with their state."""

    path: str
    closes: list[str]
    open: dict[str, str]


@dataclass
class Report:
    """The whole status: requirements, scenarios, plans, and which test results were used."""

    requirements: dict[str, Row]
    scenarios: dict[str, Row]
    plans: list[PlanStatus]
    results_valid: bool
    results_note: str

    def counts(self) -> dict[str, int]:
        """Return the numbers the RESULT line prints."""
        return {
            "requirements": len(self.requirements),
            "passing": sum(r.state == "passing" for r in self.requirements.values()),
            "scenarios": len(self.scenarios),
            "scenarios_passing": sum(s.state == "passing" for s in self.scenarios.values()),
            "not_run": sum(s.state == NOT_RUN for s in self.scenarios.values()),
            "plans": len(self.plans),
            "open": sum(len(p.open) for p in self.plans),
        }

    def as_dict(self) -> dict:
        """Return the report as plain data for `--json`."""
        return {
            "results": {"valid": self.results_valid, "note": self.results_note},
            "requirements": {k: asdict(v) for k, v in self.requirements.items()},
            "scenarios": {k: asdict(v) for k, v in self.scenarios.items()},
            "plans": [asdict(p) for p in self.plans],
            "counts": self.counts(),
        }


def _git(root: Path, *args: str) -> str:
    """Return git's output in root, or an empty string when git fails."""
    done = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 else ""


def _results(root: Path) -> tuple[dict[tuple[str, str], str] | None, str]:
    """Read the test results when they were recorded at the current commit on a clean tree.

    Args:
        root: Repository root.

    Returns:
        Outcomes keyed by (module path, test name), or None with the reason they were not used.
    """
    if not (root / RUN).exists() or not (root / RESULTS).exists():
        return None, f"no test results; run make check ({RESULTS} and {RUN})"
    run = json.loads((root / RUN).read_text())
    head = _git(root, "rev-parse", "HEAD")
    if run.get("commit") != head:
        return None, f"results are from {str(run.get('commit'))[:12]}, not the current commit {head[:12]}"
    if not run.get("clean"):
        return None, "results were recorded with uncommitted changes"
    if _git(root, "status", "--porcelain"):
        return None, "the tree has uncommitted changes since the results were recorded"
    outcomes: dict[tuple[str, str], str] = {}
    for case in ET.parse(root / RESULTS).iter("testcase"):
        key = (case.get("classname", ""), case.get("name", "").split("[")[0])
        if case.find("failure") is not None or case.find("error") is not None:
            outcome = "failing"
        elif case.find("skipped") is not None:
            outcome = "skipped"
        else:
            outcome = "passing"
        if outcomes.get(key) in (None, "passing"):
            outcomes[key] = outcome
    return outcomes, f"{RESULTS} at {head[:12]}, clean tree"


def _test_state(node: str, outcomes: dict[tuple[str, str], str]) -> str:
    """Return the outcome of a test node ID such as `tests/test_mod.py::test_works`."""
    path, name = node.split("::")
    module = path.removesuffix(".py").replace("/", ".")
    found = [o for (cls, n), o in outcomes.items() if n == name and (cls == module or cls.startswith(module + "."))]
    if not found:
        return NOT_RUN
    return min(found, key=_ORDER.index)


def plan_files(root: Path) -> list[tuple[str, list[str]]]:
    """Return (path, closed IDs) for each plan and active change that has a `Closes:` line.

    Args:
        root: Repository root.

    Returns:
        Paths relative to root, plans in `docs/plans` first, then active OpenSpec changes.
    """
    files = sorted((root / "docs" / "plans").glob("*.md"))
    files += sorted(f for f in (root / "openspec" / "changes").glob("*/proposal.md") if f.parts[-3] != "archive")
    found = []
    for path in files:
        m = CLOSES.search(path.read_text())
        if m:
            ids = [i.strip() for i in m.group(1).replace("\n", " ").split(",") if i.strip()]
            found.append((str(path.relative_to(root)), ids))
    return found


def report(root: Path, use_results: bool = True) -> Report:
    """Compute the status of every requirement, scenario and plan from the repository as it is now.

    Args:
        root: Repository root.
        use_results: Read recorded test results; when false, every tested scenario is not run.

    Returns:
        The report; nothing is read from a stored status.
    """
    plan = read_plan(root)
    pending = read_plan(root, changes=True)
    outcomes, note = _results(root) if use_results else (None, "tests not run at this revision (coverage only)")
    requirements = {i: Row(w) for i, w in {**plan.requirements, **pending.requirements}.items()}
    parents = {**plan.parent, **pending.parent}
    scenarios = {i: Row(w, requirement=parents.get(i, "")) for i, w in {**plan.scenarios, **pending.scenarios}.items()}
    for ident, _, symbol in implementers(root):
        if ident in requirements:
            requirements[ident].links.append(symbol)
    for ident, _, node in req_markers(root):
        if ident in scenarios:
            scenarios[ident].links.append(node)
    for row in scenarios.values():
        if not row.links:
            row.state = "untested"
        elif outcomes is None:
            row.state = NOT_RUN
        else:
            row.state = min((_test_state(n, outcomes) for n in row.links), key=_ORDER.index)
    for ident, row in requirements.items():
        states = [s.state for s in scenarios.values() if s.requirement == ident]
        if not row.links:
            row.state = "unimplemented"
        else:
            row.state = min(states, key=_ORDER.index) if states else "passing"
    plans = []
    for path, ids in plan_files(root):
        rows = {**requirements, **scenarios}
        found = {i: rows[i].state if i in rows else "unknown" for i in ids}
        plans.append(PlanStatus(path, ids, {i: s for i, s in found.items() if s != "passing"}))
    return Report(requirements, scenarios, plans, outcomes is not None, note)


def markdown(result: Report) -> str:
    """Return the report as a Markdown page: requirements, then scenarios, each with its state and links.

    Implements: lockstep-projection/the-docs-site-shows-coverage-at-its-commit

    Requirement text (generated):
        lockstep-projection/the-docs-site-shows-coverage-at-its-commit: `lockstep check project`
            SHALL write `docs/status.md` in a repository with a `docs/` folder and recognized
            OpenSpec requirements, listing every requirement and scenario with the state `lockstep
            status` gives when no test run is recorded, and `--check` SHALL fail when the page is
            stale.


    Args:
        result: The report to show.

    Returns:
        The page text.
    """

    def cell(links: list[str]) -> str:
        """Return links as code spans joined by commas, or a dash."""
        return ", ".join(f"`{x}`" for x in links) or "-"

    lines = [
        "# Requirement status",
        "",
        "<!-- generated by `lockstep check project`; do not edit -->",
        "",
        f"Test results: {result.results_note}. This page shows which code implements each requirement and",
        "which tests cover each scenario at this commit. For pass or fail, run `make check`, then",
        "`lockstep status`.",
        "",
        "| Requirement | State | Implemented by |",
        "| --- | --- | --- |",
    ]
    lines += [f"| `{i}` | {r.state} | {cell(r.links)} |" for i, r in result.requirements.items()]
    lines += ["", "| Scenario | Requirement | State | Tests |", "| --- | --- | --- | --- |"]
    lines += [f"| `{i}` | `{s.requirement}` | {s.state} | {cell(s.links)} |" for i, s in result.scenarios.items()]
    return "\n".join(lines) + "\n"

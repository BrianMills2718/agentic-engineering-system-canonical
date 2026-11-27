"""Status report: each requirement's implementers, each scenario's tests and whether they passed at this revision, and the IDs each plan has still to close.

Implements: lockstep-projection/status-links-each-requirement-to-its-code-and-tests,
    lockstep-projection/status-reads-test-results-from-this-revision,
    lockstep-projection/a-plan-closes-requirement-ids-only-when-they-pass

Requirement text (generated):
    lockstep-projection/status-links-each-requirement-to-its-code-and-tests: `lockstep status` SHALL
        list, for each requirement, the symbols whose docstrings implement it with each symbol's
        `file:line`, and for each scenario, the tests marked with its ID, recomputed from the
        repository on every run, as a table, as JSON (`--json`) or as the Markdown page (`--md`).
        `lockstep check project` SHALL write `docs/links.json` in a repository with a `docs/` folder
        and recognized OpenSpec requirements: a `version` and a list of `nodes`, each with `id`,
        `type` (`capability`, `requirement`, `scenario`, `test`, `file`, `symbol`, `plan`, `quote`
        or `decision`), `title`, `file`, `line` and `links` (the IDs of the nodes it points to:
        capability to its requirements, requirement to its scenarios and implementing symbols,
        scenario to its tests, symbol and test to their file, plan to the IDs on its `Closes:` line,
        quote to the ID in its `lockstep quote` marker, decision to the files, folders, requirements
        and capabilities its `Governs:` line names), and `--check` SHALL not report the file when
        git ignores it. A `plan` node SHALL be written for each plan in `docs/plans/` and each
        active or archived OpenSpec change proposal with a `Closes:` line, with `state` `active` or
        `archived`; a `quote` node, with ID `<file>:<line>`, for each quote marker, with `state`
        from the trace check; an ID either names that no node has SHALL be listed in its `unknown`
        field, not in `links`. Each requirement node SHALL carry `source`, the text of its `Source:`
        line, and `source_kind`, as the sources check classifies it. A `decision` node, with ID
        `decision/<file stem>`, SHALL be written for each record in `docs/decisions/`, with
        `status`, `superseded_by`, `source`, `source_kind` and `governs` (every `Governs:` target as
        written); a path target SHALL also be a `file` node.
    lockstep-projection/status-reads-test-results-from-this-revision: `lockstep status` SHALL mark a
        scenario passing, failing or skipped only from a test-result file recorded at the current
        commit with a clean tree, and SHALL mark it `not run at this revision` otherwise.
    lockstep-projection/a-plan-closes-requirement-ids-only-when-they-pass: `lockstep status` SHALL
        read the `Closes:` line of each plan and OpenSpec change and report each listed ID that is
        unimplemented, untested or not passing as open for that plan. It SHALL give a requirement or
        scenario the state `changed, not archived` when an active change's spec delta holds text for
        it that differs from the spec's (runs of whitespace counting as one space), whatever its
        tests' results, and SHALL report it as open for a plan that lists it.


[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:checks:status.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-projection/status-links-each-requirement-to-its-code-and-tests, lockstep-projection/status-reads-test-results-from-this-revision, lockstep-projection/a-plan-closes-requirement-ids-only-when-they-pass, lockstep-projection/the-docs-site-shows-coverage-at-its-commit, lockstep-projection/links-show-planned-files-and-exports

### Requirement: Status links each requirement to its code and tests

`lockstep status` SHALL list, for each requirement, the symbols whose docstrings implement it with each symbol's `file:line`, and for each scenario, the tests marked with its ID, recomputed from the repository on every run, as a table, as JSON (`--json`) or as the Markdown page (`--md`). `lockstep check project` SHALL write `docs/links.json` in a repository with a `docs/` folder and recognized OpenSpec requirements: a `version` and a list of `nodes`, each with `id`, `type` (`capability`, `requirement`, `scenario`, `test`, `file`, `symbol`, `plan`, `quote` or `decision`), `title`, `file`, `line` and `links` (the IDs of the nodes it points to: capability to its requirements, requirement to its scenarios and implementing symbols, scenario to its tests, symbol and test to their file, plan to the IDs on its `Closes:` line, quote to the ID in its `lockstep quote` marker, decision to the files, folders, requirements and capabilities its `Governs:` line names), and `--check` SHALL not report the file when git ignores it. A `plan` node SHALL be written for each plan in `docs/plans/` and each active or archived OpenSpec change proposal with a `Closes:` line, with `state` `active` or `archived`; a `quote` node, with ID `<file>:<line>`, for each quote marker, with `state` from the trace check; an ID either names that no node has SHALL be listed in its `unknown` field, not in `links`. Each requirement node SHALL carry `source`, the text of its `Source:` line, and `source_kind`, as the sources check classifies it. A `decision` node, with ID `decision/<file stem>`, SHALL be written for each record in `docs/decisions/`, with `status`, `superseded_by`, `source`, `source_kind` and `governs` (every `Governs:` target as written); a path target SHALL also be a `file` node.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

Source: Brian, 2026-11-23: "isnt there like a file that has how everythign is linked to everythign else like how capabilities link to fils link to successc riteria"; plan https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/linked-chain-core-2026-11-23.md

Source: Brian, 2026-11-23: "i approve" (decision -> requirement or code links that the hook hands over, read from lines that already exist); plan https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/links-existing-lines-2026-11-23.md

#### Scenario: Status lists implementers and tests

- **GIVEN** a requirement with an implementer and a marked test
- **WHEN** `lockstep status` runs
- **THEN** both appear, and a RESULT line ends the output

#### Scenario: The link file lists the whole chain

- **GIVEN** a requirement with an implementing function and a scenario with a marked test
- **WHEN** `lockstep check project` runs
- **THEN** `docs/links.json` holds the capability, requirement, scenario, test, symbol and both files as nodes, linked capability to requirement to scenario to test, and requirement to symbol to file with its line

Source: Brian, 2026-11-23: "i approve" (reading the existing `Closes:`, `Source:` and quote lines into `links.json`); plan https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/links-existing-lines-2026-11-23.md

#### Scenario: The link file reads plans, sources and quotes

- **GIVEN** a plan and an archived change proposal with `Closes:` lines, a document with a quote marker, and a requirement with a `Source:` line
- **WHEN** `lockstep check project` runs
- **THEN** `docs/links.json` has an active and an archived `plan` node and a `quote` node linking to the IDs they name, and the requirement node carries its source and its source kind

#### Scenario: The link file lists decisions and what they govern

- **GIVEN** decision records with `Governs:` lines naming a file, a folder, a capability and a rule ID, one of them superseded
- **WHEN** `lockstep check project` runs
- **THEN** `docs/links.json` has a `decision` node for each, linking to the file, folder and capability nodes, with its status, successor, source and every target as written

### Requirement: Status reads test results from this revision

`lockstep status` SHALL mark a scenario passing, failing or skipped only from a test-result file recorded at the current commit with a clean tree, and SHALL mark it `not run at this revision` otherwise.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

#### Scenario: Results from this revision set pass and fail

- **GIVEN** results recorded at HEAD on a clean tree
- **WHEN** `lockstep status` runs
- **THEN** scenarios are passing or failing as recorded

#### Scenario: Results from another revision are not used

- **GIVEN** results recorded at an older commit
- **WHEN** `lockstep status` runs
- **THEN** scenarios are `not run at this revision`

### Requirement: A plan closes requirement ids only when they pass

`lockstep status` SHALL read the `Closes:` line of each plan and OpenSpec change and report each listed ID that is unimplemented, untested or not passing as open for that plan. It SHALL give a requirement or scenario the state `changed, not archived` when an active change's spec delta holds text for it that differs from the spec's (runs of whitespace counting as one space), whatever its tests' results, and SHALL report it as open for a plan that lists it.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows). The `changed, not archived` state: Brian, 2026-11-17: "if there is a change in the nromative docuemtnation then ... the gaps relevant to that normative docuemntation need to be replanned" (code2-workspace issue 842); its name and rule are inferred by agent.

#### Scenario: Open ids of a plan are listed

- **GIVEN** a plan closing an ID that fails and an ID that does not exist
- **WHEN** `lockstep status` runs
- **THEN** both are listed as open with their state

#### Scenario: A requirement reworded in an active change is open, not passing

- **GIVEN** a requirement with an implementer and a passing test, and an active change whose spec delta gives it a different statement and whose proposal lists it on its `Closes:` line
- **WHEN** `lockstep status` runs
- **THEN** the requirement's state is `changed, not archived` and the plan lists it as open

### Requirement: The docs site shows coverage at its commit

`lockstep check project` SHALL write `docs/status.md` in a repository with a `docs/` folder and recognized OpenSpec requirements, listing every requirement and scenario with the state `lockstep status` gives when no test run is recorded, and `--check` SHALL fail when the page is stale, except that when git ignores `docs/status.md` the page is build output and `--check` SHALL not report it.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows). Inferred by agent, 2026-11-21 (code2-template#37, clean-home milestone run): an ignored page is build output, so parallel plans do not conflict on it. Brian, 2026-11-23, "i approve" to the page staying at `docs/status.md` rather than the wiki (DESIGN.md:47), listed in back-on-design slice 3

#### Scenario: Status page lists every requirement with its coverage state

- **GIVEN** a repository with `docs/`
- **WHEN** `project` runs
- **THEN** `docs/status.md` lists every requirement and scenario with its state

#### Scenario: Stale status page fails the check

- **GIVEN** a test is added after the page was written
- **WHEN** `project --check` runs
- **THEN** it names `docs/status.md`

#### Scenario: An ignored status page is not reported stale

- **GIVEN** a repository whose `.gitignore` lists `docs/status.md`, and a test added after the page was written
- **WHEN** `project --check` runs
- **THEN** it does not name `docs/status.md`, and `project` still rewrites the page

### Requirement: Links show planned files and exports

In a repository whose `lockstep.yaml` has `layout:` rows, `docs/links.json` SHALL hold a `file` node for each row's path and a `symbol` node for each declared export, each with `state` `planned` when the file (or, for an export, the top-level function or class of that name in the file) does not exist yet and `exists` when it does. A row's `file` node SHALL link to the requirements the row implements and to its test files; an export's `symbol` node, with ID the file's module path and the export name, SHALL link to the file. An implementer found in a comment line (no Python symbol) SHALL link its requirement to the `file` node directly.

Source: Brian, 2026-11-23: "i approve", item (c) of `https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/back-on-design-2026-11-23.md`; `docs/architecture/LOCKSTEP.md:23-26` (requirement, file and symbol are one chain); plan `https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/template-layout-2026-11-23.md`, step 4.

#### Scenario: A planned file that does not exist yet is shown as planned

- **GIVEN** a layout row for `src/pkg/new.py` implementing `core/do-the-thing`, with tests `tests/test_new.py` and export `make() -> int`, and no such file
- **WHEN** the links are built
- **THEN** node `src/pkg/new.py` has type `file`, state `planned` and links to `core/do-the-thing` and `tests/test_new.py`, and node `pkg.new.make` has type `symbol`, state `planned` and links to `src/pkg/new.py`

#### Scenario: A laid-out file with its export is shown as existing

- **GIVEN** the same row and `src/pkg/new.py` defining `def make() -> int`
- **WHEN** the links are built
- **THEN** both nodes have state `exists`

Tested by: tests/lockstep/checks/test_lockstep_check_links.py, tests/lockstep/checks/test_lockstep_check_status.py, tests/lockstep/checks/test_lockstep_check_status_page.py, tests/lockstep/test_lockstep_decisions.py
[[[end]]]
"""

from collections.abc import Callable
from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

from lockstep.checks.markers import implementers, req_markers
from lockstep.checks.spec import Plan, normal, read_plan

STATUS_PAGE = Path("docs/status.md")
LINKS_FILE = Path("docs/links.json")
RESULTS = Path(".code2check/junit.xml")
RUN = Path(".code2check/run.json")
NOT_RUN = "not run at this revision"
CHANGED = "changed, not archived"
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
    files: list[str] = field(default_factory=list)  # `file:line` of each link, in the same order


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
        if key not in outcomes or _ORDER.index(outcome) < _ORDER.index(outcomes[key]):  # keep the worst case
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


def _changed_in_delta(plan: Plan, pending: Plan) -> set[str]:
    """IDs the specs and an active delta both define with different text.

    A requirement counts when its statement differs or its scenarios differ (set or text); a scenario
    when its text differs. A requirement under `## REMOVED Requirements` is not counted: it is removed, not
    reworded. Runs of whitespace count as one space.
    """
    found = {
        s for s in set(plan.scenarios) & set(pending.scenarios)
        if normal(plan.scenario_text.get(s, "")) != normal(pending.scenario_text.get(s, ""))
    }
    for ident in (set(plan.requirements) & set(pending.requirements)) - set(pending.removed):
        old = {s for s, p in plan.parent.items() if p == ident}
        new = {s for s, p in pending.parent.items() if p == ident}
        if normal(plan.text.get(ident, "")) != normal(pending.text.get(ident, "")) or old != new or old & found:
            found.add(ident)
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
    for ident, where, symbol in implementers(root):
        if ident in requirements:
            requirements[ident].links.append(symbol)
            requirements[ident].files.append(where)
    for ident, where, node in req_markers(root):
        if ident in scenarios:
            scenarios[ident].links.append(node)
            scenarios[ident].files.append(where)
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
    for ident in _changed_in_delta(plan, pending):  # overrides the state from links and tests
        (requirements.get(ident) or scenarios[ident]).state = CHANGED
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
            stale, except that when git ignores `docs/status.md` the page is build output and
            `--check` SHALL not report it.


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
    def placed(row: Row) -> str:
        """Return each implementing symbol with its `file:line`, or a dash."""
        return ", ".join(f"`{s}` (`{w}`)" for s, w in zip(row.links, row.files)) or "-"

    lines += [f"| `{i}` | {r.state} | {placed(r)} |" for i, r in result.requirements.items()]
    lines += ["", "| Scenario | Requirement | State | Tests |", "| --- | --- | --- | --- |"]
    lines += [f"| `{i}` | `{s.requirement}` | {s.state} | {cell(s.links)} |" for i, s in result.scenarios.items()]
    return "\n".join(lines) + "\n"


def links(result: Report, root: Path | None = None) -> dict:
    """Return the link file: every capability, requirement, scenario, test, symbol and file, and what each points to.

    Implements: lockstep-projection/status-links-each-requirement-to-its-code-and-tests

    Requirement text (generated):
        lockstep-projection/status-links-each-requirement-to-its-code-and-tests: `lockstep status`
            SHALL list, for each requirement, the symbols whose docstrings implement it with each
            symbol's `file:line`, and for each scenario, the tests marked with its ID, recomputed
            from the repository on every run, as a table, as JSON (`--json`) or as the Markdown page
            (`--md`). `lockstep check project` SHALL write `docs/links.json` in a repository with a
            `docs/` folder and recognized OpenSpec requirements: a `version` and a list of `nodes`,
            each with `id`, `type` (`capability`, `requirement`, `scenario`, `test`, `file`,
            `symbol`, `plan`, `quote` or `decision`), `title`, `file`, `line` and `links` (the IDs
            of the nodes it points to: capability to its requirements, requirement to its scenarios
            and implementing symbols, scenario to its tests, symbol and test to their file, plan to
            the IDs on its `Closes:` line, quote to the ID in its `lockstep quote` marker, decision
            to the files, folders, requirements and capabilities its `Governs:` line names), and
            `--check` SHALL not report the file when git ignores it. A `plan` node SHALL be written
            for each plan in `docs/plans/` and each active or archived OpenSpec change proposal with
            a `Closes:` line, with `state` `active` or `archived`; a `quote` node, with ID
            `<file>:<line>`, for each quote marker, with `state` from the trace check; an ID either
            names that no node has SHALL be listed in its `unknown` field, not in `links`. Each
            requirement node SHALL carry `source`, the text of its `Source:` line, and
            `source_kind`, as the sources check classifies it. A `decision` node, with ID
            `decision/<file stem>`, SHALL be written for each record in `docs/decisions/`, with
            `status`, `superseded_by`, `source`, `source_kind` and `governs` (every `Governs:`
            target as written); a path target SHALL also be a `file` node.

    Args:
        result: The report to read the links from.
        root: Repository root; when given, the link lines the repository already writes are read too: plans
            and change proposals with a `Closes:` line (active and archived), `lockstep quote` markers, and each
            requirement's `Source:` line.

    Returns:
        `{"version": 1, "nodes": [...]}`; each node has id, type, title, file, line and links (node IDs).
        The node shape follows sphinx-needs `needs.json`, so other tools can read it. Links go only to nodes in
        the file; an ID a plan or quote names that no node has is listed in that node's `unknown`.
    """
    nodes: dict[str, dict] = {}

    def node(ident: str, kind: str, file: str = "", line: int | None = None) -> dict:
        title = ident.rsplit("/", 1)[-1].rsplit("::", 1)[-1].rsplit(".", 1)[-1].replace("-", " ")
        return nodes.setdefault(ident, {"id": ident, "type": kind, "title": title, "file": file, "line": line,
                                        "links": []})

    def link(source: dict, target: str) -> None:
        if target not in source["links"]:
            source["links"].append(target)

    def place(where: str) -> tuple[str, int | None]:
        path, _, number = where.rpartition(":")
        return (path, int(number)) if number.isdigit() else (where, None)

    for ident, row in result.requirements.items():
        capability = ident.split("/", 1)[0]
        link(node(capability, "capability", row.where), ident)
        requirement = node(ident, "requirement", row.where)
        for symbol, where in zip(row.links, row.files):
            path, line = place(where)
            if symbol == path:  # a comment-line implementer has no Python symbol: link the file itself
                link(requirement, path)
                node(path, "file", path)
                continue
            link(requirement, symbol)
            link(node(symbol, "symbol", path, line), path)
            node(path, "file", path)
    for ident, row in result.scenarios.items():
        scenario = node(ident, "scenario", row.where)
        if row.requirement:
            link(node(row.requirement, "requirement", row.where), ident)
        for test, where in zip(row.links, row.files):
            path, line = place(where)
            link(scenario, test)
            link(node(test, "test", path, line), path)
            node(path, "file", path)
    if root is not None:
        _existing_lines(Path(root), nodes, node)
        _layout_nodes(Path(root), node, link)
    return {"version": 1, "nodes": list(nodes.values())}


def _layout_nodes(root: Path, node: Callable[..., dict], link: Callable[[dict, str], None]) -> None:
    """Add a `file` node per `lockstep.yaml` layout row and a `symbol` node per export, each `planned` or `exists`.

    Implements: lockstep-projection/links-show-planned-files-and-exports

    Requirement text (generated):
        lockstep-projection/links-show-planned-files-and-exports: In a repository whose
            `lockstep.yaml` has `layout:` rows, `docs/links.json` SHALL hold a `file` node for each
            row's path and a `symbol` node for each declared export, each with `state` `planned`
            when the file (or, for an export, the top-level function or class of that name in the
            file) does not exist yet and `exists` when it does. A row's `file` node SHALL link to
            the requirements the row implements and to its test files; an export's `symbol` node,
            with ID the file's module path and the export name, SHALL link to the file. An
            implementer found in a comment line (no Python symbol) SHALL link its requirement to the
            `file` node directly.
    """
    import ast

    from lockstep.checks.markers import source_dirs
    from lockstep.layout_plan import layout_rows

    for row in layout_rows(root):
        path = row["path"]
        target = root / path
        file_node = node(path, "file", path)
        file_node["state"] = "exists" if target.is_file() else "planned"
        for ident in row["implements"] + row["tests"]:
            link(file_node, ident)
        defined: set[str] = set()
        if target.is_file() and path.endswith(".py"):
            try:
                tree = ast.parse(target.read_text())
                defined = {n.name for n in tree.body
                           if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
            except SyntaxError:
                pass
        folder = next((d for d in source_dirs(root) if target.is_relative_to(d)), root)
        parts = list(target.relative_to(folder).with_suffix("").parts)
        module = ".".join(parts[:-1] if parts and parts[-1] == "__init__" else parts)
        for export in row["exports"]:
            name = export.split("(", 1)[0].split(":", 1)[0].strip()
            symbol = node(f"{module}.{name}" if module else name, "symbol", path)
            symbol["state"] = "exists" if name in defined else "planned"
            link(symbol, path)


def _existing_lines(root: Path, nodes: dict[str, dict], node) -> None:
    """Add plan and quote nodes and requirement sources from the lines the repository already writes."""
    from lockstep.checks import config, quotes, sources

    def point(source: dict, ids: list[str]) -> None:
        for ident in ids:
            target = source["links"] if ident in nodes and nodes[ident]["type"] != "plan" else source["unknown"]
            if ident not in target:
                target.append(ident)

    archived = sorted((root / "openspec" / "changes" / "archive").glob("*/proposal.md"))
    found = [(rel, ids, "active") for rel, ids in plan_files(root)]
    for path in archived:
        m = CLOSES.search(path.read_text())
        if m:
            ids = [i.strip() for i in m.group(1).replace("\n", " ").split(",") if i.strip()]
            found.append((str(path.relative_to(root)), ids, "archived"))
    for rel, ids, state in found:
        plan = node(rel, "plan", rel)
        plan.update(type="plan", state=state, unknown=[])
        point(plan, ids)
    for q in quotes.check(root):
        quote = node(f"{q.path}:{q.line}", "quote", q.path, q.line)
        quote.update(state=q.state, unknown=[])
        point(quote, [q.id])
    try:
        pattern = config.load(root).human_pattern
    except Exception:  # a broken lockstep.yaml is the config check's finding, not the link file's
        pattern = sources.DEFAULT_HUMAN_PATTERN
    for item in sources.check(root, pattern):
        if item.id in nodes and nodes[item.id]["type"] == "requirement":
            nodes[item.id].update(source=item.text, source_kind=item.source)
    from lockstep import decisions

    known = {i for i, n in nodes.items() if n["type"] in ("requirement", "capability")}
    for d in decisions.read(root, known, pattern):
        decision = node(d.id, "decision", d.file)
        decision.update(type="decision", title=d.title, status=d.status, superseded_by=d.superseded_by,
                        source=d.source, source_kind=d.source_kind, governs=d.raw, unknown=[])
        for target in d.paths:
            node(target, "file", target.rstrip("/"))
        point(decision, d.paths + d.ids)

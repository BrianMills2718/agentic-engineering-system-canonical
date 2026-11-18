"""Changed check: requirements whose text differs from a base revision, with their code, tests and plan.

Implements: lockstep-checks/changed-requirements-that-differ-from-the-base-are-listed-with-their-code-and-tests,
    lockstep-checks/changed-every-listed-requirement-is-named-by-a-plan-in-the-same-change-set,
    lockstep-checks/changed-a-changed-statement-needs-a-changed-scenario-or-a-wording-only-declaration,
    lockstep-checks/changed-count-line-and-exit-status,
    lockstep-checks/changed-documents-that-quote-a-listed-requirement-are-listed-with-it,
    lockstep-checks/changed-every-plan-that-names-a-listed-requirement-states-its-size

Requirement text (generated):
    lockstep-checks/changed-requirements-that-differ-from-the-base-are-listed-with-their-code-and-tests:
        `lockstep check changed --base <rev>` SHALL compare the text of every requirement and
        scenario in the plan at the current revision (`openspec/specs/` with the spec deltas of
        active changes applied over it) with the plan at the base revision, treating runs of
        whitespace as one space. It SHALL print, for each requirement that is new, removed, or whose
        statement or any scenario is new, removed or different: the requirement ID and its kind
        (`new`, `changed` or `removed`), which parts differ, the symbols whose docstrings implement
        it, the tests marked for its scenarios, each labelled `changed`, `unchanged` or `new`
        against the base revision's copy of that test function, and the plan that names it. `--json`
        SHALL print the same as JSON. It SHALL read the base revision from git without changing the
        working tree.
    lockstep-checks/changed-every-listed-requirement-is-named-by-a-plan-in-the-same-change-set: The
        changed check SHALL report a listed requirement as `unplanned` and exit 1 when no plan that
        is new or different from the base revision names it. A plan names a requirement when it is
        an OpenSpec change (active, or archived since the base) whose spec delta has a heading for
        that requirement, or a page in `docs/plans/` or an OpenSpec change's `proposal.md` whose
        `Closes:` or `Wording-only:` line lists the requirement ID.
    lockstep-checks/changed-a-changed-statement-needs-a-changed-scenario-or-a-wording-only-declaration:
        The changed check SHALL report `no-scenario-changed` and exit 1 when a requirement's
        statement differs from the base while none of its scenarios is new or different, unless a
        plan that is new or different from the base lists the requirement ID on a `Wording-only:`
        line. It SHALL print each wording-only declaration it accepted with the plan's path, and
        count them in its count line. A `Wording-only:` line MAY list scenario IDs as well as
        requirement IDs; a requirement ID covers its statement and all its scenarios.
    lockstep-checks/changed-count-line-and-exit-status: The changed check SHALL end with the line
        `RESULT changed requirements=<n> unplanned=<n> no_scenario=<n> wording_only=<n> small=<n>
        full=<n> no_plan_size=<n> no_planning_package=<n> exit=<0|1>`, exiting 1 when `unplanned`,
        `no_scenario`, `no_plan_size` or `no_planning_package` is above zero. `small` and `full`
        SHALL count the listed requirements of each size. When `<rev>` does not name a commit it
        SHALL check nothing, print `RESULT changed skipped="base <rev> not found" exit=0` and exit
        0. `changed` SHALL be a check name in `lockstep.yaml` with the same `block`, `warn` and
        `off` modes as the other checks.
    lockstep-checks/changed-documents-that-quote-a-listed-requirement-are-listed-with-it: The
        changed check SHALL print, for each requirement it lists, every marked quote of it (`<!--
        lockstep quote: <id> -->` in a tracked Markdown file outside `openspec/`) as `<path>:<line>`
        with the label `current` when the passage appears in the requirement's or its scenarios'
        current text and `stale` when it does not, and SHALL include them in its JSON output.
    lockstep-checks/changed-every-plan-that-names-a-listed-requirement-states-its-size: The changed
        check SHALL read, in each plan that names a listed requirement, every line `Plan size:
        small` or `Plan size: full` that stands outside a fenced code block: in the `proposal.md` of
        an OpenSpec change, or in the page itself for a page in `docs/plans/`. A listed
        requirement's size SHALL be `full` when any plan naming it says `full`, otherwise `small`
        when one says `small`. The check SHALL report `no-plan-size` and exit 1 for a listed
        requirement that a plan names when no plan naming it gives a size, and the finding SHALL
        name the file the line belongs in. For a requirement whose size is `full` it SHALL report
        `no-planning-package` and exit 1 unless a plan naming it has, outside a fenced code block, a
        line `Planning package: <path>` (the path with or without backticks) whose path is a file in
        the repository. It SHALL print each listed requirement's size in its text block and include
        it in its JSON output. A requirement reported `unplanned` SHALL get no size finding.

Nothing is stored: "changed" is computed on every run from the two revisions. The base is read with
`git archive` of `openspec/`, `docs/plans/` and the test files the listed requirements need, into a
temporary folder; the working tree is not touched and no test is run.
"""

import ast
from dataclasses import asdict, dataclass, field
import io
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile

from lockstep.checks import quotes
from lockstep.checks.markers import implementers, req_markers
from lockstep.checks.spec import Plan, effective_plan, normal, slug
from lockstep.checks.status import CLOSES

# Same grammar as `Closes:`: IDs separated by commas, continued on indented lines.
WORDING_ONLY = re.compile(r"^Wording-only:[ \t]*(.+(?:\n[ \t]+\S.*)*)", re.MULTILINE)
_REQUIREMENT = re.compile(r"^###\s+Requirement:\s*(.+?)\s*$", re.MULTILINE)
PLAN_PATHS = ("openspec", "docs/plans")
# The size line `ship` already reads in docs/plans pages, with the value `full` added.
PLAN_SIZE = re.compile(r"^Plan size:[ \t]*(small|full)[ \t]*$", re.MULTILINE)
# The pointer line Company Planning's plan check reads (method_conformance/planning_package.py, LINE_RE).
PLANNING_PACKAGE = re.compile(r"^(?:\*\*)?Planning package:(?:\*\*)?[ \t]+`?(?P<path>[^`\s]+)`?[ \t]*$", re.MULTILINE)
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def outside_fences(text: str) -> str:
    """Return text with the lines inside fenced code blocks (and the fence lines) blanked."""
    kept, fence = [], ""
    for line in text.splitlines():
        m = _FENCE.match(line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not line.strip(" `~"):
                fence = ""
            kept.append("")
        elif m:
            fence = m.group(1)
            kept.append("")
        else:
            kept.append(line)
    return "\n".join(kept)


@dataclass
class ChangePlan:
    """A plan in the change set: an OpenSpec change folder or a `docs/plans` page, and the IDs it names."""

    path: str
    names: set[str] = field(default_factory=set)
    wording_only: list[str] = field(default_factory=list)
    declared_in: str = ""
    sizes: set[str] = field(default_factory=set)  # `small` and/or `full`, read outside fenced code blocks
    packages: list[str] = field(default_factory=list)  # paths on `Planning package:` lines

    def read_size(self, text: str) -> None:
        """Record the `Plan size:` values and `Planning package:` paths in text, outside fenced code blocks."""
        plain = outside_fences(text)
        self.sizes = {m.group(1) for m in PLAN_SIZE.finditer(plain)}
        self.packages = [m.group("path") for m in PLANNING_PACKAGE.finditer(plain)]


@dataclass
class Item:
    """One listed requirement: its kind, what differs, what links to it, its plans and its findings."""

    id: str
    kind: str
    where: str
    differs: list[str] = field(default_factory=list)
    implementers: list[str] = field(default_factory=list)
    tests: list[dict[str, str]] = field(default_factory=list)
    documents: list[dict[str, str]] = field(default_factory=list)  # marked quotes: {where, label}
    plans: list[str] = field(default_factory=list)
    findings: list[str] = field(default_factory=list)
    wording_only: str | None = None
    size: str | None = None  # `full` when any plan naming it says full, else `small` when one says small
    size_files: list[str] = field(default_factory=list)  # where the `Plan size:` line belongs
    missing_packages: list[str] = field(default_factory=list)  # `Planning package:` paths that are not files


@dataclass
class Result:
    """Every listed requirement against the base, or why nothing was checked."""

    base: str
    requirements: list[Item] = field(default_factory=list)
    skipped: str = ""
    compared: str = ""  # the commit compared with: the merge base of `base` and HEAD

    def counts(self) -> dict[str, int]:
        """Return the numbers the RESULT line prints."""
        return {
            "requirements": len(self.requirements),
            "unplanned": sum("unplanned" in i.findings for i in self.requirements),
            "no_scenario": sum("no-scenario-changed" in i.findings for i in self.requirements),
            "wording_only": sum(i.wording_only is not None for i in self.requirements),
            "small": sum(i.size == "small" for i in self.requirements),
            "full": sum(i.size == "full" for i in self.requirements),
            "no_plan_size": sum("no-plan-size" in i.findings for i in self.requirements),
            "no_planning_package": sum("no-planning-package" in i.findings for i in self.requirements),
        }

    @property
    def ok(self) -> bool:
        """True when no requirement is unplanned, changed its statement without a scenario, or lacks a size or package."""
        counts = self.counts()
        return not any(counts[k] for k in ("unplanned", "no_scenario", "no_plan_size", "no_planning_package"))

    def as_dict(self) -> dict:
        """Return the result as plain data for `--json`."""
        return {"base": self.base, "compared": self.compared,
                "requirements": [asdict(i) for i in self.requirements], "counts": self.counts()}


def _listed(text: str, pattern: re.Pattern[str]) -> list[str]:
    """Return the comma-separated IDs on the first line pattern matches in text."""
    m = pattern.search(text)
    return [i.strip() for i in m.group(1).replace("\n", " ").split(",") if i.strip()] if m else []


def _differs(path: Path, before: Path) -> bool:
    """True when the file path is absent from before or has different bytes."""
    return not before.is_file() or before.read_bytes() != path.read_bytes()


def _change(root: Path, folder: Path) -> ChangePlan:
    """Read the IDs an OpenSpec change folder names: its delta headings, `Closes:` and `Wording-only:` lines."""
    plan = ChangePlan(str(folder.relative_to(root)))
    for spec in sorted(folder.glob("specs/*/spec.md")):
        plan.names |= {f"{spec.parent.name}/{slug(m.group(1))}" for m in _REQUIREMENT.finditer(spec.read_text())}
    proposal = folder / "proposal.md"
    if proposal.is_file():
        text = proposal.read_text()
        plan.wording_only = _listed(text, WORDING_ONLY)
        plan.names |= set(_listed(text, CLOSES)) | set(plan.wording_only)
        plan.declared_in = str(proposal.relative_to(root))
        plan.read_size(text)
    else:
        plan.declared_in = str(proposal.relative_to(root))
    return plan


def change_set(root: Path, old: Path) -> list[ChangePlan]:
    """Return the plans new or different from the base revision.

    Implements: lockstep-checks/changed-every-listed-requirement-is-named-by-a-plan-in-the-same-change-set

    Requirement text (generated):
        lockstep-checks/changed-every-listed-requirement-is-named-by-a-plan-in-the-same-change-set:
            The changed check SHALL report a listed requirement as `unplanned` and exit 1 when no
            plan that is new or different from the base revision names it. A plan names a
            requirement when it is an OpenSpec change (active, or archived since the base) whose
            spec delta has a heading for that requirement, or a page in `docs/plans/` or an OpenSpec
            change's `proposal.md` whose `Closes:` or `Wording-only:` line lists the requirement ID.

    Args:
        root: Repository root (the working tree).
        old: A folder holding the base revision's `openspec/` and `docs/plans/`.

    Returns:
        Active change folders absent at base or with any file new or different; archived change
        folders absent at base; `docs/plans/*.md` pages new or different.
    """
    plans = []
    changes = root / "openspec" / "changes"
    for folder in sorted(p for p in changes.glob("*") if p.is_dir() and p.name != "archive"):
        before = old / folder.relative_to(root)
        if any(_differs(f, before / f.relative_to(folder)) for f in folder.rglob("*") if f.is_file()):
            plans.append(_change(root, folder))
    for folder in sorted(p for p in (changes / "archive").glob("*") if p.is_dir()):
        if not (old / folder.relative_to(root)).exists():
            plans.append(_change(root, folder))
    for page in sorted((root / "docs" / "plans").glob("*.md")):
        if _differs(page, old / page.relative_to(root)):
            text = page.read_text()
            wording = _listed(text, WORDING_ONLY)
            rel = str(page.relative_to(root))
            plan = ChangePlan(rel, set(_listed(text, CLOSES)) | set(wording), wording, rel)
            plan.read_size(text)
            plans.append(plan)
    return plans


def wording_only(plans: list[ChangePlan]) -> dict[str, str]:
    """Map each requirement or scenario ID declared `Wording-only:` by a plan to the file declaring it."""
    declared: dict[str, str] = {}
    for plan in plans:
        for ident in plan.wording_only:
            declared.setdefault(ident, plan.declared_in)
    return declared


def base_exists(root: Path, base: str) -> bool:
    """True when base names a commit in the repository at root."""
    found = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--verify", "--quiet", f"{base}^{{commit}}"], capture_output=True
    )
    return found.returncode == 0


def compare_with(root: Path, base: str) -> str | None:
    """Return the commit a check compares with: where the branch started.

    Implements: lockstep-checks/changed-and-test-first-the-base-is-where-the-branch-started

    Requirement text (generated):
        lockstep-checks/changed-and-test-first-the-base-is-where-the-branch-started: `lockstep check
            changed --base <rev>` and `lockstep check test-first --base <rev>` SHALL compare the
            current revision with the merge base of `<rev>` and the current commit, so that what was
            merged into `<rev>` after the branch started is not counted as this branch's change.
            When `<rev>` and the current commit share no history, or the repository has no commit
            yet, they SHALL compare with `<rev>` itself.

    Args:
        root: Repository root.
        base: Git revision given as `--base`, such as `origin/main`.

    Returns:
        The merge base of base and HEAD; base itself when they share no history or there is no
        commit yet; None when base names no commit.
    """
    if not base_exists(root, base):
        return None
    found = subprocess.run(["git", "-C", str(root), "merge-base", base, "HEAD"], capture_output=True, text=True)
    return found.stdout.strip() if found.returncode == 0 and found.stdout.strip() else base


def extract(root: Path, base: str, dest: Path, paths: list[str]) -> None:
    """Unpack the given paths of revision base into dest, skipping those absent at base.

    Args:
        root: Repository root.
        base: Git revision.
        dest: Folder to unpack into.
        paths: Files or folders relative to the repository root.
    """
    if not paths:
        return
    listed = subprocess.run(
        ["git", "-C", str(root), "ls-tree", "-r", "-z", "--name-only", "--full-tree", base, "--", *paths],
        check=True, capture_output=True,
    ).stdout.decode().split("\0")
    present = [p for p in paths if any(f == p or f.startswith(p.rstrip("/") + "/") for f in listed)]
    if not present:
        return
    archive = subprocess.run(
        ["git", "-C", str(root), "archive", base, "--", *present], check=True, capture_output=True
    ).stdout
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(dest, filter="data")


def _function_source(path: Path, name: str) -> str | None:
    """Return the source of the first function called name in path, decorators included, or None."""
    if not path.is_file():
        return None
    text = path.read_text()
    lines = text.splitlines()
    for node in ast.walk(ast.parse(text, filename=str(path))):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            start = min([d.lineno for d in node.decorator_list] + [node.lineno])
            return "\n".join(lines[start - 1: node.end_lineno])
    return None


def _compare(before: Plan, now: Plan) -> list[tuple[str, str, str, bool, list[tuple[str, str]]]]:
    """Return (ID, kind, where, statement differs, [(scenario ID, label)]) for each requirement that differs."""
    found = []
    for ident in sorted(set(before.requirements) | set(now.requirements)):
        old_sc = {s: normal(before.scenario_text.get(s, "")) for s, p in before.parent.items() if p == ident}
        new_sc = {s: normal(now.scenario_text.get(s, "")) for s, p in now.parent.items() if p == ident}
        scenarios = [(s, "new") for s in sorted(set(new_sc) - set(old_sc))]
        scenarios += [(s, "removed") for s in sorted(set(old_sc) - set(new_sc))]
        scenarios += [(s, "changed") for s in sorted(set(old_sc) & set(new_sc)) if old_sc[s] != new_sc[s]]
        if ident not in before.requirements:
            found.append((ident, "new", now.requirements[ident], True, scenarios))
        elif ident not in now.requirements:
            found.append((ident, "removed", before.requirements[ident], True, scenarios))
        else:
            statement = normal(before.text.get(ident, "")) != normal(now.text.get(ident, ""))
            if statement or scenarios:
                found.append((ident, "changed", now.requirements[ident], statement, scenarios))
    return found


def _size(root: Path, item: Item, naming: list[ChangePlan]) -> None:
    """Set item's size from the plans naming it, with `no-plan-size` or `no-planning-package` when due.

    Implements: lockstep-checks/changed-every-plan-that-names-a-listed-requirement-states-its-size

    Requirement text (generated):
        lockstep-checks/changed-every-plan-that-names-a-listed-requirement-states-its-size: The
            changed check SHALL read, in each plan that names a listed requirement, every line `Plan
            size: small` or `Plan size: full` that stands outside a fenced code block: in the
            `proposal.md` of an OpenSpec change, or in the page itself for a page in `docs/plans/`.
            A listed requirement's size SHALL be `full` when any plan naming it says `full`,
            otherwise `small` when one says `small`. The check SHALL report `no-plan-size` and exit
            1 for a listed requirement that a plan names when no plan naming it gives a size, and
            the finding SHALL name the file the line belongs in. For a requirement whose size is
            `full` it SHALL report `no-planning-package` and exit 1 unless a plan naming it has,
            outside a fenced code block, a line `Planning package: <path>` (the path with or without
            backticks) whose path is a file in the repository. It SHALL print each listed
            requirement's size in its text block and include it in its JSON output. A requirement
            reported `unplanned` SHALL get no size finding.

    Args:
        root: Repository root.
        item: A listed requirement that at least one plan names.
        naming: The plans in the change set that name it.
    """
    sizes = set().union(*(p.sizes for p in naming))
    item.size = "full" if "full" in sizes else ("small" if "small" in sizes else None)
    if item.size is None:
        item.findings.append("no-plan-size")
        item.size_files = sorted({p.declared_in for p in naming})
        return
    if item.size == "full":
        paths = [path for p in naming for path in p.packages]
        if not any((root / path).is_file() for path in paths):
            item.findings.append("no-planning-package")
            item.missing_packages = sorted(set(paths))


def check(root: Path, base: str) -> Result:
    """List every requirement that is new, removed or changed since base, with its links, plans and findings.

    Implements: lockstep-checks/changed-requirements-that-differ-from-the-base-are-listed-with-their-code-and-tests,
        lockstep-checks/changed-a-changed-statement-needs-a-changed-scenario-or-a-wording-only-declaration

    Requirement text (generated):
        lockstep-checks/changed-requirements-that-differ-from-the-base-are-listed-with-their-code-and-tests:
            `lockstep check changed --base <rev>` SHALL compare the text of every requirement and
            scenario in the plan at the current revision (`openspec/specs/` with the spec deltas of
            active changes applied over it) with the plan at the base revision, treating runs of
            whitespace as one space. It SHALL print, for each requirement that is new, removed, or
            whose statement or any scenario is new, removed or different: the requirement ID and its
            kind (`new`, `changed` or `removed`), which parts differ, the symbols whose docstrings
            implement it, the tests marked for its scenarios, each labelled `changed`, `unchanged`
            or `new` against the base revision's copy of that test function, and the plan that names
            it. `--json` SHALL print the same as JSON. It SHALL read the base revision from git
            without changing the working tree.
        lockstep-checks/changed-a-changed-statement-needs-a-changed-scenario-or-a-wording-only-declaration:
            The changed check SHALL report `no-scenario-changed` and exit 1 when a requirement's
            statement differs from the base while none of its scenarios is new or different, unless
            a plan that is new or different from the base lists the requirement ID on a
            `Wording-only:` line. It SHALL print each wording-only declaration it accepted with the
            plan's path, and count them in its count line. A `Wording-only:` line MAY list scenario
            IDs as well as requirement IDs; a requirement ID covers its statement and all its
            scenarios.

    Args:
        root: Repository root (the working tree, uncommitted edits included).
        base: Git revision to compare with, such as `origin/main`.

    Returns:
        The result; `skipped` says why when base is not a commit.
    """
    root = Path(root)
    start = compare_with(root, base)
    if start is None:
        return Result(base, skipped=f"base {base} not found")
    now = effective_plan(root)
    result = Result(base, compared=start)
    with tempfile.TemporaryDirectory() as tmp:
        old = Path(tmp)
        extract(root, start, old, list(PLAN_PATHS))
        diffs = _compare(effective_plan(old), now)
        if not diffs:
            return result
        markers = req_markers(root)
        scenario_ids = {s for _, _, _, _, scs in diffs for s, _ in scs}
        scenario_ids |= {s for d in diffs for s, p in now.parent.items() if p == d[0]}
        needed = sorted({node.split("::")[0] for ident, _, node in markers if ident in scenario_ids})
        extract(root, start, old, needed)
        plans = change_set(root, old)
        declared = wording_only(plans)
        links = implementers(root)
        documents = quotes.check(root, [now])
        for ident, kind, where, statement, scenarios in diffs:
            item = Item(ident, kind, where)
            if kind == "changed":
                item.differs = (["statement"] if statement else []) + [f"scenario {s} ({lab})" for s, lab in scenarios]
            else:
                item.differs = [f"{kind} requirement"] + [f"scenario {s} ({lab})" for s, lab in scenarios]
            item.implementers = sorted({symbol for i, _, symbol in links if i == ident})
            own = {s for s, p in now.parent.items() if p == ident} | {s for s, _ in scenarios}
            for sid, _, node in markers:
                if sid in own:
                    path, name = node.split("::")
                    before = _function_source(old / path, name)
                    label = "new" if before is None else (
                        "unchanged" if before == _function_source(root / path, name) else "changed")
                    item.tests.append({"node": node, "scenario": sid, "label": label})
            item.documents = [{"where": f"{q.path}:{q.line}", "label": "current" if q.state == "current" else "stale"}
                              for q in documents if q.id == ident]
            naming = [p for p in plans if ident in p.names]
            item.plans = [p.path for p in naming]
            if not item.plans:
                item.findings.append("unplanned")
            else:
                _size(root, item, naming)
            item.wording_only = declared.get(ident)
            moved = any(lab in ("new", "changed") for _, lab in scenarios)
            if kind == "changed" and statement and not moved and item.wording_only is None:
                item.findings.append("no-scenario-changed")
            result.requirements.append(item)
    return result

"""Read OpenSpec spec files into requirement and scenario IDs."""

from dataclasses import dataclass, field
from pathlib import Path
import re

_HEADING = re.compile(r"^(#{3,4})\s+(Requirement|Scenario):\s*(.+?)\s*$")


def slug(name: str) -> str:
    """Turn a requirement or scenario name into its ID part.

    Args:
        name: The heading text after "Requirement:" or "Scenario:".

    Returns:
        Lowercase words joined by hyphens.
    """
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


@dataclass
class Plan:
    """Every requirement and scenario ID the specs define, each mapped to its spec file.

    `parent` maps each scenario ID to the requirement it sits under; `text` maps each requirement ID
    to its statement, the lines under its heading up to its `Source:` line or first scenario;
    `scenario_text` maps each scenario ID to the lines under its heading up to the next heading.
    `removed` lists the requirement IDs a delta puts under `## REMOVED Requirements` (they are also in
    `requirements`, as the delta's headings are).
    """

    requirements: dict[str, str] = field(default_factory=dict)
    scenarios: dict[str, str] = field(default_factory=dict)
    parent: dict[str, str] = field(default_factory=dict)
    text: dict[str, str] = field(default_factory=dict)
    scenario_text: dict[str, str] = field(default_factory=dict)
    removed: list[str] = field(default_factory=list)


def read_plan(root: Path, changes: bool = False) -> Plan:
    """Collect IDs from `openspec/specs/<capability>/spec.md` under root.

    Args:
        root: Repository root.
        changes: Read active change deltas (`openspec/changes/<name>/specs/`) instead of the specs.

    Returns:
        The plan; empty when the repository has no specs.
    """
    if changes:
        files = [f for f in (root / "openspec" / "changes").glob("*/specs/*/spec.md") if f.parts[-4] != "archive"]
    else:
        files = list((root / "openspec" / "specs").glob("*/spec.md"))
    plan = Plan()
    for spec in sorted(files):
        _read_file(root, spec, plan)
    return plan


def _read_file(root: Path, spec: Path, plan: Plan) -> None:
    """Add the requirements and scenarios of one spec or delta file to plan."""
    capability = spec.parent.name
    requirement = ""
    scenario = ""
    collecting = False
    removing = False
    for line in spec.read_text().splitlines():
        m = _HEADING.match(line)
        if not m:
            if line.startswith("## "):
                removing = line.strip().lower().startswith("## removed")
            if line.startswith("#"):
                collecting = False
                scenario = ""
            elif line.startswith("Source:"):
                collecting = False
            elif collecting and line.strip():
                plan.text[requirement] = f"{plan.text.get(requirement, '')} {line.strip()}".strip()
            if scenario and line.strip() and not line.startswith("#"):
                plan.scenario_text[scenario] = f"{plan.scenario_text.get(scenario, '')} {line.strip()}".strip()
            continue
        collecting = m.group(2) == "Requirement"
        ident = f"{capability}/{slug(m.group(3))}"
        if m.group(2) == "Requirement":
            plan.requirements[ident] = str(spec.relative_to(root))
            requirement = ident
            scenario = ""
            if removing:
                plan.removed.append(ident)
        else:
            plan.scenarios[ident] = str(spec.relative_to(root))
            plan.parent[ident] = requirement
            plan.scenario_text.setdefault(ident, "")
            scenario = ident


def normal(text: str) -> str:
    """Return text with every run of whitespace made one space, so re-wrapping is not a change."""
    return " ".join(text.split())


def effective_plan(root: Path) -> Plan:
    """Return the plan at a revision: `openspec/specs/` with each active change's spec delta applied over it.

    Implements: lockstep-checks/changed-requirements-that-differ-from-the-base-are-listed-with-their-code-and-tests

    A requirement in a delta replaces the spec's requirement entirely, scenarios included (an OpenSpec
    delta carries the whole requirement); one under `## REMOVED Requirements` is removed. Deltas apply
    in the order of their change folders' names.

    Args:
        root: Repository root (or a folder holding a revision's `openspec/`).

    Returns:
        The plan; `removed` is empty.
    """
    plan = read_plan(root)
    files = [f for f in (root / "openspec" / "changes").glob("*/specs/*/spec.md") if f.parts[-4] != "archive"]
    for spec in sorted(files):
        delta = Plan()
        _read_file(root, spec, delta)
        for req in delta.requirements:
            for sid in [s for s, p in plan.parent.items() if p == req]:
                for table in (plan.scenarios, plan.parent, plan.scenario_text):
                    table.pop(sid, None)
            for table in (plan.requirements, plan.text):
                table.pop(req, None)
            if req in delta.removed:
                continue
            plan.requirements[req] = delta.requirements[req]
            if req in delta.text:
                plan.text[req] = delta.text[req]
            for sid, parent in delta.parent.items():
                if parent == req:
                    plan.scenarios[sid] = delta.scenarios[sid]
                    plan.parent[sid] = req
                    plan.scenario_text[sid] = delta.scenario_text.get(sid, "")
    return plan

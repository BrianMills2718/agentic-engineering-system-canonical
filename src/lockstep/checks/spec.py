"""Read OpenSpec spec files into requirement and scenario IDs.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:checks:spec.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-checks/changed-requirements-that-differ-from-the-base-are-listed-with-their-code-and-tests

### Requirement: Changed: Requirements that differ from the base are listed with their code and tests

`lockstep check changed --base <rev>` SHALL compare the text of every requirement and scenario in the plan at the current revision (`openspec/specs/` with the spec deltas of active changes applied over it) with the plan at the base revision, treating runs of whitespace as one space. It SHALL print, for each requirement that is new, removed, or whose statement or any scenario is new, removed or different: the requirement ID and its kind (`new`, `changed` or `removed`), which parts differ, the symbols whose docstrings implement it, the tests marked for its scenarios, each labelled `changed`, `unchanged` or `new` against the base revision's copy of that test function, and the plan that names it. `--json` SHALL print the same as JSON. It SHALL read the base revision from git without changing the working tree.

Source: Brian, 2026-11-17: "if there is a change in the nromative docuemtnation then that normative docuemtnation gets updated and then the gaps relevant to that normative docuemntation need to be replanned" (code2-workspace issue 842; approved for build 2026-11-17, "i approve"). The output columns are inferred by agent.

#### Scenario: Changed: A reworded requirement is listed with its implementer and tests

- **GIVEN** a requirement whose statement differs from the base, with an implementing docstring and a marked test that is the same as at the base
- **WHEN** `lockstep check changed --base <rev>` runs
- **THEN** it lists the requirement as `changed`, names the implementing symbol, and labels the test `unchanged`

#### Scenario: Changed: Re-wrapped text is not a change

- **GIVEN** a requirement whose statement differs from the base only in line breaks and spacing
- **WHEN** the check runs
- **THEN** it lists nothing and exits 0

#### Scenario: Changed: A changed scenario marks its requirement changed

- **GIVEN** a requirement whose statement is the same as at the base and one of whose scenarios has different text
- **WHEN** the check runs
- **THEN** it lists the requirement as `changed` and names that scenario as the part that differs

#### Scenario: Changed: Text in an active change counts before it is archived

- **GIVEN** an active change whose spec delta gives an existing requirement a different statement
- **WHEN** the check runs
- **THEN** it lists the requirement as `changed` and names the change as its plan

#### Scenario: Changed: A test edited since the base is labelled changed

- **GIVEN** a changed requirement whose marked test function differs from the base revision's copy
- **WHEN** the check runs
- **THEN** the test is labelled `changed`

Tested by: tests/lockstep/checks/test_lockstep_check_changed.py
[[[end]]]
"""

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
    to its statement: the lines under its heading before its `Source:` line, or, when there are none,
    the lines after the `Source:` paragraph (which runs to a blank line) up to its first scenario;
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
    in_source = False  # inside a `Source:` paragraph, which runs to the next blank line
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
                in_source = True
                collecting = collecting and not plan.text.get(requirement)
            elif not line.strip():
                in_source = False
            elif collecting and not in_source:
                plan.text[requirement] = f"{plan.text.get(requirement, '')} {line.strip()}".strip()
            if scenario and line.strip() and not line.startswith("#"):
                plan.scenario_text[scenario] = f"{plan.scenario_text.get(scenario, '')} {line.strip()}".strip()
            continue
        collecting = m.group(2) == "Requirement"
        in_source = False
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

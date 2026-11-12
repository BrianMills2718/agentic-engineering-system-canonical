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
    to its statement, the lines under its heading up to its `Source:` line or first scenario.
    """

    requirements: dict[str, str] = field(default_factory=dict)
    scenarios: dict[str, str] = field(default_factory=dict)
    parent: dict[str, str] = field(default_factory=dict)
    text: dict[str, str] = field(default_factory=dict)


def read_plan(root: Path, changes: bool = False) -> Plan:
    """Collect IDs from `openspec/specs/<capability>/spec.md` under root.

    Args:
        root: Repository root.
        changes: Read active change deltas (`openspec/changes/<name>/specs/`) instead of the specs.

    Returns:
        The plan; empty when the repository has no specs.
    """
    plan = Plan()
    if changes:
        files = [f for f in (root / "openspec" / "changes").glob("*/specs/*/spec.md") if f.parts[-4] != "archive"]
    else:
        files = list((root / "openspec" / "specs").glob("*/spec.md"))
    for spec in sorted(files):
        capability = spec.parent.name
        requirement = ""
        collecting = False
        for line in spec.read_text().splitlines():
            m = _HEADING.match(line)
            if not m:
                if line.startswith("#") or line.startswith("Source:"):
                    collecting = False
                elif collecting and line.strip():
                    plan.text[requirement] = f"{plan.text.get(requirement, '')} {line.strip()}".strip()
                continue
            collecting = m.group(2) == "Requirement"
            ident = f"{capability}/{slug(m.group(3))}"
            if m.group(2) == "Requirement":
                plan.requirements[ident] = str(spec.relative_to(root))
                requirement = ident
            else:
                plan.scenarios[ident] = str(spec.relative_to(root))
                plan.parent[ident] = requirement
    return plan

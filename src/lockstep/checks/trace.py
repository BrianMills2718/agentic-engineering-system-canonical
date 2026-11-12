"""Trace check: every requirement has an implementer, every scenario a test, and no ID is unknown.

Implements: lockstep-checks/trace-every-requirement-has-an-implementer, lockstep-checks/trace-every-scenario-has-a-test,
    lockstep-checks/trace-unknown-ids-fail, lockstep-checks/trace-ids-from-changes-in-progress-are-known

Requirement text (generated):
    lockstep-checks/trace-every-requirement-has-an-implementer: The trace check SHALL fail when an OpenSpec
        requirement has no source module, class or function whose docstring contains a line
        `Implements: <capability>/<requirement-slug>`.
    lockstep-checks/trace-every-scenario-has-a-test: The trace check SHALL fail when an OpenSpec scenario has no
        test decorated with `@pytest.mark.req("<capability>/<scenario-slug>")`.
    lockstep-checks/trace-unknown-ids-fail: The trace check SHALL fail when a docstring or test marker names an ID
        that no spec defines.
    lockstep-checks/trace-ids-from-changes-in-progress-are-known: The trace check SHALL treat requirement and
        scenario IDs defined in an active change's spec delta
        (`openspec/changes/<name>/specs/<capability>/spec.md`, archive excluded) as known, and SHALL
        not require them to be implemented or tested until the change is archived.
"""

from dataclasses import dataclass
from pathlib import Path

from lockstep.checks.markers import implements, req_markers
from lockstep.checks.spec import read_plan


@dataclass(frozen=True)
class Finding:
    """One trace problem: its kind, the ID, and where it was found."""

    kind: str
    id: str
    where: str


def check(root: Path) -> list[Finding]:
    """Compare the specs with source docstrings and test markers.

    Args:
        root: Repository root.

    Returns:
        Findings, unimplemented first, then untested, then unknown; empty when everything traces.
    """
    plan = read_plan(root)
    pending = read_plan(root, changes=True)
    known_requirements = plan.requirements.keys() | pending.requirements.keys()
    known_scenarios = plan.scenarios.keys() | pending.scenarios.keys()
    impl = implements(root)
    tests = req_markers(root)
    implemented = {i for i, _ in impl}
    tested = {i for i, _, _ in tests}
    findings = [Finding("unimplemented", r, w) for r, w in plan.requirements.items() if r not in implemented]
    findings += [Finding("untested", s, w) for s, w in plan.scenarios.items() if s not in tested]
    findings += [Finding("unknown", i, w) for i, w in impl if i not in known_requirements]
    findings += [Finding("unknown", i, w) for i, w, _ in tests if i not in known_scenarios]
    return findings

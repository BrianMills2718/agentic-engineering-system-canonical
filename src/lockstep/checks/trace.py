"""Trace check: every requirement has an implementer, every scenario a test, and no ID is unknown.

Implements: lockstep-checks/trace-every-requirement-has-an-implementer, lockstep-checks/trace-every-scenario-has-a-test,
    lockstep-checks/trace-unknown-ids-fail, lockstep-checks/trace-ids-from-changes-in-progress-are-known,
    lockstep-checks/trace-a-marked-quote-matches-its-requirement

Requirement text (generated):
    lockstep-checks/trace-every-requirement-has-an-implementer: The trace check SHALL fail when an
        OpenSpec requirement has no source module, class or function whose docstring contains a line
        `Implements: <capability>/<requirement-slug>`.
    lockstep-checks/trace-every-scenario-has-a-test: The trace check SHALL fail when an OpenSpec
        scenario has no test decorated with `@pytest.mark.req("<capability>/<scenario-slug>")`.
    lockstep-checks/trace-unknown-ids-fail: The trace check SHALL fail when a docstring or test
        marker names an ID that no spec defines.
    lockstep-checks/trace-ids-from-changes-in-progress-are-known: The trace check SHALL treat
        requirement and scenario IDs defined in an active change's spec delta
        (`openspec/changes/<name>/specs/<capability>/spec.md`, archive excluded) as known, and SHALL
        not require them to be implemented or tested until the change is archived.
    lockstep-checks/trace-a-marked-quote-matches-its-requirement: The trace check SHALL read, in
        every Markdown file tracked by git outside `openspec/`, each passage between `<!-- lockstep
        quote: <requirement id> -->` and `<!-- /lockstep quote -->`. It SHALL report `stale-quote`
        and fail when the passage, with runs of whitespace counting as one space, does not appear in
        the text of that requirement or of one of its scenarios, in `openspec/specs/` or in an
        active change's spec delta. It SHALL report `unknown` when no spec or active change defines
        the ID, and `unclosed-quote` when a start marker has no end marker after it in the same
        file. Each finding SHALL name the file and line of the start marker. A marker inside a code
        span or a fenced code block is shown as code, not used as a marker, and SHALL be skipped; a
        passage SHALL be compared with its code words kept. In a folder that is not a git repository
        it SHALL read every Markdown file outside `openspec/` and folders whose name starts with a
        dot.
"""

from dataclasses import dataclass
from pathlib import Path

from lockstep.checks import quotes
from lockstep.checks.markers import implements, req_markers
from lockstep.checks.spec import read_plan

# A quote's state, other than current, and the finding it gives.
QUOTE_FINDINGS = {"stale": "stale-quote", "unknown": "unknown", "unclosed": "unclosed-quote"}


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
        Findings, unimplemented first, then untested, then unknown, then the marked quotes in
        Markdown documents (`stale-quote`, `unknown`, `unclosed-quote`, each at `<path>:<line>`);
        empty when everything traces.
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
    findings += [Finding(QUOTE_FINDINGS[q.state], q.id, f"{q.path}:{q.line}")
                 for q in quotes.check(root, [plan, pending]) if q.state != "current"]
    return findings

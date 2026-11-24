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

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:checks:trace.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-checks/trace-every-requirement-has-an-implementer, lockstep-checks/trace-every-scenario-has-a-test, lockstep-checks/trace-unknown-ids-fail, lockstep-checks/trace-ids-from-changes-in-progress-are-known, lockstep-checks/trace-a-marked-quote-matches-its-requirement

### Requirement: Trace: Every requirement has an implementer

The trace check SHALL fail when an OpenSpec requirement has no source module, class or function whose
docstring contains a line `Implements: <capability>/<requirement-slug>`.

Source: Brian, 2026-10-15: "we plan out with models and diagrams and then those are linked to tests presumablhy in a tdd way" Ported from code2-template `openspec/specs/trace/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Trace: Requirement without implementer fails

- **GIVEN** a spec with requirement "Do the thing" in capability "core"
- **WHEN** no source docstring says `Implements: core/do-the-thing`
- **THEN** the check reports `core/do-the-thing` as unimplemented and exits 1

#### Scenario: Trace: Implemented requirement passes

- **GIVEN** the same spec
- **WHEN** a source docstring says `Implements: core/do-the-thing`
- **THEN** the check reports no finding for that requirement

### Requirement: Trace: Every scenario has a test

The trace check SHALL fail when an OpenSpec scenario has no test decorated with
`@pytest.mark.req("<capability>/<scenario-slug>")`.

Source: Brian, 2026-10-15: "we plan out with models and diagrams and then those are linked to tests presumablhy in a tdd way" Ported from code2-template `openspec/specs/trace/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Trace: Scenario without test fails

- **GIVEN** a spec with scenario "It works" in capability "core"
- **WHEN** no test carries `req("core/it-works")`
- **THEN** the check reports `core/it-works` as untested and exits 1

### Requirement: Trace: Unknown IDs fail

The trace check SHALL fail when a docstring or test marker names an ID that no spec defines.

Source: inferred by agent (a marker naming no planned ID means the plan and code disagree) Ported from code2-template `openspec/specs/trace/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Trace: Stale marker fails

- **GIVEN** a test marked `req("core/renamed-away")`
- **WHEN** no spec defines that scenario
- **THEN** the check reports the unknown ID with its file and exits 1

### Requirement: Trace: IDs from changes in progress are known

The trace check SHALL treat requirement and scenario IDs defined in an active change's spec delta
(`openspec/changes/<name>/specs/<capability>/spec.md`, archive excluded) as known, and SHALL not
require them to be implemented or tested until the change is archived.

Source: inferred by agent (needed so failing tests can be committed before the spec is archived) Ported from code2-template `openspec/specs/trace/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Trace: Test written for an active change passes trace

- **GIVEN** an active change whose delta adds scenario "It also works" to capability "core"
- **WHEN** a test carries `req("core/it-also-works")` and no code implements the new requirement yet
- **THEN** the check reports no finding for either ID

### Requirement: Trace: A marked quote matches its requirement

The trace check SHALL read, in every Markdown file tracked by git outside `openspec/`, each passage between `<!-- lockstep quote: <requirement id> -->` and `<!-- /lockstep quote -->`. It SHALL report `stale-quote` and fail when the passage, with runs of whitespace counting as one space, does not appear in the text of that requirement or of one of its scenarios, in `openspec/specs/` or in an active change's spec delta. It SHALL report `unknown` when no spec or active change defines the ID, and `unclosed-quote` when a start marker has no end marker after it in the same file. Each finding SHALL name the file and line of the start marker. A marker inside a code span or a fenced code block is shown as code, not used as a marker, and SHALL be skipped; a passage SHALL be compared with its code words kept. In a folder that is not a git repository it SHALL read every Markdown file outside `openspec/` and folders whose name starts with a dot.

Source: Brian, 2026-10-22: "this doc string linkage system where the normative and docs tring stuff and gaps and planns would stay algined over time" (code2-workspace decision 0006); Brian, 2026-11-17: "if there is a change in the nromative docuemtnation ..." (code2-workspace issue 842, where seven hand-typed copies of one requirement's number stayed unchanged after the requirement changed). The marker form is inferred by agent.

#### Scenario: Trace: A quote that matches passes

- **GIVEN** a Markdown file with a marked passage that appears word for word in its requirement's statement
- **WHEN** the trace check runs
- **THEN** it reports no finding for the passage

#### Scenario: Trace: A quote left behind by a changed requirement fails

- **GIVEN** the same file after the requirement's statement changed so that the passage no longer appears in it
- **WHEN** the trace check runs
- **THEN** it reports `stale-quote` with the file and line, and exits 1

#### Scenario: Trace: A quote of a scenario's text passes

- **GIVEN** a marked passage that appears in the text of one of the requirement's scenarios
- **WHEN** the trace check runs
- **THEN** it reports no finding for the passage

#### Scenario: Trace: A quote of an unknown requirement fails

- **GIVEN** a marked passage naming an ID no spec defines
- **WHEN** the trace check runs
- **THEN** it reports `unknown` for the passage and exits 1

#### Scenario: Trace: A quote matching an active change's text passes

- **GIVEN** a marked passage that appears only in an active change's spec delta for that requirement
- **WHEN** the trace check runs
- **THEN** it reports no finding for the passage

#### Scenario: Trace: A start marker with no end marker fails

- **GIVEN** a Markdown file with a start marker and no end marker after it
- **WHEN** the trace check runs
- **THEN** it reports `unclosed-quote` with the file and line, and exits 1

#### Scenario: Trace: A marker written as code is not a quote

- **GIVEN** a Markdown file that shows the marker inside backticks and inside a fenced block
- **WHEN** the trace check runs
- **THEN** it reports no finding for those lines

#### Scenario: Trace: A quoted passage keeps its code words

- **GIVEN** a marked passage containing a backticked command that appears in its requirement's statement
- **WHEN** the trace check runs
- **THEN** it reports no finding for the passage

Tested by: tests/lockstep/checks/test_lockstep_check_quotes.py, tests/lockstep/checks/test_lockstep_check_trace.py
[[[end]]]
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

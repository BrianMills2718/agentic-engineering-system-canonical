"""Report where the committed code differs from the plan: a missing file, export or signature.

Lockstep does not compare plan and code itself: it calls AES `characterize` (pinned in
pyproject.toml), which reads the governed files at HEAD by their syntax tree and never runs
them. So the facts are of the last commit; uncommitted edits show once committed, and
`make check` runs after the commit, before merge. At edit time the symbol gate (`lockstep.symbol_gate`,
behavior 5.5) judges the edit's own text with the same AES reader, so an uncommitted edit that adds an
undeclared symbol, changes a declared signature or removes a declared export is answered then (Q38).

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:plan_to_code.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-plan-format/old-route-checks-stay-while-a-repository-runs-them

### Requirement: Old-route checks stay while a repository runs them

For a repository with `.aes/target.yaml`, Lockstep SHALL keep the checks that plan route uses, each importable as
`lockstep.<name>` and `pcw.<name>`, and runnable as `python -m` under both names where it has a command line:
`action_check`, `behavior_check`, `change_list`, `change_log`, `criterion_checks`, `declared_reason`,
`docstring_up`, `linked_tests`, `plan_edit`, `plan_to_code`, `requirement_status`, `unplanned_symbols`, `wiki` and
`wiki_reach`. One SHALL be retired, with a dated record under
`docs/retired/`, only once no repository in `~/code2` runs it (code2-workspace decision 0009: `.aes/target.yaml`
retires one repository at a time).

Source: Brian, 2026-11-23: "i approve", to Q54 in `docs/planning/open-questions.json` ("write one requirement for
the ones the core calls; retire the rest"); the 2026-11-23 search found all 14 still run, so none retired (inferred by
agent from that search).

#### Scenario: An AES-plan repository's checks still run

- **GIVEN** a repository with `.aes/target.yaml`
- **WHEN** its Makefile or edit hook runs one of the 14 checks
- **THEN** the check runs as before, as each module's own tests show

Tested by: tests/lockstep/test_lockstep_plan_to_code.py
[[[end]]]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import NamedTuple

from agentic_engineering_system.characterize import check as characterize_check

from lockstep.aes_bridge import find_root


class PlanDrift(NamedTuple):
    revision: str
    dirty: bool  # the working tree differs from HEAD; the facts are still of HEAD
    failing: list[str]  # missing file, missing export, changed signature, or a file the plan does not name
    unrealized: list[str]  # planned files not written yet; reported, not failing


def plan_drift(root: Path) -> PlanDrift:
    """Every difference AES finds between the plan and the code at HEAD, one plain line each."""
    report = characterize_check(root)
    lines: dict[bool, list[str]] = {True: [], False: []}
    for d in report.drift:
        who = f" ({d.artifact_id})" if d.artifact_id else ""
        lines[d.failing].append(f"{d.kind}: {d.path}{who} - {d.detail}")
    c = report.characterization
    return PlanDrift(c.subject_revision, c.dirty, lines[True], lines[False])


def main(argv: list[str] | None = None) -> int:
    """`python -m lockstep.plan_to_code [--root DIR]`: print the drift; exit 1 if any of it fails."""
    ap = argparse.ArgumentParser(prog="lockstep.plan_to_code", description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path.cwd())
    args = ap.parse_args(argv)
    root = find_root(args.root)
    if root is None:
        print(f"no .aes/project.yaml at or above {args.root}", file=sys.stderr)
        return 2
    drift = plan_drift(root)
    for line in drift.failing:
        print(line)
    for line in drift.unrealized:
        print(f"  {line}")
    note = " (uncommitted changes present; facts are of HEAD)" if drift.dirty else ""
    print(f"plan_to_code: commit={drift.revision[:12]}{note} failing={len(drift.failing)} "
          f"unrealized={len(drift.unrealized)}")
    return 1 if drift.failing else 0


if __name__ == "__main__":
    raise SystemExit(main())

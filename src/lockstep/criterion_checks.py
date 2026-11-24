"""Check every success criterion names how it is checked: a test, a sign-off or an AI rubric (behavior 2.1).

A criterion counts as checked when one of these routes reaches it:
  - a test: a verification subject with proof kind `deterministic_test` and a locator naming the
    test (that the named file exists is behavior 2.2, `lockstep.linked_tests`);
  - a sign-off: a verification subject with proof kind `human_review` or `trace_review`;
  - an AI-graded rubric declared for it in Lockstep's side file, `lockstep.yaml` (`lockstep.side_file`).
A criterion whose only route is a runtime observation, or an evidence requirement routed outside
the repository (`external_boundaries`), names none of the three and is reported. So is a rubric
that names a criterion the plan does not hold. `python -m lockstep.criterion_checks` is part of
`make check`.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:criterion_checks.py", indent=0)]]]
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

Tested by: tests/lockstep/test_lockstep_criterion_checks.py
[[[end]]]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lockstep.aes_bridge import find_root, target
from lockstep.side_file import SIDE_FILE, load_side_file

TEST = {"deterministic_test"}
SIGN_OFF = {"human_review", "trace_review"}


def criterion_problems(plan: dict, rubrics: dict[str, str]) -> list[str]:
    """Each criterion with no test, sign-off or rubric route, and each rubric for an unknown criterion."""
    criteria = [sc["id"] for sc in plan.get("success_criteria") or [] if isinstance(sc, dict) and sc.get("id")]
    kinds: dict[str, set[str]] = {sc: set() for sc in criteria}
    for vs in plan.get("verification_subjects") or []:
        kind = vs.get("proof_kind")
        if kind in TEST and not (vs.get("locator") or "").strip():
            kind = "deterministic_test with no locator"
        for sc in vs.get("criterion_refs") or []:
            kinds.setdefault(sc, set()).add(kind)
    problems: list[str] = []
    for sc in criteria:
        if kinds[sc] & (TEST | SIGN_OFF) or sc in rubrics:
            continue
        found = f" (its only routes: {', '.join(sorted(kinds[sc]))})" if kinds[sc] else ""
        problems.append(f"{sc} names no way it is checked{found}: give it a test file, a sign-off "
                        f"(human_review or trace_review) or an AI-graded rubric in {SIDE_FILE}.")
    problems += [f"{SIDE_FILE} declares a rubric for {sc}, which is not a success criterion in .aes/target.yaml."
                 for sc in sorted(set(rubrics) - set(criteria))]
    return problems


def main(argv: list[str] | None = None) -> int:
    """`python -m lockstep.criterion_checks [--root DIR]`: print each problem; exit 1 if there is any."""
    ap = argparse.ArgumentParser(prog="lockstep.criterion_checks", description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path.cwd())
    args = ap.parse_args(argv)
    root = find_root(args.root)
    if root is None:
        print(f"no .aes/project.yaml at or above {args.root}", file=sys.stderr)
        return 2
    plan = target(root)
    try:
        side = load_side_file(root)
    except ValueError as exc:
        print(exc)
        print("criterion_checks: side_file=unreadable")
        return 1
    rubrics = side.rubrics if side is not None else {}
    problems = criterion_problems(plan, rubrics)
    for p in problems:
        print(p)
    print(f"criterion_checks: criteria={len(plan.get('success_criteria') or [])} rubrics={len(rubrics)} "
          f"problems={len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())

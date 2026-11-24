"""Report a behavior that lacks exactly one source file of its own or a criterion with a test route.

Reads only the plan (.aes/target.yaml): which components target a behavior, which source
artifacts those components list, and which verification subjects route its criteria. Whether
a planned file exists yet is behavior 5.3's question (src/pcw/plan_to_code.py), not this one.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:behavior_check.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-plan-format/old-route-checks-stay-while-a-repository-runs-them

### Requirement: Old-route checks stay while a repository runs them

For a repository with `.aes/target.yaml`, Lockstep SHALL keep the checks that plan route uses, each runnable as
`python -m lockstep.<name>` and `python -m pcw.<name>`: `action_check`, `behavior_check`, `change_list`,
`change_log`, `criterion_checks`, `declared_reason`, `docstring_up`, `linked_tests`, `plan_edit`, `plan_to_code`,
`requirement_status`, `unplanned_symbols`, `wiki` and `wiki_reach`. One SHALL be retired, with a dated record under
`docs/retired/`, only once no repository in `~/code2` runs it (code2-workspace decision 0009: `.aes/target.yaml`
retires one repository at a time).

Source: Brian, 2026-11-23: "i approve", to Q54 in `docs/planning/open-questions.json` ("write one requirement for
the ones the core calls; retire the rest"); the 2026-11-23 search found all 14 still run, so none retired (inferred by
agent from that search).

#### Scenario: An AES-plan repository's checks still run

- **GIVEN** a repository with `.aes/target.yaml`
- **WHEN** its Makefile or edit hook runs one of the 14 checks
- **THEN** the check runs as before, as each module's own tests show

Tested by: tests/lockstep/test_lockstep_behavior_check.py
[[[end]]]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lockstep.aes_bridge import find_root, target


def behavior_problems(plan: dict) -> list[str]:
    """Each place the plan breaks "one behavior, one source file, one routed criterion", in plain words.

    A behavior's files are the source artifacts listed by the components that target it, so a
    shared helper in a component that targets only requirements (CMP-SHARED) holds no behavior.
    A criterion is routed when a verification subject names it and gives a locator.
    """
    behaviors = [n["id"] for n in plan.get("normative_items") or [] if n.get("kind") == "behavior"]
    sources = {a["id"]: a["locator"]["exact_path"] for a in plan.get("planned_artifacts") or []
               if a.get("kind") == "source"}
    files_of: dict[str, set[str]] = {b: set() for b in behaviors}
    held_by: dict[str, set[str]] = {}
    for comp in plan.get("components") or []:
        targets = [r for r in comp.get("target_refs") or [] if r in files_of]
        for aid in comp.get("planned_artifact_refs") or []:
            if aid in sources:
                for b in targets:
                    files_of[b].add(sources[aid])
                    held_by.setdefault(sources[aid], set()).add(b)
    routed = {sc for vs in plan.get("verification_subjects") or [] if vs.get("locator")
              for sc in vs.get("criterion_refs") or []}

    problems: list[str] = []
    for b in behaviors:
        files = sorted(files_of[b])
        if not files:
            problems.append(f"{b} has no source file: no component that targets it lists a planned source artifact.")
        elif len(files) > 1:
            problems.append(f"{b} is spread over {len(files)} source files ({', '.join(files)}); "
                            "a behavior has exactly one.")
        criteria = [sc["id"] for sc in plan.get("success_criteria") or [] if b in (sc.get("target_refs") or [])]
        if not criteria:
            problems.append(f"{b} has no criterion: no success criterion targets it.")
        elif not any(sc in routed for sc in criteria):
            problems.append(f"{b} has no routed criterion: no verification subject with a locator proves "
                            f"{', '.join(criteria)}.")
    for path, held in sorted(held_by.items()):
        if len(held) > 1:
            problems.append(f"{path} holds {len(held)} behaviors ({', '.join(sorted(held))}); "
                            "each behavior gets a file of its own.")
    return problems


def main(argv: list[str] | None = None) -> int:
    """`python -m lockstep.behavior_check [--root DIR]`: print each problem; exit 1 if there is any."""
    ap = argparse.ArgumentParser(prog="lockstep.behavior_check", description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path.cwd())
    args = ap.parse_args(argv)
    root = find_root(args.root)
    if root is None:
        print(f"no .aes/project.yaml at or above {args.root}", file=sys.stderr)
        return 2
    plan = target(root)
    problems = behavior_problems(plan)
    for p in problems:
        print(p)
    count = sum(n.get("kind") == "behavior" for n in plan.get("normative_items") or [])
    print(f"behavior_check: behaviors={count} problems={len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())

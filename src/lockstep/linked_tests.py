"""Check tests and criteria link both ways: every named test file exists, every test file is named.

A test file is one pytest would collect by name (`test_*.py` or `*_test.py`) under a governed
folder, tracked or new; files `aes adopt` accepted as legacy are listed, not checked. A named
test file is the locator of a verification subject whose proof kind is `deterministic_test`.
A named file that is planned but not written yet is listed, not failing, as in `aes topology`.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:linked_tests.py", indent=0)]]]
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

Tested by: tests/lockstep/test_lockstep_linked_tests.py
[[[end]]]
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import NamedTuple

from lockstep.aes_bridge import find_root, governed_roots, legacy_files, target


class LinkReport(NamedTuple):
    dangling: list[str]  # a test route names a file that does not exist and the plan does not declare
    unnamed: list[str]  # a test file that no test route names
    unbuilt: list[str]  # a test route names a planned test file not written yet; listed, not failing
    legacy: list[str]  # test files accepted as-is by `aes adopt`; not checked until planned


def _is_test_file(path: str) -> bool:
    name = PurePosixPath(path).name
    return name.endswith(".py") and (name.startswith("test_") or name.endswith("_test.py"))


def link_report(root: Path) -> LinkReport:
    """Both directions between the plan's test routes and the test files on disk, one plain line each."""
    plan = target(root)
    planned = {(a.get("locator") or {}).get("exact_path") for a in plan.get("planned_artifacts") or []}
    named: dict[str, list[str]] = {}
    for vs in plan.get("verification_subjects") or []:
        locator = (vs.get("locator") or "").split("::")[0]
        if locator and vs.get("proof_kind") == "deterministic_test":
            named.setdefault(locator, []).append(vs["id"])

    dangling, unbuilt = [], []
    for path, ids in sorted(named.items()):
        if (root / path).is_file():
            continue
        if path in planned:
            unbuilt.append(f"{path} is named by {', '.join(ids)} and planned, not written yet.")
        else:
            dangling.append(f"{path} is named by {', '.join(ids)} but does not exist, and the plan does not declare it.")

    roots = governed_roots(root)
    listed = subprocess.run(["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard",
                             "--", *roots], capture_output=True, text=True, check=True).stdout.split()
    tests = sorted({p for p in listed if _is_test_file(p) and (root / p).is_file()})
    legacy = legacy_files(root)
    unnamed = [f"{p} is a test file that no criterion's test route names." for p in tests
               if p not in named and p not in legacy]
    return LinkReport(dangling, unnamed, unbuilt, [p for p in tests if p in legacy])


def main(argv: list[str] | None = None) -> int:
    """`python -m lockstep.linked_tests [--root DIR]`: print what does not link; exit 1 if anything fails."""
    ap = argparse.ArgumentParser(prog="lockstep.linked_tests", description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path.cwd())
    args = ap.parse_args(argv)
    root = find_root(args.root)
    if root is None:
        print(f"no .aes/project.yaml at or above {args.root}", file=sys.stderr)
        return 2
    r = link_report(root)
    for line in [*r.dangling, *r.unnamed]:
        print(line)
    for line in r.unbuilt:
        print(f"  {line}")
    print(f"linked_tests: dangling={len(r.dangling)} unnamed={len(r.unnamed)} unbuilt={len(r.unbuilt)} "
          f"legacy={len(r.legacy)}")
    return 1 if r.dangling or r.unnamed else 0


if __name__ == "__main__":
    raise SystemExit(main())

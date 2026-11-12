"""Report where the committed code differs from the plan: a missing file, export or signature.

Lockstep does not compare plan and code itself: it calls AES `characterize` (pinned in
pyproject.toml), which reads the governed files at HEAD by their syntax tree and never runs
them. So the facts are of the last commit; uncommitted edits show once committed, and
`make check` runs after the commit, before merge. At edit time the symbol gate (`lockstep.symbol_gate`,
behavior 5.5) judges the edit's own text with the same AES reader, so an uncommitted edit that adds an
undeclared symbol, changes a declared signature or removes a declared export is answered then (Q38).

[[[cog import lockstep.cogtext as c; c.docstring("ART-PLAN-TO-CODE", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

Part of REQ-5: Links are checked both ways on every change: links between
  requirement, criterion, test, file and symbol are checked in both
  directions on every change, at edit time (the hook) and before commit
  (`pcw check`); an unplanned or stale item is refused.
BEH-5.3: A planned file or declared symbol that has no code, or whose
  signature differs from the plan, is reported.
SC-5.3: A missing planned file, a missing export and a changed signature are
  each reported.
  Disproved if: A planned file or export is missing, or its signature
  differs, and nothing reports it.
Proven by: VS-5.3-a (tests/test_plan_to_code.py)
Declares (typed signatures, from the plan):
  PlanDrift
  plan_drift(root: Path) -> PlanDrift
  main(argv: list[str] | None = None) -> int
[[[end]]] (sum: B0Afrt3DKk)
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

"""Refuse a planned file whose declaration gives no reason (behavior 1.3).

Every file in the plan names the plan items it serves in `semantic_justification_refs`. AES
refuses an entry there that names nothing in the plan, but accepts an empty list, so a file can
enter the plan with no reason at all. This names each such file. `python -m lockstep.declared_reason`
is part of `make check`, and `pcw check` refuses an accepted plan change whose resulting plan
holds one (`lockstep.check`).

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:declared_reason.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: (no requirement)
[[[end]]]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lockstep.aes_bridge import find_root, target


def reasonless_artifacts(plan: dict) -> list[str]:
    """One plain-words problem for each planned file whose reason list is empty."""
    problems: list[str] = []
    for art in plan.get("planned_artifacts") or []:
        if not isinstance(art, dict) or art.get("semantic_justification_refs"):
            continue
        path = (art.get("locator") or {}).get("exact_path") or "(no path)"
        problems.append(f"{art.get('id')} ({path}) gives no reason for being in the plan: its "
                        "semantic_justification_refs list is empty. Name the requirement, behavior or "
                        "criterion it serves, through `aes plan prepare/validate/accept`.")
    return problems


def main(argv: list[str] | None = None) -> int:
    """`python -m lockstep.declared_reason [--root DIR]`: print each problem; exit 1 if there is any."""
    ap = argparse.ArgumentParser(prog="lockstep.declared_reason", description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path.cwd())
    args = ap.parse_args(argv)
    root = find_root(args.root)
    if root is None:
        print(f"no .aes/project.yaml at or above {args.root}", file=sys.stderr)
        return 2
    plan = target(root)
    problems = reasonless_artifacts(plan)
    for p in problems:
        print(p)
    print(f"declared_reason: files={len(plan.get('planned_artifacts') or [])} problems={len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Build the list of contract items the grader scores: every requirement, rule, invariant and scenario of one game,
minus the items the decidability pilot dropped (docs/planning/next.goal.md, "Game benchmark plan", Results).

Usage: python3 items.py <game dir> <out.json>
"""
import json, sys
from pathlib import Path

DROPPED = {"requirement:R1", "rule:R1", "invariant:SYN-INIT-runseed", "scenario:chain_cluster",
           "scenario:enemy_roster_zone1"}  # pilot 2026-11-26, abyssal_chain


def _main(game: Path, out: Path) -> int:
    items = []
    for name, kind in [("requirements", "requirement"), ("rules", "rule"), ("invariants", "invariant"),
                       ("scenarios", "scenario")]:
        for x in json.loads((game / "contracts" / f"{name}.json").read_text()):
            iid = f"{kind}:{x.get('id')}"
            if iid not in DROPPED:
                items.append({"id": iid, "kind": kind, "item": x})
    out.write_text(json.dumps(items, indent=1))
    print(f"RESULT items={len(items)} dropped={len(DROPPED)}")
    return 0


if __name__ == "__main__":
    sys.exit(_main(Path(sys.argv[1]), Path(sys.argv[2])))

"""`lockstep plan units [--repo PATH] [--json]`: is the plan's work-unit DAG well formed, and what can start now?

Implements: lockstep-plan-check/work-units-form-a-checked-dag

Requirement text (generated):
    lockstep-plan-check/work-units-form-a-checked-dag: `lockstep plan units` SHALL read
        `docs/planning/work-units.json` (record type `work_units`, a list `units`) and exit 1,
        naming each problem, unless: each unit has a unique `id`, a `title`, a `depends_on` list of
        existing unit ids (empty means it can start now), a `touches` list of repository paths, and
        a `status` of `planned`, `in progress` or `merged`; a `merged` unit has `evidence`; and the
        dependencies contain no cycle. It SHALL print the units that are ready (not merged, every
        dependency merged), the longest chain of unmerged units, and each pair of unmerged units
        with no dependency path between them whose `touches` overlap (paths are compared as exact
        strings, so a directory and a file inside it do not overlap). It exits 2 when the file is
        missing or not JSON. `lockstep plan check` SHALL report the same problems when the file is
        present.

Reads `docs/planning/work-units.json` (record type `work_units`, a list `units`; each unit has `id`, `title`,
`depends_on`, `touches`, `status`, and `evidence` once merged). Reports problems, the ready units, the longest chain of
unmerged units and independent unmerged units that touch the same file. Reads no model and runs no code.

Exit 0 well formed, 1 problems (each named), 2 the file is missing or is not JSON.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:work_units.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-plan-check/work-units-form-a-checked-dag

### Requirement: Work units form a checked DAG

Source: Brian, 2026-11-14: "we should always have a dag as part of the plans so we can optimally parallelize and stay on track"; approved with "i apporve your recs".

`lockstep plan units` SHALL read `docs/planning/work-units.json` (record type `work_units`, a list `units`) and exit 1, naming each problem, unless: each unit has a unique `id`, a `title`, a `depends_on` list of existing unit ids (empty means it can start now), a `touches` list of repository paths, and a `status` of `planned`, `in progress` or `merged`; a `merged` unit has `evidence`; and the dependencies contain no cycle. It SHALL print the units that are ready (not merged, every dependency merged), the longest chain of unmerged units, and each pair of unmerged units with no dependency path between them whose `touches` overlap (paths are compared as exact strings, so a directory and a file inside it do not overlap). It exits 2 when the file is missing or not JSON. `lockstep plan check` SHALL report the same problems when the file is present.

#### Scenario: Independent units are both ready

- **GIVEN** units A and B with empty `depends_on` and different `touches`
- **WHEN** `lockstep plan units` runs
- **THEN** it exits 0 and lists both as ready

#### Scenario: A cycle fails

- **GIVEN** unit A depending on B and B depending on A
- **WHEN** `lockstep plan units` runs
- **THEN** it exits 1 and names the cycle

#### Scenario: A dependency on a missing unit fails

- **GIVEN** a unit whose `depends_on` names an id no unit has
- **WHEN** `lockstep plan units` runs
- **THEN** it exits 1 and names the unit and the missing id

#### Scenario: Independent units touching one file are flagged

- **GIVEN** unmerged units A and B with no dependency path between them that both touch `src/x.py`
- **WHEN** `lockstep plan units` runs
- **THEN** it reports the conflict naming both units and the file

#### Scenario: A merged unit needs evidence

- **GIVEN** a `merged` unit without `evidence`
- **WHEN** `lockstep plan units` runs
- **THEN** it exits 1 naming the unit

Tested by: tests/lockstep/test_lockstep_work_units.py
[[[end]]]
"""

import argparse
import json
import sys
from itertools import combinations
from pathlib import Path
from typing import Any

DEFAULT_UNITS = "docs/planning/work-units.json"
STATUSES = ("planned", "in progress", "merged")


def _str_list(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(v, str) for v in value)


def analyse(record: Any) -> dict:
    """Problems, ready ids, critical path and file conflicts for one parsed record."""
    out: dict = {"problems": [], "ready": [], "critical_path": [], "conflicts": [], "counts": {}}
    problems: list[str] = out["problems"]
    units = record.get("units") if isinstance(record, dict) else None
    if not isinstance(record, dict) or record.get("record_type") != "work_units":
        return {**out, "problems": ["record_type is not work_units"]}
    if not isinstance(units, list) or not units:
        return {**out, "problems": ["units: none listed"]}
    by_id: dict[str, dict] = {}
    for i, u in enumerate(units):
        uid = u.get("id") if isinstance(u, dict) else None
        if not isinstance(uid, str) or not uid:
            problems.append(f"unit {i + 1}: no id")
            continue
        if uid in by_id:
            problems.append(f"{uid}: duplicate id")
            continue
        by_id[uid] = u
        if not u.get("title"):
            problems.append(f"{uid}: no title")
        if not _str_list(u.get("depends_on")):
            problems.append(f"{uid}: depends_on must be a list of unit ids (empty means it can start now)")
        if not _str_list(u.get("touches")):
            problems.append(f"{uid}: touches must be a list of repository paths")
        if u.get("status") not in STATUSES:
            problems.append(f"{uid}: status must be one of {', '.join(STATUSES)}")
        if u.get("status") == "merged" and not u.get("evidence"):
            problems.append(f"{uid}: merged but no evidence")
    deps = {uid: (u["depends_on"] if _str_list(u.get("depends_on")) else []) for uid, u in by_id.items()}
    for uid, ds in deps.items():
        for d in ds:
            if d not in by_id:
                problems.append(f"{uid}: depends_on names {d}, which is not a unit")
    cycle = _find_cycle({k: [d for d in v if d in by_id] for k, v in deps.items()})
    if cycle:
        problems.append("cycle: " + " -> ".join(cycle))
    out["counts"] = {s: sum(1 for u in by_id.values() if u.get("status") == s) for s in STATUSES}
    if cycle:
        return out
    merged = {k for k, u in by_id.items() if u.get("status") == "merged"}
    out["ready"] = [k for k, u in by_id.items()
                    if k not in merged and all(d in merged for d in deps[k] if d in by_id)]
    out["critical_path"] = _critical_path(by_id, deps, merged)
    out["conflicts"] = _conflicts(by_id, deps, merged)
    return out


def _find_cycle(graph: dict[str, list[str]]) -> list[str]:
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(n: str) -> list[str]:
        state[n] = 1
        stack.append(n)
        for m in graph[n]:
            if state.get(m) == 1:
                return stack[stack.index(m):] + [m]
            if m not in state and (c := visit(m)):
                return c
        stack.pop()
        state[n] = 2
        return []

    for n in graph:
        if n not in state and (c := visit(n)):
            return c
    return []


def _critical_path(by_id: dict, deps: dict, merged: set) -> list[str]:
    best: dict[str, list[str]] = {}

    def chain(n: str) -> list[str]:
        if n not in best:
            below = [chain(d) for d in deps[n] if d in by_id and d not in merged]
            best[n] = max(below, key=len, default=[]) + [n]
        return best[n]

    paths = [chain(n) for n in by_id if n not in merged]
    return max(paths, key=len, default=[])


def _conflicts(by_id: dict, deps: dict, merged: set) -> list[dict]:
    reach: dict[str, set[str]] = {}

    def up(n: str) -> set[str]:
        if n not in reach:
            reach[n] = set()
            for d in deps[n]:
                if d in by_id:
                    reach[n] |= {d} | up(d)
        return reach[n]

    found = []
    for a, b in combinations([k for k in by_id if k not in merged], 2):
        if a in up(b) or b in up(a):
            continue
        shared = sorted(set(by_id[a].get("touches") or []) & set(by_id[b].get("touches") or []))
        if shared:
            found.append({"units": [a, b], "files": shared})
    return found


def units_cli(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="lockstep plan units", description=__doc__.split("\n\n")[0])
    parser.add_argument("--repo", type=Path, default=Path("."), help="the repository (default: the current directory)")
    parser.add_argument("--json", action="store_true", help="print the result as one JSON object")
    args = parser.parse_args(argv)
    path = args.repo / DEFAULT_UNITS
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"cannot check: {path}: {exc}", file=sys.stderr)
        return 2
    result = analyse(record)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        c = result["counts"]
        print(f"{'ok  ' if not result['problems'] else 'FAIL'} work units: "
              + ", ".join(f"{n} {s}" for s, n in c.items()))
        print("ready: " + (", ".join(result["ready"]) or "none"))
        print("critical path: " + (" -> ".join(result["critical_path"]) or "none"))
        for x in result["conflicts"]:
            print(f"conflict: {x['units'][0]} and {x['units'][1]} are independent but both touch {', '.join(x['files'])}")
        for p in result["problems"]:
            print(f"  {p}")
        print(f"OUTCOME {'ok' if not result['problems'] else 'fail'}: {len(result['problems'])} problems")
    return 0 if not result["problems"] else 1

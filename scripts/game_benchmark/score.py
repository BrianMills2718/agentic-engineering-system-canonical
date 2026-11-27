"""Score one graded build: fidelity = mean over contract items, pass 1, partial 0.5, fail 0).

Usage: python3 score.py <grade dir>   (reads items.json and verdicts.json, writes score.json)
"""
import json, sys
from collections import Counter
from pathlib import Path

POINTS = {"pass": 1.0, "partial": 0.5, "fail": 0.0}


def _main(g: Path) -> int:
    items = [i["id"] for i in json.loads((g / "items.json").read_text())]
    report = json.loads((g / "verdicts.json").read_text())
    rows = report["verdicts"]
    got = {row["id"]: row for row in rows}
    if not items or len(set(items)) != len(items) or len(got) != len(rows) or set(got) != set(items):
        print("Scoring refused: require exactly one verdict for every unique scored item.", file=sys.stderr)
        return 2
    if type(report.get("loads")) is not bool or any(
        row["verdict"] not in POINTS or row["method"] not in {"play", "source"}
        or not row["evidence"].strip() for row in rows
    ):
        print("Scoring refused: invalid load status, verdict, method or evidence.", file=sys.stderr)
        return 2
    verdicts = [got[i]["verdict"] for i in items]
    if not report["loads"] and any(v != "fail" for v in verdicts):
        print("Scoring refused: a game that cannot load must fail every item.", file=sys.stderr)
        return 2
    by_kind = {}
    for i, v in zip(items, verdicts):
        by_kind.setdefault(i.split(":")[0], []).append(POINTS[v])
    score = {"fidelity": round(100 * sum(POINTS[v] for v in verdicts) / len(items), 1),
             "counts": dict(Counter(verdicts)), "missing_verdicts": 0, "items": len(items),
             "by_kind": {k: round(100 * sum(p) / len(p), 1) for k, p in by_kind.items()},
             "source_judged": sum(1 for v in got.values() if v.get("method") == "source")}
    (g / "score.json").write_text(json.dumps(score, indent=1))
    print("RESULT", json.dumps(score))
    return 0


if __name__ == "__main__":
    sys.exit(_main(Path(sys.argv[1])))

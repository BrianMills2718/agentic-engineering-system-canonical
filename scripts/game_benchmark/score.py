"""Score one graded build: fidelity = mean over contract items, pass 1, partial 0.5, fail 0 (missing verdict = fail).

Usage: python3 score.py <grade dir>   (reads items.json and verdicts.json, writes score.json)
"""
import json, sys
from collections import Counter
from pathlib import Path

POINTS = {"pass": 1.0, "partial": 0.5, "fail": 0.0}


def main(g: Path) -> int:
    items = [i["id"] for i in json.loads((g / "items.json").read_text())]
    got = {v["id"]: v for v in json.loads((g / "verdicts.json").read_text())["verdicts"]}
    missing = [i for i in items if i not in got]
    verdicts = [got[i]["verdict"] if i in got else "fail" for i in items]
    by_kind = {}
    for i, v in zip(items, verdicts):
        by_kind.setdefault(i.split(":")[0], []).append(POINTS[v])
    score = {"fidelity": round(100 * sum(POINTS[v] for v in verdicts) / len(items), 1),
             "counts": dict(Counter(verdicts)), "missing_verdicts": len(missing), "items": len(items),
             "by_kind": {k: round(100 * sum(p) / len(p), 1) for k, p in by_kind.items()},
             "source_judged": sum(1 for v in got.values() if v.get("method") == "source")}
    (g / "score.json").write_text(json.dumps(score, indent=1))
    print("RESULT", json.dumps(score))
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1])))

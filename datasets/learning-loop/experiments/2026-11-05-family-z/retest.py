"""Re-test a question set on the judged sets before trusting a change (label_items.py docstring).

Runs the 2026-10-02 held-out set (20 judged learnings + 4 synthetic `other` items)
and the private feedback issues named in FEEDBACK (fetched at run time with `gh`;
their text is never written here) through Jev with the question set
given, using label_items.py's own ask() and decide(). Prints counts; writes rows.

  python3 retest.py <question_set.json> <out.json>
"""
import json, os, subprocess, sys, glob
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3] / "scripts" / "learning_loop"))
import label_items as li  # noqa: E402

FEEDBACK = [475, 1068, 1686, 1266, 1419, 904]  # BrianMills2718/agent-feedback-log
qs = json.loads(Path(sys.argv[1]).read_text())
SRC = HERE.parent / "2026-10-02-question-design"
GT = {l.split("\t")[0]: l.split("\t")[1].split() for l in (SRC / "holdout_gt.tsv").read_text().strip().split("\n")}
docs = {d.get("entry_id"): d for d in (json.load(open(f)) for f in glob.glob(os.path.expanduser(li.LEGACY_GLOB)))}
items = [("holdout", k, {"learning": li.entry_text(docs[k])[:1800], "recommended_action": str(docs[k].get("recommended_action") or "")[:400]}, acc) for k, acc in GT.items()]
items += [("synthetic", k, {"learning": t, "recommended_action": ""}, a.split()) for k, (t, a) in json.load(open(SRC / "synthetic.json")).items()]
def issue_state(n):  # the same state label_items.py builds for an issue
    i = json.loads(subprocess.run(["gh", "issue", "view", str(n), "--repo", li.REPO, "--json", "title,body"],
                                  capture_output=True, text=True, check=True).stdout)
    return {"learning": (i["title"] + "\n\n" + i["body"])[:1800], "recommended_action": ""}
items += [("feedback", f"#{n}", issue_state(n), []) for n in FEEDBACK]
key, rows, errors = li.api_key(), [], 0
for group, k, state, acc in items:
    r, err, secs = li.ask(state, qs["question"], key)
    if err:
        errors += 1; rows.append({"group": group, "key": k, "error": err}); continue
    d = li.decide(r["answers"], qs)
    near = d["families"] or [d["choice"]]
    rows.append({"group": group, "key": k, "acc": acc, **d, "near": near,
                 "top_ok": d["choice"] in acc, "near_ok": any(x in acc for x in near), "cost": r.get("usage", {}).get("cost")})
Path(sys.argv[2]).write_text(json.dumps(rows, indent=1))
for g in ("holdout", "synthetic"):
    rs = [r for r in rows if r["group"] == g and "error" not in r]
    print(f"{g}: top {sum(r['top_ok'] for r in rs)}/{len(rs)}, near-top {sum(r['near_ok'] for r in rs)}/{len(rs)}")
for r in rows:
    if r["group"] == "feedback" and "error" not in r:
        print(f"feedback {r['key']}: {r['choice']} p={r['p']} near={r['near']} second={r['second']}")
print(f"errors {errors}, cost ${sum(r.get('cost') or 0 for r in rows):.4f}")
sys.exit(1 if errors else 0)

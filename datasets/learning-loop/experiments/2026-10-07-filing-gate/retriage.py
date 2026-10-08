"""Score the 2026-10-06 backlog's pending closeout-Learnings items with the collector's own triage
(kind + reusable question) and append updated item lines, so file-pending applies the same gate."""
import json, sys
sys.path.insert(0, "/home/brian/.hive-brain/aes/scripts/learning_loop")
import collect_feedback as C
path = C.OUT / "items-2026-10-06.jsonl"
items = {}
for l in open(path):
    d = json.loads(l)
    if "filing_update" in d:
        if d["id"] in items: items[d["id"]]["filing"] = d["filing_update"]
    else: items[d["id"]] = d
todo = [i for i in items.values() if str(i.get("filing", "")).startswith(C.PENDING)
        and (i["source"], i["field"]) in C.AUTO_FILE_SOURCES and "reusable_p" not in (i.get("triage") or {})]
with open(path, "a") as fh:
    for it in todo:
        it["triage"] = C.jev_triage(it)
        fh.write(json.dumps(it) + "\n")
        print(it["id"], it["triage"]["kind"], it["triage"]["p"], it["triage"]["reusable_p"], it["quote"][:80].replace("\n", " "))
print("rescored", len(todo))

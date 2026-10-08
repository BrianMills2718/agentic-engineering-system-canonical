import json, sys
from concurrent.futures import ThreadPoolExecutor
from llm_client import NoulQuestion, call_decisions
JEV = "openrouter/typesafe/jev-1.13"
Q = ("Would this help a future AI coding agent working on a DIFFERENT task or project? "
     "Yes only if it states a general fact or practice about tools, code, data, process or the environment. "
     "No if it is narration of what this session is doing, a status update, or details that only matter "
     "for this one task, document, client or person.")
gold_yes = {0,1,2,3,4,5,6,7,10,12,16,17,23,24,30}
items = json.load(open("filed.json"))
def ask(n_it):
    n, it = n_it
    r = call_decisions(JEV, state={"text": it["quote"][:2000], "lesson": it.get("lesson") or ""},
                       questions={"reusable": NoulQuestion(Q)}, task="feedback-collector.reusable-eval",
                       trace_id=f"feedback-collector/reusable-eval/{it['id']}", max_budget=0.01)
    return n, float(r.answers["reusable"].probability), r.cost
with ThreadPoolExecutor(8) as ex:
    res = sorted(ex.map(ask, enumerate(items)))
cost = sum(c or 0 for _, _, c in res)
for n, p, _ in res:
    print(f"{n:2d} gold={'Y' if n in gold_yes else 'N'} p={p:.2f}")
for t in (0.5, 0.6, 0.7, 0.8, 0.9):
    kept = [n for n, p, _ in res if p >= t]
    good = [n for n in kept if n in gold_yes]
    print(f"threshold {t}: kept {len(kept)}, of which reusable {len(good)} ({(len(good)/len(kept)*100 if kept else 0):.0f}%), reusable missed {len(gold_yes)-len(good)}")
print(f"cost ${cost:.4f}")

"""Does the collector's light model (deepseek-v4-flash) catch the two known reworded repeats, and pass the 8 distinct ones?"""
import json, subprocess
from pydantic import BaseModel
from llm_client import call_llm_structured
IDS = ["20261007T223152837944Z-72db6015f0","20261007T223149056443Z-28f315cef1","20261007T223157008135Z-07e015f808","20261007T223143329980Z-a6029c8254","20261007T223302003421Z-cf440831a4","20261007T223305802135Z-c33c22a6e0","20261007T223309382106Z-6da3d556cf","20261007T223312880169Z-c580e5514d","20261007T223316831868Z-9707659561","20261007T223320160250Z-6cdf7df120"]
def text(i):
    d=json.loads(subprocess.run(["git","-C","/home/brian/code/project-meta","show",f"origin/main:learnings/entries/lrn-{i}.json"],capture_output=True,text=True,check=True).stdout)
    return d["learning"].split(" wrote: ",1)[1].split("\n\nSuggested lesson",1)[0].strip()
T=[text(i) for i in IDS]
class Same(BaseModel):
    same_lesson_as: int | None
    reason: str
truth={6:5, 8:7}
hits=0
for k in range(1,len(T)):
    earlier="\n".join(f"[{j}] {T[j]}" for j in range(k))
    r=call_llm_structured("openrouter/deepseek/deepseek-v4-flash",[{"role":"user","content":
      "A new lesson is about to be added to a register of lessons for AI coding agents. Does it state the SAME lesson as one of the "
      "earlier entries (same fact or practice, even if worded differently or mixed with other points)? Answer the earlier entry's "
      f"number, or null if none.\n\nEarlier entries:\n{earlier}\n\nNew lesson:\n{T[k]}"}], Same,
      task="feedback-collector.paraphrase-probe", trace_id=f"feedback-collector/paraphrase-probe/{k}", max_budget=0.02, reasoning_effort="none",
      model_justification="light model for prose meaning: does a new lesson repeat an earlier one")
    res=r[0] if isinstance(r,tuple) else r
    ans=res.same_lesson_as
    ok = ans==truth.get(k)
    hits+=ok
    print(k, "said", ans, "expected", truth.get(k), "OK" if ok else "WRONG", "|", res.reason[:110])
print(f"PROBE: {hits}/{len(T)-1} correct")

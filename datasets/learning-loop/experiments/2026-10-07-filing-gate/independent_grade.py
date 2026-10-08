"""Independent grade of the 10 gated entries by a different model family (Gemini), blind to the
filer's kind label and scores. Prints one line per entry and a summary."""
import json, subprocess
from typing import Literal
from pydantic import BaseModel
from llm_client import call_llm_structured

IDS = ["20261007T223152837944Z-72db6015f0", "20261007T223149056443Z-28f315cef1", "20261007T223157008135Z-07e015f808",
       "20261007T223143329980Z-a6029c8254", "20261007T223302003421Z-cf440831a4", "20261007T223305802135Z-c33c22a6e0",
       "20261007T223309382106Z-6da3d556cf", "20261007T223312880169Z-c580e5514d", "20261007T223316831868Z-9707659561",
       "20261007T223320160250Z-6cdf7df120"]
texts = {}
for i in IDS:
    d = json.loads(subprocess.run(["git", "-C", "/home/brian/code/project-meta", "show", f"origin/main:learnings/entries/lrn-{i}.json"],
                                  capture_output=True, text=True, check=True).stdout)
    texts[i[-10:]] = d["learning"].split(" wrote: ", 1)[1].split("\n\nSuggested lesson", 1)[0].strip()

class Grade(BaseModel):
    entry: str
    reusable: bool
    kind: Literal["learning", "friction", "correction", "concern", "noise"]
    repeats_entry: str | None
    reason: str

class Grades(BaseModel):
    grades: list[Grade]

prompt = ("You are auditing entries filed into a shared register of lessons for AI coding agents. For EACH entry decide:\n"
          "- reusable: true only if it states a general fact or practice that would help an agent on a DIFFERENT task or project; "
          "false if it is narration, status, or only matters for its own task, document, client or person.\n"
          "- kind: learning (a reusable fact or practice), friction (a rule/tool/process got in the way), correction (a person "
          "told an agent it was wrong), concern (an open unresolved risk), noise (nothing reusable).\n"
          "- repeats_entry: the id of an EARLIER entry in this list that states the same lesson, else null.\n"
          "Judge each on its own text. Entries:\n\n" + "\n\n".join(f"[{k}] {v}" for k, v in texts.items()))
r = call_llm_structured("openrouter/google/gemini-3.1-pro-preview", [{"role": "user", "content": prompt}], Grades,
                        task="feedback-collector.independent-grade", trace_id="feedback-collector/independent-grade/2026-10-07",
                        max_budget=0.5, reasoning_effort="medium",
                        model_justification="independent grader from a model family different from the filer (Jev, deepseek) and the session agent (Claude)")
res = r[0] if isinstance(r, tuple) else r
res = getattr(res, "grades", None) or res.output.grades
ok = 0
for g in res:
    passed = g.reusable and g.kind == "learning" and not g.repeats_entry
    ok += passed
    print(f"{g.entry} reusable={g.reusable} kind={g.kind} repeats={g.repeats_entry} PASS={passed} | {g.reason[:150]}")
print(f"INDEPENDENT GRADE: {ok}/{len(res)} pass (reusable, typed learning, not a repeat); grader=gemini-3.1-pro-preview")

"""Build review-page/requirements.html: each of Brian's feedback-system requirements vs the running system."""
import html, json, sys
from pathlib import Path
OUT = Path(sys.argv[1])
NOT, PART, MET = "not", "part", "met"
# (area, quote, source, status, evidence, fix)
R = [
("Capture", "if there was anything worth learning that agents would put it in the feedback seciton and it would get automatically added to a log", "chat, 8 Oct 02:57", PART,
 "The nightly collector read 931 feedback reports on 12 Oct (623 from Claude, 308 from Codex) for $0.05. But only 80 a night are filed to the log: 803 of the 931 waited for the limit.",
 "Raise or remove the 80-a-night filing limit (no model cost; it limits GitHub issue creation)."),
("Capture", "you not recording frictions is itself a friction.", "chat, 5 Oct", PART,
 "Every reply must end with a Feedback field (workspace instructions), and the collector reads it nightly. Nothing checks that a turn with a workaround actually recorded one.",
 "Count turns whose trace shows a blocked command or retry but whose Feedback field says None."),
("Capture", "the agent i thnk should nb be encoruage to specurlate on more than just what hepned and evidnece. so it should be as much information as it can provide and qualfiied and provenanced.", "chat, 8 Oct 03:27", PART,
 "The learned skill quotes this and asks for qualified guesses with links. No check measures whether lines carry a confidence and a link.",
 "Have the nightly job count reports without a qualifier or link, and show the share."),
("Capture", "links out to evidence htan explains it or else it consumes my attention", "WORKING_RULES, 7 Oct", PART,
 "First production run (8 Oct): 22 of 69 records had no link. Not re-measured since.",
 "Same nightly count as above."),
("Capture", "this is suppsoed to be like a feedback record whcih would include friction as well as learning", "WORKING_RULES, 7 Oct", MET,
 "One private log holds lessons, friction, problems and your corrections, each labelled by kind.", ""),
("Sorting", "that log would be sorted. failure into failure modes which would go go the audit skill/audit subagent", "chat, 8 Oct 02:57", NOT,
 "Reports get failure-mode labels, but the weekly job that feeds them back to the audit skill's failure-mode list has failed since 11 Oct (a duplicate report id in the 10 Oct file). Concerns project-meta #2538 and #2060 are open; no fix yet.",
 "Fix the duplicate-id crash so the weekly failure-mode check runs again."),
("Sorting", "that system 1 models might be helpful here", "chat, 8 Oct 02:57", MET,
 "A light model extracts and labels reports nightly (12 Oct: 327 items, 0 errors, $0.047).", ""),
("Fixing", "root solutions in planning to aovide those to company planning", "chat, 8 Oct 02:57", PART,
 "Prevent-type fixes go through a planning lane: 25 proposed, 20 enforced with a receipt, 5 declined. But only problems that get analysed reach this step, and only 5 of 181 repeating problems have been analysed.",
 "Remove the 3-a-week analysis limit (about $3.50 once, then about $0.70 a week)."),
("Fixing", "i am not waiting 6 weeks. thtat is what the feedback system is for.", "chat, 11 Oct", NOT,
 "The fix agent now runs daily. But the weekly grouping job analyses 3 problems a week, and 176 are waiting: at that rate the queue takes about a year.",
 "Same: remove the analysis limit, and run grouping daily."),
("Fixing", "i dont want to be in the feedback loop for goals ... i need agents to maek their best judgment", "chat, 8 Oct 03:52", MET,
 "The daily fix agent decides each item itself (implement, already enforced, decline, or defer with a blocker) and a script checks every decision on GitHub. None of the 25 asked you.", ""),
("Fixing", "a lesson or rule counts only once a check enforces it, until then it is a note", "vision thesis, 5 Oct", MET,
 "A fix counts only with an enforcement receipt naming the commit and the proof; 20 have one.", ""),
("Fixing", "enforcement observations ... declar which situation it is in and why and then each situation should have a checklist it has to check off", "chat, 6 Oct 17:35", PART,
 "The fix agent must pick one of four fixed outcomes and the script reads each back. The broader rule is registered but only partly enforced.",
 ""),
("Your view", "i want to be able to observe it sorted by like impact ucnertainty and notified", "chat, 8 Oct 03:52", PART,
 "A ranked list (impact, then uncertainty) is written weekly, but to a file in a private repository, not a page you open. Notifications fire only for high-impact active fixes.",
 "Put the ranked list on the live review pages."),
("Rules", "most improant thing is the new policy ad wheter it is docuemtned, and wehther it is observable enforceable and connected to a feebdack loop", "chat, 12 Oct", NOT,
 "Your workspace instructions name 11 rules. 10 have a source entry, but only 2 are in the policy register that records how a rule is enforced and where its friction goes. The other 9 (including read-the-trace and loud-failures) have no enforcement record and no feedback path. Found and made checkable today.",
 "Done today: a daily check that names every unregistered rule and opens a concern for an agent. Still to do: write the 9 register entries."),
("Measuring", "how are we going to build the thumbs up thumbs down? dont we need to do this by exmaining traces? ... more like shared lessons resused ... an objective llm adjustcate this stuff", "chat, 7 Oct 22:25", NOT,
 "The effect counter only checks whether a problem was seen again after its fix (10 counted). Nothing measures whether a lesson was reused, and no model reads traces to judge it.",
 "Add a weekly judge that reads a sample of traces after each fix and records reused, ignored or not applicable."),
("Measuring", "this is one of the most important policies for coding", "read-the-trace, 8 Oct", PART,
 "The fix agent's own outcome is read from GitHub, not from its summary, and every run keeps its full trace. But read-the-trace itself is one of the 9 unregistered rules.",
 "Register it (part of the 9)."),
("Measuring", "we always want maximum observability in logs and in output for my coding agents", "WORKING_RULES, 29 Sep", PART,
 "Every feedback job writes a run log and a RESULT line with counts. The failure-mode job failed on 11 Oct, and no alert reached an agent until one was filed by hand (#2538).",
 "Make that job open a concern when it fails, like the other jobs do."),
("Build", "doesnt all the situff exist off the hself. we shouldnt need ot make anything", "chat, 11 Oct", PART,
 "The record format and action types are adopted standards (W3C PROV, Google SRE action types). The pipeline itself is about 177 KB of custom Python.",
 "Landscape review of off-the-shelf feedback/eval tools against what the custom code does."),
("Build", "did you check out my vision repo because this feedback loop i think is very relevant", "chat, 8 Oct 03:37", MET,
 "The plan adopts the vision repo's thesis and its metamodel: a fix's licence is derived by the metamodel's evaluator from two independent sightings.", ""),
]
cls = {NOT: ("not", "Not met"), PART: ("part", "Partly met"), MET: ("met", "Met")}
counts = {k: sum(1 for r in R if r[3] == k) for k in cls}
rows = []
for area, q, src, st, ev, fix in R:
    c, w = cls[st]
    rows.append(f'<tr data-s="{c}"><td data-l="Area">{area}</td><td data-l="You asked for"><q>{html.escape(q)}</q><br><span class="src">{html.escape(src)}</span></td>'
                f'<td data-l="Status"><span class="pill {c}">{w}</span></td><td data-l="What runs">{html.escape(ev)}</td><td data-l="Fix">{html.escape(fix) or "&mdash;"}</td></tr>')
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Feedback requirements check</title>
<style>:root{{--bg:#fff;--fg:#111827;--muted:#4b5563;--line:#d1d5db;--panel:#f3f4f6;--blue:#1d4ed8;--bluefill:#dbeafe;--orange:#b45309;--orangefill:#fff7ed;--grey:#4b5563;--greyfill:#eef0f3}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#0f1420;--fg:#e5e7eb;--muted:#a3adba;--line:#2f3747;--panel:#1a2030;--blue:#7fb2ff;--bluefill:#1e3a5f;--orange:#f5a524;--orangefill:#3a2a10;--grey:#b6bfcc;--greyfill:#202634}}}}
:root[data-theme="dark"]{{--bg:#0f1420;--fg:#e5e7eb;--muted:#a3adba;--line:#2f3747;--panel:#1a2030;--blue:#7fb2ff;--bluefill:#1e3a5f;--orange:#f5a524;--orangefill:#3a2a10;--grey:#b6bfcc;--greyfill:#202634}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
main{{max-width:1200px;margin:0 auto;padding:20px 16px 48px}}h1{{font-size:1.4rem;margin:0 0 8px}}
.q{{border-left:4px solid var(--orange);padding:4px 0 4px 12px;margin:0 0 12px}}.sub{{color:var(--muted);font-size:14px}}
.filters{{position:relative;display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}}
.filters button{{font:inherit;font-size:14px;padding:6px 12px;border-radius:8px;border:2px solid var(--line);background:var(--panel);color:var(--fg);cursor:pointer}}
.filters button[aria-pressed=true]{{border-color:var(--fg);font-weight:700}}
.filters button .tip{{position:absolute;left:0;top:calc(100% + 6px);max-width:min(340px,100%);background:var(--fg);color:var(--bg);font-size:13px;font-weight:400;padding:6px 8px;border-radius:6px;opacity:0;pointer-events:none;transition:opacity .12s;z-index:5}}
.filters button:hover .tip,.filters button:focus-visible .tip{{opacity:1}}
.wrap{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font-size:14px;min-width:820px}}td,th{{border-top:1px solid var(--line);padding:8px;text-align:left;vertical-align:top}}th{{background:var(--panel)}}
th:nth-child(1){{width:80px}}th:nth-child(3){{width:96px}}q{{font-style:italic}}.src{{color:var(--muted);font-size:12px}}
.pill{{display:inline-block;font-size:12px;font-weight:700;padding:2px 8px;border-radius:10px;border:2px solid;white-space:nowrap}}
.pill.met{{color:var(--blue);background:var(--bluefill);border-color:var(--blue)}}.pill.part{{color:var(--grey);background:var(--greyfill);border-style:dashed}}.pill.not{{color:var(--orange);background:var(--orangefill);border-color:var(--orange)}}
a{{color:var(--blue)}}
@media (max-width:700px){{table{{min-width:0}}thead{{display:none}}table,tbody,tr,td{{display:block;width:auto}}tr{{border-top:2px solid var(--line);padding:8px 0}}td{{border:0;padding:3px 0}}td::before{{content:attr(data-l);display:block;font-size:12px;font-weight:700;color:var(--muted)}}tr[hidden]{{display:none}}}}</style></head><body><main>
<h1>Your feedback-system requirements, checked against what runs</h1>
<p class="q">Of the {len(R)} things you asked for, <b>{counts[NOT]} are not met, {counts[PART]} are partly met, and {counts[MET]} are met.</b> The biggest gaps: 9 of the 11 rules in your workspace instructions have no enforcement record or feedback path; the weekly analysis limit leaves 176 repeating problems waiting; and nothing measures whether a lesson is actually reused.</p>
<p class="sub">Each row is your own words with where you said them, then live evidence as of Monday 12 October 2026, read from the jobs' run logs, the scheduled-job list and GitHub. Quotes were read in the original sessions. Written plan documents that only restate these are not listed again. <a href="whole-picture.html">Whole picture</a> &middot; <a href="index.html">plan overview</a></p>
<div class="filters" role="group" aria-label="Filter by status">
<button aria-pressed="true" data-f="all">All ({len(R)})<span class="tip">Show every requirement.</span></button>
<button aria-pressed="false" data-f="not">Not met ({counts[NOT]})<span class="tip">Nothing running does this yet, or the part that does is broken.</span></button>
<button aria-pressed="false" data-f="part">Partly met ({counts[PART]})<span class="tip">Something runs, but it misses part of what you asked for. The gap is in the evidence column.</span></button>
<button aria-pressed="false" data-f="met">Met ({counts[MET]})<span class="tip">Running and checked today against its logs or GitHub.</span></button>
</div>
<div class="wrap"><table><thead><tr><th>Area</th><th>What you asked for</th><th>Status</th><th>What actually runs (12 Oct)</th><th>Fix</th></tr></thead><tbody>
{''.join(rows)}
</tbody></table></div>
<p class="sub">Sources: <code>~/projects/data/feedback-collector/</code> (runs.jsonl, problems-runs.jsonl, fix-owner-runs.jsonl, effects-2026-10-12.jsonl, policies-runs.jsonl); <code>systemctl --user list-timers</code>; GitHub issues in the AES and project-meta repositories; the rule check is <code>scripts/learning_loop/policies.py</code>. No private feedback text is on this page; only your own quoted words and counts.</p>
</main><script>
document.querySelectorAll('.filters button').forEach(b=>b.addEventListener('click',()=>{{
document.querySelectorAll('.filters button').forEach(x=>x.setAttribute('aria-pressed',x===b));
const f=b.dataset.f;document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!(f==='all'||r.dataset.s===f));}}));
</script></body></html>"""
OUT.write_text(page)
print(f"rows={len(R)} not={counts[NOT]} part={counts[PART]} met={counts[MET]}")

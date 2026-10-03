#!/usr/bin/env python3
"""Build Brian's hive-brain dashboard page (hive brain v1).

One phone-first page answering: is it working, how close is v1, what is waiting
on Brian; then, on tap, the plan, what the agents are doing, what is built, and
the health checks. Design: Representation Router recommendation (list primary,
status line, details on demand), use case in scripts/hive/dashboard-use-case.json.

  python3 scripts/hive/dashboard.py --out <file.html>

Sources: the Paperclip board (scripts/hive/board.sh), scripts/hive/controls.py,
the roadmap's Capabilities table, and scripts/hive/conditions.json (progress on
the five done-conditions, updated by hand with evidence). The page is a
snapshot: it states when it was built. Exit 2 if the board cannot be read.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C = "da165590-b0b3-4bf9-bb7f-e455292df499"
BRIAN = "Fr6jPHXrgB7tlyFcDMdJEiKNmBk2vjAl"
AGENT_JOB = {
    "Coordinator": "plans: picks pilot work from your weekly plan and assigns it",
    "Research and Code Review": "builds: researches, writes code, opens pull requests",
    "Brian Contact": "messages you (Telegram, currently unused)",
}
CAP_PLAIN = {
    "C-ORCH": "Running the agents", "C-MSG": "Agents talking to each other", "C-HUMAN-IF": "Reaching you",
    "C-IDENTITY": "One brain per project", "C-KNOW": "Where knowledge lives", "C-CONTEXT": "Keeping context fresh",
    "C-GOV": "Rules and safety", "C-LEARN": "Learning from mistakes", "C-EVAL": "Measuring how it's doing",
    "C-RUNTIME": "The server it runs on",
}
e = html.escape


def board(path: str):
    r = subprocess.run(["bash", str(HERE / "board.sh"), "GET", path], capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:200])
    return json.loads(r.stdout)


def ago(s: str | None) -> str:
    if not s:
        return "never"
    d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    h = (dt.datetime.now(dt.timezone.utc) - d).total_seconds() / 3600
    return "just now" if h < 1 else (f"{h:.0f} h ago" if h < 48 else f"{h / 24:.0f} days ago")


def pill(kind: str, text: str) -> str:
    return f'<span class="pill {kind}">{e(text)}</span>'


def capabilities() -> list[dict]:
    text = (ROOT / "proposals/hive-brain-v1/ROADMAP.md").read_text()
    rows = []
    for line in text.splitlines():
        m = re.match(r"^\| (C-[A-Z-]+) [^|]*\| ([^|]*)\| ([^|]*)\| ([^|]*)\|$", line)
        if m:
            rows.append({"id": m.group(1), "tool": m.group(2).strip(), "state": m.group(3).strip(), "needed": m.group(4).strip()})
    return rows


def md(s: str) -> str:
    """Escape, then turn `code` into <code>."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", e(s))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()
    built = dt.datetime.now(dt.timezone.utc)
    try:
        issues = board(f"/api/companies/{C}/issues")
        issues = issues if isinstance(issues, list) else issues.get("issues", [])
        runs = board(f"/api/companies/{C}/heartbeat-runs?limit=100")
        runs = runs if isinstance(runs, list) else runs.get("runs", [])
        agents = board(f"/api/companies/{C}/agents")
        agents = agents if isinstance(agents, list) else agents.get("agents", [])
    except (RuntimeError, ValueError, subprocess.TimeoutExpired) as err:
        print(f"dashboard: could not read the Paperclip board: {err}", file=sys.stderr)
        return 2
    cond = json.loads((HERE / "conditions.json").read_text())
    ctl = subprocess.run([sys.executable, str(HERE / "controls.py")], capture_output=True, text=True, timeout=400)
    ctl_rows = []
    for line in ctl.stdout.splitlines()[:-1]:
        m = re.match(r"^(.*?)\s{2,}last (.*?)\s{2,}normal gap .*?\s{2,}(\S.*)$", line)
        if m:
            ctl_rows.append((m.group(1).strip(), m.group(2).strip(), m.group(3).strip()))
    ctl_ok = ctl.returncode == 0

    # Agents and their latest run
    names = {x["id"]: x["name"] for x in agents}
    agent_rows, broken = [], 0
    for x in agents:
        mine = sorted((r for r in runs if r.get("agentId") == x["id"]), key=lambda r: r.get("startedAt") or "", reverse=True)
        last = mine[0] if mine else None
        status = last["status"] if last else "no runs"
        bad = status == "failed"
        broken += bad
        agent_rows.append((x["name"], AGENT_JOB.get(x["name"], ""), status, ago(last["startedAt"]) if last else "never", bad))

    open_tasks = [i for i in issues if i.get("status") not in ("done", "cancelled")]
    waiting = [i for i in open_tasks if i.get("assigneeUserId") == BRIAN]
    recent_done = sorted((i for i in issues if i.get("status") == "done"), key=lambda i: i.get("updatedAt") or "", reverse=True)[:4]
    done_n = sum(c["status"] == "done" for c in cond["conditions"])
    pilot = next(c for c in cond["conditions"] if c["n"] == 1)

    # Answer strip
    working = broken == 0 and ctl_ok
    strip = [
        ("Working right now?", pill("ok" if working else "warn", "Yes" if working else "Needs attention"),
         f"{len(agents) - broken} of {len(agents)} agents' last run succeeded; {sum(r[2] == 'ok' for r in ctl_rows)} of {len(ctl_rows)} health checks ok"),
        ("How close is v1?", pill("ok" if done_n == 5 else "mid", f"{done_n} of 5 done"),
         f"all five under way; pilot {pilot['progress']}"),
        ("Waiting on you?", pill("warn" if waiting else "ok", f"{len(waiting)} item{'s' if len(waiting) != 1 else ''}" if waiting else "Nothing"),
         "; ".join(i["title"] for i in waiting)[:200] if waiting else "agents are working on their own"),
    ]
    p = []
    p.append('<title>Is my hive brain working?</title>')
    p.append(STYLE)
    p.append('<main><header><h1>Is my hive brain working?</h1>'
             f'<p class="sub">Your personal hive brain: you, three AI agents on your server, and one brain per project. Snapshot built {built:%a %d %b, %H:%M} UTC.</p></header>')
    p.append('<section class="strip">' + "".join(
        f'<div class="ans"><div class="q">{e(q)}</div><div class="a">{a_}</div><div class="why">{e(w)}</div></div>' for q, a_, w in strip) + "</section>")

    # The plan: five conditions (primary)
    kind = {"done": "ok", "partway": "mid", "not_started": "idle"}
    word = {"done": "Done", "partway": "Under way", "not_started": "Not started"}
    p.append('<section><h2>The plan: five things that make v1 done</h2><ol class="conds">')
    for c in cond["conditions"]:
        p.append(f'<li><details><summary><span class="cname">{e(c["name"])}</span>{pill(kind[c["status"]], word[c["status"]])}'
                 f'<span class="prog">{e(c["progress"])}</span></summary>'
                 f'<p>{e(c["plain"])}</p><p><b>So far:</b> {md(c["evidence"])}</p><p><b>Next:</b> {md(c["next"])}</p></details></li>')
    p.append(f'</ol><p class="note">Progress last updated {e(cond["updated"])} by the terminal session, with evidence.</p></section>')

    # What it is doing now
    p.append('<section><h2>What the agents are doing</h2><ul class="rows">')
    for name, job, status, when, bad in agent_rows:
        p.append(f'<li><div class="row"><b>{e(name)}</b>{pill("warn" if bad else ("ok" if status == "succeeded" else "idle"), "last run failed" if bad else ("last run ok" if status == "succeeded" else status))}</div>'
                 f'<div class="meta">{e(job)} · last ran {e(when)}</div></li>')
    p.append("</ul><h3>Open tasks</h3><ul class=\"rows\">")
    for i in sorted(open_tasks, key=lambda i: i["identifier"]):
        who = "you" if i.get("assigneeUserId") == BRIAN else names.get(i.get("assigneeAgentId"), "nobody")
        p.append(f'<li><div class="row"><span>{e(i["title"])}</span>{pill("warn" if who == "you" else "idle", i["status"].replace("_", " "))}</div>'
                 f'<div class="meta">{e(i["identifier"])} · with {e(who)}</div></li>')
    if not open_tasks:
        p.append('<li class="meta">No open tasks.</li>')
    p.append("</ul><h3>Recently finished</h3><ul class=\"rows\">")
    for i in recent_done:
        p.append(f'<li><div class="row"><span>{e(i["title"])}</span>{pill("ok", "done")}</div><div class="meta">{e(i["identifier"])} · {e(ago(i.get("updatedAt")))}</div></li>')
    p.append('</ul><p class="note">Live board: <a href="https://paperclip.brianmills.dev/BRI/issues">paperclip.brianmills.dev</a></p></section>')

    # What is built
    p.append('<section><h2>What has been built</h2><p class="note">Ten capabilities from your AI Astronauts hive-brain design. Tap one for its tool and what v1 still needs.</p><ul class="rows">')
    for c in capabilities():
        p.append(f'<li><details><summary><span>{e(CAP_PLAIN.get(c["id"], c["id"]))}</span><span class="meta">{e(c["id"])}</span></summary>'
                 f'<p><b>Tool:</b> {md(c["tool"])}</p><p><b>State:</b> {md(c["state"])}</p><p><b>Still needed for v1:</b> {md(c["needed"])}</p></details></li>')
    p.append("</ul></section>")

    # Health checks
    p.append('<section><h2>Health checks</h2><p class="note">Each check asks whether one part of the system has done its job recently. One goes quiet or fails, and this list says so.</p><ul class="rows">')
    for name, last, status in ctl_rows:
        ok = status == "ok"
        p.append(f'<li><div class="row"><span>{e(name)}</span>{pill("ok" if ok else "warn", "ok" if ok else status.split(":")[0].lower())}</div>'
                 f'<div class="meta">last activity {e(last)}{"" if ok else " · " + e(status)}</div></li>')
    p.append('</ul></section>')
    p.append(f'<footer class="note">Built by <code>scripts/hive/dashboard.py</code> in agentic-engineering-system-canonical from the Paperclip board, '
             f'the health checks, the roadmap and <code>conditions.json</code>, {built:%Y-%m-%d %H:%M} UTC. '
             'Colours: blue = fine, orange = needs a look, grey = waiting or idle; every colour also has a word.</footer></main>')
    a.out.write_text("\n".join(p))
    print(f"dashboard: wrote {a.out} ({a.out.stat().st_size} bytes); agents broken {broken}, waiting on Brian {len(waiting)}, controls exit {ctl.returncode}")
    return 0


STYLE = """<style>
/* Layout: one narrow column, answer strip first, then tap-to-open sections. */
:root{--bg:#f6f7f9;--card:#ffffff;--fg:#1d2430;--muted:#5d6878;--line:#dde2ea;--ok:#1f5fbf;--ok-bg:#e3edfb;--warn:#a85300;--warn-bg:#fdecd9;--idle:#5d6878;--idle-bg:#eceff3;--mid:#3d4f7a;--mid-bg:#e6e9f3;
--display:"Fraunces",Georgia,serif;--body:"IBM Plex Sans",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#11151c;--card:#1a202a;--fg:#e6eaf0;--muted:#9aa6b6;--line:#2c3442;--ok:#8ab4ff;--ok-bg:#1d2c47;--warn:#ffb36b;--warn-bg:#3a2714;--idle:#9aa6b6;--idle-bg:#252c38;--mid:#b9c4e4;--mid-bg:#262e45;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#11151c;--card:#1a202a;--fg:#e6eaf0;--muted:#9aa6b6;--line:#2c3442;--ok:#8ab4ff;--ok-bg:#1d2c47;--warn:#ffb36b;--warn-bg:#3a2714;--idle:#9aa6b6;--idle-bg:#252c38;--mid:#b9c4e4;--mid-bg:#262e45;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font:15px/1.5 var(--body)}
main{max-width:42rem;margin:0 auto;padding-inline:16px;padding-block:20px 40px;display:grid;gap:22px}
h1{font:600 1.7rem/1.15 var(--display);margin:0;text-wrap:balance}
h2{font:600 1.15rem/1.3 var(--display);margin:0 0 10px}
h3{font-size:.8rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:16px 0 6px}
.sub,.note,.meta{color:var(--muted);font-size:.85rem;margin:4px 0 0}
.strip{display:grid;gap:10px}
.ans{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;display:grid;grid-template-columns:1fr auto;gap:2px 10px}
.ans .q{font-weight:600}.ans .a{grid-row:span 2;align-self:center}.ans .why{color:var(--muted);font-size:.85rem;min-width:0}
.pill{display:inline-block;font-size:.75rem;font-weight:600;padding:2px 9px;border-radius:999px;white-space:nowrap}
.ok{color:var(--ok);background:var(--ok-bg)}.warn{color:var(--warn);background:var(--warn-bg);outline:1px dashed var(--warn)}.idle{color:var(--idle);background:var(--idle-bg)}.mid{color:var(--mid);background:var(--mid-bg)}
ol.conds,ul.rows{list-style:none;margin:0;padding:0;display:grid;gap:8px}
ol.conds>li,ul.rows>li{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px;min-width:0}
summary{cursor:pointer;display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px}
summary:focus-visible{outline:2px solid var(--ok);outline-offset:3px}
.cname{font-weight:600}.prog{color:var(--muted);font-size:.85rem;margin-left:auto}
details p{margin:8px 0 0;font-size:.9rem}
.row{display:flex;justify-content:space-between;gap:10px;align-items:baseline}.row>span{min-width:0}
code{font-family:var(--mono);font-size:.82em;overflow-wrap:anywhere}
a{color:var(--ok)}footer{padding-top:6px;border-top:1px solid var(--line)}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=IBM+Plex+Mono&family=IBM+Plex+Sans:wght@400;600&display=swap">"""


if __name__ == "__main__":
    sys.exit(main())

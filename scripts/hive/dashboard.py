#!/usr/bin/env python3
"""Build Brian's hive-brain dashboard page (hive brain v1).

Five phone screens, each question in the form that answers it (Brian's
AI Astronauts design plus Representation Router; picked from a ChatGPT sketch
2026-10-03):
  Map       what the system is made of: you, the communication route, project
            brains, agents, tools (a drawn graph);
  Live      what is happening now: work in progress and just finished (a feed);
  Path      the way to v1: the five done-conditions as a path, each step with
            what it waits on;
  Decisions what needs you: one item at a time with the recommendation;
  Health    is anything broken or gone quiet (calm list, the quiet one stands out).

  python3 scripts/hive/dashboard.py --out <file.html>

Sources: the Paperclip board (scripts/hive/board.sh), scripts/hive/controls.py,
and scripts/hive/conditions.json (progress on the five conditions plus any
decisions held in the terminal session). The page is a snapshot and says when
it was built. Exit 2 if the board cannot be read.
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
C = "da165590-b0b3-4bf9-bb7f-e455292df499"
BRIAN = "Fr6jPHXrgB7tlyFcDMdJEiKNmBk2vjAl"
AGENT_JOB = {"Coordinator": "plans the work", "Research and Code Review": "builds and reviews",
             "Brian Contact": "messages you"}
PROJECT_REPOS = ["agentic-engineering-system-canonical", "theory-forge", "cybernetic_influence_v3", "personal-wiki", "portfolio"]
SHORT = {"agentic-engineering-system-canonical": "AES", "cybernetic_influence_v3": "Cybernetic", "personal-wiki": "Personal wiki",
         "theory-forge": "Theory Forge", "portfolio": "Portfolio"}
e = html.escape


def board(path: str):
    r = subprocess.run(["bash", str(HERE / "board.sh"), "GET", path], capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:200])
    d = json.loads(r.stdout)
    return d if isinstance(d, list) else next((v for v in d.values() if isinstance(v, list)), [])


def ago(s: str | None) -> str:
    if not s:
        return "never"
    d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    if d.tzinfo is None:
        d = d.astimezone()
    m = (dt.datetime.now(dt.timezone.utc) - d).total_seconds() / 60
    return "just now" if m < 2 else (f"{m:.0f} min ago" if m < 90 else (f"{m / 60:.0f} h ago" if m < 2880 else f"{m / 1440:.0f} days ago"))


def md(s: str) -> str:
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", e(s))


def brain_ok(repo: str) -> bool | None:
    p = Path.home() / "code" / repo
    if not (p / ".project-brain").exists():
        return None
    return subprocess.run([sys.executable, str(HERE / "brain_fresh.py"), str(p)], capture_output=True).returncode == 0


def map_svg(agents, busy: set[str]) -> str:
    """You at the top, the communication route, project brains around it, agents and tools below."""
    W = 360
    out = [f'<svg viewBox="0 0 {W} 520" role="img" aria-label="Map of the hive brain">']
    def node(x, y, label, sub, kind, href=""):
        cls = {"you": "n-you", "hub": "n-hub", "on": "n-on", "off": "n-off", "tool": "n-tool"}[kind]
        out.append(f'<g class="node {cls}" tabindex="0" data-info="{e(sub)}"><rect x="{x-54}" y="{y-20}" width="108" height="40" rx="12"/>'
                   f'<text x="{x}" y="{y-3}" class="t1">{e(label)}</text><text x="{x}" y="{y+12}" class="t2">{e(sub.split(" · ")[0])}</text></g>')
    def line(x1, y1, x2, y2, on=False):
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{"edge-on" if on else "edge"}"/>')
    projects = [(r, brain_ok(r)) for r in PROJECT_REPOS]
    you, hub = (180, 36), (180, 116)
    agent_pos = [(60, 206), (180, 206), (300, 206)]
    proj_pos = [(60, 306), (180, 306), (300, 306), (120, 366), (240, 366)]
    tool_pos = [(60, 466), (180, 466), (300, 466)]
    line(*you, *hub, True)
    for x, y in agent_pos:
        line(*hub, x, y, agents and agents[agent_pos.index((x, y))]["name"] in busy if agent_pos.index((x, y)) < len(agents) else False)
    for x, y in proj_pos:
        line(180, 206, x, y)
    for x, y in tool_pos:
        line(x, y - 20, x, 386 if x != 180 else 386)
    node(*you, "You", "the one who decides", "you")
    node(*hub, "Terminal relay", "communication route · decisions come to you here, one at a time", "hub")
    for (x, y), a in zip(agent_pos, agents):
        node(x, y, {"Brian Contact": "Contact"}.get(a["name"], a["name"].split(" ")[0]), f"{AGENT_JOB.get(a['name'], '')} · {'working now' if a['name'] in busy else 'idle'}",
             "on" if a["name"] in busy else "off")
    for (x, y), (r, ok) in zip(proj_pos, projects):
        state = "brain fresh" if ok else ("brain stale" if ok is False else "no brain yet")
        node(x, y, SHORT[r], f"{state} · project {r}", "on" if ok else "off")
    for (x, y), (t, sub) in zip(tool_pos, [("Safety rules", "checks commands · Jev gate and CC Safety Net"),
                                         ("Learning loop", "issues to rules · GitHub issues, labelled weekly"),
                                         ("Server", "personal-vps · agents run here, backed up nightly")]):
        node(x, y, t, sub, "tool")
    out.append('<text x="180" y="262" class="t2">projects (each with its own brain)</text>')
    out.append('<text x="180" y="426" class="t2">what keeps it safe and running</text>')
    out.append("</svg>")
    return "".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()
    built = dt.datetime.now(dt.timezone.utc)
    try:
        issues = board(f"/api/companies/{C}/issues")
        runs = board(f"/api/companies/{C}/heartbeat-runs?limit=100")
        agents = board(f"/api/companies/{C}/agents")
    except (RuntimeError, ValueError, subprocess.TimeoutExpired) as err:
        print(f"dashboard: could not read the Paperclip board: {err}", file=sys.stderr)
        return 2
    cond = json.loads((HERE / "conditions.json").read_text())
    ctl = subprocess.run([sys.executable, str(HERE / "controls.py")], capture_output=True, text=True, timeout=400)
    ctl_rows = [(m.group(1).strip(), m.group(2).strip(), m.group(3).strip()) for line in ctl.stdout.splitlines()[:-1]
                if (m := re.match(r"^(.*?)\s{2,}last (.*?)\s{2,}normal gap .*?\s{2,}(\S.*)$", line))]
    names = {x["id"]: x["name"] for x in agents}
    latest = {}
    for r in sorted(runs, key=lambda r: r.get("startedAt") or ""):
        latest[r.get("agentId")] = r
    busy = {names[k] for k, r in latest.items() if k in names and r.get("status") in ("running", "queued")}
    broken = [names[k] for k, r in latest.items() if k in names and r.get("status") == "failed"]
    open_t = [i for i in issues if i.get("status") not in ("done", "cancelled")]
    waiting = [i for i in open_t if i.get("assigneeUserId") == BRIAN]
    held = cond.get("decisions_in_terminal", [])
    done_t = sorted((i for i in issues if i.get("status") == "done"), key=lambda i: i.get("updatedAt") or "", reverse=True)[:5]
    quiet = [r for r in ctl_rows if r[2] != "ok"]
    n_need = len(waiting) + len(held)

    p = ['<title>Is my hive brain working?</title>', STYLE, '<div class="app">']
    p.append(f'<header class="top"><b>Hive brain</b><span>snapshot {built:%a %H:%M} UTC</span></header>')

    # Map
    p.append('<section class="screen" id="map"><h1>The big picture</h1><p class="sub">How everything fits together. Tap a box to see what it is.</p>')
    p.append(map_svg(agents, busy))
    p.append('<p class="info" id="info">Blue = active or fresh. Grey = idle or not set up yet.</p></section>')

    # Live
    p.append('<section class="screen" id="live" hidden><h1>What\'s happening right now</h1><p class="sub">Work in motion, newest first.</p><ol class="feed">')
    for i in sorted(open_t, key=lambda i: i.get("updatedAt") or "", reverse=True):
        who = "you" if i.get("assigneeUserId") == BRIAN else names.get(i.get("assigneeAgentId"), "nobody")
        p.append(f'<li class="now"><span class="dot"></span><div><b>{e(i["title"])}</b><span class="m">with {e(who)} · {e(i["status"].replace("_", " "))} · {e(ago(i.get("updatedAt")))}</span></div></li>')
    p.append('</ol><h2>Just finished</h2><ol class="feed">')
    for i in done_t:
        p.append(f'<li class="done"><span class="dot"></span><div><b>{e(i["title"])}</b><span class="m">done · {e(ago(i.get("updatedAt")))}</span></div></li>')
    p.append('</ol></section>')

    # Path
    p.append('<section class="screen" id="path" hidden><h1>Path to v1</h1><p class="sub">Five things make the first version done. Each says what it is waiting on.</p><ol class="path">')
    for c in cond["conditions"]:
        st = {"done": "done", "partway": "underway", "not_started": "todo"}[c["status"]]
        p.append(f'<li class="{st}"><span class="dot"></span><details><summary><b>{e(c["name"])}</b><span class="m">{e(c["progress"])}</span></summary>'
                 f'<p>{e(c["plain"])}</p><p><b>So far:</b> {md(c["evidence"])}</p><p class="wait"><b>Waiting on:</b> {md(c["next"])}</p></details></li>')
    p.append(f'</ol><p class="sub">Updated {e(cond["updated"])} with evidence.</p></section>')

    # Decisions
    p.append(f'<section class="screen" id="decide" hidden><h1>{"Nothing needs you" if not n_need else ("You have a decision" if n_need == 1 else f"You have {n_need} decisions")}</h1>')
    p.append('<p class="sub">The communication route brings you only what needs you, one at a time. Answer in the terminal or on the board.</p>')
    for i in waiting:
        p.append(f'<article class="decision"><b>{e(i["title"])}</b><p>{e((i.get("description") or "")[:420])}</p>'
                 f'<a class="btn" href="https://paperclip.brianmills.dev/BRI/issues/{e(i["identifier"])}">Open {e(i["identifier"])}</a></article>')
    for d in held:
        p.append(f'<article class="decision"><b>{e(d["question"])}</b><p>{md(d["context"])}</p><p class="rec"><b>Recommended:</b> {md(d["recommendation"])}</p>'
                 f'<div class="opts">' + "".join(f'<span class="opt">{e(o)}</span>' for o in d["options"]) + '</div><p class="m">Reply in the terminal session.</p></article>')
    if not n_need:
        p.append('<p class="calm">The agents are working on their own. You will see a decision here when one needs you.</p>')
    p.append('</section>')

    # Health
    p.append(f'<section class="screen" id="health" hidden><h1>System health</h1><p class="sub">Each check asks whether one part did its job recently.</p>'
             f'<div class="overall {"ok" if not quiet and not broken else "warn"}"><b>{"Everything is running" if not quiet and not broken else "Something needs a look"}</b>'
             f'<span>{len(ctl_rows) - len(quiet)} of {len(ctl_rows)} checks fine{"; agent failing: " + ", ".join(broken) if broken else ""}</span></div><ul class="checks">')
    for name, last, status in sorted(ctl_rows, key=lambda r: r[2] == "ok"):
        ok = status == "ok"
        p.append(f'<li class="{"ok" if ok else "warn"}"><span>{e(name)}</span><span class="m">{e("fine" if ok else status)} · {e(last)}</span></li>')
    p.append('</ul></section>')

    p.append(f'<nav class="tabs">' + "".join(
        f'<button data-s="{s}"{" aria-current=\"page\"" if s == "map" else ""}>{l}{" <i>" + str(n_need) + "</i>" if s == "decide" and n_need else ""}</button>'
        for s, l in [("map", "Map"), ("live", "Live"), ("path", "Path"), ("decide", "Decisions"), ("health", "Health")]) + "</nav></div>")
    p.append(SCRIPT)
    a.out.write_text("\n".join(p))
    print(f"dashboard: wrote {a.out} ({a.out.stat().st_size} bytes); busy {sorted(busy)}, broken {broken}, "
          f"decisions {n_need}, checks not ok {len(quiet)}, controls exit {ctl.returncode}")
    return 0


STYLE = """<style>
/* Layout: phone app, five screens behind a bottom tab bar; blue / orange / grey with words (red-green colourblind). */
:root{--bg:#f3f5f9;--card:#fff;--fg:#1b2333;--mute:#64708a;--line:#dbe1ea;--on:#1f5fbf;--on-bg:#e4edfb;--warn:#a65200;--warn-bg:#fdeedd;--off:#8b95a7;--off-bg:#eef1f5;
--body:"IBM Plex Sans",system-ui,sans-serif;--display:"Fraunces",Georgia,serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#10141b;--card:#1a2029;--fg:#e7ebf1;--mute:#9aa5b8;--line:#2b3340;--on:#8ab4ff;--on-bg:#1c2b45;--warn:#ffb26a;--warn-bg:#3a2713;--off:#7d889b;--off-bg:#232a35;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#10141b;--card:#1a2029;--fg:#e7ebf1;--mute:#9aa5b8;--line:#2b3340;--on:#8ab4ff;--on-bg:#1c2b45;--warn:#ffb26a;--warn-bg:#3a2713;--off:#7d889b;--off-bg:#232a35;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font:15px/1.45 var(--body)}
.app{max-width:30rem;margin:0 auto;padding-inline:16px;padding-block:8px 84px}
.top{display:flex;justify-content:space-between;align-items:baseline;padding-block:8px}.top span{color:var(--mute);font-size:.8rem}
h1{font:600 1.45rem/1.2 var(--display);margin:6px 0 2px;text-wrap:balance}h2{font-size:.8rem;text-transform:uppercase;letter-spacing:.06em;color:var(--mute);margin:18px 0 6px}
.sub,.m,.info{color:var(--mute);font-size:.84rem}.m{display:block}
svg{width:100%;height:auto;margin-top:8px}.edge{stroke:var(--line);stroke-width:2}.edge-on{stroke:var(--on);stroke-width:3}
.node rect{fill:var(--card);stroke:var(--line);stroke-width:1.5}.node{cursor:pointer}.node:focus rect,.node:hover rect{stroke:var(--fg)}
.t1{font:600 12px var(--body);fill:var(--fg);text-anchor:middle}.t2{font:10px var(--body);fill:var(--mute);text-anchor:middle}
.n-you rect{fill:var(--fg)}.n-you .t1,.n-you .t2{fill:var(--bg)}.n-hub rect,.n-on rect{fill:var(--on-bg);stroke:var(--on)}.n-hub .t1,.n-on .t1{fill:var(--on)}
.n-off rect{fill:var(--off-bg);stroke-dasharray:4 3}.n-tool rect{fill:var(--card);stroke:var(--mute)}
.info{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
ol.feed,ol.path,ul.checks{list-style:none;margin:10px 0 0;padding:0;display:grid;gap:8px}
ol.feed li,ol.path li{display:grid;grid-template-columns:14px 1fr;gap:10px;align-items:start}
.dot{width:12px;height:12px;border-radius:99px;margin-top:5px;border:2px solid var(--off);background:var(--card)}
.feed .now .dot,.path .underway .dot{border-color:var(--on);background:var(--on-bg)}.feed .done .dot,.path .done .dot{border-color:var(--on);background:var(--on)}
.feed li>div,.path details{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:9px 12px;min-width:0}
.path summary{cursor:pointer}.path details p{margin:8px 0 0;font-size:.88rem}.wait{color:var(--warn)}
.decision{background:var(--card);border:1px solid var(--warn);border-radius:12px;padding:12px 14px;margin-top:12px}.decision p{font-size:.9rem;margin:8px 0 0}
.rec{background:var(--on-bg);border-radius:8px;padding:8px 10px}.opts{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.opt{border:1px solid var(--on);color:var(--on);border-radius:99px;padding:3px 10px;font-size:.82rem}
.btn{display:inline-block;margin-top:10px;background:var(--on);color:var(--bg);border-radius:10px;padding:8px 14px;text-decoration:none;font-weight:600}
.calm{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin-top:12px}
.overall{border-radius:12px;padding:12px 14px;margin-top:12px;display:grid}.overall.ok{background:var(--on-bg);color:var(--on)}.overall.warn{background:var(--warn-bg);color:var(--warn)}
ul.checks li{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:9px 12px}ul.checks li.warn{border:1px dashed var(--warn);background:var(--warn-bg)}
ul.checks li span:first-child{font-weight:600;display:block}
code{font-size:.82em;overflow-wrap:anywhere}
.tabs{position:fixed;left:0;right:0;bottom:0;background:var(--card);border-top:1px solid var(--line);display:flex;justify-content:space-around;padding:8px 6px calc(8px + env(safe-area-inset-bottom,0px))}
.tabs button{background:none;border:0;color:var(--mute);font:600 .78rem var(--body);padding:6px 4px;cursor:pointer}.tabs button[aria-current]{color:var(--on)}
.tabs i{font-style:normal;background:var(--warn);color:var(--bg);border-radius:99px;padding:0 6px;margin-left:3px}
.tabs button:focus-visible,summary:focus-visible{outline:2px solid var(--on);outline-offset:2px}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=IBM+Plex+Sans:wght@400;600&display=swap">"""

SCRIPT = """<script>
const tabs=[...document.querySelectorAll('.tabs button')];
function show(s){document.querySelectorAll('.screen').forEach(x=>x.hidden=x.id!==s);tabs.forEach(b=>b.toggleAttribute('aria-current',b.dataset.s===s));try{localStorage.setItem('hive-tab',s)}catch(e){}}
tabs.forEach(b=>b.addEventListener('click',()=>show(b.dataset.s)));
const h=location.hash.slice(1);let saved=null;try{saved=localStorage.getItem('hive-tab')}catch(e){}
if(h&&document.getElementById(h))show(h);else if(saved&&document.getElementById(saved))show(saved);
const info=document.getElementById('info');
document.querySelectorAll('.node').forEach(n=>{const f=()=>{info.textContent=n.querySelector('.t1').textContent+': '+n.dataset.info};n.addEventListener('click',f);n.addEventListener('keydown',ev=>{if(ev.key==='Enter')f()})});
</script>"""


if __name__ == "__main__":
    sys.exit(main())

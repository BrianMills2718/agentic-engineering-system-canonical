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

  python3 scripts/hive/dashboard.py --out <file.html>            # snapshot, on Brian's PC
  python3 scripts/hive/dashboard.py --vps --wsl-controls <json> \
      --out <index.html> --json-out <status.json>                  # hosted, on the VPS

Sources: the Paperclip board (scripts/hive/board.sh), the controls checks
(scripts/hive/controls.py), and scripts/hive/conditions.json (progress on the
five conditions plus any decisions held in the terminal session).

--vps is the hosted mode (personal-vps apps/hive-dashboard, rebuilt every minute
by a timer; the open page reloads itself when what it shows changed): board calls run on the VPS itself (HIVE_BOARD_LOCAL=1, no
ssh); checks only Brian's PC can see come from the JSON his PC pushes up
(scripts/hive/push_controls.sh), and the VPS-side checks are measured here.
Decision cards get one-tap answer buttons that post to the page's own server
(personal-vps apps/hive-dashboard/server.py), which comments on the Paperclip
task. --json-out writes the small status file that server hands the page's
(and, beside it, status-full.json: every check, condition, brain, cost and decision for the Glance page)
30-second poll.

Every data source is shown with its age. A source past its normal age is
STALE and a missing one is UNKNOWN; neither is ever shown as fine. Exit 2 if
the board cannot be read (the previous page stays in place).
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
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
BRIAN_THREAD = "BRI-2"  # Brian's Telegram-bound conversation with the Brian Contact agent
WSL_REPORT_MAX = dt.timedelta(hours=26)  # hive-controls.timer runs daily on Brian's PC
BUILD_MAX_MIN = 5  # the VPS timer rebuilds every minute; a few missed builds = stale
TAB_TIP = {"map": "What the system is made of. Tap any box to open it.", "live": "What happened in the last 24 hours, and your message thread.",
           "path": "The five conditions for v1, and how far each one is.", "decide": "Anything waiting on your answer.",
           "health": "Whether each part of the system did its job recently."}
ANSWER_OPTIONS = ["Yes, go with the recommendation", "No, don't do it", "Tell me more first"]


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


def parse_ts(s: str | None) -> dt.datetime | None:
    if not s:
        return None
    d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    return d if d.tzinfo else d.astimezone()


def brain_local(repo: str) -> str:
    """fresh / stale / none, measured on this machine (Brian's PC)."""
    p = Path.home() / "code" / repo
    if not (p / ".project-brain").exists():
        return "none"
    ok = subprocess.run([sys.executable, str(HERE / "brain_fresh.py"), str(p)], capture_output=True).returncode == 0
    return "fresh" if ok else "stale"


def brain_from_rows(repo: str, rows: list[dict], report_ok: bool) -> str:
    """fresh / stale / none / unknown, from the controls report Brian's PC pushed up."""
    if not report_ok:
        return "unknown"
    row = next((r for r in rows if r["name"] == f"Project brain: {repo}"), None)
    if row is None:
        return "none"
    return {"ok": "fresh", "STALE": "stale"}.get(row["status"], "unknown")


BRAIN_LABEL = {"fresh": "brain fresh", "stale": "brain stale", "none": "no brain yet", "unknown": "brain status unknown"}



def _ts(v):
    if not v:
        return None
    d = dt.datetime.fromisoformat(str(v).replace("Z", "+00:00"))
    return d if d.tzinfo else d.astimezone()


def _wrap(t: str, n: int) -> list[str]:
    """Every word of t, in lines of at most n characters (a longer word gets a line of its own). Never shortened."""
    lines, cur = [], ""
    for w in " ".join((t or "").split()).split(" "):
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    return lines + [cur] if cur else lines or [""]


def _fraction(c: dict) -> tuple[float, str]:
    """How far one condition is, from its numeric fields, else its status."""
    if isinstance(c.get("steps_done"), (int, float)) and c.get("steps_total"):
        return max(0.0, min(1.0, c["steps_done"] / c["steps_total"])), f'{c["steps_done"]:g}/{c["steps_total"]:g}'
    m = re.search(r"(\d+)\s+of\s+(\d+)", c.get("progress") or "")
    if m and int(m.group(2)):
        return int(m.group(1)) / int(m.group(2)), f"{m.group(1)}/{m.group(2)}"
    return {"done": (1.0, "done"), "not_started": (0.0, "")}.get(c.get("status"), (0.5, ""))


def path_svg(conds: list[dict]) -> str:
    """The five done-conditions as stations on one line, each filled by its progress."""
    L = 13  # line height of the small text
    plan, y = [], 40
    for c in conds:
        f, lab = _fraction(c)
        done = c.get("status") == "done" or f >= 1
        prog = _wrap("done" if done else (c.get("progress") or ""), 44)
        wait = [] if done else _wrap("waiting on: " + (c.get("next") or ""), 44)
        plan.append((c, y, f, lab, done, prog, wait))
        y += max(70, 30 + L * (len(prog) + len(wait)) + 22)
    H = y
    out = [f'<svg viewBox="0 0 360 {H}" role="img" aria-label="Path to v1">',
           f'<line x1="40" y1="40" x2="40" y2="{plan[-1][1] if plan else 40}" class="edge"/>']
    for c, y, f, lab, done, prog, wait in plan:
        r, circ = 22, 2 * 3.14159 * 22
        cls = "st-done" if done else ("st-todo" if f == 0 else "st-on")
        tip = f'{c["name"]}: {c.get("plain") or ""} Status: {"done" if done else (c.get("progress") or "")}'
        out.append(f'<g class="station {cls}" tabindex="0" data-tip="{e(tip)}"><title>{e(tip)}</title><circle cx="40" cy="{y}" r="{r}" class="ring"/>')
        if done:
            out.append(f'<circle cx="40" cy="{y}" r="{r}" class="fill"/><path d="M30 {y} l7 7 l13 -14" class="tick"/>')
        elif f > 0:
            out.append(f'<circle cx="40" cy="{y}" r="{r}" class="arc" stroke-dasharray="{circ * f:.1f} {circ:.1f}" transform="rotate(-90 40 {y})"/>'
                       f'<text x="40" y="{y + 4}" class="frac">{e(lab)}</text>')
        out.append(f'<text x="76" y="{y - 4}" class="t1 left">{e(c["name"])}</text>')
        for k, ln in enumerate(prog):
            out.append(f'<text x="76" y="{y + 13 + L * k}" class="t2 left">{e(ln)}</text>')
        for k, ln in enumerate(wait):
            out.append(f'<text x="76" y="{y + 13 + L * (len(prog) + k) + 4}" class="t2 left waitc">{e(ln)}</text>')
        out.append("</g>")
    out.append("</svg>")
    return "".join(out)


def timeline_svg(runs: list[dict], agents: list[dict], thread: list[dict], now: dt.datetime) -> str:
    """Last 24 hours: one lane per agent (runs as bars) and one for Brian (messages as dots)."""
    x0, x1, span = 88, 350, 24 * 3600
    lanes = [(a["id"], {"Brian Contact": "Contact", "Research and Code Review": "Builder"}.get(a["name"], a["name"].split(" ")[0])) for a in agents]
    H = 34 + 36 * (len(lanes) + 1) + 26
    xs = lambda d: x0 + (x1 - x0) * max(0.0, min(1.0, 1 - (now - d).total_seconds() / span))
    out = [f'<svg viewBox="0 0 360 {H}" role="img" aria-label="Agent activity, last 24 hours">']
    for h in (24, 18, 12, 6, 0):
        x = x0 + (x1 - x0) * (1 - h / 24)
        out.append(f'<line x1="{x:.1f}" y1="24" x2="{x:.1f}" y2="{H - 22}" class="grid"/><text x="{x:.1f}" y="{H - 8}" class="t2">{"now" if h == 0 else f"-{h}h"}</text>')
    for k, (aid, name) in enumerate(lanes):
        y = 34 + 36 * k
        out.append(f'<text x="{x0 - 8}" y="{y + 14}" class="t1 right">{e(name)}</text><line x1="{x0}" y1="{y + 10}" x2="{x1}" y2="{y + 10}" class="lane"/>')
        for r in runs:
            if r.get("agentId") != aid:
                continue
            st, fin = _ts(r.get("startedAt")), _ts(r.get("finishedAt")) or now
            if not st or (now - st).total_seconds() > span:
                continue
            a_, b_ = xs(st), xs(fin)
            cls = {"succeeded": "bar-ok", "failed": "bar-bad", "running": "bar-run", "queued": "bar-run"}.get(r.get("status"), "bar-other")
            out.append(f'<rect x="{a_:.1f}" y="{y + 2}" width="{max(3.0, b_ - a_):.1f}" height="16" rx="3" class="{cls}" data-tip="{e(name + ": run " + (r.get("status") or "") + ", started " + ago(r.get("startedAt")))}"><title>{e(name + ": run " + (r.get("status") or "") + ", started " + ago(r.get("startedAt")))}</title></rect>')
    y = 34 + 36 * len(lanes)
    out.append(f'<text x="{x0 - 8}" y="{y + 14}" class="t1 right">You</text><line x1="{x0}" y1="{y + 10}" x2="{x1}" y2="{y + 10}" class="lane"/>')
    for c in thread:
        d = _ts(c.get("at"))
        if d and (now - d).total_seconds() <= span:
            out.append(f'<circle cx="{xs(d):.1f}" cy="{y + 10}" r="5" class="{"msg-you" if c["who"] == "you" else "msg-agent"}" data-tip="{e(c["who"] + ", " + ago(c.get("at")) + ": " + plain(c.get("body") or "", 0))}"><title>{e(c["who"] + ", " + ago(c.get("at")))}</title></circle>')
    out.append("</svg>")
    return "".join(out)


def week_strip(conds: list[dict]) -> str:
    """Condition 4 (nothing silent for a week) as seven day cells."""
    c4 = next((c for c in conds if c.get("n") == 4), None)
    if not c4:
        return ""
    f, _ = _fraction(c4)
    n = round(7 * f)
    cells = "".join(f'<rect x="{8 + 49 * i}" y="8" width="42" height="28" rx="6" class="{"day-ok" if i < n else "day-todo"}"/>'
                    f'<text x="{29 + 49 * i}" y="27" class="t2">{"✓" if i < n else i + 1}</text>' for i in range(7))
    return (f'<h2>A clean week ({n} of 7 days)</h2><svg viewBox="0 0 360 44" role="img" aria-label="{n} of 7 clean days">{cells}</svg>')


CHECK_EXPLAIN = [  # (name prefix, what the check watches and what "fine" means), in plain words
    ("Jev gate", "Reads every command an agent is about to run and stops dangerous ones. Fine means it made a decision in the last 7 days."),
    ("CC Safety Net", "Blocks destructive git and file commands (force-push, deleting branches, mass deletes). Fine means it logged activity in the last 7 days."),
    ("Paperclip agents", "Your agents on the server. Fine means a run succeeded in the last 7 days and the latest run did not fail."),
    ("VPS backup", "The nightly backup of the server. Fine means last night's backup succeeded."),
    ("Telegram relay", "Carries messages between your Telegram and the agents. Fine means it checked in within the last 10 minutes."),
    ("Learning loop", "The weekly summary that turns agents' mistakes into rules (AES issue #74). Fine means it posted within 8 days."),
    ("Project brain", "The project's own notes on where it stands and what is next. Fine means they were updated within the last 15 commits and 14 days."),
    ("Hive settings", "The live agent settings (models, schedules) match the settings file kept in git."),
    ("Checks only Brian's PC", "Checks your PC runs daily and pushes to this page. Unknown means no report has arrived."),
]
STATUS_EXPLAIN = {"SILENT": "SILENT: it has not done anything for longer than its normal gap.",
                  "FAILING": "FAILING: its last action failed.", "STALE": "STALE: the information is older than it should be.",
                  "UNKNOWN": "UNKNOWN: this page could not read it, so it is not shown as fine."}


def explain_check(r: dict) -> str:
    what = next((t for k, t in CHECK_EXPLAIN if r["name"].startswith(k)), "")
    st = r["status"]
    state = "Now: fine." if st == "ok" else "Now: " + next((v for k, v in STATUS_EXPLAIN.items() if st.startswith(k)), st) + f" ({st})"
    return f'{r["name"]}. {what} {state} Last activity: {r["last"]}.'


def health_tiles(rows: list[dict]) -> str:
    tiles = []
    for r in sorted(rows, key=lambda r: r["status"] == "ok"):
        ok = r["status"] == "ok"
        tip = explain_check(r)
        tiles.append(f'<div class="tile {"ok" if ok else "warn"}" tabindex="0" data-tip="{e(tip)}" title="{e(tip)}"><span class="glyph">{"✓" if ok else "!"}</span>'
                     f'<b>{e(r["name"])}</b><span class="m">{e("fine" if ok else r["status"])} · {e(r["last"])}</span></div>')
    return '<div class="tiles">' + "".join(tiles) + "</div>"

GH = "https://github.com/BrianMills2718"
# Paperclip's own pages are the detail view for agents and projects (landscape review 2026-10-04: its agent page
# already has overview, instructions, skills, tools, configuration, runs, budget and audit; its project page has
# configuration, issues and workspaces). This page only links into them.
PC = "https://paperclip.brianmills.dev/BRI"
BRAIN_STATE_EXPLAIN = {"fresh": "Its notes are up to date with the project's recent work.",
                       "stale": "Its notes are behind: the project changed since they were last updated.",
                       "none": "This project has no brain yet: no .project-brain/ folder in the repository.",
                       "unknown": "This page could not tell whether its notes are current (no recent report from your PC)."}


def node_details(agents, busy: set[str], brains: dict[str, str], brain_text: dict[str, dict], failing: set[str]) -> dict[str, str]:
    """What each map box opens: plain words on what it is, its state now, and links to its subject."""
    d = {"you": "<h3>You</h3><ul><li>The one who decides.</li><li>Decisions come to you one at a time, in the terminal and on your Telegram thread "
                f"({BRIAN_THREAD}).</li><li>Answer them on the <a href='#decide' data-go='decide'>Decisions</a> screen, or send a message from "
                "<a href='#live' data-go='live'>Live</a>.</li></ul>",
         "hub": "<h3>Terminal relay</h3><ul><li>The route between you and the agents.</li><li>Agents post to your Telegram thread "
                f"({BRIAN_THREAD}); the relay sends it to your phone and brings your replies back.</li><li>Its health is the Telegram relay check on "
                "<a href='#health' data-go='health'>Health</a>.</li></ul>"}
    for a in agents:
        st = "failing: its latest run failed" if a["name"] in failing else ("working now" if a["name"] in busy else "idle, waiting for its next task")
        d["agent:" + a["name"]] = (f"<h3>{e(a['name'])}</h3><ul><li>Job: {e(AGENT_JOB.get(a['name'], 'an agent'))}.</li><li>Now: {e(st)}.</li>"
                                   "<li>Its runs are the bars on <a href='#live' data-go='live'>Live</a>.</li></ul>"
                                   f"<a class='btn' href='{PC}/agents/{e(a.get('urlKey') or a['id'])}'>Open {e(a['name'])} in Paperclip</a>"
                                   "<p class='m'>Its page there shows its instructions, skills, tools, configuration, every run with its transcript, "
                                   "budget, and the history of every change to its setup.</p>")
    for r in PROJECT_REPOS:
        state = brains.get(r, "unknown")
        bt = brain_text.get(r) or {}
        head = (f"<h3>{e(SHORT[r])} brain</h3><p class='m'>Project <code>{e(r)}</code> · {e(BRAIN_LABEL[state])}. {e(BRAIN_STATE_EXPLAIN[state])}</p>"
                f"<a class='btn' href='{PC}/projects/{e(r.replace('_', '-'))}'>Open {e(SHORT[r])} in Paperclip</a>"
                "<p class='m'>Its project page there shows its configuration, the agents' tasks on it and their history.</p>")
        if bt.get("now"):
            files = bt.get("files") or ["now.md"]
            links = "".join(f"<li><a href='{GH}/{e(r)}/blob/main/.project-brain/{e(f)}'>{e(f)}</a></li>" for f in files)
            d["brain:" + r] = (head + "<p class='m'>What its <code>now.md</code> says (where it stands and what is next):</p>"
                               f"<div class='mdsrc' hidden>{e(bt['now'])}</div><div class='mdout'></div>"
                               f"<p class='m'>All of its brain files on GitHub:</p><ul>{links}</ul>")
        else:
            why = bt.get("error") or ("no report from your PC yet" if state == "unknown" else "")
            d["brain:" + r] = head + (f"<p class='m'>{e(why)}</p>" if why else "") + f"<ul><li><a href='{GH}/{e(r)}'>Open the repository</a></li></ul>"
    d["tool:Safety rules"] = ("<h3>Safety rules</h3><ul><li>Jev gate reads every command an agent is about to run and stops dangerous ones.</li>"
                              "<li>CC Safety Net blocks destructive git and file commands.</li><li>Both are checks on <a href='#health' data-go='health'>Health</a>.</li></ul>")
    d["tool:Learning loop"] = ("<h3>Learning loop</h3><ul><li>Agents' mistakes are filed as GitHub issues and labelled.</li>"
                               "<li>Once a week a summary turns repeated mistakes into rules.</li>"
                               "<li><a href='https://github.com/BrianMills2718/agentic-engineering-system-canonical/issues/74'>Open the weekly summaries (AES #74)</a></li></ul>")
    d["tool:Server"] = ("<h3>Server</h3><ul><li>personal-vps: the agents, the board and this page run here.</li><li>Backed up nightly.</li>"
                        "<li>Its checks are on <a href='#health' data-go='health'>Health</a>.</li></ul>")
    return d


def map_svg(agents, busy: set[str], brains: dict[str, str]) -> str:
    """You at the top, the communication route, project brains around it, agents and tools below."""
    W = 360
    out = [f'<svg viewBox="0 0 {W} 520" role="img" aria-label="Map of the hive brain">']
    def node(x, y, label, sub, kind, key):
        cls = {"you": "n-you", "hub": "n-hub", "on": "n-on", "off": "n-off", "tool": "n-tool"}[kind]
        out.append(f'<g class="node {cls}" tabindex="0" role="button" data-key="{e(key)}"><title>{e(label)}: {e(sub)}. Tap for more.</title>'
                   f'<rect x="{x-54}" y="{y-20}" width="108" height="40" rx="12"/>'
                   f'<text x="{x}" y="{y-3}" class="t1">{e(label)}</text><text x="{x}" y="{y+12}" class="t2">{e(sub.split(" · ")[0])}</text></g>')
    def line(x1, y1, x2, y2, on=False):
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{"edge-on" if on else "edge"}"/>')
    you, hub = (180, 36), (180, 116)
    agent_pos = [(60, 206), (180, 206), (300, 206)]
    proj_pos = [(60, 306), (180, 306), (300, 306), (120, 366), (240, 366)]
    tool_pos = [(60, 466), (180, 466), (300, 466)]
    line(*you, *hub, True)
    for k, (x, y) in enumerate(agent_pos):
        line(*hub, x, y, k < len(agents) and agents[k]["name"] in busy)
    for x, y in proj_pos:
        line(180, 206, x, y)
    for x, y in tool_pos:
        line(x, y - 20, x, 386)
    node(*you, "You", "the one who decides", "you", "you")
    node(*hub, "Terminal relay", "communication route · decisions come to you here, one at a time", "hub", "hub")
    for (x, y), a in zip(agent_pos, agents):
        node(x, y, {"Brian Contact": "Contact"}.get(a["name"], a["name"].split(" ")[0]), f"{AGENT_JOB.get(a['name'], '')} · {'working now' if a['name'] in busy else 'idle'}",
             "on" if a["name"] in busy else "off", "agent:" + a["name"])
    for (x, y), r in zip(proj_pos, PROJECT_REPOS):
        state = brains.get(r, "unknown")
        node(x, y, SHORT[r], f"{BRAIN_LABEL[state]} · project {r}", "on" if state == "fresh" else "off", "brain:" + r)
    for (x, y), (t, sub) in zip(tool_pos, [("Safety rules", "checks commands · Jev gate and CC Safety Net"),
                                         ("Learning loop", "issues to rules · GitHub issues, labelled weekly"),
                                         ("Server", "personal-vps · agents run here, backed up nightly")]):
        node(x, y, t, sub, "tool", "tool:" + t)
    out.append('<text x="180" y="262" class="t2">projects (each with its own brain)</text>')
    out.append('<text x="180" y="426" class="t2">what keeps it safe and running</text>')
    out.append("</svg>")
    return "".join(out)


def run_controls_here() -> tuple[dict | None, str]:
    """Run controls.py on this machine (snapshot mode); return its JSON report."""
    tmp = Path(os.environ.get("TMPDIR", "/tmp")) / f"hive-controls-{os.getpid()}.json"
    try:
        r = subprocess.run([sys.executable, str(HERE / "controls.py"), "--json-out", str(tmp)],
                           capture_output=True, text=True, timeout=400)
        return json.loads(tmp.read_text()), f"controls exit {r.returncode}"
    except (OSError, ValueError, subprocess.TimeoutExpired) as err:
        return None, f"controls.py failed: {err}"
    finally:
        tmp.unlink(missing_ok=True)


def vps_rows(runs: list[dict]) -> list[dict]:
    """Checks the VPS can measure itself: Paperclip agent runs and the nightly backup."""
    now = dt.datetime.now(dt.timezone.utc)
    rows = []
    rs = sorted(runs, key=lambda x: x.get("startedAt") or "", reverse=True)
    good = next((x for x in rs if x.get("status") == "succeeded"), None)
    good_at = parse_ts(good.get("startedAt")) if good else None
    if rs and rs[0].get("status") == "failed":
        st = f"FAILING: latest run failed ({rs[0].get('errorCode')})"
    else:
        st = "SILENT" if good_at is None or now - good_at > 7 * dt.timedelta(days=1) else "ok"
    rows.append({"name": "Paperclip agents (last good run)", "last": ago(good.get("startedAt")) if good else "never", "status": st, "side": "vps",
                 "at": good.get("startedAt") if good else None})
    r = subprocess.run(["systemctl", "show", "vps-backup.service", "-p", "Result", "-p", "ExecMainExitTimestamp", "--value", "--timestamp=unix"],
                       capture_output=True, text=True)
    lines = r.stdout.split("\n")
    if r.returncode != 0 or len(lines) < 2:
        rows.append({"name": "VPS backup (nightly)", "last": "?", "status": f"UNKNOWN: systemctl failed ({r.stderr.strip()[:80]})", "side": "vps"})
    else:
        result, when = lines[0].strip(), lines[1].strip().lstrip("@")
        when_d = dt.datetime.fromtimestamp(int(when), dt.timezone.utc) if when else None
        st = (f"FAILING: result {result}" if result != "success" else
              ("SILENT" if when_d is None or now - when_d > 2 * dt.timedelta(days=1) else "ok"))
        rows.append({"name": "VPS backup (nightly)", "last": ago(when_d.isoformat()) if when_d else "never", "status": st, "side": "vps",
                     "at": when_d.isoformat() if when_d else None})
    return rows


def thread_feed(issues: list[dict], names: dict[str, str]) -> tuple[list[dict], str, str]:
    """Newest exchanges on Brian's Telegram-bound thread."""
    t = next((i for i in issues if i.get("identifier") == BRIAN_THREAD), None)
    if t is None:
        return [], f"{BRIAN_THREAD} is not in the issues list", ""
    try:
        cs = board(f"/api/issues/{t['id']}/comments")
    except (RuntimeError, ValueError, subprocess.TimeoutExpired) as err:
        return [], f"could not read {BRIAN_THREAD}: {err}", t["id"]
    cs = sorted((c for c in cs if not c.get("deletedAt")), key=lambda c: c.get("createdAt") or "", reverse=True)[:6]
    return [{"who": "you" if c.get("authorUserId") == BRIAN else names.get(c.get("authorAgentId"), "an agent"),
             "at": c.get("createdAt"), "body": c.get("body") or ""} for c in cs], "", t["id"]


def plain(s: str, n: int) -> str:
    """One line of readable text from Markdown: drop link targets, emphasis and heading marks."""
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"(\*\*|__|`)", "", s)
    s = re.sub(r"(^|\n)\s*#{1,6}\s*", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s  # n is kept for callers; text is never shortened (Brian, 2026-10-04: "i should never see truncation")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--vps", action="store_true", help="hosted mode, run on the VPS (see above)")
    ap.add_argument("--wsl-controls", type=Path, help="with --vps: the controls report Brian's PC pushed up")
    ap.add_argument("--json-out", type=Path, help="also write the status JSON the page's 30 s poll reads")
    a = ap.parse_args()
    if a.vps:
        os.environ["HIVE_BOARD_LOCAL"] = "1"
        if not a.wsl_controls:
            ap.error("--vps needs --wsl-controls")
    built = dt.datetime.now(dt.timezone.utc)
    try:
        issues = board(f"/api/companies/{C}/issues")
        runs = board(f"/api/companies/{C}/heartbeat-runs?limit=100")
        agents = board(f"/api/companies/{C}/agents")
    except (RuntimeError, ValueError, subprocess.TimeoutExpired) as err:
        print(f"dashboard: could not read the Paperclip board: {err}", file=sys.stderr)
        return 2
    cond = json.loads((HERE / "conditions.json").read_text())
    names = {x["id"]: x["name"] for x in agents}

    # Data sources, each with its age; a source is "ok", "STALE" or "UNKNOWN", never silently fine.
    sources = [{"name": "Paperclip board (tasks, agents, runs)", "at": built.isoformat(timespec="seconds"), "state": "ok",
                "note": "read for this build"}]
    if a.vps:
        report, why = None, ""
        try:
            report = json.loads(a.wsl_controls.read_text())
            parse_ts(report["at"])
        except FileNotFoundError:
            why = "no report from Brian's PC has arrived yet"
        except (OSError, ValueError, KeyError, TypeError) as err:
            report, why = None, f"report unreadable: {err}"
        at = parse_ts(report["at"]) if report else None
        fresh = at is not None and built - at <= WSL_REPORT_MAX
        sources.append({"name": "Checks only Brian's PC can see (pushed daily)", "at": report["at"] if report else None,
                        "state": "ok" if fresh else ("STALE" if report else "UNKNOWN"),
                        "note": why or (f"from {report.get('host', '?')}; stale after {WSL_REPORT_MAX.total_seconds() / 3600:.0f} h")})
        # "last" inside the report is relative to when Brian's PC measured it; say so.
        wsl = [{**r, "last": f"{r['last']} (PC report, {ago(report['at'])})"}
               for r in (report or {}).get("rows", []) if r.get("side") == "wsl"]
        if report and not fresh:
            wsl = [{**r, "status": f"STALE: report {ago(report['at'])} (it said: {'fine' if r['status'] == 'ok' else r['status']})"} for r in wsl]
        if not report:
            wsl = [{"name": "Checks only Brian's PC can see", "last": "?", "status": f"UNKNOWN: {why}", "side": "wsl"}]
        ctl_rows = wsl + vps_rows(runs)
        sources.append({"name": "Server checks (agents, backup)", "at": built.isoformat(timespec="seconds"), "state": "ok",
                        "note": "measured on the VPS for this build"})
        brains = {r: brain_from_rows(r, wsl, fresh) for r in PROJECT_REPOS}
        brain_text = (report or {}).get("brains") or {}
        ctl_note = f"wsl report {'fresh' if fresh else ('stale' if report else 'missing')}"
    else:
        report, ctl_note = run_controls_here()
        ctl_rows = report["rows"] if report else [{"name": "Controls checks", "last": "?", "status": f"UNKNOWN: {ctl_note}", "side": "wsl"}]
        sources.append({"name": "Controls checks (this machine)", "at": report["at"] if report else None,
                        "state": "ok" if report else "UNKNOWN", "note": ctl_note})
        brains = {r: brain_local(r) for r in PROJECT_REPOS}
        brain_text = {}
        for r in PROJECT_REPOS:
            bd = Path.home() / "code" / r / ".project-brain"
            if (bd / "now.md").exists():
                brain_text[r] = {"now": (bd / "now.md").read_text(), "files": sorted(f.name for f in bd.glob("*.md"))}
    cond_at = parse_ts(cond.get("updated"))
    sources.append({"name": "Path to v1 (conditions.json, updated by hand)", "at": cond.get("updated"),
                    "state": "ok" if cond_at and built - cond_at <= 7 * dt.timedelta(days=1) else "STALE",
                    "note": "stale after 7 days without an update"})

    latest = {}
    for r in sorted(runs, key=lambda r: r.get("startedAt") or ""):
        latest[r.get("agentId")] = r
    busy = {names[k] for k, r in latest.items() if k in names and r.get("status") in ("running", "queued")}
    broken = [names[k] for k, r in latest.items() if k in names and r.get("status") == "failed"]
    open_t = [i for i in issues if i.get("status") not in ("done", "cancelled")]
    waiting = sorted((i for i in open_t if i.get("assigneeUserId") == BRIAN), key=lambda i: i.get("createdAt") or "")
    held = cond.get("decisions_in_terminal", [])
    held_open = [d for d in held if not d.get("answered")]
    done_t = sorted((i for i in issues if i.get("status") == "done"), key=lambda i: i.get("updatedAt") or "", reverse=True)[:5]
    quiet = [r for r in ctl_rows if r["status"] != "ok"]
    bad_sources = [s for s in sources if s["state"] != "ok"]
    n_need = len(waiting) + len(held_open)
    thread, thread_err, thread_id = thread_feed(issues, names)
    interactive = a.vps

    p = ['<title>Hive brain</title>', STYLE, '<div class="app">']
    p.append(f'<header class="top"><b>Hive brain</b><span id="age" data-built="{built.isoformat(timespec="seconds")}">'
             f'built {built:%a %H:%M} UTC</span></header><div id="banner" class="banner" role="status" hidden></div>')

    # Map
    p.append('<section class="screen" id="map"><h1>The big picture</h1><p class="sub">How everything fits together. Tap any box to open it.</p>')
    p.append(map_svg(agents, busy, brains))
    p.append('<p class="legend"><span class="sw bar-run"></span>blue: active, or notes up to date <span class="sw off"></span>grey dashed: idle, not set up yet, or not known</p>')
    details = node_details(agents, busy, brains, brain_text, set(broken))
    p.append('<div class="info" id="info" aria-live="polite"><p class="m">Nothing open yet. Tap a box above.</p></div>'
             + "".join(f'<template data-key="{e(k)}">{v}</template>' for k, v in details.items()) + '</section>')

    def message_box(where: str) -> str:
        if not interactive:
            return '<p class="sub">Open hive.brianmills.dev to message your agents from here.</p>'
        return (f'<form class="message" data-where="{where}"><label for="msg-{where}"><b>Message your agents</b></label>'
                f'<p class="sub">Goes to your Telegram thread ({BRIAN_THREAD}); the Coordinator wakes and replies there and on your phone.</p>'
                f'<textarea id="msg-{where}" name="text" rows="3" maxlength="2000" placeholder="e.g. Pause pilot work until Monday"></textarea>'
                '<button type="submit" class="pick">Send</button><p class="result" aria-live="polite"></p></form>')
    # Live
    p.append('<section class="screen" id="live" hidden><h1>What\'s happening right now</h1><p class="sub">The last 24 hours: each bar is an agent at work, each dot a message.</p>')
    p.append(timeline_svg(runs, agents, thread, built))
    p.append('<p class="legend"><span class="sw bar-ok"></span>finished <span class="sw bar-bad"></span>failed <span class="sw bar-run"></span>working now '
             '<span class="sw msg-you round"></span>you <span class="sw msg-agent round"></span>agent message</p>')
    p.append(f'<h2>Your Telegram thread ({BRIAN_THREAD})</h2><ol class="feed">')
    for k, c in enumerate(thread):
        if k == 3:
            p.append('</ol><details class="more"><summary>Older messages</summary><ol class="feed">')
        p.append(f'<li class="{"done" if c["who"] == "you" else "now"}"><span class="dot"></span><div><b>{e(c["who"])}</b>'
                 f'<span class="m">{e(ago(c["at"]))}</span><p class="msg">{e(plain(c["body"], 160))}</p></div></li>')
    if thread_err:
        p.append(f'<li class="warn"><span class="dot"></span><div><b>Could not show the thread</b><span class="m">{e(thread_err)}</span></div></li>')
    p.append(('</ol></details>' if len(thread) > 3 else '</ol>') + message_box("live")
             + f'<details class="more"><summary>Tasks in motion ({len(open_t)}) and just finished ({len(done_t)})</summary><h2>Tasks in motion</h2><ol class="feed">')
    for i in sorted(open_t, key=lambda i: i.get("updatedAt") or "", reverse=True):
        who = "you" if i.get("assigneeUserId") == BRIAN else names.get(i.get("assigneeAgentId"), "nobody")
        p.append(f'<li class="now"><span class="dot"></span><div><b>{e(i["title"])}</b><span class="m">with {e(who)} · {e(i["status"].replace("_", " "))} · {e(ago(i.get("updatedAt")))}</span></div></li>')
    p.append('</ol><h2>Just finished</h2><ol class="feed">')
    for i in done_t:
        p.append(f'<li class="done"><span class="dot"></span><div><b>{e(i["title"])}</b><span class="m">done · {e(ago(i.get("updatedAt")))}</span></div></li>')
    p.append('</ol></details></section>')

    # Path
    p.append('<section class="screen" id="path" hidden><h1>Path to v1</h1><p class="sub">Five stations; each fills as it gets done.</p>')
    p.append(path_svg(cond["conditions"]))
    p.append('<details class="more"><summary>What each one means, and the evidence</summary><ol class="path">')
    for c in cond["conditions"]:
        st = {"done": "done", "partway": "underway", "not_started": "todo"}[c["status"]]
        p.append(f'<li class="{st}"><span class="dot"></span><details><summary><b>{e(c["name"])}</b><span class="m">{e(c["progress"])}</span></summary>'
                 f'<p>{e(c["plain"])}</p><p><b>So far:</b> {md(c["evidence"])}</p><p class="wait"><b>Waiting on:</b> {md(c["next"])}</p></details></li>')
    p.append(f'</ol></details><p class="sub">Updated {e(cond["updated"])} with evidence.</p></section>')

    # Decisions
    p.append(f'<section class="screen" id="decide" hidden><h1>{"Nothing needs you" if not n_need else ("You have a decision" if n_need == 1 else f"You have {n_need} decisions")}</h1>')
    p.append('<p class="sub">' + ("Add a note if you like, then tap an answer. It goes to the task as a comment and wakes the agent." if interactive
             else "Answer in the terminal or on the board. (Answer buttons work on the hosted page.)") + '</p>')
    for i in waiting:
        desc = i.get("description") or ""
        p.append(f'<article class="decision" data-issue="{e(i["id"])}"><b>{e(i["title"])}</b><span class="m">{e(i["identifier"])} · asked {e(ago(i.get("createdAt")))}'
                 f' by {e(names.get(i.get("createdByAgentId"), "someone"))}</span><div class="full">{e(desc)}</div>')
        if interactive:
            p.append(f'<form class="answer"><label>Note (optional)<textarea name="note" rows="2" maxlength="2000"></textarea></label><div class="opts">'
                     + "".join(f'<button type="button" class="pick" value="{e(o)}">{e(o)}</button>' for o in ANSWER_OPTIONS)
                     + '</div><p class="result" role="status"></p></form>')
        p.append(f'<a class="link" href="https://paperclip.brianmills.dev/BRI/issues/{e(i["identifier"])}">Open {e(i["identifier"])} on the board</a></article>')
    for d in held:
        p.append(f'<article class="decision held{" answered" if d.get("answered") else ""}"><b>{e(d["question"])}</b>'
                 f'<span class="m">held in the terminal session · for information only</span><p>{md(d["context"])}</p>')
        if d.get("answered"):
            p.append(f'<p class="rec"><b>Answered:</b> {md(d["answered"])}</p></article>')
        else:
            p.append(f'<p class="rec"><b>Recommended:</b> {md(d["recommendation"])}</p><div class="opts">'
                     + "".join(f'<span class="opt">{e(o)}</span>' for o in d["options"]) + '</div><p class="m">Reply in the terminal session.</p></article>')
    if not n_need:
        p.append('<p class="calm">The agents are working on their own. You will see a decision here when one needs you.</p>')
    p.append(message_box("decide") + '</section>')

    # Health
    all_ok = not quiet and not broken and not bad_sources
    p.append(f'<section class="screen" id="health" hidden><h1>System health</h1><p class="sub">Each check asks whether one part did its job recently.</p>'
             f'<div class="overall {"ok" if all_ok else "warn"}"><b>{"Everything is running" if all_ok else "Something needs a look"}</b>'
             f'<span>{len(ctl_rows) - len(quiet)} of {len(ctl_rows)} checks fine{"; agent failing: " + ", ".join(broken) if broken else ""}'
             f'{"; data not current: " + ", ".join(s["name"] for s in bad_sources) if bad_sources else ""}</span></div>')
    p.append(health_tiles(ctl_rows) + week_strip(cond["conditions"]))
    p.append('<details class="more"><summary>Where this page\'s data comes from</summary><ul class="checks">')
    for s in sources:
        ok = s["state"] == "ok"
        p.append(f'<li class="{"ok" if ok else "warn"}"><span>{e(s["name"])}</span><span class="m">{e("current" if ok else s["state"])} · '
                 f'{e(ago(s["at"]) if s["at"] else "never")} · {e(s["note"])}</span></li>')
    p.append('</ul></details></section>')

    p.append(f'<nav class="tabs">' + "".join(
        f'<button data-s="{s}" title="{e(TAB_TIP[s])}"{" aria-current=\"page\"" if s == "map" else ""}>{l}{" <i>" + str(n_need) + "</i>" if s == "decide" and n_need else ""}</button>'
        for s, l in [("map", "Map"), ("live", "Live"), ("path", "Path"), ("decide", "Decisions"), ("health", "Health")]) + "</nav></div>")
    import hashlib
    digest = hashlib.sha256(json.dumps([
        [(c.get("at"), c.get("body")) for c in thread], [(i.get("id"), i.get("status"), i.get("updatedAt")) for i in issues],
        [(r.get("id"), r.get("status")) for r in runs], [(r["name"], r["status"]) for r in ctl_rows], cond, brains,
        {k: v.get("now") for k, v in brain_text.items()}], sort_keys=True, default=str).encode()).hexdigest()[:16]
    status = {"built": built.isoformat(timespec="seconds"), "digest": digest, "build_max_min": BUILD_MAX_MIN, "sources": sources,
              "decisions": [{"id": i["id"], "identifier": i["identifier"], "title": i["title"]} for i in waiting],
              "answer_options": ANSWER_OPTIONS, "hosted": interactive, "thread_id": thread_id, "need": n_need, "checks_not_ok": len(quiet)}
    p.append(f'<script id="page-status" type="application/json">{json.dumps(status).replace("<", "\\u003c")}</script>')
    p.append(SCRIPT)
    write_atomic(a.out, "\n".join(p))
    if a.json_out:
        write_atomic(a.json_out, json.dumps(status, indent=1) + "\n")
        write_atomic(a.json_out.with_name("status-full.json"), json.dumps(
            full_status(built, n_need, ctl_rows, cond, brains, brain_text, waiting, held_open, runs, names), indent=1) + "\n")
    print(f"dashboard: wrote {a.out} ({a.out.stat().st_size} bytes){' and ' + str(a.json_out) if a.json_out else ''}; "
          f"busy {sorted(busy)}, broken {broken}, decisions {n_need}, checks {len(ctl_rows)} ({len(quiet)} not ok), "
          f"sources not current {len(bad_sources)}, thread messages {len(thread)}{' (' + thread_err + ')' if thread_err else ''}, {ctl_note}")
    return 0


def md_html(text: str) -> str:
    """Markdown to HTML with raw HTML escaped (markdown-it, CommonMark, html=False); escaped text if it is missing."""
    try:
        from markdown_it import MarkdownIt
    except ImportError:
        return f"<pre>{e(text)}</pre>"
    return MarkdownIt("commonmark", {"html": False, "linkify": False}).enable("table").render(text)


def full_status(built, n_need, ctl_rows, cond, brains, brain_text, waiting, held_open, runs, names) -> dict:
    """Everything the page shows, as plain data, for the Glance page (personal-vps apps/glance) to read."""
    def state(st: str) -> str:
        return "ok" if st == "ok" else next((v for k, v in (("STALE", "stale"), ("FAILING", "failing"), ("SILENT", "silent"))
                                             if st.startswith(k)), "unknown")
    week = built - 7 * dt.timedelta(days=1)
    recent = [r for r in runs if (parse_ts(r.get("startedAt")) or built) >= week]
    oldest = min((parse_ts(r.get("startedAt")) for r in runs if r.get("startedAt")), default=None)
    by = {}
    for r in recent:
        u = r.get("usageJson") or {}
        a = by.setdefault(names.get(r.get("agentId"), "unknown agent"), {"usd": 0.0, "runs": 0, "failed": 0})
        a["usd"] += float(u.get("costUsd") or 0)
        a["runs"] += 1
        a["failed"] += r.get("status") == "failed"
    return {
        "built": built.isoformat(timespec="seconds"), "need": n_need,
        "checks": [{"name": r["name"], "state": state(r["status"]), "last": r.get("at"),
                    "note": ("fine" if r["status"] == "ok" else r["status"]) + f"; last activity {r['last']}. " + explain_check(r),
                    "where": "vps" if r.get("side") == "vps" else "pc"} for r in ctl_rows],
        "conditions": [{k: c.get(k) for k in ("n", "name", "plain", "status", "progress", "next")} for c in cond["conditions"]],
        "brains": [{"repo": r, "state": brains.get(r, "unknown"),
                    "now_html": md_html((brain_text.get(r) or {}).get("now") or "") if (brain_text.get(r) or {}).get("now") else None,
                    "paperclip_url": f"{PC}/projects/{r.replace('_', '-')}"} for r in PROJECT_REPOS],
        "costs": {"days": 7, "total_usd": round(sum(a["usd"] for a in by.values()), 2),
                  "by_agent": [{"name": n, "usd": round(a["usd"], 2), "runs": a["runs"], "failed": a["failed"]} for n, a in sorted(by.items())],
                  "note": "API-price cost of the board's latest 100 runs inside the last 7 days"
                          + (f"; those runs only reach back to {oldest.isoformat(timespec='minutes')}" if oldest and oldest > week else "")
                          + ". Runs on a subscription are counted at API prices too."} if runs else None,
        "decisions": [{"title": i["title"], "url": f"{PC}/issues/{i['identifier']}"} for i in waiting]
                     + [{"title": d["question"], "url": None} for d in held_open],
        "links": {"paperclip": f"{PC}/dashboard", "costs": f"{PC}/costs", "inbox": f"{PC}/inbox", "decisions": f"{PC}/decisions",
                  "agents": f"{PC}/agents", "old_dashboard": "https://hive.brianmills.dev"},
    }


def write_atomic(path: Path, text: str) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text)
    tmp.chmod(0o644)
    tmp.replace(path)


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
.top span.stale{color:var(--warn);font-weight:600}.banner{background:var(--warn-bg);color:var(--warn);border:1px dashed var(--warn);border-radius:10px;padding:9px 12px;font-size:.88rem}
.banner button{margin-left:6px;background:var(--warn);color:var(--bg);border:0;border-radius:8px;padding:4px 10px;font-weight:600}
.feed li.warn>div{border:1px dashed var(--warn);background:var(--warn-bg)}.msg{margin:4px 0 0;font-size:.88rem;overflow-wrap:anywhere}
.decision>.m{margin-top:2px}.decision.answered{border-color:var(--line)}.full{white-space:pre-wrap;font-size:.85rem;margin-top:6px;overflow-wrap:anywhere}
.answer{margin-top:10px}.answer label{display:grid;gap:4px;font-size:.84rem;color:var(--mute)}
.message{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin-top:12px;display:grid;gap:8px}
.answer textarea,.message textarea{font:inherit;color:var(--fg);background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:6px 8px;width:100%;box-sizing:border-box}
.pick{font:600 .88rem var(--body);border:1px solid var(--on);color:var(--on);background:var(--card);border-radius:10px;padding:9px 12px;min-height:44px;cursor:pointer}
.pick:disabled{opacity:.55;cursor:wait}.pick.chosen{background:var(--on);color:var(--bg)}
.result{margin:8px 0 0;font-size:.88rem}.result.ok{color:var(--on);font-weight:600}.result.err{color:var(--warn);font-weight:600}
.link{display:inline-block;margin-top:10px;color:var(--on);font-size:.88rem}
.tabs{position:fixed;left:0;right:0;bottom:0;background:var(--card);border-top:1px solid var(--line);display:flex;justify-content:space-around;padding:8px 6px calc(8px + env(safe-area-inset-bottom,0px))}
.tabs button{background:none;border:0;color:var(--mute);font:600 .78rem var(--body);padding:6px 4px;cursor:pointer}.tabs button[aria-current]{color:var(--on)}
.tabs i{font-style:normal;background:var(--warn);color:var(--bg);border-radius:99px;padding:0 6px;margin-left:3px}
.tabs button:focus-visible,summary:focus-visible{outline:2px solid var(--on);outline-offset:2px}
/* Pictures (picture-before-prose): path stations, 24 h timeline, health tiles, week strip */
.t1.left,.t2.left{text-anchor:start}.t1.right{text-anchor:end}
.station .ring{fill:var(--card);stroke:var(--line);stroke-width:4}.station .fill{fill:var(--on)}
.station .tick{fill:none;stroke:var(--bg);stroke-width:4;stroke-linecap:round;stroke-linejoin:round}
.station .arc{fill:none;stroke:var(--on);stroke-width:5;stroke-linecap:round}.st-todo .ring{stroke-dasharray:5 4}
.frac{font:700 10px var(--body);fill:var(--on);text-anchor:middle}.waitc{fill:var(--warn)}
.grid{stroke:var(--line);stroke-width:1}.lane{stroke:var(--line);stroke-width:1;stroke-dasharray:2 3}
.bar-ok{fill:var(--on)}.bar-run{fill:var(--on-bg);stroke:var(--on);stroke-width:1.5}.bar-bad{fill:var(--warn-bg);stroke:var(--warn);stroke-width:1.5;stroke-dasharray:3 2}.bar-other{fill:var(--off)}
.msg-you{fill:var(--fg)}.msg-agent{fill:var(--card);stroke:var(--on);stroke-width:2}
.legend{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:center;color:var(--mute);font-size:.8rem}
.sw{display:inline-block;width:16px;height:10px;border-radius:3px;margin-right:4px;vertical-align:middle}.sw.round{width:10px;border-radius:99px}
.sw.bar-ok{background:var(--on)}.sw.bar-bad{background:var(--warn-bg);border:1.5px dashed var(--warn)}.sw.bar-run{background:var(--on-bg);border:1.5px solid var(--on)}
.sw.msg-you{background:var(--fg)}.sw.msg-agent{background:var(--card);border:2px solid var(--on)}
.tiles{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:12px}
.tile{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px;display:grid;gap:2px;min-width:0}
.tile b{font-size:.84rem;overflow-wrap:anywhere}.tile.warn{border:1.5px dashed var(--warn);background:var(--warn-bg)}
.glyph{width:30px;height:30px;border-radius:99px;display:grid;place-items:center;font-weight:700;background:var(--on);color:var(--bg)}.tile.warn .glyph{background:var(--warn)}
.day-ok{fill:var(--on)}.day-ok+text{fill:var(--bg);font-weight:700}.day-todo{fill:var(--card);stroke:var(--line);stroke-dasharray:4 3}
details.more{margin-top:14px}
.sw.off{background:var(--off-bg);border:1.5px dashed var(--off)}
.info h3{margin:2px 0 6px;font-size:1rem}.info ul{margin:4px 0;padding-left:1.2em}.info li{margin:2px 0}.info a{color:var(--on)}
.mdout{background:var(--bg);border-radius:8px;padding:6px 10px;font-size:.88rem;overflow-wrap:anywhere}.mdout h1,.mdout h2{font:600 .95rem var(--body);text-transform:none;letter-spacing:0;color:var(--fg);margin:8px 0 4px}
.mdout pre{white-space:pre-wrap}.mdsrc-raw{white-space:pre-wrap;font-size:.85rem}
[data-tip]{cursor:help}.tipsheet{position:fixed;left:12px;right:12px;bottom:76px;z-index:9;background:var(--card);border:1.5px solid var(--on);border-radius:12px;
padding:12px 40px 12px 14px;font-size:.9rem;box-shadow:0 6px 24px rgba(0,0,0,.18)}.tipsheet button{position:absolute;top:6px;right:6px;border:0;background:none;color:var(--mute);font-size:1.2rem;cursor:pointer;min-width:32px;min-height:32px}
/* Laptop: the bottom tabs become a left side menu; one screen at a time, with room to read. */
@media (min-width:64rem){
.app{max-width:64rem;padding-left:15rem;padding-block:8px 24px}
.tabs{top:0;bottom:0;left:0;right:auto;width:13rem;flex-direction:column;justify-content:flex-start;gap:4px;padding:64px 12px;border-top:0;border-right:1px solid var(--line)}
.tabs button{text-align:left;font-size:.95rem;padding:10px 12px;border-radius:8px}.tabs button[aria-current]{background:var(--on-bg)}
#map svg{max-width:34rem}#map:not([hidden]){display:grid;grid-template-columns:minmax(0,34rem) minmax(0,1fr);gap:0 24px;align-items:start}#map>h1,#map>.sub{grid-column:1/-1}
#map>svg{grid-column:1;grid-row:3/6}#map>.legend,#map>.info{grid-column:2}
#health .tiles{grid-template-columns:repeat(3,minmax(0,1fr))}.tipsheet{left:auto;right:24px;bottom:24px;max-width:28rem}}details.more>summary{cursor:pointer;color:var(--on);font-weight:600;font-size:.88rem}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=IBM+Plex+Sans:wght@400;600&display=swap">
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.2/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/dompurify/3.1.6/purify.min.js"></script>"""

SCRIPT = """<script>
const tabs=[...document.querySelectorAll('.tabs button')];
function show(s){document.querySelectorAll('.screen').forEach(x=>x.hidden=x.id!==s);tabs.forEach(b=>b.toggleAttribute('aria-current',b.dataset.s===s));try{localStorage.setItem('hive-tab',s)}catch(e){}}
tabs.forEach(b=>b.addEventListener('click',()=>show(b.dataset.s)));
const h=location.hash.slice(1);let saved=null;try{saved=localStorage.getItem('hive-tab')}catch(e){}
if(h&&document.getElementById(h))show(h);else if(saved&&document.getElementById(saved))show(saved);
const info=document.getElementById('info');
const wide=()=>matchMedia('(min-width:64rem)').matches;
function go(s){show(s)}
function wireGo(root){root.querySelectorAll('a[data-go]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();go(a.dataset.go)}))}
// Brain notes are Markdown: render with marked + DOMPurify (cdnjs); without them, show the text as written.
function renderMd(root){root.querySelectorAll('.mdsrc').forEach(src=>{const out=src.nextElementSibling;
  if(window.marked&&window.DOMPurify)out.innerHTML=DOMPurify.sanitize(marked.parse(src.textContent));else{out.textContent=src.textContent;out.classList.add('mdsrc-raw')}})}
document.querySelectorAll('.node').forEach(n=>{const f=()=>{const t=document.querySelector('template[data-key="'+CSS.escape(n.dataset.key)+'"]');
  info.innerHTML=t?t.innerHTML:'<p class="m">No details for this box.</p>';renderMd(info);wireGo(info);
  document.querySelectorAll('.node').forEach(x=>x.classList.toggle('sel',x===n));if(!wide())info.scrollIntoView({behavior:'smooth',block:'nearest'})};
  n.addEventListener('click',f);n.addEventListener('keydown',ev=>{if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();f()}})});
// Tap-to-explain for everything else with a data-tip (phones have no hover; laptops also get the title tooltip).
let sheet=null;function tip(text){if(!sheet){sheet=document.createElement('div');sheet.className='tipsheet';sheet.setAttribute('role','status');
  sheet.innerHTML='<span></span><button aria-label="Close">×</button>';sheet.querySelector('button').onclick=()=>{sheet.hidden=true};document.body.appendChild(sheet)}
  sheet.querySelector('span').textContent=text;sheet.hidden=false}
document.addEventListener('click',ev=>{const t=ev.target.closest('[data-tip]');if(t)tip(t.dataset.tip)});
document.addEventListener('keydown',ev=>{if(ev.key==='Enter'){const t=ev.target.closest&&ev.target.closest('[data-tip]');if(t)tip(t.dataset.tip)}if(ev.key==='Escape'&&sheet)sheet.hidden=true});
// Age of this page, kept current; STALE once two 15-minute rebuilds are missed.
const page=JSON.parse(document.getElementById('page-status').textContent);
const ageEl=document.getElementById('age'),banner=document.getElementById('banner');
const mins=t=>Math.round((Date.now()-Date.parse(t))/60000);
const fmt=m=>m<2?'just now':m<90?m+' min ago':Math.round(m/60)+' h ago';
let newest=page.built;
function tick(){const m=mins(newest);const stale=m>page.build_max_min;ageEl.textContent=(stale?'STALE: ':'')+'updated '+fmt(m);ageEl.classList.toggle('stale',stale)}
tick();setInterval(tick,30000);
function say(html){banner.innerHTML=html;banner.hidden=!html}
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
// Poll the page's own server every 30 s (hosted page only).
async function poll(){
  try{
    const r=await fetch('api/status',{headers:{'X-Hive-Dashboard':'1'},cache:'no-store'});
    if(!r.ok)throw new Error('HTTP '+r.status);
    const s=await r.json();newest=s.status.built;tick();
    const known=new Set(page.decisions.map(d=>d.id));
    const fresh=(s.live.decisions||[]).filter(d=>!known.has(d.id));
    const msgs=[];
    if(s.status.digest&&s.status.digest!==page.digest){
      // Something on the page changed: reload by itself, unless Brian is typing or an answer is being sent.
      const busy=[...document.querySelectorAll('textarea')].some(t=>t.value.trim()||t===document.activeElement)||document.querySelector('.pick:disabled');
      if(!busy){location.reload();return}
      msgs.push('Something new arrived. It will show when you finish typing. <button onclick="location.reload()">Show it now</button>');}
    if(fresh.length)msgs.push('New decision: '+fresh.map(d=>esc(d.identifier+' '+d.title)).join('; ')+'. It gets answer buttons at the next rebuild (within a minute); <a href="https://paperclip.brianmills.dev/BRI/issues/'+esc(fresh[0].identifier)+'">open it on the board</a> now.');
    if(s.live.error)msgs.push('Live check of new decisions failed: '+esc(s.live.error));
    say(msgs.join('<br>'));
  }catch(err){say('Cannot reach the dashboard server ('+esc(err.message)+'). What you see may be old.')}
}
if(page.hosted&&location.protocol.startsWith('http')){poll();setInterval(poll,30000)}
// One-tap answers: post to the page's own server, which comments on the Paperclip task.
document.querySelectorAll('form.answer').forEach(f=>{
  const out=f.querySelector('.result'),btns=[...f.querySelectorAll('.pick')],id=f.closest('.decision').dataset.issue;
  btns.forEach(b=>b.addEventListener('click',async()=>{
    btns.forEach(x=>x.disabled=true);out.className='result';out.textContent='Sending "'+b.value+'"...';
    try{
      const r=await fetch('api/answer',{method:'POST',headers:{'Content-Type':'application/json','X-Hive-Dashboard':'1'},
        body:JSON.stringify({issue:id,option:b.value,note:f.note.value})});
      let d={};try{d=await r.json()}catch(e){}
      if(!r.ok||!d.ok)throw new Error(d.error||('HTTP '+r.status));
      b.classList.add('chosen');out.className='result ok';
      out.textContent=(d.dry_run?'DRY RUN, nothing posted. Would have sent: ':'Sent to the task at '+new Date(d.posted_at||Date.now()).toLocaleTimeString()+': ')+d.body;
    }catch(err){out.className='result err';out.textContent='Not sent: '+err.message+'. Try again, or answer on the board.';btns.forEach(x=>x.disabled=false)}
  }))});
// Free-text messages: post to the page's own server, which comments on Brian's Telegram thread.
document.querySelectorAll('form.message').forEach(f=>{
  const out=f.querySelector('.result'),btn=f.querySelector('button');
  f.addEventListener('submit',async ev=>{
    ev.preventDefault();const text=f.text.value.trim();if(!text){out.className='result err';out.textContent='Type a message first.';return}
    btn.disabled=true;out.className='result';out.textContent='Sending...';
    try{
      const r=await fetch('api/message',{method:'POST',headers:{'Content-Type':'application/json','X-Hive-Dashboard':'1'},body:JSON.stringify({text})});
      let d={};try{d=await r.json()}catch(e){}
      if(!r.ok||!d.ok)throw new Error(d.error||('HTTP '+r.status));
      out.className='result ok';out.textContent=(d.dry_run?'DRY RUN, nothing posted. Would have sent: ':'Sent at '+new Date(d.posted_at||Date.now()).toLocaleTimeString()+': ')+d.body;f.text.value='';
    }catch(err){out.className='result err';out.textContent='Not sent: '+err.message+'. Try again, or reply on Telegram.'}
    btn.disabled=false;
  })});
</script>"""


if __name__ == "__main__":
    sys.exit(main())

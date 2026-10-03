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

--vps is the hosted mode (personal-vps apps/hive-dashboard, rebuilt every 15
minutes by a timer): board calls run on the VPS itself (HIVE_BOARD_LOCAL=1, no
ssh); checks only Brian's PC can see come from the JSON his PC pushes up
(scripts/hive/push_controls.sh), and the VPS-side checks are measured here.
Decision cards get one-tap answer buttons that post to the page's own server
(personal-vps apps/hive-dashboard/server.py), which comments on the Paperclip
task. --json-out writes the small status file that server hands the page's
60-second poll.

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
BUILD_MAX_MIN = 35  # the VPS timer rebuilds every 15 minutes; two missed builds = stale
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


def map_svg(agents, busy: set[str], brains: dict[str, str]) -> str:
    """You at the top, the communication route, project brains around it, agents and tools below."""
    W = 360
    out = [f'<svg viewBox="0 0 {W} 520" role="img" aria-label="Map of the hive brain">']
    def node(x, y, label, sub, kind, href=""):
        cls = {"you": "n-you", "hub": "n-hub", "on": "n-on", "off": "n-off", "tool": "n-tool"}[kind]
        out.append(f'<g class="node {cls}" tabindex="0" data-info="{e(sub)}"><rect x="{x-54}" y="{y-20}" width="108" height="40" rx="12"/>'
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
    node(*you, "You", "the one who decides", "you")
    node(*hub, "Terminal relay", "communication route · decisions come to you here, one at a time", "hub")
    for (x, y), a in zip(agent_pos, agents):
        node(x, y, {"Brian Contact": "Contact"}.get(a["name"], a["name"].split(" ")[0]), f"{AGENT_JOB.get(a['name'], '')} · {'working now' if a['name'] in busy else 'idle'}",
             "on" if a["name"] in busy else "off")
    for (x, y), r in zip(proj_pos, PROJECT_REPOS):
        state = brains.get(r, "unknown")
        node(x, y, SHORT[r], f"{BRAIN_LABEL[state]} · project {r}", "on" if state == "fresh" else "off")
    for (x, y), (t, sub) in zip(tool_pos, [("Safety rules", "checks commands · Jev gate and CC Safety Net"),
                                         ("Learning loop", "issues to rules · GitHub issues, labelled weekly"),
                                         ("Server", "personal-vps · agents run here, backed up nightly")]):
        node(x, y, t, sub, "tool")
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
    rows.append({"name": "Paperclip agents (last good run)", "last": ago(good.get("startedAt")) if good else "never", "status": st, "side": "vps"})
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
        rows.append({"name": "VPS backup (nightly)", "last": ago(when_d.isoformat()) if when_d else "never", "status": st, "side": "vps"})
    return rows


def thread_feed(issues: list[dict], names: dict[str, str]) -> tuple[list[dict], str]:
    """Newest exchanges on Brian's Telegram-bound thread."""
    t = next((i for i in issues if i.get("identifier") == BRIAN_THREAD), None)
    if t is None:
        return [], f"{BRIAN_THREAD} is not in the issues list"
    try:
        cs = board(f"/api/issues/{t['id']}/comments")
    except (RuntimeError, ValueError, subprocess.TimeoutExpired) as err:
        return [], f"could not read {BRIAN_THREAD}: {err}"
    cs = sorted((c for c in cs if not c.get("deletedAt")), key=lambda c: c.get("createdAt") or "", reverse=True)[:6]
    return [{"who": "you" if c.get("authorUserId") == BRIAN else names.get(c.get("authorAgentId"), "an agent"),
             "at": c.get("createdAt"), "body": c.get("body") or ""} for c in cs], ""


def plain(s: str, n: int) -> str:
    """One line of readable text from Markdown: drop link targets, emphasis and heading marks."""
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"(\*\*|__|`)", "", s)
    s = re.sub(r"(^|\n)\s*#{1,6}\s*", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--vps", action="store_true", help="hosted mode, run on the VPS (see above)")
    ap.add_argument("--wsl-controls", type=Path, help="with --vps: the controls report Brian's PC pushed up")
    ap.add_argument("--json-out", type=Path, help="also write the status JSON the page's 60 s poll reads")
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
        ctl_note = f"wsl report {'fresh' if fresh else ('stale' if report else 'missing')}"
    else:
        report, ctl_note = run_controls_here()
        ctl_rows = report["rows"] if report else [{"name": "Controls checks", "last": "?", "status": f"UNKNOWN: {ctl_note}", "side": "wsl"}]
        sources.append({"name": "Controls checks (this machine)", "at": report["at"] if report else None,
                        "state": "ok" if report else "UNKNOWN", "note": ctl_note})
        brains = {r: brain_local(r) for r in PROJECT_REPOS}
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
    thread, thread_err = thread_feed(issues, names)
    interactive = a.vps

    p = ['<title>Hive brain</title>', STYLE, '<div class="app">']
    p.append(f'<header class="top"><b>Hive brain</b><span id="age" data-built="{built.isoformat(timespec="seconds")}">'
             f'built {built:%a %H:%M} UTC</span></header><div id="banner" class="banner" role="status" hidden></div>')

    # Map
    p.append('<section class="screen" id="map"><h1>The big picture</h1><p class="sub">How everything fits together. Tap a box to see what it is.</p>')
    p.append(map_svg(agents, busy, brains))
    p.append('<p class="info" id="info">Blue = active or fresh. Grey dashed = idle, not set up yet, or not known.</p></section>')

    # Live
    p.append('<section class="screen" id="live" hidden><h1>What\'s happening right now</h1><p class="sub">Work in motion, newest first.</p>')
    p.append(f'<h2>Your Telegram thread ({BRIAN_THREAD})</h2><ol class="feed">')
    for c in thread:
        p.append(f'<li class="{"done" if c["who"] == "you" else "now"}"><span class="dot"></span><div><b>{e(c["who"])}</b>'
                 f'<span class="m">{e(ago(c["at"]))}</span><p class="msg">{e(plain(c["body"], 280))}</p></div></li>')
    if thread_err:
        p.append(f'<li class="warn"><span class="dot"></span><div><b>Could not show the thread</b><span class="m">{e(thread_err)}</span></div></li>')
    p.append('</ol><h2>Tasks in motion</h2><ol class="feed">')
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
    p.append('<p class="sub">' + ("Add a note if you like, then tap an answer. It goes to the task as a comment and wakes the agent." if interactive
             else "Answer in the terminal or on the board. (Answer buttons work on the hosted page.)") + '</p>')
    for i in waiting:
        desc = i.get("description") or ""
        p.append(f'<article class="decision" data-issue="{e(i["id"])}"><b>{e(i["title"])}</b><span class="m">{e(i["identifier"])} · asked {e(ago(i.get("createdAt")))}'
                 f' by {e(names.get(i.get("createdByAgentId"), "someone"))}</span><p>{e(plain(desc, 420))}</p>')
        if len(desc) > 420:
            p.append(f'<details><summary>Read all of it</summary><div class="full">{e(desc[:6000])}</div></details>')
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
    p.append('</section>')

    # Health
    all_ok = not quiet and not broken and not bad_sources
    p.append(f'<section class="screen" id="health" hidden><h1>System health</h1><p class="sub">Each check asks whether one part did its job recently.</p>'
             f'<div class="overall {"ok" if all_ok else "warn"}"><b>{"Everything is running" if all_ok else "Something needs a look"}</b>'
             f'<span>{len(ctl_rows) - len(quiet)} of {len(ctl_rows)} checks fine{"; agent failing: " + ", ".join(broken) if broken else ""}'
             f'{"; data not current: " + ", ".join(s["name"] for s in bad_sources) if bad_sources else ""}</span></div><ul class="checks">')
    for r in sorted(ctl_rows, key=lambda r: r["status"] == "ok"):
        ok = r["status"] == "ok"
        p.append(f'<li class="{"ok" if ok else "warn"}"><span>{e(r["name"])}</span><span class="m">{e("fine" if ok else r["status"])} · {e(r["last"])}</span></li>')
    p.append('</ul><h2>Where this page\'s data comes from</h2><ul class="checks">')
    for s in sources:
        ok = s["state"] == "ok"
        p.append(f'<li class="{"ok" if ok else "warn"}"><span>{e(s["name"])}</span><span class="m">{e("current" if ok else s["state"])} · '
                 f'{e(ago(s["at"]) if s["at"] else "never")} · {e(s["note"])}</span></li>')
    p.append('</ul></section>')

    p.append(f'<nav class="tabs">' + "".join(
        f'<button data-s="{s}"{" aria-current=\"page\"" if s == "map" else ""}>{l}{" <i>" + str(n_need) + "</i>" if s == "decide" and n_need else ""}</button>'
        for s, l in [("map", "Map"), ("live", "Live"), ("path", "Path"), ("decide", "Decisions"), ("health", "Health")]) + "</nav></div>")
    status = {"built": built.isoformat(timespec="seconds"), "build_max_min": BUILD_MAX_MIN, "sources": sources,
              "decisions": [{"id": i["id"], "identifier": i["identifier"], "title": i["title"]} for i in waiting],
              "answer_options": ANSWER_OPTIONS, "hosted": interactive, "need": n_need, "checks_not_ok": len(quiet)}
    p.append(f'<script id="page-status" type="application/json">{json.dumps(status).replace("<", "\\u003c")}</script>')
    p.append(SCRIPT)
    write_atomic(a.out, "\n".join(p))
    if a.json_out:
        write_atomic(a.json_out, json.dumps(status, indent=1) + "\n")
    print(f"dashboard: wrote {a.out} ({a.out.stat().st_size} bytes){' and ' + str(a.json_out) if a.json_out else ''}; "
          f"busy {sorted(busy)}, broken {broken}, decisions {n_need}, checks {len(ctl_rows)} ({len(quiet)} not ok), "
          f"sources not current {len(bad_sources)}, thread messages {len(thread)}{' (' + thread_err + ')' if thread_err else ''}, {ctl_note}")
    return 0


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
.answer textarea{font:inherit;color:var(--fg);background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:6px 8px;width:100%;box-sizing:border-box}
.pick{font:600 .88rem var(--body);border:1px solid var(--on);color:var(--on);background:var(--card);border-radius:10px;padding:9px 12px;min-height:44px;cursor:pointer}
.pick:disabled{opacity:.55;cursor:wait}.pick.chosen{background:var(--on);color:var(--bg)}
.result{margin:8px 0 0;font-size:.88rem}.result.ok{color:var(--on);font-weight:600}.result.err{color:var(--warn);font-weight:600}
.link{display:inline-block;margin-top:10px;color:var(--on);font-size:.88rem}
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
// Poll the page's own server every 60 s (hosted page only).
async function poll(){
  try{
    const r=await fetch('api/status',{headers:{'X-Hive-Dashboard':'1'},cache:'no-store'});
    if(!r.ok)throw new Error('HTTP '+r.status);
    const s=await r.json();newest=s.status.built;tick();
    const known=new Set(page.decisions.map(d=>d.id));
    const fresh=(s.live.decisions||[]).filter(d=>!known.has(d.id));
    const msgs=[];
    if(s.status.built!==page.built)msgs.push('A newer page is ready. <button onclick="location.reload()">Reload</button>');
    if(fresh.length)msgs.push('New decision: '+fresh.map(d=>esc(d.identifier+' '+d.title)).join('; ')+'. It gets answer buttons at the next rebuild (within 15 min); <a href="https://paperclip.brianmills.dev/BRI/issues/'+esc(fresh[0].identifier)+'">open it on the board</a> now.');
    if(s.live.error)msgs.push('Live check of new decisions failed: '+esc(s.live.error));
    say(msgs.join('<br>'));
  }catch(err){say('Cannot reach the dashboard server ('+esc(err.message)+'). What you see may be old.')}
}
if(page.hosted&&location.protocol.startsWith('http')){poll();setInterval(poll,60000)}
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
</script>"""


if __name__ == "__main__":
    sys.exit(main())

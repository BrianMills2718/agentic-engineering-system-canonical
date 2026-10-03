#!/usr/bin/env python3
"""Has any hive-brain control gone silent? (hive brain v1, done condition 4)

For each control, the last time it did something and the longest normal gap.
A control past its gap is SILENT; one whose last action failed is FAILING.

  python3 scripts/hive/controls.py

Controls and where their activity is read:
  - Jev gate: last line of ~/.jev-gate/decisions.jsonl (every Claude and Codex tool call)
  - CC Safety Net: newest entry under ~/.cc-safety-net/logs, per client
  - Paperclip agents: latest heartbeat run, and latest successful one (board API on personal-vps)
  - Learning loop: latest summary comment on AES issue #74 (weekly timer on personal-vps)
  - VPS backup: last result of vps-backup.service on personal-vps
  - Project brains: scripts/hive/brain_fresh.py for every ~/code repo with a .project-brain/
  - Hive settings: scripts/hive/settings_check.py (live system matches scripts/hive/settings.json)
Exit status: 0 = every control active, 1 = something SILENT, FAILING or STALE,
2 = a source could not be read (printed as UNKNOWN, never as fine).

Every run appends one line to ~/.hive-brain/controls.jsonl (time, exit status,
counts, the rows not ok), so "exit 0 for a week" can be shown, not remembered.
`readout.py` prints that history.

Every run also replaces ~/.hive-brain/controls-latest.json (or --json-out PATH)
with this run's full rows, each tagged with where it was measured: "wsl" (only
this machine can see it) or "vps" (the VPS can measure it itself). The hosted
dashboard (dashboard.py --vps) reads the "wsl" rows from the copy that
push_controls.sh puts on the VPS, and recomputes the "vps" rows locally.
"""
from __future__ import annotations

import datetime as dt
import argparse
import glob
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMPANY = "da165590-b0b3-4bf9-bb7f-e455292df499"
AES_REPO = "BrianMills2718/agentic-engineering-system-canonical"
SUMMARY_ISSUE = 74
DAY = dt.timedelta(days=1)
NOW = dt.datetime.now(dt.timezone.utc)

REMOTE = r"""
set -euo pipefail
set -a; . /root/.paperclip-cli/board.env; set +a
runs=$(docker exec -e K="$PAPERCLIP_API_KEY" paperclip sh -c "curl -sf -H \"Authorization: Bearer \$K\" \"http://127.0.0.1:3100/api/companies/__C__/heartbeat-runs?limit=200\"")
backup=$(systemctl show vps-backup.service -p Result -p ExecMainExitTimestamp --value --timestamp=unix | paste -sd'|')
echo "$runs" | python3 -c 'import json,sys; r=json.load(sys.stdin); r=r if isinstance(r,list) else r.get("runs",[]); print(json.dumps({"runs":[{k:x.get(k) for k in ("status","startedAt","errorCode")} for x in r],"backup":sys.argv[1]}))' "$backup"
"""


def ts(s: str | None) -> dt.datetime | None:
    if not s:
        return None
    d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    return d if d.tzinfo else d.astimezone()  # naive = this machine's local time


def ago(d: dt.datetime | None) -> str:
    if d is None:
        return "never"
    h = (NOW - d).total_seconds() / 3600
    return f"{h:.0f}h ago" if h < 48 else f"{h / 24:.0f}d ago"


def jsonl_last(path: str) -> dict | None:
    try:
        lines = [l for l in Path(path).read_text().splitlines() if l.strip()]
    except OSError:
        return None
    return json.loads(lines[-1]) if lines else None


VPS_SIDE = ("Paperclip agents", "VPS backup")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json-out", type=Path, default=Path.home() / ".hive-brain" / "controls-latest.json")
    args = ap.parse_args()
    rows: list[tuple[str, str, str, str]] = []  # control, last activity, normal gap, status

    def add(name: str, last: dt.datetime | None, gap: dt.timedelta, failing: str = "") -> None:
        status = "FAILING: " + failing if failing else ("SILENT" if last is None or NOW - last > gap else "ok")
        rows.append((name, ago(last), f"{gap.days}d", status))

    j = jsonl_last(os.path.expanduser("~/.jev-gate/decisions.jsonl"))
    add("Jev gate (Claude + Codex)", ts(j["at"]) if j else None, 7 * DAY)

    last_by_client: dict[str, str] = {}
    for f in glob.glob(os.path.expanduser("~/.cc-safety-net/logs/*/*/*.jsonl")):
        e = jsonl_last(f)
        if e and e.get("ts", "") > last_by_client.get(e.get("agent", "?"), ""):
            last_by_client[e.get("agent", "?")] = e["ts"]
    for client in ("claude-code", "codex"):
        add(f"CC Safety Net ({client})", ts(last_by_client.get(client)), 7 * DAY)

    r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", "personal-vps", "sudo -n bash -s"],
                       input=REMOTE.replace("__C__", COMPANY), capture_output=True, text=True, timeout=120)
    unknown = False
    if r.returncode == 0:
        vps = json.loads(r.stdout)
        runs = sorted(vps["runs"], key=lambda x: x["startedAt"] or "", reverse=True)
        good = next((x for x in runs if x["status"] == "succeeded"), None)
        latest = runs[0] if runs else None
        fail = f"latest run {latest['status']} ({latest['errorCode']})" if latest and latest["status"] == "failed" else ""
        add("Paperclip agents (last good run)", ts(good["startedAt"]) if good else None, 7 * DAY, fail)
        result, _, when = vps["backup"].partition("|")
        when_d = dt.datetime.fromtimestamp(int(when.strip().lstrip("@")), dt.timezone.utc) if when.strip() else None
        add("VPS backup (nightly)", when_d, 2 * DAY, "" if result == "success" else f"result {result}")
    else:
        unknown = True
        rows.append(("Paperclip agents + VPS backup", "?", "-", f"UNKNOWN: ssh failed ({r.stderr.strip()[:80]})"))

    g = subprocess.run(["gh", "api", f"repos/{AES_REPO}/issues/{SUMMARY_ISSUE}/comments?per_page=100"],
                       capture_output=True, text=True)
    if g.returncode == 0:
        comments = json.loads(g.stdout)
        add("Learning loop (weekly, #74)", ts(comments[-1]["created_at"]) if comments else None, 8 * DAY)
    else:
        unknown = True
        rows.append(("Learning loop (weekly, #74)", "?", "-", "UNKNOWN: gh api failed"))

    for brain in sorted(glob.glob(os.path.expanduser("~/code/*/.project-brain"))):
        repo = Path(brain).parent
        b = subprocess.run([sys.executable, str(HERE / "brain_fresh.py"), str(repo)], capture_output=True, text=True)
        status = "ok" if b.returncode == 0 else ("STALE" if b.returncode == 1 else "UNKNOWN")
        rows.append((f"Project brain: {repo.name}", b.stdout.split("last updated ")[-1].split(" at ")[0] if b.stdout else "?",
                     "15 commits/14d", status))

    sc = subprocess.run([sys.executable, str(HERE / "settings_check.py")], capture_output=True, text=True, timeout=300)
    summary = (sc.stdout.strip().splitlines() or ["?"])[-1].replace("settings check: ", "")
    rows.append(("Hive settings match settings.json", "now", "-",
                 "ok" if sc.returncode == 0 else (f"FAILING: {summary}" if sc.returncode == 1 else f"UNKNOWN: {summary}")))

    w = max(len(r[0]) for r in rows)
    for name, last, gap, status in rows:
        print(f"{name:<{w}}  last {last:<9}  normal gap {gap:<15} {status}")
    bad = [r for r in rows if r[3] != "ok" and not r[3].startswith("UNKNOWN")]
    unread = [r for r in rows if r[3].startswith("UNKNOWN")]
    print(f"checked {len(rows)} controls: {len(rows) - len(bad) - len(unread)} ok, {len(bad)} silent/failing/stale, "
          f"{len(unread)} unknown")
    code = 1 if bad else (2 if unknown else 0)
    try:
        hist = Path.home() / ".hive-brain" / "controls.jsonl"
        hist.parent.mkdir(exist_ok=True)
        with hist.open("a") as fh:
            fh.write(json.dumps({"at": NOW.isoformat(timespec="seconds"), "exit": code, "controls": len(rows),
                                 "not_ok": [f"{r[0]}: {r[3]}" for r in rows if r[3] != "ok"]}) + "\n")
    except OSError as e:
        print(f"controls: could not record this run: {e}", file=sys.stderr)
    try:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        tmp = args.json_out.with_suffix(".tmp")
        tmp.write_text(json.dumps({
            "at": NOW.isoformat(timespec="seconds"), "exit": code, "host": os.uname().nodename,
            "rows": [{"name": n, "last": l, "gap": g, "status": st, "side": "vps" if n.startswith(VPS_SIDE) else "wsl"}
                     for n, l, g, st in rows]}, indent=1) + "\n")
        tmp.replace(args.json_out)
    except OSError as e:
        print(f"controls: could not write {args.json_out}: {e}", file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())

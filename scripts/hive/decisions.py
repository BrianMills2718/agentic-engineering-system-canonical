#!/usr/bin/env python3
"""List everything in Paperclip waiting on Brian (hive brain v1, capability C-HUMAN-IF).

Brian answers decisions in his terminal (2026-10-02), so a session runs this and
relays what it prints. Read-only.

  python3 scripts/hive/decisions.py          # human-readable
  python3 scripts/hive/decisions.py --json   # for another script

Prints, in order:
  - agents not working: any agent whose latest run failed or whose status is
    "error", with the failure text and its last good run (2026-10-02: every
    agent failed for 16 hours and nothing showed it);
  - tasks assigned to Brian that are not done (agents file these as "Decision: ...");
  - blocked tasks, which wait on someone;
  - a count line, which is printed even when every group is empty.
Exit status: 0 = read OK and every agent working, 1 = read OK but an agent is
not working, 2 = could not reach Paperclip (the error is printed).

How it reaches Paperclip: `ssh personal-vps`, then the board API key in
/root/.paperclip-cli/board.env, and the request runs inside the container on
127.0.0.1:3100. Paperclip refuses other hostnames (private mode allowlist).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

HOST = "personal-vps"
COMPANY = "da165590-b0b3-4bf9-bb7f-e455292df499"
BOARD = "https://paperclip.brianmills.dev/BRI/issues/"
DONE = {"done", "cancelled"}

REMOTE = r"""
set -euo pipefail
set -a; . /root/.paperclip-cli/board.env; set +a
q(){ docker exec -e K="$PAPERCLIP_API_KEY" paperclip sh -c "curl -sf -H \"Authorization: Bearer \$K\" http://127.0.0.1:3100$1"; }
issues=$(q "/api/companies/__C__/issues?limit=500")
echo "$issues" | python3 -c '
import sys, json, subprocess, os
d = json.load(sys.stdin); d = d if isinstance(d, list) else d.get("issues", d.get("data", []))
keep = [i for i in d if i.get("status") not in ("done", "cancelled") and (i.get("assigneeUserId") or i.get("status") == "blocked")]
out = []
for i in keep:
    r = subprocess.run(["docker", "exec", "-e", "K=" + os.environ["PAPERCLIP_API_KEY"], "paperclip", "sh", "-c",
                        "curl -sf -H \"Authorization: Bearer $K\" http://127.0.0.1:3100/api/issues/" + i["id"] + "/comments"],
                       capture_output=True, text=True)
    try:
        c = json.loads(r.stdout); c = c if isinstance(c, list) else c.get("comments", c.get("data", []))
    except ValueError:
        c = []
    last = sorted(c, key=lambda x: x.get("createdAt") or "")[-1] if c else None
    out.append({k: i.get(k) for k in ("identifier", "title", "status", "assigneeUserId", "assigneeAgentId", "updatedAt", "description")}
               | {"last_comment": (last or {}).get("body"), "last_comment_at": (last or {}).get("createdAt")})
agents = json.loads(subprocess.run(["docker", "exec", "-e", "K=" + os.environ["PAPERCLIP_API_KEY"], "paperclip", "sh", "-c",
                    "curl -sf -H \"Authorization: Bearer $K\" http://127.0.0.1:3100/api/companies/__C__/agents"],
                   capture_output=True, text=True, check=True).stdout)
runs = json.loads(subprocess.run(["docker", "exec", "-e", "K=" + os.environ["PAPERCLIP_API_KEY"], "paperclip", "sh", "-c",
                  "curl -sf -H \"Authorization: Bearer $K\" \"http://127.0.0.1:3100/api/companies/__C__/heartbeat-runs?limit=200\""],
                 capture_output=True, text=True, check=True).stdout)
agents = agents if isinstance(agents, list) else agents.get("agents", [])
runs = runs if isinstance(runs, list) else runs.get("runs", [])
health = []
for a in agents:
    mine = sorted((r for r in runs if r.get("agentId") == a["id"]), key=lambda r: r.get("startedAt") or r.get("createdAt") or "", reverse=True)
    last = mine[0] if mine else {}
    good = next((r for r in mine if r.get("status") == "succeeded"), {})
    health.append({"name": a.get("name"), "status": a.get("status"), "last_run_status": last.get("status"),
                   "last_run_at": last.get("startedAt"), "last_error": last.get("error"), "last_error_code": last.get("errorCode"),
                   "last_success_at": good.get("startedAt"), "runs_seen": len(mine)})
print(json.dumps({"total": len(d), "items": out, "agents": health}))
'
"""


def fetch() -> dict:
    r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", HOST, "sudo -n bash -s"],
                       input=REMOTE.replace("__C__", COMPANY), capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"ssh/board query failed (exit {r.returncode}): {r.stderr.strip()[:400]}")
    return json.loads(r.stdout)


def short(text: str | None, n: int) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= n else text[: n - 1] + "…"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        data = fetch()
    except (RuntimeError, subprocess.TimeoutExpired, ValueError) as e:
        print(f"decisions: could not read Paperclip: {e}", file=sys.stderr)
        return 2
    items = data["items"]
    broken = [a for a in data["agents"] if a["status"] == "error" or a["last_run_status"] == "failed"]
    for_brian = [i for i in items if i["assigneeUserId"]]
    blocked = [i for i in items if not i["assigneeUserId"] and i["status"] == "blocked"]
    if args.json:
        print(json.dumps({"agents_not_working": broken, "for_brian": for_brian, "blocked": blocked,
                          "total_tasks": data["total"]}, indent=1))
        return 1 if broken else 0
    print(f"Agents not working: {len(broken)} of {len(data['agents'])}")
    for a in broken:
        print(f"  {a['name']} [{a['status']}] latest run {a['last_run_status']} at {(a['last_run_at'] or '?')[:16]}: "
              f"{short(a['last_error'], 160)} ({a['last_error_code']})")
        print(f"    last good run: {(a['last_success_at'] or '')[:16] or 'none in the last 200 runs'}")
    for title, group in (("Waiting on Brian", for_brian), ("Blocked (waiting on someone)", blocked)):
        print(f"{title}: {len(group)}")
        for i in sorted(group, key=lambda i: i["updatedAt"] or "", reverse=True):
            print(f"  {i['identifier']} [{i['status']}] {short(i['title'], 110)}")
            print(f"    {BOARD}{i['identifier']}")
            said = i["last_comment"] or i["description"]
            if said:
                print(f"    latest: {short(said, 300)}")
    print(f"checked {data['total']} Paperclip tasks and {len(data['agents'])} agents: {len(broken)} agents not working, "
          f"{len(for_brian)} tasks waiting on Brian, {len(blocked)} blocked")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())

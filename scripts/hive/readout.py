#!/usr/bin/env python3
"""Weekly hive-brain readout (hive brain v1, capability C-EVAL).

What the system did over the last N days, from its own logs and traces, so Brian
and the learning loop can judge it without opening five tools:

  python3 scripts/hive/readout.py            # last 7 days
  python3 scripts/hive/readout.py --days 30

Sections:
  - Paperclip: tasks created and finished, pilot tasks ("Pilot:" titles) with
    status, agent runs succeeded/failed with failure codes;
  - Gates: Jev decisions by verdict and source (rule K1 blocks counted
    separately), CC Safety Net denials by client;
  - Learning loop: kind:* issues opened in the period, with their families;
  - Controls: the one-line result of scripts/hive/controls.py.
Every section prints its counts even when they are zero. Exit status: 0 = read
everything, 2 = a source could not be read (named as UNREADABLE).
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import glob
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMPANY = "da165590-b0b3-4bf9-bb7f-e455292df499"
AES_REPO = "BrianMills2718/agentic-engineering-system-canonical"
REMOTE = r"""
set -euo pipefail
set -a; . /root/.paperclip-cli/board.env; set +a
q(){ docker exec -e K="$PAPERCLIP_API_KEY" paperclip sh -c "curl -sf -H \"Authorization: Bearer \$K\" \"http://127.0.0.1:3100$1\""; }
{ q "/api/companies/__C__/issues?limit=500"; echo; q "/api/companies/__C__/heartbeat-runs?limit=500"; echo; q "/api/companies/__C__/agents"; } \
 | python3 -c 'import json,sys; i,r,a=[json.loads(l) for l in sys.stdin if l.strip()]; L=lambda x,k: x if isinstance(x,list) else x.get(k,[]); print(json.dumps({"issues":[{k:x.get(k) for k in ("id","identifier","title","status","createdAt","updatedAt","completedAt")} for x in L(i,"issues")],"runs":[{**{k:x.get(k) for k in ("agentId","status","startedAt","finishedAt","errorCode")},"issueId":(x.get("contextSnapshot") or {}).get("issueId"),"model":(x.get("usageJson") or {}).get("model"),"costUsd":(x.get("usageJson") or {}).get("costUsd"),"billing":(x.get("usageJson") or {}).get("billingType"),"tokens":((x.get("usageJson") or {}).get("inputTokens") or 0)+((x.get("usageJson") or {}).get("outputTokens") or 0)} for x in L(r,"runs")],"agents":{x["id"]:x["name"] for x in L(a,"agents")}}))'
"""


def when(s: str | None) -> dt.datetime | None:
    if not s:
        return None
    d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    return d if d.tzinfo else d.astimezone()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=7)
    a = ap.parse_args()
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.days)
    inside = lambda s: (d := when(s)) is not None and d >= since
    unreadable = []
    print(f"Hive brain readout, last {a.days} days (since {since:%Y-%m-%d %H:%M} UTC)")

    r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", "personal-vps", "sudo -n bash -s"],
                       input=REMOTE.replace("__C__", COMPANY), capture_output=True, text=True, timeout=180)
    print("\nPaperclip")
    if r.returncode == 0:
        pc = json.loads(r.stdout)
        made = [i for i in pc["issues"] if inside(i["createdAt"])]
        done = [i for i in pc["issues"] if i["status"] == "done" and inside(i.get("completedAt") or i["updatedAt"])]
        pilot = [i for i in pc["issues"] if (i["title"] or "").lower().startswith("pilot")]
        print(f"  tasks: {len(made)} created, {len(done)} finished")
        print(f"  pilot tasks: {len(pilot)} ({dict(collections.Counter(i['status'] for i in pilot))})")
        byissue = collections.defaultdict(list)
        for x in pc["runs"]:
            byissue[x.get("issueId")].append(x)
        ids = {i["identifier"]: i for i in pc["issues"]}
        for i in pilot:
            print(f"    {i['identifier']} [{i['status']}] {(i['title'] or '')[:90]}")
            rs = byissue.get(i.get("id"), [])
            cost = sum(x.get("costUsd") or 0 for x in rs)
            models = dict(collections.Counter(x.get("model") or "?" for x in rs))
            start, end = when(i.get("createdAt")), when(i.get("completedAt") or (i["updatedAt"] if i["status"] == "done" else None))
            hours = f"{(end - start).total_seconds() / 3600:.1f} h from created to done" if start and end else "not done yet"
            subs = sum((x.get("billing") or "").startswith("subscription") for x in rs)
            print(f"      cost and throughput: {len(rs)} runs, ${cost:.2f} at API prices ({subs} of {len(rs)} covered by a subscription), "
                  f"models {models}, {sum(x.get('tokens') or 0 for x in rs):,} tokens, {hours}")
        runs = [x for x in pc["runs"] if inside(x["startedAt"])]
        by = collections.defaultdict(collections.Counter)
        for x in runs:
            by[pc["agents"].get(x["agentId"], x["agentId"][:8])][x["status"]] += 1
        print(f"  agent runs: {len(runs)} ({dict(collections.Counter(x['status'] for x in runs))})")
        for name, c in sorted(by.items()):
            print(f"    {name}: {dict(c)}")
        fails = collections.Counter(x["errorCode"] for x in runs if x["status"] == "failed")
        print(f"  failure codes: {dict(fails) or 'none'}")
    else:
        unreadable.append("Paperclip")
        print(f"  UNREADABLE: ssh failed ({r.stderr.strip()[:120]})")

    print("\nGates")
    try:
        rows, damaged = [], 0
        for l in Path(os.path.expanduser("~/.jev-gate/decisions.jsonl")).read_text(errors="replace").splitlines():
            try:
                rows.append(json.loads(l))
            except ValueError:
                damaged += l.strip() != ""
        if damaged:
            print(f"  note: skipped {damaged} damaged line(s) in the Jev log")
        rows = [x for x in rows if inside(x.get("at"))]
        print(f"  Jev: {len(rows)} decisions; by verdict {dict(collections.Counter(x['verdict'] for x in rows))}; "
              f"by source {dict(collections.Counter(x['source'] for x in rows))}")
        print(f"  rule K1 blocks: {sum(x.get('rule') == 'K1-worktree-cwd' for x in rows)}")
    except OSError as e:
        unreadable.append("Jev log")
        print(f"  UNREADABLE: Jev log ({e})")
    denies = collections.Counter()
    seen = 0
    for f in glob.glob(os.path.expanduser("~/.cc-safety-net/logs/*/*/*.jsonl")):
        for line in open(f):
            try:
                x = json.loads(line)
            except ValueError:
                continue
            if inside(x.get("ts")):
                seen += 1
                if x.get("decision") != "allow":
                    denies[x.get("agent", "?")] += 1
    print(f"  CC Safety Net: {seen} checks, denials by client {dict(denies) or 'none'}")

    print("\nLearning loop")
    g = subprocess.run(["gh", "issue", "list", "--repo", AES_REPO, "--state", "all", "--limit", "200", "--search",
                        f"created:>={since:%Y-%m-%d}", "--json", "number,title,labels,createdAt"], capture_output=True, text=True)
    if g.returncode == 0:
        items = [i for i in json.loads(g.stdout) if any(l["name"].startswith("kind:") for l in i["labels"])]
        fam = collections.Counter(l["name"] for i in items for l in i["labels"] if l["name"].startswith("family:"))
        kinds = collections.Counter(l["name"] for i in items for l in i["labels"] if l["name"].startswith("kind:"))
        print(f"  kind:* issues opened: {len(items)} {dict(kinds)}; families {dict(fam) or 'none yet'}")
    else:
        unreadable.append("GitHub issues")
        print("  UNREADABLE: gh issue list failed")

    print("\nControls")
    c = subprocess.run([sys.executable, str(HERE / "controls.py")], capture_output=True, text=True, timeout=300)
    lines = c.stdout.strip().splitlines()
    for line in lines:
        if "SILENT" in line or "FAILING" in line or "STALE" in line or "UNKNOWN" in line:
            print("  " + " ".join(line.split()))
    print("  " + (lines[-1] if lines else f"UNREADABLE: controls.py exit {c.returncode}"))
    try:
        runs = [json.loads(l) for l in (Path.home() / ".hive-brain" / "controls.jsonl").read_text().splitlines() if l.strip()]
        runs = [x for x in runs if inside(x["at"])]
        days = collections.defaultdict(set)
        for x in runs:
            days[x["at"][:10]].add(x["exit"])
        clean = sorted(d for d, codes in days.items() if codes == {0})
        print(f"  history: {len(runs)} recorded runs on {len(days)} days; days with only clean runs: {len(clean)} "
              f"({', '.join(clean) or 'none'})")
    except OSError:
        print("  history: none recorded yet (~/.hive-brain/controls.jsonl)")

    if unreadable:
        print(f"\nUNREADABLE sources: {', '.join(unreadable)}")
    return 2 if unreadable else 0


if __name__ == "__main__":
    sys.exit(main())

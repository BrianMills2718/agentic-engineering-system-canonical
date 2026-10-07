#!/usr/bin/env python3
"""Hive must-never rules, judged from what actually ran (hive hardening U7, rules N1-N4).

Reads the records the hive already writes (no new trace store yet; U6's OpenTelemetry viewer is
later) and reports each rule as PASS, VIOLATION or UNKNOWN with the evidence it used:

  N1 only Brian's replies are passed on as his: every "from phone" relay of a BRI-2 comment must be
     a comment from Brian's Telegram account or carrying the dashboard/terminal prefix (relay journal
     on personal-vps plus the BRI-2 comments themselves).
  N2 a crash never reads as a pass: no hive-controls run both raised a Python traceback and pushed
     its result to the dashboard (laptop journal of hive-controls.service).
  N3 no stall goes unreported: every hive-stall check that turned stalled posted its fyi line
     (/var/lib/hive-stall/checks-*.jsonl on personal-vps).
  N4 every scheduled check reports in its window: relay heartbeat <= 10 min, hive-stall <= 2 h,
     hive-controls <= 26 h.

Usage: must_never.py [--since 2026-10-03] [--json]   exit 0 all PASS or UNKNOWN, 1 any VIOLATION.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRI2 = "519c6831-6967-4177-aef5-5aaea5d91850"
BRIAN_TELEGRAM_ID = "8055596302"
BRIAN_PREFIXES = ("Brian (dashboard):", "Brian (terminal):")


def run(cmd: list[str], timeout: int = 90) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd[:3])}... exit {r.returncode}: {r.stderr.strip()[:200]}")
    return r.stdout


def vps(command: str) -> str:
    return run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", "personal-vps", f"sudo -n bash -c {json.dumps(command)}"])


def is_brian(c: dict) -> bool:
    for section in (c.get("metadata") or {}).get("sections") or []:
        if section.get("title") == "Telegram sender":
            if any(r.get("label") == "Provider ID" and str(r.get("value")) == BRIAN_TELEGRAM_ID for r in section.get("rows") or []):
                return True
    return (c.get("body") or "").strip().startswith(BRIAN_PREFIXES)


def n1(since: str) -> dict:
    journal = vps(f"journalctl -u telegram-relay --since '{since}' --no-pager -o cat")
    relayed = re.findall(r"from phone: (?:user comment|Brian's reply) ([0-9a-f]{8})", journal)
    comments = json.loads(run(["bash", str(HERE / "board.sh"), "GET", f"/api/issues/{BRI2}/comments"]))
    comments = comments if isinstance(comments, list) else comments.get("comments", comments)
    by_prefix = {c["id"][:8]: c for c in comments}
    bad = [f"{cid} {by_prefix[cid].get('createdAt', '')[:16]} {(by_prefix[cid].get('body') or '')[:50]!r}"
           for cid in relayed if cid in by_prefix and not is_brian(by_prefix[cid])]
    unknown = [cid for cid in relayed if cid not in by_prefix]
    status = "VIOLATION" if bad else ("UNKNOWN" if unknown and not relayed else "PASS")
    return {"rule": "N1", "status": status, "checked": len(relayed), "violations": bad, "unresolved": unknown,
            "source": "relay journal + BRI-2 comments"}


def n2(since: str) -> dict:
    out = run(["journalctl", "--user", "-u", "hive-controls.service", "--since", since, "--no-pager", "-o", "json"])
    runs: dict[str, dict] = {}
    for line in out.splitlines():
        e = json.loads(line)
        inv = e.get("_SYSTEMD_INVOCATION_ID") or e.get("INVOCATION_ID") or "?"
        msg = e.get("MESSAGE") if isinstance(e.get("MESSAGE"), str) else ""
        r = runs.setdefault(inv, {"crash": False, "pushed": False, "at": e.get("__REALTIME_TIMESTAMP")})
        r["crash"] |= msg.startswith("Traceback")
        r["pushed"] |= msg.startswith("push_controls: pushed")
    bad = [datetime.fromtimestamp(int(r["at"]) / 1e6, timezone.utc).isoformat(timespec="minutes")
           for r in runs.values() if r["crash"] and r["pushed"]]
    return {"rule": "N2", "status": "VIOLATION" if bad else ("PASS" if runs else "UNKNOWN"),
            "checked": len(runs), "violations": bad, "source": "laptop journal of hive-controls.service"}


def n3() -> dict:
    lines = vps("cat /var/lib/hive-stall/checks-*.jsonl 2>/dev/null || true").splitlines()
    checks = [json.loads(l) for l in lines if l.strip()]
    bad, previous = [], False
    for c in checks:
        if c.get("stalled") and not previous and not c.get("posted"):
            bad.append(c.get("at"))
        previous = bool(c.get("stalled"))
    return {"rule": "N3", "status": "VIOLATION" if bad else ("PASS" if checks else "UNKNOWN"),
            "checked": len(checks), "violations": bad, "source": "hive-stall checks on personal-vps"}


def n4() -> dict:
    now = time.time()
    ages: dict[str, float | None] = {}
    try:
        ages["telegram relay heartbeat"] = now - float(vps("cat /var/lib/telegram-relay/heartbeat").strip())
    except Exception:  # noqa: BLE001 - reported as unknown
        ages["telegram relay heartbeat"] = None
    try:
        last = json.loads(vps("tail -qn1 $(ls -1 /var/lib/hive-stall/checks-*.jsonl | tail -1)"))["at"]
        ages["hive-stall"] = now - datetime.fromisoformat(last).timestamp()
    except Exception:  # noqa: BLE001
        ages["hive-stall"] = None
    hist = Path.home() / ".hive-brain" / "controls.jsonl"
    try:
        last = json.loads(hist.read_text().splitlines()[-1])["at"]
        ages["hive-controls"] = now - datetime.fromisoformat(last.replace("Z", "+00:00")).timestamp()
    except Exception:  # noqa: BLE001
        ages["hive-controls"] = None
    limits = {"telegram relay heartbeat": 600, "hive-stall": 7200, "hive-controls": 26 * 3600}
    bad = [f"{k} last {ages[k] / 60:.0f} min ago (limit {limits[k] / 60:.0f})" for k in limits
           if ages[k] is not None and ages[k] > limits[k]]
    unknown = [k for k in limits if ages[k] is None]
    return {"rule": "N4", "status": "VIOLATION" if bad else ("UNKNOWN" if unknown else "PASS"),
            "checked": len(limits), "violations": bad, "unresolved": unknown,
            "ages_minutes": {k: (round(v / 60) if v is not None else None) for k, v in ages.items()},
            "source": "relay heartbeat, hive-stall checks, ~/.hive-brain/controls.jsonl"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--since", default="2026-10-03")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    results = []
    for name, fn in (("N1", lambda: n1(args.since)), ("N2", lambda: n2(args.since)), ("N3", n3), ("N4", n4)):
        try:
            results.append(fn())
        except Exception as e:  # noqa: BLE001 - one unreadable source never hides the others
            results.append({"rule": name, "status": "UNKNOWN", "error": str(e)[:200]})
    for r in results:
        if args.json:
            print(json.dumps(r))
        else:
            detail = "; ".join(r.get("violations") or []) or r.get("error") or ""
            print(f"{r['rule']} {r['status']:<9} checked={r.get('checked', '-')} {detail}")
    counts = {s: sum(r["status"] == s for r in results) for s in ("PASS", "VIOLATION", "UNKNOWN")}
    print(f"must-never: {counts['PASS']} pass, {counts['VIOLATION']} violation, {counts['UNKNOWN']} unknown")
    return 1 if counts["VIOLATION"] else 0


if __name__ == "__main__":
    sys.exit(main())

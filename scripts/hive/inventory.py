#!/usr/bin/env python3
"""Inventory of what actually runs for the hive (hive hardening U4): one JSON snapshot that AES compares
with the running pieces its target declares.

  inventory.py [--out PATH]   default PATH: .aes/running-inventory.json in the current repository

Items: {host, kind, name}
  host "wsl"            kind "systemd_unit"   every user unit file (systemctl --user list-unit-files)
  host "personal-vps"   kind "container"      every running container (docker ps)
  host "personal-vps"   kind "systemd_unit"   every unit file under /etc/systemd/system (locally installed)
  host "paperclip"      kind "agent"          every Paperclip agent on the board
A source that cannot be read is listed under "unreadable", never silently left out.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMPANY = "da165590-b0b3-4bf9-bb7f-e455292df499"


def run(cmd: list[str]) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"exit {r.returncode}: {r.stderr.strip()[:160]}")
    return r.stdout


def vps(command: str) -> str:
    return run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", "personal-vps", command])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=Path(".aes/running-inventory.json"))
    args = ap.parse_args()
    items, unreadable = [], []
    sources = {
        ("wsl", "systemd_unit"): lambda: [l.split()[0] for l in run(
            ["systemctl", "--user", "list-unit-files", "--type=service", "--type=timer", "--no-legend"]).splitlines() if l.strip()],
        ("personal-vps", "container"): lambda: vps("docker ps --format '{{.Names}}'").split(),
        ("personal-vps", "systemd_unit"): lambda: [p.rsplit("/", 1)[-1] for p in vps(
            "ls -1 /etc/systemd/system/*.service /etc/systemd/system/*.timer 2>/dev/null").split()],
        ("paperclip", "agent"): lambda: [a["name"] for a in (lambda d: d if isinstance(d, list) else d.get("items", d))(
            json.loads(run(["bash", str(HERE / "board.sh"), "GET", f"/api/companies/{COMPANY}/agents"])))],
    }
    for (host, kind), read in sources.items():
        try:
            items += [{"host": host, "kind": kind, "name": n} for n in sorted(set(read()))]
        except Exception as e:  # noqa: BLE001 - recorded, never hidden
            unreadable.append({"host": host, "kind": kind, "error": str(e)[:200]})
    snapshot = {"collected_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "items": items,
                "unreadable": unreadable}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(snapshot, indent=1) + "\n", encoding="utf-8")
    print(f"inventory: {len(items)} items from {len(sources) - len(unreadable)} of {len(sources)} sources "
          f"-> {args.out}" + (f"; unreadable: {[u['host'] + '/' + u['kind'] for u in unreadable]}" if unreadable else ""))
    return 2 if unreadable else 0


if __name__ == "__main__":
    raise SystemExit(main())

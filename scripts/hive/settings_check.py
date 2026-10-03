#!/usr/bin/env python3
"""Does the live hive match scripts/hive/settings.json? (hive brain v1, C-GOV)

  python3 scripts/hive/settings_check.py

Checks, one line each:
  - every Paperclip agent named in the file exists with that role, heartbeat
    values and env keys, and has no AI-connection binding; no extra agents;
  - Jev gate mode (~/.jev-gate/mode, default observe) and the rule K1 guard
    (~/.local/bin/jev-gate-worktree-guard, wired into ~/.local/bin/jev-gate-hook);
  - CC Safety Net enabled in ~/.claude/settings.json;
  - each named timer is enabled (WSL user timers here, VPS timers over ssh).
Exit status: 0 = live matches the file, 1 = a difference (each printed as
DIFF), 2 = a source could not be read (UNKNOWN).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WANT = json.loads((HERE / "settings.json").read_text())


def main() -> int:
    diffs, unknown, ok = [], [], 0

    def check(name: str, live, want) -> None:
        nonlocal ok
        if live == want:
            ok += 1
            print(f"ok    {name}: {want}")
        else:
            diffs.append(name)
            print(f"DIFF  {name}: live {live!r}, settings.json says {want!r}")

    r = subprocess.run(["bash", str(HERE / "board.sh"), "GET", f"/api/companies/{WANT['paperclip']['company']}/agents"],
                       capture_output=True, text=True, timeout=120)
    if r.returncode == 0:
        agents = json.loads(r.stdout)
        agents = {a["name"]: a for a in (agents if isinstance(agents, list) else agents.get("agents", []))}
        check("Paperclip agent names", sorted(agents), sorted(WANT["paperclip"]["agents"]))
        for name, want in WANT["paperclip"]["agents"].items():
            a = agents.get(name)
            if not a:
                continue
            rc, ac = a.get("runtimeConfig") or {}, a.get("adapterConfig") or {}
            check(f"{name} id", a["id"], want["id"])
            check(f"{name} role", a.get("role"), want["role"])
            hb = rc.get("heartbeat") or {}
            check(f"{name} heartbeat", {k: hb.get(k) for k in want["heartbeat"]}, want["heartbeat"])
            check(f"{name} env keys", sorted((ac.get("env") or {}).keys()), sorted(want["env"]))
            if "model" in want:
                check(f"{name} model", ac.get("model"), want["model"])
            check(f"{name} AI-connection binding", "aiConnection" in rc, False)
    else:
        unknown.append("Paperclip agents")
        print(f"UNKNOWN Paperclip agents: {r.stderr.strip()[:120]}")

    mode_file = Path.home() / ".jev-gate" / "mode"
    mode = os.environ.get("JEV_GATE_MODE") or (mode_file.read_text().strip() if mode_file.exists() else "observe")
    check("Jev gate mode", mode, WANT["gates"]["jev_mode"])
    guard = Path.home() / ".local/bin/jev-gate-worktree-guard"
    hook = Path.home() / ".local/bin/jev-gate-hook"
    wired = guard.exists() and os.access(guard, os.X_OK) and hook.exists() and "jev-gate-worktree-guard" in hook.read_text()
    check("rule K1 guard installed and wired", wired, WANT["gates"]["k1_guard_installed"])
    try:
        plugins = json.loads((Path.home() / ".claude/settings.json").read_text()).get("enabledPlugins", {})
        check("CC Safety Net enabled", bool(plugins.get(WANT["gates"]["cc_safety_net_plugin"])), True)
    except (OSError, ValueError) as e:
        unknown.append("Claude settings")
        print(f"UNKNOWN CC Safety Net: {e}")

    for t in WANT["timers"]["wsl_user"]:
        s = subprocess.run(["systemctl", "--user", "is-enabled", t], capture_output=True, text=True).stdout.strip()
        check(f"WSL timer {t}", s, "enabled")
    v = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", "personal-vps",
                        "systemctl is-enabled " + " ".join(WANT["timers"]["personal_vps"])], capture_output=True, text=True)
    states = v.stdout.split()
    if len(states) == len(WANT["timers"]["personal_vps"]):
        for t, s in zip(WANT["timers"]["personal_vps"], states):
            check(f"VPS timer {t}", s, "enabled")
    else:
        unknown.append("VPS timers")
        print(f"UNKNOWN VPS timers: {v.stderr.strip()[:120] or v.stdout.strip()[:120]}")

    print(f"settings check: {ok} ok, {len(diffs)} differ, {len(unknown)} unknown")
    return 1 if diffs else (2 if unknown else 0)


if __name__ == "__main__":
    sys.exit(main())

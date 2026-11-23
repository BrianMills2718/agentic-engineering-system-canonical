"""AES's own `lockstep.yaml` plans every file in the Lockstep package, and its client settings run the edit hook."""

import json
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]


def _pretool_commands(settings: Path) -> list[str]:
    data = json.loads(settings.read_text())
    return [h.get("command", "") for entry in data.get("hooks", {}).get("PreToolUse", []) for h in entry.get("hooks", [])]


@pytest.mark.req("lockstep-plan-format/every-package-file-is-planned-and-the-hook-refuses-an-unplanned-one")
def test_every_package_file_is_planned_and_the_hook_refuses_an_unplanned_one(tmp_path):
    side = yaml.safe_load((ROOT / "lockstep.yaml").read_text())
    tracked = set(subprocess.run(["git", "-C", str(ROOT), "ls-files", "src/lockstep"], check=True,
                                 capture_output=True, text=True).stdout.split())
    planned = {row["path"] for row in side.get("layout") or []}
    assert tracked, "git lists no files under src/lockstep/"
    assert not tracked - planned, f"files under src/lockstep/ with no layout row: {sorted(tracked - planned)}"
    assert "src/lockstep/" in (side.get("governed") or [])
    assert "src/lockstep/*" in (side.get("fixed") or [])
    for settings in (ROOT / ".claude/settings.json", ROOT / ".codex/hooks.json"):
        assert any("lockstep-hook" in c for c in _pretool_commands(settings)), f"{settings} runs no lockstep-hook"

    call = {"hook_event_name": "PreToolUse", "tool_name": "Write", "cwd": str(ROOT),
            "tool_input": {"file_path": str(ROOT / "src/lockstep/not_planned.py"), "content": "x = 1\n"}}
    env = {"PATH": "/usr/bin:/bin", "HOME": str(tmp_path), "XDG_STATE_HOME": str(tmp_path / "state")}
    out = subprocess.run([sys.executable, "-m", "lockstep.hook"], input=json.dumps(call), capture_output=True,
                         text=True, cwd=ROOT, env=env)
    decision = json.loads(out.stdout or "{}").get("hookSpecificOutput", {})
    assert decision.get("permissionDecision") == "deny", out.stdout + out.stderr
    assert "lockstep.yaml" in decision.get("permissionDecisionReason", "")

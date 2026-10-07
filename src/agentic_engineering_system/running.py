"""`aes running check`: what actually runs against the running pieces the target declares (hive hardening U4).

Every running thing should be a file in git and a declared running piece. A collector (for the hive,
`scripts/hive/inventory.py`) writes a snapshot of what runs - `{collected_at, items: [{host, kind, name}],
unreadable: [...]}` - by default to `.aes/running-inventory.json` (not tracked; `AES_RUNNING_INVENTORY`
overrides). Inside each running scope, an item that no running piece declares is **undeclared** and
fails `aes status`; a declared piece absent from the snapshot is reported as **not running** (a finding,
not a failure, since a timer's service unit is only listed while it exists). A scope whose source was
unreadable is reported as such, never as clean.
"""

from __future__ import annotations

import fnmatch
import json
import os
from dataclasses import dataclass, field
from pathlib import Path

from .records import TargetRecord

DEFAULT_INVENTORY = Path(".aes") / "running-inventory.json"


@dataclass
class RunningReport:
    collected_at: str | None
    in_scope: int = 0
    undeclared: list[str] = field(default_factory=list)
    not_running: list[str] = field(default_factory=list)
    unreadable: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.undeclared


def inventory_path(root: Path) -> Path:
    override = os.environ.get("AES_RUNNING_INVENTORY")
    return Path(override) if override else Path(root) / DEFAULT_INVENTORY


def load_inventory(path: Path) -> dict | None:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def check_running(target: TargetRecord, inventory: dict) -> RunningReport:
    report = RunningReport(collected_at=inventory.get("collected_at"))
    items = {(i["host"], i["kind"], i["name"]) for i in inventory.get("items", [])}
    blind = {(u.get("host"), u.get("kind")) for u in inventory.get("unreadable", [])}
    declared = {(p.host, p.kind, p.name) for p in target.running_pieces}
    for scope in target.running_scopes:
        if (scope.host, scope.kind) in blind:
            report.unreadable.append(f"{scope.host}/{scope.kind} ({scope.id})")
            continue
        for host, kind, name in sorted(items):
            if host == scope.host and kind == scope.kind and any(fnmatch.fnmatch(name, g) for g in scope.include):
                report.in_scope += 1
                if (host, kind, name) not in declared:
                    report.undeclared.append(f"{host}/{kind}/{name}")
    report.undeclared = sorted(set(report.undeclared))
    report.not_running = sorted(f"{h}/{k}/{n}" for h, k, n in declared - items if (h, k) not in blind)
    return report


def render(report: RunningReport) -> str:
    head = "OK" if report.ok else "FAIL"
    lines = [f"{head} running: {report.in_scope} in scope, {len(report.undeclared)} undeclared, "
             f"{len(report.not_running)} declared but not running (snapshot {report.collected_at})"]
    lines += [f"  undeclared: {u}" for u in report.undeclared]
    lines += [f"  not running: {n}" for n in report.not_running]
    lines += [f"  unreadable: {u}" for u in report.unreadable]
    if report.undeclared:
        lines.append("  fix: declare each as a running_pieces entry (through aes plan) with the file in git that "
                     "defines it, or stop it")
    return "\n".join(lines)

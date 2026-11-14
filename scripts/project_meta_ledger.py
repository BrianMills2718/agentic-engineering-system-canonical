#!/usr/bin/env python3
"""Ledger of what still calls Project Meta (retirement plan, slice 0). Read-only; no model call.

Three measured lists: other repositories that mention a Project Meta file path, systemd units that
mention the Project Meta path (with whether their timers are enabled), and commands in a bin folder
that mention it. A mention is a text match of `project-meta/<path>`, not proof of use at runtime.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location("triage", Path(__file__).with_name("project_meta_docs_triage.py"))
triage = importlib.util.module_from_spec(_spec)
sys.modules["triage"] = triage
_spec.loader.exec_module(triage)

SUFFIXES = (".py", ".sh", ".yml", ".yaml", ".md", ".json", ".toml", ".service", ".timer", ".conf", ".mk", "")
CALLED = ("scripts/", "policy/", "PROJECT_GRAPH.json")


def called_files(repo: Path) -> list[str]:
    """Tracked files at depth 1 or 2 under scripts/ and policy/, plus the project graph."""
    out = subprocess.run(["git", "-C", str(repo), "ls-files"], capture_output=True, text=True).stdout.splitlines()
    return [f for f in out if f.startswith(CALLED) and f.count("/") <= 2]


SKIP_DIRS = {".git", "worktrees", "node_modules", ".venv", "__pycache__", "archive", "data", "runs"}
MAX_BYTES = 2_000_000


def mentions_in(root: Path, name: str, files: set[str], docs: bool = False) -> dict[str, int]:
    """For each file of the Project Meta checkout, how many files under root mention `<name>/<file>`.

    docs=False counts code and configuration files (everything but .md); docs=True counts only .md files.

    Each file is read once; only text containing `<name>/` is searched further.
    """
    pattern = re.compile(re.escape(name) + r"/([A-Za-z0-9_./-]+)")
    counts: dict[str, int] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and "worktrees" not in d]
        for fn in filenames:
            path = Path(dirpath) / fn
            if path.suffix not in SUFFIXES or (path.suffix == ".md") != docs:
                continue
            try:
                if path.stat().st_size > MAX_BYTES or not path.is_file():
                    continue
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if f"{name}/" not in text:
                continue
            for hit in {m.rstrip(".,)`'\"") for m in pattern.findall(text)}:
                if hit in files:
                    counts[hit] = counts.get(hit, 0) + 1
    return counts


def repo_callers(repo: Path, workspace: Path, files: list[str]) -> dict[str, dict[str, int]]:
    """For each other repository under workspace, the files of repo it mentions and how many of its files do."""
    known = set(files)
    result: dict[str, dict[str, int]] = {}
    for other in sorted(workspace.iterdir()):
        if other == repo or not other.is_dir() or other.name.startswith(".") or "worktrees" in other.name:
            continue
        found = mentions_in(other, repo.name, known)   # code and configuration callers only
        if found:
            result[other.name] = found
    return result


def units(unit_dirs: list[Path], name: str) -> list[dict]:
    """Units whose text mentions name; for a timer, whether it is enabled (systemctl --user is-enabled)."""
    seen: dict[str, dict] = {}
    for d in unit_dirs:
        for p in sorted(d.glob("*.service")) + sorted(d.glob("*.timer")):
            if p.name in seen:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if p.suffix == ".timer":
                sibling = p.with_suffix(".service")
                if sibling.is_file():
                    text += sibling.read_text(encoding="utf-8", errors="ignore")
            if name not in text:
                continue
            row = {"unit": p.name, "kind": p.suffix[1:]}
            if p.suffix == ".timer":
                done = subprocess.run(["systemctl", "--user", "is-enabled", p.name], capture_output=True, text=True)
                row["enabled"] = done.stdout.strip() or done.stderr.strip()
            seen[p.name] = row
    return list(seen.values())


def commands(bin_dir: Path, name: str) -> list[str]:
    """Files in bin_dir whose text mentions name."""
    found = []
    for p in sorted(bin_dir.iterdir()) if bin_dir.is_dir() else []:
        if p.is_file():
            try:
                if name in p.read_text(encoding="utf-8", errors="ignore"):
                    found.append(p.name)
            except OSError:
                continue
    return found


def origin_of(path: Path) -> str:
    """The origin URL of a checkout, or '' when it has none; checkouts sharing one URL are copies of one repository."""
    done = subprocess.run(["git", "-C", str(path), "remote", "get-url", "origin"], capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 else ""


def add_origins(ledger: dict, workspace: Path) -> None:
    """Add origins (checkout name to origin URL) and distinct_repositories (callers counted once per origin)."""
    names = sorted({r for repos in ledger["called_files"].values() for r in repos})
    origins = {n: origin_of(workspace / n) for n in names}
    ledger["origins"] = origins
    ledger["summary"]["calling_checkouts"] = len(names)
    ledger["summary"]["distinct_calling_repositories"] = len({o or n for n, o in origins.items()})


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, required=True, help="the Project Meta checkout")
    ap.add_argument("--workspace", type=Path, required=True, help="folder holding the other repositories")
    ap.add_argument("--unit-dir", type=Path, action="append", default=[], help="systemd unit folder (repeatable)")
    ap.add_argument("--bin-dir", type=Path, required=True)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--reuse", type=Path, help="an earlier ledger file: keep its measured lists, only add origins")
    a = ap.parse_args(argv)
    if not (a.repo / ".git").exists():
        print(f"{a.repo} is not a git checkout", file=sys.stderr)
        return 2
    if a.reuse:
        ledger = json.loads(a.reuse.read_text())
        add_origins(ledger, a.workspace)
        if a.out:
            a.out.write_text(json.dumps(ledger, indent=2) + "\n")
        print(json.dumps(ledger["summary"]))
        return 0
    files = called_files(a.repo)
    callers = repo_callers(a.repo, a.workspace, files)
    by_file: dict[str, dict[str, int]] = {}
    for other, found in callers.items():
        for f, n in found.items():
            by_file.setdefault(f, {})[other] = n
    ledger = {
        "repo": str(a.repo), "revision": triage.git(a.repo, "rev-parse", "HEAD")[:9],
        "files_checked": len(files),
        "called_files": {f: by_file[f] for f in sorted(by_file, key=lambda f: -len(by_file[f]))},
        "units": units(a.unit_dir, a.repo.name),
        "commands": commands(a.bin_dir, a.repo.name),
    }
    timers = [u for u in ledger["units"] if u["kind"] == "timer"]
    ledger["summary"] = {
        "called_files": len(ledger["called_files"]),
        "units": len(ledger["units"]), "timers": len(timers),
        "timers_enabled": sum(1 for t in timers if t["enabled"] == "enabled"), "commands": len(ledger["commands"]),
    }
    add_origins(ledger, a.workspace)
    text = json.dumps(ledger, indent=2)
    if a.out:
        a.out.write_text(text + "\n")
    print(json.dumps(ledger["summary"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

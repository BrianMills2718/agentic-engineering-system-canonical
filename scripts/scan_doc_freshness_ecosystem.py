#!/usr/bin/env python3
"""Ecosystem-wide documentation freshness scan.

Derives doc freshness purely from git history (the last commit that touched
the file) rather than a self-declared date header, which drifts stale the
moment nobody remembers to update it (see check_freshness_sla.py, which
relies on a "Last reviewed:" header, and the peer-review finding this script
responds to). Flags repos where the active root instruction file hasn't moved in
a long time relative to how active the repo's code has actually been -- the
strongest actionable signal (code changed, doc didn't), not just raw doc
age in isolation, which conflates "stale" with "dormant" (a repo nobody has
touched in a year with an equally old instruction file is not the problem this
finds; a repo with fresh commits and stagnant instructions is).

Also scores each repo's top-level docs/*.md files (non-recursive -- generated/
and archive/ subdirectories under docs/ are common and would otherwise
dominate results with content not meant to track live code), not just
the active root instruction file. Top-level report fields (doc_last_touch,
drift_days, etc.) retain their names for existing consumers; `primary_doc`
identifies whether they describe AGENTS.md or legacy CLAUDE.md. Per-doc detail is under the
"docs" key, worst-drift first.

Measured-report mode only -- no enforcement. Per the accretion-detector
rollout's own lesson ("we wrote the tool, it never reached other repos")
and the project-workbench-evidence-ladder finding (a policy that's been
advisory since inception, never actually checked at scale): validate the
signal is genuinely useful before promoting it into a gate anywhere.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Copied from Project Meta scripts/scan_doc_freshness_ecosystem.py at f6f0d6f91 (AES consolidation plan, "Before item 11", step 5). The only
# change: the project graph is one person's own data, so the PROJECT_GRAPH environment variable names it, else it is read
# from the private `aes-config` repository, as md_file_cap.py does.
DEFAULT_GRAPH_PATH = Path(os.environ.get("PROJECT_GRAPH") or Path.home() / "code2/aes-config/PROJECT_GRAPH.json").expanduser()


def _git_log_date(repo_path: Path, rel_path: str | None) -> datetime | None:
    """Return the latest author date for a path.

    Use the repository HEAD commit when rel_path is None. Return None when
    Git history cannot be resolved.
    """
    cmd = ["git", "-C", str(repo_path), "log", "-1", "--format=%aI"]
    if rel_path is not None:
        cmd += ["--", rel_path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    line = result.stdout.strip()
    if not line:
        return None
    try:
        return datetime.fromisoformat(line)
    except ValueError:
        return None


def _primary_instruction(path: Path) -> str | None:
    """Choose the active authored root file during the migration."""
    if (path / "CLAUDE.md").is_file():
        return "CLAUDE.md"
    if (path / "AGENTS.md").is_file():
        return "AGENTS.md"
    return None


def _discover_doc_files(path: Path) -> list[str]:
    """Return the root instruction path plus top-level docs/*.md.

    Non-recursive on purpose -- archive/ and generated/ subdirectories under
    docs/ are common and would otherwise dominate the results with content
    that isn't meant to track live code (see Plan #245 failure-mode notes).
    """
    primary = _primary_instruction(path)
    candidates = [primary] if primary else []
    docs_dir = path / "docs"
    if docs_dir.is_dir():
        for entry in sorted(docs_dir.iterdir()):
            if entry.is_file() and entry.suffix == ".md" and entry.name != "README.md":
                candidates.append(f"docs/{entry.name}")
    return [c for c in candidates if (path / c).exists()]


def _score_doc(path: Path, rel_doc: str, repo_touch: datetime, now: datetime) -> dict[str, Any] | None:
    """Compute drift for one doc file against the repo's own last-touch date."""
    doc_touch = _git_log_date(path, rel_doc)
    if doc_touch is None:
        return None
    doc_age_days = (now - doc_touch).days
    repo_age_days = (now - repo_touch).days
    # Drift: how far the doc's last-touch point lags behind the repo's most
    # recent activity. Always >= 0. Large drift + small repo_age_days means
    # "actively worked repo, stagnant doc" -- the actionable case.
    drift_days = doc_age_days - repo_age_days
    return {
        "doc": rel_doc,
        "doc_last_touch": doc_touch.date().isoformat(),
        "doc_age_days": doc_age_days,
        "drift_days": drift_days,
    }


def scan_project(project: dict[str, Any], now: datetime) -> dict[str, Any] | None:
    """Scan one project-graph entry. Returns None if the path doesn't exist locally."""
    raw_path = project.get("path")
    if not raw_path:
        return None
    path = Path(raw_path).expanduser()
    if not path.is_dir():
        return None

    project_id = project.get("id", str(path))
    primary_doc = _primary_instruction(path)
    if primary_doc is None:
        return {"id": project_id, "path": str(path), "status": "no_instruction_file"}
    doc_files = _discover_doc_files(path)

    repo_touch = _git_log_date(path, None)
    if repo_touch is None:
        return {"id": project_id, "path": str(path), "status": "no_git_history"}

    scored = [s for s in (_score_doc(path, doc, repo_touch, now) for doc in doc_files) if s is not None]
    if not scored:
        return {"id": project_id, "path": str(path), "status": "no_git_history"}

    # Repo-level drift describes the active root instruction file. Ranking
    # uses the worst-drifted doc in the repo -- a repo whose instructions are
    # fine but whose docs/API.md is badly stale is
    # still a real finding this tool exists to surface.
    primary = next((s for s in scored if s["doc"] == primary_doc), scored[0])
    docs_sorted = sorted(scored, key=lambda s: s["drift_days"], reverse=True)
    worst = docs_sorted[0]
    repo_age_days = (now - repo_touch).days

    return {
        "id": project_id,
        "path": str(path),
        "primary_doc": primary_doc,
        "doc_last_touch": primary["doc_last_touch"],
        "repo_last_touch": repo_touch.date().isoformat(),
        "doc_age_days": primary["doc_age_days"],
        "repo_age_days": repo_age_days,
        "drift_days": primary["drift_days"],
        "max_drift_days": worst["drift_days"],
        "max_drift_doc": worst["doc"],
        "docs": docs_sorted,
        "status": "ok",
    }


def main() -> int:
    """Scan active Project Graph entries and print a measured freshness report."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--project-graph",
        default=str(DEFAULT_GRAPH_PATH),
        help="Path to PROJECT_GRAPH.json",
    )
    parser.add_argument("--top", type=int, default=20, help="Show top N most doc-drifted repos")
    parser.add_argument("--min-repo-activity-days", type=int, default=30,
                         help="Only surface repos with a commit within this many days (default 30) -- "
                              "excludes dormant repos where a stale doc isn't actionable right now")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of a text report")
    args = parser.parse_args()

    graph_path = Path(args.project_graph)
    if not graph_path.exists():
        print(f"ERROR: project graph not found: {graph_path}", file=sys.stderr)
        return 1

    projects = json.loads(graph_path.read_text(encoding="utf-8"))
    active = [p for p in projects if p.get("status") == "active"]

    now = datetime.now(timezone.utc)
    results = [r for r in (scan_project(p, now) for p in active) if r is not None]

    ok = [r for r in results if r["status"] == "ok"]
    actionable = [r for r in ok if r["repo_age_days"] <= args.min_repo_activity_days]
    actionable.sort(key=lambda r: r["max_drift_days"], reverse=True)

    no_doc = [r for r in results if r["status"] == "no_instruction_file"]
    no_history = [r for r in results if r["status"] == "no_git_history"]

    if args.json:
        print(json.dumps({
            "scanned_active": len(active),
            "resolved_locally": len(results),
            "with_git_history": len(ok),
            "actionable_drift": actionable,
            "no_instruction_file": no_doc,
            "no_claude_md": no_doc,  # Deprecated key for existing digest consumers.
            "no_git_history": no_history,
        }, indent=2))
        return 0

    print(f"Scanned {len(active)} active projects in PROJECT_GRAPH.json.")
    print(f"  {len(results)} resolved to a local path; {len(ok)} have usable git history.")
    print(f"  {len(no_doc)} have neither AGENTS.md nor CLAUDE.md.")
    print(f"  {len(actionable)} are actively worked (commit within {args.min_repo_activity_days}d) -- these are the actionable candidates.\n")

    print(f"Top {args.top} most doc-drifted among actively-worked repos (code moving, doc not):\n")
    for r in actionable[: args.top]:
        primary_doc = r["primary_doc"]
        doc_label = primary_doc if r["max_drift_doc"] == primary_doc else f"{r['max_drift_doc']} (worse than {primary_doc}'s {r['drift_days']}d)"
        print(f"  {r['id']:35s} drift={r['max_drift_days']:5d}d   {doc_label}   repo last touched {r['repo_last_touch']} ({r['repo_age_days']}d ago)")

    if no_doc:
        print(f"\n{len(no_doc)} active, locally resolved projects have no root instruction file:")
        for r in no_doc[:15]:
            print(f"  {r['id']} ({r['path']})")
        if len(no_doc) > 15:
            print(f"  ... and {len(no_doc) - 15} more")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

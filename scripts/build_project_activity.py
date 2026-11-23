#!/usr/bin/env python3
"""Build project_activity.json: where each PROJECT_GRAPH.json project stands right now, read from git.

PROJECT_GRAPH.json records what a project is (identity and lifecycle). This snapshot adds what it is doing:
last commit, commits in the last 30 days, branch, uncommitted files, open pull requests, and which file to
read first for its current state. Everything is read from the checkout or GitHub, never typed by hand, so
rerun it rather than editing the output. Projects whose path is not on this machine are listed as such.

    python3 scripts/build_project_activity.py            # write the snapshot beside the project graph
    python3 scripts/build_project_activity.py --stdout   # print it instead

Exit 0 when the snapshot was built; 1 when the graph cannot be read. A failed GitHub call is recorded in
the output (`open_prs_error`), not hidden.

Copied from Project Meta scripts/build_project_activity.py (retirement plan step 4, Decision 20). The graph is one
person's own data: the PROJECT_GRAPH environment variable names it, else it is read from the private `aes-config`
repository. Settings come from `graph-config.yaml` beside the graph: `owner` (the GitHub account whose repositories are
"personal") and `github_accounts` (a map of every GitHub account the graph must account for to the `gh` wrapper that
may read it). The GitHub-coverage section also reads `workspace_map_extras.yaml` beside the graph (or the
WORKSPACE_MAP_EXTRAS environment variable): its `github_not_projects` and `github_not_project_patterns` say which
repositories are left out on purpose. A missing setting stops the run and names where to set it.
Implements: project-activity-snapshot/settings-come-from-config
Implements: project-activity-snapshot/last-commit-per-checkout
"""

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import re

import yaml

GRAPH_DEFAULT = os.environ.get("PROJECT_GRAPH") or os.path.expanduser("~/code2/aes-config/PROJECT_GRAPH.json")
REPO_FIELDS = "name,nameWithOwner,description,isArchived,isFork,isPrivate,pushedAt"


def config_path(graph_path=None):
    return Path(os.path.expanduser(graph_path or GRAPH_DEFAULT)).parent / "graph-config.yaml"


def load_config(graph_path=None):
    """The settings file beside the graph, or {} when it is absent or empty."""
    try:
        return yaml.safe_load(config_path(graph_path).read_text(encoding="utf-8")) or {}
    except OSError:
        return {}


def github_accounts(graph_path=None):
    """{GitHub account: gh wrapper that may read it}; no value is a loud stop."""
    accounts = load_config(graph_path).get("github_accounts")
    if not isinstance(accounts, dict) or not accounts:
        raise SystemExit(f"build_project_activity: no github_accounts named: put a map of account to gh wrapper under "
                         f"`github_accounts:` in {config_path(graph_path)}")
    return accounts


def github_owner(graph_path=None):
    named = os.environ.get("PROJECT_GRAPH_OWNER") or load_config(graph_path).get("owner")
    if not named:
        raise SystemExit(f"build_project_activity: no owner named: set PROJECT_GRAPH_OWNER or put `owner:` in {config_path(graph_path)}")
    return named


def list_repo_details(accounts):
    """Every repository of every account, with its GitHub metadata. Raises RuntimeError when any account cannot
    answer: a partial list would make missing repositories look covered."""
    repos = []
    for owner, wrapper in accounts.items():
        try:
            out = subprocess.run([wrapper, "repo", "list", owner, "--limit", "2000", "--json", REPO_FIELDS],
                                 capture_output=True, text=True, timeout=120)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RuntimeError(f"{wrapper} repo list {owner} failed: {exc}") from None
        if out.returncode != 0:
            raise RuntimeError(f"{wrapper} repo list {owner} exit {out.returncode}: {out.stderr.strip()[:200]}")
        repos += json.loads(out.stdout)
    return repos

# First file that exists is where a reader starts; the state file says where the project stands.
ENTRY_DOCS = ("docs/index.md", "README.md", "AGENTS.md")
STATE_DOCS = ("STATE.md", "STATUS.md", "STATE_OF_PROJECT.md", "docs/STATE.md", "docs/STATUS.md",
              "ROADMAP.md", "docs/ROADMAP.md", "PLAN.md", "docs/PLAN.md", "docs/plans/INDEX.md")
WINDOW_DAYS = 30


GIT_TIMEOUT = 120  # seconds for one git call; a stuck checkout reads as empty instead of stalling the snapshot


def git(path, *args):
    try:
        out = subprocess.run(["git", "-C", path, *args], capture_output=True, text=True, timeout=GIT_TIMEOUT)
    except subprocess.TimeoutExpired:
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


def open_prs_by_repo(accounts):
    """One search call per GitHub account for its open pull requests: {owner/repo (lowercase): count}."""
    counts = {}
    for owner, wrapper in accounts.items():
        cmd = [wrapper, "search", "prs", "--owner", owner, "--state", "open", "--limit", "1000", "--json", "repository"]
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if out.returncode != 0:
            return None, f"{wrapper} search prs --owner {owner} exit {out.returncode}: {out.stderr.strip()[:200]}"
        for pr in json.loads(out.stdout or "[]"):
            name = (pr.get("repository") or {}).get("nameWithOwner", "").lower()
            counts[name] = counts.get(name, 0) + 1
    return counts, None


def github_facts(accounts):
    """{owner/repo (lowercase): GitHub metadata}, so a repository not cloned here still shows its last push."""
    try:
        return {r["nameWithOwner"].lower(): r for r in list_repo_details(accounts)}, None
    except RuntimeError as exc:
        return {}, str(exc)


def extras_path(graph_path=None):
    return Path(os.environ.get("WORKSPACE_MAP_EXTRAS") or config_path(graph_path).parent / "workspace_map_extras.yaml")


def github_coverage(records, facts, accounts, owner, extras):
    """Account for every GitHub repository: it has a record, or a stated reason to have none, or it is a gap."""
    reasons = {str(k).lower(): v for k, v in (extras.get("github_not_projects") or {}).items()}
    patterns = [(re.compile(p["pattern"], re.I), p["reason"]) for p in (extras.get("github_not_project_patterns") or [])]
    full = {str(r.get("github_repo") or "").lower() for r in records}
    bare = {str(r.get("github_repo") or "").split("/")[-1].lower() for r in records} | {str(r.get("id") or "").lower() for r in records}
    recorded, left_out, gaps = 0, [], []
    for key, fact in sorted(facts.items()):
        account, name = fact["nameWithOwner"].split("/")
        personal = account == owner
        reason = reasons.get(key) or (reasons.get(name.lower()) if personal else None)
        reason = reason or next((why for rx, why in patterns if rx.search(name)), None)
        if key in full:
            recorded += 1
        elif personal and name.lower() in bare:
            left_out.append({"repo": fact["nameWithOwner"], "reason": "personal copy of a repository recorded under another account"})
        elif reason:
            left_out.append({"repo": fact["nameWithOwner"], "reason": reason})
        elif fact.get("isArchived"):
            left_out.append({"repo": fact["nameWithOwner"], "reason": "archived on GitHub, never registered"})
        else:
            gaps.append(fact["nameWithOwner"])
    return {"github_repos": len(facts), "recorded": recorded, "left_out": left_out, "gaps": gaps, "accounts": sorted(accounts)}


def first_existing(path, candidates):
    for rel in candidates:
        if os.path.isfile(os.path.join(path, rel)):
            return rel
    return None


def activity(record, now, prs, accounts, facts=None):
    raw = record.get("path")
    path = os.path.expanduser(raw) if raw else None
    row = {"id": record["id"]}
    gh = (record.get("github_repo") or "").lower()
    if prs is not None and gh.split("/")[0] in {a.lower() for a in accounts}:
        row["open_prs"] = prs.get(gh, 0)
    fact = (facts or {}).get(gh)
    if fact:
        row["last_push"] = (fact.get("pushedAt") or "")[:10] or None
        row["github_archived"] = bool(fact.get("isArchived"))
    if not path or not os.path.isdir(path):
        row["on_this_machine"] = False
        return row
    row["on_this_machine"] = True
    if not git(path, "rev-parse", "--git-dir"):
        row["git"] = False
        return row
    last = git(path, "log", "-1", "--format=%ct%x00%cs%x00%s")
    if last:
        ts, day, subject = last.split("\x00", 2)
        row.update(last_commit=day, last_commit_subject=subject[:160], idle_days=int((now - int(ts)) // 86400))
    since = time.strftime("%Y-%m-%d", time.localtime(now - WINDOW_DAYS * 86400))
    row["commits_30d"] = int(git(path, "rev-list", "--count", f"--since={since}", "HEAD") or 0)
    row["branch"] = git(path, "branch", "--show-current") or None
    row["uncommitted_files"] = len([l for l in git(path, "status", "--porcelain").splitlines() if l.strip()])
    entry, state = first_existing(path, ENTRY_DOCS), first_existing(path, STATE_DOCS)
    if entry:
        row["entry_doc"] = entry
    if state:
        row["state_doc"] = state
        row["state_doc_updated"] = git(path, "log", "-1", "--format=%cs", "--", state) or None
    return row


def build(graph_path):
    records = json.loads(Path(graph_path).read_text(encoding="utf-8"))
    now = time.time()
    accounts, owner = github_accounts(graph_path), github_owner(graph_path)
    prs, pr_error = open_prs_by_repo(accounts)
    facts, facts_error = github_facts(accounts)
    with ThreadPoolExecutor(max_workers=12) as pool:  # git calls are I/O-bound; serial took ~110 s for 264 checkouts
        rows = list(pool.map(lambda r: activity(r, now, prs, accounts, facts), records))
    here = [r for r in rows if r.get("on_this_machine")]
    out = {
        "schema": "project-activity/v1",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(now)),
        "generated_on": os.uname().nodename,
        "source": "scripts/build_project_activity.py over PROJECT_GRAPH.json",
        "summary": {
            "projects": len(rows),
            "on_this_machine": len(here),
            "committed_last_30d": sum(1 for r in here if r.get("commits_30d")),
            "with_uncommitted_files": sum(1 for r in here if r.get("uncommitted_files")),
            "with_state_doc": sum(1 for r in here if r.get("state_doc")),
            "open_prs": sum(r.get("open_prs", 0) for r in rows),
        },
        "projects": rows,
    }
    if pr_error:
        out["open_prs_error"] = pr_error
    if facts_error:
        out["github_facts_error"] = facts_error
    else:
        try:
            extras = yaml.safe_load(extras_path(graph_path).read_text(encoding="utf-8")) or {}
        except OSError as exc:
            out["github_coverage_error"] = f"cannot read {extras_path(graph_path)}: {exc}"
        else:
            out["github_coverage"] = github_coverage(records, facts, accounts, owner, extras)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--project-graph", default=GRAPH_DEFAULT)
    ap.add_argument("--output", help="where to write (default: project_activity.json beside the project graph)")
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args()
    try:
        out = build(args.project_graph)
    except (OSError, ValueError) as exc:
        print(f"build_project_activity: cannot read graph: {exc}", file=sys.stderr)
        return 1
    output = args.output or str(Path(os.path.expanduser(args.project_graph)).parent / "project_activity.json")
    text = json.dumps(out, indent=1, ensure_ascii=False) + "\n"
    if args.stdout:
        sys.stdout.write(text)
    else:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text(text, encoding="utf-8")
        print(f"build_project_activity: wrote {output}")
    s = out["summary"]
    print(f"build_project_activity: {s['projects']} projects, {s['on_this_machine']} on this machine, "
          f"{s['committed_last_30d']} committed in {WINDOW_DAYS} days, {s['open_prs']} open PRs"
          f"{'; PR lookup FAILED: ' + out['open_prs_error'] if 'open_prs_error' in out else ''}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

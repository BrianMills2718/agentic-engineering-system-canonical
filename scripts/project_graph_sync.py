#!/usr/bin/env python3
"""Register every GitHub repository that PROJECT_GRAPH.json does not yet account for.

The daily workspace check names such repositories, but naming them did not get them recorded: six sat in its
report for days. This writes the record instead. A new record says only what is known without a judgement:
where it lives, its GitHub description or README title, and status `unreviewed` until a checkout exists here
(then `active`). `area-unreviewed` in utility_tags marks a record whose area and purpose nobody has read yet.

A repository that should have no record gets a reason in workspace_map_extras.yaml instead
(github_not_projects, Owner/name for an account other than the owner's).

    python3 scripts/project_graph_sync.py           # report what is missing; exit 0
    python3 scripts/project_graph_sync.py --write   # add the records; exit 0
Exit 1 when GitHub cannot be read or a would-be id collides: nothing is written. Exit 2 when a setting is missing.

Copied from Project Meta scripts/project_graph_sync.py (retirement plan step 4, Decision 20). The graph is one
person's own data: the PROJECT_GRAPH environment variable (or --graph) names it, else it is read from the private
`aes-config` repository; workspace_map_extras.yaml sits beside it. The values the old script held in code come
from `graph-config.yaml` beside the graph: `owner`, `github_accounts`, `default_home` (where a checkout of a
repository lives, `{name}` filled in), `record_source` (`owner:` and `other:`, the `source` of a new record), and
`organizations` (per GitHub account: `home`, `id_prefix`, `tags`, `utility_tags`). A missing setting stops the run
and names where to set it.
Implements: project-graph-sync/settings-come-from-config
Implements: project-graph-sync/missing-repositories-get-a-record
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import workspace_map as wm  # noqa: E402

NOT_REVIEWED = "purpose not yet reviewed"


def settings():
    """The record-making settings from graph-config.yaml; a missing one is a loud stop (wm.ConfigMissing)."""
    cfg = wm.graph_config()
    for key, form in (("default_home", "a path with {name}, e.g. ~/code2/{name}"),
                      ("record_source", "a map with `owner:` and `other:`")):
        if not cfg.get(key):
            raise wm.ConfigMissing(f"project_graph_sync: no `{key}:` ({form}) in {wm.config_path()}")
    if not {"owner", "other"} <= set(cfg["record_source"]):
        raise wm.ConfigMissing(f"project_graph_sync: `record_source:` needs `owner:` and `other:` in {wm.config_path()}")
    return {"owner": wm.github_owner(), "default_home": cfg["default_home"], "record_source": cfg["record_source"],
            "organizations": cfg.get("organizations") or {}}


def readme_title(full_name, wrapper):
    """First heading or line of the repository's README, or None when it has none we can read."""
    out = subprocess.run([wrapper, "api", f"repos/{full_name}/readme", "-q", ".content"],
                         capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        return None
    text = base64.b64decode(out.stdout).decode("utf-8", "replace")
    for line in text.splitlines():
        line = re.sub(r"^#+\s*", "", line).strip()
        if line and not line.startswith(("<", "[", "!")):
            return line[:160]
    return None


def is_checkout_of(path, full_name):
    """True when `path` is a git checkout whose origin is this repository. A folder of the same name is not enough:
    Inside-Success/company-planning's would-be folder holds BrianMills2718/company-planning."""
    if not os.path.isdir(path):
        return False
    out = subprocess.run(["git", "-C", path, "remote", "get-url", "origin"], capture_output=True, text=True)
    url = re.sub(r"\.git$", "", out.stdout.strip())
    return out.returncode == 0 and url.lower().endswith(("/" + full_name.lower(), ":" + full_name.lower()))


def new_record(repo, taken, today, cfg, title=None):
    """The record for one GitHub repository. `repo` is a `gh repo list` row; `taken` the lowercase ids in use;
    `cfg` what settings() returns."""
    owner, name = repo["nameWithOwner"].split("/")
    org = cfg["organizations"].get(owner) or {}
    home = org.get("home") or cfg["default_home"]
    record_id = org.get("id_prefix", "") + name
    if record_id.lower() in taken:
        record_id = f"{owner.lower()}-{name}"
    if record_id.lower() in taken:
        raise ValueError(f"no free id for {repo['nameWithOwner']}: {record_id} is taken")
    path = home.format(name=name)
    cloned = is_checkout_of(path, repo["nameWithOwner"])
    if not cloned and os.path.exists(path):  # the folder belongs to another repository of the same name
        path = home.format(name=f"{owner}-{name}")
    status = "archived" if repo.get("isArchived") else ("active" if cloned else "unreviewed")
    description = (repo.get("description") or "").strip()
    one_liner = description or (f"{title} (README title; {NOT_REVIEWED})" if title else f"No GitHub description or README; {NOT_REVIEWED}")
    source = cfg["record_source"]["owner" if owner == cfg["owner"] else "other"]
    return {
        "id": record_id, "record_kind": "repository", "name": name, "path": path,
        "github_repo": repo["nameWithOwner"], "status": status, "one_liner": one_liner,
        "domains": [], "tech": [], "capabilities": [], "depends_on": [], "superseded_by": None, "supersedes": [],
        "tags": [f"github-coverage-{today}"] + list(org.get("tags") or []),
        "source": source,
        "portfolio_area": "application", "organization_status": "do-not-move",
        "utility_tags": ["area:application", f"status:{status}", "github-linked", "area-unreviewed"]
        + list(org.get("utility_tags") or []),
        "provenance": f"project_graph_sync {today} (last push {(repo.get('pushedAt') or '')[:10]}); local clone: {'yes' if cloned else 'no'}",
    }


def missing_repos(graph, extras, repos, owner):
    """The rows of `repos` that have neither a graph record nor a stated reason."""
    names = {(r["name"] if r["nameWithOwner"].split("/")[0] == owner else r["nameWithOwner"]): r
             for r in repos if not r.get("isArchived")}
    return [names[n] for n in wm.uncovered_repos(extras, graph, list(names))]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--write", action="store_true", help="add the missing records to PROJECT_GRAPH.json")
    ap.add_argument("--graph", type=Path, help="the graph (default: $PROJECT_GRAPH, else ~/code2/aes-config/PROJECT_GRAPH.json)")
    args = ap.parse_args(argv)
    if args.graph:
        os.environ["PROJECT_GRAPH"] = str(args.graph)  # settings and extras are read beside it
    graph_file = Path(wm.graph_path())
    try:
        cfg = settings()
        graph = wm.graph_records()
        extras = wm.load_extras()
        accounts = wm.github_accounts()
    except wm.ConfigMissing as exc:
        print(f"CRASH: {exc}", file=sys.stderr)
        return 2
    try:
        missing = missing_repos(graph, extras, wm.list_repo_details(), cfg["owner"])
    except RuntimeError as exc:
        print(f"GITHUB NOT READ, nothing changed: {exc}", file=sys.stderr)
        return 1
    today, added = time.strftime("%Y-%m-%d"), []
    taken = {str(r["id"]).lower() for r in graph}
    try:
        for repo in missing:
            wrapper = accounts[repo["nameWithOwner"].split("/")[0]]
            title = None if repo.get("description") else readme_title(repo["nameWithOwner"], wrapper)
            record = new_record(repo, taken, today, cfg, title)
            taken.add(record["id"].lower())
            added.append(record)
    except ValueError as exc:
        print(f"ID COLLISION, nothing changed: {exc}", file=sys.stderr)
        return 1
    for record in added:
        print(f"{'add' if args.write else 'missing'}: {record['id']} ({record['github_repo']}, {record['status']})")
    if args.write and added:
        graph_file.write_text(json.dumps(graph + added, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(added)} of {len(graph) + len(added)} records {'added' if args.write else 'missing'}; exit 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

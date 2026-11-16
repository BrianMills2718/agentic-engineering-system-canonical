#!/usr/bin/env python3
"""workspace_map: the clutter check that keeps ~/code, ~/projects and ~/code2 explained.

  workspace_map.py --check [--report P]   print clutter findings; exit 1 if any need action; write report P

Implements: workspace-map-check/settings-come-from-config
Implements: workspace-map-check/dependency-scan-skip-is-visible

Sources of truth (this script invents nothing):
  * PROJECT_GRAPH.json           purpose (one_liner), status, origin of every registered project
  * workspace_map_extras.yaml    purpose + kind of everything the graph does not describe, the
                                 placement rules, and the intentional same-remote pairs
A top-level entry in neither is reported UNKNOWN. That is the whole mechanism: new clutter cannot be
added silently, because the next check names it.

Both files are one person's own data. The graph is named by the PROJECT_GRAPH environment variable, else
it is read from the private `aes-config` repository (~/code2/aes-config/PROJECT_GRAPH.json), as
md_file_cap.py does. The extras file sits beside the graph (WORKSPACE_MAP_EXTRAS overrides). The GitHub
owner and the accounts the GitHub coverage check reads come from `graph-config.yaml` beside the graph
(keys `owner` and `github_accounts`; PROJECT_GRAPH_OWNER overrides the owner).

Ported from Project Meta `scripts/workspace_map.py` (retirement plan step 6). Left out on purpose: the
coordination-claims reader and the repository-authority snapshot check (the claims system is retired),
and `--write-map` with its WORKSPACE_MAP.md staleness finding (the derived page was dropped, Decision 20).
"""
import argparse, collections, glob, os, re, subprocess, sys, time
import json

try:
    import yaml
except ImportError:  # fail loudly: the scheduled run must not pretend to have checked
    sys.exit("workspace_map.py needs PyYAML (python3 -c 'import yaml')")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)  # repository root (this file lives in scripts/)


class ConfigMissing(RuntimeError):
    """A settings file or value the check needs is missing. A crash, not a finding (exit 2, never 1)."""


def graph_path():
    return os.path.expanduser(os.environ.get("PROJECT_GRAPH") or "~/code2/aes-config/PROJECT_GRAPH.json")


def config_path():
    return os.path.join(os.path.dirname(graph_path()), "graph-config.yaml")


def extras_path():
    return os.path.expanduser(os.environ.get("WORKSPACE_MAP_EXTRAS") or os.path.join(os.path.dirname(graph_path()), "workspace_map_extras.yaml"))


def _read(path, what, env):
    if not os.path.isfile(path):
        raise ConfigMissing(f"workspace_map: {what} not found at {path}: put it there, or name it with {env}")
    return open(path).read()


def graph_records():
    return json.loads(_read(graph_path(), "project graph", "PROJECT_GRAPH"))


def graph_config():
    return yaml.safe_load(_read(config_path(), "graph settings (graph-config.yaml)", "PROJECT_GRAPH")) or {}


def github_owner():
    named = os.environ.get("PROJECT_GRAPH_OWNER")
    if named:
        return named
    owner = graph_config().get("owner")
    if not owner:
        raise ConfigMissing(f"workspace_map: no owner named: set PROJECT_GRAPH_OWNER or put `owner:` in {config_path()}")
    return owner


def github_accounts():
    """{account: gh wrapper} for every GitHub account whose repositories the graph must account for."""
    accounts = graph_config().get("github_accounts")
    if not accounts:
        raise ConfigMissing(f"workspace_map: no GitHub accounts named: put a `github_accounts:` map (account: gh wrapper) in {config_path()}")
    return accounts


ROOT = os.path.expanduser(os.environ.get("CODE_ROOT", "~/code"))
PROJECTS = os.path.expanduser(os.environ.get("PROJECTS_ROOT", "~/projects"))
CODE2 = os.path.expanduser(os.environ.get("CODE2_ROOT", "~/code2"))
LIVE_HOURS = float(os.environ.get("LIVE_HOURS", "3"))       # dirty + touched within this = a live agent's work
STALE_WT_DAYS = float(os.environ.get("STALE_WT_DAYS", "7"))  # clean worktree idle this long = stale

CLUTTER_WORDS = re.compile(r"(^|[-_.])(scratch|tmp|temp|trash|backup|bak|corrupt|restore|old|copy)([-_.]|$)", re.I)
# random suffixes: "name.AbC123", "name-1790589453" (epoch), "name-3ef5e4c8" (hex with a letter). Dates (20260910) and dot-dirs are fine.
RANDOM_SUFFIX = re.compile(r"(^[^.].*\.[A-Za-z0-9]{5,8}$|-\d{10,}$|-(?=[0-9]*[a-f])[0-9a-f]{8,}$)")
DATA_DIR_NAMES = {"var", "data", "results", "runs", "private_runs", "outputs", "exports", "corpus", "raw"}


def sh(*args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True).stdout


def load_graph():
    recs = graph_records()
    idx = {}
    for r in recs:
        for key in (os.path.basename((r.get("path") or "").rstrip("/")), r.get("workspace_slug"), r.get("id")):
            if key:
                idx.setdefault(key, r)
    return idx


def load_extras():
    return yaml.safe_load(_read(extras_path(), "workspace map extras (workspace_map_extras.yaml)", "WORKSPACE_MAP_EXTRAS"))


def is_repo(p):
    return os.path.isdir(os.path.join(p, ".git")) and not os.path.islink(p)


def classify():
    graph, ex = load_graph(), load_extras()
    entries = ex.get("entries") or {}
    inferred = set(ex.get("inferred_purpose") or [])
    rows = []
    for name in sorted(os.listdir(ROOT)):
        p = os.path.join(ROOT, name)
        mega = name.endswith("-mega")
        if name in entries:
            e = entries[name]
            rows.append(dict(name=name, src="registry", kind=e["kind"], mut=e.get("mutability", "live"),
                             purpose=e["purpose"], inferred=name in inferred, path=p))
        elif name in graph:
            g = graph[name]
            kind = "finder" if mega else ("symlink" if os.path.islink(p) else "repo")
            rows.append(dict(name=name, src="graph", kind=kind, mut="read-only" if mega else "live",
                             purpose=(g.get("one_liner") or g.get("name") or "").strip(),
                             inferred=False, path=p, status=g.get("status"), origin=g.get("source")))
        else:
            rows.append(dict(name=name, src="UNKNOWN", kind="UNKNOWN", mut="?", purpose="", inferred=False, path=p))
    return rows, ex


def classify_projects(ex):
    """Top-level entries of ~/projects. A symlink to a checkout under ~/code (or another ~/projects path that exists) is an alias and
    needs no registry line; everything else must be in extras.projects_entries or it is UNKNOWN."""
    reg = ex.get("projects_entries") or {}
    rows = []
    if not os.path.isdir(PROJECTS):
        return rows
    for name in sorted(os.listdir(PROJECTS)):
        p = os.path.join(PROJECTS, name)
        if name in reg:
            e = reg[name]
            rows.append(dict(name=name, src="registry", kind=e["kind"], mut=e.get("mutability", "live"), purpose=e["purpose"], path=p))
        elif os.path.islink(p):
            if os.path.exists(p):
                rows.append(dict(name=name, src="alias", kind="alias", mut="read-only",
                                 purpose="alias of " + os.path.realpath(p).replace(os.path.expanduser("~"), "~"), path=p))
            else:
                rows.append(dict(name=name, src="DANGLING", kind="DANGLING", mut="?", purpose="symlink to " + os.readlink(p), path=p))
        else:
            rows.append(dict(name=name, src="UNKNOWN", kind="UNKNOWN", mut="?", purpose="", path=p))
    return rows


# ---------------- checks ----------------
def norm_remote(u):
    u = u.strip().removesuffix(".git")
    u = re.sub(r"^git@[^:]*:", "https://x/", u)
    return re.sub(r"^https?://[^/]*/", "https://x/", u).lower()


def unregistered_code2_repos(rows, ex, root=None):
    """Repos at the top of ~/code2 that neither a ~/code entry nor a graph record path resolves to.
    Repos live in ~/code2 since 2026-10-13, and one created there without a ~/code symlink was invisible to this check."""
    root = root or CODE2
    if not os.path.isdir(root):
        return []
    known = {os.path.realpath(r["path"]) for r in rows}
    for rec in graph_records():
        if rec.get("path"):
            known.add(os.path.realpath(os.path.expanduser(rec["path"])))
    entries = ex.get("entries") or {}
    return [n for n in sorted(os.listdir(root))
            if is_repo(os.path.join(root, n)) and n not in entries and os.path.realpath(os.path.join(root, n)) not in known]


def undeclared_dependency_links(scan=None):
    """Return "consumer -> provider (evidence)" for uses missing from PROJECT_GRAPH.json depends_on.

    A use is an import, a path into the provider's folder, or a run of its command.

    scan defaults to check_capability_consumption.run_scan (about a minute over every local repo)."""
    if scan is None:
        sys.path.insert(0, os.path.join(REPO, "scripts"))
        import check_capability_consumption as consumption
        scan = consumption.run_scan
    return [f"{x['consumer']} -> {x['provider']} ({', '.join(x.get('via') or x.get('packages', []))})"
            for x in scan().findings if x["kind"] == "undeclared_project_dependency"]


DEPENDENCY_TITLE = ("repo uses another repo (import, path or command) not in its PROJECT_GRAPH.json depends_on "
                    "(run scripts/check_capability_consumption.py --write and commit)")
DEPENDENCY_SKIPPED = "INFO dependency scan not ported yet (retirement plan step 4)"


def dependency_findings(scan=None):
    """The depends_on finding, or a visible INFO line when the scanner is not in this repository yet.

    check_capability_consumption.py has not been ported from Project Meta (retirement plan step 4). Until it is,
    the finding is skipped and the report says so; an INFO line is not actionable, so it opens no concern."""
    try:
        links = undeclared_dependency_links(scan)
    except ImportError as exc:
        return {DEPENDENCY_SKIPPED: [f"scripts/check_capability_consumption.py is not importable ({exc}); the depends_on finding is skipped"]}
    return {DEPENDENCY_TITLE: links} if links else {}


def check(rows, ex, dependency_scan=None):
    f = collections.defaultdict(list)
    now = time.time()
    accepted = ex.get("accepted_clutter_names") or {}
    today = time.strftime("%Y-%m-%d")
    for r in rows:
        if r["src"] == "UNKNOWN":
            f["UNKNOWN top-level entry (add to PROJECT_GRAPH.json or workspace_map_extras.yaml, or move it)"].append(r["name"])
        n = r["name"]
        # graph-registered repos are deliberate by definition; the name check is for entries nobody registered as a repo
        if n in accepted and str(accepted[n].get("until", "")) < today:
            f["accepted-clutter exception EXPIRED (re-decide: resolve it or renew with a new reason)"].append(f"{n}: {accepted[n].get('reason')} (expired {accepted[n].get('until')})")
        elif n in accepted:
            continue  # deliberate, reviewed, and not yet due
        if (CLUTTER_WORDS.search(n) or RANDOM_SUFFIX.search(n)) and r["src"] != "graph" and r["kind"] not in ("scratch", "archive", "shim", "alias", "tool-state") and not n.endswith("-mega"):
            f["WARN clutter-looking name (backup/scratch/restore/random suffix): resolve or rename"].append(n)
        if os.path.islink(r["path"]) and not os.path.exists(r["path"]):
            f["dangling symlink"].append(n)
    for r in classify_projects(ex):
        if r["src"] == "UNKNOWN":
            f["UNKNOWN ~/projects entry (add to extras.projects_entries or move it)"].append(r["name"])
        elif r["src"] == "DANGLING":
            f["dangling symlink in ~/projects"].append(f"{r['name']} -> {r['purpose']}")
    for name in unregistered_code2_repos(rows, ex):
        f["~/code2 repo with no PROJECT_GRAPH.json record (add one, or an extras entry)"].append(name)
    for k, v in dependency_findings(dependency_scan).items():
        f[k] += v
    repos =[r for r in rows if os.path.isdir(os.path.join(r["path"], ".git")) and not os.path.islink(r["path"])]
    procs = set()  # cwd of every running process: a repo with one inside it is in use (measured from here, never from inside a target)
    for pid in os.listdir("/proc"):
        if pid.isdigit():
            try:
                procs.add(os.readlink(f"/proc/{pid}/cwd"))
            except OSError:
                pass
    # duplicate clones
    by_remote = collections.defaultdict(list)
    for r in repos:
        u = sh("git", "-C", r["path"], "remote", "get-url", "origin").strip()
        if u:
            by_remote[norm_remote(u)].append(r["name"])
    ok_pairs = [set(p) for p in ex.get("intentional_same_remote", [])]
    for u, names in by_remote.items():
        if len(names) > 1 and not any(set(names) <= p for p in ok_pairs):
            f["duplicate clones of one remote (confirm intent in extras.intentional_same_remote or retire one)"].append(f"{', '.join(names)}  ({u})")
    # dirty repos and stale worktrees
    for r in repos:
        if r["name"].endswith("-mega"):
            continue  # sync automation owns the finders
        st = sh("git", "-C", r["path"], "status", "--porcelain").splitlines()
        if st:
            newest = 0
            for line in st:
                try:
                    newest = max(newest, os.stat(os.path.join(r["path"], line[3:].strip().strip('"'))).st_mtime)
                except OSError:
                    pass
            age_h = (now - newest) / 3600 if newest else 9999
            in_use = any(c == r["path"] or c.startswith(r["path"] + "/") for c in procs)
            if age_h >= LIVE_HOURS and not in_use:
                f[f"dirty repo with no recent writer (>{LIVE_HOURS:g}h): commit, stash to a worktree, or reset"].append(f"{r['name']} ({len(st)} files, newest change {age_h:.0f}h ago)")
        wt = sh("git", "-C", r["path"], "worktree", "list", "--porcelain").split("\n\n")[1:]
        for blk in wt:
            m = re.search(r"^worktree (.+)$", blk, re.M)
            if not m:
                continue
            p = m.group(1)
            if not os.path.isdir(p):
                f["stale worktree: directory missing (git worktree prune)"].append(f"{r['name']}: {p}")
                continue
            if "locked" in blk:
                continue  # an agent session holds it
            if sh("git", "-C", p, "status", "--porcelain").strip():
                continue
            gd = sh("git", "-C", p, "rev-parse", "--absolute-git-dir").strip()
            try:
                idle_d = (now - max(os.stat(os.path.join(gd, "index")).st_mtime, float(sh("git", "-C", p, "log", "-1", "--format=%ct").strip() or 0))) / 86400
            except OSError:
                idle_d = 9999
            if idle_d >= STALE_WT_DAYS:
                f[f"stale worktree: clean and idle >= {STALE_WT_DAYS:g} days (remove via session-close)"].append(f"{r['name']}: {p} ({idle_d:.0f}d)")
    # ~/archive must be fully explained too (archive_map.py owns the registry and the only-copy computation)
    try:
        if HERE not in sys.path:
            sys.path.insert(0, HERE)
        import archive_map
        for k, v in archive_map.check().items():
            f[k] += v
    except Exception as e:  # fail loudly: an archive check that cannot run must not look like a clean one
        f["archive check could not run"].append(f"{type(e).__name__}: {e}")
    # commits that exist only on this machine (a lost disk loses them). Verified against the REAL remote with ls-remote, because a repo
    # with a single-branch fetch refspec never learns about a branch it just pushed. Skipped: repos a live agent owns (a process
    # in the folder, or a commit/change within LIVE_HOURS) and third-party clones (graph source=external-reference).
    ext = {r["name"] for r in rows if r["src"] == "graph" and (load_graph().get(r["name"]) or {}).get("source") == "external-reference"}
    for r in repos:
        n = r["name"]
        if n.endswith("-mega") or n in ext:
            continue
        has_remote = bool(sh("git", "-C", r["path"], "remote", "get-url", "origin").strip())
        lc = sh("git", "-C", r["path"], "log", "-1", "--format=%ct").strip()
        recent = lc and (now - int(lc)) / 3600 < LIVE_HOURS
        live = recent or any(c == r["path"] or c.startswith(r["path"] + "/") for c in procs)
        if not has_remote:
            if sh("git", "-C", r["path"], "rev-parse", "--verify", "-q", "HEAD").strip():
                f["repo has commits but NO remote (create one, or archive it): the history exists only on this disk"].append(n)
            continue
        local_only = []
        for br in sh("git", "-C", r["path"], "for-each-ref", "--format=%(refname:short)", "refs/heads").split():
            if sh("git", "-C", r["path"], "rev-list", "--count", br, "--not", "--remotes").strip() not in ("", "0"):
                local_only.append(br)
        if not local_only or live:
            continue
        url = sh("git", "-C", r["path"], "remote", "get-url", "origin").strip()
        cmd = ["git", "-C", r["path"]]
        cmd += credential_override(url)
        rr = subprocess.run(cmd + ["ls-remote", "--heads", "origin"], capture_output=True, text=True)
        if rr.returncode != 0:
            f["could not verify pushes against the remote (ls-remote failed)"].append(f"{n}: {rr.stderr.strip()[:80]}")
            continue
        remote_shas = {l.split()[0] for l in rr.stdout.splitlines() if l.strip()}
        unp = [b for b in local_only if sh("git", "-C", r["path"], "rev-parse", b).strip() not in remote_shas]
        if unp:
            f["repo has local-only commits with no live owner (push a wip branch: git push origin <sha>:refs/heads/wip/<branch>)"].append(f"{n}: {', '.join(unp[:4])}{' ...' if len(unp) > 4 else ''}")
    # a systemd user unit whose WorkingDirectory, program, or any path in its command ARGUMENTS no longer exists cannot start: it fails
    # (status 200 CHDIR / 203 EXEC / argparse "directory is unavailable") until someone notices. Deleting a "stray" worktree, clone or virtualenv
    # that a unit runs from is exactly how this happens, so test every absolute path on the command lines directly. Environment/PATH lists and
    # log redirects are skipped (colon lists and files created at runtime are not dependencies).
    unit_dir = os.path.expanduser("~/.config/systemd/user")
    if os.path.isdir(unit_dir):
        home = os.path.expanduser("~")
        for uf in sorted(glob.glob(os.path.join(unit_dir, "*.service"))):
            # a deliberately disabled unit is not a failure waiting to happen (enabled/static/linked/... all still run or can be triggered)
            st = subprocess.run(["systemctl", "--user", "is-enabled", os.path.basename(uf)], capture_output=True, text=True).stdout.strip()
            if st in ("disabled", "masked"):
                continue
            try:
                body = open(uf).read()
            except OSError:
                continue
            seen = set()
            for line in body.splitlines():
                m = re.match(r"\s*(WorkingDirectory|ExecStart|ExecStartPre|ExecStartPost|ExecStop)\s*=\s*(.*)", line)
                if not m:
                    continue
                for tok in m.group(2).split():
                    tok = tok.lstrip("-@+!").split("=", 1)[-1] if tok.startswith("--") else tok.lstrip("-@+!")
                    tok = tok.replace("%h", home).replace("$HOME", home)
                    if tok.startswith("~"):
                        tok = home + tok[1:]
                    if not tok.startswith(home + "/") or any(c in tok for c in "*%{}$:;"):
                        continue
                    if not os.path.exists(tok) and tok not in seen:
                        seen.add(tok)
                        f["systemd user unit depends on a path that does not exist (restore it, or fix the unit)"].append(f"{os.path.basename(uf)}: {m.group(1)} -> {tok}")
    # secret-looking files must not live under ~/code (they belong in ~/.secrets)
    secret_names = ["credentials.json", "token.json", "msal_token_cache.json", "*_token_cache.json", "id_rsa", "id_ed25519", "*.pem"]
    name_expr = []
    for n in secret_names:
        name_expr += ["-name", n, "-o"]
    found = sh("find", ROOT, "-maxdepth", "6", "(", "-name", ".git", "-o", "-name", "node_modules", "-o", "-name", ".venv", "-o", "-name", "*-mega", "-o", "-name", "worktrees", ")", "-prune",
               "-o", "(", *name_expr[:-1], ")", "-type", "f", "-print").splitlines()
    def _is_secret(path):
        if not path.endswith(".pem"):
            return True  # credential-named files are flagged by name
        try:  # a .pem is only a secret if it carries a PRIVATE KEY header (public keys are fine); never print the bytes
            return b"PRIVATE KEY" in open(path, "rb").read(400)
        except OSError:
            return False
    found = [x for x in found if _is_secret(x)]
    if found:
        f["secret-looking file under ~/code (move to ~/.secrets; never print or commit it)"] += [os.path.relpath(x, ROOT) for x in found]
    # big data dirs inside repos (info)
    for r in repos:
        for c in os.listdir(r["path"]):
            cp = os.path.join(r["path"], c)
            if c in DATA_DIR_NAMES and os.path.isdir(cp) and not os.path.islink(cp):
                size = sh("du", "-sm", cp).split()
                if size and int(size[0]) > 500:
                    st_lines = sh("git", "-C", r["path"], "status", "--porcelain", "--ignored", "--", c).splitlines()
                    ign = bool(st_lines) and all(l.startswith("!!") for l in st_lines)
                    tracked = sh("git", "-C", r["path"], "ls-files", c).count("\n")
                    state = "gitignored" if ign else (f"{tracked} tracked files" if tracked else "untracked and NOT ignored")
                    f["INFO large data dir inside a repo (fine if gitignored; move to ~/archive if idle 30+ days)"].append(f"{r['name']}/{c} {size[0]} MB ({state})")
    if os.environ.get("WORKSPACE_MAP_SKIP_GITHUB") != "1":
        for title, items in github_coverage(ex):
            f[title].extend(items)
    return f


def credential_override(url, accounts=None, owner=None):
    """git -c flags for a remote in an account read through a different gh wrapper than the owner's
    (an organization's remotes need the per-request credential helper of their own wrapper)."""
    accounts = github_accounts() if accounts is None else accounts
    m = re.search(r"github[^/:]*[:/]([^/]+)/", url)
    if not m or m.group(1) not in accounts:
        return []
    wrapper, mine = accounts[m.group(1)], accounts.get(owner or github_owner())
    if wrapper == mine:
        return []
    return ["-c", "credential.https://github.com.helper=", "-c", f"credential.https://github.com.helper=!{wrapper} auth git-credential"]


# Every account whose repositories the graph must account for, and the gh wrapper that may read it, are
# `github_accounts` in graph-config.yaml.
REPO_FIELDS = "name,nameWithOwner,description,isArchived,isFork,isPrivate,pushedAt"


def list_repo_details():
    """Every repository of every account in github_accounts(), with its GitHub metadata. Raises RuntimeError when
    any account cannot answer: a partial list would make missing repositories look covered."""
    repos = []
    for owner, wrapper in github_accounts().items():
        try:
            out = subprocess.run([wrapper, "repo", "list", owner, "--limit", "2000", "--json", REPO_FIELDS],
                                 capture_output=True, text=True, timeout=120)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RuntimeError(f"{wrapper} repo list {owner} failed: {exc}") from None
        if out.returncode != 0:
            raise RuntimeError(f"{wrapper} repo list {owner} exit {out.returncode}: {out.stderr.strip()[:200]}")
        repos += json.loads(out.stdout)
    return repos


def list_github_repos():
    """Non-archived repositories: a bare name in the owner's account, Owner/name in the other accounts."""
    me = github_owner()
    return [r["name"] if r["nameWithOwner"].split("/")[0] == me else r["nameWithOwner"]
            for r in list_repo_details() if not r.get("isArchived")]


def uncovered_repos(ex, graph_records, names):
    """The names (as list_github_repos spells them) with no graph record and no stated reason to have none.
    A bare name also counts as covered by a record in another account, since a personal copy of an
    organization repository is the same project. An Owner/name needs its own record or its own reason:
    the same bare name elsewhere proves nothing about a repository in that account."""
    known = {str(r.get("id") or "").lower() for r in graph_records}
    known |= {str(r.get("github_repo") or "").split("/")[-1].lower() for r in graph_records}
    known_full = {str(r.get("github_repo") or "").lower() for r in graph_records}
    explained = {str(k).lower() for k in (ex.get("github_not_projects") or {})}
    patterns = [re.compile(p["pattern"], re.I) for p in (ex.get("github_not_project_patterns") or [])]
    missing = []
    for name in names:
        low, bare = name.lower(), name.split("/")[-1]
        if low in explained or any(p.search(bare) for p in patterns):
            continue
        if low in known_full if "/" in name else low in known:
            continue
        missing.append(name)
    return sorted(missing)


def github_coverage(ex, records=None, lister=list_github_repos):
    """Every non-archived GitHub repository is a PROJECT_GRAPH record or is explained in workspace_map_extras.yaml
    (github_not_projects, or a github_not_project_patterns entry). Returns (finding title, items) pairs."""
    if records is None:
        records = graph_records()
    try:
        names = lister()
    except RuntimeError as exc:
        return [("GitHub coverage NOT CHECKED (fix gh access; the graph may be missing repositories)", [str(exc)])]
    missing = uncovered_repos(ex, records, names)
    if not missing:
        return []
    return [("GitHub repository in neither PROJECT_GRAPH.json nor workspace_map_extras.yaml github_not_projects "
             "(add a graph record with a one_liner, or list it with a reason)", missing)]


def render_report(f, rows):
    lines = [f"# Workspace health ({time.strftime('%Y-%m-%d %H:%M')})\n", f"{len(rows)} top-level entries checked.\n"]
    actionable = {k: v for k, v in f.items() if not k.startswith("INFO")}
    if not f:
        lines.append("**Clean.** No unknown entries, clutter, duplicate clones, stale worktrees, or unowned dirty repos.")
    for k in sorted(f):
        lines.append(f"## {k}  ({len(f[k])})")
        lines += [f"- {x}" for x in f[k]]
        lines.append("")
    return "\n".join(lines), len(actionable)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", help="write the check report to this path")
    a = ap.parse_args()
    if not a.check:
        ap.error("pass --check")
    try:
        rows, ex = classify()
        f = check(rows, ex)
    except ConfigMissing as exc:  # a missing settings file is a crash, not a finding: exit 2, never 1
        print(f"CRASH: {exc}", file=sys.stderr)
        sys.exit(2)
    text, n = render_report(f, rows)
    print(text)
    if a.report:
        os.makedirs(os.path.dirname(a.report), exist_ok=True)
        open(a.report, "w").write(text + "\n")
    print(f"findings needing action: {n}   exit {1 if n else 0}")
    sys.exit(1 if n else 0)


if __name__ == "__main__":
    main()

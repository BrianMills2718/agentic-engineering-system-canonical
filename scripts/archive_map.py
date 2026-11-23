#!/usr/bin/env python3
"""archive_map: the check that keeps ~/archive explained.

  archive_map.py --check         report archive entries the registry does not explain (exit 1 if any), and
                                 archives that hold the ONLY copy of something. An entry whose folder was
                                 offloaded to Drive names the exact tar in `offloaded:` and is not "gone".

Implements: workspace-map-check/settings-come-from-config

Requirement text (generated):
    workspace-map-check/settings-come-from-config: The project graph SHALL be read from
        `PROJECT_GRAPH` or `~/code2/aes-config/PROJECT_GRAPH.json`; `workspace_map_extras.yaml` and
        `archive_map_registry.yaml` SHALL be read from beside the graph (`WORKSPACE_MAP_EXTRAS` and
        `ARCHIVE_MAP_REGISTRY` override); the owner, the GitHub accounts and the concern repository
        SHALL come from the environment or `graph-config.yaml` beside the graph. A missing file or
        value SHALL stop the run with a message naming where to put it, and the run SHALL exit 2,
        not the findings code 1.

Two sources, nothing invented:
  * archive_map_registry.yaml  hand-written purpose / why / restore for each ~/archive entry. One person's own
    data: it sits beside the project graph (PROJECT_GRAPH, else ~/code2/aes-config/PROJECT_GRAPH.json);
    ARCHIVE_MAP_REGISTRY overrides the path
  * facts computed from the archive itself on every run: size, file count, age, receipts
    (registered-repository-archive-v1, workspace-custody-receipt/v1), duplicate-clone manifests, wiki/log.md,
    git bundles (do their commits exist in the live repo?) and embedded clones (unpushed commits? dirty?)

"Holds the only copy" is computed, not asserted: a bundle whose commits are missing from its live repo, or a
clone with unpushed commits, is flagged ONLY COPY. A registry `only_copy:` of yes/no overrides the computation
only when it names the evidence (`only_copy_evidence`).

Ported from Project Meta `scripts/archive_map.py` (retirement plan step 6) without `--write-map` and its
ARCHIVE_MAP.md page (the derived page was dropped, Decision 20).
"""
import argparse, collections, glob, json, os, subprocess, sys, time

try:
    import yaml
except ImportError:
    sys.exit("archive_map.py needs PyYAML")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ARCHIVE = os.path.expanduser(os.environ.get("ARCHIVE_ROOT", "~/archive"))
CODE = os.path.expanduser(os.environ.get("CODE_ROOT", "~/code"))


def git(*a, cwd=None):
    r = subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout


def registry_path():
    graph = os.path.expanduser(os.environ.get("PROJECT_GRAPH") or "~/code2/aes-config/PROJECT_GRAPH.json")
    return os.path.expanduser(os.environ.get("ARCHIVE_MAP_REGISTRY") or os.path.join(os.path.dirname(graph), "archive_map_registry.yaml"))


def load_registry():
    path = registry_path()
    if not os.path.isfile(path):
        raise FileNotFoundError(f"archive_map: registry not found at {path}: put archive_map_registry.yaml there, or name it with ARCHIVE_MAP_REGISTRY")
    return yaml.safe_load(open(path))


def walk_stats(p):
    size = nfiles = 0
    newest = 0.0
    gits, bundles = [], []
    if os.path.isfile(p):
        st = os.stat(p)
        return st.st_size, 1, st.st_mtime, gits, bundles
    for dp, dns, fns in os.walk(p):
        if ".git" in dns:
            gits.append(dp)
            dns.remove(".git")
            for gdp, _, gfns in os.walk(os.path.join(dp, ".git")):  # count the history's BYTES (not its files): embedded clones were under-reported by 3.5 GB
                for gf in gfns:
                    try:
                        size += os.lstat(os.path.join(gdp, gf)).st_size
                    except OSError:
                        pass
        for f in fns:
            fp = os.path.join(dp, f)
            try:
                st = os.lstat(fp)
            except OSError:
                continue
            size += st.st_size
            nfiles += 1
            newest = max(newest, st.st_mtime)
            if f.endswith(".bundle"):
                bundles.append(fp)
    return size, nfiles, newest, gits, bundles


def bundle_coverage(bundle, live_repo):
    """(unique heads, heads present in the live repo) -- present means the commit exists in that repo's objects."""
    rc, out = git("bundle", "list-heads", bundle)
    heads = sorted({l.split()[0] for l in out.splitlines() if l.strip()})
    if rc != 0 or not heads:
        return 0, 0
    if not live_repo or not os.path.isdir(live_repo):
        return len(heads), 0
    have = sum(1 for h in heads if subprocess.run(["git", "-C", live_repo, "cat-file", "-e", h + "^{commit}"], capture_output=True).returncode == 0)
    return len(heads), have


def facts(name, reg):
    p = os.path.join(ARCHIVE, name)
    size, nfiles, newest, gits, bundles = walk_stats(p)
    f = {"size": size, "files": nfiles, "age_d": int((time.time() - newest) / 86400) if newest else None, "notes": [], "only_copy": False, "only_copy_why": []}
    for rc in glob.glob(p + "/*/archive-receipt.json") + glob.glob(p + "/archive-receipt.json"):
        try:
            d = json.load(open(rc))
            f["notes"].append(f"repo-archive receipt: archived {str(d.get('archived_at', ''))[:10]}, head {str(d.get('head', ''))[:9]}, replacement `{d.get('replacement')}`")
        except (OSError, ValueError):
            pass
    for m in glob.glob(p + "/*.manifest.json")[:1]:
        try:
            d = json.load(open(m))
            f["notes"].append(f"duplicate-clone retirement: {str(d.get('reason', ''))[:170]} (kept instead: {d.get('kept_instead')})")
        except (OSError, ValueError):
            pass
    if os.path.exists(p + "/wiki/log.md"):
        f["notes"].append("has wiki/log.md (per-file retirement log with rationale and recovery path)")
    live = os.path.join(CODE, reg.get("repo", "")) if reg.get("repo") else None
    for b in bundles:
        blive = live
        if not blive:  # no registry repo: a bundle inside a folder named after a live repo (e.g. <repo>/lane-state.bundle) belongs to it
            cand = os.path.join(CODE, os.path.basename(os.path.dirname(b)))
            blive = cand if os.path.isdir(os.path.join(cand, ".git")) else None
        n, have = bundle_coverage(b, blive)
        tag = os.path.basename(b)[:46]
        if n and have == n:
            f["notes"].append(f"bundle {tag}: all {n} commits also exist in ~/code/{os.path.relpath(blive, CODE) if blive else '?'}")
        elif n:
            f["notes"].append(f"bundle {tag}: {n - have} of {n} commits NOT in a live repo")
            f["only_copy"] = True
            f["only_copy_why"].append(f"bundle {tag} has {n - have} commits not found in {'~/code/' + os.path.relpath(blive, CODE) if blive else 'any named live repo'}")
    for g in gits:
        rc, out = git("log", "--branches", "--not", "--remotes", "--oneline", cwd=g)
        unp = len([l for l in out.splitlines() if l.strip()]) if rc == 0 else 0
        rc2, st = git("status", "--porcelain", cwd=g)
        dirty = len([l for l in st.splitlines() if l.strip()]) if rc2 == 0 else 0
        if unp or dirty:
            f["notes"].append(f"embedded clone {os.path.relpath(g, p)}: {unp} unpushed commits, {dirty} uncommitted files")
            f["only_copy"] = True
            f["only_copy_why"].append(f"clone {os.path.relpath(g, p)} has {unp} unpushed commits / {dirty} uncommitted files")
    if reg.get("only_copy") in (True, False, "yes", "no"):
        v = reg["only_copy"] in (True, "yes")
        f["only_copy"] = v
        if reg.get("only_copy_evidence"):
            f["only_copy_why"] = [reg["only_copy_evidence"]]
    return f


def entries():
    reg = load_registry()
    items = reg.get("entries") or {}
    names = sorted(os.listdir(ARCHIVE))
    return reg, items, names


def offloaded(item):
    """The exact Drive tar an offloaded entry names, or "" (offload-cold moves idle ~/archive folders to Drive).

    Implements: workspace-map-check/offloaded-archive-entry-is-not-gone"""
    tar = (item or {}).get("offloaded") or ""
    return tar if isinstance(tar, str) and tar.endswith(".tar.gz") else ""


def check():
    reg, items, names = entries()
    findings = collections.defaultdict(list)
    for n in names:
        if n not in items:
            findings["UNKNOWN ~/archive entry (add it to archive_map_registry.yaml beside the project graph)"].append(n)
        else:
            for k in ("purpose", "why", "restore"):
                if not items[n].get(k):
                    findings[f"archive registry entry missing '{k}'"].append(n)
    for n in items:
        if n not in names and not offloaded(items[n]):
            findings["registry lists an archive that is gone from ~/archive (name its offloaded: tar, remove it, or restore it)"].append(n)
    only = []
    for n in names:
        f = facts(n, items.get(n, {}))
        if f["only_copy"]:
            only.append(f"{n}: {'; '.join(f['only_copy_why'])}")
    if only:  # informational: keeps the guard visible without demanding action
        findings["INFO archives that hold the ONLY copy of something (keep; see archive_map.py --check)"] += only
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if not a.check:
        ap.error("pass --check")
    f = check()
    act = {k: v for k, v in f.items() if not k.startswith("INFO")}
    for k, v in sorted(f.items()):
        print(f"## {k} ({len(v)})")
        for x in v:
            print(f"- {x}")
    print(f"findings needing action: {sum(len(v) for v in act.values())}")
    sys.exit(1 if act else 0)


if __name__ == "__main__":
    main()

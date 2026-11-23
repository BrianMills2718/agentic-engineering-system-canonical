#!/usr/bin/env python3
"""Flat cap on Markdown files in Brian-owned repositories, with written exceptions.

Rule (Brian, 2026-10-07): a repository Brian owns holds at most 100 git-tracked .md
files unless it carries a clearly explained exception. Repositories other people or
organizations own (Inside-Success, upstream projects) are out of scope.

Counted on each repo's default branch as last fetched (origin/HEAD), not the
checked-out branch. Which repositories: every PROJECT_GRAPH.json entry whose github_repo owner is
BrianMills2718 and whose local path is a git checkout. Entries that resolve to the
same checkout are counted once.
Markdown files under generated/ are generator output, not documents anyone keeps: they are not counted
(Brian, 2026-11-17, "skip generated").

Exception: a file named .md-file-cap.yaml at the repository root:

    limit: 400
    reason: "This repo is a document corpus; the Markdown files are its product."

`limit` raises the cap for that repo only; `reason` is a plain sentence a person can
judge. An exception without a reason, or with a limit the repo has already outgrown,
is a finding like any other.

Second rule (Brian, 2026-10-07, "probably both"): every Markdown document a reader is
meant to read is reachable from the repo's wiki/index.md within two links. Files a
reader is not meant to open may stay unlinked: instruction files (CLAUDE.md, AGENTS.md,
SKILL.md, .claude/, any hidden folder such as .project-brain/), test fixtures (tests/fixtures/),
TEMPLATE.md, generator outputs (anything under generated/, or a .md path assigned to an
*OUTPUT* constant in any Python file), and folders or files the exception file lists, each
with its own reason:

    unlinked_ok:
      - path: raw/sources/
        reason: "Source documents the wiki cites; material, not reading."

Third column, layout (AES canonical, plan aes-brownfield-docs M6): a repository that declares
its documentation layout in .agentic/repo.yaml keeps decision records under its decision_roots,
governing design (any architecture/ folder) under its normative_roots, numbered plans
(NNN_name.md) under its plan_roots, and committed generator output under generated/. A repository
without .agentic/repo.yaml is reported "layout not declared": not a pass, and not a failure until
it declares a layout. Folders or files kept elsewhere on purpose go under `layout_ok` in the
exception file, each with a reason. The reachability and layout rules are the same as
agentic-engineering-system-canonical proposals/aes-brownfield-docs/reach.py and layout_check.py.

Fourth column, durable documents (AES canonical, plan aes-durable-docs M5): a repository whose
.agentic/repo.yaml carries a `durable_documents` block is checked with company-planning's
durable_docs_check.py (`--repo <checkout at ref> --arc42`: goal, requirements, system model and
trace, decisions with Governs lines, plans, catalog). A repository without the block is reported
"durable undeclared", which is not a failure, so the one concern opens only for a repository that
declared its durable set and then let it drift. The checker comes from DURABLE_DOCS_CHECK, else
from the company-planning checkout named in PROJECT_GRAPH.json at its default branch, copied once
per content hash into ~/.cache/md-file-cap/ and reused. Each check runs in a shared clone under
<tmp>/md-file-cap/ (its origin/* copied from the checked repository's origin/*, so they are
GitHub's branches), never a worktree registered on the checked repository, so a killed run leaves
only a folder that the next run removes once it is older than STALE_SECONDS.

Classification uses paths and code assignments only, never document prose.

    md_file_cap.py [--cap 100] [--graph PATH] [--json] [--repo PATH [--ref REF]]

--repo checks the given checkouts (at --ref, default their default branch) instead of the
Brian-owned graph entries, for spot checks on repositories outside the daily scope.

Prints one line per over-cap repository, a summary with counts, and exits 1 when any
repository breaks the rule (0 when none do).

Implements: project-graph-config/the-checks-read-the-graph-and-owner-from-the-person-s-own-files
"""
import argparse, hashlib, json, os, re, shutil, signal, subprocess, sys, tempfile, time
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
# Copied from Project Meta scripts/md_file_cap.py at f1e27c906 (retirement plan, slice 1). The only change is where
# The project graph is one person's own data: the PROJECT_GRAPH environment variable names it, else it is read from the
# private `aes-config` repository (retirement plan step 4, Decision 20). The GitHub owner whose repositories are
# checked comes from `graph-config.yaml` beside the graph (key `owner`), or the PROJECT_GRAPH_OWNER environment variable.
GRAPH_DEFAULT = os.environ.get("PROJECT_GRAPH") or os.path.expanduser("~/code2/aes-config/PROJECT_GRAPH.json")

OWNER = None  # set once per run in main() from graph_owner(); the code below compares against it


def graph_owner(graph_path=None):
    """The GitHub owner whose repositories are checked; fails loudly when no setting names one."""
    named = os.environ.get("PROJECT_GRAPH_OWNER")
    if named:
        return named
    config = os.path.join(os.path.dirname(os.path.expanduser(graph_path or GRAPH_DEFAULT)), "graph-config.yaml")
    try:
        found = re.search(r"^owner:\s*(\S+)", open(config).read(), re.M)
    except OSError:
        found = None
    if not found:
        raise SystemExit(f"md_file_cap: no owner named: set PROJECT_GRAPH_OWNER or put `owner:` in {config}")
    return found.group(1)


EXCEPTION_FILE = ".md-file-cap.yaml"
DEFAULT_CAP = 100


def git(path, *args):
    r = subprocess.run(["git", "-C", path, *args], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def remote_slug(path):
    """owner/name from the origin URL (https or ssh, any host alias), or '' when there is none."""
    m = re.search(r"[:/]([^/:]+)/([^/]+?)(?:\.git)?/?$", (git(path, "remote", "get-url", "origin") or "").strip())
    return f"{m.group(1)}/{m.group(2)}" if m else ""


def owned_checkouts(graph_path):
    """Distinct git toplevels for Brian-owned graph entries that exist on disk."""
    seen = {}
    for p in json.load(open(graph_path)):
        if not p.get("path"):
            continue
        path = os.path.expanduser(p["path"])
        if not os.path.isdir(path):
            continue
        # Some entries carry no github_repo; their origin remote still says who owns them.
        gr = p.get("github_repo") or remote_slug(path)
        if gr.split("/")[0] != (OWNER or graph_owner(graph_path)):
            continue
        top = (git(path, "rev-parse", "--show-toplevel") or "").strip()
        if top and top not in seen:
            seen[top] = gr
    return seen


def default_ref(top):
    """The repo's default branch as last fetched (origin/HEAD), else the checked-out HEAD.

    The rule is about the repository's main line, not whichever work branch a local
    checkout happens to have checked out.
    """
    for ref in ("origin/HEAD", "origin/main", "origin/master"):
        if git(top, "rev-parse", "--verify", "--quiet", ref + "^{commit}"):
            return ref
    return "HEAD"


def count_md(top, ref="HEAD"):
    out = git(top, "ls-tree", "-r", "-z", "--name-only", ref)
    if out is None:
        return None
    return sum(1 for f in out.split("\0")
               if f.lower().endswith(".md") and not f.startswith("generated/"))


def read_exception(top, ref="HEAD"):
    """Return (limit, reason, problem). problem is None when the file is absent or valid."""
    text = git(top, "show", f"{ref}:{EXCEPTION_FILE}")
    if text is None:
        return None, None, None
    try:
        import yaml
        data = yaml.safe_load(text) or {}
    except Exception as e:  # unreadable exception file is itself a finding
        return None, None, f"{EXCEPTION_FILE} unreadable: {e}"
    limit, reason = data.get("limit"), str(data.get("reason") or "").strip()
    if limit is None and not reason:  # a file that only lists unlinked_ok or layout_ok raises no limit
        return None, None, None
    if not isinstance(limit, int) or limit <= 0:
        return None, reason, f"{EXCEPTION_FILE} needs a positive integer 'limit'"
    if not reason:
        return limit, None, f"{EXCEPTION_FILE} needs a 'reason' explaining why this repo needs more than the cap"
    return limit, reason, None


LINK = re.compile(r"\]\(([^)\s]+)\)")
OUTPUT_ASSIGN = re.compile(r"^\s*\w*OUTPUT\w*\s*=\s*Path\(\s*[\"']([^\"']+\.md)[\"']", re.M | re.I)
WIKI_ENTRY = "wiki/index.md"
MAX_HOPS = 2


def read_unlinked_ok(top, ref="HEAD"):
    """Return ([(prefix, reason)], problem) from the exception file's optional unlinked_ok list."""
    text = git(top, "show", f"{ref}:{EXCEPTION_FILE}")
    if text is None:
        return [], None
    try:
        import yaml
        entries = (yaml.safe_load(text) or {}).get("unlinked_ok") or []
    except Exception as e:
        return [], f"{EXCEPTION_FILE} unreadable: {e}"
    out = []
    for e in entries:
        path, reason = str((e or {}).get("path") or "").strip(), str((e or {}).get("reason") or "").strip()
        if not path or path in (".", "/", "./"):
            return [], f"{EXCEPTION_FILE} unlinked_ok entries need a specific folder or file 'path'"
        if not reason:
            return [], f"{EXCEPTION_FILE} unlinked_ok entry {path} needs a 'reason'"
        out.append((path.rstrip("/"), reason))
    return out, None


class BlobReader:
    """Read many files at one ref through a single `git cat-file --batch` process."""

    def __init__(self, top, ref):
        self.ref = ref
        self.proc = subprocess.Popen(["git", "-C", top, "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def read(self, path):
        self.proc.stdin.write(f"{self.ref}:{path}\n".encode())
        self.proc.stdin.flush()
        header = self.proc.stdout.readline().decode().split()
        if len(header) < 3 or header[1] != "blob":
            return ""
        data = self.proc.stdout.read(int(header[2]))
        self.proc.stdout.read(1)  # trailing newline
        return data.decode("utf-8", "replace")

    def close(self):
        self.proc.stdin.close()
        self.proc.wait()


def under(path, prefix):
    """True when path is prefix itself or inside the folder prefix names."""
    return path == prefix or path.startswith(prefix.rstrip("/") + "/")


def reachability(top, ref="HEAD"):
    """Return {status, reachable, orphans: [paths], beyond: [paths], detail} for the wiki rule."""
    tracked = (git(top, "ls-tree", "-r", "-z", "--name-only", ref) or "").split("\0")
    md = {p for p in tracked if p.lower().endswith(".md")}
    allowed, problem = read_unlinked_ok(top, ref)
    if problem:
        return {"status": "orphans", "reachable": 0, "orphans": [], "beyond": [], "detail": problem}
    if WIKI_ENTRY not in md:
        return {"status": "no-wiki", "reachable": 0, "orphans": sorted(md), "beyond": [],
                "detail": f"no {WIKI_ENTRY}; add one that routes to the repo's reader documents"}
    blobs = BlobReader(top, ref)
    dist, queue = {WIKI_ENTRY: 0}, [WIKI_ENTRY]
    while queue:
        cur = queue.pop(0)
        for target in LINK.findall(blobs.read(cur)):
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            target = unquote(target.split("#")[0])  # links to names with spaces are %20-encoded
            if target.startswith("/"):  # root-relative: repo root first, then the wiki folder
                path = os.path.normpath(target.lstrip("/"))
                if path not in md:
                    path = os.path.normpath(os.path.join(os.path.dirname(WIKI_ENTRY), path))
            else:
                path = os.path.normpath(os.path.join(os.path.dirname(cur), target))
            if path in md and path not in dist:
                dist[path] = dist[cur] + 1
                queue.append(path)
    generated = set()
    for py in (p for p in tracked if p.endswith(".py")):
        generated.update(OUTPUT_ASSIGN.findall(blobs.read(py)))
    blobs.close()

    def exempt(p):
        base = os.path.basename(p)
        return (base in ("CLAUDE.md", "AGENTS.md", "SKILL.md") or p.startswith(".claude/")
                or any(part.startswith(".") for part in p.split("/")[:-1])  # hidden tool folders (.project-brain/, .wiki/, .templates/)
                or p.startswith("tests/fixtures/") or base == "TEMPLATE.md"
                or p.startswith("generated/") or p in generated
                or any(under(p, prefix) for prefix, _ in allowed))

    orphans = sorted(p for p in md - set(dist) if not exempt(p))
    beyond = sorted(p for p, d in dist.items() if d > MAX_HOPS and not exempt(p))
    bad = orphans + beyond
    detail = (f"{len(orphans)} reader docs not linked from {WIKI_ENTRY}" + (f", {len(beyond)} more than {MAX_HOPS} links deep" if beyond else "")
              + (f" (e.g. {', '.join(bad[:3])})" if bad else "")) if bad else ""
    return {"status": "orphans" if bad else "ok", "reachable": len(dist), "orphans": orphans, "beyond": beyond, "detail": detail}


PLAN_FILE = re.compile(r"\d{2,4}_[\w.-]+\.md$")
PY_OUTPUT = re.compile(r"^\s*\w*OUTPUT\w*\s*=\s*Path\(\s*[\"']([^\"']+)[\"']", re.M | re.I)
MAKE_OUTPUT = re.compile(r"--output(?:-root)?[ =]+([\w./-]+)")


def layout(top, ref="HEAD"):
    """Return {status: ok|findings|undeclared, findings: [(kind, path)], detail} for the AES layout rule."""
    try:
        import yaml
    except ImportError:
        return {"status": "findings", "findings": [], "detail": "PyYAML required for the layout check"}
    text = git(top, "show", f"{ref}:.agentic/repo.yaml")
    cfg = (yaml.safe_load(text) or {}) if text else {}
    if not cfg:
        return {"status": "undeclared", "findings": [], "detail": "layout not declared (no .agentic/repo.yaml)"}
    roots = cfg.get("authorities") if isinstance(cfg, dict) else None
    if not roots:  # a repo.yaml that only declares durable_documents has not declared a layout
        return {"status": "undeclared", "findings": [], "detail": "layout not declared (no authorities block in .agentic/repo.yaml)"}
    norm, dec, plans = ([r.rstrip("/") + "/" for r in roots.get(k) or []] for k in ("normative_roots", "decision_roots", "plan_roots"))
    cap = yaml.safe_load(git(top, "show", f"{ref}:{EXCEPTION_FILE}") or "{}") or {}
    keep = [(str((e or {}).get("path") or "").rstrip("/"), str((e or {}).get("reason") or "").strip()) for e in cap.get("layout_ok") or []]
    tracked = (git(top, "ls-tree", "-r", "-z", "--name-only", ref) or "").split("\0")
    inside = lambda p, rs: any(p.startswith(r) for r in rs)
    kept = lambda p: any(k and under(p, k) for k, _ in keep)
    blobs = BlobReader(top, ref)
    outputs = set()
    for py in (p for p in tracked if p.endswith(".py")):
        outputs.update(PY_OUTPUT.findall(blobs.read(py)))
    outputs.update(MAKE_OUTPUT.findall(blobs.read("Makefile")))
    blobs.close()
    gen_roots = [o.lstrip("./").rstrip("/") + "/" for o in outputs]
    findings = [("root-missing", r) for r in norm + dec + plans if not any(p.startswith(r) for p in tracked)]
    for p in tracked:
        if not p.lower().endswith(".md") or kept(p) or os.path.basename(p) in ("CLAUDE.md", "AGENTS.md", "README.md", "INDEX.md"):
            continue
        parts = p.split("/")
        if p.startswith("generated/") or any(p == g.rstrip("/") or p.startswith(g) for g in gen_roots) or "okf" in parts[:-1]:
            continue  # generator output is judged below; OKF bundles hold typed concepts, not the repo's own records
        if (re.match(r"ADR[-_]", os.path.basename(p)) or "decisions" in parts[:-1]) and not inside(p, dec):
            findings.append(("decision-outside", p))
        elif "architecture" in parts[:-1] and not inside(p, norm):
            findings.append(("design-outside", p))
        elif PLAN_FILE.match(os.path.basename(p)) and not inside(p, plans):
            findings.append(("plan-outside", p))
    for o in sorted(outputs):
        o = o.lstrip("./").rstrip("/")
        committed = any(p == o or p.startswith(o + "/") for p in tracked)  # runtime outputs never committed are not documentation
        if o and committed and not o.startswith("generated/") and not kept(o) and not o.startswith(("$", "/tmp")):
            findings.append(("generated-outside", o))
    findings += [("layout-ok-without-reason", k) for k, r in keep if not r]
    detail = (f"{len(findings)} layout findings (e.g. " + ", ".join(f"{k} {p}" for k, p in findings[:3]) + ")") if findings else ""
    return {"status": "findings" if findings else "ok", "findings": findings, "detail": detail}


CHECKER_REL = "plugins/company-planning/scripts/durable_docs_check.py"
SCHEMA_REL = "plugins/company-planning/contracts/durable-documents/durable_documents.v0_1.schema.json"
_checker = {}


def resolve_checker(graph_path=None):
    """Path to durable_docs_check.py: $DURABLE_DOCS_CHECK, else company-planning's default branch copied out once per run."""
    if os.environ.get("DURABLE_DOCS_CHECK"):
        return os.environ["DURABLE_DOCS_CHECK"]
    if "path" in _checker:
        return _checker["path"]
    _checker["path"] = None
    try:
        graph = json.load(open(graph_path or GRAPH_DEFAULT))
    except (OSError, ValueError):
        return None
    entry = next((p for p in graph if isinstance(p, dict) and p.get("id") == "company-planning"), None)
    top = os.path.expanduser((entry or {}).get("path") or "")
    if not top or not os.path.isdir(top):
        return None
    ref = default_ref(top)
    script, schema = git(top, "show", f"{ref}:{CHECKER_REL}"), git(top, "show", f"{ref}:{SCHEMA_REL}")
    if not script or not schema:
        return None
    # One copy per content hash, reused by every run (a fresh temp folder per run leaked one per run, 160 in a day).
    root = cache_root()
    final = os.path.join(root, "durable-checker-" + hashlib.sha256((script + "\0" + schema).encode()).hexdigest()[:16])
    if not os.path.isfile(os.path.join(final, CHECKER_REL)):
        os.makedirs(root, exist_ok=True)
        part = tempfile.mkdtemp(prefix=".partial-", dir=root)
        for rel, text in ((CHECKER_REL, script), (SCHEMA_REL, schema)):
            os.makedirs(os.path.join(part, os.path.dirname(rel)), exist_ok=True)
            with open(os.path.join(part, rel), "w") as fh:
                fh.write(text)
        try:
            os.rename(part, final)  # atomic: a reader never sees a half-written copy
        except OSError:  # another run stored the same content first
            shutil.rmtree(part, ignore_errors=True)
    if not os.path.isfile(os.path.join(final, CHECKER_REL)):
        return None
    os.utime(final)  # in use: a run with a newer checker sweeps only copies untouched for STALE_SECONDS
    sweep_stale(root, keep=final)
    _checker["path"] = os.path.join(final, CHECKER_REL)
    return _checker["path"]


def durable(top, ref="HEAD", checker=None):
    """Return {status: ok|findings|undeclared, findings: [line], detail} for the AES durable document set."""
    try:
        import yaml
    except ImportError:
        return {"status": "findings", "findings": [], "detail": "PyYAML required for the durable-documents check"}
    try:
        cfg = yaml.safe_load(git(top, "show", f"{ref}:.agentic/repo.yaml") or "") or {}
    except yaml.YAMLError as exc:
        return {"status": "findings", "findings": [], "detail": f"durable: .agentic/repo.yaml does not parse ({exc.__class__.__name__})"}
    if not isinstance(cfg, dict) or "durable_documents" not in cfg:
        return {"status": "undeclared", "findings": [], "detail": "durable document set not declared"}
    checker = checker or resolve_checker()
    if not checker:
        return {"status": "findings", "findings": [], "detail": "durable: checker unavailable (set DURABLE_DOCS_CHECK or check the company-planning checkout)"}
    sha = (git(top, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}") or "").strip()
    common = (git(top, "rev-parse", "--path-format=absolute", "--git-common-dir") or "").strip()
    if not sha or not common:
        return {"status": "findings", "findings": [], "detail": f"durable: could not resolve {ref} in {top}"}
    parent = tree_root()
    os.makedirs(parent, exist_ok=True)
    sweep_stale(parent)
    tmp = tempfile.mkdtemp(prefix="durable-", dir=parent)
    try:
        # A shared clone, not `git worktree add`: the checker reads history, so a `git archive` copy will not do,
        # but nothing is registered on the checked repository, so a run killed before this `finally` (SIGKILL, a
        # hook timeout) leaves only a folder that sweep_stale removes.
        # A clone of a local path makes origin/* the source's local branches, not GitHub's. plan-code-wiki's local
        # main sat weeks behind its origin/main, so lockstep's `make check` (`pcw check --base $(git merge-base
        # origin/main HEAD)`) blocked on 102 files the checked revision never changed (2026-11-07). The fetch
        # mirrors the source's GitHub-tracking refs over them; a source with none matches nothing, which git does
        # not treat as an error, and keeps its local branches as origin/*.
        for step in (["git", "clone", "-q", "--shared", "--no-checkout", common, tmp],
                     ["git", "-C", tmp, "fetch", "-q", "origin", "+refs/remotes/origin/*:refs/remotes/origin/*"],
                     ["git", "-C", tmp, "checkout", "-q", "--detach", sha]):
            done = subprocess.run(step, capture_output=True, text=True)
            if done.returncode:
                return {"status": "findings", "findings": [], "detail": f"durable: could not check out {ref}: {done.stderr.strip()[:200]}"}
        proc = subprocess.run([sys.executable, checker, "--repo", tmp, "--arc42"], capture_output=True, text=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    lines =[l for l in proc.stdout.splitlines() if l.startswith("FINDING ")]
    if proc.returncode == 0:
        return {"status": "ok", "findings": [], "detail": ""}
    if proc.returncode == 1:
        return {"status": "findings", "findings": lines,
                "detail": f"{len(lines)} durable-document findings (e.g. " + "; ".join(l[len("FINDING "):] for l in lines[:2])[:300] + ")"}
    tail = (proc.stderr or proc.stdout).strip().splitlines()[-1:] or ["no output"]
    return {"status": "findings", "findings": [], "detail": f"durable: checker exit {proc.returncode} (invalid input): {tail[0][:200]}"}


# A leftover older than this is from a killed run: a whole daily run (every Brian-owned repository, each with
# its catalog command) takes minutes, and one --repo check of lockstep took 96 s on 2026-11-07.
STALE_SECONDS = 6 * 3600


def cache_root():
    """Folder holding the company-planning checker copies, one per content hash, reused across runs."""
    return os.path.join(os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"), "md-file-cap")


def tree_root():
    """Parent of the per-check clones. Only this script writes here, so everything in it is its own."""
    return os.path.join(tempfile.gettempdir(), "md-file-cap")


def sweep_stale(parent, keep=None, max_age=STALE_SECONDS):
    """Remove folders in `parent` untouched for max_age seconds: what runs killed before their cleanup left."""
    now = time.time()
    try:
        names = os.listdir(parent)
    except OSError:
        return
    for name in names:
        path = os.path.join(parent, name)
        try:
            stale = now - os.lstat(path).st_mtime > max_age
        except OSError:
            continue
        if stale and path != keep and os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path, ignore_errors=True)


def _exit_on_signal(signum, frame):
    raise SystemExit(128 + signum)  # unwind, so durable()'s finally removes its clone


def evaluate(checkouts, cap, ref_override=None):
    rows = []
    for top, slug in sorted(checkouts.items()):
        started = time.monotonic()
        ref = ref_override or default_ref(top)
        n = count_md(top, ref)
        if n is None:
            rows.append({"repo": slug, "path": top, "md": None, "status": "not-checked", "detail": "git ls-files failed"})
            continue
        limit, reason, problem = read_exception(top, ref)
        allowed = limit or cap
        if slug.split("/")[0] != (OWNER or graph_owner()):  # a --repo spot check of someone else's repository: the cap is Brian's rule only
            status, detail = "out-of-scope", "the 100-file cap applies to Brian-owned repositories only"
        elif problem:
            status, detail = "over", problem
        elif n > allowed:
            status = "over"
            detail = (f"{n} > exception limit {limit} ({reason})" if limit else
                      f"{n} > cap {cap}; prune, or add {EXCEPTION_FILE} with a limit and a reason")
        elif limit:
            status, detail = "exception", reason
        else:
            status, detail = "ok", ""
        reach = reachability(top, ref)
        lay = layout(top, ref)
        dur = durable(top, ref)
        rows.append({"repo": slug, "path": top, "ref": ref, "md": n, "limit": allowed, "status": status, "detail": detail,
                     "reach": reach["status"], "reach_detail": reach["detail"], "orphans": len(reach["orphans"]) + len(reach["beyond"]),
                     "reach_findings": reach["orphans"] + reach["beyond"],
                     "layout": lay["status"], "layout_detail": lay["detail"], "layout_findings": [f"{k} {p}" for k, p in lay["findings"]],
                     "durable": dur["status"], "durable_detail": dur["detail"], "durable_findings": dur["findings"],
                     "seconds": round(time.monotonic() - started, 2)})
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cap", type=int, default=DEFAULT_CAP)
    ap.add_argument("--graph", default=GRAPH_DEFAULT)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--repo", action="append", help="check this checkout instead of the Brian-owned graph entries (repeatable)")
    ap.add_argument("--ref", help="with --repo: the commit or ref to check (default: the repo's default branch)")
    a = ap.parse_args(argv)
    global OWNER
    OWNER = graph_owner(a.graph)
    if a.repo:
        checkouts = {}
        for path in a.repo:
            top = (git(os.path.expanduser(path), "rev-parse", "--show-toplevel") or "").strip()
            if top:
                checkouts[top] = remote_slug(top) or os.path.basename(top)
        rows = evaluate(checkouts, a.cap, a.ref)
    else:
        rows = evaluate(owned_checkouts(a.graph), a.cap)
    counts = {s: sum(r["status"] == s for r in rows) for s in ("ok", "exception", "over", "not-checked", "out-of-scope")}
    reach_counts = {s: sum(r.get("reach") == s for r in rows) for s in ("ok", "orphans", "no-wiki")}
    layout_counts = {s: sum(r.get("layout") == s for r in rows) for s in ("ok", "findings", "undeclared")}
    durable_counts = {s: sum(r.get("durable") == s for r in rows) for s in ("ok", "findings", "undeclared")}
    if a.json:
        print(json.dumps({"cap": a.cap, "counts": counts, "reach_counts": reach_counts, "layout_counts": layout_counts,
                          "durable_counts": durable_counts, "rows": rows}, indent=2))
    else:
        for r in sorted(rows, key=lambda r: -(r["md"] or 0)):
            if r["status"] in ("over", "not-checked"):
                print(f"OVER  {r['md'] if r['md'] is not None else '?':>5}  {r['repo']}  -- {r['detail']}")
        for r in rows:
            if r["status"] == "exception":
                print(f"EXCEPTION  {r['md']:>5}/{r['limit']}  {r['repo']}  -- {r['detail']}")
        for r in sorted(rows, key=lambda r: -r.get("orphans", 0)):
            if r.get("reach") in ("orphans", "no-wiki"):
                print(f"UNREACHABLE {r['orphans']:>5}  {r['repo']}  -- {r['reach_detail']}")
        for r in sorted(rows, key=lambda r: -len(r.get("layout_findings") or [])):
            if r.get("layout") == "findings":
                print(f"LAYOUT {len(r['layout_findings']):>5}  {r['repo']}  -- {r['layout_detail']}")
        for r in rows:
            if r.get("durable") == "findings":
                print(f"DURABLE {len(r['durable_findings']):>5}  {r['repo']}  -- {r['durable_detail']}")
        for r in rows:
            print(f"REPO  {r['repo']}  md={r['md'] if r['md'] is not None else '?'}  cap={r['status']}  reach={r.get('reach')}"
                  f"({r.get('orphans', 0)})  layout={r.get('layout')}({len(r.get('layout_findings') or [])})"
                  f"  durable={r.get('durable')}({len(r.get('durable_findings') or [])})")
    rc = 1 if counts["over"] or counts["not-checked"] or reach_counts["orphans"] or reach_counts["no-wiki"] or layout_counts["findings"] or durable_counts["findings"] else 0
    print(f"md-file-cap: {len(rows)} {'given' if a.repo else 'Brian-owned'} repos checked, cap {a.cap}: "
          f"ok={counts['ok']} exception={counts['exception']} over={counts['over']} "
          f"not-checked={counts['not-checked']}" + (f" out-of-scope={counts['out-of-scope']}" if counts["out-of-scope"] else "") + f"; wiki reachability ok={reach_counts['ok']} "
          f"orphans={reach_counts['orphans']} no-wiki={reach_counts['no-wiki']}; layout ok={layout_counts['ok']} "
          f"findings={layout_counts['findings']} undeclared={layout_counts['undeclared']}; durable ok={durable_counts['ok']} "
          f"findings={durable_counts['findings']} undeclared={durable_counts['undeclared']}   exit {rc}", file=sys.stderr if a.json else sys.stdout)  # keep --json stdout parseable
    return rc


if __name__ == "__main__":
    # A caller's timeout usually sends SIGTERM, which by default ends Python without running `finally` blocks.
    for _sig in (signal.SIGTERM, signal.SIGHUP):
        if signal.getsignal(_sig) == signal.SIG_DFL:
            signal.signal(_sig, _exit_on_signal)
    sys.exit(main())

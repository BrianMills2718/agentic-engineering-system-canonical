"""`aes commit check` / `aes commit replay`: the commit-tag rule (`RU-AES-COMMIT-RULE`, AP-REQ-001).

Real implementation work lands only under a plan Company Planning adopted; trivial
work still lands, decided by measured facts about the change, never by the tag
text alone. The first line of every commit message carries one tag:

- ``[Plan #N]`` / ``[Goal <id>]``: the named plan (``docs/plans/<N>_*.md``, or a
  Markdown plan whose front matter says ``plan_id: <id>``, in this repository or a
  configured plan root) declares ``method_conformance_receipt``; the adoption
  decision beside that receipt says ``adopted`` and its ``plan_sha256`` and
  ``receipt_sha256`` match the current bytes of the plan and the receipt.
- ``[Trivial]``: the change touches at most ``trivial_max_files`` files and
  ``trivial_max_lines`` added+deleted lines, adds no file under a governed root,
  and touches no running-thing file (Dockerfile, compose file, systemd unit,
  hook, deploy script, CI workflow, agent instructions).
- ``[Unplanned]``: an emergency; the message needs an ``Emergency: <reason>`` line.
- ``[Shaping <id>]``: drafting a plan; every changed file is under ``proposals/<id>/``.
- ``[Auto]``: a commit made by a scheduled job; the message needs an ``Auto-job: <job>``
  line naming the job, and the change may touch no running-thing file. There is no size
  limit (data refreshes are large); the daily report counts ``[Auto]`` commits per job so
  misuse shows up as a job that should not be committing.

``plan_adoption`` (``observe`` or ``enforce``; default: the same as ``mode``) lets ``mode:
enforce`` refuse missing tags, oversized ``[Trivial]`` and the rest while a ``[Plan #N]`` /
``[Goal <id>]`` naming a plan that is not adopted is only logged (Brian, 2026-10-07: enforce
in stages; plan adoption stays observe until each project has adopted plans).

In a repository adopted with ``aes adopt``, a commit that modifies (``M``/``T``) a
file still in ``.aes/legacy_baseline.json`` that the target does not plan is an
unplanned legacy edit, refused under any tag (check ``legacy-edit``) except Git's own
messages and an ``[Unplanned]`` emergency: plan the file through ``aes plan accept``
first, which removes it from the baseline. Deleting a legacy file is allowed.
``replay`` judges history against today's baseline.

Company Planning plans declare their path scope with the work-unit record's own field
(issue #218): front matter ``conflict_surfaces``, each entry shaped as Company Planning's
work-unit schema 1.1 ``conflictSurface`` (``kind: repository_path``, ``repository``,
``target``, ``access``). A ``[Plan #N]`` / ``[Goal <id>]`` commit whose plan is adopted may
edit a legacy file inside one of that plan's ``write`` or ``exclusive`` surfaces for this
repository; ``target`` is a file, a directory (everything under it) or a glob (``*``, ``?``,
``**``). The surfaces are inside the plan's adopted bytes, so widening them means
re-adopting the plan. A legacy edit outside the named plan's surfaces is still refused.
Once such a file has changed at ``HEAD`` it leaves the unplanned-legacy set
(``adopt.unplanned_legacy``), the way ``aes plan accept`` drops a file the target plans.

Git's own merge, fixup, squash and amend messages are accepted. Paths and tags
are matched with regular expressions (identifiers, not prose); nothing judges
what a message means.

``.aes/commit_rule.yaml`` sets ``mode`` (``observe``: log every verdict, refuse
nothing, the default; ``enforce``: refuse), the trivial limits and extra
``plan_roots``. A repository without one falls back to the machine-wide file
(``$AES_COMMIT_RULE_MACHINE_CONFIG``, default ``~/.config/aes/commit_rule.yaml``),
whose top-level keys are the defaults and whose ``repos: {<directory name>: {...}}``
entries override them for one repository; that is how the rule reaches
repositories that are not AES projects yet. Every verdict appends one JSON line to
``<git-common-dir>/aes/commit-rule-<UTC date>.jsonl``.
"""

from __future__ import annotations

import datetime as dt
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

from ruamel.yaml import YAML

from .records import load_project

_YAML = YAML(typ="safe")

CONFIG_PATH = Path(".aes") / "commit_rule.yaml"
MACHINE_CONFIG_ENV = "AES_COMMIT_RULE_MACHINE_CONFIG"
TAG_RE = re.compile(
    # plan ids may contain capitals (e.g. [Goal PATH-brent-v1-2026-10-02]); #193
    r"^\[(?:Plan #(?P<plan>\d+)|Goal (?P<goal>[A-Za-z0-9][A-Za-z0-9._:-]*)|(?P<trivial>Trivial)"
    r"|(?P<unplanned>Unplanned)|(?P<auto>Auto)|Shaping (?P<shaping>[A-Za-z0-9][A-Za-z0-9._-]*))\]"
)
GIT_OWN_PREFIXES = ("Merge ", "fixup! ", "squash! ", "amend! ")
EMERGENCY_RE = re.compile(r"^Emergency:\s*\S", re.MULTILINE)
EMERGENCY_LINE_RE = re.compile(r"^Emergency:.*$", re.MULTILINE)
# An Emergency: line that declares there is none ("Emergency: none; ...", "Emergency: n/a").
# A declared placeholder value, checked like a field value; judging whether a stated reason is a
# real emergency is the nightly light-model review's job (misuse_review.py), not this hook's.
# "none" or "n/a" must stand alone (end of line or ; . , : ( or a dash next), so a real reason that
# starts with the word ("Emergency: none of the backups ran") is still accepted.
NO_EMERGENCY_RE = re.compile(r"^Emergency:\s*(?:none|n/a|na)\s*(?:$|[;.,:(\u2014-])", re.MULTILINE | re.IGNORECASE)
AUTO_JOB_RE = re.compile(r"^Auto-job:\s*(\S.*)$", re.MULTILINE)
# Provenance, not a verdict input (Brian, 2026-10-07: "it depends on what i asked ... maybe a secondary
# tag"): who asked for the change, in their words, e.g. Asked: Brian 2026-10-07 "make it public".
ASKED_RE = re.compile(r"^Asked:\s*(\S.*)$", re.MULTILINE)
RUNNING_THING_NAMES = (
    "Dockerfile", "Dockerfile.*", "*.dockerfile", "compose.yaml", "compose.yml",
    "docker-compose*.yaml", "docker-compose*.yml", "*.service", "*.timer", "*.socket",
    "deploy.sh", "deploy-*.sh", "deploy_*.sh", "AGENTS.md", "CLAUDE.md", "*.AGENTS.md",
    # pytest loads it into every test run (plan commit-rule-followups; AES #239)
    "conftest.py",
)
RUNNING_THING_DIRS = (".githooks/", "hooks/", ".github/workflows/", ".claude/", ".codex/")
FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


@dataclass(frozen=True)
class FileChange:
    path: str
    status: str  # git name-status letter: A, M, D, R, C, T
    added: int
    deleted: int


@dataclass(frozen=True)
class RuleConfig:
    mode: str = "observe"
    trivial_max_files: int = 3
    trivial_max_lines: int = 60
    plan_roots: tuple[Path, ...] = ()
    source: str = "default"
    plan_adoption: str = "observe"
    # Federated plans: a [Goal <id>] not found under plan_roots is looked up in every Git
    # repository directly under this folder (one level), so a plan lives in the repository
    # that owns it and work in any other repository can still name it.
    plan_workspace: Path | None = None
    # Names a conflict surface's `repository` may use for this repository (lower case):
    # origin's owner/repo, its repo part, and the main checkout's folder name.
    repository_names: tuple[str, ...] = ()
    # files a systemd unit tracked in this repository runs (ExecStart*), so [Trivial] may not touch them
    running_extra: frozenset[str] = frozenset()


@dataclass
class Verdict:
    verdict: str  # accept | refuse
    tag: str
    reasons: list[str] = field(default_factory=list)
    files: int = 0
    lines: int = 0
    running_things: list[str] = field(default_factory=list)
    check: str = ""  # "plan-adoption" for a plan named but not adopted; lets that check stay observe-only
    scope: list[str] = field(default_factory=list)  # the adopted plan's write surfaces in this repository
    asked: str = ""  # the commit's Asked: line, if any; recorded for review, never changes the verdict
    notes: list[str] = field(default_factory=list)  # logged observations that never change the verdict


def _git(root: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
    if done.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed in {root}: {done.stderr.strip()}")
    return done.stdout


def machine_config_path() -> Path:
    return Path(os.environ.get(MACHINE_CONFIG_ENV) or Path.home() / ".config" / "aes" / "commit_rule.yaml")


def repository_names(root: Path) -> tuple[str, ...]:
    """What a conflict surface's `repository` may say to mean this repository, lower-cased:
    origin's `owner/repo` and `repo`, and the main checkout's folder name (a linked
    worktree's own folder name is not the repository's)."""
    names = []
    url = subprocess.run(["git", "-C", str(root), "remote", "get-url", "origin"],
                         capture_output=True, text=True, check=False).stdout.strip()
    if url:
        parts = re.split(r"[/:]", url.removesuffix(".git").rstrip("/"))
        if len(parts) >= 2 and parts[-1]:
            names += [f"{parts[-2]}/{parts[-1]}", parts[-1]]
    common = subprocess.run(["git", "-C", str(root), "rev-parse", "--path-format=absolute", "--git-common-dir"],
                            capture_output=True, text=True, check=False).stdout.strip()
    if common:
        names.append(Path(common).parent.name)
    return tuple(dict.fromkeys(n.lower() for n in names if n))


def unit_scripts(root: Path) -> frozenset[str]:
    """Tracked files that a systemd unit tracked in this repository runs: every token of an Exec*
    line that ends with a tracked file's path (units name scripts by absolute or %h paths)."""
    try:
        listed = _git(root, "ls-files", "-z").split("\0")
    except (RuntimeError, OSError):
        return frozenset()
    tracked = [f for f in listed if f]
    tokens: set[str] = set()
    for unit in (f for f in tracked if f.endswith(".service")):
        try:
            text = (root / unit).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for line in text.splitlines():
            key, _, value = line.partition("=")
            if key.strip().startswith("Exec"):
                tokens.update(t.strip("'\"") for t in value.split())
    return frozenset(f for f in tracked if not f.endswith(".service")
                     and any(t == f or t.endswith("/" + f) for t in tokens))


def load_rule_config(root: Path) -> RuleConfig:
    path = root / CONFIG_PATH
    if path.is_file():
        data = _YAML.load(path.read_text(encoding="utf-8")) or {}
    else:
        path = machine_config_path()
        if not path.is_file():
            return RuleConfig(plan_roots=(root,), repository_names=repository_names(root), running_extra=unit_scripts(root))
        machine = _YAML.load(path.read_text(encoding="utf-8")) or {}
        override = (machine.get("repos") or {}).get(root.name) or {}
        data = {**{k: v for k, v in machine.items() if k != "repos"}, **override}
    mode = data.get("mode", "observe")
    if mode not in ("observe", "enforce"):
        raise ValueError(f"{path}: mode must be observe or enforce, not {mode!r}")
    plan_adoption = data.get("plan_adoption", mode)
    if plan_adoption not in ("observe", "enforce"):
        raise ValueError(f"{path}: plan_adoption must be observe or enforce, not {plan_adoption!r}")
    extra = tuple((root / p).resolve() if not Path(p).is_absolute() else Path(p)
                  for p in data.get("plan_roots", []))
    return RuleConfig(
        running_extra=unit_scripts(root),
        mode=mode,
        trivial_max_files=int(data.get("trivial_max_files", 3)),
        trivial_max_lines=int(data.get("trivial_max_lines", 60)),
        plan_roots=(root, *extra),
        source=str(path),
        plan_adoption=plan_adoption,
        plan_workspace=Path(data["plan_workspace"]).expanduser() if data.get("plan_workspace") else None,
        repository_names=repository_names(root),
    )


def _parse_changes(numstat: str, name_status: str) -> list[FileChange]:
    statuses: dict[str, str] = {}
    for line in name_status.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            statuses[parts[-1]] = parts[0][:1]
    changes = []
    for line in numstat.splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        added, deleted, path = parts[0], parts[1], parts[-1]
        if " => " in path:  # rename in numstat brace form; name-status holds the new path
            path = next((p for p in statuses if path.endswith(p.rsplit("/", 1)[-1])), path)
        changes.append(FileChange(path=path, status=statuses.get(path, "M"),
                                  added=int(added) if added.isdigit() else 0,
                                  deleted=int(deleted) if deleted.isdigit() else 0))
    return changes


def staged_changes(root: Path) -> list[FileChange]:
    return _parse_changes(_git(root, "diff", "--cached", "--numstat", "--no-renames"),
                          _git(root, "diff", "--cached", "--name-status", "--no-renames"))


def commit_changes(root: Path, rev: str) -> list[FileChange]:
    return _parse_changes(
        _git(root, "show", "--numstat", "--format=", "--no-renames", "--first-parent", "-m", rev),
        _git(root, "show", "--name-status", "--format=", "--no-renames", "--first-parent", "-m", rev),
    )


def running_thing(path: str) -> bool:
    name = path.rsplit("/", 1)[-1]
    if any(fnmatch.fnmatch(name, pattern) for pattern in RUNNING_THING_NAMES):
        return True
    return any(path.startswith(d) or f"/{d}" in f"/{path}" for d in RUNNING_THING_DIRS)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _plan_candidates(plan_root: Path, number: str | None, plan_id: str | None) -> list[Path]:
    if number is not None:
        return [p for p in sorted((plan_root / "docs" / "plans").glob("*.md"))
                if re.match(rf"0*{int(number)}_", p.name)]
    found = []
    for p in sorted(plan_root.glob("proposals/*/*.md")) + sorted(plan_root.glob("docs/plans/*.md")):
        match = FRONT_MATTER_RE.match(p.read_text(encoding="utf-8", errors="replace"))
        if match and (_YAML.load(match.group(1)) or {}).get("plan_id") == plan_id:
            found.append(p)
    return found


def _adoption(read, plan_rel: str, where: str) -> tuple[bool, str, dict]:
    """The adoption check over any byte source: `read(path relative to the plan root)` returns the
    file's bytes or None. `where` names the plan in messages. The third value is the plan's front
    matter (empty when the plan is missing)."""
    text = read(plan_rel)
    if text is None:
        return False, f"{where}: plan file not found", {}
    match = FRONT_MATTER_RE.match(text.decode("utf-8", errors="replace"))
    meta = (_YAML.load(match.group(1)) or {}) if match else {}
    meta = meta if isinstance(meta, dict) else {}
    ok, why = _adoption_of(read, text, meta, where)
    return ok, why, meta


def _adoption_of(read, text: bytes, meta: dict, where: str) -> tuple[bool, str]:
    receipt_ref = meta.get("method_conformance_receipt")
    if not receipt_ref:
        return False, f"{where}: no method_conformance_receipt in front matter (not adopted through Company Planning)"
    # Company Planning's decision_path_for: drop ".json", then a trailing ".receipt"
    head, _, name = str(receipt_ref).rpartition("/")
    decision_ref = (head + "/" if head else "") + name.removesuffix(".json").removesuffix(".receipt") + ".adoption-decision.json"
    receipt, decision = read(str(receipt_ref)), read(decision_ref)
    if receipt is None or decision is None:
        return False, f"{where}: receipt or adoption decision missing ({receipt_ref})"
    record = json.loads(decision.decode("utf-8"))
    if record.get("decision") != "adopted":
        return False, f"{where}: adoption decision is {record.get('decision')!r}, not adopted"
    if record.get("plan_sha256") != hashlib.sha256(text).hexdigest():
        return False, f"{where}: plan changed since adoption; re-adopt it"
    if record.get("receipt_sha256") != hashlib.sha256(receipt).hexdigest():
        return False, f"{where}: receipt changed since adoption"
    return True, f"{where} adopted"


def plan_adoption(plan_root: Path, plan: Path) -> tuple[bool, str]:
    """Whether `plan` declares a Company Planning receipt whose adoption decision is `adopted`
    for the current bytes of both the plan and the receipt; the reason either way."""
    rel = str(plan.relative_to(plan_root)) if plan.is_relative_to(plan_root) else str(plan)

    def read(r: str) -> bytes | None:
        f = plan if r == rel else plan_root / r
        return f.read_bytes() if f.is_file() else None
    ok, why, _meta = _adoption(read, rel, str(plan))
    return ok, (f"{rel} adopted" if ok else why)


def _glob_re(pattern: str) -> re.Pattern[str]:
    out, i = [], 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif pattern[i] == "*":
            out.append("[^/]*")
            i += 1
        elif pattern[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("".join(out))


def in_surface(path: str, target: str) -> bool:
    """Whether `path` lies in a repository_path surface `target`: the same file, anything under
    that directory, or a glob match (`*` and `?` stay within one directory, `**` crosses them)."""
    target = target.strip().removeprefix("./")
    if any(ch in target for ch in "*?"):
        return bool(_glob_re(target).fullmatch(path))
    target = target.rstrip("/")
    return bool(target) and (path == target or path.startswith(target + "/"))


def write_scope(meta: dict, names: tuple[str, ...]) -> list[str]:
    """The plan's `conflict_surfaces` targets this repository may write: Company Planning's
    work-unit `conflictSurface` shape, `kind: repository_path`, `access: write | exclusive`, and a
    `repository` that names this repository. Other entries (read access, other kinds, other
    repositories, malformed ones) grant nothing."""
    out = []
    surfaces = meta.get("conflict_surfaces")
    for s in surfaces if isinstance(surfaces, list) else []:
        if not isinstance(s, dict) or s.get("kind") != "repository_path" or s.get("access") not in ("write", "exclusive"):
            continue
        if str(s.get("repository", "")).strip().lower() not in names:
            continue
        if isinstance(s.get("target"), str) and s["target"].strip():
            out.append(s["target"].strip())
    return out


def adopted_write_scopes(plan_roots: tuple[Path, ...], names: tuple[str, ...]) -> list[str]:
    """Write surfaces for this repository of every adopted plan under `plan_roots`
    (`docs/plans/*.md`, `proposals/*/*.md`). Only plans whose front matter mentions
    `conflict_surfaces` are parsed and checked."""
    out: list[str] = []
    for plan_root in plan_roots:
        for plan in sorted(plan_root.glob("docs/plans/*.md")) + sorted(plan_root.glob("proposals/*/*.md")):
            try:
                text = plan.read_bytes()
            except OSError:
                continue
            match = FRONT_MATTER_RE.match(text.decode("utf-8", errors="replace"))
            if not match or "conflict_surfaces" not in match.group(1):
                continue
            try:
                meta = _YAML.load(match.group(1)) or {}
            except Exception:  # a malformed plan grants no scope; its own [Plan #N] commits say why
                continue
            if not isinstance(meta, dict):
                continue

            def read(r: str, _root: Path = plan_root) -> bytes | None:
                f = _root / r
                return f.read_bytes() if f.is_file() else None
            ok, _why = _adoption_of(read, text, meta, str(plan))
            if ok:
                out += write_scope(meta, names)
    return out


def workspace_plan_roots(workspace: Path, plan_id: str, skip: tuple[Path, ...] = ()) -> list[Path]:
    """Repositories directly under `workspace` holding a plan whose front matter names `plan_id`.

    A cheap text test picks the candidate files before any YAML is parsed; the whole
    workspace (about 1,700 plan files in ~/code) scans in well under a second."""
    needle = re.compile(rf"^plan_id:\s*['\"]?{re.escape(plan_id)}['\"]?\s*$", re.MULTILINE)
    skipped = {s.resolve() for s in skip}
    roots = []
    for repo in sorted(workspace.iterdir()) if workspace.is_dir() else []:
        if not (repo / ".git").exists() or repo.resolve() in skipped:
            continue
        for p in [*repo.glob("proposals/*/*.md"), *repo.glob("docs/plans/*.md")]:
            try:
                with p.open(encoding="utf-8", errors="replace") as fh:
                    head = fh.read(8192)
            except OSError:
                continue
            match = FRONT_MATTER_RE.match(head)
            if match and needle.search(match.group(1)):
                roots.append(repo)
                break
    return roots


PLAN_INDEX_ENV = "AES_PLAN_INDEX"
PLAN_INDEX_FRESH_SECONDS = 3600
DEFAULT_REFS = ("origin/HEAD", "origin/main", "origin/master", "main", "master")


def plan_index_path() -> Path:
    return Path(os.environ.get(PLAN_INDEX_ENV) or Path.home() / ".cache" / "aes" / "plan-index.json")


def _default_ref(repo: Path) -> tuple[str, str] | None:
    for ref in DEFAULT_REFS:
        done = subprocess.run(["git", "-C", str(repo), "rev-parse", "-q", "--verify", f"{ref}^{{commit}}"],
                              capture_output=True, text=True, check=False)
        if done.returncode == 0 and done.stdout.strip():
            return ref, done.stdout.strip()
    return None


def build_plan_index(workspace: Path, path: Path | None = None) -> dict:
    """Which plan ids each repository directly under `workspace` holds on its default branch (read
    through git, not its working tree, which may sit on another branch). Incremental: a repository
    whose default-branch commit is unchanged keeps its previous entry, so only moved repositories are
    re-read (a full rebuild over ~/code takes about 20 s, a refresh a few)."""
    path = path or plan_index_path()
    try:
        old = json.loads(path.read_text(encoding="utf-8")).get("repos", {})
    except (OSError, ValueError):
        old = {}
    repos: dict[str, dict] = {}
    errors: list[str] = []
    for repo in sorted(workspace.iterdir()) if workspace.is_dir() else []:
        if not (repo / ".git").exists():
            continue
        found = _default_ref(repo)
        if found is None:
            continue
        ref, sha = found
        key = str(repo.resolve())
        if old.get(key, {}).get("sha") == sha:
            repos[key] = old[key]
            continue
        grep = subprocess.run(["git", "-C", str(repo), "grep", "-E", r"^plan_id:", sha, "--",
                               "proposals/*/*.md", "docs/plans/*.md"], capture_output=True, text=True, check=False)
        if grep.returncode > 1:
            # exit 1 is "no match"; 2+ is an error. Leave the repository out so the next build retries
            # it, instead of caching "no plans" under this commit until its main moves.
            errors.append(f"{repo.name}: git grep exit {grep.returncode}: {grep.stderr.strip()[-200:]}")
            continue
        plans: dict[str, list[str]] = {}
        for line in grep.stdout.splitlines():
            # "<sha>:<path>:plan_id: <id>"
            parts = line.split(":", 3)
            if len(parts) == 4:
                pid = parts[3].strip().strip("'\"")
                if pid:
                    plans.setdefault(pid, []).append(parts[1])
        repos[key] = {"ref": ref, "sha": sha, "plans": plans}
    index = {"built_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
             "workspace": str(workspace), "repos": repos, "errors": errors}
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")  # concurrent builders never share a temp file
    tmp.write_text(json.dumps(index, indent=1) + "\n", encoding="utf-8")
    tmp.replace(path)
    path.with_name(path.name + ".refreshing").unlink(missing_ok=True)  # releases the background-refresh lock
    return index


def _refresh_index_in_background(workspace: Path) -> None:
    """Start an index rebuild that outlives this commit; the next commit reads its result.
    AES_PLAN_INDEX_REFRESH=0 turns this off (tests build the index explicitly)."""
    if os.environ.get("AES_PLAN_INDEX_REFRESH") == "0":
        return
    # One rebuild at a time: a rebuild takes 12-18 s, and every commit that misses a plan meanwhile
    # would otherwise start another. The lock is ignored once older than ten minutes (a crashed rebuild).
    lock = plan_index_path().with_name(plan_index_path().name + ".refreshing")
    try:
        lock.parent.mkdir(parents=True, exist_ok=True)
        if lock.exists() and dt.datetime.now().timestamp() - lock.stat().st_mtime < 600:
            return
        lock.unlink(missing_ok=True)
        os.close(os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
    except FileExistsError:
        return
    except OSError:
        pass
    try:
        subprocess.Popen([sys.executable, "-m", "agentic_engineering_system.cli", "commit", "index",
                          "--workspace", str(workspace)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True)
    except OSError:
        pass


def indexed_adoption(workspace: Path, plan_id: str) -> tuple[list[tuple[bool, str, dict]], bool]:
    """Judge `plan_id` from each repository's default branch as recorded in the plan index.
    Returns the per-candidate verdicts and whether the index was missing or stale (and so a
    background refresh was started)."""
    path = plan_index_path()
    try:
        index = json.loads(path.read_text(encoding="utf-8"))
        age = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(index["built_at"])).total_seconds()
    except (OSError, ValueError, KeyError):
        index, age = {"repos": {}}, float("inf")
    stale = age > PLAN_INDEX_FRESH_SECONDS or index.get("workspace") != str(workspace)
    verdicts = []
    for repo, entry in index.get("repos", {}).items():
        for rel in entry.get("plans", {}).get(plan_id, []):
            sha = entry["sha"]

            def read(r: str, _repo: str = repo, _sha: str = sha) -> bytes | None:
                done = subprocess.run(["git", "-C", _repo, "show", f"{_sha}:{r}"], capture_output=True, check=False)
                return done.stdout if done.returncode == 0 else None
            ok, why, meta = _adoption(read, rel, f"{Path(repo).name} {entry['ref']}:{rel}")
            verdicts.append((ok, why, meta))
    if stale:
        _refresh_index_in_background(workspace)
    return verdicts, stale


def receipt_status(plan_roots: tuple[Path, ...], number: str | None, plan_id: str | None,
                   plan_workspace: Path | None = None) -> tuple[bool, str]:
    """Whether the named plan has a current adopted Company Planning receipt, and why not.

    [Plan #N] numbers are per repository, so only a [Goal <id>] is looked up across the
    workspace, and only when no plan root holds it."""
    ok, why, _meta = adopted_plan(plan_roots, number, plan_id, plan_workspace)
    return ok, why


def adopted_plan(plan_roots: tuple[Path, ...], number: str | None, plan_id: str | None,
                 plan_workspace: Path | None = None) -> tuple[bool, str, dict]:
    """`receipt_status`, plus the adopted plan's front matter (empty unless adopted)."""
    label = f"#{number}" if number is not None else plan_id
    plans = [(r, p) for r in plan_roots for p in _plan_candidates(r, number, plan_id)]
    searched = [str(r) for r in plan_roots]
    if not plans and plan_id is not None and plan_workspace is not None:
        for repo in workspace_plan_roots(plan_workspace, plan_id, plan_roots):
            plans += [(repo, p) for p in _plan_candidates(repo, None, plan_id)]
        searched.append(f"every repository in {plan_workspace}")
    if not plans and (plan_id is None or plan_workspace is None):
        return False, f"no plan {label} found under {', '.join(searched)}", {}
    reasons = [] if plans else [f"no plan {label} found under {', '.join(searched)}"]
    for plan_root, plan in plans:
        rel = str(plan.relative_to(plan_root)) if plan.is_relative_to(plan_root) else str(plan)

        def read(r: str, _plan: Path = plan, _rel: str = rel, _root: Path = plan_root) -> bytes | None:
            f = _plan if r == _rel else _root / r
            return f.read_bytes() if f.is_file() else None
        ok, why, meta = _adoption(read, rel, str(plan))
        if ok:
            return True, f"plan {label} adopted ({plan.relative_to(plan_root)})", meta
        reasons.append(why)
    if plan_id is not None and plan_workspace is not None:
        # A checkout may sit on another branch or behind main: judge each repository's default
        # branch too, from the plan index (rebuilt daily and in the background when stale).
        verdicts, stale = indexed_adoption(plan_workspace, plan_id)
        for ok, why, meta in verdicts:
            if ok:
                return True, f"plan {label} adopted on the default branch ({why.removesuffix(' adopted')})", meta
            reasons.append(why)
        if stale:
            reasons.append("plan index missing or older than an hour; a refresh was started")
    return False, "; ".join(reasons), {}


QUICK_FILE_RE = re.compile(r"^- `([^`]+)`\s*$", re.MULTILINE)


def _plan_text(config: RuleConfig, plan_id: str) -> tuple[Path, str, str] | None:
    """(repository, plan path relative to it, text) of the named plan: the plan roots and the
    workspace checkouts first, then each repository's default branch from the plan index."""
    roots = list(config.plan_roots)
    if config.plan_workspace is not None:
        roots += workspace_plan_roots(config.plan_workspace, plan_id, config.plan_roots)
    for root in roots:
        for plan in _plan_candidates(root, None, plan_id):
            return root, str(plan.relative_to(root)), plan.read_text(encoding="utf-8", errors="replace")
    if config.plan_workspace is not None:
        try:
            index = json.loads(plan_index_path().read_text(encoding="utf-8"))
        except (OSError, ValueError):
            index = {}
        for repo, entry in index.get("repos", {}).items():
            for rel in entry.get("plans", {}).get(plan_id, []):
                done = subprocess.run(["git", "-C", repo, "show", f"{entry['sha']}:{rel}"],
                                      capture_output=True, text=True, check=False)
                if done.returncode == 0:
                    return Path(repo), rel, done.stdout
    return None


def quick_plan_notes(plan_id: str, changes: list[FileChange], config: RuleConfig) -> list[str]:
    """For a plan made by Company Planning's quick-adopt (front matter `planning_path: requested`):
    whether the commit's changes stay inside the plan's file list (its Vertical and reset section, plus
    the plan's own folder and AES evidence records) and whether the plan's saved check output
    (`<plan folder>/<id>.check.txt`) is present. Notes only: they never change the verdict."""
    found = _plan_text(config, plan_id)
    if found is None:
        return []
    repo, rel, text = found
    match = FRONT_MATTER_RE.match(text)
    meta = (_YAML.load(match.group(1)) or {}) if match else {}
    if meta.get("planning_path") != "requested":
        return []
    folder = rel.rsplit("/", 1)[0] if "/" in rel else ""
    section = text.split("## Vertical and reset", 1)[1].split("\n## ", 1)[0] if "## Vertical and reset" in text else ""
    listed = set(QUICK_FILE_RE.findall(section))
    same_repo = bool(config.plan_roots) and repo.resolve() == config.plan_roots[0].resolve()
    check_rel = f"{folder}/{plan_id}.check.txt" if folder else f"{plan_id}.check.txt"
    staged = {c.path for c in changes if c.status != "D"}
    outside = sorted(p for p in staged if p not in listed and not p.startswith(".aes/observations/")
                     and not (same_repo and folder and p.startswith(folder + "/")))
    present = (same_repo and check_rel in staged) or (repo / check_rel).is_file()
    notes = [f"quick plan {plan_id}: saved check output {check_rel} " + ("present" if present else "missing")]
    notes.append(f"quick plan {plan_id}: files outside the plan's list: {', '.join(outside)}" if outside
                 else f"quick plan {plan_id}: every changed file is in the plan's list")
    return notes


def judge(message: str, changes: list[FileChange], governed_roots: list[str], config: RuleConfig,
          legacy: frozenset[str] = frozenset()) -> Verdict:
    """The tag's verdict (with the legacy-edit check), plus notes for a quick-adopt plan."""
    v = _judge_with_legacy(message, changes, governed_roots, config, legacy)
    goal = TAG_RE.match(message.lstrip().splitlines()[0] if message.strip() else "")
    if goal and goal["goal"] and v.verdict == "accept":
        try:
            v.notes = quick_plan_notes(goal["goal"], changes, config)
        except (OSError, ValueError, RuntimeError) as err:  # a note must never break a commit
            v.notes = [f"quick plan check skipped: {type(err).__name__}: {err}"]
    return v


def _judge_with_legacy(message: str, changes: list[FileChange], governed_roots: list[str], config: RuleConfig,
                       legacy: frozenset[str] = frozenset()) -> Verdict:
    """The tag's verdict, then the adopted repository's legacy-edit check (`adopt`). An `Asked:` line is
    recorded on the verdict either way and never changes it: being asked does not make large work trivial."""
    asked = ASKED_RE.search(message)
    v = _judge_tag(message, changes, governed_roots, config)
    v.asked = asked.group(1).strip()[:300] if asked else ""
    edited = sorted(c.path for c in changes if c.status in ("M", "T") and c.path in legacy)
    if not edited or v.tag == "git" or (v.tag == "Unplanned" and v.verdict == "accept"):
        return v
    named_plan = v.check == "plan-adoption"
    if named_plan and v.verdict == "accept":
        inside = [p for p in edited if any(in_surface(p, t) for t in v.scope)]
        if inside:
            v.reasons.append(f"legacy edit inside {v.tag}'s declared conflict_surfaces: {', '.join(inside)}")
        edited = [p for p in edited if p not in inside]
        if not edited:
            return v
    reason = (f"unplanned legacy edit: {', '.join(edited)} still in .aes/legacy_baseline.json and planned by no "
              f"target artifact; plan the file first (aes plan accept removes it from the baseline)")
    if named_plan:
        reason += (f", or declare it in {v.tag}'s front matter conflict_surfaces (kind: repository_path, "
                   f"repository, target, access: write) and re-adopt the plan")
    return Verdict("refuse", v.tag, (v.reasons if v.verdict == "refuse" else []) + [reason],
                   v.files, v.lines, v.running_things, check="legacy-edit", scope=v.scope, asked=v.asked)


def _judge_tag(message: str, changes: list[FileChange], governed_roots: list[str], config: RuleConfig) -> Verdict:
    first = message.lstrip().splitlines()[0] if message.strip() else ""
    files = len(changes)
    lines = sum(c.added + c.deleted for c in changes)
    running = sorted(c.path for c in changes if running_thing(c.path) or c.path in config.running_extra)

    def verdict(result: str, tag: str, reason: str) -> Verdict:
        return Verdict(result, tag, [reason], files, lines, running)

    if first.startswith(GIT_OWN_PREFIXES):
        return verdict("accept", "git", "git's own merge/fixup/squash message")
    match = TAG_RE.match(first)
    if not match:
        return verdict("refuse", "none",
                       "no tag: start the first line with [Plan #N], [Goal <id>], [Trivial], [Unplanned], [Auto] or [Shaping <id>]")
    if match["plan"] is not None or match["goal"] is not None:
        tag = f"Plan #{match['plan']}" if match["plan"] is not None else f"Goal {match['goal']}"
        ok, why, meta = adopted_plan(config.plan_roots, match["plan"], match["goal"], config.plan_workspace)
        result = verdict("accept" if ok else "refuse", tag, why)
        result.check = "plan-adoption"
        result.scope = write_scope(meta, config.repository_names) if ok else []
        return result
    if match["trivial"]:
        problems = []
        if files > config.trivial_max_files:
            problems.append(f"{files} files (trivial allows {config.trivial_max_files})")
        if lines > config.trivial_max_lines:
            problems.append(f"{lines} changed lines (trivial allows {config.trivial_max_lines})")
        added_governed = sorted(c.path for c in changes if c.status == "A"
                                and any(c.path.startswith(r) for r in governed_roots))
        if added_governed:
            problems.append(f"adds file(s) under a governed root: {', '.join(added_governed)}")
        if running:
            problems.append(f"touches running-thing file(s): {', '.join(running)}")
        if problems:
            return verdict("refuse", "Trivial", "not trivial: " + "; ".join(problems) + "; plan it ([Plan #N] or [Goal <id>])")
        return verdict("accept", "Trivial", f"trivial: {files} file(s), {lines} line(s), no running-thing file")
    if match["unplanned"]:
        if NO_EMERGENCY_RE.search(message) and not any(
                not NO_EMERGENCY_RE.match(line) for line in EMERGENCY_LINE_RE.findall(message)):
            return verdict("refuse", "Unplanned", "[Unplanned] is for emergencies, and the Emergency: line says there "
                           "is none; plan it in about 10 s with Company Planning's `quick-adopt` and tag [Goal <id>], "
                           "or use [Trivial] for at most 3 files and 60 lines that touch nothing that runs")
        if EMERGENCY_RE.search(message):
            return verdict("accept", "Unplanned", "emergency recorded (Emergency: line present); logged for review")
        why = "[Unplanned] is for emergencies: add an 'Emergency: <reason>' line"
        if running:
            why += f"; this change touches running-thing file(s) {', '.join(running)} and needs a plan ([Plan #N] or [Goal <id>])"
        return verdict("refuse", "Unplanned", why)
    if match["auto"]:
        job = AUTO_JOB_RE.search(message)
        if not job:
            return verdict("refuse", "Auto", "[Auto] is for scheduled jobs: add an 'Auto-job: <job name>' line")
        if running:
            return verdict("refuse", "Auto", f"[Auto] may not touch running-thing file(s) {', '.join(running)}; plan it ([Plan #N] or [Goal <id>])")
        return verdict("accept", "Auto", f"scheduled job {job.group(1).strip()}: {files} file(s), {lines} line(s)")
    plan_id = match["shaping"]
    outside = sorted(c.path for c in changes if not c.path.startswith(f"proposals/{plan_id}/"))
    if outside:
        return verdict("refuse", f"Shaping {plan_id}", f"[Shaping {plan_id}] may touch only proposals/{plan_id}/; also touches {', '.join(outside)}")
    return verdict("accept", f"Shaping {plan_id}", f"drafting plan {plan_id} inside proposals/{plan_id}/")


def _governed_roots(root: Path) -> list[str]:
    try:
        return list(load_project(root / ".aes" / "project.yaml").governed_roots)
    except (OSError, ValueError):
        return []


def _legacy(root: Path, *, released: bool = True) -> frozenset[str]:
    """Legacy baseline paths the target does not plan, minus (with `released`) those an adopted
    plan's scope released (`adopt.unplanned_legacy`); empty outside an adopted AES project. The
    pre-commit hook has already refused a target that does not load, so a load error here is raised."""
    from .adopt import legacy_paths, unplanned_legacy

    if not (root / ".aes" / "project.yaml").is_file():
        return frozenset()
    return unplanned_legacy(root) if released else legacy_paths(root)


def _log(root: Path, entry: dict) -> Path:
    common = Path(_git(root, "rev-parse", "--git-common-dir").strip())
    log_dir = (common if common.is_absolute() else root / common) / "aes"
    log_dir.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc)
    path = log_dir / f"commit-rule-{now.date().isoformat()}.jsonl"
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"at": now.isoformat(timespec="seconds"), **entry}) + "\n")
    return path


def check_message(root: Path, message_file: Path) -> tuple[int, str]:
    """Judge the commit being made; return (exit status, report). Observe mode never refuses."""
    root = root.resolve()
    config = load_rule_config(root)
    message = "\n".join(l for l in message_file.read_text(encoding="utf-8").splitlines() if not l.startswith("#"))
    verdict = judge(message, staged_changes(root), _governed_roots(root), config, _legacy(root))
    log = _log(root, {"mode": config.mode, "config": config.source, "subject": message.strip().splitlines()[0] if message.strip() else "",
                      **asdict(verdict)})
    word = (verdict.verdict if verdict.verdict == "accept"
            else "would refuse (observe mode)" if config.mode != "enforce"
            else "would refuse (plan adoption is observe-only)" if verdict.check == "plan-adoption" and config.plan_adoption == "observe"
            else "refuse")
    asked = f"; asked: {verdict.asked}" if verdict.asked else ""
    notes = "".join(f"; {n}" for n in verdict.notes)
    report = f"aes commit rule: {word} [{verdict.tag}] — {'; '.join(verdict.reasons)}{asked}{notes} (logged to {log})"
    soft = verdict.check == "plan-adoption" and config.plan_adoption == "observe"
    blocked = config.mode == "enforce" and verdict.verdict == "refuse" and not soft
    return (1 if blocked else 0), report


def replay(root: Path, revisions: str = "HEAD", max_count: int = 300) -> tuple[list[tuple[str, str, Verdict]], dict[str, int]]:
    """Judge past commits (non-merge, first-parent order) with today's rule and today's receipts.
    Legacy is today's baseline without the scope release: a file the replayed commits themselves
    changed is still judged against the plan each commit names."""
    root = root.resolve()
    config = load_rule_config(root)
    governed = _governed_roots(root)
    legacy = _legacy(root, released=False)
    out = _git(root, "log", "--no-merges", f"--max-count={max_count}", "--format=%H%x00%B%x01", revisions)
    rows = []
    for record in out.split("\x01"):
        if "\x00" not in record:
            continue
        sha, body = record.strip("\n").split("\x00", 1)
        verdict = judge(body, commit_changes(root, sha), governed, config, legacy)
        rows.append((sha, body.strip().splitlines()[0] if body.strip() else "", verdict))
    counts: dict[str, int] = {"commits": len(rows), "accept": 0, "refuse": 0}
    for _, _, v in rows:
        counts[v.verdict] += 1
        counts[f"tag:{v.tag.split(' ')[0]}"] = counts.get(f"tag:{v.tag.split(' ')[0]}", 0) + 1
    return rows, counts

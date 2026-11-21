#!/usr/bin/env python3
"""Remove finished git worktrees (lanes) and report the rest.

Implements: lane-sweep/remove-finished-lanes-and-report-the-rest, lane-sweep/keep-lanes-git-will-not-remove-without-force,
    lane-sweep/fast-forward-primary-checkouts-that-are-clean-and-idle,
    lane-sweep/keep-lanes-that-a-systemd-user-unit-runs-from, lane-sweep/keep-locked-worktrees
Implements: lane-sweep/settings-come-from-config, lane-sweep/archive-then-remove-idle-unmerged-lanes,
    lane-sweep/count-kept-lanes-per-repository

A lane is removed, with its local branch, only when every check passes:
- the tree has no uncommitted changes (ignored files do not count);
- its content is on the remote default branch: the tip is an ancestor of it, or
  every file the branch changed has the same content there (squash merges), or a merged
  pull request's head is exactly this tip (GitHub, through the gh wrapper `github_accounts:` in
  graph-config.yaml names for the repository's owner, else for `owner:`, else plain `gh`);
- no running process outside this sweep's ancestors and session uses it: its working directory, an
  argument, an open or mapped file, a code search path in its environment (PYTHONPATH, VIRTUAL_ENV and
  similar) or a .pth file of the virtual environment it runs from points inside it;
- no systemd user unit names it: a unit file, or a drop-in, in ~/.config/systemd/user, the transient folder
  `systemd-run --user --on-calendar` writes to ($XDG_RUNTIME_DIR/systemd/transient) or the other user-unit
  folders, with its path in WorkingDirectory, ExecStart, Environment or any other line (a pending timer's job
  is no process until it starts, code2-workspace#76);
- it has been idle 30 minutes, or 24 hours when the branch has no commits of its own; a lane
  passed as --merged-lane (ship, right after its pull request merged) skips only this wait;
- its ignored files that are not regenerable caches (anything under .venv, node_modules, __pycache__, build,
  dist, .cache and the other REBUILDABLE names) total under 1 MiB; otherwise it is kept with the reason
  "holds ignored non-cache files: <up to 5 paths>", since `git worktree remove` deletes ignored files.
A lane whose content is not on the remote default branch, and that passes every other check, is archived and
its worktree removed once it has been idle 72 hours (`lane_sweep_archive_after_hours:` in graph-config.yaml;
0 turns this off; the ignored-files check above applies too): unless a remote branch already holds the tip, the local ref refs/archive/<YYYYMMDD>/<lane>
is created at it, a `git bundle` of that ref (only the commits not on the default branch) is written beside the
day's log and verified, and the ref is pushed to origin only when origin's owner is the `owner:` setting and
GitHub reports the repository private. Then only the worktree is removed; the local branch stays. The log names
branch, tip, bundle and the `git worktree add` command that restores the lane. A failed verify keeps the lane.
A lane passed as --keep-lane (ship --keep-lane) is always kept. So is a worktree locked with
`git worktree lock`: that is how a tool marks a worktree that is not a lane, such as a pinned checkout
another project's environment imports from, which by every check above looks like a finished lane.
Everything else is kept and listed with its reason. Each removal appends the branch,
its tip and the restoring `git branch <name> <tip>` command to one log file per day.
Removal moves the lane aside to `.<name>.lane-sweep-removing` first, so its own path disappears in one
step, then runs `git worktree remove` without --force. A failure with the tree intact moves it back; a
failure after deleting files leaves the remains at the hidden path, keeps the branch and logs the command
that recreates the lane. A git command that times out is a failed step, never a crash.
Without --apply nothing changes. Worktree records whose folder is gone are pruned.

Then each repository's primary checkout (the main worktree) is fast-forwarded to the remote default
branch with `git merge --ff-only`, never reset or rebase, when it is on that branch, has no
uncommitted changes, is strictly behind it, holds no index.lock, and no process outside this sweep works in it (processes
inside a lane nested in the checkout do not count). Each fast-forward logs the old and new commit;
a checkout left behind is listed with its reason.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

IDLE_MINUTES = 30
IDLE_MINUTES_NO_COMMITS = 24 * 60
# An unmerged lane idle this long is archived (ref + verified bundle) and its worktree removed, branch kept.
# 2026-11-19: 136 lanes held about 23 GB under ~/code2, 47 of them unmerged and untouched since one fan-out day
# on 2026-11-13; the sweep kept every one ("work not on origin/main"), so they were removed by hand.
ARCHIVE_IDLE_HOURS = 72.0
# A repository keeping more lanes than this is marked in the per-repository count line.
MANY_LANES = 8
REMOVE_TIMEOUT = 600
ASIDE_SUFFIX = ".lane-sweep-removing"
# A primary checkout that canonical_lock.py made read-only (a lane claim is live) moves only through that
# tool's --sync, which unlocks, pulls --ff-only and re-locks; a plain merge fails on the read-only folders
# (2026-11-05: process_tracing, "unable to unlink old 'docs/CONCERNS.md': Permission denied").
# Its path is the `canonical_lock:` setting (none named: every checkout moves with a plain merge).
# Settings are read when needed, never at import: ship runs this after every merge, and a machine without
# the configuration still sweeps.
CONFIG = Path(os.environ.get("PROJECT_GRAPH") or Path.home() / "code2/aes-config/PROJECT_GRAPH.json").parent / "graph-config.yaml"


def config_text() -> str:
    """The text of graph-config.yaml beside the project graph, or "" when there is none."""
    try:
        return CONFIG.read_text(encoding="utf-8")
    except OSError:
        return ""


def setting(key: str, env: str) -> str | None:
    """One value from the environment, else top-level `key:` in graph-config.yaml, else None."""
    named = os.environ.get(env)
    if named:
        return named
    found = re.search(rf"^{re.escape(key)}:[ \t]*([^\s#]+)", config_text(), re.M)
    return found.group(1) if found else None


def github_accounts() -> dict[str, str]:
    """The `github_accounts:` block of graph-config.yaml: GitHub account to the gh wrapper that can read it."""
    block = re.search(r"^github_accounts:[^\n]*\n((?:[ \t]+[^\n]*\n?)*)", config_text(), re.M)
    pairs = re.findall(r"^[ \t]+([^\s:#]+):[ \t]*([^\s#]+)", block.group(1), re.M) if block else []
    return dict(pairs)


def gh_for(slug: str) -> str:
    """The gh command for a repository: LANE_SWEEP_GH, else the wrapper for its owner, else for `owner:`, else gh."""
    named = os.environ.get("LANE_SWEEP_GH")
    if named:
        return named
    accounts = github_accounts()
    return accounts.get(slug.split("/", 1)[0]) or accounts.get(setting("owner", "PROJECT_GRAPH_OWNER") or "") or "gh"


def archive_idle_hours() -> float:
    """Hours an unmerged lane must be idle before it is archived and removed (0 or less: never)."""
    named = setting("lane_sweep_archive_after_hours", "LANE_SWEEP_ARCHIVE_AFTER_HOURS")
    try:
        return float(named) if named else ARCHIVE_IDLE_HOURS
    except ValueError:
        return ARCHIVE_IDLE_HOURS


def canonical_lock() -> Path | None:
    """The canonical-lock tool named by `canonical_lock:` (or LANE_SWEEP_CANONICAL_LOCK), or None."""
    named = setting("canonical_lock", "LANE_SWEEP_CANONICAL_LOCK")
    return Path(named).expanduser() if named else None


# Environment variables whose folders a process loads code from; a lane named in one is in use even when
# the process holds none of its files open (Python reads a .py file and closes it).
CODE_PATH_VARS = ("PYTHONPATH", "VIRTUAL_ENV", "PYTHONHOME", "PYTHONSTARTUP", "PYTHONUSERBASE", "UV_PROJECT",
                  "UV_PROJECT_ENVIRONMENT", "NODE_PATH", "PERL5LIB", "RUBYLIB", "CLASSPATH", "LD_LIBRARY_PATH")


@dataclass
class Lane:
    """One linked worktree as `git worktree list --porcelain` reports it."""

    path: Path
    head: str
    branch: str | None
    locked: bool
    prunable: bool
    lock_reason: str = ""


def git(repo: Path, *args: str, timeout: int = 60, env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    """Run git in repo and return the completed process without raising."""
    # --no-optional-locks keeps `git status` from rewriting the index, whose age is the idle signal.
    cmd = ["git", "--no-optional-locks", "-C", str(repo), *args]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        # A timeout is a failed step for the caller to report, never a crash that skips the summary.
        return subprocess.CompletedProcess(cmd, 124, "", f"timed out after {timeout} seconds")


def lanes(repo: Path) -> list[Lane]:
    """List the linked worktrees of repo, skipping the main checkout."""
    out = git(repo, "worktree", "list", "--porcelain").stdout
    found: list[Lane] = []
    for block in out.strip().split("\n\n")[1:]:
        fields = dict((line.split(" ", 1) + [""])[:2] for line in block.splitlines())
        branch = fields.get("branch", "").removeprefix("refs/heads/") or None
        found.append(Lane(Path(fields["worktree"]), fields.get("HEAD", ""), branch, "locked" in fields, "prunable" in fields,
                          fields.get("locked", "").strip()))
    return found


def default_branch(repo: Path) -> str | None:
    """Return the remote default branch as origin/<name>, or None when there is none."""
    ref = git(repo, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
    if ref.returncode == 0 and ref.stdout.strip():
        return ref.stdout.strip()
    for name in ("origin/main", "origin/master"):
        if git(repo, "rev-parse", "--verify", "-q", name).returncode == 0:
            return name
    return None


def content_on(repo: Path, tip: str, base: str) -> bool:
    """True when tip is an ancestor of base, or every file tip changed has the same content on base."""
    if git(repo, "merge-base", "--is-ancestor", tip, base).returncode == 0:
        return True
    fork = git(repo, "merge-base", tip, base)
    if fork.returncode != 0:
        return False
    changed = git(repo, "diff", "--name-only", "--no-renames", "-z", fork.stdout.strip(), tip)
    if changed.returncode != 0:
        return False
    paths = [p for p in changed.stdout.split("\0") if p]
    # One call compares every changed file between tip and base; exit 0 means identical content.
    return not paths or git(repo, "diff", "--quiet", "--no-renames", tip, base, "--", *paths).returncode == 0


def github_slug(repo: Path) -> str | None:
    """owner/name of origin when it is a GitHub URL (raw config value, before insteadOf rewriting)."""
    url = git(repo, "config", "--get", "remote.origin.url").stdout.strip()
    m = re.search(r"github[^:/]*[:/]([^/:]+)/([^/]+?)(?:\.git)?$", url)
    return f"{m.group(1)}/{m.group(2)}" if m else None


def merged_pr_at(repo: Path, branch: str | None, tip: str) -> int | None:
    """Number of a merged pull request whose head commit is tip, or None.

    This is the core.md merged-PR rule: GitHub keeps the head of a merged pull request, so a lane at
    that exact commit holds nothing the merge did not take, even after main later changed its files.
    """
    slug = github_slug(repo)
    if not slug or not branch:
        return None
    gh = gh_for(slug)
    try:
        out = subprocess.run([gh, "pr", "list", "-R", slug, "--head", branch, "--state", "merged",
                              "--json", "number,headRefOid"], capture_output=True, text=True, timeout=30)
        prs = json.loads(out.stdout or "[]") if out.returncode == 0 else []
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None
    return next((p["number"] for p in prs if p.get("headRefOid") == tip), None)


def own_ancestors() -> set[int]:
    """Process ids of this process and every parent up to init."""
    pids, pid = set(), os.getpid()
    while pid > 1 and pid not in pids:
        pids.add(pid)
        try:
            stat = Path(f"/proc/{pid}/stat").read_text()
            pid = int(stat.rsplit(")", 1)[1].split()[1])
        except (OSError, ValueError, IndexError):
            break
    return pids


def _pth_paths(venv: Path, cache: dict[Path, list[str]]) -> list[str]:
    """Absolute paths named in the .pth files of a virtual environment (editable installs), cached per sweep step."""
    if venv not in cache:
        found: list[str] = []
        for pth in venv.glob("lib/python*/site-packages/*.pth"):
            try:
                found += [line.strip() for line in pth.read_text(errors="replace").splitlines() if line.startswith("/")]
            except OSError:
                continue
        cache[venv] = found
    return cache[venv]


def _uses(entry: Path, pth_cache: dict[Path, list[str]] | None = None) -> list[str]:
    """Paths a process uses: working directory, arguments, open and mapped files, code search paths.

    The working directory alone misses a run started elsewhere that executes code from the lane, such as
    `<lane>/.venv/bin/python <lane>/script.py` (code2-workspace#65). Open and mapped files miss Python
    imports, which read a file and close it: the 2026-10-27 greer runs reached their lanes only through
    PYTHONPATH, or an editable install's .pth file, so those count too.
    """
    pth_cache = {} if pth_cache is None else pth_cache
    paths = [os.readlink(entry / "cwd")]
    args: list[str] = []
    try:
        args = (entry / "cmdline").read_bytes().decode(errors="replace").split("\0")
    except OSError:
        pass
    for a in args:
        if a.startswith("/"):
            paths.append(a)
        elif a.startswith("-") and "=/" in a:  # --project=/path
            paths.append(a.split("=", 1)[1])
    try:
        for item in (entry / "environ").read_bytes().split(b"\0"):
            name, _, value = item.decode(errors="replace").partition("=")
            if name in CODE_PATH_VARS:
                paths += [v for v in value.split(os.pathsep) if v.startswith("/")]
    except OSError:
        pass
    try:
        for fd in (entry / "fd").iterdir():
            try:
                paths.append(os.readlink(fd))
            except OSError:
                continue
    except OSError:
        pass
    try:
        paths += [line.split(None, 5)[5] for line in (entry / "maps").read_text(errors="replace").splitlines() if len(line.split(None, 5)) == 6]
    except OSError:
        pass
    # The virtual environments the process runs from: its interpreter's folder, VIRTUAL_ENV, or the prefix
    # of a site-packages file it mapped. Their .pth files name the source folders of editable installs.
    venvs: set[Path] = set()
    if args and args[0].startswith("/"):
        venvs.add(Path(args[0]).parent.parent)
    for p in paths:
        if "/lib/python" in p:
            venvs.add(Path(p.split("/lib/python", 1)[0]))
        elif (Path(p) / "pyvenv.cfg").is_file():
            venvs.add(Path(p))
    for venv in venvs:
        if (venv / "pyvenv.cfg").is_file():
            paths += _pth_paths(venv, pth_cache)
    return paths


def busy(path: Path, ignore: set[int], exclude: tuple[Path, ...] = ()) -> int | None:
    """Return the id of a process using a path inside path: working directory, argument, open or mapped file.

    Skips this sweep's ancestors and its own session: the command that launched the sweep, such as
    the other end of `ship | tail`. Another agent or terminal is another session and still counts.
    Paths inside one of the exclude folders (lanes nested in path) do not count.
    """
    root = str(path.resolve())
    skip = [str(e.resolve()) for e in exclude]
    own_session = os.getsid(0)
    pth_cache: dict[Path, list[str]] = {}
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit() or int(entry.name) in ignore:
            continue
        try:
            if os.getsid(int(entry.name)) == own_session:
                continue
            used = _uses(entry, pth_cache)
        except OSError:
            continue
        for used_path in used:
            if any(used_path == e or used_path.startswith(e + os.sep) for e in skip):
                continue
            if used_path == root or used_path.startswith(root + os.sep):
                return int(entry.name)
    return None


def unit_dirs() -> list[Path]:
    """Folders systemd reads user units from, the transient ones included.

    `systemd-run --user --on-calendar ... --working-directory=<lane>` writes its timer and service to
    $XDG_RUNTIME_DIR/systemd/transient, not to ~/.config/systemd/user, so a scan of the second folder alone
    removed the lanes of the 2026-10-28 personal-wiki second-pass runs before their 22:00 start (#76).
    LANE_SWEEP_UNITS_DIR (folders separated like PATH) replaces the list, for tests.
    """
    override = os.environ.get("LANE_SWEEP_UNITS_DIR")
    if override:
        return [Path(d) for d in override.split(os.pathsep) if d]
    home = Path.home()
    runtime = Path(os.environ.get("XDG_RUNTIME_DIR") or f"/run/user/{os.getuid()}")
    return [home / ".config" / "systemd" / "user", runtime / "systemd" / "transient", runtime / "systemd" / "user",
            home / ".local" / "share" / "systemd" / "user", Path("/etc/systemd/user")]


def unit_uses(path: Path) -> str | None:
    """Return the systemd user unit whose file names a path inside path, or None.

    A timer's job is not a running process between runs, so `busy` cannot see it. Removing its folder
    breaks the job at its next start (2026-10-25: label-speakers failed from then on). The unit's file and
    its drop-ins (`<unit>.service.d/*.conf`) count, in every folder in `unit_dirs`.
    """
    root = path.resolve()
    home = str(Path.home())
    for folder in unit_dirs():
        try:
            names = sorted({p.name for p in folder.glob("*.service")} | {p.name[: -len(".d")] for p in folder.glob("*.service.d")})
        except OSError:
            continue
        for name in names:
            for unit in [folder / name, *sorted((folder / f"{name}.d").glob("*.conf"))]:
                try:
                    text = unit.read_text(encoding="utf-8").replace("%h", home)
                except OSError:
                    continue
                for token in re.findall(r"/[^\s\"'=:;]+", text):
                    try:
                        target = Path(token).resolve()
                    except (OSError, RuntimeError):
                        continue
                    if target == root or root in target.parents:
                        return name
    return None


def idle_minutes(repo: Path, lane: Lane) -> float:
    """Minutes since the lane's HEAD, index or reflog last changed."""
    gitdir = Path(git(lane.path, "rev-parse", "--absolute-git-dir").stdout.strip())
    times = [p.stat().st_mtime for p in (gitdir / "HEAD", gitdir / "index", gitdir / "logs" / "HEAD") if p.exists()]
    return (time.time() - max(times)) / 60 if times else float("inf")


def judge(repo: Path, lane: Lane, base: str, ignore: set[int], limits: tuple[float, ...], merged: set[Path], keep: frozenset[Path] = frozenset()) -> tuple[str | None, bool]:
    """Return (why the lane must stay or None, whether it must be archived before removal).

    limits are (idle minutes, idle minutes with no commits, idle minutes before an unmerged lane is archived;
    0 or less never archives).
    """
    if lane.path.resolve() in keep:
        return "kept by --keep-lane", False
    if lane.locked:
        # Not a lane: a tool locked it so that nothing removes it (2026-11-13: process_tracing's pinned
        # llm_client checkout was removed while unlocked, and its tests could not import for three days).
        return (f"locked: {lane.lock_reason}" if lane.lock_reason else "locked"), False
    unit = unit_uses(lane.path)
    if unit:
        return f"the systemd unit {unit} runs from it", False
    if lane.path.name.endswith(ASIDE_SUFFIX):
        return "left by a lane-sweep removal that stopped partway; restore with the command in the day's log", False
    status = git(lane.path, "status", "--porcelain", "--untracked-files=all")
    if status.returncode != 0:
        return f"git status failed: {status.stderr.strip()[:120]}", False
    if status.stdout.strip():
        return "uncommitted changes", False
    if (lane.path / ".gitmodules").is_file():
        return "contains submodules: git moves or removes it only with --force, which the sweep never uses; remove it by hand after checking", False
    if lane.branch and git(repo, "rev-parse", f"refs/heads/{lane.branch}").stdout.strip() != lane.head:
        return "branch moved during the sweep", False
    unmerged = not content_on(repo, lane.head, base) and not merged_pr_at(repo, lane.branch, lane.head)
    archive_limit = limits[2] if len(limits) > 2 else 0
    if unmerged:
        if archive_limit <= 0:
            return f"work not on {base}", False
        # The idle wait comes first here (it is cheap and keeps most unmerged lanes); --merged-lane never
        # shortens it, since nothing was merged.
        idle = idle_minutes(repo, lane)
        if idle < archive_limit:
            return f"work not on {base}; archived and removed after {archive_limit / 60:.0f} h idle ({idle / 60:.1f} h so far)", False
        pid = busy(lane.path, ignore)
        if pid:
            return f"work not on {base}; in use by process {pid}", False
        held = ignored_keep_reason(lane)
        if held:
            return f"work not on {base}; {held}", False
        return None, True
    pid = busy(lane.path, ignore)
    if pid:
        return f"in use by process {pid}", False
    # A branch made its own commits if its reflog has more than the "Created from" entry; merged
    # lanes look the same as brand-new ones by ancestry alone.
    reflog = git(repo, "reflog", "show", "--format=%H", f"refs/heads/{lane.branch}").stdout.split() if lane.branch else []
    has_commits = len(reflog) > 1 or git(repo, "merge-base", "--is-ancestor", lane.head, base).returncode != 0
    if lane.path.resolve() not in merged:
        limit = limits[0] if has_commits else limits[1]
        idle = idle_minutes(repo, lane)
        if idle < limit:
            return f"recently active ({idle:.0f} min idle, limit {limit:.0f})", False
    # git worktree remove deletes ignored files too, without --force; a merged lane's data is lost the same way.
    return ignored_keep_reason(lane), False


def _unwritable_folder(path: Path) -> Path | None:
    """A folder inside path whose entries this user cannot delete, or None."""
    for folder, _dirs, _files in os.walk(path):
        if not os.access(folder, os.W_OK | os.X_OK):
            return Path(folder)
    return None


def remove(repo: Path, lane: Lane, log, ignore: set[int] | None = None, keep_branch: bool = False) -> bool:
    """Remove the lane's worktree and branch, never leaving a half-deleted tree at the lane's path.

    Logs the restore command first, moves the lane aside with `git worktree move` (one rename), checks
    again that no process uses it, then runs `git worktree remove` without --force. A failure with the
    tracked files intact moves the lane back; a failure after deleting files leaves the remains at the
    hidden path, keeps the branch and logs the command that recreates the lane. With keep_branch (an
    archived unmerged lane) only the worktree goes; the caller has logged its restore command.
    """
    if not keep_branch:
        restore = f"git -C {repo} branch {lane.branch} {lane.head}" if lane.branch else f"git -C {repo} worktree add {lane.path} {lane.head}"
        log(f"remove {lane.path} branch={lane.branch} tip={lane.head} restore: {restore}")
        extra, _size = ignored_entries(lane)
        if extra:
            log(f"  ignored files the removal deletes (not in git, not rebuildable caches, under 1 MiB): {', '.join(extra[:20])}"
                + (" ..." if len(extra) > 20 else ""))
    aside = lane.path.with_name(f".{lane.path.name}{ASIDE_SUFFIX}")
    moved = git(repo, "worktree", "move", str(lane.path), str(aside))
    if moved.returncode != 0:
        log(f"  worktree move aside failed, nothing changed: {moved.stderr.strip()[:200]}")
        return False

    def put_back(why: str) -> bool:
        """Move the lane back to its own path, log why the removal stopped, and report failure."""
        back = git(repo, "worktree", "move", str(aside), str(lane.path))
        log(f"  {why}; " + ("moved back, nothing changed" if back.returncode == 0 else f"move back failed, the lane is at {aside}: {back.stderr.strip()[:200]}"))
        return False

    pid = busy(aside, ignore or set())
    if pid:
        return put_back(f"process {pid} started using it")
    stuck = _unwritable_folder(aside)
    if stuck:
        return put_back(f"{stuck} cannot be written, so removal would stop partway")
    gone = git(repo, "worktree", "remove", str(aside), timeout=REMOVE_TIMEOUT)
    if gone.returncode != 0:
        why = f"worktree remove failed: {gone.stderr.strip()[:200]}"
        intact = git(aside, "status", "--porcelain", "--untracked-files=no") if aside.exists() else None
        if intact is not None and intact.returncode == 0 and not intact.stdout.strip():
            return put_back(why)
        recreate = f"git -C {repo} worktree add {lane.path} {lane.branch or lane.head}"
        log(f"  {why}; it stopped partway, the remains are at {aside}, the branch is kept; recreate the lane: {recreate}")
        return False
    if lane.branch and not keep_branch:
        # update-ref with the old value deletes only if the branch still points at the checked tip.
        deleted = git(repo, "update-ref", "-d", f"refs/heads/{lane.branch}", lane.head)
        if deleted.returncode != 0:
            log(f"  branch delete failed: {deleted.stderr.strip()[:200]}")
            return False
    return True


# Ignored folders that are regenerable caches: anything under one of these names (at any depth) neither keeps a
# lane nor is listed in the log. Everything else ignored (.claude/hook_log.jsonl, *.db, *-wal, *-shm, var/,
# results/, data/, openspec/changes/archive/, site/, all found in real lanes by the 2026-11-19 manual cleanup)
# is work a removal would destroy.
REBUILDABLE = {".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
               ".tox", "dist", "build", ".cache", ".next", "target", ".lockstep", ".code2check", ".work"}
# A lane whose ignored non-cache files reach this many bytes in total is kept; below it they are logged and removed.
IGNORED_KEEP_BYTES = 1024 * 1024


def repo_is_private(repo: Path, slug: str) -> bool:
    """True only when GitHub, asked through the owner's gh wrapper, says the repository is private."""
    try:
        out = subprocess.run([gh_for(slug), "repo", "view", slug, "--json", "isPrivate"],
                             capture_output=True, text=True, timeout=30)
        return out.returncode == 0 and json.loads(out.stdout or "{}").get("isPrivate") is True
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return False


def push_archive_ref(repo: Path, ref: str, log) -> None:
    """Push ref to origin when origin's owner is the `owner:` setting and the repository is private.

    The tip was never pushed (no remote branch holds it), so pushing it to a public repository would publish
    work nobody chose to publish; another owner's remote is not this person's to write to. A failed push is
    logged and does not stop the removal: the verified bundle and the kept local refs preserve the tip.
    """
    slug = github_slug(repo)
    owner = setting("owner", "PROJECT_GRAPH_OWNER")
    if not slug or not owner or slug.split("/", 1)[0] != owner:
        log(f"  not pushed: origin {slug or 'is not on GitHub'} is not owned by the configured owner")
        return
    if not repo_is_private(repo, slug):
        log(f"  not pushed: {slug} is not reported private, and this tip was never pushed")
        return
    pushed = git(repo, "push", "-q", "origin", f"{ref}:{ref}", timeout=120,
                 env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    log(f"  pushed {ref} to {slug}" if pushed.returncode == 0 else f"  push of {ref} failed (bundle and local refs keep the tip): {pushed.stderr.strip()[:200]}")


def _is_cache(rel: str) -> bool:
    """True when a lane-relative path lies under a regenerable cache folder (any component) or an .egg-info."""
    return any(part in REBUILDABLE or part.endswith(".egg-info") for part in Path(rel.rstrip("/")).parts)


def _non_cache_bytes(path: Path, limit: int) -> int:
    """Bytes of the non-cache files at path (a file or folder), stopping once limit is reached.

    Cache folders nested inside are skipped; symbolic links are not followed. A file whose size cannot be read
    counts as limit, so an unreadable tree keeps the lane rather than letting it go unmeasured.
    """
    try:
        if not path.is_dir() or path.is_symlink():
            return path.lstat().st_size
    except OSError:
        return limit
    total = 0
    for folder, dirs, files in os.walk(path, followlinks=False, onerror=lambda _e: None):
        dirs[:] = [d for d in dirs if d not in REBUILDABLE and not d.endswith(".egg-info")]
        for name in files:
            try:
                total += os.lstat(os.path.join(folder, name)).st_size
            except OSError:
                return limit
            if total >= limit:
                return total
    return total


def ignored_entries(lane: Lane, limit: int = IGNORED_KEEP_BYTES) -> tuple[list[str], int]:
    """(ignored non-cache paths a removal deletes, their total bytes, counted only up to limit).

    -z keeps paths with spaces or non-ASCII characters unquoted, so each one can be measured. A folder holding
    only caches is not listed. A failed `git status` returns ["(git status --ignored failed)"] at limit bytes.
    """
    out = git(lane.path, "status", "--porcelain", "-z", "--ignored")
    if out.returncode != 0:
        return ["(git status --ignored failed)"], limit
    found: list[str] = []
    total = 0
    for entry in out.stdout.split("\0"):
        if not entry.startswith("!! ") or _is_cache(entry[3:]):
            continue
        size = _non_cache_bytes(lane.path / entry[3:], max(limit - total, 1))
        if size or not entry.endswith("/"):
            found.append(entry[3:])
            total = min(total + size, limit)
    return found, total


def ignored_keep_reason(lane: Lane) -> str | None:
    """Why a lane must stay because removing it deletes ignored files that are not caches, or None.

    Implements: lane-sweep/remove-finished-lanes-and-report-the-rest
    """
    found, total = ignored_entries(lane)
    if total < IGNORED_KEEP_BYTES:
        return None
    return "holds ignored non-cache files: " + ", ".join(found[:5]) + (" ..." if len(found) > 5 else "")


def archive_and_remove(repo: Path, lane: Lane, base: str, log, log_dir: Path, ignore: set[int] | None = None) -> bool:
    """Preserve an idle unmerged lane's tip, then remove only its worktree; the local branch stays.

    Unless a remote branch already holds the tip: create refs/archive/<YYYYMMDD>/<lane> at it, write a bundle of
    that ref (and the branch) holding only the commits not on base, verify it, and push the ref when allowed.
    Any failure before the removal leaves the lane as it was and reports failure.
    """
    day = dt.date.today().strftime("%Y%m%d")
    name = lane.path.name
    held = [r for r in git(repo, "for-each-ref", "--contains", lane.head, "--format=%(refname)", "refs/remotes/").stdout.split()
            if not r.endswith("/HEAD")]
    target = lane.branch or lane.head
    bundle: Path | None = None
    ref = f"refs/archive/{day}/{name}"
    if held and lane.branch:
        log(f"archive {lane.path}: tip {lane.head} is already on {held[0].removeprefix('refs/remotes/')}; no archive ref needed")
    if not held or not lane.branch:
        # A detached lane always gets the local ref: a remote-tracking ref can be stale (the sweep fetches
        # without --prune), and without a ref the tip would be reachable only from the reflog.
        have = git(repo, "rev-parse", "-q", "--verify", ref).stdout.strip()
        if have and have != lane.head:  # two lanes with one folder name on one day
            ref = f"{ref}-{lane.head[:12]}"
            have = git(repo, "rev-parse", "-q", "--verify", ref).stdout.strip()
        if have != lane.head:
            # The zero old value makes update-ref refuse to overwrite a ref that appeared meanwhile.
            made = git(repo, "update-ref", ref, lane.head, "0" * 40)
            if made.returncode != 0:
                log(f"archive {lane.path}: could not create {ref}, lane kept: {made.stderr.strip()[:200]}")
                return False
        target = lane.branch or ref
    if held:
        if not lane.branch:
            log(f"archive {lane.path}: tip {lane.head} is already on {held[0].removeprefix('refs/remotes/')}; local ref {ref} created")
    else:
        refs = [ref] + ([f"refs/heads/{lane.branch}"] if lane.branch else [])
        bundle = log_dir / f"{repo.name}--{name}--{day}-{lane.head[:12]}.bundle"
        made = git(repo, "bundle", "create", "-q", str(bundle), *refs, f"^{base}", timeout=REMOVE_TIMEOUT)
        if made.returncode != 0:
            log(f"archive {lane.path}: bundle create failed, lane kept (ref {ref} stays): {made.stderr.strip()[:200]}")
            return False
        checked = git(repo, "bundle", "verify", "-q", str(bundle), timeout=REMOVE_TIMEOUT)
        if checked.returncode != 0:
            log(f"archive {lane.path}: bundle verify failed, lane kept (ref {ref} and {bundle} stay): {checked.stderr.strip()[:200]}")
            return False
        log(f"archive {lane.path}: created {ref} at {lane.head}, bundle {bundle} verified; offline restore: "
            f"git -C {repo} fetch {bundle} {ref}:{ref}")
        push_archive_ref(repo, ref, log)
    extra, _size = ignored_entries(lane)
    if extra:
        log(f"  ignored files the removal deletes (not in git, not rebuildable caches): {', '.join(extra[:20])}" + (" ..." if len(extra) > 20 else ""))
    log(f"archive-remove {lane.path} branch={lane.branch} tip={lane.head} bundle={bundle or 'none (tip on a remote branch)'} "
        f"branch kept; restore: git -C {repo} worktree add {lane.path} {target}")
    return remove(repo, lane, log, ignore, keep_branch=True)


def primary_checkout(repo: Path) -> Path:
    """The main worktree of repo: the parent of its common git directory."""
    common = git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir").stdout.strip()
    return Path(common).parent if common else repo


def judge_primary(primary: Path, base: str, ignore: set[int], nested: tuple[Path, ...]) -> tuple[str | None, str, str, str]:
    """Return (why the checkout must not move or None, its branch label, old commit, new commit).

    A reason of "" means the checkout is already current: nothing to do and nothing to report.
    """
    head = git(primary, "symbolic-ref", "-q", "--short", "HEAD").stdout.strip()
    label = head or "detached"
    old = git(primary, "rev-parse", "HEAD").stdout.strip()
    new = git(primary, "rev-parse", base).stdout.strip()
    want = base.split("/", 1)[1]
    if head != want:
        return f"not on {want}", label, old, new
    if old == new:
        return "", label, old, new
    status = git(primary, "status", "--porcelain", "--untracked-files=all")
    if status.returncode != 0:
        return f"git status failed: {status.stderr.strip()[:120]}", label, old, new
    if status.stdout.strip():
        return "uncommitted changes", label, old, new
    if git(primary, "merge-base", "--is-ancestor", old, new).returncode != 0:
        return f"diverged from {base}", label, old, new
    lock = Path(git(primary, "rev-parse", "--path-format=absolute", "--git-path", "index.lock").stdout.strip() or primary / ".git" / "index.lock")
    if lock.exists():
        since = dt.datetime.fromtimestamp(lock.stat().st_mtime).isoformat(timespec="minutes")
        return f"index.lock present since {since} (a git command is running, or one stopped and left it)", label, old, new
    pid = busy(primary, ignore, nested)
    if pid:
        return f"in use by process {pid}", label, old, new
    return None, label, old, new


def fast_forward_primary(repo: Path, base: str | None, found: list[Lane], apply: bool, ignore: set[int], log) -> tuple[list[str], Counter]:
    """Fast-forward the primary checkout of repo to base when judge_primary allows it."""
    tally: Counter = Counter()
    primary = primary_checkout(repo).resolve()
    if base is None:
        tally["ff_skipped"] += 1
        return [f"skip fast-forward {primary}: no remote default branch"], tally
    reason, label, old, new = judge_primary(primary, base, ignore, tuple(l.path for l in found))
    if reason == "":
        return [], tally
    where = f"{primary} [{label}]"
    if reason:
        tally["ff_skipped"] += 1
        return [f"skip fast-forward {where}: {reason}"], tally
    if not apply:
        tally["fast_forwardable"] += 1
        return [f"fast-forwardable {where} {old[:12]} -> {new[:12]}"], tally
    log(f"fast-forward {where} {old} -> {new} (both on {base}; nothing local is lost)")
    tool = canonical_lock()
    if not os.access(primary, os.W_OK) and tool is not None and tool.exists():
        log(f"  {primary} is read-only (canonical lock); moving it with {tool.name} --sync")
        done = subprocess.run([sys.executable, str(tool), "--sync", str(primary), "--quiet"],
                              capture_output=True, text=True, timeout=REMOVE_TIMEOUT)
    else:
        done = git(primary, "merge", "--ff-only", "-q", new)
    if done.returncode != 0:
        log(f"  fast-forward failed: {done.stderr.strip()[:200]}")
        tally["failed"] += 1
    else:
        tally["fast_forwarded"] += 1
    return [], tally


def repos_under(root: Path) -> list[Path]:
    """Main checkouts directly under root (a .git directory, not a worktree's .git file)."""
    return sorted(p for p in root.iterdir() if (p / ".git").is_dir())


def sweep_repo(repo: Path, apply: bool, fetch: bool, ignore: set[int], limits: tuple[float, ...], merged: set[Path], log,
               keep: frozenset[Path] = frozenset(), log_dir: Path | None = None) -> tuple[list[str], Counter]:
    """Judge every lane of one repository, removing finished ones and archiving idle unmerged ones when apply is set.

    The tally's key ("kept_in", repo name) counts the lanes kept in this repository.
    """
    lines: list[str] = []
    tally: Counter = Counter()
    log_dir = log_dir or Path.home() / "code2" / ".lane-sweep-logs"
    found = lanes(repo)
    if apply and any(l.prunable for l in found):
        git(repo, "worktree", "prune")
    if fetch:
        try:
            git(repo, "fetch", "-q", "origin", timeout=60)
        except subprocess.TimeoutExpired:
            pass
    base = default_branch(repo)
    for lane in found:
        if lane.prunable:
            continue
        reason, archive = ("no remote default branch", False) if base is None else judge(repo, lane, base, ignore, limits, merged, keep)
        label = f"{lane.path} [{lane.branch or 'detached'}]"
        if reason:
            tally["kept"] += 1
            tally[("kept_in", repo.name)] += 1
            lines.append(f"keep {label}: {reason}")
        elif not apply:
            tally["archivable" if archive else "removable"] += 1
            lines.append(f"archivable {label}: work not on {base}, idle past the limit" if archive else f"removable {label}")
        elif archive and base is not None:
            if archive_and_remove(repo, lane, base, log, log_dir, ignore):
                tally["archived"] += 1
            else:
                tally["failed"] += 1
                tally[("kept_in", repo.name)] += 1
        elif remove(repo, lane, log, ignore):
            tally["removed"] += 1
        else:
            tally["failed"] += 1
    ff_lines, ff_tally = fast_forward_primary(repo, base, found, apply, ignore, log)
    return lines + ff_lines, tally + ff_tally


def main(argv: list[str] | None = None) -> int:
    """Sweep the given repositories; print counts and return 0 unless a removal or fast-forward failed."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--apply", action="store_true", help="remove finished lanes (default: report only)")
    ap.add_argument("--repo", action="append", type=Path, help="repository to sweep (repeatable)")
    ap.add_argument("--root", type=Path, default=Path.home() / "code2", help="sweep every repository under this folder")
    ap.add_argument("--no-fetch", action="store_true", help="do not fetch the remote default branch first")
    ap.add_argument("--log-dir", type=Path, default=Path(os.environ.get("LANE_SWEEP_LOG_DIR", Path.home() / "code2" / ".lane-sweep-logs")))
    ap.add_argument("--idle-minutes", type=float, default=IDLE_MINUTES)
    ap.add_argument("--idle-minutes-no-commits", type=float, default=IDLE_MINUTES_NO_COMMITS)
    ap.add_argument("--archive-after-hours", type=float, default=None,
                    help="archive and remove an unmerged lane idle this long; 0 never (default: lane_sweep_archive_after_hours "
                         f"in graph-config.yaml, else {ARCHIVE_IDLE_HOURS:.0f})")
    ap.add_argument("--merged-lane", action="append", type=Path,
                    help="a lane whose pull request was just merged at its tip: skip only the idle wait (ship passes this)")
    ap.add_argument("--keep-lane", action="append", type=Path,
                    help="a lane never to remove in this run (ship --keep-lane passes its own lane)")
    args = ap.parse_args(argv)

    args.log_dir.mkdir(parents=True, exist_ok=True)
    log_file = args.log_dir / f"{dt.date.today().isoformat()}.log"
    stamp = dt.datetime.now().isoformat(timespec="seconds")

    lock = threading.Lock()

    def log(line: str) -> None:
        """Print a line and append it, timestamped, to the day's log."""
        with lock:
            print(line)
            with log_file.open("a") as fh:
                fh.write(f"{stamp} {line}\n")

    repos = [r.resolve() for r in args.repo] if args.repo else repos_under(args.root)
    ignore = own_ancestors()
    archive_hours = archive_idle_hours() if args.archive_after_hours is None else args.archive_after_hours
    limits = (args.idle_minutes, args.idle_minutes_no_commits, archive_hours * 60)
    merged = {m.resolve() for m in args.merged_lane or []}
    keep = frozenset(k.resolve() for k in args.keep_lane or [])
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda r: sweep_repo(r, args.apply, not args.no_fetch, ignore, limits, merged, log, keep, args.log_dir), repos))
    counts: Counter = Counter()
    kept_lines: list[str] = []
    for lines, tally in results:
        kept_lines += lines
        counts.update(tally)
    removed, removable, archived, archivable, kept, failed = (counts[k] for k in ("removed", "removable", "archived", "archivable", "kept", "failed"))
    ff = ", ".join(f"{name} {counts[k]}" for k, name in (("fast_forwarded", "fast-forwarded"), ("fast_forwardable", "fast-forwardable"), ("ff_skipped", "skipped")))
    per_repo = sorted(((n, k[1]) for k, n in counts.items() if isinstance(k, tuple) and k[0] == "kept_in" and n), key=lambda p: (-p[0], p[1]))
    per_repo_line = "lanes kept per repository: " + (", ".join(
        f"{name} {n}" + (f" (more than {MANY_LANES})" if n > MANY_LANES else "") for n, name in per_repo) or "none")
    for line in kept_lines:
        print(line)
    (args.log_dir / "last-report.txt").write_text("\n".join(kept_lines + [per_repo_line]) + "\n")
    code = 1 if failed else 0
    log(per_repo_line)
    log(f"lane-sweep: repos {len(repos)}, removed {removed}, removable {removable}, archived {archived}, archivable {archivable}, "
        f"kept {kept}, failed {failed}; primary checkouts: {ff}; exit status {code}")
    return code


if __name__ == "__main__":
    sys.exit(main())

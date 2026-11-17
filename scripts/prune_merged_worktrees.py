#!/usr/bin/env python3
"""Remove git worktrees whose branch has actually landed on the default branch.

Implements: prune-merged-worktrees/proven-merge-only

Moved here unchanged from Project Meta (``scripts/prune_merged_worktrees.py`` at ``b743c308a``) on 2026-11-17,
AES consolidation plan row 11; ``~/.local/bin/prune-merged-worktrees`` links to the AES runtime clone's copy.

Squash-merge safe. This matters because squash-merge is the default in this
ecosystem, and every naive merge check gets it wrong:

  * `git branch --merged` / `git merge-base --is-ancestor` -- WRONG. A squash
    merge writes a brand-new commit on the default branch with no parent link
    to the branch, so the branch tip is never an ancestor of it.
  * `git cherry <default> <branch>` -- ALSO WRONG, despite being widely
    recommended for this. It compares *per-commit* patch ids. A squash merge
    collapses N branch commits into ONE commit whose diff equals their sum, so
    no individual patch id matches and every commit is reported `+` (unapplied).
    Measured 2026-09-07 against three real Inside-Success PRs: `git cherry`
    reported "unapplied" for all of them, including the two that were verifiably
    merged (PRs #630 and #628). It is a false-negative machine, not a fallback.

What this script actually asks, per worktree branch:

  1. THE FORGE (authoritative). Is there a PR whose head is this exact branch,
     whose state is MERGED, and whose merge commit is an ancestor of the local
     default branch? That last clause matters: a PR merged into some other base
     branch is not evidence that this branch landed *here*. This is what
     literally happened, not an inference from history.

     `gh` account routing is discovered, not assumed. Inside-Success repos are
     invisible to the default `gh` account (it answers "Could not resolve to a
     Repository") and need the `gh-insidesuccess` wrapper; personal repos need
     plain `gh`. The script tries plain `gh` first, then every `gh-*` wrapper on
     PATH, and uses the first identity that can actually see the repo. It
     reports which identity answered.

  2. CONTENT (offline, no forge auth, works for every repo). Does merging this
     branch into the default branch change anything at all?
     `git merge-tree --write-tree <default> <branch>` produces the tree that
     the merge would yield. If that tree is byte-identical to the default
     branch's own tree, the branch contributes literally nothing -- every line
     it introduced is already present -- so removing it cannot lose work. This
     survives squash merges, and it survives the default branch moving on
     afterwards.

     Note this check is sound but not complete: if the default branch later
     edited the same regions, the re-merge conflicts and the check returns
     UNKNOWN rather than a "no". That is exactly what happened to PR #628 above,
     and it is why signal 1 exists.

A worktree is removed only when signal 1 or signal 2 positively proves the work
landed, and nothing vetoes it -- and `--exclude PATH` (repeatable) is exactly
that veto, for a caller that knows something this script cannot see (a live
coordination claim, say): a merge proof about the BRANCH is not proof that the
WORKTREE has nothing else going on. Everything else is kept and printed with the
reason and the branch's age, for a human to decide. This script never removes
unmerged or ambiguous work, and it never guesses.

Usage:
  prune-merged-worktrees [repo_path] [--dry-run] [--verbose] [--exclude PATH ...]
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# `git merge-tree --write-tree` landed in git 2.38. Below that we have no sound
# content check, and we say so rather than silently degrading to a broken one.
MERGE_TREE_MIN = (2, 38)


def run(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    """Run a command in `cwd` and capture it; never raises on non-zero."""
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def git_version() -> tuple[int, ...]:
    """Local git version as a tuple, or (0,) when it cannot be parsed."""
    r = subprocess.run(["git", "--version"], text=True, capture_output=True, check=False)
    parts = r.stdout.strip().split()
    for p in parts:
        if p and p[0].isdigit():
            try:
                return tuple(int(x) for x in p.split(".")[:3])
            except ValueError:
                break
    return (0,)


def default_branch(repo: Path) -> str:
    """Name of the remote default branch, falling back to main/master."""
    r = run("git", "symbolic-ref", "refs/remotes/origin/HEAD", cwd=repo)
    if r.returncode == 0 and r.stdout.strip():
        return r.stdout.strip().rsplit("/", 1)[-1]
    for cand in ("main", "master"):
        if run("git", "rev-parse", "--verify", "--quiet", f"origin/{cand}", cwd=repo).returncode == 0:
            return cand
    return "main"


def list_worktrees(repo: Path) -> list[dict]:
    """Read every registration, including missing/detached/locked paths.

    NUL-delimited porcelain preserves spaces, newlines and Git-quoted paths.
    Enumeration failure must not masquerade as an empty repository.
    """
    r = run("git", "worktree", "list", "--porcelain", "-z", cwd=repo)
    if r.returncode:
        raise RuntimeError(f"worktree enumeration exit {r.returncode}: {r.stderr.strip()}")
    entries: list[dict] = []
    cur: dict = {}
    for field in r.stdout.split("\0"):
        key, separator, value = field.partition(" ")
        if key == "worktree":
            if cur:
                entries.append(cur)
            cur = {"path": value, "branch": None, "detached": False}
        elif key == "branch":
            cur["branch"] = value.removeprefix("refs/heads/")
        elif key == "detached":
            cur["detached"] = True
        elif key:
            cur[key] = value if separator else True
    if cur:
        entries.append(cur)
    return entries


# --------------------------------------------------------------------------
# Signal 1: the forge
# --------------------------------------------------------------------------

def gh_candidates() -> list[tuple[str, str]]:
    """(label, executable) for every gh identity available on this machine.

    Plain `gh` first, then any `gh-<org>` wrapper on PATH. Discovered rather
    than hardcoded, so a wrapper added later is picked up without a code change.
    """
    cands: list[tuple[str, str]] = []
    plain = shutil.which("gh")
    if plain:
        cands.append(("gh", plain))
    seen = set()
    for d in os.environ.get("PATH", "").split(os.pathsep):
        if not d or d in seen:
            continue
        seen.add(d)
        try:
            names = sorted(os.listdir(d))
        except OSError:
            continue
        for name in names:
            if not name.startswith("gh-") or name == "gh":
                continue
            p = os.path.join(d, name)
            if os.path.isfile(p) and os.access(p, os.X_OK):
                if p not in [c[1] for c in cands]:
                    cands.append((name, p))
    return cands


_GH_IDENTITY: dict[str, tuple[str, str] | None] = {}


def resolve_gh_identity(repo: Path) -> tuple[str, str] | None:
    """First gh identity that can actually see this repo, or None.

    Selection is a capability probe, not a name match: we ask each identity a
    real question about this repository and keep the first that answers. Cached
    per repo so a many-worktree run probes once, not once per branch.
    """
    key = str(repo)
    if key in _GH_IDENTITY:
        return _GH_IDENTITY[key]
    found = None
    for label, exe in gh_candidates():
        r = run(exe, "repo", "view", "--json", "name", cwd=repo)
        if r.returncode == 0 and r.stdout.strip():
            found = (label, exe)
            break
    _GH_IDENTITY[key] = found
    return found


def gh_prs_for_branch(repo: Path, branch: str) -> tuple[list[dict] | None, str | None]:
    """PRs whose head is exactly `branch`, plus the gh identity that answered.

    Returns (None, None) when no gh identity can see this repository at all.
    An empty list means "this identity sees the repo and there is no such PR".
    """
    ident = resolve_gh_identity(repo)
    if ident is None:
        return None, None
    label, exe = ident
    r = run(
        exe, "pr", "list", "--head", branch, "--state", "all",
        "--json", "number,state,mergedAt,mergeCommit",
        "--limit", "50", cwd=repo,
    )
    if r.returncode != 0:
        return None, None
    try:
        return json.loads(r.stdout or "[]"), label
    except json.JSONDecodeError:
        return None, None


def is_ancestor(repo: Path, commit: str, ref: str) -> bool:
    """True if `commit` is an ancestor of `ref`, fetching the object if needed."""
    if run("git", "cat-file", "-e", f"{commit}^{{commit}}", cwd=repo).returncode != 0:
        # Object not local -- try to fetch just this one commit before answering.
        run("git", "fetch", "--quiet", "origin", commit, cwd=repo)
        if run("git", "cat-file", "-e", f"{commit}^{{commit}}", cwd=repo).returncode != 0:
            return False
    return run("git", "merge-base", "--is-ancestor", commit, ref, cwd=repo).returncode == 0


# --------------------------------------------------------------------------
# Signal 2: content
# --------------------------------------------------------------------------

def merge_adds_nothing(repo: Path, default_ref: str, branch: str) -> bool | None:
    """True if merging `branch` into `default_ref` would change nothing.

    True  -> every change the branch introduced is already present. Removing it
             cannot lose work. Survives squash merges.
    False -> the merge would add content that is not on the default branch.
    None  -> undecidable here (merge conflict, or git too old). NOT a "no".
    """
    if git_version() < MERGE_TREE_MIN:
        return None
    r = run("git", "merge-tree", "--write-tree", default_ref, branch, cwd=repo)
    if r.returncode != 0:
        # Non-zero means conflict (or unsupported) -- we cannot decide.
        return None
    merged_tree = r.stdout.strip().splitlines()[0].strip() if r.stdout.strip() else ""
    base = run("git", "rev-parse", f"{default_ref}^{{tree}}", cwd=repo)
    if base.returncode != 0 or not merged_tree:
        return None
    return merged_tree == base.stdout.strip()


def last_commit_age_days(repo: Path, branch: str) -> float | None:
    """Age in days of the branch tip commit, or None if it cannot be read."""
    r = run("git", "log", "-1", "--format=%ct", branch, cwd=repo)
    if r.returncode != 0 or not r.stdout.strip():
        return None
    return (datetime.now(timezone.utc).timestamp() - int(r.stdout.strip())) / 86400


def age_str(repo: Path, branch: str) -> str:
    """Human-readable branch age for keep/skip reporting."""
    age = last_commit_age_days(repo, branch)
    return f"{age:.0f}d old" if age is not None else "age unknown"


# --------------------------------------------------------------------------

def classify(repo: Path, default_ref: str, branch: str) -> tuple[bool, str]:
    """(should_remove, reason). Removal requires positive proof the work landed."""
    prs, gh_label = gh_prs_for_branch(repo, branch)

    if prs:
        open_prs = [p for p in prs if p.get("state") == "OPEN"]
        if open_prs:
            nums = ", ".join(f"#{p['number']}" for p in open_prs)
            return False, f"PR {nums} still open ({gh_label})"

        for p in prs:
            if p.get("state") != "MERGED":
                continue
            mc = (p.get("mergeCommit") or {}).get("oid")
            if mc and is_ancestor(repo, mc, default_ref):
                return True, (
                    f"PR #{p['number']} merged {p.get('mergedAt')}, "
                    f"merge commit {mc[:9]} is on {default_ref} ({gh_label})"
                )

        merged = [p for p in prs if p.get("state") == "MERGED"]
        if merged:
            nums = ", ".join(f"#{p['number']}" for p in merged)
            # Merged, but not into this default branch -- fall through to content.
            forge_note = f"PR {nums} merged but its merge commit is not on {default_ref}"
        else:
            nums = ", ".join(f"#{p['number']}" for p in prs)
            return False, f"PR {nums} closed without merging ({gh_label})"
    elif prs == []:
        forge_note = f"no PR for this branch ({gh_label})"
    else:
        forge_note = "no gh identity can see this repo"

    content = merge_adds_nothing(repo, default_ref, branch)
    if content is True:
        return True, f"merging into {default_ref} adds nothing -- all content already landed"
    if content is False:
        return False, f"branch has content not on {default_ref}; {forge_note}, {age_str(repo, branch)}"
    return False, f"undecidable (re-merge conflicts with {default_ref}); {forge_note}, {age_str(repo, branch)}"


def main() -> int:
    """Entry point: prune worktrees whose branches are proven merged."""
    args = [a for a in sys.argv[1:]]
    # This command removes worktrees by default. An unrecognised flag used to be
    # ignored, so `--help` (or a typo of `--dry-run`) ran a real prune
    # (observed 2026-09-15: `--help` removed three worktrees). Refuse instead.
    known_flags = {"--dry-run", "-n", "--verbose", "-v", "--exclude", "--inventory-only"}
    if "--help" in args or "-h" in args:
        print("usage: prune_merged_worktrees.py [REPO] [--dry-run|-n] [--verbose|-v] [--exclude PATH]... [--inventory-only]")
        return 0
    unknown = [a for i, a in enumerate(args) if a.startswith("-") and a not in known_flags
               and not (i > 0 and args[i - 1] == "--exclude")]
    if unknown:
        print(f"error: unrecognised option(s) {' '.join(unknown)}; nothing was pruned", file=sys.stderr)
        return 2
    dry_run = "--dry-run" in args or "-n" in args
    verbose = "--verbose" in args or "-v" in args
    exclude_paths: set[Path] = set()
    positional: list[str] = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--exclude":
            i += 1
            if i < len(args):
                exclude_paths.add(Path(args[i]).resolve())
        elif not a.startswith("-"):
            positional.append(a)
        i += 1
    repo = Path(positional[0]).resolve() if positional else Path.cwd()

    if run("git", "rev-parse", "--git-dir", cwd=repo).returncode != 0:
        print(f"error: {repo} is not a git repository", file=sys.stderr)
        return 2

    try:
        worktrees = list_worktrees(repo)
    except (OSError, RuntimeError) as exc:
        print(f"error: {repo}: {exc}", file=sys.stderr)
        return 2
    if "--inventory-only" in args:
        print(json.dumps({"repository": str(repo), "worktrees": worktrees}, indent=2))
        return 0

    fetched = run("git", "fetch", "origin", "--quiet", "--prune", cwd=repo)
    if fetched.returncode:
        print(f"error: {repo}: fetch exit {fetched.returncode}: {fetched.stderr.strip()}; nothing was pruned", file=sys.stderr)
        return 2
    default = default_branch(repo)
    default_ref = f"origin/{default}"
    if run("git", "rev-parse", "--verify", "--quiet", default_ref, cwd=repo).returncode != 0:
        print(f"error: cannot resolve {default_ref}; refusing to judge merges blind", file=sys.stderr)
        return 2

    if git_version() < MERGE_TREE_MIN:
        print(
            f"warning: git {'.'.join(map(str, git_version()))} lacks "
            f"`merge-tree --write-tree` (needs {'.'.join(map(str, MERGE_TREE_MIN))}); "
            "the offline content check is disabled and only the forge can prove a merge.",
            file=sys.stderr,
        )

    main_worktree = worktrees[0]["path"] if worktrees else ""
    removed, kept, errors = [], [], []

    for wt in worktrees:
        if wt["path"] == main_worktree:
            continue
        branch = wt["branch"] or "DETACHED"
        if wt["detached"] or not wt["branch"] or "locked" in wt or "prunable" in wt:
            kept.append((wt["path"], branch, "retained registration: detached, locked or missing; individual disposition required"))
            continue
        if Path(wt["path"]).resolve() in exclude_paths:
            kept.append((wt["path"], branch, "excluded: caller protection (live claim or pending preservation preflight)"))
            continue
        should_remove, reason = classify(repo, default_ref, branch)
        if verbose:
            print(f"  [check] {branch}: {'MERGED' if should_remove else 'KEEP'} -- {reason}")

        if not should_remove:
            kept.append((wt["path"], branch, reason))
            continue
        if dry_run:
            removed.append((wt["path"], branch, reason + " [dry-run, not removed]"))
            continue
        r1 = run("git", "worktree", "remove", wt["path"], cwd=repo)
        if r1.returncode != 0:
            reason = f"proven merged but remove failed: {r1.stderr.strip()}"
            kept.append((wt["path"], branch, reason))
            errors.append(reason)
            continue
        deleted = run("git", "branch", "-D", branch, cwd=repo)
        if deleted.returncode:
            reason = f"folder removed but branch retained: {deleted.stderr.strip()}"
            errors.append(reason)
            kept.append((wt["path"], branch, reason))
            continue
        removed.append((wt["path"], branch, reason))

    if removed:
        verb = "Would remove" if dry_run else "Removed"
        print(f"{verb} {len(removed)} merged worktree(s):")
        for path, branch, reason in removed:
            print(f"  - {path}  [{branch}]")
            print(f"      proof: {reason}")
    if kept:
        print(f"Kept {len(kept)} worktree(s):")
        for path, branch, reason in kept:
            print(f"  - {path}  [{branch}]  -- {reason}")
    if not removed and not kept:
        print("No non-main worktrees found.")
    print(f"Summary: removed={len(removed) if not dry_run else 0} proposed={len(removed) if dry_run else 0} retained={len(kept)} errors={len(errors)} exit_status={1 if errors else 0}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

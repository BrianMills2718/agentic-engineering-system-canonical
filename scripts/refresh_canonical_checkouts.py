#!/usr/bin/env python3
"""Keep canonical checkouts exact, clean, and on the advertised default branch.

A canonical checkout that falls behind `origin` does not fail. It answers, with
stale content, and nothing marks the answer as old. On 2026-08-23 that cost a
session most of an hour: `~/code/active/project-meta` was 46 commits behind, a
handoff file it had been asked to review appeared not to exist, and a coverage
figure derived from its working tree reported 68/139 against a true 84/139 --
naming 16 already-published projects as outstanding work.

The read-only bit on those trees is deliberate: it stops agents committing in a
shared checkout. It is also not stable -- project-meta was mode 555 and mode 755
within the same hour -- so this script never reasons about permissions. It does
the two things that work regardless:

1. **Always fetch.** `.git/` stays writable even when the working tree is not, so
   fetching succeeds in a read-only checkout. This is the part that matters most:
   `git show origin/main:<path>` is the prescribed way to read current facts from
   these trees, and it is only correct if the remote refs are fresh. Nothing was
   guaranteeing that.
2. **Fast-forward through the lock controller.** When the real
   ``.git/canonical-lock-v1.json`` receipt exists, the checkout's sanctioned
   controller performs one unlock/pull/re-lock transaction and verifies that
   the checkout is both current and locked again. Unlocked clean default-branch
   checkouts still use a direct fast-forward.
3. **Also check the repo the current session is sitting in.** TARGETS is a
   short, deliberately fixed list of ecosystem-critical checkouts -- it is not
   "every repo," and a session working in an ordinary project repo that is not
   on that list gets none of the above. On 2026-09-02 that gap let a different
   checkout (`agentic-engineering-system`, not in TARGETS) go stale unnoticed
   the same way project-meta had. Every default invocation (no explicit
   ``--targets``) now also resolves the session's current working directory to
   its canonical repo root -- walking past a worktree to the checkout that owns
   its shared ``.git`` -- and adds it to the check if it is not already present.
   An explicit ``--targets`` still means exactly that list; this addition never
   changes what a caller asked for by name.

Non-blocking at session start: it prints and exits 0 unless ``--strict``. It
never resets or discards local work and never advances a dirty or non-default
checkout.

Copied from Project Meta scripts/refresh_canonical_checkouts.py (retirement plan step 4, Decision 20), with these
differences, each because AES does not carry the thing the old code leaned on:
  * The project graph is one person's own data: the PROJECT_GRAPH environment variable names it, else it is read from
    the private `aes-config` repository. The concern repository for stuck checkouts is `concern_repo` in
    `graph-config.yaml` beside the graph (or the CONCERN_REPO environment variable); a missing value stops the run and
    names where to set it.
  * TARGETS is empty: its keys were Project Meta's old ~/code/active layout and nothing in AES reads them. The graph
    sweep (``--all-graph``) and the session's own repository are the targets.
  * The canonical lock controller (``canonical_lock.py``, 1,765 lines of Project Meta) is not ported and no checkout in
    the graph carries a lock receipt. A checkout that does carry one, or whose changes need that controller to classify,
    is reported left alone, never modified.
  * Targets derived from systemd unit files (``unit_execution_targets``) are dropped: the graph sweep already covers every
    registered checkout. The "checkouts a unit operates on in place" list is read from the JSON file named by
    IN_PLACE_BASELINE, else ``unattended_execution_sources_baseline.json`` beside the graph; a missing file means no
    checkout is skipped as in place.
Implements: graph-checkout-refresh/settings-come-from-config
Implements: graph-checkout-refresh/never-discards-local-work
Implements: graph-checkout-refresh/graph-sweep-covers-registered-checkouts
Implements: graph-checkout-refresh/stuck-checkouts-raise-a-concern
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

GRAPH_DEFAULT = Path(os.environ.get("PROJECT_GRAPH") or Path.home() / "code2/aes-config/PROJECT_GRAPH.json")
CONFIG = GRAPH_DEFAULT.parent / "graph-config.yaml"

# Fixed checkouts to refresh on every default run, keyed by path relative to $HOME with the reason each earns a fetch.
# Empty here: the old keys named Project Meta's ~/code/active layout, and the graph sweep covers every registered checkout.
TARGETS: dict[str, str] = {}


def setting(key: str, env: str) -> str:
    """One value from the environment, else `key:` in graph-config.yaml beside the project graph. No value is a loud stop."""
    named = os.environ.get(env)
    if named:
        return named
    try:
        found = re.search(rf"^{key}:\s*(\S+)", CONFIG.read_text(), re.M)
    except OSError:
        found = None
    if not found:
        raise SystemExit(f"refresh_canonical_checkouts: no {key} named: set {env} or put `{key}:` in {CONFIG}")
    return found.group(1)


STAMP = Path.home() / ".claude" / "state" / "canonical_checkout_refresh.json"
FETCH_TIMEOUT_SECONDS = 20
LOCK_RECEIPT_NAME = "canonical-lock-v1.json"  # a checkout holding one needs a controller AES does not have


def resolve_target(rel: str, targets: dict[str, str]) -> str:
    """Resolve a caller-supplied ``--targets`` value against the known TARGETS keys.

    A bare short name (``project-meta``) is not a valid key -- the keys are
    full relative paths (``code/active/project-meta``) -- but it reads as one,
    and typing it silently produced ``~/project-meta`` (nonexistent), which the
    caller then skipped with a bare ``continue`` and reported as
    "all current" without ever checking anything. This resolves an exact key
    match first, then falls back to a basename match when exactly one TARGETS
    key ends in that name; an unmatched or ambiguous name is returned
    unchanged so the caller still resolves a (missing) path and reports it as
    unreachable instead of silently disappearing from the result set.
    """
    if rel in targets:
        return rel
    basename_matches = [key for key in targets if Path(key).name == rel]
    if len(basename_matches) == 1:
        return basename_matches[0]
    return rel


def git(repo: Path, *args: str, timeout: int = 10) -> tuple[int, str, str]:
    """Run git in a repo and return (returncode, stdout, stderr), all trimmed."""
    try:
        done = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return 124, "", f"timed out after {timeout}s"
    except OSError as exc:
        return 127, "", str(exc)
    return done.returncode, done.stdout.strip(), done.stderr.strip()


def upstream_ref(repo: Path) -> str | None:
    """Return the remote-tracking ref for the default branch, or None."""
    for repair in (False, True):
        if repair:
            git(repo, "remote", "set-head", "origin", "--auto")
        code, out, _ = git(
            repo, "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD"
        )
        if code == 0 and out:
            target_code, _, _ = git(repo, "rev-parse", "--verify", "--quiet", out)
            if target_code == 0:
                return out
    for candidate in ("origin/main", "origin/master"):
        code, _, _ = git(repo, "rev-parse", "--verify", "--quiet", candidate)
        if code == 0:
            return candidate
    return None


SESSION_REPO_REASON = (
    "The repository this session is currently working in, detected from the "
    "working directory -- not fixed ecosystem-critical content, but a stale "
    "answer here is exactly as misleading to the session reading it."
)


def current_session_repo(home: Path) -> tuple[Path, str] | None:
    """Return (canonical repo root, path relative to $HOME) for the cwd, or None.

    Resolves through ``git rev-parse --git-common-dir`` so a worktree at
    ``<repo>/worktrees/<branch>/`` reports its canonical repo root, not the
    worktree itself -- a worktree's HEAD is a feature branch, and diffing it
    against origin's default branch would misreport ordinary unmerged commits
    as staleness. Returns None when the cwd is not inside a repo, or when the
    repo root is not under $HOME (TARGETS' paths are HOME-relative by
    convention; a repo outside it cannot be named the same way).
    """
    cwd = Path.cwd()
    code, common_dir, _ = git(cwd, "rev-parse", "--git-common-dir")
    if code != 0 or not common_dir:
        return None
    common_path = Path(common_dir)
    if not common_path.is_absolute():
        common_path = (cwd / common_path).resolve()
    else:
        common_path = common_path.resolve()
    repo_root = common_path.parent
    try:
        rel = repo_root.relative_to(home)
    except ValueError:
        return None
    return repo_root, str(rel)


def refresh(repo: Path) -> dict:
    """Fetch, then fast-forward if it is safe to try. Never discards anything.

    ``unknown`` marks a result where the check itself could not run to a real
    ahead/behind count. ``noncanonical`` marks a dirty tree, wrong branch, or
    local-only/diverged history. A caller must never fold either into
    "current": that is precisely the failure mode this script exists to prevent.
    """
    result: dict = {
        "path": str(repo), "fetched": False, "behind": None, "ahead": None,
        "advanced": False, "unknown": False, "noncanonical": False, "note": "",
    }

    code, _, err = git(repo, "fetch", "--quiet", "origin", timeout=FETCH_TIMEOUT_SECONDS)
    if code != 0:
        result["note"] = f"fetch failed: {err.splitlines()[-1] if err else 'unknown error'}"
        return result
    result["fetched"] = True

    upstream = upstream_ref(repo)
    if upstream is None:
        result["unknown"] = True
        result["note"] = "no origin/HEAD and neither origin/main nor origin/master exists"
        return result
    result["upstream"] = upstream

    code, shallow, _ = git(repo, "rev-parse", "--is-shallow-repository")
    if code == 0 and shallow == "true":
        head_code, head, _ = git(repo, "rev-parse", "--verify", "HEAD^{commit}")
        upstream_code, upstream_tip, _ = git(
            repo, "rev-parse", "--verify", f"{upstream}^{{commit}}"
        )
        if head_code != 0 or upstream_code != 0:
            result["unknown"] = True
            result["note"] = "shallow clone; HEAD or upstream tip could not be resolved"
            return result
        if head == upstream_tip:
            result["behind"] = 0
            result["ahead"] = 0
        ancestor_code, _, _ = git(repo, "merge-base", "--is-ancestor", "HEAD", upstream)
        if head != upstream_tip and ancestor_code != 0:
            result["unknown"] = True
            result["note"] = (
                "shallow clone; HEAD is not provably an ancestor of the fetched upstream"
            )
            return result

    code, counts, _ = git(repo, "rev-list", "--left-right", "--count", f"HEAD...{upstream}")
    parts = counts.split()
    if code != 0 or len(parts) != 2 or not all(part.isdigit() for part in parts):
        result["unknown"] = True
        result["note"] = "could not count commits ahead of and behind upstream"
        return result
    result["ahead"], result["behind"] = map(int, parts)

    # Exact revision equality is not enough for a canonical checkout: a dirty
    # tree or a feature branch at that revision still answers from noncanonical
    # local state. Observe both before returning a green result.
    code, dirty, _ = git(repo, "status", "--porcelain")
    if code != 0:
        result["unknown"] = True
        result["note"] = "could not read status; left alone"
        return result
    code, head_branch, _ = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    default_branch = upstream.removeprefix("origin/")
    if code != 0:
        result["unknown"] = True
        result["note"] = "could not read current branch; left alone"
        return result
    if result["ahead"]:
        result["noncanonical"] = True
        if result["behind"]:
            result["note"] = (
                f"HEAD diverged from {upstream}: {result['ahead']} commit(s) ahead and "
                f"{result['behind']} behind; left alone"
            )
        else:
            result["note"] = f"HEAD is {result['ahead']} commit(s) ahead of {upstream}; left alone"
        return result
    if dirty:
        # Merged-work residue (files identical to upstream) used to be cleared through Project Meta's lock
        # controller. AES has none, so a dirty tree is left alone and the stuck-checkout concern says how to unstick it.
        result["noncanonical"] = True
        behind_note = f" and {result['behind']} commit(s) behind {upstream}" if result["behind"] else ""
        result["note"] = f"{len(dirty.splitlines())} uncommitted change(s){behind_note}; left alone"
        return result
    if head_branch != default_branch:
        result["noncanonical"] = True
        behind_note = f" and {result['behind']} commit(s) behind {upstream}" if result["behind"] else ""
        result["note"] = (
            f"on branch '{head_branch}', not the default branch{behind_note}; left alone"
        )
        return result
    if result["behind"] == 0:
        return result

    if (repo / ".git" / LOCK_RECEIPT_NAME).exists():
        result["noncanonical"] = True
        result["note"] = f"{result['behind']} commit(s) behind; canonical lock receipt present and AES has no lock controller; left alone"
        return result

    code, _, err = git(repo, "merge", "--ff-only", upstream, timeout=30)
    if code == 0:
        result["advanced"] = True
        result["behind"] = 0
        result["ahead"] = 0
        return result

    detail = err.splitlines()[-1] if err else "fast-forward refused"
    if "unable to unlink" in err or "Permission denied" in err:
        detail = "read-only working tree (unlink needs write permission on the directory, not the file)"
    result["note"] = f"could not fast-forward: {detail}"
    return result


def _report(results: list[dict], args: argparse.Namespace, *, throttled: bool) -> int:
    """Print (or JSON-emit) results and return the exit code -- shared by the
    fresh-fetch path and the throttled/cached-stamp path, so a persistent
    problem is reported every time this is invoked, not only the one run that
    happened to observe it first.
    """
    stale = [r for r in results if r.get("behind") and not r.get("noncanonical")]
    advanced = [r for r in results if r["advanced"]]
    failed = [r for r in results if not r["fetched"]]
    unknown = [r for r in results if r.get("unknown")]
    noncanonical = [r for r in results if r.get("noncanonical")]

    if args.json:
        print(json.dumps({"results": results, "throttled": throttled}, indent=1))
        return 1 if ((stale or noncanonical or unknown or failed) and args.strict) else 0

    if not results:
        # An empty sweep must not read as "all current": that is the silent-staleness failure this script exists to prevent.
        print("canonical checkouts: NOTHING WAS CHECKED (TARGETS is empty and the working directory is not in a repository under $HOME).")
        return 1 if args.strict else 0

    if not stale and not noncanonical and not failed and not unknown:
        if not args.quiet:
            moved = f", {len(advanced)} fast-forwarded" if advanced else ""
            note = " (cached, not re-fetched this run)" if throttled else ""
            print(f"canonical checkouts: {len(results)} fetched, all current{moved}{note}.")
        return 0

    prefix = "[cached from an earlier run within --min-interval-hours; not re-fetched] " if throttled else ""
    for row in failed:
        print(f"{prefix}CANONICAL CHECKOUT UNREACHABLE: ~/{row['name']} -- {row['note']}")
    for row in unknown:
        print(f"{prefix}CANONICAL CHECKOUT FRESHNESS UNKNOWN: ~/{row['name']} -- {row['note']}")
    for row in noncanonical:
        print(f"{prefix}NONCANONICAL CHECKOUT STATE: ~/{row['name']} -- {row['note']}")
    for row in stale:
        print(f"{prefix}STALE CANONICAL CHECKOUT: ~/{row['name']} is {row['behind']} commit(s) behind {row.get('upstream', 'origin')}.")
        print(f"  {row['note']}")
        print(f"  Its remote refs ARE current. Read facts with: git -C ~/{row['name']} show {row.get('upstream', 'origin/main')}:<path>")
        reason = row["reason"]
        purpose = reason[0].lower() + reason[1:] if reason else "authoritative project content."
        print(f"  Do not trust its working tree for {purpose}")
    # `failed` (unreachable -- fetch failed, or now also "no .git at that
    # path") is at least as bad as `stale`/`unknown` for --strict's purpose: a
    # target that was never actually checked must not pass silently either.
    return 1 if ((stale or noncanonical or unknown or failed) and args.strict) else 0


# A graph checkout held behind by local changes is skipped every hour, by
# design, and the skip only reached the journal. On 2026-10-12 the AES
# canonical checkout -- whose CLAUDE.md the instruction loader serves -- had
# been 494 commits behind for a week behind one stray edit already saved on a
# remote branch, and nine more checkouts were stuck the same way. The sweep
# now keeps one keyed concern open while any checkout is that far behind.
STUCK_BEHIND_THRESHOLD = 20
STUCK_CONCERN_KEY = "graph-checkouts-stuck-behind"
STUCK_CONCERN_SOURCE = "graph-checkout-sync"


def stuck_rows(results: list[dict], threshold: int = STUCK_BEHIND_THRESHOLD) -> list[dict]:
    """Checkouts the sweep left alone that are at least ``threshold`` commits behind."""
    rows = [r for r in results if r.get("noncanonical") and (r.get("behind") or 0) >= threshold]
    return sorted(rows, key=lambda r: (-(r.get("behind") or 0), r.get("name", "")))


def _load_concern_issue():
    import importlib.util

    spec = importlib.util.spec_from_file_location("concern_issue", Path(__file__).resolve().parent / "concern_issue.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["concern_issue"] = module
    spec.loader.exec_module(module)
    return module


def route_stuck_concern(results: list[dict], threshold: int = STUCK_BEHIND_THRESHOLD, run=None) -> str:
    """Open (or refresh) the stuck-checkout concern, or close it when none remain."""
    ci = _load_concern_issue()
    run = run or ci.gh_runner
    stuck = stuck_rows(results, threshold)
    if not stuck:
        return ci.close_concern(
            setting("concern_repo", "CONCERN_REPO"), STUCK_CONCERN_KEY,
            f"The graph checkout sweep found no checkout held {threshold}+ commits behind by local changes.", run,
        )
    lines = [f"- `~/{r['name']}`: {r['behind']} commits behind; {r.get('note', '')}" for r in stuck]
    body = (
        f"The hourly graph checkout sweep (`scripts/refresh_canonical_checkouts.py --all-graph`) left "
        f"{len(stuck)} checkout(s) at least {threshold} commits behind their remote because of local changes. "
        "Agents and the instruction loader read these working trees, so they get outdated files.\n\n"
        + "\n".join(lines)
        + "\n\n**To unstick one:** for each local change, check whether it is already "
        "on a remote branch (`git branch -r --contains`, byte-compare); if it is, park it with a named "
        "`git stash push -m <why> -- <path>`, otherwise commit it to a branch and push. Then "
        "`git merge --ff-only origin/<default>`. Never discard work that exists only locally.\n\n"
        "Trace-Review: none (checkout freshness report; no model or pipeline run is assessed)"
    )
    occurrence = ",".join(sorted(r["name"] for r in stuck))
    title = f"{len(stuck)} checkout(s) stuck {threshold}+ commits behind their remote"
    return ci.open_concern(
        setting("concern_repo", "CONCERN_REPO"), STUCK_CONCERN_KEY, title, body, STUCK_CONCERN_SOURCE, run, occurrence=occurrence,
    )


def canonical_roots(project_graph: Path) -> dict[Path, str]:
    """Map resolved shared-checkout roots to Project Graph ids."""
    roots: dict[Path, str] = {}
    for record in json.loads(project_graph.read_text(encoding="utf-8")):
        raw = record.get("path")
        if not raw:
            continue
        path = Path(raw).expanduser()
        if not (path / ".git").exists():
            continue
        done = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--path-format=absolute", "--git-common-dir", "--git-dir"],
            capture_output=True, text=True, check=False,
        )
        lines = done.stdout.split()
        if done.returncode != 0 or len(lines) != 2 or lines[0] != lines[1]:
            continue  # a linked worktree registered as a project is not a shared checkout
        roots[path.resolve()] = record.get("id") or str(path)
    return roots


def in_place_project_ids(graph: Path) -> set[str]:
    """Project ids a scheduled unit operates on in place (mirror refreshes), from the baseline file; none when absent."""
    baseline = Path(os.environ.get("IN_PLACE_BASELINE") or graph.parent / "unattended_execution_sources_baseline.json")
    if not baseline.is_file():
        return set()
    pairs = json.loads(baseline.read_text(encoding="utf-8")).get("intended_in_place") or {}
    return {pair.split("|", 1)[1] for pair in pairs if "|" in pair}


GRAPH_REASON = "Registered in the project graph (--all-graph sweep)."


def graph_targets(home: Path, graph: Path | None = None) -> list[str]:
    """Home-relative canonical checkouts for every Project Graph repository.

    TARGETS is deliberately short, so on 2026-09-26 most of the ~210 registered
    checkouts had no scheduled refresh at all: brians-2nd-brain-integration-work
    was 34 commits behind origin and onto-canon6 21, and a commit review read
    both as current. ``--all-graph`` applies the same never-discard refresh to
    every registered checkout. Checkouts a unit intentionally operates on in
    place (the mirror refreshes) are skipped: refreshing would fight that unit.
    """
    graph = graph or GRAPH_DEFAULT
    if not graph.is_file():
        raise SystemExit(f"--all-graph needs the project graph, not found at {graph}: set PROJECT_GRAPH")
    in_place_ids = in_place_project_ids(graph)
    real_home = Path(os.path.realpath(home))
    roots = canonical_roots(graph)
    # Submodules nested in an in-place mirror are that mirror's to move too.
    in_place_roots = [root for root, project_id in roots.items() if project_id in in_place_ids]
    out = []
    for root, project_id in sorted(roots.items(), key=lambda item: str(item[0])):
        if any(root.is_relative_to(mirror) for mirror in in_place_roots):
            continue
        try:
            out.append(str(root.relative_to(real_home)))
        except ValueError:
            continue  # outside $HOME: this refresher only addresses home-relative paths
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--targets", nargs="*", help="Override the target list (paths relative to $HOME).")
    parser.add_argument("--min-interval-hours", type=float, default=0.0,
                        help="Skip entirely if the last run was more recent than this.")
    parser.add_argument("--quiet", action="store_true",
                        help="Print nothing when every target is current.")
    parser.add_argument("--strict", action="store_true",
                        help="Exit 1 when a target is stale, noncanonical, or unknown.")
    parser.add_argument("--no-session-repo", action="store_true",
                        help="Do not auto-add the session's current working repo "
                             "(default target list only; ignored with --targets).")
    parser.add_argument("--all-graph", action="store_true",
                        help="Refresh every PROJECT_GRAPH checkout under $HOME in addition to TARGETS. "
                             "Does not read or write the throttle stamp.")
    parser.add_argument("--stuck-threshold", type=int, default=STUCK_BEHIND_THRESHOLD,
                        help="With --all-graph: open a concern for checkouts left this many commits behind.")
    parser.add_argument("--no-concern", action="store_true",
                        help="With --all-graph: report only; do not open or close the stuck-checkout concern.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.all_graph and args.targets:
        parser.error("--all-graph and --targets are mutually exclusive")

    if args.min_interval_hours and STAMP.exists() and not args.all_graph:
        try:
            stamp_payload = json.loads(STAMP.read_text(encoding="utf-8"))
            last = stamp_payload.get("ran_at", 0)
            if time.time() - last < args.min_interval_hours * 3600:
                # Skip the redundant fetch, but never skip reporting a real,
                # still-unresolved problem the last run already found -- a
                # persistent dirty/stale canonical checkout must not go silent
                # just because this session isn't the one that first noticed
                # it. Fail open (fall through to a real run) on any malformed
                # or missing cached results, same as any other stamp read.
                cached_results = stamp_payload.get("results")
                if isinstance(cached_results, list) and cached_results:
                    return _report(cached_results, args, throttled=True)
                return 0
        except (OSError, ValueError):
            pass

    home = Path.home()
    reasons = dict(TARGETS)
    wanted = args.targets if args.targets else list(TARGETS)
    if args.all_graph:
        for rel in graph_targets(home):
            if os.path.realpath(home / rel) not in {os.path.realpath(home / w) for w in wanted}:
                wanted = [*wanted, rel]
                reasons.setdefault(rel, GRAPH_REASON)
    if not args.targets and not args.no_session_repo:
        detected = current_session_repo(home)
        if detected is not None:
            _repo_root, rel = detected
            if rel not in wanted:
                wanted = [*wanted, rel]
                reasons.setdefault(rel, SESSION_REPO_REASON)
    if args.targets:
        wanted = [resolve_target(rel, TARGETS) for rel in wanted]

    results = []
    for rel in wanted:
        repo = home / rel
        if not (repo / ".git").exists():
            # A bare `continue` here previously vanished the target from
            # `results` entirely, so an empty result set read as "0 fetched,
            # all current" -- a false positive reproducing the exact silent-
            # staleness failure this script exists to prevent. Report it as
            # unreachable instead, same as a real fetch failure.
            results.append(
                {
                    "path": str(repo), "fetched": False, "behind": None,
                    "advanced": False, "unknown": False,
                    "note": f"no .git at ~/{rel}; not a real checkout path",
                    "name": rel, "reason": reasons.get(rel, ""),
                }
            )
            continue
        outcome = refresh(repo)
        outcome["name"] = rel
        outcome["reason"] = reasons.get(rel, "")
        results.append(outcome)

    # The stamp feeds the session-start hook's cached report; a graph-wide
    # sweep's ~200 rows would replace the critical-target view it relies on.
    if args.all_graph:
        code = _report(results, args, throttled=False)
        if args.no_concern:
            return code
        try:
            outcome = route_stuck_concern(results, args.stuck_threshold)
        except Exception as exc:  # noqa: BLE001 - a dead alarm must fail the unit, not vanish
            print(f"STUCK-CHECKOUT CONCERN ROUTING FAILED: {exc}", file=sys.stderr)
            return 1
        print(f"stuck-checkout concern: {outcome}", file=sys.stderr)
        return code
    try:
        STAMP.parent.mkdir(parents=True, exist_ok=True)
        STAMP.write_text(json.dumps({"ran_at": time.time(), "results": results}, indent=1), encoding="utf-8")
    except OSError:
        pass  # A missing stamp costs a redundant fetch, not correctness.

    return _report(results, args, throttled=False)


if __name__ == "__main__":
    raise SystemExit(main())

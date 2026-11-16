#!/usr/bin/env python3
"""Keep the project graph and its page current: the daily job behind `project-graph-refresh.timer`.

Each day this, on a staging copy of the graph (with its settings files beside it):

  a. registers GitHub repositories with no record (project_graph_sync.py --write);
  b. refills `depends_on` from real use in code (check_capability_consumption.py --write). This reads every Python
     file and can take many minutes; day-old links are far better than a stale page, so its failure is reported
     but the run carries on;
  c. refuses to continue if the graph fails its taxonomy check (--fail-on hard). The live graph is untouched;
  d. only when the graph really changed: copies it over the live PROJECT_GRAPH.json and lands it in the
     private settings repository that holds it (aes-config): one commit of that file and `git push origin HEAD:main`.
     That repository holds records only and has no check, so there is no pull request. Fail closed: it must be on
     main and clean before the run (then `pull --ff-only`) and clean after the commit; nothing is ever forced.
     A refused landing does not stop the page; it is reported;
  e. rebuilds the activity snapshot (build_project_activity.py) and
  f. the "My projects" page (code2-workspace scripts/build_project_graph_page.py, from a runtime clone of that
     repository's main), and pushes both to its data branch (`shaping/project-graph-data`), where the private plan
     site serves them. Main's copy of the page only points there.

Every step is timed and appended to one log per day, ~/projects/data/logs/project-graph-refresh-YYYY-MM-DD.log, with
its command, exit status and output. A failed step stops the run, pushes nothing further, and opens the keyed concern
`project-graph-refresh` in the configured concern repository; a later good run closes it.

    python3 scripts/project_graph_refresh.py             # the daily run
    python3 scripts/project_graph_refresh.py --no-push   # every step, but nothing committed, pushed or filed
Exit 0 when every step passed, 1 when one failed, 2 when a setting is missing.

Rewritten from Project Meta scripts/project_graph_refresh.py (retirement plan step 4, Decision 20). Dropped: the
runtime clone of project-meta, landing through `ship`, and the ten pages derived from the graph. The graph is named
by PROJECT_GRAPH, else ~/code2/aes-config/PROJECT_GRAPH.json. Settings come from `graph-config.yaml` beside it:
`concern_repo`, `ssh_host_alias`, `graph_page` (`repo`, `data_branch`, `viewer`) and `git_identity` (`name`,
`email`). PROJECT_GRAPH_REFRESH_RUNTIME and PROJECT_GRAPH_REFRESH_LOG_DIR move the clones and the log.
Implements: project-graph-refresh/step-log
Implements: project-graph-refresh/graph-lands-in-settings-repo
Implements: project-graph-refresh/page-goes-to-data-branch
Implements: project-graph-refresh/failure-opens-one-concern
"""

import argparse
import filecmp
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import workspace_map as wm  # noqa: E402

LOG_DIR = Path(os.environ.get("PROJECT_GRAPH_REFRESH_LOG_DIR") or Path.home() / "projects/data/logs")
RUNTIME = Path(os.environ.get("PROJECT_GRAPH_REFRESH_RUNTIME") or Path.home() / ".local/share/ecosystem-runtime/project-graph-refresh")
PAGE = "docs/plans/project-graph.review.html"
ACTIVITY = "docs/plans/project_activity.json"
WORKSPACE_CLONE, DATA_CLONE, STAGING = "code2-workspace", "code2-workspace-data", "staging"
SETTINGS_FILES = ("graph-config.yaml", "workspace_map_extras.yaml")  # read beside the graph by the steps
CONCERN = "project-graph-refresh"
SCAN_TIMEOUT = 2700      # seconds, as before; the job's unit allows 90 minutes in all
ACTIVITY_TIMEOUT = 1800  # usually 2-7 minutes; under daytime disk load it passed 900 s (2026-11-05)


class StepFailed(RuntimeError):
    """A step exited non-zero; the message names it."""


def settings():
    """The refresh settings from graph-config.yaml beside the graph; a missing one is a loud stop."""
    cfg = wm.graph_config()
    page, who = cfg.get("graph_page") or {}, cfg.get("git_identity") or {}
    needed = {"concern_repo": cfg.get("concern_repo"), "ssh_host_alias": cfg.get("ssh_host_alias"),
              "graph_page.repo": page.get("repo"), "graph_page.data_branch": page.get("data_branch"),
              "graph_page.viewer": page.get("viewer"), "git_identity.name": who.get("name"),
              "git_identity.email": who.get("email")}
    absent = [k for k, v in needed.items() if not v]
    if absent:
        raise wm.ConfigMissing(f"project_graph_refresh: no {', '.join(absent)} in {wm.config_path()}")
    return {**needed, "remote": f"git@{cfg['ssh_host_alias']}:{page['repo']}.git"}


def identity(s):
    return ["-c", f"user.name={s['git_identity.name']}", "-c", f"user.email={s['git_identity.email']}"]


def run_group(cmd, cwd, timeout):
    """Run a command in its own process group. On timeout kill the whole group: subprocess.run alone kills only
    the parent, and the scan's worker processes then kept running after the first real run failed."""
    proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.communicate()
        raise
    return subprocess.CompletedProcess(cmd, proc.returncode, stdout, stderr)


class Run:
    """Runs commands, each timed and written whole to the day's log."""

    def __init__(self, log_dir=None):
        log_dir = Path(log_dir or LOG_DIR)
        log_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = log_dir / f"project-graph-refresh-{time.strftime('%Y-%m-%d')}.log"

    def log(self, text):
        line = f"{time.strftime('%H:%M:%S')} {text}"
        print(line, flush=True)
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    def __call__(self, name, cmd, cwd=None, check=True, timeout=900):
        start = time.time()
        out = run_group(cmd, cwd, timeout)
        self.log(f"step={name} exit={out.returncode} seconds={time.time() - start:.1f} cmd={' '.join(map(str, cmd))}")
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write((out.stdout + out.stderr)[-20000:] + "\n")
        if check and out.returncode != 0:
            raise StepFailed(f"{name} exit {out.returncode}: {(out.stderr or out.stdout).strip()[-400:]}")
        return out


def prepare_workspace(run, s):
    """A runtime clone of the page builder's repository, reset to its main branch. It belongs to this job alone."""
    path = RUNTIME / WORKSPACE_CLONE
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        run("clone-workspace", ["git", "clone", "--quiet", s["remote"], str(path)], timeout=600)
    run("fetch-workspace", ["git", "-C", str(path), "fetch", "--quiet", "origin", "main"])
    run("reset-workspace", ["git", "-C", str(path), "checkout", "--quiet", "--force", "-B", "main", "origin/main"])
    return path


def prepare_data_branch(run, s):
    """Check out the data branch in a clone of its own, starting it with no history the first time. It holds only
    generated files, so it never carries a copy of the workspace's code or planning package."""
    path = RUNTIME / DATA_CLONE
    if not (path / ".git").exists():
        path.mkdir(parents=True, exist_ok=True)
        run("init-data", ["git", "-C", str(path), "init", "--quiet"])
        run("remote-data", ["git", "-C", str(path), "remote", "add", "origin", s["remote"]])
    run("identity-data", ["git", "-C", str(path), "config", "user.name", s["git_identity.name"]])
    run("identity-email-data", ["git", "-C", str(path), "config", "user.email", s["git_identity.email"]])
    branch = s["graph_page.data_branch"]
    heads = run("find-data-branch", ["git", "-C", str(path), "ls-remote", "--heads", "origin", branch])
    if heads.stdout.strip():
        run("fetch-data", ["git", "-C", str(path), "fetch", "--quiet", "origin", branch])
        run("reset-data", ["git", "-C", str(path), "checkout", "--quiet", "--force", "-B", "data", "FETCH_HEAD"])
    else:
        run("start-data", ["git", "-C", str(path), "symbolic-ref", "HEAD", "refs/heads/data"])
    (path / PAGE).parent.mkdir(parents=True, exist_ok=True)
    return path


def publish_data(run, path, day, push, branch):
    """Commit the page and the activity snapshot to the data branch and push them."""
    run("add-data", ["git", "-C", str(path), "add", "--", PAGE, ACTIVITY])
    if run("diff-data", ["git", "-C", str(path), "diff", "--cached", "--quiet"], check=False).returncode == 0:
        run.log("nothing changed on the data branch")
        return
    if not push:
        run.log("--no-push: the data branch has changes, not committed")
        return
    run("commit-data", ["git", "-C", str(path), "commit", "--quiet", "-m", f"Project graph data: {day}"])
    run("push-data", ["git", "-C", str(path), "push", "--quiet", "origin", f"HEAD:refs/heads/{branch}"])


def stage_graph(live):
    """Copy the live graph and the settings beside it to the staging folder; the steps work on that copy."""
    staging = RUNTIME / STAGING
    staging.mkdir(parents=True, exist_ok=True)
    for name in SETTINGS_FILES:
        if (live.parent / name).exists():
            shutil.copyfile(live.parent / name, staging / name)
    shutil.copyfile(live, staging / live.name)
    return staging / live.name


def clean_on_main(run, repo):
    """None when the settings repository is on main with nothing uncommitted, else the reason it is not."""
    head = run("graph-repo-branch", ["git", "-C", str(repo), "symbolic-ref", "--short", "HEAD"], check=False)
    if head.returncode != 0 or head.stdout.strip() != "main":
        return f"{repo} is not on main ({head.stdout.strip() or head.stderr.strip()})"
    status = run("graph-repo-status", ["git", "-C", str(repo), "status", "--porcelain"], check=False)
    if status.returncode != 0 or status.stdout.strip():
        return f"{repo} has uncommitted changes: {status.stdout.strip()[:300] or status.stderr.strip()[:300]}"
    return None


def prepare_graph_repo(run, live):
    """Before any step: the settings repository must be on main and clean, then fast-forward it. Returns a problem
    (the graph is then not landed this run) or None."""
    problem = clean_on_main(run, live.parent)
    if problem:
        return problem
    pulled = run("graph-repo-pull", ["git", "-C", str(live.parent), "pull", "--ff-only", "--quiet"], check=False)
    return None if pulled.returncode == 0 else f"pull --ff-only in {live.parent} exit {pulled.returncode}: {pulled.stderr.strip()[-300:]}"


def land_graph(run, live, staged, s, push, blocked):
    """Copy a changed graph over the live one and push it to the settings repository's main. Returns a problem or None."""
    if filecmp.cmp(live, staged, shallow=False):
        run.log(f"{live.name} unchanged; nothing to land")
        return None
    if not push:
        run.log(f"--no-push: the graph changed, not landed (staged copy: {staged})")
        return None
    if blocked:
        return f"graph changes were not landed: {blocked}"
    repo = live.parent
    problem = clean_on_main(run, repo)  # another writer may have left changes since the start
    if problem:
        return f"graph changes were not landed: {problem}"
    shutil.copyfile(staged, live)
    git = ["git", "-C", str(repo)]
    for name, cmd in (("add-graph", git + ["add", "--", live.name]),
                      ("commit-graph", git + identity(s) + ["commit", "--quiet", "-m", "Project graph: new records or dependency links"])):
        out = run(name, cmd, check=False)
        if out.returncode != 0:
            return f"graph changes were not landed: {name} exit {out.returncode}: {(out.stderr or out.stdout).strip()[-300:]}"
    problem = clean_on_main(run, repo)
    if problem:
        return f"graph committed but not pushed: {problem}"
    pushed = run("push-graph", git + ["push", "--quiet", "origin", "HEAD:main"], check=False)
    if pushed.returncode != 0:
        return f"graph committed but not pushed, exit {pushed.returncode}: {pushed.stderr.strip()[-300:]}"
    return None


def refresh(run, push, live, s, scan=True):
    """Run every step. Returns the problems that did not stop the run; a problem that should stop it raises."""
    problems = []
    blocked = prepare_graph_repo(run, live) if push else None
    if blocked:
        run.log(f"the graph will not be landed this run: {blocked}")
    workspace = prepare_workspace(run, s)
    data = prepare_data_branch(run, s)
    staged = stage_graph(live)
    py = sys.executable
    run("register-new-repositories", [py, str(HERE / "project_graph_sync.py"), "--graph", str(staged), "--write"])
    try:
        if not scan:
            run.log("--skip-scan: depends_on left as it is")
        else:
            run("fill-depends-on", [py, str(HERE / "check_capability_consumption.py"), "--project-graph", str(staged), "--write"],
                timeout=SCAN_TIMEOUT)
    except (StepFailed, subprocess.TimeoutExpired) as exc:
        run.log(f"continuing without new depends_on links: {str(exc)[:300]}")
        problems.append(f"depends_on scan: {str(exc)[:300]}")
    run("taxonomy", [py, str(HERE / "check_project_graph_taxonomy.py"), "--project-graph", str(staged), "--fail-on", "hard"])
    landing = land_graph(run, live, staged, s, push, blocked)
    if landing:
        run.log(f"continuing with the page: {landing}")
        problems.append(landing)
    run("activity", [py, str(HERE / "build_project_activity.py"), "--project-graph", str(staged), "--output", str(data / ACTIVITY)],
        timeout=ACTIVITY_TIMEOUT)
    run("page", [py, "scripts/build_project_graph_page.py", "--graph", str(staged), "--activity", str(data / ACTIVITY),
                 "--viewer", s["graph_page.viewer"], "--out", str(data / PAGE)], cwd=workspace)
    publish_data(run, data, time.strftime("%Y-%m-%d"), push, s["graph_page.data_branch"])
    return problems


def report(run, concern, problems, repo):
    """Open the keyed concern for the problems, or close it after a clean run. A concern that cannot be filed
    fails the run, so the unit shows as failed and failed-unit-watch still reports it."""
    if problems:
        args = ["open", "--repo", repo, "--key", CONCERN, "--title", "Daily project graph refresh failed",
                "--source", CONCERN, "--no-run-claim", "reports a failed step; the trace is the log named in the body",
                "--body", "\n".join(problems) + f"\n\nFull trace: {run.log_path}"]
    else:
        args = ["close", "--repo", repo, "--key", CONCERN, "--evidence", f"Clean run, trace in {run.log_path}"]
    return run("concern", concern + args, check=False).returncode == 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--no-push", action="store_true", help="run every step but commit, push and file nothing")
    ap.add_argument("--skip-scan", action="store_true", help="leave depends_on alone: the scan takes many minutes")
    args = ap.parse_args(argv)
    try:
        s = settings()
    except wm.ConfigMissing as exc:
        print(f"CRASH: {exc}", file=sys.stderr)
        return 2
    run = Run()
    start = time.time()
    try:
        problems = refresh(run, push=not args.no_push, live=Path(wm.graph_path()), s=s, scan=not args.skip_scan)
    except (StepFailed, subprocess.TimeoutExpired, OSError) as exc:
        problems = [f"run stopped: {exc}"]
    outcome = f"{len(problems)} problem(s): {problems}" if problems else "OK"
    run.log(f"{outcome} after {time.time() - start:.0f}s; exit {1 if problems else 0}")
    filed = args.no_push or report(run, [sys.executable, str(HERE / "concern_issue.py")], problems, s["concern_repo"])
    return 1 if problems or not filed else 0


if __name__ == "__main__":
    raise SystemExit(main())

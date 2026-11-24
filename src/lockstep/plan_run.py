"""Run one OpenSpec plan with hidden acceptance tests and a departure report (spec plan-run).

Implements: plan-run/a-departure-report-compares-the-change-with-its-plan
Implements: plan-run/hidden-acceptance-tests-are-written-before-and-run-after-implementation
Implements: plan-run/one-driver-runs-a-plan-with-claude-or-codex
Implements: plan-run/the-agents-are-told-to-lay-out-the-planned-files

`lockstep accept write <change>` has a separate headless agent session write pytest files from the plan
into a run folder outside every worktree; `lockstep accept check <change>`, run in the implementer's
worktree after its last commit, copies them in, runs them, removes them, runs the check command and writes
the departure report; `lockstep run-plan <change>` does both around one headless implementer session. All
three report; none merges. Everything a run did is kept in its run folder
(`${XDG_STATE_HOME:-~/.local/state}/lockstep-runs/<repository>/<run id>/`).

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:plan_run.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: plan-run/a-departure-report-compares-the-change-with-its-plan, plan-run/hidden-acceptance-tests-are-written-before-and-run-after-implementation, plan-run/one-driver-runs-a-plan-with-claude-or-codex, plan-run/the-agents-are-told-to-lay-out-the-planned-files

### Requirement: A departure report compares the change with its plan

The departure report SHALL list every file changed in commits since `REF` whose repository-relative path does not appear in the change's `tasks.md` as read from `REF` and is neither the `path` of a `layout:` row in `lockstep.yaml` as read from `REF` nor a file one of those rows names in its `tests:`, excluding files under `openspec/`, the OpenSpec spec links `make docs-specs` writes under `docs/specs/`, `lockstep.yaml` itself and the generated `docs/links.json`, and every task line still unticked in the change's `tasks.md` at the branch head, read from `openspec/changes/<change>/` or, once archived, from the latest `openspec/changes/archive/YYYY-MM-DD-<change>/`. It reports and never blocks.

Source: Brian, 2026-11-20: "the goal is to give a well specified plan to an agent on some proejct nad have it faithfulyy and successfully impelemnt it"; report-only, inferred by agent from minimal-core-2026-11-20.md C4 and K5 (a check becomes blocking only after it is shown to catch something).

#### Scenario: A file outside the tasks is listed

- **GIVEN** a change whose `tasks.md` at `REF` names `src/app.py`, and commits since `REF` that changed `src/app.py`, `src/other.py`, `tests/test_new.py` and the change's `tasks.md`
- **WHEN** the departure report runs
- **THEN** it lists `src/other.py` and `tests/test_new.py` as outside the tasks and lists neither `src/app.py` nor the OpenSpec file

#### Scenario: A name added to tasks.md after REF does not count

- **GIVEN** the implementer added `src/other.py` to `tasks.md` in its own commit
- **WHEN** the departure report runs
- **THEN** `src/other.py` is still listed as outside the tasks

#### Scenario: An unticked task is listed, archived or not

- **GIVEN** the change was archived to `openspec/changes/archive/2026-11-20-<change>/` with one `- [x]` line and one `- [ ]` line in its `tasks.md`
- **WHEN** the departure report runs with the change's name
- **THEN** it lists the `- [ ]` line as unticked and not the ticked one

Source: Brian, 2026-11-23: "i approve", item (c) of `docs/planning/back-on-design-2026-11-23.md` (a plan names its files in `layout:` rows); plan `docs/planning/template-layout-2026-11-23.md`, step 3.

#### Scenario: A file planned by a layout row at REF is not listed

- **GIVEN** `lockstep.yaml` at `REF` has a `layout:` row with path `src/planned.py`, `tasks.md` does not name it, and commits since `REF` added `src/planned.py`, changed `lockstep.yaml` and added `src/late.py`, whose row was added after `REF`
- **WHEN** the departure report runs
- **THEN** it lists `src/late.py` and lists neither `src/planned.py` nor `lockstep.yaml`

Source: inferred by agent from the template-layout proof run of 2026-11-23 (docs/evidence/template-layout-proof-2026-11-23/summary.json): the row's own test file and the `docs/specs/` link of the archived spec were listed as departures although the plan named the one and the other is generated.

#### Scenario: A row's test file and a spec link are not listed

- **GIVEN** `lockstep.yaml` at `REF` has a row for `src/planned.py` whose `tests:` names `tests/test_planned.py`, and commits since `REF` added `tests/test_planned.py`, `docs/specs/greeting/spec.md` and `tests/test_other.py`
- **WHEN** the departure report runs
- **THEN** it lists only `tests/test_other.py`

### Requirement: Hidden acceptance tests are written before and run after implementation

`lockstep accept write <change>` SHALL run one headless agent session, in a detached worktree at `REF` that is removed afterwards and with no session history kept on disk, that writes pytest files into the run folder outside every worktree, and SHALL then run those tests once at `REF` and record the result. `lockstep accept check <change>` SHALL, in the implementer's worktree, count uncommitted files, copy the hidden tests into `tests/` without overwriting any file, run the test command, remove the copies, run the check command, write the departure report, and record the head commit, all results and the transcripts in the run folder's `summary.json`. Neither command merges.

Source: Brian, 2026-11-20: "the goal is to give a well specified plan to an agent on some proejct nad have it faithfulyy and successfully impelemnt it"; "we shoudl start with the minimal core". Procedure from the plan-fidelity test of 2026-11-20 (minimal-core-2026-11-20.md section 4, C3), inferred by agent.

#### Scenario: Hidden tests are outside the worktree until the last commit

- **GIVEN** a repository with an OpenSpec change at `REF`, and a fake runner that writes a test file for the writer session and, for the implementer session, asserts that no hidden test file is in its worktree, then commits an implementation
- **WHEN** `accept write`, the implementer session and `accept check` run
- **THEN** the hidden test file is in the run folder's `accept/`, the fake runner's assertion held, the test was run in the worktree and removed from it, the writer worktree is gone, and `summary.json` records `accept` pass and fail counts, `check_exit`, the departure report, `head` and zero uncommitted files

#### Scenario: A hidden test that passes before implementation is flagged

- **GIVEN** a writer session whose test already passes at `REF`
- **WHEN** `accept write` finishes
- **THEN** `summary.json` records `accept_before` with that pass and the command prints a warning naming it

#### Scenario: A name collision is refused

- **GIVEN** the implementer's worktree already has `tests/test_accept_1.py`
- **WHEN** `accept check` runs
- **THEN** it does not overwrite or remove that file, records the collision, and exits non-zero

#### Scenario: Uncommitted work is reported

- **GIVEN** an implementer session that leaves a changed tracked file uncommitted
- **WHEN** `accept check` runs
- **THEN** `summary.json` records `uncommitted` above zero, counted before the hidden tests are copied in

#### Scenario: The implementer is not told where the tests are

- **WHEN** the implementer prompt and environment are built
- **THEN** neither contains the run folder's path, and `summary.json` counts implementer transcript lines naming `lockstep-runs` or the writer worktree's path as `peek_reads`

### Requirement: One driver runs a plan with Claude or Codex

`lockstep run-plan <change> --agent claude|codex` SHALL run `accept write`, then one headless implementer session in a new worktree on branch `impl/<change>-<run id>`, then `accept check`, saving each session's JSON event stream as its transcript, and SHALL print the `ship` command to run next without running it: `uv run ship` when the repository's `pyproject.toml` depends on `agentic-engineering-system` (which installs `ship`), else `ship`. The agent choice SHALL change only the command that starts each session.

Source: Brian, 2026-09-14: "the answer is always yes" (keep Claude Code and Codex in sync; workspace agents/rule-sources.md, Policy `claude-codex-parity`), via minimal-core-2026-11-20.md K6. Inferred by agent, 2026-11-21 (#994): a second user has `ship` only inside the repository's environment.

#### Scenario: Each agent gets its own command

- **WHEN** `agent_command` is built for `codex` and for `claude` with the same prompt and worktree
- **THEN** the codex command is `codex exec --json` with `-C <worktree>`, the claude command is `claude -p --output-format stream-json` started in the worktree, both carry the prompt, and a session that keeps no history adds `--ephemeral` or `--no-session-persistence`

#### Scenario: The driver does not merge

- **GIVEN** a fake runner whose implementer commits
- **WHEN** `run_plan` finishes
- **THEN** the default branch is unchanged, the implementer branch exists, and the printed output contains the `ship` command

#### Scenario: The printed ship command matches the repository

- **GIVEN** one repository whose `pyproject.toml` lists `agentic-engineering-system` and one that does not
- **WHEN** `ship_command` is asked for each
- **THEN** it gives `uv run ship` for the first and `ship` for the second

### Requirement: The agents are told to lay out the planned files

The implementer's prompt and the acceptance-test writer's prompt SHALL say that when `lockstep.yaml` has `layout:` rows, those rows name the files the plan creates or changes, with their exports; the implementer's prompt SHALL tell it to run `uv run lockstep layout` before writing code, so each new planned file starts with its requirement text.

Source: Brian, 2026-11-23: "i approve", item (c) of `docs/planning/back-on-design-2026-11-23.md`; `proposals/one-planning-tool/DESIGN.md` step 3 (`lockstep layout` creates the planned files before code); plan `docs/planning/template-layout-2026-11-23.md`, step 3.

#### Scenario: The implementer is told to run lockstep layout

- **GIVEN** a change name and a check command
- **WHEN** the implementer's and the writer's prompts are built
- **THEN** the implementer's names `uv run lockstep layout` and `layout:`, and the writer's names `layout:`

Tested by: tests/lockstep/test_lockstep_plan_run.py
[[[end]]]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import shlex
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

RUNS = "lockstep-runs"
DEFAULT_TEST_CMD = "uv run pytest -q"
DEFAULT_CHECK_CMD = "make check"
DEFAULT_TIMEOUT = 3600


class Runner(Protocol):
    def __call__(self, agent: str, prompt: str, cwd: Path, transcript: Path, timeout: int,
                 env: dict[str, str] | None = None, persist: bool = True) -> int: ...


# ---- git helpers ---------------------------------------------------------------------------------


def _git(repo: Path, *args: str, check: bool = True) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def repo_name(repo: Path) -> str:
    """The main checkout's folder name, the same for every worktree of it."""
    common = Path(_git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir"))
    return common.parent.name


def runs_root(repo: Path) -> Path:
    state = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")
    return Path(state) / RUNS / repo_name(repo)


# ---- departure report ----------------------------------------------------------------------------


def _named(path: str, text: str) -> bool:
    """True when the repository-relative path appears in text as a whole path, not as part of a longer one."""
    return re.search(r"(?<![\w/.-])" + re.escape(path) + r"(?![\w/.-])", text) is not None


def _tasks_at(repo: Path, rev: str, change: str) -> tuple[str, str] | None:
    """(path, text) of the change's tasks.md at rev, active or in the latest archive folder."""
    active = f"openspec/changes/{change}/tasks.md"
    files = _git(repo, "ls-tree", "-r", "--name-only", rev, "openspec/changes").splitlines()
    if active in files:
        return active, _git(repo, "show", f"{rev}:{active}")
    pat = re.compile(r"^openspec/changes/archive/(\d{4}-\d{2}-\d{2})-" + re.escape(change) + r"/tasks\.md$")
    archived = sorted(f for f in files if pat.match(f))
    if archived:
        return archived[-1], _git(repo, "show", f"{rev}:{archived[-1]}")
    return None


# The plan file itself and the generated link file change with every planned file; they are never departures.
_NEVER_DEPARTURES = {"lockstep.yaml", "docs/links.json"}


def _layout_paths_at(repo: Path, rev: str) -> set[str]:
    """The `path` of every `layout:` row in lockstep.yaml as it was at rev, and each test file a row names; empty
    when there is none."""
    import yaml

    if "lockstep.yaml" not in _git(repo, "ls-tree", "--name-only", rev).splitlines():
        return set()
    data = yaml.safe_load(_git(repo, "show", f"{rev}:lockstep.yaml")) or {}
    rows = [r for r in (data.get("layout") if isinstance(data, dict) else None) or [] if isinstance(r, dict)]
    paths = {str(r["path"]).strip() for r in rows if r.get("path")}
    tests = {str(t).strip() for r in rows if isinstance(r.get("tests"), list) for t in r["tests"] if str(t).strip()}
    return paths | tests


def departures(repo: Path, change: str, base: str) -> dict[str, Any]:
    """Files changed in commits since base that the plan's tasks.md (as at base) does not name, and unticked tasks."""
    at_base = _tasks_at(repo, base, change)
    if at_base is None:
        raise FileNotFoundError(f"no tasks.md for change {change!r} at {base}")
    plan_text = at_base[1]
    planned = _layout_paths_at(repo, base)
    changed = sorted(p for p in _git(repo, "diff", "--name-only", f"{base}..HEAD").splitlines() if p)
    outside = [p for p in changed if not p.startswith(("openspec/", "docs/specs/")) and p not in _NEVER_DEPARTURES
               and p not in planned and not _named(p, plan_text)]
    at_head = _tasks_at(repo, "HEAD", change)
    head_text = at_head[1] if at_head else plan_text
    unticked = [ln.strip() for ln in head_text.splitlines() if ln.strip().startswith("- [ ]")]
    return {"changed": changed, "outside_tasks": outside, "unticked": unticked,
            "tasks_file": at_head[0] if at_head else at_base[0]}


# ---- agents --------------------------------------------------------------------------------------


def agent_command(agent: str, prompt: str, cwd: Path, persist: bool) -> tuple[list[str], Path]:
    """The argv that starts one headless session of agent in cwd, and the directory to start it in."""
    if agent == "claude":
        argv = ["claude", "-p", "--output-format", "stream-json", "--verbose", "--permission-mode", "bypassPermissions"]
        if not persist:
            argv.append("--no-session-persistence")
        return argv + [prompt], cwd
    if agent == "codex":
        argv = ["codex", "exec", "--json", "--dangerously-bypass-approvals-and-sandbox", "-C", str(cwd)]
        if not persist:
            argv.append("--ephemeral")
        return argv + [prompt], cwd
    raise ValueError(f"unknown agent {agent!r}; use claude or codex")


def default_runner(agent: str, prompt: str, cwd: Path, transcript: Path, timeout: int,
                   env: dict[str, str] | None = None, persist: bool = True) -> int:
    """Run one session, its JSON event stream to transcript and stderr beside it; 124 on timeout."""
    argv, start = agent_command(agent, prompt, cwd, persist)
    with transcript.open("w") as out, transcript.with_suffix(".stderr").open("w") as err:
        try:
            return subprocess.run(argv, cwd=start, stdout=out, stderr=err, stdin=subprocess.DEVNULL,
                                  timeout=timeout, env=env).returncode
        except subprocess.TimeoutExpired:
            err.write(f"\nlockstep: session stopped after {timeout} s\n")
            return 124


# ---- prompts -------------------------------------------------------------------------------------


def writer_prompt(change: str, accept_dir: Path) -> str:
    return f"""ACCEPTANCE TEST WRITER. ACCEPT_DIR={accept_dir}

You are in a detached git worktree at a commit that holds a PLAN: the OpenSpec change openspec/changes/{change}/
(proposal.md, spec delta under specs/, tasks.md). Nothing is implemented yet. Another agent will implement the plan
later without seeing your tests.

- Read the plan, and the existing code and tests it names, for fixtures and import patterns. When lockstep.yaml
  has `layout:` rows, they are part of the plan: the files to create, their requirements and their `exports`.
- Write pytest files named test_accept_<n>.py (n = 1, 2, ...) into ACCEPT_DIR, outside the repository. Each test
  checks one scenario of the spec delta through the interfaces the plan names (its "Test seam" section when there is
  one). Import from the repository the way its tests do: the files will be copied into tests/ before they run.
- Each test has a docstring naming the scenario. Do not copy the plan's own test code.
- No paid model or provider calls: patch them the way existing tests do.
- The tests should fail now, for the expected reason (missing behaviour), not an import error in your own code.
  Check by copying a file into tests/, running it, and deleting the copy.
- Do not change or commit anything in the repository.

At the end, list each test and the scenario it checks."""


def implementer_prompt(change: str, check_cmd: str) -> str:
    check = f"Run `{check_cmd}` until it exits 0." if check_cmd != "none" else "Run the repository's tests."
    return f"""You are in a git worktree on a new branch. Implement the plan in openspec/changes/{change}/ exactly as written.

1. Read proposal.md, the spec delta under specs/, and tasks.md. Read AGENTS.md and the AGENTS.md of each folder you edit.
   When lockstep.yaml has `layout:` rows, they are part of the plan: each names a file to create or change, the
   requirements it implements, its tests and its public functions (`exports`). Run `uv run lockstep layout` before
   writing code; it creates each new planned file with its requirement text.
2. Do the tasks in order. Write each task's test first and see it fail, then make it pass. Tick each task (`- [x]`) when done.
3. When all tasks are done, archive the change: `openspec archive {change} --yes`.
4. {check}
5. Commit with plain `git commit`. If a hook refuses, do what its message asks; do not bypass it.

Stay inside the plan. Do not change files the tasks do not name unless the plan cannot work without it; if you do, or
skip, change or reorder a task, record it as a departure. No paid model or provider calls. Do not push, merge or deploy.
If the plan needs a decision only the repository owner can make, stop and say so.

At the end report: Commits (id and message); Departures (every changed file not named in tasks.md, every task
skipped, changed or reordered, with the reason, or "none"); check result and exit status; every hook refusal, quoted."""


# ---- test runs -----------------------------------------------------------------------------------


def pytest_counts(text: str) -> dict[str, int | None]:
    """Pass, fail and error counts from pytest's final summary line; None when no such line is found."""
    found: dict[str, int | None] = {"passed": None, "failed": None, "errors": None}
    lines = [ln for ln in text.splitlines() if re.search(r"\d+ (passed|failed|errors?)\b", ln)]
    if not lines:
        return found
    last = lines[-1]
    for key, word in (("passed", "passed"), ("failed", "failed"), ("errors", "errors?")):
        m = re.search(r"(\d+) " + word + r"\b", last)
        found[key] = int(m.group(1)) if m else 0
    return found


def _run_tests(cwd: Path, test_cmd: str, files: list[str], log: Path) -> dict[str, Any]:
    cmd = f"{test_cmd} {' '.join(shlex.quote(f) for f in files)}"
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    log.write_text(f"$ {cmd}\n{r.stdout}\n{r.stderr}")
    return {"exit": r.returncode, **pytest_counts(r.stdout)}


def _hidden_files(run_dir: Path) -> list[Path]:
    return sorted((run_dir / "accept").glob("test_accept_*.py"))


def _save(run_dir: Path, summary: dict[str, Any]) -> None:
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def _load(run_dir: Path) -> dict[str, Any]:
    p = run_dir / "summary.json"
    return json.loads(p.read_text()) if p.exists() else {}


# ---- the three steps -----------------------------------------------------------------------------


def accept_write(repo: Path, change: str, ref: str = "HEAD", agent: str = "claude", runner: Runner = default_runner,
                 test_cmd: str = DEFAULT_TEST_CMD, timeout: int = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """A writer session writes hidden tests into a new run folder; they are run once at ref and recorded."""
    repo = repo.resolve()
    sha = _git(repo, "rev-parse", ref)
    if _tasks_at(repo, sha, change) is None:
        raise FileNotFoundError(f"no openspec/changes/{change}/tasks.md at {ref}")
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + secrets.token_hex(2)
    run_dir = runs_root(repo) / run_id
    (run_dir / "accept").mkdir(parents=True)
    writer_wt = Path(tempfile.mkdtemp(prefix="lockstep-writer-")) / "wt"
    _git(repo, "worktree", "add", "--detach", str(writer_wt), sha)
    summary: dict[str, Any] = {"run_id": run_id, "run_dir": str(run_dir), "change": change, "agent": agent,
                               "ref": sha, "writer_worktree": str(writer_wt)}
    try:
        prompt = writer_prompt(change, run_dir / "accept")
        (run_dir / "writer-prompt.md").write_text(prompt)
        summary["writer_exit"] = runner(agent, prompt, writer_wt, run_dir / "writer.jsonl", timeout, env=None, persist=False)
        hidden = _hidden_files(run_dir)
        summary["accept_files"] = [p.name for p in hidden]
        if hidden:
            for p in hidden:
                shutil.copy(p, writer_wt / "tests" / p.name)
            summary["accept_before"] = _run_tests(writer_wt, test_cmd, [f"tests/{p.name}" for p in hidden],
                                                  run_dir / "accept-before.log")
        else:
            summary["accept_before"] = None
    finally:
        _git(repo, "worktree", "remove", "--force", str(writer_wt), check=False)
        shutil.rmtree(writer_wt.parent, ignore_errors=True)
        _git(repo, "worktree", "prune", check=False)
    _save(run_dir, summary)
    before = summary["accept_before"]
    if not summary["accept_files"]:
        print(f"WARNING: the writer session wrote no test_accept_*.py into {run_dir / 'accept'}")
    elif before and before.get("passed"):
        print(f"WARNING: {before['passed']} hidden test(s) already pass before implementation; see {run_dir / 'accept-before.log'}")
    print(f"accept write: run {run_id}, {len(summary['accept_files'])} file(s), before: {before}")
    return summary


def _peek_reads(run_dir: Path, writer_wt: str | None) -> int:
    t = run_dir / "implementer.jsonl"
    if not t.exists():
        return 0
    marks = [RUNS] + ([writer_wt] if writer_wt else [])
    return sum(1 for ln in t.read_text(errors="replace").splitlines() if any(m in ln for m in marks))


def accept_check(worktree: Path, change: str, run_dir: Path, base: str | None = None,
                 test_cmd: str = DEFAULT_TEST_CMD, check_cmd: str = DEFAULT_CHECK_CMD) -> dict[str, Any]:
    """After the implementer's last commit: run the hidden tests in its worktree, the check, and the departure report."""
    worktree = worktree.resolve()
    summary = _load(run_dir)
    base = base or summary.get("ref") or "HEAD"
    summary.update({"worktree": str(worktree), "branch": _git(worktree, "rev-parse", "--abbrev-ref", "HEAD"),
                    "head": _git(worktree, "rev-parse", "HEAD")})
    summary["uncommitted"] = len([ln for ln in _git(worktree, "status", "--porcelain", "--untracked-files=no").splitlines() if ln])
    hidden = _hidden_files(run_dir)
    collisions = [f"tests/{p.name}" for p in hidden if (worktree / "tests" / p.name).exists()]
    summary["collisions"] = collisions
    if collisions:
        summary["accept"] = None
    elif hidden:
        (worktree / "tests").mkdir(exist_ok=True)
        copies = [worktree / "tests" / p.name for p in hidden]
        try:
            for src, dst in zip(hidden, copies):
                shutil.copy(src, dst)
            summary["accept"] = _run_tests(worktree, test_cmd, [f"tests/{p.name}" for p in hidden], run_dir / "accept.log")
        finally:
            for dst in copies:
                dst.unlink(missing_ok=True)
    else:
        summary["accept"] = None
    if check_cmd == "none":
        summary["check_exit"] = None
    else:
        r = subprocess.run(check_cmd, shell=True, cwd=worktree, capture_output=True, text=True)
        (run_dir / "check.log").write_text(f"$ {check_cmd}\n{r.stdout}\n{r.stderr}")
        summary["check_exit"] = r.returncode
    summary["departures"] = departures(worktree, change, base)
    summary["peek_reads"] = _peek_reads(run_dir, summary.get("writer_worktree"))
    _save(run_dir, summary)
    _print_check(summary)
    return summary


def exit_code(summary: dict[str, Any]) -> int:
    """0 only when the hidden tests ran and passed, the check passed or was skipped, and nothing is uncommitted."""
    acc = summary.get("accept")
    bad = (summary.get("collisions") or not acc or acc.get("exit") != 0
           or summary.get("check_exit") not in (0, None) or summary.get("uncommitted"))
    return 1 if bad else 0


def _print_check(s: dict[str, Any]) -> None:
    d = s["departures"]
    print(f"accept check: run {s['run_id']} head {s['head'][:12]} hidden={s.get('accept')} check_exit={s['check_exit']} "
          f"uncommitted={s['uncommitted']} peek_reads={s['peek_reads']}")
    if s.get("collisions"):
        print(f"REFUSED: hidden test name(s) already in the worktree: {', '.join(s['collisions'])}")
    if s["uncommitted"]:
        print(f"WARNING: {s['uncommitted']} tracked file(s) changed but not committed")
    print(f"departures: {len(d['outside_tasks'])} file(s) outside tasks.md, {len(d['unticked'])} unticked task(s)")
    for p in d["outside_tasks"]:
        print(f"  outside tasks: {p}")
    for t in d["unticked"]:
        print(f"  unticked: {t}")
    print(f"record: {s['run_dir']}/summary.json")


def _impl_env() -> dict[str, str]:
    return {k: v for k, v in os.environ.items() if RUNS not in v}


def ship_command(repo: Path) -> str:
    """`uv run ship` when the repository's pyproject.toml depends on agentic-engineering-system (which installs
    `ship`), else `ship`.

    Implements: plan-run/one-driver-runs-a-plan-with-claude-or-codex

    Requirement text (generated):
        plan-run/one-driver-runs-a-plan-with-claude-or-codex: `lockstep run-plan <change> --agent
            claude|codex` SHALL run `accept write`, then one headless implementer session in a new
            worktree on branch `impl/<change>-<run id>`, then `accept check`, saving each session's
            JSON event stream as its transcript, and SHALL print the `ship` command to run next
            without running it: `uv run ship` when the repository's `pyproject.toml` depends on
            `agentic-engineering-system` (which installs `ship`), else `ship`. The agent choice
            SHALL change only the command that starts each session.
    """
    import tomllib

    try:
        data = tomllib.loads((repo / "pyproject.toml").read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return "ship"
    project = data.get("project", {})
    lists = [project.get("dependencies", []), *project.get("optional-dependencies", {}).values(),
             *data.get("dependency-groups", {}).values()]
    names = [re.split(r"[\s\[<>=!~;@]", item, maxsplit=1)[0].lower()
             for group in lists for item in group if isinstance(item, str)]
    return "uv run ship" if "agentic-engineering-system" in names else "ship"


def run_plan(repo: Path, change: str, ref: str = "HEAD", agent: str = "claude", runner: Runner = default_runner,
             test_cmd: str = DEFAULT_TEST_CMD, check_cmd: str = DEFAULT_CHECK_CMD,
             timeout: int = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """accept write, one implementer session in a new worktree, accept check; prints the ship command; never merges."""
    repo = repo.resolve()
    s = accept_write(repo, change, ref, agent, runner, test_cmd, timeout)
    run_dir = Path(s["run_dir"])
    branch = f"impl/{change}-{s['run_id']}"
    wt = repo.parent / f"{repo_name(repo)}_worktrees" / f"impl-{change}-{s['run_id']}"
    wt.parent.mkdir(parents=True, exist_ok=True)
    _git(repo, "worktree", "add", "-b", branch, str(wt), s["ref"])
    prompt = implementer_prompt(change, check_cmd)
    (run_dir / "implementer-prompt.md").write_text(prompt)
    s["implementer_exit"] = runner(agent, prompt, wt, run_dir / "implementer.jsonl", timeout, env=_impl_env(), persist=True)
    _save(run_dir, s)
    s = accept_check(wt, change, run_dir, s["ref"], test_cmd, check_cmd)
    print(f"next: review the record, then merge with `cd {wt} && {ship_command(repo)}` (run-plan does not merge)")
    return s


# ---- command line --------------------------------------------------------------------------------


def _latest_run(repo: Path, change: str) -> Path:
    root = runs_root(repo)
    runs = sorted(p for p in root.glob("*") if _load(p).get("change") == change) if root.exists() else []
    if not runs:
        raise FileNotFoundError(f"no run for change {change!r} under {root}; run `lockstep accept write {change}` first")
    return runs[-1]


def cli(argv: list[str]) -> int:
    """`lockstep accept write|check <change>` and `lockstep run-plan <change>`."""
    ap = argparse.ArgumentParser(prog="lockstep")
    sub = ap.add_subparsers(dest="cmd", required=True)
    w = sub.add_parser("write", help="a separate session writes hidden acceptance tests from the plan")
    c = sub.add_parser("check", help="after the last commit: run hidden tests, the check and the departure report")
    r = sub.add_parser("run-plan", help="write hidden tests, run one implementer session, check; never merges")
    for p in (w, c, r):
        p.add_argument("change")
        p.add_argument("--repo", type=Path, default=Path.cwd())
        p.add_argument("--test-cmd", default=DEFAULT_TEST_CMD)
    for p in (w, r):
        p.add_argument("--ref", default="HEAD")
        p.add_argument("--agent", choices=["claude", "codex"], default="claude")
        p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    for p in (c, r):
        p.add_argument("--check-cmd", default=DEFAULT_CHECK_CMD)
    c.add_argument("--base", default=None)
    c.add_argument("--run-dir", type=Path, default=None)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "write":
            s = accept_write(a.repo, a.change, a.ref, a.agent, default_runner, a.test_cmd, a.timeout)
            return 0 if s["accept_files"] else 1
        if a.cmd == "check":
            run_dir = a.run_dir or _latest_run(a.repo, a.change)
            return exit_code(accept_check(a.repo, a.change, run_dir, a.base, a.test_cmd, a.check_cmd))
        return exit_code(run_plan(a.repo, a.change, a.ref, a.agent, default_runner, a.test_cmd, a.check_cmd, a.timeout))
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"lockstep {a.cmd}: {exc}", file=sys.stderr)
        return 2

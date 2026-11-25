"""`lockstep check mutation`: run mutation testing (mutmut) and list the code changes the tests let pass.

Brian, 2026-11-24 ("i approve adding the redit ideas to the plan"): a test suite can pass while checking little;
mutmut changes the code one small edit at a time (a `+=` to `=`, a `continue` to `break`) and reruns the tests that
cover it. A change no test notices "survived": either a test is missing or the change makes no difference. The
surviving list is a report for an agent to read, not a failure. First AES's nightly script in code2-workspace; a
Lockstep check each repository switches on in its `lockstep.yaml` since Brian, 2026-11-25 ("ia prpove yourr
ecommednations").

It runs `mutmut run` in the repository (what to mutate and which tests to run is the repository's `[tool.mutmut]`
in pyproject.toml; without one mutmut guesses), within a time limit, then reads `mutmut results --all true` and
prints one line per module with survivors and a final `mutation:` summary line. `mutants/` must be ignored by git;
it stays between runs and mutmut reruns only the mutants whose code or tests changed. mutmut is found in the
repository's `.venv/bin`, else on PATH: it must run in the environment that can import the code and its tests.

mutmut saves each mutant's result as it finishes, so a run stopped at the time limit (its whole process group is
stopped) keeps what it checked and the next run continues; the summary then counts `not checked` mutants. A results
file cut off mid-write by that stop is renamed `.meta.broken` before the next run, so mutmut rechecks it.
Exit 0 whenever mutmut finished, or was stopped at the limit, survivors or not; exit 2 when it could not run, failed
(its first step runs the selected tests once, and a test that needs a git checkout fails in mutmut's copy: the line
names the test so an agent can add a `--deselect`), or was stopped at the limit two runs running without fewer
mutants left unchecked. In `warn` mode Lockstep turns that 2 into 0 with a warning, so a nightly run uses `block`.
`--issue` keeps one open `owner:agent` issue in `mutation.issue_repo` (default: the origin repository) with the
survived count per module and up to SHOWN diffs; the shown survivors are rerun by name first, because mutmut keeps a
result until its function changes and so would not notice a test added for it. The last survivors and progress are
kept per repository under `<git-common-dir>/lockstep-mutation/`.

Implements: lockstep-checks/mutation-lists-surviving-mutants-per-repository,
    lockstep-checks/mutation-survivors-are-a-report-and-a-broken-run-is-a-failure,
    lockstep-checks/mutation-one-agent-issue-carries-the-survivors

Requirement text (generated):
    lockstep-checks/mutation-lists-surviving-mutants-per-repository: `lockstep check mutation
        [--timeout S]` SHALL run `mutmut run` in the repository (mutmut from its `.venv/bin`, else
        PATH; what to mutate from its `[tool.mutmut]`), read `mutmut results --all true`, print one
        `<module>: <n> survived` line per module and end with `mutation: <n> survived, <n> killed[,
        <n> <status>] of <n> mutants in <s>s (<name>)`, where `<name>` is `mutation.name` in
        `lockstep.yaml`, else the origin repository's name.
    lockstep-checks/mutation-survivors-are-a-report-and-a-broken-run-is-a-failure: The mutation
        check SHALL exit 0 when mutmut finished or was stopped at the time limit, survivors or not,
        and 2 when mutmut is missing, fails (naming any test that failed in mutmut's copy), gives no
        results, or was stopped at the limit twice running without fewer mutants left unchecked. A
        run stopped at the limit SHALL stop mutmut's whole process group, and a results file cut off
        by the stop SHALL be set aside so mutmut checks those mutants again. In `warn` mode the 2
        becomes 0 with a warning, so a nightly run SHALL use `block`.
    lockstep-checks/mutation-one-agent-issue-carries-the-survivors: With `--issue`, the mutation
        check SHALL first rerun the shown survivors by name, then keep one open `owner:agent` issue
        titled `Mutation testing: code changes <name>'s tests let pass` in `mutation.issue_repo`
        (default: the origin repository): open it when none is open and something survived, comment
        when the survived counts per module changed, and leave it otherwise, with up to 30 diffs
        under GitHub's body limit.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:checks:mutation.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-checks/mutation-lists-surviving-mutants-per-repository, lockstep-checks/mutation-survivors-are-a-report-and-a-broken-run-is-a-failure, lockstep-checks/mutation-one-agent-issue-carries-the-survivors, lockstep-checks/mutation-off-unless-switched-on-and-set-per-repository

### Requirement: Mutation: Lists surviving mutants per repository

`lockstep check mutation [--timeout S]` SHALL run `mutmut run` in the repository (mutmut from its `.venv/bin`, else
PATH; what to mutate from its `[tool.mutmut]`), read `mutmut results --all true`, print one `<module>: <n> survived`
line per module and end with `mutation: <n> survived, <n> killed[, <n> <status>] of <n> mutants in <s>s (<name>)`,
where `<name>` is `mutation.name` in `lockstep.yaml`, else the origin repository's name.

Source: Brian, 2026-11-24: "i approve adding the redit ideas to the plan" (code2-workspace mutation-nightly) and Brian, 2026-11-25: "ia prpove yourr ecommednations" (moved into Lockstep)

#### Scenario: Mutation: Lists surviving mutants per repository

- **GIVEN** mutmut results with survivors in two modules
- **WHEN** the check runs
- **THEN** it prints each module's survived count, most first, and the summary line

### Requirement: Mutation: Survivors are a report and a broken run is a failure

The mutation check SHALL exit 0 when mutmut finished or was stopped at the time limit, survivors or not, and 2 when
mutmut is missing, fails (naming any test that failed in mutmut's copy), gives no results, or was stopped at the limit
twice running without fewer mutants left unchecked. A run stopped at the limit SHALL stop mutmut's whole process group,
and a results file cut off by the stop SHALL be set aside so mutmut checks those mutants again. In `warn` mode the 2
becomes 0 with a warning, so a nightly run SHALL use `block`.

Source: Brian, 2026-11-24 (code2-workspace mutation-nightly) and Brian, 2026-11-25: "ia prpove yourr ecommednations"

#### Scenario: Mutation: Survivors are a report and a broken run is a failure

- **GIVEN** a run with survivors, a run where a test fails in mutmut's copy, and two stopped runs with no progress
- **WHEN** the check runs
- **THEN** the first exits 0, the second exits 2 naming the test, the second stopped run exits 2

### Requirement: Mutation: One agent issue carries the survivors

With `--issue`, the mutation check SHALL first rerun the shown survivors by name, then keep one open `owner:agent`
issue titled `Mutation testing: code changes <name>'s tests let pass` in `mutation.issue_repo` (default: the origin
repository): open it when none is open and something survived, comment when the survived counts per module changed,
and leave it otherwise, with up to 30 diffs under GitHub's body limit.

Source: Brian, 2026-11-24 (code2-workspace mutation-nightly) and Brian, 2026-11-25: "ia prpove yourr ecommednations"

#### Scenario: Mutation: One agent issue carries the survivors

- **GIVEN** survivors on three runs, the third with one more
- **WHEN** the check runs with `--issue` each time
- **THEN** the first opens the issue, the second leaves it, the third comments on it

### Requirement: Mutation: Off unless switched on and set per repository

`mutation` SHALL be `off` when absent from `lockstep.yaml`. Its last survivors and progress SHALL be kept per
repository under `<git-common-dir>/lockstep-mutation/`, and `mutation.issue_repo` and `mutation.name` SHALL set where
the issue goes and the name in its title and summary.

Source: Brian, 2026-11-25: "ia prpove yourr ecommednations" (directive: issue repository from `lockstep.yaml`, default origin; AES sets code2-workspace)

#### Scenario: Mutation: Off unless switched on and set per repository

- **GIVEN** no `mutation` in `lockstep.yaml`, then `checks: {mutation: block}` with `mutation: {issue_repo: Acme/tracker, name: Widget}`
- **WHEN** `lockstep check mutation --issue` runs each time
- **THEN** the first is skipped and runs nothing; the second opens `Mutation testing: code changes Widget's tests let
  pass` in `Acme/tracker` and keeps its state in the repository's git folder

Tested by: tests/lockstep/checks/test_lockstep_check_mutation.py

Declares (typed signatures, from the plan):
  title(name: str) -> str
  state_dir(tree: Path) -> Path
  find_mutmut(tree: Path) -> Path | None
  keep_agent_issue(repo: str, title_: str, body: str, key: list[str], state: Path, anything: bool) -> str
  module_of(key: str) -> str
  parse_results(text: str) -> dict[str, str]
  summary_line(status: dict[str, str], secs: int, name: str='') -> str
  issue_body(by_module: dict[str, list[str]], diffs: dict[str, str], line: str, name: str='', tree: Path | str='.') -> str
  run_mutmut(cmd: list[str], cwd: Path, env: dict, timeout: int) -> tuple[int | None, str, int]
  set_aside_broken(tree: Path) -> list[str]
  read_status(mutmut: Path, tree: Path, env: dict) -> tuple[int, dict[str, str]]
  stalled(progress: Path, stopped: bool, unchecked: int) -> int | None
  recheck(mutmut: Path, keys: list[str], tree: Path, env: dict) -> tuple[dict[str, str], str]
  show_diffs(mutmut: Path, keys: list[str], tree: Path, env: dict) -> dict[str, str]
  run(tree: Path, timeout: int=TIMEOUT, issue: bool=False, issue_repo: str | None=None, name: str | None=None) -> int
  main(argv: list[str] | None=None) -> int
[[[end]]]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path

TIMEOUT = 3600
SHOWN = 30
RECHECK_LIMIT = 900
BODY_LIMIT = 60_000
RESULT = re.compile(r"^\s+(\S+): (.+)$")
FAILING = re.compile(r"^(?:FAILED|ERROR) (\S+)", re.M)
OWNER_NAME = re.compile(r"[:/]([^/:\s]+)/([^/\s]+?)(?:\.git)?/?$")


def title(name: str) -> str:
    """The issue title; for AES (`mutation.name: AES`) the title its nightly issue has had since 2026-11-24."""
    return f"Mutation testing: code changes {name}'s tests let pass"


def _origin(tree: Path) -> tuple[str, str] | None:
    """(owner, name) of the tree's origin remote, or None."""
    done = subprocess.run(["git", "-C", str(tree), "remote", "get-url", "origin"], capture_output=True, text=True)
    match = OWNER_NAME.search(done.stdout.strip()) if done.returncode == 0 else None
    return (match.group(1), match.group(2)) if match else None


def state_dir(tree: Path) -> Path:
    """Where this repository's last survivors and progress are kept: `<git-common-dir>/lockstep-mutation`."""
    done = subprocess.run(["git", "-C", str(tree), "rev-parse", "--path-format=absolute", "--git-common-dir"],
                          capture_output=True, text=True)
    if done.returncode:
        return tree / ".lockstep-mutation"
    return Path(done.stdout.strip()) / "lockstep-mutation"


def find_mutmut(tree: Path) -> Path | None:
    """mutmut in the tree's `.venv/bin`, else on PATH."""
    local = tree / ".venv" / "bin" / "mutmut"
    if local.exists():
        return local
    found = shutil.which("mutmut")
    return Path(found) if found else None


def keep_agent_issue(repo: str, title_: str, body: str, key: list[str], state: Path, anything: bool) -> str:
    """Keep one open owner:agent issue in `repo` titled `title_`: open it when none is open and `anything` is listed,
    comment when `key` differs from the last one kept in `state`. Returns what was done.

    Ported from code2-workspace `scripts/prompt_cost.py`; a failed create or comment leaves `state` alone, so it is
    retried the next run.
    """
    try:
        last = json.loads(state.read_text())
    except (OSError, ValueError):  # no state yet, or a truncated file: treat as never run
        last = None
    try:
        found = subprocess.run(["gh", "issue", "list", "-R", repo, "--state", "open", "--search",
                                f'"{title_}" in:title', "--json", "number"], capture_output=True, text=True, timeout=60)
        if found.returncode:
            return "issue not checked (gh failed)"
        open_now = json.loads(found.stdout or "[]")
        ok = True
        if not anything:
            done = "nothing flagged"
        elif not open_now:
            made = subprocess.run(["gh", "issue", "create", "-R", repo, "--title", title_, "--body", body,
                                   "--label", "owner:agent"], capture_output=True, text=True, timeout=60)
            ok = made.returncode == 0
            done = f"opened {made.stdout.strip()}" if ok else "issue not opened (gh failed)"
        elif key != last:
            num = str(open_now[0]["number"])
            made = subprocess.run(["gh", "issue", "comment", num, "-R", repo, "--body",
                                   "The list changed.\n\n" + body], capture_output=True, text=True, timeout=60)
            ok = made.returncode == 0
            done = f"commented on #{num}" if ok else "issue comment failed"
        else:
            done = f"list unchanged, #{open_now[0]['number']} left as is"
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        return f"issue not kept ({type(exc).__name__})"
    if ok:
        state.parent.mkdir(parents=True, exist_ok=True)
        state.write_text(json.dumps(key))
    return done


def module_of(key: str) -> str:
    """`lockstep.checks.suppressions.x_check__mutmut_12` -> `lockstep.checks.suppressions` (methods use `xǁ`)."""
    return re.split(r"\.x[_ǁ]", key, maxsplit=1)[0]


def parse_results(text: str) -> dict[str, str]:
    """mutant key -> status, from `mutmut results --all true`."""
    return {m.group(1): m.group(2).strip() for m in map(RESULT.match, text.splitlines()) if m}


def summary_line(status: dict[str, str], secs: int, name: str = "") -> str:
    """The `mutation:` line: counts by status over all mutants."""
    counts = Counter(status.values())
    rest = ", ".join(f"{n} {s}" for s, n in sorted(counts.items()) if s not in ("survived", "killed"))
    return (f"mutation: {counts['survived']} survived, {counts['killed']} killed"
            + (f", {rest}" if rest else "") + f" of {len(status)} mutants in {secs}s ({name})")


def issue_body(by_module: dict[str, list[str]], diffs: dict[str, str], line: str, name: str = "",
               tree: Path | str = ".") -> str:
    """Survivor counts per module, then as many of the diffs as fit under GitHub's 65,536-character body limit."""
    parts = [f"`lockstep check mutation` ran mutmut on {name}: {line.removeprefix('mutation: ')}.",
             "A survived mutant is a one-line change to the code that every test covering it still passed. For each:"
             " add or tighten a test that fails on the change, or, when the change makes no difference (for example"
             " `False` to `None` in a flag only read as true or false), leave it. mutmut keeps a mutant's result until"
             " its function changes, so confirm a new test with `mutmut run <key>` in"
             f" `{tree}`; the diffs below are rechecked by name each night. `mutmut show <key>` prints any diff.",
             "", "Survived, by module:"]
    parts += [f"- `{m}`: {len(keys)}" for m, keys in sorted(by_module.items(), key=lambda kv: -len(kv[1]))]
    blocks = []
    size = len("\n".join(parts)) + 200
    for d in diffs.values():
        block = f"\n```diff\n{d.strip()}\n```"
        if size + len(block) > BODY_LIMIT:
            break
        blocks.append(block)
        size += len(block) + 1
    if blocks:
        parts += ["", f"{len(blocks)} diffs (rechecked tonight):"] + blocks
    return "\n".join(parts)


def run_mutmut(cmd: list[str], cwd: Path, env: dict, timeout: int) -> tuple[int | None, str, int]:
    """Run mutmut in its own process group; (exit code or None when stopped at `timeout`, output, seconds)."""
    start = time.monotonic()
    proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                            start_new_session=True)
    out = ""
    try:
        out, _ = proc.communicate(timeout=timeout)
        rc: int | None = proc.returncode
    except subprocess.TimeoutExpired:
        rc = None
        for sig in (signal.SIGTERM, signal.SIGKILL):  # mutmut's workers are in the same group
            try:
                os.killpg(proc.pid, sig)
            except ProcessLookupError:  # the group exited as the limit passed
                pass
            try:
                out, _ = proc.communicate(timeout=30)
                break
            except subprocess.TimeoutExpired:  # a process outside the group may hold the pipe: stop waiting
                continue
    return rc, out or "", round(time.monotonic() - start)


def set_aside_broken(tree: Path) -> list[str]:
    """Rename every unreadable mutmut results file (`mutants/**/*.meta`, cut off mid-write when a run is stopped), with
    the mutated copy of its source file and its `.spans` file, to `.broken`. Without the mutated copy mutmut makes the
    file's mutants again and rechecks them; with only the results file gone it would silently skip them. Returns the
    results files set aside."""
    broken = []
    for meta in sorted((tree / "mutants").rglob("*.meta")):
        try:
            json.loads(meta.read_text())
        except (OSError, ValueError):
            copy = meta.with_suffix("")  # mutants/src/x.py.meta -> mutants/src/x.py
            for part in (meta, copy, copy.with_name(copy.name + ".spans")):
                if part.exists():
                    part.rename(part.with_name(part.name + ".broken"))
            broken.append(str(meta.relative_to(tree)))
    return broken


def read_status(mutmut: Path, tree: Path, env: dict) -> tuple[int, dict[str, str]]:
    """(exit code, mutant key -> status) from `mutmut results --all true`."""
    try:
        res = subprocess.run([str(mutmut), "results", "--all", "true"], cwd=tree, env=env, capture_output=True,
                             text=True, timeout=600)
    except subprocess.TimeoutExpired:
        return -1, {}
    return res.returncode, parse_results(res.stdout)


def stalled(progress: Path, stopped: bool, unchecked: int) -> int | None:
    """Record this run's progress in `progress`; return the last run's unchecked count when both runs were stopped at
    the limit and this one left no fewer mutants unchecked, else None."""
    try:
        last = json.loads(progress.read_text())
    except (OSError, ValueError):  # first run, or a truncated file
        last = None
    progress.parent.mkdir(parents=True, exist_ok=True)
    progress.write_text(json.dumps({"stopped": stopped, "unchecked": unchecked}))
    if (stopped and isinstance(last, dict) and last.get("stopped")
            and isinstance(last.get("unchecked"), int) and unchecked >= last["unchecked"]):
        return last["unchecked"]
    return None


def recheck(mutmut: Path, keys: list[str], tree: Path, env: dict) -> tuple[dict[str, str], str]:
    """Rerun `keys` by name; (every mutant's status, "") when that worked, else ({}, a note saying it failed)."""
    again, _, _ = run_mutmut([str(mutmut), "run", "--max-children", "10", *keys], tree, env, RECHECK_LIMIT)
    code, status = read_status(mutmut, tree, env)
    if again == 0 and code == 0 and status:
        return status, ""
    return {}, f"recheck of the shown survivors failed (exit {again})"


def show_diffs(mutmut: Path, keys: list[str], tree: Path, env: dict) -> dict[str, str]:
    """Mutant key -> `mutmut show` diff, for each of `keys` that mutmut can show within a minute."""
    diffs = {}
    for key in keys:
        try:
            got = subprocess.run([str(mutmut), "show", key], cwd=tree, env=env, capture_output=True, text=True,
                                 timeout=60)
        except subprocess.TimeoutExpired:
            continue
        if got.returncode == 0:
            diffs[key] = got.stdout
    return diffs


def run(tree: Path, timeout: int = TIMEOUT, issue: bool = False, issue_repo: str | None = None,
        name: str | None = None) -> int:
    """Run mutmut in `tree`, print survivors by module and the summary line; keep the issue when `issue`."""
    tree = tree.resolve()
    origin = _origin(tree)
    name = name or (origin[1] if origin else tree.name)
    mutmut = find_mutmut(tree)
    if mutmut is None:
        print(f"mutation: could not run: no mutmut in {tree / '.venv' / 'bin'} or on PATH (install mutmut==3.8.1 in"
              " the environment that runs the tests)")
        return 2
    repo = issue_repo or (f"{origin[0]}/{origin[1]}" if origin else None)
    if issue and repo is None:
        print("mutation: could not run: --issue needs mutation.issue_repo in lockstep.yaml or an origin remote")
        return 2
    state, progress = state_dir(tree) / "last-survivors.json", state_dir(tree) / "last-not-checked.json"
    env = {**os.environ, "PATH": f"{mutmut.parent}{os.pathsep}{os.environ.get('PATH', '')}"}
    notes = [f"set aside unreadable {b}" for b in set_aside_broken(tree)]
    rc, out, secs = run_mutmut([str(mutmut), "run", "--max-children", "10"], tree, env, timeout)
    if rc:
        failing = sorted(set(FAILING.findall(out)))
        print(out[-3000:])
        print(f"mutation: could not run: mutmut exit {rc}"
              + (f"; failing test(s) in mutmut's copy: {', '.join(failing[:5])} (a test that needs a git checkout"
                 " gets a --deselect in [tool.mutmut] pytest_add_cli_args)" if failing else ""))
        return 2
    code, status = read_status(mutmut, tree, env)
    if code or not status:
        print(f"mutation: could not run: `mutmut results` exit {code}, {len(status)} mutants read")
        return 2
    unchecked = sum(s == "not checked" for s in status.values())
    before = stalled(progress, rc is None, unchecked)
    if before is not None:
        print(f"mutation: could not run: stopped at the {timeout}s limit twice running with {unchecked} mutants not"
              f" checked, no fewer than the {before} the run before (narrow [tool.mutmut] in pyproject.toml)")
        return 2
    survivors = sorted(k for k, s in status.items() if s == "survived")
    shown = survivors[:SHOWN]
    if issue and shown:  # recheck the shown ones by name: a kept result ignores a test added since
        rechecked, failed = recheck(mutmut, shown, tree, env)
        if rechecked:
            status = rechecked
            survivors = sorted(k for k, s in status.items() if s == "survived")
            shown = [k for k in shown if status.get(k) == "survived"]
        else:
            notes.append(failed)
    by_module: dict[str, list[str]] = defaultdict(list)
    for key in survivors:
        by_module[module_of(key)].append(key)
    for mod, keys in sorted(by_module.items(), key=lambda kv: -len(kv[1])):
        print(f"{mod}: {len(keys)} survived")
    line = summary_line(status, secs, name) + (f"; stopped at the {timeout}s limit, the next run continues" if rc is None else "")
    if issue and repo is not None:  # checked above: --issue without a repository already exited 2
        diffs = show_diffs(mutmut, shown, tree, env)
        # survived counts per module, not mutant keys: a key is numbered within its function and renames on any edit
        # the issue repository is part of the key, so moving `mutation.issue_repo` posts to the new one at once
        issue_key = [f"repo={repo}"] + sorted(f"{m}={len(k)}" for m, k in by_module.items())
        notes.append(keep_agent_issue(repo, title(name), issue_body(by_module, diffs, line, name, tree), issue_key, state,
                                      bool(survivors)))
    print(line + "".join(f"; {n}" for n in notes))
    return 0


def main(argv: list[str] | None = None) -> int:
    """The check with no `lockstep.yaml` mode applied: `python -m lockstep.checks.mutation`."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", type=Path, default=Path("."))
    ap.add_argument("--timeout", type=int, default=TIMEOUT)
    ap.add_argument("--issue", action="store_true")
    ap.add_argument("--issue-repo", default=None)
    ap.add_argument("--name", default=None)
    a = ap.parse_args(argv)
    return run(a.repo, a.timeout, a.issue, a.issue_repo, a.name)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Run a repository's check and merge its pull request only if the check passed.

Steps, each printing its exit status and time, stopping at the first that fails:
clean tree on a non-default branch; the one-page plans and the prior-art record of each OpenSpec change the
merge touches (code2-workspace scripts/prior_art_check.py, from $SHIP_WORKSPACE); the planning gate; the check (default `make check`), skipped when
this tree already passed the same check; the tree still clean and HEAD unchanged; push; open the pull request when the branch has none; merge pinned to the checked commit
(`gh pr merge --match-head-commit`); read the state back and require MERGED.
The merge method is chosen before the check, from what the repository allows: --method when allowed, else the
repository's default method when allowed, else the first allowed of rebase, squash, merge. Allowed means the
repository's settings enable it and, for `merge`, the default branch does not require linear history (branch
protection or a ruleset). A replaced --method is printed; a repository that allows none stops the run before the check.
Every run is appended to one log per day under $SHIP_LOG_DIR (default ~/code2/.ship-logs).
Usage: ship [--repo DIR] [--check CMD] [--method merge|rebase|squash] [--recheck] [--keep-lane]

After the merge, the repository's finished lanes are swept, this lane included; --keep-lane (or
SHIP_KEEP_LANE=1) keeps this lane for a caller that still works in it.

Before the check, a fresh worktree gets its environment: `uv sync --all-extras` when the top has
uv.lock or pyproject.toml and no .venv, `npm ci` when it has package-lock.json and no node_modules.
The uv sync runs only when the check is the repository's own Makefile check (a `make ...` command, the default
`make check` included); a `--check` that names some other command is trusted to bring what it needs, so a
hook-only change ships even where `uv sync` cannot run. A sync or `npm ci` that fails removes the .venv or
node_modules it just created, so a failed run leaves no empty one for the next run to mistake for an environment.
A passed check is appended to $SHIP_STATE_DIR/passed.jsonl (default ~/.local/state/ship) by tree hash
and check command; the same tree and command later skips the check unless --recheck is given.

One-page plans (agents/topics/working-method.md, "Plan size"): every .md under docs/plans/ that the merge adds or
changes and that carries the line `Plan size: small` must have its five headed parts, at most 150 lines and a line
`Independent read: <YYYY-MM-DD>, pass ...` (the last such line counts); an incomplete one stops the run before the
planning gate, with no exception. Text inside a code block is a quotation and is not read as the page's own.

The planning gate: a NEW repository (first commit on or after 2026-11-05) with no docs/planning/planning-package.json and
no complete one-page plan is refused; with a complete, committed one-page plan it proceeds, and the plan list is not read; an older
one merges with a warning. With a package, Company Planning's validate_planning_package.py (read from origin/main of
$SHIP_COMPANY_PLANNING, default ~/code2/company-planning) must exit 0 on it, or fail only for freshness (plan content
changed since its cold review; it then passes with --no-freshness, and ship warns and proceeds). A repository whose first
commit is on or after 2026-11-05 is new: its package must also be on the plan list (the file
`plan_list_path:` names, on origin/main of the checkout `plan_list_checkout:` names, both in graph-config.yaml
beside the project graph; $SHIP_PLAN_LIST and $SHIP_PERSONAL_VPS override them; none named refuses),
so its review page deploys. The gate runs only when ship merges in that repository.
The validator runs under a fixed interpreter that has its packages (jsonschema, pydantic), never under ship's
own python: ship called from a project venv (dodaf's `uv run scripts/release.py`) would run it with that venv's
python, which lacks them. The first of /usr/bin/python3 and `uv run --no-project --with ...` that imports both is
used; $SHIP_VALIDATOR_PYTHON (a command line) names one instead. When none can import them, or the validator dies
on an import error, ship stops with "could not run", which is not a verdict on the package.
When origin/main has Company Planning's goal provenance check (scripts/goal_provenance.py and its prompt),
ship extracts it beside the validator at its own path, so the validator runs it, and prints
`ship: goal provenance: <mark> (required from <date>)` from the validator's line: the date an existing
repository's unsourced goals start refusing the merge.

A check takes one of $SHIP_CHECK_SLOTS (default 3) machine-wide slots (flock files under $SHIP_STATE_DIR/check-slots),
so a dozen agents merging at once do not run a dozen suites on the 20 cores; a run that finds all slots taken says
who holds them and waits up to $SHIP_SLOT_WAIT seconds (default 1800), then stops with nothing pushed. 0 slots
turns the limit off.

Implements: ship/merge-only-the-commit-whose-check-passed
Implements: ship/refuse-a-new-repository-with-no-planning-package
Implements: ship/check-every-one-page-plan-a-merge-adds-or-changes
Implements: ship/a-plan-repair-is-never-refused
Implements: ship/an-upkeep-only-change-is-never-refused
Implements: ship/refuse-a-merge-whose-openspec-change-lacks-a-prior-art-record
Implements: ship/a-record-only-change-is-never-refused
Implements: ship/refuse-a-planning-package-the-validator-rejects
Implements: ship/hold-a-new-repository-to-a-deployed-plan
Implements: ship/prepare-a-fresh-worktree-s-environment-before-the-check
Implements: ship/skip-a-check-that-already-passed-on-the-same-tree
Implements: ship/keep-its-own-lane-when-the-caller-still-needs-it
Implements: ship/refuse-goals-that-do-not-name-their-sources
Implements: ship/merge-with-a-method-the-repository-allows
Implements: ship/limit-how-many-checks-run-at-once
Implements: ship/settings-come-from-config
"""
import argparse
import contextlib
import datetime
import fcntl
import json
import os
import re
import shutil
import shlex
import subprocess
import sys
import tempfile
import time
from pathlib import Path

METHODS = {"MERGE": "merge", "REBASE": "rebase", "SQUASH": "squash"}
# The repository settings that enable each method, and the order tried when the wanted one is not allowed.
ENABLED_BY = {"merge": "mergeCommitAllowed", "rebase": "rebaseMergeAllowed", "squash": "squashMergeAllowed"}
FALLBACK_ORDER = ("rebase", "squash", "merge")
SETTINGS_FIELDS = "defaultBranchRef,viewerDefaultMergeMethod," + ",".join(ENABLED_BY.values())
PACKAGE = "docs/planning/planning-package.json"
VALIDATOR = "plugins/company-planning/skills/planning-compliance/scripts/validate_planning_package.py"
GOAL_PROVENANCE = ("plugins/company-planning/scripts/goal_provenance.py",
                   "plugins/company-planning/scripts/goal_provenance_prompt.yaml")
# Interpreters that may run the validator, best first; each is tried with VALIDATOR_IMPORTS (the validator's
# third-party imports: jsonschema in initiative_home.py, pydantic in coverage_check.py).
VALIDATOR_PYTHONS = (["/usr/bin/python3"],
                     ["uv", "run", "--no-project", "--with", "jsonschema", "--with", "pydantic", "python"])
VALIDATOR_IMPORTS = "import jsonschema, pydantic"
IMPORT_ERRORS = ("ModuleNotFoundError:", "ImportError:")   # the exception class that ends a Python traceback
GOAL_LINE = re.compile(r"^(ok|WAIT|FAIL)\s+goal provenance:.*?\(required from (\d{4}-\d{2}-\d{2})\)", re.M)
NEW_FROM = "2026-11-05"   # a first commit on or after this date is a new repository (Brian, 2026-11-04)
# Where the plan list (the repositories whose review pages deploy) lives is a person's setting, not code.
CONFIG = Path(os.environ.get("PROJECT_GRAPH") or Path.home() / "code2/aes-config/PROJECT_GRAPH.json").parent / "graph-config.yaml"
PRIOR_ART_RULE = "prior-art rule (code2-workspace agents/topics/working-method.md, \"The per-feature prior-art record\")"
PLANNING_RULE = "planning rule (agents/topics/working-method.md, \"Starting work on a project\")"
NEW_RULE = "new-repository rule (agents/topics/working-method.md, \"Starting work on a project\")"
# The one-page plan for small planned work (Brian, 2026-11-15, "6 all": decision record 0010). The marker line, the
# heading names and the wording of the read line were inferred by agent.
SIZE_RULE = "plan size rule (agents/topics/working-method.md, \"Plan size\")"
PLANS_DIR = "docs/plans/"
SMALL_PLAN = re.compile(r"^Plan size:[ \t]*small[ \t]*$", re.M)
SMALL_PLAN_PARTS = ("Goal", "How Brian judges it", "Cost and time", "Scoring fixed beforehand", "What already exists")
SMALL_PLAN_LINES = 150
SMALL_PLAN_READ = re.compile(r"^Independent read:.*$", re.M)
SMALL_PLAN_PASS = re.compile(r"Independent read:[ \t]*(\d{4}-\d{2}-\d{2}),[ \t]*pass\b")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
SMALL_PLAN_READ_FORM = "Independent read: <YYYY-MM-DD>, pass (<who read it, and what was fixed>)"
CHECK_SLOTS = 3        # checks that may run at once on this machine (Brian, 2026-11-09: "i approve decision 2 and anything else that makes this more efficent")
SLOT_WAIT = 1800.0     # seconds a run waits for a slot before it stops
SLOT_POLL = 2.0        # seconds between looks at the slots
ORIGIN_NAME = re.compile(r"([^/:]+)[/:]([^/:]+?)(?:\.git)?/?$")


class Run:
    """One ship run: prints each step and appends it, with the check's full output, to the day's log."""

    def __init__(self, repo: Path):
        """Open the day's log and record the start of the run."""
        self.repo = repo
        log_dir = Path(os.environ.get("SHIP_LOG_DIR", Path.home() / "code2" / ".ship-logs"))
        log_dir.mkdir(parents=True, exist_ok=True)
        self.log = log_dir / f"{datetime.date.today().isoformat()}.log"
        self.write(f"\n=== ship {repo} at {datetime.datetime.now().isoformat(timespec='seconds')}")

    def write(self, text: str) -> None:
        """Append text to the day's log."""
        with self.log.open("a", encoding="utf-8") as fh:
            fh.write(text.rstrip("\n") + "\n")

    def step(self, name: str, cmd: list[str] | str, *, shell: bool = False) -> subprocess.CompletedProcess:
        """Run one step in the repository, print and log its exit status and time."""
        started = time.monotonic()
        result = subprocess.run(cmd, cwd=self.repo, shell=shell, capture_output=True, text=True,
                                env={**os.environ, "NO_COLOR": "1"})
        line = f"ship: {name}: exit status {result.returncode} ({time.monotonic() - started:.1f} s)"
        print(line)
        self.write(line)
        self.write(result.stdout + result.stderr)
        return result

    def fail(self, message: str) -> int:
        """Report why the run stopped; exit status 1."""
        line = f"ship: stopped: {message}; exit status 1 (log {self.log})"
        print(line)
        self.write(line)
        return 1


def git(repo: Path, *args: str) -> str:
    """Return git's stripped output, raising on failure."""
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout.strip()


def first_commit_day(repo: Path) -> str | None:
    """Return the date of the repository's earliest first commit as YYYY-MM-DD, or None when it cannot be read."""
    done = subprocess.run(["git", "-C", str(repo), "log", "--max-parents=0", "--format=%cI"],
                          capture_output=True, text=True)
    stamps = done.stdout.split()
    if done.returncode != 0 or not stamps:
        return None
    return min(datetime.datetime.fromisoformat(stamp) for stamp in stamps).date().isoformat()


def setting(key: str, env: str) -> str | None:
    """One value from the environment, else top-level `key:` in graph-config.yaml, else None. Read when needed."""
    named = os.environ.get(env)
    if named:
        return named
    try:
        found = re.search(rf"^{re.escape(key)}:[ \t]*([^\s#]+)", CONFIG.read_text(encoding="utf-8"), re.M)
    except OSError:
        found = None
    return found.group(1) if found else None


def plan_list_refusal(run: Run, repo: Path) -> str | None:
    """Return why a new repository's review page would not deploy, or None when it is on the plan list."""
    checkout, plan_list = setting("plan_list_checkout", "SHIP_PERSONAL_VPS"), setting("plan_list_path", "SHIP_PLAN_LIST")
    if not checkout or not plan_list:
        return (f"{NEW_RULE}: no plan list is named: set `plan_list_checkout:` and `plan_list_path:` in {CONFIG} "
                "(or SHIP_PERSONAL_VPS and SHIP_PLAN_LIST), so ship cannot tell whether this repository's review page deploys")
    url = subprocess.run(["git", "-C", str(repo), "remote", "get-url", "origin"], capture_output=True, text=True)
    match = ORIGIN_NAME.search(url.stdout.strip())
    if url.returncode != 0 or not match:
        return f"{NEW_RULE}: could not read this repository's name from its origin ({url.stdout.strip() or 'none'})"
    owner, name = match.groups()
    source = Path(checkout).expanduser()
    # A failed fetch leaves the last fetched list; a line merged on GitHub counts only after a fetch.
    run.step("fetch the plan-list checkout", ["git", "-C", str(source), "fetch", "-q", "origin"])
    shown = run.step("read the plan list", ["git", "-C", str(source), "show", f"origin/main:{plan_list}"])
    if shown.returncode != 0:
        return (f"{NEW_RULE}: could not read {plan_list} from {source} origin/main (git exit {shown.returncode}: "
                f"{shown.stderr.strip()}), so ship cannot tell whether this repository's review page deploys")
    urls = [line.split()[2] for line in shown.stdout.splitlines()
            if not line.lstrip().startswith("#") and len(line.split()) >= 3]
    listed = {found.group(2) for found in map(ORIGIN_NAME.search, urls) if found}
    if name not in listed:
        return (f"{NEW_RULE}: {name} is not on the plan list, so its review page would not deploy. Add this line to "
                f"{plan_list} in {source} (a private repository also needs a deploy key on the host that serves the "
                f"pages, see that repository's README, \"Plan pages\"): {name:<23} private     github-plans-{name}:{owner}/{name}.git")
    line = f"ship: new repository: {name} is on the plan list"
    print(line)
    run.write(line)
    return None


def validator_python(run: Run) -> list[str] | None:
    """Return the command that runs the planning validator, or None when no interpreter has its packages.

    Never sys.executable: ship is often called from a project's venv, which lacks the validator's packages
    (issue 197). $SHIP_VALIDATOR_PYTHON is taken as given; otherwise the first VALIDATOR_PYTHONS candidate whose
    probe exits 0 wins. The probe runs outside the repository so nothing in it can shadow an import.
    """
    named = os.environ.get("SHIP_VALIDATOR_PYTHON")
    if named:
        return shlex.split(named)
    for candidate in VALIDATOR_PYTHONS:
        try:
            probe = subprocess.run([*candidate, "-c", VALIDATOR_IMPORTS], cwd=run.log.parent,
                                   capture_output=True, text=True, timeout=120)
            status = f"exit status {probe.returncode}"
            usable = probe.returncode == 0
            detail = (probe.stdout + probe.stderr).strip().splitlines()[-1:] or [""]
        except (OSError, subprocess.TimeoutExpired) as error:
            status, usable, detail = f"could not start ({error})", False, [""]
        run.write(f"ship: validator interpreter {' '.join(candidate)}: {status} {detail[0]}".rstrip())
        if usable:
            return list(candidate)
    return None


def import_failure(result: subprocess.CompletedProcess) -> str | None:
    """Return the last traceback line when the process died on an import error, else None.

    A Python traceback ends with the exception's class name, so this reads that name, not prose.
    """
    lines = result.stderr.strip().splitlines()
    last = lines[-1] if lines else ""
    return last if result.returncode != 0 and last.startswith(IMPORT_ERRORS) else None


# Asks the validator's own freshness check (validate_planning_package.py, freshness()) whether plan content differs
# between the merge base and HEAD, so plan content has one definition: the validator's. Prints one JSON line after
# PLAN_ANSWER; {"entry": false} when the validator has no freshness().
PLAN_QUESTION = """
import copy, importlib.util, json, sys
from pathlib import Path
validator, repo, package, base = sys.argv[1:5]
sys.path.insert(0, str(Path(validator).parent))
spec = importlib.util.spec_from_file_location("ship_plan_validator", validator)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
if not callable(getattr(module, "freshness", None)):
    print("PLAN_ANSWER " + json.dumps({"entry": False}))
    sys.exit(0)
manifest = json.loads(Path(package).read_text())
asked = copy.deepcopy(manifest) if isinstance(manifest, dict) else {}
asked["subject_revision"] = base
parts = asked.get("parts") if isinstance(asked.get("parts"), dict) else {}
if isinstance(parts.get("cold_review"), dict):
    parts["cold_review"]["reviewed_revision"] = base
row = module.freshness(Path(repo), Path(package), asked)
print("PLAN_ANSWER " + json.dumps({"entry": True, "ok": bool(row.get("ok")), "changed": row.get("changed") or [],
                                    "problems": row.get("problems") or []}))
"""


def plan_unchanged_since(repo: Path, base: str, python: list[str], validator: str, cwd: Path) -> tuple[str | None, str]:
    """Return (why the validator may be skipped, or None to validate; what was asked and answered).

    Plan content is the validator's own: its freshness() is called with base as the reviewed revision and compares
    base with HEAD. The planning package itself also counts. Every doubt (no freshness() entry point, an error)
    answers None, which means validate. Shared with the push hook through scripts/plan_content.py.
    """
    manifest = subprocess.run(["git", "-C", str(repo), "diff", "--name-only", base, "HEAD", "--", PACKAGE],
                              capture_output=True, text=True)
    if manifest.returncode != 0:
        return None, f"git diff {base[:12]} failed: {manifest.stderr.strip()}"
    if manifest.stdout.strip():
        return None, f"{PACKAGE} itself changed since {base[:12]}"
    try:
        asked = subprocess.run([*python, "-c", PLAN_QUESTION, validator, str(repo), str(repo / PACKAGE), base],
                               cwd=cwd, capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as error:
        return None, f"plan-content question could not run ({error})"
    answers = [line[len("PLAN_ANSWER "):] for line in asked.stdout.splitlines() if line.startswith("PLAN_ANSWER ")]
    try:
        answer = json.loads(answers[-1]) if asked.returncode == 0 and answers else None
    except ValueError:
        answer = None
    detail = (f"plan-content question since {base[:12]}: exit status {asked.returncode}: "
              f"{answers[-1] if answers else (asked.stdout + asked.stderr).strip()[-500:]}")
    if not isinstance(answer, dict) or not answer.get("entry") or not answer.get("ok") or answer.get("changed"):
        return None, detail
    return (f"no plan content changed since {base[:12]} (the validator's freshness check: plan files, "
            f"docs/GOAL.md, openspec/specs/; and {PACKAGE} itself)"), detail


def plan_content_unchanged(run: Run, repo: Path, python: list[str], validator: str) -> str | None:
    """Return why the validator may be skipped (the merge changes no plan content), or None to validate.

    Brian, 2026-11-12, "i approve decision 4": a package is rechecked only when the plan's own content changes,
    never because code was committed. No merge base means validate.

    Implements: ship/validate-the-planning-package-only-when-the-merge-changes-plan-content
    """
    base = merge_base(repo)
    if not base:
        return None
    reason, detail = plan_unchanged_since(repo, base, python, validator, run.log.parent)
    run.write(f"ship: {detail}")
    return reason.replace("no plan content changed since", "the merge changes no plan content since", 1) if reason else None


def outside_fences(text: str) -> str:
    """Return text without its fenced code blocks: a page that quotes the format in a code block is not using it."""
    kept, fence = [], ""
    for line in text.splitlines():
        mark = FENCE.match(line)
        if not fence:
            if mark:
                fence = mark.group(1)
            else:
                kept.append(line)
        elif mark and mark.group(1).startswith(fence) and not line.strip().strip(fence[0]):
            fence = ""
    return "\n".join(kept)


def passing_read(text: str) -> bool:
    """Whether the last `Independent read:` line records a pass on a real date (a later read replaces an earlier one)."""
    reads = SMALL_PLAN_READ.findall(text)
    found = SMALL_PLAN_PASS.match(reads[-1]) if reads else None
    if not found:
        return False
    try:
        datetime.date.fromisoformat(found.group(1))
    except ValueError:
        return False
    return True


def one_page_plan_gaps(text: str) -> list[str] | None:
    """Return what a one-page plan lacks ([] when it is complete), or None when the page does not call itself small.

    The marker line, the headings and the read line count only outside fenced code blocks; the length is the whole file's.
    """
    own = outside_fences(text)
    if not SMALL_PLAN.search(own):
        return None
    gaps = [f"the heading `## {part}`" for part in SMALL_PLAN_PARTS
            if not re.search(rf"^## {re.escape(part)}[ \t]*$", own, re.M)]
    lines = len(text.splitlines())
    if lines > SMALL_PLAN_LINES:
        gaps.append(f"a length of at most {SMALL_PLAN_LINES} lines (it has {lines})")
    if not passing_read(own):
        gaps.append(f"the line `{SMALL_PLAN_READ_FORM}` recording an independent read that passed")
    return gaps


def committed_plan_pages(repo: Path) -> list[str]:
    """Every .md file git tracks under docs/plans/. A page git ignores is not on GitHub for Brian to read, so it does not count."""
    listed = subprocess.run(["git", "-C", str(repo), "ls-files", "-z", "--", PLANS_DIR], capture_output=True, text=True)
    return sorted(path for path in listed.stdout.split("\0") if path.endswith(".md")) if listed.returncode == 0 else []


def one_page_plans(repo: Path, paths: list[str] | None = None) -> dict[str, list[str]]:
    """Return {page: what it lacks} for the one-page plans among paths (default: every committed .md under docs/plans/).

    A byte-order mark is dropped and bytes that are not UTF-8 are replaced, so such a page is checked, not skipped.
    """
    if paths is None:
        paths = committed_plan_pages(repo)
    found = {}
    for path in paths:
        try:
            gaps = one_page_plan_gaps((repo / path).read_text(encoding="utf-8-sig", errors="replace"))
        except OSError:
            continue
        if gaps is not None:
            found[path] = gaps
    return found


def incomplete_pages(pages: dict[str, list[str]]) -> str:
    """Name each incomplete one-page plan and what it lacks, for a refusal."""
    return "; ".join(f"{page} lacks {', '.join(gaps)}" for page, gaps in pages.items() if gaps)


def one_page_plan_refusal(run: Run, repo: Path) -> str | None:
    """Return why a one-page plan this merge adds or changes stops the merge, or None when each one is complete.

    No merge base, or a diff git cannot make, means every committed one-page plan is checked. Names are read
    NUL-separated, because git puts a name with an accented letter or a quote in quotation marks otherwise.

    Implements: ship/check-every-one-page-plan-a-merge-adds-or-changes
    """
    base = merge_base(repo)
    paths = None
    if base:
        changed = subprocess.run(["git", "-C", str(repo), "diff", "-z", "--name-only", "--diff-filter=d", base, "HEAD",
                                  "--", PLANS_DIR], capture_output=True, text=True)
        if changed.returncode == 0:
            paths = [path for path in changed.stdout.split("\0") if path.endswith(".md")]
    pages = one_page_plans(repo, paths)
    for page, gaps in pages.items():
        if not gaps:
            line = (f"ship: one-page plan {page} is complete (its five parts, at most {SMALL_PLAN_LINES} lines, "
                    "a recorded independent read)")
            print(line)
            run.write(line)
    if any(pages.values()):
        return (f"{SIZE_RULE}: a one-page plan this merge adds or changes is incomplete: {incomplete_pages(pages)}. "
                "Complete the page, or remove the line `Plan size: small` when the work needs the full planning package")
    return None


PRIOR_ART_SCRIPT = "scripts/prior_art_check.py"   # in code2-workspace
PRIOR_ART_PYTHON = ["uv", "run", "--no-project", "--with", "jsonschema", "python"]
CHANGES_DIR = "openspec/changes/"


def prior_art_refusal(run: Run, repo: Path) -> str | None:
    """Return why the prior-art rule stops the merge, or None when every change the merge touches passes.

    Runs code2-workspace's prior-art check on the files under openspec/changes/ that the merge adds or changes
    (every unarchived change when there is no merge base). Anything other than exit 0 refuses: a check that is
    missing or cannot run is not taken as a pass.

    Implements: ship/refuse-a-merge-whose-openspec-change-lacks-a-prior-art-record
    """
    base = merge_base(repo)
    files: list[str] | None = None
    if base:
        changed = subprocess.run(["git", "-C", str(repo), "diff", "-z", "--name-only", "--diff-filter=d", base, "HEAD",
                                  "--", CHANGES_DIR], capture_output=True, text=True)
        if changed.returncode == 0:
            files = [path for path in changed.stdout.split("\0") if path]
            if not files:
                line = "ship: prior-art check not run: this merge adds or changes no OpenSpec change"
                print(line)
                run.write(line)
                return None
    workspace = Path(os.environ.get("SHIP_WORKSPACE", Path.home() / "code2" / "workspace"))
    script = workspace / PRIOR_ART_SCRIPT
    if not script.is_file():
        return (f"{PRIOR_ART_RULE}: the prior-art check {script} is missing, so this merge's OpenSpec changes cannot "
                f"be checked; run `git -C {workspace} pull --ff-only` (or set SHIP_WORKSPACE) and ship again")
    python = os.environ.get("SHIP_PRIOR_ART_PYTHON")
    command = [*(python.split() if python else PRIOR_ART_PYTHON), str(script), "--repo", str(repo)]
    if files is not None:
        command += ["--files", *files]
    result = run.step("prior-art check", command)
    said = (result.stdout + result.stderr).strip()
    if result.returncode == 0:
        line = f"ship: {said.splitlines()[-1] if said else 'prior-art check passed'}"
        print(line)
        run.write(line)
        return None
    if result.returncode == 1:
        return f"{PRIOR_ART_RULE}: an OpenSpec change this merge adds or changes has no decided prior-art record:\n{said}"
    return (f"{PRIOR_ART_RULE}: the prior-art check could not run (exit {result.returncode}); this is not a verdict "
            f"on the record. Its output:\n{said}")


def planning_gate(run: Run, repo: Path, *, always_validate: bool = False) -> str | None:
    """Return why the planning rules stop the merge, or None when it may proceed.

    always_validate runs the validator even when the merge changes no plan content (the merge-base check of a plan repair).
    """
    first_day = first_commit_day(repo)
    if first_day is None:
        return f"{NEW_RULE}: could not read this repository's first commit"
    new = first_day >= NEW_FROM
    if not (repo / PACKAGE).is_file():
        if new:
            # A complete, committed one-page plan stands in for the package when the work is small planned work
            # (Brian, 2026-11-15, "6 all"); it is read on GitHub, so the plan list is not consulted.
            pages = one_page_plans(repo)
            complete = [page for page, gaps in pages.items() if not gaps]
            if complete:
                line = (f"ship: new repository (first commit {first_day}) has no planning package; it has a complete "
                        f"one-page plan ({', '.join(complete)}), which the {SIZE_RULE} accepts for small planned work")
                print(line)
                run.write(line)
                return None
            lacking = f" Its one-page plan is incomplete: {incomplete_pages(pages)}." if pages else ""
            return (f"{NEW_RULE}: new repository (first commit {first_day}) with no planning package ({PACKAGE}) and no "
                    f"complete one-page plan ({PLANS_DIR}<name>.md; {SIZE_RULE}).{lacking} For small planned work write "
                    "the one-page plan; otherwise build the package with the company-planning:planning-compliance skill")
        # An older repository with no package merges with a warning (Brian, 2026-11-10, "i aprpove" to Decision 12, after
        # a tested wiki-tool fix could not land for lack of a package); a new repository (first commit on or after
        # NEW_FROM) is still refused above.
        line = (f"ship: warning: {PLANNING_RULE}: repository (first commit {first_day}) has no planning package "
                f"({PACKAGE}); not refused. Build it with the company-planning:planning-compliance skill when this "
                "repository is next planned")
        print(line)
        run.write(line)
        return None
    if new:
        refused = plan_list_refusal(run, repo)
        if refused:
            return refused
    validator = os.environ.get("SHIP_PLANNING_VALIDATOR")
    if not validator:
        source = Path(os.environ.get("SHIP_COMPANY_PLANNING", Path.home() / "code2" / "company-planning"))
        if run.step("fetch company-planning", ["git", "-C", str(source), "fetch", "-q", "origin"]).returncode:
            return f"could not fetch {source}, so the planning package cannot be validated"
        # the validator imports its sibling modules (coverage_check.py), so extract the whole scripts folder;
        # it finds goal_provenance.py three folders up, so every path keeps its place in company-planning
        scripts_dir = str(Path(VALIDATOR).parent)
        present = [p for p in GOAL_PROVENANCE
                   if subprocess.run(["git", "-C", str(source), "cat-file", "-e", f"origin/main:{p}"],
                                     capture_output=True).returncode == 0]
        archive = Path(run.log.parent) / "planning-validator.tar"
        target = Path(run.log.parent) / "planning-validator"
        target.mkdir(parents=True, exist_ok=True)
        made = run.step("archive the validator folder from company-planning origin/main",
                        ["git", "-C", str(source), "archive", "-o", str(archive), "origin/main", scripts_dir, *present])
        if made.returncode:
            return f"could not archive {scripts_dir} from {source} origin/main"
        unpacked = run.step("unpack the validator folder", ["tar", "-x", "-f", str(archive), "-C", str(target)])
        if unpacked.returncode:
            return f"could not unpack {scripts_dir} into {target}"
        validator = str(target / VALIDATOR)
    if not Path(validator).is_file():
        return f"the planning validator {validator} does not exist"
    python = validator_python(run)
    if python is None:
        return (f"the planning validator could not run: none of {', '.join(' '.join(c) for c in VALIDATOR_PYTHONS)} "
                f"imports the validator's packages ({VALIDATOR_IMPORTS}). This is not a verdict on the planning "
                "package. Install them for /usr/bin/python3, or set SHIP_VALIDATOR_PYTHON to an interpreter that has them")
    skipped = None if always_validate else plan_content_unchanged(run, repo, python, validator)
    if skipped:
        line = f"ship: skipped the planning validator: {skipped}"
        print(line)
        run.write(line)
        return None
    result = run.step("planning package", [*python, validator, "--repo", str(repo), str(repo / PACKAGE)])
    print((result.stdout + result.stderr).rstrip())
    broken = import_failure(result)
    if broken:
        return (f"the planning validator could not run ({broken}). This is not a verdict on the planning "
                "package. Set SHIP_VALIDATOR_PYTHON to an interpreter that has the validator's packages")
    goals = GOAL_LINE.search(result.stdout)
    if goals:
        line = f"ship: goal provenance: {goals.group(1)} (required from {goals.group(2)})"
        print(line)
        run.write(line)
    if result.returncode != 0:
        # Decision 6 of the Work flow row (2026-11-07): a package that fails only freshness warns, not refuses. Since
        # 2026-11-10 (Brian, "i approve decision 1-2") freshness means plan content changed since the cold review.
        aged = run.step("planning package without the freshness check",
                        [*python, validator, "--repo", str(repo), str(repo / PACKAGE), "--no-freshness"])
        if aged.returncode == 0:
            line = (f"ship: warning: the planning package {PACKAGE} is out of date: its plan content changed "
                    "since its cold review (it passes without that check); not refused. Run the cold review again "
                    "(company-planning:planning-compliance) and record the revision it read")
            print(line)
            run.write(line)
            return None
        return (f"the planning package is not compliant (validator exit {result.returncode}); rebuild it "
                "with the company-planning:planning-compliance skill, commit, and ship again")
    return None


PLAN_PATHS = ("docs/", "wiki/", "planning/")   # with any *.md: what a plan repair may change
# Record-only folders: a run's case folder, result files and captured sources. Adding a result there changes no
# behavior the planning package describes (Brian, 2026-11-10, "fix it: 1 to 4", recommendation 1, after "ok so it seems like
# my whole system is messed up and jut causing endless paperowrk": a pre-registration merge was refused for lack of a package).
RECORD_PATHS = ("cases/", "results/", "raw/")


def merge_base(repo: Path) -> str:
    """The commit where this branch left the default branch, or "" when git cannot say."""
    def read(*args: str) -> str:
        """Return git's stripped output, or "" when git fails."""
        done = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
        return done.stdout.strip() if done.returncode == 0 else ""
    default = read("symbolic-ref", "-q", "--short", "refs/remotes/origin/HEAD") or "origin/main"
    return read("merge-base", "HEAD", default)


def base_planning_refusal(run: Run, repo: Path) -> str | None:
    """Why the planning gate refuses the merge base, or None when the base passes (or cannot be judged).

    The plan-repair exception lets a documentation branch repair a failing package, never make a passing one
    fail (issue #261: a docs-only branch broke goal provenance and blocked every later ship).
    """
    base = merge_base(repo)
    if not base:
        return "the merge base could not be found"
    scratch = tempfile.mkdtemp(prefix="ship-base-")
    tree = Path(scratch) / "base"
    added = run.step("check out the merge base", ["git", "-C", str(repo), "worktree", "add", "--detach", str(tree), base])
    try:
        if added.returncode:
            return None
        return planning_gate(run, tree, always_validate=True)
    finally:
        subprocess.run(["git", "-C", str(repo), "worktree", "remove", "--force", str(tree)], capture_output=True)
        shutil.rmtree(scratch, ignore_errors=True)


def plan_only_change(repo: Path) -> list[str] | None:
    """The files this branch changes when every one is a planning or documentation file, else None.

    A repository that is not compliant must still be able to become compliant, so the planning gate never
    refuses a branch that only repairs the plan (Brian, 2026-11-05: "i want to make sure that this block
    doesnt block updating hte plans themself. like it needs to be able to become complaint if it is not").
    """
    def read(*args: str) -> str:
        """Return git's stripped output, or "" when git fails."""
        done = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
        return done.stdout.strip() if done.returncode == 0 else ""
    base = merge_base(repo)
    if not base:
        return None
    changed = [f for f in read("diff", "--name-only", base, "HEAD").splitlines() if f]
    if not changed or not all(f.startswith(PLAN_PATHS) or f.endswith(".md") for f in changed):
        return None
    return changed


# Upkeep that changes no required behavior (Brian, 2026-11-06, "i aprpove": model-name, dependency-version and
# documentation updates do not count as work). The same rule as Company Planning's freshness check
# (validate_planning_package.py, _is_upkeep); judged from the lines a branch changes, never from its messages.
_MODEL_ID = re.compile(r"(?:[A-Za-z0-9_.-]+/)*(?:gpt|gemini|claude|o[1-9]|llama|mistral|mixtral|deepseek|qwen|grok|kimi|glm|"
                       r"command|sonar|phi|gemma|nova)-[A-Za-z0-9_.:-]*[A-Za-z0-9]", re.IGNORECASE)
_VERSION = re.compile(r"\d+(?:\.\d+)+(?:[a-z]+\d*)?")
_LOCK_FILES = {"uv.lock", "poetry.lock", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "Cargo.lock",
               "Gemfile.lock", "go.sum", "composer.lock", "Pipfile.lock"}
_DEPENDENCY_FILES = {"pyproject.toml", "package.json", "Cargo.toml", "go.mod", "Gemfile", "Pipfile"}


def _upkeep_file(repo: Path, base: str, path: str) -> bool:
    """True for a lock file, or a file whose changed lines differ from removed lines only in model names
    (and, in dependency manifests, version numbers)."""
    name = path.rsplit("/", 1)[-1]
    if name in _LOCK_FILES:
        return True
    shown = subprocess.run(["git", "-C", str(repo), "diff", "--unified=0", "--no-renames", base, "HEAD", "--", path],
                           capture_output=True, text=True)
    out = "\n" + shown.stdout
    if shown.returncode != 0 or "Binary files" in out or "\nnew file mode" in out or "\ndeleted file mode" in out:
        return False
    is_dep = name in _DEPENDENCY_FILES or (name.startswith("requirements") and name.endswith(".txt"))

    def norm(line: str) -> str:
        """Mask model names (and, in dependency manifests, versions) so only other differences remain."""
        line = _MODEL_ID.sub("<model>", line)
        return _VERSION.sub("<version>", line) if is_dep else line
    removed, added, raw = [], [], []
    for line in shown.stdout.splitlines():
        if line.startswith(("---", "+++")) or not line or line[0] not in "-+":
            continue
        (removed if line[0] == "-" else added).append(norm(line[1:]))
        raw.append(line[1:])
    return bool(raw) and sorted(removed) == sorted(added) and any(norm(r) != r for r in raw)


def upkeep_only_change(repo: Path) -> list[str] | None:
    """The files this branch changes when every one is upkeep (a model-name or dependency-version update, a lock
    file, a planning or documentation file, or a file in a record-only folder: RECORD_PATHS), else None. Such a branch changes nothing the planning package
    describes, so the planning gate does not hold it (Brian, 2026-11-06, "i aprpove", Decision 2)."""
    def read(*args: str) -> str:
        """Return git's stripped output, or "" when git fails."""
        done = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
        return done.stdout.strip() if done.returncode == 0 else ""
    base = merge_base(repo)
    if not base:
        return None
    changed = [f for f in read("diff", "--name-only", base, "HEAD").splitlines() if f]
    if not changed or not all(f.startswith(PLAN_PATHS + RECORD_PATHS) or f.endswith(".md") or _upkeep_file(repo, base, f)
                              for f in changed):
        return None
    return changed


DEFAULT_CHECK = "make check"

ENVIRONMENTS = [  # (files that call for it, what it creates, the command that creates it, only for a Makefile check)
    (("uv.lock", "pyproject.toml"), ".venv", ["uv", "sync", "--all-extras"], True),
    (("package-lock.json",), "node_modules", ["npm", "ci"], False),
]


def is_makefile_check(check: str) -> bool:
    """True when the check is a `make` command, which is the repository's own Makefile check."""
    try:
        words = shlex.split(check)
    except ValueError:
        return False
    while words and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", words[0]):  # leading VAR=value words
        words = words[1:]
    return bool(words) and words[0] == "make"


def prepare_environment(run: Run, repo: Path, check: str = DEFAULT_CHECK) -> str | None:
    """Create a missing .venv or node_modules at the repository top; return why it failed, or None.

    The Python environment is made only for a Makefile check. A failed command removes the folder it just
    created, which did not exist before the step, so no empty one is left behind.
    """
    for markers, made, cmd, makefile_only in ENVIRONMENTS:
        if any((repo / m).is_file() for m in markers) and not (repo / made).exists():
            if makefile_only and not is_makefile_check(check):
                line = f"ship: environment `{' '.join(cmd)}` skipped: the check `{check}` is not a Makefile check"
                print(line)
                run.write(line)
                continue
            result = run.step(f"environment `{' '.join(cmd)}`", cmd)
            if result.returncode != 0:
                print("\n".join((result.stdout + result.stderr).rstrip().splitlines()[-15:]))
                leftover = repo / made
                if leftover.is_dir() and not leftover.is_symlink():  # absent before this step, so the step made it
                    shutil.rmtree(leftover)
                    run.write(f"ship: removed the {made} that the failed `{' '.join(cmd)}` left behind")
                return f"`{' '.join(cmd)}` exited {result.returncode}"
    return None


def passed_record() -> Path:
    """Return the file of trees whose check passed."""
    return Path(os.environ.get("SHIP_STATE_DIR", Path.home() / ".local" / "state" / "ship")) / "passed.jsonl"


def already_passed(tree: str, check: str) -> dict | None:
    """Return the newest record of this tree passing this check command, or None."""
    found = None
    try:
        lines = passed_record().read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    for line in lines:
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        if isinstance(entry, dict) and entry.get("tree") == tree and entry.get("check") == check:
            found = entry
    return found


def record_pass(repo: Path, tree: str, check: str, head: str) -> None:
    """Append that this tree passed this check command."""
    record = passed_record()
    record.parent.mkdir(parents=True, exist_ok=True)
    entry = {"tree": tree, "check": check, "repo": str(repo), "head": head,
             "time": datetime.datetime.now().isoformat(timespec="seconds")}
    with record.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


@contextlib.contextmanager
def check_slot(run: Run, repo: Path):
    """Hold one machine-wide check slot while the body runs; yield the slot number, or None when none came free.

    A slot is a flock on a file under $SHIP_STATE_DIR/check-slots, so a killed run frees it at once. The file
    says which repository holds it, and a run that has to wait prints that list once. $SHIP_CHECK_SLOTS = 0
    turns the limit off (yields 0 without locking).
    """
    slots = int(os.environ.get("SHIP_CHECK_SLOTS", CHECK_SLOTS))
    if slots <= 0:
        yield 0
        return
    wait = float(os.environ.get("SHIP_SLOT_WAIT", SLOT_WAIT))
    folder = passed_record().parent / "check-slots"
    folder.mkdir(parents=True, exist_ok=True)
    started, announced, held, number = time.monotonic(), False, None, None
    while held is None:
        busy = []
        for n in range(slots):
            handle = open(folder / f"slot-{n}.lock", "a+", encoding="utf-8")
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                handle.seek(0)
                busy.append(handle.read().strip() or f"slot {n}")
                handle.close()
                continue
            handle.seek(0)
            handle.truncate()
            handle.write(f"{repo.name} (pid {os.getpid()})")
            handle.flush()
            held, number = handle, n
            break
        if held is not None:
            break
        waited = time.monotonic() - started
        if waited >= wait:
            break
        if not announced:
            line = f"ship: all {slots} check slots are taken ({'; '.join(busy)}); waiting up to {wait:.0f} s"
            print(line)
            run.write(line)
            announced = True
        time.sleep(min(SLOT_POLL, max(0.0, wait - waited)))
    if held is not None and announced:
        line = f"ship: check slot {number} free after {time.monotonic() - started:.0f} s"
        print(line)
        run.write(line)
    try:
        yield number
    finally:
        if held is not None:
            held.close()   # closing the file releases the lock


def read_json(result: subprocess.CompletedProcess):
    """Return the JSON a gh step printed, or None when it failed or did not print JSON."""
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def requires_linear_history(run: Run, branch: str) -> bool:
    """Return whether the branch's protection or an active ruleset requires linear history.

    Unprotected, or protection this login cannot read (404, 403), counts as not required: GitHub enforces
    the rule at merge time, and a rule that cannot be seen is no reason to refuse before the check.
    """
    protection = read_json(run.step(f"read protection of {branch} (exit 1 with a 404 means none)",
                                    ["gh", "api", f"repos/{{owner}}/{{repo}}/branches/{branch}/protection"]))
    if isinstance(protection, dict) and (protection.get("required_linear_history") or {}).get("enabled"):
        return True
    rules = read_json(run.step(f"read rulesets of {branch}",
                               ["gh", "api", f"repos/{{owner}}/{{repo}}/rules/branches/{branch}"]))
    return isinstance(rules, list) and any(isinstance(r, dict) and r.get("type") == "required_linear_history"
                                           for r in rules)


def choose_method(run: Run, requested: str | None) -> str | None:
    """Return the merge method to use, or None when the repository allows none (the caller stops the run).

    Read before the check, so a repository that cannot take the merge costs no check. Settings that cannot
    be read leave the old behaviour (the requested method, else merge) and say so.
    """
    info = read_json(run.step("read merge settings", ["gh", "repo", "view", "--json", SETTINGS_FIELDS]))
    if not isinstance(info, dict):
        method = requested or "merge"
        note = f"ship: merge settings unreadable; using {method} unchecked"
        print(note)
        run.write(note)
        return method
    allowed = [m for m in FALLBACK_ORDER if info.get(ENABLED_BY[m], True)]
    branch = (info.get("defaultBranchRef") or {}).get("name")
    why = "the repository's settings disable it"
    if branch and "merge" in allowed and requires_linear_history(run, branch):
        allowed.remove("merge")
        why = f"{branch} requires linear history"
    if not allowed:
        return None
    default = METHODS.get(info.get("viewerDefaultMergeMethod") or "")
    wanted = requested or default
    if wanted in allowed:
        return wanted
    chosen = allowed[0]
    if wanted is None:
        return chosen
    note = f"ship: merge method: {wanted or 'the default'} is not allowed ({why}); using {chosen}"
    print(note)
    run.write(note)
    return chosen


def main(argv: list[str] | None = None) -> int:
    """Ship the current branch of --repo; return 0 only when its pull request is merged."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--check", default=DEFAULT_CHECK)
    parser.add_argument("--method", choices=sorted(METHODS.values()))
    parser.add_argument("--recheck", action="store_true", help="run the check even if this tree already passed it")
    parser.add_argument("--keep-lane", action="store_true",
                        help="after the merge, do not remove this lane (also SHIP_KEEP_LANE=1)")
    args = parser.parse_args(argv)
    repo = Path(git(args.repo, "rev-parse", "--show-toplevel"))
    run = Run(repo)
    branch = git(repo, "branch", "--show-current")
    if not branch or branch in ("main", "master"):
        return run.fail(f"on {branch or 'a detached HEAD'}; ship works from a feature branch")
    if git(repo, "status", "--porcelain"):
        return run.fail("the tree has uncommitted changes; commit them first")
    head = git(repo, "rev-parse", "HEAD")
    incomplete = one_page_plan_refusal(run, repo)
    if incomplete:
        return run.fail(f"{incomplete}; nothing was pushed")
    no_record = prior_art_refusal(run, repo)
    if no_record:
        return run.fail(f"{no_record}\nnothing was pushed")
    refused = planning_gate(run, repo)
    if refused:
        changed = plan_only_change(repo)
        if changed is not None and base_planning_refusal(run, repo) is None:
            return run.fail(f"{refused}; this branch changes only planning and documentation files, but the merge "
                            "base passes the planning gate, so the branch would make a compliant package fail "
                            "(a plan repair may fix a failing package, never break a passing one); nothing was pushed")
        if changed is not None:
            line = (f"ship: planning gate not met ({refused}), but this branch changes only planning and "
                    f"documentation files ({len(changed)}), so it may merge: a plan must always be able to become "
                    "compliant")
        else:
            changed = upkeep_only_change(repo)
            if changed is None:
                return run.fail(f"{refused}; nothing was pushed")
            line = (f"ship: planning gate not met ({refused}), but this branch is upkeep only ({len(changed)} files: "
                    "model names, dependency versions, lock files, documentation or record-only folders "
                    f"{', '.join(RECORD_PATHS)}), so it may merge")
        print(line)
        run.write(line)
    method = choose_method(run, args.method)
    if not method:
        return run.fail("no merge method is allowed on this repository; nothing was pushed")
    tree = git(repo, "rev-parse", "HEAD^{tree}")
    passed = None if args.recheck else already_passed(tree, args.check)
    if passed:
        line = (f"ship: check skipped: tree {tree[:12]} already passed `{args.check}` at {passed.get('time')} "
                f"(head {str(passed.get('head'))[:8]})")
        print(line)
        run.write(line)
    else:
        with check_slot(run, repo) as slot:
            if slot is None:
                return run.fail(f"no check slot came free within {os.environ.get('SHIP_SLOT_WAIT', SLOT_WAIT)} s "
                                f"(SHIP_CHECK_SLOTS={os.environ.get('SHIP_CHECK_SLOTS', CHECK_SLOTS)}); nothing was pushed")
            failed = prepare_environment(run, repo, args.check)
            if failed:
                return run.fail(f"the environment could not be set up: {failed}; nothing was pushed")
            # pipefail: a check written as `cmd | tail -1` must fail when cmd fails, not report tail's 0.
            check = run.step(f"check `{args.check}` on {head[:8]}", ["bash", "-o", "pipefail", "-c", args.check])
        tail = "\n".join((check.stdout + check.stderr).rstrip().splitlines()[-15:])
        if tail:
            print(tail)
        if check.returncode != 0:
            return run.fail("the check failed; nothing was pushed")
    if git(repo, "status", "--porcelain") or git(repo, "rev-parse", "HEAD") != head:
        return run.fail("the check changed the tree or HEAD; commit what it wrote and ship again")
    if not passed:
        record_pass(repo, tree, args.check, head)
    if run.step("push", ["git", "push", "-u", "origin", branch]).returncode != 0:
        return run.fail("push failed")
    # Only an open one: `gh pr view <branch>` also returns a merged pull request, and merging that again
    # exits 0 and reads back MERGED while the new commit never lands (code2-workspace #206, 2026-11-07).
    view = run.step("find open pull request", ["gh", "pr", "list", "--head", branch, "--state", "open",
                                                "--json", "number", "-q", ".[0].number"])
    number = view.stdout.strip() if view.returncode == 0 else ""
    if not number:
        created = run.step("open pull request", ["gh", "pr", "create", "--fill", "--head", branch])
        if created.returncode != 0:
            return run.fail("could not open the pull request")
        number = created.stdout.strip().rsplit("/", 1)[-1]
    merged = run.step(f"merge #{number} ({method})", ["gh", "pr", "merge", number, f"--{method}",
                                                      "--match-head-commit", head])
    if merged.returncode != 0:
        return run.fail(f"gh pr merge #{number} failed")
    state = run.step(f"read back #{number}", ["gh", "pr", "view", number, "--json", "state,mergeCommit"])
    data = json.loads(state.stdout or "{}") if state.returncode == 0 else {}
    if data.get("state") != "MERGED":
        return run.fail(f"#{number} reads back as {data.get('state', 'unknown')}, not MERGED")
    line = f"ship: merged #{number} as {(data.get('mergeCommit') or {}).get('oid', '?')}; exit status 0"
    print(line)
    run.write(line)
    sweep_lanes(run, repo, keep=args.keep_lane or os.environ.get("SHIP_KEEP_LANE") == "1")
    return 0


def sweep_script() -> Path:
    """Return lane_sweep.py beside the real ship.py; ship runs through the ~/.local/bin/ship symlink."""
    return Path(__file__).resolve().with_name("lane_sweep.py")


def sweep_lanes(run: "Run", repo: Path, keep: bool = False) -> None:
    """Remove this repository's finished lanes, this one included unless keep, now that its pull request merged.

    The merge already proved this lane's tip is the merged head, so it skips the idle wait; every
    other check in lane_sweep still applies. With keep, this lane is passed as --keep-lane and stays
    for the caller (BrianMills2718/dodaf#563). A failed sweep never fails the ship.
    """
    sweep = sweep_script()
    try:
        lane = git(repo, "rev-parse", "--show-toplevel")
        main_repo = Path(git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir")).parent
        mode = "--keep-lane" if keep else "--merged-lane"
        run.step("sweep finished lanes", [sys.executable, str(sweep), "--apply", "--repo", str(main_repo),
                                          mode, lane])
        if keep:
            line = "ship: kept this lane (--keep-lane); the periodic sweep removes it once idle"
            print(line)
            run.write(line)
    except (OSError, subprocess.SubprocessError) as exc:
        run.write(f"ship: lane sweep did not run: {exc}")


if __name__ == "__main__":
    sys.exit(main())

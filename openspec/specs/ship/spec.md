# ship Specification

## Purpose

Merge a pull request only when the repository's own check passed on the exact commit being merged, so a failing check can never merge.

Ported into AES from code2-workspace commit eafa8e06894917f0d297e281202b60e86b12f819 (2026-11-16) under the AES consolidation plan, item 7 (Brian, 2026-11-16, Decision 25). The installed `ship` command still runs the workspace copy until a side-by-side run switches it over. In the port, where the plan list lives became the person's setting (`graph-config.yaml`), not code.

## Requirements

### Requirement: Merge only the commit whose check passed

`scripts/ship.py` SHALL run the repository's check (default `make check`, or `--check`) on a clean
tree, and push and merge only when it exits 0. The merge SHALL be pinned to the checked commit
(`gh pr merge --match-head-commit`), the pull request merged SHALL be one that is open for the
branch (a merged one is never reused), and the run SHALL succeed only when the pull request reads back
as MERGED. Every step prints its exit status and time, and the whole run is appended to one log file
per day.

Source: Brian, 2026-10-24, "i approve" (the proposal named one ship command that runs the check and merges only if it passes, after PR #548 merged with a failing test)

#### Scenario: A failing check pushes nothing

- **GIVEN** a clean branch whose check exits 1
- **WHEN** ship runs
- **THEN** it exits 1, and the branch is not on the remote

#### Scenario: A dirty tree is refused before the check

- **GIVEN** a branch with an uncommitted change
- **WHEN** ship runs
- **THEN** it exits 1 without running the check

#### Scenario: A passing check merges the checked commit

- **GIVEN** a clean branch whose check exits 0
- **WHEN** ship runs
- **THEN** it pushes the branch, opens a pull request, merges it with `--match-head-commit` set to the checked commit, reads back MERGED and exits 0

#### Scenario: A merge that does not read back as MERGED fails

- **GIVEN** a passing check whose pull request reads back as OPEN after the merge call
- **WHEN** ship runs
- **THEN** it exits 1

#### Scenario: A branch whose earlier pull request merged gets a new pull request

- **GIVEN** a passing check on a branch whose only pull request is already merged
- **WHEN** ship runs
- **THEN** it looks up only an open pull request for the branch, opens a new one, and merges that one

### Requirement: Prepare a fresh worktree's environment before the check

Before running the check, `scripts/ship.py` SHALL run `uv sync --all-extras` when the repository top
has a `uv.lock` or `pyproject.toml`, no `.venv`, and the check is a `make` command (the repository's own Makefile check,
which the default `make check` is), and `npm ci` when it has a `package-lock.json` and
no `node_modules`. A `--check` that is not a `make` command SHALL NOT trigger `uv sync`, and ship SHALL print one line saying it was skipped.
Each step that runs SHALL be a logged step, and a nonzero exit SHALL stop the run with nothing
pushed and SHALL remove the `.venv` or `node_modules` that the failed step created. An environment that is already present SHALL be left alone.

Source: inferred by agent from a 14-day audit of `~/code2/.ship-logs/`: fresh worktrees failed the check for a missing `.venv` or `node_modules` (three wasted runs of about 2.5 minutes in one session). Changed 2026-11-17 on Brian's instruction: research_v3 could not ship a hook-only change with `--check` because `uv sync` failed on open-web-retrieval and left an empty `.venv`.

#### Scenario: A fresh worktree gets its environment before the check

- **GIVEN** a clean branch with `pyproject.toml` and `package-lock.json` but no `.venv` or `node_modules`
- **WHEN** ship runs with the Makefile check (`make check`), which needs both
- **THEN** it runs `uv sync --all-extras` and `npm ci` first, merges and exits 0, and a later run with both present runs neither

#### Scenario: A failing environment setup pushes nothing

- **GIVEN** a clean branch with `pyproject.toml`, no `.venv`, and `uv sync` exiting 1
- **WHEN** ship runs the Makefile check
- **THEN** it exits 1 without running the check, and the branch is not on the remote

#### Scenario: A failing environment setup leaves no empty folder

- **GIVEN** a clean branch with `pyproject.toml`, no `.venv`, and a `uv sync` that exits 1 after creating an empty `.venv`
- **WHEN** ship runs the Makefile check
- **THEN** it exits 1 and the `.venv` no longer exists

#### Scenario: A custom check does not sync the python environment

- **GIVEN** a clean branch with `pyproject.toml`, no `.venv`, and a `uv sync` that would exit 1
- **WHEN** ship runs with `--check` set to a command that is not a `make` command
- **THEN** `uv` is never called, the check runs, the branch merges and ship exits 0

### Requirement: Skip a check that already passed on the same tree

After the check exits 0 on an unchanged tree, `scripts/ship.py` SHALL append the tree hash
(`git rev-parse HEAD^{tree}`), check command, repository, head and time to
`~/.local/state/ship/passed.jsonl` (folder overridable by `$SHIP_STATE_DIR`). Before running the
check, when an entry has the same tree hash and check command, ship SHALL skip the check and print
and log `ship: check skipped: tree <hash> already passed`<cmd>`at <time> (head <sha>)`. `--recheck`
SHALL run the check regardless. A failed check SHALL record nothing.

Source: inferred by agent from a 14-day audit of `~/code2/.ship-logs/`: identical trees were re-checked after unrelated failures.

#### Scenario: A tree that already passed skips the check

- **GIVEN** a tree whose check passed in an earlier ship run, now under a different head
- **WHEN** ship runs with the same check command
- **THEN** it prints `check skipped`, does not run the check, merges the new head and exits 0

#### Scenario: Recheck runs the check again

- **GIVEN** a tree whose check already passed
- **WHEN** ship runs with `--recheck`
- **THEN** it runs the check again

#### Scenario: A different check command or a failed check is not skipped

- **GIVEN** a tree whose check failed, or passed only under another command
- **WHEN** ship runs
- **THEN** it runs the check

### Requirement: Keep its own lane when the caller still needs it

When given `--keep-lane`, or when the environment has `SHIP_KEEP_LANE=1`, `scripts/ship.py` SHALL,
after the pull request reads back MERGED, run the lane sweep for its repository without removing its
own lane (passing it to `scripts/lane_sweep.py` as `--keep-lane`, which keeps that lane with the reason
`kept by --keep-lane`), and SHALL print and log
`ship: kept this lane (--keep-lane); the periodic sweep removes it once idle`. The repository's other
finished lanes SHALL still be removed. Without the flag, ship SHALL remove its own lane as before.

Source: inferred by agent from BrianMills2718/dodaf#563: ship's after-merge sweep removed the worktree dodaf's `scripts/release.py` was still running in, and release.py crashed with `FileNotFoundError` writing `.release-logs`.

#### Scenario: Keep-lane leaves this lane and sweeps the others

- **GIVEN** a clean lane being shipped and another clean lane whose work is already on main
- **WHEN** ship runs with `--keep-lane` and the merge reads back MERGED
- **THEN** it prints `kept this lane (--keep-lane)`, exits 0, this lane and its branch remain, and the other lane is removed

#### Scenario: The lane sweep is found beside the real ship

- **GIVEN** ship run through a symlink to `scripts/ship.py`
- **WHEN** it looks for the lane sweep
- **THEN** it uses `lane_sweep.py` beside the real file, not beside the symlink

#### Scenario: The environment variable keeps the lane too

- **GIVEN** a clean lane being shipped
- **WHEN** ship runs with `SHIP_KEEP_LANE=1` and no flag
- **THEN** the lane and its branch remain after the merge

### Requirement: Refuse a new repository with no planning package

Before running the check, `scripts/ship.py` SHALL refuse, with nothing pushed, a repository whose first commit
is on or after 2026-11-05 and that has neither `docs/planning/planning-package.json` nor a complete one-page
plan (requirement "Check every one-page plan a merge adds or changes"), naming the rule, the one-page plan and
the company-planning:planning-compliance skill, and naming what each incomplete one-page plan lacks. A new
repository with no package and at least one complete one-page plan committed under `docs/plans/` SHALL proceed:
ship SHALL print and log one line naming the page, and SHALL not read the plan list. For this it reads every
committed one-page plan, whether or not the merge touches it; a page git does not track does not count. A repository whose first commit
is earlier SHALL merge with a printed warning that names the rule and the skill. It applies only when ship
merges in that repository; ship SHALL start no agent for it.

Source: Brian, 2026-11-10, "i aprpove" to Decision 12 (an older repository with no package merges with a warning, not a refusal), after "ok so it seems like my whole system is messed up and jut causing endless paperowrk". This replaces Brian's 2026-11-05 "make it active now but it should only matter when you try to work in that repo", which refused an older repository with no package, and keeps the refusal for a new repository (Brian, 2026-11-04). The one-page plan in place of the package: Brian, 2026-11-15, "6 all" (decision record 0010: "a new repository needs the one page or a package"); not reading the plan list for it, and counting only a committed page, were inferred by agent, because a one-page plan is read on GitHub.

#### Scenario: An older repository with no package merges with a warning

- **GIVEN** a repository with no planning package whose first commit is before 2026-11-05
- **WHEN** ship runs with a passing check
- **THEN** it prints a warning naming the planning-compliance skill, runs the check, starts no agent, merges, and exits 0

#### Scenario: An older repository with a passing package merges

- **GIVEN** a repository whose first commit is before 2026-11-05, with a planning package the validator accepts
- **WHEN** ship runs with a passing check
- **THEN** it merges and exits 0 without reading the plan list

#### Scenario: A new repository with a one-page plan and no package merges

- **GIVEN** a repository whose first commit is on 2026-11-05, with no planning package and a complete one-page plan
- **WHEN** ship runs with a passing check
- **THEN** it prints a line naming the one-page plan, does not read the plan list, merges and exits 0

#### Scenario: A new repository whose only one-page plan is incomplete is refused

- **GIVEN** a repository whose first commit is on 2026-11-05, with no planning package and, on its default branch, a one-page plan with no `## Cost and time` heading
- **WHEN** ship runs on a branch that changes only another file
- **THEN** it exits 1 before the check runs, names the page and the missing heading, and the branch is not on the remote

#### Scenario: An uncommitted one-page plan does not stand in for the package

- **GIVEN** a repository whose first commit is on 2026-11-05, with no planning package, whose only complete one-page plan is a file git ignores
- **WHEN** ship runs
- **THEN** it exits 1 before the check runs, says there is no complete one-page plan, and the branch is not on the remote

### Requirement: A plan repair is never refused

When the planning gate would refuse (no package, or a package the validator rejects), `scripts/ship.py`
SHALL still let the branch proceed when every file it changes since its merge base with the default branch
is a planning or documentation file (under `docs/`, `wiki/` or `planning/`, or any `*.md`), and SHALL print
that it did so. A branch that changes any other file SHALL be refused as before. The exception repairs, never
breaks: ship SHALL also run the planning gate on the merge base, and when the base passes it SHALL refuse the
branch (the branch would make a compliant package fail; issue #261).

Source: Brian, 2026-11-05, "i want to make sure that this block doesnt block updating hte plans themself. like it needs to be able to become complaint if it is not".

#### Scenario: A plan repair merges while the package fails

- **GIVEN** a branch that changes only planning and documentation files, and a package the validator rejects
- **WHEN** ship runs
- **THEN** it says the branch changes only planning and documentation files, merges, and exits 0

#### Scenario: A plan repair never breaks a passing package

- **GIVEN** a branch that changes only documentation files, a merge base the planning gate passes, and a package the validator rejects once the branch is applied
- **WHEN** ship runs
- **THEN** it refuses, exits 1 and pushes nothing

### Requirement: Refuse a planning package the validator rejects

Before running the check, `scripts/ship.py` SHALL look for `docs/planning/planning-package.json`.
When it exists, ship SHALL run Company Planning's `validate_planning_package.py` on it, read from
`origin/main` of the company-planning repository (`$SHIP_COMPANY_PLANNING`, default
`~/code2/company-planning`, fetched first), and stop with nothing pushed unless the validator exits 0 or fails only for age (below).
This holds however old the repository is. When the validator cannot be fetched or run, ship SHALL stop, and SHALL say it could not run, which is
not a verdict on the package. ship SHALL run the validator under a fixed interpreter that imports its
packages (`jsonschema`, `pydantic`), never under ship's own python, which is a project's venv when a
caller such as `uv run scripts/release.py` runs ship: the first of `/usr/bin/python3` and
`uv run --no-project --with jsonschema --with pydantic python` that imports both, or the command line
in `$SHIP_VALIDATOR_PYTHON`. A validator that dies on an import error SHALL stop ship as "could not run",
without the `--no-freshness` rerun.
When the validator rejects the package, ship SHALL run it once more with `--no-freshness`; when that run
exits 0, the package failed only for its age, so ship SHALL print a warning that names the out-of-date
package and proceed.

Source: Brian, 2026-10-25, "i dont get why i have asked 100s of times to make ure that my proejcts are always company plannign complaint and they never are and it is never enforced", then "yes that soudns good" to ship refusing a failing package. Age-only failures warn instead of refusing: the Work flow row's decision 6, approved under Brian's decision rule of 2026-11-07 ("i am auto approving al decisions that arent high significane and low confidence"), after ship refused a logging change in company-planning for a 29-day-old package.

Interpreter and could-not-run reporting: inferred by agent from issue 197 (filed 2026-11-07 after dodaf release dodaf-mock-ccd3eb7 stopped on `No module named 'jsonschema'` under `uv run`); a technical call, not a product or priority one.

#### Scenario: A failing planning package pushes nothing

- **GIVEN** a clean branch with a planning package the validator rejects (exit 1)
- **WHEN** ship runs
- **THEN** it exits 1 before the check runs, and the branch is not on the remote

#### Scenario: A compliant planning package lets the merge proceed

- **GIVEN** a clean branch with a planning package the validator accepts and a passing check
- **WHEN** ship runs
- **THEN** it merges and exits 0

#### Scenario: A validator that cannot run stops the merge

- **GIVEN** a planning package and a validator that cannot be found
- **WHEN** ship runs
- **THEN** it exits 1 and the branch is not on the remote

#### Scenario: A package that is only out of date warns and proceeds

- **GIVEN** a clean branch with a planning package the validator rejects only for age (it passes with `--no-freshness`), and a passing check
- **WHEN** ship runs
- **THEN** it prints that the planning package is out of date and not refused, merges, and exits 0

#### Scenario: The validator runs under an interpreter that has its packages

- **GIVEN** a planning package, and ship called from a process whose own python lacks the validator's packages
- **WHEN** ship runs the validator
- **THEN** it uses the first candidate interpreter (or `$SHIP_VALIDATOR_PYTHON`) that imports `jsonschema` and `pydantic`, not ship's own python

#### Scenario: A validator that cannot run is not reported as a failing package

- **GIVEN** a planning package, and either no interpreter that imports the validator's packages or a validator that dies on an import error
- **WHEN** ship runs
- **THEN** it exits 1 saying the validator could not run, not that the package is not compliant, does not rerun with `--no-freshness`, and the branch is not on the remote

### Requirement: Hold a new repository to a deployed plan

`scripts/ship.py` SHALL treat a repository as new when its earliest first commit
(`git log --max-parents=0 --format=%cI`) is dated on or after 2026-11-05. A new repository with no
planning package and no complete one-page plan SHALL be refused, naming the
company-planning:planning-compliance skill. A new repository with a package SHALL also be listed in
the plan list: the file `plan_list_path:` names on `origin/main` of the checkout `plan_list_checkout:` names
(Requirement: settings-come-from-config; fetched first, a failed fetch leaving the last fetched list), matched on the
repository name of its clone URL, so its review page deploys; if it is not listed, ship SHALL refuse
and print the exact line to add. When that list cannot be read, ship SHALL refuse and say why. Each
refusal names the rule.

Source: Brian, 2026-11-04, "well anytime i got ot work on a new project i want to enfroce that it first has company plans complaint plasn that are deployed for me to review. but i dotn want to actually do this for every proejct right now". This replaces the 2026-11-08 refusal date (Brian, 2026-10-25) and the quiet-repository package builder (Brian, 2026-10-27). Fetching the list first, so a line merged on GitHub counts, was inferred by agent. For small planned work the plan deployed for review is the one-page plan: Brian, 2026-11-15, "6 all" (decision record 0010).

#### Scenario: A new repository with no package is refused

- **GIVEN** a repository with no planning package and no one-page plan whose first commit is on 2026-11-05
- **WHEN** ship runs
- **THEN** it exits 1 before the check runs, names the planning-compliance skill, and the branch is not on the remote

#### Scenario: A new repository whose package is not on the plan list is refused

- **GIVEN** a new repository with a compliant package, and a plan list without it
- **WHEN** ship runs
- **THEN** it exits 1, prints the exact line to add, and the branch is not on the remote

#### Scenario: A new repository with a package on the plan list proceeds

- **GIVEN** a new repository with a package, listed on the remote's plan list after the local copy was last fetched
- **WHEN** ship runs with a passing check
- **THEN** it says the repository is on the plan list, and then the validator decides the merge

#### Scenario: An unreadable plan list refuses

- **GIVEN** a new repository with a compliant package, and a plan list that cannot be read
- **WHEN** ship runs
- **THEN** it exits 1, says it could not read the list, names the rule, and the branch is not on the remote

### Requirement: Refuse goals that do not name their sources

When ship extracts Company Planning's validator from company-planning's `origin/main`, `scripts/ship.py`
SHALL extract the validator's folder and, when `origin/main` has them,
`plugins/company-planning/scripts/goal_provenance.py` and `goal_provenance_prompt.yaml`, each at its path
in company-planning, so the validator runs the goal provenance check. When `origin/main` has neither, ship
SHALL extract the validator's folder alone, as before. After the validator runs, ship SHALL print and log
`ship: goal provenance: <ok|WAIT|FAIL> (required from <date>)` from the validator's goal provenance line,
so the date a waiting repository starts being refused is on screen. The validator's exit status still
decides the merge.

Source: Brian, 2026-11-06, "yes on d14" (prevention plan item 4: ship refuses on exit 1 where a goal page exists, with a dated 7-day grace for existing repositories). Incident: a Team-Brains goal cited "Tyler's Oct 16 ask", which nobody had read.

#### Scenario: The goal provenance check is extracted beside the validator

- **GIVEN** company-planning's origin/main with the validator folder and `goal_provenance.py`
- **WHEN** ship runs the planning gate
- **THEN** the validator finds `goal_provenance.py` at `../../../scripts/` from its own folder, ship prints `ship: goal provenance: WAIT (required from 2026-11-13)`, and the merge proceeds

#### Scenario: A goal provenance failure refuses the merge

- **GIVEN** company-planning's origin/main whose validator fails goal provenance (exit 1)
- **WHEN** ship runs the planning gate
- **THEN** it prints `ship: goal provenance: FAIL`, exits 1, and the branch is not on the remote

#### Scenario: An older company-planning without the check still validates

- **GIVEN** company-planning's origin/main with the validator folder and no `goal_provenance.py`
- **WHEN** ship runs the planning gate
- **THEN** it extracts the validator folder alone and the validator's exit status decides the merge

### Requirement: An upkeep-only change is never refused

When the planning gate would refuse (no package, or a package the validator rejects), `scripts/ship.py`
SHALL still let the branch proceed when every file it changes since its merge base with the default branch
is upkeep: a planning or documentation file as in "A plan repair is never refused", a lock file (`uv.lock`,
`package-lock.json` and the like), or a file whose added lines equal its removed lines once model names (and,
in dependency manifests, version numbers) are masked, with at least one name or version really changed.
Ship SHALL print that the branch is upkeep only and how many files it changes. A branch that changes any
other file, or adds or deletes a file outside the documentation rule, SHALL be refused as before. The
classification is the one Company Planning's validator uses for package freshness.

Source: Brian, 2026-11-06, "i aprpove" (Decision 2: model-name, dependency-version and documentation updates are upkeep, not work; company-planning #258). Applying it to this gate is inferred by agent from the same rule, after the 2026-11-06 model sweep was refused in 23 repositories with no package.

#### Scenario: An upkeep-only branch merges without a package

- **GIVEN** a new repository with no planning package, and a branch that changes a model name in a code file and a lock file
- **WHEN** ship runs with a passing check
- **THEN** it says the branch is upkeep only (2 files), merges, and exits 0

#### Scenario: A behavior change beside a model update is still refused

- **GIVEN** a new repository with no planning package, and a branch that changes a model name and a timeout in the same file
- **WHEN** ship runs
- **THEN** it exits 1 naming the missing planning package, and the branch is not on the remote

### Requirement: A record-only change is never refused

`scripts/ship.py` SHALL treat a file under `cases/`, `results/` or `raw/` as upkeep for "An upkeep-only change is never refused", so a branch that only adds or changes a run's record (its case folder, result files, captured sources) merges without the planning package gate. A branch that also changes any file outside those folders, the documentation rule and the model/lock rule SHALL be refused as before. Ship's printed line SHALL name the record-only folders.

Source: Brian, 2026-11-10, "fix it: 1 to 4" (recommendation 1: a change confined to a case or result folder skips the planning-package gate; the package check runs when someone is replanning), after "ok so it seems like my whole system is messed up and jut causing endless paperowrk. how do we solve this across my proejcts". The folder names are inferred by agent from the observation-to-action-metamodel and vision layouts.

#### Scenario: A branch that only adds a case record merges without a package

- **GIVEN** a new repository with no planning package, and a branch that adds files only under `cases/x/`
- **WHEN** ship runs with a passing check
- **THEN** it says the branch is upkeep only, merges, and exits 0

#### Scenario: A code change beside a case record is still refused

- **GIVEN** the same repository and a branch that adds a case file and changes `src/app.py`
- **WHEN** ship runs
- **THEN** it exits 1 naming the missing planning package, and the branch is not on the remote

### Requirement: Merge with a method the repository allows

Before the check, `scripts/ship.py` SHALL read which merge methods the repository allows
(`gh repo view --json mergeCommitAllowed,rebaseMergeAllowed,squashMergeAllowed,viewerDefaultMergeMethod,defaultBranchRef`)
and whether its default branch requires linear history (branch protection `required_linear_history`
or an active ruleset rule of type `required_linear_history`); linear history rules out `merge`. It SHALL
merge with `--method` when that method is allowed, else with the repository's default method when
allowed, else with the first allowed of rebase, squash, merge, and SHALL print and log each
replacement of `--method`. When no method is allowed it SHALL stop with exit status 1 before the check
and push nothing. When the settings cannot be read it SHALL use `--method`, else `merge`, and say the
settings were unreadable (a branch that is not protected, or protection that cannot be read without
admin rights, is not a refusal).

Source: inferred by agent from BrianMills2718/code2-workspace#62 (Brian's issue, 2026-10-26: "ship should read the repo's merge settings / branch protection before checking and pick the allowed method"); the order of preference (default, then rebase, squash, merge) is the agent's.

#### Scenario: A repository that requires linear history is merged by rebase

- **GIVEN** a passing check on a repository whose default branch requires linear history and whose default method is merge
- **WHEN** ship runs without `--method`
- **THEN** it merges with `--rebase`, reads back MERGED and exits 0

#### Scenario: A merge method that the repository does not allow is replaced before the check

- **GIVEN** a repository whose default branch requires linear history
- **WHEN** ship runs with `--method merge`
- **THEN** it prints that merge is not allowed and rebase is used, merges with `--rebase` and exits 0

#### Scenario: An allowed method that was asked for is used

- **GIVEN** a repository that allows all three methods
- **WHEN** ship runs with `--method squash`
- **THEN** it merges with `--squash`

#### Scenario: A ruleset that requires linear history is honored too

- **GIVEN** a repository whose default branch has no protection but an active ruleset rule `required_linear_history`
- **WHEN** ship runs without `--method`
- **THEN** it merges with `--rebase`

#### Scenario: A repository that disables a method falls back to the allowed ones

- **GIVEN** a repository that disables merge commits and whose default method is merge
- **WHEN** ship runs without `--method`
- **THEN** it merges with `--rebase`

#### Scenario: A repository that allows no merge method stops before the check

- **GIVEN** a repository that requires linear history and disables rebase and squash merges
- **WHEN** ship runs
- **THEN** it exits 1 without running the check, and the branch is not on the remote

#### Scenario: The merge settings are read before the check

- **GIVEN** a check that exits 0 only when the repository's settings were already read
- **WHEN** ship runs
- **THEN** it exits 0

#### Scenario: Settings that cannot be read leave the method unchanged

- **GIVEN** a repository whose settings `gh repo view` cannot read
- **WHEN** ship runs with `--method squash`
- **THEN** it says the settings were unreadable, merges with `--squash` and exits 0

### Requirement: Limit how many checks run at once

`scripts/ship.py` SHALL take one of `$SHIP_CHECK_SLOTS` (default 3) machine-wide check slots before
it sets up the environment and runs the check, and SHALL hold it until the check ends. A slot is a
file lock under `$SHIP_STATE_DIR/check-slots`, so a run that dies frees it. A run that finds every
slot taken SHALL print which repositories hold them, wait up to `$SHIP_SLOT_WAIT` seconds (default
1800), and then stop with exit status 1 and nothing pushed. A slot count of 0 SHALL turn the limit
off. A run that skips its check because the tree already passed SHALL take no slot.

Source: Brian, 2026-11-09, "i approve decision 2 andanything else that makes this more efficent
gogin forward" (Decision 4, limit concurrent merge checks); the count of 3 and the 30-minute wait are
the agent's, from a machine at load 27 to 31 on 20 cores.

#### Scenario: Every slot taken and none freed stops the run with nothing pushed

- **GIVEN** every check slot is held by another run and the wait is one second
- **WHEN** ship runs
- **THEN** it says the slots are taken and by whom, exits 1 without running the check, and the branch is not on the remote

#### Scenario: A slot that frees lets the check run

- **GIVEN** every check slot is held and one is released while ship waits
- **WHEN** ship runs with a passing check
- **THEN** it prints that it waited, runs the check, merges and exits 0

#### Scenario: The slot is released after the check

- **GIVEN** one check slot and a passing check
- **WHEN** ship runs and finishes
- **THEN** the slot can be locked again by another process

### Requirement: Validate the planning package only when the merge changes plan content

Before running the validator, `scripts/ship.py` SHALL ask whether the merge (from the merge base with the
default branch to HEAD) changes plan content. Plan content SHALL be what the validator's freshness check counts,
read by calling the validator's own `freshness()` with the merge base as the reviewed revision, never a second
list in ship; a change to `docs/planning/planning-package.json` itself SHALL also count. When the merge changes
no plan content, ship SHALL not run the validator and SHALL print and log one line saying it skipped the
validator and why. When it changes plan content, ship SHALL validate as before. When the answer cannot be
had (no merge base, a validator without `freshness()`, an error), ship SHALL validate. Checking the merge base
for a plan repair SHALL always validate. The new-repository rules SHALL apply as before: a new repository with
no package is refused, and one with a package must be on the plan list.

Source: Brian, 2026-11-12, "i approve decision 4" (ship runs the planning check only on merges that change plan content), applying his rule of 2026-11-10 (core.md, "How to think"): a planning package "is reviewed once at adoption and rechecked only when the plan's own content changes, never because code was committed".

#### Scenario: A code-only merge skips the validator

- **GIVEN** a repository whose planning package the validator would reject, and a branch that changes only code
- **WHEN** ship runs with a passing check
- **THEN** it prints that it skipped the planning validator because the merge changes no plan content, does not run the validator, merges and exits 0

#### Scenario: A plan change is validated

- **GIVEN** a branch that changes a plan file or the planning package itself
- **WHEN** ship runs
- **THEN** it runs the validator, and refuses with nothing pushed when the validator rejects the package

#### Scenario: A validator without the freshness entry point validates every merge

- **GIVEN** a validator with no `freshness()` function and a branch that changes only code
- **WHEN** ship runs
- **THEN** it runs the validator as before

### Requirement: Answer the plan-content question for the push hook

`scripts/plan_content.py --repo R --base B --head H --validator V` SHALL answer whether the commits from B to H
change plan content, using the same function `ship` uses, so the push hook and `ship` decide alike. It SHALL exit
0 and print a line starting `skip:` when nothing changed, and exit 1 with a line starting `validate:` when plan
content changed or anything is uncertain: B is not a commit, H is not the checkout's HEAD, or the validator has
no `freshness()`.

Source: Brian, 2026-11-12, "i approve decision 4" (the planning check runs only when plan content changes); applied to the push hook by the coordinator's go-ahead on Decision 5 option A, 2026-11-12.

#### Scenario: The push hook asks the same question

- **GIVEN** a branch that changes only code, then the same branch with a plan file changed
- **WHEN** `plan_content.py` is asked from the merge base
- **THEN** it exits 0 with `skip:` for the first, and exits 1 with `validate:` for the second, for a head that is not HEAD, and for a base that is no commit

### Requirement: Check every one-page plan a merge adds or changes

A one-page plan is a `.md` file committed under `docs/plans/` that carries the line `Plan size: small`. Text
inside a fenced code block is a quotation, not the page's own: the marker line, the headings and the read line
count only outside code blocks. Before the planning gate and the check run, `scripts/ship.py` SHALL check every
one-page plan that the merge (from the merge base with the default branch to HEAD) adds, changes or renames,
whatever characters its file name holds; when no merge base is found it SHALL check every committed one-page
plan. A one-page plan is complete when it has the five headings `## Goal`, `## How Brian judges it`,
`## Cost and time`, `## Scoring fixed beforehand` and `## What already exists`, at most 150 lines, and a line
that starts `Independent read: <YYYY-MM-DD>, pass` with a real date; when the page has more than one line that
starts `Independent read:`, the last one counts. A page that starts with a byte-order mark or holds bytes that
are not UTF-8 SHALL be checked, not skipped. ship SHALL refuse the merge, with nothing pushed, when a page it
checked is not complete, naming the page, each thing it lacks and the rule; no exception for a plan repair or
an upkeep-only change SHALL let that page merge. For each complete page it SHALL print and log one line naming
it. Under this requirement ship SHALL not refuse a merge for a plan page that lacks the line
`Plan size: small`, for a one-page plan the merge does not touch, or for one the merge deletes.

Source: Brian, 2026-11-15, "6 all", accepting decision record 0010, whose table of changes says "`ship` checks every one-page plan a merge adds or changes (its five parts, its length, its recorded read)". The marker line, the heading names, the wording of the read line, and checking every page when there is no merge base were inferred by agent. Counting only committed pages, leaving out code blocks, counting the last read line, checking that the date is real, and not skipping a page for its name or encoding were inferred by agent from an independent read of the code on 2026-11-15, which found each as a way an incomplete page could merge or a complete repository be refused.

#### Scenario: A complete one-page plan merges

- **GIVEN** a branch that adds a one-page plan with its five headings, fewer than 150 lines and the line `Independent read: 2026-11-15, pass (...)`
- **WHEN** ship runs with a passing check
- **THEN** it prints a line naming the page as a complete one-page plan, merges and exits 0

#### Scenario: A one-page plan missing a part is refused

- **GIVEN** a branch that adds a one-page plan with no `## Cost and time` heading
- **WHEN** ship runs
- **THEN** it exits 1 before the check runs, names the page and the missing heading, and the branch is not on the remote

#### Scenario: A one-page plan over 150 lines is refused

- **GIVEN** a branch that adds a one-page plan of more than 150 lines
- **WHEN** ship runs
- **THEN** it exits 1 before the check runs, says the page has more than 150 lines, and the branch is not on the remote

#### Scenario: A one-page plan with no passing independent read is refused

- **GIVEN** a branch that adds a one-page plan whose `Independent read:` line is absent, or records a verdict other than pass
- **WHEN** ship runs
- **THEN** it exits 1 before the check runs, names the missing `Independent read:` line, and the branch is not on the remote

#### Scenario: A plan page that does not call itself small is not checked

- **GIVEN** a branch that adds a file under `docs/plans/` with none of the five headings and no line `Plan size: small`
- **WHEN** ship runs with a passing check in a repository whose planning package passes
- **THEN** it merges and exits 0

#### Scenario: A one-page plan the merge does not touch is not checked

- **GIVEN** an incomplete one-page plan already on the default branch, and a branch that changes only another file
- **WHEN** ship runs with a passing check in a repository whose planning package passes
- **THEN** it merges and exits 0

#### Scenario: A one-page plan the merge deletes is not checked

- **GIVEN** an incomplete one-page plan already on the default branch, and a branch that deletes it
- **WHEN** ship runs with a passing check in a repository whose planning package passes
- **THEN** it merges and exits 0 without naming the deleted page

#### Scenario: A format quoted in a code block is not a one-page plan

- **GIVEN** a branch that adds a page under `docs/plans/` whose only `Plan size: small` line is inside a fenced code block
- **WHEN** ship runs with a passing check in a repository whose planning package passes
- **THEN** it merges and exits 0 without naming that page

#### Scenario: A plan repair or an upkeep-only branch does not excuse an incomplete one-page plan

- **GIVEN** a new repository with no planning package, and a branch that changes only documentation, or only a model name, a lock file and documentation, and adds a one-page plan with no `## Cost and time` heading
- **WHEN** ship runs
- **THEN** it exits 1 before the check runs, names the page, and the branch is not on the remote

#### Scenario: With no merge base every committed one-page plan is checked

- **GIVEN** an incomplete one-page plan on the default branch, a branch that changes only another file, and a clone in which git finds no merge base
- **WHEN** ship runs
- **THEN** it exits 1 before the check runs, names the page, and the branch is not on the remote

### Requirement: settings-come-from-config

Where the plan list lives SHALL be read when it is needed: from `$SHIP_PERSONAL_VPS` and `$SHIP_PLAN_LIST`
when set, else from the top-level `plan_list_checkout:` and `plan_list_path:` keys of `graph-config.yaml`
beside the project graph (`$PROJECT_GRAPH`, default `~/code2/aes-config/PROJECT_GRAPH.json`). When either
is not named, a new repository with a package SHALL be refused with a message naming both keys; nothing is
pushed. No other run reads them.

Source: inferred by agent from the AES consolidation plan item 7 task: AES is public, so a person's repository names and paths are their configuration in their private settings repository, as for the project-graph machinery.

#### Scenario: A new repository with no plan list named is refused

- **GIVEN** a new repository with a package, and neither the environment nor `graph-config.yaml` naming the plan list
- **WHEN** ship runs
- **THEN** it exits 1, says no plan list is named and names `plan_list_checkout`, and the branch is not on the remote

#### Scenario: The plan list location is read from graph-config

- **GIVEN** `graph-config.yaml` naming `plan_list_checkout:` and `plan_list_path:`
- **WHEN** ship reads the settings
- **THEN** it returns those values, an environment variable wins over the file, and a key named nowhere is none

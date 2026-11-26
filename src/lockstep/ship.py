#!/usr/bin/env python3
"""Run a repository's check and merge its pull request only if the check passed.

Steps, each printing its exit status and time, stopping at the first that fails:
clean tree on a non-default branch; the one-page plans and the prior-art record of each OpenSpec change the
merge touches (Lockstep's prior_art.py, beside this module); the planning gate; the check (default `make check`), skipped when
this tree already passed the same check; the tree still clean and HEAD unchanged; push; open the pull request when the branch has none; merge pinned to the checked commit
(`gh pr merge --match-head-commit`); read the state back and require MERGED.
The merge method is chosen before the check, from what the repository allows: --method when allowed, else the
repository's default method when allowed, else the first allowed of rebase, squash, merge. Allowed means the
repository's settings enable it and, for `merge`, the default branch does not require linear history (branch
protection or a ruleset). A replaced --method is printed; a repository that allows none stops the run before the check.
Every run is appended to one log per day under $SHIP_LOG_DIR (default ~/code2/.ship-logs where ~/code2 exists, else
${XDG_STATE_HOME:-~/.local/state}/ship/logs).
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

Switches (2026-11-20): `ship_planning_gate: false` or `ship_one_page_plans: false` in `.copier-answers.yml` on the
default branch at origin turns that gate off for the repository; a missing file or key leaves it on. The prior-art
check has no switch. Hidden acceptance gate: after catching up and before the check, the newest run record
`lockstep accept check` wrote for this branch (spec plan-run) must show the hidden tests passed, nothing
uncommitted, and the HEAD being merged; with no record ship says so and goes on.

A check takes one of $SHIP_CHECK_SLOTS (default 3) machine-wide slots (flock files under $SHIP_STATE_DIR/check-slots),
so a dozen agents merging at once do not run a dozen suites on the 20 cores; a run that finds all slots taken says
who holds them and waits up to $SHIP_SLOT_WAIT seconds (default 1800), then stops with nothing pushed. 0 slots
turns the limit off.

Implements: ship/install-ship-as-a-command-from-the-public-repository
Implements: ship/merge-only-the-commit-whose-check-passed
Implements: ship/rebase-a-branch-that-is-behind-the-default-branch-before-checking-it
Implements: ship/refuse-a-new-repository-with-no-planning-package
Implements: ship/check-every-one-page-plan-a-merge-adds-or-changes
Implements: ship/add-on-gates-switch-off-from-the-copier-answers
Implements: ship/refuse-a-branch-whose-hidden-acceptance-run-failed-or-is-out-of-date
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
Implements: ship/regenerate-a-status-page-conflict-and-rerun-hidden-tests-after-ship-s-own-rebase

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:ship.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: ship/install-ship-as-a-command-from-the-public-repository, ship/merge-only-the-commit-whose-check-passed, ship/rebase-a-branch-that-is-behind-the-default-branch-before-checking-it, ship/refuse-a-new-repository-with-no-planning-package, ship/check-every-one-page-plan-a-merge-adds-or-changes, ship/add-on-gates-switch-off-from-the-copier-answers, ship/refuse-a-branch-whose-hidden-acceptance-run-failed-or-is-out-of-date, ship/a-plan-repair-is-never-refused, ship/an-upkeep-only-change-is-never-refused, ship/refuse-a-merge-whose-openspec-change-lacks-a-prior-art-record, ship/a-record-only-change-is-never-refused, ship/refuse-a-planning-package-the-validator-rejects, ship/hold-a-new-repository-to-a-deployed-plan, ship/prepare-a-fresh-worktree-s-environment-before-the-check, ship/skip-a-check-that-already-passed-on-the-same-tree, ship/keep-its-own-lane-when-the-caller-still-needs-it, ship/refuse-goals-that-do-not-name-their-sources, ship/merge-with-a-method-the-repository-allows, ship/limit-how-many-checks-run-at-once, ship/settings-come-from-config, ship/regenerate-a-status-page-conflict-and-rerun-hidden-tests-after-ship-s-own-rebase, ship/validate-the-planning-package-only-when-the-merge-changes-plan-content

### Requirement: Install ship as a command from the public repository

The package SHALL install a `ship` command (`lockstep.ship:main`), so `uvx --from git+https://github.com/BrianMills2718/agentic-engineering-system-canonical ship` runs it on any machine with `uv`, `git` and `gh`. The files `scripts/ship.py` and `scripts/lane_sweep.py` SHALL keep working as before, run as files or imported from `scripts/`, by loading the modules in `src/lockstep/`.

Source: Brian, 2026-11-20: "the whole thing should be configurable and shareable/protable". Inferred by agent (minimal core, section 7: "install from the public repo with `uvx`, like `lockstep` already is"): keeping the old paths, because `~/.local/bin/ship` and the daily refresh point at them.

#### Scenario: The command and the old file both run

- **GIVEN** the package installed, and the file `scripts/ship.py`
- **WHEN** `python -m lockstep.ship --help` and `python scripts/ship.py --help` run
- **THEN** both exit 0 and print ship's usage

#### Scenario: The old import path is the moved module

- **GIVEN** `scripts/` on the import path
- **WHEN** `import ship` runs
- **THEN** the module is `lockstep.ship`

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

### Requirement: Rebase a branch that is behind the default branch before checking it

After refusing a dirty tree and before the gates and the check, `scripts/ship.py` SHALL fetch `origin` and, when the default branch (`origin/HEAD`, else `origin/main`) is not an ancestor of HEAD and the branch is not on the remote, rebase the branch onto the default branch, then check and merge the rebased commit. A repository's `.gitattributes` merge drivers apply to this rebase, so a file marked `merge=union` keeps the lines both sides added. When the rebase stops on a conflict it SHALL abort the rebase, leave the branch at its earlier commit, refuse the merge with nothing pushed, and name the conflicting paths. When the branch is already on the remote, or the fetch fails, it SHALL print and log one line saying it did not rebase and why, and go on.

Source: inferred by agent (code2-workspace issue 472, 2026-11-17): two sessions adding a top entry to the same log file conflicted on GitHub's merge, which does not apply `.gitattributes` merge drivers; a local rebase does. A pushed branch is not rebased because that would need a force-push.

#### Scenario: A branch behind the default branch is rebased and merged

- **GIVEN** a branch whose default branch gained a commit touching another file after the branch was cut
- **WHEN** ship runs
- **THEN** it rebases the branch onto the default branch, merges the rebased commit, and exits 0

#### Scenario: Two top entries in a union log both survive

- **GIVEN** a log file marked `merge=union` in `.gitattributes`, and the default branch and the branch each added a different entry at its top
- **WHEN** ship runs
- **THEN** it merges, and the merged log holds both entries

#### Scenario: A conflicting rebase pushes nothing

- **GIVEN** a branch and its default branch that changed the same line of a file with no merge driver
- **WHEN** ship runs
- **THEN** it exits 1, names the file, the branch is at its earlier commit with no rebase in progress, and nothing is pushed

#### Scenario: A branch already on the remote is not rebased

- **GIVEN** a branch that is behind the default branch and was pushed earlier
- **WHEN** ship runs
- **THEN** it says it did not rebase because the branch is on the remote, and merges as before

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

### Requirement: Add-on gates switch off from the copier answers

`scripts/ship.py` SHALL read the keys `ship_planning_gate` and `ship_one_page_plans` from `.copier-answers.yml` on the default branch at `origin` (never from the branch being shipped, so a branch cannot turn its own gate off), reading each as a top-level `key: value` line. When a key's value is `false` (any letter case), ship SHALL skip that gate (the whole planning gate with its plan-repair and upkeep exceptions, or the one-page-plan check) and print and log `ship: planning gate: off (.copier-answers.yml ship_planning_gate: false)` or `ship: one-page plans: off (.copier-answers.yml ship_one_page_plans: false)`. A missing file, a missing key or any other value SHALL leave the gate on. The prior-art check is core and has no switch.

Source: Brian, 2026-11-20: "the whole thing should be configurable and shareable/protable. we shoudl start with the minimal core than add on other things as needed after the first minimal core milestone". The copier answers file as the one switch, and these two gates as add-ons, inferred by agent in docs/planning/minimal-core-2026-11-20.md sections 5 and 7.

#### Scenario: The planning gate is switched off

- **GIVEN** a new repository with no planning package whose `.copier-answers.yml` says `ship_planning_gate: false`
- **WHEN** ship runs with a passing check
- **THEN** it merges and prints `ship: planning gate: off (.copier-answers.yml ship_planning_gate: false)`

#### Scenario: The one-page-plan check is switched off

- **GIVEN** a branch adding an incomplete one-page plan, in a repository whose `.copier-answers.yml` says `ship_one_page_plans: false`
- **WHEN** ship runs with a passing check
- **THEN** it merges

#### Scenario: No answers file keeps every gate on

- **GIVEN** a new repository with no planning package and no `.copier-answers.yml` on the default branch, or one that only the branch being shipped adds
- **WHEN** ship runs
- **THEN** it is refused as before

### Requirement: Refuse a branch whose hidden acceptance run failed or is out of date

After it has caught up with the default branch and before it runs the check, `scripts/ship.py` SHALL read every readable `summary.json` under `${XDG_STATE_HOME:-~/.local/state}/lockstep-runs/<repository>/` (the main checkout's folder name) whose `branch` is the branch being shipped or whose `head` is a commit reachable from HEAD and not from the default branch; an unreadable one SHALL be skipped with a printed warning. When there is at least one, ship SHALL refuse the merge with nothing pushed, naming `lockstep accept check <change>` as the way to record a new run, unless the newest by run id has `accept.exit` 0, `uncommitted` 0, and `head` equal to HEAD as it will be merged (so a branch that was rebased must be checked again). With none, ship SHALL print and log `ship: no hidden-test run recorded for this branch` and go on; a run made by another user or under another `XDG_STATE_HOME` is not found, which this message makes visible.

Source: minimal-core-2026-11-20.md section 6 step 2, hidden tests "must pass before `ship`" (inferred by agent from the 2026-11-20 plan-fidelity test, where they were the check that measured success), under Brian, 2026-11-20: "the goal is to give a well specified plan to an agent on some proejct nad have it faithfulyy and successfully impelemnt it".

#### Scenario: A passing record at HEAD merges

- **GIVEN** a run record for the branch with `accept.exit` 0, `uncommitted` 0 and `head` equal to HEAD
- **WHEN** ship runs with a passing check
- **THEN** it merges

#### Scenario: A failing or out-of-date record is refused

- **GIVEN** a run record for the branch whose hidden tests failed or did not run, or whose `head` is another commit, or which counted uncommitted files
- **WHEN** ship runs
- **THEN** it exits 1, names `lockstep accept check`, and the branch is not on the remote

#### Scenario: No record goes on

- **GIVEN** no run record for the branch
- **WHEN** ship runs with a passing check
- **THEN** it merges and prints `ship: no hidden-test run recorded for this branch`

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

### Requirement: Refuse a merge whose OpenSpec change lacks a prior-art record

Before the planning gate and the check, `ship` SHALL run Lockstep's prior-art check (`src/lockstep/prior_art.py`, the file beside ship's own module) with `--repo` set to the repository and `--files` set to every file under `openspec/changes/` that the merge (from the merge base with the default branch to HEAD) adds or changes; when no merge base is found it SHALL run it without `--files`. When the merge adds or changes no file under `openspec/changes/` it SHALL run nothing and print and log one line saying so. It SHALL refuse the merge, with nothing pushed, when the check exits 1, showing what the check printed. When the check file is missing it SHALL refuse the merge and say to reinstall `ship`; when the check exits with any status other than 0 or 1 it SHALL refuse the merge, show the exit status and say this is not a verdict on the record. When the check exits 0 it SHALL print and log its summary line.

Source: Brian, 2026-11-17: "every cpaability/featuer shoul dhave a prior art search so that we are only buidling what we need to. that needs to be ienforced" (code2-workspace Policy `prior-art-per-feature`; issue 833, slice 1, names `ship` as the merge point). Inferred by agent: running nothing when no change is touched, and refusing when the check is missing or cannot run (the merge rules fail closed). Inferred by agent, 2026-11-20 (minimal core, section 7): the check ships inside the public package instead of being read from the private workspace checkout, so `ship` works on another machine.

#### Scenario: A change with no record is refused

- **GIVEN** a branch that adds an OpenSpec change whose prior-art check exits 1
- **WHEN** `ship` runs
- **THEN** it exits 1, the check does not run, nothing is pushed, and the output holds what the prior-art check printed

#### Scenario: A change with a record merges

- **GIVEN** a branch that adds an OpenSpec change whose prior-art check exits 0
- **WHEN** `ship` runs
- **THEN** it merges, the prior-art check was given `--files` naming the change's files, and its summary line is printed and logged

#### Scenario: A merge that touches no change runs nothing

- **GIVEN** a branch that changes no file under `openspec/changes/`
- **WHEN** `ship` runs
- **THEN** the prior-art check is not run, a line says no OpenSpec change is in the merge, and the merge proceeds

#### Scenario: A missing prior-art check refuses

- **GIVEN** a branch that adds an OpenSpec change, and no prior-art check beside ship's module
- **WHEN** `ship` runs
- **THEN** it exits 1 with nothing pushed and says to reinstall `ship`

#### Scenario: A prior-art check that cannot run refuses

- **GIVEN** a branch that adds an OpenSpec change whose prior-art check exits 2
- **WHEN** `ship` runs
- **THEN** it exits 1 with nothing pushed, and says the exit status and that this is not a verdict on the record

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

### Requirement: Regenerate a status-page conflict and rerun hidden tests after ship's own rebase

When the rebase in "Rebase a branch that is behind the default branch before checking it" stops and every conflicted
path is `docs/status.md`, `ship` SHALL take the default branch's copy, continue the rebase (a commit left empty is
dropped), run the regenerate command (`SHIP_REGENERATE`, default `uv run lockstep check project`) and commit the page
when it changed; when any other path conflicts it SHALL abort as that requirement says. When `ship` itself rebased
the branch and the newest hidden-test record passed at the head before that rebase, `ship` SHALL run the hidden tests
again (`SHIP_ACCEPT_RERUN`, default `uv run lockstep accept check <change> --run-dir <run folder>`) and judge the
rewritten record; a record out of date for any other reason SHALL still be refused.

Source: Brian, 2026-11-20: "the whole thing should be configurable and shareable/protable"; inferred by agent from the
2026-11-21 milestone run, where two plans merged one after the other each stopped on a `docs/status.md` conflict and
then on a hidden-test record made stale by the rebase.

#### Scenario: A conflict only in the status page is regenerated

- **GIVEN** a branch and its default branch that each rewrote `docs/status.md`, and nothing else in common
- **WHEN** ship runs
- **THEN** it rebases, the page holds the regenerate command's output, the branch keeps its other changes, and it merges

#### Scenario: Hidden tests run again after ship's own rebase

- **GIVEN** a passing hidden-test record at the branch head and a default branch that moved on
- **WHEN** ship rebases the branch
- **THEN** it runs the hidden tests again on the rebased commit and merges only when the new record passes

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

Tested by: tests/test_ship.py
[[[end]]]
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
from collections.abc import Callable

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


def default_log_dir(name: str) -> Path:
    """~/code2/.<name>-logs where the ~/code2 workspace exists (its scripts read it), else
    ${XDG_STATE_HOME:-~/.local/state}/<name>/logs, so another machine gets no ~/code2 folder."""
    workspace = Path.home() / "code2"
    if workspace.is_dir():
        return workspace / f".{name}-logs"
    return Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local" / "state") / name / "logs"
PRIOR_ART_RULE = "prior-art rule (every OpenSpec change that adds a requirement holds a decided prior-art.json; rules: lockstep/prior-art.schema.json)"
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

    def __init__(self, repo: Path, log_dir: Path | None = None):
        """Open the day's log (in log_dir when given, e.g. `lockstep plan check`'s own folder) and record the start."""
        self.repo = repo
        self.rebased_from: str | None = None  # the head before ship's own rebase, when it rebased
        log_dir = log_dir or Path(os.environ.get("SHIP_LOG_DIR") or default_log_dir("ship"))
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

    Requirement text (generated):
        ship/validate-the-planning-package-only-when-the-merge-changes-plan-content: Before running
            the validator, `scripts/ship.py` SHALL ask whether the merge (from the merge base with
            the default branch to HEAD) changes plan content. Plan content SHALL be what the
            validator's freshness check counts, read by calling the validator's own `freshness()`
            with the merge base as the reviewed revision, never a second list in ship; a change to
            `docs/planning/planning-package.json` itself SHALL also count. When the merge changes no
            plan content, ship SHALL not run the validator and SHALL print and log one line saying
            it skipped the validator and why. When it changes plan content, ship SHALL validate as
            before. When the answer cannot be had (no merge base, a validator without `freshness()`,
            an error), ship SHALL validate. Checking the merge base for a plan repair SHALL always
            validate. The new-repository rules SHALL apply as before: a new repository with no
            package is refused, and one with a package must be on the plan list.
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

    Requirement text (generated):
        ship/check-every-one-page-plan-a-merge-adds-or-changes: A one-page plan is a `.md` file
            committed under `docs/plans/` that carries the line `Plan size: small`. Text inside a
            fenced code block is a quotation, not the page's own: the marker line, the headings and
            the read line count only outside code blocks. Before the planning gate and the check
            run, `scripts/ship.py` SHALL check every one-page plan that the merge (from the merge
            base with the default branch to HEAD) adds, changes or renames, whatever characters its
            file name holds; when no merge base is found it SHALL check every committed one-page
            plan. A one-page plan is complete when it has the five headings `## Goal`, `## How Brian
            judges it`, `## Cost and time`, `## Scoring fixed beforehand` and `## What already
            exists`, at most 150 lines, and a line that starts `Independent read: <YYYY-MM-DD>,
            pass` with a real date; when the page has more than one line that starts `Independent
            read:`, the last one counts. A page that starts with a byte-order mark or holds bytes
            that are not UTF-8 SHALL be checked, not skipped. ship SHALL refuse the merge, with
            nothing pushed, when a page it checked is not complete, naming the page, each thing it
            lacks and the rule; no exception for a plan repair or an upkeep-only change SHALL let
            that page merge. For each complete page it SHALL print and log one line naming it. Under
            this requirement ship SHALL not refuse a merge for a plan page that lacks the line `Plan
            size: small`, for a one-page plan the merge does not touch, or for one the merge
            deletes.
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


# Lockstep's prior-art check, beside this module (ported from code2-workspace 2026-11-20 so ship needs no private checkout).
PRIOR_ART_CHECK = Path(__file__).resolve().with_name("prior_art.py")
# Fully generated by `lockstep check project`; a rebase conflict confined to these is settled by regenerating them.
GENERATED = ("docs/status.md", "docs/links.json")
REGENERATE = "uv run lockstep check project"             # override: SHIP_REGENERATE
ACCEPT_RERUN = "uv run lockstep accept check {change} --run-dir {run_dir}"  # override: SHIP_ACCEPT_RERUN
PRIOR_ART_PYTHON = ["uv", "run", "--no-project", "--with", "jsonschema", "python"]
CHANGES_DIR = "openspec/changes/"


def prior_art_refusal(run: Run, repo: Path) -> str | None:
    """Return why the prior-art rule stops the merge, or None when every change the merge touches passes.

    Runs Lockstep's prior-art check (prior_art.py beside this module) on the files under openspec/changes/ that the merge adds or changes
    (every unarchived change when there is no merge base). Anything other than exit 0 refuses: a check that is
    missing or cannot run is not taken as a pass.

    Implements: ship/refuse-a-merge-whose-openspec-change-lacks-a-prior-art-record

    Requirement text (generated):
        ship/refuse-a-merge-whose-openspec-change-lacks-a-prior-art-record: Before the planning gate
            and the check, `ship` SHALL run Lockstep's prior-art check (`src/lockstep/prior_art.py`,
            the file beside ship's own module) with `--repo` set to the repository and `--files` set
            to every file under `openspec/changes/` that the merge (from the merge base with the
            default branch to HEAD) adds or changes; when no merge base is found it SHALL run it
            without `--files`. When the merge adds or changes no file under `openspec/changes/` it
            SHALL run nothing and print and log one line saying so. It SHALL refuse the merge, with
            nothing pushed, when the check exits 1, showing what the check printed. When the check
            file is missing it SHALL refuse the merge and say to reinstall `ship`; when the check
            exits with any status other than 0 or 1 it SHALL refuse the merge, show the exit status
            and say this is not a verdict on the record. When the check exits 0 it SHALL print and
            log its summary line.
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
    script = PRIOR_ART_CHECK
    if not script.is_file():
        return (f"{PRIOR_ART_RULE}: the prior-art check {script} is missing, so this merge's OpenSpec changes cannot "
                "be checked; reinstall ship (uvx --from git+https://github.com/BrianMills2718/agentic-engineering-system-canonical "
                "ship, or pull the checkout it runs from) and ship again")
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


class _Unavailable(str):
    """A planning-gate refusal that is not a plan verdict (no validator to run); `warn` still refuses it."""


def planning_gate(run: Run, repo: Path, *, always_validate: bool = False) -> str | None:
    """Return why the planning rules stop the merge, or None when it may proceed.

    always_validate runs the validator even when the merge changes no plan content (the merge-base check of a plan repair).
    """
    first_day = first_commit_day(repo)
    if first_day is None:
        return _Unavailable(f"{NEW_RULE}: could not read this repository's first commit")
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
    from lockstep.plan_check import fetch_planning_validator  # here, not at the top: plan_check imports ship
    validator, refused = fetch_planning_validator(run)
    if validator is None:
        return _Unavailable(refused or "the planning validator could not be fetched")
    python = validator_python(run)
    if python is None:
        return _Unavailable(f"the planning validator could not run: none of {', '.join(' '.join(c) for c in VALIDATOR_PYTHONS)} "
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
        return _Unavailable(f"the planning validator could not run ({broken}). This is not a verdict on the planning "
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


ANSWERS = ".copier-answers.yml"


def addon_off_line(run: "Run", gate: str, key: str) -> None:
    line = f"ship: {gate}: off ({ANSWERS} {key}: false)"
    print(line)
    run.write(line)


def _gated(run: "Run", repo: Path, gate: str, key: str, answers_key: str, check: Callable[["Run", Path], str | None]) -> str | None:
    """Run and record one planning gate in its mode (lockstep.yaml `planning.<key>`, else the copier answers): its refusal."""
    from lockstep.checks.config import copier_answer_on, planning_setting
    from lockstep.checks.gate_records import record_gate_verdict
    mode, refused, outcome, line = planning_setting(repo, key), None, "off", ""
    if mode == "off":
        line = f"ship: {gate}: off (lockstep.yaml planning.{key}: off)"
    elif not copier_answer_on(repo, answers_key):
        addon_off_line(run, gate, answers_key)
        mode = f"off ({ANSWERS} {answers_key})"
    else:
        refused = check(run, repo)
        outcome = "pass" if not refused else "unavailable" if isinstance(refused, _Unavailable) else "warn" if mode == "warn" else "refuse"
        if outcome == "warn":
            line = f"ship: warning: {gate}: {refused}; not refused (lockstep.yaml planning.{key}: warn)"
    if line:
        print(line)
        run.write(line)
    record_gate_verdict(run.log, repo, gate, mode, outcome, refused, on_error=run.write)
    return refused if outcome in ("refuse", "unavailable") else None


def accept_refusal(run: "Run", repo: Path, branch: str) -> str | None:
    """Return why the newest hidden-test run recorded for this branch stops the merge, or None.

    Run records are the `summary.json` files `lockstep accept check` writes (spec plan-run) under
    ${XDG_STATE_HOME:-~/.local/state}/lockstep-runs/<main checkout folder name>/<run id>/. A record belongs to this
    branch when its `branch` is this branch's name or its `head` is a commit on this branch (reachable from HEAD,
    not from the default branch). The newest must show the hidden tests ran and passed, nothing uncommitted, and
    its head equal to HEAD as it will be merged.

    Implements: ship/refuse-a-branch-whose-hidden-acceptance-run-failed-or-is-out-of-date

    Requirement text (generated):
        ship/refuse-a-branch-whose-hidden-acceptance-run-failed-or-is-out-of-date: After it has
            caught up with the default branch and before it runs the check, `scripts/ship.py` SHALL
            read every readable `summary.json` under
            `${XDG_STATE_HOME:-~/.local/state}/lockstep-runs/<repository>/` (the main checkout's
            folder name) whose `branch` is the branch being shipped or whose `head` is a commit
            reachable from HEAD and not from the default branch; an unreadable one SHALL be skipped
            with a printed warning. When there is at least one, ship SHALL refuse the merge with
            nothing pushed, naming `lockstep accept check <change>` as the way to record a new run,
            unless the newest by run id has `accept.exit` 0, `uncommitted` 0, and `head` equal to
            HEAD as it will be merged (so a branch that was rebased must be checked again). With
            none, ship SHALL print and log `ship: no hidden-test run recorded for this branch` and
            go on; a run made by another user or under another `XDG_STATE_HOME` is not found, which
            this message makes visible.
    """
    common = Path(git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir"))
    state = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")
    root = Path(state) / "lockstep-runs" / common.parent.name
    head = git(repo, "rev-parse", "HEAD")
    base = merge_base(repo)
    on_branch = set(subprocess.run(["git", "-C", str(repo), "rev-list", f"{base}..HEAD" if base else "HEAD"],
                                   capture_output=True, text=True).stdout.split())
    records = []
    for path in sorted(root.glob("*/summary.json")) if root.is_dir() else []:
        try:
            rec = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            line = f"ship: warning: skipped an unreadable run record {path}"
            print(line)
            run.write(line)
            continue
        if isinstance(rec, dict) and (rec.get("branch") == branch or rec.get("head") in on_branch
                                     or (run.rebased_from and rec.get("head") == run.rebased_from)):
            records.append((str(rec.get("run_id") or path.parent.name), rec, path.parent))
    if not records:
        line = "ship: no hidden-test run recorded for this branch"
        print(line)
        run.write(line)
        return None
    run_id, rec, run_dir = max(records, key=lambda item: item[0])
    accept = rec.get("accept") or {}
    if (run.rebased_from and rec.get("head") == run.rebased_from and rec.get("head") != head
            and accept.get("exit") == 0 and not rec.get("uncommitted")):
        # ship's own rebase moved the branch past a passing run: run the hidden tests again on the rebased commit.
        line = f"ship: rebased past run {run_id}; running the hidden tests again at {head[:12]}"
        print(line)
        run.write(line)
        command = ((os.environ.get("SHIP_ACCEPT_RERUN") or ACCEPT_RERUN)
                   .replace("{change}", shlex.quote(str(rec.get("change", ""))))
                   .replace("{run_dir}", shlex.quote(str(run_dir))))
        run.step("hidden tests again", command, shell=True)
        try:
            rec = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return f"the hidden-test rerun left no readable record in {run_dir}; run `lockstep accept check` in this worktree"
        accept = rec.get("accept") or {}
    again = f"run `lockstep accept check {rec.get('change', '<change>')}` in this worktree to record a new run"
    if accept.get("exit") != 0:
        return f"hidden acceptance tests did not pass in run {run_id} ({accept or 'no hidden test ran'}); fix the code, then {again}"
    if rec.get("uncommitted"):
        return f"run {run_id} counted {rec['uncommitted']} uncommitted file(s); commit them, then {again}"
    if rec.get("head") != head:
        return (f"run {run_id} checked {str(rec.get('head'))[:12]}, but the branch is now at {head[:12]} "
                f"(new commits or a rebase); {again}")
    line = f"ship: hidden tests passed in run {run_id} at {head[:12]} ({accept.get('passed')} passed)"
    print(line)
    run.write(line)
    return None


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
    removed: list[str] = []
    added: list[str] = []
    raw: list[str] = []
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


def regenerate(run: Run, repo: Path, note: Callable[[str], None]) -> str | None:
    """After a rebase that took the default branch's generated pages, rebuild them and commit any change.

    Implements: ship/regenerate-a-status-page-conflict-and-rerun-hidden-tests-after-ship-s-own-rebase

    Requirement text (generated):
        ship/regenerate-a-status-page-conflict-and-rerun-hidden-tests-after-ship-s-own-rebase: When
            the rebase in "Rebase a branch that is behind the default branch before checking it"
            stops and every conflicted path is `docs/status.md`, `ship` SHALL take the default
            branch's copy, continue the rebase (a commit left empty is dropped), run the regenerate
            command (`SHIP_REGENERATE`, default `uv run lockstep check project`) and commit the page
            when it changed; when any other path conflicts it SHALL abort as that requirement says.
            When `ship` itself rebased the branch and the newest hidden-test record passed at the
            head before that rebase, `ship` SHALL run the hidden tests again (`SHIP_ACCEPT_RERUN`,
            default `uv run lockstep accept check <change> --run-dir <run folder>`) and judge the
            rewritten record; a record out of date for any other reason SHALL still be refused.
    """
    command = os.environ.get("SHIP_REGENERATE") or REGENERATE
    pages = ", ".join(GENERATED)
    if run.step("regenerate the generated pages", command, shell=True).returncode != 0:
        return f"the rebase took the default branch's {pages}, but `{command}` failed; run it, commit, then ship again"
    others = [line[3:] for line in subprocess.run(["git", "-C", str(repo), "status", "--porcelain"],
                                                  capture_output=True, text=True).stdout.splitlines()
              if line[3:] not in GENERATED]
    if others:
        return (f"`{command}` also changed {', '.join(others)}; review and commit them, then ship again")
    changed = [line[3:] for line in subprocess.run(["git", "-C", str(repo), "status", "--porcelain", "--", *GENERATED],
                                                   capture_output=True, text=True).stdout.splitlines()]
    if not changed:
        note(f"regenerated {pages}: unchanged")
        return None
    # Only the pages that changed: a repository may not produce every generated page, and git add refuses a missing path.
    run.step("stage the generated pages", ["git", "-C", str(repo), "add", "--", *changed])
    done = run.step("commit the generated pages", ["git", "-C", str(repo), "commit", "-q", "--no-verify", "-m",
                                                   f"Regenerate {pages} after rebasing (ship)"])
    if done.returncode != 0:
        return f"regenerated {pages} but could not commit it; commit it, then ship again"
    note(f"regenerated {pages} and committed it")
    return None


def catch_up(run: Run, repo: Path, branch: str) -> str | None:
    """Rebase an unpushed branch onto the default branch when it is behind; return why it cannot, or None.

    GitHub's merge ignores `.gitattributes` merge drivers, so two branches that each add a top entry to one log
    file conflict there; a local rebase applies `merge=union` and keeps both (code2-workspace issue 472).
    """
    def note(text: str) -> None:
        print(f"ship: {text}")
        run.write(f"ship: {text}")
    if run.step("fetch origin", ["git", "-C", str(repo), "fetch", "-q", "origin"]).returncode != 0:
        note("not rebased: the fetch failed, so the branch is merged as it is")
        return None
    head_ref = subprocess.run(["git", "-C", str(repo), "symbolic-ref", "-q", "--short", "refs/remotes/origin/HEAD"],
                              capture_output=True, text=True)
    default = head_ref.stdout.strip() if head_ref.returncode == 0 and head_ref.stdout.strip() else "origin/main"
    behind = subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", default, "HEAD"],
                            capture_output=True, text=True)
    if behind.returncode == 0:
        return None
    if behind.returncode != 1:
        note(f"not rebased: git cannot compare the branch with {default}")
        return None
    pushed = subprocess.run(["git", "-C", str(repo), "ls-remote", "--exit-code", "--heads", "origin", branch],
                            capture_output=True, text=True)
    if pushed.returncode == 0:
        note(f"not rebased onto {default}: {branch} is already on the remote and rebasing it would need a force-push")
        return None
    before = git(repo, "rev-parse", "HEAD")
    rebased = run.step(f"rebase onto {default}", ["git", "-C", str(repo), "rebase", "-q", default])
    settled = False
    conflicts: list[str] = []
    for _ in range(100):  # one stop per replayed commit at most
        if rebased.returncode == 0:
            break
        conflicts = subprocess.run(["git", "-C", str(repo), "diff", "--name-only", "--diff-filter=U"],
                                   capture_output=True, text=True).stdout.split()
        if not conflicts or any(path not in GENERATED for path in conflicts):
            break
        # Take the default branch's copy; the page is regenerated once the rebase is done.
        took = run.step(f"take {default}'s {', '.join(conflicts)}",
                        ["git", "-C", str(repo), "checkout", "--ours", "--", *conflicts])
        if took.returncode != 0 or run.step("stage it", ["git", "-C", str(repo), "add", "--", *conflicts]).returncode != 0:
            break
        rebased = run.step("continue the rebase",
                           ["git", "-C", str(repo), "-c", "core.editor=true", "rebase", "--continue"])
        settled = True
    if rebased.returncode == 0:
        run.rebased_from = before
        note(f"rebased onto {default} ({git(repo, 'rev-parse', '--short', default)})")
        return regenerate(run, repo, note) if settled else None
    run.step("abort the rebase", ["git", "-C", str(repo), "rebase", "--abort"])
    return (f"{branch} conflicts with {default} in: {', '.join(conflicts) or 'paths git did not name'}; the branch is "
            f"unchanged. Rebase it onto {default} and resolve these (a log file may take `merge=union` in "
            ".gitattributes), then ship again")


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
    behind = catch_up(run, repo, branch)
    if behind:
        return run.fail(f"{behind}; nothing was pushed")
    head = git(repo, "rev-parse", "HEAD")
    hidden = accept_refusal(run, repo, branch)
    if hidden:
        return run.fail(f"{hidden}; nothing was pushed")
    from lockstep.checks.config import ConfigError
    try:
        incomplete = _gated(run, repo, "one-page plans", "one_page_plans", "ship_one_page_plans", one_page_plan_refusal)
        if incomplete:
            return run.fail(f"{incomplete}; nothing was pushed")
        no_record = prior_art_refusal(run, repo)
        if no_record:
            return run.fail(f"{no_record}\nnothing was pushed")
        refused = _gated(run, repo, "planning gate", "gate", "ship_planning_gate", planning_gate)
    except ConfigError as exc:
        return run.fail(f"{exc}; nothing was pushed")
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

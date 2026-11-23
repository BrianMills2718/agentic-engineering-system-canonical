# portable-template Specification

## Purpose

This repository holds the starter template. A repository made from it works for anyone with the defaults (no private hooks remote, owner identity or home-folder paths), and keeps the shared code2 hooks and rules when it belongs to Brian's workspace.

## Requirements

### Requirement: A repository made with the defaults works for anyone

A repository made with `copier copy --defaults` SHALL have a `lefthook.yml` with no `remotes:` block, whose pre-commit jobs refuse a staged `.env` file and run `gitleaks` on the staged changes; an `AGENTS.md`, `pyproject.toml` and `lefthook.yml` that name no home-folder path (`~/`), SSH alias, person or e-mail address of the template's owner, other than the public URL Lockstep installs from; no `authors` line when `author` is empty; no local git `user.name` or `user.email` unless `git_user_name` and `git_user_email` were answered; and `.copier-answers.yml` with `code2_workspace: false`, `ship_planning_gate: false` and `ship_one_page_plans: false`. Its `make check` SHALL exit 0.

Source: Brian, 2026-11-20: "the whole thing should be configurable and shareable/protable. we shoudl start with the minimal core than add on other things as needed after the first minimal core milestone". The specific blockers and defaults inferred by agent from a fresh copy on 2026-11-20 (agentic-engineering-system-canonical docs/planning/minimal-core-2026-11-20.md section 7).

#### Scenario: Default copy has no machine-bound parts

- **GIVEN** the template rendered with `--defaults`, a project name and a description
- **WHEN** its files are read
- **THEN** `lefthook.yml` has no `remotes:` and has the jobs `no-env-file` and `secrets-staged`, `AGENTS.md`, `pyproject.toml` and `lefthook.yml` contain no `~/`, `github-personal`, `Brian` (outside the Lockstep URL) or e-mail address, the local git config has no `user.name`, the answers file has the three `false` answers, and `make check` exits 0

### Requirement: A workspace repository keeps the shared hooks

With `code2_workspace: true`, the template SHALL write today's `lefthook.yml` (the `code2-workspace` remote with `hooks/base.yml`) an `AGENTS.md` that links the workspace rules, and set the local git identity to Brian's GitHub name and no-reply address unless other values are answered.

Source: inferred by agent: Brian's own repositories keep the shared hooks and rules they use today (code2-workspace AGENTS.md, "Checks").

#### Scenario: Workspace copy keeps the remote

- **GIVEN** the template rendered with `code2_workspace=true`
- **WHEN** `lefthook.yml` and `AGENTS.md` are read
- **THEN** `lefthook.yml` names the `code2-workspace` remote and `hooks/base.yml`, `AGENTS.md` links `~/code2/AGENTS.md`, and a commit succeeds on a machine with no global git identity

### Requirement: Make a repository from this repository

This repository SHALL hold the template, so `copier copy --trust gh:BrianMills2718/agentic-engineering-system-canonical <dir>` makes a repository: `copier.yml` at the root with `_subdirectory: template`, and the README naming that command.

Source: Brian, 2026-11-21: "i thoguht as canoncial was one repo that contained all this stuff?", then "yes" to moving code2-template into this repository (session 5651a525).

#### Scenario: The template is served from here

- **GIVEN** this repository
- **WHEN** `copier.yml` and `README.md` are read
- **THEN** `copier.yml` sets `_subdirectory: template` and names `gh:BrianMills2718/agentic-engineering-system-canonical`, and the README gives the `copier copy` command with that address

### Requirement: A copy runs its commit checks after a move and in every worktree

A repository made from the template SHALL hold tracked, executable `.githooks/pre-commit` and `.githooks/pre-push`
scripts that each run `lefthook run` for their hook and name no machine path, and the copier tasks SHALL set the local
`core.hooksPath` to the relative path `.githooks`, so a commit in a moved copy or in any worktree runs the
`lefthook.yml` jobs.

Source: Brian, 2026-11-20: "the whole thing should be configurable and shareable/protable"; inferred by agent from the
2026-11-21 milestone run, where a moved copy committed with no hooks because `core.hooksPath` held an absolute path.

#### Scenario: A moved copy and a worktree still run the hooks

- **GIVEN** a rendered copy with `core.hooksPath` set as the copier task sets it and a `lefthook.yml` job that prints a marker
- **WHEN** the copy's folder is moved and a commit is made there, and a commit is made in a new worktree of it
- **THEN** both commits print the marker, and the hook scripts contain no home-folder path

### Requirement: The commit check stages rewritten files that git tracks

The `lockstep-fast` pre-commit job of a copy SHALL stage each file `lockstep check project` reports as rewritten,
except a file git ignores, and SHALL then run `make fast`. An ignored rewritten file SHALL NOT make the commit fail.

#### Scenario: An ignored status page does not block a commit

- **GIVEN** a copy whose `.gitignore` lists `docs/status.md`
- **WHEN** the job runs and `lockstep check project` reports `rewrote docs/status.md` and `rewrote src/demo/a.py`
- **THEN** the job exits 0, `src/demo/a.py` is staged and `docs/status.md` is not

### Requirement: A copy hands an editing agent the requirement text

A repository made from the template SHALL include `.claude/settings.json` and `.codex/hooks.json` whose PreToolUse hooks run `uv run lockstep-hook` (the copy's own locked Lockstep) on file edits and shell commands, without `PCW_MODE=block`, and SHALL git-ignore `docs/links.json`.

Source: Brian, 2026-11-23: "isnt this the whole thing that makes the whle systme work?"; AES docs/architecture/GOAL.md:88; plan docs/planning/linked-chain-core-2026-11-23.md

#### Scenario: A rendered copy has both hook files

- **GIVEN** the template rendered with its defaults
- **WHEN** its `.claude/settings.json` and `.codex/hooks.json` are read
- **THEN** each runs `uv run lockstep-hook` on edits, neither sets `PCW_MODE=block`, and `.gitignore` lists `docs/links.json`

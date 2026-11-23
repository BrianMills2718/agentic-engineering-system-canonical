## ADDED Requirements

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

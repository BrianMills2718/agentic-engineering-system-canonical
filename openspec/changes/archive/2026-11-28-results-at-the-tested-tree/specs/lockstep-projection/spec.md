## MODIFIED Requirements

### Requirement: Status reads test results from this revision

`lockstep status` SHALL mark a scenario passing, failing or skipped only from a test-result file recorded at the current commit with a clean tree, or recorded on working files whose git tree equals the current commit's tree when nothing is uncommitted now, and SHALL mark it `not run at this revision` otherwise. `make check` SHALL record that git tree in `.code2check/run.json` as `tree`, through `lockstep record-tree`, after its last step that rewrites files and also when a test fails: the tree of the tracked files and the untracked files git does not ignore, as they are on disk, built in a temporary index so that the repository's own index is not changed.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows). Brian, 2026-11-27 18:50: "Pass or fail only appears after make check on that exact commit, and it isn't written back into this page". The tree rule is inferred by agent from the 2026-11-28 isolated Haiku run on a fresh copy (commit 1fcf203), which ran `make check`, committed exactly what it tested, and was told its results were recorded with uncommitted changes.

#### Scenario: Results from this revision set pass and fail

- **GIVEN** results recorded at HEAD on a clean tree
- **WHEN** `lockstep status` runs
- **THEN** scenarios are passing or failing as recorded

#### Scenario: Results from another revision are not used

- **GIVEN** results recorded at an older commit
- **WHEN** `lockstep status` runs
- **THEN** scenarios are `not run at this revision`

#### Scenario: Results tested on the files that were then committed are used

- **GIVEN** results recorded with uncommitted changes, with the tree of those working files, and those files then committed unchanged
- **WHEN** `lockstep status` runs
- **THEN** scenarios are passing or failing as recorded, and the note says the tested tree matches the commit
- **AND** after one more edit to a tracked file, scenarios are `not run at this revision`

#### Scenario: Recording the tested tree leaves the index alone

- **GIVEN** a repository with a staged change, an unstaged change and a new untracked file
- **WHEN** `lockstep record-tree` runs
- **THEN** `.code2check/run.json` keeps its `commit` and `clean` and gains `tree`, which equals the tree of a commit of all three files, and `git diff --cached` is the same as before

## ADDED Requirements

### Requirement: A fresh copy rewrites its results page after each commit

A fresh copy of the template SHALL run `lockstep check project` from a tracked `post-commit` hook (`.githooks/post-commit`, a lefthook `post-commit` job), so that its git-ignored `generated/wiki/results.md` gives pass or fail for the new commit when the commit holds the files `make check` tested.

Source: Brian, 2026-11-27 18:50: "Pass or fail only appears after make check on that exact commit, and it isn't written back into this page". Running it from a post-commit hook is inferred by agent: the pre-commit hook runs before the commit exists, so it cannot name it.

#### Scenario: A commit in a fresh copy rewrites the results page

- **GIVEN** a fresh copy of the template
- **WHEN** its hooks are read
- **THEN** `.githooks/post-commit` is executable and runs lefthook's `post-commit` jobs, and `lefthook.yml` has a `post-commit` job that runs `lockstep check project`

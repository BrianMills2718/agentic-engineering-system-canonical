## ADDED Requirements

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

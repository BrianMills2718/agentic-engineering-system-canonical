# ship settles a status-page conflict and re-runs hidden tests after its own rebase

Plan size: small

## Why

In the minimal-core milestone run (2026-11-21), each of the two plans that merged one after the other stopped `ship`
twice. First, its rebase conflicted in `docs/status.md`, a page `lockstep check project` writes in full. Then, after
the person rebased and regenerated the page by hand, `ship` refused the hidden-test record because the rebase had
changed the head (`/home/brian/projects/data/lockstep-milestone/NOTES.md`, "2026-11-21 run"; ship log 2026-11-21:
"conflicts with origin/main in: docs/status.md").

## What changes

- When every conflicted path in ship's own rebase is `docs/status.md`, ship takes the default branch's copy, finishes
  the rebase, runs `uv run lockstep check project` (`SHIP_REGENERATE`) and commits the page if it changed. Any other
  conflicted path aborts the rebase exactly as before.
- When ship's own rebase moved the branch past a passing hidden-test record, ship runs
  `uv run lockstep accept check <change> --run-dir <run>` (`SHIP_ACCEPT_RERUN`) and judges the new record. A record
  out of date for any other reason is refused as before.
- `docs/index.md` (its spec list comes from a repository's own `make docs-specs`) stays out: the page also holds
  hand-written text, so taking one side could drop a person's edit.

Source: Brian, 2026-11-20: "the whole thing should be configurable and shareable/protable"; the fix inferred by agent
from the milestone run above.

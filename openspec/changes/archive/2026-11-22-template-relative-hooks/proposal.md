# A copy keeps its commit checks when it is moved

Plan size: small

## Why

The template's copier task sets `core.hooksPath` to the absolute path of the copy's `.git/hooks`. After the folder is
moved, git looks for hooks at the old path, finds nothing and runs no commit check at all, without any message. This
happened in the minimal-core milestone run on 2026-11-21: the first Claude run committed with no hooks after the copy
was moved (`/home/brian/projects/data/lockstep-milestone/NOTES.md`, "More findings").

## What changes

- The template ships `.githooks/pre-commit` and `.githooks/pre-push`, tracked and executable, each one line:
  `exec lefthook run <hook> "$@"`.
- The copier task sets `core.hooksPath .githooks` (relative to the working tree, so every worktree and a moved copy
  find the same tracked scripts) and no longer runs `lefthook install --force`.
- Copies made before this keep their absolute path; `copier update` or `git config core.hooksPath .githooks` with
  the two files fixes one.

Source: Brian, 2026-11-20: "the whole thing should be configurable and shareable/protable"; the fix inferred by agent
from the milestone finding above.

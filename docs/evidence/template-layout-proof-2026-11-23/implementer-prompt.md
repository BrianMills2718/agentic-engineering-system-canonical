You are in a git worktree on a new branch. Implement the plan in openspec/changes/add-greeting/ exactly as written.

1. Read proposal.md, the spec delta under specs/, and tasks.md. Read AGENTS.md and the AGENTS.md of each folder you edit.
   When lockstep.yaml has `layout:` rows, they are part of the plan: each names a file to create or change, the
   requirements it implements, its tests and its public functions (`exports`). Run `uv run lockstep layout` before
   writing code; it creates each new planned file with its requirement text.
2. Do the tasks in order. Write each task's test first and see it fail, then make it pass. Tick each task (`- [x]`) when done.
3. When all tasks are done, archive the change: `openspec archive add-greeting --yes`.
4. Run `make check` until it exits 0.
5. Commit with plain `git commit`. If a hook refuses, do what its message asks; do not bypass it.

Stay inside the plan. Do not change files the tasks do not name unless the plan cannot work without it; if you do, or
skip, change or reorder a task, record it as a departure. No paid model or provider calls. Do not push, merge or deploy.
If the plan needs a decision only the repository owner can make, stop and say so.

At the end report: Commits (id and message); Departures (every changed file not named in tasks.md, every task
skipped, changed or reordered, with the reason, or "none"); check result and exit status; every hook refusal, quoted.

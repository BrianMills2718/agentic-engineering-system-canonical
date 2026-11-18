## Why

Brian, 2026-11-17: "i approve your reccomendations", answering Decision 7 (how much of the planning checklist a requirement change must pass) with its option 7A: "Each plan states its size in one line, small or full. Small: the proposal is the plan, Lockstep's checks are the gate, and the checklist is not run. Full: the whole planning package and checklist, as now. Lockstep prints and counts the declared sizes."

The decision came from one real requirement change taken through the flow on 2026-11-17 (code2-workspace `docs/analysis/flow-first-run-2026-11-17.md`): the change took 3 minutes 25 seconds from worktree to committed fix (measured from file and commit times), and the 18-item planning checklist, read against it, passed 13 items and did not pass 5. Nothing in a plan said which of the two paths it was on, so no program could tell a small change that skipped the checklist on purpose from a large one that skipped it by mistake.

## What Changes

- `lockstep check changed` reads the line `Plan size: small` or `Plan size: full` in every plan that names a listed requirement: the `proposal.md` of an OpenSpec change, or a page in `docs/plans/`. A line inside a fenced code block does not count.
- A listed requirement that a plan names, with no size in any plan naming it, fails with `no-plan-size`; the finding names the file to add the line to.
- A requirement whose size is `full` fails with `no-planning-package` unless a plan naming it has a line `Planning package: <path>` naming a file that exists.
- A requirement named `small` by one plan and `full` by another is `full`.
- The text block of each listed requirement gains a `size` line, the JSON a `size` field, and the count line four fields: `small`, `full`, `no_plan_size`, `no_planning_package`.

The size is the author's declaration. The check does not test whether a change deserves the size it states; it makes the statement required, visible and counted. When a plan may call itself small is a rule for agents, in code2-workspace `agents/topics/working-method.md`, "Plan size".

## Impact

- `src/lockstep/checks/changed.py` and `src/lockstep/checks/cli.py`.
- Every repository that runs `lockstep check changed` and takes this revision: a branch whose OpenSpec change or plan page has no `Plan size:` line fails the check until the line is added. On 2026-11-18 one repository runs the check: code2-workspace (measured: of the 113 Makefiles one level under `~/code2`, 39 mention Lockstep and one has `check changed`). Its pin moves in a following change by the same session.
- `ship` is unchanged: it goes on reading `Plan size: small` in `docs/plans/` pages and checking such a page's five parts, length and independent read. It reads no `proposal.md`.

Plan size: small

Closes: lockstep-checks/changed-every-plan-that-names-a-listed-requirement-states-its-size,
    lockstep-checks/changed-count-line-and-exit-status

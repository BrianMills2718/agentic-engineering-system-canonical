---
description: Goal after the first minimal-core milestone -- a second user runs the core with nothing of Brian's, agents included
---

# Goal: a second user runs the minimal core with nothing of Brian's

Planning package: exempt -- one clean-home test run plus the small fixes it finds; each fix that changes required
behaviour goes through its own OpenSpec change with `Plan size: small` and `ship`.

**Execution profile:** continuous-light

Source: Brian, 2026-11-20: "the whole thing should be configurable and
shareable/protable. we shoudl start with the minimal core than add on other things as needed after the first
minimal core milestone."

## Mission and canonical example

The first milestone ([minimal-core-2026-11-20.md](minimal-core-2026-11-20.md), section 8) was met with one stated
compromise: the Claude and Codex agents used Brian's own login folders, so they read his global agent instructions
(`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`). This goal removes it, and checks the template's own `AGENTS.md` is
enough (section 7, row "core.md and topic files use home-directory paths").

Canonical example: in the clean home folder (`/home/brian/projects/data/lockstep-milestone/home`, run with
`env -i HOME=... PATH=<home>/bin:/usr/local/bin:/usr/bin:/bin`), with agent config folders that hold no global
instructions:

```text
uvx copier copy --trust --defaults --data project_name=second-user --data description=... \
  gh:BrianMills2718/agentic-engineering-system-canonical second-user
# one small OpenSpec plan per agent, merged first with `uv run ship`
uv run lockstep run-plan <change-a> --agent claude   -> hidden tests fail before, pass after; departure report
uv run lockstep run-plan <change-b> --agent codex    -> same
cd <printed worktree> && uv run ship                 -> "hidden tests passed", merged
```

Forbidden substitutes: a run whose agent config folder holds a `CLAUDE.md` or `AGENTS.md` of Brian's, or that is
pointed at `/home/brian/.claude` or `/home/brian/.codex`; tests written by the implementer; a merge without `ship`;
a copy from `code2-template` or a local path instead of the public address.

## Boundaries

- In scope: the run above, and fixes in agentic-engineering-system-canonical (template, Lockstep, `ship`) for what
  it finds. Out of scope: add-ons (section 5), code2-template, Brian's own repositories.
- Never copy or print a login file or key (Safety Net refused copying `~/.claude/.credentials.json` on 2026-11-21:
  "Do not retry this operation or attempt any workaround"). An agent login in a fresh config folder is Brian's step.

## Increments

1. Fresh agent config folders under the clean home with no instruction files; Brian logs both agents in once.
2. Copy from the public address; two plans; both `run-plan` runs; both merges.
3. Fix each friction found at its source (template or Lockstep), through `ship`.
4. Record the result in section 8 of the minimal-core plan and in `.project-brain/now.md`, through `ship`.

## Checks

- Before each run: `ls <config folder>` shows no `CLAUDE.md` / `AGENTS.md`; the agent's transcript (kept by
  `run-plan` under `~/.local/state/lockstep-runs/<repo>/<run id>/` in the clean home) shows no read of a file outside
  the clean home and the worktree.
- `summary.json` of each run: hidden tests failed before, passed after; `peek_reads` 0; departures listed.
- `ship` output: "hidden tests passed" and the merge number.

## Stops

- Stop as blocked after 3 attempts at the same reproduced failure with no new evidence; report the failure, its
  owner and what would resume it.
- Revalidate after three increments or about four hours.

## Current state

**Deferred by Brian (2026-11-22): "docuemnt the gap thne lets come back to it later".** Known, accepted gap: the
milestone's agents read Brian's global instructions, so it is not shown that the template's own `AGENTS.md` is
enough for a stranger. Agent's judgment (not measured): the result is likely the same, because no step of the run
depended on Brian's instructions and the template's `AGENTS.md` names the same core steps.

Ready when it resumes: empty agent config folders (`/home/brian/projects/data/lockstep-milestone/home/agent-config/`),
repository `BrianMills2718/second-user` (copied from the public address, `make check` 0) with plans `add-greeting`
and `add-farewell` merged as #1. Left: the two agent logins (browser approval by the account owner; Codex device
codes last 15 minutes, three expired unused on 2026-11-22), then the two `run-plan` runs and `ship` merges.
Resume when a second person or machine uses the template, or when Brian says so.

## Non-gating next actions

- Brian: archive code2-template; decide whether the six repositories made from it move to this template.

## Roadmap

| Row | Goal | Depends on | Status |
| --- | --- | --- | --- |
| 1 | First minimal-core milestone (minimal-core plan, section 8) | none | done 2026-11-21 |
| 2 | A second user runs the core with nothing of Brian's (this file) | row 1 | deferred 2026-11-22 (gap accepted) |
| 3 | Add-ons, each only after a logged failure justifies it (section 8, "Rule for add-ons") | row 2 | open |

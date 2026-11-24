# Repoint citations of four retired plans

## Why

Brian, 2026-11-24: "cut whatever get us to optimal and safe then we can discuss" (the 100-file Markdown cap). Four
finished plans in `docs/planning/` were retired (`docs/retired/2026-11-24.md`, "Finished plans"). `Source:` lines in
the specs cited them by path; those paths now point at pinned GitHub copies of the same files.

## What Changes

Plan size: small

Only the cited path inside `Source:` lines. No requirement or scenario changes what it requires.

Wording-only: lockstep-projection/status-links-each-requirement-to-its-code-and-tests, plan-run/a-departure-report-compares-the-change-with-its-plan, lockstep-projection/the-link-file-lists-the-whole-chain, plan-run/an-unticked-task-is-listed-archived-or-not

## Impact

Specs `lockstep-checks`, `lockstep-guard`, `lockstep-plan-format`, `lockstep-projection`, `plan-run` and
`portable-template`, and the generated requirement text copied into `src/lockstep/`.

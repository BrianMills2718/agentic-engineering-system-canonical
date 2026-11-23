## Why

In the linked-chain acceptance run (2026-11-23, private repository `chain-test`, clean home), Claude built two plans
using only Bash: 7 and 5 shell calls, no Edit or Write. The copy's hook ran on each call (Claude debug log:
`PreToolUse:Bash [... lockstep-hook] finished with status 0`) but in a repository with OpenSpec specs and no layout
plan the shell route returned nothing, so the requirement text never reached the agent.

Source: inferred by agent from that run; Brian, 2026-11-23: "isnt this the whole thing that makes the whle systme
work?" (plan docs/planning/linked-chain-core-2026-11-23.md).

## What Changes

- In a repository with specs and no plan, a shell command that names or writes a file with an `Implements:`
  line gets that requirement's text, logged as `openspec_text`. Nothing is refused.

## Impact

- `src/lockstep/hook.py`, `tests/lockstep/test_lockstep_openspec_text.py`.

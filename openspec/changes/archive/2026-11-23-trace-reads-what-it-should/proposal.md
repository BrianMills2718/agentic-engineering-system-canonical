## Why

The trace check reported 142 findings in AES, many of them false. Two kinds came from behavior the spec did not
state: a quote marker shown as code in a document was read as a real marker, and a passing arch test (a diagram that
maps no packages) had no scenario to name. Source: Brian, 2026-11-23: "cleanup. and as you go make sure to docuemtn
any concern open quesiton icnonsitencies recommndations or anythgin else we should discuss"; plan
`docs/planning/alignment-cleanup-2026-11-23.md`.

## What Changes

- Quote markers inside code spans and fenced blocks are skipped; quoted passages keep their code words.
- The arch check's pass on a diagram that maps no packages is stated, with its scenario.

## Impact

`src/lockstep/checks/quotes.py`, `tests/lockstep/checks/test_lockstep_check_quotes.py`,
`tests/lockstep/checks/test_lockstep_check_arch.py`. Documents without such markers are read as before.

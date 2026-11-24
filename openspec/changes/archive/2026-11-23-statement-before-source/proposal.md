## Why

12 requirements put their `Source:` line before their statement, so the spec reader read their statement as empty
and the trace check and edit hook handed agents no requirement text (#1019 made the reader accept both orders as a
repair). Brian approved one order, checked (2026-11-23: "i approve", to Q49 in `docs/planning/open-questions.json`).

## What Changes

- The sources check fails on a requirement whose first paragraph is its `Source:` line (`source-first`).
- The 11 requirements in that order are reordered: statement, then `Source:`.
- AES's `make check` runs the order part (`make check-source-order`); its 63 items with no `Source:` line are a
  separate, older backlog and do not fail it.

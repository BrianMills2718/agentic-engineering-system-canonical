## Why

`aes-documentation-projection` repeats the general `lockstep-doc-facts` capability for AES alone: its two
requirements are that capability's "Declared source facts have one authority" and "Installed edit and merge paths
maintain facts", applied to AES's `projections:` in `lockstep.yaml`. Its 3 scenarios had no tests and sat on the
trace check's accepted list (alignment cleanup item 6). Brian approved keeping only the general spec (2026-11-23:
"i approve", to Q51 in `docs/planning/open-questions.json`).

## What Changes

- Both requirements are removed; AES's `lockstep.yaml` says that its `projections:` follow `lockstep-doc-facts`.
- The 5 trace findings leave `docs/planning/trace-accepted.txt`; links to the removed spec point to `lockstep-doc-facts`.

Compared scenario by scenario: "One source updates both views" is `lockstep-doc-facts` "Markdown facts regenerate
and stale check is read only" and "Installed post edit hook refreshes and precommit rejects stale"; "Bypassed
refresh is refused" and "Explicit refresh recovers" are the same two scenarios. "Existing hook and commit
configuration SHALL be preserved" is the general requirement's "while preserving existing hooks". Nothing unique
was left to move.

## Why

`scripts/concern_issue.py` and `tests/test_concern_issue.py` name `compliance-list/...` requirement IDs, but that
spec lives only in code2-workspace, so this repository's trace check read them as unknown (6 findings on the
accepted list; alignment cleanup item 13). Brian approved giving the requirement a home beside the script
(2026-11-23: "i approve", to Q52 in `docs/planning/open-questions.json`).

## What Changes

- New AES capability `concern-issue` holding the requirement "An open concern's title follows the repository's
  current status" and its five scenarios, word for word, for AES's copy of the script.
- The script's `Implements:` line and the tests' marks name `concern-issue/...`; the findings leave the accepted list.

Found while doing it: code2-workspace keeps its own copy of `scripts/concern_issue.py` (called by its
`compliance_list.py` and `process_share.py`) and tests it against its `compliance-list` spec, so the requirement
stays there too for that copy, instead of moving. Each repository stays self-contained; AES's copy differs only by
redacting issue text (`public_text.redact`).

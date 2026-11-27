Plan size: small

## Why

Pytest can exit zero when every hidden test is skipped. The acceptance check and ship can currently treat that as proof the implementation passed, although no hidden test passed.

Source: Brian, 2026-11-26: "make any high confidence imrpvoements", following the audit. C3 of `docs/planning/minimal-core-2026-11-20.md` requires the hidden tests to pass.

## What changes

- Read fresh pytest JUnit outcomes and require at least one passing hidden test.
- Keep compatibility with custom pytest commands that forward the hidden filenames and the pytest environment.
- Apply the same result check when ship reads a receipt or reruns hidden tests after its rebase.

# Source-local documentation facts reach reader surfaces

## Why

AES-CTX-004 and accepted Decision 0013 require artifact facts to live in the
artifact and wiki copies to be generated. Lockstep currently projects
requirements and coverage, while descriptions, interfaces and evidence
summaries can drift independently.

Source: Brian, 2026-11-12, "its not jsut a status tag ... ther should be hooks and stuff that automatically keep this all up to date", followed by "ok proceed", in the Company Planning documentation conversation.

## What Changes

Extend existing `lockstep check project` with declarative Markdown fact blocks.
Read YAML front matter, JSON/YAML records and Python AST docstrings/signatures
without importing project code. Install native post-edit fact refresh hooks
and include read-only projection checking in the pre-commit gate. Invalid
sources or target markers fail before projection writes. Narrative correctness
and source-description adequacy remain distinct from generated-copy freshness.

## Impact

Existing requirement projection and AES compatibility remain. Fact-only
consumers without OpenSpec requirements do not generate empty coverage pages
or rewrite historical plans. No model stage or other-consumer rollout.

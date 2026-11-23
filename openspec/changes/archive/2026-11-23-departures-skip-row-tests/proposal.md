# Departures skip a row's tests and spec links

Plan size: small

## Why

The template-layout proof run (docs/evidence/template-layout-proof-2026-11-23/) listed `tests/test_greet.py`, which
the layout row names in `tests:`, and `docs/specs/greeting/spec.md`, the link `make docs-specs` writes, as departures.

## What changes

- `run-plan`'s departure report also treats files named in a layout row's `tests:` at `REF` as planned, and never lists
  `docs/specs/` links.

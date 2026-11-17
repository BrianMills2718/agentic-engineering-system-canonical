## Why

While Project Meta's issues were being moved to code2-workspace on 2026-11-17, the moved copies lost their
`source:*` labels and changed numbers, so the hub page's label rules and issue references stopped matching them
(Needs you went from 9 to 12 within minutes). Each issue's body carries the marker `<!-- concern-key: K -->` written
by the job that filed it, and that marker survives the move.

Source: Brian, 2026-11-17 (the hub-page brief: sort by "a label or explicit title rule in config, not regex on prose
meaning"; list each item once). The concern-key marker is a machine field, not prose.

## What Changes

- The hub reads each waiting issue's concern key. `quiet_concern_keys` quiets by key; an `fyi_rules` entry may match
  by `concern_key_prefix` instead of its label; a `shared_causes` entry may name `concern_keys`; a failing unit's
  own issue is also found by the key `failed-unit:<unit>`.

## Impact

`scripts/hub_page.py`, `tests/test_hub_page.py`, `openspec/specs/hub-page/spec.md`; aes-config `hub_page:` settings.

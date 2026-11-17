## Why

The hub page's "Needs you" counted 31 items on 2026-11-17, but most were not things Brian must decide or do: 12 were
records-request status notices ("Records request j4: records provided"), 6 were failed services that agents fix,
`gates-nightly` was counted twice (the unit and its issue), the empty OpenRouter key appeared as 2 issues and 2
services, and the 98 inferred approvals sat in the same section. Brian's rule: only significant items go to him
(2026-11-16, "i approve 7 tight"), and he does not want to decide high-confidence or low-significance items
(2026-11-17, brief to this session).

Source: Brian, 2026-11-16 ("i approve 7 tight") and 2026-11-17 (the hub-page brief; AES #926, #927).

## What Changes

- Needs you holds only open `waiting:brian` issues and AES `owner:brian` issues, each listed once.
- Issues are sorted by labels and fixed title prefixes from settings, never by reading meaning: `quiet_issue_labels`
  (shown with the reason, not counted), `fyi_rules` (a label plus a title prefix: "FYI: records updates", grouped by
  label and repository, not counted).
- Failed services move to "Broken services", grouped by cause: a `shared_causes` entry gathers the units and issues it
  names; every other unit is its own cause with the failing-jobs page's reason (`failures_file`). A unit's own issue
  (the failing-jobs page's `issue_url`) and a cause's issues are listed there once, not under Needs you.
- The inferred approvals become a footer count, "Not shown: no significance field", because the oversight data has no
  field that marks significant items.
- What changed compares across every section, so an item that only moved section is neither new nor cleared.
- All new settings are optional; without them the page still builds.

## Impact

`scripts/hub_page.py`, `tests/test_hub_page.py`, `openspec/specs/hub-page/spec.md`; settings in aes-config
`graph-config.yaml` (`hub_page:`).

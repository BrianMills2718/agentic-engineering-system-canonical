## Why

On 2026-11-17 the hub's "Needs you" counted 9 issues, and 4 of them carry both `waiting:brian` and `owner:agent`
(code2-workspace #355 and #282, llm_client #369 and #407): an agent owns the next step, so they are not Brian's to
decide. They were counted only because nothing in the hub settings reads the `owner:agent` label.

Source: Brian's rules ("i approve 7 tight", 2026-11-16: only significant items go to him), applied by the
coordinator's Batch A brief of 2026-11-17 (use labels, not issue numbers).

## What Changes

- A new optional setting, `agent_labels` (label to reason), under `hub_page:`. A waiting issue carrying one of these
  labels goes to a new "Agent work" section, after Broken services and before FYI, with the reason, and is not
  counted under Needs you. Quiet labels and Broken services still take an issue first.
- Without the setting the page is unchanged.
- What changed counts an issue that moved into Agent work as neither new nor cleared.

## Impact

`scripts/hub_page.py`, `tests/test_hub_page.py`, `openspec/specs/hub-page/spec.md`; the setting in aes-config
`graph-config.yaml` (`hub_page:`).

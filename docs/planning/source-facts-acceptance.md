---
description: Bounded acceptance table for declared source-owned documentation facts, with replay, native dispatch and stale-check evidence kept distinct.
---

# A9: source facts stay current in their declared wiki copies

For example, changing Plan 61's source status must update its declared reader
block. If an edit bypasses the refresh hook, the read-only project check must
refuse the stale copy. This checks declared copied facts; it does not certify
arbitrary narrative accuracy or claim that all documentation has been organized.

Source: Brian's Company Planning conversation, 2026-11-12: "ther should be hooks
and stuff that automatically keep this all up to date", followed by "ok proceed".
Contract: [source-fact specification](../../openspec/specs/lockstep-doc-facts/spec.md).

| Case | What Brian should see | Observed result | Evidence |
|---|---|---|---|
| Plan lifecycle | A changed source status appears in the declared reader block. | Passed in both installed client-command paths. | Provider tests: `tests/lockstep/checks/test_lockstep_doc_projection.py`; [Consumer traces](https://github.com/BrianMills2718/company-planning/blob/main/docs/planning/reader-upkeep/demonstration-observations.json). |
| Description | Editing the source docstring changes the declared description. | Passed in both installed client-command paths. | [Consumer command traces](https://github.com/BrianMills2718/company-planning/blob/main/docs/planning/reader-upkeep/demonstration-observations.json). |
| Interface | Editing a source function signature changes the declared interface. | Passed in both installed client-command paths. | [Consumer command traces](https://github.com/BrianMills2718/company-planning/blob/main/docs/planning/reader-upkeep/demonstration-observations.json). |
| Evidence | Changing a retained JSON/YAML evidence field changes the displayed value. | Passed in both installed client-command paths. | [Consumer command traces](https://github.com/BrianMills2718/company-planning/blob/main/docs/planning/reader-upkeep/demonstration-observations.json). |
| Installed hook command | Replaying the exact installed Claude Code and Codex refresh commands updates the declared block. | 8/8 source-edit command replays passed; separate from native dispatch. | [Full command records](https://github.com/BrianMills2718/company-planning/blob/main/docs/planning/reader-upkeep/demonstration-observations.json). |
| Native-client dispatch | A fresh client edits only the source, and its recorded PostToolUse callback refreshes the block. | 2/2 fresh native CLI fixtures passed, each with exactly one source edit. Codex used its explicit audited-fixture trust bypass; installed checkout trust is a separate observation. | [Native full traces](https://github.com/BrianMills2718/company-planning/blob/main/docs/planning/reader-upkeep/native-dispatch.json). |
| Bypassed refresh | The project check exits nonzero for stale output and writes nothing; after refresh it passes. | Passed in both installed client-command paths. | [Stale make docs-check refusal, before/after](https://github.com/BrianMills2718/company-planning/blob/main/docs/planning/reader-upkeep/demonstration-observations.json). |
| Invalid declaration | Missing sources or malformed target markers fail explicitly. | Passed in both installed client-command paths. | Provider negative tests; [Consumer traces](https://github.com/BrianMills2718/company-planning/blob/main/docs/planning/reader-upkeep/demonstration-observations.json). |

The paired reader will be served at
[Company Planning documentation](https://hive.brianmills.dev/docs/company-planning/reader/upkeep/).
Delivery requires the consumer committed revision to be deployed. The recorded
observations above distinguish command replay, native fixtures and deployment. A1–A8 retain their previous
review scope; this table does not re-audit those outcomes.

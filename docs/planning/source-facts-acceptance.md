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
| Plan lifecycle | A changed source status appears in the declared reader block. | Consumer run pending. | Provider tests: `tests/lockstep/test_doc_projection.py`; consumer evidence pending. |
| Description | Editing the source docstring changes the declared description. | Consumer run pending. | Same provider tests; consumer evidence pending. |
| Interface | Editing a source function signature changes the declared interface. | Consumer run pending. | Same provider tests; consumer evidence pending. |
| Evidence | Changing a retained JSON/YAML evidence field changes the displayed value. | Consumer run pending. | Same provider tests; consumer evidence pending. |
| Installed hook command | Replaying the exact installed Claude Code and Codex refresh commands updates the declared block. | Consumer run pending; this is separate from native dispatch. | Consumer full command records pending. |
| Native-client dispatch | A fresh client edits only the source, and its recorded PostToolUse callback refreshes the block. | Unobserved; no native-dispatch claim. | Native session trace pending. |
| Bypassed refresh | The project check exits nonzero for stale output and writes nothing; after refresh it passes. | Consumer run pending. | Consumer read-only before/after command records pending. |
| Invalid declaration | Missing sources or malformed target markers fail explicitly. | Consumer run pending. | Provider negative tests; consumer evidence pending. |

The paired reader will be served at
[Company Planning documentation](https://hive.brianmills.dev/docs/company-planning/reader/upkeep/).
It is not declared delivered here until its committed revision is deployed and
the recorded consumer observations are linked. A1–A8 retain their previous
review scope; this table does not re-audit those outcomes.

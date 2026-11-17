## Why

code2-workspace `scripts/rule_audit_nightly.py` (the `context-upkeep` job, daily 04:15) audits the agent instruction
files across the workspace by running two Project Meta tools with Project Meta as the working folder:
`scripts/audit_instruction_quality.py --all --json` (oversized, misplaced, duplicated, derivable) and
`scripts/scan_doc_freshness_ecosystem.py --json` (instruction files that sat still while the code moved). Brian approved
the nightly audit on 2026-11-06 ("i approve", harness review Context row); its 2026-11-16 run reported 315 findings in
123 repositories, and no AES or Lockstep check covers instruction-file size, duplication or staleness. Project Meta is
being retired (AES consolidation plan, row 11, "Before item 11", step 5), so both tools move here.

Source: inferred by agent, from the AES consolidation plan row 11 (the ordered ports before the archive yes).

## What Changes

- The two scripts are copied from Project Meta `f6f0d6f91` with their tests. The only change: the project graph default
  is `PROJECT_GRAPH`, else `~/code2/aes-config/PROJECT_GRAPH.json` (as `md_file_cap.py`), not the graph beside the script.
- New capability `instruction-audit`.

## Impact

New `scripts/audit_instruction_quality.py`, `scripts/scan_doc_freshness_ecosystem.py`,
`tests/test_audit_instruction_quality.py`, `tests/test_scan_doc_freshness_ecosystem.py`. The caller switches separately
(code2-workspace `rule_audit_nightly.py`, run from `~/.hive-brain/aes`). The `instruction-surfaces` skill still names
the Project Meta paths.

---
schema_version: "1.0"
artifact_type: design_plan
id: adoption-progress-fields
plan_id: adoption-progress-fields
status: proposed
planning_path: requested
method_conformance_receipt: docs/plans/adoption-progress-fields.receipt.json
conflict_surfaces:
  - {kind: repository_path, repository: "BrianMills2718/agentic-engineering-system-canonical", target: "src/agentic_engineering_system/commit_rule.py", access: write}
  - {kind: repository_path, repository: "BrianMills2718/agentic-engineering-system-canonical", target: "tests/greenfield/test_commit_rule.py", access: write}
  - {kind: repository_path, repository: "BrianMills2718/agentic-engineering-system-canonical", target: "docs/model/trace.yaml", access: write}
  - {kind: repository_path, repository: "BrianMills2718/agentic-engineering-system-canonical", target: "generated/docstring_wiki.md", access: write}
trace_review_criteria:
  - criterion_id: outcome
    expected_outcome: pass
goal:
  outcome: "A [Goal id]/[Plan #N] commit whose plan differs from its adopted bytes only in progress fields (front-matter status/owner/updated, Status:/Owner: lines, Status/Progress/Notes/Log-style sections) is accepted with the advisory 'plan progress fields changed since adoption; identity unchanged'; any other plan change, or an adopted version not found in the plan file's git history, is still refused with 'plan changed since adoption; re-adopt it'"
  canonical_example: "In a temp git repo with an adopted plan committed, changing its front matter status: proposed to status: in_progress and committing [Goal demo] work is accepted with the advisory; appending a new step to its body is refused."
  forbidden_substitutes: "claiming success from a check's last line or exit status alone; a change outside the listed files; a commit without the saved check output"
  boundaries: "only these files: src/agentic_engineering_system/commit_rule.py, tests/greenfield/test_commit_rule.py, docs/model/trace.yaml, generated/docstring_wiki.md; no irreversible action and no spend; Brian's request as quoted is the scope"
  done_when: "One success check, its complete output (every test name, pass/fail counts and exit status) saved to docs/plans/adoption-progress-fields.check.txt and read in full: python -m pytest -v tests/greenfield/test_commit_rule.py, where test_plan_status_line_change_after_adoption_is_accepted_with_advisory asserts accept plus the advisory text for a status-field and Status-section edit; test_plan_owner_rename_after_adoption_is_accepted asserts accept for an owner: change; test_plan_scope_change_after_adoption_is_still_refused asserts refusal for a goal/steps edit; test_plan_progress_change_without_adopted_history_is_refused asserts refusal when the adopted bytes are in no commit; and the existing test_plan_changed_after_adoption_is_refused still passes. The check's full output on the parent commit and on the change commit is committed as docs/plans/adoption-progress-fields.check.txt, and the commit is tagged [Goal adoption-progress-fields] with an Asked: line quoting the request. python3 \"$SESSION_PLUGIN_ROOT/scripts/durable_docs_check.py\" --repo . --plan docs/plans/adoption-progress-fields.md --range 573c7496ddc86bc9d79d8a2681f32bd33765f422..HEAD exits 0 and its output is in the same file."
  do_not_gate_on: "Brian's review of the plan page; work outside the listed files"
---

# Commit rule accepts plan progress-field edits made after adoption

## When a run fails or surprises us

This procedure is separate from the anticipated failure named in the disproof
under Success and disproof: it applies to any run that fails or surprises us.
Preserve the failed run itself: keep its complete output (command, every
line, exit status) and its execution trace id, never overwritten by a rerun.
Before selecting a fix,
read the complete inputs, prompts, tool arguments/results, intermediate stages
and final output, including the full check command/output and the changed files.
Cite the observed divergence and classify evidence absent, returned but unused
or contradicted, invalid expectation, or unresolved. An unresolved diagnosis
cannot authorize a causal repair; it permits only further investigation. Bind the targeted repair to a new
traced verification run; retain the failed original. Review every failing or
surprising item and a sample of passes. A complete review is distinct from a
passing run. Criterion `outcome` covers the entire requested success check.

## Actor and result

**Actor:** Brian, who asked for this change.

**Request (verbatim):** feedback loop licence AES#673 2026-10-12 "Narrow the adoption fingerprint to only the fields that define plan identity and scope, excluding fields the procedure itself requires to change post-adoption such as status lines, owner, and notes."

**Desired result:** A [Goal id]/[Plan #N] commit whose plan differs from its adopted bytes only in progress fields (front-matter status/owner/updated, Status:/Owner: lines, Status/Progress/Notes/Log-style sections) is accepted with the advisory 'plan progress fields changed since adoption; identity unchanged'; any other plan change, or an adopted version not found in the plan file's git history, is still refused with 'plan changed since adoption; re-adopt it'.

**Stable example:** In a temp git repo with an adopted plan committed, changing its front matter status: proposed to status: in_progress and committing [Goal demo] work is accepted with the advisory; appending a new step to its body is refused.

## Authority and non-goals

**Authority:** Brian asked for this change in his own repository; one agent makes it.

**Non-goals:** nothing outside the files listed under Vertical and reset. No irreversible action and no spend.

## Requirements

| Id | Requirement | Source | Check | Status |
| --- | --- | --- | --- | --- |
| R1 | A [Goal id]/[Plan #N] commit whose plan differs from its adopted bytes only in progress fields (front-matter status/owner/updated, Status:/Owner: lines, Status/Progress/Notes/Log-style sections) is accepted with the advisory 'plan progress fields changed since adoption; identity unchanged'; any other plan change, or an adopted version not found in the plan file's git history, is still refused with 'plan changed since adoption; re-adopt it'. | asked: feedback loop licence AES#673 2026-10-12 "Narrow the adoption fingerprint to only the fields that define plan identity and scope, excluding fields the procedure itself requires to change post-adoption such as status lines, owner, and notes." | the success check under Success and disproof, its output saved as `docs/plans/adoption-progress-fields.check.txt` | planned, not yet run |

Requirements the change's own claims imply: none beyond R1; the change presents nothing as following a standard, schema or contract.

## AES target

This repository is governed by an AES target (`.aes/target.yaml`). How R1 onward map to it:

- No target delta: the change leaves .aes/target.yaml unchanged, so no aes plan validate result is needed. Existing items it maps to: AP-REQ-001 and SC-AP-001 (the commit rule keeps refusing unplanned or re-scoped work and stops refusing progress-only plan edits); verification subject: the four new tests in tests/greenfield/test_commit_rule.py

## Durable documents

This repository declares durable documents (`durable_documents` in `.agentic/repo.yaml`); its declared roles are `goal`, `requirements`, `system_model`, `decisions`, `plans`, `catalog`. Each role named below is one of them (checked by quick-adopt).

Durable documents: system_model#RULE-PLAN-ADOPTED-FOR-COMMIT

At completion, `python3 "$SESSION_PLUGIN_ROOT/scripts/durable_docs_check.py" --repo . --plan docs/plans/adoption-progress-fields.md --range 573c7496ddc86bc9d79d8a2681f32bd33765f422..HEAD` must exit 0; its full output is appended to `docs/plans/adoption-progress-fields.check.txt` (the durable-documents check, Plan #61; `durable_docs_check.py` ships in the Company Planning plugin).

## Success and disproof

**Success evidence:** One success check, its complete output (every test name, pass/fail counts and exit status) saved to docs/plans/adoption-progress-fields.check.txt and read in full: python -m pytest -v tests/greenfield/test_commit_rule.py, where test_plan_status_line_change_after_adoption_is_accepted_with_advisory asserts accept plus the advisory text for a status-field and Status-section edit; test_plan_owner_rename_after_adoption_is_accepted asserts accept for an owner: change; test_plan_scope_change_after_adoption_is_still_refused asserts refusal for a goal/steps edit; test_plan_progress_change_without_adopted_history_is_refused asserts refusal when the adopted bytes are in no commit; and the existing test_plan_changed_after_adoption_is_refused still passes.

**Trace review:** two runs of the success check above are judged from their full output: one on the parent commit before the change (the disproof run: it must show the defect or the check failing, which proves the check can fail) and one on the commit that makes the change (the success run); no model, agent or LLM pipeline runs under this plan. Where the trace lives: the check's complete output, with the exact command and its exit status, is saved as `docs/plans/adoption-progress-fields.check.txt` and committed with the change. What must be seen in it beyond the final result: the command ran against the files listed under Vertical and reset at that commit, each check or test it reports appears by name with its result and none is skipped, and the exit status matches; for each model element listed under System model, the output shows what that line says. Both runs are saved in that one file, each headed by its commit: the disproof condition is judged from both (it holds if the success run still shows the defect, or if the before run already passes, meaning the check cannot detect it), and success from the success run.

**Disproof:** A plan whose goal, scope or steps changed after adoption is accepted, or a status-only edit is still refused.

## System model

**System model:** `docs/model/trace.yaml`, a file in this repository describing this repository only (not a shared model). Reachable from the documentation entry point `wiki/index.md`, which links `docs/model/trace.yaml`.

**Model elements this change adds, changes or relies on, and what the saved check output must show of each:**

- Rule RULE-PLAN-ADOPTED-FOR-COMMIT (docs/model/trace.yaml, owner commit_rule.py): its statement changes from 'plan bytes match' to 'plan identity matches, progress fields excluded', and its checks list gains the four new tests; the saved check output must show the four new tests passing by name, the status-only commit printing 'accept [Goal demo]' with 'plan progress fields changed since adoption; identity unchanged', and the scope-change commit printing 'plan changed since adoption; re-adopt it'

**Views, freshness and reconciliation:** the applicable view is the requirement-to-verification link in the Requirements table (each requirement and the check that shows it, the check being source-linked by its command); no other view applies because the change adds, changes or relies on no entity, process, record, event or view beyond the elements listed above. Freshness: the model's drift test (`tests/greenfield/test_commit_rule.py`, `tests/greenfield/test_plan_receipt.py`, `tests/greenfield/test_trace_review.py`, `tests/greenfield/test_characterize.py`, `tests/greenfield/test_evidence.py`, `tests/greenfield/test_reconcile.py`) runs inside the success check and its output is in the saved check file. If an element above is added, removed or renamed, the model, its view coverage and the saved check output are reconciled in the same commit, and otherwise the model needs no update because the elements keep their meaning.

## Capability reuse

Checked against the capability catalogue in agentic-capability-architecture-canonical (`reuse_candidates.yml` and `capability_registry.yml`):

- No catalogue entry fits, because the catalogue does not list the AES commit rule; this change narrows an existing check and adds no capability
- What the work needs that no entry provides: edits to this repository's own files (`src/agentic_engineering_system/commit_rule.py`, `tests/greenfield/test_commit_rule.py`, `docs/model/trace.yaml`, `generated/docstring_wiki.md`); catalogue entries are cross-project capabilities, and none edits a repository's own source.

## Uncertainties

Material uncertainties. This one is the complete set; it is material because a file outside the list would
make the change exceed this plan's scope.

| Material uncertainty | Owner or resolving evidence |
| --- | --- |
| Whether the change needs files beyond the list below; if so it is out of scope for this plan | Resolved before editing: grep -n _adoption_of src/agentic_engineering_system/commit_rule.py shows the hash comparison at one function with five callers in the same file; tests live in tests/greenfield/test_commit_rule.py; trace rule RULE-PLAN-ADOPTED-FOR-COMMIT in docs/model/trace.yaml |

## Vertical and reset

One vertical over these files (and the saved check output, `docs/plans/adoption-progress-fields.check.txt`):

- `src/agentic_engineering_system/commit_rule.py`
- `tests/greenfield/test_commit_rule.py`
- `docs/model/trace.yaml`
- `generated/docstring_wiki.md`

The vertical delivers: A [Goal id]/[Plan #N] commit whose plan differs from its adopted bytes only in progress fields (front-matter status/owner/updated, Status:/Owner: lines, Status/Progress/Notes/Log-style sections) is accepted with the advisory 'plan progress fields changed since adoption; identity unchanged'; any other plan change, or an adopted version not found in the plan file's git history, is still refused with 'plan changed since adoption; re-adopt it'. It is done when this holds: One success check, its complete output (every test name, pass/fail counts and exit status) saved to docs/plans/adoption-progress-fields.check.txt and read in full: python -m pytest -v tests/greenfield/test_commit_rule.py, where test_plan_status_line_change_after_adoption_is_accepted_with_advisory asserts accept plus the advisory text for a status-field and Status-section edit; test_plan_owner_rename_after_adoption_is_accepted asserts accept for an owner: change; test_plan_scope_change_after_adoption_is_still_refused asserts refusal for a goal/steps edit; test_plan_progress_change_without_adopted_history_is_refused asserts refusal when the adopted bytes are in no commit; and the existing test_plan_changed_after_adoption_is_refused still passes.

Make the change, run the success check before and after it, commit. Reset: `git revert` of the commit. Not pursued: anything outside these files. This plan adds no coordinated-work ceremony: no work-unit graph, no review or release contract, no claim beyond the repository's own rules.

## Activation facts

Each fact, with its value and why:

- `shared_mechanism`: false -- the change edits only the listed files and adds no contract, algorithm or mechanism other code uses.
- `empirical_comparison_proposed`: false -- no alternatives are compared; the success check verifies the one change.
- `llm_central`: false -- the change makes no model call.
- `irreversible_or_spend_action`: false -- the change is reverted by `git revert` and spends nothing.
- `claims_external_standard`: false -- the work claims no external standard, schema or contract.
- `aes_governed_target`: true -- derived, this repository has `.aes/target.yaml`; see AES target.
- `durable_documents_declared`: true -- derived, `.agentic/repo.yaml` has `durable_documents`; see Durable documents.


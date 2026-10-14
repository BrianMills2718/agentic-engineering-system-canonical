---
schema_version: "1.0"
artifact_type: design_plan
id: durable-check-commit-rule
plan_id: durable-check-commit-rule
status: proposed
planning_path: requested
method_conformance_receipt: docs/plans/durable-check-commit-rule.receipt.json
trace_review_criteria:
  - criterion_id: outcome
    expected_outcome: pass
goal:
  outcome: "A [Goal id] commit under a quick plan whose plan names a durable-documents completion command, in a repository that declares durable_documents, runs that check on the commit being made and is refused when the plan fails to name a durable rule whose owner file the change touches (or its declaration is otherwise invalid); an unchanged declared document stays a logged note"
  canonical_example: "In a fixture repo whose trace names src/app.py as a rule's owner, a [Goal p] commit editing src/app.py under a plan whose Durable documents line is 'none -- tidy wording only here' is refused with check durable-docs naming PLAN-OWNER-UNNAMED; the same commit with the line naming system_model#RULE-A is accepted."
  forbidden_substitutes: "claiming success from a check's last line or exit status alone; a change outside the listed files; a commit without the saved check output"
  boundaries: "only these files: src/agentic_engineering_system/commit_rule.py, tests/greenfield/test_commit_rule.py, docs/model/trace.yaml, docs/model/ODD.md, generated/docstring_wiki.md; no irreversible action and no spend; Brian's request as quoted is the scope"
  done_when: "tests/greenfield/test_commit_rule.py::test_durable_docs_check_refuses_unnamed_owner_and_accepts_named asserts the refusal names PLAN-OWNER-UNNAMED and check durable-docs for the unnamed case and acceptance for the named case; test_durable_docs_check_observe_and_skips asserts durable: observe only logs, a plan without the completion command or a repo without durable_documents gets no durable check, and a missing check script leaves a note and never refuses; all other commit-rule tests still pass unchanged. The check's full output on the parent commit and on the change commit is committed as docs/plans/durable-check-commit-rule.check.txt, and the commit is tagged [Goal durable-check-commit-rule] with an Asked: line quoting the request. python3 \"$SESSION_PLUGIN_ROOT/scripts/durable_docs_check.py\" --repo . --plan docs/plans/durable-check-commit-rule.md --range f0076040e67914cef0d96d144ed23f4ba7370686..HEAD exits 0 and its output is in the same file."
  do_not_gate_on: "Brian's review of the plan page; work outside the listed files"
---

# Commit rule runs the durable-documents check for quick plans

## When a run fails or surprises us

This procedure is separate from the anticipated failure named in the disproof
under Success and disproof: it applies to any run that fails or surprises us.
Preserve the failed check and its execution trace id. Before selecting a fix,
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

**Request (verbatim):** Brian 2026-10-12 "i approve" (approving four fixes; the first: close the gap that lets plans finish without the durable-documents check)

**Desired result:** A [Goal id] commit under a quick plan whose plan names a durable-documents completion command, in a repository that declares durable_documents, runs that check on the commit being made and is refused when the plan fails to name a durable rule whose owner file the change touches (or its declaration is otherwise invalid); an unchanged declared document stays a logged note.

**Stable example:** In a fixture repo whose trace names src/app.py as a rule's owner, a [Goal p] commit editing src/app.py under a plan whose Durable documents line is 'none -- tidy wording only here' is refused with check durable-docs naming PLAN-OWNER-UNNAMED; the same commit with the line naming system_model#RULE-A is accepted.

## Authority and non-goals

**Authority:** Brian asked for this change in his own repository; one agent makes it.

**Non-goals:** nothing outside the files listed under Vertical and reset. No irreversible action and no spend.

## Requirements

| Id | Requirement | Source | Check | Status |
| --- | --- | --- | --- | --- |
| R1 | A [Goal id] commit under a quick plan whose plan names a durable-documents completion command, in a repository that declares durable_documents, runs that check on the commit being made and is refused when the plan fails to name a durable rule whose owner file the change touches (or its declaration is otherwise invalid); an unchanged declared document stays a logged note. | asked: Brian 2026-10-12 "i approve" (approving four fixes; the first: close the gap that lets plans finish without the durable-documents check) | the success check under Success and disproof, its output saved as `docs/plans/durable-check-commit-rule.check.txt` | planned, not yet run |

Requirements the change's own claims imply: none beyond R1; the change presents nothing as following a standard, schema or contract.

## AES target

This repository is governed by an AES target (`.aes/target.yaml`). How R1 onward map to it:

- No target delta: the change leaves .aes/target.yaml unchanged, so no aes plan validate result is needed. Existing items it maps to: AP-REQ-001 and SC-AP-001 (the commit rule keeps refusing unplanned work and now also refuses a quick-plan commit whose durable-documents declaration fails); verification subject: the two new tests in tests/greenfield/test_commit_rule.py

## Durable documents

This repository declares durable documents (`durable_documents` in `.agentic/repo.yaml`); its declared roles are `goal`, `requirements`, `system_model`, `decisions`, `plans`, `catalog`. Each role named below is one of them (checked by quick-adopt).

Durable documents: system_model#RULE-DURABLE-DOCS-FOR-COMMIT, system_model#RULE-COMMIT-TAG, system_model#RULE-PLAN-ADOPTED-FOR-COMMIT

At completion, `python3 "$SESSION_PLUGIN_ROOT/scripts/durable_docs_check.py" --repo . --plan docs/plans/durable-check-commit-rule.md --range f0076040e67914cef0d96d144ed23f4ba7370686..HEAD` must exit 0; its full output is appended to `docs/plans/durable-check-commit-rule.check.txt` (the durable-documents check, Plan #61; `durable_docs_check.py` ships in the Company Planning plugin).

## Success and disproof

**Success evidence:** tests/greenfield/test_commit_rule.py::test_durable_docs_check_refuses_unnamed_owner_and_accepts_named asserts the refusal names PLAN-OWNER-UNNAMED and check durable-docs for the unnamed case and acceptance for the named case; test_durable_docs_check_observe_and_skips asserts durable: observe only logs, a plan without the completion command or a repo without durable_documents gets no durable check, and a missing check script leaves a note and never refuses; all other commit-rule tests still pass unchanged.

**Trace review:** two runs of the success check above are judged from their full output: one on the parent commit before the change (the disproof run: it must show the defect or the check failing, which proves the check can fail) and one on the commit that makes the change (the success run); no model, agent or LLM pipeline runs under this plan. Where the trace lives: the check's complete output, with the exact command and its exit status, is saved as `docs/plans/durable-check-commit-rule.check.txt` and committed with the change. What must be seen in it beyond the final result: the command ran against the files listed under Vertical and reset at that commit, each check or test it reports appears by name with its result and none is skipped, and the exit status matches; for each model element listed under System model, the output shows what that line says. Both runs are saved in that one file, each headed by its commit: the disproof condition is judged from both (it holds if the success run still shows the defect, or if the before run already passes, meaning the check cannot detect it), and success from the success run.

**Disproof:** A commit touching a rule owner under a plan that does not name the rule is accepted under durable: enforce, or a commit in a repository without durable_documents (or under an older plan without the completion command) is refused by this check.

## System model

**System model:** `docs/model/ODD.md`, a file in this repository describing this repository only (not a shared model). Reachable from the documentation entry point `wiki/index.md`, which links `docs/model/ODD.md`.

**Model elements this change adds, changes or relies on, and what the saved check output must show of each:**

- Process PROC-COMMIT-CHECK (docs/model/trace.yaml): gains rule RULE-DURABLE-DOCS-FOR-COMMIT; the check output shows the new test refusing with check durable-docs
- Stored state: the per-repository verdict log gains check value durable-docs and notes from the durable check; the new tests assert the verdict's check field and notes
- Configuration: new key durable (observe or enforce, default: mode) in the commit-rule config; the observe test asserts it only logs
- Freshness and drift: the model's own drift check is durable_docs_check.py --repo . (trace ids, owners and checks resolve; prose and trace agree), run in the success check and saved to check.txt with exit 0; the plan completion command durable_docs_check.py --plan ... --range must also exit 0, which requires the trace to gain RULE-DURABLE-DOCS-FOR-COMMIT since commit_rule.py is a rule owner

**Views, freshness and reconciliation:** the applicable view is the requirement-to-verification link in the Requirements table (each requirement and the check that shows it, the check being source-linked by its command); no other view applies because the change adds, changes or relies on no entity, process, record, event or view beyond the elements listed above. Freshness: the model names no drift test, so none runs; the success check is the only freshness evidence for the elements above. If an element above is added, removed or renamed, the model, its view coverage and the saved check output are reconciled in the same commit, and otherwise the model needs no update because the elements keep their meaning.

## Capability reuse

Checked against the capability catalogue in agentic-capability-architecture-canonical (`reuse_candidates.yml` and `capability_registry.yml`):

- No catalogue entry fits, because the catalogue lists neither the AES commit rule nor Company Planning's durable-documents check; this change wires the existing check into the existing rule and adds no capability
- What the work needs that no entry provides: edits to this repository's own files (`src/agentic_engineering_system/commit_rule.py`, `tests/greenfield/test_commit_rule.py`, `docs/model/trace.yaml`, `docs/model/ODD.md`, `generated/docstring_wiki.md`); catalogue entries are cross-project capabilities, and none edits a repository's own source.

## Uncertainties

Material uncertainties. This one is the complete set; it is material because a file outside the list would
make the change exceed this plan's scope.

| Material uncertainty | Owner or resolving evidence |
| --- | --- |
| Whether the change needs files beyond the list below; if so it is out of scope for this plan | Resolved before editing: git diff --stat origin/main after the change lists only the five files below plus docs/plans/durable-check-commit-rule.* |

## Vertical and reset

One vertical over these files (and the saved check output, `docs/plans/durable-check-commit-rule.check.txt`):

- `src/agentic_engineering_system/commit_rule.py`
- `tests/greenfield/test_commit_rule.py`
- `docs/model/trace.yaml`
- `docs/model/ODD.md`
- `generated/docstring_wiki.md`

The vertical delivers: A [Goal id] commit under a quick plan whose plan names a durable-documents completion command, in a repository that declares durable_documents, runs that check on the commit being made and is refused when the plan fails to name a durable rule whose owner file the change touches (or its declaration is otherwise invalid); an unchanged declared document stays a logged note. It is done when this holds: tests/greenfield/test_commit_rule.py::test_durable_docs_check_refuses_unnamed_owner_and_accepts_named asserts the refusal names PLAN-OWNER-UNNAMED and check durable-docs for the unnamed case and acceptance for the named case; test_durable_docs_check_observe_and_skips asserts durable: observe only logs, a plan without the completion command or a repo without durable_documents gets no durable check, and a missing check script leaves a note and never refuses; all other commit-rule tests still pass unchanged.

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

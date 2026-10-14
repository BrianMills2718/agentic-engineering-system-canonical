---
schema_version: "1.0"
artifact_type: design_plan
id: commit-rule-root-relative-links
plan_id: commit-rule-root-relative-links
status: proposed
planning_path: requested
method_conformance_receipt: docs/plans/commit-rule-root-relative-links.receipt.json
conflict_surfaces:
  - {kind: repository_path, repository: "BrianMills2718/agentic-engineering-system-canonical", target: "src/agentic_engineering_system/commit_rule.py", access: write}
  - {kind: repository_path, repository: "BrianMills2718/agentic-engineering-system-canonical", target: "tests/greenfield/test_commit_rule.py", access: write}
  - {kind: repository_path, repository: "BrianMills2718/agentic-engineering-system-canonical", target: "generated/docstring_wiki.md", access: write}
  - {kind: repository_path, repository: "BrianMills2718/agentic-engineering-system-canonical", target: "docs/model/trace.yaml", access: write}
  - {kind: repository_path, repository: "BrianMills2718/agentic-engineering-system-canonical", target: "wiki/index.md", access: write}
trace_review_criteria:
  - criterion_id: outcome
    expected_outcome: pass
goal:
  outcome: "aes commit check resolves a Markdown link starting with / against the repository root, then wiki/, so new pages a wiki links root-relatively count as reached"
  canonical_example: "personal-wiki worktrees/v1-calls has 25 new pages that wiki/index.md links as /people/..., /places/...; aes commit check currently refuses them and accepts them after the fix."
  forbidden_substitutes: "claiming success from a check's last line or exit status alone; a change outside the listed files; a commit without the saved check output"
  boundaries: "only these files: src/agentic_engineering_system/commit_rule.py, tests/greenfield/test_commit_rule.py, generated/docstring_wiki.md, docs/model/trace.yaml, wiki/index.md; no irreversible action and no spend; Brian's request as quoted is the scope"
  done_when: "tests/greenfield/test_commit_rule.py::test_root_relative_links_resolve_against_the_repo_root_then_the_wiki_folder asserts a commit adding wiki/people/a.md (linked /people/a.md) and docs/b.md (linked /docs/b.md) is accepted while an unlinked page is still refused; ::test_a_shaping_commit_may_link_its_proposal_root_relatively asserts a [Shaping] commit whose wiki line links /proposals/<id>/plan.md is accepted as navigation; both fail before the fix and pass after; the rest of test_commit_rule.py passes. The check's full output on the parent commit and on the change commit is committed as docs/plans/commit-rule-root-relative-links.check.txt, and the commit is tagged [Goal commit-rule-root-relative-links] with an Asked: line quoting the request. python3 \"$SESSION_PLUGIN_ROOT/scripts/durable_docs_check.py\" --repo . --plan docs/plans/commit-rule-root-relative-links.md --range fecf733682da79461ec31f28d18420f089552a85..HEAD exits 0 and its output is in the same file."
  do_not_gate_on: "Brian's review of the plan page; work outside the listed files"
---

# Commit rule resolves root-relative wiki links

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

**Request (verbatim):** Brian 2026-10-13 (via coordinator session): "Please also fix the AES commit rule, which has the same root-relative link bug and currently blocks a personal-wiki commit ... Use the same rule as md_file_cap: strip the leading \"/\", try the repo root first, then wiki/."

**Desired result:** aes commit check resolves a Markdown link starting with / against the repository root, then wiki/, so new pages a wiki links root-relatively count as reached.

**Stable example:** personal-wiki worktrees/v1-calls has 25 new pages that wiki/index.md links as /people/..., /places/...; aes commit check currently refuses them and accepts them after the fix.

## Authority and non-goals

**Authority:** Brian asked for this change in his own repository; one agent makes it.

**Non-goals:** nothing outside the files listed under Vertical and reset. No irreversible action and no spend.

## Requirements

| Id | Requirement | Source | Check | Status |
| --- | --- | --- | --- | --- |
| R1 | aes commit check resolves a Markdown link starting with / against the repository root, then wiki/, so new pages a wiki links root-relatively count as reached. | asked: Brian 2026-10-13 (via coordinator session): "Please also fix the AES commit rule, which has the same root-relative link bug and currently blocks a personal-wiki commit ... Use the same rule as md_file_cap: strip the leading \"/\", try the repo root first, then wiki/." | the success check under Success and disproof, its output saved as `docs/plans/commit-rule-root-relative-links.check.txt` | planned, not yet run |

Requirements the change's own claims imply: none beyond R1; the change presents nothing as following a standard, schema or contract.

## AES target

This repository is governed by an AES target (`.aes/target.yaml`). How R1 onward map to it:

- No target delta: .aes/target.yaml is unchanged, so no aes plan validate result is needed. Existing items it maps to: AP-REQ-001 and SC-AP-001 (the commit rule judges each commit correctly); planned artifacts ART-SRC-COMMIT-RULE and the test_commit_rule.py artifact; verification subject: the two new tests in tests/greenfield/test_commit_rule.py

## Durable documents

This repository declares durable documents (`durable_documents` in `.agentic/repo.yaml`); its declared roles are `goal`, `requirements`, `system_model`, `decisions`, `plans`, `catalog`. Each role named below is one of them (checked by quick-adopt).

Durable documents: system_model#RULE-COMMIT-TAG, system_model#RULE-PLAN-ADOPTED-FOR-COMMIT, system_model#RULE-DURABLE-DOCS-FOR-COMMIT

At completion, `python3 "$SESSION_PLUGIN_ROOT/scripts/durable_docs_check.py" --repo . --plan docs/plans/commit-rule-root-relative-links.md --range fecf733682da79461ec31f28d18420f089552a85..HEAD` must exit 0; its full output is appended to `docs/plans/commit-rule-root-relative-links.check.txt` (the durable-documents check, Plan #61; `durable_docs_check.py` ships in the Company Planning plugin).

## Success and disproof

**Success evidence:** tests/greenfield/test_commit_rule.py::test_root_relative_links_resolve_against_the_repo_root_then_the_wiki_folder asserts a commit adding wiki/people/a.md (linked /people/a.md) and docs/b.md (linked /docs/b.md) is accepted while an unlinked page is still refused; ::test_a_shaping_commit_may_link_its_proposal_root_relatively asserts a [Shaping] commit whose wiki line links /proposals/<id>/plan.md is accepted as navigation; both fail before the fix and pass after; the rest of test_commit_rule.py passes.

**Trace review:** two runs of the success check above are judged from their full output: one on the parent commit before the change (the disproof run: it must show the defect or the check failing, which proves the check can fail) and one on the commit that makes the change (the success run); no model, agent or LLM pipeline runs under this plan. Where the trace lives: the check's complete output, with the exact command and its exit status, is saved as `docs/plans/commit-rule-root-relative-links.check.txt` and committed with the change. What must be seen in it beyond the final result: the command ran against the files listed under Vertical and reset at that commit, each check or test it reports appears by name with its result and none is skipped, and the exit status matches; for each model element listed under System model, the output shows what that line says. Both runs are saved in that one file, each headed by its commit: the disproof condition is judged from both (it holds if the success run still shows the defect, or if the before run already passes, meaning the check cannot detect it), and success from the success run.

**Disproof:** Every run's full output goes to docs/plans/commit-rule-root-relative-links.check.txt in this repository. Run 1: pytest tests/greenfield/test_commit_rule.py (each test's pass/fail; for a failure the captured hook stderr and the commit-rule log entry the test reads); fails if either new test or any existing test fails. Run 2: after reinstalling aes from merged main, 'aes commit check --preflight -m "[Goal personal-wiki-v1-calls] ..."' in ~/code/personal-wiki/worktrees/v1-calls (full stdout/stderr, appended to check.txt in a follow-up commit); fails if it still lists any of the 25 root-relatively linked pages under 'new document(s) not reached'.

## System model

**System model:** `docs/model/trace.yaml`, a file in this repository describing this repository only (not a shared model). Reachable from the documentation entry point `wiki/index.md`, which links `docs/model/trace.yaml`.

**Model elements this change adds, changes or relies on, and what the saved check output must show of each:**

- PROC-COMMIT-CHECK (relied on, unchanged): the change lives inside the commit-msg check's new-document reach step and relies on no other model element. Run 1's saved output must show the new test passing, meaning the commit-rule log entry has verdict accept for the commit adding the root-relatively linked pages and verdict refuse with check doc-reach naming nope2.md for the unlinked page

**Views, freshness and reconciliation:** the applicable view is the requirement-to-verification link in the Requirements table (each requirement and the check that shows it, the check being source-linked by its command); no other view applies because the change adds, changes or relies on no entity, process, record, event or view beyond the elements listed above. Freshness: the model's drift test (`tests/greenfield/test_commit_rule.py`, `tests/greenfield/test_plan_receipt.py`, `tests/greenfield/test_trace_review.py`, `tests/greenfield/test_characterize.py`, `tests/greenfield/test_evidence.py`, `tests/greenfield/test_reconcile.py`) runs inside the success check and its output is in the saved check file. If an element above is added, removed or renamed, the model, its view coverage and the saved check output are reconciled in the same commit, and otherwise the model needs no update because the elements keep their meaning.

## Capability reuse

Checked against the capability catalogue in agentic-capability-architecture-canonical (`reuse_candidates.yml` and `capability_registry.yml`):

- No catalogue entry fits, because this is a bug fix inside the existing commit rule, adding no capability
- What the work needs that no entry provides: edits to this repository's own files (`src/agentic_engineering_system/commit_rule.py`, `tests/greenfield/test_commit_rule.py`, `generated/docstring_wiki.md`, `docs/model/trace.yaml`, `wiki/index.md`); catalogue entries are cross-project capabilities, and none edits a repository's own source.

## Uncertainties

Material uncertainties. This one is the complete set; it is material because a file outside the list would
make the change exceed this plan's scope.

| Material uncertainty | Owner or resolving evidence |
| --- | --- |
| Whether the change needs files beyond the list below; if so it is out of scope for this plan | Resolved before editing: git diff --stat 8ce5a66c7 in the worktree: commit_rule.py, test_commit_rule.py, generated/docstring_wiki.md, wiki/index.md (one navigation line for the plan), docs/model/trace.yaml (reviewed_at re-read date); reach.py is committed separately under [Shaping aes-brownfield-docs] |

## Vertical and reset

One vertical over these files (and the saved check output, `docs/plans/commit-rule-root-relative-links.check.txt`):

- `src/agentic_engineering_system/commit_rule.py`
- `tests/greenfield/test_commit_rule.py`
- `generated/docstring_wiki.md`
- `docs/model/trace.yaml`
- `wiki/index.md`

The vertical delivers: aes commit check resolves a Markdown link starting with / against the repository root, then wiki/, so new pages a wiki links root-relatively count as reached. It is done when this holds: tests/greenfield/test_commit_rule.py::test_root_relative_links_resolve_against_the_repo_root_then_the_wiki_folder asserts a commit adding wiki/people/a.md (linked /people/a.md) and docs/b.md (linked /docs/b.md) is accepted while an unlinked page is still refused; ::test_a_shaping_commit_may_link_its_proposal_root_relatively asserts a [Shaping] commit whose wiki line links /proposals/<id>/plan.md is accepted as navigation; both fail before the fix and pass after; the rest of test_commit_rule.py passes.

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

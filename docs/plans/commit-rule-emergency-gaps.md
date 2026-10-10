---
schema_version: "1.0"
artifact_type: design_plan
id: commit-rule-emergency-gaps
plan_id: commit-rule-emergency-gaps
status: proposed
planning_path: requested
method_conformance_receipt: docs/plans/commit-rule-emergency-gaps.receipt.json
trace_review_criteria:
  - criterion_id: outcome
    expected_outcome: pass
goal:
  outcome: "An [Unplanned] commit whose Emergency line is a placeholder such as 'not an emergency.' is refused by the commit rule, and install_everywhere.py check reports an AES project whose .githooks has no commit-msg running aes commit check as unwired and install wraps it"
  canonical_example: "The vision 0df694a message ('Emergency: not an emergency. Routine vision work has no fitting commit label') is refused through the installed hook, while second-brain-mega 48c5eb9 ('Emergency: server finder refresh has failed every run since ...') is accepted."
  forbidden_substitutes: "claiming success from a check's last line or exit status alone; a change outside the listed files; a commit without the saved check output"
  boundaries: "only these files: src/agentic_engineering_system/commit_rule.py, tests/greenfield/test_commit_rule.py, proposals/aes-planning/rollout/install_everywhere.py, tests/rollout/test_install_everywhere.py, proposals/aes-planning/ROLLOUT.md; no irreversible action and no spend; Brian's request as quoted is the scope"
  done_when: "Observed through real git commits: each of the eight real placeholder messages is refused by the installed commit-msg hook with exit 1 and no commit is made; the real 48c5eb9 emergency message is accepted and makes exactly one commit; a throwaway repository with .aes/project.yaml and a pre-commit-only .githooks (as observation-to-action-metamodel has) is reported local and unwired, then after install a refused message stops the commit and the rule runs exactly once per commit, including in a checkout whose own commit-msg already runs it. These are asserted in tests/greenfield/test_commit_rule.py and tests/rollout/test_install_everywhere.py, which fail on the previous code; make check exit 0. The check's full output is committed as docs/plans/commit-rule-emergency-gaps.check.txt, and the commit is tagged [Goal commit-rule-emergency-gaps] with an Asked: line quoting the request."
  do_not_gate_on: "Brian's review of the plan page; work outside the listed files"
---

# Commit rule refuses placeholder Emergency lines and the installer stops calling hook-less AES projects wired

## When a run fails or surprises us

This procedure is separate from, and distinct from, the anticipated failure modes listed under Disproof:
it covers any failing or surprising run, including ones nobody anticipated. Preserve the failed run itself
(its full output saved next to the plan) and its trace id or command line. Before selecting a fix, read the
complete inputs, prompts, each tool call's arguments and results, intermediate stages and final output,
including the full check command and output and the changed files. Cite the observed divergence and classify
it as evidence absent, evidence returned but unused or contradicted, invalid expectation, or unresolved. An
unresolved diagnosis permits further investigation but cannot authorize a causal repair. Link the targeted
repair to a new traced verification run, and retain the original failed run. Review every failing or
surprising item and a sample of passes. Review completeness is judged separately from the run verdict: a
passing run does not show the review was complete. Criterion `outcome` covers the entire requested success check.

## Actor and result

**Actor:** Brian, who asked for this change.

**Request (verbatim):** Brian 2026-10-10 "Brian asked for this fix" (relayed by the parent session: recent [Unplanned] commits in vision and observation-to-action-metamodel got through for ordinary documentation work; find why and fix the root cause in agentic-engineering-system-canonical)

**Desired result:** An [Unplanned] commit whose Emergency line is a placeholder such as 'not an emergency.' is refused by the commit rule, and install_everywhere.py check reports an AES project whose .githooks has no commit-msg running aes commit check as unwired and install wraps it.

**Stable example:** The vision 0df694a message ('Emergency: not an emergency. Routine vision work has no fitting commit label') is refused through the installed hook, while second-brain-mega 48c5eb9 ('Emergency: server finder refresh has failed every run since ...') is accepted.

## Authority and non-goals

**Authority:** Brian asked for this change in his own repository; one agent makes it.

**Non-goals:** nothing outside the files listed under Vertical and reset. No irreversible action and no spend.

## Requirements

| Id | Requirement | Source | Check | Status |
| --- | --- | --- | --- | --- |
| R1 | An [Unplanned] commit whose Emergency line is a placeholder such as 'not an emergency.' is refused by the commit rule, and install_everywhere.py check reports an AES project whose .githooks has no commit-msg running aes commit check as unwired and install wraps it. | asked: Brian 2026-10-10 "Brian asked for this fix" (relayed by the parent session: recent [Unplanned] commits in vision and observation-to-action-metamodel got through for ordinary documentation work; find why and fix the root cause in agentic-engineering-system-canonical) | the success check under Success and disproof, its output saved as `docs/plans/commit-rule-emergency-gaps.check.txt` | planned, not yet run |
| R2 | Placeholder Emergency values (the eight real messages, dashes, tbd, an empty line) are refused | stated with the request | tests/greenfield/test_commit_rule.py::test_real_placeholder_emergency_messages_are_refused_and_a_real_emergency_is_accepted and ::test_placeholder_and_empty_emergency_values_are_refused | planned, not yet run |
| R3 | Whether a stated reason is a real emergency is prose meaning and is not judged by regex | stated with the request | only a closed placeholder list standing alone is refused; the same tests accept 'Emergency: no deploy has succeeded since 06:00' and the real 48c5eb9 emergency | planned, not yet run |
| R4 | An AES project with no commit-msg running the rule is reported unwired and wrapped without double runs, shown on a throwaway test repository shaped like observation-to-action-metamodel | stated with the request | tests/rollout/test_install_everywhere.py (both tests) | planned, not yet run |
| R5 | This plan adds no coordinated-work ceremony (one agent, one pull request, no work-unit graph or claims beyond the maintenance worktree) | stated with the request | script step 'git diff --name-only origin/main...HEAD' run before merge lists only the 5 listed files and this plan's docs/plans/commit-rule-emergency-gaps.* files | planned, not yet run |

Requirements the change's own claims imply are listed above as R2 onward.

## AES target

This repository is governed by an AES target (`.aes/target.yaml`). How R1 onward map to it:

- Target unchanged (no target delta, no new running things). Every requirement serves normative item AP-REQ-001 (the rule checks the tag against facts, including an Emergency trailer; the installer is how that rule runs in each repository) and success criterion SC-AP-001. Verification subjects: VS-AP-COMMIT-RULE (tests/greenfield/test_commit_rule.py) for R1-R3; for R4 the installer sits outside the governed roots, so its verification is the external check tests/rollout/test_install_everywhere.py; R5 is checked by the git diff script step. aes target validate --root . exit 0 (components=12 planned_artifacts=47 verification_subjects=16, every evidence requirement has a route); aes plan validate not run because no AES plan proposal changes the target.

## Success and disproof

**Success evidence:** Observed through real git commits: each of the eight real placeholder messages is refused by the installed commit-msg hook with exit 1 and no commit is made; the real 48c5eb9 emergency message is accepted and makes exactly one commit; a throwaway repository with .aes/project.yaml and a pre-commit-only .githooks (as observation-to-action-metamodel has) is reported local and unwired, then after install a refused message stops the commit and the rule runs exactly once per commit, including in a checkout whose own commit-msg already runs it. These are asserted in tests/greenfield/test_commit_rule.py and tests/rollout/test_install_everywhere.py, which fail on the previous code; make check exit 0.

**Trace review:** the run whose full trace is judged is the success check above, run once on the commit that makes the change; no model, agent or LLM pipeline runs under this plan. Where the trace lives: the check's complete output, with the exact command and its exit status, is saved as `docs/plans/commit-rule-emergency-gaps.check.txt` and committed with the change. What must be seen in it beyond the final result: the command ran against the files listed under Vertical and reset at that commit, each check or test it reports appears by name with its result and none is skipped, and the exit status matches; for each model element listed under System model, the output shows what that line says. Success and disproof are both judged from that file.

**Disproof:** Anticipated failure modes: any of the eight real messages is accepted, the real emergency is refused, the throwaway pre-commit-only AES repository is reported wired, or the rule runs twice for a checkout whose own commit-msg already runs it. Any other failing or surprising result is not one of these and goes through the separate procedure under 'When a run fails or surprises us' (diagnose from the full trace first; no causal repair on an unresolved diagnosis).

## System model

**System model:** `.aes/target.yaml`

**Model elements this change adds, changes or relies on, and what the saved check output must show of each:**

- Scope, views and reconciliation: `.aes/target.yaml` is this repository's own model, not a shared one. Its applicable source-linked views are `aes status` (one screen of components, artifacts and verification subjects with their evidence state) and the generated `AGENTS.md` projection; no view is omitted, because the change adds, renames or removes no element, so neither view's content changes except VS-AP-COMMIT-RULE's evidence state. Reconciliation in the same change: the pre-commit hook re-validates the model against the staged tree (`aes target validate`, `aes topology check`), `aes evidence record VS-AP-COMMIT-RULE` records the verification evidence at the change commit, and `aes status` is read afterwards to confirm model coverage (every planned artifact present), view coverage (VS-AP-COMMIT-RULE shown) and evidence (SUPPORTS) agree.
- Model entry point and freshness (.aes/target.yaml, this repository's own model, reached from wiki/index.md via AGENTS.md 'AES governs itself'): the pre-commit hook on the change commit must print 'every evidence requirement has a route' from aes target validate and pass aes topology check; the model is unchanged, so no view needs updating
- RU-AES-COMMIT-RULE with ART-SRC-COMMIT-RULE and ART-TEST-COMMIT-RULE (relied on, unchanged paths): the saved check output must list test_real_placeholder_emergency_messages_are_refused_and_a_real_emergency_is_accepted and test_placeholder_and_empty_emergency_values_are_refused as PASSED, with every other test_commit_rule.py test PASSED
- VS-AP-COMMIT-RULE (relied on, unchanged): aes evidence record VS-AP-COMMIT-RULE must print verdict SUPPORTS naming the change commit, and aes status must then show VS-AP-COMMIT-RULE as supported at that commit
- none -- install_everywhere.py lies outside the governed roots and has no target element; the saved check output must list both tests/rollout/test_install_everywhere.py tests as PASSED

## Capability reuse

Checked against the capability catalogue in agentic-capability-architecture-canonical (`reuse_candidates.yml` and `capability_registry.yml`):

- No catalogue entry fits, because reuse_candidates.yml and capability_registry.yml in agentic-capability-architecture-canonical list no commit-message policy check; the change repairs the existing AES commit rule (aes commit check) and its installer, which AES canonical already owns

## Uncertainties

| Uncertainty | Owner or resolving evidence |
| --- | --- |
| Whether the change needs files beyond the list below; if so it is out of scope for this plan | Resolved before editing: grep -n NO_EMERGENCY_RE src/agentic_engineering_system/commit_rule.py and grep -n is_aes_native proposals/aes-planning/rollout/install_everywhere.py: both checks live only in these files; git status --short lists exactly the 5 files |

## Vertical and reset

One vertical over these files (and the saved check output, `docs/plans/commit-rule-emergency-gaps.check.txt`):

- `src/agentic_engineering_system/commit_rule.py`
- `tests/greenfield/test_commit_rule.py`
- `proposals/aes-planning/rollout/install_everywhere.py`
- `tests/rollout/test_install_everywhere.py`
- `proposals/aes-planning/ROLLOUT.md`

The vertical delivers: An [Unplanned] commit whose Emergency line is a placeholder such as 'not an emergency.' is refused by the commit rule, and install_everywhere.py check reports an AES project whose .githooks has no commit-msg running aes commit check as unwired and install wraps it. It is done when this holds: Observed through real git commits: each of the eight real placeholder messages is refused by the installed commit-msg hook with exit 1 and no commit is made; the real 48c5eb9 emergency message is accepted and makes exactly one commit; a throwaway repository with .aes/project.yaml and a pre-commit-only .githooks (as observation-to-action-metamodel has) is reported local and unwired, then after install a refused message stops the commit and the rule runs exactly once per commit, including in a checkout whose own commit-msg already runs it. These are asserted in tests/greenfield/test_commit_rule.py and tests/rollout/test_install_everywhere.py, which fail on the previous code; make check exit 0.

Make the change, run the success check, commit. Reset: `git revert` of the commit. Not pursued: anything outside these files.

## Activation facts

No shared mechanism, no comparison, no LLM at the centre, no irreversible action or spend, and no claim to follow an external standard: a bounded change Brian asked for.

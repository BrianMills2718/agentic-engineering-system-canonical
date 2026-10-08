---
schema_version: "1.0"
artifact_type: design_plan
id: commit-rule-followups
plan_id: commit-rule-followups
status: proposed
planning_path: requested
method_conformance_receipt: proposals/commit-rule-followups/commit-rule-followups.receipt.json
goal:
  outcome: "The AES commit rule logs, for a [Goal <id>] commit whose plan was made by quick-adopt, whether the commit adds the plan's saved check output and stays inside the plan's file list, and it treats test setup files and scripts run by systemd units as running things that [Trivial] may not touch"
  canonical_example: "A [Goal fix-button-label] commit that changes a file not listed in the plan, or that has no docs/plans/fix-button-label.check.txt, is logged with a reason naming the file; a [Trivial] commit changing tests/conftest.py is refused as touching a running thing."
  forbidden_substitutes: "claiming success from a check's last line or exit status alone; a change outside the listed files; a commit without the saved check output"
  boundaries: "only these files: src/agentic_engineering_system/commit_rule.py, tests/greenfield/test_commit_rule.py, proposals/aes-planning/rollout/misuse_review.py; no irreversible action and no spend; Brian's request as quoted is the scope"
  done_when: "tests/greenfield/test_commit_rule.py makes real commits through the installed hook for each case (inside and outside the file list, with and without the check file, a conftest.py change tagged [Trivial]) and asserts the logged verdict and reason for each; aes evidence record VS-AP-COMMIT-RULE then records SUPPORTS. The check's full output is committed as proposals/commit-rule-followups/commit-rule-followups.check.txt, and the commit is tagged [Goal commit-rule-followups] with an Asked: line quoting the request."
  do_not_gate_on: "Brian's review of the plan page; work outside the listed files"
---

# Commit rule follow-ups: check quick-plan promises and widen what counts as running

## Actor and result

**Actor:** Brian, who asked for this change.

**Request (verbatim):** Brian 2026-10-07 "are we company planning complaint? if so give me the /goal text"

**Desired result:** The AES commit rule logs, for a [Goal <id>] commit whose plan was made by quick-adopt, whether the commit adds the plan's saved check output and stays inside the plan's file list, and it treats test setup files and scripts run by systemd units as running things that [Trivial] may not touch.

**Stable example:** A [Goal fix-button-label] commit that changes a file not listed in the plan, or that has no docs/plans/fix-button-label.check.txt, is logged with a reason naming the file; a [Trivial] commit changing tests/conftest.py is refused as touching a running thing.

## Authority and non-goals

**Authority:** Brian asked for this change in his own repository; one agent makes it.

**Non-goals:** nothing outside the files listed under Vertical and reset. No irreversible action and no spend.

## Success and disproof

**Success evidence:** tests/greenfield/test_commit_rule.py makes real commits through the installed hook for each case (inside and outside the file list, with and without the check file, a conftest.py change tagged [Trivial]) and asserts the logged verdict and reason for each; aes evidence record VS-AP-COMMIT-RULE then records SUPPORTS.

**Trace review:** the run whose full trace is judged is the success check above, run once on the commit that makes the change; no model, agent or LLM pipeline runs under this plan. Where the trace lives: the check's complete output, with the exact command and its exit status, is saved as `proposals/commit-rule-followups/commit-rule-followups.check.txt` and committed with the change. What must be seen in it beyond the final result: the command ran against the files listed under Vertical and reset at that commit, each check or test it reports appears by name with its result and none is skipped, and the exit status matches. Success and disproof are both judged from that file.

**Disproof:** Any of those commits is judged differently from the stated verdict, or the new checks block a commit while the rule is in observe mode.

## Uncertainties

| Uncertainty | Owner or resolving evidence |
| --- | --- |
| Whether the change needs files beyond the list below; if so it is out of scope for this plan | Resolved before editing: grep -n RUNNING_THING src/agentic_engineering_system/commit_rule.py shows the running-thing list lives only there (lines 91-96); the misuse review reads the same log (proposals/aes-planning/rollout/misuse_review.py) |

## Vertical and reset

One vertical over these files (and the saved check output, `proposals/commit-rule-followups/commit-rule-followups.check.txt`):

- `src/agentic_engineering_system/commit_rule.py`
- `tests/greenfield/test_commit_rule.py`
- `proposals/aes-planning/rollout/misuse_review.py`

The vertical delivers: The AES commit rule logs, for a [Goal <id>] commit whose plan was made by quick-adopt, whether the commit adds the plan's saved check output and stays inside the plan's file list, and it treats test setup files and scripts run by systemd units as running things that [Trivial] may not touch. It is done when this holds: tests/greenfield/test_commit_rule.py makes real commits through the installed hook for each case (inside and outside the file list, with and without the check file, a conftest.py change tagged [Trivial]) and asserts the logged verdict and reason for each; aes evidence record VS-AP-COMMIT-RULE then records SUPPORTS.

Make the change, run the success check, commit. Reset: `git revert` of the commit. Not pursued: anything outside these files.

## Activation facts

No shared mechanism, no comparison, no LLM at the centre, no irreversible action or spend: a bounded change Brian asked for.

---
schema_version: "1.0"
artifact_type: design_plan
id: commit-tag-case
plan_id: commit-tag-case
status: proposed
planning_path: requested
method_conformance_receipt: proposals/commit-tag-case/commit-tag-case.receipt.json
goal:
  outcome: "A commit tagged [Goal PATH-brent-v1-2026-10-02] or [Shaping Some-Plan] is read as a plan tag and judged against that plan, instead of being refused as having no tag"
  canonical_example: "brent-chatgpt's [Goal PATH-brent-v1-2026-10-02] commits, refused on 2026-10-07 as 'no tag', are judged as Goal tags: refused only by the observe-only plan-adoption check when that plan is not adopted."
  forbidden_substitutes: "claiming success from a check's last line or exit status alone; a change outside the listed files; a commit without the saved check output"
  boundaries: "only these files: src/agentic_engineering_system/commit_rule.py, tests/greenfield/test_commit_rule.py; no irreversible action and no spend; Brian's request as quoted is the scope"
  done_when: "tests/greenfield/test_commit_rule.py commits [Goal Upper-Case-Plan] and [Shaping Upper-Case-Plan] through the installed hook and asserts the logged tag is Goal/Shaping, never none; the full commit-rule test file passes. The check's full output is committed as proposals/commit-tag-case/commit-tag-case.check.txt, and the commit is tagged [Goal commit-tag-case] with an Asked: line quoting the request."
  do_not_gate_on: "Brian's review of the plan page; work outside the listed files"
---

# Commit rule reads plan names with capital letters as plan tags

## Actor and result

**Actor:** Brian, who asked for this change.

**Request (verbatim):** Brian 2026-10-08 "ok do that" (prepare the 10-09 enforce decision from the would-be-blocked commits)

**Desired result:** A commit tagged [Goal PATH-brent-v1-2026-10-02] or [Shaping Some-Plan] is read as a plan tag and judged against that plan, instead of being refused as having no tag.

**Stable example:** brent-chatgpt's [Goal PATH-brent-v1-2026-10-02] commits, refused on 2026-10-07 as 'no tag', are judged as Goal tags: refused only by the observe-only plan-adoption check when that plan is not adopted.

## Authority and non-goals

**Authority:** Brian asked for this change in his own repository; one agent makes it.

**Non-goals:** nothing outside the files listed under Vertical and reset. No irreversible action and no spend.

## Success and disproof

**Success evidence:** tests/greenfield/test_commit_rule.py commits [Goal Upper-Case-Plan] and [Shaping Upper-Case-Plan] through the installed hook and asserts the logged tag is Goal/Shaping, never none; the full commit-rule test file passes.

**Trace review:** the run whose full trace is judged is the success check above, run once on the commit that makes the change; no model, agent or LLM pipeline runs under this plan. Where the trace lives: the check's complete output, with the exact command and its exit status, is saved as `proposals/commit-tag-case/commit-tag-case.check.txt` and committed with the change. What must be seen in it beyond the final result: the command ran against the files listed under Vertical and reset at that commit, each check or test it reports appears by name with its result and none is skipped, and the exit status matches. Success and disproof are both judged from that file.

**Disproof:** A commit whose first line starts with [Goal X] with capital letters in X is still logged with tag none.

## Uncertainties

| Uncertainty | Owner or resolving evidence |
| --- | --- |
| Whether the change needs files beyond the list below; if so it is out of scope for this plan | Resolved before editing: grep -n TAG_RE src/agentic_engineering_system/commit_rule.py: the pattern is defined once (line 81) and used only by the rule. This is the only material uncertainty: the change is one regular expression and its tests, so no other unknown affects the outcome |

## Vertical and reset

One vertical over these files (and the saved check output, `proposals/commit-tag-case/commit-tag-case.check.txt`):

- `src/agentic_engineering_system/commit_rule.py`
- `tests/greenfield/test_commit_rule.py`

The vertical delivers: A commit tagged [Goal PATH-brent-v1-2026-10-02] or [Shaping Some-Plan] is read as a plan tag and judged against that plan, instead of being refused as having no tag. It is done when this holds: tests/greenfield/test_commit_rule.py commits [Goal Upper-Case-Plan] and [Shaping Upper-Case-Plan] through the installed hook and asserts the logged tag is Goal/Shaping, never none; the full commit-rule test file passes.

Make the change, run the success check, commit. Reset: `git revert` of the commit. Not pursued: anything outside these files.

## Activation facts

No shared mechanism, no comparison, no LLM at the centre, no irreversible action or spend: a bounded change Brian asked for.

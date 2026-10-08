---
schema_version: "1.0"
artifact_type: design_plan
id: commit-rule-notes-report
plan_id: commit-rule-notes-report
status: proposed
planning_path: requested
method_conformance_receipt: proposals/commit-rule-notes-report/commit-rule-notes-report.receipt.json
goal:
  outcome: "The daily commit-rule report counts, per day and repository, [Goal] commits whose quick-plan notes say the saved check output is missing or files fall outside the plan's list, records the counts in its per-day line, and opens or updates the keyed concern aes-quick-plan-drift naming those commits when any occur"
  canonical_example: "A day whose logs hold a [Goal fix-label] commit noted 'files outside the plan's list: notes.md' produces a per-day line with quick_plan_problems 1 and a concern listing fix-label, notes.md and the repository; a day with only clean notes produces quick_plan_problems 0 and no concern."
  forbidden_substitutes: "claiming success from a check's last line or exit status alone; a change outside the listed files; a commit without the saved check output"
  boundaries: "only these files: proposals/aes-planning/rollout/daily_report.py, tests/rollout/test_daily_report.py; no irreversible action and no spend; Brian's request as quoted is the scope"
  done_when: "tests/rollout/test_daily_report.py builds observe logs with clean, missing-check and outside-list notes, runs the report's counting function on them, and asserts the per-day counts and the concern text naming each problem commit; then the real report run on the machine's logs prints the quick-plan line. The check's full output is committed as proposals/commit-rule-notes-report/commit-rule-notes-report.check.txt, and the commit is tagged [Goal commit-rule-notes-report] with an Asked: line quoting the request."
  do_not_gate_on: "Brian's review of the plan page; work outside the listed files"
---

# The daily commit-rule report reads the quick-plan notes and raises problems

## Actor and result

**Actor:** Brian, who asked for this change.

**Request (verbatim):** Brian 2026-10-08 "give me t h new /goal text" (next step: AES issue #279, quick-plan notes nothing reads)

**Desired result:** The daily commit-rule report counts, per day and repository, [Goal] commits whose quick-plan notes say the saved check output is missing or files fall outside the plan's list, records the counts in its per-day line, and opens or updates the keyed concern aes-quick-plan-drift naming those commits when any occur.

**Stable example:** A day whose logs hold a [Goal fix-label] commit noted 'files outside the plan's list: notes.md' produces a per-day line with quick_plan_problems 1 and a concern listing fix-label, notes.md and the repository; a day with only clean notes produces quick_plan_problems 0 and no concern.

## Authority and non-goals

**Authority:** Brian asked for this change in his own repository; one agent makes it.

**Non-goals:** nothing outside the files listed under Vertical and reset. No irreversible action and no spend.

## Success and disproof

**Success evidence:** tests/rollout/test_daily_report.py builds observe logs with clean, missing-check and outside-list notes, runs the report's counting function on them, and asserts the per-day counts and the concern text naming each problem commit; then the real report run on the machine's logs prints the quick-plan line.

**Trace review:** the run whose full trace is judged is the success check above, run once on the commit that makes the change; no model, agent or LLM pipeline runs under this plan. Where the trace lives: the check's complete output, with the exact command and its exit status, is saved as `proposals/commit-rule-notes-report/commit-rule-notes-report.check.txt` and committed with the change. What must be seen in it beyond the final result: the command ran against the files listed under Vertical and reset at that commit, each check or test it reports appears by name with its result and none is skipped, and the exit status matches. Success and disproof are both judged from that file.

**Disproof:** A logged note about missing check output or files outside the list does not appear in the day's counts or concern, or a day of clean notes opens a concern.

## Uncertainties

| Uncertainty | Owner or resolving evidence |
| --- | --- |
| Whether the change needs files beyond the list below; if so it is out of scope for this plan | Resolved before editing: grep -n 'notes' proposals/aes-planning/rollout/daily_report.py finds no reader today; the per-day line is written in main() (the counts block near line 125) and concerns go through concern() at line 45. This is the only material uncertainty: the change is one function and its use in main(), plus a test, so no other unknown affects the outcome |

## Vertical and reset

One vertical over these files (and the saved check output, `proposals/commit-rule-notes-report/commit-rule-notes-report.check.txt`):

- `proposals/aes-planning/rollout/daily_report.py`
- `tests/rollout/test_daily_report.py`

The vertical delivers: The daily commit-rule report counts, per day and repository, [Goal] commits whose quick-plan notes say the saved check output is missing or files fall outside the plan's list, records the counts in its per-day line, and opens or updates the keyed concern aes-quick-plan-drift naming those commits when any occur. It is done when this holds: tests/rollout/test_daily_report.py builds observe logs with clean, missing-check and outside-list notes, runs the report's counting function on them, and asserts the per-day counts and the concern text naming each problem commit; then the real report run on the machine's logs prints the quick-plan line.

Make the change, run the success check, commit. Reset: `git revert` of the commit. Not pursued: anything outside these files.

## Activation facts

No shared mechanism, no comparison, no LLM at the centre, no irreversible action or spend: a bounded change Brian asked for.

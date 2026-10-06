# Goal: AES planning

Goal document for the adopted plan `proposals/aes-planning/README.md` (Company Planning receipt `method-conformance-receipt.json`, adopted 2026-10-06, route coordinated). Hand-written with the `authoring-goals` skill as the prototype for work unit P2, which will make the adoption gate write this file itself. The plan is the authority for design and work units; this file holds only what the goal loop needs.

**Execution profile:** continuous-coordinated

## Mission and canonical example

Real implementation work in Brian's repositories lands only under an adopted, AES-accepted plan; trivial work still flows, decided by measured facts about the change; adopting a plan writes its `/goal` text.

Canonical example: in AES canonical with the new commit rule installed, a staged change that adds a Dockerfile and edits a compose file, committed as `[Unplanned] add worker tools` with no `Emergency:` trailer, is refused with a message naming the running-thing files and the `[Plan #N]` route; the same change committed as `[Plan #N] U2: worker tools`, where plan N has an adopted receipt, is accepted; a one-line README typo fix committed as `[Trivial] fix typo` is accepted.

Forbidden substitutes: a hook that only checks the tag text; a unit test of the rule function without the installed hook refusing a real staged commit; a replay listing produced without running the real rule over the real commits; a goal file written by hand for any plan other than this one when claiming P2.

## Boundaries

- In scope: company-planning (`plugins/company-planning/contracts/method-conformance`, `scripts/method_conformance`, `tests/test_method_conformance.py`) for P1 and P2, only after the plan-48 claim is closed or its owner agrees; AES canonical (`aes plan accept`, `meta-process.yaml`, the commit rule) for P3–P6; the hook installer for observe-mode rollout.
- Out of scope: changing any policy text in project-meta; a Stop hook; migrating repositories other than AES canonical, whygame5, DIGIMON and process tracing.
- Enforce mode is switched on per repository only after its observe week shows a false-refusal rate at or under 1 in 5, quoted in the switching commit. Above trivial model cost (5 dollars a plan, 20 a week) is a `needs-reply` to Brian.

## Increments (smallest vertical first)

1. P4 in observe mode in AES canonical, with the 300-commit replay of AES canonical and personal-vps (retires the trivial-threshold uncertainty).
2. P3: `aes plan accept` refuses without a fresh adopted receipt.
3. P1, P2 in company-planning (after the plan-48 owner's reply or claim closure).
4. P5: hive-hardening through the gate, producing its receipt and goal file.
5. P6: enforce in AES canonical after its observe week; then repository by repository.

## Acceptance checks

- The installed commit-msg hook in AES canonical, in observe mode, logs the three canonical-example commits with the expected verdicts (would-refuse, accept, accept); exit status and log line quoted.
- Replay output lists personal-vps #87's commit as would-refuse and a README typo commit as accept, with total counts.
- `aes plan accept` on a proposal without a receipt exits non-zero with the reason; with a fresh adopted receipt exits 0; tests pass with counts.
- company-planning `tests/test_method_conformance.py` passes with counts after P1/P2; adopting a plan in a repository with `.aes/` writes `<plan>.goal.md`.
- hive-hardening's adoption decision reads `adopted`.

## Stops

- No progress: after 3 attempts on the same reproduced blocker with no new evidence or safe next action, stop as blocked and report blocker, owner, resume event.
- Revalidate after three increments or about four hours: report outcome, enabling and process progress, and whether to keep, replace or clear this goal.

## Owners and reporting

| Lane | Owner | Next expected event | Deadline | If missing |
|---|---|---|---|---|
| AES pieces (P3–P6) | code-71 | P4 observe install commit | PT4H from goal start | one probe of the session and claims, then block with resume event |
| company-planning P1/P2 | code-71, after plan-48 owner | plan-48 owner reply or claim closure | PT24H from goal start | one claims probe; if still open, reassign P1/P2 to after its expiry (2026-10-07 17:57 UTC) |

<!-- goal-authority-reversion:v1:start -->
```yaml
schema_version: "1.1"
owner: "coordinator:code-71"
receiver: "coordinator:recovery"
transfer:
  trigger: "owner_runtime_absent_after_missed_event_and_probe"
reporting:
  event: "work-unit completion receipt"
  deadline: "PT4H"
  one_probe_transition: "reassign"
non_gating_utility_review:
  broad_cycle_limit: 2
  on_limit: "compare_direct_route_and_merge_or_defer"
  later_review: "exact_counterexample_only_unless_scope_expands"
```
<!-- goal-authority-reversion:v1:end -->

## Non-gating next actions (outside the goal)

- Brian looks at the plan's review page; his feedback feeds the next increment but nothing waits on it.
- Moving every other repository into AES.

## /goal launcher

```text
Goal: real implementation work in Brian's repositories lands only under an adopted plan; trivial work is decided by measured facts; adopting a plan writes its /goal text. Read and follow proposals/aes-planning/aes-planning.goal.md in agentic-engineering-system-canonical (branch shaping/aes-planning).
Profile: continuous-coordinated.
Canonical example: in AES canonical, "[Unplanned] add worker tools" adding a Dockerfile with no Emergency trailer is refused naming the running-thing files; the same change as "[Plan #N] ..." with an adopted receipt is accepted; "[Trivial] fix typo" on one README line is accepted.
Forbidden substitutes: a tag-text-only check; a unit test without the installed hook refusing a real staged commit; a replay not run with the real rule over real commits.
Boundaries: company-planning files only after the plan-48 claim closes or its owner agrees; no policy-text edits in project-meta; enforce mode per repository only after an observe week with false refusals at or under 1 in 5; model cost above 5 dollars a plan is a needs-reply to Brian.
Done when: the installed hook in AES canonical gives those three verdicts (quote output and exit codes); the replay lists personal-vps #87 as would-refuse with counts; aes plan accept refuses without and accepts with a fresh adopted receipt (tests with counts); company-planning tests pass and adoption writes the goal file; hive-hardening's adoption decision reads adopted.
Stop as blocked only after 3 attempts on the same reproduced blocker produce no new evidence or safe next action; report the blocker, owner, and resume event. A stop at a boundary above (plan-48 claim still open, enforce-mode threshold not met) is a correct terminal when reported with the request made. Do not gate on: Brian's review of the plan page, other repositories' migration, the observe week's elapsed time beyond AES canonical.
Revalidate after three increments or about four hours. Report outcome/enabling/process progress and whether to retain, replace, or clear this goal. If it is misaligned, stop substantive execution and return control.
```

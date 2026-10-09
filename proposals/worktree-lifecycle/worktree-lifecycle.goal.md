# Goal: consistent worktree creation and recoverable closeout

Authored through the authoring-goals contract from Brian's active /goal and the adopted [plan](PLAN.md) (sha256 `02cf7f114beb6e342da0498e467144b4bdab702238a13f2aeb11cc0fbb5e8a48`). This file owns mission, loop boundaries and the exact launch condition. The native PM execution cursor will own current slice/progress; the plan owns design, ownership and acceptance. There is no independent progress diary.

The native adoption helper's default generated goal is replaced under the explicit user authority: that renderer ignores the plan's `goal.transfer_trigger: explicit_handoff` and emits automatic recovery transfer. This authored contract preserves the requested explicit handoff rule. The native receipt and plan bytes are unchanged.

**Execution profile:** continuous-release

<!-- goal-authority-reversion:v1:start -->
```yaml
schema_version: "1.1"
owner: "coordinator:primary"
receiver: "coordinator:explicit-successor"
transfer:
  trigger: "explicit_handoff"
reporting:
  event: "slice verification or terminal blocker receipt"
  deadline: "PT30M"
  one_probe_transition: "block"
non_gating_utility_review:
  broad_cycle_limit: 2
  on_limit: "compare_direct_route_and_merge_or_defer"
  later_review: "exact_counterexample_only_unless_scope_expands"
```
<!-- goal-authority-reversion:v1:end -->

## Canonical example

A real governed task creates `<repo>/worktrees/<branch>`, makes and verifies its change, preserves the exact work on a verified remote recovery object, and closes its folder, local branch and claim together through public Make commands. Active, uncertain and service-dependent work is retained with a reason, responsible owner and exact reassessment event.

## Authority and next event

Owner: native coordinator `codex:01a11e1e-21f8-7f22-a467-a25b56fffe8c`; one sequential implementing writer, with no child dispatch. The next event is the PM discovery slice's accepted verification receipt, reported within PT30M of that slice's admission. A missed event gets one fresh owner/claim probe, then blocks dependent mutation; it never transfers custody. A successor requires an explicit handoff naming owner, retained paths/refs and exact resume event.

## /goal launcher

```text
/goal Make worktree creation and closeout consistent across ~/code, without losing work or interrupting services. Profile: continuous-release. Follow the committed worktree-lifecycle plan at proposals/worktree-lifecycle/PLAN.md (adopted bytes sha256:02cf7f114beb6e342da0498e467144b4bdab702238a13f2aeb11cc0fbb5e8a48). First resolve its adoption evidence and navigation gaps, validate and adopt it through Company Planning, and establish one durable progress authority. Refresh the inventory and relevant claims, then execute its four slices: complete discovery, guarded creation and closeout, installed-tool proof, and individual legacy dispositions. Use sanctioned claimed lanes; preserve other writers, ignored/uncommitted data, unique history and service dependencies. Transfer ownership only through explicit handoff. Canonical example: a real task creates <repo>/worktrees/<branch>, finishes and closes its folder, local branch and claim together, with exact remote recovery verified. Done when full placement, inventory, preservation, interrupted-closeout, sweep-failure and real-canary traces prove correct paths, complete membership, visible errors and recoverable closure; every baseline member is closed with evidence or retained with a reason, responsible owner and exact reassessment event; all task-created lanes are closed or durably handed off. Report source revisions, trace locations and actual before/after states. Forbidden substitutes: fewer folders, expired claims, clean status, fixture-only success or a green timer. Stop as blocked only after three consecutive turns reproduce the same blocker with no new evidence or safe next action; report its owner, exact resume event and any specific missing authority/access. Never cross irreversible deletion, private-publication or new-spend boundaries without authorization. Do not gate on zero worktrees, hosted CI, benchmarks, unrelated writers finishing or approval already granted by standing policy. Revalidate strategy after three substantive increments, three process-only increments or four hours.
```

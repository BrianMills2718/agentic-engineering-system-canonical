---
description: The purpose, ownership and evidence limits of AES feedback and policy
status: current
---

# Feedback and policy

AES includes the feedback loop and the policy layer alongside Lockstep. Their purpose is to turn observations and corrections into changes whose implementation and later behavior can be inspected. Collecting reports is an input to that purpose, not evidence that the correction has taken effect.

Source: Brian's definition of AES recorded in [CLAUDE.md](../../CLAUDE.md), the [system boundary](SYSTEM_BOUNDARY.md), and the retained [feedback operator contract](../../scripts/learning_loop/systemd/README.md). This page describes existing intent and machinery; it does not authorize new automation or introduce a new policy gate.

## The complete path

| Stage | What it establishes | Owning implementation or record |
| --- | --- | --- |
| Correction or observation | What someone said or what happened, with source and occurrence time | `collect_feedback.py`, `transcripts.py`, `records.py`, `subagents.py` |
| Evidence qualification | Whether references resolve, identify independent observations and support this particular claim | `evidence.py`, `relation_check.py` |
| Analysis | Which records describe a recurring problem and which proposed change they support | `problems.py`, `licences.py`; a licence is not proof of implementation |
| Disposition | Implement, identify existing enforcement, reject, defer or escalate with a reason | `fix_owner.py`; a closed issue alone is insufficient |
| Enforcement | A concrete changed instruction, check or control, with revision, effective time and verification | The owning repository and an explicit enforcement receipt; `effects.py` reads that receipt |
| Follow-up | Whether independently observed failures recur after that boundary | `effects.py` and `problems.py`; retained evidence determines the scope of the conclusion |

The [operator guide](../../scripts/learning_loop/systemd/README.md) explains commands, outputs and recovery. Transcript-derived evidence and feedback reports belong in the private store described there; this public architecture does not reproduce their contents. Full traces and parent-executed checks distinguish observed outcomes from an agent's own assertion of success.

## Policy is distinct from its machinery

Policy says which behavior is required, when and why. A hook, checker, timer or agent is a mechanism that may implement or observe it. The presence of that mechanism does not establish coverage of every relevant path. [The rules register](../rules/register.yaml) records enforcement status, mechanism and feedback path; [its generated page](../rules/RULES.md) distinguishes advisory, checked, partially enforced and enforced rules.

AES owns `scripts/learning_loop`, `scripts/rules` and the register in `docs/rules`. Brian's shared agent instructions and their source records live in code2-workspace `agents/`; client-native hooks and skills have their own owning sources. Changes belong at those sources, with the register describing the resulting coverage. This register currently contains one advisory rule and a legacy disposition manifest; it is not an inventory proving coverage of all shared instructions.

A blocking control should offer a runnable recovery path or an explicit human escalation boundary, as the [system boundary](SYSTEM_BOUNDARY.md) requires. Feedback about a control should remain attributable to that control rather than becoming an unexplained addition to general instructions.

## Observed limits, 2026-11-13

Read-only local inspection on this date found:

- Five feedback timers: collector and labels were enabled/active; problems, fix-owner and effects were disabled/inactive. This confirms scheduling state, not end-to-end improvement.
- The latest retained collector service result was `timeout`, exit status `143`, at 06:09:03 America/New_York; labels reported success, status `0`, at 06:15:35. No journal entries were returned by the bounded journal query. The latest completed collector run receipt was dated November 12.
- Retained analysis and effects outputs stopped on October 12. There was one effects file with 50 rows across 10 distinct rule identifiers. These are historical monitoring observations, not a current effect measurement.
- A read-only call to `policies.check(30)` returned zero policies and zero gaps. Its defaults still read the old workspace bootstrap path and discover only inline policy identifiers. A zero-gap result over zero discovered policies establishes no coverage of today's shared instructions.

Reproduce scheduling and service inspection with `systemctl --user show feedback-{collector,labels,problems,fix-owner,effects}.timer -p Id -p ActiveState -p UnitFileState -p LastTriggerUSec` and `systemctl --user show feedback-collector.service feedback-labels.service -p Id -p Result -p ExecMainStatus -p ExecMainExitTimestamp`. The operator guide names the private output store. These observations are dated and will need fresh inspection before an operational claim.

`effects.py` requires a revision-bound receipt, separates unknown timestamps, and excludes restatements of pre-fix incidents. Those are useful evidence boundaries. Its before/after sighting counts do not include comparable opportunity counts or establish observation completeness. Zero recorded recurrence therefore does not by itself demonstrate a reduced failure rate; a later recurrence can disprove a prevention claim without proving that the change provided no benefit.

The [open-questions ledger](../../wiki/open-questions.md) tracks the stopped repair stages, collector reliability, policy discovery and effect-evidence gaps. This page does not resolve them by describing the intended path.

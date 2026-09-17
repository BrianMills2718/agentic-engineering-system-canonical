# Fluid Governance selective-salvage review

Status: research synthesis; candidate dispositions only. This document does not
adopt an implementation, transfer authority, or change the canonical AES system
boundary.

## Review question

Which ideas, if any, should the canonical Agentic Engineering System salvage
from the dormant Fluid Governance lineage without importing its architecture or
creating a second execution-governance authority?

## Review basis

- Canonical AES revision reviewed:
  `BrianMills2718/agentic-engineering-system-canonical@735d2e84c224c3ae672f5509aa5c1702c68eaeec`.
- Fluid Governance source reviewed:
  `BrianMills2718/frame-club-governance-system@9b452ba293acf1319a08fb1d843f58715137ef90`.
- Captured: 2026-09-16.
- Evidence inspected: `README.md`, `fluid_governance/models.py`,
  `fluid_governance/governor.py`, `fluid_governance/engine.py`,
  `tests/test_governor.py`, and preserved run artifacts.
- Freshness boundary: conclusions describe those exact revisions. Any later
  implementation or adoption decision requires comparison with the then-current
  canonical boundary and incumbent capability owners.

## Recommendation

Selectively salvage two ideas:

1. **Typed transition decisions.** Represent an execution-control decision as
   an explicit action, target, rationale, and affected work rather than hiding
   recovery in prose or control flow.
2. **Append-only execution receipts.** Retain the observed stage output,
   decision inputs, transition decision, cost/errors, and resulting state so a
   block, recovery, and later allowance can be inspected as one evidence chain.

Do not adopt the Fluid Governance engine, its six-phase cycle, its global
governor role, or its model-reported heuristic metrics as AES architecture.

## Candidate dispositions

| Fluid Governance idea | Candidate disposition | AES fit | Boundary |
| --- | --- | --- | --- |
| Explicit transition actions (`continue`, `repeat`, `regress`, `branch`, `restart`) | salvage semantics | Supports AES-POL-003 recovery and AES-DOGFOOD-002 enforced transitions | Derive an AES-native vocabulary; do not copy the enum unchanged |
| Per-phase outputs plus decision/metric history in the run result | adapt | Supports AES-EVID-001 append-only observations and replayable dogfood evidence | Store observed facts and provenance; distinguish them from model estimates |
| Work-dependent cycle selection | research candidate | Could eventually vary checks inside an execution stage | Must not skip required target/current/gap/evidence reconciliation |
| `scope -> fracture -> diverge -> challenge -> converge -> reflect` | not applicable as AES lifecycle | A problem-solving workflow, not the canonical engineering lifecycle | Company Planning and Enforced Planning retain their declared roles |
| One global governor controlling the cycle | reject | Would collapse or duplicate component authority | AES-SYS-002 and AES-PLAN-002 require authority-preserving composition |
| Confidence delta, contradiction density, progress velocity, and novelty as routing signals | unresolved / evidence source only | May be useful experimental observations | They are model-reported proxies and are not calibrated control evidence |
| Generated Frame Club applications | historical | Evidence of the lineage's experiments | Not canonical AES implementation material |

## Concrete AES-shaped example

A policy control blocks an execution step. Instead of returning only
`blocked`, the execution evidence records:

```text
BLOCK
  observed_control_state: fail
  reason: required verification evidence is absent
  recovery_action: return_to_verification
  recovery_owner: current execution lane
  recovery_evidence: <stable evidence reference>

RECOVER_TO verification
  action_taken: run the required counterfactual check
  result: expected failure observed

ALLOW
  observed_control_state: pass
  basis: <stable evidence reference>
```

This is a candidate shape, not a new contract. Company Planning should derive
the required transition and evidence topology for the first vertical; ACA
should resolve any reusable transition/receipt capability; Enforced Planning
remains the execution-governance incumbent unless evidence supports a different
disposition.

## Evidence and limitations

Observed:

- Fluid Governance has typed phase outputs and governor decisions.
- Its engine records each phase output, computed metrics, the resulting
  decision, cost, errors, and transition counts in the run result.
- Its governor can repeat a phase, return to an earlier phase, replay weak work
  units on a branch, or restart after a bounded failure.
- The focused governor tests pass (`PYTHONPATH=. pytest -q
  tests/test_governor.py`: 3 passed).
- Preserved artifacts include both a 39-transition passing run with eight
  regressions and a 36-transition aborted run with eight regressions.

Limitations:

- The three focused tests demonstrate selected routing branches, not calibration
  or end-to-end recovery correctness.
- No reviewed evidence establishes that the model-reported confidence,
  novelty, contradiction, or progress values predict delivery quality.
- The governor can finalize a failed reflection after one prior regression or
  when its alignment score crosses a configured threshold. That behavior is
  incompatible with treating an uncorrected failure as conformance.
- The preserved runs show that recovery loops occurred; they do not prove that
  the chosen regressions were necessary, sufficient, or cost-effective.

## Adoption test

The cheapest decision-ready test is to replay one authentic AES policy block
and recovery through a minimal transition receipt. The candidate is useful if
the receipt makes all of the following directly inspectable without inventing a
second authority:

1. the observed state that caused the block;
2. the responsible control and its evidence;
3. the runnable recovery action and destination;
4. the evidence produced by recovery;
5. the subsequent allow, continued block, escalation, or stop decision; and
6. the immutable linkage between those events.

Reject or revise the candidate if it merely records self-reported scores,
duplicates Enforced Planning state, or allows an unresolved failure to appear
green.

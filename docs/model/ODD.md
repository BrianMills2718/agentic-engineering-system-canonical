---
description: AES canonical's system model in prose -- the plan, target, evidence and reconcile loop -- with its checked trace file
---

# AES canonical: system model

This page explains the governance loop AES v0.2 runs (Decision 0010). The checked
version, with one owner file, tests and decision records per rule, is
[trace.yaml](trace.yaml). Each rule's full text lives in its owner's docstring and in
[`.aes/target.yaml`](../../.aes/target.yaml); this page and the trace only point at it.

## One example, start to finish

An agent changes `src/agentic_engineering_system/evidence.py` and commits it.

1. **Reconcile.** `aes status` characterizes HEAD (every governed file's blob, every
   Python symbol), compares it with the planned artifacts in the target, and reports
   drift: a renamed public function in `evidence.py` is drift (`RULE-DRIFT-DETECTED`).
2. **Evidence.** The test observation recorded last week named `evidence.py` as a
   dependency path. Because that file changed after the observed commit, the
   observation is now stale and the criterion it supported goes back to a gap
   (`RULE-DEPENDENCY-CHANGE-STALES`, Decision 0008 section 3). A new run that passes
   one of three required inputs leaves the criterion INSUFFICIENT, not green
   (`RULE-INSUFFICIENT-NOT-GREEN`).
3. **Change the target.** To plan new artifacts the agent writes a proposal and runs
   `aes plan accept`; work that runs must carry a trace-review requirement
   (`RULE-TRACE-REVIEW-DECLARED`).

## Things (entities)

| ID | What it is | Where it lives |
|---|---|---|
| ENT-TARGET | outcomes, normative items, criteria, planned artifacts, verification subjects | `.aes/target.yaml` |
| ENT-PROPOSAL | a target delta plus the gaps it closes | a proposal file given to `aes plan` |
| ENT-OBSERVATION | append-only evidence bound to a revision and its dependency paths | `.aes/observations/` |
| ENT-CHARACTERIZATION | what HEAD contains under the governed roots | computed by `aes characterize` |

## Processes

| ID | Trigger | Rules it enforces |
|---|---|---|
| PROC-PLAN-ACCEPT | `aes plan validate` / `accept` | RULE-TRACE-REVIEW-DECLARED |
| PROC-RECONCILE | `aes status` / `aes reconcile` | RULE-DRIFT-DETECTED, RULE-INSUFFICIENT-NOT-GREEN, RULE-DEPENDENCY-CHANGE-STALES |

## Gaps in this model

- **G1.** Not modelled: the v0.1 line (Plan 002), the `repository_context` package,
  `aes adopt` legacy baselines, the Company Planning profile files under
  `docs/architecture/`, and the vendored `enforced_planning/` package.
- **G2.** Two rules cite no decision record: the trace-review rule comes from
  `TR-REQ-001`, recorded in `.aes/target.yaml` but never as a decision record;
  `RULE-INSUFFICIENT-NOT-GREEN` comes from AES-POL-002 in
  [SYSTEM_BOUNDARY.md](../architecture/SYSTEM_BOUNDARY.md).

The commit rule (commit tags, plan adoption per commit) and the plan-receipt check on
`aes plan accept` were removed on 2026-10-14 at Brian's request (2026-10-13: "turn off all
the enforcement"); behavior changes now go through OpenSpec in `~/code2`.

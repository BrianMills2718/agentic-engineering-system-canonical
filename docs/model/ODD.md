---
description: AES canonical's system model in prose -- the commit, plan, target, evidence and reconcile loop -- with its checked trace file
---

# AES canonical: system model

This page explains the governance loop AES v0.2 runs (Decision 0010). The checked
version, with one owner file, tests and decision records per rule, is
[trace.yaml](trace.yaml). Each rule's full text lives in its owner's docstring and in
[`.aes/target.yaml`](../../.aes/target.yaml); this page and the trace only point at it.

## One example, start to finish

An agent changes `src/agentic_engineering_system/evidence.py` under an adopted plan.

1. **Commit.** The commit-msg hook runs `aes commit check`. The first line says
   `[Goal <id>]`; the rule finds the plan, reads its adoption decision, and accepts
   only if the plan and receipt bytes still match what was adopted
   (`RULE-PLAN-ADOPTED-FOR-COMMIT`). A typo fix could use `[Trivial]`, but only if the
   measured change is small and touches nothing that runs (`RULE-COMMIT-TAG`).
2. **Reconcile.** `aes status` characterizes HEAD (every governed file's blob, every
   Python symbol), compares it with the planned artifacts in the target, and reports
   drift: a renamed public function in `evidence.py` is drift (`RULE-DRIFT-DETECTED`).
3. **Evidence.** The test observation recorded last week named `evidence.py` as a
   dependency path. Because that file changed after the observed commit, the
   observation is now stale and the criterion it supported goes back to a gap
   (`RULE-DEPENDENCY-CHANGE-STALES`, Decision 0008 section 3). A new run that passes
   one of three required inputs leaves the criterion INSUFFICIENT, not green
   (`RULE-INSUFFICIENT-NOT-GREEN`).
4. **Change the target.** To plan new artifacts the agent writes a proposal and runs
   `aes plan accept`; with `require_adopted_plan: true` that refuses unless the
   proposal names a freshly adopted Company Planning plan
   (`RULE-PLAN-RECEIPT-FOR-ACCEPT`), and work that runs must carry a trace-review
   requirement (`RULE-TRACE-REVIEW-DECLARED`).

## Things (entities)

| ID | What it is | Where it lives |
|---|---|---|
| ENT-COMMIT | a commit and its first-line tag | git; verdicts in `<git-common-dir>/aes/commit-rule-<date>.jsonl` |
| ENT-PLAN | a Company Planning plan, its receipt and adoption decision | `docs/plans/`, `proposals/<id>/` |
| ENT-TARGET | outcomes, normative items, criteria, planned artifacts, verification subjects | `.aes/target.yaml` |
| ENT-PROPOSAL | a target delta plus the gaps it closes | a proposal file given to `aes plan` |
| ENT-OBSERVATION | append-only evidence bound to a revision and its dependency paths | `.aes/observations/` |
| ENT-CHARACTERIZATION | what HEAD contains under the governed roots | computed by `aes characterize` |

## Processes

| ID | Trigger | Rules it enforces |
|---|---|---|
| PROC-COMMIT-CHECK | every commit (commit-msg hook) | RULE-COMMIT-TAG, RULE-PLAN-ADOPTED-FOR-COMMIT, RULE-DURABLE-DOCS-FOR-COMMIT (quick plans that carry the durable-documents completion command) |
| PROC-PLAN-ACCEPT | `aes plan validate` / `accept` | RULE-PLAN-RECEIPT-FOR-ACCEPT, RULE-TRACE-REVIEW-DECLARED |
| PROC-RECONCILE | `aes status` / `aes reconcile` | RULE-DRIFT-DETECTED, RULE-INSUFFICIENT-NOT-GREEN, RULE-DEPENDENCY-CHANGE-STALES |

## Gaps in this model

- **G1.** Not modelled: the v0.1 line (Plan 002), the `repository_context` package,
  `aes adopt` legacy baselines, the Company Planning profile files under
  `docs/architecture/`, and the vendored `enforced_planning/` package.
- **G2.** Four rules cite no decision record: the commit-tag and plan-receipt rules
  come from outcome `OUT-AP-001` (Brian, 2026-10-07) and the trace-review rule from
  `TR-REQ-001`, all recorded in `.aes/target.yaml` but never as a decision record;
  `RULE-INSUFFICIENT-NOT-GREEN` comes from AES-POL-002 in
  [SYSTEM_BOUNDARY.md](../architecture/SYSTEM_BOUNDARY.md).

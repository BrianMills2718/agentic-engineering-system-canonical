# Initial AES Gap Ledger

Status: **recomputed for Plan 001 closure from verified AES revision `96fcf5e89ba98ad9ff278ec536a98c308cda3fe1` and follow-up A1 utility evidence on 2026-09-22**.

This ledger compares the accepted clauses in `SYSTEM_BOUNDARY.md` with the
current canonical realization. The revision-bound characterization supporting
this recomputation is:

`evidence/plan-001/96fcf5e89ba98ad9ff278ec536a98c308cda3fe1/characterization.md`

Verification review correction after GitHub Actions became administratively unavailable:

`evidence/plan-001/verification-boundary-correction-2026-09-18.json`

Decision 0008 supersedes the earlier blob-only carry-forward rule.

This remains a planning input, not a replacement for normative clauses. A closed
bootstrap gap means the specific variance originally recorded here is no longer
present; it does **not** prove timeless or system-wide conformance for every
future component.

## Disposition vocabulary

- `CLOSED` — the specific bootstrap variance recorded in this ledger is no
  longer present and current evidence is adequate for that narrow claim.
- `NARROWED` — material progress/evidence exists, but relevant target behavior
  or evidence remains incomplete.
- `PARTIAL` — some realization exists but the gap is still materially open.
- `NOW` — remains on the current Plan 001 closure path.
- `DEFER` — still real but not required to complete the present closure path.
- `NOT_YET_APPLICABLE` — target depends on behavior that still does not exist.

| Gap | Clause | Current at `96fcf5e...` | Remaining variance | Disposition |
| --- | --- | --- | --- | --- |
| GAP-AES-001 | AES-SYS-001 | The first real external vertical completed target -> gap -> plan -> provider disposition -> implementation -> bound verification -> human observation -> characterization -> gap reconciliation/learning | no remaining variance for the original first-loop bootstrap claim; breadth across later components is separate | `CLOSED` |
| GAP-AES-002 | AES-SYS-002 | Repository Context preserves native authority through evidence-bound resolution and the delivered external vertical | authority-preserving composition across additional components/providers remains unobserved | `NARROWED / DEFER` |
| GAP-AES-003 | AES-SYS-003 | The pinned methodology was exercised through planning, implementation, review, verification, utility feedback, and final reconciliation | no remaining variance for the original first-consumer-cycle bootstrap claim | `CLOSED` |
| GAP-AES-004 | AES-SYS-004 | incumbent/provider dispositions remained explicit and no donor silently became runtime authority | repeated use across additional capabilities remains unobserved | `NARROWED / DEFER` |
| GAP-AES-005 | AES-SYS-005 | first local implementation is a bounded residual after provider sourcing rather than a predecessor rewrite | no remaining variance for the original bootstrap claim; future work must preserve the rule | `CLOSED` |
| GAP-AES-006 | AES-PLAN-001 | Plan 001 originated in explicit gaps and now has exact technical evidence, utility evidence, characterization, and final reconciliation | no remaining variance for the first-plan bootstrap claim | `CLOSED` |
| GAP-AES-007 | AES-PLAN-002 | Company Planning shaped the design; Enforced Planning provided terminal exact-revision verification and historical custody limits remained honest | one fully prospective planning -> execution custody cycle from plan start remains incompletely evidenced | `NARROWED / DEFER` |
| GAP-AES-008 | AES-PLAN-003 | merge, plan completion, technical conformance, utility, and gap closure were kept distinct; final delivery followed fresh evidence | no remaining variance for the original Plan 001 separation claim | `CLOSED` |
| GAP-AES-009 | AES-CAP-001 | provider search/disposition selected Git/Pydantic/PyYAML/stdlib plus bounded AES residual semantics, and that residual was implemented | original bootstrap variance is resolved for the first capability | `CLOSED` |
| GAP-AES-010 | AES-CONTRACT-001 | AES-local RepositoryContextArtifact is implemented and exercised against the real external consumer without making Data Contracts a runtime dependency | original Slice 1 contract-ownership variance is resolved | `CLOSED` |
| GAP-AES-011 | AES-POL-001 | Enforced Planning governance and exact verification-batch behavior are observed, and utility feedback changed the delivered surface | adaptive policy behavior across broader lifecycle/components remains incomplete | `NARROWED / DEFER` |
| GAP-AES-012 | AES-POL-002 | Repository Context preserves NONE/ERROR/UNRESOLVED states and tests fail-closed behavior | full control-state coverage including stale/pass/fail across broader controls remains incomplete | `NARROWED / DEFER` |
| GAP-AES-013 | AES-POL-003 | malformed-manifest recovery semantics are implemented/tested and governance refused fabricated retroactive custody | one prospective destructive/authority-sensitive block -> recovery transition remains incompletely evidenced | `NARROWED / DEFER` |
| GAP-AES-014 | AES-POL-004 | Repository Context and architecture/profile probes include deliberate negative controls that turn red | broader important-control coverage remains incomplete | `NARROWED / DEFER` |
| GAP-AES-015 | AES-CTX-001 | wiki is an active progressive-disclosure surface and is reconciled with final Plan 001 evidence/gap state | projection remains partly hand-maintained rather than wholly regenerated | `NARROWED / DEFER` |
| GAP-AES-016 | AES-CTX-002 | realized Repository Context exists and source-local component-context dogfood has been exercised | generalized source-local delivery for realized components is not yet an operational capability | `NARROWED / DEFER` |
| GAP-AES-017 | AES-EVID-001 | fresh exact technical evidence at `96fcf5e...`, two utility observations, append-only receipts, final characterization, and recomputed gap state now exist | current projections are not yet fully mechanically regenerated across AES | `NARROWED / DEFER` |
| GAP-AES-018 | AES-LEARN-001 | negative A1 utility evidence caused a bounded correction; follow-up A1 accepted the direction and the result is explicitly dispositioned into future planning | no remaining variance for the first vertical's learning-feedback claim; no automated learning platform is required | `CLOSED` |
| GAP-AES-019 | AES-DOGFOOD-001 | exact pinned `data-contracts` consumer was exercised through the real Repository Context entrypoint and retained artifacts | no remaining variance for the requirement that the first vertical cross a real external consumer | `CLOSED` |
| GAP-AES-020 | AES-DOGFOOD-002 | the first concern traversed target/current/gap/disposition/planning/provider sourcing/execution/evidence/human observation/fresh characterization/gap recomputation, with enforced negative/recovery behavior retained | no remaining variance for the original first end-to-end dogfood claim | `CLOSED` |
| GAP-AES-021 | AES-PLAN-004 | Plan 001 was executed as one actor-centered external-consumer vertical distinct from work/dependency graph mechanics | original bootstrap variance that slice derivation was unexercised is resolved | `CLOSED` |
| GAP-AES-022 | AES-CAP-002 | external/native substrate was sourced first, internal donors were not selected by default, and chosen dependencies were exercised | original first-vertical sourcing variance is resolved; rule remains applicable to future work | `CLOSED` |
| GAP-AES-023 | AES-PLAN-005 | authentic source-bound HTML/CLI surface exists; first A1 drove correction and follow-up A1 returned `continue` | no remaining variance for the first human-observable Slice 1 claim | `CLOSED` |
| GAP-AES-024 | AES-PLAN-006 | experience-backward design met real `change` evidence, adapted, and the corrected interaction was directly judged `continue` | no remaining variance for the first vertical's confidence-weighted experience loop | `CLOSED` |
| GAP-AES-025 | AES-PLAN-007 | D1 remained bounded dependency-resolution work and returned to the usable vertical rather than expanding into infrastructure | broader evidence across runtime feasibility/enabler decisions remains limited | `NARROWED / DEFER` |
| GAP-AES-026 | AES-ECON-001 | human attention was spent at two decision-useful checkpoints: the first exposed reconstruction cost and the second accepted the bounded correction | no remaining variance for the first vertical's attention/utility-economics claim | `CLOSED` |
| GAP-AES-027 | AES-CTX-003 | a source-bound working surface was directly used, corrected from negative utility evidence, and accepted on follow-up without authority transfer | no remaining variance for the first concern-specific working-surface claim | `CLOSED` |

## Why a gap list is not an implementation plan

The rows above are variance statements. They do not imply one task, one plan
item, or one implementation slice per gap. Likewise, a dependency/work-unit
graph may express ordering or coordination without producing a useful vertical.

The required transform remains:

```text
dispositioned gaps
  + accepted actor outcome / canonical example
  + delivery maturity + epistemic certainty
  + best-known north-star experience where decision-useful
  + boundaries / provider landscape / feasibility assumptions
  + dependency constraints
  + verification, recovery and attention economics
          ↓
Company Planning slice derivation
          ↓
risk-ordered human-observable verticals
  + explicit probes/enablers only where they protect a vertical
          ↓
optional work-unit graph when coordination needs one
```

## Current grouped outcome

Plan 001 / Repository Context is **DELIVERED for its bounded Slice 1 claim**.

> Starting from the pinned real `data-contracts` consumer, AES derived an
> evidence-bound repository-context design, implemented the residual, received a
> negative first utility observation, made a bounded projection correction,
> executed a fresh exact-revision technical batch at `96fcf5e89ba98ad9ff278ec536a98c308cda3fe1`,
> received follow-up A1 `continue`, and recomputed the originating gap state.

The Plan 001 closure frontier is empty. The remaining `NARROWED / DEFER` rows
are broader AES maturation questions, not unfinished Plan 001 tasks.

No next implementation vertical is authorized merely because this one closed.
The next component-specific design must start from this fresh remaining gap state
plus one concrete human/product outcome and follow the normal Company Planning ->
provider sourcing / ACA evidence -> Enforced Planning lifecycle.

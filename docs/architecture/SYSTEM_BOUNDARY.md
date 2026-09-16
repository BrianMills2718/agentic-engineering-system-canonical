# Canonical AES system boundary

Status: accepted bootstrap target.

These clauses define the initial normative target for this repository. They are intentionally implementation-neutral. Planned implementation and verification subjects are derived later through Company Planning.

## AES-SYS-001 — Integrated lifecycle
AES is the integrated engineering system that connects orientation, normative intent, current-state characterization, gap derivation, planning, capability composition, governed execution, evidence, reconciliation, and learning into one resumable loop.

## AES-SYS-002 — Integration without authority collapse
AES may compose multiple systems, but integration does not transfer their native authority. Each mutable fact has one owning authority or is a derived projection.

## AES-SYS-003 — Methodology adoption
Project-agnostic documentation, policy, repository, and ecosystem architecture is adopted from `BrianMills2718/wiki_methodology` by exact revision rather than copied into a second mutable authority.

## AES-SYS-004 — Incumbent preservation
Existing implementations and systems remain authoritative for capabilities they currently own until an explicit evidence-backed disposition selects reuse, extend, adapt, supersede, salvage, historical, not-applicable, or unresolved.

## AES-SYS-005 — No structure-first rewrite
This repository does not reimplement predecessor systems wholesale. New local implementation exists only for a derived residual gap after incumbent capability resolution.

## AES-PLAN-001 — Gap-backed planning
Substantive implementation plans originate in explicit target/current variance. Planning does not invent current state or close gaps by declaration.

## AES-PLAN-002 — Planning subsystem split
Company Planning is the default AES planning/design derivation provider: it turns accepted intent and dispositioned gaps into success criteria, boundaries, capability requirements, target implementation topology, target verification topology, and execution-ready plans. Enforced Planning is the default execution-governance provider: it delivers context, claims work, coordinates lanes, triggers checkpoints, runs applicable controls, and provides recovery/change paths while the plan executes.

## AES-PLAN-003 — Plan completion is not conformance
A completed plan does not close a gap. Fresh evidence and revision-bound implementation characterization must be compared with the target after implementation.

## AES-CAP-001 — Capability-first residual implementation
Before hand-authoring behavior that may be reusable, the planning flow derives the required semantic capability/action and resolves relevant providers through ACA. The execution contract records reuse, configure, compose, extend, supersede, explicit exception, or residual local implementation.

## AES-CONTRACT-001 — Native typed boundaries
Typed contracts remain with their natural contract authority. Data Contracts may supply reusable provider-neutral typed/composition contracts where applicable; AES does not create a duplicate contract language or universal `contracts/` store.

## AES-POL-001 — Policy is adaptive control
Policy governs the engineering lifecycle through decision-time context, checks, workflow/operational constraints, observations, recovery or escalation, sanctioned change paths, and feedback. Policy authority is distinct from reusable policy machinery.

## AES-POL-002 — Ignorance cannot render green
Controls preserve meaningful states including pass, fail, none/unobserved, error, and stale. Absence or failure to observe never silently becomes success.

## AES-POL-003 — Recovery on block
A blocking control provides a concrete runnable recovery path, or an explicit human escalation when the protected boundary is destructive, irreversible, or authority-sensitive.

## AES-POL-004 — Controls prove they can fail
Important controls are not treated as evidenced merely because they pass. Their verification includes a deliberate negative control or equivalent counterfactual and scope/coverage evidence where applicable.

## AES-CTX-001 — Wiki as progressive disclosure
`wiki/index.md` is the repository information front door. Wiki pages may synthesize enough target/current/gap/plan/research/capability/implementation/verification context to navigate intelligently, but native authorities remain elsewhere.

## AES-CTX-002 — Source-local context after realization
When implementation subjects exist, agents working at those subjects receive generated normative clauses, success criteria, current characterization, gap state, and plan linkage appropriate to that subject. Source-local projections do not become authority.

## AES-EVID-001 — Append-only observations, current projections
Observations and evidence are retained as immutable/append-only history where practical. Current-state and gap views are materialized from the latest valid revision-bound evidence rather than storing history in current docstrings/wiki prose.

## AES-LEARN-001 — Learning re-enters future decisions
Useful observations, failures, rejected fits, policy friction, and capability outcomes receive explicit dispositions so they can influence future policy, planning, context, capability knowledge, or research rather than remaining inert records.

## AES-DOGFOOD-001 — Authentic external vertical
The first implementation vertical must cross a real external consumer boundary. Self-dogfood is required, but self-description alone is insufficient evidence of the integrated system.

## AES-DOGFOOD-002 — End-to-end closure
The first vertical is not accepted until one real concern traverses target -> current -> gap -> disposition -> Company Planning -> ACA resolution -> Enforced Planning execution -> policy controls -> evidence -> fresh characterization -> gap recomputation -> wiki/current projection, with at least one observed policy block/recovery or equivalent enforced transition.

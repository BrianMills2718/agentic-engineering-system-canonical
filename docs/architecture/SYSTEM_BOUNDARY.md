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
This repository does not reimplement predecessor systems wholesale. New local implementation exists only for a derived residual gap after provider resolution.

## AES-PLAN-001 — Gap-backed planning
Substantive implementation plans originate in explicit target/current variance. Planning does not invent current state or close gaps by declaration.

## AES-PLAN-002 — Planning subsystem split
Company Planning is the default AES planning/design derivation provider: it turns accepted intent and dispositioned gaps into success criteria, boundaries, capability requirements, provider landscape, target implementation topology, target verification topology, and execution-ready slices. Enforced Planning is the default execution-governance provider: it delivers context, claims work, coordinates lanes, triggers checkpoints, runs applicable controls, and provides recovery/change paths while the accepted execution contract runs.

## AES-PLAN-003 — Plan completion is not conformance
A completed plan does not close a gap. Fresh evidence and revision-bound implementation characterization must be compared with the target after implementation.

## AES-PLAN-004 — Gaps, graphs, and slices are distinct
A gap set identifies target/current variance. A dependency or work-unit graph identifies prerequisite, coordination, or claimability structure. Neither is itself an implementation slice. Company Planning must synthesize risk-ordered, outcome-bearing vertical slices that preserve the actor, canonical behavioral example, end-to-end path, acceptance/readout, important uncertainty, and recovery boundary. A work-unit graph is added only when coordination or a machine consumer requires it and must not substitute for slice derivation.

## AES-PLAN-005 — Implementation slices are human-observable by default
An implementation slice normally ends at an authentic human-usable surface through which the intended actor or reviewer can exercise and judge a small end-to-end version of the accepted capability. The surface may be graphical, CLI, notebook, IDE, API-client, report, operator, or another authentic interaction boundary; the requirement is direct use and judgment, not a GUI framework. Work that cannot yet produce a useful actor outcome is classified explicitly as a boundary probe, dependency-resolution subplan, enabler, or regression/hardening increment and names its return path to the next outcome-bearing slice. Tests, schemas, traces, and internal artifacts may support the slice but do not replace direct stakeholder reviewability.

## AES-PLAN-006 — Experience-backward design is confidence-weighted
When the intended end-state experience is important and sufficiently knowable, planning maintains a best-known north-star interaction or experience and reasons backward to earlier coherent human-usable surfaces, then implements forward slice by slice. Specificity is proportional to delivery maturity and epistemic confidence: stable jobs, states, boundaries, and interactions may be fixed early; details that depend on unobserved behavior remain directional, conditional, or deliberately unresolved. Low confidence favors authentic exploratory surfaces over false-precision final UX. The north star guides slice lineage but does not become authority over evidence that later disproves it.

## AES-PLAN-007 — Feasibility work protects the next usable outcome
Backend, infrastructure, performance, scale, contract, or integration work enters the pre-observation critical path only when it is part of the authentic vertical or is a demonstrated blocker whose resolution materially protects the next human-usable outcome. Planning works backward from the desired experience to identify load-bearing feasibility assumptions and uses the cheapest discriminating probe that preserves the relevant substrate. A successful probe returns immediately to an outcome-bearing vertical rather than expanding into open-ended infrastructure work.

## AES-ECON-001 — Human attention and utility discovery are first-class economics
AES planning and execution optimize expected stakeholder utility under constraints that may include human attention, AI/tool spend, elapsed time, rework and lock-in exposure, and opportunity cost. Human attention may be substantially scarcer than AI computation, so AES may spend additional automated effort to reduce human reconstruction and prepare high-quality decision surfaces when expected value justifies it. That optimization must not hide product uncertainty or allow large speculative implementation inventories to accumulate before a stakeholder can use and judge the result. An attention checkpoint is warranted when the expected decision value of direct human observation exceeds the expected value of another autonomous increment; it is not an approval gate by default. Cross-project prioritization requires an explicit portfolio authority rather than being invented by a project-local executor.

## AES-CAP-001 — Capability-first residual implementation
Before hand-authoring behavior that may be reusable, planning derives the required semantic capability/action and resolves candidate providers. The execution contract records reuse, configure, compose, extend, supersede, explicit exception, or residual local implementation.

## AES-CAP-002 — External-first provider sourcing
For a capability that could reasonably be supplied by a stable platform, standard, mature open-source package, or mature service, provider sourcing examines those options before selecting an internal bespoke implementation. Internal repositories are evidence/design donors by default and become runtime providers only through a positive fit decision. Selection considers semantic fit, stability, maintenance, dependency and operational burden, portability, control requirements, and replaceability. Local implementation is justified only for the residual semantics that remain after proportionate sourcing; trivial deterministic local behavior does not require ceremonial market research.

**Apparent novelty increases the sourcing burden; it is not a positive design signal.** When a needed capability, abstraction, protocol, framework, or mechanism appears not to have an established owner, planning treats that absence as an unmet reuse expectation and a reason to search harder before authorizing invention. Escalation should test, in proportion to the decision: alternate terminology and standards; adjacent disciplines and ecosystems; structural analogues; compositions/adapters over mature components; internal and historical attempts; known failed/abandoned approaches; and whether the requirement or frame is unnecessarily specific or general. A statement such as "this seems novel" or "I could not find an existing solution" does not justify bespoke construction. It creates **search debt** that must be resolved or explicitly bounded.

The desired control gradient is asymmetric: the more consequential and apparently novel the proposed machinery, the stronger the obligation to falsify the novelty claim and shrink the residual gap. If sourcing still leaves a genuine uncovered requirement, implement the smallest residual behavior behind a replaceable boundary and record what was searched, why existing options were insufficient, and what evidence would allow the custom behavior to be deleted or replaced later. Agents may generate speculative ideas freely, but novelty carries no intrinsic product value and must not be used as praise, evidence of importance, or a reason to expand scope.

## AES-CAP-003 — Established modular design, not a parallel platform
AES applies capability composition as ordinary product engineering, not as a separate ACA framework-building programme. Prefer one sufficient existing product or framework, then its native modules and extension mechanisms, then a small integration or consumer adapter, and implement only the remaining product behavior. Depending on a deliberately selected common framework is legitimate reuse; universal cross-framework portability is not a default requirement. No framework is mandatory across the portfolio.

For new or changed behavior, use established information hiding, dependency inversion, ports and adapters, and strategy/policy techniques where they reduce real coupling. Keep cohesive, hard-won behavior and its invariants behind an independently usable boundary within the selected ecosystem. Product-specific policy belongs in the product's configuration, strategy, or adapter, not hidden inside shared collection, normalization, or other mechanisms. Inject consequential variable dependencies or effects through the ecosystem's ordinary extension points; do not add an interface, plugin system, or configuration language for every function.

A consumer-local adapter is expected and acceptable. It may map documented structure, but must preserve identity, units, error meaning, authorization, and effect guarantees. A semantic conflict needs an explicit policy, lookup, or rejection rather than a silent field rename. Shared modules must not import a consumer's private application models or initialization. Keep a clean local seam on first use; extract or generalize when actual consumers reveal stable common behavior and real variation, not to satisfy imagined future products.

## AES-CAP-004 — Native publication and product acceptance
Reusable implementation stays with its natural product, package, module, or service owner; neither AES nor ACA is a universal store for product code. Publish using the selected ecosystem's existing package/API mechanisms, declared dependency closure, revision/version references, an invocation example, and focused boundary tests. Protect existing consumers when shared behavior changes. Framework integration, configuration variants, error/effect behavior, and compatibility are tested where the actual product requires them; hard-coded adapter line-count or reuse-percentage targets are not acceptance criteria.

Company Planning records the selected existing foundation, public boundary, variable policy, consumer-local residual, and verification obligations in the existing design packet. Enforced Planning carries that accepted design into normal implementation and review. This guidance does not add a transport schema, duplicate planning skill, registry, runtime, or new delivery gate.

## AES-CAP-005 — Delivery before speculative mechanism research
Routine product delivery does not require a benchmark or A/B study to justify modularity, configurability, or thin adapters. New ACA-specific infrastructure or a standalone experiment requires separate explicit authorization tied to a named product decision or reproducible blocker that ordinary products, native contracts, documentation, configuration, or adapters cannot reasonably resolve. Return bounded feasibility work to the usable product outcome under AES-PLAN-007. Preserve earlier experiments and their limitations as evidence, but do not restart them from historical instructions or treat a narrow reuse result as a verdict on modular architecture.

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

## AES-CTX-003 — Planning and review use tractable source-bound working surfaces
Human- and agent-facing planning/review experiences should project the smallest concern-specific set of work, architecture, assurance, current/gap, evidence, and decision context that makes the present engineering question tractable. These representations remain bound to exact source authorities and revisions, preserve unavailable/partial/stale/error states, and keep read-only or surface-local interaction distinct from authoritative effects. Representation Router is a donor/provider candidate for this concern, not an authority transfer or mandatory AES subsystem.

## AES-EVID-001 — Append-only observations, current projections
Observations and evidence are retained as immutable/append-only history where practical. Current-state and gap views are materialized from the latest valid revision-bound evidence rather than storing history in current docstrings/wiki prose.

## AES-LEARN-001 — Learning re-enters future decisions
Useful observations, failures, rejected fits, policy friction, capability outcomes, and stakeholder utility observations receive explicit dispositions so they can influence future policy, planning, context, capability knowledge, research, or project continuation rather than remaining inert records.

## AES-DOGFOOD-001 — Authentic external vertical
The first implementation vertical must cross a real external consumer boundary. Self-dogfood is required, but self-description alone is insufficient evidence of the integrated system.

## AES-DOGFOOD-002 — End-to-end closure
The first vertical is not accepted until one real concern traverses target -> current -> gap -> disposition -> Company Planning -> provider sourcing / ACA resolution -> Enforced Planning execution -> policy controls -> evidence -> fresh characterization -> gap recomputation -> wiki/current projection, with at least one observed policy block/recovery or equivalent enforced transition and one direct human observation of the usable outcome.

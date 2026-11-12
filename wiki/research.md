---
type: Concept
title: Research findings that still matter
description: What the research syntheses found that still bears on AES, with the ideas adopted or rejected and the lessons recorded.
status: current
updated: 2026-11-11
sources: [research/README.md, research/synthesis/2026-09-28-legacy-idea-harvest/README.md, research/synthesis/2026-09-28-legacy-idea-harvest/aes-archived.md, research/synthesis/2026-09-28-legacy-idea-harvest/company-planning.md, research/synthesis/2026-09-28-legacy-idea-harvest/ecosystem-ops.md, research/synthesis/2026-09-28-legacy-idea-harvest/enforced-planning.md, research/synthesis/2026-09-28-legacy-idea-harvest/hooks-instructions.md, research/synthesis/2026-09-28-legacy-idea-harvest/project-meta.md, research/synthesis/2026-09-26-inside-success-aes-harvest.md, research/synthesis/ac16-ac17-lessons-for-aes.md, research/synthesis/code-map-v4-salvage-for-aes.md, research/synthesis/fluid-governance-selective-salvage.md, research/synthesis/observation-to-action-advice-for-aes.md, research/synthesis/2026-09-17-external-document-semantics-for-normative-model.md, research/synthesis/2026-09-17-aes-semantic-ownership-crosswalk.md, research/synthesis/2026-09-17-ac17-salvage-for-aligned-normative-component-planning.md, research/synthesis/2026-09-17-proposed-aes-canonical-skeleton-after-sourcing.md]
---

# Research findings that still matter

Research is analytical and non-normative; it informs proposals and decisions but does not change architecture by itself. [research/README.md:3-5](../research/README.md#L3-L5) [research/README.md:29](../research/README.md#L29)
Many syntheses name adoption triggers tied to `aes plan` and v0.2 gaps; those triggers are history with v0.2, and only the findings are carried here. [CLAUDE.md:31-32](../CLAUDE.md#L31-L32)
- [Rationale](rationale.md) (related page)
- [Policy and rules](policy-and-rules.md) (related page)

## Lessons across Brian's earlier systems (harvest of 2026-09-28)

- Recording works; closing does not: one register held 2,506 entries with 4 resolutions, and a repair loop made 9,114 runs for 2 closures. [research/synthesis/2026-09-28-legacy-idea-harvest/README.md:37-42](../research/synthesis/2026-09-28-legacy-idea-harvest/README.md#L37-L42)
- Blocking without a way out becomes net-negative: Brian turned off all 54 Claude hooks on 2026-09-18; a gate must let its own recovery through. [research/synthesis/2026-09-28-legacy-idea-harvest/README.md:48-56](../research/synthesis/2026-09-28-legacy-idea-harvest/README.md#L48-L56)
- The sanctioned route must cost less than the bypass: `[Unplanned]` commits in Enforced Planning rose from 20 of 304 in July to 274 of 445 in September. [research/synthesis/2026-09-28-legacy-idea-harvest/README.md:61-66](../research/synthesis/2026-09-28-legacy-idea-harvest/README.md#L61-L66)
- A proxy route is not the real route: ask the running client or run the mandated route. [research/synthesis/2026-09-28-legacy-idea-harvest/README.md:67-77](../research/synthesis/2026-09-28-legacy-idea-harvest/README.md#L67-L77)
- A person's decision must be a durable record that repairers read; a self-repair re-enabled hooks Brian had turned off. [research/synthesis/2026-09-28-legacy-idea-harvest/README.md:78-83](../research/synthesis/2026-09-28-legacy-idea-harvest/README.md#L78-L83)
- The first version of every honesty mechanism reproduced its target failure; "all clear" needs proof the watched thing is alive. [research/synthesis/2026-09-28-legacy-idea-harvest/README.md:84-93](../research/synthesis/2026-09-28-legacy-idea-harvest/README.md#L84-L93)
- Evidence stores must be readable at the scale they are written (12 GB of hook receipts could not be scanned). [research/synthesis/2026-09-28-legacy-idea-harvest/README.md:94-99](../research/synthesis/2026-09-28-legacy-idea-harvest/README.md#L94-L99)
- Some facts show only in aggregate: dodaf had 38.9% of its lines unreachable from the product while every local check passed. [research/synthesis/2026-09-28-legacy-idea-harvest/README.md:100-105](../research/synthesis/2026-09-28-legacy-idea-harvest/README.md#L100-L105)
- The always-loaded instruction file grows back after every cut (35 KB to 10.5 KB to 32.6 KB in September). [research/synthesis/2026-09-28-legacy-idea-harvest/README.md:106-112](../research/synthesis/2026-09-28-legacy-idea-harvest/README.md#L106-L112)

## Per-source findings

- archived `aes`: scope audits belong to the rule declaration; "audited, found nothing" differs from "never audited"; pair every negative control with a positive one. [research/synthesis/2026-09-28-legacy-idea-harvest/aes-archived.md:16](../research/synthesis/2026-09-28-legacy-idea-harvest/aes-archived.md#L16) [research/synthesis/2026-09-28-legacy-idea-harvest/aes-archived.md:18](../research/synthesis/2026-09-28-legacy-idea-harvest/aes-archived.md#L18) [research/synthesis/2026-09-28-legacy-idea-harvest/aes-archived.md:26](../research/synthesis/2026-09-28-legacy-idea-harvest/aes-archived.md#L26)
- archived `aes` lessons: an undeclared fork, CI that never passed in 37 runs, and a recorded lesson that recurred because nothing gated it. [research/synthesis/2026-09-28-legacy-idea-harvest/aes-archived.md:36-39](../research/synthesis/2026-09-28-legacy-idea-harvest/aes-archived.md#L36-L39)
- Company Planning: a machine-decided execution cursor, proportional planning paths, and a disclosed "still unresolved" list; a gate verified only on hand fixtures had 0 of 2 precision on real transcripts. [research/synthesis/2026-09-28-legacy-idea-harvest/company-planning.md:27](../research/synthesis/2026-09-28-legacy-idea-harvest/company-planning.md#L27) [research/synthesis/2026-09-28-legacy-idea-harvest/company-planning.md:30](../research/synthesis/2026-09-28-legacy-idea-harvest/company-planning.md#L30) [research/synthesis/2026-09-28-legacy-idea-harvest/company-planning.md:56-60](../research/synthesis/2026-09-28-legacy-idea-harvest/company-planning.md#L56-L60)
- ecosystem-ops: decisions identified by their content that only move forward; four delivery states (queued, delivered, observed, responded); a gap closed only by its verifier on the landed revision. [research/synthesis/2026-09-28-legacy-idea-harvest/ecosystem-ops.md:34](../research/synthesis/2026-09-28-legacy-idea-harvest/ecosystem-ops.md#L34) [research/synthesis/2026-09-28-legacy-idea-harvest/ecosystem-ops.md:37](../research/synthesis/2026-09-28-legacy-idea-harvest/ecosystem-ops.md#L37) [research/synthesis/2026-09-28-legacy-idea-harvest/ecosystem-ops.md:41](../research/synthesis/2026-09-28-legacy-idea-harvest/ecosystem-ops.md#L41)
- Enforced Planning: allowlisting commands became an endless exception stream, and controls that passed alone did not pass together. [research/synthesis/2026-09-28-legacy-idea-harvest/enforced-planning.md:44-46](../research/synthesis/2026-09-28-legacy-idea-harvest/enforced-planning.md#L44-L46)
- Hooks and instructions: a switched-off control is a recorded decision; installed is not running, so ask the client; check delivery with a fresh-session recall probe. [research/synthesis/2026-09-28-legacy-idea-harvest/hooks-instructions.md:22](../research/synthesis/2026-09-28-legacy-idea-harvest/hooks-instructions.md#L22) [research/synthesis/2026-09-28-legacy-idea-harvest/hooks-instructions.md:25](../research/synthesis/2026-09-28-legacy-idea-harvest/hooks-instructions.md#L25) [research/synthesis/2026-09-28-legacy-idea-harvest/hooks-instructions.md:27](../research/synthesis/2026-09-28-legacy-idea-harvest/hooks-instructions.md#L27)
- Hooks and instructions: a bounded disposition loop with a two-instance bar did promote taxonomy changes, unlike a plain register. [research/synthesis/2026-09-28-legacy-idea-harvest/hooks-instructions.md:36](../research/synthesis/2026-09-28-legacy-idea-harvest/hooks-instructions.md#L36)
- Project Meta: machine-checked wrong-when conditions that open a keyed concern; one concern lifecycle closed only on verifier evidence; advisory policy changed no behavior. [research/synthesis/2026-09-28-legacy-idea-harvest/project-meta.md:13](../research/synthesis/2026-09-28-legacy-idea-harvest/project-meta.md#L13) [research/synthesis/2026-09-28-legacy-idea-harvest/project-meta.md:17](../research/synthesis/2026-09-28-legacy-idea-harvest/project-meta.md#L17) [research/synthesis/2026-09-28-legacy-idea-harvest/project-meta.md:40](../research/synthesis/2026-09-28-legacy-idea-harvest/project-meta.md#L40)
- Inside Success AES harvest: the assertion-evidence gate was the most-used mechanism the old repository shipped; its stall lessons include green checks with a lost mission and receipts written but never read. [research/synthesis/2026-09-26-inside-success-aes-harvest.md:48](../research/synthesis/2026-09-26-inside-success-aes-harvest.md#L48) [research/synthesis/2026-09-26-inside-success-aes-harvest.md:101-106](../research/synthesis/2026-09-26-inside-success-aes-harvest.md#L101-L106)

## Salvage reviews of other systems

- AC16/AC17: generated artifacts are claims, not truth; agreement is not independence; repair cannot rewrite its judge; unresolved meaning stops dependent work; diagnose cheaply before scaling. [research/synthesis/ac16-ac17-lessons-for-aes.md:969-991](../research/synthesis/ac16-ac17-lessons-for-aes.md#L969-L991)
- AC16/AC17 rejected: porting the AC17 pipeline, executable blueprints as a universal representation, and decomposition by default. [research/synthesis/ac16-ac17-lessons-for-aes.md:1023-1027](../research/synthesis/ac16-ac17-lessons-for-aes.md#L1023-L1027)
- Code Map V4: keep revision-bound evidence, dependency-aware freshness, and the lesson that facts are not comprehension; do not port its product. [research/synthesis/code-map-v4-salvage-for-aes.md:665-677](../research/synthesis/code-map-v4-salvage-for-aes.md#L665-L677)
- Fluid Governance: salvage typed transition decisions and append-only execution receipts; reject its engine, global governor and self-reported metrics. [research/synthesis/fluid-governance-selective-salvage.md:29-39](../research/synthesis/fluid-governance-selective-salvage.md#L29-L39)
- Observation-to-Action: a candidate donor for what a result is licensed to support; the feedback loop's licence derivation uses its evaluator. [research/synthesis/observation-to-action-advice-for-aes.md:46-48](../research/synthesis/observation-to-action-advice-for-aes.md#L46-L48) [scripts/learning_loop/licences.py:1-5](../scripts/learning_loop/licences.py#L1-L5)
- Document semantics: map semantic types to records, not mandatory files; conventional documents are generated views. [research/synthesis/2026-09-17-external-document-semantics-for-normative-model.md:107-119](../research/synthesis/2026-09-17-external-document-semantics-for-normative-model.md#L107-L119)
- Semantic ownership crosswalk: do not make data-contracts a foundational AES dependency; reference external standards rather than reproduce them. [research/synthesis/2026-09-17-aes-semantic-ownership-crosswalk.md:65-72](../research/synthesis/2026-09-17-aes-semantic-ownership-crosswalk.md#L65-L72)
- AC17 salvage for component planning: executable blueprint, compact component manifest and full normative context during decomposition. [research/synthesis/2026-09-17-ac17-salvage-for-aligned-normative-component-planning.md:177-189](../research/synthesis/2026-09-17-ac17-salvage-for-aligned-normative-component-planning.md#L177-L189)
- Proposed skeleton: do not stub generic Capability, ActionDescriptor, Workflow, PolicyEngine or Symbol classes. [research/synthesis/2026-09-17-proposed-aes-canonical-skeleton-after-sourcing.md:187-199](../research/synthesis/2026-09-17-proposed-aes-canonical-skeleton-after-sourcing.md#L187-L199)

## Investigations (status as last written, not verified)

- [2026-09-16 first vertical capability discovery](../research/investigations/2026-09-16-first-vertical-capability-discovery.md)
- [2026-09-16 repository context provider landscape](../research/investigations/2026-09-16-repository-context-provider-landscape.md)
- [2026-09-17 ACA/TOSCA capability fit](../research/investigations/2026-09-17-aca-tosca-capability-fit-test.md)
- [2026-09-17 PROV/in-toto/SLSA fit](../research/investigations/2026-09-17-aes-evidence-prov-intoto-slsa-fit-test.md)
- [2026-09-17 Backstage/TOSCA/SysML fit](../research/investigations/2026-09-17-backstage-tosca-sysml-topology-fit.md)
- [2026-09-17 external provider deep dive](../research/investigations/2026-09-17-external-provider-deep-dive-round-2.md)
- [2026-09-17 external sourcing audit](../research/investigations/2026-09-17-external-sourcing-audit-before-canonical-stub.md)
- [2026-09-17 OPA policy fit](../research/investigations/2026-09-17-opa-aes-policy-fit-test.md)
- [2026-09-17 OPA Enforced Planning probe](../research/investigations/2026-09-17-opa-enforced-planning-policy-probe.md)
- [2026-09-17 Open Workflow Spec vs Enforced Planning](../research/investigations/2026-09-17-open-workflow-spec-vs-enforced-planning.md)
- [2026-09-17 OWS work-graph fit](../research/investigations/2026-09-17-ows-enforced-planning-work-graph-fit-test.md)
- [2026-09-17 PROV/in-toto projection probe](../research/investigations/2026-09-17-prov-intoto-aes-verification-projection-probe.md)
- [2026-09-17 SCIP planned-subject fit](../research/investigations/2026-09-17-scip-planned-subject-fit-test.md)
- [2026-09-17 TOSCA/ACA projection probe](../research/investigations/2026-09-17-tosca-aca-capability-projection-probe.md)
- [investigations README](../research/investigations/README.md)

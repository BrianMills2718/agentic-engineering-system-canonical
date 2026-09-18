---
doc_role: active_authority
authority: canonical_if_merged
status: accepted
accepted_by: Brian Mills delegated high-confidence planning authority
date: 2026-09-17
reversible: true
resolves:
  - AQR-006
---

# Decision 0002 — Use an AES Company Planning profile before modifying or forking Company Planning

## Context

AES needs Company Planning to derive an architecture-realization blueprint that aligns normative responsibility, semantic ownership/provider disposition, component boundaries, implementation homes, typed seams where justified, and verification obligations.

That requirement is more specific than ordinary bounded design, but the current Company Planning provider already has:

- a bounded-design skill that derives requirements, boundaries, domain rules, contracts, schema, evidence/disproof, and thin slices;
- explicit design-depth and execution profiles plus a repository governance overlay;
- a strict, delta-only DesignPacketResult handback;
- DesignPacketResult.design_packet_ref for the detailed design authority;
- requirement_refs, boundary_refs, contract_refs, evidence_plan_ref, and material_concerns for machine-readable handoff without copying the detailed design into the transport record.

The generic handback therefore does not need AES-specific component fields merely to reference an AES architecture-realization design.

## Decision

1. **Do not fork Company Planning now.**
2. **Do not add AES-specific fields to the generic DesignPacketResult contract now.**
3. Define an **AES-local architecture-realization profile** over the existing Company Planning bounded-design method.
4. The detailed AES blueprint remains a project-owned design artifact referenced through the generic handback rather than embedded into Company Planning's generic transport schema.
5. The AES profile may require additional design content and validation, but it does not transfer AES normative authority to Company Planning.
6. Propose a change upstream to Company Planning only when dogfood demonstrates that the improvement is genuinely method-generic rather than AES vocabulary or lifecycle semantics.
7. Fork only if repeated real use shows that a small profile cannot preserve AES requirements without incompatible changes to Company Planning's core authority model, skill behavior, or generic contracts.

## Current AES profile boundary

The AES profile requires the detailed design to make recoverable:

- exact normative source references;
- unresolved questions/AQRs;
- semantic owner/provider disposition;
- coherent component responsibility;
- implementation and verification homes;
- consequential typed seams and explicit unresolved seams;
- verification obligation plus disproof;
- source-local normative-context applicability;
- current non-claims and epistemic limits.

It does **not** require Company Planning to own:

- realized source truth;
- current implementation characterization;
- gap closure;
- runtime execution custody;
- policy authority;
- generic capability, symbol, provenance, or workflow schemas.

## Upstream versus profile versus fork rule

- **Profile:** AES-specific lifecycle, record, traceability, and component-realization constraints.
- **Upstream proposal:** a demonstrated planning improvement that remains useful without AES-specific vocabulary or authority assumptions.
- **Fork:** only after sustained incompatibility is observed in real planning use and cannot be expressed by a bounded profile/overlay.

## Consequences

- AQR-006 is resolved for the current bootstrap.
- The current Company Planning repository remains an incumbent planning provider, not an AES-owned copy.
- Architecture-realization dogfood can proceed without waiting for changes to Company Planning.
- Any later upstream proposal is evidence-backed and separable from AES-specific policy.

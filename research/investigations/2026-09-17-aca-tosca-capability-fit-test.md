# Fit test — ACA capability vocabulary vs OASIS TOSCA 2.0

Status: discriminating probe
Date: 2026-09-17

## Purpose

Test whether Agentic Capability Architecture (ACA) should remain the semantic authority for generic `Capability` / `Requirement` concepts, or whether established TOSCA 2.0 semantics should replace or constrain that vocabulary before AES canonical stubbing.

Internal sources inspected:
- `BrianMills2718/agentic-capability-architecture-canonical` README
- `capability_registry.yml`
- `capabilities/approvals/capability.yml`

External source:
- OASIS TOSCA 2.0: https://docs.oasis-open.org/tosca/TOSCA/v2.0/TOSCA-v2.0.html

## TOSCA semantics relevant to ACA

TOSCA 2.0 provides formal reusable types for topology modeling:

- **Node Type** — reusable entity defining properties, attributes, capabilities, requirements, interfaces and artifacts;
- **Capability Type / Capability Definition** — typed feature exposed by a node and available to fulfill another node's requirement;
- **Requirement Definition / Assignment** — declares a needed capability, optional target node/type, relationship, filters and multiplicity;
- **Relationship Type** — formal relation between requirement-bearing source and capability-bearing target;
- runtime/orchestrator resolution can select matching target nodes/capabilities from constraints.

This is materially stronger than inventing an unconstrained generic `Capability` and `Requirement` pair from scratch.

## ACA semantics observed

The ACA registry organizes reusable functional packages such as `core`, `approvals`, `notifications` and `scheduling`.

Each registry entry can carry:
- status and version;
- package/runtime paths;
- `provides` semantic identities such as `approval.resolve` and `availability.query`;
- `requires` package-level dependencies;
- optional capability dependencies;
- notes/maturity context.

Individual capability manifests add:
- `public_interfaces`;
- `semantic_exports` mapping semantic action IDs to concrete public interfaces;
- configuration schema fragments;
- invariants;
- evidence/maturity observations.

The `approvals` example exposes action identities including `approval.resolve`, `approval.action.bind`, and `approval.action.verify`, binds those identities to concrete implementation interfaces, records invariants, and explicitly separates current evidence from promotion claims.

## Field/concept mapping

| ACA concept | TOSCA analogue | Fit | Notes |
| --- | --- | --- | --- |
| capability package (`approvals`) | Node Type / Node Template | partial | both are reusable units with exposed features, requirements and interfaces; ACA package is functional/library oriented rather than deployment-topology oriented |
| `provides` semantic actions | Capability definitions and/or interfaces/operations | partial | TOSCA capabilities are typed exposed features; ACA `approval.resolve` is closer to an executable semantic action/operation |
| `requires: core` | Requirement definition/assignment | strong conceptually | dependency can be framed as a requirement fulfilled by another node's capability |
| `optional` dependencies | optional requirement assignment / count semantics | partial/strong | TOSCA has optional/multiplicity semantics |
| `public_interfaces` | Node interfaces/operations | strong conceptually | concrete interface exposure maps naturally |
| `semantic_exports.action_id` | interface operation + capability metadata | weak/partial | TOSCA does not directly provide ACA's provider-independent semantic action identity convention |
| runtime path | artifact/interface implementation | partial | deployment-oriented TOSCA artifacts are richer/different |
| configuration | properties | strong conceptually | TOSCA properties are natural configuration metadata |
| invariants | constraints/policy outside core capability | weak | some constraints can be expressed, but ACA behavioral invariants are not equivalent to topology constraints |
| evidence/maturity | no direct core equivalent | absent | ACA's reuse/evidence lifecycle is distinct |
| selection/rejection/net value | no direct core equivalent | absent | provider-selection semantics are outside TOSCA topology |
| project-local residual | no direct core equivalent | absent | AES/ACA architectural disposition |

## Critical semantic mismatch

TOSCA's capability is fundamentally:

> a typed feature exposed by a node that can satisfy another node's requirement.

ACA's most important current concept is closer to:

> a provider-independent semantic behavior identity with one or more verified executable implementations/interfaces and accumulated reuse evidence.

Those are related, but not identical.

For example, `approval.resolve` is executable behavior. Modeling it only as a TOSCA capability loses the important distinction between:

- the functional capability/bundle (`approvals`);
- the semantic action (`approval.resolve`);
- the concrete public implementation (`na_approvals.engine.resolve`);
- evidence that the implementation honestly satisfies that semantic export.

## Result

**TOSCA should constrain and inform ACA/AES capability topology, but current evidence does not support replacing ACA's semantic-action/export layer with raw TOSCA.**

The promising separation is:

```text
TOSCA-style topology vocabulary
    node / capability / requirement / relationship / interface
                    +
semantic action identity
    provider-independent callable behavior
                    +
implementation binding
    concrete interface/export/provider
                    +
AES/ACA evidence lifecycle
    fit / rejection / maturity / residual
```

This suggests that the words `Capability` and `Requirement` should not be casually redefined by AES. If retained in ACA/AES, they should explicitly declare whether they are TOSCA-compatible topology concepts or a narrower/different semantic-action concept.

## Recommended bootstrap disposition

1. **Do not freeze a new AES `CapabilityDescriptor`.**
2. Treat TOSCA Capability/Requirement/Node/Relationship as the external semantic baseline for generic topology language.
3. Preserve a separate concept for **semantic action identity** if provider-independent executable behavior remains required.
4. Test whether ACA capability manifests can be projected into a TOSCA-inspired topology plus a small action/export extension.
5. Keep ACA's evidence/maturity/provider-selection semantics separate; they are not provided by TOSCA.
6. Do not make a TOSCA orchestrator/runtime an AES dependency merely to reuse its vocabulary.

## Candidate projection of `approvals`

Conceptually:

```text
Node: approvals provider/package
  properties:
    version: 0.1.1
    status: candidate

  capabilities:
    approval-behavior:
      # externally typed feature family

  requirements:
    core:
      capability: shared-core-behavior

  interfaces:
    actions:
      resolve -> na_approvals.engine.resolve
      bind    -> na_approvals.binding.bind_approval
      verify  -> na_approvals.binding.verify_approval

AES/ACA extension/projection metadata:
  semantic action ids:
    approval.resolve
    approval.action.bind
    approval.action.verify
  evidence/maturity
  behavioral invariants
```

This is intentionally a projection hypothesis, not a new canonical schema.

## Stubbing implication

Safe to stub:
- external-topology adapter/projection port;
- semantic-action identity/binding residual if confirmed after broader standards search;
- evidence/maturity/provider-fit layer.

Unsafe to stub:
- a universal AES-local `Capability`, `Requirement`, `Node`, or `Relationship` model that duplicates TOSCA semantics without an explicit incompatibility finding.

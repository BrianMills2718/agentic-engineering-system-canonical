# TOSCA 2.0 projection probe against ACA capability metadata

Status: research probe; non-normative.

## Question

How much of ACA's generic capability vocabulary can be represented by OASIS TOSCA 2.0 before AES/ACA-specific residual semantics are needed?

## Concrete ACA donor

ACA's `approvals` capability currently declares:

- capability identity: `approvals`;
- status/version/runtime;
- `provides`: semantic action IDs such as `approval.resolve`, `approval.action.bind`, `approval.action.verify`;
- `requires`: `core`;
- concrete public interfaces;
- semantic-export bindings from action IDs to public interfaces;
- configuration schema;
- behavioral invariants;
- evidence/maturity notes.

## TOSCA-style projection

Illustrative only:

```yaml
tosca_definitions_version: tosca_2_0

capability_types:
  aca.semantic_action:
    properties:
      action_id:
        type: string
        required: true

node_types:
  aca.capability:
    properties:
      version:
        type: version
      maturity:
        type: string
    capabilities:
      approval_resolve:
        type: aca.semantic_action
      approval_action_bind:
        type: aca.semantic_action
      approval_action_verify:
        type: aca.semantic_action
    requirements:
      - core:
          capability: aca.core_capability
    interfaces:
      Runtime:
        operations:
          resolve:
            implementation: na_approvals.engine.resolve
          bind:
            implementation: na_approvals.binding.bind_approval
          verify:
            implementation: na_approvals.binding.verify_approval

topology_template:
  node_templates:
    approvals:
      type: aca.capability
      properties:
        version: 0.1.1
        maturity: candidate
```

## What TOSCA covers well

- typed nodes;
- capabilities and requirements;
- relationship matching;
- properties and attributes;
- interfaces and operations;
- implementation artifacts;
- topology templates and reusable types;
- requirement-to-capability fulfillment.

This is materially stronger than inventing an AES/ACA-local generic capability/requirement graph.

## What ACA still adds

The projection loses or weakens several ACA-specific semantics:

- provider-independent semantic action identity as a first-class discovery key;
- explicit distinction between broad `provides`, declared public interfaces, and *verified* `semantic_exports`;
- evidence-backed maturity and promotion/rejection history;
- local-gap reasoning;
- candidate selection/rejection and net-value comparison before coding;
- explicit "internal donor vs selected runtime provider" disposition;
- capability reuse feedback across projects;
- proof that an executable export honestly implements the claimed semantic action.

TOSCA can encode many of these as properties/artifacts, but that would be an extension profile, not native TOSCA semantics.

## Disposition

**Use TOSCA 2.0 as the leading external reference/substrate for generic capability / requirement / topology semantics.**

Do not freeze an AES-local `CapabilityDescriptor`, generic `Requirement`, or generic capability graph until a TOSCA profile/projection test proves which residual fields are actually necessary.

ACA remains a strong donor/provider candidate for the agent-facing semantic-action catalog, executable-export verification, provider selection/rejection evidence, and capability-learning loop.

## Canonical-stub consequence

Safe to reserve:

- `capabilities/tosca_adapter.py`;
- `capabilities/semantic_action_binding.py` only if the residual semantic-action binding survives provider analysis.

Unsafe to freeze yet:

- generic AES `Capability`;
- generic AES `Requirement`;
- universal AES `ProviderGraph`.

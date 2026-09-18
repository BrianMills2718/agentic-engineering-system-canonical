# Fit test — Enforced Planning work graph projected toward Open Workflow Specification

Status: discriminating probe
Date: 2026-09-17

## Purpose

Move beyond a landscape comparison by testing a real Enforced Planning work graph against the Open Workflow Specification (OWS) semantic surface.

Internal source inspected:
- `BrianMills2718/enforced-planning@3fd1ff4465ed50613a8b9fcc86d7d0f282322d60`
- `docs/plans/106_cross_client_mailbox_fleet_delivery_work_graph.json`

External source inspected:
- Open Workflow Specification schema `1.0.3`
- https://github.com/open-workflow-specification/specification/blob/main/schema/workflow.yaml

## Real Enforced Planning work-unit shape

The sampled graph's units carry semantics including:

- stable unit identity;
- initiative / goal identity;
- design and specification revisions;
- title and objective;
- work class and execution class;
- claimability;
- authorization mode;
- explicit included/excluded scope;
- typed inputs and outputs;
- dependency edges with hard gates and rationale;
- conflict surfaces identifying repository paths/external systems and exclusivity;
- acceptance criteria;
- exact evidence required;
- negative controls;
- readiness state and required approvals;
- accepted/runtime status.

These fields combine several distinct concerns that should not be mistaken for one generic workflow schema.

## What OWS can represent well

OWS 1.0.3 has strong generic execution constructs:

- task lists and nested task bodies;
- condition/switch tasks;
- loops / `for` tasks;
- event/listen tasks;
- raised errors;
- execution of containers, scripts, shell commands and nested workflows;
- scheduling and event triggers;
- runtime expression evaluation;
- data passing to nested workflows;
- fault/retry/timeout-oriented workflow mechanics.

These constructs make OWS a credible target for the **generic executable ordering portion** of an Enforced Planning graph.

## Field-level mapping probe

| Enforced Planning work-unit field | OWS fit | Notes |
| --- | --- | --- |
| `id` | strong | workflow/task identity can represent it |
| `title` | strong | documentation/name metadata |
| `dependencies` | partial/strong | can be expressed through task ordering, nesting, conditions or explicit orchestration structure |
| `inputs` / `outputs` | partial | OWS has workflow/task data, but EP input kinds and revision semantics are richer planning metadata |
| `execution_class` | partial | may affect orchestration structure but is not the same concept |
| `objective` | metadata only | descriptive planning intent, not execution semantics |
| `scope.included/excluded` | poor | planning boundary, not generic workflow behavior |
| `claimability` | absent | engineering coordination/custody semantic |
| `authorization_mode` | absent/extension | OWS is not an engineering authorization model |
| `conflict_surfaces` | absent | mutable-source coordination / exclusivity semantic |
| `acceptance[].criterion` | poor | verification/acceptance contract, not a workflow task definition |
| `evidence_required` | absent | assurance/evidence requirement |
| `negative_control` | absent | verification quality semantic |
| `readiness.required_approval_types` | weak | could be modeled as tasks/events but would lose authority semantics if treated generically |
| `approvals` | weak | approval workflow is representable, approval authority/evidence is not natively the same |
| `status` | partial | runtime workflow state differs from governed plan/work-unit state |
| revision identity fields | metadata | can be carried, not natively interpreted |

## Concrete projection hypothesis

For a unit such as `mailbox-mf-02-duplicate-safe-adapters`, an OWS projection could represent:

```text
workflow/task identity
  mailbox-mf-02-duplicate-safe-adapters

precedence
  run only after mailbox-mf-01-host-installation-audit

execution
  invoke a script/container/subworkflow that performs the bounded implementation/check

failure behavior
  use OWS error/retry/timeout constructs where those are generic runtime concerns
```

But the following must remain outside or alongside the OWS document:

```text
why the unit exists
included/excluded scope
whether it is legitimately claimable
which repo paths are exclusive conflict surfaces
which authority approved it
which exact evidence satisfies acceptance
which negative control proves the check can fail
whether completion closes any AES gap
```

## Result

**OWS is a plausible execution projection, not the canonical source for the full Enforced Planning work-unit contract.**

The real graph demonstrates that Enforced Planning combines at least four layers:

1. planning intent/boundary;
2. generic executable workflow/dependency structure;
3. engineering coordination/custody;
4. verification/readiness/evidence governance.

Only layer 2 maps strongly to OWS.

## Recommended architecture

```text
Company Planning / AES plan semantics
        ↓
Enforced Planning governed work unit
        ├── planning + scope + acceptance + custody metadata
        └── generic execution projection
                    ↓
                   OWS
                    ↓
       selected OWS-capable runtime / adapter
```

This preserves the external standard where it is strongest without making OWS responsible for AES/EP-specific authority or assurance concepts.

## Stubbing implication

Canonical AES should create a port/adapter boundary for a generic workflow projection, not its own universal workflow DSL.

Candidate subject class:
- `WorkflowProjectionProvider` or equivalent provider port (name not frozen).

Do not freeze local generic models for:
- task sequencing;
- loops;
- retry policy;
- timeout policy;
- scheduling;
- generic event waiting;
- shell/container/subworkflow invocation.

Retain/freeze only the residual metadata needed to bind AES/EP semantics to the external workflow representation.

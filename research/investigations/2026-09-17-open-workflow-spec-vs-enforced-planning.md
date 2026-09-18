# Open Workflow Specification vs Enforced Planning

Status: research comparison for AES canonical bootstrap
Date: 2026-09-17

## Question

Can the CNCF Open Workflow Specification (OWS) replace, subsume, or materially reduce the bespoke semantics currently carried by Enforced Planning when AES canonical is bootstrapped?

## Sources reviewed

External:
- Open Workflow Specification repository and schema: https://github.com/open-workflow-specification/specification
- OWS workflow schema 1.0.3: https://github.com/open-workflow-specification/specification/blob/main/schema/workflow.yaml

Internal donor:
- `BrianMills2718/enforced-planning` README and governed-repo contract.

## External maturity / shape

OWS is a CNCF Sandbox project under the Serverless Working Group. Its repository describes the project as vendor-neutral and community-driven, with SDKs for .NET, Go, Java, PHP, Python, Rust and TypeScript and multiple runtimes, including Apache KIE SonataFlow, the Java reference implementation, Lemline and Synapse.

The current checked schema advertises DSL version `1.0.3` and itself uses JSON Schema Draft 2020-12.

OWS directly models generic workflow mechanics such as:

- named workflows and namespaces;
- ordered and nested task execution;
- branching/conditions;
- event-driven execution;
- service invocation across HTTP/gRPC/OpenAPI/AsyncAPI-style boundaries;
- timeouts;
- retries and fault handling;
- schedules / cron-like triggers;
- looping and control flow;
- reusable workflow/service constructs;
- standardized machine-readable workflow documents.

These are precisely the categories AES should avoid reinventing as a generic workflow language.

## Enforced Planning semantics observed

Enforced Planning is not merely a workflow DSL. Its repository describes a claim-first coordination/governance model for AI-assisted codebase work with semantics including:

- claim files as canonical low-level coordination truth;
- derived active lanes;
- sanctioned worktrees as bounded execution containers;
- session identity resolution across coding runtimes;
- read-first context gating;
- prewrite claim enforcement;
- generated `AGENTS.md` and governed repository context;
- explicit plan validation and relationship checks;
- blocking controls plus recovery paths;
- lane/session heartbeat and status lifecycle;
- documentation coupling and traceability;
- runtime-specific adapters for Codex, Claude Code and other agents;
- governed repository installation/audit mechanics;
- controlled human-facing runtime/surface registration.

Those semantics are not generic task sequencing. They express engineering custody and coordination around mutable source repositories and agent execution.

## Fit comparison

| Concern | OWS | Enforced Planning | Bootstrap disposition |
| --- | --- | --- | --- |
| Generic workflow/task structure | strong | bespoke/local | **prefer OWS vocabulary / projection where needed** |
| Branching / looping / retries / timeout | strong | partial/bespoke | **do not duplicate in AES/EP** |
| Event-driven triggers | strong | partial/runtime-specific | **prefer OWS where generic** |
| Service invocation description | strong | not core | **prefer OWS/OpenAPI/AsyncAPI** |
| Scheduling | strong | not core | **prefer OWS or scheduler provider** |
| Claim ownership on code/work | absent | strong | **retain as residual/provider semantics** |
| Worktree/lane custody | absent | strong | **retain as residual/provider semantics** |
| Read-before-write context | absent | strong | **retain as residual/provider semantics** |
| Prewrite enforcement | absent | strong | **retain as residual/provider semantics** |
| Agent/session identity adapters | absent | strong | **retain adapter/provider layer** |
| Repo installer/audit contract | absent | strong | **retain provider layer** |
| Requirement/test/doc traceability | not core | strong | **retain or map to separate traceability standards** |
| Recovery after governance block | generic fault recovery only | engineering-specific | **retain AES/EP semantics above OWS** |
| Human checkpoint semantics | not core | partial | **AES/Company Planning residual** |

## Conclusion

**Do not replace Enforced Planning with OWS wholesale.**

Instead, treat OWS as the strongest current candidate for the **generic workflow representation substrate** beneath any future AES/Enforced Planning workflow graph. Enforced Planning should be narrowed to the semantics that make it distinct:

```text
OWS / workflow substrate
        +
AES execution contract
        +
Enforced Planning engineering-custody semantics
        +
runtime/tool adapters
```

This means Enforced Planning should not own a competing universal representation for generic task sequencing, retry, timeout, events or service invocation if OWS can express them adequately.

At the same time, forcing Enforced Planning's claim/worktree/read-gating semantics into OWS extensions would likely be an abuse of the workflow standard. Those are better modeled as provider-specific execution/governance contracts referenced from an AES execution plan.

## Fork / dependency posture

Do not fork OWS yet.

Preferred sequence:

1. use OWS as a semantic/reference standard;
2. test whether AES work graphs can be losslessly projected into an OWS subset for the generic workflow portion;
3. use an existing SDK only if runtime parsing/validation becomes necessary;
4. add small extension metadata only at clear integration seams;
5. fork only if a required generic workflow semantic is demonstrably blocked upstream.

The present evidence does **not** justify making an OWS runtime a mandatory AES dependency. A projection/adapter boundary is the lower-lock-in first step.

## Implication for canonical stubbing

Safe to stub now:

- `workflow_projection` / adapter boundary from AES execution semantics to an external workflow representation;
- Enforced Planning adapter/provider boundary;
- claim/worktree/session/governance residual interfaces if required by AES.

Do **not** stub now:

- a new AES universal `Workflow`, `Task`, `RetryPolicy`, `Schedule`, `Event`, or generic workflow state-machine schema.

Those names should remain externally owned unless a later fit test proves OWS insufficient.

# Fit test — OPA/Rego vs AES and Enforced Planning policy semantics

Status: discriminating probe
Date: 2026-09-17

## Purpose

Determine whether AES or Enforced Planning should own a generic policy language/evaluator, or whether Open Policy Agent (OPA) should be the default external provider candidate for that layer.

External sources:
- https://www.openpolicyagent.org/docs
- https://www.openpolicyagent.org/docs/policy-language
- https://www.openpolicyagent.org/docs/management-introduction
- https://www.openpolicyagent.org/docs/management-decision-logs

Internal donor:
- `BrianMills2718/enforced-planning@3fd1ff4465ed50613a8b9fcc86d7d0f282322d60`
- effective-policy and claim-gate material in the repository

## OPA semantics observed

OPA is a graduated CNCF general-purpose policy engine. Its architecture explicitly separates:

- policy decision-making from policy enforcement;
- structured input/data from declarative Rego policy;
- distributed Policy Decision Points from application-specific Policy Enforcement Points;
- policy distribution from evaluation;
- decision evaluation from decision logging/auditing.

Relevant capabilities include:

- arbitrary structured JSON-like input;
- declarative Rego rules;
- local/embedded/sidecar/server deployment patterns;
- bundles for policy distribution;
- decision logs carrying decision IDs, query/input and bundle revision information;
- APIs/SDK integration rather than requiring a specific application architecture.

## Enforced Planning policy/governance semantics observed

Enforced Planning contains engineering-specific controls such as:

- claim ownership and prewrite admission;
- stale/unavailable projection behavior;
- allow/block reason codes;
- exception/effective-policy resolution;
- fail-closed ownership transfers;
- session lifecycle dispositions;
- recovery-required states;
- explicit recovery/continuation guidance;
- policy authority that may be distinct from the mechanism implementing a check.

AES additionally requires:

- PASS / FAIL / NONE-or-unobserved / ERROR / STALE semantics;
- recovery on block;
- negative-control proof that important controls can fail;
- policy decisions tied into plans, gaps, evidence and lifecycle state;
- authority separation between who owns a rule and what machinery evaluates it.

## Mapping

| Concern | OPA | AES / Enforced Planning residual |
| --- | --- | --- |
| declarative policy rules | strong | do not duplicate |
| structured policy input | strong | adapters provide AES/EP context |
| allow/deny or richer decisions | strong | consume result |
| policy evaluation engine | strong | do not duplicate |
| policy distribution | strong | optional provider capability |
| decision log / decision id | strong | can feed evidence/provenance |
| policy authority ownership | not decided by OPA | AES/owning system |
| when to invoke a control | application concern | AES/EP |
| enforcement point | external/application | EP/runtime adapters |
| engineering claim/worktree semantics | absent | EP residual |
| recovery path after block | absent as domain semantics | AES/EP residual |
| NONE / ERROR / STALE epistemic projection | not an AES lifecycle model | AES residual |
| negative-control adequacy | not supplied | AES verification semantics |
| plan/gap consequence of decision | absent | AES residual |

## Result

**OPA should be the default external provider candidate for generic policy evaluation.**

AES/Enforced Planning should not define a new generic policy language/evaluator unless a concrete fit test demonstrates that Rego/OPA cannot express the required decision semantics.

The likely layering is:

```text
policy authority / canonical rule source
        ↓
projection or compilation into Rego/data where appropriate
        ↓
OPA policy decision point
        ↓
decision + trace/log identity
        ↓
Enforced Planning / runtime enforcement point
        ↓
AES lifecycle interpretation
    block / recovery / evidence / characterization
```

OPA does not replace Enforced Planning because the latter owns engineering-specific enforcement/custody and recovery behavior, not merely rule evaluation.

## Important caution

Do not automatically migrate every deterministic repository validator into Rego. Small local checks may remain simpler and more transparent as direct code. OPA is justified where AES needs a reusable/general policy-decision boundary or where policy data/rules benefit from separation from enforcement code.

## Stubbing implication

Safe to stub:
- a policy-decision provider port / adapter interface;
- AES control invocation/result normalization;
- recovery/escalation semantics;
- evidence binding to policy decision identity/revision.

Do not stub:
- a universal AES policy DSL;
- a generic rule evaluator;
- a parallel bundle/distribution system that duplicates OPA.

## Follow-on probe

Take one real Enforced Planning prewrite claim decision and encode the pure decision portion in Rego while leaving claim storage, authority, mutation and recovery outside OPA. Compare:

- semantic fidelity;
- complexity;
- decision observability;
- failure behavior;
- maintenance burden.

Only then decide whether OPA should become an actual runtime dependency or remain an optional provider.

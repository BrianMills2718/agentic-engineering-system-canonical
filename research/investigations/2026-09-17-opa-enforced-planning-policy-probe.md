# OPA / Rego fit probe against Enforced Planning

Status: research probe; non-normative.

## Question

Can Open Policy Agent own the generic decision-evaluation part of an Enforced Planning control without absorbing Enforced Planning's authority, custody, recovery, and lifecycle semantics?

## Concrete donor behavior

The donor is Enforced Planning's pre-write / claim admission behavior. Current implementation and plans distinguish facts such as:

- whether a canonical claim exists;
- whether a claim/projection is stale or unavailable;
- whether the repository identity is known;
- whether the attempted operation is a sanctioned bootstrap/recovery path;
- whether the caller owns the relevant work boundary;
- explicit allow/block outcomes plus reason codes;
- recovery/continuation behavior after a block.

Enforced Planning also treats claim YAML as ownership authority while derived JSON projections are non-authoritative.

## Candidate Rego projection

The following is deliberately a *decision projection*, not a replacement for Enforced Planning:

```rego
package aes.prewrite

default allow := false

decision := {
  "allow": allow,
  "reason": reason,
} if {
  allow
  reason := "claim_valid"
}

decision := {
  "allow": false,
  "reason": "projection_unavailable_or_stale",
} if {
  not input.projection.current
}

decision := {
  "allow": false,
  "reason": "repository_identity_unavailable",
} if {
  not input.repository.identity_known
}

allow if {
  input.operation.kind == "bootstrap"
  input.operation.sanctioned == true
}

allow if {
  input.claim.exists
  input.claim.owner == input.actor.id
  input.claim.covers_target == true
  input.projection.current == true
  input.repository.identity_known == true
}

reason := "claim_bootstrap_command" if {
  input.operation.kind == "bootstrap"
  input.operation.sanctioned == true
}
```

## What maps cleanly to OPA

- deterministic decision evaluation over structured facts;
- explicit allow/block decision values;
- reason-code derivation;
- policy/data separation;
- versioned policy bundles;
- decision IDs/logging for audit;
- local/embedded evaluation through REST, Go, or WebAssembly.

## What does not map to OPA

OPA intentionally does not own:

- the authority that says claim YAML is canonical;
- creation, refresh, heartbeat, transfer, or release of claims;
- sanctioned worktree lifecycle;
- actor/session identity acquisition from Codex/Claude adapters;
- repository mutation fencing;
- stale-state detection inputs themselves;
- recovery execution after a block;
- escalation to a human;
- plan/slice semantics;
- gap or evidence lifecycle consequences;
- proof that a policy control can fail under a negative control.

OPA evaluates the facts it is given; it does not make those facts authoritative.

## Disposition

**Strong candidate for reuse as generic policy evaluation substrate.**

Do not create an AES-local generic policy language or evaluator unless a concrete semantic gap appears.

Enforced Planning remains a candidate provider for engineering-control invocation, authority/custody, recovery, and agent/runtime integration. A future adapter could project current Enforced Planning facts into OPA input and translate an OPA result back into the Enforced Planning control lifecycle.

## Canonical-stub consequence

Safe to reserve subjects such as:

- `policy/opa_adapter.py` — provider adapter;
- `policy/decision_projection.py` — provider-neutral AES projection only if required.

Do **not** stub a generic `PolicyEngine`, `PolicyLanguage`, or `RuleEvaluator` as AES-local residuals.

# AES v0.2 portable provider boundaries

Status: **candidate architecture / non-normative**
Date: 2026-09-24

## Goal

Resolve two Greenfield-MVP provider questions without binding AES to a private
planning plugin, a particular LLM vendor, or a client-specific hook runtime.

## 1. Planning reasoning provider

AES owns:

- planning input semantics;
- planning output semantics;
- completeness validation;
- target-delta acceptance ordering;
- execution-plan validation.

AES does **not** need to own the intelligence that proposes the plan.

### Provider-neutral protocol

Candidate flow:

~~~text
aes plan prepare
        ↓
planning-request.yaml
        ↓
human or agent reasoning provider
        ↓
planning-proposal.yaml
        ↓
aes plan validate
        ↓
human/authorized acceptance
        ↓
target + plan update
~~~

A planning request contains the smallest complete planning context:

- accepted target facts relevant to the gap;
- qualified current;
- gap set;
- accepted failure modes/analysis;
- known provider landscape if already available;
- planning contract/invariants;
- explicit output schema/required semantic fields.

A proposal contains:

- proposed capability requirements/provider bindings;
- proposed realization units;
- exact durable artifact topology/generation rules;
- selected load-bearing symbol commitments;
- intended consequential dependencies;
- verification subjects mapped to criterion evidence requirements;
- unresolved planning uncertainty/probes;
- proposed execution verticals.

### Provider identity

Each proposal must identify the reasoning provider:

- provider kind: human | agent | model_service | other;
- provider/product identity when available;
- model/version when applicable;
- source planning-request identity;
- proposal-generation time;
- explicit unresolved assumptions.

### Default distribution

The Greenfield MVP does not require an embedded model API.

A colleague may use:

- a supported coding agent;
- ChatGPT or another model interactively;
- a human planner;
- a future automated planning adapter.

The exact reasoning provider used for MVP evidence is recorded, but AES remains
usable as a protocol/validator without that provider being built into the core.

### Why this is enough for MVP

The differentiated AES claim is not "AES invented a planning model." It is:

> accepted engineering semantics are compiled into a constrained planning
> problem whose output can be validated and promoted into target topology.

The quality of a specific reasoning provider can be evaluated separately.

## 2. Working-context delivery

AES owns context **content and completeness**, not every host's injection API.

### MVP delivery boundary

Candidate first interface:

~~~text
aes context <subject>
~~~

Output forms:

- human-readable Markdown for direct agent/human consumption;
- structured JSON/YAML form for adapters.

The content is generated from:

- accepted target;
- current/gaps;
- active plan;
- verification obligations;
- relevant intended/observed/derived dependencies.

### Required output behavior

The command must:

- contain full applicable normative/success/disproof text;
- contain provenance/input identities;
- name the target subject;
- report unresolved/ambiguous applicability explicitly;
- never silently omit a required semantic atom due to ranking/budget;
- distinguish required context from optional/relevance-ranked supporting context.

### Automatic injection

Deferred adapter capability:

~~~text
agent/IDE pre-action event
        ↓
invoke aes context <subject>
        ↓
deliver exact returned context
        ↓
optional delivery receipt
~~~

Claude/Codex/IDE-specific hooks may later implement this. They are not necessary
to establish the core Greenfield context projection claim.

The validation profile can give the generated packet directly to a fresh agent.

## 3. Enforcement invocation

The same rule applies to enforcement.

AES owns runnable checks:

~~~text
aes check target
aes check topology
aes check evidence
aes check
~~~

Optional adapters may invoke them from:

- Git pre-commit/pre-push;
- CI;
- coding-agent pre-write/pre-completion hooks;
- editor integrations.

A bypassed hook does not make invalid state valid; explicit AES checks still
report the violation.

## 4. Portable artifact exchange

Planning/context artifacts should be content-addressable enough for receipts and
freshness without embedding self-referential Git commit hashes.

Candidate identities:

~~~text
planning request:
  request_id
  input semantic IDs/content digests
  repository base revision

planning proposal:
  proposal_id
  request_id
  provider identity/version
  proposal digest

context packet:
  subject
  repository revision
  target/current/gap/plan input digests
  packet digest
~~~

Exact serialization remains part of later schema work.

## 5. Consequence for default dependencies

The Greenfield MVP does **not** require:

- Company Planning installation;
- OpenRouter/OpenAI/Anthropic API credentials;
- Enforced Planning;
- Claude/Codex hook APIs;
- Project Meta.

Those may become optional provider/adapters if they pass the v0.2 contracts.

## 6. Consequence for validation

The fresh consumer proof should exercise:

1. AES emits a planning request.
2. A named reasoning provider returns a proposal.
3. AES rejects one malformed/incomplete proposal.
4. AES validates the corrected proposal.
5. Accepted target topology is materialized.
6. AES emits a subject context packet.
7. A fresh agent receives that packet directly.
8. The same change is separately attempted without the packet as the control.

That proves the portable semantic boundaries before native client automation.

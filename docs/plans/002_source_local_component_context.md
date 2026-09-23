# Plan 002 — Operational source-local component context

Status: **accepted for execution under the contributor's autonomous `proceed` instruction; coordinated single-lane internal-product slice**
Plan ID: `PLAN-002`
Recorded: 2026-09-22
Planning provider: `BrianMills2718/company-planning@c0887bf8901853dc5eb79f0f75667360970f7c47`
Planning method: bounded-design, Standard route, AES-local profile
Origin gaps: `GAP-AES-007`, `GAP-AES-016`, `GAP-AES-017`
Primary component: `normative_context`
First authentic consumer: existing `repository_context` source files

## Outcome

When an agent attempts to edit a file inside a realized AES component, the
existing Enforced Planning edit/context machinery should automatically surface
that component's generated, source-bound engineering context before the edit
proceeds.

For the first consumer,
`src/agentic_engineering_system/repository_context/resolver.py`, the agent
should receive:

- component responsibility and implementation home;
- applicable direct, inherited, and seam-level AES clauses verbatim from their
  owning authority;
- exact source identity for the generated projection;
- current gap authority and active-plan linkage;
- existing repository-default governance without replacement.

The agent should not have to reconstruct this manually from the wiki, system
boundary, gap ledger, plan, and an old bootstrap sidecar.

## Current state

Existing provider machinery already owns delivery:

- `enforced_planning/context_packet.py`;
- `enforced_planning/file_context.py`;
- `.claude/hooks/gate-edit.sh`;
- `scripts/relationships.yaml`.

A real pre-plan probe on canonical AES returned only the target file plus generic
repository-default context for `repository_context/resolver.py`. It did not
carry component-specific normative, gap, or plan context.

The old
`src/agentic_engineering_system/repository_context/component.context.generated.yaml`
is useful bootstrap evidence, but it is a hand-maintained pilot with stale Plan
001/current-state content and explicitly says generation is not operational.

## Provider disposition

| Concern | Disposition | Owner |
| --- | --- | --- |
| edit-time context delivery | **reuse unchanged** | Enforced Planning context packet + edit gate |
| relationship/config routing | **reuse/extend configuration only** | existing `scripts/relationships.yaml` |
| normative authority | **reuse unchanged** | `docs/architecture/SYSTEM_BOUNDARY.md` + accepted decisions |
| current/gap authority | **reuse unchanged** | `docs/architecture/INITIAL_GAP_LEDGER.md` |
| component projection generation | **AES-local residual** | `normative_context` |
| new context runtime/registry/graph | **rejected** | duplicate machinery |
| SCIP/symbol ontology | **not selected** | no demonstrated need |

The residual exists because Decision 0003 requires generated verbatim
applicability, while Enforced Planning already consumes reviewed files and
relationships but does not derive AES component normative scope from the AES
architecture-realization record.

## Planning route

`coordinated`.

Trigger: the generated component projection becomes a shared machine-consumed
context boundary used by the existing edit gate. There is one implementation
lane; no work-unit graph is justified.

Delivery maturity: `pilot`.
Repository-governance overlay applies. No LLM, deployment, migration, public API,
regulated-data, or consequential external-mutation overlay is active.

## Canonical example

Starting state:

- canonical AES checkout with Plan 002 active;
- generated Repository Context component projection is current;
- isolated session-read state has not recorded the projection.

Action:

- agent attempts to edit
  `src/agentic_engineering_system/repository_context/resolver.py`.

Expected result:

1. the existing required-reading gate identifies the component projection as
   required;
2. the blocked edit response includes the full generated projection through the
   existing hook behavior;
3. the projection contains the applicable AES clauses verbatim, source identity,
   current gap authority, and Plan 002 linkage;
4. after the projection is recorded as read, the same edit path is allowed;
5. ordinary relationship context continues to report source-derived
   current/gap/plan relationships;
6. an unrelated repository file is not forced to read Repository Context
   component context.

This proves context delivery, not behavioral conformance or human comprehension.

## Requirements

### RCX-001 — deterministic generated projection

Given a component declared in the accepted Plan 002 architecture-realization
record, AES generates one deterministic `component.context.generated.yaml`
beside that component's code home.

Disproof: identical tracked inputs produce different output or a hand edit is
needed for a valid result.

### RCX-002 — verbatim authority, not re-authored policy

Every declared direct/inherited/seam clause in the projection is extracted
verbatim from its owning authority by stable clause ID. Source path and exact
content identity are retained.

Disproof: paraphrase, omitted declared clause, unknown clause ID, or stale source
identity is accepted.

### RCX-003 — component scope, not blanket injection

Only the selected component's declared normative scope and incident seams are
projected. Repository-wide clauses are not copied merely because they exist.

Disproof: unrelated global clauses appear without applicability.

### RCX-004 — work state remains referenced authority

The projection names the current plan and gap authority without re-authoring
their mutable status as normative truth.

Disproof: generated output invents an active plan, silently claims gap closure,
or becomes a second mutable plan/gap authority.

### RCX-005 — existing edit gate delivers the projection

Existing `scripts/relationships.yaml` mechanisms make files in the first
component require the generated projection and expose relevant
current/gap/plan relationship context. No edit-hook runtime change is planned.

Disproof: the canonical edit does not require the projection or delivery needs a
new hook/runtime.

### RCX-006 — consumer locality

The first gate applies only to Repository Context source files.

Disproof: an unrelated source tree is forced to consume Repository Context
component context.

### RCX-007 — honest freshness

A `--check` mode fails when committed generated context differs from current
tracked authority inputs.

Disproof: stale or hand-edited output passes.

## Projection contract

The first AES-local projection remains intentionally small:

```yaml
schema_version: aes.component_context.v1
component_id: repository_context
generated_from:
  architecture_realization: <path + sha256>
  system_boundary: <path + sha256>
  gap_ledger: <path + sha256>
  plan: <path + sha256>
component:
  responsibility: <from architecture realization>
  code_home: <from architecture realization>
normative_context:
  direct:
    - id: <stable clause id>
      source_path: docs/architecture/SYSTEM_BOUNDARY.md
      verbatim: <exact clause body>
  inherited: [...]
  seams:
    - seam_id: <id>
      normative_refs: [...]
      clauses: [...]
work_context:
  gap_authority: docs/architecture/INITIAL_GAP_LEDGER.md
  active_plan: docs/plans/002_source_local_component_context.md
nonclaims:
  - independent_normative_authority
  - behavioral_conformance
  - gap_closure
```

This is not a universal component contract and is not promoted to Data Contracts.

## Implementation topology

Realize `normative_context` with:

```text
src/agentic_engineering_system/normative_context/__init__.py
src/agentic_engineering_system/normative_context/context.py
scripts/meta/generate_component_context.py
tests/normative_context/test_component_context.py
```

`context.py` owns deterministic projection generation and check-mode
comparison. The script is a thin CLI wrapper.

Reuse existing delivery unchanged. Planned configuration/testing touches are:

```text
scripts/relationships.yaml
.claude/hooks/gate-edit.sh            # authentic test subject; no planned code change
enforced_planning/context_packet.py   # provider runtime; no planned code change
```

If implementation requires changing Enforced Planning runtime semantics, stop and
replan rather than silently expanding this slice.

The first generated consumer projection replaces the stale bootstrap pilot at:

`src/agentic_engineering_system/repository_context/component.context.generated.yaml`.

## Architecture boundary

The detailed project-owned realization is:

`docs/architecture/architecture-realization.plan-002.yaml`.

It realizes only `normative_context` and its `normative_to_code` seam with
the existing `repository_context` consumer. Other reserved components remain
unrealized.

## Verification and disproof

Deterministic verification must cover:

- Plan 002 architecture-realization schema/profile validity;
- deterministic generation;
- exact clause extraction;
- unknown/omitted/paraphrased clause rejection;
- stale-output `--check` failure;
- relationship gate inclusion/exclusion;
- existing Repository Context tests remaining green.

Authentic consumer-path verification must execute the real
`.claude/hooks/gate-edit.sh` with isolated temporary reads/log state and an
Edit-shaped payload targeting `repository_context/resolver.py`.

Observe:

- first attempt blocks;
- additional context contains the generated component projection;
- after marking the projection read, the same path allows;
- relationship context names relevant current/gap/plan sources;
- a control target outside the component is not gated on this projection.

No real source edit is required to prove this hook behavior.

Required negative controls:

- mutate one projected normative sentence;
- remove one declared direct clause;
- change a source authority without regenerating;
- remove the component required-reading gate;
- apply the gate to an unrelated source tree.

## Single implementation slice

**Repository Context source-local context delivery** — deterministic generated
component projection + existing edit-gate delivery + authentic hook observation.

If this works, stop. Generalizing projection to every reserved component requires
a later real consumer.

## Non-goals

- no new context runtime or hook framework;
- no registry or graph database;
- no SCIP requirement or symbol ontology;
- no per-function normative metadata;
- no automatic realization of reserved components;
- no universal schema or Data Contracts artifact;
- no UI/dashboard;
- no ACA experiment;
- no attempt to close broader policy/evidence gaps.

## Failure and recovery

Fail closed on unknown component IDs, missing authorities, unknown normative
clause IDs, duplicate clause IDs, or stale generated output.

Generation never edits normative authority. Failed generation/check leaves the
last committed projection untouched.

If existing Enforced Planning relationship/gate semantics cannot deliver the
projection without runtime changes, stop at that provider mismatch and return to
Company Planning/provider disposition.

## Evidence outputs

```text
evidence/plan-002/<revision>/verification-summary.json
evidence/plan-002/<revision>/hook-observation.json
evidence/plan-002/a1/<revision>.md
```

A utility checkpoint later judges whether the injected packet is actually useful
at source-edit time. Technical delivery alone does not prove context quality.

## Still unresolved

Nothing material unresolved for the first slice.

Reversible implementation details inside `context.py` are delegated to the
implementer so long as they preserve this projection contract, provider boundary,
and negative controls.

## Execution handoff

No work graph is required. After this design and architecture-realization record
validate, hand this one slice prospectively to Enforced Planning /
evidence-first development in a claimed worktree.

Do not begin implementation until prospective execution custody is active.

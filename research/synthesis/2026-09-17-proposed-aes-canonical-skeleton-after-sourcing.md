# Proposed AES canonical skeleton after external sourcing

Status: **bootstrap topology draft — not yet an implementation freeze**

Date: 2026-09-17

Purpose: derive the repository shape AES can safely stub **after** external/OSS sourcing, while refusing to freeze generic abstractions already covered by standards or mature providers.

## Ownership tags

Every planned subject must carry one of:

- `external_projection` — AES view/projection over a standard or external model; no duplicate semantic authority.
- `provider_adapter` — adapter around a selected provider/tool.
- `aes_local_residual` — semantics demonstrated to be genuinely AES-specific.
- `generated_projection` — derived human/agent-facing materialization; never authority.
- `verification` — tests/controls/evidence probes for another subject.
- `unresolved` — do not stub yet; semantic authority/provider decision is not settled.

## Candidate package topology

```text
src/agentic_engineering_system/
├── __init__.py
├── lifecycle/
│   ├── __init__.py
│   ├── target.py
│   ├── current.py
│   ├── gaps.py
│   ├── reconciliation.py
│   └── learning.py
├── subjects/
│   ├── __init__.py
│   ├── planned.py
│   ├── realized.py
│   └── mappings.py
├── capabilities/
│   ├── __init__.py
│   ├── sourcing.py
│   ├── dispositions.py
│   ├── tosca_adapter.py
│   └── semantic_action_binding.py        # unresolved until residual proven
├── planning/
│   ├── __init__.py
│   ├── company_planning_adapter.py
│   ├── slices.py
│   └── acceptance.py
├── execution/
│   ├── __init__.py
│   ├── enforced_planning_adapter.py
│   ├── workflow_projection.py
│   └── custody.py
├── policy/
│   ├── __init__.py
│   ├── opa_adapter.py
│   ├── invocation.py
│   └── recovery.py
├── evidence/
│   ├── __init__.py
│   ├── qualification.py
│   ├── freshness.py
│   ├── epistemic.py
│   ├── prov_adapter.py
│   ├── intoto_adapter.py
│   └── slsa_adapter.py
├── topology/
│   ├── __init__.py
│   ├── backstage_projection.py
│   ├── tosca_projection.py
│   └── sysml_projection.py
├── code/
│   ├── __init__.py
│   ├── scip_adapter.py
│   └── subject_resolution.py
├── context/
│   ├── __init__.py
│   ├── repository_context/               # existing Plan 001 implementation
│   ├── subject_packet.py
│   └── materialize.py
└── cli/
    ├── __init__.py
    └── main.py
```

This is a semantic package topology, not necessarily the final physical split. The next planning pass may collapse modules that do not deserve independent implementation.

## Subject-by-subject disposition

### AES lifecycle residuals

| Planned subject | Tag | Why |
|---|---|---|
| `TargetRef` / target-resolution seam | `aes_local_residual` | AES must connect accepted normative intent into the lifecycle; no external standard owns AES target authority. |
| `CurrentCharacterization` seam | `aes_local_residual` | Current state is a materialized AES judgment from evidence, not raw provenance itself. |
| `Gap` / target-current variance | `aes_local_residual` | Core AES semantic. |
| `GapReconciler` | `aes_local_residual` | Decides closed/narrowed/open/unresolved from target + fresh characterization. |
| learning disposition / feedback seam | `aes_local_residual` | Connects observed outcomes back to future planning/policy/provider decisions. |

### Planned and realized subjects

| Planned subject | Tag | Why |
|---|---|---|
| `PlannedImplementationSubject` | `aes_local_residual` | Exists before code symbols exist; carries intended home/boundary/state. |
| realized source symbol identity | `external_projection` | Use SCIP where supported. |
| planned -> realized mapping | `aes_local_residual` | AES-specific bridge from planning topology to observed source reality. |
| verification subject | `aes_local_residual` | Planning/assurance identity that can exist before or independently of concrete test symbols. |
| realized verification symbols | `external_projection` | SCIP projection where applicable. |

### Capability/provider semantics

| Planned subject | Tag | Why |
|---|---|---|
| external/provider sourcing policy | `aes_local_residual` | AES-CAP sourcing/order/disposition semantics. |
| provider disposition | `aes_local_residual` | reuse/configure/compose/extend/supersede/residual etc. |
| generic capability/requirement topology | `external_projection` | TOSCA 2.0 is leading upstream semantic source. |
| TOSCA adapter/profile | `provider_adapter` | Needed only if practical projection is selected. |
| generic `CapabilityDescriptor` | `unresolved` | Do not stub; likely duplicate of TOSCA/ACA vocabulary. |
| generic action descriptor | `unresolved` | Compare TOSCA operations + ACA semantic action + Data Contracts ActionDescriptor before freezing. |
| semantic-action -> executable-export binding | `unresolved` | ACA has a real residual candidate; not yet proven AES-owned. |

### Planning

| Planned subject | Tag | Why |
|---|---|---|
| slice semantics | `aes_local_residual` | Gaps/work graphs are explicitly distinct from outcome-bearing AES slices. |
| Company Planning adapter | `provider_adapter` | Company Planning remains selected incumbent/donor but not universal semantic authority. |
| acceptance/readout linkage | `aes_local_residual` | AES-specific relation between slice outcome, required evidence, and human observation. |
| generic workflow/task graph | `external_projection` | OWS should carry generic workflow semantics when runtime workflow representation is actually needed. |

### Execution / coordination

| Planned subject | Tag | Why |
|---|---|---|
| Enforced Planning adapter | `provider_adapter` | Strong incumbent for claims, worktrees, execution custody and agent/runtime hooks. |
| workflow projection | `external_projection` | Project/translate executable ordering into OWS when useful; do not copy OWS. |
| claim/worktree/lane custody | `provider_adapter` | Currently Enforced Planning semantics; not AES-local by default. |
| execution consequence into AES lifecycle | `aes_local_residual` | AES interprets execution evidence for current/gap/learning. |

### Policy

| Planned subject | Tag | Why |
|---|---|---|
| generic policy evaluator | `external_projection` | OPA/Rego candidate; do not write AES engine. |
| OPA adapter | `provider_adapter` | Maps AES/Enforced facts and policy decisions. |
| policy authority / invocation | `aes_local_residual` | AES must know which authority owns the policy and when it applies. |
| block recovery / escalation linkage | `aes_local_residual` or provider adapter | Consequence belongs to AES lifecycle; concrete recovery executor may remain Enforced Planning. |

### Evidence and provenance

| Planned subject | Tag | Why |
|---|---|---|
| generic provenance graph | `external_projection` | W3C PROV. |
| signed process attestation | `provider_adapter` | in-toto when cryptographic custody matters. |
| source/build provenance | `provider_adapter` | SLSA when supply-chain/build semantics apply. |
| evidence adequacy / qualification | `aes_local_residual` | Required proof vs observed check is AES lifecycle meaning. |
| freshness / invalidation | `aes_local_residual` | Determines whether evidence may support current characterization. |
| epistemic state integration | `aes_local_residual` | PASS/FAIL/NONE/ERROR/STALE semantics across AES lifecycle. |
| evidence -> characterization effect | `aes_local_residual` | External provenance does not decide AES current truth. |
| evidence -> gap effect | `aes_local_residual` | External provenance does not close/narrow AES gaps. |

### Software/system topology

| Planned subject | Tag | Why |
|---|---|---|
| operational software catalog projection | `external_projection` | Backstage Component/API/Resource/System/Domain vocabulary. |
| capability/requirement topology projection | `external_projection` | TOSCA. |
| formal system-model projection | `external_projection` | SysML v2/KerML only where formal engineering traceability warrants it. |
| one universal AES topology metamodel | `unresolved` | Do not freeze; likely an anti-pattern. AES should compose concern-specific projections. |

### Code realization

| Planned subject | Tag | Why |
|---|---|---|
| SCIP index reader/adapter | `provider_adapter` | Realized symbol identity/occurrences. |
| planned-subject -> SCIP symbol resolution | `aes_local_residual` | Bridge from planning to implementation observation. |
| universal AES symbol model | `unresolved` | Do not create. |

### Context / representation

| Planned subject | Tag | Why |
|---|---|---|
| source-bound subject packet semantics | `aes_local_residual` | AES-specific composition of target/current/gap/plan/evidence around one subject. |
| Representation Router adapter | `provider_adapter` only if selected later | Separate workstream; presentation provider, not truth authority. |
| wiki/context materializers | `generated_projection` | Derived progressive-disclosure surfaces only. |
| Plan 001 repository context resolver | existing `aes_local_residual` pilot | Preserve as current experiment; do not use it to define the whole metamodel. |

## Do-not-stub list

Until a later probe settles ownership, do not create canonical AES classes named:

- `Capability` / `CapabilityDescriptor`;
- generic `Requirement`;
- generic `ActionDescriptor`;
- generic `Workflow` / `Task`;
- generic `PolicyEngine`;
- generic `ProvenanceGraph`;
- generic `Symbol`;
- generic `SystemNode` / universal topology node;
- universal API/schema language.

## First safe skeleton wave

The first filesystem stubbing wave can safely create package/module homes for:

1. lifecycle target/current/gap/reconciliation/learning;
2. planned implementation + verification subjects and planned/realized mappings;
3. provider sourcing + disposition;
4. slice semantics + planning adapter seams;
5. execution provider adapter seams;
6. policy invocation/recovery + OPA adapter seam;
7. evidence qualification/freshness/epistemic state + PROV/in-toto/SLSA adapter seams;
8. SCIP adapter + subject resolution seam;
9. concern-specific topology projection adapters;
10. generated subject/context packet projection seams.

This wave should contain interfaces/docstrings/types only where the semantics above are already resolved. It must not invent implementations merely to fill the tree.

## Next decision

Before converting this topology draft into actual files:

- reconcile it against the accepted AES system boundary and gap ledger;
- decide whether Company Planning should produce the complete topology as an accepted planning artifact;
- define the minimum machine-readable subject manifest that can represent planned subjects, their ownership tags, concrete homes, and verification mappings without duplicating TOSCA/SCIP/PROV/OWS schemas.

That machine-readable planned-subject manifest is likely the next genuinely AES-local contract to freeze.

# AES semantic ownership crosswalk

Date: 2026-09-17
Status: **bootstrap decision input — not yet a normative architecture freeze**
Depends on: `research/investigations/2026-09-17-external-sourcing-audit-before-canonical-stub.md`

## Purpose

This crosswalk determines which conceptual families AES should reuse, adapt, reference, or own before the canonical repository skeleton is materialized.

Disposition values:

- `reuse_standard` — use the standard vocabulary/format directly where applicable;
- `reuse_oss` — consume the OSS implementation/model directly;
- `fork_or_extend` — adopt an external model but add a bounded extension/fork if required;
- `internal_provider_selected` — an internal system is positively selected for this semantic boundary;
- `internal_donor_only` — internal implementation informs design but is not canonical;
- `aes_local_residual` — semantics are specific to AES and remain local;
- `unresolved` — do not stub a canonical type yet.

## Crosswalk

| AES concept / family | External authority/candidate | Internal donor | Disposition | Canonical interpretation |
| --- | --- | --- | --- | --- |
| JSON-shaped payload contract | JSON Schema 2020-12 | `data-contracts` / Pydantic | `reuse_standard` | JSON Schema is the interchange/schema baseline. Pydantic may remain an implementation library, not a competing schema language. |
| HTTP API contract | OpenAPI | `data-contracts` decorators/models | `reuse_standard` | Use when an actual HTTP boundary exists. |
| Event/message API contract | AsyncAPI | `data-contracts` | `reuse_standard` | Use when an actual async/event boundary exists. |
| Software component | Backstage `Component`; SysML part/usage concepts as broader systems model | ACA manifests / internal repo inventories | `fork_or_extend` | Prefer projection onto established component/system vocabulary; AES adds lifecycle/authority metadata rather than redefining “component.” |
| API as software boundary | Backstage `API` + OpenAPI/AsyncAPI/etc. | ACA public interfaces / semantic exports | `reuse_standard` | Backstage can catalog the boundary; domain-specific interface spec owns wire semantics. |
| Runtime/infrastructure resource | Backstage `Resource`; TOSCA node types | internal manifests | `fork_or_extend` | Avoid AES-local universal resource taxonomy. |
| System/domain grouping | Backstage `System` / `Domain`; SysML v2 for richer systems engineering | Vision/project-meta style internal groupings | `fork_or_extend` | Use external nouns/relations where fit; AES context may project them. |
| Application/service topology | OASIS TOSCA 2.0 | internal dependency graphs | `fork_or_extend` | Strong substrate for topology, node/relationship, capability/requirement structure; do not copy wholesale until fit is proven. |
| Rich system model | SysML v2 + KerML + Systems Modeling API | predecessor metamodel work | `internal_donor_only` + external reference | Use as semantic comparison/reference; adopt only subsets justified by software-engineering needs. |
| Generic workflow | CNCF Open Workflow Specification | Company Planning / Enforced Planning | `fork_or_extend` | Use external workflow/task/data/event/fault primitives where applicable; keep planning methodology distinct. |
| Planning methodology | no direct complete external equivalent selected | Company Planning | `internal_provider_selected` provisionally | Company Planning remains the current method provider for gap-backed design/slice derivation, but its generic workflow primitives should not become AES protocol by default. |
| Work/session coordination | generic workflow standards + SCM/worktree substrate; no complete external match selected | Enforced Planning | `internal_provider_selected` provisionally | Keep coding-agent claim/session/worktree semantics as selected provider behavior unless a closer external system is demonstrated. |
| Generic policy decision | Open Policy Agent/Rego | Enforced Planning / project-meta policies | `reuse_oss` candidate | OPA is preferred policy-evaluation substrate when declarative policy evaluation is required. Authority, recovery and lifecycle binding remain outside OPA. |
| Policy authority / ownership | no generic engine can own project authority | project-meta / repository authorities | `aes_local_residual` integration rule | AES preserves native policy ownership; engine != authority. |
| Provenance entity/activity/agent | W3C PROV | `data-contracts` provenance helpers / AES evidence docs | `reuse_standard` | Use PROV vocabulary/interchange for generic provenance where practical. |
| Signed software-process attestation | in-toto Attestation Framework | Enforced Planning receipts | `reuse_standard` / `reuse_oss` candidate | Prefer in-toto-compatible attestations for security-sensitive execution evidence rather than inventing generic attestation envelopes. |
| Build/source provenance | SLSA Provenance 1.2 | internal CI receipts | `reuse_standard` | Use only for build/source provenance; do not stretch into general AES evidence. |
| Realized code symbol identity | SCIP | Code Map / hand-built symbol notions | `reuse_standard` candidate | Use SCIP identifiers/occurrences/relationships for realized code navigation where indexer support exists. |
| Planned implementation subject | none directly equivalent | Company Planning / AES planning docs | `aes_local_residual` | A planned repository realization target may point to a future file/module/class/function/config/doc. It is planning semantics, not a code-index symbol until realized. |
| Implementation subject (realized) | SCIP + language-native identifiers, plus repository path/revision | AES / Code Map donors | `fork_or_extend` | AES subject identity should bind to standard/native code identity when possible and retain only planning/evidence metadata locally. |
| Verification subject | testing framework/native test IDs; no universal semantic standard selected | Enforced Planning relationship graph | `aes_local_residual` wrapper | AES owns the relationship between requirement/implementation/evidence; underlying test identity stays native. |
| Semantic action | Open Workflow operation/task concepts; TOSCA interfaces/operations; API operation definitions; no single universal semantic-action standard selected | `data-contracts.ActionDescriptor`, ACA semantic exports | `unresolved` | Do not canonize `ActionDescriptor` yet. Need a narrower comparison focused on agent-bindable reusable behavior identity. |
| Capability | TOSCA capabilities/requirements; Backstage system/API exposure; SysML concepts; no exact ACA-equivalent standard selected | ACA | `unresolved` | Preserve “capability” as a planning word, but do not freeze a generic AES `Capability` schema yet. |
| Provider | no single standard selected; catalogs/topology tools can describe implementations but not AES selection semantics | ACA | `aes_local_residual` selection semantics | AES/ACA may need a local provider-selection view that references externally modeled software/components/APIs. |
| Requirement graph / contract flow | TOSCA requirements/capabilities; Open Workflow data/task flow | `data-contracts.ProviderBoundGraph` | `unresolved` | Do not promote ProviderBoundGraph as universal. Determine whether it is a thin projection of external models or a justified residual. |
| Provider sourcing disposition | no external standard found for AES exact decision semantics | ACA / Company Planning | `aes_local_residual` | Reuse/configure/compose/extend/supersede/residual decisions are AES planning architecture. |
| Target state | SysML/TOSCA can represent desired model/topology but not AES epistemic distinction | AES architecture docs | `aes_local_residual` | AES-specific role in target/current/gap loop. |
| Current-state characterization | PROV + system/catalog/code sources can supply evidence | predecessor characterization systems | `aes_local_residual` projection semantics | AES owns the revision-bound characterization relation, not all underlying observations. |
| Gap | no direct external replacement selected | AES | `aes_local_residual` | Explicit target/current variance with disposition. |
| Slice | workflow/task concepts are not equivalent | Company Planning / AES | `aes_local_residual` | Human-observable, outcome-bearing implementation increment. Distinct from task/work graph. |
| Work unit / task | Open Workflow Specification task/workflow | Enforced Planning | `fork_or_extend` | Prefer standard task/workflow vocabulary for generic coordination; add agent/claim metadata only where residual. |
| Attention checkpoint | no standard selected | AES / Representation Router research | `aes_local_residual` | Human observation point selected for information value. |
| Epistemic state (`OBSERVED`, `NONE`, `ERROR`, `STALE`, etc.) | PROV expresses provenance, not AES truth-state policy | AES / internal systems | `aes_local_residual` | Keep explicit AES epistemic semantics; map evidence to PROV where helpful. |
| Authority / owning source | Backstage ownership metadata is useful but does not encode AES authority semantics | repo protocol / project-meta | `aes_local_residual` integration rule | One mutable fact has an owning authority or is derived. |
| Evidence receipt | W3C PROV / in-toto / SLSA depending evidence type | AES / Enforced Planning | `fork_or_extend` | Use external envelopes/vocabularies where applicable; AES adds claim/requirement/gap linkage. |
| Learning/disposition feedback | no exact standard selected | ACA evidence feedback / AES research | `aes_local_residual` | Learning re-enters provider/policy/planning decisions with explicit disposition. |
| Human representation selection | no external replacement selected in this audit | Representation Router | `internal_donor_only` pending separate evaluation | Keep presentation separate from semantic authority. |

## What this means for `data-contracts`

Do **not** make `data-contracts` a foundational AES dependency merely because it already contains convenient Pydantic models.

Possible salvage:

- Pydantic implementations can remain convenient local adapters;
- compatibility helpers may remain useful implementation code;
- action/composition/provider graph models are design donors until the unresolved rows above are settled;
- any shared contract retained should either implement/project an external standard or have a documented residual semantic reason.

## What this means for the canonical repository skeleton

### Safe to stub after one more topology pass

AES-local subject families whose semantic ownership is already clear enough:

- target/current/gap lifecycle;
- provider-sourcing disposition records;
- plan/slice linkage;
- planned implementation subjects;
- verification-subject linkage;
- epistemic state + authority bindings;
- evidence reconciliation/learning linkage.

These stubs should **reference** external-standard types rather than reproduce them.

### Do not stub yet

Hold these until targeted comparison resolves them:

- generic `Capability` model;
- generic `ActionDescriptor` model;
- generic requirement/provider graph;
- universal software topology model;
- universal workflow/task model;
- generic provenance model;
- universal code-symbol model;
- generic API/schema contract language.

## Recommended next bootstrap step

Create the **canonical subject topology plan**, not the implementation itself:

1. enumerate every expected AES package/module/file family;
2. assign each file/subject family an owning semantic source from this crosswalk;
3. mark each concrete subject as `external_projection`, `provider_adapter`, `aes_local_residual`, `generated_projection`, or `verification`;
4. refuse any stub whose semantic source remains `unresolved`;
5. only then materialize the repository skeleton.

This preserves the user's desired structure-first visibility without violating AES-CAP-002 by baking bespoke vocabulary into empty files.
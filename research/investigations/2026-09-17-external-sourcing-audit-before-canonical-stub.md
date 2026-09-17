# External sourcing audit before AES canonical stubbing

Date: 2026-09-17
Status: **research / pre-stub sourcing gate**
Purpose: prevent AES canonical from freezing bespoke internal vocabulary or runtime dependencies where mature standards or forkable OSS already cover the needed semantics.

## Decision rule

For every AES concept or capability family, evaluate candidates in this order:

1. established open standard/specification;
2. mature maintained open-source implementation/model;
3. forkable OSS close enough to the required semantics;
4. Brian-authored repositories as donors/candidates, not default authorities;
5. AES-local residual semantics only after the previous layers leave a demonstrated gap.

This applies to `data-contracts`, Company Planning, Enforced Planning, Agentic Capability Architecture, Representation Router, predecessor AES repositories, and any other internal system. Existing internal implementation does not exempt a concept from provider/sourcing review.

## Current external landscape and preliminary dispositions

| AES concern | Strong external candidate(s) | What the candidate already provides | Preliminary disposition before stubbing |
| --- | --- | --- | --- |
| Generic JSON-shaped contracts and validation | JSON Schema 2020-12 | Standard schema vocabulary, validation semantics, meta-schema | **REUSE STANDARD** as baseline for JSON-shaped contract description. Do not invent another generic schema language. |
| HTTP API interfaces | OpenAPI Specification | Machine-readable HTTP API description and ecosystem tooling | **REUSE STANDARD WHEN HTTP BOUNDARY EXISTS**. AES-local wrappers may bind provenance/authority, not redefine HTTP interface semantics. |
| Event/message interfaces | AsyncAPI 3.x | Machine-readable message-driven API contracts, channels, messages, operations, protocol bindings, extensions | **REUSE STANDARD WHEN EVENT BOUNDARY EXISTS**. |
| Software catalog / repository-system topology | Backstage Software Catalog system model | Component, API, Resource, System, Domain, ownership/relations, extensible descriptors and catalog API | **ADOPT VOCABULARY CANDIDATE / DO NOT ADOPT WHOLE PLATFORM YET**. Evaluate whether AES repository/system/component topology can project onto Backstage entities rather than inventing parallel nouns. |
| Deployable/application topology and relationships | OASIS TOSCA 2.0 | Standard topology/orchestration model for nodes, relationships, capabilities/requirements and application topology | **STRONG MODEL DONOR / POSSIBLE STANDARD SUBSTRATE** for topology and requirement/capability relation semantics. Test fit before creating AES-local topology schema. |
| General systems-model semantics | OMG SysML v2 + KerML + Systems Modeling API/Services | Modern standardized systems-model language, precise semantics, interoperability API | **REFERENCE / HIGH-VALUE MODEL DONOR**. Too broad to adopt wholesale without proof, but should constrain AES terminology where overlapping. |
| Workflow/orchestration description | CNCF Open Workflow Specification | Vendor-neutral workflow DSL, task/data flow, events, fault handling, schedules, timeouts, service invocation, conformance kit, SDKs | **STRONG REUSE/FORK CANDIDATE** before treating Company Planning/Enforced Planning workflow vocabulary as canonical protocol. Internal planning semantics may remain above this layer. |
| Policy decision semantics | Open Policy Agent (OPA/Rego) | Mature general-purpose policy engine; policy-as-code; decision API; decouples decision from enforcement | **REUSE ENGINE CANDIDATE** for executable policy decisions. AES still owns policy authority, epistemic state, recovery semantics and lifecycle integration unless external standards cover them. |
| General provenance | W3C PROV | Standard model for entities, activities, agents, derivation, attribution, generation/use, interchange | **REUSE VOCABULARY / INTERCHANGE CANDIDATE** for generic provenance instead of inventing generic provenance primitives. |
| Software-process attestations | in-toto Attestation Framework / in-toto | Standard/open framework for signed supply-chain step evidence, actors, materials/products, planned steps | **STRONG REUSE CANDIDATE** for tamper-evident execution/evidence receipts where security/attestation matters. |
| Build/source provenance | SLSA Provenance 1.2 | Standard provenance predicates on top of in-toto for where/when/how software artifacts were produced | **REUSE WHEN BUILD/SOURCE PROVENANCE IS THE QUESTION**; not a universal substitute for AES evidence. |
| Code symbol/index identity | SCIP Code Intelligence Protocol | Language-agnostic source indexing, symbols, occurrences, definitions/references/implementations, protobuf interchange | **REUSE PROTOCOL CANDIDATE** for realized code subjects/symbol identity. Do not invent a universal function/class symbol graph if SCIP can supply it. |
| Configuration/constraint language | CUE | Constraint-based configuration/data validation and unification | **EVALUATE**, especially for configuration and constraint-heavy declarations; do not replace simpler JSON Schema/Pydantic usage without demonstrated value. |
| Service/model IDL | Smithy | Model-first service/interface description, transformations, validators, code generation ecosystem | **EVALUATE FOR SERVICE MODELING**, not as an automatic universal AES metamodel. |

## Internal systems: donor posture

### `data-contracts`

Useful internal semantics include typed boundaries, `ActionDescriptor`, composition contracts, provider-bound requirement graphs, compatibility checks and provenance helpers. These are **not automatically canonical for AES**.

Preliminary treatment:

- generic payload/schema semantics -> compare against JSON Schema/CUE/Smithy/OpenAPI/AsyncAPI first;
- semantic action/composition semantics -> compare against TOSCA/SysML/Backstage/Open Workflow and other action/capability models before freezing;
- provider-bound requirement graph -> treat as a donor implementation until external topology/workflow standards are mapped;
- repo-specific/AES-specific result schemas -> may remain local residuals if no external semantic authority fits.

### Company Planning

Current repository packages planning skills for roadmap/design/landscape/work decomposition/evidence-first implementation/release. Treat its methods as a **planning-method donor/provider candidate**, not a universal workflow protocol.

Before AES freezes machine-readable plan/workflow types, compare them to Open Workflow Specification and relevant standardized systems/work models. Preserve the distinctive planning semantics only where they are genuinely residual (for example gap-backed slice derivation, uncertainty/attention economics, or actor-centered delivery semantics).

### Enforced Planning

Current repository supplies claim-first coordination, worktree/session lifecycle, governed-repo installation, hooks, checks and relationship/test traceability. Treat this as a **coordination/runtime donor/provider candidate**.

Before AES freezes generic workflow, policy or evidence primitives around it:

- compare workflow semantics against Open Workflow Specification;
- compare policy decision machinery against OPA;
- compare provenance/receipts against W3C PROV and in-toto/SLSA;
- preserve Enforced Planning residuals only where the external substrates do not cover lane claims, coding-agent session identity, repository-local recovery or other demonstrated specifics.

### Agentic Capability Architecture

ACA's distinctive thesis is persistent semantic capability identities plus verified executable exports, composition/rejection/local-gap planning and evidence feedback. Keep that thesis as a donor/research candidate, but do not assume its capability vocabulary is canonical.

Before AES freezes capability/provider nouns:

- map software/system topology to Backstage/TOSCA/SysML;
- map workflow/action behavior to Open Workflow Specification where applicable;
- map typed interfaces to standard API/schema formats;
- retain only the residual agent-facing capability-selection/evidence semantics not already covered.

## Vocabulary implications for AES canonical

### Terms likely safe to keep AES-local

These are currently lifecycle/planning distinctions rather than generic software-model primitives:

- **gap** — explicit target/current variance;
- **slice** — actor-centered, outcome-bearing delivery increment;
- **planned implementation subject** — concrete planned realization target in a repository;
- **verification subject** — concrete verification target associated with realization;
- **attention checkpoint** — human observation point selected for information value;
- AES-specific epistemic states and authority rules where external models do not carry the required semantics.

These terms should still be checked for overlap, but there is no current evidence that an external standard directly replaces their AES meanings.

### Terms that must not be frozen locally yet

Do not create an AES-local canonical type for these until the mapping exercise is complete:

- `Capability` / `CapabilityDescriptor`;
- generic `Action` / `ActionDescriptor`;
- generic `Requirement` graph nodes;
- generic software `Component`, `System`, `Resource`, `API` topology;
- generic workflow/task/state-transition DSL;
- generic policy rule/decision model;
- generic provenance/entity/activity/agent model;
- generic code symbol/function/class identity graph;
- generic API/schema/interface language.

## Proposed canonical layering

```text
external standards / mature OSS
  JSON Schema / OpenAPI / AsyncAPI
  Backstage / TOSCA / SysML v2
  Open Workflow Specification
  OPA
  W3C PROV / in-toto / SLSA
  SCIP
        ↓
provider adapters / projections
        ↓
AES lifecycle semantics
  target/current/gap
  planning/slice
  provider disposition
  governed execution
  epistemic state + authority
  evidence reconciliation
  learning
        ↓
repository-specific planned implementation subjects
        ↓
realized code/config/docs/tests
```

The intended direction is **composition + residual semantics**, not selecting one monolithic external framework as AES.

## Required follow-up before repository skeleton freeze

1. Produce a term-by-term crosswalk from the accepted AES `SYSTEM_BOUNDARY.md` to external standards and internal donors.
2. For each candidate semantic type, record one of:
   - `reuse_standard`
   - `reuse_oss`
   - `fork_or_extend`
   - `internal_provider_selected`
   - `internal_donor_only`
   - `aes_local_residual`
   - `unresolved`
3. Do not stub types marked `unresolved` merely to make the tree look complete.
4. Stub the full repository/file topology only after the semantic ownership of each subject family is known.
5. Where code-level subject discovery is needed, prefer SCIP or language-native indexers/adapters rather than an AES-owned universal symbol schema.
6. Keep human presentation/representation decisions separate; Representation Router work may consume the resulting semantic model but does not establish semantic ownership.

## Sources reviewed

External primary/current sources reviewed on 2026-09-17:

- OASIS TOSCA Version 2.0 standard archive/specification.
- Backstage Software Catalog system model and descriptor documentation.
- OMG SysML v2 final adoption announcement and SysML v2/KerML/API specifications.
- CNCF Open Workflow Specification repository/specification.
- Open Policy Agent official documentation.
- W3C PROV model/overview publications.
- in-toto official specification/getting-started documentation.
- SLSA Provenance 1.2 documentation.
- SCIP Code Intelligence Protocol repository/schema documentation.
- JSON Schema specification (2020-12).
- OpenAPI / AsyncAPI current specification documentation.

Internal donors reviewed:

- `BrianMills2718/data-contracts` pinned Plan-001 consumer revision.
- `BrianMills2718/company-planning` current canonical repository.
- `BrianMills2718/enforced-planning` current canonical repository.
- `BrianMills2718/agentic-capability-architecture-canonical` current canonical repository.

## Current conclusion

**Do not begin the full AES canonical stub yet.**

First complete the semantic crosswalk and ownership/disposition table. The audit already shows enough mature external coverage that blindly materializing internal `Capability`, `Action`, workflow, policy, provenance or symbol models would risk institutionalizing bespoke duplicates.

The likely AES residual is the integration/lifecycle semantics that connects externally owned models: authority, epistemic state, target/current/gap, slice derivation, provider disposition, governed execution, evidence reconciliation and learning.
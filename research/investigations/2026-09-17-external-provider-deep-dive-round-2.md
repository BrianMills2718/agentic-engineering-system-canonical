# External provider deep dive — round 2

Status: canonical-bootstrap research
Date: 2026-09-17

## Goal

Deepen the first-pass sourcing audit before AES canonical stubbing. The question is not whether one outside project can replace AES. The question is which generic semantics already have an established authority so AES can remain a small residual integration/lifecycle layer.

## 1. Open Workflow Specification (OWS)

Source: https://github.com/open-workflow-specification/specification

Observed:
- CNCF Sandbox project;
- vendor-neutral workflow DSL ecosystem;
- current checked schema version `1.0.3`;
- JSON Schema 2020-12 schema;
- SDKs in multiple languages;
- multiple runtimes/reference implementations;
- workflow semantics include tasks, branching, events, service calls, schedules, timeouts, retries/fault handling and loops.

Disposition:
- **reference/adapt** for generic workflow semantics;
- **do not fork yet**;
- **do not replace Enforced Planning wholesale**;
- keep Enforced Planning-specific claim/worktree/session/governance semantics as a provider/residual layer.

## 2. Open Policy Agent (OPA / Rego)

Source: https://www.openpolicyagent.org/docs

Observed:
- graduated CNCF project;
- general-purpose policy engine;
- decouples policy decision-making from enforcement;
- Rego is a declarative language over structured data;
- embeddable / sidecar / service integration options;
- management model supports bundles, decision logs, status and discovery.

Fit to AES:
OPA is a strong candidate for **generic decision-policy evaluation**. It should be preferred over inventing an AES policy language or policy evaluator.

OPA does **not** define:
- who owns policy authority in AES;
- when an AES checkpoint should be invoked;
- engineering-specific recovery after a blocked decision;
- plan/gap/slice lifecycle semantics;
- evidence sufficiency or stakeholder utility semantics.

Disposition:
- **provider candidate** for policy decision evaluation;
- AES retains policy authority routing, checkpoint lifecycle and recovery semantics;
- do not create a generic AES policy DSL unless OPA/Rego fit testing fails.

## 3. W3C PROV

Sources:
- https://www.w3.org/TR/prov-primer/
- https://www.w3.org/TR/prov-constraints/

Observed:
- W3C Recommendation family;
- generic provenance model built around Entity, Activity and Agent;
- relations cover generation, use, derivation, attribution/responsibility and related provenance concepts;
- explicit validity/inference constraints;
- designed as an interchange model across heterogeneous systems.

Fit to AES:
PROV is a strong authority for **generic provenance relationships**. AES should not invent competing universal terms for artifact/activity/agent provenance when a projection into PROV is adequate.

PROV does **not** by itself establish:
- that evidence is sufficient to close an AES gap;
- verification polarity or failure-mode coverage;
- stakeholder utility;
- conformance to an AES normative target;
- planning/execution lifecycle semantics.

Disposition:
- **external provenance projection/reference**;
- AES retains evidence qualification, characterization and gap-reconciliation semantics.

## 4. in-toto

Sources:
- https://in-toto.io/docs/getting-started/
- https://in-toto.io/docs/specs/

Observed:
- stable specification v1.0 plus stable Attestation Framework v1.0;
- layouts specify expected supply-chain steps and authorized functionaries;
- signed link metadata records commands/materials/products for executed steps;
- final products can be verified against signed layouts.

Fit to AES:
in-toto is a strong candidate for **signed execution attestations / software-process custody** where AES needs tamper-evident evidence of specific engineering steps.

It does not replace:
- arbitrary AES observations;
- plan derivation;
- human review outcomes;
- gap recomputation;
- generic provenance interchange (PROV is broader).

Disposition:
- **provider candidate** for strong execution/attestation receipts;
- prefer composing in-toto predicates/attestations over hand-rolling signed step receipts where its model fits.

## 5. SLSA 1.2

Source: https://slsa.dev/spec/v1.2/

Observed:
- approved specification, current version 1.2;
- supply-chain security levels/tracks;
- provenance formats for source/build artifacts;
- build provenance is expressed using the in-toto attestation framework;
- provenance records where/when/how artifacts were produced, builder identity, parameters and dependencies.

Fit to AES:
SLSA is narrower than general AES evidence but highly relevant for **build/source provenance and verification of produced software artifacts**.

Disposition:
- **reuse/reference** for build/source provenance;
- do not recreate SLSA-like build provenance models inside AES.

## 6. SCIP

Source: https://github.com/scip-code/scip

Observed:
- language-agnostic code intelligence protocol;
- Protobuf schema;
- intended for definitions, references, implementations and other source navigation;
- multiple language indexers and bindings;
- Apache-2.0 license.

Fit to AES:
SCIP is a strong candidate for the **realized-code symbol identity layer**. It is materially better than AES inventing a universal cross-language symbol graph for functions/classes/methods/references.

Important boundary:
AES `planned implementation subject` is broader than an existing code symbol. A planned subject may not exist yet and may refer to a future module, adapter, model, CLI boundary or other realization target.

Disposition:
- **SCIP for realized code-symbol identity/navigation**;
- **AES residual for planned implementation subjects and their lifecycle**;
- add an optional mapping `planned_subject -> realized SCIP symbol(s)` after implementation.

## 7. Backstage Software Catalog

Sources:
- https://backstage.io/docs/features/software-catalog/system-model/
- https://backstage.io/docs/features/software-catalog/extending-the-model/

Observed:
- mature catalog model centered on Component, API and Resource;
- optional System and Domain abstractions;
- ownership and organizational entities;
- extensible versioned entity kinds based on Kubernetes-style metadata/spec objects;
- source-controlled YAML descriptors are a first-class ingestion mechanism.

Fit to AES:
Backstage is a strong candidate for **software ecosystem catalog/topology vocabulary** and ownership projections.

It does not model:
- target/current/gap;
- implementation slices;
- provider sourcing decisions;
- epistemic state or evidence sufficiency;
- engineering execution custody.

Disposition:
- **reference/adapt** for software catalog entities and relations;
- do not create a competing universal AES software catalog model without a demonstrated gap.

## 8. OASIS TOSCA 2.0

Source: https://docs.oasis-open.org/tosca/TOSCA/v2.0/TOSCA-v2.0.html

Observed:
- OASIS standard;
- formal topology model;
- reusable capability types with properties/attributes;
- requirements on one node can be fulfilled by capabilities on another;
- broader node/relationship/service-topology semantics.

Fit to AES:
TOSCA is the strongest standards candidate found so far for a generic **capability/requirement topology** vocabulary.

Caution:
TOSCA is oriented toward service/application topology and deployment modeling. AES capability selection is agent-facing and provider/evidence-oriented. Direct adoption may be semantically awkward if we force planning or reusable software functionality into infrastructure/service-template assumptions.

Disposition:
- **semantic reference + projection experiment**;
- do not adopt TOSCA wholesale yet;
- before defining an AES/ACA `CapabilityDescriptor`, explicitly compare the required fields against TOSCA Capability/Requirement/Node/Relationship semantics.

## 9. SysML v2 / KerML

Sources:
- https://www.omg.org/sysml/sysmlv2/
- https://www.omg.org/spec/SysML/2.0/About-SysML

Observed:
- OMG SysML v2 formally adopted in 2025;
- KerML provides a formal semantic kernel;
- SysML v2 addresses requirements, behavior, structure, analysis and verification with traceability;
- standard API/services specification exists for interoperability;
- machine-readable JSON representations are part of the formal publication set.

Fit to AES:
SysML v2/KerML is a valuable **metamodel reference** for relationships among requirements, behavior, structure, verification and traceability.

Caution:
It is much broader/heavier than AES needs for normal repository execution. Treating SysML v2 as the runtime data model could introduce substantial conceptual and tooling overhead.

Disposition:
- **reference, not dependency** at this stage;
- use it to challenge AES-local concepts and relation names before inventing them;
- only adopt API/model artifacts if a concrete interoperability use case emerges.

## 10. JSON Schema 2020-12

Source: https://json-schema.org/specification

Observed:
- current published JSON Schema version remains Draft 2020-12;
- standard core + validation vocabulary;
- broad language/tool support.

Disposition:
- **default generic JSON-shape authority** where applicable;
- Pydantic may remain a Python implementation/convenience layer, but AES should not define a competing schema language.

## 11. OpenAPI 3.2

Source: https://spec.openapis.org/oas/v3.2.0.html

Observed:
- OpenAPI 3.2.0 published September 19, 2025;
- programming-language-agnostic interface description for HTTP APIs.

Disposition:
- **native authority for HTTP API descriptions**;
- do not encode HTTP API semantics into bespoke AES contracts.

## 12. AsyncAPI 3.0

Source: https://www.asyncapi.com/docs/reference/specification/v3.0.0

Observed:
- protocol-agnostic machine-readable description for message-driven APIs;
- applies across Kafka, AMQP, MQTT, WebSockets, HTTP and others.

Disposition:
- **native authority for event/message API descriptions** where applicable.

## Cross-cutting architecture conclusion

The emerging canonical shape is layered:

```text
external standards / mature OSS
    topology: Backstage / TOSCA / SysML reference
    workflow: OWS
    policy evaluation: OPA
    provenance: W3C PROV
    signed execution evidence: in-toto
    build/source provenance: SLSA
    code symbols: SCIP
    schemas/interfaces: JSON Schema / OpenAPI / AsyncAPI
                    ↓
provider adapters / projections
                    ↓
AES-local residual semantics
    target / current / gap
    slice
    planned implementation subject
    verification-subject linkage
    provider sourcing disposition
    authority + epistemic state
    attention checkpoint
    evidence qualification / reconciliation
    learning feedback
                    ↓
selected execution/planning providers
    Company Planning
    Enforced Planning
    ACA
    others only after positive fit
```

## Canonical stubbing consequences

### Safe classes of stubs

- adapters/projections onto external standards;
- AES-local lifecycle/value types proven residual;
- provider ports/interfaces;
- mappings between planned subjects and realized external identifiers;
- verification/evidence reconciliation boundaries.

### Unsafe classes of stubs until fit testing

Do not introduce universal AES-local versions of:

- `Workflow`, `Task`, `RetryPolicy`, `Schedule`;
- `Policy`, generic policy language/evaluator;
- `ProvenanceEntity`, `Activity`, `Agent` equivalents;
- `CodeSymbol` / generic symbol graph;
- generic software `Component`/`API`/`Resource` catalog entities;
- generic `Capability` / `Requirement` topology;
- generic JSON/API schema language.

## Next research questions

1. Can an actual Enforced Planning work graph be projected into OWS without loss of its generic workflow portion?
2. Can ACA capability manifests map cleanly to TOSCA capability/requirement/node semantics, or is TOSCA too deployment-centric?
3. Can Enforced Planning receipts and AES evidence be represented as PROV + in-toto/SLSA without losing AES-specific evidence qualification?
4. Can planned implementation subjects bind to SCIP symbol identifiers after realization while preserving pre-realization identity?
5. Can Backstage entity descriptors serve as optional software-topology input/output without making Backstage a runtime dependency?
6. Is OPA sufficient for AES policy evaluation while AES retains policy authority and recovery semantics?

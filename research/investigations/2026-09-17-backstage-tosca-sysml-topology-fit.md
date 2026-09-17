# Fit comparison — Backstage, TOSCA 2.0, and SysML v2 for AES topology/metamodel

Status: discriminating research
Date: 2026-09-17

## Purpose

AES needs a coherent vocabulary for repositories, software components, APIs, resources, systems, capabilities, requirements, relationships, planned implementation subjects, verification and traceability. Three external families overlap enough that choosing one blindly would be a mistake:

- Backstage Software Catalog;
- OASIS TOSCA 2.0;
- OMG SysML v2 / KerML.

This record distinguishes their natural authority zones before AES canonical stubbing.

## Backstage

Sources:
- https://backstage.io/docs/features/software-catalog/system-model/
- https://backstage.io/docs/features/software-catalog/extending-the-model/

### Natural center

Operational software ecosystem catalog / discoverability.

Core concepts:
- Component;
- API;
- Resource;
- System;
- Domain;
- User / Group;
- ownership/relations;
- source-controlled entity descriptors;
- extensible versioned entity kinds based on Kubernetes-style metadata/spec semantics.

### Strong fit for AES

- repository/ecosystem inventory projections;
- software ownership and discoverability;
- component/API/resource/system relationships;
- optional interoperability with an existing developer portal/catalog;
- generated catalog descriptors as a derived view of AES/native authorities.

### Weak fit

Backstage does not naturally model:
- target/current/gap;
- requirement satisfaction semantics;
- capability-provider matching;
- verification adequacy;
- planning slices;
- provenance/evidence qualification;
- execution custody.

### Disposition

**Use as operational software-catalog vocabulary/projection candidate.** Do not make Backstage the AES metamodel or mandatory runtime.

## TOSCA 2.0

Source:
- https://docs.oasis-open.org/tosca/TOSCA/v2.0/TOSCA-v2.0.html

### Natural center

Typed service/application topology and orchestration.

Core concepts:
- Node Type / Node Template;
- Capability Type / Capability Definition;
- Requirement Definition / Requirement Assignment;
- Relationship Type / Relationship Template;
- interfaces;
- artifacts;
- properties/attributes;
- matching/fulfillment constraints and filters;
- multiplicity/optional requirements.

### Strong fit for AES

- formal capability ↔ requirement topology semantics;
- typed relationships between provider/consumer nodes;
- exposed interfaces and artifacts;
- dependency resolution vocabulary;
- constraints and requirement fulfillment.

### Weak fit

TOSCA is deployment/service-topology oriented and does not naturally model:
- evidence-backed maturity/promotion;
- gap/slice lifecycle;
- agent-facing semantic action identities;
- stakeholder utility;
- verification adequacy;
- pre-code planned-subject realization state.

### Disposition

**Use as semantic baseline for generic capability/requirement/node/relationship concepts.** Run projections/fit tests before defining competing AES/ACA terms. Do not require a TOSCA orchestrator.

## SysML v2 / KerML

Sources:
- https://www.omg.org/sysml/sysmlv2/
- https://www.omg.org/spec/SysML/2.0/About-SysML

### Natural center

Formal systems modeling and traceability across structure, behavior, requirements, analysis and verification.

Observed strengths:
- formal semantic foundation through KerML;
- explicit requirements modeling;
- structure and behavior modeling;
- analysis and verification relationships;
- traceability across model elements;
- standardized API/services and machine-readable artifacts.

### Strong fit for AES

- challenge/reference model for requirement → behavior → structure → verification relationships;
- relationship naming/semantics sanity check;
- formal distinction between model elements that AES might otherwise collapse;
- potential future interoperability with systems-engineering tools.

### Weak fit

- substantially broader/heavier than the repository-engineering lifecycle AES needs;
- adopting SysML/KerML as AES's runtime persistence model would impose significant conceptual/tooling overhead;
- does not directly provide AES gap/slice/provider-sourcing/evidence-adequacy semantics.

### Disposition

**Use as a metamodel/reference authority, not a runtime dependency at bootstrap.** Consult it before inventing generic requirement/verification/structure relationships.

## Comparative authority zones

| Need | Best external starting point | Why |
| --- | --- | --- |
| software ecosystem catalog | Backstage | purpose-built Component/API/Resource/System/Domain/ownership vocabulary |
| generic capability/requirement topology | TOSCA 2.0 | formal matching/fulfillment semantics between typed nodes/capabilities/requirements |
| formal systems traceability | SysML v2 / KerML | requirements + behavior + structure + analysis + verification with formal semantics |
| runtime developer portal | Backstage | mature operational platform |
| deployment orchestration topology | TOSCA | natural domain |
| AES planning/gap lifecycle | none of these | AES residual |
| planned implementation subject | none directly | AES residual, later maps to files/SCIP symbols |
| evidence adequacy / gap closure | none directly | AES residual |

## Recommended AES canonical layering

Do not seek one universal topology graph.

Use a small AES relationship/core layer that can reference external semantic identities and produce concern-specific projections:

```text
AES lifecycle identities
  target / gap / plan / slice / planned subject / verification subject
                    |
                    +---- software catalog projection ----> Backstage
                    |
                    +---- capability topology projection -> TOSCA
                    |
                    +---- systems traceability mapping ---> SysML v2/KerML
                    |
                    +---- realized code mapping ----------> SCIP
```

This prevents the AES core from becoming a union of every external metamodel.

## Implication for "stub the whole canonical repository"

The complete repository skeleton can still be stubbed first, but the stubs should be **ports/projections/residuals**, not copied external domain models.

Examples of safe conceptual homes:

```text
integrations/backstage/      # projection/adapter
integrations/tosca/          # projection/adapter
integrations/sysml/          # optional mapping/reference adapter
integrations/scip/           # code realization/index mapping

lifecycle/                   # AES-local target/current/gap/reconciliation
planning/                    # provider ports + AES slice linkage
subjects/                    # planned implementation/verification subjects
providers/                   # provider selection/binding dispositions
evidence/                    # qualification/freshness/characterization residual
```

Exact filesystem names are not frozen by this research record.

## Anti-patterns to avoid

- copying Backstage `Component` into an AES `Component` class and changing its meaning;
- creating a local `Capability` that silently differs from TOSCA capability semantics;
- adopting the entire SysML/KerML metamodel as AES persistence merely because it is formal;
- one giant graph schema containing every concept from all three standards;
- treating one external projection as canonical authority over native systems.

## Conclusion

Backstage, TOSCA and SysML are complementary, not competing replacements:

- **Backstage:** operational software catalog;
- **TOSCA:** typed capability/requirement topology;
- **SysML v2/KerML:** formal systems-model/traceability reference.

AES should remain the lifecycle/reconciliation layer that binds these representations to exact authorities and evidence rather than cloning their vocabularies.

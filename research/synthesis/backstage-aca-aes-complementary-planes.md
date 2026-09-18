# Backstage, ACA, and AES as complementary engineering planes

Status: research synthesis; non-normative idea only.

Purpose: preserve a candidate architectural framing that emerged from comparing Backstage, the Agentic Capability Architecture (ACA), and canonical AES. This note does not adopt Backstage, change AES boundaries, transfer capability ownership, or select a runtime dependency.

## Idea

Treat the three systems as potentially complementary planes rather than competing catalogs or a single merged ontology:

- **Backstage / developer-experience plane:** human-facing software discovery, catalog views, documentation, search, integrations, and workflow entry points.
- **ACA / capability plane:** provider-independent semantic capability identities, verified executable exports and typed interfaces, capability discovery, selection/rejection, composition, local residuals, and reuse evidence that can compound across projects.
- **AES / engineering-control plane:** intent, policy, planning, execution, observation, evaluation, evidence, feedback, replanning, and learning across the complete engineering loop.

A compact framing is:

```text
Backstage: What software exists, who owns it, and how do I navigate/use it?
ACA:       What known executable behavior can satisfy this requirement, and what must remain local?
AES:       What engineering transition should occur, is it admissible, what happened, and what should change next?
```

## Candidate relationship

```text
                    Backstage
              developer experience
                     /     \
                    /       \
                   v         v
                 ACA <----> AES
          capability plane   engineering-control plane
                   \         /
                    \       /
                     v     v
              executable systems
                     |
                     v
                  evidence
                  /      \
                 v        v
                ACA      AES
          reuse knowledge  engineering state
```

Backstage could therefore be an **AES/ACA client and projection surface**, not an authority layer. It could expose software topology and human workflows while projecting governed AES state and ACA capability knowledge.

## Why the separation may matter

### Software entities are not capabilities

Backstage primarily models the software estate: components, APIs, resources, systems, ownership, and relationships. ACA's semantic unit is different: a capability such as `notification.email.send` or `approval.resolve` can remain stable while its provider changes.

This suggests preserving a distinction between:

```text
software identity
capability identity
engineering-state identity
```

rather than forcing all three into one catalog ontology.

### Inventory is weaker than executable capability knowledge

Knowing that a notification service exists is not equivalent to knowing that a verified, typed action satisfies `notification.email.send`. ACA's distinction between discovery metadata and verified executable exports could provide the agent-facing semantic bridge from required behavior to implementation candidates.

### Capability decisions can become part of the AES loop

A possible end-to-end path is:

```text
engineering intent
    -> required behavior
    -> capability discovery
    -> select / reject / compose / declare local residual
    -> policy/admission
    -> execute
    -> observe
    -> evaluate
    -> evidence
    -> feedback
       -> AES current state / replanning
       -> ACA compatibility, rejection, maturity, and reuse knowledge
```

This would let execution evidence improve both engineering control and future capability-selection decisions without making either system the other's source of truth.

### Human portal, CLI, and agents could share governed semantics

If Backstage is a projection/client rather than authority, a Backstage UI, an AES CLI, and coding agents could operate against the same underlying identities and evidence while presenting different views. The portal would not become a second editable home for AES normative/current truth.

## Research questions

1. What is the minimum contract between AES and ACA for expressing a required behavior and returning capability candidates, verified boundaries, compatibility evidence, and declared local gaps?
2. Should AES reference ACA semantic capability IDs directly, or should a separate stable cross-system identity contract mediate them?
3. Which evidence should feed both systems, and how can each system interpret the same observation without transferring authority?
4. How should rejected capability fits be represented so future agents benefit from negative architectural knowledge without treating old rejection evidence as permanently valid?
5. Can Backstage project AES/ACA state without duplicating mutable authority?
6. Which Backstage catalog entities should link to capabilities versus merely to providers/components?
7. Can an agent traverse `engineering requirement -> capability -> provider -> execution -> evidence -> changed capability knowledge` with revision-bound provenance and no hidden source-of-truth duplication?
8. Does this separation improve agent performance enough to justify the discovery, integration, and maintenance cost?

## Candidate experiment

Use one authentic AES engineering transition that requires a capability already represented in ACA.

Compare:

- a control path where the agent starts from repository/software discovery alone; and
- a treatment path where AES expresses required behavior, ACA returns verified capability candidates plus relevant evidence, and the agent records selection/rejection/local residual before execution.

Measure at least:

- bespoke code written;
- discovery/context cost;
- time to a correct implementation;
- capability reuse/composition;
- incorrect candidate selection;
- policy/evidence completeness;
- whether real-use evidence changes a later fresh agent's capability decision.

A Backstage projection can be evaluated separately as a human/operator experience question rather than being required for the core AES↔ACA experiment.

## Non-claims

This note does **not** establish that:

- AES should depend on Backstage;
- Backstage should own AES or ACA state;
- ACA should become the AES capability registry;
- the three systems should share one ontology;
- a portal is required for AES;
- the proposed integration produces a net benefit.

Those remain research questions requiring explicit provider sourcing, contract design, and authentic evidence before architectural adoption.

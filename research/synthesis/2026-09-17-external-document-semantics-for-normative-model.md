# External documentation semantics for the AES normative record model

Status: research synthesis; non-normative.

Date: 2026-09-17

## Purpose

Use established requirements, architecture-description, and executable-specification
semantics to sharpen the AES documentation model without importing a large document
taxonomy or making external standards runtime dependencies.

## Sources inspected

- ISO/IEC/IEEE 29148:2018 — requirements engineering. The 2018 edition remains
  current as of 2026 while a replacement draft is under development.
- ISO/IEC/IEEE 42010:2022 — architecture description.
- SysML v2 / KerML — requirements, behavior, structure, analysis, verification,
  and traceability reference.
- Cucumber/Gherkin — Feature / Rule / Example(Scenario) / Given-When-Then as an
  executable-specification vocabulary.

These are semantic/reference sources only. No conformance claim or paid-standard
text reproduction is made here.

## Transferable semantics

### Requirements engineering

Useful ideas:

- a requirement is an identifiable obligation, not merely prose in a document;
- requirements have lifecycle and traceability;
- the information item matters more than a particular file format;
- verification/validation information must remain distinct from the requirement itself.

AES implication:

A requirement should be a typed record/section with stable identity and scope.
It does not need a dedicated "requirements document" file if the canonical
structured record already owns it.

### Architecture description

Useful ideas:

- architecture and its description are distinct;
- stakeholders have concerns;
- views/viewpoints organize concern-specific representations;
- a standard can constrain architecture-description structure without mandating
  the storage format or architecting method.

AES implication:

Use one canonical normative model plus generated concern-specific views. A PRD,
architecture page, component map, or source-local context can be a view without
becoming a second authority.

### SysML v2

Useful ideas:

- requirements, behavior, structure, verification and their traceability are
  different model elements;
- richer traceability can exist without forcing every element into one kind;
- machine APIs can expose a model independently from its human diagrams.

AES implication:

Keep requirement, component/boundary, check/evidence and relationship semantics
distinct, but do not adopt SysML wholesale for the bootstrap.

### Executable examples

Gherkin usefully separates:

- Feature — behavior/outcome grouping;
- Rule — business/normative rule;
- Example/Scenario — concrete example of the rule;
- Given / When / Then — initial context, event/action, observable outcome.

AES implication:

A canonical example or user journey can be a first-class scenario record under
a system/product/component scope. It does not require Cucumber or a .feature file
unless executable BDD is actually useful for that component.

## Proposed minimal semantic vocabulary

The smallest useful canonical authored vocabulary appears to be:

- goal / north_star
- actor
- outcome
- journey_or_scenario
- requirement_or_invariant
- seam_obligation
- question (AQR)
- decision reference
- component
- boundary/contract reference
- verification obligation / check reference

Research, plans, decisions and evidence retain separate native lifecycle records
because their authority and mutability differ materially from normative target.

## Anti-explosion rule

Do not map each semantic type to a mandatory file.

Instead:

- one system-level normative record can contain goals, actors, outcomes, journeys,
  requirements, seams, questions, and references;
- one component-level normative record can contain component-scoped requirements,
  scenarios, questions, boundary references and verification obligations;
- conventional documents are generated views when a human consumer needs them.

The relevant unit is the typed semantic record, not the conventional document title.

## Current disposition

Use these standards as vocabulary checks only. The AES bootstrap should remain
lightweight and prove that one system record plus component records can generate
the needed views before adding additional canonical record families.

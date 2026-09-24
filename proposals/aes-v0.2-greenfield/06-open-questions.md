# AES v0.2 open questions after semantic review

Status: **active proposal review queue / non-normative**
Date: 2026-09-24

The first four clean-sheet passes resolved several earlier ambiguities. This file
now lists only questions still material to the next architecture gate.

## Semantic model

1. Is realization unit the right semantic boundary, and should its conventional
   public name be component?
2. Are the candidate normative-item kinds useful enough to freeze, or should kind
   remain extensible/non-normative metadata?
3. What exact form should a criterion's multi-evidence sufficiency rule take
   without creating a custom logic language?
4. Do any load-bearing relationships remain that cannot live in typed owning
   facts or be derived, thereby justifying a separate authored relationship type?
5. Does the Greenfield MVP need a first-class durable decision type, or are
   accepted target facts plus plan/provider rationale sufficient initially?

## Materialization and storage

6. What is the minimum canonical structured storage layout for outcomes,
   normative items, criteria, realization commitments and planning state?
7. Should target semantics be stored in one project-level structured record,
   realization-unit-local records, or another partition?
8. Which data is required to be YAML specifically versus another structured
   representation?
9. How are stable semantic IDs allocated and kept stable across path renames or
   record repartitioning?
10. How are accepted target changes committed atomically with source/topology
    changes so generated views cannot observe a half-migrated state?
11. What exact materialization does the initialization contract create for a
    fresh project?

## Planning

12. What is the minimum AES planning input/output contract once the semantic
    target model is accepted?
13. How are planning uncertainty, probes and stopping rules represented without a
    universal question/epistemic-planning subsystem?
14. Which provider-binding facts are required for ordinary package/tool
    dependencies versus only capability-level provider choices?
15. What exact criteria decide when a public/load-bearing symbol/signature becomes
    a target commitment?
16. How should planned dependency intent be represented where it is consequential
    without authoring a universal dependency graph?

## Verification, evidence, current and gap

17. What minimal representation expresses evidence requirements involving AND/OR,
    thresholds, human disposition, or repeated observations without becoming a
    general policy language?
18. Who/what is allowed to produce evidence assessments, and how is the assessor
    identity/version bound?
19. What dependency closure is sufficient to invalidate evidence after a change?
20. What exact current-state vocabulary should be user-facing versus derived from
    freshness/adequacy/standing dimensions?
21. What exact gap states are needed beyond open/partial/unresolved/closed/not-yet-
    applicable?
22. How are human-review and LLM-rubric observations retained in a durable,
    inspectable form?

## Realized repository characterization

23. What is the first supported source/runtime ecosystem for the Greenfield MVP?
24. What native analyzer/standard/provider best characterizes that ecosystem?
25. How deep must observed dependency analysis go for context, invalidation and
    target-realized comparison?
26. How are dynamic/uncertain dependency observations represented without false
    certainty?
27. How are tool-managed durable artifacts and generated families characterized
    back to the exact accepted generation rule?

## Working context and projections

28. Which delivery mechanism best satisfies full-text subject-local context:
    generated source regions, sidecar, agent/IDE injection, or hybrid?
29. How is context completeness tested without projecting the entire repository?
30. How are context relevance and dependency consequences derived without a
    heuristic ranking platform becoming the product?
31. What generated human navigation/review surface is necessary for the first MVP,
    if any, beyond the agent working context?

## Distribution

32. What installation/package form makes AES independently usable by colleagues?
33. What defaults must ship so ordinary Greenfield use does not require provider
    expertise?
34. Which settings are product configuration versus accepted project target and
    therefore must not be conflated in one generic config file?
35. What secrets/environment-specific values must remain outside governed target
    records?

## Validation

36. Which genuinely fresh project will serve as the first authentic consumer?
37. How will the projected-context control condition be isolated from hidden
    conversational context?
38. What measured or qualitative result is sufficient to continue the context
    projection direction without pretending one project proves universality?
39. Which deliberate falsifiers from the validation profile are safe and
    representative enough to count?

## History and versioning

40. What exact acceptance event promotes v0.2 proposal semantics into current AES
    normative authority?
41. Which v0.1 research/evidence remains physically in the live tree versus only
    reachable through Git history/tags?
42. What change threshold requires AES v0.3 instead of an additive v0.2 capability
    or maturity increment?
43. Does the Greenfield MVP reveal any semantic lifecycle information that truly
    justifies an append-only event layer beyond Git, accepted authorities and
    revision-bound observations/evidence?

## Explicitly deferred

Not prerequisites for the Greenfield MVP:

- arbitrary existing-repository retrofit;
- universal language/framework support;
- organization/portfolio-wide orchestration;
- generalized self-modifying policy;
- extracting AES capabilities into separate repositories without a demonstrated
  ownership/release boundary.

# Source-local normative context dogfood result

Status: research synthesis; **BP-D1 pilot-supported, not accepted architecture**

Date: 2026-09-17

## Probe

The first source-local context probe used the real
`RepositoryContextResolver.resolve` implementation at PR #5 revision
`9f82f3500e4a472b26756c31ea9205f908d7c394`.

A generated projection was placed at the intended component location:

`src/agentic_engineering_system/repository_context/component.context.generated.yaml`

It binds exact normative text, Plan 001 acceptance criteria, the realized code
symbol, native checks, current/freshness state, and open gap state without
claiming independent authority.

## Observed correction: shared is not the same as locally relevant

The first draft inherited every repository-wide "shared" clause into the local
packet. That produced twelve clauses for one resolver boundary, including
methodology, provider-sourcing and attention-economics text that is important
globally but not normally needed to edit this resolver.

The blueprint was revised so repository-governing clauses are a **catalog**, not
a blanket injection list.

The source-local model now distinguishes:

1. **direct component norms** — normally shown verbatim;
2. **context-delivery / seam norms** — shown because they govern this local
   projection or an incident seam;
3. **outcome context** — why the component exists in the current vertical;
4. **conditional norms** — pulled in only when a named trigger is activated;
5. **plan acceptance criteria** — exact current-plan obligations;
6. **current / gap state** — evidence-bound state, not normative prose.

This better matches "all relevant context at the code location" than "all global
context at every symbol."

## Verbatim wording proved useful immediately

The first exact-source validation failed because AC-003 had been shortened in
the generated projection. The authoritative Plan 001 wording is materially more
specific about a physical local wiki not being promoted by path existence and
about bounded-fixture behavior.

The projection was corrected rather than normalized. The corrected exact-source
check passes.

This is positive evidence for the rule:

> local normative text may be duplicated **only as a generated verbatim
> projection of one owning source**.

## Component versus symbol linkage

The pilot supports a compact division:

```text
component
  owns/collects coherent normative responsibility once
      ↓
symbols inherit that component context for routing/comprehension
      ↓
only narrower/load-bearing symbol obligations get explicit symbol links
```

For repository context, existing relationships already make this useful:

- `RepositoryContextResolver` directly maps to AC-001 through AC-003;
- `AuthoritySurfaceObservation` maps to AC-004;
- `RepositoryContextArtifact` maps to AC-005;
- `PilotManifestAdapter` maps to AC-006 and AC-007;
- the recovery rule maps to AC-008.

There is no reason to duplicate every component requirement onto every helper
function.

## Freshness result

The sidecar records the real source symbol at the pinned PR #5 revision, but
does **not** promote earlier successful execution into fresh verification at that
revision. Source presence, technical evidence and utility remain separate.

## Negative controls

The exact-source checker rejected:

- paraphrased normative text;
- an omitted direct clause;
- changed Plan 001 wording;
- a changed conditional trigger;
- a missing code symbol;
- a missing native check;
- false promotion to fresh verification;
- false gap closure.

The durable receipt is
`evidence/bootstrap-alignment/repository-context-source-local-observation-001.json`.

## Disposition

**Continue with the compact component-local model.**

BP-D1 is pilot-supported, not an accepted repository-format contract.

The next low-risk step is now justified: materialize the remaining reserved
component filesystem homes using explicit **unrealized/unresolved placeholders**
only. Do not invent classes, functions, provider APIs, or typed seams that remain
open AQRs. This lets the whole intended shape exist without pretending its
behavior or abstractions are settled.

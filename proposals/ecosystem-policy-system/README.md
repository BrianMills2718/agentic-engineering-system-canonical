# Ecosystem policy system — model before repair

Status: shaping; descriptive model, not adopted policy.
Authority: derived from the pinned sources in `review-page/sources.json`.

Brian asked to investigate, assess and critique the ecosystem policies on
2026-10-06, approved the recommendations, then directed: “i want to model the
system first”. Implementation of the proposed repairs is therefore held while
this model is presented.

The existing accepted seven-system architecture is the starting point:
Project Meta's `docs/ops/ADR-2026-07-16-engineering-control-plane-system-model.md`.
This model does not transfer any capability owner, replace an authority, or
claim that a documented interaction is implemented end to end.

Open [the system model](review-page/index.html). It has four linked views:

- **Whole system:** seven responsibilities, rather than seven repositories.
- **Policy loop:** how definitions reach an action and feedback returns.
- **Records:** the distinct policy, decision, observation and concern records.
- **Concern lifecycle:** the transitions needed for verified correction.

An evidence view keeps reproduced check defects, a runtime hook-trust snapshot
and a recorded write-handoff incident separate. The hosted review URL is
`https://hive.brianmills.dev/plans/shaping-ecosystem-policy-model/proposals/ecosystem-policy-system/review-page/index.html`;
the existing private plans index identifies the branch and committed version.
Brian reported HTTP 403 on that hosted link. The access defect remains open
in [Project Meta #2410](https://github.com/BrianMills2718/project-meta/issues/2410).
The committed HTML also opens locally; Brian confirmed that local model appears.

## Use the model: missing-evidence walkthrough

Brian approved tracing this failure on 2026-10-06. Open the
[executed failure trace](review-page/failure-trace/index.html) from the model's
**Failure trace** link. It maps six stages onto the existing model parts and
marks verified contracts, isolated executions, reproduced breaks, and the
live hook-execution boundary that remains untested.

The [retained probe](review-page/failure-trace/probe.py) runs the actual Project
Meta index, check, CLI, and router with temporary observations and an isolated
concern adapter. At the exact revision in
[its output](review-page/failure-trace/probe-output.json), eight checks pass
by reproducing three false-clear cases and the downstream close request.
No live concern was closed by this probe. The owning repair concern is
[Project Meta #2412](https://github.com/BrianMills2718/project-meta/issues/2412).

The root break is the conversion from evidence to status. Coverage and mapping
uncertainty are present in evidence prose but do not constrain `clear`, which
the concern router treats as permission to close. The existing `unknown`
route leaves concerns open. Repairs remain outside this modeling increment.

Reproduce with `PYTHONDONTWRITEBYTECODE=1 python3
review-page/failure-trace/probe.py <project-meta-checkout>
review-page/failure-trace/probe-output.json`, then `node
review-page/failure-trace/render.mjs <project-meta-checkout>`.

The machine-readable architecture is [system.c4](review-page/system.c4), using
the existing LikeC4 implementation from Representation Router. The page is a
self-contained read-only projection of that model. Sources, owner mappings and
observations are annotations; they do not create a parallel policy registry.

Success means Brian can trace one policy from definition through applicability,
guidance/checks, an agent action, observation, an owned concern, correction and
verification; distinguish current, partially implemented and intended links;
and locate the authority for any modeled responsibility or record.

Scope is the engineering control plane's policy system. Individual company
business rules, every repository's local implementation, a universal world
ontology and automatic claims of policy effectiveness are outside this model.

## Reproduce the projection

Use an existing Representation Router checkout with its installed LikeC4:

```sh
<representation-router>/node_modules/.bin/likec4 validate review-page
<representation-router>/node_modules/.bin/likec4 export json review-page --pretty -o review-page/layout.json
node review-page/render.mjs
```

The renderer is a bounded artifact adapter, retained beside this first model;
it is not a new ecosystem CLI or runtime service. Validation establishes model
consistency. Browser verification establishes the exercised interactions.
Neither establishes full system conformance or Brian's acceptance.

`use-case.json`, `recommendation.json`, `surface-spec.json` and the router
disposition are retained beside the page. The router proposed a scroll-linked
explainer; the surface uses explicit stages selected by view buttons, one
main drawing and one persistent inspector. LikeC4 is the existing
planning-review architecture implementation. No scroll-driven transition,
chat interface or new planning database was added.

Feedback remains the owning Project Meta policy/concern loop. A correction to
this projection changes the model; a change to an actual rule belongs in its
canonical authority and remains a separate step.

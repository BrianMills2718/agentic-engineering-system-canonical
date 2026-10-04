# AES v0.2 unresolved decisions for fresh review

Status: **active review queue / non-normative**
Date: 2026-09-24

This file intentionally contains only decisions that remain material after the
clean-sheet, materialization, provider and product-surface passes.

For the current architecture, start at `REVIEW.md`.

## Semantic boundary

### 1. Realization unit name and split rule

**Resolved 2026-09-25 (D3 in `24-pre-probe-decisions.md`): public term is `component`.**

Candidate direction:

- keep the semantic concept;
- use it to group artifacts with coherent responsibility/context/ownership/
  replacement/verification/failure boundaries;
- likely expose the conventional public term `component`.

Review question:

Is this a real necessary semantic boundary, or can artifact/capability ownership
cover the same need without another first-class concept?

### 2. Normative-item kinds

Candidate direction:

Keep `behavior | constraint | invariant | quality | policy | other` as useful
classification metadata, but do not make planning or conformance depend heavily
on the taxonomy.

Review question:

Should the kinds be frozen in v0.2, extensible, or removed from the MVP?

### 3. Evidence-requirement composition

**Resolved for the MVP 2026-09-25 (D2 in `24-pre-probe-decisions.md`): conjunction-only.**

Candidate direction:

A success criterion can require one or more evidence requirements with an
explicit sufficiency rule.

Review question:

What minimum representation supports conjunction/disjunction, thresholds,
repeated observations, and human/model judgment without creating a general
policy/logic language?

### 4. Separate authored relationship semantics

Candidate direction:

No universal authored relationship registry. Typed owning refs plus observed and
derived relationships are sufficient so far.

Review question:

Is there a concrete load-bearing relationship that cannot truthfully live in an
owning record or be derived? If not, keep the generic registry out.

### 5. First-class durable decision type

Candidate direction:

Not required yet for the Greenfield semantic kernel; target facts, plan rationale
and provider dispositions carry the immediate architecture.

Review question:

Does the MVP need durable decision records to preserve why an accepted target
choice was made independently of a historical plan?

## Materialization

### 6. One project-level target.yaml

Candidate direction:

Use one `.aes/target.yaml` for the Greenfield MVP to preserve atomic review and
avoid premature partition/synchronization machinery.

Review question:

Is this appropriately simple, or is the file likely to become an unusable
monolith before the MVP proves the architecture?

### 7. Stable semantic ID grammar

Candidate direction:

IDs survive storage repartition and path renames when the semantic subject
survives.

Review question:

What minimum namespace/grammar prevents collision and accidental identity change
without creating a registry service?

### 8. Target-acceptance atomicity

Candidate direction:

Target/topology/verification changes and corresponding repository mutations must
land as one internally reconcilable accepted revision. Authority files do not
self-embed their own Git SHA.

Review question:

Is Git revision + content identity sufficient, and which exact mutations must be
atomic for MVP correctness?

## Planning/topology

### 9. Provider-binding threshold

Candidate direction:

Create an AES provider binding when an external/provider choice materially
satisfies an AES capability or changes the accepted realization boundary; do not
model every ordinary package dependency as an AES provider.

Review question:

Where is the clean threshold?

### 10. Selected symbol commitment threshold

Candidate direction:

Plan only public/load-bearing symbols whose identity/signature/type/narrower
obligation or verification role is itself a target commitment.

Review question:

Is the threshold mechanically reviewable enough to avoid both symbol bureaucracy
and hidden architecture drift?

### 11. Intended dependency commitments

Candidate direction:

Represent consequential intended dependencies only where planning needs them;
observed dependencies come from characterization and impact/relevance edges are
derived.

Review question:

What is the smallest target representation that can express a consequential seam
without becoming a universal dependency graph?

## Evidence/current/gap

### 12. Evidence-assessment materialization

Candidate direction:

Observation is retained. Freshness/adequacy/standing is a separate assessment with
assessor provenance. Exact file placement is still undecided.

Review question:

Should assessments be retained records, reproducible generated projections, or a
hybrid depending on whether judgment is deterministic?

### 13. Assessor identity

Candidate direction:

Every non-trivial evidence assessment identifies the assessor implementation and
version; human/model judgments additionally identify the reviewing actor/provider
as applicable.

Review question:

What identity is sufficient for deterministic AES code, humans, and model-based
rubrics without overbuilding attestation infrastructure?

### 14. Evidence invalidation closure

Candidate direction:

Invalidate evidence when a material subject/dependency changes, using intended
and observed dependency facts conservatively.

Review question:

How much transitive closure is required for the MVP before invalidation becomes
too broad or too weak?

### 15. User-facing current/gap vocabulary

Candidate direction:

Keep freshness/adequacy/standing as underlying dimensions; project concise
human-facing states such as unrealized, unverified, supported, contradicted,
stale/error/insufficient.

Review question:

Which states should be contractual versus merely UI projection?

### 16. Human and model evidence retention

Candidate direction:

Retain a durable review/observation artifact or reference with exact criterion,
inputs, assessor identity and disposition.

Review question:

What is the minimum inspectable record for human review and LLM-rubric evidence?

## Characterization/context

### 17. Python characterization provider

Candidate direction:

Git + stdlib `ast` is the minimum first implementation. Run a bounded comparison
against Griffe before final characterizer binding; add LibCST only after a failed
requirement.

Review question:

Does Griffe materially improve symbol/public-API identity enough to justify a
runtime dependency, or should the MVP stay stdlib-only?

### 18. Working-context MVP boundary

Candidate direction:

`aes context <subject>` is the core delivery contract. Automatic agent/IDE
injection is deferred to adapters.

Review question:

Can completeness and usefulness be validated through explicit packet delivery
without weakening the product claim, and how should optional relevance be bounded
without silently omitting required context?

## Distribution/validation

### 19. Package/runtime support

Candidate direction:

Normal Python distribution with `aes` console entrypoint. The clean v0.2
semantic-core candidate stack is Git + Python + ruamel.yaml + Pydantic v2.
Pre-cutover probes in this same repository must also retain PyYAML while v0.1
Repository Context remains executable. Standard installation must work without uv
or a source checkout.

Review question:

Which Python versions and exact dependency pins become the first supported
compatibility contract after clean-install/round-trip probes?

### 20. Authentic Greenfield consumer and control

**Selection rule resolved 2026-09-25 (`24-pre-probe-decisions.md` §2, option A approved by Brian); the consumer is `BrianMills2718/whygame5` (named by Brian 2026-09-25). Control isolation rule: §3 step 3.**

Candidate direction:

Use a genuinely new project, not AES canonical, and compare one real change with
bounded projected context versus ordinary repository orientation.

Review question:

Which project is authentic but bounded enough for the first proof, and how do we
isolate the control from hidden conversational knowledge?

## Lineage/cutover

### 21. v0.2 acceptance and v0.1 supersession

**Partially resolved 2026-09-25 (D4 in `24-pre-probe-decisions.md`): cutover must explicitly supersede 0001 §3/§6, 0002 and 0009; the marking artifact/revision remains open.**

Candidate direction:

v0.1 remains historical lineage/evidence. v0.2 becomes current only through an
explicit acceptance/cutover change after this architecture review; implementation
does not silently redefine current architecture.

Review question:

What exact artifact/decision and Git revision marks that cutover, what v0.1
material remains live in the working tree, and what class of later semantic change
requires v0.3 instead of additive v0.2 capability maturity?

### 22. Human review surface

Candidate direction (added 2026-09-25):

`aes review` renders one self-contained HTML page under `.aes/generated/`
from target.yaml, generated current/gaps and the realized repository:
pending human decision first, then outcome, normative items, criterion to
evidence-requirement to verification-subject coverage with existence and
execution marks, component to file map, and orphan files under governed
roots. It is a derived projection in the sense of `02-semantic-model`
`human_navigation_and_review` and is never authority. It follows
Representation Router `references/planning-review.md` ("Reviewing a
structured proposal or target before implementation").

Evidence: `whygame5/.aes/generated/review.html` at whygame5 d989e8c, rendered
by `scripts/probe/render_review.py` (probe-0-review branch). This was built
after the first two v0.2 decisions (PR #35 accept/revise/reject, whygame5
outcome confirmation) were delivered to Brian as terminal prose, which lost
the coverage shape the decision depended on.

Review question:

Should `aes review` join the realization topology now, or only after a second
consumer use of the temporary renderer shows it reduced review cost? The
router's own rule says temporary first; the counter-argument is that AES's
delivery doc (`HUMAN_OBSERVABLE_DELIVERY.md` §7) already requires "the
smallest source-bound review surface" at every checkpoint, so the surface is
not optional.

Update 2026-10-04: the plan gate shaping (`proposals/aes-plan-gate/`, draft PR
#125) is the second real use. It extends the probe (execution marks, the
reference check with its method, a port-graph lens laid out by ELK, phone
outlines, no red-versus-green marks), renders the gate's own proposal and
whygame5's target with it, and proposes promoting it to `aes review` as
`ART-SRC-REVIEW`. The question is answered by that plan's acceptance or
rejection, not here.

## Explicitly deferred

Not prerequisites for the Greenfield MVP:

- arbitrary existing-repository retrofit;
- universal language/framework support;
- organization/portfolio-wide orchestration;
- generalized self-modifying policy;
- mandatory semantic event stream;
- automatic client-specific context injection;
- extracting AES capabilities into separate repositories without demonstrated
  ownership/release pressure.

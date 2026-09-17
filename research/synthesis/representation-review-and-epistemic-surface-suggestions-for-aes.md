# Representation Router salvage candidates for canonical AES

Status: research synthesis; non-normative candidate dispositions only.

Correction: this note addresses **what canonical AES may want to borrow from Representation Router**. It is intentionally separate from `code-map-v4-salvage-for-aes.md`, which addresses characterization/evidence lessons from Code Map V4.

Sources reviewed:

- canonical AES `docs/architecture/SYSTEM_BOUNDARY.md` on `main`;
- `research/synthesis/code-map-v4-salvage-for-aes.md` for the already-separated characterization/evidence seam;
- `brianmills-spec/representation-router` PR #24 / `chore/consolidation-v0` at head `ab7be7cf12880ec67e88837008eadb9ae6753f58`, especially:
  - `docs/design-model.md`;
  - `docs/INTEGRATION_POSITION.md`;
  - `references/planning-review.md`;
  - `docs/task-first-engineering-language.md`;
  - `schemas/view-spec.schema.json`; and
  - `schemas/surface-spec.schema.json`.

Purpose: identify Representation Router ideas that may strengthen canonical AES planning, review, context, and human/agent working surfaces **without copying Representation Router's product architecture, schemas, or workflow authority into AES**.

This document does **not** adopt Representation Router as an AES subsystem or contract authority. Per `AES-PLAN-001`, `AES-CAP-001`, and `AES-SYS-004`, any real adoption still requires an explicit AES gap, Company Planning derivation, incumbent/provider resolution through ACA, and an accepted implementation/verification topology.

---

## Executive recommendation

Representation Router contributes a useful capability that is mostly orthogonal to the Code Map salvage work:

> **Given authoritative semantic/workflow truth and a concrete human or agent concern, decide what concern-specific projection and representation should exist, how multiple views should coordinate, and where authority still lives.**

The strongest ideas for AES are:

1. **Truth, projection, representation, working surface, and implementation are different layers.**
2. **Start from the concern/job, not from the data type or renderer.**
3. **Planning and review should be source-bound projections over native authorities, not replacement authorities.**
4. **Work, Architecture, Assurance, and Review are useful coordinated lenses when the concern spans them, but only the necessary lenses should be shown.**
5. **Stable semantic identity should survive representation pivots; source-revision changes require explicit reset/remap behavior.**
6. **Visible UI actions do not create authority.** Read-only, local presentation/review state, and authoritative effects should remain distinct.
7. **Lead with the job; progressively disclose engineering structure and exact technical truth.**
8. **Unavailable or partial semantics should remain visibly unavailable/partial instead of being filled with plausible output.**
9. **The smallest useful working surface is better than a universal engineering dashboard.**
10. **Human/agent task performance is a different quality claim from schema validity, successful rendering, passing automation, or source correctness.**

The best initial AES disposition is therefore:

> **Treat Representation Router as an incumbent/provider candidate for concern-specific representation selection and source-bound working-surface composition; salvage its durable design principles now, and let ACA decide reuse/adapt/compose versus residual local implementation when an authentic AES gap requires the capability.**

---

# 1. Candidate incumbent disposition

A future incumbent-capability inventory entry could look roughly like:

| Incumbent | Candidate AES role | Initial disposition | Why |
| --- | --- | --- | --- |
| `brianmills-spec/representation-router` | concern-specific representation policy, coordinated source-bound planning/review surfaces, task-first progressive disclosure, representation QA | **candidate reuse/adapt through ACA; salvage design principles; do not copy authority or product shell** | mature separation of semantic truth from representation, source/revision-bound working-surface contracts, planning/review lens coordination, task-first UI language, and explicit action-authority boundaries |

This is more consistent with `AES-CAP-001` than immediately recreating a local AES representation framework.

If Company Planning eventually derives requirements such as:

```text
select a representation for a concern
compose several concern-specific views into one review surface
preserve semantic focus across compatible views
show provenance and exact source revision
make action authority explicit
```

ACA should first determine whether Representation Router already satisfies, can be configured for, or can be adapted to those capabilities.

---

# 2. Borrow the layer separation

Representation Router's most durable conceptual contribution is the separation:

```text
authoritative semantic / workflow truth
        ↓
concern / viewpoint
        ↓
semantic projection / view
        ↓
representation
        ↓
working surface
        ↓
product-owned implementation / workflow
```

AES already has a compatible authority model. A useful AES rendering of the same idea is:

```text
native authorities
  target / planning / source / code / tests / runtime / policy
        ↓
revision-bound characterization and evidence
        ↓
target / current / gap / plan materializations
        ↓
concern-specific projection
        ↓
representation / coordinated working surface
        ↓
human or agent understanding / judgment
        ↓
owning system performs any authoritative effect
```

The key distinction is:

> **Characterization answers what AES currently knows. Representation answers how a particular person or agent should understand or act on that knowledge for a particular concern.**

That suggests a clean seam between the existing Code Map salvage proposal and Representation Router salvage:

```text
Code Map-derived lessons
  evidence / characterization / freshness
                 |
                 v
AES current + gap materialization
                 |
                 v
Representation Router-derived lessons
  concern / projection / representation / working surface
                 |
                 v
human or agent review / navigation / decision support
```

AES should avoid collapsing these into one giant knowledge/visualization subsystem.

---

# 3. Start from the concern, not from the corpus

Representation Router explicitly rejects the idea that a stakeholder wants "the model." The stakeholder wants an answer to a concern.

That is directly useful for AES because AES will eventually contain or compose a great deal of target/current/gap/plan/evidence material. A naive implementation could expose all of it merely because it exists.

Instead, each generated context or review surface should begin with a question such as:

- What gap is preventing this outcome?
- What work can proceed next and what is blocked?
- Which architecture boundary does this planned change affect?
- What evidence currently supports closing this gap?
- What changed at this exact implemented revision?
- Which remaining uncertainty actually requires human judgment?
- Which policy blocked this transition and what recovery path exists?

Then derive only the semantic projection needed to answer that concern.

This reinforces `AES-CTX-001` and `AES-CTX-002`: progressive disclosure should not mean "dump everything and let the user filter it." It should mean **derive the smallest useful concern-specific context while keeping exact source truth reachable**.

---

# 4. Borrow temporary validated projections before durable schemas

Representation Router's planning/review guidance uses an important default:

> **A temporary validated projection is preferable for a one-off or early workflow; create a durable owned projection only after repeated use demonstrates that it reduces drift, repeated reconstruction, or review cost.**

This fits canonical AES particularly well during bootstrap.

AES should resist creating a universal durable schema for every possible planning/review/context view before the first authentic vertical exists.

A better progression is:

```text
native source contracts
        ↓
bounded adapter for one concern
        ↓
temporary validated projection
        ↓
working surface / context
        ↓
observe repeated use and friction
        ↓
only then decide whether a reusable projection contract has earned existence
```

This is consistent with:

- `AES-SYS-005` — no structure-first rewrite;
- `AES-CONTRACT-001` — typed boundaries stay with their natural authorities; and
- `AES-DOGFOOD-001/002` — authentic vertical evidence should precede generalization.

---

# 5. Borrow the planning/review lens model

Representation Router's planning/review work uses four useful linked lenses:

1. **Work** — outcomes, units, dependencies, state, blockers, next actions.
2. **Architecture** — boundaries, components, contracts, data/control flow, current versus proposed structure.
3. **Assurance** — requirements, risks, checks, evidence, gaps, unsupported obligations.
4. **Review** — implemented change, demonstrated behavior, drift, limitations, unsupported claims, and pending human judgment.

This maps naturally onto the AES lifecycle without making any of those lenses authoritative.

A future AES concern could move through:

```text
TARGET / GAP
   |
   v
WORK
what is planned / blocked / next?
   |
   v
ARCHITECTURE
what implementation boundary or contract is implicated?
   |
   v
ASSURANCE
what criterion, control, observation, and evidence establish conformance?
   |
   v
REVIEW
what changed, what remains uncertain, and what requires judgment?
```

The useful lesson is **not** that every AES screen must contain four tabs.

The useful lesson is:

> When one concern crosses multiple semantic structures, coordinated lenses are often better than either one overloaded universal view or several disconnected artifacts.

AES should include only the lenses needed by the concern.

---

# 6. Separate prospective planning from checkpoint review

Representation Router distinguishes two related modes that canonical AES should preserve:

### Prospective planning

Questions include:

- what outcome is intended?
- what work exists and what depends on what?
- what is blocked/ready?
- what architecture/contracts are implicated?
- what risks or assurance obligations remain uncovered?

### Checkpoint / completed-work review

Questions include:

- what was supposed to change?
- what actually changed at the reviewed revision?
- what evidence executed for that exact subject?
- where does implementation diverge from the target/plan/architecture?
- what remains partial or unsupported?
- what decision actually belongs to a person?

AES already distinguishes target/current/gap/plan/evidence. Representation Router suggests a human-facing way to preserve that distinction through the lifecycle.

A useful invariant is:

```text
recorded plan state
  != implementation state
  != executed evidence
  != rendered review state
  != human disposition
  != authoritative workflow state
```

That should remain true even when one surface coordinates all six.

---

# 7. Borrow source-bound working-surface discipline

Representation Router's `SurfaceSpec` is useful as a design source, even if AES never adopts the schema itself.

Its valuable ideas are:

- a working surface declares the **human job**;
- participating views have roles such as primary/complementary/supporting;
- sources have owners, exact revisions, and roles;
- semantic focus is coordinated across views;
- revision changes have explicit focus behavior;
- actions distinguish read-only, local, and authoritative effects;
- provenance and success criteria are surface-level concerns.

AES could borrow these as design requirements without copying `SurfaceSpec`.

For any consequential AES review surface, ask:

```text
what is the job?
which exact subjects/revisions are being shown?
which source owns each visible fact?
what identity coordinates the views?
what happens if the source revision changes?
which controls are merely navigation/local state?
which control, if any, invokes an owning authority?
what evidence must be retained?
what observable user/agent outcome defines success?
```

That checklist is likely more valuable to AES than the exact Representation Router JSON structure.

---

# 8. Preserve semantic identity across views

Representation Router treats a representation pivot as a lens change, not a subject-identity change.

For AES, this is important when one implementation subject appears in:

- a gap view;
- a work/dependency view;
- an architecture view;
- an assurance/evidence view;
- a review view;
- source-local context.

Selecting the implementation subject in one lens should not cause another lens to silently select a different object because its label looks similar.

A useful AES interaction rule is:

```text
same subject identity + same compatible source revision
        -> focus may survive a lens/representation pivot

source/corpus revision changed
        -> clear focus or require explicit remapping

selected subject absent in next lens
        -> retain identity and say "not represented here"
           rather than silently substituting another subject
```

This complements Code Map-style freshness/invalidation. Freshness decides whether knowledge about the subject is still valid; semantic-focus rules decide whether UI/agent context may safely carry the selected subject across a view change.

---

# 9. Borrow explicit semantic availability

Representation Router has a strong rule:

> If the semantic view required by the concern is unavailable, do not fabricate a plausible representation.

AES needs the same discipline at the context/review layer.

Examples:

```text
architecture relationship unavailable
    -> show architecture view unavailable
    -> state the required source/contract
    -> do not infer the relationship from naming conventions

verification did not execute
    -> show evidence unobserved/error
    -> do not render criterion as satisfied

plan-to-code binding absent
    -> show trace gap
    -> do not invent a link because files look relevant
```

Representation Router's `available / partial / unavailable` idea can remain a presentation-level distinction while AES characterization keeps richer states such as `PASS / FAIL / NONE / ERROR / STALE` underneath.

That separation may be useful:

```text
characterization epistemic state
        ↓
projection availability
        ↓
representation behavior
```

---

# 10. Borrow action-authority boundaries

Representation Router makes an unusually useful distinction among:

- **read-only action** — inspect/navigate without mutation;
- **surface-local action** — changes presentation or local review state only;
- **authoritative write** — changes an owning external system and therefore requires explicit destination/revision/authority/stale behavior/evidence.

AES already has stronger lifecycle/policy concepts around authority and governed execution. The useful Representation Router lesson is how to carry that truth all the way into a human-facing surface.

For example:

```text
"Show related evidence"
    -> read-only

"Add a local review note"
    -> surface-local

"Accept gap disposition"
    -> authoritative only if routed through the owning planning/workflow contract

"Retry blocked verification"
    -> authoritative execution only through the provider/policy path that owns it
```

A button label, rendered page, agent recommendation, or generated context must never imply the effect already occurred.

This directly reinforces `AES-SYS-002`, `AES-POL-001`, `AES-POL-003`, and the Company Planning / Enforced Planning split.

---

# 11. Borrow task-first progressive disclosure

Representation Router's task-first rule is strongly aligned with the AES wiki/context goal:

> **Lead with the job. Teach the technical language in context. Preserve the exact truth underneath.**

AES should consider a three-level context ladder:

### 1. Task language

Answer first:

- What changed?
- Why does it matter?
- What is blocked?
- What should I inspect?
- What proves the claim?
- What happens next?
- What decision is waiting on me?

### 2. Engineering structure

Then expose:

- target clauses;
- gap identity;
- architecture/contracts;
- work dependencies;
- capability/provider disposition;
- controls;
- implementation/verification subjects;
- evidence relationships.

### 3. Exact technical detail

Finally expose without changing subjects:

- stable IDs;
- exact source paths;
- revisions;
- schema fields;
- evidence receipts;
- commands/checks;
- code/configuration;
- formal terminology.

This is not simplification by hiding truth. It is **ordering the truth around the user's job**.

The same principle should apply to agent context packets: start with the engineering decision/action, then progressively expose structure and exact authority as needed.

---

# 12. Explain relationships, not only objects

Representation Router's task-first guidance observes that in engineering systems the relationship can carry more meaning than either endpoint.

AES is especially relationship-heavy:

```text
target clause -> gap
gap -> plan item
plan item -> capability requirement
capability requirement -> provider
requirement -> implementation subject
implementation subject -> verification subject
control -> recovery path
observation -> current characterization
review decision -> exact subject revision
```

A human/agent surface should make a load-bearing relation inspectable:

1. what two subjects it connects;
2. what the relationship means;
3. why it matters to the current concern;
4. what authority/evidence establishes it;
5. which revision it applies to;
6. what it does **not** imply; and
7. exact technical relationship details when useful.

This complements the Code Map salvage idea that some load-bearing relationships may also need evidence/freshness semantics.

---

# 13. Prefer coordinated complements over one universal view

Representation Router distinguishes alternative representations that are **substitutes** from views that answer different questions and are therefore **complements**.

AES should apply the same idea to its eventual wiki/review/context surfaces.

A dependency graph, traceability matrix, state/control view, diff, evidence table, and narrative summary are not necessarily competing presentations of one thing. They may be complementary because each makes a different operation perceptually cheap.

The useful design target is:

> **the smallest useful coordinated set of representations that answers the concern**

rather than:

> one canonical AES dashboard that displays every lifecycle concept at once.

This is particularly relevant for the first authentic vertical: let the actual concern determine whether one view or several coordinated views are needed.

---

# 14. Separate representation quality from truth/conformance quality

Representation Router carefully separates:

```text
source/model truth
test/check definition
executed evidence
rendered working surface
human comprehension/usefulness
authoritative acceptance/mutation
```

AES should preserve that distinction in evaluation.

For example:

- schema validation can establish that a generated view conforms to its contract;
- a screenshot/geometry check can establish that labels are not clipped;
- a successful test can establish the behavior it exercised;
- revision-bound evidence can establish an observation about the current implementation;
- none of those alone establish that a reviewer understood the situation correctly;
- a human disposition does not itself change authoritative state unless the owning workflow processes it.

For context/representation evaluation, prefer independent task outcomes such as:

- correct decision/action;
- correct identification of blocker or next step;
- successful trace from requirement to implementation/evidence;
- correct distinction between executed evidence and planned verification;
- time-to-answer;
- missed uncertainty or unsupported claim;
- successful movement from plain explanation to exact source.

This is a useful guard against AES treating generated artifact count or green UI tests as proof that context is effective.

---

# 15. Use success criteria at the representation layer

Representation Router carries observable `successCriteria` into view/surface design so downstream implementation does not optimize only for rendering mechanics.

AES planning already derives success criteria for system behavior. A related but separate layer may be useful for **context/review success**.

For example:

```text
system criterion:
  policy blocks execution without accepted plan linkage

working-surface criterion:
  reviewer can identify the block reason, owning policy,
  exact affected subject, and sanctioned recovery action
  without opening policy source first
```

These should not be confused, but both matter.

The first authentic AES vertical could therefore carry:

1. engineering success criteria;
2. verification/evidence criteria; and
3. representation/context task-success criteria.

---

# 16. Human attention should be scarce and explicit

Representation Router's review guidance says to queue a human decision only when judgment, authority, preference, or an irreversible boundary genuinely belongs to the person.

That is highly applicable to AES.

A review item should say:

- what is being decided;
- which exact subject/revision is being judged;
- why the decision is needed now;
- which evidence supports it;
- which limitation/uncertainty remains; and
- what each disposition actually causes.

Do not ask a person to confirm facts that automation/source authority can establish. Conversely, do not let automation manufacture a human judgment merely because every machine check passed.

This can reduce "human-in-the-loop" theater while preserving genuine authority boundaries.

---

# 17. What AES should not borrow wholesale from Representation Router

The following should remain Representation Router-specific unless an authentic AES gap independently justifies them.

## 17.1 Exact `ViewSpec`, `CollectionSpec`, or `SurfaceSpec` schemas as universal AES contracts

Their concepts are useful. AES should not copy the schemas merely because they exist.

If AES needs representation policy, ACA may resolve Representation Router itself as a provider. If a provider-neutral boundary is genuinely needed, derive it from the authentic consumer seam and respect `AES-CONTRACT-001`.

## 17.2 Representation catalogs as AES ontology

Graphs, matrices, timelines, interface patterns, renderers, and heuristics are Representation Router policy knowledge. They should not become AES lifecycle ontology.

## 17.3 Representation Router's proving products

Engineering Home, studios, runners, review workbenches, Release + Operate proofs, and the Self Map are evidence/proving surfaces, not a template for AES product topology.

## 17.4 Renderer/visualization implementation choices

AES should not own React Flow, D3, Graphviz, LikeC4, or similar renderer preferences because Representation Router experimented with them.

## 17.5 Heuristic weights or numeric thresholds as universal laws

Representation Router itself treats them as hypotheses. AES should not import them as policy authority.

## 17.6 One giant lifecycle UI

Representation Router's strongest current lesson is consolidation and separation of reusable representation policy from proving application scope. AES should learn from that history rather than reproduce the same scope accretion.

---

# 18. Candidate thin slice for the first authentic AES vertical

When Company Planning selects the first authentic external-consumer vertical, test Representation Router ideas with one real review concern.

A useful concern might be:

> **Given the accepted target and completed implementation revision, what remains before this gap can be considered closed, and which remaining judgment belongs to a human?**

### Inputs

Use native authorities for:

1. accepted target clause / success criterion;
2. current or prior characterization;
3. gap identity/state;
4. accepted plan/work item;
5. implementation subject at exact revision;
6. verification subject/check definition;
7. fresh executed evidence;
8. policy/control state where relevant.

### Concern-specific projections

Derive only the lenses needed, for example:

```text
Work
  planned outcome / work / blocker / next action

Architecture
  affected boundary / contract / implementation subject

Assurance
  criterion / check / executed evidence / remaining gap

Review
  intended change / actual change / limitations / pending judgment
```

### Interaction invariants

- stable subject IDs coordinate compatible views;
- source revision is always reachable;
- an unavailable relation/lens stays unavailable rather than inferred;
- changing source revision clears/remaps semantic focus explicitly;
- evidence and non-claims/limitations are adjacent;
- local review state is not authoritative workflow state;
- any authoritative effect routes through its owning AES provider/contract.

### Negative-control cases

Deliberately test:

```text
remove executed evidence
    -> assurance must not show verified/conformant

change implementation revision without fresh evidence
    -> prior review/evidence must not silently carry over

remove plan-to-implementation relation
    -> trace must show unavailable/gap rather than infer linkage

policy/check errors
    -> surface must show error/unobserved rather than green

selected subject absent in another lens
    -> retain identity + "not represented", not silent substitution
```

### Representation success criteria

Measure whether a reviewer or agent can:

1. state what was intended;
2. identify what actually changed;
3. trace the material criterion to implementation and executed evidence;
4. distinguish missing/stale/unexecuted evidence from failure;
5. identify the remaining gap or unsupported claim;
6. identify the exact human decision, if one remains;
7. reach exact source/revision when needed; and
8. avoid mistaking the rendered surface for authority.

This would provide authentic evidence for which Representation Router concepts AES actually needs.

---

# 19. Suggested capability-resolution questions

Before AES implements representation/context behavior locally, Company Planning + ACA should answer:

1. Does the concern require representation selection or only text/navigation synthesis?
2. Does an existing provider such as Representation Router already satisfy the semantic capability?
3. If Representation Router is reused, what is the smallest adapter from AES-native projections into the provider?
4. Which semantic eligibility rules remain owned by AES/native source systems?
5. Does the provider need read-only data, or does the surface expose any consequential action?
6. Which stable identities coordinate views?
7. Which exact source/revision changes invalidate focus or require refresh?
8. Are multiple views genuine complements or unnecessary duplication?
9. Which human/agent task outcome proves the representation helped?
10. What friction/cost does the representation layer introduce?
11. Which lessons are provider-neutral enough to promote into AES methodology, if any?
12. What remains product-specific and should stay outside canonical architecture?

---

# 20. Condensed recommendation

If only six Representation Router ideas survive into AES thinking, retain these:

### A. Concern before representation

Do not show "the AES model." Start with the human/agent question and derive the smallest semantic projection that answers it.

### B. Projection is not authority

Target/current/gap/plan/review surfaces remain derived views over native authorities.

### C. Coordinated lenses can preserve one subject across different questions

Work, Architecture, Assurance, and Review are a useful pattern when one concern crosses those structures, provided stable identity and provenance connect them.

### D. Visible action does not create authority

Read-only, surface-local, and authoritative effects remain distinct all the way into the UI/agent interaction.

### E. Lead with the job, preserve exact truth underneath

Progressive disclosure should improve engineering agency without inventing a simplified parallel truth model.

### F. Reuse the capability before copying the mechanism

When AES truly needs representation routing or coordinated working-surface composition, resolve Representation Router through ACA before building a local equivalent.

---

## Disposition summary

| Representation Router idea | Suggested AES disposition |
| --- | --- |
| truth → concern → projection → representation → surface separation | **salvage strongly** |
| concern/viewpoint-first design | **salvage strongly** |
| temporary validated projections before durable schemas | **salvage strongly** |
| Work / Architecture / Assurance / Review coordinated lenses | **salvage as a review pattern; use only when needed** |
| prospective planning vs checkpoint review distinction | **salvage** |
| source/revision-bound working surface | **salvage strongly** |
| stable semantic focus across representation pivots | **salvage** |
| explicit unavailable/partial semantic views | **salvage strongly** |
| read-only / surface-local / authoritative action boundary | **salvage strongly; map to native AES authority** |
| task-first progressive disclosure | **salvage strongly** |
| relationship inspection + non-claims | **salvage** |
| complementary representation sets | **salvage concept; prove with real concerns** |
| view/surface-level success criteria | **salvage** |
| Representation Router itself as representation provider | **candidate reuse/adapt via ACA when a gap requires it** |
| exact RR schemas as AES universal contracts | **do not copy by default** |
| RR catalogs/heuristics as AES ontology | **do not port** |
| RR proving applications as AES product architecture | **do not port** |
| renderer/library choices | **do not port** |
| one universal engineering dashboard | **reject as a default target** |

This is a research synthesis, not an implementation plan. The next legitimate transition is an authentic AES gap that requires representation/context capability, followed by Company Planning derivation and ACA resolution of Representation Router and other relevant incumbents before any local residual implementation.
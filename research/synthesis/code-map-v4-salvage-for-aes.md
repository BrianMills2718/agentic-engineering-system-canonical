# Code Map V4 salvage candidates for canonical AES

Status: research synthesis; non-normative candidate dispositions only.

Source reviewed: `BrianMills2718/code_map_v4` at revision `0c8f6f075de4db52cb753b42153d33d62bdc6210`.

Purpose: identify mechanisms and lessons from Code Map V4 that may strengthen the canonical Agentic Engineering System (AES), especially the `current -> gap -> plan -> execution -> evidence -> fresh characterization -> gap reconciliation` loop, without importing Code Map's old product architecture or creating a competing authority.

This document does **not** adopt these mechanisms. Any implementation must still be derived from explicit AES gaps through Company Planning, capability resolution through ACA, and an accepted implementation/verification topology.

## Executive recommendation

Do **not** merge Code Map V4 into AES as a subsystem.

Treat it as an incumbent evidence source containing several mature ideas worth salvaging into a much smaller AES characterization/evidence capability:

1. **Revision-bound evidence envelopes** — observations know which repository revision, producer, source anchors, dependencies, and verification results they came from.
2. **Source anchors and dependency-aware freshness** — current-state claims can become stale because the exact supporting subject changed, rather than because any file in the repository changed.
3. **Typed provenance-bearing relationships** — relationships between requirements, implementation subjects, verification subjects, and other entities can carry evidence and invalidation semantics instead of being bare links.
4. **Explicit epistemic states** — failed extraction, missing observation, stale evidence, and broken verification remain visible states rather than silently collapsing into success.
5. **Negative-control discipline** — important controls should demonstrate that they fail on deliberately invalid conditions, with scope/coverage evidence where applicable.
6. **Structured facts are substrate, not comprehension** — mechanically correct fact dumps do not by themselves create useful context; derived wiki/context surfaces should synthesize what matters while preserving authority boundaries.
7. **Independent evaluation signals** — an evaluation should not define ground truth using the same mechanism it is evaluating.

The strongest fit is not Code Map's wiki product. It is a small **AES characterization kernel** underneath current-state materialization and gap recomputation.

---

## Why this fits the canonical AES architecture

The canonical AES system boundary already establishes several requirements that Code Map explored concretely:

- `AES-PLAN-003`: plan completion is not conformance; fresh evidence and revision-bound characterization close gaps.
- `AES-POL-002`: ignorance cannot render green; meaningful states include pass, fail, none/unobserved, error, and stale.
- `AES-POL-004`: important controls prove they can fail with a negative control or equivalent counterfactual plus coverage where applicable.
- `AES-CTX-001`: the wiki is a derived progressive-disclosure surface, not authority.
- `AES-CTX-002`: implementation subjects should eventually receive source-local generated context derived from normative clauses, current characterization, gaps, and plans.
- `AES-EVID-001`: observations/evidence are retained as history while current-state and gap views are materialized from the latest valid revision-bound evidence.

Code Map V4 implemented narrower versions of several of these ideas for repository comprehension. AES can reuse the lessons while giving them a broader lifecycle meaning.

The desired relationship is therefore:

```text
Code Map V4
  evidence / characterization mechanisms
                 |
                 | salvage selected ideas
                 v
AES characterization/evidence capability
                 |
                 +--> current projection
                 +--> gap derivation
                 +--> source-local context
                 +--> conformance re-check after execution
```

not:

```text
AES -> embed Code Map -> make Code Map wiki authoritative
```

---

## Candidate disposition for Code Map V4

Suggested future entry for the incumbent capability inventory:

| Incumbent | Candidate AES role | Initial disposition | Why |
| --- | --- | --- | --- |
| `BrianMills2718/code_map_v4` | revision-bound repository characterization, source anchoring, freshness/invalidation, evidence-graph and evaluation lessons | **salvage mechanisms; do not reuse product architecture** | mature experiments in evidence provenance, change-aware characterization, explicit verification state, negative controls, and derived comprehension; Python/wiki-specific product topology is not an AES fit |

This would preserve the AES rule that incumbent work is explicitly dispositioned rather than silently rediscovered or copied.

---

# 1. Salvage: revision-bound evidence envelopes

## Code Map lesson

Code Map modeled persisted artifacts with a common envelope containing ideas such as:

- stable artifact ID,
- repository ID,
- snapshot/revision ID,
- producer and producer version,
- source-anchor IDs,
- observation IDs,
- payload hash,
- dependency IDs.

Facts then carried verification status, confidence, freshness, verification-result IDs, and invalidation triggers.

The important idea is not the exact Pydantic schema. It is that an observation cannot masquerade as timeless truth: its provenance and validity context travel with it.

## AES adaptation

AES should eventually define a provider-neutral observation/evidence contract with the smallest fields needed to answer:

```text
what was observed?
about which subject?
at which exact revision/environment?
by which observer/control?
from which supporting source/evidence?
what dependencies make this observation invalid?
what happened when it was checked?
```

A conceptual shape might be:

```yaml
observation_id: ...
subject_id: ...
observed_at_revision: ...
observer:
  capability: ...
  version: ...
source_refs: [...]
dependency_refs: [...]
status: observed | not_observed | error | stale
payload: ...
```

This is deliberately illustrative, **not** a proposed universal AES schema. Per `AES-CONTRACT-001`, native typed boundaries should remain with their natural contract authority, and Data Contracts may supply reusable provider-neutral contracts where that is actually useful.

## Why it matters

Without revision/provenance binding, AES cannot reliably distinguish:

- current implementation truth,
- a prior observation that used to be true,
- an observation that was never attempted,
- an observation attempt that failed,
- an assertion copied into prose with no current evidence.

That distinction is foundational to gap recomputation.

---

# 2. Salvage: source anchors and precise invalidation

## Code Map lesson

Code Map attached source facts to concrete source spans and computed span fingerprints. Change detection could therefore ask whether the supporting subject actually changed rather than invalidating all evidence merely because the containing file changed.

It also propagated invalidation through explicit dependencies. For example, evidence that a test covers a symbol depends on both the source subject and the test responsible for the coverage relationship.

## AES adaptation

When AES has implementation subjects, characterization should support an invalidation path roughly like:

```text
observation at revision R
        |
        v
characterization of subject S
        |
  source/dependency change
        |
        v
is the supporting anchor/dependency still valid?
        |
      yes ------------------> current
        |
       no
        v
      stale
        |
        v
re-observe / re-characterize
```

The exact anchoring mechanism can vary by subject type:

- source span / AST or CST identity for code,
- file/content hash for configs,
- schema/version identity for data contracts,
- command/environment fingerprint for runtime probes,
- exact referenced clause/version for normative dependencies.

The general principle is more important than Python-specific implementation:

> **Invalidate the smallest characterization unit whose supporting evidence changed, while failing safely toward stale rather than false-current.**

## AES value

This would make `AES-EVID-001` operational and support efficient post-execution reconciliation:

```text
new revision
    -> identify affected characterization dependencies
    -> mark affected projections stale
    -> re-observe only what requires new evidence
    -> materialize fresh current
    -> recompute affected gaps
```

That is preferable to either extreme:

- trusting old current-state prose forever, or
- recomputing every characterization artifact after every change.

---

# 3. Salvage: provenance-bearing relationship edges

## Code Map lesson

Code Map relationships were first-class artifacts rather than anonymous graph edges. An edge could carry:

- relationship kind,
- source and target IDs,
- supporting observation IDs,
- producer,
- freshness/verification status,
- invalidation triggers.

That model proved useful because relationships themselves can become stale or wrong.

## AES adaptation

The canonical repo already reserves `.agentic/relationships.yaml` for future relationships such as:

```text
requirement -> implementation subject -> verification subject
```

When Company Planning derives the first target topology, consider making those relationships evidence-bearing rather than merely structural.

For example:

```text
AES-PLAN-003
    --realized_by-->
implementation subject
    --verified_by-->
verification subject
```

could eventually be accompanied by metadata like:

```text
origin: accepted planning output
observed_at_revision: <sha>
evidence_ids: [...]
freshness: current | stale | ...
invalidation_subjects: [...]
```

This need not all live in `.agentic/relationships.yaml`; native authority boundaries should decide storage. The important design point is that AES should be able to distinguish an asserted relationship from an evidenced-current relationship.

## Why it matters

Gap reconciliation ultimately asks questions about relationships:

- Does this implementation subject realize this criterion?
- Does this verification subject still exercise the behavior it claims to cover?
- Does this policy apply to this boundary?
- Does this capability provider still satisfy this requirement?

Those edges have lifecycle semantics and deserve evidence/freshness treatment where they are load-bearing.

---

# 4. Salvage: explicit epistemic state and failure-as-evidence

## Code Map lesson

Code Map generally treated extractor/tool failures as data rather than allowing them to disappear. Its artifact model distinguished current, stale, superseded, broken, and unknown states, and verification distinguished passed, failed, skipped, stale, broken, and unknown.

Some of the exact categories are Code Map-specific, but the underlying rule is directly aligned with AES:

> **Failure to observe is itself an observation about the observation process.**

## AES adaptation

Characterization/control interfaces should avoid binary APIs such as:

```text
true | false
```

where `false`, missing data, exceptions, stale results, and “not applicable” can become indistinguishable.

Prefer an explicit state discipline conceptually like:

```text
PASS
FAIL
NONE / UNOBSERVED
ERROR
STALE
```

with richer typed details underneath.

This is already an AES architectural rule through `AES-POL-002`; Code Map provides implementation evidence for why the rule matters.

## Required behavior

A derived current projection should never turn:

```text
observer crashed
```

into:

```text
requirement satisfied
```

Likewise, a wiki/context generator should surface uncertainty or omit a conclusion rather than quietly converting unknown evidence into a positive statement.

---

# 5. Salvage: negative-control discipline, not Code Map's exact verifier

## Code Map lesson

Code Map's behavioral verifier evolved through adversarial failures:

1. a passing generated test was not enough;
2. requiring the test to mention/invoke the target was not enough;
3. a single destructive mutant was not enough;
4. type/shape-only tests could survive as false confidence;
5. a larger mutant battery improved the counterfactual check;
6. important semantic residuals still remained.

The mature lesson is **not** “use these seven Python return mutants everywhere.”

The mature lesson is:

> A control is weakly evidenced if we have only seen it pass. We gain substantially more confidence by deliberately constructing conditions under which it should fail and confirming that it does.

## AES adaptation

For important AES controls, verification evidence should include where applicable:

```text
known-good input/state     -> expected ALLOW/PASS
known-bad input/state      -> expected BLOCK/FAIL
observer/control error     -> expected ERROR, never PASS
stale evidence             -> expected STALE/RECHECK behavior
scope boundary             -> evidence that the control applies where claimed
recovery path              -> evidence that a blocked case can reach an allowed state correctly
```

This fits `AES-POL-003` and `AES-POL-004` particularly well.

### Example

For a policy that blocks unplanned implementation:

```text
valid planned change       -> ALLOW
same change without plan   -> BLOCK
BLOCK + sanctioned recovery -> plan created / approved -> ALLOW
policy evaluator crashes   -> ERROR, not ALLOW
```

This is a stronger proveout than a suite containing only examples the policy accepts.

## Do not inherit the overclaim

Code Map sometimes uses the word “verified” for behavioral prose after an LLM-written test passes on real code and fails against a mutant battery. That establishes useful behavioral sensitivity but does **not** prove semantic equivalence between arbitrary natural-language prose and the generated test.

AES should keep the proof meaning explicit:

```text
"counterfactual check passed"
```

is evidence with a known scope; it should not silently become:

```text
"this natural-language claim is proven true in every respect"
```

---

# 6. Salvage: structured facts are substrate, not comprehension

## Code Map lesson

Code Map spent multiple versions building increasingly rigorous structural repository maps. The maps contained signatures, tests, docs, imports, provenance, confidence, and freshness — but developers still did not receive an explanation of what a subject actually did, how it worked, or what could go wrong.

The eventual lesson was that **format and fact inventory are not synthesis**.

A page can be perfectly grounded and still be a poor context surface.

## AES adaptation

AES should preserve a three-layer separation:

```text
1. native authorities + raw evidence
                 |
                 v
2. structured materialized projections
   target / current / gap / plan / relationships
                 |
                 v
3. derived comprehension/navigation
   wiki / source-local context / agent briefing
```

Layer 3 should answer questions like:

- What matters at this subject?
- What target clauses constrain it?
- What is currently true?
- What is not yet true?
- What plan owns the remaining change?
- What verification will decide whether the gap is actually closed?
- What are the important risks or non-obvious interactions?

It should not merely dump every fact/evidence ID available.

This reinforces `AES-CTX-001`: the wiki is a progressive-disclosure synthesis layer, not an alternative authority database.

## Practical warning

Do not let “we generated all links, clauses, evidence IDs, and statuses” become a proxy for successful context delivery.

A useful success test is closer to:

> Does this generated context materially improve an agent's ability to make the correct engineering decision at this subject without hiding uncertainty or authority provenance?

---

# 7. Salvage: independent evaluation signals

## Code Map lesson

Code Map's first retrieval evaluation defined ground truth using essentially the same import-graph mechanism that the evaluated “map” arm received. The result looked excellent but was largely tautological. The project later replaced it with a ground-truth proxy independent from the import expansion mechanism.

The valuable lesson is methodological:

> **An evaluation is weak when the mechanism being evaluated participates in constructing the answer key.**

## AES adaptation

AES should prefer independent evidence for capability evaluation whenever possible.

Examples:

- do not evaluate a planner solely by checking whether its own generated plan says all requirements were handled;
- do not evaluate a policy registry solely from the policy registry's self-reported coverage;
- do not evaluate a characterization system solely against another projection built from the same extractor;
- do not evaluate capability resolution solely by whether the selected provider's own metadata says it fits;
- do not treat plan completion as gap closure — already required by `AES-PLAN-003`.

The canonical AES requirement for an **authentic external consumer vertical** is well aligned with this lesson. External behavior/outcomes provide a substantially more independent signal than self-description alone.

---

# 8. Proposed synthesis: an AES characterization kernel

The highest-value Code Map salvage could be expressed as a deliberately small capability tentatively called the **characterization kernel**.

This is a conceptual capability, not a requested implementation root.

## Responsibility

Given an implementation/project subject and exact revision, the kernel supports:

1. recording observations and receipts;
2. binding observations to exact revision/environment and source/dependency anchors;
3. materializing a current characterization from the latest valid evidence;
4. representing unknown/error/stale explicitly;
5. invalidating characterization when its supporting dependencies change;
6. exposing relationships/provenance needed for gap derivation;
7. supporting selective re-characterization after execution.

It does **not** own:

- normative target authority;
- planning;
- plan execution governance;
- policy authority;
- capability-provider authority;
- wiki authority;
- arbitrary natural-language truth verification.

## Conceptual flow

```text
                      normative target
                           |
                           |
repo @ exact revision --->+---> CHARACTERIZATION
          |                       |
          |                       +-- observations
          |                       +-- source/dependency anchors
          |                       +-- verification receipts
          |                       +-- relationship evidence
          |                       +-- epistemic/freshness state
          |                                  |
          |                                  v
          |                            CURRENT projection
          |                                  |
          |                                  v
          +-----------------------------> GAP comparison
```

After governed implementation:

```text
new exact revision
      |
      v
find affected evidence dependencies
      |
      v
mark affected characterization stale
      |
      v
selective fresh observation
      |
      v
new CURRENT projection
      |
      v
recompute affected GAPS
```

## Storage alignment with the canonical repository

The existing canonical roots already suggest a clean separation:

- `evidence/` — retained observations and run receipts; authoritative for what was observed, not interpretation;
- `generated/` — rebuildable derived current/gap/context projections; never independent authority;
- native implementation/test/config sources — authority for their own contents;
- `wiki/` — derived navigation/synthesis;
- `.agentic/relationships.yaml` or a future native relationship authority — topology/linkage where accepted.

This is a better fit than Code Map's old model where most of the product revolved around a generated repository wiki.

---

# 9. What should *not* be borrowed from Code Map

The following should remain historical unless a future AES gap independently justifies them.

## 9.1 The 13-extractor matrix as a goal

Code Map accumulated many Python-specific extractors: AST, LibCST, Griffe, Jedi, coverage, pytest, Ruff, Pyright, imports, git history, markdown parsing, and others.

AES should not equate extractor count with characterization maturity.

Choose observers only because a target/current/gap question requires their evidence.

## 9.2 Python-specific canonical symbol identity as a universal model

Code Map solved real Python `src/` layout and tool-naming problems. Those rules should stay with a Python characterization provider if needed. They should not become the AES universal subject identity system.

## 9.3 Whole-repository generated wiki as the product

The canonical AES wiki already has a different role: progressive disclosure across target/current/gap/plan/capability/evidence authority. Recreating Code Map's symbol wiki would pull AES backward toward an implementation-centric fact inventory.

## 9.4 Large structural claim grammar

Code Map rendered deterministic claims such as “symbol X is defined in file Y” or “module A imports B.” AES can materialize structured facts/relationships without inventing a global natural-language claim template language.

## 9.5 Per-claim LLM-written verification as a default

Generating a bespoke test for every synthesized sentence is expensive and has a semantic-faithfulness residual. AES should prefer native verification subjects, plan-derived success criteria, policy controls, and direct runtime/static evidence. Model-written probes can remain one evidence technique where justified.

## 9.6 Unsandboxed execution of generated checks

Code Map's proof runner executes model-generated pytest in a normal subprocess. That is an explicit security limitation, not a mechanism to salvage.

Any AES capability that executes generated/untrusted code should derive an isolation boundary appropriate to the threat model before it is treated as generally reusable.

## 9.7 Code Map's retrieval benchmark as an AES product metric

BM25/import-graph retrieval may be useful in some future context provider, but it is not intrinsically part of the AES lifecycle architecture.

AES should evaluate context/planning/policy/capability mechanisms against authentic engineering outcomes rather than inherit Code Map's retrieval framing.

---

# 10. Adoption criteria

A Code Map mechanism should be adopted into canonical AES only if all of the following are true:

1. **Gap-backed need** — an explicit AES target/current gap requires the capability.
2. **Authority-safe** — the mechanism does not create a second mutable authority for facts already owned elsewhere.
3. **Provider-dispositioned** — ACA/incumbent review determines whether Code Map, another incumbent, extension, composition, or local residual is appropriate.
4. **Proof meaning is explicit** — evidence says exactly what was observed/proven and no more.
5. **Epistemic failure is preserved** — unobserved/error/stale states cannot become success.
6. **Invalidation semantics exist** — current projections can determine when their evidence no longer applies.
7. **Rebuildability is clear** — derived projections are disposable/recomputable; observation receipts retain their proper lifecycle.
8. **Independent verification exists where important** — evaluation is not circular with the mechanism being evaluated.
9. **Authentic vertical evidence** — the mechanism is demonstrated in a real consumer lifecycle, not only self-description.
10. **Cost/friction is observed** — runtime, cognitive overhead, maintenance burden, and false-stale/false-current behavior feed AES learning rather than disappearing.

---

# 11. Candidate first use in the canonical AES vertical

When Company Planning selects the first authentic external-consumer vertical, use that vertical to test whether a minimal characterization kernel is actually required.

A useful thin slice would be one concern with:

1. an accepted target clause / success criterion;
2. one implementation subject;
3. one verification subject;
4. one observation receipt bound to an exact revision;
5. one materialized current characterization;
6. one derived gap;
7. governed implementation that changes the subject;
8. precise invalidation of the prior characterization;
9. fresh observation after execution;
10. recomputed gap state;
11. a wiki/source-local projection rebuilt from the new current state.

The slice should deliberately include at least one epistemic or policy failure path, for example:

```text
verification command errors
    -> ERROR / unresolved current
    -> recovery action
    -> successful fresh observation
    -> new current
```

or:

```text
policy blocks implementation lacking accepted plan linkage
    -> BLOCK + recovery path
    -> linkage corrected
    -> ALLOW
```

This would simultaneously test the best Code Map salvage ideas and the canonical AES lifecycle without committing to a broad implementation prematurely.

---

# 12. Questions Company Planning should answer before implementation

If this salvage becomes relevant to a concrete gap, Company Planning should resolve at least:

1. What is the smallest subject identity required for the vertical?
2. Which observations are authoritative receipts versus derived interpretation?
3. Which exact revision/environment dimensions must be captured?
4. Which dependencies can invalidate each characterization?
5. Is source-span precision worth its complexity for this subject type?
6. Which relationships are merely planned topology and which require observed-current evidence?
7. What are the required epistemic states at each interface?
8. Which controls need negative-control evidence and what counterfactual is meaningful?
9. What belongs in `evidence/` versus `generated/` versus a native owner?
10. What output should the wiki/source-local context synthesize for the agent, rather than merely list?
11. What independent outcome determines whether the characterization/context capability helped?
12. What is the recovery behavior when characterization fails or becomes stale?

---

# 13. Condensed recommendation

If only three ideas survive from Code Map V4, retain these:

### A. Revision-bound evidence

No current-state assertion without provenance sufficient to say **what was observed, where, when/revision, and by what**.

### B. Dependency-aware freshness

No materialized current projection without a way to know **when the evidence that supports it no longer applies**.

### C. Facts are not comprehension

Do not confuse a complete machine-readable characterization with an effective agent context surface. **Characterize structurally; synthesize progressively; keep native authority visible.**

Those three ideas reinforce the canonical AES architecture without importing Code Map's historical product assumptions.

---

## Disposition summary

| Code Map idea | Suggested AES disposition |
| --- | --- |
| evidence envelope / snapshot binding | **salvage** |
| source anchors / span fingerprints | **salvage concept; apply selectively** |
| dependency/invalidation triggers | **salvage** |
| explicit freshness / broken / unknown states | **salvage and align with AES epistemic states** |
| evidence-bearing relation graph | **salvage concept for load-bearing relationships** |
| negative-control evolution | **salvage methodological lesson** |
| structural-facts-vs-synthesis lesson | **salvage strongly** |
| independent evaluation lesson | **salvage strongly** |
| Python 13-extractor matrix | **do not port wholesale** |
| Code Map universal symbol/wiki product | **do not port** |
| large natural-language structural claim grammar | **generally do not port** |
| LLM-written test => “verified prose” framing | **do not inherit as a truth claim** |
| unsandboxed generated-test execution | **reject** |
| BM25/import retrieval as AES core | **defer unless a real context gap requires it** |

This is intentionally a salvage inventory, not an implementation plan. The next legitimate transition is an evidence-backed disposition from an authentic AES gap, followed by Company Planning and ACA resolution.
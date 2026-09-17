# AC16 / AC17 lessons and candidate mechanisms for canonical AES

Status: research synthesis; non-normative suggestions only.

Date: 2026-09-16

Purpose: identify evidence, method rules, and candidate mechanisms from the AC16 / AC17 Autocoder research lineage that may strengthen the canonical Agentic Engineering System (AES), without treating AC16 or AC17 as AES architecture, importing their product structure, or transferring authority.

## Source relationship and scope

AES is **not based on AC16 or AC17**. AC16 and AC17 are separate Autocoder research systems with a narrower experimental center: deriving executable acceptance from requests, generating implementations, repairing failures, and measuring where generated specifications and implementations disagree with independent evidence.

Canonical AES has a broader and different system boundary:

```text
orient -> target -> current -> gap -> plan -> capability composition
       -> governed execution -> evidence -> characterization -> gap reconciliation
       -> learning / policy or capability improvement
```

The useful relationship is therefore:

```text
AC16 / AC17
  measured failures, method rules, candidate mechanisms
                     |
                     | evidence-backed salvage
                     v
AES planning / policy / execution / evidence design
```

not:

```text
AES -> adopt AC17 pipeline or Autocoder architecture wholesale
```

AC17 states this distinction explicitly: it is a proving ground and can supply empirical evidence and candidate mechanisms to AES, not architecture. A mechanism should move toward AES only after surviving its own validation and proving useful to real AES consumers.

Sources inspected for this synthesis:

- `BrianMills2718/ac16@c3d2369a9ed3f6937547bef5dcd252b02ebc69b5`
- `BrianMills2718/ac17@d03b7754788373102d0b09da96757e85acb1a838`
- AC16 `README.md`
- AC16 `docs/ASSESSMENT_2026-09-04.md`
- AC17 `README.md`
- AC17 `docs/lineage/ac16/README.md`
- AC17 `docs/EXPERIMENTAL_METHOD.md`
- AC17 `plan/decisions/2026-09-09-v1-automatic-blueprint.md`

This document is a candidate-mechanism inventory. It does not make implementation decisions for AES.

---

# Executive recommendation

The strongest AC16 / AC17 contribution to AES is not a generation pipeline. It is an **epistemic and execution discipline** for systems where agents generate plans, specifications, tests, implementations, reviews, and repairs.

The central lessons are:

1. **Treat generated artifacts as claims, not truth.** A generated specification, test suite, plan, review, or characterization can be internally consistent and still wrong about its source authority.
2. **Separate authoring from checking where shared misreading is a real risk.** Same-source / same-model agreement is not independent evidence.
3. **Preserve authority boundaries between generation, review, repair, and adjudication.** A downstream healer must not receive hidden adjudication answers or be allowed to rewrite upstream truth to make itself pass.
4. **Unresolved semantics must stop downstream execution.** Ambiguity or disputed meaning is not a build hint; it is an authority gap.
5. **Changes to upstream semantic artifacts invalidate dependent evidence.** Revising a requirement, contract, blueprint, or plan requires fresh checks downstream.
6. **Structural coverage is not behavioral leverage.** A test citing a requirement is weaker than a counterfactual showing that the test fails when the required behavior is removed or inverted.
7. **Use the cheapest discriminating falsifier before expensive end-to-end runs.** Isolate one mechanism, freeze upstream inputs, preregister kill conditions, inspect traces, and replicate only when the pilot actually separates hypotheses.
8. **Keep hidden / independent adjudication firewalled from repair.** Evidence used to measure correctness must not become training data inside the counted attempt.
9. **Classify disagreements before repairing them.** A failing check may mean wrong implementation, wrong test, wrong requirement/contract, reviewer error, environment failure, or unresolved ambiguity.
10. **Operationalize method rules as gates.** A written lesson that is not encoded in routing, validation, or policy will be violated again.
11. **Freeze claims to their exact evidence scope.** `passed` means the declared validation profile passed, not universal correctness.
12. **Carry negative results forward.** Failed experiments, instrument defects, and rejected causal explanations should actively constrain future work rather than becoming inert history.

These ideas align naturally with existing AES clauses around authority separation, gap-backed planning, plan completion versus conformance, explicit epistemic state, negative controls, append-only evidence, and authentic external dogfood.

---

# 1. Generated artifacts are claims, not truth

AC16's central failure was that a model could derive an acceptance blueprint and then generate code that perfectly satisfied it while both shared the same misunderstanding of the request. AC17 made the corrective principle explicit:

> the blueprint is treated as a claim, not the truth.

For AES, this principle is broader than executable blueprints.

Candidate AES rule:

> **Any agent-generated artifact that interprets an upstream authority is a derived claim until independently checked at the authority boundary it purports to represent.**

Examples include:

- a plan claiming to cover a gap;
- a generated contract claiming to express a requirement;
- a test claiming to exercise a success criterion;
- a current-state characterization claiming to describe implementation behavior;
- a capability match claiming a provider satisfies a semantic need;
- a review claiming a requirement is satisfied;
- a wiki/context summary claiming to describe the current system.

The artifact may be useful, executable, typed, and internally consistent while still misrepresenting its source.

## AES consequence

The lifecycle should distinguish:

```text
source authority
      |
      v
agent-derived artifact
      |
      v
independent / differently-authorized check
      |
      v
accepted operational use
```

This reinforces `AES-SYS-002` rather than introducing a new authority layer.

---

# 2. Distinguish forms of independence explicitly

AC16 showed that "reviewed" is not enough if the reviewer reproduces the same interpretation error. AC17 improved this with blind reading, separate request review, hidden adjudication, independent implementation, and protected assembly, but its own evidence also shows that independence has multiple axes.

AES should avoid the unqualified word `independent` in load-bearing evidence.

Useful axes include:

- **context independence** — did the checker see the artifact being checked?
- **implementation independence** — was the checker created in a different execution/session path?
- **model independence** — was a different model/provider used?
- **source independence** — did the checker derive from the original authority rather than the same intermediate artifact?
- **authority independence** — is the checker allowed to decide this question, or merely advise?
- **adjudicator independence** — is the scoring/evaluation mechanism firewalled from generation and repair?
- **environment independence** — was behavior checked in a distinct runtime or consumer boundary?

## Why this matters

Consider:

```text
request
  -> generated requirements
  -> generated tests
  -> generated implementation
```

A second agent checking the tests only against the generated requirements is context-independent from the implementation but not source-independent from the requirements extraction.

Likewise, a different model reading the same flawed intermediate specification may be model-independent but not authority-independent.

## Candidate AES practice

Evidence records and planning language should say which independence property is actually present rather than treating `independent review` as a single binary property.

---

# 3. Same-author agreement is weak evidence when correlated error is plausible

AC16 measured a particularly important failure mode: four implementations fully satisfied their generated blueprints while scoring only 53–88% on an independent suite. The blueprint and implementation were generated from the same source and shared misreadings.

The general AES lesson is:

> **Agreement between artifacts produced by the same interpretive path may demonstrate internal consistency without adding much new information about source fidelity.**

This applies well beyond code generation.

Examples:

- planner writes success criteria, then planner self-reviews plan coverage;
- characterization model writes current-state summary, then grades its own summary;
- policy generator writes rule and tests rule using the same interpretation;
- capability resolver proposes a provider and certifies fit from the same provider metadata;
- documentation generator writes a system description and evaluates retrieval against labels derived from that same description.

## AES adaptation

When correlated error is plausible, prefer one of:

- a fresh derivation from the original source;
- a structurally different checker;
- a counterfactual / mutation signal;
- authentic runtime behavior;
- a different authority source;
- disagreement-driven escalation.

Do not add process merely to create the appearance of two opinions.

---

# 4. Provenance is necessary but not sufficient for fidelity

AC17 records source quotations and clause references, but its current V1 decision explicitly notes that source quotes prove presence/provenance, not semantic correctness or completeness.

That distinction is highly relevant to AES.

A generated artifact may correctly cite the exact target clause and still:

- omit a required consequence;
- invert precedence;
- narrow or widen scope;
- invent an unstated behavior;
- bind the wrong subject;
- ignore interaction with another clause.

Candidate AES rule:

> **Provenance answers "where did this claim come from?" Fidelity answers "did the claim preserve the source meaning?" Do not use one as a proxy for the other.**

## Practical implication

Source-linked plans, policies, context, and characterization are valuable, but important semantic transformations need a separate fidelity mechanism where the cost of mistranslation is meaningful.

---

# 5. Disagreement must be classified before repair

AC17's V1 decision identifies a key missing route: when a blind reader disagrees with a blueprint test, the system must classify the disagreement before any repair:

- wrong test;
- wrong clause/contract;
- reader implementation bug;
- unresolved ambiguity.

A disagreement alone does not prove which side is wrong.

This is a strong general AES pattern.

## Candidate AES disagreement taxonomy

For any load-bearing failed check, route through a classification such as:

```text
implementation defect
verification defect
plan defect
requirement / target defect
characterization defect
provider mismatch
policy defect
observer / tool failure
stale evidence
unresolved semantic ambiguity
```

Only then select a repair authority.

## Why this matters

Without classification, agentic systems tend to repair the nearest editable artifact. That can produce a green pipeline by weakening the check, changing the plan, or rewriting derived truth around the implementation.

AES should prefer:

```text
failure
  -> classify authority/domain
  -> route to permitted repair stage
  -> invalidate affected downstream evidence
  -> rerun required checks
```

rather than:

```text
failure
  -> let general healer edit whatever makes it green
```

---

# 6. Repair authority should be stage-scoped and non-transitive

AC16 learned that hidden adjudication must never reach the healer. AC17 further separates blueprint revision from code repair: the code healer cannot edit an accepted blueprint, and semantic blueprint changes belong to a distinct revision stage.

This suggests a broadly useful AES invariant:

> **A repair mechanism may modify only the authority domain it owns; passing evidence from a higher-authority adjudicator does not grant permission to rewrite upstream meaning.**

Examples:

- implementation repair may edit implementation but not accepted requirements;
- test repair may edit an invalid test only after the test has been classified as wrong by an authorized route;
- plan repair may revise the plan but not silently redefine the target gap;
- policy recovery may change sanctioned configuration/state but not disable the protecting policy by default;
- characterization repair may rerun or replace an observer but not fabricate current state;
- capability resolution may select a different provider but not weaken the semantic capability requirement.

This is a concrete execution form of AES authority separation.

---

# 7. Semantic changes should invalidate dependent evidence

AC17's accepted V1 direction says that changing a blueprint revision invalidates dependent checks and requires a fresh blind read.

AES should generalize this as a dependency rule:

> **When an upstream semantic artifact changes, downstream evidence that depends on its old meaning becomes stale until revalidated.**

Examples:

```text
target criterion changed
  -> gap derivation stale
  -> plan coverage stale
  -> relevant verification mapping stale

accepted plan contract changed
  -> execution-context projection stale
  -> affected work claims / checkpoints re-evaluated

interface contract changed
  -> implementation conformance stale
  -> dependent tests / integrations rechecked

policy semantics changed
  -> policy evidence / negative controls stale

characterization observer changed materially
  -> current projection requires fresh observation
```

The exact invalidation graph should be derived from the first AES vertical; the rule itself is general.

---

# 8. Unresolved semantics should stop downstream work

One of AC17's most important current implementation gaps is that reader disputes are still forwarded to the builder even though the accepted V1 direction says unresolved disputes must prevent building.

AES should adopt the intended rule, not the current AC17 defect:

> **If a downstream action depends on unresolved meaning, do not convert that ambiguity into implementation discretion unless the governing authority explicitly allows such discretion.**

This aligns with `AES-POL-002`: ignorance cannot render green.

## Candidate routing behavior

```text
semantic disagreement
       |
       v
can existing authority determine the answer?
       | yes
       v
bounded correction + fresh checks

       | no
       v
UNRESOLVED / escalation
       |
       X
no dependent execution
```

This prevents automation pressure from inventing business decisions merely to preserve flow.

---

# 9. Hidden adjudication should be firewalled from the counted attempt

AC16 discovered answer-key leakage into oracle checks and established the invariant that adjudication must never reach the healer. AC17 retains the same boundary: generation, review, and healing do not see hidden scoring inputs or results, and hidden failures are not fed back into the qualifying run.

This is a very strong AES evaluation principle.

## Generalized rule

Where AES evaluates a capability, policy, planning mechanism, context mechanism, or generated artifact using held-out or independent evidence:

- freeze the candidate before adjudication;
- run the independent evidence once according to the preregistered contract;
- preserve the result;
- do not feed held-out failures back into that counted attempt;
- diagnose afterward and make a new treatment/version explicit.

Otherwise the evaluation quietly becomes an optimization loop over its own hidden benchmark.

## AES uses

This matters for:

- capability-provider evaluation;
- planning evaluations;
- policy effectiveness tests;
- source-local context utility experiments;
- generated verification topology;
- automated migration/refactor systems;
- any benchmark used to justify promotion into canonical AES.

---

# 10. Claimed coverage is not behavioral coverage

AC16 measured a blueprint that claimed full coverage while none of its 42 cases exercised one rule. AC17 therefore layers stronger evidence:

1. clause/test linkage;
2. joint interaction coverage where applicable;
3. mutation / counterfactual evidence that the test can detect a representative semantic defect;
4. prospective validation.

The general AES lesson:

> **A declared mapping from criterion to check establishes traceability, not necessarily behavioral sensitivity.**

For important criteria, distinguish at least:

```text
mapped
executed
behaviorally discriminating
prospectively validated
```

## Example

A plan may say:

```text
criterion C -> test T
```

That proves a declared relationship.

If `T` still passes after the required behavior is deliberately removed, the mapping has little conformance value.

This aligns directly with `AES-POL-004` and can inform target-verification topology beyond policy controls.

---

# 11. Mutation is a leverage test, not universal proof

AC17 is careful about this distinction. An interaction marker is structural evidence; mutation adds evidence that the witness can detect a class of behavioral loss. Even then, representative mutation does not prove every possible defect is covered.

AES should retain that proof discipline.

Candidate language:

```text
counterfactual killed
```

means:

```text
this verification subject is sensitive to this modeled defect class
```

not:

```text
this criterion is universally proven
```

This matters because agentic systems are prone to converting a useful diagnostic into an inflated assurance label.

---

# 12. Interactions and precedence deserve first-class attention when they matter

AC17's interaction work found a common failure mode: individual clauses can each be tested while their combined behavior, precedence, suppression, or short-circuit remains wrong.

The useful AES lesson is not AC17's specific interaction manifest. It is:

> **Where two accepted constraints can co-fire or one suppresses another, verification topology should represent the interaction rather than assuming single-clause coverage composes automatically.**

Potential AES examples:

- policy precedence and exemptions;
- plan constraints interacting with capability selection;
- recovery paths interacting with destructive boundaries;
- data-contract compatibility plus provider-specific constraints;
- concurrent work ownership / lane rules;
- deployment gating plus emergency override;
- source-local context where multiple authorities constrain the same subject.

AC17's semantic dispositions are a useful conceptual vocabulary:

- co-fire;
- precedence;
- exclusive;
- independent;
- unresolved.

AES need not adopt those exact labels globally, but the classification can be useful when deriving verification topology for interaction-heavy boundaries.

---

# 13. Do not scale a mechanism that requires bespoke source strings

AC17's interaction-mutation work hit a valuable scaling falsifier: if every additional interaction requires a hand-written exact source anchor or custom mutator, enrich the semantic representation rather than extending an unscalable catalog.

This is broadly useful for AES capability design.

Candidate rule:

> **When a supposedly general mechanism scales only by accumulating one-off cases, stop and identify the missing semantic representation before expanding the catalog.**

Examples:

- policy checks requiring one bespoke parser per repository;
- capability matching requiring hard-coded provider names;
- plan verification requiring path-specific grep expressions;
- characterization requiring hand-authored source anchors per subject;
- recovery routing requiring custom logic per control;
- context generation requiring one template per project artifact.

This is a good trigger for Company Planning / capability disposition: the local exceptions may be evidence that a reusable semantic capability is missing.

---

# 14. Prefer standard executable artifacts over custom acceptance languages

AC16's custom input→exact-dictionary case language became a product limitation: value constraints, nested shapes, optional fields, state, exceptions, time, IO, and richer interactions were awkward or inexpressible. AC17 deliberately returned to ordinary pytest, Pydantic, and standard Python artifacts.

The AES lesson aligns strongly with `AES-CONTRACT-001`:

> **Do not invent a universal AES verification or contract language where native typed/executable artifacts already express the needed semantics.**

Use AES-level metadata for lifecycle linkage, authority, provenance, and state; keep semantic expression in the natural native mechanism where possible.

Examples:

- pytest for Python behavior;
- native schema systems for data contracts;
- real policy engines for policy semantics;
- deployment probes for deployed behavior;
- standard type systems for callable consistency.

AES should compose native evidence, not replace it with a lowest-common-denominator DSL.

---

# 15. Trace review should precede causal claims about agents

AC17's experimental method is especially strong here: scores classify outcomes, but traces are required before asserting why a model failed or succeeded.

The method asks whether evidence is about the mechanism under test or merely stochastic attention/allocation inside a larger workflow.

This should influence AES research and capability promotion.

## Candidate AES experiment rule

Before concluding that a mechanism improves agent behavior because a score changed, inspect whether the treatment actually changed the relevant behavior.

Useful trace questions include:

- what did the agent read before its first substantive action?
- which constraints were in context at the point of decision?
- which tools/checks were actually invoked?
- where did the first wrong decision appear?
- did the treatment alter that decision path?
- did a successful run simply make a different local choice?
- was the failure caused by environment/harness friction rather than the proposed mechanism?

This is particularly relevant to evaluating source-local context, planning packets, policy prompts, capability routing, and decomposition.

---

# 16. Use the cheapest discriminating falsifier before end-to-end replication

AC17's current experimental sequence is highly reusable as an AES research discipline:

1. name the causal claim;
2. run the cheapest falsifier;
3. isolate one mechanism;
4. choose the smallest discriminating intervention;
5. preregister prediction and kill condition;
6. pilot before replication;
7. inspect traces before causal interpretation;
8. freeze evidence before changing the mechanism.

This is a better default than repeatedly running expensive end-to-end agent workflows whenever a subsystem question appears.

## AES examples

Before building a new context subsystem:

- inspect whether the agent actually lacked the information;
- replay the same task with a small targeted packet;
- compare traces;
- only then justify broader machinery.

Before introducing multi-agent decomposition:

- freeze the plan/input;
- test whether a smaller structured-attention treatment fixes the observed miss;
- only then attribute the issue to decomposition need.

Before changing capability resolution:

- isolate the provider-selection error from planning and execution variance.

This supports cheaper and more interpretable AES evolution.

---

# 17. Pre-register stop rules and budgets so failure can teach you

AC16's assessment identified a methodological danger: treating every failed run as another fixable instrument defect can make a premise effectively unfalsifiable unless the project states when a sufficiently sound failure becomes evidence against the mechanism.

AES research should make the transition explicit:

```text
before instrument validity
  -> failures may diagnose the instrument

after preregistered validity conditions hold
  -> failure counts as evidence about the mechanism
```

Candidate practice:

- define required harness validity before the experiment;
- define retry policy for infrastructure failures;
- define repair / revision budget;
- define stop condition;
- define what result kills or weakens the causal claim;
- honor the result before redesigning the treatment.

This prevents endless "one more mechanism fix" loops.

---

# 18. Separate infrastructure failure from semantic failure

AC16 lost many runs to harness crashes, timeouts, missing artifacts, and turn caps. Those outcomes were not model-answer failures, but they initially contaminated the evidence.

AES should classify execution outcomes so infrastructure problems do not masquerade as semantic evidence.

At minimum distinguish:

```text
candidate / semantic FAIL
control / policy BLOCK
UNRESOLVED semantics
observer ERROR
execution infrastructure ERROR
budget EXHAUSTED
STALE evidence
PASS
```

This aligns with `AES-POL-002` but applies across the broader lifecycle.

A broken toolchain should not become a failed capability claim; equally, it must not disappear into green.

---

# 19. Method rules should become executable gates when they are important

AC16 recorded a blunt but valuable lesson: a method rule that lived only in prose was repeatedly violated until it became a checked test/gate.

AES should assume the same.

If a research or lifecycle rule is important enough that violating it invalidates evidence, encode it in one of:

- schema validation;
- policy control;
- stage routing;
- immutable artifact permissions;
- preflight checks;
- CI / runtime gates;
- evidence validator.

Examples:

```text
"hidden adjudication never reaches repair"
```

should be enforced by custody, not etiquette.

```text
"no execution while blocking finding is open"
```

should be a routing gate, not a wiki sentence.

```text
"changed target invalidates plan conformance"
```

should mark dependent projections stale automatically where feasible.

---

# 20. Keep open findings active, not archival

AC16 learned that chronological run logs can preserve lessons without changing future behavior. It added an open-findings table with dispositions and a gate preventing measurement while blocking findings remained open.

This maps well to `AES-LEARN-001`.

Candidate AES pattern:

```text
observation / failure
      |
      v
finding
      |
      +--> resolved by code
      +--> resolved by policy
      +--> resolved by capability change
      +--> accepted limitation
      +--> research question
      +--> superseded / refuted
      +--> blocking unresolved
```

A finding should not count as "learned" merely because it was written down. Learning is activated only when its disposition changes a future decision surface.

---

# 21. Evidence records should preserve non-claims

AC16 and AC17 are unusually disciplined about saying what a run does **not** establish. AC17's current README explicitly limits successful evidence to the declared validation profile and refuses to claim general reliability from bounded pilots.

AES should preserve this style in evidence contracts.

A useful result record should include:

```text
what was demonstrated
what exact artifact/revision was tested
which validation profile ran
what evidence was independent and in what sense
what remained untested
known residuals
whether this evidence supports promotion, diagnosis, or only local development
```

This guards against evidence inflation as results are summarized upward into wiki/context/planning layers.

---

# 22. Protected ownership boundaries are a useful execution mechanism candidate

AC17's complete-loop work uses independent unit builds, explicit component ownership, assembly-owned files, and protection against assembly rewriting passed units. Repair routing depends on whether a failure is local to a unit or occurs at the seam/assembly level.

AES should not adopt AC17's component system globally, but the underlying execution pattern is valuable for Enforced Planning / multi-lane work:

> **Where work is intentionally decomposed, make ownership and permitted mutation boundaries executable, and route failures to the smallest authority allowed to repair them.**

Potential AES uses:

- concurrent work lanes;
- delegated implementation tasks;
- generated migrations;
- multi-repository plan execution;
- integration/assembly stages;
- protected accepted artifacts.

A passed upstream work product should not be silently rewritten by a downstream assembler unless the plan explicitly grants that authority.

---

# 23. Draft inspectability should remain separate from acceptance

AC17's V1 decision explicitly says to keep draft inspectability separate from acceptance.

This is important for AES because agentic systems often need to preserve failed or partial artifacts for diagnosis.

Candidate rule:

```text
artifact exists and is inspectable
```

must not imply:

```text
artifact is accepted / authoritative / current
```

This supports resumability and debugging without creating false green states.

Useful states may include:

```text
draft
structurally valid
semantically disputed
accepted
superseded
stale
rejected
```

The exact state model should remain domain-specific unless a shared need emerges.

---

# 24. Automatic correction must not become test weakening

AC17's accepted direction permits correcting a demonstrably wrong test where the unchanged request determines the answer, but explicitly rejects weakening a test to fit candidate code.

AES should preserve the general invariant:

> **A repair that changes the verifier must establish why the verifier was wrong from an authority independent of the failing candidate.**

Otherwise self-healing systems can achieve convergence by lowering the bar.

This applies to:

- generated tests;
- policy checks;
- plan success criteria;
- schema validators;
- migration acceptance;
- capability fit criteria;
- deployment health checks.

If the only evidence that a check is wrong is "the candidate fails it," repair is not authorized.

---

# 25. Authentic external behavior is stronger than self-consistency

AC16 / AC17 repeatedly demonstrate that internally consistent artifacts can still be wrong. This reinforces the canonical AES requirement that the first vertical cross a real external consumer boundary.

For AES, self-dogfood is valuable but insufficient when the system is certifying its own planning, context, policy, or capability outputs.

The strongest promotion evidence should eventually include a consumer/outcome outside the mechanism's own artifact loop.

This is one reason `AES-DOGFOOD-001` and `AES-DOGFOOD-002` are important protection against circular success criteria.

---

# Candidate mapping into canonical AES

The following is a conceptual mapping, not an implementation proposal.

| AC16 / AC17 lesson | Possible AES home | Why |
| --- | --- | --- |
| generated artifact is a claim | planning, characterization, context, policy | prevents derived artifacts becoming authority by convenience |
| explicit independence axes | evidence model / research method | makes assurance claims precise |
| same-author correlated error | planning + verification topology | warns against self-review as independent evidence |
| provenance != fidelity | context / planning / characterization | source links do not prove semantic preservation |
| dispute classification | policy/routing / Enforced Planning | sends failures to correct repair authority |
| stage-scoped repair authority | execution governance | prevents green-by-rewriting-authority |
| semantic-change invalidation | evidence/current/gap materialization | keeps downstream state revision-correct |
| unresolved semantics stop execution | policy + planning | preserves authority gaps instead of inventing decisions |
| adjudication firewall | evals / capability promotion | prevents benchmark leakage |
| traceability != behavioral coverage | verification topology | distinguishes mapping from leverage |
| mutation / counterfactual evidence | policy + critical verification | proves checks can detect modeled failures |
| interaction / precedence classification | complex control seams | captures non-compositional behavior |
| scaling falsifier | capability architecture | detects missing semantic abstraction |
| standard executable artifacts | native contract/verification owners | avoids universal AES DSL |
| trace-first causal diagnosis | experiments/evals | avoids false mechanism conclusions |
| cheapest falsifier + preregistration | research method | reduces expensive uninterpretable agent runs |
| explicit experiment budgets | research / planning | makes mechanisms falsifiable |
| infrastructure vs semantic outcome | execution evidence | prevents contaminated measurement |
| method rules become gates | policy / CI / routing | lessons affect future behavior |
| active findings/dispositions | learning loop | turns records into future decisions |
| scoped non-claims | evidence / wiki | prevents evidence inflation |
| protected ownership boundaries | Enforced Planning candidate | makes decomposition/custody executable |
| draft != accepted | artifact lifecycle | preserves diagnosis without false authority |
| verifier repair requires external authority | repair governance | prevents bar-lowering convergence |

---

# What should not be borrowed wholesale

## 1. AC17's pipeline stages as universal AES lifecycle stages

`derive -> read -> build -> assemble -> verify -> repair -> hidden score` is appropriate to AC17's research target. AES should not force policy, deployment, documentation, data, or capability work into that topology.

Borrow the authority and evidence rules, not the exact pipeline.

## 2. Executable blueprints as the universal planning representation

AC17's EARS + Pydantic + pytest bundle is a strong experiment for generated software acceptance. AES planning spans many domains where the correct native artifacts differ.

Company Planning should choose verification topology appropriate to the concern.

## 3. Hidden suites everywhere

Held-out adjudication is useful when evaluating a generative mechanism, but production engineering often needs transparent deterministic controls. Use hidden evidence for independent evaluation where justified, not as a universal operational pattern.

## 4. Multi-agent decomposition by default

AC17 explicitly treats decomposition as a causal treatment, not a reward for any miss. AES should do the same. Use the smallest treatment that addresses the measured failure.

## 5. AC17's interaction machinery as a global semantic ontology

The interaction work is valuable evidence about coupled constraints. Its manifests, markers, effect IR, and mutant families should remain AC17-specific unless an AES gap independently demands similar machinery.

## 6. Model disagreement as truth

Two agents disagreeing identifies uncertainty. It does not establish which one is correct. Disagreement is a routing signal, not an oracle.

## 7. Same-model / different-session as sufficient independence

A new session can reduce context coupling but does not automatically remove model priors or source ambiguity. State exactly what independence is gained.

## 8. Autocoder reliability claims beyond the measured scope

AC16 and AC17 deliberately limit their own claims. AES should preserve those limits and avoid citing bounded pilot evidence as proof of broad agentic-engineering reliability.

---

# Suggested first use in the canonical AES vertical

Do **not** build an AC17-style validation framework before the vertical exists.

Instead, ask Company Planning to use the first authentic external-consumer vertical to test a few narrow AC16 / AC17-derived hypotheses.

A useful thin slice could require:

1. one accepted target criterion;
2. one generated/derived planning artifact that claims to realize it;
3. one implementation subject;
4. one verification subject;
5. an explicit statement of what authority each artifact has;
6. at least one independent check whose independence axis is named;
7. one negative control or counterfactual for a load-bearing check;
8. one intentionally induced disagreement/failure routed to the correct repair domain;
9. evidence that an upstream semantic revision marks dependent downstream evidence stale;
10. one authentic external observation used for final gap reconciliation.

A particularly valuable proveout would deliberately exercise:

```text
verification disagreement
       |
       v
classify disagreement
       |
       +--> implementation defect -> scoped implementation repair
       |
       +--> verifier defect -> verifier repair justified from target authority
       |
       +--> unresolved target meaning -> STOP / escalation
```

The point is not to recreate AC17. The point is to test whether AES can preserve authority and evidence correctly when an agentic workflow encounters conflicting generated artifacts.

---

# Questions Company Planning should consider

Before implementing any of these candidate mechanisms, answer:

1. Which AES artifacts are native authority, which are derived claims, and which are merely advisory?
2. Where is correlated same-agent / same-source error plausible enough to require a differently-derived check?
3. When AES says `independent`, which axis of independence is actually required?
4. Which semantic disagreements must block execution versus permit implementation discretion?
5. Which stage owns repair for each class of failure?
6. What evidence authorizes changing a verifier rather than the implementation?
7. Which upstream changes invalidate which downstream evidence?
8. What adjudication/eval information must be firewalled from generation or repair?
9. Which criterion-to-check mappings need counterfactual evidence that the check can actually fail?
10. Which interactions/precedence relationships are load-bearing enough to require joint verification?
11. What is the cheapest falsifier for the proposed mechanism before an expensive agent run?
12. What exact outcome would falsify or retire the proposed mechanism?
13. What execution/harness states must be separated from semantic candidate failure?
14. Which method rules are important enough to encode as gates rather than prose?
15. How do open findings become active inputs to future policy/planning/capability decisions?
16. What external consumer evidence closes the gap independently of the system's own self-description?

---

# Condensed recommendation

If only six AC16 / AC17 ideas enter the AES design conversation, retain these:

## A. Derived artifact != authority

A generated plan, test, contract, review, or characterization is a claim about its source until the relevant authority boundary has been checked.

## B. Agreement != independence

Two artifacts can agree because they share the same misunderstanding. Name the independence property that the second check actually adds.

## C. Repair cannot rewrite its judge

Separate repair domains. Hidden adjudication never enters the healer. Changing a verifier requires independent authority that the verifier is wrong.

## D. Unresolved semantics stop dependent execution

Automation must not invent authority merely to continue the pipeline.

## E. Traceability != behavioral leverage

A criterion mapped to a test is not enough. Important checks should demonstrate that they fail under meaningful counterfactual defects where practical.

## F. Diagnose cheaply before scaling

Freeze upstream artifacts, isolate one mechanism, preregister the kill condition, inspect traces, and run the smallest experiment that could change the decision.

Together these ideas fit canonical AES particularly well because AES already separates target, current, gap, plan, execution, evidence, characterization, and learning. AC16 / AC17 provide hard-won evidence for how those boundaries can fail when agent-generated artifacts are allowed to certify one another.

---

# Disposition summary

| AC16 / AC17 idea | Suggested AES disposition |
| --- | --- |
| generated artifact as claim | **salvage strongly** |
| explicit independence axes | **salvage strongly** |
| correlated same-author error lesson | **salvage strongly** |
| provenance vs semantic fidelity distinction | **salvage strongly** |
| disagreement classification before repair | **salvage strongly** |
| stage-scoped repair authority | **salvage strongly** |
| semantic revision invalidates downstream evidence | **salvage strongly** |
| unresolved semantics block dependent execution | **salvage strongly** |
| adjudication firewall / no hidden feedback | **salvage for evaluation and promotion** |
| traceability vs behavioral coverage | **salvage strongly** |
| mutation / negative-control leverage | **salvage method; apply selectively** |
| interaction co-fire / precedence discipline | **salvage concept where coupled constraints matter** |
| scaling falsifier before bespoke catalogs | **salvage as capability-design heuristic** |
| standard executable artifacts over custom DSL | **salvage and align with AES-CONTRACT-001** |
| trace-first causal diagnosis | **salvage strongly for AES research/evals** |
| cheapest falsifier / isolate one mechanism | **salvage strongly** |
| preregister stop rules and budgets | **salvage strongly** |
| infrastructure vs semantic failure distinction | **salvage strongly** |
| method rules must become gates | **salvage strongly** |
| open findings with active dispositions | **salvage and align with AES-LEARN-001** |
| explicit non-claims / bounded proof language | **salvage strongly** |
| component ownership / protected assembly | **candidate mechanism; only if execution topology needs it** |
| AC17 pipeline architecture | **do not port wholesale** |
| executable blueprint as universal AES representation | **do not universalize** |
| hidden suite as universal control pattern | **use only where evaluation requires it** |
| decomposition by default | **reject; require measured need** |
| AC17 interaction IR as universal ontology | **do not port without an AES gap** |

This synthesis should be read as evidence-backed design input to Company Planning and future AES capability disposition, not as a request to make AC17 part of the canonical runtime.
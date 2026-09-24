# Planning-derived source and realized-source characterization for AES

Status: **research synthesis; non-normative candidate architecture**

Date: 2026-09-24

Purpose: consolidate the emerging AES design in which accepted planning determines the intended repository/source topology, selected portions of native source remain mechanically generated from structured normative authority, realized native source is characterized back into a structured projection, and AES compares target versus realized state to derive current characterization and gaps.

This synthesis does **not** amend accepted AES architecture, migrate normative authority, or authorize implementation. It is an input to a future Company Planning pass and dogfood plan.

## 1. Core hypothesis

AES should treat repository/source structure as an intentional realization of accepted engineering intent rather than an accidental byproduct of coding.

The intended loop is:

```text
accepted product/system intent
        ↓
requirements + success/disproof criteria
        ↓
capabilities + failure-mode mitigation structure
        ↓
components + dependencies
        ↓
planned repository/source topology
        ↓
generated native source skeleton / generated governed regions
        ↓
native implementation
        ↓
realized-source characterization
        ↓
current characterization
        ↓
target ↔ current comparison
        ↓
gaps
        ↓
next planning
```

For a greenfield repository, planning should declare the initial target topology directly. Retrofitting arbitrary existing repositories is a separate concern and is not required to validate this model.

## 2. Structured normative authority should contain success criteria

Success criteria are part of normative authority, not merely verification metadata.

A requirement states what should be true. Its success and disproof criteria specify what satisfaction and falsification mean. The acceptable proof kind may also be normative when the kind of evidence is material to acceptance.

Illustrative shape:

```yaml
requirement:
  id: REQ-MANIFEST-001
  statement: >
    A malformed authoritative manifest must fail closed.

  success_criteria:
    - id: SC-MANIFEST-001
      statement: >
        Malformed authoritative input produces ERROR and never invokes
        legacy fallback.
      acceptable_evidence:
        - deterministic_integration_test
        - authentic_runtime_observation

  disproof:
    - id: DP-MANIFEST-001
      statement: >
        Any malformed authoritative manifest that silently falls back
        disproves conformance.
```

The criterion text and requirement text remain authored once in canonical structured authority.

## 3. Planning should determine repository topology

Company Planning / AES planning should derive not only requirements and slices but the durable repository realization expected to satisfy them.

The target topology should normally include exact durable paths when those paths are knowable:

```yaml
component:
  id: repository_context

  implementation_subjects:
    - path: src/agentic_engineering_system/repository_context/resolver.py
      purpose: >
        Resolve bounded repository navigation and authority from explicit evidence.
      realizes:
        - REQ-CTX-001
        - REQ-CTX-004

  verification_subjects:
    - path: tests/repository_context/test_resolver.py
      verifies:
        - SC-CTX-001
        - SC-CTX-004
```

A durable tracked artifact should have a recoverable semantic reason for existence.

Candidate invariant:

> Every durable governed repository artifact is either declared by exact path in accepted topology or is produced by an explicit accepted generation/tooling rule.

Ephemeral build/runtime artifacts such as caches, bytecode, temporary coverage state, or scratch outputs are outside the governed durable topology.

## 4. Strong opinionation is a feature

The model should prefer enforceable defaults over discretionary guidance such as "often declare files".

Candidate controls include:

- new durable code file with no accepted topology entry or generation rule → block;
- new durable test/eval with no success criterion or verification obligation → block;
- planned path removed or renamed without an accepted topology change → block;
- success criterion with no verification disposition → unresolved/gap, never implicitly green;
- implementation file with no component/normative purpose → orphan artifact finding;
- generated projection stale relative to its authority revision → stale/error, never current.

The purpose is to make drift difficult rather than merely document good practice.

## 5. Permanent generated regions in native source

A key candidate design is that some source information remains generated permanently from normative/planning authority rather than being generated once and then manually maintained.

Likely generated material includes, subject to language/provider constraints:

- file/module purpose headers;
- public symbol skeletons where planning freezes them;
- public strong type signatures where the signature is part of accepted design;
- normative/source-local docstring sections;
- requirement and criterion applicability;
- verification obligations and source provenance;
- generated-region fingerprints.

Executable bodies remain native-language implementation.

Conceptually:

```python
# GENERATED GOVERNED CONTEXT — DO NOT EDIT MANUALLY.

class RepositoryContextResolver:
    """
    Resolve bounded repository authority and navigation from explicit evidence.

    NORMATIVE
    REQ-CTX-001:
    <verbatim authoritative requirement text>

    REQ-CTX-004:
    <verbatim authoritative requirement text>

    SUCCESS CRITERIA
    SC-CTX-001:
    <verbatim authoritative success-criterion text>

    SC-CTX-004:
    <verbatim authoritative success-criterion text>

    DISPROOF
    DP-CTX-001:
    <verbatim authoritative disproof text>

    Authority: <canonical record + exact revision/digest>
    """

    def resolve(...) -> RepositoryContextArtifact:
        # implementation-owned body
        ...
```

The exact generated-region mechanism is unresolved and should be dogfooded before standardization.

## 6. Source-local context must contain verbatim text, not only references

A critical requirement is that an agent working at a governed source subject must receive the **actual applicable normative text** and the **actual success/disproof criterion text**.

IDs and links are necessary for provenance, graph joins, and exact authority lookup, but are not sufficient as the primary working context.

The system should not rely on an agent to notice an ID such as `REQ-17`, dereference it, read the owning record, identify the relevant clause, and carry it back correctly.

Candidate source-local rule:

> Generated source-local context contains the full verbatim applicable normative statements and success/disproof criteria, alongside stable IDs and exact provenance.

Inheritance can reduce needless repetition in storage and generation logic, but the effective working context presented to the agent must be self-contained enough to act correctly.

Where a full component context applies to many private symbols, a file/component generated region may carry the shared full text once while narrower or exceptional symbol obligations are rendered at the symbol. This is a projection optimization, not permission to omit governing text from the effective agent context.

## 7. Native code remains executable authority

AES should not create a general YAML programming language.

Native languages retain executable semantics and their mature ecosystems:

- Python / TypeScript / Rust / SQL / other source;
- native compilers/interpreters;
- native type systems;
- AST/CST tooling;
- language servers;
- debuggers;
- profilers;
- coverage tooling;
- package/library interoperability.

Structured YAML defines target engineering semantics and planned realization. It may generate constrained source structure, but it should not encode arbitrary executable bodies merely to make them machine-readable.

Declarative artifacts may naturally remain YAML or another native declarative format where that format is already the implementation.

## 8. Realized native source should be projected back into structured form

After implementation, AES should characterize native source into a generated machine-readable projection.

Illustrative form:

```yaml
realized_subject:
  path: src/agentic_engineering_system/repository_context/resolver.py
  revision: <exact-commit>
  content_digest: sha256:...

  symbols:
    - qualified_name: RepositoryContextResolver.resolve
      kind: method
      signature:
        parameters:
          - name: expected_revision
            type: str | null
        returns: RepositoryContextArtifact
      docstring: >
        <actual observed source docstring>

  dependencies:
    imports: [...]
    calls: [...]
    consumes_contracts: [...]
    produces_contracts: [...]

  verification_subjects:
    - path: tests/repository_context/test_resolver.py
      symbols: [...]
```

This projection is observation/current-state substrate, not editable implementation authority.

Existing AES work already contains relevant precursor ideas: native symbol identity, optional SCIP-based cross-language indexing, docstring/signature extraction, dependency-aware characterization, revision-bound evidence, and planned→realized subject mappings.

## 9. Target ↔ realized comparison should be mechanical where possible

With planned and realized projections, AES can derive explicit conformance/current facts:

```text
planned file exists?                         PASS
planned public symbol exists?                PASS
planned signature matches?                   PASS
generated normative region current?          FAIL
required full normative text present?        FAIL
unplanned durable public symbol exists?      GAP / review
planned verification subject exists?         PASS
verification executed at exact revision?     STALE
```

These structural facts do not by themselves establish product success. They contribute to current characterization and evidence adequacy alongside behavioral, human, model-rubric, runtime, or other required evidence.

## 10. Bidirectional projection is the central context mechanism

Normative and realized information should flow in opposite directions over one semantic graph.

Downward:

```text
system/product intent
    ↓
requirements + criteria
    ↓
capabilities/components
    ↓
planned files/symbols
    ↓
generated source-local governed context
```

Upward:

```text
native code/tests/runtime
    ↓
realized-source characterization
    ↓
component/capability current state
    ↓
criterion-level evidence standing
    ↓
gap
```

The same graph can then generate:

- PRD/product views;
- architecture/component views;
- wiki/OKF progressive-disclosure views;
- source-local agent context;
- current/status views;
- gap views;
- verification/evidence views.

## 11. Wiki/OKF should project both normative and realized information

The wiki/OKF remains a progressive-disclosure navigation and synthesis surface, not an independent prose authority.

For a concern/component it should be able to present:

- source-owned summary;
- normative outcomes/requirements;
- full or appropriately disclosed success/disproof criteria;
- capability and dependency structure;
- planned files/public symbols;
- actual files/symbols;
- strong type signatures;
- source docstrings;
- consequential dependency context;
- current characterization;
- gaps;
- verification subjects/evidence standing;
- active plan;
- decisions/research/uncertainties.

Strong typing and docstring information should come from realized native source characterization unless the displayed text is a generated normative region owned by target authority.

## 12. Dependency context should use the same projection architecture

Coupling should be made inspectable rather than left as a human reconstruction problem.

A source-local packet may include consequential relationships such as:

```text
calls
called_by
consumes
produces
depends_on
depended_on_by
shares_state_with
verified_by
invalidates
```

The projection should include enough direct/transitive dependency context to understand change impact without dumping an entire repository graph.

The exact depth and relevance-selection rule remain open design questions.

Data Contracts is a relevant reusable substrate for typed structural dependency validation where its ownership fits, but AES/Company Planning retain project-semantic and planning authority.

## 13. Failure-mode × capability matrix should be a planning input

Planning should explicitly reason about important failure modes and which capabilities prevent, detect, contain, or recover from them.

Illustrative structure:

```yaml
failure_mode:
  id: FM-CTX-001
  statement: >
    A repository folder name is mistaken for authoritative contract ownership.

  mitigations:
    - capability: repository.context.resolve
      role: prevent
    - criterion: SC-CTX-004
      role: detect

  recovery:
    - explicit_unresolved_state
    - exact_source_navigation
```

This creates a trace:

```text
failure mode
    ↓
prevent / detect / contain / recover
    ↓
capability / requirement / control
    ↓
success/disproof criterion
    ↓
verification/evidence
```

The exact taxonomy should be derived during planning rather than frozen from this synthesis.

## 14. Append-only history may provide the lifecycle substrate

The target/current/gap system benefits from preserving history separately from current projections.

Candidate model:

```text
APPEND-ONLY ENGINEERING HISTORY
    accepted normative changes
    accepted topology changes
    decision/supersession events
    implementation observations
    verification/evidence observations
    invalidation/staleness events
    human/model dispositions
             ↓
CURRENT MATERIALIZATION
             ↓
GAP MATERIALIZATION
             ↓
WIKI / SOURCE-LOCAL PROJECTIONS
```

Git history already provides immutable source revisions, but an explicit semantic event/receipt layer may make lifecycle queries and projection regeneration more reliable than reconstructing meaning from Git diffs alone.

Such a log should avoid becoming a duplicate mutable authority. Prefer stable IDs, source revisions/digests, event kind, actor/provider identity where relevant, and references to authoritative payloads/evidence rather than copying all content into another editable record.

The physical home and minimum event schema remain unresolved.

## 15. Candidate invariants

The following are candidates for future architectural decisions and dogfood:

1. Every normative statement has one editable owning source.
2. Success/disproof criteria are part of normative authority.
3. Planning determines the durable target repository topology for greenfield governed work.
4. Every durable governed artifact has an explicit semantic reason for existence.
5. Exact paths are declared when knowable; generated families require explicit generator/output rules.
6. Selected source headers/public skeletons/type signatures/normative docstring regions may remain permanently generated from target authority.
7. Generated source-local governed context includes full verbatim applicable normative and success/disproof text, not only IDs.
8. Native executable bodies remain native-language authority.
9. Realized native source is characterized into revision-bound structured projections.
10. Target↔realized structural variance contributes to current characterization and gaps.
11. Current and gap are materialized projections, not manually maintained prose.
12. Wiki/OKF and source-local context are generated concern/subject views over the same authorities and observations.
13. Important dependency relationships are projected into local working context with explicit provenance/freshness where load-bearing.
14. Planning includes failure-mode→prevention/detection/recovery capability reasoning.
15. Historical changes/observations should be append-only where practical; current views are regenerated.

## 16. Open design questions

The following should remain explicit until dogfood answers them:

1. Which generated source regions persist after initial skeleton creation?
2. At what granularity must planning freeze identity: file, public symbol, selected private symbol, or a combination?
3. Which type signatures are normative design commitments versus implementation detail?
4. How should generated normative docstring regions coexist with ordinary implementation/API documentation?
5. What mechanism safely regenerates source regions without overwriting implementation bodies?
6. How should exact normative text be included without producing pathological repetition in large components while still ensuring agents receive it without dereferencing?
7. What realized-source provider(s) should supply symbols, signatures, references, dependency edges, and docstrings across languages?
8. Where is SCIP sufficient and where are native language providers preferable?
9. What dependency depth/relevance policy produces useful source-local context without context explosion?
10. Which relationship edges are derived projections versus independently authoritative assertions?
11. What is the minimum append-only event/receipt schema needed beyond Git history?
12. What exact failure-mode taxonomy is useful for planning without becoming bureaucracy?
13. How should generated views prove freshness relative to normative authority and realized-source revision?
14. How should human-signoff, deterministic tests, LLM rubrics, runtime observations, and mixed evidence map onto criterion-level conformance?
15. What anti-drift hooks provide the most value without blocking legitimate exploratory work?

## 17. Dogfood recommendation

Before broad implementation, use AES canonical itself as the first greenfield-style governed test of this model.

A bounded dogfood should:

1. select one existing component such as `repository_context`;
2. express its target normative/component record in the candidate structured model;
3. include verbatim requirements, success/disproof criteria, capabilities, failure modes, exact code/test paths, and selected public symbols;
4. generate a governed source skeleton/region from that target;
5. implement or adapt one real change in native code;
6. characterize the realized source back into structured YAML;
7. compare planned versus realized structure;
8. execute required verification and retain revision-bound evidence;
9. materialize current and gap;
10. regenerate wiki/OKF and source-local views;
11. exercise at least one deliberate drift condition that must be blocked or rendered stale;
12. record the lifecycle in append-only history/receipts sufficient to reconstruct why current/gap changed.

Adopt or revise the model based on whether this materially reduces context reconstruction, hidden drift, unsupported completion claims, and agent mistakes without imposing greater coordination cost than it removes.

## 18. Relationship to existing AES research

This synthesis consolidates and extends, rather than supersedes, prior research including:

- `code-map-v4-salvage-for-aes.md` — realized-source facts, dependencies, revision-bound characterization, freshness, and comprehension lessons;
- `aes-evidence-characterization-and-context-suggestions.md` — evidence adequacy, current-state materialization, relationship lifecycle, and source-local packets;
- `2026-09-17-proposed-aes-canonical-skeleton-after-sourcing.md` — planned implementation subjects, realized subjects, planned→realized mapping, SCIP candidate use, and the need for a machine-readable subject manifest;
- `2026-09-17-external-document-semantics-for-normative-model.md` — compact structured normative authority and generated human views;
- Decisions 0003–0006 — component/symbol scope, structured normative records, consequential seams, and architecture realization.

The novel synthesis is the **closed bidirectional realization loop**:

```text
structured target
   → persistent generated source semantics
   → native implementation
   → structured realized characterization
   → target/current/gap reconciliation
   → regenerated working context
```

This should be reviewed through Company Planning before changing accepted AES authority.

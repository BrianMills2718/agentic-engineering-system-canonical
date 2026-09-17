# Incumbent capability inventory

Status: research synthesis; candidate dispositions only. This file does not transfer ownership or select a runtime dependency by itself.

## Donor versus provider rule

An internal repository can be a strong evidence/design donor without being the implementation AES should run. For generally available capabilities, stable platform/standard/off-the-shelf options are examined before selecting bespoke internal code. Runtime-provider selection therefore requires a positive fit decision rather than inheriting a dependency because the code already exists.

| Incumbent | Knowledge / authority role | Runtime/provider disposition | Why |
| --- | --- | --- | --- |
| `BrianMills2718/wiki_methodology` | canonical project-agnostic context/documentation/policy/repo methodology | adopt authority by exact revision; not a runtime provider | reusable methodology should be referenced rather than copied |
| Company Planning | planning/design methodology and implementation-slice derivation donor/incumbent | selected planning provider for current pilot; not assumed permanent for every mechanism | explicitly distinguishes outcomes/thin verticals from optional work-unit graphs and derives boundaries/criteria/topology |
| Enforced Planning | execution-governance patterns and current incumbent | selected execution-governance provider for current pilot; evaluate individual runtime dependencies positively | context delivery, claims, lanes/worktrees, checkpoints, checks, lifecycle enforcement |
| Agentic Capability Architecture | canonical capability-plane authority/incumbent | reuse for capability identity/discovery/binding; provider implementations still sourced independently | semantic capability identity and provider/composition knowledge are its native concern |
| Data Contracts | typed-boundary/composition authority and donor | reuse only where its provider-neutral semantics match the actual boundary | typed contracts and compatibility semantics; not a generic repository-context owner |
| Project Meta policy system | policy/control evidence, design donor, and ecosystem-policy authority where applicable | unresolved / selective runtime reuse | mature policy registry, enforcement, observation, friction and self-application work, but substantial ecosystem-specific structure |
| `Inside-Success/agentic-engineering-system` | predecessor AES evidence/design donor | default no dependency; unresolved capability-by-capability | working orchestration/context/policy mechanisms plus historical architectural sediment |
| `BrianMills2718/aes` | archived predecessor evidence/design donor | no current runtime dependency; salvage ideas only after sourcing | policy-admission, invariant, recovery, negative-control and audit lessons |
| `BrianMills2718/code_map_v4` | evidence/design donor for revision-bound characterization, source anchoring, freshness/invalidation, evidence-bearing relationships and evaluation lessons | **provider unselected; default no dependency** | strong experiments and lessons, but Python/wiki product topology is not the canonical AES boundary and off-the-shelf primitives should be examined first |

## Candidate donor themes

### AES lineage

- `BLOCK -> recovery -> ALLOW` policy-admission behavior
- explicit `PASS` / `FAIL` / `NONE` discipline, extended by the new methodology with `ERROR` / `STALE`
- negative controls before calling a control evidenced
- scope/coverage auditing and independent census
- policy self-application
- plan-owned review/audit/context triggers
- sanctioned plan-change route
- learning records that must be activated to affect future work

### Code Map V4

- revision-bound evidence envelopes
- dependency-aware freshness and precise invalidation
- explicit epistemic state
- evidence-bearing relationships where load-bearing
- negative-control evolution
- independent evaluation signals
- the warning that structured facts are substrate, not comprehension

The Code Map donor synthesis on `main` is valuable research, but its tentative “characterization kernel” should be read as a **characterization capability requirement** until provider sourcing selects an implementation. Plan 001 does not need broad source anchoring, indexing, or incremental characterization infrastructure unless its external vertical demonstrates such a gap.

## Selection rule

For each required semantic capability:

```text
required boundary
  -> stable platform / standard / mature off-the-shelf landscape
  -> ACA-known providers
  -> internal donor/provider candidates
  -> compose where possible
  -> implement only the residual semantics
```

Every selected internal runtime dependency must state why it is preferable to stable external alternatives for the actual boundary. Every rejected donor remains usable as evidence and design input without becoming a dependency.
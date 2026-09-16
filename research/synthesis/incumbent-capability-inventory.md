# Incumbent capability inventory

Status: research synthesis; candidate dispositions only. This file does not transfer ownership.

| Incumbent | Candidate AES role | Initial disposition | Why |
| --- | --- | --- | --- |
| `BrianMills2718/wiki_methodology` | project-agnostic context/documentation/policy/repo architecture | reuse | canonical methodology owner; adopt by revision rather than copy |
| Company Planning | AES planning/design compiler | reuse | derives outcomes, requirements, criteria, boundaries, target topology, verification topology, and plans |
| Enforced Planning | AES plan execution/governance runtime | reuse | context delivery, claims, lanes/worktrees, checkpoints, checks, lifecycle enforcement |
| Agentic Capability Architecture | AES capability plane | reuse | semantic capability identity, discovery, provider binding, composition/reuse knowledge |
| Data Contracts | typed boundary/composition substrate | reuse where applicable | provider-neutral typed contracts and compatibility semantics; not provider/runtime owner |
| Project Meta policy system | policy authority/infrastructure evidence and reusable mechanisms | unresolved / selective reuse | contains mature policy registry, enforcement, observation, friction, and self-application work but also ecosystem-specific authority |
| `Inside-Success/agentic-engineering-system` | predecessor/incumbent AES mechanism and evidence source | unresolved capability-by-capability | contains working orchestration/context/policy mechanisms plus historical architectural sediment |
| `BrianMills2718/aes` | archived predecessor evidence | historical / salvage candidates | valuable policy-admission, invariant, recovery, negative-control and audit lessons; not a current implementation authority |

## Candidate salvage themes from AES lineage

- `BLOCK -> recovery -> ALLOW` policy-admission behavior
- explicit `PASS` / `FAIL` / `NONE` discipline, extended by the new methodology with `ERROR` / `STALE`
- negative controls before calling a control evidenced
- scope/coverage auditing and independent census
- policy self-application
- plan-owned review/audit/context triggers
- sanctioned plan-change route
- learning records that must be activated to affect future work

Each candidate must be evaluated against the canonical system boundary and real seam before adoption.

---
type: Questions
title: Discussion after the documentation repair
description: Source-linked questions, recommendations and concerns preserved for discussion after orientation is repaired
status: current
last_checked: 2026-11-13
---

# Questions, recommendations and concerns

The owning record is [open-questions.json](../docs/planning/open-questions.json).
This view is rendered from its open entries during the 2026-11-13 repair; it is
not an additional manually maintained tracker. It includes earlier unresolved
items as well as findings from the repair. No recommendation here authorizes a
runtime change, restarts a retired project or enables a timer.

## Discuss after repair

### Q2: Inside Success rollout

Decision 0011 paused the Inside Success team rollout until whygame5 produced a result under AES; that condition was met on 2026-09-26 and the call to resume was never made. The one-tool design says any repository, personal or Inside Success, installs Lockstep with one command; slice 6 merged on 2026-11-12 and Team-Brains' Project Brain runner, an Inside Success repository, now vendors Lockstep's wheel (Team-Brains#1183, wiki/lockstep.md:22). Close the old rollout item, or keep it open?

Recommendation: Close decision 0011 item 4: the rollout it paused was of the v0.2 `aes` command line, which now retires. Putting Lockstep into Inside Success repositories is slice 6 of the one-tool plan and would come to you then as its own decision.

Sources: [docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md](../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md), [docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md](../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md), [proposals/one-planning-tool/DESIGN.md](../proposals/one-planning-tool/DESIGN.md), [wiki/lockstep.md](../wiki/lockstep.md).

Owner: brian.

### Q17: Not in the code2 repository format

~/code2/AGENTS.md brings each repository into the code2 format when it is next changed; scripts/repo_format.py reports this one 0 of 1 compliant (missing docs/index.md, arc42, a .c4 model, a Makefile that mentions code2check). The one-tool build changes this repository, and its slice 6 replaces code2check with lockstep in the code2 template. Adopt the format now, or in slice 6?

Next evidence or disposition: An argument settles it: the format's code2check target is the part slice 6 replaces, so adding it now would be redone; add docs/index.md now (pointing at wiki/index.md) and the rest in slice 6, when the template installs lockstep.

Sources: [workspace instructions](https://github.com/BrianMills2718/code2-workspace/blob/main/AGENTS.md), [proposals/one-planning-tool/DESIGN.md](../proposals/one-planning-tool/DESIGN.md), [docs/planning/checks.txt](../docs/planning/checks.txt).

Owner: agent.

### Q19: Who runs the plan check

Slice 5 merged (#832) and kept both copies of the plan and acceptance checks, with the same checks (wiki/lockstep.md:45): does Company Planning's adoption gate (method_conformance adopt) now call `lockstep plan check`, or keep its own copy for the Inside Success team?

Next evidence or disposition: An argument settles it: the design's reason for the slice is one definition of the format, which a kept copy defeats; the open fact is whether Inside Success repositories can install lockstep (Q2). Pointing the adoption gate at `lockstep plan check` is a change in the Company Planning plugin, not in this repository.

Sources: [proposals/one-planning-tool/DESIGN.md](../proposals/one-planning-tool/DESIGN.md), [wiki/lockstep.md](../wiki/lockstep.md), [src/lockstep/plan_check.py](../src/lockstep/plan_check.py).

Owner: agent.

### Q21: Three feedback jobs switched off

Three of the feedback loop's five jobs (weekly analysis, effect counter, fix owner) have been switched off since about 2026-10-12, with no recorded reason; only the collector and the labels job run. Turn them back on?

Recommendation: Inspect collector reliability (Q29), then restore one complete correction-to-verified-fix path before broad autonomous analysis. Do not enable jobs as part of a documentation repair.

Sources: [scripts/learning_loop/systemd/README.md](../scripts/learning_loop/systemd/README.md).

Owner: brian.

### Q24: Two projectors remain where the design says one

Two projectors remain inside the Lockstep package: the cog one for layout and AES-plan files and code2check's `Implements:` one (wiki/lockstep.md:35), where the design says one (DESIGN.md:43). Is a merge a seventh slice, or is the design amended?

Next evidence or disposition: An argument settles it: the design table (DESIGN.md:43) lists one projector; the code has two; the Lockstep session says whether it plans a seventh slice or amends the design (wiki/lockstep.md:35: merging them is not yet planned).

Sources: [proposals/one-planning-tool/DESIGN.md](../proposals/one-planning-tool/DESIGN.md), [wiki/lockstep.md](../wiki/lockstep.md).

Owner: agent.

### Q25: Prove the complete synchronization loop

Which current consumer demonstrates requirements into docstrings, implementation status back into normative documents, and fresh wiki navigation after an edit?

Evidence: A complete example is needed before describing all three surfaces as automatically aligned.

Recommendation: Replay one requirement through the real installed hooks and build, deliberately bypass refresh once, and inspect the stale-check refusal. Preserve every transition and revision.

Sources: [docs/architecture/LOCKSTEP.md](../docs/architecture/LOCKSTEP.md), [src/lockstep/checks/project.py](../src/lockstep/checks/project.py), [src/lockstep/doc_projection.py](../src/lockstep/doc_projection.py).

Owner: agent.

Additional observation: the [earlier CLI replay](../evidence/runs/projection-worked-20261113.json)
preserved normative-down text. The [AES self-adoption receipt](../evidence/runs/projection-self-adoption-20261113.json)
now records one real Claude Edit invoking the installed hook and updating both
architecture and wiki blocks, plus read-only stale refusal and recovery. This
closes G-SELF and the bounded Claude part of G-NATIVE. Native Codex execution,
default-session loading and general OpenSpec upward-edit parity remain open;
see the [current observation](../docs/architecture/LOCKSTEP.md#aes-self-adoption-observation).

### Q26: Guard must check every affected path

Does the edit guard judge every file and rename destination before allowing a patch?

Evidence: Read-only decide() probes in block mode allowed a planned-first/unplanned-second patch and an unplanned rename destination; the extra file alone was denied.

Recommendation: Repair complete write-set aggregation and native payload adaptation in a separately authorized implementation; verify the actual host event as well as the decision function.

Sources: [src/lockstep/hook.py](../src/lockstep/hook.py), [tests/lockstep/test_lockstep_hook.py](../tests/lockstep/test_lockstep_hook.py).

Owner: agent.

### Q27: Installation acceptance versus active enforcement

Does the public README installation produce an active commit hook, rather than just written configuration?

Evidence: The retained A5 row passes while its full agent trace reports lefthook install stopped because core.hooksPath was already set.

Recommendation: Make installation evidence distinguish configured from active and attempt a deliberately invalid commit through the installed hook. Preserve the existing global hook setup.

Sources: [scripts/acceptance/a5.py](../scripts/acceptance/a5.py), [docs/planning/runs/lockstep-acceptance/a5.json](../docs/planning/runs/lockstep-acceptance/a5.json), [docs/planning/runs/lockstep-acceptance/a5-readme-agent.jsonl](../docs/planning/runs/lockstep-acceptance/a5-readme-agent.jsonl).

Owner: agent.

### Q28: Empty policy discovery must stay unknown

Does the policy checker discover the current policy population and report missing coverage honestly?

Evidence: A read-only policies.check(30) on 2026-11-13 returned policies=0 and gaps=[]; defaults still point at the old workspace instruction bootstrap.

Recommendation: Use the current owning instruction/source records and expose discovery completeness before trusting a zero-gap result.

Sources: [scripts/learning_loop/policies.py](../scripts/learning_loop/policies.py), [docs/rules/register.yaml](../docs/rules/register.yaml), [docs/architecture/FEEDBACK_AND_POLICY.md](../docs/architecture/FEEDBACK_AND_POLICY.md).

Owner: agent.

### Q29: Collector reliability

Why did the latest collector service time out, and which inputs and filing steps completed?

Evidence: Retained systemd state on 2026-11-13: collector Result=timeout, ExecMainStatus=143, exit 06:09:03 America/New_York; labels success at 06:15:35. A bounded journal query returned no entries. The latest completed collector receipt was November 12.

Recommendation: Inspect the retained collector trace and step boundaries before increasing intake or enabling further stages; scheduling state alone is not completion evidence.

Sources: [scripts/learning_loop/collect_feedback.py](../scripts/learning_loop/collect_feedback.py), [scripts/learning_loop/systemd/feedback-collector.service](../scripts/learning_loop/systemd/feedback-collector.service), [docs/architecture/FEEDBACK_AND_POLICY.md](../docs/architecture/FEEDBACK_AND_POLICY.md).

Owner: agent.

### Q30: Wiki freshness has a declared scope

How are every-file summaries and navigation refreshed without silent exclusions, missing summaries or stale compiled views?

Evidence: The earlier check covered 69 reader Markdown files from a repository with 407 tracked files. The complete-file review replaces that subset catalog and binds content-derived summaries to inputs. Native declared-fact refresh still does not maintain every compiled description.

Recommendation: Use the complete inventory and source hashes to identify changed inputs; refresh source-owned descriptions and content-derived summaries with semantic review. Keep coverage, summary adequacy and freshness as separate checks.

Sources: [documentation assessment](../docs/architecture/DOCUMENTATION.md#coverage-and-consolidation-assessment), [inventory](../docs/planning/file-inventory.json), [catalog](documents.md).

Owner: agent.

### Q31: OpenSpec upward-edit parity

Can an edit to normative text in a current OpenSpec/layout docstring draft, accept and record the corresponding requirement change?

Evidence: The retained docstring_up implementation uses AES target families and aes plan accept; general OpenSpec/layout round-trip parity was not established by source inspection.

Recommendation: Trace one supported change through draft, review/acceptance, history and regenerated copies; preserve an explicit draft boundary rather than silently changing accepted intent.

Sources: [src/lockstep/docstring_up.py](../src/lockstep/docstring_up.py), [src/lockstep/change_log.py](../src/lockstep/change_log.py), [docs/architecture/LOCKSTEP.md](../docs/architecture/LOCKSTEP.md).

Owner: agent.

### Q32: Behavioral structure and typing enforcement

How does current planning enforce the intended behavioral units and typed interfaces without inventing one-file-per-behavior rules?

Evidence: The approved plan format names file purpose, requirement links, tests and optional typed exports. It permits multiple requirements in one file and leaves decomposition to the planner.

Recommendation: Assess representative planned units against their behavioral contracts and proving tests; record which existing guarantees are checked and which depend on planning judgment before proposing stronger requirements.

Sources: [openspec/specs/lockstep-plan-format/spec.md](../openspec/specs/lockstep-plan-format/spec.md), [src/lockstep/layout_plan.py](../src/lockstep/layout_plan.py), [src/lockstep/scaffold.py](../src/lockstep/scaffold.py), [docs/architecture/LOCKSTEP.md](../docs/architecture/LOCKSTEP.md).

Owner: agent.

### Q33: Effect evidence and observation coverage

What does an effects report establish when it counts sightings without comparable opportunities or observation completeness?

Evidence: The retained effects mechanism requires enforcement receipts, but before/after sightings alone do not establish lower failure probability.

Recommendation: For the first restored feedback path, distinguish verified disposition and later recurrence from a claim of improved failure rate; name relevant opportunities and missing observation.

Sources: [scripts/learning_loop/effects.py](../scripts/learning_loop/effects.py), [scripts/learning_loop/problems.py](../scripts/learning_loop/problems.py), [docs/architecture/FEEDBACK_AND_POLICY.md](../docs/architecture/FEEDBACK_AND_POLICY.md).

Owner: agent.

### Q34: Self-adoption and manifest scope

Which current AES mechanisms are exercised on this repository, and which declarations still describe retired machinery?

Evidence: At inspection revision 05ee80c1a there was no root lockstep.yaml; make check runs instruction sync, pytest and mypy. The repository manifest and historical brain pages retained older governance claims.

Recommendation: Keep the current reading path honest and evaluate self-adoption separately. Reconcile remaining manifest provider fields against actual callers before changing runtime configuration.

Sources: [Makefile](../Makefile), [.agentic/repo.yaml](../.agentic/repo.yaml), [docs/retired/2026-11-12.md](../docs/retired/2026-11-12.md).

Owner: agent.

### Q35: Reconcile the original policy inventory

For each of the 263 Project Meta policies, where is its current authoritative statement, disposition, delivery path and observed enforcement?

Evidence: Read-only inspection found 263 original policy IDs and the same 263 IDs in the AES disposition manifest. All manifest rows have activation:none. The separate AES register shrank 33→12→1 in November; those commits did not remove the Project Meta registry.

Recommendation: Preserve the original registry and the provisional migration manifest. Map actual sources and effects before accepting keep/covered/retire labels as execution history.

Sources: [policy source map](policy-and-rules.md#where-are-the-hundreds-of-project-meta-policies), [manifest](../docs/rules/legacy-dispositions.yaml).

Owner: agent.

## Ecosystem consolidation and predecessor review

The following entries are projected from the owning ledger after Decision 0014.

### Q36: One capability discovery route

Which existing catalogue/export/view should implement the adopted AES discovery route, and how will ACA Decision 0012, workspace Decision 0004 and Project Meta be explicitly reconciled?

Recommendation: Keep native provider facts at source and AES-owned cross-project decisions; select the publication/storage mechanism after the record comparison.

Next evidence or disposition: Compare unique entries, readers/writers, stable aliases and sufficient existing catalogue products; demonstrate one route before changing old instructions.

Sources: [Decision 0014](../docs/decisions/0014-ecosystem-consolidation-and-legacy-review.md), [source review](../docs/architecture/ECOSYSTEM.md).

Owner: agent.

### Q37: Qualified capability and schema identities

How are legacy capability/family IDs, provider-qualified action names, versions and input/output schema references preserved without ambiguous joins?

Recommendation: Preserve IDs/aliases and exact references; never infer substitutability from similar names.

Next evidence or disposition: Produce alias mappings and show distinct same-named tools cannot overwrite each other; retain explicit schema compatibility/adaptation evidence.

Sources: [Decision 0014](../docs/decisions/0014-ecosystem-consolidation-and-legacy-review.md), [source review](../docs/architecture/ECOSYSTEM.md).

Owner: agent.

### Q38: Discovery evidence and freshness

How does discovery distinguish documented, candidate, source-resolved, available, consumer-adopted and fit-for-this-requirement states, including incomplete or broken inputs?

Recommendation: Expose source-level unknown/error/stale and keep declared versus observed consumer edges separate.

Next evidence or disposition: Exercise missing source, invalid input, stale revision and catalog-only capability; inspect a real consumer receipt separately from a dependency declaration.

Sources: [Decision 0014](../docs/decisions/0014-ecosystem-consolidation-and-legacy-review.md), [source review](../docs/architecture/ECOSYSTEM.md).

Owner: agent.

### Q39: Legacy review coverage

Which older source sections have actually been read, what unique ideas remain, and what is the next bounded reading tranche?

Recommendation: Treat the first review as bounded; preserve useful requirements even without current runtime use and reject machinery that lacks a present purpose.

Next evidence or disposition: Continue the source/revision/disposition table in ECOSYSTEM.md; inspect concern lifecycle next, then selected policy families and instruction delivery.

Sources: [Decision 0014](../docs/decisions/0014-ecosystem-consolidation-and-legacy-review.md), [source review](../docs/architecture/ECOSYSTEM.md).

Owner: agent.

### Q40: Retired entrypoint and consumer reconciliation

Which Project Meta and Enforced Planning entrypoints still route agents into old claims/mailbox authority, and which surviving consumers need their implementation?

Recommendation: Keep useful design rationale and current consumers; route old global instructions to the current AES/workspace owners instead of reviving retired regimes.

Next evidence or disposition: Inventory exact readers and installed routes; change upstream pointers through their owning repositories after preserving live contract consumers.

Sources: [Decision 0014](../docs/decisions/0014-ecosystem-consolidation-and-legacy-review.md), [source review](../docs/architecture/ECOSYSTEM.md).

Owner: agent.

### Q41: Minimum composition model

Does ordinary ecosystem discovery require the rich data-contracts action/compiler vocabulary, or are typed provider references and the minimal requirement/output graph sufficient?

Recommendation: Keep contracts at their native owner and make richer composition optional until justified.

Next evidence or disposition: Compare actual ordinary plans and consumer guarantees; adopt richer effects/resources/transition semantics only for an explicit unsatisfied requirement.

Sources: [Decision 0014](../docs/decisions/0014-ecosystem-consolidation-and-legacy-review.md), [source review](../docs/architecture/ECOSYSTEM.md).

Owner: agent.

### Q42: Concern identity and repair closure

Which existing system owns durable concern identity, verifier-owned closure and recurrence reopening across native feedback evidence and GitHub issues?

Recommendation: Compose existing records and native evidence rather than create another independent concern tracker; require landed-revision closure and legitimate counter-cases.

Next evidence or disposition: Read the Project Meta concern executor/verifier lifecycle and compare its exact transitions with AES feedback implementation, Q21, Q29 and Q31.

Sources: [Decision 0014](../docs/decisions/0014-ecosystem-consolidation-and-legacy-review.md), [source review](../docs/architecture/ECOSYSTEM.md).

Owner: agent.

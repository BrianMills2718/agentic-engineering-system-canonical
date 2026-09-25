---
doc_role: active_authority
authority: canonical_if_merged
status: accepted
accepted_by: Brian Mills (2026-09-25 roadmap operating rule; phase 7b instruction)
date: 2026-09-25
reversible: true
partially_supersedes:
  - docs/decisions/0001-canonical-convergence-boundary.md (Decision items 3 and 6, for the v0.2 governed roots)
  - docs/decisions/0002-company-planning-aes-profile-before-fork.md (as the planning route for the v0.2 governed roots)
  - docs/decisions/0009-modular-product-design-without-parallel-aca-platform.md (Enforced Planning and Company Planning ownership rows, for the v0.2 governed roots)
---

# Decision 0010 - AES v0.2 greenfield MVP accepted as realized

## Context and scope

The v0.2 greenfield proposal (`proposals/aes-v0.2-greenfield/`, 2026-09-24)
was built phase by phase under
[`25-roadmap-to-mvp-acceptance.md`](../../proposals/aes-v0.2-greenfield/25-roadmap-to-mvp-acceptance.md),
with each phase's realization, findings and wrong-when conditions recorded in
[`24-pre-probe-decisions.md`](../../proposals/aes-v0.2-greenfield/24-pre-probe-decisions.md)
sections 6-21. Two consumers were governed by it: `BrianMills2718/whygame5`,
governed by AES from its first commit (the greenfield consumer), and AES
canonical itself, governed by its own `.aes/` target since phase 6b (a
retrofit, so it does not count as the fresh consumer for SC-GF-009).

This decision records what is accepted, on what evidence, with which standing
decisions, and what is explicitly not claimed.

## Decision

**Accepted: the AES v0.2 greenfield MVP as realized** — the ten components
`RU-AES-RECORDS`, `-PROJECT`, `-PLANNING`, `-TOPOLOGY`, `-CHARACTERIZE`,
`-EVIDENCE`, `-RECONCILE`, `-CONTEXT`, `-CLI`, `-DISTRIBUTION` under
`src/agentic_engineering_system/` with their tests under `tests/greenfield/`,
the `aes` command, and the `.aes/` materialization — as the architecture that
governs AES canonical's governed roots and whygame5.

- The accepted architecture documents are
  [`docs/architecture/greenfield-v0.2/`](../architecture/greenfield-v0.2/README.md):
  plain copies of the ten realized candidates, each amended where the build
  differs from the candidate and listing its amendments. The proposal
  directory stays in place as lineage, not authority.
- For AES canonical, [`.aes/target.yaml`](../../.aes/target.yaml) is the live
  authority. Where an accepted document and the target disagree, the document
  is wrong and is corrected; the target changes only through `aes plan`.
- The user-facing start is
  [`docs/greenfield/GETTING_STARTED.md`](../greenfield/GETTING_STARTED.md); the
  one-screen state is `aes status`.
- v0.1 material (the `repository_context` provider, `aes-repo-context`,
  `tests/repository_context/`, Plans 001/002, the bootstrap architecture files
  in `docs/architecture/`) is retained, not deleted, under the v0.1
  disposition below.

## Evidence

`aes status` on AES canonical at the evidence commit of this change (the
header's HEAD is the commit the re-recorded evidence names; the records and
this text are the next commit, which is why the header says dirty; clean-user run 3, recorded one commit later, moves SC-GF-001 to SUPPORTED — final counts: 9 supported, 0 insufficient):

```text
OK status: agentic-engineering-system-canonical-target at 62fe041ba9fd9945014b592b39c38e1b4eb21de2 (dirty: working tree differs from HEAD under governed roots or .aes/)
  artifacts: 39 realized, 0 unrealized, 0 drifted; 0 orphan(s)
  criteria: 8 supported, 1 insufficient, 0 refuted; 0 unsupported evidence requirement(s) with no route
  observations: 13 current, 23 stale, 1 unknown, 0 unreachable; 24 superseded
  plans: 3 accepted, 1 unreachable
  first open gap per component:
    RU-AES-RECORDS: no open gap
    RU-AES-PROJECT: insufficient SC-GF-001 - ER-SC-GF-001-01 NO_CURRENT_SUPPORT
    RU-AES-PLANNING: no open gap
    RU-AES-TOPOLOGY: no open gap
    RU-AES-CHARACTERIZE: no open gap
    RU-AES-EVIDENCE: no open gap
    RU-AES-RECONCILE: no open gap
    RU-AES-CONTEXT: no open gap
    RU-AES-CLI: insufficient SC-GF-001 - ER-SC-GF-001-01 NO_CURRENT_SUPPORT
    RU-AES-DISTRIBUTION: insufficient SC-GF-001 - ER-SC-GF-001-01 NO_CURRENT_SUPPORT
  warning: plan PLAN-AES-SELF-GOVERN accepted_at_revision 80e6da33 is not reachable from HEAD (squash-merged or deleted branch?); the target already carries its delta, so this does not fail
  INSUFFICIENT criteria are normal while work is in progress and do not fail this command; a REFUTED criterion, an orphan or drift does.
```

Per criterion, from `aes evidence status` at the same commit:

| criterion | evidence requirement | standing (from `aes evidence status`) |
| --- | --- | --- |
| SC-GF-001 (SUPPORTED) | ER-SC-GF-001-01 | SUPPORTED - supported by OBS-AES-CLEAN-USER-3dd2b9a (clean-user run 3, recorded after the status block above); OBS-GF-INIT-UNIT-62fe041b and OBS-GF-DISTRIBUTION-INSTALL-62fe041b INCONCLUSIVE (CURRENT, local tests by design); earlier records STALE or superseded |
| SC-GF-002 (SUPPORTED) | ER-SC-GF-002-01 | SUPPORTED - supported by OBS-GF-RECORDS-449cd54b |
| SC-GF-003 (SUPPORTED) | ER-SC-GF-003-01 | SUPPORTED - supported by OBS-GF-TOPOLOGY-62fe041b |
| SC-GF-003 (SUPPORTED) | ER-SC-GF-003-02 | SUPPORTED - supported by OBS-GF-SELF-GOVERNANCE-62fe041b, OBS-GF-TOPOLOGY-62fe041b |
| SC-GF-004 (SUPPORTED) | ER-SC-GF-004-01 | SUPPORTED - supported by OBS-GF-PLANNING-62fe041b, OBS-GF-SELF-GOVERNANCE-62fe041b |
| SC-GF-005 (SUPPORTED) | ER-SC-GF-005-01 | SUPPORTED - supported by OBS-GF-CONTEXT-STRUCTURAL-62fe041b |
| SC-GF-005 (SUPPORTED) | ER-SC-GF-005-02 | SUPPORTED - supported by OBS-AES-CONTEXT-AB-RETAINED-377e9707 |
| SC-GF-006 (SUPPORTED) | ER-SC-GF-006-01 | SUPPORTED - supported by OBS-GF-CHARACTERIZE-62fe041b |
| SC-GF-006 (SUPPORTED) | ER-SC-GF-006-02 | SUPPORTED - supported by OBS-GF-CHARACTERIZE-62fe041b |
| SC-GF-007 (SUPPORTED) | ER-SC-GF-007-01 | SUPPORTED - supported by OBS-GF-EVIDENCE-62fe041b, OBS-GF-EVIDENCE-CONTROLS-62fe041b, OBS-GF-RECONCILE-62fe041b |
| SC-GF-008 (SUPPORTED) | ER-SC-GF-008-01 | SUPPORTED - supported by OBS-GF-EVIDENCE-62fe041b, OBS-GF-EVIDENCE-CONTROLS-62fe041b, OBS-GF-RECONCILE-62fe041b |
| SC-GF-009 (SUPPORTED) | ER-SC-GF-009-01 | SUPPORTED - supported by OBS-AES-WG5-LIFECYCLE-38df3e5 |

SC-GF-001 was the last criterion to close. Its evidence of record at the
phase-7b evidence commit, `OBS-AES-CLEAN-USER-2d3486b`, had gone STALE because
phase 7a and 7b modified files that run exercised. Clean-user run 3 was then
run against this branch's commit `3dd2b9a` (a fresh agent with only the
getting-started page, same setup and private-repository caveat as runs 1 and
2) and recorded as `OBS-AES-CLEAN-USER-3dd2b9a`, SUPPORTS; with it, `aes
status` at the merged state reads **9 supported, 0 insufficient, 0 refuted**.
The local tests routed to ER-SC-GF-001-01 remain INCONCLUSIVE by design (24
§17). This acceptance did **not** downgrade SC-GF-001 to "documented instead
of observed" (the roadmap's phase-7 wrong-when). The mechanism was observed working twice (`0503735`,
`2d3486b`); what is missing is a current observation, which the evidence rule
correctly demands after every change to the exercised code.

## Standing decisions carried by this acceptance

Each was taken in `24` or the roadmap and is accepted here with its
wrong-when condition.

| Decision | Source | Wrong when |
| --- | --- | --- |
| **D1 governed roots.** The no-orphan rule applies only to files under the governed roots declared in `.aes/project.yaml`; inside one, every tracked file is a planned artifact at its exact path. | 24 §1, §8, §17 | a real consumer needs a governed file that cannot be expressed as an additional governed root; the check catches nothing because roots were declared too narrowly; or a generated file under a governed root cannot be listed by exact path (then implement generation rules). |
| **D2 standing is conjunction-only.** A criterion is SUPPORTED only when every evidence requirement has a CURRENT, non-superseded observation that SUPPORTS it; any CURRENT refutation makes it REFUTED; otherwise INSUFFICIENT. | 24 §1, §9 | a real criterion genuinely needs "any one of" or "N of M" and the workaround distorts its meaning; or a CURRENT refutation should be outweighed rather than win. |
| **Keep private.** The AES repository stays private until AES has shown it provides value; ER-SC-GF-001-01's evidence of record is an on-machine clean-user run (fresh agent, page only, maintainer credentials); the true no-private-access run is deferred. | 25 phase 2 | a consumer other than whygame5 or AES itself needs to install AES (then make the distribution reachable and re-run the probe). |
| **Merge-commit rule and reachability.** Evidence and plans name the commit they were produced at; an observation whose commit is not an ancestor of HEAD is UNREACHABLE and never counts; replaced records get `superseded_by`, never deletion; PRs carrying evidence merge with a merge commit; `aes evidence record` and `aes plan accept` warn off the default branch; `aes status` counts unreachable accepted plans as a warning. | 24 §19, §21 | a legitimate workflow needs evidence from a commit intentionally never merged (e.g. release branches kept apart) and UNREACHABLE forces re-recording that proves nothing new; or `superseded_by` chains grow long enough that people delete records instead (then key freshness on content identity rather than ancestry). |
| **ER-SC-GF-005-02 re-scoped.** The requirement is a pre-registered fresh-agent comparison run and retained with its verdict either way (two runs minimum), not a demonstration that the context packet reduces reconstruction cost; that discovery claim is recorded as not established. | 24 §18, §20; `PLAN-AES-RESCOPE-CONTEXT-AB` | a consumer appears whose target is large enough that reading it whole measurably costs (hundreds of criteria) and a rerun there shows the packet arm materially ahead; or the re-scoped wording is read as evidence that the packet helps. |
| **Negative controls.** A "break it on purpose" observation carries `control: {kind: negative, base_revision, ...}`; freshness is computed from the unmodified base, reachability applies to the base, and a missed mutation must REFUTE. | 24 §16, §19 | a control's base branch is deleted and `aes status` fails on the consumer (then accept a tag); or a positive observation needs expected/observed outcomes too. |
| **Entry-level target refs.** An observation may depend on target entries (`dependency_target_refs`) rather than the whole target file; an entry is the id's whole mapping compared after a strict load. | 24 §16 | an observation that references a criterion goes STALE because a sibling requirement under the same criterion was edited; or a recorded SUPPORTS stays CURRENT after its criterion's statement changes in a way that makes the old test insufficient. |
| **Vocabulary mapped, not widened.** Kinds outside the loader's vocabulary are mapped (evidence `contract_validation` -> `deterministic_test`, `external_consumer_observation` -> `runtime_observation`; artifact `normative_authority` -> `source`, `documentation` -> `configuration`; proof role `supporting` -> `direct`). | 24 §17 | a requirement is `contract_validation` in a sense `deterministic_test` misstates (a check no test runs); then add the kind to `records.EvidenceKind`. |
| **Removal requires the file out of the index first.** `remove:` in a proposal deletes target entries; a removed governed planned artifact's file must already be moved or deleted. | 24 §20 | a real removal needs the file and the entry to leave in one commit; then let accept stage the move itself. |
| **v0.1 disposition.** The eight empty v0.1 placeholder subpackages are archived under `archive/v0.1-placeholders/` (`PLAN-AES-ARCHIVE-V01-PLACEHOLDERS`); `repository_context/` (console script `aes-repo-context`, `tests/repository_context/`) and the package `__init__.py` are retained as planned artifacts justified by `NI-AES-HIST`; the v0.1 bootstrap documents, Plans 001/002 and the Enforced Planning install stay in place as retained v0.1 material. | 24 §17, §20 | a v0.1 file is changed on main without anyone noticing it is not v0.2 work, or phase work cannot tell retained files from v0.2 work by `semantic_justification_refs` alone (then add a kind or disposition field); or a retained v0.1 surface is used as if it were v0.2 authority. |
| **The AES gate is `make aes` / `make aes-check`**, not `make check` (which stays Enforced Planning's). | 24 §17 | an agent runs `make check` believing it runs the AES gate; then make `check` depend on `aes`. |

## Relation to earlier decisions

As `24` §1 D4 requires, supersession is stated. For the v0.2 governed roots
(`src/agentic_engineering_system/` and `tests/greenfield/`) and the `.aes/`
control root:

- Decision 0001 items 3 (incumbents as capability sources with retained ownership)
  and 6 (no local package until Company Planning derives topology) are
  superseded: the topology is planned in `.aes/target.yaml` through `aes plan`.
- Decision 0002 (AES-local profile over Company Planning as the planning route)
  is superseded as the planning route for that scope.
- Decision 0009's rows giving Company Planning planning derivation and
  Enforced Planning execution-governance authority are superseded for that
  scope; its modular-design guidance (AES-CAP-003..005) stands.

Decisions 0003-0006 and 0008 are carried forward, re-derived by v0.2 under new
names; 0007 was already superseded by 0008. Outside the v0.2 scope (the v0.1
provider, Plan 002, the Enforced Planning install and its `make check`), the
earlier decisions still apply unchanged. v0.1 governance was bypassed to
produce v0.2 (all 67 proposal-branch commits `[Unplanned]`, 24 §1 D5): that is
recorded here as evidence for v0.2's stance that hooks are invocation adapters,
not enforcement.

## Explicit non-claims

- **Value beyond mechanism is not demonstrated.** Both fresh-agent context
  A/Bs (probe 0 on whygame5, phase 6 on AES itself) were indistinguishable
  between the packet arm and the repository-only arm. What is shown is that
  the mechanisms work as specified on two real consumers, not that governing
  a project with AES makes agents measurably better or faster.
- **Single machine.** Every run, including both clean-user runs, was on
  Brian's one WSL machine with his credentials.
- **Two consumers only**, one of them AES itself (a retrofit). whygame5's
  `aes plan`-accepted runner plan (`PLAN-WG5-RUNNER`) is still unrealized; its
  complete lifecycle is the initially planned contracts, graph and replay
  (24 §20).
- **Repository private.** No user without access to Brian's private
  repositories has installed AES.
- **SC-GF-001 is not currently SUPPORTED** (see Evidence).
- Retrofit of arbitrary existing repositories remains a non-goal of
  `OUT-GF-001`.

## Wrong when

This acceptance was the wrong call if any of the following is observed:

- clean-user run 3 on current code cannot reach initialized state from the
  getting-started page alone, or reaches it only by reading AES source, the
  proposals directory or whygame5;
- acceptance turns out to need any criterion downgraded to "documented instead
  of observed" (the roadmap's phase-7 wrong-when) — including SC-GF-001 being
  treated as closed without a current SUPPORTS observation;
- an accepted document under `docs/architecture/greenfield-v0.2/` contradicts
  `.aes/target.yaml` or the code and an agent acts on the document;
- the next consumer (a third project, or whygame5 realizing its runner plan)
  needs an exception to D1 or a second record shape;
- `aes status` on either consumer disagrees between two clones at the same
  commit.

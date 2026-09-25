# AES v0.2 Greenfield MVP materialization candidate

Status: **accepted** by [Decision 0010](../../decisions/0010-greenfield-v0.2-accepted.md) (2026-09-25). Plain copy of `proposals/aes-v0.2-greenfield/13-greenfield-materialization.candidate.md` (copied, not `git mv`'d, so the proposal lineage stays in place). For AES canonical, `.aes/target.yaml` is the live authority: where this file and the target disagree, this file is wrong. "Accepted amendments" at the end lists what changed from the candidate. File names that are not in this directory refer to `proposals/aes-v0.2-greenfield/`.
Date: 2026-09-24

## Goal

Choose the smallest opinionated project storage convention that can materialize
the clean semantic model for a fresh project without making storage layout part
of the ontology.

This is deliberately Greenfield-MVP scoped.

## Control root

Use one project-local AES control root:

~~~text
.aes/
~~~

Rationale:

- unambiguous ownership by the AES distribution;
- does not compete with native source/test/contract roots;
- makes generated versus native project artifacts distinguishable;
- avoids inheriting the v0.1 .agentic naming merely for compatibility;
- allows a colleague to identify the AES control surface immediately.

The root name is `.aes/`, fixed by the accepted initialization contract
(`14-initialization-contract.yaml`) and written by `aes init`.

## Canonical files

~~~text
.aes/
├── project.yaml
├── target.yaml
├── analysis.yaml                 # not realized in the v0.2 MVP
├── plans/
│   └── <proposal_id>.yaml        # PLAN-<id>.yaml by convention; written by `aes plan accept`
├── observations/
│   └── <observation-id>.yaml     # written by `aes evidence record`, or by hand for external subjects
└── generated/                    # not realized in the v0.2 MVP: named in project.yaml, never written
    ├── current.yaml
    ├── gaps.yaml
    ├── semantic-graph.yaml
    └── ... concern-specific projections
~~~

Realized in the v0.2 MVP: `project.yaml`, `target.yaml`, `plans/` and
`observations/`. Outside `.aes/`, `aes hooks install` writes
`.githooks/pre-commit` and sets the repository-local `core.hooksPath` to
`.githooks`; the hook runs `aes target validate` and `aes topology check`.

Native implementation remains in the ecosystem's normal locations, for example
src/, tests/, package manifests, framework directories, contracts, migrations,
and deployment configuration as appropriate.

AES does not relocate native authorities into .aes merely for uniformity.

## .aes/project.yaml — operational adoption/configuration

Purpose:

- identify the project and AES architecture/distribution version (and, when
  written by `aes init`, when it was initialized);
- name the governed roots, the directories whose every file must be a planned
  artifact (D1);
- name the primary language or runtime, which selects the default test command
  of `aes evidence record`;
- locate the target, plans, observations and generated roots.

Not realized in the v0.2 MVP: enabled/supported ecosystem adapter profiles and
provider configuration references (the strict project record rejects both).

Must not become a dumping ground for:

- requirements;
- success criteria;
- accepted repository topology;
- provider-binding architecture decisions;
- current/gap state;
- secrets.

Candidate distinction:

~~~text
project.yaml
  how this repository uses the AES product

target.yaml
  what this project has accepted should be true
~~~

Environment secrets remain outside canonical project target records.

## .aes/target.yaml — canonical accepted target

Greenfield-MVP authority for:

- outcomes;
- normative items;
- success/disproof/evidence requirements;
- accepted realization units, as the `components` family (D3);
- accepted planned artifacts;
- selected planned symbol commitments, as `exports` on planned artifacts;
- accepted verification subjects;
- external boundaries: evidence requirements whose route is outside the
  repository, and who or what supplies the evidence.

Not realized in the v0.2 MVP: accepted capability requirements, accepted
provider bindings and accepted artifact-generation rules (every planned
artifact has an exact path). Record shapes: `16-record-shapes.yaml`.

This is one structured authority in the MVP to avoid premature partitioning and
duplicate joins.

The semantic items retain stable IDs so later architecture versions can partition
the physical storage without changing semantic identity.

### Why one target file first

Advantages:

- one atomic target snapshot;
- no cross-file synchronization protocol needed for the MVP;
- many-to-many semantic refs are local and mechanically resolvable;
- context/wiki projections mean humans/agents do not need to browse this whole
  file during ordinary implementation;
- target changes can be reviewed as one coherent semantic diff.

Risk:

- target.yaml can become large.

Disposition:

Accept that risk for the Greenfield MVP. Split only after measured scale/concurrent
editing pressure justifies a partitioning design.

## .aes/analysis.yaml — accepted engineering analysis

Not realized in the v0.2 MVP: no command writes this file and
`project.yaml` has no path for it. The candidate design follows.

Candidate authority for accepted non-target analysis needed by planning, initially:

- failure modes;
- material feasibility findings;
- explicit planning uncertainties that remain active;
- provider-landscape references/dispositions before provider binding is accepted.

Analysis may cause target changes but does not itself become target/current
conformance state.

Do not store broad research prose here. Retain source research in its natural
external/project research surface and reference it.

## .aes/plans/PLAN-<id>.yaml — accepted transitions

One plan file owns one accepted time-bounded transition.

Candidate contents:

- plan identity/status;
- origin gap refs;
- intended transition;
- proposed target changes;
- verticals/probes;
- planning uncertainty/stopping rules;
- execution boundaries;
- completion evidence requirements;
- provider selections proposed by this transition;
- plan dispositions/history refs as needed.

When a target change is accepted, target.yaml is updated atomically with the plan
acceptance/change. The plan remains transition history, not timeless target
authority.

Realized in the v0.2 MVP: a plan file is the accepted proposal
(`aes.v0_2.proposal.probe0`: `proposal_id`, `title`, `rationale`,
`closes_gaps`, a `target_delta` with `add:`, `change:` and `remove:` sections
per target family, optional `outside_governed_roots`) plus
`accepted_at_revision` (HEAD at acceptance) and `accepted_at` (UTC). Of the
candidate contents above, only identity, origin gap refs, the rationale for the
transition and the proposed target changes are realized; verticals, stopping
rules, execution boundaries, completion evidence requirements and provider
selections are not. `aes plan accept` edits target.yaml and writes the plan
file but does not commit; the two are committed together. It warns when HEAD
is not on the default branch, and `aes reconcile` / `aes status` report
`plans: N accepted, M unreachable` with a warning line per accepted plan whose
`accepted_at_revision` is not reachable from HEAD.

## .aes/observations/<observation-id>.yaml — revision-bound observations

Candidate append-only project evidence surface for AES-native observation
receipts.

Each observation records what actually ran/was attempted and its exact
subject/revision/provider/method/result/error.

This directory does not imply that large native tool artifacts must be copied
into YAML. An observation may reference an external/native retained artifact with
identity/digest.

Evidence assessments are retained inside the observation, one per evidence
requirement (never per criterion). Freshness (CURRENT, STALE, UNKNOWN,
UNREACHABLE) and criterion standing are computed from Git and the target on
every read, not stored. An observation whose commit is not reachable from HEAD
is UNREACHABLE and never counts. Records are never deleted: a replaced record
gains `superseded_by: <observation_id>` and no longer counts. Observations may
also carry entry-level `dependency_target_refs` and a negative-control block
(`control: {kind: negative, base_revision, ...}`); see `16-record-shapes.yaml`.

Observation IDs must be stable and unique; timestamp-only identity is not assumed.

## .aes/generated/ — rebuildable projections

Not realized in the v0.2 MVP. `project.yaml` names `generated_root`, but
nothing writes under it: `aes reconcile` and `aes status` compute current state
and gaps, `aes characterize` the realized characterization, and `aes context`
the working context, on every call, and print them. The candidate design
follows.

Never independent authority.

Candidate outputs:

- current.yaml;
- gaps.yaml;
- semantic-graph.yaml;
- subject/working context;
- human navigation/review views;
- conventional requirements/architecture views.

A generated projection must identify enough provenance/freshness information to
determine whether it is current.

Deleting and regenerating this directory must not destroy normative target,
accepted analysis, accepted plan history, native realization, or retained
observation evidence.

## YAML as the Greenfield-MVP canonical structured representation

Candidate choice: YAML for AES-authored structured project records.

Reasons:

- readable multiline normative prose;
- easy diff/review in Git;
- convenient typed validation;
- direct representation of IDs/refs/lists/mappings;
- usable by humans without requiring a database.

YAML is a representation choice, not the semantic model.

The implementation must reject dangerous ambiguity such as duplicate mapping
keys. Realized: strict Pydantic models (unknown fields rejected) over a YAML 1.2
loader that rejects duplicate keys, plus semantic checks for reference
resolution and evidence routes. There is no lenient mode.

## Native artifacts remain native

Examples:

- Python/TypeScript/Rust/etc. source remains native code;
- OpenAPI remains OpenAPI when it is the actual API contract;
- package manifests/lockfiles remain ecosystem-native;
- database migrations remain framework-native;
- tests remain the framework's normal test format.

AES target.yaml references and governs these where appropriate; it does not copy
their full semantics into an AES replacement format.

## Initialization contract

A fresh-project initializer should create only the minimum durable AES control
surface required before project-specific planning.

Candidate initial materialization:

~~~text
.aes/project.yaml
.aes/target.yaml
~~~

analysis.yaml, plan files, observations and generated projections appear only
when their semantic class exists.

The initializer may also create native project bootstrap artifacts only when the
chosen initialization workflow has already accepted their purpose/topology.

Do not create empty directories merely to advertise future capabilities.

Realized: `aes init --project-id ID --actor TEXT --outcome TEXT` writes exactly
these two files in one step, and no directories. It then prints the next step:
"next: aes plan prepare, write a proposal, aes plan validate/accept; or edit
.aes/target.yaml by hand, then aes target validate".

## Atomicity requirement

Changes that accept a new target topology must not leave target authority and
native realization in a misleading half-state.

Candidate transaction boundary for Git-based projects:

- target/plan changes;
- created/renamed/removed governed artifacts;
- affected verification topology;
- regenerated required projections/receipts as defined later;

are reviewed as one coherent change set.

Whether a single Git commit is always required remains open, but the resulting
accepted revision must be internally reconcilable.

Realized: `aes plan accept` refuses on a dirty tree and does not commit; the
target and plan are committed together, through the pre-commit hook. Removing a
governed planned artifact requires its file out of the Git index first, so a
removal lands as two commits (move or delete the file, then accept the
removal); in between the entry is only unrealized, which the hook allows.

## Source-local context is a projection, not another authority

The working context may eventually be delivered via:

- generated source region;
- sidecar;
- agent/IDE injection;
- hybrid.

Whichever mechanism is selected, it is generated from target/current/gap/plan
facts and contains full applicable semantic text with provenance.

Realized in the v0.2 MVP: none of the four. `aes context <subject>` compiles a
bounded packet for one declared id from the target's typed refs, with full
text and an explicit `not_included` list, and prints it; nothing is written.

Do not create another manually maintained source-local normative authority.

## Relationship graph remains generated

No relationships.yaml is part of this candidate layout.

semantic-graph.yaml (not realized in the v0.2 MVP) is generated from:

- typed target refs;
- plan refs;
- realized characterization;
- observation/evidence refs;
- derived impact/relevance relationships.

If later work proves a relationship has no natural owning fact, add the smallest
specific authored semantic type required rather than defaulting to a universal
edge registry.

## Explicit nonclaims

This candidate does not decide:

- the final .aes root name (since decided: `.aes/`);
- exact YAML schemas (since realized as the probe-0 record models in
  `16-record-shapes.yaml`);
- provider APIs;
- source characterization implementation;
- context delivery mechanism;
- observation/evidence file granularity at scale;
- signing/attestation format;
- retrofit layout;
- organization-level configuration.

## Accepted amendments

- "Candidate root" retitled "Control root" and the "root name remains candidate" sentence replaced: `.aes/` is realized (project.py `AES_DIR`, the accepted init contract).
- Canonical files tree: `analysis.yaml` and `generated/` marked not realized; plan files shown as `<proposal_id>.yaml`; a note names what is realized and adds `.githooks/pre-commit` / `core.hooksPath` from `aes hooks install` (hooks.py; 24 §11). Why: `ls .aes/` holds only project.yaml, target.yaml, plans/, observations/, and no code writes analysis or generated files.
- project.yaml purpose list: governed roots and primary language added; adapter profiles and provider configuration references marked not realized. Why: records.py `ProjectRecord` is strict and has exactly these fields (24 §12).
- target.yaml authority list: realization units -> `components`, symbol commitments -> `exports`, external boundaries added; capability requirements, provider bindings and generation rules marked not realized. Why: records.py `TargetRecord` (24 §1 D3, §13, §15).
- analysis.yaml marked not realized (no model, command or project.yaml path).
- Plans: realized plan file shape (proposal + `target_delta` add/change/remove + `accepted_at_revision` + `accepted_at`), which candidate contents are and are not realized, no-commit acceptance, the off-default-branch warning and `plans: N accepted, M unreachable` reporting. Why: planning.py `AcceptedPlan`, reconcile.py `PlanState`, cli.py (24 §15, §20 item 1; branch commit 26f8428).
- Observations: "assessments may be generated or retained ... later design" replaced by the realized choice (retained inside the observation, per evidence requirement), plus UNREACHABLE freshness, `superseded_by`, `dependency_target_refs` and negative controls. Why: evidence.py (24 §16, §19).
- `.aes/generated/` marked not realized; reconcile/status/characterize/context compute and print instead. Why: reconcile.py docstring ("nothing is written"), context.py.
- YAML section: "schemas/validators remain to be designed" replaced by the realized strict Pydantic + duplicate-key-rejecting loader. Why: records.py.
- Initialization section: realized `aes init` invocation and its next-step hint added. Why: project.py, cli.py `INIT_NEXT_STEP` (24 §12, §20 item 2).
- Atomicity section: realized acceptance transaction and the two-commit removal rule added. Why: planning.py; 24 §20 decision "removal of a governed artifact requires its file out of the index first".
- Source-local context: realized as `aes context <subject>` printed to stdout, none of the four delivery mechanisms. Why: context.py.
- Relationship graph: `semantic-graph.yaml` marked not realized.
- Explicit nonclaims: root name and exact YAML schemas marked as since decided/realized.
- Kept unchanged: the title's "candidate" wording and the date line, as lineage.

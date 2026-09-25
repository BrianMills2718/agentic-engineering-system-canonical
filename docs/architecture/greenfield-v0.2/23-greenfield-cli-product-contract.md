# AES v0.2 Greenfield CLI/product contract

Status: **accepted** by [Decision 0010](../../decisions/0010-greenfield-v0.2-accepted.md) (2026-09-25). Plain copy of `proposals/aes-v0.2-greenfield/23-greenfield-cli-product-contract.md` (copied, not `git mv`'d, so the proposal lineage stays in place). For AES canonical, `.aes/target.yaml` is the live authority: where this file and the target disagree, this file is wrong. "Accepted amendments" at the end lists what changed from the candidate. File names that are not in this directory refer to `proposals/aes-v0.2-greenfield/`.
Date: 2026-09-24

## Product principle

A colleague should not need to understand AES internals, provider repositories, or
historical governance systems to use the supported Greenfield lifecycle.

The CLI is a composition surface over AES capabilities. It does not own their
semantics.

Candidate executable:

~~~text
aes
~~~

**As realized in the v0.2 MVP** (`src/agentic_engineering_system/cli.py`,
`aes --help`), the commands are:

~~~text
aes init --project-id ID --actor TEXT --outcome TEXT [--governed-root R ...] [--language L] [--root DIR]
aes target validate [--root DIR]
aes context <subject> [--root DIR] [--format markdown|json]
aes topology check [--root DIR]
aes evidence status [--root DIR]
aes evidence record <VS-ID> [--depends-on PATH ...] [--command ...] [--inconclusive BASIS] [--root DIR]
aes hooks install [--root DIR]
aes characterize [--root DIR] [--json]
aes reconcile [--root DIR] [--json]
aes status [--root DIR]
aes plan prepare [--root DIR] [--out FILE]
aes plan validate <proposal> [--root DIR]
aes plan accept <proposal> [--root DIR]
aes --version
~~~

Without `--root`, every command except `init` uses the nearest directory at or
above the current one holding `.aes/project.yaml`. Exit codes: 0 on success;
1 on any load, validation, context or topology error, orphan, or drift, with
the message on stderr (`reconcile` and `status` also exit 1 on a REFUTED
criterion; INSUFFICIENT criteria and unreachable accepted plans do not fail
them); 2 on usage errors. Commands this contract proposes that are not in this
list are marked **not realized** below.

## 1. Initialize adoption

~~~text
aes init --project-id <id>
~~~

**MVP realization:** `aes init --project-id ID --actor TEXT --outcome TEXT
[--governed-root R ...] [--language L] [--root DIR]`. It writes exactly
`.aes/project.yaml` and `.aes/target.yaml`, the target holding the first
outcome (`OUT-001`) built from `--actor` and `--outcome`, so establishing the
first outcome is part of `init` rather than a following action; this replaces
the "do not create empty target" and "report the next required semantic
action: establish an outcome" effects below. It refuses outside a Git
repository, below the top of the work tree, and when `.aes/` already exists.
Governed roots default to `src/` and `tests/`. It prints what it wrote and
the next step (`aes plan prepare`, write a proposal, `aes plan
validate/accept`). It installs no hooks (that is `aes hooks install`) and
creates no other files.

Preconditions:

- current directory is a Git repository or the command is given an explicit
  project root;
- .aes/ does not already represent an incompatible adoption.

Effects:

- create .aes/project.yaml;
- do not create empty target/analysis/plan/observation/generated artifacts;
- report the next required semantic action: establish an outcome.

Must not:

- install private repositories;
- create CLAUDE.md/AGENTS.md/relationships.yaml/meta-process.yaml implicitly;
- install hooks without explicit opt-in;
- write credentials.

## 2. Establish/validate target

Candidate commands:

~~~text
aes target validate
aes target show
~~~

Target authoring may initially occur through direct YAML editing or an agent/human
planning interaction.

The CLI should not require a form wizard before the target schema is proven.

Validation includes:

- strict YAML parsing;
- structural typing;
- stable-ID uniqueness;
- typed-ref resolution;
- criterion/evidence requirements;
- topology/provider/verification invariants once present.

Exit non-zero on invalid canonical target.

**MVP realization:** `aes target validate` is realized: strict load (unknown
field, duplicate key or id, unresolved ref fail with their location), every
criterion has an evidence requirement, and every evidence requirement has a
route (a verification subject naming it or an `external_boundaries` entry);
exit 1 otherwise. Topology is checked by the separate `aes topology check`;
provider invariants are not realized (no provider bindings). `aes target
show` is **not realized**.

## 3. Materialize current/gaps before implementation

~~~text
aes reconcile
~~~

For a fresh target with no realization yet, output explicitly represents
unrealized current and open gaps.

Effects:

- produce/rebuild .aes/generated/current.yaml;
- produce/rebuild .aes/generated/gaps.yaml;
- retain provenance/input identities.

**MVP realization:** `aes reconcile [--json]` writes nothing: no
`.aes/generated/current.yaml` or `gaps.yaml` is produced. Every run recomputes
current and gaps from the target, the repository at HEAD and the observations,
and prints the report (every planned artifact REALIZED / UNREALIZED /
DRIFTED, every criterion's missing evidence requirements and the subjects
that could supply them, observation freshness, orphans, accepted plans, gaps
per component), or with `--json` one JSON document
(`aes.v0_2.reconciliation.probe0`) whose binding is `subject_revision` (HEAD)
and `dirty`. Gap ids are `<kind>:<ref>` with kinds drifted, refuted, orphan,
unrealized, insufficient. On a fresh target, unrealized artifacts and
insufficient criteria are listed as open gaps. Exit 1 on a REFUTED criterion,
an orphan or drift.

## 4. Prepare planning problem

~~~text
aes plan prepare [--gap <gap-id> ...]
~~~

Output:

- structured planning request;
- readable summary;
- request identity/digest;
- exact target/current/gap/analysis input identities;
- planning contract and output requirements.

Default behavior should select the smallest gap/concern set necessary rather than
dump all project state when the selected concern is known.

**MVP realization:** `aes plan prepare [--out FILE]`; `--gap` is **not
realized**, and there is no gap selection. It prints (or writes to FILE) one
YAML packet (`aes.v0_2.plan_input.probe0`): `target_id`, `subject_revision`
(HEAD), `dirty`, `governed_roots`, every open gap of the current
reconciliation with its id, unrouted evidence requirements, every declared id
by family, and an empty `proposal_skeleton`. There is no separate readable
summary, no request identity or digest, and no analysis inputs; the planning
protocol is `src/agentic_engineering_system/planning_protocol.md`. It writes
nothing in the repository unless `--out` names a path there.

## 5. Validate provider proposal

~~~text
aes plan validate <proposal>
~~~

Checks:

- proposal binds to the correct planning request;
- no unknown/unresolved refs are silently accepted;
- every proposed durable artifact has exact path or bounded generation rule;
- selected symbol commitments bind to planned artifacts;
- exercised criteria have concrete verification routes;
- load-bearing uncertainty is either resolved or represented by a probe/stopping
  rule;
- provider bindings expose semantic/replacement boundaries.

The command does not accept target changes automatically.

**MVP realization:** `aes plan validate <proposal>` applies the proposal
(`aes.v0_2.proposal.probe0`: `add`, `change`, `remove` sections over the
target families) to an in-memory copy of the target and lists every violation,
exit 1: delta keys (a `change` or `remove` of an absent key, an `add` of a
present one, a key in two sections, an empty delta); references the result
still holds to a removed entry; a removed governed planned artifact still in
the Git index; the strict target checks on the result; every evidence
requirement of the result without a route; a `closes_gaps` id not open now;
an added or changed planned artifact outside the governed roots that is
source or has no reason. Of the checks above, binding to a planning request,
bounded generation rules, planning uncertainty and provider bindings are **not
realized**; symbol commitments are bound structurally (`exports` on the
planned artifact). It writes nothing.

## 6. Accept planning result

Candidate command:

~~~text
aes plan accept <proposal>
~~~

This is a consequential mutation.

Minimum behavior:

1. verify proposal is still based on current planning inputs;
2. materialize the accepted target delta into .aes/target.yaml;
3. write the accepted transition plan under .aes/plans/;
4. validate resulting target;
5. recompute current/gaps;
6. report closing gaps and next execution boundary.

The exact human/authorization confirmation model remains open. The CLI must never
silently accept a stale proposal.

**MVP realization:** `aes plan accept <proposal>` refuses (exit 1, nothing
written) on uncommitted tracked changes or anything untracked under `.aes/`,
on any validation violation, and when `.aes/plans/<proposal_id>.yaml` exists.
Staleness is handled by re-validating against HEAD at accept time, not by
binding the proposal to a prepare packet. Otherwise it edits `.aes/target.yaml`
in place (comments and order kept), checks the result loads to exactly the
validated target, writes `.aes/plans/<proposal_id>.yaml` (the proposal plus
`accepted_at_revision` and `accepted_at`), and prints the changes and the next
step (`git add` target and plan, commit, implement). It does not commit and
does not recompute current/gaps (step 5 above is **not realized** in accept;
`aes reconcile`/`aes status` recompute on every run). It warns on stderr when
HEAD is not on the default branch (`origin/HEAD`, else `origin/main`), since a
squash merge would leave the plan's `accepted_at_revision` unreachable. There
is no confirmation prompt.

## 7. Check repository conformance

~~~text
aes check
aes check target
aes check topology
aes check evidence
~~~

aes check is the truthful aggregate local gate for AES-owned invariants.

It must be directly runnable.

Optional Git/CI/agent hooks invoke these commands; they do not replace them.

Topology findings distinguish at least:

- missing planned artifact;
- orphan governed artifact;
- generation-rule mismatch;
- selected symbol/signature/type mismatch;
- unresolved realized identity;
- intended/observed dependency mismatch when configured as consequential.

**MVP realization:** `aes check` and its subcommands are **not realized**.
The realized gates are `aes target validate`, `aes topology check` (exit 1 on
an orphan: a file in the Git index under a governed root with no planned
artifact at that exact path; an unrealized planned artifact is reported, not a
failure), `aes characterize` and `aes reconcile`/`aes status` (drift), and
the pre-commit hook written by `aes hooks install`, which runs `aes target
validate` and `aes topology check`. (AES canonical adds `make aes` over
validate, topology and status.) Of the topology findings above, missing
planned artifact (unrealized), orphan and selected symbol/signature mismatch
(`missing_export`, `signature_changed`, `missing_file` against `exports`) are
realized; generation-rule mismatch, unresolved realized identity and
dependency mismatch are **not realized**.

## 8. Characterize realized repository

~~~text
aes characterize
~~~

For the first Python/Git provider:

- bind exact Git revision;
- inventory governed/tracked artifacts;
- parse Python source statically;
- record symbols/signatures/types/docstrings/imports;
- preserve uncertainty/unsupported dynamic facts;
- compare selected planned identities where mechanically valid.

Output is generated observation/current substrate, not target authority.

**MVP realization:** `aes characterize [--json]` reads the HEAD tree (not the
working tree) under the governed roots: every file with blob hash and size,
and for Python files (AST only, never imported) the module name, top-level
public symbols with function signatures, intra-repository import edges and a
parse error if any. Docstrings are **not recorded**, and no uncertainty is
recorded beyond `parse_error`. It prints the report and drift against the
target's `exports` and topology, and writes nothing; exit 1 on drift.

## 9. Project working context

~~~text
aes context <subject>
aes context <subject> --format json
~~~

Subject forms remain to be frozen, likely stable semantic subject IDs with
path/symbol locators accepted as convenience resolution inputs.

Human-readable default includes:

- subject identity;
- full applicable normative text;
- full criterion/disproof text;
- provenance;
- current;
- gaps;
- active plan transition;
- verification obligations;
- relevant dependency consequences;
- explicit unresolved/omitted supporting context.

No required semantic atom is silently clipped to satisfy a context budget.

**MVP realization:** `aes context <subject> [--format markdown|json]`. The
subject is a declared id only (component, planned artifact, success
criterion, normative item or outcome); path and symbol locators are **not
realized**. The packet carries provenance, the subject, outcomes, normative
items, criteria with disproof and evidence requirements in full text,
components, planned artifacts, verification subjects, governed roots and the
topology rule, and lists every deliberately omitted id under "Not included".
Current state, gaps, the active plan transition and dependency consequences
are **not included** in the MVP packet (`aes status`/`aes reconcile` report
them).

## 10. Record observations

Candidate boundary:

~~~text
aes observe ...
~~~

Do not force every external test runner through an AES wrapper.

AES needs a way to retain observations from:

- deterministic commands/tests;
- runtime probes;
- human reviews;
- LLM rubrics;
- external consumer use.

The exact command grammar is deferred until observation schemas are stable.

A test command's exit code alone is not criterion satisfaction.

**MVP realization:** `aes observe` is **not realized**. Deterministic tests
are recorded with `aes evidence record <VS-ID> [--depends-on PATH ...]
[--command ...] [--inconclusive BASIS]`: it runs the verification subject's
test at HEAD (Python default: `pytest` on the locator), refuses while a
dependency or the target has uncommitted changes, and writes one observation
under `.aes/observations/` (`aes.v0_2.observation.probe0`) naming the commit,
command, result, dependency paths (the test, its discovered intra-repository
imports, each `--depends-on`) and `dependency_target_refs` (entry-level target
dependencies), with one assessment per evidence requirement. It warns on
stderr when HEAD is not on the default branch. Runtime, human, LLM-rubric and
external-consumer observations are hand-written in the same record shape; a
negative control carries `control: {kind: negative, base_revision, ...}`, and
a replaced observation is kept with `superseded_by`.

## 11. Assess/reconcile evidence

Candidate commands:

~~~text
aes evidence assess
aes reconcile
~~~

evidence assess:

- finds criterion evidence requirements;
- evaluates available observations;
- computes freshness/adequacy/standing with assessor provenance.

reconcile:

- combines target, realized characterization and evidence assessments;
- rebuilds current/gap;
- never uses plan-complete status as closure evidence.

These may later be combined operationally if that improves UX without collapsing
their semantics.

**MVP realization:** `aes evidence assess` is **not realized**; the realized
command is `aes evidence status`: per observation freshness CURRENT, STALE,
UNKNOWN or UNREACHABLE (superseded observations counted apart and never
used), and per criterion standing SUPPORTED, INSUFFICIENT or REFUTED under
conjunction (every evidence requirement needs a CURRENT supporting
assessment; any CURRENT refuting one refutes). Assessments are written by the
observation's producer inside the observation, not recomputed by an assessor.
`aes reconcile` combines characterization, evidence standing and accepted
plans as in section 3; it stores nothing.

## 12. Inspect state

~~~text
aes status
~~~

Compact output should answer:

- What outcome are we pursuing?
- What is current?
- What gaps remain?
- What plan is active?
- What evidence is stale/insufficient?
- What is the next governed action?

It is a projection, not another authority.

**MVP realization:** `aes status` prints one screen: the target id and HEAD;
artifacts realized / unrealized / drifted and orphans; criteria supported /
insufficient / refuted and evidence requirements with no route; observations
current / stale / unknown / unreachable and superseded; `plans: N accepted, M
unreachable`; the first open gap per component; a warning line per accepted
plan whose `accepted_at_revision` is not reachable from HEAD. It does not name
the outcome or an "active" plan (plans are counted, not tracked as active)
and does not suggest a next action. Exit 1 on a REFUTED criterion, an orphan
or drift; INSUFFICIENT criteria and unreachable plans do not fail it.

## 12a. Human review surface (candidate, added 2026-09-25)

~~~text
aes review [--decision <file>]
~~~

Writes `.aes/generated/review.html`: a self-contained page a person opens
with `file://` to judge the accepted target and its realization without
reading YAML. Pending decision first, then intent, rules, proof coverage with
existence marks, file map, orphans. Derived, never authority. See open
question 22. Temporary renderer: AES `scripts/probe/render_review.py`.

**MVP realization:** `aes review` is **not realized** as a CLI command; only
the probe script exists.

## 13. Optional adapters

Not required for core MVP:

~~~text
aes install-hook git
aes adapter install <agent/client>
~~~

Any adapter must call the same core commands/models rather than reimplement AES
rules.

**MVP realization:** the Git hook is realized as `aes hooks install` (not
`aes install-hook git`): it writes `.githooks/pre-commit`, which runs `aes
target validate` and `aes topology check`, and sets the local
`core.hooksPath=.githooks` (noting when that overrides a global setting). It
is opt-in, run after `aes init`. `aes adapter install` is **not realized**.

## Greenfield happy path

~~~text
git init my-project
cd my-project

install AES distribution

aes init --project-id my-project
# establish first accepted target outcome
aes target validate
aes reconcile

aes plan prepare
# human/agent produces proposal
aes plan validate proposal.yaml
aes plan accept proposal.yaml

# implementation
aes check
aes characterize
# run/record required observations
aes evidence assess
aes reconcile

aes status
~~~

At any implementation step:

~~~text
aes context <subject>
~~~

provides the bounded working surface.

**MVP realization:** the happy path as built and run end to end in
`docs/greenfield/GETTING_STARTED.md` (which is the user-facing authority for
the exact steps):

~~~text
git init my-project && cd my-project
pip install "agentic-engineering-system @ git+https://github.com/BrianMills2718/agentic-engineering-system-canonical.git@<sha>"

aes init --project-id my-project --actor "<who>" --outcome "<first outcome>"
aes hooks install
git add .aes .githooks && git commit        # hook: aes target validate + aes topology check

aes plan prepare
# human/agent writes proposal.yaml (see planning_protocol.md)
aes plan validate proposal.yaml
aes plan accept proposal.yaml
git add .aes && git commit                  # target and plan together

# implementation: write the planned files, commit (hook checks every commit)
aes evidence record <VS-ID> [--depends-on PATH]
aes evidence status
git add .aes/observations && git commit

aes status                                   # or aes reconcile [--json]
~~~

`aes check`, `aes evidence assess` and an explicit `aes reconcile` step before
planning are not part of the realized path (`aes check` and `aes evidence
assess` are not realized; `aes plan prepare` reconciles internally).
`aes characterize` is available but not a required step.

## Error design

Errors must be actionable.

A hard failure should identify:

- violated invariant;
- exact subject/file/ref;
- current evidence/input identity;
- recovery class:
  - fix implementation;
  - amend target;
  - replan;
  - rerun observation;
  - resolve uncertainty;
  - refresh stale planning/context input.

Do not emit "policy failed" without a runnable next route.

**MVP realization:** errors print `error: <subject>: <n> violation(s):`
followed by every violation (not the first) with its file, id or location, on
stderr, exit 1; usage errors exit 2. The recovery class is **not emitted** as
a field; some messages name the recovery in text (e.g. "commit or remove these
first", "run `aes init` there", "merge with a merge commit (not squash), or
re-record").

## CLI nonclaims

This candidate does not yet freeze:

- argument spelling;
- target-authoring UX;
- interactive TUI;
- automatic LLM API integration;
- Git hook installation behavior;
- CI provider;
- observation command grammar;
- deployment/operations workflows.

**MVP realization:** for the realized commands the v0.2 MVP does fix argument
spelling (as listed at the top), Git hook installation behavior (`aes hooks
install`) and the observation grammar for deterministic tests (`aes evidence
record`); they are defined by `cli.py` and `docs/greenfield/GETTING_STARTED.md`.
Target authoring is a validated proposal (`aes plan`) or a hand edit checked
by `aes target validate`. No TUI, LLM API integration, CI provider or
deployment workflow is realized.

## Accepted amendments

Each "MVP realization" paragraph above is an amendment; the candidate text is
kept and what was not built is marked **not realized**. Verified against
`cli.py`, `aes --help` and subcommand `--help` run from this worktree, and the
modules named.

- Added the realized command list, root discovery and exit codes (0/1/2) after "Candidate executable"; source: `cli.py` module docstring and `_build_parser`.
- §1: `aes init` requires `--actor` and `--outcome`, writes `.aes/project.yaml` and `.aes/target.yaml` with `OUT-001`, refuses outside Git / below the top / when `.aes/` exists; this contradicts the candidate's "no target, next action: establish an outcome"; source: `project.py` `initialize_project`, 24 §12.
- §2: `aes target validate` realized with the route rule; `aes target show` not realized; source: `cli.py` `_cmd_target_validate`, `planning.py` `route_violations`.
- §3: `aes reconcile` writes no `.aes/generated/current.yaml`/`gaps.yaml`; recomputed every run, `--json`, gap ids and kinds, exit codes; source: `reconcile.py` module docstring, 24 §14.
- §4: `aes plan prepare [--out FILE]`; `--gap`, digest and summary not realized; packet contents; source: `planning.py` `prepare`, 24 §15.
- §5: realized validation checks incl. `remove:`; request binding, generation rules, uncertainty, provider bindings not realized; source: `planning.py` module docstring, 24 §15 and §20 item 1.
- §6: `aes plan accept` refusals, in-place edit, plan file shape, no commit, no recompute, default-branch warning; source: `planning.py` `accept_proposal`, `cli.py`, `evidence.py` `branch_note`, commit 26f8428 (this branch).
- §7: `aes check` (and subcommands) not realized; realized gates and which topology findings exist; source: `topology.py`, `characterize.py` `drift`, `hooks.py`.
- §8: `aes characterize` facts; docstrings not recorded; writes nothing; source: `characterize.py`, `characterize_python.py`.
- §9: `aes context` takes declared ids only; current, gaps, plan and dependency consequences not in the packet; source: `context.py`.
- §10: `aes observe` not realized; `aes evidence record` grammar, hand-written external observations, negative controls, `superseded_by`, `dependency_target_refs`; source: `cli.py`, `evidence.py`, 24 §10, §16, §19.
- §11: `aes evidence assess` not realized; `aes evidence status` freshness (incl. UNREACHABLE) and SUPPORTED/INSUFFICIENT/REFUTED standing; source: `evidence.py` module docstring, 24 §9, §19.
- §12: `aes status` output as built, including `plans: N accepted, M unreachable` and the unreachable-plan warning; no outcome, active plan or next action shown; source: `reconcile.py` `render_status`, `aes status` run in this worktree at ef6fc25.
- §12a: `aes review` not realized as a command; source: `aes --help`.
- §13: hook realized as `aes hooks install`; `aes adapter install` not realized; source: `hooks.py`.
- Happy path: added the realized path per `docs/greenfield/GETTING_STARTED.md`; source: that file, 24 §15.
- Error design: error format and exit codes; recovery class not emitted; source: `cli.py`, `planning.py` `PlanError`.
- CLI nonclaims: noted which of them the MVP now fixes for realized commands; source: `cli.py`.

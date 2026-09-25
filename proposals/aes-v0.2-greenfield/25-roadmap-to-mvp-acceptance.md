# AES v0.2 roadmap: from probe 0 to MVP acceptance

Status: proposal, non-normative. Written 2026-09-25 after sections 6–10 of
`24-pre-probe-decisions.md`. This is the sequenced plan the earlier files did
not contain: `20-realization-topology` lists ten units, `12-…-semantic-instance`
lists nine acceptance criteria, and §3 of `24` sequenced only probe 0.

Operating rule (Brian, 2026-09-25): AES canonical is the goal; `whygame5` is a
method for finding AES's kinks. Every phase below ends in a recorded observation
on a real consumer, or it is not a phase.

Execution model: this roadmap is planned and reviewed by one orchestrating
session; each phase is built by one implementing agent in its own claimed
linked worktree, delivered as a PR with tests, and merged only after the
orchestrator has run the tests and at least one real consumer command itself.

## 0. Where we stand

"Done" for v0.2 MVP means: all nine criteria SC-GF-001..009 stand SUPPORTED
under AES's own evidence rules (D2: every evidence requirement has a CURRENT
observation that SUPPORTS it) on a consumer AES governed from its first commit,
and AES v0.2 replaces v0.1 as the surface AES canonical itself is governed by.

| criterion | what proves it | standing today | unit |
| --- | --- | --- | --- |
| SC-GF-001 clean-user install + init | a clean-user run reaches initialized state | mechanism realized; on-machine clean-user run passed at `0503735` (`evidence/greenfield/clean-user-run-2026-09-25.md`); true no-private-access run deferred by decision (§6 note); on AES's own `aes status` (phase 6b, §17 of `24`) that run is `OBS-AES-CLEAN-USER-0503735`, SUPPORTS but STALE because the files it exercised changed since `0503735`: needs a re-run on current code | PROJECT, DISTRIBUTION |
| SC-GF-002 obligations linked to criteria and evidence | contract validation on the target | SUPPORTED on AES canonical (`OBS-GF-RECORDS-cb226ba7`, phase 6b) | RECORDS |
| SC-GF-003 topology accounts for every governed artifact | orphan rejected; planned topology accepted | mechanism realized (`topology.py`); real orphan caught on whygame5 (§6, §8); SUPPORTED on AES canonical, whose own 45 governed files (18 of them retained v0.1) are all planned (`OBS-GF-TOPOLOGY-cb226ba7`, `OBS-GF-SELF-GOVERNANCE-cb226ba7`) | TOPOLOGY |
| SC-GF-004 every evidence requirement has a route | validate ERs against verification topology | mechanism realized: `aes plan validate`/`accept` refuse a proposal whose resulting target has an ER with neither a verification subject nor an external boundary (`planning.py`, `test_planning.py`, §15); `PLAN-WG5-RUNNER` accepted on whygame5 itself (`36b64ed`); AES canonical's own target built through `aes plan accept PLAN-AES-SELF-GOVERN` and SUPPORTED there (phase 6b); `aes target validate` (and so the `aes hooks install` pre-commit hook) enforces routes on the whole target since phase 6a (§16), effective on whygame5 after its next pin bump | PLANNING |
| SC-GF-005 bounded context carries full text | ER-01 deterministic; ER-02 fresh-agent A/B | ER-01 SUPPORTED on AES canonical (`OBS-GF-CONTEXT-STRUCTURAL-cb226ba7`); ER-02 inconclusive at probe 0 (§6), recorded on AES as `OBS-AES-PROBE0-CONTEXT-AB`; the phase 6 re-run is the orchestrator's | CONTEXT |
| SC-GF-006 revision-bound characterization + drift | mutate an artifact and see the mismatch; every fact bound to revision | mechanism realized (`characterize.py`, `aes characterize`); drift caught on a whygame5 scratch clone (§13), recorded on whygame5 (`OBS-WG5-DRIFT-b0c3e24f`); SUPPORTED on AES canonical, whose `exports` on eleven modules characterize with 0 drift | CHARACTERIZE |
| SC-GF-007 a pass is not satisfaction | multi-input criterion stays INSUFFICIENT | SUPPORTED on AES canonical (`test_evidence.py`, `test_evidence_controls.py`, `test_reconcile.py` recorded at `cb226ba`) | EVIDENCE |
| SC-GF-008 dependency change stales evidence | change a dependency, evidence goes STALE | realized at the evidence level and at the gap level (`aes reconcile`/`aes status`, `test_reconcile.py`, §14); SUPPORTED on AES canonical (phase 6b) | EVIDENCE, RECONCILE |
| SC-GF-009 one complete lifecycle on a new consumer | retained init/target/plan/realization/evidence/current/context at exact revisions | in progress on whygame5 (`OBS-AES-WG5-LIFECYCLE`, INCONCLUSIVE at `d5f993f`): init, target history, `PLAN-WG5-RUNNER`, 15 observations and status retained; missing the runner's realization and a context evaluation that distinguishes anything | all |

Realized units: RECORDS, CONTEXT, TOPOLOGY, EVIDENCE, and the CLI for those
four. Not realized: PROJECT, PLANNING, CHARACTERIZE, RECONCILE, DISTRIBUTION.
(Update 2026-09-25: DISTRIBUTION realized by phase 1, PROJECT by phase 2 and
CHARACTERIZE by phase 3, RECONCILE by phase 4, PLANNING (prepare, validate,
accept; no plan generation) by phase 5; see §11-§15 of
`24-pre-probe-decisions.md`. Update after phase 6b: all ten units realized and
AES canonical governed by its own `.aes/` target; `aes status` there: 6 of 9
criteria SUPPORTED, SC-GF-001/005/009 waiting on external runs, §17.)

Kinks the consumer has already exposed and that this roadmap must close:

- ~~the AES version never changes (`0.1.0` across every commit), so a pin bump
  does not reinstall and the consumer silently runs old code;~~ closed by
  phase 1 (Git-derived version, §11);
- ~~the consumer's pre-commit hook was hand-copied and broke in linked
  worktrees;~~ closed by phase 1 (`aes hooks install`, §11);
- ~~`dependency_paths` on an observation are declared by hand, not
  discovered~~ (closed by phase 3: discovered from imports, declared paths
  added, §13);
- ~~the producer version is the installed distribution's, so a worktree run
  names the main checkout's install (§13)~~ closed by phase 6a: the running
  checkout's `git describe` is appended (§16);
- ~~an observation that lists `.aes/target.yaml` goes STALE on any target edit,
  so accepting a plan or adding a requirement re-opens unrelated evidence
  (§14, §15 item 2)~~ closed by phase 6a: `dependency_target_refs` compares
  the referenced entries only; the file-level form remains as the coarse
  option (§16);
- ~~a "break it on purpose" observation is stale by construction because its
  subject is a mutated scratch commit (§14 item 2)~~ closed by phase 6a:
  `control: {kind: negative, base_revision, ...}` computes freshness from the
  unmodified base, and a missed mutation must REFUTE (§16);
- ~~AES canonical does not follow its own planning (its v0.2 code is not under
  a `.aes/` target of its own).~~ closed by phase 6b (§17): `.aes/` target,
  plan, observations and pre-commit hook of its own;
- `aes status` reports an externally bounded, unsupported requirement as "no
  route" (`reconcile._criterion_states` ignores `external_boundaries`), found
  by phase 6b (§17 item 2).

## 1. Sequencing principle

Build the unit the consumer forces next, not the next unit in the topology
list. Two constraints fix the order below:

1. **Distribution before anything else.** Every later phase is installed into
   the consumer. Until the version changes per commit and the hook ships with
   the package, each phase re-pays the "stale install" and "hand-copied hook"
   costs, and SC-GF-001 cannot even be attempted.
2. **Characterize before reconcile before plan.** Reconcile needs a realized
   description to compare against the target; planning acceptance needs
   reconcile to show the gap a plan claims to close. Building planning first
   would produce an acceptance transaction with nothing to check.

The context A/B (SC-GF-005 ER-02) is not a phase; it is re-run when a consumer
is large enough for whole-repository orientation to cost something, which the
roadmap arranges by making AES canonical its own second consumer in phase 6.

## 2. Phases

Each phase lists: what it moves, the deliverable, the proof (the observation
that gets recorded), the exit gate, and the condition under which the phase
was the wrong call. Sizes are relative to `evidence.py` + its tests (one
session, ~600 lines), the last unit built.

### Phase 1 — DISTRIBUTION: a version that moves, and a hook that ships

Moves: SC-GF-001 (prerequisite), kinks 1 and 2 above.

Deliverable:

- version derived from Git at build time (`setuptools-scm` or equivalent):
  `aes --version` prints a version that differs between any two commits, and
  a git-pinned install of a new commit reinstalls without `--force-reinstall`;
- `aes hooks install`: writes the pre-commit hook (target validate + topology
  check) into the consumer's `.githooks/` and sets `core.hooksPath`, with the
  worktree-safe interpreter lookup that whygame5 currently carries by hand;
- `tests/greenfield/test_distribution.py`: clean install into a temporary venv
  from the repository checkout, `aes --version`, `aes hooks install` into a
  temporary git repo, and a commit that the installed hook blocks.

Proof: whygame5 deletes its hand-copied hook, runs `aes hooks install`, bumps
the pin, and records the install observation against `VS` for SC-WG5's AES
gate. On the AES side, `.aes/observations/` does not exist yet (phase 6), so
the deterministic test is the evidence for now.

Exit gate: whygame5 `make check` passes with the packaged hook and no
hand-copied hook file in its tree.

Wrong when: a consumer still needs a hand-maintained hook or a
`--force-reinstall` after this phase, or the version scheme breaks
`pip install git+…@<sha>` (the consumer's pin form).

Size: ~0.7.

### Phase 2 — PROJECT: `aes init`

Moves: SC-GF-001 ER-01, SC-GF-009 (the "initialization" element).

Deliverable, per `14-initialization-contract.candidate.yaml`:

- `project.py`: `aes init --project-id <id>` in a git repository writes
  `.aes/project.yaml` (project id, governed roots, schema version, AES
  version that initialized it) and a minimal `.aes/target.yaml` holding one
  outcome placeholder-free skeleton that `aes target validate` accepts;
  refuses to run outside a git repository, on an already-initialized project,
  or when it would have to create any artifact the contract lists under
  `deferred_artifacts`;
- project discovery (`find_project_root`) used by every other command, so
  `aes` commands work from subdirectories and worktrees;
- `tests/greenfield/test_project.py`.

Proof: a **clean-user run** (ER-SC-GF-001-01 is an external observation, not a
test): a fresh agent session with no access to `~/code`, given only the
install line and the getting-started page, initializes a new throwaway
project and runs `aes target validate`, `aes topology check`,
`aes evidence status`. The transcript, exact AES revision and result are
recorded as an observation in AES canonical's own `.aes/observations/`
(created in phase 6; until then, retained under `evidence/` and moved then).

Exit gate: the clean-user run reaches initialized state without any file
copied from a private repository.

Decision (Brian, 2026-09-25): the AES repository stays private until AES has
shown it provides value, so ER-SC-GF-001-01's evidence of record is the
on-machine run above (fresh agent, page only, maintainer's credentials), and
the true no-private-access run is deferred. Wrong when: a consumer other than
whygame5 or AES itself needs to install AES; that is the trigger to make the
distribution reachable and re-run the probe.

Wrong when: the fresh agent has to read AES source, this proposals directory,
or whygame5 to complete initialization.

Size: ~0.6.

### Phase 3 — CHARACTERIZE: what the repository actually contains

Moves: SC-GF-006 ER-01 and ER-02; kink 3 (dependency discovery).

Deliverable, per `RU-AES-CHARACTERIZE`:

- `characterize.py`: at an exact revision, list every tracked file under the
  governed roots with blob hash, and bind the result to
  `subject_revision` + producer identity (`aes` version) — the same fields
  observations already carry;
- `characterize_python.py`: for Python files, the module name, top-level
  public symbols with signatures, and the intra-repository import graph;
  no execution or import of consumer code (AST only);
- target extension: optional `symbol_commitments` on a `planned_artifacts`
  entry (`exports: [name, …]`); drift = a committed symbol missing or with a
  changed signature;
- `aes evidence record` uses the import graph to **discover**
  `dependency_paths` for a `deterministic_test` subject (closure of the test
  module's intra-repo imports), with `--depends-on` becoming an addition,
  not the whole list;
- `tests/greenfield/test_characterize.py`.

Proof on whygame5: add one `exports:` commitment to `ART` for
`src/whygame5/ontology.py`, rename the symbol in a scratch commit, and record
the mismatch observation (ER-SC-GF-006-01); record a normal run for ER-02.

Exit gate: `aes characterize` output for whygame5 at its head is byte-stable
across two runs and names the revision and producer.

Wrong when: characterization needs to import consumer code, or the
discovered dependency set for whygame5's existing observations differs from
the hand-declared set in a way that makes previously CURRENT evidence STALE
for no real reason (that would mean the discovery is over-broad; fix before
merging, do not widen freshness rules).

Size: ~1.2.

### Phase 4 — RECONCILE: current state and gaps, and `aes status`

Moves: SC-GF-008 (the "current/gap state" clause), SC-GF-007 at the gap
level, SC-GF-009 (the "current/gap" element).

Deliverable, per `RU-AES-RECONCILE`:

- `reconcile.py`: composes topology (orphans, unrealized planned artifacts),
  characterization (drift) and evidence standing into one qualified current
  state: per planned artifact REALIZED | UNREALIZED | DRIFTED; per criterion
  SUPPORTED | INSUFFICIENT | REFUTED with the missing evidence requirements
  named; per component the set of open gaps;
- gap records are derived, never stored as authority (recomputed from target
  + repository + observations each time);
- `aes reconcile` (full report) and `aes status` (one screen: counts plus the
  first open gap per component), both exit non-zero on any REFUTED criterion
  or orphan;
- `tests/greenfield/test_reconcile.py` including: a supported criterion whose
  dependency then changes shows as a re-opened gap (SC-GF-008 at this level).

Proof on whygame5: `aes reconcile` at head lists exactly the gaps the
consumer knows it has (SC-WG5-001/005/006 insufficient); recorded as an
observation.

Exit gate: `make check` in whygame5 runs `aes status` instead of the three
separate commands and the result is identical.

Wrong when: reconcile needs its own stored state to answer, or a gap can be
closed by anything other than a new observation or target change.

Size: ~1.0.

### Phase 5 — PLANNING: proposals that map evidence to verification

Moves: SC-GF-004 ER-01, SC-GF-009 (the "plan" element).

Deliverable, bounded to the acceptance transaction in
`15-planning-contract.candidate.yaml` (no LLM provider, no plan generation):

- `plan.py` (`planning.py` in the topology; the v0.1 placeholder directory
  `planning/` holds no code and is dispositioned in phase 7 — keep the
  planned name, the module wins over the empty directory on import):
  a proposal file is a target delta (new/changed outcomes, normative items,
  criteria, components, planned artifacts, verification subjects) plus the
  gap ids it claims to close;
- `aes plan validate <proposal>`: strict load; every new criterion has
  evidence requirements; every evidence requirement in the resulting target
  maps to a verification subject or an explicit `external_boundary`;
  every claimed gap exists in the current reconcile output;
- `aes plan accept <proposal>`: applies the delta to `.aes/target.yaml`
  through ruamel (comments preserved), writes the accepted proposal under
  `.aes/plans/<id>.yaml` with the revision it was accepted at, and refuses
  if the working tree is dirty;
- `aes plan prepare`: emits the reconcile gap list and the target's existing
  ids as the input packet a human or agent writes a proposal against;
- `tests/greenfield/test_planning.py`.

Proof on whygame5: whygame5's next real change (its `SC-WG5-001` runner or
report) is planned through `aes plan prepare → validate → accept` before
implementation; the accepted plan file and the resulting commits are the
observation for ER-SC-GF-004-01.

Exit gate: the whygame5 pre-commit hook additionally rejects a commit that
adds a planned artifact whose criterion has no verification route.
(Update 2026-09-25, phase 6a, §16 of `24-pre-probe-decisions.md`: built in AES.
`aes target validate`, which the hook written by `aes hooks install` runs,
now fails on any evidence requirement of the whole current target that has
no verification subject or external boundary, listing each; tested with the
hook refusing such a commit. whygame5 passes (0 unrouted). The gate is met on
the consumer once whygame5 bumps its pin to include it.)

Wrong when: a proposal for a real change cannot be expressed without
editing the target by hand afterwards, or acceptance needs more than the
delta and the gap ids.

Size: ~1.2.

### Phase 6 — AES canonical governs itself (second consumer, larger A/B)

Moves: SC-GF-005 ER-02 (re-run with power), SC-GF-009's "genuinely new
consumer" is whygame5, but AES itself is the consumer that makes the tooling
credible; the last open kink in §0 (AES does not follow its own planning).

Preceded by phase 6a (2026-09-25, §16 of `24-pre-probe-decisions.md`): the
evidence-model fixes AES needs before it records evidence about itself
(entry-level target dependencies, negative-control observations, producer
version from the running code) and phase 5's route gate in
`aes target validate`.

Deliverable:

- `aes init` on AES canonical with governed roots
  `src/agentic_engineering_system/` (v0.2 modules only, by exact path; the
  v0.1 subpackages are listed as accepted historical artifacts pending phase
  7's disposition) and `tests/greenfield/`;
- target: the nine SC-GF criteria and their ERs copied from
  `12-…-semantic-instance` into `.aes/target.yaml` as the live authority, with
  verification subjects for every deterministic ER pointing at the real test
  files; observations for phases 1–5 recorded with `aes evidence record`;
- AES's own pre-commit hook via `aes hooks install`;
- re-run the probe-0 A/B on one real AES change (arm B in a separate session
  with no access to this conversation or the proposals directory), scored on
  the same sheet as `OBS-PROBE0-CONTEXT-AB.yaml`.

Independent of project-meta #2171: that issue blocks `make
maintenance-worktree` (authority runtime snapshot), not `.aes/` governance.

Exit gate: `aes status` on AES canonical shows SC-GF-002/003/005(ER-01)/
007/008 SUPPORTED from recorded observations, and the A/B has a recorded
verdict either way.

Wrong when: governing AES with AES needs an exception to D1 (governed roots)
or a second record shape; or the A/B is still indistinguishable at this
size, which then means SC-GF-005 ER-02 should be re-scoped, not re-run again.

Size: ~1.0, mostly target authoring and two probe runs.

### Phase 7 — Acceptance and promotion

Moves: SC-GF-009 ER-01; closes the v0.2 proposal lineage.

Deliverable:

- whygame5's full lifecycle retained at exact revisions: init commit, target
  history, accepted plans, realization commits, observations, reconcile
  output, and the context evaluation — listed in one observation record;
- `aes status` SUPPORTED on all nine criteria in AES canonical, with the
  external observations (SC-GF-001, SC-GF-005 ER-02, SC-GF-009) recorded
  from the retained transcripts;
- promotion: `proposals/aes-v0.2-greenfield/*.candidate.*` become accepted
  under `docs/architecture/` with stable ids; `README.md`, `CLAUDE.md` and
  `wiki/index.md` route to v0.2; the v0.1 subpackages under
  `src/agentic_engineering_system/` that the topology does not list are
  archived (moved under `archive/` with history, never deleted) with a
  disposition each; `docs/decisions/` gets the acceptance record with the
  wrong-when conditions from this file.

Exit gate: a fresh agent reading only `README.md` reaches the getting-started
page and the happy path in `23-…-cli-product-contract.md §Greenfield happy
path` runs end to end on a throwaway project.

Wrong when: acceptance needs any criterion downgraded to "documented instead
of observed", or promotion changes semantics rather than location.

Size: ~1.0.

## 3. Order, dependencies, and what can run in parallel

```
1 DISTRIBUTION ──► 2 PROJECT ──────────────────┐
        │                                      │
        └────────► 3 CHARACTERIZE ─► 4 RECONCILE ─► 5 PLANNING ─► 6 SELF-GOVERN ─► 7 ACCEPT
```

Phases 2 and 3 are independent and can run as two implementing agents at
once, in separate worktrees, after phase 1 merges. Everything else is serial:
each later unit consumes the previous one's output shape.

Expected total: about seven implementing sessions plus two probe sessions
(the clean-user run in phase 2 and arm B in phase 6, each run by an agent
with no access to this conversation).

## 4. Rules for every phase

- One claimed linked worktree per phase; PR into `main`; the orchestrator
  runs `python -m pytest -q tests/greenfield` and one real command on
  whygame5 before merging; lanes closed through `session_close.py`.
- The consumer pin in `whygame5/pyproject.toml` is bumped in the same day
  as each merge, and the consumer's `make check` is the smoke test.
- Every new module has a planned-artifact entry already in
  `20-realization-topology.candidate.yaml`; if a phase needs a file that is
  not listed there, the topology file changes in the same PR with a reason.
- Every phase appends a dated section to `24-pre-probe-decisions.md` in the
  style of §6–§10: what was realized, what the consumer exposed, and the
  wrong-when for any decision taken.
- No new architecture document in this lineage before phase 7, other than
  this roadmap's own status table being kept current.

## 5. Wrong-when for this roadmap

This ordering was the wrong call if any of the following is observed:

- phase 1 takes more than one session because Git-derived versioning fights
  the consumer's `git+https://…@<sha>` pin form (then: pin by tag instead,
  and record the change in §24);
- phase 3's discovered dependencies make whygame5's existing CURRENT
  evidence STALE without a real change (then: discovery is over-broad; the
  hand-declared list stays primary);
- two consecutive phases end without a recorded observation on a consumer
  (then: the phase boundaries are wrong, re-cut them around observations);
- **fired 2026-09-25 (§18 of `24`):** the phase-6 A/B is still indistinguishable (then: SC-GF-005 ER-02 is
  re-scoped to a different measure before any further context work).

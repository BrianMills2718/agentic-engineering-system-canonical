# AES v0.2 pre-probe decisions and independent review record

Status: **accepted pre-probe decisions / non-normative until v0.2 cutover**
Date: 2026-09-25
Review basis: `REVIEW.md`, all primary candidate files, `docs/decisions/0001`–`0009`
Reviewer: independent agent session (Claude Fable 5.1), first read not authored
by the proposal's author session. Brian approved the consumer-selection rule
(option A below) in conversation on 2026-09-25.

## Review verdict

**Accept for bounded implementation probing**, conditional on the decisions in
this file and on the build order in section 3. The architecture is coherent.
The material risk is not in the design; it is that this is the second full
architecture in nine days with no consumer, and the one claim that justifies
AES's existence (SC-GF-005/SC-GF-008: bounded projected context helps a fresh
agent on a real change) was scheduled after ten realization units.

Independent re-run of the cross-file reference check over
`12-greenfield-mvp-semantic-instance.candidate.yaml` and
`20-realization-topology.candidate.yaml` (own script, PyYAML `safe_load`,
ID pattern `^(OUT|GF-REQ|SC|ER|FM|FMR|CAP|PB|RU|ART|SYM|VS)-`):

| measure | this review | PR body |
| --- | --- | --- |
| declared IDs | 110 (122 when the 12 `PB-*` IDs in file 21 are included) | 122 |
| typed refs | 216 (counting method differs) | 188 |
| unresolved refs | 0 | 0 |
| duplicate IDs | 0 | 0 |
| exact paths / duplicates | 23 / 0 | 23 / 0 |

The zeros hold independently. The counts are not architecture evidence.

## 1. Decisions taken now (high-confidence, reversible)

### D1. "Governed" is a declared namespace, not every tracked file

The no-orphan rule (`SC-GF-003`, thesis §6) applies only to files under
governed roots declared in `.aes/project.yaml`, for example:

```yaml
governed_roots:
  - src/
  - tests/
```

Everything outside governed roots is ungoverned by default in the Greenfield
MVP: `.gitignore`, LICENSE, README, lockfiles, CI configuration, editor
configuration. `.aes/` itself is governed by the initialization contract, not by
project topology. Inside a governed root, every durable file needs an exact
planned path or a bounded generation rule, exactly as the candidate says.

Wrong-when: a real consumer needs a governed file outside `src/`/`tests/` that
cannot be expressed as an additional governed root; or the probe finds the
check catching nothing because governed roots were declared too narrowly.

### D2. Evidence sufficiency is conjunction-only for the MVP

A success criterion is `SUPPORTS` with `SUFFICIENT` adequacy only when **every**
listed evidence requirement has at least one `CURRENT` observation whose
assessment is `SUPPORTS`. No thresholds, no disjunction, no repetition counts,
no weighting. Open question 3 is closed with this rule; reopen only when a real
criterion on a real consumer cannot be expressed this way.

Wrong-when: the first authentic consumer has a criterion that genuinely needs
"any one of" or "N of M" and the workaround distorts the criterion's meaning.

### D3. The public term is `component`

`realization_unit` remains the semantic-model name in prose if useful; the
record field, CLI vocabulary and documentation use `component`. Decision 0003
already chose this word for the same boundary. Open question 1 is closed.

Wrong-when: `component` demonstrably collides with a consumer ecosystem's own
"component" concept in a way that confuses the fresh-agent evaluation.

### D4. Supersession is stated, not left implicit

The PR's nonclaim "does not supersede Decisions 0001–0009" is true of the
proposal and false of its acceptance. The v0.2 cutover decision must
explicitly supersede:

- Decision 0001 §3 (incumbents as capability sources with retained ownership)
  and §6 (no local package until Company Planning derives topology);
- Decision 0002 (AES-local profile over Company Planning as the planning route);
- Decision 0009 (Enforced Planning retains installed authority; Company
  Planning owns planning derivation).

Decisions 0003, 0004, 0005, 0006 and 0008 are largely re-derived by v0.2 under
new names and should be recorded as *carried forward with renames*, not
superseded. Decision 0007 is already superseded by 0008.

### D5. v0.1 governance was bypassed to produce v0.2, and that is evidence

All 67 commits on this branch are tagged `[Unplanned]` under v0.1's own
Enforced Planning governance. Real design work routed around the control the
moment it started. This is the strongest concrete support for v0.2's stance
that hooks are invocation adapters, not enforcement (`PB-GF-GIT` limitations,
`22-portable-provider-boundaries.md` §3). Record it in the cutover decision.

## 2. Consumer-selection rule (Brian, 2026-09-25: option A approved)

The first authentic consumer is **a small new Python tool Brian already needs,
governed by AES from its first commit**. Rejected alternatives: a purpose-built
toy (fails the validation profile's own real-scope requirement) and deferring
the choice until code exists (delays the only decisive test).

Survey of the current weekly plans (`weekly-plans/personal/THIS_WEEK.md`,
`weekly-plans/inside-success/THIS_WEEK.md`) on 2026-09-25 found **no item that
is a genuinely new small Python tool**. Candidates checked and why each fails
the "new project from inception" requirement:

| candidate | why rejected |
| --- | --- |
| hook-event reader / before-after readout (Priority 6) | `enforced-planning/scripts/hook_receipts.py` already has a scanner and `hook_feedback_report.py` consumes it; this is an extension |
| personal-wiki source extractor (Priority 5) | Gmail/Calendar connector is blocked pending re-authorization; `tools/google_access.py` already exists |
| personal-wiki page linter (Priority 5) | `~/.claude/skills/karpathy-wiki/scripts/lint.py` already lints it |
| weekly ChatGPT supervisor dispatch | exists with 11 passing tests |
| Never Absolute formation checklist (Priority 4) | not a tool; a legal filing |

**Named by Brian, 2026-09-25: a new version of WhyGame.** Repository
`BrianMills2718/whygame5`, a fresh private repo governed by AES from its first
commit. Lineage: `whygame4` (recursive why-questioning into a graph) was
superseded by `whygame-reboot` (graph as adversary). Brian's recorded
judgement on the reboot's Plan 2 (2026-09-07) found that both runs' conflicts
were planted by the proposal prompt, not found by the evaluator; the reboot's
own deferred next goal was "an evaluator that can find its own conflicts
rather than a planted one." That is the first accepted outcome of the new
version. Neither prior repository is modified; `whygame-reboot` remains the
Project Graph's current WhyGame generation until the new version earns
supersession through Project Meta.

Original open text: Selection criteria the tool must meet:
Python, new Git repository, real user this week, at least two implementation
files and one test file, one public function whose signature is a genuine
commitment, one criterion that a passing test alone cannot establish (human
review or runtime observation), and no dependency on Brian's private AES
repositories.

## 3. Build order: probe 0 first

Do not implement the ten realization units in topology order. Probe 0 is the
cheapest path to the SC-GF-005/SC-GF-008 A/B test:

1. Hand-write `.aes/target.yaml` for the consumer (outcome, normative items,
   criteria with evidence requirements, planned artifacts, verification
   subjects). Seven of the seventeen semantic families; defer failure modes,
   capability requirements, provider bindings, generation rules and symbol
   commitments to probe 1.
2. Implement only `records.py` (strict load + ref validation) and `context.py`
   (`aes context <subject>`), roughly `RU-AES-RECORDS` and `RU-AES-CONTEXT`.
3. Run the same real change twice on the consumer: arm A receives the context
   packet; arm B receives the repository and README only. **Arm B must be a
   separate agent session with no access to this conversation, this proposals
   directory, or the AES canonical repository.** The same operator running
   both arms from one session invalidates the result.
4. Record both arms as observations at exact revisions. Compare on the
   validation profile's measures (files read, missed obligations, topology
   violations, rework).
5. Only if arm A is materially better: proceed to probe 1 (topology check,
   characterize, evidence, reconcile). If it is not: stop and reframe before
   writing any further architecture document.

Stop rule for the whole lineage: **no new architecture proposal document until
probe 0 has a recorded result.**

## 4. Deferred to the probe (learn, do not decide now)

- stdlib `ast` versus Griffe for characterization;
- exact Python version range and dependency pins;
- whether ruamel.yaml round-trip preserves a hand-edited `target.yaml` well
  enough for `aes plan accept` to write it (load-bearing: if it mangles
  comments/ordering the "review target changes as one diff" benefit is lost);
- where evidence assessments are stored (open question 12);
- the assessor-identity minimum (open question 13).

## 5. Answers to the twelve load-bearing review questions

1. Kernel not minimal (17 families); freeze it, let probe 0 use seven.
2. `component` (D3).
3. Exact topology correctly scoped once D1 bounds "governed"; unbounded, too strong.
4. One `target.yaml`: yes; ruamel round-trip is load-bearing (section 4).
5. Planning transaction ordering: correct; best part of the design.
6. Evidence model: sufficient with D2.
7. Python + Git: yes.
8. Residuals: reconcile, evidence, context are AES-specific; records and topology are thin wrappers, acceptable.
9. Topology boundaries: meaningful, but 23 files and 8 signatures before a consumer is over-planned; probe 0 realizes five or six.
10. Falsification profile: strong on paper; weak on n=1 and operator contamination (section 3 step 3).
11. Provider rejections: justified.
12. Decide now: D1–D4 and the consumer. Learn in probe: section 4.

## 6. Probe 0 result (2026-09-25)

Run on the first authentic consumer, `BrianMills2718/whygame5`, at base commit
`24ce4128`. Change under test: realize `CMP-WG5-EVALUATOR` (evaluator module
and its tests). Implementation used: `records.py`, `context.py`, `cli.py` on
this branch (24 greenfield tests passing; `aes target validate` and
`aes context CMP-WG5-EVALUATOR` run against the real consumer).

| arm | input | files read | tests | obligations missed | topology violations |
| --- | --- | --- | --- | --- | --- |
| A | context packet + repository | 8 | 12 passed | 0 | 0 |
| B | repository + README only | 9 | 10 passed | 0 | 0 |

**Verdict: not distinguishable.** Both arms met all eight pre-registered
obligations and produced mergeable code. Arm B found every obligation by reading
the whole repository, including `.aes/target.yaml`, which is nine files and
about three hundred lines. The projected-context claim (`SC-GF-005`,
`SC-GF-008`) is neither supported nor refuted at this repository size; the
experiment has no power until whole-repository orientation is measurably
costly. Full observation with the pre-registered scoring sheet:
`whygame5/.aes/observations/OBS-PROBE0-CONTEXT-AB.yaml`.

What probe 0 did establish on a real consumer:

- the strict loader rejects duplicate keys, unresolved refs and criteria
  without evidence requirements on real edits of the real target;
- the packet is bounded (the report obligation appears only in the
  "not included" list) and carries full text, not IDs;
- a real topology violation occurred during setup: a build tool wrote
  `src/whygame5.egg-info/` under the governed `src/` root and it was
  committed before anyone noticed. `SC-GF-003`'s topology check
  (`RU-AES-TOPOLOGY`) is the next unit to build, and D1's governed-roots
  rule is confirmed as the right boundary.

Wrong-when for the verdict: a rerun of the same design on a consumer with at
least several thousand lines and obligations spread across files shows arm A
materially ahead, or shows arm B ahead. Either result is decisive; this one
was not.

Next: continue whygame5 toward its own `SC-WG5-001` (prompts, runner, live
run) so the consumer grows for real reasons; rerun the A/B when whygame5 has a
runner, report and CLI. (`topology.py` was built next; see section 8.)

## 7. How the two decisions in this file were delivered, and the fix (2026-09-25)

Both decisions handed to Brian today (the PR #35 verdict, and confirming the
whygame5 outcome) went out as terminal prose with lettered options. Measured
against Representation Router `references/planning-review.md` and AES's own
`HUMAN_OBSERVABLE_DELIVERY.md` §7, that was the wrong surface: the coverage
shape (which criteria have proof, which files exist, what nothing planned)
was invisible. The fix is the temporary renderer `scripts/probe/render_review.py`
and `whygame5/.aes/generated/review.html`; the guidance now lives in the
router profile (structured proposal/target case, pre-ask checklist) and open
question 22 here. Wrong-when: a second real decision delivered through the
page is answered no faster or no better than prose would have been.

## 8. Topology check realized, and the consumer now enforces it (2026-09-25)

`aes topology check` (`src/agentic_engineering_system/topology.py`) realizes
`RU-AES-TOPOLOGY` for exact paths. Durable means in the Git index, so ignored
build output is not an orphan and a staged orphan fails before it is committed.
Planned artifacts with no file yet are listed as unrealized, not failed.
Bounded generation rules are not implemented because no consumer file needs one.

Evidence:

- `ER-SC-GF-003-01`: replayed on the real historical whygame5 commit `cceec15`,
  where the egg-info was committed, the check exits 1 and names all six
  `src/whygame5.egg-info/*` files. `tests/greenfield/test_topology.py` holds the
  same case as a regression test.
- `ER-SC-GF-003-02`: on whygame5 `main@9c9ee2a` the check exits 0 with 6
  governed files and 5 unrealized planned artifacts.

whygame5 now runs `aes target validate` and `aes topology check` from a
committed pre-commit hook (`make setup` enables it) and from `make check`, with
AES as a pinned dev dependency and the rules stated in its `AGENTS.md`, so an
agent working there hits the rules without being told to reach into this
repository. Checked: a staged orphan `src/whygame5/stray.py` was refused by the
hook; the wiring commit itself passed through it.

The gate deliberately lives outside `src/` and `tests/`. A pytest file that
checks AES conformance is not part of any whygame5 outcome, and giving it one
would distort the target, so it is not a planned artifact. This is a first
data point on where AES's own scaffolding belongs in a governed consumer.

Wrong-when: a real whygame5 change needs a generated file under a governed root
that cannot be listed by exact path (implement generation rules then), or an
agent commits an orphan in whygame5 without the hook or the tests catching it.

## 9. Evidence standing realized, and the consumer is a method (2026-09-25)

**The consumer is a method, not the goal.** Brian, 2026-09-25: "i am ambivalent
abotu why game5. if advancing it towards its final state helps us work otu
kinks in aes canonical then lets do that i just dont want to mistake the methods
with the goal." whygame5 advances only where that exercises or exposes something
in AES. Product-quality work on WhyGame that teaches AES nothing is out of
scope here. Wrong-when: whygame5 stops producing AES findings while it grows,
which is the signal to change or add a consumer rather than keep building it.

`aes evidence status` (`src/agentic_engineering_system/evidence.py`) realizes
`RU-AES-EVIDENCE` in its smallest form. Choices made, each with a wrong-when:

- **Assessments live inside the observation**, one per evidence requirement,
  never per criterion (`16-record-shapes` option
  `retained_inside_observation_assessment_receipt`). Wrong-when: two assessors
  need to disagree about one observation without editing it.
- **Freshness from Git.** An observation names the commit it observed and the
  paths its result depends on; it is CURRENT until one of those paths changes,
  then STALE. With no commit or no paths it is UNKNOWN and never counts, so a
  human review names the commit and files it reviewed. Wrong-when: a real
  dependency that is not a repository path (a model version, an external
  service) changes and the evidence stays CURRENT.
- **Standing** follows D2: SUPPORTED only when every requirement has a CURRENT
  supporting assessment; REFUTED when any requirement has a CURRENT refuting
  one; otherwise INSUFFICIENT with the reason per requirement. Wrong-when: a
  CURRENT refutation should be outweighed rather than win.

Evidence on the real consumer (whygame5 `main@0a093e7` plus its converted
records): 6 criteria, 3 SUPPORTED by recorded test runs, 3 INSUFFICIENT with
the missing live run, human review, or uncovered check named. The chain-fit
refutation `OBS-WG5-006-CHAIN-FIT-1` is correctly STALE because the prompts,
ontology and probe it observed have changed since (`SC-GF-008` on real data).
Tests: `tests/greenfield/test_evidence.py` (`ER-SC-GF-007-01`, `ER-SC-GF-008`).

Kinks the consumer exposed:

1. **Hand-written observations did not load.** All three pre-existing whygame5
   observations failed the strict loader (a combined revision/identity field,
   extra top-level fields). Converted without content loss, checked by
   comparing parsed content before and after.
2. **Observations of uncommitted work have no revision.** Two were recorded as
   "branch X on base <sha>" because the run happened before the commit. The
   commit that later held the observed code was used. AES should require
   committing before observing, or record the revision at commit time.
3. **AES tests read the live consumer.** `tests/greenfield` loaded
   `/home/brian/code/whygame5/.aes`, so the consumer growing broke four AES
   tests and the tests only ran on Brian's machine. They now load a frozen copy
   (`tests/greenfield/fixtures/whygame5-54043e2/`).
4. **Recording a test run as an observation is manual.** Four observations were
   hand-written from four pytest runs. Next: `aes evidence record`, which runs
   a verification subject's command at HEAD and writes the observation with its
   revision and dependency paths.
5. **The consumer's pre-commit hook was hand-copied** and broke in linked
   worktrees (no `.venv`). AES should ship it (`aes hooks install`).

## 10. Recording evidence by running it (2026-09-25)

`aes evidence record <VS-ID>` runs one deterministic-test verification subject
at HEAD and writes the observation: the commit, the dependency paths (the test
file plus `--depends-on`), the command, exit code and output tail, and one
assessment per evidence requirement the subject proves. Exit 0 is SUPPORTS,
or INCONCLUSIVE with `--inconclusive <basis>` for a test that covers only part
of a requirement; any other exit is REFUTES. It refuses while a dependency has
uncommitted changes, closing kink 2 of section 9, and refuses human-review and
external subjects, which running a command cannot produce.

Wrong-when: a recorded SUPPORTS stays CURRENT while the code it exercised has
changed, because a source file it depends on was not listed in
`--depends-on`. Dependency paths are declared, not discovered.

A consumer hazard found while preparing the first real run: linked worktrees
share the main checkout's `.venv`, where the consumer is installed editable
from the main checkout. A test run inside a worktree can then import the main
checkout's source while the observation names the worktree's commit. The
consumer must make its test runner import its own tree (for whygame5,
pytest `pythonpath = ["src"]`).

## 11. Distribution: version moves, hook ships (2026-09-25)

Roadmap phase 1 (`25-roadmap-to-mvp-acceptance.md`). Realized:

- **Git-derived version.** `pyproject.toml` takes its version from
  `setuptools-scm`. With no tags every commit builds as `0.1.devN+g<sha>`, so
  a pin bump is a version change and pip reinstalls without
  `--force-reinstall`. There is no `fallback_version`: a build without Git
  metadata fails instead of shipping a version that never moves.
  `aes --version` prints the installed version and exits 1 if the
  distribution is not installed.
- **`aes hooks install`** (`src/agentic_engineering_system/hooks.py`, added to
  the candidate topology as `ART-SRC-HOOKS`) writes `.githooks/pre-commit`
  and sets the local `core.hooksPath`. The hook runs `aes target validate`
  and `aes topology check` with the interpreter that installed it, then the
  worktree's `.venv`, then the main checkout's `.venv` (via
  `git rev-parse --git-common-dir`), then `PATH`; none found fails the
  commit. It refuses outside a Git top level, without a target, over a
  pre-commit hook it did not write (in `.githooks/` or the repository's own
  hooks directory), and over a local `core.hooksPath` pointing elsewhere.
  Its hooks carry `# managed by aes hooks install` on line 2 (line 1 is the
  shebang) and are rewritten on reinstall.

Evidence: `tests/greenfield/test_distribution.py` installs the repository
into a fresh venv in the consumer's pin form, checks `aes --version` names
the pinned commit, and runs the installed `aes hooks install` on a copy of
the whygame5 records: a staged orphan is refused and names the file, the
same commit passes once the target plans it. A linked-worktree case with no
`.venv` of its own passes through the main checkout's venv, the case that
broke whygame5's hand-copied hook.

What it exposed:

1. **A named `git+file://` pin is not a valid requirement.** PEP 508 named
   URLs need a host, so `name @ git+file:///path@sha` is rejected by pip;
   `git+file://localhost/path@sha` works. The consumer's `git+https://` form
   is unaffected. Local pin tests use the `localhost` form.
2. **A local `core.hooksPath` silences the global hooks.** This machine
   sets a global `core.hooksPath` whose pre-commit refuses `.env` files and
   chains to `.git/hooks`. Setting the repository-local path, as whygame5
   and the governed repositories already do, bypasses it. `aes hooks
   install` reports the override rather than refusing, because refusing
   would make it unusable on every machine with a global path.
3. **The hook names an absolute interpreter.** Committed into a consumer,
   that path is machine-specific. On another machine it is absent and the
   `.venv` lookup takes over, so it degrades to the old behavior rather
   than failing, but the committed file differs per installer.

Decision: report, do not refuse, a global `core.hooksPath` override.
Wrong-when: a consumer commits a file the global hook would have refused
(an `.env`, a canonical-checkout commit) because `aes hooks install`
disabled it; then the AES hook must chain to the global one.

## 12. Project initialization realized (2026-09-25)

Roadmap phase 2 (`25-roadmap-to-mvp-acceptance.md`). Realized:

- **`aes init --project-id ID --actor TEXT --outcome TEXT`**
  (`src/agentic_engineering_system/project.py`, `ART-SRC-PROJECT`) writes
  exactly the contract's two seed artifacts: `.aes/project.yaml` (schema
  version, project id, governed roots, architecture line, the installed
  distribution version from `importlib.metadata` and `initialized_at`, the
  paths deferred artifacts will use, the primary language) and
  `.aes/target.yaml` holding one outcome and empty lists for every other
  family. Both are staged in a temporary sibling directory, loaded strictly
  with `load_project`/`load_target`, compared with the seed set, and renamed
  to `.aes/` in one step. It refuses, writing nothing, outside Git, below the
  work-tree top, over an existing `.aes/`, on an empty outcome or actor, and
  when the staged tree holds anything the contract does not name as a seed
  (the deferred analysis, plans, observations and generated paths).
- **Project discovery.** `find_project_root` walks up to the nearest
  `.aes/project.yaml`; every other command uses it when `--root` is absent,
  so `aes` works from subdirectories and from linked worktrees, which check
  out their own `.aes/`.
- **Getting started.** `docs/greenfield/GETTING_STARTED.md`
  (`ART-DOC-GREENFIELD-GETTING-STARTED`) takes an empty directory to one
  SUPPORTED criterion. Every command block in it was executed verbatim in a
  fresh directory against an install pinned to the branch commit.

Evidence: `tests/greenfield/test_project.py` (22 cases): init in a temporary
Git repository passes `target validate`, `topology check` and `evidence
status`; each refusal leaves the tree byte-identical; a deferred artifact
injected into the staged tree refuses the whole init; discovery works from a
nested directory and from a linked worktree, including `hooks install`.
Removing the seed-set comparison fails four cases; replacing discovery with
the old `.` default fails three.

What the contract under-specified:

1. **The outcome record needs an actor.** `initial_target_minimum` requires
   only `outcomes`, but the outcome record (from probe 0) requires
   `actor_or_consumer`. A placeholder would be an empty authoritative shell,
   so `aes init` takes a required `--actor`, a departure from the roadmap's
   `aes init --project-id <id>` shape.
2. **The project record needs a language.** `explicit_nonclaims` says the
   project language is not selected, but `ProjectRecord.ecosystem` is
   required and `aes evidence record` uses it to choose the default test
   command. `--language` defaults to `python` and the value is printed.
3. **`initialized_at` had no field.** The strict project record forbade it;
   it is now an optional field of `aes`, absent in hand-made projects such as
   the whygame5 fixture.
4. **The planned symbol changed.** `SYM-AES-PROJECT-INIT` planned
   `initialize_project(root, *, project_id, architecture_line) -> ProjectRecord`;
   the realized function also takes the outcome, actor, governed roots and
   language and returns an `InitResult` (paths plus both loaded records).
   The topology entry is updated to the realized signature.
5. **The install source is private.** The getting-started install line needs
   read access to this repository; the roadmap's clean-user run assumes a
   stranger can install from it. Until the repository or a built
   distribution is public, the clean-user run needs granted access.

Decision: discovery stops at the first `.aes/project.yaml` found walking up,
not at the Git work-tree top. Wrong-when: a command run inside a repository
that has no `.aes/` of its own silently operates on an enclosing directory's
project (a nested checkout under an initialized one); then discovery must
stop at `git rev-parse --show-toplevel`.

## 13. Characterization realized (2026-09-25)

Roadmap phase 3 (`25-roadmap-to-mvp-acceptance.md`). Realized:

- **`characterize.py`** (`ART-SRC-CHARACTERIZE`). `aes characterize [--json]`
  lists every file under the governed roots at HEAD with blob hash and size,
  bound to `subject_revision` (40-hex HEAD), `dirty`, and
  `producer: {identity: aes, version}`; schema
  `aes.v0_2.characterization.probe0`. The body is deterministic;
  `produced_at` is a separate field and the text report omits it. On
  whygame5 at `f5a0d01` two runs of the text report are byte-identical and
  the two JSON outputs differ only in `produced_at` (the phase exit gate).
- **`characterize_python.py`** (`ART-SRC-CHARACTERIZE-PYTHON`). With `ast`
  only: module name (`src/` layout), top-level public symbols with a
  signature string for functions, and intra-repository import edges
  (absolute, `from`, relative; package `__init__.py` files a dotted import
  executes; a bare sibling import from a non-package directory, which is how
  pytest finds test helpers). A file that raises at import characterizes
  normally; a file that does not parse records `parse_error`.
- **Symbol commitments.** A planned artifact may carry `exports:`, each
  `name` or `name(args) -> ret`, only on `kind: source` `.py` artifacts.
  `aes characterize` exits 1 on a missing committed export, a changed
  committed signature, or an orphan; orphans and unrealized artifacts come
  from `topology.compare_topology`, now shared with `aes topology check`.
  Unrealized artifacts are reported, not drift. Recorded in
  `16-record-shapes.candidate.yaml` as `realized_probe0_symbol_commitments`.
- **Dependency discovery.** `aes evidence record` on a Python test now takes
  `dependency_paths` = the test file + every governed file its imports reach
  at HEAD + `--depends-on`. The observation keeps
  `dependency_basis: {locator, discovered, declared}`, and loading fails if
  `dependency_paths` is not their union.

Evidence: `tests/greenfield/test_characterize.py` (12 tests, including
ER-SC-GF-006-01: an `exports:` commitment on `ART-WG5-PROMPTS`, the symbol
renamed in a commit, `missing_export` reported and exit 1) and three new
cases in `test_evidence.py`.

What the consumer showed:

1. **Existing standings unchanged.** `aes evidence status` on whygame5 at
   `f5a0d01`, with the pinned AES (`2d4db5c`) and with this change, is
   byte-identical: SC-WG5-002, 003, 004 SUPPORTED; 001, 005, 006
   INSUFFICIENT; the only STALE observation is `OBS-WG5-006-CHAIN-FIT-1`,
   stale before and after. Existing observations keep their stored
   `dependency_paths`; discovery applies only to new recordings.
2. **Discovered versus hand-declared**, re-recording all five
   deterministic-test subjects in a scratch clone at `f5a0d01` with no
   `--depends-on`, against the `-a7611a86` observations:
   - all five: discovery adds `src/whygame5/__init__.py` (every test imports
     through the `whygame5` package, which executes it);
   - VS-WG5-PROMPTS: the hand list has `src/whygame5/contracts.py`, which
     discovery does not find. `test_prompts.py` imports only
     `whygame5.prompts`, and `prompts.py` imports nothing local. The file
     was declared because the assessment's basis is about
     `contracts.ModelProposal`: a claim-scope dependency, not an executed
     one. That is exactly what `--depends-on` stays for.
   - otherwise identical. No observation went STALE; all five new ones are
     CURRENT at `f5a0d01`.
3. **Drift on the real consumer.** In the same scratch clone,
   `exports: [WhyChain, Misfit]` on `ART-WG5-ONTOLOGY` characterizes OK;
   renaming `WhyChain` in a commit gives `missing_export:
   src/whygame5/ontology.py (ART-WG5-ONTOLOGY) - committed export 'WhyChain'
   is not a top-level public symbol`, exit 1. Not yet recorded as an
   observation on whygame5 itself, which needs a consumer change.

Decisions:

- **Facts come from the HEAD tree, not the index.** `git ls-tree HEAD`,
  with content read by blob hash, so every fact is a fact about
  `subject_revision` (ER-SC-GF-006-02); `dirty` flags a working tree or
  index that differs. `aes topology check` keeps using the index, because
  it is a pre-commit gate. Wrong-when: a consumer wants symbol drift as a
  pre-commit gate, where HEAD is the commit before the one being checked;
  then add an index mode rather than weakening the revision binding.
- **Signatures are committed only when written.** `name` commits existence;
  `name(args) -> ret` also commits the signature, compared after both sides
  are parsed and re-rendered, so spacing is not drift. Classes and
  variables carry no signature. Wrong-when: a consumer reports drift that
  is only annotation spelling (a quoted forward reference against an
  unquoted one); then normalize annotations or compare parameter names only.
- **All imports in a file count, including function-level and
  `TYPE_CHECKING` ones; package `__init__.py` files count.** Code a test can
  reach is a dependency. Wrong-when: evidence goes STALE on whygame5 or AES
  canonical because only a `TYPE_CHECKING` import target changed; then skip
  those blocks.
- **Discovery is imports only, and declaration is additive.** It does not
  see `conftest.py`, data files the test reads, pytest configuration, or
  claim-scope files like `contracts.py` above. Wrong-when: a recorded
  SUPPORTS stays CURRENT after a `conftest.py` or test-data change it
  depended on; then add pytest's conftest chain to discovery.
- **Producer version is the installed distribution's.** Like the evidence
  recorder, it reads `importlib.metadata`, which in an editable dev venv is
  the version at install time (run from this branch's worktree it reported
  `0.1.dev367+g0503735f9`, the main checkout's install), not the code
  actually running. Consumers install by pin, where the two agree.
  Unlike the recorder it fails if the distribution is not installed.
  Wrong-when: a characterization names a producer version whose code does
  not match what produced it on a consumer install.

## 14. Reconcile and status realized (2026-09-25)

Roadmap phase 4 (`25-roadmap-to-mvp-acceptance.md`). Realized:

- **`reconcile.py`** (`ART-SRC-RECONCILE`). `reconcile(root)` composes
  `characterize` + `drift` (whose orphans and unrealized artifacts come from
  `topology.compare_topology` over the HEAD tree) and `evidence.assess`, and
  adds only what the target's refs say: which verification subjects route to
  an evidence requirement, and which artifacts and criteria concern each
  component. Output schema `aes.v0_2.reconciliation.probe0`, bound to
  `subject_revision` (HEAD), `dirty` and `producer` as a characterization is;
  `produced_at` is separate and the text reports omit it. Per planned
  artifact REALIZED | UNREALIZED | DRIFTED with the drift findings; per
  criterion its D2 standing and every evidence requirement without current
  support, each with the verification subjects that could supply it (`has_route`
  false is the SC-GF-004 "no route" gap); per observation its freshness; per
  component its open gaps, ordered drifted, refuted, unrealized, insufficient.
  Orphans, artifacts no component owns and criteria that concern no
  component are listed as project-level gaps.
- **`aes reconcile [--json]`** (full report) and **`aes status`** (one
  screen: revision and dirty flag, counts, first open gap per component).
  Both exit 1 on a REFUTED criterion, an orphan, or failing drift; INSUFFICIENT
  exits 0 and the output says so.
- Nothing is written. Every run recomputes from target, repository at HEAD and
  observations, so a gap closes only through a new observation or a change to
  code or target.

Evidence: `tests/greenfield/test_reconcile.py` (9 tests, on a temp Git copy of
the frozen whygame5 records with stand-in files): baseline statuses; a
criterion SUPPORTED at commit N whose dependency changes at N+1 is INSUFFICIENT
with its observation STALE and the gap back on its component (SC-GF-008 at the
gap level); an evidence requirement whose only verification subject is removed
is reported as no route; exit 1 for REFUTED, orphan and drift, exit 0 for
INSUFFICIENT only; two runs equal apart from `produced_at`, text output
byte-identical; no file anywhere in the repository changes. The getting-started
example (`docs/greenfield/GETTING_STARTED.md` §6) was re-run with this branch:
SC-001 SUPPORTED with no open gap, then after a commit to the greeter source
`insufficient SC-001`, observation stale.

What the consumer showed, read-only on whygame5 at `eed13c4` (its main, AES pin
`52567f9`), `aes status`:

```text
OK status: whygame5-target at eed13c47d86c62427426d0fb79c9a9cbe42b229a
  artifacts: 11 realized, 3 unrealized, 0 drifted; 0 orphan(s)
  criteria: 3 supported, 3 insufficient, 0 refuted; 0 unsupported evidence requirement(s) with no route
  observations: 11 current, 2 stale, 1 unknown
  first open gap per component:
    CMP-WG5-CONTRACTS: no open gap
    CMP-WG5-GRAPH: no open gap
    CMP-WG5-EVALUATOR: insufficient SC-WG5-001 - ER-WG5-001-01 NO_CURRENT_SUPPORT; ER-WG5-001-02 NO_CURRENT_SUPPORT; ER-WG5-001-03 NO_CURRENT_SUPPORT
    CMP-WG5-PROMPTS: insufficient SC-WG5-001 - ER-WG5-001-01 NO_CURRENT_SUPPORT; ER-WG5-001-02 NO_CURRENT_SUPPORT; ER-WG5-001-03 NO_CURRENT_SUPPORT (+1 more)
    CMP-WG5-RUNNER: unrealized ART-WG5-RUNNER - src/whygame5/runner.py: planned, no file at HEAD (+1 more)
    CMP-WG5-REPORT: unrealized ART-WG5-REPORT - src/whygame5/report.py: planned, no file at HEAD (+1 more)
    CMP-WG5-ONTOLOGY: insufficient SC-WG5-006 - ER-WG5-006-02 NO_CURRENT_SUPPORT; ER-WG5-006-03 NO_CURRENT_SUPPORT
  INSUFFICIENT criteria are normal while work is in progress and do not fail this command; a REFUTED criterion, an orphan or drift does.
```

1. **The gaps are the ones the consumer knows.** SC-WG5-001, 005, 006
   INSUFFICIENT; ART-WG5-RUNNER, REPORT, CLI unrealized; exit 0.
   `OBS-WG5-006-CHAIN-FIT-1` is STALE, as in §13. The second STALE one,
   `OBS-WG5-DRIFT-b0c3e24f`, arrived with whygame5 `eed13c4` after this phase
   was specified: it observed a scratch commit that renamed a symbol in
   `ontology.py`, so it is stale from birth and its commit message says so. At
   the previous main `f5a0d01` (a clone) the counts are
   `10 current, 1 stale, 1 unknown`, exactly the one expected.
2. **A stale-from-birth observation is a kink.** A drift observation is evidence
   about a deliberately mutated scratch revision, not about the consumer's
   line of history, so the freshness rule (any dependency changed between the
   observed commit and HEAD) marks it STALE and its SUPPORTS for
   ER-WG5-006-04 never counts. ER-WG5-006-04 stands SUPPORTED only through
   `OBS-WG5-CHARACTERIZE-4921a159`, and the stale count carries a permanent
   entry that is not a gap anyone can close. Not changed here; it belongs to
   EVIDENCE (observations of a mutated subject need their own freshness basis).
3. **Components share criteria through normative items.** SC-WG5-001 shows
   under both EVALUATOR and PROMPTS, SC-WG5-006 under PROMPTS and ONTOLOGY,
   and in the fixture SC-WG5-003 under RUNNER, because their `target_refs`
   share a normative item. That is what the target says; whether it is the
   useful reading is for the consumer to tell.
4. Two runs of `aes reconcile` on whygame5 are byte-identical; `dirty` false;
   whygame5's working tree unchanged.

Not done in this phase: the reconciliation is not yet recorded as an
observation on whygame5, and whygame5's `make check` still runs the three
separate commands (both are consumer changes, the roadmap's exit gate). Note for
that swap: `aes status` covers `aes target validate` (it loads the target
strictly) and `aes evidence status`, but reads topology from HEAD, not the
index, so it is not a pre-commit replacement for `aes topology check`.

Decisions:

- **Topology in reconcile is HEAD's, not the index's.** Everything in one
  reconciliation is a fact about `subject_revision`; the pre-commit hook keeps
  the index check. Wrong-when: a consumer relies on `aes status` alone and an
  orphan staged but not committed goes unreported where it mattered.
- **`dirty` also covers `.aes/`, untracked files included.** The target and
  observations are read from disk, so a new unrecorded observation makes the
  reconciliation not purely a fact about HEAD. Wrong-when: `dirty` is true on
  every consumer run because of generated files under `.aes/` that Git does
  not ignore.
- **Artifacts outside the governed roots get presence only.** `pyproject.toml`
  is REALIZED if it exists at HEAD, with a note that it is not characterized.
  Wrong-when: such an artifact reports REALIZED while its content has
  drifted from what the target commits.
- **A criterion concerns a component by declared refs only**: named in the
  component's `target_refs`, sharing a ref with them, or named by an artifact the
  component owns. Wrong-when: a component's first gap on whygame5 is one
  nobody working on that component would act on (as item 3 may turn out to be).
- **"No route" and unrealized are gaps, not failures.** Exit 1 is reserved
  for REFUTED, orphan and drift, as the roadmap specifies. Wrong-when: plan
  acceptance (phase 5) ships without also failing on an unrouted requirement,
  so SC-GF-004 is never enforced anywhere.

## 15. Planning acceptance realized (2026-09-25)

Roadmap phase 5 (`25-roadmap-to-mvp-acceptance.md`), bounded to the target
acceptance transaction of `15-planning-contract.candidate.yaml`: no plan
generation, no model call, no provider selection. Realized:

- **`planning.py`** (`ART-SRC-PLANNING`). A proposal
  (`aes.v0_2.proposal.probe0`) is `proposal_id`, `title`, `rationale`,
  `closes_gaps` and a `target_delta` with `add:` and `change:` sections, one
  list per target family, entries in exactly the target's shape; `change`
  replaces the whole entry with the same id. No `remove`. The module file wins
  over the empty v0.1 `planning/` directory on import (tested).
- **`aes plan prepare [--out FILE]`**: the open gaps of the current
  reconciliation with ids, unrouted evidence requirements, every declared id
  by family, and an empty proposal. Deterministic; writes nothing in the
  repository.
- **`aes plan validate <proposal>`**: applies the delta in memory and reports
  every violation: delta keys (`change` of an absent id, `add` of a present
  one), the resulting target under `records.validate_target_refs`, every
  evidence requirement of the resulting target without a verification subject
  or an external boundary (SC-GF-004), `closes_gaps` ids not open now, and
  planned artifacts outside the governed roots that are source or carry no
  reason (`outside_governed_roots`).
- **`aes plan accept <proposal>`**: refuses on tracked changes or anything
  untracked under `.aes/`, on any violation, and on an existing
  `.aes/plans/<proposal_id>.yaml`; otherwise edits `.aes/target.yaml` through
  ruamel round-trip (the proposal's entries appended in the style they were
  written, changed entries replaced in place, the blank line that ended a
  family moved to its new last entry), checks the written text loads to
  exactly the validated target, and writes the plan: the proposal plus
  `accepted_at_revision` (HEAD) and `accepted_at` (UTC). No commit.
- **`records.py`**: optional target family `external_boundaries:
  [{evidence_requirement_ref, boundary}]`, refs checked. **`reconcile.py`**:
  `Gap.id` (`<kind>:<ref>`, also in `--json`) and `Reconciliation.open_gaps()`.
- **`planning_protocol.md`** (`ART-PLANNING-PROTOCOL`): the one-page protocol
  with the whygame5 proposal as its example; a test keeps the example equal
  to `tests/greenfield/fixtures/whygame5-proposal-runner.yaml`.

Evidence: `tests/greenfield/test_planning.py` (19 tests, temp Git copy of the
frozen whygame5 records as in `test_reconcile.py`): prepare deterministic with
the fixture's eight open gaps; validate accepts the consumer proposal and
rejects, each from a single mutation of it, a criterion without an evidence
requirement, a requirement with no route (an external boundary instead is
accepted), a gap that is not open, an unresolved ref, an add of an existing
id (same and other family), a change of an absent id, and a source artifact
outside the governed roots; accept refuses a dirty tree (tracked change;
untracked observation), a failing proposal and a repeated plan id with the
repository byte-identical; accept on the fixture removes exactly one target
line (the changed component's refs), keeps a comment, writes only the plan
file, binds it to HEAD, and the committed result loads strictly and
reconciles with the claimed gaps still open; accept on an `aes init` target
turns `[]` into block lists. The getting-started example
(`docs/greenfield/GETTING_STARTED.md` §3, now planned through a proposal)
was re-run end to end with this branch's code on PATH (not a clean-user pip
install): prepare, the no-route refusal, validate, accept, commit, implement,
record, `aes status` SC-001 SUPPORTED.

What the consumer showed, on a clone of whygame5 at `a620cdc` (its main, AES
pin `68a71fe`; the real checkout was not touched). `aes status` before: 11
realized, 3 unrealized (RUNNER, CLI, REPORT); CMP-WG5-RUNNER's gaps are only
its two unrealized files. Reading the target: the runner's defining
constraint NI-WG5-006 (llm_client receipts, no retries, no fallback, a failed
call stops the run) is named by the component and the artifact but by **no
success criterion**, so a written runner could not be shown to obey it, and
the runner has no test artifact. The proposal adds SC-WG5-007 with
ER-WG5-007-01, the test artifact, and gives CMP-WG5-RUNNER the test.

```text
$ aes plan prepare --out packet.yaml        # open_gaps: insufficient:SC-WG5-001, insufficient:SC-WG5-006,
                                            # unrealized:ART-WG5-RUNNER, unrealized:ART-WG5-CLI,
                                            # unrealized:ART-WG5-REPORT, insufficient:SC-WG5-005
$ aes plan validate proposal-runner.yaml    # first draft
error: proposal PLAN-WG5-RUNNER: 2 violation(s):
  - evidence requirement 'ER-WG5-007-01' (criterion 'SC-WG5-007') has no route: no verification subject names it in evidence_requirement_refs and external_boundaries does not list it
  - closes_gaps[2] 'insufficient:SC-WG5-003' is not an open gap in the current reconciliation (open: insufficient:SC-WG5-001, insufficient:SC-WG5-006, unrealized:ART-WG5-RUNNER, unrealized:ART-WG5-CLI, unrealized:ART-WG5-REPORT, insufficient:SC-WG5-005)
$ aes plan validate proposal-runner.yaml    # + VS-WG5-RUNNER-FAIL-STOP, SC-WG5-003 dropped
OK proposal PLAN-WG5-RUNNER: 3 addition(s), 1 change(s)
  closes: unrealized:ART-WG5-RUNNER, unrealized:ART-WG5-CLI
  resulting target: success_criteria=7 evidence_requirements=13 verification_subjects=13 external_boundaries=0; every evidence requirement has a route
$ aes plan accept proposal-runner.yaml
accepted at a620cdc53dc133686bcb2163e781d5dde89d01aa
  changed components CMP-WG5-RUNNER
  added success_criteria SC-WG5-007
  added planned_artifacts ART-WG5-TEST-RUNNER
  added verification_subjects VS-WG5-RUNNER-FAIL-STOP
  updated .aes/target.yaml
  wrote .aes/plans/PLAN-WG5-RUNNER.yaml
$ git diff --stat    # first run: .aes/target.yaml 44 insertions, 8 deletions (item 1 below);
                     # clone reset, re-accepted with the fix: 30 insertions, 1 deletion (the changed refs line)
$ aes target validate                       # OK ... success_criteria=7 evidence_requirements=13 planned_artifacts=15 verification_subjects=13
$ git add .aes/target.yaml .aes/plans && git commit -m "Plan PLAN-WG5-RUNNER"
$ aes status
OK status: whygame5-target at 83c358f6a7750c9e189c71fec02344c636443e49
  artifacts: 11 realized, 4 unrealized, 0 drifted; 0 orphan(s)
  criteria: 3 supported, 4 insufficient, 0 refuted; 0 unsupported evidence requirement(s) with no route
  observations: 10 current, 4 stale, 1 unknown
    CMP-WG5-RUNNER: unrealized ART-WG5-RUNNER - src/whygame5/runner.py: planned, no file at HEAD (+3 more)
    CMP-WG5-ONTOLOGY: insufficient SC-WG5-006 - ...; ER-WG5-006-04 NO_CURRENT_SUPPORT; ER-WG5-006-05 NO_CURRENT_SUPPORT
$ aes plan accept proposal-runner.yaml      # again
error: proposal PLAN-WG5-RUNNER: 1 violation(s):
  - .aes/plans/PLAN-WG5-RUNNER.yaml already exists; a plan id is accepted once
```

The first draft's two mistakes were written deliberately to exercise the
refusal on the real consumer (the missing verification subject is the
SC-GF-004 case; SC-WG5-003 is SUPPORTED, the runner's call-count property
already has a route through `tests/test_evaluator.py`). The accepted proposal
is `tests/greenfield/fixtures/whygame5-proposal-runner.yaml`.

1. **The first acceptance rewrapped the consumer's target.** ruamel's default
   width of 80-100 refolded every long plain scalar in `.aes/target.yaml`
   (four component responsibilities, one purpose), and the blank line before
   `components:` stayed on the old last criterion. 44 insertions and 8
   deletions for a 1-line change. Fixed in this phase (width 4096; trailing
   comment moved) and pinned by the test that the fixture accept removes
   exactly one line. Only a real target with long one-line scalars showed it.
2. **A target change stales AES's own observations on the consumer.**
   `OBS-WG5-RECONCILE-73fc0ad7` lists `.aes/target.yaml` as a dependency, so
   the accept commit made it STALE and ER-WG5-006-05 lost support (current
   11 → 10, stale 3 → 4). That is the rule working: the observation was about
   the old target. It means every accepted plan re-opens the consumer's
   "AES works here" requirements until they are re-recorded; the protocol
   says so.
3. The whole-target route rule already holds on whygame5 (0 unrouted before
   and after), because whygame5 routes its human and live-run requirements
   through verification subjects with `external:` locators. The new
   `external_boundaries` family is not used by any consumer yet.

Not done in this phase: the plan is not yet accepted on the real whygame5
(the orchestrator applies the fixture), and the roadmap's exit gate, the
consumer's pre-commit hook rejecting a commit that adds a planned artifact
whose criterion has no route, is not built: `aes hooks install` still runs only
`aes target validate` and `aes topology check`, and the route rule lives in
`aes plan validate`.

Decisions:

- **Gap ids are `<kind>:<ref>`**, computed on reconcile's `Gap`. The kind is
  in the id so a proposal written against an insufficient criterion stops
  validating if the criterion is refuted before acceptance. Wrong-when: valid
  plans are repeatedly re-edited only because a gap changed kind between
  prepare and accept.
- **A proposal is add + whole-entry change, not a patch language and not
  "edit target.yaml under version control"** (`16-record-shapes` plan_record
  preferred the latter). The roadmap requires acceptance from the delta and
  the gap ids alone, and whole-entry replacement needs no path syntax.
  Wrong-when: real proposals need a `remove` or a field-level edit often
  enough that the target is hand-edited after acceptance (the roadmap's own
  wrong-when for this phase).
- **The route rule covers the whole resulting target, not only new entries.**
  Wrong-when: a consumer cannot accept an unrelated plan because an old
  requirement it cannot yet route blocks it.
- **Two route forms: a verification subject (with an `external:` locator for
  humans and live runs, as whygame5 does) or an `external_boundaries` entry.**
  Wrong-when: a consumer uses both for the same kind of requirement and
  readers cannot tell which is intended; then drop one.
- **`closes_gaps` may be empty** (a pure extension, e.g. the first plan after
  `aes init`, whose target has no gaps). Wrong-when: plans with empty
  `closes_gaps` are accepted on targets that have open gaps, i.e. plans stop
  naming what they are for.
- **The plan file is `<plans_root>/<proposal_id>.yaml`**, not
  `PLAN-<id>.yaml` as `16-record-shapes` sketched; the id is whatever the
  author chose, with a file-name-safe pattern. Wrong-when: two consumers'
  plan ids collide in a shared review surface for want of a prefix.

## 16. Evidence fixes: entry-level target dependencies, negative controls, running-code producer, routed-ER gate (2026-09-25)

Roadmap phase 6a (`25-roadmap-to-mvp-acceptance.md`): three evidence-model
kinks the consumer exposed, and phase 5's unmet exit gate, fixed before AES
records evidence about itself. Realized:

- **Entry-level target dependencies** (`evidence.py`). An observation may carry
  `dependency_target_refs: [ids]`. For each, the id's whole entry (a criterion
  with its nested evidence requirements, a verification subject, an artifact,
  ...) is taken from `git show <rev>:<target_path>` loaded strictly, serialized
  as canonical JSON, and compared between the observed revision and HEAD:
  changed or gone at HEAD is STALE, unchanged is CURRENT whatever else changed
  in the file. An id absent at the observed revision fails loudly.
  `dependency_paths` keeps real files; `.aes/target.yaml` listed there is the
  coarse form and keeps file-level staleness. No existing record is rewritten.
  `aes evidence record` now writes `dependency_target_refs` = the verification
  subject, the evidence requirements it assesses, and every planned artifact
  whose path is among the dependency paths, and refuses while the target has
  uncommitted changes (the refs name entries as committed).
- **Negative controls** (`evidence.py`). Optional `control: {kind: negative,
  base_revision, mutation, expected_outcome: detected, observed_outcome:
  detected|missed}`. Freshness is computed from `base_revision` (the unmodified
  commit the mutation was made from), which must be on a branch (local or
  remote-tracking) and an ancestor of `subject_revision`; `subject_revision`
  may be on no branch as long as it resolves. The load rejects `detected` with
  a result whose `exit_code` is 0 (the tool passed the mutated revision) and
  any assessment the outcome does not allow: `detected` permits SUPPORTS or
  INCONCLUSIVE, `missed` permits only REFUTES, so a control that failed
  refutes its requirement instead of supporting it.
- **Producer version from the running code** (`characterize.running_version`).
  Characterize, reconcile (which reuses characterize's producer), the
  `aes evidence record` observer/assessor and `aes --version` now report the
  installed distribution version plus ` (running: <git describe --always
  --dirty>)` when the executing module file is tracked by a Git checkout, the
  installed version alone otherwise (a venv's site-packages inside a consumer
  checkout is not tracked by it, so the consumer's commit is never reported as
  AES's), `not installed (running: ...)` without a distribution, and an error
  when neither exists. From this branch's worktree:
  `0.1.dev371+g4979c9df8 (running: 4979c9d-dirty)` while uncommitted; the
  metadata part is still the main checkout's install, the running part is the
  worktree's. `aes evidence record` used to write `unknown` when not installed;
  it now fails.
- **Routed-ER gate** (`cli.py`, `planning.route_violations`). `aes target
  validate` applies the whole-target SC-GF-004 rule `aes plan validate` already
  applied to a resulting target, printing each unrouted evidence requirement
  and exiting 1. The hook `aes hooks install` writes runs `aes target
  validate`, so it now refuses a commit whose target has a criterion with no
  route. No `--allow-unrouted`: the getting-started flow writes criteria and
  their verification subjects in one proposal, and whygame5 has 0 unrouted.

Evidence: `tests/greenfield/test_evidence_controls.py` (13 tests: the recorder's
refs and dirty-target refusal; an unrelated target edit keeps an entry
dependency CURRENT while the coarse form goes STALE on the same edit; an edited
and a removed referenced entry each stale it; an absent ref and a duplicate ref
are loud; a mutated revision is STALE without `control` and CURRENT with it,
then STALE for its real dependency; `missed` + SUPPORTS rejected, `missed` +
REFUTES makes the requirement REFUTED; exit 0 + `detected` rejected; a base on
no branch and a base that is not the mutation's ancestor rejected);
`test_characterize.py` (three running-version tests on a main checkout plus a
linked worktree one commit ahead, a consumer checkout with an untracked venv
module, and a plain directory); `test_distribution.py` (the hook refuses a
commit adding an unrouted criterion, then admits it with an external boundary;
`aes --version` names the running checkout). The getting-started flow
(`docs/greenfield/GETTING_STARTED.md` §1-§6) was re-run with this branch's code
on PATH: every step passes, the observation carries `dependency_target_refs:
[VS-GREET, ER-001-01, ART-PKG, ART-TEST-GREET]`, `aes status` SC-001 SUPPORTED.

What the consumer showed. On the real whygame5 at `36b64ed` (read-only),
`aes status` with the pinned AES and with this branch are byte-identical, and so
is `aes evidence status`:

```text
  criteria: 3 supported, 4 insufficient, 0 refuted; 0 unsupported evidence requirement(s) with no route
  observations: 10 current, 4 stale, 1 unknown
```

`aes target validate` on it passes with the route line. In a copy of whygame5
(`cp -a`), `OBS-WG5-RECONCILE-73fc0ad7` was rewritten to
`dependency_target_refs: [VS-WG5-AES-RECONCILE, ER-WG5-006-05]` (no paths),
`OBS-WG5-CHARACTERIZE-4921a159` to `dependency_paths: [src/whygame5/ontology.py]`
+ `dependency_target_refs: [VS-WG5-AES-CHARACTERIZE, ER-WG5-006-04,
ART-WG5-ONTOLOGY]` (the ontology entry holds the `exports` commitment), and
`OBS-WG5-DRIFT-b0c3e24f` to the same plus `control:` with `base_revision:
4921a159b546dbc34bf179548224462dbe22b15a` (on `origin/aes-phase3-pin`, the
drift commit's parent), `observed_outcome: detected`:

```text
== before (copy at 36b64ed, unmodified records)
    ER-WG5-006-04: NO_CURRENT_SUPPORT - OBS-WG5-CHARACTERIZE-4921a159 SUPPORTS (STALE); OBS-WG5-DRIFT-b0c3e24f SUPPORTS (STALE)
    ER-WG5-006-05: NO_CURRENT_SUPPORT - OBS-WG5-RECONCILE-73fc0ad7 SUPPORTS (STALE)
    OBS-WG5-CHARACTERIZE-4921a159: STALE - changed since observed: .aes/target.yaml
    OBS-WG5-DRIFT-b0c3e24f: STALE - changed since observed: .aes/target.yaml, src/whygame5/ontology.py
    OBS-WG5-RECONCILE-73fc0ad7: STALE - changed since observed: .aes/target.yaml
== after rewrite, at HEAD
    ER-WG5-006-04: SUPPORTED - supported by OBS-WG5-CHARACTERIZE-4921a159, OBS-WG5-DRIFT-b0c3e24f
    ER-WG5-006-05: SUPPORTED - supported by OBS-WG5-RECONCILE-73fc0ad7
    OBS-WG5-CHARACTERIZE-4921a159: CURRENT - no dependency or target entry changed since 4921a159b546
    OBS-WG5-DRIFT-b0c3e24f: CURRENT - negative control of 4921a159b546: no dependency or target entry changed since 4921a159b546
    OBS-WG5-RECONCILE-73fc0ad7: CURRENT - no dependency or target entry changed since 73fc0ad713c7
  observations: 13 current, 1 stale, 1 unknown
== commit editing ER-WG5-006-05's text
    OBS-WG5-CHARACTERIZE-4921a159: CURRENT - no dependency or target entry changed since 4921a159b546
    OBS-WG5-DRIFT-b0c3e24f: CURRENT - negative control of 4921a159b546: no dependency or target entry changed since 4921a159b546
    OBS-WG5-RECONCILE-73fc0ad7: STALE - target entries changed since observed: ER-WG5-006-05
== then a commit dropping WhyChain from ART-WG5-ONTOLOGY's exports
    OBS-WG5-CHARACTERIZE-4921a159: STALE - target entries changed since observed: ART-WG5-ONTOLOGY
    OBS-WG5-DRIFT-b0c3e24f: STALE - negative control of 4921a159b546: target entries changed since observed: ART-WG5-ONTOLOGY
== instead (from the rewrite commit), a commit appending a comment to src/whygame5/ontology.py
    OBS-WG5-CHARACTERIZE-4921a159: STALE - changed since observed: src/whygame5/ontology.py
    OBS-WG5-DRIFT-b0c3e24f: STALE - negative control of 4921a159b546: changed since observed: src/whygame5/ontology.py
```

1. **The three AES observations are CURRENT at the consumer's HEAD again**,
   although `.aes/target.yaml` changed twice since they were made (the
   `ER-WG5-006-05` addition and the `PLAN-WG5-RUNNER` accept). The edit to
   `ER-WG5-006-05` staled only the reconcile observation, which is exactly
   §15 item 2 no longer happening to the characterize one. With the rewrite,
   the stale count's permanent drift entry (§14 item 2) is gone: the only
   remaining STALE is `OBS-WG5-006-CHAIN-FIT-1`, stale for real reasons.
2. **The copy's hook ran the old AES.** Its `.githooks/pre-commit` names the
   real whygame5 checkout's `.venv/bin/python` by absolute path (the pinned AES,
   `4979c9d`), so committing the rewritten records in the copy used that; the target and topology checks do not load
   observations, so the new fields did not trip it. A consumer that bumps its
   pin before rewriting records needs no special order.
3. **The reconcile observation's real dependency is wider than any entry.** Its
   stdout depends on every entry, every governed file and every observation;
   the refs name only what its assessment claims (the subject and
   ER-WG5-006-05). This is a judgement the recorder of a hand-written
   observation now makes explicitly instead of by listing the whole file.

Not done in this phase: whygame5's real records are unchanged (a consumer
change, for the orchestrator: the rewrite above is three small YAML edits);
characterize and reconcile still have no `record` command, so their
observations remain hand-written.

Decisions:

- **An entry is the id's whole mapping, compared after a strict load.** Formatting,
  comments and key order are not changes; a nested evidence requirement's edit
  changes its criterion's entry as well as its own. Wrong-when: an observation
  that references a criterion goes STALE on whygame5 because a sibling
  requirement under the same criterion was edited; then reference the
  requirement, not the criterion, or compare criteria without their nested list.
- **A target that does not load strictly at an observed revision is an error,
  not STALE.** Wrong-when: a schema change in AES makes historical targets
  unloadable and `aes status` fails on a consumer for records nobody can fix;
  then load historical targets structurally only.
- **The recorder names the subject, its requirements and the artifacts among
  its dependency paths**, not criteria, normative items or components.
  Wrong-when: a recorded SUPPORTS stays CURRENT after its criterion's
  statement or disproof is changed in a way that makes the old test
  insufficient; then add the owning criterion.
- **The negative control's base must be an ancestor of its mutated revision and
  on some branch (remote-tracking counts).** whygame5's base is only on
  `origin/aes-phase3-pin` (the PR was squash-merged), so requiring an ancestor
  of HEAD would have rejected the real case. Wrong-when: a control's base branch
  is deleted and `aes status` fails on the consumer; then accept a tag, as the
  mutated commit already is kept alive by one.
- **Outcome fields live inside `control:`**, not at the observation's top
  level, so only controls carry them. Wrong-when: a positive observation needs
  expected/observed outcomes too.
- **The running version is `git describe` of the checkout that tracks the
  executing module**, appended to the metadata version, rather than replacing
  it. Wrong-when: a consumer-side record reports a `running:` part that is not
  the AES commit that ran (e.g. AES vendored into a consumer's tracked tree);
  then require the checkout's remote to be AES's.
- **`aes target validate` enforces routes with no escape flag.** Wrong-when: a
  consumer needs to commit a criterion before its verification subject exists
  (the route rule blocks incremental target authoring); then add
  `--allow-unrouted` to the hook, not remove the rule.

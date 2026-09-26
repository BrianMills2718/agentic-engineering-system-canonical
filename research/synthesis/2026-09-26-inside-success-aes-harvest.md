# Harvest: ideas worth borrowing from `Inside-Success/agentic-engineering-system`

Status: research synthesis, non-normative. Written 2026-09-26 for
[Decision 0011](../../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md),
which archives the predecessor repository. Nothing here is adopted by being
listed. Each item enters v0.2 only through the donor re-entry rule
(`proposals/aes-v0.2-greenfield/05-donor-reentry.md`) and `aes plan`, and only
when its **trigger** is observed on a real consumer.

Source repository: `Inside-Success/agentic-engineering-system` at `2933636`
(branch `plan-16-unified-aes-runtime`; `main` at `d7a5c0b`). Local checkout
`/home/brian/code/agentic-engineering-system`. Paths below are relative to it.
Three read-only sweeps produced this: decisions and topics, plans, and
code/evidence/reviews. Every cited path was checked to exist on 2026-09-26.

## How to read the status column

- **observed** — ran on a real consumer with retained evidence (path given).
- **tested** — unit or fixture tests only; never on a real consumer.
- **design** — written, acceptance boxes unchecked, no behavioural evidence.

v0.2 already has: revision-bound observations with STALE/UNREACHABLE/superseded,
negative controls, the no-orphan topology rule, `aes plan prepare/validate/accept`,
a pre-commit hook with worktree-safe interpreter lookup (`hooks.py`; do not
port the old one), Git-derived versioning, and a context packet. v0.2 has no
execution, orchestration, policy engine, agent-client hook, or learning loop.
Those are the gaps the items below sit against.

## A. Ideas, grouped by the v0.2 gap they address

### A1. Execution and orchestration (v0.2 has none)

| # | Idea | Source | Status | Trigger to adopt |
| --- | --- | --- | --- | --- |
| 1 | **Bounded supervisor**: coordinator plus depth-one leaves that cannot delegate; parent verifies independently; one recovery without duplicate mutation; needs-human deduplicated to one Inbox row; an orchestrated result cannot accept itself. Borrow the invariants, not the ~3k lines. | `docs/decisions/0015-portable-native-orchestration-adapter.md`; `src/aes/orchestration/supervisor.py` (1,937 lines), `state.py`, `contracts.py`; `docs/plans/13_portable_orchestrator_spine.md` | observed: `evidence/orchestration/plan13/` (clean environment B from an exact wheel, one real README task) | v0.2 decides to run work rather than only record evidence about it. |
| 2 | **Native adapters** for Codex app-server and Claude Code (`claude -p` stream-json, AES-issued session id, `--resume`, SIGKILL only, bearer-protected loopback MCP). | `src/aes/orchestration/native_codex.py` (705), `native_claude.py` (461), `local_mcp.py` (206) | tested; Codex runs observed under Plan 13; Claude accepted in `evidence/orchestration/claude-code/ACCEPTANCE.md`. Depends on undocumented Claude Code 2.1.270 shapes. | Item 1 is adopted and needs a specific harness. Re-verify shapes against the current client first. |
| 3 | **Context refresh lifecycle**: checkpoint persisted before compact or fresh-thread; each refresh opens an epoch; expected, emitted and acknowledged context recorded separately; writes refused from a stale epoch. | `docs/plans/14_context_refresh_lifecycle.md`; `src/aes/orchestration/context_refresh.py` (348) | observed: `evidence/orchestration/plan14/ACCEPTANCE.md` (with `--inject-defect` control; Codex only) | A v0.2-governed session exceeds its context window mid-task and required context is lost. |
| 4 | **Run record with terminal state**: goal verbatim, revisions before/after, terminal state `DELIVERED / LEARNED / REASSESS / HUMAN`, interventions list where empty is an explicit claim, mechanisms observed vs unobserved. | `docs/plans/08_one-consumer-run-one-lesson-that-binds.md`; `evidence/runs/plan08/run-01/run-record.json`; `docs/decisions/0008-...` items 5-7 | observed (one run) | v0.2 first governs a real coding goal end to end and must show which component touched the run; or `aes plan` needs "this item ended without delivering". |
| 5 | **A named legal move at an unattended boundary**: do other authorized work, state the blocker once, leave a durable addressed pause; if a required probe cannot run, label the claim unverified rather than substitute a proxy. | `docs/decisions/0010-v3-salvage-inventory.md` ("The dead end") | design (lesson) | v0.2 supports any unattended run, or a plan item hits a human-only decision mid-run. |
| 6 | **Plans carry their own interrupts** (audit, review, context-clear triggers belong to the plan, because "detecting one's own drift requires the judgement that drifted"). | `docs/decisions/0006-the-mission-in-the-owners-terms.md` items 3-4 | design | A consumer runs a long plan and the agent succeeds at the wrong thing without anyone noticing. |
| 7 | **Route-crossing declaration**: a session with live claims in more than one repository names the crossing once with a reason; unreadable registry gives NOT_CHECKED. | `docs/topics/route-boundary.md` (AES-INV-005); `route-crossings.yaml` | tested; motivated by a real scope-drift incident | A v0.2-governed session mutates two or more consumer repositories in one run. |

### A2. Policy admission and the assertion-evidence gate (v0.2 blocks only at pre-commit, with no recovery contract)

| # | Idea | Source | Status | Trigger to adopt |
| --- | --- | --- | --- | --- |
| 8 | **BLOCK → bounded recovery → ALLOW, and proof before a check may block**: every admission is exactly ALLOW, BLOCK or ERROR with a stable reason code; ERROR, timeout and NOT_CHECKED never become ALLOW; every BLOCK names a runnable recovery or the exact authority boundary; a check becomes blocking only with an executable observer, a realistic negative control, observed client wiring, an evidence surface, and results measured before blocking. Zero blocking policies is an honest baseline. | `docs/topics/policy-admission.md` (AES-POL-001..006); `src/agentic_engineering/engine.py` (199); `docs/plans/10_...md` S4 | observed: `evidence/runs/2026-08-24-whygame-coherent-loop-adoption.json` (BLOCK→recovery→ALLOW on the same revision and request); `evidence/propagation/2026-09-09-plan-10-s4-governed-loop.json` | A v0.2 hook block leaves an agent stuck or leads it to bypass the hook; or a consumer wants an evidence requirement to gate something beyond commit. |
| 9 | **Assertion-evidence gate**: a Stop-hook judge refuses a turn that claims a verification nothing in the turn ran; passes without a model call when something ran. | `src/aes/assertion_evidence_gate.py` (789), `install_assertion_evidence_gate.py` (217); `scripts/check_gate_reaches_judgement.py` | observed: installed in `whygame-reboot/.claude/settings.json`; `evidence/propagation/2026-09-06-consumer-status.md` | A v0.2 consumer's agent claims verification that `.aes/observations/` does not back. This is the single most-used mechanism the old repository shipped. |
| 10 | **Agent-client hook lifecycle** `aes coding install / check / remove` with states REGISTERED, NOT_CHECKED, OBSERVED, REMOVED, UNAVAILABLE, each with a remedy command; registers beside the consumer's own hooks. | `src/aes/coding.py` (598) | observed: fresh-clone journey and three cold-reader rounds in `evidence/propagation/2026-09-15-teammate-install-probe/` | v0.2 ships an agent-client hook in addition to the git hook. |
| 11 | **Configurable "control unavailable" policy and claim-to-evidence support records**: each control declares `BLOCK`, `NOT_CHECKED_AND_CONTINUE` or `DISABLED`; a missing policy cannot silently disable a critical control; a verification claim must name evidence of a compatible class, "the turn executed something" is not blanket support. | `docs/plans/16_one_installed_aes_runtime.md` S2, S3; `docs/plans/11_...md` (`judge_unavailable`) | design | A v0.2 checker can fail to run (missing dependency, unavailable judge), or one command is cited as evidence for several claims. |
| 12 | **Operating evidence**: a control is "operating" only if the file the runtime executes matches the default branch byte for byte; a repository's declared verification must be reachable from the pre-commit path Git actually uses. | `docs/topics/deployed-controls.md` (AES-INV-002); `docs/topics/verification-at-the-commit.md` (AES-INV-004); `src/aes/verification_at_the_commit.py`; `scripts/check_deployed_controls.py` | tested; motivated by a real false "enforced" report | v0.2 installs a hook into a consumer and claims it is in force; or a consumer commits over a red tree. |

### A3. Rules, normative items and the learning loop (v0.2 has normative items but no exception discipline and no lesson-to-check path)

| # | Idea | Source | Status | Trigger to adopt |
| --- | --- | --- | --- | --- |
| 13 | **A rule and its exceptions are one object**: every rule declares `unless:` (empty means "absolute", not "omitted"); each exception carries `authority: quoted \| authored-here`; quoted text is checked against its source; every rule needs a counter-case where it does not fire; two rules claiming the same position must resolve the collision. Caught a live contradiction (both rules pointed at an `Answer` field that did not exist). | `docs/topics/declared-rule-shape.md` (AES-INV-003); `docs/plans/0.7-portable-rule-implementation.md`; `src/aes/rules.py` (590); `scripts/check_rule_conflicts.py` | observed on AES's own 12 rules; measured limits recorded in `evidence/runs/plan0.7-rule-shape/measured-limits-of-the-checks.md` | A v0.2 target holds two or more normative items that could conflict, or an item is restated from a user's own words. |
| 14 | **Instruction surface generated from the rulebook** with a regeneration-equality check that fails on hand edits, including softened wording. | `src/aes/instruction_surface.py`; `scripts/render_instruction_surface.py --check` | observed (positive control plus injected drift) | v0.2 needs to project normative items into an agent-read file (AGENTS.md / CLAUDE.md) in a consumer. |
| 15 | **Lesson-to-check promotion with four observations**: a lesson qualifies only if it recurs and names something runnable; the check is observed red on the target case, green on a nearby legitimate case, with a runnable recovery, and the identical retry allowed; exit codes 0/1/2 where 2 is "could not run". Staged contract: retain, fix locally, aggregate frequency, generalize, observe the intervention catching the class, then promote. | `docs/plans/08_...md` S2 (`AES-INV-004`); `docs/plans/11_...md` S3; `docs/plans/16_...md` "Failure Learning Contract"; worked examples `docs/topics/status-fallthrough-guards-its-data.md`, `source-system-binding.md` | observed once, human-driven; unattended form is design | The same failure appears in two or more v0.2 consumer runs and could be caught by a command. |
| 16 | **Governance record reader**: one session id in, one run record out, joining hook receipts and pre-write events; unobservable facts are `NOT_CHECKED`, never blank. Its first reading found two controls failing at scale for days. | `docs/plans/09_read-the-governance-record-that-already-exists.md`; `scripts/build_run_record.py`; `evidence/runs/plan09/reading-01.md` | observed | A v0.2 control has produced roughly 100 or more receipts on a real consumer, or a user asks what AES actually did during a session. |
| 17 | **GSD-style target checks**: `gap-analysis` (every requirement id cross-checked against plan bodies) and `assumption-delta` (fires when something singular, required or derived becomes plural, optional or chosen). | `docs/decisions/0011-gsd-core-is-a-source-of-ideas-not-a-foundation.md` | design | `.aes/target.yaml` normative items outgrow a hand check. |

### A4. Delegation and routing (v0.2 records no executor choice)

| # | Idea | Source | Status | Trigger to adopt |
| --- | --- | --- | --- | --- |
| 18 | **DelegationDecision record**: one strict record at the planning-to-execution handoff with observed factors, prior-art dispositions, selected executor roles, rejected alternatives, rationale, and outcome refs added later; "selected" has no outcome, "completed" must reference execution and verification evidence; no scoring or router until accumulated real records justify one. | `docs/decisions/0014-adaptive-delegation-is-an-observed-decision-not-a-router.md`; `src/aes/delegation.py` (96) | tested | A consumer delegates one plan item to a subagent or another harness and someone later asks why it was allocated that way. |
| 19 | **Evidence-driven escalation tiers** (`economy / balanced / strongest_available`, mapped per instance, recorded per run; escalation on failed focused checks, ambiguity, cross-boundary conflict, repeated repair) and **failure-class-separated routing feedback** (model quality separate from transport, infrastructure, authority, verification). A routing change is a proposal until 3 or more comparable verified observations exist. | `docs/decisions/0015-...` items 5, 7, 12; `docs/plans/13_...md` P13-W11/W12 | observed: the honest result was zero comparable groups, `routing_policy_change = none`, costs unobserved | v0.2 records more than one model tier doing the same kind of work, or makes any cost claim. |

### A5. Distribution and portability beyond one machine (a v0.2 non-claim)

| # | Idea | Source | Status | Trigger to adopt |
| --- | --- | --- | --- | --- |
| 20 | **Portable-controls scan**: forbid absolute or home-relative paths in shipped controls; exceptions need `# portable-exception: <reason>`, a bare marker is still a violation; every check names the data source it read. First run found 14 machine-specific paths. | `docs/topics/portable-controls.md` (AES-INV-006); `scripts/check_portable_controls.py` (225); `docs/decisions/0012-portable-configurable-shareable.md` | observed: `evidence/clean-clone/2026-09-06-first-run.md` | The first v0.2 install outside `~/code`, or a second user. |
| 21 | **Profile export/import** carrying only an allowlist of logical configuration and exact component hashes, never paths, credentials, receipts or machine state; environment B supplies its own bindings; readiness checks the dependency the configured route actually needs and names the exact fix. | `docs/plans/10_...md` S3-S5A; `evidence/propagation/2026-09-09-plan-10-s5a-installed-profile.json` | observed (S5A); the clean-B native journey (S5B) was never observed | A second machine or user installs v0.2 for an existing consumer. |
| 22 | **Consumer status**: pinned revision, commits behind, which controls are importable, which are AES-only by design. Found three consumers 258 to 276 commits behind and six of nine controls stranded in `scripts/` (which never ships). | `src/aes/status.py` (430), `controls.py`; `evidence/propagation/2026-09-06-consumer-status.md` | observed on three consumers | More than one consumer pins v0.2 and they drift. |

### A6. Measurement and audit (v0.2's declared gap: value beyond mechanism)

| # | Idea | Source | Status | Trigger to adopt |
| --- | --- | --- | --- | --- |
| 23 | **Consumer-generalization baseline read from Git**: two declared anchor commits per consumer (bootstrap, outcome); hours to outcome, commits, authority bytes, bootstrap weight; anything Git cannot measure is `unobserved` with its route; a bad anchor errors, never zero. Its own correction: elapsed hours are not comparable across bootstraps that differ 500x, and mixing working-tree with revision reads produced a false finding. | `docs/plans/0.5-gate-3-generalization-measurement.md`; `src/agentic_engineering/generalization.py` (493); `evidence/runs/2026-08-24-consumer-generalization-baseline.json` | observed on three reboots | A second consumer reaches an accepted outcome under v0.2 and someone asks whether v0.2 made it cheaper. Pair with Decision 0011 item 5's value measure. |
| 24 | **Claim audit and repair loop**: hash-bound anchors re-checked mechanically (4,965 of 4,965), two independent leaves judge each claim (`supported / overstated / contradicted / unanchored`) without seeing each other, a reviser narrows or drops disputed claims, bounded rounds. | `docs/plans/15_claim_audit_journey.md`; `src/aes/orchestration/claim_audit.py`, `audit_supervisor.py`, `audit_repair.py`; `evidence/orchestration/claim-audit/` | observed on qualitative-coding output; verdicts varied between runs; acceptance boxes unchecked | A v0.2 consumer produces prose claims anchored to sources (a report or analysis), and `evidence`/`reconcile` need semantic rather than structural verification. |
| 25 | **Fresh-agent resume-quality verifier**: a context-blind reviewer cites consumer bytes; AES checks the citations against Git at an exact revision with a prompt digest. | `docs/plans/0.6-agent-ecology-resume-quality.md`; `src/agentic_engineering/resume_quality.py` (205) | tested, provider-free; the real review was never run | v0.2's context packet A/B is re-run on a consumer large enough for orientation to cost something (Decision 0010, ER-SC-GF-005-02 wrong-when). |

### A7. Small check ideas worth keeping (from `Makefile`, `hooks/`, `scripts/`)

- Clear `__pycache__` before trusting a green mutation run; stale bytecode once passed with the guard removed (`hooks/pre-commit`).
- A mutation harness must fail when the mutation left the file unchanged; a no-op mutation looks exactly like "the guard does not bind" (`scripts/mutate.py`).
- AES must pass every control it ships to consumers (`scripts/check_self_application.py`). v0.2 already does this for its own target; keep it as the rule when controls are added.
- State selection must not fall through to "healthy" when there is no data; zero data reads as zero problems (`scripts/check_status_fallthrough.py`).
- Every generated file has a `--check` step that something actually runs; every declared coupling resolves to an existing file, because silent renames produce no error (`scripts/check_couplings.py`).
- The sanctioned route must need fewer blanks than the escape hatch. Five required fields versus a one-variable bypass led to the bypass being used six times in one session (`Makefile`, `maintenance-worktree`).
- Audits record whether each finding was already known; repeats recurred within hours (`docs/AUDITS.md` §Repeats).
- Wiki/topic projection (`src/aes/topic.py`, `couplings.py`) is **not** recommended for porting; v0.2's context packet covers the need unless a committed human-readable page is required.

## B. What the old repository recorded about why it stalled

These are the lessons Decision 0011's "wrong when" conditions are written against.

1. **Green checks, lost mission.** The rewrite dropped decisions 0001-0005 while CLAUDE.md still cited them; an agent reported the context mechanism as the mission and Brian corrected it from memory. The docs were "internally coherent and mechanically green, also incomplete." (`docs/decisions/0006-...`, `0003-...`)
2. **Framework outgrew consumer evidence.** `scripts/` went from 2.8k to 16k lines and `invariants.yaml` from 139 to 1,110 lines with no consumer evidence newer than 2026-08-24; authority bytes across reboots rose 7,456 → 23,644 → 138,886 while no measure could attribute anything to AES. Two package trees stayed live until Plan 16. (`docs/plans/08_...md` Gap; `0.5-...md`; `07_migration_gate_m0.md`)
3. **Direction churn.** Successor (0007) → staged migration (0008) → two shots (0009) → no forced convergence (0013), including a closed PR built on a premise then rejected, and a 0014/0016 decision-number collision.
4. **Implemented was reported as operating.** A gate was reported enforced, with negative controls, while the runtime executed a checkout on another branch. Declared controls nothing ran still reported PASS. (`docs/topics/deployed-controls.md`; `evidence/clean-clone/2026-09-06-first-run.md`)
5. **Portability failed by confident answers about someone else's data**, not by crashing: a clean clone's route check went green over 37 claims from another install; the run-record tool read another install's receipts; four controls written in one day by an agent that had read the mission all failed portability. (`docs/decisions/0012-...`)
6. **Receipts were written but never read.** 486,797 hook receipts and 20,280 pre-write events that no AES artifact had read; two controls failing at scale for days; a learnings register of 1,321 entries with zero promotions. (`docs/plans/09_...md`, `08_...md`)
7. **A number without provenance became a finding.** The "149/213 unjudged" rate came from test-session receipts; operational rates must exclude test and evaluation traffic by provenance tagged at write time. (`docs/plans/11_...md`)
8. **Judgement rewritten as procedure.** All eight extraction lanes over the 242-row registry found rules that had lost their conditions or gained escape hatches; 113 rows had no source anchor. Rules only ever pushed toward more checking, and none said when verification is enough. (`docs/decisions/0010-v3-salvage-inventory.md`)
9. **A promoted check is not a changed behaviour.** No rule was ever observed changing what an agent did; hook-backed requirements were followed 100% and unhooked ones 0%, so compliance reporting became ceremony. (`docs/plans/08_...md`, `0.7-...md`; `HANDOFF.md`)
10. **The demo ran without the gate.** A run read as "AES observes but rarely intervenes" turned out to be in the one repository where the pre-write gate was not wired; wired, it denied 143 writes against 275 allows. (`docs/plans/09_...md`)
11. **Cold readers could not install from the docs** even though the lifecycle existed: 17 gaps in round one, three rounds to pass. (`evidence/propagation/2026-09-15-teammate-install-probe/`)
12. **Provider-free milestones are not the MVP.** Plan 10's clean-B native journey stalled behind a zero-spend authorization and was never observed. (`docs/plans/10_...md`)
13. **Verifier variance is normal.** Claim-audit verdicts flipped between runs; a coordinator corrupted a relayed packet; SIGTERM re-sent in-flight MCP calls. Keep rejected attempts as evidence. (`evidence/orchestration/claim-audit/repair-r3/README.md`; `claude-code/ACCEPTANCE.md`)

## C. Not harvested on purpose

- Plan 16 (absorb Company Planning and Enforced Planning into one runtime): v0.2 re-derived that from a clean sheet; the plan is closed, not migrated.
- The `assessment*.py` composite assessments (~2.3k lines, Plan 249): Project Meta-specific.
- Wiki/topic projection and doc couplings: see A7.
- The worktree-safe hook interpreter lookup: v0.2 `hooks.py` already has it.
- The learnings register and audit ledger contents: they live in `project-meta/learnings/` and `docs/AUDITS.md`, still readable at the archived commit.

# Resume here: catalog upkeep and approved AES hook activation

Handoff: 2026-11-13 evening, at Brian's request to conserve usage.
Lineage: **candidate_branch**, not merged or deployment-certified.
Draft PR: https://github.com/BrianMills2718/agentic-engineering-system-canonical/pull/861
The remote main advanced to `8b34db885386543e260a7d3164ede04400305e85` after
this lane integrated `268d58e6c`; fetch and reconcile the latest upstream before
final shipping. The draft currently reports non-mergeable. Preserve other writers
and resolve inventory rows by source identity, then regenerate the catalog.

## Next action

Continue `feat/wiki-catalog-upkeep-20261114` in this retained worktree:
`/home/brian/code2/worktrees/aes-wiki-upkeep-20261114` (or create your own from
that pushed branch). Issue: AES #857. Architecture entry:
[DOCUMENTATION.md](../docs/architecture/DOCUMENTATION.md#ongoing-complete-file-catalog-upkeep),
then [system model](../docs/planning/SYSTEM_MODEL.md#complete-file-catalog-maintenance-2026-11-14).

**Already approved — do not ask Brian again:** “Enable and verify AES project
hooks”, including inherited shared guards/planning within AES, while global
settings and other projects stay unchanged. This is the written AES-only
exception to the earlier hook stop. Project declarations are staged in this
candidate; native default-session verification and exact Codex hook trust are
unfinished. No global settings, trust records, editors or running agents were
changed/restarted by this session.

## What is implemented and evidenced

- Existing native refresh now reports changed/added/removed catalog inputs,
  requests explicit source-bound semantic review, and renders navigation without
  approving meaning. Local checks read working bytes; pre-commit reads the index.
- Concrete edits route to their owning configured repository, including another
  worktree; one patch spanning several configured roots fails clearly. Opaque
  shell commands use their reported working directory or explicit `--repo`.
- 89 focused tests passed; targeted mypy passed both runtime modules. The bounded
  planning review passed at `09414e9b4cedc5954f81395e0d7a64710e635912`.
- The [native receipt](../evidence/runs/catalog-upkeep-native-20261114.json) and
  [stream](../evidence/runs/catalog-upkeep-native-20261114.jsonl) retain an explicit-
  settings Claude fixture: 26 events, one source change from one-shot search to
  a loop, explicit summary review, and 13 CLI refusal/recovery steps. Independent
  evidence and privacy reviews passed. Raw hook additional context is absent
  from that stream; delivery evidence and that limitation are explicit.
- Concurrent main changes through `268d58e6c` were integrated, including ecosystem
  documentation and array-fact projection. Preserve them. The complete inventory
  was semantically reconciled, not blindly rehashed.

## Finish in this order

1. Read current status and run `make check-catalog check-catalog-staged check-doc-facts`,
   instruction sync and the focused tests named in the receipt. The final
   checkpoint includes explicit reviews of its own handoff/config/helper inputs.
2. Confirm the pinned code `09414e9b4cedc5954f81395e0d7a64710e635912` is reachable
   remotely (it is an ancestor of this pushed branch). Run the full planning
   validator; its recorded code-review pin is already updated. Existing route
   WAIT, nightly A9 semantic coverage and repo-format Q17 remain scoped, not hidden.
3. Complete native activation verification and ship through `ship`. Codex resolves
   the hook definition through the **canonical checkout**, even for a worktree;
   until canonical main has this candidate's `.codex/config.toml` and hook pin,
   its native inventory still sees the old handler. Do not work around this with
   a trust bypass or claim normal execution from config. If verification needs
   post-merge canonical deployment, merge only the tested candidate with that
   verification explicitly pending, safely fast-forward a clean canonical checkout,
   and immediately perform the runtime verification/follow-up record.
4. Use the [prepared Codex helper](../evidence/runs/catalog-upkeep-codex-activation-20261114.py)
   only after reviewing its fixed paths and canonical source. It is compiled and
   statically checked, **not executed**. The command is `python3 <helper> --go
   --expected-sha 09414e9b4cedc5954f81395e0d7a64710e635912 --receipt <ignored-path>`.
   It uses installed app-server APIs, CAS on the current user-config version,
   trusts only the fresh exact canonical AES handler hash, and checks preservation
   of every other hook state and unrelated setting. User project trust already
   covers the AES directories. Never set the global hooks feature or trust old hashes.
5. Verify fresh ordinary Claude and Codex sessions with **no** explicit settings-
   source/feature/trust-bypass overrides. Give each native agent its own worktree.
   Claude supports `--include-hook-events`; retain the raw hook lifecycle/context
   where available. Capture effective handlers, source/hash, tool events and
   resulting summary changes. Inspect all failures and privacy-scan before publishing.
6. Update evidence, the current brain and affected wiki prose, record exact scope,
   refresh/review catalog inputs, complete relevant local checks and merge the
   final verified result. Close #857 only after the activation outcome is established.

## Retained state and limits

Only this branch is the integration lane. Earlier worker branches and applied
stashes are provenance/safety copies, not independent next work. Keep unmerged
lanes; no data/history was deleted. Ignored `.lockstep/` contains the disposable
native fixture and runtime originals; the durable receipt preserves its inputs,
outputs and probe traces. No native model job or activation helper is running.
The prepared helper's old worktree constant may be read as a retained test target;
review paths if resuming in another checkout.

The API/CLI parsing trap is real: quoted dotted `-c` keys containing filenames
split incorrectly. Use the helper's whole-object `config/batchWrite` API, not
invented CLI trust overrides. Other untrusted/disabled handlers must retain their
states. Current installation capabilities were inspected with Codex 0.169.0 and
Claude 2.1.323; re-check if versions change.

After this repair, concrete next investigations are ordinary-host delivery gaps,
edit-guard/installation findings and the original 263-policy reconciliation.
Do not turn those into a blanket claim that all explanatory wiki prose is
mechanically maintained or that policy effectiveness is established.

## Previous progress and dated records

# Complete-file wiki upkeep (2026-11-14, AES #857)

Catalog maintenance now reuses the native Lockstep refresh and the existing
inventory: changed/added/removed Git-index files require explicit summary review
bound to the observed source hash. Deterministic refresh renders navigation and
pending warnings without approving meaning. Local checks read working files;
pre-commit checks read indexed bytes. Existing unrelated hooks are preserved.

The [native observation](../evidence/runs/catalog-upkeep-native-20261114.json)
and [full trace](../evidence/runs/catalog-upkeep-native-20261114.jsonl) retain an
explicitly configured Claude changing a search-once fixture into a looping
generator and updating the summary after its hook requested review. Thirteen CLI
steps establish bypass refusal, stale-hash rejection and staged recovery.
Brian approved the AES-only project hook exception on 2026-11-13, including
inherited shared guards and planning hooks within AES. Project declarations are
configured; exact native handler trust and normal-session execution are being
verified. Global settings and other projects remain unchanged. Native Codex
execution and normal-session loading remain unobserved until that proof completes. Raw hook
additional context is not serialized in the native stream; the receipt states
which independent observations support delivery.

Next: verify ordinary client loading and address guard/install concerns, then
map the original policies to current authority and delivery. Q30's implemented
catalog portion is repaired; semantic correctness of all explanatory wiki prose
remains a review responsibility. Do not treat hash agreement as understanding.

## Earlier observations and dated records

# Ecosystem consolidation and first predecessor review (2026-11-13)

Tracking: [AES #856](https://github.com/BrianMills2718/agentic-engineering-system-canonical/issues/856).

Brian approved AES-owned ecosystem consolidation and asked to read older system
parts for the best ideas, concerns, inconsistencies and recommendations.
[Decision 0014](../docs/decisions/0014-ecosystem-consolidation-and-legacy-review.md)
records that direction. [The first source review](../docs/architecture/ECOSYSTEM.md)
compares the catalogue sources, contracts, dataset discovery, runtime tools and
legacy governance. Q36–Q42 extend the existing question ledger.

Next: compare the actual catalogue records/readers/writers and choose the discovery
publication provider; continue reading the concern/repair lifecycle, then selected
policy families and instruction delivery. Proposed donor dispositions are not
completed migration, runtime adoption or retirement. Earlier projection and
feedback work below remains independent and is preserved.

## Earlier implementation and assessment records

# AES projection self-adoption (2026-11-13, AES #854)

Implemented the narrow P-SELF route: root declarations, source-local authored
assessment/gaps/plan, two generated document targets, pinned PostToolUse hooks,
and a facts-only local/pre-commit gate. Existing commit policy is preserved.
The [self-adoption observation](../evidence/runs/projection-self-adoption-20261113.json)
and [full native trace](../evidence/runs/projection-native-20261113.jsonl) retain
one actual Claude Edit triggering both target updates. The invocation used the
existing API authentication route and explicitly loaded project settings after
an earlier attempt stopped before editing. Read-only stale refusal and recovery passed.

Next: discuss compact wiki views and remaining policy/implementation concerns.
The bounded Claude host path is observed; Codex configuration is present but
native Codex execution and blanket default-session loading are not claimed.
The authored assessment is separate from measured evidence. The all-file
inventory and catalog include the adopted configuration and retained runs.

## Earlier assessment and dated records

# Projection worked assessment (2026-11-13, AES #852)

The [worked assessment](../docs/architecture/LOCKSTEP.md#worked-assessment-the-projection-component)
uses the real projection component in a disposable consumer. Existing full-docstring
projection preserved authored current status, gap and plan sections alongside
normative text, refreshed two targets, refused a bypassed stale copy without writes,
and recovered. Six CLI steps matched expected exits; 26 focused tests passed.
The [run receipt](../evidence/runs/projection-worked-20261113.json) retains inputs,
outputs and trace events. A directly supplied edit event is not native-host proof.

Next recommendation: P-SELF and P-NATIVE in the assessment configure this existing
mechanism for AES itself and observe a real installed-client edit. This session
changed documentation and retained observations only; runtime self-adoption is
not claimed. Current-status narrative is agent-authored and remains distinct
from measured evidence. Prior choices remain the baseline; proposed revisions
must explain what they improve.

## Earlier completed coverage and dated records

# Complete file coverage (2026-11-13, AES #849)

**Completed in PR #850:** every one of 408 tracked files now has a source-grounded
summary and navigation route. The inventory records 22 findings and 12 grouped
consolidation recommendations; independent semantic review sampled 23 files.
Source identities matched 406/406 inputs, with the two self-output hashes
explicitly omitted. This is a dated snapshot, not continuous automatic refresh. The earlier 69-file
check covered a reader-Markdown subset, not this complete requirement.

Read [the complete catalog](../wiki/documents.md) and
[coverage/consolidation assessment](../docs/architecture/DOCUMENTATION.md#coverage-and-consolidation-assessment).
Planning is an explicit whole-system function, supplied by Company Planning;
Lockstep represents and checks its output. The
[policy source map](../wiki/policy-and-rules.md#where-are-the-hundreds-of-project-meta-policies)
now links the original 263-entry Project Meta registry and current shared rules.

**Next:** discuss recorded consolidation choices and the open
runtime concerns. Do not infer policy retirement, enable jobs, or alter code
because an inventory marks an item as a candidate. Current and historical
architecture, raw evidence, generated views, fixtures and instructions retain
separate authority. Earlier reading-path verification below is explicitly a
subset result, superseded for coverage by this complete-file review.

## Prior reading-path repair and dated evidence

# Now (2026-11-13)

**Documentation repair first (AES #847):** the current reading path is
[wiki/index.md](../wiki/index.md) → [goal](../docs/architecture/GOAL.md),
[Lockstep](../docs/architecture/LOCKSTEP.md),
[document roles](../docs/architecture/DOCUMENTATION.md), and
[feedback/policy](../docs/architecture/FEEDBACK_AND_POLICY.md).
The explanation restores the existing driver (autonomous effective coding agents),
planned behavioral structure and typed interfaces, full normative context at edits,
status projected upward, source-local normative edits and navigational summaries.
It distinguishes intention, implemented mechanisms, dated observations and history.

**Reading-path verification:** the independent reader answered 8/8 orientation
questions after four stale-route findings were repaired. The native link parser
reaches 69/69 reader documents within two links. The
[review receipt](../docs/planning/runs/orientation-reader-20261113.json) states the
scope: discoverability and comprehension, not runtime synchronization proof.

**Next:** discuss the [existing open-questions ledger](../wiki/open-questions.md)
after the reading-path repair. It includes synchronization proof, OpenSpec upward
edit parity, guard aggregation, installation evidence, collector reliability,
policy discovery and wiki freshness. These are recorded concerns, not changes
made or jobs enabled by this session. Implementation assessment resumes after this
orientation repair; do not infer that documenting a gap closes it.

**Current ownership:** AES comprises Lockstep, feedback and policy. The Hive
implementation is in personal-vps. The `aes` library remains for consumers;
this repository's own `.aes/` and claims machinery are retired. The older entries
below are dated history and are not instructions to revive them.

## Earlier dated records

# Now (2026-11-12; earlier sections dated)

**Source-local document upkeep:** the authorized Company Planning example adds
declared fact blocks to the existing Lockstep projector, including native
post-edit refresh and read-only stale checking. The contract and configuration
are linked from `wiki/lockstep.md`. Focused tests and fresh installed command
smokes cover lifecycle, descriptions, interfaces and JSON/YAML evidence;
Company Planning PR #301 delivered the paired reader at
https://hive.brianmills.dev/docs/company-planning/. Its retained observations cover
11/11 command cases, 2/2 fresh native fixtures, and both canonical Codex hooks
loaded, trusted and enabled. Three served reader pages were checked at merged SHA
`a0ee3c335f25c344b01de9992c661f7dba4d23f6`, with private gate checks.
This does not certify arbitrary narrative accuracy or all consumer rollout.

**Handoff (2026-11-12, end of the Claude lockstep session; Brian is switching to Codex):**

- Done today, all merged through `ship`: the AES cleanup #842 (884 files retired, record and restore command in [docs/retired/2026-11-12.md](../docs/retired/2026-11-12.md)); Lockstep users moved to this repository at `b0d4cbd17`: lifelike#7, and Team-Brains#1249, which the server session installed on the VPS. There, a job inside the plan went through and a job outside it was refused, with the list of allowed files; log `/srv/inside-success/logs/lockstep-retest-20261112.log`. The acceptance page (A1 to A5 pass) is `proposals/planning-package/review-page/lockstep-acceptance.html` on hive.brianmills.dev/plans.
- Waiting on Brian, Decision 5, what next: (A) feedback loop: the `feedback-problems`, `feedback-fix-owner` and `feedback-effects` timers are off, so filed reports are not turned into fixes or counted; (B) a lighter planning process (the planning package refused 3 merges on 2026-11-12); (C) more Lockstep users. Recommended A.
- Left on purpose: two old branches with unmerged work, both on GitHub: `docs/wiki-consolidation-1111` here, kept for comparison, and Team-Brains `lockstep-consumer-l7-20261107` (lane l7, ruled out 2026-11-10). 18 older unmerged branches from 2026-09-30 to 2026-10-10 are mostly about parts now retired; deleting them needs Brian's yes.
- Fixed at handoff: `lockstep check arch check` no longer fails a repository whose diagram maps no Python packages, and `lockstep init` writes the `brian` human-source default (`--human-pattern` sets another); both found by the code-88 session switching 9 repositories to Lockstep.
- Known loose ends: the `feedback-collector.service` Documentation link points at a retired file; `c-drive-guard` points at the retired `scripts/hive/board.sh`; the main checkout's `.venv` is stale, so run `make check` in a fresh worktree.

**One planning-and-checking tool, built (2026-11-12):** Brian approved the one-tool design ("i approve single tool desing re d4"; [design](../proposals/one-planning-tool/DESIGN.md)); all six slices are merged (#831 to #836). Lockstep ships from this repository as package `src/lockstep/` (`pcw` kept as an alias): plan format OpenSpec plus `layout:` rows in `lockstep.yaml` (`.aes/target.yaml` still read), the edit guard with code2check's shell parser, `lockstep check <name>` commit checks, `lockstep plan check`, `lockstep status` and `show`. Users switched: code2-template installs it (code2-template#29), lifelike is pinned here (lifelike#5), and Team-Brains' runner vendors its wheel (Team-Brains#1183, installed on the server 2026-11-12, backup brain-pr-runner-20261112T170439Z). `lockstep init` (the one-command setup the design promised, missed by the six slices) writes lockstep.yaml, the Claude Code, Codex and lefthook hook entries; the guard now logs to `.lockstep/` (Q23). Status: [wiki/lockstep.md](../wiki/lockstep.md).

**Inert characterization (2026-11-08):** the retained characterization and producer-identity Git readers disable repository hooks and fsmonitor commands. Two real monitor canaries reproduced execution before the repair; the characterization regressions confirm it is prevented while revision and dirty-state facts stay accurate. This is a narrow Lockstep component inspection repair, with no restart of retired universal governance. [Specification](../openspec/specs/inert-characterization/spec.md).

**Lockstep component (2026-11-07):** Brian's Lockstep delivery goal continues the AES component described in [the current architecture boundary](../wiki/index.md#what-aes-is-now); since 2026-11-12 Lockstep is built in this repository (above). Coding agents and Project Brains consume it.

**Evidence input qualification (2026-11-07):** the retained AES library now accepts optional `required_dependency_paths` on `evidence.assess` and `reconcile.reconcile`. Lockstep can require declared subprocess inputs before evidence contributes to standing; incomplete historical current observations become UNKNOWN, so they cannot mask later staleness of correctly recorded evidence. Existing default calls and record shapes are unchanged. This narrow component API increment does not restart the retired self-governance program. [Current architecture and specification](../docs/architecture/greenfield-v0.2/README.md).

**Where AES stands (2026-11-12):** AES is the name for the whole agent system: Lockstep, the feedback loop and Brian's agent policy (Brian, 2026-11-11: "aes is the whole sysem lockstep is one part. aes include the whole feedback and policy system"). The map is code2-workspace `docs/architecture/model.c4`; the decision is code2-workspace [decision 0009](https://github.com/BrianMills2718/code2-workspace/blob/main/docs/decisions/0009-aes-and-lockstep-fate.md) (Brian, 2026-11-10, "i aprpove"; amendment 1's Lockstep wind-down was withdrawn by Brian on 2026-11-11, and amendment 3 made Lockstep part of AES canonical).

- **Lockstep is built here.** It ships from this repository as `src/lockstep/` (`pcw` alias), merged in #831 to #841: plan format, edit guard, `lockstep check`, `lockstep plan check`, `status`, `show`, `init`. It still imports this repository's library (`src/agentic_engineering_system`).
- **The `aes` command line is used by five repositories** (Makefile targets in dodaf, lifelike, lockstep, plan-code-wiki, whygame5); twelve repositories hold an `.aes/target.yaml`. It retires one repository at a time as each is next changed. AES no longer governs itself: this repository's own `.aes/` was retired on 2026-11-12.
- **The feedback loop runs from here** (`scripts/learning_loop`, copied nightly to `~/.hive-brain/aes`). Timers on: `feedback-collector`, `feedback-labels`, `hive-controls`. Timers off: `feedback-problems`, `feedback-fix-owner`, `feedback-effects` (units and code kept; whether to re-enable is a feedback-loop decision).
- **The policy layer** is the rules register in `docs/rules` and `scripts/rules` (the agent-router script was retired: no caller); the rest of Brian's rules live in code2-workspace `agents/`.
- **Retired on 2026-11-12:** the claims, session and worktree machinery, 24 old proposals, the v0.1 plans, `.aes/`, `repository_context` and the unused folders. Every path, the reason and the restore command are in [docs/retired/2026-11-12.md](../docs/retired/2026-11-12.md). The universal commit enforcement stays retired (#789, 2026-10-14).
- **Checks:** `make check` runs the AGENTS.md sync check, pytest and mypy. Merging goes through `ship`.

**Agent feedback loop (2026-10-12):** [start page](../proposals/aes-learning-loop/review-page/guide.html) lists what runs and when, the current [domain model](../proposals/aes-learning-loop/review-page/feedback-models.html), the [requirements check](../proposals/aes-learning-loop/review-page/requirements.html), every document and what is open. The daily fix owner has closed all 24 adopt issues; 10 fixes carry receipts the effect counter reads. The 2026-10-08 diagram `feedback-system.svg` was retired on 2026-11-12 (see the retirement record).

**The hive moved to personal-vps (2026-10-07):** its scripts (`hive/`) and plans (`proposals/hive-brain-v1/`, `proposals/hive-hardening/`) now live in BrianMills2718/personal-vps (PRs #113, #114); the dashboard build, Glance and the PC controls timer run from there. `scripts/hive/brain_fresh.py` stays here because other repos call it by this path.

**Subagent feedback (2026-10-08):** native assignment/outcome capture and
parent-executed checks extend the same private feedback reports, with exact
parent/call/child/result attribution and separate inconclusive/checker-failure
states. See [the plan](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-subagent-feedback/PLAN.md) and
[commands](../scripts/learning_loop/systemd/README.md).
The original live Codex canary preserved an honest inconclusive instruction-scope stop.
The [follow-on repair](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-feedback-prevention/PLAN.md) scopes Remote MCP
preflight to that transport; native local inspection now completes with a source-supported
result, and a remote-only no-network task stops before substituting local inspection.
AES #479 merged the scoped instruction; all 466 Agent Skills tests and the AES gate (340 passed, one skipped) passed. This proves the bounded behavior, not improved model selection or live remote connectivity. Claude parity remains native-trace replay, not a new live run.
The corrected [parent check](https://github.com/BrianMills2718/agent-feedback-log/issues/263)
matches native replay and all five records in the weekly reader. Delayed checks
preserve native occurrence time; checker failures remain separate events.

**Feedback loop (2026-10-08):** the nightly collector reads changed Claude and
Codex transcripts, files Feedback reports to the private agent-feedback-log,
and bridges extracted human corrections directly into the same reports (including
a deduplicated 14-day backlog). Corrections file before every other report (#826): until
2026-11-11 they were added last, and the 900-a-night cap deferred all of them from 2026-11-03;
the 867 waiting were filed on 2026-11-11 (`collect_feedback.py --corrections-only --file`,
867 of 867, 0 errors). The old project-meta register is opt-in only.
Each proposed fix needs its own independent, resolved evidence. Weekly analysis
drafts fixes; the nightly effects mode reuses analyses and requires an explicit
enforcement receipt with time, revision and verification before counting subsequent
incidents. See [the approved repair](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-learning-loop/REPAIR.md)
and [operator commands](../scripts/learning_loop/systemd/README.md).

**Rule for every agent:** read this file first. When your change moves where
the project stands, update `now.md` (and `state.md` if needed) in the same pull
request. `python3 scripts/hive/brain_fresh.py .` exits 1 when this brain is
older than the work since.

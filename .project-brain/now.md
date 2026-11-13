# Complete file coverage (2026-11-13, AES #849)

**Current work:** cover every tracked file with a source-grounded summary and
navigation route, then assess documentation consolidation. The earlier 69-file
check covered a reader-Markdown subset, not this complete requirement.

Read [the complete catalog](../wiki/documents.md) and
[coverage/consolidation assessment](../docs/architecture/DOCUMENTATION.md#coverage-and-consolidation-assessment).
Planning is an explicit whole-system function, supplied by Company Planning;
Lockstep represents and checks its output. The
[policy source map](../wiki/policy-and-rules.md#where-are-the-hundreds-of-project-meta-policies)
now links the original 263-entry Project Meta registry and current shared rules.

**Next after this repair:** discuss recorded consolidation choices and the open
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

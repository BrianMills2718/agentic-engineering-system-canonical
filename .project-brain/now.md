# Now (2026-10-04, hive-brain session)

**Feedback system diagram (2026-10-08):** [the source-bound map](../proposals/aes-learning-loop/feedback-system.svg) now distinguishes six feedback types and six agent-selected improvement targets, with generalized causes, enforced prevention and recurrence at the center. Skill-use feedback remains a separate input path. The default taxonomy reader is merged (Agent Skills #460) and the installed private runtime at d709bcf preserved the original record and passed its disposition verifier; it accepts current feedback alongside retained legacy entries; see the [bounded prevention model](../proposals/aes-feedback-prevention/SYSTEM_MODEL.md) for the source-bound case and verification limits.

**Feedback repair tooling (2026-10-08):** the installed claim runtime consumes
canonical Enforced Planning's [successor-tracker repair](https://github.com/BrianMills2718/enforced-planning/commit/9baad04).
It preserves a closed lane's tracker and allocates a bounded path for a distinct
lane under the unchanged session goal; active and conflicting identities remain
occupied or refused. Owner lifecycle regressions pass; installed native lifecycle
evidence and closure are tracked in [#437](https://github.com/BrianMills2718/agentic-engineering-system-canonical/issues/437).

**Harness detour (2026-10-08):** the [audit and specialist plan](../proposals/harness-context/README.md)
inventories instruction/skill/hook/policy delivery across both clients. Its
[interactive review](../proposals/harness-context/review-page/index.html) shows
the findings and measured native context boundaries. Vision work remains with
its existing session; this detour makes no vision changes. Detailed private
source judgments are retained in Project Meta, with public references in the inventory.
The installed specialist completed native tasks in both clients. In those recorded
Codex child invocations, the bootstrap was inherited; the separate fresh-session
route was the measured smaller-context boundary. This describes those invocations,
not every native child configuration.
The [current Workflow and parity research](../proposals/harness-context/subagent-research.md)
adds Claude's dynamic script runtime, source-supported compact Codex entrypoints,
and automatic delivery checks followed by semantic trace review. Saved native
Claude evidence proves the compiled role and exact read-only tool catalogue were
delivered; complete behavior/permission parity is not certified. The PR497 source
foundation merged; it does not prove router activation. The collector at that
revision missed this child's result binding; PR499 repaired it at `74977b4e`,
and a fresh saved-trace replay found the original child and final result.
The [paired evidence checker](../proposals/harness-context/native-parity/verify_evidence.py)
now binds all four native traces, derives context/permission observations, and
checks exhaustive source review. Fourteen negative-control tests pass. The strict
parity mode refuses certification: Claude's answer retains source errors and the
tested Codex child retains excess bootstrap context. Original answers remain intact;
full child enforcement/hook parity and compact Codex0.162 execution remain unproved.
The agent-router inventory merged in PR500 at `c08837fe`: 263 source identities,
229 keep, 27 covered and 7 retirement candidates. Its 33 published baseline rules
retain their policy/enforcement; added applicability tags are inventory metadata,
not activation or a global instruction change. Detailed private evidence remains
with its owning lane.
The [skip-only recorder repair](../proposals/evidence-recorder-counts/README.md) is
reproduced but unimplemented: required adoption demands future execution proof ([#282](https://github.com/BrianMills2718/agentic-engineering-system-canonical/issues/282)); do not report #257 fixed.

**AES planning (2026-10-06):** real implementation work now needs an adopted
plan. Plans go through Company Planning's adoption gate, which writes the plan's
`/goal` text (company-planning #49). `aes plan accept` refuses a proposal
without a fresh adoption receipt (`.aes/planning.yaml`, on here, AES #153), and
every commit's tag is checked by `aes commit check` through `.githooks/commit-msg`
(`.aes/commit_rule.yaml`, **observe** mode: logged to
`.git/aes/commit-rule-<date>.jsonl`, nothing refused yet; AES #152). Use
`[Goal <plan_id>]` or `[Plan #N]` for planned work, `[Trivial]` for at most 3
files and 60 lines with no running-thing file, `[Shaping <plan_id>]` for edits
inside `proposals/<plan_id>/`, `[Unplanned]` only with an `Emergency:` line.

**Trace reviews (2026-10-07, PLAN-AES-TRACE-REVIEW):** every proposal must
declare `trace_review: {runs_traced_work: true}` or `{runs_traced_work: false,
reason: ...}`; `aes plan validate` refuses a proposal without it, and traced work
must add a `trace_review` evidence requirement. Its observation carries a
`trace_review` record (trace ids, author, a different reviewer, steps read of
total, models and settings, context per step, outputs and reasons, decisions
checked against source) and can SUPPORT only when every step was read and no
checked decision was wrong. Bug-fix plans (Company Planning route `repair`) can
now be adopted (company-planning #52, #53).
**Existing repositories (2026-10-07, PLAN-AES-ADOPT-EXISTING, issues #180/#155):** `aes adopt`
(instead of `aes init` where the governed roots already hold code) writes `.aes/legacy_baseline.json`:
every tracked governed file at a named commit with its blob id. Those files are legacy, not orphans;
a commit that edits one without a plan is refused under enforce and logged under observe (commit
rule check `legacy-edit`); `aes plan accept` removes files the target now plans; `aes status` ends
with the legacy share. Order: `aes adopt`, commit, `aes hooks install`. DIGIMON trial (not committed
there): 1,071 files under 12 roots, 94 KB baseline, `aes status` 8.6 s at 100.0% legacy
(`proposals/aes-adopt-existing/evidence/`). Next: adopt DIGIMON for real once a DIGIMON plan covers it.
**Commit rule, 2026-10-08 (plan commit-rule-followups, #269):** `[Trivial]` may not touch `conftest.py` or any script a tracked systemd unit runs; for a `[Goal <id>]` whose plan came from Company Planning `quick-adopt` (`planning_path: requested`), the rule logs whether the saved check output (`<plan folder>/<id>.check.txt`) is present and which files fall outside the plan's list (notes, never a verdict). Commits may carry an `Asked: <who> <date> "<words>"` line (#231).

**The hive moved to personal-vps (2026-10-07):** its scripts (`hive/`) and plans (`proposals/hive-brain-v1/`, `proposals/hive-hardening/`) now live in BrianMills2718/personal-vps (PRs #113, #114); the dashboard build, Glance and the PC controls timer run from there. `scripts/hive/brain_fresh.py` stays here because other repos call it by this path.

**Federated plans and misuse review (2026-10-07):** a `[Goal <id>]` now resolves from a plan in any repository under `~/code` (`plan_workspace` in `~/.config/aes/commit_rule.yaml`), so plans can move to the repository that owns them. A nightly report-only light-model review (`aes-commit-misuse-review` timer) judges accepted `[Unplanned]`/`[Trivial]` commits and opens concern `aes-commit-tag-misuse`; details in `proposals/aes-planning/ROLLOUT.md`.
Plans: `proposals/aes-planning/` and personal-vps `proposals/hive-hardening/` (both adopted).
Rollout to every repository (2026-10-07, Brian "go" on observe everywhere now,
enforce after two days where false refusals are at or under 1 in 5):
`proposals/aes-planning/rollout/install_everywhere.py` wires the rule into all
repositories under ~/code in observe mode (machine-wide mode in
`~/.config/aes/commit_rule.yaml`); `check` reports any unwired repository. The
replay of 21,948 recent commits in 185 repositories would refuse 99% (79% carry
no tag at all), so no repository meets the enforce condition; see
`proposals/aes-planning/ROLLOUT.md`. Installed 2026-10-07: 189 of 190 repositories wired
(the exception, an AES-project worktree on an old branch, is AES #167); the user timer
`aes-commit-rule-daily` checks coverage at 07:15 and opens the enforce-review concern once on
2026-10-09. Next: read the observe logs on 2026-10-09;
before enforce anywhere, give scheduled-job commits a recognised tag and get
adopted plans for each active project's real work. P1 (AES overlay in the gate's
profile) still waits on company-planning's plan-48 work.

**Subagent feedback (2026-10-08):** native assignment/outcome capture and
parent-executed checks extend the same private feedback reports, with exact
parent/call/child/result attribution and separate inconclusive/checker-failure
states. See [the plan](../proposals/aes-subagent-feedback/PLAN.md) and
[commands](../scripts/learning_loop/systemd/README.md#native-subagent-feedback).
The original live Codex canary preserved an honest inconclusive instruction-scope stop.
The [follow-on repair](../proposals/aes-feedback-prevention/PLAN.md) scopes Remote MCP
preflight to that transport; native local inspection now completes with a source-supported
result, and a remote-only no-network task stops before substituting local inspection.
AES #479 merged the scoped instruction; all 466 Agent Skills tests and the AES gate (340 passed, one skipped) passed. This proves the bounded behavior, not improved model selection or live remote connectivity. Claude parity remains native-trace replay, not a new live run.
The corrected [parent check](https://github.com/BrianMills2718/agent-feedback-log/issues/263)
matches native replay and all five records in the weekly reader. Delayed checks
preserve native occurrence time; checker failures remain separate events.

**Feedback loop (2026-10-08):** the nightly collector reads changed Claude and
Codex transcripts, files Feedback reports to the private agent-feedback-log,
and bridges extracted human corrections directly into the same reports (including
a deduplicated 14-day backlog). The old project-meta register is opt-in only.
Each proposed fix needs its own independent, resolved evidence. Weekly analysis
drafts fixes; the nightly effects mode reuses analyses and requires an explicit
enforcement receipt with time, revision and verification before counting subsequent
incidents. See [the approved repair](../proposals/aes-learning-loop/REPAIR.md)
and [operator commands](../scripts/learning_loop/systemd/README.md).

**Stopped at (2026-10-04 16:20 UTC):** hive brain v1 has seven merged jobs;
conditions 1 (pilot) and 3 (learning loop) are met. Rule K1 blocked real work
and its wrong block came back as friction issue #137. Still open: governance
firing inside a pilot job (condition 2), seven clean days (condition 4, earliest
2026-10-10), and a fresh-reader test of the plan (condition 5). Since 08:47 UTC
the Coordinator has been stopped by the Claude weekly usage limit; it should
resume after the 17:00 UTC reset. The hosted dashboard
(https://hive.brianmills.dev) now opens a panel for every map box, explains
every label, reloads itself and has a laptop layout (#136). The plan:
personal-vps `proposals/hive-brain-v1/ROADMAP.md`; the chronicle with evidence:
personal-vps `proposals/hive-brain-v1/PROGRESS_LOG.md`.

**Install path.** In this
repository, all three `make` gates pass from a clean clone with the README's
install line since PRs #110, #112 and #118 (2026-10-04); the measurements are
in the README and the progress log. That install line is now `uv venv .venv &&
uv pip install -e ".[dev]"` (2026-10-04), not `python3 -m venv` plus `pip`:
Brian's standing preference is uv with its shared cache in every repository.
The Makefile needed no change, because `$(PYTHON)` only ever consumed
`.venv/bin/python` and never created it. `docs/greenfield/GETTING_STARTED.md`
now installs with uv too (BRI-36, 2026-10-04), so no venv-plus-pip install path
is left in this repository: the page was run end to end from an empty directory
at `d89fe2e` and recorded as `OBS-AES-CLEAN-USER-d89fe2e`, which supersedes the
three earlier clean-user observations, and the clean-install test in
`tests/greenfield/test_distribution.py` builds its throwaway venv with uv
instead of stdlib `venv` plus `pip` (so it needs no `ensurepip`; it skips only
where uv is missing). That observation assesses `ER-SC-GF-001-01` INCONCLUSIVE
rather than SUPPORTS on purpose: the runner was the session that wrote the
change, not an independent fresh reader, so it proves the page's commands work
and not that the page reads well cold. Restoring SUPPORTS needs one fresh
session given only the page and a pin — the open follow-up on the install path.

**Next step:** follow "Exact next action" in the roadmap. In short: the
Coordinator keeps taking jobs from the refreshed weekly plan; agents merge
their own AES pull requests with `gh pr merge <n> --merge`, which this repo's
hook has accepted since PR #126 (it still refuses `--squash` and `--rebase`),
and keep the roadmap current; the remaining v1 conditions are evidence that
accrues on its own (a rule blocking real work, seven quiet days, a pick-up
retest after each rewrite of the roadmap).

**Rule for every agent:** read this file first. When your change moves where
the project stands, update `now.md` (and `state.md` if needed) in the same pull
request. `python3 scripts/hive/brain_fresh.py .` exits 1 when this brain is
older than the work since.


## Standing policy update — 2026-10-06

AES capability sourcing now treats **apparent novelty as unresolved search debt**, not as a positive design signal. When a needed capability or abstraction appears to have no established owner, the expected response is increased sourcing pressure: try alternate terminology and standards, adjacent disciplines/ecosystems, structural analogues, mature compositions/adapters, internal/historical attempts, failed approaches, and requirement/frame challenge before authorizing bespoke implementation. The more consequential and apparently novel the machinery, the stronger the burden to falsify the novelty claim and shrink the residual gap. Custom construction is a last-resort bounded residual, not an achievement in itself.

This policy is encoded in `docs/architecture/SYSTEM_BOUNDARY.md` under AES-CAP-002 and surfaced in `docs/plans/TEMPLATE.md` as an apparent-novelty check plus residual-invention declaration.

**Worktree lifecycle navigation (2026-10-09):** the adopted [plan](../proposals/worktree-lifecycle/PLAN.md) is merged in AES #481; its owner retains execution custody. The [proposal index](../proposals/README.md) and canonical instruction references link the four reader documents directly.

**Harness detour, 2026-10-09:** The [harness research](../proposals/harness-context/subagent-research.md) records a real compact Codex coordinator/child run with about 48% less startup input than the same-model predecessor. Exact native traces, full source review and child-turn hook receipts are retained; full client parity is still unverified. A subsequent native Claude attempt failed before dispatch and is preserved as refusal evidence. This does not change the AES product frontier or authorize vision work.

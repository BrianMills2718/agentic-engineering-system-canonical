# Minimal core met; template and ship live here (updated 2026-11-24)

Brian, 2026-11-20: "the whole thing should be configurable and shareable/protable. we shoudl start with the minimal
core". The first milestone is met: a repository made from the template ran one plan each in Claude and Codex in a
clean home folder (hidden tests 0/3 then 3/3, and 0/10 then 10/10) and merged with `ship`
([result](../docs/planning/minimal-core-2026-11-20.md), section 8; #996). Since then:

- `ship` is a console script of this package, with the prior-art check inside Lockstep (`lockstep check prior-art`)
  (#993); logs go under XDG state when there is no `~/code2` (#998); `run-plan` prints `uv run ship` and the status
  page is build output (#997).
- The starter template moved here from code2-template (Brian, 2026-11-21: "yes"; #999): `copier.yml` and
  `template/`. Make a repository with `uvx copier copy --trust gh:BrianMills2718/agentic-engineering-system-canonical <dir>`
  (tested from that address in the clean home: copy, `make check` and first commit all exit 0). code2-template still
  works but is no longer updated; six existing repositories still name it as their copier source.
- A copy now keeps its commit checks after a move and in every worktree: the template tracks `.githooks/` and
  sets the relative `core.hooksPath .githooks` (2026-11-22; spec portable-template). Older copies keep the absolute path.
- `ship` reruns hidden tests after its own rebase, and settles a rebase conflict confined to a committed
  `docs/status.md` by regenerating it (2026-11-22; spec ship). New copies do not commit that page (since 2026-11-21),
  so the second part matters for older copies and for repositories such as this one.
- code2-workspace's own copy of the prior-art check retired (code2-workspace #904).

**Second user, done 2026-11-22:** with agent login folders holding none of Brian's instructions, Claude and Codex each
ran a plan to passing hidden tests and merged through `ship`; the second merge reran the hidden tests after rebasing
(minimal-core plan section 8; [second-user.goal.md](../docs/planning/second-user.goal.md)). The template's commit
check no longer stages the git-ignored `docs/status.md` (#1009).

**Milestone reopened 2026-11-23:** the core list missed the linked chain (requirement -> scenario -> test -> file
-> symbol), which AES's goal page makes central. New copies now ship the edit hook that hands an agent the
requirement text (never approving an edit), and `lockstep check project` writes `docs/links.json`; the status
page shows each implementer's file and line. Accepted 2026-11-23 for Claude in a clean home (three plans, `chain-test` #1-#3; minimal-core section 8):
the hook's shell route was added in #1012 after Claude edited only through Bash. Codex not shown (no API quota).

**First add-on, 2026-11-23** ([plan](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/links-existing-lines-2026-11-23.md)): `docs/links.json`
also reads the link lines repositories already write: `Closes:` lines (plan nodes, active and archived), quote
markers (quote nodes) and each requirement's `Source:` line (#1015). Slice 2: the edit hook hands an agent the
decision records whose existing `Governs:` line names the file, its folder or a requirement it implements, flags a
superseded one, and `links.json` lists decisions (15 in AES, 0007 superseded); template decision 0001 governs
`docs/architecture/model.c4`.

Accepted 2026-11-23 in `chain-test` (clean home, Claude): #4 added decision 0002 (`- Governs: greeting`), a quote
marker and plan 4; `run-plan title-case-names` passed its hidden tests (4 failed, 1 passed before; 5 passed after),
merged as #5, and the hook log recorded decision 0002 handed over on three of Claude's shell commands; `links.json`
lists the plan (archived after merge), the quote (current) and both decisions.

**Back on the settled design, 2026-11-23** ([plan](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/back-on-design-2026-11-23.md)): Brian found the
minimal core had dropped the planned file layout (`lockstep.yaml` rows, structure before code; `LOCKSTEP.md:22-29`,
`proposals/one-planning-tool/DESIGN.md`) and that Lockstep was not used on itself. Slice 1: AES's `lockstep.yaml` now
governs `src/lockstep/` with one layout row per file, marks it fixed, and the AES client settings run `lockstep-hook`,
so an unplanned file there is refused (spec lockstep-plan-format, `lockstep-governs-its-own-package`, with a test).
Found on the way: `work_units.py` named a requirement ID no spec defined, and 12 of 193 requirements have empty
statement text because their `Source:` line comes first.

A session audit then found the edit hook's named recovery for a stale planned file (`lockstep check project`) did
not rewrite cog plan copies, so any requirement rewording would have locked agents out of the implementing file in
`src/lockstep/`; `project` now rewrites them (spec lockstep-projection).

**Alignment cleanup, 2026-11-23** ([plan and the 17 items to discuss](../docs/planning/alignment-cleanup-2026-11-23.md);
its questions Q49-Q55 in `docs/planning/open-questions.json` were answered on 2026-11-23, below): `lockstep check trace` in AES went from 142 findings
to 16, and `make check` now runs it (`make check-trace`) against `docs/planning/trace-accepted.txt`, a list that
can only shrink. The trace check now reads `scripts/`, separates stacked `Implements:` lines, reads requirements
whose `Source:` line comes first (#1019), and skips quote markers shown as code. 32 findings were stale docstring
plan copies that no check catches (Q53). The 16 left: 6 template requirements the check cannot read (Q50), 5 from a
duplicate spec (Q51), 6 whose spec lives in code2-workspace (Q52). 14 Lockstep files from the retired `.aes`
route have no requirement (Q54, retiring any needs Brian).

**Alignment answers carried out, 2026-11-23** (Brian: "i approve" to Q49 and Q51-Q55): the trace accepted list is
now empty. `make check` also fails on a stale or missing docstring plan copy (`check-copies`, #1029) and on a
requirement whose `Source:` line comes before its statement (`check-source-order`; 11 reordered, #1030). The
duplicate spec `aes-documentation-projection` retired (#1030). AES has its own `concern-issue` spec for its copy of
`scripts/concern_issue.py`; code2-workspace keeps its copy and spec. The 14 old-route files retire none: every one is
still run from AES's code (lifelike pins AES and runs 11; digimon's two checkouts run AES's edit hook on an AES plan; Team-Brains calls `action_check`), so one requirement
says each retires once nothing runs it. Hook refusals in a layout repository now point to `lockstep show`, not the
crashing `python -m lockstep.wiki`. code2-workspace's plan-size rule now asks the independent read to list departures
from the settled design (#930). AES's slow tests now run nightly (code2-workspace #929).

**Back on design, slice 3 done, 2026-11-23** ([result](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/back-on-design-2026-11-23.md#slice-3-result-2026-11-23-each-invented-part-settled)):
each part the minimal core invented is settled from the documents, with no new question for Brian. The one apparent
conflict, warn versus refuse, is Brian's decision D7 plus the template marking its package `fixed:`; `lockstep-guard`
now states that rule. The plan's three slices are complete.

**Template layout, slice 2 of back-on-design, 2026-11-23** ([plan](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/template-layout-2026-11-23.md)):
step 0 is merged: the trace check reads `Implements:` comment lines in `[tool.lockstep] comment_sources`
(AES: `copier.yml`, `template`), so the 6 template requirements trace and `trace-accepted.txt` is at 10 (Q50
resolved). Steps 3-4 merged: `run-plan` counts a file with a layout row at the plan's base as planned, and
`docs/links.json` shows each layout file and export as `planned` or `exists`. Steps 1, 2 and 5 built: a fresh copy
ships `lockstep.yaml` (rows for its three starter files; `copier update` of an older copy adds none and leaves its starter files alone,
tested against the real pre-#1027 template), its starter files
carry cog blocks filled from the rows, its edit hook refuses an unplanned file under `src/<package>/`, and its
`make check` runs the whole-tree check (#1027). Step 6 proof done: in a fresh copy, Claude `run-plan` ran
`lockstep layout` before writing the planned file, the hook refused its shell write and handed the requirement on its
Edit, hidden tests went 0/3 to 3/3 ([evidence](../docs/evidence/template-layout-proof-2026-11-23/README.md)); the
departure report now skips a row's test file and `docs/specs/` links. Slice 2 is complete.

**Format cleanup, 2026-11-24** (Brian: "do the cleanup carefully"): this repository now meets the code2 format (`scripts/repo_format.py` compliant 1 of 1; Q17 resolved). New: [arc42 map](../docs/architecture/arc42.md), [lockstep.c4](../docs/architecture/lockstep.c4) and the `.importlinter` contracts written from it; every requirement and decision has a `Source:` line (`lockstep check sources` missing 0); `make check` runs `check-format` (arch, sources, docmeta, test-first, changed, whole-tree). The edit hook now judges every file and rename destination in a patch before allowing it (Q26 narrowed to a live Codex payload). 326 merged remote branches removed ([restore list](../docs/retired/2026-11-24.md)).

**Markdown cap, 2026-11-24** (Brian: "i approve" to trimming to the 100-file cap): the 100-file cap was never in `make check`, and the exception had grown to 136 while the tree held 379 Markdown files. The OpenSpec change archive (273 files, 230 Markdown) is removed ([record and restore command](../docs/retired/2026-11-24.md)); references to it point at pinned GitHub copies. `make check` now runs `check-md-cap`; the exception is 149, the exact count, and only goes down.

**Next:** the list of `docs/` files to merge or retire is with Brian (sent 2026-11-24; nothing changed until he answers), to reach 100; then layout rows so every tracked file is planned, replacing the hand catalog (`wiki/documents.md`, PR #861 parked); then a Lockstep check that refuses a lint or type suppression an agent adds (`# noqa`, `# type: ignore`, an import-linter ignore) unless the same line names its reason, shipped in the template's `make check`.

**Parking list** (slices of the plan, in order; Brian 2026-11-24: "i approve adding the redit ideas to the plan and i will trust your jdugement on the impelemtnation prirotiy", after the [Reddit thread](https://www.reddit.com/r/ClaudeAI/comments/1y1my5l/) review; the thread's fourth idea, two tries per bug then revert, is already a workspace rule, Policy `two-tries-then-reset`):

1. Maintainability checker with one job, piloted here: duplicate code (`pylint` duplicate-code or `jscpd`), an existing helper rewritten under a new name, swallowed errors (`ruff` BLE/S110), complexity (`ruff` C901) and files that keep growing. Measure a baseline on AES first; the check fails only on new findings.
2. Mutation testing (`mutmut`) run nightly on one repository, to show the existing tests fail when the code they cover is broken; test-first already covers new tests.

# AES assessment (2026-11-19)

Brian asked for an audit. [The assessment](../docs/planning/aes-assessment-20261119.md) is read-only. It finds no measure yet of whether AES makes agents more effective. Lockstep's trace check fails in world-substrate (196 findings) and digimon (228) and runs at merge nowhere. The feedback log holds 8,624 unread reports, and the reading jobs have been off since about 2026-10-12. Three decisions are open for Brian (what AES is, a two-week world-substrate pilot, the feedback collector). The 2026-10-12 adopt-issue line further down is out of date: 192 of 226 adopt issues are open.

# Lockstep plan size (2026-11-18, code2-workspace issue 853)

Every plan that names a requirement `lockstep check changed` lists now states `Plan size: small` or `Plan size: full`. The check fails with `no-plan-size` when none does, and with `no-planning-package` when a full plan names no planning package file that exists. The count line adds `small`, `full`, `no_plan_size` and `no_planning_package`. Change: `https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/02bb545f4c56638428e12bdecc59f532ab99b478/openspec/changes/archive/2026-11-18-lockstep-plan-size/`. code2-workspace is the one repository that runs the check, and it picks this up when its pin moves.

# Lockstep document quotes (2026-11-17, code2-workspace issue 842)

A document marks a passage it copies from a requirement as `<!-- lockstep quote: <requirement id> -->the passage<!-- /lockstep quote -->`. `lockstep check trace` fails with `stale-quote`, `unknown` or `unclosed-quote` (at `<path>:<line>`) when a marked passage in tracked Markdown outside `openspec/` is no longer in its requirement's or scenarios' text; `lockstep check changed` lists the documents quoting each listed requirement as `current` or `stale`.
A copy that is not marked is not checked. Existing hand-typed copies (such as the seven in issue 842) are found only once someone marks them. Change: `https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/02bb545f4c56638428e12bdecc59f532ab99b478/openspec/changes/archive/2026-11-17-lockstep-document-quotes/`.

# Lockstep changed-requirement check (2026-11-17, code2-workspace issue 842)

`lockstep check changed --base <rev>` now lists every requirement whose statement or scenario text differs from the base (new, changed or removed; re-wrapping is not a change), with its implementing code, its tests labelled changed/unchanged/new, and the plan in the same change set that names it. It fails on `unplanned` and `no-scenario-changed`.
`lockstep check test-first` now also needs one test that fails on the base for each scenario whose text changed (`existing=True` is no exemption there), and `lockstep status` shows `changed, not archived` for text an active change rewords.
It does not find hand-typed copies of requirement text in documents, and it accepts a `Wording-only:` line as typed (printed and counted, not checked). It compares against the base as given, so against a moved `origin/main` it also lists requirements that landed there since the branch point.
Nothing runs it here yet: a repository opts in by adding `lockstep check changed --base origin/main` to its `make check`. Change: `https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/02bb545f4c56638428e12bdecc59f532ab99b478/openspec/changes/archive/2026-11-17-lockstep-changed-requirements/`.

# Ecosystem consolidation and first predecessor review (2026-11-13)

Tracking: [AES #856](https://github.com/BrianMills2718/agentic-engineering-system-canonical/issues/856).

Brian approved AES-owned ecosystem consolidation and asked to read older system
parts for the best ideas, concerns, inconsistencies and recommendations.
[Decision 0014](../docs/decisions/0014-ecosystem-consolidation-and-legacy-review.md)
records that direction. [The first source review](../docs/architecture/ECOSYSTEM.md)
compares the catalogue sources, contracts, dataset discovery, runtime tools and
legacy governance. Q36–Q42 extend the existing question ledger.

The 2026-11-14 continuation reviewed Project Meta's concern lifecycle decision,
repair registration/verifier and AES's receipt/effects code. It records the useful
stable-key/native-evidence pattern, the rejected recurrence negative control, and
why receipt presence is not verifier proof. The code review is not a live run;
current AES state still records fix-owner/effects jobs disabled.

The 2026-11-14 second continuation (branch eco-review-q30-q42) did the next
step. **Q30:** all 27 stale inventory hashes reconciled (23 harmless, four
summaries reworded for the array-fact feature); re-audit shows 0 mismatches, with
five newer files catalogued only in `wiki/documents.md`. **Discovery:** compared
the catalogue records and readers; the merged view returns 33 of the 60
catalogue IDs and hides a missing source as "uncatalogued"; recommended route is
the workspace jobs list plus a generated view and one alias table (Q36).
**Concerns:** mapped five key writers (no shared key format, per-repository
registers) and verified AES concern 783: its landed fix passes at the receipt
revision and fails on the pre-fix parent (negative control). **Policy and
instructions:** two instruction families read; AES `AGENTS.md` was generated
by a Project Meta route (retired 2026-11-14: now hand-maintained, `CLAUDE.md` imports it) and the subtree checker errors for AES. See the
third to fifth readings in the ecosystem page. Done later in
this review (see the sixth to ninth readings below): alias table, discovery journeys,
verifier and reopening runs, seven policy rows. Donor dispositions remain proposals, not migration or retirement.
Earlier projection and feedback work below remains independent and is preserved.

The 2026-11-14 third continuation (branches eco-alias-table onward) authored the
[alias table](../docs/decisions/0014-capability-aliases.yaml) and fixed the
ecosystem-ops merged view (PRs 201 and 202: failed sources are named, catalogue-only
entries listed, tool joins qualified, contract version shown; 82 rows, all 60 IDs).
The [journey receipt](../evidence/runs/discovery-journey-20261114.json) covers
`llm_structured` and `web_search`: declared consumers disagree with observed
callers in both. Seventh to ninth readings (ECOSYSTEM.md): recommended the keyed
GitHub issue as the one concern register and the Project Meta verifier as closure
owner; ran its five gates end to end on the landed code change of repair 783 (scratch
clone, synthetic cluster; passed on the code diff, refused on the whole PR diff
because the reviewer diff is truncated) and reopened a throwaway issue on GitHub
([receipt](../evidence/runs/concern-lifecycle-live-20261114.json)); read seven
policy rows; Codex observed loading `AGENTS.md`, not `CLAUDE.md`, so the generator was retired (`@AGENTS.md` import, Claude and Codex loads each observed once);
read the retirement record and 2026-09-26 harvest. Executor-written repair: five runs on concern #1883 were refused by the review gate; after two defect fixes and giving refusal reasons to retries (Project Meta PRs 2797, 2798) the sixth passed all five gates and landed as PR 2799, with the landed-tree check passing.
Not done: the issue closing at the next daily audit, and the timers (Brian's call).

**Project Meta retirement (2026-11-14, Brian: it is legacy and being retired in exchange for AES).** A plan, not
work done: [project-meta-retirement-plan.md](../docs/planning/project-meta-retirement-plan.md) lists who still calls
Project Meta (9 enabled timers, 7 repositories calling `md_file_cap.py`, AES's own loop calling two scripts) and
proposes slices: port, compare, switch, make the old file fail loudly, archive. The feedback timers stay off.
Open: Q44.

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

**Slice 0b (2026-11-14):** `docs/planning/project-meta-docs-triage.md` proposes, per folder, what to read, archive or regenerate among Project Meta's 2,734 docs files (1,604 read and 1,130 archive by the fixed rule, then overridden for generated wiki folders and `ops`). Nothing moved; Brian's approval of slices is still open (Q44).

**Workspace split (2026-11-14):** Brian approved core in AES, personal rules and identity in a private profile repository, identity as configuration. `docs/planning/workspace-into-aes-split.md` is the folder-level proposal (Q45); nothing in code2-workspace moved.

**Slice 0 done (2026-11-14):** `docs/planning/project-meta-ledger.md` lists what still calls Project Meta (89 files named by 73 distinct repositories, 10 enabled timers, 15 commands). Brian approved the slice order (Decision 5); nothing in Project Meta was changed.

**Slice 1a (2026-11-14):** `scripts/md_file_cap.py` is copied into AES and gives byte-identical output and exit codes to Project Meta's on 13 real repositories (`evidence/runs/md-file-cap-equality-20261114.txt`). Callers are planning `run_checks.sh` files, not commit hooks; 1b pilot done (code2-template #30, claim-extraction #41, topic-video #26); the remaining callers are next. Its default graph is still read from Project Meta until slice 4.\n\n**Slice 1b mostly done (2026-11-15):** planning checks in every repository but the Team-Brains family (generator code in a company repository) now run the AES `md_file_cap.py`; the old file does not yet fail loudly. Decision 14 B (Brian, 2026-11-15): the Team-Brains generators wait until that repository is next worked on. See the plan's slice 1 row.

**Rule for every agent:** read this file first. When your change moves where
the project stands, update `now.md` (and `state.md` if needed) in the same pull
request. `python3 scripts/hive/brain_fresh.py .` exits 1 when this brain is
older than the work since.

**Q45 step 1 (2026-11-16):** Claude loads the private profile through a user-level import (proven once). Codex gets a generated `~/.codex/AGENTS.md` from `brian-profile/scripts/build-codex-agents.sh` (PR #1 open: the new-repository rule needs a planning package, Decision 16 A defers it); Codex reading it is unproven until its usage limit resets on 2026-11-20.

**Slice 2 code (2026-11-16):** the loop's concerns, failure alerts and phone message no longer call Project Meta (`scripts/concern_issue.py`, `alert.py`, `notify.py`; spec `feedback-loop-notices`); `collect_feedback.py` still uses the legacy learnings register. Live run done 2026-11-16 (concern #894 lifecycle; Telegram test message 281); loop scripts not run end to end. See the plan's slice 2 row.

**Register frozen (2026-11-16, Decision 18 A):** the old learnings register is a read-only copy in the private repository `learnings-archive` (not in AES: public repo, publish-checker said hold; one token redacted, rotate the original). `collect_feedback.py` reads it and writes to no register. The feedback systemd unit templates no longer name Project Meta (installed copies of the two enabled timers still do until reinstalled).

2026-11-16: external idea intake added (`scripts/learning_loop/external_ideas.py`, watch list `external_sources.yaml`); runs on request, timer deferred until Brian has judged one digest.

**Retirement step 4b (2026-11-16):** the project graph sync, the `depends_on` scan and a rewritten daily refresh now run from AES against the private `aes-config` graph (specs `project-graph-sync`, `project-graph-dependency-scan`, `project-graph-refresh`). The refresh commits a changed graph straight to `aes-config` main and publishes the page to code2-workspace's data branch; the ten derived pages are dropped. Its timer is not switched yet (step 6). See the plan's row 4.

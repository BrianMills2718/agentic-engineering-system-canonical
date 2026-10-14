---
schema_version: "1.0"
artifact_type: design_plan
id: code2-ecosystem
status: proposed
method_conformance_receipt: proposals/code2-ecosystem/PLAN.receipt.json
trace_review_criteria:
  - criterion_id: outcome
    expected_outcome: pass
goal:
  outcome: "A fresh ~/code2 folder holds AES canonical, wiki_methodology and epistemic-warrant, moved in without breaking anything, with an instruction file that carries Brian's safety rules; epistemic-warrant's wiki is converted to the selected llm-wiki tool's format so Brian can look at it before more repositories follow."
  canonical_example: "Brian opens ~/code2/epistemic-warrant/wiki/index.md: it is the only front page, every document is reachable from it, wiki/log.md and wiki/_schema.md exist as the selected llm-wiki tool writes them, and wiki.py lint reports no errors; the old path ~/code/epistemic-warrant still opens the same folder."
  forbidden_substitutes: "Copied checkouts left beside the originals; hand-written wiki files that only look like the tool's output; a move verified by folder listing alone without git status, worktree list and the repository's own check; an instruction file nobody's session actually loads."
  boundaries: "Moves are renames on the same disk with a back-symlink at the old path, one repository at a time, each verified before the next. No checkout, branch, worktree or history is deleted. AES canonical moves last, only after the commit-rule-progress-fields lane (AES#673) has closed or its owner has been told. No AES source under the governed roots changes in this plan."
  done_when: "RUN-CONVERT, RUN-AGENTS, RUN-HOOKSPATH and RUN-MOVE-1..3 each show the trace named in Success and disproof, and durable_docs_check.py --plan proposals/code2-ecosystem/PLAN.md --range <adoption revision>..HEAD exits 0."
  do_not_gate_on: "Brian reviewing pull requests, hosted CI, a benchmark, other sessions finishing unrelated work, the phase 2 AES code, or the other ~180 repositories in ~/code joining."
---

# A fresh code2 ecosystem that AES canonical owns (phase 1)

> **Redirect, 2026-10-13 (Brian).** "find off the shelf stuff instead of building my own system ...
> every check should finish in seconds." code2 now runs on off-the-shelf tools, not AES's own
> enforcement: lefthook with one shared config (`BrianMills2718/code2-workspace`,
> `hooks/base.yml`), lychee for local links, markdownlint-cli2 for formatting, and a short
> reachability script. Parallel agents use Claude Code's `claude -w` worktrees; tasks are GitHub
> Issues. AES canonical joined code2 as an ordinary repository on 2026-10-13, alongside
> wiki_methodology and epistemic-warrant. The phase 2 plan built on AES enforcement is superseded.

Brian approved this on 2026-10-13 ("yes lets make the move") after asking for a fresh start:
"start a like code2 dir that has aes canoncial and maybe like a few relevant repos and star over
there", with enforcement that "should live in the ecosystem not in the repo" and one source of
truth. Project-meta is his legacy system; AES canonical replaces it.

This plan is phase 1. It moves the three repositories and converts epistemic-warrant's wiki, which
Brian asked to see before other repositories follow. Phase 2 (central rule settings in git, the
registry switch in the shared hook, the `aes workspace setup` command and the `wiki_format` rule)
changes AES canonical's own target and gets its own plan; its target change is drafted in
`proposals/code2-ecosystem/phase2-aes-proposal.yaml`.

## Actor and result

**Actor:** Brian, and the agents that work in his repositories.

**Result:** a second workspace, `~/code2`, holding AES canonical, wiki_methodology and
epistemic-warrant. Each was moved, not copied; the old `~/code/<repo>` path is a link to the new
folder, so running sessions, worktrees and scripts keep working. `~/code2/AGENTS.md` carries Brian's
safety rules, because `~/code/AGENTS.md` does not load for folders outside `~/code`; it is a symlink
to a file committed in AES canonical, so the rules have one source in git.

**Example Brian can see:** he opens `~/code2/epistemic-warrant/wiki/index.md`. It is the only front
page (the old `docs/index.md` is folded in), all 8 documents that were unreachable are linked,
`wiki/log.md` and `wiki/_schema.md` exist as the selected llm-wiki tool writes them, the compendium
line gives the current source count instead of "nine source chats", and `wiki.py lint` reports no
errors.

## Requirements

| ID | Requirement | Source | Check | Status |
|---|---|---|---|---|
| R1 | epistemic-warrant's wiki is set up by the selected llm-wiki tool (its `init` writes the `.wiki/` configuration, `wiki/log.md` and `wiki/_schema.md`) | Brian 2026-10-13; tool chosen by project-meta Plan #250 | RUN-CONVERT: the tool's `init` output and the files it wrote | planned, not yet run |
| R2 | epistemic-warrant has one front page: `docs/index.md` folded into `wiki/index.md` | Brian 2026-10-13 (one source of truth) | RUN-CONVERT: `docs/index.md` gone or reduced to a pointer, `wiki/index.md` holding its links | planned, not yet run |
| R3 | every reader-facing document in epistemic-warrant is reachable from `wiki/index.md` within two links, including the 8 found unreachable | workspace AGENTS.md documentation rule | RUN-CONVERT: `md_file_cap.py --repo .` reports no orphans | planned, not yet run |
| R4 | the stale compendium line ("nine source chats") states the current source count | found 2026-10-13 | RUN-CONVERT: the rendered line matches the count in `tools/compendium/` output | planned, not yet run |
| R5 | the converted wiki passes the selected tool's own checks, and those checks run in epistemic-warrant's `make check` | conformance claim of R1 | RUN-CONVERT: `wiki.py lint` and `wiki.py doctor` exit 0; `make check` output shows them run | planned, not yet run |
| R6 | the 32 repositories that set a local `core.hooksPath` are each listed with the reason and a disposition | phase 2 needs the shared hook to reach every member | RUN-HOOKSPATH: `proposals/code2-ecosystem/hookspath-review.md`, one row per repository from its `git config` output | planned, not yet run |
| R7 | `~/code2/AGENTS.md` carries Brian's safety rules and points at AES canonical for everything else | instructions load by folder; `~/code` rules do not reach `~/code2` | RUN-AGENTS: a fresh session started in a `~/code2` repository lists the file among its loaded instructions | planned, not yet run |
| R8 | wiki_methodology, epistemic-warrant and AES canonical move to `~/code2` one at a time, each with a migration packet, a back-symlink at the old path, `git worktree repair`, and verification | Brian 2026-10-13; move protocol in project-meta `docs/ops/PROJECT_ORGANIZATION_POLICY.md` | RUN-MOVE-1, RUN-MOVE-2, RUN-MOVE-3 | planned, not yet run |
| R9 | central rule settings in git, registry switch in the shared hook, `aes workspace setup`, `wiki_format` rule, removal of the four repository settings files | Brian 2026-10-13 | phase 2 plan | deferred: it changes AES canonical's target, whose validation needs an adopted plan of its own; carried onto this plan's completion record |

The work claims to use the llm-wiki tool selected under project-meta Plan #250 (a fork of
arronKler/llm-wiki at 56f4ea57, kept in `wiki_methodology/foundation/llm-wiki/`); R1 and R5 check
conformance to that tool's own commands and checks, not a look-alike.

## Success and disproof

Each run below is judged from its full trace: the implementing session's transcript
(`~/.claude/projects/-home-brian-code/<session>.jsonl`), the commands it ran with their output, its
commits, and the commit hook's verdict log at `<git-common-dir>/aes/commit-rule-<date>.jsonl`.

- **RUN-CONVERT** (R1-R5). Trace must show: the tool's `init` command and its output (not
  hand-written configuration); the commit moving `docs/index.md` content into `wiki/index.md`; the
  links added for each of the 8 named documents; `md_file_cap.py --repo .` output with no orphans;
  `wiki.py lint` and `wiki.py doctor` output with exit 0; `make check` output listing both; the
  merged pull request and its merge commit.
- **RUN-HOOKSPATH** (R6). Trace must show `git config --local core.hooksPath` run in each of the 32
  repositories, the history command used to find why it was set, and the review file committed.
- **RUN-AGENTS** (R7). Trace must show the file written, and a fresh session started with its
  working folder in a `~/code2` repository whose loaded-instructions list includes
  `~/code2/AGENTS.md`.
- **RUN-MOVE-1..3** (R8). For each repository, trace must show: the migration packet committed
  before the move; the `grep` of systemd units, crontab and `~/.local/bin` for the old path;
  `git status --short` and `git worktree list` before and after with the same entries (paths changed
  only); `git worktree repair` output; `readlink` of the back-symlink; the repository's own check
  (`make check` or its named equivalent) exiting 0 from the new path; one commit made from the new
  path judged accept in the verdict log.

**Disproof:** the approach is wrong if (a) a move breaks a running session, a worktree, or a
scheduled job that the back-symlink was meant to keep working; (b) the selected llm-wiki tool
cannot produce its format on epistemic-warrant without hand-writing its files, which would show it
is not fit to be the enforced standard in phase 2; (c) a session started in `~/code2` does not load
the safety rules; or (d) the converted wiki fails the tool's own `lint` or `doctor`.

## When a run fails or surprises us

1. Keep the failed run: record the session id and the exact command, and do not re-run it over the
   top. Keep the repository state (no reset); for a failed move, leave both paths as they are until
   diagnosed.
2. Read the full trace before choosing a fix: the command and its inputs, every tool call with its
   arguments and output, the hook verdict log lines, and the final state (`git status`,
   `git worktree list`, `readlink` of the symlink).
3. Write down the exact point where what happened differs from what this plan expected, quoting the
   output.
4. Classify it: the needed evidence never came back (for example the hook never ran); it came back
   and was ignored or contradicted; this plan's expectation was wrong; or unresolved.
5. An unresolved diagnosis allows more investigation only, never a repair presented as the cause.
6. A repair links to a new traced run that shows the fix, and the original failure stays recorded
   beside it in `proposals/code2-ecosystem/runs.md`.

Whether a review of the trace was complete is recorded separately from whether the run passed.

## System model

Model: `docs/model/ODD.md` with its trace `docs/model/trace.yaml`, reached from `wiki/index.md`
through the durable-documents section. The model covers AES canonical only.

This phase adds and changes no element of that model: it moves checkouts and edits another
repository's wiki, and no AES entity, process or rule changes. It relies on two elements, and each
examined run must show them:

- **ENT-COMMIT** (relied on): RUN-CONVERT and RUN-MOVE-1..3 must show their commits with the
  verdict line each produced in `commit-rule-<date>.jsonl`.
- **PROC-COMMIT-CHECK** (relied on): RUN-MOVE-1..3 must show the hook still running from the new
  path, as an accept verdict for the post-move commit.

Views: the entity and process tables in `docs/model/ODD.md`, each row linked to its source through
`trace.yaml`, are the applicable source-linked views; no row changes, so no view update is needed.
The examined runs must show the two rows above as they stand: the ENT-COMMIT row's log location
receiving the verdict lines, and the PROC-COMMIT-CHECK row's commit-msg hook producing them.
Freshness: `make docstring-wiki-check` and the trace check run in `make check` from the moved
checkout in RUN-MOVE-3, which shows the model and its trace still agree after the move.
Reconciliation for this phase: the model needs no update because no entity, process or rule
changes; view coverage needs no update because no row is added or changed, so `trace.yaml` still
names the same owner files and tests; the verification evidence needs no update because no code
under the governed roots changes, so the existing observations for VS-AP-COMMIT-RULE stay bound to
unchanged dependency paths, and RUN-MOVE-3's `make check` from the new path (which runs `aes
status`) must show none of them gone stale. If that run shows a stale or unreachable observation,
the move is treated as a failed run under the procedure above.

## Capability reuse

No catalogue entry fits, because the catalogue in agentic-capability-architecture-canonical holds
approval workflows, notifications, scheduling, document extraction and a search wrapper; none
moves checkouts or maintains a wiki. This phase adds no new capability; it reuses the llm-wiki
tool, which is not a catalogue entry.

## Authority and non-goals

Authority: Brian (approved 2026-10-13). AES canonical owns the code2 workspace. The wiki format
belongs to the selected llm-wiki tool in wiki_methodology, used here unchanged. The move procedure
in project-meta's Project Organization Policy still binds checkout moves until AES has its own.

Non-goals:

- Moving any repository other than the three named, or copying any repository.
- Changing AES source under `src/agentic_engineering_system/` or `tests/greenfield/` (phase 2).
- Changing the llm-wiki tool's format; gaps found go back to wiki_methodology as findings.
- Changing the rules that apply in `~/code`; they keep running unchanged.
- Retiring the back-symlinks; that is a later step with its own check.

## Irreversible actions and spend

This plan proposes no irreversible action and no spend, so there is no irreversible action or
spend to authorize or contain. The actions closest to that line, and how each stays reversible:

| Action | Boundary | Authority | Containment |
|---|---|---|---|
| Moving a checkout | the repository folder on this disk | Brian, 2026-10-13 approval | rename on the same filesystem plus back-symlink; undo is `mv` back and `git worktree repair` |
| Merging the wiki conversion | epistemic-warrant main branch | Brian's standing merge authority | merge commit after `make check`; undo is `git revert` |
| Any deletion of a checkout, branch, worktree or history | none proposed | Brian, asked first in the conversation | the step stops before deleting and asks |

No step spends money.

## Uncertainties

| Uncertainty | Why it is material | Owner | What resolves it |
|---|---|---|---|
| Whether any scheduled job, service or script resolves `~/code/<repo>` in a way a symlink does not satisfy (for example `realpath` comparisons) | a broken timer or service would fail after a move (disproof a) | implementing session | the `grep` in each move run, and the move run's checks |
| Whether the llm-wiki tool's `init` handles a repository that already has a hand-made `wiki/` | if it refuses or overwrites, R1 needs a different route (disproof b) | implementing session | running `init` on epistemic-warrant in its claimed worktree first |
| Why 32 repositories set a local `core.hooksPath` | each one skips the shared hook, which phase 2 relies on | implementing session | RUN-HOOKSPATH |
| Whether AES#673 has closed when AES canonical is due to move | moving its folder under a live writer could break that session | owner of that lane; this session messages it | its claim closing, or its owner's reply |
| How many live sessions hold working folders inside AES canonical when it moves | AES canonical holds the shared hook's runtime worktree; a broken path would stop every commit on the machine | implementing session | `ListAgents` plus claims check right before RUN-MOVE-3 |

## Activation facts

Declared: shared_mechanism false (no new shared mechanism, contract or algorithm in this phase; the
phase 2 plan declares it); empirical_comparison_proposed false (the wiki tool was chosen by
Plan #250; runs here are acceptance checks); llm_central false (no step depends on model calls);
irreversible_or_spend_action false (every action is reversible and free); aes_governed_target true
(AES canonical has `.aes/target.yaml`); claims_external_standard true (the converted wiki claims
conformance to the llm-wiki tool's format, owned in wiki_methodology).

## Prior art and ownership

Searched, 2026-10-13: existing owners (AES canonical `src/` and `proposals/`, project-meta's move
procedure and registry); internal lineage (project-meta Plan #250 and its follow-on Plans #254, #268, #270,
and #284; the 2026-09-04 flatten); and external prior art (the llm-wiki candidates screened
by Plan #250).

- **Selected llm-wiki tool** (`wiki_methodology/foundation/llm-wiki/`): reuse unchanged.
- **Other llm-wiki candidates** (atomicstrata/llm-wiki-compiler, toolboxmd/karpathy-wiki,
  jackwener, Labhund and Ekgardt llm-wiki, JeanBaissari/llm-wiki-monorepo, olegiv/llm-wiki-go,
  danvega/karpathy-wiki): superseded by Plan #250's selection; not reconsidered.
- **project-meta Plans #254, #268, #270, #284** (wiki rollout, single entrypoint, progressive
  disclosure): extend; their work in `~/code` stays theirs, and this plan applies the same tool to
  epistemic-warrant.
- **project-meta Project Organization Policy move procedure**: reuse for the moves.
- **2026-09-04 flatten of `~/code/active`** (53 repositories moved with back-symlinks): reuse its
  method.
- **project-meta `md_file_cap.py`** (legacy reachability check): reuse for R3 until phase 2.
- **project-meta `PROJECT_GRAPH.json`** (legacy registry): bounded exception, updated only where
  its own check requires the moved paths; not the code2 registry.

**Parallel check:** after each move, `find ~/code ~/code2 -maxdepth 2 -name .git` must list each
moved repository once under `~/code2` and only as a symlink under `~/code`; two real checkouts of
one repository would show a silent copy.

## Boundaries

- **Checkout migration** (three repositories). Owner: AES canonical for code2; project-meta's move
  procedure for the steps. Rollback: `mv` back, remove the symlink, `git worktree repair`.
  Disposition: proceed one repository at a time under its packet.
- **epistemic-warrant wiki** (another repository, Brian-owned). Owner: epistemic-warrant.
  Containment: a claimed worktree and a pull request merged after `make check`. Rollback: revert the
  merge. Disposition: proceed.
- **Pushes and pull requests** to Brian's own GitHub repositories (AES canonical, wiki_methodology,
  epistemic-warrant). Owner: Brian. Containment: merge commits after local checks. Rollback:
  `git revert` of the merge or closing the pull request. Disposition: proceed under Brian's
  standing merge authority. Nothing is published beyond those repositories; no sensitive data moves.

## Contracts and dependencies

Boundaries this plan crosses, all of them: (1) the filesystem path of each moved checkout,
which git worktrees, the shared hook, the commit-rule settings, scheduled jobs and sessions read;
(2) epistemic-warrant's repository, where the wiki tool's format applies; (3) the instruction
loader for sessions started in `~/code2`; (4) GitHub, for pushes and pull requests. The table
lists every schema or contract used or changed at those crossings: the checkout-path row covers
crossing (1), the llm-wiki row crossing (2), the instruction-loading row crossing (3), and the git
transport row crossing (4); the worktree-link, shared-hook and settings rows are the consumers of
crossing (1) that hold the path in a file.

| Contract | Owner | File | Changed here? | Produced by | Consumed by |
|---|---|---|---|---|---|
| llm-wiki format and checks | wiki_methodology | `foundation/llm-wiki/skills/wiki-configure/scripts/wiki.py` | no | wiki_methodology | epistemic-warrant's wiki and `make check` |
| Git worktree links | git | each repository's `.git/worktrees/*/gitdir` | yes, repaired paths | `git worktree repair` | git in every worktree of the moved repository |
| Shared commit hook | AES canonical | `~/.config/git/hooks/_aes_commit_rule.sh` (generated by `proposals/aes-planning/rollout/install_everywhere.py`) | no | AES canonical | git in every repository; it reads AES from the `hook-runtime` worktree path |
| Commit rule settings | AES canonical | `~/.config/aes/commit_rule.yaml` | no (phase 2 moves it into git) | Brian and agents | `aes commit check`; its `plan_roots` names a path inside AES canonical |
| Instruction loading | Claude Code and Codex | `~/code2/AGENTS.md`, a symlink to `proposals/code2-ecosystem/workspace/AGENTS.md` committed in AES canonical | yes, new | this plan | sessions started in `~/code2` |
| Checkout paths | Brian's machine layout, recorded by project-meta's Project Organization Policy (`project-meta/docs/ops/PROJECT_ORGANIZATION_POLICY.md`) | `~/code/<repo>` becomes a symlink to `~/code2/<repo>` | yes, real location moves; old path kept | the move runs | git worktrees, the shared hook, the commit-rule settings, systemd units and crontab entries found by the move run's `grep`, and open sessions |
| Git transport to GitHub | git (`https://git-scm.com/docs/gitprotocol-v2`) and GitHub | each repository's `origin` remote | no | this session's pushes | GitHub, which receives branches and serves pull requests |

Landing order so nothing breaks in between:

1. RUN-CONVERT lands in epistemic-warrant at its current path.
2. `~/code2/AGENTS.md` is written before any repository moves in (RUN-AGENTS).
3. wiki_methodology moves; within the move, the back-symlink is created in the same command as the
   rename, then `git worktree repair` runs before any commit, so git in its worktrees never reads
   a dangling link.
4. epistemic-warrant moves, same sequence.
5. AES canonical moves last, same sequence: the back-symlink keeps the shared hook's
   `hook-runtime` path and the settings file's `plan_roots` resolving; then `git worktree repair`;
   then the move run checks that a commit in an unrelated repository still gets its verdict.
6. The commit-rule settings file stays at `~/.config/aes/commit_rule.yaml` throughout this phase.
   Phase 2 moves it into git only after its own consumer (`aes commit check`) reads the new place
   with a fallback, so no commit loses its settings in between.

## Standard conformance

The external standard is the selected llm-wiki tool's managed-wiki format, owned by
wiki_methodology. Its machine-readable rules are the `lint` and `doctor` commands in
`wiki_methodology/foundation/llm-wiki/skills/wiki-configure/scripts/wiki.py`; its written audit rules
are in `foundation/llm-wiki/skills/wiki-maintain/references/audit-checks.md`, and its page schema
template is `skills/wiki-configure/assets/schema-template.md`. The converted wiki must pass `lint`
and `doctor` with no errors (broken links, orphan pages, schema problems, index drift,
classification errors) and hold the files the tool's `init` writes.

The named check is `wiki.py lint` plus `wiki.py doctor`, added to epistemic-warrant's `make check`
as target `wiki-check`; `make check` is that repository's merge gate, so it runs before every
merge, not once by hand. Disproof includes: the converted wiki, presented as following the tool's
format, fails `lint` or `doctor`. One part is an extension, not the tool's format: "one front page"
(no second `docs/index.md`). It is labelled in the artifact itself, in a section of
`wiki/_schema.md` headed "Extensions (not part of the llm-wiki format)", and in this plan.

## AES target

AES canonical is governed by `.aes/target.yaml`; this plan changes none of it. Its work is moves
of checkouts, a new `~/code2/AGENTS.md`, a review file under `proposals/`, and epistemic-warrant's
wiki; nothing lands under the governed roots (`src/agentic_engineering_system/`,
`tests/greenfield/`), so no target delta exists and no `aes plan validate` run applies to this
plan. The phase 2 target change is drafted separately and validated under its own plan.

Requirements served, each with its existing target item:

| Requirements | Target normative item | Success criterion | Verification subject |
|---|---|---|---|
| R6 (the review file), R7 (the workspace instruction file, committed at `proposals/code2-ecosystem/workspace/AGENTS.md`) and R8's migration packets: the commits this plan makes in AES canonical, each tagged `[Goal code2-ecosystem]` | AP-REQ-001 (OUT-AP-001) | SC-AP-001 | VS-AP-COMMIT-RULE (ER-AP-001-01); ER-AP-001-02 runtime observation: the verdict accepting each such commit |

The behaviour each requirement delivers is outside what the AES target describes, so it is verified
by the named check in the Requirements table, not by an AES verification subject:

- R1-R5 change only epistemic-warrant, which has no AES target: verified by its own `make check`
  (with the new `wiki-check` target) and `md_file_cap.py`.
- R6 is a review file: verified by RUN-HOOKSPATH's per-repository `git config` output.
- R7's file is committed in AES canonical (mapped in the table above for its commit) and linked
  from `~/code2/AGENTS.md`; whether sessions load it is verified by RUN-AGENTS.
- R8 changes no repository content: verified by each repository's own check in RUN-MOVE-1..3.
- R9 is deferred to the phase 2 plan. Reason: it adds to AES canonical's target, and `aes plan
  validate` refuses a target change until the plan naming it has been adopted, while this gate asks
  for a passing validate before adoption; a separate plan whose only content is that target change
  can be adopted first and then validated. Deferred, it needs no verification subject here.

## Durable documents

AES canonical declares these roles in `.agentic/repo.yaml`:

```yaml
durable_documents:
  schema_version: "0.1"
  goal: docs/architecture/GOAL.md
  requirements: .aes/target.yaml
  system_model: {prose: docs/model/ODD.md, trace: docs/model/trace.yaml}
  decisions: docs/decisions/
  plans: docs/plans/
```

Durable documents: none -- this phase changes no AES goal, no requirement in `.aes/target.yaml`, no
system-model element or rule, and no decision; it moves checkouts and edits another repository's
wiki, and its design and status live in this proposal folder. Phase 2, which adds model elements
and a decision record, declares them in its own plan.

At completion,
`python3 ~/code/company-planning/plugins/company-planning/scripts/durable_docs_check.py --repo . --plan proposals/code2-ecosystem/PLAN.md --range <adoption revision>..HEAD`
must exit 0.

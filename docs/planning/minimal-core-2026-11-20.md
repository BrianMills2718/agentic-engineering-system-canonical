# Minimal core: what Brian wants, what exists off the shelf, what to keep

Status: milestone met (2026-11-22, `68037920b`). One part is reversed: folding the planned file list into `tasks.md`
(line 103, an agent inference) was undone by `https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/back-on-design-2026-11-23.md`, which puts the `lockstep.yaml` layout
back. Read that plan with this one.

Source: Brian, 2026-11-20, Claude session 5651a525 (no file): "the whole thing should be configurable and
shareable/protable. we shoudl start with the minimal core than add on other things as needed after the first
minimal core milestone. we should udnersand wall the capabilties and constrats that we want and have them clearly
lsited and have a landscape survey of what is off the shelf". Same day: "the goal is to give a well specified plan
to an agent on some proejct nad have it faithfulyy and successfully impelemnt it"
([next.goal.md](next.goal.md)).

## 1. What the system must do (capabilities)

| Id | Capability | Core or add-on | Brian's words |
|---|---|---|---|
| C1 | A plan with WHEN/THEN examples and a task list that names the files | core | 2026-11-20, above |
| C2 | Hand the plan to a Claude or Codex agent, which implements it | core | 2026-11-20, above |
| C3 | Acceptance check the implementer did not write: hidden tests from the plan alone | core | 2026-11-20, "faithfully and successfully" |
| C4 | Departures reported: changed files not in tasks, skipped tasks | core | 2026-11-20, "faithfully" |
| C5 | One merge path that merges only the commit whose check passed | core | 2026-11-05: "i should never have to approve a pr/deploy" (core.md) |
| C6 | Secrets and `.env` never committed | core | rule in core.md; no quote found |
| C7 | Full trace of every run | core | 2026-10-16: "every plan should have a requirement to have visibility for the full trace and that you should be examining this" (rule-sources.md:548) |
| C8 | Prior-art record per feature | open (Decision 1) | 2026-11-17: "every cpaability/featuer shoul dhave a prior art search ... that needs to be ienforced" (rule-sources.md:782) |
| C9 | Requirement ids named in code and tests exist | core (existence only) | agent inference: today's test (section 4) |
| C10 | Docs conventions (links, format, reachability, arc42, LikeC4) | add-on | workspace decision 0002 |
| C11 | Session log, feedback lines, cost basis, nightly prompt-size check | add-on | core.md, Records |
| C12 | The linked chain: each requirement linked to its scenarios, tests, files and code; an agent editing code is handed the requirement it implements; the links readable in one file | core | 2026-11-23: "isnt this the whole thing that makes the whle systme work?"; AES `docs/architecture/GOAL.md:88`, `LOCKSTEP.md:26`. Left out of the first list by agent error (plan [https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/linked-chain-core-2026-11-23.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/linked-chain-core-2026-11-23.md)) |

## 2. What the system must be (constraints)

| Id | Constraint | Brian's words |
|---|---|---|
| K1 | Configurable, portable and shareable | 2026-11-11: "configurable and protable/sharebale" ([DESIGN.md:8](../../proposals/one-planning-tool/DESIGN.md)); 2026-11-20 above |
| K2 | Minimal core first; add-ons only after the first core milestone | 2026-11-20 above |
| K3 | Off the shelf before custom | 2026-10-13: "find off the shelf stuff instead of building my own system" (workspace AGENTS.md); 2026-10-01: "novelty and building ourself is always assumed to be bad" (rule-sources.md:139) |
| K4 | Every check finishes in seconds | 2026-10-13: "every check should finish in seconds" (workspace AGENTS.md) |
| K5 | Measured before mandatory | 2026-10-26: "i guess i feel like we are overusing heavy checks to being with" (rule-sources.md:551) |
| K6 | Same behaviour in Claude and Codex | 2026-09-14: "the answer is always yes" (rule-sources.md:346) |
| K7 | Speed to a working version | 2026-10-01: "we are always speedrunning" (rule-sources.md:132) |
| K8 | One home per rule | 2026-10-11: "yes we should get rid of repitition" (rule-sources.md:11) |
| K9 | Failures loud and visible | 2026-09-29: "we always want maximum observability in logs and in output" (rule-sources.md:184) |

Conflicts: C8 enforced vs K4/K2 (Decision 1). C7 full trace vs K4: the trace is recorded during the run, not
checked at commit, so they do not collide.

## 3. Off-the-shelf landscape (checked 2026-11-20)

Release and push dates from `gh api repos/<r>` on 2026-11-20.

| Tool | Latest release | Covers | Verdict |
|---|---|---|---|
| OpenSpec (Fission-AI) | v2.1.1, 2026-11-19 | C1, C2; skills for Claude and Codex | **adopt** (already in use) |
| Spec Kit (GitHub) | v1.4.3, 2026-11-19 | C1, C2, more files per feature | reject: same job as OpenSpec, heavier |
| Superpowers (obra) | v7.0.2, 2026-11-03 | C1, C2, test-first and worktree skills, both agents | alternative to OpenSpec; use one, not both |
| Kiro specs (AWS) | n/a (editor) | C1 format (EARS WHEN/THEN SHALL) | reject the tool; copy the format |
| Tessl | closed beta | library specs | reject: not generally available |
| BMAD Method | v6.12 | full agile persona workflow | reject: far beyond a minimal core |
| Task Master | n/a | PRD to task list via MCP | reject: duplicates OpenSpec tasks |
| Agent OS | v3.0.0, 2026-01-20 | C10 only | reject: `AGENTS.md` does it |
| lefthook | v2.2.2, 2026-10-13 | commit and push hook runner, one file | **adopt** (already in use) |
| pre-commit | n/a | hook runner, clones hook repos | reject in favour of lefthook |
| gitleaks | v8.30.1, 2026-03-21 (code pushed 2026-10-28) | C6 | **adopt** |
| copier | v9.19.1, 2026-10-13 | install into a repo and `copier update` later | **adopt** (code2-template already uses it) |
| GitHub merge queue / branch protection | server feature | C5 | reject: no hosted CI here, per-repo setup |
| Claude Code OpenTelemetry | beta traces | C7 | possible later; exporter must be set per user, not per repo |
| Langfuse hook plugin | n/a | C7 for both agents | add-on if a trace UI is wanted |
| Spec-to-test tools | none found with independent evaluation | C3 | build (small) |

Codex limit that decides where checks live: Codex's PreToolUse hook does not see every shell path
([source](https://raw.githubusercontent.com/Dicklesworthstone/destructive_command_guard/main/docs/codex-integration.md)),
so any check that must hold lives in git hooks and the merge step, not in agent hooks (K6).

## 4. What today's test shows and does not show

Plan-fidelity test, 2026-11-20 ([next.goal.md](next.goal.md), "Plan-fidelity proof"): 3 OpenSpec plans, 6 builds
(3 with Lockstep's edit guard and commit checks on, 3 off). All 6 implemented their plan faithfully.

- Shows: an agent given an OpenSpec plan builds it; the hidden acceptance tests (written by a separate session
  from the plan alone, held outside the repo) are the check that actually measured success.
- Shows: the edit guard and commit checks made no difference on these plans.
- Does not show that the prior-art or requirement-id checks are useless. Neither was varied: the off arm still
  merged through `ship`, and all three plans touched only ungoverned `scripts/` and `tests/`.
- Shows the opposite for two checks: `ship`'s prior-art check refused an invalid `prior-art.json` that both #241
  builds inherited (code2-workspace#895), and the trace check (warn mode) flagged wrong `Implements:` ids in both
  arms (196 to 203 findings).

## 5. Current mechanisms: keep, merge, cut or add-on

| Mechanism | Where | Verdict | Why |
|---|---|---|---|
| OpenSpec plan (proposal, spec delta, tasks) | each repo `openspec/` | **core** | C1 |
| Repo's own `make check` | each repo | **core** | C3, K4 |
| `ship` merge | `~/.local/bin/ship` | **core, trimmed** | C5; drop the gates below that move to add-ons |
| Secret scan at commit + `.env` refusal | `hooks/base.yml` | **core** | C6; one place |
| Secret scan at push | `hooks/base.yml` | merge into commit scan | duplicate (K8) |
| Requirement-id existence (`Implements:` / `req(...)` name a real requirement) | `lockstep check trace` | **core, new findings only** | C9; caught wrong ids today |
| Prior-art check at commit | `hooks/base.yml` | Decision 1 | passed a record `ship` refused (code2-workspace#895) |
| Prior-art check at `ship` | `ship` | Decision 1 | caught today's invalid record |
| Planning-package gate | `ship` and global pre-push | add-on, one place | duplicate (K8) |
| Goal provenance gate | `ship` | add-on | not C1-C7 |
| `Source:` lines check | `lockstep check sources`, run 3 times | add-on, one place | duplicate (K8) |
| Docs: links, markdown format, reachability, docmeta | `hooks/base.yml`, `lockstep check docmeta` | add-on | C10 |
| Lockstep file layout (`lockstep.yaml` file list) | `lockstep check` | merge into departure report | same list as `tasks.md` (K8) |
| Lockstep edit guard | PreToolUse hook | handing over requirement text: core, in every copy (C12, 2026-11-23); refusing edits: add-on, off by default | refusal caught 0 defects; Codex hook cannot enforce it (section 3); hooks are off in Codex until the user turns them on |

## 6. The minimal core

1. **Plan**: OpenSpec change with WHEN/THEN scenarios and a `tasks.md` naming files. A "Test seam" section names
   the observable behaviour each scenario is checked through.
2. **Hidden acceptance (new, C3)**: a separate agent session writes tests from the plan alone into a folder
   outside the implementer's worktree; they are copied in only after the implementer's final commit, and must pass
   before `ship`. This is the procedure that worked today, packaged as one script.
3. **Implement**: any Claude or Codex agent, one worktree, instructions from one `AGENTS.md` (`CLAUDE.md` imports it).
4. **Departure report (new, C4)**: `git diff --name-only` against `tasks.md` files plus unchecked tasks; report only,
   not blocking (K5).
5. **Commit hooks (lefthook)**: gitleaks on staged files, `.env` refusal, requirement-id existence on new findings.
6. **Merge**: `ship` with only `make check` and the core checks above.
7. **Trace (C7)**: keep each run's agent transcript under a run id; a trace UI (Langfuse) is an add-on.
8. **Linked chain (C12)**: `Implements:` lines and `req()` markers are the one home of each link; the edit hook
   hands the requirement text to the agent; `lockstep check project` writes `docs/status.md` and `docs/links.json`.

Everything else in section 5 marked add-on is off until a logged failure justifies it.

## 7. Configurable and portable (K1): what is tied to this machine today

"Configured from one file" is a design goal here, not something a tool provides.

| Tied to this machine | Replacement |
|---|---|
| `ship` is a symlink to `~/.hive-brain/aes/scripts/ship.py` | install from the public repo with `uvx`, like `lockstep` already is |
| Shared hooks come from a private repo through the `github-personal` SSH alias | a public hooks file, or copied in by copier |
| `storage-policy`, `~/projects/data` paths in rules and scripts | out of the core; personal add-ons |
| core.md and topic files use home-directory paths | core rules move into the template's `AGENTS.md`; personal rules stay in core.md |
| Which add-ons are on | copier answers file (`.copier-answers.yml`) as the one switch; `lefthook.yml` and `AGENTS.md` generated from it |

## 8. First core milestone and the rule against new sprawl

Milestone: a new repo made from the template runs one plan through steps 1-6 in both Claude and Codex, on a
second machine or a clean user, with the hidden tests passing and the departure report produced.

**Result, 2026-11-21: met, with one stated compromise.** Run in a clean home folder (no `~/code2`, no global git
hooks, no tool wrappers, no `ship` link; real `uv`, `git`, `gh`, `node`, `openspec`, `lefthook`, `gitleaks`, `claude`,
`codex`), in a new private repository made with `copier copy gh:BrianMills2718/code2-template` and default answers:

| Agent | Hidden tests before / after | `make check` | Read the hidden tests | Departures named by the agent | Merged by `uv run ship` |
| --- | --- | --- | --- | --- | --- |
| Claude | 0/3 / 3/3 | 0 | no (peek_reads 0) | 3 of 3 | yes, "hidden tests passed" |
| Codex | 0/10 / 10/10 | 0 | no (peek_reads 0) | 5 of 5 | yes, "hidden tests passed" |

Both plans also merged through `ship` with the prior-art gate passing and both add-on gates printed off. `ship`
refused a branch whose hidden-test run was for the commit before a rebase, as specified. Compromise: the agents
used their own login folders (`CLAUDE_CONFIG_DIR`, `CODEX_HOME`), so they read the owner's global agent
instructions; everything under test used nothing from the machine. Found and fixed: Node.js missing from the
template's prerequisites (code2-template #36). Found and filed: the generated `docs/status.md` (and the spec list in
`docs/index.md`) conflict whenever two plans merge one after the other (code2-template#37); `run-plan` prints
`ship` where a template repository needs `uv run ship` (#994); `ship` and the lane sweep still default their logs to
`~/code2/`.

All four are fixed: a new copy's `docs/status.md` is build output and its spec list is generated (code2-template#37,
2026-11-21); `run-plan` prints `uv run ship` (#994); logs default to `${XDG_STATE_HOME:-~/.local/state}` where
`~/code2` does not exist. Found and fixed on 2026-11-22: a moved copy or a worktree ran no hooks (#1004, #1007), and
`ship` now settles a conflict confined to a committed `docs/status.md` and reruns hidden tests after its own rebase
(#1006).

**Compromise removed, 2026-11-22 ([second-user.goal.md](second-user.goal.md)).** Rerun in the same clean home with
agent login folders that hold no `CLAUDE.md` or `AGENTS.md` (Brian logged both agents in), in private repository
`second-user` copied from this repository's template, Lockstep at main:

| Agent | Hidden tests before / after | `make check` | Read the hidden tests | Reads outside clean home | Merged by `uv run ship` |
| --- | --- | --- | --- | --- | --- |
| Claude | 3 errors / 5 passed | 0 | no (peek_reads 0) | none | yes, second-user #4 |
| Codex | 4 failed / 4 passed | 0 | no (peek_reads 0) | none | yes, #5, after `ship` rebased onto #4 and reran the hidden tests (4 passed) |

Departures named: Claude 1 file, Codex 3 (architecture diagram, import contract, generated spec pages). A first
attempt was void: the plans, copied from the earlier test project, named its package; Claude stopped and asked,
Codex built the named package. Found and fixed: the template's commit check staged the git-ignored
`docs/status.md`, so every commit that changed the status page failed (#1009). Parked: `run-plan` prints the
`ship` line even when nothing was built (`ship` refuses such a branch anyway).

**Milestone reopened, 2026-11-23.** The 2026-11-22 result above stands for C1-C11, but the core list missed C12,
so the first core milestone is not met until the linked chain works in a fresh copy: the hook hands the agent the
requirement text, and the link file lists the changed requirement's scenarios, tests, file and symbol
([https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/linked-chain-core-2026-11-23.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/linked-chain-core-2026-11-23.md), acceptance).

**Linked chain accepted, 2026-11-23 (C12; milestone met for Claude).** Clean home with empty agent login folders,
private repository `chain-test` copied from the template at #1011, three plans, all built by Claude through
`run-plan` and merged by `ship`:

| Plan | Hidden tests before / after | `make check` | Read the hidden tests | Merged |
| --- | --- | --- | --- | --- |
| add-greeting (new requirement) | 4 failed / 4 passed | 0 | no (peek_reads 0) | chain-test #1 |
| greet-several (changes it) | 5 failed, 1 passed / 6 passed | 0 | no | #2 |
| greet-with-word (changes it again, Lockstep at #1012) | 3 failed, 1 passed / 4 passed | 0 | no | #3 |

In plans 1 and 2 Claude changed files only through Bash, and the hook's shell route handed over nothing in a
repository without a layout plan; fixed in #1012. In plan 3 the hook log shows two `openspec_text` hand-overs
naming `greeting/greets-a-person-by-name` for `src/chain_test/greeting.py`, and a probe in the same copy showed
Claude quoting the hook's header line, which is not in the file. After plan 3, `docs/links.json` links that
requirement to all 6 scenarios, their 8 tests and `chain_test.greeting` (`src/chain_test/greeting.py:1`), the
same scenarios the test markers name. Not shown: Codex (its stored API key had no quota; Codex hooks are off by
default and need trusting).

Rule for add-ons (inferred by agent; Brian can veto): each rule lives in one place; an add-on becomes mandatory
only after an on/off comparison shows it catches something; a mandatory check with no logged catch in 2 weeks is
switched off.

## 9. Decisions

1. **Prior-art record (C8).** Options: (a) checked at `ship` only, commit-time copy removed; (b) checked at both;
   (c) add-on, off in the core. Recommendation: (a), medium confidence: it keeps Brian's 2026-11-17 "needs to be
   enforced" with one check that caught a real defect today, and removes the copy that let it through.

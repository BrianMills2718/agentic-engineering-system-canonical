---
description: Read-only assessment of AES on 2026-11-19 covering what works, what is unproven, where Lockstep actually runs, the feedback loop's state, what a trace finding is, and three decisions for Brian
doc_role: evidence
status: current
---

# AES assessment (2026-11-19)

Source: Brian, 2026-11-19: "investigate my aes canonical work. assess question critique and advise", then
"docuemtn this audit". The assessment was read-only: it changed no repository (side effects are listed at the
end). A number is **measured** (a command was run, listed under Evidence) unless it is marked
**reader-reported** (a subagent read and counted it; not re-run) or **inferred**.

## Summary

AES has two parts that work as code: the `lockstep` command (each check runs in 1 to 9 seconds) and the
nightly feedback collector. After 1,523 commits in nine weeks, nothing measures whether AES makes agents more
effective, which is its stated goal. The two parts that would show it are not in force:

- Lockstep's check that plans and code line up (`lockstep check trace`) fails in both repositories that have
  tried it and runs at merge in neither.
- The feedback loop files about 450 reports a day, and the jobs that read them have been off since about
  2026-10-12.

Most work since 2026-11-13 has gone into moving older systems into AES (which Brian set as a requirement on
2026-11-16) and into new checks, documents and questions about AES itself.

## What AES is: Brian's description against the repository

Brian, 2026-11-19: "in my mind aes is like an agentic coding system. it helps with planning, and implementing
code and keeping plans aligned with code."

| Part of that description | What exists | State on 2026-11-19 |
| --- | --- | --- |
| Planning | Company Planning (a separate repository) writes plans; OpenSpec holds the required behavior; `lockstep plan check` checks a plan's format; `lockstep check sources` checks that each requirement names who decided it | These two checks run at merge (`make check`, which `ship` runs) in 5 repositories |
| Implementing code | AES does not run agents; Claude Code and Codex write the code. Lockstep helps them in three ways: `lockstep layout` creates the planned files, requirement text is copied into the code's docstrings, and the edit guard refuses an edit to a file the plan does not list | Only world-substrate lists planned files (52), and only in its documentation folders. A probe edit to a new, unplanned file under `src/` passed with "no rule" |
| Keeping plans aligned with code | `lockstep check trace`: every requirement has code that says it implements it, and every scenario has a test marked with it (next section) | Fails in world-substrate (196 findings) and digimon (228, set to warn). In no repository's `make check` |

Two further parts sit in AES and are not in that description:

- **Feedback loop and policy.** Brian, 2026-11-11: "aes is the whole sysem lockstep is one part. aes include the
  whole feedback and policy system".
- **Replacing the older systems.** Brian, 2026-11-16, set as a requirement of the goal: "One consistent,
  shareable, configurable AES canonical system that replaces the many old overlapping, unfinished and
  contradictory systems" ([AES consolidation plan](aes-consolidation-plan.md)). Since 2026-11-13 this has
  brought in the project graph, the notification router, the hub page, a machine manifest, outside-idea
  intake and the Project Meta port. AES now has 30 OpenSpec capabilities.

Decision 1 below asks which of these Brian means AES to be.

## What a trace finding is

A concrete case from world-substrate. Its spec `openspec/specs/causal-model-authoring/spec.md` (line 123) has
the scenario "A terminal selector is empty". No test in the repository is marked
`@pytest.mark.req("causal-model-authoring/a-terminal-selector-is-empty")`. So `lockstep check trace` prints:

```text
untested      causal-model-authoring/a-terminal-selector-is-empty  (openspec/specs/causal-model-authoring/spec.md)
```

Trace links three things by ID: the requirements and scenarios in `openspec/specs/`, the code lines that say
`Implements: <capability>/<requirement>`, and the tests marked `@pytest.mark.req("<capability>/<scenario>")`.
A finding is a broken link of one of three kinds (`src/lockstep/checks/trace.py`, lines 70 to 73):

| Kind | Meaning | world-substrate count | Example |
| --- | --- | ---: | --- |
| unimplemented | a requirement that no code line claims to implement | 58 | `cvs-situation-import/causal-boundary` |
| untested | a scenario that no test is marked with | 109 | the case above |
| unknown | code or a test names an ID that no spec contains | 29 | `scripts/world_builder_service.py` names `world-builder-page/a-what-if-branch-can-change-one-groups-brief` |

What a finding does and does not say:

- It is a missing **label**, not proof of missing behavior. The code may do what the requirement says with no
  `Implements:` line, and a test may cover a scenario without the marker.
- Some `unknown` findings look like ID spelling differences, not missing work (inferred). The example above
  matches a scenario heading in `openspec/specs/world-builder-page/spec.md` (line 424); its requirement title
  ("A what-if branch can change one group's brief", line 419) contains an apostrophe.
- A clean trace does not prove the code meets the requirement either: trace checks that the labels exist, not
  that the behavior is right.

World-substrate keeps trace out of its `make check` on purpose (its Makefile calls it "a separate failing
conformance target"). Its `lefthook.yml` lists trace as a blocking pre-commit check, but no pre-commit hook is
installed in that repository, so it never runs. If one were installed, every commit there would be refused
until the 196 findings are fixed.

## Scored against AES's own failure test

[GOAL.md](../architecture/GOAL.md), "Thesis disproof", says the bet is weakened if any of three things holds:

1. **Agents miss requirements present at their edits.** Never tested. No repository plans its code, so no
   requirement sits at a code edit to be missed. Question Q25 ("which consumer demonstrates" the full round
   trip) is open. Decision 0010 records "Value beyond mechanism is not demonstrated" (reader-reported).
2. **Projected documents conceal drift.** One real Claude edit refreshing two generated documents was observed
   on 2026-11-13 ([now.md](../../.project-brain/now.md)). Nothing at scale.
3. **Controls and upkeep cost more useful work than they protect.** The evidence there is leans this way
   (reader-reported):
   - whygame5's AES check found 0 problems where hand checks found 4, later 1 against 6 (decision 0011).
   - A replay of the old universal commit rule would have refused 99% of commits.
   - The planning package refused 3 merges on 2026-11-12 (now.md).

   Brian, 2026-10-26, about checks in general (not Lockstep): "all my agents are spending 99 percent of their
   time doing checks".

GOAL.md itself says "No improvement rate is claimed". Brian's own test, 2026-07-31: "Will this planning, test,
or instrumentation materially reduce expected time to a correct visible result?" Nothing measures that today.
The collector's corrections-per-session counts (reader-reported: 1.4, 0.8, 1.6 and 1.6 in weeks 41, 42, 46
and 47) cover every session in every repository, so they cannot show an effect of AES in either direction.

## What works

- The `lockstep` command is real and quick. In world-substrate: `lockstep check` 6.1 s, `trace` 9.0 s,
  `sources` 2.7 s, `docmeta` 1.3 s; the edit guard answers in about 1 s.
- The [2026-11-12 retirement record](../retired/2026-11-12.md) lists every retired path, the reason and a
  restore command.
- The `md_file_cap` port gave byte-identical output on 13 repositories
  ([evidence](../../evidence/runs/md-file-cap-equality-20261114.txt)).
- Concern 783 was checked with a negative control: its fix passes, and the commit before the fix fails.
- The documents say plainly what is not proven.

## Findings

1. **No outcome measure after nine weeks.** See the section above.
2. **Lockstep's alignment promise is not in force anywhere.**
   - 14 repositories have a `lockstep.yaml`; 13 list no planned files, so their edit guard has nothing to refuse.
   - Commit hooks are installed in 3 (AES, tbench-task-study, workspace); `make check` calls Lockstep in 5.
   - The checks that run at merge are `sources` and `plan check`, not `trace`.
   - AES's own `lockstep.yaml` lists no planned files ("narrow documentation self-adoption"); its `make check`
     has no `trace`, `changed` or `test-first` step. Brian, 2026-08-29: "we should dog food our approach by
     following our own policy."
   - Brian, 2026-11-05, said Lockstep should mean you "cant even have billing code without a plan for it". No
     repository's plan covers code today.
3. **The edit guard's use cannot be counted.** It writes its log into the checkout being edited
   (`src/lockstep/hook.py`, `_write_log`). Across `~/code2` there are 34 logged decisions in all, most of them
   replays. World-substrate had none between its 2026-11-12 setup and this assessment's probe, across 177
   commits. Inferred: logs written inside `claude -w` worktrees are deleted with the worktree after `ship`.
4. **The feedback loop collects and nothing reads it.**
   - The private feedback log holds 8,624 open reports and 0 closed; 7,059 arrived since 2026-11-01.
   - 2,276 (26%) are auto-generated "Subagent outcome" stubs. In a 30-report sample, 10 were specific and
     actionable (reader-reported).
   - No code closes or triages a report. The jobs that read them (weekly analysis, fix owner, effects) have been
     disabled since about 2026-10-12.
   - Their last output was 226 "Feedback loop: adopt" issues in this repository: 192 open, every one a
     proposal to add a check, and 34 closed between 10-08 and 10-13.
   - Brian, 2026-09-09: the loop "cant just leave feedback in a file that never gets acted on or requires me to
     remeber to trigger it." Brian, 2026-11-14, about the reading jobs: "i dont want to turn this stuff on"
     ([retirement plan](project-meta-retirement-plan.md)).
5. **About 8 to 10 restarts or re-scopings in nine weeks** (reader-reported):
   - v0.1 on 09-16 and v0.2 on 09-25;
   - the commit rule, built 10-06 and removed 10-14;
   - a hold on 10-18;
   - workspace decision 0009 and its three amendments on 11-10 and 11-11;
   - the 884-file cleanup on 11-12;
   - the goal rewrite on 11-13;
   - the Project Meta retirement and workspace split on 11-14.
6. **Consolidation and new checks have taken the work while the core is unproven.** Replacing the old systems
   is Brian's 2026-11-16 requirement, so its growth is not unapproved drift. But it and a run of new checks
   (changed requirements and document quotes on 11-17, plan size and prior-art on 11-18) arrived while trace,
   the guard and the feedback reading jobs were not in force. Since 2026-10-19 the docs, plans and evidence
   folders gained 50,915 lines and the code 24,705 (tests 18,850); most deletions in that window are the
   11-12 cleanup.
7. **The documents work against AES's own idea**, which is to put the current, relevant intent where the agent
   works.
   - `now.md`, which every agent reads first, is 261 lines in nine dated sections.
   - It says the fix owner "has closed all 24 adopt issues" (a 2026-10-12 snapshot; 192 of 226 are open).
   - The Project Meta retirement plan says "Nothing below has been done" while marking slices done
     (reader-reported).
   - 28 of 48 questions are open; about 8 overlap (Q19 and Q24; Q22, Q25 and Q31; Q34 with Q6, Q13 and Q16;
     Q35 with Q20); Q21 is answered by Brian's 2026-11-14 words; Q2 has been open since 09-26.
   - 435 issues are open in this repository; 476 were opened in two October weeks and 67 of those were closed.
   - The repository fails its own Markdown check on main: 256 Markdown files against the recorded 136 exception
     and 67 reader documents not reachable from `wiki/index.md`.
8. **No comparison with spec-driven coding tools was found.** These tools set out to do what Brian's
   description says: plan, implement and keep the plan aligned with the code. Examples are GitHub Spec Kit,
   AWS Kiro, Tessl and BMAD-METHOD, alongside OpenSpec, which is already in use. Searching AES, Company
   Planning and workspace documents for those names found no comparison. The tool list comes from the
   assessor's knowledge and was not checked on the web on 2026-11-19.

## Advice, in order

1. Stop adding to AES until one pilot has numbers (Decision 1).
2. Run Lockstep for real in one place, with the guard in warn mode, which logs what it would refuse and blocks
   nobody. Judge it with Brian's 2026-07-31 question (Decision 2).
3. Stop filing feedback that nothing reads (Decision 3).
4. Before building more of Lockstep, run a landscape review of the spec-driven tools in finding 8 against
   Lockstep's distinct parts: the edit guard, requirement text in docstrings, and trace.
5. Cleanup, which needs no product decision:
   - cut `now.md` to the current state and fix its contradiction;
   - close Q21 and merge the overlapping questions;
   - close the 192 adopt proposals as not planned (they can be reopened);
   - move aside the stale checkouts `~/code2/lockstep` (with its `plan-code-wiki` link) and the `-doc-roles` and
     `-lockstep-docs` checkouts, whose commits are already in main by patch, after comparing their contents.

## Decisions open for Brian

1. **What is AES?**
   - (A) The agentic coding system in Brian's 2026-11-19 description: planning, implementation help and
     plan-code alignment. New capabilities, ports and checks pause for about two weeks; bug fixes and the
     Project Meta retirement already under way continue.
   - (B) The single home for all agent infrastructure (Brian, 2026-11-16), so consolidation keeps its current
     pace.
   - Recommendation: A for the next two weeks, medium confidence. The consolidation requirement stands, but
     nothing yet shows the core works.
   - Answer: "D1 A" or "D1 B".
2. **Two-week Lockstep pilot in world-substrate.**
   - Extend the guard to `src/` in warn mode and write its log where it survives worktree deletion.
   - Work the 196 trace findings down.
   - Then count how many would-be refusals were real mistakes and the seconds each commit costs.
   - Keep the guard and trace if they catch at least 3 real mistakes for under 15 seconds per commit. Both
     thresholds are the assessor's guess.
   - Answer: "D2 yes", "D2 yes with <numbers>" or "D2 use <repository>".
3. **Feedback loop.**
   - (A) Stop filing the subagent stubs, keep human corrections, and run the weekly analysis once by hand so
     Brian can judge one digest before any timer goes on.
   - (B) Pause the collector.
   - (C) Leave it.
   - Recommendation: A, medium confidence.
   - Answer: "D3 A", "D3 B" or "D3 C".

## Corrections made during the assessment

- The assessor first read the 13 empty plans as "Lockstep's checks run nowhere". In fact `make check` runs
  `lockstep check sources` and `plan check` at merge in 5 repositories.
- The first report described AES's growth since 2026-11-13 as scope creep. Brian's 2026-11-16 statement makes
  replacing the old systems a requirement of the goal, so finding 6 is narrower: consolidation has taken the
  work while the core is unproven.
- Added 2026-11-19, after the report: the assessment counted plans only in the `lockstep.yaml` format and said
  only world-substrate lists planned files. Two company repositories (Team-Brains, plan last changed 2026-11-10, and
  one integration repository, plan last changed 2026-11-03) also have plans in the old `.aes/target.yaml` format, which current
  Lockstep still reads (`src/lockstep/aes_bridge.py:180-191`). The brain pull-request runner in Team-Brains
  checks a change against the plan only when the base has `.aes/project.yaml` or `.aes/target.yaml`
  (`deploy/organizational-brains/brain_pr_runner.py:21-23`), so a repository planned only in `lockstep.yaml`
  would go unchecked by it (inferred from the code, not run). Finding 2 stands for the `lockstep.yaml` format.
  Lessons from the older systems: [lessons-from-older-systems-20261119.md](lessons-from-older-systems-20261119.md).

## Evidence

All counts measured on 2026-11-19 unless marked.

- Commits: `git log` in this repository: 1,523 commits; by month 411 (September), 666 (October), 446
  (November to the 18th).
- Line churn since 2026-10-19: `git log --since=2026-10-19 --numstat`, grouped by top folder.
- Lockstep plans and hooks: each `~/code2/*/lockstep.yaml` read for `governed:` and `layout:`; each
  repository's git common directory checked for `hooks/pre-commit`; each Makefile searched for `lockstep`.
- Check timings and trace counts: `uvx --from git+https://github.com/BrianMills2718/agentic-engineering-system-canonical lockstep check <name>`
  in world-substrate; trace exit 1, `RESULT trace findings=196`; 109 untested, 58 unimplemented, 29 unknown.
- Guard logs: `find ~/code2 -maxdepth 7 -path '*/.lockstep/hook-*.jsonl'` (and `.pcw`): 34 decisions (14 allow,
  14 deny, 3 would_block, 3 pass).
- Guard probe: a PreToolUse event for a new file `src/world_substrate/zz_probe_unplanned.py`, sent to
  `lockstep-hook` with `PCW_MODE=block`: exit 0, decision `pass`, why `no_rule`, about 1 s.
- Feedback log: GitHub issue search on the private log: 8,624 open, 0 closed, 7,059 created since 2026-11-01,
  2,276 titles containing "Subagent outcome".
- Adopt issues: GitHub issue search in this repository for titles "Feedback loop: adopt": 192 open, 34 closed.
- Issues per week: `gh issue list --state all --limit 1000` in this repository: 515 issues, 435 open.
- Timers: `systemctl --user` shows `feedback-collector` and `feedback-labels` enabled (exit 0 on 2026-11-19);
  `feedback-problems`, `feedback-fix-owner` and `feedback-effects` disabled, no journal entries; their unit
  files last changed 2026-10-12.
- Markdown check: `python3 scripts/md_file_cap.py --repo .` on main: `md=256 cap=over reach=orphans(67)`, exit 1.
- Prior-art search: `grep -ril` for spec-kit, Kiro, Tessl and BMAD across this repository's `docs`, `proposals`,
  `wiki`, `openspec` and `raw`, Company Planning's `docs` and workspace `docs`: one hit, a raw Reddit capture.
- Brian's words: found with the `brian-positions` search over his chats and sessions; quoted with dates as
  returned. The 2026-11-14 quote is as recorded in the retirement plan; the archive search did not return it.

## Limits

- The test suite of this repository was not run.
- Whether Claude Code and Codex trust and load the project hooks in world-substrate was not checked.
- No cost figure: AES work ran on Claude Code and Codex subscriptions, which `llm-cost` does not cover. 230
  Claude session transcripts sit in this repository's Claude project folder.
- Reader-reported items were counted by subagents and not re-run.

## Side effects of the assessment

- The probe wrote `~/code2/world-substrate/.lockstep/hook-2026-11-19.jsonl` (one line, `tool_use_id`
  `assessment-probe-1`; the folder is ignored by git). It is not a sign of the guard running on real work.
  Undo: delete the file.
- A reader ran `git fetch` in the `-doc-roles` and `-lockstep-docs` checkouts; that updates remote refs only.

---
description: One-page plan for replacing Brian's old overlapping agent systems with one AES canonical system, ranked against the confirmed goal
doc_role: planning
status: proposed
---

# AES consolidation plan (one page)

## Goal, requirement, path

Source: Brian, 2026-11-16, answering which sentence is the end goal ("option A is the goal, option B is the
current path to get there. option C is a requirement of the option A goal").

| | Statement | Where it comes from |
| --- | --- | --- |
| **Goal** | Autonomous, effective coding agents | [GOAL.md](../architecture/GOAL.md) (Brian, 2026-11-06) |
| **Requirement of the goal** | One consistent, shareable, configurable AES canonical system that replaces the many old overlapping, unfinished and contradictory systems | Brian, 2026-11-16 |
| **Current path** | Brian can see his whole setup, trust what it tells him, and start clean without losing anything | the workspace harness goal (north star) |

The Project Meta retirement is a few cells of this, not the plan. Why Project Meta had grown into the whole
plan: it was the next unfinished item in a plan that ranked only its own steps. Nothing ranked it against the rest.

## What was checked

The harness grid (6 parts by 5 loop steps) on the workspace branch `shaping/harness-grid` maps 127 items; the
2026-11-07 row reviews add more. Five read-only reviewers, one per part, assessed 169 item entries against the
machine on 2026-11-16 ([evidence](harness-grid-review-20261116.md)). Limits, stated plainly:

- The 169 are entries, not distinct items: an item that sits in two parts is counted in both, and the parts
  sometimes classed the same item differently (for example `ecosystem-ops` and `agent-deck-web` are "leave" in the
  Work flow part and "retire" in the Human interface part; `oversight-page` is "retire" in Context and "finish" in
  Human interface). Those disagreements are to be settled item by item when its work starts.
- Some entries were not checked at all (for example `dashboard-tunnel`, `ask-agent`, `voice-mode`; no ssh to the
  Mac mini, the VPS or the desktop WSL), and a few of those are still classed. Each part file lists its limits.
- The counts come from the reviewers' own tables. An independent read summed them (169 = 5+21+23+23+55+34+8) and
  re-ran four counts (10 failed services, 84 timers, 6 entries in the AES job list, 42 timer files linked into git).

| Class | Entries | Meaning |
| --- | ---: | --- |
| AES already provides it | 5 | nothing to do |
| AES provides part of it | 21 | finish it |
| Valuable, not in AES yet | 23 | port it |
| A standard tool does it | 23 | AES only configures it |
| Works, not AES's concern | 55 | leave it |
| Obsolete, duplicated or contradicted | 34 | retire it |
| Cannot tell yet | 8 | name the missing check |

## What is wrong today

Labels: "checked" = the plan author or the independent read ran the command on 2026-11-16; "reviewer's reading" =
taken from a part file, not re-run.

1. **The learning half of AES does not run.** The nightly collector exited 1 at 04:03 with 50 errors (checked,
   `journalctl`). That was the old unit; the unit installed from the job list later that day has not run yet (first
   run 03:30 on 2026-11-17) and no longer files through Project Meta. `skill-review` and `router-feedback` failed
   with an OpenRouter 402, low credit (reviewer's reading); that one is a credit decision for Brian, not a
   debugging task. The three stages that turn lessons into fixes are still switched off. Ten user services are
   failed now (checked, `systemctl --user list-units --failed`), including `gates-nightly` (failed after about
   three hours of CPU) and `local-data-backup` (a "lose nothing" risk), both reviewer's reading.
2. **Judging agents run on Sonnet** (23 times in two days, `subagent_models.py`). **Checked 2026-11-16: this is by
   design, not a defect.** The usage-pace level is 2 because the Codex weekly limit reads fully used until its
   reset on 2026-11-20 (`latest.json`, `usage-pace` journal); the rule in `llm-calls.md` lowers judges to Sonnet
   under usage pressure. Left open: that reading is two days old and the usage reader currently fails.
3. **Rules are split across homes.** An old `~/projects/.claude/AGENTS.md` (dated 2026-11-07) is still loaded
   into sessions; its only wrong parts are two stale pointers to Project Meta's workspace map (checked, lines 13
   and 17), and it otherwise defers to `core.md`. 174 memory notes are visible to Claude only (reviewer's reading).
4. **A clean machine would lose jobs.** 84 timers on this laptop; the AES job list renders 6; 42 timer files are
   linked into git (checked by the independent read).
5. **What an agent can reach is guarded only by hooks.** (Checked 2026-11-16, corrects the part reviewers' reading:
   the safety-hook rulebook is in git, `workspace/config/cc-safety-net/`, byte-identical to the installed copy, and
   already blocks `gh repo delete`, `gh api` DELETE, `rclone` purge and delete, and `ssh` remote removes; whether
   each block fires today was not re-tested.) Commit-time checks are also switched off by `~/.config/git/repo-hooks.off` (reviewer's reading).
6. **The two tools every change touches, `ship` and `lane-sweep`, live only in the private workspace repository,**
   not in AES (reviewer's reading).
7. **Two facts that disagree with what you decided or documented** (reviewer's reading; for you, not for me to
   settle): the "WSL Rebuild" task shows as a one-time 3 AM run with no next run, while the core rules describe a
   standing 2pm yes; `compliance-list.timer` is enabled, while you said on 2026-11-09 "turn off all nightly
   planning" (the independent read confirmed it is enabled).

## Ranked plan

Ranking test: goal-serving work first (agents more effective now); within that, small before medium; then work
the requirement needs (one consistent system), ordered by what a clean start depends on; path work (seeing and
trusting) follows the work that feeds it. Sizes are guesses unless noted.

| # | Work | Serves | Size | Why here |
| ---: | --- | --- | --- | --- |
| 1 | Make the learning loop run: read why the collector had 50 errors, check the new unit's first run, then decide on the three disabled repair stages | goal | small to medium | The loop is AES's reason to exist; it is failing now. |
| 2 | Make the model rule and the router agree, and run the model check daily | goal | small | The biggest direct loss of agent quality; one setting and one timer. |
| 3 | Put the safety-hook rulebook in git; add the three missing delete rules | goal, path | small | What an agent can reach is the least-guarded part. |
| 4 | Fix or retire each of the ten failed services (naming `gates-nightly` and `local-data-backup` first) | path | small each | The hub shows these as broken; each is one decision. |
| 5 | Move aside the old rulebook with its stale pointers (compare first, per the core rules) | requirement | small | Cheap; removes a pointer to a system being retired. |
| 6 | One manifest of the whole machine layer (84 timers, Windows tasks, Mac, VPS) in `aes-config` | requirement, path | medium | This is what makes a clean start without losing jobs possible; the part reviewer's own first priority. |
| 7 | Port `ship` and `lane-sweep` into AES | requirement | medium | Every change uses them; both already work, so it is a move. |
| 8 | One source for rules (core.md, 17 topic files, AES docs and 174 notes overlap); retire code2check where Lockstep covers it | requirement | medium | Removes the rest of the contradiction. |
| 9 | Model defaults and plugin settings into the manifest | requirement | small to medium | Hooks already flow from git this way; models do not. |
| 10 | The hourly front page as the one hub inside AES, "Needs you" on top | path | medium | It serves seeing and trusting, once the sources feeding it work. |
| 11 | Finish Project Meta: ask for the archive yes | requirement | small (one yes) | Nearly all its live jobs now run from AES. Last, because it removes a source of contradiction rather than raising effectiveness. |

Needs Brian, not ranked: whether Company Planning belongs inside AES; the OpenRouter credit; the WSL Rebuild and
`compliance-list.timer` facts in item 7 above; whether `repo-hooks.off` is intended.

## Done already toward this plan

Project Meta's retirement plan steps 3 to 6 (AES #903 to #912) and ecosystem-ops #207: the five-gate repair
verifier, the project graph and its checks, the job list and installer, the failed-unit watch, the workspace
check, the graph refresh and the checkout sync now run from AES copies.

## Independent read

One independent read was done on 2026-11-16 (verdict: revise). Its findings are applied in this version:
overlapping entries and unchecked items stated; the learning-loop item split into debugging and the credit
decision; the old rulebook described as stale pointers, not a contradiction; the ranking reordered to follow its
test; missing items added; unlabelled claims labelled. This version has not had a second read.

## Progress, 2026-11-16 (Decision 25: Brian approved items 1 to 5)

| # | Result |
| ---: | --- |
| 1 | Cause found (checked, journals): the OpenRouter key has no credit. It stops five of the ten failed services: `feedback-collector` (50 errors), `router-feedback`, `skill-review`, `foia-page-refresh`, and the model step of `projects-refresh`. This is a credit decision for Brian, not code; nothing to fix here. The three repair stages stay off. |
| 2 | Closed as by design (see "What is wrong today", 2). |
| 3 | Already done: the rulebook is in git and identical to the installed copy; the delete rules exist. |
| 4 | Ten failures have six causes: no OpenRouter credit (5); `usage-pace` reads a wrong account login (Brian, 2026-11-11: not a concern); `client-config-drift`: **fixed**, the manifest now lists the Fable models already live (agent-skills #613; `client-config-check` drift=0); `gates-nightly`: four repositories' own checks fail (company-planning, digimon, process_tracing, vision) and `openrouter-bypass` grew by three files; `projects-refresh`: also a missing `code2check` command in the workspace virtual environment; `brent-us-sources` (sources step exit 3) and `foia-tracker` (exit 2 after 15 minutes) belong to other projects and are not diagnosed. |
| 5 | Done: `~/projects/.claude/AGENTS.md` is an index to the topic files, not a competing rulebook; its two pointers to Project Meta's workspace map now point at the AES workspace check (projects-dotclaude #133). |
| 6 | Slice 1 (AES #917): `scripts/machine_manifest.py build` and `check`; the manifest `machine-layer.yaml` is in `aes-config`: 119 units, 275 files, 115 local-only. **Slice 2 (this change):** the 115 local-only unit and drop-in files are copied verbatim into `aes-config/machine-units/` (commit `b02c16e`, branch `shaping/machine-units`; scanned for secret values, none found, none held back) and the one symlink outside git (`desktop-commander-remote.service` to `/dev/null`) is recorded as its link target text. New `machine_manifest.py check-units` (disk against repository copies; checked: same 115, differ 0, missing 0) and `install-units` (dry run unless `--apply`; backs up a differing file first; never deletes; skips symlinks; reload only with `--daemon-reload`; not run for real). Still open: 15 scripts the units run are in no git repository, and wiring a clean-machine install into the rebuild. |
| 7 | Slice 1: `scripts/ship.py`, `scripts/lane_sweep.py` and `scripts/plan_content.py` (ship's push-hook helper) copied into AES from code2-workspace commit `eafa8e0`, with their tests (`tests/test_ship.py` 83, `tests/test_lane_sweep.py` 36; every test marked `req`) and specs (`openspec/specs/ship`, `openspec/specs/lane-sweep`). Private values became settings in `aes-config` `graph-config.yaml` (branch `m7-ship-config`, commit `92794e1`, not on main: aes-config's first commit is 2026-11-16 and it has no planning package, so `ship` refuses it): the plan-list checkout and path (`plan_list_checkout`, `plan_list_path`) and the canonical-lock tool (`canonical_lock`); the gh wrapper per account reuses the existing `github_accounts` and `owner`. Side by side (checked): `--help` identical for all three; refusal runs (on main, dirty tree) identical; the plan-list check (`plan_list_refusal`, the code that changed) gives the same verdict on a listed, an unlisted and an unknown repository with the AES copy reading the `m7-ship-config` settings, and with no settings it refuses with "no plan list is named"; `lane-sweep --no-fetch` dry runs started together (AES copy with `PROJECT_GRAPH` on the `m7-ship-config` checkout): 210 repositories, normalized diff 0 lines, identical summary lines; the code differs only in the config hunks (ship 9, lane_sweep 5, plan_content 0). Merged as AES #920 (`3dde133`). The slot test `test_a_slot_that_frees_lets_the_check_run` failed now and then (5 failures in the ship logs, 2026-11-09 to 2026-11-16): it freed the slot on the first `time.sleep`, which `subprocess.run` with a timeout also calls; it now frees the slot when ship says it is waiting (the workspace copy still has the old test). Slice 2, switch-over (2026-11-16): settings landed on aes-config main (`ed596be`); the runtime clone `~/.hive-brain/aes` is at `f558f0a` (settings read from `~/code2/aes-config/graph-config.yaml`). Before switching, side by side on throwaway repositories with a local bare remote and a fake `gh`: `--help` identical for all three scripts, refusals (on main, dirty tree, new repository with no package) identical, a full `--keep-lane` merge identical apart from timings, `lane-sweep --no-fetch` over 210 repositories identical apart from idle-minute counters and one lane that aged out. Then `~/.local/bin/ship` and `lane-sweep` were repointed at `~/.hive-brain/aes/scripts/`, `lane-sweep.service` runs from that clone (code2-workspace #459), `planning-gate.sh` defaults `PLANNING_GATE_PLAN_CONTENT` to the AES copy (personal-file-infra #296), and `systemctl --user start lane-sweep.service` exited 0. Rollback: `~/archive/ship-switch-20261116/rollback.sh`. This row's own merge ran through the new `ship`. Still open: retire the workspace copies after re-diffing against `eafa8e0`. |
| 8 | Investigation only, nothing changed ([report](item8-rules-and-code2check-20261116.md)). Lockstep has an equivalent for all 8 code2check commands; on 2 repositories 7 gave identical counts and exit codes and 2 differ only by the tool name in generated headers (one regenerate each). 13 repositories already run Lockstep; code2check is still called by 2 Makefiles (`code2-template`, `real-chrome`), 3 lefthook files, the live edit hook in `~/.claude/settings.json` and `~/.codex/hooks.json`, and `workspace/proposals/oversight/requirements.py` (the missing-command cause in row 4). Rules: `core.md` plus the 17 topic files are the one source both clients load; 88 of 174 memory notes are cited from them, 86 are not; 17 contradiction or drift items found between rule files (for example claims still instructed after being retired, WSL wording, `ship` default check) and about 5 memory notes that contradict them. Proposed slice: 7 technical items and 4 decisions for Brian, in the report. **Technical slice (T1, T2, T3, T5 factual part), 2026-11-16:** T2 done: `code2-template`'s own Makefile, lefthook and AGENTS.md call `lockstep check`, Lockstep is a dev dependency, one regenerate changed 5 lines in 3 files (header and marker names); `make check` exit 0 (120 tests), merged code2-template #31 (`00bd28c`). `.compliance-list-page` needs no change: it is a worktree of code2-workspace on the timer's page branch (`shaping/compliance-list`, committed with `--no-verify`, 659 commits behind main), and workspace main already runs Lockstep; shipping it would merge the page branch into main. T3 done: `requirements.py` runs `lockstep check sources --repo R --json` and reads Makefiles with either line; run locally, before exit 1 (no `code2check` in the venv), after `repos=14 items=485 inferred=135 failed=0 exit=0`; merged code2-workspace #460 (`21ce291`). T5 factual part done: `agents/index.md` core.md line count (135 to 257) and `topics/orientation.md` map pointer (to the AES `workspace_map_alert.py` check and `aes-config`), code2-workspace #461 (`2be46e9`); the register's source line and the `RULES.md` intro now name `agents/core.md` and its topic files (this change). T1 blocked: the real-chrome `lockstep-switch` branch passes `make check` (exit 0, 14 passed, 3 skipped) and its regenerate was already in the branch (`rewrote=0`), but `ship` stops at the planning gate (exit 1, nothing pushed): the package fails 5 substance checks added since 2026-11-13 (cost basis, plain baseline, stage effects, stops) and is out of date since its cold review (real-chrome issue #1). It needs a planning-compliance pass first. Left untouched because they state what agents must do: the claims sentences in `authority-and-escalation.md:51-54`, `reviews-pages-and-finishing.md:15-16`, `git-and-repositories.md:91-92` (the named claims script still exists), the "under 200 lines" sentence in `index.md` (core.md now breaks it), and the topic-file banners. Not done: T4, T6, T7. |

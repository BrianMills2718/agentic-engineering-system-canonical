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
| 11 | Finish Project Meta: ask for the archive yes | requirement | small (one yes) | **Done 2026-11-17 (Decision 30 A).** Nearly all its live jobs now run from AES. Last, because it removes a source of contradiction rather than raising effectiveness. |

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
| 6 | Slice 1 (AES #917): `scripts/machine_manifest.py build` and `check`; the manifest `machine-layer.yaml` is in `aes-config`: 119 units, 275 files, 115 local-only. **Slice 2 (this change):** the 115 local-only unit and drop-in files are copied verbatim into `aes-config/machine-units/` (commit `b02c16e`, branch `shaping/machine-units`; scanned for secret values, none found, none held back) and the one symlink outside git (`desktop-commander-remote.service` to `/dev/null`) is recorded as its link target text. New `machine_manifest.py check-units` (disk against repository copies; checked: same 115, differ 0, missing 0) and `install-units` (dry run unless `--apply`; backs up a differing file first; never deletes; skips symlinks; reload only with `--daemon-reload`; not run for real). **Refresh 2026-11-17:** `build` gave 120 units, 277 files (new: the `hub-page` job-list unit; changed by others since slice 1: `failed-unit-watch` is now a job-list unit and `lane-sweep` runs its AES script); aes-config #7, `5e75e5a`. No new local-only files (115 before and after). `check` now counts a local-only file or a recorded link whose `machine-units` copy is identical under (e), which does not fail; a missing or differing copy or no units folder fails as before (AES #934, `bda6696`). Checked: `check` (a) 0, (b) 0, (c) 0, (d) 0, (e) 116, exit 0; `check-units` same 115, differ 0, missing 0, links same 1, exit 0. **Slice 3 (2026-11-17):** the 15 scripts the units run that were in no git repository, re-verified with readlink and by hashing against every same-named and same-sized file under `~/code2` and `~/projects` and against `origin/main`: 6 copied verbatim into `aes-config/machine-bin/` (no copy anywhere; gitleaks no leaks, read for secrets), 5 recorded as byte-identical to a committed repository file (2 of them re-extracted from personal-vps before every run; `credit_alert.py` is the progressive-air copy), 2 recorded as installed tools (agent-deck v1.16.39 binary, llm-cost entry point of llm-client 0.7.1), 2 left as `missing` (`show_replies.py` is a VPS path absent here; `basic-memory`'s venv is gone and its unit disabled); the OS programs `make` and `systemd-socket-proxyd` are recorded with their apt versions. `machine-layer.yaml` gained hand-written `scripts` (19 records), `windows_layer` (11 harness scheduled tasks of 27 outside `\Microsoft\`; 2 more scripts copied: `compact-idle.ps1`, `sync_agent_session_catalog.py`) and `other_machines` (Mac mini and VPS from repository files only, marked not checked: no access from this session); `build --out` keeps them. `machine_manifest.py check` fails on (f), a unit script outside git with no record; new `check-scripts` and `install-scripts` (dry run unless `--apply`, backs up first, never deletes, never writes through a symlink; not run for real). Checked: `check` (a)-(d) 0, (e) 116, (f) 0, exit 0 (the old manifest gives (f) 15, exit 1); `check-units` same 115, exit 0; `check-scripts` copied same 8, repo files same 5, tools present 4, missing 2, exit 0. **Update 2026-11-17:** `WSL-Rebuild.xml` was re-exported (code2-workspace #834: daily 03:00, `-OnlyIfFreeBelowGB 35`), so `install-tasks.ps1` now registers the right rebuild. The Windows task `LLM Provider Registration Drift Monitor` is reported, not unknown: its script is gone (the task was registered by a Codex session on 2026-08-28) and its definition is still in `windows/scheduled-tasks/`; deleting the task and the file is left for Brian. The clean-machine install is wired into the documented restore path: personal-file-infra `docs/MACHINE.md`, "Clean machine: put the jobs back" (#305) lists `install-units`, `install-scripts`, `client_settings_sync.py apply` and `install-tasks.ps1`, each dry run first; dry runs 2026-11-17: `install-units` 1 new (`rstg-inbox.service`), `install-scripts` 0, `install-tasks.ps1 -Check` 11 present 0 missing, all exit 0; none applied. Still open: the Mac mini and VPS are unchecked. |
| 7 | Slice 1: `scripts/ship.py`, `scripts/lane_sweep.py` and `scripts/plan_content.py` (ship's push-hook helper) copied into AES from code2-workspace commit `eafa8e0`, with their tests (`tests/test_ship.py` 83, `tests/test_lane_sweep.py` 36; every test marked `req`) and specs (`openspec/specs/ship`, `openspec/specs/lane-sweep`). Private values became settings in `aes-config` `graph-config.yaml` (branch `m7-ship-config`, commit `92794e1`, not on main: aes-config's first commit is 2026-11-16 and it has no planning package, so `ship` refuses it): the plan-list checkout and path (`plan_list_checkout`, `plan_list_path`) and the canonical-lock tool (`canonical_lock`); the gh wrapper per account reuses the existing `github_accounts` and `owner`. Side by side (checked): `--help` identical for all three; refusal runs (on main, dirty tree) identical; the plan-list check (`plan_list_refusal`, the code that changed) gives the same verdict on a listed, an unlisted and an unknown repository with the AES copy reading the `m7-ship-config` settings, and with no settings it refuses with "no plan list is named"; `lane-sweep --no-fetch` dry runs started together (AES copy with `PROJECT_GRAPH` on the `m7-ship-config` checkout): 210 repositories, normalized diff 0 lines, identical summary lines; the code differs only in the config hunks (ship 9, lane_sweep 5, plan_content 0). Merged as AES #920 (`3dde133`). The slot test `test_a_slot_that_frees_lets_the_check_run` failed now and then (5 failures in the ship logs, 2026-11-09 to 2026-11-16): it freed the slot on the first `time.sleep`, which `subprocess.run` with a timeout also calls; it now frees the slot when ship says it is waiting (the workspace copy still has the old test). Slice 2, switch-over (2026-11-16): settings landed on aes-config main (`ed596be`); the runtime clone `~/.hive-brain/aes` is at `f558f0a` (settings read from `~/code2/aes-config/graph-config.yaml`). Before switching, side by side on throwaway repositories with a local bare remote and a fake `gh`: `--help` identical for all three scripts, refusals (on main, dirty tree, new repository with no package) identical, a full `--keep-lane` merge identical apart from timings, `lane-sweep --no-fetch` over 210 repositories identical apart from idle-minute counters and one lane that aged out. Then `~/.local/bin/ship` and `lane-sweep` were repointed at `~/.hive-brain/aes/scripts/`, `lane-sweep.service` runs from that clone (code2-workspace #459), `planning-gate.sh` defaults `PLANNING_GATE_PLAN_CONTENT` to the AES copy (personal-file-infra #296), and `systemctl --user start lane-sweep.service` exited 0. Rollback: `~/archive/ship-switch-20261116/rollback.sh`. This row's own merge ran through the new `ship`. Still open: retire the workspace copies after re-diffing against `eafa8e0`. |
| 8 | Investigation only, nothing changed ([report](item8-rules-and-code2check-20261116.md)). Lockstep has an equivalent for all 8 code2check commands; on 2 repositories 7 gave identical counts and exit codes and 2 differ only by the tool name in generated headers (one regenerate each). 13 repositories already run Lockstep; code2check is still called by 2 Makefiles (`code2-template`, `real-chrome`), 3 lefthook files, the live edit hook in `~/.claude/settings.json` and `~/.codex/hooks.json`, and `workspace/proposals/oversight/requirements.py` (the missing-command cause in row 4). Rules: `core.md` plus the 17 topic files are the one source both clients load; 88 of 174 memory notes are cited from them, 86 are not; 17 contradiction or drift items found between rule files (for example claims still instructed after being retired, WSL wording, `ship` default check) and about 5 memory notes that contradict them. Proposed slice: 7 technical items and 4 decisions for Brian, in the report. **Technical slice (T1, T2, T3, T5 factual part), 2026-11-16:** T2 done: `code2-template`'s own Makefile, lefthook and AGENTS.md call `lockstep check`, Lockstep is a dev dependency, one regenerate changed 5 lines in 3 files (header and marker names); `make check` exit 0 (120 tests), merged code2-template #31 (`00bd28c`). `.compliance-list-page` needs no change: it is a worktree of code2-workspace on the timer's page branch (`shaping/compliance-list`, committed with `--no-verify`, 659 commits behind main), and workspace main already runs Lockstep; shipping it would merge the page branch into main. T3 done: `requirements.py` runs `lockstep check sources --repo R --json` and reads Makefiles with either line; run locally, before exit 1 (no `code2check` in the venv), after `repos=14 items=485 inferred=135 failed=0 exit=0`; merged code2-workspace #460 (`21ce291`). T5 factual part done: `agents/index.md` core.md line count (135 to 257) and `topics/orientation.md` map pointer (to the AES `workspace_map_alert.py` check and `aes-config`), code2-workspace #461 (`2be46e9`); the register's source line and the `RULES.md` intro now name `agents/core.md` and its topic files (this change). T1 blocked: the real-chrome `lockstep-switch` branch passes `make check` (exit 0, 14 passed, 3 skipped) and its regenerate was already in the branch (`rewrote=0`), but `ship` stops at the planning gate (exit 1, nothing pushed): the package fails 5 substance checks added since 2026-11-13 (cost basis, plain baseline, stage effects, stops) and is out of date since its cold review (real-chrome issue #1). It needs a planning-compliance pass first. Left untouched because they state what agents must do: the claims sentences in `authority-and-escalation.md:51-54`, `reviews-pages-and-finishing.md:15-16`, `git-and-repositories.md:91-92` (the named claims script still exists), the "under 200 lines" sentence in `index.md` (core.md now breaks it), and the topic-file banners. Not done: T4, T6, T7. |
| 9 | Slice 1: most of this was already in git. agent-skills `.rulesync/client-settings.jsonc` holds models, per-model effort, `enabledPlugins`, marketplaces and `pluginConfigs` for Claude and plugin switches for Codex, and rulesync holds hooks and MCP servers (checked: `client_settings_sync.py check` drift 0; MCP names on disk equal `mcp.jsonc` for both clients, 0 extra, 0 missing). What was in no repository: 27 settings, among them Claude `advisorModel` and `disableAllHooks`, Codex `approvals_reviewer`, `service_tier`, `features.hooks`, the three `project_doc_*`/`project_root_markers` keys, the three Codex marketplaces, `skills.config` and the built-in Claude marketplace. New `scripts/client_manifest.py build` and `check` (spec `openspec/specs/client-manifest`, 6 tests): every setting on disk gets an owner (agent-skills client-settings 46, rulesync 20, runtime 5, this manifest 27); the manifest holds a value only for the 27 nobody owns, so no value has two sources; credentials are never written (checked: 0 of 135 key values from `~/.secrets/api_keys.env` in the file). The manifest is `aes-config/client-layer.yaml` (aes-config #2, `b8469f3`); `check`: same 98, differ 0, missing 0, unrecorded 0, exit 0. Settings that look wrong, listed, not changed: Codex `model` is `gpt-6-luna` while the seed and Brian's 2026-11-09 words say `gpt-6.1-sol`; Codex `features.hooks = false` while rulesync installs Codex hooks; Codex `skills.config` switches off 7 skills at `~/code/active/agent-skills/...` paths that no longer exist; Claude `modelSettings` has `claude-fable-5-1`, which `availableModels` lacks; the Safety Net hook runs `~/projects/.agents/hooks/safety_net_cwd_fallback.py` or, without it, the cached copy of the disabled `cc-safety-net` plugin, so a clean machine without that cache or script has no Safety Net. Also noted: Claude `model` is `sonnet` live against the `opus` seed, by design, with three writers (/model, usage-pace, agents); model-router `routeAll=true` against the written Opus rule for judging agents is item 2, closed as by design; the Claude company-planning plugin's version `0.2.0+codex.20261116212227` comes from the company-planning marketplace itself (install path under `cache/inside-success`). Not covered: the 3 claude.ai-synced plugin folders (vendor-pushed), installed Codex plugin versions (only the switches), per-project MCP entries in `~/.claude.json`; owners are read from the agent-skills primary checkout, so an uncommitted edit there moves owners. Slice 2 (2026-11-17): the 27 values moved into agent-skills `.rulesync/client-settings.jsonc` (agent-skills #618, `c638984`), so one command, `client_settings_sync.py apply`, restores them on a clean machine (checked: a dry-run against an empty home lists all 27 among 65 writes). Hand-picked UI choices (Claude `advisorModel`, `theme`, `tui`, `verbose`, `voice`, `voiceEnabled`; Codex `approvals_reviewer`, `service_tier`, `tui.*`) are `defaults_only`, written only when missing, so a menu change is not drift. `aes-config/client-layer.yaml` was rebuilt (aes-config #19, `02e365d`): owners agent-skills client-settings 62, seeded by client-settings 14, rulesync 20, runtime 2, client-layer 0, and no entry holds a value; `check`: same 98, differ 0, missing 0, unrecorded 0, exit 0. Applied to the laptop after a dry-run named exactly the intended keys (backups in `~/archive/client-settings-20261117/`): Claude `extraKnownMarketplaces` gained `claude-plugins-official`, and Codex `skills.config`'s 7 switch-offs moved from `~/code/active/agent-skills/...` to `~/code2/agent-skills/skills/...`; nothing else changed (`client_settings_sync.py check` drift 0). Correction to slice 1: those 7 paths were not stale. `~/code/active/agent-skills` is a symlink into `~/code2`, and agent-skills `sync_skills.py` requires each switch-off because the company-planning plugin replaces those skills; emptying the list failed that check, so they were repointed. Nightly: the agent-skills `client-config-check` target, run by the `client-config-drift` unit at 03:40, already ran `client_settings_sync.py check` and now also runs `client_manifest.py check` (new target `client-manifest-check`; run under the unit's PATH: exit 0). Kept as found, reported: Codex `features.hooks = false` while rulesync installs Codex hooks (no recorded decision for Codex hooks); `claude-fable-5-1` stays in `modelSettings` because model-router spawns its `long` tier on it (`hooks/lib/pricing.ts`), though `availableModels` lacks it. Not covered still: claude.ai-synced plugin folders, installed Codex plugin versions, per-project MCP entries in `~/.claude.json`. |
| 10 | Slice 1: `scripts/hub_page.py` (spec `openspec/specs/hub-page`, 9 tests in `tests/test_hub_page.py`, every one marked `req`) builds a hub page beside the old front page, which is unchanged. Needs you comes first and reads four sources, each shown as Not checked when unread: open `waiting:brian` issues (25 on 2026-11-17), failed user units (11; `usage-pace` listed as known, not counted, Brian 2026-11-11), open AES issues labelled `owner:brian` (0; AES has no `needs-human` label), and the inferred approvals from the oversight data as a count only (163, data of 2026-11-12 because `projects-refresh` fails). Then what changed since the last run (new and cleared items, AES pull requests merged in the last day) and links to six source pages. Settings are the `hub_page:` section of aes-config `graph-config.yaml`; the page goes only to the private code2-workspace branch `shaping/aes-hub-data`, served behind the one password (checked 2026-11-17 with the login cookie: HTTP 200, title AES hub; without it 303). It is rebuilt every hour by the `hub-page` job in aes-config `timers.yaml`, and the page says so. One run: 5 commands, 4.4 s (the old page: 7.5 min CPU). The old page's Needs you also counts 25 `waiting:brian` issues; 35 overstates the distinct asks (the credit outage appears as 2 issues and 5 failed units; `gates-nightly` as a unit and an issue; `client-config-drift` still failed although row 4 fixed the drift; many `waiting:brian` items are FOIA status notices). Slice 2 (2026-11-17, Brian 2026-11-16 "i approve 7 tight" and the 2026-11-17 brief): Needs you holds only what Brian must decide or do, each listed once. Waiting issues are sorted by labels and fixed title prefixes from the `hub_page:` settings, never by meaning: `source:foia-tracker` issues titled `Records request` go to "FYI: records updates" grouped by label and repository; `source:usage_pace` is quiet (Brian, 2026-11-11). Failed services move to "Broken services", grouped by cause (a `shared_causes` entry, here the empty OpenRouter key: 2 services and 2 issues; every other unit its own cause with the failing-jobs page's reason), with each unit's own issue listed once there. The approvals are a footer count, "Not shown: no significance field" (neither `requirements.json` nor `approvals.json` marks significance). What changed compares across sections, so a moved item is neither new nor cleared. Issues are also matched by the `<!-- concern-key: K -->` marker in their body, because Project Meta's issues moving to code2-workspace on 2026-11-17 lost their `source:*` labels and numbers. Live data, same hour: Needs you 31 before (25 issues + 6 services) and 9 after; Broken services 7 services, 6 causes; FYI 12; quiet 1; approvals 98 (the 163 above was the 2026-11-12 data). Still open: the four `owner:agent` issues also labelled `waiting:brian` (code2-workspace #355, #282, llm_client #369, #407) stay under Needs you because no label says they are not his; the hive root address; retiring the old page. |
| 11 | **Done 2026-11-17 (Decision 30 A, Brian: approved).** The GitHub repository `BrianMills2718/project-meta` is archived (`gh repo view`: isArchived true) and the `project-meta-policy-audit` timer is disabled and inactive (aes-config #11 records it as present but disabled; its unit files stay in `machine-units/`). The local folder `~/code2/project-meta` is untouched, with its 42 stashes saved to `~/archive/project-meta-local-20261117/` and as `refs/archive/stash-20261117-*` on the remote. Still working because the local clone remains, and a follow-up rather than a blocker: the `lane-sweep` `canonical_lock.py --sync` setting, the relative script paths in the `instruction-surfaces` skill, and the 40 or more tracked scripts and Makefiles. Fetches from the remote still exit 0 (archived repositories allow fetch and refuse push). The sweep that preceded the yes (read-only, 2026-11-17, so its list of timers is the earlier state): checked by a read-only sweep on 2026-11-17: moving or removing the local Project Meta folder today would break live jobs; archiving it on GitHub alone breaks none of the local clones. Enabled timers found then to run or load Project Meta code: `needs-you-push`, `usage-pace`, `context-upkeep`, `skill-review`, `project-meta-policy-audit` and `lane-sweep`, plus the `OnFailure` hooks of 7 units (`concern_issue.py`) and the Claude and Codex hooks (`jev-gate-hook` calling `md_file_cap.py`). **Updated 2026-11-17 after ports 1 to 6:** `needs-you-push`, `usage-pace`, the `OnFailure` hooks, `jev-gate-hook`, `context-upkeep` and `skill-review` no longer use Project Meta (see "Before item 11"). Still on it: `project-meta-policy-audit` (runs its own clone, `~/.local/share/project-meta-policy-runtime`, which has 5 modified generated files and 6 stashes) and `lane-sweep` (runs `canonical_lock.py --sync` when the aes-config setting says so). About 40 or more scripts and Makefiles tracked in git use it too. **Updated later on 2026-11-17:** the notify callers, `rr-public-export` and `prune-merged-worktrees` moved to AES, and the policy-audit clone was compared and archived (timer still on; see steps 1, 3 and 7). The older version of this plan listed 6 timers; these 5, the `OnFailure` chain and the hooks were missing, and `skill-review` was wrongly called "not a Project Meta job". Local-only data: compared and kept on 2026-11-17 (step 8 below): all 42 stashes on the remote as backup refs, the rest in a local archive; one ignored MediaWiki environment file still needs a manual copy. The learnings gap of 11 is 11 non-entry files, not missing entries. |

### Before item 11

Source: inferred by agent, from the 2026-11-17 sweep in row 11. Port these in this order, then ask for the yes:

1. The notify router (`operator_notify_router.py`): **done 2026-11-17** for its one row-11 caller (`usage-pace`).
   AES `scripts/operator_notify_router.py`, `notify_operator.py` and `operator_notification_record.py` are copies of
   Project Meta `ee2957b1f` (the two helpers byte-identical, so the stamps `~/.local/state/operator-notify/<key>.json`,
   `history.log` and the record `notifications.jsonl` are the same files and format), with 66 tests (61 ported,
   5 new; spec `openspec/specs/operator-notify`; AES #931, `2645295`). The one private value in the code, the concern
   repository, is now `operator_notify: concern_repo` in aes-config `graph-config.yaml` (aes-config #5, `e6b3438`), set
   to AES; the Telegram token, chat id and ntfy topic are secrets and stay in `~/.secrets/api_keys.env`, not in the
   settings. Dedupe: a concern is the same when the repository, the `concern:feedback` label and the hidden marker
   `<!-- concern-key: KEY -->` match; Project Meta #2713 (key `usage-pace`, `waiting:brian`) was open, so
   `legacy_concern_repos: [BrianMills2718/project-meta]` keeps an open concern there updated or closed there (moving
   the issue would give it a new `repo#number`, which `needs-you-push` would send Brian as new). Checked live,
   read-only: `usage-pace` resolves to project-meta #2713 (OPEN), AES holds none, an unknown key resolves to AES.
   Side by side on 20 cases (stub ntfy and Telegram on 127.0.0.1, fake `gh`, throwaway home; every non-local URL
   refused): 12 identical; 8 differ only in the concern repository name and one extra read-only `issue list` in
   project-meta (the legacy lookup); exit codes equal in all 20; 4 of 6 state files identical, the other 2
   (`notifications.jsonl`, `latest.txt`) only by repository name; in the 5 cases with #2713 open the new copy
   comments on or closes #2713 and creates nothing. Not compared: the real toast (stubbed on both sides, code
   unchanged). The other callers moved the same day, each to `~/.hive-brain/aes/scripts/`:
   - ecosystem-ops `attention_push.py` and `scripts/operator_notify.py`: #208, `4755bfc`; tests 23 passed.
     - Severities are `attention` and `urgent`, so ntfy only.
     - The full `make check` fails 25 tests and errors 25 more in parts this change does not touch (a missing repo-graph database, a missing `enforced_planning` module).
     - The `attention-page` timer is not installed on this laptop.
   - personal-root FOIA `harvest.py` and `tracker.py`: #107, `5ed0641`; 77 passed, 1 deselected.
     - The deselected test fails on unchanged `main` too.
     - The units run `origin/main`.
   - personal-wiki `google_access.py`: #206, `74758f1`.
   - progressive-air `tools/credit_alert.py`: #7, `a8751b2`.
     - The installed `~/.local/share/hvac-credit-alert/credit_alert.py` was replaced by it after a backup.
     - `--dry-run` exited 0.

   The AES default concern repository is public. The FOIA, Google-access and HVAC notices carry private text, so these
   three callers set `OPERATOR_CONCERN_REPO` to their own private repository: `personal-root`, `personal-wiki` and
   `progressive-air-blueprint-poc-work`. A value already in the environment still wins. Concerns still open in Project
   Meta keep being updated or closed there (the legacy lookup).

   Old and new router, side by side on 13 cases (each caller's real arguments; the stub ntfy and Telegram, fake `gh`
   and throwaway home used in step 1):
   - Exit codes are equal in 13 of 13.
   - HTTP requests, toast calls and the set of state files are identical.
   - `gh` calls are identical apart from the repository name and one read-only legacy lookup.
   - State files are identical once time and repository are masked; `notifications.jsonl` differs only in its random id
     and timestamp.

   The harness and its output are in `~/archive/router-switch-20261117/harness/`. **Open:** `usage-pace` and any
   caller without the override file concerns in the public AES repository, because aes-config `concern_repo` names it.
2. `usage-pace` and `needs-you-push`, onto the ported router.
   - `needs-you-push`: **done 2026-11-17.** It sends through AES `scripts/learning_loop/notify.py` (loaded from
     `~/.hive-brain/aes`), which gained an opt-in link-preview switch, the message id and Telegram's error text
     (AES #929, `de931c1`); the caller changed in code2-workspace #462 (`ef0b722`). Checked: against a local stub
     Telegram server the old and new sender sent the same request (chat id, text, preview off), wrote the same
     state and gave the same exit code in 4 cases (accepted, HTTP 400, `ok` false, connection refused); only the
     failure detail wording in the log line differs. Dry runs before and after on copies of the live state:
     identical output (26 keys, "no new issues"; with 3 keys removed, the same 2 "would send" lines). No real
     message was sent for the check; `systemctl --user start needs-you-push.service` exited 0 ("no new issues",
     state unchanged).
   - `usage-pace`: **done 2026-11-17.** `NOTIFY` runs `~/.hive-brain/aes/scripts/operator_notify_router.py` with the
     same arguments (code2-workspace #464, `0927bd8`; OpenSpec change `usage-pace-aes-router`); `test_usage_pace.py`
     25 passed. A dry run read 0 of 2 accounts (the known wrong-login cause), so no notice was due;
     `systemctl --user start usage-pace.service` then exited 1 (job exit 2, as before), `notified` none, the record
     unchanged at 25,605 lines.
3. Concern filing (`concern_issue.py`) for the 7 `OnFailure` hooks: **done 2026-11-17.** `disk-job-failed@.service`
   (personal-file-infra #297, `7a3ee72`) and `harness-live-failed.service` (agent-skills #614, `6acd2a6`) run
   `%h/.hive-brain/aes/scripts/concern_issue.py` with the same `--repo`, key, title, source and occurrence. Project
   Meta's script only forwarded to the code2-workspace copy, which equals AES's apart from one comment word; with a
   stub `gh`, old and new made identical calls with identical output and exit codes in 6 of 6 cases (both units; no
   concern, open, closed). `daemon-reload` exit 0; `systemctl --user cat` shows the new path.
   `~/.local/bin/rr-public-export` line 15 (not in git) moved the same day:
   - It now runs `$HOME/.hive-brain/aes/scripts/concern_issue.py`.
   - The old file is kept in `~/archive/router-switch-20261117/rr-public-export`.
   - With a stub `gh`, old and new made identical calls with identical output and exit 0 in 2 of 2 cases.
   - `sh -n` exit 0.
4. The `md_file_cap.py` path in `jev-gate-hook`: **done 2026-11-17.** The installed hook pair has a git source:
   agent-skills `contracts/client-config/jev/` (`jev-gate-hook` was already identical; the guard's source had been
   pointed at the canonical AES checkout on 2026-11-15, `00e6ff9`, but the installed copy still ran Project Meta's).
   The guard now runs `~/.hive-brain/aes/scripts/md_file_cap.py` (agent-skills #615, `aef8d58`), and
   `~/.local/bin/jev-gate-compliance-guard` equals that source; the two old files are kept in
   `~/archive/jev-gate-switch-20261117/`. Checked: with the guard's own arguments (`--repo TOP --ref SHA`), old and new
   `md_file_cap.py` gave identical output and exit codes on 16 of 16 real repositories (6 under the cap, exit 0; 10
   over it, exit 1). agent-skills jev tests: 28 passed, 1 failed (`test_t1_observes_and_enforces_on_request`, which
   fails the same way on unchanged main).
5. `context-upkeep` (`rule_audit_nightly.py`): **done 2026-11-17**, ported, not retired. It is not obsolete: Brian
   approved the nightly audit on 2026-11-06, its 2026-11-16 run reported 315 findings, and no AES or Lockstep check
   covers instruction-file size, duplication or staleness. `audit_instruction_quality.py` and
   `scan_doc_freshness_ecosystem.py` are copies of Project Meta `f6f0d6f91` in AES with their tests (spec
   `openspec/specs/instruction-audit`; AES #933, `227ca31`); the graph comes from `PROJECT_GRAPH`, else aes-config. The
   caller runs them from `~/.hive-brain/aes` (code2-workspace #466, `82a762f`). Checked with the nightly's exact
   arguments: old and new output byte-identical (110,003 and 186,448 bytes, exit 0 both). Not run: the service itself
   (it makes a paid model call and can file an issue). The `instruction-surfaces` skill still names the Project Meta
   script paths.
6. The `skill-review` default path to `policy_friction.md`: **done 2026-11-17.** The register moved to aes-config
   (private; AES is public, and `learnings-archive` is a frozen one-commit repository with no pull request route),
   byte-identical to Project Meta `main` (aes-config #6, `0a76bc5`). `skill_review_cycle.py` now defaults to
   `SKILL_REVIEW_POLICY_FEEDBACK`, else `PROJECT_META_ROOT/policy_friction.md`, else the aes-config copy (agent-skills
   #615); the runtime clone is at that commit. Copies compared first: the kept one (last commit 2026-10-07, the newest
   commit touching the file across all refs) has the same hash as 6 other copies on disk; 3 older copies have 0 lines
   it lacks. Lines the kept copy lacks exist only in about 100 unmerged July branches and in stashes `stash@{1}`
   (2026-10-05), `stash@{40}` (2026-08-19) and `stash@{41}` (2026-08-18), all older; they stay in Project Meta's git
   and belong to step 8. Read side by side, old and new path gave the same 7 feedback items. The `skill-review` unit's
   own `ExecStartPre` still runs `git checkout --force`, which Safety Net blocks when run by hand.
7. The `project-meta-policy-audit` runtime clone: **compared and kept on 2026-11-17; timer disabled the same day (Decision 30 A).**

   What the audit is:
   - It runs daily at 06:00 for about 52 minutes: about 40 Project Meta checks plus its own steps.
   - Its 2026-11-16 run exited 0 with 6 steps red.
   - Its only output is comments on Project Meta concerns: #1976, #1982, #1983, #1984, #1986, #1987, #1979, #1980,
     #1962 and #1981. None carries `waiting:brian`, and every comment on them is its own, so nobody reads them.

   Coverage:
   - Already covered by AES: `failed_unit_watch`, `lane_sweep`, `workspace_map`, `machine_manifest`,
     `client_manifest`, the instruction audit (step 5) and doc freshness.
   - Obsolete: claims, Project Meta's own ADRs, plans and registry, and its own pytest suite.
   - Not covered, and small: the stacked-pull-request check and the hook-trigger check. They are proposed for
     retirement, not porting.

   The clone:
   - It is 0 commits ahead of `origin/main` and 11 behind.
   - It has 6 modified files (not 5). All are generated reports except `policy/friction_clusters.yaml`, which holds
     one cluster found nowhere else and can be rebuilt.
   - It has 6 stashes. 2 are already on `origin/main`; the other 4 are old generated snapshots.

   Everything unique is copied to `~/archive/policy-runtime-20261117/` (26 files; `sha256sum -c` exit 0). Nothing was
   discarded.

   **Done 2026-11-17 (Decision 30 A):** `systemctl --user disable --now project-meta-policy-audit.timer` was run; aes-config
   `machine-layer.yaml` now records it as `enabled: disabled` (aes-config #11), and its unit files stay in `machine-units/`.
8. The stashes and uncommitted or ignored data, each kept after a comparison with the copy that stays: **done
   2026-11-17** ([project-meta-local-data-20261117.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/2b2c089f002f2eb165bdc2b55ac69adcdbc2da24/docs/planning/project-meta-local-data-20261117.md); private detail in
   aes-config `docs/project-meta-local-data-20261117.md`, #8). Stashes: 11 of 42 fully contained on the remote, 31
   not; all 42 pushed as `refs/archive/stash-20261117-NN` to the private Project Meta remote (42 of 42 shas match;
   gitleaks 0 findings first), plus 42 patch files and a verified bundle in `~/archive/project-meta-local-20261117/`.
   The uncommitted wiki health report measured another repository's wiki and is not regenerable; kept byte-identical.
   Ignored files kept locally: `LocalSettings.php` (mode 600), the `worktrees/` folder (23 folders, none a git
   checkout), `generated/runtime/` and 2 logs. Not kept: the MediaWiki environment file, which Safety Net will not let
   an agent read; Brian copies it by hand. Learnings: the 11 are 6 invalid-entry files, 4 resolutions and a README on
   Project Meta `origin/main`; entry ids match both ways (0 differences). `policy/friction_clusters.yaml` has no
   content-identical copy outside Project Meta; the runtime clone's modified copy belongs to step 7.

`~/.local/bin/prune-merged-worktrees` (run weekly through personal-file-infra `prune-all-worktrees`) moved on
2026-11-17:

- `scripts/prune_merged_worktrees.py` is in AES, unchanged from Project Meta `b743c308a`, with its 3 tests (spec
  `openspec/specs/prune-merged-worktrees`; AES #938, `2a6cdcd`).
- The link now points at `~/.hive-brain/aes/scripts/prune_merged_worktrees.py`.
- The old link target and script are kept in `~/archive/router-switch-20261117/prune-merged-worktrees/`.
- Old and new `--dry-run` on all 169 entries of the weekly repository list: 161 byte-identical with equal exit codes
  (158 exit 0, 3 exit 2 on folders that are not repositories). The other 8 are not git checkouts. Comparison kept in
  `~/archive/router-switch-20261117/prune-cmp/`.

Still on Project Meta after steps 1 to 8:

- (done 2026-11-17, Decision 30 A) the `project-meta-policy-audit` timer is disabled;
- `lane-sweep`'s `canonical_lock.py --sync` setting;
- the relative script paths in the `instruction-surfaces` skill;
- the 40 or more tracked scripts and Makefiles named in row 11.

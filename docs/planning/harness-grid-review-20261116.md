---
description: Evidence for the AES consolidation plan: five part-by-part reviews of the harness grid, checked read-only on 2026-11-16
doc_role: evidence
status: current
---

# Harness grid review, 2026-11-16

Evidence for [the AES consolidation plan](aes-consolidation-plan.md). Five read-only reviewers each took one part of the harness grid (6 parts by 5 loop steps; 127 items in the grid file plus 42 more that the 2026-11-07 row reviews added). The grid is on the workspace repository branch `shaping/harness-grid`. Findings quoted in the plan were re-checked by the plan author where marked there. Each part below keeps its reviewer's own table, with its limits at the end.

## Part: context

### Grid row "Context": review (checked 2026-11-16, read-only)

#### Summary

1. 36 grid items sit in the Context row. Counts by class: AES-OWNED-DONE 0, AES-OWNED-PARTIAL 7, TO-PORT 4, OFF-THE-SHELF 4, KEEP-OUTSIDE-AES 12, RETIRE 8, UNKNOWN 1. (AES = the Agentic Engineering System, Brian's canonical system.)
2. The rule-delivery half works: core.md is loaded by both clients (`cmp` identical, `~/.claude/CLAUDE.md` imports it) and the shell-read loader fired in this very session. The 11-06 reviews' fixes mostly landed (context-upkeep timer, hooks dir emptied, compaction logs folded).
3. The learn half is broken now: `feedback-collector` (exit 1, 11-16 04:03) and `skill-review` (exit 1, 11-16 10:45) both failed; problems, fix-owner and effects timers are still disabled. Nothing turns lessons into fixes.
4. Two rule homes still contradict: the old `~/projects/.claude/AGENTS.md` (still injected by the loader, still points at Project Meta) vs `core.md`; 174 Claude-only memory notes vs shared core rules; code2check vs Lockstep both inject requirements at edit time.
5. Commit-time checks (lefthook) are switched off by `~/.config/git/repo-hooks.off` (dated 2026-10-13), and only 21 of 256 repos have `lefthook.yml`: the Enforce step for docs is mostly not real.

#### Table

Classes: AES-OWNED-DONE, AES-OWNED-PARTIAL, TO-PORT, OFF-THE-SHELF, KEEP-OUTSIDE-AES, RETIRE, UNKNOWN. "Serves": goal = agents effective; requirement = consistent/shareable/configurable; path = visible/trustworthy/clean start.

| item | status today (evidence) | belongs where | serves | overlap or contradiction | recommendation |
|---|---|---|---|---|---|
| jobs/feedback-loop | partly. collector timer enabled but last run FAILED exit 1 11-16 04:03 (`systemctl --user show feedback-collector.service`); labels enabled; problems/effects/fix-owner timers disabled (list-unit-files) | AES-OWNED-PARTIAL (AES owns `scripts/learning_loop`; FEEDBACK_AND_POLICY.md) | goal (learning) + path | Same job as frameworks/feedback-loop (duplicate row); AES doc 11-13 says collector had timed out (exit 143) | Find why collector fails (journal), fix, then decide enable/retire of the 3 disabled stages |
| jobs/policy-and-planning-gates | plan-status-refresh timer enabled, not failed now; `project-meta-policy-audit.timer` enabled (list-unit-files); retirement plan item 6 says each of 9 timers is ported, replaced or off | TO-PORT (policy audit) / RETIRE (plan-status mirror) | requirement | Project Meta policy registry (263 rows) vs AES `docs/rules`; Project Meta being retired | Follow project-meta-retirement-plan.md item 6; do not extend Project Meta |
| jobs/skills-and-hooks-health | hooks-autoapply.timer active, ran 16:47; skill-review FAILED exit 1 11-16 10:45 | TO-PORT (skill-review is in retirement plan list) | path | Overlaps skill-feedback-loop row | Fix skill-review failure; port into AES with the learning loop |
| jobs/inquiry-graph-chatgpt | off; the six `extract-*` units no longer exist (list-unit-files empty) | RETIRE | none | Superseded by frameworks/inquiry-graph | Mark retired in grid |
| jobs/rtk-measure-oct17 | one-shot done; no `rtk-measure*` unit now | RETIRE | none | none | Remove row |
| frameworks/feedback-loop | same units as above; `learned` skill lines still feed it | AES-OWNED-PARTIAL | goal + path | Duplicate of jobs/feedback-loop | Merge the two rows into one |
| frameworks/worktree-rules | core.md says one worktree per agent, no claims; but `agent-skills/AGENTS.md` still carries long "claim" text marked history (grep) | KEEP-OUTSIDE-AES (rule text in code2-workspace `agents/`) | requirement | Old claim rules vs new no-claims rule; stale text still loaded in agent-skills | Delete the claim paragraphs in agent-skills/AGENTS.md (git-tracked, undoable) |
| frameworks/inquiry-graph | running. nightly log `nightly-2026-11-16.log` exists; timer active | KEEP-OUTSIDE-AES | path (Brian's stated positions) | none | Leave; not an agent-effectiveness piece |
| pages/oversight-page | `oversight-refresh.timer` inactive; `projects-refresh.service` FAILED (feeds oversight data); front-page decided as merge target (HARNESS_RUN 11-06) | RETIRE (merged into front-page) | path | Two pages show rules and approvals | Finish the merge; drop oversight timers |
| pages/repo-docs | not re-checked live (no network call made); 21+ repos carry docs per format rule | OFF-THE-SHELF (Zensical docs tool) | path | none | Keep; AES configures |
| data/scratch | `~/code/.scratch` 7.9 GB, 113 entries (du/ls today); `offload-cold.timer` moves idle entries to Drive | KEEP-OUTSIDE-AES | path | Agent state files here vanish after 2 idle days (HARNESS_RUN) | Put durable agent state in git, not scratch |
| agent-config/rule-system-core | running. `cmp` identical for Codex; Claude imports it; core.md is 19,789 bytes; 43,803 tokens measured always-loaded vs 60,000 budget (context-budget latest.json) | AES-OWNED-PARTIAL (AES owns policy register; text lives in workspace) | goal + requirement | core.md + 17 topic files vs AES `docs/rules` register: two homes for one rule set | Decide the single source; core.md stays as delivered file generated from it |
| agent-config/folder-rule-files | rule audit 11-16: 315 stale/other findings in 123 repos (rule-audit 2026-11-16.md); AES ECOSYSTEM lists 8 gaps in `instruction-surface-sync` | AES-OWNED-PARTIAL | requirement | AGENTS.md vs CLAUDE.md copies drift (AES AGENTS.md is generated copy) | Adopt AES generated AGENTS.md with `CLAUDE.md` = `@AGENTS.md` everywhere |
| agent-config/rules-archive-projects-dotclaude | git status clean; last commit 2026-11-07; BUT its `AGENTS.md` is still injected by the loader (seen this session) and points to `project-meta` WORKSPACE_MAP | RETIRE (archive after compare) | path | Contradicts core.md ("repos live in ~/code2"; refers to Project Meta) | Compare with core + rule-sources, then archive; stop loader injecting it |
| agent-config/agent-memory | 174 files in `-home-brian-code/memory` (was 126 on 11-05); 2 in vision project | KEEP-OUTSIDE-AES | goal | Claude-only, not shared with Codex or git: breaks "shareable"; MEMORY.md says rules moved to core yet notes keep growing | Promote lasting rules to core/topic; keep memory for non-rules |
| agent-config/instruction-loader-hook | running: fired on this session's shell reads; settings still points at old `~/projects/.agents/hooks/load_instruction_context.py` path | AES-OWNED-PARTIAL | goal | Source also in `agent-skills/hooks`; two paths | Point settings at one path; check what it injects (see row above) |
| agent-config/code2check-hook | tool installed; 8 repos list code2check (claim-extraction has `.code2check`) | RETIRE (Lockstep replaces; guess pending parity check) | requirement | Same job as Lockstep hook (requirement text at edit) | Compare on one repo, then retire code2check |
| agent-config/rtk-output-shrinker | `rtk gain` today: 145,736 commands, 50.9M tokens saved (54.3%) | OFF-THE-SHELF | goal | none | Keep; AES configures |
| agent-config/skills-own-used | `~/.claude/skills` has 54 entries, `~/.agents/skills` 53; usage counts are from 11-05 (not re-run) | KEEP-OUTSIDE-AES (agent-skills repo) | goal | none | Keep; sync via rulesync |
| agent-config/skills-own-unused | skills like deliberate, orchestrator, second-opinion, research-workbench still listed (ls); 27 had 0 uses on 11-05 | RETIRE (candidates) | goal (smaller listing) | Each costs context in every session | Archive via documented command after a usage re-count |
| agent-config/external-skill-packs | no hyperframes/media-use dirs in `~/.claude/skills` now (ls grep empty) | RETIRE (apparently already gone) | none | none | Confirm and drop row |
| agent-config/skill-feedback-loop | skill-observability enabled; skill-review FAILED 11-16 | TO-PORT | goal | Second learning loop beside feedback loop | One loop for lessons and skills |
| agent-config/sub-agent-compact-plugin | now 55 log files (was 2,474); context-upkeep folds them daily | KEEP-OUTSIDE-AES | goal | none | Done; drop the "breaks one-file-per-day" note |
| agent-config/slash-commands | `~/.claude/commands` has where-are-we.md and architectural-ideas.md; where-are-we also in `~/.agents/skills` (Codex) | KEEP-OUTSIDE-AES | goal | Claude command vs Codex skill for the same job | Make where-are-we one skill for both; retire architectural-ideas (writes into Project Meta legacy path) |
| agent-config/clean-claude | `~/.local/bin/clean-claude` present | KEEP-OUTSIDE-AES | path (clean start) | none | Keep; document in front page |
| new/subagent-delegation-rule | in core.md Context section and `topics/context-budget.md` | KEEP-OUTSIDE-AES (rule text) | goal | none | Keep |
| new/front-page | `front-page.timer` active, last run 16:08 today | KEEP-OUTSIDE-AES (workspace script; AES reads it) | path | Overlaps oversight page and `failures-page` | Make it the only status page |
| new/commit-hooks-lefthook | 21 of 256 repos have `lefthook.yml`; `~/.config/git/repo-hooks.off` exists (since Oct 13), so commit checks are skipped | OFF-THE-SHELF (lefthook) | requirement | Claimed Enforce vs switched off | Ask Brian if the off-switch is intended; else remove and adopt |
| new/cloud-session-setup | `cloud_setup.py` last changed 2026-11-05; paste step by hand (guess: unchanged) | TO-PORT | requirement (shareable) | Cloud sessions can lag core.md | Pull rules from git at cloud start |
| new/builtin-agent-tools | available in this session | OFF-THE-SHELF | goal | none | None |
| new/where-is | `~/.local/bin/where-is` present | KEEP-OUTSIDE-AES | goal | duplicate row in missing_from_inventory | Remove duplicate entry |
| new/while-waiting-sweep | skill present; receipt adoption not measured | KEEP-OUTSIDE-AES | path | none | Measure receipts before claiming |
| new/learned-feedback-lines | skill present; feeds collector that currently fails | AES-OWNED-PARTIAL | goal | none | Fix collector (see first row) |
| new/claude-hooks-dir | `~/.claude/hooks` now empty (`ls \| wc -l` = 0) | RETIRE (done) | none | none | Close row |
| new/lockstep | in AES repo `src/lockstep` since 11-11; 25 openspec specs incl. 8 lockstep-*; adoption: 29 of 256 repos have openspec | AES-OWNED-PARTIAL | requirement + goal | overlaps code2check | Widen adoption on next-touched repos |
| new/jev-layer | `layer.py` exists, unreferenced; only `jev-gate-hook` is wired (settings grep) | UNKNOWN (check: is always-loaded context pressure real? latest 43.8k of 60k, under budget) | none today | none | Do not build; revisit if budget exceeded |

#### Part priority

- **Do first (small):** repair the learn half. Find why `feedback-collector` and `skill-review` exit 1 (journal), fix, then decide on the 3 disabled stages. Basis: two failed units today; AES doc 11-13 says the repair stages stopped October 12. Size: small to medium (guess: root cause unread).
- **Cheap, high value (small):** archive the old `~/projects/.claude/AGENTS.md` so the loader stops injecting a rulebook that contradicts core.md; delete stale claim text in `agent-skills/AGENTS.md`. Basis: both seen live today.
- **Requirement (medium):** pick one source for rules. Today core.md, 17 topic files, AES `docs/rules`, folder AGENTS.md and 174 memory notes overlap.
- **Large:** none urgent.

#### Could not check

- Live HTTP of repo docs and any network call (not allowed).
- Usage counts for skills (11-05 numbers not re-run).
- Why collector/skill-review fail: journal showed only exit codes; the scripts were not run.
- Hook invocation counts today vs 11-05 (receipt files are split by hour; not comparable).
- Whether `repo-hooks.off` is intentional; whether cloud_setup is still pasted by hand.
- Lockstep and code2check parity on a real repo.
- Items marked guess above.

## Part: tools

### Grid row "Tools and models": review, 2026-11-16

Summary

1. 22 items sit in this row. Checked live today with read-only commands (systemctl, journalctl, ls, settings reads, gh).
2. Counts by class: AES-OWNED-DONE 0, AES-OWNED-PARTIAL 1, TO-PORT 4, OFF-THE-SHELF 4, KEEP-OUTSIDE-AES 11, RETIRE 1, UNKNOWN 1.
3. AES (the Agentic Engineering System canonical repo) owns almost nothing here yet. It only reads the LLM database and uses `llm-cost`. The "requirement" (one shared, configurable system) is not met for models and tools: model defaults and router options live in no repository.
4. Three things are claimed but not real today: the subagent model rule is broken (23 rule-break lines in 2 days), the usage-pace job fails every run (account login mismatch), and the router-feedback and skill-review jobs fail because the OpenRouter credit balance is too low.
5. Most of the row works and belongs outside AES. The priority is the model rule plus putting model settings under version control.

Acronyms: AES = Agentic Engineering System; MCP = Model Context Protocol (external tool servers); WAL = SQLite write-ahead log file.

#### Table

Classes: AES-OWNED-DONE, AES-OWNED-PARTIAL, TO-PORT, OFF-THE-SHELF (standard tool, AES configures), KEEP-OUTSIDE-AES, RETIRE, UNKNOWN.

| item | status today (evidence) | belongs where | serves | overlap or contradiction | recommendation |
|---|---|---|---|---|---|
| jobs/spend-tracking (LLM spend sync) | Running. openrouter-billed, server-llm-spend, hive-spend all Result=success; last runs 16:00 to 16:59 today (systemctl show). | KEEP-OUTSIDE-AES | path (visible spend) | Overlaps `llm-cost` and the observability DB (three views of cost). Not contradictory. | Keep. Add to the AES timer job list (`aes-config/timers.yaml`) when timers are ported. |
| jobs/skills-and-hooks-health | Partly. hooks-autoapply fine (16:47 current). skill-review FAILED today 10:45: OpenRouter 402 "can only afford 6026" tokens (journalctl). | TO-PORT (decision) | path (trust) | Retirement plan row 6 (project-meta-retirement-plan.md line 74) says skill-review must be ported, replaced or switched off; no decision seen. | Decide skill-review's fate; until then it burns 4 minutes CPU per failed run. |
| jobs/agent-tooling-daemons | Partly. paseo active, agent-deck-web INACTIVE today (systemctl is-active). | KEEP-OUTSIDE-AES | goal (remote agents) | None found. | Keep. Check why agent-deck-web is down if Brian uses it. |
| data/hook-receipts-archive | Running. Last run 05:44 today, Result=success; next 05:17 tomorrow. | KEEP-OUTSIDE-AES | path (clean start, nothing lost) | Overlaps legacy hook cleanup (hooks are mostly disabled, see legacy row). | Keep. Revisit only if hooks stay disabled. |
| data/llm-observability-db | Running. `llm_observability.db` 10,232,504,320 bytes, WAL 55.9 MB (ls). 11-05 size was 11.47 GB, so it shrank; reason unknown (guess: prune). | KEEP-OUTSIDE-AES | goal and path (full traces) | AES reads it read-only (ECOSYSTEM.md line 283); llm_client owns writes. Consistent. | Keep. Run the deferred-write check (see could-not-check). |
| agent-config/hooks-distribution (rulesync + hooks-autoapply) | Running. 16:47 today: plugin status=current exit=0; timer every 15 min. | OFF-THE-SHELF | requirement (one manifest to both clients) | Not in AES. capabilities.md row "Checks on every agent tool call" owns it. Codex hooks.json has a backup named "all-agent-hooks-disabled" (2026-11-14). | Keep rulesync; have AES hold the manifest source. Confirm what is really enabled (see could-not-check). |
| agent-config/legacy-claude-home | Mostly gone. `~/.claude/hooks` has 0 files; grep for `.claude/hooks/` in settings.json and hooks.json = 0 each. Old settings backups (63 on 11-07) not recounted. | RETIRE | path (clean start) | Old hook generation. Contradicts nothing live. | Move aside, never delete (deletion rule). Count the backups, then archive. |
| agent-config/subagent-catalog | Running. `~/.claude/agents` 13 .md files; `~/.codex/agents` 14 files. Counts differ, so drift persists (ls). | TO-PORT | requirement and goal | Two clients, two lists; 11-07 review: Codex subagents pin no model at all. Manifest in agent-skills, not AES. | Make one manifest the source for both clients; AES owns the definitions. Small. |
| agent-config/model-router-plugin | Running. settings: routeAll=True, riskFloor=True, respectExplicitModel=True. | KEEP-OUTSIDE-AES | goal (cheaper correct models) | Contradiction: routeAll true floors judging agents at Sonnet, against the written Opus rule; llm-calls.md reportedly says false (11-07 review; not re-read today). | Fix the config or exempt judging agents; see priority. |
| agent-config/claude-ai-synced-plugins | Running. 3 synced plugin folders present. Use is low (30-day count from 11-05: only anthropic-skills used). | KEEP-OUTSIDE-AES | none (vendor-pushed) | Many skills overlap AES/company skills (engineering, design). Adds prompt noise. | Keep; consider turning off unused ones. Needs usage re-count (not run). |
| agent-config/codex-only-plugins | Running. 6 `enabled = true` lines in `~/.codex/config.toml`. | KEEP-OUTSIDE-AES | none | Same overlap with Claude-side skills. | Keep as is. |
| agent-config/mcp-servers | Partly. localhost:8787/mcp returns 401 (chatgpt-bridge up, needs token). This session: ide (connection closed) and inside-success-second-brain (502) failed to connect. | OFF-THE-SHELF | goal (reach tools) | Servers set by rulesync manifest and by plugins, two writers. | Keep manifest as source. Brian action only if he wants the second brain or bridge restored. |
| agent-config/permission-and-session-settings | Running. `permissions.allow` = [] (everything bypasses); model = sonnet today; only hooks part is generated from git. | TO-PORT | requirement (configurable, shareable) | Three writers on `model`: /model, usage-pace, agents. | Put model, effort, enabledPlugins and pluginConfigs in the manifest. Small to medium. |
| new/usage-pace | BROKEN. usage-pace.service exit 2 at 12:08 today; latest.json: verdict unknown, both accounts "login is therakorski@gmail.com, expected brianmills2718@gmail.com". Model "sonnet (hand pick kept)". | KEEP-OUTSIDE-AES | none (Brian 11-11: not a concern) | Contradicts the stated default "opus": it holds Sonnet by hand pick and the check cannot read usage. | Low priority. Fix the account mapping or switch off; one line to Brian, no more. Do not list logins. |
| new/subagent-model-assignments | Partly. `subagent_models.py --days 2`: 23 "ran on X, expected opus" lines, e.g. planning-compliance-reviewer on sonnet 16:54 today. No timer runs it. | TO-PORT | goal (right model on judges) | Contradicts the router (routeAll floors judges at Sonnet) and the rule text. | Part priority. Make the rule and the router agree, run the check daily. |
| new/router-report-loop | Partly. Daily report files 11-06 to 11-16 exist. router-feedback FAILED 07:45 today (OpenRouter 402). router-review success 07:50. | KEEP-OUTSIDE-AES | path (visible model quality) | Earlier "never ran" claim is stale: timers do run now. | Keep. Needs OpenRouter credit to work (Brian action: add credits or accept outage). |
| new/model-currency | Running. 07:15 today success; issue llm_client #369 open "Model currency: allowed routes behind current releases", waiting:brian (gh). | KEEP-OUTSIDE-AES | goal (current models) | None. | Keep. Brian can close #369 once he reads it. |
| new/agent-clients | Running. Claude model sonnet, Codex model gpt-6-luna effort medium (was "high" in the grid; changed). autoContinueAtUsageLimit and remoteControlAtStartup keys present. | OFF-THE-SHELF | goal | Grid text says opus / luna high; today differs. | Update the grid text. Config goes in the manifest (see settings row). |
| new/builtin-agent-tools | Running (tools present in this session). | OFF-THE-SHELF | goal | None. | Nothing to build. |
| new/llm-cost-cli | Running. `/home/brian/.local/bin/llm-cost` exists. AES next.goal.md line 89 cites a measured `llm-cost` figure. | KEEP-OUTSIDE-AES | path (cost basis) | Same data as spend-tracking, different slice. | Keep. |
| new/capabilities-list | Running. `workspace/docs/capabilities.md`; last workspace commit "Capabilities: hooks-autoapply" (#451). | AES-OWNED-PARTIAL | requirement (one place that names the tool per job) | AES has a discovery journey (ECOSYSTEM.md) and an earlier own inventory; capabilities.md is the one in daily use (guess: AES does not yet read it). | Keep as the single list; link AES discovery to it. |
| new/jev layer | OFF. `layer.py` exists, no wiring. BUT settings.json lines 77 and 96 call `jev-gate-hook` (a different jev piece); grid evidence "no reference" is wrong for that part. | UNKNOWN | none | Unclear whether the wired gate hook needs layer.py. | Check what jev-gate-hook calls; park layer.py until then. |

#### Part priority

First: make the model rule and the model router agree, and keep model settings in git. Today `routeAll` is true and judging agents run on Sonnet while the rule says Opus (23 breaks in 2 days). One change (router exemption for judging agents or `routeAll` false), plus a daily run of `subagent_models.py` with its output in the router report, fixes the biggest effectiveness loss (cheaper models doing the review). Size: small (one config key, one timer; basis: script and report already exist). The follow-on is medium: put `model`, `effort`, `enabledPlugins` and `pluginConfigs` into the rulesync manifest (basis: hooks already flow that way).

Cheap and high value: tell Brian once that OpenRouter credits are too low (router-feedback and skill-review both failed with 402 today). Close llm_client #369 or act on it.

Retirement and consistency: legacy-claude-home can be archived; usage-pace needs a one-line fix or switch-off.

#### Could not check

- Whether llm_client deferred writes today stay under 100 (journalctl count not run).
- Whether `~/.codex/hooks.json` hooks are enabled now (a "disabled" backup dated 2026-11-14 exists).
- How many old settings.json backups remain, and their contents.
- Whether llm-calls.md still says routeAll false (only config read today).
- Why the observability DB shrank from 11.47 GB to 10.23 GB.
- What jev-gate-hook needs from layer.py.
- Current plugin and skill usage counts (last count 11-05).
- Whether AES reads capabilities.md (guess only).
- missing_from_inventory, unplaceable and corrections entries: none mentioned this row.

## Part: environment

### Review: "Environment: where it runs" and "Environment: what it can reach"

Read-only review, 2026-11-16 ~17:00 EST. AES = the canonical Agentic Engineering System repo. Evidence is a path, command or the word "guess".

#### Summary

1. 44 grid items sit in these two rows (the 2026-11-07 row reviews, `~/code2/workspace/docs/planning/harness-rows/env-runs.md` and `env-reach.md`, add about 25 more not in the JSON).
2. Class counts: AES-OWNED-DONE 1, AES-OWNED-PARTIAL 3, TO-PORT 8, OFF-THE-SHELF 7, KEEP-OUTSIDE-AES 15, RETIRE 9, UNKNOWN 1.
3. AES owns almost none of this part today. It has one real piece: `scripts/timers.py` plus `~/code2/aes-config/timers.yaml`, which renders only 6 of the 84 timers on this laptop (`grep -c '^  - name' timers.yaml`; `ls ~/.config/systemd/user/*.timer | wc -l`). Only 42 of the 84 timer files are links into git (`ls -l | grep -c ->`).
2 of the biggest risks are "claimed but not real": the WSL Rebuild task is a one-time task that already ran (Next Run N/A), and the tool-call gate runs rules only, with no model judgment.
4. Reach (what an agent can touch) is governed by hooks alone: `~/.claude/settings.json` has `permissions.allow = []` and `skipDangerousModePermissionPrompt: true`. The hook rules that matter live in a file outside git (`~/.cc-safety-net/rules/brian-hard-lines/rulebook.json`, per the 11-07 review).
5. Priority: write one machine-layer manifest in `aes-config` (job, host, source, install command) so a clean machine can be rebuilt, then move the safety-hook rules into git.

#### Item table

Classes: DONE = AES-OWNED-DONE; PARTIAL = AES-OWNED-PARTIAL; PORT = TO-PORT; SHELF = OFF-THE-SHELF; KEEP = KEEP-OUTSIDE-AES; RETIRE; UNK = UNKNOWN. "Serves": G = goal (agents effective), R = requirement (consistent/shareable/configurable), P = path (visible/trustworthy/clean start).

| item | status today (evidence) | belongs where | serves | overlap or contradiction | recommendation |
|---|---|---|---|---|---|
| jobs/conversation-backups | Group row. Backup timers enabled; claude/codex ran 16:00-16:01 today (`systemctl --user list-timers`) | RETIRE (duplicate row) | none | Same five jobs as the four `data/*backup` rows | Merge into the data/ rows; count once |
| jobs/storage-policy | Group row. storage-policy-monitor ran 16:56 today | RETIRE (duplicate row) | none | Duplicates data/storage-policy and data/disk-growth-report | Merge; count once |
| jobs/run-artifacts-pack | Group row. Service success, exit 0 (`systemctl --user show`) | RETIRE (duplicate row) | none | Duplicate of data/run-artifacts-pack | Merge; the 11-05 "broken" status is stale |
| jobs/gates-nightly | **Broken**: Result=exit-code 1, ran 04:08 and 05:33 today; 3h06m CPU, 11.5 GB written (journal). Log tail "RESULT: FAIL" on a key-reading scan | TO-PORT (full nightly checks belong to the AES verify story; guess) | G, P | Overlaps lefthook per-commit checks and `lockstep check`; core.md says nightly failure goes to an agent, but nothing shows one is assigned | Read the failing check, assign it; cap CPU (batch slice) |
| jobs/checkout-sync | Group row over canonical-sync, graph-checkout-sync, lane-sweep. graph-checkout-sync ran 16:22 today | RETIRE (group row) | none | Overlaps frameworks/lane-sweep and canonical-sync | Merge into lane-sweep |
| jobs/agent-tooling-daemons | paseo, agent-deck autoupdate, codex-remote-control timers run today (list-timers) | KEEP-OUTSIDE-AES | G | None | Leave; list in the manifest |
| frameworks/enforced-planning | Claims retired 2026-11-05 (core.md). `enforced-planning-session-continuity` timer is now inactive (`systemctl is-active`) | RETIRE | none | Contradicts core.md ("Claims are retired") and the AES own boundary note (SYSTEM_BOUNDARY.md line 11) | Archive the sanctioned-worktree machinery; keep K1 rule only |
| frameworks/openspec | `ls ~/code2/*/openspec` was 12 repos on 11-07; AES has 25 specs under `openspec/specs/` | OFF-THE-SHELF (openspec CLI; AES configures) | R | None; belongs to Work flow, not here | Move out of this row |
| frameworks/canonical-sync | Timer not found (`systemctl is-enabled canonical-sync.timer`: not-found); was failing every 15 min on 11-07 | RETIRE | none | Same job as lane-sweep (fast-forward primary checkouts) | Confirm removed, mark retired |
| frameworks/lane-sweep | Ran 16:50 today, Result=success; timer every 10 min (list-timers) | AES-OWNED-PARTIAL (AES has `graph-checkout-refresh` spec; guess it covers the sync half only) | G, P | Overlap with graph-checkout-sync | Check what the AES spec covers; port worktree removal if missing |
| frameworks/worktree-rules | core.md: one worktree per agent, claims retired; `claude -w` in `~/code2/AGENTS.md` | TO-PORT (rule text lives in workspace core.md, not AES) | G, R | Old `~/code` claim rules contradict it; marked retired | Put the single rule in AES docs |
| frameworks/code-to-code2-move | 11-07: 55 unit files still use `~/code/...` symlink paths, 34 stray files at `~/code2` root | KEEP-OUTSIDE-AES | P | Two path layouts coexist | Repoint units when the manifest is written |
| pages/project-graph-page | project-graph-refresh ran 04:50 today; AES has 4 `project-graph-*` specs | AES-OWNED-DONE | P | None | None |
| data/wsl-vm-settings | `/mnt/c/Users/thela/.wslconfig` exists; not in any repo (11-07 review) | TO-PORT (copy into `aes-config` with install step) | R | Comment inside still names the off wsl-cache-guard | Commit file, fix comment |
| data/wsl-crash-record | 11-05: 17 "Fatal machine check" panics; not re-checked today | KEEP-OUTSIDE-AES | P | None | Leave |
| data/wsl-cache-guard | Off since 11-05; timer and service files absent (`ls ~/.config/systemd/user`) | RETIRE | none | `.wslconfig` comment still says it handles cache | Mark retired |
| data/batch-slice | 11-05: 276 tasks under the cap. Not re-run | TO-PORT (small: the unit file into git) | G | None | Put in manifest |
| data/storage-policy | storage-policy-monitor ran 16:56; AES timers use it as `exec_condition` gate (`timers.yaml`) | KEEP-OUTSIDE-AES | G | AES depends on it | Leave; name it in AES docs |
| data/c-drive-guard | Ran 16:01 today | KEEP-OUTSIDE-AES | P | Overlaps storage-policy monitor readings | Leave |
| data/disk-growth-report | 11-05: runs the same `storage-policy monitor` as the 15-min job | RETIRE | none | Exact duplicate command | Remove timer |
| data/disk-maintenance | Result=success, ran 04:11 today (was failing 11-04/05) | KEEP-OUTSIDE-AES | P | None | Leave |
| data/wsl-compaction | 11-05: 164 of 164 runs "skip". Latest log row I read is 2026-11-07 (still skip) | RETIRE (never compacts while agents run) | none | Overlaps WSL Rebuild, which does the real shrinking | Retire; rebuild is the shrinker |
| data/wsl-rebuild | schtasks today: Last Run 11/15 3:00 AM, Last Result 0, **Schedule Type One Time Only, Next Run N/A**. Core.md says "scheduled 2pm" | KEEP-OUTSIDE-AES | P | **Contradiction**: core.md and memory say a recurring 2pm standing yes; the task is one-shot at 3 AM | Report to Brian; do not restart anything |
| data/offload-cold | Result=success, ran 12:44 today | KEEP-OUTSIDE-AES | P | None | Leave |
| data/claude-conversation-backup | Ran 16:01 today | OFF-THE-SHELF (rclone to Drive) | P | Duplicate group row exists | Keep |
| data/codex-conversation-backup | Both timers ran 16:00-16:01 today | OFF-THE-SHELF (rclone) | P | Same | Keep |
| data/local-data-backup | **Broken**: last-run.status "failed" (11-16); `last-verified-run.utc` dated 11-13 (so some verified run happened since 11-07) | KEEP-OUTSIDE-AES | P | None | Read the current failure; fix |
| data/llm-observability-backup | Ran 03:47 today | KEEP-OUTSIDE-AES | P | None | Leave |
| data/run-artifacts-pack | Ran 03:17 today, success exit 0 | KEEP-OUTSIDE-AES (process_tracing data, a project) | none | Duplicate row | Merge with the jobs/ row |
| data/home-archive | 11-05: 245 MB. Not re-checked | KEEP-OUTSIDE-AES | P | None | Leave; compare before any delete |
| data/scratch | 11-07: 7.6 GB, 501 entries | KEEP-OUTSIDE-AES | G | Durable state must not live here | Leave |
| agent-config/safety-hooks | 11-07: blocks `git reset --hard`, force push; **misses** `gh repo delete`, `rclone purge`, `powershell.exe wsl --shutdown`, MCP tools. Rulebook not in git | TO-PORT | G, R, P | Overlaps jev-gate; both partial | Add the missing delete rules; commit rulebook |
| agent-config/jev-gate | 11-07: no `~/.jev-gate/mode` (confirmed absent today); runs fixed rules only, T1 logs but blocks nothing; 200 MB decisions log | TO-PORT (keep K1 and M1; retire T1) | G, P | Grid text claims "fast model decides"; not real | Fix the description; rotate log per day |
| agent-config/mcp-servers | 11-07: 6 local servers up, 12 account connectors, source `agent-skills/.rulesync/mcp.jsonc`. Today `ide` and `inside-success-second-brain` failed to connect in this session | OFF-THE-SHELF (rulesync) | R | Claude and Codex get different sets; connectors set in the account, not git | Per-project loading; document account-only ones |
| agent-config/permission-and-session-settings | Today: `permissions.allow` empty, skip-permission prompt true (`~/.claude/settings.json`) | TO-PORT | R, G | Reach set by prose and hooks only | Generate from git for both clients |
| new/pressure-sample | Ran 16:55 today | KEEP-OUTSIDE-AES | P | None | Leave |
| new/working-files-expiry | Ran 04:46 today | KEEP-OUTSIDE-AES | P | Deletes files: confirm contents compared (hard line) | Check its delete rule |
| new/recurring-jobs-and-setup-sources | `scripts/recurring_jobs.py`; AES has `failed-unit-watch` spec; timer ran 16:36 today | AES-OWNED-PARTIAL | P | Today 10 units are failed (`systemctl --user --failed`), so the watch is not clearing them | Show failed list on the front page |
| new/secrets-store | 11-07: 145 key names, 25 backup copies, not in git. Not re-counted | OFF-THE-SHELF (sops+age, guess from 11-07 review) | R, P | Whole-file load by one MCP server | Names-only template in git |
| new/github-account-routing | 11-07: wrapper `gh-wrapper` in git; routing doc stale (`gh-work` gone) | TO-PORT | G, R | Doc lives in legacy project-meta | Move doc into workspace topic |
| new/tailscale-network | 11-07: 7 nodes, key expiry 2026-12-20 for Mac mini and wsl-desktop; `tailscale status` today prints 7 lines | OFF-THE-SHELF | R | None | Add expiry watch |
| new/commit-hooks-lefthook | Adoption per repo not measured (11-07: 12 repos) | OFF-THE-SHELF | R | AES also has `lefthook.yml` | Measure adoption count |
| new/code2-repo-format | code2check in 9 of 200 repos (11-07); AES has lockstep specs | AES-OWNED-PARTIAL | R | Overlaps AES `lockstep` checks | Pick lockstep as the one check |
| new/night-only-guard | `workspace/scripts/night_only.py`; gates-nightly still ran 04:08 and 05:33 | UNKNOWN (missing check: does it defer anything today?) | P | gates-nightly used 3h CPU | Read its log |

#### Part priority

First: a machine-layer manifest in `~/code2/aes-config` (job, host, source path, install command, covering systemd units, Windows tasks, `.wslconfig`, Mac plists, VPS units). Basis: 42 of 84 timers are not links into git (`ls -l`), and the AES timer list renders 6 of 84. Without it a clean start loses scheduled jobs. Size: medium (guess: about 100 jobs to classify; the render tool `scripts/timers.py` exists).
Cheap and high value: move the safety-hook rulebook into git and add delete rules for `gh repo delete`, `rclone purge/delete` and `powershell.exe wsl --shutdown` (all passed in the 11-07 tests; not re-run today). Size: small (one rules file).
Also cheap: retire the 9 duplicate or dead items so the grid counts real things.

#### Could not check

- Re-test of the safety-hook gaps today (running them could trigger actions; only 11-07 results used).
- Why gates-nightly fails today (read only the log tail, not the full log).
- Current Mac mini, VPS and desktop WSL state (no ssh run).
- Whether the 11-07 counts (secrets keys, MCP connectors, openspec repos) still hold.
- Why local-data-backup is "failed" now.
- AES `graph-checkout-refresh` spec coverage of worktree removal (not read).
- The WSL Rebuild task's real schedule beyond `schtasks` output (core.md says 2pm; the task shows 3 AM one-time).

## Part: workflow

### Grid row "Work flow": review (checked 2026-11-16)

AES = Agentic Engineering System canonical (the one system Brian wants). All evidence below was read-only, on 2026-11-16 16:59 EST.

1. 31 items touch the Work flow row. By class: 3 AES-OWNED-DONE, 4 AES-OWNED-PARTIAL, 4 TO-PORT, 4 OFF-THE-SHELF, 10 KEEP-OUTSIDE-AES, 3 RETIRE, 3 UNKNOWN.
2. The grid (2026-11-06) is stale. AES has since taken over the failed-job watcher, the project graph and checkout sync, and Lockstep; Enforced Planning is gone from AES.
3. Biggest contradiction: `docs/capabilities.md` row 34 says the compliance-list timer has been off since 2026-11-09 (Brian: "turn off all nightly planning"). The timer is enabled and ran today 06:54.
4. Biggest gap: the two things an agent touches on every change, `ship` (merge) and `lane-sweep` (cleanup), still live only in the private workspace repo, not in AES. The move is proposed, not started.
5. Health: 10 timers are failing now, including `feedback-collector` (the Learn step) and `gates-nightly` (the Enforce step).

#### Table

Class names: AES-OWNED-DONE, AES-OWNED-PARTIAL, TO-PORT, OFF-THE-SHELF, KEEP-OUTSIDE-AES, RETIRE, UNKNOWN. "Serves": G = goal (effective agents), R = requirement (one consistent, shareable, configurable system), P = path (visible, trustworthy, clean start).

| item | status today (evidence) | belongs where | serves | overlap or contradiction | recommendation |
|---|---|---|---|---|---|
| Feedback learning loop (jobs/feedback-loop) | Collector timer enabled but last run FAILED 04:03 today: "reports=242 filed=227 errors=50 exit=1"; files its own failure as project-meta #2413. Problems, effects and fix-owner timers disabled (Brian: "i dont want to turn this stuff on"). AES has `scripts/learning_loop/` and spec `feedback-loop-notices`. | AES-OWNED-PARTIAL | G (agents learn), P | Runs from Project Meta paths and files issues into Project Meta, which is being retired. | Fix the 50 errors; move concern filing target off Project Meta. Small. |
| Failure and health watchers (jobs/failure-watch) | `failed-unit-watch` now ships from AES (`~/.hive-brain/aes/scripts/failed_unit_watch.py`, spec `failed-unit-watch`), last run 16:36 success. 10 units currently failed (`systemctl --user --failed`). | AES-OWNED-DONE | P (trust what it tells him) | Overlaps failures-page and front-page (three views of failed jobs). | Keep; let it be the one source. |
| Checkout and graph sync (jobs/checkout-sync) | `graph-checkout-sync` runs AES `refresh_canonical_checkouts.py`, success 16:32. The older `canonical-sync` timer is no longer listed. AES specs `graph-checkout-refresh`, `project-graph-refresh` exist. | AES-OWNED-DONE | P | The earlier two-timer overlap is resolved (only one timer remains). | None; remove stale grid note. |
| Policy and planning checks (jobs/policy-and-planning-gates) | `plan-status-refresh` now succeeds (own clone, fixed); `project-meta-policy-audit` enabled, ran 07:30 success; `company-planning-mirror` enabled. Plan says policy audit still needs an owner. | TO-PORT | R | Policy audit reads the Project Meta registry (263 rows); retirement plan proposes harvest, not port. | Decide per job: keep plan-status, switch off policy audit after harvest. Small. |
| User crontab (jobs/repo-crons) | `crontab -l` now: 1 never-absolute line and 1 openrouter snapshot. Weekly review is now a systemd timer (`weekly-review-log`, ran 08:13). | KEEP-OUTSIDE-AES | P | Claims sweep is moot since claims retired 2026-11-05. | Drop the grid row's claims part. None. |
| AES canonical (frameworks/aes) | Active: AES commits today (PR #912, #911). Self-governance (`.aes/`, claims, hooks) removed 2026-11-12 (`docs/retired/2026-11-12.md`). 25 OpenSpec specs; has Lockstep, timers, project graph. | AES-OWNED-PARTIAL | G, R | Grid said "on hold since 10-18": wrong now. Its own plan says Define/Enforce roles come from Lockstep + OpenSpec. | Update grid status to running. |
| Enforced Planning (frameworks/enforced-planning) | Repo last commit 2026-11-11. `enforced-planning-session-continuity` timer not found. Claims retired 2026-11-05; AES removed 44 files of its machinery 11-12. `capabilities.md` row 39 still says "still used in ~/code". | RETIRE | R | Contradiction: `~/code/AGENTS.md` says claims retired, capabilities row says still used in ~/code. Vendored copy also in Project Meta. | Archive after reading its repo's AGENTS.md profiles (continuous-light etc.) for ideas worth keeping. Small. |
| Company Planning (frameworks/company-planning) | Active: PR #364 merged today 16:24. Validator runs in ship, pre-push, Stop hook. | UNKNOWN | G, R | Not decided whether it is part of AES or a separate part; AES spec lists "planning subsystem split" (AES-PLAN-002). Also 11-09 "turn off all nightly planning" vs compliance-list. Check missing: Brian decision on its place. | Ask once; until then keep. |
| OpenSpec (frameworks/openspec) | 30 repos have `openspec/` (`ls -d ~/code2/*/openspec`), AES has 25 specs. Brian-pre-approved flow in `~/code2/AGENTS.md`. | OFF-THE-SHELF | G, R | Replaced AES plans and Project Meta plans 2026-10-13 (capabilities row 38). | AES configures it. None. |
| Project Meta governance (frameworks/project-meta-governance) | Last commit 11-11. Nine timers still use it; AES has ported: concern_issue, md_file_cap, project graph sync/refresh/dep scan, failed-unit-watch (AES `scripts/`). Retirement plan status "proposed"; nothing switched off. | AES-OWNED-PARTIAL | R, P | Two policy sources: `policy/registry.yaml` (263 rows) vs `core.md` + `rule-sources.md`. AES feedback loop still calls Project Meta. | Finish slices in the retirement plan; harvest rows still in force. Large (guess). |
| ecosystem-ops (frameworks/ecosystem-ops) | Repo commit today 15:32. `ecosystem-ops-daily` unit/timer not found now. Dashboard :8501 not checked. | KEEP-OUTSIDE-AES | P | Daily pipeline apparently gone; grid text says "exit 1". | Confirm dashboard still wanted. Small. |
| Hive brain controls watcher (frameworks/hive-brain-controls) | `hive-controls` ran 09:08 today: pushed 19 rows (was 17) to the VPS dashboard. AES has `scripts/hive/`. | AES-OWNED-PARTIAL (guess: code location not read) | P | Same job as the "hive-controls report" row. | Merge the two rows. None. |
| ship (frameworks/ship) | `~/.local/bin/ship` -> `workspace/scripts/ship.py`. Record-only-repo change (workspace PR #432) not merged; split proposal says move to AES core. | TO-PORT | G, R | `capabilities.md`: "never merge with gh pr merge". Mid-port: Brian chose carrying the planning-gate change into AES. | Port first (see priority). Medium. |
| lane-sweep (frameworks/lane-sweep) | Ran 16:51 today success (`systemctl --user`); still `workspace/scripts/lane_sweep.py`. | TO-PORT | G, P | Grid said last exit 1 (locked worktree); now success. | Port with ship. Small-medium. |
| weekly-plans / THIS_WEEK (frameworks/weekly-plans) | Not off: `personal-weekly-plans/THIS_WEEK.md` is a 151-byte pointer to `weekly-plans` repo, which has a commit today 15:30. | KEEP-OUTSIDE-AES | P | Grid status "off" is stale. | Update grid. None. |
| Failing jobs page (pages/failures-page) | `failures-page` timer enabled, ran 16:03 success. | RETIRE | P | Duplicates failed-unit-watch and front-page (which files issues for broken systems). Guess: nobody needs a third view. | Fold into front page after Brian confirms. Small. |
| Planning compliance list (pages/compliance-list) | Timer ENABLED, ran 06:54 today; capabilities row 34 says off since 11-09. | UNKNOWN | P | Direct contradiction between doc and machine. Missing: which is intended. | Ask Brian: on or off; fix the loser. Small. |
| agent-deck web (pages/agent-deck-web) | `curl 127.0.0.1:8420` fails (000); `agent-deck` systemd unit inactive. Binary exists in `~/.local/bin`. | KEEP-OUTSIDE-AES | P | Grid said running; it is not now. | Check if it should start on boot. Small. |
| Telegram relay and hive-stall alert (pages/telegram-relay-and-hive-stall) | Runs on the VPS; not checked (no network). Grid said broken 11-05. | KEEP-OUTSIDE-AES | P | None found. | Re-check by ssh. UNKNOWN status. |
| hive-controls report (pages/hive-controls-report) | Same job as the hive brain controls watcher. | RETIRE (as a separate row) | P | Duplicate row. | Merge into the watcher row. |
| LLM observability database (data/llm-observability-db) | Not re-measured today (needs disk read). Grid: 11 GB, writes deferred. `llm-observability-backup` timer enabled. | KEEP-OUTSIDE-AES | G (traces), P | Owned by llm_client, not AES. | Re-measure when row "Observe" is reviewed. |
| Log folders (data/logs-folders) | Not re-counted. Job logs still written under `~/projects/data/logs`. | KEEP-OUTSIDE-AES | P | None. | None. |
| Company Planning plugin (agent-config/company-planning-plugin) | Applied through `hooks-autoapply` (capabilities row 77). Skills listed in this session (company-planning:*). | UNKNOWN | G | Same decision as the Company Planning row. | Decide with that row. |
| Front page (new/front-page) | Ran 16:11 success hourly. | KEEP-OUTSIDE-AES | P | Split proposal puts `front_page*.py` in the machine layer. | Keep. None. |
| Recurring-jobs late check (new/recurring-jobs-and-setup-sources) | Called by front page; not separately run. | KEEP-OUTSIDE-AES | P | Overlaps AES `timer-config` spec (timers generated from a job list). | Consider moving to AES timers. Small. |
| GitHub Issues queue (new/github-issues-queue) | `~/code2/AGENTS.md`: tasks are GitHub Issues. `concern_issue.py` now in AES `scripts/`. | OFF-THE-SHELF | G, R | Project Meta's copy is a second source. | Switch callers to AES copy. Small. |
| Agent clients and options (new/agent-clients) | `agent-clients-update` timer enabled. `brian-profile` PR #1 would build Codex AGENTS.md; unproven (usage limit until 11-20). | OFF-THE-SHELF | R (configurable) | Claude and Codex configs are generated separately. | Prove the profile path on Codex after 11-20. Small. |
| llm-cost (new/llm-cost-cli) | `~/.local/bin/llm-cost` exists. | KEEP-OUTSIDE-AES | G | None. | None. |
| while-waiting sweep (new/while-waiting-sweep) | Skill is in this session's list. Adoption unmeasured (grid note). | TO-PORT | G | Rule text is in Brian's private `core.md`. | Move generic rule to AES core. Small. |
| Lockstep (new/lockstep) | In AES `src/lockstep/`; 8 specs (lockstep-*). Old repo `plan-code-wiki` folder still exists. | AES-OWNED-DONE | G, R | Two copies exist (old repo and AES); old one is history. | Archive old repo after a content check. Small. |
| Decision records (new/decision-records) | `code2-workspace docs/decisions` 0001-0006; required by code2 format. | OFF-THE-SHELF | R, P | None. | None. |

#### Part priority

Do first: port `ship` and `lane-sweep` (with the record-only-repo change and the planning gate) into AES core. Basis: every agent change goes through `ship` (capabilities row 19), the split proposal lists both as "core", and both already pass in daily use, so it is a move, not a build. Size: medium (guess: 2 scripts, their tests and spec, ~25 files counting specs; basis is the 85-script workspace folder with 6 generic tools named).

Cheap and high value: (1) resolve the compliance-list timer vs documentation contradiction (one question, one edit); (2) fix the `feedback-collector` failure (errors=50, journal line) so the Learn step runs; (3) correct stale grid rows (AES "on hold", weekly-plans "off", agent-deck "running", hive-controls duplicate). All small.

#### Could not check

- Telegram relay and hive-stall alert on the VPS (no network use allowed).
- ecosystem-ops dashboard on port 8501 and its current attention/inbox timers.
- Current size and write failures of the LLM observability database, current log folder counts.
- Where `hive/controls.py` for hive-controls lives (AES or workspace).
- Whether Company Planning is intended as part of AES (needs Brian).
- The `feedback-collector` 50 errors: cause not read, only the summary line.
- Whether `ship` and Company Planning validator actually run correctly end to end today (not executed; read-only).

## Part: human

### Grid row: Human interface (checked 2026-11-16 ~17:00 EST, read-only)

#### Summary

1. 26 grid items sit in this row, plus 10 items that the 2026-11-07 row review added but the grid JSON lacks (36 total). Counts by class are at the end of the table.
2. Most of the grid's "partly/broken" pages are already gone: 8 of the 14 systemd units the grid cites no longer exist (attention-page, control-publish, oversight-refresh, ecosystem-ops-daily, ecosystem-dashboard, export-reminder, policy-console-publish, agent-deck). The grid is stale, not the machine.
3. Brian's setup now has ONE status hub (front-page, hourly, last success 2026-11-16 16:12) plus the waiting:brian GitHub label as the needs-you list. That hub lives in the workspace repo, not in AES. AES holds the principle (SYSTEM_BOUNDARY AES-PLAN-005, AES-ECON-001) and the failed-unit-watch spec, but no human-interface feature.
4. Decisions approved 2026-11-05/06 are still not applied: hive root address for the hub (hive.brianmills.dev answers 303 today), "Needs you" on top (guess: not verified), status line parity.
5. Biggest risk to the "trust what it tells him" path: the hub's inputs are partly dead. 10 user services are failed now (e.g. projects-refresh, gates-nightly, feedback-collector, usage-pace), and the hub run costs 7.5 min CPU each hour.

#### Table (cells shortened; "PM" = Project Meta; "AES" = the canonical Agentic Engineering System repo)

| item | status today (evidence) | belongs where | serves | overlap or contradiction | recommendation |
| --- | --- | --- | --- | --- | --- |
| jobs/attention-control-center | Unit ecosystem-ops-daily: `systemctl --user cat` says missing. Grid said "failed". Gone. | RETIRE | none | Duplicate of pages/attention-page (row review 11-07 said merge). | Mark retired in grid. |
| jobs/failure-watch | failed-unit-watch.timer runs every 30 min (list-timers); AES has openspec/specs/failed-unit-watch. | AES-OWNED-DONE | path (trust) | Also feeds failures-page and front page; three views of one fact. | Keep; show only a count on hub. |
| jobs/pages-publishing | pages-deploy-catchup.timer and rr-public-export.timer exist; last runs 16:58 and 08:00 today. | KEEP-OUTSIDE-AES | path | None. | Keep. Re-check rr-public-export exit (grid said exit 1 on 11-05; now not failed). |
| frameworks/company-planning (acceptance criteria Brian can judge on a working UI) | Repo active; workspace commit 2026-11-16 "keeps Company Planning plugin current" (#451). AES SYSTEM_BOUNDARY: Company Planning is default planning provider; AES-PLAN-005 requires human-observable slices. | AES-OWNED-PARTIAL | goal + requirement | Company Planning vs "Enforced Planning" vs code2 plans: still three planning vocabularies (guess: count from retirement plan). | Keep; AES enforces human-observable slice rule. |
| frameworks/ecosystem-ops | Units missing; 127.0.0.1:8501 returns no response (curl 000). | RETIRE | none | Third status hub besides front page and oversight page. | Retire; archive repo per PM retirement plan. |
| frameworks/harness-assessment-status (group) | Group of pages; attention/control-publish/oversight units missing; failures-page, harness-live exist. | RETIRE | none | Duplicates its member items. | Delete grid row (merge into front-page). |
| pages/attention-page | Unit missing; ~/.local/share/attention/index.html last built 2026-11-07 03:27 (9 days old). control.brianmills.dev/attention/ gives 302. | RETIRE | none | Replaced by front page. | Retire. Stale file is a trap: do not read it as current. |
| pages/control-home-inbox | control.brianmills.dev gives 302 (redirect); control-publish unit missing. | RETIRE | none | Duplicates hub. | Retire. |
| pages/ui-index | ui-index.timer active, page built 2026-11-16 06:45 (153 KB). | KEEP-OUTSIDE-AES | path (find the UI) | None. | Keep; link from hub. |
| pages/ecosystem-dashboard | Port 8501 down; unit missing. Tunnel dashboard.brianmills.dev not checked. | RETIRE | none | Third hub. | Retire; confirm tunnel is removed (could not check). |
| pages/hive-dashboard | hive.brianmills.dev root gives 303 (login); healthz 200; plan pages 200. | RETIRE | none | Replaced by waiting:brian + front page. | Retire. |
| pages/glance-status | status.brianmills.dev gives 303. Off per switched-off.json (11-05). | RETIRE | none | Replaced hive dashboard, now also off. | Retire; stop VPS containers later (Brian-approved cut). |
| pages/hive-plans-pages | hive.brianmills.dev/plans/ returns 200 today. | KEEP-OUTSIDE-AES | path (Brian reads reviews) | None. | Keep; AES projects review pages here. |
| pages/failures-page | failures-page.timer exists, last run 16:03. | KEEP-OUTSIDE-AES | path | Overlaps failed-unit-watch + hub count. | Keep as agent-facing JSON. |
| pages/project-priorities-page | projects-refresh.service FAILED now (systemctl --failed). Grid said unknown. | TO-PORT (into front page) | path | Priorities also in oversight and hub. | Fix the failing job or fold into hub; small. |
| pages/oversight-page | oversight-refresh unit missing; scripts/front_page_oversight.py exists. | AES-OWNED-PARTIAL | requirement (rule origin shown) | Rules-with-sources now in AES docs/rules/RULES.md and workspace rule-sources.md: two copies. | Hub rules view reads AES RULES.md only. |
| pages/harness-assessment-page | Static file 2026-11-05; no timer. | RETIRE | none | Replaced twice (row review). | Retire (git keeps it). |
| pages/planning-package-review | `ls ~/code2/*/docs/planning/review-page` finds 0 dirs now (grid: 53). Path may have moved. | UNKNOWN | path | Overlaps hive-plans-pages (the server). | Check: find where review pages are built now. |
| pages/agent-deck-web | Port 8420 down; but agent-deck-autoupdate.timer still active. | RETIRE | none | Autoupdate timer contradicts the "cut" decision. | Retire; disable autoupdate timer (needs Brian-approved cut: row review said cut). |
| pages/policy-console-mac | Unit missing. | RETIRE | none | Rules view replaced it (approved 11-05). | Retire. |
| pages/telegram-relay-and-hive-stall | VPS service not checked (ssh is outside read-only scope here). PM retirement plan row 2: phone push ported into AES 2026-11-16. | AES-OWNED-PARTIAL | goal (agents reach Brian) | operator_notify_router.py still used by PM callers (7 in ecosystem-ops, plan line 44). | Verify relay error loop on VPS; keep one route. |
| pages/operator-notify-router | export-reminder unit missing. Retirement plan 11-16: failure alerts and phone push done in AES loop. | AES-OWNED-PARTIAL | goal + path | Old PM router vs AES feedback-loop-notices spec: two paths to Brian. | Ablate PM router once callers are gone. |
| agent-config/rule-system-core | core.md loaded by both clients; closeout and writing rules in it. AES has docs/rules/RULES.md + legacy-dispositions.yaml. | AES-OWNED-PARTIAL | requirement | core.md (workspace) vs AES RULES.md vs PM policy registry (263 rows): three rule stores. | TO-PORT core.md as AES-generated output; single source. |
| agent-config/permission-and-session-settings | ~/.claude/statusline-command.sh exists; settings.json has statusLine. | OFF-THE-SHELF | path | None. | AES configures it; check parity with Codex (not checked). |
| new/front-page | front-page.service success 16:12; 7 min 26 s CPU, 192 MB per run. scripts/front_page.py (workspace). | TO-PORT | path (see everything) | Capabilities row says page lives at hive private-plans URL; approved short address not applied. | Port to AES as the one hub; cut run cost. |
| new/closeout-format | core.md + topics/closeout.md. | TO-PORT | goal | Overlaps waiting:brian queue (decisions repeated vs stored). | Port into AES rules. |
| (extra) new/waiting-brian-queue | `gh issue list -l waiting:brian` returns issues (#417, #232...) in code2-workspace. | OFF-THE-SHELF | path | Not the same list as hub "Needs you" unless hub reads it (guess). | Keep as the single store. |
| (extra) new/human-contact-rules | authority-and-escalation.md now has the concrete-example rule (line 118) and toast rule (line 131). Moved already. | AES-OWNED-PARTIAL | requirement | Memory copies may remain (not checked). | Confirm memory duplicates removed. |
| (extra) new/representation-router | Separate repo; not re-checked beyond row review. | KEEP-OUTSIDE-AES | path | None. | Keep. |
| (extra) new/remote-control-claude | remote-control.service inactive. | OFF-THE-SHELF | goal | None. | Check it is meant to be inactive. |
| (extra) new/remote-control-codex | codex-remote-control.timer fires every 5 min, active. | OFF-THE-SHELF | goal | None. | Keep. |
| (extra) new/dashboard-tunnel | Not checked. | RETIRE | none | Goes with ecosystem dashboard. | Remove with it. |
| (extra) new/hive-spend-push | hive-spend.timer enabled. Pushes to a switched-off screen (row review). | KEEP-OUTSIDE-AES | path | Alert part useful. | Keep alert, stop push. |
| (extra) new/ask-agent | Not checked. | UNKNOWN | goal | None. | Check usage in last 30 days. |
| (extra) new/voice-mode | Not checked. | RETIRE | none | Claude app voice covers it. | Remove. |
| (extra) new/harness-review-pages | The page in use. | KEEP-OUTSIDE-AES | path | None. | Fold into planning page when review ends. |

Counts (36 items): RETIRE 13; KEEP-OUTSIDE-AES 7; AES-OWNED-PARTIAL 6; OFF-THE-SHELF 4; TO-PORT 3; UNKNOWN 2; AES-OWNED-DONE 1.

#### Part priority

Single first piece: make the front page the one trusted hub inside AES, reading only live sources, with "Needs you" (the waiting:brian list) on top and each source showing its age. Basis: it serves the path directly and the grid shows the old pages are already off. Size: medium (guess: front_page.py exists; port plus cut 7-minute run cost).
Cheap, high value: (1) fix or retire the 10 failed units that feed the hub (small, each is one unit); (2) apply the approved short address (small); (3) delete stale attention index and retire dead grid rows so he is not shown nine-day-old data (small).
What an autonomous coding agent would miss if this part vanished: the closeout format and waiting:brian queue (how it asks), not the pages.

#### Could not check

- VPS services (telegram-relay, hive-stall, glance containers, tunnel): ssh not run.
- Whether the hub's "Needs you" is on top and its content (page behind login gives 303).
- Where the 53 planning review pages moved; Codex status line parity; memory duplicates of question rules; ask-agent and voice-mode use.

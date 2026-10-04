# Hive brain v1: living plan

**Authority:** Brian's goal of 2026-10-02 and his rule changes of 2026-10-03 and
2026-10-04, all quoted under "Outcome". This repository is the home.
**Planning method:** Company Planning, durable one-human plan (`durable_solo`).
Product code under the governed roots still goes through `aes plan`.
**Who reads this:** any agent or session that picks up the work; Brian, for
"where are we against v1". This file holds only the current state; the
chronicle with its evidence is `PROGRESS_LOG.md` beside it.
**Stage:** personal pilot (Brian plus his agents), not a team product.
**Last update:** 2026-10-04 05:50 UTC.

## In one paragraph

Three robot workers on Brian's rented server, run by a program called
Paperclip, read his weekly plan, pick a job a worker can do, build it
unattended into a pull request, run the repository's own checks, merge it and
leave a report. Brian hears on his phone the moment a worker needs him and
answers there or on a private web page; otherwise he is not asked. Each
repository the workers touch has a four-page project brain they read first.
Guardrails log what every session does, a learning loop turns repeated
failures into rules, and a daily check says whether any piece has gone quiet.
Five jobs have been merged so far from two repositories.

## Words used here

- **Paperclip:** the program on personal-vps that runs the workers and their
  to-do board (https://paperclip.brianmills.dev). Tasks are `BRI-<n>`.
- **The workers:** Coordinator (plans and assigns), Research and Code Review
  (builds and reviews), Brian Contact (writes to Brian; mostly idle now).
- **Project brain:** `.project-brain/{now,project,state,truth}.md` in a repo:
  what it is, where it stands, where the last person stopped, what was decided
  and rejected. Layout: agent-skills `contracts/client-config/agents/project-brain.md`.
- **Jev gate:** a watcher on every Claude Code and Codex session on Brian's
  machine that logs risky commands (observe mode) and can block them (guard
  mode). **CC Safety Net:** a separate hook that blocks dangerous git and shell
  commands outright. **Rule K1:** the one enforced rule, "never remove the
  worktree you stand in".
- **Relay:** `telegram-relay.service` on personal-vps (personal-vps
  `apps/telegram-relay`): workers' messages on board thread BRI-2 go to
  Brian's phone; his replies, from Telegram or the dashboard's message box, go
  to the Coordinator.
- **Learning loop:** lessons, frictions and problems become labelled GitHub
  issues; a recurring failure becomes a rule proposal
  (`proposals/aes-learning-loop/DESIGN.md`).
- **Silence check / readout:** `scripts/hive/controls.py` (did every piece do
  its job recently) and `scripts/hive/readout.py` (what the system did this
  week). Index of all the scripts: `scripts/hive/README.md`.

## Outcome

**Brian's goal, 2026-10-02:** get his personal hive brain to v1, with AES
canonical as its home. His AI Astronauts hive-brain design is the vision,
scaled to him, his agents, and one brain per project. It is built from
off-the-shelf tools wherever they exist, as a speedrun, with benchmarks only
when a specific decision needs one.

**Brian, 2026-10-03 (changes the review step):** "i dont even want to answer
merge for anything that isnt public facing and that is not irreversible." So
agents merge their own pilot pull requests once the repository's checks pass
(its own local checks, `make check` or the equivalent; no hosted CI, Brian
2026-10-03. A checker a job adds, such as the wiki's stale-page report, may
exit 1 to say "findings"; that is its result, not a failed check)
and leave a report on the task; Brian is asked first only when a change is
public-facing (a live site, a published package, anything visible outside his
own machines and private repositories) or irreversible (deletes data or
history, deploys, migrates a database, sends anything outward). He also asked
for plain language, so this file says what each name means where it can.

**Brian, 2026-10-04 (narrows it again):** "public facing means only live sites.
and actually the assumption should be that i dont need to explicitly approve
merges even for those unless i say so. really no one is looking at my website so
i only care about things that i have already sent out for people to review." So
no merge needs his yes, public repositories and live sites included, unless he
has said that specific surface is out with other people for review; agents
still ask for irreversible actions (deleting data or history, database
migrations, sending anything outward).

**v1 is done when all five are true, each shown by a command's output or a link:**

1. **Pilot.** At least three real tasks from at least two of Brian's projects
   each went from the weekly plan to a merged pull request without
   hand-holding: the Coordinator plans it, agents build it unattended, the
   repository's checks pass, the agents merge it and leave a report Brian can
   read. Brian is asked first only for a surface he has said is out with
   other people for review, or for an irreversible action (his rules of
   2026-10-03 and 2026-10-04). Tasks 1 and 5 were merged on his yes before the
   rule was narrowed.
2. **Capabilities.** All 11 capabilities have a chosen off-the-shelf tool that
   is running and was used by those tasks (table below).
3. **Learning loop closed once.** Lessons, frictions and problems are filed as
   issues and labelled by Jev. A recurring failure family produces a rule
   proposal Brian accepts. The rule is enforced (an AES check or the Jev gate),
   its log shows it firing, and a wrong block comes back as a friction. The
   loop's own rules sit behind the three-level brake
   (`proposals/aes-learning-loop/DESIGN.md`).
4. **Nothing silent.** Every control logs what it did, and none went silent for
   a week.
5. **Pick-up.** A fresh agent can resume from this file alone: where we are,
   what's next, how to check it.

**Not in v1:**
- a real dashboard (the terminal stands in for it);
- re-cutting the failure families;
- team features (departments, several people's brains);
- anything Inside Success.

**Brian decides before it happens:** restarting WSL, spending more than trivial
API costs, and anything sent outward.

## Where we are (2026-10-04 05:50 UTC)

| Condition | Status | Evidence |
|---|---|---|
| 1 Pilot | **done** | five jobs merged from two repositories: BRI-17 → AES #88 (Brian's yes, 2026-10-03); BRI-21 → personal-wiki #13, BRI-24 → #14, BRI-26 → #15 (merged by the worker); BRI-27 → AES #110, #112, #116, #118 (merged from the terminal on his yes and under his rules, 2026-10-04). `python3 scripts/hive/readout.py --days 7` lists them with cost and hours |
| 2 Capabilities | partway | 11 rows running; 10 used by a job. The one not yet used is governance (C-GOV): the gate has watched every session but no rule has blocked real work (table below) |
| 3 Learning loop | partway | rule K1 came from a failure that happened twice, Brian accepted it, it is enforced and a live-test block is logged (2026-10-03); still needed: a block in real work, and one wrong block filed as a `kind:friction` issue |
| 4 Nothing silent | partway | `controls.py` runs daily and at each stop (12 controls, 12 ok on 2026-10-04); first all-clean day 2026-10-03; seven needed |
| 5 Pick-up | partway | cold pick-up tests on 2026-10-03 (twice; gaps fixed in AES #82 and #99) and 2026-10-04 after this rewrite: verdict "partly" (a stale row, a wrong count, one unexplained sentence, one overstated "done"), all fixed in the same commit; next test after the next rewrite |

**Current activity:** the workers take jobs from the refreshed weekly plan on
their own; the terminal session merges AES pull requests and keeps this file
current; the other conditions are evidence that accrues (a rule blocking real
work, seven quiet days, a pick-up test after each rewrite).

The machine-readable copy is `scripts/hive/conditions.json`; the hosted
dashboard reads it. Update it with evidence whenever a condition moves.

## Capabilities

The 10 capability ids come from the AI Astronauts hive-brain roadmap
(`PL.roadmap.capabilities` in the hive-brain explainer, 2026-10-01); C-ROUTE
was added 2026-10-03.

| Capability | Chosen tool | State (2026-10-04) | v1 evidence still needed |
|---|---|---|---|
| C-ORCH orchestration | Paperclip on personal-vps | running since 2026-10-03 15:22 UTC on Brian's one-year token; one new job per 6 hours, 2 open at once; drove jobs 1–5 | done for v1 |
| C-MSG agent messaging | Paperclip task threads | task threads with child tasks and wake-ups carried every job (BRI-20 → 21 → 23 → 24 → 25 → 26) | done for v1 |
| C-HUMAN-IF human interface | terminal relay of Paperclip `Decision:` tasks; Brian's Telegram-bound board thread BRI-2 for anything that needs him, at the moment it is asked (Brian, 2026-10-03: "i want to know as soon as my agents try to send me a message and for them to get my response as soon as i respond"); the dashboard, hosted at hive.brianmills.dev (his yes, 2026-10-03), as the overview | terminal relay `decisions.py`; Brian's Telegram thread BRI-2 both ways through the relay (proved by hand 2026-10-03 22:57–23:05 UTC, automatically 2026-10-04 03:57); hosted dashboard https://hive.brianmills.dev with a message box and one-tap answers (deployed 2026-10-03 23:10) | partway: built and proven both ways; Brian's own first look at the hosted page and one tap not yet seen |
| C-IDENTITY identity | one brain per project: `.project-brain/` in each repo (agent-skills `project-brain.md` layout), read first via the repo's `CLAUDE.md`/`AGENTS.md` | brains in AES, theory-forge, cybernetic_influence_v3 and personal-wiki; jobs 2–5 read and updated the brain of the repo they worked in; only personal-wiki has the `CLAUDE.md` pointer so far | done for v1; pointers for theory-forge and cybernetic_influence_v3 are a weekly-plan line |
| C-KNOW knowledge | git: each repo's `.project-brain/`; one task's plan in Paperclip issue documents (chosen 2026-10-02 after a landscape review; gbrain, Hermes, mem0/Letta/Cognee rejected for v1, reasons in `.project-brain/truth.md`) | the brains are the knowledge layer; jobs 2–5 updated `now.md`/`state.md` in their pull requests | done for v1 |
| C-CONTEXT context freshness | Paperclip re-reads agent and project settings each run (its `DEVELOPING.md`, "Config Freshness"); `scripts/hive/brain_fresh.py` for stale brains and checkouts behind GitHub | Paperclip re-reads agent instructions each run (rule changes took effect on the next run three times on 2026-10-03/04); `brain_fresh.py` runs daily inside `controls.py` | done for v1 |
| C-GOV governance | Jev gate + CC Safety Net + hive-brain settings as AES config | CC Safety Net on; Jev gate in observe mode in every Claude and Codex session; rule K1 enforced since 2026-10-03; `settings_check.py` 22 of 22 match | a block in real work; guard mode after the 2026-10-09 log review (condition 3, M2) |
| C-LEARN learning | AES learning loop (GitHub issues + Jev labels) | slices 1–2 done: 2,575 legacy learnings labelled; new issues labelled weekly (summaries on #74); K1 is the first rule through the whole loop | condition 3 |
| C-EVAL evaluation | readout from logs and traces: `python3 scripts/hive/readout.py [--days N]` (Paperclip tasks, pilot tasks, runs and failure codes; Jev and Safety Net decisions; learning-loop items by family; controls) | `readout.py` (tasks, jobs with cost and hours, runs, gates, loop items, clean days) ran over every job; cost per job in it since AES #100 | done for v1 (one weekly readout at acceptance) |
| C-RUNTIME runtime | netcup personal-vps, nightly backups to Drive | running; nightly backups to Drive (`vps-backup.timer`); restore check passed 2026-10-02; hosts the board, the relay and the dashboard | done for v1 (rerun the restore check before acceptance) |
| C-ROUTE model routing (throughput and cost) | Paperclip's own per-agent model and per-task model override (landscape review 2026-10-03: per-prompt routers such as OpenRouter Auto, RouteLLM, NotDiamond and the new `typesafe/jev-router` don't yet handle long tool-using agent sessions); a Codex builder agent on the ChatGPT subscription next | Coordinator on `claude-sonnet-5`, builder on `claude-opus-5` (2026-10-03, checked by `settings_check.py`); cost per run is in Paperclip's run records | a pilot task run under the routed setup, with cost and throughput per task in `readout.py` |

## Milestones

| # | Milestone | State | Done when |
|---|---|---|---|
| M1 | **Pilot running.** The Coordinator picks agent-doable items from Brian's personal weekly plan, agents build them, and decisions reach the terminal | done 2026-10-03: job 1 reviewed through `decisions.py` and merged (AES #88); the queue has run since | one job reviewed and merged |
| M2 | **Governance on everywhere.** Jev gate observe mode in all of Brian's repositories for Claude and Codex, then guard mode after a log review; hive-brain settings as an AES config file (`scripts/hive/settings.json`: agents, heartbeats and caps, gate mode, timers) | in progress: observe mode everywhere; K1 enforced; settings file checked live; guard mode waits on the wrong-deny fix (weekly plan, Priority 7) and the 2026-10-09 log review | guard mode on, with a week of log |
| M3 | **Learning loop slices 2–5,** plus coaching for Brian | slice 2 fully specifiable; 3–5 conditional on slice 2 counts | condition 3 |
| M4 | **Knowledge, identity, context.** Choose the knowledge layer; one brain per project; context freshness | done for v1 2026-10-03: brains in four repos; jobs 2–5 read and updated them; freshness checked daily | each used by a job |
| M5 | **Evaluation and observability.** Weekly readout; check that no control went silent | in progress: readout and silence check run; first all-clean day 2026-10-03 | condition 4 |
| M6 | **Model routing.** Per-agent models (done 2026-10-03), a Codex builder agent on the ChatGPT subscription, per-task overrides, cost and throughput per task in the readout, then more parallel runs once a week of logs shows no subscription caps hit | in progress | C-ROUTE row |
| M7 | **v1 acceptance.** All five conditions shown with evidence | conditional: 1 of 5 conditions met | — |

## How the jobs run now

The Coordinator picks one agent-doable line from
`weekly-plans/personal/THIS_WEEK.md` (refreshed 2026-10-04, week of 2026-10-05:
Priority 7's four lines, Priority 5's two) at most every 6 hours, with 2 jobs
open at once, and assigns it to Research and Code Review with the repository,
the exact change, the check, and the limits (no deploys, nothing outward, no
edits to `weekly-plans`). The worker reads the repo's `.project-brain/now.md`
first, builds, runs the repository's own checks, merges with a merge commit,
updates `now.md` in the same pull request and reports on the task. Brian is
asked only for a surface he has said is out with other people for review, or
for an irreversible action; the ask goes to his phone at that moment. Since
2026-10-04 06:00 UTC the workers can merge in AES canonical too: the repo's own
hook accepts `gh pr merge <n> --merge` once the checks pass and still refuses
squash and rebase (AES evidence names branch commits).

**Check:** the job task's comments show the merged pull request and the check
output; `python3 scripts/hive/decisions.py` shows nothing waiting on Brian.
**Rollback:** the "Pilot work" section of the Coordinator's instructions
(dated `.bak-` copies beside it).

## Decisions and assumptions

| Choice | Disposition | Reason / evidence |
|---|---|---|
| AES canonical is the home of the whole hive brain | human_set | goal 2026-10-02 ("recommendations stand unless I say otherwise") |
| Solo plus one brain per project, no departments | human_set | same |
| The terminal is the dashboard for now | human_set | same; Brian 2026-10-02 "for now in tui" |
| Coaching for Brian is part of the learning loop | human_set | same |
| Where cross-project rules live: action rules in the Jev gate policy (all repositories); repository rules in each repository's own checks or AES target; cross-project working rules in one rulebook section here | human_set (as recommended) | same; recommended 2026-10-02 |
| The loop's fixed core is the four items in `proposals/aes-learning-loop/DESIGN.md` | human_set (as recommended) | same |
| Pilot tasks are picked by the Coordinator from Brian's weekly plan, not by Claude | agent_decided_reversible | the hive-brain design gives planning to the orchestrator; it tests C-ORCH for real |
| Thin glue around off-the-shelf tools lives in `scripts/` (ungoverned); AES product logic goes through `aes plan` | agent_decided_reversible | speed. **Wrong when:** a script passes ~300 lines or holds logic that isn't tied to one tool; then it moves under `aes plan` |
| Failure families are not re-cut for v1 | agent_decided_reversible | issue #64. **Wrong when:** a weekly spot check finds fewer than 8 of 10 acceptable |
| The weekly plan (refreshed 2026-10-04 on Brian's yes, week of 2026-10-05) is a fair source of jobs | assumption | the Coordinator exhausted the previous plan's lines on 2026-10-03; if Brian's priorities move again, the plan is refreshed the same way, by draft and his yes |
| Agents merge their own pilot PRs after the repository's checks; Brian is asked only for a surface he has said is out with others for review, or for an irreversible action | human_set | Brian, 2026-10-04 (quote under Outcome): "public facing means only live sites" and no merge approval is assumed unless he says so; replaces the 2026-10-03 public-facing exception, under which pilot 5 (public repo) asked him twice. In all three agents' instructions (backups `.bak-20261004-merge-rule-v3`), the workspace rules (projects-dotclaude #77) and memory |
| (superseded 2026-10-04) agents merge private, reversible PRs; Brian asked for public-facing or irreversible changes | human_set | Brian, 2026-10-03 (quote under Outcome); replaces the 2026-10-02 "Decision: merge" step for private, reversible changes; Coordinator rule backup `AGENTS.md.bak-20261003-merge-rule` |
| A docs-only follow-up that only records what an approved merge made true is covered by that approval: agents merge it and report, no new `Decision:` | agent_decided_reversible | 2026-10-04: PR #116 fixed two README/brain sentences that Brian's 05:04 yes to #110+#112 had made false; asking again is the noise his 2026-10-03 rule removes. In both working agents' instructions (backups `.bak-20261004-docs-followup`). **Wrong when:** Brian objects to a docs merge he was not asked about, or a "docs-only follow-up" turns out to change behaviour |
| Pilot cadence: at most one new pilot task every 6 hours (was 12), 2 open at once | agent_decided_reversible | 2026-10-03: pilot 1 took about 80 minutes from creation to merge, so a 12-hour floor would spend two days on a few hours of work; the 2-open cap already bounds Brian's review load. Old rule kept as `AGENTS.md.bak-20261003-cadence` beside the Coordinator's instructions. **Wrong when:** two `Decision:` tasks wait on Brian for more than a day, or he says reviews arrive too fast |
| Repositories with only `AGENTS.md` get a two-line `CLAUDE.md` that points to it and to the brain | agent_decided_reversible | 2026-10-03: the VPS agents' Claude Code (2.1.278, no `instructionFiles` setting) loads only `CLAUDE.md`; the local setting that also loads `AGENTS.md` is not there. **Wrong when:** a pilot run log on an `AGENTS.md`-only repo without the pointer shows the brain was read anyway |

## Human decisions

None open. Answered so far: the six design points (goal, 2026-10-02); rule K1
(2026-10-03); the merge rule, twice (2026-10-03, 2026-10-04); hosting the
dashboard (2026-10-03, deployed the same night); the weekly plan refresh
(2026-10-04); merging AES PRs #110 and #112 (2026-10-04).

## How to check and act

- **Board:** `scripts/hive/board.sh GET|POST|PATCH <api-path>` runs a request
  on the Paperclip board over `ssh personal-vps` (ids in the script's header).
  Company `C=da165590-b0b3-4bf9-bb7f-e455292df499`. Kickoff task BRI-13
  `c8a83262-03e9-4b7a-b8fd-734cfe1d9b44` (the Coordinator's home; a comment
  there wakes it). Brian's Telegram thread BRI-2
  `519c6831-6967-4177-aef5-5aaea5d91850`. Agents: Coordinator
  `8964a584-ddfe-4fb1-b14f-c1503ae5ec23`, Research and Code Review
  `4d008def-4e59-47c2-bccf-ec5313e12ce2`, Brian Contact
  `4331dfbd-6a12-4965-b28a-d296c5aa9d3a`. Board in a browser:
  `https://paperclip.brianmills.dev/BRI/issues/<BRI-n>`.
- **Dashboard (Brian's view, phone-friendly):** https://hive.brianmills.dev,
  private behind Cloudflare Access (his email only), rebuilt every 15 minutes
  on personal-vps (`apps/hive-dashboard`); one-tap answers post on the waiting
  task; the message box posts on BRI-2. Checks: an anonymous `GET` is a 302 to
  the Access login; `ssh personal-vps systemctl list-timers
  hive-dashboard-build.timer` shows the next run; this machine's
  `hive-controls.timer` pushes the silence check's rows to the page. Rollback
  and design notes: `apps/hive-dashboard/README.md`, `scripts/hive/dashboard-use-case.json`,
  `scripts/hive/DASHBOARD_FEEDBACK.md`.
- **Phone channel:** `ssh personal-vps sudo journalctl -u telegram-relay -n 30`
  shows one line per message either way; `controls.py` has a "Telegram relay"
  row (silent after 10 minutes).
- **AES merge gate:** `.claude/hooks/worktree-coordination/enforce-make-merge.sh`
  (a Claude Code hook in this repo) allows `gh pr merge <n> --merge`, refuses
  `--squash`/`--rebase` and flagless merges, and still routes `gh api` merges
  and `make merge` through `make finish`. Test with a fake tool input:
  `echo '{"tool_input":{"command":"gh pr merge 1 --merge"}}' | bash <hook>` exits 0.
- **Workers' rules:** `/paperclip/instances/default/companies/<C>/agents/<agent-id>/instructions/AGENTS.md`
  inside the `paperclip` container on personal-vps (the Coordinator's "Pilot
  work" section holds the job rules). Edit with a dated `.bak-` copy beside it;
  Paperclip re-reads it each run, and the agent's next comment shows it did.
- **Terminal relay:** `python3 scripts/hive/decisions.py` (agents not working,
  then tasks waiting on Brian; exit 1 while an agent is broken).
- **Silence check:** `python3 scripts/hive/controls.py` (exit 0 = nothing
  silent). **Weekly readout:** `python3 scripts/hive/readout.py --days 7`.
- **Brain freshness:** `python3 scripts/hive/brain_fresh.py <repo> [--fetch]`.
- **Rule K1** (accepted by Brian 2026-10-03, enforced): the Jev launcher blocks
  `git worktree remove` of the folder the session stands in (AES #78,
  agent-skills #424). Installed as `~/.local/bin/jev-gate-worktree-guard` and
  `~/.local/bin/jev-gate-hook`; blocks are `rule: K1-worktree-cwd` rows in
  `~/.jev-gate/decisions.jsonl`, counted by `readout.py`.

## Exact next action

0. Agents run: `python3 scripts/hive/decisions.py` prints "Agents not working:
   0 of 3" and exits 0. If not, read the latest run
   (`scripts/hive/board.sh GET "/api/companies/$C/heartbeat-runs?agentId=<id>&limit=3"`).
1. **Jobs keep flowing on their own.** The Coordinator's next pick comes at
   least 6 hours after the last (BRI-27 at 03:40 UTC on 2026-10-04). The worker
   merges its own pull request in every repository, AES included, once the
   checks pass. If a `Decision:` task appears for a merge, the rule did not
   fire: answer it on the board with the rule and fix the instruction.
2. **Condition 3 (and the governance row of condition 2):** rule K1 must block
   real work once (watch `rule K1 blocks` in `readout.py`) and one wrong block
   must come back as a `kind:friction`, `source:gate` issue. K1 had no wrong
   block in 54 replayed cases; if a week passes with none, reword the
   condition to count the gate's wrong denies (AES #72, #73) or wait for guard
   mode.
3. **M2:** the Jev wrong-deny fix is weekly-plan Priority 7 line 4; guard mode
   (`jev-gate-hook --mode guard`) only after the 2026-10-09 log review shows
   every `deny` row right.
4. **Run failures to watch:** three Coordinator runs failed in about 5 s with
   "terminal limit failure" (2026-10-03 19:40, 2026-10-04 00:12 and 00:43 UTC),
   each followed by a good run; it looks like the Claude usage limit shared by
   Brian's local sessions and the agents near 5-hour window edges. `readout.py`
   counts them under `failure codes`; `decisions.py` stays green because the
   latest run succeeded. If they keep coming, the C-ROUTE lane (session "aes")
   lowers the Coordinator's 30-minute idle heartbeat or its model.
5. **Condition 4:** `python3 scripts/hive/readout.py --days 7` must show seven
   days with only clean runs (first clean day 2026-10-03; earliest 2026-10-10).
6. **Condition 5:** after any rewrite of this file, give a fresh agent only
   this file and ask where things stand, what is next and how to check;
   record the verdict in `PROGRESS_LOG.md` and fix what it could not answer.
7. **Tidy, not gating:** `CLAUDE.md` pointers for theory-forge and
   cybernetic_influence_v3 (weekly-plan line); the cybernetic_influence_v3 local branch
   `claude-md-pointer-20261003` is a leftover with a two-line commit.

## Recent changes

Full chronicle with evidence: `PROGRESS_LOG.md`. Latest, newest first:

- 2026-10-04 06:00 UTC: the AES merge hook accepts merge-commit merges (PR
  #126), so workers can finish AES jobs unattended; the merge-rule friction is
  AES #124 (learning loop).
- 2026-10-04 05:35 UTC: PR #118 (hook install leaves a clean tree) merged;
  BRI-31/32 closed. Eight pull requests from five jobs.
- 2026-10-04 05:2x UTC: Brian narrowed the merge rule ("public facing means
  only live sites"; no merge approval unless he says so); applied everywhere.
- 2026-10-04 05:04 UTC: Brian's yes; AES PRs #110 and #112 merged; `make
  check` green from a clean clone for the first time.
- 2026-10-04 03:40 UTC: the Coordinator filed the first job from the refreshed
  plan, exactly at its floor.
- 2026-10-03 23:39 UTC: weekly plan refreshed on Brian's yes (Priority 7).
- 2026-10-03 23:10 UTC: dashboard hosted at hive.brianmills.dev; 23:05 the
  relay went live and proved both legs.

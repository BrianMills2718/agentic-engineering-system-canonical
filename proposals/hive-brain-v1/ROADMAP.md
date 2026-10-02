# Hive brain v1: living plan

**Authority:** Brian's goal of 2026-10-02 (quoted under "Outcome"). This repository is the home.
**Planning method:** Company Planning, durable one-human plan (`durable_solo`). Product code under the governed roots still goes through `aes plan`.
**Who reads this:**
- any agent or session that picks up the work;
- Brian, for "where are we against v1".

**Stage:** personal pilot (Brian plus agents), not a team product.
**Last outcome-bearing update:** 2026-10-02.
- Plan written; state taken from live checks (see "Evidence").
- M1 pieces 1–3 done; the pilot was kicked off as Paperclip task BRI-13.
- Late 2026-10-02: every Paperclip agent run was failing (expired Claude login,
  upstream bug). Fix wired; it waits on Brian creating a one-year token
  ("Human decisions" below).

## Outcome

**Brian's goal, 2026-10-02:** get his personal hive brain to v1, with AES
canonical as its home. His AI Astronauts hive-brain design is the vision,
scaled to him, his agents, and one brain per project. It is built from
off-the-shelf tools wherever they exist, as a speedrun, with benchmarks only
when a specific decision needs one.

**v1 is done when all five are true, each shown by a command's output or a link:**

1. **Pilot.** At least three real tasks from at least two of Brian's projects
   each went through four steps without hand-holding in between: plan, agents
   build it unattended, Brian reviews in the terminal, merge.
2. **Capabilities.** All 10 capabilities have a chosen off-the-shelf tool that
   is running and was used by those tasks (table below).
3. **Learning loop closed once.** Lessons, frictions and problems are filed as
   issues and labelled by Jev. A recurring failure family produces a rule
   proposal Brian accepts. The rule is enforced (an AES check or the Jev gate),
   its log shows it firing, and a wrong block comes back as a friction. The
   loop's own rules sit behind the three-level brake
   (`../aes-learning-loop/DESIGN.md`).
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

## Capabilities

The 10 capability ids come from the AI Astronauts hive-brain roadmap
(`PL.roadmap.capabilities` in the hive-brain explainer, 2026-10-01).

| Capability | Chosen tool | State 2026-10-02 | v1 evidence still needed |
|---|---|---|---|
| C-ORCH orchestration | Paperclip on personal-vps | running, but every agent run has failed since 2026-10-02 20:30 UTC (expired Claude login, see Progress log); fix waits on Brian's token | agents run again; it drove the three pilot tasks |
| C-MSG agent messaging | Paperclip task threads | in use (BRI-5 → BRI-8 handoff) | the same, on pilot tasks |
| C-HUMAN-IF human interface | terminal relay of Paperclip `Decision:` tasks; dashboard later | `python3 scripts/hive/decisions.py` lists agents not working (exit 1), then every task waiting on Brian or blocked; first run 2026-10-02 found 2 stale setup tasks (closed) | pilot reviews done through it |
| C-IDENTITY identity | one brain per project: `.project-brain/` in each repo (agent-skills `project-brain.md` layout), read first via the repo's `CLAUDE.md`/`AGENTS.md` | AES has the first brain (2026-10-02) | each pilot project has a project brain agents read |
| C-KNOW knowledge | git: each repo's `.project-brain/`; one task's plan in Paperclip issue documents (chosen 2026-10-02 after a landscape review; gbrain, Hermes, mem0/Letta/Cognee rejected for v1, reasons in `.project-brain/truth.md`) | chosen; AES brain committed | used by a pilot task |
| C-CONTEXT context freshness | Paperclip re-reads agent and project settings each run (its `DEVELOPING.md`, "Config Freshness"); `scripts/hive/brain_fresh.py` for stale brains and checkouts behind GitHub | checker built; caught theory-forge `HANDOFF.md` (183 days, 209 commits since, exit 1) | run before pilot tasks; a stale case caught on a pilot project |
| C-GOV governance | Jev gate + CC Safety Net + hive-brain settings as AES config | CC Safety Net on for Claude and Codex; Jev gate in observe mode in every Claude and Codex session (2,334 decisions logged by 2026-10-02 late; Codex confirmed 2026-10-02, see Progress log); settings not in config | Jev gate in guard mode across projects; settings file; a block shows up in the log |
| C-LEARN learning | AES learning loop (GitHub issues + Jev labels) | slice 1 done: 2,575 legacy learnings labelled (PR #66); first lesson filed (issue #64) | condition 3 |
| C-EVAL evaluation | readout from logs and traces | none | a weekly readout over pilot tasks |
| C-RUNTIME runtime | netcup personal-vps, nightly backups to Drive | running; `vps-backup.timer` ran 2026-10-02 03:34; restore check passed 2026-10-02 (personal-vps `host/restore-check.sh`, #42) | done for v1 (rerun before acceptance) |

## Milestones

| # | Milestone | State | Done when |
|---|---|---|---|
| M1 | **Pilot running.** The Coordinator picks agent-doable items from Brian's personal weekly plan, agents build them, and decisions reach the terminal | in progress: pieces 1–3 done; blocked until agents can sign in to Claude again (Brian's token), then the Coordinator's first picks (BRI-13) | one pilot task is reviewed through `decisions.py` |
| M2 | **Governance on everywhere.** Jev gate observe mode in all of Brian's repositories for Claude and Codex, then guard mode after a log review; hive-brain settings as an AES config file | fully_specifiable_now | guard mode on, with a week of log |
| M3 | **Learning loop slices 2–5,** plus coaching for Brian | slice 2 fully specifiable; 3–5 conditional on slice 2 counts | condition 3 |
| M4 | **Knowledge, identity, context.** Choose the knowledge layer; one brain per project; context freshness | in progress: chosen (landscape review 2026-10-02); first brain (AES) and freshness check built; pilot projects' brains next | each used by a pilot task |
| M5 | **Evaluation and observability.** Weekly readout; check that no control went silent | in progress: `scripts/hive/controls.py` built (silence check); weekly readout waits on pilot logs | condition 4 |
| M6 | **v1 acceptance.** All five conditions shown with evidence | conditional | — |

M1 runs first because pilot tasks run unattended in the background while
M2–M4 are built, and they produce the logs M3 and M5 need.

## Active slice: M1

**Visible result:** Brian sees, in his terminal, every Paperclip task waiting on
him, each with a recommendation. The Coordinator keeps a small queue of real
pilot tasks moving.

**Pieces:**
1. **`scripts/hive/decisions.py`.** It lists Paperclip tasks assigned to Brian
   (status not done), each with its title, link and last comment. It reaches
   the board API over `ssh personal-vps` and runs the request inside the
   container, because the board's hostname allowlist refuses other hosts.
2. **Coordinator instruction.** Twice a day at most, the Coordinator picks
   one agent-doable item from `weekly-plans/personal/THIS_WEEK.md` ("Agent-
   executable work" lines), with at most 2 pilot tasks open at once. It assigns
   the item to Research and Code Review. The PR is opened but not merged; a
   `Decision: merge …?` task goes to Brian with a recommendation. Nothing is
   sent outward.
3. **Clean-up of stale setup tasks:** BRI-4 (setup decisions, answered
   2026-10-02 with "approve all") and BRI-1 (onboarding, blocked).

**Check:** run `decisions.py`. A pilot task appears there as a `Decision:` with
a PR link. **Negative case:** a task assigned to an agent must not appear.

**Rollback:** delete the Coordinator instruction paragraph; the script is
read-only.

## Decisions and assumptions

| Choice | Disposition | Reason / evidence |
|---|---|---|
| AES canonical is the home of the whole hive brain | human_set | goal 2026-10-02 ("recommendations stand unless I say otherwise") |
| Solo plus one brain per project, no departments | human_set | same |
| The terminal is the dashboard for now | human_set | same; Brian 2026-10-02 "for now in tui" |
| Coaching for Brian is part of the learning loop | human_set | same |
| Where cross-project rules live: action rules in the Jev gate policy (all repositories); repository rules in each repository's own checks or AES target; cross-project working rules in one rulebook section here | human_set (as recommended) | same; recommended 2026-10-02 |
| The loop's fixed core is the four items in `../aes-learning-loop/DESIGN.md` | human_set (as recommended) | same |
| Pilot tasks are picked by the Coordinator from Brian's weekly plan, not by Claude | agent_decided_reversible | the hive-brain design gives planning to the orchestrator; it tests C-ORCH for real |
| Thin glue around off-the-shelf tools lives in `scripts/` (ungoverned); AES product logic goes through `aes plan` | agent_decided_reversible | speed. **Wrong when:** a script passes ~300 lines or holds logic that isn't tied to one tool; then it moves under `aes plan` |
| Failure families are not re-cut for v1 | agent_decided_reversible | issue #64. **Wrong when:** a weekly spot check finds fewer than 8 of 10 acceptable |
| The weekly plan (dated week of 2026-09-21) is still a fair source of pilot tasks | assumption | if Brian's priorities moved, the Coordinator picks stale work; Brian's review catches it |

## Evidence

| Claim | Evidence | Date |
|---|---|---|
| Paperclip running, three agents idle | `docker ps` on personal-vps (up 16 h); board API agents list | 2026-10-02 |
| Paperclip tasks | 12 total: 9 done, 1 todo (BRI-4), 1 backlog (BRI-2, Telegram), 1 blocked (BRI-1) | 2026-10-02 |
| Backups | `systemctl list-timers` shows `vps-backup.timer` last ran 2026-10-02 03:34 CEST | 2026-10-02 |
| Jev gate observing every Claude session | `~/.jev-gate/decisions.jsonl` has 2,334 entries: 1,489 allow, 841 ask, 4 deny, all mode `observe` | 2026-10-02 |
| Learning loop slice 1 | PR #66 merged `3bc351e`; 2,575 labelled, 0 errors | 2026-10-02 |

## Human decisions

No decisions open; all six design points were settled by the goal.

**Waiting on Brian (action, 2026-10-02):** create the agents' one-year Claude
token. In his own terminal (not a Claude session, so the token stays out of
transcripts): `ssh -t personal-vps sudo /srv/apps/paperclip/set-claude-token.sh`,
open the link, approve, paste the code, then paste the printed `sk-ant-oat01-…`
token at the hidden prompt. It ends with PASSED or FAILED.

## Progress log

- **2026-10-02:**
  - `scripts/hive/decisions.py` written and run. It listed BRI-4 (waiting on
    Brian) and BRI-1 (blocked), and correctly left out tasks assigned to
    agents.
  - BRI-1 and BRI-4 were closed as stale, each with a comment.
  - A "Pilot work" section was added to the Coordinator's instructions through
    the board API; the backup is `AGENTS.md.bak-20261002-pilot` beside the
    file in the container.
  - Kickoff task BRI-13 was assigned to the Coordinator.
  - **Every agent run failed** from 20:30 UTC with "ACP agent reported a
    terminal access failure" (0 tokens); health check BRI-14 showed Research
    and Code Review failing too. Nothing showed it for 16 hours. Cause, read in
    Paperclip's code and confirmed by open upstream issues
    paperclipai/paperclip#13725 and #14182: the "My Claude subscription"
    connection stores only Claude's access token, which expires about 8 hours
    after sign-in and is never refreshed. "terminal access" means a final
    sign-in failure, not a shell. No upstream fix is merged (#13726, #14698,
    #14027 open), so upgrading does not help.
  - Fix (personal-vps PR #40): company secret `CLAUDE_CODE_OAUTH_TOKEN` bound
    to all three agents; their `aiConnection` binding removed in the database
    (this version cannot unbind through the API; old rows in
    `/root/paperclip-agents-backup-20261002-claude-token.json`);
    `set-claude-token.sh` lets Brian set the one-year token. The secret holds a
    placeholder until he runs it.
  - `decisions.py` now prints "Agents not working" first and exits 1 when any
    agent's latest run failed, so a dead fleet shows up the next time it runs.
  - The local AES checkout was realigned to `origin/main` (`0 0`); its stray
    merge commit is kept on `origin/wip/main-merge-20261002`.
  - Jev policy (agent-skills #422): merging Brian's own PRs moved to allow; the
    secrets-file rule fires only on direct reads. Replaying the whole log, wrong
    blocks fell from 4 to 2. In guard mode only "deny" blocks; "ask" falls back
    to Claude's own prompt, so ask-before-merge never blocked.
  - Learning loop slice 2: `label_items.py issues` labelled #64, #71–#73; a
    weekly timer on personal-vps (personal-vps #41) posts summaries to #74.
  - M4: landscape review chose per-repo `.project-brain/` folders; AES brain
    seeded; `brain_fresh.py` built and tested (theory-forge `HANDOFF.md` stale,
    exit 1).
  - Codex runs the Jev hook: a Codex session ran
    `gh api -X DELETE repos/o-nonexistent/...` at 22:53:09 UTC (CC Safety Net
    log, `agent: codex`, no Claude session ran it), and Jev logged that exact
    command in the same second. Jev's log has no client field; the Safety Net
    log does, so match commands across the two.
  - Restore check: the 2026-10-02 Drive backup restored into a throwaway
    Postgres 18 (1 company, 3 agents, 4 issues, Coordinator row present).
  - `scripts/hive/controls.py` (condition 4): last activity of each control
    against its normal gap; exit 1 on SILENT/FAILING/STALE. First run: Paperclip
    FAILING (expected, login), everything else ok. A fake 8-day-old Jev log
    showed SILENT.

## Exact next action

0. Once Brian's `set-claude-token.sh` prints PASSED: check that
   `python3 scripts/hive/decisions.py` shows "Agents not working: 0" after the
   next runs. Wake BRI-14 (health check) by commenting on it and confirm a
   `succeeded` run in `/api/companies/<C>/heartbeat-runs`.
1. Run `python3 scripts/hive/decisions.py` and read BRI-13's comments.
   Before a pilot task starts on a project, seed that repo's `.project-brain/`
   (copy AES's four files as the pattern) and add the read-first line to its
   `CLAUDE.md`/`AGENTS.md`.
   Expected: the Coordinator has named one or two `Pilot:` tasks assigned to
   Research and Code Review. If it has not acted within a few hours, look at
   its run log on the board.
2. Meanwhile, M2 toward guard mode. Done 2026-10-02: Jev gate in observe
   mode in every Claude session through agent-skills' hook manifest
   (agent-skills #417); personal-vps's project-only copy is gone. Still open:
   - Done 2026-10-02: Codex confirmed (Progress log); merge rule and
     secrets-file rule fixed (agent-skills #422).
   - Review a week of the log (from 2026-10-02), then switch to guard mode
     (`jev-gate-hook --mode guard`; only "deny" blocks). Check the replay
     first: `deny` rows in `~/.jev-gate/decisions.jsonl` must all be right.
3. Run `python3 scripts/hive/controls.py` at each stop; it must exit 0 for a
   week before condition 4 can be claimed.

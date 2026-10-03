# Hive brain v1: living plan

**Authority:** Brian's goal of 2026-10-02 (quoted under "Outcome"). This repository is the home.
**Planning method:** Company Planning, durable one-human plan (`durable_solo`). Product code under the governed roots still goes through `aes plan`.
**Who reads this:**
- any agent or session that picks up the work;
- Brian, for "where are we against v1".

**Stage:** personal pilot (Brian plus agents), not a team product.
**Last outcome-bearing update:** 2026-10-03 (UTC).
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

## Capabilities

The 10 capability ids come from the AI Astronauts hive-brain roadmap
(`PL.roadmap.capabilities` in the hive-brain explainer, 2026-10-01).

| Capability | Chosen tool | State 2026-10-02 | v1 evidence still needed |
|---|---|---|---|
| C-ORCH orchestration | Paperclip on personal-vps | running, but every agent run has failed since 2026-10-02 20:30 UTC (expired Claude login, see Progress log); fix waits on Brian's token | agents run again; it drove the three pilot tasks |
| C-MSG agent messaging | Paperclip task threads | in use (BRI-5 → BRI-8 handoff) | the same, on pilot tasks |
| C-HUMAN-IF human interface | terminal relay of Paperclip `Decision:` tasks; dashboard later | `python3 scripts/hive/decisions.py` lists agents not working (exit 1), then every task waiting on Brian or blocked; first run 2026-10-02 found 2 stale setup tasks (closed) | pilot reviews done through it |
| C-IDENTITY identity | one brain per project: `.project-brain/` in each repo (agent-skills `project-brain.md` layout), read first via the repo's `CLAUDE.md`/`AGENTS.md` | brains in AES (2026-10-02), theory-forge (#22) and cybernetic_influence_v3 (#43), 2026-10-03; each records its docs' conflicts as `needs_resolution` (e.g. theory-forge README says 5 theories compiled, AGENTS.md says 39; cybernetic_influence_v3 AGENTS.md says CI gates every merge, but GitHub Actions has been off since 2026-09-14) | each pilot project has a project brain agents read |
| C-KNOW knowledge | git: each repo's `.project-brain/`; one task's plan in Paperclip issue documents (chosen 2026-10-02 after a landscape review; gbrain, Hermes, mem0/Letta/Cognee rejected for v1, reasons in `.project-brain/truth.md`) | chosen; AES brain committed | used by a pilot task |
| C-CONTEXT context freshness | Paperclip re-reads agent and project settings each run (its `DEVELOPING.md`, "Config Freshness"); `scripts/hive/brain_fresh.py` for stale brains and checkouts behind GitHub | checker built; caught theory-forge `HANDOFF.md` (183 days, 209 commits since, exit 1) | run before pilot tasks; a stale case caught on a pilot project |
| C-GOV governance | Jev gate + CC Safety Net + hive-brain settings as AES config | CC Safety Net on for Claude and Codex; Jev gate in observe mode in every Claude and Codex session (Codex confirmed 2026-10-02); rule K1 enforced 2026-10-03; settings in `scripts/hive/settings.json`, checked against the live system by `settings_check.py` (22 of 22 match, 2026-10-03; part of `controls.py`) | Jev gate in guard mode across projects; settings file; a block shows up in the log |
| C-LEARN learning | AES learning loop (GitHub issues + Jev labels) | slice 1 done: 2,575 legacy learnings labelled (PR #66); first lesson filed (issue #64) | condition 3 |
| C-EVAL evaluation | readout from logs and traces: `python3 scripts/hive/readout.py [--days N]` (Paperclip tasks, pilot tasks, runs and failure codes; Jev and Safety Net decisions; learning-loop items by family; controls) | built 2026-10-03; first run showed the outage (13 failed runs, all `acpx_turn_failed`) | a weekly readout over pilot tasks |
| C-RUNTIME runtime | netcup personal-vps, nightly backups to Drive | running; `vps-backup.timer` ran 2026-10-02 03:34; restore check passed 2026-10-02 (personal-vps `host/restore-check.sh`, #42) | done for v1 (rerun before acceptance) |

## Milestones

| # | Milestone | State | Done when |
|---|---|---|---|
| M1 | **Pilot running.** The Coordinator picks agent-doable items from Brian's personal weekly plan, agents build them, and decisions reach the terminal | in progress: pieces 1–3 done; blocked until agents can sign in to Claude again (Brian's token), then the Coordinator's first picks (BRI-13) | one pilot task is reviewed through `decisions.py` |
| M2 | **Governance on everywhere.** Jev gate observe mode in all of Brian's repositories for Claude and Codex, then guard mode after a log review; hive-brain settings as an AES config file (`scripts/hive/settings.json`: agents, heartbeats and caps, gate mode, timers) | in progress: observe mode on everywhere (2026-10-02); rule K1 enforced and settings file with a live check done (2026-10-03); guard mode waits on the wrong-deny fix (AES #73) and the log review until 2026-10-09 | guard mode on, with a week of log |
| M3 | **Learning loop slices 2–5,** plus coaching for Brian | slice 2 fully specifiable; 3–5 conditional on slice 2 counts | condition 3 |
| M4 | **Knowledge, identity, context.** Choose the knowledge layer; one brain per project; context freshness | in progress: chosen (landscape review 2026-10-02); first brain (AES) and freshness check built; pilot projects' brains next | each used by a pilot task |
| M5 | **Evaluation and observability.** Weekly readout; check that no control went silent | in progress: `controls.py` (silence check) and `readout.py` (weekly readout) built; both wait on pilot logs | condition 4 |
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
| The loop's fixed core is the four items in `proposals/aes-learning-loop/DESIGN.md` | human_set (as recommended) | same |
| Pilot tasks are picked by the Coordinator from Brian's weekly plan, not by Claude | agent_decided_reversible | the hive-brain design gives planning to the orchestrator; it tests C-ORCH for real |
| Thin glue around off-the-shelf tools lives in `scripts/` (ungoverned); AES product logic goes through `aes plan` | agent_decided_reversible | speed. **Wrong when:** a script passes ~300 lines or holds logic that isn't tied to one tool; then it moves under `aes plan` |
| Failure families are not re-cut for v1 | agent_decided_reversible | issue #64. **Wrong when:** a weekly spot check finds fewer than 8 of 10 acceptable |
| The weekly plan (dated week of 2026-09-21) is still a fair source of pilot tasks | assumption | if Brian's priorities moved, the Coordinator picks stale work; Brian's review catches it |

## Evidence

| Claim | Evidence | Date |
|---|---|---|
| Paperclip running; Coordinator and Research and Code Review fail every run (login); Brian Contact runs only when woken and has not run since 04:13 on 2026-10-02, so it has not failed yet but would | `python3 scripts/hive/decisions.py` ("Agents not working: 2 of 3") | 2026-10-03 |
| Paperclip tasks | 15 total: BRI-13 (pilot kickoff) and BRI-14 (health check) in progress, BRI-15 (Brian: token) todo, BRI-2 backlog, the rest done | `scripts/hive/board.sh GET /api/companies/$C/issues` | 2026-10-03 |
| Backups | `systemctl list-timers` shows `vps-backup.timer` last ran 2026-10-02 03:34 CEST | 2026-10-02 |
| Jev gate observing every Claude and Codex session | `python3 scripts/hive/readout.py`: about 3,500 decisions by 2026-10-03, all mode `observe`; 9 deny (hard rules), 0 rule K1 blocks (K1 not installed) | 2026-10-03 |
| Learning loop slice 1 | PR #66 merged `3bc351e`; 2,575 labelled, 0 errors | 2026-10-02 |

## Human decisions

None open. Rule K1 was accepted 2026-10-03. All six design points were settled by the goal.

**Waiting on Brian (action, 2026-10-02; Paperclip task BRI-15):** create the agents' one-year Claude
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

- **2026-10-03:**
  - Brian ran `set-claude-token.sh` twice; both good tokens were refused because
    Claude's sign-in screen leaves the terminal wrapping pastes in invisible
    markers. Fixed (personal-vps #43). The two tokens were pasted into a chat,
    so they are treated as exposed and not used.
  - A session ended because it removed the worktree it stood in (AES #78,
    family K, the second time). Rule K1 proposed with a replay: 54 logged
    removals, 1 block, the real one (agent-skills PR #424, held for Brian).
  - `scripts/hive/readout.py` (C-EVAL) and `scripts/hive/board.sh` built;
    theory-forge brain seeded (theory-forge #22).
  - Cold pick-up test (condition 5): a fresh agent given only this file got the
    state, blocker and checks right, verdict "partly"; it lacked board commands
    and ids, and the Evidence table was stale. Fixed in this revision; the
    Brian action is now Paperclip task BRI-15, so `decisions.py` shows it.
  - **Agents work again** (15:22 UTC): Brian's `set-claude-token.sh` run saved
    the token (secret v5). The script printed FAILED only because Paperclip
    skipped its sign-in probe (wording fixed, personal-vps #44). Proof: health
    check BRI-14 ran at 15:23 and replied ok; the Coordinator ran at 15:24.
    BRI-14 and BRI-15 closed. The token was pasted into the chat, so Brian was
    asked to rerun the script once without pasting its output.
  - Pilot kickoff: the Coordinator has no GitHub token, so it asked Research
    and Code Review to read the weekly plan (BRI-16) and blocked BRI-13 on it.
    It names one pilot task per 12 hours (its own cap). Its question "should I
    get GitHub access?" was answered no for now: the only token can write to
    every repo.
  - **Rule K1 accepted and enforced** (Brian, in the terminal): the first rule
    to go the whole way from a recurring failure (family K, AES #78) to a
    proposal with a replay (1 block in 54) to Brian's yes to enforcement. A
    simulated removal of the session's own worktree was blocked live and
    logged; a removal from outside the worktree was allowed.
  - Condition 4 clock started: first all-clean `controls.py` run (8 of 8 ok) at
    15:29 UTC. Every run now appends to `~/.hive-brain/controls.jsonl`, and a
    daily user timer runs it (`scripts/hive/systemd/`); `readout.py` counts the
    clean days.

## How to check and act

- **Board:** `scripts/hive/board.sh GET|POST <api-path>` runs a request on the
  Paperclip board over `ssh personal-vps` (ids are in the script's header).
  Company `C=da165590-b0b3-4bf9-bb7f-e455292df499`. Tasks: BRI-13 (pilot
  kickoff) `c8a83262-03e9-4b7a-b8fd-734cfe1d9b44`; BRI-14 (health check)
  `3b1cd68f-0d58-4699-bf6f-e38a79fe487a`; BRI-15 (Brian: token)
  `36109986-51a2-4276-b4f5-225758ed87cc`. Board in a browser:
  `https://paperclip.brianmills.dev/BRI/issues/<BRI-n>`.
- **Terminal relay:** `python3 scripts/hive/decisions.py` (agents not working,
  then tasks waiting on Brian; exit 1 while an agent is broken).
- **Silence check:** `python3 scripts/hive/controls.py` (exit 0 = no control
  silent). **Weekly readout:** `python3 scripts/hive/readout.py`.
- **Brain freshness:** `python3 scripts/hive/brain_fresh.py <repo>`.
- **Rule K1** (accepted by Brian 2026-10-03, enforced): the Jev launcher
  blocks `git worktree remove` of the folder the session stands in (AES #78,
  agent-skills #424). Installed as `~/.local/bin/jev-gate-worktree-guard` and
  `~/.local/bin/jev-gate-hook`; blocks are `rule: K1-worktree-cwd` rows in
  `~/.jev-gate/decisions.jsonl`, counted by `readout.py`.

## Exact next action

0. Done 2026-10-03: token fixed, agents run (Progress log). To re-check any
   time: wake the health check with
   `echo '{"body":"Health check: reply ok."}' | scripts/hive/board.sh POST /api/issues/3b1cd68f-0d58-4699-bf6f-e38a79fe487a/comments`,
   then `scripts/hive/board.sh GET "/api/companies/$C/heartbeat-runs?agentId=4d008def-4e59-47c2-bccf-ec5313e12ce2&limit=3"`
   shows `"status":"succeeded"`.
1. Optional, Brian: rerun `set-claude-token.sh` once without pasting its
   output anywhere, so the saved token never appeared in a chat.
2. **Pilot:** BRI-16 (Research and Code Review reads the weekly plan,
   id `b8f04463-8fe7-43d0-9c51-86b336c829d2`) unblocks BRI-13. Read the Coordinator's picks:
   `scripts/hive/board.sh GET /api/issues/c8a83262-03e9-4b7a-b8fd-734cfe1d9b44/comments`.
   Expected: one or two `Pilot:` tasks assigned to Research and Code Review.
   If none within a few hours, wake BRI-13 with a comment the same way and
   read the Coordinator's latest run (heartbeat-runs with
   `agentId=8964a584-ddfe-4fb1-b14f-c1503ae5ec23`). Before a pilot task starts
   on a project, make sure that repo has `.project-brain/` (done: AES,
   theory-forge; portfolio waits for another session's claim to clear) and a
   read-first line where Claude Code reads it: `CLAUDE.md`. theory-forge has
   only `AGENTS.md`, so check in the first theory-forge run log that the brain
   was read. The weekly plan the Coordinator picks from is dated the week of
   2026-09-21; if its picks look stale, say so in the review.
3. **Condition 3:** K1 is proposed, accepted, enforced, and its log shows a
   live-test block. Still needed: a block in real work (watch K1 rows in
   `readout.py`) and one wrong block coming back as a `kind:friction`,
   `source:gate` issue. The 8 wrong Jev denies (AES #72, #73) are gate
   frictions already, but from the pre-existing secret rules, not K1.
4. **M2:** review the Jev log until 2026-10-09 (every `deny` row must be
   right), then switch to guard mode (`jev-gate-hook --mode guard`; only
   "deny" blocks). **Not safe yet (2026-10-03):** of 9 `deny` rows, 1 is right
   (WSL shutdown) and 8 are text-matching rules firing on heredoc or PR/issue
   text that only mentions a forbidden command (AES #72, #73). Fix that first:
   either the rules stop matching text inside heredocs and messages, or Jev's
   base `env … | curl` rule is changed upstream (posting there needs Brian's
   yes).
5. `controls.py` runs daily (user timer) and at each stop; condition 4 can be
   claimed when `python3 scripts/hive/readout.py --days 7` shows 7 days with
   only clean runs (first clean day 2026-10-03).

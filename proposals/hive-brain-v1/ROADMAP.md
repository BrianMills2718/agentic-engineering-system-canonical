# Hive brain v1: living plan

**Authority:** Brian's goal of 2026-10-02 (quoted under "Outcome"). This repository is the home.
**Planning method:** Company Planning, durable one-human plan (`durable_solo`). Product code under the governed roots still goes through `aes plan`.
**Who reads this:**
- any agent or session that picks up the work;
- Brian, for "where are we against v1".

**Stage:** personal pilot (Brian plus agents), not a team product.
**Last outcome-bearing update:** 2026-10-03 22:50 UTC. **Live status beats this
file:** for current numbers run `python3 scripts/hive/readout.py` and read
`scripts/hive/conditions.json`; prose here can lag the board.
- Pilot tasks 1 and 2 of 3 merged: AES PR #88 and personal-wiki PR #13 (BRI-21,
  a stale-page checker, merged by the agent at 21:55 UTC under Brian's rule).
- Review rule changed by Brian at 21:45 UTC: agents merge their own pilot
  PRs; he is asked only for public-facing or irreversible changes.
- Agents sign in again since 15:22 UTC (one-year token); project brains in
  four repositories; 11 of 11 controls clean.

## Outcome

**Brian's goal, 2026-10-02:** get his personal hive brain to v1, with AES
canonical as its home. His AI Astronauts hive-brain design is the vision,
scaled to him, his agents, and one brain per project. It is built from
off-the-shelf tools wherever they exist, as a speedrun, with benchmarks only
when a specific decision needs one.

**Brian, 2026-10-03 (changes the review step):** "i dont even want to answer
merge for anything that isnt public facing and that is not irreversible." So
agents merge their own pilot pull requests once the repository's checks pass
(its own local checks, `make check` or the equivalent; no hosted CI, Brian 2026-10-03; a
new checker that reports findings by exiting 1 is not a failing check)
and leave a report on the task; Brian is asked first only when a change is
public-facing (a live site, a published package, anything visible outside his
own machines and private repositories) or irreversible (deletes data or
history, deploys, migrates a database, sends anything outward). He also asked
for plain language, so this file says what each name means where it can.

**v1 is done when all five are true, each shown by a command's output or a link:**

1. **Pilot.** At least three real tasks from at least two of Brian's projects
   each went from the weekly plan to a merged pull request without
   hand-holding: the Coordinator plans it, agents build it unattended, the
   repository's checks pass, the agents merge it and leave a report Brian can
   read. Brian is asked first only for a public-facing or irreversible change
   (his rule of 2026-10-03). Task 1 was merged on his yes before that rule.
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

## Capabilities

The first 10 capability ids come from the AI Astronauts hive-brain roadmap
(`PL.roadmap.capabilities` in the hive-brain explainer, 2026-10-01). C-ROUTE (model routing) was added to v1 by Brian on 2026-10-03 ("yes i
want model routing in v1").

| Capability | Chosen tool | State (latest dated entry wins) | v1 evidence still needed |
|---|---|---|---|
| C-ORCH orchestration | Paperclip on personal-vps | running again since 2026-10-03 15:22 UTC (one-year token); drove pilot task 1 (BRI-17 → AES PR #88); pilot floor one task per 6 hours, 2 open at once | it drives pilot tasks 2 and 3 |
| C-MSG agent messaging | Paperclip task threads | in use (BRI-5 → BRI-8 handoff) | the same, on pilot tasks |
| C-HUMAN-IF human interface | terminal relay of Paperclip `Decision:` tasks; dashboard later | `python3 scripts/hive/decisions.py` lists agents not working (exit 1), then every task waiting on Brian or blocked; pilot 1's merge decision (BRI-19) went through it 2026-10-03. Since Brian's 2026-10-03 rule it is normally empty: private, reversible pilot PRs merge without him | it shows a `Decision:` only for a public-facing or irreversible change; what merged is readable in the pilot task's comments |
| C-IDENTITY identity | one brain per project: `.project-brain/` in each repo (agent-skills `project-brain.md` layout), read first via the repo's `CLAUDE.md`/`AGENTS.md` | brains in AES (2026-10-02), theory-forge (#22), cybernetic_influence_v3 (#43) and personal-wiki (#12, with a two-line `CLAUDE.md` pointer because the VPS agents' Claude Code loads only `CLAUDE.md`), 2026-10-03; each records its docs' conflicts as `needs_resolution` (e.g. theory-forge README says 5 theories compiled, AGENTS.md says 39; cybernetic_influence_v3 AGENTS.md says CI gates every merge, but GitHub Actions has been off since 2026-09-14) | each pilot project has a project brain agents read |
| C-KNOW knowledge | git: each repo's `.project-brain/`; one task's plan in Paperclip issue documents (chosen 2026-10-02 after a landscape review; gbrain, Hermes, mem0/Letta/Cognee rejected for v1, reasons in `.project-brain/truth.md`) | chosen; AES brain committed | used by a pilot task |
| C-CONTEXT context freshness | Paperclip re-reads agent and project settings each run (its `DEVELOPING.md`, "Config Freshness"); `scripts/hive/brain_fresh.py` for stale brains and checkouts behind GitHub | checker built; caught theory-forge `HANDOFF.md` (183 days, 209 commits since, exit 1); `controls.py` runs it daily for every `~/code` repo with a brain (4 on 2026-10-03) | run before pilot tasks; a stale case caught on a pilot project |
| C-GOV governance | Jev gate + CC Safety Net + hive-brain settings as AES config | CC Safety Net on for Claude and Codex; Jev gate in observe mode in every Claude and Codex session (Codex confirmed 2026-10-02); rule K1 enforced 2026-10-03; settings in `scripts/hive/settings.json`, checked against the live system by `settings_check.py` (22 of 22 match, 2026-10-03; part of `controls.py`) | Jev gate in guard mode across projects; settings file; a block shows up in the log |
| C-LEARN learning | AES learning loop (GitHub issues + Jev labels) | slice 1 done: 2,575 legacy learnings labelled (PR #66); first lesson filed (issue #64) | condition 3 |
| C-EVAL evaluation | readout from logs and traces: `python3 scripts/hive/readout.py [--days N]` (Paperclip tasks, pilot tasks, runs and failure codes; Jev and Safety Net decisions; learning-loop items by family; controls) | built 2026-10-03; first run showed the outage (13 failed runs, all `acpx_turn_failed`) | a weekly readout over pilot tasks |
| C-RUNTIME runtime | netcup personal-vps, nightly backups to Drive | running; `vps-backup.timer` ran 2026-10-02 03:34; restore check passed 2026-10-02 (personal-vps `host/restore-check.sh`, #42) | done for v1 (rerun before acceptance) |
| C-ROUTE model routing (throughput and cost) | Paperclip's own per-agent model and per-task model override (landscape review 2026-10-03: per-prompt routers such as OpenRouter Auto, RouteLLM, NotDiamond and the new `typesafe/jev-router` don't yet handle long tool-using agent sessions); a Codex builder agent on the ChatGPT subscription next | Coordinator on `claude-sonnet-5`, builder on `claude-opus-5` (2026-10-03, checked by `settings_check.py`); cost per run is in Paperclip's run records | a pilot task run under the routed setup, with cost and throughput per task in `readout.py` |

## Milestones

| # | Milestone | State | Done when |
|---|---|---|---|
| M1 | **Pilot running.** The Coordinator picks agent-doable items from Brian's personal weekly plan, agents build them, and decisions reach the terminal | done 2026-10-03: pilot task 1 (BRI-17) was reviewed through `decisions.py` (BRI-19) and merged as AES PR #88; the queue continues for pilots 2 and 3 | one pilot task is reviewed through `decisions.py` |
| M2 | **Governance on everywhere.** Jev gate observe mode in all of Brian's repositories for Claude and Codex, then guard mode after a log review; hive-brain settings as an AES config file (`scripts/hive/settings.json`: agents, heartbeats and caps, gate mode, timers) | in progress: observe mode on everywhere (2026-10-02); rule K1 enforced and settings file with a live check done (2026-10-03); guard mode waits on the wrong-deny fix (AES #73) and the log review until 2026-10-09 | guard mode on, with a week of log |
| M3 | **Learning loop slices 2–5,** plus coaching for Brian | slice 2 fully specifiable; 3–5 conditional on slice 2 counts | condition 3 |
| M4 | **Knowledge, identity, context.** Choose the knowledge layer; one brain per project; context freshness | in progress: chosen (landscape review 2026-10-02); brains in AES, theory-forge, cybernetic_influence_v3 and personal-wiki; freshness checked daily by `controls.py`; pilot 2 is the first task told to read and update a brain | each used by a pilot task |
| M5 | **Evaluation and observability.** Weekly readout; check that no control went silent | in progress: `controls.py` (silence check) and `readout.py` (weekly readout) built; both wait on pilot logs | condition 4 |
| M6 | **Model routing.** Per-agent models (done 2026-10-03), a Codex builder agent on the ChatGPT subscription, per-task overrides, cost and throughput per task in the readout, then more parallel runs once a week of logs shows no subscription caps hit | in progress | C-ROUTE row |
| M7 | **v1 acceptance.** All five conditions shown with evidence | conditional | — |

M1 runs first because pilot tasks run unattended in the background while
M2–M4 are built, and they produce the logs M3 and M5 need.

## Active slice: M1

**Visible result:** real items from Brian's weekly plan get built and merged by
the agents, each with a report on its task; his terminal shows only what needs
him (normally nothing, since 2026-10-03). The Coordinator keeps a small queue
of real pilot tasks moving.

**Pieces:**
1. **`scripts/hive/decisions.py`.** It lists Paperclip tasks assigned to Brian
   (status not done), each with its title, link and last comment. It reaches
   the board API over `ssh personal-vps` and runs the request inside the
   container, because the board's hostname allowlist refuses other hosts.
2. **Coordinator instruction.** At most one new pilot task every 6 hours
   (12 until 2026-10-03), the Coordinator picks one agent-doable item from
   `weekly-plans/personal/THIS_WEEK.md` ("Agent-executable work" lines), with
   at most 2 pilot tasks open at once. It assigns the item to Research and
   Code Review, who read the repo's `.project-brain/now.md` first. When the
   repository's checks pass they merge the PR with a merge commit and report
   on the task; a `Decision: merge …?` task goes to Brian only for a
   public-facing or irreversible change (2026-10-03). Nothing is sent outward.
3. **Clean-up of stale setup tasks:** BRI-4 (setup decisions, answered
   2026-10-02 with "approve all") and BRI-1 (onboarding, blocked).

**Check:** the pilot task's comments show the merged PR and the check output;
`decisions.py` shows a `Decision:` only for a public-facing or irreversible
change. **Negative case:** a task assigned to an agent must not appear there.

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
| Agents merge their own pilot PRs after the repository's checks; Brian is asked only for public-facing or irreversible changes | human_set | Brian, 2026-10-03 (quote under Outcome); replaces the 2026-10-02 "Decision: merge" step for private, reversible changes; Coordinator rule backup `AGENTS.md.bak-20261003-merge-rule` |
| Pilot cadence: at most one new pilot task every 6 hours (was 12), 2 open at once | agent_decided_reversible | 2026-10-03: pilot 1 took about 80 minutes from creation to merge, so a 12-hour floor would spend two days on a few hours of work; the 2-open cap already bounds Brian's review load. Old rule kept as `AGENTS.md.bak-20261003-cadence` beside the Coordinator's instructions. **Wrong when:** two `Decision:` tasks wait on Brian for more than a day, or he says reviews arrive too fast |
| Repositories with only `AGENTS.md` get a two-line `CLAUDE.md` that points to it and to the brain | agent_decided_reversible | 2026-10-03: the VPS agents' Claude Code (2.1.278, no `instructionFiles` setting) loads only `CLAUDE.md`; the local setting that also loads `AGENTS.md` is not there. **Wrong when:** a pilot run log on an `AGENTS.md`-only repo without the pointer shows the brain was read anyway |

## Evidence

| Claim | Evidence | Date |
|---|---|---|
| Paperclip running; all three agents' latest runs succeed | `python3 scripts/hive/decisions.py` ("Agents not working: 0 of 3", exit 0); run counts: `python3 scripts/hive/readout.py --days 7` (the failures are from the 2026-10-02/03 login outage) | live |
| Paperclip tasks | pilots: BRI-17 (1, done) and BRI-21 (2, done); BRI-13 (pilot kickoff) in progress; for counts run `scripts/hive/board.sh GET /api/companies/$C/issues` | live; pilots as of 2026-10-03 22:50 UTC |
| Coordinator re-reads its instructions each run | its comment at 17:53 UTC cites the 6-hour floor written into the file at 17:45 UTC | 2026-10-03 |
| Project brains fresh in 4 repositories; no control silent | `python3 scripts/hive/controls.py`: 11 of 11 ok, exit 0; `brain_fresh.py ~/code/personal-wiki --fetch` exit 0 | 2026-10-03 17:50 UTC |
| Backups | `systemctl list-timers` shows `vps-backup.timer` last ran 2026-10-02 03:34 CEST | 2026-10-02 |
| Jev gate observing every Claude and Codex session | `python3 scripts/hive/readout.py --days 7`: 7,033 decisions, all mode `observe`; 18 deny (hard rules); 1 rule K1 block (the live test) | 2026-10-03 17:40 UTC |
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

- **Pilot task 1 of 3 done (2026-10-03):** BRI-17 "make the public AES quickstart
    work from a clean clone" went plan → build → review → merge. The Coordinator
    picked it from the weekly plan; Research and Code Review built it (AES PR
    #88); the terminal review found `aes status` still failed from a fresh clone
    (exit 127), Brian approved "fix then merge", the agent fixed it, a fresh-clone
    retest passed (`.venv/bin/aes status` and `make aes` exit 0), merged
    `69846223`. Hand-holding: one scope question (BRI-18, the over-broad Inside
    Success rule, AES #87) answered by the terminal session.

- **2026-10-03, later (pilot 2 preparation):**
  - Pilot 2 target: the Coordinator first chose a `portfolio` citation pass,
    then withdrew it as a duplicate of V16.17 and chose `personal-wiki`
    (weekly plan Priority 5, "keep confidence labels current"). Scoping task
    BRI-20 (read-only) found all 274 typed pages labelled and all 963 inline
    markers well-formed; the real defect is currency (70 of 100 watched pages
    stale by the repo's own `watch`/`sources_checked` rule, 18 unverifiable
    because 14 watched repositories return 404), and the documented lint
    command exits 2 for a cold reader because the script lives outside the
    repo. It recommends "report, don't fix": a checker in `tools/` plus the
    corrected lint line. Its question card (which slice) waits on the
    Coordinator, not Brian.
  - `personal-wiki` brain seeded (personal-wiki PR #12): the four files, the
    read-first paragraph in `AGENTS.md`, and a two-line `CLAUDE.md` pointer.
    `brain_fresh.py` exit 0; `controls.py` now checks 11 controls (11 ok).
  - Coordinator rules changed (backup `AGENTS.md.bak-20261003-cadence`):
    pilot floor 12 hours → 6 hours; each pilot task tells the agent to read
    `.project-brain/now.md` first and update it in the same PR.
  - Facts posted on BRI-20 and BRI-13 (17:52 UTC): the lint script exists on
    Brian's machine (exit 0, 272 pages, 18 thin warnings, no confidence
    check); the 404s are probably the Inside Success repositories moved into
    `inside-success-mega` on 2026-10-02.
  - The Coordinator read the changed rules on its next run (17:52–17:54 UTC;
    its 17:53 comment cites the 6-hour floor, moves its monitor to 21:40 UTC
    and puts the brain clause in the pilot 2 spec) and answered BRI-20's
    slice question itself: report-only, three states, no page edits.
  - Ecosystem gap filed as project-meta #2346: the workspace instruction names
    `check_coordination_claims.py` without a path, and the copies in nine
    repos crash on import; the working one is
    `project-meta/scripts/meta/check_coordination_claims.py`.

- **2026-10-03, 21:41–21:50 UTC (pilot 2 running; review rule changed):**
  - Pilot task 2 created by the Coordinator at 21:41 UTC (BRI-21, "give
    personal-wiki a runnable confidence-currency check": a script that reports
    which wiki pages' sources have not been re-checked since the repos they
    watch changed, plus the lint line fixed so it works from a clean clone).
    Research and Code Review started building it at 21:41; the task tells it
    to read `.project-brain/now.md` first and update it in the same PR.
  - Brian, in the terminal: no merge questions for anything that is not
    public-facing or irreversible, and plain language. The Coordinator's merge
    bullet was rewritten (backup `AGENTS.md.bak-20261003-merge-rule`), both
    agents were told on BRI-21 and BRI-13 at 21:47 UTC, and the Outcome,
    condition 1, M1 and the decisions table here were changed to match.
    Recorded for every session in `~/projects/.claude/AGENTS.md`.
  - One Coordinator run failed at 19:40 UTC in 5 s with "terminal limit
    failure" (`acpx_turn_failed`); the next run at 20:11 succeeded. Probably
    the Claude usage limit shared with Brian's local sessions; watch for a
    repeat in `readout.py`.
  - Not done, dropped for now: `CLAUDE.md` pointers in theory-forge and
    cybernetic_influence_v3. theory-forge's claimed lane exists (worktree
    `worktrees/claude-md-pointer-20261003`, claim expires 2026-10-04 20:35 UTC,
    nothing committed); cybernetic_influence_v3's lane was denied because the
    claim tool cannot resolve the `github.com-personal` SSH alias (concern
    still to file), and its local branch `claude-md-pointer-20261003` holds the
    two-line file unpushed. Do this only if pilot 3 lands in one of those repos.

## How to check and act

- **Board:** `scripts/hive/board.sh GET|POST <api-path>` runs a request on the
  Paperclip board over `ssh personal-vps` (ids are in the script's header).
  Company `C=da165590-b0b3-4bf9-bb7f-e455292df499`. Tasks: BRI-13 (pilot
  kickoff) `c8a83262-03e9-4b7a-b8fd-734cfe1d9b44`; BRI-14 (health check)
  `3b1cd68f-0d58-4699-bf6f-e38a79fe487a`; BRI-15 (Brian: token)
  `36109986-51a2-4276-b4f5-225758ed87cc`; BRI-20 (pilot 2 scoping)
  `f1cb19d0-9a87-440a-9fc6-7b43c20e668c`. Board in a browser:
  `https://paperclip.brianmills.dev/BRI/issues/<BRI-n>`.
- **Dashboard (Brian's view, phone-friendly):** https://claude.ai/artifact/SvMbUicpBhWEQYR7xZi4qc,
  built by `python3 scripts/hive/dashboard.py --out <file.html>` and republished with
  the Artifact tool at each stop (it is a snapshot and shows when it was built).
  Progress on the five conditions lives in `scripts/hive/conditions.json`; update it
  with evidence whenever a condition moves. Design: Representation Router, use case
  `scripts/hive/dashboard-use-case.json`.
- **Coordinator rules:** `/paperclip/instances/default/companies/<C>/agents/8964a584-ddfe-4fb1-b14f-c1503ae5ec23/instructions/AGENTS.md`
  inside the `paperclip` container on personal-vps ("Pilot work" section).
  Edit it with a dated `.bak-` copy beside it; Paperclip re-reads it each run.
  Proof it was read: the Coordinator's next comment cites the new rule.
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

0. Agents run (since 2026-10-03 15:22 UTC). To re-check any time: wake the
   health check with
   `echo '{"body":"Health check: reply ok."}' | scripts/hive/board.sh POST /api/issues/3b1cd68f-0d58-4699-bf6f-e38a79fe487a/comments`,
   then `scripts/hive/board.sh GET "/api/companies/$C/heartbeat-runs?agentId=4d008def-4e59-47c2-bccf-ec5313e12ce2&limit=3"`
   shows `"status":"succeeded"`.
1. Optional, Brian: rerun `set-claude-token.sh` once without pasting its
   output anywhere, so the saved token never appeared in a chat.
2. **Pilot 2: done** 2026-10-03 (personal-wiki PR #13, merge commit `e320239`,
   merged by the agent; `.project-brain/now.md` updated in the same PR). Its
   follow-up BRI-23 (repo-name mapping) was answered by the terminal session:
   rewrite a watch entry only where both repositories share a root commit. Two
   Decision tasks (BRI-22, BRI-23) still reached Brian despite the merge rule;
   if that recurs, file a `kind:friction` issue.
3. **Pilot 3:** earliest 6 hours after pilot 2 was created (21:41 UTC), so
   about 03:41 UTC on 2026-10-04. The Coordinator
   picks the repo; before the task starts, make sure the repo has
   `.project-brain/` (done: AES, theory-forge, cybernetic_influence_v3,
   personal-wiki; portfolio waits for another session's claim to clear) and a
   `CLAUDE.md` read-first line. The weekly plan is dated the week of
   2026-09-21; say so in the review if the pick looks stale.
4. **Condition 3:** K1 is proposed, accepted, enforced, and its log shows a
   live-test block. Still needed: a block in real work (watch K1 rows in
   `readout.py`) and one wrong block coming back as a `kind:friction`,
   `source:gate` issue. The 8 wrong Jev denies (AES #72, #73) are gate
   frictions already, but from the pre-existing secret rules, not K1.
5. **M2:** review the Jev log until 2026-10-09 (every `deny` row must be
   right), then switch to guard mode (`jev-gate-hook --mode guard`; only
   "deny" blocks). **Not safe yet (2026-10-03):** of the `deny` rows, 1 is
   right (WSL shutdown) and the rest are text-matching rules firing on heredoc
   or PR/issue text that only mentions a forbidden command (AES #72, #73). Fix
   that first: either the rules stop matching text inside heredocs and
   messages, or Jev's base `env … | curl` rule is changed upstream (posting
   there needs Brian's yes; the exact text was shown to him by the earlier
   session and is not yet approved).
6. `controls.py` runs daily (user timer) and at each stop; condition 4 can be
   claimed when `python3 scripts/hive/readout.py --days 7` shows 7 days with
   only clean runs (first clean day 2026-10-03).

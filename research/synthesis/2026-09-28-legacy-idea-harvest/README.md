# Harvest: ideas from Brian's earlier agent-engineering systems

Status: research synthesis, non-normative. Written 2026-09-28 at Brian's request
("an in-depth investigation for ideas", not code reuse). This harvest adopts
nothing. As with the
[2026-09-26 Inside Success AES harvest](../2026-09-26-inside-success-aes-harvest.md),
an idea enters v0.2 only through the donor re-entry rule
(`proposals/aes-v0.2-greenfield/05-donor-reentry.md`) and `aes plan`, and only
when its trigger shows up on a real consumer.

This harvest extends the 2026-09-26 one, which covered only
`Inside-Success/agentic-engineering-system`. The six source files below are
deduplicated against it and cite its item numbers (as "IS-AES #n" or
"harvest item n") wherever they add to an idea it already lists.

| Source | Revision read | File | Ideas | Failure lessons |
| --- | --- | --- | --- | --- |
| `BrianMills2718/project-meta` (policy registry, concerns, decisions, audits) | `0dcc574` | [project-meta.md](project-meta.md) | 18 | 14 |
| `BrianMills2718/enforced-planning` (claims, lanes, gates, installer) | `9963dc4` | [enforced-planning.md](enforced-planning.md) | 15 | 13 |
| `ecosystem-ops`, `machine-coordination`, `openclaw` (supervisor, attention, repair loops) | see file | [ecosystem-ops.md](ecosystem-ops.md) | 15 | 10 |
| Hook systems and AGENTS.md/CLAUDE.md delivery (`agent-skills`, `.claude`, instruction-surfaces) | see file | [hooks-instructions.md](hooks-instructions.md) | 16 | 7 |
| `BrianMills2718/aes` (archived) | `804cc8b` | [aes-archived.md](aes-archived.md) | 17 | 8 |
| `BrianMills2718/company-planning` (whole plugin, beyond bounded-design) | `bfabe03` | [company-planning.md](company-planning.md) | 18 | 13 |

Each idea is marked **observed** (it ran on real use and the evidence is
retained), **tested** (tests or fixtures only) or **design** (written down, with
no evidence of behaviour). Each source investigator checked that the paths it
cites exist at the revision read. The parent session re-ran the load-bearing
counts noted under "How this was checked".

## What the six systems learned, across all of them

Nine lessons recur across the sources. They matter more than any single
mechanism, because v0.2 has not yet reached the stage where these systems
failed.

1. **Recording works; closing does not.** The learnings register holds 2,506
   entries with 4 resolutions. `policy_friction.md` has one resolution field
   across 678 entries. A repair loop made 9,114 runs and produced 5 actions, of
   which 2 closed. A wrong-when condition fired and nobody wrote the superseding
   decision. The ideas that address this share one shape: a signal belongs to a
   keyed item with an owner, and it closes only when a registered verifier
   passes on the merged revision (project-meta 1, 5; ecosystem-ops E7, E8;
   enforced-planning 14). The Inside Success AES's own loop (harvest item 15)
   never promoted anything. The failure-taxonomy loop did make 5 real changes,
   because it changes the taxonomy only when two independent cases show a
   missing category (hooks-instructions 15).
2. **Blocking without a way out becomes net-negative, and the owner switches
   everything off.** Brian turned off all 54 Claude hooks on 2026-09-18
   ("causing more problems than good"). The causes were a Stop gate that refused
   every turn over another session's work, a mailbox gate that blocked its own
   acknowledge command, and 17 separate "Admit …" allowlist patches. The fixes:
   - a gate must let its own recovery through;
   - controls must be shown to work together, not only one at a time;
   - measure the false-block rate on a frozen snapshot of real state before a
     gate may block;
   - a control that never decides anything is a retirement candidate.

   Sources: enforced-planning 6, 9; project-meta 3, 4; company-planning 13;
   hooks-instructions F2.
3. **The sanctioned route must cost less than the bypass.** `[Unplanned]`
   commits in Enforced Planning rose from 20 of 304 (July) to 129 of 364
   (August) to 274 of 445 (September); the parent re-ran this. Company
   Planning's proportional planning paths (idea 4) and its "change path when
   evidence changes" rule are the most developed answer. This matters directly
   for `aes plan prepare/validate/accept`.
4. **A proxy route is not the real route.** Examples:
   - The hook config said 39 Codex hooks and 17 ran.
   - Controls passed from the repository root and failed from the worktree
     route the project requires, where one run corrupted a checkout.
   - CI never passed once in 37 runs because a secret was never set.
   - Instruction files existed that no Codex session received (see "Live
     problems found" below; this was re-observed on 2026-09-28).

   The fix is always to ask the running client or run the mandated route
   (hooks-instructions 4, 6; project-meta 17; aes-archived 9).
5. **A person's decision has to be a durable record that repairers and
   generators read.** A self-repair re-enabled all 54 hooks because nothing
   machine-readable recorded that Brian had turned them off. The supervisor
   re-asked a deletion Brian had already approved. The fixes are
   `disabled_clients` records, decisions identified by the hash of their exact
   scope that can only move forward, and directives that keep the person's
   exact words (hooks-instructions 1; project-meta 18; ecosystem-ops E1, E2).
6. **The first version of every honesty mechanism reproduced the failure it
   was meant to prevent.** Examples:
   - A scope audit reported clean without running.
   - A HEAD stamp was always one commit stale.
   - A "no push noise" check closed as green because the sender was dead.
   - Alerting only on state changes hid 43 persistent failures.

   The fixes: "all clear" needs proof the watched thing is alive, pair every
   negative control with a positive one, and keep "audited, found nothing"
   separate from "never audited" (ecosystem-ops E5, E7; aes-archived 3, 11).
7. **Evidence stores must be readable at the scale they are written.** Hook
   receipts reached 12 GB in about 2.1 million files, and four control triggers
   report `unknown` because they cannot be scanned. A store of 1,692 YAML files
   caused 5–9 s hook latency. The fix is to read hot-path data from a derived
   projection bound to a digest of its inputs, and to treat latency as a
   promotion criterion (project-meta lesson 3; enforced-planning 7).
8. **Some facts are visible only in aggregate.** `dodaf` had 38.9% of its lines
   unreachable from the product entry point while every local check passed.
   v0.2's topology check asks only whether each file is claimed, not whether it
   is reachable from the product. One caution: counting tests as entry points
   made every tested module "reachable" (project-meta 9; enforced-planning 12
   and lesson 12).
9. **The always-loaded instruction file grows back after every cut.** The
   workspace root instruction file was cut from 35 KB to 10.5 KB on 09-10 and
   was back at 32.6 KB by 09-26. Generated `AGENTS.md` files silently dropped
   whole sections, which pushed the fleet to one hand-written file. Keeping the
   trigger in the file and the rationale elsewhere helped, but did not hold
   without a gate. This argues against harvest item 14 (a generated instruction
   surface) unless it has a delivery probe (hooks-instructions 8, 10, F3, F6).

## Strongest candidates for v0.2, by the gap they fill

These are ordered by how directly each one fills a gap v0.2 declares. Each
source file has the full trigger and its evidence.

| v0.2 gap | Idea | Source | Status |
| --- | --- | --- | --- |
| No execution | An execution position record whose transitions a machine decides: exactly one of continue, repair, switch, complete, needs-human or circuit-break | company-planning 1 | observed (14 records); circuit breaker tested only |
| No execution | A continuation lease tied to real progress: two increments with no outcome deny the next write and offer the allowed moves | enforced-planning 1 | tested; wired observe-only |
| No execution | Review-ready only when an independent verifier passes every frozen criterion on one exact artifact digest, and rejected digests never return | enforced-planning 2 | tested on a real rejected dashboard |
| No policy recovery | A gate must let its own recovery through; measure false blocks before blocking; watch the decision rate as the health signal | enforced-planning 6, 9; project-meta 4 | observed |
| Target records | Each decision carries machine-checked wrong-when conditions, and one of them firing opens a keyed concern with an owner | project-meta 1 | observed (#1979) |
| Target records | Every drafted part carries a disposition (human_set, agent_decided_reversible, assumption or human_required), and "Still unresolved" is always shown | company-planning 6 | observed (PR #191) |
| Target records | Record where each success criterion came from; a control needed only for promotion gets an activation trigger | company-planning 9 | design |
| Characterization | The author proposes a conformance claim; a separate event accepts it | project-meta 12 | design |
| Characterization | Every scan reports what it missed, with a third result for "no checker exists" | project-meta 11; aes-archived 1–3 | observed (aes-archived) |
| Topology | Reachability from the product entry point, not only whether a file is claimed | project-meta 9; enforced-planning 12 | observed (`dodaf`) |
| Topology | A claim census: a derived view may not quietly lose a claim without a recorded disposition | aes-archived 4 | observed |
| Planning | Proportional planning paths, with a report of supporting-artifact volume against the product change | company-planning 4 | tested |
| Hook lifecycle | A deliberate "turned off" state (who, when, why, the person's words, how to restore) that repair reads | hooks-instructions 1 | observed |
| Hook lifecycle | Ask the client which hooks actually run; do not read the config file | hooks-instructions 4 | observed |
| Instruction delivery | A fresh-session recall probe per client, after every change to instruction delivery | hooks-instructions 6; project-meta 17 | observed |
| Learning loop | Screen a lesson for whether it constrains code before making it a check; recording and gating are one motion | aes-archived 6, 7 | observed 1 of 3 / design |
| Alerting | "Loud" means a person hears it; two channels (health changes, watchdog death); a delivery state ladder of queued, delivered, observed, responded | ecosystem-ops E4–E6 | observed |

## Live problems found during this harvest (2026-09-28)

The investigation surfaced four live defects. The parent session verified each
one directly before acting.

1. **Codex sessions inside repositories never received the workspace
   instructions.** Codex's default `project_root_markers = [".git"]` stops
   instruction discovery at the repository root, so `~/code/AGENTS.md` (Brian's
   workspace rules) never loaded in a repo session. Checked with real
   `codex exec` sessions: inside `whygame5` the repo `AGENTS.md` arrived and the
   workspace rules did not; run from `~/code`, the workspace rules arrived.
   **Fixed:** added `project_root_markers = [".codex-workspace-root"]`,
   `project_doc_max_bytes = 131072` and a marker file at `~/.codex-workspace-root`.
   Re-checked with no overrides: in `whygame5`, both the workspace rules and the
   repo's last sentence arrived. In `hermes-agent`, the largest repo file at
   75 KB, both the workspace rules and a phrase from the file's last paragraph
   arrived; that session used about 38k tokens against about 14k before the
   fix. Consequence:
   `project-meta/scripts/check_instruction_payload_size.py` models a 32,768-byte
   combined budget, and that model no longer matches the configuration.
2. **Phone alerts failed from 2026-09-18.** `deliver_ntfy` crashed on any title
   containing a non-Latin-1 character, such as the "…" added when a title is
   truncated. **Fixed** in the shared sender (project-meta #2192). The new test
   fails on the old code, and a real alert was confirmed at the broker.
3. **Every hook-path commit to project-meta was frozen.** A cross-repository
   relative symlink broke the pre-commit render in every linked worktree. The
   hook also counted its own re-rendered, auto-staged file as the author's
   change, which turned on the 72-hour strict-freshness rule for every commit.
   This is the 2026-09-06 deadlock again. **Fixed** in project-meta #2192.
4. **The project-meta `current_execution` verification is past its 72-hour
   limit.** It is still open. It now blocks only commits that touch the
   authority surfaces.

## How this was checked

- Six read-only investigators, one per source, each checked that its cited
  paths exist at the revision it read.
- The parent session re-ran these load-bearing claims:
  - the `[Unplanned]` share of Enforced Planning's commits (July 20/304,
    August 129/364, September 274/445 on `origin/main`);
  - 0 of 260 policy-registry rows with `budget` or `retire_when` filled;
  - 60 attention-push crashes (`UnicodeEncodeError`) in the journal on
    2026-09-27;
  - the Codex instruction-delivery behaviour, in real sessions.
- The remaining statuses and counts are the investigators' readings of the
  retained evidence. They were not re-run here.

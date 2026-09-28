# Harvest: ideas from ecosystem-ops, openclaw, machine-coordination

Read-only idea harvest for AES v0.2, written 2026-09-28. Nothing here is adopted by being listed.
Does not repeat `research/synthesis/2026-09-26-inside-success-aes-harvest.md`; where an item
here is a stronger version of one of its items, that item's number is given as "cf. #N".

| Repo | HEAD | State at read |
| --- | --- | --- |
| `/home/brian/code/ecosystem-ops` | `924e556b325c9e927c4215480a08c2f407d7866e` | 12 untracked paths from another writer (brain-health monitor files, `build/`, `uv.lock`, `.claude/hook_log.jsonl`). Not read, not touched. |
| `/home/brian/code/openclaw` | `af67a1388f0639e1cb8fc6dca6c2503fe4f56fa9` | clean |
| `/home/brian/code/machine-coordination` | `f0449000375c707bd404448fca84518953b81127` | clean |

Paths are relative to each repo unless absolute. Runtime state I read (read-only) to decide
"observed" versus "tested": `~/.claude/coordination/supervisor-events-v1.jsonl`,
`~/.local/state/operator-notify/notifications.jsonl`, `~/.local/state/attention-push/`,
`~/.local/state/ecosystem-feedback-system/`, `~/.openclaw/`, the `systemctl --user` timers, and the
`attention-page.service` journal.

**What these systems are.** ecosystem-ops is Brian's ops layer. It runs a daily cron pipeline
(scout, health, anomalies, digest), a dashboard, a typed supervisor-event ledger with
attention delivery (Plan 79), a personal attention page with phone push (project-meta Plan 288),
and a registry-driven observation-to-repair runtime with a watchdog (Plan 273). openclaw holds
the task queue plus the Plan 79 role leases and attention routing. machine-coordination runs
fleet reconciliation: it keeps each machine's configuration matching a declared spec. Most of
it is machine plumbing and was skipped.

## Ideas

Status meanings: **observed** means it ran for real and left evidence (path given). **tested**
means fixture or unit tests only. **design** means written down but never exercised.

| # | Idea | Source path | Status | v0.2 gap | Trigger to adopt |
| --- | --- | --- | --- | --- | --- |
| E1 | **Decisions are identified by their content and only move forward.** A decision's id is sha256 of its key plus its exact scope. Once a decision is terminal (approved, denied or superseded), any event that tries to make it pending again is rejected. If the target or consequence changes, that is a new id and a new decision. Nobody reopens the old one. *Why:* nobody gets asked twice for the same decision, and an answer given in another thread cannot be overwritten by a stale "still pending". Stronger than cf. #1 ("needs-human deduplicated to one Inbox row"), because it defines what counts as the same decision. | `ecosystem-ops/supervisor_events.py` (`decision_digest`, `validate_against_ledger`); born from the Steno Lab stale-pending regression in `ecosystem-ops/plan/goals/2026-09-09-attention-preserving-agent-supervisor.md` ("Worker event 4") | **observed** (the ledger has 2 real terminal decisions, and the regression was reproduced as a failing test before the fix) | attention/escalation; decision records | A v0.2 run raises a human-owned decision, or AES gains any "human approves X" record. |
| E2 | **A human directive keeps the exact words and cannot act while it is ambiguous.** The directive stores Brian's exact response, the source thread and time (the directive id is a hash of these), a bounded interpretation, a confidence, any unresolved ambiguity, and an `authority_delta` that must say `none` explicitly when nothing changes. An ambiguous directive is forced to `executable=false` with `authority_delta=none`. Silence, "thanks" and acknowledgements never authorize anything. *Why:* an agent's paraphrase can no longer quietly widen what Brian authorized. | `ecosystem-ops/supervisor_events.py` (`HumanDirective`); contract in `ecosystem-ops/docs/plans/79_human_attention_orchestrator_control_loop.md` §Canonical Artifact Contract | **tested**. One real source-bound directive was recorded (SHA in Plan 79 §Current execution horizon), but the round trip that would consume it was never run. | attention routing; authority | A human approval unlocks an AES plan item, a boundary, or `aes plan accept` on someone else's behalf. |
| E3 | **Every event is recorded, but only some are sent.** Events get one of four treatments: interrupt, decision inbox, digest, or suppress. Routine states (milestone, CI result, retry, heartbeat, unchanged, support-only, delivery receipt) are marked `recorded_only`: they go in the ledger but are never sent. Suppression affects sending only; the evidence is kept. There is also a protected "human planning" mode: while Brian is planning, his session is woken only for an imminent safety or authority violation, or for a write conflict that names his session. An interrupt saves the suspended task, its checkpoint, its scope and the event that resumes it. *Why:* this measures success as attention saved, not messages sent. Complements cf. #5 (a durable pause). | `ecosystem-ops/supervisor_events.py` (`ROUTINE_EVENT_STATES`, `should_transport_event`); Plan 79 §Attention Policy | **tested** (the containment unit was accepted in commits `1c8a6df` and `c030892`). The real ledger shows all 11 events *queued*, including 3 milestones, because they predate this rule. | attention/escalation | AES sends more than one kind of event toward a human or an agent session. |
| E4 | **Four delivery states, and each channel labels how it knows.** The states are queued, delivered, observed and responded. A transport acknowledgement never counts as the human having seen it. Each route reports its own evidence level, e.g. `assumed_from_exit_code` vs `observed_at_broker`. OpenClaw spells delivery out as a transition table: queued→delivered or queue_failed; queue_failed→queued (retry); a crash after queued is "outcome in doubt", and retrying it is refused, so a message is never sent twice. *Why:* "we sent it" and "he saw it" stop being the same claim. | `ecosystem-ops/supervisor_events.py` (`AttentionDeliveryReceipt`); `openclaw/attention_routing.py` (commit `34c0863`); evidence in the pilot goal doc §"Generic notification test" | **observed** (the pilot's ntfy route was confirmed at the broker and on Brian's handset via Plan 269). The transition table is tested only. | attention/escalation | AES delivers anything to a human or a remote session. |
| E5 | **Alerting for persistent failure uses two channels.** (a) The watchdog alerts only when health changes state: exit code 20 is reserved for "newly unhealthy", and staying unhealthy exits 0. A separate systemd `OnFailure=` reporter alerts even if the watchdog itself dies. (b) Failure that lasts longer than N seconds opens one keyed concern, re-comments on it at most daily, and closes only after an unbroken healthy streak as long as that threshold. *Why:* alerting on changes alone hid a runtime that failed every sweep, and one healthy reading mid-sweep kept resetting the clock. | `ecosystem-ops/scripts/run_feedback_watchdog.py` (return 20); `ecosystem-ops/src/feedback_system/concern_sync.py`; commits `9b2a380`, `028cecf`; live `~/.local/state/ecosystem-feedback-system/concern-sync-state.json` (unhealthy since 2026-09-25, concern registered) | **observed** | attention/escalation; unattended controls | AES runs any scheduled or unattended check, e.g. drift monitoring of an installed gate. |
| E6 | **"Loud" means a person hears about it.** This became ecosystem policy `unattended-failure-must-reach-a-person` (registry 190). It is paired with a visible circuit breaker: only unrecoverable states (no credit, rejected key) trip it, never timeouts, and while it is open the output says so, with the reason and how long. *Why:* in one day, four separate silent failures were found (lasting from 1 day to 5 months). Each was written by an agent that believed it was failing loudly. This defines the acceptance test that cf. B6 ("receipts written but never read") lacks. | `ecosystem-ops/HANDOFF-2026-08-23-scout-and-unattended-failures.md` §7, §9; `ecosystem-ops/brief_circuit.py` | **observed** | attention; control observability | AES adds any background characterization, hook, or skipped check. |
| E7 | **A "wrong when" condition is a running monitor, and "all clear" requires proof the monitored thing is alive.** Accepted decision concerns and plan wrong-when conditions are checked automatically. When one fires, it opens one keyed concern issue, which closes itself on the next clear evaluation. The missing piece, learned the hard way (F2): a clear result must also prove its producer is alive. *Why:* this turns AES decision "wrong when" clauses into signals someone actually sees. | `ecosystem-ops/decision_concern_monitor.py`; `project-meta/scripts/check_decision_conditions.py`; project-meta issue #2055 (opened with real evidence, "77 pushes in 24h") | **observed** (both firing and closing) | learning loop; decisions | An AES decision's wrong-when condition can be computed from data AES already reads. |
| E8 | **A gap is closed only when its registered verifier passes on the landed revision.** A consumer commits a declaration with five parts: observer, repair adapter (`allowed_write_paths`), verifier, landing, and limits/schedule. The declaration's revision is pinned for the whole cycle. A per-concern `flock` prevents duplicate repairs. An action closes only when that exact verifier exits 0 on the landed canonical revision and the claim closeout is sanctioned. Agent prose, timeouts and changed heads never close it. A later failure reopens the same action id. *Why:* this is the missing gap-closure contract. It carries out AES-PLAN-003 ("plan completion is not conformance") mechanically. | `ecosystem-ops/docs/FEEDBACK_LOOP.md`; `ecosystem-ops/docs/feedback_system.md`; `ecosystem-ops/src/feedback_system/self-registration.yaml`; `ecosystem-ops/feedback_loop.py` | **observed**: 4 registrations, 9,114 runs, 5 actions, of which 2 closed and 3 are terminal (see F7) | execution; gap→repair→reconcile | A v0.2 gap has a runnable verifier, and someone wants it closed without a human in the loop. |
| E9 | **Recovery resets a task only when nobody can possibly be holding it.** A `running` action goes back to `open` only when it has a bound observation and *no* run dir, claim, worktree or executor trace. Any sign that something may still hold it gives `degraded`, left for reconciliation. The runtime never starts a duplicate based on a guess about a process id. The kernel `flock` is released when the process dies, so a stale lock file cannot deadlock. *Why:* a sharper rule than cf. #1's "one recovery without duplicate mutation". | `ecosystem-ops/docs/feedback_system.md` §Durable state and recovery | **tested** | execution/recovery | AES resumes any execution after a crash or restart. |
| E10 | **Scheduled controls run from a clone reset to the default branch before each run.** Before each run, the systemd units `git fetch` and `checkout --detach --force origin/main` under a flock, into `~/.local/share/ecosystem-runtime/<repo>`. They never run from a development checkout. *Why:* this prevents the "implemented but not operating" drift that cf. #12 can only detect after the fact. | `~/.config/systemd/user/ecosystem-feedback-worker.service` (ExecStartPre lines); commit `4dd7646` | **observed** (live timers) | distribution / operating evidence | AES ships a scheduled or hook control that must execute the default-branch version. |
| E11 | **Leased roles with fencing tokens, and a queue that admits each task only once.** Each role has at most one live lease. Fencing tokens only go up. Renew and release need the exact holder plus token. Handoff takes max+1, and lapsed leases are rewritten as expired. Queue admission refuses any task id the runner has already consumed, so a re-delivered directive cannot run twice. *Why:* this rules out two orchestrators running at once (split-brain) without anyone trusting prompt memory. | `openclaw/runtime_roles.py`, `openclaw/queue_admission.py`; commit `af67a13` | **tested only**. `~/.openclaw/runtime_roles.json` was never created (only a 0-byte lock file dated 2026-09-10). | orchestration | Two or more processes can act as coordinator for one AES consumer. |
| E12 | **An approval is re-checked against fresh state when it is applied.** An approved plan to fix a machine was re-checked at apply time against the freshly computed action kind. The fix: reject when the observed kind is neither the approved kind nor `no_op`. *Why:* an approval made while the service was healthy ("no_op") later let a broken service skip its repair and leave an `applying` receipt behind. | `machine-coordination/scripts/reconcile_desktop_host.py`; commit `94f02f4` | **observed** failure, then tested fix | plan acceptance → execution | Time passes, or the current characterization changes, between `aes plan accept` and execution. |
| E13 | **Claims about the running system carry a strength label, and there is a list of forbidden substitutes.** Each claim gets a label: user-confirmed, demonstrated on bounded paths, deployment-verified, or not verified. Delivery evidence and verification sit in separate columns. The forbidden substitutes: a process count is not agent state, a claim is not liveness (`unknown_claim_is_not_liveness`), a persisted mailbox message is not delivery, and an installed binary is not a running agent. *Why:* v0.2 already marks observations as stale or unreachable, but it does not grade *how* a live claim was learned. | `machine-coordination/plans/remote-control.md` §Capability Truth Table; pilot goal doc §Goal "Forbidden substitutes" and §"Cross-runtime truth after the WSL disconnect" | **observed** | current-state characterization | AES characterizes a runtime or operational claim, not just file contents. |
| E14 | **Status reads report per-source health, and first install never replays history.** Each source read reports `ok`, `partial` or `unknown`; a failing reader yields `unknown` plus its error, never silence. A push goes out once per (dedupe_key, state), only within a 60-minute freshness window. `--mark-seen` on first install records everything already pending, so old items never reach the phone. *Why:* "nothing to show" can no longer be confused with "a source broke". | `ecosystem-ops/attention_items.py` (`SourceStatus`, `AttentionSnapshot`); `ecosystem-ops/attention_push.py` | **observed** (timer live; 72 real deliveries) and currently broken (F1) | status / attention | AES produces any view that combines two or more sources. |
| E15 | **Ranking quality gets a gate based on human ratings.** Ratings go in a JSONL (useful yes/no, reason_code, outcome). There is a report of how useful each signal is. A signal with ≥5 ratings and <40% useful gets a 0.7× weight. The gate is "7 of the next 10 dispatched tasks useful". An FP-label ledger with reason codes found that 50–65% of detector output was false positives. *Why:* this is the only harvested mechanism that measures whether a recommendation helped a person. It complements cf. #23 (measures read from Git). | `ecosystem-ops/docs/plans/30_task_recommender_quality.md`; `ecosystem-ops/docs/plans/31_anomaly_fp_reduction.md` | **observed** in April 2026 per the plan docs. The rating ledgers are not in this checkout, so I could not confirm they are still used. | learning loop / measurement | AES ranks gaps or next actions for a human. |

## Failure lessons

1. **The attention push is broken right now, and nobody has filed it.** `attention-page.service`
   fails on every timer run with `UnicodeEncodeError: 'latin-1' codec can't encode character '…'`.
   The `…` added when titles are truncated ends up in an HTTP header. The operator notification record has
   3,815 `attention-push` rows: 72 delivered (the last on 2026-09-18) and 3,743 attempts with no outcome
   written. That pattern fits a crash between `record.append` and `mark_outcome`. The attempt
   repeats every tick (55 attempts for one key), with no backoff. The journal only goes back to
   2026-09-27 (60 crashes), so the crash's start date is inferred from the record, not observed. A
   `gh` search found no issue for it. Evidence: `systemctl --user status attention-page.service`,
   `~/.local/state/operator-notify/notifications.jsonl`, `ecosystem-ops/attention_push.py` (`push`).
   *Lesson:* the channel that carries alerts had no alert for its own death.
2. **A "wrong when" check closed green while the thing it watched was dead.** Project-meta #2055
   (`p288-push-noise`) correctly fired on real noise (77 pushes in 24h, duplicate keys). It then
   auto-closed on 2026-09-23 as "verified green, 1 push in 7d" while the pusher was failing. Zero
   output from a dead source counted as zero problems. This is a live instance of the old
   status-fallthrough lesson (harvest A7). Fix: a clear result needs proof its producer is alive.
3. **Alerting only on state changes, plus flapping, hid persistent failure.** 43 open `worker_degraded` incidents
   produced no alert. After the first fix, 13 of 15 sweeps failed, yet one healthy reading mid-sweep kept
   resetting the unhealthy clock. Commits `9b2a380`, `028cecf`.
4. **The same delivery bug appeared independently in two repos.** Record-before-send left a failed
   send stuck forever, first in `supervisor_events.resolve_attention` (commit `0e50400`, then `924e556` for
   dry-run) and then in `openclaw/attention_routing.send_to_role` (commit `34c0863`), on consecutive days.
   Per the root-cause rule this belongs in one shared delivery state machine, not two fixes at the call site.
5. **A stale pending decision was replayed after Brian had approved.** The supervisor repeated
   the Steno Lab deletion as pending after Brian approved it in the worker thread. It was
   corrected only when Brian challenged it. This led to E1. Pilot goal doc, "Worker event 4".
6. **The orchestrator was built but its end-to-end run was never observed.** Plan 79 was paused on 2026-09-11 by a route
   change to AES Plan 13. The supervisor ledger stops at 13 records on 2026-09-11. The role-lease
   registry was never created. Only fixture runs exercised the openclaw queue: `~/.openclaw/tasks`
   has 0 pending, 0 active, 0 completed and 2 failed. This repeats harvest B3 (direction churn) and B12. Evidence: Plan 79
   header; ledger `ls`/count.
7. **The repair loop runs constantly but rarely repairs.** It has 9,114 runs but only 5 actions: 2 closed, 3
   `terminal: non-retryable harness failure`, including its *own* health loop at cycle 5,162. The
   category-ladder repairs failed because the executor's configured model was rejected
   (`'gpt-6-luna' model is not supported`, visible in push bodies). The worker has been `degraded` since
   2026-09-25 because of an observer validation error. `~/.local/state/ecosystem-feedback-system/actions/*.json`,
   `worker-state.json`. *Lesson:* repair depends on an executor route that can break without anyone
   noticing, so executor health needs its own watch.
8. **Test traffic lands in production ledgers.** All 135 rows in `~/.openclaw/cost_log.jsonl` are
   test fixtures ($0.10, 1.0 s), written on commit days. Benchmarking once wrote 533 test records
   into the real claim archive (handoff §7.3). The default ledger paths point at `$HOME`. Harvest B7
   covers provenance tagging; the extra lesson is that tests must not have a production default path.
9. **Measurement discipline slipped.** A speedup was claimed from one timing sample, when the true
   end-to-end time was unchanged. A multi-source retrieval layer was built without checking that
   `open_web_retrieval` already owned it. Handoff §7.1–7.2.
10. **The detector's false positives defeated it.** A 50–65% FP rate (inactive-project residue,
    duplicates) made the anomaly pipeline "self-defeating". Plan 31.

## Not worth harvesting

- Tailscale, Paseo, SSH and pairing-offer plumbing in machine-coordination. The only transferable
  ideas are E12 and E13.
- Scout's GitHub/web discovery, `golden_canary.py` (a generic LLM-as-judge regression), and `triage_contracts.py`.
- Dashboard and control-center UI surfaces (`ui/registry.yaml`, command room, VS Code launchers).
- `task_recommender.py` scoring internals, and the `plan_freshness.py` auto-complete, which marks plans done when
  their checkboxes are done. That runs against AES-PLAN-003.
- Cloudflare public-route monitor specifics (Plan 80). Its transition-alert idea is already covered by E5.
- The untracked brain-health monitor files in ecosystem-ops (another writer's uncommitted work;
  not read).

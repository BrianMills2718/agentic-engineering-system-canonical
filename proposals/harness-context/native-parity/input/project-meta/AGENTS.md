# project-meta — Ecosystem Governance

This repo is the **governance hub** for Brian's project ecosystem: vision docs, enforcement scripts, project index, and operational state.

Brian operator landing file:
- `BRIAN_READ_THIS/README.md`

**Project Meta and AES are two shots on one outcome.** Brian plans and reviews
while coding agents act efficiently and autonomously toward those planned goals.
Project Meta is the established repair-and-simplify route; the Agentic
Engineering System (AES, `BrianMills2718/agentic-engineering-system-canonical`)
is the independent clean-room route. Neither is currently the declared successor
of the other. (Resolved 2026-09-26, Brian: canonical is the AES. AES Decision
0011 there archives `Inside-Success/agentic-engineering-system`, the previous
AES repository, and harvests its borrowable ideas with adoption triggers in
`research/synthesis/2026-09-26-inside-success-aes-harvest.md`; its Plan 16 is
not continued. `BrianMills2718/agentic-engineering-system` is an empty
placeholder and `BrianMills2718/aes` was folded into the Inside Success repo on
2026-08-26; both are archived. The Inside Success team rollout is paused until
whygame5 produces a result under AES governance.)

AES decision 0009 (2026-09-01) supersedes decision 0007's replacement
destination and amends decision 0008's staged-migration reading. Existing
capability owners remain authoritative until a later accepted decision selects
reuse, transfer, supersession, or retirement from observed working evidence.
Claims, worktrees, session close, and the mailbox therefore stay with Enforced
Planning unless explicitly superseded. Read
`agentic-engineering-system-canonical/docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md`
(and, for the archived route's own account, the Inside Success repo's
`docs/decisions/0009-two-shots-one-autonomous-coding-outcome.md`)
before assuming either route's destination.

`PROJECT_GRAPH.json` records current repository identity and lifecycle, not a
future winner. Its `supersedes`/`superseded_by` fields assert completed
supersession, so both records remain empty unless a later accepted convergence
decision and observed replacement evidence justify changing them.

**Policy-system orientation.** Before auditing, explaining, or changing the
cross-project policy system, read
[`docs/ops/POLICY_SYSTEM.md`](docs/ops/POLICY_SYSTEM.md). It is the single
Project Meta front door for policy authority, agent context, hooks and checks,
coordination claims and worktrees, cross-agent communication, learning and
feedback stores, concern resolution, and autonomous execution. Follow its
links to the owning implementation instead of searching sibling repositories
blindly or treating an installed home-directory copy as authority.

---

## Outcome-Persistent Execution

When Brian authorizes continuous execution, read
`docs/ops/ACTIVE_PLAN_QUEUE.md`, select the highest-value eligible slice,
execute it, retain evidence, update the owning tracker, and select again. Do not
ask for a generic "continue" merely because a turn, phase, commit, or green test
ended.

Continue while authorized, dependency-ready, outcome-advancing work remains and
the next action is **not irreversibly dangerous**. This is not a risk-free-work
requirement: reversible experiments and bounded failures are allowed. The
boundary preserves irreversible shared-state changes, external actions and
publication, human-owned decisions, explicit spend limits, missing or
conflicting authority, and circuit breakers. When one lane reaches a boundary,
continue another eligible lane rather than idling the whole program.

The older phrase "never stop" is a legacy trigger for this state-based
continuation contract; it does not expand scope, authority, or risk tolerance.

Full contract: `enforced-planning/docs/guides/CONTINUOUS_EXECUTION_CONTRACT.md`

---

## Immediate Policy Feedback

Use the single policy feedback register for two distinct entry types:

- `friction` when a required rule, command, hook, or skill is unclear, missing,
  contradictory, wrong, or creates a concrete avoidable workflow cost;
- `recommendation` when evidence supports a reusable improvement even though no
  policy has misfired.

Correctly functioning controls can still be suboptimal. Ordinary necessary work
and unsupported preferences are not feedback entries. Use
`make policy-feedback TYPE=friction|recommendation ...`; `make policy-friction`
remains a compatibility alias. Register entries are not accepted policy until
the owning authority adopts them. Verification gaps are narrower: use that log
only when new evidence contradicts work previously declared complete or green.

---

## Commands

```bash
# One-time per clone: activate git hooks (pre-commit incl. coordination-claim warn
# + global secrets-hook chain, commit-msg prefix check). Local config, not synced.
git config core.hooksPath hooks
make enforcement-liveness                            # Are hard enforcement channels (hooks/CI/audit) actually live?

# Bounded, reversible maintenance not owned by a numbered plan
make maintenance-worktree BRANCH=maintenance-issue TASK="repair one verified issue" WORKTREE_AGENT=codex SESSION_GOAL="keep Project Meta entrypoints truthful" SESSION_PHASE="repair and verify"

# Session-start context injection
python scripts/knowledge_router.py --project PROJECT [--intent "task description"]  # Load route + memory context (~600 tokens)
make context-load PROJECT=llm_client INTENT="fix batch embedding"                   # Same via Makefile

```

Governance maintenance, validation, and regeneration commands live in
`scripts/AGENTS.md`, which loads when work touches that subtree.

Documentation-subtree routing lives in [docs/AGENTS.md](docs/AGENTS.md);
follow it before changing documentation and then load the more-specific
instruction file for the target directory when one exists.
The integrated development-wiki entrypoint is [wiki/index.md](wiki/index.md);
use it for progressive project orientation, then follow links to native authority.

## Principles

1. **Generated > Narrative** for mutable facts — project counts, status, capabilities live in `generated/ecosystem_snapshot.json`, not hand-written docs
2. **Runtime metadata is ephemeral** — volatile fields (`generated_at_utc`, repo `git_head`, repo `is_dirty`) live in `generated/runtime/ecosystem_runtime_metadata.json` and are never committed
3. **ADR-0005 Compression Hierarchy** governs `vision/` — every doc must justify: unique compression, identified consumer, freshness mechanism
4. **Doc-role headers** required per `scripts/doc_lint.py`
5. **Every vision doc earns its place** — archive or delete docs that fail the 3-test (unique compression, consumed, fresh)
6. **Do not let the smallest useful first slice quietly redefine the long-term architecture.** Keep the target architecture explicit in vision/plans even when the current implementation deliberately compresses layers for speed or proof. A thin slice may prove one wedge of the system; it does not automatically become the north star.
7. **Plan in two views when needed: target architecture and current implementation slice.** When the long-term design is richer than what should be built now, write both down explicitly:
   - the north-star boundary/ownership model
   - the phase-limited implementation slice with non-goals
   This prevents "what is easiest now" from being mistaken for the intended permanent shape.
8. **Small slices should preserve future separation.** Early implementation may collapse concerns temporarily, but requirements and design docs must state which separations remain architecturally important later.
9. **Portable-first tooling** — reusable tooling should resolve paths via environment/config/project graph, not hardcoded `~/projects`.
10. **Autonomous workspace default** — treat portable workspaces as the baseline for shared execution; if portability violations are introduced, stop and fix before broadening adoption.
11. **Autonomous execution means keep moving through uncertainty, not stopping at it.** For continuous or overnight work, define the next phases explicitly, log uncertainties in the active plan or knowledge files, choose the next bounded action, and continue.
12. **Continuous execution must be converted into an explicit sprint contract immediately.** When a user asks for "all night," "never stop," or similar persistence, build the phase list before coding, write one active plan plus one active TODO tracker with explicit success criteria, uncertainties, rollback points, and next action, then execute phases in order.
13. **Commit every verified slice during autonomous runs.** Long-running work must leave rollback points after each real milestone: planning, scaffold, implementation wedge, evaluation, and documentation.
14. **Continuous execution requires a persistent TODO tracker, not just conversational intent.** For overnight or multi-phase work, keep one in-repo tracker updated with current phase, explicit success criteria, completed work, open uncertainties, and next actions.
15. **A completed sprint alone is not a stop condition during continuous execution.** When one bounded plan finishes and an authorized, dependency-ready, higher-value phase remains whose next action is not irreversibly dangerous, define that phase from the current measured state, update the active TODO tracker, and continue. When no such phase remains, apply the autonomous progress boundary: leave a resumable handoff and return control instead of manufacturing work.
16. **If a phase is blocked, record the blocker precisely and continue on the highest-value unblocked phase.** "Blocked" is not "stop." It means tighten the uncertainty, leave evidence, choose the next bounded action that still advances the plan, and keep going until no authorized, dependency-ready, outcome-advancing work remains that is not irreversibly dangerous.
17. **Shared capability extraction or migration must be governed explicitly before code moves.** If a capability may become shared infrastructure, upstream ownership, or historical/archive-only, record that in `project-meta` with a source plan, migration gate, and blocking uncertainties.
18. **Capability ownership is an ecosystem concern, not only a repo concern.** Repo-local decomposition plans are required, but any capability with cross-project consumers or migration intent must also be represented in the shared `project-meta` ownership surface.
19. **Check active coordination claims before overlapping cross-brain work.** When Claude Code, Codex, or OpenClaw may touch the same project or scope, inspect `~/.claude/coordination/claims/` and `generated/runtime/active_work_registry.json` before starting overlapping work. Those live coordination surfaces are authoritative for who is writing what. Use `agent-memory recall ...` only for an intentional lookup of legacy historical context; it is not a startup or overlap-check requirement. Reusable findings belong in the version-controlled learning register. Before treating any specific agent (Codex, another Claude Code session) as currently live -- not just before overlapping work -- run `python scripts/meta/check_agent_liveness.py`: a claim file's existence, or even a recent-looking heartbeat, is not proof by itself (fixed 2026-09-14 after treating "the other Codex session" as an ongoing participant for hours without ever checking; every codex claim on the machine was already terminal, and its own session index showed no activity in ~12 hours).
20. **Broad program claims are not enough for narrow write safety.** For governed repos, active implementation work should move toward narrow write claims with explicit `write_paths`, branch, worktree, and plan reference. A claim like `phase-6-ops-and-governance` is useful context, but it is not a precise write boundary.
21. **Continuous runs must leave one authoritative active-work surface.** If a sprint creates or mutates claims, regenerate the active-work registry and update the sprint/TODO docs so another agent can answer “who is writing what right now?” without reading raw YAML.
22. **Merge, push, or a green verification pass are rollback points, not stop conditions.** If the operator asked for continuous execution and there is still a higher-value unblocked phase, immediately open the next worktree/plan or continue the active sprint.
23. **Shared safety mechanisms are not rolled out until repos expose sanctioned entrypoints for them.** A helper that exists only in `project-meta` or only in pattern docs is not enough. If a shared safeguard matters operationally, give governed repos one clear local interface for it and audit that interface explicitly.
24. **Default-branch policy must be explicit and branch-name assumptions must stay localized.** The active ecosystem target state is `main`. Active policy and automation should refer to the "canonical default branch" unless the literal branch name matters for a concrete migration or historical record.
25. **Hot-path renames are compatibility migrations, not search-and-replace events.** For any active repo/path rename, first introduce a logical-id registry, then flip the active path, keep a compatibility alias during the migration window, verify generators/validators against the new path, and only later clean up historical references.
26. **After a hot-path rename lands, forward-writing docs must use the new identifier exclusively.** For the Research Synthesis Library, active canonical docs should use `research_synthesis`; `research_texts` is reserved for compatibility, lineage, and historical artifacts only.
27. **The research_synthesis cutover contract is mechanically enforced.** `scripts/check_research_synthesis_cutover.py` is the authoritative validator. Forward-writing canonical docs must not contain `research_texts`; compatibility aliases and historical artifacts may. Any forward-writing doc that introduces `research_texts` is a CI lint failure. Run `python scripts/check_research_synthesis_cutover.py` to verify locally.
28. **LLM cost is observe-only by default.** An active goal or plan authorizes the calls needed to execute it. Record requested/resolved models, tokens, latency, and actual cost, but do not require a spend permit, reservation, launch pin, manual approval, or cost-based stop condition unless the project's canonical configuration or plan explicitly opts into cost enforcement. A required `max_budget` argument is a configurable technical ceiling and telemetry field, not proof of authorization.
29. **The critical path is outcome-first and value-per-time.** Every non-trivial implementation plan preserves one plain-language user outcome and one canonical behavioral example. Classify increments as `vertical`, `direct_blocker`, `enabler`, or `hardening`; before the example is observed, only vertical work and demonstrated direct blockers belong on the critical path. Enablers and hardening never advance product status by themselves. Optimize for expected user-visible value or decisive learning per wall-clock hour. At the earliest of roughly 45 minutes, two consecutive non-outcome increments, or user concern about pace, ask what would make the result substantially more impressive or useful in the next 30–60 minutes and compare it with the current path. Switch reversible in-scope tactics when another action is materially better; the check creates no plan, report, approval gate, or narrower success criterion. Report behavioral evidence separately from substrate/process evidence.
30. **Choose from first principles before benchmarking.** Derive decisions from goals, requirements, failure modes, boundaries, reversibility, and established evidence. A blocking or consequential decision does not itself justify comparative evaluation. Compare only an irreducibly empirical uncertainty when candidates meet a common minimum capability contract, the result can change the decision, and testing costs less than a reversible choice. If fairness requires fully building and polishing multiple options, choose behind a replaceable boundary and validate the selected implementation against its own requirements.
31. **No untested human handoffs.** Before asking a human to try, assess, or accept a changed runnable workflow, execute its canonical journey against the exact target revision, launch configuration, and route; inspect the result and repair any direct failure. When an LLM is central, this includes one authentic traced model call, not a fixture. State the passing endpoint or command, observed outcome, and trace/evidence reference in the handoff. Ask the human only for an irreducibly human action (for example, sign-in or judgment) or a stated remaining uncertainty; any changed runtime/configuration requires a fresh journey. For a material UI, build the exercised journey to be agent-operable through the same public surface a human uses: semantic controls with stable accessible names, explicit loading/empty/success/disabled/failure states, deterministic launch/seed/reset paths, and visible console or network failures. Keep the critical journey executable next to the owning UI. Setup APIs may prepare state, but API-only checks, source inspection, compilation, or screenshots without interaction do not prove the UI works. Prototype evidence stays proportional: one representative viewport and one critical flow unless broader coverage can invalidate the prototype's hypothesis.

---

## Terminology

| Term | Meaning |
|------|---------|
| Document authority | The single canonical location for a piece of information |
| Governance snapshot | Machine-generated ecosystem state (`generated/ecosystem_snapshot.json`) |
| Compression layer | ADR-0005 hierarchy: Foundation > Framework > Status > Generated |
| Status ledger | `STATUS_LEDGER.md` — historical governance decisions and milestones |
| Doc coupling | Declared dependency between source files and documentation |

---

## Workflow

### Process Awareness
- All significant work follows meta-process plans in `docs/plans/`
- Use `[Trivial]` only when neither the fact a change happened nor its result
  needs durable documentation — not a line-count threshold (Plan #261); see
  `docs/plans/AGENTS.md` Working Rule 1 for the full test
- Route durable future work by owner and artifact type: uncertain short-lived
  observations go to the owner's inbox; confirmed problems or questions go to
  the owner's issue register; accepted execution goes to an owner-local plan;
  and sequencing goes to the owner's roadmap. Cross-project work has one named
  coordinator with linked dependent work. Only a genuinely new-project idea
  without an owner uses the candidate-project incubator. `deferred` is a
  lifecycle status, not a destination.
- The subtree instruction layer is delta-only; see `docs/ops/SUBTREE_INSTRUCTION_HIERARCHY.md`

### Autonomous Workspace Rule
- Start new agentic work in a portable workspace first using the launcher:
  `bash scripts/bootstrap_portable_workspace.sh <project-id...>`.
- Keep `--portable-first` enabled for any project expected to run outside its
  configured Project-Graph checkout.
- Concrete pilot flow for new systems:
  1. `bash scripts/bootstrap_portable_workspace.sh <project-id...>`
  2. Switch to `/home/brian/autonomous_projects/<timestamp>/managed/<project-id>` and run work from there.
  3. Only promote to broader use when the bootstrap stays `PASS` and the report at `autonomous_portability_check.json` is clean.
- Clustered pilot mode: `bash scripts/bootstrap_portable_workspace.sh --cluster <cluster-name>...`
- Cluster definitions file: [scripts/autonomous_workspace_clusters.txt](scripts/autonomous_workspace_clusters.txt)
  - This creates an isolated workspace under `/home/brian/autonomous_projects/<timestamp>/`
  - It always enables strict `--portable-first` checks and keeps source roots configurable through `PROJECTS_ROOT`.

---

## References

| Doc | Purpose |
|-----|---------|
| `STATUS_LEDGER.md` | Historical governance decisions and milestones (not live operational state) |
| `vision/00_START_HERE.md` | Navigation entry point for new readers |
| `vision/README.md` | Vision docs index and hygiene rules |
| Project Graph record `enforced-planning` | Portable framework docs (extracted 2026-04-01) |
| `docs/plans/INDEX.md` | Complete plan catalog |
| `wiki/index.md` | Integrated development-wiki entrypoint and progressive reading routes |
| `docs/ops/SUBTREE_INSTRUCTION_HIERARCHY.md` | Delta-only nested `AGENTS.md` policy |
| `meta-process.yaml` | Framework configuration |

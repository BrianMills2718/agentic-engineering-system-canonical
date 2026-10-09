---
doc_role: operations
authority: canonical
mutable_facts_allowed: yes
status: active
updated: 2026-09-16
---

# Policy system — single-repository front door

This repository is the information authority for Brian's policy system. A
reader should be able to start here and answer:

- what rules exist and why;
- what context an agent receives before acting;
- which hook, check, or human judgment applies a rule;
- whether that enforcement path is live;
- what evidence the rule emits;
- where friction, corrections, and reusable lessons go; and
- how an observed problem becomes a verified change.

The policy system is not only its hooks. Hooks are one delivery and enforcement
channel inside a larger loop. Implementations may remain in the repository that
owns them, but their policy meaning, owner, executable path, feedback route,
known gaps, and verification command must be discoverable from Project Meta.
Copying implementation code here would create a second source of truth; tracing
it from here gives one comprehensible system without forking its owners.

An agent started inside this repository automatically receives its authored `AGENTS.md`, which routes policy-system work to this page. That gives
the agent a category-indexed map and runnable discovery routes; it does not
preload the contents of every linked implementation into the model's context.

## Coverage categories and completeness boundary

The current policy-system information is organized into these categories:

| Category | Information that belongs in it | Primary Project Meta route |
| --- | --- | --- |
| Authority and scope | Governing rules, whose authority applies, protected boundaries, permissions, and publication or irreversible-action limits | Root `AGENTS.md`, [`policy/registry.yaml`](../../policy/registry.yaml), and [`PROJECT_GRAPH.json`](../../PROJECT_GRAPH.json) |
| Policy inventory and rationale | Each policy's intent, scope, source, enforcement classification, declared gaps, and why the design was chosen | [`policy/registry.yaml`](../../policy/registry.yaml), [`ECOSYSTEM_POLICY_MODEL.md`](./ECOSYSTEM_POLICY_MODEL.md), and the policy ADRs indexed by [`INDEX.md`](./INDEX.md) |
| Context and instruction delivery | Workspace/repository instructions, expected-context routing, skills, generated client surfaces, and delivery receipts | [`AGENT_CONTEXT_SURFACE_TARGET_STATE.md`](./AGENT_CONTEXT_SURFACE_TARGET_STATE.md), [`INSTRUCTION_SURFACE_SYNC_POLICY.md`](./INSTRUCTION_SURFACE_SYNC_POLICY.md), and [`scripts/relationships.yaml`](../../scripts/relationships.yaml) |
| Hooks and enforcement | Lifecycle hooks, repository hooks, checks, CI, scheduled audits, human judgment points, client parity, and the executable negative controls that show a channel can fail | [`INSTRUCTION_SURFACE_SYNC_POLICY.md`](./INSTRUCTION_SURFACE_SYNC_POLICY.md), [`wiki/concepts/cross_client_config_sync.md`](../../wiki/concepts/cross_client_config_sync.md), and the relevant registry rows |
| Coordination and communication | Claims, worktrees, session lifecycle, live-agent discovery, messages, durable mailbox obligations, and acknowledgements | [`2026-09-02-agent-coordination-systems.md`](./2026-09-02-agent-coordination-systems.md) and [convergence decision D7](./ADR-2026-09-15-convergence-decisions.md#d7--answer-expected-agent-messages-go-through-the-coordination-mailbox) |
| Autonomous execution and priorities | Goal/plan authority, active queues, continuous-execution rules, stop conditions, and current priorities | [`CURRENT_AUTHORITY_STACK.md`](./CURRENT_AUTHORITY_STACK.md), [`ACTIVE_PLAN_QUEUE.md`](./ACTIVE_PLAN_QUEUE.md), and the Project Graph record for `enforced-planning` |
| Observation and system health | Runtime receipts, status commands, liveness probes, audits, degradation, and the distinction between declared, configured, delivered, and executed behavior | [`POLICY_SYSTEM_OPERATIONS.md`](./POLICY_SYSTEM_OPERATIONS.md), `make policy-system-status`, and `make enforcement-liveness` |
| Feedback and correction | Policy friction, human corrections, recommendations, proposals, and the path from observed misfit to an accepted or rejected policy change | [`policy_friction.md`](../../policy_friction.md), [`policy/proposals/`](../../policy/proposals/), and [`POLICY_SYSTEM_OPERATIONS.md`](./POLICY_SYSTEM_OPERATIONS.md) |
| Learning and memory | Immutable reusable learnings, review/promotion routes, the measured failure-mode taxonomy, client-specific memory boundaries, and cross-client parity requirements | [`learnings/README.md`](../../learnings/README.md), [`learnings.md`](../../learnings.md), the [`agent-skills` failure taxonomy](https://github.com/BrianMills2718/agent-skills/blob/main/skills/review/references/failure-modes.md), and [`wiki/concepts/cross_client_config_sync.md`](../../wiki/concepts/cross_client_config_sync.md) |
| Concerns, remediation, and closure | Keyed concerns, ownership, implementation lanes, verification against the original failure, reopen conditions, and durable recovery dispositions | [`ADR-2026-09-14-one-feedback-concern-lifecycle.md`](./ADR-2026-09-14-one-feedback-concern-lifecycle.md) and [`POLICY_SYSTEM_OPERATIONS.md`](./POLICY_SYSTEM_OPERATIONS.md) |
| Ownership and dependencies | Capability owners, repository boundaries, cross-project contracts, implementation references, consumers, and custody/recovery routes | [`PROJECT_GRAPH.json`](../../PROJECT_GRAPH.json), [`scripts/capability_ownership_registry.yaml`](../../scripts/capability_ownership_registry.yaml), and [`scripts/capability_custody_registry.yaml`](../../scripts/capability_custody_registry.yaml) |
| Decisions and history | ADRs, rejected alternatives, lineage, supersession, and evidence that preserves why the current state exists | Policy ADRs and reviews indexed by [`INDEX.md`](./INDEX.md), plus [`STATUS_LEDGER.md`](../../STATUS_LEDGER.md) for historical milestones |
| Runtime and sensitive-state boundary | Machine-local configuration, credentials, trust state, transient observations, retention, and what must be inspectable without being copied into Git | [`INSTRUCTION_SURFACE_SYNC_POLICY.md`](./INSTRUCTION_SURFACE_SYNC_POLICY.md), [`scripts/capability_custody_registry.yaml`](../../scripts/capability_custody_registry.yaml), and the runtime boundary in this page's [one-repository definition](#what-one-repository-means) |

This table is the **current coverage schema, not a claim that no future category
can exist**. A newly observed class of relevant information must be recorded and
added here rather than silently forced into the nearest row. At a specific Git
revision, “informationally complete” means every declared category has a
canonical Project Meta route, an owner for any external implementation, and
either a live verification path or an explicit unverified gap. It does not mean
that Project Meta contains every implementation, secret, runtime event, or
conversation transcript, and a successful fresh-agent navigation test proves
reachability of the tested categories rather than closed-world completeness.

## One concrete example

When an agent changes `policy/registry.yaml`, the system is physically doing
several different things:

1. Workspace and repository `AGENTS.md` files establish durable
   rules and authority.
2. `scripts/prepare_expected_context.py` resolves the target file through
   `scripts/relationships.yaml` and delivers the required policy/context
   documents in a content-addressed packet.
3. Claude Code or Codex lifecycle hooks run configured pre-tool checks. Their
   Git-backed desired configuration is owned by `agent-skills`; Project Meta
   records the policies those hooks implement and how to verify them.
4. The edit changes the canonical registry row, including its source,
   enforcement, executable references, feedback path, and declared gaps.
5. Repository hooks and checks validate the registry and generated views.
6. Runtime observations, policy friction, a human correction, or a failed
   verification feed the concern lifecycle; a change is resolved only when a
   verifier proves the original failure no longer occurs.

On 2026-09-16, the real context-delivery command for that example resolved six
required atoms totaling 109,949 bytes and completed in ten 12 KB chunks. That
observation is evidence about the current delivery boundary, not a permanent
target or a reason to copy the packet into this document.

## System map

```text
policy intent and source documents
  -> policy/registry.yaml
  -> context delivery and enforcement configuration
  -> agent decision, hook, check, CI, or scheduled audit
  -> receipts, findings, friction, corrections, and lessons
  -> one owned concern and remediation lane
  -> verification against the original failure
  -> close, reopen, weaken, strengthen, or retire the policy
```

| Question | Start here in Project Meta | What it owns |
| --- | --- | --- |
| What policies exist? | [`policy/registry.yaml`](../../policy/registry.yaml) | Canonical structured inventory: intent, scope, sources, enforcement, commands, artifacts, feedback, maintenance, and gaps |
| What does one policy currently claim? | [`wiki/policies.md`](../../wiki/policies.md) and [`docs/POLICY_ENFORCEMENT_MATRIX.md`](../POLICY_ENFORCEMENT_MATRIX.md) | Generated human views; never edit directly |
| How is the intended system synthesized for an agent reader? | [`wiki/concepts/policy_system.md`](../../wiki/concepts/policy_system.md) | Derived, source-linked explanation of observable, enforceable, connected, and effective policy |
| What is a policy and how is enforcement classified? | [`ECOSYSTEM_POLICY_MODEL.md`](./ECOSYSTEM_POLICY_MODEL.md) | Policy model, tiers, channels, layers, lifecycle, and self-application |
| How does the whole loop operate? | [`POLICY_SYSTEM_OPERATIONS.md`](./POLICY_SYSTEM_OPERATIONS.md) | Observation, feedback, concern, ownership, verification, and recovery |
| What context reaches an agent? | [`AGENT_CONTEXT_SURFACE_TARGET_STATE.md`](./AGENT_CONTEXT_SURFACE_TARGET_STATE.md), [`INSTRUCTION_SURFACE_SYNC_POLICY.md`](./INSTRUCTION_SURFACE_SYNC_POLICY.md), and `scripts/relationships.yaml` | Target context architecture, client-surface contract, and repository-local routing |
| How are hook declarations governed? | Registry rows plus [`INSTRUCTION_SURFACE_SYNC_POLICY.md`](./INSTRUCTION_SURFACE_SYNC_POLICY.md) | Policy meaning and cross-client requirements; the Git-backed hook manifest remains with its implementation owner, `agent-skills` |
| Which repository owns an implementation? | [`PROJECT_GRAPH.json`](../../PROJECT_GRAPH.json) and `scripts/capability_ownership_registry.yaml` | Repository identity and cross-project capability ownership |
| Are enforcement channels actually live? | `make policy-system-status` and `make enforcement-liveness` | Fresh observed status, not prose claims |
| Where does feedback go? | [`policy_friction.md`](../../policy_friction.md), [`learnings/`](../../learnings/), policy proposals, and the concern lifecycle in [`POLICY_SYSTEM_OPERATIONS.md`](./POLICY_SYSTEM_OPERATIONS.md) | Native evidence stores and their promotion path |
| Which recurring agent failures must reviews test for? | The [`agent-skills` failure taxonomy](https://github.com/BrianMills2718/agent-skills/blob/main/skills/review/references/failure-modes.md) | `agent-skills` owns the current 19-family audit instrument, its accepted-input contract, derivation bundle, semantic dispositions, and backlog-draining feedback loop; Project Meta owns the learning register that supplies recurring input |
| Why was the current design chosen? | Policy ADRs in this directory and source-linked reviews under `docs/reviews/` | Durable decisions, rejected alternatives, and evidence |

## Operational subsystems every agent must be able to find

| Subsystem | Project Meta route | Owning implementation and first check |
| --- | --- | --- |
| Authority, safety, and publication boundaries | Root `AGENTS.md`, [`policy/registry.yaml`](../../policy/registry.yaml), and [`PROJECT_GRAPH.json`](../../PROJECT_GRAPH.json) | Project Meta owns cross-project authority and policy meaning; resolve an unfamiliar owner through the Project Graph and verify the applicable registry row before acting |
| Hooks and client wiring | Registry rows, [`INSTRUCTION_SURFACE_SYNC_POLICY.md`](./INSTRUCTION_SURFACE_SYNC_POLICY.md), and [`wiki/concepts/cross_client_config_sync.md`](../../wiki/concepts/cross_client_config_sync.md) | Project Graph record `agent-skills`; from that repository run `python scripts/manage_client_config.py check` and `python scripts/check_hook_parity.py` |
| Claims, worktrees, and session lifecycle | Root instructions plus the installed `scripts/meta/` entrypoints | Project Graph record `enforced-planning`; inspect current ownership with `python scripts/meta/check_coordination_claims.py --check --project <project>` and use the repository's sanctioned `make maintenance-worktree` / `make session-close` lifecycle |
| Cross-agent discovery and communication | [`2026-09-02-agent-coordination-systems.md`](./2026-09-02-agent-coordination-systems.md), [messaging comparison](../reviews/2026-09-15-agent-messaging-comparison.md), and [convergence decision D7](./ADR-2026-09-15-convergence-decisions.md#d7--answer-expected-agent-messages-go-through-the-coordination-mailbox) | Use the client-native live-agent list before assuming another session's state. Messages requiring an answer use `python scripts/meta/coordination_messages.py`; native messaging is the prompt nudge, while the mailbox is the durable obligation and acknowledgement record |
| Reusable learning | [`learnings/README.md`](../../learnings/README.md), [`learnings.md`](../../learnings.md), and immutable `learnings/entries/` | Project Meta owns the register; write only through `python scripts/log_learning.py`, normally via the shared `learned` skill |
| Failure-mode taxonomy | This row and the `agent-skills` Project Graph record | [`skills/review/references/failure-modes.md`](https://github.com/BrianMills2718/agent-skills/blob/main/skills/review/references/failure-modes.md) is canonical; run `python scripts/check_failure_mode_taxonomy.py` in `agent-skills` for structural consistency and inspect the shared feedback observation for reviewed/pending counts, oldest/newest pending IDs, and queue policy |
| Policy feedback and corrections | [`POLICY_SYSTEM_OPERATIONS.md`](./POLICY_SYSTEM_OPERATIONS.md), `policy_friction.md`, and `policy/proposals/` | Record friction or recommendations through `make policy-feedback`; human corrections are first-class evidence, and accepted durable rules move through the policy lifecycle rather than directly from a complaint into enforcement |
| Concerns and verified closure | [`ADR-2026-09-14-one-feedback-concern-lifecycle.md`](./ADR-2026-09-14-one-feedback-concern-lifecycle.md) | `scripts/concern_issue.py` owns keyed open/comment/reopen/close operations; evidence stays in its native store and the concern holds shared resolution state |
| Autonomous and continuous execution | Root `AGENTS.md`, [`ACTIVE_PLAN_QUEUE.md`](./ACTIVE_PLAN_QUEUE.md), and the Project Graph record for `enforced-planning` | The portable contract is `enforced-planning/docs/guides/CONTINUOUS_EXECUTION_CONTRACT.md`; authorization persists across reversible slices but does not expand scope, publication authority, or irreversible-action authority |
| Plans, priorities, and current authority | [`CURRENT_AUTHORITY_STACK.md`](./CURRENT_AUTHORITY_STACK.md), [`ACTIVE_PLAN_QUEUE.md`](./ACTIVE_PLAN_QUEUE.md), and [`docs/plans/INDEX.md`](../plans/INDEX.md) | Project Meta owns cross-project routing and generated current views; each implementation plan remains with its owning repository |
| Skills and procedures | [`SKILL_POLICY.md`](./SKILL_POLICY.md) and the capability/ownership registries | Project Graph record `agent-skills`; canonical skill authoring stays in its shared repository and client copies are derived |
| Capability access, custody, and recovery | `scripts/capability_custody_registry.yaml`, registry rows governing credentials and access, and the owning capability's Project Graph record | Project Meta stores identifiers, owners, canaries, and recovery routes, never credential values; verify the named canary or recovery path at the actual account/host boundary |
| Live system health | `make policy-system-status`, `make enforcement-liveness`, active claims, and owner-specific doctors | Probe the actual runtime boundary; configuration, source presence, registration, delivery, and execution are different claims |

The mailbox and native messaging are complementary. An answer-expected message
belongs in the durable mailbox so it can be acknowledged and audited; a native
Claude/Codex message may nudge the live recipient but is not the obligation's
source of truth. Claims likewise own write authority; a message never grants a
write path.

## What “one repository” means

Project Meta must contain enough information to understand and audit the whole
system without searching sibling repositories blindly. For every active
policy, the registry is expected to name:

- the governing source document and intent;
- its scope and enforcement classification;
- the actual mechanism, channel, script, command, or artifact;
- the feedback path and maintenance trigger; and
- any known gap between the claim and reality.

Implementation source stays with its capability owner. The boundary is:

- **Project Meta owns system meaning, navigation, registry truth, cross-project
  ownership, live-status entrypoints, feedback routing, and decisions.**
- **Capability repositories own executable implementations and local tests.**
  Today the main ones are `agent-skills` for shared skills and client hook
  declarations, `enforced-planning` for claims/session lifecycle, and
  `agentic-engineering-system` for the independent AES route.
- **Machine-local files are runtime state, not policy authority.** Live client
  configs, receipts, SQLite observations, and skill-feedback streams must be
  inspectable through commands documented here, but secrets, trust hashes, and
  ephemeral state do not belong in Git.

An external implementation with no registry row, owner, command, or gap is an
information-custody defect. A copied external implementation in this repo is
also a defect unless Project Meta has formally become its owner.

## How policy reaches an agent

Policy arrives through four distinct surfaces:

1. **Instructions** load durable workspace, repository, and subtree rules.
2. **Expected context** resolves task- and target-specific documents through
   repository relationships and leaves a delivery receipt.
3. **Skills** provide procedures an agent explicitly or automatically follows.
4. **Hooks and checks** observe, inject context, allow, block, mutate, notify,
   or verify at a lifecycle boundary.

The canonical cross-client distinctions and synchronization rules are in
[`INSTRUCTION_SURFACE_SYNC_POLICY.md`](./INSTRUCTION_SURFACE_SYNC_POLICY.md).
The generated or installed client copy is never sufficient evidence by itself:
use the Git-backed declaration, then probe the actual consumer boundary.

For a concrete Project Meta edit, run:

```bash
python scripts/prepare_expected_context.py \
  --target policy/registry.yaml \
  --action "understand and change one policy hook"
```

Continue until the command reports `DELIVERY COMPLETE`. Emission is not proof
that an agent used the content, and a configured hook is not proof that its
client executed it; those are separate observations.

## Operating the system

```bash
# Whole-system status: registry, generated views, channel liveness,
# observation stores, feedback, learnings, and scheduler.
make policy-system-status

# Fail when required lifecycle surfaces are not live.
make policy-system-status STRICT=1

# Verify the channels supporting declared hard policies.
make enforcement-liveness

# Validate registry structure and referenced mechanisms.
make policy-contract
make policy-references-check

# Regenerate the human views from the registry.
make policy-enforcement

# Record observed policy friction or a reusable recommendation.
make policy-feedback TYPE=friction ...
```

The status command is the current-state boundary. Do not copy its counts into
undated prose. As observed on 2026-09-16, it reported the overall system
`degraded`: 18 of 29 declared hard policies were on live channels, while the
session-hook channel was incomplete and the suite channel had no observable run
marker. Later readers must rerun the command rather than inheriting those
numbers as current.

## Maintaining informational completeness

When adding or materially changing a policy:

1. Update the nearest governing source document.
2. Update the policy's registry row in the same change.
3. Name external implementation owners and stable executable references rather
   than relying on an installed home-directory copy.
4. Regenerate the policy views.
5. Run the contract, reference, and relevant negative-control checks.
6. Exercise the real delivery or enforcement boundary with a case where the
   trivial outcome would be wrong.
7. Record friction, a correction, or a reusable learning in its native store;
   promote only accepted durable rules into the registry.

This page is the stable human entrypoint. The registry and linked authorities
own the underlying facts; generated views and runtime status remain derived.

---
schema_version: "1.0"
artifact_type: design_plan
id: worktree-lifecycle
status: proposed
method_conformance_receipt: proposals/worktree-lifecycle/PLAN.receipt.json
goal:
  profile: continuous-release
  owner: "coordinator:primary"
  report_deadline: "PT30M"
  transfer_trigger: explicit_handoff
  outcome: "New worktrees use the governed location; every existing worktree has a truthful, recoverable disposition."
  canonical_example: "Create an attention-manager maintenance lane, finish its change, then close its worktree and claim while retaining the remote work."
  forbidden_substitutes: "A lower folder count, expired claims, ancestor checks alone, or a green timer cannot prove safe closeout."
  boundaries: "Enforced Planning owns creation and claims; Project Meta owns discovery and sweeping. Preserve unique work and running dependencies."
  done_when: "Named acceptance runs prove placement, complete discovery, recoverable closeout, and visible partial failures."
  do_not_gate_on: "Zero worktrees, hosted CI, benchmarks, third-party permission, or completion of unrelated active lanes."
---

# Consistent worktree placement and recoverable closeout

Authorized scope: repair the existing creation and closeout tools, prove their behavior on a real lane, then resolve existing worktrees individually. Brian activated this mission through /goal on 2026-10-09. Implementation and cleanup wait for native plan adoption; neither has started. No new service, hosting, or paid infrastructure is proposed, and no delivery deadline is assumed.

## Actor and result

Brian should be able to finish a task without leaving an unexplained extra copy of its repository. For example, a new attention-manager task creates `attention-manager/worktrees/<branch>`. Finishing through `make session-close` removes that task's folder and live ownership claim together, after verifying its work remains recoverable. An unfinished task stays with a named owner, reason, and exact resume event.

A worktree is a separate folder of files for one task, connected to the repository's shared Git history. The standard folder inside the repository is intentional. Inconsistent placement and incomplete closeout are the concern; nesting by itself is allowed.

The desired result is consistent creation, complete discovery, and truthful closure. Active worktrees may remain. The visual review page explains the proposed mechanism; it is not a live inventory or evidence of implemented fixes.

## Requirements

All requirements R1–R6 in the this section are **planned and not yet run** against the repaired source or installed runtime. Each row names its acceptance run. These cover both Brian's explicit request and the delivered controls' claims: governed path placement, complete Git membership, preservation of data/history/ownership/runtime dependencies, native coherent closeout, visible partial failure, and authentic installed behavior. Every final release/completion record must carry any deferred requirement with its reason; a requirement is not satisfied by an older source test or a proxy.


| Requirement | Failure to prevent | Control / owner | Named run and required evidence | Status |
|---|---|---|---|---|
| R1: governed creation conforms | Explicit paths bypass the correct default | EP validates canonical repo and resolved target before mutation | `placement-regressions`: branch-with-slashes standard path succeeds; sibling, traversal and symlink escapes leave neither folder nor claim; authorized fixture exception remains scoped | Planned, not yet run |
| R2: all registrations appear | Sweeper skips repos without an internal worktrees folder | PM enumerates Git registrations for graph repos and joins canonical claim identities | `inventory-regressions`: assert exact standard, sibling-only, detached, missing, locked and fixture members; none silently disappear | Planned, not yet run |
| R3: preserve work and dependencies | Clean status or expiry is treated as disposal authority | EP preflight checks recovery, claim, tracked/untracked/ignored data and service dependencies | `preservation-regressions`: dirty work, unique commits, squash ambiguity, detached HEAD, ignored data, live ownership and a process using the folder each lead to specified retention or verified recovery | Planned, not yet run |
| R4: folder and claim close coherently | Generic release refuses managed claims; partial operations strand state | PM delegates managed closeout to EP; EP reconciles actual state with receipts | `closeout-regressions`: inject failure at every state transition, retry without false closure or lost work; competing claim update invalidates stale preflight | Planned, not yet run |
| R5: operational errors surface | Child fails while timer reports success | PM checks child exits, emits totals and the existing keyed concern | `sweep-failure-regressions`: failing repo named, state preserved, overall nonzero exit; ordinary deliberate retention distinguished from operational error | Planned, not yet run |
| R6: authentic consumer uses the repair | Source fixtures pass while installed runtime is old | Existing runtime installers and timer load verified revisions | `workspace-canary`: a real claimed maintenance lane creates, finishes, preserves remote work and closes through public Make targets; exact before/after membership changes only for that lane | Planned, not yet run |

R7 is host-governance compatibility: every runtime source change has an adopted plan, sanctioned exact-session claimed lane and accepted local merge checks; named check `claim-admission-and-local-gates`, status planned. It is a prerequisite for A–D rather than permission to change another writer's paths. This plan claims no new Git format, claim registry, capability catalogue entry, hosted CI, daemon or dashboard. Existing EP ClaimRecord/session-close, Git porcelain and PM sweep-result contracts remain the operative standards covered by R1–R6's producer/consumer tests.

## Success and disproof

The [October 8 investigation](https://github.com/BrianMills2718/project-meta/issues/1985#issuecomment-6072216350) found 60 existing linked worktrees and five missing registered paths. Forty-two used the standard layout; the other 18 include fixtures and possible exceptions, so they are not all established violations. Twenty-nine had tracked or untracked changes. These dated counts must be refreshed before selecting cleanup targets.

Acceptance is by exact membership and behavior, not a target folder count:



For full-trace acceptance, R1 is judged from `placement-regressions` (resolved targets, positive creation and rejected mutation state); R2 from `inventory-regressions` (exact registration identities and membership); R3 from `preservation-regressions` (bytes, history, owner and runtime dependency preflight); R4 from `closeout-regressions` (every mutation/retry state, recovery before removal and claim closure); R5 from `sweep-failure-regressions` (child error, preserved state, reported totals, concern and overall exit); R6 from `workspace-canary` (authentic public Make creation/work/remote readback/closure and exact installed revision); R7 from `claim-admission-and-local-gates` (adopted receipt, claim identity/paths, candidate diff and every local gate output/exit). All are planned runs. Read each named full trace, every failing or surprising case and a successful case before accepting its requirement; summary output alone is insufficient.


Every run retains commands/arguments, resolved paths, timestamps, source revision, stdout/stderr and exit status, claim IDs before/after, object IDs and remote readback, disposition receipts and inventory membership. Store sanitized full traces in each owner's existing run-artifact store and link them from the implementation plan and concern #1985. Read every failing or surprising trace and a successful case; inspect preservation before removal and removal before claim closure. Never publish private contents to prove preservation.

The authentic canary trace must show loaded module paths/revisions, exact remote object readback, and no unrelated lane changes. A documentation-only edit is exempt from an execution trace because it executes no behavior: its evidence is the committed diff, conformance check and rendered-page verification. This exemption never covers runtime slices.

Disproof: any unexplained new nonstandard path, omitted registration, unrecoverable unique work, service interrupted by removal, false closed claim, or unhandled child error with overall success. On any preservation failure stop further cleanup, retain remaining targets and repair the invariant.

## System model

The scoped model source is [SYSTEM_MODEL.md](SYSTEM_MODEL.md). The following synchronized evidence excerpt supplies the native adoption verifier with its actual observations; it is derived from that source, not an independently edited model. Both change in the same owning commit.


Scope: the existing EP/PM worktree control, a partial shared model rather than the full architectures of either repository. Git, claims and closeout retain their existing owners.

| Element | Kind / owner / representation | Required trace observation |
|---|---|---|
| Repository | Entity / PM graph, Git common directory | Canonical graph identity and actual common directory resolve to the same repo |
| Worktree | Entity / Git porcelain record | Exact path, HEAD, branch/detached, locked/missing state and before/after membership |
| Claim | Record / EP ClaimRecord | Native ID, owner, scope, freshness and target identity; competing update invalidates stale preflight |
| RuntimeDependency | Relationship / process and service configuration | Actual cwd/open files and configured paths, or explicit inspection failure; dependency prevents closure |
| DispositionReceipt | Record / EP closeout and recovery proof | Target, reason, remote readback/archive verification, mutation steps and final folder/claim state |
| SweepResult | Record / PM output and exit | Every repository outcome, retained/error distinction, child exits, totals and appropriate overall failure |
| Create admission | Process / EP creator and Make target | Resolved target checked before mutation; valid folder and claim together; refused target leaves neither |
| Discover | Process / PM graph plus Git enumeration | Exact standard, sibling-only, detached, missing and fixture members appear once |
| Preflight | Process / EP lifecycle owner | Fresh recovery, work, claim and dependency evidence leads to specified retain/close result |
| Close/reconcile | Process / EP session-close and safe remover | Recovery precedes removal; interrupted operations retry without false closure or data loss |
| Report | Process / PM sweep and existing concern | Partial error reaches output, exit and concern; deliberate retention stays visible |
| Inventory view | View / existing PM worktree/status surface | Every member exposes owner, evidence, disposition and next event; unknowns remain visible |

Relationships: Repository registers Worktree; Claim owns a lane at Worktree; RuntimeDependency requires Worktree; Preflight reads those identities plus recovery evidence; Close produces DispositionReceipt; Discover and Report produce Inventory view and SweepResult. PM invokes EP closeout instead of independently releasing managed claims.

Trace mapping: `placement-regressions` covers Repository, Worktree, Claim and Create admission; `inventory-regressions` covers Discover and Inventory view; `preservation-regressions` covers RuntimeDependency and Preflight; `closeout-regressions` covers DispositionReceipt and Close/reconcile; `sweep-failure-regressions` covers SweepResult and Report. `workspace-canary` connects these identities through the authentic lifecycle, while the service sentinel remains retained.

### Entry point, views and freshness

AES `wiki/index.md` remains the repository documentation entry point; the proposal index must link this partial model directly within two links. PM's own wiki entry point routes to the existing worktree/status surface. This model is discoverable there by its plan authority link, not a substitute whole-repository architecture.

The existing review page is a proposed lifecycle sequence sourced from this model; it omits live membership and dispositions because no runtime inventory is bound to it. PM's existing inventory/status view projects Git registrations joined to native claims and receipts; it must expose unavailable and partial states. Full EP/PM system architecture is outside this repair's partial model; no missing architecture is fabricated.

Before each slice, compare source/module revisions, canonical Git common directories, native claim identities and timer entrypoint with the model's named owners and contracts. Compare exact porcelain members with the inventory view and link each changed model element to its named acceptance run. A new producer, consumer, entity or close state without a mapped source, view and trace is model drift and blocks that slice's promotion. The source commit that changes such an element must update this model, affected view coverage and evidence links in the same change. All six named runs are planned; their later results are reported as observed only after full trace inspection. A successful source test cannot silently close missing installed evidence.

## Capability reuse

No catalogue entry fits, because these repairs need Git worktree placement, registered-worktree discovery, EP native claim/session closeout and the existing PM scheduled sweep; ACA's `reuse_candidates.yml` and `capability_registry.yml` have no capability providing those incumbent lifecycle seams. This plan extends EP/PM rather than adding a new cross-project capability. The first authentic consumer is the governed Make lifecycle and existing PM sweep timer, proved by `workspace-canary` and the scheduled report-only run.

## AES target

No AES target delta is proposed: `.aes/target.yaml`, `.aes/` state, `src/agentic_engineering_system/` and `tests/greenfield/` stay outside this plan's owned paths. AES stores the plan, model, evidence links and review page; EP/PM own the runtime subject. Decision 0010 retains Enforced Planning as incumbent for this non-v0.2 operational material.

| Requirement | AES normative mapping / verification subject |
|---|---|
| R1 | `AP-REQ-001` / `SC-AP-001` govern its planned source commit; subject EP creator/Make admission, `placement-regressions` |
| R2 | `AP-REQ-001` / `SC-AP-001` govern its planned source commit; subject PM Git-registration discovery, `inventory-regressions` |
| R3 | `AP-REQ-001` / `SC-AP-001` govern its planned source commit; subject EP preservation preflight, `preservation-regressions` |
| R4 | `AP-REQ-001` / `SC-AP-001` govern its planned source commit; subject EP close/reconcile and PM delegation, `closeout-regressions` |
| R5 | `AP-REQ-001` / `SC-AP-001` govern its planned source commit; subject PM child outcome/output/exit/concern, `sweep-failure-regressions` |
| R6 | `AP-REQ-001` / `SC-AP-001` govern its planned source commit; subject installed Make runtime and PM timer runtime, `workspace-canary` |
| R7 | `AP-REQ-001`, `SC-AP-001`: staged exact path/tag/receipt checks; verification subject is each claimed source commit and its adopted-plan receipt, plus local repository checks |

The AP mapping is a governance constraint on all planned changes, not a claim that an AES product item specifies external EP/PM behavior. No `aes plan validate` target proposal is needed because no target requirement, success criterion, realization or running AES artifact changes. This is an explicit scoped mapping, not a claim that AES product evidence verifies EP/PM behavior.

## Authority and non-goals

Brian requested this plan. His workspace rules and Project Meta's Project Organization Policy govern placement and preservation. EP owns creation, coordination claims and session close. PM owns project registration, discovery, scheduled sweeping and failure reporting. AES stores this proposal and review page; runtime ownership stays with EP/PM.

This plan changes no worktree policy. Brian authorized implementation through the active /goal; its native Company Planning adoption decision and receipt govern admission before the first runtime source change. Execution then uses claimed lanes in the owning repositories. Repository-specific authority, including read-only restrictions, remains binding.

Non-goals: zero worktrees; age-based deletion; treating every alternative layout as a violation; rewriting history; moving all repos; a replacement claim store; another daemon, CLI or dashboard; deployment-host changes; or taking over other sessions' unfinished work.

## Irreversible actions and spend

No irreversible action or new spend is proposed. A selected linked folder closes only after every valuable byte and required Git object has verified durable recovery, ownership has a disposition, and runtime dependencies are clear. A local bundle alone is insufficient. Secret-bearing or ignored data needs the owning protected archive with readback, not a Git push; unavailable preservation means retain.

Deleting unique data/history, abandoning unrecoverable changes, publishing private material, or stopping another task's service is excluded. If a later case requires one, retain that exact target and route the specific irreversible decision to Brian. Ordinary recoverable closure uses existing authority. The main risk is incorrect removal; conservative retention and object-level recovery checks contain it. Deferring the repair preserves today's accumulation risk.

## Uncertainties

Still unresolved, with safe dispositions:

| Question | Owner / resolving evidence | Until resolved |
|---|---|---|
| Which alternative paths are fixtures or exceptions? | PM lane checks each Git identity, graph entry and owning policy | Unclassified; no relocation or deletion |
| Which expired claims still represent active work? | EP lane checks fresh native discovery, heartbeat and reachability | Expiry never authorizes closure |
| Which clean heads are squash-integrated or unique? | EP lane checks integration proof or exact remote recovery readback | Retain undecidable work |
| Which ignored files or services depend on a folder? | Owning lane checks process cwd/open files and configured unit/script paths | Retain dependent or uninspectable paths; service migration is separate |
| Which installed clients need updating? | EP traces actual Make/Claude/Codex module paths; PM reads timer runtime | No rollout claim from source tests alone |
| Do earlier plans own unfinished repairs? | Integration owner checks fresh claims and exact open items in PM 212/234/259 and #2382 | Reuse owned work; avoid duplicate lanes |

These are bounded execution preflights, not open design questions for Brian. Refresh baseline and ownership before each target mutation.

## Activation facts

Route: `repair`, because failure is reproduced and existing repair seams are identified. [path-decision.json](path-decision.json) records route facts. concurrent_writers=false for the execution scope: one coordinator implements units A–D sequentially with no child writer dispatch. Independent ecosystem writers remain protected collision surfaces, not contributors whose work this plan integrates.

shared_mechanism=true, crosses_system_boundary=true, deploys=true: shared lifecycle contracts and installed scheduled consumers change. Consequential-boundary checks remain active; multiple-writer applies only on future concurrent writer admission. empirical_comparison_proposed=false: required-behavior regression checks are not a comparative benchmark. llm_central=false: runtime uses deterministic Git/claim contracts; planning verification does not create a product model dependency. irreversible_or_spend_action=false: unrecoverable deletion and new paid resources are excluded. claims_external_standard=true: the consumer claims conformance to Git porcelain and existing EP/PM lifecycle contracts, verified by the requirement-linked checks. aes_governed_target=true is derived from the AES storage host, whose product target is unchanged.

## Prior art and ownership

| Candidate inspected | Disposition |
|---|---|
| [Official Git worktree documentation](https://git-scm.com/docs/git-worktree): registered inventory, remove/move/repair and locked/detached states | Reuse Git primitives. Metadata pruning cannot substitute for preserving and closing an existing working folder |
| EP creator, session-close, safe remover and claim library | Extend existing owners; resolved path validation and preservation checks |
| PM sweeper, merged-worktree pruning, concern #1985 and four-hour timer | Extend discovery, delegate managed closure, propagate operational errors; no parallel sweeper |
| PM plans 212, 234, 259; EP plan 59; concerns #2382, #2157, #2275 | Compose completed controls and remaining owned work; supply observed missing acceptance cases rather than blanket replacement |
| `vision/legacy/project-meta-vision/ARCHITECTURAL_IDEAS.md`: canonical-path guard, typed mutation receipts and scoped claims | Reuse identity, receipt and narrow-ownership patterns |
| ACA `reuse_candidates.yml` and `capability_registry.yml` | Bounded exception: no catalogue entry fits, because Git creation/claims/closeout already belong to EP/PM rather than approval, notification or document capabilities; retain incumbent implementations |

Evidence source pins: PM `eb27da46b7795d9db15cf60162c82f85c58d3c98`; EP `761cab45a003786d4fde99a5af44a692eae40b6d`; Company Planning `3b788317927d28d6e7cf442ffc741172c8d76038`. Reconcile newer changes at admission; these pins do not request rollback.

Parallel-implementation check: trace public creation/close Make targets and the timer to loaded owner modules; inspect registered scheduled units and consumer entrypoints for competing mutation paths. The real canary and scheduled dry run must use EP's same closeout owner. A separate remover or claim store fails the check.

## Coordination

Integration owner: Codex session `codex:01a11e1e-21f8-7f22-a467-a25b56fffe8c`. The authoring claim is the sanctioned AES `worktree-lifecycle-adoption` lane and owns only `proposals/worktree-lifecycle`. Implementation remains sequential: one narrowed claimed lane at a time in PM/EP; no concurrent child writers are admitted. The native execution cursor in the admitted PM lane is the sole current progress authority; this plan owns design and acceptance, and the mission goal owns loop boundaries. No parallel progress diary is introduced. Authority transfers only by explicit handoff, never by claim expiry or silence.

Fresh native claim checks on 2026-10-09 showed no PM write claims; the EP `mailbox-isolated-delivery` writer owns coordination-hook/messages code and its tests, outside B's creator/closeout surface. AES `capability-catalogue` owns the root wiki and its catalogue surfaces; `feedback-prevention` owns the proposal index, project brain and AES-root execution cursor; `rules-sort` remains handed off with its exact six rule paths. None contributes implementation under this plan. Their missing formal work-unit metadata is neither an adoption requirement for this sequential plan nor a transfer of their custody. A native message to `feedback-prevention` acknowledged navigation coordination: it will add the proposal-index link after this plan reaches main; its claimed paths remain excluded here. Refresh claims and actual module revisions at each slice admission.

If parallel implementation is later useful, revise the activation fact and re-adopt with an admitted native work-unit record for every actual writer before dispatch. Each record must name narrowed paths, dependencies, integration evidence and owner. Claims own writes; messages supply coordination only.

| Sequential unit | Exact ownership / conflict surfaces | Dependency and review point |
|---|---|---|
| A: complete inventory and honest results | PM `scripts/sweep_lifecycle_residue.py`, `scripts/prune_merged_worktrees.py`, focused tests and owning docs | First slice; existing status surface exposes all exact Git members and retained/error outcomes. Newly discovered legacy targets stay report-only; unchanged safe eligibility controls remain in place |
| B: guarded creation and recoverable closure | EP `scripts/worktree-coordination/create_worktree.py`, `scripts/session_close.py`, safe remover, claim library only if necessary, focused tests/docs | Uses A's identity cases; reconcile #2382 ownership first. Land compatible closeout support before PM delegation or widened automatic eligibility |
| C: installed consumer proof | PM sweeper delegation/integration tests; EP existing runtime installer and module sync | Depends on B. Prove the authentic lifecycle and timer dry run. Existing portfolio service dependency remains retained |
| D: resolve legacy members | PM integration lane selects exact targets; owning repo lanes claim and close | Depends on C. Every member gets retained, integrated, recovered, fixture-exempt or missing-metadata disposition with evidence and next event |

Each unit is a reversible checkpoint: narrowed claim, source change, focused evidence, current owning docs, local merge checks and pushed recovery revision. Native work-unit metadata is recorded at admission; do not create all worktrees in advance. Depend on an existing writer's evidenced repair instead of duplicating it.

## Boundaries

Disposition: preserve and incrementally repair. Legacy paths stay readable. New arbitrary production paths are rejected; explicitly scoped fixtures remain distinguishable. No bulk automatic relocation. Existing checkout moves/closures follow PM's organization policy after individual disposition.

PM discovers candidates; EP owns managed lifecycle mutations. A failed EP call stays unresolved, with no fallback generic claim release. Rollback reverts the owning source commit and restores the installed revision; preserve recovery refs, and resume partial closure from actual state rather than inventing a live claim.

The existing portfolio worktree used by a running service is a preservation sentinel: recognize and retain it. Service migration needs its own verified deployment/rollback lane. Public review contains sanitized control evidence only; secret scan and approved light-model prose screening precede publication. Raw private claim narratives and file contents remain protected.

## Contracts and dependencies

| Boundary | Native contract / owner | Change and producer-to-consumer order |
|---|---|---|
| Git to EP/PM | Git `worktree list --porcelain -z`, refs and object IDs | No Git format change; parse registration including detached/missing/locked states before claim join |
| Make to EP creation | EP creator and creation result: repo, branch, resolved path | Validate before mutation; standard callers unchanged; arbitrary explicit callers get scoped exception or actionable refusal |
| PM to EP claims | EP `enforced_planning/coordination_claims.py` ClaimRecord and check CLI | Preserve registry/native IDs; additive fields only if required, reader first; no PM replacement schema |
| PM to EP close | EP `scripts/session_close.py` and `scripts/worktree-coordination/safe_worktree_remove.py`: disposition, reason, recovery_ref, merge evidence, receipt | Reuse supported values. Add compatible result/readers in EP, verify old callers, then switch PM. Unknown results retain |
| Sweep to health/concerns | PM result/output/exit and `scripts/concern_issue.py` key `audit-step:10` | Add per-repo outcomes and totals; adapt health readers before errors fail overall; ordinary retention is distinct |
| Source to installed runtime | EP `scripts/update_installed_runtime.py`; PM existing unit/runtime checkout | Tests, pushed revision, installed provenance, real canary, timer dry run, then narrowly enabled cleanup |

Contract locations and explicit roles: Git owns [worktree porcelain](https://git-scm.com/docs/git-worktree#_porcelain_format) and produces registrations; PM `scripts/sweep_lifecycle_residue.py` and EP `scripts/worktree_paths.py` consume them. No Git producer changes; update/test consumers first. Governed repository Make targets produce creator arguments; EP `scripts/worktree-coordination/create_worktree.py` owns and consumes the creation contract, and its creation result is consumed by those targets. Land backward-compatible creator changes before enabling stricter explicit-path callers.

EP `enforced_planning/coordination_claims.py` produces and owns native ClaimRecord; EP `scripts/check_coordination_claims.py` exposes it and PM sweeper consumes the canonical identity view. EP readers support additive identity first, then PM consumes it. PM sweeper produces close requests; EP `scripts/session_close.py` consumes them and produces disposition results consumed by PM. EP adds compatible result support before PM switches. PM owns and produces sweep result/output/exit in `scripts/sweep_lifecycle_residue.py`; PM `scripts/check_scheduled_unit_health.py`, systemd `project-meta-lifecycle-sweep.service`, and `scripts/concern_issue.py` consume its outcome. Adapt those consumers before changing error semantics.

EP `scripts/update_installed_runtime.py` owns and produces installed revision metadata consumed by both client entrypoints; PM owns the unit at `~/.config/systemd/user/project-meta-lifecycle-sweep.service`, which produces the runtime invocation consumed by PM sweeper. Change status: installed revision metadata format is unchanged; EP installer invocation contract is unchanged; PM systemd runtime invocation contract is unchanged in this design. Only the executed source revision changes. Any later required unit-contract change must first revise this plan and its compatible consumers. Push verified producer code, install/update the runtime, then verify the exact loaded revision from the consumer before eligibility expands.

Use each owner's existing typed contract style; validate additive/versioned output and reject unknown destructive dispositions. Enumerate authentic callers and add compatibility fixtures before changing a schema. This table does not authorize speculative new schemas.

## Standard conformance

The claimed standards are Git's official `worktree list --porcelain -z` format and EP/PM's existing native lifecycle contracts. Git specification owner and location: https://git-scm.com/docs/git-worktree#_porcelain_format; no producer format change. `inventory-regressions` verifies exactly parsed path, HEAD, branch/detached, locked/prunable state and record membership, including nonstandard registrations. EP ClaimRecord owner/location: `enforced-planning/enforced_planning/coordination_claims.py`, consumed by its native check CLI and PM; `preservation-regressions` and `closeout-regressions` verify canonical identity, fresh ownership, safe refusal and closed state. Native close contract owner/location: EP `scripts/session_close.py` and `enforced_planning/session_lifecycle.py`; closeout tests and canary verify compatible disposition, recovery and coherent final folder/branch/claim state. PM sweep contract owner/location: PM `scripts/sweep_lifecycle_residue.py`; `sweep-failure-regressions` verifies child failures, totals and overall exit. Git does not publish a machine-readable JSON Schema for the porcelain output; its official written porcelain-field, record-separator and quoting rules are the specification encoded by the parser fixtures. EP supplies native typed ClaimRecord and lifecycle-disposition contracts; use their actual validators and source-defined accepted fields rather than inventing a parallel schema.

These checks enter the local integration gate before each affected commit lands: PM `python -m pytest tests/test_sweep_lifecycle_residue.py tests/test_prune_merged_worktrees.py` and its native `make check`; EP `python -m pytest tests/test_create_worktree.py tests/test_safe_worktree_remove.py tests/test_session_cli.py tests/test_worktree_paths.py` and `python scripts/self_test.py`. Unit C additionally gates promotion on the authentic public Make canary and scheduled report-only invocation. These commands are planned, not reported as having passed yet; they are the required merge/promotion steps rather than optional after-the-fact checks.

Disproof case: feed an output labelled conforming with a omitted registered detached/missing member, malformed record separator or mismatched claim repository identity; parser/identity checks must refuse it or visibly mark unavailable and exit nonzero where operational, never silently return a conforming inventory. Additions beyond Git's format—claim joins, recovery/owner/reassessment dispositions and service dependency labels—are explicitly labelled EP/PM extensions in the inventory/result artifacts and this plan; they are not claimed as Git porcelain fields.

Status for every listed conformance check: planned, not yet run on the repaired runtime. No claim is made that existing source fixtures already prove installed conformance.

## Deployment

EP target: installed Codex runtime and sanctioned lifecycle modules used by both clients. Existing route: `make install-codex-runtime RUNTIME_REVISION=<pushed-revision>` / `scripts/update_installed_runtime.py`. In B, resolve the actual Claude consumer and existing sanctioned module-sync command, record and verify it before promotion. Until that command and rollback are known, that consumer stays unpromoted; no invented route. Live check: public Make commands show loaded paths/revisions and complete the canary. Rollback reinstalls the previous verified remote revision retained by the installer.

PM target: `project-meta-lifecycle-sweep.service`'s existing runtime checkout. The current unit fetches origin, checks out detached `origin/main`, then invokes `scripts/sweep_lifecycle_residue.py --apply --quiet`. Promotion is a checked local merge/push to PM main; no new service. First verify the pushed revision using report-only execution in that runtime, full membership and injected-error reporting. Only then allow a normal scheduled run after C's eligibility proof. If needed, hold only this timer during cutover, record/restore its prior enablement; never stop a repository service.

PM rollback: revert the specific source commit, push, verify the next fetched revision and dry-run outcome, retain unresolved targets. If a unit changed, restore its recorded file, run `systemctl --user daemon-reload`, and restore the timer's prior state. Inspect the full append log and child exits, rather than relying on systemd success alone.

Concrete promotion commands, run by the implementation owner after local gates: `git push origin main` in PM publishes the checked source; `systemctl --user start project-meta-lifecycle-sweep.service` executes the existing update/invocation route only after report-only preflight and C pass. Read `git -C <runtime-checkout> rev-parse HEAD` and its full invocation trace to prove the executing source equals the pushed commit; record the output and result in the existing append log. For EP, `make maintenance-worktree BRANCH=<canary> MAINTENANCE_BOOTSTRAP_WRITE_PATHS="<owned-paths>"` and `make session-close BRANCH=<canary>` are the live public consumer commands: verify their loaded owner-module revision equals the installed pushed revision, rather than treating the installer exit as proof. Placeholders resolve to exact admitted paths/branches before execution; these commands are not being run by the proposal.

## First implementation boundary

Start with A's read-only inventory/error contract and the existing status surface. Then B proves guarded operations, C proves the installed real consumer, and D performs verified target-by-target cleanup. Cleanup never serves as the experiment for whether preservation works.

Complete means R1–R6 hold and every refreshed baseline member has verified closure or a truthful retained disposition with owner/resume event. Retained active work is valid. An unexplained leftover, hidden failure, or unrecoverable removal is not.

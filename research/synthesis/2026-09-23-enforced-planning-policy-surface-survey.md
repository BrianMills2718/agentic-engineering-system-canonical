# Enforced Planning policy decision surface survey

Snapshot: AES canonical `25d6305ac75439343046c9294e3e4e51c84b480c`
Date: 2026-09-23
Purpose: inventory current deterministic and semantic decision surfaces before adding another policy engine or model evaluator.

This is a descriptive survey. It does not change active policy, authorize Plan 002 execution, or create a new runtime.

## Executive finding

Enforced Planning already has most of the machinery normally associated with a policy engine:

- typed request and decision contracts;
- stable reason codes;
- fail-closed handling of stale/missing evidence;
- exact repository/revision/claim binding;
- append-only receipts;
- explicit defer/human-decision states;
- bounded recovery leases/actions;
- permitted-next-action sets;
- semantic review with typed `pass | fail | inconclusive`, evidence references, rationale, negative controls, and exact revision binding.

The biggest inconsistency is not missing policy intelligence. It is the path from an internal decision to a uniformly actionable agent-facing problem:

```text
facts
  -> deterministic policy / semantic criterion
  -> typed result
  -> reason
  -> evidence
  -> recovery
  -> agent-facing feedback
```

Some current surfaces already provide the whole chain. Others expose only a reason code or generic exception string.

## First-principles policy goals

The current code implies these goals:

1. Do not let stale, missing, ambiguous, or mismatched evidence become success.
2. Bind decisions to exact repository/session/claim/outcome state.
3. Keep mutation inside owned scope.
4. Keep completion distinct from partial progress or green-but-incomplete checks.
5. Preserve safe inspection/evidence operations even when productive mutation is blocked.
6. Route human-only questions to humans instead of pretending the system can decide them.
7. Make recovery bounded and explicit.
8. Keep semantic judgment separate from deterministic custody, revision binding, and final enforcement.

These are appropriate goals for an engineering-governance system.

## Decision-family matrix

| Surface | Non-allow result vocabulary | Inputs/evidence | Recovery already present? | Semantic judgment needed? | Survey disposition |
| --- | --- | --- | --- | --- | --- |
| Pre-write claim gate | `deny`, `observe_violation` | session identity, Git worktree, branch, projected claims, target paths | **Yes**, often exact recovery text | No | Keep Python; normalize output envelope |
| Session target resolution | typed resolution errors | native session/agent identity, projected claim, live Git identity | Indirect through pre-write wrapper | No | Keep |
| Outcome admission | `deny`, `defer` | selected outcome, portfolio allocation, continuation state, scope | Partial; reason/error available, user message often generic | No | Keep; add uniform recovery mapping |
| Selection-pending activation | `defer` or fail-closed denial | exact staged claim, authority, tracker absence, binding | Error message exists | No | Keep |
| Outcome continuation | `allowed=false` plus permitted next actions | lease, contract, requested operation, optional recovery lease | **Yes**, action classes are first-class | No | Keep; surface actions more directly |
| Review readiness | `review_ready=false` | criterion coverage, artifact identity, review transition | Missing criterion IDs available | Usually no; semantic criterion production may be separate | Keep |
| Goal completion | `accepted=false` | contract, lease, execution projection, evidence revision | Missing item/criterion IDs on several paths | No for state/custody; semantic evidence quality may be upstream | Keep |
| Native Stop/completion gate | `allow_stop=false` | exact claim, selected outcome, retained completion, current lease | Human-readable summary on key paths | No | Keep |
| Blocker disposition | `continue_ready_work`, `integration_wait`, `blocker_unverified_return_control`, `human_decision_required`, `goal_blocked_verified` | work graph, ready queue, blocker request, claims, mailbox/path-conflict evidence | Resume event + claim action + alternatives/evidence | No | Strong existing model; surface it consistently |
| Artifact creation | `deny` / `observe_violation` | path, artifact registry, directory policy, intent | **Yes**, explicit recovery string | No | Keep |
| Plan validation | integrity `pass/fail` + findings | exact plan bytes + config | Findings identify missing/invalid structure | No for structure | Keep |
| PR semantic review | semantic `pass/fail/inconclusive` + findings | exact head SHA, rubric, evidence, programmatic checks | Rationale/evidence refs; final signoff deterministic | **Yes** | Reuse before adding a second semantic-judgment framework |
| Session continuity | bounded resume/offer states | claim/session/transcript/activity state | State-specific next behavior | No | Keep |
| Push/integration safety | path/blocking coordination states | live claims, overlap paths, branch/worktree state | User-facing guidance exists | No | Keep |

## Detailed reason-code survey

### A. Pre-write claim / session targeting

These decisions protect mutation ownership and worktree/session identity.

| Reason code | Meaning | Current recovery shape | Semantic? |
| --- | --- | --- | --- |
| `unsupported_client` | hook client is not admitted | configuration/programming correction | No |
| `session_identity_unavailable` | no native agent/session identity | restore valid hook/session identity | No |
| `client_identity_mismatch` | native identity prefix disagrees with client | fix identity source | No |
| `projection_unavailable_or_stale` | claim authority projection cannot be trusted | refresh exact projection | No |
| `claim_not_healthy` | matching claim exists but custody/state is invalid | repair/resume claim | No |
| `claim_git_identity_mismatch` | claim's worktree/repo/branch differs from live Git | repair worktree/claim binding | No |
| `target_worktree_not_claimed` | requested target belongs to no session claim | create/resume correct claim | No |
| `no_exact_session_target` | session has no healthy exact target | create/resume exact lane | No |
| `ambiguous_exact_session_target` | multiple healthy targets match | reconcile duplicate/overlapping lanes | No |
| `repository_identity_unavailable` | request is not attributable to governed Git identity | run from named branch/governed worktree | No |
| `bash_runtime_workdir_unattested` | mutation shell cwd cannot be proven | re-run with explicit `-C` / bound cwd | No |
| `bash_target_unprovable` | shell expansion prevents proving target paths | use literal paths | No |
| `bash_path_outside_worktree` | command touches paths outside owned worktree | split read-only inspection or mutate in claimed lane | No |
| `no_exact_claim` | no claim covers the mutation | create/resume exact claimed lane | No |
| `ambiguous_exact_claim` | multiple claims individually authorize the same request | reconcile overlapping claims | No |
| `path_outside_claim` | mutation is outside declared write scope | update scope or use separate lane | No |

This family is already a strong example of actionable policy output: several denial paths contain exact recovery strings.

### B. Outcome admission and staged activation

| Disposition / reason | Meaning | Evidence/context | Recovery implication | Semantic? |
| --- | --- | --- | --- | --- |
| `defer / cross_repository_membership_not_promoted` | calibration state is not production authority | admission request | do not promote automatically | No |
| `deny / ordinary_authority_denied` | underlying ordinary control already denied | ordinary admission state | fix the ordinary denial first | No |
| `deny / admission_bootstrap_scope_violation` | first allocation tries to write outside sanctioned bootstrap paths | requested write paths | narrow bootstrap scope | No |
| `deny / admission_bootstrap_state_invalid` | bootstrap portfolio state is inconsistent | typed portfolio state | repair state/config | No |
| `deny / portfolio_allocation_required` | selected work lacks exact portfolio allocation | portfolio ledger | allocate/select correctly | No |
| `deny / portfolio_slot_occupied` | bounded portfolio/WIP slot belongs elsewhere | portfolio ledger | wait/reselect/resolve owner | No |
| `deny / portfolio_allocation_inactive` | allocation is disposed/inactive | portfolio ledger | reselect/reallocate | No |
| `deny / portfolio_allocation_mismatch` | allocation binding/digest does not match | exact allocation evidence | refresh exact binding | No |
| `deny / out_of_scope` | operation target is outside selected outcome scope | contract + target path | use allowed scope or revise plan | No |
| `deny / recovery_required` | ordinary product mutation is blocked until recovery | continuation lease | perform bounded recovery | No |
| `deny / outcome_stalled` | repeated failure has moved lease to stalled | continuation lease | inspect/evidence/recovery/human action | No |
| `deny / outcome_terminal` | outcome is already terminal | lease | do not continue product mutation | No |
| `deny / outcome_selection_required` | no exact selected outcome exists | selection owner | select/activate outcome | No |
| `deny / outcome_admission_state_invalid` | admission cannot derive a supported state | exact resolution error attached | repair specific resolution error | No |
| `defer / selection_pending` | a valid staged reservation may create its first tracker | exact staged evidence | attach tracker then continue normal admission | No |

Selection-pending denials use `outcome_admission_state_invalid` as the public reason and preserve a more specific resolution code. Current specific codes include:

- `selection_pending_identity_incomplete`
- `selection_pending_claim_version_invalid`
- `selection_pending_write_scope_missing`
- `selection_pending_tracker_already_linked`
- `selection_pending_plan_authority_invalid`
- `selection_pending_goal_authority_mixed`
- `selection_pending_start_revision_invalid`
- `selection_pending_claim_source_unavailable`
- `selection_pending_claim_source_changed`
- `selection_pending_claim_not_live`
- `selection_pending_claim_invariants_invalid`
- `selection_pending_binding_unresolvable`
- `selection_pending_binding_mismatch`

These are all deterministic validation/custody failures.

### C. Review readiness, goal completion, and continuation

#### Review readiness

| Reason | Meaning | Useful recovery data already present? | Semantic? |
| --- | --- | --- | --- |
| `criterion_contract_not_configured` | current contract version cannot use this readiness path | contract version | No |
| `artifact_rejected` | exact artifact is already rejected | artifact SHA | No |
| `criterion_evidence_missing` | one or more frozen success criteria lack evidence | **Yes: missing criterion IDs** | Evidence quality may be semantic upstream |
| `review_transition_not_recorded` | criteria may pass but review state transition was not recorded | artifact + lease | No |

#### Goal completion

| Reason | Meaning | Recovery signal | Semantic? |
| --- | --- | --- | --- |
| `completion_proposal_collision` | reused proposal ID has different bytes | issue fresh/correct proposal | No |
| `outcome_already_complete` | completion requested after terminal completion | stop mutating/close out | No |
| `completion_contract_mismatch` | proposal is bound to different outcome contract | regenerate from current contract | No |
| `execution_projection_contract_mismatch` | execution projection belongs to different contract | refresh projection | No |
| `completion_lease_stale` | proposal expected an older lease | retry from current lease | No |
| `completion_projection_stale` | proposal references old execution projection | refresh and retry | No |
| `completion_evidence_stale` | evidence revision is not current | re-verify current artifact | No |
| `execution_criterion_unknown` | execution projection names criteria outside contract | fix projection/contract mapping | No |
| `criterion_not_represented` | contract criterion has no execution item | add representation or revise plan | No |
| `execution_items_incomplete` | one or more execution items are incomplete | **Yes: missing item IDs** | No |
| propagated review reason | review is not ready | missing criterion IDs / review state | Maybe semantic evidence production upstream |

#### Operation admission / recovery

| Reason | Meaning | Current next-action support | Semantic? |
| --- | --- | --- | --- |
| `recovery_not_required` | recovery action requested while active | `ACTIVE_NEXT_ACTIONS` | No |
| `out_of_scope` | target not inside allowed contract/recovery scope | action classes + contract scope | No |
| `recovery_lease_missing` | recovery state lacks required lease | `RECOVERY_NEXT_ACTIONS` | No |
| `recovery_contract_mismatch` | recovery lease belongs to another contract | `RECOVERY_NEXT_ACTIONS` | No |
| `recovery_parent_mismatch` | recovery lease is stale against current parent lease | `RECOVERY_NEXT_ACTIONS` | No |
| `recovery_action_mismatch` | requested recovery action is not the authorized one | `RECOVERY_NEXT_ACTIONS` | No |
| `recovery_path_mismatch` | recovery target path is outside bounded recovery scope | `RECOVERY_NEXT_ACTIONS` | No |
| `recovery_required` | normal mutation is blocked until bounded recovery | inspection/replay/evidence/closeout/recovery | No |
| `outcome_stalled` | repeated same-boundary failure exceeded threshold | same recovery action classes | No |
| `outcome_complete` | selected outcome is complete | terminal/passive action classes | No |
| `outcome_parked` | outcome was deliberately parked | terminal/passive action classes | No |

The continuation subsystem already contains the strongest reusable recovery pattern in the repository: stable state + reason code + explicit permitted action classes.

### D. Native Stop / outcome completion

| Reason | Meaning | Current feedback | Semantic? |
| --- | --- | --- | --- |
| `outcome_completion_mode_invalid` | completion configuration is malformed | detailed summary | No |
| `exact_claim_unavailable` | exact live session claim cannot be resolved uniquely | count/detail in summary | No |
| `canonical_outcome_incomplete` | selected outcome has no single accepted completion | summary tells agent to continue against frozen success criteria | No |
| `completion_evidence_stale` | progress changed after retained completion evidence | summary says re-verify current artifact | No |
| propagated selection/lineage error | exact selected/canonical state could not be reconstructed | exception code + message | No |
| `canonical_outcome_complete` | allow Stop | positive summary | No |

This path does not need an AI judge to decide freshness/completeness. The only potentially semantic question is upstream: whether evidence should count as satisfying a criterion.

### E. Blocker policy

The blocker subsystem is not binary. It already distinguishes five useful dispositions.

| Decision | Reason codes | Meaning / action | Semantic? |
| --- | --- | --- | --- |
| `continue_ready_work` | `eligible_alternative_exists` | claimed blocker does not stop the goal; do other ready work | No |
| `integration_wait` | `path_conflict_verified_local`, `active_unit_in_progress` | wait for an evidenced local integration dependency | No |
| `blocker_unverified_return_control` | `path_conflict_evidence_unverified`, `queue_coverage_unavailable`, `blocked_item_not_in_queue`, `requested_unit_not_blocked_in_queue`, `queue_contains_active_or_indeterminate_state`, `queue_has_no_blocked_units`, `mailbox_delivery_below_required`, `unsupported_or_unknown_blocker` | do not accept blocker claim; return control and fix evidence/state | No |
| `human_decision_required` | `named_human_decision_required` | system explicitly routes decision to a human | **Human**, not model authority |
| `goal_blocked_verified` | `complete_queue_no_eligible_unit` + `supported_blocker:<class>` | whole goal is actually blocked by a supported evidenced condition | No |

The result also retains:

- alternative work-unit IDs;
- claim action;
- evidence references;
- resume event.

This is already close to the desired blocker contract.

### F. Artifact creation

| Reason | Meaning | Current recovery | Semantic? |
| --- | --- | --- | --- |
| `directory_not_allowed` | no controlled-directory rule permits the new path | update existing owner or register allowed artifact | No |
| `intent_missing` | controlled new artifact lacks registry intent | explicit registration/update guidance | No |
| `intent_invalid` | registered intent violates artifact policy | detailed violations | No |
| `retained_artifact_invalid` | retained artifact no longer satisfies registry/policy | repair record/artifact | No |
| aggregate `artifact_policy_violation` | at least one target violates policy | explicit recovery string | No |

This family already has the desired shape: typed decision + specific reason + detail + recovery.

### G. Plan validation

Structural plan failures are deterministic. Representative findings include:

- `missing_user_outcome`
- `invalid_canonical_behavioral_example`
- `missing_critical_path_classification`
- `missing_capability_adoption_disposition`
- `missing_acceptance_criteria`
- `missing_epistemic_frontier`
- `invalid_frontier_headers`
- `invalid_frontier_state`
- `missing_reassessment_contract`
- `invalid_reassessment_contract`
- `missing_landscape_disposition`
- `missing_landscape_reference`

These are contract/structure checks. Whether the *content* is strategically good is a different semantic/human review question.

### H. Semantic PR review

This is the existing semantic-judgment mechanism.

A review spec contains:

- exact base/head SHA;
- programmatic checks;
- semantic rubric;
- required evidence per criterion;
- negative control per criterion;
- one or more review lanes.

The model returns typed:

```text
pass | fail | inconclusive
+ criterion results
+ evidence refs
+ rationale
+ blocking/advisory findings
```

Final signoff remains deterministic and exact-revision bound.

This is the first place to reuse/generalize if AES needs semantic judgment about whether evidence supports a claim.

## Failure-mode survey

The current policy system already addresses most important engineering-policy failures:

| Failure mode | Current handling |
| --- | --- |
| stale evidence | explicit stale reason codes and SHA/revision checks |
| missing evidence | missing criterion/item IDs |
| wrong scope | exact path/claim/outcome scope checks |
| ambiguous authority | ambiguity blocks rather than combines authority |
| replay/collision | proposal/transition IDs and digest checks |
| invalid current state | fail-closed state-invalid paths |
| missing human decision | explicit `human_decision_required` |
| repeated failed recovery | lease moves to recovery/stalled states |
| unsafe artifact sprawl | artifact creation gate + registry intent |
| model semantic uncertainty | existing `inconclusive` semantic review state |
| provider/model unavailable | not needed for deterministic core; semantic lane can fail/inconclusive separately |

The weaker failure modes are mostly presentation/operability:

1. A denial may expose only `reason_code` when another family exposes a rich recovery string.
2. The same conceptual condition can appear at multiple layers with different names.
3. There is no single stable `policy_id + policy_version` on every decision.
4. Some user-facing entrypoints format only `Outcome admission denied (<reason>); receipt ...` even though richer evidence exists underneath.
5. Recovery is represented inconsistently as free text, action-class tuples, resolution-error messages, resume events, or specialized recovery leases.

## Off-the-shelf survey

### OPA / Rego

Open Policy Agent is a mature general-purpose policy engine that accepts structured input, evaluates declarative policy, and separates decision-making from enforcement. Its decision logs retain input, result, decision ID, policy/bundle revision, timestamps and optional masking for sensitive data.

Fit for AES: **reference architecture / possible future policy backend**, not an immediate migration.

Why not adopt now:

- Enforced Planning already has typed Python rules, exact state bindings, receipts, replay/idempotency semantics, and tests.
- Rewriting mature Python policy into Rego would add migration cost without solving the current feedback inconsistency.
- OPA becomes attractive if rule authoring/distribution becomes a genuine multi-repository maintenance problem.

Official references:

- https://www.openpolicyagent.org/docs
- https://www.openpolicyagent.org/docs/management-decision-logs

### CEL

Common Expression Language is a safe, non-Turing-complete embedded expression language for fast predicates and simple data transformations. It supports compile/check/evaluate workflows and is used for policy-like conditions.

Fit for AES: **potential configuration expression language if project-owned policy conditions need to become data-driven**.

Do not adopt simply to rewrite existing Python decisions.

Reference: https://cel.dev/

### Cedar

Cedar is specifically an authorization policy language. It evaluates principal/action/resource/context requests and returns `Allow` or `Deny` plus diagnostics including determining policies and policy evaluation errors.

Fit for AES: **authorization only** — e.g. whether an agent/principal may invoke a protected operation/resource.

It is not a natural replacement for evidence adequacy or completion semantics.

Reference: https://docs.cedarpolicy.com/

### OpenFGA

OpenFGA is a relationship-based authorization system for graph-shaped questions such as whether a user/agent can access a resource through organization/team/project relationships.

Fit for AES: only if cross-project/organization resource authorization becomes a real requirement.

It is not a completion/evidence policy engine.

Reference: https://openfga.dev/

### DMN decision tables

DMN provides standardized decision tables with inputs, outputs, rules and dependencies. Camunda and other engines execute them.

Fit for AES: potentially useful if policy rules become business-owned, table-shaped, and need non-programmer editing/auditing.

Current Enforced Planning policies are mostly state-machine/custody invariants, not simple business decision tables, so DMN would be a poor default migration target.

Reference: https://docs.camunda.io/docs/components/modeler/dmn/

### RFC 9457 Problem Details

RFC 9457 defines a standard machine-readable problem object so clients do not need a new error format for every API. It has a stable problem `type`, human-readable title/detail and allows extension members.

Fit for AES: **very strong design precedent for agent-facing policy feedback**.

AES does not need to use HTTP to borrow the model:

```yaml
type: aes://policy/completion/current-evidence
title: Completion evidence is stale
detail: Current progress changed after retained completion evidence.
instance: receipt://...
reason_code: completion_evidence_stale
evidence_refs: [...]
recovery:
  action: reverify_current_artifact
  commands: [...]
retry: completion
```

Reference: https://www.rfc-editor.org/rfc/rfc9457.html

### gRPC / Google richer error-detail pattern

gRPC itself has standard status codes and points protocol-buffer users to Google's richer error model for structured error details.

Fit for AES: design precedent for separating a stable status from typed detail payloads such as precondition failures, retry guidance, and help.

AES can copy the architectural idea without adopting gRPC.

Reference: https://grpc.io/docs/guides/error/

### TypeSafe / Jev

TypeSafe exposes typed Noul, Choice and Score questions. That is a good fit for one genuinely semantic sub-question.

Fit for AES: **optional semantic provider behind the existing semantic-review boundary**, not policy authority and not a new policy runtime.

Reference: https://api.typesafe.ai/docs

## Recommended target shape

Do not replace the current deterministic core. Standardize its outward result.

A cross-policy decision envelope could conceptually contain:

```yaml
schema_version: aes.policy_problem.v1

decision:
  disposition: block | allow | defer | human_decision | review
  policy_id: completion.current-evidence
  policy_version: 1
  reason_code: completion_evidence_stale

problem:
  title: Completion evidence is stale
  detail: Current progress changed after retained completion evidence.

evidence:
  refs: [...]
  current_state: {...}

recovery:
  code: reverify_current_artifact
  permitted_actions:
    - passive_inspection
    - evidence_preservation
    - bounded_recovery_action
  instructions:
    - run the canonical verification command
    - retain the new receipt
    - retry completion

semantic:
  required: false
  result: null

receipt:
  id: ...
  source_revision: ...
```

This should initially be a **projection/adapter over existing result types**, not a migration that rewrites every subsystem.

## Where semantic judgment is actually justified

From the surveyed decision paths, nearly every current gate is deterministically answerable.

Good deterministic examples:

- Is the receipt current?
- Does the claim own this path?
- Is the worktree the exact claimed branch/repository?
- Are all frozen criteria represented?
- Are required execution items complete?
- Is the recovery lease current?
- Is the requested path in scope?
- Is there another ready work unit?
- Is a human decision explicitly required?

A semantic model is justified only for questions such as:

- Does this evidence actually substantiate the meaning of this criterion?
- Does the implementation satisfy a behavioral requirement not reducible to a programmatic check?
- Is a review finding materially blocking or advisory under an authored semantic rubric?

AES already has the PR semantic-review lane for this shape.

## Survey recommendation

1. **Do not introduce OPA, Cedar, OpenFGA, DMN, CEL, or Jev as a replacement for current Enforced Planning policy.**
2. **Do not build a new AES policy DSL/runtime/registry/replay platform.**
3. Treat OPA/CEL/Cedar/OpenFGA/DMN as future providers selected only when a named requirement fits them better than the existing Python owner.
4. Reuse/generalize the existing semantic PR-review boundary before creating another semantic evaluator framework.
5. Standardize a machine-readable policy-problem/recovery projection over existing decisions, borrowing from RFC 9457 and rich error-detail patterns.
6. Build/maintain a mapping from current reason codes to:
   - policy identity;
   - plain-language explanation;
   - evidence references;
   - recovery code;
   - permitted next actions;
   - exact retry condition.
7. First validate the projection against a handful of real current blockers. Do not start with a Jev-vs-deterministic benchmark.
8. Leave current deterministic decision owners unchanged until the normalized projection exposes a concrete deficiency.

## Immediate evidence-backed conclusion

The current system's central risk is **not that deterministic policy is too primitive**.

It is that rich internal policy state is not consistently exposed to the agent as one understandable, actionable contract.

That is the smallest useful problem to solve before evaluating another policy engine or semantic provider.

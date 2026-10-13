# Docstring Wiki

<!-- GENERATED FILE: DO NOT EDIT -->
<!-- source: git ls-files + actual source docstrings/document summaries -->
<!-- regenerate: python scripts/docstring_wiki.py --write -->

Searchable, non-authoritative compression of the repository's tracked
artifacts. Open the cited source for full context and current truth.

## Coverage

- Tracked artifacts: 1102
- Artifacts with source summaries: 420
- Coverage findings: 1061
- Finding types: python-docstring-missing=1061

## Source (189)

### [`datasets/learning-loop/experiments/2026-10-02-question-design/hier.py`](../datasets/learning-loop/experiments/2026-10-02-question-design/hier.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`datasets/learning-loop/experiments/2026-10-02-question-design/holdout.py`](../datasets/learning-loop/experiments/2026-10-02-question-design/holdout.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`datasets/learning-loop/experiments/2026-10-02-question-design/ml.py`](../datasets/learning-loop/experiments/2026-10-02-question-design/ml.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`datasets/learning-loop/experiments/2026-10-02-question-design/sc.py`](../datasets/learning-loop/experiments/2026-10-02-question-design/sc.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`datasets/learning-loop/experiments/2026-10-02-question-design/v2.py`](../datasets/learning-loop/experiments/2026-10-02-question-design/v2.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`datasets/learning-loop/experiments/2026-10-02-question-design/v2lib.py`](../datasets/learning-loop/experiments/2026-10-02-question-design/v2lib.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`datasets/learning-loop/experiments/2026-10-07-filing-gate/eval_reusable.py`](../datasets/learning-loop/experiments/2026-10-07-filing-gate/eval_reusable.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`datasets/learning-loop/experiments/2026-10-07-filing-gate/independent_grade.py`](../datasets/learning-loop/experiments/2026-10-07-filing-gate/independent_grade.py)

Independent grade of the 10 gated entries by a different model family (Gemini), blind to the filer's kind label and scores. Prints one line per entry and a summary.

_Coverage findings: python-docstring-missing._

### [`datasets/learning-loop/experiments/2026-10-07-filing-gate/paraphrase_probe.py`](../datasets/learning-loop/experiments/2026-10-07-filing-gate/paraphrase_probe.py)

Does the collector's light model (deepseek-v4-flash) catch the two known reworded repeats, and pass the 8 distinct ones?

_Coverage findings: python-docstring-missing._

### [`datasets/learning-loop/experiments/2026-10-07-filing-gate/retriage.py`](../datasets/learning-loop/experiments/2026-10-07-filing-gate/retriage.py)

Score the 2026-10-06 backlog's pending closeout-Learnings items with the collector's own triage (kind + reusable question) and append updated item lines, so file-pending applies the same gate.

### [`enforced_planning/__init__.py`](../enforced_planning/__init__.py)

Importable package surfaces for enforced-planning.

### [`enforced_planning/agents_rendering.py`](../enforced_planning/agents_rendering.py)

Importable AGENTS.md rendering helpers for governed repos.

**Symbols**

- `CanonicalInputs` · `CanonicalInputs` · line 26: Resolved canonical inputs used to render ``AGENTS.md``.
- `RendererRuntime` · `RendererRuntime` · line 37: Runtime configuration for one truthful render entrypoint layout.
- `RendererRuntime.repo_relative` · `repo_relative(self, path: Path, repo_root: Path) -> str` · line 44: Return a stable path string for generated output provenance.
- `RendererRuntime.resolve_inputs` · `resolve_inputs(self, repo_root: Path, claude_file: str = 'CLAUDE.md', relationships_file: str = 'scripts/relationships.yaml', output_file: str = 'AGENTS.md', template_path: Path | None = None) -> CanonicalInputs` · line 56: Resolve canonical input paths and fail loudly when missing.
- `RendererRuntime.render_agents_markdown` · `render_agents_markdown(self, inputs: CanonicalInputs) -> str` · line 95: Render the generated ``AGENTS.md`` content for a repo.
- `detect_repo_root` · `detect_repo_root(script_path: Path) -> Path` · line 141: Resolve the target repo root for both canonical and installed entrypoints.
- `default_template_path` · `default_template_path(repo_root: Path) -> Path` · line 151: Return the truthful default template path for this repo layout.
- `build_renderer` · `build_renderer(script_path: Path) -> RendererRuntime` · line 164: Build one renderer runtime for a concrete entrypoint path.
- `extract_title` · `extract_title(markdown: str) -> str` · line 175: Return the first H1 heading from a markdown document.
- `extract_overview` · `extract_overview(markdown: str) -> str` · line 184: Return the intro block between the title and the first thematic break.
- `extract_section` · `extract_section(markdown: str, heading: str) -> str` · line 208: Return the body for a named H2 section or supported heading alias.
- `parse_args` · `parse_args(default_template: Path) -> argparse.Namespace` · line 232: Parse CLI arguments for the renderer.

### [`enforced_planning/artifact_creation.py`](../enforced_planning/artifact_creation.py)

Evaluate and observe governed creation of new tracked repository artifacts.

**Symbols**

- `ArtifactCreationError` · `ArtifactCreationError` · line 41: Raised when configuration or native input cannot be evaluated safely.
- `StrictContract` · `StrictContract` · line 45: Reject unknown fields on durable artifact-governance contracts.
- `ArtifactTargetDecisionV1` · `ArtifactTargetDecisionV1` · line 51: One path-level creation decision and its exact policy reason.
- `ArtifactCreationDecisionV1` · `ArtifactCreationDecisionV1` · line 65: One aggregate pre-write or staged-candidate artifact decision.
- `ArtifactPolicyFeedbackV1` · `ArtifactPolicyFeedbackV1` · line 83: Human or agent feedback tied to one concrete gate receipt.
- `ArtifactPolicyFeedbackDispositionV1` · `ArtifactPolicyFeedbackDispositionV1` · line 97: Append-only resolution of one prior feedback record.
- `ArtifactRepositoryAuditV1` · `ArtifactRepositoryAuditV1` · line 109: Current repository findings that require cleanup outside a write event.
- `_mapping` · `_mapping(path: Path) -> dict[str, Any]` · line 120: Load a YAML mapping and fail loudly on any other shape.
- `_normalize_path` · `_normalize_path(value: str) -> str` · line 132: Return one safe repository-relative POSIX path.
- `_git` · `_git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]` · line 144: Run one bounded Git query without mutating repository state.
- `_branch` · `_branch(repo_root: Path) -> str | None` · line 155: Return the current branch when Git can identify it.
- `_is_tracked` · `_is_tracked(repo_root: Path, relative_path: str) -> bool` · line 163: Return whether a path already belongs to the Git index.
- `load_artifact_settings` · `load_artifact_settings(repo_root: Path) -> dict[str, Any]` · line 170: Load the explicit artifact-creation settings from meta-process.yaml.
- `_load_policy` · `_load_policy(repo_root: Path, settings: dict[str, Any]) -> dict[str, Any]` · line 193: Load and minimally validate the repository directory policy.
- `_artifact_blocks` · `_artifact_blocks(registry_text: str, registry_path: Path) -> tuple[str, ...]` · line 209: Return raw top-level artifact records without parsing unrelated registry data.
- `_block_path` · `_block_path(block: str) -> str | None` · line 247: Read one ordinary artifact path scalar while keeping the scan inexpensive.
- `_parse_artifact_block` · `_parse_artifact_block(block: str, registry_path: Path) -> dict[str, Any]` · line 265: Parse one selected artifact record and fail loud on its local shape.
- `_load_artifacts` · `_load_artifacts(repo_root: Path, settings: dict[str, Any], *, target_paths: tuple[str, ...], include_all: bool = False) -> list[dict[str, Any]]` · line 285: Load only target records and canonical-concern records needed by this decision.
- `_rule_for` · `_rule_for(path: str, policy: dict[str, Any]) -> dict[str, Any] | None` · line 313: Return the first exact directory rule matching one controlled path.
- `_path_glob_matches` · `_path_glob_matches(path: str, pattern: str) -> bool` · line 327: Match repository globs with segment-local ``*`` and recursive ``**``.
- `_intent_for` · `_intent_for(path: str, artifacts: list[dict[str, Any]]) -> dict[str, Any] | None` · line 350: Return the unique exact intent record for one proposed path.
- `_nonempty` · `_nonempty(value: Any) -> bool` · line 359: Return whether one scalar or collection carries meaningful content.
- `_validate_intent` · `_validate_intent(*, path: str, intent: dict[str, Any], rule: dict[str, Any], artifacts: list[dict[str, Any]], now: datetime) -> tuple[list[str], str | None]` · line 369: Return deterministic business-rule violations plus the concern ID.
- `evaluate_paths` · `evaluate_paths(*, repo_root: Path, target_paths: tuple[str, ...], client: str, tool_name: str, mode: ArtifactMode | None = None, force_new_paths: set[str] | None = None, receipt_path: Path = DEFAULT_RECEIPT_PATH, write_receipt: bool = True) -> ArtifactCreationDecisionV1` · line 465: Evaluate proposed paths and optionally append one local decision receipt.
- `evaluate_native_payload` · `evaluate_native_payload(payload: dict[str, Any], *, client: Literal['codex', 'claude-code'], mode: ArtifactMode | None = None, receipt_path: Path = DEFAULT_RECEIPT_PATH) -> ArtifactCreationDecisionV1` · line 619: Adapt one supported native pre-write payload and evaluate its paths.
- `staged_new_paths` · `staged_new_paths(repo_root: Path) -> tuple[str, ...]` · line 656: Return newly added paths from the current staged candidate.
- `audit_repository` · `audit_repository(repo_root: Path) -> ArtifactRepositoryAuditV1` · line 665: Audit retained quarantine and generated records that can decay over time.
- `append_jsonl` · `append_jsonl(path: Path, payload: dict[str, Any]) -> None` · line 728: Append one durable local JSONL record.
- `record_feedback` · `record_feedback(*, feedback_type: FeedbackKind, receipt_id: str, observation: str, recommendation: str, feedback_path: Path = DEFAULT_FEEDBACK_PATH) -> ArtifactPolicyFeedbackV1` · line 737: Persist concrete friction or improvement evidence without changing policy.
- `record_feedback_disposition` · `record_feedback_disposition(*, feedback_id: str, disposition: Literal['resolved', 'accepted_risk', 'superseded'], resolution: str, feedback_path: Path = DEFAULT_FEEDBACK_PATH) -> ArtifactPolicyFeedbackDispositionV1` · line 759: Append a durable disposition without rewriting the original feedback.
- `_read_jsonl` · `_read_jsonl(path: Path) -> list[dict[str, Any]]` · line 790: Read valid JSON objects from a local evidence stream and fail on corruption.
- `build_report` · `build_report(*, receipt_path: Path = DEFAULT_RECEIPT_PATH, feedback_path: Path = DEFAULT_FEEDBACK_PATH, repo_root: Path | None = None) -> dict[str, Any]` · line 810: Build a step-down-friendly enforcement, latency, and feedback report.

### [`enforced_planning/blocker_policy.py`](../enforced_planning/blocker_policy.py)

Provider-free ready-queue evaluation and blocker disposition policy.

**Symbols**

- `StrictContract` · `StrictContract` · line 109: Strict immutable base for Plan 110 public contracts.
- `QueueWorkUnitV1` · `QueueWorkUnitV1` · line 263: Strict runtime projection of canonical WorkUnitV1.
- `WorkGraphRefV1` · `WorkGraphRefV1` · line 389: Identity of the exact work-graph bytes used for one queue evaluation.
- `BlockedUnitV1` · `BlockedUnitV1` · line 409: One non-eligible work unit and its deterministic blocker references.
- `ClaimQueueSnapshotV1` · `ClaimQueueSnapshotV1` · line 416: Minimal immutable claim projection used by the queue evaluator.
- `ReadyQueueEvaluationV1` · `ReadyQueueEvaluationV1` · line 441: Revision-bound view of eligible, blocked, and actively owned work.
- `ReadyQueueEvaluationV1.queue_sets_are_internally_consistent` · `queue_sets_are_internally_consistent(self) -> ReadyQueueEvaluationV1` · line 460: Fail closed on structurally impossible queue projections.
- `MailboxDependencyV1` · `MailboxDependencyV1` · line 495: Delivery evidence required before one dependency wait may be certified.
- `MailboxEvidenceV1` · `MailboxEvidenceV1` · line 502: Current append-only delivery state for one exact mailbox message.
- `BlockerRequestV1` · `BlockerRequestV1` · line 510: Evidence supplied by an agent asking for a blocker disposition.
- `BlockerDispositionV1` · `BlockerDispositionV1` · line 546: System-owned deterministic decision; never an ownership mutation.
- `BlockerDecisionResultV1` · `BlockerDecisionResultV1` · line 563: Replayable system result retaining both derived queue and disposition.
- `BlockerDecisionInputV1` · `BlockerDecisionInputV1` · line 571: Portable evidence envelope for one provider-free blocker decision.
- `BlockerDecisionInputV1.require_one_mailbox_evidence_row_per_message` · `require_one_mailbox_evidence_row_per_message(self) -> BlockerDecisionInputV1` · line 595: Reject ambiguous duplicate message-state inputs.
- `_graph_semantic_errors` · `_graph_semantic_errors(units: tuple[QueueWorkUnitV1, ...], *, as_of: datetime) -> tuple[str, ...]` · line 666: Apply the canonical queue-relevant WorkUnitV1 graph invariants.
- `_active_unit_conflicts` · `_active_unit_conflicts(*, units: tuple[QueueWorkUnitV1, ...], claims: tuple[ClaimQueueSnapshotV1, ...], requesting_session_id: str, goal_or_graph_scope: str, graph_path: str, graph_sha256: str) -> set[str]` · line 845: Return exact-bound units actively owned by another session.
- `_work_graph_matches_numbered_scope` · `_work_graph_matches_numbered_scope(graph_ref_path: str, goal_or_graph_scope: str) -> bool` · line 893: Bind one plan-qualified scope to the numbered graph filename.
- `_verified_path_conflicts` · `_verified_path_conflicts(decision_input: BlockerDecisionInputV1) -> tuple[str, ...]` · line 904: Match requested path blockers to an exact-bound other-session claim.
- `_hard_dependency_blocker` · `_hard_dependency_blocker(dependency: WorkDependencyV1, *, units_by_id: dict[str, QueueWorkUnitV1]) -> str | None` · line 927: Return a blocker only for an unsatisfied canonical hard dependency.
- `evaluate_ready_queue` · `evaluate_ready_queue(*, repository_root: Path, work_graph_ref_path: str, expected_sha256: str, session_id: str, goal_or_graph_scope: str, claim_snapshots: tuple[ClaimQueueSnapshotV1, ...] = (), evaluated_at: datetime | None = None) -> ReadyQueueEvaluationV1` · line 947: Evaluate one exact work graph without mutating any coordination state.
- `evaluate_blocker_request` · `evaluate_blocker_request(decision_input: BlockerDecisionInputV1, *, repository_root: Path, recorded_at: datetime | None = None) -> BlockerDecisionResultV1` · line 1249: Evaluate source graph bytes and retain queue plus disposition.
- `decide_blocker_disposition` · `decide_blocker_disposition(decision_input: BlockerDecisionInputV1, *, repository_root: Path, recorded_at: datetime | None = None) -> BlockerDispositionV1` · line 1381: Compatibility API returning only the source-derived disposition.

_Coverage findings: python-docstring-missing._

### [`enforced_planning/claim_bootstrap.py`](../enforced_planning/claim_bootstrap.py)

Narrow self-service lane controls for a natively identified agent session.

**Symbols**

- `ClaimBootstrapError` · `ClaimBootstrapError` · line 53: A bootstrap request was malformed or exceeded self-service authority.
- `GoalWorktreeRequest` · `GoalWorktreeRequest` · line 209: Atomic claim/worktree/session bootstrap under explicit goal authority.
- `DelegatedMaintenanceWorktreeRequest` · `DelegatedMaintenanceWorktreeRequest` · line 226: Parent-authorized creation of one narrow child-owned maintenance lane.
- `RevokeDelegatedMaintenanceWorktreeRequest` · `RevokeDelegatedMaintenanceWorktreeRequest` · line 250: Parent cleanup for one pristine delegated lane that never produced work.
- `WorkspaceFileArchiveRequest` · `WorkspaceFileArchiveRequest` · line 353: Move one exact loose workspace file into its recoverable archive tree.
- `WorkspaceImageCanaryRequest` · `WorkspaceImageCanaryRequest` · line 389: Stage one preserved PNG as the exact image.png watcher canary.
- `_canonical_lock_module` · `_canonical_lock_module() -> Any` · line 453: Load the shipped canonical-lock owner without creating a second implementation.
- `_reconcile_canonical_after_claim` · `_reconcile_canonical_after_claim(repo: Path, *, session_id: str) -> dict[str, Any]` · line 478: Make the canonical checkout match the exact live-claim registry.
- `_finish_canonical_relock` · `_finish_canonical_relock(canonical_lock: Any, repo: Path, *, justifying_claims: list[str], session_id: str) -> dict[str, Any]` · line 499: Finish a relock after integration, including a partial first attempt.
- `_github_repo_from_remote` · `_github_repo_from_remote(remote_url: str) -> str` · line 543: Return owner/repository from an HTTPS, SSH, or SSH-host-alias URL.
- `_repository_authority` · `_repository_authority(repo: Path, *, branch: str | None = None) -> RepositoryAuthority | MaintenanceWorktreeAuthority` · line 600: Inspect repository identity, then delegate policy to the installed adapter.
- `_validate_existing_session_worktree` · `_validate_existing_session_worktree(request: SessionStartOrUpdateRequest) -> None` · line 628: Prove an ordinary session upsert names one existing Git checkout.
- `_fresh_remote_default_revision` · `_fresh_remote_default_revision(repo: Path, authority: RepositoryAuthority | MaintenanceWorktreeAuthority) -> str` · line 660: Fetch and resolve the graph-declared remote default before lane creation.
- `_reject_duplicate_object_keys` · `_reject_duplicate_object_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]` · line 708: Build one JSON object while rejecting ambiguity at every nesting level.
- `parse_request_json` · `parse_request_json(raw_json: str) -> ClaimBootstrapRequest` · line 719: Parse one strict v1 request; unknown fields, including session_id, fail.
- `canonical_script_path` · `canonical_script_path(repo_root: Path | None = None) -> Path` · line 736: Return the one canonical script path accepted by the raw Bash grammar.
- `parse_raw_bash_command` · `parse_raw_bash_command(raw_command: str, *, script_path: Path | None = None) -> ClaimBootstrapRequest` · line 743: Accept only one uncomposed absolute Python bootstrap command.
- `projection_recovery_command` · `projection_recovery_command(*, script_path: Path, claims_dir: Path, projection_path: Path) -> str` · line 769: Render the exact projection refresh command advertised by the gate.
- `parse_projection_recovery_command` · `parse_projection_recovery_command(raw_command: str, *, script_path: Path, claims_dir: Path, projection_path: Path) -> None` · line 784: Accept only the exact installed refresh operation and destinations.
- `_native_agent` · `_native_agent(requested: AgentName | None) -> tuple[AgentName, str]` · line 802: Resolve one current native runtime and reject borrowed agent identity.
- `_require_self_owned_slot` · `_require_self_owned_slot(*, agent: AgentName, session_id: str, project: str, scope: str, allow_absent: bool) -> None` · line 831: Refuse ambiguous, ownerless, or foreign claim-slot mutation.
- `_delegated_session_id` · `_delegated_session_id(*, agent: AgentName, child_agent_id: str, parent_session_id: str) -> str` · line 858: Normalize one child identity without letting the request change client.
- `_delegating_parent_claim` · `_delegating_parent_claim(*, agent: AgentName, project: str, parent_scope: str, parent_session_id: str, repo: Path) -> coordination_claims.ClaimRecord` · line 884: Resolve one healthy unparented program claim owned by the caller.
- `_configured_workspace_root` · `_configured_workspace_root() -> Path` · line 927: Resolve the canonical workspace from the hash-pinned authority provider.
- `execute_request` · `execute_request(request: ClaimBootstrapRequest) -> dict[str, Any]` · line 1077: Execute one self-owned claim mutation and return a JSON-safe receipt.
- `_execute_local_repository_integrate` · `_execute_local_repository_integrate(request: LocalRepositoryIntegrateRequest, *, agent: AgentName, session_id: str) -> dict[str, Any]` · line 1185: Fast-forward one locked local-only canonical checkout from its sole live lane.
- `_rollback_created_worktree` · `_rollback_created_worktree(*, repo: Path, worktree: Path, branch: str, expected_head: str, branch_created: bool, created_dirs: list[Path]) -> list[str]` · line 1322: Remove only the exact, untouched no-checkout lane created by bootstrap.
- `_preserve_partial_session_claim_as_blocked` · `_preserve_partial_session_claim_as_blocked(*, agent: AgentName, project: str, scope: str, session_id: str, branch: str, worktree: Path, failure: Exception) -> bool` · line 1452: Preserve and block an exact claim that survived a bootstrap failure.
- `_remove_pristine_bootstrap_repository` · `_remove_pristine_bootstrap_repository(repo: Path, *, expected_head: str | None = None) -> list[str]` · line 1499: Remove only an exact repository created by this failed transaction.
- `_execute_local_repository_worktree` · `_execute_local_repository_worktree(request: LocalRepositoryWorktreeRequest, *, agent: AgentName, session_id: str) -> dict[str, Any]` · line 1532: Initialize one local-only repository and its first claimed task worktree.
- `_execute_revoke_delegated_worktree` · `_execute_revoke_delegated_worktree(request: RevokeDelegatedMaintenanceWorktreeRequest, *, agent: AgentName, session_id: str) -> dict[str, Any]` · line 1719: Remove only a pristine child lane through its exact parent authority.
- `_execute_maintenance_worktree` · `_execute_maintenance_worktree(request: MaintenanceWorktreeRequest | DelegatedMaintenanceWorktreeRequest | GoalWorktreeRequest, *, agent: AgentName, session_id: str) -> dict[str, Any]` · line 1847: Create one maintenance or goal-bound worktree as a typed transaction.

_Coverage findings: python-docstring-missing._

### [`enforced_planning/claim_mutation_receipts.py`](../enforced_planning/claim_mutation_receipts.py)

Durable, typed evidence for sanctioned claim-registry mutations.

**Symbols**

- `CompletedClaimPruneBindingV1` · `CompletedClaimPruneBindingV1` · line 54: Bind one archived completed claim to its sanctioned prune provenance.
- `CompletedClaimPruneBindingV1._require_exact_binding_identity` · `_require_exact_binding_identity(self) -> 'CompletedClaimPruneBindingV1'` · line 62: Each binding kind owns exactly one provenance identifier.
- `_decode_source_yaml_bytes` · `_decode_source_yaml_bytes(encoded: str) -> bytes` · line 78: Decode a strict base64 source payload.
- `_completed_claim_identity` · `_completed_claim_identity(source_bytes: bytes) -> tuple[str, str, str, str | None, CompletedClaimStatus]` · line 87: Parse the exact identity needed by the completed-claim archive.
- `CompletedClaimArchiveReceiptV1` · `CompletedClaimArchiveReceiptV1` · line 148: One exact-byte, intrinsically validated completed-claim archive record.
- `CompletedClaimArchiveReceiptV1._validate_exact_source_and_receipt` · `_validate_exact_source_and_receipt(self) -> 'CompletedClaimArchiveReceiptV1'` · line 170: Reject any drift in source bytes, identity, binding, or receipt digest.
- `ClaimMutationReceiptV1` · `ClaimMutationReceiptV1` · line 217: One terminal audit record for one sanctioned claim mutation.
- `ClaimMutationReceiptV1._require_outcome_details_when_applied` · `_require_outcome_details_when_applied(self) -> 'ClaimMutationReceiptV1'` · line 244: Applied mutations must retain the complete authority outcome.
- `NarrowClaimMutationReceiptV1` · `NarrowClaimMutationReceiptV1` · line 273: One narrow receipt isolated from the backward-compatible shared v1 ledger.
- `MutationAuditError` · `MutationAuditError` · line 301: A mutation completed, but its durable provenance receipt could not persist.
- `CompletedClaimArchiveError` · `CompletedClaimArchiveError` · line 346: Archive validation or persistence failed before claim-registry mutation.
- `writer_identity` · `writer_identity(source_path: Path) -> tuple[str, str, str]` · line 372: Return the loaded runtime source identity without relying on cwd or repo names.
- `completed_claim_archive_id` · `completed_claim_archive_id(*, source_path: str, source_sha256: str) -> str` · line 384: Return the deterministic identity for one exact claim source artifact.
- `completed_claim_archive_transaction_id` · `completed_claim_archive_transaction_id(archive_id: str) -> str` · line 396: Return the deterministic live-prune transaction for one archive identity.
- `_canonical_json_value` · `_canonical_json_value(value: Any) -> Any` · line 404: Normalize Pydantic and datetime values for a stable canonical digest.
- `completed_claim_archive_receipt_sha256` · `completed_claim_archive_receipt_sha256(receipt: CompletedClaimArchiveReceiptV1 | dict[str, Any]) -> str` · line 420: Hash canonical receipt content while excluding its self-digest field.
- `build_completed_claim_archive_receipt` · `build_completed_claim_archive_receipt(*, source_kind: CompletedClaimSourceKind, source_path: Path | str, source_bytes: bytes, prune_event_id: str | None = None, writer: tuple[str, str, str] | None = None, archived_at: datetime | None = None) -> CompletedClaimArchiveReceiptV1` · line 447: Build and fully validate one deterministic exact-byte archive receipt.
- `_completed_claim_archive_semantic_payload` · `_completed_claim_archive_semantic_payload(receipt: CompletedClaimArchiveReceiptV1) -> dict[str, Any]` · line 506: Return immutable source and prune fields used for duplicate comparison.
- `_parse_completed_claim_archive` · `_parse_completed_claim_archive(text: str, *, archive_path: Path) -> list[CompletedClaimArchiveReceiptV1]` · line 527: Parse an intrinsic archive ledger and reject conflicting duplicate IDs.
- `_archive_receipts_matching_id` · `_archive_receipts_matching_id(text: str, *, archive_path: Path, archive_id: str) -> list['CompletedClaimArchiveReceiptV1']` · line 560: Validate only the ledger records that could carry one archive_id.
- `append_completed_claim_archive_receipt` · `append_completed_claim_archive_receipt(receipt: CompletedClaimArchiveReceiptV1, *, archive_path: Path | None = None) -> tuple[Path, bool]` · line 604: Append and fsync one receipt, with idempotent exact-identity replay.
- `validate_completed_claim_archive_prune_binding` · `validate_completed_claim_archive_prune_binding(receipt: CompletedClaimArchiveReceiptV1, *, mutation_receipts: list[ClaimMutationReceiptV1]) -> ClaimMutationReceiptV1` · line 646: Require one applied prune mutation matching the archived claim exactly.
- `load_completed_claim_archive_receipts` · `load_completed_claim_archive_receipts(*, archive_path: Path | None = None, mutation_events_path: Path | None = None) -> list[CompletedClaimArchiveReceiptV1]` · line 706: Load the archive and require every record's applied prune binding.
- `append_receipt` · `append_receipt(receipt: ClaimMutationReceiptV1, *, events_path: Path | None = None) -> Path` · line 731: Append and fsync one receipt while preserving JSONL record boundaries.
- `append_narrow_receipt` · `append_narrow_receipt(receipt: NarrowClaimMutationReceiptV1, *, events_path: Path | None = None) -> Path` · line 749: Append one typed narrow receipt to its version-isolated ledger.
- `load_receipts` · `load_receipts(*, events_path: Path | None = None) -> list[ClaimMutationReceiptV1]` · line 771: Load a complete JSONL ledger, rejecting malformed or unknown fields.
- `load_narrow_receipts` · `load_narrow_receipts(*, events_path: Path | None = None) -> list[NarrowClaimMutationReceiptV1]` · line 788: Load the complete narrow ledger without changing the shared v1 reader.

_Coverage findings: python-docstring-missing._

### [`enforced_planning/client_session_metadata.py`](../enforced_planning/client_session_metadata.py)

Read-only client display metadata and truthful mailbox response projections.

**Symbols**

- `StrictProjection` · `StrictProjection` · line 19: Strict immutable base for local operator projections.
- `ClientSessionDisplayV1` · `ClientSessionDisplayV1` · line 25: Mutable client display metadata kept separate from routing identity.
- `CoordinationResponseReadoutV1` · `CoordinationResponseReadoutV1` · line 38: Legacy joined operator view retained for strict consumer compatibility.
- `CoordinationResponseReadoutV2` · `CoordinationResponseReadoutV2` · line 63: Versioned operator view with explicit host delivery capability.
- `_portable_path` · `_portable_path(path: Path) -> str` · line 79: Render a home-relative path without persisting a personal home prefix.
- `_client_name` · `_client_name(session_id: str) -> Literal['codex', 'claude-code', 'openclaw', 'unknown']` · line 89: Classify one canonical session ID without inventing client metadata.
- `_resolve_claude_code_display` · `_resolve_claude_code_display(session_id: str, *, claude_session_registry: Path) -> ClientSessionDisplayV1` · line 98: Resolve one Claude Code session's addressable peer name from its registry.
- `resolve_client_session_display` · `resolve_client_session_display(session_id: str, *, codex_session_index: Path = DEFAULT_CODEX_SESSION_INDEX, claude_session_registry: Path = DEFAULT_CLAUDE_SESSION_REGISTRY) -> ClientSessionDisplayV1` · line 171: Resolve optional human-facing metadata without changing canonical identity.
- `build_coordination_response_readout` · `build_coordination_response_readout(status: coordination_messages.MessageStatusView, *, claims: list[coordination_claims.ClaimRecord], codex_session_index: Path = DEFAULT_CODEX_SESSION_INDEX, codex_config_path: Path | None = None, claude_config_path: Path | None = None) -> CoordinationResponseReadoutV2` · line 254: Join message lifecycle and display metadata without inferring completion.

### [`enforced_planning/concern_routing.py`](../enforced_planning/concern_routing.py)

Review-claim creation and concern routing for coordination-aware review work.

**Symbols**

- `ConcernRoute` · `ConcernRoute` · line 24: Describe where one concern was delivered.
- `ConcernRoute.to_dict` · `to_dict(self) -> dict[str, Any]` · line 34: Return a JSON-safe representation for CLI use.
- `_split_path_values` · `_split_path_values(raw_values: list[str] | None) -> list[str]` · line 40: Normalize repeated delimiter-packed path lists into stable write paths.
- `_candidate_review_scope` · `_candidate_review_scope(target_branch: str) -> str` · line 55: Derive a stable review-claim scope for one target branch.
- `_current_branch` · `_current_branch(repo_root: Path) -> str | None` · line 61: Return the current branch when HEAD is attached, else ``None``.
- `create_review_claim` · `create_review_claim(*, repo_root: str | Path, agent: str, project: str, target_branch: str, intent: str, write_paths: list[str], plan_ref: str | None = None, ttl_hours: float = coordination_claims.DEFAULT_TTL_HOURS, notes: str | None = None, scope: str | None = None, session_id: str | None = None, session_name: str | None = None) -> dict[str, Any]` · line 70: Create a review claim that makes cross-lane inspection visible.
- `_run_gh` · `_run_gh(repo_root: Path, args: list[str]) -> subprocess.CompletedProcess[str]` · line 118: Run one GitHub CLI command and capture stdout/stderr without guessing.
- `_open_pr_for_branch` · `_open_pr_for_branch(repo_root: Path, branch: str) -> dict[str, Any] | None` · line 130: Return the first open PR for a head branch when one exists.
- `_best_recipient` · `_best_recipient(project: str, target_branch: str, explicit_recipient: str | None) -> str` · line 147: Resolve exactly one canonical recipient session for an unpublished lane.
- `route_concern` · `route_concern(*, repo_root: str | Path, agent: str, project: str, target_branch: str, subject: str, content: str, recipient: str | None = None, idempotency_key: str | None = None, dry_run: bool = False) -> dict[str, Any]` · line 169: Route a concern to a PR or persist it in the canonical mailbox.

### [`enforced_planning/concurrent_writers.py`](../enforced_planning/concurrent_writers.py)

Report what landed on a shared ref while a lane was open.

**Symbols**

- `ForeignCommit` · `ForeignCommit` · line 51: One commit on the shared ref that did not come from this lane.
- `SharedRefReport` · `SharedRefReport` · line 64: What was learned about movement on ``ref`` while a lane was open.
- `collect_shared_ref_movement` · `collect_shared_ref_movement(repo_root: Path, *, ref: str, since_revision: str | None, lane_refs: tuple[str, ...] = (), basis: str = BASIS_START_REVISION) -> SharedRefReport` · line 111: Read ``since_revision..ref``, minus anything reachable from ``lane_refs``.
- `render_report` · `render_report(report: SharedRefReport) -> str` · line 179: One short block naming what this session must not describe from memory.

_Coverage findings: python-docstring-missing._

### [`enforced_planning/context_packet.py`](../enforced_planning/context_packet.py)

Build bounded edit-context packets from source summaries and relationship edges.

**Symbols**

- `ContextPacketError` · `ContextPacketError` · line 82: Report malformed relationships or a target that cannot be resolved.
- `RelationshipSpec` · `RelationshipSpec` · line 87: Normalize one reviewed or legacy relationship declaration.
- `ContextDiagnostic` · `ContextDiagnostic` · line 100: Describe context that could not be resolved or included.
- `ContextItem` · `ContextItem` · line 109: Carry one provenance-bound source summary in an edit context packet.
- `ContextPacket` · `ContextPacket` · line 128: Provide deterministic bounded context for one file or Python symbol edit.
- `ContextPacket.to_json` · `to_json(self, *, pretty: bool = False) -> str` · line 140: Serialize the packet deterministically for hooks and agents.
- `RequiredContextAtom` · `RequiredContextAtom` · line 153: Carry one complete required file and its exact source identity.
- `RequiredAtomReceipt` · `RequiredAtomReceipt` · line 166: Describe one expected atom without archiving its payload.
- `ContextPacketV3` · `ContextPacketV3` · line 178: Separate unclipped required files from bounded optional summaries.
- `ContextReceipt` · `ContextReceipt` · line 187: Bind expected context to an action without claiming host delivery.
- `ContextReceipt.to_json` · `to_json(self, *, pretty: bool = False) -> str` · line 201: Serialize the expected receipt deterministically.
- `_to_strings` · `_to_strings(value: Any) -> tuple[str, ...]` · line 216: Normalize one selector field without accepting broad arbitrary values.
- `_to_refs` · `_to_refs(value: Any) -> tuple[str, ...]` · line 228: Normalize ADR and plan reference identifiers that may be numeric in V1.
- `_validate_spec` · `_validate_spec(spec: RelationshipSpec) -> RelationshipSpec` · line 240: Fail loudly when an edge cannot produce predictable context behavior.
- `relationship_specs` · `relationship_specs(relationships: dict[str, Any]) -> tuple[RelationshipSpec, ...]` · line 256: Normalize explicit V2 edges and existing relationship sections.
- `_split_selector` · `_split_selector(selector: str) -> tuple[str, str | None]` · line 375: Split a file or ``file::qualified.symbol`` selector.
- `_glob_matches` · `_glob_matches(value: str, pattern: str) -> bool` · line 382: Match recursive globs with ``**/`` also representing zero directories.
- `_selector_matches` · `_selector_matches(selector: str, path: str, symbol: str | None) -> bool` · line 402: Match one path/symbol selector against a requested target node.
- `_expand_selectors` · `_expand_selectors(selectors: tuple[str, ...], inventory: InventoryReport) -> tuple[tuple[str, str | None], ...]` · line 411: Expand declared selectors deterministically against tracked artifacts and symbols.
- `expand_selectors` · `expand_selectors(selectors: tuple[str, ...], inventory: InventoryReport) -> tuple[tuple[str, str | None], ...]` · line 427: Expand file/symbol selectors for context and reconciliation consumers.
- `selector_path_matches` · `selector_path_matches(selector: str, path: str) -> bool` · line 433: Match only the file component of a selector for file-level change sets.
- `_required_selector_provenance` · `_required_selector_provenance(target_path: str, target_symbol: str | None, relationships: dict[str, Any]) -> dict[str, set[str]]` · line 440: Resolve applicable required-reading declarations to selectors and provenance.
- `_required_paths` · `_required_paths(inventory: InventoryReport, selector_provenance: dict[str, set[str]]) -> dict[str, set[str]]` · line 482: Expand required full-file selectors without accepting symbol fragments.
- `_git_output` · `_git_output(repo_root: Path, args: list[str]) -> str` · line 509: Run one bounded read-only Git query and return stripped stdout.
- `_git_bytes` · `_git_bytes(repo_root: Path, args: list[str]) -> bytes` · line 524: Run one bounded read-only Git query that must preserve exact bytes.
- `_required_atoms` · `_required_atoms(repo_root: Path, target_path: str, target_symbol: str | None, relationships: dict[str, Any], inventory: InventoryReport, required_capacity_bytes: int) -> tuple[RequiredContextAtom, ...]` · line 538: Read every applicable required file whole or block compilation.
- `_context_item` · `_context_item(artifact: ArtifactRecord, *, symbol_name: str | None, relation: str, direction: Direction, reason: str, maintenance: str, archive_effect: str, provenance: str) -> ContextItem` · line 601: Bind one artifact or symbol's actual source summary to an edge.
- `_item_chars` · `_item_chars(item: ContextItem) -> int` · line 650: Measure exactly the serialized context contribution of one item.
- `_fit_target` · `_fit_target(item: ContextItem, max_chars: int) -> ContextItem` · line 656: Keep the target present by truncating only its source summary when required.
- `build_context_packet` · `build_context_packet(repo_root: Path, target_path: str, relationships: dict[str, Any], *, target_symbol: str | None = None, max_items: int = 20, max_chars: int = 8000, allow_untracked_target: bool = False) -> ContextPacket` · line 670: Resolve and budget source-derived context for one edit target.
- `build_context_packet_with_receipt` · `build_context_packet_with_receipt(repo_root: Path, target_path: str, relationships: dict[str, Any], *, required_capacity_bytes: int, session_id: str, context_epoch: str, action: str, adapter_id: str, adapter_version: str, target_symbol: str | None = None, max_items: int = 20, max_chars: int = 8000, allow_untracked_target: bool = False) -> tuple[ContextPacketV3, ContextReceipt]` · line 811: Build V3 required context and an honest expected-visibility receipt.
- `_load_relationships` · `_load_relationships(repo_root: Path, config_path: str | Path) -> dict[str, Any]` · line 896: Load one repository relationship graph without legacy module coupling.
- `main` · `main(argv: list[str] | None = None) -> int` · line 910: Run the portable context-packet CLI for one edit target.

### [`enforced_planning/coordination_claims.py`](../enforced_planning/coordination_claims.py)

Cross-brain coordination claims for multi-agent work.

**Symbols**

- `ClaimRegistryLockTimeout` · `ClaimRegistryLockTimeout` · line 92: The single local claim writer stayed busy beyond the bounded wait.
- `ProgressEventV1` · `ProgressEventV1` · line 185: One explicit durable-advancement event for an owning live claim.
- `claim_registry_lock` · `claim_registry_lock(claims_dir: Path | None = None, *, timeout_seconds: float = CLAIM_REGISTRY_LOCK_TIMEOUT_SECONDS) -> Iterator[None]` · line 226: Serialize mutations, failing with an exact retry condition on contention.
- `_claim_write_staging_dir` · `_claim_write_staging_dir(claims_dir: Path) -> Path` · line 262: Return same-filesystem staging outside the live claim registry.
- `_prune_abandoned_claim_write_artifacts` · `_prune_abandoned_claim_write_artifacts(claims_dir: Path, *, minimum_age_seconds: int = CLAIM_WRITE_STAGING_MAX_AGE_SECONDS) -> int` · line 268: Remove only old atomic-write artifacts from sanctioned claim writers.
- `_atomic_write_claim` · `_atomic_write_claim(path: Path, payload: dict[str, Any]) -> None` · line 295: Replace one claim without exposing a truncated or partially written file.
- `_atomic_restore_file` · `_atomic_restore_file(path: Path, content: bytes | None) -> None` · line 328: Restore exact prior bytes, or exact prior absence, after a failed transition.
- `_replace_claim_and_refresh_projection_fail_atomic` · `_replace_claim_and_refresh_projection_fail_atomic(*, claim_path: Path, payload: dict[str, Any], claims_dir: Path) -> tuple[str, str]` · line 354: Replace claim plus projection or restore both exact preflight states.
- `replace_claim_payloads_and_refresh_projection_fail_atomic` · `replace_claim_payloads_and_refresh_projection_fail_atomic(*, replacements: dict[Path, dict[str, Any]], claims_dir: Path) -> tuple[str, str]` · line 376: Replace a bounded claim set or restore every claim and the projection.
- `refresh_prewrite_authority_projection` · `refresh_prewrite_authority_projection(claims_dir: Path | None = None) -> tuple[str, str]` · line 415: Regenerate the replaceable pre-write projection from canonical YAML.
- `_registry_digest` · `_registry_digest(claims_dir: Path) -> str` · line 428: Return the canonical digest used to bind derived projection state.
- `_registry_snapshot` · `_registry_snapshot(claims_dir: Path) -> dict[str, bytes]` · line 436: Read every YAML authority record once, keyed by the digest's own key.
- `_registry_digest_from_snapshot` · `_registry_digest_from_snapshot(snapshot: dict[str, bytes]) -> str` · line 442: Reproduce ``prewrite_claim_fast.registry_digest`` from an in-memory snapshot.
- `PruneRegistryDivergenceError` · `PruneRegistryDivergenceError` · line 460: The registry moved underneath an in-progress prune, after a mutation applied.
- `record_claim_mutation` · `record_claim_mutation(*, operation: 'claim_mutation_receipts.MutationOperation', claims_dir: Path, registry_digest_before: str | None, target_project: str | None, target_scope: str | None, target_claim_path: Path | None, session_id: str | None, projection_digest_after: str | None, archive_transaction_id: str | None = None, known_registry_digest_after: str | None = None, known_projection_current_after: bool | None = None) -> 'claim_mutation_receipts.ClaimMutationReceiptV1'` · line 471: Persist one terminal receipt after a sanctioned YAML/projection mutation.
- `active_session_takeover_reservation` · `active_session_takeover_reservation(payload: dict[str, Any]) -> dict[str, Any] | None` · line 546: Return one validated active custody-takeover reservation from raw claim state.
- `reject_mutation_during_session_takeover` · `reject_mutation_during_session_takeover(payload: dict[str, Any], *, operation: str) -> None` · line 575: Fence predecessor claim mutations while an exact custody takeover is active.
- `reserve_session_takeover` · `reserve_session_takeover(*, claim_file: Path, agent: str, project: str, scope: str, predecessor_session_id: str, successor_session_id: str, worktree_path: str, predecessor_pid: int, predecessor_process_start_ticks: int, reserved_at: str, pre_reservation_claim_bytes: bytes, claims_dir: Path | None = None) -> tuple[ClaimRecord, dict[str, Any], bytes, dict[str, Any]]` · line 592: Durably reserve one exact predecessor claim epoch before process fencing.
- `abort_unfenced_session_takeover_reservation` · `abort_unfenced_session_takeover_reservation(*, claim_file: Path, agent: str, project: str, scope: str, successor_session_id: str, worktree_path: str, claims_dir: Path | None = None) -> dict[str, Any]` · line 671: Cancel one successor-owned reservation before fencing ever began.
- `record_claim_narrow_mutation` · `record_claim_narrow_mutation(*, claims_dir: Path, registry_digest_before: str, target_project: str, target_scope: str, target_claim_path: Path, session_id: str, projection_digest_after: str) -> 'claim_mutation_receipts.NarrowClaimMutationReceiptV1'` · line 737: Persist one narrow receipt without extending the shared v1 operation enum.
- `PlanAuthorityBinding` · `PlanAuthorityBinding` · line 790: Resolved navigation-independent target and numbered-plan identities.
- `MethodConformanceRefusal` · `MethodConformanceRefusal` · line 830: A claim-admission refusal with one stable reason code.
- `MethodConformanceBindingV1` · `MethodConformanceBindingV1` · line 838: The exact receipt identity a plan-backed claim retains.
- `method_conformance_mode` · `method_conformance_mode(plan_root: Path, revision: str) -> Literal['required', 'off']` · line 872: Read the repository's structural requirement at the exact plan revision.
- `resolve_method_conformance_binding` · `resolve_method_conformance_binding(*, plan_root: Path | str, plan_revision: str, plan_number: int | None, receipt_ref: str | None, receipt_sha256: str | None) -> MethodConformanceBindingV1 | None` · line 908: Resolve the exact passing receipt a plan-backed claim names, or refuse.
- `CanonicalWorkUnitBinding` · `CanonicalWorkUnitBinding` · line 1005: Exact target-graph and optional external-plan authority custody.
- `CanonicalWorkUnitBinding.__iter__` · `__iter__(self) -> Iterator[object]` · line 1016: Retain the historical three-value unpacking API for local consumers.
- `coerce_canonical_work_unit_binding` · `coerce_canonical_work_unit_binding(binding: CanonicalWorkUnitBinding | tuple[str, tuple[str, ...], str]) -> CanonicalWorkUnitBinding` · line 1024: Adapt legacy test/consumer triples while callers migrate to typed custody.
- `ClaimRecord` · `ClaimRecord` · line 1036: Normalized coordination claim record used across readable schema versions.
- `ClaimRecord.primary_project` · `primary_project(self) -> str | None` · line 1086: Return the first project for CLI compatibility surfaces.
- `ClaimRecord.is_live` · `is_live(self) -> bool` · line 1090: Return whether the claim should participate in active coordination.
- `ClaimRecord.to_dict` · `to_dict(self) -> dict[str, Any]` · line 1094: Return a JSON/YAML-safe dictionary for reporting and persistence.
- `ClaimInteraction` · `ClaimInteraction` · line 1102: Describe how one candidate claim interacts with another active claim.
- `ClaimInteraction.to_dict` · `to_dict(self) -> dict[str, Any]` · line 1121: Return a JSON-safe interaction summary.
- `NarrowClaimResult` · `NarrowClaimResult` · line 1130: Committed result of one owner/session-bound subset-only narrowing.
- `NarrowClaimResult.to_dict` · `to_dict(self) -> dict[str, Any]` · line 1143: Return a JSON-safe narrowing result.
- `ClaimCheckResult` · `ClaimCheckResult` · line 1149: Structured result for candidate-vs-active-claims evaluation.
- `ClaimCheckResult.hard_conflicts` · `hard_conflicts(self) -> list[ClaimInteraction]` · line 1156: Return hard-conflict interactions only.
- `ClaimCheckResult.continuation` · `continuation(self) -> dict[str, Any]` · line 1160: Describe safe work that remains outside path-local claim conflicts.
- `ClaimCheckResult.to_dict` · `to_dict(self) -> dict[str, Any]` · line 1207: Return a JSON-safe check result.
- `is_goal_authority_ref` · `is_goal_authority_ref(plan_ref: str | None) -> bool` · line 1217: Return whether a ref names one explicit non-plan outcome authority.
- `requires_work_graph` · `requires_work_graph(plan_ref: str | None) -> bool` · line 1223: Return whether write ownership names plan-like authority needing a graph.
- `_normalized_repository_id` · `_normalized_repository_id(value: str) -> str` · line 1234: Normalize repository identity spellings used by qualified plan refs.
- `_qualified_plan_repository` · `_qualified_plan_repository(plan_ref: str | None) -> str | None` · line 1240: Return the explicit authority repository from ``repository#number``.
- `_claim_uses_external_plan_authority` · `_claim_uses_external_plan_authority(claim: ClaimRecord) -> bool` · line 1249: Return whether a claim's qualified plan belongs to another project.
- `claim_health_issues` · `claim_health_issues(claim: ClaimRecord) -> list[str]` · line 1257: Return machine-readable health issues for one normalized claim.
- `claim_health_status` · `claim_health_status(claim: ClaimRecord) -> str` · line 1324: Classify one claim as healthy or weak for registry/reporting surfaces.
- `normalize_plan_identity` · `normalize_plan_identity(plan_ref: str | None) -> str | None` · line 1329: Return one stable numbered-plan identity from descriptive plan text.
- `_same_claim` · `_same_claim(left: ClaimRecord, right: ClaimRecord) -> bool` · line 1348: Return whether two records identify the same canonical claim slot.
- `claim_hierarchy_issues` · `claim_hierarchy_issues(claim: ClaimRecord, *, active_claims: list[ClaimRecord]) -> list[str]` · line 1354: Validate one claim against the existing root-program hierarchy.
- `coordination_health_issues` · `coordination_health_issues(claim: ClaimRecord, *, active_claims: list[ClaimRecord]) -> list[str]` · line 1427: Return local metadata plus cross-claim hierarchy health issues.
- `validate_claim_hierarchy_for_creation` · `validate_claim_hierarchy_for_creation(candidate: ClaimRecord, *, active_claims: list[ClaimRecord]) -> None` · line 1437: Reject a new or refreshed session claim that would be hierarchically invalid.
- `session_root_conflicts` · `session_root_conflicts(claim: ClaimRecord, *, active_claims: list[ClaimRecord]) -> list[ClaimRecord]` · line 1452: Return other unparented lanes owned by the exact runtime session.
- `normalize_parent_scope` · `normalize_parent_scope(parent_scope: str | None, project: str | None) -> str | None` · line 1479: Store a parent scope as the bare scope its parent claim records.
- `validate_session_root_for_creation` · `validate_session_root_for_creation(candidate: ClaimRecord, *, active_claims: list[ClaimRecord]) -> None` · line 1495: Reject accidental tangent roots while preserving explicit parallelism.
- `validate_no_preserved_lane_conflict` · `validate_no_preserved_lane_conflict(candidate: ClaimRecord, *, claims: list[ClaimRecord]) -> None` · line 1513: Require explicit recovery before replacing preserved ended work.
- `_heartbeat_stale_after` · `_heartbeat_stale_after() -> timedelta` · line 1548: Return the configured heartbeat freshness window.
- `_progress_stale_after` · `_progress_stale_after() -> timedelta` · line 1562: Return the configured durable-progress lease and fail on invalid policy.
- `_run_git` · `_run_git(repo_root: Path, args: list[str]) -> subprocess.CompletedProcess[str]` · line 1577: Run one git command for lifecycle diagnostics without throwing.
- `_resolve_repo_root_from_worktree_path` · `_resolve_repo_root_from_worktree_path(worktree_path: str | None) -> Path | None` · line 1588: Resolve the canonical repo root from a claim worktree path when possible.
- `_resolve_default_branch` · `_resolve_default_branch(repo_root: Path) -> str | None` · line 1607: Return the canonical default branch name for one repo when resolvable.
- `_default_integration_ref` · `_default_integration_ref(repo_root: Path, default_branch: str) -> str` · line 1623: Prefer the canonical remote default ref when it exists.
- `resolve_default_integration_revision` · `resolve_default_integration_revision(repo_root: Path | str) -> str` · line 1631: Resolve one full immutable commit for the canonical integration tip.
- `validate_start_revision_targets` · `validate_start_revision_targets(*, repo_root: Path | str, start_revision: str, branch: str | None, worktree_path: str | None, require_branch: bool = False, require_worktree: bool = False) -> None` · line 1646: Require any existing execution identities to retain one start commit.
- `_claimed_worktree_has_pending_changes` · `_claimed_worktree_has_pending_changes(worktree_path: Path | None) -> bool` · line 1704: Return whether pending tracked or untracked work is positively proven.
- `claim_lifecycle_issues` · `claim_lifecycle_issues(claim: ClaimRecord) -> list[str]` · line 1720: Return mechanically provable stale-lifecycle issues for one live claim.
- `_claim_branch_unmerged_progress` · `_claim_branch_unmerged_progress(claim: ClaimRecord) -> dict[str, Any] | None` · line 1770: Return git evidence that a claim's branch holds real unmerged commits.
- `list_abandoned_claims` · `list_abandoned_claims(project: str | None = None, *, claims_dir: Path | None = None, min_ahead: int = 1) -> list[tuple[ClaimRecord, dict[str, Any]]]` · line 1821: Surface EXPIRED claims whose branch still holds real unmerged commits.
- `claim_liveness_issues` · `claim_liveness_issues(claim: ClaimRecord, *, now: datetime | None = None) -> list[str]` · line 1873: Return stale-session issues derived from heartbeat freshness.
- `_parse_aware_iso_datetime` · `_parse_aware_iso_datetime(value: Any) -> datetime | None` · line 1908: Parse a timezone-aware ISO timestamp without silently assuming UTC.
- `build_progress_event` · `build_progress_event(*, progress_kind: str, evidence_ref: str, next_action: str, expected_quiet_until: str | datetime | None = None, quiet_reason: str | None = None, progress_at: datetime | None = None) -> ProgressEventV1` · line 1922: Validate one server-timestamped progress event before claim mutation.
- `_progress_event_payload` · `_progress_event_payload(event: ProgressEventV1) -> dict[str, str | None]` · line 1947: Flatten a validated event into the additive claim storage contract.
- `claim_progress_issues` · `claim_progress_issues(claim: ClaimRecord, *, now: datetime | None = None) -> list[str]` · line 1962: Return instrumentation defects or an expired durable-progress lease.
- `claim_runtime_status` · `claim_runtime_status(claim: ClaimRecord, *, active_claims: list[ClaimRecord] | None = None, now: datetime | None = None) -> str` · line 2020: Classify one live claim across stale/stalled/weak/healthy states.
- `peer_claims_by_goal` · `peer_claims_by_goal(claims: 'list[ClaimRecord]') -> 'dict[str, list[ClaimRecord]]'` · line 2049: Group live claims that declare a byte-identical ``broader_goal``.
- `render_peer_claim_groups` · `render_peer_claim_groups(claims: 'list[ClaimRecord]') -> 'list[str]'` · line 2075: Render the shared-goal groups as display lines, or nothing when none.
- `claim_enforcement_issues` · `claim_enforcement_issues(claim: ClaimRecord) -> list[dict[str, str]]` · line 2088: Return blocking operator findings that require an explicit disposition.
- `validate_claim_for_creation` · `validate_claim_for_creation(claim: ClaimRecord) -> None` · line 2120: Reject new claims that omit required ownership metadata for live coordination.
- `_plan_number` · `_plan_number(plan_ref: str | None) -> int | None` · line 2155: Extract a numbered-plan identity from canonical claim spellings.
- `_resolve_commit` · `_resolve_commit(repo_root: Path, start_point: str, *, label: str) -> str` · line 2164: Resolve one commit-ish to a full immutable object ID.
- `_numbered_plan_digest` · `_numbered_plan_digest(repo_root: Path, revision: str, plan_number: int) -> str` · line 2174: Bind exact plan bytes even when structural integrity enforcement is off.
- `resolve_plan_authority_binding` · `resolve_plan_authority_binding(*, repo_root: str, plan_ref: str, start_point: str = 'HEAD', plan_repo_root: str | None = None, plan_start_point: str | None = None, target_repository_id: str | None = None) -> PlanAuthorityBinding` · line 2198: Resolve explicit plan authority separately from exact mutation-target custody.
- `resolve_canonical_work_unit_binding` · `resolve_canonical_work_unit_binding(*, repo_root: str, plan_ref: str, work_graph_path: str, work_unit_id: str, start_point: str = 'HEAD', plan_repo_root: str | None = None, plan_start_point: str | None = None, target_repository_id: str | None = None, method_receipt_ref: str | None = None, method_receipt_sha256: str | None = None) -> CanonicalWorkUnitBinding` · line 2259: Validate an owning plan graph and its target revision independently.
- `_parent_pid` · `_parent_pid(pid: int) -> int | None` · line 2413: Return a process's parent pid, or None when it cannot be read.
- `session_id_from_process_tree` · `session_id_from_process_tree(registry_dir: Path | None = None) -> str | None` · line 2426: Recover the owning Claude Code session id by walking process ancestry.
- `session_identity_aliases` · `session_identity_aliases(agent: str, resolved_session_id: str | None) -> tuple[str, ...]` · line 2455: Return every identity this process may legitimately claim ownership under.
- `resolve_session_id` · `resolve_session_id(agent: str, explicit_session_id: str | None = None) -> str | None` · line 2477: Return an explicit or environment-derived session identifier.
- `validate_native_session_binding` · `validate_native_session_binding(agent: str, session_id: str | None, *, require_native_marker: bool = False) -> None` · line 2508: Reject an explicit session identity that contradicts the native runtime.
- `_safe_string_list` · `_safe_string_list(value: Any) -> list[str]` · line 2543: Normalize a scalar-or-list YAML value into a clean string list.
- `_normalize_repo_path` · `_normalize_repo_path(path: str) -> str` · line 2564: Normalize a repo-relative path for parent/child overlap checks.
- `bootstrap_authority_disabled_worktree_path` · `bootstrap_authority_disabled_worktree_path(target_worktree_path: str) -> str` · line 2572: Return a deterministic non-Git path that older readers cannot authorize.
- `classify_broad_write_paths` · `classify_broad_write_paths(repo_root: str | None, write_paths: list[str], *, verified_new_files: set[str] | None = None) -> dict[str, str]` · line 2581: Classify root/top-level directory reservations without guessing.
- `_regular_top_level_files_at_revision` · `_regular_top_level_files_at_revision(repo_root: str | None, revision: str | None, write_paths: list[str]) -> set[str]` · line 2638: Return exact top-level regular files recorded by one retained Git tree.
- `_broad_scope_contract_issues` · `_broad_scope_contract_issues(claim: ClaimRecord) -> list[str]` · line 2676: Return deterministic schema-v6 broad-scope contract violations.
- `_projects_overlap` · `_projects_overlap(left: ClaimRecord, right: ClaimRecord) -> bool` · line 2782: Return whether two claims touch at least one common project.
- `_paths_overlap` · `_paths_overlap(left: str, right: str) -> bool` · line 2787: Return whether two normalized repo-relative paths overlap.
- `session_transcript_path` · `session_transcript_path(session_id: str | None, *, codex_root: Path | None = None, claude_root: Path | None = None) -> Path | None` · line 2800: Locate the runtime transcript one session is actually writing to.
- `session_last_active_at` · `session_last_active_at(session_id: str | None, *, codex_root: Path | None = None, claude_root: Path | None = None) -> datetime | None` · line 2833: Return when a session's own client last wrote, or None when unknowable.
- `describe_session_activity` · `describe_session_activity(last_active_at: datetime | None, *, now: datetime | None = None) -> str` · line 2854: Render one claim owner's liveness for an operator reading a conflict.
- `_is_append_only_path` · `_is_append_only_path(path: str) -> bool` · line 2874: Return whether a declared write path lands only in an append-only store.
- `_compute_overlapping_write_paths` · `_compute_overlapping_write_paths(candidate: ClaimRecord, other: ClaimRecord) -> list[str]` · line 2886: Return normalized write-path overlaps between two claims.
- `_overlap_relations` · `_overlap_relations(candidate: ClaimRecord, other: ClaimRecord) -> tuple[str, ...]` · line 2905: Classify every effective overlap from the candidate's perspective.
- `_reservation_kind` · `_reservation_kind(other: ClaimRecord, relations: tuple[str, ...]) -> str | None` · line 2926: Explain a parent reservation without changing conflict severity.
- `_current_diff_disjoint` · `_current_diff_disjoint(candidate: ClaimRecord, other: ClaimRecord) -> bool | None` · line 2938: Return advisory Git status disjointness, or unknown when unreadable.
- `_interaction_explanation` · `_interaction_explanation(candidate: ClaimRecord, other: ClaimRecord) -> dict[str, Any]` · line 2967: Build shared explanatory fields for one overlap interaction.
- `_git_worktree_boundary` · `_git_worktree_boundary(claim: ClaimRecord) -> tuple[Path, Path, Path, str] | None` · line 2982: Return verified repository, common-dir, worktree, and target kind.
- `_has_isolated_worktree_boundary` · `_has_isolated_worktree_boundary(candidate: ClaimRecord, other: ClaimRecord) -> bool` · line 3029: Return whether Git isolates the two overlapping mutation surfaces.
- `_has_write_ownership` · `_has_write_ownership(claim: ClaimRecord) -> bool` · line 3048: Return whether a claim owns its declared write paths.
- `_parse_iso_datetime` · `_parse_iso_datetime(value: Any) -> datetime | None` · line 3059: Parse an ISO timestamp from claim data if present.
- `_progress_text_with_presence` · `_progress_text_with_presence(data: dict[str, Any], key: str, *, null_is_invalid: bool = True) -> str | None` · line 3072: Preserve invalid explicit progress keys instead of erasing them as legacy absence.
- `normalize_claim` · `normalize_claim(data: dict[str, Any], *, source_file: str | None = None) -> ClaimRecord | None` · line 3088: Normalize a raw YAML claim into the v2 in-memory representation.
- `_load_claims` · `_load_claims(claims_dir: Path | None = None) -> list[ClaimRecord]` · line 3267: Load live claim files from the configured or explicitly supplied registry.
- `unregistered_claim_files` · `unregistered_claim_files() -> list[str]` · line 3320: Return claim-dir files that coordination tooling cannot parse as claims.
- `malformed_claim_files` · `malformed_claim_files(claims_dir: Path | None = None) -> list[dict[str, str]]` · line 3335: Return `.yaml` claim-dir files that exist but fail to parse as YAML.
- `_claim_filename` · `_claim_filename(agent: str, project: str, scope: str) -> str` · line 3365: Generate a deterministic filename for a claim.
- `check_claims` · `check_claims(project: str | None = None, *, claims_dir: Path | None = None) -> list[ClaimRecord]` · line 3374: Check active claims, optionally selecting a registry and project.
- `list_claims` · `list_claims(project: str | None = None, *, claims_dir: Path | None = None, include_inactive: bool = False) -> list[ClaimRecord]` · line 3382: List claims with an explicit option to retain non-live audit records.
- `evaluate_claim` · `evaluate_claim(candidate: ClaimRecord, *, active_claims: list[ClaimRecord] | None = None) -> ClaimCheckResult` · line 3398: Classify candidate claim interactions against active live claims.
- `build_candidate_claim` · `build_candidate_claim(*, agent: str, project: str, scope: str, intent: str, plan_ref: str | None = None, claim_type: str | None = None, write_paths: list[str] | None = None, read_paths: list[str] | None = None, worktree_path: str | None = None, repo_root: str | None = None, branch: str | None = None, session_name: str | None = None, broader_goal: str | None = None, tracker_path: str | None = None, session_id: str | None = None, heartbeat_at: str | None = None, status: str = 'active', parent_scope: str | None = None, notes: str | None = None, claimed_at: str | None = None, expires_at: str | None = None, updated_at: str | None = None, start_revision: str | None = None, plan_repo_root: str | None = None, plan_revision: str | None = None, plan_sha256: str | None = None, work_unit_id: str | None = None, work_graph_path: str | None = None, work_graph_sha256: str | None = None, approval_revisions: tuple[str, ...] = (), parallel_root_authorized: bool = False, progress_at: str | None = None, progress_kind: str | None = None, evidence_ref: str | None = None, next_action: str | None = None, expected_quiet_until: str | None = None, quiet_reason: str | None = None, broad_scope_mode: str | None = None, broad_scope_reason: str | None = None, target_worktree_path: str | None = None, contact_ref: str | None = None, new_files: list[str] | tuple[str, ...] | None = None, schema_version: int | None = None, method_receipt_ref: str | None = None, method_receipt_sha256: str | None = None) -> ClaimRecord` · line 3521: Build a normalized candidate claim from CLI or test inputs.
- `_refresh_exact_owner_claim` · `_refresh_exact_owner_claim(*, agent: str, project: str, scope: str, session_id: str | None, intent: str, plan_ref: str | None, claim_type: str | None, write_paths: list[str] | None, read_paths: list[str] | None, worktree_path: str | None, repo_root: str | None, branch: str | None, session_name: str | None, broader_goal: str | None, status: str, parent_scope: str | None, notes: str | None, allow_parallel: bool, broad_scope_mode: str | None, broad_scope_reason: str | None, target_worktree_path: str | None, ttl_hours: float) -> tuple[bool, str] | None` · line 3647: Expand an exact-owner live claim without reconstructing retained custody.
- `_tracker_path_yaml_error` · `_tracker_path_yaml_error(tracker_path: str | None) -> str | None` · line 3748: Why this tracker path cannot serve as a session tracker, or None.
- `_reject_unreadable_tracker_path` · `_reject_unreadable_tracker_path(tracker_path: str | None) -> None` · line 3790: Fail at claim time rather than stranding a lane at closeout.
- `create_claim` · `create_claim(agent: str, project: str, scope: str, intent: str, plan_ref: str | None = None, ttl_hours: float = DEFAULT_TTL_HOURS, claim_type: str | None = None, write_paths: list[str] | None = None, read_paths: list[str] | None = None, worktree_path: str | None = None, repo_root: str | None = None, branch: str | None = None, session_name: str | None = None, broader_goal: str | None = None, tracker_path: str | None = None, session_id: str | None = None, status: str = 'active', parent_scope: str | None = None, notes: str | None = None, work_graph_path: str | None = None, work_unit_id: str | None = None, start_point: str = 'HEAD', plan_repo_root: str | None = None, plan_start_point: str | None = None, resume_requested: bool = False, require_new: bool = False, allow_parallel: bool = False, require_native_session_binding: bool = False, require_native_session_marker: bool = False, broad_scope_mode: str | None = None, broad_scope_reason: str | None = None, target_worktree_path: str | None = None, contact_ref: str | None = None, new_files: list[str] | None = None, verified_goal_default_revision: str | None = None, verified_maintenance_default_revision: str | None = None, method_receipt_ref: str | None = None, method_receipt_sha256: str | None = None) -> tuple[bool, str]` · line 3798: Create a new claim after checking for hard conflicts.
- `_replacement_is_within_existing_authority` · `_replacement_is_within_existing_authority(replacement: str, existing: str) -> bool` · line 4130: Return whether one normalized replacement is equal to/below an old path.
- `_validate_bootstrap_target_identity` · `_validate_bootstrap_target_identity(claim: ClaimRecord) -> None` · line 4138: Require the separated bootstrap target to be the claimed Git branch/repository.
- `narrow_claim` · `narrow_claim(*, agent: str, project: str, scope: str, session_id: str | None, write_paths: list[str], claims_dir: Path | None = None, require_native_session_binding: bool = False, known_new_files: list[str] | None = None, start_revision: str | None = None) -> NarrowClaimResult` · line 4165: Commit one owner-only strict subset claim/projection transition.
- `hydrate_missing_session_ids` · `hydrate_missing_session_ids(*, agent: str, project: str, session_id: str | None = None, scope: str | None = None, branch: str | None = None) -> tuple[int, list[str], str]` · line 4303: Fill in missing session IDs for matching live claims.
- `_extended_lease_expiry` · `_extended_lease_expiry(current_expires_at: Any, renewed_at: str, ttl_hours: float) -> str` · line 4358: Return the later of a claim's current lease and one renewed at ``renewed_at``.
- `heartbeat_claims` · `heartbeat_claims(*, agent: str, project: str, session_id: str | None = None, scope: str | None = None, branch: str | None = None, claims_dir: Path | None = None, require_exact_session: bool = False, ttl_hours: float = DEFAULT_TTL_HOURS) -> tuple[int, list[str], str, str]` · line 4378: Refresh heartbeat metadata and the lease for live claims owned by one session.
- `record_progress_claims` · `record_progress_claims(*, agent: str, project: str, scope: str, progress_kind: str, evidence_ref: str, next_action: str, session_id: str | None = None, expected_quiet_until: str | datetime | None = None, quiet_reason: str | None = None, claims_dir: Path | None = None, require_native_session_binding: bool = False, now: datetime | None = None) -> tuple[ClaimRecord, ProgressEventV1]` · line 4480: Record durable advancement on exactly one live claim owned by this session.
- `end_session_claims` · `end_session_claims(*, agent: str, session_id: str | None = None, reason: str = 'session ended', claims_dir: Path | None = None) -> tuple[int, list[str], str, str]` · line 4591: Retire exact-session live ownership without deleting recovery state.
- `release_claim` · `release_claim(agent: str, project: str, scope: str, *, expected_session_id: str | None = None, expected_start_revision: str | None = None, allow_managed_lane_rollback: bool = False) -> tuple[bool, str]` · line 4651: Release an existing claim, optionally guarded by exact custody.
- `release_claims_for_branch` · `release_claims_for_branch(branch: str) -> tuple[int, list[str]]` · line 4719: Release every live canonical claim attached to one branch.
- `_archive_completed_claim_locked` · `_archive_completed_claim_locked(claim_file: Path, *, claims_dir: Path) -> tuple[ClaimRecord, claim_mutation_receipts.CompletedClaimArchiveReceiptV1]` · line 4745: Archive and remove one exact completed claim while the registry lock is held.
- `complete_claims_for_plan` · `complete_claims_for_plan(*, project: str, plan_ref: str, note: str | None = None) -> tuple[int, list[str]]` · line 4810: Mark matching live claims completed and return the affected scopes.
- `_matches_prune_selectors` · `_matches_prune_selectors(claim: ClaimRecord, *, agent: str | None, project: str | None, scope: str | None) -> bool` · line 4877: Return whether one normalized claim matches every supplied selector.
- `prune_expired` · `prune_expired(*, agent: str | None = None, project: str | None = None, scope: str | None = None) -> tuple[int, list[str]]` · line 4893: Remove selected expired claims and return count plus exact scope labels.
- `prune_stale` · `prune_stale(*, agent: str | None = None, project: str | None = None, scope: str | None = None) -> tuple[int, list[str]]` · line 4943: Remove selected stale live claims and return count plus scope labels.
- `prune_completed` · `prune_completed(*, agent: str | None = None, project: str | None = None, scope: str | None = None) -> tuple[int, list[str]]` · line 4995: Remove claims already marked complete/completed.
- `backfill_completed_claim_archive` · `backfill_completed_claim_archive(*, source_claim_snapshot: Path, expected_source_sha256: str, prune_event_id: str) -> tuple[claim_mutation_receipts.CompletedClaimArchiveReceiptV1, bool]` · line 5204: Archive one legacy completed claim using exact bytes and prune provenance.
- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 5266: Parse CLI arguments for coordination-claim management.
- `_validate_explicit_prune_selectors` · `_validate_explicit_prune_selectors(args: argparse.Namespace) -> None` · line 5465: Reject empty prune selectors before the registry lock can be acquired.
- `_render_check_output` · `_render_check_output(*, claims: list[ClaimRecord], project: str | None, candidate: ClaimRecord | None) -> dict[str, Any]` · line 5476: Build a structured report for list/check operations.
- `_render_mutation_audit_failure` · `_render_mutation_audit_failure(exc: MutationAuditError, *, as_json: bool) -> int` · line 5536: Report an already-applied mutation whose receipt could not be persisted.
- `_render_completed_claim_archive_failure` · `_render_completed_claim_archive_failure(exc: CompletedClaimArchiveError, *, as_json: bool) -> int` · line 5546: Report an archive-before-prune failure that left claim YAML unchanged.
- `main` · `main(argv: list[str] | None = None) -> int` · line 5560: Run the CLI for cross-brain coordination claim management.

### [`enforced_planning/coordination_messages.py`](../enforced_planning/coordination_messages.py)

Durable cross-client coordination messages and append-only receipts.

**Symbols**

- `CoordinationMessageError` · `CoordinationMessageError` · line 51: Base class for fail-loud mailbox contract and storage errors.
- `UnknownSessionError` · `UnknownSessionError` · line 55: Raised when no live claim or exact native client authorizes a session.
- `AmbiguousRecipientError` · `AmbiguousRecipientError` · line 59: Raised when a claim selector resolves to multiple recipient sessions.
- `IdentityMismatchError` · `IdentityMismatchError` · line 63: Raised when caller identity differs from the asserted sender identity.
- `RecordCollisionError` · `RecordCollisionError` · line 67: Raised when an immutable identifier is reused for different content.
- `CorruptRecordError` · `CorruptRecordError` · line 71: Raised after an unreadable or integrity-invalid record is quarantined.
- `MessageNotFoundError` · `MessageNotFoundError` · line 75: Raised when a requested canonical message does not exist.
- `WrongRecipientError` · `WrongRecipientError` · line 79: Raised when a session attempts to observe or acknowledge another inbox.
- `StrictContract` · `StrictContract` · line 83: Strict immutable base for every public mailbox boundary model.
- `ExactSessionSelector` · `ExactSessionSelector` · line 89: Select one recipient by canonical live session identity.
- `ClaimRecipientSelector` · `ClaimRecipientSelector` · line 96: Select one recipient through a live project claim.
- `SendMessageRequest` · `SendMessageRequest` · line 110: Typed command for persisting one immutable coordination message.
- `SendMessageRequest.require_exactly_one_content_source` · `require_exactly_one_content_source(self) -> SendMessageRequest` · line 147: Reject missing content and ambiguous dual inline/reference content.
- `PollMessagesRequest` · `PollMessagesRequest` · line 155: Typed command for reading one canonical session inbox.
- `AcknowledgeMessageRequest` · `AcknowledgeMessageRequest` · line 174: Typed command for appending one recipient acknowledgement.
- `MessageStatusRequest` · `MessageStatusRequest` · line 191: Typed command for deriving status from one message and its receipt set.
- `CoordinationMessage` · `CoordinationMessage` · line 198: Immutable resolved coordination intent persisted by the mailbox.
- `CoordinationMessage.validate_content_and_time` · `validate_content_and_time(self) -> CoordinationMessage` · line 228: Keep persisted content exclusive and expiry strictly after creation.
- `MessageReceipt` · `MessageReceipt` · line 238: Immutable evidence of runtime acceptance, observation, or acknowledgement.
- `MessageReceipt.validate_acknowledgement_fields` · `validate_acknowledgement_fields(self) -> MessageReceipt` · line 261: Prevent weaker receipt classes from carrying acknowledgement claims.
- `StoredMessageRecord` · `StoredMessageRecord` · line 273: Integrity envelope for one canonical message file.
- `StoredMessageRecord.validate_digest` · `validate_digest(self) -> StoredMessageRecord` · line 281: Reject storage bytes whose payload no longer matches its digest.
- `StoredReceiptRecord` · `StoredReceiptRecord` · line 289: Integrity envelope for one canonical receipt file.
- `StoredReceiptRecord.validate_digest` · `validate_digest(self) -> StoredReceiptRecord` · line 297: Reject storage bytes whose payload no longer matches its digest.
- `DeliveryEventRecord` · `DeliveryEventRecord` · line 305: Immutable duplicate-suppression marker for one displayed lifecycle event.
- `StoredDeliveryEventRecord` · `StoredDeliveryEventRecord` · line 319: Integrity envelope for one lifecycle duplicate-suppression marker.
- `StoredDeliveryEventRecord.validate_digest` · `validate_digest(self) -> StoredDeliveryEventRecord` · line 327: Reject marker bytes whose payload no longer matches its digest.
- `BoundaryBlockRecord` · `BoundaryBlockRecord` · line 335: Immutable evidence that active mailbox debt denied one lifecycle boundary.
- `BoundaryBlockRecord.validate_tool_boundary` · `validate_tool_boundary(self) -> BoundaryBlockRecord` · line 348: Only a tool boundary may retain a tool name.
- `StoredBoundaryBlockRecord` · `StoredBoundaryBlockRecord` · line 356: Integrity envelope for one immutable mailbox boundary denial.
- `StoredBoundaryBlockRecord.validate_digest` · `validate_digest(self) -> StoredBoundaryBlockRecord` · line 364: Reject boundary bytes whose payload no longer matches its digest.
- `MessageStatusView` · `MessageStatusView` · line 372: Derived lifecycle view computed from immutable message and receipts.
- `HostDeliveryCapabilityV1` · `HostDeliveryCapabilityV1` · line 394: Sender-visible local host capability for the recipient's client type.
- `_event_state_name` · `_event_state_name(event: str) -> str` · line 439: Render native CamelCase hook names as Codex state-table identifiers.
- `_configured_coordination_hook_command` · `_configured_coordination_hook_command(config: dict[str, Any], event: str, matcher: str, *, config_path: Path) -> str | None` · line 445: Return the enabled coordination adapter command for one exact hook surface.
- `_configured_adapter_issue` · `_configured_adapter_issue(client: str, commands: tuple[str, ...]) -> str | None` · line 477: Fail closed unless configured commands match the canonical adapter bytes.
- `inspect_host_delivery_capability` · `inspect_host_delivery_capability(session_id: str, *, codex_config_path: Path | None = None, claude_config_path: Path | None = None, scope: Literal['sender_host_recipient_client_config', 'operator_host_recipient_client_config'] = 'sender_host_recipient_client_config') -> HostDeliveryCapabilityV1` · line 546: Inspect local configured hook state without promoting it to runtime proof.
- `_looks_unreachable` · `_looks_unreachable(backlog: int, oldest_age_seconds: float | None) -> bool` · line 660: Treat an aged, never-observed backlog as evidence the recipient cannot read.
- `PersistedMessageResult` · `PersistedMessageResult` · line 668: Legacy V1 send result retained for strict consumer compatibility.
- `PersistedMessageResultV2` · `PersistedMessageResultV2` · line 693: Versioned send result that adds truthful sender-host delivery capability.
- `MessagePollResult` · `MessagePollResult` · line 705: Ordered inbox views and any observation receipts appended by polling.
- `AcknowledgementResult` · `AcknowledgementResult` · line 726: Acknowledgement receipt plus the resulting derived message status.
- `SessionInboxNotice` · `SessionInboxNotice` · line 739: Compact agent-facing projection of one lifecycle mailbox poll.
- `_canonical_json` · `_canonical_json(value: Any) -> bytes` · line 758: Serialize one JSON-compatible value deterministically for identity and storage.
- `_model_digest` · `_model_digest(model: BaseModel) -> str` · line 764: Hash one strict model in JSON mode using canonical ordering.
- `_receipt_set_digest` · `_receipt_set_digest(receipts: list[MessageReceipt]) -> str` · line 770: Hash the exact ordered receipt payload set used by a status projection.
- `_utc_now` · `_utc_now() -> datetime` · line 777: Return an aware UTC timestamp for default runtime operations.
- `_fsync_directory` · `_fsync_directory(path: Path) -> None` · line 783: Durably commit a directory-entry change before reporting success.
- `_stable_id` · `_stable_id(prefix: str, *parts: str) -> str` · line 793: Build a collision-resistant deterministic ID from a namespaced tuple.
- `CoordinationMessageStore` · `CoordinationMessageStore` · line 800: Filesystem authority for immutable messages, receipts, and derived views.
- `CoordinationMessageStore._index_key` · `_index_key(session_id: str) -> str` · line 831: Derive one path-safe directory name for an arbitrary session identity.
- `CoordinationMessageStore._record_ids` · `_record_ids(directory: Path, *, suffix: str = '') -> set[str]` · line 837: List record identifiers in one directory without reading any record.
- `CoordinationMessageStore._write_marker` · `_write_marker(path: Path) -> None` · line 854: Create one empty derived-index marker, tolerating a concurrent writer.
- `CoordinationMessageStore._index_message` · `_index_message(self, message: CoordinationMessage) -> None` · line 873: Publish the derived lookup markers for one canonical message.
- `CoordinationMessageStore._index_receipt` · `_index_receipt(self, receipt: MessageReceipt) -> None` · line 890: Publish the derived lookup marker for one canonical receipt.
- `CoordinationMessageStore._refresh_message_index` · `_refresh_message_index(self) -> None` · line 898: Backfill messages published without a derived index, once per instance.
- `CoordinationMessageStore._refresh_receipt_index` · `_refresh_receipt_index(self) -> None` · line 910: Backfill receipts published without a derived index, once per instance.
- `CoordinationMessageStore._indexed_messages` · `_indexed_messages(self, index_root: Path, session_id: str) -> list[tuple[CoordinationMessage, Path]]` · line 922: Load only the messages one session owns, in deterministic creation order.
- `CoordinationMessageStore._drop_orphan_marker` · `_drop_orphan_marker(self, path: Path) -> None` · line 938: Remove one derived marker whose canonical record no longer exists.
- `CoordinationMessageStore._messages_for_recipient` · `_messages_for_recipient(self, session_id: str) -> list[tuple[CoordinationMessage, Path]]` · line 946: Return every message addressed to one exact recipient session.
- `CoordinationMessageStore._messages_for_sender` · `_messages_for_sender(self, session_id: str) -> list[tuple[CoordinationMessage, Path]]` · line 951: Return every message sent by one exact session.
- `CoordinationMessageStore._live_claims` · `_live_claims(self, project: str | None = None) -> list[coordination_claims.ClaimRecord]` · line 956: Read canonical live identity records without introducing another registry.
- `CoordinationMessageStore._require_live_session` · `_require_live_session(self, session_id: str) -> None` · line 973: Fail when a caller or exact recipient is absent from live claims.
- `CoordinationMessageStore._reachable_recipient_claims` · `_reachable_recipient_claims(self, project: str | None = None, *, now: datetime | None = None) -> list[coordination_claims.ClaimRecord]` · line 979: Live claims plus recently-ended ones, for RECIPIENT resolution only.
- `CoordinationMessageStore.resolve_recipient` · `resolve_recipient(self, selector: RecipientSelector, *, now: datetime | None = None) -> str` · line 1041: Resolve an exact or claim-backed selector to one canonical session.
- `CoordinationMessageStore._quarantine` · `_quarantine(self, path: Path, reason: str) -> NoReturn` · line 1069: Move one corrupt record out of the canonical scan path and retain its evidence.
- `CoordinationMessageStore._read_message_path` · `_read_message_path(self, path: Path) -> CoordinationMessage` · line 1084: Validate one message record, quarantining malformed or digest-invalid content.
- `CoordinationMessageStore._read_receipt_path` · `_read_receipt_path(self, path: Path) -> MessageReceipt` · line 1093: Validate one receipt record, quarantining malformed or digest-invalid content.
- `CoordinationMessageStore._read_delivery_path` · `_read_delivery_path(self, path: Path) -> DeliveryEventRecord` · line 1102: Validate one marker before treating an event as already delivered.
- `CoordinationMessageStore._write_immutable` · `_write_immutable(self, path: Path, payload: bytes) -> bool` · line 1111: Atomically publish immutable bytes without overwriting an existing identifier.
- `CoordinationMessageStore._store_message` · `_store_message(self, message: CoordinationMessage) -> tuple[Path, bool]` · line 1132: Persist one integrity-wrapped message or verify an idempotent replay.
- `CoordinationMessageStore._store_receipt` · `_store_receipt(self, receipt: MessageReceipt) -> tuple[Path, bool]` · line 1151: Append one integrity-wrapped receipt or verify an idempotent replay.
- `CoordinationMessageStore._claim_event_delivery` · `_claim_event_delivery(self, message: CoordinationMessage, *, display_session_id: str | None = None, delivery_event_id: str, now: datetime) -> bool` · line 1171: Atomically reserve one agent-visible delivery for a native event.
- `CoordinationMessageStore.poll_sender_acknowledgements` · `poll_sender_acknowledgements(self, *, current_session_id: str, project: str | None = None, consume: bool = True, limit: int = DEFAULT_NOTICE_MESSAGE_LIMIT, now: datetime | None = None) -> tuple[MessageStatusView, ...]` · line 1212: Return acknowledgements not yet surfaced to the exact sender session.
- `CoordinationMessageStore._message` · `_message(self, message_id: str) -> tuple[CoordinationMessage, Path]` · line 1261: Load one canonical message or fail when it is absent.
- `CoordinationMessageStore._all_messages` · `_all_messages(self) -> list[tuple[CoordinationMessage, Path]]` · line 1269: Load every canonical message in deterministic creation order.
- `CoordinationMessageStore._receipts_for` · `_receipts_for(self, message_id: str) -> list[MessageReceipt]` · line 1277: Load and order only the receipts recorded against one message.
- `CoordinationMessageStore.assess_recipient_reachability` · `assess_recipient_reachability(self, recipient_session_id: str, *, now: datetime, before: datetime | None = None) -> tuple[int, float | None]` · line 1299: Count active messages the recipient has never once observed.
- `CoordinationMessageStore.send` · `send(self, request: SendMessageRequest, *, now: datetime | None = None, require_live_claim: bool = True) -> PersistedMessageResultV2` · line 1331: Resolve identities and persist one immutable coordination message.
- `CoordinationMessageStore._append_observation` · `_append_observation(self, message: CoordinationMessage, *, now: datetime) -> tuple[MessageReceipt, Path]` · line 1416: Append or reuse one observation receipt for the exact recipient.
- `CoordinationMessageStore.record_boundary_block` · `record_boundary_block(self, *, current_session_id: str, message_ids: tuple[str, ...], hook_event_name: Literal['PreToolUse', 'Stop'], delivery_event_id: str, tool_name: str | None = None, now: datetime | None = None) -> tuple[BoundaryBlockRecord, ...]` · line 1430: Append idempotent evidence that active mailbox debt denied a boundary.
- `CoordinationMessageStore.boundary_blocks` · `boundary_blocks(self, message_id: str) -> tuple[BoundaryBlockRecord, ...]` · line 1487: Return validated boundary-denial evidence for one message in time order.
- `CoordinationMessageStore.status` · `status(self, request: MessageStatusRequest) -> MessageStatusView` · line 1502: Derive lifecycle state from one immutable message and exact receipt set.
- `CoordinationMessageStore.poll` · `poll(self, request: PollMessagesRequest, *, now: datetime | None = None, require_live_claim: bool = True, max_messages: int | None = None, active_only: bool = False) -> MessagePollResult` · line 1540: Read one session inbox and optionally append observation receipts.
- `CoordinationMessageStore.acknowledge` · `acknowledge(self, request: AcknowledgeMessageRequest, *, now: datetime | None = None, require_live_claim: bool = True) -> AcknowledgementResult` · line 1612: Append one recipient acknowledgement without mutating message state.
- `default_message_root` · `default_message_root(claims_dir: Path | None = None) -> Path` · line 1660: Derive the mailbox authority beside the configured canonical claims directory.
- `poll_session_inbox` · `poll_session_inbox(*, agent: str, project: str | None, session_id: str | None = None, observe: bool = True, claims_dir: Path | None = None, root: Path | None = None, max_body_chars: int = DEFAULT_NOTICE_BODY_LENGTH, max_messages: int = DEFAULT_NOTICE_MESSAGE_LIMIT, delivery_event_id: str | None = None, require_live_claim: bool = True) -> SessionInboxNotice` · line 1666: Resolve one native session and return an agent-visible mailbox notice.
- `_request_json` · `_request_json(raw: str) -> str` · line 1810: Read a request from an inline JSON string or stdin marker.
- `_is_current_native_session` · `_is_current_native_session(session_id: str) -> bool` · line 1816: Return whether ambient client identity exactly matches one canonical ID.
- `build_parser` · `build_parser() -> argparse.ArgumentParser` · line 1825: Build the agent-drivable JSON request CLI.
- `main` · `main(argv: list[str] | None = None) -> int` · line 1842: Execute one typed mailbox operation and print a strict JSON result.

### [`enforced_planning/doc_authority.py`](../enforced_planning/doc_authority.py)

Authority-drift reconciliation storage and validation.

**Symbols**

- `AuthorityRule` · `AuthorityRule` · line 37: One configured indexed authority rule for a governed repo.
- `RequiredContextEntry` · `RequiredContextEntry` · line 48: One additional mandatory read attached to a doc-spine node.
- `AuthorityDocEntry` · `AuthorityDocEntry` · line 57: One authority-bearing document in the recursive documentation spine.
- `CodeSurfaceEntry` · `CodeSurfaceEntry` · line 71: One bounded code-surface mapping into the doc spine.
- `RoleBudget` · `RoleBudget` · line 79: Configured size budget for one document role.
- `DocSpineConfig` · `DocSpineConfig` · line 87: Repo-level recursive documentation-spine settings.
- `DocSpineContext` · `DocSpineContext` · line 97: Resolved doc-spine closure for one managed code surface.
- `DocAuthorityConfig` · `DocAuthorityConfig` · line 111: Parsed documentation-authority config for one repo.
- `AuthorityObligation` · `AuthorityObligation` · line 124: One unresolved or resolved reconciliation obligation.
- `AuthorityObligation.to_dict` · `to_dict(self) -> dict[str, Any]` · line 143: Return a JSON/YAML-safe payload.
- `AuthorityIssue` · `AuthorityIssue` · line 152: One validation finding for doc-authority drift.
- `AuthorityIssue.to_dict` · `to_dict(self) -> dict[str, Any]` · line 163: Return a JSON-safe issue payload.
- `_normalize_repo_path` · `_normalize_repo_path(path: str) -> str` · line 169: Normalize a repo-relative path for overlap checks.
- `_paths_overlap` · `_paths_overlap(left: str, right: str) -> bool` · line 177: Return whether two repo-relative paths overlap.
- `_path_matches` · `_path_matches(pattern: str, candidate: str) -> bool` · line 189: Return whether one configured code-surface path matches a candidate.
- `_parse_yaml_mapping` · `_parse_yaml_mapping(path: Path) -> dict[str, Any]` · line 199: Load one YAML mapping from disk.
- `_severity_rank` · `_severity_rank(value: str) -> int` · line 210: Return deterministic severity sorting order.
- `_normalize_plan_status` · `_normalize_plan_status(raw_status: str) -> str` · line 216: Return the stable status marker used by plan docs and their index.
- `_parse_plan_doc_status` · `_parse_plan_doc_status(plan_path: Path) -> tuple[str, str] | None` · line 238: Return one plan number plus normalized status marker.
- `_parse_plan_index` · `_parse_plan_index(index_path: Path) -> dict[str, str]` · line 251: Return artifact-or-number to status-marker mapping from the plan index.
- `_repo_project_name` · `_repo_project_name(repo_root: Path) -> str` · line 273: Return the canonical project name for a repo or worktree root.
- `_resolve_config_path` · `_resolve_config_path(repo_root: Path, config_path: Path | None = None) -> Path` · line 279: Resolve the effective doc-authority config path for a repo or worktree.
- `_require_nonempty_str` · `_require_nonempty_str(value: Any, *, field_name: str, config_path: Path) -> str` · line 290: Return one required non-empty string field from config.
- `_coerce_int` · `_coerce_int(value: Any, *, field_name: str, config_path: Path) -> int | None` · line 298: Parse one optional integer field from config.
- `_coerce_str_tuple` · `_coerce_str_tuple(value: Any, *, field_name: str, config_path: Path) -> tuple[str, ...]` · line 316: Normalize one string-or-list-of-strings field into a tuple.
- `_parse_required_context_entries` · `_parse_required_context_entries(raw_entries: Any, *, config_path: Path) -> tuple[RequiredContextEntry, ...]` · line 329: Parse required-context items from config.
- `_parse_indexed_authority_rules` · `_parse_indexed_authority_rules(payload: dict[str, Any], *, config_path: Path) -> tuple[AuthorityRule, ...]` · line 350: Parse indexed authority rules from config.
- `_parse_doc_spine` · `_parse_doc_spine(payload: dict[str, Any], *, config_path: Path) -> DocSpineConfig | None` · line 369: Parse repo-level doc-spine settings from config.
- `_parse_role_budgets` · `_parse_role_budgets(payload: dict[str, Any], *, config_path: Path) -> dict[str, RoleBudget]` · line 385: Parse role budgets from config.
- `_parse_docs` · `_parse_docs(payload: dict[str, Any], *, config_path: Path) -> tuple[AuthorityDocEntry, ...]` · line 403: Parse authority-bearing docs from config.
- `_parse_code_surfaces` · `_parse_code_surfaces(payload: dict[str, Any], *, config_path: Path) -> tuple[CodeSurfaceEntry, ...]` · line 434: Parse bounded code-surface mappings from config.
- `load_doc_authority_config` · `load_doc_authority_config(repo_root: Path, *, config_path: Path | None = None) -> DocAuthorityConfig` · line 456: Load the full doc-authority config for one repo.
- `load_authority_rules` · `load_authority_rules(repo_root: Path, *, config_path: Path | None = None) -> list[AuthorityRule]` · line 475: Load indexed doc-authority rules for one repo.
- `_doc_map` · `_doc_map(config: DocAuthorityConfig) -> dict[str, AuthorityDocEntry]` · line 481: Return path to doc-entry mapping for one config.
- `_resolve_repo_file` · `_resolve_repo_file(repo_root: Path, relative_path: str) -> Path` · line 487: Resolve one repo-relative path from the active repo or worktree root.
- `_word_count` · `_word_count(path: Path) -> int` · line 493: Return a simple whitespace-based word count for one file.
- `_dedupe_paths` · `_dedupe_paths(paths: list[str]) -> tuple[str, ...]` · line 501: Return a stable deduplicated path tuple.
- `_dedupe_required_context` · `_dedupe_required_context(entries: list[RequiredContextEntry]) -> tuple[RequiredContextEntry, ...]` · line 515: Return stable deduplicated required-context entries by path.
- `_build_doc_chain` · `_build_doc_chain(config: DocAuthorityConfig, start_path: str) -> list[AuthorityDocEntry]` · line 528: Resolve one doc plus its ancestor chain.
- `_match_code_surface` · `_match_code_surface(config: DocAuthorityConfig, file_path: str) -> CodeSurfaceEntry | None` · line 549: Return the matching bounded code surface for one file path, if any.
- `get_doc_spine_context` · `get_doc_spine_context(repo_root: Path, file_path: str, *, config_path: Path | None = None, config: DocAuthorityConfig | None = None) -> DocSpineContext | None` · line 559: Return the resolved doc-spine closure for one managed file, if any.
- `list_obligations` · `list_obligations(*, project: str | None = None, concern: str | None = None, status: str | None = None) -> list[AuthorityObligation]` · line 604: Return authority obligations filtered by project/concern/status.
- `record_obligation` · `record_obligation(*, project: str, concern: str, authority_surface: str, artifact_path: str, required_action: str, created_by_agent: str, created_by_scope: str, plan_ref: str | None = None, owner_scope: str | None = None, notes: str | None = None) -> AuthorityObligation` · line 646: Create or return one open authority reconciliation obligation.
- `resolve_obligation` · `resolve_obligation(*, obligation_id: str, notes: str | None = None) -> AuthorityObligation` · line 697: Mark one obligation resolved and return the updated record.
- `_owner_claims_for_surface` · `_owner_claims_for_surface(project: str, authority_surface: str) -> list[coordination_claims.ClaimRecord]` · line 715: Return live write claims that own one authority surface.
- `_matching_open_obligations` · `_matching_open_obligations(*, project: str, concern: str, authority_surface: str, artifact_path: str) -> list[AuthorityObligation]` · line 728: Return open obligations for one concrete drift item.
- `_issue` · `_issue(*, code: str, severity: str, concern: str, authority_surface: str, artifact_path: str, message: str, evidence: dict[str, Any]) -> AuthorityIssue` · line 747: Build one authority validation issue.
- `_validate_plan_index_rule` · `_validate_plan_index_rule(repo_root: Path, rule: AuthorityRule) -> list[AuthorityIssue]` · line 770: Validate one indexed plan authority surface.
- `_validate_doc_spine` · `_validate_doc_spine(repo_root: Path, config: DocAuthorityConfig) -> list[AuthorityIssue]` · line 880: Validate the bounded recursive doc spine for one repo.
- `validate_doc_authority` · `validate_doc_authority(repo_root: Path, *, config_path: Path | None = None) -> list[AuthorityIssue]` · line 1159: Return sorted authority validation issues for one repo.
- `unresolved_owned_obligations` · `unresolved_owned_obligations(claim: coordination_claims.ClaimRecord) -> list[AuthorityObligation]` · line 1184: Return unresolved obligations against surfaces owned by one claim.
- `assert_no_unresolved_owned_obligations` · `assert_no_unresolved_owned_obligations(claim: coordination_claims.ClaimRecord) -> None` · line 1198: Fail loud when one lane owns an authority surface with open debt.

### [`enforced_planning/docstring_wiki.py`](../enforced_planning/docstring_wiki.py)

Render a deterministic whole-repository wiki from source-local summaries.

**Symbols**

- `_first_paragraph` · `_first_paragraph(text: str | None) -> str | None` · line 35: Compress one real docstring paragraph for the generated navigation view.
- `_inline_code` · `_inline_code(value: str) -> str` · line 46: Render stable Markdown code even when a source name contains backticks.
- `_artifact_link` · `_artifact_link(path: str, *, output_dir: str) -> str` · line 53: Relative, percent-encoded link from the generated page to one tracked artifact.
- `_artifact_lines` · `_artifact_lines(artifact: ArtifactRecord, *, self_path: str | None, output_dir: str = '.') -> list[str]` · line 64: Render one tracked artifact and its documented Python symbols.
- `render_docstring_wiki` · `render_docstring_wiki(repo_root: Path, *, output_path: Path = DEFAULT_OUTPUT) -> str` · line 93: Render every tracked artifact into a deterministic Markdown projection.
- `check_docstring_wiki` · `check_docstring_wiki(repo_root: Path, *, output_path: Path = DEFAULT_OUTPUT) -> tuple[bool, str]` · line 135: Compare generated output byte-for-byte without rewriting the worktree.
- `main` · `main(argv: list[str] | None = None) -> int` · line 149: Generate, check, or print the deterministic docstring wiki.

### [`enforced_planning/effective_project_profile.py`](../enforced_planning/effective_project_profile.py)

Resolve one portable, explainable governed-project profile.

**Symbols**

- `EffectiveControlV1` · `EffectiveControlV1` · line 15: One configured value and the value effective after master policy.
- `EffectiveProjectProfileV1` · `EffectiveProjectProfileV1` · line 24: Machine-readable effective state for the portable framework.
- `resolve_effective_project_profile` · `resolve_effective_project_profile(payload: dict[str, Any] | None) -> EffectiveProjectProfileV1` · line 65: Resolve defaults and master override without mutating source configuration.
- `load_effective_project_profile` · `load_effective_project_profile(repo_root: Path) -> EffectiveProjectProfileV1` · line 98: Load ``meta-process.yaml`` when present; absence uses default-on policy.

### [`enforced_planning/file_context.py`](../enforced_planning/file_context.py)

Load and print context relationships for files from scripts/relationships.yaml.

**Symbols**

- `_normalize_scope_mode` · `_normalize_scope_mode(raw: Any, *, default: str) -> str` · line 76: Normalize a file-scope policy mode into canonical values.
- `_get_file_scope_config` · `_get_file_scope_config(relationships: dict[str, Any]) -> dict[str, Any]` · line 95: Extract and normalize file_scope settings from relationships config.
- `_is_managed_file` · `_is_managed_file(file_path: str, scope_config: dict[str, Any]) -> bool` · line 156: Whether a file path is within managed scope for gating policy.
- `ReadCheckResult` · `ReadCheckResult` · line 172: Result container for `check_required_reads` with optional scope policy metadata.
- `ReadCheckResult.__iter__` · `__iter__(self)` · line 181: Yield the three legacy fields for unpack compatibility.
- `load_relationships` · `load_relationships(repo_root: Path | None = None, config_path: str | Path | None = None) -> dict[str, Any]` · line 232: Load a consumer repository's relationship graph.
- `_resolve_authority_config_path` · `_resolve_authority_config_path(repo_root: Path, authority_config_path: str | Path | None) -> Path | None` · line 366: Return the effective doc-authority config path if one exists.
- `_any_seen_matches_glob` · `_any_seen_matches_glob(pattern: str, seen: set[str]) -> bool` · line 507: Check if any seen read matches a glob pattern in required reads.
- `check_required_reads` · `check_required_reads(file_path: str, relationships: dict[str, Any], reads_file: Path, *, repo_root: Path | None = None, authority_config_path: str | Path | None = None) -> ReadCheckResult` · line 525: Check whether file-specific required reads were completed for a given file.
- `main` · `main() -> int` · line 619: CLI entrypoint for resolving file context and read requirements.

_Coverage findings: python-docstring-missing._

### [`enforced_planning/impact_obligations.py`](../enforced_planning/impact_obligations.py)

Derive auditable reconciliation obligations from changed relationship nodes.

**Symbols**

- `ImpactObligationError` · `ImpactObligationError` · line 33: Report malformed change, revision, or disposition evidence.
- `ReconciliationDisposition` · `ReconciliationDisposition` · line 38: Record one reviewed resolution that cannot be inferred from changed files.
- `ImpactObligation` · `ImpactObligation` · line 49: Require one linked artifact to be reconciled after a source change.
- `ImpactReport` · `ImpactReport` · line 67: Summarize deterministic reconciliation state for one repository diff.
- `ImpactReport.to_json` · `to_json(self, *, pretty: bool = False) -> str` · line 78: Serialize a stable report for hooks, CI, and agents.
- `current_revision` · `current_revision(repo_root: Path) -> str` · line 90: Return repository HEAD for provenance, not as a working-diff review token.
- `review_revision` · `review_revision(repo_root: Path, *, base: str, staged: bool = False) -> str` · line 105: Fingerprint HEAD, comparison mode, base, and exact diff under review.
- `changed_paths` · `changed_paths(repo_root: Path, *, base: str, staged: bool = False) -> tuple[str, ...]` · line 131: Return a NUL-safe changed path set from the requested Git comparison.
- `_obligation_id` · `_obligation_id(changed_path: str, related_path: str, related_symbol: str | None, spec: RelationshipSpec) -> str` · line 148: Derive a stable obligation id from semantic edge identity, not line numbers.
- `load_dispositions` · `load_dispositions(path: Path | None) -> tuple[ReconciliationDisposition, ...]` · line 164: Load and validate optional reviewed reconciliation dispositions.
- `_apply_disposition` · `_apply_disposition(obligation_id: str, *, revision: str, disposition: ReconciliationDisposition | None, tracked_paths: set[str]) -> tuple[ObligationStatus, str | None, str | None]` · line 199: Validate one reviewed disposition against current revision and inventory.
- `plan_lifecycle` · `plan_lifecycle(path: Path) -> PlanLifecycle` · line 227: Classify a plan's declared status without treating its filename as truth.
- `build_impact_report` · `build_impact_report(repo_root: Path, changed: tuple[str, ...], relationships: dict[str, Any], *, revision: str, dispositions: tuple[ReconciliationDisposition, ...] = ()) -> ImpactReport` · line 259: Derive and resolve maintenance obligations for an exact changed-file set.
- `_load_relationships` · `_load_relationships(repo_root: Path, config_path: str | Path) -> dict[str, Any]` · line 366: Load a relationship mapping for the impact-report CLI.
- `main` · `main(argv: list[str] | None = None) -> int` · line 380: Run report-only or strict reconciliation checks for a Git comparison.

### [`enforced_planning/integration_authority.py`](../enforced_planning/integration_authority.py)

Canonical-claim authority for the hook-governed pull-request finish path.

**Symbols**

- `IntegrationAuthorityError` · `IntegrationAuthorityError` · line 33: Raised when an exact native branch owner cannot integrate one PR head.
- `_claim_authority_sha256` · `_claim_authority_sha256(claim: coordination_claims.ClaimRecord) -> str` · line 163: Hash stable custody fields, excluding expected heartbeat/progress churn.
- `_strict_active_claims` · `_strict_active_claims(*, project: str, claims_dir: Path | None, now: datetime) -> list[coordination_claims.ClaimRecord]` · line 300: Load one complete locked registry view or fail on any malformed record.
- `assert_integration_authority` · `assert_integration_authority(*, target: IntegrationTargetV1, agent: str, repo_root: Path, review_spec_path: Path, claims_dir: Path | None = None, now: datetime | None = None, validity: timedelta = timedelta(seconds=DEFAULT_ASSERTION_SECONDS), lock_registry: bool = True) -> IntegrationAuthorityAssertionV1` · line 361: Build a digest-bound assertion from the current canonical branch claim.
- `validate_integration_authority` · `validate_integration_authority(assertion: IntegrationAuthorityAssertionV1, *, expected_target: IntegrationTargetV1, agent: str, repo_root: Path, review_spec_path: Path, claims_dir: Path | None = None, now: datetime | None = None, lock_registry: bool = True) -> None` · line 421: Reject a stale assertion or any change to target, owner, or claim bytes.
- `integration_authority_guard` · `integration_authority_guard(assertion: IntegrationAuthorityAssertionV1, *, expected_target: IntegrationTargetV1, agent: str, repo_root: Path, review_spec_path: Path, claims_dir: Path | None = None, now: datetime | None = None) -> Iterator[None]` · line 471: Hold claim custody stable across the final remote head CAS operation.

_Coverage findings: python-docstring-missing._

### [`enforced_planning/mailbox_execution_identity.py`](../enforced_planning/mailbox_execution_identity.py)

Classify mailbox callbacks by proven native root/child identity.

**Symbols**

- `PrimaryExecutionDecisionV1` · `PrimaryExecutionDecisionV1` · line 19: Root/child classification consumed before any mailbox access.
- `classify_hook_execution` · `classify_hook_execution(payload: dict[str, object], *, client: Literal['codex', 'claude-code']) -> PrimaryExecutionDecisionV1` · line 34: Classify one callback from stable native identity fields only.

### [`enforced_planning/notebook_registry_validation.py`](../enforced_planning/notebook_registry_validation.py)

Validate notebook registries and registered journey notebooks.

**Symbols**

- `NotebookRegistryValidationResult` · `NotebookRegistryValidationResult` · line 42: Validation result for notebook registry checks.
- `NotebookRegistryValidationResult.ok` · `ok(self) -> bool` · line 51: Return True when no hard validation errors were found.
- `NotebookRegistryValidationResult.to_dict` · `to_dict(self) -> dict[str, Any]` · line 55: Return a JSON-serializable representation of the result.
- `load_yaml` · `load_yaml(path: Path) -> dict[str, Any]` · line 60: Load YAML from disk and normalize empty documents to an empty mapping.
- `load_notebook_registry` · `load_notebook_registry(path: Path) -> dict[str, Any]` · line 71: Load the notebook registry YAML document from disk.
- `resolve_workspace_path` · `resolve_workspace_path(raw_path: str, *, workspace_root: Path | None = None) -> Path` · line 76: Resolve a registry path relative to the shared workspace root.
- `resolve_registered_path` · `resolve_registered_path(raw_path: str, *, workspace_root: Path, repo_root: Path) -> Path` · line 82: Resolve a registry path that may be workspace-relative or repo-relative.
- `load_notebook` · `load_notebook(path: Path) -> dict[str, Any]` · line 99: Load and validate notebook JSON structure from disk.
- `_to_list` · `_to_list(value: Any) -> list[str]` · line 111: Normalize a scalar or list value into a list of non-empty strings.
- `_markdown_texts` · `_markdown_texts(notebook: dict[str, Any]) -> list[str]` · line 121: Return normalized markdown cell text for a notebook.
- `_validate_registry_top_level` · `_validate_registry_top_level(registry: dict[str, Any], result: NotebookRegistryValidationResult) -> list[dict[str, Any]]` · line 135: Validate required registry top-level fields and return journey entries.
- `_validate_file_list` · `_validate_file_list(values: list[str], *, label: str, journey_id: str, result: NotebookRegistryValidationResult, workspace_root: Path, repo_root: Path) -> None` · line 151: Validate that each workspace-relative file path in a list exists.
- `_validate_notebook_header` · `_validate_notebook_header(notebook: dict[str, Any], *, journey: dict[str, Any], result: NotebookRegistryValidationResult) -> None` · line 173: Validate the visible header contract near the top of the notebook.
- `_validate_notebook_metadata` · `_validate_notebook_metadata(notebook: dict[str, Any], *, journey: dict[str, Any], phase_ids: list[str], result: NotebookRegistryValidationResult) -> None` · line 194: Validate notebook-level machine-readable metadata against the registry.
- `_validate_phase_sections` · `_validate_phase_sections(notebook: dict[str, Any], *, journey: dict[str, Any], phases: list[dict[str, Any]], result: NotebookRegistryValidationResult) -> None` · line 230: Validate that each registered phase has an explicit visible contract cell.
- `_validate_proof_mode` · `_validate_proof_mode(*, journey: dict[str, Any], phases: list[dict[str, Any]], result: NotebookRegistryValidationResult) -> None` · line 277: Enforce proof-mode semantics for proof-critical phases.
- `_validate_phase_entries` · `_validate_phase_entries(phases: list[dict[str, Any]], *, journey_id: str, result: NotebookRegistryValidationResult, workspace_root: Path, repo_root: Path) -> list[str]` · line 297: Validate phase entry shape and return phase IDs in declared order.
- `validate_notebook_registry` · `validate_notebook_registry(registry: dict[str, Any], *, registry_path: Path, journey_id: str | None = None, workspace_root: Path | None = None) -> NotebookRegistryValidationResult` · line 354: Validate the notebook registry and all selected journey entries.
- `print_human_readable` · `print_human_readable(result: NotebookRegistryValidationResult) -> None` · line 472: Print a concise human-readable validation summary.
- `main` · `main(argv: Sequence[str] | None = None, *, repo_root: Path | None = None, workspace_root: Path | None = None) -> int` · line 492: Run notebook registry validation from the command line.

### [`enforced_planning/outcome_admission.py`](../enforced_planning/outcome_admission.py)

Production outcome-admission ordering for the first Enforced Planning consumer.

**Symbols**

- `_mapping` · `_mapping(value: object, *, field_name: str) -> dict[str, Any]` · line 108: Return one strict configuration mapping or fail visibly.
- `load_outcome_admission_mode` · `load_outcome_admission_mode(repo_root: Path) -> OutcomeAdmissionMode` · line 116: Load the strict repo-local outcome-admission mode.
- `StrictModel` · `StrictModel` · line 153: Strict immutable base for admission contracts.
- `OutcomeAdmissionRequestV1` · `OutcomeAdmissionRequestV1` · line 159: One already-authorized operation classified for outcome admission.
- `OutcomeAdmissionDecisionV1` · `OutcomeAdmissionDecisionV1` · line 181: Stable production admission result.
- `OutcomeAdmissionBootstrapV1` · `OutcomeAdmissionBootstrapV1` · line 189: Exact write scope requested for the first-consumer allocation bootstrap.
- `OutcomeAdmissionBootstrapResultV1` · `OutcomeAdmissionBootstrapResultV1` · line 204: Bootstrap classification plus the canonical production decision.
- `SelectedOutcomeAdmissionEvidenceV1` · `SelectedOutcomeAdmissionEvidenceV1` · line 242: Exact canonical state used to derive one selected admission request.
- `SelectionPendingActivationEvidenceV1` · `SelectionPendingActivationEvidenceV1` · line 286: Exact current reservation allowed to create only its first session tracker.
- `SelectionPendingActivationResultV1` · `SelectionPendingActivationResultV1` · line 320: A separately versioned tracker-attachment result, never selected admission.
- `SelectionPendingActivationReceiptV1` · `SelectionPendingActivationReceiptV1` · line 345: Append-only staged-activation receipt isolated from admission v1 readers.
- `OutcomeAdmissionResultV1` · `OutcomeAdmissionResultV1` · line 364: One bootstrap or exact-selected result before an entrypoint mutation.
- `OutcomeAdmissionReceiptV1` · `OutcomeAdmissionReceiptV1` · line 416: Append-only exact admission receipt emitted before protected continuation.
- `decide_outcome_admission` · `decide_outcome_admission(request: OutcomeAdmissionRequestV1) -> OutcomeAdmissionDecisionV1` · line 435: Apply the signed-off first-consumer ordering to one typed request.
- `_portable_repo_path` · `_portable_repo_path(value: str) -> str | None` · line 496: Return one canonical POSIX repository path or None for unsafe syntax.
- `is_first_consumer_bootstrap_path` · `is_first_consumer_bootstrap_path(path: str, *, plan_number: int) -> bool` · line 508: Return whether one exact path belongs to the fixed source bootstrap set.
- `_bootstrap_path_plan` · `_bootstrap_path_plan(path: str) -> int | None` · line 523: Return the Plan number carried by one exact bootstrap path.
- `infer_first_consumer_bootstrap_plan` · `infer_first_consumer_bootstrap_plan(write_paths: tuple[str, ...]) -> int | None` · line 536: Infer one unique Plan only when the complete claim is bootstrap-safe.
- `evaluate_claim_bootstrap_admission` · `evaluate_claim_bootstrap_admission(claim: coordination_claims.ClaimRecord, *, target_path: str, ordinary_allowed: bool = True) -> OutcomeAdmissionResultV1 | None` · line 550: Return bootstrap admission only for an exact target in one safe claim.
- `has_sanctioned_maintenance_claim_identity` · `has_sanctioned_maintenance_claim_identity(claim: coordination_claims.ClaimRecord) -> bool` · line 580: Return whether claim-side fields retain canonical maintenance identity.
- `has_sanctioned_delegated_maintenance_claim_identity` · `has_sanctioned_delegated_maintenance_claim_identity(claim: coordination_claims.ClaimRecord) -> bool` · line 623: Return whether a child claim retains the exact delegated identity.
- `is_sanctioned_maintenance_claim_payload` · `is_sanctioned_maintenance_claim_payload(claim: coordination_claims.ClaimRecord, payload: object, *, tracker_path: Path | None = None) -> bool` · line 680: Classify typed maintenance provenance from one already-read tracker payload.
- `is_sanctioned_delegated_maintenance_claim_payload` · `is_sanctioned_delegated_maintenance_claim_payload(claim: coordination_claims.ClaimRecord, payload: object, *, tracker_path: Path | None = None) -> bool` · line 739: Classify a delegated child from one already-read tracker payload.
- `is_sanctioned_maintenance_claim` · `is_sanctioned_maintenance_claim(claim: coordination_claims.ClaimRecord) -> bool` · line 782: Read and classify one claim's linked tracker without a caller-held lock.
- `is_sanctioned_delegated_maintenance_claim` · `is_sanctioned_delegated_maintenance_claim(claim: coordination_claims.ClaimRecord) -> bool` · line 800: Read and classify one exact delegated child claim fail-closed.
- `evaluate_first_consumer_bootstrap` · `evaluate_first_consumer_bootstrap(bootstrap: OutcomeAdmissionBootstrapV1) -> OutcomeAdmissionBootstrapResultV1` · line 819: Classify and decide one bounded source-repository allocation bootstrap.
- `bootstrap_admission_result` · `bootstrap_admission_result(bootstrap: OutcomeAdmissionBootstrapV1) -> OutcomeAdmissionResultV1` · line 847: Return the canonical receipt-ready result for one bootstrap request.
- `_selection_error_reason` · `_selection_error_reason(code: str) -> str` · line 861: Map exact selection-owner failures to stable admission denial reasons.
- `_target_is_in_selected_scope` · `_target_is_in_selected_scope(target_path: str, allowed_scope: list[str]) -> bool` · line 891: Require a pre-write target to remain inside the selected outcome contract.
- `_continuation_state` · `_continuation_state(resolved: ResolvedOutcomeSelectionV1) -> tuple[ContinuationState, str]` · line 903: Translate the exact current continuation owner result into policy state.
- `evaluate_selected_outcome_admission` · `evaluate_selected_outcome_admission(*, agent: str, project: str, scope: str, session_id: str, repo_root: str, worktree_path: str, branch: str, claim_source_file: str, boundary: OperationBoundary, ordinary_allowed: bool, renewal: bool, target_path: str | None = None) -> OutcomeAdmissionResultV1` · line 927: Derive and decide exact selected admission without trusting state labels.
- `evaluate_selected_claim_admission` · `evaluate_selected_claim_admission(claim: coordination_claims.ClaimRecord, *, boundary: OperationBoundary, ordinary_allowed: bool = True, renewal: bool, target_path: str | None = None) -> OutcomeAdmissionResultV1` · line 1048: Evaluate one normalized exact claim through selected admission.
- `_selection_pending_failure` · `_selection_pending_failure(code: str, message: str) -> SelectionPendingActivationResultV1` · line 1095: Return one fail-closed staged-activation result.
- `evaluate_selection_pending_session_activation` · `evaluate_selection_pending_session_activation(claim: coordination_claims.ClaimRecord) -> SelectionPendingActivationResultV1` · line 1106: Validate one exact pre-tracker v4/v5/v6 reservation without selecting an outcome.
- `selection_pending_activation_receipt_path` · `selection_pending_activation_receipt_path(outcome_receipt_path: Path) -> Path` · line 1283: Route staged activation away from the shared admission-v1 stream.
- `build_selection_pending_activation_receipt` · `build_selection_pending_activation_receipt(result: SelectionPendingActivationResultV1, *, observed_at: datetime | None = None, receipt_id: str | None = None) -> SelectionPendingActivationReceiptV1` · line 1293: Build one separately framed staged-activation receipt.
- `append_selection_pending_activation_receipt` · `append_selection_pending_activation_receipt(receipt: SelectionPendingActivationReceiptV1, *, receipt_path: Path) -> None` · line 1309: Append one staged-activation receipt under its own sibling lock.
- `record_selection_pending_activation` · `record_selection_pending_activation(result: SelectionPendingActivationResultV1, *, outcome_receipt_path: Path = DEFAULT_OUTCOME_ADMISSION_RECEIPT_PATH) -> SelectionPendingActivationReceiptV1` · line 1334: Record staged activation without contaminating admission-v1 framing.
- `load_selection_pending_activation_receipts` · `load_selection_pending_activation_receipts(path: Path) -> list[SelectionPendingActivationReceiptV1]` · line 1349: Strictly load the separately versioned staged-activation stream.
- `build_outcome_admission_receipt` · `build_outcome_admission_receipt(result: OutcomeAdmissionResultV1, *, observed_at: datetime | None = None, receipt_id: str | None = None) -> OutcomeAdmissionReceiptV1` · line 1365: Build one digest-bound receipt without writing it.
- `append_outcome_admission_receipt` · `append_outcome_admission_receipt(receipt: OutcomeAdmissionReceiptV1, *, receipt_path: Path = DEFAULT_OUTCOME_ADMISSION_RECEIPT_PATH) -> None` · line 1381: Append one canonical JSON receipt under a sibling file lock.
- `record_outcome_admission` · `record_outcome_admission(result: OutcomeAdmissionResultV1, *, receipt_path: Path = DEFAULT_OUTCOME_ADMISSION_RECEIPT_PATH) -> OutcomeAdmissionReceiptV1` · line 1406: Build and append one admission receipt before protected continuation.
- `load_outcome_admission_receipts` · `load_outcome_admission_receipts(path: Path) -> list[OutcomeAdmissionReceiptV1]` · line 1418: Strictly load an append-only admission receipt stream.

_Coverage findings: python-docstring-missing._

### [`enforced_planning/outcome_completion.py`](../enforced_planning/outcome_completion.py)

Persist and enforce criterion-bound completion for one selected outcome.

**Symbols**

- `OutcomeCompletionError` · `OutcomeCompletionError` · line 40: Fail-loud completion error with one stable machine-readable code.
- `OutcomeCompletionTransitionV1` · `OutcomeCompletionTransitionV1` · line 55: One accepted completion bound to exact selected and evidence bytes.
- `OutcomeCompletionStopDecisionV1` · `OutcomeCompletionStopDecisionV1` · line 126: Native Stop decision for an explicitly activated consumer.
- `load_outcome_completion_mode` · `load_outcome_completion_mode(repo_root: Path) -> OutcomeCompletionMode` · line 145: Load the isolated first-consumer mode; absence remains compatible.
- `_validate_completed_portfolio_scenario` · `_validate_completed_portfolio_scenario(binding: outcome_selection.OutcomeSelectionBindingV1, *, claim: coordination_claims.ClaimRecord) -> OutcomeContinuationScenarioV1` · line 211: Reopen a classed scenario after its exact allocation completed.
- `record_selected_outcome_completion_for_session` · `record_selected_outcome_completion_for_session(*, agent: str, project: str, scope: str, projection_path: Path, proposal_path: Path, session_id: str | None = None, claims_dir: Path | None = None) -> OutcomeCompletionResultV1` · line 317: Validate and append one exact accepted completion to the session tracker.
- `evaluate_stop_for_session` · `evaluate_stop_for_session(*, repo_root: Path, agent: str, project: str, session_id: str, active_claims: tuple[coordination_claims.ClaimRecord, ...]) -> OutcomeCompletionStopDecisionV1` · line 488: Allow Stop only after the activated repo's exact outcome is complete.

_Coverage findings: python-docstring-missing._

### [`enforced_planning/outcome_continuation.py`](../enforced_planning/outcome_continuation.py)

Evaluate progress-bound coding-agent continuation without cost gating.

**Symbols**

- `ContinuationError` · `ContinuationError` · line 94: Fail-loud continuation contract or lineage error with a stable code.
- `ContinuationError.to_dict` · `to_dict(self) -> dict[str, str]` · line 101: Return a portable JSON error payload.
- `StrictModel` · `StrictModel` · line 107: Strict base for durable Plan 114 contracts.
- `_canonical_compatibility_payload` · `_canonical_compatibility_payload(value: Any) -> Any` · line 139: Remove inactive extension defaults from pre-extension durable identities.
- `canonical_sha256` · `canonical_sha256(value: BaseModel | dict[str, Any]) -> str` · line 197: Hash a model or JSON-compatible mapping with stable serialization.
- `CanonicalJourneyV1` · `CanonicalJourneyV1` · line 206: Stable user-visible journey against which progress is observed.
- `OutcomeCriterionV1` · `OutcomeCriterionV1` · line 216: One non-substitutable condition of the user-visible outcome.
- `OutcomeContractV1` · `OutcomeContractV1` · line 228: Immutable identity, scope, and canonical journey for one outcome lineage.
- `EvidenceBindingV1` · `EvidenceBindingV1` · line 289: Exact source, configuration, route, command, and observation binding.
- `OutcomeProgressReceiptV1` · `OutcomeProgressReceiptV1` · line 312: One independently bound progress or non-outcome observation.
- `OutcomeLeaseV1` · `OutcomeLeaseV1` · line 377: Replay-safe continuation state for one exact outcome contract digest.
- `ReviewReadinessDecisionV1` · `ReviewReadinessDecisionV1` · line 434: Deterministic review gate for one exact candidate artifact.
- `ExecutionItemV1` · `ExecutionItemV1` · line 444: One stable client-neutral execution item projected into native UIs.
- `AppliedExecutionTransitionV1` · `AppliedExecutionTransitionV1` · line 484: Retained idempotency identity for one accepted projection transition.
- `ExecutionProjectionV1` · `ExecutionProjectionV1` · line 496: Canonical execution state; native task lists are projections of this record.
- `ExecutionItemUpdateV1` · `ExecutionItemUpdateV1` · line 541: A bounded native or canonical intent for one existing execution item.
- `ExecutionProjectionTransitionV1` · `ExecutionProjectionTransitionV1` · line 556: Revision-bound transition intent independent of any client tool schema.
- `ExecutionProjectionTransitionResultV1` · `ExecutionProjectionTransitionResultV1` · line 581: Accepted, replayed projection transition and its current canonical state.
- `NativeProjectionObservationV1` · `NativeProjectionObservationV1` · line 597: A typed native observation that never mutates canonical execution state.
- `GoalCompletionProposalV1` · `GoalCompletionProposalV1` · line 632: The only terminal success intent for a criterion-bound outcome.
- `GoalCompletionDecisionV1` · `GoalCompletionDecisionV1` · line 651: Deterministic completion decision and resulting canonical lease.
- `RecoveryLeaseV1` · `RecoveryLeaseV1` · line 676: One bounded recovery action bound to the exact current lease.
- `RestartDeltaV1` · `RestartDeltaV1` · line 701: Exact causal difference required to restart a stalled or parked lineage.
- `AdmissionRequestV1` · `AdmissionRequestV1` · line 756: One requested supported operation plus decision-inert operator context.
- `LeaseTransitionV1` · `LeaseTransitionV1` · line 781: Result of applying or replaying one receipt.
- `ContinuationDecisionV1` · `ContinuationDecisionV1` · line 797: Deterministic allow/deny result for one supported operation.
- `OutcomeContinuationScenarioV1` · `OutcomeContinuationScenarioV1` · line 811: Complete deterministic input for the operator-facing evaluator.
- `OutcomeContinuationResultV1` · `OutcomeContinuationResultV1` · line 828: Lease and admission result emitted by the public JSON CLI.
- `issue_initial_lease` · `issue_initial_lease(contract: OutcomeContractV1, *, lease_id: str | None = None) -> OutcomeLeaseV1` · line 842: Issue the deterministic initial active lease for an accepted contract.
- `transition_lease` · `transition_lease(contract: OutcomeContractV1, lease: OutcomeLeaseV1, receipt: OutcomeProgressReceiptV1) -> LeaseTransitionV1` · line 865: Apply one lineage-bound receipt without allowing evidence replay.
- `evaluate_review_readiness` · `evaluate_review_readiness(contract: OutcomeContractV1, lease: OutcomeLeaseV1, *, artifact_sha256: str) -> ReviewReadinessDecisionV1` · line 1011: Refuse review until every frozen criterion passes on this exact artifact.
- `apply_execution_projection_transition` · `apply_execution_projection_transition(projection: ExecutionProjectionV1, transition: ExecutionProjectionTransitionV1) -> ExecutionProjectionTransitionResultV1` · line 1055: Apply one CAS-bound item update, retaining exact replay identity.
- `propose_goal_completion` · `propose_goal_completion(contract: OutcomeContractV1, lease: OutcomeLeaseV1, projection: ExecutionProjectionV1, proposal: GoalCompletionProposalV1) -> GoalCompletionDecisionV1` · line 1188: Close one outcome only from current criterion and execution evidence.
- `admit_operation` · `admit_operation(contract: OutcomeContractV1, lease: OutcomeLeaseV1, request: AdmissionRequestV1, *, recovery_lease: RecoveryLeaseV1 | None = None) -> ContinuationDecisionV1` · line 1349: Admit one supported operation from lease evidence, never approval/cost.
- `evaluate_scenario` · `evaluate_scenario(scenario: OutcomeContinuationScenarioV1) -> OutcomeContinuationResultV1` · line 1461: Apply an ordered scenario and return its final lease/admission result.
- `load_scenario` · `load_scenario(path: str) -> OutcomeContinuationScenarioV1` · line 1492: Load one strict scenario JSON file.

### [`enforced_planning/outcome_portfolio.py`](../enforced_planning/outcome_portfolio.py)

Allocate graph-bound outcome slots before durable outcome selection.

**Symbols**

- `OutcomePortfolioError` · `OutcomePortfolioError` · line 48: Fail-loud portfolio error with one stable machine-readable code.
- `StrictModel` · `StrictModel` · line 59: Strict immutable-compatible base for portfolio records.
- `ProjectGraphOutcomeAuthorityV1` · `ProjectGraphOutcomeAuthorityV1` · line 75: Exact reviewed repository identity loaded from one Git object.
- `PortfolioClaimBindingV1` · `PortfolioClaimBindingV1` · line 102: Stable exact-claim identity retained by one portfolio event.
- `OutcomePortfolioAllocationRequestV1` · `OutcomePortfolioAllocationRequestV1` · line 117: Explicit human/operator decision to consume one bounded WIP slot.
- `OutcomePortfolioDispositionRequestV1` · `OutcomePortfolioDispositionRequestV1` · line 148: Explicit append-only release request for one exact allocation.
- `OutcomePortfolioAllocationV1` · `OutcomePortfolioAllocationV1` · line 169: Immutable accepted allocation event.
- `OutcomePortfolioDispositionV1` · `OutcomePortfolioDispositionV1` · line 231: Immutable event that releases one allocation without deleting it.
- `OutcomePortfolioLedgerV1` · `OutcomePortfolioLedgerV1` · line 274: Atomically stored append-only portfolio event history.
- `OutcomePortfolioAllocationResultV1` · `OutcomePortfolioAllocationResultV1` · line 282: Operator-facing accepted or idempotently replayed allocation.
- `OutcomePortfolioDispositionResultV1` · `OutcomePortfolioDispositionResultV1` · line 293: Operator-facing accepted or idempotently replayed disposition.
- `ResolvedOutcomePortfolioAllocationV1` · `ResolvedOutcomePortfolioAllocationV1` · line 304: One exact active allocation accepted for classed selection.
- `portfolio_bucket` · `portfolio_bucket(portfolio_class: PortfolioClass, owner_class: str) -> str` · line 314: Return the approved WIP bucket for one class and reviewed owner.
- `resolve_project_graph_authority` · `resolve_project_graph_authority(*, project_graph_repo: Path, project_graph_revision: str, project_id: str) -> ProjectGraphOutcomeAuthorityV1` · line 345: Resolve one active reviewed repository from exact Git bytes.
- `_load_claim_records` · `_load_claim_records(claims_dir: Path) -> list[coordination_claims.ClaimRecord]` · line 463: Load authority-relevant claims while isolating explicit terminal debris.
- `load_outcome_portfolio_ledger` · `load_outcome_portfolio_ledger(path: Path) -> OutcomePortfolioLedgerV1` · line 704: Load and validate the complete event history, or return an empty ledger.
- `allocate_outcome_portfolio` · `allocate_outcome_portfolio(*, agent: str, project: str, scope: str, scenario_path: Path, request_path: Path, project_graph_repo: Path, project_graph_revision: str, session_id: str | None = None, claims_dir: Path | None = None, ledger_path: Path = DEFAULT_OUTCOME_PORTFOLIO_LEDGER_PATH) -> OutcomePortfolioAllocationResultV1` · line 839: Deliberately allocate one exact graph-backed portfolio slot.
- `dispose_outcome_portfolio_allocation` · `dispose_outcome_portfolio_allocation(*, agent: str, project: str, scope: str, request_path: Path, session_id: str | None = None, claims_dir: Path | None = None, ledger_path: Path = DEFAULT_OUTCOME_PORTFOLIO_LEDGER_PATH) -> OutcomePortfolioDispositionResultV1` · line 950: Append one exact disposition and release its bucket.
- `require_active_portfolio_allocation` · `require_active_portfolio_allocation(scenario: OutcomeContinuationScenarioV1, *, ledger_path: Path = DEFAULT_OUTCOME_PORTFOLIO_LEDGER_PATH) -> ResolvedOutcomePortfolioAllocationV1 | None` · line 1060: Require the unique exact active allocation for a classed scenario.

_Coverage findings: python-docstring-missing._

### [`enforced_planning/outcome_selection.py`](../enforced_planning/outcome_selection.py)

Bind one exact claimed session to one immutable outcome scenario.

**Symbols**

- `OutcomeSelectionError` · `OutcomeSelectionError` · line 48: Fail-loud selection error with one stable machine-readable code.
- `StrictModel` · `StrictModel` · line 59: Strict frozen-compatible base for session selection records.
- `OutcomeSelectionBindingV1` · `OutcomeSelectionBindingV1` · line 65: Create-once outcome choice bound to one stable exact claim identity.
- `OutcomeSelectionResultV1` · `OutcomeSelectionResultV1` · line 134: Operator-facing result for a selected or idempotently replayed choice.
- `OutcomeProgressTransitionV1` · `OutcomeProgressTransitionV1` · line 144: Append-only exact receipt and lease transition for selected state.
- `OutcomeProgressResultV1` · `OutcomeProgressResultV1` · line 195: Operator-facing accepted or idempotently replayed progress append.
- `ResolvedOutcomeSelectionV1` · `ResolvedOutcomeSelectionV1` · line 208: Validated selected state ready for one exact pre-write correlation.
- `OutcomeSessionTransferV1` · `OutcomeSessionTransferV1` · line 244: Append-only receipt for a sanctioned exact-runtime handoff.
- `OutcomeRestartTransitionV1` · `OutcomeRestartTransitionV1` · line 286: Append-only retained predecessor and successor state for one restart.
- `OutcomeRestartResultV1` · `OutcomeRestartResultV1` · line 337: Operator-facing accepted or idempotently replayed causal restart.
- `PreparedOutcomeSessionTransfer` · `PreparedOutcomeSessionTransfer` · line 350: Validated in-memory tracker mutation prepared before claim ownership changes.
- `ResolvedOutcomeProgressHead` · `ResolvedOutcomeProgressHead` · line 361: Validated in-memory current head for one selected binding lineage.
- `_load_claim_records` · `_load_claim_records(claims_dir: Path) -> list[coordination_claims.ClaimRecord]` · line 371: Load live-claim candidates without coupling them to terminal residue.
- `_validate_planned_outcome_baseline` · `_validate_planned_outcome_baseline(*, authority: str, claim: coordination_claims.ClaimRecord, scenario: OutcomeContinuationScenarioV1) -> None` · line 622: Revalidate a planned selection at its immutable outcome baseline.
- `_assert_binding_portfolio_allocation` · `_assert_binding_portfolio_allocation(binding: OutcomeSelectionBindingV1, *, scenario: OutcomeContinuationScenarioV1) -> None` · line 690: Reopen the exact active allocation retained by a classed binding.
- `_assert_binding_matches_claim` · `_assert_binding_matches_claim(binding: OutcomeSelectionBindingV1, *, claim: coordination_claims.ClaimRecord, tracker_path: Path) -> None` · line 799: Require every stored binding identity field to match its exact claim.
- `_validate_binding_scenario` · `_validate_binding_scenario(binding: OutcomeSelectionBindingV1, *, claim: coordination_claims.ClaimRecord) -> OutcomeContinuationScenarioV1` · line 841: Reopen and evaluate the immutable scenario behind one stored binding.
- `_binding_transfer_aliases` · `_binding_transfer_aliases(tracker: dict[str, Any], *, binding: OutcomeSelectionBindingV1) -> set[str]` · line 913: Resolve prior exact-runtime bindings sanctioned as the same selection.
- `_resolve_progress_head` · `_resolve_progress_head(tracker: dict[str, Any], *, binding: OutcomeSelectionBindingV1, scenario: OutcomeContinuationScenarioV1) -> ResolvedOutcomeProgressHead` · line 963: Replay accepted transitions for the current selection/transfer lineage.
- `_load_progress_receipt_for_claim` · `_load_progress_receipt_for_claim(receipt_path: Path, *, claim: coordination_claims.ClaimRecord) -> tuple[OutcomeProgressReceiptV1, str, str]` · line 1045: Load one strict immutable progress receipt from the exact worktree.
- `prepare_outcome_session_transfer` · `prepare_outcome_session_transfer(*, claim: coordination_claims.ClaimRecord, successor_session_id: str, transferred_at: datetime | None = None) -> PreparedOutcomeSessionTransfer | None` · line 1078: Validate selected state before a cross-session claim mutation begins.
- `build_prepared_outcome_session_transfer_payload` · `build_prepared_outcome_session_transfer_payload(prepared: PreparedOutcomeSessionTransfer, *, tracker_payload: dict[str, Any], predecessor_claim: coordination_claims.ClaimRecord, successor_claim: coordination_claims.ClaimRecord, current_phase: str, notes: str, updated_at: str) -> dict[str, Any]` · line 1150: Build one successor tracker payload without acquiring an external lock.
- `apply_prepared_outcome_session_transfer` · `apply_prepared_outcome_session_transfer(prepared: PreparedOutcomeSessionTransfer, *, predecessor_claim: coordination_claims.ClaimRecord, successor_claim: coordination_claims.ClaimRecord, current_phase: str, notes: str, updated_at: str) -> OutcomeSessionTransferV1` · line 1225: Atomically rebind one prepared selection and append its transfer receipt.
- `_binding_identity_sha256` · `_binding_identity_sha256(binding: OutcomeSelectionBindingV1) -> str` · line 1257: Hash the create-once choice while excluding its first-write timestamp.
- `select_outcome_for_session` · `select_outcome_for_session(*, agent: str, project: str, scope: str, execution_authority_ref: str, scenario_path: Path, session_id: str | None = None, claims_dir: Path | None = None, portfolio_ledger_path: Path = DEFAULT_OUTCOME_PORTFOLIO_LEDGER_PATH) -> OutcomeSelectionResultV1` · line 1265: Create or idempotently replay one exact-session outcome selection.
- `record_selected_outcome_progress_for_session` · `record_selected_outcome_progress_for_session(*, agent: str, project: str, scope: str, receipt_path: Path, session_id: str | None = None, claims_dir: Path | None = None) -> OutcomeProgressResultV1` · line 1372: Append one exact current-head receipt to selected outcome custody.
- `_load_restart_delta_for_claim` · `_load_restart_delta_for_claim(restart_delta_path: Path, *, claim: coordination_claims.ClaimRecord) -> tuple[RestartDeltaV1, str, str]` · line 1544: Load one strict restart delta from the exact claim worktree.
- `_failed_evidence_refs` · `_failed_evidence_refs(scenario: OutcomeContinuationScenarioV1) -> tuple[str, ...]` · line 1577: Return stable unique evidence refs retained from non-outcome receipts.
- `_assert_restart_contract` · `_assert_restart_contract(*, predecessor_binding: OutcomeSelectionBindingV1, predecessor_scenario: OutcomeContinuationScenarioV1, successor_binding: OutcomeSelectionBindingV1, successor_scenario: OutcomeContinuationScenarioV1, delta: RestartDeltaV1) -> tuple[OutcomeLeaseV1, tuple[str, ...]]` · line 1593: Validate exact same-outcome custody and retained predecessor failure state.
- `restart_selected_outcome_for_session` · `restart_selected_outcome_for_session(*, agent: str, project: str, scope: str, successor_scenario_path: Path, restart_delta_path: Path, session_id: str | None = None, claims_dir: Path | None = None, portfolio_ledger_path: Path = DEFAULT_OUTCOME_PORTFOLIO_LEDGER_PATH) -> OutcomeRestartResultV1` · line 1691: Replace stalled selected state only through one exact causal restart.
- `_resolve_selected_outcome` · `_resolve_selected_outcome(*, agent: str, project: str, scope: str, session_id: str, repo_root: str, worktree_path: str, branch: str, claim_source_file: str, target_path: str | None) -> ResolvedOutcomeSelectionV1` · line 1918: Resolve current selected state, with an optional exact target constraint.
- `resolve_selected_outcome_for_session` · `resolve_selected_outcome_for_session(*, agent: str, project: str, scope: str, session_id: str, repo_root: str, worktree_path: str, branch: str, claim_source_file: str) -> ResolvedOutcomeSelectionV1` · line 2061: Resolve and revalidate selected state for one exact live session claim.
- `resolve_selected_outcome_for_prewrite` · `resolve_selected_outcome_for_prewrite(*, agent: str, project: str, scope: str, session_id: str, repo_root: str, worktree_path: str, branch: str, claim_source_file: str, target_path: str) -> ResolvedOutcomeSelectionV1` · line 2087: Resolve selected state and require one exact ordinary pre-write target.

_Coverage findings: python-docstring-missing._

### [`enforced_planning/plan_close.py`](../enforced_planning/plan_close.py)

Plan-owned lane inventory and fail-closed atomic closeout.

**Symbols**

- `StrictContract` · `StrictContract` · line 17: Base contract that rejects unknown enforcement fields.
- `PlanCloseLaneV1` · `PlanCloseLaneV1` · line 23: One lane considered by a plan close operation.
- `PlanCloseResultV1` · `PlanCloseResultV1` · line 36: Atomic closeout result submitted before a plan status transition.
- `_split_qualified_plan_id` · `_split_qualified_plan_id(value: str) -> tuple[str, int]` · line 53: Parse the strict project#number identity used by plan lifecycle gates.
- `_claim_matches_plan` · `_claim_matches_plan(claim: coordination_claims.ClaimRecord, *, project: str, plan_number: int) -> bool` · line 61: Return whether one live claim belongs to the qualified plan.
- `_completed_lane` · `_completed_lane(claim: coordination_claims.ClaimRecord, *, project: str) -> PlanCloseLaneV1 | ValueError` · line 76: Validate durable terminal evidence on an already-completed claim.
- `_default_preflight` · `_default_preflight(claim: coordination_claims.ClaimRecord) -> dict[str, Any] | Exception` · line 113: Run existing merge/disposition checks without mutating lifecycle state.
- `_default_closer` · `_default_closer(claim: coordination_claims.ClaimRecord) -> dict[str, Any]` · line 141: Close one lane through the canonical session lifecycle.
- `_contains_path` · `_contains_path(root: Path, candidate: Path) -> bool` · line 156: Return whether ``candidate`` is equal to or beneath ``root``.
- `close_plan_lanes` · `close_plan_lanes(*, qualified_plan_id: str, submitted_revision: str, claims: list[coordination_claims.ClaimRecord] | None = None, preflight: Preflight = _default_preflight, closer: Closer = _default_closer, dry_run: bool = False, protected_path: Path | None = None) -> PlanCloseResultV1` · line 165: Preflight every live owned lane, then close all or mutate none.

### [`enforced_planning/plan_dependencies.py`](../enforced_planning/plan_dependencies.py)

Plan dependency contract validator (project-meta Plan #289).

**Symbols**

- `PlanDependencyError` · `PlanDependencyError` · line 111: One contract violation, addressed by file and (when known) plan id.
- `PlanFile` · `PlanFile` · line 123: One plan document and the project that owns it.
- `ParsedPlan` · `ParsedPlan` · line 136: Plan fields the dependency contract needs.
- `normalize_project_name` · `normalize_project_name(name: str) -> str` · line 151: Normalize a project id exactly as plan_graph._normalize_project_name.
- `normalize_qualified_id` · `normalize_qualified_id(value: str) -> str | None` · line 164: Return the canonical ``project#plan`` form, or None when malformed.
- `split_yaml_frontmatter` · `split_yaml_frontmatter(content: str) -> tuple[dict[str, Any] | None, str, str | None]` · line 178: Split a leading ``---`` YAML block; mirrors parse_plans._split_yaml_frontmatter.
- `is_plan_filename` · `is_plan_filename(name: str) -> bool` · line 200: Return whether a filename names a numbered plan.
- `_is_plan_relative_path` · `_is_plan_relative_path(relative_path: str) -> bool` · line 214: Filename rule plus: nothing under a companion subdirectory is a plan.
- `is_plan_path` · `is_plan_path(relative_path: str) -> bool` · line 221: Return whether a repo-relative path is a plan file under the five plan dirs.
- `iter_plan_paths` · `iter_plan_paths(repo_root: Path) -> list[Path]` · line 237: List plan files on disk, using the parse_plans depth rule per directory.
- `classify_status` · `classify_status(raw_status: str | None) -> tuple[str | None, bool]` · line 253: Return ``(status, is_open)``; a missing status is reported, never exempt.
- `extract_statuses` · `extract_statuses(frontmatter: Mapping[str, Any] | None, body: str) -> list[str]` · line 279: Return every plan-level status declaration, in precedence order.
- `derive_plan_id` · `derive_plan_id(project_id: str, relative_path: str) -> str | None` · line 320: Derive ``project#N`` from the filename number, as plan_graph._plan_identity does.
- `parse_plan` · `parse_plan(source: PlanFile) -> ParsedPlan | None` · line 329: Parse one plan; returns None for a non-plan file (unnumbered or untitled).
- `plan_identity` · `plan_identity(plan: ParsedPlan) -> str` · line 363: Known id: the declared plan_id when valid for this project, else the derived id.
- `PlanRef` · `PlanRef` · line 372: One plan file holding an id, for duplicate and ambiguity reporting.
- `build_known_ids` · `build_known_ids(plans: Iterable[ParsedPlan]) -> dict[str, list[PlanRef]]` · line 383: Index every resolvable id to the plan files holding it.
- `build_dependency_graph` · `build_dependency_graph(plans: Iterable[ParsedPlan]) -> dict[str, list[str]]` · line 400: Edges from each converted plan to its normalized dependencies.
- `check_cycles` · `check_cycles(graph: Mapping[str, Sequence[str]], *, through: Iterable[str] | None = None) -> list[str] | None` · line 413: Return the first cycle path (``[a, b, a]``) or None.
- `validate_plan_dependencies` · `validate_plan_dependencies(plan_files: Iterable[PlanFile], known_ids: Mapping[str, Sequence[PlanRef]], *, repo_project_id: str, graph: Mapping[str, Sequence[str]] | None = None) -> list[PlanDependencyError]` · line 518: Validate the Plan #289 contract for each open plan in ``plan_files``.
- `errors_to_json` · `errors_to_json(errors: Sequence[PlanDependencyError]) -> str` · line 561: Serialize errors for CLI output.

_Coverage findings: python-docstring-missing._

### [`enforced_planning/plan_readiness.py`](../enforced_planning/plan_readiness.py)

Portable, revision-bound plan start and explicit-resume decisions.

**Symbols**

- `StrictContract` · `StrictContract` · line 28: Base class for internal enforcement contracts.
- `PlanReadinessDecisionV1` · `PlanReadinessDecisionV1` · line 34: Canonical static decision returned by the ecosystem plan graph.
- `PlanLaneIdentityV1` · `PlanLaneIdentityV1` · line 47: Backward-compatible Plan 74 lane identity payload.
- `PlanStartGateResultV1` · `PlanStartGateResultV1` · line 63: Backward-compatible Plan 74 start-gate payload.
- `PlanLaneIdentityV2` · `PlanLaneIdentityV2` · line 73: Identity and distinct source/graph revisions for one planned lane.
- `PlanStartGateResultV2` · `PlanStartGateResultV2` · line 90: Result produced before mutation, including visible integrity evidence.
- `_plan_number` · `_plan_number(value: str | None) -> int | None` · line 101: Extract the numbered-plan identity from canonical and legacy spellings.
- `_live_matching_claim_scopes` · `_live_matching_claim_scopes(*, repository: str, qualified_plan_id: str) -> list[str]` · line 109: Return live or preserved canonical claim scopes for one numbered plan.
- `check_plan_start_readiness` · `check_plan_start_readiness(*, qualified_plan_id: str | None, execution_profile: ExecutionProfile, query_command: str | None, repository: str, lane_id: str, branch: str, worktree_path: str, claim_identity: str, session_identity: str, repo_root: Path | str | None = None, start_point: str = 'HEAD', plan_repo_root: Path | str | None = None, plan_start_point: str | None = None, parent_lane_id: str | None = None, allow_unplanned: bool = False, resume_requested: bool = False) -> PlanStartGateResultV2` · line 126: Validate static readiness and the non-owning precondition for a resume.

### [`enforced_planning/plan_validation.py`](../enforced_planning/plan_validation.py)

Validate implementation plans against the documentation relationship graph.

**Symbols**

- `_detect_repo_root` · `_detect_repo_root(script_path: Path) -> Path` · line 31: Resolve repo root for canonical, installed, and package layouts.
- `detect_repository_id` · `detect_repository_id(repo_root: Path) -> str` · line 40: Prefer the stable common-checkout directory over a linked-worktree name.
- `PlanningIntegrityError` · `PlanningIntegrityError` · line 119: Fail-loud planning-integrity configuration or source error.
- `_UniqueKeyLoader` · `_UniqueKeyLoader` · line 123: YAML loader that rejects duplicate mapping keys instead of last-write-wins.
- `StrictIntegrityModel` · `StrictIntegrityModel` · line 147: Strict base for the portable planning-integrity contract.
- `PlanningIntegrityConfigV1` · `PlanningIntegrityConfigV1` · line 153: Repository adoption configuration for Planning Integrity 1.0.0.
- `PlanningFrontierEntryV1` · `PlanningFrontierEntryV1` · line 161: One declared epistemic planning area and its executable resolution rule.
- `ReassessmentSummaryV1` · `ReassessmentSummaryV1` · line 178: Explicit triggers and authority boundaries for adaptive execution.
- `PlanIntegrityFindingV1` · `PlanIntegrityFindingV1` · line 188: One stable structural finding from the exact plan bytes.
- `PlanIntegrityResultV1` · `PlanIntegrityResultV1` · line 195: Versioned result consumed by admission and AES documentation projection.
- `normalize` · `normalize(path: str) -> str` · line 224: Normalize a repo-relative path for comparisons.
- `get_current_plan_number` · `get_current_plan_number(repo_root: Path = ROOT) -> int | None` · line 229: Infer the active plan number from the current git branch name.
- `find_plan_file` · `find_plan_file(plan_number: int, plans_dir: Path) -> Path | None` · line 248: Find one plan file by numeric prefix inside the plans directory.
- `validate_plan_integrity_at_revision` · `validate_plan_integrity_at_revision(*, repo_root: Path | str, repository_id: str, plan_number: int, start_point: str = 'HEAD') -> PlanIntegrityResultV1` · line 298: Validate plan/config bytes from the exact Git commit used to open a lane.
- `validate_plan_integrity_from_path` · `validate_plan_integrity_from_path(*, repo_root: Path, repository_id: str, plan_path: Path, plan_number: int | None) -> PlanIntegrityResultV1` · line 362: Validate exact working-tree bytes for explicit inspection/CLI output.
- `read_text` · `read_text(path: Path) -> str` · line 389: Read one UTF-8 text file from disk.
- `_validator_source_sha256` · `_validator_source_sha256() -> str` · line 394: Bind results to the exact executing validator bytes in every layout.
- `_load_unique_yaml_bytes` · `_load_unique_yaml_bytes(content: bytes, *, source: str) -> dict[str, Any]` · line 404: Decode one strict YAML mapping and reject duplicate keys.
- `parse_planning_integrity_config_bytes` · `parse_planning_integrity_config_bytes(content: bytes | None) -> tuple[PlanningIntegrityConfigV1, str, str | None]` · line 422: Return strict live settings, plans directory, and exact config digest.
- `_authored_section` · `_authored_section(section: str) -> str | None` · line 463: Remove instructions and accept only non-placeholder authored section bytes.
- `_bold_fields` · `_bold_fields(section: str) -> dict[str, str]` · line 475: Parse bold Markdown field declarations with multiline values.
- `_duplicate_bold_field_keys` · `_duplicate_bold_field_keys(section: str) -> list[str]` · line 490: Return normalized bold-field keys declared more than once.
- `_second_level_heading_pattern` · `_second_level_heading_pattern(heading: str) -> str` · line 511: Return one CommonMark-compatible ATX level-two heading pattern.
- `_ambiguous_governed_structure_findings` · `_ambiguous_governed_structure_findings(content: str) -> list[PlanIntegrityFindingV1]` · line 517: Reject duplicate governed headings or field declarations.
- `_parse_acceptance_criteria` · `_parse_acceptance_criteria(content: str) -> list[str]` · line 592: Return authored observable criteria from the canonical plan section.
- `evaluate_plan_integrity_bytes` · `evaluate_plan_integrity_bytes(*, plan_bytes: bytes | None, plan_path: str | None, plan_number: int | None, repository_id: str, config: PlanningIntegrityConfigV1, config_sha256: str | None, source_revision: str | None = None) -> PlanIntegrityResultV1` · line 717: Evaluate exact plan bytes without trusting a caller-supplied verdict.
- `extract_section` · `extract_section(content: str, heading: str) -> str` · line 843: Extract one second-level markdown section body by heading name.
- `split_lines` · `split_lines(section: str) -> list[str]` · line 856: Return non-empty stripped lines from one markdown section body.
- `looks_like_file_path` · `looks_like_file_path(value: str) -> bool` · line 867: Heuristic filter for inline repo-relative file path references.
- `extract_inline_paths` · `extract_inline_paths(line: str) -> list[str]` · line 879: Extract path-like tokens from one line of markdown text.
- `extract_paths` · `extract_paths(section: str) -> list[str]` · line 902: Extract and de-duplicate path references from one markdown section.
- `parse_files_affected` · `parse_files_affected(content: str) -> list[str]` · line 918: Parse the Files Affected section of a plan.
- `parse_references_reviewed` · `parse_references_reviewed(content: str) -> list[str]` · line 923: Parse the canonical reviewed-reference section or a legacy alias.
- `parse_uncertainty_register` · `parse_uncertainty_register(content: str) -> list[str]` · line 932: Parse bullet items under the Uncertainty Register section.
- `parse_contracts_used` · `parse_contracts_used(content: str) -> list[str]` · line 946: Parse the Contracts Used section from a plan.
- `parse_tools_used` · `parse_tools_used(content: str) -> list[str]` · line 961: Parse the Tools Used section from a plan.
- `parse_data_flow` · `parse_data_flow(content: str) -> list[dict[str, str]]` · line 976: Parse the Data Flow section from a plan.
- `parse_plan_status` · `parse_plan_status(content: str) -> tuple[str, str]` · line 1005: Extract the markdown title and bolded Status line.
- `parse_mentioned_adrs` · `parse_mentioned_adrs(content: str) -> set[int]` · line 1024: Return ADR numbers mentioned anywhere in the plan text.
- `_extract_metadata_value` · `_extract_metadata_value(content: str, field_name: str) -> str | None` · line 1035: Extract one bolded metadata field value from the plan header.
- `_parse_research_citations` · `_parse_research_citations(content: str) -> tuple[list[str], list[dict[str, str]]]` · line 1048: Parse and validate the optional research_citations metadata field.
- `_parse_landscape_contract` · `_parse_landscape_contract(content: str) -> tuple[str | None, list[str], list[dict[str, str]]]` · line 1113: Parse the report-only landscape disposition and its structural evidence.
- `_research_provenance_hint_present` · `_research_provenance_hint_present(content: str) -> bool` · line 1193: Heuristically detect plan text that cites prior-session provenance.
- `get_plan_file` · `get_plan_file(plan_number: int | None, plans_dir: Path, plan_file: str | None, *, repo_root: Path = ROOT) -> Path` · line 1205: Resolve the effective plan file from CLI inputs.
- `collect_plan_requirements` · `collect_plan_requirements(file_paths: list[str], relationships: dict[str, Any], *, repo_root: Path = ROOT, authority_config_path: Path | None = None) -> tuple[set[str], set[str], set[int], list[tuple[str, int, str]]]` · line 1234: Collect required docs and ADRs implied by affected files.
- `ValidationResult` · `ValidationResult` · line 1294: Structured output for one plan validation run.
- `ValidationResult.to_payload` · `to_payload(self) -> dict[str, Any]` · line 1320: Return a JSON-serializable summary payload.
- `validate_plan` · `validate_plan(plan_file: Path, plan_number: int | None, relationships: dict[str, Any], *, repo_root: Path = ROOT, authority_config_path: Path | None = None, plan_integrity: PlanIntegrityResultV1 | None = None) -> ValidationResult` · line 1354: Validate one plan file against required docs, ADRs, and section rules.
- `print_summary` · `print_summary(result: ValidationResult) -> None` · line 1545: Print a concise human-readable validation summary.
- `load_ack_file` · `load_ack_file(ack_path: Path) -> dict[str, str]` · line 1647: Load acknowledged plan-validation gaps from a YAML file.
- `_apply_acknowledgments` · `_apply_acknowledgments(result: ValidationResult, *, ack_file: str | None) -> set[str]` · line 1668: Downgrade acknowledged strict gaps to non-blocking notes.
- `_run_soft_notebook_check` · `_run_soft_notebook_check(repo_root: Path) -> None` · line 1697: Run the non-blocking notebook registry validation for one repo.
- `main` · `main(argv: Sequence[str] | None = None, *, repo_root: Path | None = None, plans_dir: Path | None = None) -> int` · line 1726: Run plan validation from the command line.

### [`enforced_planning/pr_review_signoff.py`](../enforced_planning/pr_review_signoff.py)

Exact-revision PR review orchestration and signoff receipts.

_Coverage findings: python-docstring-missing._

### [`enforced_planning/prewrite_claim_fast.py`](../enforced_planning/prewrite_claim_fast.py)

Dependency-light pre-write decisions over a canonical claim projection.

**Symbols**

- `FastPreWriteError` · `FastPreWriteError` · line 131: Raised when a hook request cannot be normalized safely.
- `registry_digest` · `registry_digest(claims_dir: Path) -> str` · line 135: Hash every YAML authority record deterministically without parsing it.
- `projection_path_for` · `projection_path_for(claims_dir: Path) -> Path` · line 149: Return the default derived projection path for one registry.
- `_shell_commands` · `_shell_commands(command: str) -> tuple[tuple[str, ...], ...] | None` · line 183: Return safely separated shell argv groups, or ``None`` when ambiguous.
- `_gh_command_is_read_only` · `_gh_command_is_read_only(argv: tuple[str, ...]) -> bool` · line 289: Admit only bounded GitHub CLI queries with no write-capable flags.
- `_date_command_is_read_only` · `_date_command_is_read_only(argv: tuple[str, ...]) -> bool` · line 340: Reject GNU date's clock-setting forms while allowing observation.
- `_sort_command_is_read_only` · `_sort_command_is_read_only(argv: tuple[str, ...]) -> bool` · line 352: Allow formatting-only sort calls while rejecting file-writing options.
- `classify_bash_command` · `classify_bash_command(command: str, *, claim_bootstrap_classifier: BashBootstrapClassifier | None = None) -> str` · line 376: Classify Bash without executing it.
- `_if_control_argv_is_read_only` · `_if_control_argv_is_read_only(argv: tuple[str, ...]) -> bool` · line 414: Admit a flat shell ``if`` only when every contained command is read-only.
- `_bash_declared_paths` · `_bash_declared_paths(command: str) -> tuple[str, ...]` · line 432: Extract explicit path operands that could redirect a shell mutation.
- `_bash_effective_argv` · `_bash_effective_argv(argv: tuple[str, ...]) -> tuple[str, ...]` · line 551: Return the command executed by the supported literal env cwd wrapper.
- `_paths_except_identifier_options` · `_paths_except_identifier_options(argv: tuple[str, ...], *, start: int, identifier_options: frozenset[str]) -> tuple[str, ...]` · line 559: Return path-shaped operands while skipping typed identifier values.
- `_github_declared_paths` · `_github_declared_paths(argv: tuple[str, ...]) -> tuple[str, ...] | None` · line 582: Treat GitHub ``owner/repo`` selectors as identifiers, not paths.
- `_concern_issue_declared_paths` · `_concern_issue_declared_paths(argv: tuple[str, ...]) -> tuple[str, ...] | None` · line 594: Classify concern-register arguments by their typed CLI contract.
- `_is_trusted_lifecycle_script` · `_is_trusted_lifecycle_script(value: str) -> bool` · line 655: Accept canonical relative paths and this runtime's absolute scripts.
- `_lifecycle_declared_paths` · `_lifecycle_declared_paths(argv: tuple[str, ...]) -> tuple[str, ...] | None` · line 670: Return only filesystem operands from a direct lifecycle invocation.
- `_make_lifecycle_declared_paths` · `_make_lifecycle_declared_paths(argv: tuple[str, ...]) -> tuple[str, ...] | None` · line 711: Return path operands for the sanctioned Make lifecycle targets.
- `_git_declared_paths` · `_git_declared_paths(argv: tuple[str, ...]) -> tuple[str, ...] | None` · line 752: Return actual path operands for bounded Git command shapes.
- `_bash_target_is_unprovable` · `_bash_target_is_unprovable(command: str) -> bool` · line 810: Reject expansions that can conceal a target path from the hook.
- `_bash_explicit_worktree` · `_bash_explicit_worktree(command: str) -> Path | None` · line 850: Return one literal runtime cwd attested by a supported Bash form.
- `_bash_is_explicitly_bound` · `_bash_is_explicitly_bound(command: str, worktree: Path) -> bool` · line 867: Require a literal runtime cwd when the native payload omits workdir.
- `_canonical_sync_command_targets_repo` · `_canonical_sync_command_targets_repo(command: str, *, worktree: Path, repo_root: Path) -> bool` · line 873: Recognize the exact installed canonical-checkout sync operation.
- `_session_status_command_is_read_only` · `_session_status_command_is_read_only(argv: tuple[str, ...]) -> bool` · line 920: Recognize only the canonical Python-backed session-status operation.
- `_argv_is_read_only` · `_argv_is_read_only(argv: tuple[str, ...]) -> bool` · line 970: Return whether one already-tokenized shell component is read-only.
- `_goal_authority_validator_is_read_only` · `_goal_authority_validator_is_read_only(argv: tuple[str, ...]) -> bool` · line 1037: Admit the exact shared goal validator with one read-only document operand.
- `_systemctl_command_is_read_only` · `_systemctl_command_is_read_only(argv: tuple[str, ...]) -> bool` · line 1056: Admit only bounded systemd queries; lifecycle verbs remain claim-bound.
- `adapt_native_payload` · `adapt_native_payload(payload: dict[str, Any], *, client: str, claim_bootstrap_classifier: BashBootstrapClassifier | None = None) -> dict[str, Any]` · line 1090: Normalize one supported native event without retaining write contents.
- `_valid_projected_claim` · `_valid_projected_claim(claim: object) -> bool` · line 1295: Validate the dependency-light view of PreWriteAuthorityClaimV1.
- `_is_append_only_path` · `_is_append_only_path(path: str) -> bool` · line 1439: Return whether a normalized target path lands only in an append-only store.
- `_claim_covers_targets` · `_claim_covers_targets(claim: dict[str, Any], targets: tuple[str, ...]) -> bool` · line 1452: Return whether one claim alone authorizes every normalized target.
- `evaluate_request_fast` · `evaluate_request_fast(request: dict[str, Any], *, mode: str, claims_dir: Path = DEFAULT_CLAIMS_DIR, projection_path: Path | None = None, receipt_path: Path = DEFAULT_RECEIPT_PATH, cache_hit: bool = True, projection_recovery_command: str | None = None) -> dict[str, Any]` · line 1513: Evaluate one normalized request and append its durable receipt.
- `evaluate_prewrite_fast` · `evaluate_prewrite_fast(payload: dict[str, Any], *, client: str, mode: str, claims_dir: Path = DEFAULT_CLAIMS_DIR, projection_path: Path | None = None, receipt_path: Path = DEFAULT_RECEIPT_PATH, claim_bootstrap_classifier: BashBootstrapClassifier | None = None, projection_recovery_command: str | None = None) -> dict[str, Any]` · line 1791: Normalize and evaluate one native hook payload.
- `native_mutation_worktree` · `native_mutation_worktree(payload: dict[str, Any], *, client: str) -> Path` · line 1819: Resolve the Git worktree named by one native mutation event.

### [`enforced_planning/prewrite_claim_projection.py`](../enforced_planning/prewrite_claim_projection.py)

Compile canonical YAML claims into a digest-bound pre-write projection.

**Symbols**

- `ProjectionBuildError` · `ProjectionBuildError` · line 19: Raised when canonical claim state cannot be projected safely.
- `StrictProjectionContract` · `StrictProjectionContract` · line 23: Reject unknown fields on the local projection contract.
- `PreWriteAuthorityClaimV1` · `PreWriteAuthorityClaimV1` · line 29: Normalized claim facts consumed by the dependency-light gate.
- `PreWriteAuthorityProjectionV1` · `PreWriteAuthorityProjectionV1` · line 49: Replaceable projection whose digest binds it to YAML authority.
- `_load_projection_claims` · `_load_projection_claims(claims_dir: Path) -> list[coordination_claims.ClaimRecord]` · line 71: Load valid unexpired claims and fail on unreadable registry records.
- `build_projection` · `build_projection(*, claims_dir: Path) -> PreWriteAuthorityProjectionV1` · line 100: Build a validated projection without mutating local state.
- `rebind_projection_digest` · `rebind_projection_digest(projection: PreWriteAuthorityProjectionV1, *, registry_digest_value: str) -> PreWriteAuthorityProjectionV1` · line 165: Re-validate the same projected claim set against a new registry digest.
- `write_projection_document` · `write_projection_document(*, claims_dir: Path, projection: PreWriteAuthorityProjectionV1, projection_path: Path | None = None) -> PreWriteAuthorityProjectionV1` · line 188: Atomically replace the derived projection file with one built projection.
- `write_projection` · `write_projection(*, claims_dir: Path, projection_path: Path | None = None) -> PreWriteAuthorityProjectionV1` · line 224: Atomically replace one derived projection after full validation.
- `projection_is_current` · `projection_is_current(*, claims_dir: Path, projection_path: Path | None = None) -> bool` · line 239: Return whether one readable validated projection matches YAML authority.

### [`enforced_planning/push_safety.py`](../enforced_planning/push_safety.py)

Pre-push coordination checks for governed worktree branches.

**Symbols**

- `PushCheckFinding` · `PushCheckFinding` · line 22: One push-safety issue or warning with enough detail to act on it.
- `PushCheckFinding.to_dict` · `to_dict(self) -> dict[str, Any]` · line 29: Return a JSON-safe representation for CLI and tests.
- `_run_git` · `_run_git(repo_root: Path, args: list[str]) -> subprocess.CompletedProcess[str]` · line 35: Run one git command inside the repo and capture the result.
- `_git_stdout` · `_git_stdout(repo_root: Path, args: list[str]) -> str` · line 47: Return stdout for one successful git command or fail loudly.
- `resolve_repo_root` · `resolve_repo_root(start_path: str | Path = '.') -> Path` · line 56: Resolve the canonical git toplevel for the current repo.
- `resolve_default_branch` · `resolve_default_branch(repo_root: Path) -> str | None` · line 63: Resolve the repo's default branch from local refs and origin/HEAD.
- `current_branch` · `current_branch(repo_root: Path) -> str` · line 80: Return the current symbolic branch name or fail on detached HEAD.
- `current_upstream` · `current_upstream(repo_root: Path) -> str | None` · line 92: Return the configured upstream for HEAD when one exists.
- `ahead_behind` · `ahead_behind(repo_root: Path, upstream_ref: str) -> tuple[int, int]` · line 102: Return ahead/behind counts for HEAD relative to its upstream.
- `changed_paths_since_default` · `changed_paths_since_default(repo_root: Path, default_branch: str) -> list[str]` · line 110: Return repo-relative paths changed on this branch against default.
- `_working_tree_dirty` · `_working_tree_dirty(repo_root: Path) -> bool` · line 123: Return whether tracked content could make the published delta ambiguous.
- `_branch_claims` · `_branch_claims(project: str, branch: str) -> list[coordination_claims.ClaimRecord]` · line 132: Return live claims attached to one project branch.
- `_healthy_branch_claims` · `_healthy_branch_claims(claims: list[coordination_claims.ClaimRecord]) -> list[coordination_claims.ClaimRecord]` · line 142: Return branch claims that still confer live push ownership.
- `_extract_json_block` · `_extract_json_block(raw_text: str) -> str` · line 158: Strip CLI noise before the first JSON token so parsing stays deterministic.
- `load_active_decisions` · `load_active_decisions(project: str, *, limit: int = 5) -> list[dict[str, Any]]` · line 168: Read active architectural decisions from agent_memory as raw JSON.
- `_claim_overlap_for_paths` · `_claim_overlap_for_paths(changed_paths: list[str], claim: coordination_claims.ClaimRecord) -> list[str]` · line 197: Return normalized changed-path overlaps against one active claim.
- `_predicts_clean_merge` · `_predicts_clean_merge(repo_root: Path, ref_a: str, ref_b: str) -> bool | None` · line 223: Predict whether the eventual integration of ref_a and ref_b would conflict.
- `_is_overbroad_undeclared_claim` · `_is_overbroad_undeclared_claim(claim: 'coordination_claims.ClaimRecord') -> bool` · line 247: True when a claim holds the whole repository without deliberately reserving it.
- `_is_same_session_default_integration` · `_is_same_session_default_integration(repo_root: Path, *, canonical_repo_root: Path, resolved_branch: str, default_branch: str, changed_paths: list[str], claim: coordination_claims.ClaimRecord) -> bool` · line 262: Return whether HEAD safely contains one current-session source lane.
- `evaluate_push_safety` · `evaluate_push_safety(repo_root: str | Path = '.', *, project: str | None = None, branch: str | None = None, include_active_decisions: bool = False, fail_on_active_decisions: bool = False) -> dict[str, Any]` · line 304: Evaluate whether the current branch is safe to push as-is.

### [`enforced_planning/relationship_context.py`](../enforced_planning/relationship_context.py)

Compile source-local summaries for every Git-tracked repository artifact.

**Symbols**

- `RelationshipContextError` · `RelationshipContextError` · line 72: Report an inventory failure that prevents truthful repository coverage.
- `Diagnostic` · `Diagnostic` · line 77: Describe one stable, actionable source-summary coverage finding.
- `SymbolRecord` · `SymbolRecord` · line 87: Represent one statically discovered Python symbol and its real docstring.
- `ArtifactRecord` · `ArtifactRecord` · line 99: Represent one tracked artifact without duplicating source-local meaning.
- `InventoryReport` · `InventoryReport` · line 113: Provide deterministic aggregate coverage over all tracked artifacts.
- `InventoryReport.to_dict` · `to_dict(self) -> dict[str, object]` · line 122: Return a JSON-compatible representation with stable field names.
- `InventoryReport.to_json` · `to_json(self, *, pretty: bool = False) -> str` · line 127: Serialize deterministically without timestamps or absolute paths.
- `tracked_paths` · `tracked_paths(repo_root: Path) -> tuple[str, ...]` · line 140: Return every Git-tracked path, preserving unusual names via NUL output.
- `classify_format` · `classify_format(path: str) -> ArtifactFormat` · line 160: Classify artifact syntax independently from governance classification.
- `classify_artifact` · `classify_artifact(path: str) -> ArtifactClassification` · line 177: Classify maintenance ownership from conventional repository path segments.
- `_first_paragraph` · `_first_paragraph(text: str | None) -> str | None` · line 198: Collapse the first non-empty source paragraph into compact context.
- `_annotation` · `_annotation(node: ast.expr | None) -> str | None` · line 209: Render one AST annotation for descriptive signature context.
- `_render_signature` · `_render_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str` · line 215: Render a compact, non-executable signature from function AST fields.
- `_python_symbols` · `_python_symbols(path: str, tree: ast.Module) -> tuple[SymbolRecord, ...]` · line 260: Extract module, class, and callable records in source order.
- `_python_record` · `_python_record(repo_root: Path, path: str, classification: ArtifactClassification) -> ArtifactRecord` · line 321: Build a Python artifact record with explicit parse and docstring diagnostics.
- `_markdown_sections` · `_markdown_sections(text: str) -> tuple[str | None, list[tuple[str, str, int]]]` · line 363: Return the H1 title and level-2 sections with source line provenance.
- `_split_front_matter` · `_split_front_matter(text: str) -> tuple[str | None, str]` · line 412: Return the document's own ``description`` front-matter value and the body after the block.
- `_markdown_first_paragraph` · `_markdown_first_paragraph(text: str) -> str | None` · line 437: Find initial prose while skipping headings, comments, and metadata lines.
- `_markdown_record` · `_markdown_record(repo_root: Path, path: str, classification: ArtifactClassification) -> ArtifactRecord` · line 463: Build a Markdown record from actual title and semantic section prose.
- `_unavailable_record` · `_unavailable_record(path: str, artifact_format: ArtifactFormat, classification: ArtifactClassification, state: Literal['missing', 'symlink']) -> ArtifactRecord` · line 505: Represent a tracked artifact whose working-tree source is not readable.
- `inventory_repository` · `inventory_repository(repo_root: Path) -> InventoryReport` · line 531: Compile deterministic source-summary records for every tracked artifact.
- `main` · `main(argv: list[str] | None = None) -> int` · line 561: Run the read-only relationship-context inventory CLI.

### [`enforced_planning/repository_authority.py`](../enforced_planning/repository_authority.py)

Generic, fail-closed repository mutation-authority provider boundary.

**Symbols**

- `RepositoryAuthorityError` · `RepositoryAuthorityError` · line 16: The configured provider could not produce one trustworthy decision.
- `MaintenanceWorktreeAuthority` · `MaintenanceWorktreeAuthority` · line 34: An exact worktree-creation grant, never general repository-write authority.
- `_provider_response` · `_provider_response(request: dict[str, str], config_path: Path) -> dict[str, Any]` · line 97: Call the pinned adapter without falling back to broader authority.
- `resolve_repository_authority` · `resolve_repository_authority(*, repo_root: Path, repository_identity: str, remote_url: str, config_path: Path = DEFAULT_PROVIDER_CONFIG) -> RepositoryAuthority` · line 117: Resolve legacy v1 general authority; scoped grants cannot satisfy it.
- `_literal_branch` · `_literal_branch(value: object) -> bool` · line 157: Reject Git shorthands whose meaning depends on the caller's checkout.
- `resolve_maintenance_worktree_authority` · `resolve_maintenance_worktree_authority(*, repo_root: Path, repository_identity: str, remote_url: str, branch: str, config_path: Path = DEFAULT_PROVIDER_CONFIG) -> MaintenanceWorktreeAuthority` · line 168: Require a v2 grant bound to this operation, root, identity, and branch.

_Coverage findings: python-docstring-missing._

### [`enforced_planning/repository_status.py`](../enforced_planning/repository_status.py)

Read-only Git freshness status for current project authority.

**Symbols**

- `RepositoryStatus` · `RepositoryStatus` · line 21: One exact repository and default-branch freshness observation.
- `RepositoryStatus.to_dict` · `to_dict(self) -> dict[str, object]` · line 43: Return a stable JSON-safe status payload.
- `_run_git` · `_run_git(repo_root: Path, args: list[str], *, timeout_seconds: float | None = None) -> subprocess.CompletedProcess[str]` · line 49: Run one bounded Git query without raising on ordinary Git failures.
- `_safe_error` · `_safe_error(value: str) -> str` · line 67: Remove URI credentials from a bounded Git error before reporting it.
- `_unknown` · `_unknown(*, repo_root: Path, current_branch: str | None, default_branch: str | None, remote_name: str | None, fetch_attempted: bool, fetch_succeeded: bool, fetch_error: str, worktree_dirty: bool | None) -> RepositoryStatus` · line 74: Build one fail-closed freshness-unknown result.
- `_current_branch` · `_current_branch(repo_root: Path) -> str | None` · line 105: Return the checked-out branch, or ``None`` for detached HEAD.
- `_remote_name` · `_remote_name(repo_root: Path, default_branch: str | None) -> str | None` · line 112: Resolve authority remote from the default branch, then fall back to origin.
- `_default_branch` · `_default_branch(repo_root: Path, remote_name: str) -> str | None` · line 129: Resolve the remote default branch with a local main/master fallback.
- `_ahead_behind` · `_ahead_behind(repo_root: Path, left_ref: str, right_ref: str) -> tuple[int, int] | None` · line 147: Return left-only and right-only commit counts for two Git refs.
- `_drift_status` · `_drift_status(ahead_count: int, behind_count: int) -> str` · line 167: Classify one local ref's exact relation to a remote authority ref.
- `inspect_repository` · `inspect_repository(repo_root: Path, *, fetch_remote: bool = True, fetch_timeout_seconds: float = DEFAULT_FETCH_TIMEOUT_SECONDS) -> RepositoryStatus` · line 179: Inspect canonical default-branch freshness without mutating local work.

### [`enforced_planning/session_continuity.py`](../enforced_planning/session_continuity.py)

Classify session activity without turning silence into takeover authority.

**Symbols**

- `ContinuityClaim` · `ContinuityClaim` · line 19: Claim fields required by the observe-only continuity classifier.
- `ResumeOfferStatus` · `ResumeOfferStatus` · line 32: Mailbox status fields required before a successor may be launched.
- `CodexActivityV1` · `CodexActivityV1` · line 41: Last durable Codex task boundary observed in one exact transcript.
- `ContinuityAssessmentV1` · `ContinuityAssessmentV1` · line 59: Observe-only continuity result; transfer always needs a later handshake.
- `ResumeOfferReviewV1` · `ResumeOfferReviewV1` · line 91: Decision after projecting one exact owner resume offer and its receipts.
- `SuccessorCustodyOfferV1` · `SuccessorCustodyOfferV1` · line 107: Exact recoverable lane state offered to one future successor runtime.
- `SuccessorCustodyAcceptanceV1` · `SuccessorCustodyAcceptanceV1` · line 140: Successor-authored acceptance of every exact offered custody field.
- `CodexSuccessorLaunchV1` · `CodexSuccessorLaunchV1` · line 164: Exact disabled-by-default native launch request for one successor.
- `CodexSuccessorLaunchReceiptV1` · `CodexSuccessorLaunchReceiptV1` · line 186: Host acknowledgement that a successor unit started, not custody acceptance.
- `NativeCodexSuccessorLaunchJournalV1` · `NativeCodexSuccessorLaunchJournalV1` · line 205: Write-ahead state for one verified native successor launch.
- `NativeCodexResumeOfferV1` · `NativeCodexResumeOfferV1` · line 242: One exact, idempotently identifiable prompt for Codex's durable queue.
- `NativeCodexQueueReceiptV1` · `NativeCodexQueueReceiptV1` · line 256: Strictly parsed acceptance receipt from the installed Codex client.
- `NativeCodexConsumptionReceiptV1` · `NativeCodexConsumptionReceiptV1` · line 270: Transcript proof that the exact queued prompt became an owner user turn.
- `NativeCodexDeliveryJournalV1` · `NativeCodexDeliveryJournalV1` · line 289: Write-ahead state for one correlation-bound native queue attempt.
- `read_codex_activity` · `read_codex_activity(*, session_id: str, transcript_path: Path) -> CodexActivityV1` · line 339: Read the latest task boundary; malformed transcript records fail visibly.
- `read_native_codex_consumption` · `read_native_codex_consumption(*, owner_session_id: str, correlation_id: str, queued_submission_id: str, transcript_path: Path) -> NativeCodexConsumptionReceiptV1 | None` · line 428: Find the exact continuity marker only in a native owner user-message event.
- `assess_continuity` · `assess_continuity(*, claim: ContinuityClaim, activity: CodexActivityV1 | None, now: datetime | None = None, notify_after: timedelta = timedelta(minutes=15)) -> ContinuityAssessmentV1` · line 502: Classify custody while withholding transfer authority from passive signals.
- `native_resume_progress_fingerprint` · `native_resume_progress_fingerprint(*, progress_at: str | None, head_revision: str, next_action: str) -> str` · line 649: Bind retry accounting to durable outcome evidence, not liveness telemetry.
- `build_resume_offer_request` · `build_resume_offer_request(*, assessment: ContinuityAssessmentV1, sender_session_id: str, project: str, scope: str, next_action: str) -> coordination_messages.SendMessageRequest` · line 672: Build one idempotent owner-first resume offer from an idle assessment.
- `build_native_codex_resume_offer` · `build_native_codex_resume_offer(*, assessment: ContinuityAssessmentV1, project: str, scope: str, next_action: str, progress_fingerprint: str) -> NativeCodexResumeOfferV1` · line 711: Build one exact-thread prompt accepted by the native Codex queue CLI.
- `parse_native_codex_queue_receipt` · `parse_native_codex_queue_receipt(*, offer: NativeCodexResumeOfferV1, stdout: str) -> NativeCodexQueueReceiptV1` · line 755: Accept only Codex's exact queue acknowledgement for the requested thread.
- `assess_resume_offer` · `assess_resume_offer(*, assessment: ContinuityAssessmentV1, status: ResumeOfferStatus, now: datetime | None = None, successor_after: timedelta = timedelta(minutes=30)) -> ResumeOfferReviewV1` · line 779: Allow successor launch only after the exact owner offer reached its runtime.
- `build_successor_custody_offer` · `build_successor_custody_offer(*, review: ResumeOfferReviewV1, project: str, scope: str, branch: str, worktree_path: str, claim_epoch_sha256: str, head_revision: str, next_action: str, created_at: datetime | None = None) -> SuccessorCustodyOfferV1` · line 849: Freeze the exact lane state a later successor may explicitly accept.
- `build_native_successor_custody_offer` · `build_native_successor_custody_offer(*, delivery: NativeCodexDeliveryJournalV1, consumption: NativeCodexConsumptionReceiptV1, consumed_attempt_count: int, project: str, scope: str, branch: str, worktree_path: str, claim_epoch_sha256: str, head_revision: str, next_action: str, created_at: datetime | None = None) -> SuccessorCustodyOfferV1` · line 886: Freeze custody after bounded, consumed native retries without launching it.
- `successor_custody_offer_sha256` · `successor_custody_offer_sha256(offer: SuccessorCustodyOfferV1) -> str` · line 935: Return the canonical digest bound into a successor acceptance receipt.
- `build_codex_successor_launch` · `build_codex_successor_launch(*, offer: SuccessorCustodyOfferV1, offer_path: str, resume_script: str, predecessor_process_pid: int, predecessor_process_start_ticks: int, codex: str = 'codex', systemd_run: str = 'systemd-run') -> CodexSuccessorLaunchV1` · line 946: Build one transient fork whose first authorized mutation is acceptance.
- `accept_successor_custody_offer` · `accept_successor_custody_offer(*, offer: SuccessorCustodyOfferV1, successor_session_id: str, project: str, scope: str, branch: str, worktree_path: str, claim_epoch_sha256: str, head_revision: str, next_action: str, accepted_at: datetime | None = None) -> SuccessorCustodyAcceptanceV1` · line 1034: Accept only an exact offer; this receipt does not itself mutate custody.
- `validate_successor_custody_acceptance` · `validate_successor_custody_acceptance(*, offer: SuccessorCustodyOfferV1, acceptance: SuccessorCustodyAcceptanceV1) -> SuccessorCustodyAcceptanceV1` · line 1076: Verify a successor receipt is bound to the exact immutable offer.

_Coverage findings: python-docstring-missing._

### [`enforced_planning/session_contracts.py`](../enforced_planning/session_contracts.py)

Session bootstrap contract and tracker helpers.

**Symbols**

- `_require_text` · `_require_text(value: str, *, field_name: str) -> str` · line 64: Return one stripped text field or raise a clear contract error.
- `normalize_plan_ref` · `normalize_plan_ref(plan_ref: str | None, *, allow_unplanned: bool = False) -> str` · line 73: Return a normalized plan marker or fail loud if none was declared.
- `_clean_string_list` · `_clean_string_list(items: list[str] | None) -> list[str]` · line 85: Return a stable deduplicated string list for tracker serialization.
- `derive_session_name` · `derive_session_name(broader_goal: str) -> str` · line 99: Derive the canonical session name from the broader goal text.
- `validate_session_name` · `validate_session_name(*, session_name: str, broader_goal: str) -> str` · line 108: Require the session name to match the broader-goal-derived canonical slug.
- `SessionContract` · `SessionContract` · line 121: Compact session contract fields that belong on the canonical claim.
- `SessionContract.build` · `build(cls, *, agent: str, project: str, scope: str, intent: str, repo_root: str, worktree_path: str, branch: str, session_id: str, broader_goal: str, plan_ref: str | None = None, session_name: str | None = None, tracker_path: str | None = None, start_revision: str | None = None, plan_repo_root: str | None = None, plan_revision: str | None = None, plan_sha256: str | None = None, allow_unplanned: bool = False) -> SessionContract` · line 142: Build a validated session contract from bootstrap inputs.
- `SessionContract.with_tracker_path` · `with_tracker_path(self, tracker_path: str) -> SessionContract` · line 206: Return the same contract with a concrete tracker path attached.
- `SessionContract.claim_fields` · `claim_fields(self) -> dict[str, str]` · line 211: Return only the claim-critical contract fields.
- `SessionTrackerRecord` · `SessionTrackerRecord` · line 238: Human-readable tracker artifact linked from one session contract.
- `SessionTrackerRecord.tracker_fields` · `tracker_fields(self) -> dict[str, Any]` · line 252: Return only the tracker-only execution fields.
- `SessionTrackerRecord.to_dict` · `to_dict(self) -> dict[str, Any]` · line 264: Return the nested contract/tracker representation for YAML output.
- `session_contract_schema` · `session_contract_schema() -> dict[str, list[str]]` · line 278: Return the formal split between claim and tracker fields.
- `build_session_tracker` · `build_session_tracker(*, contract: SessionContract, current_phase: str, intended_next_phases: list[str] | None = None, depends_on_repos: list[str] | None = None, requires_shared_infra_changes: bool = False, stop_conditions: list[str] | None = None, notes: str | None = None, now: datetime | None = None) -> SessionTrackerRecord` · line 287: Build the linked tracker artifact for one active session contract.
- `_bounded_tracker_filename` · `_bounded_tracker_filename(*, agent: str, project: str, safe_session_id: str, session_name: str) -> str` · line 332: Compose a tracker filename that survives its own atomic rewrite.
- `session_tracker_path` · `session_tracker_path(contract: SessionContract, *, tracker_dir: Path = DEFAULT_SESSION_TRACKERS_DIR) -> Path` · line 359: Return the canonical tracker path for one session contract.
- `find_session_tracker_path` · `find_session_tracker_path(*, agent: str, project: str, scope: str, session_id: str | None, preferred_path: str | None = None, tracker_dir: Path | None = None) -> Path | None` · line 436: Find one exact tracker when refreshed claim metadata lost its path.
- `write_session_tracker` · `write_session_tracker(record: SessionTrackerRecord, *, tracker_dir: Path = DEFAULT_SESSION_TRACKERS_DIR) -> Path` · line 479: Persist one tracker without erasing selected outcome custody history.
- `tracker_lock_path` · `tracker_lock_path(path: Path) -> Path` · line 557: Where the mutation lock for one tracker lives.
- `TrackerPathNotYAML` · `TrackerPathNotYAML` · line 593: A claim's tracker path is not a readable YAML mapping.
- `session_tracker_lock` · `session_tracker_lock(path: Path) -> Iterator[None]` · line 601: Serialize exact-session tracker mutations through one out-of-tree lock.
- `_atomic_write_session_tracker` · `_atomic_write_session_tracker(path: Path, payload: dict[str, Any]) -> None` · line 617: Replace one tracker without exposing partial YAML to another reader.
- `read_session_tracker` · `read_session_tracker(path: Path) -> dict[str, Any]` · line 643: Load one tracker artifact and fail loud if the structure is invalid.
- `mutate_session_tracker` · `mutate_session_tracker(path: Path, mutation: Callable[[dict[str, Any]], None], *, updated_at: str | None = None) -> dict[str, Any]` · line 674: Apply one locked tracker transformation and atomically persist it.
- `update_session_tracker` · `update_session_tracker(path: Path, *, current_phase: str | None = None, intended_next_phases: list[str] | None = None, depends_on_repos: list[str] | None = None, requires_shared_infra_changes: bool | None = None, stop_conditions: list[str] | None = None, notes: str | None = None, updated_at: str | None = None) -> dict[str, Any]` · line 694: Update one existing tracker artifact in place and return the payload.

### [`enforced_planning/session_lifecycle.py`](../enforced_planning/session_lifecycle.py)

Session lifecycle operations for sanctioned worktree flows.

**Symbols**

- `SessionTransferIncompleteError` · `SessionTransferIncompleteError` · line 52: A cross-file session transfer failed and exact rollback was incomplete.
- `OutcomeAdmissionDeniedError` · `OutcomeAdmissionDeniedError` · line 58: One recorded outcome denial raised before lifecycle mutation.
- `BlockerDispositionApplicationReceiptV1` · `BlockerDispositionApplicationReceiptV1` · line 70: Immutable evidence that one accepted disposition was safely consumed.
- `_shared_lock_fd_if_present` · `_shared_lock_fd_if_present(lock_path: Path) -> int | None` · line 93: Acquire an existing lock for observation without creating or chmodding it.
- `_release_shared_lock` · `_release_shared_lock(fd: int) -> None` · line 109: Release one observation lock acquired by `_shared_lock_fd_if_present`.
- `_file_observation_fingerprint` · `_file_observation_fingerprint(path: Path) -> tuple[int, int, str] | None` · line 118: Return stable identity, size, and digest for an observed file.
- `_claim_registry_observation_fingerprint` · `_claim_registry_observation_fingerprint(claims_dir: Path) -> tuple[tuple[str, int, int, str], ...]` · line 129: Fingerprint authoritative claim YAML without touching staging artifacts.
- `_read_session_tracker_for_status` · `_read_session_tracker_for_status(path: Path) -> dict[str, Any] | None` · line 143: Read one tracker under an existing shared lock or a verified stable snapshot.
- `_poll_mailbox` · `_poll_mailbox(*, agent: str, project: str, session_id: str) -> dict[str, Any]` · line 173: Inject canonical mailbox state into a shared lifecycle response.
- `_poll_mailbox_after_committed_transition` · `_poll_mailbox_after_committed_transition(*, agent: str, project: str, session_id: str) -> dict[str, Any]` · line 217: Expose post-commit poll failure without misreporting committed custody.
- `_load_worktree_lifecycle_policy` · `_load_worktree_lifecycle_policy(path: Path) -> tuple[str, frozenset[str], frozenset[str], frozenset[str]]` · line 245: Load and validate the configurable disposition vocabulary.
- `CloseoutPreflight` · `CloseoutPreflight` · line 296: Validated branch state that licenses one closeout mutation sequence.
- `CloseoutPreflight.to_dict` · `to_dict(self) -> dict[str, Any]` · line 310: Return a JSON-safe representation for CLI payloads and audit records.
- `_tracker_sha256` · `_tracker_sha256(path: Path) -> str` · line 316: Return the exact byte digest used to bind missing-worktree closeout.
- `_claim_sha256` · `_claim_sha256(path: Path) -> str` · line 322: Return the exact byte digest used to bind legacy-claim reconciliation.
- `_exact_tracker_candidates` · `_exact_tracker_candidates(claim: coordination_claims.ClaimRecord) -> list[Path]` · line 328: Return trackers matching every preserved claim identity field.
- `_session_ended_reconciliation_tracker` · `_session_ended_reconciliation_tracker(claim: coordination_claims.ClaimRecord) -> tuple[Path, dict[str, dict[str, str | None]]]` · line 358: Resolve a tracker while preserving evidence of stale mutable identity.
- `_validate_missing_worktree_reconciliation` · `_validate_missing_worktree_reconciliation(*, claim: coordination_claims.ClaimRecord, claim_file: Path, expected_tracker_sha256: str | None, expected_claim_sha256: str | None = None) -> dict[str, Any]` · line 435: Fail closed before reconciling one preserved lane with no worktree.
- `_validate_session_ended_closeout_reconciliation` · `_validate_session_ended_closeout_reconciliation(*, claim: coordination_claims.ClaimRecord, claim_file: Path, repo_root: Path, actor_session_id: str | None, expected_claim_sha256: str | None, expected_tracker_sha256: str | None, tracker_absent: bool = False) -> dict[str, Any]` · line 505: Authorize terminal closeout without transferring write custody.
- `_verify_session_ended_tracker_absent` · `_verify_session_ended_tracker_absent(claim: coordination_claims.ClaimRecord) -> dict[str, Any]` · line 638: Prove, not assume, that a session-ended claim has no tracker to bind (#2010).
- `_git_capture` · `_git_capture(cwd: Path, *args: str) -> str` · line 664: Run one Git command for lane-state capture; any failure is a capture failure.
- `_capture_session_ended_lane_state` · `_capture_session_ended_lane_state(*, claim: coordination_claims.ClaimRecord, worktree: Path, repo_root: Path, archive_dir: str | None) -> dict[str, Any]` · line 676: Capture an existing session-ended worktree before any lifecycle mutation (#2010).
- `_validate_canonical_root_reconciliation` · `_validate_canonical_root_reconciliation(*, claim: coordination_claims.ClaimRecord, claim_file: Path, repo_root: Path, expected_claim_sha256: str | None, expected_tracker_sha256: str | None) -> dict[str, Any]` · line 771: Bind ended owned custody to a retained root and digest-bound tracker.
- `_resolve_active_mailbox_for_closeout` · `_resolve_active_mailbox_for_closeout(*, claim: coordination_claims.ClaimRecord, mailbox_disposition: str | None, mailbox_note: str | None) -> dict[str, Any]` · line 875: Require an explicit durable disposition for active recipient messages.
- `_split_cli_values` · `_split_cli_values(values: list[str] | None) -> list[str]` · line 946: Normalize repeated or delimiter-packed CLI values into one clean list.
- `_claim_path` · `_claim_path(agent: str, project: str, scope: str) -> Path` · line 958: Return the canonical YAML path for one claim.
- `_load_claim_payload` · `_load_claim_payload(agent: str, project: str, scope: str) -> dict[str, Any] | None` · line 964: Load one claim payload if it exists.
- `_write_claim_payload` · `_write_claim_payload(path: Path, payload: dict[str, Any]) -> None` · line 976: Persist one normalized claim payload through the canonical atomic writer.
- `_write_claim_and_refresh_projection` · `_write_claim_and_refresh_projection(path: Path, payload: dict[str, Any], claims_dir: Path = coordination_claims.CLAIMS_DIR) -> tuple[Path, str]` · line 988: Write claim and atomically refresh projection in one operation.
- `_atomic_restore_bytes` · `_atomic_restore_bytes(path: Path, content: bytes) -> None` · line 1035: Atomically restore exact preflight bytes for a failed two-file transfer.
- `_renewed_lease_expiry` · `_renewed_lease_expiry(updated_at: str, current_expires_at: str | None) -> str` · line 1059: Return the lease expiry a resume attaching at ``updated_at`` should carry.
- `_apply_cross_agent_handoff_transaction` · `_apply_cross_agent_handoff_transaction(*, claim: coordination_claims.ClaimRecord, claim_file: Path, claim_bytes_before: bytes, successor_agent: str, successor_session_id: str, current_phase: str, note: str | None, updated_at: str, expected_fields: dict[str, Any], project: str, scope: str) -> dict[str, Any]` · line 1094: Transfer a quiesced claim's identity to a different native agent.
- `_apply_legacy_cross_session_resume_transaction` · `_apply_legacy_cross_session_resume_transaction(*, claim: coordination_claims.ClaimRecord, claim_file: Path, claim_bytes_before: bytes, tracker_path: Path, tracker_bytes_before: bytes, successor_session_id: str, current_phase: str, note: str | None, updated_at: str, expected_fields: dict[str, Any], transfer_preflight: outcome_selection.PreparedOutcomeSessionTransfer | None, project: str, scope: str, worktree_path: str, branch: str) -> tuple[dict[str, Any], outcome_selection.OutcomeSessionTransferV1 | None, dict[str, Any]]` · line 1189: Commit an unfenced non-Codex custody transfer with exact rollback.
- `_apply_codex_cross_session_resume_transaction` · `_apply_codex_cross_session_resume_transaction(*, claim: coordination_claims.ClaimRecord, claim_file: Path, claim_bytes_before: bytes, tracker_path: Path, tracker_bytes_before: bytes, successor_session_id: str, current_phase: str, note: str | None, updated_at: str, expected_fields: dict[str, Any], transfer_preflight: outcome_selection.PreparedOutcomeSessionTransfer | None, project: str, scope: str, worktree_path: str, branch: str, process_fence: dict[str, Any] | None, predecessor_process_pid: int | None, predecessor_process_start_ticks: int | None, takeover_reservation: dict[str, Any] | None) -> tuple[dict[str, Any], outcome_selection.OutcomeSessionTransferV1 | None, dict[str, Any]]` · line 1332: Commit custody through a reservation journal with the claim written last.
- `_validate_same_runtime_tracker_identity` · `_validate_same_runtime_tracker_identity(*, claim: coordination_claims.ClaimRecord, tracker_path: Path, tracker_payload: dict[str, Any]) -> None` · line 1597: Require exact claim and tracker custody before reattaching a lost path.
- `_reattach_same_runtime_tracker` · `_reattach_same_runtime_tracker(*, claim: coordination_claims.ClaimRecord, claim_file: Path, tracker_path: Path, current_phase: str, note: str | None, updated_at: str, expected_fields: dict[str, Any]) -> dict[str, Any]` · line 1636: Atomically restore a uniquely identified tracker path and resume its lane.
- `_persist_claim_session_transfer_receipt` · `_persist_claim_session_transfer_receipt(*, claim: coordination_claims.ClaimRecord, project: str, scope: str, worktree_path: str, branch: str, successor_session_id: str, transferred_at: str, prior_claim_bytes: bytes, successor_claim_bytes: bytes, process_fence: dict[str, Any] | None, predecessor_process_pid: int | None, predecessor_process_start_ticks: int | None, process_fence_transfer_epoch_sha256: str | None) -> dict[str, Any]` · line 1726: Persist one immutable, digest-bound receipt for cross-session claim custody.
- `_rollback_outcome_session_transfer` · `_rollback_outcome_session_transfer(*, claim: coordination_claims.ClaimRecord, claim_file: Path, successor_session_id: str, claim_bytes: bytes, tracker_path: Path, tracker_bytes: bytes) -> None` · line 1858: Restore the exact claim and tracker bytes after a failed transfer.
- `_apply_claim_payload_updates` · `_apply_claim_payload_updates(*, claim: coordination_claims.ClaimRecord, claim_file: Path, updates: dict[str, Any], operation: claim_mutation_receipts.MutationOperation = 'session_upsert', expected_fields: dict[str, Any] | None = None) -> dict[str, Any]` · line 1895: Apply one lifecycle mutation and refresh its projection under one lock.
- `_upsert_session_claim` · `_upsert_session_claim(*, agent: str, project: str, scope: str, intent: str, plan_ref: str | None, repo_root: str, worktree_path: str, branch: str, session_id: str, broader_goal: str, session_name: str, tracker_path: str, claim_type: str | None = None, write_paths: list[str] | None = None, read_paths: list[str] | None = None, parent_scope: str | None = None, work_graph_path: str | None = None, work_unit_id: str | None = None, start_revision: str | None = None, plan_repo_root: str | None = None, plan_start_point: str | None = None, ttl_hours: float = coordination_claims.DEFAULT_TTL_HOURS, allow_parallel: bool = False, broad_scope_mode: str | None = None, broad_scope_reason: str | None = None, target_worktree_path: str | None = None, new_files: list[str] | None = None, staged_reservation: coordination_claims.ClaimRecord | None = None, maintenance_snapshot: _MaintenanceRefreshSnapshot | None = None, registry_lock_held: bool = False, verified_goal_default_revision: str | None = None, verified_maintenance_default_revision: str | None = None) -> str` · line 1941: Create or update the compact claim-side session contract metadata.
- `_iter_matching_live_claims` · `_iter_matching_live_claims(*, agent: str | None = None, project: str | None = None, scope: str | None = None, branch: str | None = None) -> list[coordination_claims.ClaimRecord]` · line 2261: Return live claims filtered to one bounded session scope.
- `_single_matching_live_claim` · `_single_matching_live_claim(*, agent: str, project: str, scope: str) -> coordination_claims.ClaimRecord` · line 2285: Return one live claim for a bounded lane or fail loud.
- `_record_required_outcome_admission` · `_record_required_outcome_admission(result: outcome_admission.OutcomeAdmissionResultV1, *, receipt_path: Path) -> dict[str, Any]` · line 2301: Record one required admission and fail before lifecycle mutation on deny.
- `_record_selection_pending_activation` · `_record_selection_pending_activation(result: outcome_admission.SelectionPendingActivationResultV1, *, receipt_path: Path) -> dict[str, Any]` · line 2320: Record the narrow pre-selection tracker bootstrap without calling it allow.
- `_require_staged_activation_arguments_match` · `_require_staged_activation_arguments_match(claim: coordination_claims.ClaimRecord, *, agent: str, project: str, scope: str, intent: str, plan_ref: str | None, repo_root: str, worktree_path: str, branch: str, session_id: str, session_name: str | None, broader_goal: str, claim_type: str | None, write_paths: list[str] | None, read_paths: list[str] | None, parent_scope: str | None, work_graph_path: str | None, work_unit_id: str | None, start_revision: str | None, plan_repo_root: str | None, plan_start_point: str | None, allow_parallel: bool) -> None` · line 2339: Reject any attempt to turn tracker attachment into claim replacement.
- `_claim_status` · `_claim_status(claim: coordination_claims.ClaimRecord) -> str` · line 2454: Return the current persisted status string for one claim.
- `_require_claim_actor` · `_require_claim_actor(claim: coordination_claims.ClaimRecord, *, actor_session_id: str | None) -> str` · line 2460: Require the exact native actor before a lane lifecycle mutation.
- `_recovery_action_for_claim` · `_recovery_action_for_claim(claim: coordination_claims.ClaimRecord, *, active_claims: list[coordination_claims.ClaimRecord] | None = None, now: datetime | None = None) -> str` · line 2484: Return the operator action implied by one claim's lifecycle state.
- `_worktree_is_clean` · `_worktree_is_clean(worktree_path: str) -> tuple[bool, str]` · line 2518: Return whether one worktree has a clean git status.
- `_claim_snapshot_any_status` · `_claim_snapshot_any_status(*, agent: str, project: str, scope: str) -> tuple[coordination_claims.ClaimRecord, dict[str, Any], Path, bytes]` · line 2533: Load one exact claim-byte snapshot regardless of lifecycle status.
- `_claim_record_any_status` · `_claim_record_any_status(*, agent: str, project: str, scope: str) -> tuple[coordination_claims.ClaimRecord, dict[str, Any], Path]` · line 2555: Load one claim regardless of current lifecycle status.
- `_resolve_claim_repo_root` · `_resolve_claim_repo_root(claim: coordination_claims.ClaimRecord) -> Path` · line 2571: Return the canonical repo root for one claim.
- `_cwd_inside` · `_cwd_inside(path: Path) -> bool` · line 2583: Return whether the current shell cwd is inside the target path.
- `_branch_exists` · `_branch_exists(repo_root: Path, branch: str) -> bool` · line 2597: Return whether one local branch ref exists.
- `_ref_exists` · `_ref_exists(repo_root: Path, ref: str) -> bool` · line 2610: Return whether one Git ref resolves to a commit.
- `_is_ancestor` · `_is_ancestor(repo_root: Path, ancestor_ref: str, descendant_ref: str) -> bool` · line 2623: Return whether ``ancestor_ref`` is integrated into ``descendant_ref``.
- `_validate_worktree_path_repair` · `_validate_worktree_path_repair(*, recorded_worktree_path: str, provided_worktree_path: str, branch: str) -> None` · line 2636: Fail closed before accepting a corrected ``worktree_path`` on resume.
- `_patch_without_blob_identity` · `_patch_without_blob_identity(patch: bytes) -> bytes` · line 2696: Remove full-index blob IDs and hunk-header line offsets while preserving the complete patch body.
- `_squash_merge_matches_branch` · `_squash_merge_matches_branch(repo_root: Path, *, branch_ref: str, merge_commit: str, default_ref: str) -> bool` · line 2723: Prove a one-parent merge commit carries exactly the task branch patch.
- `_discover_squash_merge_commit` · `_discover_squash_merge_commit(repo_root: Path, *, branch_ref: str, default_ref: str, candidate_cap: int = 100) -> str | None` · line 2769: Find the squash-merge commit for a branch, or None.
- `_validate_closeout_preflight` · `_validate_closeout_preflight(*, repo_root: Path, branch: str | None, disposition: str, disposition_reason: str | None, recovery_ref: str | None, merge_commit: str | None, allow_discard_unique: bool, delete_branch: bool, retain_canonical_default_branch: bool = False) -> CloseoutPreflight` · line 2819: Validate merge or explicit recovery evidence before any closeout mutation.
- `_detached_canonical_preflight` · `_detached_canonical_preflight(*, repo_root: Path, disposition: str, disposition_reason: str | None, recovery_ref: str | None, head_commit: str) -> CloseoutPreflight` · line 2987: Archive metadata for a retained pin only with independent remote history.
- `_captured_lane_preflight` · `_captured_lane_preflight(*, repo_root: Path, branch: str | None, disposition: str, disposition_reason: str | None, capture: dict[str, Any]) -> CloseoutPreflight` · line 3009: Preflight for a tracker-absent lane whose uncommitted state was captured (#2010).
- `_is_closed_lane_placeholder` · `_is_closed_lane_placeholder(path: Path) -> bool` · line 3060: Return whether ``path`` is the empty directory a closed lane leaves behind.
- `_leave_closed_lane_placeholder` · `_leave_closed_lane_placeholder(worktree_path: Path) -> None` · line 3069: Recreate the removed lane path as an empty directory.
- `_remove_worktree_path` · `_remove_worktree_path(repo_root: Path, worktree_path: Path) -> str` · line 3088: Remove one worktree path from a safe root-anchored control session.
- `_assert_worktree_removal_access` · `_assert_worktree_removal_access(worktree_path: Path) -> None` · line 3122: Fail before Git mutation when the current user cannot remove a tree.
- `_delete_branch` · `_delete_branch(repo_root: Path, branch: str | None, *, force: bool = False) -> str` · line 3147: Delete one local branch after worktree cleanup.
- `_MaintenanceRefreshSnapshot` · `_MaintenanceRefreshSnapshot` · line 3168: Immutable maintenance-bootstrap state observed before session refresh.
- `_validate_locked_sanctioned_maintenance_refresh` · `_validate_locked_sanctioned_maintenance_refresh(existing_claim: coordination_claims.ClaimRecord, *, claim_path: Path, claim_bytes: bytes, tracker_path: Path, tracker_bytes: bytes, existing_tracker: dict[str, Any], agent: str, project: str, scope: str, intent: str, plan_ref: str | None, repo_root: str, worktree_path: str, branch: str, session_id: str, session_name: str | None, broader_goal: str, current_phase: str, intended_next_phases: list[str] | None, depends_on_repos: list[str] | None, requires_shared_infra_changes: bool | None, stop_conditions: list[str] | None, notes: str | None, claim_type: str | None, write_paths: list[str] | None, read_paths: list[str] | None, parent_scope: str | None, work_graph_path: str | None, work_unit_id: str | None, start_revision: str | None, plan_repo_root: str | None, plan_start_point: str | None, allow_unplanned: bool, allow_parallel: bool, broad_scope_mode: str | None, broad_scope_reason: str | None, target_worktree_path: str | None, tracker_dir: Path) -> _MaintenanceRefreshSnapshot | None` · line 3178: Validate immutable refresh inputs against one locked claim/tracker snapshot.
- `start_session` · `start_session(*, agent: str, project: str, scope: str, intent: str, repo_root: str, worktree_path: str, branch: str, broader_goal: str, current_phase: str, plan_ref: str | None = None, session_id: str | None = None, session_name: str | None = None, intended_next_phases: list[str] | None = None, depends_on_repos: list[str] | None = None, requires_shared_infra_changes: bool | None = None, stop_conditions: list[str] | None = None, notes: str | None = None, claim_type: str | None = None, write_paths: list[str] | None = None, read_paths: list[str] | None = None, parent_scope: str | None = None, work_graph_path: str | None = None, work_unit_id: str | None = None, start_revision: str | None = None, plan_repo_root: str | None = None, plan_start_point: str | None = None, tracker_dir: Path = session_contracts.DEFAULT_SESSION_TRACKERS_DIR, allow_unplanned: bool = False, allow_parallel: bool = False, broad_scope_mode: str | None = None, broad_scope_reason: str | None = None, target_worktree_path: str | None = None, new_files: list[str] | None = None, outcome_selected: bool = False, outcome_bootstrap_plan: int | None = None, outcome_admission_receipt_path: Path = outcome_admission.DEFAULT_OUTCOME_ADMISSION_RECEIPT_PATH, verified_goal_default_revision: str | None = None, verified_maintenance_default_revision: str | None = None) -> dict[str, Any]` · line 3353: Create or refresh the session contract plus linked tracker artifact.
- `_require_delegation_session_id` · `_require_delegation_session_id(agent: str, session_id: str, *, field: str) -> str` · line 3864: Require one exact native-client identity without accepting nested prefixes.
- `_locked_delegation_parent` · `_locked_delegation_parent(*, agent: str, project: str, parent_scope: str, parent_session_id: str, repo_root: str, active_claims: list[coordination_claims.ClaimRecord]) -> coordination_claims.ClaimRecord` · line 3872: Return the exact healthy program root that may delegate one child lane.
- `start_delegated_session` · `start_delegated_session(*, agent: str, project: str, scope: str, intent: str, repo_root: str, worktree_path: str, branch: str, broader_goal: str, current_phase: str, parent_scope: str, parent_session_id: str, child_session_id: str, start_revision: str, write_paths: list[str], session_name: str | None = None, tracker_dir: Path = session_contracts.DEFAULT_SESSION_TRACKERS_DIR, notes: str | None = None, **legacy_fixed_fields: Any) -> dict[str, Any]` · line 3903: Create one narrow child claim using its authenticated parent as actor.
- `revoke_delegated_session` · `revoke_delegated_session(*, agent: str, project: str, scope: str, repo_root: str, worktree_path: str, branch: str, parent_scope: str, parent_session_id: str, child_session_id: str, expected_start_revision: str, tracker_path: str, note: str | None = None) -> dict[str, Any]` · line 4129: Cancel one pristine delegated child using its authenticated parent.
- `heartbeat_session` · `heartbeat_session(*, agent: str, project: str, session_id: str | None = None, scope: str | None = None, branch: str | None = None, current_phase: str | None = None, tracker_dir: Path = session_contracts.DEFAULT_SESSION_TRACKERS_DIR, outcome_selected: bool = False, outcome_admission_receipt_path: Path = outcome_admission.DEFAULT_OUTCOME_ADMISSION_RECEIPT_PATH) -> dict[str, Any]` · line 4325: Refresh claim heartbeat state and the linked tracker timestamp.
- `narrow_session_claim` · `narrow_session_claim(*, agent: str, project: str, scope: str, write_paths: list[str], session_id: str | None = None) -> dict[str, Any]` · line 4435: Narrow one live claim without renewing its heartbeat or expiry.
- `_blocker_claim_snapshots` · `_blocker_claim_snapshots(*, project: str, goal_scope: str, claims_dir: Path) -> tuple[ClaimQueueSnapshotV1, ...]` · line 4464: Project the locked canonical registry into the accepted evaluator contract.
- `_write_immutable_blocker_receipt` · `_write_immutable_blocker_receipt(receipt: BlockerDispositionApplicationReceiptV1, *, receipt_dir: Path) -> Path` · line 4514: Publish one receipt without permitting replacement or conflicting replay.
- `apply_blocker_disposition` · `apply_blocker_disposition(*, decision_input: BlockerDecisionInputV1, expected_result: BlockerDecisionResultV1, repository_root: Path, agent: str, project: str, root_scope: str, actor_session_id: str | None = None, claims_dir: Path | None = None, receipt_dir: Path | None = None) -> dict[str, Any]` · line 4549: Re-evaluate and consume one disposition against current canonical custody.
- `_status_sessions_locked` · `_status_sessions_locked(*, project: str | None = None, agent: str | None = None, scope: str | None = None, branch: str | None = None, session_id: str | None = None, include_ended: bool = False, now: datetime | None = None) -> dict[str, Any]` · line 4766: Return session summaries derived from claims plus linked trackers.
- `status_sessions` · `status_sessions(*, project: str | None = None, agent: str | None = None, scope: str | None = None, branch: str | None = None, session_id: str | None = None, include_ended: bool = False, now: datetime | None = None) -> dict[str, Any]` · line 4885: Observe claims and trackers without creating or pruning coordination artifacts.
- `end_runtime_session` · `end_runtime_session(*, agent: str, session_id: str | None = None, reason: str = 'session ended', claims_dir: Path | None = None) -> dict[str, Any]` · line 4930: Detach a terminated runtime from every exact-session live claim.
- `finish_session` · `finish_session(*, agent: str, project: str, scope: str, worktree_path: str, note: str | None = None, release_claim: bool = False, allow_dirty_handoff: bool = False, actor_session_id: str | None = None) -> dict[str, Any]` · line 4974: Close out one session or fail loud if the worktree state is unsafe.
- `_resolve_closeout_worktree_path` · `_resolve_closeout_worktree_path(claim: coordination_claims.ClaimRecord, requested_worktree_path: str | None) -> Path` · line 5041: Resolve physical cleanup to the real bootstrap target, never its sentinel.
- `close_session` · `close_session(*, agent: str, project: str, scope: str, worktree_path: str | None = None, branch: str | None = None, note: str | None = None, delete_branch: bool = True, disposition: str = MERGED_DISPOSITION, disposition_reason: str | None = None, recovery_ref: str | None = None, merge_commit: str | None = None, allow_discard_unique: bool = False, reconcile_missing_worktree: bool = False, expected_tracker_sha256: str | None = None, reconcile_canonical_root: bool = False, reconcile_session_ended: bool = False, expected_claim_sha256: str | None = None, mailbox_disposition: str | None = None, mailbox_note: str | None = None, actor_session_id: str | None = None, terminalize_shared_child: bool = False, tracker_absent: bool = False, recovery_archive_dir: str | None = None) -> dict[str, Any]` · line 5050: Finish, clean up, and release one claimed lane as a single sanctioned flow.
- `_verify_successor_custody_offer_state` · `_verify_successor_custody_offer_state(*, claim: coordination_claims.ClaimRecord, claim_snapshot_bytes: bytes, project: str, scope: str, worktree_path: str, branch: str, successor_custody_offer: session_continuity.SuccessorCustodyOfferV1, git_run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run) -> dict[str, Any]` · line 5393: Bind one immutable offer to the current lane without changing custody.
- `verify_successor_custody_offer_state` · `verify_successor_custody_offer_state(*, agent: str, project: str, scope: str, worktree_path: str, branch: str, successor_custody_offer: session_continuity.SuccessorCustodyOfferV1) -> dict[str, Any]` · line 5450: Verify a prepared offer against live state without reserving custody.
- `resume_session` · `resume_session(*, agent: str, project: str, scope: str, worktree_path: str, branch: str, current_phase: str, session_id: str | None = None, note: str | None = None, predecessor_process_pid: int | None = None, predecessor_process_start_ticks: int | None = None, successor_custody_offer: session_continuity.SuccessorCustodyOfferV1 | None = None, successor_custody_acceptance: session_continuity.SuccessorCustodyAcceptanceV1 | None = None, repair_worktree_path: bool = False, repair_missing_plan_ref: bool = False, successor_agent: str | None = None) -> dict[str, Any]` · line 5485: Reattach a new runtime session to an existing plan-bound lane.
- `abort_unfenced_session_takeover` · `abort_unfenced_session_takeover(*, agent: str, project: str, scope: str, worktree_path: str, session_id: str | None = None) -> dict[str, Any]` · line 5920: Recover a successor-owned reservation left before process fencing.
- `handoff_session` · `handoff_session(*, agent: str, project: str, scope: str, note: str, current_phase: str = 'handoff required', actor_session_id: str | None = None) -> dict[str, Any]` · line 5957: Mark one live lane as intentionally handed off.
- `abandon_session` · `abandon_session(*, agent: str, project: str, scope: str, note: str, actor_session_id: str | None = None) -> dict[str, Any]` · line 6003: Mark one live, or preserved session-ended, lane as explicitly abandoned.
- `_session_tracker_archive_root` · `_session_tracker_archive_root() -> Path` · line 6067: Return the canonical archive root beside the live session-tracker tree.
- `_branch_unique_commits` · `_branch_unique_commits(repo_root: Path, *, branch: str, upstream_ref: str) -> list[str]` · line 6073: Return branch commits with no patch-equivalent already on ``upstream_ref``.
- `_validate_orphaned_tracker_archival` · `_validate_orphaned_tracker_archival(*, tracker_path: Path, expected_tracker_sha256: str | None, allow_unique_branch_commits: bool) -> dict[str, Any]` · line 6096: Fail closed before archiving one claim-less tracker with no worktree.
- `archive_orphaned_session_tracker` · `archive_orphaned_session_tracker(*, tracker_path: str | Path, expected_tracker_sha256: str | None, note: str | None = None, allow_unique_branch_commits: bool = False, archive_root: str | Path | None = None) -> dict[str, Any]` · line 6300: Archive one claim-less session tracker whose worktree is already gone.

### [`enforced_planning/session_process_fencing.py`](../enforced_planning/session_process_fencing.py)

Exact predecessor-process fencing for cross-session Codex custody transfer.

**Symbols**

- `ProcessFenceReceiptV1` · `ProcessFenceReceiptV1` · line 37: Immutable proof that one exact predecessor Codex process exited.
- `ProcessFenceIntentV1` · `ProcessFenceIntentV1` · line 55: Durable pre-signal identity used to recover an interrupted fence.
- `PredecessorProcessIdentityV1` · `PredecessorProcessIdentityV1` · line 72: Exact live Codex process generation resolved before successor launch.
- `_trusted_codex_executable` · `_trusted_codex_executable(proc_root: Path) -> Path` · line 139: Resolve the exact Codex executable used by this successor runtime.
- `resolve_predecessor_process` · `resolve_predecessor_process(*, predecessor_session_id: str, worktree_path: str, trusted_codex_executable: Path, proc_root: Path = Path('/proc'), session_index: Path = DEFAULT_CODEX_SESSION_INDEX) -> PredecessorProcessIdentityV1` · line 253: Resolve exactly one direct Codex resume process for an offered owner.
- `fence_predecessor_process` · `fence_predecessor_process(*, predecessor_session_id: str, successor_session_id: str, worktree_path: str, predecessor_pid: int, transfer_epoch_sha256: str, predecessor_process_start_ticks: int, proc_root: Path = Path('/proc'), session_index: Path = DEFAULT_CODEX_SESSION_INDEX, receipt_root: Path = DEFAULT_FENCE_RECEIPT_ROOT, trusted_codex_executable: Path | None = None, timeout_seconds: float = 5.0, open_pidfd: Callable[[int], int] = _open_pidfd, signal_pidfd: Callable[[int, int], None] = _signal_pidfd, pidfd_exited: Callable[[int, float], bool] = _pidfd_exited, close_pidfd: Callable[[int], None] = os.close) -> dict[str, object]` · line 303: Terminate one exact Codex predecessor and persist fail-closed evidence.

### [`enforced_planning/session_target.py`](../enforced_planning/session_target.py)

Resolve a mutation target to one exact claimed worktree.

**Symbols**

- `SessionTargetError` · `SessionTargetError` · line 29: The hook could not prove one healthy exact-session target.
- `SessionTarget` · `SessionTarget` · line 38: One exact target selected by a healthy projected claim.
- `_bootstrap_target_worktree` · `_bootstrap_target_worktree(claim: dict[str, Any]) -> Path | None` · line 48: Read a v6 bootstrap target only from projection-bound canonical YAML.
- `effective_session_id` · `effective_session_id(payload: dict[str, Any], client: str) -> str` · line 79: Return the child agent identity when present, otherwise the session.
- `_validate_claimed_git_identity` · `_validate_claimed_git_identity(claim: dict[str, Any], *, worktree: Path) -> None` · line 110: Prove that a projected target is the claim's exact repository and branch.
- `resolve_exact_session_target` · `resolve_exact_session_target(payload: dict[str, Any], *, client: str, claims_dir: Path, projection_path: Path | None = None, target_worktree: Path | None = None) -> SessionTarget` · line 165: Select one healthy projected claim for the identity and optional target.

### [`enforced_planning/surface_runtime.py`](../enforced_planning/surface_runtime.py)

Revision-bound runtime leases for governed human-facing surfaces.

**Symbols**

- `SurfaceRuntimeError` · `SurfaceRuntimeError` · line 32: A surface declaration or runtime failed a deterministic precondition.
- `load_surface` · `load_surface(repo_root: Path, surface_id: str) -> SurfaceDefinition` · line 138: Load one surface from the repository-owned UI registry.
- `_terminate_started_process` · `_terminate_started_process(process: subprocess.Popen[bytes], timeout_seconds: float = 5.0) -> None` · line 358: Clean the private process group created by this invocation.
- `start_surface` · `start_surface(repo_root: Path, surface_id: str, *, mode: str = 'canonical', state_root: Path | None = None) -> dict[str, Any]` · line 404: Start one exact surface and return its readiness-verified lease.
- `list_leases` · `list_leases(*, state_root: Path | None = None, project_id: str | None = None) -> list[dict[str, Any]]` · line 523: Return every lease with freshly evaluated process state.
- `stop_surface` · `stop_surface(repo_root: Path, surface_id: str, *, lease_id: str | None = None, state_root: Path | None = None) -> dict[str, Any]` · line 535: Stop only the exact process represented by a selected lease.
- `audit_surface` · `audit_surface(repo_root: Path, surface_id: str, *, state_root: Path | None = None, require_running: bool = False) -> dict[str, Any]` · line 562: Compare repository authority, lease state, and served identity.
- `live_leases_for_worktree` · `live_leases_for_worktree(worktree_path: Path, *, state_root: Path | None = None) -> list[dict[str, Any]]` · line 600: Return live leases whose recorded cwd belongs to one worktree.
- `assert_no_live_leases_for_worktree` · `assert_no_live_leases_for_worktree(worktree_path: Path, *, state_root: Path | None = None) -> None` · line 620: Fail before worktree removal when a governed surface is still running.

_Coverage findings: python-docstring-missing._

### [`enforced_planning/verification_batch.py`](../enforced_planning/verification_batch.py)

Freeze terminal verification to immutable Git bytes until explicit invalidation.

**Symbols**

- `VerificationBatchError` · `VerificationBatchError` · line 20: Report malformed state or mutation of a frozen verification batch.
- `VerificationBatch` · `VerificationBatch` · line 25: Bind one terminal verification decision to exact Git bytes.
- `VerificationBatch.to_dict` · `to_dict(self) -> dict[str, Any]` · line 37: Return stable JSON-safe batch state for agents and hooks.
- `_git` · `_git(repo_root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]` · line 43: Run Git with captured output so failures remain actionable.
- `resolve_repo_root` · `resolve_repo_root(repo_root: Path) -> Path` · line 58: Resolve a caller path to the exact Git worktree under verification.
- `_git_private_path` · `_git_private_path(repo_root: Path, name: str) -> Path` · line 65: Return a worktree-local untracked Git metadata path.
- `state_path` · `state_path(repo_root: Path) -> Path` · line 75: Return the private state path for the current worktree.
- `history_path` · `history_path(repo_root: Path) -> Path` · line 82: Return the append-only local invalidation history path.
- `_head` · `_head(repo_root: Path) -> str` · line 89: Return the exact commit currently checked out.
- `_branch` · `_branch(repo_root: Path) -> str` · line 95: Return the symbolic branch and reject detached verification targets.
- `_tracked_dirty` · `_tracked_dirty(repo_root: Path) -> bool` · line 104: Return whether staged or unstaged tracked bytes differ from HEAD.
- `_normalize_relative_path` · `_normalize_relative_path(path: str) -> str` · line 112: Normalize one allowlisted repository-relative path without escape.
- `_untracked_paths` · `_untracked_paths(repo_root: Path) -> tuple[str, ...]` · line 126: Return every untracked, non-ignored file because it may affect execution.
- `_unexpected_untracked` · `_unexpected_untracked(repo_root: Path, allowed: tuple[str, ...]) -> tuple[str, ...]` · line 133: Return untracked files not covered by an explicit exact path or subtree.
- `load_batch` · `load_batch(repo_root: Path) -> VerificationBatch | None` · line 143: Load and strictly validate the active worktree batch, if any.
- `freeze_batch` · `freeze_batch(repo_root: Path, *, decision: str, command: str, allowed_untracked: tuple[str, ...] = ()) -> VerificationBatch` · line 177: Freeze a clean named branch at HEAD for one terminal decision.
- `check_batch` · `check_batch(repo_root: Path, *, require_active: bool = False) -> VerificationBatch | None` · line 220: Fail if an active batch no longer names the current clean branch bytes.
- `thaw_batch` · `thaw_batch(repo_root: Path, *, reason: str) -> VerificationBatch` · line 246: Invalidate a batch explicitly and retain a local audit record.

### [`enforced_planning/worktree_paths.py`](../enforced_planning/worktree_paths.py)

Importable workspace and canonical-repo path helpers.

**Symbols**

- `detect_workspace_root` · `detect_workspace_root(project_root: Path) -> Path` · line 8: Resolve the shared workspace root from main or worktree checkouts.
- `_canonical_root_from_gitfile` · `_canonical_root_from_gitfile(worktree_root: Path) -> Path | None` · line 19: Return the main checkout named by a linked worktree's ``.git`` gitfile.
- `resolve_canonical_repo_root` · `resolve_canonical_repo_root(repo_root: Path) -> Path` · line 67: Return the canonical repo root for a main checkout or linked worktree.
- `resolve_canonical_target_path` · `resolve_canonical_target_path(*, target_path: Path, repo_root: Path) -> Path | None` · line 102: Map a missing worktree-local path to the canonical repo root when safe.

### [`proposals/aes-brownfield-docs/layout_check.py`](../proposals/aes-brownfield-docs/layout_check.py)

layout_check.py REPO [REF] : is the repository's documentation organized in its declared AES layout?

### [`proposals/aes-brownfield-docs/reach.py`](../proposals/aes-brownfield-docs/reach.py)

reach.py REPO_PATH [REF] [--list] : can a reader reach every reader document from wiki/index.md in two links?

**Symbols**

- `Blobs` · `Blobs` · line 35: Read many files at one ref through a single `git cat-file --batch` process.

_Coverage findings: python-docstring-missing._

### [`proposals/aes-durable-docs/evidence/m5-sample-tools/gen.py`](../proposals/aes-durable-docs/evidence/m5-sample-tools/gen.py)

Write the per-plan sections of m5-disproof-sample.md from git, for the first 10 candidates.

_Coverage findings: python-docstring-missing._

### [`proposals/aes-durable-docs/evidence/m5-sample-tools/select.py`](../proposals/aes-durable-docs/evidence/m5-sample-tools/select.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`proposals/aes-durable-docs/review-page/build_page.py`](../proposals/aes-durable-docs/review-page/build_page.py)

Build index.html (the visual review page) from ../PLAN.md.

**Symbols**

- `table_after` · `table_after(text: str, heading: str) -> list[dict[str, str]]` · line 32: Rows of the first Markdown table after the line that starts with `heading`.
- `plain` · `plain(md: str) -> str` · line 51: Markdown cell -> plain text (drop backticks and bold).
- `need` · `need(w, title, lines = (), label = '', badge = '') -> int` · line 97: Height in px a node() of width w needs for its text (same arithmetic as node()).
- `node` · `node(x, y, w, h, title, lines = (), tip = '', cls = '', label = '', badge = '') -> str` · line 108: One box: optional small label line, bold title (wrapped), muted lines, badge, and an info mark.
- `milestones` · `milestones(text: str, adopted: str)` · line 372: Milestone state comes from the Output cell: 'done <date>:' prefix = done, 'done <date>' inside = partly done.

_Coverage findings: python-docstring-missing._

### [`proposals/aes-feedback-prevention/verify_case.py`](../proposals/aes-feedback-prevention/verify_case.py)

Parent check for the bounded native/Remote MCP instruction regression.

_Coverage findings: python-docstring-missing._

### [`proposals/aes-learning-loop/review-page/build_requirements.py`](../proposals/aes-learning-loop/review-page/build_requirements.py)

Build review-page/requirements.html: each of Brian's feedback-system requirements vs the running system.

### [`proposals/aes-planning/review-page/build_page.py`](../proposals/aes-planning/review-page/build_page.py)

Build aes-planning-plan.html from the adopted plan ../README.md (kept in step by hand).

_Coverage findings: python-docstring-missing._

### [`proposals/aes-planning/rollout/daily_report.py`](../proposals/aes-planning/rollout/daily_report.py)

Daily report on the AES commit rule across every repository (plan aes-planning, P4/P6).

**Symbols**

- `quick_plan_problems` · `quick_plan_problems(rows: list[tuple[str, dict]]) -> list[dict]` · line 79: [Goal] commits whose quick-plan notes (AES #269) say the saved check output is missing or that files fall outside the plan's list, one record per commit with the problem notes. Clean notes are not problems.
- `refresh_runtime` · `refresh_runtime() -> str` · line 107: Keep the hook runtime and shared plan root at AES main: fetch, move the runtime worktree to origin/main, and reinstall the `aes` tool when main moved (plans adopted in AES resolve from every repository through this checkout).

_Coverage findings: python-docstring-missing._

### [`proposals/aes-planning/rollout/install_everywhere.py`](../proposals/aes-planning/rollout/install_everywhere.py)

Wire the AES commit rule (`aes commit check`) into every repository under a workspace.

**Symbols**

- `aes_runtime` · `aes_runtime() -> str | None` · line 99: The `aes` the hooks will find: PATH first, then ~/.local/bin (where scheduled jobs look).
- `repo_id` · `repo_id(repo: Path) -> str` · line 117: The underlying repository's name: linked worktrees share one config, so they share one wrapper folder.
- `runs_rule` · `runs_rule(hook: Path) -> bool` · line 127: True when this commit-msg hook is AES-generated and calls ``aes commit check``.
- `is_aes_native` · `is_aes_native(repo: Path) -> bool` · line 135: An AES project whose own hooks (``aes hooks install`` into .githooks) already run the rule.
- `kind` · `kind(repo: Path) -> tuple[str, str]` · line 149: (kind, local hooksPath or '').

_Coverage findings: python-docstring-missing._

### [`proposals/aes-planning/rollout/misuse_review.py`](../proposals/aes-planning/rollout/misuse_review.py)

Nightly review of commits that passed the AES commit rule on form alone (plan aes-planning).

**Symbols**

- `find_commit` · `find_commit(repo: Path, subject: str, day: dt.date) -> str | None` · line 75: The commit in `repo` made on `day` whose subject is `subject` (logs carry no SHA: the commit-msg hook runs before the commit exists).

_Coverage findings: python-docstring-missing._

### [`proposals/aes-planning/rollout/replay_emergency.py`](../proposals/aes-planning/rollout/replay_emergency.py)

Replay the "Emergency: none" refusal over every [Unplanned] commit in ~/code since 2026-10-07 (ROLLOUT.md, 2026-10-08).

### [`proposals/aes-subagent-feedback/verify_canary.py`](../proposals/aes-subagent-feedback/verify_canary.py)

Check the actual native canary return against its frozen packet and result schema.

### [`proposals/agent-router/run-local-check.py`](../proposals/agent-router/run-local-check.py)

Detached local merge gate; records exact revision, command, timing and exit.

### [`proposals/doc-reach-new-docs/replay.py`](../proposals/doc-reach-new-docs/replay.py)

Replay: commits since 2026-10-07 in Brian-owned repos that ADD .md files; are the added files reachable from wiki/index.md within 2 links at that commit (daily-check rules)?

### [`proposals/doc-reach-new-docs/replay_compare.py`](../proposals/doc-reach-new-docs/replay_compare.py)

Replay for plan doc-reach-new-docs: for every commit since 2026-10-07 that added .md files in a Brian-owned repository under ~/code, compare the commit rule's new-document answer (run on that commit's tree loaded into a temporary index) with the daily check's (project-meta md_file_cap reachability at that commit). Prints one row per added file and the totals.

### [`proposals/harness-context/native-parity/input/enforced-planning/enforced_planning/coordination_claims.py`](../proposals/harness-context/native-parity/input/enforced-planning/enforced_planning/coordination_claims.py)

Cross-brain coordination claims for multi-agent work.

**Symbols**

- `ClaimRegistryLockTimeout` · `ClaimRegistryLockTimeout` · line 92: The single local claim writer stayed busy beyond the bounded wait.
- `ProgressEventV1` · `ProgressEventV1` · line 185: One explicit durable-advancement event for an owning live claim.
- `claim_registry_lock` · `claim_registry_lock(claims_dir: Path | None = None, *, timeout_seconds: float = CLAIM_REGISTRY_LOCK_TIMEOUT_SECONDS) -> Iterator[None]` · line 226: Serialize mutations, failing with an exact retry condition on contention.
- `_claim_write_staging_dir` · `_claim_write_staging_dir(claims_dir: Path) -> Path` · line 262: Return same-filesystem staging outside the live claim registry.
- `_prune_abandoned_claim_write_artifacts` · `_prune_abandoned_claim_write_artifacts(claims_dir: Path, *, minimum_age_seconds: int = CLAIM_WRITE_STAGING_MAX_AGE_SECONDS) -> int` · line 268: Remove only old atomic-write artifacts from sanctioned claim writers.
- `_atomic_write_claim` · `_atomic_write_claim(path: Path, payload: dict[str, Any]) -> None` · line 295: Replace one claim without exposing a truncated or partially written file.
- `_atomic_restore_file` · `_atomic_restore_file(path: Path, content: bytes | None) -> None` · line 328: Restore exact prior bytes, or exact prior absence, after a failed transition.
- `_replace_claim_and_refresh_projection_fail_atomic` · `_replace_claim_and_refresh_projection_fail_atomic(*, claim_path: Path, payload: dict[str, Any], claims_dir: Path) -> tuple[str, str]` · line 354: Replace claim plus projection or restore both exact preflight states.
- `replace_claim_payloads_and_refresh_projection_fail_atomic` · `replace_claim_payloads_and_refresh_projection_fail_atomic(*, replacements: dict[Path, dict[str, Any]], claims_dir: Path) -> tuple[str, str]` · line 376: Replace a bounded claim set or restore every claim and the projection.
- `refresh_prewrite_authority_projection` · `refresh_prewrite_authority_projection(claims_dir: Path | None = None) -> tuple[str, str]` · line 415: Regenerate the replaceable pre-write projection from canonical YAML.
- `_registry_digest` · `_registry_digest(claims_dir: Path) -> str` · line 428: Return the canonical digest used to bind derived projection state.
- `_registry_snapshot` · `_registry_snapshot(claims_dir: Path) -> dict[str, bytes]` · line 436: Read every YAML authority record once, keyed by the digest's own key.
- `_registry_digest_from_snapshot` · `_registry_digest_from_snapshot(snapshot: dict[str, bytes]) -> str` · line 442: Reproduce ``prewrite_claim_fast.registry_digest`` from an in-memory snapshot.
- `PruneRegistryDivergenceError` · `PruneRegistryDivergenceError` · line 460: The registry moved underneath an in-progress prune, after a mutation applied.
- `record_claim_mutation` · `record_claim_mutation(*, operation: 'claim_mutation_receipts.MutationOperation', claims_dir: Path, registry_digest_before: str | None, target_project: str | None, target_scope: str | None, target_claim_path: Path | None, session_id: str | None, projection_digest_after: str | None, archive_transaction_id: str | None = None, known_registry_digest_after: str | None = None, known_projection_current_after: bool | None = None) -> 'claim_mutation_receipts.ClaimMutationReceiptV1'` · line 471: Persist one terminal receipt after a sanctioned YAML/projection mutation.
- `active_session_takeover_reservation` · `active_session_takeover_reservation(payload: dict[str, Any]) -> dict[str, Any] | None` · line 546: Return one validated active custody-takeover reservation from raw claim state.
- `reject_mutation_during_session_takeover` · `reject_mutation_during_session_takeover(payload: dict[str, Any], *, operation: str) -> None` · line 575: Fence predecessor claim mutations while an exact custody takeover is active.
- `reserve_session_takeover` · `reserve_session_takeover(*, claim_file: Path, agent: str, project: str, scope: str, predecessor_session_id: str, successor_session_id: str, worktree_path: str, predecessor_pid: int, predecessor_process_start_ticks: int, reserved_at: str, pre_reservation_claim_bytes: bytes, claims_dir: Path | None = None) -> tuple[ClaimRecord, dict[str, Any], bytes, dict[str, Any]]` · line 592: Durably reserve one exact predecessor claim epoch before process fencing.
- `abort_unfenced_session_takeover_reservation` · `abort_unfenced_session_takeover_reservation(*, claim_file: Path, agent: str, project: str, scope: str, successor_session_id: str, worktree_path: str, claims_dir: Path | None = None) -> dict[str, Any]` · line 671: Cancel one successor-owned reservation before fencing ever began.
- `record_claim_narrow_mutation` · `record_claim_narrow_mutation(*, claims_dir: Path, registry_digest_before: str, target_project: str, target_scope: str, target_claim_path: Path, session_id: str, projection_digest_after: str) -> 'claim_mutation_receipts.NarrowClaimMutationReceiptV1'` · line 737: Persist one narrow receipt without extending the shared v1 operation enum.
- `PlanAuthorityBinding` · `PlanAuthorityBinding` · line 790: Resolved navigation-independent target and numbered-plan identities.
- `MethodConformanceRefusal` · `MethodConformanceRefusal` · line 830: A claim-admission refusal with one stable reason code.
- `MethodConformanceBindingV1` · `MethodConformanceBindingV1` · line 838: The exact receipt identity a plan-backed claim retains.
- `method_conformance_mode` · `method_conformance_mode(plan_root: Path, revision: str) -> Literal['required', 'off']` · line 872: Read the repository's structural requirement at the exact plan revision.
- `resolve_method_conformance_binding` · `resolve_method_conformance_binding(*, plan_root: Path | str, plan_revision: str, plan_number: int | None, receipt_ref: str | None, receipt_sha256: str | None) -> MethodConformanceBindingV1 | None` · line 908: Resolve the exact passing receipt a plan-backed claim names, or refuse.
- `CanonicalWorkUnitBinding` · `CanonicalWorkUnitBinding` · line 1005: Exact target-graph and optional external-plan authority custody.
- `CanonicalWorkUnitBinding.__iter__` · `__iter__(self) -> Iterator[object]` · line 1016: Retain the historical three-value unpacking API for local consumers.
- `coerce_canonical_work_unit_binding` · `coerce_canonical_work_unit_binding(binding: CanonicalWorkUnitBinding | tuple[str, tuple[str, ...], str]) -> CanonicalWorkUnitBinding` · line 1024: Adapt legacy test/consumer triples while callers migrate to typed custody.
- `ClaimRecord` · `ClaimRecord` · line 1036: Normalized coordination claim record used across readable schema versions.
- `ClaimRecord.primary_project` · `primary_project(self) -> str | None` · line 1086: Return the first project for CLI compatibility surfaces.
- `ClaimRecord.is_live` · `is_live(self) -> bool` · line 1090: Return whether the claim should participate in active coordination.
- `ClaimRecord.to_dict` · `to_dict(self) -> dict[str, Any]` · line 1094: Return a JSON/YAML-safe dictionary for reporting and persistence.
- `ClaimInteraction` · `ClaimInteraction` · line 1102: Describe how one candidate claim interacts with another active claim.
- `ClaimInteraction.to_dict` · `to_dict(self) -> dict[str, Any]` · line 1121: Return a JSON-safe interaction summary.
- `NarrowClaimResult` · `NarrowClaimResult` · line 1130: Committed result of one owner/session-bound subset-only narrowing.
- `NarrowClaimResult.to_dict` · `to_dict(self) -> dict[str, Any]` · line 1143: Return a JSON-safe narrowing result.
- `ClaimCheckResult` · `ClaimCheckResult` · line 1149: Structured result for candidate-vs-active-claims evaluation.
- `ClaimCheckResult.hard_conflicts` · `hard_conflicts(self) -> list[ClaimInteraction]` · line 1156: Return hard-conflict interactions only.
- `ClaimCheckResult.continuation` · `continuation(self) -> dict[str, Any]` · line 1160: Describe safe work that remains outside path-local claim conflicts.
- `ClaimCheckResult.to_dict` · `to_dict(self) -> dict[str, Any]` · line 1207: Return a JSON-safe check result.
- `is_goal_authority_ref` · `is_goal_authority_ref(plan_ref: str | None) -> bool` · line 1217: Return whether a ref names one explicit non-plan outcome authority.
- `requires_work_graph` · `requires_work_graph(plan_ref: str | None) -> bool` · line 1223: Return whether write ownership names plan-like authority needing a graph.
- `_normalized_repository_id` · `_normalized_repository_id(value: str) -> str` · line 1234: Normalize repository identity spellings used by qualified plan refs.
- `_qualified_plan_repository` · `_qualified_plan_repository(plan_ref: str | None) -> str | None` · line 1240: Return the explicit authority repository from ``repository#number``.
- `_claim_uses_external_plan_authority` · `_claim_uses_external_plan_authority(claim: ClaimRecord) -> bool` · line 1249: Return whether a claim's qualified plan belongs to another project.
- `claim_health_issues` · `claim_health_issues(claim: ClaimRecord) -> list[str]` · line 1257: Return machine-readable health issues for one normalized claim.
- `claim_health_status` · `claim_health_status(claim: ClaimRecord) -> str` · line 1324: Classify one claim as healthy or weak for registry/reporting surfaces.
- `normalize_plan_identity` · `normalize_plan_identity(plan_ref: str | None) -> str | None` · line 1329: Return one stable numbered-plan identity from descriptive plan text.
- `_same_claim` · `_same_claim(left: ClaimRecord, right: ClaimRecord) -> bool` · line 1348: Return whether two records identify the same canonical claim slot.
- `claim_hierarchy_issues` · `claim_hierarchy_issues(claim: ClaimRecord, *, active_claims: list[ClaimRecord]) -> list[str]` · line 1354: Validate one claim against the existing root-program hierarchy.
- `coordination_health_issues` · `coordination_health_issues(claim: ClaimRecord, *, active_claims: list[ClaimRecord]) -> list[str]` · line 1427: Return local metadata plus cross-claim hierarchy health issues.
- `validate_claim_hierarchy_for_creation` · `validate_claim_hierarchy_for_creation(candidate: ClaimRecord, *, active_claims: list[ClaimRecord]) -> None` · line 1437: Reject a new or refreshed session claim that would be hierarchically invalid.
- `session_root_conflicts` · `session_root_conflicts(claim: ClaimRecord, *, active_claims: list[ClaimRecord]) -> list[ClaimRecord]` · line 1452: Return other unparented lanes owned by the exact runtime session.
- `normalize_parent_scope` · `normalize_parent_scope(parent_scope: str | None, project: str | None) -> str | None` · line 1479: Store a parent scope as the bare scope its parent claim records.
- `validate_session_root_for_creation` · `validate_session_root_for_creation(candidate: ClaimRecord, *, active_claims: list[ClaimRecord]) -> None` · line 1495: Reject accidental tangent roots while preserving explicit parallelism.
- `validate_no_preserved_lane_conflict` · `validate_no_preserved_lane_conflict(candidate: ClaimRecord, *, claims: list[ClaimRecord]) -> None` · line 1513: Require explicit recovery before replacing preserved ended work.
- `_heartbeat_stale_after` · `_heartbeat_stale_after() -> timedelta` · line 1548: Return the configured heartbeat freshness window.
- `_progress_stale_after` · `_progress_stale_after() -> timedelta` · line 1562: Return the configured durable-progress lease and fail on invalid policy.
- `_run_git` · `_run_git(repo_root: Path, args: list[str]) -> subprocess.CompletedProcess[str]` · line 1577: Run one git command for lifecycle diagnostics without throwing.
- `_resolve_repo_root_from_worktree_path` · `_resolve_repo_root_from_worktree_path(worktree_path: str | None) -> Path | None` · line 1588: Resolve the canonical repo root from a claim worktree path when possible.
- `_resolve_default_branch` · `_resolve_default_branch(repo_root: Path) -> str | None` · line 1607: Return the canonical default branch name for one repo when resolvable.
- `_default_integration_ref` · `_default_integration_ref(repo_root: Path, default_branch: str) -> str` · line 1623: Prefer the canonical remote default ref when it exists.
- `resolve_default_integration_revision` · `resolve_default_integration_revision(repo_root: Path | str) -> str` · line 1631: Resolve one full immutable commit for the canonical integration tip.
- `validate_start_revision_targets` · `validate_start_revision_targets(*, repo_root: Path | str, start_revision: str, branch: str | None, worktree_path: str | None, require_branch: bool = False, require_worktree: bool = False) -> None` · line 1646: Require any existing execution identities to retain one start commit.
- `_claimed_worktree_has_pending_changes` · `_claimed_worktree_has_pending_changes(worktree_path: Path | None) -> bool` · line 1704: Return whether pending tracked or untracked work is positively proven.
- `claim_lifecycle_issues` · `claim_lifecycle_issues(claim: ClaimRecord) -> list[str]` · line 1720: Return mechanically provable stale-lifecycle issues for one live claim.
- `_claim_branch_unmerged_progress` · `_claim_branch_unmerged_progress(claim: ClaimRecord) -> dict[str, Any] | None` · line 1770: Return git evidence that a claim's branch holds real unmerged commits.
- `list_abandoned_claims` · `list_abandoned_claims(project: str | None = None, *, claims_dir: Path | None = None, min_ahead: int = 1) -> list[tuple[ClaimRecord, dict[str, Any]]]` · line 1821: Surface EXPIRED claims whose branch still holds real unmerged commits.
- `claim_liveness_issues` · `claim_liveness_issues(claim: ClaimRecord, *, now: datetime | None = None) -> list[str]` · line 1873: Return stale-session issues derived from heartbeat freshness.
- `_parse_aware_iso_datetime` · `_parse_aware_iso_datetime(value: Any) -> datetime | None` · line 1908: Parse a timezone-aware ISO timestamp without silently assuming UTC.
- `build_progress_event` · `build_progress_event(*, progress_kind: str, evidence_ref: str, next_action: str, expected_quiet_until: str | datetime | None = None, quiet_reason: str | None = None, progress_at: datetime | None = None) -> ProgressEventV1` · line 1922: Validate one server-timestamped progress event before claim mutation.
- `_progress_event_payload` · `_progress_event_payload(event: ProgressEventV1) -> dict[str, str | None]` · line 1947: Flatten a validated event into the additive claim storage contract.
- `claim_progress_issues` · `claim_progress_issues(claim: ClaimRecord, *, now: datetime | None = None) -> list[str]` · line 1962: Return instrumentation defects or an expired durable-progress lease.
- `claim_runtime_status` · `claim_runtime_status(claim: ClaimRecord, *, active_claims: list[ClaimRecord] | None = None, now: datetime | None = None) -> str` · line 2020: Classify one live claim across stale/stalled/weak/healthy states.
- `peer_claims_by_goal` · `peer_claims_by_goal(claims: 'list[ClaimRecord]') -> 'dict[str, list[ClaimRecord]]'` · line 2049: Group live claims that declare a byte-identical ``broader_goal``.
- `render_peer_claim_groups` · `render_peer_claim_groups(claims: 'list[ClaimRecord]') -> 'list[str]'` · line 2075: Render the shared-goal groups as display lines, or nothing when none.
- `claim_enforcement_issues` · `claim_enforcement_issues(claim: ClaimRecord) -> list[dict[str, str]]` · line 2088: Return blocking operator findings that require an explicit disposition.
- `validate_claim_for_creation` · `validate_claim_for_creation(claim: ClaimRecord) -> None` · line 2120: Reject new claims that omit required ownership metadata for live coordination.
- `_plan_number` · `_plan_number(plan_ref: str | None) -> int | None` · line 2155: Extract a numbered-plan identity from canonical claim spellings.
- `_resolve_commit` · `_resolve_commit(repo_root: Path, start_point: str, *, label: str) -> str` · line 2164: Resolve one commit-ish to a full immutable object ID.
- `_numbered_plan_digest` · `_numbered_plan_digest(repo_root: Path, revision: str, plan_number: int) -> str` · line 2174: Bind exact plan bytes even when structural integrity enforcement is off.
- `resolve_plan_authority_binding` · `resolve_plan_authority_binding(*, repo_root: str, plan_ref: str, start_point: str = 'HEAD', plan_repo_root: str | None = None, plan_start_point: str | None = None, target_repository_id: str | None = None) -> PlanAuthorityBinding` · line 2198: Resolve explicit plan authority separately from exact mutation-target custody.
- `resolve_canonical_work_unit_binding` · `resolve_canonical_work_unit_binding(*, repo_root: str, plan_ref: str, work_graph_path: str, work_unit_id: str, start_point: str = 'HEAD', plan_repo_root: str | None = None, plan_start_point: str | None = None, target_repository_id: str | None = None, method_receipt_ref: str | None = None, method_receipt_sha256: str | None = None) -> CanonicalWorkUnitBinding` · line 2259: Validate an owning plan graph and its target revision independently.
- `_parent_pid` · `_parent_pid(pid: int) -> int | None` · line 2413: Return a process's parent pid, or None when it cannot be read.
- `session_id_from_process_tree` · `session_id_from_process_tree(registry_dir: Path | None = None) -> str | None` · line 2426: Recover the owning Claude Code session id by walking process ancestry.
- `session_identity_aliases` · `session_identity_aliases(agent: str, resolved_session_id: str | None) -> tuple[str, ...]` · line 2455: Return every identity this process may legitimately claim ownership under.
- `resolve_session_id` · `resolve_session_id(agent: str, explicit_session_id: str | None = None) -> str | None` · line 2477: Return an explicit or environment-derived session identifier.
- `validate_native_session_binding` · `validate_native_session_binding(agent: str, session_id: str | None, *, require_native_marker: bool = False) -> None` · line 2508: Reject an explicit session identity that contradicts the native runtime.
- `_safe_string_list` · `_safe_string_list(value: Any) -> list[str]` · line 2543: Normalize a scalar-or-list YAML value into a clean string list.
- `_normalize_repo_path` · `_normalize_repo_path(path: str) -> str` · line 2564: Normalize a repo-relative path for parent/child overlap checks.
- `bootstrap_authority_disabled_worktree_path` · `bootstrap_authority_disabled_worktree_path(target_worktree_path: str) -> str` · line 2572: Return a deterministic non-Git path that older readers cannot authorize.
- `classify_broad_write_paths` · `classify_broad_write_paths(repo_root: str | None, write_paths: list[str], *, verified_new_files: set[str] | None = None) -> dict[str, str]` · line 2581: Classify root/top-level directory reservations without guessing.
- `_regular_top_level_files_at_revision` · `_regular_top_level_files_at_revision(repo_root: str | None, revision: str | None, write_paths: list[str]) -> set[str]` · line 2638: Return exact top-level regular files recorded by one retained Git tree.
- `_broad_scope_contract_issues` · `_broad_scope_contract_issues(claim: ClaimRecord) -> list[str]` · line 2676: Return deterministic schema-v6 broad-scope contract violations.
- `_projects_overlap` · `_projects_overlap(left: ClaimRecord, right: ClaimRecord) -> bool` · line 2782: Return whether two claims touch at least one common project.
- `_paths_overlap` · `_paths_overlap(left: str, right: str) -> bool` · line 2787: Return whether two normalized repo-relative paths overlap.
- `session_transcript_path` · `session_transcript_path(session_id: str | None, *, codex_root: Path | None = None, claude_root: Path | None = None) -> Path | None` · line 2800: Locate the runtime transcript one session is actually writing to.
- `session_last_active_at` · `session_last_active_at(session_id: str | None, *, codex_root: Path | None = None, claude_root: Path | None = None) -> datetime | None` · line 2833: Return when a session's own client last wrote, or None when unknowable.
- `describe_session_activity` · `describe_session_activity(last_active_at: datetime | None, *, now: datetime | None = None) -> str` · line 2854: Render one claim owner's liveness for an operator reading a conflict.
- `_is_append_only_path` · `_is_append_only_path(path: str) -> bool` · line 2874: Return whether a declared write path lands only in an append-only store.
- `_compute_overlapping_write_paths` · `_compute_overlapping_write_paths(candidate: ClaimRecord, other: ClaimRecord) -> list[str]` · line 2886: Return normalized write-path overlaps between two claims.
- `_overlap_relations` · `_overlap_relations(candidate: ClaimRecord, other: ClaimRecord) -> tuple[str, ...]` · line 2905: Classify every effective overlap from the candidate's perspective.
- `_reservation_kind` · `_reservation_kind(other: ClaimRecord, relations: tuple[str, ...]) -> str | None` · line 2926: Explain a parent reservation without changing conflict severity.
- `_current_diff_disjoint` · `_current_diff_disjoint(candidate: ClaimRecord, other: ClaimRecord) -> bool | None` · line 2938: Return advisory Git status disjointness, or unknown when unreadable.
- `_interaction_explanation` · `_interaction_explanation(candidate: ClaimRecord, other: ClaimRecord) -> dict[str, Any]` · line 2967: Build shared explanatory fields for one overlap interaction.
- `_git_worktree_boundary` · `_git_worktree_boundary(claim: ClaimRecord) -> tuple[Path, Path, Path, str] | None` · line 2982: Return verified repository, common-dir, worktree, and target kind.
- `_has_isolated_worktree_boundary` · `_has_isolated_worktree_boundary(candidate: ClaimRecord, other: ClaimRecord) -> bool` · line 3029: Return whether Git isolates the two overlapping mutation surfaces.
- `_has_write_ownership` · `_has_write_ownership(claim: ClaimRecord) -> bool` · line 3048: Return whether a claim owns its declared write paths.
- `_parse_iso_datetime` · `_parse_iso_datetime(value: Any) -> datetime | None` · line 3059: Parse an ISO timestamp from claim data if present.
- `_progress_text_with_presence` · `_progress_text_with_presence(data: dict[str, Any], key: str, *, null_is_invalid: bool = True) -> str | None` · line 3072: Preserve invalid explicit progress keys instead of erasing them as legacy absence.
- `normalize_claim` · `normalize_claim(data: dict[str, Any], *, source_file: str | None = None) -> ClaimRecord | None` · line 3088: Normalize a raw YAML claim into the v2 in-memory representation.
- `_load_claims` · `_load_claims(claims_dir: Path | None = None) -> list[ClaimRecord]` · line 3267: Load live claim files from the configured or explicitly supplied registry.
- `unregistered_claim_files` · `unregistered_claim_files() -> list[str]` · line 3320: Return claim-dir files that coordination tooling cannot parse as claims.
- `malformed_claim_files` · `malformed_claim_files(claims_dir: Path | None = None) -> list[dict[str, str]]` · line 3335: Return `.yaml` claim-dir files that exist but fail to parse as YAML.
- `_claim_filename` · `_claim_filename(agent: str, project: str, scope: str) -> str` · line 3365: Generate a deterministic filename for a claim.
- `check_claims` · `check_claims(project: str | None = None, *, claims_dir: Path | None = None) -> list[ClaimRecord]` · line 3374: Check active claims, optionally selecting a registry and project.
- `list_claims` · `list_claims(project: str | None = None, *, claims_dir: Path | None = None, include_inactive: bool = False) -> list[ClaimRecord]` · line 3382: List claims with an explicit option to retain non-live audit records.
- `evaluate_claim` · `evaluate_claim(candidate: ClaimRecord, *, active_claims: list[ClaimRecord] | None = None) -> ClaimCheckResult` · line 3398: Classify candidate claim interactions against active live claims.
- `build_candidate_claim` · `build_candidate_claim(*, agent: str, project: str, scope: str, intent: str, plan_ref: str | None = None, claim_type: str | None = None, write_paths: list[str] | None = None, read_paths: list[str] | None = None, worktree_path: str | None = None, repo_root: str | None = None, branch: str | None = None, session_name: str | None = None, broader_goal: str | None = None, tracker_path: str | None = None, session_id: str | None = None, heartbeat_at: str | None = None, status: str = 'active', parent_scope: str | None = None, notes: str | None = None, claimed_at: str | None = None, expires_at: str | None = None, updated_at: str | None = None, start_revision: str | None = None, plan_repo_root: str | None = None, plan_revision: str | None = None, plan_sha256: str | None = None, work_unit_id: str | None = None, work_graph_path: str | None = None, work_graph_sha256: str | None = None, approval_revisions: tuple[str, ...] = (), parallel_root_authorized: bool = False, progress_at: str | None = None, progress_kind: str | None = None, evidence_ref: str | None = None, next_action: str | None = None, expected_quiet_until: str | None = None, quiet_reason: str | None = None, broad_scope_mode: str | None = None, broad_scope_reason: str | None = None, target_worktree_path: str | None = None, contact_ref: str | None = None, new_files: list[str] | tuple[str, ...] | None = None, schema_version: int | None = None, method_receipt_ref: str | None = None, method_receipt_sha256: str | None = None) -> ClaimRecord` · line 3521: Build a normalized candidate claim from CLI or test inputs.
- `_refresh_exact_owner_claim` · `_refresh_exact_owner_claim(*, agent: str, project: str, scope: str, session_id: str | None, intent: str, plan_ref: str | None, claim_type: str | None, write_paths: list[str] | None, read_paths: list[str] | None, worktree_path: str | None, repo_root: str | None, branch: str | None, session_name: str | None, broader_goal: str | None, status: str, parent_scope: str | None, notes: str | None, allow_parallel: bool, broad_scope_mode: str | None, broad_scope_reason: str | None, target_worktree_path: str | None, ttl_hours: float) -> tuple[bool, str] | None` · line 3647: Expand an exact-owner live claim without reconstructing retained custody.
- `_tracker_path_yaml_error` · `_tracker_path_yaml_error(tracker_path: str | None) -> str | None` · line 3748: Why this tracker path cannot serve as a session tracker, or None.
- `_reject_unreadable_tracker_path` · `_reject_unreadable_tracker_path(tracker_path: str | None) -> None` · line 3790: Fail at claim time rather than stranding a lane at closeout.
- `create_claim` · `create_claim(agent: str, project: str, scope: str, intent: str, plan_ref: str | None = None, ttl_hours: float = DEFAULT_TTL_HOURS, claim_type: str | None = None, write_paths: list[str] | None = None, read_paths: list[str] | None = None, worktree_path: str | None = None, repo_root: str | None = None, branch: str | None = None, session_name: str | None = None, broader_goal: str | None = None, tracker_path: str | None = None, session_id: str | None = None, status: str = 'active', parent_scope: str | None = None, notes: str | None = None, work_graph_path: str | None = None, work_unit_id: str | None = None, start_point: str = 'HEAD', plan_repo_root: str | None = None, plan_start_point: str | None = None, resume_requested: bool = False, require_new: bool = False, allow_parallel: bool = False, require_native_session_binding: bool = False, require_native_session_marker: bool = False, broad_scope_mode: str | None = None, broad_scope_reason: str | None = None, target_worktree_path: str | None = None, contact_ref: str | None = None, new_files: list[str] | None = None, verified_goal_default_revision: str | None = None, verified_maintenance_default_revision: str | None = None, method_receipt_ref: str | None = None, method_receipt_sha256: str | None = None) -> tuple[bool, str]` · line 3798: Create a new claim after checking for hard conflicts.
- `_replacement_is_within_existing_authority` · `_replacement_is_within_existing_authority(replacement: str, existing: str) -> bool` · line 4130: Return whether one normalized replacement is equal to/below an old path.
- `_validate_bootstrap_target_identity` · `_validate_bootstrap_target_identity(claim: ClaimRecord) -> None` · line 4138: Require the separated bootstrap target to be the claimed Git branch/repository.
- `narrow_claim` · `narrow_claim(*, agent: str, project: str, scope: str, session_id: str | None, write_paths: list[str], claims_dir: Path | None = None, require_native_session_binding: bool = False, known_new_files: list[str] | None = None, start_revision: str | None = None) -> NarrowClaimResult` · line 4165: Commit one owner-only strict subset claim/projection transition.
- `hydrate_missing_session_ids` · `hydrate_missing_session_ids(*, agent: str, project: str, session_id: str | None = None, scope: str | None = None, branch: str | None = None) -> tuple[int, list[str], str]` · line 4303: Fill in missing session IDs for matching live claims.
- `_extended_lease_expiry` · `_extended_lease_expiry(current_expires_at: Any, renewed_at: str, ttl_hours: float) -> str` · line 4358: Return the later of a claim's current lease and one renewed at ``renewed_at``.
- `heartbeat_claims` · `heartbeat_claims(*, agent: str, project: str, session_id: str | None = None, scope: str | None = None, branch: str | None = None, claims_dir: Path | None = None, require_exact_session: bool = False, ttl_hours: float = DEFAULT_TTL_HOURS) -> tuple[int, list[str], str, str]` · line 4378: Refresh heartbeat metadata and the lease for live claims owned by one session.
- `record_progress_claims` · `record_progress_claims(*, agent: str, project: str, scope: str, progress_kind: str, evidence_ref: str, next_action: str, session_id: str | None = None, expected_quiet_until: str | datetime | None = None, quiet_reason: str | None = None, claims_dir: Path | None = None, require_native_session_binding: bool = False, now: datetime | None = None) -> tuple[ClaimRecord, ProgressEventV1]` · line 4480: Record durable advancement on exactly one live claim owned by this session.
- `end_session_claims` · `end_session_claims(*, agent: str, session_id: str | None = None, reason: str = 'session ended', claims_dir: Path | None = None) -> tuple[int, list[str], str, str]` · line 4591: Retire exact-session live ownership without deleting recovery state.
- `release_claim` · `release_claim(agent: str, project: str, scope: str, *, expected_session_id: str | None = None, expected_start_revision: str | None = None, allow_managed_lane_rollback: bool = False) -> tuple[bool, str]` · line 4651: Release an existing claim, optionally guarded by exact custody.
- `release_claims_for_branch` · `release_claims_for_branch(branch: str) -> tuple[int, list[str]]` · line 4719: Release every live canonical claim attached to one branch.
- `_archive_completed_claim_locked` · `_archive_completed_claim_locked(claim_file: Path, *, claims_dir: Path) -> tuple[ClaimRecord, claim_mutation_receipts.CompletedClaimArchiveReceiptV1]` · line 4745: Archive and remove one exact completed claim while the registry lock is held.
- `complete_claims_for_plan` · `complete_claims_for_plan(*, project: str, plan_ref: str, note: str | None = None) -> tuple[int, list[str]]` · line 4810: Mark matching live claims completed and return the affected scopes.
- `_matches_prune_selectors` · `_matches_prune_selectors(claim: ClaimRecord, *, agent: str | None, project: str | None, scope: str | None) -> bool` · line 4877: Return whether one normalized claim matches every supplied selector.
- `prune_expired` · `prune_expired(*, agent: str | None = None, project: str | None = None, scope: str | None = None) -> tuple[int, list[str]]` · line 4893: Remove selected expired claims and return count plus exact scope labels.
- `prune_stale` · `prune_stale(*, agent: str | None = None, project: str | None = None, scope: str | None = None) -> tuple[int, list[str]]` · line 4943: Remove selected stale live claims and return count plus scope labels.
- `prune_completed` · `prune_completed(*, agent: str | None = None, project: str | None = None, scope: str | None = None) -> tuple[int, list[str]]` · line 4995: Remove claims already marked complete/completed.
- `backfill_completed_claim_archive` · `backfill_completed_claim_archive(*, source_claim_snapshot: Path, expected_source_sha256: str, prune_event_id: str) -> tuple[claim_mutation_receipts.CompletedClaimArchiveReceiptV1, bool]` · line 5204: Archive one legacy completed claim using exact bytes and prune provenance.
- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 5266: Parse CLI arguments for coordination-claim management.
- `_validate_explicit_prune_selectors` · `_validate_explicit_prune_selectors(args: argparse.Namespace) -> None` · line 5465: Reject empty prune selectors before the registry lock can be acquired.
- `_render_check_output` · `_render_check_output(*, claims: list[ClaimRecord], project: str | None, candidate: ClaimRecord | None) -> dict[str, Any]` · line 5476: Build a structured report for list/check operations.
- `_render_mutation_audit_failure` · `_render_mutation_audit_failure(exc: MutationAuditError, *, as_json: bool) -> int` · line 5536: Report an already-applied mutation whose receipt could not be persisted.
- `_render_completed_claim_archive_failure` · `_render_completed_claim_archive_failure(exc: CompletedClaimArchiveError, *, as_json: bool) -> int` · line 5546: Report an archive-before-prune failure that left claim YAML unchanged.
- `main` · `main(argv: list[str] | None = None) -> int` · line 5560: Run the CLI for cross-brain coordination claim management.

### [`proposals/harness-context/native-parity/input/project-meta/scripts/meta/check_coordination_claims.py`](../proposals/harness-context/native-parity/input/project-meta/scripts/meta/check_coordination_claims.py)

Compatibility facade for package-backed coordination claims.

**Symbols**

- `_find_repo_root` · `_find_repo_root() -> Path` · line 13: Resolve the nearest ancestor that contains the installed support package.
- `_sync_runtime_config` · `_sync_runtime_config() -> None` · line 52: Keep the package module aligned with script-level monkeypatches.
- `_cli_value` · `_cli_value(argv: list[str], flag: str) -> str | None` · line 57: Return one long-option value without trying to replace argparse.
- `_git_common_dir` · `_git_common_dir(path: Path) -> Path | None` · line 68: Return the absolute Git common dir for one checkout/worktree.
- `_validate_claim_repo_root` · `_validate_claim_repo_root(argv: list[str]) -> None` · line 81: Reject the worktree-as-repo-root ambiguity before a claim is persisted.
- `normalize_claim` · `normalize_claim(data: dict[str, Any], *, source_file: str | None = None) -> ClaimRecord | None` · line 113: Delegate normalized claim loading to the package module.
- `check_claims` · `check_claims(project: str | None = None, *, claims_dir: Path | None = None) -> list[ClaimRecord]` · line 118: Delegate live-claim loading with an optional explicit registry.
- `evaluate_claim` · `evaluate_claim(candidate: ClaimRecord, *, active_claims: list[ClaimRecord] | None = None) -> ClaimCheckResult` · line 124: Delegate candidate evaluation while honoring script-level CLAIMS_DIR overrides.
- `build_candidate_claim` · `build_candidate_claim(**kwargs: Any) -> ClaimRecord` · line 130: Delegate candidate claim construction to the package module.
- `validate_native_session_binding` · `validate_native_session_binding(agent: str, session_id: str | None) -> None` · line 135: Expose native runtime/session binding through the legacy facade.
- `claim_health_issues` · `claim_health_issues(claim: ClaimRecord) -> list[str]` · line 141: Expose claim health diagnostics through the legacy script surface.
- `claim_health_status` · `claim_health_status(claim: ClaimRecord) -> str` · line 146: Expose claim health classification through the legacy script surface.
- `normalize_plan_identity` · `normalize_plan_identity(plan_ref: str | None) -> str | None` · line 151: Expose normalized numbered-plan identity through the legacy surface.
- `claim_hierarchy_issues` · `claim_hierarchy_issues(claim: ClaimRecord, *, active_claims: list[ClaimRecord]) -> list[str]` · line 157: Expose root/child hierarchy diagnostics through the legacy surface.
- `claim_lifecycle_issues` · `claim_lifecycle_issues(claim: ClaimRecord) -> list[str]` · line 167: Expose stale-lifecycle diagnostics through the legacy script surface.
- `claim_runtime_status` · `claim_runtime_status(claim: ClaimRecord, *, active_claims: list[ClaimRecord] | None = None) -> str` · line 172: Expose combined stale/weak/healthy runtime classification.
- `claim_enforcement_issues` · `claim_enforcement_issues(claim: ClaimRecord) -> list[dict[str, str]]` · line 181: Expose blocking merged-ownership diagnostics through the legacy script surface.
- `claim_liveness_issues` · `claim_liveness_issues(claim: ClaimRecord, *, now: Any | None = None) -> list[str]` · line 187: Expose heartbeat-backed liveness diagnostics.
- `hydrate_missing_session_ids` · `hydrate_missing_session_ids(*args: Any, **kwargs: Any) -> tuple[int, list[str], str]` · line 192: Delegate session-id hydration while honoring script-level CLAIMS_DIR overrides.
- `create_claim` · `create_claim(*args: Any, **kwargs: Any) -> tuple[bool, str]` · line 198: Delegate claim creation while honoring script-level CLAIMS_DIR overrides.
- `release_claim` · `release_claim(*args: Any, **kwargs: Any) -> tuple[bool, str]` · line 204: Delegate claim release while honoring script-level CLAIMS_DIR overrides.
- `unregistered_claim_files` · `unregistered_claim_files() -> list[str]` · line 210: Delegate unregistered-format claim detection while honoring script-level CLAIMS_DIR overrides.
- `prune_expired` · `prune_expired(*args: Any, **kwargs: Any) -> tuple[int, list[str]]` · line 216: Delegate claim pruning while honoring script-level CLAIMS_DIR overrides.
- `prune_stale` · `prune_stale(*args: Any, **kwargs: Any) -> tuple[int, list[str]]` · line 222: Delegate stale-claim pruning while honoring script-level CLAIMS_DIR overrides.
- `prune_completed` · `prune_completed(*args: Any, **kwargs: Any) -> tuple[int, list[str]]` · line 228: Delegate completed-claim pruning while honoring script-level CLAIMS_DIR overrides.
- `heartbeat_claims` · `heartbeat_claims(*args: Any, **kwargs: Any) -> tuple[int, list[str], str, str]` · line 234: Delegate heartbeat refresh while honoring script-level CLAIMS_DIR overrides.
- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 240: Expose CLI argument parsing through the legacy script surface.
- `main` · `main(argv: list[str] | None = None) -> int` · line 245: Run the package-backed coordination-claims CLI.

### [`proposals/harness-context/native-parity/verify_evidence.py`](../proposals/harness-context/native-parity/verify_evidence.py)

Check saved paired traces without model calls; integrity is not behavior parity.

**Symbols**

- `review_result` · `review_result(result, review, root, checks)` · line 46: Check review coverage/provenance. A human or agent supplies semantic judgments.
- `behavior` · `behavior(semantics, derived, claude_raw)` · line 126: Legacy broader runtime certification, not the native task or session goal.
- `native_task_result` · `native_task_result(semantics, raw_results)` · line 154: Grade source correctness and literal JSON after trace/schema prerequisites.
- `packet_in_text` · `packet_in_text(text, packet)` · line 175: Recognize one complete exact task object amid other JSON values.
- `verify_child_callbacks` · `verify_child_callbacks(record, parent_id, turn_id, checks)` · line 198: Replay exact turn-correlated membership; receipts do not identify each tool.
- `output_parts` · `output_parts(value)` · line 395: Unwrap native text/JSON envelopes and retain literal shell outcome records.
- `derive_source_call_outcomes` · `derive_source_call_outcomes(rows, checks)` · line 467: Bind each source command to one terminal outcome; retain empty rg no-match.
- `derive_native_delivery` · `derive_native_delivery(parent_ref, child_ref, checks)` · line 502: Use the incumbent collector with only the exact parent/child local index.
- `verify_authority_reads` · `verify_authority_reads(rows, calls, packet, checks, *, strict = False)` · line 537: Check exact numbered source-line membership, without inferring prose meaning.
- `verify_required_authority` · `verify_required_authority(manifest, packet, role, parent, checks, *, context_dir = 'authority-context')` · line 582: Bind the native prompt to frozen authority, rather than a worker's echo.

_Coverage findings: python-docstring-missing._

### [`proposals/harness-context/review-page/build_page.py`](../proposals/harness-context/review-page/build_page.py)

Render the public-safe harness projection from the frozen findings.

### [`proposals/trace-review-enforcement/check_publication.py`](../proposals/trace-review-enforcement/check_publication.py)

One light shared-client read of new publication material; retains the actual verdict.

_Coverage findings: python-docstring-missing._

### [`proposals/trace-review-enforcement/run_final_gate.py`](../proposals/trace-review-enforcement/run_final_gate.py)

Detached local merge gate with retained output, timings and explicit exits.

### [`research/investigations/render_normative_record_views.py`](../research/investigations/render_normative_record_views.py)

Validate and render conventional views from one structured AES normative projection.

_Coverage findings: python-docstring-missing._

### [`research/investigations/validate_aes_company_planning_profile.py`](../research/investigations/validate_aes_company_planning_profile.py)

Bounded structural/profile probe for AES-CP-PROFILE-001.

_Coverage findings: python-docstring-missing._

### [`research/investigations/validate_architecture_blueprint.py`](../research/investigations/validate_architecture_blueprint.py)

Bounded structural probe for AES-BLUEPRINT-001, not a production AES schema.

**Symbols**

- `UniqueKeysLoader` · `UniqueKeysLoader` · line 21: Reject duplicate mapping keys instead of accepting the last value.

_Coverage findings: python-docstring-missing._

### [`research/investigations/validate_architecture_realization_schema.py`](../research/investigations/validate_architecture_realization_schema.py)

Validate an AES architecture-realization YAML record with JSON Schema 2020-12.

_Coverage findings: python-docstring-missing._

### [`research/investigations/validate_repository_context_source_context.py`](../research/investigations/validate_repository_context_source_context.py)

Bounded checker for the repository-context source-local normative-context pilot.

_Coverage findings: python-docstring-missing._

### [`scripts/artifact_creation.py`](../scripts/artifact_creation.py)

Run native, staged, reporting, and feedback artifact-governance operations.

**Symbols**

- `_parser` · `_parser() -> argparse.ArgumentParser` · line 31: Build the multi-operation command parser.
- `_native_notice` · `_native_notice(message: str) -> str` · line 83: Render a non-blocking client-visible hook notice.
- `_render_decision` · `_render_decision(decision: dict[str, Any], *, as_json: bool) -> int` · line 89: Render one decision for a native or terminal caller.
- `main` · `main(argv: list[str] | None = None) -> int` · line 118: Dispatch artifact creation operations.

### [`scripts/audit_dead_code.py`](../scripts/audit_dead_code.py)

Generate or refresh the reviewed dead-code audit file for one repo.

**Symbols**

- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 20: Parse CLI arguments for dead-code audit generation.
- `_merge_findings` · `_merge_findings(raw_findings: list[check_dead_code.Finding], *, detector: str, existing_entries: list[dict[str, Any]]) -> list[dict[str, Any]]` · line 42: Merge current detector output with any existing reviewer annotations.
- `build_audit_payload` · `build_audit_payload(repo_root: Path, output_file: str) -> dict[str, Any]` · line 89: Return the merged dead-code audit payload for one repo.
- `main` · `main(argv: list[str] | None = None) -> int` · line 118: Generate or refresh the current repo's dead-code audit file.

### [`scripts/check_dead_code.py`](../scripts/check_dead_code.py)

Dead code sensor for enforced-planning framework.

**Symbols**

- `Finding` · `Finding` · line 32: A single dead code finding from vulture or knip.
- `Result` · `Result` · line 43: Aggregated result of dead code detection.
- `_repo_python` · `_repo_python(project_root: Path) -> str` · line 58: Return the repo-local Python interpreter when one is available.
- `_load_config` · `_load_config(project_root: Path) -> dict[str, Any]` · line 76: Load dead_code config from meta-process.yaml.
- `_coerce_yaml_scalar` · `_coerce_yaml_scalar(raw_value: str) -> Any` · line 117: Convert a small YAML scalar into a Python value.
- `_load_dead_code_config_without_yaml` · `_load_dead_code_config_without_yaml(raw_text: str) -> dict[str, Any]` · line 136: Parse only the quality.dead_code block when PyYAML is unavailable.
- `_parse_vulture_line` · `_parse_vulture_line(line: str) -> Finding | None` · line 204: Parse a vulture output line into a Finding.
- `finding_signature` · `finding_signature(finding: Finding, detector: str | None) -> str` · line 223: Return the stable review signature for a finding.
- `_current_timestamp` · `_current_timestamp() -> str` · line 236: Return a stable UTC timestamp string.
- `_load_audit_payload` · `_load_audit_payload(project_root: Path, audit_file: str) -> dict[str, Any]` · line 242: Load the reviewed dead-code audit file when present.
- `_retained_audit_entries` · `_retained_audit_entries(project_root: Path, audit_file: str) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]` · line 259: Return retained audit entries keyed by signature plus the raw list.
- `_parse_knip_item` · `_parse_knip_item(issue_type: str, file_path: str, item: Any) -> Finding | None` · line 288: Convert one JSON knip issue item into a normalized finding.
- `_parse_knip_report` · `_parse_knip_report(output: str) -> list[Finding]` · line 323: Parse the JSON reporter output from knip.
- `_run_vulture` · `_run_vulture(project_root: Path, paths: list[str], min_confidence: int, whitelist: str) -> Result` · line 368: Run vulture for Python dead code detection.
- `_run_knip` · `_run_knip(project_root: Path) -> Result` · line 450: Run knip for TypeScript dead code detection.
- `scan_dead_code` · `scan_dead_code(project_root: Path) -> Result` · line 527: Run the raw dead-code detector without applying review policy.
- `check_dead_code` · `check_dead_code(project_root: Path) -> Result` · line 554: Run dead code detection and apply reviewed-retention policy.
- `main` · `main() -> None` · line 591: CLI entry point. Outputs JSON to stdout.

### [`scripts/check_doc_coupling.py`](../scripts/check_doc_coupling.py)

Check that documentation is updated when coupled source files change.

**Symbols**

- `load_yaml` · `load_yaml(path: Path)` · line 33: Load YAML from path and return dict-like object.
- `resolve_couplings` · `resolve_couplings(config_path: Path) -> list[dict]` · line 39: Load coupling definitions from legacy or unified config.
- `resolve_config_path` · `resolve_config_path(config_arg: str) -> Path` · line 59: Resolve default config path with legacy fallback.
- `get_changed_files` · `get_changed_files(base_ref: str) -> set[str]` · line 75: Get files changed between base_ref and HEAD.
- `get_staged_files` · `get_staged_files() -> set[str]` · line 99: Get files staged for commit.
- `load_couplings` · `load_couplings(config_path: Path) -> list[dict]` · line 113: Load coupling definitions from YAML.
- `validate_config` · `validate_config(couplings: list[dict]) -> list[str]` · line 118: Validate that all referenced files in config exist.
- `matches_any_pattern` · `matches_any_pattern(filepath: str, patterns: list[str]) -> bool` · line 138: Check if filepath matches any glob pattern.
- `load_ack_file` · `load_ack_file(ack_path: Path) -> dict[str, str]` · line 151: Load acknowledged doc-coupling gaps from a YAML file.
- `filter_violations_with_acks` · `filter_violations_with_acks(strict_violations: list[dict], acks: dict[str, str]) -> tuple[list[dict], list[dict]]` · line 176: Separate strict violations into remaining violations and acknowledged gaps.
- `matches_any_doc` · `matches_any_doc(filepath: str, docs: list[str]) -> bool` · line 203: Check whether a changed file matches any configured documentation target.
- `run_verify_sync` · `run_verify_sync(cmd: str) -> bool` · line 209: Run a verify_sync command. Returns True if docs are verified in sync.
- `check_couplings` · `check_couplings(changed_files: set[str], couplings: list[dict]) -> tuple[list[dict], list[dict]]` · line 224: Check which couplings have source changes without doc changes.
- `print_suggestions` · `print_suggestions(changed_files: set[str], couplings: list[dict]) -> None` · line 278: Print which docs should be updated based on changed files.
- `default_ack_file` · `default_ack_file() -> Path | None` · line 313: Return `<git toplevel>/.doc-coupling-acks` when it exists, else None.
- `main` · `main() -> int` · line 335: CLI entry point. Parses args and checks that docs are updated when coupled source files change.

### [`scripts/check_markdown_links.py`](../scripts/check_markdown_links.py)

Check local markdown link integrity for governance docs.

**Symbols**

- `LinkViolation` · `LinkViolation` · line 36: A broken or missing markdown link with source location and target details.
- `LinkViolation.format` · `format(self) -> str` · line 44: Format as file:line: message (target: ...) for terminal output.
- `_slugify_heading` · `_slugify_heading(value: str) -> str` · line 106: Generate a GitHub-compatible anchor slug from a heading string.
- `check_markdown_links` · `check_markdown_links(targets: list[str], root: Path) -> list[LinkViolation]` · line 211: Validate all local markdown links and anchors across the given targets.
- `main` · `main() -> int` · line 227: CLI entry point. Parses args and runs the markdown link integrity check.

### [`scripts/check_push_safety.py`](../scripts/check_push_safety.py)

Validate whether the current branch is safe to push.

**Symbols**

- `_print_notification_line` · `_print_notification_line(issue: dict[str, object]) -> None` · line 48: Surface whether the colliding claim's owner was notified.

_Coverage findings: python-docstring-missing._

### [`scripts/check_reachability.py`](../scripts/check_reachability.py)

Module reachability sensor.

**Symbols**

- `Report` · `Report` · line 50: Two measurements, because they answer different questions.
- `_module_name` · `_module_name(path: Path, root: Path, package_roots: list[Path]) -> str | None` · line 97: Map a file to its importable dotted name, or None if not importable.
- `_imports` · `_imports(path: Path, module: str, is_init: bool) -> list[str]` · line 111: Dotted names imported by this file, including `from x import y` targets.

_Coverage findings: python-docstring-missing._

### [`scripts/check_required_reading.py`](../scripts/check_required_reading.py)

Compatibility wrapper for required-read enforcement.

### [`scripts/coordination_hook.py`](../scripts/coordination_hook.py)

Expose canonical mailbox requests through native Codex lifecycle hooks.

**Symbols**

- `_bootstrap_package` · `_bootstrap_package() -> None` · line 28: Load the local package or a governed repo's upstream bootstrap.
- `RepositoryCloseoutError` · `RepositoryCloseoutError` · line 89: Compatibility name for unavailable turn-end repository safety evidence.
- `TurnEndProjectionError` · `TurnEndProjectionError` · line 93: Raised when derived claim state cannot be repaired within the Stop budget.
- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 97: Parse test and rollout overrides without changing the hook wire format.
- `_read_hook_input` · `_read_hook_input(*, project_supplied: bool) -> dict[str, Any]` · line 111: Read and validate the common native lifecycle-hook fields from stdin.
- `_canonical_project` · `_canonical_project(cwd: str) -> str | None` · line 126: Resolve a worktree cwd, or return no project for a non-Git workspace path.
- `_worktree_root` · `_worktree_root(cwd: str) -> Path | None` · line 152: Resolve the exact checkout containing cwd, preserving worktree identity.
- `_outcome_stop_decisions` · `_outcome_stop_decisions(*, payload: dict[str, Any], agent: str, session_id: str, cwd_project: str | None, active_claims: tuple[Any, ...]) -> tuple[outcome_completion.OutcomeCompletionStopDecisionV1, ...]` · line 167: Evaluate every exact-session claimed worktree plus the callback cwd.
- `_repository_scan_root` · `_repository_scan_root(cwd: str) -> Path` · line 201: Use one Git root locally, or the non-Git workspace root for a fleet scan.
- `_repository_status` · `_repository_status(repository: Path) -> dict[str, Any]` · line 220: Return a stable fingerprint of one repository's complete working-tree state.
- `_repository_statuses` · `_repository_statuses(repositories: tuple[Path, ...]) -> dict[str, dict[str, Any]]` · line 280: Capture status fingerprints concurrently for exact attributed repositories.
- `_write_closeout_baseline` · `_write_closeout_baseline(*, payload: dict[str, Any], agent: str, session_id: str, ledger_dir: Path) -> None` · line 306: Persist the session's initial repository state once, before mutation.
- `_projection_has_registry_change` · `_projection_has_registry_change(projection_path: Path, claims_dir: Path) -> bool` · line 338: Cheaply detect atomic writes, additions, or deletions since projection.
- `_repair_phase` · `_repair_phase(output: str | bytes | None) -> str` · line 352: Return the last content-free phase marker emitted by the repair worker.
- `_repair_turn_end_projection` · `_repair_turn_end_projection(claims_dir: Path, *, timeout: float = TURN_END_PROJECTION_REPAIR_TIMEOUT_SECONDS) -> dict[str, Any]` · line 363: Run the lock-owning projection repair in a killable, bounded subprocess.
- `_projection_is_current` · `_projection_is_current(claims_dir: Path) -> bool` · line 403: Check the derived projection against one lock-owned registry state.
- `_repair_projection_under_lock` · `_repair_projection_under_lock(claims_dir: Path) -> dict[str, Any]` · line 419: Recheck after writer contention and rebuild only genuinely stale state.
- `_active_claims` · `_active_claims(claims_dir: Path | None, *, turn_end: bool = False) -> tuple[Any, ...]` · line 444: Load active claims strictly, or repair derived state for ordinary turn end.
- `_startup_claims` · `_startup_claims(claims_dir: Path | None) -> tuple[tuple[Any, ...], str | None]` · line 524: Read one current projection without scanning or repairing claim YAML.
- `_startup_registry_read_lock` · `_startup_registry_read_lock(claims_dir: Path) -> Iterator[None]` · line 556: Observe claims and their projection under the writer's lock, without mutation.
- `_startup_claim_summary` · `_startup_claim_summary(*, agent: str, session_id: str, project: str | None, claims: tuple[Any, ...]) -> str | None` · line 589: Label exact-session ownership separately from other live project claims.
- `_canonical_repository_root` · `_canonical_repository_root(cwd: str) -> Path | None` · line 613: Resolve a linked worktree cwd to the canonical repository checkout.
- `_git_path` · `_git_path(repository: Path, option: str) -> Path` · line 632: Resolve one Git administrative path or fail closeout loudly.
- `_is_linked_worktree` · `_is_linked_worktree(repository: Path) -> bool` · line 649: Return whether one checkout has session-attributable Git custody.
- `_record_touched_repositories` · `_record_touched_repositories(*, payload: dict[str, Any], agent: str, session_id: str, ledger_dir: Path, active_claims: tuple[Any, ...]) -> None` · line 657: Persist only repositories this exact session had evidence of touching.
- `_repository_closeout_gate_disabled` · `_repository_closeout_gate_disabled() -> bool` · line 731: Whether the dirty-repository turn-end gate is switched off.
- `_repository_closeout_failure` · `_repository_closeout_failure(*, agent: str, session_id: str, ledger_dir: Path, active_claims: tuple[Any, ...]) -> str | None` · line 747: Explain session-created dirty repositories, or return a clean closeout.
- `_claimed_projects` · `_claimed_projects(*, agent: str, session_id: str, active_claims: tuple[Any, ...]) -> tuple[str, ...]` · line 815: Return exact-session live claim projects without adopting another lane.
- `_session_id` · `_session_id(agent: str, raw_session_id: str) -> str` · line 832: Normalize one native client session UUID into canonical claim identity.
- `_delivery_event_id` · `_delivery_event_id(payload: dict[str, Any], *, agent: str, session_id: str) -> str` · line 838: Derive one client-neutral identity for a native lifecycle callback.
- `_render_codex_result` · `_render_codex_result(event_name: str, summary: str) -> dict[str, Any]` · line 879: Render the event-specific output accepted by the native Codex client.
- `_tool_command` · `_tool_command(payload: dict[str, Any]) -> str | None` · line 892: Return the direct shell command from one native tool payload, when present.
- `_is_exact_acknowledgement_command` · `_is_exact_acknowledgement_command(payload: dict[str, Any], *, session_id: str, active_message_ids: tuple[str, ...]) -> bool` · line 905: Allow only one structurally exact mailbox acknowledgement shell command.
- `_is_mutation_boundary` · `_is_mutation_boundary(payload: dict[str, Any]) -> bool` · line 951: Return whether a PreToolUse callback represents a common mutation tool.
- `_render_boundary_denial` · `_render_boundary_denial(event_name: str, summary: str) -> dict[str, Any]` · line 958: Render a native blocking decision for mutation or final-response boundaries.
- `_is_completion_shaped_stop` · `_is_completion_shaped_stop(payload: dict[str, Any]) -> bool` · line 972: Classify an explicit completion protocol without interpreting free prose.
- `main` · `main(argv: list[str] | None = None) -> int` · line 1047: Refresh matching claim state and expose requests to the native session.

### [`scripts/coordination_inbox.py`](../scripts/coordination_inbox.py)

Poll the canonical coordination mailbox for one live agent session.

**Symbols**

- `_bootstrap_package` · `_bootstrap_package() -> None` · line 12: Load a local installed package or the target repo's upstream bootstrap.
- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 43: Parse an agent-drivable inbox poll command.
- `main` · `main(argv: list[str] | None = None) -> int` · line 56: Poll, optionally append observation evidence, and render the notice.

### [`scripts/coordination_messages.py`](../scripts/coordination_messages.py)

Run the package-backed cross-client coordination mailbox CLI.

**Symbols**

- `_bootstrap_package` · `_bootstrap_package() -> None` · line 10: Load a local installed package or the target repo's upstream bootstrap.

### [`scripts/coordination_operator_status.py`](../scripts/coordination_operator_status.py)

Show one message's human-identifiable recipient and truthful response state.

_Coverage findings: python-docstring-missing._

### [`scripts/hive/brain_fresh.py`](../scripts/hive/brain_fresh.py)

Is a project's brain older than the work done since? (hive brain v1, C-CONTEXT)

_Coverage findings: python-docstring-missing._

### [`scripts/hook_receipts.py`](../scripts/hook_receipts.py)

Private, content-free lifecycle receipts shared by portable agent hooks.

**Symbols**

- `HookReceiptError` · `HookReceiptError` · line 48: Raised when persisted hook evidence is incomplete or malformed.
- `_normalize_details` · `_normalize_details(details: dict[str, Any] | None) -> dict[str, str | int | float | bool | None] | None` · line 52: Validate a small, flat diagnostic map suitable for the shared index.
- `scan_prewrite_events` · `scan_prewrite_events(event_path: Path = DEFAULT_PREWRITE_EVENT_PATH) -> dict[str, Any]` · line 93: Scan the append-only prewrite JSONL store without hiding bad lines.
- `group_prewrite_recurrences` · `group_prewrite_recurrences(event_scan: dict[str, Any], *, threshold: int = 2) -> dict[str, Any]` · line 148: Group prewrite decisions by stable content-free failure dimensions.
- `HookInvocation` · `HookInvocation` · line 203: One hook invocation whose missing completion receipt proves interruption.
- `start_hook_invocation` · `start_hook_invocation(*, hook_name: str, hook_version: str, script_path: Path, payload: dict[str, Any], receipt_root: Path = DEFAULT_RECEIPT_ROOT) -> HookInvocation` · line 239: Write a started receipt before expensive work or semantic classification.
- `validate_completed_receipt` · `validate_completed_receipt(payload: Any, path: Path) -> str | None` · line 293: Return a human-readable defect reason, or None when the receipt is valid.
- `load_completed_receipts` · `load_completed_receipts(receipt_root: Path = DEFAULT_RECEIPT_ROOT) -> tuple[dict[str, Any], ...]` · line 314: Load strict content-free completion receipts in stable evidence order.
- `MalformedReceipt` · `MalformedReceipt` · line 345: One receipt file the sweep could not trust, kept as reportable evidence.
- `ReceiptScan` · `ReceiptScan` · line 359: Resilient sweep result: what parsed, what did not, and what never finished.
- `scan_hook_receipts` · `scan_hook_receipts(receipt_root: Path = DEFAULT_RECEIPT_ROOT) -> ReceiptScan` · line 384: Sweep every receipt directory without letting one bad record abort the run.
- `group_hook_recurrences` · `group_hook_recurrences(receipts: tuple[dict[str, Any], ...], *, threshold: int = 2) -> dict[str, Any]` · line 464: Group content-free episodes and retain exact receipt step-down evidence.
- `DeclaredHookCommand` · `DeclaredHookCommand` · line 512: One hook command registered in a settings file, with its declared budget.
- `load_declared_hook_commands` · `load_declared_hook_commands(settings_paths: tuple[Path, ...] = DEFAULT_SETTINGS_PATHS) -> tuple[tuple[DeclaredHookCommand, ...], tuple[str, ...]]` · line 533: Read hook command declarations and their timeouts from settings files.
- `match_declared_timeouts` · `match_declared_timeouts(receipts: tuple[dict[str, Any], ...], declared: tuple[DeclaredHookCommand, ...]) -> dict[str, dict[str, Any]]` · line 595: Bind emitting hook names to declared timeouts via recorded script digests.
- `percentile_nearest_rank` · `percentile_nearest_rank(values: list[float], percentile: float) -> float` · line 651: Nearest-rank percentile over an already-collected sample.
- `summarize_hook_health` · `summarize_hook_health(scan: ReceiptScan, *, declared: dict[str, dict[str, Any]] | None = None, budget_fraction: float = DEFAULT_TIMEOUT_BUDGET_FRACTION) -> dict[str, Any]` · line 663: Per-hook invocation count, latency distribution, exits, and orphaned starts.

_Coverage findings: python-docstring-missing._

### [`scripts/learning_loop/collect_feedback.py`](../scripts/learning_loop/collect_feedback.py)

Nightly feedback collector: transcripts -> one daily feedback log -> the learnings register.

**Symbols**

- `clip` · `clip(text: str, head: int = 700, tail: int = 300) -> str` · line 109: Keep the start and the end of a long error. log_learning prints the failing step first ("AUTOMATIC LEARNING LANE FAILED at: <step>") and the closeout residue last; keeping only the last 300 characters hid the cause of the 2026-10-07 stranded entries.
- `extract` · `extract(t: T.Transcript, text: str, turns: list[T.Turn], counts, errors) -> list[dict]` · line 221: One window of one transcript; windows of all transcripts run in one thread pool.
- `Register` · `Register` · line 279: Word-overlap (BM25) candidate retrieval over existing learnings; Jev judges the match.
- `filed_quotes` · `filed_quotes() -> set[str]` · line 329: Normalized text of every item already filed (from the daily logs), so a closeout line repeated across sessions is filed once. 2026-10-07 spot check: 2 of 10 filed entries were exact repeats.
- `filed_texts` · `filed_texts(days: int = 14, limit: int = 60) -> list[str]` · line 348: Quotes filed in the last `days` daily logs, newest last, for the reworded-repeat check.
- `repeats_filed` · `repeats_filed(quote: str, recent: list[str]) -> bool` · line 375: Light-model check: does this line state the same lesson as one filed recently, even reworded?
- `_repeat_or_defer` · `_repeat_or_defer(it: dict, recent: list[str]) -> str | None` · line 400: 'repeats_filed' for a reworded repeat, 'deferred_repeat_check' if the check failed (retried next run), else None.
- `earlier_splits` · `earlier_splits(ids: set[str], out: Path = OUT) -> dict[str, list[dict]]` · line 441: Records an earlier run already split each of `ids` into, from the first clean split in the daily report logs. A report the filing cap deferred is re-read next run; splitting it again with the light model can parse it differently and give one record id two payloads (project-meta #2538).
- `file_pending` · `file_pending(path: Path, cap: int, min_reusable: float = 0.6) -> tuple[int, list[str]]` · line 718: File items a dry run judged eligible; the day file stays append-only (update lines carry `filing_update`).

_Coverage findings: python-docstring-missing._

### [`scripts/learning_loop/effects.py`](../scripts/learning_loop/effects.py)

Effect boundaries are explicit enforcement receipts, never issue-close dates.

_Coverage findings: python-docstring-missing._

### [`scripts/learning_loop/evidence.py`](../scripts/learning_loop/evidence.py)

Resolve feedback references and count independent, verified observations.

**Symbols**

- `resolve_records` · `resolve_records(records: list[dict], db = None) -> dict[str, int]` · line 79: Annotate derived state, without rewriting the immutable source records.

_Coverage findings: python-docstring-missing._

### [`scripts/learning_loop/feedback_log.py`](../scripts/learning_loop/feedback_log.py)

Closeout Feedback fields -> feedback-report.v1 records -> the private feedback log.

**Symbols**

- `repo_of` · `repo_of(cwd: str) -> str` · line 32: `owner/repo` of the GitHub remote of the session's working directory ("" when unknown), cached.
- `reports` · `reports(t: T.Transcript, counts) -> list[dict]` · line 55: Every non-empty, non-"None" Feedback (or legacy Learnings) field in the agent's closeouts.
- `correction_reports` · `correction_reports(items: list[dict]) -> list[dict]` · line 80: Bridge already-extracted human corrections directly to immutable reports.
- `sentence_links` · `sentence_links(note: str, excerpt: str) -> list[R.Link]` · line 131: Links of the sentence holding `excerpt` when the excerpt itself has none: the nearest one before it in that sentence, else the nearest after. Position only; meaning is the model's job.
- `split_rest` · `split_rest(rep: dict, counts) -> list[str]` · line 144: Light-model split of a report's unmarked lines; returns error strings (empty when clean).
- `file_report` · `file_report(rep: dict) -> str` · line 221: Create the report's issue in the private log; returns its URL.
- `main` · `main() -> int` · line 238: File one report now (the `learned` skill's explicit invocation); the closeout then links the issue.

_Coverage findings: python-docstring-missing._

### [`scripts/learning_loop/fix_owner.py`](../scripts/learning_loop/fix_owner.py)

Weekly owner for the fixes the feedback loop licenses (plan aes-learning-loop, S6).

**Symbols**

- `check` · `check(number: int) -> dict` · line 136: What GitHub shows for one handed item: the only evidence this script trusts.
- `left_claims` · `left_claims(session_id: str | None) -> list[str]` · line 210: Claims the agent's own session still holds: a lane it opened and never closed.

_Coverage findings: python-docstring-missing._

### [`scripts/learning_loop/label_items.py`](../scripts/learning_loop/label_items.py)

Label lessons with Jev into failure-mode families (AES learning loop, slices 1-2).

_Coverage findings: python-docstring-missing._

### [`scripts/learning_loop/licences.py`](../scripts/learning_loop/licences.py)

S4: licences for proposed fixes, derived by the Observation-to-Action evaluator (PLAN.md, slice S4).

**Symbols**

- `fixture_for` · `fixture_for(problem: dict, fix: dict, challenged: bool, revoked: bool = False) -> dict` · line 29: One licence and its conditions as a metamodel record (nodes + hyperedges).
- `derive` · `derive(fixture: dict) -> str` · line 57: R-401 status from the metamodel's evaluator (imported from its checkout, not reimplemented).

_Coverage findings: python-docstring-missing._

### [`scripts/learning_loop/policies.py`](../scripts/learning_loop/policies.py)

Is each workspace rule documented, enforced, observed and on a feedback path? (plan aes-learning-loop, S8)

**Symbols**

- `registry_entries` · `registry_entries(registry: str) -> dict[str, dict]` · line 48: Top-level `- id:` blocks of registry.yaml, with the scalar fields this check reads.

_Coverage findings: python-docstring-missing._

### [`scripts/learning_loop/problems.py`](../scripts/learning_loop/problems.py)

S3: group related feedback records into problems and analyse the recurring ones (PLAN.md, slice S3).

**Symbols**

- `load_records` · `load_records(out: Path, days: int) -> list[dict]` · line 66: Every record of every report in the window, with the report's session, day and issue.
- `nearest_pairs` · `nearest_pairs(recs: list[dict]) -> list[tuple[int, int, float]]` · line 89: For each record, its most similar record from another report (one pair per unordered couple).
- `_with_evidence` · `_with_evidence(rec: dict, db: sqlite3.Connection | None) -> dict` · line 134: A record's view for a relation judge, with the title and opening of the issues it links to: a record's sentence is often a pointer ("another occurrence happened (#202)") and its content is in the evidence.
- `read_evidence` · `read_evidence(members: list[dict], db: sqlite3.Connection, limit: int = 10) -> list[str]` · line 213: Title and opening text of the GitHub issues the records link to, read by code (cached): the records point at their evidence instead of retelling it, so the analyst reads it here.
- `concern_enforcement` · `concern_enforcement(key: str) -> dict | None` · line 288: A completed concern needs an explicit, revision-bound enforcement receipt.
- `rank` · `rank(p: dict) -> tuple` · line 313: Impact first (independent sightings, sessions, records), then uncertainty (no analysis, inferred or guessed steps, no licence yet): high impact with high uncertainty sorts to the top (PLAN.md, What Brian sees).

_Coverage findings: python-docstring-missing._

### [`scripts/learning_loop/records.py`](../scripts/learning_loop/records.py)

Feedback records (contract feedback-report.v1): observations, claims and actions with links.

**Symbols**

- `Provenance` · `Provenance` · line 39: Who filed it, when, and from where (the nanopublication-style pubinfo).
- `find_links` · `find_links(text: str) -> list[Link]` · line 83: Every resolvable reference in `text`, in order, without duplicates.
- `normalize_links` · `normalize_links(links: list[Link], default_repo: str = '') -> list[Link]` · line 114: Qualify a bare `#N` with the session's repository, and drop an issue reference that a GitHub URL in the same list already names (`#300` beside `.../issues/300`).
- `_strip_links` · `_strip_links(text: str) -> str` · line 149: The sentence without its bracketed link references (kept in `links`); markdown link text stays.
- `parse_line` · `parse_line(line: str, prov: Provenance, observations: list[Record], default_repo: str = '') -> Record | None` · line 158: One marked Feedback line -> a Record, or None when the line carries no marker.
- `parse_feedback` · `parse_feedback(value: str, prov: Provenance, default_repo: str = '') -> tuple[list[Record], list[str]]` · line 209: A Feedback field -> (records from marked lines, unmarked non-empty lines left for the light model).

_Coverage findings: python-docstring-missing._

### [`scripts/learning_loop/relation_check.py`](../scripts/learning_loop/relation_check.py)

S2 measurement: does Jev judge how two feedback records relate well enough? (PLAN.md, "The S2 measurement").

_Coverage findings: python-docstring-missing._

### [`scripts/learning_loop/subagents.py`](../scripts/learning_loop/subagents.py)

Native child lifecycle -> existing feedback reports; parent checks bind exact results.

**Symbols**

- `Outcome` · `Outcome` · line 51: Additive report-envelope contract; existing feedback records stay unchanged.
- `rows` · `rows(path: Path)` · line 69: Stream complete native records with byte offsets; partial writes wait for reread.
- `messages_in` · `messages_in(value)` · line 102: Unwrap native code-tool output envelopes before reading fixed receipts.
- `claude_children` · `claude_children(parent: Path, session: str)` · line 119: Index native child identities and exact initial packets, without reading prose meaning.
- `calls` · `calls(path: Path, client: str)` · line 136: Pair calls/results over the whole changed parent, not the collector's new tail.
- `codex_index` · `codex_index(root: Path)` · line 255: Metadata-only index, once per collection; includes parents and children.
- `persist` · `persist(rep: dict, out: Path, file: bool) -> dict` · line 411: Use exactly the collector's daily report log and report-dedup table.

_Coverage findings: python-docstring-missing._

### [`scripts/learning_loop/transcripts.py`](../scripts/learning_loop/transcripts.py)

Read Claude Code and Codex transcripts as plain turns, and split closeout fields.

**Symbols**

- `read_transcript` · `read_transcript(path: Path, client: str, offset: int = 0, since: str = '') -> Transcript` · line 75: Turns from byte `offset` on (only complete lines), skipping records older than `since` (ISO).
- `split_closeout` · `split_closeout(text: str) -> tuple[str, dict[str, str]]` · line 145: (text before the closeout, {heading: value}) when `text` holds at least 3 closeout headings.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/apply_blocker_disposition.py`](../scripts/meta/apply_blocker_disposition.py)

Revalidate and safely apply one accepted Plan 110 blocker disposition.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/audit_dead_code.py`](../scripts/meta/audit_dead_code.py)

Generate or refresh the reviewed dead-code audit file for one repo.

**Symbols**

- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 20: Parse CLI arguments for dead-code audit generation.
- `_merge_findings` · `_merge_findings(raw_findings: list[check_dead_code.Finding], *, detector: str, existing_entries: list[dict[str, Any]]) -> list[dict[str, Any]]` · line 42: Merge current detector output with any existing reviewer annotations.
- `build_audit_payload` · `build_audit_payload(repo_root: Path, output_file: str) -> dict[str, Any]` · line 89: Return the merged dead-code audit payload for one repo.
- `main` · `main(argv: list[str] | None = None) -> int` · line 118: Generate or refresh the current repo's dead-code audit file.

### [`scripts/meta/canonical_lock.py`](../scripts/meta/canonical_lock.py)

Make a canonical checkout physically read-only while a lane claim is live.

**Symbols**

- `RegistryUnreadable` · `RegistryUnreadable` · line 147: The claim registry could not be trusted, so no unlock decision is safe.
- `LockReceipt` · `LockReceipt` · line 157: Durable record of one canonical lock, stored inside the repo's .git.
- `receipt_path` · `receipt_path(repo_root: Path) -> Path` · line 183: Return the receipt location, which lives in .git and is never locked.
- `refresh_lock_justifications` · `refresh_lock_justifications(repo_root: Path, *, justifying_claims: list[str], session_id: str | None = None) -> dict[str, Any]` · line 198: Atomically refresh claim metadata without changing recorded modes.
- `tracked_files` · `tracked_files(repo_root: Path) -> list[Path]` · line 260: Return tracked files, excluding anything under an excluded top-level dir.
- `lockable_paths` · `lockable_paths(repo_root: Path) -> tuple[list[Path], list[Path]]` · line 279: Return (files, directories) to lock.
- `_ensure_worktrees_dir` · `_ensure_worktrees_dir(repo_root: Path) -> None` · line 303: Guarantee ``worktrees/`` exists before the root becomes read-only.
- `_control_paths` · `_control_paths(repo_root: Path) -> tuple[Path, ...]` · line 315: Return excluded control paths that must stay user-writable.
- `_control_path_issues` · `_control_path_issues(repo_root: Path) -> list[str]` · line 338: Report excluded control paths that cannot support sanctioned Git work.
- `_restore_control_path_write_access` · `_restore_control_path_write_access(repo_root: Path) -> dict[str, Any]` · line 361: Repair only excluded control paths, never canonical or lane contents.
- `lock_repo` · `lock_repo(repo_root: Path, *, justifying_claims: list[str] | None = None, session_id: str | None = None) -> dict[str, Any]` · line 386: Make the canonical working tree read-only. Idempotent.
- `unlock_repo` · `unlock_repo(repo_root: Path) -> dict[str, Any]` · line 448: Restore recorded modes and drop the receipt. Idempotent.
- `_expected_locked_mode` · `_expected_locked_mode(recorded_mode: int) -> int` · line 514: The mode ``lock_repo`` would have produced for a path recorded as this.
- `_receipt_paths_deepest_first` · `_receipt_paths_deepest_first(receipt: LockReceipt) -> list[str]` · line 519: Recorded relative paths, deepest first with the repository root last.
- `verify_lock_integrity` · `verify_lock_integrity(repo_root: Path) -> dict[str, Any]` · line 524: Measure whether a recorded lock still holds, path by path.
- `relock_repo` · `relock_repo(repo_root: Path) -> dict[str, Any]` · line 597: Re-apply the lock's chmod to paths that drifted writable.
- `_index_record` · `_index_record(repo_root: Path, *, locked: bool) -> None` · line 671: Track which repositories hold a lock, so stale ones can be found.
- `load_live_lane_claims` · `load_live_lane_claims(claims_dir: Path | None = None) -> list[dict[str, Any]]` · line 700: Return live claims, or raise if the registry cannot be trusted.
- `repo_root_for_worktree` · `repo_root_for_worktree(worktree_path: str | None) -> Path | None` · line 734: Derive the canonical repository root from a claimed lane path.
- `live_lanes_by_repo` · `live_lanes_by_repo(claims_dir: Path | None = None) -> dict[Path, list[str]]` · line 753: Map canonical repository root -> scopes of live lane claims against it.
- `reconcile` · `reconcile(*, repos: list[Path] | None = None, claims_dir: Path | None = None, dry_run: bool = False, session_id: str | None = None) -> dict[str, Any]` · line 769: Bring lock state into agreement with live lane claims.
- `_committed_ancestor` · `_committed_ancestor(repo_root: Path, path: str, blob: str | None) -> str | None` · line 885: Return a commit reachable from HEAD whose version of ``path`` is ``blob``.
- `classify_dirty_entries` · `classify_dirty_entries(repo_root: Path, upstream: str) -> dict[str, Any]` · line 910: Split working-tree changes into upstream residue, benign untracked, and real work.
- `_restore_residue` · `_restore_residue(repo_root: Path, residue: list[dict[str, Any]]) -> None` · line 1006: Return residue paths to HEAD so a fast-forward can bring upstream's identical copy.
- `clear_upstream_residue` · `clear_upstream_residue(repo_root: Path, *, upstream: str | None = None) -> dict[str, Any]` · line 1024: Discard working-tree changes that are byte-identical to upstream; never touch real work.
- `sync_repo` · `sync_repo(repo_root: Path, *, ref_args: list[str] | None = None) -> dict[str, Any]` · line 1090: Fast-forward a locked canonical checkout, restoring the lock afterwards.
- `recovery_message` · `recovery_message(repo_root: Path) -> str` · line 1185: The escape hatch, printed at the moment of blocking rather than filed.
- `locked_repo_roots` · `locked_repo_roots() -> list[Path]` · line 1220: Return repositories currently holding a lock, cheaply.
- `_hook_text` · `_hook_text(payload: dict[str, Any]) -> str` · line 1237: Flatten the parts of a hook payload that can name a blocked path.
- `hook_main` · `hook_main(payload: dict[str, Any]) -> dict[str, Any] | None` · line 1259: Handle one hook event.
- `run_hook` · `run_hook(stream: Any = None) -> int` · line 1330: Read a hook payload and emit guidance. Always exits 0; never blocks.
- `_lane_probes` · `_lane_probes(repo: Path) -> list[dict[str, Any]]` · line 1424: Positive controls: the lane must still be fully usable.
- `grade_self_test` · `grade_self_test(*, locked: bool, writes: list[dict[str, Any]], lanes: list[dict[str, Any]]) -> dict[str, Any]` · line 1453: Grade a probe run. Only the locked arm can ever report boundary_verified.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/check_agents_sync.py`](../scripts/meta/check_agents_sync.py)

Check that generated AGENTS.md is in sync with canonical governance inputs.

**Symbols**

- `_detect_repo_root` · `_detect_repo_root(script_path: Path) -> Path` · line 14: Resolve repo root for both canonical and installed script layouts.
- `_renderer_entrypoint` · `_renderer_entrypoint(repo_root: Path) -> Path` · line 31: Return the truthful render entrypoint path for this repo layout.
- `resolve_inputs` · `resolve_inputs(repo_root: Path, claude_file: str = 'CLAUDE.md', relationships_file: str = 'scripts/relationships.yaml', output_file: str = 'AGENTS.md', template_path: Path = DEFAULT_TEMPLATE)` · line 51: Resolve AGENTS canonical inputs for one repo layout.
- `render_agents_markdown` · `render_agents_markdown(inputs)` · line 69: Render AGENTS using the truthful local renderer runtime.
- `parse_args` · `parse_args() -> argparse.Namespace` · line 75: Parse CLI arguments for the sync checker.
- `main` · `main() -> int` · line 113: Compare current AGENTS.md to the deterministic rendered output.

### [`scripts/meta/check_coordination_claims.py`](../scripts/meta/check_coordination_claims.py)

Compatibility facade for package-backed coordination claims.

**Symbols**

- `_find_repo_root` · `_find_repo_root() -> Path` · line 12: Resolve the nearest ancestor that contains the installed support package.
- `_sync_runtime_config` · `_sync_runtime_config() -> None` · line 51: Keep the package module aligned with script-level monkeypatches.
- `normalize_claim` · `normalize_claim(data: dict[str, Any], *, source_file: str | None = None) -> ClaimRecord | None` · line 56: Delegate normalized claim loading to the package module.
- `check_claims` · `check_claims(project: str | None = None, *, claims_dir: Path | None = None) -> list[ClaimRecord]` · line 61: Delegate live-claim loading with an optional explicit registry.
- `evaluate_claim` · `evaluate_claim(candidate: ClaimRecord, *, active_claims: list[ClaimRecord] | None = None) -> ClaimCheckResult` · line 67: Delegate candidate evaluation while honoring script-level CLAIMS_DIR overrides.
- `list_abandoned_claims` · `list_abandoned_claims(project: str | None = None, *, claims_dir: Path | None = None, min_ahead: int = 1) -> list[tuple[ClaimRecord, dict[str, Any]]]` · line 73: Delegate abandoned-expired-claim detection while honoring script-level CLAIMS_DIR overrides.
- `build_candidate_claim` · `build_candidate_claim(**kwargs: Any) -> ClaimRecord` · line 84: Delegate candidate claim construction to the package module.
- `validate_native_session_binding` · `validate_native_session_binding(agent: str, session_id: str | None) -> None` · line 89: Expose native runtime/session binding through the legacy facade.
- `claim_health_issues` · `claim_health_issues(claim: ClaimRecord) -> list[str]` · line 95: Expose claim health diagnostics through the legacy script surface.
- `claim_health_status` · `claim_health_status(claim: ClaimRecord) -> str` · line 100: Expose claim health classification through the legacy script surface.
- `normalize_plan_identity` · `normalize_plan_identity(plan_ref: str | None) -> str | None` · line 105: Expose normalized numbered-plan identity through the legacy surface.
- `claim_hierarchy_issues` · `claim_hierarchy_issues(claim: ClaimRecord, *, active_claims: list[ClaimRecord]) -> list[str]` · line 111: Expose root/child hierarchy diagnostics through the legacy surface.
- `claim_lifecycle_issues` · `claim_lifecycle_issues(claim: ClaimRecord) -> list[str]` · line 121: Expose stale-lifecycle diagnostics through the legacy script surface.
- `claim_runtime_status` · `claim_runtime_status(claim: ClaimRecord, *, active_claims: list[ClaimRecord] | None = None) -> str` · line 126: Expose combined stale/weak/healthy runtime classification.
- `claim_enforcement_issues` · `claim_enforcement_issues(claim: ClaimRecord) -> list[dict[str, str]]` · line 135: Expose blocking merged-ownership diagnostics through the legacy script surface.
- `claim_liveness_issues` · `claim_liveness_issues(claim: ClaimRecord, *, now: Any | None = None) -> list[str]` · line 141: Expose heartbeat-backed liveness diagnostics.
- `hydrate_missing_session_ids` · `hydrate_missing_session_ids(*args: Any, **kwargs: Any) -> tuple[int, list[str], str]` · line 146: Delegate session-id hydration while honoring script-level CLAIMS_DIR overrides.
- `create_claim` · `create_claim(*args: Any, **kwargs: Any) -> tuple[bool, str]` · line 152: Delegate claim creation while honoring script-level CLAIMS_DIR overrides.
- `release_claim` · `release_claim(*args: Any, **kwargs: Any) -> tuple[bool, str]` · line 158: Delegate claim release while honoring script-level CLAIMS_DIR overrides.
- `release_claims_for_branch` · `release_claims_for_branch(branch: str) -> tuple[int, list[str]]` · line 164: Delegate branch-wide claim release while honoring script-level CLAIMS_DIR overrides.
- `unregistered_claim_files` · `unregistered_claim_files() -> list[str]` · line 170: Delegate unregistered-format claim detection while honoring script-level CLAIMS_DIR overrides.
- `malformed_claim_files` · `malformed_claim_files() -> list[dict[str, str]]` · line 176: Delegate malformed-YAML claim detection while honoring script-level CLAIMS_DIR overrides.
- `prune_expired` · `prune_expired(*args: Any, **kwargs: Any) -> tuple[int, list[str]]` · line 182: Delegate claim pruning while honoring script-level CLAIMS_DIR overrides.
- `prune_stale` · `prune_stale(*args: Any, **kwargs: Any) -> tuple[int, list[str]]` · line 188: Delegate stale-claim pruning while honoring script-level CLAIMS_DIR overrides.
- `prune_completed` · `prune_completed(*args: Any, **kwargs: Any) -> tuple[int, list[str]]` · line 194: Delegate completed-claim pruning while honoring script-level CLAIMS_DIR overrides.
- `heartbeat_claims` · `heartbeat_claims(*args: Any, **kwargs: Any) -> tuple[int, list[str], str, str]` · line 200: Delegate heartbeat refresh while honoring script-level CLAIMS_DIR overrides.
- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 206: Expose CLI argument parsing through the legacy script surface.
- `main` · `main(argv: list[str] | None = None) -> int` · line 211: Run the package-backed coordination-claims CLI.

### [`scripts/meta/check_dead_code.py`](../scripts/meta/check_dead_code.py)

Dead code sensor for enforced-planning framework.

**Symbols**

- `Finding` · `Finding` · line 32: A single dead code finding from vulture or knip.
- `Result` · `Result` · line 43: Aggregated result of dead code detection.
- `_repo_python` · `_repo_python(project_root: Path) -> str` · line 58: Return the repo-local Python interpreter when one is available.
- `_load_config` · `_load_config(project_root: Path) -> dict[str, Any]` · line 76: Load dead_code config from meta-process.yaml.
- `_coerce_yaml_scalar` · `_coerce_yaml_scalar(raw_value: str) -> Any` · line 117: Convert a small YAML scalar into a Python value.
- `_load_dead_code_config_without_yaml` · `_load_dead_code_config_without_yaml(raw_text: str) -> dict[str, Any]` · line 136: Parse only the quality.dead_code block when PyYAML is unavailable.
- `_parse_vulture_line` · `_parse_vulture_line(line: str) -> Finding | None` · line 204: Parse a vulture output line into a Finding.
- `finding_signature` · `finding_signature(finding: Finding, detector: str | None) -> str` · line 223: Return the stable review signature for a finding.
- `_current_timestamp` · `_current_timestamp() -> str` · line 236: Return a stable UTC timestamp string.
- `_load_audit_payload` · `_load_audit_payload(project_root: Path, audit_file: str) -> dict[str, Any]` · line 242: Load the reviewed dead-code audit file when present.
- `_retained_audit_entries` · `_retained_audit_entries(project_root: Path, audit_file: str) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]` · line 259: Return retained audit entries keyed by signature plus the raw list.
- `_parse_knip_item` · `_parse_knip_item(issue_type: str, file_path: str, item: Any) -> Finding | None` · line 288: Convert one JSON knip issue item into a normalized finding.
- `_parse_knip_report` · `_parse_knip_report(output: str) -> list[Finding]` · line 323: Parse the JSON reporter output from knip.
- `_run_vulture` · `_run_vulture(project_root: Path, paths: list[str], min_confidence: int, whitelist: str) -> Result` · line 368: Run vulture for Python dead code detection.
- `_run_knip` · `_run_knip(project_root: Path) -> Result` · line 450: Run knip for TypeScript dead code detection.
- `scan_dead_code` · `scan_dead_code(project_root: Path) -> Result` · line 527: Run the raw dead-code detector without applying review policy.
- `check_dead_code` · `check_dead_code(project_root: Path) -> Result` · line 554: Run dead code detection and apply reviewed-retention policy.
- `main` · `main() -> None` · line 591: CLI entry point. Outputs JSON to stdout.

### [`scripts/meta/check_doc_coupling.py`](../scripts/meta/check_doc_coupling.py)

Check that documentation is updated when coupled source files change.

**Symbols**

- `load_yaml` · `load_yaml(path: Path)` · line 33: Load YAML from path and return dict-like object.
- `resolve_couplings` · `resolve_couplings(config_path: Path) -> list[dict]` · line 39: Load coupling definitions from legacy or unified config.
- `resolve_config_path` · `resolve_config_path(config_arg: str) -> Path` · line 59: Resolve default config path with legacy fallback.
- `get_changed_files` · `get_changed_files(base_ref: str) -> set[str]` · line 75: Get files changed between base_ref and HEAD.
- `get_staged_files` · `get_staged_files() -> set[str]` · line 99: Get files staged for commit.
- `load_couplings` · `load_couplings(config_path: Path) -> list[dict]` · line 113: Load coupling definitions from YAML.
- `validate_config` · `validate_config(couplings: list[dict]) -> list[str]` · line 118: Validate that all referenced files in config exist.
- `matches_any_pattern` · `matches_any_pattern(filepath: str, patterns: list[str]) -> bool` · line 138: Check if filepath matches any glob pattern.
- `load_ack_file` · `load_ack_file(ack_path: Path) -> dict[str, str]` · line 151: Load acknowledged doc-coupling gaps from a YAML file.
- `filter_violations_with_acks` · `filter_violations_with_acks(strict_violations: list[dict], acks: dict[str, str]) -> tuple[list[dict], list[dict]]` · line 176: Separate strict violations into remaining violations and acknowledged gaps.
- `matches_any_doc` · `matches_any_doc(filepath: str, docs: list[str]) -> bool` · line 203: Check whether a changed file matches any configured documentation target.
- `run_verify_sync` · `run_verify_sync(cmd: str) -> bool` · line 209: Run a verify_sync command. Returns True if docs are verified in sync.
- `check_couplings` · `check_couplings(changed_files: set[str], couplings: list[dict]) -> tuple[list[dict], list[dict]]` · line 224: Check which couplings have source changes without doc changes.
- `print_suggestions` · `print_suggestions(changed_files: set[str], couplings: list[dict]) -> None` · line 278: Print which docs should be updated based on changed files.
- `default_ack_file` · `default_ack_file() -> Path | None` · line 313: Return `<git toplevel>/.doc-coupling-acks` when it exists, else None.
- `main` · `main() -> int` · line 335: CLI entry point. Parses args and checks that docs are updated when coupled source files change.

### [`scripts/meta/check_plan_readiness.py`](../scripts/meta/check_plan_readiness.py)

Gate plan-owned lane creation on canonical readiness and explicit resume.

**Symbols**

- `_add_repo_root_to_path` · `_add_repo_root_to_path() -> None` · line 12: Make the adjacent source package importable from source or installed paths.
- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 31: Parse portable plan-start gate arguments.
- `main` · `main(argv: list[str] | None = None) -> int` · line 56: Run the gate and emit its strict result as JSON.

### [`scripts/meta/check_push_safety.py`](../scripts/meta/check_push_safety.py)

Validate whether the current branch is safe to push.

**Symbols**

- `_print_notification_line` · `_print_notification_line(issue: dict[str, object]) -> None` · line 48: Surface whether the colliding claim's owner was notified.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/claim_bootstrap.py`](../scripts/meta/claim_bootstrap.py)

Execute one strict, native-session self-claim bootstrap request.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/context_packet.py`](../scripts/meta/context_packet.py)

CLI wrapper for bounded relationship-aware edit context packets.

### [`scripts/meta/coordination_hook.py`](../scripts/meta/coordination_hook.py)

Run the native Codex mailbox hook from an installed governed repo.

### [`scripts/meta/coordination_inbox.py`](../scripts/meta/coordination_inbox.py)

Poll the canonical coordination mailbox from an installed governed repo.

### [`scripts/meta/coordination_messages.py`](../scripts/meta/coordination_messages.py)

Run the canonical coordination mailbox CLI from an installed governed repo.

### [`scripts/meta/coordination_operator_status.py`](../scripts/meta/coordination_operator_status.py)

Show one message's human-identifiable recipient and truthful response state.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/docstring_wiki.py`](../scripts/meta/docstring_wiki.py)

CLI wrapper for deterministic source-docstring wiki generation.

### [`scripts/meta/effective_project_profile.py`](../scripts/meta/effective_project_profile.py)

Print the effective governed-project profile as JSON.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/file_context.py`](../scripts/meta/file_context.py)

CLI wrapper for the importable file-context module.

**Symbols**

- `_detect_repo_root` · `_detect_repo_root(script_path: Path) -> Path` · line 10: Resolve repo root for both canonical and installed script layouts.

### [`scripts/meta/hook_log.py`](../scripts/meta/hook_log.py)

Append structured JSONL entries for Claude hook activity.

**Symbols**

- `_detect_repo_root` · `_detect_repo_root(script_path: Path) -> Path` · line 22: Resolve repo root for both canonical and installed script layouts.
- `_normalize` · `_normalize(path_text: str) -> str` · line 44: Return a stable forward-slash path string for logging.
- `_repo_root` · `_repo_root() -> Path` · line 49: Return the canonical repo root for this script.
- `_resolve_path` · `_resolve_path(repo_root: Path, raw_path: str) -> Path` · line 54: Resolve a repo-relative or absolute path against the repo root.
- `_repo_relative_path` · `_repo_relative_path(repo_root: Path, path: Path) -> str` · line 62: Return one normalized path string relative to the repo when possible.
- `_timestamp` · `_timestamp() -> str` · line 70: Return an ISO-8601 UTC timestamp suitable for JSONL logs.
- `_write_entry` · `_write_entry(log_file: Path, entry: dict[str, Any]) -> None` · line 75: Append one JSON line, creating the parent directory when needed.
- `_build_gate_entry` · `_build_gate_entry(repo_root: Path, file_path: str, tool_name: str, decision: str, reads_file: Path, config_path: Path, reason: str, context_emitted: bool, context_bytes: int, experiment_id: str | None, variant_id: str | None, downstream_run_id: str | None) -> dict[str, Any]` · line 82: Build a gate-decision log entry with resolved required-read state.
- `_build_read_entry` · `_build_read_entry(repo_root: Path, file_path: str, reads_file: Path, reason: str, experiment_id: str | None, variant_id: str | None, downstream_run_id: str | None) -> dict[str, Any]` · line 133: Build a read-tracking log entry after a read is appended.
- `main` · `main(argv: list[str] | None = None) -> int` · line 158: Dispatch hook-log subcommands for gate and read hooks.

### [`scripts/meta/hook_receipts.py`](../scripts/meta/hook_receipts.py)

Private, content-free lifecycle receipts shared by portable agent hooks.

**Symbols**

- `HookReceiptError` · `HookReceiptError` · line 48: Raised when persisted hook evidence is incomplete or malformed.
- `_normalize_details` · `_normalize_details(details: dict[str, Any] | None) -> dict[str, str | int | float | bool | None] | None` · line 52: Validate a small, flat diagnostic map suitable for the shared index.
- `scan_prewrite_events` · `scan_prewrite_events(event_path: Path = DEFAULT_PREWRITE_EVENT_PATH) -> dict[str, Any]` · line 93: Scan the append-only prewrite JSONL store without hiding bad lines.
- `group_prewrite_recurrences` · `group_prewrite_recurrences(event_scan: dict[str, Any], *, threshold: int = 2) -> dict[str, Any]` · line 148: Group prewrite decisions by stable content-free failure dimensions.
- `HookInvocation` · `HookInvocation` · line 203: One hook invocation whose missing completion receipt proves interruption.
- `start_hook_invocation` · `start_hook_invocation(*, hook_name: str, hook_version: str, script_path: Path, payload: dict[str, Any], receipt_root: Path = DEFAULT_RECEIPT_ROOT) -> HookInvocation` · line 239: Write a started receipt before expensive work or semantic classification.
- `validate_completed_receipt` · `validate_completed_receipt(payload: Any, path: Path) -> str | None` · line 293: Return a human-readable defect reason, or None when the receipt is valid.
- `load_completed_receipts` · `load_completed_receipts(receipt_root: Path = DEFAULT_RECEIPT_ROOT) -> tuple[dict[str, Any], ...]` · line 314: Load strict content-free completion receipts in stable evidence order.
- `MalformedReceipt` · `MalformedReceipt` · line 345: One receipt file the sweep could not trust, kept as reportable evidence.
- `ReceiptScan` · `ReceiptScan` · line 359: Resilient sweep result: what parsed, what did not, and what never finished.
- `scan_hook_receipts` · `scan_hook_receipts(receipt_root: Path = DEFAULT_RECEIPT_ROOT) -> ReceiptScan` · line 384: Sweep every receipt directory without letting one bad record abort the run.
- `group_hook_recurrences` · `group_hook_recurrences(receipts: tuple[dict[str, Any], ...], *, threshold: int = 2) -> dict[str, Any]` · line 464: Group content-free episodes and retain exact receipt step-down evidence.
- `DeclaredHookCommand` · `DeclaredHookCommand` · line 512: One hook command registered in a settings file, with its declared budget.
- `load_declared_hook_commands` · `load_declared_hook_commands(settings_paths: tuple[Path, ...] = DEFAULT_SETTINGS_PATHS) -> tuple[tuple[DeclaredHookCommand, ...], tuple[str, ...]]` · line 533: Read hook command declarations and their timeouts from settings files.
- `match_declared_timeouts` · `match_declared_timeouts(receipts: tuple[dict[str, Any], ...], declared: tuple[DeclaredHookCommand, ...]) -> dict[str, dict[str, Any]]` · line 595: Bind emitting hook names to declared timeouts via recorded script digests.
- `percentile_nearest_rank` · `percentile_nearest_rank(values: list[float], percentile: float) -> float` · line 651: Nearest-rank percentile over an already-collected sample.
- `summarize_hook_health` · `summarize_hook_health(scan: ReceiptScan, *, declared: dict[str, dict[str, Any]] | None = None, budget_fraction: float = DEFAULT_TIMEOUT_BUDGET_FRACTION) -> dict[str, Any]` · line 663: Per-hook invocation count, latency distribution, exits, and orphaned starts.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/impact_obligations.py`](../scripts/meta/impact_obligations.py)

CLI wrapper for relationship reconciliation impact reports.

### [`scripts/meta/outcome_completion_hook.py`](../scripts/meta/outcome_completion_hook.py)

Record canonical selected-outcome completion for a native Stop gate.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/plan_close.py`](../scripts/meta/plan_close.py)

Close every live lane owned by one qualified plan.

**Symbols**

- `_add_repo_root_to_path` · `_add_repo_root_to_path() -> None` · line 13: Make the sibling package importable from source and installed paths.
- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 31: Parse plan-close arguments.
- `main` · `main(argv: list[str] | None = None) -> int` · line 42: Run atomic plan-owned lane closeout.

### [`scripts/meta/pr_auto.py`](../scripts/meta/pr_auto.py)

Autonomous PR workflow with deterministic preflight checks.

**Symbols**

- `sanitize_github_env` · `sanitize_github_env(env: Mapping[str, str] | None = None) -> dict[str, str]` · line 36: Return env with token overrides removed so gh uses stored auth.
- `parse_github_repo_slug` · `parse_github_repo_slug(remote_url: str) -> str | None` · line 45: Parse owner/repo slug from common GitHub remote URL forms.
- `origin_matches_expected_repo` · `origin_matches_expected_repo(remote_url: str, expected_repo: str) -> bool` · line 60: Return True when origin URL resolves to the expected repository name.
- `resolve_github_account` · `resolve_github_account(explicit_account: str | None, remote_url: str) -> str` · line 69: Return the gh login to act as: explicit, else the origin repository owner.
- `filter_non_ignorable_status_lines` · `filter_non_ignorable_status_lines(lines: list[str]) -> list[str]` · line 85: Drop known transient metadata files from git-status output lines.
- `run_cmd` · `run_cmd(cmd: list[str], *, cwd: Path, env: dict[str, str] | None = None, check: bool = True) -> subprocess.CompletedProcess[str]` · line 98: Run command in cwd and return captured completed-process output.
- `isolated_github_auth` · `isolated_github_auth(*, cwd: Path, gh_env: dict[str, str], account: str) -> Iterator[dict[str, str]]` · line 167: Select one stored GitHub account without mutating the shared profile.
- `_staged_rebased_history` · `_staged_rebased_history(cwd: Path, *, base: str) -> Iterator[tuple[str, str]]` · line 245: Yield a temporary ref containing rebased history without moving the branch.
- `_publish_unpublished_branch` · `_publish_unpublished_branch(cwd: Path, *, branch: str, base: str) -> None` · line 304: Create a remote branch before advancing its clean local counterpart.
- `_prepare_branch_for_push` · `_prepare_branch_for_push(cwd: Path, *, branch: str, base: str) -> bool` · line 327: Publish an unpublished branch or validate a published fast-forward push.
- `main` · `main() -> int` · line 430: Execute preflighted non-interactive PR flow.

### [`scripts/meta/pr_review_signoff_runtime.py`](../scripts/meta/pr_review_signoff_runtime.py)

Exact-revision PR review orchestration and signoff receipts.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/project_status.py`](../scripts/meta/project_status.py)

Report current repository authority freshness and fail loud on stale main.

**Symbols**

- `_find_framework_root` · `_find_framework_root() -> Path` · line 12: Return the installed repository root containing the shared package.
- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 35: Parse repository status arguments.
- `main` · `main(argv: list[str] | None = None) -> int` · line 49: Render one exact freshness observation and return its gate status.

### [`scripts/meta/relationship_context.py`](../scripts/meta/relationship_context.py)

CLI wrapper for the source-local relationship context inventory.

### [`scripts/meta/render_agents_md.py`](../scripts/meta/render_agents_md.py)

Render a generated AGENTS.md projection from canonical repo governance.

**Symbols**

- `_repo_relative` · `_repo_relative(path: Path, repo_root: Path) -> str` · line 40: Return a stable path string for generated output provenance.
- `resolve_inputs` · `resolve_inputs(repo_root: Path, claude_file: str = 'CLAUDE.md', relationships_file: str = 'scripts/relationships.yaml', output_file: str = 'AGENTS.md', template_path: Path = DEFAULT_TEMPLATE) -> CanonicalInputs` · line 46: Resolve canonical input paths and fail loudly when missing.
- `render_agents_markdown` · `render_agents_markdown(inputs: CanonicalInputs) -> str` · line 63: Render the generated ``AGENTS.md`` content for a repo.
- `render_agents_md` · `render_agents_md(claude_path: Path) -> str` · line 68: Backwards-compatible wrapper around the explicit rendering API.
- `parse_args` · `parse_args() -> argparse.Namespace` · line 78: Parse CLI arguments for the renderer.
- `main` · `main() -> int` · line 83: Render ``AGENTS.md`` and write or print the result.

### [`scripts/meta/session_close.py`](../scripts/meta/session_close.py)

Close one claimed lane: cleanup worktree/branch and release claim together.

**Symbols**

- `_mailbox_dispositions` · `_mailbox_dispositions() -> list[str]` · line 38: Use mailbox closeout choices only when the installed lifecycle supports them.
- `_supported_closeout_kwargs` · `_supported_closeout_kwargs(args: argparse.Namespace) -> dict[str, object]` · line 54: Pass new closeout fields only to lifecycle modules that declare them.
- `_resolve_durable_repo_root` · `_resolve_durable_repo_root(repo_root: Path = REPO_ROOT) -> Path` · line 187: Return the canonical checkout that survives linked-worktree removal.
- `_materialize_shared_ref_history` · `_materialize_shared_ref_history(repo_root: Path, *, remote: str = 'origin', branch: str = 'main') -> str | None` · line 208: Refresh the durable shared-ref graph while the lane still owns writes.
- `_resolve_canonical_lock_module` · `_resolve_canonical_lock_module(*, repo_root: Path = REPO_ROOT, script_path: Path | None = None) -> Path | None` · line 248: Locate canonical_lock.py from either shipped script depth.
- `_reconcile_canonical_lock` · `_reconcile_canonical_lock(scope: str, module_path: Path | None = None) -> None` · line 287: Release the canonical lock once the lane that justified it is closed.
- `_lane_range_basis` · `_lane_range_basis(project: str, scope: str, branch: str | None, *, repo_root: Path = REPO_ROOT) -> tuple[str | None, str]` · line 324: The revision this lane branched from, read before the claim is released.
- `_report_shared_ref_movement` · `_report_shared_ref_movement(since_revision: str | None, basis: str, lane_refs: tuple[str, ...], *, repo_root: Path = REPO_ROOT) -> None` · line 355: Say whether the shared branch moved from outside this lane while it was open.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/session_continuity.py`](../scripts/meta/session_continuity.py)

Observe one claim owner and report resume-first continuity action.

**Symbols**

- `_bootstrap_package` · `_bootstrap_package() -> None` · line 24: Load vendored support at either source or installed script depth.
- `_assess_claim` · `_assess_claim(claim: coordination_claims.ClaimRecord, *, notify_minutes: int) -> dict[str, Any]` · line 211: Produce one fail-visible observation without creating takeover authority.
- `build_successor_offer_for_claim` · `build_successor_offer_for_claim(*, review: session_continuity.ResumeOfferReviewV1, claim: coordination_claims.ClaimRecord, run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run) -> session_continuity.SuccessorCustodyOfferV1` · line 257: Resolve exact durable claim and Git state for a launch-eligible offer.
- `persist_successor_offer` · `persist_successor_offer(offer: session_continuity.SuccessorCustodyOfferV1, *, offer_dir: Path = DEFAULT_SUCCESSOR_OFFER_DIR) -> Path` · line 292: Persist one immutable exact offer before any successor process starts.
- `launch_codex_successor` · `launch_codex_successor(launch: session_continuity.CodexSuccessorLaunchV1, *, run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run) -> session_continuity.CodexSuccessorLaunchReceiptV1` · line 320: Start one transient unit; launch acknowledgement is not custody acceptance.
- `build_observe_sweep` · `build_observe_sweep(*, notify_minutes: int) -> dict[str, Any]` · line 347: Observe every live Codex claim through one shared, non-mutating pass.
- `_append_receipt` · `_append_receipt(path: Path, payload: dict[str, Any]) -> None` · line 412: Append one fsynced sweep receipt while excluding overlapping sweeps.
- `_exclusive_sweep` · `_exclusive_sweep(receipt_path: Path) -> Iterator[None]` · line 431: Prevent two shared timer invocations from scanning concurrently.
- `run_observe_sweep` · `run_observe_sweep(*, notify_minutes: int, receipt_path: Path) -> dict[str, Any]` · line 446: Run and receipt one full observe sweep under the shared process lock.
- `_delivery_journal_states` · `_delivery_journal_states(receipt_path: Path) -> dict[str, session_continuity.NativeCodexDeliveryJournalV1]` · line 455: Load the latest valid write-ahead state for every delivery correlation.
- `_native_consumption_receipts` · `_native_consumption_receipts(receipt_path: Path) -> dict[str, session_continuity.NativeCodexConsumptionReceiptV1]` · line 503: Load one immutable active-client consumption receipt per correlation.
- `_native_successor_launch_states` · `_native_successor_launch_states(receipt_path: Path) -> dict[str, session_continuity.NativeCodexSuccessorLaunchJournalV1]` · line 533: Load the latest typed launch state for every exact successor offer.
- `reconcile_native_resume_consumption` · `reconcile_native_resume_consumption(*, receipt_path: Path) -> list[dict[str, Any]]` · line 584: Promote queue acceptance only when the exact owner transcript consumed it.
- `deliver_native_resume_offers` · `deliver_native_resume_offers(*, sweep: Mapping[str, Any], receipt_path: Path, codex: str = 'codex', run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run, git_run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run, max_consumed_attempts_without_progress: int = 2) -> list[dict[str, Any]]` · line 642: Queue bounded consumed attempts per unchanged durable progress fingerprint.
- `prepare_native_successor_offers` · `prepare_native_successor_offers(*, sweep: Mapping[str, Any], deliveries: Sequence[Mapping[str, Any]], receipt_path: Path, offer_dir: Path = DEFAULT_SUCCESSOR_OFFER_DIR, git_run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run, offer_verifier: Callable[..., Mapping[str, Any]] = session_lifecycle.verify_successor_custody_offer_state) -> list[dict[str, Any]]` · line 842: Persist and verify exhausted-retry custody offers without launching.
- `launch_verified_native_successors` · `launch_verified_native_successors(*, successor_offers: Sequence[Mapping[str, Any]], receipt_path: Path, resume_script: Path = DEFAULT_INSTALLED_RESUME_SCRIPT, codex: str = 'codex', systemd_run: str = 'systemd-run', run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run, process_resolver: Callable[[session_continuity.SuccessorCustodyOfferV1], session_process_fencing.PredecessorProcessIdentityV1] | None = None) -> list[dict[str, Any]]` · line 977: Launch each exact verified offer at most once; never claim acceptance.
- `run_native_delivery_sweep` · `run_native_delivery_sweep(*, notify_minutes: int, receipt_path: Path, codex: str = 'codex', successor_offer_dir: Path = DEFAULT_SUCCESSOR_OFFER_DIR, launch_native_successors: bool = False, installed_resume_script: Path = DEFAULT_INSTALLED_RESUME_SCRIPT, systemd_run: str = 'systemd-run', launch_run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run) -> dict[str, Any]` · line 1122: Observe and deliver owner-first prompts under one shared process lock.
- `run_native_consumption_reconciliation` · `run_native_consumption_reconciliation(*, receipt_path: Path) -> dict[str, Any]` · line 1202: Reconcile exact owner turns and report all durable receipts without delivery.
- `render_observe_timer` · `render_observe_timer(*, script_path: Path, python_path: Path, receipt_path: Path, timer_minutes: int, notify_minutes: int, delivery_enabled: bool = False, successor_launch_enabled: bool = False, codex_path: Path | None = None) -> tuple[str, str]` · line 1223: Render one shared oneshot service and its bounded observe timer.
- `install_observe_timer` · `install_observe_timer(*, unit_dir: Path, receipt_path: Path, timer_minutes: int, notify_minutes: int, run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run, delivery_enabled: bool = False, successor_launch_enabled: bool = False, codex: str = 'codex') -> dict[str, Any]` · line 1293: Install one shared observe or bounded native-delivery timer.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/session_end.py`](../scripts/meta/session_end.py)

Retire exact-session live claims when a tool runtime truly terminates.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/session_finish.py`](../scripts/meta/session_finish.py)

Finish one sanctioned session without worktree cleanup.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/session_heartbeat.py`](../scripts/meta/session_heartbeat.py)

Refresh heartbeat state for one sanctioned session.

**Symbols**

- `_bootstrap_package` · `_bootstrap_package() -> None` · line 12: Load local package support or the target repo's upstream bootstrap.
- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 40: Parse the session selector and optional phase refresh.
- `main` · `main(argv: list[str] | None = None) -> int` · line 63: Refresh the session heartbeat and expose its mailbox state.

### [`scripts/meta/session_narrow.py`](../scripts/meta/session_narrow.py)

Narrow one live claim to strict descendant write paths.

**Symbols**

- `_bootstrap_package` · `_bootstrap_package() -> None` · line 13: Load local package support or the target repo's upstream bootstrap.
- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 41: Parse the exact owner/session-bound narrowing contract.
- `main` · `main(argv: list[str] | None = None) -> int` · line 54: Narrow the claim and render its committed projection/receipt evidence.

### [`scripts/meta/session_resume.py`](../scripts/meta/session_resume.py)

Resume one plan-bound sanctioned session with a fresh runtime attachment.

**Symbols**

- `_bootstrap_package` · `_bootstrap_package() -> None` · line 12: Load local package support or the target repo's upstream bootstrap.
- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 45: Parse the bounded session-resume identity and phase contract.
- `main` · `main(argv: list[str] | None = None) -> int` · line 132: Resume the session and expose its current mailbox state.

### [`scripts/meta/session_start.py`](../scripts/meta/session_start.py)

Start or refresh one sanctioned session contract.

**Symbols**

- `_bootstrap_package` · `_bootstrap_package() -> None` · line 14: Load local package support or the target repo's upstream bootstrap.
- `_supported_start_kwargs` · `_supported_start_kwargs(args: argparse.Namespace) -> dict[str, Any]` · line 43: Retain compatibility with a target's older local lifecycle contract.
- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 109: Parse the complete session-start contract without hidden defaults.
- `_undeclared_plan_binding_message` · `_undeclared_plan_binding_message(args: argparse.Namespace) -> str | None` · line 180: Return the operator-facing denial when no plan binding was declared.
- `_fail` · `_fail(message: str, *, code: str, as_json: bool) -> int` · line 195: Emit one loud, actionable failure without a bare traceback.
- `main` · `main(argv: list[str] | None = None) -> int` · line 205: Start the session and expose its initial mailbox state.

### [`scripts/meta/session_status.py`](../scripts/meta/session_status.py)

Show live session summaries derived from claims plus trackers.

**Symbols**

- `enrich_client_displays` · `enrich_client_displays(payload: dict[str, object], *, codex_session_index: Path) -> None` · line 50: Add read-only client display projections to session-status output.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/surface_runtime.py`](../scripts/meta/surface_runtime.py)

Operate revision-bound canonical and preview UI surface leases.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/sync_plan_status.py`](../scripts/meta/sync_plan_status.py)

Sync and verify plan status across all locations.

**Symbols**

- `parse_plan_status` · `parse_plan_status(plan_path: Path) -> dict | None` · line 44: Parse status from a plan file.
- `_split_table_cells` · `_split_table_cells(line: str) -> list[str]` · line 94: Split a simple Markdown table row into trimmed cells.
- `_is_separator_row` · `_is_separator_row(line: str) -> bool` · line 99: Return true when a Markdown table row is only separator syntax.
- `_find_plan_index_table_rows` · `_find_plan_index_table_rows(content: str) -> tuple[list[str], dict[str, int]]` · line 107: Find the plan index table by header cells, not by surrounding heading.
- `parse_index_table` · `parse_index_table(index_path: Path) -> dict[int, dict]` · line 143: Parse the plan status table from index file.
- `collect_canonical_plan_statuses` · `collect_canonical_plan_statuses(index_statuses: dict[int, dict]) -> tuple[dict[int, dict], list[dict]]` · line 202: Select one canonical status source per plan number.
- `check_content_consistency` · `check_content_consistency() -> list[dict]` · line 246: Check that plan status matches content.
- `fix_content_status` · `fix_content_status() -> int` · line 285: Auto-fix status based on content.
- `check_consistency` · `check_consistency() -> list[dict]` · line 320: Check for inconsistencies between plan files and index.
- `sync_index_to_plans` · `sync_index_to_plans() -> int` · line 353: Update index table to match plan file statuses.
- `list_statuses` · `list_statuses() -> None` · line 430: List all plan statuses.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/validate_dead_code_audit.py`](../scripts/meta/validate_dead_code_audit.py)

Validate reviewed dead-code dispositions against fresh detector output.

**Symbols**

- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 24: Parse CLI arguments for audit validation.
- `_find_plan_file` · `_find_plan_file(repo_root: Path, plan_number: int) -> Path | None` · line 46: Return the numbered plan file if it exists.
- `_plan_status` · `_plan_status(plan_file: Path) -> str | None` · line 58: Return the plan's Status field when present.
- `validate_dead_code_audit` · `validate_dead_code_audit(repo_root: Path, audit_file: str) -> dict[str, Any]` · line 68: Validate the repo's reviewed dead-code dispositions.
- `main` · `main(argv: list[str] | None = None) -> int` · line 186: Validate the current repo's dead-code review file.

### [`scripts/meta/validate_doc_authority.py`](../scripts/meta/validate_doc_authority.py)

Validate or manage documentation-authority reconciliation obligations.

**Symbols**

- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 33: Parse CLI args for doc-authority validation and obligation management.
- `_print_json` · `_print_json(payload: object) -> None` · line 59: Emit stable JSON output.
- `main` · `main(argv: list[str] | None = None) -> int` · line 65: Run validation or mutate obligation state.

### [`scripts/meta/validate_plan.py`](../scripts/meta/validate_plan.py)

CLI wrapper for the importable plan-validation module.

**Symbols**

- `_detect_repo_root` · `_detect_repo_root(script_path: Path) -> Path` · line 11: Resolve repo root for both canonical and installed script layouts.
- `get_current_plan_number` · `get_current_plan_number() -> int | None` · line 74: Infer the active plan number using this repo's checkout root.
- `get_plan_file` · `get_plan_file(plan_number: int | None, plans_dir: Path, plan_file: str | None) -> Path` · line 79: Resolve one plan file using this repo's checkout root.
- `main` · `main() -> int` · line 89: Run plan validation using this repo's local defaults.

### [`scripts/meta/validate_plan_dependencies.py`](../scripts/meta/validate_plan_dependencies.py)

Validate the Plan #289 plan dependency contract.

**Symbols**

- `_detect_repo_root` · `_detect_repo_root(script_path: Path) -> Path` · line 29: Resolve repo root for both canonical and installed script layouts.
- `CorpusError` · `CorpusError` · line 54: The corpus needed for resolution could not be loaded.
- `active_projects` · `active_projects(graph_path: Path) -> list[tuple[str, Path]]` · line 90: Active registry records with an existing root, first owner of a root wins.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/verification_batch.py`](../scripts/meta/verification_batch.py)

Freeze, check, or explicitly invalidate an exact terminal verification batch.

**Symbols**

- `_parser` · `_parser() -> argparse.ArgumentParser` · line 29: Build the agent-drivable verification-batch command contract.
- `main` · `main() -> int` · line 52: Execute one verification-batch transition with visible failure output.

### [`scripts/meta/worktree-coordination/create_publish_worktree.py`](../scripts/meta/worktree-coordination/create_publish_worktree.py)

Create a publish worktree only when the canonical main checkout is clean.

**Symbols**

- `_load_create_worktree_module` · `_load_create_worktree_module()` · line 20: Load the sibling worktree-creation script as a module.
- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 33: Parse CLI arguments for publish-worktree creation.
- `main` · `main(argv: list[str] | None = None) -> int` · line 57: CLI entry point for publish-worktree creation.

### [`scripts/meta/worktree-coordination/create_review_claim.py`](../scripts/meta/worktree-coordination/create_review_claim.py)

Create a coordination-visible review claim for another branch.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/worktree-coordination/create_worktree.py`](../scripts/meta/worktree-coordination/create_worktree.py)

Create a git worktree and fail loud if the fresh checkout is unsafe.

**Symbols**

- `StatusEntry` · `StatusEntry` · line 38: One porcelain status entry from a worktree checkout.
- `WorktreeStatusSummary` · `WorktreeStatusSummary` · line 46: Summarize the immediate status of a freshly created worktree.
- `WorktreeCreationResult` · `WorktreeCreationResult` · line 58: Structured result for worktree creation and first-status verification.
- `CheckoutStateSummary` · `CheckoutStateSummary` · line 77: Summarize whether one checkout is safe to use as a control surface.
- `parse_args` · `parse_args(argv: list[str] | None = None) -> argparse.Namespace` · line 87: Parse CLI arguments for worktree creation.
- `run_git` · `run_git(args: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]` · line 170: Run one git command and capture stdout/stderr for diagnosis.
- `provisioning_marker_path` · `provisioning_marker_path(worktree_path: Path) -> Path` · line 181: Return the collision-resistant sibling marker for one target path.
- `write_provisioning_marker` · `write_provisioning_marker(*, worktree_path: Path, branch: str) -> Path` · line 187: Make an in-progress worktree creation discoverable before Git mutates it.
- `clear_provisioning_marker` · `clear_provisioning_marker(marker: Path) -> None` · line 207: Remove the marker only after creation has reached a terminal result.
- `branch_exists` · `branch_exists(repo_root: Path, branch: str) -> bool` · line 212: Return whether a local branch already exists in the target repo.
- `resolve_fresh_start_revision` · `resolve_fresh_start_revision(*, repo_root: Path, start_point: str) -> str` · line 218: Resolve a start revision after refreshing its configured upstream.
- `resolve_main_repo_root` · `resolve_main_repo_root(repo_root: Path) -> Path` · line 288: Resolve the canonical main repo root from either a root checkout or worktree.
- `get_default_worktree_dir` · `get_default_worktree_dir(repo_root: Path) -> Path` · line 302: Return the canonical worktrees/ directory inside this repo.
- `get_canonical_project_name` · `get_canonical_project_name(repo_root: Path) -> str` · line 308: Return a stable project name from root or linked-worktree context.
- `ensure_default_worktree_container_excluded` · `ensure_default_worktree_container_excluded(repo_root: Path, worktree_path: Path) -> bool` · line 314: Keep the required nested worktree container out of canonical status.
- `_load_claims_module` · `_load_claims_module() -> Any` · line 354: Load the sibling coordination-claims script as a module.
- `parse_status_porcelain` · `parse_status_porcelain(porcelain: str, *, split_brain_threshold: int) -> WorktreeStatusSummary` · line 366: Parse porcelain status output into a deterministic summary.
- `inspect_worktree_state` · `inspect_worktree_state(worktree_path: Path, *, split_brain_threshold: int) -> WorktreeStatusSummary` · line 405: Inspect immediate worktree status after creation.
- `classify_summary` · `classify_summary(summary: WorktreeStatusSummary) -> str` · line 423: Classify the immediate worktree state for operator-facing messages.
- `inspect_checkout_state` · `inspect_checkout_state(checkout_path: Path) -> CheckoutStateSummary` · line 432: Inspect whether one checkout is safe to use as a control surface.
- `verify_clean_main_root` · `verify_clean_main_root(repo_root: Path) -> tuple[bool, str]` · line 471: Require the canonical main checkout to be clean before publish-worktree creation.
- `cleanup_failed_worktree` · `cleanup_failed_worktree(repo_root: Path, worktree_path: Path, *, branch: str, created_branch: bool) -> tuple[bool, str]` · line 493: Attempt to remove a failed worktree and delete its just-created branch.
- `ensure_safe_target_path` · `ensure_safe_target_path(worktree_path: Path) -> None` · line 511: Reject non-empty target paths before invoking git worktree add.
- `_claim_project` · `_claim_project(repo_root: Path, explicit_project: str | None) -> str` · line 520: Resolve the project name used for scoped claim matching.
- `_write_paths_are_covered` · `_write_paths_are_covered(*, claims_module: Any, required_paths: list[str], claim_paths: list[str]) -> bool` · line 527: Return whether a scoped claim covers every required write path.
- `verify_scoped_write_claim` · `verify_scoped_write_claim(*, repo_root: Path, worktree_path: Path, branch: str, claim_agent: str | None, claim_project: str | None, claim_write_paths: list[str], claims_dir: Path | None, expected_start_revision: str | None = None) -> tuple[bool, str]` · line 535: Require matching explicit write authority and reject conflicting claims.
- `create_worktree` · `create_worktree(*, repo_root: Path, worktree_path: Path, branch: str, start_point: str, split_brain_threshold: int, keep_failed_worktree: bool, require_write_claim: bool = False, claim_agent: str | None = None, claim_project: str | None = None, claim_write_paths: list[str] | None = None, claims_dir: Path | None = None, require_clean_main_root: bool = False, claim_start_revision: str | None = None, allow_stale_start_point: bool = False) -> WorktreeCreationResult` · line 693: Create a worktree, inspect it immediately, and fail loud on unsafe state.
- `_recent_write_path_history` · `_recent_write_path_history(worktree_path: Path, write_paths: list[str], *, limit: int = 3) -> str | None` · line 896: One-line-per-commit recent history for each claimed write path, read at this worktree's own fresh HEAD -- so a diagnosis formed before the worktree existed doesn't go stale before the first edit.
- `_import_provenance_warning` · `_import_provenance_warning(worktree_path: Path) -> str | None` · line 921: Report, without blocking, when this worktree's packages resolve elsewhere.
- `_print_human` · `_print_human(result: WorktreeCreationResult) -> None` · line 951: Print a concise operator summary.
- `_canonical_lock_module_path` · `_canonical_lock_module_path(script_path: Path | None = None) -> Path` · line 983: Resolve the helper in both source and installed worktree layouts.
- `_lock_canonical_checkout` · `_lock_canonical_checkout(repo_root: Path, *, as_json: bool) -> None` · line 995: Make the canonical checkout read-only now that a lane exists.
- `main` · `main(argv: list[str] | None = None) -> int` · line 1045: CLI entry point for safe worktree creation.

### [`scripts/meta/worktree-coordination/finish_pr.py`](../scripts/meta/worktree-coordination/finish_pr.py)

Review and merge one exact PR head, then close its claimed lane.

**Symbols**

- `_framework_root` · `_framework_root() -> Path` · line 22: Resolve both source and installed ``scripts/meta`` layouts.
- `require_integration_authority` · `require_integration_authority() -> None` · line 77: Fail execution, but not CLI discovery, when the pinned package is stale.
- `_load_pr_auto` · `_load_pr_auto() -> ModuleType` · line 125: Load the existing isolated account-routing seam beside this helper.
- `github_repository_context` · `github_repository_context() -> Iterator[tuple[str, dict[str, str]]]` · line 140: Select the origin owner in a private gh config; never mutate shared auth.
- `load_trusted_review_spec` · `load_trusted_review_spec(path: Path, *, canonical_root: Path, worktree_roots: tuple[Path, ...] | None = None) -> PRReviewSpec` · line 231: Load coordinator input only when it is outside PR-controlled repository bytes.
- `load_trusted_review_bundle` · `load_trusted_review_bundle(path: Path, *, canonical_root: Path, worktree_roots: tuple[Path, ...] | None = None) -> TrustedReviewSpec` · line 251: Read and validate the trusted review spec exactly once.
- `resolve_branch_worktree` · `resolve_branch_worktree(branch: str) -> Path` · line 276: Resolve exactly one linked worktree checked out on the requested branch.
- `run_local_review_gate` · `run_local_review_gate(*, spec: PRReviewSpec, snapshot: PrSnapshot, review_worktree: Path, repo_slug: str, pr_number: int, gh_env: Mapping[str, str], output_root: Path) -> tuple[PRSignoffReceipt, Path]` · line 295: Run the potentially slow evidence-bound review outside hook execution.
- `base_branch_required_checks` · `base_branch_required_checks(pr_number: int, repo_slug: str, gh_env: Mapping[str, str]) -> tuple[list[str] | None, str]` · line 380: Return required check names on the PR base branch, or None when unknowable.
- `integration_target` · `integration_target(*, snapshot: PrSnapshot, repository: str, project: str, pr_number: int, branch: str, trusted_review: TrustedReviewSpec) -> IntegrationTargetV1` · line 481: Bind the reviewed revision and trusted spec to canonical claim custody.
- `prepare_post_merge_recovery` · `prepare_post_merge_recovery(*, snapshot: PrSnapshot, merge_commit: str | None, branch: str, pr_number: int, repo_slug: str, gh_env: Mapping[str, str], agent: str, project: str, repo_root: Path, review_spec_path: Path, review_output_root: Path) -> tuple[str, Path, IntegrationAuthorityAssertionV1]` · line 548: Re-prove exact review and claim custody after merge-before-close failure.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/worktree-coordination/integration_authority.py`](../scripts/meta/worktree-coordination/integration_authority.py)

Emit or validate one native-session, canonical-claim integration assertion.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/worktree-coordination/raise_concern.py`](../scripts/meta/worktree-coordination/raise_concern.py)

Route a concern to PR review when published, otherwise to the local inbox.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/worktree-coordination/safe_worktree_remove.py`](../scripts/meta/worktree-coordination/safe_worktree_remove.py)

Safely remove a git worktree, checking for uncommitted changes first.

**Symbols**

- `_find_framework_root` · `_find_framework_root() -> Path` · line 29: Find the repository root from either supported script layout.
- `run_cmd` · `run_cmd(cmd: list[str], cwd: str | None = None) -> tuple[bool, str]` · line 58: Run command and return (success, output).
- `find_provisioning_marker` · `find_provisioning_marker(worktree_path: str) -> Path | None` · line 74: Return the live creation marker for this exact target, if present.
- `has_uncommitted_changes` · `has_uncommitted_changes(worktree_path: str) -> tuple[bool, str]` · line 90: Check if worktree has uncommitted changes.
- `get_worktree_branch` · `get_worktree_branch(worktree_path: str) -> str | None` · line 110: Get the branch name of a worktree.
- `get_main_repo_root` · `get_main_repo_root() -> Path` · line 119: Get the main repo root (not worktree).
- `get_target_repo_root` · `get_target_repo_root(worktree_path: str) -> tuple[Path | None, str]` · line 138: Resolve the common Git repository for a registered target worktree.
- `make_tree_deletable` · `make_tree_deletable(path: Path) -> tuple[bool, list[tuple[Path, int]], str]` · line 151: Add owner write/search bits to directories so clean-tree removal can finish.
- `restore_tree_modes` · `restore_tree_modes(changed: list[tuple[Path, int]]) -> None` · line 168: Restore modes changed solely to prepare a failed worktree removal.
- `get_current_cc_identity` · `get_current_cc_identity() -> dict[str, Any]` · line 181: Get the current CC instance's identity.
- `check_worktree_claimed` · `check_worktree_claimed(worktree_path: str, claims_file: Path | None = None) -> tuple[bool, dict[str, Any] | None]` · line 200: Check if a worktree has an active claim.
- `check_session_marker_recent` · `check_session_marker_recent(worktree_path: str) -> tuple[bool, datetime | None]` · line 261: Check if session marker exists and is recent (< 24h old).
- `should_block_removal` · `should_block_removal(worktree_path: str, force: bool = False, claims_file: Path | None = None, my_identity: dict[str, Any] | None = None) -> tuple[bool, str, dict[str, Any] | None]` · line 300: Determine if worktree removal should be blocked.
- `remove_worktree` · `remove_worktree(worktree_path: str, force: bool = False) -> bool` · line 366: Remove a worktree safely.
- `_reconcile_canonical_lock` · `_reconcile_canonical_lock(worktree_path: str) -> None` · line 532: Release the canonical lock once the lane that justified it is gone.

_Coverage findings: python-docstring-missing._

### [`scripts/probe/render_review.py`](../scripts/probe/render_review.py)

Probe 0 temporary review projection.

_Coverage findings: python-docstring-missing._

### [`scripts/refresh_prewrite_claim_projection.py`](../scripts/refresh_prewrite_claim_projection.py)

Atomically refresh the derived pre-write authority projection.

_Coverage findings: python-docstring-missing._

### [`scripts/repo_stats_block.py`](../scripts/repo_stats_block.py)

Session-start repetition counters.

**Symbols**

- `_source_dirs` · `_source_dirs(root: Path) -> tuple[str, ...]` · line 27: Package roots to count, from `quality.reachability.packages`.
- `_net_lines` · `_net_lines(root: Path, count: int = 8) -> tuple[int, int, int]` · line 62: Added, deleted, and commit count over the last `count` commits.

_Coverage findings: python-docstring-missing._

### [`scripts/rules/agent_router.py`](../scripts/rules/agent_router.py)

AES profile and handoff accounting contracts consumed by native adapters.

**Symbols**

- `resolve_profile` · `resolve_profile(profile: AgentRouterProfileV1, capabilities: NativeCapabilities, *, registry_ids: set[str], mandatory_rule_ids: set[str], authority_limits: BudgetLimits, authorized_provider_routes: set[str], environment: Mapping[str, str]) -> EffectiveProfile` · line 93: Resolve configuration against trusted inputs supplied by the owning caller.
- `account_handoffs` · `account_handoffs(eligible_ids: Sequence[str], records: Sequence[HandoffRecordV1]) -> dict` · line 227: Report exact membership and outcome coverage separately from proposal validity.

_Coverage findings: python-docstring-missing._

### [`scripts/rules/build_rules_page.py`](../scripts/rules/build_rules_page.py)

Build docs/rules/RULES.md: every rule agents in Brian's workspace are expected to follow.

**Symbols**

- `_cell` · `_cell(text: Any, limit: int | None = None) -> str` · line 57: One Markdown table cell: single line, pipes escaped, optionally shortened at a word boundary.

_Coverage findings: python-docstring-missing._

### [`scripts/rules/sort_legacy.py`](../scripts/rules/sort_legacy.py)

Sort project-meta's legacy rules into covered / keep / retire, with checked quotes (agent-router slice 1).

**Symbols**

- `_resolve` · `_resolve(rel: str) -> Path` · line 71: A source path as the legacy register wrote it: absolute, ~, project-meta-relative or workspace-relative.
- `facts` · `facts(rule: dict) -> dict` · line 82: Plain file facts the model must not contradict.
- `check` · `check(answer: Disposition, rule: dict, f: dict, sources: dict[str, str]) -> str | None` · line 94: Return why the answer fails its evidence check, or None when it passes.
- `source_context` · `source_context(rule: dict, base: list[dict], instructions: str) -> tuple[dict, dict]` · line 141: Read all declared documents; a navigation page cannot mask a later source.
- `input_digest` · `input_digest(rule: dict, f: dict, sources: dict) -> str` · line 153: Bind caller-owned workflow inputs, independently of model call receipts.
- `retain` · `retain(rule: dict, row: dict, reason: str) -> Disposition` · line 269: Conservative fallback preserves authority, not a model's abbreviated rewrite.
- `reviewed_answer` · `reviewed_answer(rule: dict, row: dict, f: dict, sources: dict) -> tuple[Disposition, str | None]` · line 285: Recheck historical proposals against current inputs; never call a model.
- `apply` · `apply(cache_path: Path, *, check_only: bool = False) -> int` · line 325: Materialize or check an input-bound inventory; preserve raw attempts unchanged.

_Coverage findings: python-docstring-missing._

### [`scripts/sync_plan_status.py`](../scripts/sync_plan_status.py)

Sync and verify plan status across all locations.

**Symbols**

- `parse_plan_status` · `parse_plan_status(plan_path: Path) -> dict | None` · line 44: Parse status from a plan file.
- `_split_table_cells` · `_split_table_cells(line: str) -> list[str]` · line 94: Split a simple Markdown table row into trimmed cells.
- `_is_separator_row` · `_is_separator_row(line: str) -> bool` · line 99: Return true when a Markdown table row is only separator syntax.
- `_find_plan_index_table_rows` · `_find_plan_index_table_rows(content: str) -> tuple[list[str], dict[str, int]]` · line 107: Find the plan index table by header cells, not by surrounding heading.
- `parse_index_table` · `parse_index_table(index_path: Path) -> dict[int, dict]` · line 143: Parse the plan status table from index file.
- `collect_canonical_plan_statuses` · `collect_canonical_plan_statuses(index_statuses: dict[int, dict]) -> tuple[dict[int, dict], list[dict]]` · line 202: Select one canonical status source per plan number.
- `check_content_consistency` · `check_content_consistency() -> list[dict]` · line 246: Check that plan status matches content.
- `fix_content_status` · `fix_content_status() -> int` · line 285: Auto-fix status based on content.
- `check_consistency` · `check_consistency() -> list[dict]` · line 320: Check for inconsistencies between plan files and index.
- `sync_index_to_plans` · `sync_index_to_plans() -> int` · line 353: Update index table to match plan file statuses.
- `list_statuses` · `list_statuses() -> None` · line 430: List all plan statuses.

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/__init__.py`](../src/agentic_engineering_system/__init__.py)

Canonical Agentic Engineering System package.

### [`src/agentic_engineering_system/adopt.py`](../src/agentic_engineering_system/adopt.py)

`aes adopt`: bring an existing repository under AES without planning its old files (`RU-AES-ADOPT`).

**Symbols**

- `AdoptError` · `AdoptError` · line 53: Adoption refused, or the baseline file does not load.
- `load_baseline` · `load_baseline(root: Path) -> Baseline | None` · line 135: The baseline, or None when the repository was never adopted. A malformed file is an error.
- `adopt` · `adopt(root: Path, *, revision: str = 'HEAD', dry_run: bool = False, project_id: str | None = None, actor: str | None = None, outcome: str | None = None, governed_roots: Sequence[str] | None = None, language: str = 'python', now: datetime | None = None) -> AdoptResult` · line 175: Write the legacy baseline at `revision`; initialize the project first when it has no `.aes/`.
- `legacy_paths` · `legacy_paths(root: Path, target: TargetRecord | None = None) -> frozenset[str]` · line 237: Baseline paths the target does not plan; empty for a repository never adopted.
- `scope_released` · `scope_released(root: Path, baseline: Baseline | None = None) -> frozenset[str]` · line 249: Baseline files changed at HEAD that lie in a write surface of an adopted Company Planning plan in this repository's plan roots (`commit_rule.adopted_write_scopes`). HEAD, not the index: the commit being judged has not released the file it edits yet.
- `unplanned_legacy` · `unplanned_legacy(root: Path) -> frozenset[str]` · line 271: `legacy_paths` minus `scope_released`: the files whose edit still needs a plan's scope.
- `prune_baseline` · `prune_baseline(root: Path) -> tuple[str, ...]` · line 291: Drop entries the target now plans or Git no longer tracks; return them (sorted).
- `tracked_under` · `tracked_under(root: Path, roots: Sequence[str]) -> int` · line 308: How many tracked files the governed roots already hold (aes init warns when non-zero).

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/characterize.py`](../src/agentic_engineering_system/characterize.py)

Revision-bound characterization and target drift (`RU-AES-CHARACTERIZE`, `SC-GF-006`).

**Symbols**

- `CharacterizeError` · `CharacterizeError` · line 43: The repository could not be characterized.
- `_source_checkout_revision` · `_source_checkout_revision(module_file: Path) -> str | None` · line 79: `git describe --always --dirty` of the checkout that tracks `module_file`, else None.
- `running_version` · `running_version(module_file: Path | None = None) -> str` · line 107: The AES version of the code that is actually executing.
- `_read_blobs` · `_read_blobs(root: Path, shas: list[str]) -> dict[str, bytes]` · line 137: Blob contents by sha, through one `git cat-file --batch` call.
- `render_report` · `render_report(report: CharacterizeReport) -> str` · line 267: Text report; deterministic for one revision (no produced_at).

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/characterize_python.py`](../src/agentic_engineering_system/characterize_python.py)

Python AST characterization provider (`RU-AES-CHARACTERIZE`, `SC-GF-006`).

**Symbols**

- `module_name` · `module_name(path: str) -> str` · line 46: Dotted module name for a repository path ending in `.py`.
- `parse_export` · `parse_export(entry: str) -> tuple[str, str | None]` · line 62: Split a symbol commitment into (name, normalized signature or None).
- `_resolve` · `_resolve(dotted: str, modules: dict[str, str]) -> list[str]` · line 106: Governed paths executed by importing `dotted`: the module and its packages.
- `analyze` · `analyze(path: str, source: str, modules: dict[str, str]) -> PythonFacts` · line 154: Characterize one file. `modules` maps every governed module name to its path.
- `import_closure` · `import_closure(start: str, facts: dict[str, PythonFacts]) -> list[str]` · line 171: Every governed path reachable from `start` through import edges, `start` excluded.

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/cli.py`](../src/agentic_engineering_system/cli.py)

`aes` console entrypoint (probe 0).

**Symbols**

- `_VersionAction` · `_VersionAction` · line 69: Print the version of the running code: the installed distribution's version (Git-derived at build time), plus the running checkout's `git describe` when the code executes from a Git checkout (`characterize.running_version`).

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/commit_rule.py`](../src/agentic_engineering_system/commit_rule.py)

`aes commit check` / `aes commit replay`: the commit-tag rule (`RU-AES-COMMIT-RULE`, AP-REQ-001).

**Symbols**

- `_git_local_env_vars` · `_git_local_env_vars() -> tuple[str, ...]` · line 228: AES implementation extension: cache Git's documented hook-local names.
- `_foreign_git_env` · `_foreign_git_env() -> dict[str, str]` · line 235: Clear repository-local hook context for foreign Git calls, preserving auth.
- `repository_names` · `repository_names(root: Path) -> tuple[str, ...]` · line 247: What a conflict surface's `repository` may say to mean this repository, lower-cased: origin's `owner/repo` and `repo`, and the main checkout's folder name (a linked worktree's own folder name is not the repository's).
- `unit_scripts` · `unit_scripts(root: Path) -> frozenset[str]` · line 265: Tracked files that a systemd unit tracked in this repository runs: every token of an Exec* line that ends with a tracked file's path (units name scripts by absolute or %h paths).
- `skipped_by` · `skipped_by(root: Path, config: RuleConfig) -> Path | None` · line 333: The machine-wide skip root `root` lies under, if any.
- `_front_matter_plan_id` · `_front_matter_plan_id(meta: object) -> str | None` · line 384: A plan's id: `plan_id:`, or `id:` as Company Planning's `skeleton` writes it for a design plan (artifact_type: design_plan); found 2026-10-08 when a skeleton-built plan's own [Goal <id>] commit was reported as "no plan found".
- `plan_identity` · `plan_identity(text: bytes) -> str` · line 409: A plan's text without its progress fields: front-matter `status`/`owner`/`updated` keys, `Status:`/`Owner:` lines, progress sections (`PROGRESS_HEADING_RE`, up to the next heading of the same or a higher level) and blank lines. Two versions with the same identity are the same adopted plan (AES #673).
- `git_plan_history` · `git_plan_history(repo: Path, rel: str, rev: str = 'HEAD', index: bool = True)` · line 446: A lookup `want_sha256 -> bytes | None` over the versions of `rel` (relative to `repo`) in its last `PLAN_HISTORY_DEPTH` commits up to `rev`, plus the index when `index`; None whenever Git fails or no version has that sha256.
- `split_advisory` · `split_advisory(why: str) -> tuple[str, str]` · line 489: An adoption reason and its trailing progress advisory ("; ..." or "").
- `_adoption` · `_adoption(read, plan_rel: str, where: str, history = None) -> tuple[bool, str, dict]` · line 495: The adoption check over any byte source: `read(path relative to the plan root)` returns the file's bytes or None. `where` names the plan in messages. The third value is the plan's front matter (empty when the plan is missing). `history(want_sha256)` returns an earlier version of the plan with that sha256, or None (`git_plan_history`).
- `plan_adoption` · `plan_adoption(plan_root: Path, plan: Path) -> tuple[bool, str]` · line 534: Whether `plan` declares a Company Planning receipt whose adoption decision is `adopted` for the current bytes of both the plan and the receipt; the reason either way.
- `in_surface` · `in_surface(path: str, target: str) -> bool` · line 568: Whether `path` lies in a repository_path surface `target`: the same file, anything under that directory, or a glob match (`*` and `?` stay within one directory, `**` crosses them).
- `write_scope` · `write_scope(meta: dict, names: tuple[str, ...]) -> list[str]` · line 578: The plan's `conflict_surfaces` targets this repository may write: Company Planning's work-unit `conflictSurface` shape, `kind: repository_path`, `access: write | exclusive`, and a `repository` that names this repository. Other entries (read access, other kinds, other repositories, malformed ones) grant nothing.
- `adopted_write_scopes` · `adopted_write_scopes(plan_roots: tuple[Path, ...], names: tuple[str, ...]) -> list[str]` · line 595: Write surfaces for this repository of every adopted plan under `plan_roots` (`docs/plans/*.md`, `proposals/*/*.md`). Only plans whose front matter mentions `conflict_surfaces` are parsed and checked.
- `workspace_plan_roots` · `workspace_plan_roots(workspace: Path, plan_id: str, skip: tuple[Path, ...] = ()) -> list[Path]` · line 626: Repositories directly under `workspace` holding a plan whose front matter names `plan_id`.
- `fetch_all` · `fetch_all(workspace: Path, timeout: int = 60) -> list[str]` · line 672: `git fetch origin` in every repository directly under `workspace`, 16 at a time, so the plan index reads each default branch as GitHub has it (a plan merged there is not in a clone's origin/HEAD until a fetch). Never prompts for credentials. Returns one line per failure.
- `build_plan_index` · `build_plan_index(workspace: Path, path: Path | None = None) -> dict` · line 692: Which plan ids each repository directly under `workspace` holds on its default branch (read through git, not its working tree, which may sit on another branch). Incremental: a repository whose default-branch commit is unchanged keeps its previous entry, so only moved repositories are re-read (a full rebuild over ~/code takes about 20 s, a refresh a few).
- `_refresh_index_in_background` · `_refresh_index_in_background(workspace: Path) -> None` · line 745: Start an index rebuild that outlives this commit; the next commit reads its result. AES_PLAN_INDEX_REFRESH=0 turns this off (tests build the index explicitly).
- `indexed_adoption` · `indexed_adoption(workspace: Path, plan_id: str) -> tuple[list[tuple[bool, str, dict]], bool]` · line 771: Judge `plan_id` from each repository's default branch as recorded in the plan index. Returns the per-candidate verdicts and whether the index was missing or stale (and so a background refresh was started).
- `receipt_status` · `receipt_status(plan_roots: tuple[Path, ...], number: str | None, plan_id: str | None, plan_workspace: Path | None = None) -> tuple[bool, str]` · line 802: Whether the named plan has a current adopted Company Planning receipt, and why not.
- `staged_adoption` · `staged_adoption(root: Path, number: str | None, plan_id: str | None) -> tuple[bool, str, dict] | None` · line 812: The named plan as staged in the commit being made, judged from the index (with the working tree as fallback for files the commit does not touch): a plan adopted and committed together with its first work exists nowhere else yet. None when the commit stages no such plan.
- `adopted_plan` · `adopted_plan(plan_roots: tuple[Path, ...], number: str | None, plan_id: str | None, plan_workspace: Path | None = None, index_root: Path | None = None) -> tuple[bool, str, dict]` · line 842: `receipt_status`, plus the adopted plan's front matter (empty unless adopted).
- `_plan_text` · `_plan_text(config: RuleConfig, plan_id: str) -> tuple[Path, str, str] | None` · line 889: (repository, plan path relative to it, text) of the named plan: the plan roots and the workspace checkouts first, then each repository's default branch from the plan index.
- `quick_plan_notes` · `quick_plan_notes(plan_id: str, changes: list[FileChange], config: RuleConfig) -> list[str]` · line 912: For a plan made by Company Planning's quick-adopt (front matter `planning_path: requested`): whether the commit's changes stay inside the plan's file list (its Vertical and reset section, plus the plan's own folder and AES evidence records) and whether the plan's saved check output (`<plan folder>/<id>.check.txt`) is present. Notes only: they never change the verdict.
- `durable_plan_findings` · `durable_plan_findings(plan_id: str, config: RuleConfig) -> tuple[list[str], list[str]]` · line 960: (refusing findings, notes) from the durable-documents check for the named quick plan, run on the commit being made. Empty when the plan is not a quick plan in this repository or carries no command.
- `unreached_new_docs` · `unreached_new_docs(root: Path, added: list[str]) -> list[str]` · line 1006: The added reader documents that wiki/index.md does not reach within two links in the staged tree (the index), by the daily check's rules: instruction files, hidden folders, test fixtures, templates, generated output and `.md-file-cap.yaml` `unlinked_ok` paths are exempt.
- `_link_path` · `_link_path(cur: str, target: str, exists: Callable[[str], bool]) -> str` · line 1059: The repository path a Markdown link in page `cur` points at. A target starting with "/" is root-relative: the repository root when `exists` says that path is there, else the wiki folder (personal-wiki links "/people/a.md" from wiki/). Same rule as project-meta md_file_cap.
- `judge` · `judge(message: str, changes: list[FileChange], governed_roots: list[str], config: RuleConfig, legacy: frozenset[str] = frozenset()) -> Verdict` · line 1084: The tag's verdict (with the legacy-edit check), plus notes for a quick-adopt plan.
- `_judge_with_legacy` · `_judge_with_legacy(message: str, changes: list[FileChange], governed_roots: list[str], config: RuleConfig, legacy: frozenset[str] = frozenset()) -> Verdict` · line 1127: The tag's verdict, then the adopted repository's legacy-edit check (`adopt`). An `Asked:` line is recorded on the verdict either way and never changes it: being asked does not make large work trivial.
- `shaping_navigation_problems` · `shaping_navigation_problems(root: Path, plan_id: str, outside: list[FileChange]) -> list[str]` · line 1228: The staged changes outside proposals/<id>/ that are not navigation into it (#476, #531).
- `_legacy` · `_legacy(root: Path, *, released: bool = True) -> frozenset[str]` · line 1268: Legacy baseline paths the target does not plan, minus (with `released`) those an adopted plan's scope released (`adopt.unplanned_legacy`); empty outside an adopted AES project. The pre-commit hook has already refused a target that does not load, so a load error here is raised.
- `message_tag` · `message_tag(message_file: Path) -> str | None` · line 1290: The tag on the message's first line under TAG_RE, the one grammar for commit tags (#414), or None.
- `check_message` · `check_message(root: Path, message_file: Path | None, *, message_text: str | None = None, preflight: bool = False) -> tuple[int, str]` · line 1301: Judge the commit being made; return (exit status, report). Observe mode never refuses.
- `replay` · `replay(root: Path, revisions: str = 'HEAD', max_count: int = 300) -> tuple[list[tuple[str, str, Verdict]], dict[str, int]]` · line 1345: Judge past commits (non-merge, first-parent order) with today's rule and today's receipts. Legacy is today's baseline without the scope release: a file the replayed commits themselves changed is still judged against the plan each commit names.

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/context.py`](../src/agentic_engineering_system/context.py)

Bounded working-context compiler (probe 0): `aes context <subject>`.

**Symbols**

- `ContextError` · `ContextError` · line 59: The context could not be compiled; the message names the exact cause.
- `project_context` · `project_context(project_root: Path, subject: str) -> WorkingContext` · line 289: Load `.aes/project.yaml` + its target under `project_root` and compile the packet.

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/evidence.py`](../src/agentic_engineering_system/evidence.py)

Observations, freshness and criterion standing (`RU-AES-EVIDENCE`, `SC-GF-007`, `SC-GF-008`, decision D2).

**Symbols**

- `EvidenceError` · `EvidenceError` · line 87: Observations could not be loaded or checked against the target.
- `DependencyBasis` · `DependencyBasis` · line 103: Where `dependency_paths` came from: the subject's own file, what AES discovered from its intra-repository imports, and what the recorder declared.
- `NegativeControl` · `NegativeControl` · line 112: The observation is of a deliberately broken revision (a "break it on purpose" run).
- `DecisionCheck` · `DecisionCheck` · line 136: One output of the run, followed back to the source it was made from.
- `TraceReview` · `TraceReview` · line 145: What a `trace_review` observation must say: the run read end to end, not judged by its output.
- `_trace_review_problems` · `_trace_review_problems(obs: ObservationRecord, ers: dict[str, Any]) -> list[str]` · line 252: A trace_review assessment needs a TraceReview record, and SUPPORTS needs the whole trace read with no decision found wrong.
- `_target_entries_at` · `_target_entries_at(root: Path, revision: str, target_path: str) -> dict[str, str]` · line 313: Every id of the target at `revision` -> its entry, canonically serialized.
- `_reachable` · `_reachable(root: Path, commit: str) -> bool` · line 337: Whether `commit` is an ancestor of HEAD. A commit this clone lacks is not; any other git failure is an error.
- `_check_control` · `_check_control(root: Path, obs: ObservationRecord) -> str` · line 354: The revision a negative control's freshness is computed from, after checking its commits.
- `freshness` · `freshness(root: Path, obs: ObservationRecord, target_path: str = '.aes/target.yaml') -> tuple[Freshness, str]` · line 376: CURRENT, STALE, UNKNOWN or UNREACHABLE, with the reason; see the module docstring.
- `EvidenceReport.counts` · `counts(self) -> str` · line 438: `N current, N stale, N unknown, N unreachable; N superseded`: freshness over the observations that count, superseded ones apart.
- `_discover_dependencies` · `_discover_dependencies(root: Path, locator: str) -> list[str]` · line 541: Governed files a Python test's imports reach at HEAD, the test excluded.
- `branch_note` · `branch_note(root: Path, revision: str, consequence: str = 'this evidence stays valid') -> str | None` · line 574: A warning when `revision` is not yet on the default branch, a note when that cannot be checked, None when it is already there.
- `_aes_version` · `_aes_version() -> str` · line 603: The running AES code's version (`characterize.running_version`); fails if undeterminable.
- `record` · `record(root: Path, subject_id: str, depends_on: list[str], command: list[str] | None = None, downgrade_basis: str | None = None) -> Recorded` · line 613: Run one deterministic-test verification subject at HEAD and write its observation.

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/hooks.py`](../src/agentic_engineering_system/hooks.py)

`aes hooks install`: ship the consumer's pre-commit gate (`RU-AES-DISTRIBUTION`).

**Symbols**

- `HookInstallError` · `HookInstallError` · line 116: The hook was not installed; the message says why and what to do.
- `render_hook` · `render_hook() -> str` · line 120: The hook body: machine-independent, so the tracked file never churns.
- `render_commit_msg_hook` · `render_commit_msg_hook() -> str` · line 125: The commit-msg hook body; machine-independent like the pre-commit hook.
- `install_hooks` · `install_hooks(root: Path, interpreter: str | None = None) -> tuple[Path, str | None]` · line 146: Write `<root>/.githooks/pre-commit` and `commit-msg`, set `core.hooksPath` and `aes.installer`.

### [`src/agentic_engineering_system/planning.py`](../src/agentic_engineering_system/planning.py)

`aes plan prepare / validate / accept` (`RU-AES-PLANNING`, `SC-GF-004`).

**Symbols**

- `PlanError` · `PlanError` · line 93: A proposal was refused; `violations` lists every reason. Nothing was written.
- `FamilyEntries.entries` · `entries(self) -> list[tuple[str, str, Any]]` · line 116: (family, key, entry) for every entry, in family then file order.
- `FamilyKeys` · `FamilyKeys` · line 121: `remove:` - the keys (`id`, or `evidence_requirement_ref`) of entries to delete.
- `FamilyKeys.entries` · `entries(self) -> list[tuple[str, str]]` · line 132: (family, key) for every key, in family then file order.
- `TraceReviewDeclaration` · `TraceReviewDeclaration` · line 148: Whether the planned work runs a model, agent or pipeline, which every proposal must say.
- `AcceptedPlan` · `AcceptedPlan` · line 198: What `.aes/plans/<proposal_id>.yaml` holds: the proposal and where it was accepted.
- `_target_path` · `_target_path(root: Path) -> tuple[Path, list[str], Path]` · line 227: (target file, governed roots, plans directory) from `.aes/project.yaml`.
- `unrouted_requirements` · `unrouted_requirements(target: TargetRecord) -> list[str]` · line 234: Evidence requirements no verification subject names and no external boundary lists.
- `route_violations` · `route_violations(target: TargetRecord) -> list[str]` · line 241: One line per unrouted evidence requirement (SC-GF-004); used by `aes plan validate` on the resulting target and by `aes target validate` (the pre-commit hook) on the current one.
- `apply_delta` · `apply_delta(target: TargetRecord, delta: TargetDelta) -> tuple[TargetRecord, list[str]]` · line 252: Apply `delta` to a copy of `target`; return the result and every delta-level violation.
- `references` · `references(target: TargetRecord) -> list[tuple[str, str]]` · line 305: (referenced key, location) for every reference the target holds, in file order.
- `_removal_violations` · `_removal_violations(root: Path, current: TargetRecord, result: TargetRecord, delta: TargetDelta, governed: list[str]) -> tuple[list[str], set[str]]` · line 329: Dangling references to removed entries, and removed artifacts whose files are still indexed.
- `prepare` · `prepare(root: Path) -> dict[str, Any]` · line 383: The input packet a proposal is written against. Deterministic for one revision and tree.
- `require_adopted_plan` · `require_adopted_plan(root: Path) -> bool` · line 454: `.aes/planning.yaml` `require_adopted_plan` (default false, so a project without Company Planning still works; Brian's repositories turn it on one at a time).
- `_adoption_violations` · `_adoption_violations(root: Path, proposal: Proposal) -> list[str]` · line 466: AP-REQ-002: a named plan must be adopted for its current bytes; required when configured.
- `_trace_review_violations` · `_trace_review_violations(proposal: Proposal) -> list[str]` · line 479: Every proposal says whether its work runs a model, agent or pipeline; if it does, the delta carries a `trace_review` evidence requirement, so the run is judged by its trace, not its output.
- `validate_proposal` · `validate_proposal(root: Path, proposal: Proposal) -> ValidatedProposal` · line 499: Every violation at once as PlanError, or the resulting target.
- `_sequence_offset` · `_sequence_offset(text: str) -> int` · line 547: Indentation of the file's block-sequence dashes, so appended entries match.
- `_trailing_slot` · `_trailing_slot(node: Any) -> tuple[dict, Any, int] | None` · line 562: Where ruamel keeps the comment (blank lines included) that follows `node`.
- `_edit_target` · `_edit_target(target_text: str, proposal_doc: CommentedMap) -> tuple[str, list[str]]` · line 597: Apply the proposal's delta, as written, to the round-trip target document.

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/project.py`](../src/agentic_engineering_system/project.py)

`aes init` and project discovery (`RU-AES-PROJECT`, `SC-GF-001`).

**Symbols**

- `ProjectError` · `ProjectError` · line 61: No project was found or initialization was refused; nothing was written.
- `find_project_root` · `find_project_root(start: Path) -> Path` · line 73: The nearest directory at or above `start` that holds `.aes/project.yaml`.
- `initialize_project` · `initialize_project(root: Path, *, project_id: str, outcome: str, actor: str, governed_roots: Sequence[str] = ('src/', 'tests/'), architecture_line: str = ARCHITECTURE_LINE, language: str = 'python', _stage_hook: Callable[[Path], None] | None = None) -> InitResult` · line 166: Write `.aes/project.yaml` and `.aes/target.yaml` at the top of a Git work tree.

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/reconcile.py`](../src/agentic_engineering_system/reconcile.py)

Qualified current state and target/current gaps (`RU-AES-RECONCILE`, `SC-GF-007`, `SC-GF-008` at the gap level).

**Symbols**

- `MissingRequirement` · `MissingRequirement` · line 82: An evidence requirement without current support, and whether anything could supply it.
- `Gap.id` · `id(self) -> str` · line 120: `<kind>:<ref>`, the handle a plan proposal names in `closes_gaps`.
- `Reconciliation.open_gaps` · `open_gaps(self) -> list[Gap]` · line 161: Every open gap once, in report order (a criterion gap can appear under several components).
- `render_status` · `render_status(r: Reconciliation) -> str` · line 357: One screen: revision, counts, the first open gap per component.
- `render_report` · `render_report(r: Reconciliation) -> str` · line 372: Full report: every artifact, criterion, observation and gap.

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/records.py`](../src/agentic_engineering_system/records.py)

Strict typed records for `.aes/project.yaml` and `.aes/target.yaml` (probe 0).

**Symbols**

- `RecordLoadError` · `RecordLoadError` · line 28: The YAML file could not be read into the declared record shape.
- `TargetValidationError` · `TargetValidationError` · line 32: The target loaded structurally but violates a semantic invariant.
- `ExternalBoundary` · `ExternalBoundary` · line 126: An evidence requirement whose route is outside the repository (SC-GF-004).
- `TargetRecord.evidence_requirements` · `evidence_requirements(self) -> dict[str, tuple[SuccessCriterion, EvidenceRequirement]]` · line 150: ER id -> (owning criterion, ER). ERs are nested, so this is the only index.
- `TargetRecord.families` · `families(self) -> dict[str, dict[str, Any]]` · line 158: Family name -> {id: record} for every declared ID, ERs included.
- `_to_plain` · `_to_plain(value: Any) -> Any` · line 227: Convert ruamel round-trip containers/scalars into plain Python values.
- `load_yaml_mapping` · `load_yaml_mapping(path: Path) -> dict[str, Any]` · line 238: Load one YAML document as a mapping. Duplicate keys and non-mapping roots fail.
- `parse_yaml_mapping` · `parse_yaml_mapping(text: str, label: str) -> dict[str, Any]` · line 246: `load_yaml_mapping` for text that is not a file on disk (e.g. `git show REV:path`).
- `load_target` · `load_target(path: Path) -> TargetRecord` · line 273: Strict load + semantic validation. Raises RecordLoadError or TargetValidationError.
- `parse_target` · `parse_target(data: dict[str, Any], path: Path) -> TargetRecord` · line 279: `load_target` on an already-parsed mapping; `path` labels errors.
- `validate_target_refs` · `validate_target_refs(target: TargetRecord) -> list[str]` · line 293: Return every semantic violation as a human-readable line (empty = valid).

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/repository_context/__init__.py`](../src/agentic_engineering_system/repository_context/__init__.py)

Repository context resolution for one exact repository revision.

### [`src/agentic_engineering_system/repository_context/cli.py`](../src/agentic_engineering_system/repository_context/cli.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/repository_context/git_source.py`](../src/agentic_engineering_system/repository_context/git_source.py)

_No source-local artifact summary._

**Symbols**

- `GitSourceError` · `GitSourceError` · line 7: Raised when a local repository cannot provide required Git evidence.

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/repository_context/legacy.py`](../src/agentic_engineering_system/repository_context/legacy.py)

_No source-local artifact summary._

**Symbols**

- `LegacyRepositoryAdapter` · `LegacyRepositoryAdapter` · line 36: Resolve only explicit, bounded repository evidence; never infer authority from names.

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/repository_context/manifest.py`](../src/agentic_engineering_system/repository_context/manifest.py)

_No source-local artifact summary._

**Symbols**

- `ManifestError` · `ManifestError` · line 12: Raised when the authoritative pilot manifest is malformed.

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/repository_context/models.py`](../src/agentic_engineering_system/repository_context/models.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/repository_context/render_html.py`](../src/agentic_engineering_system/repository_context/render_html.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/repository_context/resolver.py`](../src/agentic_engineering_system/repository_context/resolver.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/topology.py`](../src/agentic_engineering_system/topology.py)

Governed-root topology check (`RU-AES-TOPOLOGY`, `SC-GF-003`).

**Symbols**

- `TopologyError` · `TopologyError` · line 33: The topology could not be computed (not a Git repository, bad root).
- `compare_topology` · `compare_topology(governed: tuple[str, ...], files: tuple[str, ...], target: TargetRecord, legacy: frozenset[str] = frozenset()) -> TopologyReport` · line 83: Orphans and unrealized artifacts for a given governed file list.

_Coverage findings: python-docstring-missing._

### [`src/agentic_engineering_system/trace_review.py`](../src/agentic_engineering_system/trace_review.py)

Thin AES binding to Company Planning's source-bound review provider.

**Symbols**

- `check_source_review` · `check_source_review(root: Path, observation: Any, criterion_id: str) -> ReviewCheck` · line 47: Validate retained reviews afresh, then bind them to native observation identity.

_Coverage findings: python-docstring-missing._

## Test (56)

### [`enforced_planning/test_relationships.py`](../enforced_planning/test_relationships.py)

Audit requirement-linked test semantics without treating test count as quality.

**Symbols**

- `TestRelationshipError` · `TestRelationshipError` · line 41: Report malformed test-audit configuration or relationship semantics.
- `TestCaseRecord` · `TestCaseRecord` · line 46: Represent one authored Python test function or class method.
- `RequirementRecord` · `RequirementRecord` · line 56: Represent one declared behavioral authority whose proof can be audited.
- `TestEdge` · `TestEdge` · line 65: Normalize one reviewed test-to-boundary relationship.
- `TestAuditFinding` · `TestAuditFinding` · line 81: Describe one report-only test-purpose, coverage, or evidence concern.
- `TestAuditReport` · `TestAuditReport` · line 92: Provide deterministic test inventory, linkage metrics, and findings.
- `TestAuditReport.to_dict` · `to_dict(self) -> dict[str, object]` · line 108: Return stable JSON-compatible fields.
- `TestAuditReport.to_json` · `to_json(self, *, pretty: bool = False) -> str` · line 113: Serialize without timestamps or workspace-specific paths.
- `TestAuditReport.to_markdown` · `to_markdown(self) -> str` · line 124: Render a compact human review surface from the same report data.
- `_strings` · `_strings(value: Any, *, field: str) -> tuple[str, ...]` · line 156: Normalize a scalar/list string field while rejecting ambiguous shapes.
- `_enum` · `_enum(value: Any, *, field: str, allowed: set[str]) -> str | None` · line 169: Normalize an optional enum and fail loudly on misspellings.
- `_selectors` · `_selectors(edge: dict[str, Any], primary: str, plural: str, alias: str) -> tuple[str, ...]` · line 182: Read one selector side using the V2 and compatibility field names.
- `_looks_like_test` · `_looks_like_test(selector: str) -> bool` · line 188: Identify the test side of an edge from its repository-relative selector.
- `parse_requirements` · `parse_requirements(data: dict[str, Any]) -> tuple[RequirementRecord, ...]` · line 196: Parse optional behavioral authorities without duplicating requirement prose.
- `parse_test_edges` · `parse_test_edges(data: dict[str, Any]) -> tuple[TestEdge, ...]` · line 223: Parse reviewed ``tests`` edges while preserving legacy incomplete edges.
- `inventory_tests` · `inventory_tests(inventory: InventoryReport, includes: tuple[str, ...]) -> tuple[TestCaseRecord, ...]` · line 278: Return every authored test function/method in the selected path scope.
- `_selector_matches` · `_selector_matches(selector: str, test: TestCaseRecord) -> bool` · line 298: Match file/glob or exact ``file::symbol`` selectors to an authored test.
- `_selector_in_scope` · `_selector_in_scope(selector: str, includes: tuple[str, ...]) -> bool` · line 307: Return whether a reviewed test selector belongs to the requested audit scope.
- `_finding` · `_finding(code: str, severity: str, subject: str, message: str, related: tuple[str, ...] = ()) -> TestAuditFinding` · line 314: Construct one stable finding with sorted related identifiers.
- `_edge_is_complete` · `_edge_is_complete(edge: TestEdge) -> bool` · line 322: Return whether an edge carries every policy-required test semantic.
- `_requirement_source_exists` · `_requirement_source_exists(repo_root: Path, requirement: RequirementRecord) -> bool` · line 335: Return whether a requirement's source authority resolves to a local file.
- `audit_test_relationships` · `audit_test_relationships(repo_root: Path, relationships: dict[str, Any], *, includes: tuple[str, ...] = ('tests/**/*.py', 'tests/*.py')) -> TestAuditReport` · line 344: Compile a deterministic report-only audit for one governed repository.
- `load_relationships` · `load_relationships(path: Path) -> dict[str, Any]` · line 559: Load one relationships mapping and reject missing or invalid roots.
- `audit_includes` · `audit_includes(data: dict[str, Any]) -> tuple[str, ...]` · line 570: Read the optional report-only audit scope from relationships config.
- `main` · `main(argv: list[str] | None = None) -> int` · line 585: Run the report-only test relationship audit CLI.

### [`proposals/harness-context/native-parity/test_verify_evidence.py`](../proposals/harness-context/native-parity/test_verify_evidence.py)

Negative controls for false certificates; all use saved evidence, no model calls.

_Coverage findings: python-docstring-missing._

### [`scripts/meta/test_relationships.py`](../scripts/meta/test_relationships.py)

CLI wrapper for report-only requirement-linked test auditing.

### [`tests/README.md`](../tests/README.md)

Status: no implementation verification yet.

### [`tests/capability_sourcing/verification.placeholder.yaml`](../tests/capability_sourcing/verification.placeholder.yaml)

_No source-local artifact summary._

### [`tests/conftest.py`](../tests/conftest.py)

Every test runs as on a clean machine: no machine-wide Git config, so no machine-wide hooks.

_Coverage findings: python-docstring-missing._

### [`tests/evidence_assessment/verification.placeholder.yaml`](../tests/evidence_assessment/verification.placeholder.yaml)

_No source-local artifact summary._

### [`tests/execution/verification.placeholder.yaml`](../tests/execution/verification.placeholder.yaml)

_No source-local artifact summary._

### [`tests/gap_reconciliation/verification.placeholder.yaml`](../tests/gap_reconciliation/verification.placeholder.yaml)

_No source-local artifact summary._

### [`tests/greenfield/test_adopt.py`](../tests/greenfield/test_adopt.py)

SC-ADOPT-001: adopting an existing repository, through the real CLI and the installed hooks.

**Symbols**

- `_adopted_plan` · `_adopted_plan(root: Path, plan_id: str = 'demo') -> None` · line 65: A Company Planning-shaped plan whose adoption decision is bound to its bytes.
- `existing` · `existing(tmp_path: Path) -> Path` · line 85: A clone of this repository with no .aes/: an existing codebase AES has never seen.
- `adopted` · `adopted(existing: Path) -> Path` · line 96: `existing` adopted, hooks installed after the adoption commit (the documented order).
- `test_adoption_commit_passes_installed_hooks` · `test_adoption_commit_passes_installed_hooks(existing: Path) -> None` · line 141: Issue #155: with hooks installed before the first commit, the adoption commit is not refused.
- `_numbered_plan` · `_numbered_plan(root: Path, number: int, surfaces: list[dict] | None, *, adopt_it: bool = True) -> Path` · line 263: `docs/plans/<N>_scoped.md`, Company Planning-shaped, with `conflict_surfaces` in its front matter (the work-unit schema 1.1 conflictSurface shape) and, when `adopt_it`, an adoption decision bound to its bytes.
- `test_plan_scope_admits_a_legacy_edit_inside_it_and_releases_the_file` · `test_plan_scope_admits_a_legacy_edit_inside_it_and_releases_the_file(adopted: Path) -> None` · line 291: #218 test 1: under enforce, a [Plan #N] commit editing a legacy file inside its adopted plan's conflict_surfaces lands, and the file then leaves the unplanned-legacy set.
- `test_plan_scope_refuses_a_legacy_edit_outside_it` · `test_plan_scope_refuses_a_legacy_edit_outside_it(adopted: Path) -> None` · line 327: #218 test 2: the same adopted plan editing a legacy file outside its scope is refused, naming only the file outside, and a mixed commit is refused as a whole.
- `test_unadopted_or_widened_plan_scope_admits_nothing` · `test_unadopted_or_widened_plan_scope_admits_nothing(adopted: Path) -> None` · line 349: #218 test 3: a plan that is not adopted is refused even though its front matter names the file; a plan whose scope was widened after adoption is refused until re-adopted.

_Coverage findings: python-docstring-missing._

### [`tests/greenfield/test_characterize.py`](../tests/greenfield/test_characterize.py)

`aes characterize`: revision-bound facts, Python AST extraction, symbol drift (SC-GF-006) and dependency discovery for recorded evidence.

**Symbols**

- `_checkout_with_module` · `_checkout_with_module(tmp_path: Path) -> tuple[Path, Path]` · line 289: A main checkout tracking pkg/mod.py and a linked worktree one commit ahead: the layout in which an editable install reports the main checkout's version.
- `test_running_version_is_the_install_alone_outside_a_tracking_checkout` · `test_running_version_is_the_install_alone_outside_a_tracking_checkout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None` · line 321: A venv's site-packages inside a consumer checkout is not tracked by it: the consumer's commit must not be reported as the AES code's.

_Coverage findings: python-docstring-missing._

### [`tests/greenfield/test_commit_rule.py`](../tests/greenfield/test_commit_rule.py)

SC-AP-001: the commit-tag rule, through the installed commit-msg hook on real commits.

**Symbols**

- `_adopted_plan` · `_adopted_plan(root: Path, plan_id: str = 'demo', front_matter: str = '', body: str = '') -> Path` · line 48: A plan with a Company Planning-shaped adoption decision bound to its bytes.
- `_committed_progress_plan` · `_committed_progress_plan(repo: Path, plan_id: str) -> Path` · line 132: An adopted plan with progress fields, committed so its adopted bytes are in history.
- `test_an_older_aes_without_the_rule_warns_and_does_not_block` · `test_an_older_aes_without_the_rule_warns_and_does_not_block(repo: Path, tmp_path: Path) -> None` · line 383: A main checkout on an older branch must not stop every commit in every worktree.
- `test_in_aes_itself_the_hooks_run_the_working_copy_code` · `test_in_aes_itself_the_hooks_run_the_working_copy_code() -> None` · line 400: Both hooks put `<root>/src` first when the repository is AES, so a worktree is checked by its own code, not by the branch the shared venv's editable install points at.
- `test_machine_config_reaches_repositories_without_their_own` · `test_machine_config_reaches_repositories_without_their_own(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None` · line 413: A plain repository takes the machine-wide mode; a per-repository entry overrides it; a repo file wins.
- `test_machine_skip_roots_exempt_throwaway_repositories_and_nothing_else` · `test_machine_skip_roots_exempt_throwaway_repositories_and_nothing_else(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None` · line 432: Issue #488: a repository under a machine-wide skip root commits untagged with a logged skip; one outside it is still refused; a repository's own file can neither name nor inherit a skip.
- `test_skip_root_at_or_above_home_is_ignored` · `test_skip_root_at_or_above_home_is_ignored(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None` · line 477: A too-broad skip root ('/', '~') must not switch the rule off for every repository (issue #488).
- `test_auto_tag_names_its_job_and_touches_no_running_thing` · `test_auto_tag_names_its_job_and_touches_no_running_thing() -> None` · line 491: [Auto] is for scheduled jobs: it must name the job and may not change anything that runs.
- `test_enforce_with_plan_adoption_observe_blocks_untagged_but_not_unadopted_plans` · `test_enforce_with_plan_adoption_observe_blocks_untagged_but_not_unadopted_plans(repo: Path) -> None` · line 502: Staged enforcement: tags and trivial size are refused; a plan that is not adopted is only logged.
- `test_goal_plan_owned_by_another_repository_resolves_through_the_workspace` · `test_goal_plan_owned_by_another_repository_resolves_through_the_workspace(repo: Path, tmp_path: Path) -> None` · line 515: Federated plans: the plan and its receipt live in the repository that owns them; a commit in another repository under the same workspace that names it is judged against it.
- `test_goal_plan_on_another_repositorys_main_resolves_when_its_checkout_is_elsewhere` · `test_goal_plan_on_another_repositorys_main_resolves_when_its_checkout_is_elsewhere(repo: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None` · line 536: The owner repository's checkout sits on a branch without the plan; its main has it. The working-tree scan cannot see it; the plan index, read from main through git, can.
- `test_foreign_plan_reads_preserve_repository_identity_under_hook_environment` · `test_foreign_plan_reads_preserve_repository_identity_under_hook_environment(repo: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None` · line 571: AES #483: Git's hook environment used PM objects for every foreign repo.
- `test_conflict_surface_matching_and_repository_names` · `test_conflict_surface_matching_and_repository_names(tmp_path: Path) -> None` · line 639: #218: the scope vocabulary is Company Planning's conflictSurface; only write/exclusive repository_path surfaces naming this repository grant edits.
- `test_asked_line_is_recorded_and_never_changes_the_verdict` · `test_asked_line_is_recorded_and_never_changes_the_verdict() -> None` · line 669: Asked: says who wanted the change, in their words; size and effect still decide the tag.
- `test_plan_index_does_not_cache_a_failed_search_as_no_plans` · `test_plan_index_does_not_cache_a_failed_search_as_no_plans(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None` · line 682: git grep exits 1 for 'no match' and 2+ for an error; an error must not be recorded as 'this repository holds no plans', or the plan stays invisible until the repository's main moves.
- `_last_log` · `_last_log(root: Path) -> dict` · line 721: The rule's own record of the commit just attempted (the hook writes one JSON line per verdict).
- `_quick_plan` · `_quick_plan(root: Path, plan_id: str, files: list[str]) -> None` · line 727: A plan shaped like Company Planning's quick-adopt output, with an adoption decision bound to its bytes.
- `test_quick_plan_commit_is_logged_for_its_check_output_and_file_list` · `test_quick_plan_commit_is_logged_for_its_check_output_and_file_list(repo: Path) -> None` · line 741: Plan commit-rule-followups: for a quick-adopt plan, the rule logs whether the commit adds the saved check output and stays inside the plan's file list. The notes never change the verdict.
- `_real_durable_check` · `_real_durable_check() -> Path | None` · line 788: Company Planning's durable_docs_check.py: $AES_DURABLE_DOCS_CHECK, or a company-planning checkout beside one of this checkout's parent folders.
- `_durable_repo` · `_durable_repo(repo: Path, script: Path, durable_line: str, mode: str = 'enforce') -> None` · line 797: A repository declaring durable_documents whose trace names src/whygame5/graph.py as RULE-A's owner, and an adopted quick plan carrying quick-adopt's durable-documents completion command.
- `test_durable_docs_check_refuses_unnamed_owner_and_accepts_named` · `test_durable_docs_check_refuses_unnamed_owner_and_accepts_named(repo: Path) -> None` · line 823: A [Goal] commit that edits a durable rule's owner file under a quick plan whose Durable documents line does not name the rule is refused (check durable-docs, PLAN-OWNER-UNNAMED); naming the rule and updating the trace in the same plan lets the same edit land. Runs Company Planning's real check.
- `_fake_durable_check` · `_fake_durable_check(tmp_path: Path, findings: str) -> Path` · line 866: A stand-in check script printing fixed findings (exit 1 when there are any), the real script's format.
- `test_durable_docs_check_observe_and_skips` · `test_durable_docs_check_observe_and_skips(repo: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None` · line 876: durable: observe only logs a refusal; an unchanged declared document is a note, not a refusal; a missing check script leaves a note and never refuses; a quick plan without the completion command gets no check.
- `test_trivial_may_not_touch_test_setup_or_a_script_a_systemd_unit_runs` · `test_trivial_may_not_touch_test_setup_or_a_script_a_systemd_unit_runs(repo: Path) -> None` · line 929: conftest.py changes every test run; a script named in a tracked unit's ExecStart runs on a schedule.
- `test_plan_names_with_capital_letters_are_read_as_plan_tags` · `test_plan_names_with_capital_letters_are_read_as_plan_tags(repo: Path) -> None` · line 952: #193: '[Goal PATH-brent-v1-2026-10-02]' was logged as 'no tag'. A plan id may contain capitals.
- `test_root_relative_links_resolve_against_the_repo_root_then_the_wiki_folder` · `test_root_relative_links_resolve_against_the_repo_root_then_the_wiki_folder(repo: Path) -> None` · line 991: 2026-10-13: a link starting with "/" was joined onto the linking page's folder, giving "/people/a.md", never a tracked path, so personal-wiki (links root-relative from wiki/) had 25 new pages refused that wiki/index.md links directly. "/x" now resolves at the repo root, else under wiki/.
- `test_a_shaping_commit_may_link_its_proposal_root_relatively` · `test_a_shaping_commit_may_link_its_proposal_root_relatively(repo: Path) -> None` · line 1011: 2026-10-13: a root-relative navigation link into proposals/<id>/ counts as navigation.
- `test_commit_tag_prints_the_rule_grammar_tag` · `test_commit_tag_prints_the_rule_grammar_tag(tmp_path: Path, first_line: str, tag: str | None, capsys: pytest.CaptureFixture[str]) -> None` · line 1148: #414: chained repository hooks ask `aes commit tag` instead of keeping their own grammar copy.
- `test_a_shaping_commit_may_carry_link_lines_into_its_own_proposal` · `test_a_shaping_commit_may_carry_link_lines_into_its_own_proposal(repo: Path) -> None` · line 1161: #476/#531: a new proposal and the wiki link that makes it reachable land in one [Shaping] commit; anything else outside proposals/<id>/ is still refused.
- `test_a_shaping_commit_may_create_the_first_wiki_index` · `test_a_shaping_commit_may_create_the_first_wiki_index(repo: Path) -> None` · line 1188: #531: in a repository with no wiki/index.md, the first index can land with the first proposal.
- `test_preflight_reports_the_hooks_verdict_without_logging` · `test_preflight_reports_the_hooks_verdict_without_logging(repo: Path) -> None` · line 1204: #532: `aes commit check --preflight -m` judges the staged change before a commit is attempted, exits 1 on a refusal in any mode, and writes nothing to the commit-rule log.

_Coverage findings: python-docstring-missing._

### [`tests/greenfield/test_context.py`](../tests/greenfield/test_context.py)

Probe 0: `aes context <subject>` on the real whygame5 target.

**Symbols**

- `project_root` · `project_root(tmp_path: Path) -> Path` · line 58: A git-initialised project root holding the real whygame5 .aes records.

_Coverage findings: python-docstring-missing._

### [`tests/greenfield/test_distribution.py`](../tests/greenfield/test_distribution.py)

Distribution and the packaged pre-commit hook (`RU-AES-DISTRIBUTION`).

**Symbols**

- `_consumer` · `_consumer(root: Path) -> Path` · line 71: The frozen whygame5 records plus its realized governed files, committed.
- `_assert_hook_gates_orphan` · `_assert_hook_gates_orphan(root: Path, env: dict[str, str] | None) -> None` · line 105: The installed hook refuses a staged orphan, then admits it once planned.
- `test_hook_refuses_a_criterion_with_no_route_and_admits_it_once_routed` · `test_hook_refuses_a_criterion_with_no_route_and_admits_it_once_routed(consumer: Path) -> None` · line 151: Phase 5 exit gate (SC-GF-004 at commit time): the hook's `aes target validate` rejects a target in which an evidence requirement has no route.
- `test_linked_worktree_falls_back_to_main_checkout_venv` · `test_linked_worktree_falls_back_to_main_checkout_venv(consumer: Path) -> None` · line 179: whygame5's kink: a linked worktree has no .venv; the hook must find the main one.
- `test_install_leaves_the_tracked_hook_clean_on_another_machine` · `test_install_leaves_the_tracked_hook_clean_on_another_machine(consumer: Path) -> None` · line 206: BRI-31: `.githooks/pre-commit` is tracked and shared, so the installing checkout's absolute interpreter path must not land in it — otherwise the documented install dirties the worktree and one `git add -A` publishes a path that exists on nobody else's machine.
- `test_hook_runs_without_the_installer_config` · `test_hook_runs_without_the_installer_config(consumer: Path) -> None` · line 227: A clone that never ran `aes hooks install` (or whose aes.installer is gone) falls through to the worktree venv instead of failing on an empty path.
- `test_version_names_the_install_and_the_running_checkout` · `test_version_names_the_install_and_the_running_checkout(capsys: pytest.CaptureFixture[str]) -> None` · line 299: Run from this checkout's src/ (pytest pythonpath), the version is the installed distribution's plus this checkout's describe, not the install alone (§13 kink).
- `test_getting_started_guide_runs_end_to_end_as_written` · `test_getting_started_guide_runs_end_to_end_as_written(tmp_path: Path) -> None` · line 352: Every ```bash block of docs/greenfield/GETTING_STARTED.md, in order, in a fresh folder, must succeed and end with the guide's criterion supported. The only substitution is the install pin: this checkout's HEAD instead of `<sha>` on GitHub. Machine-wide Git config and hooks are switched off, as a colleague's clean machine would have none. (2026-10-07: the guide's proposal stopped validating when plans began to require `trace_review`, and nothing ran the guide to notice.)

_Coverage findings: python-docstring-missing._

### [`tests/greenfield/test_evidence.py`](../tests/greenfield/test_evidence.py)

`aes evidence status` on the whygame5 target (SC-GF-007, SC-GF-008, D2).

**Symbols**

- `test_one_passing_input_of_three_stays_insufficient` · `test_one_passing_input_of_three_stays_insufficient(root: Path) -> None` · line 82: ER-SC-GF-007-01: a pass-like observation does not satisfy a multi-input criterion.
- `test_changed_dependency_stales_support` · `test_changed_dependency_stales_support(root: Path) -> None` · line 97: ER-SC-GF-008: changing what evidence depends on withdraws it until re-established.
- `_squash_merged_branch_commit` · `_squash_merged_branch_commit(root: Path) -> str` · line 166: A commit on a branch that is then squash-merged into main and deleted: the object stays in this clone's store, but no branch reaches it.
- `test_commit_this_clone_lacks_is_unreachable_with_the_same_text` · `test_commit_this_clone_lacks_is_unreachable_with_the_same_text(root: Path) -> None` · line 195: A fresh clone does not have the squashed branch's objects at all; it must agree.
- `test_cli_record_writes_an_observation` · `test_cli_record_writes_an_observation(with_test: Path, capsys: pytest.CaptureFixture[str]) -> None` · line 322: The first real use crashed: --command shared argparse dest 'command' with the subcommand, so every `aes evidence record` raised 'unhandled command None'.
- `test_discovered_dependencies_union_declared_ones` · `test_discovered_dependencies_union_declared_ones(with_test: Path) -> None` · line 334: --depends-on adds to what the test's imports reach; the basis keeps them apart.
- `_with_origin` · `_with_origin(root: Path) -> Path` · line 366: Give `root` a bare `origin` holding main, as a clone would have.

_Coverage findings: python-docstring-missing._

### [`tests/greenfield/test_evidence_controls.py`](../tests/greenfield/test_evidence_controls.py)

Entry-level target dependencies and negative-control observations (roadmap phase 6a).

**Symbols**

- `_mutated` · `_mutated(root: Path) -> tuple[str, str]` · line 186: A base commit on main and a scratch commit off it that breaks prompts.py, reachable only through a tag, as whygame5's drift observation is.
- `test_mutated_revision_without_control_is_unreachable` · `test_mutated_revision_without_control_is_unreachable(root: Path) -> None` · line 207: Without `control`, the tag-only mutated commit is judged on its own: it is not an ancestor of HEAD, so it never counts (it used to be STALE by construction).
- `test_reachability_applies_to_the_base_and_the_mutation_only_has_to_resolve` · `test_reachability_applies_to_the_base_and_the_mutation_only_has_to_resolve(root: Path) -> None` · line 274: The mutated commit is off-branch by design (a tag keeps it); the base is what must be reachable from HEAD. A base left on an unmerged side branch is UNREACHABLE.

_Coverage findings: python-docstring-missing._

### [`tests/greenfield/test_plan_receipt.py`](../tests/greenfield/test_plan_receipt.py)

SC-AP-002: `aes plan validate/accept` require a fresh Company Planning adoption when asked.

**Symbols**

- `_adopt` · `_adopt(root: Path) -> None` · line 48: A plan and a Company Planning-shaped adoption decision bound to its current bytes.
- `test_receipt_named_dot_receipt_json_finds_company_planning_decision` · `test_receipt_named_dot_receipt_json_finds_company_planning_decision(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None` · line 138: Company Planning names the decision for `x.receipt.json` `x.adoption-decision.json`.

_Coverage findings: python-docstring-missing._

### [`tests/greenfield/test_planning.py`](../tests/greenfield/test_planning.py)

`aes plan prepare / validate / accept` (RU-AES-PLANNING, SC-GF-004 ER-01).

**Symbols**

- `test_accept_on_a_freshly_initialized_target` · `test_accept_on_a_freshly_initialized_target(tmp_path: Path) -> None` · line 314: The getting-started path: `aes init` writes `[]` families; accepted entries become block lists.
- `test_accept_on_a_branch_warns_like_evidence_record` · `test_accept_on_a_branch_warns_like_evidence_record(root: Path, capsys: pytest.CaptureFixture[str]) -> None` · line 449: §20: a plan accepted on a branch that is then squash-merged names a commit the default branch never contains, so accept prints evidence record's warning.

_Coverage findings: python-docstring-missing._

### [`tests/greenfield/test_project.py`](../tests/greenfield/test_project.py)

`aes init` and project discovery (`RU-AES-PROJECT`, `SC-GF-001`).

**Symbols**

- `_snapshot` · `_snapshot(root: Path) -> dict[str, bytes]` · line 39: Every file and directory under root (outside .git), with file contents.

_Coverage findings: python-docstring-missing._

### [`tests/greenfield/test_reconcile.py`](../tests/greenfield/test_reconcile.py)

`aes reconcile` / `aes status`: qualified current state and derived gaps (RU-AES-RECONCILE; SC-GF-007 and SC-GF-008 at the gap level; SC-GF-004 "no route").

**Symbols**

- `test_requirement_with_external_boundary_is_routed` · `test_requirement_with_external_boundary_is_routed(root: Path) -> None` · line 191: An external boundary is a route, as `aes target validate` already accepts (SC-GF-004).
- `test_squash_merged_evidence_is_unreachable_and_a_superseded_record_is_counted_apart` · `test_squash_merged_evidence_is_unreachable_and_a_superseded_record_is_counted_apart(root: Path, capsys: pytest.CaptureFixture[str]) -> None` · line 292: §19: evidence recorded on a branch that was squash-merged and deleted stops counting in the clone that recorded it too; re-recording and marking the old record superseded restores support without deleting history.
- `test_plan_accepted_on_a_squash_merged_branch_is_an_unreachable_warning_not_a_failure` · `test_plan_accepted_on_a_squash_merged_branch_is_an_unreachable_warning_not_a_failure(root: Path, capsys: pytest.CaptureFixture[str]) -> None` · line 341: §20: whygame5's PLAN-WG5-RUNNER names a commit of a squash-merged branch. The target carries the delta either way, so the lost provenance commit warns only.

_Coverage findings: python-docstring-missing._

### [`tests/greenfield/test_records.py`](../tests/greenfield/test_records.py)

Probe 0: strict target/project loading against the real whygame5 records.

_Coverage findings: python-docstring-missing._

### [`tests/greenfield/test_self_governance.py`](../tests/greenfield/test_self_governance.py)

AES canonical governs itself (roadmap phase 6b, `SC-GF-003`, `SC-GF-004`).

_Coverage findings: python-docstring-missing._

### [`tests/greenfield/test_source_bound_trace_review.py`](../tests/greenfield/test_source_bound_trace_review.py)

Counterexamples cross the actual CP provider, not a fabricated passing receipt.

_Coverage findings: python-docstring-missing._

### [`tests/greenfield/test_topology.py`](../tests/greenfield/test_topology.py)

`aes topology check` on the real whygame5 target (`SC-GF-003`).

**Symbols**

- `project_root` · `project_root(tmp_path: Path) -> Path` · line 50: The real whygame5 .aes records plus its realized governed files, committed.

_Coverage findings: python-docstring-missing._

### [`tests/greenfield/test_trace_review.py`](../tests/greenfield/test_trace_review.py)

Plans require trace reviews (Brian, 2026-10-07).

**Symbols**

- `_with_trace_review_er` · `_with_trace_review_er(data: dict[str, Any]) -> dict[str, Any]` · line 32: The runner proposal declaring a real run and carrying a routed trace_review requirement.
- `_target_with_trace_review_er` · `_target_with_trace_review_er(tmp_path: Path)` · line 104: The frozen whygame5 target with its first evidence requirement turned into a trace review.

_Coverage findings: python-docstring-missing._

### [`tests/learning/test_feedback_collector_reuse.py`](../tests/learning/test_feedback_collector_reuse.py)

_No source-local artifact summary._

**Symbols**

- `test_a_deferred_report_reuses_its_last_clean_split` · `test_a_deferred_report_reuses_its_last_clean_split(tmp_path)` · line 13: A report the filing cap deferred keeps the records it was first split into: re-splitting with the light model can parse it differently, giving one record id two payloads (project-meta #2538).

_Coverage findings: python-docstring-missing._

### [`tests/learning/test_feedback_evidence_effects.py`](../tests/learning/test_feedback_evidence_effects.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`tests/learning/test_feedback_filing_gate.py`](../tests/learning/test_feedback_filing_gate.py)

Filing gate of the feedback collector: only closeout Learnings lines file, and a line already filed is not filed again (2026-10-07 spot check: 2 of 10 filed entries were exact repeats).

_Coverage findings: python-docstring-missing._

### [`tests/learning/test_feedback_records.py`](../tests/learning/test_feedback_records.py)

feedback-report.v1 parsing: the plan's canonical example and its negative controls (proposals/aes-learning-loop/PLAN.md, "Fixtures").

_Coverage findings: python-docstring-missing._

### [`tests/learning/test_feedback_transcripts.py`](../tests/learning/test_feedback_transcripts.py)

Synthetic-transcript tests for scripts/learning_loop/transcripts.py (no real transcript text here).

_Coverage findings: python-docstring-missing._

### [`tests/learning/test_fix_owner.py`](../tests/learning/test_fix_owner.py)

S6 weekly fix owner: an item counts as handled only from what GitHub shows, never the agent's summary.

_Coverage findings: python-docstring-missing._

### [`tests/learning/test_licences.py`](../tests/learning/test_licences.py)

S4: licence status comes from the Observation-to-Action evaluator (R-401), on the plan's fixtures.

_Coverage findings: python-docstring-missing._

### [`tests/learning/test_policies.py`](../tests/learning/test_policies.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`tests/learning/test_problems.py`](../tests/learning/test_problems.py)

S3 recurrence rule: independent observations with links; echoes of the same evidence count once.

_Coverage findings: python-docstring-missing._

### [`tests/learning/test_relation_check.py`](../tests/learning/test_relation_check.py)

S2 scoring rules: acceptable answers fixed with the labels, and the parity rule.

_Coverage findings: python-docstring-missing._

### [`tests/learning/test_subagents.py`](../tests/learning/test_subagents.py)

Native lifecycle capture and counterexamples to child self-rating as evidence.

_Coverage findings: python-docstring-missing._

### [`tests/learning/verification.placeholder.yaml`](../tests/learning/verification.placeholder.yaml)

_No source-local artifact summary._

### [`tests/normative_context/verification.placeholder.yaml`](../tests/normative_context/verification.placeholder.yaml)

_No source-local artifact summary._

### [`tests/planning/verification.placeholder.yaml`](../tests/planning/verification.placeholder.yaml)

_No source-local artifact summary._

### [`tests/policy_control/verification.placeholder.yaml`](../tests/policy_control/verification.placeholder.yaml)

_No source-local artifact summary._

### [`tests/repository_context/conftest.py`](../tests/repository_context/conftest.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`tests/repository_context/test_cli.py`](../tests/repository_context/test_cli.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`tests/repository_context/test_data_contracts_pinned.py`](../tests/repository_context/test_data_contracts_pinned.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`tests/repository_context/test_legacy_adapter.py`](../tests/repository_context/test_legacy_adapter.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`tests/repository_context/test_manifest_adapter.py`](../tests/repository_context/test_manifest_adapter.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`tests/repository_context/test_models.py`](../tests/repository_context/test_models.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`tests/repository_context/test_render_html.py`](../tests/repository_context/test_render_html.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`tests/repository_context/test_resolver.py`](../tests/repository_context/test_resolver.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`tests/rollout/test_daily_report.py`](../tests/rollout/test_daily_report.py)

The daily commit-rule report reads the rule's quick-plan notes (plan commit-rule-notes-report, AES #279).

_Coverage findings: python-docstring-missing._

### [`tests/rollout/test_install_everywhere.py`](../tests/rollout/test_install_everywhere.py)

The commit-rule installer reads a repository's commit-msg hook instead of trusting its config.

**Symbols**

- `home` · `home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path` · line 45: Point the installer's machine paths into tmp, with a stand-in rule that logs and refuses on REFUSE.
- `_real_aes` · `_real_aes(home: Path) -> Path` · line 133: An `aes` on PATH that is this checkout's CLI, so the wrapper asks the real commit-rule grammar.
- `test_tag_the_rule_recognises_passes_a_lagging_prefix_only_hook` · `test_tag_the_rule_recognises_passes_a_lagging_prefix_only_hook(home: Path) -> None` · line 148: #414: a valid [Goal <Upper-case id>] was refused by the chained copy of project-meta's prefix list.
- `test_without_aes_the_prefix_only_hook_still_decides` · `test_without_aes_the_prefix_only_hook_still_decides(home: Path) -> None` · line 161: A missing aes must not open the gate: the repository's own list is then the only judge.

_Coverage findings: python-docstring-missing._

### [`tests/test_agent_router.py`](../tests/test_agent_router.py)

Profiles cannot widen authority; failed proposals cannot leave the denominator.

_Coverage findings: python-docstring-missing._

### [`tests/test_agents_rendering.py`](../tests/test_agents_rendering.py)

_No source-local artifact summary._

_Coverage findings: python-docstring-missing._

### [`tests/test_docstring_wiki_links.py`](../tests/test_docstring_wiki_links.py)

The generated docstring wiki links every tracked artifact relative to its own location.

_Coverage findings: python-docstring-missing._

### [`tests/test_records_governed_roots.py`](../tests/test_records_governed_roots.py)

A governed root written without a trailing slash must not capture sibling paths.

_Coverage findings: python-docstring-missing._

### [`tests/test_rules_page.py`](../tests/test_rules_page.py)

The rules page lists every register rule and the legacy register, and survives table-breaking text.

_Coverage findings: python-docstring-missing._

### [`tests/test_sort_legacy.py`](../tests/test_sort_legacy.py)

The legacy sort's evidence check rejects answers its quote or the file facts do not support.

**Symbols**

- `_inventory` · `_inventory(tmp_path: Path)` · line 89: Use real files and the public apply/check boundary; never call a provider.

_Coverage findings: python-docstring-missing._

## Documentation (291)

### [`.agentic/events/README.md`](../.agentic/events/README.md)

Status: bootstrap.

### [`.project-brain/now.md`](../.project-brain/now.md)

canonical Enforced Planning's [successor-tracker repair](https://github.com/BrianMills2718/enforced-planning/commit/9baad04). It preserves a closed lane's tracker and allocates a bounded path for a distinct lane under the unchanged session goal; active and conflicting identities remain occupied or refused. Owner lifecycle regressions pass; installed native lifecycle evidence and closure are tracked in [#437](https://github.com/BrianMills2718/agentic-engineering-system-canonical/issues/437).

### [`.project-brain/project.md`](../.project-brain/project.md)

Layout and status words: agent-skills `contracts/client-config/agents/project-brain.md`. Each claim is `working` (understood, not agreed), `approved` (current source of truth) or `needs_resolution`.

### [`.project-brain/state.md`](../.project-brain/state.md)

Detail and evidence: personal-vps `proposals/hive-brain-v1/ROADMAP.md` ("Where we are", "Capabilities") and personal-vps `proposals/hive-brain-v1/PROGRESS_LOG.md`. This page is the short version.

### [`.project-brain/truth.md`](../.project-brain/truth.md)

Full table with reasons: personal-vps `proposals/hive-brain-v1/ROADMAP.md` "Decisions and assumptions" and `proposals/aes-learning-loop/DESIGN.md`. Rejected alternatives, which are the point of this page:

### [`AGENTS.md`](../AGENTS.md)

Start with `wiki/index.md`.

### [`CLAUDE.md`](../CLAUDE.md)

Start with `wiki/index.md`.

### [`README.md`](../README.md)

**This repository is the Agentic Engineering System** ([Decision 0011](docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md), 2026-09-26). `Inside-Success/agentic-engineering-system` is archived; the ideas worth borrowing from it are in [`research/synthesis/2026-09-26-inside-success-aes-harvest.md`](research/synthesis/2026-09-26-inside-success-aes-harvest.md), each with the consumer trigger that would bring it in. Next frontier: whygame5 realizes its runner and records the first value measure (Decision 0011, item 5).

### [`datasets/README.md`](../datasets/README.md)

Status: unused Role: durable project-owned data assets Authority: dataset bytes/metadata at identified version Lifecycle: versioned/immutable per dataset contract

### [`datasets/learning-loop/README.md`](../datasets/learning-loop/README.md)

Design: `proposals/aes-learning-loop/DESIGN.md`.

### [`datasets/learning-loop/experiments/2026-10-02-question-design/README.md`](../datasets/learning-loop/experiments/2026-10-02-question-design/README.md)

How should Jev (typesafe/jev-1.13) be asked to sort a learning into the failure families of `docs/failure-modes.md`? Lesson and discussion: issue #64.

### [`datasets/learning-loop/experiments/2026-10-07-filing-gate/README.md`](../datasets/learning-loop/experiments/2026-10-07-filing-gate/README.md)

Scripts behind the feedback collector's filing gates (AES #181, #216, #220). Each reads learnings entries by id from project-meta (a private repository) at run time; the scripts themselves contain no transcript text, only entry ids and hand labels.

### [`deployment/README.md`](../deployment/README.md)

Status: unused Role: deployment/release/target-environment concern Authority: deployment config/procedure within scope Lifecycle: versioned config plus retained deployment evidence

### [`docs/architecture/GOAL.md`](../docs/architecture/GOAL.md)

What the Agentic Engineering System is for, the bet behind it, what would disprove it, and the repository it replaces

### [`docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md`](../docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md)

Status: accepted AES delivery constraint.

### [`docs/architecture/INITIAL_GAP_LEDGER.md`](../docs/architecture/INITIAL_GAP_LEDGER.md)

Status: **recomputed for Plan 001 closure from verified AES revision `96fcf5e89ba98ad9ff278ec536a98c308cda3fe1` and follow-up A1 utility evidence on 2026-09-22**.

### [`docs/architecture/README.md`](../docs/architecture/README.md)

This directory contains AES-specific normative and delivery architecture for the canonical convergence project. Project-agnostic methodology remains owned by `BrianMills2718/wiki_methodology` at the revision declared in `.agentic/repo.yaml`; generic planning-method improvements should be proposed to Company Planning rather than silently duplicated here.

### [`docs/architecture/SYSTEM_BOUNDARY.md`](../docs/architecture/SYSTEM_BOUNDARY.md)

Status: accepted bootstrap target.

### [`docs/architecture/aes-company-planning-profile.bootstrap.yaml`](../docs/architecture/aes-company-planning-profile.bootstrap.yaml)

_No source-local artifact summary._

### [`docs/architecture/architecture-realization.bootstrap.yaml`](../docs/architecture/architecture-realization.bootstrap.yaml)

_No source-local artifact summary._

### [`docs/architecture/greenfield-v0.2/02-semantic-model.yaml`](../docs/architecture/greenfield-v0.2/02-semantic-model.yaml)

_No source-local artifact summary._

### [`docs/architecture/greenfield-v0.2/03-lifecycle.yaml`](../docs/architecture/greenfield-v0.2/03-lifecycle.yaml)

_No source-local artifact summary._

### [`docs/architecture/greenfield-v0.2/04-greenfield-mvp.yaml`](../docs/architecture/greenfield-v0.2/04-greenfield-mvp.yaml)

_No source-local artifact summary._

### [`docs/architecture/greenfield-v0.2/12-greenfield-mvp-semantic-instance.yaml`](../docs/architecture/greenfield-v0.2/12-greenfield-mvp-semantic-instance.yaml)

_No source-local artifact summary._

### [`docs/architecture/greenfield-v0.2/13-greenfield-materialization.md`](../docs/architecture/greenfield-v0.2/13-greenfield-materialization.md)

Choose the smallest opinionated project storage convention that can materialize the clean semantic model for a fresh project without making storage layout part of the ontology.

### [`docs/architecture/greenfield-v0.2/14-initialization-contract.yaml`](../docs/architecture/greenfield-v0.2/14-initialization-contract.yaml)

_No source-local artifact summary._

### [`docs/architecture/greenfield-v0.2/15-planning-contract.yaml`](../docs/architecture/greenfield-v0.2/15-planning-contract.yaml)

_No source-local artifact summary._

### [`docs/architecture/greenfield-v0.2/16-record-shapes.yaml`](../docs/architecture/greenfield-v0.2/16-record-shapes.yaml)

_No source-local artifact summary._

### [`docs/architecture/greenfield-v0.2/20-realization-topology.yaml`](../docs/architecture/greenfield-v0.2/20-realization-topology.yaml)

_No source-local artifact summary._

### [`docs/architecture/greenfield-v0.2/23-greenfield-cli-product-contract.md`](../docs/architecture/greenfield-v0.2/23-greenfield-cli-product-contract.md)

Status: **accepted** by [Decision 0010](../../decisions/0010-greenfield-v0.2-accepted.md) (2026-09-25). Plain copy of `proposals/aes-v0.2-greenfield/23-greenfield-cli-product-contract.md` (copied, not `git mv`'d, so the proposal lineage stays in place). For AES canonical, `.aes/target.yaml` is the live authority: where this file and the target disagree, this file is wrong. "Accepted amendments" at the end lists what changed from the candidate. File names that are not in this directory refer to `proposals/aes-v0.2-greenfield/`. Date: 2026-09-24

### [`docs/architecture/greenfield-v0.2/README.md`](../docs/architecture/greenfield-v0.2/README.md)

Status: **accepted** by [Decision 0010](../../decisions/0010-greenfield-v0.2-accepted.md) (2026-09-25).

### [`docs/architecture/normative-component-alignment.bootstrap.yaml`](../docs/architecture/normative-component-alignment.bootstrap.yaml)

_No source-local artifact summary._

### [`docs/architecture/normative-record-model.bootstrap.yaml`](../docs/architecture/normative-record-model.bootstrap.yaml)

_No source-local artifact summary._

### [`docs/architecture/schemas/architecture-realization.bootstrap.schema.json`](../docs/architecture/schemas/architecture-realization.bootstrap.schema.json)

_No source-local artifact summary._

### [`docs/decisions/0001-canonical-convergence-boundary.md`](../docs/decisions/0001-canonical-convergence-boundary.md)

Why AES was restarted as a clean canonical repository and what it converges from

### [`docs/decisions/0002-company-planning-aes-profile-before-fork.md`](../docs/decisions/0002-company-planning-aes-profile-before-fork.md)

Use a Company Planning profile inside AES before changing or forking Company Planning

### [`docs/decisions/0003-component-local-normative-context-and-symbol-inheritance.md`](../docs/decisions/0003-component-local-normative-context-and-symbol-inheritance.md)

Normative context lives beside each component and symbols inherit their component's scope

### [`docs/decisions/0004-compact-structured-normative-records-and-generated-views.md`](../docs/decisions/0004-compact-structured-normative-records-and-generated-views.md)

Normative records are compact structured data with generated conventional views

### [`docs/decisions/0005-aes-component-scope-and-consequential-seam-typing.md`](../docs/decisions/0005-aes-component-scope-and-consequential-seam-typing.md)

An AES component is a governance scope and only consequential seams are typed early

### [`docs/decisions/0006-minimal-architecture-realization-json-schema.md`](../docs/decisions/0006-minimal-architecture-realization-json-schema.md)

Freeze the minimal architecture-realization contract on JSON Schema 2020-12

### [`docs/decisions/0007-provider-independent-verification-and-blob-evidence-carry-forward.md`](../docs/decisions/0007-provider-independent-verification-and-blob-evidence-carry-forward.md)

Superseded first version of provider-independent verification with blob-level evidence carry-forward

### [`docs/decisions/0008-provider-independent-verification-with-transitive-subjects.md`](../docs/decisions/0008-provider-independent-verification-with-transitive-subjects.md)

Verification is provider-independent and evidence is reused only while its executed subjects are unchanged

### [`docs/decisions/0009-modular-product-design-without-parallel-aca-platform.md`](../docs/decisions/0009-modular-product-design-without-parallel-aca-platform.md)

Apply modular product design through AES instead of building a parallel platform

### [`docs/decisions/0010-greenfield-v0.2-accepted.md`](../docs/decisions/0010-greenfield-v0.2-accepted.md)

The AES v0.2 greenfield MVP was accepted as realized and replaces the v0.1 line as current

### [`docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md`](../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md)

This repository is the Agentic Engineering System and the Inside Success repository is archived

### [`docs/decisions/0012-capability-reuse-enforced-at-plan-adoption.md`](../docs/decisions/0012-capability-reuse-enforced-at-plan-adoption.md)

Capability reuse is enforced at plan adoption against one shared catalogue

### [`docs/decisions/0013-truth-lives-where-it-is-edited.md`](../docs/decisions/0013-truth-lives-where-it-is-edited.md)

Truth lives where it is edited, so documents are generated or checked from their owning source

### [`docs/failure-modes.md`](../docs/failure-modes.md)

The audit instrument for `review` and `audit`. Twenty-two families, each with a **detecting question** — ask it of the artifact, then ask it of your own findings.

### [`docs/greenfield/GETTING_STARTED.md`](../docs/greenfield/GETTING_STARTED.md)

AES keeps a project's accepted target in `.aes/target.yaml`: what the project is for (outcomes), the rules it must obey (normative items), how you would know it works (success criteria and their evidence requirements), which files are supposed to exist (planned artifacts) and which checks prove the criteria (verification subjects). The `aes` command checks that the target is consistent, that every file under the governed directories is planned, and which criteria current evidence supports.

### [`docs/model/ODD.md`](../docs/model/ODD.md)

AES canonical's system model in prose -- the commit, plan, target, evidence and reconcile loop -- with its checked trace file

### [`docs/model/trace.yaml`](../docs/model/trace.yaml)

_No source-local artifact summary._

### [`docs/plans/001_D1_contract_surface_topology_freeze.md`](../docs/plans/001_D1_contract_surface_topology_freeze.md)

Close only the remaining design decisions that prevent Slice 1 from starting without hidden architectural choices:

### [`docs/plans/001_repository_context_resolution_vertical.md`](../docs/plans/001_repository_context_resolution_vertical.md)

Status: **DELIVERED for bounded Slice 1 at verified AES revision `96fcf5e89ba98ad9ff278ec536a98c308cda3fe1`; final technical verification and follow-up A1 = `continue` recorded 2026-09-22** Origin gaps: GAP-AES-001, 002, 003, 004, 005, 006, 007, 009, 010, 011, 013, 014, 015, 017, 019, 020, 021, 022, 023, 024, 025, 026, 027 External consumer: `BrianMills2718/data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0` Execution profile: pilot

### [`docs/plans/002_offline_policy_decision_replay.md`](../docs/plans/002_offline_policy_decision_replay.md)

**Current:** Plan 001 proved one bounded AES lifecycle, including exact verification, direct human utility, and gap reconciliation. The fresh gap state still marks broader policy/evidence maturation as incomplete. AES already has deterministic completion/verification controls through Enforced Planning, but there is no accepted evidence that a contextual model improves judgment on real AES policy decisions, and no current live model-evaluator integration is authorized.

### [`docs/plans/1_repository_context_resolution_work_graph.json`](../docs/plans/1_repository_context_resolution_work_graph.json)

_No source-local artifact summary._

### [`docs/plans/CLAUDE.md`](../docs/plans/CLAUDE.md)

Track all implementation work here.

### [`docs/plans/README.md`](../docs/plans/README.md)

Status: Plan 001 / Repository Context is **DELIVERED** for its bounded Slice 1 claim. Plan 002 / Offline Policy-Decision Replay is now the active planned vertical; no live policy behavior has changed.

### [`docs/plans/TEMPLATE.md`](../docs/plans/TEMPLATE.md)

**Current:** What exists now

### [`docs/plans/adoption-progress-fields.adoption-attempts.jsonl`](../docs/plans/adoption-progress-fields.adoption-attempts.jsonl)

_No source-local artifact summary._

### [`docs/plans/adoption-progress-fields.adoption-decision.json`](../docs/plans/adoption-progress-fields.adoption-decision.json)

_No source-local artifact summary._

### [`docs/plans/adoption-progress-fields.bundle.json`](../docs/plans/adoption-progress-fields.bundle.json)

_No source-local artifact summary._

### [`docs/plans/adoption-progress-fields.check.txt`](../docs/plans/adoption-progress-fields.check.txt)

_No source-local artifact summary._

### [`docs/plans/adoption-progress-fields.facts.json`](../docs/plans/adoption-progress-fields.facts.json)

_No source-local artifact summary._

### [`docs/plans/adoption-progress-fields.goal.md`](../docs/plans/adoption-progress-fields.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `docs/plans/adoption-progress-fields.md` (plan sha256 789a049bca54aec1f3c7a069fdb4430fe7866db213cdc74ef5d1c8c065ffcfab, route inline_prototype). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`docs/plans/adoption-progress-fields.md`](../docs/plans/adoption-progress-fields.md)

This procedure is separate from the anticipated failure named in the disproof under Success and disproof: it applies to any run that fails or surprises us. Preserve the failed run itself: keep its complete output (command, every line, exit status) and its execution trace id, never overwritten by a rerun. Before selecting a fix, read the complete inputs, prompts, tool arguments/results, intermediate stages and final output, including the full check command/output and the changed files. Cite the observed divergence and classify evidence absent, returned but unused or contradicted, invalid expectation, or unresolved. An unresolved diagnosis cannot authorize a causal repair; it permits only further investigation. Bind the targeted repair to a new traced verification run; retain the failed original. Review every failing or surprising item and a sample of passes. A complete review is distinct from a passing run. Criterion `outcome` covers the entire requested success check.

### [`docs/plans/adoption-progress-fields.path-decision.json`](../docs/plans/adoption-progress-fields.path-decision.json)

_No source-local artifact summary._

### [`docs/plans/adoption-progress-fields.receipt.json`](../docs/plans/adoption-progress-fields.receipt.json)

_No source-local artifact summary._

### [`docs/plans/adoption-progress-fields.verdicts.json`](../docs/plans/adoption-progress-fields.verdicts.json)

_No source-local artifact summary._

### [`docs/plans/capability-catalogue.adoption-attempts.jsonl`](../docs/plans/capability-catalogue.adoption-attempts.jsonl)

_No source-local artifact summary._

### [`docs/plans/capability-catalogue.adoption-decision.json`](../docs/plans/capability-catalogue.adoption-decision.json)

_No source-local artifact summary._

### [`docs/plans/capability-catalogue.bundle.json`](../docs/plans/capability-catalogue.bundle.json)

_No source-local artifact summary._

### [`docs/plans/capability-catalogue.facts.json`](../docs/plans/capability-catalogue.facts.json)

_No source-local artifact summary._

### [`docs/plans/capability-catalogue.goal.md`](../docs/plans/capability-catalogue.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `docs/plans/capability-catalogue.md` (plan sha256 5ee99c45221bcab843da60c44790b174b4bfad208745a5b1c88fda5eac1f39cb, route coordinated). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`docs/plans/capability-catalogue.md`](../docs/plans/capability-catalogue.md)

Each section below answers the checklist items quoted in it; the gate judges only that section's text.

### [`docs/plans/capability-catalogue.path-decision.json`](../docs/plans/capability-catalogue.path-decision.json)

_No source-local artifact summary._

### [`docs/plans/capability-catalogue.receipt.json`](../docs/plans/capability-catalogue.receipt.json)

_No source-local artifact summary._

### [`docs/plans/capability-catalogue.verdicts.json`](../docs/plans/capability-catalogue.verdicts.json)

_No source-local artifact summary._

### [`docs/plans/commit-rule-emergency-gaps.adoption-attempts.jsonl`](../docs/plans/commit-rule-emergency-gaps.adoption-attempts.jsonl)

_No source-local artifact summary._

### [`docs/plans/commit-rule-emergency-gaps.adoption-decision.json`](../docs/plans/commit-rule-emergency-gaps.adoption-decision.json)

_No source-local artifact summary._

### [`docs/plans/commit-rule-emergency-gaps.bundle.json`](../docs/plans/commit-rule-emergency-gaps.bundle.json)

_No source-local artifact summary._

### [`docs/plans/commit-rule-emergency-gaps.check.txt`](../docs/plans/commit-rule-emergency-gaps.check.txt)

_No source-local artifact summary._

### [`docs/plans/commit-rule-emergency-gaps.facts.json`](../docs/plans/commit-rule-emergency-gaps.facts.json)

_No source-local artifact summary._

### [`docs/plans/commit-rule-emergency-gaps.md`](../docs/plans/commit-rule-emergency-gaps.md)

This procedure is separate from, and distinct from, the anticipated failure modes listed under Disproof: it covers any failing or surprising run, including ones nobody anticipated. Preserve the failed run itself (its full output saved next to the plan) and its trace id or command line. Before selecting a fix, read the complete inputs, prompts, each tool call's arguments and results, intermediate stages and final output, including the full check command and output and the changed files. Cite the observed divergence and classify it as evidence absent, evidence returned but unused or contradicted, invalid expectation, or unresolved. An unresolved diagnosis permits further investigation but cannot authorize a causal repair. Link the targeted repair to a new traced verification run, and retain the original failed run. Review every failing or surprising item and a sample of passes. Review completeness is judged separately from the run verdict: a passing run does not show the review was complete. Criterion `outcome` covers the entire requested success check.

### [`docs/plans/commit-rule-emergency-gaps.path-decision.json`](../docs/plans/commit-rule-emergency-gaps.path-decision.json)

_No source-local artifact summary._

### [`docs/plans/commit-rule-emergency-gaps.receipt.json`](../docs/plans/commit-rule-emergency-gaps.receipt.json)

_No source-local artifact summary._

### [`docs/plans/commit-rule-emergency-gaps.verdicts.json`](../docs/plans/commit-rule-emergency-gaps.verdicts.json)

_No source-local artifact summary._

### [`docs/plans/commit-rule-root-relative-links.adoption-attempts.jsonl`](../docs/plans/commit-rule-root-relative-links.adoption-attempts.jsonl)

_No source-local artifact summary._

### [`docs/plans/commit-rule-root-relative-links.adoption-decision.json`](../docs/plans/commit-rule-root-relative-links.adoption-decision.json)

_No source-local artifact summary._

### [`docs/plans/commit-rule-root-relative-links.bundle.json`](../docs/plans/commit-rule-root-relative-links.bundle.json)

_No source-local artifact summary._

### [`docs/plans/commit-rule-root-relative-links.check.txt`](../docs/plans/commit-rule-root-relative-links.check.txt)

_No source-local artifact summary._

### [`docs/plans/commit-rule-root-relative-links.facts.json`](../docs/plans/commit-rule-root-relative-links.facts.json)

_No source-local artifact summary._

### [`docs/plans/commit-rule-root-relative-links.goal.md`](../docs/plans/commit-rule-root-relative-links.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `docs/plans/commit-rule-root-relative-links.md` (plan sha256 9e900e9effb26ce852948c9a9de843b7e616a6bc85615d26413048c02d784cd7, route inline_prototype). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`docs/plans/commit-rule-root-relative-links.md`](../docs/plans/commit-rule-root-relative-links.md)

This procedure is separate from the anticipated failure named in the disproof under Success and disproof: it applies to any run that fails or surprises us. Preserve the failed run itself: keep its complete output (command, every line, exit status) and its execution trace id, never overwritten by a rerun. Before selecting a fix, read the complete inputs, prompts, tool arguments/results, intermediate stages and final output, including the full check command/output and the changed files. Cite the observed divergence and classify evidence absent, returned but unused or contradicted, invalid expectation, or unresolved. An unresolved diagnosis cannot authorize a causal repair; it permits only further investigation. Bind the targeted repair to a new traced verification run; retain the failed original. Review every failing or surprising item and a sample of passes. A complete review is distinct from a passing run. Criterion `outcome` covers the entire requested success check.

### [`docs/plans/commit-rule-root-relative-links.path-decision.json`](../docs/plans/commit-rule-root-relative-links.path-decision.json)

_No source-local artifact summary._

### [`docs/plans/commit-rule-root-relative-links.receipt.json`](../docs/plans/commit-rule-root-relative-links.receipt.json)

_No source-local artifact summary._

### [`docs/plans/commit-rule-root-relative-links.verdicts.json`](../docs/plans/commit-rule-root-relative-links.verdicts.json)

_No source-local artifact summary._

### [`docs/plans/commit-rule-skip-roots.adoption-attempts.jsonl`](../docs/plans/commit-rule-skip-roots.adoption-attempts.jsonl)

_No source-local artifact summary._

### [`docs/plans/commit-rule-skip-roots.adoption-decision.json`](../docs/plans/commit-rule-skip-roots.adoption-decision.json)

_No source-local artifact summary._

### [`docs/plans/commit-rule-skip-roots.bundle.json`](../docs/plans/commit-rule-skip-roots.bundle.json)

_No source-local artifact summary._

### [`docs/plans/commit-rule-skip-roots.check.txt`](../docs/plans/commit-rule-skip-roots.check.txt)

_No source-local artifact summary._

### [`docs/plans/commit-rule-skip-roots.facts.json`](../docs/plans/commit-rule-skip-roots.facts.json)

_No source-local artifact summary._

### [`docs/plans/commit-rule-skip-roots.goal.md`](../docs/plans/commit-rule-skip-roots.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `docs/plans/commit-rule-skip-roots.md` (plan sha256 b5292dab8cfd186457eeaa785e5b04d0d55f2663206bdd29a53361b05cc115c6, route inline_prototype). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`docs/plans/commit-rule-skip-roots.md`](../docs/plans/commit-rule-skip-roots.md)

Preserve the failed check and its execution trace id. Before selecting a fix, read the complete inputs, prompts, tool arguments/results, intermediate stages and final output, including the full check command/output and the changed files. Cite the observed divergence and classify evidence absent, returned but unused or contradicted, invalid expectation, or unresolved. Investigate an unresolved cause before authorizing a causal repair. Bind the targeted repair to a new traced verification run; retain the failed original. Review every failing or surprising item and a sample of passes. A complete review is distinct from a passing run. Criterion `outcome` covers the entire requested success check.

### [`docs/plans/commit-rule-skip-roots.path-decision.json`](../docs/plans/commit-rule-skip-roots.path-decision.json)

_No source-local artifact summary._

### [`docs/plans/commit-rule-skip-roots.receipt.json`](../docs/plans/commit-rule-skip-roots.receipt.json)

_No source-local artifact summary._

### [`docs/plans/commit-rule-skip-roots.verdicts.json`](../docs/plans/commit-rule-skip-roots.verdicts.json)

_No source-local artifact summary._

### [`docs/plans/commit-tag-contract.adoption-attempts.jsonl`](../docs/plans/commit-tag-contract.adoption-attempts.jsonl)

_No source-local artifact summary._

### [`docs/plans/commit-tag-contract.adoption-decision.json`](../docs/plans/commit-tag-contract.adoption-decision.json)

_No source-local artifact summary._

### [`docs/plans/commit-tag-contract.bundle.json`](../docs/plans/commit-tag-contract.bundle.json)

_No source-local artifact summary._

### [`docs/plans/commit-tag-contract.check.txt`](../docs/plans/commit-tag-contract.check.txt)

_No source-local artifact summary._

### [`docs/plans/commit-tag-contract.facts.json`](../docs/plans/commit-tag-contract.facts.json)

_No source-local artifact summary._

### [`docs/plans/commit-tag-contract.goal.md`](../docs/plans/commit-tag-contract.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `docs/plans/commit-tag-contract.md` (plan sha256 a708a625716b4b52229ff5ac12ec79e765bd9d24685670c754f32d4cd31713fb, route inline_prototype). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`docs/plans/commit-tag-contract.md`](../docs/plans/commit-tag-contract.md)

This procedure is separate from the anticipated failure named in the disproof under Success and disproof: it applies to any run that fails or surprises us. Preserve the failed check and its execution trace id. Before selecting a fix, read the complete inputs, prompts, tool arguments/results, intermediate stages and final output, including the full check command/output and the changed files. Cite the observed divergence and classify evidence absent, returned but unused or contradicted, invalid expectation, or unresolved. An unresolved diagnosis cannot authorize a causal repair; it permits only further investigation. Bind the targeted repair to a new traced verification run; retain the failed original. Review every failing or surprising item and a sample of passes. A complete review is distinct from a passing run. Criterion `outcome` covers the entire requested success check.

### [`docs/plans/commit-tag-contract.path-decision.json`](../docs/plans/commit-tag-contract.path-decision.json)

_No source-local artifact summary._

### [`docs/plans/commit-tag-contract.receipt.json`](../docs/plans/commit-tag-contract.receipt.json)

_No source-local artifact summary._

### [`docs/plans/commit-tag-contract.verdicts.json`](../docs/plans/commit-tag-contract.verdicts.json)

_No source-local artifact summary._

### [`docs/plans/durable-check-commit-rule.adoption-attempts.jsonl`](../docs/plans/durable-check-commit-rule.adoption-attempts.jsonl)

_No source-local artifact summary._

### [`docs/plans/durable-check-commit-rule.adoption-decision.json`](../docs/plans/durable-check-commit-rule.adoption-decision.json)

_No source-local artifact summary._

### [`docs/plans/durable-check-commit-rule.bundle.json`](../docs/plans/durable-check-commit-rule.bundle.json)

_No source-local artifact summary._

### [`docs/plans/durable-check-commit-rule.check.txt`](../docs/plans/durable-check-commit-rule.check.txt)

_No source-local artifact summary._

### [`docs/plans/durable-check-commit-rule.facts.json`](../docs/plans/durable-check-commit-rule.facts.json)

_No source-local artifact summary._

### [`docs/plans/durable-check-commit-rule.goal.md`](../docs/plans/durable-check-commit-rule.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `docs/plans/durable-check-commit-rule.md` (plan sha256 69e294bad1b9718cc259f937544176e1643dab781f142476a10e959feb3337c5, route inline_prototype). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`docs/plans/durable-check-commit-rule.md`](../docs/plans/durable-check-commit-rule.md)

This procedure is separate from the anticipated failure named in the disproof under Success and disproof: it applies to any run that fails or surprises us. Preserve the failed check and its execution trace id. Before selecting a fix, read the complete inputs, prompts, tool arguments/results, intermediate stages and final output, including the full check command/output and the changed files. Cite the observed divergence and classify evidence absent, returned but unused or contradicted, invalid expectation, or unresolved. An unresolved diagnosis cannot authorize a causal repair; it permits only further investigation. Bind the targeted repair to a new traced verification run; retain the failed original. Review every failing or surprising item and a sample of passes. A complete review is distinct from a passing run. Criterion `outcome` covers the entire requested success check.

### [`docs/plans/durable-check-commit-rule.path-decision.json`](../docs/plans/durable-check-commit-rule.path-decision.json)

_No source-local artifact summary._

### [`docs/plans/durable-check-commit-rule.receipt.json`](../docs/plans/durable-check-commit-rule.receipt.json)

_No source-local artifact summary._

### [`docs/plans/durable-check-commit-rule.verdicts.json`](../docs/plans/durable-check-commit-rule.verdicts.json)

_No source-local artifact summary._

### [`docs/plans/rules-register.adoption-attempts.jsonl`](../docs/plans/rules-register.adoption-attempts.jsonl)

_No source-local artifact summary._

### [`docs/plans/rules-register.adoption-decision.json`](../docs/plans/rules-register.adoption-decision.json)

_No source-local artifact summary._

### [`docs/plans/rules-register.bundle.json`](../docs/plans/rules-register.bundle.json)

_No source-local artifact summary._

### [`docs/plans/rules-register.facts.json`](../docs/plans/rules-register.facts.json)

_No source-local artifact summary._

### [`docs/plans/rules-register.goal.md`](../docs/plans/rules-register.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `docs/plans/rules-register.md` (plan sha256 5ddc64fa7caa79880a30337611e86ea889ee56d19304000d6beed5d6f1bf2e39, route inline_prototype). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`docs/plans/rules-register.md`](../docs/plans/rules-register.md)

- register rule entries (id, rule, origin, enforcement_status, enforcement_mechanism, evidence): every entry must appear on the built page with its status - RULES.md page: summary counts must equal the register's and project-meta's counts (12, 21, 263)

### [`docs/plans/rules-register.path-decision.json`](../docs/plans/rules-register.path-decision.json)

_No source-local artifact summary._

### [`docs/plans/rules-register.receipt.json`](../docs/plans/rules-register.receipt.json)

_No source-local artifact summary._

### [`docs/plans/rules-register.verdicts.json`](../docs/plans/rules-register.verdicts.json)

_No source-local artifact summary._

### [`docs/plans/shaping-nav-preflight.adoption-attempts.jsonl`](../docs/plans/shaping-nav-preflight.adoption-attempts.jsonl)

_No source-local artifact summary._

### [`docs/plans/shaping-nav-preflight.adoption-decision.json`](../docs/plans/shaping-nav-preflight.adoption-decision.json)

_No source-local artifact summary._

### [`docs/plans/shaping-nav-preflight.bundle.json`](../docs/plans/shaping-nav-preflight.bundle.json)

_No source-local artifact summary._

### [`docs/plans/shaping-nav-preflight.check.txt`](../docs/plans/shaping-nav-preflight.check.txt)

_No source-local artifact summary._

### [`docs/plans/shaping-nav-preflight.facts.json`](../docs/plans/shaping-nav-preflight.facts.json)

_No source-local artifact summary._

### [`docs/plans/shaping-nav-preflight.goal.md`](../docs/plans/shaping-nav-preflight.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `docs/plans/shaping-nav-preflight.md` (plan sha256 fec0dc40c1a1a10f829922ad1394930aacdabc85be356503c6235c9404eaa9fa, route inline_prototype). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`docs/plans/shaping-nav-preflight.md`](../docs/plans/shaping-nav-preflight.md)

This procedure is separate from the anticipated failure named in the disproof under Success and disproof: it applies to any run that fails or surprises us. Preserve the failed check and its execution trace id. Before selecting a fix, read the complete inputs, prompts, tool arguments/results, intermediate stages and final output, including the full check command/output and the changed files. Cite the observed divergence and classify evidence absent, returned but unused or contradicted, invalid expectation, or unresolved. An unresolved diagnosis cannot authorize a causal repair; it permits only further investigation. Bind the targeted repair to a new traced verification run; retain the failed original. Review every failing or surprising item and a sample of passes. A complete review is distinct from a passing run. Criterion `outcome` covers the entire requested success check.

### [`docs/plans/shaping-nav-preflight.path-decision.json`](../docs/plans/shaping-nav-preflight.path-decision.json)

_No source-local artifact summary._

### [`docs/plans/shaping-nav-preflight.receipt.json`](../docs/plans/shaping-nav-preflight.receipt.json)

_No source-local artifact summary._

### [`docs/plans/shaping-nav-preflight.verdicts.json`](../docs/plans/shaping-nav-preflight.verdicts.json)

_No source-local artifact summary._

### [`docs/rules/RULES.md`](../docs/rules/RULES.md)

Published AES rules, their enforcement and evidence. Complete legacy source text stays in the private inventory; its proposed dispositions are summarized below. Generated by `scripts/rules/build_rules_page.py` from [the AES rules register](register.yaml); edit the inputs, not this page.

### [`docs/rules/legacy-dispositions.yaml`](../docs/rules/legacy-dispositions.yaml)

_No source-local artifact summary._

### [`docs/rules/register.yaml`](../docs/rules/register.yaml)

_No source-local artifact summary._

### [`docs/terms/ecosystem-terms.md`](../docs/terms/ecosystem-terms.md)

Status: first entries, 2026-10-05. A controlled vocabulary: one meaning per term, usable in any project. It is a terms list, not an architecture authority. Planning-runtime words (accepted, approved, claimed, ready, ...) live in `agent-skills/contracts/terminology.md`; do not duplicate them here.

### [`evals/README.md`](../evals/README.md)

Status: active Role: behavioral/system evaluations distinct from deterministic tests Authority: evaluation definitions and scoped measurements Lifecycle: versioned definitions; retained observations where needed

### [`evals/plan-002/P0_RUNBOOK.md`](../evals/plan-002/P0_RUNBOOK.md)

Status: executable handoff; **P0 is not yet closed** Plan authority: `docs/plans/002_offline_policy_decision_replay.md` Case inventory: `evals/plan-002/case_manifest.json` Execution tracker: Issue #20

### [`evals/plan-002/README.md`](../evals/plan-002/README.md)

Status: P0 source inventory in progress Authority: Plan 002 defines scope and stop rules; this directory holds bounded evaluation definitions and source-reference manifests. Execution handoff: [`P0_RUNBOOK.md`](P0_RUNBOOK.md) contains the exact machine/provider closure sequence.

### [`evidence/README.md`](../evidence/README.md)

Status: active Role: retained observations and run receipts Authority: authoritative for what was observed, not its interpretation Lifecycle: append-only/immutable where practical

### [`evidence/greenfield/clean-user-run-2-2026-09-25.md`](../evidence/greenfield/clean-user-run-2-2026-09-25.md)

Repeat of `clean-user-run-2026-09-25.md` at AES `2d3486b` after phases 3–6. Observation of record: `.aes/observations/OBS-AES-CLEAN-USER-2d3486b.yaml` (supersedes `OBS-AES-CLEAN-USER-0503735`). Same runner setup and the same caveat: a fresh agent given only the page, on the maintainer's machine, since the repository is private by decision.

### [`evidence/greenfield/clean-user-run-2026-09-25.md`](../evidence/greenfield/clean-user-run-2026-09-25.md)

Evidence for `ER-SC-GF-001-01` (external consumer observation), retained here until AES canonical has its own `.aes/observations/` (roadmap phase 6), when it is converted to an observation record at this exact revision. Converted in roadmap phase 6b: `.aes/observations/OBS-AES-CLEAN-USER-0503735.yaml` (this file stays as the report the record cites).

### [`evidence/greenfield/clean-user-run-3-2026-09-25.md`](../evidence/greenfield/clean-user-run-3-2026-09-25.md)

At AES `3dd2b9a` (the phase-7b commit, run before merge and merged with a merge commit). Observation of record: `.aes/observations/OBS-AES-CLEAN-USER-3dd2b9a.yaml` (supersedes run 2). Same setup and caveat as runs 1 and 2.

### [`evidence/greenfield/clean-user-run-4-2026-10-04.md`](../evidence/greenfield/clean-user-run-4-2026-10-04.md)

At AES `d89fe2e` (branch `bri36-getting-started-uv`, run before merge and merged with a merge commit), the commit that moved the page's install from `python3 -m venv` plus `pip` to `uv venv` plus `uv pip install`. Observation of record: `.aes/observations/OBS-AES-CLEAN-USER-d89fe2e.yaml` (supersedes runs 1-3).

### [`evidence/greenfield/context-ab-2026-09-25/preregistration.md`](../evidence/greenfield/context-ab-2026-09-25/preregistration.md)

Change under test: `aes status`/`aes reconcile` report ER-SC-GF-005-02 and ER-SC-GF-009-01 as "no route" although each has an `external_boundaries` entry in `.aes/target.yaml` and `aes target validate` accepts them. Fix: an evidence requirement with an external boundary is routed.

### [`evidence/greenfield/context-ab-2026-09-25/result.md`](../evidence/greenfield/context-ab-2026-09-25/result.md)

Base: AES canonical `2509ea4` (the repository governing itself; ~4,000 lines of v0.2 source and tests under the governed roots plus 18 retained v0.1 files). Change: "an external boundary is a route" in `reconcile.py` — a real bug found by the phase-6b builder. Pre-registration: `preregistration.md` (written before either arm ran). Arms: two fresh Claude Opus 5.5 agent sessions in separate clones, no access to the orchestrator's conversation or the proposals directory. Arm A: change request + `aes context RU-AES-RECONCILE` packet (as a file) + repository. Arm B: change request + repository, README first.

### [`evidence/modular-design-integration-2026-09-22.md`](../evidence/modular-design-integration-2026-09-22.md)

Recorded: 2026-09-22. Subject: documentation-only commit `d65df4a6df2015dc345f2cd04c0d6ce003df59c4`. Comparison baseline: `996530de0d034687b49a1acb89d3261681eb6274`. Scope: Decision 0009, AES-CAP-003/004/005, canonical agent instructions and their generated projection, existing Company Planning profile, and navigation.

### [`evidence/plan-001/320991b96a3e3aaa15aa8ba05817a7eee1c52603/characterization.md`](../evidence/plan-001/320991b96a3e3aaa15aa8ba05817a7eee1c52603/characterization.md)

Characterized AES revision: `320991b96a3e3aaa15aa8ba05817a7eee1c52603`

### [`evidence/plan-001/96fcf5e89ba98ad9ff278ec536a98c308cda3fe1/characterization.md`](../evidence/plan-001/96fcf5e89ba98ad9ff278ec536a98c308cda3fe1/characterization.md)

Characterized AES revision: `96fcf5e89ba98ad9ff278ec536a98c308cda3fe1`

### [`evidence/plan-001/a1/53be16fa1159f31648773062531d751c85d7a011.md`](../evidence/plan-001/a1/53be16fa1159f31648773062531d751c85d7a011.md)

Reviewed AES revision: `53be16fa1159f31648773062531d751c85d7a011` Reviewed consumer: `BrianMills2718/data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0` Surface: `generated/repository-context/BrianMills2718__data-contracts/90c38998e8141bd07e49a77a49ec417aa29beee0/index.html`

### [`evidence/plan-001/a1/96fcf5e89ba98ad9ff278ec536a98c308cda3fe1.md`](../evidence/plan-001/a1/96fcf5e89ba98ad9ff278ec536a98c308cda3fe1.md)

Reviewed AES revision: `96fcf5e89ba98ad9ff278ec536a98c308cda3fe1` Reviewed consumer: `BrianMills2718/data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0` Reviewed surface SHA-256: `dfabfa0749614a04ef2206eb503002085c5313d9fb46d52288e81c692bb0aed6`

### [`evidence/plan-001/pr5-integration-readiness-2026-09-18.md`](../evidence/plan-001/pr5-integration-readiness-2026-09-18.md)

**Approved for integration into canonical `main` as implementation-partial.**

### [`experiments/README.md`](../experiments/README.md)

Status: unused Role: bounded experiments and prototypes Authority: experimental observations; non-normative Lifecycle: design -> run -> readout/disposition

### [`human-facing/README.md`](../human-facing/README.md)

Status: unused Role: routing for human-facing interactive/non-interactive surfaces Authority: concern routing, not necessarily implementation source Lifecycle: versioned routing/current surfaces

### [`operations/README.md`](../operations/README.md)

Status: unused Role: operating a realized system Authority: current operating procedure/configuration Lifecycle: current procedures plus append-only operational evidence

### [`proposals/README.md`](../proposals/README.md)

Status: active Role: non-binding proposed changes Authority: proposed only Lifecycle: retained through disposition

### [`proposals/aes-adopt-existing/README.md`](../proposals/aes-adopt-existing/README.md)

**Example.** DIGIMON (`~/code/Digimon_for_KG_application`) has about 1,800 tracked files and 220 numbered plans. Today `aes init` there followed by a commit is refused: every existing file is an orphan (issue #155 reproduced the same on tinydb's 20 files). After this plan, `aes adopt --governed-root Core/ ...` lists every tracked file under those roots in one JSON file, the adoption commit passes the hooks, and `aes status` reads `legacy: N of N governed files (100.0%)`. When an agent later edits `Core/x.py` under a plan that lists it, the baseline drops to N-1, and the dropped entry is exactly `Core/x.py`.

### [`proposals/aes-adopt-existing/aes-adopt-existing.goal.md`](../proposals/aes-adopt-existing/aes-adopt-existing.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/aes-adopt-existing/README.md` (plan sha256 273d9e2044673d7aed4ba3b6b91ff3e0cca1c71ae08cef91469259c29f9c2411, route repair). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/aes-brownfield-docs/PLAN.md`](../proposals/aes-brownfield-docs/PLAN.md)

<a id="outcome"></a>

### [`proposals/aes-brownfield-docs/RETROFIT_NOTE.md`](../proposals/aes-brownfield-docs/RETROFIT_NOTE.md)

Milestone M2 of [`PLAN.md`](PLAN.md). Records what bringing an existing repository's documentation into AES canonical's declared layout actually took, so the documentation-rule decision (M3) and any rollout (M4) start from evidence.

### [`proposals/aes-brownfield-docs/aes-brownfield-docs.goal.md`](../proposals/aes-brownfield-docs/aes-brownfield-docs.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/aes-brownfield-docs/PLAN.md` (plan sha256 cd951538870e86e8514788b53ce37128c52568b1f2a8e6fa377ec899deaca9c5, route durable_solo). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/aes-durable-docs/PLAN.md`](../proposals/aes-durable-docs/PLAN.md)

**Why now.** A survey of 36 repositories active in the last two weeks (2026-10-10, `git ls-files` by path) found about 3,300 plan files and about 600 decision records, but requirements documents in 2 repositories, a system model (`docs/model/ODD.md`) in 8 and `.aes/target.yaml` in 4. Plans record each change and are never folded back into anything a reader can trust as current. Company Planning makes a PRD optional (`landscape-review/SKILL.md:74`), never asks for decision records, and has no completion step for quick-adopted plans.

### [`proposals/aes-durable-docs/aes-durable-docs.goal.md`](../proposals/aes-durable-docs/aes-durable-docs.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/aes-durable-docs/PLAN.md` (plan sha256 76365003ff6ee2ed150e773dfc8e81ac658d125fdde87b69a885f8c9c7142d9e, route coordinated). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/aes-durable-docs/evidence/m4-aes-canonical-cold-reader-review.md`](../proposals/aes-durable-docs/evidence/m4-aes-canonical-cold-reader-review.md)

Review of the fresh Haiku reader's trace answering the canonical question in AES canonical (aes-durable-docs M4)

### [`proposals/aes-durable-docs/evidence/m4-company-planning-cold-reader-review.md`](../proposals/aes-durable-docs/evidence/m4-company-planning-cold-reader-review.md)

Review of the fresh Haiku reader's trace answering the canonical question in company-planning (Plan

### [`proposals/aes-durable-docs/evidence/m5-disproof-sample.md`](../proposals/aes-durable-docs/evidence/m5-disproof-sample.md)

M5 disproof sample for aes-durable-docs, run 2026-10-11 under the amended timing and population; the disproof condition fires (9 of 10 none or mechanical), because the rule was not in effect for 8 of the 10 plans (stale installed plugin or repository not yet declared)

### [`proposals/aes-durable-docs/evidence/m5-rollout.md`](../proposals/aes-durable-docs/evidence/m5-rollout.md)

Inventory: `m5-inventory.json` (22 active governed repositories, built by Haiku readers on 2026-10-11). Each repository got one PR that adds its durable document set (system model at `docs/model/ARCHITECTURE.md`, per company-planning#116), checked with `durable_docs_check.py --arc42` and the repository's own local check before merge. "Daily check" is `project-meta/scripts/md_file_cap.py --repo <path> --ref origin/main`, run after merge; `durable=ok(0)` means zero durable-set findings on main.

### [`proposals/aes-feedback-prevention/PLAN.md`](../proposals/aes-feedback-prevention/PLAN.md)

Each section below answers the checklist items quoted in it; the gate judges only that section's text. Replace every `TODO(answer ...)` line before running `cli.py check`. Quote values in the front matter: an unquoted ` #` starts a YAML comment and cuts the value.

### [`proposals/aes-feedback-prevention/SYSTEM_MODEL.md`](../proposals/aes-feedback-prevention/SYSTEM_MODEL.md)

Scope: AES owns report production, native parent checks and canonical instructions; agent-skills owns the taxonomy reader and dispositions. This extends the existing [subagent model](../aes-subagent-feedback/SYSTEM_MODEL.md), not its producer contract.

### [`proposals/aes-feedback-prevention/aes-feedback-prevention.goal.md`](../proposals/aes-feedback-prevention/aes-feedback-prevention.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/aes-feedback-prevention/PLAN.md` (plan sha256 664e310495ad628711ddc020bb36be45abcb9e9ed9be29bcdddf2d311ee01c97, route repair). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/aes-learning-loop/DESIGN.md`](../proposals/aes-learning-loop/DESIGN.md)

Status: **historical, the original design (2 to 7 October 2026).** Kept as the record of why the loop was built this way. It no longer describes what runs: since then the loop gained feedback reports in a private issue log, a weekly analysis that licenses fixes, enforcement receipts and an effect counter, a daily fix owner, and a rule check. For the system as it runs today, read in this order:

### [`proposals/aes-learning-loop/PLAN.md`](../proposals/aes-learning-loop/PLAN.md)

**Actors.** Every Claude and Codex agent working in Brian's repositories (they report), the nightly and weekly loop runs (they sort, analyse, and adopt or retire rules by their best judgment), and Brian (he observes a view ranked by impact and uncertainty and is notified of the items that matter; he is not an approver).

### [`proposals/aes-learning-loop/REPAIR.md`](../proposals/aes-learning-loop/REPAIR.md)

Brian approved this bounded repair on 2026-10-08 after the independent review. It implements the existing adopted learning-loop plan's evidence and observed effect requirements; it does not adopt new agent-behavior rules.

### [`proposals/aes-learning-loop/aes-learning-loop.goal.md`](../proposals/aes-learning-loop/aes-learning-loop.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/aes-learning-loop/PLAN.md` (plan sha256 c70b91d36508c444f4f64cf2bb2d70ef2e11c5572b48540a1b4b1ed57535a387, route coordinated). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/aes-plan-scope/README.md`](../proposals/aes-plan-scope/README.md)

**Example.** DIGIMON's robot worker opened pull request 414 under adopted Plan 216: three commits, one of which edits an existing test file. Under enforce that commit is refused today (`aes commit replay`: 3 commits, 2 accepted, 1 refused), because a Company Planning plan declares no paths and only `aes plan accept` can clear a file from the baseline. After this plan, Plan 216 adds five `conflict_surfaces` lines, is re-adopted, and the same replay reads 3 accepted.

### [`proposals/aes-plan-scope/aes-plan-scope.goal.md`](../proposals/aes-plan-scope/aes-plan-scope.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/aes-plan-scope/README.md` (plan sha256 1fcf700f1681ac40cdbc078f0c8bf680aa29a977738ba980247e480653d1a9fe, route repair). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/aes-planning/README.md`](../proposals/aes-planning/README.md)

- 2026-10-06: "we should enforce this ['I wrote a plan page, but I didn't plan it the way your system says to']". - 2026-10-06: "i guess we could have aes plans be one of the routes in company planning and then we can work towards getting everything in that format ... yeah we need to lock down unplanned. there are some trivial cases where that is correct but for real implementation work we should always have a plan." - 2026-10-06: "in general we want to be upfront planning what is optimal then using /goal ... company planning ... should generate the /goal text where it is known as part of the plans." - 2026-10-06: "once we get aes canonical working we refactor all my projects into aes and force all work going forward into aes compliance."

### [`proposals/aes-planning/ROLLOUT.md`](../proposals/aes-planning/ROLLOUT.md)

Work units P4 and P6 of `proposals/aes-planning/` (owner was `coordinator:code-71`; that session ended, and this rollout was taken over on 2026-10-07).

### [`proposals/aes-planning/aes-planning.goal.md`](../proposals/aes-planning/aes-planning.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/aes-planning/README.md` (plan sha256 3f23048815244cf7b768c0f35f752f7cdd752ebcb2ff00b3324e77351255962e, route coordinated). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/aes-subagent-feedback/PLAN.md`](../proposals/aes-subagent-feedback/PLAN.md)

Each section below answers the checklist items quoted in it; the gate judges only that section's text. Replace every `TODO(answer ...)` line before running `cli.py check`. Quote values in the front matter: an unquoted ` #` starts a YAML comment and cuts the value.

### [`proposals/aes-subagent-feedback/SYSTEM_MODEL.md`](../proposals/aes-subagent-feedback/SYSTEM_MODEL.md)

This extends the [existing loop](../aes-learning-loop/PLAN.md) without another store.

### [`proposals/aes-subagent-feedback/aes-subagent-feedback.goal.md`](../proposals/aes-subagent-feedback/aes-subagent-feedback.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/aes-subagent-feedback/PLAN.md` (plan sha256 00979b080c2f9fc96a078926a838eee827b96b48c223303a39dba0ab47b94fb7, route coordinated). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/aes-v0.2-greenfield/01-design-thesis.md`](../proposals/aes-v0.2-greenfield/01-design-thesis.md)

Status: **candidate design thesis / non-normative**

### [`proposals/aes-v0.2-greenfield/05-donor-reentry.md`](../proposals/aes-v0.2-greenfield/05-donor-reentry.md)

Prevent the clean-sheet architecture from silently becoming a repackaging of existing private systems.

### [`proposals/aes-v0.2-greenfield/06-open-questions.md`](../proposals/aes-v0.2-greenfield/06-open-questions.md)

Status: **active review queue / non-normative** Date: 2026-09-24

### [`proposals/aes-v0.2-greenfield/07-semantic-clean-sheet-review-pass-1.md`](../proposals/aes-v0.2-greenfield/07-semantic-clean-sheet-review-pass-1.md)

Review role: **historical/supporting rationale**. Its accepted corrections are incorporated into `02-semantic-model.candidate.yaml` and `03-lifecycle.candidate.yaml`.

### [`proposals/aes-v0.2-greenfield/08-semantic-clean-sheet-review-pass-2.md`](../proposals/aes-v0.2-greenfield/08-semantic-clean-sheet-review-pass-2.md)

Define the minimum semantic joins required by the Greenfield MVP without introducing a universal relationship registry.

### [`proposals/aes-v0.2-greenfield/09-semantic-clean-sheet-review-pass-3-topology.md`](../proposals/aes-v0.2-greenfield/09-semantic-clean-sheet-review-pass-3-topology.md)

Review role: **historical/supporting rationale**. Current topology semantics are incorporated into `02-semantic-model.candidate.yaml`, `13-greenfield-materialization.candidate.md`, and `20-realization-topology.candidate.yaml`.

### [`proposals/aes-v0.2-greenfield/10-greenfield-mvp-validation-profile.md`](../proposals/aes-v0.2-greenfield/10-greenfield-mvp-validation-profile.md)

Prevent the Greenfield MVP from being "validated" by a project so trivial that it does not exercise the architecture's load-bearing semantics.

### [`proposals/aes-v0.2-greenfield/11-semantic-clean-sheet-review-pass-4-target-analysis.md`](../proposals/aes-v0.2-greenfield/11-semantic-clean-sheet-review-pass-4-target-analysis.md)

Review role: **historical/supporting rationale**. Current target/analysis/transition distinctions are incorporated into `02-semantic-model.candidate.yaml` and `03-lifecycle.candidate.yaml`.

### [`proposals/aes-v0.2-greenfield/13-greenfield-materialization.candidate.md`](../proposals/aes-v0.2-greenfield/13-greenfield-materialization.candidate.md)

Choose the smallest opinionated project storage convention that can materialize the clean semantic model for a fresh project without making storage layout part of the ontology.

### [`proposals/aes-v0.2-greenfield/18-provider-evaluation-round-1.md`](../proposals/aes-v0.2-greenfield/18-provider-evaluation-round-1.md)

Review role: **supporting provider rationale**. Current candidate bindings are in `21-provider-bindings.candidate.yaml`.

### [`proposals/aes-v0.2-greenfield/19-provider-evaluation-round-2-generic-dependencies.md`](../proposals/aes-v0.2-greenfield/19-provider-evaluation-round-2-generic-dependencies.md)

Review role: **supporting dependency rationale**. Current candidate bindings are in `21-provider-bindings.candidate.yaml`.

### [`proposals/aes-v0.2-greenfield/22-portable-provider-boundaries.md`](../proposals/aes-v0.2-greenfield/22-portable-provider-boundaries.md)

Resolve two Greenfield-MVP provider questions without binding AES to a private planning plugin, a particular LLM vendor, or a client-specific hook runtime.

### [`proposals/aes-v0.2-greenfield/23-greenfield-cli-product-contract.md`](../proposals/aes-v0.2-greenfield/23-greenfield-cli-product-contract.md)

Status: **candidate product surface / non-normative** Date: 2026-09-24

### [`proposals/aes-v0.2-greenfield/24-pre-probe-decisions.md`](../proposals/aes-v0.2-greenfield/24-pre-probe-decisions.md)

Status: **accepted pre-probe decisions / non-normative until v0.2 cutover** Date: 2026-09-25 Review basis: `REVIEW.md`, all primary candidate files, `docs/decisions/0001`–`0009` Reviewer: independent agent session (Claude Fable 5.1), first read not authored by the proposal's author session. Brian approved the consumer-selection rule (option A below) in conversation on 2026-09-25.

### [`proposals/aes-v0.2-greenfield/25-roadmap-to-mvp-acceptance.md`](../proposals/aes-v0.2-greenfield/25-roadmap-to-mvp-acceptance.md)

Status: accepted by Decision 0010 (`docs/decisions/0010-greenfield-v0.2-accepted.md`, 2026-09-25). The accepted architecture is `docs/architecture/greenfield-v0.2/`; this file is proposal lineage. One criterion, SC-GF-001, stands INSUFFICIENT at acceptance and is not downgraded: it waits on clean-user run 3 on current code (§0, Decision 0010).

### [`proposals/aes-v0.2-greenfield/README.md`](../proposals/aes-v0.2-greenfield/README.md)

Define the next AES architecture generation from first principles while preserving the existing repository as empirical history.

### [`proposals/aes-v0.2-greenfield/REVIEW.md`](../proposals/aes-v0.2-greenfield/REVIEW.md)

Status: **review snapshot / proposal / non-normative** Date: 2026-09-24 Branch: `architecture/v0.2-greenfield` Base lineage: `main@36c205d3363a7304c6043ca645acae5eea58e97c`

### [`proposals/agent-router/PLAN.md`](../proposals/agent-router/PLAN.md)

Design, diagram and the dashboard example: [README.md](README.md). Brian activated the goal "finish all remaning work" on 2026-10-09, authorizing completion of this remaining feedback/router work. The earlier [revision goal](revision.goal.md), [revision route](revision-path-decision.json) and [verification trace](verification.log) remain evidence of the document-only correction task. The 2026-10-08 receipt and generated goal do not adopt the changed plan. Re-adopt this exact plan before implementation; retain the original outcome and all observation, parity, fallback and promotion obligations below.

### [`proposals/agent-router/README.md`](../proposals/agent-router/README.md)

Status: adopted 2026-10-09; collector repair merged in PR #499 and inventory repair in PR #500; privacy/source-binding follow-up merged in PR #503 and verified in the installed reader; profile/accounting core merged in [PR #497](https://github.com/BrianMills2718/agentic-engineering-system-canonical/pull/497), while runtime acceptance remains pending. [PLAN.md](PLAN.md), its [adoption decision](receipt.adoption-decision.json), [receipt](receipt.json) and [generated goal](agent-router.goal.md) govern completion. All eight complete criteria remain planned in the [acceptance records](evidence.json). The [revision goal](revision.goal.md), [route](revision-path-decision.json) and [verification](verification.log) retain the earlier document-only evidence. The [offline inventory check](inventory-check.json) binds all 263 current source IDs: 229 keep, 27 covered and 7 retirement candidates. Complete policies, named quotations and validated applicability remain privately recoverable; the [public manifest](../../docs/rules/legacy-dispositions.yaml) exposes structural outcomes and evidence hashes. No further paid sorting is authorized by the exhausted legacy allowance; mandatory instructions are neither retired nor activated by the inventory.

### [`proposals/agent-router/agent-router.goal.md`](../proposals/agent-router/agent-router.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/agent-router/PLAN.md` (plan sha256 2c5c15085ffc0d1c3090e800ef1ef3beae6f49f1ab7eebaff69a3c81e180c0f7, route coordinated). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/agent-router/revision.goal.md`](../proposals/agent-router/revision.goal.md)

Brian explicitly set this goal in native session `01a11cae-eadf-7192-9a72-ca2283a3ebc0` on 2026-10-08 local time. The existing [PLAN](PLAN.md) is the design being revised; [verification](verification.log) records this revision's checks. The older generated `agent-router.goal.md` is retained historical adoption evidence and is not this task's launcher.

### [`proposals/code2-ecosystem/PLAN.md`](../proposals/code2-ecosystem/PLAN.md)

Brian approved this on 2026-10-13 ("yes lets make the move") after asking for a fresh start: "start a like code2 dir that has aes canoncial and maybe like a few relevant repos and star over there", with enforcement that "should live in the ecosystem not in the repo" and one source of truth. Project-meta is his legacy system; AES canonical replaces it.

### [`proposals/code2-ecosystem/code2-ecosystem.goal.md`](../proposals/code2-ecosystem/code2-ecosystem.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/code2-ecosystem/PLAN.md` (plan sha256 cb486612c978bd9195879b4d17ae6b8445e44a22161561fb2e9c233f44c7fb46, route coordinated). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/code2-ecosystem/hookspath-review.md`](../proposals/code2-ecosystem/hookspath-review.md)

Git runs hooks from exactly one folder. Most repositories under `~/code` use the shared folder `~/.config/git/hooks`. The 34 below override it with a local `core.hooksPath`, so the shared hooks do not run there unless something forwards to them. This page lists each one, why it overrides the shared folder, and what phase 2 should do with it.

### [`proposals/code2-ecosystem/workspace/AGENTS.md`](../proposals/code2-ecosystem/workspace/AGENTS.md)

`~/code2` is the fresh workspace that repositories join by moving in. This file is linked as `~/code2/AGENTS.md`; its source of truth is `proposals/code2-ecosystem/workspace/AGENTS.md` in agentic-engineering-system-canonical (AES canonical). Change it there, through a commit, never by editing the link target in place.

### [`proposals/commit-rule-followups/commit-rule-followups.goal.md`](../proposals/commit-rule-followups/commit-rule-followups.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/commit-rule-followups/commit-rule-followups.md` (plan sha256 81a52810fadde51eff4e73a22e784caeb415a9ff05fd0b7d9452a3b6c548e60c, route inline_prototype). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/commit-rule-followups/commit-rule-followups.md`](../proposals/commit-rule-followups/commit-rule-followups.md)

| Uncertainty | Owner or resolving evidence | | --- | --- | | Whether the change needs files beyond the list below; if so it is out of scope for this plan | Resolved before editing: grep -n RUNNING_THING src/agentic_engineering_system/commit_rule.py shows the running-thing list lives only there (lines 91-96); the misuse review reads the same log (proposals/aes-planning/rollout/misuse_review.py) |

### [`proposals/commit-rule-notes-report/commit-rule-notes-report.goal.md`](../proposals/commit-rule-notes-report/commit-rule-notes-report.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/commit-rule-notes-report/commit-rule-notes-report.md` (plan sha256 50d45de7933b0f6eb95b34c941c1caa13cb24a93e90ad23a8f2e4422549ce9b5, route inline_prototype). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/commit-rule-notes-report/commit-rule-notes-report.md`](../proposals/commit-rule-notes-report/commit-rule-notes-report.md)

| Uncertainty | Owner or resolving evidence | | --- | --- | | Whether the change needs files beyond the list below; if so it is out of scope for this plan | Resolved before editing: grep -n 'notes' proposals/aes-planning/rollout/daily_report.py finds no reader today; the per-day line is written in main() (the counts block near line 125) and concerns go through concern() at line 45. This is the only material uncertainty: the change is one function and its use in main(), plus a test, so no other unknown affects the outcome |

### [`proposals/commit-tag-case/commit-tag-case.goal.md`](../proposals/commit-tag-case/commit-tag-case.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/commit-tag-case/commit-tag-case.md` (plan sha256 35f50bb7c0ef24e7a10ca61a983adbac11bf0179c5c624c2e528ecbe0a726265, route inline_prototype). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/commit-tag-case/commit-tag-case.md`](../proposals/commit-tag-case/commit-tag-case.md)

| Uncertainty | Owner or resolving evidence | | --- | --- | | Whether the change needs files beyond the list below; if so it is out of scope for this plan | Resolved before editing: grep -n TAG_RE src/agentic_engineering_system/commit_rule.py: the pattern is defined once (line 81) and used only by the rule. This is the only material uncertainty: the change is one regular expression and its tests, so no other unknown affects the outcome |

### [`proposals/doc-reach-new-docs/PLAN.md`](../proposals/doc-reach-new-docs/PLAN.md)

> **CORE-ACTOR-RESULT-EXAMPLE** (blocking): The plan names the actor it serves, the desired result, and one stable, concrete, user-visible example of that result.

### [`proposals/doc-reach-new-docs/doc-reach-new-docs.goal.md`](../proposals/doc-reach-new-docs/doc-reach-new-docs.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/doc-reach-new-docs/PLAN.md` (plan sha256 6ed76bdc52a47689c2fd6b5f35905958735197acd7c234d93145a363ede5e584, route repair). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/evidence-recorder-counts/README.md`](../proposals/evidence-recorder-counts/README.md)

An agent using `aes evidence record` needs to know whether its tests actually ran. At source revision `431deeb6`, a real pytest file with one skipped assertion returned exit 0 and the default recorder saved SUPPORTS. The reproduction is in `reproduction.before.json`; source inspection alone was not used as runtime proof.

### [`proposals/harness-context/README.md`](../proposals/harness-context/README.md)

Brian wants a harness that follows his rules without making every job carry every procedure. The coordinator keeps the outcome and routes bounded jobs; native specialists load the shared safety core, their role, the target repository authority, and only the procedure activated by that job.

### [`proposals/harness-context/harness-context.goal.md`](../proposals/harness-context/harness-context.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/harness-context/README.md` (plan sha256 adb7a0d79f12cce9fa93a5f54d8aecd9bb99e4a160c6c52fe9c58ce2307f7da0, route coordinated). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/harness-context/native-parity/input/enforced-planning/AGENTS.md`](../proposals/harness-context/native-parity/input/enforced-planning/AGENTS.md)

Status: active

### [`proposals/harness-context/native-parity/input/project-meta/AGENTS.md`](../proposals/harness-context/native-parity/input/project-meta/AGENTS.md)

This repo is the **governance hub** for Brian's project ecosystem: vision docs, enforcement scripts, project index, and operational state.

### [`proposals/harness-context/subagent-research.md`](../proposals/harness-context/subagent-research.md)

Use native workers with an explicit history policy, keep their shared behavior in one source, and verify the effective client settings before claiming parity.

### [`proposals/meeting-claims-true/PLAN.md`](../proposals/meeting-claims-true/PLAN.md)

In the 2026-10-08 "SD - AI Astronaut" meeting (zoom:b5b26a4b0e7daf1a) Brian described his project brains, Company Planning, plan-to-code alignment, feedback system, positions map and ChatGPT backup to Tyler, Dagim, Jawad and Syed. Five read-only checks the same day found most claims partly true and several false. Brian, 2026-10-08: "we need to make all the claims i made true and improve the quality."

### [`proposals/meeting-claims-true/meeting-claims-true.goal.md`](../proposals/meeting-claims-true/meeting-claims-true.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/meeting-claims-true/PLAN.md` (plan sha256 4556c915dc474f8bfdef57a0a7f342a1394d837c7719cc17f0faf06c88c2593d, route coordinated). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/second-brain-evaluation/PLAN.md`](../proposals/second-brain-evaluation/PLAN.md)

<a id="outcome"></a>

### [`proposals/second-brain-evaluation/second-brain-evaluation.goal.md`](../proposals/second-brain-evaluation/second-brain-evaluation.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/second-brain-evaluation/PLAN.md` (plan sha256 f69d9ad3309c6505c2bcb76556911ad5635393d72928e57bf94ba23d80ec7521, route coordinated). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/trace-review-enforcement/plan.md`](../proposals/trace-review-enforcement/plan.md)

Each section below answers the checklist items quoted in it; the gate judges only that section's text. Replace every `TODO(answer ...)` line before running `cli.py check`. Quote values in the front matter: an unquoted ` #` starts a YAML comment and cuts the value.

### [`proposals/trace-review/README.md`](../proposals/trace-review/README.md)

- 2026-10-07: "ok the first thing is that we need aes plans to require trace reviews as part of its planning." - 2026-10-06: "my general principle of maximum observability (although there should be filters/views) and always reviewing full e2e traces of stuff not just the final output."

### [`proposals/trace-review/trace-review.goal.md`](../proposals/trace-review/trace-review.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/trace-review/README.md` (plan sha256 e1db8ded71823d4cc57dccc6b1b2652b784a9c2ecca3d57a2f4bcd15bd4d51ae, route repair). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/worktree-lifecycle/PLAN.md`](../proposals/worktree-lifecycle/PLAN.md)

Authorized scope: repair the existing creation and closeout tools, prove their behavior on a real lane, then resolve existing worktrees individually. Brian activated this mission through /goal on 2026-10-09. Implementation and cleanup wait for native plan adoption; neither has started. No new service, hosting, or paid infrastructure is proposed, and no delivery deadline is assumed.

### [`proposals/worktree-lifecycle/SYSTEM_MODEL.md`](../proposals/worktree-lifecycle/SYSTEM_MODEL.md)

Scope: the existing EP/PM worktree control, a partial shared model rather than the full architectures of either repository. Git, claims and closeout retain their existing owners.

### [`proposals/worktree-lifecycle/VALIDATION.md`](../proposals/worktree-lifecycle/VALIDATION.md)

The repair plan is natively adopted for implementation: `PLAN.adoption-decision.json` records `adopted`, and `PLAN.receipt.json` records **20 passed items, zero not applicable, zero advisory deviations**, at the exact plan digest it binds. `cli.py check` exited 0 before `cli.py adopt` exited 0. The initial draft's 16-item ownership gap is historical, not current admission evidence. Independent writers remain protected; the actual implementation has one sequential writer and no child dispatch.

### [`proposals/worktree-lifecycle/worktree-lifecycle.goal.md`](../proposals/worktree-lifecycle/worktree-lifecycle.goal.md)

Authored through the authoring-goals contract from Brian's active /goal and the adopted [plan](PLAN.md) (sha256 `02cf7f114beb6e342da0498e467144b4bdab702238a13f2aeb11cc0fbb5e8a48`). This file owns mission, loop boundaries and the exact launch condition. The native PM execution cursor will own current slice/progress; the plan owns design, ownership and acceptance. There is no independent progress diary.

### [`proposals/worktree-plan-lookup/worktree-plan-lookup.goal.md`](../proposals/worktree-plan-lookup/worktree-plan-lookup.goal.md)

Generated by company-planning `adopt` from the `goal:` front matter of `proposals/worktree-plan-lookup/worktree-plan-lookup.md` (plan sha256 d0a6d7112756be7456085059133f2c35e2518521e3649a3cc78792677b51efd4, route repair). Do not edit: change the plan and re-adopt it. The plan is the authority for design, work units and evidence; this file holds the goal loop's launcher.

### [`proposals/worktree-plan-lookup/worktree-plan-lookup.md`](../proposals/worktree-plan-lookup/worktree-plan-lookup.md)

Each section below answers the checklist items quoted in it; the gate judges only that section's text. Replace every `TODO(answer ...)` line before running `cli.py check`. Quote values in the front matter: an unquoted ` #` starts a YAML comment and cuts the value.

### [`research/README.md`](../research/README.md)

Status: active Role: research evidence, bounded investigations, and reusable synthesis Authority: analytical; non-normative Lifecycle: retained; sources immutable/append-only where practical

### [`research/investigations/2026-09-16-first-vertical-capability-discovery.md`](../research/investigations/2026-09-16-first-vertical-capability-discovery.md)

Date: 2026-09-16 Status: current investigation

### [`research/investigations/2026-09-16-repository-context-provider-landscape.md`](../research/investigations/2026-09-16-repository-context-provider-landscape.md)

Date: 2026-09-16 Status: current sourcing investigation Capability requirement: `repository.context.resolve`

### [`research/investigations/2026-09-17-aca-tosca-capability-fit-test.md`](../research/investigations/2026-09-17-aca-tosca-capability-fit-test.md)

Test whether Agentic Capability Architecture (ACA) should remain the semantic authority for generic `Capability` / `Requirement` concepts, or whether established TOSCA 2.0 semantics should replace or constrain that vocabulary before AES canonical stubbing.

### [`research/investigations/2026-09-17-aes-evidence-prov-intoto-slsa-fit-test.md`](../research/investigations/2026-09-17-aes-evidence-prov-intoto-slsa-fit-test.md)

Determine which evidence/provenance concepts AES should reuse from standards rather than hand-model, while preserving the genuinely AES-specific semantics around evidence adequacy, freshness, characterization, and gap reconciliation.

### [`research/investigations/2026-09-17-backstage-tosca-sysml-topology-fit.md`](../research/investigations/2026-09-17-backstage-tosca-sysml-topology-fit.md)

AES needs a coherent vocabulary for repositories, software components, APIs, resources, systems, capabilities, requirements, relationships, planned implementation subjects, verification and traceability. Three external families overlap enough that choosing one blindly would be a mistake:

### [`research/investigations/2026-09-17-external-provider-deep-dive-round-2.md`](../research/investigations/2026-09-17-external-provider-deep-dive-round-2.md)

Deepen the first-pass sourcing audit before AES canonical stubbing. The question is not whether one outside project can replace AES. The question is which generic semantics already have an established authority so AES can remain a small residual integration/lifecycle layer.

### [`research/investigations/2026-09-17-external-sourcing-audit-before-canonical-stub.md`](../research/investigations/2026-09-17-external-sourcing-audit-before-canonical-stub.md)

Date: 2026-09-17 Status: **research / pre-stub sourcing gate** Purpose: prevent AES canonical from freezing bespoke internal vocabulary or runtime dependencies where mature standards or forkable OSS already cover the needed semantics.

### [`research/investigations/2026-09-17-opa-aes-policy-fit-test.md`](../research/investigations/2026-09-17-opa-aes-policy-fit-test.md)

Determine whether AES or Enforced Planning should own a generic policy language/evaluator, or whether Open Policy Agent (OPA) should be the default external provider candidate for that layer.

### [`research/investigations/2026-09-17-opa-enforced-planning-policy-probe.md`](../research/investigations/2026-09-17-opa-enforced-planning-policy-probe.md)

Status: research probe; non-normative.

### [`research/investigations/2026-09-17-open-workflow-spec-vs-enforced-planning.md`](../research/investigations/2026-09-17-open-workflow-spec-vs-enforced-planning.md)

Status: research comparison for AES canonical bootstrap Date: 2026-09-17

### [`research/investigations/2026-09-17-ows-enforced-planning-work-graph-fit-test.md`](../research/investigations/2026-09-17-ows-enforced-planning-work-graph-fit-test.md)

Move beyond a landscape comparison by testing a real Enforced Planning work graph against the Open Workflow Specification (OWS) semantic surface.

### [`research/investigations/2026-09-17-prov-intoto-aes-verification-projection-probe.md`](../research/investigations/2026-09-17-prov-intoto-aes-verification-projection-probe.md)

Status: research probe; non-normative.

### [`research/investigations/2026-09-17-scip-planned-subject-fit-test.md`](../research/investigations/2026-09-17-scip-planned-subject-fit-test.md)

Determine whether AES should define its own universal code-symbol vocabulary for functions/classes/modules, or reuse SCIP for realized code identity while retaining only the planning semantics SCIP cannot represent.

### [`research/investigations/2026-09-17-tosca-aca-capability-projection-probe.md`](../research/investigations/2026-09-17-tosca-aca-capability-projection-probe.md)

Status: research probe; non-normative.

### [`research/investigations/README.md`](../research/investigations/README.md)

Bounded questions and findings go here. Each investigation should state its question, sources, findings, uncertainty, and disposition.

### [`research/sources/README.md`](../research/sources/README.md)

Preserve exact references/captures used by investigations. Initial external sources include the standalone `wiki_methodology` architecture and incumbent AES/planning/ACA/Data Contracts repositories. Do not duplicate large upstream repositories here.

### [`research/synthesis/2026-09-17-ac17-salvage-for-aligned-normative-component-planning.md`](../research/synthesis/2026-09-17-ac17-salvage-for-aligned-normative-component-planning.md)

Status: research synthesis; non-normative donor analysis.

### [`research/synthesis/2026-09-17-aes-semantic-ownership-crosswalk.md`](../research/synthesis/2026-09-17-aes-semantic-ownership-crosswalk.md)

This crosswalk determines which conceptual families AES should reuse, adapt, reference, or own before the canonical repository skeleton is materialized.

### [`research/synthesis/2026-09-17-external-document-semantics-for-normative-model.md`](../research/synthesis/2026-09-17-external-document-semantics-for-normative-model.md)

Use established requirements, architecture-description, and executable-specification semantics to sharpen the AES documentation model without importing a large document taxonomy or making external standards runtime dependencies.

### [`research/synthesis/2026-09-17-fresh-agent-handoff.md`](../research/synthesis/2026-09-17-fresh-agent-handoff.md)

Date: 2026-09-17

### [`research/synthesis/2026-09-17-normative-component-alignment-dogfood-checkpoint.md`](../research/synthesis/2026-09-17-normative-component-alignment-dogfood-checkpoint.md)

Status: **provisional blueprint recorded; structural probe observed; architecture adoption and runtime behavior unverified**

### [`research/synthesis/2026-09-17-proposed-aes-canonical-skeleton-after-sourcing.md`](../research/synthesis/2026-09-17-proposed-aes-canonical-skeleton-after-sourcing.md)

Status: **bootstrap topology draft — not yet an implementation freeze**

### [`research/synthesis/2026-09-17-source-local-context-dogfood-result.md`](../research/synthesis/2026-09-17-source-local-context-dogfood-result.md)

Status: research synthesis; **BP-D1 pilot-supported, not accepted architecture**

### [`research/synthesis/2026-09-26-inside-success-aes-harvest.md`](../research/synthesis/2026-09-26-inside-success-aes-harvest.md)

Status: research synthesis, non-normative. Written 2026-09-26 for [Decision 0011](../../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md), which archives the predecessor repository. Nothing here is adopted by being listed. Each item enters v0.2 only through the donor re-entry rule (`proposals/aes-v0.2-greenfield/05-donor-reentry.md`) and `aes plan`, and only when its **trigger** is observed on a real consumer.

### [`research/synthesis/2026-09-28-legacy-idea-harvest/README.md`](../research/synthesis/2026-09-28-legacy-idea-harvest/README.md)

Status: research synthesis, non-normative. Written 2026-09-28 at Brian's request ("an in-depth investigation for ideas", not code reuse). This harvest adopts nothing. As with the [2026-09-26 Inside Success AES harvest](../2026-09-26-inside-success-aes-harvest.md), an idea enters v0.2 only through the donor re-entry rule (`proposals/aes-v0.2-greenfield/05-donor-reentry.md`) and `aes plan`, and only when its trigger shows up on a real consumer.

### [`research/synthesis/2026-09-28-legacy-idea-harvest/aes-archived.md`](../research/synthesis/2026-09-28-legacy-idea-harvest/aes-archived.md)

Read-only idea harvest, 2026-09-27. Nothing here is adopted by being listed; each item enters v0.2 only through the donor re-entry rule and `aes plan`, when its trigger shows up on a real consumer.

### [`research/synthesis/2026-09-28-legacy-idea-harvest/company-planning.md`](../research/synthesis/2026-09-28-legacy-idea-harvest/company-planning.md)

Status: read-only idea harvest, non-normative. Nothing listed here is adopted by being listed; each item enters AES v0.2 only through the donor re-entry rule and `aes plan`, and only when its trigger is observed on a real consumer.

### [`research/synthesis/2026-09-28-legacy-idea-harvest/ecosystem-ops.md`](../research/synthesis/2026-09-28-legacy-idea-harvest/ecosystem-ops.md)

Read-only idea harvest for AES v0.2, written 2026-09-28. Nothing here is adopted by being listed. Does not repeat `research/synthesis/2026-09-26-inside-success-aes-harvest.md`; where an item here is a stronger version of one of its items, that item's number is given as "cf. #N".

### [`research/synthesis/2026-09-28-legacy-idea-harvest/enforced-planning.md`](../research/synthesis/2026-09-28-legacy-idea-harvest/enforced-planning.md)

Source: `BrianMills2718/enforced-planning`, local `/home/brian/code/enforced-planning` at `git rev-parse HEAD` = `9963dc41fcdaaa90f857d66a637fad745cda3b09` (1,329 commits, 2026-04 to 2026-09-26). Read-only sweep on 2026-09-27: plan index and status lines (146 files in `docs/plans/`), ADRs 0002/0004/0005, `ISSUES.md`, `docs/evidence/`, targeted code listing, and `git log` for reverts/removals/escape-hatch rates. Every path below was checked to exist at that revision. Paths are relative to the repo root.

### [`research/synthesis/2026-09-28-legacy-idea-harvest/hooks-instructions.md`](../research/synthesis/2026-09-28-legacy-idea-harvest/hooks-instructions.md)

Read-only idea harvest for AES v0.2 (`agentic-engineering-system-canonical` @ `0d51390`). Scope excludes what `research/synthesis/2026-09-26-inside-success-aes-harvest.md` already covers (items 9-12, 14; lessons B6, B9, B10). Where a source here is stronger or contradicts one of those items, the row says so.

### [`research/synthesis/2026-09-28-legacy-idea-harvest/project-meta.md`](../research/synthesis/2026-09-28-legacy-idea-harvest/project-meta.md)

- Source repo: `BrianMills2718/project-meta`, revision `0dcc574ebfcc47fa9815aeaf7e5786b2884392a1` (7,226 commits), read 2026-09-27/28. - Method: indexes and headings first, then targeted sections; GitHub concern issues read with `gh` (read-only); git log checked for landed vs abandoned work. All paths are relative to the repo root and were checked to exist at this revision. `#NNNN` means a `BrianMills2718/project-meta` GitHub issue or PR. - Deduplication: checked against `research/synthesis/2026-09-26-inside-success-aes-harvest.md` (cited as "IS-AES #n" for ideas and "IS-AES B.n" for stall lessons). Nothing here repeats that harvest unless it is a stronger or different version, and those rows say so.

### [`research/synthesis/ac16-ac17-lessons-for-aes.md`](../research/synthesis/ac16-ac17-lessons-for-aes.md)

Status: research synthesis; non-normative suggestions only.

### [`research/synthesis/aes-evidence-characterization-and-context-suggestions.md`](../research/synthesis/aes-evidence-characterization-and-context-suggestions.md)

Status: research synthesis; non-normative suggestions only.

### [`research/synthesis/code-map-v4-salvage-for-aes.md`](../research/synthesis/code-map-v4-salvage-for-aes.md)

Status: research synthesis; non-normative candidate dispositions only.

### [`research/synthesis/fluid-governance-selective-salvage.md`](../research/synthesis/fluid-governance-selective-salvage.md)

Status: research synthesis; candidate dispositions only. This document does not adopt an implementation, transfer authority, or change the canonical AES system boundary.

### [`research/synthesis/incumbent-capability-inventory.md`](../research/synthesis/incumbent-capability-inventory.md)

Status: research synthesis; candidate dispositions only. This file does not transfer ownership or select a runtime dependency by itself.

### [`research/synthesis/observation-to-action-advice-for-aes.md`](../research/synthesis/observation-to-action-advice-for-aes.md)

Status: research synthesis / tentative advice

### [`research/synthesis/representation-review-and-epistemic-surface-suggestions-for-aes.md`](../research/synthesis/representation-review-and-epistemic-surface-suggestions-for-aes.md)

Status: research synthesis; non-normative candidate dispositions only.

### [`scripts/README.md`](../scripts/README.md)

Repo-local validation/generation/maintenance tooling belongs here once required by accepted plans. Product/runtime implementation should remain in declared implementation roots derived by planning.

### [`scripts/hive/README.md`](../scripts/hive/README.md)

The hive (Paperclip agents, dashboard, controls, readout) moved to [BrianMills2718/personal-vps](https://github.com/BrianMills2718/personal-vps) on 2026-10-07: scripts in `hive/`, plans in `proposals/hive-brain-v1/` and `proposals/hive-hardening/`.

### [`scripts/learning_loop/systemd/README.md`](../scripts/learning_loop/systemd/README.md)

Four timers run the agent feedback loop. Start page for the whole loop: [guide.html](../../../proposals/aes-learning-loop/review-page/guide.html).

### [`src/agentic_engineering_system/planning_protocol.md`](../src/agentic_engineering_system/planning_protocol.md)

For a human or agent changing an AES project's target (`ART-PLANNING-PROTOCOL`, `SC-GF-004`). The target is `.aes/target.yaml`; a change to it is written as a proposal, validated, accepted, and committed before any code it plans is written. Implementation follows the accepted target; it never edits the target on the side.

### [`wiki/index.md`](../wiki/index.md)

This is the progressive-disclosure front door for the canonical AES convergence project. It is a derived navigation surface, not a native authority. Follow links to the owning architecture, decision, plan, evidence, or code before making consequential claims.

## Fixture (4)

### [`tests/greenfield/fixtures/whygame5-54043e2/.aes/project.yaml`](../tests/greenfield/fixtures/whygame5-54043e2/.aes/project.yaml)

_No source-local artifact summary._

### [`tests/greenfield/fixtures/whygame5-54043e2/.aes/target.yaml`](../tests/greenfield/fixtures/whygame5-54043e2/.aes/target.yaml)

_No source-local artifact summary._

### [`tests/greenfield/fixtures/whygame5-54043e2/README`](../tests/greenfield/fixtures/whygame5-54043e2/README)

_No source-local artifact summary._

### [`tests/greenfield/fixtures/whygame5-proposal-runner.yaml`](../tests/greenfield/fixtures/whygame5-proposal-runner.yaml)

_No source-local artifact summary._

## Generated (9)

### [`generated/README.md`](README.md)

Rebuildable derived output only. Nothing here is an independent authority. Safe deletion/rebuild is the default expectation once generators exist.

### [`generated/bootstrap-normative/architecture-realization.minimal.pilot.yaml`](bootstrap-normative/architecture-realization.minimal.pilot.yaml)

_No source-local artifact summary._

### [`generated/bootstrap-normative/system.pilot.yaml`](bootstrap-normative/system.pilot.yaml)

_No source-local artifact summary._

### [`generated/bootstrap-normative/view-bundle.md`](bootstrap-normative/view-bundle.md)

> Generated projection. Not normative authority.

### [`generated/docstring_wiki.md`](docstring_wiki.md)

_Generated wiki projection; self-content intentionally omitted._

### [`generated/docstring_wiki.md`](docstring_wiki.md)

_Generated wiki projection; self-content intentionally omitted._

### [`generated/docstring_wiki.md`](docstring_wiki.md)

_Generated wiki projection; self-content intentionally omitted._

### [`generated/repository-context/BrianMills2718__data-contracts/90c38998e8141bd07e49a77a49ec417aa29beee0/context.json`](repository-context/BrianMills2718__data-contracts/90c38998e8141bd07e49a77a49ec417aa29beee0/context.json)

_No source-local artifact summary._

### [`generated/repository-context/BrianMills2718__data-contracts/90c38998e8141bd07e49a77a49ec417aa29beee0/index.html`](repository-context/BrianMills2718__data-contracts/90c38998e8141bd07e49a77a49ec417aa29beee0/index.html)

_No source-local artifact summary._

## Archive (9)

### [`archive/v0.1-placeholders/README.md`](../archive/v0.1-placeholders/README.md)

Disposition: **historical**. These eight `component.placeholder.yaml` files are v0.1 planning placeholders. Each reserved a directory under `src/agentic_engineering_system/` for a v0.1 component that was never built; no directory ever held code (at archive time each held only this one file). They are retained for history, not deleted.

### [`archive/v0.1-placeholders/capability_sourcing/component.placeholder.yaml`](../archive/v0.1-placeholders/capability_sourcing/component.placeholder.yaml)

_No source-local artifact summary._

### [`archive/v0.1-placeholders/evidence_assessment/component.placeholder.yaml`](../archive/v0.1-placeholders/evidence_assessment/component.placeholder.yaml)

_No source-local artifact summary._

### [`archive/v0.1-placeholders/execution/component.placeholder.yaml`](../archive/v0.1-placeholders/execution/component.placeholder.yaml)

_No source-local artifact summary._

### [`archive/v0.1-placeholders/gap_reconciliation/component.placeholder.yaml`](../archive/v0.1-placeholders/gap_reconciliation/component.placeholder.yaml)

_No source-local artifact summary._

### [`archive/v0.1-placeholders/learning/component.placeholder.yaml`](../archive/v0.1-placeholders/learning/component.placeholder.yaml)

_No source-local artifact summary._

### [`archive/v0.1-placeholders/normative_context/component.placeholder.yaml`](../archive/v0.1-placeholders/normative_context/component.placeholder.yaml)

_No source-local artifact summary._

### [`archive/v0.1-placeholders/planning/component.placeholder.yaml`](../archive/v0.1-placeholders/planning/component.placeholder.yaml)

_No source-local artifact summary._

### [`archive/v0.1-placeholders/policy_control/component.placeholder.yaml`](../archive/v0.1-placeholders/policy_control/component.placeholder.yaml)

_No source-local artifact summary._

## Other (544)

### [`.aes/commit_rule.yaml`](../.aes/commit_rule.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-ADOPT-03dba8f8.yaml`](../.aes/observations/OBS-ADOPT-03dba8f8.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-ADOPT-e101ef70.yaml`](../.aes/observations/OBS-ADOPT-e101ef70.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AES-CLEAN-USER-0503735.yaml`](../.aes/observations/OBS-AES-CLEAN-USER-0503735.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AES-CLEAN-USER-2d3486b.yaml`](../.aes/observations/OBS-AES-CLEAN-USER-2d3486b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AES-CLEAN-USER-3dd2b9a.yaml`](../.aes/observations/OBS-AES-CLEAN-USER-3dd2b9a.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AES-CLEAN-USER-d89fe2e.yaml`](../.aes/observations/OBS-AES-CLEAN-USER-d89fe2e.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AES-CONTEXT-AB-2509ea4.yaml`](../.aes/observations/OBS-AES-CONTEXT-AB-2509ea4.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AES-CONTEXT-AB-RETAINED-377e9707.yaml`](../.aes/observations/OBS-AES-CONTEXT-AB-RETAINED-377e9707.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AES-PROBE0-CONTEXT-AB.yaml`](../.aes/observations/OBS-AES-PROBE0-CONTEXT-AB.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AES-WG5-LIFECYCLE-38df3e5.yaml`](../.aes/observations/OBS-AES-WG5-LIFECYCLE-38df3e5.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AES-WG5-LIFECYCLE.yaml`](../.aes/observations/OBS-AES-WG5-LIFECYCLE.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-08f53436.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-08f53436.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-247c56f7.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-247c56f7.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-40c43386.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-40c43386.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-42765501.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-42765501.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-4ee979fe.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-4ee979fe.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-5978e55e.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-5978e55e.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-5ba9b30d.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-5ba9b30d.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-68450fe8.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-68450fe8.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-72925dc1.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-72925dc1.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-8ace3cd8.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-8ace3cd8.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-9fe9b32a.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-9fe9b32a.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-RUNTIME-08f5343.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-RUNTIME-08f5343.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-RUNTIME-4276550.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-RUNTIME-4276550.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-RUNTIME-72925dc.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-RUNTIME-72925dc.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-RUNTIME-8ace3cd.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-RUNTIME-8ace3cd.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-RUNTIME-b023fb0.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-RUNTIME-b023fb0.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-RUNTIME-b91592b.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-RUNTIME-b91592b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-RUNTIME-ca78424.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-RUNTIME-ca78424.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-b023fb02.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-b023fb02.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-b7a54252.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-b7a54252.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-bbde5185.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-bbde5185.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-COMMIT-RULE-c860a860.yaml`](../.aes/observations/OBS-AP-COMMIT-RULE-c860a860.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-PLAN-RECEIPT-42765501.yaml`](../.aes/observations/OBS-AP-PLAN-RECEIPT-42765501.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-PLAN-RECEIPT-72925dc1.yaml`](../.aes/observations/OBS-AP-PLAN-RECEIPT-72925dc1.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-AP-PLAN-RECEIPT-8ace3cd8.yaml`](../.aes/observations/OBS-AP-PLAN-RECEIPT-8ace3cd8.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-CHARACTERIZE-42765501.yaml`](../.aes/observations/OBS-GF-CHARACTERIZE-42765501.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-CHARACTERIZE-449cd54b.yaml`](../.aes/observations/OBS-GF-CHARACTERIZE-449cd54b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-CHARACTERIZE-61e1edbf.yaml`](../.aes/observations/OBS-GF-CHARACTERIZE-61e1edbf.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-CHARACTERIZE-62fe041b.yaml`](../.aes/observations/OBS-GF-CHARACTERIZE-62fe041b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-CHARACTERIZE-c5ea63d0.yaml`](../.aes/observations/OBS-GF-CHARACTERIZE-c5ea63d0.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-CHARACTERIZE-cb226ba7.yaml`](../.aes/observations/OBS-GF-CHARACTERIZE-cb226ba7.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-CONTEXT-STRUCTURAL-42765501.yaml`](../.aes/observations/OBS-GF-CONTEXT-STRUCTURAL-42765501.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-CONTEXT-STRUCTURAL-449cd54b.yaml`](../.aes/observations/OBS-GF-CONTEXT-STRUCTURAL-449cd54b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-CONTEXT-STRUCTURAL-61e1edbf.yaml`](../.aes/observations/OBS-GF-CONTEXT-STRUCTURAL-61e1edbf.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-CONTEXT-STRUCTURAL-62fe041b.yaml`](../.aes/observations/OBS-GF-CONTEXT-STRUCTURAL-62fe041b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-CONTEXT-STRUCTURAL-c5ea63d0.yaml`](../.aes/observations/OBS-GF-CONTEXT-STRUCTURAL-c5ea63d0.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-CONTEXT-STRUCTURAL-cb226ba7.yaml`](../.aes/observations/OBS-GF-CONTEXT-STRUCTURAL-cb226ba7.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-DISTRIBUTION-INSTALL-42765501.yaml`](../.aes/observations/OBS-GF-DISTRIBUTION-INSTALL-42765501.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-DISTRIBUTION-INSTALL-449cd54b.yaml`](../.aes/observations/OBS-GF-DISTRIBUTION-INSTALL-449cd54b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-DISTRIBUTION-INSTALL-4546d179.yaml`](../.aes/observations/OBS-GF-DISTRIBUTION-INSTALL-4546d179.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-DISTRIBUTION-INSTALL-61e1edbf.yaml`](../.aes/observations/OBS-GF-DISTRIBUTION-INSTALL-61e1edbf.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-DISTRIBUTION-INSTALL-62fe041b.yaml`](../.aes/observations/OBS-GF-DISTRIBUTION-INSTALL-62fe041b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-DISTRIBUTION-INSTALL-c5ea63d0.yaml`](../.aes/observations/OBS-GF-DISTRIBUTION-INSTALL-c5ea63d0.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-DISTRIBUTION-INSTALL-cb226ba7.yaml`](../.aes/observations/OBS-GF-DISTRIBUTION-INSTALL-cb226ba7.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-DISTRIBUTION-INSTALL-d89fe2e3.yaml`](../.aes/observations/OBS-GF-DISTRIBUTION-INSTALL-d89fe2e3.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-EVIDENCE-42765501.yaml`](../.aes/observations/OBS-GF-EVIDENCE-42765501.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-EVIDENCE-449cd54b.yaml`](../.aes/observations/OBS-GF-EVIDENCE-449cd54b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-EVIDENCE-61e1edbf.yaml`](../.aes/observations/OBS-GF-EVIDENCE-61e1edbf.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-EVIDENCE-62fe041b.yaml`](../.aes/observations/OBS-GF-EVIDENCE-62fe041b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-EVIDENCE-CONTROLS-42765501.yaml`](../.aes/observations/OBS-GF-EVIDENCE-CONTROLS-42765501.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-EVIDENCE-CONTROLS-449cd54b.yaml`](../.aes/observations/OBS-GF-EVIDENCE-CONTROLS-449cd54b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-EVIDENCE-CONTROLS-61e1edbf.yaml`](../.aes/observations/OBS-GF-EVIDENCE-CONTROLS-61e1edbf.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-EVIDENCE-CONTROLS-62fe041b.yaml`](../.aes/observations/OBS-GF-EVIDENCE-CONTROLS-62fe041b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-EVIDENCE-CONTROLS-c5ea63d0.yaml`](../.aes/observations/OBS-GF-EVIDENCE-CONTROLS-c5ea63d0.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-EVIDENCE-CONTROLS-cb226ba7.yaml`](../.aes/observations/OBS-GF-EVIDENCE-CONTROLS-cb226ba7.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-EVIDENCE-c5ea63d0.yaml`](../.aes/observations/OBS-GF-EVIDENCE-c5ea63d0.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-EVIDENCE-cb226ba7.yaml`](../.aes/observations/OBS-GF-EVIDENCE-cb226ba7.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-INIT-UNIT-42765501.yaml`](../.aes/observations/OBS-GF-INIT-UNIT-42765501.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-INIT-UNIT-449cd54b.yaml`](../.aes/observations/OBS-GF-INIT-UNIT-449cd54b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-INIT-UNIT-61e1edbf.yaml`](../.aes/observations/OBS-GF-INIT-UNIT-61e1edbf.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-INIT-UNIT-62fe041b.yaml`](../.aes/observations/OBS-GF-INIT-UNIT-62fe041b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-INIT-UNIT-c5ea63d0.yaml`](../.aes/observations/OBS-GF-INIT-UNIT-c5ea63d0.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-INIT-UNIT-cb226ba7.yaml`](../.aes/observations/OBS-GF-INIT-UNIT-cb226ba7.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-PLANNING-42765501.yaml`](../.aes/observations/OBS-GF-PLANNING-42765501.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-PLANNING-449cd54b.yaml`](../.aes/observations/OBS-GF-PLANNING-449cd54b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-PLANNING-61e1edbf.yaml`](../.aes/observations/OBS-GF-PLANNING-61e1edbf.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-PLANNING-62fe041b.yaml`](../.aes/observations/OBS-GF-PLANNING-62fe041b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-PLANNING-c5ea63d0.yaml`](../.aes/observations/OBS-GF-PLANNING-c5ea63d0.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-PLANNING-cb226ba7.yaml`](../.aes/observations/OBS-GF-PLANNING-cb226ba7.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-RECONCILE-42765501.yaml`](../.aes/observations/OBS-GF-RECONCILE-42765501.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-RECONCILE-449cd54b.yaml`](../.aes/observations/OBS-GF-RECONCILE-449cd54b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-RECONCILE-61e1edbf.yaml`](../.aes/observations/OBS-GF-RECONCILE-61e1edbf.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-RECONCILE-62fe041b.yaml`](../.aes/observations/OBS-GF-RECONCILE-62fe041b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-RECONCILE-c5ea63d0.yaml`](../.aes/observations/OBS-GF-RECONCILE-c5ea63d0.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-RECONCILE-cb226ba7.yaml`](../.aes/observations/OBS-GF-RECONCILE-cb226ba7.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-RECORDS-42765501.yaml`](../.aes/observations/OBS-GF-RECORDS-42765501.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-RECORDS-449cd54b.yaml`](../.aes/observations/OBS-GF-RECORDS-449cd54b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-RECORDS-61e1edbf.yaml`](../.aes/observations/OBS-GF-RECORDS-61e1edbf.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-RECORDS-c5ea63d0.yaml`](../.aes/observations/OBS-GF-RECORDS-c5ea63d0.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-RECORDS-cb226ba7.yaml`](../.aes/observations/OBS-GF-RECORDS-cb226ba7.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-SELF-GOVERNANCE-42765501.yaml`](../.aes/observations/OBS-GF-SELF-GOVERNANCE-42765501.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-SELF-GOVERNANCE-449cd54b.yaml`](../.aes/observations/OBS-GF-SELF-GOVERNANCE-449cd54b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-SELF-GOVERNANCE-61e1edbf.yaml`](../.aes/observations/OBS-GF-SELF-GOVERNANCE-61e1edbf.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-SELF-GOVERNANCE-62fe041b.yaml`](../.aes/observations/OBS-GF-SELF-GOVERNANCE-62fe041b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-SELF-GOVERNANCE-c5ea63d0.yaml`](../.aes/observations/OBS-GF-SELF-GOVERNANCE-c5ea63d0.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-SELF-GOVERNANCE-cb226ba7.yaml`](../.aes/observations/OBS-GF-SELF-GOVERNANCE-cb226ba7.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-TOPOLOGY-42765501.yaml`](../.aes/observations/OBS-GF-TOPOLOGY-42765501.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-TOPOLOGY-449cd54b.yaml`](../.aes/observations/OBS-GF-TOPOLOGY-449cd54b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-TOPOLOGY-61e1edbf.yaml`](../.aes/observations/OBS-GF-TOPOLOGY-61e1edbf.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-TOPOLOGY-62fe041b.yaml`](../.aes/observations/OBS-GF-TOPOLOGY-62fe041b.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-TOPOLOGY-c5ea63d0.yaml`](../.aes/observations/OBS-GF-TOPOLOGY-c5ea63d0.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-GF-TOPOLOGY-cb226ba7.yaml`](../.aes/observations/OBS-GF-TOPOLOGY-cb226ba7.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-TR-SOURCE-INDEPENDENT-REVIEW.yaml`](../.aes/observations/OBS-TR-SOURCE-INDEPENDENT-REVIEW.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-TR-SOURCE-c0610191.yaml`](../.aes/observations/OBS-TR-SOURCE-c0610191.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-TRACE-REVIEW-42765501.yaml`](../.aes/observations/OBS-TRACE-REVIEW-42765501.yaml)

_No source-local artifact summary._

### [`.aes/observations/OBS-TRACE-REVIEW-7a637486.yaml`](../.aes/observations/OBS-TRACE-REVIEW-7a637486.yaml)

_No source-local artifact summary._

### [`.aes/planning.yaml`](../.aes/planning.yaml)

_No source-local artifact summary._

### [`.aes/plans/PLAN-AES-ACCEPT-RECEIPT.yaml`](../.aes/plans/PLAN-AES-ACCEPT-RECEIPT.yaml)

_No source-local artifact summary._

### [`.aes/plans/PLAN-AES-ADOPT-EXISTING.yaml`](../.aes/plans/PLAN-AES-ADOPT-EXISTING.yaml)

_No source-local artifact summary._

### [`.aes/plans/PLAN-AES-ARCHIVE-V01-PLACEHOLDERS.yaml`](../.aes/plans/PLAN-AES-ARCHIVE-V01-PLACEHOLDERS.yaml)

_No source-local artifact summary._

### [`.aes/plans/PLAN-AES-COMMIT-RULE.yaml`](../.aes/plans/PLAN-AES-COMMIT-RULE.yaml)

_No source-local artifact summary._

### [`.aes/plans/PLAN-AES-RESCOPE-CONTEXT-AB.yaml`](../.aes/plans/PLAN-AES-RESCOPE-CONTEXT-AB.yaml)

_No source-local artifact summary._

### [`.aes/plans/PLAN-AES-SELF-GOVERN.yaml`](../.aes/plans/PLAN-AES-SELF-GOVERN.yaml)

_No source-local artifact summary._

### [`.aes/plans/PLAN-AES-SOURCE-BOUND-TRACE-REVIEW.yaml`](../.aes/plans/PLAN-AES-SOURCE-BOUND-TRACE-REVIEW.yaml)

_No source-local artifact summary._

### [`.aes/plans/PLAN-AES-TRACE-REVIEW.yaml`](../.aes/plans/PLAN-AES-TRACE-REVIEW.yaml)

_No source-local artifact summary._

### [`.aes/project.yaml`](../.aes/project.yaml)

_No source-local artifact summary._

### [`.aes/target.yaml`](../.aes/target.yaml)

_No source-local artifact summary._

### [`.agentic/relationships.yaml`](../.agentic/relationships.yaml)

_No source-local artifact summary._

### [`.agentic/repo.yaml`](../.agentic/repo.yaml)

_No source-local artifact summary._

### [`.claude/hooks/check-hook-enabled.sh`](../.claude/hooks/check-hook-enabled.sh)

_No source-local artifact summary._

### [`.claude/hooks/gate-edit.sh`](../.claude/hooks/gate-edit.sh)

_No source-local artifact summary._

### [`.claude/hooks/notify-coordination-messages.sh`](../.claude/hooks/notify-coordination-messages.sh)

_No source-local artifact summary._

### [`.claude/hooks/reconcile-canonical-locks.sh`](../.claude/hooks/reconcile-canonical-locks.sh)

_No source-local artifact summary._

### [`.claude/hooks/track-reads.sh`](../.claude/hooks/track-reads.sh)

_No source-local artifact summary._

### [`.claude/hooks/worktree-coordination/check-hook-enabled.sh`](../.claude/hooks/worktree-coordination/check-hook-enabled.sh)

_No source-local artifact summary._

### [`.claude/hooks/worktree-coordination/enforce-make-merge.sh`](../.claude/hooks/worktree-coordination/enforce-make-merge.sh)

_No source-local artifact summary._

### [`.claude/settings.json`](../.claude/settings.json)

_No source-local artifact summary._

### [`.codex/hooks.json`](../.codex/hooks.json)

_No source-local artifact summary._

### [`.codex/hooks/enforce-make-merge.sh`](../.codex/hooks/enforce-make-merge.sh)

_No source-local artifact summary._

### [`.codex/hooks/notify-coordination-messages.sh`](../.codex/hooks/notify-coordination-messages.sh)

_No source-local artifact summary._

### [`.company-planning/history/036a4c0aa1ce7c84-r4.json`](../.company-planning/history/036a4c0aa1ce7c84-r4.json)

_No source-local artifact summary._

### [`.company-planning/history/12a72d10301d23eb-r3.json`](../.company-planning/history/12a72d10301d23eb-r3.json)

_No source-local artifact summary._

### [`.company-planning/history/188d10837dd7e08e-r3.disposition.json`](../.company-planning/history/188d10837dd7e08e-r3.disposition.json)

_No source-local artifact summary._

### [`.company-planning/history/188d10837dd7e08e-r3.json`](../.company-planning/history/188d10837dd7e08e-r3.json)

_No source-local artifact summary._

### [`.githooks/commit-msg`](../.githooks/commit-msg)

_No source-local artifact summary._

### [`.githooks/pre-commit`](../.githooks/pre-commit)

_No source-local artifact summary._

### [`.github/workflows/slice-1-tests.yml`](../.github/workflows/slice-1-tests.yml)

_No source-local artifact summary._

### [`.gitignore`](../.gitignore)

_No source-local artifact summary._

### [`.md-file-cap.yaml`](../.md-file-cap.yaml)

_No source-local artifact summary._

### [`Makefile`](../Makefile)

_No source-local artifact summary._

### [`contracts/agent-router/handoff.v1.schema.json`](../contracts/agent-router/handoff.v1.schema.json)

_No source-local artifact summary._

### [`contracts/agent-router/profile.v1.schema.json`](../contracts/agent-router/profile.v1.schema.json)

_No source-local artifact summary._

### [`contracts/learning-loop/feedback-report.v1.schema.json`](../contracts/learning-loop/feedback-report.v1.schema.json)

_No source-local artifact summary._

### [`contracts/pr-review-signoff.schema.json`](../contracts/pr-review-signoff.schema.json)

_No source-local artifact summary._

### [`datasets/learning-loop/experiments/2026-10-02-question-design/gt.tsv`](../datasets/learning-loop/experiments/2026-10-02-question-design/gt.tsv)

_No source-local artifact summary._

### [`datasets/learning-loop/experiments/2026-10-02-question-design/hier_holdout.json`](../datasets/learning-loop/experiments/2026-10-02-question-design/hier_holdout.json)

_No source-local artifact summary._

### [`datasets/learning-loop/experiments/2026-10-02-question-design/hier_tuned.json`](../datasets/learning-loop/experiments/2026-10-02-question-design/hier_tuned.json)

_No source-local artifact summary._

### [`datasets/learning-loop/experiments/2026-10-02-question-design/holdout_gt.tsv`](../datasets/learning-loop/experiments/2026-10-02-question-design/holdout_gt.tsv)

_No source-local artifact summary._

### [`datasets/learning-loop/experiments/2026-10-02-question-design/holdout_ids.json`](../datasets/learning-loop/experiments/2026-10-02-question-design/holdout_ids.json)

_No source-local artifact summary._

### [`datasets/learning-loop/experiments/2026-10-02-question-design/holdout_out.json`](../datasets/learning-loop/experiments/2026-10-02-question-design/holdout_out.json)

_No source-local artifact summary._

### [`datasets/learning-loop/experiments/2026-10-02-question-design/ml_out.jsonl`](../datasets/learning-loop/experiments/2026-10-02-question-design/ml_out.jsonl)

_No source-local artifact summary._

### [`datasets/learning-loop/experiments/2026-10-02-question-design/sc_out.jsonl`](../datasets/learning-loop/experiments/2026-10-02-question-design/sc_out.jsonl)

_No source-local artifact summary._

### [`datasets/learning-loop/experiments/2026-10-02-question-design/synthetic.json`](../datasets/learning-loop/experiments/2026-10-02-question-design/synthetic.json)

_No source-local artifact summary._

### [`datasets/learning-loop/experiments/2026-10-02-question-design/v2_out.json`](../datasets/learning-loop/experiments/2026-10-02-question-design/v2_out.json)

_No source-local artifact summary._

### [`datasets/learning-loop/legacy-learnings-labelled-v2.jsonl`](../datasets/learning-loop/legacy-learnings-labelled-v2.jsonl)

_No source-local artifact summary._

### [`enforced_planning/worktree_lifecycle.yaml`](../enforced_planning/worktree_lifecycle.yaml)

_No source-local artifact summary._

### [`evals/plan-002/case_manifest.json`](../evals/plan-002/case_manifest.json)

_No source-local artifact summary._

### [`evidence/bootstrap-alignment/architecture-realization-schema-observation-001.json`](../evidence/bootstrap-alignment/architecture-realization-schema-observation-001.json)

_No source-local artifact summary._

### [`evidence/bootstrap-alignment/blueprint-structural-observation-001.json`](../evidence/bootstrap-alignment/blueprint-structural-observation-001.json)

_No source-local artifact summary._

### [`evidence/bootstrap-alignment/company-planning-profile-conformance-001.json`](../evidence/bootstrap-alignment/company-planning-profile-conformance-001.json)

_No source-local artifact summary._

### [`evidence/bootstrap-alignment/current-profile-path-coherence-001.json`](../evidence/bootstrap-alignment/current-profile-path-coherence-001.json)

_No source-local artifact summary._

### [`evidence/bootstrap-alignment/normative-record-view-dogfood-001.json`](../evidence/bootstrap-alignment/normative-record-view-dogfood-001.json)

_No source-local artifact summary._

### [`evidence/bootstrap-alignment/repository-context-source-local-observation-001.json`](../evidence/bootstrap-alignment/repository-context-source-local-observation-001.json)

_No source-local artifact summary._

### [`evidence/bootstrap-alignment/reserved-component-tree-observation-001.json`](../evidence/bootstrap-alignment/reserved-component-tree-observation-001.json)

_No source-local artifact summary._

### [`evidence/greenfield/context-ab-2026-09-25/arm-a-fix.patch`](../evidence/greenfield/context-ab-2026-09-25/arm-a-fix.patch)

_No source-local artifact summary._

### [`evidence/greenfield/context-ab-2026-09-25/arm-b-fix.patch`](../evidence/greenfield/context-ab-2026-09-25/arm-b-fix.patch)

_No source-local artifact summary._

### [`evidence/plan-001/320991b96a3e3aaa15aa8ba05817a7eee1c52603/verification-summary.json`](../evidence/plan-001/320991b96a3e3aaa15aa8ba05817a7eee1c52603/verification-summary.json)

_No source-local artifact summary._

### [`evidence/plan-001/96fcf5e89ba98ad9ff278ec536a98c308cda3fe1/verification-summary.json`](../evidence/plan-001/96fcf5e89ba98ad9ff278ec536a98c308cda3fe1/verification-summary.json)

_No source-local artifact summary._

### [`evidence/plan-001/evidence-carry-forward-2026-09-18.json`](../evidence/plan-001/evidence-carry-forward-2026-09-18.json)

_No source-local artifact summary._

### [`evidence/plan-001/verification-boundary-correction-2026-09-18.json`](../evidence/plan-001/verification-boundary-correction-2026-09-18.json)

_No source-local artifact summary._

### [`evidence/provider-provenance/enforced-planning-install-2026-09-18.json`](../evidence/provider-provenance/enforced-planning-install-2026-09-18.json)

_No source-local artifact summary._

### [`hooks/pre-push`](../hooks/pre-push)

_No source-local artifact summary._

### [`meta-process.yaml`](../meta-process.yaml)

_No source-local artifact summary._

### [`meta-process/templates/agents.md.template`](../meta-process/templates/agents.md.template)

_No source-local artifact summary._

### [`proposals/aes-adopt-existing/activation-facts.json`](../proposals/aes-adopt-existing/activation-facts.json)

_No source-local artifact summary._

### [`proposals/aes-adopt-existing/checklist-bundle.json`](../proposals/aes-adopt-existing/checklist-bundle.json)

_No source-local artifact summary._

### [`proposals/aes-adopt-existing/evidence/digimon-adopt-2026-10-07.txt`](../proposals/aes-adopt-existing/evidence/digimon-adopt-2026-10-07.txt)

_No source-local artifact summary._

### [`proposals/aes-adopt-existing/evidence/gates-1539967.txt`](../proposals/aes-adopt-existing/evidence/gates-1539967.txt)

_No source-local artifact summary._

### [`proposals/aes-adopt-existing/evidence/test-adopt-03dba8f.txt`](../proposals/aes-adopt-existing/evidence/test-adopt-03dba8f.txt)

_No source-local artifact summary._

### [`proposals/aes-adopt-existing/method-conformance-receipt.adoption-decision.json`](../proposals/aes-adopt-existing/method-conformance-receipt.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/aes-adopt-existing/method-conformance-receipt.json`](../proposals/aes-adopt-existing/method-conformance-receipt.json)

_No source-local artifact summary._

### [`proposals/aes-adopt-existing/planning-path-decision.json`](../proposals/aes-adopt-existing/planning-path-decision.json)

_No source-local artifact summary._

### [`proposals/aes-brownfield-docs/PLANNING_PATH.json`](../proposals/aes-brownfield-docs/PLANNING_PATH.json)

_No source-local artifact summary._

### [`proposals/aes-brownfield-docs/activation-facts.json`](../proposals/aes-brownfield-docs/activation-facts.json)

_No source-local artifact summary._

### [`proposals/aes-brownfield-docs/checklist.bundle.json`](../proposals/aes-brownfield-docs/checklist.bundle.json)

_No source-local artifact summary._

### [`proposals/aes-brownfield-docs/cold-reader-transcripts.json`](../proposals/aes-brownfield-docs/cold-reader-transcripts.json)

_No source-local artifact summary._

### [`proposals/aes-brownfield-docs/conformance.adoption-decision.json`](../proposals/aes-brownfield-docs/conformance.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/aes-brownfield-docs/conformance.receipt.json`](../proposals/aes-brownfield-docs/conformance.receipt.json)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/PLAN.adoption-attempts.jsonl`](../proposals/aes-durable-docs/PLAN.adoption-attempts.jsonl)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/PLAN.adoption-decision.json`](../proposals/aes-durable-docs/PLAN.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/PLAN.receipt.json`](../proposals/aes-durable-docs/PLAN.receipt.json)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/PLAN.verdicts.json`](../proposals/aes-durable-docs/PLAN.verdicts.json)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/PLANNING_PATH.json`](../proposals/aes-durable-docs/PLANNING_PATH.json)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/activation-facts.json`](../proposals/aes-durable-docs/activation-facts.json)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/adopt-output.txt`](../proposals/aes-durable-docs/adopt-output.txt)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/checklist.bundle.json`](../proposals/aes-durable-docs/checklist.bundle.json)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/evidence/m2-seeded-defects.txt`](../proposals/aes-durable-docs/evidence/m2-seeded-defects.txt)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/evidence/m4-aes-canonical-check.txt`](../proposals/aes-durable-docs/evidence/m4-aes-canonical-check.txt)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/evidence/m4-aes-canonical-cold-reader-question.txt`](../proposals/aes-durable-docs/evidence/m4-aes-canonical-cold-reader-question.txt)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/evidence/m4-aes-canonical-cold-reader.jsonl`](../proposals/aes-durable-docs/evidence/m4-aes-canonical-cold-reader.jsonl)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/evidence/m4-company-planning-check.txt`](../proposals/aes-durable-docs/evidence/m4-company-planning-check.txt)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/evidence/m4-company-planning-cold-reader.jsonl`](../proposals/aes-durable-docs/evidence/m4-company-planning-cold-reader.jsonl)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/evidence/m4-r13-r14-seeded-run.txt`](../proposals/aes-durable-docs/evidence/m4-r13-r14-seeded-run.txt)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/evidence/m4-r13-r14-tests.txt`](../proposals/aes-durable-docs/evidence/m4-r13-r14-tests.txt)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/evidence/m5-aes-canonical-cold-reader.jsonl`](../proposals/aes-durable-docs/evidence/m5-aes-canonical-cold-reader.jsonl)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/evidence/m5-company-planning-cold-reader-question.txt`](../proposals/aes-durable-docs/evidence/m5-company-planning-cold-reader-question.txt)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/evidence/m5-company-planning-cold-reader.jsonl`](../proposals/aes-durable-docs/evidence/m5-company-planning-cold-reader.jsonl)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/evidence/m5-inventory.json`](../proposals/aes-durable-docs/evidence/m5-inventory.json)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/evidence/m5-sample-tools/run-reader.sh`](../proposals/aes-durable-docs/evidence/m5-sample-tools/run-reader.sh)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/review-page/aes-durable-docs-plan-1440.png`](../proposals/aes-durable-docs/review-page/aes-durable-docs-plan-1440.png)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/review-page/aes-durable-docs-plan-390.png`](../proposals/aes-durable-docs/review-page/aes-durable-docs-plan-390.png)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/review-page/aes-durable-docs-plan.disposition.json`](../proposals/aes-durable-docs/review-page/aes-durable-docs-plan.disposition.json)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/review-page/aes-durable-docs-plan.recommendation.json`](../proposals/aes-durable-docs/review-page/aes-durable-docs-plan.recommendation.json)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/review-page/aes-durable-docs-plan.usecase.json`](../proposals/aes-durable-docs/review-page/aes-durable-docs-plan.usecase.json)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/review-page/index.html`](../proposals/aes-durable-docs/review-page/index.html)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/review-page/modeling-review.html`](../proposals/aes-durable-docs/review-page/modeling-review.html)

_No source-local artifact summary._

### [`proposals/aes-durable-docs/review-page/tooltip_test.cjs`](../proposals/aes-durable-docs/review-page/tooltip_test.cjs)

_No source-local artifact summary._

### [`proposals/aes-feedback-prevention/PLAN.adoption-attempts.jsonl`](../proposals/aes-feedback-prevention/PLAN.adoption-attempts.jsonl)

_No source-local artifact summary._

### [`proposals/aes-feedback-prevention/PLAN.adoption-decision.json`](../proposals/aes-feedback-prevention/PLAN.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/aes-feedback-prevention/PLAN.receipt.json`](../proposals/aes-feedback-prevention/PLAN.receipt.json)

_No source-local artifact summary._

### [`proposals/aes-feedback-prevention/PLAN.verdicts.json`](../proposals/aes-feedback-prevention/PLAN.verdicts.json)

_No source-local artifact summary._

### [`proposals/aes-feedback-prevention/bundle.json`](../proposals/aes-feedback-prevention/bundle.json)

_No source-local artifact summary._

### [`proposals/aes-feedback-prevention/completion-evidence.json`](../proposals/aes-feedback-prevention/completion-evidence.json)

_No source-local artifact summary._

### [`proposals/aes-feedback-prevention/facts.json`](../proposals/aes-feedback-prevention/facts.json)

_No source-local artifact summary._

### [`proposals/aes-feedback-prevention/planning-path-decision.json`](../proposals/aes-feedback-prevention/planning-path-decision.json)

_No source-local artifact summary._

### [`proposals/aes-feedback-prevention/representation-disposition.json`](../proposals/aes-feedback-prevention/representation-disposition.json)

_No source-local artifact summary._

### [`proposals/aes-feedback-prevention/representation-recommendation.json`](../proposals/aes-feedback-prevention/representation-recommendation.json)

_No source-local artifact summary._

### [`proposals/aes-feedback-prevention/representation-use-case.json`](../proposals/aes-feedback-prevention/representation-use-case.json)

_No source-local artifact summary._

### [`proposals/aes-learning-loop/PLAN.verdicts.json`](../proposals/aes-learning-loop/PLAN.verdicts.json)

_No source-local artifact summary._

### [`proposals/aes-learning-loop/activation-facts.json`](../proposals/aes-learning-loop/activation-facts.json)

_No source-local artifact summary._

### [`proposals/aes-learning-loop/checklist-bundle.json`](../proposals/aes-learning-loop/checklist-bundle.json)

_No source-local artifact summary._

### [`proposals/aes-learning-loop/feedback-system.svg`](../proposals/aes-learning-loop/feedback-system.svg)

_No source-local artifact summary._

### [`proposals/aes-learning-loop/method-conformance-receipt.adoption-attempts.jsonl`](../proposals/aes-learning-loop/method-conformance-receipt.adoption-attempts.jsonl)

_No source-local artifact summary._

### [`proposals/aes-learning-loop/method-conformance-receipt.adoption-decision.json`](../proposals/aes-learning-loop/method-conformance-receipt.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/aes-learning-loop/method-conformance-receipt.json`](../proposals/aes-learning-loop/method-conformance-receipt.json)

_No source-local artifact summary._

### [`proposals/aes-learning-loop/planning-path-decision.json`](../proposals/aes-learning-loop/planning-path-decision.json)

_No source-local artifact summary._

### [`proposals/aes-learning-loop/review-page/feedback-coverage.html`](../proposals/aes-learning-loop/review-page/feedback-coverage.html)

_No source-local artifact summary._

### [`proposals/aes-learning-loop/review-page/feedback-models.html`](../proposals/aes-learning-loop/review-page/feedback-models.html)

_No source-local artifact summary._

### [`proposals/aes-learning-loop/review-page/guide.html`](../proposals/aes-learning-loop/review-page/guide.html)

_No source-local artifact summary._

### [`proposals/aes-learning-loop/review-page/index.html`](../proposals/aes-learning-loop/review-page/index.html)

_No source-local artifact summary._

### [`proposals/aes-learning-loop/review-page/requirements.html`](../proposals/aes-learning-loop/review-page/requirements.html)

_No source-local artifact summary._

### [`proposals/aes-learning-loop/review-page/whole-picture.html`](../proposals/aes-learning-loop/review-page/whole-picture.html)

_No source-local artifact summary._

### [`proposals/aes-learning-loop/s1-tracker.yaml`](../proposals/aes-learning-loop/s1-tracker.yaml)

_No source-local artifact summary._

### [`proposals/aes-plan-scope/activation-facts.json`](../proposals/aes-plan-scope/activation-facts.json)

_No source-local artifact summary._

### [`proposals/aes-plan-scope/checklist-bundle.json`](../proposals/aes-plan-scope/checklist-bundle.json)

_No source-local artifact summary._

### [`proposals/aes-plan-scope/evidence/digimon-replay-2026-10-07.txt`](../proposals/aes-plan-scope/evidence/digimon-replay-2026-10-07.txt)

_No source-local artifact summary._

### [`proposals/aes-plan-scope/evidence/gates-47d6e14.txt`](../proposals/aes-plan-scope/evidence/gates-47d6e14.txt)

_No source-local artifact summary._

### [`proposals/aes-plan-scope/evidence/gates-9c981a5.txt`](../proposals/aes-plan-scope/evidence/gates-9c981a5.txt)

_No source-local artifact summary._

### [`proposals/aes-plan-scope/evidence/test-plan-scope-c3866f2.txt`](../proposals/aes-plan-scope/evidence/test-plan-scope-c3866f2.txt)

_No source-local artifact summary._

### [`proposals/aes-plan-scope/method-conformance-receipt.adoption-decision.json`](../proposals/aes-plan-scope/method-conformance-receipt.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/aes-plan-scope/method-conformance-receipt.json`](../proposals/aes-plan-scope/method-conformance-receipt.json)

_No source-local artifact summary._

### [`proposals/aes-plan-scope/planning-path-decision.json`](../proposals/aes-plan-scope/planning-path-decision.json)

_No source-local artifact summary._

### [`proposals/aes-planning/PLAN-AES-ACCEPT-RECEIPT.yaml`](../proposals/aes-planning/PLAN-AES-ACCEPT-RECEIPT.yaml)

_No source-local artifact summary._

### [`proposals/aes-planning/PLAN-AES-COMMIT-RULE.yaml`](../proposals/aes-planning/PLAN-AES-COMMIT-RULE.yaml)

_No source-local artifact summary._

### [`proposals/aes-planning/activation-facts.json`](../proposals/aes-planning/activation-facts.json)

_No source-local artifact summary._

### [`proposals/aes-planning/checklist-bundle.json`](../proposals/aes-planning/checklist-bundle.json)

_No source-local artifact summary._

### [`proposals/aes-planning/evidence/p3-live-validate-beedf30.txt`](../proposals/aes-planning/evidence/p3-live-validate-beedf30.txt)

_No source-local artifact summary._

### [`proposals/aes-planning/evidence/p4-canonical-example-transcript-4276550.txt`](../proposals/aes-planning/evidence/p4-canonical-example-transcript-4276550.txt)

_No source-local artifact summary._

### [`proposals/aes-planning/evidence/p4-canonical-example-transcript-72925dc.txt`](../proposals/aes-planning/evidence/p4-canonical-example-transcript-72925dc.txt)

_No source-local artifact summary._

### [`proposals/aes-planning/evidence/p4-canonical-example-transcript-8ace3cd.txt`](../proposals/aes-planning/evidence/p4-canonical-example-transcript-8ace3cd.txt)

_No source-local artifact summary._

### [`proposals/aes-planning/evidence/p4-canonical-example-transcript-b023fb0.txt`](../proposals/aes-planning/evidence/p4-canonical-example-transcript-b023fb0.txt)

_No source-local artifact summary._

### [`proposals/aes-planning/evidence/p4-canonical-example-transcript-b91592b.txt`](../proposals/aes-planning/evidence/p4-canonical-example-transcript-b91592b.txt)

_No source-local artifact summary._

### [`proposals/aes-planning/evidence/p4-canonical-example-transcript-ca78424.txt`](../proposals/aes-planning/evidence/p4-canonical-example-transcript-ca78424.txt)

_No source-local artifact summary._

### [`proposals/aes-planning/evidence/p4-canonical-example-transcript.txt`](../proposals/aes-planning/evidence/p4-canonical-example-transcript.txt)

_No source-local artifact summary._

### [`proposals/aes-planning/evidence/p4-replay-aes-canonical-300-4276550.txt`](../proposals/aes-planning/evidence/p4-replay-aes-canonical-300-4276550.txt)

_No source-local artifact summary._

### [`proposals/aes-planning/evidence/p4-replay-aes-canonical-300-b91592b.txt`](../proposals/aes-planning/evidence/p4-replay-aes-canonical-300-b91592b.txt)

_No source-local artifact summary._

### [`proposals/aes-planning/evidence/p4-replay-aes-canonical-300-ca78424.txt`](../proposals/aes-planning/evidence/p4-replay-aes-canonical-300-ca78424.txt)

_No source-local artifact summary._

### [`proposals/aes-planning/evidence/p4-replay-aes-canonical-300.txt`](../proposals/aes-planning/evidence/p4-replay-aes-canonical-300.txt)

_No source-local artifact summary._

### [`proposals/aes-planning/evidence/p4-replay-personal-vps-300-4276550.txt`](../proposals/aes-planning/evidence/p4-replay-personal-vps-300-4276550.txt)

_No source-local artifact summary._

### [`proposals/aes-planning/evidence/p4-replay-personal-vps-300-b91592b.txt`](../proposals/aes-planning/evidence/p4-replay-personal-vps-300-b91592b.txt)

_No source-local artifact summary._

### [`proposals/aes-planning/evidence/p4-replay-personal-vps-300-ca78424.txt`](../proposals/aes-planning/evidence/p4-replay-personal-vps-300-ca78424.txt)

_No source-local artifact summary._

### [`proposals/aes-planning/evidence/p4-replay-personal-vps-300.txt`](../proposals/aes-planning/evidence/p4-replay-personal-vps-300.txt)

_No source-local artifact summary._

### [`proposals/aes-planning/evidence/p4-replay-trivial-share.txt`](../proposals/aes-planning/evidence/p4-replay-trivial-share.txt)

_No source-local artifact summary._

### [`proposals/aes-planning/evidence/run_p4_live.sh`](../proposals/aes-planning/evidence/run_p4_live.sh)

_No source-local artifact summary._

### [`proposals/aes-planning/method-conformance-receipt.adoption-decision.json`](../proposals/aes-planning/method-conformance-receipt.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/aes-planning/method-conformance-receipt.json`](../proposals/aes-planning/method-conformance-receipt.json)

_No source-local artifact summary._

### [`proposals/aes-planning/planning-path-decision.json`](../proposals/aes-planning/planning-path-decision.json)

_No source-local artifact summary._

### [`proposals/aes-planning/review-page/aes-planning-plan-1440.png`](../proposals/aes-planning/review-page/aes-planning-plan-1440.png)

_No source-local artifact summary._

### [`proposals/aes-planning/review-page/aes-planning-plan.disposition.json`](../proposals/aes-planning/review-page/aes-planning-plan.disposition.json)

_No source-local artifact summary._

### [`proposals/aes-planning/review-page/aes-planning-plan.html`](../proposals/aes-planning/review-page/aes-planning-plan.html)

_No source-local artifact summary._

### [`proposals/aes-planning/review-page/aes-planning-plan.recommendation.json`](../proposals/aes-planning/review-page/aes-planning-plan.recommendation.json)

_No source-local artifact summary._

### [`proposals/aes-planning/review-page/aes-planning-plan.usecase.json`](../proposals/aes-planning/review-page/aes-planning-plan.usecase.json)

_No source-local artifact summary._

### [`proposals/aes-planning/rollout/replay-2026-10-07.csv`](../proposals/aes-planning/rollout/replay-2026-10-07.csv)

_No source-local artifact summary._

### [`proposals/aes-planning/rollout/systemd/aes-commit-misuse-review.service`](../proposals/aes-planning/rollout/systemd/aes-commit-misuse-review.service)

_No source-local artifact summary._

### [`proposals/aes-planning/rollout/systemd/aes-commit-misuse-review.timer`](../proposals/aes-planning/rollout/systemd/aes-commit-misuse-review.timer)

_No source-local artifact summary._

### [`proposals/aes-planning/rollout/systemd/aes-commit-rule-daily.service`](../proposals/aes-planning/rollout/systemd/aes-commit-rule-daily.service)

_No source-local artifact summary._

### [`proposals/aes-planning/rollout/systemd/aes-commit-rule-daily.timer`](../proposals/aes-planning/rollout/systemd/aes-commit-rule-daily.timer)

_No source-local artifact summary._

### [`proposals/aes-subagent-feedback/PLAN.adoption-decision.json`](../proposals/aes-subagent-feedback/PLAN.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/aes-subagent-feedback/PLAN.receipt.json`](../proposals/aes-subagent-feedback/PLAN.receipt.json)

_No source-local artifact summary._

### [`proposals/aes-subagent-feedback/PLAN.verdicts.json`](../proposals/aes-subagent-feedback/PLAN.verdicts.json)

_No source-local artifact summary._

### [`proposals/aes-subagent-feedback/bundle.json`](../proposals/aes-subagent-feedback/bundle.json)

_No source-local artifact summary._

### [`proposals/aes-subagent-feedback/facts.json`](../proposals/aes-subagent-feedback/facts.json)

_No source-local artifact summary._

### [`proposals/aes-subagent-feedback/planning-path-decision.json`](../proposals/aes-subagent-feedback/planning-path-decision.json)

_No source-local artifact summary._

### [`proposals/aes-v0.2-greenfield/02-semantic-model.candidate.yaml`](../proposals/aes-v0.2-greenfield/02-semantic-model.candidate.yaml)

_No source-local artifact summary._

### [`proposals/aes-v0.2-greenfield/03-lifecycle.candidate.yaml`](../proposals/aes-v0.2-greenfield/03-lifecycle.candidate.yaml)

_No source-local artifact summary._

### [`proposals/aes-v0.2-greenfield/04-greenfield-mvp.candidate.yaml`](../proposals/aes-v0.2-greenfield/04-greenfield-mvp.candidate.yaml)

_No source-local artifact summary._

### [`proposals/aes-v0.2-greenfield/12-greenfield-mvp-semantic-instance.candidate.yaml`](../proposals/aes-v0.2-greenfield/12-greenfield-mvp-semantic-instance.candidate.yaml)

_No source-local artifact summary._

### [`proposals/aes-v0.2-greenfield/14-initialization-contract.candidate.yaml`](../proposals/aes-v0.2-greenfield/14-initialization-contract.candidate.yaml)

_No source-local artifact summary._

### [`proposals/aes-v0.2-greenfield/15-planning-contract.candidate.yaml`](../proposals/aes-v0.2-greenfield/15-planning-contract.candidate.yaml)

_No source-local artifact summary._

### [`proposals/aes-v0.2-greenfield/16-record-shapes.candidate.yaml`](../proposals/aes-v0.2-greenfield/16-record-shapes.candidate.yaml)

_No source-local artifact summary._

### [`proposals/aes-v0.2-greenfield/17-provider-evaluation-contract.candidate.yaml`](../proposals/aes-v0.2-greenfield/17-provider-evaluation-contract.candidate.yaml)

_No source-local artifact summary._

### [`proposals/aes-v0.2-greenfield/18-internal-provider-evaluation.candidate.yaml`](../proposals/aes-v0.2-greenfield/18-internal-provider-evaluation.candidate.yaml)

_No source-local artifact summary._

### [`proposals/aes-v0.2-greenfield/19-public-native-provider-evaluation.candidate.yaml`](../proposals/aes-v0.2-greenfield/19-public-native-provider-evaluation.candidate.yaml)

_No source-local artifact summary._

### [`proposals/aes-v0.2-greenfield/20-realization-topology.candidate.yaml`](../proposals/aes-v0.2-greenfield/20-realization-topology.candidate.yaml)

_No source-local artifact summary._

### [`proposals/aes-v0.2-greenfield/21-provider-bindings.candidate.yaml`](../proposals/aes-v0.2-greenfield/21-provider-bindings.candidate.yaml)

_No source-local artifact summary._

### [`proposals/aes-v0.2-greenfield/review-manifest.candidate.yaml`](../proposals/aes-v0.2-greenfield/review-manifest.candidate.yaml)

_No source-local artifact summary._

### [`proposals/agent-router/PLAN.verdicts.json`](../proposals/agent-router/PLAN.verdicts.json)

_No source-local artifact summary._

### [`proposals/agent-router/README.md.writing.json`](../proposals/agent-router/README.md.writing.json)

_No source-local artifact summary._

### [`proposals/agent-router/bundle.json`](../proposals/agent-router/bundle.json)

_No source-local artifact summary._

### [`proposals/agent-router/claude-feedback-capture.json`](../proposals/agent-router/claude-feedback-capture.json)

_No source-local artifact summary._

### [`proposals/agent-router/core-integration.json`](../proposals/agent-router/core-integration.json)

_No source-local artifact summary._

### [`proposals/agent-router/cursor-replace.json`](../proposals/agent-router/cursor-replace.json)

_No source-local artifact summary._

### [`proposals/agent-router/cursor-start.json`](../proposals/agent-router/cursor-start.json)

_No source-local artifact summary._

### [`proposals/agent-router/deployed-collector-check.json`](../proposals/agent-router/deployed-collector-check.json)

_No source-local artifact summary._

### [`proposals/agent-router/evidence.json`](../proposals/agent-router/evidence.json)

_No source-local artifact summary._

### [`proposals/agent-router/facts.json`](../proposals/agent-router/facts.json)

_No source-local artifact summary._

### [`proposals/agent-router/inventory-check-process.json`](../proposals/agent-router/inventory-check-process.json)

_No source-local artifact summary._

### [`proposals/agent-router/inventory-check.json`](../proposals/agent-router/inventory-check.json)

_No source-local artifact summary._

### [`proposals/agent-router/inventory-followup-check.json`](../proposals/agent-router/inventory-followup-check.json)

_No source-local artifact summary._

### [`proposals/agent-router/inventory-publication-privacy.json`](../proposals/agent-router/inventory-publication-privacy.json)

_No source-local artifact summary._

### [`proposals/agent-router/local-check-process.json`](../proposals/agent-router/local-check-process.json)

_No source-local artifact summary._

### [`proposals/agent-router/local-check.json`](../proposals/agent-router/local-check.json)

_No source-local artifact summary._

### [`proposals/agent-router/native-feedback-consumer.json`](../proposals/agent-router/native-feedback-consumer.json)

_No source-local artifact summary._

### [`proposals/agent-router/native-feedback-parent-check.txt`](../proposals/agent-router/native-feedback-parent-check.txt)

_No source-local artifact summary._

### [`proposals/agent-router/native-handoff-replay.json`](../proposals/agent-router/native-handoff-replay.json)

_No source-local artifact summary._

### [`proposals/agent-router/native-handoff-role-mismatch.json`](../proposals/agent-router/native-handoff-role-mismatch.json)

_No source-local artifact summary._

### [`proposals/agent-router/planning-path-decision.json`](../proposals/agent-router/planning-path-decision.json)

_No source-local artifact summary._

### [`proposals/agent-router/pr-description.txt`](../proposals/agent-router/pr-description.txt)

_No source-local artifact summary._

### [`proposals/agent-router/pr-description.txt.writing.json`](../proposals/agent-router/pr-description.txt.writing.json)

_No source-local artifact summary._

### [`proposals/agent-router/profiles/brian.json`](../proposals/agent-router/profiles/brian.json)

_No source-local artifact summary._

### [`proposals/agent-router/profiles/colleague.json`](../proposals/agent-router/profiles/colleague.json)

_No source-local artifact summary._

### [`proposals/agent-router/profiles/effective-profiles.json`](../proposals/agent-router/profiles/effective-profiles.json)

_No source-local artifact summary._

### [`proposals/agent-router/receipt.adoption-attempts.jsonl`](../proposals/agent-router/receipt.adoption-attempts.jsonl)

_No source-local artifact summary._

### [`proposals/agent-router/receipt.adoption-decision.json`](../proposals/agent-router/receipt.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/agent-router/receipt.json`](../proposals/agent-router/receipt.json)

_No source-local artifact summary._

### [`proposals/agent-router/revision-path-decision.json`](../proposals/agent-router/revision-path-decision.json)

_No source-local artifact summary._

### [`proposals/agent-router/verification.log`](../proposals/agent-router/verification.log)

_No source-local artifact summary._

### [`proposals/code2-ecosystem/PLAN.adoption-attempts.jsonl`](../proposals/code2-ecosystem/PLAN.adoption-attempts.jsonl)

_No source-local artifact summary._

### [`proposals/code2-ecosystem/PLAN.adoption-decision.json`](../proposals/code2-ecosystem/PLAN.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/code2-ecosystem/PLAN.receipt.json`](../proposals/code2-ecosystem/PLAN.receipt.json)

_No source-local artifact summary._

### [`proposals/code2-ecosystem/PLAN.verdicts.json`](../proposals/code2-ecosystem/PLAN.verdicts.json)

_No source-local artifact summary._

### [`proposals/code2-ecosystem/bundle.json`](../proposals/code2-ecosystem/bundle.json)

_No source-local artifact summary._

### [`proposals/code2-ecosystem/check.txt`](../proposals/code2-ecosystem/check.txt)

_No source-local artifact summary._

### [`proposals/code2-ecosystem/facts.json`](../proposals/code2-ecosystem/facts.json)

_No source-local artifact summary._

### [`proposals/code2-ecosystem/path-decision.json`](../proposals/code2-ecosystem/path-decision.json)

_No source-local artifact summary._

### [`proposals/code2-ecosystem/phase2-aes-proposal.yaml`](../proposals/code2-ecosystem/phase2-aes-proposal.yaml)

_No source-local artifact summary._

### [`proposals/code2-ecosystem/phase2-aes-validate.txt`](../proposals/code2-ecosystem/phase2-aes-validate.txt)

_No source-local artifact summary._

### [`proposals/commit-rule-followups/commit-rule-followups.adoption-decision.json`](../proposals/commit-rule-followups/commit-rule-followups.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/commit-rule-followups/commit-rule-followups.bundle.json`](../proposals/commit-rule-followups/commit-rule-followups.bundle.json)

_No source-local artifact summary._

### [`proposals/commit-rule-followups/commit-rule-followups.check.txt`](../proposals/commit-rule-followups/commit-rule-followups.check.txt)

_No source-local artifact summary._

### [`proposals/commit-rule-followups/commit-rule-followups.facts.json`](../proposals/commit-rule-followups/commit-rule-followups.facts.json)

_No source-local artifact summary._

### [`proposals/commit-rule-followups/commit-rule-followups.path-decision.json`](../proposals/commit-rule-followups/commit-rule-followups.path-decision.json)

_No source-local artifact summary._

### [`proposals/commit-rule-followups/commit-rule-followups.receipt.json`](../proposals/commit-rule-followups/commit-rule-followups.receipt.json)

_No source-local artifact summary._

### [`proposals/commit-rule-notes-report/commit-rule-notes-report.adoption-decision.json`](../proposals/commit-rule-notes-report/commit-rule-notes-report.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/commit-rule-notes-report/commit-rule-notes-report.bundle.json`](../proposals/commit-rule-notes-report/commit-rule-notes-report.bundle.json)

_No source-local artifact summary._

### [`proposals/commit-rule-notes-report/commit-rule-notes-report.check.txt`](../proposals/commit-rule-notes-report/commit-rule-notes-report.check.txt)

_No source-local artifact summary._

### [`proposals/commit-rule-notes-report/commit-rule-notes-report.facts.json`](../proposals/commit-rule-notes-report/commit-rule-notes-report.facts.json)

_No source-local artifact summary._

### [`proposals/commit-rule-notes-report/commit-rule-notes-report.path-decision.json`](../proposals/commit-rule-notes-report/commit-rule-notes-report.path-decision.json)

_No source-local artifact summary._

### [`proposals/commit-rule-notes-report/commit-rule-notes-report.receipt.json`](../proposals/commit-rule-notes-report/commit-rule-notes-report.receipt.json)

_No source-local artifact summary._

### [`proposals/commit-tag-case/commit-tag-case.adoption-decision.json`](../proposals/commit-tag-case/commit-tag-case.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/commit-tag-case/commit-tag-case.bundle.json`](../proposals/commit-tag-case/commit-tag-case.bundle.json)

_No source-local artifact summary._

### [`proposals/commit-tag-case/commit-tag-case.check.txt`](../proposals/commit-tag-case/commit-tag-case.check.txt)

_No source-local artifact summary._

### [`proposals/commit-tag-case/commit-tag-case.facts.json`](../proposals/commit-tag-case/commit-tag-case.facts.json)

_No source-local artifact summary._

### [`proposals/commit-tag-case/commit-tag-case.path-decision.json`](../proposals/commit-tag-case/commit-tag-case.path-decision.json)

_No source-local artifact summary._

### [`proposals/commit-tag-case/commit-tag-case.receipt.json`](../proposals/commit-tag-case/commit-tag-case.receipt.json)

_No source-local artifact summary._

### [`proposals/doc-reach-new-docs/PLAN.adoption-decision.json`](../proposals/doc-reach-new-docs/PLAN.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/doc-reach-new-docs/PLAN.receipt.json`](../proposals/doc-reach-new-docs/PLAN.receipt.json)

_No source-local artifact summary._

### [`proposals/doc-reach-new-docs/PLAN.verdicts.json`](../proposals/doc-reach-new-docs/PLAN.verdicts.json)

_No source-local artifact summary._

### [`proposals/doc-reach-new-docs/activation-facts.json`](../proposals/doc-reach-new-docs/activation-facts.json)

_No source-local artifact summary._

### [`proposals/doc-reach-new-docs/check.txt`](../proposals/doc-reach-new-docs/check.txt)

_No source-local artifact summary._

### [`proposals/doc-reach-new-docs/checklist.bundle.json`](../proposals/doc-reach-new-docs/checklist.bundle.json)

_No source-local artifact summary._

### [`proposals/doc-reach-new-docs/planning-path-decision.json`](../proposals/doc-reach-new-docs/planning-path-decision.json)

_No source-local artifact summary._

### [`proposals/doc-reach-new-docs/replay-after.txt`](../proposals/doc-reach-new-docs/replay-after.txt)

_No source-local artifact summary._

### [`proposals/doc-reach-new-docs/replay.txt`](../proposals/doc-reach-new-docs/replay.txt)

_No source-local artifact summary._

### [`proposals/evidence-recorder-counts/admission-attempts.json`](../proposals/evidence-recorder-counts/admission-attempts.json)

_No source-local artifact summary._

### [`proposals/evidence-recorder-counts/junit.native-probes.json`](../proposals/evidence-recorder-counts/junit.native-probes.json)

_No source-local artifact summary._

### [`proposals/evidence-recorder-counts/method-bundle.json`](../proposals/evidence-recorder-counts/method-bundle.json)

_No source-local artifact summary._

### [`proposals/evidence-recorder-counts/method-conformance-receipt.adoption-decision.json`](../proposals/evidence-recorder-counts/method-conformance-receipt.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/evidence-recorder-counts/method-conformance-receipt.json`](../proposals/evidence-recorder-counts/method-conformance-receipt.json)

_No source-local artifact summary._

### [`proposals/evidence-recorder-counts/method-facts.json`](../proposals/evidence-recorder-counts/method-facts.json)

_No source-local artifact summary._

### [`proposals/evidence-recorder-counts/native-proposal.yaml`](../proposals/evidence-recorder-counts/native-proposal.yaml)

_No source-local artifact summary._

### [`proposals/evidence-recorder-counts/planning-path-decision.json`](../proposals/evidence-recorder-counts/planning-path-decision.json)

_No source-local artifact summary._

### [`proposals/evidence-recorder-counts/prepare.yaml`](../proposals/evidence-recorder-counts/prepare.yaml)

_No source-local artifact summary._

### [`proposals/evidence-recorder-counts/privacy-checkpoint.initial-false-positive.json`](../proposals/evidence-recorder-counts/privacy-checkpoint.initial-false-positive.json)

_No source-local artifact summary._

### [`proposals/evidence-recorder-counts/privacy-checkpoint.json`](../proposals/evidence-recorder-counts/privacy-checkpoint.json)

_No source-local artifact summary._

### [`proposals/evidence-recorder-counts/publication-pattern-scan.json`](../proposals/evidence-recorder-counts/publication-pattern-scan.json)

_No source-local artifact summary._

### [`proposals/evidence-recorder-counts/refused3-method-conformance-receipt.adoption-decision.json`](../proposals/evidence-recorder-counts/refused3-method-conformance-receipt.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/evidence-recorder-counts/refused3-method-conformance-receipt.json`](../proposals/evidence-recorder-counts/refused3-method-conformance-receipt.json)

_No source-local artifact summary._

### [`proposals/evidence-recorder-counts/reproduction.before.json`](../proposals/evidence-recorder-counts/reproduction.before.json)

_No source-local artifact summary._

### [`proposals/evidence-recorder-counts/reproduction.review.json`](../proposals/evidence-recorder-counts/reproduction.review.json)

_No source-local artifact summary._

### [`proposals/evidence-recorder-counts/reproduction.trace.json`](../proposals/evidence-recorder-counts/reproduction.trace.json)

_No source-local artifact summary._

### [`proposals/harness-context/activation-facts.json`](../proposals/harness-context/activation-facts.json)

_No source-local artifact summary._

### [`proposals/harness-context/additional-findings.json`](../proposals/harness-context/additional-findings.json)

_No source-local artifact summary._

### [`proposals/harness-context/checklist-bundle.json`](../proposals/harness-context/checklist-bundle.json)

_No source-local artifact summary._

### [`proposals/harness-context/evidence.json`](../proposals/harness-context/evidence.json)

_No source-local artifact summary._

### [`proposals/harness-context/feedback-records.json`](../proposals/harness-context/feedback-records.json)

_No source-local artifact summary._

### [`proposals/harness-context/findings.json`](../proposals/harness-context/findings.json)

_No source-local artifact summary._

### [`proposals/harness-context/hooks-policy-inventory.json`](../proposals/harness-context/hooks-policy-inventory.json)

_No source-local artifact summary._

### [`proposals/harness-context/instructions-skills-inventory.json`](../proposals/harness-context/instructions-skills-inventory.json)

_No source-local artifact summary._

### [`proposals/harness-context/method-conformance-receipt.adoption-decision.json`](../proposals/harness-context/method-conformance-receipt.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/harness-context/method-conformance-receipt.json`](../proposals/harness-context/method-conformance-receipt.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/authority-context-proof.json`](../proposals/harness-context/native-parity/authority-context-proof.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/authority-context/child-source-review.json`](../proposals/harness-context/native-parity/authority-context/child-source-review.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/authority-context/claude-agents.json`](../proposals/harness-context/native-parity/authority-context/claude-agents.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/authority-context/development-investigator.codex.toml`](../proposals/harness-context/native-parity/authority-context/development-investigator.codex.toml)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/authority-context/manifest.json`](../proposals/harness-context/native-parity/authority-context/manifest.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/claude-native-refusal.json`](../proposals/harness-context/native-parity/claude-native-refusal.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/claude-paid/child-result.json`](../proposals/harness-context/native-parity/claude-paid/child-result.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/claude-paid/workflow-and-parity-evidence.json`](../proposals/harness-context/native-parity/claude-paid/workflow-and-parity-evidence.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/claude-refusal.json`](../proposals/harness-context/native-parity/claude-refusal.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/codex-child-result.json`](../proposals/harness-context/native-parity/codex-child-result.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/codex-trace-summary.json`](../proposals/harness-context/native-parity/codex-trace-summary.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/compact-codex-proof.json`](../proposals/harness-context/native-parity/compact-codex-proof.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/cursor-handoff.json`](../proposals/harness-context/native-parity/cursor-handoff.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/cursor-replace.json`](../proposals/harness-context/native-parity/cursor-replace.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/cursor-retirement-refusal.json`](../proposals/harness-context/native-parity/cursor-retirement-refusal.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/cursor-retirement.json`](../proposals/harness-context/native-parity/cursor-retirement.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/cursor-start.json`](../proposals/harness-context/native-parity/cursor-start.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/delivery-context-proof.json`](../proposals/harness-context/native-parity/delivery-context-proof.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/delivery-context/claude-agents.json`](../proposals/harness-context/native-parity/delivery-context/claude-agents.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/delivery-context/claude-availability.json`](../proposals/harness-context/native-parity/delivery-context/claude-availability.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/delivery-context/development-investigator.codex.toml`](../proposals/harness-context/native-parity/delivery-context/development-investigator.codex.toml)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/delivery-context/discovery-exit-semantics.json`](../proposals/harness-context/native-parity/delivery-context/discovery-exit-semantics.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/delivery-context/launcher-refusal.json`](../proposals/harness-context/native-parity/delivery-context/launcher-refusal.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/delivery-context/local-check-subject.json`](../proposals/harness-context/native-parity/delivery-context/local-check-subject.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/delivery-context/manifest.json`](../proposals/harness-context/native-parity/delivery-context/manifest.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/delivery-context/semantic-review.json`](../proposals/harness-context/native-parity/delivery-context/semantic-review.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/input/project-meta/Makefile`](../proposals/harness-context/native-parity/input/project-meta/Makefile)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/input/task.json`](../proposals/harness-context/native-parity/input/task.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/launch.json`](../proposals/harness-context/native-parity/launch.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/local-check-process.json`](../proposals/harness-context/native-parity/local-check-process.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/local-check.json`](../proposals/harness-context/native-parity/local-check.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/local-gate-delay.json`](../proposals/harness-context/native-parity/local-gate-delay.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/paired-trace-review.json`](../proposals/harness-context/native-parity/paired-trace-review.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/parent-prompt.txt`](../proposals/harness-context/native-parity/parent-prompt.txt)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/parity-issue-comment.txt`](../proposals/harness-context/native-parity/parity-issue-comment.txt)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/permission-probe.json`](../proposals/harness-context/native-parity/permission-probe.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/pr-body.txt`](../proposals/harness-context/native-parity/pr-body.txt)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/pr-body.txt.writing.json`](../proposals/harness-context/native-parity/pr-body.txt.writing.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/privacy.json`](../proposals/harness-context/native-parity/privacy.json)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/resume-goal.txt`](../proposals/harness-context/native-parity/resume-goal.txt)

_No source-local artifact summary._

### [`proposals/harness-context/native-parity/verification.json`](../proposals/harness-context/native-parity/verification.json)

_No source-local artifact summary._

### [`proposals/harness-context/planning-path-decision.json`](../proposals/harness-context/planning-path-decision.json)

_No source-local artifact summary._

### [`proposals/harness-context/prior-art-ownership-evidence.json`](../proposals/harness-context/prior-art-ownership-evidence.json)

_No source-local artifact summary._

### [`proposals/harness-context/public-plan-check.json`](../proposals/harness-context/public-plan-check.json)

_No source-local artifact summary._

### [`proposals/harness-context/recommendations.json`](../proposals/harness-context/recommendations.json)

_No source-local artifact summary._

### [`proposals/harness-context/review-page/browser-verification.json`](../proposals/harness-context/review-page/browser-verification.json)

_No source-local artifact summary._

### [`proposals/harness-context/review-page/disposition-receipt/harness-context--layered-architecture-view--2026-10-08T03-55-21-249Z.json`](../proposals/harness-context/review-page/disposition-receipt/harness-context--layered-architecture-view--2026-10-08T03-55-21-249Z.json)

_No source-local artifact summary._

### [`proposals/harness-context/review-page/disposition-receipt/harness-context--layered-architecture-view--2026-10-08T04-08-03-666Z.json`](../proposals/harness-context/review-page/disposition-receipt/harness-context--layered-architecture-view--2026-10-08T04-08-03-666Z.json)

_No source-local artifact summary._

### [`proposals/harness-context/review-page/disposition.json`](../proposals/harness-context/review-page/disposition.json)

_No source-local artifact summary._

### [`proposals/harness-context/review-page/index.html`](../proposals/harness-context/review-page/index.html)

_No source-local artifact summary._

### [`proposals/harness-context/review-page/index.html.writing.json`](../proposals/harness-context/review-page/index.html.writing.json)

_No source-local artifact summary._

### [`proposals/harness-context/review-page/verify_page.cjs`](../proposals/harness-context/review-page/verify_page.cjs)

_No source-local artifact summary._

### [`proposals/harness-context/review-recommendation.json`](../proposals/harness-context/review-recommendation.json)

_No source-local artifact summary._

### [`proposals/harness-context/review-use-case.json`](../proposals/harness-context/review-use-case.json)

_No source-local artifact summary._

### [`proposals/harness-context/subagent-research.disposition.json`](../proposals/harness-context/subagent-research.disposition.json)

_No source-local artifact summary._

### [`proposals/harness-context/subagent-research.evidence.json`](../proposals/harness-context/subagent-research.evidence.json)

_No source-local artifact summary._

### [`proposals/harness-context/subagent-research.md.writing.json`](../proposals/harness-context/subagent-research.md.writing.json)

_No source-local artifact summary._

### [`proposals/meeting-claims-true/PLAN.adoption-decision.json`](../proposals/meeting-claims-true/PLAN.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/meeting-claims-true/PLAN.receipt.json`](../proposals/meeting-claims-true/PLAN.receipt.json)

_No source-local artifact summary._

### [`proposals/meeting-claims-true/PLAN.verdicts.json`](../proposals/meeting-claims-true/PLAN.verdicts.json)

_No source-local artifact summary._

### [`proposals/meeting-claims-true/PLANNING_PATH.json`](../proposals/meeting-claims-true/PLANNING_PATH.json)

_No source-local artifact summary._

### [`proposals/meeting-claims-true/activation-facts.json`](../proposals/meeting-claims-true/activation-facts.json)

_No source-local artifact summary._

### [`proposals/meeting-claims-true/checklist.bundle.json`](../proposals/meeting-claims-true/checklist.bundle.json)

_No source-local artifact summary._

### [`proposals/second-brain-evaluation/PLANNING_PATH.json`](../proposals/second-brain-evaluation/PLANNING_PATH.json)

_No source-local artifact summary._

### [`proposals/second-brain-evaluation/activation-facts.json`](../proposals/second-brain-evaluation/activation-facts.json)

_No source-local artifact summary._

### [`proposals/second-brain-evaluation/checklist.bundle.json`](../proposals/second-brain-evaluation/checklist.bundle.json)

_No source-local artifact summary._

### [`proposals/second-brain-evaluation/conformance.adoption-decision.json`](../proposals/second-brain-evaluation/conformance.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/second-brain-evaluation/conformance.receipt.json`](../proposals/second-brain-evaluation/conformance.receipt.json)

_No source-local artifact summary._

### [`proposals/system-model-review/review-page/index.html`](../proposals/system-model-review/review-page/index.html)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/aes-proposal.yaml`](../proposals/trace-review-enforcement/aes-proposal.yaml)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/authentic-assessment.json`](../proposals/trace-review-enforcement/authentic-assessment.json)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/authentic-source.json`](../proposals/trace-review-enforcement/authentic-source.json)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/authentic.review.json`](../proposals/trace-review-enforcement/authentic.review.json)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/authority-source.json`](../proposals/trace-review-enforcement/authority-source.json)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/boundary-probes.before-custody-fix.trace.json`](../proposals/trace-review-enforcement/boundary-probes.before-custody-fix.trace.json)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/boundary-probes.before-membership-fix.trace.json`](../proposals/trace-review-enforcement/boundary-probes.before-membership-fix.trace.json)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/boundary-probes.initial.trace.json`](../proposals/trace-review-enforcement/boundary-probes.initial.trace.json)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/boundary-probes.review.json`](../proposals/trace-review-enforcement/boundary-probes.review.json)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/boundary-probes.trace.json`](../proposals/trace-review-enforcement/boundary-probes.trace.json)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/final-gate-supervisor.log`](../proposals/trace-review-enforcement/final-gate-supervisor.log)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/final-gate.json`](../proposals/trace-review-enforcement/final-gate.json)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/final-gate.log`](../proposals/trace-review-enforcement/final-gate.log)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/plan.adoption-decision.json`](../proposals/trace-review-enforcement/plan.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/plan.receipt.json`](../proposals/trace-review-enforcement/plan.receipt.json)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/publication-check.json`](../proposals/trace-review-enforcement/publication-check.json)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/publication-check.trace.json`](../proposals/trace-review-enforcement/publication-check.trace.json)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/publication-disposition.json`](../proposals/trace-review-enforcement/publication-disposition.json)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/self-governance-failure.review.json`](../proposals/trace-review-enforcement/self-governance-failure.review.json)

_No source-local artifact summary._

### [`proposals/trace-review-enforcement/self-governance-failure.trace.json`](../proposals/trace-review-enforcement/self-governance-failure.trace.json)

_No source-local artifact summary._

### [`proposals/trace-review/activation-facts.json`](../proposals/trace-review/activation-facts.json)

_No source-local artifact summary._

### [`proposals/trace-review/checklist-bundle.json`](../proposals/trace-review/checklist-bundle.json)

_No source-local artifact summary._

### [`proposals/trace-review/method-conformance-receipt.adoption-decision.json`](../proposals/trace-review/method-conformance-receipt.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/trace-review/method-conformance-receipt.json`](../proposals/trace-review/method-conformance-receipt.json)

_No source-local artifact summary._

### [`proposals/trace-review/planning-path-decision.json`](../proposals/trace-review/planning-path-decision.json)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/PLAN.adoption-attempts.jsonl`](../proposals/worktree-lifecycle/PLAN.adoption-attempts.jsonl)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/PLAN.adoption-decision.json`](../proposals/worktree-lifecycle/PLAN.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/PLAN.md.writing.json`](../proposals/worktree-lifecycle/PLAN.md.writing.json)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/PLAN.receipt.json`](../proposals/worktree-lifecycle/PLAN.receipt.json)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/PLAN.verdicts.json`](../proposals/worktree-lifecycle/PLAN.verdicts.json)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/bundle.json`](../proposals/worktree-lifecycle/bundle.json)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/conformance.exit`](../proposals/worktree-lifecycle/conformance.exit)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/conformance.log`](../proposals/worktree-lifecycle/conformance.log)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/disposition.json`](../proposals/worktree-lifecycle/disposition.json)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/facts.json`](../proposals/worktree-lifecycle/facts.json)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/path-decision.json`](../proposals/worktree-lifecycle/path-decision.json)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/privacy-screen.json`](../proposals/worktree-lifecycle/privacy-screen.json)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/recommendation.json`](../proposals/worktree-lifecycle/recommendation.json)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/representation-records/worktree-lifecycle-plan--scroll-linked-explainer--2026-10-09T03-07-16-294Z.json`](../proposals/worktree-lifecycle/representation-records/worktree-lifecycle-plan--scroll-linked-explainer--2026-10-09T03-07-16-294Z.json)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/review-page/browser-qa.json`](../proposals/worktree-lifecycle/review-page/browser-qa.json)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/review-page/desktop.png`](../proposals/worktree-lifecycle/review-page/desktop.png)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/review-page/index.html`](../proposals/worktree-lifecycle/review-page/index.html)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/review-page/lifecycle-mobile.d2`](../proposals/worktree-lifecycle/review-page/lifecycle-mobile.d2)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/review-page/lifecycle-mobile.svg`](../proposals/worktree-lifecycle/review-page/lifecycle-mobile.svg)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/review-page/lifecycle.d2`](../proposals/worktree-lifecycle/review-page/lifecycle.d2)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/review-page/lifecycle.svg`](../proposals/worktree-lifecycle/review-page/lifecycle.svg)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/review-page/link-qa.json`](../proposals/worktree-lifecycle/review-page/link-qa.json)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/review-page/mobile.png`](../proposals/worktree-lifecycle/review-page/mobile.png)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/review-use-case.json`](../proposals/worktree-lifecycle/review-use-case.json)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/secret-scan.json`](../proposals/worktree-lifecycle/secret-scan.json)

_No source-local artifact summary._

### [`proposals/worktree-lifecycle/validation.json`](../proposals/worktree-lifecycle/validation.json)

_No source-local artifact summary._

### [`proposals/worktree-plan-lookup/worktree-plan-lookup.adoption-attempts.jsonl`](../proposals/worktree-plan-lookup/worktree-plan-lookup.adoption-attempts.jsonl)

_No source-local artifact summary._

### [`proposals/worktree-plan-lookup/worktree-plan-lookup.adoption-decision.json`](../proposals/worktree-plan-lookup/worktree-plan-lookup.adoption-decision.json)

_No source-local artifact summary._

### [`proposals/worktree-plan-lookup/worktree-plan-lookup.bundle.json`](../proposals/worktree-plan-lookup/worktree-plan-lookup.bundle.json)

_No source-local artifact summary._

### [`proposals/worktree-plan-lookup/worktree-plan-lookup.check.txt`](../proposals/worktree-plan-lookup/worktree-plan-lookup.check.txt)

_No source-local artifact summary._

### [`proposals/worktree-plan-lookup/worktree-plan-lookup.facts.json`](../proposals/worktree-plan-lookup/worktree-plan-lookup.facts.json)

_No source-local artifact summary._

### [`proposals/worktree-plan-lookup/worktree-plan-lookup.path-decision.json`](../proposals/worktree-plan-lookup/worktree-plan-lookup.path-decision.json)

_No source-local artifact summary._

### [`proposals/worktree-plan-lookup/worktree-plan-lookup.receipt.json`](../proposals/worktree-plan-lookup/worktree-plan-lookup.receipt.json)

_No source-local artifact summary._

### [`proposals/worktree-plan-lookup/worktree-plan-lookup.verdicts.json`](../proposals/worktree-plan-lookup/worktree-plan-lookup.verdicts.json)

_No source-local artifact summary._

### [`pyproject.toml`](../pyproject.toml)

_No source-local artifact summary._

### [`scripts/learning_loop/question_set_v2.json`](../scripts/learning_loop/question_set_v2.json)

_No source-local artifact summary._

### [`scripts/learning_loop/systemd/feedback-collector.service`](../scripts/learning_loop/systemd/feedback-collector.service)

_No source-local artifact summary._

### [`scripts/learning_loop/systemd/feedback-collector.timer`](../scripts/learning_loop/systemd/feedback-collector.timer)

_No source-local artifact summary._

### [`scripts/learning_loop/systemd/feedback-effects.service`](../scripts/learning_loop/systemd/feedback-effects.service)

_No source-local artifact summary._

### [`scripts/learning_loop/systemd/feedback-effects.timer`](../scripts/learning_loop/systemd/feedback-effects.timer)

_No source-local artifact summary._

### [`scripts/learning_loop/systemd/feedback-fix-owner.service`](../scripts/learning_loop/systemd/feedback-fix-owner.service)

_No source-local artifact summary._

### [`scripts/learning_loop/systemd/feedback-fix-owner.timer`](../scripts/learning_loop/systemd/feedback-fix-owner.timer)

_No source-local artifact summary._

### [`scripts/learning_loop/systemd/feedback-problems.service`](../scripts/learning_loop/systemd/feedback-problems.service)

_No source-local artifact summary._

### [`scripts/learning_loop/systemd/feedback-problems.timer`](../scripts/learning_loop/systemd/feedback-problems.timer)

_No source-local artifact summary._

### [`scripts/relationships.yaml`](../scripts/relationships.yaml)

_No source-local artifact summary._

### [`src/agentic_engineering_system/repository_context/component.context.generated.yaml`](../src/agentic_engineering_system/repository_context/component.context.generated.yaml)

_No source-local artifact summary._

### [`uv.lock`](../uv.lock)

_No source-local artifact summary._

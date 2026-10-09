# === META-PROCESS TARGETS ===
# Added by meta-process install.sh

# Configuration
# Auto-select the repo virtualenv for test targets: the full pytest suite needs
# heavy deps (tree_sitter_python, ruamel, ...) that live only in .venv, not in
# system python. Overridable: `make test PYTHON=python3`. CI does not use these
# targets (it runs a curated pytest allowlist with its own installed deps).
PYTHON ?= $(shell [ -x .venv/bin/python ] && echo .venv/bin/python || echo python3)
SCRIPTS_META := scripts/meta
PLANS_DIR := docs/plans
GITHUB_ACCOUNT ?= BrianMills2718
PR_AUTO_EXPECTED_REPO ?= $(notdir $(CURDIR))
ROUTE_REQUEST ?= Change llm_client event taxonomy and update project-meta parity checks.
ROUTE_OUTPUT ?= text
REMOTE_DEV_SESSION ?= dev-main
# Workspace-specific provider for the portable numbered-plan start gate. Git's
# common directory resolves the canonical repository from either checkout.
PROJECTS_ROOT ?= $(abspath $(shell git rev-parse --path-format=absolute --git-common-dir)/../..)
PLAN_READINESS_PYTHON ?= $(shell [ -x "$(PROJECTS_ROOT)/ecosystem-ops/.venv/bin/python" ] && echo "$(PROJECTS_ROOT)/ecosystem-ops/.venv/bin/python" || echo "$(PYTHON)")
PLAN_READINESS_COMMAND ?= $(PLAN_READINESS_PYTHON) $(PROJECTS_ROOT)/ecosystem-ops/plan_graph.py

# --- Session Start ---
.PHONY: status

PROJECT_STATUS_PYTHON ?= $(if $(strip $(PYTHON)),$(PYTHON),$(if $(wildcard .venv/bin/python),.venv/bin/python,python3))
PROJECT_STATUS_SCRIPT ?= scripts/meta/project_status.py
status:  ## Verify repository authority freshness and show branch status
	@$(PROJECT_STATUS_PYTHON) $(PROJECT_STATUS_SCRIPT) --repo-root .

.PHONY: governed-knowledge-plan-check

governed-knowledge-plan-check:  ## Validate governed knowledge-analysis planning closure
	@$(PYTHON) scripts/check_governed_knowledge_plan.py \
		--manifest vision/planning/governed_knowledge_analysis_manifest.json \
		--repo-root .

.PHONY: remote-dev-check remote-dev-setup remote-dev-session remote-dev-status remote-dev-tunnel remote-dev-tunnel-service

remote-dev-check:  ## Check WSL remote development prerequisites
	@scripts/remote_dev/install_remote_dev.sh --check

remote-dev-setup:  ## Install local WSL remote development prerequisites
	@scripts/remote_dev/install_remote_dev.sh

remote-dev-session:  ## Create/attach durable tmux session for remote agent work
	@scripts/remote_dev/agent_session.sh --session "$(REMOTE_DEV_SESSION)"

remote-dev-status:  ## Show VS Code tunnel, tmux, agent CLI, and Tailscale status
	@scripts/remote_dev/remote_dev_status.sh

remote-dev-tunnel:  ## Start foreground VS Code tunnel in a tmux session
	@scripts/remote_dev/tunnel_control.sh foreground

remote-dev-tunnel-service:  ## Install VS Code tunnel service after authentication
	@scripts/remote_dev/tunnel_control.sh service-install

# >>> META-PROCESS WORKTREE TARGETS >>>
PYTHON ?= python3
WORKTREE_CREATE_SCRIPT := scripts/meta/worktree-coordination/create_worktree.py
WORKTREE_REMOVE_SCRIPT := scripts/meta/worktree-coordination/safe_worktree_remove.py
WORKTREE_CLAIMS_SCRIPT := scripts/meta/worktree-coordination/../check_coordination_claims.py
WORKTREE_SESSION_START_SCRIPT := scripts/meta/worktree-coordination/../session_start.py
WORKTREE_SESSION_HEARTBEAT_SCRIPT := scripts/meta/worktree-coordination/../session_heartbeat.py
WORKTREE_SESSION_STATUS_SCRIPT := scripts/meta/worktree-coordination/../session_status.py
WORKTREE_SESSION_END_SCRIPT := scripts/meta/worktree-coordination/../session_end.py
WORKTREE_SESSION_FINISH_SCRIPT := scripts/meta/worktree-coordination/../session_finish.py
WORKTREE_SESSION_CLOSE_SCRIPT := scripts/meta/worktree-coordination/../session_close.py
WORKTREE_REVIEW_CLAIM_SCRIPT := scripts/meta/worktree-coordination/create_review_claim.py
WORKTREE_RAISE_CONCERN_SCRIPT := scripts/meta/worktree-coordination/raise_concern.py
WORKTREE_PLAN_READINESS_SCRIPT := scripts/meta/worktree-coordination/../check_plan_readiness.py
SURFACE_RUNTIME_SCRIPT := scripts/meta/worktree-coordination/../surface_runtime.py
WORKTREE_REPO_ROOT ?= $(shell git rev-parse --path-format=absolute --git-common-dir 2>/dev/null | sed 's|/\.git$$||')
WORKTREE_DIR ?= $(shell $(PYTHON) "$(WORKTREE_CREATE_SCRIPT)" --repo-root "$(WORKTREE_REPO_ROOT)" --print-default-worktree-dir)
WORKTREE_START_POINT ?= HEAD
WORKTREE_START_REVISION := $(shell git -C "$(WORKTREE_REPO_ROOT)" rev-parse --verify "$(WORKTREE_START_POINT)^{commit}" 2>/dev/null)
WORKTREE_PROJECT ?= $(shell $(PYTHON) "$(WORKTREE_CREATE_SCRIPT)" --repo-root "$(WORKTREE_REPO_ROOT)" --print-canonical-project)
WORKTREE_AGENT ?= $(shell if [ -n "$$CODEX_THREAD_ID" ]; then printf codex; elif [ -n "$$CLAUDE_CODE_SESSION_ID" ] || [ -n "$$CLAUDE_SESSION_ID" ] || [ -n "$$CLAUDE_CODE_SSE_PORT" ]; then printf claude-code; elif [ -n "$$OPENCLAW_SESSION_ID" ] || [ -n "$$OPENCLAW_RUN_ID" ]; then printf openclaw; fi)
SESSION_GOAL ?=
SESSION_PHASE ?=
SESSION_NEXT ?=
SESSION_DEPENDS ?=
SESSION_STOP_CONDITIONS ?=
SESSION_NOTE ?=
SESSION_ALLOW_PARALLEL ?=
ALLOW_UNPLANNED ?=
PLAN_RESUME ?=
WORKTREE_EXECUTION_PROFILE ?= coordinated
PLAN_PROJECT ?= $(WORKTREE_PROJECT)
PLAN_REPO_ROOT ?=
PLAN_START_POINT ?=
PLAN_READINESS_COMMAND ?=
SESSION_CLAIM_TYPE ?= program
SESSION_PARENT_SCOPE ?=
SESSION_WRITE_PATHS ?=
SESSION_READ_PATHS ?=
SESSION_WORK_GRAPH ?=
SESSION_WORK_UNIT_ID ?=
WORKTREE_DISPOSITION ?= merged
WORKTREE_DISPOSITION_REASON ?=
WORKTREE_RECOVERY_REF ?=
WORKTREE_ALLOW_DISCARD_UNIQUE ?=
WORKTREE_MERGE_COMMIT ?=
REVIEW_SCOPE ?=
REVIEW_NOTES ?=
RECIPIENT ?=

.PHONY: worktree maintenance-worktree worktree-list worktree-remove session-start session-heartbeat session-status session-end session-finish session-close review-claim raise-concern verification-batch-freeze verification-batch-check verification-batch-thaw surface-up surface-preview surface-status surface-down surface-audit

verification-batch-freeze:  ## Freeze clean HEAD for DECISION="..." VERIFY_COMMAND="..."
	@test -n "$(DECISION)" || (echo "DECISION is required" && exit 1)
	@test -n "$(VERIFY_COMMAND)" || (echo "VERIFY_COMMAND is required" && exit 1)
	$(PYTHON) scripts/meta/verification_batch.py --repo-root . freeze --decision "$(DECISION)" --command "$(VERIFY_COMMAND)" $(if $(ALLOW_UNTRACKED),--allow-untracked "$(ALLOW_UNTRACKED)",)

verification-batch-check:  ## Require the active batch to match exact clean HEAD
	$(PYTHON) scripts/meta/verification_batch.py --repo-root . check --require-active

verification-batch-thaw:  ## Invalidate the batch with REASON="..." before a scoped fix
	@test -n "$(REASON)" || (echo "REASON is required" && exit 1)
	$(PYTHON) scripts/meta/verification_batch.py --repo-root . thaw --reason "$(REASON)"

worktree:  ## Create claimed worktree (BRANCH=name TASK="..." [PLAN=N] [AGENT=name])
ifndef BRANCH
	$(error BRANCH is required. Usage: make worktree BRANCH=plan-42-feature TASK="Describe the task")
endif
ifndef TASK
	$(error TASK is required. Usage: make worktree BRANCH=plan-42-feature TASK="Describe the task")
endif
ifndef SESSION_GOAL
	$(error SESSION_GOAL is required. Name the broader objective, not the local branch)
endif
ifndef SESSION_PHASE
	$(error SESSION_PHASE is required. Describe the current execution phase)
endif
ifndef WORKTREE_AGENT
	$(error Unable to infer agent runtime. Set AGENT via WORKTREE_AGENT=codex|claude-code|openclaw)
endif
	@if [ ! -f "$(WORKTREE_CREATE_SCRIPT)" ]; then \
		echo "Missing worktree coordination module: $(WORKTREE_CREATE_SCRIPT)"; \
		echo "Install or sync the sanctioned worktree-coordination module before using make worktree."; \
		exit 1; \
	fi
	@if [ ! -f "$(WORKTREE_CLAIMS_SCRIPT)" ]; then \
		echo "Missing worktree coordination module: $(WORKTREE_CLAIMS_SCRIPT)"; \
		echo "Install or sync the sanctioned worktree-coordination module before using make worktree."; \
		exit 1; \
	fi
	@if [ ! -f "$(WORKTREE_SESSION_START_SCRIPT)" ]; then \
		echo "Missing session lifecycle module: $(WORKTREE_SESSION_START_SCRIPT)"; \
		echo "Install or sync the sanctioned session lifecycle module before using make worktree."; \
		exit 1; \
	fi
	@test -n "$(WORKTREE_START_REVISION)" || { \
		echo "Unable to resolve one full Git start revision from $(WORKTREE_START_POINT)"; \
		exit 1; \
	}
	@$(PYTHON) "$(WORKTREE_PLAN_READINESS_SCRIPT)" \
		$(if $(PLAN),--qualified-plan-id "$(PLAN_PROJECT)#$(PLAN)",) \
		--execution-profile "$(WORKTREE_EXECUTION_PROFILE)" \
		--repo-root "$(WORKTREE_REPO_ROOT)" \
		--start-point "$(WORKTREE_START_REVISION)" \
		$(if $(PLAN_REPO_ROOT),--plan-repo-root "$(PLAN_REPO_ROOT)",) \
		$(if $(PLAN_START_POINT),--plan-start-point "$(PLAN_START_POINT)",) \
		$(if $(PLAN_READINESS_COMMAND),--query-command "$(PLAN_READINESS_COMMAND)",) \
		--repository "$(WORKTREE_PROJECT)" \
		--lane-id "$(BRANCH)" \
		$(if $(SESSION_PARENT_SCOPE),--parent-lane-id "$(SESSION_PARENT_SCOPE)",) \
		--branch "$(BRANCH)" \
		--worktree-path "$(WORKTREE_DIR)/$(BRANCH)" \
		--agent "$(WORKTREE_AGENT)" \
		--scope "$(BRANCH)" \
		$(if $(ALLOW_UNPLANNED),--allow-unplanned,) \
		$(if $(PLAN_RESUME),--resume,)
	@$(PYTHON) "$(WORKTREE_CLAIMS_SCRIPT)" --claim \
		--agent "$(WORKTREE_AGENT)" \
		--project "$(WORKTREE_PROJECT)" \
		--scope "$(BRANCH)" \
		--intent "$(TASK)" \
		--claim-type "$(SESSION_CLAIM_TYPE)" \
		--repo-root "$(WORKTREE_REPO_ROOT)" \
		--branch "$(BRANCH)" \
		--worktree-path "$(WORKTREE_DIR)/$(BRANCH)" \
		--start-point "$(WORKTREE_START_REVISION)" \
		$(if $(PLAN_REPO_ROOT),--plan-repo-root "$(PLAN_REPO_ROOT)",) \
		$(if $(PLAN_START_POINT),--plan-start-point "$(PLAN_START_POINT)",) \
		--require-new \
		$(if $(PLAN_RESUME),--resume,) \
		--session-name "$(SESSION_GOAL)" \
		--broader-goal "$(SESSION_GOAL)" \
		$(if $(SESSION_PARENT_SCOPE),--parent-scope "$(SESSION_PARENT_SCOPE)",) \
		$(if $(filter 1 true yes,$(SESSION_ALLOW_PARALLEL)),--allow-parallel,) \
		$(if $(SESSION_BROAD_SCOPE_MODE),--broad-scope-mode "$(SESSION_BROAD_SCOPE_MODE)",) \
		$(if $(SESSION_BROAD_SCOPE_REASON),--broad-scope-reason "$(SESSION_BROAD_SCOPE_REASON)",) \
		$(foreach path,$(SESSION_WRITE_PATHS),--write-path "$(path)") \
		$(foreach path,$(SESSION_READ_PATHS),--read-path "$(path)") \
		$(if $(SESSION_WORK_GRAPH),--work-graph "$(SESSION_WORK_GRAPH)",) \
		$(if $(SESSION_WORK_UNIT_ID),--work-unit-id "$(SESSION_WORK_UNIT_ID)",) \
		$(if $(PLAN),--plan "$(PLAN_PROJECT)#$(PLAN)",$(if $(ALLOW_UNPLANNED),--plan UNPLANNED,))
	@mkdir -p "$(WORKTREE_DIR)"
	@creation_receipt=$$(mktemp "$(WORKTREE_DIR)/.worktree-create.XXXXXX.json"); \
	trap 'rm -f "$$creation_receipt"' EXIT HUP INT TERM; \
	if ! $(PYTHON) "$(WORKTREE_CREATE_SCRIPT)" \
		--repo-root "$(WORKTREE_REPO_ROOT)" \
		--path "$(WORKTREE_DIR)/$(BRANCH)" \
		--branch "$(BRANCH)" \
		--start-point "$(WORKTREE_START_REVISION)" \
		--require-write-claim \
		--claim-agent "$(WORKTREE_AGENT)" \
		--claim-project "$(WORKTREE_PROJECT)" \
		$(foreach path,$(SESSION_WRITE_PATHS),--claim-write-path "$(path)") \
		$(if $(PLAN),--claim-start-revision "$(WORKTREE_START_REVISION)",) \
		--json > "$$creation_receipt"; then \
		if ! $(PYTHON) -c 'import json, sys; payload=json.load(open(sys.argv[1], encoding="utf-8")); print("Worktree creation failed: " + payload["message"], file=sys.stderr)' "$$creation_receipt"; then \
			echo "Worktree creation failed and its receipt was unreadable." >&2; \
		fi; \
		if ! created_branch=$$($(PYTHON) -c 'import json, sys; print(1 if json.load(open(sys.argv[1], encoding="utf-8"))["created_branch"] else 0)' "$$creation_receipt"); then \
			echo "Worktree creation failed without a readable ownership receipt; claim retained."; \
			exit 1; \
		fi; \
		unsafe_residue=0; \
		if [ -e "$(WORKTREE_DIR)/$(BRANCH)" ]; then unsafe_residue=1; fi; \
		if [ "$$created_branch" -eq 1 ] && git -C "$(WORKTREE_REPO_ROOT)" show-ref --verify --quiet "refs/heads/$(BRANCH)"; then unsafe_residue=1; fi; \
		if [ "$$unsafe_residue" -eq 0 ]; then \
			$(PYTHON) "$(WORKTREE_CLAIMS_SCRIPT)" --release \
				--agent "$(WORKTREE_AGENT)" --project "$(WORKTREE_PROJECT)" --scope "$(BRANCH)" \
				--require-current-session --rollback-managed-lane \
				$(if $(PLAN),--expected-start-revision "$(WORKTREE_START_REVISION)",) || exit 1; \
		else \
			echo "Worktree creation failed with recoverable branch/worktree residue; claim retained."; \
		fi; \
		exit 1; \
	fi; \
	if ! created_branch=$$($(PYTHON) -c 'import json, sys; print(1 if json.load(open(sys.argv[1], encoding="utf-8"))["created_branch"] else 0)' "$$creation_receipt"); then \
		echo "Worktree was created without a readable ownership receipt; claim retained."; \
		exit 1; \
	fi; \
	if ! $(PYTHON) "$(WORKTREE_SESSION_START_SCRIPT)" \
		--agent "$(WORKTREE_AGENT)" \
		--project "$(WORKTREE_PROJECT)" \
		--scope "$(BRANCH)" \
		--intent "$(TASK)" \
		--repo-root "$(WORKTREE_REPO_ROOT)" \
		--worktree-path "$(WORKTREE_DIR)/$(BRANCH)" \
		--branch "$(BRANCH)" \
		--broader-goal "$(SESSION_GOAL)" \
		--current-phase "$(SESSION_PHASE)" \
		--claim-type "$(SESSION_CLAIM_TYPE)" \
		$(if $(SESSION_BROAD_SCOPE_MODE),--broad-scope-mode "$(SESSION_BROAD_SCOPE_MODE)",) \
		$(if $(SESSION_BROAD_SCOPE_REASON),--broad-scope-reason "$(SESSION_BROAD_SCOPE_REASON)",) \
		$(if $(SESSION_PARENT_SCOPE),--parent-scope "$(SESSION_PARENT_SCOPE)",) \
		$(if $(filter 1 true yes,$(SESSION_ALLOW_PARALLEL)),--allow-parallel,) \
		$(if $(SESSION_BROAD_SCOPE_MODE),--broad-scope-mode "$(SESSION_BROAD_SCOPE_MODE)",) \
		$(if $(SESSION_BROAD_SCOPE_REASON),--broad-scope-reason "$(SESSION_BROAD_SCOPE_REASON)",) \
		$(foreach path,$(SESSION_WRITE_PATHS),--write-path "$(path)") \
		$(foreach path,$(SESSION_READ_PATHS),--read-path "$(path)") \
		$(if $(SESSION_WORK_GRAPH),--work-graph "$(SESSION_WORK_GRAPH)",) \
		$(if $(SESSION_WORK_UNIT_ID),--work-unit-id "$(SESSION_WORK_UNIT_ID)",) \
		$(if $(PLAN),--plan "$(PLAN_PROJECT)#$(PLAN)",) \
		$(if $(PLAN),--start-revision "$(WORKTREE_START_REVISION)",) \
		$(if $(PLAN_REPO_ROOT),--plan-repo-root "$(PLAN_REPO_ROOT)",) \
		$(if $(PLAN_START_POINT),--plan-start-point "$(PLAN_START_POINT)",) \
		$(if $(ALLOW_UNPLANNED),--allow-unplanned,) \
		$(if $(SESSION_NEXT),--next-phase "$(SESSION_NEXT)",) \
		$(if $(SESSION_DEPENDS),--depends-on "$(SESSION_DEPENDS)",) \
		$(if $(SESSION_STOP_CONDITIONS),--stop-condition "$(SESSION_STOP_CONDITIONS)",) \
		$(if $(SESSION_NOTE),--notes "$(SESSION_NOTE)",); then \
		cleanup_ok=1; \
		git -C "$(WORKTREE_REPO_ROOT)" worktree remove --force "$(WORKTREE_DIR)/$(BRANCH)" || cleanup_ok=0; \
		if [ "$$created_branch" -eq 1 ]; then \
			git -C "$(WORKTREE_REPO_ROOT)" branch -D "$(BRANCH)" || cleanup_ok=0; \
		fi; \
		if [ "$$cleanup_ok" -eq 1 ]; then \
			$(PYTHON) "$(WORKTREE_CLAIMS_SCRIPT)" --release \
				--agent "$(WORKTREE_AGENT)" --project "$(WORKTREE_PROJECT)" --scope "$(BRANCH)" \
				--require-current-session --rollback-managed-lane \
				$(if $(PLAN),--expected-start-revision "$(WORKTREE_START_REVISION)",) || exit 1; \
		else \
			echo "Session start failed and exact cleanup was incomplete; claim retained."; \
		fi; \
		exit 1; \
	fi; \
	rm -f "$$creation_receipt"; \
	trap - EXIT HUP INT TERM
	@echo ""
	@echo "Worktree created at $(WORKTREE_DIR)/$(BRANCH)"
	@echo "Claim created for branch $(BRANCH)"
	@echo "Session contract started for $(SESSION_GOAL)"


# Defaults that make `make maintenance-worktree BRANCH=<name>` sufficient.
# The escape hatch this competes with (ALLOW_CANONICAL_CHECKOUT_COMMIT=1) is one
# variable with zero blanks to fill. Requiring five blanks here is why one
# session on 2026-08-23 took the hatch six times across two repositories rather
# than create a single worktree. Every default below stays overridable, and
# `make worktree` (plan-owned lanes) still requires all of them explicitly --
# a numbered plan lane should not get its goal invented from a branch name.
MAINTENANCE_LABEL = $(subst -, ,$(BRANCH))
MAINTENANCE_TASK = $(if $(strip $(TASK)),$(TASK),Unplanned maintenance: $(MAINTENANCE_LABEL))
MAINTENANCE_SESSION_GOAL = $(if $(strip $(SESSION_GOAL)),$(SESSION_GOAL),Unplanned maintenance: $(MAINTENANCE_LABEL))
MAINTENANCE_SESSION_PHASE = $(if $(strip $(SESSION_PHASE)),$(SESSION_PHASE),maintenance)
MAINTENANCE_AGENT = $(if $(strip $(WORKTREE_AGENT)),$(WORKTREE_AGENT),claude-code)
# This is the one deliberately broad bootstrap claim.  A maintenance lane has
# no declared implementation surface yet, so requiring a caller-supplied path
# makes the sanctioned entrypoint impossible to use.  The surrounding command
# still binds it to one repository, branch, worktree, and native session; the
# lane must narrow its authority before it begins scoped implementation work.
# Bootstrap claim scope for an unplanned maintenance lane. Defaults to the repo
# root because the lane may not know its targets yet, but an explicit
# SESSION_WRITE_PATHS must win: silently discarding it made every maintenance
# lane conflict with every other active lane by construction, and the operator
# saw a CONFLICT naming the other lanes rather than their own claim.
MAINTENANCE_BOOTSTRAP_WRITE_PATHS = $(if $(strip $(SESSION_WRITE_PATHS)),$(SESSION_WRITE_PATHS),.)

maintenance-worktree:  ## Claimed light maintenance worktree; needs BRANCH (other maintenance metadata has safe defaults)
	@if [ -n "$(PLAN)" ]; then \
		echo "maintenance-worktree is only for explicitly unplanned light maintenance; use make worktree PLAN=N for plan-owned work."; \
		exit 2; \
	fi
	@if [ -z "$(strip $(BRANCH))" ]; then \
		echo "BRANCH is required. Usage: make maintenance-worktree BRANCH=fix-hook-guard"; \
		echo "Everything else has a default: TASK, SESSION_GOAL, and SESSION_PHASE come"; \
		echo "from the branch name, and the agent from the runtime. Override any of them."; \
		exit 2; \
	fi
	@$(MAKE) worktree \
		BRANCH="$(BRANCH)" TASK="$(MAINTENANCE_TASK)" WORKTREE_AGENT="$(MAINTENANCE_AGENT)" \
		SESSION_GOAL="$(MAINTENANCE_SESSION_GOAL)" SESSION_PHASE="$(MAINTENANCE_SESSION_PHASE)" \
		SESSION_NEXT="$(SESSION_NEXT)" SESSION_DEPENDS="$(SESSION_DEPENDS)" \
		SESSION_STOP_CONDITIONS="$(SESSION_STOP_CONDITIONS)" SESSION_NOTE="$(SESSION_NOTE)" \
		SESSION_CLAIM_TYPE="$(SESSION_CLAIM_TYPE)" SESSION_PARENT_SCOPE="$(SESSION_PARENT_SCOPE)" \
		SESSION_ALLOW_PARALLEL="$(SESSION_ALLOW_PARALLEL)" \
		SESSION_WRITE_PATHS="$(MAINTENANCE_BOOTSTRAP_WRITE_PATHS)" SESSION_READ_PATHS="$(SESSION_READ_PATHS)" \
		WORKTREE_EXECUTION_PROFILE=light ALLOW_UNPLANNED=1

session-start:  ## Create or refresh the active session contract for BRANCH=name
ifndef BRANCH
	$(error BRANCH is required. Usage: make session-start BRANCH=plan-42-feature TASK="..." SESSION_GOAL="..." SESSION_PHASE="...")
endif
ifndef TASK
	$(error TASK is required. Usage: make session-start BRANCH=plan-42-feature TASK="...")
endif
ifndef SESSION_GOAL
	$(error SESSION_GOAL is required. Name the broader objective, not the local branch)
endif
ifndef SESSION_PHASE
	$(error SESSION_PHASE is required. Describe the current execution phase)
endif
ifndef WORKTREE_AGENT
	$(error Unable to infer agent runtime. Set AGENT via WORKTREE_AGENT=codex|claude-code|openclaw)
endif
	@$(PYTHON) "$(WORKTREE_SESSION_START_SCRIPT)" \
		--agent "$(WORKTREE_AGENT)" \
		--project "$(WORKTREE_PROJECT)" \
		--scope "$(BRANCH)" \
		--intent "$(TASK)" \
		--repo-root "$(WORKTREE_REPO_ROOT)" \
		--worktree-path "$(WORKTREE_DIR)/$(BRANCH)" \
		--branch "$(BRANCH)" \
		--broader-goal "$(SESSION_GOAL)" \
		--current-phase "$(SESSION_PHASE)" \
		--claim-type "$(SESSION_CLAIM_TYPE)" \
		$(if $(SESSION_BROAD_SCOPE_MODE),--broad-scope-mode "$(SESSION_BROAD_SCOPE_MODE)",) \
		$(if $(SESSION_BROAD_SCOPE_REASON),--broad-scope-reason "$(SESSION_BROAD_SCOPE_REASON)",) \
		$(if $(SESSION_PARENT_SCOPE),--parent-scope "$(SESSION_PARENT_SCOPE)",) \
		$(if $(filter 1 true yes,$(SESSION_ALLOW_PARALLEL)),--allow-parallel,) \
		$(if $(SESSION_BROAD_SCOPE_MODE),--broad-scope-mode "$(SESSION_BROAD_SCOPE_MODE)",) \
		$(if $(SESSION_BROAD_SCOPE_REASON),--broad-scope-reason "$(SESSION_BROAD_SCOPE_REASON)",) \
		$(foreach path,$(SESSION_WRITE_PATHS),--write-path "$(path)") \
		$(foreach path,$(SESSION_READ_PATHS),--read-path "$(path)") \
		$(if $(SESSION_WORK_GRAPH),--work-graph "$(SESSION_WORK_GRAPH)",) \
		$(if $(SESSION_WORK_UNIT_ID),--work-unit-id "$(SESSION_WORK_UNIT_ID)",) \
		$(if $(PLAN),--plan "$(PLAN_PROJECT)#$(PLAN)",) \
		$(if $(PLAN_REPO_ROOT),--plan-repo-root "$(PLAN_REPO_ROOT)",) \
		$(if $(PLAN_START_POINT),--plan-start-point "$(PLAN_START_POINT)",) \
		$(if $(ALLOW_UNPLANNED),--allow-unplanned,) \
		$(if $(SESSION_NEXT),--next-phase "$(SESSION_NEXT)",) \
		$(if $(SESSION_DEPENDS),--depends-on "$(SESSION_DEPENDS)",) \
		$(if $(SESSION_STOP_CONDITIONS),--stop-condition "$(SESSION_STOP_CONDITIONS)",) \
		$(if $(SESSION_NOTE),--notes "$(SESSION_NOTE)",)

session-heartbeat:  ## Refresh heartbeat and optional phase for BRANCH=name
ifndef BRANCH
	$(error BRANCH is required. Usage: make session-heartbeat BRANCH=plan-42-feature)
endif
ifndef WORKTREE_AGENT
	$(error Unable to infer agent runtime. Set AGENT via WORKTREE_AGENT=codex|claude-code|openclaw)
endif
	@$(PYTHON) "$(WORKTREE_SESSION_HEARTBEAT_SCRIPT)" \
		--agent "$(WORKTREE_AGENT)" \
		--project "$(WORKTREE_PROJECT)" \
		--scope "$(BRANCH)" \
		--branch "$(BRANCH)" \
		$(if $(SESSION_PHASE),--current-phase "$(SESSION_PHASE)",)

session-status:  ## Show live session summaries for this repo
	@$(PYTHON) "$(WORKTREE_SESSION_STATUS_SCRIPT)" --project "$(WORKTREE_PROJECT)"

session-end:  ## Retire this runtime session's live claims without deleting Git work
ifndef WORKTREE_AGENT
	$(error Unable to infer agent runtime. Set AGENT via WORKTREE_AGENT=codex|claude-code|openclaw)
endif
	@$(PYTHON) "$(WORKTREE_SESSION_END_SCRIPT)" \
		--agent "$(WORKTREE_AGENT)" \
		$(if $(SESSION_NOTE),--reason "$(SESSION_NOTE)",)

session-finish:  ## Record dirty handoff only; clean managed lanes must use session-close
ifndef BRANCH
	$(error BRANCH is required. Usage: make session-finish BRANCH=plan-42-feature)
endif
ifndef WORKTREE_AGENT
	$(error Unable to infer agent runtime. Set AGENT via WORKTREE_AGENT=codex|claude-code|openclaw)
endif
	@$(PYTHON) "$(WORKTREE_SESSION_FINISH_SCRIPT)" \
		--agent "$(WORKTREE_AGENT)" \
		--project "$(WORKTREE_PROJECT)" \
		--scope "$(BRANCH)" \
		--worktree-path "$(WORKTREE_DIR)/$(BRANCH)" \
		$(if $(SESSION_NOTE),--note "$(SESSION_NOTE)",)

session-close:  ## Close the claimed lane for BRANCH=name: cleanup worktree + branch + claim together
ifndef BRANCH
	$(error BRANCH is required. Usage: make session-close BRANCH=plan-42-feature)
endif
ifndef WORKTREE_AGENT
	$(error Unable to infer agent runtime. Set AGENT via WORKTREE_AGENT=codex|claude-code|openclaw)
endif
	@$(PYTHON) "$(WORKTREE_SESSION_CLOSE_SCRIPT)" \
		--agent "$(WORKTREE_AGENT)" \
		--project "$(WORKTREE_PROJECT)" \
		--scope "$(BRANCH)" \
		--worktree-path "$(WORKTREE_DIR)/$(BRANCH)" \
		--branch "$(BRANCH)" \
		--disposition "$(WORKTREE_DISPOSITION)" \
		--disposition-reason "$(WORKTREE_DISPOSITION_REASON)" \
		--recovery-ref "$(WORKTREE_RECOVERY_REF)" \
		$(if $(filter 1 true yes,$(WORKTREE_ALLOW_DISCARD_UNIQUE)),--allow-discard-unique,) \
		$(if $(WORKTREE_MERGE_COMMIT),--merge-commit "$(WORKTREE_MERGE_COMMIT)",) \
		$(if $(SESSION_NOTE),--note "$(SESSION_NOTE)",)

worktree-list:  ## Show claimed worktree coordination status
	@if [ ! -f "$(WORKTREE_CLAIMS_SCRIPT)" ]; then \
		echo "Missing worktree coordination module: $(WORKTREE_CLAIMS_SCRIPT)"; \
		echo "Install or sync the sanctioned worktree-coordination module before using make worktree-list."; \
		exit 1; \
	fi
	@$(PYTHON) "$(WORKTREE_CLAIMS_SCRIPT)" --list

worktree-remove:  ## Safely remove worktree for BRANCH=name
ifndef BRANCH
	$(error BRANCH is required. Usage: make worktree-remove BRANCH=plan-42-feature)
endif
	@if [ ! -f "$(WORKTREE_SESSION_CLOSE_SCRIPT)" ]; then \
		echo "Missing session lifecycle module: $(WORKTREE_SESSION_CLOSE_SCRIPT)"; \
		echo "Install or sync the sanctioned session lifecycle module before using make worktree-remove."; \
		exit 1; \
	fi
	@$(MAKE) session-close BRANCH="$(BRANCH)" \
		$(if $(WORKTREE_MERGE_COMMIT),WORKTREE_MERGE_COMMIT="$(WORKTREE_MERGE_COMMIT)",) \
		$(if $(SESSION_NOTE),SESSION_NOTE="$(SESSION_NOTE)",)

review-claim:  ## Create a review claim for TARGET_BRANCH=name WRITE_PATHS="a|b" TASK="..."
ifndef TARGET_BRANCH
	$(error TARGET_BRANCH is required. Usage: make review-claim TARGET_BRANCH=plan-42-feature WRITE_PATHS="src/foo.py|tests/test_foo.py" TASK="Review concern")
endif
ifndef WRITE_PATHS
	$(error WRITE_PATHS is required. Provide one or more repo-relative paths separated by '|')
endif
ifndef TASK
	$(error TASK is required. Describe the review intent)
endif
ifndef SESSION_GOAL
	$(error SESSION_GOAL is required. Name the broader review objective)
endif
ifndef WORKTREE_AGENT
	$(error Unable to infer agent runtime. Set AGENT via WORKTREE_AGENT=codex|claude-code|openclaw)
endif
	@$(PYTHON) "$(WORKTREE_REVIEW_CLAIM_SCRIPT)" \
		--repo-root "$(CURDIR)" \
		--agent "$(WORKTREE_AGENT)" \
		--project "$(WORKTREE_PROJECT)" \
		--target-branch "$(TARGET_BRANCH)" \
		--intent "$(TASK)" \
		--session-name "$(SESSION_GOAL)" \
		--write-path "$(WRITE_PATHS)" \
		$(if $(PLAN),--plan "Plan #$(PLAN)",) \
		$(if $(REVIEW_SCOPE),--scope "$(REVIEW_SCOPE)",) \
		$(if $(REVIEW_NOTES),--notes "$(REVIEW_NOTES)",)

raise-concern:  ## Route concern to TARGET_BRANCH via PR comment or local inbox
ifndef TARGET_BRANCH
	$(error TARGET_BRANCH is required. Usage: make raise-concern TARGET_BRANCH=plan-42-feature SUBJECT="..." MESSAGE="...")
endif
ifndef SUBJECT
	$(error SUBJECT is required. Usage: make raise-concern TARGET_BRANCH=plan-42-feature SUBJECT="..." MESSAGE="...")
endif
ifndef WORKTREE_AGENT
	$(error Unable to infer agent runtime. Set AGENT via WORKTREE_AGENT=codex|claude-code|openclaw)
endif
ifndef MESSAGE
ifndef MESSAGE_FILE
	$(error MESSAGE or MESSAGE_FILE is required. Provide inline content or a path to a concern file)
endif
endif
	@$(PYTHON) "$(WORKTREE_RAISE_CONCERN_SCRIPT)" \
		--repo-root "$(CURDIR)" \
		--agent "$(WORKTREE_AGENT)" \
		--project "$(WORKTREE_PROJECT)" \
		--target-branch "$(TARGET_BRANCH)" \
		--subject "$(SUBJECT)" \
		$(if $(MESSAGE),--content "$(MESSAGE)",) \
		$(if $(MESSAGE_FILE),--content-file "$(MESSAGE_FILE)",) \
		$(if $(RECIPIENT),--recipient "$(RECIPIENT)",)

surface-up:  ## Start the registered canonical UI (SURFACE=id)
	@test -n "$(SURFACE)" || { echo "SURFACE is required" >&2; exit 2; }
	$(PYTHON) "$(SURFACE_RUNTIME_SCRIPT)" --repo-root . up "$(SURFACE)"

surface-preview:  ## Start a registered preview on noncanonical ports (SURFACE=id)
	@test -n "$(SURFACE)" || { echo "SURFACE is required" >&2; exit 2; }
	$(PYTHON) "$(SURFACE_RUNTIME_SCRIPT)" --repo-root . up "$(SURFACE)" --mode preview

surface-status:  ## Show exact surface leases
	$(PYTHON) "$(SURFACE_RUNTIME_SCRIPT)" --repo-root . status

surface-down:  ## Stop the exact selected surface lease (SURFACE=id [LEASE=id])
	@test -n "$(SURFACE)" || { echo "SURFACE is required" >&2; exit 2; }
	$(PYTHON) "$(SURFACE_RUNTIME_SCRIPT)" --repo-root . down "$(SURFACE)" $(if $(LEASE),--lease-id "$(LEASE)",)

surface-audit:  ## Compare registry, lease, process, and served identity (SURFACE=id)
	@test -n "$(SURFACE)" || { echo "SURFACE is required" >&2; exit 2; }
	$(PYTHON) "$(SURFACE_RUNTIME_SCRIPT)" --repo-root . audit "$(SURFACE)" $(if $(REQUIRE_RUNNING),--require-running,)
# <<< META-PROCESS WORKTREE TARGETS <<<

# --- During Implementation ---
.PHONY: test test-quick check

recall:  ## Surface prior findings and failures relevant to work about to start (Q="what you are about to do" [PROJECT=name])
ifndef Q
	$(error Q is required. Usage: make recall Q="wire a donor client into the loop" [PROJECT=research_v3])
endif
	@$(PYTHON) scripts/recall_learnings.py "$(Q)" $(if $(PROJECT),--project "$(PROJECT)",)

test:  ## Run pytest
	$(PYTHON) -m pytest tests/ -v

test-quick:  ## Run pytest (no traceback)
	$(PYTHON) -m pytest tests/ -q --tb=no

check:  ## Run all checks (test, mypy, lint)
	@echo "Running tests... (interpreter: $(PYTHON))"
	@$(PYTHON) -m pytest tests/ -q --tb=short
	@echo ""
	@$(MAKE) check-generated
	@echo ""
	@if [ -d src ] && command -v mypy >/dev/null 2>&1; then \
		echo "Running mypy..."; \
		mypy src/ --ignore-missing-imports; \
	else \
		echo "Skipping mypy (docs-only repo or mypy not installed)."; \
	fi
	@echo ""
	@echo "All checks passed!"

# --- PR Workflow ---
.PHONY: pr-ready pr merge finish pr-auto-check pr-auto

pr-ready:  ## Rebase on main and push
	@git fetch origin main
	@git rebase origin/main
	@git push -u origin HEAD

pr:  ## Create PR (opens browser)
	@gh pr create --fill --web

pr-auto-check:  ## Autonomous PR preflight (branch/clean tree/origin/account)
	@python $(SCRIPTS_META)/pr_auto.py --preflight-only --expected-origin-repo $(PR_AUTO_EXPECTED_REPO) --account $(GITHUB_ACCOUNT)

pr-auto:  ## Autonomous PR create + auto-merge request (non-interactive)
	@python $(SCRIPTS_META)/pr_auto.py --expected-origin-repo $(PR_AUTO_EXPECTED_REPO) --account $(GITHUB_ACCOUNT) --fill --auto-merge

merge:  ## Merge PR (PR=number required)
ifndef PR
	$(error PR is required. Usage: make merge PR=123)
endif
	@python $(SCRIPTS_META)/merge_pr.py $(PR)

finish:  ## Merge PR + cleanup branch (BRANCH=name PR=number required)
ifndef BRANCH
	$(error BRANCH is required. Usage: make finish BRANCH=plan-42-feature PR=123)
endif
ifndef PR
	$(error PR is required. Usage: make finish BRANCH=plan-42-feature PR=123)
endif
	@gh pr merge $(PR) --squash --delete-branch
	@git checkout main && git pull --ff-only
	@git branch -d $(BRANCH) 2>/dev/null || true

# --- Plans ---
.PHONY: plan-tests plan-complete

plan-tests:  ## Check plan's required tests (PLAN=N required)
ifndef PLAN
	$(error PLAN is required. Usage: make plan-tests PLAN=42)
endif
	@python $(SCRIPTS_META)/check_plan_tests.py --plan $(PLAN)

plan-complete:  ## Mark plan complete with verification (PLAN=N required)
ifndef PLAN
	$(error PLAN is required. Usage: make plan-complete PLAN=42)
endif
	@python $(SCRIPTS_META)/complete_plan.py --plan $(PLAN)

# --- Quality ---
STATUS_FRESHNESS_ARGS ?= --repo-root .

.PHONY: input-surface-scan dead-code route route-eval parse-steps mcp-config-review mcp-config-check mcp-on-demand-check mcp-context-cost mcp-context-cost-check mcp-doctor refresh-generated check-generated handoff-index handoff-index-check archive-preflight archive-preflight-check policy-enforcement policy-contract policy-validation-coverage policy-validation-coverage-check ui-learning-receipt-check github-personal-remote-check policy-violations policy-violations-check policy-capture policy-trends policy-actions policy-console policy-finding-disposition enforcement-liveness policy-system-status policy-audit-systemd-install policy-audit-systemd-status policy-feedback policy-friction policy-friction-clusters policy-friction-clusters-json issue-concern policy-review inbox-review inbox-stale promote-to-policy promote-candidates policy-coherence agent-guide agent-guide-check workspace-state worktree-health worktree-health-check worktree-close-plan worktree-close-plan-check metadata-proposal metadata-proposal-check repository-governance-review repository-governance-review-check recoverable-git-preflight workspace-lifecycle-candidate-receipts workspace-lifecycle-candidate-receipts-check workspace-lifecycle-cleanup workspace-lifecycle-cleanup-results-check repo-doc-conformance repo-doc-conformance-check repo-layout-report repo-layout-report-check dossier-coverage dossier-coverage-check portfolio-evidence portfolio-evidence-check ecosystem-navigation-index ecosystem-navigation-index-check ecosystem-navigation-drift ecosystem-navigation-drift-check policy-references policy-references-check canonical-refresh wiki-coverage wiki-publication-health wiki-publication-health-check wiki-backlink-index wiki-backlink-index-check wiki-graph-health wiki-graph-health-check wiki-graph-health-enforce project-membership-check project-graph-check project-graph-audit project-graph-query project-organization-plan project-wiki project-wiki-html project-wiki-mediawiki wiki-artifacts wiki-portfolio wiki-build wiki-serve wiki-import wiki-reset status-freshness

status-freshness:  ## Emit read-only revision-bound receipts (default: this repo; override STATUS_FRESHNESS_ARGS)
	@python scripts/check_status_freshness.py $(STATUS_FRESHNESS_ARGS)

dead-code:  ## Run dead code detection
	@python $(SCRIPTS_META)/check_dead_code.py

refresh-generated:  ## Regenerate derived runtime/publication surfaces; may change files
	@echo "Refreshing active-work registry..."
	@python scripts/generate_active_work_registry.py
	@echo ""
	@echo "Refreshing handoff index..."
	@python scripts/render_handoff_index.py --write
	@echo ""
	@echo "Refreshing compact authority surface..."
	@python scripts/render_authority_stack.py --write
	@echo ""
	@echo "Refreshing active plan queue..."
	@python scripts/render_active_plan_queue.py --write
	@echo ""
	@echo "Refreshing worktree close plan..."
	@python scripts/plan_worktree_closure.py
	@echo ""
	@echo "Refreshing wiki publication health..."
	@$(PYTHON) scripts/check_wiki_publication_health.py
	@echo ""
	@echo "Refreshing MediaWiki artifact bundle..."
	@python scripts/render_wiki_artifacts_mediawiki.py

check-generated:  ## Check generated governance/project surfaces without rewriting them
	@echo "Checking authority-surface integrity..."
	@python scripts/check_authority_surfaces.py --strict-freshness
	@echo ""
	@echo "Checking active plan queue sync..."
	@python scripts/check_active_plan_queue.py
	@echo ""
	@echo "Checking documentation governance structural truth..."
	@python scripts/check_documentation_governance.py
	@echo ""
	@echo "Verifying plan index is in sync with plan files..."
	@python scripts/verify_plan_index_generation.py
	@echo ""
	@echo "Checking markdown links..."
	@python scripts/check_markdown_links.py vision STATUS_LEDGER.md
	@echo ""
	@echo "Checking knowledge-surface triggers..."
	@python scripts/check_knowledge_surface_triggers.py --repo-root .
	@echo ""
	@echo "Reporting claim-liveness violations (report-only)..."
	@python scripts/check_claim_liveness_violations.py || true
	@echo ""
	@echo "Reporting defaults with an unverifiable owning plan (report-only)..."
	@python scripts/check_default_artefact_plan_status.py --repo-root . || true
	@echo ""
	@echo "Checking project graph metadata..."
	@$(MAKE) project-graph-check

handoff-index:  ## Refresh generated ecosystem handoff index
	@python scripts/render_handoff_index.py --write

handoff-index-check:  ## Check generated ecosystem handoff index freshness
	@python scripts/check_handoff_index.py

archive-preflight:  ## Regenerate Plan #207 archive preflight evidence
	@python scripts/generate_archive_preflight.py

archive-preflight-check:  ## Check Plan #207 archive preflight evidence freshness
	@python scripts/generate_archive_preflight.py --check

project-graph-audit:  ## Full PROJECT_GRAPH audit: paths, taxonomy, dangling refs, sparse records
	@python scripts/validate_project_graph_paths.py --project-graph PROJECT_GRAPH.json
	@python scripts/check_project_graph_taxonomy.py --project-graph PROJECT_GRAPH.json --json | python3 -c "\
import json,sys; d=json.load(sys.stdin); cats={'dangling':[e for e in d['errors'] if 'unknown id' in e],'sparse':[e for e in d['errors'] if any(k in e for k in ['capabilities','tags (need','one_liner'])]}; \
print(f'records={d[\"records\"]} errors={len(d[\"errors\"])} dangling={len(cats[\"dangling\"])} sparse={len(cats[\"sparse\"])}'); \
[print(f'  DANGLING: {e}') for e in cats['dangling']]; \
[print(f'  SPARSE:   {e}') for e in cats['sparse'][:20]]; \
sys.exit(1 if cats['dangling'] else 0)"

project-graph-check:  ## Validate PROJECT_GRAPH paths and taxonomy
	@python scripts/validate_project_graph_paths.py --project-graph PROJECT_GRAPH.json
	@python scripts/check_project_graph_taxonomy.py --project-graph PROJECT_GRAPH.json --fail-on hard
	@$(MAKE) project-membership-check
	@python scripts/render_repository_governance_review.py --check
	@python scripts/render_policy_enforcement.py --check
	@python scripts/render_policy_wiki.py --check
	@python scripts/check_wiki_graph_health.py --check --check-backlink-index --enforce-calibrated
	@python scripts/plan_project_organization.py --check
	@python scripts/propose_project_metadata.py --check
	@python scripts/check_project_dossier_coverage.py --check
	@python scripts/render_portfolio_evidence_matrix.py --check
	@python scripts/render_project_wiki.py --check
	@python scripts/render_project_wiki_html.py --check
	@python scripts/render_project_wiki_mediawiki.py --check
	@python scripts/render_portfolio_wiki.py --check

project-membership-check:  ## Validate human-project membership pointers and manifests
	@python scripts/check_project_membership.py --project-graph PROJECT_GRAPH.json

PROJECT_GRAPH_QUERY ?= summary

project-graph-query:  ## Query PROJECT_GRAPH (PROJECT_GRAPH_QUERY='list --area shared-infrastructure')
	@python scripts/query_project_graph.py $(PROJECT_GRAPH_QUERY)

project-organization-plan:  ## Generate docs/PROJECT_ORGANIZATION_PLAN.md without moving repos
	@python scripts/plan_project_organization.py

mcp-config-review:  ## Review global MCP config entries without modifying settings
	@python scripts/check_mcp_config.py

mcp-config-check:  ## Fail if global MCP config has missing commands or justifications
	@python scripts/check_mcp_config.py --strict

mcp-on-demand-check:  ## Fail if an enabled local stdio MCP would start one process per session
	@python scripts/check_mcp_config.py --on-demand-strict

mcp-context-cost:  ## Estimate MCP tools/list context cost (CLIENT=codex SERVER=puppeteer TIMEOUT_SEC=30 optional)
	@python scripts/review_mcp_context_cost.py $(if $(CLIENT),--client $(CLIENT),) $(if $(SERVER),--server $(SERVER),) $(if $(TIMEOUT_SEC),--timeout-sec $(TIMEOUT_SEC),)

mcp-context-cost-check:  ## Strict MCP context-cost review; fails if selected MCP tools/list fails
	@python scripts/review_mcp_context_cost.py --strict $(if $(CLIENT),--client $(CLIENT),) $(if $(SERVER),--server $(SERVER),) $(if $(TIMEOUT_SEC),--timeout-sec $(TIMEOUT_SEC),)

mcp-doctor:  ## Diagnose MCP config, stdio smoke, and session visibility (CLIENT=claude SERVER=social-media SESSION_VISIBLE=unknown)
	@python scripts/mcp_doctor.py $(if $(CLIENT),--client $(CLIENT),) $(if $(SERVER),--server $(SERVER),) $(if $(TIMEOUT_SEC),--timeout-sec $(TIMEOUT_SEC),) $(if $(SMOKE_TOOL),--smoke-tool $(SMOKE_TOOL),) $(if $(SMOKE_ARGS_JSON),--smoke-args-json '$(SMOKE_ARGS_JSON)',) $(if $(SESSION_VISIBLE),--session-visible $(SESSION_VISIBLE),)

policy-enforcement:  ## Regenerate docs/POLICY_ENFORCEMENT_MATRIX.md and wiki/policies.md from policy/registry.yaml
	@$(PYTHON) scripts/render_policy_enforcement.py
	@$(PYTHON) scripts/render_policy_wiki.py

policy-contract:  ## Report policy registry lifecycle/completeness gaps (visibility-first; STRICT=1 gates)
	@$(PYTHON) scripts/check_policy_registry_contract.py $(if $(STRICT),--strict,)

ui-learning-receipt-check:  ## Validate one UI learning receipt (UI_LEARNING_RECEIPT=/absolute/path/file.yaml)
	@if [ -z "$(UI_LEARNING_RECEIPT)" ]; then \
		echo "UI_LEARNING_RECEIPT is required."; \
		echo "Usage: make ui-learning-receipt-check UI_LEARNING_RECEIPT=/absolute/path/to/receipt.yaml"; \
		exit 2; \
	fi
	@$(PYTHON) -c 'import json, pathlib, sys, yaml; from jsonschema import Draft202012Validator, FormatChecker; receipt=pathlib.Path(sys.argv[1]); schema=pathlib.Path(sys.argv[2]); payload=yaml.safe_load(receipt.read_text(encoding="utf-8")); contract=json.loads(schema.read_text(encoding="utf-8")); errors=sorted(Draft202012Validator(contract, format_checker=FormatChecker()).iter_errors(payload), key=lambda e: list(e.absolute_path)); [print("%s: %s" % ("/".join(map(str, e.absolute_path)) or "<root>", e.message)) for e in errors]; sys.exit(1 if errors else 0)' "$(UI_LEARNING_RECEIPT)" "schemas/ui_learning_receipt.schema.json"

policy-validation-coverage:  ## Regenerate docs/POLICY_VALIDATION_COVERAGE.md from registry/test evidence
	@$(PYTHON) scripts/render_policy_validation_coverage.py

policy-validation-coverage-check:  ## Check whether policy validation coverage report is fresh
	@$(PYTHON) scripts/render_policy_validation_coverage.py --check

github-personal-remote-check:  ## Report personal GitHub remotes that do not use github-personal SSH alias
	@python scripts/check_github_personal_remote.py --repo .

policy-feedback:  ## Append typed feedback (TYPE=friction|recommendation POLICY=... RECOMMENDATION=...)
ifndef POLICY
	$(error POLICY is required)
endif
ifndef TYPE
	$(error TYPE is required. Use friction or recommendation)
endif
ifndef RECOMMENDATION
	$(error RECOMMENDATION is required)
endif
ifeq ($(TYPE),friction)
ifndef FRICTION
	$(error FRICTION is required when TYPE=friction)
endif
	@$(PYTHON) scripts/log_policy_friction.py --type friction --policy "$(POLICY)" --friction "$(FRICTION)" --recommendation "$(RECOMMENDATION)" $(if $(SOURCE_REF),--source-ref "$(SOURCE_REF)",)
else ifeq ($(TYPE),recommendation)
ifndef OBSERVATION
	$(error OBSERVATION is required when TYPE=recommendation)
endif
ifndef PRIOR_ART
	$(error PRIOR_ART is required when TYPE=recommendation: what you checked for existing/concurrent work before proposing a new mechanism, in at least 8 words)
endif
	@$(PYTHON) scripts/log_policy_friction.py --type recommendation --policy "$(POLICY)" --observation "$(OBSERVATION)" --recommendation "$(RECOMMENDATION)" --prior-art "$(PRIOR_ART)" $(if $(SOURCE_REF),--source-ref "$(SOURCE_REF)",)
else
	$(error TYPE must be friction or recommendation)
endif

policy-friction:  ## Compatibility alias for typed friction feedback
ifndef POLICY
	$(error POLICY is required. Usage: make policy-friction POLICY=id FRICTION="..." RECOMMENDATION="...")
endif
ifndef FRICTION
	$(error FRICTION is required. Usage: make policy-friction POLICY=id FRICTION="..." RECOMMENDATION="...")
endif
ifndef RECOMMENDATION
	$(error RECOMMENDATION is required. Usage: make policy-friction POLICY=id FRICTION="..." RECOMMENDATION="...")
endif
	@$(MAKE) --no-print-directory policy-feedback TYPE=friction POLICY="$(POLICY)" FRICTION="$(FRICTION)" RECOMMENDATION="$(RECOMMENDATION)"

remote-less-repos:  ## Report git checkouts that have commits but no remote
	@$(PYTHON) scripts/check_remote_less_repos.py

policy-friction-clusters:  ## Render stable recurrence clusters from the raw friction log
	@$(PYTHON) scripts/policy_friction_clusters.py --format markdown

policy-friction-clusters-json:  ## Render machine-readable recurrence clusters
	@$(PYTHON) scripts/policy_friction_clusters.py --format json

policy-auto-cluster:  ## Report exact-recurring unmatched friction labels (dry-run)
	@$(PYTHON) scripts/auto_cluster_recurring_friction.py

policy-auto-cluster-write:  ## Register exact-recurring unmatched friction labels as new clusters
	@$(PYTHON) scripts/auto_cluster_recurring_friction.py --write

issue-concern:  ## Append an unconfirmed concern to ISSUES.md (TITLE=... RISK=... NEXT_ACTION=...)
ifndef TITLE
	$(error TITLE is required. Usage: make issue-concern TITLE="..." RISK="..." NEXT_ACTION="...")
endif
ifndef RISK
	$(error RISK is required. Usage: make issue-concern TITLE="..." RISK="..." NEXT_ACTION="...")
endif
ifndef NEXT_ACTION
	$(error NEXT_ACTION is required. Usage: make issue-concern TITLE="..." RISK="..." NEXT_ACTION="...")
endif
	@python scripts/log_issue_concern.py --title "$(TITLE)" --risk "$(RISK)" --next-action "$(NEXT_ACTION)"

SCAN_REPOS ?= $(HOME)/projects/claimcheck $(HOME)/projects/project-meta $(HOME)/projects/inside-success $(HOME)/projects/onto-canon6

input-surface-scan:  ## Inventory parse/IO call sites outside contained loaders (triad policy visibility; never a gate)
	@python scripts/scan_input_surfaces.py $(SCAN_REPOS)

policy-review:  ## List pending policy proposals in policy/proposals/
	@$(PYTHON) scripts/validate_policy_proposals.py || echo "  (validation errors above are in specific proposal files; the pending list below is unaffected)"
	@$(PYTHON) scripts/list_policy_proposals.py --pending

guard-negative-controls:  ## Which guard scripts have a test that observes them failing (policy show-the-check-failing-before-trusting-it)
	@$(PYTHON) scripts/check_guard_negative_controls.py --list

semantic-fail-loud-check:  ## Validate and execute forced-failure evidence (MANIFEST=path, REPO_ROOT=path)
	@test -n "$(MANIFEST)" || (echo "MANIFEST is required" && exit 2)
	@$(PYTHON) scripts/check_semantic_fail_loud.py --manifest "$(MANIFEST)" --repo-root "$(if $(REPO_ROOT),$(REPO_ROOT),.)" --run-evidence

inbox-review:  ## List open inbox items sorted by review_by
	@python scripts/inbox_review.py

inbox-stale:  ## List stale open inbox items (past review_by date)
	@python scripts/inbox_review.py --stale

promote-to-policy:  ## Scaffold a proposal from an agent_memory finding: make promote-to-policy ID=sm-XXXXXXXX
	@python scripts/promote_to_policy.py $(ID)

promote-candidates:  ## List agent_memory findings that are candidates for policy promotion
	@python scripts/promote_to_policy.py --list-candidates

policy-coherence:  ## Check policy/skill registry coherence against filesystem
	@$(PYTHON) scripts/check_policy_coherence.py

agent-guide:  ## Regenerate policy/wiki/AGENT_GUIDE.md and SKILL_INDEX.md from registry
	@$(PYTHON) scripts/generate_agent_guide.py --write

agent-guide-check:  ## Check whether policy/wiki/AGENT_GUIDE.md is stale
	@$(PYTHON) scripts/generate_agent_guide.py --check

policy-violations:  ## Regenerate stable docs/POLICY_VIOLATION_REPORT.md snapshot
	@$(PYTHON) scripts/check_policy_violations.py

policy-violations-check:  ## Check whether stable policy violation snapshot is fresh
	@$(PYTHON) scripts/check_policy_violations.py --check

policy-capture:  ## Record policy and wiki graph-health findings to the observability time-series
	@$(PYTHON) scripts/policy_observability.py capture

policy-trends:  ## Show policy/wiki finding trends over captured history (chronic/rising/new)
	@$(PYTHON) scripts/policy_observability.py trends

policy-actions:  ## Show the owned policy finding + feedback queue (JSON=1 for the complete UI contract)
	@$(PYTHON) scripts/policy_observability.py actions $(if $(JSON),--json,) $(if $(INCLUDE_CLOSED),--include-closed,) $(if $(LIMIT),--limit "$(LIMIT)",)

policy-console:  ## Serve the policy action workbench (READ_ONLY=1 for a snapshot deployment)
	@$(PYTHON) scripts/policy_console.py $(if $(DB),--db "$(DB)",) $(if $(PORT),--port "$(PORT)",) $(if $(READ_ONLY),--read-only,) $(if $(DEPLOYMENT_LABEL),--deployment-label "$(DEPLOYMENT_LABEL)",)

policy-finding-disposition:  ## Append a finding disposition (FINDING_ID=... DISPOSITION=... OWNER=... RATIONALE=...)
ifndef FINDING_ID
	$(error FINDING_ID is required)
endif
ifndef DISPOSITION
	$(error DISPOSITION is required: accepted_risk, deferred, false_positive, fixed, or superseded)
endif
ifndef OWNER
	$(error OWNER is required)
endif
ifndef RATIONALE
	$(error RATIONALE is required)
endif
	@$(PYTHON) scripts/policy_observability.py disposition \
		--finding-id "$(FINDING_ID)" --status "$(DISPOSITION)" \
		--owner "$(OWNER)" --rationale "$(RATIONALE)" \
		$(if $(EVIDENCE_REF),--evidence-ref "$(EVIDENCE_REF)",) \
		$(if $(REVIEW_AFTER),--review-after "$(REVIEW_AFTER)",) \
		$(if $(OBSERVED_RUN_TS),--observed-run-ts "$(OBSERVED_RUN_TS)",)

enforcement-liveness:  ## Report whether each hard enforcement channel (hooks/CI/audit) is observably live
	@$(PYTHON) scripts/check_enforcement_liveness.py

reachability:  ## Report module reachability across scripts/tests/enforced_planning
	@$(PYTHON) scripts/meta/check_reachability.py --project-root .

reachability-check:  ## Fail if any module became unreachable since the baseline
	@$(PYTHON) scripts/meta/check_reachability.py --project-root . --check

reachability-baseline:  ## Lower the ratchet after retiring modules
	@$(PYTHON) scripts/meta/check_reachability.py --project-root . --write-baseline

repo-stats:  ## Print repetition counters for session start
	@$(PYTHON) scripts/meta/repo_stats_block.py --project-root .

policy-system-status:  ## Report authority, enforcement, observability, feedback, and scheduler state
	@$(PYTHON) scripts/policy_system_status.py $(if $(STRICT),--check,)

policy-audit-systemd-install:  ## Install and enable the user-level recurring policy audit
	@$(PYTHON) scripts/install_policy_audit_systemd.py install --python "$(PYTHON)" --enable-now \
		$(if $(PUBLISH_TARGET),--snapshot-publish-target "$(PUBLISH_TARGET)" \
		--snapshot-publish-receiver "$(PUBLISH_RECEIVER)" \
		--snapshot-remote-install-root "$(PUBLISH_INSTALL_ROOT)" \
		--snapshot-publish-receipt "$(PUBLISH_RECEIPT)",)

policy-audit-systemd-status:  ## Inspect the user-level recurring policy audit timer
	@$(PYTHON) scripts/install_policy_audit_systemd.py status

workspace-state:  ## Write cross-project workspace drift report and file stale-unpushed escalations
	@$(PYTHON) scripts/check_workspace_state.py

worktree-health:  ## Regenerate docs/WORKTREE_HEALTH_REPORT.md from current worktree/claim state
	@python scripts/check_worktree_health.py

worktree-health-check:  ## Check whether docs/WORKTREE_HEALTH_REPORT.md matches current worktree/claim state
	@python scripts/check_worktree_health.py --check

worktree-close-plan:  ## Generate docs/WORKTREE_CLOSE_PLAN.md dry-run close tiers
	@python scripts/plan_worktree_closure.py

worktree-close-plan-check:  ## Check whether docs/WORKTREE_CLOSE_PLAN.md matches current worktree state
	@python scripts/plan_worktree_closure.py --check

metadata-proposal:  ## Generate docs/PROJECT_METADATA_PROPOSAL.md for missing organization metadata
	@python scripts/propose_project_metadata.py

metadata-proposal-check:  ## Check whether docs/PROJECT_METADATA_PROPOSAL.md is fresh
	@python scripts/propose_project_metadata.py --check

repository-governance-review:  ## Generate the review-only Git ownership/publication inventory
	@python scripts/render_repository_governance_review.py --write

repository-governance-review-check:  ## Check the governance review inventory freshness
	@python scripts/render_repository_governance_review.py --check

recoverable-git-preflight:  ## Emit a read-only recoverable-Git authorization receipt
	@python scripts/check_recoverable_git_preflight.py --repo . --action push

workspace-lifecycle-candidate-receipts:  ## Generate read-only receipts for future lifecycle cleanup goals
	@python scripts/generate_workspace_lifecycle_candidate_receipts.py --write

workspace-lifecycle-candidate-receipts-check:  ## Check lifecycle candidate receipts match current observations
	@python scripts/generate_workspace_lifecycle_candidate_receipts.py --check

.PHONY: workspace-lifecycle-ratchet workspace-lifecycle-ratchet-baseline

workspace-lifecycle-ratchet:  ## Fail on lifecycle residue newer than the reviewed/runtime baseline
	@python scripts/check_workspace_lifecycle_ratchet.py

workspace-lifecycle-ratchet-baseline:  ## Explicitly replace the reviewed ratchet bootstrap baseline
	@python scripts/check_workspace_lifecycle_ratchet.py --write-baseline

workspace-lifecycle-cleanup:  ## Dry-run one receipt; pass APPLY=1 to close or PRESERVE_REASON=... to hand off
ifndef ITEM_ID
	$(error ITEM_ID is required. Use an eligible item id from the candidate receipt)
endif
	@python scripts/execute_workspace_lifecycle_cleanup.py --item-id "$(ITEM_ID)" $(if $(filter 1 true yes,$(APPLY)),--apply,) $(if $(PRESERVE_REASON),--preserve-reason "$(PRESERVE_REASON)",)

workspace-lifecycle-cleanup-results-check:  ## Verify closed and preserved cleanup results against Git and claims
	@python scripts/check_workspace_lifecycle_cleanup_results.py

repo-doc-conformance:  ## Generate exact-revision repository documentation conformance reports
	@python scripts/check_repo_documentation_profiles.py

repo-doc-conformance-check:  ## Check repository documentation conformance report freshness
	@python scripts/check_repo_documentation_profiles.py --check

repo-layout-report:  ## Generate report-only universal repository concern-layout observations
	@python scripts/governed_repository_layout.py

repo-layout-report-check:  ## Check universal repository concern-layout report freshness
	@python scripts/governed_repository_layout.py --check

instruction-audit:  ## Audit CLAUDE.md instruction-surface quality across active repos
	@python scripts/audit_instruction_quality.py --all

instruction-audit-repo:  ## Audit one repo's instruction surfaces (REPO=/path/to/repo, default .)
	@python scripts/audit_instruction_quality.py --repo-root $(or $(REPO),.)

blocking-gates:  ## Check that turn-denying hooks leave the agent a way to clear them
	@python scripts/check_blocking_gates.py --check

dossier-coverage:  ## Generate docs/PROJECT_DOSSIER_COVERAGE_REPORT.md from current portfolio project state
	@python scripts/check_project_dossier_coverage.py

dossier-coverage-check:  ## Check whether docs/PROJECT_DOSSIER_COVERAGE_REPORT.md matches current source state
	@python scripts/check_project_dossier_coverage.py --check

portfolio-evidence:  ## Generate docs/PORTFOLIO_EVIDENCE_MATRIX.md from curated portfolio evidence
	@python scripts/render_portfolio_evidence_matrix.py

portfolio-evidence-check:  ## Check whether docs/PORTFOLIO_EVIDENCE_MATRIX.md matches curated portfolio evidence
	@python scripts/render_portfolio_evidence_matrix.py --check

ecosystem-navigation-index:  ## Regenerate generated/ecosystem_navigation_index.json
	@python scripts/render_ecosystem_navigation_index.py

ecosystem-navigation-index-check:  ## Check ecosystem navigation index freshness and contract
	@python scripts/render_ecosystem_navigation_index.py --check

ecosystem-navigation-drift:  ## Regenerate generated/ecosystem_navigation_drift_report.md
	@python scripts/check_ecosystem_navigation_drift.py

ecosystem-navigation-drift-check:  ## Check ecosystem navigation drift report freshness and enforced findings
	@python scripts/check_ecosystem_navigation_drift.py --check --strict

policy-references:  ## Report policy entries claiming enforcement whose linked_scripts do not resolve
	@$(PYTHON) scripts/check_policy_reference_resolution.py

policy-references-check:  ## Fail when a policy entry claims a mechanism that is not there
	@$(PYTHON) scripts/check_policy_reference_resolution.py --strict

canonical-refresh:  ## Fetch canonical checkouts and report any that cannot fast-forward
	@$(PYTHON) scripts/refresh_canonical_checkouts.py

wiki-coverage:  ## Report which active projects publish to the wiki (refuses on a stale checkout)
	@$(PYTHON) scripts/check_wiki_manifest_coverage.py

wiki-publication-health:  ## Regenerate docs/WIKI_PUBLICATION_HEALTH_REPORT.md from wiki publication manifests
	@python scripts/check_wiki_publication_health.py

wiki-publication-health-check:  ## Check whether docs/WIKI_PUBLICATION_HEALTH_REPORT.md matches current source state
	@$(PYTHON) scripts/check_wiki_publication_health.py --check

wiki-backlink-index:  ## Regenerate generated wiki authority->wiki backlink index
	@$(PYTHON) scripts/check_wiki_graph_health.py --write-backlink-index

wiki-backlink-index-check:  ## Check whether docs/WIKI_BACKLINK_INDEX.json matches current wiki links
	@$(PYTHON) scripts/check_wiki_graph_health.py --check-backlink-index --json >/dev/null

wiki-graph-health:  ## Regenerate measured wiki-first navigation graph-health report
	@$(PYTHON) scripts/check_wiki_graph_health.py --write-backlink-index

wiki-graph-health-check:  ## Check whether docs/WIKI_GRAPH_HEALTH_REPORT.md matches current source state
	@$(PYTHON) scripts/check_wiki_graph_health.py --check --check-backlink-index

wiki-graph-health-enforce:  ## Hard-fail calibrated wiki graph defects; backlink findings remain report-only
	@$(PYTHON) scripts/check_wiki_graph_health.py --check --check-backlink-index --enforce-calibrated

project-wiki:  ## Regenerate docs/PROJECT_WIKI.md from PROJECT_GRAPH.json
	@python scripts/render_project_wiki.py

project-wiki-html:  ## Regenerate docs/PROJECT_WIKI.html from PROJECT_GRAPH.json
	@python scripts/render_project_wiki_html.py

project-wiki-mediawiki:  ## Regenerate docs/project_wiki_mediawiki/*.wikitext from PROJECT_GRAPH.json
	@python scripts/render_project_wiki_mediawiki.py

wiki-artifacts:  ## Regenerate docs/wiki_artifacts_mediawiki/*.wikitext from repo wiki manifests
	@python scripts/render_wiki_artifacts_mediawiki.py

wiki-portfolio:  ## Regenerate docs/portfolio_wiki_mediawiki/*.wikitext from wiki/portfolio_pages.yaml
	@python scripts/render_portfolio_wiki.py

wiki-build:  ## Regenerate all project wiki publication bundles
	@python scripts/render_policy_enforcement.py
	@python scripts/render_policy_wiki.py
	@python scripts/check_policy_violations.py
	@python scripts/check_worktree_health.py
	@python scripts/propose_project_metadata.py
	@python scripts/plan_worktree_closure.py
	@python scripts/check_project_dossier_coverage.py
# Artifact pages must be generated before anything validates references to
# them. Previously render_portfolio_evidence_matrix.py ran first and checked
# the artifact list from the *previous* build, so adding a docs/wiki_manifest.yaml
# to a repo could not take effect in the same run: the validator failed on a
# reference whose page this run was about to create.
	@python scripts/render_wiki_artifacts_mediawiki.py
	@python scripts/render_portfolio_evidence_matrix.py
	@python scripts/render_project_wiki.py
	@python scripts/render_project_wiki_html.py
	@python scripts/check_wiki_publication_health.py
	@python scripts/render_project_wiki_mediawiki.py
	@python scripts/render_portfolio_wiki.py

wiki-serve:  ## Start reproducible local MediaWiki preview
	@cd wiki/local_mediawiki && ./setup_local_mediawiki.sh

wiki-import:  ## Import generated project and artifact wiki bundles into local MediaWiki
	@cd wiki/local_mediawiki && python import_wiki_bundle.py

wiki-reset:  ## Delete local MediaWiki runtime state; run wiki-serve afterward to reinstall
	@cd wiki/local_mediawiki && docker compose down
	@rm -rf wiki/local_mediawiki/LocalSettings.php wiki/local_mediawiki/mediawiki-data wiki/local_mediawiki/images

context-load:  ## Inject session-start context for PROJECT (and optional INTENT). E.g. make context-load PROJECT=llm_client INTENT="fix batch embedding"
	@python scripts/knowledge_router.py --project "$(PROJECT)" $(if $(INTENT),--intent "$(INTENT)",) --backend $(or $(BACKEND),graph)

route:  ## Emit a route for ROUTE_REQUEST
	@python scripts/route_discovery.py "$(ROUTE_REQUEST)" $(if $(filter json,$(ROUTE_OUTPUT)),--indent 2,)

discover:  ## Scan 5 repos via tree-sitter, rebuild graph, show discovered boundaries and tools
	@python scripts/code_graph.py --scan --verbose
	@echo ""
	@python scripts/discover_boundaries.py $(if $(filter json,$(ROUTE_OUTPUT)),--json,)

route-eval:  ## Run the frozen route-discovery evaluation harness
	@python scripts/route_discovery_eval.py --format $(ROUTE_OUTPUT)

parse-steps:  ## Parse steps from a plan (PLAN=N required)
ifndef PLAN
	$(error PLAN is required. Usage: make parse-steps PLAN=19)
endif
	@PYTHONPATH=. python $(SCRIPTS_META)/parse_plan.py --plan $(PLAN) --steps

# --- Friction ---
.PHONY: friction friction-summary

friction:  ## Log governance friction (FRICTION="what" IMPACT="how" SUGGESTION="fix")
ifndef FRICTION
	$(error FRICTION is required. Usage: make friction FRICTION="..." IMPACT="..." SUGGESTION="...")
endif
	@python $(SCRIPTS_META)/log_friction.py --friction "$(FRICTION)" --impact "$(IMPACT)" --suggestion "$(SUGGESTION)" --severity $(or $(SEVERITY),medium) --phase $(or $(PHASE),unknown)

friction-summary:  ## Show friction log summary
	@python $(SCRIPTS_META)/log_friction.py --summary

# --- Help ---
.PHONY: help help-meta

help:  ## Show all targets with descriptions
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

help-meta:  ## Show meta-process targets (verbose)
	@echo "Meta-Process Targets:"
	@echo ""
	@echo "  Session:"
	@echo "    status          Show git status"
	@echo "    worktree        Create claimed worktree (BRANCH=... TASK=... [PLAN=N])"
	@echo "    worktree-list   Show claimed worktree coordination status"
	@echo "    worktree-remove Safely remove worktree (BRANCH=...)"
	@echo ""
	@echo "  Development:"
	@echo "    test            Run tests"
	@echo "    check           Run all checks"
	@echo ""
	@echo "  PR Workflow:"
	@echo "    pr-ready        Rebase + push"
	@echo "    pr              Create PR"
	@echo "    pr-auto-check   Preflight autonomous PR flow"
	@echo "    pr-auto         Non-interactive PR + auto-merge request"
	@echo "    merge           Merge PR (PR=number)"
	@echo "    finish          Merge + cleanup (BRANCH=name PR=number)"
	@echo ""
	@echo "  Quality:"
	@echo "    dead-code       Run dead code detection"
	@echo "    route           Emit a route for ROUTE_REQUEST"
	@echo "    route-eval      Run the frozen route-discovery evaluation harness"
	@echo ""
	@echo "  Plans:"
	@echo "    plan-tests      Check plan tests (PLAN=N)"
	@echo "    plan-complete   Complete plan (PLAN=N)"

.PHONY: ui-index
ui-index:  ## Rebuild the ecosystem UI index and its browsable page (generated/ui/ecosystem_ui_index.html)
	$(PYTHON) scripts/generate_ecosystem_ui_index.py
	$(PYTHON) scripts/render_ecosystem_ui_index_page.py

# Complete-file wiki upkeep

## Why

The complete catalog is a reviewed snapshot. Existing native refresh maintains only declared fact blocks; changed files can leave the catalog silently stale.

## What Changes

Extend the existing Lockstep integration with opt-in inventory pending/review/render/check operations. The active coding agent reads changed sources and reviews their summaries. A review names the observed hash and fails if bytes changed. Deterministic refresh never approves semantic meaning or blindly replaces hashes. Reuse Git index membership, the existing inventory and native hook path; no separate LLM service. Repo Docs retains code-documentation ownership.

## Scope and evidence

Source: Brian, 2026-11-13: “i approve proceed” after the recommendation to establish and repair actual wiki upkeep. The existing documentation architecture and Q30 own this gap. Existing native refresh, inventory and semantic review protocol are reused; this extends complete-file navigation rather than restoring retired universal AES governance.

Canonical example: edit a tracked module; hook identifies its pending summary review; the coding agent reads it and explicitly retains or revises the summary for those bytes; renderer updates navigation; check passes. Bypassing review or acknowledging an older hash fails without approving stale prose.

Trace: ordinary pending, refresh and review operations retain daily runtime receipts under ignored `.lockstep/`; a bounded native run and negative cases will be retained under `evidence/runs/`. AI review occurs in the existing native agent session, whose full tool trace is retained for the demonstration; no new model call path is added.

Planning package: docs/planning/planning-package.json
System model: docs/planning/SYSTEM_MODEL.md (documents/implementation/projections), existing inventory represents tracked artifacts; no new domain layer.

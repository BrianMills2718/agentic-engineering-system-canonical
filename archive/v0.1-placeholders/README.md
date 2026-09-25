# v0.1 planning placeholders (archived)

Disposition: **historical**. These eight `component.placeholder.yaml` files are
v0.1 planning placeholders. Each reserved a directory under
`src/agentic_engineering_system/` for a v0.1 component that was never built; no
directory ever held code (at archive time each held only this one file). They
are retained for history, not deleted.

| v0.1 component | was at |
| --- | --- |
| capability_sourcing | `src/agentic_engineering_system/capability_sourcing/component.placeholder.yaml` |
| evidence_assessment | `src/agentic_engineering_system/evidence_assessment/component.placeholder.yaml` |
| execution | `src/agentic_engineering_system/execution/component.placeholder.yaml` |
| gap_reconciliation | `src/agentic_engineering_system/gap_reconciliation/component.placeholder.yaml` |
| learning | `src/agentic_engineering_system/learning/component.placeholder.yaml` |
| normative_context | `src/agentic_engineering_system/normative_context/component.placeholder.yaml` |
| planning | `src/agentic_engineering_system/planning/component.placeholder.yaml` |
| policy_control | `src/agentic_engineering_system/policy_control/component.placeholder.yaml` |

Moved with `git mv` in AES v0.2 roadmap phase 7a (2026-09-25), so `git log
--follow` on each file shows its full history. Their planned-artifact entries
(`ART-V01-*-COMPONENT-PLACEHOLDER-YAML`) were removed from `.aes/target.yaml` by
the accepted plan `.aes/plans/PLAN-AES-ARCHIVE-V01-PLACEHOLDERS.yaml`; see
`proposals/aes-v0.2-greenfield/24-pre-probe-decisions.md` section 20.

Documents that still name the old paths (`docs/architecture/architecture-realization.bootstrap.yaml`,
`generated/bootstrap-normative/`, `evidence/bootstrap-alignment/`) are v0.1
records of that time and are left as they were. The v0.1 provider that did hold
code, `src/agentic_engineering_system/repository_context/`, is not archived: it
is retained with its console script `aes-repo-context` and its tests under
`tests/repository_context/`.

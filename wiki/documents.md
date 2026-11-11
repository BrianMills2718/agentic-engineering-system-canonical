# Documents by folder

Every other document in this repository, by folder, so each one is reachable from the [wiki index](index.md).
The [wiki pages](index.md) are the current account; these documents are the sources they cite, kept as written.
Plans, proposals and evidence record what was intended or observed on their own dates and may be out of date.

## .agentic/events

- [Agentic events](../.agentic/events/README.md) (`.agentic/events/README.md`)

## (repository root)

- [Agentic Engineering System (AES), canonical](../README.md) (`README.md`)

## archive/v0.1-placeholders

- [v0.1 planning placeholders (archived)](../archive/v0.1-placeholders/README.md) (`archive/v0.1-placeholders/README.md`)

## datasets

- [Datasets](../datasets/README.md) (`datasets/README.md`)

## deployment

- [Deployment](../deployment/README.md) (`deployment/README.md`)

## docs/plans

- [Plan #N: [Name]](../docs/plans/TEMPLATE.md) (`docs/plans/TEMPLATE.md`)
- [Goal: A [Goal id]/[Plan #N] commit whose plan differs from its adopted bytes only in progress fields (front-matter status/owner/updated, Status:/Owner: lines, Status/Progress/Notes/Log-style sections) is accepted with the advisory 'plan progress fields changed since adoption; identity unchanged'; any other plan change, or an adopted version not found in the plan file's git history, is still refused with 'plan changed since adoption; re-adopt it'](../docs/plans/adoption-progress-fields.goal.md) (`docs/plans/adoption-progress-fields.goal.md`)
- [Commit rule accepts plan progress-field edits made after adoption](../docs/plans/adoption-progress-fields.md) (`docs/plans/adoption-progress-fields.md`)
- [Goal: One generated capability catalogue (YAML plus an HTML page) lists, for every Project Graph repository on this machine, the capabilities its catalog-info.yaml declares and the tools found in its pyproject scripts, MCP server declarations and Makefile, and flags tools no capability claims and claimed tools that no longer exist](../docs/plans/capability-catalogue.goal.md) (`docs/plans/capability-catalogue.goal.md`)
- [One capability catalogue filled from evidence (first slice)](../docs/plans/capability-catalogue.md) (`docs/plans/capability-catalogue.md`)
- [Goal: aes commit check resolves a Markdown link starting with / against the repository root, then wiki/, so new pages a wiki links root-relatively count as reached](../docs/plans/commit-rule-root-relative-links.goal.md) (`docs/plans/commit-rule-root-relative-links.goal.md`)
- [Commit rule resolves root-relative wiki links](../docs/plans/commit-rule-root-relative-links.md) (`docs/plans/commit-rule-root-relative-links.md`)
- [Goal: A repository under a skip root named in the machine-wide commit-rule file commits without a tag and gets a logged skip; every other repository is judged as before, and no repository file can name a skip root](../docs/plans/commit-rule-skip-roots.goal.md) (`docs/plans/commit-rule-skip-roots.goal.md`)
- [Commit rule: central temp-folder opt-out (issue #488)](../docs/plans/commit-rule-skip-roots.md) (`docs/plans/commit-rule-skip-roots.md`)
- [Goal: A commit whose first line carries a tag the AES commit grammar (commit_rule.TAG_RE) recognises is no longer rejected by a repository's copied prefix-only commit-msg hook, because the generated hook wrapper asks 'aes commit tag' instead of trusting each repo's own regex list](../docs/plans/commit-tag-contract.goal.md) (`docs/plans/commit-tag-contract.goal.md`)
- [Local commit hooks accept every tag the AES commit rule accepts](../docs/plans/commit-tag-contract.md) (`docs/plans/commit-tag-contract.md`)
- [Goal: A [Goal id] commit under a quick plan whose plan names a durable-documents completion command, in a repository that declares durable_documents, runs that check on the commit being made and is refused when the plan fails to name a durable rule whose owner file the change touches (or its declaration is otherwise invalid); an unchanged declared document stays a logged note](../docs/plans/durable-check-commit-rule.goal.md) (`docs/plans/durable-check-commit-rule.goal.md`)
- [Commit rule runs the durable-documents check for quick plans](../docs/plans/durable-check-commit-rule.md) (`docs/plans/durable-check-commit-rule.md`)
- [Goal: docs/rules/RULES.md in AES canonical lists the workspace instruction rules, the feedback loop's rules and project-meta's 263 legacy rules, each with how it is enforced, built from docs/rules/register.yaml](../docs/plans/rules-register.goal.md) (`docs/plans/rules-register.goal.md`)
- [One page listing every rule agents follow](../docs/plans/rules-register.md) (`docs/plans/rules-register.md`)
- [Goal: A [Shaping <id>] commit that adds a new proposal document may also add link lines into proposals/<id>/ in existing Markdown pages or create the first wiki/index.md, so one commit lands the proposal and its navigation; and 'aes commit check --preflight -m <message>' reports the commit rule's verdict on the staged change without logging, before any commit is attempted](../docs/plans/shaping-nav-preflight.goal.md) (`docs/plans/shaping-nav-preflight.goal.md`)
- [A shaping commit can carry its own wiki link; the commit rule runs as a preflight](../docs/plans/shaping-nav-preflight.md) (`docs/plans/shaping-nav-preflight.md`)

## evals

- [Evals](../evals/README.md) (`evals/README.md`)

## evals/plan-002

- [Plan 002 P0 closure runbook](../evals/plan-002/P0_RUNBOOK.md) (`evals/plan-002/P0_RUNBOOK.md`)
- [Plan 002 eval protocol](../evals/plan-002/README.md) (`evals/plan-002/README.md`)

## evidence

- [Evidence](../evidence/README.md) (`evidence/README.md`)
- [Modular-design instruction integration - verification record](../evidence/modular-design-integration-2026-09-22.md) (`evidence/modular-design-integration-2026-09-22.md`)

## evidence/greenfield

- [Clean-user run 2 of the Greenfield getting-started page (2026-09-25)](../evidence/greenfield/clean-user-run-2-2026-09-25.md) (`evidence/greenfield/clean-user-run-2-2026-09-25.md`)
- [Clean-user run of the Greenfield getting-started page (2026-09-25)](../evidence/greenfield/clean-user-run-2026-09-25.md) (`evidence/greenfield/clean-user-run-2026-09-25.md`)
- [Clean-user run 3 of the Greenfield getting-started page (2026-09-25)](../evidence/greenfield/clean-user-run-3-2026-09-25.md) (`evidence/greenfield/clean-user-run-3-2026-09-25.md`)
- [Clean-user run 4 of the Greenfield getting-started page (2026-10-04)](../evidence/greenfield/clean-user-run-4-2026-10-04.md) (`evidence/greenfield/clean-user-run-4-2026-10-04.md`)
- [Context A/B rerun — pre-registration (2026-09-25, AES canonical at 2509ea4)](../evidence/greenfield/context-ab-2026-09-25/preregistration.md) (`evidence/greenfield/context-ab-2026-09-25/preregistration.md`)
- [Context A/B rerun — result (2026-09-25)](../evidence/greenfield/context-ab-2026-09-25/result.md) (`evidence/greenfield/context-ab-2026-09-25/result.md`)

## evidence/plan-001

- [Plan 001 / post-integration characterization](../evidence/plan-001/320991b96a3e3aaa15aa8ba05817a7eee1c52603/characterization.md) (`evidence/plan-001/320991b96a3e3aaa15aa8ba05817a7eee1c52603/characterization.md`)
- [Plan 001 / final revision-bound characterization](../evidence/plan-001/96fcf5e89ba98ad9ff278ec536a98c308cda3fe1/characterization.md) (`evidence/plan-001/96fcf5e89ba98ad9ff278ec536a98c308cda3fe1/characterization.md`)
- [Plan 001 / Attention Checkpoint A1](../evidence/plan-001/a1/53be16fa1159f31648773062531d751c85d7a011.md) (`evidence/plan-001/a1/53be16fa1159f31648773062531d751c85d7a011.md`)
- [Plan 001 / Attention Checkpoint A1 — follow-up](../evidence/plan-001/a1/96fcf5e89ba98ad9ff278ec536a98c308cda3fe1.md) (`evidence/plan-001/a1/96fcf5e89ba98ad9ff278ec536a98c308cda3fe1.md`)
- [Plan 001 / PR #5 integration-readiness record](../evidence/plan-001/pr5-integration-readiness-2026-09-18.md) (`evidence/plan-001/pr5-integration-readiness-2026-09-18.md`)

## experiments

- [Experiments](../experiments/README.md) (`experiments/README.md`)

## generated

- [Generated](../generated/README.md) (`generated/README.md`)
- [Docstring Wiki](../generated/docstring_wiki.md) (`generated/docstring_wiki.md`)

## generated/bootstrap-normative

- [Generated AES normative view bundle](../generated/bootstrap-normative/view-bundle.md) (`generated/bootstrap-normative/view-bundle.md`)

## human-facing

- [Human-facing](../human-facing/README.md) (`human-facing/README.md`)

## operations

- [Operations](../operations/README.md) (`operations/README.md`)

## proposals/aes-adopt-existing

- [Goal: an existing repository joins AES in one command without planning its old files; from then on only files a plan touches need a plan, and aes status shows how much is still legacy](../proposals/aes-adopt-existing/aes-adopt-existing.goal.md) (`proposals/aes-adopt-existing/aes-adopt-existing.goal.md`)

## proposals/aes-brownfield-docs

- [Goal: Inside-Success/brians-2nd-brain-integration-work is organized in AES canonical's layout (decisions in docs/decisions/, governing design in docs/architecture/, plans in docs/plans/, generated output separated from reading), with wiki/index.md routing by question to every reader document within two links](../proposals/aes-brownfield-docs/aes-brownfield-docs.goal.md) (`proposals/aes-brownfield-docs/aes-brownfield-docs.goal.md`)

## proposals/aes-durable-docs

- [Goal: Every governed repository keeps one fixed set of durable documents (goal and thesis, requirements with success criteria, the system model with traceable rules, decision records) that a fresh reader reaches from wiki/index.md, and no plan completes without updating the durable documents it declared](../proposals/aes-durable-docs/aes-durable-docs.goal.md) (`proposals/aes-durable-docs/aes-durable-docs.goal.md`)
- [Cold-reader review: AES canonical (M4)](../proposals/aes-durable-docs/evidence/m4-aes-canonical-cold-reader-review.md) (`proposals/aes-durable-docs/evidence/m4-aes-canonical-cold-reader-review.md`)
- [Cold-reader review (Plan #63, R11)](../proposals/aes-durable-docs/evidence/m4-company-planning-cold-reader-review.md) (`proposals/aes-durable-docs/evidence/m4-company-planning-cold-reader-review.md`)

## proposals/aes-feedback-prevention

- [Goal: New feedback reaches existing failure-pattern review and one real native-agent failure reaches checked prevention](../proposals/aes-feedback-prevention/aes-feedback-prevention.goal.md) (`proposals/aes-feedback-prevention/aes-feedback-prevention.goal.md`)

## proposals/aes-learning-loop

- [Goal: every lesson, friction, problem, experiment and research finding an agent meets becomes a short report whose claims link to their evidence and say how they are known; the loop extracts and sorts the reports, analyses problems that recur, turns licensed claims into enforced rules or checks, and observes whether the failure stops recurring](../proposals/aes-learning-loop/aes-learning-loop.goal.md) (`proposals/aes-learning-loop/aes-learning-loop.goal.md`)

## proposals/aes-plan-scope

- [Goal: in a repository adopted with aes adopt, work planned through Company Planning can edit the legacy files its plan declares, under enforce, while a legacy edit outside every plan's declared scope is still refused](../proposals/aes-plan-scope/aes-plan-scope.goal.md) (`proposals/aes-plan-scope/aes-plan-scope.goal.md`)

## proposals/aes-planning

- [Goal: real implementation work in Brian's repositories lands only under an adopted plan; trivial work is decided by measured facts; adopting a plan writes its /goal text](../proposals/aes-planning/aes-planning.goal.md) (`proposals/aes-planning/aes-planning.goal.md`)

## proposals/aes-v0.2-greenfield

- [AES v0.2 design thesis](../proposals/aes-v0.2-greenfield/01-design-thesis.md) (`proposals/aes-v0.2-greenfield/01-design-thesis.md`)
- [AES v0.2 donor/provider re-entry rule](../proposals/aes-v0.2-greenfield/05-donor-reentry.md) (`proposals/aes-v0.2-greenfield/05-donor-reentry.md`)
- [AES v0.2 unresolved decisions for fresh review](../proposals/aes-v0.2-greenfield/06-open-questions.md) (`proposals/aes-v0.2-greenfield/06-open-questions.md`)
- [AES v0.2 Greenfield MVP validation profile](../proposals/aes-v0.2-greenfield/10-greenfield-mvp-validation-profile.md) (`proposals/aes-v0.2-greenfield/10-greenfield-mvp-validation-profile.md`)
- [AES v0.2 Greenfield MVP materialization candidate](../proposals/aes-v0.2-greenfield/13-greenfield-materialization.candidate.md) (`proposals/aes-v0.2-greenfield/13-greenfield-materialization.candidate.md`)
- [AES v0.2 provider evaluation — round 1](../proposals/aes-v0.2-greenfield/18-provider-evaluation-round-1.md) (`proposals/aes-v0.2-greenfield/18-provider-evaluation-round-1.md`)
- [AES v0.2 provider evaluation — round 2: generic dependencies](../proposals/aes-v0.2-greenfield/19-provider-evaluation-round-2-generic-dependencies.md) (`proposals/aes-v0.2-greenfield/19-provider-evaluation-round-2-generic-dependencies.md`)
- [AES v0.2 portable provider boundaries](../proposals/aes-v0.2-greenfield/22-portable-provider-boundaries.md) (`proposals/aes-v0.2-greenfield/22-portable-provider-boundaries.md`)
- [AES v0.2 Greenfield CLI/product contract](../proposals/aes-v0.2-greenfield/23-greenfield-cli-product-contract.md) (`proposals/aes-v0.2-greenfield/23-greenfield-cli-product-contract.md`)

## proposals/code2-ecosystem

- [Goal: A fresh ~/code2 folder holds AES canonical, wiki_methodology and epistemic-warrant, moved in without breaking anything, with an instruction file that carries Brian's safety rules; epistemic-warrant's wiki is converted to the selected llm-wiki tool's format so Brian can look at it before more repositories follow](../proposals/code2-ecosystem/code2-ecosystem.goal.md) (`proposals/code2-ecosystem/code2-ecosystem.goal.md`)

## proposals/commit-rule-followups

- [Goal: The AES commit rule logs, for a [Goal <id>] commit whose plan was made by quick-adopt, whether the commit adds the plan's saved check output and stays inside the plan's file list, and it treats test setup files and scripts run by systemd units as running things that [Trivial] may not touch](../proposals/commit-rule-followups/commit-rule-followups.goal.md) (`proposals/commit-rule-followups/commit-rule-followups.goal.md`)

## proposals/commit-rule-notes-report

- [Goal: The daily commit-rule report counts, per day and repository, [Goal] commits whose quick-plan notes say the saved check output is missing or files fall outside the plan's list, records the counts in its per-day line, and opens or updates the keyed concern aes-quick-plan-drift naming those commits when any occur](../proposals/commit-rule-notes-report/commit-rule-notes-report.goal.md) (`proposals/commit-rule-notes-report/commit-rule-notes-report.goal.md`)
- [The daily commit-rule report reads the quick-plan notes and raises problems](../proposals/commit-rule-notes-report/commit-rule-notes-report.md) (`proposals/commit-rule-notes-report/commit-rule-notes-report.md`)

## proposals/commit-tag-case

- [Goal: A commit tagged [Goal PATH-brent-v1-2026-10-02] or [Shaping Some-Plan] is read as a plan tag and judged against that plan, instead of being refused as having no tag](../proposals/commit-tag-case/commit-tag-case.goal.md) (`proposals/commit-tag-case/commit-tag-case.goal.md`)

## proposals/doc-reach-new-docs

- [Goal: In Brian's repositories, a commit that adds a document a reader is meant to open is refused unless wiki/index.md reaches it within two links, and the refusal names the exact link line to add; documents that already exist are left to the per-repository cleanup](../proposals/doc-reach-new-docs/doc-reach-new-docs.goal.md) (`proposals/doc-reach-new-docs/doc-reach-new-docs.goal.md`)

## proposals/harness-context

- [Goal: Brian can see which harness rules actually work and route a real bounded investigation to a native specialist with only the context it needs](../proposals/harness-context/harness-context.goal.md) (`proposals/harness-context/harness-context.goal.md`)

## proposals/meeting-claims-true

- [Goal: Every checkable claim Brian made in the 2026-10-08 SD - AI Astronaut meeting is true of the running systems, and the second brain answers Tyler's Slack-only positions correctly](../proposals/meeting-claims-true/meeting-claims-true.goal.md) (`proposals/meeting-claims-true/meeting-claims-true.goal.md`)

## proposals/second-brain-evaluation

- [Goal: For the Inside Success second brain, each feature in the feature register shows whether it works today, whether people use it, and whether its answers are good, each reading backed by a reviewed run trace; the first measure (Tyler's positions from the June gold set) is fixed, traced and re-measured after the Slack retrieval fix](../proposals/second-brain-evaluation/second-brain-evaluation.goal.md) (`proposals/second-brain-evaluation/second-brain-evaluation.goal.md`)

## proposals/worktree-plan-lookup

- [Goal: An installed commit hook admits an actually adopted plan from its owning repository while preserving the caller's staged changes](../proposals/worktree-plan-lookup/worktree-plan-lookup.goal.md) (`proposals/worktree-plan-lookup/worktree-plan-lookup.goal.md`)

## research/investigations

- [OPA / Rego fit probe against Enforced Planning](../research/investigations/2026-09-17-opa-enforced-planning-policy-probe.md) (`research/investigations/2026-09-17-opa-enforced-planning-policy-probe.md`)
- [W3C PROV / in-toto projection probe against AES verification evidence](../research/investigations/2026-09-17-prov-intoto-aes-verification-projection-probe.md) (`research/investigations/2026-09-17-prov-intoto-aes-verification-projection-probe.md`)
- [TOSCA 2.0 projection probe against ACA capability metadata](../research/investigations/2026-09-17-tosca-aca-capability-projection-probe.md) (`research/investigations/2026-09-17-tosca-aca-capability-projection-probe.md`)
- [Investigations](../research/investigations/README.md) (`research/investigations/README.md`)

## research/sources

- [Research sources](../research/sources/README.md) (`research/sources/README.md`)

## research/synthesis

- [External documentation semantics for the AES normative record model](../research/synthesis/2026-09-17-external-document-semantics-for-normative-model.md) (`research/synthesis/2026-09-17-external-document-semantics-for-normative-model.md`)
- [Normative/component alignment dogfood checkpoint](../research/synthesis/2026-09-17-normative-component-alignment-dogfood-checkpoint.md) (`research/synthesis/2026-09-17-normative-component-alignment-dogfood-checkpoint.md`)
- [Proposed AES canonical skeleton after external sourcing](../research/synthesis/2026-09-17-proposed-aes-canonical-skeleton-after-sourcing.md) (`research/synthesis/2026-09-17-proposed-aes-canonical-skeleton-after-sourcing.md`)
- [Source-local normative context dogfood result](../research/synthesis/2026-09-17-source-local-context-dogfood-result.md) (`research/synthesis/2026-09-17-source-local-context-dogfood-result.md`)

## scripts

- [Scripts](../scripts/README.md) (`scripts/README.md`)

## tests

- [Tests](../tests/README.md) (`tests/README.md`)

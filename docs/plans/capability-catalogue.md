---
schema_version: "1.0"
artifact_type: design_plan
id: capability-catalogue
plan_id: capability-catalogue
status: proposed
method_conformance_receipt: docs/plans/capability-catalogue.receipt.json
goal:
  outcome: "One generated capability catalogue (YAML plus an HTML page) lists, for every Project Graph repository on this machine, the capabilities its catalog-info.yaml declares and the tools found in its pyproject scripts, MCP server declarations and Makefile, and flags tools no capability claims and claimed tools that no longer exist"
  canonical_example: "DIGIMON's row shows capability documents_to_text with status selected, implementation docling (not yet a declared dependency) and boundary unresolved, and lists its MCP tool get_config as unclaimed"
  forbidden_substitutes: "a count of entries without checking named members; a catalogue entry with no evidence line; a boundary pointing at a data_contracts type that does not exist; a page checked only by reading its source; a new descriptor format instead of the Backstage entity format"
  boundaries: "only the files listed under Vertical and reset, in AES canonical, DIGIMON, agentic-capability-architecture-canonical and ecosystem-ops; no Backstage server; no edit to company-planning's checklist; no private data published; every change revertible by git revert"
  done_when: "tests/test_capability_catalogue.py passes; the generated catalogue contains DIGIMON's documents_to_text and ACA's three reuse candidates with their evidence; the page shows a styled tooltip on hover for every control in a real browser; the PRs in the four repositories are merged after each repository's own checks. The check output is committed as docs/plans/capability-catalogue.check.txt"
  do_not_gate_on: "Brian's review of the page; the system-models session's own descriptor work; the live publish succeeding before the next 15-minute control-publish run"
---

# One capability catalogue filled from evidence (first slice)

Each section below answers the checklist items quoted in it; the gate judges only that
section's text.

## Actor and result

> **CORE-ACTOR-RESULT-EXAMPLE** (blocking): The plan names the actor it serves, the desired result, and one stable, concrete, user-visible example of that result.

**Actor:** an agent (or Brian) about to plan new work, who needs to know whether a capability
already exists somewhere in the ecosystem before building it (Decision 0012 item 3). Brian,
2026-10-08: the catalogue "should really be a part of agentic engineering system canonical and
company planning which is what my ecosystem is moving towards".

**Result:** one catalogue, `generated/capabilities/capability_catalogue.yaml` and its page
`generated/capabilities/capability_catalogue.html`, built by `scripts/catalogue/` from each
repository's Backstage `catalog-info.yaml` plus tools discovered from the repository's own
files, published at control.brianmills.dev/capabilities/ behind the existing password gate.

**Example:** on the page, the DIGIMON row lists `documents_to_text` (status selected,
implementation docling, boundary unresolved) and shows `get_config` among its unclaimed MCP
tools; the ACA row lists `documents_to_text`, `approval_action_workflow` and
`twitterapi_io_search_candidates_wrapper`, each pointing back to its `reuse_candidates.yml` id.

## Success and disproof

> **CORE-SUCCESS-DISPROOF** (blocking): The plan defines the evidence that would show success and a concrete condition that would disprove the approach.

> **CORE-TRACE-REVIEW** (blocking): Every success or acceptance criterion in the plan is judged from the full trace of a run, not only its final outcome: it names the run whose full trace is examined (for example the session, its tool and LLM calls, commits, check output, or messages), where that trace lives, and what must be seen in that trace beyond the final outcome. A criterion that names only an outcome, such as tests passing, a PR merged, a test fixture reproducing the journey, or a status reading succeeded, fails this item. A criterion for which no run exists, such as a pure document edit, passes only when the plan states that exemption and its reason explicitly.

**Success evidence:** (1) `tests/test_capability_catalogue.py` passes, asserting membership:
DIGIMON's `documents_to_text` present with implementation `docling`, ACA's three candidate ids
present, a fixture repository's unclaimed tool and missing claimed tool both flagged, and an
invalid Backstage descriptor rejected; (2) the collector run over the real Project Graph prints
per-repository counts (capabilities, tools, unclaimed tools, missing tools) and the same named
members; (3) a real-browser check hovers every visible control on the page and finds a styled
tooltip for each; (4) the four PRs are merged after their repositories' own checks.

**Disproof:** the collector cannot read a repository's tools without scanning its whole source
tree, or a Backstage-conformant descriptor cannot carry capabilities without a parallel format
(the spec extension is rejected by the Backstage schema). Either would show the design wrong.

**Trace review:** the runs examined are (a) the success check, run once on the commit that
makes the change, with its full output, exact command and exit status saved as
`docs/plans/capability-catalogue.check.txt`; (b) the collector run over the real Project Graph,
whose full stdout (per-step timing and per-repository counts) is saved in the same file; (c) the
browser check's output (each control's selector and the tooltip text it showed) saved in the
same file. Beyond the final result the trace must show: each test by name with its result and
none skipped; the named members above in the collector output, not only totals; the number of
repositories read and skipped with reasons; and every hovered control with its tooltip text. No
model, agent or LLM pipeline runs under this plan.

## System model

> **CORE-SYSTEM-MODEL** (blocking): The plan links the project's system model (a path such as docs/model/ODD.md) or carries the one-line exemption `System model: exempt -- <reason>`, which fits only a project with no stored state and no user-facing view. Unless exempt, the plan names each system-model element (entity, process, record or event, or view) that the work adds, changes, or relies on, and its trace review names, for each such element, what the examined run must show of it (for example an event of that record type with its id, or the view displaying that entity). A plan with neither a model link nor the exemption line fails this item, as does one that lists model elements without saying what the examined run must show of each, or one that names no element without stating that the work touches none and why.

**System model:** `generated/capabilities/capability_catalogue.yaml` (its record shape is
documented in the collector's module docstring, `scripts/catalogue/collect_capability_catalogue.py`).

**Model elements this change adds, and what the saved check output must show of each:**

- capability record (id, status, implementations, tools, boundary, evidence): DIGIMON's
  `documents_to_text` with status `selected`, implementation `docling` and boundary
  `unresolved`, shown in the collector output;
- tool record (kind cli, mcp or make; name; source file): DIGIMON's MCP tool count and the CLI
  `digimon`, shown in the collector output;
- unclaimed-tool and missing-tool flags: the fixture test shows one of each, and the real run
  prints DIGIMON's unclaimed list including `get_config`;
- the catalogue page (view): the browser check output shows the DIGIMON row and every
  control's tooltip.

## Authority and non-goals

> **CORE-AUTHORITY-NONGOALS** (blocking): The plan states who holds authority over the work and what it explicitly will not do (non-goals).

**Authority:** Brian asked for this; all four repositories are his (BrianMills2718). The
catalogue's authority is Decision 0012 (one catalogue, filled from evidence; ACA's
`reuse_candidates.yml` and `capability_registry.yml` named in PR #456); Decision 0005 picks
Backstage for the operational software-catalogue projection; Decision 0009 folds ACA into AES.

**Non-goals:** no Backstage server; no change to company-planning's adoption checklist (its
CORE-CAPABILITY-REUSE item belongs to another session); no edit to ACA's `reuse_candidates.yml`
or `capability_registry.yml` (the descriptor points at their ids, it does not replace them); no
change to what any repository does; no retirement of the ecosystem-ops capabilities dashboard
in this slice (recorded as a follow-up); no whole-source scan of any repository.

## Irreversible actions and spend

> **CORE-IRREVERSIBLE-SPEND** (blocking): For each irreversible action or spend the plan proposes, it names the boundary, who must authorize it, and how it is contained.

None. Publishing the page on control.brianmills.dev is reversible (revert the copy step; the
next 15-minute publish removes it) and covered by Brian's standing deploy rule for his own sites
when no private data is published. The page holds repository names, tool names, dependency names
and local paths, none of which is private data under the workspace rule; it is still served only
behind the one-password gate. No spend.

## Uncertainties

> **CORE-UNCERTAINTIES** (blocking): The plan lists its material uncertainties, and each one has an owner or the evidence that would resolve it.

| Uncertainty | Owner or resolving evidence |
| --- | --- |
| Whether Backstage accepts a `spec.capabilities` extension | Resolved: the Backstage Component and API JSON schemas (backstage/backstage master, `packages/catalog-model/src/schema/kinds/*.v1alpha1.schema.json`, fetched 2026-10-08) set no `additionalProperties: false` on `spec`; the validator checks the required fields they name |
| Whether a data_contracts passage type exists for documents_to_text | Resolved: data-contracts origin/master b87ca90 has `GovernedEvidenceSpan`, `EvidenceSpan` and `SourceClaimEvidenceSpanV1` (claim evidence spans), none a document passage with page and position; boundary marked unresolved |
| Whether Makefile scaffolding targets (worktree, session-*) drown real tools | Owner: this session; evidence: the collector marks a target shared scaffolding when it appears in ten or more repositories' Makefiles and reports it separately; the real-run counts show the split |
| Whether the system-models session writes DIGIMON's catalog-info.yaml in a conflicting shape | Owner: this session; evidence: its goal (observation-to-action-metamodel GOAL_SYSTEM_MODELS.md) uses the same Backstage Component; the parent session is told so the second writer extends the same file |
| Whether the publish route is reusable | Resolved: ecosystem-ops `deploy/cloudflare-control/prepare_snapshot.py` already copies `/uis/` from `~/.local/share/ui-index/`; one copy function and one build script reuse it, the gate covers every path |

## Activation facts

> **CORE-ACTIVATION-FACTS** (blocking): No activation fact that the plan triggers is declared false. Declaring a fact true when the plan does not strictly need it is acceptable, because it only adds checks; judge only facts declared false. empirical_comparison_proposed is triggered when the plan proposes an A/B test, benchmark, bake-off, or other experiment comparing alternative designs, models, or candidates to choose among them; checking the built result against an expected outcome (an acceptance test, fixture replay, or regression check) is verification and does not trigger it. shared_mechanism is triggered by a new shared mechanism, contract, or algorithm; llm_central by behavior that centrally depends on LLM calls; irreversible_or_spend_action by a proposed irreversible action or spend.

shared_mechanism is true (a cross-repository collector and descriptor convention).
empirical_comparison_proposed is false: nothing compares alternatives; tests check the built
result. llm_central is false: no LLM call. irreversible_or_spend_action is false: see above.

## Prior art and ownership

> **OV-PRIOR-ART-DISPOSITION** (blocking): Existing ownership, internal lineage, and relevant external prior art were searched, and each candidate found is dispositioned as reuse, extend, compose, supersede, or bounded exception.

> **OV-PRIOR-ART-PARALLEL-CHECK** (advisory): The plan names one concrete structural check or consumer-path observation that would detect a silent parallel implementation of the same concern.

**Searches run (2026-10-08), and what each found:**

- Ownership: AES `docs/decisions/` read on origin/main (0005, 0009, 0012 found the Backstage
  projection, the ACA fold-in and the one-catalogue rule); `check_coordination_claims.py --check`
  for the four repositories (found the system-models claim on DIGIMON).
- Internal lineage: project-meta `PROJECT_GRAPH.json` and `scripts/` (found the UI index
  generator and renderer); ecosystem-ops `deploy/cloudflare-control/` and its `ui/registry.yaml`
  (found the control publish route and the existing `capabilities-dashboard` / `tools-dashboard`
  surfaces); ACA `tools/` and its two YAML files; the workspace for other `catalog-info.yaml`
  files (found the observation-to-action-metamodel goal that plans them, none yet written).
- External prior art: the Backstage catalog-model JSON schemas (backstage/backstage master,
  fetched 2026-10-08) and descriptor format; data-contracts origin/master for a passage type.

The candidate set is the union of those results; any later-found registry is caught by the
parallel check below.

| Candidate | Disposition |
| --- | --- |
| Backstage software catalog descriptor (`catalog-info.yaml`, Component/API entities) | **Reuse** the format (Decision 0005); no server. Capabilities go in `spec.capabilities`, which the schema allows |
| project-meta `generate_ecosystem_ui_index.py` + `render_ecosystem_ui_index_page.py` | **Reuse the approach**: Project Graph records through `publishable_records` rules (private records skipped), working tree else default branch, YAML out then a rendered page |
| ecosystem-ops control publish (`prepare_snapshot.py`, `build_ui_index.sh`, ui-index timer, one-password gate) | **Extend**: one copy function and one build script beside the UI index's |
| ACA `reuse_candidates.yml` / `capability_registry.yml` (Decision 0012 authority) | **Compose**: ACA's descriptor points at each candidate id (`source: reuse_candidates.yml#<id>`) and the collector fails the entry when the id is gone, so the files stay the authority |
| ACA `tools/capability_catalog.py` (lists ACA's own packages) | **Bounded exception**: scope is one repository's Frappe packages; not replaced |
| ecosystem-ops `capability_registry.py` / dashboard.brianmills.dev/capabilities | **Supersede (later)**: Decision 0012 makes it a view or retires it; this slice registers the new page and records the retirement as a follow-up |
| observation-to-action-metamodel system-models goal (Backstage descriptors for seams) | **Compose**: same file and Component entity; this slice adds capabilities, that one adds system/API seams |

**Parallel check:** the collector reports every repository holding a file named
`capability_registry.*` or `reuse_candidates.*`; a new one appearing outside ACA in that report
is a silent parallel catalogue.

## Coordination

> **OV-COORD-OWNERSHIP** (blocking): The plan names exact ownership, dependencies, conflict surfaces, the integration owner, and the work-unit evidence for each concurrent writer.

**Owner and integration owner:** this session (claim `agentic-engineering-system-canonical:capability-catalogue`, worktree `worktrees/capability-catalogue`), one writer for every file below.

**Concurrent writer:** the system-models session (observation-to-action-metamodel
`GOAL_SYSTEM_MODELS.md`), live claim `Digimon_for_KG_application:System model and catalog
descriptor (roadmap row 7)` over `docs/model` and `tests/test_system_model.py`. Conflict
surface: `catalog-info.yaml` at the root of DIGIMON (and later AES). This plan writes DIGIMON's
file first, as a Backstage Component that session's goal also uses; the parent session is told
so the later writer adds its `system`/`providesApis` fields to the same entity. Work-unit
evidence: `check_coordination_claims.py --check --project Digimon_for_KG_application`
(2026-10-08) shows its claim does not cover `catalog-info.yaml`.

**Dependencies:** the ACA and DIGIMON PRs need nothing from AES; the AES collector tolerates a
repository without a descriptor; the ecosystem-ops publish step tolerates a missing catalogue.

## Vertical and reset

- AES canonical: `scripts/catalogue/collect_capability_catalogue.py`,
  `scripts/catalogue/render_capability_catalogue_page.py`, `tests/test_capability_catalogue.py`,
  `generated/capabilities/capability_catalogue.yaml`, `generated/capabilities/capability_catalogue.html`,
  `wiki/index.md`, and this plan's records under `docs/plans/capability-catalogue.*`.
- DIGIMON (BrianMills2718/digimon_application_20260215): `catalog-info.yaml`.
- agentic-capability-architecture-canonical: `catalog-info.yaml`.
- ecosystem-ops: `deploy/cloudflare-control/prepare_snapshot.py`,
  `deploy/cloudflare-control/build_capability_catalogue.sh`,
  `deploy/cloudflare-control/systemd/capability-catalogue.{service,timer}`,
  `deploy/cloudflare-control/README.md`, `ui/registry.yaml`.

Reset: `git revert` of each merge.

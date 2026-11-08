# AES v0.2 greenfield architecture (accepted)

Status: **accepted** by [Decision 0010](../../decisions/0010-greenfield-v0.2-accepted.md)
(2026-09-25).

These are the accepted architecture documents of the AES v0.2 greenfield MVP.
Each is a plain copy of a candidate in
[`proposals/aes-v0.2-greenfield/`](../../../proposals/aes-v0.2-greenfield/README.md)
(copied, not `git mv`'d, so the proposal lineage keeps its history), renamed
without `.candidate`, marked accepted, and amended where what was built differs
from what was proposed. Every amendment is listed at the end of its file
(`accepted_amendments:` in YAML, "Accepted amendments" in Markdown), with its
reason and source.

**Current boundary (2026-11-07).** AES's former self-governance is on hold; its mandatory commit refusal and plan-accept workflow are retired. [Lockstep is the active AES component](../../../wiki/index.md#current-boundary-lockstep-and-the-retained-aes-engine) carrying structured linkage and bidirectional projection, with coding agents and Project Brains as consumers. This architecture records the retained engine contract and historical governance, not a restart instruction.

**Library input policy (2026-11-07).** The retained engine's `evidence.assess(root, required_dependency_paths=None)` and `reconcile.reconcile(root, required_dependency_paths=None)` accept a mapping `{verification_subject_id: [repository_relative_path, ...]}`. This is a consumer-owned declaration policy, not a new record shape or governance workflow. AES keeps freshness, route inference and standing computation in the existing engine. Ordinary calls remain unchanged.

A current observation missing applicable required declared paths is reported UNKNOWN with those missing paths and cannot contribute to standing. Directory coverage includes descendants, using normalized literal repository paths; unsafe or outside paths fail. Modern observations use `dependency_basis.declared`, and older records without a basis use `dependency_paths`. A legacy observation naming a criterion instead of a verification subject is routed through its assessed evidence requirements. Stored records and actual assessments remain intact; a correctly qualified current refutation still wins. The existing `record(..., depends_on=[...])` API records those explicit inputs. See [the input-policy specification](../../../openspec/specs/required-evidence-inputs/spec.md) and `tests/greenfield/test_evidence.py`.

**Read-only Git inspection (2026-11-08).** Characterization and source-checkout producer identity disable repository hooks and fsmonitor commands on their existing Git readers. This prevents executable repository integrations from running during structural inspection while retaining actual HEAD, dirty-state and AST facts. The public APIs and stored record shapes are unchanged. See [the inert inspection specification](../../../openspec/specs/inert-characterization/spec.md).

**Historical engine authority.** [`.aes/target.yaml`](../../../.aes/target.yaml)
records ids, criteria, evidence requirements, components,
planned artifacts and verification subjects are what the target says. These
documents explain and constrain it; where one disagrees with the target or the
code, the document is wrong and is corrected. Consumers using this engine change
their target through `aes plan prepare / validate / accept`; this is not a universal requirement on current AES repository changes.

File names mentioned inside these documents that are not in this directory
(for example `18-provider-evaluation-round-1.md`) refer to the proposal
lineage directory.

| File | What it defines | Source proposal |
| --- | --- | --- |
| [`02-semantic-model.yaml`](02-semantic-model.yaml) | the clean semantic model: target, current, gap, evidence, standing | `02-semantic-model.candidate.yaml` |
| [`03-lifecycle.yaml`](03-lifecycle.yaml) | state classes and lifecycle transitions | `03-lifecycle.candidate.yaml` |
| [`04-greenfield-mvp.yaml`](04-greenfield-mvp.yaml) | the MVP's product outcome, supported scope and minimum acceptance | `04-greenfield-mvp.candidate.yaml` |
| [`12-greenfield-mvp-semantic-instance.yaml`](12-greenfield-mvp-semantic-instance.yaml) | the MVP target instance: `OUT-GF-001`, `GF-REQ-001..009`, `SC-GF-001..009` and their evidence requirements (`tests/greenfield/test_self_governance.py` asserts the live target's texts match this file) | `12-greenfield-mvp-semantic-instance.candidate.yaml` |
| [`13-greenfield-materialization.md`](13-greenfield-materialization.md) | the `.aes/` storage convention | `13-greenfield-materialization.candidate.md` |
| [`14-initialization-contract.yaml`](14-initialization-contract.yaml) | what `aes init` creates | `14-initialization-contract.candidate.yaml` |
| [`15-planning-contract.yaml`](15-planning-contract.yaml) | the plan prepare / validate / accept transaction | `15-planning-contract.candidate.yaml` |
| [`16-record-shapes.yaml`](16-record-shapes.yaml) | project, target, plan and observation record shapes | `16-record-shapes.candidate.yaml` |
| [`20-realization-topology.yaml`](20-realization-topology.yaml) | the ten components, planned artifacts and verification subjects of AES itself | `20-realization-topology.candidate.yaml` |
| [`23-greenfield-cli-product-contract.md`](23-greenfield-cli-product-contract.md) | the `aes` command surface and the greenfield happy path | `23-greenfield-cli-product-contract.md` |

Not promoted (they remain proposal lineage only): the provider-evaluation and
provider-binding candidates (`17`, `18-internal-…`, `19-public-…`, `21`), the
review manifest, and the narrative review and decision files (`01`, `05`–`11`,
`18`/`19` rounds, `22`, `24`, `25`, `REVIEW.md`). `24-pre-probe-decisions.md`
and `25-roadmap-to-mvp-acceptance.md` remain the record of how the MVP was
built and why; Decision 0010 carries forward their standing decisions.

Users start at [`docs/greenfield/GETTING_STARTED.md`](../../greenfield/GETTING_STARTED.md).

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

**Authority.** For AES canonical, [`.aes/target.yaml`](../../../.aes/target.yaml)
is the live authority: ids, criteria, evidence requirements, components,
planned artifacts and verification subjects are what the target says. These
documents explain and constrain it; where one disagrees with the target or the
code, the document is wrong and is corrected. The target itself changes only
through `aes plan prepare / validate / accept`.

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

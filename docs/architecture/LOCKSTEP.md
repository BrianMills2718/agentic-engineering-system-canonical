---
description: Lockstep plans linked behavioral structure and projects normative intent and observed status between code and documentation
status: current
---

# Lockstep: planned behavior at the point of implementation

Status: component architecture and implementation account, checked against source on
2026-11-13. This document explains the component; it does not certify every consumer
or make a new behavior requirement. The normative boundary is
[SYSTEM_BOUNDARY.md](SYSTEM_BOUNDARY.md), especially AES-SYS-006, AES-CTX-002,
AES-CTX-004 and AES-POL-002. The accepted consolidation design is
[one planning tool](../../proposals/one-planning-tool/DESIGN.md).

## Why it exists

Lockstep helps autonomous coding agents implement intended behavior effectively.
An agent should encounter the behavior, its boundaries and how it will be judged
where it writes the code, rather than reconstructing intent from distant documents.
Lockstep is the planning-and-checking component of AES; coding agents and Project
Brains consume it. AES also includes the feedback loop and policy layer.

Its opinionated approach starts with planned structure: name the behavioral units,
the files that hold them, their public typed seams, the requirements they implement
and the tests or other checks that establish success. Then implement inside those
boundaries. The linked chain is requirement → success criterion → proving test or
check → file → symbol. A file list alone does not express the intended approach;
a working test alone does not establish that the right behavior was chosen.

This is the architectural intent, not an automatic decomposition algorithm. A
planning agent or person supplies the decomposition. Current layout rows can name
multiple requirements per file and make typed exports optional; Lockstep does not
require one function or one file per behavioral unit. The retained [behavior checker](../../src/lockstep/behavior_check.py) has a
stronger legacy contract: each behavior in AES target records has exactly one
source file of its own and a criterion with a proving route. Modern layout rows
do not populate that same record structure, so the legacy check does not establish
that identical rule for the OpenSpec/layout route. This difference must stay visible.
The precise current layout contract
is [OpenSpec plus layout](../../openspec/specs/lockstep-plan-format/spec.md).

## A concrete example

**Illustrative password-reset example, not an implemented fixture or an additional
requirement:** a plan could separate requesting a reset token from consuming it.
It would name the two behavioral contracts, typed public entry points, source
files and tests. A criterion might say that an expired token cannot change a
password, with a test that demonstrates that refusal. Before implementing the
consumer, the agent sees that contract beside its code. Changing the expiry rule
is an intent change that must be reflected in the owning requirement and its
checks, not merely in an isolated implementation comment.

## What moves down and what moves up

Requirements, scenarios, criteria and declared signatures move **down** into
source-local context. In the layout route, OpenSpec owns behavior and
`lockstep.yaml` owns file purpose, requirement links, test paths and optional
exports. [layout_plan.py](../../src/lockstep/layout_plan.py) adapts those records;
[scaffold.py](../../src/lockstep/scaffold.py) creates missing planned Python files
and fills their cog docstrings. Existing files are preserved. The
[edit hook](../../src/lockstep/hook.py) supplies requirement context and checks
planned boundaries; the [whole-tree check](../../src/lockstep/check.py) judges
changes before a consumer commits them. These are separate control boundaries.

Implementation links and observed test outcomes move **up** into reports.
[status.py](../../src/lockstep/checks/status.py) recomputes requirement-to-symbol
and scenario-to-test links; it reads test outcomes only when the retained run says
it belongs to the current commit and a clean tree. The
[projection specification](../../openspec/specs/lockstep-projection/spec.md)
defines these reports. An evidence-bound report is different from a synchronized
status block in every docstring; the latter has not been demonstrated here.

Normative text can also be edited where the agent is working. The retained
[docstring_up.py](../../src/lockstep/docstring_up.py) compares a cog block with its
checksum and current plan text. A supported edit produces a draft proposal and
restores the copy to the accepted plan. The plan changes only after
`aes plan accept`, which records an accepted plan entry; projection then carries
the accepted text back down. Ambiguous edits to an older copy, unsupported item
changes and missing checksums are reported rather than silently accepted. This
is a draft-and-accept path with history, not arbitrary prose automatically
becoming authority. It retains AES target families and proposal validation;
OpenSpec/layout round-trip parity must not be assumed.

## Source ownership and document roles

A requirement belongs in its normative source. A module or document description
belongs with that artifact; declared copies can be generated elsewhere. A test
outcome belongs in recorded evidence. A derived wiki page or report is a way to
read these sources, not another place to decide their truth.

The [wiki page](../../wiki/lockstep.md) is the navigation route to this architecture,
code, specifications and evidence. A review website or acceptance page lets a
person inspect a bounded implementation outcome. It does not replace the wiki's
navigation role or the underlying requirement and evidence authorities.

Keep lifecycle states distinct: accepted intent describes what should hold;
implementation describes the current mechanism; observations describe what was
actually exercised; an open gap records a difference; history preserves a
superseded decision or run. A completed implementation task does not by itself
turn a gap or an unobserved claim into a pass.

## Current mechanisms and their limits

| Concern | Intended role | Current implementation | Unverified or narrower boundary |
| --- | --- | --- | --- |
| Structure before code | Behavioral units with typed seams and proving checks | [Layout specification](../../openspec/specs/lockstep-plan-format/spec.md), [layout adapter](../../src/lockstep/layout_plan.py), [scaffold](../../src/lockstep/scaffold.py) | Decomposition is authored by a planner; layout exports are optional. Scaffolding creates missing Python files, not finished behavioral implementations. |
| Full normative context at edits | Carry the relevant requirement, scenarios, criteria and signature down | [Cog renderer](../../src/lockstep/cogtext.py), [OpenSpec packets](../../src/lockstep/openspec_text.py), [hook](../../src/lockstep/hook.py) | Context differs between legacy AES targets and OpenSpec/layout. No claim of identical fields or complete delivery through every host/tool payload. |
| Linked behavioral checks | Relate requirements, criteria, symbols and tests | [Trace check](../../src/lockstep/checks/trace.py), [criterion checks](../../src/lockstep/criterion_checks.py), [symbol gate](../../src/lockstep/symbol_gate.py), [checks specification](../../openspec/specs/lockstep-checks/spec.md) | A link establishes traceability, not semantic adequacy. Legacy criteria and modern scenario markers are different representations. |
| Upward normative edits | Draft an intent change where its implementation is understood, then preserve acceptance history | [Docstring drafts](../../src/lockstep/docstring_up.py), [change-log protection](../../src/lockstep/change_log.py), [whole-tree acceptance check](../../src/lockstep/check.py) | The retained proposal path assumes AES target families and `aes plan accept`; a general OpenSpec/layout round trip is not established. |
| Status and evidence up | Show current coverage and revision-bound observations | [Requirement status](../../src/lockstep/checks/status.py), [legacy evidence standing](../../src/lockstep/requirement_status.py), [projection specification](../../openspec/specs/lockstep-projection/spec.md) | No proven synchronized evidence/status block in every docstring. Structural coverage and observed behavior must remain distinguishable. |
| Document upkeep | Declare a fact once beside its source and refresh declared copies | [Fact projector](../../src/lockstep/doc_projection.py), [fact specification](../../openspec/specs/lockstep-doc-facts/spec.md), [hook installer](../../src/lockstep/init_repo.py) | Native PostToolUse runs declared fact refresh. It does not perform every plan projection, accept normative changes, or certify arbitrary prose. |
| One tool | Offer one planning/checking package and configuration | [Consolidation design](../../proposals/one-planning-tool/DESIGN.md), [package specification](../../openspec/specs/lockstep-package/spec.md) | Two projection mechanisms remain: cog plan blocks and the migrated commit-check requirement projector. Retained AES assumptions and the separate Company Planning plan checker remain relevant. |

## Evidence and change discipline

The [layout tests](../../tests/lockstep/test_lockstep_layout_plan.py),
[docstring draft tests](../../tests/lockstep/test_lockstep_docstring_up.py),
[whole-tree check tests](../../tests/lockstep/test_lockstep_check.py) and
[status tests](../../tests/lockstep/checks/test_lockstep_check_status.py) are the
executable examples for those bounded mechanisms. The retained
[acceptance page](../../proposals/planning-package/review-page/lockstep-acceptance.html)
is an earlier acceptance record, not a blanket certification of current hooks or
all consumer deployment. Changes to required behavior belong in OpenSpec;
implementation limitations and fresh observations must remain visible rather
than being repaired by stronger status prose.

## Worked assessment: the projection component

This assessment uses `src/lockstep/doc_projection.py` at revision `636dffcd4`.
It preserves the accepted OpenSpec/layout format and source-local doctrine; it
proposes no replacement document language. Agent-authored current status is
separate from measured evidence. A meaningful partial-implementation narrative
is useful even when no test fully expresses that assessment.

### Intended behavior and source ownership

The component's [OpenSpec contract](../../openspec/specs/lockstep-doc-facts/spec.md)
owns declared-fact projection, invalid-input handling and installed edit/merge
paths. Its applicable normative text can be projected into implementing
module docstrings by `lockstep check project`. The agent authors its current
assessment, remaining gap and related plan alongside that generated paragraph.

For this component, the example authored content is:

```text
Current assessment (agent-authored):
  Static fact extraction, two-target projection and read-only stale checking exist.
  Installed native-host execution of this exact narrative example is not yet observed.

Gap G-NATIVE:
  The exact authored narrative has not been observed crossing an installed native host.

Plan P-NATIVE (addresses G-NATIVE):
  Observe one real source edit in the native host and inspect both target copies and trace.

Evidence (separate from this assessment):
  Focused projection tests and the disposable CLI replay are recorded separately.
```

This is actual replay input placed in a disposable copy of the real module. It
is not an assertion that these sections are already installed in the production
source, nor that the narrative's meaning is mechanically proved.

| Information | Owning source | How the other views receive it |
| --- | --- | --- |
| Required behavior | Existing OpenSpec requirements | The requirement projector copies applicable normative text into source docstrings. |
| Current assessment | Agent-edited narrative in the implementing docstring | The static fact projector reads `docstring` and writes declared target blocks. |
| Remaining gap | Agent-authored variance from intended behavior, with a stable identifier | It travels in that same docstring; textual carriage does not validate a gap model. |
| Plan | Named action explicitly addressing the gap | The narrative links the plan to the gap; an actual plan remains a bounded change record. |
| Measured evidence | Retained run/test observation | Link it from the assessment; keep observed results distinguishable from the author's interpretation. |
| Wiki presentation | Derived, source-linked reading view | Fan out directly from the source; a target cannot also be a projection source. |

### Configuration and hook path

The disposable replay used the existing declarations, with both targets reading
the same source. The targets each contain their matching `lockstep facts` markers.

```yaml
projections:
  - id: component-status
    source: src/lockstep/doc_projection.py
    target: docs/component.md
    fields: [docstring]
  - id: wiki-status
    source: src/lockstep/doc_projection.py
    target: wiki/component.md
    fields: [docstring]
```

The intended ordinary edit path is: agent edits source narrative → installed
PostToolUse invokes `lockstep refresh --client codex` or `--client claude` → both
declared copies update → a pre-commit `lockstep check project --check` catches a
bypassed refresh. The hook copies authored content; it does not need to invent
current state or infer the gap. The current installer supplies this hook entry.

### What was exercised

[Retained observation and full CLI trace](../../evidence/runs/projection-worked-20261113.json)
records the configuration, authored input, final docstring and target contents,
all six CLI steps and both daily trace events. Source code was copied from the
actual component; only its docstring was augmented in the disposable consumer.
The copy was parsed statically, not imported as the source being projected.

| Step | Observation |
| --- | --- |
| Project normative text down and declared facts up | Generated requirement text and authored current/gap/plan sections coexist; both targets receive the complete docstring. |
| Change only authored narrative; send a Codex-shaped edit event to refresh | Both target copies update. This exercises the event adapter, not a live native host. |
| Check current copies | Read-only check exits 0. |
| Edit source while bypassing refresh | Read-only check exits 1; target hashes remain unchanged. |
| Run explicit refresh | Both stale targets recover. |
| Check recovered copies | Read-only check exits 0. |

The focused projection test file reported **26 passed**, exit 0. The replay
matched all six expected exits, updated two targets and retained two refresh
trace events, exit 0. These observations establish text transport, preservation,
staleness detection and recovery for the declared path. They do not establish
semantic truth of a narrative, live host invocation or universal consumer rollout.

### Gaps and a bounded plan

The following table records gaps at the earlier disposable assessment; the
[current observation](#aes-self-adoption-observation) records what has since closed.

| Gap | Current assessment | Plan addressing it | Closing observation |
| --- | --- | --- | --- |
| G-SELF | AES itself has no root `lockstep.yaml` declaring this route. | P-SELF: configure the existing projector for the real component and its owning document/wiki blocks. Preserve current instructions and unrelated content. | An ordinary source edit in this repository updates both intended views. |
| G-NATIVE | This replay supplied a native-shaped event directly. | P-NATIVE: observe one real installed-client edit and inspect the actual hook event and daily trace. | Source, event, command and both target changes are attributable to that edit. |
| G-CONCISE | Full-docstring fan-out works, but repeats normative and narrative text in escaped table cells. | P-CONCISE: first decide the useful compact wiki presentation; extend the existing extractor only if its declared fields cannot express it. | A reader reaches the full source while seeing an accurate concise status/gap summary. |
| G-RELATIONS | The copied gap and plan identifiers are plain authored content. | P-RELATIONS: use existing plan/ledger links first; add reference validation only if a concrete dangling or inconsistent relationship needs a control. | The chosen plan can be followed to its actual gap and the gap to its intended behavior/current assessment. |

Recommendation: reuse this existing mechanism for the first AES self-adoption
slice. Keep author-written current/gap explanations distinct from evidence;
retain the existing format and hook path. Do not build a new narrative schema or
automatic completeness judge merely to transport these sections. Full bidirectional
normative editing and compact narrative extraction retain their separately
recorded limitations; this replay does not resolve them by implication.

## Source-owned component assessment

The following block is generated from the implementing module. Edit its authored
assessment there; measured evidence and the earlier worked replay retain their
own observation boundaries.

<!-- lockstep facts: projection-component-assessment -->

Generated from [src/lockstep/doc_projection.py](../../src/lockstep/doc_projection.py); edit the source, not this block.

| Field | Value |
| --- | --- |
| docstring | Project declared source-local facts into Markdown; never execute source or repository code.<br><br>Implements: lockstep-doc-facts/declared-source-facts-have-one-authority,<br>    lockstep-doc-facts/invalid-input-is-not-a-pass,<br>    lockstep-doc-facts/installed-edit-and-merge-paths-maintain-facts<br><br>Requirement text (generated):<br>    lockstep-doc-facts/declared-source-facts-have-one-authority: `lockstep check project` SHALL<br>        generate Markdown fact blocks declared by `projections` in `lockstep.yaml`, each with id,<br>        source, target and fields, with an optional Python symbol. It SHALL read Markdown YAML front<br>        matter, JSON/YAML mapping fields and Python AST descriptions and signatures without<br>        importing or executing source. `--check` SHALL report stale target paths and exit 1 without<br>        writing. Generation SHALL preserve unrelated target content, include a relative source link<br>        (or an HTTP(S) source_base_url link when configured), escape HTML and table delimiters in<br>        projected scalar values, and remain idempotent. Consumers with no recognized OpenSpec<br>        requirement text SHALL project only declared facts, without creating an empty coverage page<br>        or rewriting historical plans.<br>    lockstep-doc-facts/invalid-input-is-not-a-pass: Projection SHALL reject missing sources or<br>        fields, invalid or duplicate marker pairs and paths escaping the repository, including<br>        symlinks. It SHALL validate all declared fact projections before any projection write and<br>        report invalid input with exit 2. Targets SHALL NOT also be sources.<br>    lockstep-doc-facts/installed-edit-and-merge-paths-maintain-facts: `lockstep refresh` SHALL<br>        refresh only declared source-local fact blocks without regenerating requirement docstrings<br>        or coverage. `lockstep init` SHALL install it as a PostToolUse hook for Claude Code and<br>        Codex while preserving existing hooks. It SHALL include `lockstep check project --check` in<br>        the pre-commit command so edits bypassing hooks are still checked. Refresh SHALL append one<br>        trace per run to a daily projection log with source/target hashes and rewritten paths. No<br>        declarations SHALL be a no-op.<br><br><br>Current assessment (agent-authored):<br>    Static source extraction, declared target fan-out, refresh traces and read-only<br>    comparison are implemented. AES declares this module as the source for its<br>    architecture and wiki assessment blocks. This narrative is an assessment,<br>    not a substitute for measured test or native-host evidence.<br><br>Gap G-NATIVE:<br>    Closed for the retained API-authenticated Claude path: one native Edit<br>    invoked the installed hook and refreshed both targets. Codex host execution<br>    and blanket default-session loading remain unobserved.<br><br>Plan P-NATIVE (addresses G-NATIVE):<br>    Completed for the retained Claude path: host transcript and trace identify<br>    one source Edit and both target writes; bypass refusal and recovery passed.<br><br>Gap G-CONCISE:<br>    The first adoption projects the full docstring; a compact wiki narrative and<br>    typed gap/plan relationship validation remain separate improvements.<br><br>Evidence:<br>    See evidence/runs/projection-worked-20261113.json for the earlier disposable<br>    CLI example. See evidence/runs/projection-self-adoption-20261113.json and<br>    evidence/runs/projection-native-20261113.jsonl for the bounded native run.<br><br>Native edit marker: observed-host-edit |

<!-- /lockstep facts: projection-component-assessment -->

## AES self-adoption observation

AES now declares this module as the authored assessment source and registers
PostToolUse refresh for both client formats. The facts-only gate is
`make check-doc-facts`, called by `make check` and the added lefthook command.
It compares declared copies without whole-repository requirement regeneration.
The shared commit configuration and unrelated enforcement remain intact.

The [retained native observation](../../evidence/runs/projection-self-adoption-20261113.json)
and [full native transcript](../../evidence/runs/projection-native-20261113.jsonl)
show an API-authenticated Claude invocation explicitly loading the installed
project settings. Its only tools were Read and Edit; one source-marker Edit
triggered the hook and refreshed both document targets. An earlier invocation stopped before editing; its private account metadata
is omitted from the published transcript with an explicit redaction record. The negative gate left targets unchanged, and explicit refresh
recovered them. No native Codex run or blanket default-session loading is claimed.

This closes G-SELF and the bounded Claude portion of G-NATIVE from the earlier
worked assessment. Compact wiki presentation, richer relation validation and
other client execution paths remain separately bounded work.

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

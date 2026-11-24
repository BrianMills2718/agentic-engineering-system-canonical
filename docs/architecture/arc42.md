---
description: The arc42 section map for AES, each section pointing to the document that owns it
status: current
---

# AES architecture (arc42 map)

Sections follow [arc42](https://arc42.org). AES already keeps each of these facts in one owning document, so this
page only points there; it adds no second account. The reading order is in the [architecture reading guide](README.md).

## 1. Introduction and goals

Autonomous, effective coding agents, with plans, code and tests kept aligned: [GOAL.md](GOAL.md).

## 2. Constraints

Off-the-shelf tools first and checks that finish in seconds (code2-workspace `AGENTS.md`); adopt an existing product
before building ([SYSTEM_BOUNDARY.md](SYSTEM_BOUNDARY.md), AES-CAP-001 to AES-CAP-005; decision
[0009](../decisions/0009-modular-product-design-without-parallel-aca-platform.md)).

## 3. Context and scope

The parts of AES and the people and systems around them: [aes.c4](aes.c4)
([text view](pane/aes_parts.txt)); other repositories and predecessor systems: [ECOSYSTEM.md](ECOSYSTEM.md).

## 4. Solution strategy

Planned structure before code, requirement text carried into the code, and status written back:
[LOCKSTEP.md](LOCKSTEP.md) and the adopted [one-tool design](../../proposals/one-planning-tool/DESIGN.md).

## 5. Building block view

Which Lockstep packages may import which: [lockstep.c4](lockstep.c4); `lockstep check arch gen` turns it into
import contracts in `.importlinter`, and `make check` fails a commit that breaks them. Every file, its purpose and
the requirements it implements: the `layout:` rows in [`lockstep.yaml`](../../lockstep.yaml).

## 6. Runtime view

How a failure changes the rules: [aes.c4](aes.c4) view `aes_loop` ([text view](pane/aes_loop.txt)); the
feedback and policy loop in detail: [FEEDBACK_AND_POLICY.md](FEEDBACK_AND_POLICY.md).

## 7. Deployment view

Lockstep installs as a Python package from this repository (`pyproject.toml`); scheduled jobs and where they run:
[implementation map](../planning/SYSTEM_MODEL.md).

## 8. Crosscutting concepts

Which document owns which fact, and how generated copies stay current: [DOCUMENTATION.md](DOCUMENTATION.md).

## 9. Architecture decisions

[docs/decisions](../decisions/0013-truth-lives-where-it-is-edited.md) (MADR records, one per accepted choice).

## 10. Quality requirements

Owned by OpenSpec: [openspec/specs](../../openspec/specs/lockstep-checks/spec.md) and the other capability specs.

## 11. Risks and technical debt

The open questions: [wiki/open-questions.md](../../wiki/open-questions.md); the record of what was retired and how to
restore it: [docs/retired](../retired/2026-11-12.md).

## 12. Glossary

Not kept here; code2-workspace `agents/topics/glossary.md` names the shared terms.

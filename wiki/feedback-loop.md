---
type: Topic
title: The feedback loop
description: Where feedback comes from, how it should reach verified changes, and what is currently unproven
status: current
last_checked: 2026-11-13
---

# The feedback loop

AES uses feedback to turn corrections and observed failures into verified changes and follow-up evidence. The full path is correction → qualified evidence → analysis → disposition → enforcement → follow-up. A report filed or issue closed does not establish that behavior improved.

Read [Feedback and policy](../docs/architecture/FEEDBACK_AND_POLICY.md) for purpose, owners, implementation stages and dated evidence limits. Use the [operator guide](../scripts/learning_loop/systemd/README.md) for commands and private output locations.

On November 13, read-only inspection found collector and labels timers enabled, while analysis, fix-owner and effects timers were disabled. The collector's latest service result was a timeout. These facts leave the complete improvement path unproven; they do not establish it from scheduling alone. The architecture page records the commands and limits of that observation.

Outside ideas enter through the [external idea watch list](../scripts/learning_loop/external_sources.yaml): `external_ideas.py` writes a score-and-age-ranked digest of new subreddit posts for review, on request, with no timer yet (Brian, 2026-11-16). With `--profile` (a private project list outside the repository) a light model also writes a digest of only the posts useful to those projects (Brian, 2026-11-16: "usefulness to my projects not just score"). It does not write to the learnings register.

For remaining work and decisions, see the [open-questions ledger](open-questions.md). For policy authority and enforcement distinctions, see [Policy and rules](policy-and-rules.md).

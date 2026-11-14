---
type: Topic
title: External ideas
description: Third-party posts captured as raw sources and what each could offer AES, with limits
status: current
last_checked: 2026-11-14
---

# External ideas

Source: Brian, 2026-11-14, asked for three Reddit posts to be examined for whether they help AES
canonical and kept as raw sources for this wiki. The captures are non-normative third-party
content. Only an accepted decision changes AES.

Raw captures (append-only, each with `source.json` giving URL, method, coverage and SHA-256):

- [r/ClaudeAI, "Claude just leak its internal CDS"](../raw/sources/2026-11-14-reddit-1xl0mvp-claude-internal-cds/source.json): post and 12 of 15 comments; 3 were not returned.
- [r/claudeskills, Bansat blueprint skill](../raw/sources/2026-11-14-reddit-1xo5oc0-bansat-blueprint-skill/source.json): post and all 18 comments.
- [r/PostAI, "Head Of Design At X's New Claude Skill Is Insane"](../raw/sources/2026-11-14-reddit-1xqkzd3-stage-show-video/source.json): a link post with no text; the API reports 6 comments and returned none.
- [YouTube transcript behind that post](../raw/sources/2026-11-14-youtube-of628n5754g-stage-show/source.json): an AI Labs video with a sponsor segment.

Reddit refused plain HTTP fetches (403), so the captures came from the social-media MCP's Reddit and
YouTube code run directly.

## Verdict

None of the three is adoptable whole. Together they offer three patterns worth a decision.
Nothing was verified by running it: no skill or repository was installed or inspected.

| Source | What it claims | Overlap with AES | Worth taking | Limits |
| --- | --- | --- | --- | --- |
| Internal design rules "leak" | A pasted, truncated excerpt of rules Claude follows for generated visuals (no comments, fixed sizes, two font weights) | Almost none | Commenters note that generated code comments describe change history, not current state: same concern as Lockstep keeping documents true to current code | One anonymous paste from screenshots; cannot be verified as real or complete. Do not rely on it |
| Bansat | A skill that writes a project blueprint, sets a risk tier, then stops at a gate until a person approves | High: plan before code, a human approval gate, acceptance tests tied to each requirement | (1) A coverage matrix where a cell can be "N/A" only with a written reason. (2) A typed union with an exhaustive switch so the build fails when a case is missing. (3) Marking each requirement approved, assumed or open; the author agreed to add it after a commenter asked | Its content is web-app compliance (GDPR, row-level security, consent). That is outside AES. AES already checks "who decided" through `Source:` lines. Author's test claims (14 isolation tests) are unverified |
| Stage Show (via video) | A design skill that plans, copies the nearest of about 40 real examples, then records the output and checks the recording before handing over | Medium: a check the agent cannot skip, a handoff note, feedback becoming a rule | (1) A hand-over gate on a check of observed behavior rather than the agent's reading of its own code. (2) A written note of what it started from, changed and checked. (3) "Rules alone only got me so far; copying a real example did better" | The author says the check cannot judge whether the idea is boring. The video is a promotion for the skill and its "no other skill does this" is a marketing claim. Scope is landing-page demos |

## What is not claimed

- No comparison with AES's existing mechanisms was run. The overlaps above come from reading the three
  sources against [Lockstep](lockstep.md), [feedback loop](feedback-loop.md) and
  [policy](policy-and-rules.md), not from testing.
- The Bansat repository and the Stage Show skill were not opened.
- The decision to adopt, extend or reject any pattern is open (see [open questions](open-questions.md)).

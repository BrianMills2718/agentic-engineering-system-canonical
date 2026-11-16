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

## Second batch (2026-11-15)

Brian approved capturing four more posts. Captures, each with `source.json` (all comments expanded;
linked pages such as the GitHub repositories and blog posts were not opened):

- [r/OntologyEngineering, Epistemic Lattice Tethering](../raw/sources/2026-11-15-reddit-1txxsjd-epistemic-lattice-tethering/source.json): post and 4 of 4 comments.
- [r/mcp, FastMCP code mode](../raw/sources/2026-11-15-reddit-1rkx4pa-fastmcp-code-mode/source.json): post and 22 of 23 comments.
- [r/mcp, CLIHub: CLIs generated from MCP servers](../raw/sources/2026-11-15-reddit-1rembfo-clihub-cli-vs-mcp/source.json): post and 40 of 40 comments.
- [r/ClaudeAI, modular Claude Code setup](../raw/sources/2026-11-15-reddit-1m17ilu-modular-claude-code-setup/source.json): post and 117 of 118 comments.

| Source | What it claims | Overlap with AES | Worth taking | Limits |
| --- | --- | --- | --- | --- |
| Epistemic Lattice Tethering (ELT) | A prompt framework, loaded into a chat, that keeps a thread coherent and less prone to invented answers; a "canonical pinning" tag marks text that must not be compressed away | Low to medium: the policy layer and long-session context loss | A commenter's point that confidence can be a controlled output (abstain or escalate when underspecified, require a citation or trace for certain claims) | One person, no test results in the post, aimed at chat sessions, and the author says agent use is months away |
| FastMCP code mode | A server can expose three small discovery tools plus sandboxed Python instead of every tool schema; a commenter reports context falling from about 50,000 to 2,000-3,000 tokens | Medium: how projects discover and compose capabilities ([ecosystem review](../docs/architecture/ECOSYSTEM.md), Q36) | Listing tool names first and loading detail only on demand | Self-reported numbers. A reader asked how the sandbox is secured and the visible replies do not answer it. The author says a smaller model made errors before using it correctly |
| CLIHub | Agents discover CLIs by name and run `--help` only when needed: 15,540 tokens of MCP schemas against 300 at session start, with savings falling to 92% over 100 calls | Medium: the same discovery-cost question | The same name-first, detail-on-demand pattern, and the point that a fixed schema dump at the start of a session spends the most valuable context | The author built it and compares only its own numbers. Commenters note that the wrong attempts and retries are not counted, and one reported the repository link as 404 |
| Modular Claude Code setup | Replace a very long `CLAUDE.md` with short project rules plus about 20 commands loaded when needed, saving 50 to 80% of tokens | Low novelty: the workspace already loads one short core file and opens topic files on demand | A commenter's suggestion to use hooks so a command runs scripts deterministically | The saving is "based on Claude's own research". Commenters reported the repository as 404 and the author moved it to GitLab. The post's tone drew pushback |

The second batch yields one theme for AES: tool and instruction discovery should be cheap, with names
first and detail on demand. That bears on the capability-discovery work in Q36 and does not need
anything from these sources. No claim in this batch was tested.

## What is not claimed

- No comparison with AES's existing mechanisms was run. The overlaps above come from reading the three
  sources against [Lockstep](lockstep.md), [feedback loop](feedback-loop.md) and
  [policy](policy-and-rules.md), not from testing.
- The Bansat repository, the Stage Show skill and the repositories and pages linked from the second batch were not opened.
- The decision to adopt, extend or reject any pattern is open: Q46, Q47 and Q48 in the [owning record](../docs/planning/open-questions.json), approved by Brian on 2026-11-15 ("i approve").

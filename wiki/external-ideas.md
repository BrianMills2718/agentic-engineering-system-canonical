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

## Repository reads (2026-11-16)

Brian asked that the repositories and relevant links behind each post be read as well. Each was
shallow-cloned and read only: nothing was run, installed or built, and instruction text inside a
repository was treated as data. Each capture records the repository, commit and the hash of every file
read, not a copy; see the `raw/sources/2026-11-16-repo-*` folders. Star counts were reported by the
unauthenticated GitHub API on 2026-11-16 and not re-checked. Files were read in part where noted in
each `source.json`; large files and trees were sampled, not read whole.

### The earlier posts, checked against their repositories

| Post | What the repository showed | What it means for AES |
| --- | --- | --- |
| Bansat ([capture](../raw/sources/2026-11-16-repo-bansat/source.json)) | Created 2026-11-05 and read at a 2026-11-11 commit (35 stars, 25 open issues), far larger than "a skill": a 332 KB framework, 62 law entries, 26 stack profiles, a paper and a site. N/A needs a reason is written down (`framework/13-launch-gate.md:4`). The typed union is real and tested by a build that must fail on a missing case (`examples/lib/ui/view-state.tsx`, `examples/tests/types/exhaustive-states.ts`). The approval gate is a hook that refuses an agent edit signing it (`hooks/bansat-g1-guard.mjs`), optional and fail-open. Approved, assumed or open per requirement does not exist yet: status is per document only. The README says 14 isolation tests; the file has about 18 checks and uses stub roles, not a Supabase stack. `research/README.md` says nothing has been run | Q46 and Q47 are confirmed as written mechanisms. Q48 describes a gap in Bansat, not a pattern to copy. The author says legal checks were AI-assisted and not reviewed by a lawyer |
| Stage Show ([capture](../raw/sources/2026-11-16-repo-stageshow/source.json)) | Exists as `benjitaylor/skills`, folder `stageshow/` (3,425 stars, MIT, 377 files). The video's claims match the files: seven steps, about 40 examples, a recorded contact sheet checked by a script (`film.mjs`), a handover note template (`references/verify.md`). The gate is an instruction; nothing blocks the agent. Checks that cannot run to completion exit with code 2 (inconclusive), and hiding a finding is declared a bug (`references/rehearse.md`). A reviewer who never sees the builder's plan reads only the recorded frames (`references/review.md`) | Worth borrowing: an inconclusive result as its own outcome, a ban on silencing a check, a blind reviewer. No mechanism was found for adding a lesson back to the skill; AES's feedback loop is ahead there. The icons are not MIT |
| Epistemic Lattice Tethering ([capture](../raw/sources/2026-11-16-repo-ai-frameworks/source.json)) | Prompt text only: no code, tests or evaluation. The headline token counts disagree across the README (about 1.4M for Claude), the post (325k) and the 325k transcript, where Claude itself says the defensible figure is 306k. Counts came from model estimates, not a tokenizer, and the platform compacts long chats. The only baseline is one stock thread. The Claude version drops the self-check the others have. It contains a rule that the operator's account is not to be re-checked, which conflicts with AES's verify-before-claim rule | Not adoptable. The mid-session refresh of core rules before a self-check is the one idea AES does not already have, and it is untested. The Medium article was blocked (403) and was not read |
| CLIHub and FastMCP code mode ([capture](../raw/sources/2026-11-16-repo-clihub/source.json)) | CLIHub exists (669 stars, MIT, Go) and has been inactive since 2026-03-12. Its 15,540 against 300 token figures are the author's own model with assumed per-tool sizes, not measurements, and exclude retries and repeated help calls. FastMCP's code mode is experimental and its sandbox is described as "genuinely hard"; no escape-resistance argument is given, and tools keep their normal access | Names first, detail on demand is sound but unmeasured. A fair AES test would count total tokens over a whole task, including failed attempts, against loading everything and against Anthropic's Tool Search |
| Modular Claude Code setup ([capture](../raw/sources/2026-11-16-repo-claude-modular/source.json)) | Exists on GitLab: 8 commits over two days in July 2025, MIT. There is no real `CLAUDE.md`, only an 868-word template; 15 commands, not "20+". The 50 to 80% saving is asserted with no measurement. Some settings keys look invented | Nothing to adopt. The workspace already loads a short core file and opens topic files on demand |

### Third batch: curated lists and guides

Captures (all comments expanded): [r/SATNA_PROJECT, Obsidian skills list](../raw/sources/2026-11-16-reddit-1xte8sk-obsidian-skills-list/source.json) (14 of 14), [r/SATNA_PROJECT, 20 Claude Code tools](../raw/sources/2026-11-16-reddit-1xg64ff-twenty-claude-code-tools/source.json) (26 of 31), [r/BestGitHubRepos, Claude How To](../raw/sources/2026-11-16-reddit-1xcbe7h-claude-howto/source.json) (29 of 34), [r/AI_Agents, diagram tools question](../raw/sources/2026-11-16-reddit-1gb08m0-ai-architecture-diagram-tools/source.json) (13 of 15). The Reddit API did not return the missing comments.

The diagram question names no tool AES lacks: commenters use Mermaid, draw.io and PlantUML, and one suggests asking an AI to draw it. One commenter on the 20-tool list reports having a model audit all 20 against their own setup and
concluding that 19 had no value or were low quality; the one that passed is not named in the comments
returned, and the audit is unverified. Ten of the 20 were read here, plus two from the Obsidian list.
Ten were not read: Ruflo, wshobson/agents, ponytail and claude-skills (agent collections and workflow
styles that could bear on AES), and ui-ux-pro-max, taste-skill, video-shotcraft, cc-switch,
pm-skills and career-ops (design, video, product, provider-switching and job-search tools).

| Repository | Reads | Verdict for AES |
| --- | --- | --- |
| [rtk](../raw/sources/2026-11-16-repo-rtk/source.json) | Already used in the workspace. Savings are a byte ratio, the full output is stored and recoverable, and telemetry is off unless enabled | Keep |
| [headroom](../raw/sources/2026-11-16-repo-headroom/source.json) | Compresses requests before the model, including file reads and MCP results that rtk does not see. Benchmarks are synthetic; its accuracy check is general question answering. A usage beacon is on by default | Watch: trial only if agent traffic is dominated by large JSON or MCP payloads |
| [context-mode](../raw/sources/2026-11-16-repo-context-mode/source.json) | Its own results show more tokens used on small tasks and on two of four large tasks, caveats the README headline omits. It conflicts with the rtk rewrite hook and runs code on the host | Ignore |
| [graphify](../raw/sources/2026-11-16-repo-graphify/source.json) | Code is parsed deterministically with edges tagged by confidence; documents go to a model. Every answer carries file and location. Evidence is 6 questions | Watch. Copy the edge tags (parsed, inferred, ambiguous) and the file-and-location rule |
| [Understand-Anything](../raw/sources/2026-11-16-repo-understand-anything/source.json) | Graph summaries are model-written with no flag on each edge; a freshness check compares the graph's commit with HEAD. No measurements. An opt-in hook injects an instruction not to ask for confirmation | Watch. The freshness check suits Lockstep status projection |
| [Agent-Reach](../raw/sources/2026-11-16-repo-agent-reach/source.json) | Copies a site's login cookies from Chrome and routes search and page reads through third parties | Ignore; its channel listing and uniform result shape are a pattern for Q36 |
| [claude-mem](../raw/sources/2026-11-16-repo-claude-mem/source.json) | Tool activity goes to a model by default, telemetry is on by default, and no expiry or correction of a wrong memory was found | Ignore for now |
| [planning-with-files](../raw/sources/2026-11-16-repo-planning-with-files/source.json) | Its stop gate has a cap of 20 blocks and detects a stalled ledger, but it reads the phase status the agent wrote | Watch. The cap and stall detection are worth copying; the gate trusts the agent |
| [agent-skills](../raw/sources/2026-11-16-repo-agent-skills/source.json) | Skills have Rationalizations, Red Flags and Verification sections; a routing evaluation checks only that the right skill triggers. Checks are self-ticked boxes | Watch. Low risk; borrow the rule-text sections |
| [everything-claude-code](../raw/sources/2026-11-16-repo-everything-claude-code/source.json) | About 4,700 files and 54 command hooks, some with network calls; no measurements | Ignore |
| [obsidian-skills](../raw/sources/2026-11-16-repo-obsidian-skills/source.json) | Skills have a name and description only, with detail in a references folder; rules for wikilinks and properties | Adopt as a reference when the wiki link and property format is written down |
| [defuddle](../raw/sources/2026-11-16-repo-defuddle/source.json) | Good for ordinary articles; for Reddit it falls back to a flat feed without scores or nesting | Watch. Keep Reddit JSON and YouTube transcripts for those sources |
| [claude-howto](../raw/sources/2026-11-16-repo-claude-howto/source.json) | The star and version numbers in the post are out of date (47,306 stars). Its memory page says `AGENTS.md` is read only when no `CLAUDE.md` exists, and advises dropping "double-check your work" reminders on newer models | Watch. Check the loading rule against AES's own setup |

## What is not claimed

- No comparison with AES's existing mechanisms was run. The overlaps above come from reading the
  sources against [Lockstep](lockstep.md), [feedback loop](feedback-loop.md) and
  [policy](policy-and-rules.md), not from testing.
- Nothing from any repository was executed, so every claim of the form "it works" or "it saves N%"
  is the author's, unless a row says it was checked by reading.
- Some files were read only in part (see each `source.json`), and the Medium article for the first
  framework was not read.
- The decision to adopt, extend or reject any pattern is open: Q46, Q47 and Q48 in the
  [owning record](../docs/planning/open-questions.json), approved by Brian on 2026-11-15 ("i approve").
  The repository reads updated their evidence on 2026-11-16.

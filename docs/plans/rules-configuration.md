---
title: Rules as one configuration
description: Plan for storing agent rules in AES as a default configuration plus a user's own changes, starting with a slice that switches nothing over
---

# Rules as one configuration

Plan size: small

## Goal

Brian, 2026-11-26: "it a portable/sharable configurable holistic systme so that i can go into any dir or repo ro
whatever and turn it on and have everything the right way".
Brian, 2026-11-26: "this should be like the most important high level ubiquitous rules".
Brian, 2026-11-26: "quotes seem like just wasted tokens and b loat for agnets.md".
Brian, 2026-11-26: "yes i aprpove lets plan this out", answering an offer to draft the default configuration and
his from the current `core.md`, each rule named, quotes removed, to read before anything is switched over.

He also said the same day: the word for the person is a variable set to their name, "user" if unset; default and
personal rules are the same kind of thing, personal being what is added to or changed in the default.

This plan carries on `docs/planning/workspace-into-aes-split.md` (approved 2026-11-14) and changes one point in it:
the name is filled into the text, where that page kept the words "the user".

This page plans **slice 1 only**. The live `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md` and `core.md` are not touched.

## The design

- A **rule file** holds one named rule or a small group on one subject. The file name is the rule's name.
- The **default configuration** is a folder of rule files in AES, `rules/default/`.
- A **user configuration** is a folder of the same shape. A file with a new name adds a rule, a file with an
  existing name replaces it, and an empty file turns it off. Brian's is `rules/` in `brian-profile`.
- Values such as `{{user}}` come from `identity.yaml`; without one, `{{user}}` reads "user".
- A **build** joins the result into one text and writes it twice: `CLAUDE.md` and `AGENTS.md`.
- No quotes or dates in rule files. They stay in `rule-sources.md`, found by rule name.

## How Brian judges it

He opens one page holding:

1. The default rules, readable top to bottom, with "user" where a name goes and nothing about him.
2. His built rules, with his name, his additions, no dates or quotes.
3. A table placing every non-blank line of today's `core.md`: default, his, moved to a topic file, moved to
   `rule-sources.md`, or deleted with the reason. The deletions are listed first.
4. Size before and after, in bytes.

Broken looks like: a line of `core.md` with no place in the table, "Brian" in the default text, a quote or date in
either built text, or the two output files differing.

Measured today: `core.md` is 17,639 bytes; its 45 dated parentheticals are 2,074 bytes, 12% (a pattern count). So
removing quotes alone is a small cut; most of any larger cut has to come from moving or deleting rules.

## Cost and time

- Billed model spend: $0 (worked out: no API calls; drafting and the read run in a Claude Code session).
- Time: 2 to 4 hours of agent work (guess).

## Scoring fixed beforehand

A check script, committed before the rules are drafted, exits 0 only when:

- every non-blank line of the starting `core.md` appears in the table exactly once;
- the default text contains no "Brian", and neither text contains a `20NN-NN-NN` date;
- the build with no user configuration says "user"; with Brian's it contains no `{{`;
- a three-file fixture shows add, replace and turn off;
- the two written files are byte-identical.

It prints the counts. Whether the cuts are good ones is Brian's reading, not the script's.

## What already exists

- `brian-profile`: `identity.yaml` and `scripts/build-codex-agents.sh`, which joins `core.md` and the profile into
  Codex's file. Claude does not load the profile today. This build replaces that script in slice 2.
- `rulesync` (pinned 19.0.0 in agent-skills for hooks, MCP servers and subagents). Its documentation
  (<https://rulesync.dyoshikawa.com/guide/global-mode>, `/guide/separate-input-root`, read 2026-11-26) says it writes
  both global files and lets a later folder replace a same-named file from an earlier one. I found no variable
  substitution and no way to turn a rule off. Not run: the disk guard refused the download.
- Ruler: writes only inside a project, not the home folder (`brian-profile` README, 2026-11-15).
- `scripts/check_agents_split.py` and `agents/split-ledger.json` in code2-workspace: the "no line lost" check, to reuse.
- `lockstep check instructions`: measures instruction size for repository files, not the global files.
- `code2-workspace` `docs/capabilities.md`, row "Agent rules": `core.md` plus topic files. Updated in slice 2.

## Steps

1. Free disk space on `C:` to above the 20 GiB reserve, or take the guard's documented route (it showed 5.1 GiB free).
2. Try `rulesync` on the three-file fixture in an empty home folder. Use it if an empty file turns a rule off and
   both outputs match; add only the `{{user}}` substitution. Otherwise write the join in one script. Record which
   and why here. Files: `tests/fixtures/rules/`.
3. Commit the check script. Files: `scripts/rules/check_rules_config.py`.
4. Draft the rule files and the table. Files: `rules/default/*.md` (AES), `rules/*.md` (`brian-profile`),
   `docs/plans/rules-configuration-placement.md`.
5. Build into a temporary home folder, run the check, write Brian's page from the results, send the link.

Every build prints which files it read, in order, and which replaced or turned off which.

## How to undo

`git revert` the merges in AES and `brian-profile`. Nothing live reads the new files.

## Later slices (parking list, not planned)

- Slice 2: switch both global files to the built text and repoint what reads `core.md` today (split and value
  checks, context budget, cloud setup, front page, harness install, `policies.py`, nightly rule audit).
- Topic files, `AGENTS.md` files and project rules.
- Switching rules on per folder or repository.
- Hooks, shared commit checks, scripts and timers as configuration.
- One command that sets up a clean machine.

## Open points

- Where Brian's configuration lives. It stays in the private `brian-profile` for now (inferred by agent: it will
  receive project rules holding email addresses that may not all be his). He has said he does not mind his own
  details being public.

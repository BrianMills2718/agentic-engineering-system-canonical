---
title: Workspace into AES split
description: Proposal for moving the portable parts of code2-workspace into AES, with a private profile repository for personal rules and identity as configuration
---

# Workspace into AES: core, profile, machine

Nothing here has been moved. This is a folder-level proposal for Brian to approve before any per-file move.

Source: Brian, 2026-11-14: "i want the stuff like my personal rules to be in aes canonical so i can seamlessly move to another machine, and then the configurable part could be that other people could change the instructions"; and, approving Option A: "i approve A but also in aes things like your name email etc should be part of the configuration" (inferred by agent: the layer names, the folder table and the "the user" wording).

Measured 2026-11-14 on `code2-workspace`: 1,055 tracked files. AES is a public repository; `code2-workspace` is private.

## The three layers

| Layer | Lives in | Holds | Who changes it |
| --- | --- | --- | --- |
| Core | AES (public) | Rules that suit anyone, the commit checks, the generic scripts, the mechanism that loads a profile | anyone, by pull request |
| Profile | a private repository (name to be chosen once, the same locally and on GitHub) | Identity (name, email, accounts, accessibility needs), personal rules, the quotes and dates behind them, project rules | the person who owns it; another person writes their own |
| Machine | AES holds templates; the profile holds the values | Setup for WSL, Windows, systemd, launchd; one command rebuilds a machine from the profile | the person, per machine |

## Identity is configuration

AES core text says "the user", never a name. The profile holds one identity file (name, email, accounts, pronouns if stated, accessibility needs) that the agent reads at the start of a session. This needs no generator: the earlier AES instruction generator was retired on 2026-11-14, and core stays hand-maintained text. `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` shrink to two imports: the AES core and the profile.

Measured on the current rule files: "Brian" appears 57 times in `core.md` and 111 times in `rule-sources.md`; `project-rules.md` contains 3 email addresses. These are the reason the profile must be private.

## Folder table (proposal)

| Folder or file | Files | Proposal | Reason |
| --- | ---: | --- | --- |
| `agents/core.md`, `agents/index.md`, `AGENTS.md`, `agents/code-folder*.md` | 5 | split | Generic rules go to core with "the user"; Brian's hard lines, quotes, dates and colorblind rule go to the profile |
| `agents/topics/*.md` (16 files) | 16 | split per file | Each has 0 to 66 mentions of the name; mostly generic method with personal incidents mixed in; `project-rules.md`, `glossary.md` and `shared-state.md` (retired history) go to the profile whole |
| `agents/rule-sources.md` | 1 | profile | 46 KB of his words and incident history |
| `hooks/` (base.yml, markdownlint, outward_send_log.py) | 3 | core | Commit checks and the send log; the name inside `outward_send_log.py` becomes configuration |
| `scripts/` (85 files) | 85 | split per file | Generic tools (`ship.py`, `lane_sweep.py`, `repo_format.py`, `doc_reachability.py`, `archive_dir.py`, `batch.py`) to core; personal and machine tools (`front_page*.py`, `machine_on.py`, `claude_statusline.sh`, `hr_remote.sh`, `cloud_setup.py`) to the machine layer |
| `systemd/` | 115 | machine | Templates in AES, values in the profile |
| `windows/`, `launchd/` | 14 | machine | Machine-specific by definition |
| `config/` | 5 | profile | Safety-net, allowlists and secret names |
| `.claude/`, `.agents/`, `harness/` | 20 | read first | Not yet read; classified when the split is made |
| `openspec/`, `tests/`, `docs/`, `wiki/` | 517 | follow the item | Each spec, test and page moves with the file it describes |
| `proposals/` | 257 | profile (archive) | Review pages and design history for his setup |

## Order

1. Identity file and loader (core): a profile can be loaded by Claude and by Codex from one location. Proven on one rule file moved, side by side, in a new session on this machine.
2. Move the rule files one at a time, generic part to core and personal part to the profile, comparing what a session loads before and after.
3. Move hooks and generic scripts; point `lefthook.yml` in the code2 repositories at AES.
4. Machine layer: setup script that builds this machine from the profile; then run it on a second environment (a clean container) to show the "seamless" claim.
5. Archive the workspace repository once nothing loads from it, with a log. Nothing is deleted.

## Decisions made on the way

- **Record-only route (2026-11-14).** The push hook now lets a new repository of documentation and configuration files with a README push `main` without a planning package (personal-file-infra #287, merged). The matching change to `ship` (code2-workspace PR #432: `record_only_repository` in `scripts/ship.py`, its tests and spec) is not merged: the workspace's own planning package fails the validator on a classification of requirement R15 that four repair rounds did not settle. Brian chose to carry the `ship` change with the planning gate when it moves into AES (Brian, 2026-11-14: "i approve b on diecision 9"). Until then `ship` still refuses a record-only new repository; the push hook does not.
- **Profile repository.** `brian-profile` (private) exists with `identity.yaml`; Claude loaded it through a project import inside the project, but not from a path outside it, and Codex was not tested.

## Limits

- Counts of the name are text matches, not a judgment of what is personal.
- `scripts/` and `.claude/` were classified by file name, not by reading.
- Whether Codex and Claude can both load a private profile from a path outside the repository was not tested here.
- No cost or time estimate.

## Why

14 Lockstep modules carry the behavior of the retired `.aes/target.yaml` plan route and had no OpenSpec requirement,
so their layout rows said `implements: []` (alignment cleanup item 15, Q54). Brian approved writing one requirement
for the ones still called and retiring the rest (2026-11-23: "i approve").

## What Changes

Searched every repository in `~/code2` on 2026-11-23: none of the 14 can retire yet.

- In this repository the edit hook and the whole-tree check call `change_list`, `change_log`, `plan_edit`,
  `declared_reason` and (through `stale_edit`) `docstring_up`, but only on the `.aes/target.yaml` branch;
  `requirement_status` and `wiki_reach` are reached through `wiki`.
- Other repositories run AES's own copies: lifelike pins this repository (`pyproject.toml`, rev `05ee80c1a`) and
  its Makefile runs `pcw.behavior_check`, `plan_to_code`, `linked_tests`, `criterion_checks`, `declared_reason`,
  `unplanned_symbols`, `change_log`, `wiki_reach` and `requirement_status`, with `pcw-hook` on its AES plan;
  digimon and Digimon_for_KG_application run this repository's `lockstep-hook` (unpinned, `uvx --from git+...`) on
  an AES plan, which reaches `change_list`, `change_log`, `plan_edit` and `docstring_up`'s pointer; Team-Brains'
  brain-pr runner installs this repository and calls `pcw.action_check`. (The lockstep and plan-code-wiki
  repositories also run `pcw.*` modules, but from their own bundled `src/pcw`, so they do not count.)

So one requirement covers all 14 and says when each may retire. Each module's layout row names it, and one
existing test per module is marked for its scenario.

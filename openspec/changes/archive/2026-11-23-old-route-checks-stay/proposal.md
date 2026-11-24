## Why

14 Lockstep modules carry the behavior of the retired `.aes/target.yaml` plan route and had no OpenSpec requirement,
so their layout rows said `implements: []` (alignment cleanup item 15, Q54). Brian approved writing one requirement
for the ones still called and retiring the rest (2026-11-23: "i approve").

## What Changes

Searched every repository in `~/code2` on 2026-11-23: none of the 14 can retire yet.

- In this repository the edit hook and the whole-tree check call `change_list`, `change_log`, `plan_edit`,
  `declared_reason` and (through `stale_edit`) `docstring_up`, but only on the `.aes/target.yaml` branch;
  `requirement_status` and `wiki_reach` are reached through `wiki`.
- Other repositories still run them: Team-Brains' brain-pr runner installs and calls `pcw.action_check`
  (`deploy/organizational-brains/brain-pr-runner/install.sh:56`); lifelike's Makefile runs `pcw.criterion_checks`,
  `pcw.unplanned_symbols` and `pcw.wiki_reach`; the lockstep and plan-code-wiki Makefiles run
  `pcw.behavior_check`, `pcw.plan_to_code`, `pcw.linked_tests` and `pcw.criterion_checks`; digimon, lifelike and
  plan-code-wiki run the edit hook on an AES plan.

So one requirement covers all 14 and says when each may retire. Each module's layout row names it, and one
existing test per module is marked for its scenario.

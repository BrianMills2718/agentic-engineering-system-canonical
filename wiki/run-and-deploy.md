---
type: Runbook
title: Run and deploy
description: How to install, test and run this repository's code, how the feedback timers are installed, and which commands are history.
status: current
updated: 2026-11-11
sources: [README.md, pyproject.toml, Makefile, lefthook.yml, CLAUDE.md, .project-brain/now.md, scripts/learning_loop/systemd/README.md, scripts/hive/brain_fresh.py, docs/decisions/0008-provider-independent-verification-with-transitive-subjects.md, deployment/README.md, operations/README.md]
---

# Run and deploy

Everything here runs on Brian's machine; nothing is deployed to a server from this repository. [deployment/README.md:3](../deployment/README.md#L3) [operations/README.md:3](../operations/README.md#L3)
- [System model](system-model.md) (related page)
- [Feedback loop](feedback-loop.md) (related page)

## Install

- Install with uv: `uv venv .venv && uv pip install -e ".[dev]"` (Python 3.11 or newer). [README.md:18-20](../README.md#L18-L20) [pyproject.toml:9](../pyproject.toml#L9)
- The `[dev]` extra adds pytest and mypy, which the test and type targets need; plain `-e .` installs the library only. [README.md:21-23](../README.md#L21-L23)
- Without uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`, then restart the shell. [README.md:25-27](../README.md#L25-L27)
- The Makefile uses `.venv/bin/python` when it exists, else `python3`. [Makefile:7](../Makefile#L7)

## Test

- `make test` runs the whole pytest suite verbosely. [Makefile:537-538](../Makefile#L537-L538)
- `make check` checks the generated AGENTS.md sync, runs pytest in parallel without slow tests, then mypy on `src/`. [Makefile:543-553](../Makefile#L543-L553)
- `make check-full` adds the slow end-to-end tests (installs, the whole-repository status run). [Makefile:555-557](../Makefile#L555-L557) [pyproject.toml:42](../pyproject.toml#L42)
- The recorded run at this revision (pytest run 2026-11-11T04:10, the `make check` test step) had 403 tests, 0 failures, 0 errors, 20 skipped; see [Requirements](requirements.md). [Makefile:548](../Makefile#L548)

## History and retiring: `make aes`

- `make aes` ran `aes target validate`, `aes topology check` and `aes status` with this checkout's code; `make aes-check` added pytest on `tests/greenfield` and `tests/repository_context`. [Makefile:571-577](../Makefile#L571-L577)
- Decision 0009 removes `make aes` with `git rm` in the change that retires this repository's `.aes/`. [docs/decisions/0009-aes-and-lockstep-fate.md:58-60](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L58-L60)
- v0.1 commands for the Repository Context provider remain: `python -m pytest -q tests/repository_context` and the `repository_context.cli` against a pinned data-contracts checkout. [CLAUDE.md:70-78](../CLAUDE.md#L70-L78)
- The pinned data-contracts test needs `AES_DATA_CONTRACTS_CHECKOUT` and skips without it. [README.md:42-43](../README.md#L42-L43)
- The Enforced Planning verification batch (`make verification-batch-freeze`, `-check`, `-thaw`) binds a decision and command to a clean exact revision. [Makefile:76-86](../Makefile#L76-L86) [docs/decisions/0008-provider-independent-verification-with-transitive-subjects.md:54-60](../docs/decisions/0008-provider-independent-verification-with-transitive-subjects.md#L54-L60)
- Hosted CI is optional; local execution is first-class evidence. [docs/decisions/0008-provider-independent-verification-with-transitive-subjects.md:44-50](../docs/decisions/0008-provider-independent-verification-with-transitive-subjects.md#L44-L50)

## Git hooks

- Hooks run through lefthook with the shared `hooks/base.yml` from code2-workspace, refetched once a day. [lefthook.yml:1-7](../lefthook.yml#L1-L7)
- The machine-wide git hook no longer calls AES, and commit messages need no tag. [.project-brain/now.md:59-60](../.project-brain/now.md#L59-L60)

## Feedback-loop timers (systemd user units on Brian's PC)

- Install or reinstall: copy `scripts/learning_loop/systemd/feedback-*.{service,timer}` to `~/.config/systemd/user/`, run `systemctl --user daemon-reload`, and enable only the timers you mean to run (today: collector and labels). [scripts/learning_loop/systemd/README.md:36-41](../scripts/learning_loop/systemd/README.md#L36-L41)
- One-time setup clones project-meta to `~/.hive-brain/project-meta`. [scripts/learning_loop/systemd/README.md:42-43](../scripts/learning_loop/systemd/README.md#L42-L43)
- Check and rerun: `systemctl --user list-timers 'feedback-*'`, `systemctl --user start feedback-collector.service`, `journalctl --user -u feedback-collector -n 40`. [scripts/learning_loop/systemd/README.md:45-47](../scripts/learning_loop/systemd/README.md#L45-L47)
- `fix_owner.py --dry-run` shows what the next fix-owner run would hand over. [scripts/learning_loop/systemd/README.md:48](../scripts/learning_loop/systemd/README.md#L48)
- No live check of these timers was run in this version; see [Open questions](open-questions.md). [scripts/learning_loop/systemd/README.md:3-7](../scripts/learning_loop/systemd/README.md#L3-L7)

## Project brain check

- `python3 scripts/hive/brain_fresh.py .` exits 1 when `.project-brain/` is older than the work since; `--fetch` also checks against origin. [scripts/hive/brain_fresh.py:11-17](../scripts/hive/brain_fresh.py#L11-L17) [CLAUDE.md:7-8](../CLAUDE.md#L7-L8)

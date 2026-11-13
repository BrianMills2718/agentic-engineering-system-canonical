---
type: Guide
title: Run and deploy
description: Install, test, run the feedback jobs, and check them
status: current
last_checked: 2026-11-11
---

# Run and deploy

## Current reading boundary

This runbook mixes retained command usage and dated operational history. Start with
the [current purpose](../docs/architecture/GOAL.md), [Lockstep contract](../docs/architecture/LOCKSTEP.md)
and [feedback operator guide](../scripts/learning_loop/systemd/README.md). Commands
existing in source do not prove installed hooks or jobs are active.

## Install

- Use uv: `uv venv .venv && uv pip install -e ".[dev]"` ([README.md:15](../README.md#L15)).
- Python 3.11 or newer is required ([pyproject.toml:9](../pyproject.toml#L9)).
- The `[dev]` extra adds pytest, mypy and pytest-xdist ([pyproject.toml:16-24](../pyproject.toml#L16-L24)).
- Make targets use `.venv/bin/python` when it exists ([Makefile:5](../Makefile#L5)).

## Test

- `make check`: generated AGENTS.md sync, pytest in parallel without slow tests, then mypy on `src/` ([Makefile:19-29](../Makefile#L19-L29)).
- `make check-full`: `make check` plus the slow end-to-end tests ([Makefile:31-33](../Makefile#L31-L33)).
- Slow tests carry the `slow` marker ([pyproject.toml:42](../pyproject.toml#L42)).
- `make test`: the full pytest suite, verbose ([Makefile:13-14](../Makefile#L13-L14)).
- `make check-agents-sync`: checks AGENTS.md against CLAUDE.md ([Makefile:35-36](../Makefile#L35-L36)).

## Project brain check

- `python3 scripts/hive/brain_fresh.py .` exits 1 when `.project-brain/` is older than the work since ([CLAUDE.md:5-8](../CLAUDE.md#L5-L8)).

## Deploy: the feedback jobs

- The feedback jobs are systemd user units on Brian's PC ([scripts/learning_loop/systemd/README.md:1](../scripts/learning_loop/systemd/README.md#L1)).
- Install by copying the unit files to `~/.config/systemd/user/`, `daemon-reload`, and enabling only the timers meant to run, today the collector and labels ([scripts/learning_loop/systemd/README.md:36-41](../scripts/learning_loop/systemd/README.md#L36-L41)).
- Check timers with `systemctl --user list-timers 'feedback-*'`, run one with `systemctl --user start`, and read output with `journalctl --user -u <unit>` ([scripts/learning_loop/systemd/README.md:45-48](../scripts/learning_loop/systemd/README.md#L45-L48)).
- Each run fetches and resets its clone under `flock` and first deletes a git lock older than an hour ([scripts/learning_loop/systemd/feedback-collector.service:10-16](../scripts/learning_loop/systemd/feedback-collector.service#L10-L16)).
- Never commit anything from the output folder ([scripts/learning_loop/systemd/README.md:24-26](../scripts/learning_loop/systemd/README.md#L24-L26)).

## Hooks

- lefthook pulls `hooks/base.yml` from code2-workspace and refetches it daily ([lefthook.yml:1-7](../lefthook.yml#L1-L7)).

## Live check

- No live check was run in this version; the read-only check is `systemctl --user list-timers 'feedback-*'` ([scripts/learning_loop/systemd/README.md:45](../scripts/learning_loop/systemd/README.md#L45)).

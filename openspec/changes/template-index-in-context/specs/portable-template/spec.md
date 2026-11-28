## ADDED Requirements

### Requirement: A fresh copy starts each session with the wiki index

A repository made with `copier copy` SHALL have a `SessionStart` hook in both `.claude/settings.json` and
`.codex/hooks.json` that prints the text of `generated/wiki/index.md` as the session's added context
(`hookSpecificOutput.additionalContext`, with `hookEventName` `SessionStart`), and prints nothing when that file does
not exist.

Source: Brian, 2026-11-27: "the wiki is more for tha gent than anyone. python is fine as the first mielstone ... it
always has the high leve navtiational wiki index in its context". A hook rather than an instruction, and the same
hook for Claude and Codex, are inferred by agent (core.md: Claude and Codex behave the same).

#### Scenario: Both clients get the index at session start

- **GIVEN** the template rendered with its defaults
- **WHEN** the `SessionStart` hook command of `.claude/settings.json` and of `.codex/hooks.json` runs in it
- **THEN** each prints JSON whose `hookSpecificOutput.additionalContext` holds the text of `generated/wiki/index.md`

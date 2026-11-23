## ADDED Requirements

### Requirement: Handing over text never approves an edit

When the edit hook lets a call through with only context (requirement text, a plan, a warning), its answer to Claude Code and to Codex SHALL carry that context without a `permissionDecision`, so the agent's own permission settings still decide whether the edit runs; a refusal SHALL keep `permissionDecision: deny` and its reason.

Source: inferred by agent: Claude Code treats a PreToolUse `allow` as approving the call without the user's prompt (probe 2026-11-23: a context-only answer with no decision still reaches the model); the template now installs the hook in every copy (plan docs/planning/linked-chain-core-2026-11-23.md).

#### Scenario: A context-only answer carries no decision

- **GIVEN** an edit the hook lets through with requirement text
- **WHEN** the hook answers for Claude Code
- **THEN** the answer has `additionalContext` and no `permissionDecision`

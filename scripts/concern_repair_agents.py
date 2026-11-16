"""Launch full-harness Claude Code / Codex agents for concern repair via llm_client.

"Full harness" means the agent runs with the same instructions, hooks, skills,
and connectors an interactive session gets:

- Claude Code: ``setting_sources=["user", "project", "local"]`` so the Agent SDK
  loads ``~/.claude`` settings/hooks/skills and the repository ``CLAUDE.md``.
  (llm_client's default loads none of them.)
- Codex: ``codex_home`` is the real home, so ``~/.codex`` config, skills, hooks
  and MCP servers load. (llm_client's default is an isolated temporary home.)

Client choice is an ordered preference. A client that is *unavailable* -- its
subscription usage is exhausted, auth fails, or the model route is missing --
is skipped and the next one runs. Unavailability is decided by llm_client's own
typed error classification (``wrap_error``), never by matching prose here. Any
other failure is a real repair failure and is raised, not failed over.
"""

from __future__ import annotations

import os
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from concern_repair_contract import CLIENTS, ClientName, RootCauseReview

PROMPT_DIR = Path(__file__).resolve().parents[1] / "prompts" / "concern_repair"

DEFAULT_MODELS: dict[ClientName, str] = {
    "claude-code": os.environ.get("CONCERN_REPAIR_CLAUDE_MODEL", "claude-code/sonnet"),
    "codex": os.environ.get("CONCERN_REPAIR_CODEX_MODEL", "codex/gpt-5.6-sol"),
}

LlmCall = Callable[..., Any]


class NoAvailableClientError(RuntimeError):
    """Every configured client was unavailable; nothing ran."""


@dataclass
class AgentRun:
    client: ClientName
    result: Any
    unavailable: list[str] = field(default_factory=list)


def client_order(raw: str | None = None) -> list[ClientName]:
    """Parse ``CONCERN_REPAIR_CLIENT_ORDER`` (comma-separated), failing on unknown names."""
    value = raw if raw is not None else os.environ.get("CONCERN_REPAIR_CLIENT_ORDER", "claude-code,codex")
    order: list[ClientName] = []
    for name in (part.strip() for part in value.split(",")):
        if not name:
            continue
        if name not in CLIENTS:
            raise ValueError(f"unknown concern-repair client {name!r}; expected one of {CLIENTS}")
        if name not in order:
            order.append(name)  # type: ignore[arg-type]
    if not order:
        raise ValueError("CONCERN_REPAIR_CLIENT_ORDER names no client")
    return order


def is_unavailable(exc: BaseException) -> bool:
    """True when llm_client classifies the failure as the client being unusable right now."""
    from llm_client.core.errors import (
        LLMAuthError,
        LLMModelNotFoundError,
        LLMQuotaExhaustedError,
        LLMRateLimitError,
        wrap_error,
    )

    if not isinstance(exc, Exception):
        return False
    wrapped = wrap_error(exc)
    return isinstance(wrapped, (LLMQuotaExhaustedError, LLMRateLimitError, LLMAuthError, LLMModelNotFoundError))


def harness_kwargs(client: ClientName, workspace: Path, *, timeout_seconds: int, reviewer: bool = False) -> dict[str, Any]:
    """llm_client kwargs for one client.

    The repairer gets the full native harness with write access. The reviewer is
    deliberately the opposite: read-only and isolated from user settings, hooks,
    and session history, so its verdict rests only on the issue, diff, and report.
    """
    justification = {
        False: "Unattended root-cause repair of one feedback concern using subscription agent capacity.",
        True: "Independent read-only root-cause review of one automated repair using subscription agent capacity.",
    }[reviewer]
    if client == "claude-code":
        # No per-call ``timeout``: llm_client's default timeout policy ignores it.
        # The bound is the process safety ceiling set by ``apply_safety_ceiling``.
        return {
            "execution_mode": "workspace_agent",
            "cwd": str(workspace),
            "setting_sources": [] if reviewer else ["user", "project", "local"],
            "permission_mode": "plan" if reviewer else "bypassPermissions",
            "max_turns": 8 if reviewer else int(os.environ.get("CONCERN_REPAIR_MAX_TURNS", "200")),
            "model_justification": justification,
        }
    kwargs: dict[str, Any] = {
        "execution_mode": "workspace_agent",
        "codex_transport": "cli",
        "working_directory": str(workspace),
        "sandbox_mode": "read-only" if reviewer else "danger-full-access",
        "approval_policy": "never",
        "reasoning_effort": "high",
        "agent_hard_timeout": timeout_seconds,
        "model_justification": justification,
    }
    if not reviewer:
        kwargs["codex_home"] = str(Path.home())
    return kwargs


def apply_safety_ceiling(timeout_seconds: int) -> None:
    """Bound every agent attempt in this process.

    llm_client's safety ceiling (``LLM_CLIENT_SAFETY_TIMEOUT``, default 300s)
    applies even when per-call timeouts are banned. Left at the default, a real
    repair is cancelled after five minutes; unset entirely, nothing bounds it.
    """
    os.environ["LLM_CLIENT_SAFETY_TIMEOUT"] = str(int(timeout_seconds))


def run_with_failover(
    messages_for: Callable[[ClientName], list[dict[str, str]]],
    *,
    order: Sequence[ClientName],
    workspace: Path,
    task: str,
    trace_id: str,
    timeout_seconds: int,
    call: LlmCall | None = None,
) -> AgentRun:
    """Run the first available client; raise on a real failure, never fall through silently.

    ``messages_for`` renders per client, because the prompt names the client that
    must own the claim it creates.
    """
    if call is None:
        from llm_client import call_llm as call
    apply_safety_ceiling(timeout_seconds)
    unavailable: list[str] = []
    for client in order:
        try:
            result = call(
                DEFAULT_MODELS[client],
                messages_for(client),
                task=f"{task}.{client}",
                trace_id=f"{trace_id}/{client}",
                max_budget=0,
                **harness_kwargs(client, workspace, timeout_seconds=timeout_seconds),
            )
        except Exception as exc:  # noqa: BLE001 - classified, then re-raised unless unavailable
            if is_unavailable(exc):
                unavailable.append(f"{client}: {type(exc).__name__}: {str(exc)[:300]}")
                continue
            raise
        return AgentRun(client=client, result=result, unavailable=unavailable)
    raise NoAvailableClientError("no concern-repair client available: " + " | ".join(unavailable))


def review_root_cause(
    messages: list[dict[str, str]],
    *,
    order: Sequence[ClientName],
    workspace: Path,
    task: str,
    trace_id: str,
    timeout_seconds: int,
    call_structured: LlmCall | None = None,
) -> tuple[ClientName, RootCauseReview, list[str]]:
    """Independent structured review in a read-only, fresh-context session."""
    if call_structured is None:
        from llm_client import call_llm_structured as call_structured
    apply_safety_ceiling(timeout_seconds)
    unavailable: list[str] = []
    for client in order:
        try:
            parsed, _meta = call_structured(
                DEFAULT_MODELS[client],
                messages,
                response_model=RootCauseReview,
                task=f"{task}.{client}",
                trace_id=f"{trace_id}/{client}",
                max_budget=0,
                **harness_kwargs(client, workspace, timeout_seconds=timeout_seconds, reviewer=True),
            )
        except Exception as exc:  # noqa: BLE001 - classified, then re-raised unless unavailable
            if is_unavailable(exc):
                unavailable.append(f"{client}: {type(exc).__name__}: {str(exc)[:300]}")
                continue
            raise
        return client, RootCauseReview.model_validate(parsed.model_dump() if hasattr(parsed, "model_dump") else parsed), unavailable
    raise NoAvailableClientError("no reviewer client available: " + " | ".join(unavailable))

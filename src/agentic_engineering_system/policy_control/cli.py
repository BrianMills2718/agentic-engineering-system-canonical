from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .models import ReplayCaseV1
from .providers.openrouter import (
    DEFAULT_PLAN002_MODEL,
    OpenRouterClient,
    VerificationSupportOpenRouterEvaluator,
)
from .render import write_report_bundle
from .replay import run_offline_replay


def _api_key(env_name: str) -> str:
    value = os.environ.get(env_name)
    if not value:
        raise SystemExit(f"{env_name} is not set")
    return value


def _load_case(path: Path) -> ReplayCaseV1:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"unable to read replay case {path}: {exc}") from exc
    return ReplayCaseV1.model_validate(payload)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Plan 002 offline policy-decision replay; never a live policy hook."
    )
    parser.add_argument(
        "--api-key-env",
        default="OPENROUTER_API_KEY",
        help="Environment variable containing the OpenRouter API key.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser(
        "models",
        help="List OpenRouter model IDs that advertise structured-output support.",
    )

    run = sub.add_parser("run", help="Run one frozen offline replay case.")
    run.add_argument("--case", type=Path, required=True)
    run.add_argument("--model", default=DEFAULT_PLAN002_MODEL)
    run.add_argument("--output-dir", type=Path, required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    client = OpenRouterClient(api_key=_api_key(args.api_key_env))

    if args.command == "models":
        print(json.dumps({"models": list(client.list_structured_models())}, indent=2))
        return

    case = _load_case(args.case)
    evaluator = VerificationSupportOpenRouterEvaluator(
        client=client,
        model=args.model,
    )
    report = run_offline_replay(
        evaluator_input=case.evaluator_input,
        baseline=case.baseline,
        evaluator=evaluator,
        later_outcome=case.later_outcome,
    )
    json_path, html_path = write_report_bundle(args.output_dir, report)
    print(json_path)
    print(html_path)


if __name__ == "__main__":
    main()

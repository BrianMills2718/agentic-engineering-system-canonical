from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .models import ReplayCaseV1
from .providers.jev import JevClient, VerificationSupportJevEvaluator
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


def _write_report(path: Path, report: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = report.model_dump(mode="json")  # type: ignore[attr-defined]
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Plan 002 offline policy-decision replay; never a live policy hook."
    )
    parser.add_argument(
        "--api-key-env",
        default="TYPESAFE_API_KEY",
        help="Environment variable containing the TypeSafe API key.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("models", help="List model names available to the authenticated account.")

    run = sub.add_parser("run", help="Run one frozen offline replay case.")
    run.add_argument("--case", type=Path, required=True)
    run.add_argument("--model", required=True, help="Exact model name or alias selected from models.")
    run.add_argument("--output", type=Path, required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    client = JevClient(api_key=_api_key(args.api_key_env))

    if args.command == "models":
        print(json.dumps({"models": list(client.list_models())}, indent=2))
        return

    case = _load_case(args.case)
    evaluator = VerificationSupportJevEvaluator(client=client, model=args.model)
    report = run_offline_replay(
        evaluator_input=case.evaluator_input,
        baseline=case.baseline,
        evaluator=evaluator,
        later_outcome=case.later_outcome,
    )
    _write_report(args.output, report)
    print(args.output)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
from pathlib import Path

from .render_html import write_surface
from .resolver import resolve_repository_context


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aes-repo-context", description="Resolve source-bound repository context.")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--expect-revision")
    parser.add_argument("--output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        artifact = resolve_repository_context(args.repo, expect_revision=args.expect_revision)
    except (ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    root = Path(args.output) if args.output else Path("generated") / "repository-context" / artifact.repository_id / artifact.revision
    json_path, html_path = write_surface(artifact, root)
    print(f"{artifact.repository_id}@{artifact.revision}: {artifact.resolution_status.value}")
    print(f"JSON: {json_path}")
    print(f"HTML: {html_path}")
    if artifact.resolution_status.value == "ERROR":
        print("Recovery: correct the authoritative repository declaration and retry; no legacy fallback was used.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

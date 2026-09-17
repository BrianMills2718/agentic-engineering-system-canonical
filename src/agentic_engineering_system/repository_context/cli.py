from __future__ import annotations

import argparse
from pathlib import Path

from .render_html import write_outputs
from .resolver import RepositoryContextResolver


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resolve repository navigation and authority context.")
    parser.add_argument("--repo", required=True, type=Path, help="Local repository checkout.")
    parser.add_argument("--expect-revision", help="Require this exact Git revision.")
    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory. Defaults to generated/repository-context/<repository>/<revision>.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    artifact = RepositoryContextResolver(args.repo).resolve(args.expect_revision)
    output = args.output or (
        Path("generated")
        / "repository-context"
        / artifact.repository_id.replace("/", "__")
        / artifact.revision
    )
    json_path, html_path = write_outputs(artifact, output)
    print(f"resolution: {artifact.resolution_status.value}")
    print(f"context: {json_path}")
    print(f"surface: {html_path}")
    return 0 if artifact.resolution_status.value != "ERROR" else 2


if __name__ == "__main__":
    raise SystemExit(main())

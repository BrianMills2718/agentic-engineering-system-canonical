"""`aes` console entrypoint (probe 0).

    aes target validate [--root DIR]
    aes context <subject> [--root DIR] [--format markdown|json]
    aes topology check [--root DIR]
    aes evidence status [--root DIR]

Exit 0 on success, 1 on any load/validation/context/topology error or orphan (message on stderr),
2 on usage errors (argparse).
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from .evidence import EvidenceError, assess
from .evidence import render_report as render_evidence
from .context import ContextError, project_context, render_json, render_markdown
from .records import RecordLoadError, TargetValidationError, load_project, load_target
from .topology import TopologyError, check_topology, render_report


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aes", description="Agentic Engineering System (v0.2 probe 0)")
    sub = parser.add_subparsers(dest="command", required=True)

    target = sub.add_parser("target", help="operate on .aes/target.yaml")
    target_sub = target.add_subparsers(dest="target_command", required=True)
    validate = target_sub.add_parser("validate", help="strictly load and validate the target")
    validate.add_argument("--root", type=Path, default=Path("."), help="project root (default: .)")

    context = sub.add_parser("context", help="compile the working context for one subject ID")
    context.add_argument("subject", help="a declared ID: component, artifact, criterion, normative item or outcome")
    context.add_argument("--root", type=Path, default=Path("."), help="project root (default: .)")
    context.add_argument("--format", choices=["markdown", "json"], default="markdown")

    topology = sub.add_parser("topology", help="compare governed roots in Git with planned artifacts")
    topology_sub = topology.add_subparsers(dest="topology_command", required=True)
    check = topology_sub.add_parser("check", help="fail on any governed file the target does not plan")
    check.add_argument("--root", type=Path, default=Path("."), help="project root (default: .)")

    evidence = sub.add_parser("evidence", help="observations, freshness and criterion standing")
    evidence_sub = evidence.add_subparsers(dest="evidence_command", required=True)
    status = evidence_sub.add_parser("status", help="standing of every success criterion (decision D2)")
    status.add_argument("--root", type=Path, default=Path("."), help="project root (default: .)")
    return parser


def _cmd_target_validate(root: Path) -> int:
    root = root.resolve()
    project = load_project(root / ".aes" / "project.yaml")
    target_path = root / project.materialization.target_path
    target = load_target(target_path)
    er_count = len(target.evidence_requirements())
    print(
        f"OK {target_path}\n"
        f"  target_id={target.target_id} schema_version={target.schema_version}\n"
        f"  outcomes={len(target.outcomes)} normative_items={len(target.normative_items)} "
        f"success_criteria={len(target.success_criteria)} evidence_requirements={er_count}\n"
        f"  components={len(target.components)} planned_artifacts={len(target.planned_artifacts)} "
        f"verification_subjects={len(target.verification_subjects)}\n"
        f"  governed_roots={project.governed_roots}"
    )
    return 0


def _cmd_context(root: Path, subject: str, fmt: str) -> int:
    ctx = project_context(root, subject)
    print(render_json(ctx) if fmt == "json" else render_markdown(ctx))
    return 0


def _cmd_topology_check(root: Path) -> int:
    report = check_topology(root)
    print(render_report(report), file=sys.stdout if report.ok else sys.stderr)
    return 0 if report.ok else 1


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "target" and args.target_command == "validate":
            return _cmd_target_validate(args.root)
        if args.command == "context":
            return _cmd_context(args.root, args.subject, args.format)
        if args.command == "topology" and args.topology_command == "check":
            return _cmd_topology_check(args.root)
        if args.command == "evidence" and args.evidence_command == "status":
            print(render_evidence(assess(args.root)))
            return 0
    except (RecordLoadError, TargetValidationError, ContextError, TopologyError, EvidenceError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    raise AssertionError(f"unhandled command {args.command!r}")  # argparse prevents this


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())

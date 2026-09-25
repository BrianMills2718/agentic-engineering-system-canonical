"""`aes` console entrypoint (probe 0).

    aes target validate [--root DIR]
    aes context <subject> [--root DIR] [--format markdown|json]
    aes topology check [--root DIR]
    aes evidence status [--root DIR]
    aes evidence record <VS-ID> [--depends-on PATH ...] [--command ...] [--inconclusive BASIS] [--root DIR]
    aes hooks install [--root DIR]
    aes characterize [--root DIR] [--json]
    aes --version

Exit 0 on success, 1 on any load/validation/context/topology error or orphan (message on stderr),
2 on usage errors (argparse).
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from .characterize import CharacterizeError
from .characterize import check as characterize_check
from .characterize import render_report as render_characterization
from .evidence import EvidenceError, assess, record
from .evidence import render_report as render_evidence
from .context import ContextError, project_context, render_json, render_markdown
from .hooks import HookInstallError, install_hooks
from .records import RecordLoadError, TargetValidationError, load_project, load_target
from .topology import TopologyError, check_topology, render_report


DISTRIBUTION = "agentic-engineering-system"


class _VersionAction(argparse.Action):
    """Print the installed distribution's version (Git-derived at build time)."""

    def __init__(self, option_strings: Sequence[str], dest: str, **kwargs: object) -> None:
        super().__init__(option_strings, dest, nargs=0, help="print the installed AES version and exit")

    def __call__(self, parser: argparse.ArgumentParser, *_: object) -> None:
        try:
            installed = version(DISTRIBUTION)
        except PackageNotFoundError:
            parser.exit(1, f"error: distribution {DISTRIBUTION!r} is not installed; no version to report\n")
        print(installed)
        parser.exit(0)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aes", description="Agentic Engineering System (v0.2 probe 0)")
    parser.add_argument("--version", action=_VersionAction)
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
    rec = evidence_sub.add_parser("record", help="run a deterministic-test verification subject and write its observation")
    rec.add_argument("subject", help="verification subject ID (VS-...)")
    rec.add_argument("--depends-on", action="append", default=[], metavar="PATH",
                     help="repository path the result depends on (repeatable), added to the test file and, "
                          "for a Python test, its discovered intra-repository imports")
    rec.add_argument("--command", dest="run_command", nargs=argparse.REMAINDER,
                     help="command to run instead of the ecosystem default (python: pytest on the locator)")
    rec.add_argument("--inconclusive", metavar="BASIS",
                     help="record a pass as INCONCLUSIVE, with this reason (test covers only part of the requirement)")
    rec.add_argument("--root", type=Path, default=Path("."), help="project root (default: .)")

    hooks = sub.add_parser("hooks", help="Git hooks that enforce the target")
    hooks_sub = hooks.add_subparsers(dest="hooks_command", required=True)
    install = hooks_sub.add_parser("install", help="write .githooks/pre-commit and set core.hooksPath")
    install.add_argument("--root", type=Path, default=Path("."), help="project root (default: .)")

    charac = sub.add_parser("characterize", help="revision-bound facts about the governed files, and drift from the target")
    charac.add_argument("--root", type=Path, default=Path("."), help="project root (default: .)")
    charac.add_argument("--json", action="store_true", help="print the characterization as JSON (drift goes to stderr)")
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
        if args.command == "evidence" and args.evidence_command == "record":
            done = record(args.root, args.subject, args.depends_on, args.run_command or None, args.inconclusive)
            a = done.observation.assessments
            print(f"wrote {done.path}\n  {a[0].assessment if a else 'no assessment'} for "
                  f"{', '.join(x.evidence_requirement_ref for x in a)} at {done.observation.subject_revision[:12]}")
            return 0
        if args.command == "evidence" and args.evidence_command == "status":
            print(render_evidence(assess(args.root)))
            return 0
        if args.command == "characterize":
            report = characterize_check(args.root)
            if args.json:
                print(report.characterization.model_dump_json(indent=2))
                failing = [d for d in report.drift if d.failing]
                for d in failing:
                    print(f"drift {d.kind}: {d.path} - {d.detail}", file=sys.stderr)
            else:
                print(render_characterization(report), file=sys.stdout if report.ok else sys.stderr)
            return 0 if report.ok else 1
        if args.command == "hooks" and args.hooks_command == "install":
            hook, overridden = install_hooks(args.root)
            print(f"wrote {hook}\n  core.hooksPath=.githooks; runs aes target validate + aes topology check")
            if overridden:
                print(f"  note: overrides the global core.hooksPath {overridden} in this repository", file=sys.stderr)
            return 0
    except (RecordLoadError, TargetValidationError, ContextError, TopologyError, EvidenceError,
            HookInstallError, CharacterizeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    raise AssertionError(f"unhandled command {args.command!r}")  # argparse prevents this


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())

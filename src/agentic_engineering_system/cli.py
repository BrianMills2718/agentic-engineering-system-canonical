"""`aes` console entrypoint (probe 0).

    aes init --project-id ID --actor TEXT --outcome TEXT [--governed-root R ...] [--language L] [--root DIR]
    aes target validate [--root DIR]
    aes context <subject> [--root DIR] [--format markdown|json]
    aes topology check [--root DIR]
    aes evidence status [--root DIR]
    aes evidence record <VS-ID> [--depends-on PATH ...] [--command ...] [--inconclusive BASIS] [--root DIR]
    aes hooks install [--root DIR]
    aes characterize [--root DIR] [--json]
    aes reconcile [--root DIR] [--json]
    aes status [--root DIR]
    aes plan prepare [--root DIR] [--out FILE]
    aes plan validate <proposal> [--root DIR]
    aes plan accept <proposal> [--root DIR]
    aes --version

Without --root, every command except init uses the nearest directory at or above
the current one that holds .aes/project.yaml; init uses the current directory.

Exit 0 on success, 1 on any load/validation/context/topology error or orphan (message on stderr),
2 on usage errors (argparse). reconcile and status also exit 1 on a REFUTED criterion or drift;
INSUFFICIENT criteria do not fail them. plan validate and plan accept exit 1 listing every
violation; plan accept does not commit.
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
from .planning import (
    PlanError,
    accept_proposal,
    load_proposal,
    prepare,
    render_accepted,
    render_validated,
    render_yaml,
    validate_proposal,
)
from .project import ProjectError, find_project_root, initialize_project
from .reconcile import reconcile, render_status
from .reconcile import render_report as render_reconciliation
from .records import RecordLoadError, TargetValidationError, load_project, load_target
from .topology import TopologyError, check_topology, render_report


DISTRIBUTION = "agentic-engineering-system"
ROOT_HELP = "project root (default: nearest directory at or above . holding .aes/project.yaml)"


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

    init = sub.add_parser("init", help="create .aes/project.yaml and a target holding the first outcome")
    init.add_argument("--project-id", required=True, help="stable project identifier, e.g. my-service")
    init.add_argument("--actor", required=True, help="who the first outcome is for (a person or consumer)")
    init.add_argument("--outcome", required=True, help="the first accepted outcome, as one statement")
    init.add_argument("--governed-root", action="append", dest="governed_roots", metavar="R",
                      help="directory whose tracked files must all be planned (repeatable; default: src/ tests/)")
    init.add_argument("--language", default="python",
                      help="primary language; selects evidence record's default test command (default: python)")
    init.add_argument("--root", type=Path, default=Path("."), help="top of the Git work tree (default: .)")

    target = sub.add_parser("target", help="operate on .aes/target.yaml")
    target_sub = target.add_subparsers(dest="target_command", required=True)
    validate = target_sub.add_parser("validate", help="strictly load and validate the target")
    validate.add_argument("--root", type=Path, default=None, help=ROOT_HELP)

    context = sub.add_parser("context", help="compile the working context for one subject ID")
    context.add_argument("subject", help="a declared ID: component, artifact, criterion, normative item or outcome")
    context.add_argument("--root", type=Path, default=None, help=ROOT_HELP)
    context.add_argument("--format", choices=["markdown", "json"], default="markdown")

    topology = sub.add_parser("topology", help="compare governed roots in Git with planned artifacts")
    topology_sub = topology.add_subparsers(dest="topology_command", required=True)
    check = topology_sub.add_parser("check", help="fail on any governed file the target does not plan")
    check.add_argument("--root", type=Path, default=None, help=ROOT_HELP)

    evidence = sub.add_parser("evidence", help="observations, freshness and criterion standing")
    evidence_sub = evidence.add_subparsers(dest="evidence_command", required=True)
    status = evidence_sub.add_parser("status", help="standing of every success criterion (decision D2)")
    status.add_argument("--root", type=Path, default=None, help=ROOT_HELP)
    rec = evidence_sub.add_parser("record", help="run a deterministic-test verification subject and write its observation")
    rec.add_argument("subject", help="verification subject ID (VS-...)")
    rec.add_argument("--depends-on", action="append", default=[], metavar="PATH",
                     help="repository path the result depends on (repeatable), added to the test file and, "
                          "for a Python test, its discovered intra-repository imports")
    rec.add_argument("--command", dest="run_command", nargs=argparse.REMAINDER,
                     help="command to run instead of the ecosystem default (python: pytest on the locator)")
    rec.add_argument("--inconclusive", metavar="BASIS",
                     help="record a pass as INCONCLUSIVE, with this reason (test covers only part of the requirement)")
    rec.add_argument("--root", type=Path, default=None, help=ROOT_HELP)

    hooks = sub.add_parser("hooks", help="Git hooks that enforce the target")
    hooks_sub = hooks.add_subparsers(dest="hooks_command", required=True)
    install = hooks_sub.add_parser("install", help="write .githooks/pre-commit and set core.hooksPath")
    install.add_argument("--root", type=Path, default=None, help=ROOT_HELP)

    charac = sub.add_parser("characterize", help="revision-bound facts about the governed files, and drift from the target")
    charac.add_argument("--root", type=Path, default=None, help=ROOT_HELP)
    charac.add_argument("--json", action="store_true", help="print the characterization as JSON (drift goes to stderr)")

    recon = sub.add_parser("reconcile", help="current state and open gaps: artifacts, criteria, observations, components")
    recon.add_argument("--root", type=Path, default=None, help=ROOT_HELP)
    recon.add_argument("--json", action="store_true", help="print the reconciliation as JSON (failures go to stderr)")
    stat = sub.add_parser("status", help="one screen: revision, counts, first open gap per component")
    stat.add_argument("--root", type=Path, default=None, help=ROOT_HELP)

    plan = sub.add_parser("plan", help="propose, validate and accept a target change before implementing it")
    plan_sub = plan.add_subparsers(dest="plan_command", required=True)
    prep = plan_sub.add_parser("prepare", help="open gaps, existing ids and an empty proposal to write against")
    prep.add_argument("--root", type=Path, default=None, help=ROOT_HELP)
    prep.add_argument("--out", type=Path, default=None, metavar="FILE", help="write the packet here instead of stdout")
    pval = plan_sub.add_parser("validate", help="apply a proposal in memory and report every violation")
    pval.add_argument("proposal", type=Path, help="proposal YAML (aes.v0_2.proposal.probe0)")
    pval.add_argument("--root", type=Path, default=None, help=ROOT_HELP)
    pacc = plan_sub.add_parser("accept", help="apply a valid proposal to the target and write the plan (no commit)")
    pacc.add_argument("proposal", type=Path, help="proposal YAML (aes.v0_2.proposal.probe0)")
    pacc.add_argument("--root", type=Path, default=None, help=ROOT_HELP)
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
        if args.command == "init":
            done = initialize_project(
                args.root, project_id=args.project_id, outcome=args.outcome, actor=args.actor,
                governed_roots=args.governed_roots or ("src/", "tests/"), language=args.language,
            )
            print("\n".join(f"wrote {p}" for p in done.written))
            print(f"  project_id={done.project.project_id} governed_roots={done.project.governed_roots} "
                  f"language={done.project.ecosystem.primary_language_or_runtime} "
                  f"aes={done.project.aes.distribution_version}\n"
                  f"  outcome {done.target.outcomes[0].id}; next: plan it in .aes/target.yaml, then aes target validate")
            return 0
        if args.root is None:
            args.root = find_project_root(Path.cwd())
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
        if args.command in ("reconcile", "status"):
            r = reconcile(args.root)
            if args.command == "reconcile" and args.json:
                print(r.model_dump_json(indent=2))
                for f in r.failures:
                    print(f"failure {f}", file=sys.stderr)
            else:
                text = render_status(r) if args.command == "status" else render_reconciliation(r)
                print(text, file=sys.stdout if r.ok else sys.stderr)
            return 0 if r.ok else 1
        if args.command == "plan" and args.plan_command == "prepare":
            text = render_yaml(prepare(args.root))
            if args.out is None:
                print(text, end="")
            else:
                args.out.write_text(text, encoding="utf-8")
                print(f"wrote {args.out}")
            return 0
        if args.command == "plan" and args.plan_command == "validate":
            print(render_validated(validate_proposal(args.root, load_proposal(args.proposal))))
            return 0
        if args.command == "plan" and args.plan_command == "accept":
            print(render_accepted(args.root, accept_proposal(args.root, args.proposal)))
            return 0
        if args.command == "hooks" and args.hooks_command == "install":
            hook, overridden = install_hooks(args.root)
            print(f"wrote {hook}\n  core.hooksPath=.githooks; runs aes target validate + aes topology check")
            if overridden:
                print(f"  note: overrides the global core.hooksPath {overridden} in this repository", file=sys.stderr)
            return 0
    except (RecordLoadError, TargetValidationError, ContextError, TopologyError, EvidenceError,
            HookInstallError, ProjectError, CharacterizeError, PlanError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    raise AssertionError(f"unhandled command {args.command!r}")  # argparse prevents this


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())

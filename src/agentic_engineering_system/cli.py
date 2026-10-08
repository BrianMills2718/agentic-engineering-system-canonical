"""`aes` console entrypoint (probe 0).

    aes init --project-id ID --actor TEXT --outcome TEXT [--governed-root R ...] [--language L] [--root DIR]
    aes adopt [--project-id ID --actor TEXT --outcome TEXT] [--governed-root R ...] [--revision REV] [--dry-run] [--root DIR]
    aes target validate [--root DIR]      (also: every evidence requirement has a route)
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
INSUFFICIENT criteria do not fail them, and neither does an accepted plan whose
accepted_at_revision is not reachable from HEAD (a warning line). plan validate and plan accept
exit 1 listing every violation; plan accept does not commit, and warns on stderr, as evidence
record does, when the revision it recorded is not on the default branch.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from . import adopt as _adopt
from .characterize import CharacterizeError
from .characterize import check as characterize_check
from .characterize import render_report as render_characterization
from .characterize import running_version
from .commit_rule import check_message, replay
from .evidence import EvidenceError, assess, branch_note, record
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
    route_violations,
    validate_proposal,
)
from .project import ProjectError, find_project_root, initialize_project
from .reconcile import reconcile, render_status
from .reconcile import render_report as render_reconciliation
from .records import RecordLoadError, TargetValidationError, load_project, load_target
from .topology import TopologyError, check_topology, render_report


ROOT_HELP = "project root (default: nearest directory at or above . holding .aes/project.yaml)"


class _VersionAction(argparse.Action):
    """Print the version of the running code: the installed distribution's version
    (Git-derived at build time), plus the running checkout's `git describe` when the
    code executes from a Git checkout (`characterize.running_version`)."""

    def __init__(self, option_strings: Sequence[str], dest: str, **kwargs: object) -> None:
        super().__init__(option_strings, dest, nargs=0, help="print the running AES version and exit")

    def __call__(self, parser: argparse.ArgumentParser, *_: object) -> None:
        try:
            running = running_version()
        except CharacterizeError as exc:
            parser.exit(1, f"error: {exc}\n")
        print(running)
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

    adp = sub.add_parser("adopt", help="existing repository: accept today's governed files as legacy in "
                         ".aes/legacy_baseline.json (initializing .aes/ first if absent)")
    adp.add_argument("--project-id", help="as aes init; only when the repository has no .aes/ yet")
    adp.add_argument("--actor", help="as aes init; only when the repository has no .aes/ yet")
    adp.add_argument("--outcome", help="as aes init; only when the repository has no .aes/ yet")
    adp.add_argument("--governed-root", action="append", dest="governed_roots", metavar="R",
                     help="as aes init (default: src/ tests/); only when the repository has no .aes/ yet")
    adp.add_argument("--language", default="python", help="as aes init (default: python)")
    adp.add_argument("--revision", default="HEAD", help="commit whose tracked files become legacy (default HEAD)")
    adp.add_argument("--dry-run", action="store_true", help="print what would be adopted; write nothing")
    adp.add_argument("--root", type=Path, default=Path("."), help="top of the Git work tree (default: .)")

    target = sub.add_parser("target", help="operate on .aes/target.yaml")
    target_sub = target.add_subparsers(dest="target_command", required=True)
    validate = target_sub.add_parser("validate", help="strictly load and validate the target; every evidence requirement needs a route")
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
    install = hooks_sub.add_parser("install", help="write .githooks/pre-commit and commit-msg and set core.hooksPath")
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
    commit = sub.add_parser("commit", help="the commit-tag rule (AP-REQ-001): real work lands only under an adopted plan")
    commit_sub = commit.add_subparsers(dest="commit_command", required=True)
    cchk = commit_sub.add_parser("check", help="judge the commit being made (run by the commit-msg hook)")
    cchk.add_argument("message_file", type=Path, help="the commit message file git passes to commit-msg")
    cchk.add_argument("--root", type=Path, default=None, help=ROOT_HELP)
    crep = commit_sub.add_parser("replay", help="judge past commits with today's rule and receipts")
    crep.add_argument("revisions", nargs="?", default="HEAD", help="revision or range (default HEAD)")
    crep.add_argument("-n", "--max-count", type=int, default=300, help="commits to judge (default 300)")
    crep.add_argument("--root", type=Path, default=None,
                      help="repository root (default: top of the current Git work tree)")
    crep.add_argument("--json", action="store_true", help="one JSON object per commit, then the counts")
    cidx = commit_sub.add_parser("index", help="record which plans each repository holds on its default branch "
                                 "(read through git), for [Goal <id>] lookups when a checkout is on another branch")
    cidx.add_argument("--workspace", type=Path, default=Path.home() / "code",
                      help="folder whose child repositories are indexed (default ~/code)")
    cidx.add_argument("--fetch", action="store_true",
                      help="git fetch origin in every repository first, so plans merged on GitHub are seen")
    cidx.add_argument("--root", type=Path, default=None, help=argparse.SUPPRESS)
    return parser


def _cmd_commit_replay(root: Path, revisions: str, max_count: int, as_json: bool) -> int:
    import json
    from dataclasses import asdict

    rows, counts = replay(root, revisions, max_count)
    for sha, subject, verdict in rows:
        if as_json:
            print(json.dumps({"sha": sha, "subject": subject, **asdict(verdict)}))
        else:
            print(f"{verdict.verdict:<6} {sha[:8]} [{verdict.tag}] {subject[:90]}\n         {'; '.join(verdict.reasons)[:300]}")
    print(json.dumps(counts) if as_json else
          "replay: " + ", ".join(f"{k}={v}" for k, v in counts.items()))
    return 0


def _cmd_target_validate(root: Path) -> int:
    root = root.resolve()
    project = load_project(root / ".aes" / "project.yaml")
    target_path = root / project.materialization.target_path
    target = load_target(target_path)
    er_count = len(target.evidence_requirements())
    # SC-GF-004 on the whole current target, so the pre-commit hook refuses a
    # commit that adds a criterion no verification subject or boundary can supply.
    unrouted = route_violations(target)
    if unrouted:
        lines = "\n".join(f"  - {v}" for v in unrouted)
        print(f"error: {target_path}: {len(unrouted)} evidence requirement(s) with no route:\n{lines}",
              file=sys.stderr)
        return 1
    print(
        f"OK {target_path}\n"
        f"  target_id={target.target_id} schema_version={target.schema_version}\n"
        f"  outcomes={len(target.outcomes)} normative_items={len(target.normative_items)} "
        f"success_criteria={len(target.success_criteria)} evidence_requirements={er_count}\n"
        f"  components={len(target.components)} planned_artifacts={len(target.planned_artifacts)} "
        f"verification_subjects={len(target.verification_subjects)}\n"
        f"  governed_roots={project.governed_roots}\n"
        f"  every evidence requirement has a route (verification subject or external boundary)"
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


INIT_NEXT_STEP = (
    "next: aes plan prepare, write a proposal, aes plan validate/accept; "
    "or edit .aes/target.yaml by hand, then aes target validate"
)


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
                  f"  outcome {done.target.outcomes[0].id}\n"
                  f"  {INIT_NEXT_STEP}")
            if tracked := _adopt.tracked_under(args.root, done.project.governed_roots):
                print(f"warning: the governed roots already hold {tracked} tracked file(s); the pre-commit hook will "
                      f"refuse each as an orphan. For an existing codebase run `rm -r .aes && aes adopt` with the "
                      f"same arguments instead (docs/greenfield/GETTING_STARTED.md)", file=sys.stderr)
            return 0
        if args.command == "adopt":
            print(_adopt.render_adopted(_adopt.adopt(
                args.root, revision=args.revision, dry_run=args.dry_run, project_id=args.project_id,
                actor=args.actor, outcome=args.outcome, governed_roots=args.governed_roots, language=args.language)))
            return 0
        # needs no AES project: it reads every repository under the workspace
        if args.command == "commit" and args.commit_command == "index":
            import time
            from .commit_rule import build_plan_index, plan_index_path
            t0 = time.perf_counter()
            if args.fetch:
                from .commit_rule import fetch_all
                failed = fetch_all(args.workspace)
                print(f"fetch: {len(failed)} repositories failed, {time.perf_counter() - t0:.1f}s")
                for err in failed[:20]:
                    print(f"  {err}", file=sys.stderr)
            index = build_plan_index(args.workspace)
            plans = sum(len(e["plans"]) for e in index["repos"].values())
            print(f"plan index: {len(index['repos'])} repositories, {plans} plan ids on default branches, "
                  f"{time.perf_counter() - t0:.1f}s -> {plan_index_path()}")
            for err in index.get("errors", []):
                print(f"  not indexed (retried next build): {err}", file=sys.stderr)
            return 1 if index.get("errors") else 0
        if args.root is None:
            args.root = find_project_root(Path.cwd())
        if args.command == "target" and args.target_command == "validate":
            return _cmd_target_validate(args.root)
        if args.command == "context":
            return _cmd_context(args.root, args.subject, args.format)
        if args.command == "topology" and args.topology_command == "check":
            return _cmd_topology_check(args.root)
        if args.command == "evidence" and args.evidence_command == "record":
            recorded = record(args.root, args.subject, args.depends_on, args.run_command or None, args.inconclusive)
            a = recorded.observation.assessments
            assert recorded.observation.subject_revision is not None  # record() always runs at HEAD
            print(f"wrote {recorded.path}\n  {a[0].assessment if a else 'no assessment'} for "
                  f"{', '.join(x.evidence_requirement_ref for x in a)} at {recorded.observation.subject_revision[:12]}")
            if recorded.branch_note:
                print(recorded.branch_note, file=sys.stderr)
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
                if args.command == "status" and (legacy := _adopt.legacy_state(args.root)):
                    text += "\n" + _adopt.render_legacy(legacy)
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
            accepted = accept_proposal(args.root, args.proposal)
            print(render_accepted(args.root, accepted))
            if pruned := _adopt.prune_baseline(args.root):
                print(f"  baseline: removed {len(pruned)} now planned or untracked from {_adopt.BASELINE_PATH} "
                      f"(commit it with the target): {', '.join(pruned)}")
            note = branch_note(args.root, accepted.revision, "this plan's accepted_at_revision stays reachable")
            if note:
                print(note, file=sys.stderr)
            return 0
        if args.command == "commit" and args.commit_command == "check":
            rule_status, rule_report = check_message(args.root or Path.cwd(), args.message_file)
            print(rule_report, file=sys.stderr)
            return rule_status
        if args.command == "commit" and args.commit_command == "replay":
            repo_root = args.root or Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                                                    text=True, check=True).stdout.strip())
            return _cmd_commit_replay(repo_root, args.revisions, args.max_count, args.json)
        if args.command == "hooks" and args.hooks_command == "install":
            hook, overridden = install_hooks(args.root)
            print(f"wrote {hook} and {hook.with_name('commit-msg')}\n  core.hooksPath=.githooks; pre-commit runs aes target validate + aes topology check; commit-msg runs aes commit check"
                  f"\n  aes.installer={sys.executable} in .git/config, so the tracked hook stays unchanged")
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

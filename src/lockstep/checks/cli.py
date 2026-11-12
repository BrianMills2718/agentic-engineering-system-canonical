"""`lockstep check <name> [options]`: run one commit check and apply its mode from `lockstep.yaml`.

Implements: lockstep-checks/each-check-can-be-set-to-block-warn-or-off-in-lockstep-yaml

Names: `trace`, `arch [gen|check]`, `test-first [--base REV]`, `sources [--json]`, `docmeta`, `project [--check]`; each takes
`--repo PATH` (default the current folder). The output is code2check's, ending in a `RESULT` line.
Exit: the check's own status when its mode is `block` (the default); 0 with a `warning:` line when
it fails and its mode is `warn`; 0 with `skipped (off)` and nothing run when `off`; 2 when
`lockstep.yaml` or the options cannot be read.
"""

import argparse
import json
from pathlib import Path
import sys

from lockstep.checks import arch, docmeta, project, show, sources, status, test_first, trace
from lockstep.checks.config import CHECK_NAMES, Config, ConfigError, load


def _trace(root: Path, args: argparse.Namespace, cfg: Config) -> int:
    """Print trace findings and return the exit status."""
    findings = trace.check(root)
    for f in findings:
        print(f"{f.kind:13} {f.id}  ({f.where})")
    print(f"RESULT trace findings={len(findings)} exit={int(bool(findings))}")
    return int(bool(findings))


def _arch(root: Path, args: argparse.Namespace, cfg: Config) -> int:
    """Write or compare the import contracts and return the exit status."""
    action = args.action
    try:
        text = arch.generate(root, cfg.likec4)
    except arch.DiagramInvalid as err:
        print(err)
        print(f"RESULT arch-{action} invalid_diagram=1 exit=1")
        return 1
    path = root / arch.CONTRACTS
    if action == "gen":
        path.write_text(text)
        print(f"RESULT arch-gen wrote={path.name} exit=0")
        return 0
    current = path.read_text() if path.exists() else ""
    stale = current != text
    if stale:
        print(f"{path.name} does not match the diagram; run: lockstep check arch gen")
    print(f"RESULT arch-check stale={int(stale)} exit={int(stale)}")
    return int(stale)


def _test_first(root: Path, args: argparse.Namespace, cfg: Config) -> int:
    """Print tests that passed on base and return the exit status."""
    result = test_first.check(root, args.base)
    if result.skipped:
        print(f"RESULT test-first skipped=\"{result.skipped}\" exit=0")
        return 0
    for node in result.passed_before:
        print(f"passed-before {node}  (it does not prove the new behavior)")
    for node in result.existing:
        print(f"existing      {node}  (marked existing=True; not run on the base)")
    print(f"RESULT test-first checked={len(result.checked)} existing={len(result.existing)} "
          f"passed_before={len(result.passed_before)} exit={int(not result.ok)}")
    return int(not result.ok)


def _sources(root: Path, args: argparse.Namespace, cfg: Config) -> int:
    """Print items without a source (or all items as JSON) and return the exit status."""
    items = sources.check(root, cfg.human_pattern)
    missing = [i for i in items if i.source == "missing"]
    if args.json:
        print(json.dumps(sources.as_dicts(items), indent=1))
    for i in missing:
        print(f"no-source     {i.id}  ({i.where}); add a line: Source: Brian, <date>: \"<quote>\" or "
              "Source: inferred by agent (<basis>)", file=sys.stderr if args.json else sys.stdout)
    counts = {k: sum(i.source == k for i in items) for k in ("brian", "inferred", "other", "missing")}
    print("RESULT sources " + " ".join(f"{k}={v}" for k, v in counts.items()) + f" exit={int(bool(missing))}")
    return int(bool(missing))


def _docmeta(root: Path, args: argparse.Namespace, cfg: Config) -> int:
    """Print the docmeta count line and one line per finding; return 1 on any finding."""
    result = docmeta.check(root)
    print(result.count_line())
    for f in result.findings:
        print(f"{f.kind:28} {f.where}  ({f.reason})")
    return int(bool(result.findings))


def _project(root: Path, args: argparse.Namespace, cfg: Config) -> int:
    """Rewrite generated blocks (or with --check, list stale ones) and return the exit status.

    Implements: lockstep-projection/project-status-and-show-are-lockstep-commands

    Requirement text (generated):
        lockstep-projection/project-status-and-show-are-lockstep-commands: `lockstep check project`,
            `lockstep status` and `lockstep show` SHALL be commands of the one `lockstep` tool;
            `project` SHALL take its mode (block, warn or off) from `lockstep.yaml` like the other
            checks, and SHALL read source and test folders from `[tool.lockstep]` in
            `pyproject.toml`, else from `[tool.code2check]`.
    """
    changed = project.project(root, check=args.check)
    for path in changed:
        print(f"stale         {path}" if args.check else f"rewrote {path}")
    if args.check:
        if changed:
            print("generated blocks are out of date; run: lockstep check project")
        print(f"RESULT project stale={len(changed)} exit={int(bool(changed))}")
        return int(bool(changed))
    print(f"RESULT project rewrote={len(changed)} exit=0")
    return 0


def run_status(argv: list[str]) -> int:
    """`lockstep status [--json|--md] [--repo PATH]`: print the status table, JSON or Markdown page; exit 0.

    Implements: lockstep-projection/project-status-and-show-are-lockstep-commands

    Requirement text (generated):
        lockstep-projection/project-status-and-show-are-lockstep-commands: `lockstep check project`,
            `lockstep status` and `lockstep show` SHALL be commands of the one `lockstep` tool;
            `project` SHALL take its mode (block, warn or off) from `lockstep.yaml` like the other
            checks, and SHALL read source and test folders from `[tool.lockstep]` in
            `pyproject.toml`, else from `[tool.code2check]`.

    Args:
        argv: The options after `status`.

    Returns:
        0, or 2 when the options cannot be read.
    """
    ap = argparse.ArgumentParser(prog="lockstep status", description="each requirement's code, tests and result")
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--json", action="store_true", help="print the report as JSON")
    ap.add_argument("--md", action="store_true", help="print the report as the Markdown status page")
    try:
        args = ap.parse_args(argv)
    except SystemExit as exit_:
        return int(exit_.code or 0) if isinstance(exit_.code, int) else 2
    result = status.report(args.repo)
    if args.md:
        print(status.markdown(result))
        return 0
    if args.json:
        print(json.dumps(result.as_dict(), indent=1))
    else:
        print(f"results: {result.results_note}")
        for ident, req in result.requirements.items():
            print(f"{req.state:24} {ident}  {', '.join(req.links) or '-'}")
            for sid, sc in result.scenarios.items():
                if sc.requirement == ident:
                    print(f"  {sc.state:22} {sid}  {', '.join(sc.links) or '-'}")
        for plan in result.plans:
            shown = ", ".join(f"{i} ({s})" for i, s in plan.open.items()) or "none"
            print(f"plan {plan.path}: {len(plan.closes)} closes, open: {shown}")
    print("RESULT status " + " ".join(f"{k}={v}" for k, v in result.counts().items()) + " exit=0")
    return 0


def run_show(argv: list[str]) -> int:
    """`lockstep show FILE [--repo PATH]`: print the requirements a file implements; exit 0.

    Implements: lockstep-projection/project-status-and-show-are-lockstep-commands

    Requirement text (generated):
        lockstep-projection/project-status-and-show-are-lockstep-commands: `lockstep check project`,
            `lockstep status` and `lockstep show` SHALL be commands of the one `lockstep` tool;
            `project` SHALL take its mode (block, warn or off) from `lockstep.yaml` like the other
            checks, and SHALL read source and test folders from `[tool.lockstep]` in
            `pyproject.toml`, else from `[tool.code2check]`.

    Args:
        argv: The file, then options.

    Returns:
        0, or 2 when the options cannot be read.
    """
    ap = argparse.ArgumentParser(prog="lockstep show", description="the requirements a file implements")
    ap.add_argument("file")
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    try:
        args = ap.parse_args(argv)
    except SystemExit as exit_:
        return int(exit_.code or 0) if isinstance(exit_.code, int) else 2
    text = show.show(args.repo, args.file)
    print(text or f"{args.file} implements no requirement", end="" if text else "\n")
    print(f"RESULT show requirements={sum(1 for line in text.splitlines()[1:] if not line.startswith(' '))} exit=0")
    return 0


def run(argv: list[str]) -> int:
    """Run the named check, `argv[0]`, with its options and apply its mode.

    Args:
        argv: The check name, then its options.

    Returns:
        The exit status described in the module docstring.
    """
    ap = argparse.ArgumentParser(prog="lockstep check", description="run one commit check")
    sub = ap.add_subparsers(dest="name", required=True)
    for name in CHECK_NAMES:
        p = sub.add_parser(name)
        p.add_argument("--repo", type=Path, default=Path.cwd())
        if name == "arch":
            p.add_argument("action", nargs="?", choices=["gen", "check"], default="check")
        if name == "test-first":
            p.add_argument("--base", default="origin/main")
        if name == "project":
            p.add_argument("--check", action="store_true", help="fail when a generated block is stale, writing nothing")
        if name == "sources":
            p.add_argument("--json", action="store_true", help="print every item with its source")
    try:
        args = ap.parse_args(argv)
    except SystemExit as exit_:
        return int(exit_.code or 0) if isinstance(exit_.code, int) else 2
    root = args.repo
    try:
        cfg = load(root)
    except ConfigError as err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    mode = cfg.mode(args.name)
    if mode == "off":
        print(f"{args.name}: skipped (off)")
        return 0
    runner = {"trace": _trace, "arch": _arch, "test-first": _test_first, "sources": _sources, "docmeta": _docmeta,
              "project": _project}
    status = runner[args.name](root, args, cfg)
    if status and mode == "warn":
        print(f"warning: {args.name} failed (mode warn in lockstep.yaml); not blocking")
        return 0
    return status

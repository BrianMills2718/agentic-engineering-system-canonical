"""`lockstep check <name> [options]`: run one commit check and apply its mode from `lockstep.yaml`.

Implements: lockstep-checks/each-check-can-be-set-to-block-warn-or-off-in-lockstep-yaml

Names: `trace`, `arch [gen|check]`, `test-first [--base REV]`, `sources [--json]`, `docmeta`; each takes
`--repo PATH` (default the current folder). The output is code2check's, ending in a `RESULT` line.
Exit: the check's own status when its mode is `block` (the default); 0 with a `warning:` line when
it fails and its mode is `warn`; 0 with `skipped (off)` and nothing run when `off`; 2 when
`lockstep.yaml` or the options cannot be read.
"""

import argparse
import json
from pathlib import Path
import sys

from lockstep.checks import arch, docmeta, sources, test_first, trace
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
    runner = {"trace": _trace, "arch": _arch, "test-first": _test_first, "sources": _sources, "docmeta": _docmeta}
    status = runner[args.name](root, args, cfg)
    if status and mode == "warn":
        print(f"warning: {args.name} failed (mode warn in lockstep.yaml); not blocking")
        return 0
    return status

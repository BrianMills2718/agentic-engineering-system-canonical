"""Tell another gate whether a pushed commit changes plan content since a base, with ship's own question.

The push hook (personal-file-infra git-hooks/planning-gate.sh) calls this so that it and ship decide the same way
(Brian, 2026-11-12, "i approve decision 4", applied to the push hook by the coordinator's go-ahead on Decision 5).

Usage: plan_content.py --repo R --base B --head H --validator V [--python CMD]
Exit 0 and print the reason when no plan content changed between B and H; exit 1 and print why when it changed or
when anything is uncertain (H is not the checkout's HEAD, B is not a commit, the validator has no freshness()).

Implements: ship/answer-the-plan-content-question-for-the-push-hook

Requirement text (generated):
    ship/answer-the-plan-content-question-for-the-push-hook: `scripts/plan_content.py --repo R
        --base B --head H --validator V` SHALL answer whether the commits from B to H change plan
        content, using the same function `ship` uses, so the push hook and `ship` decide alike. It
        SHALL exit 0 and print a line starting `skip:` when nothing changed, and exit 1 with a line
        starting `validate:` when plan content changed or anything is uncertain: B is not a commit,
        H is not the checkout's HEAD, or the validator has no `freshness()`.
"""
from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ship  # noqa: E402  (beside this file)


def main(argv: list[str] | None = None) -> int:
    """Return 0 when no plan content changed between --base and --head, else 1."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--validator", required=True)
    parser.add_argument("--python", default=sys.executable, help="the interpreter that imports the validator")
    args = parser.parse_args(argv)
    # The question runs in a scratch folder, so relative paths would point there (found 2026-11-12 with --repo .).
    args.repo, args.validator = args.repo.resolve(), str(Path(args.validator).resolve())

    def rev(ref: str) -> str:
        """The commit a ref names, or "" when it names none."""
        done = subprocess.run(["git", "-C", str(args.repo), "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
                              capture_output=True, text=True)
        return done.stdout.strip() if done.returncode == 0 else ""
    head, base = rev("HEAD"), rev(args.base)
    if not base:
        print(f"validate: the base {args.base} is not a commit here")
        return 1
    if not head or head != rev(args.head):
        print(f"validate: the pushed commit {args.head[:12]} is not the checkout's HEAD {head[:12]}")
        return 1
    with tempfile.TemporaryDirectory(prefix="plan-content-") as scratch:
        reason, detail = ship.plan_unchanged_since(args.repo, base, shlex.split(args.python), args.validator,
                                                   Path(scratch))
    print(f"skip: {reason}" if reason else f"validate: {detail}")
    return 0 if reason else 1


if __name__ == "__main__":
    sys.exit(main())

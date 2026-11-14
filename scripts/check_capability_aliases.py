#!/usr/bin/env python3
"""Check the capability alias table against the native catalogue records.

Fails (exit 1) when a referenced ID does not exist, or a catalogue family, ACA package or ACA
candidate is missing or listed twice. Fails closed (exit 2) when a source cannot be read or parsed.
Usage: check_capability_aliases.py --pm CATALOGUE --aca REGISTRY --candidates CANDIDATES [--aliases FILE]
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

import yaml

DEFAULT = Path(__file__).resolve().parents[1] / "docs/decisions/0014-capability-aliases.yaml"


def load(path: Path):
    try:
        return yaml.safe_load(path.read_text())
    except (OSError, yaml.YAMLError) as exc:
        raise SystemExit(f"error: cannot read {path}: {exc}") from exc


def problems(aliases: dict, pm: dict, aca: dict, cands: dict) -> list[str]:
    families = {e["capability_family_id"] for e in pm["entries"]}
    packages = set(aca["capabilities"])
    candidates = {c["id"] for c in cands["candidates"]}
    rows = aliases["aliases"]
    out = [f"duplicate alias id {k}" for k, v in Counter(r["id"] for r in rows).items() if v > 1]
    fam_use = Counter(f for r in rows for f in r["project_meta_families"])
    aca_use = Counter(a for r in rows for a in r["aca"])
    for f in fam_use:
        if f not in families:
            out.append(f"unknown catalogue family {f}")
    for a in aca_use:
        if a not in packages | candidates:
            out.append(f"unknown ACA identifier {a}")
    out += [f"catalogue family not covered exactly once: {f} ({fam_use[f]})" for f in sorted(families) if fam_use[f] != 1]
    out += [f"ACA record not covered exactly once: {a} ({aca_use[a]})" for a in sorted(packages | candidates) if aca_use[a] != 1]
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--aliases", type=Path, default=DEFAULT)
    for name in ("pm", "aca", "candidates"):
        ap.add_argument(f"--{name}", type=Path, required=True)
    a = ap.parse_args(argv)
    found = problems(load(a.aliases), load(a.pm), load(a.aca), load(a.candidates))
    for line in found:
        print(line)
    print(f"alias check: {len(found)} problem(s)")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())

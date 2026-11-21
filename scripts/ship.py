#!/usr/bin/env python3
"""Moved to src/lockstep/ship.py (2026-11-20, so `uvx` can install `ship` from the public repository).

This file stays so the link ~/.local/bin/ship, the daily refresh of ~/.hive-brain/aes and code that imports `ship`
from scripts/ keep working. Run as a file it calls the module's main(); imported, it is the same module object as
lockstep.ship, so a test that patches one patches the other. lockstep.ship uses only the standard library.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from lockstep import ship as _module  # noqa: E402

if __name__ == "__main__":
    sys.exit(_module.main())
sys.modules[__name__] = _module

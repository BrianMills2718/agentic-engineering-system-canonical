"""People finder: find the people who work at a target company now."""

from __future__ import annotations

import json
from pathlib import Path

_PROFILES = Path(__file__).with_name("profiles.json")


def find_people(company: str) -> list[dict]:
    """Return the profiles of people whose current employer is `company`.

    [[[cog import lockstep.cogtext as c; c.docstring("ART-FINDER")]]]
    [[[end]]]
    """
    if not company.strip():
        raise ValueError("company name is empty")
    wanted = company.strip().casefold()
    profiles = json.loads(_PROFILES.read_text(encoding="utf-8"))
    return [p for p in profiles if p["employer"].casefold() == wanted]

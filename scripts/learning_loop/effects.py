"""Effect boundaries are explicit enforcement receipts, never issue-close dates."""
from __future__ import annotations

import datetime as dt
import json

from evidence import identity, sightings

MARKER = "<!-- feedback-enforcement "


def timestamp(value: str) -> dt.datetime | None:
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.astimezone(dt.timezone.utc) if parsed.tzinfo else None
    except (ValueError, TypeError, AttributeError):
        return None


def enforcement_receipt(comments: list[dict]) -> dict | None:
    receipts = []
    for comment in comments:
        body = comment.get("body", "")
        start = body.find(MARKER)
        end = body.find("-->", start + len(MARKER))
        if start < 0 or end < 0:
            continue
        try:
            receipt = json.loads(body[start + len(MARKER):end])
            when = timestamp(receipt.get("enforced_at", ""))
            filed = timestamp(comment.get("createdAt", ""))
            if when and filed and when <= filed and receipt.get("revision") and receipt.get("verification"):
                receipts.append(receipt)
        except (ValueError, AttributeError):
            continue
    return max(receipts, key=lambda r: timestamp(r["enforced_at"])) if receipts else None


def measure(members: list[dict], receipt: dict) -> dict:
    boundary = timestamp(receipt["enforced_at"])
    if boundary is None:
        raise ValueError("enforcement needs a timezone-aware timestamp")
    before, after, unknown = [], [], []
    for r in members:
        when = timestamp((r.get("provenance") or {}).get("ts", ""))
        (unknown if when is None else before if when <= boundary else after).append(r)
    # Restating a pre-fix incident in a later report is not a new failure.
    baseline = {identity(lk, (r.get("provenance") or {}).get("cwd", ""))
                for r in before for lk in r.get("resolved_links", [])}
    after = [r for r in after if not baseline.intersection(
        identity(lk, (r.get("provenance") or {}).get("cwd", "")) for lk in r.get("resolved_links", []))]
    return {"enforced_at": receipt["enforced_at"], "revision": receipt["revision"],
            "verification": receipt["verification"], "sightings_before": len(sightings(before)),
            "sightings_after": len(sightings(after)), "unknown_timestamp_records": len(unknown),
            "matched_after": [{"id": r["id"], "text": r["text"], "links": r["links"]} for r in after
                              if r["kind"] == "observation" and r.get("resolved_links")]}

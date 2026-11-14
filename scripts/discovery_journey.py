#!/usr/bin/env python3
"""Run the ecosystem discovery journey for two capabilities and the four failure exercises.

Reads the ecosystem-ops merged capability view (a pinned checkout), the shared contract registry
and the LLM observability database (read-only), and writes one JSON receipt with every input,
source revision, query, result and limit. No model call is made.

Usage: discovery_journey.py --ecosystem-ops DIR --data-dir DIR --out FILE
"""
from __future__ import annotations

import argparse
import copy
import importlib
import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

CAPABILITIES = {
    "llm_structured": {"boundary": "llm_client.call_llm_structured"},
    "web_search": {"boundary": "open_web_retrieval.search"},
}


def git_rev(path: Path) -> str:
    out = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, text=True)
    return out.stdout.strip() or "unknown"


def observed_callers(db: sqlite3.Connection, boundary: str) -> list[dict]:
    q = ("select project, sum(event_count), min(first_timestamp), max(last_timestamp) "
         "from boundary_success_aggregates where boundary_name=? group by project order by 2 desc")
    return [{"project": p, "events": n, "first": a, "last": b} for p, n, a, b in db.execute(q, (boundary,))]


def journey(cr, rows, contracts: dict, db: sqlite3.Connection, capability: str, boundary: str) -> dict:
    mine = [r for r in rows if r["capability_id"] == capability]
    contract = contracts.get(boundary, {})
    declared = contract.get("consumers", [])
    observed = observed_callers(db, boundary)
    observed_names = {o["project"] for o in observed}
    return {
        "capability": capability,
        "provider_rows": [{k: r.get(k) for k in ("project", "tool_name", "boundary_name", "surface_profile",
                                                  "provider_state", "catalog_status", "has_tool", "has_contract")}
                          for r in mine],
        "schema": {"boundary": boundary, "version_in_registry": contract.get("version"),
                   "version_in_view": next((r.get("contract_version") for r in rows if r.get("boundary_name") == boundary), None),
                   "input_schema_present": bool(contract.get("input_schema")),
                   "output_schema_present": bool(contract.get("output_schema"))},
        "declared_consumers": declared,
        "observed_callers": {"count_projects": len(observed), "top": observed[:5],
                             "declared_and_observed": sorted(set(declared) & observed_names),
                             "declared_not_observed": sorted(set(declared) - observed_names),
                             "observed_not_declared_count": len(observed_names - set(declared))},
    }


def exercise(cr, label: str, setup) -> dict:
    """Apply one fault to copies of the sources, run the view, restore the originals."""
    saved = {k: getattr(cr, k) for k in ("CAPABILITY_CATALOG", "REPO_TOOL_REGISTRY", "LEGACY_TOOL_REGISTRY", "CONTRACT_REGISTRY")}
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for key, src in saved.items():
            if Path(src).exists():
                shutil.copyfile(src, tmp / f"{key}{Path(src).suffix}")
                setattr(cr, key, tmp / f"{key}{Path(src).suffix}")
        try:
            setup(cr, tmp)
            rows, sources = cr.load_checked()
            return {"exercise": label,
                    "failed_sources": [{k: s[k] for k in ("source", "state", "detail")} for s in cr.source_errors(sources)
                                       if s["source"] != "tool_usage_observations"],
                    "rows": len(rows),
                    "catalog_status": {s: sum(1 for r in rows if r["catalog_status"] == s) for s in {r["catalog_status"] for r in rows}},
                    "catalogue_only_rows": sum(1 for r in rows if r.get("provider_state") == "catalogue_only")}
        finally:
            for key, value in saved.items():
                setattr(cr, key, value)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ecosystem-ops", type=Path, required=True)
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    sys.path.insert(0, str(a.ecosystem_ops))
    cr = importlib.import_module("capability_registry")
    cr.OBSERVABILITY_DB = a.data_dir / "llm_observability.db"
    cr.CONTRACT_REGISTRY = a.data_dir / "contract_registry.json"
    rows, sources = cr.load_checked()
    contracts = json.loads(cr.CONTRACT_REGISTRY.read_text())["contracts"]
    db = sqlite3.connect(f"file:{cr.OBSERVABILITY_DB}?mode=ro", uri=True)
    receipt = {
        "record": "discovery-journey-receipt/v1",
        "run_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "ecosystem_ops_revision": git_rev(a.ecosystem_ops),
        "sources": sources,
        "view": {"rows": len(rows), "distinct_capability_ids": len({r["capability_id"] for r in rows}),
                 "catalogue_only_rows": sum(1 for r in rows if r.get("provider_state") == "catalogue_only")},
        "journeys": [journey(cr, rows, contracts, db, c, v["boundary"]) for c, v in CAPABILITIES.items()],
    }
    def drop_catalogue(cr_, tmp):
        cr_.CAPABILITY_CATALOG.unlink()
    def break_catalogue(cr_, tmp):
        cr_.CAPABILITY_CATALOG.write_text("entries: [unclosed")
    def break_contracts(cr_, tmp):
        cr_.CONTRACT_REGISTRY.write_text("{not json")
    def stale_schema(cr_, tmp):
        data = json.loads(cr_.CONTRACT_REGISTRY.read_text())
        data["contracts"]["llm_client.call_llm_structured"]["version"] = "9.9.9-changed"
        cr_.CONTRACT_REGISTRY.write_text(json.dumps(data))
    ex = [exercise(cr, "catalogue file missing", drop_catalogue),
          exercise(cr, "catalogue file invalid", break_catalogue),
          exercise(cr, "contract registry invalid", break_contracts)]
    # Changed provider schema: the view is computed on read, so a changed version appears at once.
    saved = cr.CONTRACT_REGISTRY
    def view_version(path):
        cr.CONTRACT_REGISTRY = path
        found, _ = cr.load_checked()
        return next(r.get("contract_version") for r in found if r.get("boundary_name") == "llm_client.call_llm_structured")
    with tempfile.TemporaryDirectory() as tmp:
        copy_path = Path(tmp) / "contract_registry.json"
        data = json.loads(saved.read_text())
        copy_path.write_text(json.dumps(data))
        try:
            before = view_version(copy_path)
            data["contracts"]["llm_client.call_llm_structured"]["version"] = "9.9.9-changed"
            copy_path.write_text(json.dumps(data))
            after = view_version(copy_path)
            ex.append({"exercise": "provider schema version changed in the source", "view_version_before": before,
                       "view_version_after": after, "refreshed_on_next_read": before != after,
                       "note": "the view stores no copy: it is rebuilt from the sources on every read"})
        finally:
            cr.CONTRACT_REGISTRY = saved
    receipt["failure_exercises"] = ex
    receipt["limits"] = [
        "Declared consumers come from the contract registry; observed callers are project names in the observability aggregates. Names are compared as strings and a project may log under a different name.",
        "An observed call proves a call was logged, not that the output was fit for the caller's requirement.",
        "The schema version is the registry's recorded version; compatibility between provider and consumer is not tested here.",
    ]
    a.out.write_text(json.dumps(receipt, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {a.out}: {len(rows)} rows, {len(ex)} exercises")
    return 0


if __name__ == "__main__":
    sys.exit(main())

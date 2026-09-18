#!/usr/bin/env python3
"""Bounded structural conformance probe for AES-CP-PROFILE-001.

This checks whether the current AES architecture-realization blueprint carries
the information required by the accepted pilot profile. It does not execute
Company Planning, validate DesignPacketResult against its upstream JSON Schema,
or prove semantic correctness of the design.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import yaml


class ValidationError(ValueError):
    pass


def load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValidationError(f"{path}: expected mapping")
    return value


def require(value, message: str):
    if not value:
        raise ValidationError(message)


def validate(profile: dict, blueprint: dict) -> dict:
    require(profile.get("status") == "accepted_pilot_profile", "profile not accepted for pilot")
    transport = profile["transport"]
    require(transport.get("contract") == "DesignPacketResult", "unexpected generic transport")
    require(transport.get("change_required") is False, "generic handoff change incorrectly required")
    require(transport.get("detailed_design_field") == "design_packet_ref", "missing detailed design reference seam")

    require(blueprint.get("status") == "proposed", "blueprint falsely promoted")
    require(blueprint.get("not_claimed"), "blueprint missing non-claims")
    require(blueprint.get("sources"), "blueprint missing exact source references")
    require(blueprint.get("outcome"), "blueprint missing goal/outcome context")
    require(blueprint.get("normative_binding_proposal"), "blueprint missing source-local context policy")
    require(blueprint.get("state_rules"), "blueprint missing epistemic/non-promotion rules")

    components = blueprint.get("components", [])
    require(components, "blueprint has no components")
    for component in components:
        cid = component.get("id", "<missing>")
        for field in ("purpose", "provider_disposition", "code_home", "proposed_record", "boundary", "checks", "open_questions"):
            require(component.get(field), f"{cid}: missing {field}")
        boundary = component["boundary"]
        require(boundary.get("state"), f"{cid}: boundary state missing")
        if boundary["state"] == "unresolved":
            require(boundary.get("blocked_by"), f"{cid}: unresolved boundary has no blockers")
        checks = component["checks"]
        require(checks.get("obligation"), f"{cid}: verification obligation missing")
        require(checks.get("disproof"), f"{cid}: disproof missing")
        require(checks.get("planned_home") or checks.get("source"), f"{cid}: verification home/source missing")

    return {
        "profile": profile["id"],
        "blueprint": blueprint["id"],
        "components": len(components),
        "generic_transport_changed": False,
        "status": "accepted_by_bounded_probe",
    }


def self_test(profile: dict, blueprint: dict) -> dict:
    mutations = {}

    x = copy.deepcopy(blueprint)
    x["components"][0].pop("provider_disposition")
    mutations["missing_provider_disposition"] = x

    x = copy.deepcopy(blueprint)
    unresolved = next(component for component in x["components"] if component["boundary"]["state"] == "unresolved")
    unresolved["boundary"].pop("blocked_by")
    mutations["unresolved_without_blocker"] = x

    x = copy.deepcopy(blueprint)
    x["components"][0]["checks"].pop("disproof")
    mutations["missing_disproof"] = x

    x = copy.deepcopy(blueprint)
    x["not_claimed"] = []
    mutations["missing_nonclaims"] = x

    bad_profile = copy.deepcopy(profile)
    bad_profile["transport"]["change_required"] = True

    results = {}
    for name, candidate in mutations.items():
        try:
            validate(profile, candidate)
        except ValidationError as error:
            results[name] = {"rejected": True, "reason": str(error)}
        else:
            results[name] = {"rejected": False, "reason": "unexpectedly accepted"}

    try:
        validate(bad_profile, blueprint)
    except ValidationError as error:
        results["unjustified_generic_handoff_change"] = {"rejected": True, "reason": str(error)}
    else:
        results["unjustified_generic_handoff_change"] = {"rejected": False, "reason": "unexpectedly accepted"}

    if not all(item["rejected"] for item in results.values()):
        raise ValidationError(f"negative control failed: {results}")
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", type=Path)
    parser.add_argument("blueprint", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    profile = load(args.profile)
    blueprint = load(args.blueprint)
    result = validate(profile, blueprint)
    if args.self_test:
        result["negative_controls"] = self_test(profile, blueprint)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

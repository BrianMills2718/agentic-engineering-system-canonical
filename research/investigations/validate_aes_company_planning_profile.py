#!/usr/bin/env python3
"""Bounded structural/profile probe for AES-CP-PROFILE-001.

This checks that the AES-local Company Planning profile can carry the current
minimal architecture-realization record without changing the generic
DesignPacketResult transport. JSON Schema remains the structural authority for
architecture-realization records and should be run separately.

The probe also rejects already-resolved bootstrap AQRs when they are reused as
if they were still unresolved component questions or blockers. It does not
execute Company Planning or prove semantic correctness of a component design.
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


def resolved_aqr_ids(alignment: dict) -> set[str]:
    require(
        alignment.get("record_id") == "AES-BOOTSTRAP-ALIGNMENT-001",
        "unexpected bootstrap alignment record",
    )
    require(
        alignment.get("status") == "resolved_bootstrap_design_record",
        "bootstrap alignment is not resolved",
    )
    aqrs = alignment.get("aqrs", [])
    require(aqrs, "bootstrap alignment has no AQRs")
    return {
        item["id"]
        for item in aqrs
        if isinstance(item, dict) and item.get("status") == "resolved" and item.get("id")
    }


def validate(profile: dict, record: dict, alignment: dict) -> dict:
    require(profile.get("status") == "accepted_pilot_profile", "profile not accepted for pilot")

    transport = profile.get("transport", {})
    require(transport.get("contract") == "DesignPacketResult", "unexpected generic transport")
    require(transport.get("change_required") is False, "generic handoff change incorrectly required")
    require(
        transport.get("detailed_design_field") == "design_packet_ref",
        "missing detailed design reference seam",
    )

    architecture = profile.get("architecture_realization", {})
    require(architecture.get("schema_path"), "profile missing architecture schema path")
    require(architecture.get("schema_version"), "profile missing architecture schema version")
    require(
        architecture.get("bootstrap_probe_role") == "generated_non_authoritative_projection",
        "bootstrap probe role must remain non-authoritative",
    )
    require(architecture.get("design_packet_rule"), "profile missing design-packet rule")
    require(architecture.get("required_content"), "profile missing required content")

    require(
        record.get("schema_version") == architecture["schema_version"],
        "architecture record schema version does not match profile",
    )
    require(record.get("status") in {"proposed", "accepted"}, "unexpected architecture record status")
    require(record.get("source_refs"), "architecture record missing exact source references")
    require(record.get("nonclaims"), "architecture record missing nonclaims")
    require(record.get("components"), "architecture record has no components")
    require("seams" in record, "architecture record missing seams")

    resolved = resolved_aqr_ids(alignment)
    components = record["components"]

    for component in components:
        cid = component.get("id", "<missing>")
        for field in (
            "responsibility",
            "normative",
            "semantic_owner",
            "implementation",
            "boundary",
            "verification",
            "question_refs",
            "decision_refs",
        ):
            require(field in component, f"{cid}: missing {field}")

        normative = component["normative"]
        for field in ("direct", "inherited", "seams"):
            require(field in normative, f"{cid}: normative scope missing {field}")

        semantic_owner = component["semantic_owner"]
        require(semantic_owner.get("mode"), f"{cid}: semantic-owner mode missing")
        if semantic_owner["mode"] == "unresolved":
            require(semantic_owner.get("blocked_by"), f"{cid}: unresolved semantic owner has no blockers")

        implementation = component["implementation"]
        require(implementation.get("home"), f"{cid}: implementation home missing")
        require(implementation.get("state"), f"{cid}: implementation state missing")

        boundary = component["boundary"]
        require(boundary.get("state"), f"{cid}: boundary state missing")
        if boundary["state"] == "unresolved":
            require(boundary.get("blocked_by"), f"{cid}: unresolved boundary has no blockers")

        verification = component["verification"]
        require(verification.get("home"), f"{cid}: verification home missing")
        obligations = verification.get("obligations", [])
        require(obligations, f"{cid}: verification obligations missing")
        for obligation in obligations:
            require(obligation.get("id"), f"{cid}: verification obligation id missing")
            require(obligation.get("claim"), f"{cid}: verification claim missing")
            require(obligation.get("disproof"), f"{cid}: verification disproof missing")

        unresolved_refs = set(component.get("question_refs", []))
        unresolved_refs.update(boundary.get("blocked_by", []))
        unresolved_refs.update(semantic_owner.get("blocked_by", []))
        stale = sorted(unresolved_refs & resolved)
        require(
            not stale,
            f"{cid}: resolved bootstrap AQR reused as unresolved reference/blocker: {stale}",
        )

    return {
        "profile": profile["id"],
        "architecture_record": record["id"],
        "components": len(components),
        "seams": len(record.get("seams", [])),
        "resolved_bootstrap_aqrs_checked": len(resolved),
        "generic_transport_changed": False,
        "status": "accepted_by_bounded_profile_probe",
    }


def self_test(profile: dict, record: dict, alignment: dict) -> dict:
    mutations: dict[str, tuple[dict, dict, dict]] = {}

    x = copy.deepcopy(record)
    x["components"][0].pop("semantic_owner")
    mutations["missing_semantic_owner"] = (profile, x, alignment)

    x = copy.deepcopy(record)
    unresolved = next(
        component for component in x["components"] if component["boundary"]["state"] == "unresolved"
    )
    unresolved["boundary"].pop("blocked_by")
    mutations["unresolved_without_blocker"] = (profile, x, alignment)

    x = copy.deepcopy(record)
    x["components"][0]["verification"]["obligations"][0].pop("disproof")
    mutations["missing_disproof"] = (profile, x, alignment)

    x = copy.deepcopy(record)
    x["nonclaims"] = []
    mutations["missing_nonclaims"] = (profile, x, alignment)

    resolved = sorted(resolved_aqr_ids(alignment))
    require(resolved, "self-test requires at least one resolved bootstrap AQR")
    x = copy.deepcopy(record)
    x["components"][0]["question_refs"] = [resolved[0]]
    mutations["resolved_aqr_reused_as_open_question"] = (profile, x, alignment)

    bad_profile = copy.deepcopy(profile)
    bad_profile["transport"]["change_required"] = True
    mutations["unjustified_generic_handoff_change"] = (bad_profile, record, alignment)

    results = {}
    for name, (candidate_profile, candidate_record, candidate_alignment) in mutations.items():
        try:
            validate(candidate_profile, candidate_record, candidate_alignment)
        except ValidationError as error:
            results[name] = {"rejected": True, "reason": str(error)}
        else:
            results[name] = {"rejected": False, "reason": "unexpectedly accepted"}

    if not all(item["rejected"] for item in results.values()):
        raise ValidationError(f"negative control failed: {results}")
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", type=Path)
    parser.add_argument("record", type=Path)
    parser.add_argument("--alignment", required=True, type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    profile = load(args.profile)
    record = load(args.record)
    alignment = load(args.alignment)

    result = validate(profile, record, alignment)
    if args.self_test:
        result["negative_controls"] = self_test(profile, record, alignment)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Profiles cannot widen authority; failed proposals cannot leave the denominator."""
import importlib.util
from pathlib import Path
import sys

import pytest
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("agent_router", ROOT / "scripts/rules/agent_router.py")
router = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = router
SPEC.loader.exec_module(router)


def profile(**changes):
    values = dict(profile_id="workspace", daily_cap_usd=1, total_cap_usd=30,
                  allowed_rule_ids=["floor", "ui"], required_rule_ids=["floor"],
                  specialist_aliases={"investigate": "development-investigator"},
                  native_field_maps={"codex": {"subagent": "agent_type"}}, provider_route="openrouter")
    values.update(changes)
    return router.AgentRouterProfileV1(**values)


def resolve(selected, tmp_path):
    return router.resolve_profile(
        selected, router.NativeCapabilities(client="codex", version="fixture-version",
                    roles=["development-investigator"], field_map={"subagent": "agent_type"}, evidence_ref="fixture"),
        registry_ids={"floor", "ui"}, mandatory_rule_ids={"floor"},
        authority_limits=router.BudgetLimits(daily_cap_usd=0.5, total_cap_usd=5),
        authorized_provider_routes={"openrouter"},
        environment={"WORKSPACE_ROOT": str(tmp_path), "AGENT_ROUTER_OUT": str(tmp_path / "logs")},
    )


def test_profiles_narrow_caps_and_resolve_portable_roots(tmp_path):
    first = resolve(profile(), tmp_path)
    other = resolve(profile(profile_id="colleague", daily_cap_usd=0.1, total_cap_usd=1,
                            allowed_rule_ids=["floor"], specialist_aliases={"audit": "development-investigator"}), tmp_path)
    assert first.budgets.model_dump() == {"daily_cap_usd": 0.5, "total_cap_usd": 5.0}
    assert other.budgets.model_dump() == {"daily_cap_usd": 0.1, "total_cap_usd": 1.0}
    assert first.specialist_aliases == {"investigate": "development-investigator"}
    assert other.specialist_aliases == {"audit": "development-investigator"}
    assert first.workspace_root == str(tmp_path)
    assert other.profile_digest != first.profile_digest
    assert first.mode == "manual"
    assert other.allowed_rule_ids == ["floor"]


@pytest.mark.parametrize("changes,message", [
    ({"allowed_rule_ids": ["ui"]}, "required rule"),
    ({"allowed_rule_ids": ["floor", "unknown"]}, "unknown rule"),
    ({"specialist_aliases": {"investigate": "imaginary-role"}}, "unsupported native role"),
    ({"allowed_models": ["invented-model"]}, "unsupported native model"),
    ({"allowed_efforts": ["maximum"]}, "unsupported native effort"),
    ({"native_field_maps": {"codex": {"subagent": "invented_field"}}}, "unsupported native field"),
    ({"native_field_maps": {"codex": {"subagent": "agent_type", "model": "agent_type"}}}, "unsupported native field"),
    ({"provider_route": "unauthorized-provider"}, "cannot authorize"),
])
def test_profile_rejects_unsupported_or_widened_authority(changes, message, tmp_path):
    with pytest.raises(ValueError, match=message):
        resolve(profile(**changes), tmp_path)


@pytest.mark.parametrize("value", [-1, float("inf"), float("nan")])
def test_budget_does_not_accept_nonfinite_or_negative_limits(value):
    with pytest.raises(ValidationError):
        profile(daily_cap_usd=value)


def record(id, status="unsupported", **changes):
    values = dict(handoff_id=id, input_digest="a" * 64, profile_digest="b" * 64,
                  parent_session_id="parent", full_trace_ref="trace", proposal_status=status,
                  failure_reason="native field unavailable")
    values.update(changes)
    return router.HandoffRecordV1(**values)


def test_all_failure_categories_remain_in_the_same_eligible_membership():
    ids = ["invalid", "capped", "call_failed", "input_unavailable", "unsupported"]
    records = [record(id, id) for id in ids]
    result = router.account_handoffs(ids, records)
    assert result["eligible_ids"] == ids
    assert result["accounting_complete"] is True
    assert result["proposal_status_counts"] == {"valid": 0, **dict.fromkeys(ids, 1)}
    assert result["missing_outcome_ids"] == sorted(ids)


def test_missing_duplicate_and_unexpected_ids_cannot_look_complete():
    result = router.account_handoffs(["kept", "dropped"], [record("kept"), record("kept"), record("extra")])
    assert result["accounting_complete"] is False
    assert result["missing_ids"] == ["dropped"]
    assert result["duplicate_ids"] == ["kept"]
    assert result["unexpected_ids"] == ["extra"]
    assert result["eligible_total"] == 2


def test_missing_cost_and_inconclusive_outcome_are_visible():
    rec = record("real-job", "call_failed", llm_attempted=True,
                 outcome=router.IndependentOutcome(status="inconclusive", check_id="check", check_output_ref="output"))
    result = router.account_handoffs(["real-job"], [rec])
    assert result["unknown_cost_ids"] == ["real-job"]
    assert result["outcome_status_counts"] == {"inconclusive": 1}
    assert result["missing_outcome_ids"] == []


def test_validity_requires_the_actual_proposal():
    with pytest.raises(ValidationError, match="actual structured proposal"):
        record("job", "valid")


def test_eligible_duplicates_are_rejected():
    with pytest.raises(ValueError, match="eligible handoff IDs contain duplicates"):
        router.account_handoffs(["job", "job"], [])


def test_missing_input_and_profile_are_recorded_without_fabricated_digests():
    rec = record("job", "input_unavailable", input_digest=None, profile_digest=None)
    assert rec.input_digest is None
    assert router.account_handoffs(["job"], [rec])["proposal_status_counts"]["input_unavailable"] == 1


def test_call_provenance_cannot_disappear_from_cost_accounting():
    with pytest.raises(ValidationError, match="not attempted"):
        record("job", llm_call_id="actual-call", llm_attempted=False)


def test_missing_native_execution_cost_remains_unknown():
    rec = record("job", actual_choice=router.ActualChoice(subagent="development-investigator",
                 native_dispatch_ref="native-trace", choice_source="incumbent"))
    assert router.account_handoffs(["job"], [rec])["unknown_cost_ids"] == ["job"]

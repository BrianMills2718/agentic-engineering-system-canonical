"""The legacy sort's evidence check rejects answers its quote or the file facts do not support."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _module():
    spec = importlib.util.spec_from_file_location("sort_legacy", ROOT / "scripts" / "rules" / "sort_legacy.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["sort_legacy"] = module  # pydantic resolves the model's annotations through the module
    spec.loader.exec_module(module)
    return module


SOURCES = {
    "source_doc": "Classify by shape (public/stateless vs private/stateful) before comparing platforms.",
    "instructions": "Never infer prose meaning with regex; use an approved light LLM.",
    "register": "commit-tags: Every commit's first line starts with one tag.",
    "aes_ids": {"commit-tags"},
}
FACTS_PRESENT = {"source_docs": {"docs/a.md": True}, "linked_scripts": {"scripts/x.py": True}, "first_source": "docs/a.md"}
FACTS_GONE = {"source_docs": {"docs/a.md": False}, "linked_scripts": {"scripts/x.py": False}, "first_source": None}


def _answer(m, **kw):
    base = {"disposition": "keep", "covered_by": None, "retire_kind": None, "quote": "", "quote_from": "none",
            "reason": "r", "rule": "r", "applies_kind": "intent", "applies_value": "v"}
    return m.Disposition(**{**base, **kw})


def test_a_verbatim_quote_passes_and_a_paraphrase_fails() -> None:
    m = _module()
    good = _answer(m, quote="Classify by shape (public/stateless vs private/stateful)", quote_from="source_doc")
    assert m.check(good, {}, FACTS_PRESENT, SOURCES) is None
    paraphrase = _answer(m, quote="classify projects by their shape before choosing a host", quote_from="source_doc")
    assert "not found verbatim" in m.check(paraphrase, {}, FACTS_PRESENT, SOURCES)


def test_covered_must_name_a_real_rule_and_quote_it() -> None:
    m = _module()
    ok = _answer(m, disposition="covered", covered_by="workspace-instructions",
                 quote="Never infer prose meaning with regex", quote_from="workspace_instructions")
    assert m.check(ok, {}, FACTS_PRESENT, SOURCES) is None
    invented = _answer(m, disposition="covered", covered_by="no-such-rule",
                       quote="Never infer prose meaning with regex", quote_from="workspace_instructions")
    assert "neither an AES register id" in m.check(invented, {}, FACTS_PRESENT, SOURCES)


def test_retire_for_missing_files_must_agree_with_the_file_facts() -> None:
    m = _module()
    gone = _answer(m, disposition="retire", retire_kind="source_missing")
    assert m.check(gone, {}, FACTS_GONE, SOURCES) is None
    assert "a source document exists" in m.check(gone, {}, FACTS_PRESENT, SOURCES)
    tool = _answer(m, disposition="retire", retire_kind="tool_missing")
    assert "no linked script is missing" in m.check(tool, {}, FACTS_PRESENT, SOURCES)
    assert "no source documents were declared" in m.check(gone, {}, {**FACTS_GONE, "source_docs": {}}, SOURCES)


def test_a_quote_from_a_different_target_cannot_claim_coverage() -> None:
    m = _module()
    sources = {**SOURCES, "aes_ids": {"one", "two"}, "aes_targets": {
        "one": "Keep all private records behind authentication.",
        "two": "Every commit's first line starts with one tag."}}
    answer = _answer(m, disposition="covered", covered_by="one", quote_from="aes_register",
                     quote="Every commit's first line starts with one tag.")
    assert "not found verbatim" in m.check(answer, {}, FACTS_PRESENT, sources)
    answer.covered_by = "two"
    assert m.check(answer, {}, FACTS_PRESENT, sources) is None


def test_a_named_document_and_nonempty_applicability_are_required() -> None:
    m = _module()
    sources = {**SOURCES, "source_docs": {"a.md": SOURCES["source_doc"], "b.md": "Different source text."}}
    answer = _answer(m, quote=SOURCES["source_doc"], quote_from="source_doc", quote_source="b.md")
    assert "not found verbatim" in m.check(answer, {}, FACTS_PRESENT, sources)
    answer.quote_source = "a.md"
    assert m.check(answer, {}, FACTS_PRESENT, sources) is None
    answer.applies_value = "  "
    assert "nonempty" in m.check(answer, {}, FACTS_PRESENT, sources)


def _inventory(tmp_path: Path):
    """Use real files and the public apply/check boundary; never call a provider."""
    m = _module()
    m.PROJECT_META = tmp_path / "project-meta"
    m.PROJECT_META.mkdir()
    m.LEGACY = m.PROJECT_META / "registry.yaml"
    m.REGISTER = tmp_path / "register.yaml"
    m.DISPOSITIONS = tmp_path / "dispositions.yaml"
    m.OUT = tmp_path / "private"
    m.INSTRUCTIONS = tmp_path / "instructions.md"
    m.INSTRUCTIONS.write_text("Never publish credentials or private records.")
    doc = m.PROJECT_META / "source.md"
    doc.write_text("Preserve every validation clause and fail when any clause is missing.")
    rule = {"id": "old-a", "policy": doc.read_text() + " Record each failure's evidence.",
            "source_docs": ["source.md"], "linked_scripts": ["helper.py"], "scope": "validating artifacts",
            "enforcement_status": "advisory", "enforcement_mechanism": "prose"}
    (m.PROJECT_META / "helper.py").write_text('"""A real existing helper fixture."""\n')
    m.LEGACY.write_text(yaml.safe_dump({"policies": [rule]}))
    m.REGISTER.write_text(yaml.safe_dump({"schema_version": "aes-rules-register/v1", "rules": []}))
    f, _ = m.source_context(rule, [], m.INSTRUCTIONS.read_text())
    row = {"id": rule["id"], "status": "sorted", "facts": f,
           **_answer(m, quote=doc.read_text(), quote_from="source_doc", rule="An incomplete model rewrite.").model_dump(),
           "attempts": [{"model": "historical", "cost": 0.01}]}
    cache = tmp_path / "cache.jsonl"
    cache.write_text(json.dumps(row) + "\n")
    return m, rule, row, cache, doc


def test_apply_preserves_complete_policy_and_check_rejects_changed_inputs(tmp_path: Path) -> None:
    m, rule, _, cache, doc = _inventory(tmp_path)
    raw = cache.read_bytes()
    assert m.apply(cache) == 0
    kept = yaml.safe_load((m.OUT / "legacy-register.private.yaml").read_text())["rules"][0]
    assert kept["rule"] == rule["policy"]  # the second clause must survive migration
    assert yaml.safe_load(m.REGISTER.read_text())["rules"] == []
    assert rule["policy"] not in m.DISPOSITIONS.read_text()
    assert m.apply(cache, check_only=True) == 0
    doc.write_text(doc.read_text() + "\nAn additional current source clause.")
    assert m.apply(cache, check_only=True) == 1
    assert cache.read_bytes() == raw  # immutable provider history


def test_equal_counts_with_different_source_membership_fail_without_writes(tmp_path: Path) -> None:
    m, _, row, cache, _ = _inventory(tmp_path)
    row["id"] = "other-id"
    cache.write_text(json.dumps(row) + "\n")
    original = m.REGISTER.read_bytes()
    assert m.apply(cache) == 1
    assert m.REGISTER.read_bytes() == original
    assert not m.DISPOSITIONS.exists()


def test_existing_tool_invalidates_missing_tool_retirement_and_preserves_unknown_cost(tmp_path: Path) -> None:
    m, rule, row, cache, _ = _inventory(tmp_path)
    row.update(disposition="retire", retire_kind="tool_missing", quote="", quote_from="none")
    row["facts"]["linked_scripts"]["helper.py"] = False
    row["attempts"] = [{"model": "historical", "failed": "network failure"}]
    cache.write_text(json.dumps(row) + "\n")
    assert m.apply(cache) == 0
    output = yaml.safe_load((m.OUT / "legacy-dispositions.private.yaml").read_text())
    assert output["rules"][0]["disposition"] == "keep"
    assert output["rules"][0]["quote"] == rule["policy"]
    assert output["historical_accounting"] == {"attempts": 1, "known_cost_usd": 0,
                                                "unknown_cost_attempts": 1, "complete_cost": False}


def test_input_digest_tracks_all_sources_but_not_migration_output(tmp_path: Path) -> None:
    m, rule, _, _, doc = _inventory(tmp_path)
    extra = m.PROJECT_META / "second.md"
    extra.write_text("An independently owned policy source.")
    rule["source_docs"].append("second.md")
    def digest():
        f, sources = m.source_context(rule, [], m.INSTRUCTIONS.read_text())
        return m.input_digest(rule, f, sources)
    first = digest()
    extra.write_text(extra.read_text() + " A changed requirement.")
    assert digest() != first
    first = digest()
    m.INSTRUCTIONS.write_text(m.INSTRUCTIONS.read_text() + " Do not remove mandatory rules.")
    assert digest() != first
    assert doc.is_file()


def test_duplicate_source_ids_and_blank_model_tags_cannot_hide(tmp_path: Path) -> None:
    m, rule, row, cache, _ = _inventory(tmp_path)
    m.LEGACY.write_text(yaml.safe_dump({"policies": [rule, rule]}))
    assert m.apply(cache) == 1
    m.LEGACY.write_text(yaml.safe_dump({"policies": [rule]}))
    row["applies_value"] = ""
    cache.write_text(json.dumps(row) + "\n")
    assert m.apply(cache) == 0
    tag = yaml.safe_load((m.OUT / "legacy-register.private.yaml").read_text())["rules"][0]["applies_when"]
    assert tag["kind"] == "intent" and tag["value"] == rule["scope"]


def test_private_prose_cannot_escape_through_public_projection(tmp_path: Path) -> None:
    import hashlib
    m, rule, row, cache, doc = _inventory(tmp_path)
    secret = "Synthetic private customer Bluebird has an unreleased deployment."
    rule["policy"] = secret
    rule["enforcement_mechanism"] = secret
    doc.write_text(secret)
    m.LEGACY.write_text(yaml.safe_dump({"policies": [rule]}))
    row.update(quote=secret, reason=secret, rule=secret, applies_value=secret)
    row["facts"], _ = m.source_context(rule, [], m.INSTRUCTIONS.read_text())
    cache.write_text(json.dumps(row) + "\n")
    raw = cache.read_bytes()
    assert m.apply(cache) == 0
    public = yaml.safe_load(m.DISPOSITIONS.read_text())
    private = (m.OUT / "legacy-dispositions.private.yaml").read_bytes()
    assert secret not in m.DISPOSITIONS.read_text() + m.REGISTER.read_text()
    assert public["rules"][0]["id"] == rule["id"]
    assert public["rules"][0]["quote_sha256"] == hashlib.sha256(secret.encode()).hexdigest()
    assert public["private_dispositions_sha256"] == hashlib.sha256(private).hexdigest()
    assert secret in private.decode()
    assert (m.OUT / "legacy-register.private.yaml").stat().st_mode & 0o777 == 0o600
    assert m.apply(cache, check_only=True) == 0
    assert cache.read_bytes() == raw


def test_private_output_inside_public_checkout_fails_before_writes(tmp_path: Path) -> None:
    import pytest
    m, _, _, cache, _ = _inventory(tmp_path)
    m.OUT = m.ROOT / "docs"
    original = m.REGISTER.read_bytes()
    with pytest.raises(ValueError, match="outside the public repository"):
        m.apply(cache)
    assert m.REGISTER.read_bytes() == original
    assert not m.DISPOSITIONS.exists()


def test_private_output_cannot_enter_another_git_checkout(tmp_path: Path) -> None:
    import pytest
    m, _, _, cache, _ = _inventory(tmp_path)
    other = tmp_path / "other-checkout"
    (other / ".git").mkdir(parents=True)
    (other / ".git" / "HEAD").write_text("ref: refs/heads/main\n")
    m.OUT = other / "private"
    with pytest.raises(ValueError, match="all Git checkouts"):
        m.apply(cache)
    assert not m.OUT.exists()

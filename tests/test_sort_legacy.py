"""The legacy sort's evidence check rejects answers its quote or the file facts do not support."""
from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _module():
    spec = importlib.util.spec_from_file_location("sort_legacy", ROOT / "scripts" / "rules" / "sort_legacy.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("llm_client", types.ModuleType("llm_client"))  # check() never calls the model
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
    good = _answer(m, quote="classify by shape (public/stateless vs private/stateful)", quote_from="source_doc")
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

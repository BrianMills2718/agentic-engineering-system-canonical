"""The rules page lists every register rule and the legacy register, and survives table-breaking text."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _module():
    spec = importlib.util.spec_from_file_location("build_rules_page", ROOT / "scripts" / "rules" / "build_rules_page.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _register(tmp_path: Path) -> Path:
    path = tmp_path / "register.yaml"
    path.write_text(yaml.safe_dump({"schema_version": "aes-rules-register/v1", "enforcement_statuses": {"enforced": "refused"},
                                    "rules": [
        {"id": "commit-tags", "rule": "Tag every commit | no exceptions", "origin": "workspace-instructions",
         "enforcement_status": "enforced", "enforcement_mechanism": "commit hook"},
        {"id": "loop-1", "rule": "Read exit codes", "origin": "feedback-loop", "enforcement_status": "licensed",
         "enforcement_mechanism": "handed", "evidence": {"concern": "https://github.com/o/r/issues/1", "sightings": 2}},
    ]}), encoding="utf-8")
    return path


def test_page_lists_every_rule_and_legacy_group(tmp_path: Path) -> None:
    module = _module()
    legacy = tmp_path / "registry.yaml"
    legacy.write_text(yaml.safe_dump({"policies": [
        {"id": "old-a", "policy": "A", "enforcement_status": "advisory", "enforcement_mechanism": "prose"},
        {"id": "old-b", "policy": "B", "enforcement_status": "enforced", "enforcement_mechanism": "hook"},
    ]}), encoding="utf-8")
    page = module.build(_register(tmp_path), legacy)
    for rule_id in ("commit-tags", "loop-1", "old-a", "old-b"):
        assert f"**{rule_id}**" in page
    assert "[issue #1](https://github.com/o/r/issues/1); 2 sightings" in page
    assert "<strong>advisory</strong> (1)" in page and "<strong>enforced</strong> (1)" in page
    assert "Tag every commit \\| no exceptions" in page  # a pipe in rule text cannot split the table row


def test_missing_legacy_register_is_stated_not_hidden(tmp_path: Path) -> None:
    page = _module().build(_register(tmp_path), tmp_path / "absent.yaml")
    assert "Not available when this page was built" in page
    assert "**commit-tags**" in page


def test_committed_page_matches_a_fresh_build_of_the_committed_register(tmp_path: Path) -> None:
    module = _module()
    built = module.build(module.REGISTER, tmp_path / "absent.yaml").split("## Legacy project-meta register")[0]
    committed = module.OUTPUT.read_text(encoding="utf-8").split("## Legacy project-meta register")[0]
    current_rules = built.split("| Section |")[1].split("\n\n", 1)[1]
    assert committed.split("| Section |")[1].split("\n\n", 1)[1] == current_rules

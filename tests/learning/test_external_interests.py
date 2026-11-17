"""Interests in the private profile: loaded, shown to the judge, named in the digest (fake model, no network)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "learning_loop"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import external_ideas as E  # noqa: E402
import external_judge as J  # noqa: E402

PROFILE = """projects:
  - {name: aes, goal: "agent engineering system"}
interests:
  - {name: "ontology", goal: "represent anything so meaning survives a change of form"}
"""


@pytest.mark.req("external-idea-intake/interests-listed-and-named")
def test_profile_loads_interests_and_judge_prompt_lists_them(tmp_path):
    p = tmp_path / "p.yaml"
    p.write_text(PROFILE)
    entries = E.load_profile(p)
    assert [(e["name"], e.get("kind", "project")) for e in entries] == [("aes", "project"), ("ontology", "interest")]
    prompts = []

    def call(prompt):
        prompts.append(prompt)
        return J.Verdicts(verdicts=[J.Verdict(id="a", decision="useful", projects=["ontology"], reason="adopt x")])

    judge = J.build_judge(entries, call, lambda pid, want: "")
    out = judge("sub", [{"id": "a", "title": "t", "body": "b"}])
    assert "Interests (" in prompts[0] and "meaning survives a change of form" in prompts[0]
    assert out["a"][0] == ["ontology"] and "ontology" in judge.names and judge.interests == {"ontology"}


@pytest.mark.req("external-idea-intake/interests-listed-and-named")
def test_no_interests_section_without_interests():
    prompts = []
    judge = J.build_judge([{"name": "aes", "goal": "g"}], lambda pr: (prompts.append(pr) or J.Verdicts(verdicts=[])),
                          lambda pid, want: "")
    judge("sub", [{"id": "a", "title": "t", "body": ""}])
    assert "Interests (" not in prompts[0] and judge.interests == set()


@pytest.mark.req("external-idea-intake/bad-interest-refused")
def test_interest_without_goal_is_refused(tmp_path):
    p = tmp_path / "p.yaml"
    p.write_text('projects:\n  - {name: aes, goal: "g"}\ninterests:\n  - {name: "ontology"}\n')
    with pytest.raises(E.ConfigError) as exc:
        E.load_profile(p)
    assert "ontology" in str(exc.value)


@pytest.mark.req("external-idea-intake/interests-listed-and-named")
def test_useful_digest_prints_interests_line_separately(tmp_path):
    import test_external_ideas as T  # noqa: E402 - reuse the intake test helpers (fake listing, config writer)
    out = tmp_path / "out"
    judge = lambda sub, posts: {"u2": (["ontology"], "adopt this"), "u3": (["aes", "ontology"], "both")}  # noqa: E731
    judge.interests = {"ontology"}
    judge.names = ["aes", "ontology"]
    assert E.run(T.write_cfg(tmp_path, [T.entry()]), out, fetch=T._fetch3, now=T.NOW, judge=judge) == 0
    useful = next(out.glob("digest-useful-*.md")).read_text()
    assert "Interests: ontology" in useful and "Projects: aes" in useful
    assert useful.count("Projects: (unassigned)") == 0

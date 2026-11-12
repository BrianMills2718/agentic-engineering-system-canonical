"""The whole example, end to end: every step's expected exit and key output."""

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent


def test_end_to_end(tmp_path):
    out = tmp_path / "run.json"
    proc = subprocess.run([sys.executable, str(REPO / "e2e" / "run.py"), "--out", str(out)],
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    steps = json.loads(out.read_text())["steps"]
    text = {s["n"]: "\n".join(c["output"] for c in s["commands"]) for s in steps}
    assert '"deny"' in text[4] and "not in the plan" in text[4]          # unplanned file refused at the edit
    assert '"allow"' in text[5] and "NI-001" in text[5]                  # plan text handed to the agent
    assert "Disproved if" in steps[5]["files"][0]["text"]                # projected into the docstring
    assert "SC-001: SUPPORTED" in text[7]
    assert "STALE" in text[9]                                            # old evidence stale after the change
    assert "Check failed" in text[10]                                    # docstring out of date detected
    assert '"deny"' in text[11] and "out of date" in text[11]            # edit blocked while stale
    assert "sorted by" in text[12]                                       # new requirement handed over
    assert "1 failed" in text[13]                                        # new test catches old code
    assert "SC-001" in text[14] and "sorted by" in text[14]              # back in step; wiki shows new text


def test_smallest_example(tmp_path):
    out = tmp_path / "simple.json"     # never overwrite the committed walkthrough data from a test
    proc = subprocess.run([sys.executable, str(REPO / "e2e" / "simple.py"), "--out", str(out)], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    steps = json.loads(out.read_text())["steps"]
    assert [s["n"] for s in steps] == [1, 2, 3, 4, 5, 6, 7]
    assert "NI-001" in steps[1]["code"] and "Hello, <name>!" in steps[1]["code"]       # plan copied into docstring
    assert "SUPPORTED" in steps[2]["wiki"]                                                 # wiki shows the test result
    assert steps[3]["agent"]["decision"] == "allow" and "NI-001" in steps[3]["agent"]["text"]
    assert "empty name" in steps[4]["plan"]["yaml"] and "empty name" not in steps[4]["code"]       # plan changed, docstring stale
    assert steps[5]["agent"]["decision"] == "deny"                                         # agent stopped
    assert "empty name" in steps[6]["code"] and "raise ValueError" in steps[6]["code"]     # back in step
    assert "empty" in steps[6]["wiki"] and "SUPPORTED" in steps[6]["wiki"]


def test_wiki_sections_are_questions_and_files_are_links(proj):
    """Behavior 6.1 (Q20): the front page asks the reader's questions; each component page links its files and its test."""
    from lockstep.wiki import pages

    from lockstep_support import sh
    built = pages(proj, "greeter")
    front = built["index.md"]
    heads = [line for line in front.splitlines() if line.startswith("## ")]
    assert heads and all(h.endswith("?") for h in heads), heads
    assert "](components/CMP-GREETER.md)" in front and "](requirements/" in front
    comp = built["components/CMP-GREETER.md"]
    on_disk = (proj / "src/greeter/__init__.py").resolve().as_uri()  # no remote: the file on disk
    assert f"[src/greeter/__init__.py]({on_disk})" in comp
    assert "- Proven by: [tests/test_greet.py](" in comp and "[.aes/target.yaml](" in comp
    sh("git remote add origin git@github.com:someone/greeter.git", proj)  # a GitHub remote: the hosted copy at this commit
    head = sh("git rev-parse HEAD", proj).strip()
    comp = pages(proj, "greeter")["components/CMP-GREETER.md"]
    assert f"[src/greeter/__init__.py](https://github.com/someone/greeter/blob/{head}/src/greeter/__init__.py)" in comp

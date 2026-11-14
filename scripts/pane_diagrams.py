"""Turn the views of a LikeC4 model into pane-sized text diagrams (boxes and arrows).

Reads `likec4 export json` output (box titles, descriptions, arrow labels), writes one D2 file per view, renders it
with `d2` to text, and refuses a diagram that does not fit: wider than --max-width, or any box title, description line
or arrow label that does not appear whole in the output (the text renderer overlaps boxes and cuts labels when a
row is too wide).

Pipeline (run from the repository root):
    npx --yes likec4@1.60.0 export json -o /tmp/aes-model.json docs/architecture
    python3 scripts/pane_diagrams.py /tmp/aes-model.json docs/architecture/pane
The model is docs/architecture/aes.c4 (LikeC4); the output `.txt` files are generated, so change the model and rerun,
not the text. Each box shows its title and description, each arrow its label, so the wording lives in the model.

Usage: pane_diagrams.py MODEL_JSON OUT_DIR [--max-width 72] [--wrap 30]
Exit 0 all views written and fit, 1 a view did not fit (named), 2 bad input.
"""
import argparse
import json
import re
import subprocess
import sys
import textwrap
from pathlib import Path


def build(view: dict, wrap: int) -> tuple[str, list[str]]:
    lines, must = ["direction: down"], []
    ids = {}
    for n in view["nodes"]:
        title = n["title"]
        desc = ((n.get("description") or {}).get("txt") or "").strip()
        wrapped = textwrap.wrap(desc, wrap) if desc else []
        nid = "n" + re.sub(r"\W", "_", n["id"])
        ids[n["id"]] = nid
        label = "\\n".join([title, *wrapped])
        lines.append(f'{nid}: "{label}"')
        must += [title, *wrapped]
    for e in view["edges"]:
        label = (e.get("label") or "").strip()
        lines.append(f'{ids[e["source"]]} -> {ids[e["target"]]}' + (f': "{label}"' if label else ""))
        if label:
            must.append(label)
    return "\n".join(lines) + "\n", must


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("model_json", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--max-width", type=int, default=72)
    ap.add_argument("--wrap", type=int, default=30)
    a = ap.parse_args()
    try:
        views = json.loads(a.model_json.read_text())["views"]
    except (OSError, ValueError, KeyError) as exc:
        print(f"cannot read {a.model_json}: {exc}", file=sys.stderr)
        return 2
    a.out_dir.mkdir(parents=True, exist_ok=True)
    bad = 0
    for name, view in views.items():
        if not view.get("nodes") or not view.get("edges") or name == "index":
            continue
        d2, must = build(view, a.wrap)
        src, txt = a.out_dir / f"{name}.d2", a.out_dir / f"{name}.txt"
        src.write_text(d2)
        r = subprocess.run(["d2", str(src), str(txt)], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"FAIL {name}: d2 exited {r.returncode}: {r.stderr.strip()[:200]}")
            bad += 1
            continue
        rows = [x.rstrip() for x in txt.read_text().splitlines()]
        txt.write_text("\n".join(rows).rstrip() + "\n")
        flat = "\n".join(rows)
        width = max(len(x) for x in rows)
        missing = [m for m in must if m not in flat]
        problems = ([f"width {width} > {a.max_width}"] if width > a.max_width else []) + [f"label cut or overlapped: {m!r}" for m in missing]
        print(f"{'ok  ' if not problems else 'FAIL'} {name}: width {width}, {len(rows)} rows" + ("; " + "; ".join(problems) if problems else ""))
        bad += bool(problems)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

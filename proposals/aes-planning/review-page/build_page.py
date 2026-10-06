"""Build aes-planning-plan.html from the adopted plan ../README.md (kept in step by hand).

Run: python3 build_page.py
"""
from html import escape
from pathlib import Path

# id, x, y, w, h, kind, title, sub, unit
NODES = [
    ("work", 20, 260, 190, 86, "k-src", "Work arrives", "an agent is about to change something", ""),
    ("facts", 250, 260, 200, 86, "k-step", "Facts, not a label", "14 yes/no facts → route (code decides)", "exists"),
    ("triv", 500, 40, 250, 86, "k-step", "Trivial lane: [Trivial]", "≤3 files, ≤60 lines, no running-thing file", "P4"),
    ("emer", 500, 145, 250, 86, "k-step", "Emergency: [Unplanned]", "needs Emergency: trailer; logged; fyi to you", "P4"),
    ("cp", 500, 260, 250, 86, "k-step", "Company Planning plan", "+ AES overlay: running things declared, 2–4 UI review points", "P1"),
    ("adopt", 500, 390, 250, 86, "k-gate", "Adoption gate (adopt)", "checklist + evidence + AI check → receipt", "exists"),
    ("goal", 800, 390, 200, 86, "k-step", "/goal text written", "from the plan's own fields", "P2"),
    ("accept", 800, 260, 200, 86, "k-gate", "aes plan accept", "refuses without a fresh adopted receipt", "P3"),
    ("commit", 1040, 145, 200, 86, "k-gate", "Commit hook", "[Plan #N] must find the receipt; [Trivial] measured", "P4"),
    ("land", 1040, 290, 200, 86, "k-src", "Work lands", "observe week, then enforce per repo", "P6"),
]
EDGES = [("work", "facts"), ("facts", "triv"), ("facts", "emer"), ("facts", "cp"), ("cp", "adopt"), ("adopt", "goal"),
         ("adopt", "accept"), ("accept", "commit"), ("triv", "commit"), ("emer", "commit"), ("commit", "land")]
UNIT_STATE = {"exists": ("✓ exists", "done"), "P1": ("P1 · planned", "todo"), "P2": ("P2 · planned", "todo"),
              "P3": ("P3 · planned", "todo"), "P4": ("P4 · planned", "todo"), "P6": ("P6 · planned", "todo")}


def wrap(text, w):
    limit = int((w - 20) / 6.4)
    lines, cur = [], ""
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > limit:
            lines.append(cur); cur = word
        else:
            cur = (cur + " " + word).strip()
    return (lines + [cur])[:2]


def center(n):
    _, x, y, w, h, *_ = n
    return x + w / 2, y + h / 2


def anchor(a, b):
    ax, ay = center(a); bx, by = center(b)
    _, x, y, w, h, *_ = a
    _, x2, y2, w2, h2, *_ = b
    if abs(bx - ax) > abs(by - ay) * 1.2:
        return (x + w if bx > ax else x, ay), (x2 if bx > ax else x2 + w2, by)
    return (ax, y + h if by > ay else y), (bx, y2 if by > ay else y2 + h2)


def svg() -> str:
    idx = {n[0]: n for n in NODES}
    out = ['<svg class="wide" viewBox="0 0 1260 500" role="img" aria-label="Work arrives, facts decide the route: trivial, emergency, or a Company Planning plan that goes through the adoption gate, writes the goal text and is accepted by AES; the commit hook checks every lane before work lands.">',
           '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="ahp"/></marker></defs>']
    for a, b in EDGES:
        (x1, y1), (x2, y2) = anchor(idx[a], idx[b])
        out.append(f'<path d="M{x1},{y1} L{x2},{y2}" class="arrow" marker-end="url(#ah)"/>')
    for nid, x, y, w, h, kind, title, sub, unit in NODES:
        label, st = UNIT_STATE.get(unit, ("", ""))
        out.append(f'<g class="{kind} st-{st}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>'
                   f'<text x="{x+10}" y="{y+22}" class="t-title">{escape(title)}</text>'
                   + "".join(f'<text x="{x+10}" y="{y+40+14*i}" class="t-prov">{escape(line)}</text>' for i, line in enumerate(wrap(sub, w)))
                   + (f'<text x="{x+10}" y="{y+76}" class="t-state">{escape(label)}</text>' if label else "") + "</g>")
    out.append('<g class="callout"><rect x="20" y="40" width="440" height="150" rx="6"/>'
               '<text x="32" y="64" class="t-title">The case that started this (10-06)</text>'
               '<text x="32" y="86" class="t-prov">"[Unplanned] Paperclip: add make, uv and PyYAML"</text>'
               '<text x="32" y="104" class="t-prov">new Dockerfile + compose change, then a live deploy.</text>'
               '<text x="32" y="122" class="t-prov">Today: accepted everywhere. After P4: refused,</text>'
               '<text x="32" y="140" class="t-prov">it touches running-thing files and has no plan.</text>'
               '<text x="32" y="166" class="t-prov">81 of AES canonical\'s last 300 commits were [Unplanned].</text></g>')
    out.append("</svg>")
    return "\n".join(out)


def narrow() -> str:
    steps = [
        ("1. Facts decide the route", "An agent records 14 yes/no facts; code picks the route. Labels don't."),
        ("2a. Trivial: [Trivial]", "Allowed only if the change is ≤3 files, ≤60 lines and touches no running-thing file (P4)."),
        ("2b. Emergency: [Unplanned]", "Needs an Emergency: line; logged; you get an fyi the same day (P4)."),
        ("2c. Real work: a plan", "Company Planning plan with the AES overlay: running things declared, 2–4 working-UI review points (P1)."),
        ("3. Adoption gate", "Checklist + evidence + AI check → receipt. Already exists; it refused this plan three times before adopting it."),
        ("4. /goal text written", "From the plan's own fields (P2). This plan's goal was written by hand as the prototype."),
        ("5. aes plan accept", "Refuses without a fresh adopted receipt (P3)."),
        ("6. Commit hook", "[Plan #N] must find the receipt; [Trivial] is measured from the diff (P4)."),
        ("7. Rollout", "Observe for a week, then enforce, one repository at a time (P6)."),
    ]
    return '<div class="narrow">' + "".join(f'<section class="card"><h2>{escape(t)}</h2><p>{escape(b)}</p></section>' for t, b in steps) + "</div>"


CSS = """:root{--bg:#fff;--fg:#111827;--muted:#4b5563;--line:#9ca3af;--panel:#f3f4f6;--blue:#1d4ed8;--bluefill:#dbeafe;--orange:#b45309;--grey:#6b7280}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#0f1420;--fg:#e5e7eb;--muted:#a3adba;--line:#6b7280;--panel:#1a2030;--blue:#7fb2ff;--bluefill:#1e3a5f;--orange:#f5a524;--grey:#a3adba}}
:root[data-theme="dark"]{--bg:#0f1420;--fg:#e5e7eb;--muted:#a3adba;--line:#6b7280;--panel:#1a2030;--blue:#7fb2ff;--bluefill:#1e3a5f;--orange:#f5a524;--grey:#a3adba}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:1300px;margin:0 auto;padding:20px 16px 40px}h1{font-size:1.35rem;line-height:1.25;margin:0 0 6px}
p.q{font-size:1.05rem;margin:0 0 14px;border-left:4px solid var(--blue);padding:4px 0 4px 12px}
svg{width:100%;height:auto;display:block}svg text{fill:var(--fg);font-family:inherit}
.t-title{font-size:14px;font-weight:700}.t-state{font-size:12px;font-weight:700}.t-prov{font-size:12px;fill:var(--muted)}
.k-src rect{fill:var(--panel);stroke:var(--fg);stroke-width:1.5}.k-step rect{fill:none;stroke:var(--fg);stroke-width:1.5}
.k-gate rect{fill:none;stroke:var(--fg);stroke-width:3.5}
.st-done rect{fill:var(--bluefill);stroke:var(--blue)}.st-todo rect{stroke-dasharray:6 5}
.callout rect{fill:none;stroke:var(--orange);stroke-width:2}
.arrow{stroke:var(--line);stroke-width:1.6}.ahp{fill:var(--line)}
.wide{display:block}.narrow{display:none}@media (max-width:760px){.wide{display:none}.narrow{display:block}h1{font-size:1.15rem}}
.card{border:1px solid var(--line);border-radius:6px;padding:10px 12px;margin:10px 0}.card h2{font-size:1rem;margin:0 0 4px}.card p{margin:0}
ul.legend{list-style:none;padding:0;margin:16px 0 8px;display:flex;flex-wrap:wrap;gap:8px 18px;font-size:.9rem}
ul.legend span{display:inline-block;width:26px;height:14px;vertical-align:-2px;margin-right:6px;border-radius:3px}
.l-done{background:var(--bluefill);border:2px solid var(--blue)}.l-todo{border:2px dashed var(--fg)}.l-gate{border:3.5px solid var(--fg)}.l-case{border:2px solid var(--orange)}
footer{margin-top:14px;font-size:.8rem;color:var(--muted)}footer code{font-size:.78rem;overflow-wrap:anywhere}"""


def main() -> None:
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AES planning plan</title><style>{CSS}</style></head><body><main>
<h1>AES planning: facts decide whether work needs a plan; real work needs an adopted plan, which writes its /goal; the commit hook checks every lane.</h1>
<p class="q">Is this the flow you want every project on? Reply in the terminal. (Adopted by Company Planning's gate on its fourth run; nothing is enforced yet.)</p>
{svg()}
{narrow()}
<ul class="legend"><li><span class="l-done"></span>Already exists</li><li><span class="l-todo"></span>Planned (work unit)</li><li><span class="l-gate"></span>A check that can refuse</li><li><span class="l-case"></span>The escape it closes</li></ul>
<footer>Source: <code>proposals/aes-planning/README.md</code> (adopted; receipt <code>method-conformance-receipt.json</code>) and goal <code>aes-planning.goal.md</code> on branch <code>shaping/aes-planning</code> of BrianMills2718/agentic-engineering-system-canonical. Generated by <code>review-page/build_page.py</code>.</footer>
</main></body></html>"""
    Path(__file__).with_name("aes-planning-plan.html").write_text(html)


if __name__ == "__main__":
    main()

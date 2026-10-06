"""Build hive-hardening-plan.html from the plan in ../README.md (hand-kept in step).

Run: python3 build_page.py  (writes hive-hardening-plan.html beside this file)
"""
from html import escape
from pathlib import Path

FAILURES = [
    ("F1", "An agent answered for you", "said \"compact now\" on your phone thread, 06:02 UTC"),
    ("F2", "Workers stuck a day, no one told", "both slots blocked; Coordinator says \"succeeded\""),
    ("F3", "Silence check crashed, hid it", "dashboard got yesterday's all-clear"),
    ("F4", "Jobs mostly upkeep of itself", "installs, READMEs; AES frontier idle since 09-27"),
    ("F5", "AES status always red", "1 of 9 criteria supported; 32 of 37 stale"),
]
GAPS = [
    ("G1", "AES declared only files in 2 folders", "running things had no plan, so no check"),
    ("G2", "Criteria only say what should work", "never what must not happen; tests use clean inputs"),
    ("G3", "AES checks at commit time", "these broke at run time"),
    ("G4", "Always-red status gets skipped", "nothing re-records stale evidence"),
    ("G5", "Success counted activity", "v1 conditions count jobs merged, not value"),
]
# id, title, detail, state (done|next|todo|you), causes it fixes
UNITS = [
    ("U0", "Checks survive damaged logs", "crash fails service · PR #151", "done", ["F3"]),
    ("U1", "Only you can answer your questions", "rule applied to agents; relay check next", "run", ["F1"]),
    ("U2", "Unstick workers + stall alert", "tools installed; alert after 12 h next", "run", ["F2"]),
    ("U3", "Every running thing is a file in git", "compose, linked units, rule files, containers", "run", ["G1"]),
    ("U4", "AES checks running = files", "new kinds; drift check; default in scope", "todo", ["G1"]),
    ("U5", "AES asks what must never happen", "STPA list; failure-input tests", "todo", ["G2"]),
    ("U6", "One trace per run, end to end", "OpenTelemetry; viewer with filters", "todo", ["G3"]),
    ("U7", "Rules checked against traces", "results into aes status; heartbeats", "todo", ["G3", "G4"]),
    ("U8", "Jobs aim at your outcomes", "DIGIMON #215 + process tracing", "done", ["G5"]),
    ("U9", "One front door", "README current; services follow main", "todo", ["G4"]),
    ("U10", "Review whole traces, not outputs", "failures, your channel, sampled passes", "todo", ["G4", "G5"]),
]
F_TO_G = {"F1": ["G1", "G2"], "F2": ["G2", "G3", "G5"], "F3": ["G1", "G2"], "F4": ["G5"], "F5": ["G4"]}
STATE = {"done": "✓ Done", "run": "◐ Started", "next": "▶ Next", "todo": "○ Planned", "you": "◆ Your pick"}

W, X1, X2, X3, BW = 1200, 10, 425, 840, 350
FY, FH, FS = 70, 70, 112
UY, UH, US = 50, 54, 62


def box(x, y, w, h, cls, title, sub, tag=""):
    t = f'<text x="{x+12}" y="{y+22}" class="t-title">{escape(title)}</text>'
    s = f'<text x="{x+12}" y="{y+40}" class="t-prov">{escape(sub)}</text>'
    tg = f'<text x="{x+w-10}" y="{y+22}" class="t-state" text-anchor="end">{escape(tag)}</text>' if tag else ""
    return f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>{t}{s}{tg}</g>'


def edge(x1, y1, x2, y2, cls="arrow"):
    mx = (x1 + x2) / 2
    return f'<path d="M{x1},{y1} C{mx},{y1} {mx},{y2} {x2-6},{y2}" class="{cls}" fill="none" marker-end="url(#ah)"/>'


def svg() -> str:
    fy = {fid: FY + i * FS for i, (fid, *_) in enumerate(FAILURES)}
    gy = {gid: FY + i * FS for i, (gid, *_) in enumerate(GAPS)}
    uy = {u[0]: UY + i * US for i, u in enumerate(UNITS)}
    out = [f'<svg class="wide" viewBox="0 0 {W} 750" role="img" aria-label="Five failures on the left, each linked to the gaps in AES that let it through in the middle, each gap linked to the fix units on the right with their state.">',
           '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="ahp"/></marker></defs>',
           f'<text x="{X1}" y="30" class="lane">What went wrong (10-06)</text>',
           f'<text x="{X2}" y="30" class="lane">Why AES let it through</text>',
           f'<text x="{X3}" y="30" class="lane">Fix</text>']
    for f, gs in F_TO_G.items():
        for g in gs:
            out.append(edge(X1 + BW, fy[f] + FH / 2, X2, gy[g] + FH / 2))
    for u in UNITS:
        for c in u[4]:
            if c.startswith("G"):
                out.append(edge(X2 + BW, gy[c] + FH / 2, X3, uy[u[0]] + UH / 2))
    for fid, t, s in FAILURES:
        out.append(box(X1, fy[fid], BW, FH, "k-fail", f"{fid} · {t}", s))
    for gid, t, s in GAPS:
        out.append(box(X2, gy[gid], BW, FH, "k-gap", f"{gid} · {t}", s))
    for uid, t, s, st, causes in UNITS:
        fixes = [c for c in causes if c.startswith("F")]
        sub = STATE[st] + " · " + s + (f" · fixes {', '.join(fixes)}" if fixes else "")
        out.append(box(X3, uy[uid], BW, UH, f"k-unit st-{st}", f"{uid} · {t}", sub))
    out.append("</svg>")
    return "\n".join(out)


def narrow() -> str:
    parts = ['<div class="narrow">']
    for fid, t, s in FAILURES:
        gaps = [g for g in GAPS if g[0] in F_TO_G[fid]]
        units = [u for u in UNITS if fid in u[4] or any(g[0] in u[4] for g in gaps)]
        parts.append(f'<section class="card"><h2>{fid} · {escape(t)}</h2><p class="sub">{escape(s)}</p><p class="lbl">Why AES let it through</p><ul>')
        parts += [f"<li><b>{g[0]}</b> {escape(g[1])}: {escape(g[2])}</li>" for g in gaps]
        parts.append('</ul><p class="lbl">Fix</p><ul>')
        parts += [f'<li class="st-{u[3]}"><b>{u[0]}</b> {escape(u[1])} <span class="badge">{STATE[u[3]]}</span></li>' for u in units]
        parts.append("</ul></section>")
    parts.append("</div>")
    return "\n".join(parts)


CSS = """:root{--bg:#fff;--fg:#111827;--muted:#4b5563;--line:#9ca3af;--panel:#f3f4f6;--blue:#1d4ed8;--bluefill:#dbeafe;--orange:#b45309;--grey:#6b7280}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#0f1420;--fg:#e5e7eb;--muted:#a3adba;--line:#6b7280;--panel:#1a2030;--blue:#7fb2ff;--bluefill:#1e3a5f;--orange:#f5a524;--grey:#a3adba}}
:root[data-theme="dark"]{--bg:#0f1420;--fg:#e5e7eb;--muted:#a3adba;--line:#6b7280;--panel:#1a2030;--blue:#7fb2ff;--bluefill:#1e3a5f;--orange:#f5a524;--grey:#a3adba}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:1240px;margin:0 auto;padding:20px 16px 40px}h1{font-size:1.35rem;line-height:1.25;margin:0 0 6px}
p.q{font-size:1.05rem;margin:0 0 14px;border-left:4px solid var(--blue);padding:4px 0 4px 12px}
svg{width:100%;height:auto;display:block}svg text{fill:var(--fg);font-family:inherit}
.lane{font-size:13px;font-weight:700;fill:var(--muted);letter-spacing:.04em;text-transform:uppercase}
.t-title{font-size:14px;font-weight:700}.t-state{font-size:12px;font-weight:700}.t-prov{font-size:12px;fill:var(--muted)}
.k-fail rect{fill:var(--panel);stroke:var(--fg);stroke-width:1.5}
.k-gap rect{fill:none;stroke:var(--fg);stroke-width:3}
.st-done rect{fill:var(--bluefill);stroke:var(--blue);stroke-width:2.5}
.st-next rect{fill:none;stroke:var(--orange);stroke-width:3;stroke-dasharray:10 4 2 4}
.st-run rect{fill:none;stroke:var(--orange);stroke-width:3}
.st-todo rect{fill:none;stroke:var(--grey);stroke-width:2;stroke-dasharray:6 5}
.st-you rect{fill:none;stroke:var(--fg);stroke-width:4}
.arrow{stroke:var(--line);stroke-width:1.5}.ahp{fill:var(--line)}
.wide{display:block}.narrow{display:none}
@media (max-width:760px){.wide{display:none}.narrow{display:block}h1{font-size:1.15rem}}
.card{border:1px solid var(--line);border-radius:6px;padding:10px 12px;margin:10px 0}.card h2{font-size:1rem;margin:0}
.card .sub{margin:2px 0 6px;color:var(--muted);font-size:.9rem}.card .lbl{margin:6px 0 2px;font-weight:700;font-size:.85rem;text-transform:uppercase;color:var(--muted)}
.card ul{margin:0;padding-left:18px}.badge{font-size:.8rem;font-weight:700;white-space:nowrap}
ul.legend{list-style:none;padding:0;margin:16px 0 8px;display:flex;flex-wrap:wrap;gap:8px 18px;font-size:.9rem}
ul.legend span{display:inline-block;width:26px;height:14px;vertical-align:-2px;margin-right:6px;border-radius:3px}
.l-done{background:var(--bluefill);border:2.5px solid var(--blue)}.l-run{border:3px solid var(--orange)}.l-next{border:3px dashed var(--orange)}.l-todo{border:2px dashed var(--grey)}.l-you{border:4px solid var(--fg)}
.decide{border:2px solid var(--fg);border-radius:6px;padding:10px 14px;margin:16px 0}.decide h2{font-size:1.05rem;margin:0 0 6px}
footer{margin-top:14px;font-size:.8rem;color:var(--muted)}footer code{font-size:.78rem;overflow-wrap:anywhere}"""

DECIDE = """<section class="decide"><h2>✓ U8 decided: what the workers aim at</h2>
<p>Right now they take any agent-doable line from your weekly plan, which turned out to be mostly upkeep.
<b>Your answer, 2026-10-06:</b> "completing the digimon architecture and process tracing." Set in the weekly plan: DIGIMON Plan #215 slices and process tracing's GOAL order, upkeep at most one job in three.</p></section>"""


def main() -> None:
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Hive hardening plan</title><style>{CSS}</style></head><body><main>
<h1>Hive hardening plan: five things broke on 10-06 because AES's plan declared only files in two folders. Fix: declare the running system too, scan to prove the plan complete, record every run end to end, check the rules against what happened.</h1>
<p class="q">Does each fix close the gap it points at? Reply in the terminal.</p>
{svg()}
{narrow()}
<ul class="legend"><li><span class="l-done"></span>Done</li><li><span class="l-run"></span>Started</li><li><span class="l-next"></span>Next</li><li><span class="l-todo"></span>Planned</li></ul>
{DECIDE}
<footer>Source: <code>proposals/hive-hardening/README.md</code> on branch <code>shaping/hive-hardening</code> of BrianMills2718/agentic-engineering-system-canonical (evidence for every row there). Generated by <code>review-page/build_page.py</code>.</footer>
</main></body></html>"""
    Path(__file__).with_name("hive-hardening-plan.html").write_text(html)


if __name__ == "__main__":
    main()

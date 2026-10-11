"""Build index.html (the visual review page) from ../PLAN.md.

The durable-set diagram is generated from the plan's "The durable set" table, the
milestone track from its "Milestones" table, the adoption date from
../PLAN.adoption-decision.json, and the disproof box from the plan's
"Disproof" paragraph. Fixed wording (the made-up library example, plan sizing)
is guarded: the build fails if the plan text it summarises is no longer present.

Run:   python3 build_page.py          # writes index.html
Check: python3 build_page.py --check  # exit 1 if index.html differs from a fresh build
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAN = HERE.parent / "PLAN.md"
DECISION = HERE.parent / "PLAN.adoption-decision.json"
OUT = HERE / "index.html"


# ---------------------------------------------------------------- plan parsing
def plan_text() -> str:
    return PLAN.read_text(encoding="utf-8")


def table_after(text: str, heading: str) -> list[dict[str, str]]:
    """Rows of the first Markdown table after the line that starts with `heading`."""
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if l.strip().startswith(heading)), None)
    if start is None:
        raise SystemExit(f"build_page: heading not found in PLAN.md: {heading!r}")
    i = start + 1
    while i < len(lines) and not lines[i].lstrip().startswith("|"):
        i += 1
    rows = []
    while i < len(lines) and lines[i].lstrip().startswith("|"):
        rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
        i += 1
    if len(rows) < 3:
        raise SystemExit(f"build_page: no table after {heading!r}")
    header, body = rows[0], rows[2:]
    return [dict(zip(header, r)) for r in body]


def plain(md: str) -> str:
    """Markdown cell -> plain text (drop backticks and bold)."""
    return md.replace("`", "").replace("**", "").strip()


def require(text: str, *phrases: str) -> None:
    for p in phrases:
        if p not in text:
            raise SystemExit(f"build_page: PLAN.md no longer contains {p!r}; update build_page.py's fixed wording")


def first_path(cell: str) -> str:
    m = re.search(r"`([^`]+)`", cell)
    return m.group(1) if m else plain(re.sub(r"\(.*?\)", "", cell))


def short_extends(cell: str) -> str:
    s = plain(cell)
    while re.search(r"\([^()]*\)", s):
        s = re.sub(r"\s*\([^()]*\)", "", s)
    parts = [p.strip() for p in s.split(";") if p.strip()]
    return "; ".join(parts[:2])


# ---------------------------------------------------------------- svg helpers
OVERFLOWS: list[str] = []

def wrap(text: str, width_px: float, char_px: float) -> list[str]:
    limit = max(8, int(width_px / char_px))
    lines, cur = [], ""
    words = []
    for word in text.split():
        while len(word) > limit:  # break long identifiers, preferably after an underscore
            cut = word.rfind("_", 0, limit) + 1 or limit
            words.append(word[:cut])
            word = word[cut:]
        words.append(word)
    for word in words:
        if cur and len(cur) + 1 + len(word) > limit:
            lines.append(cur)
            cur = word
        else:
            cur = (cur + " " + word).strip()
    return lines + ([cur] if cur else [])


def need(w, title, lines=(), label="", badge="") -> int:
    """Height in px a node() of width w needs for its text (same arithmetic as node())."""
    ty = 20 + (18 if label else 0) + 18 * len(wrap(title, w - 46, 8.4)) + 1
    ty += sum(15 * len(wrap(ln, w - 24, 6.7)) for ln in lines)
    return ty - 8 + (16 if badge else 0) + 6


def tip_attr(title: str, tip: str) -> str:
    return f'tabindex="0" role="button" aria-label="{escape(title)}: {escape(tip)}" data-tip="{escape(tip)}"'


def node(x, y, w, h, title, lines=(), tip="", cls="", label="", badge="") -> str:
    """One box: optional small label line, bold title (wrapped), muted lines, badge, and an info mark."""
    out = [f'<g class="node {cls}" {tip_attr(title, tip)}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7"/>']
    ty = y + 20
    if label:
        out.append(f'<text x="{x+12}" y="{ty}" class="t-label">{escape(label)}</text>')
        ty += 18
    tlines = wrap(title, w - 46, 8.4)
    for t in tlines:
        out.append(f'<text x="{x+12}" y="{ty}" class="t-title">{escape(t)}</text>')
        ty += 18
    ty += 1
    for ln in lines:
        for t in wrap(ln, w - 24, 6.7):
            out.append(f'<text x="{x+12}" y="{ty}" class="t-sub">{escape(t)}</text>')
            ty += 15
    if badge:
        out.append(f'<text x="{x+12}" y="{y+h-10}" class="t-badge">{escape(badge)}</text>')
        ty += 16
    if ty - 8 > y + h:
        OVERFLOWS.append(f"{title!r} needs {ty - 8 - y} px, has {h}")
    out.append(f'<g class="imark" aria-hidden="true"><circle cx="{x+w-16}" cy="{y+16}" r="9"/>'
               f'<text x="{x+w-16}" y="{y+20.5}" text-anchor="middle">i</text></g></g>')
    return "".join(out)


def arrow(x1, y1, x2, y2, label="", cls="arrow", lx=None, ly=None, curve=None) -> str:
    d = f"M{x1},{y1} Q{curve[0]},{curve[1]} {x2},{y2}" if curve else f"M{x1},{y1} L{x2},{y2}"
    s = f'<path d="{d}" class="{cls}" marker-end="url(#{"ahr" if "refuse" in cls else "ah"})"/>'
    if label:
        lx = (x1 + x2) / 2 if lx is None else lx
        ly = (y1 + y2) / 2 - 6 if ly is None else ly
        s += f'<text x="{lx}" y="{ly}" class="t-edge{" t-refuse" if "refuse" in cls else ""}" text-anchor="middle">{escape(label)}</text>'
    return s


def svg(cls, vb_w, vb_h, aria, body) -> str:
    return (f'<svg class="{cls}" viewBox="0 0 {vb_w} {vb_h}" role="group" aria-label="{escape(aria)}">'
            '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ahp"/></marker>'
            '<marker id="ahr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ahr"/></marker></defs>'
            + body + "</svg>")


# ---------------------------------------------------------------- 1. durable set
ROLE_KEYS = {
    "Goal and thesis": "goal", "Requirements": "req", "System model": "model",
    "Schema and contracts": "schema", "Decisions": "dec", "Glossary": "gloss", "Plans": "plans",
}
ROLE_PLAIN = {
    "goal": "Goal and thesis",
    "req": "Requirements",
    "model": "System model (rules)",
    "schema": "Schema and contracts",
    "dec": "Decision records",
    "gloss": "Glossary",
    "plans": "Plans (temporary)",
}
ROLE_WHY = {
    "goal": "Plain words: what the repository is steering toward, why this approach should get there, and what would show it won't.",
    "req": "Plain words: each thing the repository must do, with an ID and a test for 'done' and for 'wrong'.",
    "model": "Plain words: the map of the system. Every rule gets an ID, exactly one owner file, at least one check, and a link to the decision that explains it. 'ODD' is the shape: things, processes, records, views.",
    "schema": "Plain words: no new document. The system model's rules point at the real code files that define the data and the function signatures.",
    "dec": "Plain words: one short record per decision (an ADR), naming the rules it governs and what would show it was wrong.",
    "gloss": "Plain words: a word list built automatically from the model's names. Deferred: built only if fresh readers stumble on vocabulary.",
    "plans": "Plain words: a plan is temporary. Each one names which durable documents it will update; after completion it is archived.",
}
ROLE_BADGE = {"goal": "new page", "req": "extends existing", "model": "extends existing", "schema": "pointers only",
              "dec": "extends existing", "gloss": "generated · deferred", "plans": "temporary"}


def durable_roles(text: str) -> dict[str, dict[str, str]]:
    rows = table_after(text, "### The durable set")
    roles = {}
    for r in rows:
        key = ROLE_KEYS.get(plain(r["Role"]))
        if key is None:
            raise SystemExit(f"build_page: unknown durable role in PLAN.md: {r['Role']!r}; add it to ROLE_KEYS and the layout")
        home_cell = r["Home (default; repo.yaml may repoint)"]
        roles[key] = {
            "role": plain(r["Role"]),
            "holds": plain(r["What it must hold (minimum)"]),
            "home_full": plain(home_cell),
            "home": first_path(home_cell),
            "extends_full": plain(r["Existing owner it extends"]),
            "extends": short_extends(r["Existing owner it extends"]),
        }
    missing = set(ROLE_KEYS.values()) - set(roles)
    if missing:
        raise SystemExit(f"build_page: PLAN.md durable-set table lost roles: {sorted(missing)}")
    return roles


def role_tip(k, r) -> str:
    return (f"{ROLE_WHY[k]}\n\nMust hold: {r['holds']}\nLives at: {r['home_full']}\nExtends: {r['extends_full']}")


def role_node(k, r, x, y, w, h, extra="") -> str:
    cls = {"gloss": "k-deferred", "plans": "k-temp", "model": "k-key"}.get(k, "")
    lines = [f"Lives at: {r['home']}", f"Extends: {r['extends'] or 'nothing (new)'}"]
    if extra:
        lines.append(extra)
    return node(x, y, w, h, ROLE_PLAIN[k], lines, role_tip(k, r), cls, badge=ROLE_BADGE[k])


def durable_wide(roles) -> str:
    W, H = 300, 112
    pos = {"goal": (250, 52), "req": (250, 186), "dec": (250, 320),
           "schema": (630, 52), "model": (630, 186), "gloss": (630, 320)}
    b = []
    b.append('<rect x="226" y="18" width="724" height="438" rx="12" class="enclosure"/>'
             '<text x="244" y="40" class="t-group">Kept current: the durable set (every governed repository)</text>')
    b.append(node(20, 186, 170, 112, "Start here: wiki/index.md", ["A fresh reader reaches every durable document from here, within two links."],
                  "wiki/index.md is each repository's front page. The plan's success test: a fresh agent starting here answers 'what rule governs this, who owns it, which check proves it, and why' by following links only.", "k-src"))
    b.append(arrow(190, 242, 226, 242))
    for k, (x, y) in pos.items():
        b.append(role_node(k, roles[k], x, y, W, H))
    c = lambda k: (pos[k][0] + W / 2, pos[k][1] + H / 2)
    # relations inside the set
    b.append(arrow(400, 186, 400, 164, ""))  # req -> goal (serves)
    b.append('<text x="410" y="179" class="t-edge">serve the goal</text>')
    b.append(arrow(550, 242, 630, 242, "rules serve", ly=234))
    b.append(arrow(780, 186, 780, 164, ""))
    b.append('<text x="790" y="179" class="t-edge">points at code files</text>')
    b.append(arrow(780, 298, 780, 320, ""))
    b.append('<text x="790" y="314" class="t-edge">names generate it</text>')
    b.append(arrow(550, 376, 630, 290, "explain rules", lx=590, ly=352))
    # plans
    b.append(role_node("plans", roles["plans"], 1010, 186, 240, H + 56, "Each plan names which of these documents it updates."))
    b.append(arrow(1010, 262, 950, 262, "updates", ly=254))
    return svg("wide", 1260, 470, "Durable set: wiki/index.md leads to six kept-current documents; plans update them.", "".join(b))


def durable_narrow(roles) -> str:
    W, H, X = 316, 126, 22
    b = [node(X, 10, W, 76, "Start here: wiki/index.md", ["A fresh reader reaches every document below within two links."],
              "wiki/index.md is each repository's front page. A fresh agent starting here must answer 'what rule, who owns it, which check, why' by following links only.", "k-src")]
    b.append(arrow(180, 86, 180, 112))
    order = [("goal", "Requirements serve it."), ("req", "Rules in the model serve these."), ("model", "Points at code; names generate the glossary."),
             ("schema", "Pointed at by the model's rules."), ("dec", "Each explains one or more rules."), ("gloss", "")]
    y = 140
    top = 112
    for k, rel in order:
        b.append(role_node(k, roles[k], X + 10, y, W - 20, H + (16 if rel else 0), rel))
        y += H + (16 if rel else 0) + 12
    b.insert(1, f'<rect x="{X-6}" y="{top}" width="{W+12}" height="{y-top+4}" rx="12" class="enclosure"/>'
                f'<text x="{X+6}" y="{top+20}" class="t-group">Kept current: the durable set</text>')
    b.append(arrow(180, y + 50, 180, y + 6, "", ))
    b.append(f'<text x="190" y="{y+34}" class="t-edge">updates</text>')
    b.append(role_node("plans", roles["plans"], X, y + 50, W, H + 16, "Each names which documents it updates."))
    return svg("narrow", 360, y + 50 + H + 26, "Durable set, stacked for phone.", "".join(b))


# ---------------------------------------------------------------- 2. traceability chain
# The library example is illustrative (given by Brian's session, not in PLAN.md).
# The plan's own canonical example (RULE-ADOPT-GATE) is shown in the tooltip.
CHAIN = [
    ("owned by", "Owner: loan service", "the one component that enforces this rule", "System model: each rule names exactly one owner file or component (R4). The checker fails if that path does not exist."),
    ("reads", "Schema: Loan.due_date", "the data field the rule depends on", "Schema and contracts are not a separate document: the rule points at the code file that defines Loan.due_date (R4)."),
    ("enforced at", "Contract: checkout() refuses", "returns error OVERDUE_LOAN", "The function signature and error code live in code; the model's rule points at that file. A changed contract makes the model stale (R9)."),
    ("happens at", "Data flow: checkout step", "checkout looks up the member's open loans", "The model's processes name the rules they enforce (R4), so the checkout process lists RULE-LOAN-OVERDUE."),
    ("checked by", "Test: test_checkout_refused_when_overdue", "the check that proves the rule holds", "Each rule names at least one check path that exists (R4). No test, no clean report."),
    ("explained by", "ADR-0031: why 14 days", "the decision record with the reason", "Decision records name the rule IDs they govern and every ID must resolve (R5). The ADR also says what would show 14 days was wrong."),
]


def chain_wide(canonical: str) -> str:
    b = [node(20, 150, 230, 104, "REQ-12: Members can't hoard books", ["a requirement, with a success test"], "Requirement REQ-12, from the requirements document. Each requirement has an ID, a success criterion and a disproof condition (R3).", "", label="Requirement")]
    b.append(node(320, 140, 270, 124, "RULE-LOAN-OVERDUE", ["no borrowing while a loan is overdue"],
                  "A rule in the system model. It has an ID and links to exactly one owner, at least one check, and the decision record that explains it. The checker verifies every link resolves.\n\nThe plan's real example: " + canonical, "k-key", label="System-model rule"))
    b.append(arrow(320, 202, 250, 202, "serves", ly=194))
    n = len(CHAIN)
    top, step, h = 12, 64, 56
    for i, (edge, title, sub, tip) in enumerate(CHAIN):
        y = top + i * step
        b.append(node(800, y, 440, h, title, [sub], tip))
        yc = y + h / 2
        t = 0.74
        lx, ly = 590 + (800 - 590) * t, 202 + (yc - 202) * t
        b.append(arrow(590, 202, 800, yc, edge, lx=lx - 6, ly=ly - 5))
    return svg("wide", 1260, top + n * step + 4, "Traceability chain: REQ-12 is served by RULE-LOAN-OVERDUE, which links to its owner, schema, contract, data-flow step, test and decision record.", "".join(b))


def chain_narrow(canonical: str) -> str:
    b = [node(20, 10, 320, 86, "REQ-12: Members can't hoard books", ["a requirement, with a success test"], "Requirement REQ-12. Each requirement has an ID, a success criterion and a disproof condition (R3).", "", label="Requirement")]
    b.append(arrow(180, 132, 180, 98, ""))
    b.append('<text x="190" y="120" class="t-edge">serves</text>')
    b.append(node(20, 134, 320, 90, "RULE-LOAN-OVERDUE", ["no borrowing while a loan is overdue"],
                  "A system-model rule: ID, one owner, at least one check, and its decision record. The plan's real example: " + canonical, "k-key", label="System-model rule"))
    y = 244
    for edge, title, sub, tip in CHAIN:
        h = need(274, title, [sub], label=edge)
        b.append(f'<path d="M36,{y-20} L36,{y+h/2} L64,{y+h/2}" class="arrow" marker-end="url(#ah)"/>')
        b.append(node(66, y, 274, h, title, [sub], tip, label=edge))
        y += h + 12
    return svg("narrow", 360, y, "Traceability chain stacked for phone.", "".join(b))


# ---------------------------------------------------------------- 3. lifecycle
def lifecycle_wide() -> str:
    b = []
    y, h = 104, 116
    b.append(node(20, y, 190, h, "Write the plan", ["names which durable documents it will update"], "The author writes the plan with a Durable documents section (or one line for a small plan). See plan sizes below.", "k-src"))
    b.append(node(270, y, 260, h, "Adoption check", ["NEW: refuses a plan with no Durable documents section"],
                  "Company Planning's adoption gate gets a new checklist item, CORE-DURABLE-DOCS (R7). A plan without the section, or with 'none' and no reason, is not adopted. Lands at milestone M3.", "k-gate", badge="planned · M3"))
    b.append(node(590, y, 190, h, "Do the work", ["commits on the plan's branch"], "Normal work. The commits are the range the completion check reads.", ""))
    b.append(node(840, y, 260, h, "Completion check", ["NEW: refuses if a declared document did not change"],
                  "durable_docs_check.py --plan <id> --range <base>..<head> (R8). Refuses when a document the plan named was not changed in its commits, and refuses 'none' without a reason. Runs from the plan-finish step and from make check on the branch. Lands at M3.", "k-gate", badge="planned · M3"))
    b.append(node(1160, y, 90, h, "Done", ["docs current"], "The plan is archived; the durable documents it named now reflect the change.", "k-src"))
    b.append(arrow(210, y + h / 2, 270, y + h / 2))
    b.append(arrow(530, y + h / 2, 590, y + h / 2, "adopted", ly=y + h / 2 - 8))
    b.append(arrow(780, y + h / 2, 840, y + h / 2))
    b.append(arrow(1100, y + h / 2, 1160, y + h / 2))
    b.append(arrow(330, y, 150, y, "refused: add the section", cls="arrow refuse", curve=(240, 4), lx=240, ly=44))
    b.append(arrow(900, y, 700, y, "refused: update the document", cls="arrow refuse", curve=(800, 4), lx=800, ly=44))
    return svg("wide", 1260, 236, "Plan lifecycle: write, adoption check (new), work, completion check (new), done; each check can send the plan back.", "".join(b))


def lifecycle_narrow() -> str:
    b = []
    X, W = 20, 270
    rows = [
        ("Write the plan", ["names which durable documents it will update"], "The author writes the plan with a Durable documents section (or one line for a small plan).", "k-src", ""),
        ("Adoption check", ["NEW: refuses a plan with no Durable documents section"], "New checklist item CORE-DURABLE-DOCS in Company Planning's adoption gate (R7). Lands at M3.", "k-gate", "planned · M3"),
        ("Do the work", ["commits on the plan's branch"], "Normal work; the commits are the range the completion check reads.", "", ""),
        ("Completion check", ["NEW: refuses if a declared document did not change"], "durable_docs_check.py --plan --range (R8): refuses an unchanged declared document, and 'none' without a reason. Lands at M3.", "k-gate", "planned · M3"),
        ("Done", ["plan archived; durable documents current"], "The durable documents the plan named now reflect the change.", "k-src", ""),
    ]
    y, ys = 10, []
    for t, l, tip, cls, badge in rows:
        h = 96 if badge else 76
        b.append(node(X, y, W, h, t, l, tip, cls, badge=badge))
        ys.append((y, h))
        y += h + 30
    for i in range(len(ys) - 1):
        b.append(arrow(X + W / 2, ys[i][0] + ys[i][1], X + W / 2, ys[i + 1][0]))
    (y0, h0), (y1, h1) = ys[0], ys[1]
    b.append(arrow(X + W, y1 + h1 / 2, X + W, y0 + h0 / 2, "", cls="arrow refuse", curve=(350, (y0 + y1) / 2 + 40)))
    b.append(f'<text x="{X+W-4}" y="{y1 + h1 + 20}" class="t-edge t-refuse" text-anchor="end">refused: add the section ↑</text>')
    (y2, h2), (y3, h3) = ys[2], ys[3]
    b.append(arrow(X + W, y3 + h3 / 2, X + W, y2 + h2 / 2, "", cls="arrow refuse", curve=(350, (y2 + y3) / 2 + 40)))
    b.append(f'<text x="{X+W-4}" y="{y3 + h3 + 20}" class="t-edge t-refuse" text-anchor="end">refused: update the document ↑</text>')
    return svg("narrow", 360, y, "Plan lifecycle stacked for phone.", "".join(b))


def sizing_html(text: str) -> str:
    require(text, "Durable documents: <role>#<ID>, ...", "Durable documents: none -- <reason>", "A full plan carries a delta table (role, ID, change)", "a Trivial change (AES commit rule) declares nothing")
    frames = [
        ("Trivial change", "declares nothing",
         '<div class="mono empty">(nothing to write)</div>',
         "Trivial means at most 3 files and 60 lines, touching nothing that runs (the AES commit rule). No plan, so no Durable documents line."),
        ("Small plan (quick-adopt)", "one line",
         '<div class="mono">Durable documents: system_model#RULE-LOAN-OVERDUE</div><div class="mono alt">or: Durable documents: none -- &lt;reason&gt;</div>',
         "quick-adopt is Company Planning's 10-second adoption for one-repository reversible work. It gains a --durable-doc flag that writes this line (R7). 'none' must carry a reason."),
        ("Full plan", "a small table",
         '<table class="mini"><tr><th>role</th><th>ID</th><th>change</th></tr><tr><td>system_model</td><td>RULE-LOAN-OVERDUE</td><td>new rule</td></tr><tr><td>decisions</td><td>ADR-0031</td><td>why 14 days</td></tr></table>',
         "A full plan carries a delta table: which role, which ID, what changes. The completion check reads it and confirms each named document changed in the plan's commits."),
    ]
    cards = "".join(
        f'<div class="frame" {tip_attr(t, tip)}><span class="ibtn" aria-hidden="true">i</span><h3>{escape(t)}</h3><p class="lead">writes: <b>{escape(s)}</b></p>{body}</div>'
        for t, s, body, tip in frames)
    return f'<div class="frames">{cards}</div>'


# ---------------------------------------------------------------- 4. milestones
def milestones(text: str, adopted: str):
    """Milestone state comes from the Output cell: 'done <date>:' prefix = done, 'done <date>' inside = partly done."""
    rows = table_after(text, "## Milestones")
    out = []
    for r in rows:
        name = plain(r["Milestone"])
        mid, _, label = name.partition(" ")
        output = plain(r["Output"])
        m_done = re.match(r"done (\d{4}-\d{2}-\d{2}):\s*", output)
        m_part = re.search(r"done (\d{4}-\d{2}-\d{2})", output)
        short = output[m_done.end():] if m_done else output
        while re.search(r"\([^()]*\)", short):
            short = re.sub(r"\s*\([^()]*\)", "", short)
        if m_done:
            st, state = "done", f"✓ done {m_done.group(1)}"
        elif m_part:
            st, state = "part", f"◐ partly done {m_part.group(1)}"
        else:
            st, state = "todo", "planned"
        out.append({"id": mid, "label": label, "output": output, "short": short.strip(" ;,"), "trigger": plain(r["Promotion trigger"]),
                    "state": state, "st": st, "done": st == "done"})
    if [m["id"] for m in out] != ["M0", "M1", "M2", "M3", "M4", "M5"]:
        raise SystemExit("build_page: milestone IDs in PLAN.md are not M0..M5; update the layout")
    return out


def ms_tip(m) -> str:
    return f"{m['id']} {m['label']}\nOutput: {m['output']}\nCounts as finished when: {m['trigger']}\nState: {m['state']}"


def milestones_wide(ms) -> str:
    b, W, gap = [], 190, 18
    H = max(need(W, f"{m['id']} {m['label']}", [m["short"]], badge="x") for m in ms)
    for i, m in enumerate(ms):
        x = 20 + i * (W + gap)
        b.append(node(x, 14, W, H, f"{m['id']} {m['label']}", [m["short"]], ms_tip(m), "st-" + m["st"], badge=m["state"]))
        if i:
            b.append(arrow(x - gap, 14 + H / 2, x, 14 + H / 2))
    return svg("wide", 1260, H + 28, "Milestones M0 to M5; M0 is done, the rest are planned.", "".join(b))


def milestones_narrow(ms) -> str:
    b, y = [], 10
    for i, m in enumerate(ms):
        h = need(320, f"{m['id']} {m['label']}", [m["short"]], badge="x")
        b.append(node(20, y, 320, h, f"{m['id']} {m['label']}", [m["short"]], ms_tip(m), "st-" + m["st"], badge=m["state"]))
        if i:
            b.append(arrow(180, y - 14, 180, y))
        y += h + 14
    return svg("narrow", 360, y, "Milestones stacked for phone.", "".join(b))


# ---------------------------------------------------------------- 5. disproof
def disproof_html(text: str) -> str:
    m = re.search(r"\*\*Disproof \(the approach is wrong if\):\*\*(.+)", text)
    if not m:
        raise SystemExit("build_page: Disproof paragraph not found in PLAN.md")
    full = plain(m.group(1))
    require(text, "five or more declare `none`", "mechanical (only IDs, dates or links changed", "the cold reader fails the canonical question on a checker-clean pilot",
            "a document labelled as using arc42 section names violates one of the four rules")
    items = [
        ("Plans dodge it", "Two weeks after M4, of the 10 latest finished plans in the two pilot repositories, 5 or more say 'none'."),
        ("Updates are paperwork", "Or their document changes only touch IDs, dates or links, judged by reading the diffs."),
        ("The documents don't answer", "A fresh agent fails the canonical question ('what rule, who owns it, which check, why') on a pilot the checker calls clean."),
        ("arc42 claim broken", "A document claiming arc42 section names breaks one of the plan's four heading rules, or an AES addition is unlabelled."),
    ]
    lis = "".join(f'<li {tip_attr(t, d + chr(10) + chr(10) + "From the plan: " + full)}><span class="ibtn" aria-hidden="true">i</span><b>{escape(t)}.</b> {escape(d)}</li>' for t, d in items)
    return (f'<aside class="disproof"><h2>5. What would prove this wrong</h2><ul>{lis}</ul>'
            '<p class="then">If any of these happens, the plan\'s feedback entry records it and the rule is revised or withdrawn.</p></aside>')


# ---------------------------------------------------------------- page
CSS = """:root{--bg:#ffffff;--fg:#111827;--muted:#4b5563;--line:#8b95a3;--panel:#f3f4f6;--blue:#1d4ed8;--bluefill:#dbeafe;--orange:#b45309;--orangefill:#fff4e5;--grey:#6b7280;--tipbg:#111827;--tipfg:#f9fafb}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#0f1420;--fg:#e5e7eb;--muted:#a3adba;--line:#6b7280;--panel:#1a2030;--blue:#7fb2ff;--bluefill:#1e3a5f;--orange:#f5a524;--orangefill:#2a1f0e;--grey:#a3adba;--tipbg:#f3f4f6;--tipfg:#111827}}
:root[data-theme="dark"]{--bg:#0f1420;--fg:#e5e7eb;--muted:#a3adba;--line:#6b7280;--panel:#1a2030;--blue:#7fb2ff;--bluefill:#1e3a5f;--orange:#f5a524;--orangefill:#2a1f0e;--grey:#a3adba;--tipbg:#f3f4f6;--tipfg:#111827}
*{box-sizing:border-box}html,body{overflow-x:hidden}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:1300px;margin:0 auto;padding:20px 16px 40px}
h1{font-size:1.4rem;line-height:1.25;margin:0 0 8px}
p.q{font-size:1.05rem;margin:0 0 6px;border-left:4px solid var(--blue);padding:4px 0 4px 12px}
p.status{font-size:.88rem;color:var(--muted);margin:0 0 18px}
section.view{margin:26px 0 0}section.view>h2{font-size:1.1rem;margin:0 0 2px}section.view>p.ask{margin:0 0 8px;color:var(--muted);font-size:.95rem}
svg{width:100%;height:auto;display:block;overflow:visible}svg text{fill:var(--fg);font-family:inherit}
.t-title{font-size:14px;font-weight:700}.t-sub{font-size:12px;fill:var(--muted)}.t-label{font-size:11.5px;fill:var(--muted);font-style:italic}
.t-badge{font-size:11.5px;font-weight:700;fill:var(--blue)}.t-group{font-size:13px;font-weight:700;fill:var(--muted)}
.t-edge{font-size:12px;fill:var(--muted);paint-order:stroke;stroke:var(--bg);stroke-width:5px;stroke-linejoin:round}.t-refuse{fill:var(--orange);font-weight:700}
.node{cursor:help;outline:none}.node rect{fill:var(--bg);stroke:var(--fg);stroke-width:1.5}
.node:hover rect,.node:focus-visible rect,.node.on rect{stroke:var(--blue);stroke-width:3}
.k-src rect{fill:var(--panel)}.k-key rect{stroke:var(--blue);stroke-width:3;fill:var(--bluefill)}
.k-gate rect{stroke-width:4;stroke-dasharray:9 5}.k-deferred rect{stroke:var(--grey);stroke-dasharray:2 4}.k-temp rect{stroke:var(--grey);fill:var(--panel)}
.st-done rect{fill:var(--bluefill);stroke:var(--blue);stroke-width:2.5}.st-todo rect{stroke-dasharray:6 5}.st-part rect{stroke:var(--blue);stroke-width:2.5}
.imark circle{fill:none;stroke:var(--muted);stroke-width:1.3}.imark text{font-size:12px;font-weight:700;fill:var(--muted);font-style:italic;font-family:Georgia,serif}
.enclosure{fill:none;stroke:var(--line);stroke-width:1.5;stroke-dasharray:1 0}
.arrow{fill:none;stroke:var(--line);stroke-width:1.7}.ahp{fill:var(--line)}.refuse{stroke:var(--orange);stroke-width:2.2;stroke-dasharray:7 4}.ahr{fill:var(--orange)}
.wide{display:block}.narrow{display:none}
@media (max-width:760px){.wide{display:none}.narrow{display:block}h1{font-size:1.15rem}}
.frames{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:12px}
@media (max-width:760px){.frames{grid-template-columns:1fr}}
.frame{position:relative;border:1.5px solid var(--line);border-radius:8px;padding:12px 14px;cursor:help;outline:none;min-width:0}
.frame:hover,.frame:focus-visible,.frame.on{border-color:var(--blue);box-shadow:0 0 0 2px var(--blue) inset}
.frame h3{margin:0 0 2px;font-size:1rem}.frame p.lead{margin:0 0 8px;font-size:.9rem;color:var(--muted)}
.mono{font:13px/1.4 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:var(--panel);border-radius:5px;padding:6px 8px;overflow-wrap:anywhere}
.mono.alt{margin-top:6px;color:var(--muted)}.mono.empty{color:var(--muted);font-style:italic}
table.mini{border-collapse:collapse;font:12.5px/1.35 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;width:100%;table-layout:fixed}
table.mini th,table.mini td{border:1px solid var(--line);padding:3px 5px;text-align:left;overflow-wrap:anywhere}table.mini th{background:var(--panel)}
.ibtn{position:absolute;top:8px;right:8px;width:20px;height:20px;border:1.3px solid var(--muted);border-radius:50%;font:italic 700 12px/17px Georgia,serif;text-align:center;color:var(--muted)}
.disproof{margin-top:28px;border:2.5px solid var(--orange);background:var(--orangefill);border-radius:10px;padding:12px 16px}
.disproof h2{margin:0 0 6px;font-size:1.1rem}.disproof ul{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:8px 16px}
@media (max-width:760px){.disproof ul{grid-template-columns:1fr}}
.disproof li{position:relative;padding:8px 32px 8px 10px;border:1px dashed var(--orange);border-radius:6px;background:var(--bg);cursor:help;outline:none}
.disproof li:hover,.disproof li:focus-visible,.disproof li.on{border-style:solid;border-width:2px}
.disproof p.then{margin:10px 0 0;font-size:.92rem}
ul.legend{list-style:none;padding:0;margin:14px 0 4px;display:flex;flex-wrap:wrap;gap:8px 18px;font-size:.88rem}
ul.legend span{display:inline-block;width:28px;height:15px;vertical-align:-3px;margin-right:6px;border-radius:3px}
.l-done{background:var(--bluefill);border:2.5px solid var(--blue)}.l-todo{border:2px dashed var(--fg)}.l-part{border:2.5px solid var(--blue)}.l-gate{border:4px dashed var(--fg)}
.l-def{border:2px dotted var(--grey)}.l-ref{border-top:3px dashed var(--orange);height:0!important;margin-bottom:4px}.l-key{background:var(--bluefill);border:3px solid var(--blue)}
#tip{position:fixed;z-index:10;max-width:min(420px,calc(100vw - 24px));background:var(--tipbg);color:var(--tipfg);padding:9px 12px;border-radius:7px;font-size:.86rem;line-height:1.4;white-space:pre-line;box-shadow:0 6px 20px rgba(0,0,0,.25);pointer-events:none;opacity:0;transition:opacity 80ms}
#tip.show{opacity:1}
footer{margin-top:22px;font-size:.8rem;color:var(--muted)}footer code{font-size:.78rem;overflow-wrap:anywhere}"""

JS = """(function(){var tip=document.getElementById('tip'),cur=null,pinned=null;
function place(el){var r=el.getBoundingClientRect(),vw=document.documentElement.clientWidth,vh=window.innerHeight;tip.style.left='0px';tip.style.top='0px';
var w=tip.offsetWidth,h=tip.offsetHeight,x=Math.min(Math.max(8,r.left),vw-w-8),y=r.bottom+8;if(y+h>vh-8&&r.top-h-8>8)y=r.top-h-8;if(y+h>vh-8)y=Math.max(8,vh-h-8);
tip.style.left=x+'px';tip.style.top=y+'px';}
function show(el){if(cur&&cur!==el)cur.classList.remove('on');cur=el;el.classList.add('on');tip.textContent=el.getAttribute('data-tip');tip.classList.add('show');tip.setAttribute('aria-hidden','false');place(el);}
function hide(){if(cur)cur.classList.remove('on');cur=null;pinned=null;tip.classList.remove('show');tip.setAttribute('aria-hidden','true');}
function target(e){return e.target&&e.target.closest?e.target.closest('[data-tip]'):null;}
document.addEventListener('pointerover',function(e){var t=target(e);if(t&&!pinned)show(t);});
document.addEventListener('pointerout',function(e){var t=target(e);if(t&&!pinned&&!(e.relatedTarget&&t.contains(e.relatedTarget)))hide();});
document.addEventListener('focusin',function(e){var t=target(e);if(t)show(t);});
document.addEventListener('focusout',function(e){if(!pinned)hide();});
document.addEventListener('click',function(e){var t=target(e);if(!t){hide();return;}if(pinned===t){hide();}else{show(t);pinned=t;}});
document.addEventListener('keydown',function(e){var t=target(e);if(e.key==='Escape')hide();else if(t&&(e.key==='Enter'||e.key===' ')){e.preventDefault();show(t);pinned=t;}});
window.addEventListener('scroll',function(){if(cur)place(cur);},{passive:true});})();"""


def build() -> str:
    text = plan_text()
    sha = hashlib.sha256(text.encode()).hexdigest()[:12]
    dec = json.loads(DECISION.read_text())
    adopted = dec["decided_at"][:10]
    if dec.get("decision") != "adopted":
        raise SystemExit("build_page: adoption decision is not 'adopted'")
    roles = durable_roles(text)
    ms = milestones(text, adopted)
    canonical = re.search(r'canonical_example: "(.+)"', text).group(1)
    done_count = sum(m["done"] for m in ms)
    nm = re.search(r"(\d+) items evidenced", dec["summary"][0])
    summary = f"pass, {nm.group(1)} checklist items evidenced" if nm else dec["summary"][0]
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Durable documents plan</title><style>{CSS}</style></head><body><main>
<h1>Every governed repository keeps one fixed set of documents, and a plan cannot finish without updating the ones it named.</h1>
<p class="q">Decide: does this make planning rigorous within reason, and is the set of documents right? Reply in the terminal.</p>
<p class="status">Plan adopted {adopted} by Company Planning's gate ({escape(summary)}). Milestones done: {done_count} of {len(ms)}{"; partly done: " + ", ".join(m["id"] for m in ms if m["st"] == "part") if any(m["st"] == "part" for m in ms) else ""}. Nothing enforced yet. Built from <code>PLAN.md</code> sha256 {sha}. Hover, focus or tap any box marked <i>i</i> for detail.</p>
<ul class="legend"><li><span class="l-done"></span>Done</li><li><span class="l-part"></span>Partly done</li><li><span class="l-todo"></span>Planned</li><li><span class="l-gate"></span>New check that can refuse</li><li><span class="l-ref"></span>Refused: sent back</li><li><span class="l-key"></span>The rule at the centre</li><li><span class="l-def"></span>Generated, deferred</li></ul>
<section class="view"><h2>1. The durable set: which documents, where they live, what they build on</h2><p class="ask">Six documents stay current; plans are temporary and must update them. Only the goal page is new.</p>
{durable_wide(roles)}{durable_narrow(roles)}</section>
<section class="view"><h2>2. One rule, traced end to end (made-up library example)</h2><p class="ask">The checker follows every link from a rule; a broken or missing link is a finding.</p>
{chain_wide(canonical)}{chain_narrow(canonical)}</section>
<section class="view"><h2>3. A plan's life: two new checks that can send it back</h2><p class="ask">How much a plan must write depends on its size.</p>
{lifecycle_wide()}{lifecycle_narrow()}{sizing_html(text)}</section>
<section class="view"><h2>4. Milestones</h2><p class="ask">Two pilots first (company-planning and AES canonical), then every governed repository.</p>
{milestones_wide(ms)}{milestones_narrow(ms)}</section>
{disproof_html(text)}
<footer>Source: <code>proposals/aes-durable-docs/PLAN.md</code> (durable-set and milestones tables; disproof paragraph), adoption record <code>PLAN.adoption-decision.json</code>, on branch <code>shaping/aes-durable-docs</code> of BrianMills2718/agentic-engineering-system-canonical. Generated by <code>review-page/build_page.py</code>; <code>--check</code> fails if this page drifts from the plan. The library example is illustrative; the plan's real example is RULE-ADOPT-GATE in company-planning.</footer>
</main><div id="tip" role="tooltip" aria-hidden="true"></div><script>{JS}</script></body></html>
"""
    if OVERFLOWS:
        raise SystemExit("build_page: text overflows boxes:\n  " + "\n  ".join(OVERFLOWS))
    return page


def main() -> int:
    html = build()
    if "--check" in sys.argv[1:]:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != html:
            print(f"build_page --check: FAIL, {OUT.name} differs from a fresh build of PLAN.md (run python3 build_page.py)")
            return 1
        print(f"build_page --check: PASS, {OUT.name} matches a fresh build of PLAN.md")
        return 0
    OUT.write_text(html, encoding="utf-8")
    print(f"build_page: wrote {OUT} ({len(html)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

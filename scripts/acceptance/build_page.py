"""Build proposals/planning-package/review-page/lockstep-acceptance.html from the A1-A5 run records.

Reads docs/planning/acceptance-criteria.json (entries A1-A5: criterion, expected, failure example, view) and
docs/planning/runs/lockstep-acceptance/a<n>.json (written by the a<n>.py run scripts). An entry with no record shows
NOT RUN. Self-contained: inline style, no scripts. Verdicts are read from the rows' computed pass flags, not typed here.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RECORDS = ROOT / "docs/planning/runs/lockstep-acceptance"
OUT = ROOT / "proposals/planning-package/review-page/lockstep-acceptance.html"
RAW = "https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/main/docs/planning/runs/lockstep-acceptance/"
ENTRIES = ["A1", "A2", "A3", "A4", "A5"]
SHORT = {
    "A1": "One command sets Lockstep up",
    "A2": "The guard refuses writes the plan does not name",
    "A3": "Bad commits are refused",
    "A4": "Files carry the approved text word for word",
    "A5": "Portable and shareable",
}
EXPLAIN = {
    "A1": "Lockstep is the tool that makes an agent follow the plan. Here, one typed command should set it up in an empty repository.",
    "A2": "The guard is a small program that Claude Code runs before every action the agent takes. It can say no. "
          "Each row below is one thing an agent tried, fed to the real guard.",
    "A3": "A commit is a saved set of changes. Lockstep's commit checks run before a commit is accepted. "
          "Each row below is one real commit, made in a throwaway repository, and the check that should judge it.",
    "A4": "After you approve a plan, the agent runs one command that creates every planned file. "
          "The first comment block in each file (its docstring) should hold the approved text exactly. Pick a file below.",
    "A5": "Can someone else install and use Lockstep on their own computer without edits?",
}
CSS = """
:root{--bg:#fff;--fg:#1b1f24;--mut:#57606a;--line:#c9ced4;--blue:#0b5cad;--blueb:#e3effb;--orange:#b84a00;--orangeb:#fdeedd;--grey:#57606a;--greyb:#eceef1;--card:#f6f8fa}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#14181d;--fg:#e6e9ed;--mut:#a3acb7;--line:#3a424b;--blue:#6db3f2;--blueb:#14304d;--orange:#ffa44d;--orangeb:#4a2a10;--grey:#a3acb7;--greyb:#262c33;--card:#1c2127}}
*{box-sizing:border-box}
body{font:16px/1.5 system-ui,-apple-system,sans-serif;margin:0;padding:0 16px;color:var(--fg);background:var(--bg)}
main{max-width:1100px;margin:0 auto;padding:20px 0 64px;min-width:0}
h1{font-size:26px;margin:8px 0}
h2{font-size:21px;margin:0 0 8px}
h3{font-size:16px;margin:20px 0 6px}
a{color:var(--blue)}
code,pre{font:13px/1.45 ui-monospace,Menlo,Consolas,monospace;overflow-wrap:anywhere}
pre{background:var(--card);border:1px solid var(--line);padding:10px;overflow-x:auto;white-space:pre-wrap;overflow-wrap:anywhere;margin:6px 0}
section.entry{border:1px solid var(--line);border-radius:10px;padding:16px;margin:24px 0;background:var(--bg)}
.crit{border-left:4px solid var(--line);padding:2px 0 2px 12px;margin:8px 0 12px;font-size:17px}
.verdict{display:flex;gap:14px;align-items:center;flex-wrap:wrap;border-radius:10px;padding:12px 16px;margin:12px 0}
.verdict .big{font-size:34px;font-weight:800;letter-spacing:.02em}
.verdict .why{font-size:15px;flex:1 1 220px}
.v-pass{background:var(--blueb);color:var(--blue);border:2px solid var(--blue)}
.v-fail{background:var(--orangeb);color:var(--orange);border:2px solid var(--orange)}
.v-none{background:var(--greyb);color:var(--grey);border:2px dashed var(--grey)}
.why{color:var(--fg)}
.pill{white-space:nowrap;display:inline-block;font-weight:700;font-size:13px;padding:1px 8px;border-radius:999px;border:1.5px solid}
.p-pass{color:var(--blue);background:var(--blueb);border-color:var(--blue)}
.p-fail{color:var(--orange);background:var(--orangeb);border-color:var(--orange)}
table{border-collapse:collapse;width:100%;font-size:14px;margin:8px 0}
th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top;overflow-wrap:anywhere}
th{background:var(--card)}
tr.r-fail td{background:var(--orangeb)}
details{margin:6px 0}summary{cursor:pointer;color:var(--blue)}
.broken{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:14px 0}
.meta{color:var(--mut);font-size:13px}
.md{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:8px 0}
.md>div{min-width:0}
.md h4{margin:0 0 4px;font-size:14px;color:var(--mut)}
.file{border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:10px 0}
.file>summary{font-weight:700;color:var(--fg)}
.receipt{border:2px solid var(--line);border-radius:12px;padding:12px 16px;background:var(--card)}
.nav{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}
.nav a{border:1px solid var(--line);border-radius:8px;padding:4px 10px;text-decoration:none;font-weight:600}
.legend{font-size:14px}
@media (max-width:700px){
 .md{grid-template-columns:1fr}
 table.stack thead{display:none}
 table.stack tr{display:block;border:1px solid var(--line);border-radius:8px;margin:10px 0;overflow:hidden}
 table.stack td{display:block;border:0;border-bottom:1px solid var(--line)}
 table.stack td:last-child{border-bottom:0}
 table.stack td::before{content:attr(data-l);display:block;font-size:12px;font-weight:700;color:var(--mut)}
 .verdict .big{font-size:30px}
}
"""


def e(x) -> str:
    return html.escape(str(x))


def load(entry: str) -> dict | None:
    path = RECORDS / f"{entry.lower()}.json"
    return json.loads(path.read_text()) if path.is_file() else None


def pill(ok: bool) -> str:
    return f'<span class="pill {"p-pass" if ok else "p-fail"}">{"PASS" if ok else "FAIL"}</span>'


def verdict_box(rec: dict | None) -> str:
    if not rec or not rec.get("rows"):
        return ('<div class="verdict v-none"><span class="big">NOT RUN</span><span class="why">No run record exists yet, '
                'so this entry can be neither passed nor failed.</span></div>')
    rows = rec["rows"]
    bad = [r for r in rows if not r["pass"]]
    if not bad:
        return (f'<div class="verdict v-pass"><span class="big">PASS</span><span class="why">All {len(rows)} rows '
                f'did what they should.</span></div>')
    names = "; ".join(e(r["label"]) for r in bad)
    return (f'<div class="verdict v-fail"><span class="big">FAIL</span><span class="why">{len(rows) - len(bad)} of '
            f'{len(rows)} rows pass. Did not do what it should: {names}.</span></div>')


def decision_table(rec: dict) -> str:
    body = []
    for r in rec["rows"]:
        msg = r.get("message") or ""
        detail = ""
        if r.get("command") and not r["command"].startswith("("):
            detail += f'<div class="meta">Command or commit: <code>{e(r["command"])}</code></div>'
        if r.get("files_changed"):
            detail += f'<div class="meta">Files in the commit: {e(", ".join(r["files_changed"]))}</div>'
        if msg.strip():
            detail += f'<details><summary>Open the message it gave</summary><pre>{e(msg)}</pre></details>'
        elif r.get("command"):
            detail += '<div class="meta">It gave no message (allowed silently).</div>'
        body.append(f'<tr class="{"" if r["pass"] else "r-fail"}"><td data-l="What was tried">{e(r["label"])}{detail}</td>'
                    f'<td data-l="Should">{e(r["should"])}</td><td data-l="Did">{e(r["did"])}</td>'
                    f'<td data-l="Result">{pill(r["pass"])}</td></tr>')
    return ('<table class="stack"><thead><tr><th>What was tried</th><th>Should (what the plan says)</th>'
            '<th>Did (what actually happened)</th><th>Result</th></tr></thead><tbody>' + "".join(body) + "</tbody></table>")


def master_detail(rec: dict) -> str:
    out = []
    for r in rec["rows"]:
        if "first_docstring" not in r:
            out.append(f'<div class="receipt"><b>{e(r["label"])}</b> {pill(r["pass"])}<br>'
                       f'Should: {e(r["should"])}<br>Did: {e(r["did"])}</div>')
            continue
        scen = "\n\n".join(r["scenarios"])
        found = "".join(f'<li>{e(k)}: {pill(v)}</li>' for k, v in r["parts_found"].items())
        out.append(
            f'<details class="file"><summary>{e(r["id"])} {pill(r["pass"])}</summary>'
            f'<div class="md"><div><h4>Approved plan (left): {e(r["requirement_id"])}</h4>'
            f'<pre>{e(r["requirement_text"])}\n\n{e(scen)}</pre>'
            f'<h4>Test names the plan lists</h4><pre>{e(chr(10).join(r["test_names"]) or "(none for a test file)")}</pre></div>'
            f'<div><h4>The file\'s first docstring (right)</h4><pre>{e(r["first_docstring"])}</pre></div></div>'
            f'<div class="meta">Is each piece in the docstring exactly as approved?</div><ul>{found}</ul></details>')
    appr = next((r for r in rec["rows"] if r["id"] == "approval"), None)
    head = ""
    if appr:
        head = (f'<h3>Was anything laid out before the approval?</h3><div class="receipt">{pill(appr["pass"])} '
                f'Should: {e(appr["should"])}. Did: {e(appr["did"])}.<br>'
                f'<span class="meta">Files that existed after the plan was approved and before the layout command ran: '
                f'{e(", ".join(rec.get("files_before_layout", [])))}</span></div>')
    return head + '<h3>The planned files (open one)</h3>' + "".join(
        o for o, r in zip(out, rec["rows"]) if r["id"] != "approval")


def receipt_card(rec: dict) -> str:
    inst = rec.get("install")
    if not inst:  # a record without the install fields falls back to the plain list
        rows = "".join(f'<li>{pill(r["pass"])} {e(r["label"])}: should {e(r["should"])}; did {e(r["did"])}</li>' for r in rec["rows"])
        return f'<div class="receipt"><ul>{rows}</ul></div>'
    rows = "".join(f'<tr class="{"" if r["pass"] else "r-fail"}"><td data-l="What was checked">{e(r["label"])}</td>'
                   f'<td data-l="Should">{e(r["should"])}</td><td data-l="Did">{e(r["did"])}</td>'
                   f'<td data-l="Result">{pill(r["pass"])}</td></tr>' for r in rec["rows"])
    files = "".join(f'<details class="file"><summary>{e(path)}</summary><pre>{e(text)}</pre></details>'
                    for path, text in rec.get("files_written", {}).items())
    hooks = rec.get("hook_commands", {})
    names = (("claude", "1. Claude Code: .claude/settings.json, PreToolUse"), ("codex", "2. Codex: .codex/hooks.json, PreToolUse"),
             ("lefthook", "3. Commit checker: lefthook.yml, pre-commit"))
    hook_html = "".join(f'<h4>{e(label)}</h4>' + "".join(f"<pre>{e(c)}</pre>" for c in hooks.get(k, [])) for k, label in names)
    return (f'<div class="receipt"><h3 style="margin-top:0">The one command typed</h3><pre>{e(inst["command_run"])}</pre>'
            f'<p class="meta">Taken from the README line <code>{e(inst["readme_line"])}</code>, run in a new empty git repository '
            f'with origin {e(inst["repo_origin"])}, with an empty uv cache so nothing came from this machine.</p>'
            f'<h3>The files it wrote ({len(rec.get("files_written", {}))}; open one)</h3>{files}'
            f'<h3>The three hook entries it added</h3>{hook_html}'
            f'<h3>Checks on the result</h3><table class="stack"><thead><tr><th>What was checked</th><th>Should</th><th>Did</th>'
            f'<th>Result</th></tr></thead><tbody>{rows}</tbody></table></div>')


def data_table(rec: dict) -> str:
    out = decision_table(rec)
    paths = next((r for r in rec["rows"] if r["id"] == "paths"), None)
    if paths:
        items = "".join(f"<li><code>{e(k)}</code>: {v}</li>" for k, v in paths["per_pattern"].items())
        out += (f'<details><summary>Machine-path count by pattern ({len(paths["files_scanned"])} files scanned: '
                f'{e(", ".join(paths["files_scanned"]))})</summary><ul>{items}</ul></details>')
    checks = next((r for r in rec["rows"] if r["id"] == "checks"), None)
    if checks:
        items = "".join(f"<li><code>{e(k)}</code>: {e(v)}</li>" for k, v in checks["settings"].items())
        out += f'<details open><summary>Each check and its setting in lockstep.yaml</summary><ul>{items}</ul></details>'
    agent = rec.get("readme_agent")
    if agent:
        cost = agent.get("cost_usd")
        out += (f'<h3>The README-only agent</h3><div class="receipt">Model {e(agent["model"])}, {e(agent.get("num_turns"))} turns, '
                f'reported cost ${cost if cost is None else format(cost, ".4f")}. Origin of its repository: {e(agent["origin"])}. '
                f'Files it left: {e(", ".join(agent["files_written"]))}.<br>'
                f'<a href="{RAW}{e(agent["transcript"])}">The full transcript (stream-json)</a>'
                f'<details><summary>What the agent reported</summary><pre>{e(agent["agent_report"])}</pre></details></div>')
    return out


def pending(entry: str) -> str:
    return {"A1": '<div class="receipt">Receipt card, empty: the command that was typed, the files it wrote and the three '
                  'hook entries it added will appear here once the run exists.</div>',
            "A5": '<table><tr><th>Check or path</th><th>Setting or count</th><th>Result</th></tr>'
                  '<tr><td colspan="3">No rows yet: the portability run has not been made.</td></tr></table>'}.get(entry, "")


def extras(entry: str, rec: dict) -> str:
    out = ""
    probe = rec.get("arch_import_linter_probe")
    if entry == "A3" and probe:
        out += ('<details><summary>Extra evidence: a separate tool, run by hand on the forbidden-import commit</summary>'
                '<p class="meta">Not part of the result above. import-linter is the tool whose contracts the arch check '
                'writes; here it was run directly on the same commit.</p><pre>' + e(probe["stdout"]["text"]) + "</pre></details>")
    if entry == "A2":
        out += ('<p class="meta">The guard ran in "block" mode, the way lifelike\'s own settings run it. Lockstep\'s '
                'default mode only warns.</p>')
    if entry == "A4" and rec.get("approval"):
        out += (f'<p class="meta">Plan approved in commit {e(rec["approval"]["commit"][:9])} at '
                f'{e(rec["approval"]["committed_at"])}; the layout command ran after it.</p>')
    return out


def section(entry: str, spec: dict, rec: dict | None) -> str:
    view = spec["representation"]["view"]
    if rec and rec.get("rows"):
        body = {"decision-table": decision_table, "master-detail": master_detail,
                "answer-receipt-card": receipt_card, "data-table": data_table}[view](rec)
        body += extras(entry, rec)
        if rec.get("install", {}).get("unmerged_build"):
            body = ('<div class="verdict v-fail"><span class="why"><b>Run against an unmerged build.</b> This record installed Lockstep from '
                    'a local build that is not on the published address yet, so it is a dry run. The final run, against the '
                    'published address, replaces it.</span></div>') + body
        meta = (f'<p class="meta">Run at {e(rec["run_at"])} on Lockstep revision <code>{e(rec["lockstep_revision"][:12])}</code>.</p>')
        link = f'<p><a href="{RAW}{entry.lower()}.json">The raw run record (every command, input, exit code and output)</a></p>'
    else:
        body, meta = pending(entry), ""
        link = (f'<p class="meta">The record will be <code>docs/planning/runs/lockstep-acceptance/{entry.lower()}.json</code>.'
                f' <a href="{RAW}{entry.lower()}.json">Link to it on GitHub</a> (a missing page means not run yet).</p>')
    return (f'<section class="entry" id="{entry.lower()}"><h2>{entry}: {e(SHORT[entry])}</h2>'
            f'<div class="crit">{e(spec["criterion"])}</div><p>{e(EXPLAIN[entry])}</p>'
            f'{verdict_box(rec)}{meta}'
            f'<h3>What passing looks like</h3><p>{e(spec["expected"])}</p>'
            f'<h3>The rows</h3>{body}'
            f'<div class="broken"><b>This is what broken would look like.</b> {e(spec["failure_example"])}</div>{link}</section>')


def main() -> int:
    spec = {x["id"]: x for x in json.loads((ROOT / "docs/planning/acceptance-criteria.json").read_text())["entries"]}
    recs = {a: load(a) for a in ENTRIES}
    def state(a):
        r = recs[a]
        return "NOT RUN" if not r or not r.get("rows") else ("PASS" if all(x["pass"] for x in r["rows"]) else "FAIL")
    nav = "".join(f'<a href="#{a.lower()}">{a} {state(a)}</a>' for a in ENTRIES)
    counts = {k: sum(state(a) == k for a in ENTRIES) for k in ("PASS", "FAIL", "NOT RUN")}
    page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>Lockstep acceptance results</title><style>{CSS}</style></head><body><main>'
            f'<h1>Does Lockstep pass your acceptance entries?</h1>'
            f'<p>Each section below is one of your acceptance entries (A1 to A5), judged from a real run of the installed '
            f'Lockstep, not from a description of it. Right now: <b>{counts["PASS"]} pass (blue), {counts["FAIL"]} fail (orange), '
            f'{counts["NOT RUN"]} not run (grey)</b>. Every result is the words PASS, FAIL or NOT RUN, so colour is never the only signal.</p>'
            f'<div class="nav">{nav}</div>'
            f'<p class="legend meta">How to read a row: <b>Should</b> is what the plan says must happen. <b>Did</b> is what Lockstep actually did. '
            f'The program, not a person, compares the two and writes PASS or FAIL. <a href="index.html">Back to the plan review</a>.</p>'
            + "".join(section(a, spec[a], recs[a]) for a in ENTRIES) + '</main></body></html>\n')
    OUT.write_text(page)
    print(f"wrote {OUT} ({len(page)} bytes) " + " ".join(f"{a}={state(a)}" for a in ENTRIES))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

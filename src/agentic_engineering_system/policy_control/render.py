from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote

from .models import ReplayReportV1


def _source_url(report: ReplayReportV1) -> str:
    source = report.evaluator_input.source
    repository = quote(source.repository, safe="/")
    revision = quote(source.revision, safe="")
    path = quote(source.source_record, safe="/")
    return f"https://github.com/{repository}/blob/{revision}/{path}"


def render_report_html(report: ReplayReportV1) -> str:
    source = report.evaluator_input.source
    candidate = report.candidate
    usage = candidate.usage

    def esc(value: object) -> str:
        return html.escape("" if value is None else str(value))

    evidence_rows = "".join(
        "<tr>"
        f"<td>{esc(item.evidence_id)}</td>"
        f"<td>{esc(item.state.value)}</td>"
        f"<td>{esc(item.evidence_class)}</td>"
        f"<td>{esc(item.subject_scope)}</td>"
        f"<td>{esc(item.summary)}</td>"
        "</tr>"
        for item in report.evaluator_input.event_time_evidence
    )
    if not evidence_rows:
        evidence_rows = '<tr><td colspan="5">No event-time evidence rows.</td></tr>'

    later = (
        esc(report.later_outcome.summary)
        if report.later_outcome is not None
        else "No later outcome retained."
    )
    input_tokens = usage.input_tokens if usage else None
    output_tokens = usage.output_tokens if usage else None
    cost = usage.cost_usd if usage else None
    provider_error = ""
    if candidate.error_code:
        provider_error = (
            f"<p><strong>Provider error:</strong> {esc(candidate.error_code)} — "
            f"{esc(candidate.error_summary)}</p>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AES Plan 002 replay</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 1100px; margin: 2rem auto; padding: 0 1rem; line-height: 1.45; }}
table {{ border-collapse: collapse; width: 100%; margin: 1rem 0 2rem; }}
th, td {{ border: 1px solid #bbb; padding: .5rem; text-align: left; vertical-align: top; }}
code {{ overflow-wrap: anywhere; }}
.notice {{ border: 1px solid #888; padding: .75rem; }}
</style>
</head>
<body>
<h1>AES Plan 002 offline replay</h1>
<p><strong>Case:</strong> <code>{esc(report.evaluator_input.case_id)}</code></p>
<h2>Source</h2>
<ul>
<li>Repository: <code>{esc(source.repository)}</code></li>
<li>Revision: <code>{esc(source.revision)}</code></li>
<li>Session: <code>{esc(source.session_id)}</code></li>
<li>Transcript SHA-256: <code>{esc(source.transcript_sha256)}</code></li>
<li>Source record: <a href="{esc(_source_url(report))}"><code>{esc(source.source_record)}</code></a></li>
</ul>
<h2>Protected claim</h2>
<p>{esc(report.evaluator_input.claim_text)}</p>
<h2>Existing AES decision</h2>
<table>
<tr><th>Decision</th><th>Reason</th><th>Summary</th></tr>
<tr><td>{esc(report.baseline.decision.value)}</td><td>{esc(report.baseline.reason_code)}</td><td>{esc(report.baseline.summary)}</td></tr>
</table>
<h2>OpenRouter model judgment</h2>
<table>
<tr><th>State</th><th>Requested model</th><th>Response model</th><th>Judgment</th><th>Latency ms</th><th>Input tokens</th><th>Output tokens</th><th>Cost USD</th></tr>
<tr>
<td>{esc(candidate.state.value)}</td>
<td>{esc(candidate.requested_model)}</td>
<td>{esc(candidate.response_model)}</td>
<td>{esc(candidate.answer)}</td>
<td>{esc(candidate.latency_ms)}</td>
<td>{esc(input_tokens)}</td>
<td>{esc(output_tokens)}</td>
<td>{esc(cost)}</td>
</tr>
</table>
{provider_error}
<h2>Event-time evidence supplied to evaluator</h2>
<table>
<tr><th>ID</th><th>State</th><th>Class</th><th>Scope</th><th>Summary</th></tr>
{evidence_rows}
</table>
<h2>Later outcome — review only</h2>
<div class="notice">
<strong>This section was not supplied to the evaluator.</strong>
<p>{later}</p>
</div>
<h2>Evaluator-input identity</h2>
<p>SHA-256: <code>{esc(report.evaluator_input_sha256)}</code></p>
</body>
</html>
"""


def write_report_bundle(output_dir: Path, report: ReplayReportV1) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "replay.json"
    html_path = output_dir / "index.html"
    json_path.write_text(
        json.dumps(report.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    html_path.write_text(render_report_html(report), encoding="utf-8")
    return json_path, html_path

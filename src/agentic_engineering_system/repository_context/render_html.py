from __future__ import annotations

import html
import json
from pathlib import Path

from .models import RepositoryContextArtifact


def _state(value: object) -> str:
    return html.escape(str(value))


def render_html(artifact: RepositoryContextArtifact) -> str:
    def evidence_links(ids: tuple[str, ...]) -> str:
        if not ids:
            return "<span>none</span>"
        by_id = {item.evidence_id: item for item in artifact.evidence}
        links = []
        for evidence_id in ids:
            item = by_id.get(evidence_id)
            if item is None:
                links.append(f"<li>{html.escape(evidence_id)} (unresolved evidence reference)</li>")
                continue
            target = item.source_url or ""
            label = html.escape(item.path)
            if target:
                links.append(f'<li><a href="{html.escape(target, quote=True)}">{label}</a> @ <code>{html.escape(item.revision[:12])}</code></li>')
            else:
                links.append(f"<li>{label} @ <code>{html.escape(item.revision[:12])}</code></li>")
        return "<ul>" + "".join(links) + "</ul>"

    authorities = []
    for item in artifact.authorities:
        authorities.append(
            "<details>"
            f"<summary><strong>{html.escape(item.role.value)}</strong> — {_state(item.state)}</summary>"
            f"<p>{html.escape(item.summary)}</p>"
            f"<p>Locations: {html.escape(', '.join(item.locations) or 'none')}</p>"
            f"<div>Evidence: {evidence_links(item.evidence_refs)}</div>"
            "</details>"
        )

    concerns = []
    for item in artifact.concern_roots:
        concerns.append(
            f"<li><strong>{html.escape(item.concern)}</strong>: {_state(item.state)}"
            + (f" — <code>{html.escape(item.path)}</code>" if item.path else "")
            + "</li>"
        )

    unresolved = []
    for item in artifact.unresolved:
        unresolved.append(
            f"<li><strong>{html.escape(item.subject)}</strong>: {html.escape(item.reason)}"
            f"<div>Evidence: {evidence_links(item.evidence_refs)}</div></li>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Repository Context — {html.escape(artifact.repository_id)}</title>
<style>
body {{ font-family: system-ui, sans-serif; line-height: 1.5; max-width: 980px; margin: 2rem auto; padding: 0 1rem; }}
header, section {{ border: 1px solid #ccc; border-radius: .5rem; padding: 1rem; margin: 1rem 0; }}
code {{ word-break: break-word; }}
.state {{ font-weight: 700; }}
</style>
</head>
<body>
<header>
<h1>Repository context</h1>
<p><strong>Repository:</strong> <code>{html.escape(artifact.repository_id)}</code></p>
<p><strong>Revision:</strong> <code>{html.escape(artifact.revision)}</code></p>
<p><strong>Resolution:</strong> <span class="state">{html.escape(artifact.resolution_status.value)}</span></p>
</header>
<section>
<h2>Start here</h2>
<p><strong>Navigation:</strong> {html.escape(artifact.navigation.state.value)} — {html.escape(artifact.navigation.summary)}</p>
<p>Locations: <code>{html.escape(', '.join(artifact.navigation.locations) or 'none')}</code></p>
<div>Evidence: {evidence_links(artifact.navigation.evidence_refs)}</div>
</section>
<section>
<h2>Authority surfaces</h2>
{''.join(authorities) or '<p>No authority surfaces were observed.</p>'}
</section>
<section>
<h2>Concern roots</h2>
<ul>{''.join(concerns) or '<li>None observed.</li>'}</ul>
</section>
<section>
<h2>Unresolved or blocked</h2>
<ul>{''.join(unresolved) or '<li>None.</li>'}</ul>
</section>
<section>
<h2>Evidence</h2>
<ul>{''.join(f'<li><code>{html.escape(e.evidence_id)}</code> — {html.escape(e.path)} @ {html.escape(e.revision)}</li>' for e in artifact.evidence) or '<li>None.</li>'}</ul>
</section>
</body>
</html>
"""


def write_outputs(artifact: RepositoryContextArtifact, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "context.json"
    html_path = output_dir / "index.html"
    json_path.write_text(
        json.dumps(artifact.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    html_path.write_text(render_html(artifact), encoding="utf-8")
    return json_path, html_path

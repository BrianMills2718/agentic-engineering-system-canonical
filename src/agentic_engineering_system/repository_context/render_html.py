from __future__ import annotations

import html
from pathlib import Path

from .models import RepositoryContextArtifact


def _badge(state: str) -> str:
    return f'<span class="state state-{html.escape(state.lower())}">{html.escape(state)}</span>'


def render_html(artifact: RepositoryContextArtifact) -> str:
    authority_rows = []
    for item in artifact.authorities:
        locations = ", ".join(item.locations) if item.locations else "—"
        authority_rows.append(f"<tr><td>{html.escape(item.role.value)}</td><td>{_badge(item.state.value)}</td><td><code>{html.escape(locations)}</code></td><td>{html.escape(item.summary)}</td></tr>")
    unresolved = "".join(f"<li><strong>{html.escape(item.subject)}</strong>: {html.escape(item.reason)}</li>" for item in artifact.unresolved) or "<li>None</li>"
    evidence = "".join(f"<li><code>{html.escape(item.path)}</code> — {html.escape(item.note or '')}</li>" for item in artifact.evidence) or "<li>None</li>"
    next_place = artifact.navigation.locations[0] if artifact.navigation.locations else next((loc for a in artifact.authorities for loc in a.locations), "No resolved starting point")
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Repository context — {html.escape(artifact.repository_id)}</title>
<style>body{{font-family:system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;line-height:1.45;color:#1b1b1b}}code{{background:#f4f4f4;padding:.12rem .3rem;border-radius:.25rem}}table{{border-collapse:collapse;width:100%}}th,td{{text-align:left;border-bottom:1px solid #ddd;padding:.6rem;vertical-align:top}}.state{{font-weight:700;font-size:.8rem}}.state-observed{{color:#176b2c}}.state-none,.state-unresolved{{color:#8a5a00}}.state-error{{color:#a60000}}.notice{{padding:.8rem 1rem;background:#fff8df;border-left:4px solid #b47b00}}details{{margin:1rem 0}}</style></head><body>
<h1>Repository context</h1><p><strong>Repository:</strong> {html.escape(artifact.repository_id)}<br><strong>Revision:</strong> <code>{html.escape(artifact.revision)}</code><br><strong>Status:</strong> {_badge(artifact.resolution_status.value)}</p>
<h2>Start here</h2><p>{_badge(artifact.navigation.state.value)} {html.escape(artifact.navigation.summary)}</p><p><strong>Next legitimate place to deepen:</strong> <code>{html.escape(next_place)}</code></p>
<div class="notice"><strong>Authority rule:</strong> directory names alone do not establish semantic authority. In particular, a root <code>contracts/</code> directory is not universal contract authority without positive evidence.</div>
<h2>Authority surfaces</h2><table><thead><tr><th>Role</th><th>State</th><th>Location</th><th>Meaning</th></tr></thead><tbody>{''.join(authority_rows)}</tbody></table>
<h2>Unresolved / absent / error</h2><ul>{unresolved}</ul>
<details><summary>Evidence and exact source paths</summary><ul>{evidence}</ul></details>
<details><summary>Technical details</summary><p>This page is a non-authoritative projection of <code>RepositoryContextArtifact</code>. Use <code>context.json</code> for the deterministic machine-readable artifact.</p></details>
</body></html>"""


def write_surface(artifact: RepositoryContextArtifact, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "context.json"
    html_path = output_dir / "index.html"
    json_path.write_text(artifact.model_dump_json(indent=2), encoding="utf-8")
    html_path.write_text(render_html(artifact), encoding="utf-8")
    return json_path, html_path

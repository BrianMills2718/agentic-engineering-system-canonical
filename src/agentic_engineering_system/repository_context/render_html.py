from __future__ import annotations

import html
import json
from pathlib import Path

from .models import AuthorityRole, EpistemicState, RepositoryContextArtifact


def _state(value: object) -> str:
    return html.escape(str(value))


def _first_location(artifact: RepositoryContextArtifact, role: AuthorityRole) -> str | None:
    for item in artifact.authorities:
        if item.role is role and item.state is EpistemicState.OBSERVED and item.locations:
            return item.locations[0]
    return None


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
                links.append(
                    f'<li><a href="{html.escape(target, quote=True)}">{label}</a> '
                    f'@ <code>{html.escape(item.revision[:12])}</code></li>'
                )
            else:
                links.append(
                    f"<li>{label} @ <code>{html.escape(item.revision[:12])}</code></li>"
                )
        return "<ul>" + "".join(links) + "</ul>"

    def observed_card(role: AuthorityRole, heading: str, question: str) -> str:
        matches = [item for item in artifact.authorities if item.role is role]
        observed = next((item for item in matches if item.state is EpistemicState.OBSERVED), None)
        if observed is None:
            return (
                '<article class="card unresolved-card">'
                f"<p class=\"eyebrow\">{html.escape(question)}</p>"
                f"<h3>{html.escape(heading)}</h3>"
                "<p><strong>Not established from bounded evidence.</strong></p>"
                "<p>Do not guess from directory names. Deepen into repository-native sources if this matters to the task.</p>"
                "</article>"
            )
        locations = ", ".join(observed.locations) or "none"
        return (
            '<article class="card">'
            f"<p class=\"eyebrow\">{html.escape(question)}</p>"
            f"<h3>{html.escape(heading)}</h3>"
            f"<p class=\"location\"><code>{html.escape(locations)}</code></p>"
            f"<p>{html.escape(observed.summary)}</p>"
            f"<details><summary>Why AES says this</summary>{evidence_links(observed.evidence_refs)}</details>"
            "</article>"
        )

    navigation_location = ", ".join(artifact.navigation.locations) or "none"
    implementation_path = _first_location(artifact, AuthorityRole.IMPLEMENTATION)
    ownership_path = _first_location(artifact, AuthorityRole.OWNERSHIP)
    contract_path = _first_location(artifact, AuthorityRole.CONTRACT)

    route_steps: list[str] = []
    if artifact.navigation.state is EpistemicState.OBSERVED and artifact.navigation.locations:
        route_steps.append(
            f"<li><strong>Orient:</strong> start with <code>{html.escape(artifact.navigation.locations[0])}</code>. "
            "Use it to understand the repository's own framing before planning or editing.</li>"
        )
    if ownership_path:
        route_steps.append(
            f"<li><strong>Check ownership:</strong> use <code>{html.escape(ownership_path)}</code> "
            "when deciding what this repository owns versus what belongs elsewhere.</li>"
        )
    if contract_path:
        route_steps.append(
            f"<li><strong>For contract questions:</strong> deepen into <code>{html.escape(contract_path)}</code>; "
            "this is positively evidenced as the contract surface.</li>"
        )
    if implementation_path:
        route_steps.append(
            f"<li><strong>For implementation:</strong> inspect <code>{html.escape(implementation_path)}</code> "
            "after the authority/ownership context is clear.</li>"
        )
    if not route_steps:
        route_steps.append(
            "<li>No evidence-backed route is currently available. Treat the repository context as unresolved rather than guessing.</li>"
        )

    cautions: list[str] = []
    for item in artifact.concern_roots:
        if item.concern == "contracts-root" and item.state is EpistemicState.NONE:
            cautions.append(
                "<li><strong>Do not treat <code>contracts/</code> as repository-wide contract authority.</strong> "
                "Its presence is not positive semantic evidence.</li>"
            )
        elif item.concern == "wiki-navigation" and item.state is EpistemicState.NONE:
            cautions.append(
                "<li><strong>Do not route through a local wiki by assumption.</strong> "
                "No bounded root source established it as the navigation authority for this resolution.</li>"
            )
        else:
            path = f" <code>{html.escape(item.path)}</code>" if item.path else ""
            cautions.append(
                f"<li><strong>{html.escape(item.concern)}</strong>: {_state(item.state)}{path}</li>"
            )

    authority_details = []
    for authority in artifact.authorities:
        authority_details.append(
            "<details>"
            f"<summary><strong>{html.escape(authority.role.value)}</strong> — {_state(authority.state)}</summary>"
            f"<p>{html.escape(authority.summary)}</p>"
            f"<p>Locations: <code>{html.escape(', '.join(authority.locations) or 'none')}</code></p>"
            f"<div>Evidence: {evidence_links(authority.evidence_refs)}</div>"
            "</details>"
        )

    unresolved = []
    for surface in artifact.unresolved:
        unresolved.append(
            f"<li><strong>{html.escape(surface.subject)}</strong>: {html.escape(surface.reason)}"
            f"<div>Evidence: {evidence_links(surface.evidence_refs)}</div></li>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Repository Context — {html.escape(artifact.repository_id)}</title>
<style>
:root {{ color-scheme: light dark; }}
body {{ font-family: system-ui, sans-serif; line-height: 1.55; max-width: 1080px; margin: 2rem auto; padding: 0 1rem 4rem; }}
header, section {{ border: 1px solid color-mix(in srgb, currentColor 24%, transparent); border-radius: .75rem; padding: 1.25rem; margin: 1rem 0; }}
header {{ padding: 1.5rem; }}
h1, h2, h3 {{ line-height: 1.2; }}
h1 {{ margin-bottom: .35rem; }}
h2 {{ margin-top: 0; }}
code {{ word-break: break-word; }}
a {{ color: inherit; }}
.state {{ font-weight: 750; }}
.lede {{ font-size: 1.08rem; max-width: 75ch; }}
.meta {{ opacity: .78; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(235px, 1fr)); gap: .8rem; }}
.card {{ border: 1px solid color-mix(in srgb, currentColor 18%, transparent); border-radius: .65rem; padding: 1rem; }}
.card h3 {{ margin: .2rem 0 .45rem; }}
.eyebrow {{ font-size: .78rem; font-weight: 750; text-transform: uppercase; letter-spacing: .05em; opacity: .7; margin: 0; }}
.location {{ font-size: 1.03rem; }}
.route li, .cautions li {{ margin: .65rem 0; }}
.secondary {{ opacity: .88; }}
details {{ margin: .6rem 0; }}
summary {{ cursor: pointer; }}
</style>
</head>
<body>
<header>
<p class="eyebrow">Repository orientation</p>
<h1>{html.escape(artifact.repository_id)}</h1>
<p class="lede">This view answers the first repository questions from bounded, revision-bound evidence: where to begin, which surfaces carry authority, what not to infer, and where to deepen next.</p>
<p class="meta"><strong>Revision:</strong> <code>{html.escape(artifact.revision)}</code> · <strong>Resolution:</strong> <span class="state">{html.escape(artifact.resolution_status.value)}</span></p>
</header>
<section>
<h2>What you need to know first</h2>
<div class="grid">
<article class="card">
<p class="eyebrow">Where do I start?</p>
<h3>Repository entrypoint</h3>
<p class="location"><code>{html.escape(navigation_location)}</code></p>
<p>{html.escape(artifact.navigation.summary)}</p>
<details><summary>Why AES says this</summary>{evidence_links(artifact.navigation.evidence_refs)}</details>
</article>
{observed_card(AuthorityRole.OWNERSHIP, 'Ownership boundary', 'Where is ownership decided?')}
{observed_card(AuthorityRole.CONTRACT, 'Contract surface', 'Where do contract questions go?')}
{observed_card(AuthorityRole.IMPLEMENTATION, 'Implementation', 'Where does the code live?')}
</div>
</section>
<section>
<h2>Recommended route</h2>
<p class="secondary">Follow this order so implementation detail does not outrun repository authority and ownership context.</p>
<ol class="route">{''.join(route_steps)}</ol>
</section>
<section>
<h2>Do not infer</h2>
<p class="secondary">These are deliberate guardrails, not missing polish. AES preserves absence and uncertainty instead of turning plausible folder names into authority.</p>
<ul class="cautions">{''.join(cautions) or '<li>No explicit caution states were observed.</li>'}</ul>
</section>
<section>
<h2>Anything unresolved?</h2>
<ul>{''.join(unresolved) or '<li>No blocking or unresolved surfaces were reported for this bounded resolution.</li>'}</ul>
</section>
<section>
<details>
<summary><strong>Technical authority details and source evidence</strong></summary>
<p class="secondary">Use this when you need to audit how the orientation above was derived.</p>
{''.join(authority_details) or '<p>No authority surfaces were observed.</p>'}
<h3>All evidence</h3>
<ul>{''.join(f'<li><code>{html.escape(e.evidence_id)}</code> — {html.escape(e.path)} @ {html.escape(e.revision)}</li>' for e in artifact.evidence) or '<li>None.</li>'}</ul>
</details>
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

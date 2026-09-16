# Repository context provider landscape

Date: 2026-09-16
Status: current sourcing investigation
Capability requirement: `repository.context.resolve`

## Question

Before selecting an AES-local implementation or an internal donor as a runtime dependency, is there a stable platform, standard, mature open-source package, or mature service that already satisfies the first vertical's repository-context boundary?

The required behavior is narrower than general code intelligence and broader than reading one manifest: bind one repository to an exact revision, resolve declared/native navigation and authority surfaces without folder-name guessing, preserve unknown/error states, and retain evidence for each positive routing claim.

## Sourcing order

1. stable platform/native facilities;
2. standards and mature off-the-shelf implementations;
3. ACA-known providers;
4. internal repositories as evidence/design donors and provider candidates only when justified;
5. residual local implementation for semantics still missing.

## External candidates

| Candidate | Useful capability | Fit to `repository.context.resolve` | Disposition for Plan 001 |
| --- | --- | --- | --- |
| Git + GitHub repository APIs | repository identity, exact commit/revision, tree/file reads | strong substrate for identity/evidence; does not know AES authority roles | **compose as substrate candidate** |
| Sourcegraph + SCIP | language-agnostic precise code navigation, definitions/references/dependencies from uploaded indexes | strong future code-intelligence option; does not resolve normative/decision/plan/navigation authority and is unnecessary for the first read-only routing slice | **defer** |
| Tree-sitter | incremental concrete syntax trees and source positions across many languages | useful future anchoring/characterization primitive; no repository authority semantics | **defer** |
| Backstage Software Catalog | declared software metadata, ownership and entity relations from catalog descriptors | useful catalog/ownership model, but requires its own catalog declarations and does not provide exact-revision repo-local AES authority resolution | **do not select as Plan 001 provider** |
| OpenRewrite | lossless semantic trees, scanning recipes, Git provenance markers, source transformation | useful for large-scale source scanning/refactoring; substantially broader and mutation-oriented relative to this read-only context boundary | **defer** |
| GitHub CodeQL | source database plus query/analysis results | mature static-analysis substrate, primarily security/query oriented and too heavy for the first authority-routing slice | **do not select for Plan 001** |

Sources consulted:
- Sourcegraph precise code navigation / SCIP: https://sourcegraph.com/docs/code-navigation/precise-code-navigation
- Tree-sitter: https://tree-sitter.github.io/tree-sitter/
- Backstage Software Catalog: https://backstage.io/docs/features/software-catalog/
- OpenRewrite recipes/scanning: https://docs.openrewrite.org/concepts-and-explanations/recipes
- GitHub CodeQL database analysis: https://docs.github.com/en/code-security/reference/code-scanning/codeql/codeql-cli-manual/database-analyze

## ACA result

The separate ACA investigation found no verified semantic export matching `repository.context.resolve`.

## Internal donors are not selected providers

Internal repositories remain useful evidence/design donors:

- `code_map_v4` demonstrates revision-bound evidence, source anchoring, freshness/invalidation, explicit epistemic state, and independent-evaluation lessons;
- Enforced Planning demonstrates repository context delivery and execution governance patterns;
- Project Meta demonstrates authority/projection and policy machinery;
- prior AES lineages demonstrate recovery-bearing controls and negative-control discipline.

None is selected as a runtime dependency merely because it contains a useful mechanism.

## Provider conclusion

No reviewed off-the-shelf candidate supplies the complete semantic boundary needed by Plan 001.

The likely first-vertical shape is therefore **composition plus a small AES-specific residual**:

- reuse native Git/GitHub capabilities for repository identity, exact revision, and source retrieval;
- use ordinary stable parsing/validation libraries for declared manifest formats rather than inventing parsers;
- implement only the residual authority-resolution semantics needed to map explicit declarations and bounded legacy evidence into `RepositoryContextArtifact`;
- do not introduce a generalized symbol index, repository crawler, code graph, generated wiki engine, or characterization kernel unless a later gap independently requires it.

This conclusion justifies residual semantics, not a concrete package/file topology. Company Planning must still derive the smallest outcome-bearing slice and exact implementation/verification subjects.

## Reconsideration triggers

Re-run sourcing if:

- ACA gains an equivalent verified action;
- a stable tool gains explicit repository authority/navigation semantics that match the boundary;
- the first vertical requires symbol-level code intelligence or dependency-aware source anchoring;
- the residual grows beyond bounded authority resolution into generalized indexing or analysis.

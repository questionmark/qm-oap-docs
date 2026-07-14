# ai-docs — how this repo verifies OData documentation

`qm-oap-docs` is documentation-only: it describes the public OAP integration APIs
but does not implement them. This folder captures **how we keep those docs correct
against the services**, so the process is repeatable and does not rot.

It complements the contributor-facing `AGENTS.md` (workflow rules) and `README.md`
(repo overview / build) at the repository root.

## What lives where

| Path | Contents |
|------|----------|
| [`adrs/`](adrs/README.md) | Architecture Decision Records — *why* the verification approach is what it is. |
| [`rails/`](rails/README.md) | Operational guardrails — *how* to run the recurring work safely. |
| [`../ai-scripts/`](../ai-scripts/README.md) | The reconciliation tooling (parsers, reconciler, baseline fetcher). |

## The model in one paragraph

The service code is the source of truth; the documentation is a *description of the
contract* (ADR-0001). For OData, each service emits machine-readable CSDL at
`GET .../$metadata`, which we treat as the primary contract. The `ai-scripts/`
tooling diffs that `$metadata` against the `od:` directives in `src/` and reports
drift (ADR-0002). Structural facts (feeds, types, properties, keys, action
params/return types) are checked automatically; behaviour that metadata cannot
express (`:filter:`, HTTP methods, metadata-omitted return types) is verified in a
manual controller-code pass. Genuine code/metadata mismatches are service bugs
raised with the owning team, not docs to degrade (ADR-0004).

## Services at a glance

| Service | OData | Docs | Strategy |
|---------|-------|------|----------|
| Delivery | v3 | `src/deliveryodata/` | `od:` directives |
| Authoring | v4 | `src/authoringodata/` | `od:` directives |
| Results | v3 | `src/resultsodata.rst` | Help Center redirect (ADR-0003) |

Full endpoints, source repos, and owning teams: `rails/service-inventory.md`.

## Common tasks

- **Run a reconciliation check:** `rails/reconciliation-workflow.md`.
- **Edit `od:` directives correctly:** `rails/editing-od-directives.md`.
- **Understand a past decision:** `adrs/`.

## Decision log

| ADR | Title |
|-----|-------|
| [0001](adrs/0001-docs-follow-code.md) | Docs follow code; `$metadata` is the contract |
| [0002](adrs/0002-reconciliation-tooling.md) | Namespace-agnostic CSDL-vs-RST reconciliation tooling |
| [0003](adrs/0003-results-odata-help-redirect.md) | Results OData docs redirect to the Help Center |
| [0004](adrs/0004-getaccessurl-return-type-bug.md) | Handling the `GetAccessUrl` metadata return-type gap |

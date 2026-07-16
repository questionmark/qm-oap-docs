# Architecture Decision Records (ADRs)

Short, immutable records of the significant decisions behind how this
documentation repository is verified and maintained. Each ADR captures the
context, the decision, and its consequences at a point in time. Superseding a
decision means adding a new ADR, not editing an old one.

| ADR | Title | Status |
|-----|-------|--------|
| [0001](0001-docs-follow-code.md) | Docs follow code; `$metadata` is the contract | Accepted |
| [0002](0002-reconciliation-tooling.md) | Namespace-agnostic CSDL-vs-RST reconciliation tooling | Accepted |
| [0003](0003-results-odata-help-redirect.md) | Results OData docs redirect to the Help Center | Accepted |
| [0004](0004-getaccessurl-return-type-bug.md) | Handling the `GetAccessUrl` metadata return-type gap | Accepted |

## Format

Each ADR uses the same lightweight structure:

- **Status** — Proposed / Accepted / Superseded (by ADR-N).
- **Context** — the forces and facts that make a decision necessary.
- **Decision** — what we decided to do.
- **Consequences** — the resulting trade-offs, good and bad.

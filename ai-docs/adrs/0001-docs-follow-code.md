# ADR-0001: Docs follow code; `$metadata` is the contract

**Status:** Accepted

## Context

`qm-oap-docs` is a documentation-only repository. It *describes* public
integration APIs but does not implement them; the services live in their own
repositories (`qm-DeliveryOData`, `qm-AuthoringApi`, and the Results/analytics
service). When the documentation and the service disagree, one of them is wrong.

For OData services the emitted CSDL/EDMX (`GET .../$metadata`) is a
machine-readable description of the actual contract: entity sets, types,
properties, keys, and actions. It is generated from the running service, so it
cannot silently drift from what the service exposes.

## Decision

Treat the service code as the source of truth and the documentation as a
*description of the contract*. Concretely:

- When docs and code disagree, **change the docs to match the code**, unless we
  are explicitly told the code is wrong.
- Use `$metadata` as the primary, machine-readable contract for structural facts
  (feeds, types, properties, keys, actions, params, return types).
- Use the service **controllers** (`Controllers/*.cs`) as the final authority for
  behaviour that metadata cannot express (filterable properties, HTTP methods,
  and return types the metadata omits).
- A genuine code/metadata mismatch is a **service** change, not a docs change,
  and is raised with the owning team rather than papered over in the docs.

## Consequences

- Documentation edits are objective and verifiable against a concrete artifact,
  which enables the automated reconciliation in ADR-0002.
- Some real problems surface as "the code looks wrong" (e.g. ADR-0004). These are
  escalated to the owning team; the docs describe the intended contract with a
  note, rather than inventing behaviour.
- Owning teams: Delivery OData → **Delivery QM / Firestar**; Authoring OData →
  **Team Aurora**. See `ai-docs/rails/service-inventory.md`.

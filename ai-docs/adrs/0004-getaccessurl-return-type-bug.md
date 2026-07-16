# ADR-0004: Handling the `GetAccessUrl` metadata return-type gap

**Status:** Accepted

## Context

The Delivery OData action `Administrator.GetAccessUrl` returns an access URL
string at runtime, and the documentation correctly describes a `String` return
type. However, the service's `$metadata` declares **no return type** for the
action. The reconciliation tool reports this as:

```
[RETURN MISMATCH] GetAccessUrl: docs=String code=None
```

This is not documentation drift — the docs describe the true, intended behaviour.
It is a **service-side metadata bug**: the action's return type is missing from
the emitted CSDL. Several other Delivery actions show the same class of gap where
metadata under-declares what the controller actually returns.

## Decision

- Keep the documented `String` return type for `GetAccessUrl`; do **not** "correct"
  the docs to match the incomplete metadata.
- Treat this as a code/metadata defect owned by **Delivery QM / Firestar** and
  raise it with them (per ADR-0001, genuine mismatches are service changes).
- Where the controller confirms the real return type, the docs stay accurate and
  a note may be added; the tool's `[RETURN MISMATCH] ... code=None` findings for
  this class are triaged as "service metadata gap", not docs fixes.

## Consequences

- The reconciliation report for Delivery will keep showing `code=None`
  return-type findings until the service metadata is fixed; these are knowingly
  accepted, not silenced.
- This is exactly why ADR-0002 keeps the tool structural-only and mandates a
  controller-code pass: metadata alone would push us to *remove* correct docs.
- The controller-code pass is the authority for return types the metadata omits.

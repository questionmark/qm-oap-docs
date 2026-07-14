# Proposed fixes

Reviewed, source-verified corrections for the OData documentation, produced by the
reconciliation workflow (see [`../rails/reconciliation-workflow.md`](../rails/reconciliation-workflow.md)).

These documents are a **review gate**. They record every reconciliation finding, its
classification, and the exact before/after RST edit *before* any `.rst` file is
touched. Nothing here is applied until the owning reviewer approves.

## Files

| File | Service | Source of truth | Status |
|------|---------|-----------------|--------|
| [`delivery.md`](delivery.md) | Delivery OData (v3) | `qm-DeliveryOData` | Ready for review |
| `authoring.md` | Authoring OData (v4) | `qm-AuthoringApi` | Pending (Phase 3) |

Results OData is intentionally excluded: it is documented via a redirect to the Help
Center, not `od:` directives (see [`../adrs/0003-results-odata-help-redirect.md`](../adrs/0003-results-odata-help-redirect.md)).

## Classification legend

Every finding is tagged with who is wrong, which decides whether we edit the docs or
raise a service ticket (per [`../adrs/0001-docs-follow-code.md`](../adrs/0001-docs-follow-code.md)):

| Tag | Meaning | Action |
|-----|---------|--------|
| **DOC** | Docs disagree with the emitted metadata (docs wrong) | Edit the `.rst` |
| **DOC-ADD** | Contract exists in metadata but is undocumented | Add to the `.rst` |
| **SVC** | Metadata is wrong/incomplete vs. the controller code (service bug) | Keep docs, raise with owning team |
| **LAG** | Contract is valid in code but absent from the captured tenant baseline (deployment lag) | Keep docs, re-verify after redeploy |

Only **DOC** and **DOC-ADD** result in `.rst` edits. **SVC** and **LAG** are recorded
so the docs are *not* "corrected" to match a buggy or stale metadata snapshot.

# ADR-0002: Namespace-agnostic CSDL-vs-RST reconciliation tooling

**Status:** Accepted

## Context

Manual, name-only review of the OData docs missed real drift: undocumented
properties, a stray-quote type (`Edm.Boolean"`), casing mismatches
(`CurrentUtcTime` vs `CurrentUTCTime`), and action return-type gaps. We needed a
re-runnable, directive-level check that compares the docs against `$metadata`.

Two complications:

1. **Two OData versions.** Delivery and Results are OData **v3** (actions appear
   as `FunctionImport`, edm namespace `.../2009/11/edm`). Authoring is OData **v4**
   (`Action`/`Function`, edm namespace `docs.oasis-open.org/odata/ns/edm`).
2. **Bound-action noise.** Bound actions always carry an implicit
   `bindingParameter` in `$metadata` that the docs intentionally omit from
   `:input:`. A naive param diff flags every bound action.

## Decision

Build a small, standard-library-only Python toolchain in `ai-scripts/`:

- `edmx_parser.py` matches elements by **local tag name** (namespace-stripped),
  so a single code path handles v3 and v4. Actions are collected from `Action`,
  `Function`, and `FunctionImport`.
- `rst_parser.py` extracts `od:feed` / `od:type` / `od:prop` / `od:action`
  directives into a mirror-image inventory.
- `reconcile_odata.py` diffs the two and reports categorized findings; it ignores
  `bindingParameter` in the param comparison to remove the known noise.
- `fetch_baselines.ps1` snapshots each service's `$metadata` into
  `ignore/metadata-baselines/` for offline, repeatable runs.

## Consequences

- Reconciliation is repeatable and diffable; `--fail-on-diff` allows CI gating.
- The tool is deliberately **structural only**. It cannot verify `:filter:`,
  HTTP methods, or metadata-omitted return types — those need the controller
  pass (see ADR-0001 and `ai-scripts/README.md` "Coverage limits").
- Validation run (2026-07-13): every reported finding was confirmed as real
  drift, not a parser artifact, after filtering `bindingParameter`.
- Optional future hardening: generate OpenAPI from `$metadata` and diff against a
  stored baseline with `oasdiff` for continuous drift detection.

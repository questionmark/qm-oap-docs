# Rail: editing `od:` directives

The custom `od` domain is defined in `src/qmdomain.py`. Use only these directives;
do not invent new ones.

| Directive | Use |
|-----------|-----|
| `.. od:service:: <service>` | Once per product page. |
| `.. od:feed:: <EntitySetName> <Type>` | The queryable feed (`:method:`, `:filter:`). |
| `.. od:type:: <Type>` | Entity / complex type definition. |
| `.. od:prop:: <Name> <EdmType>` | Property; flags `:key:`, `:notnull:`, `:collection:`. |
| `.. od:action:: <Name> <ReturnType>` | Action; `:input: P1 Type, P2 Type` for params. |

Reference them with roles `:od:feed:`, `:od:type:`, `:od:prop:`, `:od:action:`.

## Names are case- and spelling-sensitive

The Delivery service runs on `System.Web.Http.OData` v5.x, where URL segment
resolution is **case-sensitive and exact** (case-insensitive routing only arrived
in WebAPI OData v7). Therefore:

- `TimeZones` will **404** if the code registers `Timezones`.
- `SessionAuditLog` (singular) will **404** if the entity set is
  `SessionAuditLogs`.

Copy feed, type, and property names **verbatim** from `$metadata` / the service
code. The reconciler catches casing drift (e.g. `CurrentUtcTime` vs
`CurrentUTCTime`, `AttemptID` vs `AttemptId`).

## A feed only exists when it is defined

A feed is a contract only when it has its own `.. od:feed::` directive. A
hyperlink in `feeds.rst` or a toctree entry is **not** a feed definition. Every
defined feed must also be listed in the product index (`feeds.rst`) so it is
discoverable.

## Composite keys

Mark **all** parts of a composite key with `:key:`. For example a type keyed on
`{ID, Language}` must flag both `ID` and `Language`. A half-marked key is a
common, easy-to-miss drift.

## Property types

- The `od:prop` EDM type must match `$metadata` exactly (e.g. `Edm.DateTimeOffset`
  not `Edm.String`).
- Watch for copy/paste typos such as a trailing quote: `Edm.Boolean"`.
- Navigation properties reference the target **type name** (e.g.
  `RulesOfConduct`), never a fabricated `Edm.<TypeName>`.

## Actions

- `<ReturnType>` and `:input:` must match the service. The implicit
  `bindingParameter` on bound actions is **not** documented in `:input:` (the
  reconciler ignores it).
- If metadata omits a return type the controller genuinely returns, keep the
  documented type and raise a service bug (ADR-0004) — do not delete it.

## Before committing

- `make docs` (or `sphinx-build -b html src docs`) with **zero** warnings.
- Unresolved `:od:type:` / `:od:feed:` cross-references indicate a broken or
  misnamed reference — fix before committing.
- Keep diffs minimal; preserve existing anchors so external links stay stable.

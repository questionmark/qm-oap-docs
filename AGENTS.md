# AI Agent Guidelines for qm-oap-docs

Guidance for AI agents and contributors editing the Questionmark Open Assessment
Platform (OAP) API documentation.

This repository is **documentation only**. It describes public integration APIs but
does not implement them; the services live in their own repositories. For repository
purpose, structure, and build instructions, see [README.md](README.md).

---

## Golden rule: docs follow code

The documentation is a **contract description**; the service code is the source of
truth. When docs and code disagree, **change the docs to match the code** unless
explicitly told the code is wrong. A genuine code mismatch is a service change, not a
docs change, and must be raised with the owning team (Delivery QM / Firestar).

For Delivery OData the authoritative sources in `qm-DeliveryOData` are:

| Aspect | Source of truth |
|--------|-----------------|
| Feed (entity set) names | `App_Start/ODataConfig.cs` (`ConfigureEntitySets`) |
| Type properties and keys | `QM.Delivery.ODataService.Entity/*.cs` + DAL `EntityMappings/*.cs` |
| Bound/unbound actions | `ODataConfig.cs` + `Controllers/*.cs` |

---

## OData names are case- and spelling-sensitive

The Delivery service runs on `System.Web.Http.OData` v5.x, where URL segment
resolution is **case-sensitive and exact** (case-insensitive routing only arrived in
WebAPI OData v7). Consequences:

- A feed documented as `TimeZones` will **404** if the code registers `Timezones`.
- `SessionAuditLog` (singular) will **404** if the entity set is `SessionAuditLogs`.

Always copy feed, type, and property names **verbatim** from the code.

---

## Custom `od` domain (defined in `src/qmdomain.py`)

Document OData entities with these directives - do not invent new ones:

- `.. od:service:: <service>` - once per product page
- `.. od:feed:: <EntitySetName> <Type>` - the queryable feed (`:method:`, `:filter:`)
- `.. od:type:: <Type>` - entity / complex type definition
- `.. od:prop:: <Name> <EdmType>` - flags `:key:`, `:notnull:`, `:collection:`
- `.. od:action:: <Name> <ReturnType>` - `:input: P1 Type, P2 Type` for parameters

Reference them with the roles `:od:feed:`, `:od:type:`, `:od:prop:`, `:od:action:`.

A feed only exists as a contract when it has its own `.. od:feed::` directive. A
hyperlink in `feeds.rst` or a toctree entry is **not** a feed definition.

---

## Verification workflow (directive-level, not name-only)

1. List registered entity sets and actions from `ODataConfig.cs` in the code repo.
2. Extract every directive from the relevant `src/<product>/*.rst` files, e.g.:
   `Select-String -Path src\deliveryodata\*.rst -Pattern '^\s*\.\.\s+od:(feed|type|prop|action)::'`
3. Compare *definitions* (not link text): every entity set has an `od:feed`; every
   documented `od:prop` exists on the entity; composite keys mark **all** key parts
   with `:key:` (for example `ID` plus `Language`).
4. Ensure each defined feed is also listed in the product index (`feeds.rst`) so it
   is discoverable.

---

## Optional: automated regression

For ongoing drift detection, generate OpenAPI from the live `$metadata`
(`GET .../deliveryodata/<tenant>/$metadata`) with a converter such as
`Microsoft.OpenAPI.OData.Reader` or `odata-openapi`, then diff against a stored
baseline using `oasdiff`. This catches naming, property, and action drift that manual
review can miss.

---

## Build and check before committing

- Build locally: `make docs` (or `sphinx-build -b html src docs`).
- Resolve all warnings - unresolved `:od:type:` / `:od:feed:` cross-references mean a
  broken or misnamed reference.
- Keep diffs minimal and scoped; preserve existing anchors and cross-references so
  external links remain stable.

---

## Working branch

Active Delivery OData documentation gap work is on branch
`feature/add-missing-delivery-odata-feeds`.

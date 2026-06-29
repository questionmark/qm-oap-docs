# qm-oap-docs

Source for the **Questionmark Open Assessment Platform (OAP) API documentation**.
These pages document Questionmark's public integration APIs and are published as a
static Sphinx site to GitHub Pages.

- Live site: https://questionmark.github.io/qm-oap-docs/
- Delivery OData: https://questionmark.github.io/qm-oap-docs/deliveryodata.html

This repository is **documentation only**. The APIs it describes are implemented in
their own service repositories (for Delivery OData that is `qm-DeliveryOData`).

## What is documented

| Area | Source | Notes |
|------|--------|-------|
| Overview / data model | `src/overview.rst`, `src/data_model.rst`, `src/model/` | Platform concepts and shared data model |
| OData (general) | `src/odata.rst` | Common OData conventions |
| Authoring OData | `src/authoringodata.rst`, `src/authoringodata/` | Authoring API feeds/types |
| Delivery OData | `src/deliveryodata.rst`, `src/deliveryodata/` | Delivery API feeds/types/actions |
| Results OData | `src/resultsodata.rst` | Results API |
| QMWISe (SOAP) | `src/qmwise.rst`, `src/qmwise/` | Legacy SOAP API |
| Python client | `src/pip.rst` | pip-installable client notes |

## Repository layout

```
src/
  conf.py            Sphinx configuration (project: QuestionmarkAPIs)
  qmdomain.py        Custom Sphinx domains: od (OData) and qm (QMWISe/SQL)
  index.rst          Master toctree
  *.rst              Per-product top-level pages
  deliveryodata/     Delivery OData feed/type/action pages (.rst)
  authoringodata/    Authoring OData pages
  qmwise/            QMWISe pages
  model/             Data model pages
docs/                Generated HTML output (published to GitHub Pages)
```

## Building the docs

Requires Python with Sphinx and the Alabaster theme:

```bash
pip install sphinx alabaster
```

Build the HTML site (output to `docs/`):

```bash
make docs            # runs: sphinx-build -b html src docs/
```

On Windows without `make`, build directly:

```powershell
sphinx-build -b html src docs
```

Resolve Sphinx build warnings before publishing - an unresolved `:od:type:` or
`:od:feed:` cross-reference indicates a broken or misnamed link.

## Custom OData markup (`od` domain)

OData entities are documented with directives defined in `src/qmdomain.py`:

| Directive | Purpose |
|-----------|---------|
| `.. od:service::` | Declares the OData service for a page |
| `.. od:feed::` | An entity set (URL-addressable feed) |
| `.. od:type::` | An entity / complex type |
| `.. od:prop::` | A property of a type (flags: `:key:`, `:notnull:`, `:collection:`) |
| `.. od:action::` | A bound/unbound action (`:input:` for parameters) |

Cross-reference roles: `:od:feed:`, `:od:type:`, `:od:prop:`, `:od:action:`.

## Source of truth

The Delivery OData contract is **defined by the service code**, not by these docs.
When documenting or correcting Delivery OData, the authoritative source is the
`qm-DeliveryOData` repository - primarily:

- `solutions/src/QM.Delivery.ODataService/App_Start/ODataConfig.cs` (entity sets + actions)
- `solutions/src/QM.Delivery.ODataService.Entity/*.cs` (properties + keys)
- `solutions/src/QM.Delivery.ODataService/Controllers/*.cs` (actions)

See [AGENTS.md](AGENTS.md) for the contribution and verification workflow.

## Feedback

developer@questionmark.com or open an issue on the
[GitHub project](https://github.com/questionmark/qm-oap-docs).

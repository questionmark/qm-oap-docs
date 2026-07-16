# ai-scripts — OData documentation reconciliation tooling

Re-runnable tooling that checks the OData documentation in `src/` against each
service's **live `$metadata`** (the machine-readable contract). It implements the
"docs follow code" golden rule from `AGENTS.md`: `$metadata` is the source of truth,
and any drift is a docs bug to fix (unless it is a genuine service bug, which is
raised with the owning team).

> These scripts are tooling only. They are outside `src/`, so they are never part of
> the published Sphinx build.

## Files

| File | Purpose |
|------|---------|
| `edmx_parser.py` | Parses CSDL/EDMX (`$metadata`) into a normalized inventory. Namespace-agnostic: one code path handles OData **v3** (`FunctionImport`) and **v4** (`Action`/`Function`). |
| `rst_parser.py` | Extracts `od:feed` / `od:type` / `od:prop` / `od:action` directives from the `src/<product>/*.rst` docs into a matching inventory. |
| `reconcile_odata.py` | Diffs the two inventories and prints a findings report. Handles feeds, entity/complex types, properties (incl. `:key:` flags and scalar type mismatches), and actions (params + return types). |
| `fetch_baselines.ps1` | Downloads live `$metadata` for all three services into `ignore/metadata-baselines/`. |

## Quick start

```powershell
# 1. Refresh the $metadata baselines (writes ignore/metadata-baselines/*.xml)
pwsh ai-scripts/fetch_baselines.ps1

# 2. Reconcile each product against its baseline (UTF-8 report via --out)
python ai-scripts/reconcile_odata.py `
    --metadata ignore/metadata-baselines/delivery.<date>.metadata.xml `
    --rst-dir src/deliveryodata --product Delivery --out ignore/recon-reports/delivery.txt

python ai-scripts/reconcile_odata.py `
    --metadata ignore/metadata-baselines/authoring.<date>.metadata.xml `
    --rst-dir src/authoringodata --product Authoring --out ignore/recon-reports/authoring.txt
```

`--metadata` also accepts a live URL directly, so a network run needs no baseline:

```powershell
python ai-scripts/reconcile_odata.py `
    --metadata "https://ondemand.questionmark.com/deliveryodata/406611/$metadata" `
    --rst-dir src/deliveryodata --product Delivery
```

Add `--fail-on-diff` to make the script exit non-zero when any finding is reported
(useful for CI / pre-commit gating).

## Reading the report

Each finding is one line prefixed with a category tag:

| Tag | Meaning |
|-----|---------|
| `[MISSING IN DOCS]` | Present in `$metadata`, absent from the RST. |
| `[EXTRA IN DOCS]` | Present in the RST, absent from `$metadata`. |
| `[TYPE MISMATCH]` | Property type (scalar or nav target) differs; also flags `Edm.`-prefixed nav targets. |
| `[KEY NOT MARKED]` / `[KEY EXTRA]` | Key membership disagrees between code and docs. |
| `[NOTNULL MISSING]` / `[NOTNULL EXTRA]` | `:notnull:` disagrees with metadata `Nullable`. Triage NOTNULL EXTRA against the service before editing — v3 metadata derives nullability from CLR types and `[Required]` only, so mapping/validator-enforced requiredness shows as nullable (service under-declaration, not doc drift). |
| `[COLLECTION MISMATCH]` | `:collection:` disagrees with metadata cardinality (v3: Association End multiplicity; v4: `Collection(...)`). |
| `[RETURN MISMATCH]` | Action return type differs. |
| `[PARAM MISMATCH]` | Action parameter *names* differ (implicit `bindingParameter` is ignored). |
| `[PARAM TYPE MISMATCH]` | A shared parameter's EDM type differs. |
| `[BINDING MISMATCH]` | Action exists on both sides but is documented under a different type than it is bound to. |

Actions are matched by **(binding type, name)** — the binding comes from the
`bindingParameter` in metadata and from the enclosing `od:type`/`od:feed` in the
docs — so same-named actions on different types (Delivery has two `Upsert`, two
`ActionableSchedules`, two `CheckPassword`) are compared independently.

## Coverage limits (require the controller-code pass)

`$metadata` cannot express everything the docs describe. The following must be
verified against the service controllers (`Controllers/*.cs`), **not** this tool:

- `:filter:` — which properties are actually filterable.
- Supported HTTP methods per feed (GET / POST / PATCH / DELETE).
- Action **return types** when the service omits them from metadata
  (e.g. the known `GetAccessUrl` bug: docs say `String`, metadata says none).
- Prose accuracy, examples, and descriptions.

## Fixed blind spots (2026-07-14 tool upgrade)

Four structural blind spots found during the 2026-07-14 verification pass (see
`ai-docs/proposed-fixes/delivery.md` sections G/H for the findings each masked)
are now **covered by the tool**:

- Duplicate action names no longer collide — actions are keyed by
  (binding type, name) on both sides.
- Parameter EDM types are compared (`[PARAM TYPE MISMATCH]`).
- v3 nav-prop targets and cardinality are resolved through `Association`
  ends (`[TYPE MISMATCH]` / `[COLLECTION MISMATCH]`), including detection of
  bogus `Edm.`-prefixed nav targets that namespace-stripping used to hide.
- Nullability is diffed (`[NOTNULL MISSING]` / `[NOTNULL EXTRA]`).

The report grew accordingly (Delivery 37 → 78 findings on the same baseline);
every added finding was triaged as real on 2026-07-14 — zero false positives.

## Requirements

- Python 3.9+ (standard library only — no third-party packages).
- PowerShell (for `fetch_baselines.ps1`); or fetch `$metadata` any other way.

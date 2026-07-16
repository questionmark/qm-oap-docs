# Rail: reconciliation workflow

How to check the docs against a service and fix any drift. Runs the tooling
described in `ai-scripts/README.md` and ADR-0002.

## 1. Refresh the `$metadata` baselines

```powershell
pwsh ai-scripts/fetch_baselines.ps1
```

Writes `ignore/metadata-baselines/<service>.<date>.metadata.xml` for delivery
(v3), authoring (v4), and results (v3). `ignore/` is outside `src/`, so baselines
never enter the Sphinx build.

## 2. Run the reconciler per product

```powershell
python ai-scripts/reconcile_odata.py `
    --metadata ignore/metadata-baselines/delivery.<date>.metadata.xml `
    --rst-dir src/deliveryodata --product Delivery `
    --out ignore/recon-reports/delivery.txt

python ai-scripts/reconcile_odata.py `
    --metadata ignore/metadata-baselines/authoring.<date>.metadata.xml `
    --rst-dir src/authoringodata --product Authoring `
    --out ignore/recon-reports/authoring.txt
```

Always use `--out` so the report is written as UTF-8. Piping through PowerShell
`Tee-Object`/redirection produces UTF-16, which renders as spaced-out characters.

Results is expected to report all 14 feeds as "missing in docs" — that is the
intended redirect stub, not a defect (ADR-0003).

## 3. Triage findings

Work top-down through the report tags:

- `[MISSING IN DOCS]` — add the missing feed/type/property/action, copying names
  and types verbatim from `$metadata`.
- `[EXTRA IN DOCS]` — the docs describe something the service does not expose;
  remove it, or confirm it is a casing/spelling error (e.g. `AttemptID` vs
  `AttemptId`, `CurrentUtcTime` vs `CurrentUTCTime`).
- `[TYPE MISMATCH]` — correct the `od:prop` EDM type (watch for typos such as a
  stray quote: `Edm.Boolean"`, and `Edm.`-prefixed nav targets, which must be
  bare type names).
- `[KEY NOT MARKED]` / `[KEY EXTRA]` — align `:key:` flags; mark **all** parts of
  a composite key.
- `[NOTNULL MISSING]` — add `:notnull:` (metadata says `Nullable="false"`).
- `[NOTNULL EXTRA]` — do **not** blindly remove `:notnull:`. v3 metadata derives
  nullability from CLR types and `[Required]` only; requiredness enforced via EF
  mappings or validators shows as nullable. Check the entity/mapping/validator —
  if the service never accepts null, keep the flag and raise a service ticket
  (metadata under-declares).
- `[COLLECTION MISMATCH]` — align `:collection:` with the metadata cardinality.
- `[RETURN MISMATCH]` / `[PARAM MISMATCH]` / `[PARAM TYPE MISMATCH]` — verify
  against the controller before editing. If metadata omits a return type the
  controller really returns, it is a **service bug** (ADR-0004), not a docs fix.
- `[BINDING MISMATCH]` — the action is documented under a different type than
  its metadata binding; move it (or its context) rather than duplicating it.

## 4. Controller-code pass (what metadata cannot verify)

From the service `Controllers/*.cs`, confirm:

- `:filter:` — which properties are actually filterable.
- Supported HTTP methods per feed (GET / POST / PATCH / DELETE).
- Action return types the metadata omits (`code=None` findings).

## 5. Fix, build, verify

- Edit the `src/<product>/*.rst` files with `od:` directives.
- Ensure each defined feed is listed in the product index (`feeds.rst`).
- Build: `make docs` (or `sphinx-build -b html src docs`) and resolve **all**
  warnings — an unresolved `:od:type:` / `:od:feed:` xref means a broken or
  misnamed reference.
- Re-run the reconciler; confirm the finding count dropped as expected.

## 6. Re-run gate (optional, for CI)

Add `--fail-on-diff` so the script exits non-zero when any finding remains, and
wire it into CI or a pre-commit hook to catch future drift.

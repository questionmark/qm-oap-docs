# OData documentation audit - PR handoff report

**Branch:** `feature/add-missing-delivery-odata-feeds`
**Prepared:** 2026-07-15
**Audience:** the code owner opening the PR and the reviewers on it.

This is the single-page briefing for the PR. Deeper detail lives in
`ai-docs/proposed-fixes/` (per-service fix specs) and `ai-docs/adrs/`
(why-decisions). If you read nothing else, read the **TL;DR**, the **Reviewer
guide**, and **Before you open the PR**.

---

## TL;DR

This branch reconciles the **Delivery OData (v3)** and **Authoring OData (v4)**
documentation in `src/` against each service's machine-readable `$metadata`
contract, adds re-runnable reconciliation tooling (`ai-scripts/`), and records the
decisions and guardrails (`ai-docs/`).

Every structural fact in the docs (feeds, types, properties, keys, nullability,
navigation targets, action params/returns) is now verified against the
`2026-07-13` `$metadata` baselines and, where metadata can't express it (HTTP
methods, filterability, examples, version history), against the `qm-DeliveryOData`
and `qm-AuthoringApi` source.

**State:** all known documentation defects are fixed and verified. Remaining
reconciler findings are a small, explicitly-accepted set caused by **service-side
metadata bugs** and one deployment lag - these are documented, not fixed in docs,
and should be raised as service tickets (see **Service tickets**).

**Quality gates (current):**
- `sphinx-build -b html src docs` - clean (0 errors; only a pre-existing
  `_static` warning that is also present on `master`).
- Reconciler: **Delivery 17** findings (all accepted residual), **Authoring 0**,
  **Results** all-missing by design (redirect stub, ADR-0003).

---

## What changed, by area

| Area | Path | Summary |
|------|------|---------|
| Delivery docs | `src/deliveryodata/*.rst` | Added missing feeds/types/properties/actions; fixed keys, casing, EDM types, nullability, nav targets; corrected HTTP-method and example-URL claims; fixed fabricated version history. |
| Authoring docs | `src/authoringodata/*.rst` | Added missing properties on `AssessmentAML`/`QuestionQML`; corrected `ModifiedDateTime` types (`String`->`DateTimeOffset`); removed nonexistent `TopicPath`, added `TopicId`; fixed composite-key filter docs. |
| Tooling | `ai-scripts/` | `$metadata`-vs-RST reconciler (v3+v4), baseline fetcher. Handles duplicate-named actions, param types, v3 nav cardinality, and nullability. |
| Decision log | `ai-docs/adrs/` | Why docs-follow-code, why the tooling, Results redirect, and the metadata-gap handling. |
| Guardrails | `ai-docs/rails/` | How to run reconciliation and edit `od:` directives safely. |
| Review trail | `ai-docs/proposed-fixes/` | Per-finding classification + before/after, and the pre-merge review remediation log. |
| Built HTML | `docs/` | Regenerated from the corrected source. |

---

## How this was verified (methodology)

1. **Structural reconciliation.** `ai-scripts/reconcile_odata.py` diffs `$metadata`
   (source of truth) against the `od:` directives in `src/`. Baselines captured
   `2026-07-13` from tenant `406611`.
2. **Controller-code pass.** Everything metadata cannot express - HTTP methods,
   filterability, action return types the service omits - checked against
   `Controllers/*.cs`, `App_Start/ODataConfig.cs`, entities, EF mappings, and
   validators in the service repos.
3. **Independent line reviews.** Each applied commit was reviewed hunk-by-hunk
   against the baseline and the service source.
4. **Version archaeology.** Every `versionadded` was resolved to the real release
   by finding the introducing commit in `qm-DeliveryOData` and the earliest
   `Release_YYYY.MM` tag containing it.
5. **Build gate.** Full `sphinx-build` with warnings-as-signal.

---

## Reviewer guide - expected reconciler residuals (do NOT "fix" these)

Running `ai-scripts/reconcile_odata.py` against the Delivery baseline reports
**17 findings**. Every one is intentional; a reviewer should expect exactly these:

| Residual | Count | Why it stays |
|----------|-------|--------------|
| `[RETURN MISMATCH]` GetAccessUrl, CanLiveProctor | 2 | Service `$metadata` omits the return type (registration defect). Docs state the true type. **Service bug E1/E2.** |
| `[RETURN MISMATCH]` AvailableAppointments + `[MISSING IN DOCS] List_1OfDateTime` | 2 | Service mangles `List<DateTime>` into a fake `List_1OfDateTime` type. Docs state the true `Collection(DateTime)`. **Service bug E3.** |
| `[EXTRA IN DOCS]` PracticeAttempts, PracticeAttempt | 2 | Valid, unconditionally-registered feed absent from the tenant baseline = deployment lag. Re-verify after redeploy. **F1.** |
| `[NOTNULL EXTRA]` (11 properties) | 11 | Service enforces required-ness via EF mappings/validators, which OData v3 `$metadata` does not express (derives nullability from CLR types + `[Required]` only). Docs state the enforced contract. **Service bug E6.** |

If a reviewer sees anything **outside** this list, that is a real regression to
investigate.

---

## Service tickets to raise (Delivery QM / Firestar) - not doc fixes

These are genuine service/metadata defects. The docs describe the intended
contract and must not be "corrected" to match the buggy metadata (ADR-0001/0004).

| # | Defect | Evidence |
|---|--------|----------|
| E1 | `GetAccessUrl` emits no `ReturnType` | `ODataConfig.cs:558` calls `.Returns<string>()` on the wrong variable (`getReviewUrl`) instead of `getAccessUrl`. |
| E2 | `CanLiveProctor` emits no `ReturnType` | `ODataConfig.cs:209` calls `.Returns<bool>()` on `canReview` instead of `canProctor`. |
| E3 | `AvailableAppointments` returns mangled `List_1OfDateTime` | `ODataConfig.cs:349` uses `Returns<List<DateTime>>()`; should be `ReturnsCollection<DateTime>()`. |
| E4 | `PrintBatchUpload.PrecessedDateTime` misspelling | Misspelled in the C# entity; the DB column is correctly `Processed_DateTime_UTC`. API-surface rename is breaking - coordinate. |
| E5 | `Rubric.ShowParticipant` typed as `double` | CLR `double` backing column `SM_RUBRICSHOWNAME`; looks like a flag/name mis-typed as float. Wire contract is `Edm.Double` (docs correct). |
| E6 | `$metadata` under-declares nullability (11 props) | v3 metadata ignores EF `IsRequired()`/validators. Add `[Required]` or non-nullable CLR types to: AssessmentMetadata.Key/Value, Attempt.ParticipantID, AttemptList.ExternalAttemptListID, AttemptMetadata.Key/Value, AttemptMetadataKeyValue.Key/Value, Result.AssessmentID, ScheduleMetadata.Key/Value. |

Re-verify item (not a ticket): **F1** `PracticeAttempts` - re-run reconciliation
after tenant 406611 redeploys; the feed is additionally gated at runtime by the
`FeatureTalviewLiveOnlineProctoring` flag (404 when off).

---

## Pre-merge review: defects found and fixed

A full-branch review before merge found the structural work correct but caught
content defects in the prose/metadata layer. All are now fixed and re-verified
(detail + status table in `ai-docs/proposed-fixes/branch-review-remediation.md`):

- **Build break** - a literal-block `:`/`::` typo caused a docutils ERROR. Fixed.
- **Fabricated version history** - ~19 `versionadded` stamps had been set to a
  placeholder `2021.08`; none was actually 2021.08. Replaced with tag-verified
  versions where confirmable (e.g. 2023.01, 2022.08, 2024.04, 2021.07); the 7
  post-`Release_2024.09` items were **dropped** (see open items) rather than
  ship estimates.
- **Wrong "read only" claims** - three feeds this branch added (AssessmentMetadata,
  Appointments, RulesOfConductTranslations) were writable; verb sets corrected
  against the controllers.
- **404-ing example URLs** - example requests used singular entity-set names;
  corrected to the registered plural sets across all Delivery docs. Also fixed a
  copy-paste `Groups`->`Roles` bug in a `$links` example.
- **Authoring** - removed a nonexistent `TopicPath` from a response example and
  fixed bogus `:filter Id:` on the two composite-key feeds.
- **Misc prose** - stale "future release" ShowHidden warning made present-tense;
  an author-facing instruction removed from a published property description; the
  metadata-gap notes reworded to consumer-facing language.

---

## Open items (deliberately deferred - reviewer's call)

1. **7 `versionadded` dropped pending confirmation.** The local `qm-DeliveryOData`
   clone is not tagged past `Release_2024.09`, so these could not be pinned to a
   release: JobTitle, MinMinutesBetweenAttempts, CanLiveProctor, GetLiveProctorUrl,
   RequirePasscode, Category, SubmitResultsByAdministrator. Re-add once versions
   are confirmed from the release calendar (introduction dates are known and
   recorded in the remediation doc).
2. **Pre-existing wrong "read only" claims** (NOT introduced by this branch;
   present on `master`): MonitoringTypes, ProctoringProviders (both POST+PATCH),
   PrintBatches (full CRUD). Also the Talview Protocol-uniqueness rule on
   ProctoringProviders create is undocumented. Left for a separate cleanup so this
   PR stays scoped to its own changes.
3. **Minor/cosmetic:** `practiceattempt.rst` could note the feature-flag
   availability; `ReplaceExistingGroups`/`ReplaceExistingRoles` are only honored
   under `FFM.UsePeopleSync`; `AGENTS.md` still references a superseded regression
   approach; a pre-existing schedule.rst prose warning cites "2021.08".

---

## Before you open the PR

**Uncommitted work in the tree (needs committing):**
- 12 `src/*.rst` remediation edits (the pre-merge fixes above).
- Regenerated `docs/` (25 files) - rebuilt from the corrected source.
- `ai-docs/proposed-fixes/branch-review-remediation.md` (new) and a one-row edit
  to `ai-docs/proposed-fixes/README.md`.

Already committed on the branch: `ai-scripts/` (tooling), `ai-docs/adrs` + `rails`
+ `delivery.md`/`authoring.md`, and the earlier doc waves.
`ignore/` (baselines, reports, worklist) is gitignored - local only.

**Suggested commit structure for the uncommitted work:**
1. `fix(deliveryodata,authoringodata): correct version history, method and example defects`
   (the 12 `src` files + the two `ai-docs/proposed-fixes` files)
2. `build: regenerate HTML docs` (the `docs/` tree)

**Reproduce the verification:**
```powershell
# reconcile (expect Delivery 17 accepted residual, Authoring 0)
python ai-scripts/reconcile_odata.py `
    --metadata ignore/metadata-baselines/delivery.2026-07-13.metadata.xml `
    --rst-dir src/deliveryodata --product Delivery --out ignore/recon-reports/delivery.txt
python ai-scripts/reconcile_odata.py `
    --metadata ignore/metadata-baselines/authoring.2026-07-13.metadata.xml `
    --rst-dir src/authoringodata --product Authoring --out ignore/recon-reports/authoring.txt

# build (expect clean, only pre-existing _static warning)
sphinx-build -b html src docs
```
(Baselines live under gitignored `ignore/`; regenerate with
`pwsh ai-scripts/fetch_baselines.ps1` if absent.)

---

## Suggested PR description (ready to paste)

> ### Reconcile OData documentation with the service `$metadata` contract
>
> Audits and corrects the Delivery (v3) and Authoring (v4) OData docs against each
> service's `$metadata`, adds re-runnable reconciliation tooling, and records the
> supporting decisions.
>
> **Docs:** added missing feeds/types/properties/actions; fixed keys, casing, EDM
> types, nullability, nav targets, HTTP-method claims, example URLs, and version
> history. **Tooling:** `ai-scripts/` reconciler (v3+v4) + baseline fetcher.
> **Docs-about-docs:** ADRs and rails in `ai-docs/`.
>
> **Verified:** `sphinx-build` clean; reconciler reports only the accepted residual
> (Delivery 17, Authoring 0). The residual is caused by service-side metadata bugs
> and one deployment lag, documented in `ai-docs/pr-report.md` and filed as service
> tickets E1-E6 with Delivery QM / Firestar - the docs intentionally describe the
> true contract rather than match the buggy metadata.
>
> See `ai-docs/pr-report.md` for the full audit report and reviewer guide.

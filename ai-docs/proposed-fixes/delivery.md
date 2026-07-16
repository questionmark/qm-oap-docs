# Delivery OData - proposed fixes

- **Service:** Delivery OData (`System.Web.Http.OData` v5.x, OData **v3**)
- **Source of truth:** `qm-DeliveryOData` -> `App_Start/ODataConfig.cs`,
  `Controllers/*.cs`, `QM.Delivery.ODataService.Entity/*.cs`,
  `QM.Delivery.ODataservice.Common/DTO/*.cs`
- **Baseline:** `ignore/metadata-baselines/delivery.2026-07-13.metadata.xml`
  (tenant 406611)
- **Report:** `ignore/recon-reports/delivery.txt` - **78 findings**
  (37 from the original tool; 41 more after the 2026-07-14 tool upgrade, see
  sections G/H)
- **Owning team:** Delivery QM / Firestar
- **Classification legend:** see [`README.md`](README.md)

## Summary

| Class | Count | Effect |
|-------|-------|--------|
| DOC (docs wrong) | 7 | Edit `.rst` |
| DOC-ADD (undocumented contract) | 18 | Add to `.rst` |
| SVC (service/metadata bug) | 3 (+E4 typo, +E5 side-flag) | Keep docs, raise ticket |
| LAG (deployment lag) | 2 | Keep docs, re-verify |

**2026-07-14 verification addendum:** every A-F item below was independently
re-verified against the baseline XML, the RST, `qmdomain.py`, and the
`qm-DeliveryOData` source - all confirmed (one A4 omission fixed in place, F1
gained a feature-flag caveat). Six further findings were discovered in tool
blind spots (section **G**); the tool was then upgraded to close those blind
spots and its 35 additional findings were all triaged as real - 25 DOC,
10 SVC-class (section **H**, consolidated ticket **E6**).

---

## A. DOC - docs disagree with metadata (edit)

### A1. `ResultAuditLog.IsInQueue` - stray quote typo
`result.rst:478`. A trailing `"` was left in the EDM type.

```rst
-    ..  od:prop::   IsInQueue Edm.Boolean"
+    ..  od:prop::   IsInQueue Edm.Boolean
```

### A2. `Role` - wrong key and missing nav property
`administrator.rst:266-287`. The emitted `Role` type has key **`Name`** (String),
no `ID` property, and an `Administrators` navigation property.

```rst
-    ..  od:prop::   ID  Edm.String
+    ..  od:prop::   Name  Edm.String
         :key:
         :notnull:
+
+    ..  od:prop::   Administrators  Administrator
+        :collection:
+
+        Navigation property to the administrators holding this role.
```

Also update the feed filter text (`administrator.rst:282`):

```rst
-    :filter ID: primary key (the role name)
+    :filter Name: primary key (the role name)
```

### A3. `Rubric.ShowParticipant` - wrong EDM type
`rubric.rst:59`. Metadata emits `Edm.Double`, not `Edm.String`.

```rst
-    ..  od:prop::   ShowParticipant    Edm.String
+    ..  od:prop::   ShowParticipant    Edm.Double
```

### A4. `AttemptMetadata.AttemptID` - casing
`attempt.rst:599`. Emitted name is `AttemptId` (lower `d`). OData v3 URL
resolution is case-sensitive, so `AttemptID` would 404 on `$filter`/`$select`.

```rst
-    ..  od:prop::   AttemptID  Edm.Int32
+    ..  od:prop::   AttemptId  Edm.Int32
```

Also update the AttemptMetadata **feed** filter line (`attempt.rst:60`), which names
the same property and is equally case-sensitive in `$filter`:

```rst
-    :filter AttemptID: associated attempt
+    :filter AttemptId: associated attempt
```

> Scope note: the `AttemptID` at `attempt.rst:646` belongs to `Appointment` and is
> **correct** (metadata emits `Appointment.AttemptID`). Do not change it. The
> `:filter AttemptID:` at `attempt.rst:689` sits under the Appointments feed and is
> likewise correct. `Result.AttemptId` (`result.rst:290`) already uses the right
> casing.

### A5. `Timezone.CurrentUtcTime` - casing
`timezone.rst:43`. Emitted name is `CurrentUTCTime` (matches the sibling
`CurrentUTCOffset*` casing).

```rst
-    ..  od:prop::   CurrentUtcTime    Edm.DateTime
+    ..  od:prop::   CurrentUTCTime    Edm.DateTime
```

### A6. `TestCenter.ID` - key not marked
`testcenter.rst:21`. The key property is documented but missing the `:key:` flag.

```rst
     ..  od:prop::   ID      Edm.Int32
+        :key:
         :notnull:
```

### A7. Ambiguous `Upsert` action cross-references (broken xref)
`administrator.rst:25` and `administrator.rst:33`. Two bare `Upsert` action
references sit in the **Administrators feed** prose, *before* the `Administrator`
type directive (line 64). There the `od` domain has no `od:type` context to qualify
against, so it emits the unresolved target `od-action.Upsert` (confirmed via
`sphinx-build`). The `Upsert` action is defined under the feed (line 35), so its real
target is `od-action.deliveryodata.Administrators.Upsert`. Qualify both references
explicitly (keeping the visible link text as "Upsert"):

```rst
-    ... you can use the :od:action:`Upsert` action
+    ... you can use the :od:action:`Upsert <Administrators.Upsert>` action
```

> The third bare reference at `participant.rst:338` is **not** broken: it sits inside
> the `Participant` type body, so the domain auto-qualifies it to
> `deliveryodata.Participant.Upsert` (the participant `Upsert` is defined under the
> type at line 300), which resolves. Leave it unchanged.

---

## B. DOC-ADD - undocumented properties (add)

| # | Property | EDM type | Location |
|---|----------|----------|----------|
| B1 | `ActionableSchedule.AssessmentID` | `Edm.Int64` | `schedule.rst:458` (ActionableSchedule type) |
| B2 | `Appointment.ExternalAppointmentData` | `Edm.String` | `attempt.rst` (Appointment type) |
| B3 | `AssessmentTranslation.Description` | `Edm.String` | `assessment.rst` (AssessmentTranslation type) |
| B5 | `RulesOfConduct.AllowedResources` | `Edm.String` | `monitoring_type.rst:189` (RulesOfConduct type) |
| B6 | `RulesOfConductTranslation.AllowedResources` | `Edm.String` | `monitoring_type.rst:240` (RulesOfConductTranslation type) |
| B7 | `Schedule.ExternalProctoringID` | `Edm.String` | `schedule.rst` (Schedule type) |

> Nullability (from metadata): **B1 is `Nullable="false"`** and must carry
> `:notnull:`; B2, B3, B5, B6, B7 are nullable (no flag). B7 is system-managed
> (set server-side for Talview-protocol proctoring; explicitly rejected by
> `ScheduleValidator` on PATCH) - the description should say it is read-only.

### B4. `PrintBatchUpload` - type declared with no properties
`printbatch.rst:66`. The `od:type:: PrintBatchUpload` block currently has **zero**
`od:prop` entries. Add the five emitted members:

```rst
 ..  od:type::   PrintBatchUpload
     .. versionadded:: 2020.02
     ...
+    ..  od:prop::   ID  Edm.Int64
+        :key:
+        :notnull:
+
+    ..  od:prop::   PrintBatchId  Edm.Int64
+        :notnull:
+
+    ..  od:prop::   RequestData  Edm.String
+
+    ..  od:prop::   PrecessedDateTime  Edm.DateTime
+
+    ..  od:prop::   PrintBatch  PrintBatch
+
+        Navigation property to the parent PrintBatch.
```

> `PrecessedDateTime` is spelled verbatim from the entity/metadata (should read
> `Processed`). It is a **misspelling in the service code** (`PrintBatchUpload.cs`).
> Document it as-is (renaming it would 404) and raise the typo separately with the
> owning team - see **SVC** note E4.

---

## C. DOC-ADD - undocumented response types (add)

These complex types are returned by the Upsert-family and publish actions but have no
`od:type` directive. Add them (nearest to their producing action). Metadata emits
**only** the ID/payload fields below - the C# `ResponseStatus` (`HttpStatusCode`) on
`BaseUpsertResponse` is marked `[IgnoreDataMember]` (`BaseUpsertResponse.cs:13-14`),
so it is excluded from metadata and the JSON payload by design; it only drives the
HTTP status code of the response. It is **not** part of the contract - do not
document it.

### C1. `UpsertParticipantResponse` (in `participant.rst`)
```rst
..  od:type::   UpsertParticipantResponse

    ..  od:prop::   ParticipantID  Edm.Int32
```

### C2. `UpsertAdministratorResponse` (in `administrator.rst`)
```rst
..  od:type::   UpsertAdministratorResponse

    ..  od:prop::   AdministratorID  Edm.Int32
```

### C3. `UpsertParticipantAndScheduleResponse` (in `participant.rst`)
```rst
..  od:type::   UpsertParticipantAndScheduleResponse

    ..  od:prop::   ParticipantID  Edm.Int32
    ..  od:prop::   ScheduleID  Edm.Int32
```

### C4. `CustomScheduleAndLaunchResponse` (in `participant.rst`)
```rst
..  od:type::   CustomScheduleAndLaunchResponse

    ..  od:prop::   ScheduleID  Edm.Int32
    ..  od:prop::   LaunchURL  Edm.String
```

### C5. `PublishResultResponse` (in `result.rst`)
```rst
..  od:type::   PublishResultResponse

    ..  od:prop::   SuccessCount  Edm.Int32
    ..  od:prop::   FailureCount  Edm.Int32
    ..  od:prop::   Message  Edm.String
    ..  od:prop::   FailureResultIds  Edm.Int32
        :collection:
```

### C6. `List_1OfDateTime` - **do not document**
This is a framework artifact emitted because `AvailableAppointments` returns
`List<DateTime>` (see **SVC** E3), which the v3 model builder mangled into a fake
complex type exposing `Capacity`. It is not a real contract type; the fix belongs in
the service, not the docs.

---

## D. DOC-ADD - action return types and parameters (add)

The action bodies are documented; only the return type / parameter list is missing.
Add the return type as the second positional token of `od:action::`.

| # | Action | Location | Change |
|---|--------|----------|--------|
| D1 | `Upsert` (Participant) | `participant.rst:300` | `od:action:: Upsert` -> `od:action:: Upsert UpsertParticipantResponse` |
| D2 | `Upsert` (Administrator) | `administrator.rst:35` | `od:action:: Upsert` -> `od:action:: Upsert UpsertAdministratorResponse` |
| D3 | `ScheduleAndLaunch` | `participant.rst:321` | append return `CustomScheduleAndLaunchResponse` |
| D4 | `UpsertParticipantAndSchedule` | `participant.rst:334` | append return `UpsertParticipantAndScheduleResponse` |
| D5 | `ReplayResultsByIDList` | `result.rst:125` | append return `PublishResultResponse` |
| D6 | `ActionableSchedulesForObservation` | `administrator.rst:235` | add `:input: ScheduleID Edm.Int32` (param present in metadata + code, absent in docs) |

> D6 note: the plural `ActionableSchedulesForObservation` (administrator) is distinct
> from the singular `ActionableScheduleForObservation` (participant.rst:344), which
> already documents its `ScheduleID`/`ObserverID` inputs correctly.
>
> D6 also requires prose changes: `administrator.rst:239-240` says "It takes no
> parameters" and the example POST body at lines 245-246 is `{}` - both are wrong.
> The parameter is **required**: `ODataConfig.cs:286-290` declares
> `Parameter<int>("ScheduleID")` and `AdministratorsController.cs:226-241` returns
> `BadRequest("The parameter 'ScheduleID' is required.")` when it is absent. Update
> the prose and make the example body `{"ScheduleID": <id>}`.

---

## E. SVC - metadata/service bugs (keep docs, raise ticket)

Do **not** "correct" the docs to match these - the metadata is wrong, the docs match
the intended contract. Raise each with Delivery QM / Firestar.

- **E1. `GetAccessUrl`** - metadata emits no `ReturnType`. Cause: `.Returns<string>()`
  was chained on the wrong action object in `ODataConfig.cs`. Docs correctly keep
  `Edm.String`. See [`../adrs/0004-getaccessurl-return-type-bug.md`](../adrs/0004-getaccessurl-return-type-bug.md).
- **E2. `CanLiveProctor`** - same defect class; metadata emits no `ReturnType`. Docs
  correctly keep `Edm.Boolean`.
- **E3. `AvailableAppointments`** - returns `List_1OfDateTime` instead of
  `Collection(Edm.DateTime)` (see C6). Docs correctly keep `Edm.DateTime` with
  `:collection:`. The `List<DateTime>` return should be projected as a proper
  collection in the service.
- **E4. `PrintBatchUpload.PrecessedDateTime`** - misspelling in the entity/DAL. Docs
  must mirror it verbatim (B4); the rename is a service change.

---

## F. LAG - valid in code, absent from baseline (keep docs, re-verify)

- **F1. `PracticeAttempt` / `PracticeAttempts`** - the entity has a conventional `ID`
  key (`PracticeAttempt.cs:7`) and is registered unconditionally in
  `ODataConfig.cs:188` (the file contains no conditionals at all; the EDM model is
  built once at app start, so no flag can remove it from a deployed build's
  `$metadata`). The code is recent - added 2026-06-15 (`618afc22`,
  "AB#265565: Test it out Flow - Expose with DeliveryOData") - so absence from the
  tenant 406611 baseline is a **deployment lag**, not a docs error. Keep
  `practiceattempt.rst` as-is and re-run reconciliation after the tenant is
  redeployed to confirm it appears.

  **Runtime caveat:** every action in `PracticeAttemptsController` is additionally
  gated by `FFM.FeatureTalviewLiveOnlineProctoring` and returns **404** when the
  flag is off (`PracticeAttemptsController.cs:67-73`). Once deployed, the feed
  appears in `$metadata` for all tenants but only answers for tenants with the
  Talview Live Online Proctoring feature. Consider a doc note about this
  availability restriction on `practiceattempt.rst`.

---

## G. Verification addendum (2026-07-14) - additional findings

Found during the independent source-verification pass of this document (every A-F
item was re-checked against the baseline `$metadata`, the RST, `qmdomain.py`, and
the `qm-DeliveryOData` source). All A-F items were confirmed; the items below are
**new** findings the original pass missed, mostly in blind spots of the
reconciliation tool (see "Tooling limitations" below).

### G1. DOC - `ReplayResultsByDateRange` parameter types wrong
`result.rst:108-109` documents `:input: StartDate Edm.DateTime, EndDate
Edm.DateTime`, but metadata declares both parameters **`Edm.String`**
(baseline lines 1299-1302), and the service confirms:
`ODataConfig.cs:327-328` uses `Parameter<string>("StartDate")` /
`Parameter<string>("EndDate")`.

```rst
-    :input: StartDate Edm.DateTime, EndDate Edm.DateTime
+    :input: StartDate Edm.String, EndDate Edm.String
```

### G2. DOC-ADD - `ActionableSchedules` (Participant) missing `ShowHidden` input
`participant.rst:237-238` documents the Participant-bound `ActionableSchedules`
action with no `:input:`, and the prose at line 241 says "It takes no parameters".
Metadata (baseline lines 1213-1216) declares an optional payload parameter
`ShowHidden Edm.Boolean` (`ODataConfig.cs:218-220`, `Parameter<bool?>`). The
warning prose at lines 261-271 describes `ShowHidden` as arriving "as of the
2022.03 release" - it is present today, so add the input and update both prose
passages:

```rst
     ..  od:action:: ActionableSchedules ActionableSchedule
         :collection:
+        :input: ShowHidden Edm.Boolean
```

### G3. DOC - `RulesOfConductTranslations` nav prop has bogus `Edm.` prefix
`monitoring_type.rst:237` documents the navigation property as
`RulesOfConductTranslations Edm.RulesOfConductTranslation`. Navigation properties
reference the target type name, never `Edm.<TypeName>` (see
`rails/editing-od-directives.md`), and the association multiplicity is `*`:

```rst
-    ..  od:prop::   RulesOfConductTranslations  Edm.RulesOfConductTranslation
+    ..  od:prop::   RulesOfConductTranslations  RulesOfConductTranslation
+        :collection:
```

(Adjust the `-` line to the exact current text when applying.)

### G4. DOC - PrintBatchUploads feed method list stale
`printbatch.rst:85` says `:method GET: read only`, but the controller is
constructed with `postEnabled: true` (`PrintBatchUploadsController.cs:33-34` base
call; the `Post` override at line 54 ingests the uploaded CSV). PATCH and DELETE
are disabled. Add the POST method line alongside GET.

### G5. DOC - duplicated sentence in `ExceptionSchedules`
`schedule.rst:338-344` contains a duplicated/leftover sentence "A navigation
property to the (optional) parent schedule." Remove the stray copy.

### G6. DOC (minor) - missing `:notnull:` flags
Metadata declares `Nullable="false"` for properties whose docs lack `:notnull:`:
`Timezone.BaseUTCOffsetMinutes`, `Timezone.CurrentUTCOffsetMinutes`,
`Timezone.CurrentUTCTime` (after A5), `Timezone.CurrentTimezoneTime`, and
`TestCenter.Name`. Low-impact; align while editing those files for A5/A6.

### E5. SVC (side-flag) - `Rubric.ShowParticipant` modeled as `double`
The docs fix A3 is faithful (CLR `public double ShowParticipant`, `Rubric.cs:15`),
but the backing column is `SM_RUBRICSHOWNAME` (`RubricMapping.cs:19`) - a
"show name" flag modeled as a floating-point number. Semantically this looks like
a modeling defect worth mentioning to Delivery QM / Firestar alongside E1-E4;
the wire contract is `Edm.Double` regardless.

### Tooling limitations exposed by G1-G3 - FIXED 2026-07-14

The four blind spots that hid G1-G3/G6 (action-name collisions, name-only param
comparison, untyped v3 nav props, undiffed nullability) were closed by the
2026-07-14 tool upgrade (see `ai-scripts/README.md`). The upgraded tool now
catches G1, G2, G3, and G6 mechanically, independently confirms D2
(`Administrator.Upsert` return type), and surfaced the additional findings in
section **H** below. Delivery report: 37 -> 78 findings on the same baseline;
all new findings triaged 2026-07-14 with zero false positives.

---

## H. Findings from the upgraded reconciler (2026-07-14) - all triaged, zero false positives

The tool upgrade surfaced 35 additional findings. Every one was verified against
the baseline XML, the RST, and the `qm-DeliveryOData` source (entities, EF
mappings, validators, controllers). Verdicts: 25 DOC, 10 SVC-class.

### H1. DOC - missing `:notnull:` (21 properties; metadata `Nullable="false"`)

Add `:notnull:` under the `od:prop` line at each location (subsumes and extends
G6):

| Property | RST location |
|----------|--------------|
| `Administrator.Blocked` | `administrator.rst:123` |
| `Answer.Revision` | `answer.rst:93` |
| `MonitoringType.Name` | `monitoring_type.rst:48` |
| `MonitoringType.TextToSpeech` | `monitoring_type.rst:124` |
| `MonitoringType.RequireObserver` | `monitoring_type.rst:130` |
| `MonitoringType.RequireConfirmation` | `monitoring_type.rst:136` |
| `MonitoringType.RequirePasscode` | `monitoring_type.rst:142` |
| `MonitoringType.Disabled` | `monitoring_type.rst:154` |
| `Participant.Blocked` | `participant.rst:202` |
| `ProctoringProvider.Name` | `monitoring_type.rst:285` |
| `ProctoringProvider.Protocol` | `monitoring_type.rst:290` |
| `RulesOfConduct.CreatedDateTime` | `monitoring_type.rst:233` |
| `RulesOfConduct.ModifiedDateTime` | `monitoring_type.rst:235` |
| `RulesOfConductTranslation.Language` | `monitoring_type.rst:250` |
| `RulesOfConductTranslation.CreatedDateTime` | `monitoring_type.rst:253` |
| `RulesOfConductTranslation.ModifiedDateTime` | `monitoring_type.rst:255` |
| `Schedule.IsDeleted` | `schedule.rst:309` |
| `TestCenter.Name` | `testcenter.rst:28` |
| `Timezone.BaseUTCOffsetMinutes` | `timezone.rst:37` |
| `Timezone.CurrentUTCOffsetMinutes` | `timezone.rst:41` |
| `Timezone.CurrentTimezoneTime` | `timezone.rst:47` |

(Plus `Timezone.CurrentUTCTime` when applying A5, per G6.)

### H2. SVC - `:notnull:` in docs, nullable in metadata (10 properties; keep docs)

Root cause (verified in source): OData v3 metadata derives nullability from CLR
types and `[Required]` **only** - requiredness enforced via EF fluent mappings
(`IsRequired()`) or validators is invisible in the wire contract. Every one of
these is genuinely required by the service, so the docs describe the intended
contract and stay unchanged:

`AssessmentMetadata.Key` (EF `IsRequired()` + validator), `Attempt.ParticipantID`
(CLR `int?` but validator requires on create; unpatchable),
`AttemptList.ExternalAttemptListID` (EF + validator), `AttemptMetadata.Key` /
`.Value` (controller validation), `AttemptMetadataKeyValue.Key` / `.Value`
(enforced downstream; lowest confidence), `Result.AssessmentID` (CLR `long?`;
engine-written, backing column NOT NULL), `ScheduleMetadata.Key` / `.Value`
(validator, create and update).

**E6 (SVC ticket, consolidated):** Delivery OData `$metadata` under-declares
nullability for the ten properties above - add `[Required]` or non-nullable CLR
types so the wire contract matches enforcement. While in there:
`AssessmentMetadata.Value` is enforced exactly like `.Key` but the docs at
`assessment.rst:334` lack `:notnull:` - add it (single DOC edit folded into H1
application) so Key/Value are consistent.

### H3. DOC - missing `:collection:` on navigation properties

- `Attempt.BranchedResults` (`attempt.rst:504`) - association multiplicity `*`,
  C# `ICollection<Result>`; the prose already says "all the results".
- `Question.Rubric` (`question.rst:53`) - multiplicity `*`, C# `ICollection<Rubric>`.

### H4. DOC - `Edm.`-prefixed nav targets in scoringtask.rst (same class as G3)

Both render as dead text instead of cross-reference links (`qmdomain.py:210`
only xrefs non-`Edm.` types). Both are single-valued (`0..1`) - no
`:collection:` needed:

```rst
-    ..  od:prop::   ScoringResult    Edm.ScoringResult      (scoringtask.rst:309)
+    ..  od:prop::   ScoringResult    ScoringResult

-    ..  od:prop::   Dimension    Edm.Dimension              (scoringtask.rst:311)
+    ..  od:prop::   Dimension    Dimension
```

---

## Application order (after review approval)

1. Apply **A** (7 findings, 10 line edits incl. the A4 filter line) and **B**
   (7 additions) - pure doc corrections/additions.
2. Apply **C** (5 type additions) then **D** (6 action wirings) so the new
   `:od:type:` return references resolve.
3. Apply **G1-G5** and **H1/H3/H4** (plus the `AssessmentMetadata.Value`
   `:notnull:` from H2/E6) - verification-addendum doc fixes. G6 is subsumed by
   H1.
4. Leave **E**/**F**/**H2** untouched in the docs; open service tickets for
   E1-E6 and a re-verify note for F1 (including the Talview feature-flag
   caveat).
5. Rebuild (`make docs`) and confirm zero unresolved `:od:type:`/`:od:feed:`
   xrefs.
6. Re-run `reconcile_odata.py` (upgraded 2026-07-14; Delivery currently reports
   **78** findings). After applying, the remaining findings should be exactly:
   the E-set return-type gaps (`GetAccessUrl`, `CanLiveProctor`,
   `AvailableAppointments` + its `List_1OfDateTime` missing-type line), the two
   F1 `PracticeAttempt(s)` EXTRA lines, and the ten H2 `[NOTNULL EXTRA]` lines -
   all knowingly kept until the service is fixed/redeployed.

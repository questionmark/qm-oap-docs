# Branch review - remediation before merge

- **Branch:** `feature/add-missing-delivery-odata-feeds`
- **Reviewed:** 2026-07-14 (full delta `master..HEAD`, all six commits)
- **Original verdict:** NOT ready to merge - one build-breaking error and several
  factually wrong statements (invented version history, wrong writability claims,
  404-ing example URLs) that would ship misinformation to integrators.
- **Sources of truth:** `ignore/metadata-baselines/*.2026-07-13.metadata.xml`,
  the service repos `qm-DeliveryOData` / `qm-AuthoringApi` (controllers +
  entities + git history), and `src/qmdomain.py` for directive semantics.

## Resolution status (applied 2026-07-14, uncommitted in working tree)

**All P0 and P1 items fixed; R11/R12 partially swept.** Post-fix gates: `sphinx`
build clean (the R1 docutils ERROR is gone; only the pre-existing `_static`
warning remains); reconciler = Delivery **17** (exactly the accepted residual:
E1-E3 + F1 x2 + 11 `[NOTNULL EXTRA]`), Authoring **0**.

| Item | Status |
|------|--------|
| R1 build break | FIXED (`::`); `docs/` regenerated |
| R2 version history | 19 stamps replaced with tag-verified versions; 7 post-2024.09 (unconfirmed) **dropped** rather than estimate; `Groups` stamp dropped (documented the edit-capability, nav is old) |
| R3 method claims | FIXED - AssessmentMetadata (full CRUD), Appointments (POST+DELETE), RulesOfConductTranslations (POST+PATCH), all verb sets verified against controllers |
| R4 example URLs | FIXED (plural entity sets) |
| R5 stale ShowHidden warning | FIXED (present-tense note, correct default semantics) |
| R6 leaked instruction | FIXED (consumer-facing description) |
| R7 GetAccessUrl note | reworded consumer-facing; matching note added to CanLiveProctor; **AvailableAppointments left** (marked "Reserved for internal use", note would be noise) |
| R8 AssessmentMetadata.Value :notnull: | FIXED (adds the 11th accepted `[NOTNULL EXTRA]`) |
| R9 TopicPath example | FIXED (`TopicId`) |
| R10 bogus `:filter Id:` | FIXED (composite-key members on both AML/QML feeds) |
| R11 singular URLs | swept ALL in delivery docs (incl. `$links`, InvokeAction, Open); also fixed a copy-paste `Groups`->`Roles` bug in the Roles `$links` example |
| R12 pre-existing "read only" | **NOT changed** - MonitoringTypes/ProctoringProviders/PrintBatches "read only" pre-date this branch (confirmed on `master`); flagged, left for a separate pass |

**Still open / flagged (not applied):**
- The 7 dropped `versionadded` (JobTitle, MinMinutesBetweenAttempts, CanLiveProctor,
  GetLiveProctorUrl, RequirePasscode, Category, SubmitResultsByAdministrator) can be
  re-added once their release versions are confirmed from the release calendar.
- R12 pre-existing wrong "read only" on MonitoringTypes / ProctoringProviders /
  PrintBatches (all support POST+PATCH; PrintBatches full CRUD), plus the
  undocumented Talview Protocol-uniqueness rule on ProctoringProviders create.
- R13-R16 (practiceattempt availability note, `ReplaceExistingGroups` conditionality,
  AGENTS.md stale tooling section, cosmetic) - not applied.
- Pre-existing prose `schedule.rst` warning references "2021.08" (not a real release);
  left as-is (historical behavior note, on `master`).
- Uncommitted: 12 `src/*.rst` remediation edits, regenerated `docs/` (25 files),
  and the two `ai-docs/proposed-fixes/` files (this doc + the README row).
  `ai-scripts/` (reconciler upgrade + key-nullability fix) is already committed at
  HEAD; `ignore/recon-reports/` is gitignored (local only).

## How this was verified

- **Reconciler acceptance run** (upgraded tool): Delivery -> 16 residual findings,
  all in the knowingly-accepted set (E1-E3 service return-type bugs, F1 deployment
  lag, H2 nullability under-declaration). Authoring -> **0** after an
  `edmx_parser.py` fix (v4 composite-key members are implicitly non-nullable).
  Results -> 28, all-missing by design (ADR-0003).
- **Sphinx build gate:** one docutils ERROR (item **R1**); otherwise clean
  (`_static` warning is pre-existing on `master`, not a branch regression).
- **Three independent line-by-line reviews** of the apply commits vs baseline +
  service source: Delivery structural = perfect; Authoring structural = perfect;
  prose/method/filter/version claims = the defects below.

## Severity legend

- **P0** - blocks merge (build breaks, or publishes provably false facts)
- **P1** - should fix before merge (misleads integrators)
- **P2** - fix opportunistically / pre-existing, batch if convenient

---

## P0 - Blockers

### R1. Build-breaking literal-block error - `participant.rst:244`
The `ActionableSchedules` example intro ends with a single colon, so the JSON
block below it is not a literal block. `sphinx-build` emits
`ERROR: Unexpected section title` at `participant.rst:249`, and the published
HTML (already regenerated in commit `b3d0213`) renders the example as broken body
text.

```rst
-        an optional ``ShowHidden`` parameter (defaults to False):
+        an optional ``ShowHidden`` parameter (defaults to False)::
```
After fixing, rebuild `docs/` (`sphinx-build -b html src docs`) and confirm zero
warnings.

### R2. Fabricated `versionadded:: 2021.08` stamps (26 directives)
Commit `54c0399` stamped `.. versionadded:: 2021.08` onto 26 documented
properties/actions as a placeholder. **None of the 26 is actually 2021.08** - and
no `Release_2021.08` (or `Release_21.08`) tag has ever existed; the only 2021
release is `Release_21.07`. The true release for each was recovered by finding the
commit that introduced the feature in `qm-DeliveryOData` and the earliest
`Release_YYYY.MM` tag containing it (method reproducible; worked example:
`Participant.Blocked` -> commit `f50d7040` 2022-11-14 -> `Release_2023.01`).

**Resolved versions (19 exact, from release tags):**

| doc location | item | correct `versionadded` |
|---|---|---|
| administrator.rst:35 | `Upsert` action | 2022.01 |
| administrator.rst:126 | PeopleSyncID | 2022.08 |
| administrator.rst:132 | Blocked | 2023.01 |
| administrator.rst:139 | Groups (nav) | 2018.06 *(see note)* |
| administrator.rst:171 | Roles (nav) | 2021.07 |
| participant.rst:156 | DateOfBirth | 2022.01 |
| participant.rst:196 | PeopleSyncID | 2022.08 |
| participant.rst:202 | Blocked | 2023.01 |
| schedule.rst:302 | RulesOfConductID | 2021.07 |
| schedule.rst:309 | IsDeleted | 2024.04 |
| schedule.rst:355 | RulesOfConduct (nav) | 2021.07 |
| monitoring_type.rst:119 | TranslationToolLangs | 2022.06 |
| monitoring_type.rst:125 | TextToSpeech | 2022.08 |
| monitoring_type.rst:132 | RequireObserver | 2022.10 |
| monitoring_type.rst:139 | RequireConfirmation | 2024.02 |
| monitoring_type.rst:168 | RulesOfConductID | 2021.07 |
| monitoring_type.rst:175 | RulesOfConduct (nav) | 2021.07 |
| assessment.rst:109 | RulesOfConductID | 2021.07 |
| assessment.rst:174 | RulesOfConduct (nav) | 2021.07 |

**Needs confirmation (7 items, introduced after the newest local tag
`Release_2024.09`):** introducing-commit dates are known, but no release tag in
the local clone contains them, so the exact `YYYY.MM` must be confirmed against
the release calendar (or `git fetch --tags` once the mirror is updated). Estimates
are commit-month + ~1 (normal release cadence):

| doc location | item | introduced (commit date) | estimate - CONFIRM |
|---|---|---|---|
| participant.rst:190 | JobTitle | 2025-02-25 | ~2025.03 |
| schedule.rst:322 | MinMinutesBetweenAttempts | 2024-09-10 | ~2024.10 |
| schedule.rst:443 | CanLiveProctor action | 2024-12-09 | ~2025.01 |
| schedule.rst:449 | GetLiveProctorUrl action | 2024-12-09 | ~2025.01 |
| monitoring_type.rst:146 | RequirePasscode | 2024-09-11 | ~2024.10 |
| monitoring_type.rst:153 | Category | 2025-08-11 | ~2025.09 |
| result.rst:116 | SubmitResultsByAdministrator | 2025-04-28 | ~2025.05 |

**Application:**
- Replace the 19 exact stamps directly.
- For the 7 estimates, confirm the release version before writing it; if it cannot
  be confirmed in time, **remove** the `versionadded` line for that item rather
  than ship an estimate (an absent "since" marker beats a wrong one). Do not leave
  any at 2021.08.
- **Note on `Groups` (2018.06, MEDIUM confidence):** `Groups` predates this repo's
  file history; 2018.06 is the earliest tag demonstrably containing it, but the
  nav is genuinely old and arguably shouldn't carry a "versionadded" at all -
  consider dropping the stamp instead of asserting 2018.06.
- Re-confirm each line number before editing (they drift as earlier fixes land);
  attribute by item name. Untouched `2021.05 / 2020.08 / 2019.05 / 2020.02` stamps
  elsewhere are unrelated and correct - leave them.

---

## P1 - Should fix before merge

### R3. Wrong `:method GET: read only` claims (writable feeds documented as read-only)
Introduced by `54c0399`. Verified against each feed's controller constructor
flags (`postEnabled` / `patchEnabled` / `deleteEnabled`) in `qm-DeliveryOData`:

| Feed (doc) | Documented | Controller reality |
|---|---|---|
| `assessment.rst:301` AssessmentMetadata | GET read only | POST + PATCH + DELETE all enabled (`AssessmentMetadataController.cs:19`) |
| `attempt.rst:689` Appointments | GET read only | POST (`AppointmentsController.cs:150`) + DELETE (`:191`) |
| `monitoring_type.rst:281` RulesOfConductTranslations | GET read only | POST + PATCH (`RulesOfConductTranslationsController.cs:32-34`) |

Correct each to the real supported verbs, mirroring the `:method:` style already
used on writable feeds elsewhere in the docs.

### R4. Example URLs use singular entity-set names (would 404)
The two newly added action examples address the entity by its **singular** type
name, but the service registers **plural** entity sets and resolves paths
exactly (no singular aliasing - `CustomODataPathHandler` / `DefaultODataPathHandler`):

```rst
- POST /deliveryodata/<customer-id>/Participant(123456)/ScheduleAndLaunch   (participant.rst:330)
+ POST /deliveryodata/<customer-id>/Participants(123456)/ScheduleAndLaunch

- POST /deliveryodata/<customer-id>/Administrator(456789)/GetAccessUrl      (administrator.rst:266)
+ POST /deliveryodata/<customer-id>/Administrators(456789)/GetAccessUrl
```
The tutorial page `sdelivery.rst` already uses the correct plural form. (Several
*pre-existing* examples share this bug - see R11 - but these two are new.)

### R5. Stale, now self-contradictory `ShowHidden` warning - `participant.rst:263-273`
The `.. warning::` still says ShowHidden "as of the 2022.03 release ... **will be**
supported" and "Currently, all schedules are returned by default". This now
contradicts the input documented directly above it (R1 block), and the controller
confirms hidden schedules are excluded by default today
(`ParticipantsController.cs:276-277`). Rewrite in the present tense: ShowHidden is
a supported optional parameter defaulting to False; pass True to include hidden
schedules. (This is the second half of proposed-fix **G2**, left unapplied.)

### R6. Author-facing instruction leaked into published prose - `printbatch.rst`
The `PrecessedDateTime` description ends with:
> "Document it verbatim to match the wire contract."
That is a note to doc authors, meaningless to an API consumer. Keep the
user-relevant fact (the property name is misspelled in the service but is the real
wire field), drop the instruction sentence. Example:
```
The property name is misspelled (the service emits ``PrecessedDateTime``,
not ``ProcessedDateTime``); use the spelling shown, which is what the API returns.
```

### R7. `GetAccessUrl` note - internal language + inconsistent - `administrator.rst` (~line 271)
The uncommitted-then-committed `.. note::` reads "...tracked separately with the
owning team", which is internal process language in public docs. Also, the
identical metadata-gap defect affects `CanLiveProctor` and `AvailableAppointments`,
which received no such note - so the treatment is inconsistent. Choose one:
- drop the note (the docs already state the correct `Edm.String` return type), or
- reword to consumer-facing language ("The service's `$metadata` does not currently
  advertise a return type for this action; it returns a JSON string.") and add the
  equivalent to `CanLiveProctor` and `AvailableAppointments`.

### R8. Missing approved `:notnull:` - `assessment.rst` AssessmentMetadata.Value
Proposed-fix **H1-extra** (fold-in from H2/E6) was not applied. `AssessmentMetadata.Key`
carries `:notnull:` but `.Value` does not, though both are enforced identically by
the service. Add `:notnull:` under the `Value Edm.String` prop for consistency.
(This is one of the 10 accepted `[NOTNULL EXTRA]` residuals - documenting the
intended contract; the service ticket E6 covers the metadata side.)

### R9. Authoring - `TopicPath` leftover in JSON example - `question_revision.rst:45`
Commit `8d381a4` correctly removed the `TopicPath` property (it exists in neither
metadata nor the `QuestionRevision` entity - it was a legacy SOAP-only field), but
its response example still shows `"TopicPath": "SubjectiveQuestions"`. The page now
documents a property set that contradicts its own example. Replace with the real
FK: `"TopicId": <n>`.

### R10. Authoring - bogus `:filter Id:` on composite-key feeds
`assessment_aml.rst:10` and `question_qml.rst:10` declare `:filter Id: primary key`,
but neither entity has an `Id` property - the key is composite
(`AssessmentRevisionId` + `Language`, `QuestionRevisionId` + `Language`). Now
visibly wrong against the property sets this branch just documented. Correct the
filter lines to the real key members. (Pre-existing, but same-file and made
conspicuous by this branch.)

---

## P2 - Pre-existing / opportunistic (NOT introduced by this branch)

These are the same defect classes found in code the branch did not add. Not
"new bugs you are submitting", but cheap to batch:

- **R11. More singular-URL examples** (pre-existing): `participant.rst:246,284`,
  `administrator.rst:254`, `result.rst:370`, `schedule.rst:398`, `testcenter.rst:76`.
- **R12. More wrong "read only" feeds** (pre-existing): `monitoring_type.rst:9`
  MonitoringTypes (POST/PATCH enabled), `monitoring_type.rst:22` ProctoringProviders
  (POST/PATCH enabled - and the new `d820010b` Talview Protocol-uniqueness rule on
  create is undocumented), `printbatch.rst:9` PrintBatches (full CRUD).
- **R13. `practiceattempt.rst` availability** - the whole feed 404s unless
  `FeatureTalviewLiveOnlineProctoring` is enabled
  (`PracticeAttemptsController.cs:67-73`), and the brand-new feed (service code
  2026-06-15) carries no `versionadded`. Add an availability note and a version
  marker. (Overlaps proposed-fix **F1** re-verify note.)
- **R14. `ReplaceExistingGroups` / `ReplaceExistingRoles`** on Upsert are only
  honored when `FFM.UsePeopleSync` is enabled (`ParticipantsController.cs:426-427`);
  silently ignored otherwise. Undocumented conditionality.
- **R15. `AGENTS.md`** still recommends the superseded OpenAPI + `oasdiff`
  regression approach and hardcodes this branch name; the repo now has its own
  `ai-scripts/reconcile_odata.py`. Refresh so future contributors are not
  misdirected.
- **R16. Cosmetic:** `feeds.rst` missing trailing newline;
  `assessment_revision.rst` example omits the now-documented `AssessmentName`.

---

## What is verified CORRECT (no action)

- Every `od:feed` / `od:type` / `od:prop` / `od:action` name, EDM type, and
  `:key:` / `:notnull:` / `:collection:` flag added by the apply commits matches
  the metadata baseline exactly (Delivery and Authoring).
- All Delivery action return-type wirings (D1-D6) match the baseline FunctionImports.
- `feeds.rst` indexes all 39 defined Delivery feeds - no orphan/missing entries.
- The URL-breaking casing fixes (`SessionAuditLogs`, `Timezones`, Role key ->
  `Name`) are correct.
- Must-not-change items held: `Appointment.AttemptID` casing, the Appointments-feed
  filter, the in-type bare `Upsert` xref, no `List_1OfDateTime` type, no
  `ResponseStatus` on response types.

---

## Suggested fix order

1. **R1** (unbreak the build) + rebuild `docs/`.
2. **R2** (version history) - decide replace-vs-remove with whoever owns the
   release calendar; this is the largest correctness item.
3. **R3, R4, R9, R10** (false facts integrators would act on).
4. **R5, R6, R7, R8** (prose/consistency).
5. Optionally batch **R11-R16**.
6. Re-run the reconciler (expect the same 16 Delivery / 0 Authoring residuals) and
   a clean `sphinx-build`. Commit the uncommitted `edmx_parser.py` key-nullability
   fix separately.

## Open decision for the reviewer

**R2** is now mostly resolved: 19 of the 26 stamps have exact release versions
recovered from `qm-DeliveryOData` release tags (table above). The only remaining
decision is the **7 post-2024.09 items** - confirm their release versions against
the release calendar, or drop the `versionadded` line for any that can't be
confirmed. The branch must not merge with any `2021.08` stamp intact.

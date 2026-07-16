# Authoring OData — Proposed Fixes

Reconciliation of `src/authoringodata/` against metadata baseline
`ignore/metadata-baselines/authoring.2026-07-13.metadata.xml` (OData v4).

**Source repo:** `qm-AuthoringApi` (Team Aurora)  
**Reconciler run:** 2026-07-14  
**Total findings:** 36

---

## Summary

| Class | Count | Action |
|-------|-------|--------|
| DOC (docs wrong) | 3 | Edit `.rst` |
| DOC-ADD (undocumented) | 19 | Add to `.rst` |
| DOC-REM (extra in docs) | 1 | Remove or note |
| NOTNULL (missing flag) | 13 | Add `:notnull:` |

---

## A. DOC — Type Mismatches (3 edits)

| ID | Property | Docs say | Code says | File | Line |
|----|----------|----------|-----------|------|------|
| A1 | `AssessmentRevision.ModifiedDateTime` | `Edm.String` | `DateTimeOffset` | assessment_revision.rst | 98 |
| A2 | `QuestionRevision.ModifiedDateTime` | `Edm.String` | `DateTimeOffset` | question_revision.rst | 88 |
| A3 | `Topic.ModifiedDateTime` | `Edm.String` | `DateTimeOffset` | topic.rst | 42 |

**Root cause:** Original docs pre-date service migration to `DateTimeOffset`.

---

## B. DOC-ADD — Missing Properties (19 additions)

### B1–B9: AssessmentAML (9 properties)
Currently only describes feed/type stub. All properties from entity:

| Property | Type | Notes |
|----------|------|-------|
| `AssessmentRevisionId` | `Edm.Int32` | FK |
| `Language` | `Edm.String` | |
| `CreatedDateTime` | `Edm.DateTimeOffset` | |
| `Author` | `Edm.String` | |
| `ModifiedDateTime` | `Edm.DateTimeOffset` | |
| `Editor` | `Edm.String` | |
| `TranslationStatus` | `Edm.Int32` | Nullable |
| `IsDeleted` | `Edm.Boolean` | |
| `AssessmentRevision` | `AssessmentRevision` | Nav property |

### B10–B18: QuestionQML (9 properties)
Same pattern:

| Property | Type | Notes |
|----------|------|-------|
| `QuestionRevisionId` | `Edm.Int32` | FK |
| `Language` | `Edm.String` | |
| `CreatedDateTime` | `Edm.DateTimeOffset` | |
| `Author` | `Edm.String` | |
| `ModifiedDateTime` | `Edm.DateTimeOffset` | |
| `Editor` | `Edm.String` | |
| `TranslationStatus` | `Edm.Int32` | Nullable |
| `IsDeleted` | `Edm.Boolean` | |
| `QuestionRevision` | `QuestionRevision` | Nav property |

### B19: AssessmentRevision.AssessmentName
| Property | Type |
|----------|------|
| `AssessmentName` | `Edm.String` |

### B20-B21: QuestionRevision.Topic navigation
| Property | Type | Notes |
|----------|------|-------|
| `TopicId` | `Edm.Int32` | Nullable FK (`int?`) |
| `Topic` | `Topic` | Nav property |

---

## C. DOC-REM — Extra in Docs (1 removal)

| ID | Property | Issue |
|----|----------|-------|
| C1 | `QuestionRevision.TopicPath` | Not in metadata; replaced by `TopicId`/`Topic` nav |

**Verified:** `TopicPath` is absent from both entity code and `$metadata`. The docs are outdated.
The JSON example (line 45) shows `"TopicPath": "SubjectiveQuestions"` which is historical.

**Action:** Remove `TopicPath` property, add `TopicId` + `Topic` nav (B20-B21). Note in
description that `TopicPath` was removed.

---

## D. NOTNULL — Missing :notnull: Flags (13 additions)

From code: non-nullable CLR types (`int`, `long`, `bool`, `DateTimeOffset` without `?`).

| Property | CLR Type | Reason |
|----------|----------|--------|
| `AssessmentRevision.AssessmentId` | `long` | Non-nullable |
| `AssessmentRevision.CreatedDateTime` | `DateTimeOffset` | Non-nullable |
| `AssessmentRevision.IsDeleted` | `bool` | Non-nullable |
| `AssessmentRevision.ModifiedDateTime` | `DateTimeOffset` | Non-nullable |
| `QuestionRevision.QuestionId` | `long` | Non-nullable |
| `QuestionRevision.CreatedDateTime` | `DateTimeOffset` | Non-nullable |
| `QuestionRevision.IsDeleted` | `bool` | Non-nullable |
| `QuestionRevision.ModifiedDateTime` | `DateTimeOffset` | Non-nullable |
| `Topic.CreatedDateTime` | `DateTimeOffset` | Non-nullable |
| `Topic.ModifiedDateTime` | `DateTimeOffset` | Non-nullable |
| `Topic.PublishedId` | `int` | Non-nullable |

---

## Edit Plan

1. **A1–A3:** Fix `ModifiedDateTime` type from `Edm.String` → `Edm.DateTimeOffset`
2. **B1–B9:** Add all 9 properties to `assessment_aml.rst`
3. **B10–B18:** Add all 9 properties to `question_qml.rst`
4. **B19:** Add `AssessmentName` to `assessment_revision.rst`
5. **B20–B21:** Add `TopicId` and `Topic` nav to `question_revision.rst`
6. **C1:** Remove or note `TopicPath` (verify with live endpoint first)
7. **D1–D11:** Add `:notnull:` flags across 3 files

---

## Verified

All findings verified against:
- `qm-AuthoringApi/solution/QM.AuthoringApi.OData.Entity/*.cs`
- `ignore/metadata-baselines/authoring.2026-07-13.metadata.xml`

Ready to apply edits.

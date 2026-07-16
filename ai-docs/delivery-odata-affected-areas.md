# Delivery OData API - Affected Objects & Properties

Summary of documentation gaps and fixes for the Delivery OData API, organized by entity/type and property name.

**Generated:** 2026-07-15  
**Total findings:** 78 items

---

## Affected Items

| Entity/Type | Property/Action | Issue | Metadata Reflects Fix? |
|-------------|-----------------|-------|------------------------|
| **ActionableSchedule** | `AssessmentID` | Missing from docs (Edm.Int64, non-nullable) | ✅ Yes |
| **Administrator** | `Blocked` | Missing `:notnull:` flag | ✅ Yes |
| **Administrator** | `Upsert` action | Return type `UpsertAdministratorResponse` not documented | ✅ Yes |
| **Administrator** | `ActionableSchedulesForObservation` action | Missing `ScheduleID` input parameter | ✅ Yes |
| **Answer** | `Revision` | Missing `:notnull:` flag | ✅ Yes |
| **Appointment** | `ExternalAppointmentData` | Missing from docs (Edm.String) | ✅ Yes |
| **AssessmentMetadata** | `Key` | Docs say non-null, metadata says nullable | ❌ No (service enforces it) |
| **AssessmentMetadata** | `Value` | Missing `:notnull:` flag | ✅ Yes |
| **AssessmentTranslation** | `Description` | Missing from docs (Edm.String) | ✅ Yes |
| **Attempt** | `ParticipantID` | Docs say non-null, metadata says nullable | ❌ No (service enforces it) |
| **Attempt** | `BranchedResults` | Missing `:collection:` flag | ✅ Yes |
| **AttemptList** | `ExternalAttemptListID` | Docs say non-null, metadata says nullable | ❌ No (service enforces it) |
| **AttemptMetadata** | `AttemptId` | **Casing wrong** - documented as `AttemptID` | ✅ Yes |
| **AttemptMetadata** | `Key` | Docs say non-null, metadata says nullable | ❌ No (service enforces it) |
| **AttemptMetadata** | `Value` | Docs say non-null, metadata says nullable | ❌ No (service enforces it) |
| **AttemptMetadataKeyValue** | `Key` | Docs say non-null, metadata says nullable | ❌ No (service enforces it) |
| **AttemptMetadataKeyValue** | `Value` | Docs say non-null, metadata says nullable | ❌ No (service enforces it) |
| **MonitoringType** | `Name` | Missing `:notnull:` flag | ✅ Yes |
| **MonitoringType** | `TextToSpeech` | Missing `:notnull:` flag | ✅ Yes |
| **MonitoringType** | `RequireObserver` | Missing `:notnull:` flag | ✅ Yes |
| **MonitoringType** | `RequireConfirmation` | Missing `:notnull:` flag | ✅ Yes |
| **MonitoringType** | `RequirePasscode` | Missing `:notnull:` flag | ✅ Yes |
| **MonitoringType** | `Disabled` | Missing `:notnull:` flag | ✅ Yes |
| **Participant** | `Blocked` | Missing `:notnull:` flag | ✅ Yes |
| **Participant** | `ActionableSchedules` action | Missing `ShowHidden` input parameter | ✅ Yes |
| **Participant** | `Upsert` action | Return type not documented | ✅ Yes |
| **Participant** | `ScheduleAndLaunch` action | Return type not documented | ✅ Yes |
| **Participant** | `UpsertParticipantAndSchedule` action | Return type not documented | ✅ Yes |
| **PracticeAttempt(s)** | *entire feed/type* | Documented but not in baseline metadata | ⏳ Pending deployment |
| **PrintBatchUpload** | `ID`, `PrintBatchId`, `RequestData`, `PrecessedDateTime`, `PrintBatch` | All properties missing from docs | ✅ Yes |
| **PrintBatchUpload** | `PrecessedDateTime` | Misspelled in service (should be "Processed") | ❌ No (typo in service) |
| **PrintBatchUploads** | *feed* | POST method not documented | ✅ Yes |
| **ProctoringProvider** | `Name` | Missing `:notnull:` flag | ✅ Yes |
| **ProctoringProvider** | `Protocol` | Missing `:notnull:` flag | ✅ Yes |
| **Question** | `Rubric` | Missing `:collection:` flag | ✅ Yes |
| **Result** | `AssessmentID` | Docs say non-null, metadata says nullable | ❌ No (service enforces it) |
| **Result** | `ReplayResultsByDateRange` action | Parameter types wrong (String not DateTime) | ✅ Yes |
| **Result** | `ReplayResultsByIDList` action | Return type not documented | ✅ Yes |
| **ResultAuditLog** | `IsInQueue` | Typo - trailing quote in docs | ✅ Yes |
| **Role** | `ID` → `Name` | Key property is `Name`, not `ID` | ✅ Yes |
| **Role** | `Administrators` | Missing navigation property | ✅ Yes |
| **Rubric** | `ShowParticipant` | Wrong type (Edm.Double, not String) | ✅ Yes (but semantically odd) |
| **RulesOfConduct** | `AllowedResources` | Missing from docs | ✅ Yes |
| **RulesOfConduct** | `CreatedDateTime` | Missing `:notnull:` flag | ✅ Yes |
| **RulesOfConduct** | `ModifiedDateTime` | Missing `:notnull:` flag | ✅ Yes |
| **RulesOfConductTranslation** | `AllowedResources` | Missing from docs | ✅ Yes |
| **RulesOfConductTranslation** | `Language` | Missing `:notnull:` flag | ✅ Yes |
| **RulesOfConductTranslation** | `CreatedDateTime` | Missing `:notnull:` flag | ✅ Yes |
| **RulesOfConductTranslation** | `ModifiedDateTime` | Missing `:notnull:` flag | ✅ Yes |
| **RulesOfConduct** | `RulesOfConductTranslations` | Nav property syntax wrong | ✅ Yes |
| **Schedule** | `ExternalProctoringID` | Missing from docs (read-only) | ✅ Yes |
| **Schedule** | `IsDeleted` | Missing `:notnull:` flag | ✅ Yes |
| **ScheduleMetadata** | `Key` | Docs say non-null, metadata says nullable | ❌ No (service enforces it) |
| **ScheduleMetadata** | `Value` | Docs say non-null, metadata says nullable | ❌ No (service enforces it) |
| **ScoringTask** | `ScoringResult` | Nav property syntax wrong | ✅ Yes |
| **ScoringTask** | `Dimension` | Nav property syntax wrong | ✅ Yes |
| **TestCenter** | `ID` | Missing `:key:` flag | ✅ Yes |
| **TestCenter** | `Name` | Missing `:notnull:` flag | ✅ Yes |
| **Timezone** | `CurrentUtcTime` | **Casing wrong** - must be `CurrentUTCTime` | ✅ Yes |
| **Timezone** | `BaseUTCOffsetMinutes` | Missing `:notnull:` flag | ✅ Yes |
| **Timezone** | `CurrentUTCOffsetMinutes` | Missing `:notnull:` flag | ✅ Yes |
| **Timezone** | `CurrentTimezoneTime` | Missing `:notnull:` flag | ✅ Yes |
| **GetAccessUrl** | *action* | Return type missing in metadata | ❌ No (service bug) |
| **CanLiveProctor** | *action* | Return type missing in metadata | ❌ No (service bug) |
| **AvailableAppointments** | *action* | Returns wrong type in metadata | ❌ No (service bug) |

---

## New Response Types (not currently documented)

| Type | Properties |
|------|------------|
| `UpsertParticipantResponse` | `ParticipantID` |
| `UpsertAdministratorResponse` | `AdministratorID` |
| `UpsertParticipantAndScheduleResponse` | `ParticipantID`, `ScheduleID` |
| `CustomScheduleAndLaunchResponse` | `ScheduleID`, `LaunchURL` |
| `PublishResultResponse` | `SuccessCount`, `FailureCount`, `Message`, `FailureResultIds` |

---

## Legend

| Status | Meaning |
|--------|---------|
| ✅ Yes | Metadata is correct; docs will be updated to match |
| ❌ No | Docs are correct; service/metadata needs fixing (ticket required) |
| ⏳ Pending | Code exists but not yet deployed to baseline tenant |

---

## Critical Items (can cause 404 errors)

1. **AttemptMetadata.AttemptId** - use lowercase `d`
2. **Timezone.CurrentUTCTime** - use uppercase `UTC`
3. **Role** - key is `Name`, not `ID`

---



# Rail: service inventory

The three OData services documented (or redirected) by this repository. Tenant
`406611` is used for live `$metadata` capture.

| Aspect | Delivery | Authoring | Results |
|--------|----------|-----------|---------|
| OData version | v3 | v4 | v3 |
| Source repo | `qm-DeliveryOData` | `qm-AuthoringApi` | analytics/reporting service |
| Owning team | Delivery QM / Firestar | Team Aurora | (reporting) |
| Docs location | `src/deliveryodata/` | `src/authoringodata/` | `src/resultsodata.rst` (stub) |
| Doc strategy | `od:` directives | `od:` directives | Help Center redirect (ADR-0003) |
| Namespace | (Delivery OData) | (Authoring) | `QM.Reporting.Services.OData` |

## Live `$metadata` endpoints

| Service | URL |
|---------|-----|
| Delivery | `https://ondemand.questionmark.com/deliveryodata/406611/$metadata` |
| Authoring | `https://ondemand.questionmark.com/authoringapi/406611/odata/$metadata` |
| Results | `https://ondemand.questionmark.com/analyticsodata/406611/odata/$metadata` |

Note the path shapes differ per service (`/deliveryodata/<tenant>/`,
`/authoringapi/<tenant>/odata/`, `/analyticsodata/<tenant>/odata/`).

## Source-of-truth files (Delivery)

For Delivery OData, the authoritative sources in `qm-DeliveryOData` are:

| Aspect | Source of truth |
|--------|-----------------|
| Feed (entity set) names | `App_Start/ODataConfig.cs` (`ConfigureEntitySets`) |
| Type properties and keys | `QM.Delivery.ODataService.Entity/*.cs` + DAL `EntityMappings/*.cs` |
| Bound/unbound actions | `ODataConfig.cs` + `Controllers/*.cs` |

## Results service (redirect only)

Live at the `analyticsodata` path (v3), 14 entity sets: Participants, Topics,
JTADimensions, JTAPoints, JTAAnswers, TopicScores, Results, Groups, Questions,
AssessmentQuestionLinks, Choices, Outcomes, Assessments, Answers. Documented via a
redirect to the Questionmark Help Center, not `od:` directives (ADR-0003).

## Snapshot baselines

`fetch_baselines.ps1` writes dated copies to `ignore/metadata-baselines/`:

- `delivery.<date>.metadata.xml` (~189 KB)
- `authoring.<date>.metadata.xml` (~5.5 KB)
- `results.<date>.metadata.xml` (~33 KB)

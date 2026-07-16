# ADR-0003: Results OData docs redirect to the Help Center

**Status:** Accepted

## Context

The Results OData service is live at the `analyticsodata` path
(`https://ondemand.questionmark.com/analyticsodata/<tenant>/odata/$metadata`,
OData v3, namespace `QM.Reporting.Services.OData`). Its `$metadata` exposes 14
entity sets (Participants, Topics, JTADimensions, JTAPoints, JTAAnswers,
TopicScores, Results, Groups, Questions, AssessmentQuestionLinks, Choices,
Outcomes, Assessments, Answers).

Earlier 404s were caused by probing the wrong path (`resultsapi`), not by the
service being absent. Despite the service existing, the product decision is that
Results is documented on the Questionmark Help Center, not with inline `od:`
directives in this repository.

## Decision

Do **not** document Results OData with `od:` directives here. `src/resultsodata.rst`
remains a stub that redirects readers to the canonical Results API guide on the
Help Center. The reconciliation tooling is still run against the Results
`$metadata` for awareness, but a full 0-vs-14 "missing in docs" report for Results
is **expected and intentional**, not a defect to fix.

## Consequences

- Results is intentionally out of scope for the `od:` audit; its reconciliation
  report will always show all feeds/types as "missing in docs" by design.
- The only maintenance task for Results here is keeping the stub's redirect link
  and wording correct and current.
- If the product decision ever changes, this ADR is superseded and the 14 entity
  sets are documented using the `od:` domain like Delivery and Authoring.

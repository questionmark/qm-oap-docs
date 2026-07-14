# Rails — operational guardrails

Practical, do-this guidance for keeping the OData documentation correct. Where
ADRs (`ai-docs/adrs/`) record *why* decisions were made, rails record *how* to
carry out recurring work safely.

| Rail | Purpose |
|------|---------|
| [reconciliation-workflow.md](reconciliation-workflow.md) | Step-by-step: refresh baselines, run the reconciler, triage findings, fix docs. |
| [editing-od-directives.md](editing-od-directives.md) | Rules for editing `od:` directives (exact names, keys, casing) without breaking the build. |
| [service-inventory.md](service-inventory.md) | The three services: endpoints, source repos, owning teams, doc locations, OData version. |

## First principles (see ADR-0001)

1. Docs follow code. `$metadata` is the contract; controllers are the final word
   on behaviour metadata cannot express.
2. Never invent feeds, types, properties, or names — copy them verbatim from the
   service.
3. A real code/metadata mismatch is a service bug: raise it with the owning team;
   do not "fix" it by degrading the docs.
4. Keep diffs minimal and scoped; preserve existing anchors and cross-references
   so external links stay stable.

# Incremental Adoption and Migration Protocol

## Purpose

This protocol brings an established project under IEPE without rewriting history, disrupting active delivery, or converting unsupported legacy claims into evidence maturity.

## Migration classes

Every legacy item is placed into one of three classes.

| Class | Meaning | Required treatment |
| --- | --- | --- |
| Historical | Closed or dormant work not required for current authority, dependency, or evidence | Preserve identity and source status; do not enrich by default |
| Active | Work currently claimed, under review, blocked, or required by an active dependency | Reconcile intent, ownership, relationships, acceptance, evidence, permissions, and status |
| New | Work committed after the adoption boundary | Require the complete IEPE issue contract before execution |

Migration is demand-driven. Historical records are reconciled only when they become relevant to authority, dependency, incident analysis, promotion, or evidence.

## Adoption boundary

The project records one adoption boundary containing:

- effective time or project revision
- governing protocol version
- project profile
- coordinator identity
- provider and work-graph identity
- migration owner
- protected actions
- rollback condition

Items created after this boundary follow IEPE. Earlier items retain their original identity and status semantics.

## Reconciliation packet

An active legacy item cannot become `Ready` until the migration process resolves:

- governing intent or an explicit unresolved-intent blocker
- owning project, repository, or workspace
- native parent and dependency relationships
- current actor or claim
- acceptance criteria
- evidence already present
- evidence still required
- side-effect permissions
- stop conditions
- mapping between source status and IEPE workflow status
- claim maturity supported by existing evidence

Missing provenance is recorded as missing. It is never reconstructed from confidence or status labels.

## Status mapping

Source status and IEPE status are separate fields. A migration adapter may recommend a target workflow state, but it must retain the source value and mapping rationale.

Examples:

| Source condition | IEPE recommendation |
| --- | --- |
| Open with complete contract and no blocker | Ready |
| Open with active claim | In progress after claim reconciliation |
| Pull request awaiting review | In review when the PR relationship is proven |
| Closed with merged artifact | Done only when repository gates are proven |
| Deployed and observed | Verified only when required observation evidence is retained |
| Closed without evidence | Historical source status retained; claim maturity remains unresolved |

## Migration sequence

```text
Inventory
  -> Classify
  -> Preserve source identity
  -> Reconcile active work
  -> Validate new-work gate
  -> Audit relationships
  -> Record evidence gaps
  -> Pilot one vertical slice
  -> Activate adoption boundary
```

## Rollback

Migration adds IEPE metadata and relationships without deleting source identity. If the adoption fails, stop coordinator claims, preserve migration records, restore the previous operational workflow, and retain the failure as a negative result.

## Stop conditions

- provider-native identity or relationships would be destroyed
- a field mapping changes the meaning of source status
- the owning workspace cannot be established
- provenance required for a promotion claim is absent
- automation would advance or close work without evidence
- the coordinator cannot distinguish historical from active work

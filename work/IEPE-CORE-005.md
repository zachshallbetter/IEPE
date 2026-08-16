# IEPE-CORE-005: Define Incremental Adoption and Migration

## Intent

Allow established projects to adopt IEPE without rewriting history, disrupting current delivery, or assigning unsupported evidence maturity to legacy work.

## Type

Delivery

## Parent

M1: Adoption Kit

## Objective

Define a provider-neutral migration protocol, legacy-item classification, minimum field mapping, reconciliation procedure, and pilot acceptance test.

## Acceptance criteria

- Migration distinguishes historical, active, and new work.
- Legacy status is not treated as evidence maturity.
- New committed work uses complete IEPE issue contracts.
- Active work receives a bounded reconciliation packet.
- Historical work is migrated only when needed for authority, dependency, or evidence.
- Native relationships remain authoritative where the provider supports them.
- Migration has rollback and stop conditions.
- One synthetic legacy backlog fixture passes the migration procedure.

## Evidence required

- Migration specification.
- Field and status mapping.
- Synthetic before-and-after backlog fixture.
- Reconciliation evidence.
- Conformance results.

## Constraints

- Do not require wholesale historical conversion.
- Do not invent missing provenance.
- Do not close or advance work merely because fields were mapped.
- Remain project-management-provider neutral.

## Permissions

- Local project artifacts: allowed.
- External project mutation: not authorized.

## Stop conditions

- Migration would destroy provider-native identity or relationships.
- Required provenance cannot be established.
- A field mapping changes the semantic meaning of an existing status.

## Status

Verified

## Claim maturity

Tested

## Result

The migration protocol and synthetic backlog fixture passed conformance. Historical identity was preserved, active work retained explicit evidence gaps, and new work remained gated by the full issue contract. No status or maturity was inferred from a legacy label alone.

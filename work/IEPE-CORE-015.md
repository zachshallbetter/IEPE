# IEPE-CORE-015: Qualify Worker Evidence Intake

## Intent

Convert worker artifacts and observations into evidence assertions without allowing completion language or adapter success to overstate maturity.

## Type

Delivery

## Parent

M2: Coordinator Reference

## Owner

IEPE Core coordinator

## Dependencies

- IEPE-CORE-006
- IEPE-CORE-007
- IEPE-CORE-008
- IEPE-CORE-014

## Objective

Implement evidence qualification rules that bind worker output to dispatch lineage, evaluate multi-dimensional evidence, retain negative results, and block overclaimed maturity promotion.

## Scope

- Define intake binding across worker dispatches, candidates, evaluators, and environments.
- Enforce structural separation between artifact creation, execution, testing, and empirical validation.
- Implement qualification checks that reject missing provenance, unverified assertions, or invalid claims.
- Retain negative and inconclusive evidence bundles for institutional memory.

## Acceptance criteria

- Intake binds evidence to dispatch, issue, candidate, environment, and evaluator.
- Artifact existence is distinct from evaluation.
- Qualification cannot exceed its strongest valid evidence.
- Missing provenance, reproduction, or required dimensions blocks promotion recommendation.
- Negative and inconclusive results remain retained.
- Tests cover documented, implemented, tested, invalid, and overclaimed evidence.

## Evidence required

- Coordinator evidence qualification unit tests.
- Validation results for valid, invalid, and overclaimed evidence bundles.
- Negative-result retention receipts.

## Constraints

- Domain-neutral evaluator interfaces only.
- Do not grant authority based on worker self-reporting or completion text.
- Maintain four-tier maturity taxonomy.

## Exclusions

- Domain-specific test runner adapters.
- Provider-specific webhooks.

## Permissions

- Write within `IEPE-Core` and temporary test directories.
- No network, external repository, deployment, or spending authority.

## Budget

- One bounded implementation cycle with local deterministic tests.

## Stop conditions

- An evidence claim cannot be evaluated without domain-specific runtime assumptions.
- Invalid provenance or missing issue contracts cannot be trapped by coordinator intake.

## Status

Ready

## Claim maturity

Specified


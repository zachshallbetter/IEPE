# IEPE-CORE-003: Implement the M1 Conformance Runner

## Intent

Make IEPE contract validation reproducible by adopters rather than dependent on an undocumented evaluator environment.

## Type

Delivery

## Parent

M1: Adoption Kit

## Objective

Provide one documented command that validates schemas, positive and negative fixtures, evidence records, GitHub issue templates, schema identifier uniqueness, and domain-neutrality constraints.

## Acceptance criteria

- Development dependencies are declared.
- A repository-owned validation command exists.
- Every schema has a representative valid fixture.
- Every schema rejects an empty invalid fixture.
- Evidence records validate against the evidence schema.
- GitHub templates parse and contain unique body field identifiers.
- Forbidden domain references and unresolved placeholders fail validation.
- The command returns nonzero on failure.
- README documents the command.

## Evidence required

- Clean command output.
- Deliberate invalid-fixture rejection.
- Evidence bundle validated by the runner.

## Constraints

- Validation tooling must remain independent from a specific project domain.
- Do not implement the operational coordinator in this issue.
- Do not claim empirical validation.

## Permissions

- Local project writes: allowed.
- Temporary dependency installation: allowed.
- External publishing and deployment: not authorized.

## Stop conditions

- Required validation cannot run in a clean Python environment with declared dependencies.
- The runner must weaken a schema to make fixtures pass.

## Status

Verified

## Claim maturity

Tested

## Result

The repository now carries its declared validation dependencies, positive and negative fixtures, and a single conformance command. The runner passed the complete current suite and returned a nonzero status during a deliberate domain-term violation probe. See `evidence/IEPE-CORE-003-evidence.json`.

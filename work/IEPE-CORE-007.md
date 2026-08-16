# IEPE-CORE-007: Replace String Gates with Typed Coordinator Assertions

## Intent

Prevent callers from satisfying coordinator gates with unstructured strings that are syntactically present but semantically unsupported.

## Type

Delivery

## Parent

M2: Coordinator Reference

## Objective

Introduce typed assertions, assertion provenance, gate policies, and explicit readiness failures while preserving provider neutrality.

## Acceptance criteria

- Gate assertions have type, subject, issuer, evidence references, and validity.
- Required gates accept only matching valid assertion types.
- Assertions for the wrong issue or subject fail.
- Invalidated assertions fail.
- Transition receipts retain assertion identity rather than only text.
- Existing valid delivery and experiment paths continue to pass.
- Tests cover wrong type, wrong subject, invalid assertion, and complete typed paths.

## Evidence required

- Typed assertion model.
- Gate-policy tests.
- Updated execution traces.
- Conformance results.

## Constraints

- No identity-provider dependency.
- No cryptographic implementation in this issue.
- Preserve simple adapter construction for pilots.

## Permissions

- Local code, tests, fixtures, and documentation: allowed.
- External actions: not authorized.

## Stop conditions

- Typed assertions require provider-specific identity semantics.
- Compatibility requires weakening an existing stop-state test.

## Status

Verified

## Claim maturity

Tested

## Result

Coordinator gates now require typed, issue-bound, valid assertions carrying issuer and evidence references. Valid delivery and experiment cycles continue to complete. Wrong types, wrong subjects, invalidated assertions, missing gates, and invalid transitions are rejected. Ten automated tests pass.

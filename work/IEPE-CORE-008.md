# IEPE-CORE-008: Persist and Replay Coordinator Receipts

## Intent

Allow coordinator work to survive interruption and be audited or resumed without reconstructing state from conversation memory.

## Type

Delivery

## Parent

M2: Coordinator Reference

## Objective

Define a versioned receipt format, deterministic serialization, integrity checking, and replay validation for completed and stopped coordinator executions.

## Acceptance criteria

- Receipts serialize deterministically.
- Receipt format is versioned.
- State history, assertion identities, artifacts, and stop records persist.
- Replay rejects impossible transition history.
- Replay rejects altered receipt content through an integrity digest.
- Completed and stopped receipts round-trip.
- No external database is required.

## Evidence required

- Receipt schema or typed model.
- Round-trip tests.
- Tamper and invalid-history tests.
- Conformance results.

## Constraints

- Local file or byte representation only.
- No production durability claim.
- No provider-specific storage.

## Permissions

- Local code, tests, fixtures, and documentation: allowed.
- External actions: not authorized.

## Stop conditions

- Replay requires trusting unverified state transitions.
- Serialization discards assertion or stop provenance.

## Status

Verified

## Claim maturity

Tested

## Result

Coordinator receipts now serialize deterministically into a versioned envelope with a SHA-256 payload digest. Completed and stopped receipts round-trip. Replay rejects changed content, unsupported versions, impossible histories, wrong assertion subjects, incomplete assertion provenance, and nonterminal outcomes. Eighteen total reference tests pass.

# IEPE-CORE-006: Implement the Coordinator State Machine

## Intent

Move IEPE from a documented coordination sequence to an executable, provider-neutral reference state machine.

## Type

Delivery

## Parent

M2: Coordinator Reference

## Objective

Implement coordinator state, transition rules, stop-state handling, execution receipts, and a deterministic local simulation for delivery and experiment work.

## Acceptance criteria

- Coordinator states match `docs/COORDINATOR.md`.
- Only declared transitions are permitted.
- Invalid authority, context, ownership, dependencies, permission, budget, and evidence can stop execution.
- A stop record identifies the reason and resumption authority.
- Delivery and experiment simulations complete valid paths.
- Invalid transitions and missing readiness evidence fail.
- State history is retained as a receipt.
- Implementation has no project-management-provider dependency.

## Evidence required

- Automated state-transition tests.
- Successful delivery trace.
- Successful experiment trace.
- Stop-state and invalid-transition traces.
- Conformance results.

## Constraints

- Local deterministic reference only.
- No worker process spawning.
- No external provider mutation.
- No production-readiness claim.

## Permissions

- Local code, tests, fixtures, and documentation: allowed.
- External writes, deployment, communication, and spending: not authorized.

## Stop conditions

- Implementation requires provider-specific concepts in the core state model.
- A test must bypass an authority or evidence gate to complete.

## Status

Verified

## Claim maturity

Tested

## Result

The provider-neutral coordinator state machine completed valid delivery and experiment paths and rejected invalid transitions, missing gate evidence, premature artifacts, and nonterminal receipts. Stop records retain the originating state, reason, evidence, and resumption authority. Seven automated tests pass.

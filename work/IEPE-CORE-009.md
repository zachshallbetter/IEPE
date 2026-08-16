# IEPE-CORE-009: Implement Claim Capacity and Conflict Management

## Intent

Prevent the coordinator from dispatching overlapping or excessive work that violates project ownership, resource limits, or isolation boundaries.

## Type

Delivery

## Parent

M2: Coordinator Reference

## Objective

Implement typed claims, capacity limits, workspace conflict detection, expiration, release, and receipt integration.

## Acceptance criteria

- Claims identify issue, agent, workspace, scope, and expiration.
- Coordinator capacity is enforced.
- Overlapping mutable scope is rejected.
- Read-only scope may coexist when policy permits.
- Expired claims cannot authorize dispatch.
- Release is idempotent and recorded.
- Claim assertions are derived from valid claim state.
- Tests cover capacity, overlap, expiration, coexistence, and release.

## Evidence required

- Claim model and registry.
- Positive and negative tests.
- Updated coordinator integration.
- Conformance results.

## Constraints

- In-memory reference registry only.
- No provider-specific lock service.
- No distributed-consensus claim.

## Permissions

- Local code, tests, fixtures, and documentation: allowed.
- External actions: not authorized.

## Stop conditions

- Scope overlap cannot be represented without provider-specific paths.
- Claim release can silently erase execution history.

## Result

The reference registry enforces global capacity, isolates workspaces, detects hierarchical mutable-scope conflicts, permits read-only coexistence, expires authority, records repeated release attempts, and derives subject-bound claim assertions from active state.

## Status

Verified / Tested

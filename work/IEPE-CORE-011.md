# IEPE-CORE-011: Assemble Bounded Context Packets

## Intent

Give a worker the minimum sufficient, authority-ordered context required to execute one claimed issue without silently expanding scope.

## Type

Delivery

## Parent

M2: Coordinator Reference

## Acceptance criteria

- Packets bind issue, claim, intent, authority, dependencies, constraints, evidence requirements, permissions, and stop conditions.
- Missing mandatory context blocks dispatch.
- Authority conflicts are surfaced rather than flattened.
- Packet construction is deterministic and provider-neutral.
- Tests cover complete, missing, conflicting, and excess-context cases.

## Result

Context packets now bind issue and active claim, order selected sources by authority, include dependency state and execution boundaries, surface conflicts, omit unrelated corpus material, enforce a source limit, and retain a deterministic digest.

## Status

Verified / Tested

# IEPE-CORE-014: Define Worker Dispatch Interfaces

## Intent

Dispatch a bounded context packet to a worker through a provider-neutral interface while preserving worker identity, permissions, result provenance, and stop-state behavior.

## Type

Delivery

## Parent

M2: Coordinator Reference

## Acceptance criteria

- Dispatch binds issue, claim, context digest, worker identity, role, and attempt.
- Provider adapters cannot expand packet permissions.
- Worker results distinguish completed, failed, blocked, and stopped outcomes.
- Results retain artifact, observation, command, cost, and limitation references.
- Duplicate dispatch and stale result conditions are rejected.
- Tests cover success, failure, permission expansion, stale context, and retry identity.

## Result

Dispatch envelopes now bind worker identity, role, issue, claim, context digest, permissions, and attempt. Results preserve distinct terminal outcomes and evidence provenance. Stale context, permission expansion, duplicate work, and invalid retry lineage are rejected.

## Status

Verified / Tested

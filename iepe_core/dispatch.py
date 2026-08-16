"""Provider-neutral worker dispatch and result provenance."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .claims import ClaimRegistry
from .context import ContextPacket


class WorkerOutcome(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    STOPPED = "stopped"


@dataclass(frozen=True)
class DispatchEnvelope:
    id: str
    issue_id: str
    claim_id: str
    context_sha256: str
    worker_id: str
    role: str
    attempt: int
    permissions: tuple[tuple[str, bool], ...]


@dataclass(frozen=True)
class WorkerResult:
    dispatch_id: str
    issue_id: str
    claim_id: str
    context_sha256: str
    worker_id: str
    attempt: int
    outcome: WorkerOutcome
    artifacts: tuple[str, ...] = ()
    observations: tuple[str, ...] = ()
    commands: tuple[str, ...] = ()
    cost: float | None = None
    limitations: tuple[str, ...] = ()


class DispatchRegistry:
    def __init__(self) -> None:
        self._dispatches: dict[str, DispatchEnvelope] = {}
        self._results: dict[str, WorkerResult] = {}

    def dispatch(
        self,
        envelope: DispatchEnvelope,
        *,
        packet: ContextPacket,
        claims: ClaimRegistry,
        now: datetime,
    ) -> None:
        if envelope.id in self._dispatches:
            raise ValueError(f"Duplicate dispatch: {envelope.id}")
        if envelope.attempt < 1:
            raise ValueError("Dispatch attempt must be positive")
        record = packet.record
        if envelope.issue_id != record["issueId"] or envelope.claim_id != record["claimId"]:
            raise ValueError("Dispatch subject does not match context packet")
        if envelope.context_sha256 != packet.digest:
            raise ValueError("Dispatch context is stale or mismatched")
        if not claims.claim_assertion(envelope.claim_id, issue_id=envelope.issue_id, now=now).valid:
            raise ValueError("Dispatch requires a matching active claim")

        packet_permissions = record["permissions"]
        for name, value in envelope.permissions:
            if value and not packet_permissions.get(name, False):
                raise ValueError(f"Dispatch permission expansion: {name}")

        related = [item for item in self._dispatches.values() if item.issue_id == envelope.issue_id]
        if related:
            highest = max(item.attempt for item in related)
            previous = [item for item in related if item.attempt == highest][0]
            if previous.id not in self._results:
                raise ValueError("Previous dispatch is still active")
            if envelope.attempt != highest + 1:
                raise ValueError("Retry attempt must follow prior attempt")
        elif envelope.attempt != 1:
            raise ValueError("First dispatch must be attempt one")

        self._dispatches[envelope.id] = envelope

    def accept_result(self, result: WorkerResult) -> dict:
        envelope = self._dispatches.get(result.dispatch_id)
        if envelope is None:
            raise ValueError("Result references an unknown dispatch")
        if result.dispatch_id in self._results:
            raise ValueError("Duplicate worker result")
        expected = (envelope.issue_id, envelope.claim_id, envelope.context_sha256, envelope.worker_id, envelope.attempt)
        actual = (result.issue_id, result.claim_id, result.context_sha256, result.worker_id, result.attempt)
        if actual != expected:
            raise ValueError("Worker result provenance does not match dispatch")
        if result.cost is not None and result.cost < 0:
            raise ValueError("Worker result cost cannot be negative")
        self._results[result.dispatch_id] = result
        return self.record(result.dispatch_id)

    def record(self, dispatch_id: str) -> dict:
        envelope = self._dispatches[dispatch_id]
        result = self._results.get(dispatch_id)
        return {
            "$schema": "../schemas/worker-dispatch.schema.json",
            "id": envelope.id,
            "issueId": envelope.issue_id,
            "claimId": envelope.claim_id,
            "contextSha256": envelope.context_sha256,
            "workerId": envelope.worker_id,
            "role": envelope.role,
            "attempt": envelope.attempt,
            "permissions": {key: value for key, value in sorted(envelope.permissions)},
            "status": result.outcome.value if result else "active",
            "result": None if result is None else {
                "artifacts": list(result.artifacts),
                "observations": list(result.observations),
                "commands": list(result.commands),
                "cost": result.cost,
                "limitations": list(result.limitations),
            },
        }

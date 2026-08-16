"""Provider-neutral in-memory claim capacity and conflict management."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

from .coordinator import AssertionType, GateAssertion


class ClaimMode(str, Enum):
    READ = "read"
    WRITE = "write"


@dataclass(frozen=True)
class Claim:
    id: str
    issue_id: str
    agent_id: str
    workspace: str
    scopes: tuple[str, ...]
    mode: ClaimMode
    acquired_at: datetime
    expires_at: datetime


@dataclass(frozen=True)
class ClaimEvent:
    sequence: int
    claim_id: str
    action: str
    at: datetime
    reason: str | None = None


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("Claim timestamps must be timezone-aware")
    return value.astimezone(timezone.utc)


def _scope_parts(scope: str) -> tuple[str, ...]:
    normalized = scope.strip().strip("/")
    if not normalized:
        raise ValueError("Claim scope cannot be empty")
    return tuple(part for part in normalized.split("/") if part)


def scopes_overlap(left: str, right: str) -> bool:
    """Return true when either provider-neutral hierarchical scope contains the other."""
    left_parts = _scope_parts(left)
    right_parts = _scope_parts(right)
    common = min(len(left_parts), len(right_parts))
    return left_parts[:common] == right_parts[:common]


class ClaimRegistry:
    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("Claim capacity must be at least one")
        self.capacity = capacity
        self._claims: dict[str, Claim] = {}
        self._released: set[str] = set()
        self._events: list[ClaimEvent] = []

    @property
    def history(self) -> tuple[ClaimEvent, ...]:
        return tuple(self._events)

    def active(self, *, now: datetime) -> tuple[Claim, ...]:
        point = _utc(now)
        return tuple(
            claim
            for claim in self._claims.values()
            if claim.id not in self._released and _utc(claim.expires_at) > point
        )

    def acquire(self, claim: Claim, *, now: datetime) -> Claim:
        point = _utc(now)
        acquired = _utc(claim.acquired_at)
        expires = _utc(claim.expires_at)
        if claim.id in self._claims:
            raise ValueError(f"Claim id already exists: {claim.id}")
        if not claim.scopes:
            raise ValueError("Claim requires at least one scope")
        if acquired > point:
            raise ValueError("Claim acquisition cannot be in the future")
        if expires <= point or expires <= acquired:
            raise ValueError("Claim must expire after acquisition and after the current time")

        active = self.active(now=point)
        if len(active) >= self.capacity:
            raise ValueError("Coordinator claim capacity exceeded")
        for existing in active:
            if existing.workspace != claim.workspace:
                continue
            if claim.mode is ClaimMode.READ and existing.mode is ClaimMode.READ:
                continue
            if any(scopes_overlap(left, right) for left in claim.scopes for right in existing.scopes):
                raise ValueError(f"Claim scope conflicts with active claim: {existing.id}")

        self._claims[claim.id] = claim
        self._record(claim.id, "acquired", point)
        return claim

    def release(self, claim_id: str, *, now: datetime, reason: str | None = None) -> bool:
        point = _utc(now)
        if claim_id not in self._claims:
            raise KeyError(f"Unknown claim: {claim_id}")
        if claim_id in self._released:
            self._record(claim_id, "release-repeated", point, reason)
            return False
        self._released.add(claim_id)
        self._record(claim_id, "released", point, reason)
        return True

    def claim_assertion(self, claim_id: str, *, issue_id: str, now: datetime) -> GateAssertion:
        point = _utc(now)
        claim = self._claims.get(claim_id)
        valid = claim is not None and claim.issue_id == issue_id and claim in self.active(now=point)
        return GateAssertion(
            id=f"assertion.{issue_id}.claim.valid.{claim_id}",
            kind=AssertionType.CLAIM_VALID,
            subject=issue_id,
            issuer="coordinator.claim-registry",
            evidence_refs=(f"claim.{claim_id}",),
            valid=valid,
        )

    def _record(self, claim_id: str, action: str, at: datetime, reason: str | None = None) -> None:
        self._events.append(ClaimEvent(len(self._events) + 1, claim_id, action, at, reason))

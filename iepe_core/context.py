"""Deterministic, claim-bound context packet assembly."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
from typing import Mapping

from .claims import ClaimRegistry


@dataclass(frozen=True)
class ContextSource:
    ref: str
    kind: str
    authority_rank: int
    content: str
    assertion_subject: str | None = None

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.content.encode()).hexdigest()


@dataclass(frozen=True)
class ContextRequest:
    issue_id: str
    claim_id: str
    objective: str
    intent_refs: tuple[str, ...]
    authority_refs: tuple[str, ...]
    experience_refs: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()
    evidence_required: tuple[str, ...] = ()
    permissions: tuple[tuple[str, bool], ...] = ()
    stop_conditions: tuple[str, ...] = ()


@dataclass(frozen=True)
class ContextPacket:
    record: dict

    @property
    def digest(self) -> str:
        return self.record["contextSha256"]


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def assemble_context_packet(
    request: ContextRequest,
    *,
    registry: ClaimRegistry,
    now: datetime,
    sources: Mapping[str, ContextSource],
    dependency_records: Mapping[str, str],
    max_sources: int = 24,
) -> ContextPacket:
    if not request.issue_id or not request.objective:
        raise ValueError("Context request requires issue and objective")
    if not request.intent_refs or not request.authority_refs:
        raise ValueError("Context request requires intent and authority references")
    if not request.evidence_required or not request.stop_conditions:
        raise ValueError("Context request requires evidence and stop conditions")
    assertion = registry.claim_assertion(request.claim_id, issue_id=request.issue_id, now=now)
    if not assertion.valid:
        raise ValueError("Context packet requires a matching active claim")

    ordered_refs = tuple(dict.fromkeys(request.intent_refs + request.authority_refs + request.experience_refs))
    missing = sorted(ref for ref in ordered_refs if ref not in sources)
    if missing:
        raise ValueError(f"Missing mandatory context: {', '.join(missing)}")
    missing_dependencies = sorted(ref for ref in request.dependencies if ref not in dependency_records)
    if missing_dependencies:
        raise ValueError(f"Missing dependency state: {', '.join(missing_dependencies)}")
    if len(ordered_refs) > max_sources:
        raise ValueError("Bounded context source limit exceeded")

    selected = [sources[ref] for ref in ordered_refs]
    assertions: dict[str, str] = {}
    for source in selected:
        if source.assertion_subject is None:
            continue
        previous = assertions.get(source.assertion_subject)
        if previous is not None and previous != source.sha256:
            raise ValueError(f"Authority conflict for subject: {source.assertion_subject}")
        assertions[source.assertion_subject] = source.sha256

    selected.sort(key=lambda source: (source.authority_rank, source.ref))
    record = {
        "$schema": "../schemas/context-packet.schema.json",
        "id": f"context.{request.issue_id}.{request.claim_id}",
        "issueId": request.issue_id,
        "claimId": request.claim_id,
        "objective": request.objective,
        "sources": [
            {"ref": source.ref, "kind": source.kind, "authorityRank": source.authority_rank, "sha256": source.sha256}
            for source in selected
        ],
        "dependencies": {ref: dependency_records[ref] for ref in sorted(request.dependencies)},
        "constraints": list(request.constraints),
        "evidenceRequired": list(request.evidence_required),
        "permissions": {key: value for key, value in sorted(request.permissions)},
        "stopConditions": list(request.stop_conditions),
    }
    record["contextSha256"] = hashlib.sha256(_canonical(record)).hexdigest()
    return ContextPacket(record)

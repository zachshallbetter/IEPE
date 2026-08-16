"""Deterministic reference state machine for the IEPE operational coordinator."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class CoordinatorState(str, Enum):
    PREFLIGHT = "preflight"
    RECONCILE = "reconcile"
    SELECT = "select"
    VALIDATE = "validate"
    CLAIM = "claim"
    ASSEMBLE_CONTEXT = "assemble_context"
    DISPATCH = "dispatch"
    OBSERVE = "observe"
    EVALUATE = "evaluate"
    DISPOSITION = "disposition"
    RECORD = "record"
    CLOSE_LOOP = "close_loop"
    COMPLETE = "complete"
    STOPPED = "stopped"
    WAITING_EXTERNAL = "waiting_external"


class ConditionType(str, Enum):
    AUTHORIZATION_MISSING = "authorization_missing"
    CAPABILITY_MISSING = "capability_missing"
    EVIDENCE_MISSING = "evidence_missing"
    INPUT_MISSING = "input_missing"
    WORK_UNAVAILABLE = "work_unavailable"
    EXTERNAL_EVENT_PENDING = "external_event_pending"


@dataclass(frozen=True)
class BlockerFingerprint:
    code: str
    scope: str
    required_change: str
    retryable_by_agent: bool
    condition_type: ConditionType

    @property
    def fingerprint(self) -> str:
        return f"{self.code}:{self.scope}"


class AssertionType(str, Enum):
    PREFLIGHT_VALID = "preflight.valid"
    STATE_RECONCILED = "state.reconciled"
    ISSUE_SELECTED = "issue.selected"
    ISSUE_READY = "issue.ready"
    CLAIM_VALID = "claim.valid"
    CONTEXT_BOUNDED = "context.bounded"
    WORKER_DISPATCHED = "worker.dispatched"
    WORKER_RESULT = "worker.result"
    EVALUATION_COMPLETE = "evaluation.complete"
    DISPOSITION_SELECTED = "disposition.selected"
    RECORD_PERSISTED = "record.persisted"
    CLAIM_RELEASED = "claim.released"


ORDERED_PATH = (
    CoordinatorState.PREFLIGHT,
    CoordinatorState.RECONCILE,
    CoordinatorState.SELECT,
    CoordinatorState.VALIDATE,
    CoordinatorState.CLAIM,
    CoordinatorState.ASSEMBLE_CONTEXT,
    CoordinatorState.DISPATCH,
    CoordinatorState.OBSERVE,
    CoordinatorState.EVALUATE,
    CoordinatorState.DISPOSITION,
    CoordinatorState.RECORD,
    CoordinatorState.CLOSE_LOOP,
    CoordinatorState.COMPLETE,
)

ALLOWED_TRANSITIONS = {
    current: {ORDERED_PATH[index + 1], CoordinatorState.STOPPED, CoordinatorState.WAITING_EXTERNAL}
    for index, current in enumerate(ORDERED_PATH[:-1])
}
ALLOWED_TRANSITIONS[CoordinatorState.COMPLETE] = set()
ALLOWED_TRANSITIONS[CoordinatorState.STOPPED] = set()
ALLOWED_TRANSITIONS[CoordinatorState.WAITING_EXTERNAL] = set()


@dataclass(frozen=True)
class TransitionRecord:
    sequence: int
    source: CoordinatorState
    target: CoordinatorState
    assertion_ids: tuple[str, ...]


@dataclass(frozen=True)
class GateAssertion:
    id: str
    kind: AssertionType
    subject: str
    issuer: str
    evidence_refs: tuple[str, ...] = ()
    valid: bool = True


@dataclass(frozen=True)
class StopRecord:
    state: CoordinatorState
    reason: str
    resume_authority: str
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExecutionReceipt:
    issue_id: str
    work_type: str
    final_state: CoordinatorState
    transitions: tuple[TransitionRecord, ...]
    stop: StopRecord | None
    artifacts: tuple[str, ...]
    assertions: tuple[GateAssertion, ...]

    @property
    def assertion_ids(self) -> tuple[str, ...]:
        return tuple(assertion.id for assertion in self.assertions)


@dataclass
class Coordinator:
    issue_id: str
    work_type: str
    state: CoordinatorState = CoordinatorState.PREFLIGHT
    history: list[TransitionRecord] = field(default_factory=list)
    stop_record: StopRecord | None = None
    artifacts: list[str] = field(default_factory=list)
    retained_assertions: list[GateAssertion] = field(default_factory=list)
    last_blocker_fingerprint: str | None = None

    def transition(self, target: CoordinatorState, *, assertions: list[GateAssertion] | None = None) -> None:
        assertions = assertions or []
        if target not in ALLOWED_TRANSITIONS[self.state]:
            raise ValueError(f"Invalid coordinator transition: {self.state.value} -> {target.value}")
        self._enforce_gate(target, assertions)
        source = self.state
        self.state = target
        self.history.append(
            TransitionRecord(
                sequence=len(self.history) + 1,
                source=source,
                target=target,
                assertion_ids=tuple(assertion.id for assertion in assertions),
            )
        )
        self.retained_assertions.extend(assertions)

    def stop(self, reason: str, resume_authority: str, *, evidence: list[str] | None = None) -> None:
        if self.state in {CoordinatorState.COMPLETE, CoordinatorState.STOPPED, CoordinatorState.WAITING_EXTERNAL}:
            raise ValueError(f"Cannot stop coordinator from {self.state.value}")
        evidence = evidence or []
        stopped_from = self.state
        self.transition(CoordinatorState.STOPPED)
        self.stop_record = StopRecord(
            state=stopped_from,
            reason=reason,
            resume_authority=resume_authority,
            evidence=tuple(evidence),
        )

    def park_waiting_external(self, blocker: BlockerFingerprint, resume_authority: str) -> None:
        if self.last_blocker_fingerprint == blocker.fingerprint and not blocker.retryable_by_agent:
            raise ValueError(f"Duplicate non-retryable blocker fingerprint '{blocker.fingerprint}': do not retry")
        if self.state in {CoordinatorState.COMPLETE, CoordinatorState.STOPPED, CoordinatorState.WAITING_EXTERNAL}:
            raise ValueError(f"Cannot park coordinator from {self.state.value}")
        self.last_blocker_fingerprint = blocker.fingerprint
        stopped_from = self.state
        self.transition(CoordinatorState.WAITING_EXTERNAL)
        self.stop_record = StopRecord(
            state=stopped_from,
            reason=f"[{blocker.condition_type.value}] {blocker.code}: {blocker.required_change}",
            resume_authority=resume_authority,
            evidence=(f"fingerprint:{blocker.fingerprint}",),
        )

    def add_artifact(self, artifact_ref: str) -> None:
        if self.state in {CoordinatorState.PREFLIGHT, CoordinatorState.RECONCILE, CoordinatorState.SELECT}:
            raise ValueError("Artifacts cannot be accepted before issue validation")
        self.artifacts.append(artifact_ref)

    def receipt(self) -> ExecutionReceipt:
        if self.state not in {CoordinatorState.COMPLETE, CoordinatorState.STOPPED, CoordinatorState.WAITING_EXTERNAL}:
            raise ValueError("A receipt requires a terminal coordinator state")
        return ExecutionReceipt(
            issue_id=self.issue_id,
            work_type=self.work_type,
            final_state=self.state,
            transitions=tuple(self.history),
            stop=self.stop_record,
            artifacts=tuple(self.artifacts),
            assertions=tuple(self.retained_assertions),
        )

    def _enforce_gate(self, target: CoordinatorState, assertions: list[GateAssertion]) -> None:
        required = {
            CoordinatorState.RECONCILE: AssertionType.PREFLIGHT_VALID,
            CoordinatorState.SELECT: AssertionType.STATE_RECONCILED,
            CoordinatorState.VALIDATE: AssertionType.ISSUE_SELECTED,
            CoordinatorState.CLAIM: AssertionType.ISSUE_READY,
            CoordinatorState.ASSEMBLE_CONTEXT: AssertionType.CLAIM_VALID,
            CoordinatorState.DISPATCH: AssertionType.CONTEXT_BOUNDED,
            CoordinatorState.OBSERVE: AssertionType.WORKER_DISPATCHED,
            CoordinatorState.EVALUATE: AssertionType.WORKER_RESULT,
            CoordinatorState.DISPOSITION: AssertionType.EVALUATION_COMPLETE,
            CoordinatorState.RECORD: AssertionType.DISPOSITION_SELECTED,
            CoordinatorState.CLOSE_LOOP: AssertionType.RECORD_PERSISTED,
            CoordinatorState.COMPLETE: AssertionType.CLAIM_RELEASED,
        }.get(target)
        if not required:
            return
        matching = [assertion for assertion in assertions if assertion.kind is required]
        if not matching:
            raise ValueError(f"Transition to {target.value} requires assertion: {required.value}")
        assertion = matching[0]
        if assertion.subject != self.issue_id:
            raise ValueError(f"Assertion {assertion.id} has the wrong subject")
        if not assertion.valid:
            raise ValueError(f"Assertion {assertion.id} is invalid")


def make_assertion(kind: AssertionType, issue_id: str, *, valid: bool = True) -> GateAssertion:
    return GateAssertion(
        id=f"assertion.{issue_id}.{kind.value}",
        kind=kind,
        subject=issue_id,
        issuer="coordinator.reference-evaluator",
        evidence_refs=(f"evidence.{issue_id}.{kind.value}",),
        valid=valid,
    )


def simulate_valid_cycle(issue_id: str, work_type: str) -> ExecutionReceipt:
    coordinator = Coordinator(issue_id=issue_id, work_type=work_type)
    path = (
        (CoordinatorState.RECONCILE, AssertionType.PREFLIGHT_VALID),
        (CoordinatorState.SELECT, AssertionType.STATE_RECONCILED),
        (CoordinatorState.VALIDATE, AssertionType.ISSUE_SELECTED),
        (CoordinatorState.CLAIM, AssertionType.ISSUE_READY),
        (CoordinatorState.ASSEMBLE_CONTEXT, AssertionType.CLAIM_VALID),
        (CoordinatorState.DISPATCH, AssertionType.CONTEXT_BOUNDED),
        (CoordinatorState.OBSERVE, AssertionType.WORKER_DISPATCHED),
        (CoordinatorState.EVALUATE, AssertionType.WORKER_RESULT),
        (CoordinatorState.DISPOSITION, AssertionType.EVALUATION_COMPLETE),
        (CoordinatorState.RECORD, AssertionType.DISPOSITION_SELECTED),
        (CoordinatorState.CLOSE_LOOP, AssertionType.RECORD_PERSISTED),
        (CoordinatorState.COMPLETE, AssertionType.CLAIM_RELEASED),
    )
    for state, assertion_type in path:
        coordinator.transition(state, assertions=[make_assertion(assertion_type, issue_id)])
        if state is CoordinatorState.EVALUATE:
            coordinator.add_artifact(f"artifact.{issue_id}")
    return coordinator.receipt()

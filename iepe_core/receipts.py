"""Deterministic persistence and replay validation for coordinator receipts."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from .coordinator import ALLOWED_TRANSITIONS, AssertionType, CoordinatorState, ExecutionReceipt


RECEIPT_FORMAT = "iepe.coordinator-receipt"
RECEIPT_VERSION = 1

REQUIRED_ASSERTIONS = {
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
}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest_payload(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def receipt_payload(receipt: ExecutionReceipt) -> dict[str, Any]:
    return {
        "issueId": receipt.issue_id,
        "workType": receipt.work_type,
        "finalState": receipt.final_state.value,
        "transitions": [
            {
                "sequence": transition.sequence,
                "source": transition.source.value,
                "target": transition.target.value,
                "assertionIds": list(transition.assertion_ids),
            }
            for transition in receipt.transitions
        ],
        "assertions": [
            {
                "id": assertion.id,
                "kind": assertion.kind.value,
                "subject": assertion.subject,
                "issuer": assertion.issuer,
                "evidenceRefs": list(assertion.evidence_refs),
                "valid": assertion.valid,
            }
            for assertion in receipt.assertions
        ],
        "stop": None
        if receipt.stop is None
        else {
            "state": receipt.stop.state.value,
            "reason": receipt.stop.reason,
            "resumeAuthority": receipt.stop.resume_authority,
            "evidence": list(receipt.stop.evidence),
        },
        "artifacts": list(receipt.artifacts),
    }


def seal_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "format": RECEIPT_FORMAT,
        "version": RECEIPT_VERSION,
        "payload": payload,
        "sha256": digest_payload(payload),
    }


def seal_receipt(receipt: ExecutionReceipt) -> dict[str, Any]:
    return seal_payload(receipt_payload(receipt))


def serialize_receipt(receipt: ExecutionReceipt) -> bytes:
    return canonical_bytes(seal_receipt(receipt))


def load_and_validate_receipt(data: bytes | str) -> dict[str, Any]:
    envelope = json.loads(data)
    if envelope.get("format") != RECEIPT_FORMAT:
        raise ValueError("Unsupported receipt format")
    if envelope.get("version") != RECEIPT_VERSION:
        raise ValueError("Unsupported receipt version")
    payload = envelope.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("Receipt payload is missing")
    if envelope.get("sha256") != digest_payload(payload):
        raise ValueError("Receipt integrity check failed")
    validate_replay(payload)
    return envelope


def validate_replay(payload: dict[str, Any]) -> None:
    issue_id = payload.get("issueId")
    transitions = payload.get("transitions")
    assertion_rows = payload.get("assertions")
    if not isinstance(issue_id, str) or not issue_id:
        raise ValueError("Receipt issue identity is missing")
    if not isinstance(transitions, list) or not transitions:
        raise ValueError("Receipt transition history is missing")
    if not isinstance(assertion_rows, list):
        raise ValueError("Receipt assertions are missing")

    assertions: dict[str, dict[str, Any]] = {}
    for assertion in assertion_rows:
        assertion_id = assertion.get("id")
        if not isinstance(assertion_id, str) or assertion_id in assertions:
            raise ValueError("Receipt assertion identity is missing or duplicated")
        assertions[assertion_id] = assertion

    expected_source = CoordinatorState.PREFLIGHT
    for index, transition in enumerate(transitions, start=1):
        if transition.get("sequence") != index:
            raise ValueError("Receipt transition sequence is invalid")
        source = CoordinatorState(transition.get("source"))
        target = CoordinatorState(transition.get("target"))
        if source is not expected_source:
            raise ValueError("Receipt transition history is discontinuous")
        if target not in ALLOWED_TRANSITIONS[source]:
            raise ValueError("Receipt contains an impossible transition")

        required = REQUIRED_ASSERTIONS.get(target)
        transition_assertions = [assertions.get(value) for value in transition.get("assertionIds", [])]
        if any(assertion is None for assertion in transition_assertions):
            raise ValueError("Receipt transition references an unknown assertion")
        if required:
            matching = [assertion for assertion in transition_assertions if assertion["kind"] == required.value]
            if not matching:
                raise ValueError(f"Receipt transition lacks required assertion: {required.value}")
            assertion = matching[0]
            if assertion.get("subject") != issue_id:
                raise ValueError("Receipt assertion has the wrong subject")
            if assertion.get("valid") is not True:
                raise ValueError("Receipt assertion is invalid")
            if not assertion.get("issuer") or not assertion.get("evidenceRefs"):
                raise ValueError("Receipt assertion provenance is incomplete")
        expected_source = target

    final_state = CoordinatorState(payload.get("finalState"))
    if expected_source is not final_state:
        raise ValueError("Receipt final state does not match transition history")
    if final_state not in {CoordinatorState.COMPLETE, CoordinatorState.STOPPED, CoordinatorState.WAITING_EXTERNAL}:
        raise ValueError("Receipt final state is not terminal")
    stop = payload.get("stop")
    if final_state in {CoordinatorState.STOPPED, CoordinatorState.WAITING_EXTERNAL}:
        if not isinstance(stop, dict) or not stop.get("reason") or not stop.get("resumeAuthority"):
            raise ValueError("Stopped receipt is missing its stop record")
    elif stop is not None:
        raise ValueError("Completed receipt cannot contain a stop record")

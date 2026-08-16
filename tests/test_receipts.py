import copy
import json
import unittest

from iepe_core.coordinator import Coordinator, CoordinatorState, simulate_valid_cycle
from iepe_core.receipts import load_and_validate_receipt, seal_payload, seal_receipt, serialize_receipt


class ReceiptTests(unittest.TestCase):
    def test_completed_receipt_round_trips(self) -> None:
        receipt = simulate_valid_cycle("ROUNDTRIP-1", "delivery")
        envelope = load_and_validate_receipt(serialize_receipt(receipt))
        self.assertEqual(envelope["payload"]["finalState"], "complete")
        self.assertEqual(len(envelope["payload"]["assertions"]), 12)

    def test_stopped_receipt_round_trips(self) -> None:
        coordinator = Coordinator("STOPPED-ROUNDTRIP", "delivery")
        coordinator.stop("provider unavailable", "project owner", evidence=["provider.health.failed"])
        envelope = load_and_validate_receipt(serialize_receipt(coordinator.receipt()))
        self.assertEqual(envelope["payload"]["stop"]["resumeAuthority"], "project owner")

    def test_serialization_is_deterministic(self) -> None:
        receipt = simulate_valid_cycle("DETERMINISTIC-1", "experiment")
        self.assertEqual(serialize_receipt(receipt), serialize_receipt(receipt))

    def test_tampered_payload_fails_integrity(self) -> None:
        envelope = seal_receipt(simulate_valid_cycle("TAMPER-1", "delivery"))
        envelope["payload"]["workType"] = "altered"
        with self.assertRaisesRegex(ValueError, "integrity"):
            load_and_validate_receipt(json.dumps(envelope))

    def test_unsupported_version_fails(self) -> None:
        envelope = seal_receipt(simulate_valid_cycle("VERSION-1", "delivery"))
        envelope["version"] = 999
        with self.assertRaisesRegex(ValueError, "version"):
            load_and_validate_receipt(json.dumps(envelope))

    def test_impossible_history_fails_even_with_valid_digest(self) -> None:
        envelope = seal_receipt(simulate_valid_cycle("HISTORY-1", "delivery"))
        payload = copy.deepcopy(envelope["payload"])
        payload["transitions"][1]["target"] = "claim"
        resealed = seal_payload(payload)
        with self.assertRaisesRegex(ValueError, "impossible|discontinuous"):
            load_and_validate_receipt(json.dumps(resealed))

    def test_wrong_assertion_subject_fails_replay(self) -> None:
        envelope = seal_receipt(simulate_valid_cycle("SUBJECT-REPLAY", "delivery"))
        payload = copy.deepcopy(envelope["payload"])
        payload["assertions"][0]["subject"] = "OTHER"
        with self.assertRaisesRegex(ValueError, "wrong subject"):
            load_and_validate_receipt(json.dumps(seal_payload(payload)))

    def test_missing_assertion_provenance_fails_replay(self) -> None:
        envelope = seal_receipt(simulate_valid_cycle("PROVENANCE-1", "delivery"))
        payload = copy.deepcopy(envelope["payload"])
        payload["assertions"][0]["evidenceRefs"] = []
        with self.assertRaisesRegex(ValueError, "provenance"):
            load_and_validate_receipt(json.dumps(seal_payload(payload)))


if __name__ == "__main__":
    unittest.main()

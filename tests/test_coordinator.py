import unittest

from iepe_core.coordinator import AssertionType, Coordinator, CoordinatorState, GateAssertion, make_assertion, simulate_valid_cycle


class CoordinatorTests(unittest.TestCase):
    def test_delivery_cycle_completes(self) -> None:
        receipt = simulate_valid_cycle("DELIVERY-1", "delivery")
        self.assertEqual(receipt.final_state, CoordinatorState.COMPLETE)
        self.assertEqual(len(receipt.transitions), 12)
        self.assertIn("artifact.DELIVERY-1", receipt.artifacts)

    def test_experiment_cycle_completes(self) -> None:
        receipt = simulate_valid_cycle("EXPERIMENT-1", "experiment")
        self.assertEqual(receipt.work_type, "experiment")
        self.assertIn("assertion.EXPERIMENT-1.evaluation.complete", receipt.assertion_ids)

    def test_invalid_transition_fails(self) -> None:
        coordinator = Coordinator("INVALID-1", "delivery")
        with self.assertRaisesRegex(ValueError, "Invalid coordinator transition"):
            coordinator.transition(CoordinatorState.CLAIM, assertions=[make_assertion(AssertionType.ISSUE_READY, "INVALID-1")])

    def test_missing_gate_evidence_fails(self) -> None:
        coordinator = Coordinator("INVALID-2", "delivery")
        with self.assertRaisesRegex(ValueError, "preflight.valid"):
            coordinator.transition(CoordinatorState.RECONCILE)

    def test_wrong_assertion_type_fails(self) -> None:
        coordinator = Coordinator("INVALID-TYPE", "delivery")
        with self.assertRaisesRegex(ValueError, "preflight.valid"):
            coordinator.transition(
                CoordinatorState.RECONCILE,
                assertions=[make_assertion(AssertionType.ISSUE_READY, "INVALID-TYPE")],
            )

    def test_wrong_assertion_subject_fails(self) -> None:
        coordinator = Coordinator("SUBJECT-1", "delivery")
        assertion = make_assertion(AssertionType.PREFLIGHT_VALID, "OTHER-ISSUE")
        with self.assertRaisesRegex(ValueError, "wrong subject"):
            coordinator.transition(CoordinatorState.RECONCILE, assertions=[assertion])

    def test_invalidated_assertion_fails(self) -> None:
        coordinator = Coordinator("INVALIDATED-1", "delivery")
        assertion = make_assertion(AssertionType.PREFLIGHT_VALID, "INVALIDATED-1", valid=False)
        with self.assertRaisesRegex(ValueError, "is invalid"):
            coordinator.transition(CoordinatorState.RECONCILE, assertions=[assertion])

    def test_stop_record_preserves_reason_and_authority(self) -> None:
        coordinator = Coordinator("STOP-1", "delivery")
        coordinator.stop(
            "owning workspace is ambiguous",
            "project owner",
            evidence=["workspace.conflict"],
        )
        receipt = coordinator.receipt()
        self.assertEqual(receipt.final_state, CoordinatorState.STOPPED)
        self.assertEqual(receipt.stop.state, CoordinatorState.PREFLIGHT)
        self.assertEqual(receipt.stop.resume_authority, "project owner")

    def test_artifact_before_validation_fails(self) -> None:
        coordinator = Coordinator("INVALID-3", "delivery")
        with self.assertRaisesRegex(ValueError, "before issue validation"):
            coordinator.add_artifact("artifact.invalid")

    def test_nonterminal_receipt_fails(self) -> None:
        coordinator = Coordinator("INVALID-4", "delivery")
        with self.assertRaisesRegex(ValueError, "terminal"):
            coordinator.receipt()

    def test_waiting_external_state(self) -> None:
        from iepe_core.coordinator import BlockerFingerprint, ConditionType
        coordinator = Coordinator("WAIT-1", "delivery")
        blocker = BlockerFingerprint(
            code="ENV_WORKSPACE_READ_ONLY",
            scope="SES",
            required_change="workspace-write capability",
            retryable_by_agent=False,
            condition_type=ConditionType.CAPABILITY_MISSING,
        )
        coordinator.park_waiting_external(blocker, resume_authority="user")
        receipt = coordinator.receipt()
        self.assertEqual(receipt.final_state, CoordinatorState.WAITING_EXTERNAL)
        self.assertIn("ENV_WORKSPACE_READ_ONLY", receipt.stop.reason)
        self.assertEqual(receipt.stop.resume_authority, "user")

    def test_duplicate_non_retryable_blocker_fails(self) -> None:
        from iepe_core.coordinator import BlockerFingerprint, ConditionType
        coordinator = Coordinator("WAIT-2", "delivery")
        blocker = BlockerFingerprint(
            code="ENV_WORKSPACE_READ_ONLY",
            scope="SES",
            required_change="workspace-write capability",
            retryable_by_agent=False,
            condition_type=ConditionType.CAPABILITY_MISSING,
        )
        coordinator.park_waiting_external(blocker, resume_authority="user")
        with self.assertRaisesRegex(ValueError, "Duplicate non-retryable blocker fingerprint"):
            coordinator.park_waiting_external(blocker, resume_authority="user")


if __name__ == "__main__":
    unittest.main()

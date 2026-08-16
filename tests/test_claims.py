from datetime import datetime, timedelta, timezone
import unittest

from iepe_core.claims import Claim, ClaimMode, ClaimRegistry, scopes_overlap


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def claim(identifier, issue, workspace, scope, mode=ClaimMode.WRITE, minutes=30):
    return Claim(identifier, issue, "agent.test", workspace, (scope,), mode, NOW, NOW + timedelta(minutes=minutes))


class ClaimRegistryTests(unittest.TestCase):
    def test_hierarchical_scope_overlap_is_provider_neutral(self):
        self.assertTrue(scopes_overlap("project/component", "project/component/file"))
        self.assertFalse(scopes_overlap("project/component-a", "project/component-b"))

    def test_capacity_is_enforced(self):
        registry = ClaimRegistry(capacity=1)
        registry.acquire(claim("c1", "i1", "w", "a"), now=NOW)
        with self.assertRaisesRegex(ValueError, "capacity"):
            registry.acquire(claim("c2", "i2", "w", "b"), now=NOW)

    def test_overlapping_write_is_rejected(self):
        registry = ClaimRegistry(capacity=2)
        registry.acquire(claim("c1", "i1", "w", "area"), now=NOW)
        with self.assertRaisesRegex(ValueError, "conflicts"):
            registry.acquire(claim("c2", "i2", "w", "area/file"), now=NOW)

    def test_read_only_overlap_can_coexist(self):
        registry = ClaimRegistry(capacity=2)
        registry.acquire(claim("c1", "i1", "w", "area", ClaimMode.READ), now=NOW)
        registry.acquire(claim("c2", "i2", "w", "area/file", ClaimMode.READ), now=NOW)
        self.assertEqual(2, len(registry.active(now=NOW)))

    def test_workspaces_are_isolated(self):
        registry = ClaimRegistry(capacity=2)
        registry.acquire(claim("c1", "i1", "w1", "area"), now=NOW)
        registry.acquire(claim("c2", "i2", "w2", "area"), now=NOW)
        self.assertEqual(2, len(registry.active(now=NOW)))

    def test_expired_claim_does_not_authorize_or_consume_capacity(self):
        registry = ClaimRegistry(capacity=1)
        registry.acquire(claim("c1", "i1", "w", "area", minutes=1), now=NOW)
        later = NOW + timedelta(minutes=2)
        self.assertFalse(registry.claim_assertion("c1", issue_id="i1", now=later).valid)
        fresh = Claim("c2", "i2", "agent.test", "w", ("area",), ClaimMode.WRITE, later, later + timedelta(minutes=10))
        registry.acquire(fresh, now=later)

    def test_release_is_idempotent_and_both_attempts_are_recorded(self):
        registry = ClaimRegistry(capacity=1)
        registry.acquire(claim("c1", "i1", "w", "area"), now=NOW)
        self.assertTrue(registry.release("c1", now=NOW, reason="complete"))
        self.assertFalse(registry.release("c1", now=NOW, reason="retry"))
        self.assertEqual(["acquired", "released", "release-repeated"], [event.action for event in registry.history])

    def test_assertion_is_derived_from_matching_active_claim(self):
        registry = ClaimRegistry(capacity=1)
        registry.acquire(claim("c1", "i1", "w", "area"), now=NOW)
        assertion = registry.claim_assertion("c1", issue_id="i1", now=NOW)
        self.assertTrue(assertion.valid)
        self.assertEqual(("claim.c1",), assertion.evidence_refs)
        self.assertFalse(registry.claim_assertion("c1", issue_id="other", now=NOW).valid)


if __name__ == "__main__":
    unittest.main()

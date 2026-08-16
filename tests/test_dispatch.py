from datetime import datetime, timedelta, timezone
import unittest

from iepe_core.claims import Claim, ClaimMode, ClaimRegistry
from iepe_core.context import ContextRequest, ContextSource, assemble_context_packet
from iepe_core.dispatch import DispatchEnvelope, DispatchRegistry, WorkerOutcome, WorkerResult


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def setup():
    claims = ClaimRegistry(1)
    claims.acquire(Claim("claim-1", "ISSUE-1", "agent", "workspace", ("project",), ClaimMode.WRITE, NOW, NOW + timedelta(hours=1)), now=NOW)
    request = ContextRequest("ISSUE-1", "claim-1", "Do work", ("intent",), ("authority",), evidence_required=("tests",), permissions=(("externalWrites", False), ("localWrites", True)), stop_conditions=("authority conflict",))
    sources = {"intent": ContextSource("intent", "intent", 1, "Intent"), "authority": ContextSource("authority", "authority", 2, "Authority")}
    packet = assemble_context_packet(request, registry=claims, now=NOW, sources=sources, dependency_records={})
    return claims, packet


def envelope(packet, identifier="dispatch-1", worker="worker-1", attempt=1, permissions=(("localWrites", True),)):
    return DispatchEnvelope(identifier, "ISSUE-1", "claim-1", packet.digest, worker, "resolver", attempt, permissions)


def result(packet, dispatch="dispatch-1", worker="worker-1", attempt=1, outcome=WorkerOutcome.COMPLETED):
    return WorkerResult(dispatch, "ISSUE-1", "claim-1", packet.digest, worker, attempt, outcome, artifacts=("artifact.1",), commands=("test",), limitations=("local only",))


class DispatchTests(unittest.TestCase):
    def test_success_record_retains_provenance(self):
        claims, packet = setup(); registry = DispatchRegistry()
        registry.dispatch(envelope(packet), packet=packet, claims=claims, now=NOW)
        record = registry.accept_result(result(packet))
        self.assertEqual("completed", record["status"])
        self.assertEqual(["artifact.1"], record["result"]["artifacts"])

    def test_failure_blocked_and_stopped_are_distinct(self):
        for outcome in (WorkerOutcome.FAILED, WorkerOutcome.BLOCKED, WorkerOutcome.STOPPED):
            with self.subTest(outcome=outcome):
                claims, packet = setup(); registry = DispatchRegistry()
                registry.dispatch(envelope(packet), packet=packet, claims=claims, now=NOW)
                self.assertEqual(outcome.value, registry.accept_result(result(packet, outcome=outcome))["status"])

    def test_permission_expansion_is_rejected(self):
        claims, packet = setup(); registry = DispatchRegistry()
        with self.assertRaisesRegex(ValueError, "permission expansion"):
            registry.dispatch(envelope(packet, permissions=(("externalWrites", True),)), packet=packet, claims=claims, now=NOW)

    def test_stale_context_is_rejected(self):
        claims, packet = setup(); registry = DispatchRegistry()
        changed = DispatchEnvelope("dispatch-1", "ISSUE-1", "claim-1", "0" * 64, "worker-1", "resolver", 1, ())
        with self.assertRaisesRegex(ValueError, "stale"):
            registry.dispatch(changed, packet=packet, claims=claims, now=NOW)

    def test_retry_preserves_attempt_lineage_and_may_change_worker(self):
        claims, packet = setup(); registry = DispatchRegistry()
        registry.dispatch(envelope(packet), packet=packet, claims=claims, now=NOW)
        registry.accept_result(result(packet, outcome=WorkerOutcome.FAILED))
        retry = envelope(packet, identifier="dispatch-2", worker="worker-2", attempt=2)
        registry.dispatch(retry, packet=packet, claims=claims, now=NOW)
        self.assertEqual(2, registry.record("dispatch-2")["attempt"])
        self.assertEqual("worker-2", registry.record("dispatch-2")["workerId"])

    def test_duplicate_dispatch_and_result_are_rejected(self):
        claims, packet = setup(); registry = DispatchRegistry(); item = envelope(packet)
        registry.dispatch(item, packet=packet, claims=claims, now=NOW)
        with self.assertRaisesRegex(ValueError, "Duplicate dispatch"):
            registry.dispatch(item, packet=packet, claims=claims, now=NOW)
        registry.accept_result(result(packet))
        with self.assertRaisesRegex(ValueError, "Duplicate worker result"):
            registry.accept_result(result(packet))


if __name__ == "__main__":
    unittest.main()

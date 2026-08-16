from datetime import datetime, timedelta, timezone
import unittest

from iepe_core.claims import Claim, ClaimMode, ClaimRegistry
from iepe_core.context import ContextRequest, ContextSource, assemble_context_packet


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def registry():
    value = ClaimRegistry(1)
    value.acquire(Claim("claim-1", "ISSUE-1", "agent", "workspace", ("project",), ClaimMode.WRITE, NOW, NOW + timedelta(hours=1)), now=NOW)
    return value


def request(**changes):
    values = dict(
        issue_id="ISSUE-1",
        claim_id="claim-1",
        objective="Produce the bounded outcome.",
        intent_refs=("intent",),
        authority_refs=("authority",),
        dependencies=("DEP-1",),
        constraints=("remain reversible",),
        evidence_required=("independent review",),
        permissions=(("externalWrites", False),),
        stop_conditions=("authority becomes ambiguous",),
    )
    values.update(changes)
    return ContextRequest(**values)


def sources():
    return {
        "intent": ContextSource("intent", "intent", 1, "Serve the declared participant.", "purpose"),
        "authority": ContextSource("authority", "authority", 2, "Owner approves promotion."),
        "unrelated": ContextSource("unrelated", "operations", 9, "Do not include me."),
    }


class ContextPacketTests(unittest.TestCase):
    def test_complete_packet_is_deterministic_and_claim_bound(self):
        first = assemble_context_packet(request(), registry=registry(), now=NOW, sources=sources(), dependency_records={"DEP-1": "complete"})
        second = assemble_context_packet(request(), registry=registry(), now=NOW, sources=sources(), dependency_records={"DEP-1": "complete"})
        self.assertEqual(first.record, second.record)
        self.assertEqual("claim-1", first.record["claimId"])

    def test_missing_mandatory_context_blocks_packet(self):
        with self.assertRaisesRegex(ValueError, "Missing mandatory context"):
            assemble_context_packet(request(), registry=registry(), now=NOW, sources={"intent": sources()["intent"]}, dependency_records={"DEP-1": "complete"})

    def test_authority_conflict_is_surfaced(self):
        conflicting = sources()
        conflicting["other-intent"] = ContextSource("other-intent", "intent", 1, "A different purpose.", "purpose")
        with self.assertRaisesRegex(ValueError, "Authority conflict"):
            assemble_context_packet(request(intent_refs=("intent", "other-intent")), registry=registry(), now=NOW, sources=conflicting, dependency_records={"DEP-1": "complete"})

    def test_unreferenced_excess_context_is_excluded(self):
        packet = assemble_context_packet(request(), registry=registry(), now=NOW, sources=sources(), dependency_records={"DEP-1": "complete"})
        self.assertNotIn("unrelated", [source["ref"] for source in packet.record["sources"]])

    def test_referenced_excess_context_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "limit exceeded"):
            assemble_context_packet(request(), registry=registry(), now=NOW, sources=sources(), dependency_records={"DEP-1": "complete"}, max_sources=1)

    def test_expired_claim_blocks_packet(self):
        with self.assertRaisesRegex(ValueError, "active claim"):
            assemble_context_packet(request(), registry=registry(), now=NOW + timedelta(hours=2), sources=sources(), dependency_records={"DEP-1": "complete"})


if __name__ == "__main__":
    unittest.main()

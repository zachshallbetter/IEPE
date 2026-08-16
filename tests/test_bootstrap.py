import json
from pathlib import Path
import tempfile
import unittest

from iepe_core.bootstrap import BootstrapConfig, discover_existing, generated_files, initialize_new
from tools.compile_package import compile_package


class BootstrapTests(unittest.TestCase):
    def config(self) -> BootstrapConfig:
        return BootstrapConfig(
            project_id="project.alpha",
            project_name="Project Alpha",
            intent="Help readers understand a difficult system through a verified interactive explanation.",
            protocol_source="https://example.test/iepe-core",
            protocol_revision="v0.1.0-test",
            evaluators=("content.correctness", "experience.observation"),
            promotion_authorities=("owner.alpha",),
        )

    def test_new_project_is_deterministic_and_reference_pinned(self):
        one = generated_files(self.config())
        two = generated_files(self.config())
        self.assertEqual(one, two)
        reference = json.loads(one[".iepe/protocol-reference.json"])
        profile = json.loads(one["PROJECT_PROFILE.json"])
        self.assertEqual(reference["revision"], "v0.1.0-test")
        self.assertEqual(profile["protocol"]["source"], reference["source"])
        self.assertIn("first agent cycle is read-only reconciliation", one["AGENTS.md"])

    def test_initializer_refuses_existing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "AGENTS.md").write_text("user content", encoding="utf-8")
            with self.assertRaisesRegex(FileExistsError, "AGENTS.md"):
                initialize_new(root, self.config())
            self.assertEqual((root / "AGENTS.md").read_text(encoding="utf-8"), "user content")

    def test_existing_discovery_is_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "notes.md"
            source.write_text("observed behavior", encoding="utf-8")
            before = source.read_bytes()
            report = discover_existing(root)
            self.assertEqual(source.read_bytes(), before)
            self.assertEqual([item["path"] for item in report["files"]], ["notes.md"])
            self.assertFalse(report["signals"]["hasProtocolReference"])

    def test_generated_project_compiles_with_protocol_provenance(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as output:
            root = Path(directory)
            initialize_new(root, self.config())
            manifest = compile_package(root / ".agents/package-source.json", Path(output))
            self.assertEqual(manifest["protocol"]["protocolId"], "IEPE-001")
            self.assertEqual(manifest["protocol"]["revision"], "v0.1.0-test")


if __name__ == "__main__":
    unittest.main()

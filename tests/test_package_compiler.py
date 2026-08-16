import json
from pathlib import Path
import tempfile
import unittest

from tools.compile_package import compile_package


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "agent-package" / "package-source.json"


class PackageCompilerTests(unittest.TestCase):
    def test_example_compiles_deterministically(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            one = compile_package(EXAMPLE, Path(first))
            two = compile_package(EXAMPLE, Path(second))
            self.assertEqual(one, two)
            self.assertEqual(
                (Path(first) / "agent-package-manifest.json").read_bytes(),
                (Path(second) / "agent-package-manifest.json").read_bytes(),
            )
            self.assertEqual(
                (Path(first) / "context-full.md").read_bytes(),
                (Path(second) / "context-full.md").read_bytes(),
            )

    def test_missing_source_is_rejected(self):
        config = json.loads(EXAMPLE.read_text())
        config["projectRoot"] = str((EXAMPLE.parent / "project").resolve())
        config["sources"][0]["path"] = "MISSING.md"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(json.dumps(config))
            with self.assertRaisesRegex(ValueError, "Missing source"):
                compile_package(path, Path(directory) / "out")

    def test_unsafe_and_machine_paths_are_rejected(self):
        config = json.loads(EXAMPLE.read_text())
        config["projectRoot"] = str((EXAMPLE.parent / "project").resolve())
        for bad in ("../secret.txt", "__pycache__/record.pyc"):
            with self.subTest(path=bad), tempfile.TemporaryDirectory() as directory:
                changed = dict(config)
                changed["sources"] = [dict(config["sources"][0], path=bad), *config["sources"][1:]]
                changed["operatingContract"] = bad
                path = Path(directory) / "config.json"
                path.write_text(json.dumps(changed))
                with self.assertRaisesRegex(ValueError, "Unsafe|Excluded"):
                    compile_package(path, Path(directory) / "out")

    def test_dirty_release_is_rejected(self):
        config = json.loads(EXAMPLE.read_text())
        config["projectRoot"] = str((EXAMPLE.parent / "project").resolve())
        config["sourceState"] = "dirty"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(json.dumps(config))
            with self.assertRaisesRegex(ValueError, "clean source state"):
                compile_package(path, Path(directory) / "out")


if __name__ == "__main__":
    unittest.main()

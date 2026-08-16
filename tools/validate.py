#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
TEMPLATE_DIR = ROOT / ".github" / "ISSUE_TEMPLATE"
SKILL_DIR = ROOT / ".agents" / "skills"
EVIDENCE_DIR = ROOT / "evidence"
FIXTURE_PATH = ROOT / "fixtures" / "conformance.json"
TEXT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".py", ".txt"}
PLACEHOLDER_PATTERNS = (rf"\b{'TO' + 'DO'}\b", rf"\b{'T' + 'BD'}\b")


def fail(message: str) -> None:
    raise AssertionError(message)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schemas() -> dict[str, dict]:
    schemas: dict[str, dict] = {}
    for path in sorted(SCHEMA_DIR.glob("*.json")):
        schema = load_json(path)
        Draft202012Validator.check_schema(schema)
        schemas[path.name] = schema

    ids = [schema["$id"] for schema in schemas.values()]
    if len(ids) != len(set(ids)):
        fail("Schema $id values must be unique")

    fixtures = load_json(FIXTURE_PATH)
    if set(fixtures) != set(schemas):
        fail("Every schema must have exactly one named conformance fixture")

    for name, schema in schemas.items():
        validator = Draft202012Validator(schema)
        validator.validate(fixtures[name])
        if not list(validator.iter_errors({})):
            fail(f"{name} accepted the empty negative fixture")

    return schemas


def validate_evidence(schemas: dict[str, dict]) -> int:
    validator = Draft202012Validator(schemas["evidence-bundle.schema.json"])
    paths = sorted(EVIDENCE_DIR.glob("*.json"))
    for path in paths:
        validator.validate(load_json(path))
    return len(paths)


def validate_examples() -> int:
    record_count = 0
    for manifest_path in sorted((ROOT / "examples").glob("*/conformance-manifest.json")):
        manifest = load_json(manifest_path)
        for schema_ref, record_refs in manifest.items():
            schema_path = (manifest_path.parent / schema_ref).resolve()
            schema = load_json(schema_path)
            if isinstance(record_refs, str):
                record_refs = [record_refs]
            for record_ref in record_refs:
                record_path = (manifest_path.parent / record_ref).resolve()
                if ROOT.resolve() not in schema_path.parents or ROOT.resolve() not in record_path.parents:
                    fail(f"{manifest_path} contains a path outside the project root")
                record = load_json(record_path)
                Draft202012Validator(schema).validate(record)
                record_count += 1
    return record_count


def validate_templates() -> int:
    paths = sorted(TEMPLATE_DIR.glob("*.yml"))
    for path in paths:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not document.get("name") or not document.get("description") or not document.get("body"):
            fail(f"{path.name} is missing required template structure")
        ids = [item.get("id") for item in document["body"] if item.get("id")]
        if len(ids) != len(set(ids)):
            fail(f"{path.name} contains duplicate body IDs")
    return len(paths)


def validate_skills() -> int:
    paths = sorted(SKILL_DIR.glob("*/SKILL.md"))
    if not paths:
        fail("No IEPE process skills found")
    for path in paths:
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not match:
            fail(f"{path} has invalid skill frontmatter")
        metadata = yaml.safe_load(match.group(1))
        if set(metadata) != {"name", "description"}:
            fail(f"{path} skill metadata must contain only name and description")
        if metadata["name"] != path.parent.name or not re.fullmatch(r"[a-z0-9-]+", metadata["name"]):
            fail(f"{path} has invalid or mismatched skill name")
        if not metadata["description"].strip():
            fail(f"{path} has an empty skill description")
    return len(paths)


def validate_domain_neutrality() -> None:
    project_terms = [term.strip() for term in os.getenv("IEPE_FORBIDDEN_TERMS", "").split(",") if term.strip()]
    forbidden_patterns = PLACEHOLDER_PATTERNS + tuple(re.escape(term) for term in project_terms)
    violations: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden_patterns:
            if re.search(pattern, text):
                violations.append(f"{path.relative_to(ROOT)}: {pattern}")
    if violations:
        fail("Domain-neutrality audit failed:\n" + "\n".join(violations))


def validate_reference_tests() -> str:
    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        fail("Reference tests failed:\n" + completed.stdout + completed.stderr)
    return completed.stdout + completed.stderr


def main() -> int:
    try:
        schemas = validate_schemas()
        evidence_count = validate_evidence(schemas)
        example_record_count = validate_examples()
        template_count = validate_templates()
        skill_count = validate_skills()
        validate_domain_neutrality()
        reference_test_output = validate_reference_tests()
    except Exception as error:
        print(f"IEPE conformance failed: {error}", file=sys.stderr)
        return 1

    print(f"IEPE conformance passed: {len(schemas)} schemas")
    print(f"IEPE conformance passed: {template_count} issue templates")
    print(f"IEPE conformance passed: {skill_count} process skills")
    print(f"IEPE conformance passed: {evidence_count} evidence bundles")
    print(f"IEPE conformance passed: {example_record_count} example records")
    print("IEPE conformance passed: domain-neutrality audit")
    print(f"IEPE conformance passed: reference tests ({reference_test_output.count(' ... ok')} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Compile canonical project sources into a deterministic Agent Project Package."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


OUTPUTS = ("AGENTS.md", "context-index.md", "context-full.md")
FORBIDDEN_PARTS = {"__MACOSX", "__pycache__", ".git"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_source(root: Path, relative: str) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"Unsafe source path: {relative}")
    if any(part in FORBIDDEN_PARTS for part in candidate.parts) or candidate.suffix in FORBIDDEN_SUFFIXES:
        raise ValueError(f"Excluded source path: {relative}")
    resolved = (root / candidate).resolve()
    if root.resolve() not in resolved.parents and resolved != root.resolve():
        raise ValueError(f"Source escapes project root: {relative}")
    if not resolved.is_file():
        raise ValueError(f"Missing source: {relative}")
    return resolved


def compile_package(config_path: Path, output_dir: Path) -> dict:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    root = (config_path.parent / config.get("projectRoot", ".")).resolve()
    if config["releaseClass"] == "release" and config["sourceState"] != "clean":
        raise ValueError("Release packages require clean source state")

    declared = config["sources"]
    paths = [item["path"] for item in declared]
    if len(paths) != len(set(paths)):
        raise ValueError("Duplicate source path")
    if config["operatingContract"] not in paths:
        raise ValueError("Operating contract must be a declared source")

    source_records = []
    bodies = []
    for item in sorted(declared, key=lambda value: (value["authorityRank"], value["path"])):
        path = safe_source(root, item["path"])
        data = path.read_bytes()
        source_records.append({
            "path": item["path"],
            "role": item["role"],
            "authorityRank": item["authorityRank"],
            "bytes": len(data),
            "sha256": digest(data),
        })
        text = data.decode("utf-8")
        bodies.append(f"--- SOURCE: {item['path']} | ROLE: {item['role']} | AUTHORITY: {item['authorityRank']} ---\n{text.rstrip()}\n")

    operating_data = safe_source(root, config["operatingContract"]).read_bytes()
    index_lines = [
        f"# {config['packageId']} Context Index",
        "",
        f"> Package version: {config['packageVersion']}",
        f"> Source state: {config['sourceState']}",
        "",
    ]
    for record in source_records:
        index_lines.append(
            f"- `{record['path']}` | {record['role']} | authority {record['authorityRank']} | "
            f"{record['bytes']} bytes | `{record['sha256']}`"
        )
    index_data = ("\n".join(index_lines) + "\n").encode()
    full_data = (f"# {config['packageId']} Compiled Context\n\n" + "\n".join(bodies)).encode()

    output_dir.mkdir(parents=True, exist_ok=True)
    generated = {"AGENTS.md": operating_data, "context-index.md": index_data, "context-full.md": full_data}
    for name, data in generated.items():
        (output_dir / name).write_bytes(data)

    output_records = [
        {"path": name, "bytes": len(generated[name]), "sha256": digest(generated[name])}
        for name in OUTPUTS
    ]
    payload = b"".join(name.encode() + b"\0" + generated[name] for name in OUTPUTS)
    manifest = {
        "$schema": config.get("manifestSchema", "https://iepe.dev/schema/agent-package-manifest.schema.json"),
        "formatVersion": "1",
        "packageId": config["packageId"],
        "packageVersion": config["packageVersion"],
        "protocol": config["protocol"],
        "releaseClass": config["releaseClass"],
        "sourceState": config["sourceState"],
        "operatingContract": config["operatingContract"],
        "sources": source_records,
        "skills": sorted(config.get("skills", [])),
        "adapters": sorted(config.get("adapters", [])),
        "outputs": output_records,
        "exclusions": sorted(config.get("exclusions", [])),
        "payloadSha256": digest(payload),
    }
    (output_dir / "agent-package-manifest.json").write_bytes(canonical_json(manifest))
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    compile_package(args.config.resolve(), args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

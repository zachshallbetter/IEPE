#!/usr/bin/env python3
"""Initialize a new IEPE project or inspect an existing project without mutation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from iepe_core.bootstrap import BootstrapConfig, discover_existing, initialize_new


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser()
    commands = root.add_subparsers(dest="mode", required=True)
    new = commands.add_parser("new")
    new.add_argument("--project-root", type=Path, required=True)
    new.add_argument("--project-id", required=True)
    new.add_argument("--project-name", required=True)
    new.add_argument("--intent", required=True)
    new.add_argument("--protocol-source", required=True)
    new.add_argument("--protocol-revision", required=True)
    new.add_argument("--protocol-version", default="0.2.0")
    new.add_argument("--work-graph-provider", default="local")
    new.add_argument("--project-ref", default="work")
    new.add_argument("--coordinator-identity", default="coordinator.local")
    new.add_argument("--coordinator-capacity", type=int, default=1)
    new.add_argument("--evaluator", action="append", default=[])
    new.add_argument("--promotion-authority", action="append", default=[])
    new.add_argument("--overwrite", action="store_true")
    existing = commands.add_parser("existing")
    existing.add_argument("--project-root", type=Path, required=True)
    existing.add_argument("--report", type=Path)
    return root


def main() -> int:
    args = parser().parse_args()
    if args.mode == "existing":
        report = json.dumps(discover_existing(args.project_root), sort_keys=True, indent=2) + "\n"
        if args.report:
            if args.report.exists():
                raise FileExistsError(f"Refusing to overwrite report: {args.report}")
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(report, encoding="utf-8")
        else:
            print(report, end="")
        return 0

    config = BootstrapConfig(
        project_id=args.project_id,
        project_name=args.project_name,
        intent=args.intent,
        protocol_source=args.protocol_source,
        protocol_revision=args.protocol_revision,
        protocol_version=args.protocol_version,
        work_graph_provider=args.work_graph_provider,
        project_ref=args.project_ref,
        coordinator_identity=args.coordinator_identity,
        coordinator_capacity=args.coordinator_capacity,
        evaluators=tuple(args.evaluator or ["manual.acceptance"]),
        promotion_authorities=tuple(args.promotion_authority or ["project.owner"]),
    )
    written = initialize_new(args.project_root, config, overwrite=args.overwrite)
    print(json.dumps({"mode": "new", "projectRoot": str(args.project_root.resolve()), "files": [str(path) for path in written]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

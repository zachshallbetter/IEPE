"""Deterministic, reference-pinned IEPE project initialization."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from typing import Iterable


FORBIDDEN_PARTS = {".git", "__MACOSX", "__pycache__", ".pytest_cache"}
PROJECT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
CORE_ROOT = Path(__file__).resolve().parents[1]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


@dataclass(frozen=True)
class BootstrapConfig:
    project_id: str
    project_name: str
    intent: str
    protocol_source: str
    protocol_revision: str
    protocol_version: str = "0.1.0"
    work_graph_provider: str = "local"
    project_ref: str = "work"
    coordinator_identity: str = "coordinator.local"
    coordinator_capacity: int = 1
    evaluators: tuple[str, ...] = ("manual.acceptance",)
    promotion_authorities: tuple[str, ...] = ("project.owner",)
    protected_actions: tuple[str, ...] = (
        "external-publication",
        "production-deployment",
        "spending",
        "destructive-migration",
        "credential-or-iam-change",
        "authoritative-intent-change",
        "external-communication",
    )

    def validate(self) -> None:
        values = {
            "project ID": self.project_id,
            "project name": self.project_name,
            "intent": self.intent,
            "protocol source": self.protocol_source,
            "protocol revision": self.protocol_revision,
            "protocol version": self.protocol_version,
            "work graph provider": self.work_graph_provider,
            "project reference": self.project_ref,
            "coordinator identity": self.coordinator_identity,
        }
        for label, value in values.items():
            if not value.strip():
                raise ValueError(f"Missing {label}")
        if not PROJECT_ID.fullmatch(self.project_id):
            raise ValueError("Project ID must use letters, numbers, dots, underscores, or hyphens")
        if len(self.protocol_revision) < 7:
            raise ValueError("Protocol revision must be an immutable tag or digest with at least seven characters")
        if self.coordinator_capacity < 1:
            raise ValueError("Coordinator capacity must be positive")
        if not self.evaluators or not self.promotion_authorities:
            raise ValueError("At least one evaluator and promotion authority are required")


def protocol_reference(config: BootstrapConfig) -> dict:
    return {
        "$schema": "https://iepe.dev/schema/protocol-reference.schema.json",
        "protocolId": "IEPE-001",
        "protocolVersion": config.protocol_version,
        "source": config.protocol_source,
        "revision": config.protocol_revision,
        "relationship": "reference",
        "conformanceCommand": "python3 tools/validate.py",
    }


def project_profile(config: BootstrapConfig) -> dict:
    protocol = protocol_reference(config)
    return {
        "$schema": "https://iepe.dev/schema/project-profile.schema.json",
        "id": config.project_id,
        "name": config.project_name,
        "protocol": {key: protocol[key] for key in ("protocolId", "protocolVersion", "source", "revision")},
        "intentRefs": ["INTENT.md"],
        "authorityOrder": ["INTENT.md", "docs/EXPERIENCE.md", "docs/ARCHITECTURE.md", "PROJECT_PROFILE.json", "AGENTS.md"],
        "workGraph": {"provider": config.work_graph_provider, "projectRefs": [config.project_ref]},
        "workspaces": ["."],
        "coordinator": {
            "identity": config.coordinator_identity,
            "capacity": config.coordinator_capacity,
            "stopPolicyRef": "AGENTS.md#stop-conditions",
        },
        "evaluators": list(config.evaluators),
        "protectedActions": list(config.protected_actions),
        "promotionAuthorities": list(config.promotion_authorities),
        "memory": {
            "operational": config.project_ref,
            "institutional": "docs",
            "negativeResults": "docs/NEGATIVE_RESULTS.md",
        },
    }


def _agents(config: BootstrapConfig) -> str:
    return f"""# {config.project_name} Agent Operating Contract

## IEPE authority

This project operates under `IEPE-001`, version `{config.protocol_version}`, from `{config.protocol_source}` at immutable revision `{config.protocol_revision}`. The pin is recorded in `.iepe/protocol-reference.json`.

IEPE Core governs claim, context, dispatch, evidence, perturbation, promotion, memory, and stop semantics. Local canonical sources govern this project's intent, experience, architecture, work graph, evaluators, adapters, and protected actions. Local instructions may specialize IEPE but may not weaken its invariants.

Preserve this trace:

```text
intent -> epic -> issue -> claim -> context -> artifact -> evaluation -> evidence -> qualification -> promotion
```

## Authority order

1. `INTENT.md`
2. `docs/EXPERIENCE.md`
3. `docs/ARCHITECTURE.md`
4. `PROJECT_PROFILE.json`
5. Authorized issues and decisions
6. Implementation and operational observations
7. Generated agent context

Conversation and generated files are evidence inputs, not automatic authority.

## Operational loop

```text
reconcile -> select -> validate -> claim -> assemble bounded context -> dispatch -> observe -> evaluate -> stress test when required -> record evidence -> disposition -> release claim -> repeat
```

## Startup

1. Verify `.iepe/protocol-reference.json` and `PROJECT_PROFILE.json` against the pinned IEPE revision.
2. Inspect repository, documentation, work graph, claims, dependencies, tests, and evidence without mutation.
3. Reconcile contradictions and missing authority.
4. Select only a complete Ready issue.
5. Claim bounded scope, assemble minimal context, dispatch, evaluate, record, and release.

The first agent cycle is read-only reconciliation. Do not infer mutation authority from repository access.

## Status honesty

`Documented != Implemented != Tested != Empirically Validated`

Artifact existence, a passing API call, or completion language does not establish qualification.

## Process routing

Use the narrowest procedure under `.agents/skills/`: initialize, reconcile, operate, qualify, stress test, or maintain the package. These procedures are projections from the pinned IEPE revision and cannot expand local authority.

## Protected actions

Read `PROJECT_PROFILE.json`. Protected actions require its named promotion authority and issue-level authorization.

## Stop conditions

Stop and record a typed result when authority, ownership, context, dependencies, permissions, evidence, evaluator availability, provider health, or recovery becomes ambiguous. Stop when capacity or retry limits are exhausted. Silence is not approval.
"""


def _intent(config: BootstrapConfig) -> str:
    return f"""# {config.project_name} Intent

## Purpose

{config.intent.strip()}

## Beneficiaries

Unconfirmed. Establish before the first promotional decision.

## Protected qualities

Unconfirmed. Record qualities that implementation must preserve.

## Exclusions

Unconfirmed. Record outcomes this project must not pursue.

## Success evidence

Unconfirmed. Define observable evidence before the first issue becomes Ready.
"""


def generated_files(config: BootstrapConfig) -> dict[str, str]:
    config.validate()
    protocol = protocol_reference(config)
    profile = project_profile(config)
    package_source = {
        "$schema": "https://iepe.dev/schema/agent-package-source.schema.json",
        "manifestSchema": "https://iepe.dev/schema/agent-package-manifest.schema.json",
        "packageId": f"{config.project_id}.agent-package",
        "packageVersion": "0.1.0",
        "projectRoot": "..",
        "protocol": {key: protocol[key] for key in ("protocolId", "protocolVersion", "source", "revision")},
        "releaseClass": "provisional",
        "sourceState": "provisional",
        "operatingContract": "AGENTS.md",
        "sources": [
            {"path": ".iepe/protocol-reference.json", "role": "doctrine", "authorityRank": 1},
            {"path": "INTENT.md", "role": "intent", "authorityRank": 2},
            {"path": "docs/EXPERIENCE.md", "role": "doctrine", "authorityRank": 3},
            {"path": "docs/ARCHITECTURE.md", "role": "doctrine", "authorityRank": 4},
            {"path": "PROJECT_PROFILE.json", "role": "operations", "authorityRank": 5},
            {"path": "AGENTS.md", "role": "operations", "authorityRank": 6},
            {"path": "ROADMAP.md", "role": "operations", "authorityRank": 7},
        ],
        "skills": [
            f"iepe-core:initialize-iepe-project@{config.protocol_revision}",
            f"iepe-core:maintain-iepe-package@{config.protocol_revision}",
            f"iepe-core:operate-iepe-project@{config.protocol_revision}",
            f"iepe-core:qualify-iepe-outcome@{config.protocol_revision}",
            f"iepe-core:reconcile-iepe-project@{config.protocol_revision}",
            f"iepe-core:stress-test-iepe-candidate@{config.protocol_revision}",
        ],
        "adapters": [],
        "exclusions": [".git", "__MACOSX", "__pycache__", "*.pyc", "undeclared files"],
    }
    files = {
        ".agents/NEW_AGENT_PROMPT.md": f"""# First Agent Cycle

Operate {config.project_name} under the pinned IEPE reference in `.iepe/protocol-reference.json` and the local contract in `AGENTS.md`.

Begin with read-only reconciliation. Verify the protocol pin, local profile, authority chain, repository state, work graph, dependencies, evaluators, protected actions, and evidence gaps. Do not implement, claim, create or change work items, push, merge, deploy, publish, spend, or communicate externally during this first cycle unless the user explicitly expands authority.

Return a typed reconciliation result, the material unknowns, and the first candidate Ready issue. If initialization gates are incomplete, stop with the exact authority or evidence needed to continue.
""",
        ".agents/package-source.json": canonical_json(package_source),
        ".agents/runtime/COORDINATOR.md": """# Coordinator Runtime

Use the state sequence defined by pinned IEPE Core: preflight, reconcile, select, validate, claim, assemble context, dispatch, observe, evaluate, disposition, record, and close loop.

Concurrency, work-graph identity, evaluators, protected actions, promotion authorities, and memory locations come from `PROJECT_PROFILE.json`. Persist typed receipts. Never let a provider adapter expand local permissions or IEPE invariants.
""",
        ".iepe/protocol-reference.json": canonical_json(protocol),
        "AGENTS.md": _agents(config),
        "INTENT.md": _intent(config),
        "PROJECT_PROFILE.json": canonical_json(profile),
        "ROADMAP.md": f"""# {config.project_name} Roadmap

## M0: Governed baseline

Exit evidence:

- intent, beneficiaries, protected qualities, exclusions, and success evidence are confirmed
- project profile and protocol pin conform
- zero-state or operational baseline is recorded
- one material unknown is registered
- one bounded, reversible issue is Ready

## M1: First qualified outcome

Define after M0. Express the milestone as observable capability and exit evidence rather than a feature inventory.
""",
        "docs/ARCHITECTURE.md": "# Architecture\n\nNo architecture has been authorized. Record established decisions separately from proposals and observations.\n",
        "docs/EXPERIENCE.md": "# Experience Contract\n\nBeneficiaries, critical journeys, states, accessibility requirements, protected qualities, and observation methods remain unconfirmed.\n",
        "docs/NEGATIVE_RESULTS.md": "# Negative and Inconclusive Results\n\nRetain rejected candidates, failed evaluations, contradictions, limitations, and the evidence that produced each disposition.\n",
    }
    for source in sorted((CORE_ROOT / ".agents/skills").glob("*/SKILL.md")):
        files[f".agents/skills/{source.parent.name}/SKILL.md"] = source.read_text(encoding="utf-8")
    return files


def initialize_new(root: Path, config: BootstrapConfig, *, overwrite: bool = False) -> tuple[Path, ...]:
    root = root.resolve()
    files = generated_files(config)
    conflicts = sorted(relative for relative in files if (root / relative).exists())
    if conflicts and not overwrite:
        raise FileExistsError("Refusing to overwrite existing files: " + ", ".join(conflicts))
    written = []
    for relative, content in sorted(files.items()):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(path)
    return tuple(written)


def discover_existing(root: Path) -> dict:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"Project root is not a directory: {root}")
    records = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root)
        if any(part in FORBIDDEN_PARTS for part in relative.parts):
            continue
        data = path.read_bytes()
        records.append({"path": relative.as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    names = {record["path"] for record in records}
    return {
        "mode": "existing-read-only",
        "projectRoot": str(root),
        "files": records,
        "signals": {
            "hasAgentContract": "AGENTS.md" in names,
            "hasIntent": "INTENT.md" in names,
            "hasProjectProfile": "PROJECT_PROFILE.json" in names,
            "hasProtocolReference": ".iepe/protocol-reference.json" in names,
            "hasGitMetadata": (root / ".git").exists(),
        },
        "nextAction": "Review provenance and contradictions before authorizing an IEPE overlay.",
    }

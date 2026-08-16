# IEPE Core

IEPE Core is the project-agnostic reference implementation of the Intent and Evidence Project Engine.

It provides a reusable operating layer for documentation-first, ticket-first, agent-executed projects. It connects project intent, experience and design authority, work graphs, operational coordination, worker agents, empirical search, independent evaluation, evidence, promotion control, and durable project memory.

## Governing chain

```text
Intent
  -> Doctrine and experience contracts
  -> Portfolio, milestones, and epics
  -> Authorized issues and experiments
  -> Coordinated agent execution
  -> Artifacts and observations
  -> Independent evaluation
  -> Evidence-qualified promotion
  -> Project memory and revised understanding
```

## Current maturity

| Capability | Maturity |
| --- | --- |
| Core doctrine | Documented |
| Coordinator contract | Documented |
| Contract schema suite | Tested with positive and negative fixtures |
| GitHub issue templates | Tested for structural validity |
| Conformance runner | Tested locally, including deliberate failure probe |
| Cross-domain example | Tested synthetically; no human or field validation |
| Incremental migration | Tested with a synthetic legacy backlog |
| Coordinator state machine | Tested locally with typed, subject-bound gate assertions |
| Receipt persistence and replay | Tested locally for round-trip, tamper, and impossible-history rejection |
| Epistemic stress testing | Tested synthetically with two blind counterfactual trials |
| Claim capacity and conflict management | Tested locally with typed in-memory claims |
| New and existing project initialization | Tested locally with reference pinning, deterministic scaffolding, overwrite refusal, and read-only discovery |
| Agent Project Package | Tested locally with deterministic source and payload hashing |
| Bounded context-packet assembly | Tested locally with claim, authority, dependency, and size gates |
| Worker dispatch interface | Tested locally with permission, provenance, outcome, and retry gates |
| Reference coordinator | Not implemented |
| Cross-domain adapters | Not implemented |
| Empirical validation | Not validated |

## Project structure

```text
IEPE-Core/
├── AGENTS.md
├── .agents/skills/
├── README.md
├── ROADMAP.md
├── evidence/
├── examples/
├── fixtures/
├── docs/
│   ├── ADOPTION.md
│   ├── AGENT_PROJECT_PACKAGE.md
│   ├── COORDINATOR.md
│   ├── EPISTEMIC_STRESS_TESTING.md
│   ├── INITIALIZATION.md
│   ├── UPSTREAM_REFERENCE.md
│   └── PROTOCOL.md
├── schemas/
│   ├── evaluation-record.schema.json
│   ├── agent-package-manifest.schema.json
│   ├── agent-package-source.schema.json
│   ├── context-packet.schema.json
│   ├── evidence-bundle.schema.json
│   ├── experience-contract.schema.json
│   ├── issue-contract.schema.json
│   ├── project-profile.schema.json
│   ├── protocol-reference.schema.json
│   ├── promotion-record.schema.json
│   ├── perturbation.schema.json
│   ├── robustness-profile.schema.json
│   ├── unknown-variable-ledger.schema.json
│   ├── worker-dispatch.schema.json
│   └── world-card.schema.json
├── tools/
│   ├── init_project.py
│   ├── compile_package.py
│   └── validate.py
├── work/
└── .github/ISSUE_TEMPLATE/
    ├── decision.yml
    ├── delivery.yml
    ├── design.yml
    ├── evaluation.yml
    ├── experiment.yml
    ├── incident.yml
    ├── perturbation.yml
    └── promotion.yml
```

## Starting or adopting a project

Use the [Project Initialization Protocol](docs/INITIALIZATION.md) and [Adoption Guide](docs/ADOPTION.md) for either a new project or an existing project.

IEPE adoption follows a **Two-Stage Trigger Pattern**:
1. **Stage 1 (Reconcile):** Existing projects begin with read-only discovery, intent reconstruction, and work-graph reconciliation.
2. **Stage 2 (Apply):** Once approved, the project-local operating layer is installed under isolated mutation authority.

### Quickstart & CLI Commands

Install the core package locally:

```bash
python3 -m pip install -e .[dev]
```

Inspect an existing project without mutation (Stage 1):

```bash
iepe-init existing --project-root /path/to/project --report /external/path/iepe-report.json
```

Initialize a new project operating layer (Stage 2 / Greenfield):

```bash
iepe-init new \
  --project-root /path/to/new-project \
  --project-id project.example \
  --project-name "Example Project" \
  --intent "The outcome this project exists to cause." \
  --protocol-source "https://github.com/example/iepe-core" \
  --protocol-revision "v0.1.0"

iepe-compile \
  --config /path/to/new-project/.agents/package-source.json \
  --output /path/to/new-project/.agents/generated
```

Replace the example source and revision with the canonical repository and immutable release tag or commit digest. Then hand off to the operational agent using `/path/to/new-project/.agents/NEW_AGENT_PROMPT.md`.

## Conformance and Validation

Run the full schema validation, template check, evidence bundle audit, and domain-neutrality suite:

```bash
iepe-validate
```

Or execute pytest unit tests directly:

```bash
pytest -v
```

Adopters can supply project-specific terms that must not leak into core contracts:

```bash
IEPE_FORBIDDEN_TERMS="Project Name,Product Name" iepe-validate
```

## License

IEPE Core is licensed under the [Apache License, Version 2.0](LICENSE).

## Status honesty

```text
Documented != Implemented != Tested != Empirically Validated
```

This repository currently establishes a documented protocol and starter contracts. It does not yet claim an operational coordinator or empirical validation.

M1 is structurally complete at `Tested` maturity. Its external-pilot exit condition remains unresolved.

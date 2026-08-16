# IEPE Core: Intent and Evidence Project Engine

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Protocol Version](https://img.shields.io/badge/Protocol-IEPE--001%20v0.2.0-green.svg)](docs/PROTOCOL.md)
[![Python Version](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue.svg)](pyproject.toml)

**IEPE** (Intent and Evidence Project Engine) is a open-source, project-agnostic engine for **documentation-first, ticket-first, evidence-qualified AI software engineering**.

It solves the fundamental failure modes of autonomous coding agents: **governance livelocks, infinite retry loops, phantom completions, unverified claims, and lost project context**.

---

## ⚡ Single Agentic Adoption Command

To adopt IEPE on any new or existing project, copy and paste this single command block directly into your AI coding agent (Cursor, Antigravity, Claude, ChatGPT, Windsurf, Devin):

```text
Adopt IEPE for this repository.
Target: ./
Pinned IEPE source: https://github.com/zachshallbetter/IEPE (v0.2.0)
Project Intent: "<Describe the core project intent here>"
Project Mode: existing | new
Mutation Authority: local-files

Execution sequence:
1. Preflight: Run workspace write capability probe once.
2. Reconcile: Perform read-only discovery of intent, files, and authority order.
3. Apply: Generate AGENTS.md, PROJECT_PROFILE.json, and .iepe/protocol-reference.json.
4. Validate: Run iepe-validate or python3 tools/validate.py.
```

---

## 💡 What is IEPE?

Modern AI agents write code fast, but without governance they drift from intent, claim completion on broken builds, overwrite existing invariants, or loop indefinitely on missing environment capabilities.

IEPE provides a deterministic operating layer beneath any agent:

1. **Intent Governs Implementation:** Code exists to fulfill declared human intent, not arbitrary agent guesswork.
2. **Ticket-Bound Authority:** Agents execute bounded work contracts with explicit scope, permissions, and budget.
3. **Preflight Capability Probing:** Environment constraints (e.g. read-only filesystems) are detected *before* discovery to prevent governance livelocks.
4. **Evidence-Qualified Promotion:** Claims require empirical proof (tests, schemas, benchmarks) before work is promoted to `Done`.
5. **Status Honesty:** Strict operational boundary: `Documented != Implemented != Tested != Empirically Validated`.

---

## 🔗 The Governing Chain

Every material change must preserve complete lineage from intent to promotion:

```text
Intent
  -> Doctrine & Experience Contracts
  -> Portfolio Objectives & Epics
  -> Issue Contracts & Experiments
  -> Coordinated Agent Execution
  -> Artifacts & Empirical Observations
  -> Independent Evaluation
  -> Evidence-Qualified Promotion
  -> Retained Institutional Memory
```

---

## 📖 Quick Links & Documentation Index

| Document | Purpose |
| :--- | :--- |
| ⚡ [**Single Agent Reference**](docs/REFERENCE.md) | **One-page cheat-sheet** for human developers and AI agents |
| 📖 [**Protocol Specification**](docs/PROTOCOL.md) | Canonical protocol invariants, condition taxonomy, and stop semantics |
| 🚀 [**Adoption Guide**](docs/ADOPTION.md) | Two-stage adoption pattern (`reconcile` then `apply`) |
| 🛠️ [**Initialization Guide**](docs/INITIALIZATION.md) | Step-by-step onboarding for greenfield and existing projects |
| 🔄 [**Coordinator Specification**](docs/COORDINATOR.md) | Coordinator state machine, preflight sequence, and blocker deduplication |
| 🧪 [**Epistemic Stress Testing**](docs/EPISTEMIC_STRESS_TESTING.md) | Designed perturbation trials and unknown-variable discovery |
| 📜 [**Negative Results Register**](docs/NEGATIVE_RESULTS.md) | Institutional memory of disproven hypotheses and protocol lessons |

---

## 🛠️ Quickstart CLI

### Installation

```bash
pip install -e .[dev]
```

### 1. Stage 1: Reconcile (Existing Project Discovery)

Inspect an existing repository without making any file modifications:

```bash
iepe-init existing --project-root /path/to/project --report /path/to/report.json
```

### 2. Stage 2: Apply (Initialize Operating Layer)

Establish the project-local operating layer:

```bash
iepe-init new \
  --project-root /path/to/project \
  --project-id project.example \
  --project-name "Example Project" \
  --intent "The core outcome this project exists to cause." \
  --protocol-source "https://github.com/zachshallbetter/IEPE" \
  --protocol-revision "v0.2.0"
```

### 3. Conformance Validation

Run the full validation suite (schemas, issue templates, skills, evidence bundles, and domain neutrality):

```bash
iepe-validate
```

Or execute unit tests directly:

```bash
pytest -v
```

---

## 📊 Current Engine Maturity

```text
Documented != Implemented != Tested != Empirically Validated
```

| Capability | Maturity | Evidence / Location |
| :--- | :--- | :--- |
| Core Protocol (`IEPE-001`) | **Tested** | [`docs/PROTOCOL.md`](docs/PROTOCOL.md) |
| Preflight Capability Probing | **Tested** | [`iepe_core/bootstrap.py`](iepe_core/bootstrap.py) |
| Blocker Fingerprinting & Livelock Fix | **Tested** | [`iepe_core/coordinator.py`](iepe_core/coordinator.py) |
| `WAITING_EXTERNAL` Parked State | **Tested** | [`tests/test_coordinator.py`](tests/test_coordinator.py) |
| Provisional Profile Generation | **Tested** | [`tests/test_bootstrap.py`](tests/test_bootstrap.py) |
| Contract Schema Suite (16 Schemas) | **Tested** | [`schemas/`](schemas/) |
| GitHub Issue Templates (8 Templates) | **Tested** | [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/) |
| Conformance Suite (`iepe-validate`) | **Tested** | [`tools/validate.py`](tools/validate.py) |
| Agent Project Package Compiler | **Tested** | [`tools/compile_package.py`](tools/compile_package.py) |

---

## 📄 License

IEPE Core is open-source software licensed under the [Apache License, Version 2.0](LICENSE).

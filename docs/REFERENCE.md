# IEPE Single Agent Reference & Operational Sheet

> Protocol: `IEPE-001`  
> Version: `v0.2.0`  
> Purpose: Universal single-file reference for human developers and autonomous AI agents.

---

## ⚡ The Single Agentic Adoption Command

Copy and paste this single command block into any AI agent chat interface (Cursor, Antigravity, Claude, ChatGPT, Windsurf, Devin) to adopt IEPE on any project:

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

## 🏛️ Authority Hierarchy

Resolve authority conflicts in strict canonical order:

```text
1. docs/PROTOCOL.md (Governing Protocol)
2. Approved Decision Records (docs/DECISIONS.md)
3. JSON Schemas (schemas/*.schema.json)
4. Coordinator & Adoption Specifications (docs/COORDINATOR.md, docs/ADOPTION.md)
5. Issue Contracts & Acceptance Criteria (work/*.md)
6. Implemented Substrate Code & Templates (iepe_core/, tools/)
7. Generated Artifacts & Agent Outputs
```

---

## 🔗 The Governing Chain

Every material project change must preserve complete provenance:

```text
intent -> epic -> issue -> artifact -> evidence -> qualification -> promotion
```

---

## 📊 Status Honesty & Maturity Taxonomy

Never conflate maturity levels. Always state the weaker claim when in doubt:

```text
Backlog -> Ready -> In progress -> In review -> Done -> Verified
Documented != Implemented != Tested != Empirically Validated
Intent -> Explored -> Specified -> Prototyped -> Implemented -> Observed -> Validated
```

---

## 🚥 Condition Classification Taxonomy

The coordinator classifies all unresolved execution conditions into six explicit types:

| Condition | Meaning | Coordinator Response |
| :--- | :--- | :--- |
| `AUTHORIZATION_MISSING` | User has not permitted the action | Ask one precise question |
| `CAPABILITY_MISSING` | Environment cannot perform the action | Stop once; identify required capability |
| `EVIDENCE_MISSING` | Promotion cannot yet be justified | Continue allowed preparation; block promotion |
| `INPUT_MISSING` | Consequential project decision is unresolved | Use provisional value or ask if execution materially depends on it |
| `WORK_UNAVAILABLE` | Nothing actionable is Ready | Park the loop |
| `EXTERNAL_EVENT_PENDING` | Only another actor can change state | Enter `WAITING_EXTERNAL`; do not retry |

---

## 🔄 Coordinator State Machine & Preflight Sequence

### Execution Sequence
```text
resolve project -> inspect instructions -> test required capabilities -> perform discovery -> prepare changes -> mutate
```

### State Machine
```text
PREFLIGHT (Capabilities & Environment Probe)
  -> RECONCILE
  -> SELECT
  -> VALIDATE
  -> CLAIM
  -> ASSEMBLE_CONTEXT
  -> DISPATCH
  -> OBSERVE
  -> EVALUATE
  -> DISPOSITION
  -> RECORD
  -> CLOSE_LOOP
  -> WAITING_EXTERNAL (Parked on Non-Retryable Blocker)
```

---

## 🛡️ Hard-Blocker Fingerprinting & Livelock Prevention

Every blocker receives a stable `code:scope` fingerprint:

```json
{
  "code": "ENV_WORKSPACE_READ_ONLY",
  "scope": "target-project",
  "requiredChange": "workspace-write capability",
  "retryableByAgent": false,
  "fingerprint": "ENV_WORKSPACE_READ_ONLY:target-project"
}
```

**Rule:** If the current blocker fingerprint matches the previous non-retryable blocker, the agent MUST NOT retry, reread the objective, or consume additional attempts. It immediately enters `WAITING_EXTERNAL` and returns control to the user.

---

## 📜 Provisional Profile Protocol

Creating local reversible operating files (`AGENTS.md`, `PROJECT_PROFILE.json`, `.iepe/protocol-reference.json`) requires only local reversible authorization. Unassigned promotion authority yields:

```json
{
  "promotionAuthority": "unassigned",
  "profileStatus": "provisional",
  "promotionBlocked": true
}
```

Initialization proceeds without blocking, while milestone promotion remains blocked until a named authority is assigned.

---

## 🛠️ Essential CLI Reference

```bash
# Install IEPE Core package locally
pip install -e .[dev]

# Inspect existing project without mutation (Stage 1: Reconcile)
iepe-init existing --project-root /path/to/project --report /path/to/report.json

# Initialize project operating layer (Stage 2: Apply)
iepe-init new \
  --project-root /path/to/project \
  --project-id project.name \
  --project-name "Project Name" \
  --intent "Core project intent statement." \
  --protocol-source "https://github.com/zachshallbetter/IEPE" \
  --protocol-revision "v0.2.0"

# Validate full schema, template, evidence, and domain-neutrality suite
iepe-validate

# Execute pytest unit test suite
pytest -v
```

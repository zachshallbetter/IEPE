# IEPE Adoption Guide

## Two-Stage Adoption Pattern

IEPE adoption follows a strict two-stage sequence: **reconcile first, then apply**.

Existing projects always begin in a read-only discovery and reconciliation phase before any file mutations or configuration changes are authorized. New projects may initialize directly once originating intent and protocol authority are supplied. Approved adoption plans are applied in Stage 2 under isolated mutation authority.

### Universal Adoption Inputs

Every IEPE adoption requires these baseline inputs:

```yaml
target_project: ""
project_mode: new | existing
iepe_source: ""
iepe_revision: "" # Immutable tag, commit, or content digest
project_intent: ""
work_graph_provider: local | github | other
mutation_authority: read-only | local-files | repository | external
protected_actions: []
```

The pinned IEPE revision must be an immutable tag, commit, or content digest.

## Adoption Modes

IEPE supports two entry modes. Both produce the same governed operating model, but they begin from different evidence.

| Mode | Starting condition | Stage 1 Responsibility | Stage 2 Responsibility |
| --- | --- | --- | --- |
| New project | Intent exists but implementation and work history may not | Validate intent & protocol pin; establish zero-state baseline | Direct initialization of governing layer and package compilation |
| Existing project | Artifacts, tickets, and behavior already exist | Read-only discovery, intent reconstruction, work-graph reconciliation | Apply approved overlay without replacing existing valid local authority |

The complete procedures, standard triggers, and reference commands are defined in [`INITIALIZATION.md`](INITIALIZATION.md).

## Minimum Adoption Steps

1. **Reconcile (Stage 1):** Perform read-only inventory, reconstruct authority order, and reconcile work graph.
2. **Apply (Stage 2):**
   - Pin versioned IEPE authority in `.iepe/protocol-reference.json`.
   - Add the IEPE block to controlling `AGENTS.md`.
   - Create `PROJECT_PROFILE.json` with workspace, evaluator, and protected-action configuration.
   - Configure `.agents/package-source.json` and `.agents/NEW_AGENT_PROMPT.md`.
   - Install narrow process skills under `.agents/skills/`.
3. **Operational Handoff:** Execute the first agent cycle (read-only reconciliation) before running the pilot issue.

This is the minimum structural installation. A project does not enter autonomous operation until it has established a baseline, selected a bounded pilot, declared evidence requirements, and identified protected actions.

## Required project profile

```yaml
project:
  id: ""
  protocol:
    protocolId: IEPE-001
    protocolVersion: ""
    source: ""
    revision: ""
  intent_refs: []
  authority_order: []
  work_graph:
    provider: github | other
    project_refs: []
  repositories_or_workspaces: []
  coordinator:
    identity: ""
    capacity: 1
  evaluators: []
  protected_actions: []
  promotion_authorities: []
  memory:
    operational: ""
    institutional: ""
```

## `AGENTS.md` adoption block

```markdown
## Intent and Evidence Project Engine

This project operates under `IEPE-001` from the source and immutable revision recorded in `.iepe/protocol-reference.json`.

Intent governs implementation. Canonical documentation defines authority. Issues authorize committed work. The project graph owns live status and native dependencies. The coordinator claims ready work, assembles bounded context, dispatches worker agents, and routes results through evaluation. Agents may explore within their granted environment but may not promote, publish, deploy, spend, communicate externally, or alter authoritative state without explicit authority.

Preserve traceability:

`intent -> epic -> issue -> artifact -> evidence -> qualification -> promotion`

Continue while authority, context, ownership, dependencies, permissions, and evidence remain valid. Stop at unverified boundaries.
```

The upstream relationship and update procedure are defined in [`UPSTREAM_REFERENCE.md`](UPSTREAM_REFERENCE.md).

## Migration rule

Do not convert every historical ticket immediately. Apply IEPE to new committed work and selected active epics. Promote durable historical conclusions into institutional memory only when their provenance can be established.

The complete incremental migration procedure is defined in [`MIGRATION.md`](MIGRATION.md).

Existing-project initialization begins with a read-only inventory. Discovery does not authorize the coordinator to rewrite documentation, close tickets, change project fields, or reinterpret undocumented behavior as governing intent.

## Pilot selection

Choose a pilot that is meaningful, bounded, reversible, measurable, and representative of normal work. Avoid the most politically sensitive, financially consequential, or architecturally ambiguous project as the first validation case.

The pilot must exercise one complete trace:

```text
intent -> authorized issue -> claim -> context -> execution -> evaluation -> evidence -> disposition -> promotion
```

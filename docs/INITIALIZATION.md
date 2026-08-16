# Project Initialization Protocol

## Purpose

This protocol installs IEPE as an operating layer for a new or existing project. It does not prescribe product architecture. The stable engine supplies coordination, claims, evidence, perturbation, promotion, and memory contracts. A project profile supplies domain-specific intent, authority, workspaces, evaluators, and protected actions.

The installation references an immutable IEPE Core revision through `.iepe/protocol-reference.json`. See [`UPSTREAM_REFERENCE.md`](UPSTREAM_REFERENCE.md) for the authority and update boundary.

## Two-Stage Trigger Pattern

IEPE adoption follows a two-stage pattern: **reconcile first, then apply**.

Existing projects always begin in a read-only discovery and reconciliation stage before mutation authority is granted. New projects may initialize directly once originating intent and authority are supplied. Approved adoptions are applied in Stage 2 under explicit mutation authority.

### Universal Inputs

Every IEPE adoption requires:

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

The IEPE revision must be an immutable tag, commit, or content digest. A moving branch such as `main` is suitable only for provisional development.

### Repository Arrangement

```text
workspace/
├── IEPE-Core/
└── target-project/
```

The target project references the pinned IEPE source. It does not redefine IEPE's claim, evidence, promotion, or stop semantics.

Both initialization modes converge on the same operational condition:

- governing intent is explicit
- authority order is defined
- work is represented as a dependency graph
- the current baseline is recorded
- claims can bound concurrent work
- evidence requirements match the domain
- protected actions require named authority
- unknown variables and negative results are retained
- one bounded issue is Ready for a complete coordinator cycle

## Mode A: New project

### A1. Capture the originating conversation

The initializer separates statements into:

| Class | Meaning |
| --- | --- |
| Intent | Outcome the project exists to cause |
| Established decision | Choice already made by an authorized person |
| Requirement | Condition the project must satisfy |
| Preference | Desired quality that may permit tradeoffs |
| Hypothesis | Testable explanation or proposed approach |
| Constraint | Boundary on implementation or operation |
| Exclusion | Work or outcome intentionally outside scope |
| Unknown | Material variable not yet established |

Conversation is input evidence, not automatic authority. The initializer presents inferred intent and consequential assumptions for correction before committing them to the governing layer.

### A2. Create the governing foundation

A new project should begin with this minimum structure or an equivalent mapping:

```text
project/
├── AGENTS.md
├── INTENT.md
├── PROJECT_PROFILE.json
├── ROADMAP.md
├── .iepe/
│   └── protocol-reference.json
├── .agents/
│   ├── NEW_AGENT_PROMPT.md
│   ├── package-source.json
│   └── runtime/COORDINATOR.md
├── docs/
│   ├── EXPERIENCE.md
│   ├── ARCHITECTURE.md
│   ├── DECISIONS/
│   ├── RESEARCH/
│   └── NEGATIVE_RESULTS/
├── evidence/
├── experiments/
└── work/
```

`INTENT.md` governs purpose, beneficiaries, protected qualities, exclusions, and success evidence. `PROJECT_PROFILE.json` binds the project to workspaces, work graphs, coordinator capacity, evaluators, protected actions, promotion authorities, and memory locations. `AGENTS.md` defines local operating instructions and validation commands. `ROADMAP.md` defines milestones through exit evidence rather than feature inventories.

### A3. Record the zero-state baseline

The absence of implementation is valid evidence. Record what exists, what does not, what has been decided, what is proposed, and what remains unvalidated. Do not use a polished project description as evidence that demand, feasibility, usability, or outcomes have been established.

### A4. Define the first measurable milestone

The milestone states an observable project capability and the evidence required to exit. Its issues form a dependency graph rather than an undifferentiated backlog.

The first milestone should include:

- an intent or experience contract
- the smallest useful artifact or operational result
- domain-appropriate evaluation
- a reversible promotion decision
- at least one material unknown scheduled for investigation

### A5. Select the first Ready issue

Choose a bounded issue with one clear workspace, available dependencies, explicit permissions, reproducible evaluation, and a recovery path. The issue becomes the first end-to-end test of the project engine, not merely the first production task.

## Mode B: Existing project

### B1. Perform read-only discovery

Inventory the project before changing it:

- repositories and workspace structure
- controlling agent instructions
- documentation and architectural decisions
- Git history, active branches, and releases
- open and closed work items
- project-board fields and dependencies
- builds, tests, and validation commands
- deployment configuration
- design assets and experience documentation
- available analytics, observations, and operational evidence

Discovery does not authorize mutation.

### B2. Reconstruct intent with provenance

Every proposed governing statement receives a provenance class:

| Class | Treatment |
| --- | --- |
| Established | Explicit in a governing source |
| Inferred | Repeated pattern or converging evidence |
| Proposed | Future behavior described but not approved |
| Observed | Current behavior without governing authority |
| Unresolved | Unsupported or contradictory |

Current implementation is evidence of behavior, not automatic evidence of intent. The owner or named authority approves the reconstructed intent before the coordinator uses it to reject or promote work.

### B3. Reconcile the work graph

Classify existing work as active, blocked, superseded, completed but unverified, abandoned, duplicate, missing evidence, misaligned, or requiring review. Preserve original identifiers and provenance. Do not rewrite history to create artificial consistency.

### B4. Establish the operational baseline

Run authorized diagnostics and record their environment, results, and limitations. Depending on the project, this may include builds, tests, type checks, browser flows, accessibility, performance, schema validation, documentation integrity, deployment inspection, or security analysis.

Existing failures become baseline facts. They block adoption only when they prevent safe execution or invalidate the selected pilot.

### B5. Select a bounded intervention

Choose a reversible, representative change that can exercise the full IEPE trace without requiring broad architectural repair or an unauthorized external consequence. Reconcile and automate the rest of the backlog incrementally after the pilot qualifies.

## Conversational initialization

A person may initialize a project in natural language. The conversation is processed into a provisional package containing:

- interpreted intent
- intended beneficiaries and experience
- constraints and exclusions
- established decisions
- risky assumptions
- initial unknown-variable ledger
- authority questions
- proposed project profile
- first milestone and work graph
- evaluation and perturbation plan
- permissions and stop conditions
- first Ready issue

The initializer must distinguish user statements from its own inferences. It requests confirmation only for ambiguities that would materially alter intent, authority, external consequences, or irreversible work.

Example entry:

```text
Start a new IEPE project for a browser-based aerodynamics visualization.
It should help students understand how wing shape affects lift and drag.
```

The resulting profile might establish an educational purpose, require physically plausible behavior, exclude engineering certification, identify model fidelity as an unknown, and require separate evidence for technical correctness and student understanding.

## Project profile boundary

The project profile makes the engine portable. It supplies project-specific configuration without changing core coordination semantics.

Software profiles commonly add build, test, browser, deployment, code-ownership, and security evaluators. Editorial profiles add source, fact-checking, voice, legal-review, and publication requirements. Research profiles add hypotheses, datasets, reproducibility, provenance, statistical evaluation, and uncertainty. Design profiles add experience contracts, states, responsive conditions, accessibility, visual evidence, and human observation. Operational profiles add process owners, service levels, cost limits, approval chains, audit records, and affected parties.

Domain profiles may extend evaluation and adapters. They may not silently replace project intent, claim semantics, evidence maturity, protected actions, or promotion authority.

## Initialization gates

Initialization completes only when:

1. Intent and authority are explicit enough to govern the pilot.
2. The project profile conforms to the declared schema (or declares `"profileStatus": "provisional"` if promotion authority is unassigned).
3. The baseline records known failures and evidence gaps.
4. Work-graph relationships required by the pilot are reconciled.
5. Evaluators and evidence maturity are declared.
6. Protected actions and promotion authorities are named (or declared `"unassigned"` for provisional local initialization).
7. The unknown-variable ledger contains material assumptions.
8. A bounded, reversible issue is Ready.

### Preflight Workspace Capability Probe

Before performing discovery or constructing an overlay, the initializer MUST run a single workspace write probe:

1. Test write capability by writing a temporary probe file (e.g. `.iepe-write-test`) inside the authorized workspace.
2. Remove or quarantine the probe immediately.
3. If writes succeed, proceed to discovery and overlay generation.
4. If writes fail (`CAPABILITY_MISSING`), stop ONCE with `ENV_WORKSPACE_READ_ONLY`, do not prepare full overlays, do not retry, and enter `WAITING_EXTERNAL`.

### Provisional Profiles & Promotion Decoupling

Local initialization requires only local reversible action authorization. An unassigned promotion authority generates a provisional profile:

```json
{
  "promotionAuthority": "unassigned",
  "profileStatus": "provisional",
  "promotionBlocked": true
}
```

This permits creation of `AGENTS.md`, `PROJECT_PROFILE.json`, and `.iepe/protocol-reference.json` while blocking milestone promotion until a named authority is assigned.

### Compile the Agent Project Package

After the initialization gates pass, compile the canonical sources into the Agent Project Package defined in [`AGENT_PROJECT_PACKAGE.md`](AGENT_PROJECT_PACKAGE.md). Validate its manifest and integrity before the coordinator uses it to assemble worker context.

## Operational handoff

After initialization, the normal loop begins:

```text
reconcile
  -> select Ready issue
  -> validate authority and dependencies
  -> claim scope
  -> assemble bounded context
  -> dispatch
  -> observe
  -> evaluate
  -> stress test when required
  -> record evidence
  -> disposition and promotion
  -> release claim
  -> select again
```

The coordinator continues until the milestone qualifies, the budget expires, evidence becomes unavailable, authority becomes ambiguous, a protected action is reached, or another declared stop condition occurs.

## Standard Triggers and Reference Commands

### Trigger for an Existing Project (Stage 1: Reconcile)

Start the agent inside the target repository:

```text
Adopt IEPE for this existing project.
Target:
<TARGET_PROJECT_PATH_OR_URL>
Pinned IEPE source:
<IEPE_SOURCE_PATH_OR_URL>
Pinned IEPE revision:
<IMMUTABLE_TAG_COMMIT_OR_DIGEST>
Use and strictly follow:
<IEPE_SOURCE>/AGENTS.md
<IEPE_SOURCE>/.agents/skills/initialize-iepe-project/SKILL.md
<IEPE_SOURCE>/docs/INITIALIZATION.md
<IEPE_SOURCE>/docs/UPSTREAM_REFERENCE.md
<IEPE_SOURCE>/docs/MIGRATION.md
Mode: existing project.
Authority: read-only discovery and reconciliation.
First cycle:
1. Read every applicable AGENTS.md, CLAUDE.md, and nested agent instruction.
2. Inspect repository identity, branches, workspaces, packages, documentation, architecture, decisions, tests, releases, deployments, issues, pull requests, and project boards.
3. Run IEPE existing-project discovery.
4. Reconstruct intent using these provenance classes:
   established, inferred, proposed, observed, and unresolved.
5. Identify the authority order for intent, terminology, experience, architecture, schemas, implementation, operations, and generated artifacts.
6. Reconcile the work graph, dependencies, claims, implementation state, reviews, releases, deployments, and evidence.
7. Identify contradictions, stale work, incomplete issue contracts, unsupported maturity, missing evidence, protected actions, and material unknowns.
8. Propose the project-specific IEPE profile.
9. Propose how IEPE should integrate with existing agent instructions without replacing valid local authority.
10. Select one bounded and reversible pilot issue.
Do not modify files, create or change work items, alter project fields, push, merge, deploy, publish, spend, or communicate externally.
Return:
- discovery report
- authority and provenance map
- project baseline
- proposed PROJECT_PROFILE.json
- proposed protocol reference
- proposed AGENTS.md integration
- work-graph reconciliation
- unknown-variable ledger
- protected-action list
- proposed overlay file map
- first candidate pilot issue
- blockers and decisions requiring human authority
```

The discovery command is:

```bash
python3 <IEPE_SOURCE>/tools/init_project.py existing \
  --project-root <TARGET_PROJECT_ROOT>
```

To save the report without changing the project:

```bash
python3 <IEPE_SOURCE>/tools/init_project.py existing \
  --project-root <TARGET_PROJECT_ROOT> \
  --report <PATH_OUTSIDE_TARGET>/iepe-discovery.json
```

### Trigger for a New Project

A new project may initialize directly after its originating intent and protocol reference are supplied:

```text
Initialize a new project under IEPE.
Project root:
<TARGET_PROJECT_ROOT>
Project ID:
<PROJECT_ID>
Project name:
<PROJECT_NAME>
Originating intent:
<PROJECT_INTENT>
Pinned IEPE source:
<IEPE_SOURCE_PATH_OR_URL>
Pinned IEPE revision:
<IMMUTABLE_TAG_COMMIT_OR_DIGEST>
Work-graph provider:
<LOCAL_GITHUB_OR_OTHER>
Evaluator candidates:
<EVALUATORS>
Promotion authority:
<NAMED_AUTHORITY>
Use:
<IEPE_SOURCE>/.agents/skills/initialize-iepe-project/SKILL.md
<IEPE_SOURCE>/docs/INITIALIZATION.md
<IEPE_SOURCE>/docs/UPSTREAM_REFERENCE.md
Initialize the project without claiming that beneficiaries, architecture, implementation, demand, usability, or outcomes are established.
After initialization:
1. Validate the protocol reference and project profile.
2. Record the zero-state baseline.
3. Separate established decisions from agent inference.
4. Identify protected qualities and protected actions.
5. Create the initial unknown-variable ledger.
6. Define the first milestone through exit evidence.
7. Propose one bounded, reversible Ready issue.
8. Compile the Agent Project Package.
9. Return the generated files, validation evidence, unresolved authority, and first-agent prompt.
Do not deploy, publish, spend, create external resources, or communicate externally.
```

The corresponding command is:

```bash
python3 <IEPE_SOURCE>/tools/init_project.py new \
  --project-root <TARGET_PROJECT_ROOT> \
  --project-id <PROJECT_ID> \
  --project-name "<PROJECT_NAME>" \
  --intent "<PROJECT_INTENT>" \
  --protocol-source "<IEPE_SOURCE_PATH_OR_URL>" \
  --protocol-revision "<IMMUTABLE_REVISION>" \
  --work-graph-provider <PROVIDER> \
  --project-ref <PROJECT_REFERENCE> \
  --evaluator <EVALUATOR> \
  --promotion-authority <AUTHORITY>
```

### Trigger to Apply an Approved Existing-Project Adoption (Stage 2: Apply)

After reviewing the reconciliation report and approving the adoption plan:

```text
Apply the approved IEPE adoption plan.
Target:
<TARGET_PROJECT>
Approved reconciliation:
<REPORT_PATH_OR_ISSUE_REFERENCE>
Mutation authority:
local repository files on an isolated branch
Preserve all existing project authority and unrelated changes. Integrate with existing agent instructions instead of replacing them.
Create or update only the approved IEPE operating layer:
- .iepe/protocol-reference.json
- AGENTS.md
- PROJECT_PROFILE.json
- .agents/package-source.json
- .agents/NEW_AGENT_PROMPT.md
- .agents/runtime/COORDINATOR.md
- .agents/skills/*
- approved authority and memory documents
- approved work-graph configuration
Configure evaluators from actual project commands and evidence. Do not invent tests, providers, deployment targets, issue relationships, or authority.
Compile the Agent Project Package and run IEPE plus project-native validation.
Do not push, merge, deploy, publish, modify live work items, or communicate externally.
Return:
- complete diff
- validation evidence
- package manifest
- unresolved evidence gaps
- limitations
- proposed pilot issue
- next action requiring authorization
```

### Trigger for the First Operational Agent

Once the project overlay is installed:

```text
Operate this project under its pinned IEPE protocol reference.
Follow AGENTS.md, PROJECT_PROFILE.json, and the narrowest applicable skill under .agents/skills.
Your first cycle is read-only reconciliation. Verify project identity, protocol revision, authority, work graph, dependencies, claims, evaluators, protected actions, and evidence.
Return a typed reconciliation result and the first candidate Ready issue. Do not claim or implement work until the project is internally consistent and the issue contract is complete.
```

After that first cycle, the normal IEPE operational loop begins:

```text
reconcile
-> select
-> validate
-> claim
-> assemble bounded context
-> dispatch
-> observe
-> evaluate
-> stress test when required
-> record evidence
-> disposition
-> release claim
-> repeat
```

This universal trigger pattern applies across software, research, writing, design, operations, physical production, and mixed-domain projects. Only the local project profile, adapters, evaluators, protected actions, and authority sources change.

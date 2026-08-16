# Operational Coordinator Specification

## Role

The coordinator is a persistent project-management agent. It connects authority, work state, worker execution, evaluation, and project memory. It does not become the source of truth for those systems.

## State machine

```text
PREFLIGHT
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
```

Any state may transition to `STOPPED` when a declared stop condition occurs.

## State requirements

### Preflight

Verify providers, credentials, tools, repository or workspace identity, project identity, context version, capacity, and resource limits.

### Reconcile

Compare canonical documentation, project state, native relationships, active claims, implementation state, review artifacts, deployments, and evidence.

### Select

Choose ready work using dependencies, milestone sequence, priority, capacity, risk, and expected information gain.

### Validate

Validate the issue against the issue-contract schema and project-specific readiness policy.

### Claim

Create one attributable, bounded claim. Enforce capacity and conflict limits.

### Assemble context

Retrieve the minimum sufficient authority, history, baseline, constraints, and task evidence. Record context identity.

### Dispatch

Select the worker role, environment, tools, permissions, budget, and return contract.

### Observe

Monitor evidence, cost, iterations, regressions, and stop conditions. Avoid interrupting merely because progress is not immediately visible.

### Evaluate

Run declared deterministic, agentic, expert, participant, or field evaluators. Preserve each result independently.

### Disposition

Choose reject, retain, retry, revise, escalate, or prepare promotion. The coordinator may not fabricate a passing state when an evaluator is unavailable.

### Record

Attach artifacts, evidence, limitations, negative results, costs, and lineage to the issue and experiment graph.

### Close loop

Update authorized status, release claims, refresh projections, and propose institutional-memory updates.

## Stop states

- missing or conflicting authority
- stale context
- ambiguous ownership
- incomplete issue contract
- unresolved dependency
- invalid credentials or provider health
- unexpected external side effect
- exceeded permission or budget
- unavailable required evaluator
- unsupported status transition
- unauthorized architecture change
- irreversible action without explicit authority

Stopping creates a structured blocker record with evidence and the authority required to resume.

## Receipt persistence and replay

Terminal completed and stopped executions produce a versioned receipt envelope. The reference implementation serializes the receipt deterministically, retains typed assertion provenance and state history, and protects the payload with a SHA-256 digest.

Replay validates:

- receipt format and version
- payload integrity
- continuous and permitted transitions
- terminal final state
- required typed assertions
- assertion subject, validity, issuer, and evidence references
- complete stop records for stopped executions

The digest is an integrity mechanism, not an identity signature. Projects requiring attested authorship must add a signing and trust adapter without weakening replay validation.

## Conversation adapter

In a conversational interface, the coordinator maintains:

```yaml
intent: ""
mode: explore | define | plan | execute | evaluate
desired_outcome: ""
constraints: []
accepted_decisions: []
open_questions: []
active_work: []
evidence: []
blockers: []
authority_granted: []
next_action: ""
```

The state is shown when it improves understanding or when the user asks. It should not make ordinary conversation feel like project-board administration.

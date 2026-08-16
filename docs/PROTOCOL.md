# Intent and Evidence Project Engine Protocol

> Protocol: `IEPE-001`  
> Version: `0.1.0`  
> Status: Draft reference protocol  
> Scope: Domain-neutral

## Definition

IEPE is a governed process that converts project intent into authorized work, generates or implements candidate interventions, evaluates results against declared evidence, preserves learning, and promotes only qualified outcomes.

## Constitutional invariants

1. Intent governs implementation.
2. Canonical documentation defines project authority.
3. Tickets authorize committed work.
4. The project graph owns live status and dependencies.
5. Coordination, execution, evaluation, and promotion are distinct responsibilities.
6. Evidence qualifies claims.
7. Exploration authority may exceed promotion authority.
8. Negative results become project memory.
9. Metrics may inform intent but may not silently replace it.
10. Invalid authority, context, ownership, permissions, or evidence is a stop state.
11. Environmental capability checks must precede discovery and preparation.
12. Non-retryable blockers must fingerprint, emit once, and enter a parked state (`WAITING_EXTERNAL`) to prevent livelocks.

## Engine planes

| Plane | Responsibility |
| --- | --- |
| Intent and Authority | Purpose, values, doctrine, terminology, constraints, decisions |
| Experience and Design | Human outcomes, journeys, interactions, accessibility, design system |
| Coordination | Work graph, dependencies, claims, budgets, scheduling, dispatch |
| Execution | Research, design, implementation, testing, and bounded operations |
| Evaluation and Evidence | Verification, observation, comparison, qualification, lineage |

## Condition classification taxonomy

The coordinator distinguishes unresolved conditions into six explicit types:

| Condition | Meaning | Coordinator Response |
| --- | --- | --- |
| `AUTHORIZATION_MISSING` | User has not permitted the action | Ask one precise question |
| `CAPABILITY_MISSING` | Environment cannot perform the action | Stop once; identify the required capability |
| `EVIDENCE_MISSING` | Promotion cannot yet be justified | Continue allowed preparation; block only promotion |
| `INPUT_MISSING` | Consequential project decision is unresolved | Use provisional value or ask if execution materially depends on it |
| `WORK_UNAVAILABLE` | Nothing actionable is Ready | Park the loop |
| `EXTERNAL_EVENT_PENDING` | Only another actor can change state | Enter `WAITING_EXTERNAL`; do not retry |

## Authority boundaries and implicit defaults

### Initialization vs. Promotion Authority

Creating local, reversible project-operating files (e.g. `AGENTS.md`, `PROJECT_PROFILE.json`, `.iepe/protocol-reference.json`) requires only local reversible authorization. Unassigned promotion authority yields:

```json
{
  "promotionAuthority": "unassigned",
  "profileStatus": "provisional",
  "promotionBlocked": true
}
```

It must not prevent creation of local operating documentation or initial work contracts.

### Implicit Action Authorization

When a user requests project initialization or local adoption, the implicit authorization defaults are:

- `read_project`: allowed
- `write_local_iepe_files`: allowed
- `run_local_validation`: allowed
- `create_external_work_items`: not_allowed
- `push_or_merge`: not_allowed
- `deploy_or_publish`: not_allowed
- `spend_or_change_credentials`: not_allowed

### Hard-blocker fingerprinting

Every blocker receives a stable fingerprint:

```json
{
  "code": "ENV_WORKSPACE_READ_ONLY",
  "scope": "target-project",
  "requiredChange": "workspace-write capability",
  "retryableByAgent": false,
  "fingerprint": "ENV_WORKSPACE_READ_ONLY:target-project"
}
```

If the current blocker fingerprint matches the previous non-retryable blocker, the coordinator MUST NOT retry, reread the objective, or consume additional attempts. It immediately enters `WAITING_EXTERNAL` and returns control to the user.

## Canonical objects

Projects may extend these objects but should preserve their meanings:

- `ProjectIntent`
- `ExperienceContract`
- `DesignDecision`
- `PortfolioObjective`
- `Milestone`
- `Epic`
- `IssueContract`
- `Experiment`
- `Candidate`
- `Baseline`
- `Evaluation`
- `EvidenceBundle`
- `Qualification`
- `Promotion`
- `NegativeResult`

## Work modes

### Delivery

Use when the desired change is understood.

```text
Ready -> Claimed -> Implemented -> Reviewed -> Done -> Verified
```

### Improvement

Use when the outcome is understood but the best intervention is uncertain.

```text
Baseline -> Hypotheses -> Candidate beam -> Evaluation -> Promotion decision
```

### Conversation

Use when the project is operated through a conversational coordinator.

```text
Explore -> Define -> Plan -> Execute -> Evaluate
```

Conversation modes may recur. The coordinator maintains intent and work state beneath a natural interface.

## Issue readiness

An issue is ready only when it defines:

- governing intent
- objective or hypothesis
- ownership and parent relationship
- dependencies
- acceptance criteria
- evidence requirements
- affected experience or design contracts
- constraints and exclusions
- permissions and side effects
- budget
- stop and escalation conditions

## Worker contract

A worker receives a bounded packet containing the issue, authority references, scope, constraints, acceptance, evidence, permissions, budget, stop conditions, and return requirements.

A worker returns artifacts, evidence, limitations, blockers, cost where material, and a recommended next action. It does not accept or promote its own work unless the project explicitly permits that low-risk operation.

## Evaluation

Evaluation uses a visible vector rather than hiding material tradeoffs in one score. Applicable dimensions may include:

- correctness
- intent alignment
- human effectiveness
- accessibility
- quality
- performance
- cost
- risk
- maintainability
- portability
- trust
- uncertainty

Human evidence is required before claims about comprehension, lived usefulness, emotional quality, cultural interpretation, trust, or delight become empirically validated.

## Promotion

Promotion is separate from evaluation. It requires valid authority, complete lineage, required checks, independent assessment where specified, visible tradeoffs, recovery planning where applicable, and a retained decision record.

## Epistemic stress testing

Qualified candidates may require designed perturbations before promotion. A candidate is frozen before sealed World Cards are revealed. Resulting robustness dispositions and unknown-variable discoveries inform, constrain, revise, block, or escalate promotion without silently changing governing intent. See [`EPISTEMIC_STRESS_TESTING.md`](EPISTEMIC_STRESS_TESTING.md).

## Memory

Operational memory retains issues, runs, candidates, evidence, and incidents. Institutional memory retains approved doctrine, specifications, decisions, design systems, standards, and rejected directions.

Generated context is a downstream projection of canonical sources.

## Protocol expression

> Define intent. Authorize through tickets. Explore within bounds. Evaluate independently. Promote through evidence. Preserve what the project learns.

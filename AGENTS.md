# IEPE Core Agent Operating Contract

This repository develops the project-agnostic Intent and Evidence Project Engine.

## Authority

Resolve conflicts in this order:

```text
1. docs/PROTOCOL.md
2. Approved decision records
3. JSON schemas
4. Coordinator and adoption specifications
5. Issue contracts and acceptance criteria
6. Implemented code and templates
7. Generated artifacts and agent output
```

## Required operating behavior

Intent governs implementation. Issues authorize committed work. Project state belongs in the work graph. Agents execute only within bounded authority. Evaluation is independent from candidate authorship where practical. Promotion requires declared evidence.

Every material change must preserve:

```text
intent -> epic -> issue -> artifact -> evidence -> qualification -> promotion
```

## Ticket-first rule

Committed changes require a complete issue contract with intent, objective or hypothesis, owner, parent, dependencies, acceptance, evidence, constraints, permissions, budget, and stop conditions.

## Maturity

Keep these dimensions separate:

```text
Backlog -> Ready -> In progress -> In review -> Done -> Verified
Documented != Implemented != Tested != Empirically Validated
Intent -> Explored -> Specified -> Prototyped -> Implemented -> Observed -> Validated
```

## Stop rule

Continue while authority, context, ownership, dependencies, permissions, and evidence remain valid. Stop at unverified boundaries.

## Generalization rule

Core artifacts must remain domain-neutral. Domain-specific terminology, integrations, evaluators, and policies belong in adoption profiles or adapters.

## Process routing

Use the narrowest applicable project-local skill:

- `initialize-iepe-project` for new and existing project adoption.
- `reconcile-iepe-project` for first-cycle and stale-state reconciliation.
- `operate-iepe-project` for the coordinator execution loop.
- `qualify-iepe-outcome` for evidence and promotion review.
- `stress-test-iepe-candidate` for designed unknown-variable trials.
- `maintain-iepe-package` for package compilation and protocol updates.

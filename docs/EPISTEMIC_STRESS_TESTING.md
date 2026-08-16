# Epistemic Stress Testing

## Definition

Epistemic stress testing uses **designed perturbations** to reveal assumptions, unknown variables, brittle dependencies, absent perspectives, and validity boundaries that ordinary optimization may not expose.

The operating question is:

> What must remain true for this result to remain good?

## Blind Counterfactual Trial

After a candidate qualifies against its known evaluation contract, it is frozen. A sealed World Card is then revealed and the frozen candidate is evaluated under the changed conditions.

```text
Known contract
  -> Candidate development
  -> Known evaluation
  -> Candidate freeze
  -> World Card reveal
  -> Counterfactual trial
  -> Robustness disposition
  -> Promotion decision
```

The candidate-producing worker must not see the World Card before the freeze gate.

## Protected invariants

Perturbations may change context, constraints, evidence availability, actor perspective, time, dependency behavior, or scale. They may not silently remove:

- governing project intent
- safety and human-rights constraints
- consent requirements
- factual standards
- identity boundaries
- promotion authority

## Perturbation families

| Family | Example |
| --- | --- |
| Context | different environment, audience condition, language, or interaction mode |
| Constraint | reduced time, budget, tools, connectivity, or provider access |
| Evidence | conflicting sources, delayed telemetry, missing provenance, invalid evaluator |
| Actor | maintainer, purchaser, regulator, child, critic, or affected non-user |
| Time | accumulated state, future dependency, absent original team, emergency repair |
| Dependency | unavailable provider, read-only service, degraded integration |
| Scale | one versus millions, local exception versus global process |
| Intent collision | privacy with personalization, simplicity with expert control, speed with auditability |

## Surprise budget

Projects reserve evaluation capacity for conditions hidden during candidate development. A project profile may define a percentage, minimum World Card count, required candidate visibility, and promotion classes that require stress testing.

A starting reference profile is fifteen percent of evaluation capacity and at least two sealed World Cards before architecture freeze, production promotion, or an empirical-validation claim.

## Robustness dispositions

| Disposition | Meaning |
| --- | --- |
| Robust | Candidate remains qualified without adaptation |
| Adaptable | An authorized bounded adjustment restores qualification |
| Bounded | Candidate remains valid only within a narrower declared domain |
| Fragile | Candidate fails under a plausible changed condition |
| Unsafe | Candidate crosses a protected invariant |
| Unknown | Available evaluation cannot establish the result |

A bounded result can remain useful. Stress testing should reveal validity conditions rather than demanding universal robustness.

## Unknown-variable ledger

Unknowns are classified as:

- known and controlled
- known but unresolved
- assumed but untested
- observed only once
- discovered through perturbation
- currently unknowable

The ledger guides future World Card selection toward neglected uncertainty classes.

## Authority

The Perturbation Steward creates or selects World Cards independently from candidate authorship where practical. The steward does not redefine intent, approve promotion, or waive protected invariants.

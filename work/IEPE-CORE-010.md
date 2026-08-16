# IEPE-CORE-010: Add Epistemic Stress Testing

## Intent

Expose hidden assumptions and unknown variables before promotion by testing frozen candidates against controlled conditions they were not optimized to satisfy.

## Type

Delivery

## Parent

M2: Coordinator Reference

## Objective

Add designed perturbations, sealed World Cards, surprise budgets, robustness profiles, and an unknown-variable ledger to the IEPE protocol and conformance suite.

## Acceptance criteria

- Epistemic stress testing is distinct from ordinary evaluation and random disruption.
- Perturbations declare protected invariants and changed conditions.
- World Cards remain sealed until a candidate-freeze gate.
- Robustness dispositions include robust, adaptable, bounded, fragile, unsafe, and unknown.
- Unknown variables are classified rather than collapsed into one uncertainty field.
- Projects can define a surprise budget.
- One existing candidate completes at least two synthetic blind counterfactual trials.
- Stress trials cannot silently change project intent or promotion authority.
- Human-outcome claims remain unvalidated without observation.

## Evidence required

- Protocol document.
- Contract schemas and conformance fixtures.
- GitHub issue template.
- Synthetic World Cards and robustness profile.
- Updated unknown-variable ledger.
- Conformance results.

## Constraints

- Initial trials are synthetic.
- No random destructive mutations.
- Protected human, safety, consent, identity, and authority invariants cannot be perturbed away.
- Do not treat fragility as universal failure when the validity boundary can be stated honestly.

## Permissions

- Local documents, schemas, templates, examples, and evaluation artifacts: allowed.
- External experiments, communications, deployment, and spending: not authorized.

## Stop conditions

- A perturbation changes the governing purpose rather than testing its realization.
- The evaluator lacks authority or evidence for the resulting claim.
- A trial could create an external consequence.

## Result

Two sealed synthetic World Cards were revealed after Candidate B was frozen. The trials produced bounded and adaptable dispositions, constrained promotion, and added three classified unknowns without making a human-outcome claim.

## Status

Verified / Tested

# IEPE-CORE-002: Complete the M1 Contract and Template Suite

## Intent

Make IEPE adoptable by unrelated projects without requiring them to invent core intent, experience, evaluation, decision, incident, or promotion records.

## Type

Delivery

## Parent

M1: Adoption Kit

## Objective

Add the missing domain-neutral schemas and GitHub issue templates required to operate the principal IEPE work types.

## Acceptance criteria

- Project profile schema defines authority, work graph, coordinator, evaluators, protected actions, promotion authorities, and memory.
- Experience contract schema preserves audience, desired outcomes, qualities, states, constraints, accessibility, and evidence.
- Evaluation record schema represents independent multi-dimensional assessment.
- Promotion record schema separates qualification from adoption authority.
- GitHub templates exist for design, evaluation, decision, incident, and promotion work.
- Every JSON schema parses and validates representative valid and invalid fixtures.
- Every YAML issue template parses.
- Core artifacts contain no project-specific authority or runtime dependency.
- README and roadmap accurately report maturity.

## Evidence required

- Automated parsing results.
- Positive and negative JSON Schema fixture results.
- Cross-file identifier and reference audit.
- Domain-neutrality search.
- Updated evidence bundle.

## Constraints

- Remain provider-neutral at the protocol layer.
- GitHub files are reference adapters, not core authority.
- Do not claim coordinator implementation.
- Do not claim empirical validation.

## Permissions

- Local file writes: allowed within `IEPE-Core`.
- Library replacement: allowed for the existing project archive after qualification.
- GitHub writes: not authorized or available.
- Deployments: not authorized.
- External communication: not authorized.
- Spending: not authorized.

## Stop conditions

- A required contract cannot be expressed without domain-specific assumptions.
- Validation tooling is unavailable and cannot be replaced by a local equivalent.
- Existing authority conflicts with the proposed schema semantics.

## Status

Verified

## Claim maturity

Tested

## Result

Six domain-neutral schemas and seven GitHub issue templates passed structural evaluation. One residual originating-project name was found during domain-neutrality review and removed before qualification. See `evidence/IEPE-CORE-002-evidence.json`.

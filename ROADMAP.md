# IEPE Core Roadmap

## Project intent

Make rigorous agentic project operation portable across domains without forcing every project to invent its own coordination, evidence, and promotion model.

## M1: Adoption Kit

Goal: make IEPE installable as a documentation and GitHub workflow profile.

- Refine the protocol vocabulary and boundaries. **In progress**
- Validate issue and evidence schemas. **Tested**
- Add design, evaluation, decision, incident, and promotion templates. **Tested**
- Define the minimum project profile. **Tested as schema**
- Provide a reproducible conformance command and fixture suite. **Tested locally**
- Define migration from an existing ticket system. **Tested synthetically**
- Produce one complete example project. **Tested synthetically**
- Specify new-project and existing-project initialization. **Documented**
- Implement reference-pinned command-line initialization. **Tested locally**
- Implement conversational initialization.
- Compile canonical sources into Agent Project Packages. **Tested locally**

Exit evidence: an unrelated pilot can adopt the protocol and create a valid work graph without additional doctrine.

## M2: Coordinator Reference

Goal: implement a provider-neutral coordinator state machine.

- Project preflight and reconciliation. **State gates tested locally**
- Readiness validation. **Typed assertion gates tested locally**
- Claim and capacity management. **Tested locally**
- Context-packet assembly. **Tested locally**
- Worker dispatch interfaces. **Tested locally**
- Evidence intake and qualification.
- Stop-state enforcement. **Tested locally**
- Receipt persistence and replay. **Tested locally**
- Epistemic stress testing. **Tested synthetically with sealed World Cards**
- Promotion recommendation.

Exit evidence: a coordinator can complete a simulated delivery issue and experiment while rejecting invalid transitions.

## M3: GitHub Adapter

Goal: make GitHub Issues and Projects a complete IEPE work-graph adapter.

- Native hierarchy and dependency mapping.
- Field and status synchronization.
- Branch, commit, pull request, and deployment lineage.
- Evidence comments and reconciliation.
- Portfolio and focused-project projections.

Exit evidence: an end-to-end pilot completes through a real GitHub project.

## M4: Experience and Design Qualification

Goal: prove that intent and design survive agentic decomposition.

- Experience-contract schema.
- Journey and interaction references.
- Automated UI evidence adapters.
- Human observation records.
- Design maturity enforcement.

Exit evidence: a user-facing change remains traceable from intent through observed production behavior.

## M5: Cross-Domain Validation

Goal: validate IEPE outside software engineering.

- Research pilot.
- Writing or editorial pilot.
- Business-operations pilot.
- Creative-production pilot.

Exit evidence: the core remains unchanged while domain profiles supply appropriate evaluators and promotion rules.

## Initial epics

1. Protocol and terminology refinement.
2. Contract and schema suite.
3. Coordinator state machine.
4. GitHub adapter.
5. Experience and design evaluation.
6. Project memory and negative-result retention.
7. Pilot and conformance suite.

# IEPE-CORE-016: Implement Reference-Pinned Project Bootstrap

## Intent

Make IEPE directly usable when starting a new agent or project by generating a local operating layer that references a versioned IEPE Core source without copying project-specific assumptions into the protocol.

## Type

Delivery

## Parent

M1: Adoption Kit

## Owner

IEPE Core coordinator

## Dependencies

- IEPE-CORE-012
- IEPE-CORE-013
- IEPE-CORE-014

## Scope

- Define a machine-readable upstream protocol reference.
- Implement deterministic greenfield scaffolding and read-only existing-project discovery.
- Generate a compact `AGENTS.md`, project profile, coordinator configuration, package-source declaration, and first-cycle prompt.
- Bind Agent Project Packages to the upstream protocol reference.
- Document the adoption and update boundary.

## Exclusions

- Creating or configuring a live GitHub repository or Project.
- Installing credentials or provider applications.
- Inferring production authority from repository access.
- Automatically rewriting an established project's governing documentation.

## Acceptance criteria

- A new project can be initialized from one command with an explicit IEPE source and immutable revision.
- The generated project separates upstream invariants from local intent, profile, skills, adapters, and evidence.
- A new agent receives an unambiguous read-only first-cycle prompt.
- Existing-project discovery performs no writes unless an external report path is explicitly supplied.
- Package manifests retain the pinned IEPE protocol identity and revision.
- Repeated initialization with identical inputs produces identical files.
- Existing files are never overwritten without explicit authorization.
- Tests cover generation, determinism, overwrite refusal, read-only discovery, and protocol provenance.

## Required evidence

- IEPE conformance suite
- Bootstrap unit tests
- A generated synthetic project that compiles into a valid Agent Project Package
- A deliberate overwrite refusal

## Permissions

- Write within `IEPE-Core` and temporary test directories.
- No network, external repository, provider, deployment, publication, or credential mutation.

## Budget

- One bounded implementation cycle with local deterministic tests.

## Stop conditions

- The upstream reference cannot be represented without inventing a canonical repository URL.
- Existing IEPE schemas require an incompatible authority change.
- Validation would require live provider access.

## Definition of done

The bootstrap and provenance contracts are implemented, documented, tested, recorded in evidence, and honestly classified by maturity.

## Result

IEPE Core now generates a deterministic, reference-pinned operating layer for new projects and performs read-only discovery for established projects. The generated layer includes local intent and profile authority, a protocol pin, coordinator runtime, six narrow process skills, package-source declaration, and a first-agent reconciliation prompt. Compiled packages retain protocol provenance.

## Status

Verified / Tested

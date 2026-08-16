# IEPE-CORE-012: Specify New and Existing Project Initialization

## Intent

Make IEPE adoption portable to both greenfield and established projects without confusing conversation, current behavior, or historical tickets with governing authority.

## Type

Documentation

## Parent

M1: Adoption Kit

## Acceptance criteria

- New-project initialization defines conversation capture, governing structure, zero-state baseline, first milestone, and first Ready issue.
- Existing-project initialization begins with read-only discovery and provenance-aware reconciliation.
- Conversational initialization separates user statements from agent inference.
- Domain profiles extend evaluation without replacing core semantics.
- Initialization gates and operational handoff are explicit.
- Proposed commands are labeled unimplemented.

## Result

`docs/INITIALIZATION.md` defines both entry modes, their convergence conditions, project-profile boundary, conversational entry, and handoff into the coordinator loop. `docs/ADOPTION.md` now routes adopters through these modes.

## Status

Verified / Documented

# Upstream IEPE Reference

## Purpose

An adopting project should reference a versioned IEPE Core source instead of copying the protocol into local documentation. This preserves a visible boundary between stable process semantics and project-specific authority.

```text
IEPE Core at immutable revision
  -> protocol invariants and schemas
  -> local protocol reference
  -> local project profile and authority
  -> compiled Agent Project Package
  -> coordinator and worker cycles
```

## Required pin

The project records `.iepe/protocol-reference.json` with:

- `protocolId`: the governing protocol identity, currently `IEPE-001`
- `protocolVersion`: the declared semantic version
- `source`: the canonical repository or content-addressed source
- `revision`: an immutable commit, release tag, or digest
- `relationship`: `reference` or `vendored`
- `conformanceCommand`: the validation entry point for the pinned source

A branch name such as `main` is not an adequate release pin. It may be used during provisional development only when the package reports provisional or unknown source state.

## Authority boundary

Upstream IEPE owns invariant semantics for claims, bounded context, worker dispatch, evidence maturity, perturbation, promotion, receipts, project memory, and stop conditions. The adopting project owns intent, beneficiaries, experience, architecture, workspaces, providers, evaluators, local procedures, protected actions, and named authorities.

Local files may specialize IEPE. They may not redefine artifact existence as evaluation, bypass claims, remove provenance, weaken a protected action, or promote beyond available evidence.

## Update procedure

Treat an IEPE revision change as a governed dependency update:

1. Read the release or revision difference.
2. Run upstream conformance at the proposed revision.
3. Validate the local project profile and compiled package.
4. Reconcile schema, status, adapter, and authority changes.
5. Exercise one representative coordinator cycle in a reversible environment.
6. Record evidence and update the pin only after qualification.

Do not let an agent update the protocol pin as incidental cleanup during ordinary project work.

## New-agent preflight

The first agent verifies that the recorded source and revision can resolve the declared protocol and schemas. If the source is unavailable, the revision is mutable, or the local profile conflicts with the pinned protocol, the agent returns a stopped reconciliation result. Repository access alone does not authorize repair.

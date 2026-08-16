# Agent Project Package

## Definition

An Agent Project Package is a versioned, reproducible operating bundle compiled from a project's canonical sources. It gives coordinators and workers a governing contract, searchable context, installed procedures, provider adapters, provenance, and integrity metadata without making generated artifacts authoritative.

```text
canonical sources
  -> package compiler
  -> operating contract
  -> context index
  -> compiled corpus
  -> skill and adapter inventory
  -> package manifest and digest
```

## Authority boundary

The package preserves this order:

```text
canonical intent and doctrine
  -> ontology and formal contracts
  -> implementation sources
  -> generated package artifacts
```

Generated output is a projection. A contradiction is repaired in the canonical source and then recompiled. Generated context must never be edited to overrule its source.

## Package planes

| Plane | Purpose |
| --- | --- |
| Governance | Compiled operating contract and authority order |
| Context | Compact source index and selectively readable full corpus |
| Procedure | Narrow skills with declared triggers and operating boundaries |
| Adapter | Provider-specific translation for work graphs, repositories, deployments, or evidence systems |
| Runtime | Coordinator configuration, worker roles, claims, and gates |
| Integrity | Source versions, state, exclusions, hashes, and manifest |

The manifest also binds the package to its upstream IEPE protocol source, version, and immutable revision. Identical local sources compiled under different protocol revisions are different operating packages even when their generated context bytes happen to match.

Skills describe reusable procedures. Adapters translate provider operations. Project profiles bind both to project-specific vocabulary, identifiers, authority, and protected actions. A reusable skill must not require a particular repository name, board number, or product ontology.

## Required outputs

- `AGENTS.md`: compiled or selected project operating contract
- `context-index.md`: compact source-routing manifest
- `context-full.md`: deterministic concatenation of selected sources
- `agent-package-manifest.json`: package identity, provenance, inventories, outputs, exclusions, and payload digest
- `.iepe/protocol-reference.json`: project-local pin to the governing IEPE source and revision

Projects may add role prompts, scripts, schemas, and assets. Every included artifact must be declared in the manifest or traceable through a declared source.

## Compiler requirements

The compiler must:

- resolve paths beneath the declared project root
- reject missing, absolute, or escaping paths
- require one operating-contract source
- retain explicit source roles and authority ranks
- generate stable ordering
- hash canonical inputs and generated outputs
- retain the IEPE protocol identity, source, version, and revision
- disclose clean, dirty, unknown, or provisional source state
- reject release classification when source state is not clean
- exclude machine metadata, bytecode, caches, secrets, and undeclared files
- avoid timestamps or nondeterministic values unless supplied as versioned input
- produce byte-identical output for identical declared input

## Context use

Workers consult the compact index first. The full corpus is a searchable source, not routine prompt payload. The coordinator assembles a bounded context packet from the package according to the claimed issue, authority references, dependencies, evidence requirements, and stop conditions.

## Maturity

A conforming package proves that declared sources were compiled reproducibly. It does not prove that the sources are correct, the skills are effective, the adapters are operational, or project outcomes are empirically valid. Those remain separate evidence claims.

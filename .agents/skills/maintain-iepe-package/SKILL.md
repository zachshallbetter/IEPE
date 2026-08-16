---
name: maintain-iepe-package
description: Compile, validate, or update an IEPE Agent Project Package and its upstream protocol pin. Use when canonical sources, skills, adapters, schemas, or IEPE versions change, or when generated context is stale.
---

# Maintain an IEPE Package

Read `docs/AGENT_PROJECT_PACKAGE.md` and `docs/UPSTREAM_REFERENCE.md` from the pinned source.

Repair contradictions in canonical project sources, then compile the package. Never edit generated context as an authority fix. Retain source roles, ranks, state, hashes, skills, adapters, exclusions, protocol identity, and revision.

For a protocol update, compare revisions, run upstream conformance, validate the local profile, reconcile schema and adapter changes, and exercise one reversible coordinator cycle. Change the pin only after qualification.

Release classification requires clean declared source state. Package integrity does not prove semantic correctness or empirical validity.

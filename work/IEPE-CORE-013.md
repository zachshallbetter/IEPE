# IEPE-CORE-013: Implement Agent Project Packages

## Intent

Compile canonical project sources into a versioned agent-operable package without allowing generated context to become authority.

## Type

Delivery

## Parent

M1: Adoption Kit

## Acceptance criteria

- Package planes separate governance, context, procedure, adapters, runtime, and integrity.
- A manifest records source roles, authority ranks, state, hashes, outputs, skills, adapters, and exclusions.
- The compiler rejects missing, unsafe, machine-generated, and duplicate sources.
- Release packages require clean source state.
- Identical inputs produce byte-identical outputs.
- Generated artifacts remain non-authoritative.

## Result

The reference compiler produces a deterministic operating contract, context index, compiled corpus, and integrity manifest. It records skills and adapters while rejecting unsafe inputs and dishonest release state.

## Status

Verified / Tested

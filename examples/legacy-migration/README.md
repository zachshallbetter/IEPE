# Legacy Migration Fixture

This synthetic fixture tests incremental IEPE adoption against a small pre-existing backlog.

The fixture includes:

- one closed historical item with no reason to enrich it
- one active item with partial provenance that requires reconciliation
- one new item created after the adoption boundary that must satisfy the full contract

The fixture does not simulate a live provider. It validates classification, status honesty, evidence gaps, and preservation of source identity.

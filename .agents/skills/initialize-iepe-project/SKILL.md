---
name: initialize-iepe-project
description: Initialize a new project under IEPE or inspect an existing project for adoption. Use when starting a project, creating its agent operating layer, adopting IEPE, generating a project profile, or preparing the first agent cycle.
---

# Initialize an IEPE Project

Read `docs/INITIALIZATION.md` and `docs/UPSTREAM_REFERENCE.md` from the pinned IEPE Core source.

IEPE adoption follows a two-stage pattern: **reconcile first, then apply**.

### Universal Inputs Required
- `target_project`, `project_mode` (`new` | `existing`), `iepe_source`, `iepe_revision` (immutable tag/digest), `project_intent`, `work_graph_provider`, `mutation_authority`, `protected_actions`.

### Existing Project Adoption (Two-Stage)
1. **Stage 1 (Reconcile):** Execute read-only discovery using `tools/init_project.py existing --project-root <TARGET_PROJECT_ROOT>`. Reconstruct intent provenance (established, inferred, proposed, observed, unresolved), map authority, reconcile work graph, and propose the IEPE overlay. Do not modify files.
2. **Stage 2 (Apply):** Once the reconciliation report and adoption plan are approved, apply the overlay under explicit mutation authority on an isolated branch. Preserve existing valid local authority.

### New Project Initialization
1. Require project ID, name, originating intent, IEPE source, and immutable revision.
2. Run `tools/init_project.py new` from the pinned IEPE source.
3. Preserve existing files unless the user explicitly authorizes replacement.
4. Validate the protocol reference and project profile.
5. Complete the initialization gates before making an issue Ready.
6. Hand off to the first operational agent with `.agents/NEW_AGENT_PROMPT.md` for read-only reconciliation.

Return created or inspected artifacts, unresolved authority, evidence gaps, and the next authorized action.

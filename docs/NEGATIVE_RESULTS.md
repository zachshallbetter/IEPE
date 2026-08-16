# Retained Negative Results and Incident Records

> Governing Protocol: [`PROTOCOL.md`](PROTOCOL.md#condition-classification-taxonomy)  
> Retained Memory: Institutional Memory & Regression Fixtures

---

## Incident IEPE-INCIDENT-001: SES Governance Livelock

### Context & Description
During initial adoption of the Semantic Expression System (SES) project under IEPE, an operational agent entered an indefinite governance livelock. The agent remained active across multiple attempts but could not advance state because:
1. Read-only discovery became an indefinite mode rather than a bounded first phase.
2. Initialization was coupled to named promotion authority (`promotionAuthorities`), blocking provisional local file creation.
3. User authorization and environment capability were conflated (user authorized work, but filesystem environment was read-only).
4. The coordinator lacked blocker deduplication, repeatedly discovering the same non-retryable blocker (`ENV_WORKSPACE_READ_ONLY`) and retrying without state change.

### Disproven Hypotheses
- **Hypothesis 1:** Prompting an agent with expanded user authorization can resolve a physical filesystem capability restriction (`CAPABILITY_MISSING`).  
  *Disposition:* Disproven. Environment capability checks MUST precede discovery/planning and fail fast (`ENV_WORKSPACE_READ_ONLY`).
- **Hypothesis 2:** Promotion authority is required to initialize a local, reversible project operating layer.  
  *Disposition:* Disproven. Initialization authority and promotion authority are separate. Unassigned promotion authority yields `"profileStatus": "provisional"`.
- **Hypothesis 3:** Retrying a non-retryable blocker after re-reading the prompt will yield progress.  
  *Disposition:* Disproven. Non-retryable blockers MUST be fingerprinted (`code:scope`) and immediately transition the coordinator to `WAITING_EXTERNAL`.

### Protocol Invariants Established
- **Preflight Capability Probing:** Environment capability probes (e.g. workspace write test) must execute before discovery and preparation.
- **Condition Classification Taxonomy:** Distinguishes `AUTHORIZATION_MISSING`, `CAPABILITY_MISSING`, `EVIDENCE_MISSING`, `INPUT_MISSING`, `WORK_UNAVAILABLE`, and `EXTERNAL_EVENT_PENDING`.
- **Blocker Fingerprint Deduplication:** `code:scope` fingerprints halt retries immediately and transition the coordinator to `WAITING_EXTERNAL`.

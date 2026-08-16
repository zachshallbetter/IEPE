---
name: operate-iepe-project
description: Run the IEPE coordinator loop for authorized project work. Use when selecting, claiming, dispatching, evaluating, recording, and closing agent-executed issues under a project profile.
---

# Operate an IEPE Project

Read `docs/COORDINATOR.md` from the pinned IEPE source and the local `PROJECT_PROFILE.json`.

Run the state sequence:

```text
preflight -> reconcile -> select -> validate -> claim -> assemble context
-> dispatch -> observe -> evaluate -> disposition -> record -> close loop
```

Require a complete Ready issue before a claim. Bind each dispatch to issue, claim, context digest, worker, role, permissions, and attempt. Do not expand permissions through an adapter. Preserve negative and inconclusive results. Release the claim at terminal disposition.

Stop with a typed blocker when any gate loses authority, context, ownership, dependency validity, permission, evaluator availability, provider health, or recovery.

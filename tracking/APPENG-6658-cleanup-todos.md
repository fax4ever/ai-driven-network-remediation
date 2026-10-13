---
parent: APPENG-6658
title: Clean up TODOs in Network Remediation codebase
status: open
---

# Clean up TODOs in Network Remediation codebase

Sub-task of APPENG-6658: Validate Network Remediation use case for AI-driven
network remediation quickstart.

Review and remove TODOs that have already been addressed in the Network side of
the codebase. For any TODOs that represent genuine pending work, create dedicated
issues to track them.

## Application Logic TODOs

1. ~~`hub/agent-service/src/agent_service/nodes/lightspeed.py:271` — remove stub once LIGHTSPEED_URL is always set in deployment~~ **STALE** — the stub is legitimate; "no Lightspeed" is a valid deployment config (Helm defaults to `url: ""`). Just remove the TODO comment.
2. ~~`hub/agent-service/src/agent_service/nodes/lightspeed.py:323` — validate playbook ops before AAP submission (block dangerous modules: delete, shell, command)~~ **STALE** — auto-executing AI-generated playbooks is the design choice; a module denylist is a half-measure that doesn't change the fundamental tradeoff. Just remove the TODO comment.
3. ~~`hub/agent-service/src/agent_service/nodes/lightspeed.py:396` — raise or log error when `rca` is None instead of falling back to defaults silently~~ **STALE** — the pipeline guarantees the analysis exists at this point; the `else "Unknown"` is dead code, and "Unknown" is a reasonable fallback regardless. Just remove the TODO comment.
4. `hub/agent-service/src/agent_service/nodes/rag_retrieval.py:43` — validate that a generated playbook actually solved the problem before storing — **ENHANCEMENT**, not a bug. Keep as TODO or track separately.
5. `hub/agent-service/src/agent_service/nodes/rag_retrieval.py:51` — consider enriching ALS prompt to return explanation alongside playbook — **ENHANCEMENT**, not a bug. Keep as TODO or track separately.

## Production-Readiness TODOs (Kafka Helm chart)

Not applicable for a quickstart — these are "what you'd change for prod" notes, not actionable items.

6. `hub/helm/charts/kafka/templates/kafka.yaml:83` — derive Kafka node ID from pod ordinal for replicas > 1
7. `hub/helm/charts/kafka/templates/kafka.yaml:86` — generate quorum voter list for all replicas
8. `hub/helm/charts/kafka/values.yaml:3` — set replicas to 3 for HA
9. `hub/helm/charts/kafka/values.yaml:4` — generate unique Kafka cluster ID
10. `hub/helm/charts/kafka/values.yaml:18` — increase resource limits for production

## Summary

- **3 stale TODOs** (#1, #2, #3) — remove the comments, code is correct as-is
- **2 enhancements** (#4, #5) — genuine future improvements, keep or track separately
- **5 production-readiness** (#6–#10) — expected for a quickstart, no action needed

## Acceptance Criteria

- All resolved TODOs removed from the codebase
- Any remaining TODOs either addressed or tracked in dedicated issues

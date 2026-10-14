---
parent: APPENG-6670
title: Integration test failures — model inference unreachable from cluster
status: open
---

# Integration test failures — model inference unreachable from cluster

## Test results (2026-10-14)

- **41 passed** — health checks, MCP server tools, chatbot endpoints, LlamaStack toolgroup registration, vector store, ingestion
- **5 failed** — all involve the agent-service pipeline which requires large language model inference
- **12 skipped** — LokiStack-related (expected, disabled by default)
- **1 rerun** — test_kafka_agent_loop (marked flaky, failed on both attempts)

## Failed tests

| Test | Failure |
|---|---|
| `test_kafka_agent_loop` | Polled 120s, 0 entries in incident_movie — pipeline never completed |
| `test_high_confidence_remediates` | httpx.ReadTimeout on POST /remediate |
| `test_high_confidence_generation_type_routes_to_lightspeed` | httpx.ReadTimeout on POST /remediate |
| `test_mid_confidence_escalates` | httpx.ReadTimeout on POST /remediate |
| `test_low_confidence_escalates` | httpx.ReadTimeout on POST /remediate |

## Root cause

LlamaStack cannot reach the external model serving endpoint from inside the cluster.

- **Endpoint:** `https://maas-rhdp.apps.maas.redhatworkshops.io/v1`
- **Model:** `granite-3-2-8b-instruct` (registered in LlamaStack as `adnr-llm/granite-3-2-8b-instruct`)
- **From local machine:** endpoint responds correctly (HTTP 200, model listed)
- **From LlamaStack pod:** `openai.APIConnectionError: Connection error.`

The model name configuration is correct across all components:
- LlamaStack registration: `adnr-llm/granite-3-2-8b-instruct`
- agent-service `GRANITE_MODEL_NAME`: `adnr-llm/granite-3-2-8b-instruct`

All 5 test failures are caused by the same issue — the agent pipeline calls the large language model for investigation and analysis, and every call times out because LlamaStack cannot connect to the inference endpoint.

## Conclusion

This is an infrastructure/networking issue on the `ai-dev02` cluster, not a code issue. Possible causes:
- Egress network restrictions blocking outbound HTTPS
- DNS resolution failure for external hosts from within the cluster
- Missing proxy configuration

## Additional fix

Updated `docs/rest/rest-commands.md`: corrected model name from `granite-32-8b-vllm` to `granite-3-2-8b-instruct` to match the actual model served by the endpoint.

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

The network is reachable — DNS resolves, TCP connects, TLS completes, and curl
with the API token returns HTTP 200 from inside the LlamaStack pod. The issue is
at the HTTP client level: LlamaStack's Python openai client (via httpx) gets
`RemoteProtocolError: Server disconnected without sending a response` on every
`POST /v1/chat/completions`, while curl to the same endpoint succeeds.

- **Endpoint:** `https://maas-rhdp.apps.maas.redhatworkshops.io/v1`
- **Model:** `granite-3-2-8b-instruct` (registered in LlamaStack as `adnr-llm/granite-3-2-8b-instruct`)
- **From LlamaStack pod (curl with token):** HTTP 200, model listed
- **From LlamaStack pod (curl without token):** HTTP 401
- **From LlamaStack pod (Python openai client):** `Server disconnected without sending a response`

The LlamaStack config (`run-config` ConfigMap) has the correct `api_token` field,
and the code path (`vllm/config.py` → `vllm.py:get_api_key()` →
`openai_mixin.py:client` property) correctly passes it to `AsyncOpenAI(api_key=...)`.

Health checks, vector store operations, and tool-runtime calls all succeed (200 OK).
Only outbound inference calls to MaaS fail.

### Exception chain (from LlamaStack pod logs)

```
httpcore.RemoteProtocolError: Server disconnected without sending a response.

The above exception was the direct cause of the following exception:

httpx.RemoteProtocolError: Server disconnected without sending a response.

The above exception was the direct cause of the following exception:

openai.APIConnectionError: Connection error.
```

### Key stack frames

```
llama_stack/providers/utils/inference/openai_mixin.py:427 in openai_chat_completion
    resp = await self.client.chat.completions.create(**request_params)

openai/resources/chat/completions/completions.py:2814 in create
    return await self._post(...)

openai/_base_client.py:1683 in request
    raise APIConnectionError(request=request) from err

httpx/_transports/default.py:118 in map_httpcore_exceptions
    raise mapped_exc(message) from exc

httpcore/_async/http11.py:231 in _receive_event
    raise RemoteProtocolError(msg)
```

The same issue affects the telco use case — see APPENG-6466-silent-degradation.md.

## Conclusion

This is a client-level issue between LlamaStack's httpx-based openai client and
the MaaS endpoint. The network path is functional (proven by curl). The root cause
is still under investigation — likely related to how the httpx async transport
handles the connection differently from curl.

## Additional fix

Updated `docs/rest/rest-commands.md`: corrected model name from `granite-32-8b-vllm` to `granite-3-2-8b-instruct` to match the actual model served by the endpoint.

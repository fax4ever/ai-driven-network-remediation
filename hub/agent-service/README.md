# Agent Service

Minimal LangGraph-backed REST service using LlamaStack.

## Required environment

Set these variables before running the service:

- `LLAMASTACK_HOST` - hostname for the LlamaStack API. Defaults to `llamastack`.
- `LLAMASTACK_PORT` - port for the LlamaStack API. Defaults to `8321`.
- `LLAMASTACK_MODEL` - model identifier to send with the chat completion request.
- `AGENT_SYSTEM_PROMPT` - optional system prompt. Defaults to `You are a network remediation assistant.`

## Run locally

From `hub/agent-service`:

```bash
uv run agent-service
```

The service listens on port `8000`.

### Endpoints

- `GET /health` returns `{"status": "ok"}`.
- `POST /v1/respond` accepts `{"user_request": "..."}` and returns `{"response_text": "..."}`.

Example request:

```bash
curl -X POST http://localhost:8000/v1/respond \
  -H 'Content-Type: application/json' \
  -d '{"user_request":"Summarize the remediation plan for a failed switch port"}'
```

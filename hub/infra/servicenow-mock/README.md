# ServiceNow Mock

Lightweight FastAPI server simulating the ServiceNow REST Table API for CI and local development. Uses the same API contract as a real ServiceNow instance (Basic Auth, flat JSON payloads, `sysparm_query` lookups).

## Running Locally

```bash
uv sync --group dev
uv run uvicorn main:app --host 0.0.0.0 --port 8080
```

## Running Tests

```bash
uv sync --group dev
uv run pytest -v
```

Also included in `make unit-tests` from the repo root.

## Deploying to a Cluster

```bash
# Via Makefile (builds, pushes, deploys)
make build-push-servicenow-mock deploy-servicenow-mock

# Or as part of full install
ENABLE_SERVICENOW_MOCK=true make helm-install
```

## API Surface

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/now/table/incident` | POST | Create incident (flat JSON body) |
| `/api/now/table/incident/{sys_id}` | PATCH | Update incident by sys_id |
| `/api/now/table/incident` | GET | List/query incidents (`sysparm_query`, `sysparm_limit`, `sysparm_fields`) |
| `/api/now/table/sys_user` | GET | Lookup user |
| `/api/now/table/sys_user` | POST | Create user |
| `/healthz` | GET | Readiness probe |

Auth: HTTP Basic Auth (configurable via `SERVICENOW_USERNAME` / `SERVICENOW_PASSWORD` env vars, default `admin`/`admin`).

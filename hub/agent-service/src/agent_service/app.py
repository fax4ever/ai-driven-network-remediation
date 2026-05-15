from fastapi import FastAPI, HTTPException

from agent_service.workflow import run_workflow

app = FastAPI(
    title="Agent Service",
    description="Minimal LangGraph-backed agent service",
    version="0.1.0",
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/respond")
async def respond(payload: dict[str, str]) -> dict[str, str]:
    user_request = payload.get("user_request", "").strip()
    if not user_request:
        raise HTTPException(status_code=400, detail="user_request is required")

    try:
        result = run_workflow(user_request=user_request)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate response",
        ) from exc

    response_text = result.get("response_text", "").strip()
    if not response_text:
        raise HTTPException(
            status_code=500,
            detail="Workflow returned an empty response",
        )

    return {"response_text": response_text}

def test_health(agent_service_client):
    response = agent_service_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_respond(agent_service_client):
    response = agent_service_client.post(
        "/v1/respond",
        json={"user_request": "Reply with a short remediation summary."},
    )

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload.get("response_text"), str)
    assert payload["response_text"].strip()

import os

import httpx
import pytest


@pytest.fixture(scope="session")
def agent_service_client():
    base_url = os.environ.get("AGENT_SERVICE_URL", "http://localhost:8090")
    with httpx.Client(base_url=base_url) as client:
        yield client

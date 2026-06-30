import os

import pytest


def _find_connector(connectors, connector_id: str):
    return next(
        (c for c in connectors if c.get("connector_id") == connector_id),
        None,
    )


def _assert_mcp_connector(connectors, connector_id: str, service_name: str):
    connector = _find_connector(connectors, connector_id)
    assert connector is not None, f"connector {connector_id} not found"
    assert connector["connector_type"] == "mcp"
    assert connector["url"].endswith("/mcp")
    assert service_name in connector["url"]


@pytest.mark.parametrize(
    ("connector_id", "service_name"),
    [
        ("mcp::noc-openshift", "mcp-noc-openshift"),
        ("mcp::noc-kafka", "mcp-noc-kafka"),
        ("mcp::noc-aap", "mcp-noc-aap"),
        ("mcp::noc-slack", "mcp-noc-slack"),
        ("mcp::noc-servicenow", "mcp-noc-servicenow"),
    ],
)
def test_ogx_registers_mcp_connectors(llamastack_client, connector_id: str, service_name: str):
    """Verify MCP servers are registered as connectors in the OGX config."""
    response = llamastack_client.get("/v1/admin/connectors")
    assert response.status_code == 200

    data = response.json()
    connectors = data.get("data", data)

    _assert_mcp_connector(connectors, connector_id, service_name)


@pytest.mark.skipif(
    os.environ.get("ENABLE_LOKISTACK", "false").lower() != "true",
    reason="LokiStack MCP server is optional and not deployed by default",
)
def test_ogx_registers_lokistack_mcp_connector(llamastack_client):
    """Verify optional LokiStack MCP connector is registered when enabled."""
    response = llamastack_client.get("/v1/admin/connectors")
    assert response.status_code == 200

    data = response.json()
    connectors = data.get("data", data)

    _assert_mcp_connector(connectors, "mcp::noc-lokistack", "mcp-noc-lokistack")

---
parent: APPENG-6658
title: Fix flaky tests in Network Remediation test suite
status: open
---

# Fix flaky tests in Network Remediation test suite

Sub-task of APPENG-6658: Validate Network Remediation use case for AI-driven
network remediation quickstart.

Review and fix the flaky tests on the Network side (e.g. LokiStack-related tests).
The goal is to have a reliable, deterministic test suite.

## Flaky tests

- `hub/integration-tests/tests/network/kafka/test_agent_loop.py:93` — marked with `@pytest.mark.flaky(reruns=1)`. This is the full E2E test: triggers a demo scenario via the chatbot API, publishes to Kafka `system-alerts`, then polls for the agent to consume and write to `incident-audit`. Flaky because it depends on async Kafka consumption with a polling timeout — inherently timing-sensitive.

## Conditional skips (legitimate — no action needed)

These guard tests for optional or environment-dependent components. Correct test design, not broken tests.

- `hub/integration-tests/tests/network/test_llamastack_toolgroups.py:43` — skip if `ENABLE_NETWORK_REMEDIATION != true` (OpenShift MCP only deployed in network-remediation environments)
- `hub/integration-tests/tests/network/test_llamastack_toolgroups.py:57` — skip if `ENABLE_LOKISTACK != true` (LokiStack is optional, not deployed by default)
- `hub/integration-tests/tests/network/mcp_servers/test_kafka_tools.py:41` — `pytest.skip()` if Kafka topic seeding fails in fixture
- `hub/integration-tests/tests/network/mcp_servers/conftest.py:133` — `pytest.skip()` if LokiStack is disabled

## Acceptance Criteria

- Flaky E2E test fixed to pass reliably without reruns
- Conditional skips reviewed and confirmed as legitimate

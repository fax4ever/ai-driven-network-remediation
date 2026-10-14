---
parent: APPENG-6670
title: "Fabio's Deployment Model — Network Remediation use case"
status: complete
---

# Deployment Model — Network Remediation use case

## Table 1 — Infrastructural Deployments

| Component | Kind | Responsibility | Interactions |
|---|---|---|---|
| Kafka | StatefulSet | Message broker for alerts and audit events | agent-service, chatbot-service, MCP Kafka |
| pgvector | StatefulSet | PostgreSQL with vector extensions — vector store backend | LlamaStack |
| LlamaStack | Deployment | AI gateway — routes large language model calls, hosts vector stores, registers MCP toolgroups | agent-service, chatbot-service, ingestion-pipeline, pgvector, external inference endpoint |
| S4 | Deployment | S3-compatible object storage — stores runbook documents | ingestion-pipeline |
| Ansible Automation Platform Mock | Deployment | Simulates Ansible Automation Platform controller for demo and testing | MCP Ansible Automation Platform |
| ServiceNow Mock | Deployment | Simulates ServiceNow for demo and testing | MCP ServiceNow |

## Table 2 — Application-Specific Deployments

| Component | Kind | Responsibility | Interactions |
|---|---|---|---|
| agent-service | Deployment | LangGraph incident pipeline — consumes alerts, runs analysis, routes to remediate, lightspeed, or escalate | Kafka, LlamaStack, all 4 MCP servers |
| chatbot-service | Deployment | Dashboard backend for frontend — incident movie, demo trigger, chat | Kafka, LlamaStack, all 4 MCP servers |
| frontend | Deployment | React single page application — network operations center dashboard | chatbot-service |
| ingestion-pipeline | Deployment | Uploads runbook files from S4 into LlamaStack vector store on startup | S4, LlamaStack |
| MCP OpenShift | Deployment | OpenShift command line wrapper — pods, events, logs, restart, patch | OpenShift (edge cluster) |
| MCP Kafka | Deployment | Kafka produce, consume, and lag tools | Kafka |
| MCP Ansible Automation Platform | Deployment | Job templates, launch, status | Ansible Automation Platform (or mock) |
| MCP ServiceNow | Deployment | Incident create, read, update, resolve | ServiceNow (or mock) |

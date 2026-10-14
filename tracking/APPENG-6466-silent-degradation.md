---
parent: APPENG-6466
title: "Telco services silently degrade when LLM inference is unavailable"
status: open
---

# Telco services silently degrade when LLM inference is unavailable

## Problem

When LlamaStack cannot reach the external model inference endpoint, two telco
services swallow the failure and report success — masking the fact that the LLM
never ran.

## Affected services

### 1. ran-chatbot-service — fallback reply

**`hub/ran-chatbot-service/src/ran_chatbot_service/chat.py:124-126`**

`call_model()` wraps the LLM call in a bare `except Exception` and returns
`("", ModelSource.UNREACHABLE)`. The downstream `format_chat_reply()` (line 154)
substitutes a canned string:
`"Live model unavailable; using deterministic operational fallback."`

The integration test `test_chat` does not catch this because it only asserts
response shape — it accepts `model.source = "unreachable"` and the fallback
reply as valid.

### 2. ran-rca-service — unenriched analysis

**`hub/ran-rca-service/src/ran_rca_service/nodes/analyze.py:167-169`**

`analyze_node()` wraps the LLM call in a bare `except Exception` and returns:
```python
{"root_cause_category": "unknown", "root_cause": "", "recommended_fix": ""}
```

This "unknown" category flows into the remediation service, where
`decide_node()` (`ran-remediation-service/nodes/decide.py:18,23`) maps it to the
`ran-generic-remediation` AAP template and launches a job as if analysis
succeeded.

**Result:** the full telco pipeline (detect → RCA → remediate) completes green
without any LLM involvement.

## Recommendation

- ran-chatbot-service: `test_chat` should assert `data["model"]["source"] == "live"`.
- ran-rca-service: `analyze_node` should propagate the failure or mark the result
  so downstream consumers know the analysis was not LLM-backed.

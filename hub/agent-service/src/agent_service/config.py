import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AgentConfig:
    llamastack_host: str
    llamastack_port: int
    llamastack_model: str
    system_prompt: str

    @classmethod
    def from_env(cls) -> "AgentConfig":
        return cls(
            llamastack_host=os.environ.get("LLAMASTACK_HOST", "llamastack"),
            llamastack_port=int(os.environ.get("LLAMASTACK_PORT", "8321")),
            llamastack_model=os.environ.get("LLAMASTACK_MODEL", "unset-model"),
            system_prompt=os.environ.get(
                "AGENT_SYSTEM_PROMPT",
                "You are a network remediation assistant.",
            ),
        )

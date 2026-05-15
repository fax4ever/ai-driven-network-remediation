from dataclasses import dataclass
from typing import Any, Callable

from llama_stack_client import LlamaStackClient
from agent_service.config import AgentConfig


@dataclass(frozen=True)
class LlamaStackResponse:
    text: str


class LlamaStackClientAdapter:
    def __init__(
        self,
        config: AgentConfig,
        client_factory: Callable[..., Any] = LlamaStackClient,
    ) -> None:
        self._config = config
        self._client = client_factory(
            base_url=f"http://{config.llamastack_host}:{config.llamastack_port}",
        )

    def generate(self, user_request: str) -> LlamaStackResponse:
        response = self._client.chat.completions.create(
            model=self._config.llamastack_model,
            messages=[
                {"role": "system", "content": self._config.system_prompt},
                {"role": "user", "content": user_request},
            ],
        )
        return LlamaStackResponse(
            text=_extract_response_text(response),
        )


def _extract_response_text(response: Any) -> str:
    first_choice = response.choices[0]
    return first_choice.message.content

from typing import NotRequired, TypedDict


class AgentState(TypedDict):
    user_request: str
    response_text: NotRequired[str]

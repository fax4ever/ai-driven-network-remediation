from langgraph.graph import END, START, StateGraph

from agent_service.clients.llamastack import LlamaStackClientAdapter
from agent_service.config import AgentConfig
from agent_service.state import AgentState


def build_workflow(config: AgentConfig | None = None):
    workflow_config = config or AgentConfig.from_env()
    graph = StateGraph(AgentState)
    graph.add_node("respond", _respond(workflow_config))
    graph.add_edge(START, "respond")
    graph.add_edge("respond", END)
    return graph.compile()


def run_workflow(user_request: str, config: AgentConfig | None = None) -> AgentState:
    workflow = build_workflow(config=config)
    return workflow.invoke({"user_request": user_request})


def _respond(config: AgentConfig):
    client = LlamaStackClientAdapter(config)

    def _run(state: AgentState) -> AgentState:
        result = client.generate(state["user_request"])
        return {
            "user_request": state["user_request"],
            "response_text": result.text,
        }

    return _run

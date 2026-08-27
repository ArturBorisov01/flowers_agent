from agents.registry import get_agent_graph
from agents.state import AgentState


async def chat_generation(
    message: str,
    agent_name: str,
    summary: str | None = None,
    customer: dict | None = None,
    channel: dict | None = None,
) -> dict:
    graph = get_agent_graph(agent_name)

    initial_state: AgentState = {
        "message": message,
        "summary": summary or "",
        "customer": customer or {},
        "channel": channel or {},
        "agent_name": agent_name,
        "escalate": False,
    }

    final_state = await graph.ainvoke(initial_state)

    return {
        "message": final_state.get("reply", ""),
        "summary": final_state.get("summary", ""),
        "escalate": final_state.get("escalate", False),
        "agent_name": agent_name,
    }
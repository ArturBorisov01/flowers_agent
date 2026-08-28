# services\chat_generation.py
from langchain_core.messages import HumanMessage
from agents.registry import get_agent_graph


async def chat_generation(message: str, agent_name: str, summary: str | None = None, customer: dict | None = None, channel: dict | None = None) -> dict:
    graph = get_agent_graph(agent_name)

    initial_state = {
        "messages": [HumanMessage(content=message)],
        "summary": summary or "",
        "customer": customer or {},
        "channel": channel or {},
        "agent_name": agent_name,
        "escalate": False,
    }
    print("Debug_chat_generation_input", initial_state)
    print()

    final_state = await graph.ainvoke(initial_state)
    last_ai_message = final_state["messages"][-1]

    print("Debug_chat_generation_output", last_ai_message)
    print()
    return {
        "message": last_ai_message.content,
        "summary": final_state.get("summary", ""),
        "escalate": final_state.get("escalate", False),
        "agent_name": agent_name,
    }
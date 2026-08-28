# agents\common\nodes\assistant.py
from langchain_core.messages import SystemMessage
from agents.state import AgentState

def make_assistant_node(llm_with_tools, system_prompt: SystemMessage):
    async def assistant(state: AgentState) -> dict:
        print("→ NODE: assistant")
        messages = [system_prompt]

        if state.get("summary"):
            messages.append(
                SystemMessage(content=f"Контекст предыдущего диалога с этим клиентом: {state['summary']}")
            )

        messages += state["messages"]
        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}

    return assistant
# agents\common\edges.py
from agents.state import AgentState


def route_after_spam_check(state: AgentState) -> str:
    return "spam" if state.get("is_spam") else "ok"


def route_after_assistant(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return "summary"
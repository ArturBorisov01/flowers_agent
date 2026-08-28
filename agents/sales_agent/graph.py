# agents\sales_agent\graph.py
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition, ToolNode

from agents.state import AgentState
from agents.common.nodes.spam_filter import check_spam, handle_spam
from agents.common.nodes.assistant import make_assistant_node
from agents.common.nodes.summarizer import build_summary
from agents.common.edges import route_after_spam_check, route_after_assistant
from agents.sales_agent.tools import TOOLS
from agents.sales_agent.prompts import SALES_SYSTEM_PROMPT
from services.llm_client import llm


def build_graph():
    llm_with_tools = llm.bind_tools(TOOLS, parallel_tool_calls=False)

    graph = StateGraph(AgentState)

    graph.add_node("check_spam", check_spam)
    graph.add_node("handle_spam", handle_spam)
    graph.add_node("assistant", make_assistant_node(llm_with_tools, SALES_SYSTEM_PROMPT))
    graph.add_node("tools", ToolNode(TOOLS))
    graph.add_node("build_summary", build_summary)

    graph.add_edge(START, "check_spam")

    graph.add_conditional_edges(
        "check_spam",
        route_after_spam_check,
        {"spam": "handle_spam", "ok": "assistant"},
    )

    graph.add_conditional_edges(
        "assistant", 
        route_after_assistant,
        {"tools": "tools", "summary": "build_summary"})
    # route_after_assistant проверяет tool_calls в последнем сообщении:
    # если модель просит тул -> "tools", если дала финальный ответ -> "summary"

    graph.add_edge("tools", "assistant")
    graph.add_edge("handle_spam", END)

    return graph.compile()
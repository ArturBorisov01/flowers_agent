from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.common.nodes.spam_filter import check_spam, handle_spam
from agents.common.nodes.tool_caller import make_tool_caller_node
from agents.common.nodes.summarizer import build_summary
from agents.common.edges import route_after_spam_check
from agents.sales_agent.tools import TOOLS, TOOL_FUNCTIONS


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("check_spam", check_spam)
    graph.add_node("handle_spam", handle_spam)
    graph.add_node("call_tools", make_tool_caller_node(TOOLS, TOOL_FUNCTIONS))
    graph.add_node("build_summary", build_summary)

    graph.set_entry_point("check_spam")

    graph.add_conditional_edges(
        "check_spam",
        route_after_spam_check,
        {"spam": "handle_spam", "ok": "call_tools"},
    )

    graph.add_edge("handle_spam", END)


    graph.add_edge("call_tools", "build_summary")
    graph.add_edge("build_summary", END)

    return graph.compile()
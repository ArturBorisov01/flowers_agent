import os
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter

load_dotenv()
os.getenv("OPENROUTER_API_KEY")

model = ChatOpenRouter(
    model = os.getenv("MODEL_NAME"),
    temperature=0,
    max_tokens=1024,
    max_retries=2,
    # other params...
)



from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition


def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

def subtraction(a: int, b: int) -> int:
    """Subtraction a and b.

    Args:
        a: first int
        b: second int
    """
    return a - b

llm_with_tools = model.bind_tools([multiply, subtraction])
    
# Node
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([multiply, subtraction]))
builder.add_edge(START, "tool_calling_llm")
builder.add_edge("tool_calling_llm", END)

builder.add_conditional_edges(
    "tool_calling_llm",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)

graph = builder.compile()

messages = graph.invoke({"messages": HumanMessage(content="Hello!")})
for m in messages['messages']:
    m.pretty_print()

messages = graph.invoke({"messages": HumanMessage(content="Multiply 2 and 3")})
for m in messages['messages']:
    m.pretty_print()

messages = graph.invoke({"messages": HumanMessage(content="Subtraction 2 and 3")})
for m in messages['messages']:
    m.pretty_print()
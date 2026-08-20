import os
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter


os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "langchain-academy"

load_dotenv()
os.getenv("OPENROUTER_API_KEY")

llm = ChatOpenRouter(
    model = os.getenv("MODEL_NAME"),
    temperature=0,
    max_tokens=1024,
    max_retries=2,
    # other params...
)


def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

# This will be a tool
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b

def subtract(a: float, b: float) -> float:
    """subtract a and b.

    Args:
        a: first float
        b: second float
    """
    return a - b



tools = [add, subtract, multiply, divide]
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)



from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage

# System message
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

# Node
def assistant(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode

# Graph
builder = StateGraph(MessagesState)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")
react_graph = builder.compile()

messages = [HumanMessage(content="Add 3 and 4.")]
# messages = react_graph.invoke({"messages": messages})
# for m in messages['messages']:
#     m.pretty_print()

messages = [HumanMessage(content="Multiply that by 2.")]
# messages = react_graph.invoke({"messages": messages})
# for m in messages['messages']:
#     m.pretty_print()

# ===============
# About thread_id
# ===============
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
# react_graph_memory = builder.compile(checkpointer=memory)
react_graph_memory = builder.compile()

# Specify a thread
config = {"configurable": {"thread_id": "1"}}

# Specify an input
messages = [HumanMessage(content="Add 3 and 4.")]

# Run
# messages = react_graph_memory.invoke({"messages": messages},config)
# for m in messages['messages']:
#     m.pretty_print()

messages = [HumanMessage(content="Multiply that by 2.")]
# messages = react_graph_memory.invoke({"messages": messages}, config)
# for m in messages['messages']:
#     m.pretty_print()    
